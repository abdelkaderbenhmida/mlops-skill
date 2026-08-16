"""Drift-driven retraining trigger.

Checks the latest drift score and, when it exceeds ``DRIFT_THRESHOLD``,
triggers the ZenML retraining pipeline. As a safety guard the trigger never
skips the fairness check: the retraining pipeline itself re-runs the full
gate suite before any promotion.
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
from pathlib import Path

from src.config import DRIFT_THRESHOLD, MONITORING_REPORTS_DIR

logger = logging.getLogger(__name__)

DRIFT_SCORE_FILE = MONITORING_REPORTS_DIR / "drift_score.json"


def read_drift_score(path: Path = DRIFT_SCORE_FILE) -> float:
    """Read the latest drift score produced by ``drift_report.py``."""
    if not path.exists():
        return 0.0
    data = json.loads(path.read_text())
    return float(data["drift_score"])


def should_retrain(score: float, threshold: float = DRIFT_THRESHOLD) -> bool:
    """Return True when the drift score exceeds the threshold."""
    return score > threshold


def trigger_retraining(dry_run: bool = False) -> dict:
    """Evaluate drift and launch the retraining pipeline when needed."""
    score = read_drift_score()
    trigger = should_retrain(score)
    logger.info("Drift score=%.3f threshold=%.3f trigger=%s", score, DRIFT_THRESHOLD, trigger)

    if trigger and not dry_run:
        _launch_retraining_pipeline()
    return {
        "drift_score": score,
        "threshold": DRIFT_THRESHOLD,
        "triggered": trigger,
        "dry_run": dry_run,
    }


def _launch_retraining_pipeline() -> None:
    """Shell out to the ZenML retraining pipeline.

    The retraining pipeline re-runs data validation, tuning, Deepchecks and
    Fairlearn before any model is promoted (all promotion guards remain
    active on automated retraining).
    """
    cmd = ["python", "-m", "pipelines.retraining_pipeline"]
    logger.info("Launching retraining pipeline: %s", " ".join(cmd))
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Notification / supervision trace: structured log for human oversight.
    logger.warning(
        "AUTOMATED_RETRAINING_TRIGGERED score=%.3f", read_drift_score()
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Drift-based retraining trigger.")
    parser.add_argument("--dry-run", action="store_true", help="Only report, don't launch.")
    args = parser.parse_args()

    result = trigger_retraining(dry_run=args.dry_run)
    print(result)


if __name__ == "__main__":
    main()
