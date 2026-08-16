"""ZenML automated retraining pipeline triggered by drift.

Steps:
- check_drift: read latest drift score from monitoring
- if drift > threshold: re-run full training + tuning + gates
- retrain: training with best params from Optuna
- validate_gates: Deepchecks + Fairlearn (same gates as promotion)
- promote_if_better: only promote if beats current production

This pipeline reuses the same validation gates as manual promotion - no shortcuts.
"""
from __future__ import annotations

from zenml import pipeline, step
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def check_drift() -> dict:
    """Read latest drift score and decide if retraining is needed."""
    from src.monitoring.retraining_trigger import read_drift_score, should_retrain
    from src.config import DRIFT_THRESHOLD

    score = read_drift_score()
    trigger = should_retrain(score, DRIFT_THRESHOLD)
    logger.info(f"Drift check: score={score:.3f}, threshold={DRIFT_THRESHOLD}, trigger={trigger}")
    return {"drift_score": score, "threshold": DRIFT_THRESHOLD, "trigger": trigger}


@step
def retrain_model(drift_info: dict) -> dict:
    """Re-run training with Optuna tuning on recent data if drift detected."""
    if not drift_info.get("trigger", False):
        logger.info("No drift detected - skipping retraining")
        return {"retrained": False, "reason": "no_drift"}

    logger.info("Drift detected - starting retraining pipeline")

    # Run tuning to find best params
    from src.models.tune import tune
    best = tune(n_trials=30, experiment_name="churn_retraining")

    # Train with best params
    from src.models.train import load_training_data, train_and_log
    from sklearn.model_selection import train_test_split

    X, y = load_training_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    result = train_and_log(
        X_train, X_test, y_train, y_test,
        params=best["best_params"],
        run_name="retrained_model",
        experiment_name="churn_retraining",
        register=True,
    )

    return {
        "retrained": True,
        "run_id": result["run_id"],
        "best_params": best["best_params"],
        "best_cv_f1": best["best_value"],
        "test_f1": result["metrics"]["f1_score"],
        "test_accuracy": result["metrics"]["accuracy"],
        "test_roc_auc": result["metrics"]["roc_auc"],
    }


@step
def validate_retrained_model(retrain_result: dict) -> dict:
    """Run Deepchecks and Fairlearn on the retrained model."""
    if not retrain_result.get("retrained", False):
        return {"deepchecks_passed": True, "fairness_passed": True, "skipped": True}

    import joblib
    from src.models.promote import run_deepchecks, _load_test_frame

    model_path = "models/churn_model.joblib"
    model = joblib.load(model_path)
    X_test, y_test = _load_test_frame()

    # Deepchecks
    deepchecks = run_deepchecks(model, X_test, y_test)

    # Fairness
    from src.models.fairness_check import fairness_check
    from pathlib import Path
    fairness = fairness_check(Path(model_path))

    logger.info(f"Deepchecks: {'PASSED' if deepchecks['passed'] else 'FAILED'}")
    logger.info(f"Fairness: {'PASSED' if fairness['passed'] else 'FAILED'}")

    return {
        "deepchecks_passed": deepchecks["passed"],
        "fairness_passed": fairness["passed"],
        "dp_diff": fairness.get("demographic_parity_difference"),
    }


@step
def promote_if_better(validation: dict, retrain_result: dict) -> dict:
    """Promote retrained model if it beats production and passes all gates."""
    if not retrain_result.get("retrained", False):
        return {"promoted": False, "reason": "not_retrained"}

    # Check all gates
    gates = {
        "deepchecks": validation.get("deepchecks_passed", False),
        "fairness": validation.get("fairness_passed", False),
    }

    # Performance gate
    candidate_f1 = retrain_result.get("test_f1", 0)
    from src.config import F1_PROMOTION_THRESHOLD
    gates["performance"] = candidate_f1 >= F1_PROMOTION_THRESHOLD

    # Beats production gate
    from src.models.promote import load_production_model_metrics
    prod_f1 = load_production_model_metrics()
    if prod_f1 is None:
        gates["beats_production"] = True
    else:
        gates["beats_production"] = candidate_f1 > prod_f1 + 0.005

    all_passed = all(gates.values())

    if all_passed:
        from src.models.promote import _move_to_production
        _move_to_production(retrain_result.get("run_id"))
        logger.info("Retrained model promoted to Production")
    else:
        logger.warning(f"Retrained model failed gates: {gates}")

    return {
        "promoted": all_passed,
        "gates": gates,
        "candidate_f1": candidate_f1,
        "production_f1": prod_f1,
    }


@pipeline
def retraining_pipeline():
    """Automated retraining pipeline triggered by drift."""
    drift_info = check_drift()
    retrain_result = retrain_model(drift_info)
    validation = validate_retrained_model(retrain_result)
    promote_if_better(validation, retrain_result)


if __name__ == "__main__":
    retraining_pipeline()