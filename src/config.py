"""Shared project configuration: paths, feature columns, model names."""

from __future__ import annotations

from pathlib import Path

# Project root: two levels up from src/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = Path("/tmp/realdata/creditcard.csv")
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "dataset_clean.csv"
FEATURES_PATH = PROJECT_ROOT / "data" / "features" / "features.parquet"
REFERENCE_DATA_PATH = PROJECT_ROOT / "data" / "reference" / "reference.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
MONITORING_REPORTS_DIR = PROJECT_ROOT / "monitoring" / "reports"
MODEL_CARDS_DIR = PROJECT_ROOT / "model_cards"
MLFLOW_DIR = PROJECT_ROOT / "mlflow" / "mlruns"

# Target / sensitive attribute / id
TARGET_COL = "Class"
SENSITIVE_COL = None
ID_COL = None
TIMESTAMP_COL = "Time"

# Features: Time, V1-V28 (PCA), Amount
V_FEATURES = [f"V{i}" for i in range(1, 29)]
NUMERIC_FEATURES = ["Time", "Amount"] + V_FEATURES

# No binary or categorical features for this dataset
BINARY_FEATURES = []
CATEGORICAL_FEATURES = []

# Full feature set fed to the model
BASE_FEATURES = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATURES

# Fairness / drift metrics thresholds
FAIRNESS_DP_THRESHOLD = 0.1
DRIFT_THRESHOLD = 0.3
F1_PROMOTION_THRESHOLD = 0.25
AUC_PROMOTION_THRESHOLD = 0.80
CHALLENGER_RATIO = 0.1
