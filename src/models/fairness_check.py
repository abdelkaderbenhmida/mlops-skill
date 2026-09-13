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

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

    from src.config import RAW_DATA_PATH, SENSITIVE_COL, TARGET_COL
    from src.data.preprocessing import preprocess
    from src.features.build_features import build_features

    raw = pd.read_csv(RAW_DATA_PATH)
    clean = preprocess(raw)

    # gender is one-hot encoded (and dropped) inside build_features; keep the
    # raw series aligned positionally with the feature frame for the audit.
    gender_all = clean[SENSITIVE_COL].reset_index(drop=True)
    frame = build_features(clean, include_sensitive=False)

    model = joblib.load("models/churn_model.joblib")

    X = frame.drop(columns=[TARGET_COL])
    y = frame[TARGET_COL]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    sensitive = gender_all.iloc[X_test.index].reset_index(drop=True)
    X_test_model = X_test.reset_index(drop=True)
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

# TODO: high - Add test to ensure protected attributes are excluded from feature schema
# TODO: medium - Implement tiered severity gate with documented sign-off for Amber results
