"""Production model monitoring with Evidently.

Builds a drift report (``DataDriftPreset`` + ``TargetDriftPreset``) comparing
a production sample against the training reference dataset, saves the HTML to
``monitoring/reports/drift_report.html`` and extracts the dataset drift score.

A simulated drift mode injects distribution shifts so the report is demonstrable
without needing real production traffic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import MONITORING_REPORTS_DIR, REFERENCE_DATA_PATH

try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

    EVIDENTLY_AVAILABLE = True
except ImportError:  # pragma: no cover
    EVIDENTLY_AVAILABLE = False


def build_reference() -> pd.DataFrame:
    """Persist and return the training reference (for drift comparison)."""
    from src.features.build_features import build_features
    from src.config import RAW_DATA_PATH
    from src.data.preprocessing import preprocess

    raw = pd.read_csv(RAW_DATA_PATH)
    clean = preprocess(raw)
    frame = build_features(clean, include_sensitive=True)

    REFERENCE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(REFERENCE_DATA_PATH, index=False)
    return frame


def simulate_production_sample(n: int = 1000, drift_strength: float = 0.0) -> pd.DataFrame:
    """Sample rows and optionally shift distributions to simulate drift."""
    if not REFERENCE_DATA_PATH.exists():
        build_reference()
    ref = pd.read_csv(REFERENCE_DATA_PATH)

    current = ref.sample(n=min(n, len(ref)), random_state=7)
    if drift_strength > 0:
        rng = np.random.default_rng(7)
        numeric_cols = current.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            std = current[col].std() or 1.0
            current[col] = current[col] + rng.normal(
                0, drift_strength * std, size=len(current)
            )
    return current


def generate_drift_report(
    current_data: pd.DataFrame | None = None,
    reference_data: pd.DataFrame | None = None,
    output_path: Path = MONITORING_REPORTS_DIR / "drift_report.html",
) -> dict:
    """Run the Evidently report and extract the dataset drift score."""
    if not EVIDENTLY_AVAILABLE:
        raise ImportError("evidently is required for drift monitoring")

    reference = reference_data if reference_data is not None else build_reference()
    current = (
        current_data if current_data is not None
        else simulate_production_sample()
    )

    report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
    report.run(reference_data=reference, current_data=current)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report.save_html(str(output_path))

    as_dict = report.as_dict()
    dataset_drift = as_dict["metrics"][0]["result"]["dataset_drift"]
    drift_score = as_dict["metrics"][0]["result"]["share_of_drifted_columns"]

    result = {
        "dataset_drift": bool(dataset_drift),
        "drift_score": float(drift_score),
        "report_path": str(output_path),
    }
    (MONITORING_REPORTS_DIR / "drift_score.json").write_text(
        json.dumps(result, indent=2)
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Evidently drift report.")
    parser.add_argument("--drift-strength", type=float, default=0.0,
                        help=">0 simulates a drifted production sample.")
    args = parser.parse_args()

    current = simulate_production_sample(drift_strength=args.drift_strength)
    result = generate_drift_report(current_data=current)
    print(
        f"dataset_drift={result['dataset_drift']} "
        f"drift_score={result['drift_score']:.3f}"
    )
    print(f"Report saved to {result['report_path']}")


if __name__ == "__main__":
    main()
