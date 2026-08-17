"""Shared project configuration: paths, feature columns, model names."""

from __future__ import annotations

from pathlib import Path

# Project root: two levels up from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "dataset.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "dataset_clean.csv"
FEATURES_PATH = PROJECT_ROOT / "data" / "features" / "features.parquet"
REFERENCE_DATA_PATH = PROJECT_ROOT / "data" / "reference" / "reference.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
MONITORING_REPORTS_DIR = PROJECT_ROOT / "monitoring" / "reports"
MODEL_CARDS_DIR = PROJECT_ROOT / "model_cards"
MLFLOW_DIR = PROJECT_ROOT / "mlflow" / "mlruns"

# Target / sensitive attribute / id
TARGET_COL = "churn"
SENSITIVE_COL = "gender"
ID_COL = "customer_id"
TIMESTAMP_COL = "timestamp"

# Numerical features kept as-is
NUMERIC_FEATURES = [
    "age",
    "tenure_months",
    "monthly_charges",
    "total_charges",
    "num_services",
    "support_tickets",
    "avg_call_minutes",
]

# Binary features kept as-is (already 0/1)
BINARY_FEATURES = [
    "has_online_backup",
    "has_device_protection",
    "has_tech_support",
]

# Categorical features to one-hot encode
CATEGORICAL_FEATURES = [
    "gender",
    "region",
    "contract_type",
    "payment_method",
]

# Full feature set fed to the model (after one-hot encoding)
BASE_FEATURES = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES

# Fairness / drift metrics thresholds
FAIRNESS_DP_THRESHOLD = 0.1
DRIFT_THRESHOLD = 0.3
F1_PROMOTION_THRESHOLD = 0.2
CHALLENGER_RATIO = 0.1
