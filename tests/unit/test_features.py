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


def _fraud_frame():
    return pd.DataFrame({
        "Time": [0.0, 10.0, 20.0],
        "Amount": [50.0, 250.0, 3000.0],
        "V1": [1.1, -2.2, 0.5],
        "V2": [0.5, -0.3, 1.2],
        "Class": [0, 1, 0],
    })


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


def test_derive_features_passthrough_on_fraud_data():
    df = _fraud_frame()
    result = derive_features(df)
    assert list(result.columns) == list(df.columns)


def test_one_hot_encode():
    df = pd.DataFrame({"color": ["red", "blue", "red", "green"]})
    result = one_hot_encode(df, ["color"])
    # drop_first=True: first category ("blue") dropped, others encoded
    assert "color_blue" not in result.columns
    assert "color_green" in result.columns
    assert "color_red" in result.columns
    assert len(result) == 4


def test_build_features():
    df = _fraud_frame()
    result = build_features(df, include_sensitive=False)
    assert "Class" in result.columns
    assert "Time" in result.columns
    assert "Amount" in result.columns
    assert "V1" in result.columns
    assert len(result) == 3


def test_feature_sets():
    df = pd.DataFrame({
        "V1": [1, 2, 3],
        "V2": [4, 5, 6],
        "Class": [0, 1, 0],
    })
    sets = feature_sets(df)
    assert "X" in sets
    assert "y" in sets
    assert list(sets["X"].columns) == ["V1", "V2"]
    assert list(sets["y"]) == [0, 1, 0]


def test_build_feast_features():
    df = _fraud_frame()
    result = build_feast_features(df)
    assert "Time" in result.columns
    assert "Amount" in result.columns
    assert "V1" in result.columns
    assert "Class" in result.columns
    assert result["Time"].dtype == "float64"