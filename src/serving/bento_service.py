"""BentoML serving service: ``/predict`` and ``/explain`` endpoints.

Loads the trained model artifact (``models/churn_model.joblib``) and exposes:
- ``predict``: returns the churn probability + class label,
- ``explain``: returns per-feature SHAP contributions for the instance.

BentoML 1.4 API (@bentoml.service class + @bentoml.api methods; the old
``bentoml.io`` / ``bentoml.Service`` API was removed in 1.3).

Run with: ``bentoml serve src.serving.bento_service:ChurnService``
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import bentoml

MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.joblib"


@bentoml.service(name="mlops_churn_service")
class ChurnService:
    def __init__(self) -> None:
        self._model = None

    def _load_model(self):
        if self._model is None:
            import joblib

            self._model = joblib.load(MODEL_PATH)
        return self._model

    @bentoml.api
    def predict(self, input_data: np.ndarray) -> dict:
        """Return the predicted class and churn probability."""
        arr = np.asarray(input_data, dtype=np.float32)
        proba = self._load_model().predict_proba(arr)[:, 1]
        pred = (proba >= 0.5).astype(int)
        return {
            "prediction": pred.tolist(),
            "churn_probability": proba.tolist(),
        }

    @bentoml.api
    def explain(self, input_data: np.ndarray) -> dict:
        """Return SHAP contributions for the given instance(s)."""
        arr = np.asarray(input_data, dtype=np.float32)
        import shap

        explainer = shap.TreeExplainer(self._load_model())
        shap_values = explainer.shap_values(arr)
        if isinstance(shap_values, list):
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]

        expected_value = explainer.expected_value
        if isinstance(expected_value, (list, np.ndarray)):
            expected_value = expected_value[1] if len(expected_value) > 1 else expected_value[0]

        return {
            "expected_value": float(expected_value),
            "shap_values": shap_values.tolist(),
        }
