"""AutoML comparative baseline (FLAML).

Trains a baseline with FLAML in a short time budget and logs it to MLflow so
it can be objectively compared against the Optuna-optimised model.
"""

from __future__ import annotations

import argparse
import logging

import mlflow
import pandas as pd
from flaml import AutoML
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.config import MLFLOW_DIR

logger = logging.getLogger(__name__)


def run_automl_baseline(time_budget: int = 60, experiment_name: str = "churn_automl") -> dict:
    X, y = _load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    automl = AutoML()
    automl.fit(
        X_train,
        y_train,
        task="classification",
        time_budget=time_budget,
        metric="f1",
        n_jobs=-1,
        log_file_name="artifacts/automl.log",
    )

    y_pred = automl.predict(X_test)
    y_proba = automl.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred),
    }

    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=f"flaml_baseline_{time_budget}s"):
        mlflow.log_params(automl.best_config)
        mlflow.log_metrics(metrics)
        mlflow.log_param("time_budget", time_budget)
        mlflow.set_tag("tool", "FLAML")
        mlflow.sklearn.log_model(automl.model.estimator, artifact_path="model")

    logger.info("FLAML baseline metrics: %s", metrics)
    return {"metrics": metrics, "best_config": automl.best_config}


def _load_data():
    from src.models.train import load_training_data

    return load_training_data()


def main() -> None:
    parser = argparse.ArgumentParser(description="FLAML AutoML baseline.")
    parser.add_argument("--time-budget", type=int, default=60)
    args = parser.parse_args()
    result = run_automl_baseline(time_budget=args.time_budget)
    print(f"FLAML baseline F1: {result['metrics']['f1_score']:.4f}")


if __name__ == "__main__":
    main()
