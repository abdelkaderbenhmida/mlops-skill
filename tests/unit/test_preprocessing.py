"""Unit tests for preprocessing functions."""
import pandas as pd
import pytest

from src.data.preprocessing import (
    drop_duplicates,
    drop_missing,
    clamp_numeric,
    cast_dtypes,
    preprocess,
)


def _churn_frame() -> pd.DataFrame:
    """A minimal frame carrying the columns preprocessing cares about."""
    return pd.DataFrame(
        {
            "age": [34, 51, 51],
            "tenure_months": [5, 48, 48],
            "monthly_charges": [55.0, 89.5, 89.5],
            "total_charges": [275.0, 4296.0, 4296.0],
            "num_services": [2, 4, 4],
            "support_tickets": [1, 0, 0],
            "avg_call_minutes": [220.0, 410.0, 410.0],
            "has_online_backup": [0, 1, 1],
            "has_device_protection": [1, 1, 1],
            "has_tech_support": [0, 1, 1],
            "region": ["north", "west", "west"],
            "contract_type": ["month-to-month", "two_year", "two_year"],
            "payment_method": ["electronic_check", "credit_card", "credit_card"],
            "churn": [1, 0, 0],
        }
    )


def test_drop_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    result = drop_duplicates(df)
    assert len(result) == 2


def test_drop_missing():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})
    result = drop_missing(df, columns=["a"])
    assert len(result) == 2
    assert result["a"].notna().all()


def test_clamp_numeric():
    df = pd.DataFrame(
        {
            "age": [5.0, 40.0, 250.0],
            "tenure_months": [-3.0, 12.0, 999.0],
            "monthly_charges": [-10.0, 60.0, 5000.0],
        }
    )
    result = clamp_numeric(df)
    assert result["age"].between(18, 100).all()
    assert result["tenure_months"].between(0, 120).all()
    assert result["monthly_charges"].between(0, 500).all()


def test_clamp_numeric_accepts_custom_ranges():
    df = pd.DataFrame({"age": [10.0, 90.0]})
    result = clamp_numeric(df, ranges={"age": (30, 60)}, numeric_features=["age"])
    assert result["age"].tolist() == [30.0, 60.0]


def test_cast_dtypes():
    result = cast_dtypes(_churn_frame())
    assert result["monthly_charges"].dtype == "float64"
    assert result["tenure_months"].dtype == "int64"
    assert result["has_tech_support"].dtype == "int8"
    assert result["contract_type"].dtype == "string"
    assert result["churn"].dtype == "int8"


def test_preprocess_chain():
    df = _churn_frame()
    df.loc[0, "monthly_charges"] = -20.0  # out of range, must be clamped
    result = preprocess(df)
    assert len(result) == 2  # deduped
    assert (result["monthly_charges"] >= 0).all()
    assert result["churn"].dtype == "int8"


def test_preprocess_is_pure():
    df = _churn_frame()
    before = df.copy()
    preprocess(df)
    pd.testing.assert_frame_equal(df, before)
