"""BentoML serving service: ``/predict`` and ``/explain`` endpoints.

The service loads the registered MLflow model and exposes:
- ``predict``: returns the churn probability + class label,
- ``explain``: returns per-feature SHAP contributions for the instance.

Run with: ``bentoml serve src.serving.bento_service:svc``
"""

from __future__ import annotations

import numpy as np
import pandas as pd

import bentoml
from bentoml.io import JSON, NumpyNdarray

MODEL_TAG = "churn_model:production"


def _load_runner():
    model_ref = bentoml.mlflow.get(MODEL_TAG)
    return model_ref.to_runner()


runner = _load_runner()

svc = bentoml.Service("mlops_churn_service", runners=[runner])


@svc.api(input=NumpyNdarray(), output=JSON())
def predict(input_data: np.ndarray) -> dict:
    """Return the predicted class and churn probability."""
    arr = np.asarray(input_data, dtype=np.float32)
    proba = runner.predict_proba.run(arr)[:, 1]
    pred = (proba >= 0.5).astype(int)
    return {
        "prediction": pred.tolist(),
        "churn_probability": proba.tolist(),
    }


@svc.api(input=NumpyNdarray(), output=JSON())
def explain(input_data: np.ndarray) -> dict:
    """Return SHAP force values for the given instance(s)."""
    arr = np.asarray(input_data, dtype=np.float32)
    model = _model_ref()
    import shap

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(arr)
    if isinstance(shap_values, list):
        shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

    return {
        "expected_value": float(explainer.expected_value),
        "shap_values": shap_values.tolist(),
    }


def _model_ref():
    return bentoml.mlflow.get(MODEL_TAG).load()
