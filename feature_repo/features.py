"""Feast feature definitions.

A single ``FeatureView`` groups the customer features with a TTL and an
explicit schema (``Float32`` / ``Int64`` fields). The Parquet-backed source
with a ``timestamp`` field gives point-in-time correctness: offline
(training) retrieval joins each entity to the feature values valid *at* the
event timestamp, and online retrieval returns the latest values, so there is
no training-serving skew.
"""

from __future__ import annotations

from datetime import timedelta

from feast import Field, FeatureView
from feast.types import Float32, Int64

try:
    from feature_repo.data_sources import customer_features_source
    from feature_repo.entities import customer
except ImportError:  # running from inside feature_repo/ (e.g. `feast apply`)
    from data_sources import customer_features_source
    from entities import customer

customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=30),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="tenure_months", dtype=Int64),
        Field(name="monthly_charges", dtype=Float32),
        Field(name="total_charges", dtype=Float32),
        Field(name="num_services", dtype=Int64),
        Field(name="support_tickets", dtype=Int64),
        Field(name="avg_call_minutes", dtype=Float32),
        Field(name="has_online_backup", dtype=Int64),
        Field(name="has_device_protection", dtype=Int64),
        Field(name="has_tech_support", dtype=Int64),
        Field(name="avg_charge_per_month", dtype=Float32),
        Field(name="service_density", dtype=Float32),
        Field(name="ticket_intensity", dtype=Float32),
        Field(name="is_long_tenure", dtype=Int64),
        Field(name="is_high_value_customer", dtype=Int64),
        Field(name="usage_efficiency", dtype=Float32),
    ],
    source=customer_features_source,
)
