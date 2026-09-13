"""Run the Great Expectations input-data contract against the raw dataset.

The project's datasource is a ``RuntimeDataConnector``, which receives its
batch as an in-memory dataframe. The ``great_expectations checkpoint run``
CLI cannot supply one, so the checkpoint is driven programmatically here and
this module — not the CLI — is what the DVC ``validate`` stage invokes.

Exits non-zero when the contract is breached, so the pipeline stops before a
bad dataset reaches preprocessing.
"""

from __future__ import annotations

import sys

import pandas as pd

from src.config import RAW_DATA_PATH

CHECKPOINT_NAME = "dataset_checkpoint"
SUITE_NAME = "dataset_suite"
DATA_ASSET_NAME = "churn_dataset"


def validate(path=RAW_DATA_PATH) -> dict:
    """Validate ``path`` against the expectation suite.

    Returns the summary dict; raises RuntimeError when expectations fail.
    """
    import great_expectations as gx
    from great_expectations.core.batch import RuntimeBatchRequest

    context = gx.get_context(context_root_dir="great_expectations")
    df = pd.read_csv(path)

    batch_request = RuntimeBatchRequest(
        datasource_name="pandas_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name=DATA_ASSET_NAME,
        runtime_parameters={"batch_data": df},
        batch_identifiers={"default_identifier_name": "raw_dataset"},
    )

    result = context.run_checkpoint(
        checkpoint_name=CHECKPOINT_NAME,
        validations=[
            {"batch_request": batch_request, "expectation_suite_name": SUITE_NAME}
        ],
    )

    stats = {}
    for validation_result in result.run_results.values():
        stats = validation_result["validation_result"]["statistics"]

    summary = {
        "source_file": str(path),
        "rows": len(df),
        "success": bool(result.success),
        "evaluated_expectations": stats.get("evaluated_expectations"),
        "successful_expectations": stats.get("successful_expectations"),
        "unsuccessful_expectations": stats.get("unsuccessful_expectations"),
    }

    if not result.success:
        failed = [
            r["expectation_config"]["expectation_type"]
            for validation_result in result.run_results.values()
            for r in validation_result["validation_result"]["results"]
            if not r["success"]
        ]
        raise RuntimeError(
            f"Data contract breached on {path}: {len(failed)} failed expectation(s): {failed}"
        )

    return summary


def main() -> None:
    try:
        summary = validate()
    except RuntimeError as exc:
        print(f"validation FAILED: {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"validation PASSED: {summary['successful_expectations']}"
        f"/{summary['evaluated_expectations']} expectations green "
        f"on {summary['rows']} rows from {summary['source_file']}"
    )


if __name__ == "__main__":
    main()
