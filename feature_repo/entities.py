"""Feast entity definitions.

A single entity: ``customer`` keyed by ``customer_id`` (Int64), used by both
offline (training) and online (inference) feature retrieval.
"""

from feast import Entity, ValueType

customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    value_type=ValueType.INT64,
    description="Customer identity key for the churn prediction feature store.",
)
