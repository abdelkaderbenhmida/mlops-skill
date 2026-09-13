"""FastAPI app for Fraud Detection (P3) — self-contained, trains on creditcard.csv at startup.

Data comes from the repository (``data/raw/creditcard.csv``, produced by
``data/raw/generate_creditcard_data.py``); set FRAUD_DATA_PATH to point at a
real export instead.
"""

import os
import subprocess
import sys
import time
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, f1_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UI_DIR = PROJECT_ROOT / "ui"
GENERATOR = PROJECT_ROOT / "data" / "raw" / "generate_creditcard_data.py"
REAL_DATA_PATH = Path(
    os.getenv("FRAUD_DATA_PATH", PROJECT_ROOT / "data" / "raw" / "creditcard.csv")
)
MODEL = None
SCALER = None
FEATURE_COLS = None
MODEL_META = {}
PREDICTION_LOG = []
LOG_CAP = 500

RISK_LEVELS = ["low", "medium", "high", "critical"]

class PredictRequest(BaseModel):
    Time: float = Field(default=0, ge=0)
    V1: float = Field(default=0)
    V2: float = Field(default=0)
    V3: float = Field(default=0)
    V4: float = Field(default=0)
    V5: float = Field(default=0)
    V6: float = Field(default=0)
    V7: float = Field(default=0)
    V8: float = Field(default=0)
    V9: float = Field(default=0)
    V10: float = Field(default=0)
    V11: float = Field(default=0)
    V12: float = Field(default=0)
    V13: float = Field(default=0)
    V14: float = Field(default=0)
    V15: float = Field(default=0)
    V16: float = Field(default=0)
    V17: float = Field(default=0)
    V18: float = Field(default=0)
    V19: float = Field(default=0)
    V20: float = Field(default=0)
    V21: float = Field(default=0)
    V22: float = Field(default=0)
    V23: float = Field(default=0)
    V24: float = Field(default=0)
    V25: float = Field(default=0)
    V26: float = Field(default=0)
    V27: float = Field(default=0)
    V28: float = Field(default=0)
    Amount: float = Field(default=100, ge=0)

class PredictResponse(BaseModel):
    prediction: str
    probability: float
    risk_level: str

def load_real_data():
    """Load creditcard.csv, generating the synthetic demo file if absent."""
    if not REAL_DATA_PATH.exists():
        print(f"P3: {REAL_DATA_PATH} missing, generating synthetic demo data")
        REAL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [sys.executable, str(GENERATOR), "--output", str(REAL_DATA_PATH)],
            check=True,
        )
    df = pd.read_csv(REAL_DATA_PATH)
    # Drop NaN rows
    initial = len(df)
    df = df.dropna(subset=["Class"])
    if len(df) < initial:
        print(f"P3: Dropped {initial - len(df)} rows with NaN Class")
    print(f"P3: Loaded {len(df)} real transactions, fraud rate={df['Class'].mean()*100:.2f}%")
    return df

def train_model():
    global MODEL, SCALER, FEATURE_COLS, MODEL_META
    
    df = load_real_data()
    
    # Features: Time, V1-V28, Amount; Target: Class
    FEATURE_COLS = [c for c in df.columns if c != "Class"]
    X = df[FEATURE_COLS]
    y = df["Class"]
    
    # Scale features (important for V1-V28 PCA features)
    SCALER = StandardScaler()
    X_scaled = SCALER.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    MODEL = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced_subsample")
    MODEL.fit(X_train, y_train)
    
    proba = MODEL.predict_proba(X_test)[:, 1]
    preds = MODEL.predict(X_test)
    auc = roc_auc_score(y_test, proba)
    f1 = f1_score(y_test, preds)
    print(f"P3: AUC={auc:.4f}, F1={f1:.4f}")
    
    MODEL_META = {
        "model_name": "RandomForestClassifier",
        "n_estimators": MODEL.n_estimators,
        "max_depth": int(MODEL.max_depth or 0),
        "class_weight": "balanced_subsample",
        "trained_samples": int(len(df)),
        "feature_count": int(len(FEATURE_COLS)),
        "auc": round(auc, 4),
        "f1": round(f1, 4),
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "data_source": str(REAL_DATA_PATH)
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    train_model()
    yield

app = FastAPI(title="Fraud Detection API (Real Data)", version="1.0.0", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": MODEL is not None, "data_source": str(REAL_DATA_PATH)}

@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    t0 = time.perf_counter()
    input_dict = req.model_dump()
    
    # Build feature vector in correct order
    feat_vec = np.array([input_dict[col] for col in FEATURE_COLS]).reshape(1, -1)
    feat_scaled = SCALER.transform(feat_vec)
    
    prob = float(MODEL.predict_proba(feat_scaled)[0][1])
    pred = "fraud" if prob >= 0.5 else "legitimate"
    risk = "critical" if prob >= 0.7 else "high" if prob >= 0.4 else "medium" if prob >= 0.15 else "low"
    latency_ms = round((time.perf_counter() - t0) * 1000, 2)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_dict,
        "result": {
            "prediction": pred,
            "probability": round(prob, 4),
            "risk_level": risk,
        },
        "latency_ms": latency_ms,
    }
    PREDICTION_LOG.append(entry)
    if len(PREDICTION_LOG) > LOG_CAP:
        del PREDICTION_LOG[: len(PREDICTION_LOG) - LOG_CAP]

    return PredictResponse(prediction=pred, probability=round(prob, 4), risk_level=risk)

@app.get("/history")
async def history(limit: int = 50):
    n = max(1, min(limit, LOG_CAP))
    return {"total": len(PREDICTION_LOG), "entries": list(reversed(PREDICTION_LOG))[:n]}

@app.get("/stats")
async def stats():
    n = len(PREDICTION_LOG)
    empty = {
        "total_scans": 0,
        "fraud_rate": 0.0,
        "flagged_count": 0,
        "risk_level_distribution": {lvl: 0 for lvl in RISK_LEVELS},
        "avg_probability": 0.0,
        "avg_latency_ms": 0.0,
    }
    if n == 0:
        return empty
    flagged = sum(1 for e in PREDICTION_LOG if e["result"]["prediction"] == "fraud")
    dist = {lvl: 0 for lvl in RISK_LEVELS}
    for e in PREDICTION_LOG:
        dist[e["result"]["risk_level"]] += 1
    return {
        "total_scans": n,
        "fraud_rate": round(flagged / n, 4),
        "flagged_count": flagged,
        "risk_level_distribution": dist,
        "avg_probability": round(sum(e["result"]["probability"] for e in PREDICTION_LOG) / n, 4),
        "avg_latency_ms": round(sum(e["latency_ms"] for e in PREDICTION_LOG) / n, 2),
    }

@app.get("/model-info")
async def model_info():
    if MODEL is None or FEATURE_COLS is None:
        return {"error": "model not loaded"}
    f_imports = sorted(
        zip(FEATURE_COLS, MODEL.feature_importances_),
        key=lambda pair: pair[1],
        reverse=True,
    )
    return {
        **MODEL_META,
        "feature_importance": [
            {"feature": name, "importance": round(imp, 4)} for name, imp in f_imports
        ],
    }

@app.get("/")
async def serve_ui():
    return FileResponse(UI_DIR / "index.html")

if UI_DIR.exists():
    app.mount("/ui", StaticFiles(directory=str(UI_DIR)), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)