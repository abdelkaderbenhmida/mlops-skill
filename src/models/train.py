"""Model training with full MLflow tracking.

Every training run logs:
- hyperparameters,
- metrics (accuracy, F1, ROC-AUC),
- the model artifact,
- a confusion matrix figure,
- tags linking to the data source hash and pipeline version.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.config import (
    MLFLOW_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    TARGET_COL,
    F1_PROMOTION_THRESHOLD,
)
from src.features.build_features import build_features, feature_sets

logger = logging.getLogger(__name__)

DEFAULT_PARAMS = {
    "n_estimators": 200,
    "max_depth": 12,
    "min_samples_leaf": 5,
    "max_features": "sqrt",
    "random_state": 42,
}


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load raw data and build the full feature matrix (sensitive excluded)."""
    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=False)
    sets = feature_sets(frame)
    return sets["X"], sets["y"]


def _preprocess_pipeline(raw: pd.DataFrame) -> pd.DataFrame:
    """Small local preprocess used by training (keeps module self-contained)."""
    from src.data.preprocessing import preprocess

    return preprocess(raw)


def save_confusion_matrix(y_true, y_pred, path: Path) -> None:
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.7)
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, str(val), ha="center", va="center")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def train_and_log(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    params: dict | None = None,
    run_name: str = "churn_rf",
    experiment_name: str = "churn_prediction",
    register: bool = False,
) -> dict:
    """Train a RandomForest classifier, log everything to MLflow.

    Returns a dict with the model, metrics and run id for downstream steps.
    """
    params = params or dict(DEFAULT_PARAMS)
    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_pred),
        }

        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("data_source", "data/raw/dataset.csv")
        mlflow.set_tag("pipeline", run_name)

        cm_path = REPORTS_DIR / "confusion_matrix.png"
        cm_path.parent.mkdir(parents=True, exist_ok=True)
        save_confusion_matrix(y_test, y_pred, cm_path)
        mlflow.log_artifact(str(cm_path))

        model_dir = MODELS_DIR / f"run_{run.info.run_id}"
        model_dir.mkdir(parents=True, exist_ok=True)
        mlflow.sklearn.log_model(model, artifact_path="model")

        if register:
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                registered_model_name="churn_model",
            )

        mlflow.end_run()

    logger.info("Trained model: %s", metrics)
    return {
        "model": model,
        "metrics": metrics,
        "run_id": run.info.run_id,
        "feature_columns": list(X_train.columns),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train and track the churn model.")
    parser.add_argument("--register", action="store_true", help="Register in MLflow registry.")
    parser.add_argument("--run-name", default="churn_rf")
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument("--experiment", default="churn_prediction")
    args = parser.parse_args()

    X, y = load_training_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42, stratify=y
    )
    result = train_and_log(
        X_train, X_test, y_train, y_test,
        run_name=args.run_name,
        experiment_name=args.experiment,
        register=args.register,
    )

    f1 = result["metrics"]["f1_score"]
    status = "PASS" if f1 >= F1_PROMOTION_THRESHOLD else "FAIL"
    print(f"Training done. F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}) -> {status}")
    print(f"MLflow run: {result['run_id']}")

    # Persist model + feature columns for downstream steps.
    import joblib

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(result["model"], MODELS_DIR / "churn_model.joblib")
    with open(MODELS_DIR / "feature_columns.txt", "w") as handle:
        handle.write("\n".join(result["feature_columns"]))
    print("Model saved to models/churn_model.joblib")


if __name__ == "__main__":
    main()
