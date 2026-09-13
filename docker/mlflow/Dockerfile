# MLflow tracking UI over the project's LOCAL file store (mlflow/mlruns).
# No Azure. This container is read-mostly: the train container writes the same
# mlruns dir via a shared host volume.
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MLFLOW_HOME=/opt/mlflow

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    mlflow==2.15.1 \
    psycopg2-binary \
    boto3

WORKDIR /opt/mlflow

VOLUME ["/opt/mlflow/mlruns"]

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -fsS http://localhost:5000/health || exit 1

ENTRYPOINT ["mlflow", "server"]