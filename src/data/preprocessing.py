"""Pure preprocessing functions.

Every transformation is a pure function operating on a DataFrame and
returning a new DataFrame, so each step is independently testable and
side-effect free.
"""

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from src.config import (
    BINARY_FEATURES,
    CATEGORICAL_FEATURES,
    ID_COL,
    NUMERIC_FEATURES,
    TARGET_COL,
    TIMESTAMP_COL,
)


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully duplicated rows (keeps first occurrence)."""
    return df.drop_duplicates().reset_index(drop=True)


def drop_missing(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Drop rows with missing values on critical columns."""
    cols = columns or [ID_COL, TARGET_COL, "age", "gender", "tenure_months"]
    return df.dropna(subset=cols).reset_index(drop=True)


def clamp_numeric(
    df: pd.DataFrame,
    ranges: Optional[dict] = None,
    numeric_features: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Clamp numeric features to sane business ranges (age 18-100 etc.)."""
    bounds = ranges or {
        "age": (18, 100),
        "tenure_months": (0, 120),
        "monthly_charges": (0, 1000),
        "total_charges": (0, 100000),
        "num_services": (0, 10),
        "support_tickets": (0, 100),
        "avg_call_minutes": (0, 2000),
    }
    features = numeric_features or NUMERIC_FEATURES
    out = df.copy()
    for col in features:
        if col in out.columns and col in bounds:
            lo, hi = bounds[col]
            out[col] = out[col].clip(lower=lo, upper=hi)
    return out


def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Enforce canonical dtypes across the dataset."""
    out = df.copy()
    for col in NUMERIC_FEATURES:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    for col in BINARY_FEATURES + [TARGET_COL]:
        if col in out.columns:
            out[col] = out[col].astype("int8")
    for col in CATEGORICAL_FEATURES:
        if col in out.columns:
            out[col] = out[col].astype("category")
    if ID_COL in out.columns:
        out[ID_COL] = out[ID_COL].astype("int64")
    if TIMESTAMP_COL in out.columns:
        out[TIMESTAMP_COL] = pd.to_datetime(out[TIMESTAMP_COL])
    return out


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full preprocessing chain (pure, returns a new frame)."""
    return (
        df.pipe(drop_duplicates)
        .pipe(drop_missing)
        .pipe(clamp_numeric)
        .pipe(cast_dtypes)
    )


def run(output_path=None) -> pd.DataFrame:
    """Entry point: load raw data, preprocess, persist to CSV."""
    from src.data.ingestion import ingest_raw_data

    raw, meta = ingest_raw_data()
    clean = preprocess(raw)
    path = output_path or "data/processed/dataset_clean.csv"
    clean.to_csv(path, index=False)
    print(f"Preprocessed {len(clean)} rows -> {path} (raw had {meta['rows']})")
    return clean


if __name__ == "__main__":
    run()
