"""FastAPI server for fraud detection.

Self-contained: trains model on startup using real credit card data.
Endpoints: /health, /predict, /history, /stats, /model-info, / (UI)
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.config import BASE_FEATURES, MLFLOW_DIR, MODELS_DIR, TARGET_COL
from src.data.ingestion import ingest_raw_data
from src.data.preprocessing import preprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = MODELS_DIR / "fraud_model.joblib"
FEATURE_COLS_PATH = MODELS_DIR / "feature_columns.txt"

prediction_history: list[dict] = []
model: RandomForestClassifier | None = None
feature_columns: list[str] = []
model_info: dict[str, Any] = {}


def train_model() -> tuple[RandomForestClassifier, list[str], dict]:
    """Train the fraud detection model on real data."""
    logger.info("Loading and preprocessing data...")
    raw, meta = ingest_raw_data()
    clean = preprocess(raw)

    feature_cols = [c for c in clean.columns if c != TARGET_COL]
    X = clean[feature_cols]
    y = clean[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    logger.info("Training RandomForest with class_weight='balanced_subsample'...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=5,
        max_features="sqrt",
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    y_proba = rf.predict_proba(X_test)[:, 1]

    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    feature_importance = dict(zip(feature_cols, rf.feature_importances_))
    top_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:15]

    info = {
        "model_name": "fraud-detection-model",
        "model_type": "RandomForestClassifier",
        "n_estimators": 200,
        "max_depth": 12,
        "class_weight": "balanced_subsample",
        "trained_samples": len(X_train),
        "test_samples": len(X_test),
        "f1": f1,
        "auc": auc,
        "feature_importance": top_features,
        "feature_columns": feature_cols,
        "class_distribution": meta.get("class_distribution", {}),
        "trained_at": datetime.utcnow().isoformat() + "Z",
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(rf, MODEL_PATH)
    with open(FEATURE_COLS_PATH, "w") as f:
        f.write("\n".join(feature_cols))

    logger.info(f"Model trained: F1={f1:.4f}, AUC={auc:.4f}")
    return rf, feature_cols, info


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, feature_columns, model_info
    logger.info("Starting up: training model on real credit card data...")
    try:
        model, feature_columns, model_info = train_model()
        logger.info("Model ready.")
    except Exception as e:
        logger.error(f"Failed to train model: {e}")
        model = None
        feature_columns = []
        model_info = {"error": str(e)}
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Fraud Detection API",
    description="Real-time credit card fraud detection using RandomForest on PCA features",
    version="1.0.0",
    lifespan=lifespan,
)

ui_path = Path(__file__).resolve().parents[2].parents[1] / "ui"
if ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(ui_path)), name="static")


class PredictRequest(BaseModel):
    Time: float = Field(..., description="Seconds elapsed since first transaction")
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float = Field(..., description="Transaction amount")


class PredictResponse(BaseModel):
    prediction: str = Field(..., description="fraud or legitimate")
    probability: float = Field(..., description="Fraud probability [0,1]")
    risk_level: str = Field(..., description="low, medium, high, critical")
    request_id: str
    latency_ms: int


def compute_risk_level(probability: float) -> str:
    if probability >= 0.9:
        return "critical"
    elif probability >= 0.7:
        return "high"
    elif probability >= 0.3:
        return "medium"
    return "low"


@app.get("/health")
async def health():
    return {
        "status": "ok" if model is not None else "degraded",
        "model_loaded": model is not None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest, http_request: Request):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start = time.perf_counter()

    input_dict = request.model_dump()
    input_array = np.array([[input_dict[col] for col in feature_columns]])
    prob = float(model.predict_proba(input_array)[0, 1])
    pred = "fraud" if prob >= 0.5 else "legitimate"
    risk = compute_risk_level(prob)
    latency_ms = int((time.perf_counter() - start) * 1000)

    req_id = str(uuid.uuid4())[:8]
    record = {
        "request_id": req_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input": input_dict,
        "result": {
            "prediction": pred,
            "probability": prob,
            "risk_level": risk,
        },
        "latency_ms": latency_ms,
    }
    prediction_history.append(record)

    return PredictResponse(
        prediction=pred,
        probability=prob,
        risk_level=risk,
        request_id=req_id,
        latency_ms=latency_ms,
    )


@app.get("/history")
async def history(limit: int = 100):
    return {"entries": prediction_history[-limit:]}


@app.get("/stats")
async def stats():
    if not prediction_history:
        return {
            "total_scans": 0,
            "fraud_rate": 0.0,
            "flagged_count": 0,
            "avg_probability": 0.0,
            "avg_latency_ms": 0,
            "risk_level_distribution": {"low": 0, "medium": 0, "high": 0, "critical": 0},
        }

    total = len(prediction_history)
    flagged = sum(1 for h in prediction_history if h["result"]["prediction"] == "fraud")
    avg_prob = sum(h["result"]["probability"] for h in prediction_history) / total
    avg_lat = sum(h["latency_ms"] for h in prediction_history) / total

    risk_dist = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for h in prediction_history:
        risk_dist[h["result"]["risk_level"]] += 1

    return {
        "total_scans": total,
        "fraud_rate": flagged / total,
        "flagged_count": flagged,
        "avg_probability": avg_prob,
        "avg_latency_ms": round(avg_lat, 1),
        "risk_level_distribution": risk_dist,
    }


@app.get("/model-info")
async def model_info_endpoint():
    if not model_info:
        return {"error": "Model not trained yet"}
    return model_info


@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = ui_path / "index.html"
    if index_path.exists():
        return index_path.read_text()
    return HTMLResponse("<h1>Fraud Detection API</h1><p>UI not found. See <a href='/docs'>/docs</a> for API.</p>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8101, reload=False)