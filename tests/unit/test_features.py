"""Unit tests for feature engineering functions."""
import pandas as pd
import pytest

from src.config import ID_COL, SENSITIVE_COL, TARGET_COL, TIMESTAMP_COL
from src.features.build_features import (
    derive_features,
    one_hot_encode,
    build_features,
    feature_sets,
    build_feast_features,
)


def _churn_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "timestamp": [
                "2023-01-01 00:00:00",
                "2023-06-01 00:00:00",
                "2024-01-01 00:00:00",
                "2024-06-01 00:00:00",
            ],
            "age": [25, 40, 55, 70],
            "gender": ["female", "male", "female", "male"],
            "region": ["north", "south", "east", "west"],
            "tenure_months": [1, 12, 36, 60],
            "monthly_charges": [50.0, 60.0, 70.0, 80.0],
            "total_charges": [50.0, 720.0, 2520.0, 4800.0],
            "num_services": [1, 2, 3, 4],
            "contract_type": [
                "month-to-month",
                "one_year",
                "two_year",
                "two_year",
            ],
            "payment_method": [
                "electronic_check",
                "mailed_check",
                "bank_transfer",
                "credit_card",
            ],
            "support_tickets": [0, 1, 2, 3],
            "avg_call_minutes": [100.0, 200.0, 300.0, 400.0],
            "has_online_backup": [0, 1, 0, 1],
            "has_device_protection": [1, 0, 1, 0],
            "has_tech_support": [0, 0, 1, 1],
            "churn": [1, 0, 1, 0],
        }
    )


def test_derive_features():
    result = derive_features(_churn_frame())
    for col in (
        "avg_charge_per_month",
        "service_density",
        "ticket_intensity",
        "is_long_tenure",
        "is_high_value_customer",
        "usage_efficiency",
    ):
        assert col in result.columns
    assert result.loc[0, "avg_charge_per_month"] == 50.0  # 50/1
    assert result.loc[1, "is_long_tenure"] == 0
    assert result.loc[2, "is_long_tenure"] == 1


def test_derive_features_passthrough_without_churn_columns():
    """Frames lacking the churn columns are returned untouched."""
    df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
    result = derive_features(df)
    assert list(result.columns) == list(df.columns)


def test_derive_features_survives_zero_tenure():
    df = _churn_frame()
    df.loc[0, "tenure_months"] = 0
    result = derive_features(df)
    assert result["avg_charge_per_month"].notna().all()


def test_one_hot_encode():
    df = pd.DataFrame({"color": ["red", "blue", "red", "green"]})
    result = one_hot_encode(df, ["color"])
    # drop_first=True: first category ("blue") dropped, others encoded
    assert "color_blue" not in result.columns
    assert "color_green" in result.columns
    assert "color_red" in result.columns
    assert len(result) == 4


def test_build_features_drops_id_timestamp_and_sensitive():
    result = build_features(_churn_frame(), include_sensitive=False)
    assert ID_COL not in result.columns
    assert TIMESTAMP_COL not in result.columns
    assert not [c for c in result.columns if c.startswith(SENSITIVE_COL)]
    assert TARGET_COL in result.columns
    assert len(result) == 4


def test_build_features_can_keep_sensitive_for_audit():
    result = build_features(_churn_frame(), include_sensitive=True)
    assert SENSITIVE_COL in result.columns


def test_build_features_one_hot_encodes_categoricals():
    result = build_features(_churn_frame(), include_sensitive=False)
    assert "contract_type" not in result.columns
    assert any(c.startswith("contract_type_") for c in result.columns)


def test_feature_sets():
    frame = build_features(_churn_frame(), include_sensitive=False)
    sets = feature_sets(frame)
    assert TARGET_COL not in sets["X"].columns
    assert list(sets["y"]) == [1, 0, 1, 0]


def test_build_feast_features():
    result = build_feast_features(_churn_frame())
    # Entity key + event timestamp are what make point-in-time joins correct.
    assert ID_COL in result.columns
    assert TIMESTAMP_COL in result.columns
    assert TARGET_COL in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result[TIMESTAMP_COL])
