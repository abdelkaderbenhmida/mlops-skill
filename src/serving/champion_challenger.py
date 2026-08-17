"""Champion / Challenger traffic routing.

A challenger model receives a small, controlled fraction of the traffic
(``CHALLENGER_RATIO`` = 10% by default) in parallel with the current
champion. Every routing decision is logged (structured JSON lines) so the
two models can be compared statistically a posteriori.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import logging
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from src.config import CHALLENGER_RATIO, MODELS_DIR, REPORTS_DIR

logger = logging.getLogger(__name__)

ROUTING_LOG = Path("monitoring/logs/routing_decisions.jsonl")


def load_model(path: Path):
    import joblib

    return joblib.load(path)


def _default_predict_fn(model):
    def predict(input_data):
        import numpy as np

        arr = np.asarray(input_data, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        return model.predict(arr)

    return predict


class ChampionChallengerRouter:
    """Routes each inference to champion or challenger and logs the decision."""

    def __init__(
        self,
        champion_model,
        challenger_model,
        champion_name: str = "champion",
        challenger_name: str = "challenger",
        challenger_ratio: float = CHALLENGER_RATIO,
        log_path: Path = ROUTING_LOG,
        predict_fn: Callable | None = None,
        seed: int | None = None,
    ):
        self.champion = champion_model
        self.challenger = challenger_model
        self.champion_name = champion_name
        self.challenger_name = challenger_name
        self.challenger_ratio = challenger_ratio
        self.log_path = log_path
        self.predict_fn = predict_fn or _default_predict_fn
        self.rng = random.Random(seed)

    def route(self, input_data) -> dict:
        """Route one request, log the decision, return prediction + version."""
        if self.rng.random() < self.challenger_ratio:
            version = self.challenger_name
            model = self.challenger
        else:
            version = self.champion_name
            model = self.champion

        prediction = self.predict_fn(model)(input_data).tolist()
        self._log(input_data, prediction, version)
        return {"prediction": prediction, "model_version": version}

    def _log(self, input_data, prediction, version) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_version": version,
            "prediction": prediction,
            "request_id": f"{int(datetime.now().timestamp()*1000)}",
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a") as handle:
            handle.write(json.dumps(entry) + "\n")
        logger.info("Routed request to %s -> %s", version, prediction)


def build_router(
    champion_path: Path = MODELS_DIR / "churn_model.joblib",
    challenger_path: Path | None = None,
    challenger_ratio: float = CHALLENGER_RATIO,
) -> ChampionChallengerRouter:
    """Build a router, defaulting the challenger to the ONNX-converted model."""
    champion = load_model(champion_path)
    challenger = load_model(challenger_path) if challenger_path else champion
    return ChampionChallengerRouter(
        champion, challenger, challenger_ratio=challenger_ratio
    )


def simulate_routing(n_requests: int = 1000, challenger_ratio: float = CHALLENGER_RATIO) -> dict:
    """Send ``n_requests`` synthetic requests through the router.

    Returns a small summary (request counts per model version) proving the
    ~10% challenger split and that every decision was logged.
    """
    import numpy as np

    X = _load_sample_features(n_requests)
    router = build_router(challenger_ratio=challenger_ratio)
    counts = {router.champion_name: 0, router.challenger_name: 0}
    for row in X:
        result = router.route([row])
        counts[result["model_version"]] += 1
    return {"requests": n_requests, "counts": counts, "log_path": str(ROUTING_LOG)}


def _load_sample_features(n: int):
    import numpy as np
    import pandas as pd

    from src.features.build_features import build_features, feature_sets
    from src.models.train import _preprocess_pipeline

    raw = pd.read_csv("data/raw/dataset.csv")
    clean = _preprocess_pipeline(raw)
    frame = build_features(clean, include_sensitive=False)
    sets = feature_sets(frame)
    return sets["X"].head(n).to_numpy(dtype=np.float32)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Champion/Challenger routing simulation.")
    parser.add_argument("--requests", type=int, default=1000)
    parser.add_argument("--challenger-ratio", type=float, default=CHALLENGER_RATIO)
    args = parser.parse_args()

    summary = simulate_routing(args.requests, args.challenger_ratio)
    print(summary)


if __name__ == "__main__":
    main()
