"""Model evaluation: metrics + ROC curve on a held-out test set.

Reusable for any trained model object; logs the results into the current
MLflow run (or a dedicated evaluation run) and saves the ROC curve to
``reports/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import pandas as pd
from sklearn.metrics import (
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

from src.config import MLFLOW_DIR, REPORTS_DIR, F1_PROMOTION_THRESHOLD, AUC_PROMOTION_THRESHOLD


def load_model(path: Path):
    import joblib

    return joblib.load(path)


def evaluate(model, X_test, y_test, log_to_mlflow: bool = True, experiment: str = "fraud_eval") -> dict:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    roc_path = REPORTS_DIR / "roc_curve.png"
    pr_path = REPORTS_DIR / "precision_recall_curve.png"

    fig, ax = plt.subplots()
    RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax)
    ax.set_title("ROC Curve")
    fig.savefig(roc_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots()
    PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=ax)
    ax.set_title("Precision-Recall Curve")
    fig.savefig(pr_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    if log_to_mlflow:
        os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
        mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
        mlflow.set_experiment(experiment)
        with mlflow.start_run(run_name="evaluate"):
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(str(roc_path))
            mlflow.log_artifact(str(pr_path))

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained model.")
    parser.add_argument("--model", default="models/fraud_model.joblib")
    args = parser.parse_args()

    X, y = _load_data()
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = load_model(Path(args.model))
    metrics = evaluate(model, X_test, y_test)

    f1 = metrics["f1_score"]
    auc = metrics["roc_auc"]
    f1_pass = f1 >= F1_PROMOTION_THRESHOLD
    auc_pass = auc >= AUC_PROMOTION_THRESHOLD
    status = "PASS" if (f1_pass and auc_pass) else "FAIL"
    print(f"Evaluation: {metrics}")
    print(f"F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}) {'PASS' if f1_pass else 'FAIL'}")
    print(f"AUC={auc:.4f} (threshold {AUC_PROMOTION_THRESHOLD}) {'PASS' if auc_pass else 'FAIL'}")
    print(f"Overall: {status}")


def _load_data():
    from src.models.train import load_training_data

    return load_training_data()


if __name__ == "__main__":
    main()
