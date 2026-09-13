# GPU-serving FastAPI image (local). CUDA base so XGBoost GPU predict works.
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    fastapi==0.108.0 \
    "uvicorn[standard]==0.25.0" \
    pydantic==2.5.3 \
    scikit-learn==1.5.0 \
    pandas==2.2.2 \
    numpy==1.26.4

COPY api/main.py .
COPY ui ./ui
COPY data/raw/generate_creditcard_data.py ./data/raw/generate_creditcard_data.py

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]