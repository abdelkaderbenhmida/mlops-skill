"""Unit tests for feature engineering functions."""
import pandas as pd
import pytest

from src.features.build_features import (
    derive_features,
    one_hot_encode,
    build_features,
    feature_sets,
    build_feast_features,
)


def test_derive_features():
    df = pd.DataFrame({
        "tenure_months": [1, 12, 36, 60],
        "monthly_charges": [50.0, 60.0, 70.0, 80.0],
        "num_services": [1, 2, 3, 4],
        "support_tickets": [0, 1, 2, 3],
        "total_charges": [50.0, 720.0, 2520.0, 4800.0],
        "avg_call_minutes": [100.0, 200.0, 300.0, 400.0],
    })
    result = derive_features(df)
    assert "avg_charge_per_month" in result.columns
    assert "service_density" in result.columns
    assert "ticket_intensity" in result.columns
    assert "is_long_tenure" in result.columns
    assert "is_high_value_customer" in result.columns
    assert "usage_efficiency" in result.columns
    # Check values
    assert result.loc[0, "avg_charge_per_month"] == 50.0  # 50/1
    assert result.loc[1, "is_long_tenure"] == 0
    assert result.loc[2, "is_long_tenure"] == 1


def test_one_hot_encode():
    df = pd.DataFrame({"color": ["red", "blue", "red", "green"]})
    result = one_hot_encode(df, ["color"])
    assert "color_blue" in result.columns
    assert "color_green" in result.columns
    assert "color_red" not in result.columns  # dropped first
    assert len(result) == 4


def test_build_features():
    df = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "timestamp": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "age": [25, 30, 35],
        "gender": ["M", "F", "M"],
        "region": ["north", "south", "east"],
        "tenure_months": [12, 24, 36],
        "monthly_charges": [50.0, 60.0, 70.0],
        "total_charges": [600.0, 1440.0, 2520.0],
        "num_services": [2, 3, 4],
        "contract_type": ["one_year", "two_year", "month-to-month"],
        "payment_method": ["credit_card", "bank_transfer", "electronic_check"],
        "support_tickets": [1, 0, 2],
        "avg_call_minutes": [100.0, 50.0, 200.0],
        "has_online_backup": [1, 0, 1],
        "has_device_protection": [0, 1, 0],
        "has_tech_support": [1, 0, 1],
        "churn": [0, 1, 0],
    })
    result = build_features(df, include_sensitive=False)
    assert "churn" in result.columns
    assert "gender" not in result.columns
    assert "customer_id" not in result.columns
    assert "timestamp" not in result.columns


def test_feature_sets():
    df = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [4, 5, 6],
        "churn": [0, 1, 0],
    })
    sets = feature_sets(df)
    assert "X" in sets
    assert "y" in sets
    assert list(sets["X"].columns) == ["feature1", "feature2"]
    assert list(sets["y"]) == [0, 1, 0]


def test_build_feast_features():
    df = pd.DataFrame({
        "customer_id": [1, 2, 3],
        "timestamp": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "age": [25, 30, 35],
        "gender": ["M", "F", "M"],
        "region": ["north", "south", "east"],
        "tenure_months": [12, 24, 36],
        "monthly_charges": [50.0, 60.0, 70.0],
        "total_charges": [600.0, 1440.0, 2520.0],
        "num_services": [2, 3, 4],
        "contract_type": ["one_year", "two_year", "month-to-month"],
        "payment_method": ["credit_card", "bank_transfer", "electronic_check"],
        "support_tickets": [1, 0, 2],
        "avg_call_minutes": [100.0, 50.0, 200.0],
        "has_online_backup": [1, 0, 1],
        "has_device_protection": [0, 1, 0],
        "has_tech_support": [1, 0, 1],
        "churn": [0, 1, 0],
    })
    result = build_feast_features(df)
    assert "customer_id" in result.columns
    assert "timestamp" in result.columns
    assert "churn" in result.columns
    assert result["timestamp"].dtype == "datetime64[ns]"