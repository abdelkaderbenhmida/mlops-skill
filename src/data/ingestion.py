"""Data ingestion: load raw data and log key facts.

Logs the row count, the covered time period, and a SHA256 hash of the raw
source file so every downstream artifact can be traced back to its input.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Tuple

import pandas as pd

from src.config import RAW_DATA_PATH

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
    the covered time period, and the source file hash.
    """
    data_hash = file_hash(path)
    df = pd.read_csv(path)

    time_col = "timestamp" if "timestamp" in df.columns else None
    if time_col is not None:
        df[time_col] = pd.to_datetime(df[time_col])

    period = (
        f"{df[time_col].min()} -> {df[time_col].max()}"
        if time_col is not None
        else "n/a"
    )

    metadata = {
        "rows": len(df),
        "columns": len(df.columns),
        "time_period": period,
        "source_file": str(path),
        "source_hash": data_hash,
    }

    logger.info("Ingested %d rows from %s", len(df), path)
    logger.info("Covered time period: %s", period)
    logger.info("Source file hash: %s", data_hash)

    return df, metadata


if __name__ == "__main__":
    ingest_raw_data()
