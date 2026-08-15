"""Data validation tests using Great Expectations."""
import pandas as pd
import pytest

from src.config import RAW_DATA_PATH


def test_raw_data_exists():
    assert RAW_DATA_PATH.exists(), "Raw dataset not found"


def test_raw_data_schema():
    df = pd.read_csv(RAW_DATA_PATH)
    expected_columns = [
        "customer_id", "timestamp", "age", "gender", "region",
        "tenure_months", "monthly_charges", "total_charges",
        "num_services", "contract_type", "payment_method",
        "support_tickets", "avg_call_minutes",
        "has_online_backup", "has_device_protection",
        "has_tech_support", "churn"
    ]
    assert list(df.columns) == expected_columns


def test_raw_data_row_count():
    df = pd.read_csv(RAW_DATA_PATH)
    assert 5000 <= len(df) <= 10000


def test_no_nulls_on_critical_columns():
    df = pd.read_csv(RAW_DATA_PATH)
    critical = ["customer_id", "age", "gender", "churn", "tenure_months"]
    for col in critical:
        assert df[col].notna().all(), f"Nulls found in {col}"


def test_age_range():
    df = pd.read_csv(RAW_DATA_PATH)
    assert df["age"].between(18, 100).all()


def test_tenure_range():
    df = pd.read_csv(RAW_DATA_PATH)
    assert df["tenure_months"].between(0, 120).all()


def test_monthly_charges_positive():
    df = pd.read_csv(RAW_DATA_PATH)
    assert (df["monthly_charges"] >= 0).all()


def test_gender_values():
    df = pd.read_csv(RAW_DATA_PATH)
    assert set(df["gender"].unique()).issubset({"M", "F"})


def test_contract_type_values():
    df = pd.read_csv(RAW_DATA_PATH)
    expected = {"month-to-month", "one_year", "two_year"}
    assert set(df["contract_type"].unique()).issubset(expected)


def test_churn_binary():
    df = pd.read_csv(RAW_DATA_PATH)
    assert set(df["churn"].unique()).issubset({0, 1})


def test_dtypes():
    df = pd.read_csv(RAW_DATA_PATH)
    assert df["customer_id"].dtype == "int64"
    assert df["age"].dtype == "int64"
    assert df["monthly_charges"].dtype == "float64"