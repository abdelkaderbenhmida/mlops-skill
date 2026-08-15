"""Optuna hyperparameter optimisation with nested MLflow runs.

Each Optuna trial is logged as a *nested* MLflow run under the parent search
run, so the whole search space is comparable in the MLflow UI via parallel
coordinates. Uses the default TPE (bayesian) sampler.
"""

from __future__ import annotations

import argparse
import logging

import mlflow
import optuna
import pandas as pd
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score

from src.config import MLFLOW_DIR

logger = logging.getLogger(__name__)


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    from src.models.train import load_training_data

    return load_training_data()


def objective(trial, X, y):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),
        "max_depth": trial.suggest_int("max_depth", 3, 20),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
        "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2", None]),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 15),
    }

    model = RandomForestClassifier(**params, random_state=42)
    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        cv_score = cross_val_score(
            model, X, y, cv=StratifiedKFold(3), scoring="f1", n_jobs=-1
        ).mean()
        mlflow.log_metric("cv_f1", cv_score)
        trial.report(cv_score, step=0)
    return cv_score


def tune(n_trials: int = 50, experiment_name: str = "churn_optuna") -> dict:
    """Run a bayesian search; return best params / value / study."""
    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment(experiment_name)

    X, y = load_data()

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(seed=42),
        study_name="churn_rf_bayesian",
    )

    with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):
        mlflow.log_param("n_trials", n_trials)
        mlflow.log_param("sampler", "TPE")
        study.optimize(
            lambda t: objective(t, X, y), n_trials=n_trials, show_progress_bar=False
        )
        mlflow.log_metric("best_cv_f1", study.best_value)
        mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})

    logger.info("Best trial: %.4f with %s", study.best_value, study.best_params)
    return {"best_params": study.best_params, "best_value": study.best_value}


def main() -> None:
    parser = argparse.ArgumentParser(description="Optuna tuning for the churn model.")
    parser.add_argument("--trials", type=int, default=50)
    parser.add_argument("--experiment", default="churn_optuna")
    args = parser.parse_args()

    result = tune(n_trials=args.trials, experiment_name=args.experiment)
    print(f"Best CV F1: {result['best_value']:.4f}")
    print(f"Best params: {result['best_params']}")


if __name__ == "__main__":
    main()
