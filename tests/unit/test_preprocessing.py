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
    df = pd.DataFrame({"age": [10, 50, 120], "monthly_charges": [-10, 50, 2000]})
    result = clamp_numeric(df)
    assert result["age"].between(18, 100).all()
    assert result["monthly_charges"].between(0, 1000).all()


def test_cast_dtypes():
    df = pd.DataFrame({
        "age": [25, 30],
        "monthly_charges": [50.0, 60.0],
        "churn": [0, 1],
        "gender": ["M", "F"],
    })
    result = cast_dtypes(df)
    assert result["age"].dtype == "int64"
    assert result["monthly_charges"].dtype == "float64"
    assert result["churn"].dtype == "int8"
    assert result["gender"].dtype.name == "category"


def test_preprocess_chain():
    df = pd.DataFrame({
        "customer_id": [1, 2, 2],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-02"],
        "age": [25, 30, 30],
        "gender": ["M", "F", "F"],
        "tenure_months": [12, 24, 24],
        "monthly_charges": [50.0, 60.0, 60.0],
        "total_charges": [600.0, 1440.0, 1440.0],
        "num_services": [2, 3, 3],
        "contract_type": ["one_year", "two_year", "two_year"],
        "payment_method": ["credit_card", "bank_transfer", "bank_transfer"],
        "support_tickets": [1, 0, 0],
        "avg_call_minutes": [100.0, 50.0, 50.0],
        "has_online_backup": [1, 0, 0],
        "has_device_protection": [0, 1, 1],
        "has_tech_support": [1, 0, 0],
        "churn": [0, 1, 1],
    })
    result = preprocess(df)
    assert len(result) == 2  # deduped
    assert result["age"].between(18, 100).all()
    assert result["churn"].dtype == "int8"