"""Data validation tests: the raw dataset must satisfy the input contract.

Mirrors great_expectations/expectations/dataset_suite.json so a contract
breach fails in CI as well as in the DVC `validate` stage.
"""
import pandas as pd
import pytest

from src.config import (
    BINARY_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_RANGES,
    RAW_DATA_PATH,
    SENSITIVE_COL,
    TARGET_COL,
)

EXPECTED_COLUMNS = [
    "customer_id",
    "timestamp",
    "age",
    "gender",
    "region",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "num_services",
    "contract_type",
    "payment_method",
    "support_tickets",
    "avg_call_minutes",
    "has_online_backup",
    "has_device_protection",
    "has_tech_support",
    "churn",
]


@pytest.fixture(scope="module")
def raw() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_PATH)


def test_raw_data_exists():
    assert RAW_DATA_PATH.exists(), f"Raw dataset not found at {RAW_DATA_PATH}"


def test_raw_data_schema(raw):
    assert list(raw.columns) == EXPECTED_COLUMNS


def test_raw_data_row_count(raw):
    assert 5000 <= len(raw) <= 10000


def test_no_nulls_on_critical_columns(raw):
    critical = ["customer_id", "timestamp", TARGET_COL, SENSITIVE_COL]
    for col in critical:
        assert raw[col].notna().all(), f"Nulls found in {col}"


def test_customer_id_unique(raw):
    assert raw["customer_id"].is_unique


def test_timestamp_parses(raw):
    parsed = pd.to_datetime(raw["timestamp"], errors="coerce")
    assert parsed.notna().all()


def test_numeric_ranges(raw):
    for col, (lo, hi) in NUMERIC_RANGES.items():
        assert raw[col].between(lo, hi).all(), f"{col} outside [{lo}, {hi}]"


def test_target_binary(raw):
    assert set(raw[TARGET_COL].unique()) <= {0, 1}


def test_target_not_degenerate(raw):
    rate = raw[TARGET_COL].mean()
    assert 0.01 < rate < 0.5, f"Implausible churn rate: {rate}"


def test_binary_features_are_binary(raw):
    for col in BINARY_FEATURES:
        assert set(raw[col].unique()) <= {0, 1}, f"{col} is not 0/1"


def test_categorical_levels_are_closed(raw):
    allowed = {
        "region": {"north", "south", "east", "west"},
        "contract_type": {"month-to-month", "one_year", "two_year"},
        "payment_method": {
            "electronic_check",
            "mailed_check",
            "bank_transfer",
            "credit_card",
        },
    }
    for col in CATEGORICAL_FEATURES:
        assert set(raw[col].unique()) <= allowed[col], f"Unexpected level in {col}"


def test_numeric_features_finite(raw):
    numeric = raw.select_dtypes("number")
    assert numeric.notna().all().all()
