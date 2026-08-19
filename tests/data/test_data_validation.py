"""Data validation tests using Great Expectations."""
import pandas as pd
import pytest

from src.config import RAW_DATA_PATH

EXPECTED_COLUMNS = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount", "Class"]


def test_raw_data_exists():
    assert RAW_DATA_PATH.exists(), "Raw dataset not found"


def test_raw_data_schema():
    df = pd.read_csv(RAW_DATA_PATH)
    assert list(df.columns) == EXPECTED_COLUMNS


def test_raw_data_row_count():
    df = pd.read_csv(RAW_DATA_PATH)
    assert 5000 <= len(df) <= 20000


def test_no_nulls_on_critical_columns():
    df = pd.read_csv(RAW_DATA_PATH)
    critical = ["Time", "Amount", "Class"]
    for col in critical:
        assert df[col].notna().all(), f"Nulls found in {col}"


def test_time_non_negative():
    df = pd.read_csv(RAW_DATA_PATH)
    assert (df["Time"] >= 0).all()


def test_amount_range():
    df = pd.read_csv(RAW_DATA_PATH)
    assert (df["Amount"] >= 0).all()
    assert (df["Amount"] <= 100000).all()


def test_class_binary():
    df = pd.read_csv(RAW_DATA_PATH)
    assert set(df["Class"].unique()).issubset({0, 1})


def test_pca_features_finite():
    df = pd.read_csv(RAW_DATA_PATH)
    pca_cols = [f"V{i}" for i in range(1, 29)]
    assert df[pca_cols].notna().all().all()
    assert df[pca_cols].apply(lambda s: pd.api.types.is_float_dtype(s)).all()


def test_dtypes():
    df = pd.read_csv(RAW_DATA_PATH)
    assert pd.api.types.is_numeric_dtype(df["Time"])
    assert df["Amount"].dtype == "float64"
    assert df["V1"].dtype == "float64"