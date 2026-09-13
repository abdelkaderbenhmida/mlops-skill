# GPU training image (local). NVIDIA CUDA runtime so XGBoost gpu_hist works.
FROM nvidia/cuda:12.2.2-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

# /workspace/src must import cleanly (src on sys.path), so use python -m.
ENV PYTHONPATH=/workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir \
    mlflow==2.15.1 \
    xgboost>=3.0.0 \
    scikit-learn==1.5.0 \
    pandas==2.2.2 \
    numpy==1.26.4 \
    matplotlib==3.9.2 \
    pyyaml==6.0.1

COPY src/ ./src/
COPY data/raw/dataset.csv ./data/raw/dataset.csv

# MLflow local file store lives at mlflow/mlruns (mounted from host in compose).

ENTRYPOINT ["python3", "-m", "src.models.train"]