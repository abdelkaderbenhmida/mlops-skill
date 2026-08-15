"""Fairness audit with Fairlearn.

Computes, per sensitive group (``gender``):
- selection rate (positive prediction rate),
- accuracy,
and the two headline disparity metrics:
- Demographic Parity Difference (dp_diff),
- Equalized Odds Difference (eq_odds_diff).

A model is considered **unfair** (rejected for promotion) when the
demographic parity difference exceeds ``FAIRNESS_DP_THRESHOLD`` (0.1).
Results are saved as JSON + a bar chart in ``reports/``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.config import FAIRNESS_DP_THRESHOLD, REPORTS_DIR

try:
    from fairlearn.metrics import (
        MetricFrame,
        demographic_parity_difference,
        equalized_odds_difference,
        selection_rate,
    )

    FAIRLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover - graceful degradation
    FAIRLEARN_AVAILABLE = False


def _build_test_frame():
    """Return (y_test, y_pred, sensitive_series) aligned on the same split."""
    import joblib

    from src.features.build_features import build_features, feature_sets
    from src.models.train import _preprocess_pipeline

    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=True)

    model = joblib.load("models/churn_model.joblib")

    # The model was trained without the sensitive column; drop it only after
    # the split so we can keep gender for the audit.
    X = frame.drop(columns=["churn"])
    y = frame["churn"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    sensitive = X_test["gender"].reset_index(drop=True)
    X_test_model = X_test.drop(columns=["gender"]).reset_index(drop=True)
    y_pred = model.predict(X_test_model)

    return y_test.reset_index(drop=True), y_pred, sensitive


def fairness_check(model_path: Path = Path("models/churn_model.joblib")) -> dict:
    """Run the full fairness audit and persist a JSON report."""
    if not FAIRLEARN_AVAILABLE:
        raise ImportError("fairlearn is required for fairness_check")

    y_test, y_pred, sensitive = _build_test_frame()

    metric_frame = MetricFrame(
        metrics={
            "accuracy": accuracy_score,
            "selection_rate": selection_rate,
        },
        y_true=y_test,
        y_pred=y_pred,
        sensitive_features=sensitive,
    )

    dp_diff = float(
        demographic_parity_difference(
            y_test, y_pred, sensitive_features=sensitive
        )
    )
    eq_odds_diff = float(
        equalized_odds_difference(
            y_test, y_pred, sensitive_features=sensitive
        )
    )

    group_summary = metric_frame.by_group.to_dict()

    result = {
        "demographic_parity_difference": dp_diff,
        "equalized_odds_difference": eq_odds_diff,
        "threshold": FAIRNESS_DP_THRESHOLD,
        "passed": dp_diff <= FAIRNESS_DP_THRESHOLD,
        "selection_rate_by_group": group_summary["selection_rate"],
        "accuracy_by_group": group_summary["accuracy"],
        "overall_selection_rate": float(selection_rate(y_test, y_pred)),
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "fairness_report.json", "w") as handle:
        json.dump(result, handle, indent=2, default=str)

    _plot_selection_rates(group_summary["selection_rate"])

    return result


def _plot_selection_rates(by_group: dict) -> None:
    groups = list(by_group.keys())
    rates = list(by_group.values())
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([str(g) for g in groups], rates, color=["#4C72B0", "#DD8452"])
    ax.set_ylabel("Selection rate")
    ax.set_title("Selection rate by gender group")
    fig.savefig(REPORTS_DIR / "fairness_selection_rate.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fairness audit with Fairlearn.")
    parser.add_argument("--model", default="models/churn_model.joblib")
    args = parser.parse_args()

    result = fairness_check(Path(args.model))
    verdict = "PASS" if result["passed"] else "FAIL"
    print(
        f"DP difference={result['demographic_parity_difference']:.4f} "
        f"(threshold {result['threshold']}) -> {verdict}"
    )
    print(f"Equalized odds difference={result['equalized_odds_difference']:.4f}")
    print(f"Saved to reports/fairness_report.json")


if __name__ == "__main__":
    main()
