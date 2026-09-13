"""Data ingestion: load the raw dataset and log key facts.

Logs the row count, class distribution, and a SHA256 hash of the raw
source file so every downstream artifact can be traced back to its input.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Tuple

import pandas as pd

from src.config import RAW_DATA_PATH, TARGET_COL, TIMESTAMP_COL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def file_hash(path) -> str:
    """Return the SHA256 hex digest of a file, streaming-friendly."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ingest_raw_data(path=RAW_DATA_PATH) -> Tuple[pd.DataFrame, dict]:
    """Load the raw CSV and log ingestion metadata.

    Returns ``(dataframe, metadata)`` where metadata contains the row count,
    class distribution, and the source file hash.
    """
    data_hash = file_hash(path)
    df = pd.read_csv(path)

    time_col = TIMESTAMP_COL if TIMESTAMP_COL in df.columns else None
    target_col = TARGET_COL if TARGET_COL in df.columns else None

    class_dist = df[target_col].value_counts().to_dict() if target_col else {}

    period = (
        f"{df[time_col].min()} -> {df[time_col].max()}"
        if time_col is not None
        else "n/a"
    )

    positive_rate = class_dist.get(1, 0) / len(df) if len(df) > 0 else 0

    metadata = {
        "rows": len(df),
        "columns": len(df.columns),
        "time_period": period,
        "source_file": str(path),
        "source_hash": data_hash,
        "class_distribution": class_dist,
        "positive_rate": positive_rate,
    }

    logger.info("Ingested %d rows from %s", len(df), path)
    logger.info("Class distribution: %s", class_dist)
    logger.info("Positive (%s=1) rate: %.4f%%", TARGET_COL, positive_rate * 100)
    logger.info("Covered time period: %s", period)
    logger.info("Source file hash: %s", data_hash)

    return df, metadata


if __name__ == "__main__":
    ingest_raw_data()
