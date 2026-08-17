"""Model explainability: SHAP (global + local) and LIME (local).

- SHAP ``TreeExplainer`` produces a global summary plot saved to
  ``reports/shap_summary.png`` plus per-instance local explanations.
- LIME is run independently on a few test instances to cross-check the local
  explanations with a method different from SHAP.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import MLFLOW_DIR, REPORTS_DIR


def compute_shap(model, X_sample: pd.DataFrame) -> dict:
    import shap

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)

    # GradientBoosting / modern shap returns a single (n, p) array for
    # binary classifiers; handle the legacy (p, n) pair case too.
    if isinstance(shap_values, list):
        shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    elif getattr(shap_values, "ndim", 0) == 3:
        shap_values = shap_values[..., 1]

    mean_abs = np.abs(shap_values).mean(axis=0)
    importance = pd.Series(mean_abs, index=X_sample.columns).sort_values(ascending=False)
    return {"explainer": explainer, "shap_values": shap_values, "importance": importance}


def save_shap_summary(model, X_sample: pd.DataFrame, path: Path) -> dict:
    import shap

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    if isinstance(shap_values, list):
        shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
    elif getattr(shap_values, "ndim", 0) == 3:
        shap_values = shap_values[..., 1]

    path.parent.mkdir(parents=True, exist_ok=True)
    shap.summary_plot(shap_values, X_sample, show=False)
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()

    mean_abs = np.abs(shap_values).mean(axis=0)
    return pd.Series(mean_abs, index=X_sample.columns).sort_values(ascending=False)


def explain_lime(model, X_sample: pd.DataFrame, feature_names: list, n: int = 5) -> list:
    import lime
    from lime.lime_tabular import LimeTabularExplainer

    X_np = X_sample.values
    explainer = LimeTabularExplainer(
        X_np,
        feature_names=feature_names,
        class_names=["not_churn", "churn"],
        mode="classification",
        random_state=42,
    )
    explanations = []
    for i in range(min(n, len(X_np))):
        exp = explainer.explain_instance(
            X_np[i], model.predict_proba, num_features=5, labels=(1,)
        )
        explanations.append(
            {"instance": i, "top_features": exp.as_list(label=1)}
        )
    return explanations


def run(model_path: Path = Path("models/churn_model.joblib"), n_samples: int = 200) -> dict:
    import joblib

    from src.models.evaluate import _load_data
    from src.models.train import _preprocess_pipeline
    from src.features.build_features import build_features, feature_sets

    model = joblib.load(model_path)

    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=False)
    sets = feature_sets(frame)
    X = sets["X"]
    X_sample = X.sample(n=min(n_samples, len(X)), random_state=42)

    importance = save_shap_summary(model, X_sample, REPORTS_DIR / "shap_summary.png")

    local_shap = []
    explainer_shap = _shap_explainer(model, X_sample)
    shap_values = _shap_values(explainer_shap, X_sample)
    local_shap.append({"instance": 0, "values": shap_values[0].tolist()})

    lime_explanations = explain_lime(model, X_sample, list(X_sample.columns), n=3)

    result = {
        "shap_importance": importance.to_dict(),
        "shap_summary_path": str(REPORTS_DIR / "shap_summary.png"),
        "lime_explanations": lime_explanations,
        "n_instances_explained": len(local_shap),
    }
    return result


def _shap_explainer(model, X_sample):
    import shap

    return shap.TreeExplainer(model)


def _shap_values(explainer, X_sample):
    values = explainer.shap_values(X_sample)
    if isinstance(values, list):
        values = values[1] if len(values) > 1 else values[0]
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description="SHAP + LIME explainability report.")
    parser.add_argument("--model", default="models/churn_model.joblib")
    parser.add_argument("--samples", type=int, default=200)
    args = parser.parse_args()

    result = run(Path(args.model), n_samples=args.samples)
    print("SHAP top-5 features:", list(result["shap_importance"].items())[:5])
    print("Saved summary to:", result["shap_summary_path"])
    print("LIME explanations generated for", len(result["lime_explanations"]), "instances")


if __name__ == "__main__":
    main()
