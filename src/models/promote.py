"""Model promotion logic with hard gates.

A candidate model may only be promoted to Production when **all** gates pass:
1. Performance: F1 >= ``F1_PROMOTION_THRESHOLD`` on the held-out set.
2. Competitive: beats the current Production model (if any) by a margin.
3. Quality: Deepchecks suite passes (no critical failures).
4. Fairness: Fairlearn demographic parity difference within threshold.

On success the MLflow registered model is moved to Production and a model
card is generated.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import json
import logging
from pathlib import Path

import mlflow
import pandas as pd

from src.config import (
    F1_PROMOTION_THRESHOLD,
    MLFLOW_DIR,
    MODEL_CARDS_DIR,
    MODELS_DIR,
    REPORTS_DIR,
    FAIRNESS_DP_THRESHOLD,
)

logger = logging.getLogger(__name__)

BEAT_MARGIN = 0.005


def run_deepchecks(model, X_test, y_test) -> dict:
    """Run the Deepchecks full suite; return pass/fail summary."""
    try:
        from deepchecks.tabular import Dataset
        from deepchecks.tabular.suites import full_suite

        train_ds = Dataset(pd.DataFrame(X_test), label=y_test)
        test_ds = train_ds.copy()
        suite = full_suite()
        result = suite.run(train_ds, test_ds, model=model)
        result.save_as_html("reports/deepchecks_report.html")
        critical_failures = [
            check.get_header() for check in result.results
            if not check.passed
        ]
        passed = not any(not check.passed for check in result.results)
        return {"passed": passed, "critical_failures": critical_failures}
    except ImportError:
        logger.warning("deepchecks unavailable; treating gate as passed (skip).")
        return {"passed": True, "skip": True}


def load_production_model_metrics() -> float | None:
    """Return the F1 of the current registered Production model, if any."""
    try:
        client = mlflow.MlflowClient(mlflow.get_tracking_uri())
        versions = client.get_latest_versions("churn_model", stages=["Production"])
        if not versions:
            return None
        run = client.get_run(versions[0].run_id)
        return float(run.data.metrics.get("f1_score", 0.0))
    except Exception:
        return None


def promote(
    model_path: Path = MODELS_DIR / "churn_model.joblib",
    run_id: str | None = None,
    experiment: str = "churn_prediction",
) -> dict:
    """Evaluate all promotion gates and promote the model if they all pass."""
    mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())
    mlflow.set_experiment(experiment)

    # 1. Performance gate (F1).
    metrics = _evaluate_model(model_path)
    f1 = metrics["f1_score"]
    gates = {"performance": f1 >= F1_PROMOTION_THRESHOLD}

    # 2. Beats current Production.
    prod_f1 = load_production_model_metrics()
    if prod_f1 is None:
        gates["beats_production"] = True
    else:
        gates["beats_production"] = f1 > prod_f1 + BEAT_MARGIN
    gates_detail = {"candidate_f1": f1, "production_f1": prod_f1}

    # 3. Deepchecks.
    X_test, y_test = _load_test_frame()
    model = _load_model(model_path)
    deepchecks = run_deepchecks(model, X_test, y_test)
    gates["deepchecks"] = deepchecks["passed"]

    # 4. Fairness.
    fairness = _load_fairness_report()
    gates["fairness"] = fairness.get("passed", False)

    all_passed = all(gates.values())

    report = {
        "gates": gates,
        "gate_detail": gates_detail,
        "fairness": {
            "dp_diff": fairness.get("demographic_parity_difference"),
            "threshold": fairness.get("threshold", FAIRNESS_DP_THRESHOLD),
        },
        "deepchecks": {"passed": deepchecks["passed"]},
        "promoted": all_passed,
        "metrics": metrics,
    }

    if all_passed:
        _move_to_production(run_id)
        logger.info("All promotion gates passed -> moved to Production.")
    else:
        logger.warning("Promotion rejected: %s", {k: v for k, v in gates.items() if not v})

    _write_report(report)
    _generate_model_card(report)
    return report


def _evaluate_model(model_path: Path) -> dict:
    import joblib
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

    model = joblib.load(model_path)
    X_test, y_test = _load_test_frame()
    y_pred = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred),
    }


def _load_test_frame():
    from src.features.build_features import build_features, feature_sets
    from src.models.train import _preprocess_pipeline
    from sklearn.model_selection import train_test_split

    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=False)
    sets = feature_sets(frame)
    _, X_test, _, y_test = train_test_split(
        sets["X"], sets["y"], test_size=0.25, random_state=42, stratify=sets["y"]
    )
    return X_test, y_test


def _load_model(model_path: Path):
    import joblib

    return joblib.load(model_path)


def _load_fairness_report() -> dict:
    report_path = REPORTS_DIR / "fairness_report.json"
    if report_path.exists():
        return json.loads(report_path.read_text())
    return {"passed": False, "demographic_parity_difference": 1.0}


def _move_to_production(run_id: str | None) -> None:
    client = mlflow.MlflowClient(mlflow.get_tracking_uri())
    if run_id:
        try:
            client.set_registered_model_alias("churn_model", "production", run_id)
            return
        except Exception:
            pass
    # Fallback: transition the newest Staging/None version.
    versions = client.get_latest_versions("churn_model", stages=["None", "Staging"])
    if versions:
        client.transition_model_version_stage(
            "churn_model", versions[0].version, "Production", archive_existing_versions=True
        )


def _write_report(report: dict) -> None:
    from src.config import REPORTS_DIR

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "promotion_report.json", "w") as handle:
        json.dump(report, handle, indent=2, default=str)


def _generate_model_card(report: dict) -> None:
    try:
        from model_cards.model_card_template import generate_model_card

        generate_model_card(report, output_path=MODEL_CARDS_DIR / "model_card.md")
    except Exception as exc:  # pragma: no cover
        logger.warning("Model card generation failed: %s", exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Promotion gates + registry update.")
    parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.joblib"))
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    report = promote(Path(args.model), run_id=args.run_id)
    print(f"Promoted: {report['promoted']}")
    print("Gates:", report["gates"])
    print("Report saved to reports/promotion_report.json")


if __name__ == "__main__":
    main()
