"""ZenML training pipeline with step caching and MLflow ExperimentTracker integration.

Steps:
- ingest: load raw data + log metadata (row count, time period, source hash)
- validate: Great Expectations checkpoint
- preprocess: pure preprocessing functions
- build_features: feature engineering (one-hot, derived features)
- train: MLflow-tracked training (params, metrics, artifacts)
"""
from __future__ import annotations

from zenml import pipeline, step
from zenml.integrations.mlflow.experiment_trackers import MLFlowExperimentTracker
from zenml.logger import get_logger

logger = get_logger(__name__)


@step
def ingest_data() -> tuple:
    """Ingest raw data and return (dataframe, metadata)."""
    from src.data.ingestion import ingest_raw_data
    from src.config import RAW_DATA_PATH

    return ingest_raw_data(RAW_DATA_PATH)


@step
def validate_data(df_metadata: tuple) -> bool:
    """Run Great Expectations checkpoint on raw data."""
    import great_expectations as ge

    df, metadata = df_metadata
    context = ge.get_context(context_root_dir="great_expectations")
    checkpoint = context.checkpoints.get("dataset_checkpoint")
    result = checkpoint.run(batch_request={"batch_data": df})
    passed = result.success
    logger.info(f"Great Expectations validation: {'PASSED' if passed else 'FAILED'}")
    if not passed:
        raise ValueError("Data validation failed - pipeline aborted")
    return passed


@step
def preprocess_data(df_metadata: tuple):
    """Apply pure preprocessing chain."""
    from src.data.preprocessing import preprocess

    df, metadata = df_metadata
    return preprocess(df)


@step
def build_features_step(clean_df) -> str:
    """Build feature matrix and persist to parquet; return feature path."""
    from src.features.build_features import run

    run()
    return "data/features/features.parquet"


@step
def train_model(feature_path: str) -> dict:
    """Train model with MLflow tracking."""
    from src.models.train import load_training_data, train_and_log
    from sklearn.model_selection import train_test_split

    X, y = load_training_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    result = train_and_log(
        X_train, X_test, y_train, y_test,
        run_name="zenml_training",
        experiment_name="churn_prediction",
        register=True,
    )
    return {
        "run_id": result["run_id"],
        "f1_score": result["metrics"]["f1_score"],
        "accuracy": result["metrics"]["accuracy"],
        "roc_auc": result["metrics"]["roc_auc"],
    }


@pipeline
def training_pipeline():
    """Full training pipeline with caching and MLflow tracking."""
    ingested = ingest_data()
    validate_data(ingested)
    cleaned = preprocess_data(ingested)
    features = build_features_step(cleaned)
    train_model(features)


if __name__ == "__main__":
    training_pipeline()