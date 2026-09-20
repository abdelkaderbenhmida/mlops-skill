"""Feature engineering: turn the cleaned dataframe into model-ready features.

Design goals:
- Point-in-time friendly: no global statistics that leak future info; the
  only features derived here are row-local (safe for both training and
  real-time inference).
- Pure functions, deterministic, testable independently.
"""

from __future__ import annotations

from typing import Dict, List

import pandas as pd

from src.config import (
    BINARY_FEATURES,
    CATEGORICAL_FEATURES,
    ID_COL,
    NUMERIC_FEATURES,
    TARGET_COL,
    TIMESTAMP_COL,
)

# Explicit ordering guarantee -> stable column order for the model.
DERIVED_FEATURES: List[str] = [
    "avg_charge_per_month",       # monthly charges normalised by tenure
    "service_density",            # services per month of tenure
    "ticket_intensity",           # support tickets per service
    "is_long_tenure",             # tenure >= 36 months
    "is_high_value_customer",     # total charges above median-like band
    "usage_efficiency",           # call minutes per service
]


def derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived (engineered) features, row-local only.

    Derived features are churn-domain specific; datasets without the churn
    columns (e.g. credit card fraud with PCA features) pass through unchanged.
    """
    out = df.copy()
    if "tenure_months" not in out.columns:
        return out

    tenure = out["tenure_months"].replace(0, 1)
    services = out["num_services"].clip(lower=1)

    out["avg_charge_per_month"] = out["monthly_charges"] / tenure
    out["service_density"] = out["num_services"] / tenure
    out["ticket_intensity"] = out["support_tickets"] / services
    out["is_long_tenure"] = (out["tenure_months"] >= 36).astype("int8")
    out["is_high_value_customer"] = (out["total_charges"] >= 1500).astype("int8")
    out["usage_efficiency"] = out["avg_call_minutes"] / services

    return out


def one_hot_encode(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """One-hot encode categorical columns (drops first level).

    Indicators are emitted as ``int8`` rather than pandas' default ``bool``:
    downstream consumers (Evidently drift reports, ONNX export) cannot
    interpret a boolean extension dtype as a numeric type.
    """
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out = pd.get_dummies(
                out, columns=[col], prefix=col, drop_first=True, dtype="int8"
            )
    return out


def build_features(
    df: pd.DataFrame,
    include_sensitive: bool = False,
    drop_columns: List[str] | None = None,
) -> pd.DataFrame:
    """Transform a cleaned dataframe into the full feature matrix.

    Args:
        df: cleaned dataframe.
        include_sensitive: keep the sensitive attribute (gender) in the
            feature matrix. By default it is excluded from the model but kept
            available for fairness audits in a separate frame.
        drop_columns: extra columns to drop (e.g. id / timestamp).

    Returns:
        Feature matrix (already one-hot encoded, with churn preserved).
    """
    drop = list(drop_columns or [])
    drop += [ID_COL, TIMESTAMP_COL]
    if not include_sensitive:
        drop += ["gender"]
    drop = [c for c in drop if c in df.columns]
    # Keep a numeric time column (e.g. fraud "Time" feature); only drop
    # datetime-typed timestamps that are useless to the model.
    if TIMESTAMP_COL in drop and pd.api.types.is_numeric_dtype(df[TIMESTAMP_COL]):
        drop.remove(TIMESTAMP_COL)

    out = derive_features(df).drop(columns=drop)

    cat_cols = [c for c in CATEGORICAL_FEATURES if c in out.columns]
    out = one_hot_encode(out, cat_cols)

    return out.reset_index(drop=True)


def feature_sets(frame: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Split a built feature frame into (X, y) plus metadata columns."""
    if TARGET_COL in frame.columns:
        y = frame[TARGET_COL]
        X = frame.drop(columns=[TARGET_COL])
    else:
        y = None
        X = frame
    return {"X": X, "y": y}


def run() -> pd.DataFrame:
    """Entry point: load clean data, build features, persist to parquet."""
    clean = pd.read_csv("data/processed/dataset_clean.csv")
    features = build_features(clean, include_sensitive=True)
    features.to_parquet("data/features/features.parquet", index=False)
    print(
        f"Built {features.shape[0]} rows x {features.shape[1]} columns "
        f"-> data/features/features.parquet"
    )

    # Feast-ready variant keeps the entity key + timestamp for point-in-time joins.
    feast = build_feast_features(clean)
    feast.to_parquet("data/features/feast_features.parquet", index=False)
    print(
        f"Feast-ready frame {feast.shape[0]} rows x {feast.shape[1]} columns "
        f"-> data/features/feast_features.parquet"
    )
    return features


def build_feast_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build a feature frame that keeps ``customer_id`` and ``timestamp``.

    This frame is what the Feast ``FileSource`` reads; the timestamp enables
    point-in-time correct joins so offline (training) and online (inference)
    feature values match.
    """
    out = derive_features(df)
    # Engineered features must be included: the Feast FeatureView schema
    # (feature_repo/features.py) declares them alongside the base features.
    engineered = [
        "avg_charge_per_month",
        "service_density",
        "ticket_intensity",
        "is_long_tenure",
        "is_high_value_customer",
        "usage_efficiency",
    ]
    keep = [ID_COL, TIMESTAMP_COL] + NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES + engineered + [TARGET_COL]
    keep = [c for c in dict.fromkeys(keep) if c in out.columns]
    out = out[keep]
    if TIMESTAMP_COL in out.columns and not pd.api.types.is_numeric_dtype(out[TIMESTAMP_COL]):
        out[TIMESTAMP_COL] = pd.to_datetime(out[TIMESTAMP_COL])
    return out.reset_index(drop=True)


if __name__ == "__main__":
    run()
