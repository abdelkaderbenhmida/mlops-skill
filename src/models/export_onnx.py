"""ONNX export and parity verification.

Converts the trained sklearn model to ONNX with ``skl2onnx``, then checks that
the ONNX model produces predictions identical (within a numeric tolerance) to
the original sklearn model on the held-out test set.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from src.config import MODELS_DIR
from src.config import REPORTS_DIR

TOLERANCE = 1e-5


def export_to_onnx(model_path: Path = MODELS_DIR / "churn_model.joblib",
                   out_path: Path = MODELS_DIR / "churn_model.onnx") -> Path:
    import joblib
    import onnxruntime as ort

    model = joblib.load(model_path)

    X = _load_feature_matrix()
    n_features = X.shape[1]
    initial_types = [("input", FloatTensorType([None, n_features]))]
    onnx_model = convert_sklearn(model, initial_types=initial_types)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as handle:
        handle.write(onnx_model.SerializeToString())

    parity = check_parity(model, X, out_path, n_features)
    _write_report(parity)
    return out_path


def _load_feature_matrix() -> pd.DataFrame:
    from src.features.build_features import build_features, feature_sets
    from src.models.train import _preprocess_pipeline

    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=False)
    sets = feature_sets(frame)
    X = sets["X"].astype(np.float32)
    return X.sample(n=min(500, len(X)), random_state=42)


def check_parity(model, X: pd.DataFrame, onnx_path: Path, n_features: int) -> dict:
    import onnxruntime as ort

    X_np = X.to_numpy(dtype=np.float32)

    sklearn_pred = model.predict(X_np)
    sklearn_proba = model.predict_proba(X_np)[:, 1]

    session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    onnx_out = session.run(None, {"input": X_np})
    # ONNX output may be (proba) or (label, proba) depending on converter.
    onnx_proba = onnx_out[-1]
    if isinstance(onnx_proba, list):
        if isinstance(onnx_proba[0], dict):
            onnx_proba = np.array([row[1] for row in onnx_proba])
        else:
            onnx_proba = np.asarray(onnx_proba)
    if onnx_proba.ndim == 2:
        onnx_proba = onnx_proba[:, 1]

    proba_diff = float(np.max(np.abs(sklearn_proba - onnx_proba)))
    onnx_pred = (onnx_proba >= 0.5).astype(int)
    label_agreement = float(np.mean(sklearn_pred == onnx_pred))

    return {
        "max_proba_abs_diff": proba_diff,
        "label_agreement": label_agreement,
        "n_instances": int(len(X_np)),
        "tolerance": TOLERANCE,
        "passed": proba_diff <= TOLERANCE,
    }


def _write_report(parity: dict) -> None:
    import json

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_DIR / "onnx_parity_report.json", "w") as handle:
        json.dump(parity, handle, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export model to ONNX and verify parity.")
    parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.joblib"))
    parser.add_argument("--output", default=str(MODELS_DIR / "churn_model.onnx"))
    args = parser.parse_args()

    path = export_to_onnx(Path(args.model), Path(args.output))
    print(f"ONNX model written to {path}")
    report = _read_report()
    print(
        f"Parity: max proba diff={report['max_proba_abs_diff']:.2e} "
        f"-> {'PASS' if report['passed'] else 'FAIL'} "
        f"(label agreement {report['label_agreement']:.4f})"
    )


def _read_report() -> dict:
    import json

    with open(REPORTS_DIR / "onnx_parity_report.json") as handle:
        return json.load(handle)


if __name__ == "__main__":
    main()
