"""Feast data sources.

The offline source is the engineered Parquet frame produced by
``src/features/build_features.build_feast_features``. The ``timestamp``
column is used for point-in-time correctness: historical (training) queries
return the feature values valid *at* the event timestamp, and online
retrieval returns the latest values, so offline and online features match.
"""

from __future__ import annotations

from feast import FileSource

CUSTOMER_FEATURES_PATH = "data/features/feast_features.parquet"

customer_features_source = FileSource(
    name="customer_features_source",
    path=CUSTOMER_FEATURES_PATH,
    timestamp_field="timestamp",
    created_timestamp_column=None,
    file_format="parquet",
)
