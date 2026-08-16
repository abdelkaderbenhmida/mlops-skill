"""ZenML hyperparameter tuning pipeline with Optuna and nested MLflow runs.

Steps:
- load_data: same data loading as training
- tune: Optuna bayesian search (50 trials), each trial logged as nested MLflow run
- log_best: logs best params and score to MLflow
"""
from __future__ import annotations

from zenml import pipeline, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def load_data() -> tuple:
    """Load training data (X, y)."""
    from src.models.train import load_training_data

    return load_training_data()


@step
def tune_hyperparameters(data: tuple, n_trials: int = 50) -> dict:
    """Run Optuna bayesian optimization with nested MLflow runs."""
    import optuna
    import mlflow
    from optuna.samplers import TPESampler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    from src.config import MLFLOW_DIR

    X, y = data

    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment("churn_optuna")

    def objective(trial):
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

    study = optuna.create_study(
        direction="maximize",
        sampler=TPESampler(seed=42),
        study_name="churn_rf_bayesian",
    )

    with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):
        mlflow.log_param("n_trials", n_trials)
        mlflow.log_param("sampler", "TPE")
        study.optimize(
            objective, n_trials=n_trials, show_progress_bar=False
        )
        mlflow.log_metric("best_cv_f1", study.best_value)
        mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})

    logger.info("Best trial: %.4f with %s", study.best_value, study.best_params)
    return {"best_params": study.best_params, "best_value": study.best_value}


@step
def log_best_params(best_result: dict) -> dict:
    """Log the best hyperparameters for downstream use."""
    return best_result


@pipeline
def tuning_pipeline(n_trials: int = 50):
    """Hyperparameter tuning pipeline with Optuna."""
    data = load_data()
    best = tune_hyperparameters(data, n_trials)
    log_best_params(best)


if __name__ == "__main__":
    tuning_pipeline(n_trials=50)