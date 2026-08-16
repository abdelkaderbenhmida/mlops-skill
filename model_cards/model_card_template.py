"""Automatic Model Card generation.

Builds a Markdown model card from MLflow metrics + Fairlearn fairness results
so the documentation is regenerated at every promotion instead of going stale.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Optional

from src.config import REPORTS_DIR


def _read_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _format_metric(value) -> str:
    try:
        return f"{float(value):.4f}"
    except (TypeError, ValueError):
        return str(value)


def generate_model_card(
    report: Optional[dict] = None,
    output_path: Path = Path("model_cards/model_card.md"),
) -> str:
    """Generate a model card markdown string and write it to ``output_path``."""
    report = report or {}
    metrics = report.get("metrics", {}) or _read_json(REPORTS_DIR / "promotion_report.json").get(
        "metrics", {}
    )
    fairness = report.get("fairness", {}) or _read_json(REPORTS_DIR / "fairness_report.json")
    gates = report.get("gates", {})

    lines = [
        "# Model Card: Customer Churn Classifier",
        "",
        f"*Generated automatically on {datetime.datetime.now().isoformat()}*",
        "",
        "## Model details",
        "",
        "- Algorithm: RandomForestClassifier",
        "- Task: Binary classification (customer churn)",
        "- Objective: Predict churn probability to enable proactive retention",
        "",
        "## Intended use",
        "",
        "- Valid: churn risk scoring for telecom customers",
        "- Avoid: credit decisions, medical predictions, or any other domain",
        "",
        "## Training data",
        "",
        "- Source: synthetic telecom dataset (`data/raw/dataset.csv`)",
        "- Rows: ~7000, binary target with a sensitive attribute (`gender`)",
        "",
        "## Performance metrics (held-out test set)",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    for name, value in metrics.items():
        lines.append(f"| {name} | {_format_metric(value)} |")

    lines += [
        "",
        "## Fairness analysis (Fairlearn)",
        "",
        f"- Demographic parity difference: {_format_metric(fairness.get('demographic_parity_difference'))}",
        f"- Equalized odds difference: {_format_metric(fairness.get('equalized_odds_difference'))}",
        f"- Threshold (dp_diff): {_format_metric(fairness.get('threshold', 0.1))}",
    ]
    if "selection_rate_by_group" in fairness:
        lines.append("")
        lines.append("| Group | Selection rate |")
        lines.append("| --- | --- |")
        for group, rate in fairness.get("selection_rate_by_group", {}).items():
            lines.append(f"| {group} | {_format_metric(rate)} |")

    lines += [
        "",
        "## Promotion gates",
        "",
        "| Gate | Status |",
        "| --- | --- |",
    ]
    for name, passed in gates.items():
        lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} |")

    lines += [
        "",
        "## Known limitations & identified biases",
        "",
        "- Trained on synthetic data; real-world performance may differ.",
        "- Fairness is measured on `gender` only; other sensitive dimensions"
        " (e.g. age bands) are not audited in this version.",
        "- Small residual demographic parity difference exists and is monitored.",
    ]

    card = "\n".join(lines) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(card)
    return card


def main() -> None:
    card = generate_model_card()
    print(card)


if __name__ == "__main__":
    main()
