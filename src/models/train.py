"""
# TODO: high - Add monotonicity constraint enforcement check before promotion
# TODO: medium - Implement SHAP value computation for each prediction
# TODO: low - Add feature importance visualization to evidence pack


# TODO: high - Add monotonicity constraint enforcement check before promotion
# TODO: medium - Implement SHAP value computation for each prediction
# TODO: low - Add feature importance visualization to evidence pack

Model training with full MLflow tracking for churn prediction.

Every training run logs:
- hyperparameters,
- metrics (accuracy, F1, ROC-AUC),
- the model artifact,
- a confusion matrix figure,
- tags linking to the data source hash and pipeline version.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import logging
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.xgboost
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from src.config import (
    MLFLOW_DIR,
    MODELS_DIR,
    RAW_DATA_PATH,
    REPORTS_DIR,
    TARGET_COL,
    F1_PROMOTION_THRESHOLD,
    AUC_PROMOTION_THRESHOLD,
)

logger = logging.getLogger(__name__)

DEFAULT_PARAMS = {
    "n_estimators": 200,
    "max_depth": 12,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
    "n_jobs": -1,
    "device": "cuda",
    "tree_method": "hist",
}


def build_params(y_train: pd.Series, params: dict | None = None) -> dict:
    """Resolve XGBoost params, adding a balanced scale_pos_weight."""
    resolved = dict(params or DEFAULT_PARAMS)
    if "scale_pos_weight" not in resolved:
        n_pos = int((y_train == 1).sum())
        n_neg = int((y_train == 0).sum())
        if n_pos > 0 and n_neg > 0:
            resolved["scale_pos_weight"] = n_neg / n_pos
    return resolved


def fit_xgb(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    params: dict,
) -> XGBClassifier:
    """Fit XGBClassifier on GPU, falling back to CPU if CUDA is unavailable."""
    try:
        model = XGBClassifier(**params)
        model.fit(X_train, y_train)
        return model
    except Exception:
        logger.warning("GPU training failed, falling back to CPU (device=cpu, tree_method=hist)")
        cpu_params = dict(params)
        cpu_params["device"] = "cpu"
        cpu_params["tree_method"] = "hist"
        model = XGBClassifier(**cpu_params)
        model.fit(X_train, y_train)
        return model


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    """Load raw data and build the model-ready feature matrix.

    Goes through ``build_features`` so the id, timestamp and sensitive
    columns are dropped and categoricals are one-hot encoded — the model
    never sees the raw frame.
    """
    from src.data.ingestion import ingest_raw_data
    from src.data.preprocessing import preprocess
    from src.features.build_features import build_features, feature_sets

    raw, _ = ingest_raw_data()
    clean = preprocess(raw)
    frame = build_features(clean, include_sensitive=False)

    sets = feature_sets(frame)
    return sets["X"], sets["y"]


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
    run_name: str = "churn_xgb",
    experiment_name: str = "churn_prediction",
    register: bool = False,
) -> dict:
    """Train an XGBoost (GPU) classifier, log everything to MLflow.

    Returns a dict with the model, metrics and run id for downstream steps.
    """
    params = build_params(y_train, params)
    os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name) as run:
        model = fit_xgb(X_train, y_train, params)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_proba),
        }

        mlflow.log_params(model.get_params())
        mlflow.log_metrics(metrics)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("data_source", str(RAW_DATA_PATH))
        mlflow.set_tag("pipeline", run_name)

        cm_path = REPORTS_DIR / "confusion_matrix.png"
        cm_path.parent.mkdir(parents=True, exist_ok=True)
        save_confusion_matrix(y_test, y_pred, cm_path)
        mlflow.log_artifact(str(cm_path))

        model_dir = MODELS_DIR / f"run_{run.info.run_id}"
        model_dir.mkdir(parents=True, exist_ok=True)
        mlflow.xgboost.log_model(model, artifact_path="model")

        if register:
            mlflow.xgboost.log_model(
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
    parser = argparse.ArgumentParser(description="Train and track the churn prediction model.")
    parser.add_argument("--register", action="store_true", help="Register in MLflow registry.")
    parser.add_argument("--run-name", default="churn_xgb")
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
    auc = result["metrics"]["roc_auc"]
    f1_pass = f1 >= F1_PROMOTION_THRESHOLD
    auc_pass = auc >= AUC_PROMOTION_THRESHOLD
    status = "PASS" if (f1_pass and auc_pass) else "FAIL"
    print(f"Training done. F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}) AUC={auc:.4f} (threshold {AUC_PROMOTION_THRESHOLD}) -> {status}")
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
