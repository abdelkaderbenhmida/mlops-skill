# MLOps Full Project — Pure MLOps Skills Maximization

> **Périmètre** : 100 % MLOps tooling — cycle de vie données/modèle, feature store, tuning, explicabilité, équité, serving, monitoring, champion/challenger. **Exclu** : Kubernetes, Terraform/Ansible, Vault, monitoring infra générique.

---

## Architecture Overview

```
Raw Data → Great Expectations → DVC → Feature Engineering → Feast (Feature Store)
                                                                    ↓
                        ┌──────────────────────────────────────────┼────────────────────────────┐
                        ↓                                          ↓                            ↓
                 Optuna (50 trials)                      MLflow Tracking                  AutoML (FLAML)
                        ↓                                          ↓                            ↓
                        └──────────────────────────┬───────────────┘                            ↓
                                                   ↓
                                          Deepchecks Validation
                                                   ↓
                                    ┌──────────────┼──────────────┐
                                    ↓              ↓              ↓
                               SHAP/LIME    Fairlearn         ONNX Export
                               (explain)    (fairness)         (portability)
                                    ↓              ↓              ↓
                                                   MLflow Registry (Staging/Production)
                                                   ↓
                                          BentoML Service
                                          /predict + /explain
                                                   ↓
                                    ┌──────────────┼──────────────┐
                                    ↓              ↓
                            Champion (90%)    Challenger (10%)
                                    ↓              ↓
                                    └──────┬───────┘
                                           ↓
                                   Evidently Monitoring
                                   (Data/Concept/Prediction Drift)
                                           ↓
                              Retraining Trigger → ZenML Pipeline
```

---

## Repository Structure

```
mlops-full-project/
├── data/
│   ├── raw/                    # Immutable raw data (dataset.csv + generator)
│   ├── processed/              # Cleaned data
│   ├── reference/              # Reference dataset for drift detection
│   └── features/               # Engineered features (parquet)
├── great_expectations/
│   └── expectations/dataset_suite.json
├── feature_repo/               # Feast feature store
│   ├── feature_store.yaml
│   ├── entities.py
│   ├── features.py
│   └── data_sources.py
├── pipelines/                  # ZenML pipelines
│   ├── training_pipeline.py
│   ├── tuning_pipeline.py
│   └── retraining_pipeline.py
├── src/
│   ├── data/
│   │   ├── ingestion.py        # Logs row count, time period, source hash
│   │   └── preprocessing.py    # Pure functions
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py            # MLflow tracking
│   │   ├── tune.py             # Optuna bayesian search
│   │   ├── automl_baseline.py  # FLAML comparative baseline
│   │   ├── evaluate.py
│   │   ├── explain.py          # SHAP + LIME
│   │   ├── fairness_check.py   # Fairlearn
│   │   ├── export_onnx.py      # skl2onnx + parity check
│   │   └── promote.py          # Promotion gates
│   ├── serving/
│   │   ├── bento_service.py    # BentoML /predict + /explain
│   │   └── champion_challenger.py
│   └── monitoring/
│       ├── drift_report.py     # Evidently DataDrift + TargetDrift
│       └── retraining_trigger.py
├── model_cards/
│   └── model_card_template.py  # Auto-generated from MLflow + Fairlearn
├── tests/
│   ├── unit/
│   ├── model/
│   └── data/
├── notebooks/
│   └── exploration.ipynb
├── mlflow/mlruns/
├── dvc.yaml
├── requirements.txt
├── pyproject.toml
├── Dockerfile.bento
└── README.md
```

---

## Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python data/raw/generate_churn_data.py
# Outputs: data/raw/dataset.csv (~7000 rows, sensitive attribute: gender)
```

### 3. Run Data Validation (Great Expectations)

```bash
great_expectations checkpoint run dataset_checkpoint
```

### 4. Run DVC Pipeline

```bash
dvc repro
```

### 5. Train + Track with MLflow

```bash
python -m src.models.train --register --run-name churn_rf
# Or via ZenML:
python -m pipelines.training_pipeline
```

### 6. Hyperparameter Tuning (Optuna)

```bash
python -m src.models.tune --trials 50
# Or via ZenML:
python -m pipelines.tuning_pipeline
```

### 7. AutoML Baseline (FLAML)

```bash
python -m src.models.automl_baseline --time-budget 60
```

### 8. Explainability (SHAP + LIME)

```bash
python -m src.models.explain
# Generates: reports/shap_summary.png, LIME explanations
```

### 9. Fairness Audit (Fairlearn)

```bash
python -m src.models.fairness_check
# Generates: reports/fairness_report.json, reports/fairness_selection_rate.png
# Fails if demographic parity difference > 0.1
```

### 10. ONNX Export + Parity Check

```bash
python -m src.models.export_onnx
# Generates: models/churn_model.onnx, reports/onnx_parity_report.json
```

### 11. Promotion Gates

```bash
python -m src.models.promote
# Checks: F1 threshold, beats production, Deepchecks, Fairness
# On success: moves model to MLflow Production stage + generates model card
```

### 12. Serve with BentoML

```bash
bentoml serve src.serving.bento_service:svc
# POST /predict  → {prediction, churn_probability}
# POST /explain  → {expected_value, shap_values}
```

### 13. Champion/Challenger Routing

```bash
python -m src.serving.champion_challenger --requests 1000
# Routes ~10% to challenger, logs every decision to monitoring/logs/routing_decisions.jsonl
```

### 14. Drift Monitoring (Evidently)

```bash
python -m src.monitoring.drift_report --drift-strength 0.5
# Generates: monitoring/reports/drift_report.html
# Extracts dataset_drift score
```

### 15. Automated Retraining Trigger

```bash
python -m src.monitoring.retraining_trigger --dry-run
# Triggers ZenML retraining_pipeline when drift_score > 0.3
```

---

## Key MLOps Skills Demonstrated

| Domain | Tool | Status |
|--------|------|--------|
| Data Versioning | DVC | ✅ |
| Data Quality | Great Expectations | ✅ |
| Feature Store | Feast (offline + online) | ✅ |
| ML Orchestration | ZenML | ✅ |
| Experiment Tracking | MLflow | ✅ |
| Hyperparameter Tuning | Optuna (Bayesian, 50 trials) | ✅ |
| AutoML Baseline | FLAML | ✅ |
| Model Registry | MLflow Registry | ✅ |
| Model Validation | Deepchecks | ✅ |
| Explainability | SHAP (global + local), LIME | ✅ |
| Fairness | Fairlearn (DP diff, EqOdds diff) | ✅ |
| Model Portability | ONNX + parity check | ✅ |
| Model Serving | BentoML (predict + explain) | ✅ |
| Champion/Challenger | Custom router + logging | ✅ |
| Production Monitoring | Evidently (3 drift types) | ✅ |
| Model Cards | Auto-generated (MLflow + Fairlearn) | ✅ |
| Automated Retraining | Drift-triggered ZenML pipeline | ✅ |

---

## Configuration

Key thresholds in `src/config.py`:

```python
FAIRNESS_DP_THRESHOLD = 0.1      # Demographic parity difference max
DRIFT_THRESHOLD = 0.3            # Drift score trigger
F1_PROMOTION_THRESHOLD = 0.5     # Minimum F1 for promotion
CHALLENGER_RATIO = 0.1           # 10% traffic to challenger
```

---

## Model Card

Auto-generated at each promotion to `model_cards/model_card.md` containing:
- Model details & intended use
- Training data description
- Performance metrics (accuracy, F1, ROC-AUC)
- Fairness analysis (selection rates by gender, DP difference, EqOdds difference)
- Promotion gate statuses
- Known limitations

---

## Tests

```bash
# Unit tests
pytest tests/unit/

# Data validation tests
pytest tests/data/

# Model quality tests (Deepchecks)
pytest tests/model/
```

---

## License

MIT — Educational / portfolio project demonstrating pure MLOps tooling depth.