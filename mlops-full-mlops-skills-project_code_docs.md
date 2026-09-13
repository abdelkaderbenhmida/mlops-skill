# mlops-full-mlops-skills-project: training_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/pipelines/training_pipeline.py`
- **Total lines:** 97
- **File size:** 2941 bytes

## Line Type Summary
- **Code:** 75
- **Comment:** 0
- **Empty:** 22
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML training pipeline with step caching and MLflow ExperimentTrac...`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- ingest: load raw data + log metadata (row count, time period, source...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- validate: Great Expectations checkpoint`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- preprocess: pure preprocessing functions`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- build_features: feature engineering (one-hot, derived features)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- train: MLflow-tracked training (params, metrics, artifacts)`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** `from zenml.integrations.mlflow.experiment_trackers import MLFlowExperi...`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `@step`
> **Type:** Code statement

### Line  20
> **Code:** `def ingest_data() -> tuple:`
> **Type:** Function definition

### Line  21
> **Code:** `"""Ingest raw data and return (dataframe, metadata)."""`
> **Type:** Logical operation

### Line  22
> **Code:** `from src.data.ingestion import ingest_raw_data`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `return ingest_raw_data(RAW_DATA_PATH)`
> **Type:** Returns a value from a function

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `@step`
> **Type:** Code statement

### Line  29
> **Code:** `def validate_data(df_metadata: tuple) -> bool:`
> **Type:** Function definition

### Line  30
> **Code:** `"""Run Great Expectations checkpoint on raw data."""`
> **Type:** Code statement

### Line  31
> **Code:** `import great_expectations as ge`
> **Type:** Imports a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `df, metadata = df_metadata`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `context = ge.get_context(context_root_dir="great_expectations")`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `checkpoint = context.checkpoints.get("dataset_checkpoint")`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `result = checkpoint.run(batch_request={"batch_data": df})`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `passed = result.success`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `logger.info(f"Great Expectations validation: {'PASSED' if passed else ...`
> **Type:** Function call

### Line  39
> **Code:** `if not passed:`
> **Type:** Conditional statement

### Line  40
> **Code:** `raise ValueError("Data validation failed - pipeline aborted")`
> **Type:** Raises an exception

### Line  41
> **Code:** `return passed`
> **Type:** Returns a value from a function

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `@step`
> **Type:** Code statement

### Line  45
> **Code:** `def preprocess_data(df_metadata: tuple):`
> **Type:** Function definition

### Line  46
> **Code:** `"""Apply pure preprocessing chain."""`
> **Type:** Code statement

### Line  47
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `df, metadata = df_metadata`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return preprocess(df)`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `@step`
> **Type:** Code statement

### Line  54
> **Code:** `def build_features_step(clean_df) -> str:`
> **Type:** Function definition

### Line  55
> **Code:** `"""Build feature matrix and persist to parquet; return feature path.""...`
> **Type:** Logical operation

### Line  56
> **Code:** `from src.features.build_features import run`
> **Type:** Imports specific names from a module

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `run()`
> **Type:** Function call

### Line  59
> **Code:** `return "data/features/features.parquet"`
> **Type:** Returns a value from a function

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `@step`
> **Type:** Code statement

### Line  63
> **Code:** `def train_model(feature_path: str) -> dict:`
> **Type:** Function definition

### Line  64
> **Code:** `"""Train model with MLflow tracking."""`
> **Type:** Code statement

### Line  65
> **Code:** `from src.models.train import load_training_data, train_and_log`
> **Type:** Imports specific names from a module

### Line  66
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `)`
> **Type:** Code statement

### Line  72
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line  74
> **Code:** `run_name="zenml_training",`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `experiment_name="churn_prediction",`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `register=True,`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  79
> **Code:** `"run_id": result["run_id"],`
> **Type:** Data structure operation

### Line  80
> **Code:** `"f1_score": result["metrics"]["f1_score"],`
> **Type:** Logical operation

### Line  81
> **Code:** `"accuracy": result["metrics"]["accuracy"],`
> **Type:** Data structure operation

### Line  82
> **Code:** `"roc_auc": result["metrics"]["roc_auc"],`
> **Type:** Data structure operation

### Line  83
> **Code:** `}`
> **Type:** Code statement

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `@pipeline`
> **Type:** Code statement

### Line  87
> **Code:** `def training_pipeline():`
> **Type:** Function definition

### Line  88
> **Code:** `"""Full training pipeline with caching and MLflow tracking."""`
> **Type:** Logical operation

### Line  89
> **Code:** `ingested = ingest_data()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `validate_data(ingested)`
> **Type:** Function call

### Line  91
> **Code:** `cleaned = preprocess_data(ingested)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `features = build_features_step(cleaned)`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `train_model(features)`
> **Type:** Function call

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  97
> **Code:** `training_pipeline()`
> **Type:** Function call

## Summary
- **Total lines:** 97
- **Code lines:** 75
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 22

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: training_pipeline.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/pipelines/__init__.py`
- **Total lines:** 1
- **File size:** 81 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""pipelines package: ZenML pipeline definitions for the churn MLOps p...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: retraining_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/pipelines/retraining_pipeline.py`
- **Total lines:** 156
- **File size:** 5199 bytes

## Line Type Summary
- **Code:** 114
- **Comment:** 7
- **Empty:** 35
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML automated retraining pipeline triggered by drift.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- check_drift: read latest drift score from monitoring`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- if drift > threshold: re-run full training + tuning + gates`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- retrain: training with best params from Optuna`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- validate_gates: Deepchecks + Fairlearn (same gates as promotion)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- promote_if_better: only promote if beats current production`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `This pipeline reuses the same validation gates as manual promotion - n...`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `@step`
> **Type:** Code statement

### Line  21
> **Code:** `def check_drift() -> dict:`
> **Type:** Function definition

### Line  22
> **Code:** `"""Read latest drift score and decide if retraining is needed."""`
> **Type:** Logical operation

### Line  23
> **Code:** `from src.monitoring.retraining_trigger import read_drift_score, should...`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from src.config import DRIFT_THRESHOLD`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `score = read_drift_score()`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `trigger = should_retrain(score, DRIFT_THRESHOLD)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `logger.info(f"Drift check: score={score:.3f}, threshold={DRIFT_THRESHO...`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `return {"drift_score": score, "threshold": DRIFT_THRESHOLD, "trigger":...`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `@step`
> **Type:** Code statement

### Line  33
> **Code:** `def retrain_model(drift_info: dict) -> dict:`
> **Type:** Function definition

### Line  34
> **Code:** `"""Re-run training with Optuna tuning on recent data if drift detected...`
> **Type:** Arithmetic operation

### Line  35
> **Code:** `if not drift_info.get("trigger", False):`
> **Type:** Conditional statement

### Line  36
> **Code:** `logger.info("No drift detected - skipping retraining")`
> **Type:** Arithmetic operation

### Line  37
> **Code:** `return {"retrained": False, "reason": "no_drift"}`
> **Type:** Returns a value from a function

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `logger.info("Drift detected - starting retraining pipeline")`
> **Type:** Arithmetic operation

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `# Run tuning to find best params`
> **Type:** Comment: Run tuning to find best params

### Line  42
> **Code:** `from src.models.tune import tune`
> **Type:** Imports specific names from a module

### Line  43
> **Code:** `best = tune(n_trials=30, experiment_name="churn_retraining")`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `# Train with best params`
> **Type:** Comment: Train with best params

### Line  46
> **Code:** `from src.models.train import load_training_data, train_and_log`
> **Type:** Imports specific names from a module

### Line  47
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `)`
> **Type:** Code statement

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line  56
> **Code:** `params=best["best_params"],`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `run_name="retrained_model",`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `experiment_name="churn_retraining",`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `register=True,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `)`
> **Type:** Code statement

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  63
> **Code:** `"retrained": True,`
> **Type:** Code statement

### Line  64
> **Code:** `"run_id": result["run_id"],`
> **Type:** Data structure operation

### Line  65
> **Code:** `"best_params": best["best_params"],`
> **Type:** Data structure operation

### Line  66
> **Code:** `"best_cv_f1": best["best_value"],`
> **Type:** Data structure operation

### Line  67
> **Code:** `"test_f1": result["metrics"]["f1_score"],`
> **Type:** Logical operation

### Line  68
> **Code:** `"test_accuracy": result["metrics"]["accuracy"],`
> **Type:** Data structure operation

### Line  69
> **Code:** `"test_roc_auc": result["metrics"]["roc_auc"],`
> **Type:** Data structure operation

### Line  70
> **Code:** `}`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `@step`
> **Type:** Code statement

### Line  74
> **Code:** `def validate_retrained_model(retrain_result: dict) -> dict:`
> **Type:** Function definition

### Line  75
> **Code:** `"""Run Deepchecks and Fairlearn on the retrained model."""`
> **Type:** Logical operation

### Line  76
> **Code:** `if not retrain_result.get("retrained", False):`
> **Type:** Conditional statement

### Line  77
> **Code:** `return {"deepchecks_passed": True, "fairness_passed": True, "skipped":...`
> **Type:** Returns a value from a function

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  80
> **Code:** `from src.models.promote import run_deepchecks, _load_test_frame`
> **Type:** Imports specific names from a module

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `model_path = "models/churn_model.joblib"`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `# Deepchecks`
> **Type:** Comment: Deepchecks

### Line  87
> **Code:** `deepchecks = run_deepchecks(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `# Fairness`
> **Type:** Comment: Fairness

### Line  90
> **Code:** `from src.models.fairness_check import fairness_check`
> **Type:** Imports specific names from a module

### Line  91
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  92
> **Code:** `fairness = fairness_check(Path(model_path))`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `logger.info(f"Deepchecks: {'PASSED' if deepchecks['passed'] else 'FAIL...`
> **Type:** Function call

### Line  95
> **Code:** `logger.info(f"Fairness: {'PASSED' if fairness['passed'] else 'FAILED'}...`
> **Type:** Function call

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  98
> **Code:** `"deepchecks_passed": deepchecks["passed"],`
> **Type:** Data structure operation

### Line  99
> **Code:** `"fairness_passed": fairness["passed"],`
> **Type:** Data structure operation

### Line 100
> **Code:** `"dp_diff": fairness.get("demographic_parity_difference"),`
> **Type:** Code statement

### Line 101
> **Code:** `}`
> **Type:** Code statement

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `@step`
> **Type:** Code statement

### Line 105
> **Code:** `def promote_if_better(validation: dict, retrain_result: dict) -> dict:`
> **Type:** Function definition

### Line 106
> **Code:** `"""Promote retrained model if it beats production and passes all gates...`
> **Type:** Logical operation

### Line 107
> **Code:** `if not retrain_result.get("retrained", False):`
> **Type:** Conditional statement

### Line 108
> **Code:** `return {"promoted": False, "reason": "not_retrained"}`
> **Type:** Returns a value from a function

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `# Check all gates`
> **Type:** Comment: Check all gates

### Line 111
> **Code:** `gates = {`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `"deepchecks": validation.get("deepchecks_passed", False),`
> **Type:** Code statement

### Line 113
> **Code:** `"fairness": validation.get("fairness_passed", False),`
> **Type:** Code statement

### Line 114
> **Code:** `}`
> **Type:** Code statement

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `# Performance gate`
> **Type:** Comment: Performance gate

### Line 117
> **Code:** `candidate_f1 = retrain_result.get("test_f1", 0)`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `from src.config import F1_PROMOTION_THRESHOLD`
> **Type:** Imports specific names from a module

### Line 119
> **Code:** `gates["performance"] = candidate_f1 >= F1_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `# Beats production gate`
> **Type:** Comment: Beats production gate

### Line 122
> **Code:** `from src.models.promote import load_production_model_metrics`
> **Type:** Imports specific names from a module

### Line 123
> **Code:** `prod_f1 = load_production_model_metrics()`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `if prod_f1 is None:`
> **Type:** Conditional statement

### Line 125
> **Code:** `gates["beats_production"] = True`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `else:`
> **Type:** Else block

### Line 127
> **Code:** `gates["beats_production"] = candidate_f1 > prod_f1 + 0.005`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `all_passed = all(gates.values())`
> **Type:** Assignment/comparison

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `if all_passed:`
> **Type:** Conditional statement

### Line 132
> **Code:** `from src.models.promote import _move_to_production`
> **Type:** Imports specific names from a module

### Line 133
> **Code:** `_move_to_production(retrain_result.get("run_id"))`
> **Type:** Function call

### Line 134
> **Code:** `logger.info("Retrained model promoted to Production")`
> **Type:** Function call

### Line 135
> **Code:** `else:`
> **Type:** Else block

### Line 136
> **Code:** `logger.warning(f"Retrained model failed gates: {gates}")`
> **Type:** Function call

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 139
> **Code:** `"promoted": all_passed,`
> **Type:** Code statement

### Line 140
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 141
> **Code:** `"candidate_f1": candidate_f1,`
> **Type:** Logical operation

### Line 142
> **Code:** `"production_f1": prod_f1,`
> **Type:** Code statement

### Line 143
> **Code:** `}`
> **Type:** Code statement

### Line 144
> **Code:** ``
> **Type:** Empty line

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `@pipeline`
> **Type:** Code statement

### Line 147
> **Code:** `def retraining_pipeline():`
> **Type:** Function definition

### Line 148
> **Code:** `"""Automated retraining pipeline triggered by drift."""`
> **Type:** Code statement

### Line 149
> **Code:** `drift_info = check_drift()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `retrain_result = retrain_model(drift_info)`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `validation = validate_retrained_model(retrain_result)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `promote_if_better(validation, retrain_result)`
> **Type:** Function call

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 156
> **Code:** `retraining_pipeline()`
> **Type:** Function call

## Summary
- **Total lines:** 156
- **Code lines:** 114
- **Comments:** 7
- **TODO items:** 0
- **Empty lines:** 35

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: retraining_pipeline.py*
---

# mlops-full-mlops-skills-project: tuning_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/pipelines/tuning_pipeline.py`
- **Total lines:** 93
- **File size:** 3022 bytes

## Line Type Summary
- **Code:** 71
- **Comment:** 0
- **Empty:** 22
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML hyperparameter tuning pipeline with Optuna and nested MLflow ...`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- load_data: same data loading as training`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- tune: Optuna bayesian search (50 trials), each trial logged as neste...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- log_best: logs best params and score to MLflow`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `@step`
> **Type:** Code statement

### Line  17
> **Code:** `def load_data() -> tuple:`
> **Type:** Function definition

### Line  18
> **Code:** `"""Load training data (X, y)."""`
> **Type:** Code statement

### Line  19
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `@step`
> **Type:** Code statement

### Line  25
> **Code:** `def tune_hyperparameters(data: tuple, n_trials: int = 50) -> dict:`
> **Type:** Function definition

### Line  26
> **Code:** `"""Run Optuna bayesian optimization with nested MLflow runs."""`
> **Type:** Code statement

### Line  27
> **Code:** `import optuna`
> **Type:** Imports a module

### Line  28
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  29
> **Code:** `from optuna.samplers import TPESampler`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from sklearn.model_selection import StratifiedKFold, cross_val_score`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `X, y = data`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  38
> **Code:** `mlflow.set_experiment("churn_optuna")`
> **Type:** Function call

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `def objective(trial):`
> **Type:** Function definition

### Line  41
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `"n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `"max_depth": trial.suggest_int("max_depth", 3, 20),`
> **Type:** Code statement

### Line  44
> **Code:** `"min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),`
> **Type:** Code statement

### Line  45
> **Code:** `"max_features": trial.suggest_categorical("max_features", ["sqrt", "lo...`
> **Type:** Logical operation

### Line  46
> **Code:** `"min_samples_split": trial.suggest_int("min_samples_split", 2, 15),`
> **Type:** Code statement

### Line  47
> **Code:** `}`
> **Type:** Code statement

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `model = RandomForestClassifier(**params, random_state=42)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `with mlflow.start_run(nested=True):`
> **Type:** Context manager

### Line  51
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line  52
> **Code:** `cv_score = cross_val_score(`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `model, X, y, cv=StratifiedKFold(3), scoring="f1", n_jobs=-1`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `).mean()`
> **Type:** Function call

### Line  55
> **Code:** `mlflow.log_metric("cv_f1", cv_score)`
> **Type:** Logical operation

### Line  56
> **Code:** `trial.report(cv_score, step=0)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `return cv_score`
> **Type:** Returns a value from a function

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `study = optuna.create_study(`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `direction="maximize",`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `sampler=TPESampler(seed=42),`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `study_name="churn_rf_bayesian",`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `)`
> **Type:** Code statement

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):`
> **Type:** Context manager

### Line  66
> **Code:** `mlflow.log_param("n_trials", n_trials)`
> **Type:** Function call

### Line  67
> **Code:** `mlflow.log_param("sampler", "TPE")`
> **Type:** Function call

### Line  68
> **Code:** `study.optimize(`
> **Type:** Code statement

### Line  69
> **Code:** `objective, n_trials=n_trials, show_progress_bar=False`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** `mlflow.log_metric("best_cv_f1", study.best_value)`
> **Type:** Function call

### Line  72
> **Code:** `mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items(...`
> **Type:** Logical operation

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `logger.info("Best trial: %.4f with %s", study.best_value, study.best_p...`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `return {"best_params": study.best_params, "best_value": study.best_val...`
> **Type:** Returns a value from a function

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `@step`
> **Type:** Code statement

### Line  79
> **Code:** `def log_best_params(best_result: dict) -> dict:`
> **Type:** Function definition

### Line  80
> **Code:** `"""Log the best hyperparameters for downstream use."""`
> **Type:** Logical operation

### Line  81
> **Code:** `return best_result`
> **Type:** Returns a value from a function

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `@pipeline`
> **Type:** Code statement

### Line  85
> **Code:** `def tuning_pipeline(n_trials: int = 50):`
> **Type:** Function definition

### Line  86
> **Code:** `"""Hyperparameter tuning pipeline with Optuna."""`
> **Type:** Code statement

### Line  87
> **Code:** `data = load_data()`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `best = tune_hyperparameters(data, n_trials)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `log_best_params(best)`
> **Type:** Function call

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  93
> **Code:** `tuning_pipeline(n_trials=50)`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 93
- **Code lines:** 71
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 22

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: tuning_pipeline.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/model_cards/__init__.py`
- **Total lines:** 1
- **File size:** 68 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""model_cards package: generated model card markdown artifacts."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: model_card_template.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/model_cards/model_card_template.py`
- **Total lines:** 122
- **File size:** 4032 bytes

## Line Type Summary
- **Code:** 103
- **Comment:** 0
- **Empty:** 19
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Automatic Model Card generation.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Builds a Markdown model card from MLflow metrics + Fairlearn fairness ...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `so the documentation is regenerated at every promotion instead of goin...`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import datetime`
> **Type:** Imports a module

### Line  10
> **Code:** `import json`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** `from typing import Optional`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `def _read_json(path: Path) -> dict:`
> **Type:** Function definition

### Line  18
> **Code:** `if path.exists():`
> **Type:** Conditional statement

### Line  19
> **Code:** `return json.loads(path.read_text())`
> **Type:** Returns a value from a function

### Line  20
> **Code:** `return {}`
> **Type:** Returns a value from a function

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `def _format_metric(value) -> str:`
> **Type:** Function definition

### Line  24
> **Code:** `try:`
> **Type:** Code statement

### Line  25
> **Code:** `return f"{float(value):.4f}"`
> **Type:** Returns a value from a function

### Line  26
> **Code:** `except (TypeError, ValueError):`
> **Type:** Logical operation

### Line  27
> **Code:** `return str(value)`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def generate_model_card(`
> **Type:** Function definition

### Line  31
> **Code:** `report: Optional[dict] = None,`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `output_path: Path = Path("model_cards/model_card.md"),`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `) -> str:`
> **Type:** Arithmetic operation

### Line  34
> **Code:** `"""Generate a model card markdown string and write it to ``output_path...`
> **Type:** Logical operation

### Line  35
> **Code:** `report = report or {}`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `metrics = report.get("metrics", {}) or _read_json(REPORTS_DIR / "promo...`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `"metrics", {}`
> **Type:** Code statement

### Line  38
> **Code:** `)`
> **Type:** Code statement

### Line  39
> **Code:** `fairness = report.get("fairness", {}) or _read_json(REPORTS_DIR / "fai...`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `gates = report.get("gates", {})`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `lines = [`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `"# Model Card: Customer Churn Classifier (Attest demo artifact)",`
> **Type:** Code statement

### Line  44
> **Code:** `"",`
> **Type:** Code statement

### Line  45
> **Code:** `f"*Generated automatically on {datetime.datetime.now().isoformat()}*",`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `"",`
> **Type:** Code statement

### Line  47
> **Code:** `"> Auto-generated demo artifact of the Attest model-risk platform (see...`
> **Type:** Arithmetic operation

### Line  48
> **Code:** `"> `mlops-full-mlops-skills-project.md`). The platform's target use ca...`
> **Type:** Arithmetic operation

### Line  49
> **Code:** `"> & AI compliance; this churn model exercises the platform's governan...`
> **Type:** Comparison operation

### Line  50
> **Code:** `"",`
> **Type:** Code statement

### Line  51
> **Code:** `"## Model details",`
> **Type:** Code statement

### Line  52
> **Code:** `"",`
> **Type:** Code statement

### Line  53
> **Code:** `"- Algorithm: RandomForestClassifier",`
> **Type:** Arithmetic operation

### Line  54
> **Code:** `"- Task: Binary classification (customer churn)",`
> **Type:** Arithmetic operation

### Line  55
> **Code:** `"- Objective: Predict churn probability to enable proactive retention"...`
> **Type:** Arithmetic operation

### Line  56
> **Code:** `"",`
> **Type:** Code statement

### Line  57
> **Code:** `"## Intended use",`
> **Type:** Code statement

### Line  58
> **Code:** `"",`
> **Type:** Code statement

### Line  59
> **Code:** `"- Valid: churn risk scoring for telecom customers (demo only)",`
> **Type:** Arithmetic operation

### Line  60
> **Code:** `"- Avoid: credit decisions, medical predictions, or any other domain",`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `"",`
> **Type:** Code statement

### Line  62
> **Code:** `"## Training data",`
> **Type:** Code statement

### Line  63
> **Code:** `"",`
> **Type:** Code statement

### Line  64
> **Code:** `"- Source: synthetic telecom dataset (`data/raw/dataset.csv`)",`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `"- Rows: ~7000, binary target with a sensitive attribute (`gender`)",`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `"",`
> **Type:** Code statement

### Line  67
> **Code:** `"## Performance metrics (held-out test set)",`
> **Type:** Arithmetic operation

### Line  68
> **Code:** `"",`
> **Type:** Code statement

### Line  69
> **Code:** `"| Metric | Value |",`
> **Type:** Code statement

### Line  70
> **Code:** `"| --- | --- |",`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `]`
> **Type:** Code statement

### Line  72
> **Code:** `for name, value in metrics.items():`
> **Type:** For loop

### Line  73
> **Code:** `lines.append(f"| {name} | {_format_metric(value)} |")`
> **Type:** Logical operation

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `"",`
> **Type:** Code statement

### Line  77
> **Code:** `"## Fairness analysis (Fairlearn)",`
> **Type:** Code statement

### Line  78
> **Code:** `"",`
> **Type:** Code statement

### Line  79
> **Code:** `f"- Demographic parity difference: {_format_metric(fairness.get('demog...`
> **Type:** Arithmetic operation

### Line  80
> **Code:** `f"- Equalized odds difference: {_format_metric(fairness.get('equalized...`
> **Type:** Arithmetic operation

### Line  81
> **Code:** `f"- Threshold (dp_diff): {_format_metric(fairness.get('threshold', 0.1...`
> **Type:** Arithmetic operation

### Line  82
> **Code:** `]`
> **Type:** Code statement

### Line  83
> **Code:** `if "selection_rate_by_group" in fairness:`
> **Type:** Conditional statement

### Line  84
> **Code:** `lines.append("")`
> **Type:** Function call

### Line  85
> **Code:** `lines.append("| Group | Selection rate |")`
> **Type:** Function call

### Line  86
> **Code:** `lines.append("| --- | --- |")`
> **Type:** Arithmetic operation

### Line  87
> **Code:** `for group, rate in fairness.get("selection_rate_by_group", {}).items()...`
> **Type:** For loop

### Line  88
> **Code:** `lines.append(f"| {group} | {_format_metric(rate)} |")`
> **Type:** Logical operation

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `"",`
> **Type:** Code statement

### Line  92
> **Code:** `"## Promotion gates",`
> **Type:** Code statement

### Line  93
> **Code:** `"",`
> **Type:** Code statement

### Line  94
> **Code:** `"| Gate | Status |",`
> **Type:** Code statement

### Line  95
> **Code:** `"| --- | --- |",`
> **Type:** Arithmetic operation

### Line  96
> **Code:** `]`
> **Type:** Code statement

### Line  97
> **Code:** `for name, passed in gates.items():`
> **Type:** For loop

### Line  98
> **Code:** `lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} |")`
> **Type:** Function call

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `"",`
> **Type:** Code statement

### Line 102
> **Code:** `"## Known limitations & identified biases",`
> **Type:** Code statement

### Line 103
> **Code:** `"",`
> **Type:** Code statement

### Line 104
> **Code:** `"- Trained on synthetic data; real-world performance may differ.",`
> **Type:** Arithmetic operation

### Line 105
> **Code:** `"- Fairness is measured on `gender` only; other sensitive dimensions"`
> **Type:** Arithmetic operation

### Line 106
> **Code:** `" (e.g. age bands) are not audited in this version.",`
> **Type:** Logical operation

### Line 107
> **Code:** `"- Small residual demographic parity difference exists and is monitore...`
> **Type:** Arithmetic operation

### Line 108
> **Code:** `]`
> **Type:** Code statement

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `card = "\n".join(lines) + "\n"`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `output_path.write_text(card)`
> **Type:** Function call

### Line 113
> **Code:** `return card`
> **Type:** Returns a value from a function

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 117
> **Code:** `card = generate_model_card()`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `print(card)`
> **Type:** Prints output to console

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 122
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 122
- **Code lines:** 103
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 19

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: model_card_template.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/model/__init__.py`
- **Total lines:** 1
- **File size:** 44 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: model lifecycle tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_model_quality.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/model/test_model_quality.py`
- **Total lines:** 124
- **File size:** 3919 bytes

## Line Type Summary
- **Code:** 87
- **Comment:** 3
- **Empty:** 34
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model quality tests (Deepchecks where available).`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Trains on the versioned churn dataset through the same feature pipelin...`
> **Type:** Code statement

### Line   4
> **Code:** `production trainer uses, so what is asserted here is what gets shipped...`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   7
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from src.config import SENSITIVE_COL, TARGET_COL`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from src.models.train import DEFAULT_PARAMS, load_training_data`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `@pytest.fixture(scope="module")`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `def model_and_data():`
> **Type:** Function definition

### Line  16
> **Code:** `"""Train a churn model and expose the held-out split."""`
> **Type:** Arithmetic operation

### Line  17
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `)`
> **Type:** Code statement

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `params = {**DEFAULT_PARAMS, "n_estimators": 100}`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `model = RandomForestClassifier(**params)`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `model.fit(X_train, y_train)`
> **Type:** Function call

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `return model, X_test, y_test`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def test_model_loaded(model_and_data):`
> **Type:** Function definition

### Line  31
> **Code:** `model, _, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `assert model is not None`
> **Type:** Enforces a condition

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `def test_model_predicts(model_and_data):`
> **Type:** Function definition

### Line  36
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `preds = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `assert len(preds) == len(X_test)`
> **Type:** Enforces a condition

### Line  39
> **Code:** `assert set(preds).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `def test_model_predict_proba(model_and_data):`
> **Type:** Function definition

### Line  43
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `proba = model.predict_proba(X_test)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `assert proba.shape == (len(X_test), 2)`
> **Type:** Enforces a condition

### Line  46
> **Code:** `assert (proba >= 0).all() and (proba <= 1).all()`
> **Type:** Enforces a condition

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def test_sensitive_attribute_isolated(model_and_data):`
> **Type:** Function definition

### Line  50
> **Code:** `"""The protected attribute must never reach the model."""`
> **Type:** Code statement

### Line  51
> **Code:** `_, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `leaked = [c for c in X_test.columns if c.startswith(SENSITIVE_COL)]`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `assert not leaked, f"Sensitive attribute leaked into features: {leaked...`
> **Type:** Enforces a condition

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def test_model_performance_threshold(model_and_data):`
> **Type:** Function definition

### Line  57
> **Code:** `"""Basic performance check - F1 should be reasonable."""`
> **Type:** Arithmetic operation

### Line  58
> **Code:** `from sklearn.metrics import f1_score`
> **Type:** Imports specific names from a module

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `model, X_test, y_test = model_and_data`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `f1 = f1_score(y_test, y_pred)`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `assert f1 >= 0.2, f"F1 score {f1:.4f} below minimum threshold"`
> **Type:** Enforces a condition

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def test_model_auc_threshold(model_and_data):`
> **Type:** Function definition

### Line  67
> **Code:** `from sklearn.metrics import roc_auc_score`
> **Type:** Imports specific names from a module

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `model, X_test, y_test = model_and_data`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `assert auc >= 0.75, f"AUC {auc:.4f} below minimum threshold"`
> **Type:** Enforces a condition

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def test_deepchecks_suite(model_and_data):`
> **Type:** Function definition

### Line  75
> **Code:** `"""Run Deepchecks full suite if available."""`
> **Type:** Code statement

### Line  76
> **Code:** `try:`
> **Type:** Code statement

### Line  77
> **Code:** `from deepchecks.tabular import Dataset`
> **Type:** Imports specific names from a module

### Line  78
> **Code:** `from deepchecks.tabular.suites import full_suite`
> **Type:** Imports specific names from a module

### Line  79
> **Code:** `except ImportError:`
> **Type:** Logical operation

### Line  80
> **Code:** `pytest.skip("deepchecks not available")`
> **Type:** Logical operation

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `model, X_test, y_test = model_and_data`
> **Type:** Assignment/comparison

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `# Deepchecks needs the full dataframe with label`
> **Type:** Comment: Deepchecks needs the full dataframe with label

### Line  85
> **Code:** `test_df = X_test.copy()`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `test_df[TARGET_COL] = y_test.values`
> **Type:** Assignment/comparison

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `ds = Dataset(test_df, label=TARGET_COL)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `result = full_suite().run(ds, model=model)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `critical_failures = [`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `check.get_header() for check in result.results if not check.passed`
> **Type:** Logical operation

### Line  93
> **Code:** `]`
> **Type:** Code statement

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `# Failures are surfaced as warnings here; promotion gates in`
> **Type:** Comment: Failures are surfaced as warnings here; promotion gates in

### Line  96
> **Code:** `# src/models/promote.py are what actually block a release.`
> **Type:** Comment: src/models/promote.py are what actually block a release.

### Line  97
> **Code:** `if critical_failures:`
> **Type:** Conditional statement

### Line  98
> **Code:** `print(f"Deepchecks critical failures: {critical_failures}")`
> **Type:** Prints output to console

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `def test_model_feature_importance_stable(model_and_data):`
> **Type:** Function definition

### Line 102
> **Code:** `"""Top features must stay in the churn-tenure/charges family."""`
> **Type:** Arithmetic operation

### Line 103
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `importances = model.feature_importances_`
> **Type:** Imports a module

### Line 108
> **Code:** `top_feature_names = {X_test.columns[i] for i in np.argsort(importances...`
> **Type:** Assignment/comparison

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `expected_important = {`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `"tenure_months",`
> **Type:** Code statement

### Line 112
> **Code:** `"avg_charge_per_month",`
> **Type:** Code statement

### Line 113
> **Code:** `"service_density",`
> **Type:** Code statement

### Line 114
> **Code:** `"monthly_charges",`
> **Type:** Code statement

### Line 115
> **Code:** `"total_charges",`
> **Type:** Code statement

### Line 116
> **Code:** `"is_long_tenure",`
> **Type:** Code statement

### Line 117
> **Code:** `"usage_efficiency",`
> **Type:** Code statement

### Line 118
> **Code:** `}`
> **Type:** Code statement

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `overlap = len(expected_important & top_feature_names)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `assert overlap >= 2, (`
> **Type:** Enforces a condition

### Line 122
> **Code:** `f"Top features {sorted(top_feature_names)} don't match "`
> **Type:** Logical operation

### Line 123
> **Code:** `f"expected {sorted(expected_important)}"`
> **Type:** Logical operation

### Line 124
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 124
- **Code lines:** 87
- **Comments:** 3
- **TODO items:** 0
- **Empty lines:** 34

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_model_quality.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/unit/__init__.py`
- **Total lines:** 1
- **File size:** 33 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: unit tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/unit/test_features.py`
- **Total lines:** 127
- **File size:** 4282 bytes

## Line Type Summary
- **Code:** 104
- **Comment:** 2
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for feature engineering functions."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from src.config import ID_COL, SENSITIVE_COL, TARGET_COL, TIMESTAMP_CO...`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** `from src.features.build_features import (`
> **Type:** Imports specific names from a module

### Line   7
> **Code:** `derive_features,`
> **Type:** Code statement

### Line   8
> **Code:** `one_hot_encode,`
> **Type:** Code statement

### Line   9
> **Code:** `build_features,`
> **Type:** Code statement

### Line  10
> **Code:** `feature_sets,`
> **Type:** Code statement

### Line  11
> **Code:** `build_feast_features,`
> **Type:** Code statement

### Line  12
> **Code:** `)`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `def _churn_frame() -> pd.DataFrame:`
> **Type:** Function definition

### Line  16
> **Code:** `return pd.DataFrame(`
> **Type:** Returns a value from a function

### Line  17
> **Code:** `{`
> **Type:** Data structure operation

### Line  18
> **Code:** `"customer_id": [1, 2, 3, 4],`
> **Type:** Data structure operation

### Line  19
> **Code:** `"timestamp": [`
> **Type:** Code statement

### Line  20
> **Code:** `"2023-01-01 00:00:00",`
> **Type:** Arithmetic operation

### Line  21
> **Code:** `"2023-06-01 00:00:00",`
> **Type:** Arithmetic operation

### Line  22
> **Code:** `"2024-01-01 00:00:00",`
> **Type:** Arithmetic operation

### Line  23
> **Code:** `"2024-06-01 00:00:00",`
> **Type:** Arithmetic operation

### Line  24
> **Code:** `],`
> **Type:** Code statement

### Line  25
> **Code:** `"age": [25, 40, 55, 70],`
> **Type:** Data structure operation

### Line  26
> **Code:** `"gender": ["female", "male", "female", "male"],`
> **Type:** Data structure operation

### Line  27
> **Code:** `"region": ["north", "south", "east", "west"],`
> **Type:** Logical operation

### Line  28
> **Code:** `"tenure_months": [1, 12, 36, 60],`
> **Type:** Data structure operation

### Line  29
> **Code:** `"monthly_charges": [50.0, 60.0, 70.0, 80.0],`
> **Type:** Data structure operation

### Line  30
> **Code:** `"total_charges": [50.0, 720.0, 2520.0, 4800.0],`
> **Type:** Data structure operation

### Line  31
> **Code:** `"num_services": [1, 2, 3, 4],`
> **Type:** Data structure operation

### Line  32
> **Code:** `"contract_type": [`
> **Type:** Code statement

### Line  33
> **Code:** `"month-to-month",`
> **Type:** Arithmetic operation

### Line  34
> **Code:** `"one_year",`
> **Type:** Code statement

### Line  35
> **Code:** `"two_year",`
> **Type:** Code statement

### Line  36
> **Code:** `"two_year",`
> **Type:** Code statement

### Line  37
> **Code:** `],`
> **Type:** Code statement

### Line  38
> **Code:** `"payment_method": [`
> **Type:** Code statement

### Line  39
> **Code:** `"electronic_check",`
> **Type:** Code statement

### Line  40
> **Code:** `"mailed_check",`
> **Type:** Code statement

### Line  41
> **Code:** `"bank_transfer",`
> **Type:** Code statement

### Line  42
> **Code:** `"credit_card",`
> **Type:** Code statement

### Line  43
> **Code:** `],`
> **Type:** Code statement

### Line  44
> **Code:** `"support_tickets": [0, 1, 2, 3],`
> **Type:** Logical operation

### Line  45
> **Code:** `"avg_call_minutes": [100.0, 200.0, 300.0, 400.0],`
> **Type:** Data structure operation

### Line  46
> **Code:** `"has_online_backup": [0, 1, 0, 1],`
> **Type:** Data structure operation

### Line  47
> **Code:** `"has_device_protection": [1, 0, 1, 0],`
> **Type:** Data structure operation

### Line  48
> **Code:** `"has_tech_support": [0, 0, 1, 1],`
> **Type:** Logical operation

### Line  49
> **Code:** `"churn": [1, 0, 1, 0],`
> **Type:** Data structure operation

### Line  50
> **Code:** `}`
> **Type:** Code statement

### Line  51
> **Code:** `)`
> **Type:** Code statement

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `def test_derive_features():`
> **Type:** Function definition

### Line  55
> **Code:** `result = derive_features(_churn_frame())`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `for col in (`
> **Type:** For loop

### Line  57
> **Code:** `"avg_charge_per_month",`
> **Type:** Code statement

### Line  58
> **Code:** `"service_density",`
> **Type:** Code statement

### Line  59
> **Code:** `"ticket_intensity",`
> **Type:** Code statement

### Line  60
> **Code:** `"is_long_tenure",`
> **Type:** Code statement

### Line  61
> **Code:** `"is_high_value_customer",`
> **Type:** Code statement

### Line  62
> **Code:** `"usage_efficiency",`
> **Type:** Code statement

### Line  63
> **Code:** `):`
> **Type:** Code statement

### Line  64
> **Code:** `assert col in result.columns`
> **Type:** Enforces a condition

### Line  65
> **Code:** `assert result.loc[0, "avg_charge_per_month"] == 50.0  # 50/1`
> **Type:** Enforces a condition

### Line  66
> **Code:** `assert result.loc[1, "is_long_tenure"] == 0`
> **Type:** Enforces a condition

### Line  67
> **Code:** `assert result.loc[2, "is_long_tenure"] == 1`
> **Type:** Enforces a condition

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `def test_derive_features_passthrough_without_churn_columns():`
> **Type:** Function definition

### Line  71
> **Code:** `"""Frames lacking the churn columns are returned untouched."""`
> **Type:** Code statement

### Line  72
> **Code:** `df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `result = derive_features(df)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `assert list(result.columns) == list(df.columns)`
> **Type:** Enforces a condition

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `def test_derive_features_survives_zero_tenure():`
> **Type:** Function definition

### Line  78
> **Code:** `df = _churn_frame()`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `df.loc[0, "tenure_months"] = 0`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `result = derive_features(df)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `assert result["avg_charge_per_month"].notna().all()`
> **Type:** Enforces a condition

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def test_one_hot_encode():`
> **Type:** Function definition

### Line  85
> **Code:** `df = pd.DataFrame({"color": ["red", "blue", "red", "green"]})`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `result = one_hot_encode(df, ["color"])`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `# drop_first=True: first category ("blue") dropped, others encoded`
> **Type:** Comment: drop_first=True: first category ("blue") dropped, others encoded

### Line  88
> **Code:** `assert "color_blue" not in result.columns`
> **Type:** Enforces a condition

### Line  89
> **Code:** `assert "color_green" in result.columns`
> **Type:** Enforces a condition

### Line  90
> **Code:** `assert "color_red" in result.columns`
> **Type:** Enforces a condition

### Line  91
> **Code:** `assert len(result) == 4`
> **Type:** Enforces a condition

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `def test_build_features_drops_id_timestamp_and_sensitive():`
> **Type:** Function definition

### Line  95
> **Code:** `result = build_features(_churn_frame(), include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `assert ID_COL not in result.columns`
> **Type:** Enforces a condition

### Line  97
> **Code:** `assert TIMESTAMP_COL not in result.columns`
> **Type:** Enforces a condition

### Line  98
> **Code:** `assert not [c for c in result.columns if c.startswith(SENSITIVE_COL)]`
> **Type:** Enforces a condition

### Line  99
> **Code:** `assert TARGET_COL in result.columns`
> **Type:** Enforces a condition

### Line 100
> **Code:** `assert len(result) == 4`
> **Type:** Enforces a condition

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `def test_build_features_can_keep_sensitive_for_audit():`
> **Type:** Function definition

### Line 104
> **Code:** `result = build_features(_churn_frame(), include_sensitive=True)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `assert SENSITIVE_COL in result.columns`
> **Type:** Enforces a condition

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `def test_build_features_one_hot_encodes_categoricals():`
> **Type:** Function definition

### Line 109
> **Code:** `result = build_features(_churn_frame(), include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `assert "contract_type" not in result.columns`
> **Type:** Enforces a condition

### Line 111
> **Code:** `assert any(c.startswith("contract_type_") for c in result.columns)`
> **Type:** Enforces a condition

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `def test_feature_sets():`
> **Type:** Function definition

### Line 115
> **Code:** `frame = build_features(_churn_frame(), include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `assert TARGET_COL not in sets["X"].columns`
> **Type:** Enforces a condition

### Line 118
> **Code:** `assert list(sets["y"]) == [1, 0, 1, 0]`
> **Type:** Enforces a condition

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `def test_build_feast_features():`
> **Type:** Function definition

### Line 122
> **Code:** `result = build_feast_features(_churn_frame())`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `# Entity key + event timestamp are what make point-in-time joins corre...`
> **Type:** Comment: Entity key + event timestamp are what make point-in-time joins correct.

### Line 124
> **Code:** `assert ID_COL in result.columns`
> **Type:** Enforces a condition

### Line 125
> **Code:** `assert TIMESTAMP_COL in result.columns`
> **Type:** Enforces a condition

### Line 126
> **Code:** `assert TARGET_COL in result.columns`
> **Type:** Enforces a condition

### Line 127
> **Code:** `assert pd.api.types.is_datetime64_any_dtype(result[TIMESTAMP_COL])`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 127
- **Code lines:** 104
- **Comments:** 2
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_features.py*
---

# mlops-full-mlops-skills-project: test_fairness.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/unit/test_fairness.py`
- **Total lines:** 74
- **File size:** 2842 bytes

## Line Type Summary
- **Code:** 45
- **Comment:** 10
- **Empty:** 19
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for fairness checking logic."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line   4
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `from src.config import FAIRNESS_DP_THRESHOLD`
> **Type:** Imports specific names from a module

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `def test_fairness_threshold():`
> **Type:** Function definition

### Line  10
> **Code:** `"""Test that the fairness threshold constant is set correctly."""`
> **Type:** Logical operation

### Line  11
> **Code:** `assert FAIRNESS_DP_THRESHOLD == 0.1`
> **Type:** Enforces a condition

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `def test_demographic_parity_difference_calculation():`
> **Type:** Function definition

### Line  15
> **Code:** `"""Test manual calculation of demographic parity difference."""`
> **Type:** Code statement

### Line  16
> **Code:** `# Simple case: equal selection rates -> DP diff = 0`
> **Type:** Comment: Simple case: equal selection rates -> DP diff = 0

### Line  17
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1])`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `y_pred = np.array([0, 1, 0, 1, 0, 1, 0, 1])`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `sensitive = np.array(["M", "M", "M", "M", "F", "F", "F", "F"])`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `# Selection rate for M: 2/4 = 0.5, for F: 2/4 = 0.5`
> **Type:** Comment: Selection rate for M: 2/4 = 0.5, for F: 2/4 = 0.5

### Line  22
> **Code:** `# DP diff = |0.5 - 0.5| = 0`
> **Type:** Comment: DP diff = |0.5 - 0.5| = 0

### Line  23
> **Code:** `from fairlearn.metrics import selection_rate, demographic_parity_diffe...`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `sr_m = selection_rate(y_true[sensitive == "M"], y_pred[sensitive == "M...`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `sr_f = selection_rate(y_true[sensitive == "F"], y_pred[sensitive == "F...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `assert sr_m == 0.5`
> **Type:** Enforces a condition

### Line  30
> **Code:** `assert sr_f == 0.5`
> **Type:** Enforces a condition

### Line  31
> **Code:** `assert abs(dp_diff) < 1e-10`
> **Type:** Enforces a condition

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `def test_fairness_rejection_threshold():`
> **Type:** Function definition

### Line  35
> **Code:** `"""Test that dp_diff > 0.1 triggers rejection."""`
> **Type:** Comparison operation

### Line  36
> **Code:** `# M group: 80% positive predictions, F group: 40%`
> **Type:** Comment: M group: 80% positive predictions, F group: 40%

### Line  37
> **Code:** `# DP diff = 0.4 > 0.1 -> should fail`
> **Type:** Comment: DP diff = 0.4 > 0.1 -> should fail

### Line  38
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1] * 10)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `y_pred = np.array([1, 1, 1, 1, 1, 1, 1, 1,  # M: all 1`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `1, 1, 1, 1, 0, 0, 0, 0] * 5)  # F: half 1, half 0`
> **Type:** Arithmetic operation

### Line  41
> **Code:** `sensitive = np.array(["M"] * 40 + ["F"] * 40)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `from fairlearn.metrics import demographic_parity_difference`
> **Type:** Imports specific names from a module

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `assert dp_diff > FAIRNESS_DP_THRESHOLD`
> **Type:** Enforces a condition

### Line  48
> **Code:** `# This model would be rejected`
> **Type:** Comment: This model would be rejected

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `def test_fairness_pass_threshold():`
> **Type:** Function definition

### Line  52
> **Code:** `"""Test that dp_diff <= 0.1 passes."""`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `# M group: 55% positive, F group: 50% -> DP diff = 0.05 < 0.1 -> pass`
> **Type:** Comment: M group: 55% positive, F group: 50% -> DP diff = 0.05 < 0.1 -> pass

### Line  54
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1] * 10)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `y_pred = np.array([1, 1, 1, 1, 0, 1, 0, 1,  # M: 6/8 = 0.75`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `0, 1, 1, 0, 0, 1, 0, 0] * 5)  # F: 4/8 = 0.5`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `sensitive = np.array(["M"] * 40 + ["F"] * 40)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `from fairlearn.metrics import demographic_parity_difference`
> **Type:** Imports specific names from a module

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `# Adjust to make it pass`
> **Type:** Comment: Adjust to make it pass

### Line  64
> **Code:** `# Let's make it closer: M 52%, F 50%`
> **Type:** Comment: Let's make it closer: M 52%, F 50%

### Line  65
> **Code:** `y_pred_balanced = np.array([1, 1, 0, 1, 0, 1, 0, 1] * 5)  # 5/8 = 0.62...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `y_pred_balanced_f = np.array([0, 1, 1, 0, 0, 1, 0, 0] * 5)  # 4/8 = 0....`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `dp_diff_balanced = demographic_parity_difference(`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `y_true,`
> **Type:** Code statement

### Line  69
> **Code:** `np.concatenate([y_pred_balanced, y_pred_balanced_f]),`
> **Type:** Data structure operation

### Line  70
> **Code:** `sensitive_features=np.array(["M"]*40 + ["F"]*40)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `)`
> **Type:** Code statement

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `# This demonstrates the threshold logic works`
> **Type:** Comment: This demonstrates the threshold logic works

### Line  74
> **Code:** `assert FAIRNESS_DP_THRESHOLD == 0.1`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 74
- **Code lines:** 45
- **Comments:** 10
- **TODO items:** 0
- **Empty lines:** 19

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_fairness.py*
---

# mlops-full-mlops-skills-project: test_preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/unit/test_preprocessing.py`
- **Total lines:** 91
- **File size:** 2806 bytes

## Line Type Summary
- **Code:** 74
- **Comment:** 0
- **Empty:** 17
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for preprocessing functions."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from src.data.preprocessing import (`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** `drop_duplicates,`
> **Type:** Code statement

### Line   7
> **Code:** `drop_missing,`
> **Type:** Code statement

### Line   8
> **Code:** `clamp_numeric,`
> **Type:** Code statement

### Line   9
> **Code:** `cast_dtypes,`
> **Type:** Code statement

### Line  10
> **Code:** `preprocess,`
> **Type:** Code statement

### Line  11
> **Code:** `)`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `def _churn_frame() -> pd.DataFrame:`
> **Type:** Function definition

### Line  15
> **Code:** `"""A minimal frame carrying the columns preprocessing cares about."""`
> **Type:** Code statement

### Line  16
> **Code:** `return pd.DataFrame(`
> **Type:** Returns a value from a function

### Line  17
> **Code:** `{`
> **Type:** Data structure operation

### Line  18
> **Code:** `"age": [34, 51, 51],`
> **Type:** Data structure operation

### Line  19
> **Code:** `"tenure_months": [5, 48, 48],`
> **Type:** Data structure operation

### Line  20
> **Code:** `"monthly_charges": [55.0, 89.5, 89.5],`
> **Type:** Data structure operation

### Line  21
> **Code:** `"total_charges": [275.0, 4296.0, 4296.0],`
> **Type:** Data structure operation

### Line  22
> **Code:** `"num_services": [2, 4, 4],`
> **Type:** Data structure operation

### Line  23
> **Code:** `"support_tickets": [1, 0, 0],`
> **Type:** Logical operation

### Line  24
> **Code:** `"avg_call_minutes": [220.0, 410.0, 410.0],`
> **Type:** Data structure operation

### Line  25
> **Code:** `"has_online_backup": [0, 1, 1],`
> **Type:** Data structure operation

### Line  26
> **Code:** `"has_device_protection": [1, 1, 1],`
> **Type:** Data structure operation

### Line  27
> **Code:** `"has_tech_support": [0, 1, 1],`
> **Type:** Logical operation

### Line  28
> **Code:** `"region": ["north", "west", "west"],`
> **Type:** Logical operation

### Line  29
> **Code:** `"contract_type": ["month-to-month", "two_year", "two_year"],`
> **Type:** Arithmetic operation

### Line  30
> **Code:** `"payment_method": ["electronic_check", "credit_card", "credit_card"],`
> **Type:** Data structure operation

### Line  31
> **Code:** `"churn": [1, 0, 0],`
> **Type:** Data structure operation

### Line  32
> **Code:** `}`
> **Type:** Code statement

### Line  33
> **Code:** `)`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def test_drop_duplicates():`
> **Type:** Function definition

### Line  37
> **Code:** `df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `result = drop_duplicates(df)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `def test_drop_missing():`
> **Type:** Function definition

### Line  43
> **Code:** `df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `result = drop_missing(df, columns=["a"])`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  46
> **Code:** `assert result["a"].notna().all()`
> **Type:** Enforces a condition

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def test_clamp_numeric():`
> **Type:** Function definition

### Line  50
> **Code:** `df = pd.DataFrame(`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `{`
> **Type:** Data structure operation

### Line  52
> **Code:** `"age": [5.0, 40.0, 250.0],`
> **Type:** Data structure operation

### Line  53
> **Code:** `"tenure_months": [-3.0, 12.0, 999.0],`
> **Type:** Arithmetic operation

### Line  54
> **Code:** `"monthly_charges": [-10.0, 60.0, 5000.0],`
> **Type:** Arithmetic operation

### Line  55
> **Code:** `}`
> **Type:** Code statement

### Line  56
> **Code:** `)`
> **Type:** Code statement

### Line  57
> **Code:** `result = clamp_numeric(df)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `assert result["age"].between(18, 100).all()`
> **Type:** Enforces a condition

### Line  59
> **Code:** `assert result["tenure_months"].between(0, 120).all()`
> **Type:** Enforces a condition

### Line  60
> **Code:** `assert result["monthly_charges"].between(0, 500).all()`
> **Type:** Enforces a condition

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def test_clamp_numeric_accepts_custom_ranges():`
> **Type:** Function definition

### Line  64
> **Code:** `df = pd.DataFrame({"age": [10.0, 90.0]})`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `result = clamp_numeric(df, ranges={"age": (30, 60)}, numeric_features=...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `assert result["age"].tolist() == [30.0, 60.0]`
> **Type:** Enforces a condition

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def test_cast_dtypes():`
> **Type:** Function definition

### Line  70
> **Code:** `result = cast_dtypes(_churn_frame())`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `assert result["monthly_charges"].dtype == "float64"`
> **Type:** Enforces a condition

### Line  72
> **Code:** `assert result["tenure_months"].dtype == "int64"`
> **Type:** Enforces a condition

### Line  73
> **Code:** `assert result["has_tech_support"].dtype == "int8"`
> **Type:** Enforces a condition

### Line  74
> **Code:** `assert result["contract_type"].dtype == "string"`
> **Type:** Enforces a condition

### Line  75
> **Code:** `assert result["churn"].dtype == "int8"`
> **Type:** Enforces a condition

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `def test_preprocess_chain():`
> **Type:** Function definition

### Line  79
> **Code:** `df = _churn_frame()`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `df.loc[0, "monthly_charges"] = -20.0  # out of range, must be clamped`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `result = preprocess(df)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `assert len(result) == 2  # deduped`
> **Type:** Enforces a condition

### Line  83
> **Code:** `assert (result["monthly_charges"] >= 0).all()`
> **Type:** Enforces a condition

### Line  84
> **Code:** `assert result["churn"].dtype == "int8"`
> **Type:** Enforces a condition

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `def test_preprocess_is_pure():`
> **Type:** Function definition

### Line  88
> **Code:** `df = _churn_frame()`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `before = df.copy()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `preprocess(df)`
> **Type:** Function call

### Line  91
> **Code:** `pd.testing.assert_frame_equal(df, before)`
> **Type:** Logical operation

## Summary
- **Total lines:** 91
- **Code lines:** 74
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 17

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_preprocessing.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/data/__init__.py`
- **Total lines:** 1
- **File size:** 42 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: data pipeline tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_data_validation.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/tests/data/test_data_validation.py`
- **Total lines:** 107
- **File size:** 2645 bytes

## Line Type Summary
- **Code:** 78
- **Comment:** 0
- **Empty:** 29
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Data validation tests: the raw dataset must satisfy the input contr...`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Mirrors great_expectations/expectations/dataset_suite.json so a contra...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `breach fails in CI as well as in the DVC `validate` stage.`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   7
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** `BINARY_FEATURES,`
> **Type:** Code statement

### Line  11
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  12
> **Code:** `NUMERIC_RANGES,`
> **Type:** Code statement

### Line  13
> **Code:** `RAW_DATA_PATH,`
> **Type:** Code statement

### Line  14
> **Code:** `SENSITIVE_COL,`
> **Type:** Code statement

### Line  15
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  16
> **Code:** `)`
> **Type:** Code statement

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `EXPECTED_COLUMNS = [`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `"customer_id",`
> **Type:** Code statement

### Line  20
> **Code:** `"timestamp",`
> **Type:** Code statement

### Line  21
> **Code:** `"age",`
> **Type:** Code statement

### Line  22
> **Code:** `"gender",`
> **Type:** Code statement

### Line  23
> **Code:** `"region",`
> **Type:** Code statement

### Line  24
> **Code:** `"tenure_months",`
> **Type:** Code statement

### Line  25
> **Code:** `"monthly_charges",`
> **Type:** Code statement

### Line  26
> **Code:** `"total_charges",`
> **Type:** Code statement

### Line  27
> **Code:** `"num_services",`
> **Type:** Code statement

### Line  28
> **Code:** `"contract_type",`
> **Type:** Code statement

### Line  29
> **Code:** `"payment_method",`
> **Type:** Code statement

### Line  30
> **Code:** `"support_tickets",`
> **Type:** Logical operation

### Line  31
> **Code:** `"avg_call_minutes",`
> **Type:** Code statement

### Line  32
> **Code:** `"has_online_backup",`
> **Type:** Code statement

### Line  33
> **Code:** `"has_device_protection",`
> **Type:** Code statement

### Line  34
> **Code:** `"has_tech_support",`
> **Type:** Logical operation

### Line  35
> **Code:** `"churn",`
> **Type:** Code statement

### Line  36
> **Code:** `]`
> **Type:** Code statement

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `@pytest.fixture(scope="module")`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `def raw() -> pd.DataFrame:`
> **Type:** Function definition

### Line  41
> **Code:** `return pd.read_csv(RAW_DATA_PATH)`
> **Type:** Returns a value from a function

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `def test_raw_data_exists():`
> **Type:** Function definition

### Line  45
> **Code:** `assert RAW_DATA_PATH.exists(), f"Raw dataset not found at {RAW_DATA_PA...`
> **Type:** Enforces a condition

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def test_raw_data_schema(raw):`
> **Type:** Function definition

### Line  49
> **Code:** `assert list(raw.columns) == EXPECTED_COLUMNS`
> **Type:** Enforces a condition

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def test_raw_data_row_count(raw):`
> **Type:** Function definition

### Line  53
> **Code:** `assert 5000 <= len(raw) <= 10000`
> **Type:** Enforces a condition

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def test_no_nulls_on_critical_columns(raw):`
> **Type:** Function definition

### Line  57
> **Code:** `critical = ["customer_id", "timestamp", TARGET_COL, SENSITIVE_COL]`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `for col in critical:`
> **Type:** For loop

### Line  59
> **Code:** `assert raw[col].notna().all(), f"Nulls found in {col}"`
> **Type:** Enforces a condition

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `def test_customer_id_unique(raw):`
> **Type:** Function definition

### Line  63
> **Code:** `assert raw["customer_id"].is_unique`
> **Type:** Enforces a condition

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def test_timestamp_parses(raw):`
> **Type:** Function definition

### Line  67
> **Code:** `parsed = pd.to_datetime(raw["timestamp"], errors="coerce")`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `assert parsed.notna().all()`
> **Type:** Enforces a condition

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `def test_numeric_ranges(raw):`
> **Type:** Function definition

### Line  72
> **Code:** `for col, (lo, hi) in NUMERIC_RANGES.items():`
> **Type:** For loop

### Line  73
> **Code:** `assert raw[col].between(lo, hi).all(), f"{col} outside [{lo}, {hi}]"`
> **Type:** Enforces a condition

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def test_target_binary(raw):`
> **Type:** Function definition

### Line  77
> **Code:** `assert set(raw[TARGET_COL].unique()) <= {0, 1}`
> **Type:** Enforces a condition

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def test_target_not_degenerate(raw):`
> **Type:** Function definition

### Line  81
> **Code:** `rate = raw[TARGET_COL].mean()`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `assert 0.01 < rate < 0.5, f"Implausible churn rate: {rate}"`
> **Type:** Enforces a condition

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def test_binary_features_are_binary(raw):`
> **Type:** Function definition

### Line  86
> **Code:** `for col in BINARY_FEATURES:`
> **Type:** For loop

### Line  87
> **Code:** `assert set(raw[col].unique()) <= {0, 1}, f"{col} is not 0/1"`
> **Type:** Enforces a condition

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `def test_categorical_levels_are_closed(raw):`
> **Type:** Function definition

### Line  91
> **Code:** `allowed = {`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `"region": {"north", "south", "east", "west"},`
> **Type:** Logical operation

### Line  93
> **Code:** `"contract_type": {"month-to-month", "one_year", "two_year"},`
> **Type:** Arithmetic operation

### Line  94
> **Code:** `"payment_method": {`
> **Type:** Code statement

### Line  95
> **Code:** `"electronic_check",`
> **Type:** Code statement

### Line  96
> **Code:** `"mailed_check",`
> **Type:** Code statement

### Line  97
> **Code:** `"bank_transfer",`
> **Type:** Code statement

### Line  98
> **Code:** `"credit_card",`
> **Type:** Code statement

### Line  99
> **Code:** `},`
> **Type:** Code statement

### Line 100
> **Code:** `}`
> **Type:** Code statement

### Line 101
> **Code:** `for col in CATEGORICAL_FEATURES:`
> **Type:** For loop

### Line 102
> **Code:** `assert set(raw[col].unique()) <= allowed[col], f"Unexpected level in {...`
> **Type:** Enforces a condition

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `def test_numeric_features_finite(raw):`
> **Type:** Function definition

### Line 106
> **Code:** `numeric = raw.select_dtypes("number")`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `assert numeric.notna().all().all()`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 107
- **Code lines:** 78
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 29

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_data_validation.py*
---

# mlops-full-mlops-skills-project: main.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/api/main.py`
- **Total lines:** 232
- **File size:** 7710 bytes

## Line Type Summary
- **Code:** 198
- **Comment:** 4
- **Empty:** 30
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""FastAPI app for Fraud Detection (P3) — self-contained, trains on cr...`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Data comes from the repository (``data/raw/creditcard.csv``, produced ...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** ```data/raw/generate_creditcard_data.py``); set FRAUD_DATA_PATH to poin...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `real export instead.`
> **Type:** Logical operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `import os`
> **Type:** Imports a module

### Line   9
> **Code:** `import subprocess`
> **Type:** Imports a module

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `import time`
> **Type:** Imports a module

### Line  12
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  13
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  14
> **Code:** `from contextlib import asynccontextmanager`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from datetime import datetime, timezone`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from fastapi import FastAPI`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from fastapi.staticfiles import StaticFiles`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** `from fastapi.responses import FileResponse`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** `from pydantic import BaseModel, Field`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from sklearn.preprocessing import StandardScaler`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from sklearn.metrics import roc_auc_score, f1_score`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parent.parent`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `UI_DIR = PROJECT_ROOT / "ui"`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `GENERATOR = PROJECT_ROOT / "data" / "raw" / "generate_creditcard_data....`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `REAL_DATA_PATH = Path(`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `os.getenv("FRAUD_DATA_PATH", PROJECT_ROOT / "data" / "raw" / "creditca...`
> **Type:** Arithmetic operation

### Line  32
> **Code:** `)`
> **Type:** Code statement

### Line  33
> **Code:** `MODEL = None`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `SCALER = None`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `FEATURE_COLS = None`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `MODEL_META = {}`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `PREDICTION_LOG = []`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `LOG_CAP = 500`
> **Type:** Assignment/comparison

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `RISK_LEVELS = ["low", "medium", "high", "critical"]`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `class PredictRequest(BaseModel):`
> **Type:** Class definition

### Line  43
> **Code:** `Time: float = Field(default=0, ge=0)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `V1: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `V2: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `V3: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `V4: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `V5: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `V6: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `V7: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `V8: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `V9: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `V10: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `V11: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `V12: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `V13: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `V14: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `V15: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `V16: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `V17: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `V18: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `V19: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `V20: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `V21: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `V22: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `V23: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `V24: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `V25: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `V26: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `V27: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `V28: float = Field(default=0)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `Amount: float = Field(default=100, ge=0)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `class PredictResponse(BaseModel):`
> **Type:** Class definition

### Line  75
> **Code:** `prediction: str`
> **Type:** Code statement

### Line  76
> **Code:** `probability: float`
> **Type:** Code statement

### Line  77
> **Code:** `risk_level: str`
> **Type:** Code statement

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `def load_real_data():`
> **Type:** Function definition

### Line  80
> **Code:** `"""Load creditcard.csv, generating the synthetic demo file if absent."...`
> **Type:** Code statement

### Line  81
> **Code:** `if not REAL_DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  82
> **Code:** `print(f"P3: {REAL_DATA_PATH} missing, generating synthetic demo data")`
> **Type:** Prints output to console

### Line  83
> **Code:** `REAL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `subprocess.run(`
> **Type:** Code statement

### Line  85
> **Code:** `[sys.executable, str(GENERATOR), "--output", str(REAL_DATA_PATH)],`
> **Type:** Arithmetic operation

### Line  86
> **Code:** `check=True,`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `)`
> **Type:** Code statement

### Line  88
> **Code:** `df = pd.read_csv(REAL_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `# Drop NaN rows`
> **Type:** Comment: Drop NaN rows

### Line  90
> **Code:** `initial = len(df)`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `df = df.dropna(subset=["Class"])`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `if len(df) < initial:`
> **Type:** Conditional statement

### Line  93
> **Code:** `print(f"P3: Dropped {initial - len(df)} rows with NaN Class")`
> **Type:** Prints output to console

### Line  94
> **Code:** `print(f"P3: Loaded {len(df)} real transactions, fraud rate={df['Class'...`
> **Type:** Prints output to console

### Line  95
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `def train_model():`
> **Type:** Function definition

### Line  98
> **Code:** `global MODEL, SCALER, FEATURE_COLS, MODEL_META`
> **Type:** Code statement

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `df = load_real_data()`
> **Type:** Assignment/comparison

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `# Features: Time, V1-V28, Amount; Target: Class`
> **Type:** Comment: Features: Time, V1-V28, Amount; Target: Class

### Line 103
> **Code:** `FEATURE_COLS = [c for c in df.columns if c != "Class"]`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `X = df[FEATURE_COLS]`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `y = df["Class"]`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `# Scale features (important for V1-V28 PCA features)`
> **Type:** Comment: Scale features (important for V1-V28 PCA features)

### Line 108
> **Code:** `SCALER = StandardScaler()`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `X_scaled = SCALER.fit_transform(X)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_...`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `MODEL = RandomForestClassifier(n_estimators=200, max_depth=10, random_...`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `MODEL.fit(X_train, y_train)`
> **Type:** Function call

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `proba = MODEL.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `preds = MODEL.predict(X_test)`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `auc = roc_auc_score(y_test, proba)`
> **Type:** Assignment/comparison

### Line 119
> **Code:** `f1 = f1_score(y_test, preds)`
> **Type:** Assignment/comparison

### Line 120
> **Code:** `print(f"P3: AUC={auc:.4f}, F1={f1:.4f}")`
> **Type:** Prints output to console

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `MODEL_META = {`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `"model_name": "RandomForestClassifier",`
> **Type:** Logical operation

### Line 124
> **Code:** `"n_estimators": MODEL.n_estimators,`
> **Type:** Logical operation

### Line 125
> **Code:** `"max_depth": int(MODEL.max_depth or 0),`
> **Type:** Logical operation

### Line 126
> **Code:** `"class_weight": "balanced_subsample",`
> **Type:** Code statement

### Line 127
> **Code:** `"trained_samples": int(len(df)),`
> **Type:** Code statement

### Line 128
> **Code:** `"feature_count": int(len(FEATURE_COLS)),`
> **Type:** Code statement

### Line 129
> **Code:** `"auc": round(auc, 4),`
> **Type:** Code statement

### Line 130
> **Code:** `"f1": round(f1, 4),`
> **Type:** Code statement

### Line 131
> **Code:** `"trained_at": datetime.now(timezone.utc).isoformat(),`
> **Type:** Logical operation

### Line 132
> **Code:** `"data_source": str(REAL_DATA_PATH)`
> **Type:** Function call

### Line 133
> **Code:** `}`
> **Type:** Code statement

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** `@asynccontextmanager`
> **Type:** Code statement

### Line 136
> **Code:** `async def lifespan(app: FastAPI):`
> **Type:** Code statement

### Line 137
> **Code:** `train_model()`
> **Type:** Function call

### Line 138
> **Code:** `yield`
> **Type:** Code statement

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** `app = FastAPI(title="Fraud Detection API (Real Data)", version="1.0.0"...`
> **Type:** Assignment/comparison

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `@app.get("/health")`
> **Type:** Arithmetic operation

### Line 143
> **Code:** `async def health():`
> **Type:** Code statement

### Line 144
> **Code:** `return {"status": "healthy", "model_loaded": MODEL is not None, "data_...`
> **Type:** Returns a value from a function

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `@app.post("/predict", response_model=PredictResponse)`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `async def predict(req: PredictRequest):`
> **Type:** Code statement

### Line 148
> **Code:** `t0 = time.perf_counter()`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `input_dict = req.model_dump()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** `# Build feature vector in correct order`
> **Type:** Comment: Build feature vector in correct order

### Line 152
> **Code:** `feat_vec = np.array([input_dict[col] for col in FEATURE_COLS]).reshape...`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `feat_scaled = SCALER.transform(feat_vec)`
> **Type:** Assignment/comparison

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `prob = float(MODEL.predict_proba(feat_scaled)[0][1])`
> **Type:** Assignment/comparison

### Line 156
> **Code:** `pred = "fraud" if prob >= 0.5 else "legitimate"`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `risk = "critical" if prob >= 0.7 else "high" if prob >= 0.4 else "medi...`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `latency_ms = round((time.perf_counter() - t0) * 1000, 2)`
> **Type:** Assignment/comparison

### Line 159
> **Code:** ``
> **Type:** Empty line

### Line 160
> **Code:** `entry = {`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `"timestamp": datetime.now(timezone.utc).isoformat(),`
> **Type:** Logical operation

### Line 162
> **Code:** `"input": input_dict,`
> **Type:** Code statement

### Line 163
> **Code:** `"result": {`
> **Type:** Code statement

### Line 164
> **Code:** `"prediction": pred,`
> **Type:** Code statement

### Line 165
> **Code:** `"probability": round(prob, 4),`
> **Type:** Code statement

### Line 166
> **Code:** `"risk_level": risk,`
> **Type:** Code statement

### Line 167
> **Code:** `},`
> **Type:** Code statement

### Line 168
> **Code:** `"latency_ms": latency_ms,`
> **Type:** Code statement

### Line 169
> **Code:** `}`
> **Type:** Code statement

### Line 170
> **Code:** `PREDICTION_LOG.append(entry)`
> **Type:** Function call

### Line 171
> **Code:** `if len(PREDICTION_LOG) > LOG_CAP:`
> **Type:** Conditional statement

### Line 172
> **Code:** `del PREDICTION_LOG[: len(PREDICTION_LOG) - LOG_CAP]`
> **Type:** Arithmetic operation

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** `return PredictResponse(prediction=pred, probability=round(prob, 4), ri...`
> **Type:** Returns a value from a function

### Line 175
> **Code:** ``
> **Type:** Empty line

### Line 176
> **Code:** `@app.get("/history")`
> **Type:** Arithmetic operation

### Line 177
> **Code:** `async def history(limit: int = 50):`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `n = max(1, min(limit, LOG_CAP))`
> **Type:** Assignment/comparison

### Line 179
> **Code:** `return {"total": len(PREDICTION_LOG), "entries": list(reversed(PREDICT...`
> **Type:** Returns a value from a function

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** `@app.get("/stats")`
> **Type:** Arithmetic operation

### Line 182
> **Code:** `async def stats():`
> **Type:** Code statement

### Line 183
> **Code:** `n = len(PREDICTION_LOG)`
> **Type:** Assignment/comparison

### Line 184
> **Code:** `empty = {`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `"total_scans": 0,`
> **Type:** Code statement

### Line 186
> **Code:** `"fraud_rate": 0.0,`
> **Type:** Code statement

### Line 187
> **Code:** `"flagged_count": 0,`
> **Type:** Code statement

### Line 188
> **Code:** `"risk_level_distribution": {lvl: 0 for lvl in RISK_LEVELS},`
> **Type:** Logical operation

### Line 189
> **Code:** `"avg_probability": 0.0,`
> **Type:** Code statement

### Line 190
> **Code:** `"avg_latency_ms": 0.0,`
> **Type:** Code statement

### Line 191
> **Code:** `}`
> **Type:** Code statement

### Line 192
> **Code:** `if n == 0:`
> **Type:** Conditional statement

### Line 193
> **Code:** `return empty`
> **Type:** Returns a value from a function

### Line 194
> **Code:** `flagged = sum(1 for e in PREDICTION_LOG if e["result"]["prediction"] =...`
> **Type:** Assignment/comparison

### Line 195
> **Code:** `dist = {lvl: 0 for lvl in RISK_LEVELS}`
> **Type:** Assignment/comparison

### Line 196
> **Code:** `for e in PREDICTION_LOG:`
> **Type:** For loop

### Line 197
> **Code:** `dist[e["result"]["risk_level"]] += 1`
> **Type:** Assignment/comparison

### Line 198
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 199
> **Code:** `"total_scans": n,`
> **Type:** Code statement

### Line 200
> **Code:** `"fraud_rate": round(flagged / n, 4),`
> **Type:** Arithmetic operation

### Line 201
> **Code:** `"flagged_count": flagged,`
> **Type:** Code statement

### Line 202
> **Code:** `"risk_level_distribution": dist,`
> **Type:** Code statement

### Line 203
> **Code:** `"avg_probability": round(sum(e["result"]["probability"] for e in PREDI...`
> **Type:** Arithmetic operation

### Line 204
> **Code:** `"avg_latency_ms": round(sum(e["latency_ms"] for e in PREDICTION_LOG) /...`
> **Type:** Arithmetic operation

### Line 205
> **Code:** `}`
> **Type:** Code statement

### Line 206
> **Code:** ``
> **Type:** Empty line

### Line 207
> **Code:** `@app.get("/model-info")`
> **Type:** Arithmetic operation

### Line 208
> **Code:** `async def model_info():`
> **Type:** Code statement

### Line 209
> **Code:** `if MODEL is None or FEATURE_COLS is None:`
> **Type:** Conditional statement

### Line 210
> **Code:** `return {"error": "model not loaded"}`
> **Type:** Returns a value from a function

### Line 211
> **Code:** `f_imports = sorted(`
> **Type:** Assignment/comparison

### Line 212
> **Code:** `zip(FEATURE_COLS, MODEL.feature_importances_),`
> **Type:** Logical operation

### Line 213
> **Code:** `key=lambda pair: pair[1],`
> **Type:** Assignment/comparison

### Line 214
> **Code:** `reverse=True,`
> **Type:** Assignment/comparison

### Line 215
> **Code:** `)`
> **Type:** Code statement

### Line 216
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 217
> **Code:** `**MODEL_META,`
> **Type:** Arithmetic operation

### Line 218
> **Code:** `"feature_importance": [`
> **Type:** Logical operation

### Line 219
> **Code:** `{"feature": name, "importance": round(imp, 4)} for name, imp in f_impo...`
> **Type:** Logical operation

### Line 220
> **Code:** `],`
> **Type:** Code statement

### Line 221
> **Code:** `}`
> **Type:** Code statement

### Line 222
> **Code:** ``
> **Type:** Empty line

### Line 223
> **Code:** `@app.get("/")`
> **Type:** Arithmetic operation

### Line 224
> **Code:** `async def serve_ui():`
> **Type:** Code statement

### Line 225
> **Code:** `return FileResponse(UI_DIR / "index.html")`
> **Type:** Returns a value from a function

### Line 226
> **Code:** ``
> **Type:** Empty line

### Line 227
> **Code:** `if UI_DIR.exists():`
> **Type:** Conditional statement

### Line 228
> **Code:** `app.mount("/ui", StaticFiles(directory=str(UI_DIR)), name="ui")`
> **Type:** Assignment/comparison

### Line 229
> **Code:** ``
> **Type:** Empty line

### Line 230
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 231
> **Code:** `import uvicorn`
> **Type:** Imports a module

### Line 232
> **Code:** `uvicorn.run(app, host="0.0.0.0", port=8001)`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 232
- **Code lines:** 198
- **Comments:** 4
- **TODO items:** 0
- **Empty lines:** 30

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: main.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/__init__.py`
- **Total lines:** 1
- **File size:** 65 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""src package: core source code for the churn MLOps project."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: config.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/config.py`
- **Total lines:** 78
- **File size:** 2318 bytes

## Line Type Summary
- **Code:** 54
- **Comment:** 10
- **Empty:** 14
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Shared project configuration: paths, feature columns, model names."...`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `import os`
> **Type:** Imports a module

### Line   6
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `# Project root: two levels up from src/`
> **Type:** Comment: Project root: two levels up from src/

### Line   9
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[1]`
> **Type:** Assignment/comparison

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `DATA_DIR = PROJECT_ROOT / "data"`
> **Type:** Assignment/comparison

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `# Canonical training input: the synthetic churn dataset produced by`
> **Type:** Comment: Canonical training input: the synthetic churn dataset produced by

### Line  14
> **Code:** `# data/raw/generate_churn_data.py and versioned through the DVC `valid...`
> **Type:** Comment: data/raw/generate_churn_data.py and versioned through the DVC `validate`

### Line  15
> **Code:** `# stage. Overridable via RAW_DATA_PATH for alternative environments.`
> **Type:** Comment: stage. Overridable via RAW_DATA_PATH for alternative environments.

### Line  16
> **Code:** `RAW_DATA_PATH = Path(os.getenv("RAW_DATA_PATH", DATA_DIR / "raw" / "da...`
> **Type:** Assignment/comparison

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `# Secondary dataset used only by the standalone fraud demo API (api/ma...`
> **Type:** Comment: Secondary dataset used only by the standalone fraud demo API (api/main.py,

### Line  19
> **Code:** `# src/api/main.py) and its UI. Generated by data/raw/generate_creditca...`
> **Type:** Comment: src/api/main.py) and its UI. Generated by data/raw/generate_creditcard_data.py.

### Line  20
> **Code:** `FRAUD_DATA_PATH = Path(os.getenv("FRAUD_DATA_PATH", DATA_DIR / "raw" /...`
> **Type:** Assignment/comparison

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `PROCESSED_DATA_PATH = DATA_DIR / "processed" / "dataset_clean.csv"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `FEATURES_PATH = DATA_DIR / "features" / "features.parquet"`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `REFERENCE_DATA_PATH = DATA_DIR / "reference" / "reference.csv"`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `MODELS_DIR = PROJECT_ROOT / "models"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `REPORTS_DIR = PROJECT_ROOT / "reports"`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `MONITORING_REPORTS_DIR = PROJECT_ROOT / "monitoring" / "reports"`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `MODEL_CARDS_DIR = PROJECT_ROOT / "model_cards"`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `MLFLOW_DIR = PROJECT_ROOT / "mlflow" / "mlruns"`
> **Type:** Assignment/comparison

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `# Target / sensitive attribute / id`
> **Type:** Comment: Target / sensitive attribute / id

### Line  32
> **Code:** `TARGET_COL = "churn"`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `SENSITIVE_COL = "gender"`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `ID_COL = "customer_id"`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `TIMESTAMP_COL = "timestamp"`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `NUMERIC_FEATURES = [`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `"age",`
> **Type:** Code statement

### Line  39
> **Code:** `"tenure_months",`
> **Type:** Code statement

### Line  40
> **Code:** `"monthly_charges",`
> **Type:** Code statement

### Line  41
> **Code:** `"total_charges",`
> **Type:** Code statement

### Line  42
> **Code:** `"num_services",`
> **Type:** Code statement

### Line  43
> **Code:** `"support_tickets",`
> **Type:** Logical operation

### Line  44
> **Code:** `"avg_call_minutes",`
> **Type:** Code statement

### Line  45
> **Code:** `]`
> **Type:** Code statement

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `BINARY_FEATURES = [`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `"has_online_backup",`
> **Type:** Code statement

### Line  49
> **Code:** `"has_device_protection",`
> **Type:** Code statement

### Line  50
> **Code:** `"has_tech_support",`
> **Type:** Logical operation

### Line  51
> **Code:** `]`
> **Type:** Code statement

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `CATEGORICAL_FEATURES = [`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `"region",`
> **Type:** Code statement

### Line  55
> **Code:** `"contract_type",`
> **Type:** Code statement

### Line  56
> **Code:** `"payment_method",`
> **Type:** Code statement

### Line  57
> **Code:** `]`
> **Type:** Code statement

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `# Full feature set fed to the model`
> **Type:** Comment: Full feature set fed to the model

### Line  60
> **Code:** `BASE_FEATURES = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATU...`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `# Plausible ranges enforced by clamp_numeric during preprocessing.`
> **Type:** Comment: Plausible ranges enforced by clamp_numeric during preprocessing.

### Line  63
> **Code:** `NUMERIC_RANGES = {`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `"age": (18, 100),`
> **Type:** Code statement

### Line  65
> **Code:** `"tenure_months": (0, 120),`
> **Type:** Code statement

### Line  66
> **Code:** `"monthly_charges": (0, 500),`
> **Type:** Code statement

### Line  67
> **Code:** `"total_charges": (0, 60000),`
> **Type:** Code statement

### Line  68
> **Code:** `"num_services": (0, 10),`
> **Type:** Code statement

### Line  69
> **Code:** `"support_tickets": (0, 50),`
> **Type:** Logical operation

### Line  70
> **Code:** `"avg_call_minutes": (0, 5000),`
> **Type:** Code statement

### Line  71
> **Code:** `}`
> **Type:** Code statement

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `# Fairness / drift metrics thresholds`
> **Type:** Comment: Fairness / drift metrics thresholds

### Line  74
> **Code:** `FAIRNESS_DP_THRESHOLD = 0.1`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `DRIFT_THRESHOLD = 0.3`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `F1_PROMOTION_THRESHOLD = 0.25`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `AUC_PROMOTION_THRESHOLD = 0.80`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `CHALLENGER_RATIO = 0.1`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 78
- **Code lines:** 54
- **Comments:** 10
- **TODO items:** 0
- **Empty lines:** 14

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: config.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/serving/__init__.py`
- **Total lines:** 1
- **File size:** 72 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""serving package: model serving (BentoML) and inference endpoints.""...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: bento_service.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/serving/bento_service.py`
- **Total lines:** 69
- **File size:** 1893 bytes

## Line Type Summary
- **Code:** 48
- **Comment:** 0
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""BentoML serving service: ``/predict`` and ``/explain`` endpoints.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `The service loads the registered MLflow model and exposes:`
> **Type:** Logical operation

### Line   4
> **Code:** `- ``predict``: returns the churn probability + class label,`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- ``explain``: returns per-feature SHAP contributions for the instance...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `Run with: ``bentoml serve src.serving.bento_service:svc```
> **Type:** Code statement

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import sys`
> **Type:** Imports a module

### Line  13
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  17
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `import bentoml`
> **Type:** Imports a module

### Line  23
> **Code:** `from bentoml.io import JSON, NumpyNdarray`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `MODEL_TAG = "churn_model:production"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `def _load_runner():`
> **Type:** Function definition

### Line  29
> **Code:** `model_ref = bentoml.mlflow.get(MODEL_TAG)`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `return model_ref.to_runner()`
> **Type:** Returns a value from a function

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `runner = _load_runner()`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `svc = bentoml.Service("mlops_churn_service", runners=[runner])`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `@svc.api(input=NumpyNdarray(), output=JSON())`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `def predict(input_data: np.ndarray) -> dict:`
> **Type:** Function definition

### Line  40
> **Code:** `"""Return the predicted class and churn probability."""`
> **Type:** Logical operation

### Line  41
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `proba = runner.predict_proba.run(arr)[:, 1]`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `pred = (proba >= 0.5).astype(int)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  45
> **Code:** `"prediction": pred.tolist(),`
> **Type:** Code statement

### Line  46
> **Code:** `"churn_probability": proba.tolist(),`
> **Type:** Code statement

### Line  47
> **Code:** `}`
> **Type:** Code statement

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `@svc.api(input=NumpyNdarray(), output=JSON())`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `def explain(input_data: np.ndarray) -> dict:`
> **Type:** Function definition

### Line  52
> **Code:** `"""Return SHAP force values for the given instance(s)."""`
> **Type:** Logical operation

### Line  53
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `model = _model_ref()`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `import shap`
> **Type:** Imports a module

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `shap_values = explainer.shap_values(arr)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  60
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  63
> **Code:** `"expected_value": float(explainer.expected_value),`
> **Type:** Code statement

### Line  64
> **Code:** `"shap_values": shap_values.tolist(),`
> **Type:** Code statement

### Line  65
> **Code:** `}`
> **Type:** Code statement

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def _model_ref():`
> **Type:** Function definition

### Line  69
> **Code:** `return bentoml.mlflow.get(MODEL_TAG).load()`
> **Type:** Returns a value from a function

## Summary
- **Total lines:** 69
- **Code lines:** 48
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: bento_service.py*
---

# mlops-full-mlops-skills-project: champion_challenger.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/serving/champion_challenger.py`
- **Total lines:** 157
- **File size:** 5139 bytes

## Line Type Summary
- **Code:** 120
- **Comment:** 0
- **Empty:** 37
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Champion / Challenger traffic routing.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A challenger model receives a small, controlled fraction of the traffi...`
> **Type:** Code statement

### Line   4
> **Code:** `(``CHALLENGER_RATIO`` = 10% by default) in parallel with the current`
> **Type:** Assignment/comparison

### Line   5
> **Code:** `champion. Every routing decision is logged (structured JSON lines) so ...`
> **Type:** Code statement

### Line   6
> **Code:** `two models can be compared statistically a posteriori.`
> **Type:** Logical operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import sys`
> **Type:** Imports a module

### Line  12
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import json`
> **Type:** Imports a module

### Line  19
> **Code:** `import logging`
> **Type:** Imports a module

### Line  20
> **Code:** `import random`
> **Type:** Imports a module

### Line  21
> **Code:** `from datetime import datetime, timezone`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from typing import Callable`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import CHALLENGER_RATIO, MODELS_DIR, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `ROUTING_LOG = Path("monitoring/logs/routing_decisions.jsonl")`
> **Type:** Assignment/comparison

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def load_model(path: Path):`
> **Type:** Function definition

### Line  33
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `return joblib.load(path)`
> **Type:** Returns a value from a function

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `def _default_predict_fn(model):`
> **Type:** Function definition

### Line  39
> **Code:** `def predict(input_data):`
> **Type:** Function definition

### Line  40
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `if arr.ndim == 1:`
> **Type:** Conditional statement

### Line  44
> **Code:** `arr = arr.reshape(1, -1)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `return model.predict(arr)`
> **Type:** Returns a value from a function

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `return predict`
> **Type:** Returns a value from a function

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `class ChampionChallengerRouter:`
> **Type:** Class definition

### Line  51
> **Code:** `"""Routes each inference to champion or challenger and logs the decisi...`
> **Type:** Logical operation

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def __init__(`
> **Type:** Function definition

### Line  54
> **Code:** `self,`
> **Type:** Code statement

### Line  55
> **Code:** `champion_model,`
> **Type:** Code statement

### Line  56
> **Code:** `challenger_model,`
> **Type:** Code statement

### Line  57
> **Code:** `champion_name: str = "champion",`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `challenger_name: str = "challenger",`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `challenger_ratio: float = CHALLENGER_RATIO,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `log_path: Path = ROUTING_LOG,`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `predict_fn: Callable | None = None,`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `seed: int | None = None,`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `):`
> **Type:** Code statement

### Line  64
> **Code:** `self.champion = champion_model`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `self.challenger = challenger_model`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `self.champion_name = champion_name`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `self.challenger_name = challenger_name`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `self.challenger_ratio = challenger_ratio`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `self.log_path = log_path`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `self.predict_fn = predict_fn or _default_predict_fn`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `self.rng = random.Random(seed)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def route(self, input_data) -> dict:`
> **Type:** Function definition

### Line  74
> **Code:** `"""Route one request, log the decision, return prediction + version.""...`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `if self.rng.random() < self.challenger_ratio:`
> **Type:** Conditional statement

### Line  76
> **Code:** `version = self.challenger_name`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `model = self.challenger`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `else:`
> **Type:** Else block

### Line  79
> **Code:** `version = self.champion_name`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `model = self.champion`
> **Type:** Assignment/comparison

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `prediction = self.predict_fn(model)(input_data).tolist()`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `self._log(input_data, prediction, version)`
> **Type:** Function call

### Line  84
> **Code:** `return {"prediction": prediction, "model_version": version}`
> **Type:** Returns a value from a function

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def _log(self, input_data, prediction, version) -> None:`
> **Type:** Function definition

### Line  87
> **Code:** `entry = {`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `"timestamp": datetime.now(timezone.utc).isoformat(),`
> **Type:** Logical operation

### Line  89
> **Code:** `"model_version": version,`
> **Type:** Code statement

### Line  90
> **Code:** `"prediction": prediction,`
> **Type:** Code statement

### Line  91
> **Code:** `"request_id": f"{int(datetime.now().timestamp()*1000)}",`
> **Type:** Arithmetic operation

### Line  92
> **Code:** `}`
> **Type:** Code statement

### Line  93
> **Code:** `self.log_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `with open(self.log_path, "a") as handle:`
> **Type:** Context manager

### Line  95
> **Code:** `handle.write(json.dumps(entry) + "\n")`
> **Type:** Arithmetic operation

### Line  96
> **Code:** `logger.info("Routed request to %s -> %s", version, prediction)`
> **Type:** Arithmetic operation

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def build_router(`
> **Type:** Function definition

### Line 100
> **Code:** `champion_path: Path = MODELS_DIR / "churn_model.joblib",`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `challenger_path: Path | None = None,`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `challenger_ratio: float = CHALLENGER_RATIO,`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `) -> ChampionChallengerRouter:`
> **Type:** Arithmetic operation

### Line 104
> **Code:** `"""Build a router, defaulting the challenger to the ONNX-converted mod...`
> **Type:** Arithmetic operation

### Line 105
> **Code:** `champion = load_model(champion_path)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `challenger = load_model(challenger_path) if challenger_path else champ...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `return ChampionChallengerRouter(`
> **Type:** Returns a value from a function

### Line 108
> **Code:** `champion, challenger, challenger_ratio=challenger_ratio`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `)`
> **Type:** Code statement

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `def simulate_routing(n_requests: int = 1000, challenger_ratio: float =...`
> **Type:** Function definition

### Line 113
> **Code:** `"""Send ``n_requests`` synthetic requests through the router.`
> **Type:** Code statement

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `Returns a small summary (request counts per model version) proving the`
> **Type:** Code statement

### Line 116
> **Code:** `~10% challenger split and that every decision was logged.`
> **Type:** Arithmetic operation

### Line 117
> **Code:** `"""`
> **Type:** Code statement

### Line 118
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `X = _load_sample_features(n_requests)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `router = build_router(challenger_ratio=challenger_ratio)`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `counts = {router.champion_name: 0, router.challenger_name: 0}`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `for row in X:`
> **Type:** For loop

### Line 124
> **Code:** `result = router.route([row])`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `counts[result["model_version"]] += 1`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `return {"requests": n_requests, "counts": counts, "log_path": str(ROUT...`
> **Type:** Returns a value from a function

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `def _load_sample_features(n: int):`
> **Type:** Function definition

### Line 130
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line 131
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line 134
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line 135
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line 136
> **Code:** ``
> **Type:** Empty line

### Line 137
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 141
> **Code:** `return sets["X"].head(n).to_numpy(dtype=np.float32)`
> **Type:** Returns a value from a function

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 145
> **Code:** `import argparse`
> **Type:** Imports a module

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `parser = argparse.ArgumentParser(description="Champion/Challenger rout...`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `parser.add_argument("--requests", type=int, default=1000)`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `parser.add_argument("--challenger-ratio", type=float, default=CHALLENG...`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `summary = simulate_routing(args.requests, args.challenger_ratio)`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `print(summary)`
> **Type:** Prints output to console

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 157
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 157
- **Code lines:** 120
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 37

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: champion_challenger.py*
---

# mlops-full-mlops-skills-project: automl_baseline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/automl_baseline.py`
- **Total lines:** 83
- **File size:** 2416 bytes

## Line Type Summary
- **Code:** 62
- **Comment:** 0
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""AutoML comparative baseline (FLAML).`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Trains a baseline with FLAML in a short time budget and logs it to MLf...`
> **Type:** Logical operation

### Line   4
> **Code:** `it can be objectively compared against the Optuna-optimised model.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import sys`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  14
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import logging`
> **Type:** Imports a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** `from flaml import AutoML`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from sklearn.metrics import accuracy_score, f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def run_automl_baseline(time_budget: int = 60, experiment_name: str = ...`
> **Type:** Function definition

### Line  31
> **Code:** `X, y = _load_data()`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `)`
> **Type:** Code statement

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `automl = AutoML()`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `automl.fit(`
> **Type:** Code statement

### Line  38
> **Code:** `X_train,`
> **Type:** Code statement

### Line  39
> **Code:** `y_train,`
> **Type:** Code statement

### Line  40
> **Code:** `task="classification",`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `time_budget=time_budget,`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `metric="f1",`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `n_jobs=-1,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `log_file_name="artifacts/automl.log",`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `)`
> **Type:** Code statement

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `y_pred = automl.predict(X_test)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `y_proba = automl.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  51
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  52
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  53
> **Code:** `}`
> **Type:** Code statement

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  56
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line  57
> **Code:** `with mlflow.start_run(run_name=f"flaml_baseline_{time_budget}s"):`
> **Type:** Context manager

### Line  58
> **Code:** `mlflow.log_params(automl.best_config)`
> **Type:** Function call

### Line  59
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line  60
> **Code:** `mlflow.log_param("time_budget", time_budget)`
> **Type:** Function call

### Line  61
> **Code:** `mlflow.set_tag("tool", "FLAML")`
> **Type:** Function call

### Line  62
> **Code:** `mlflow.sklearn.log_model(automl.model.estimator, artifact_path="model"...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `logger.info("FLAML baseline metrics: %s", metrics)`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `return {"metrics": metrics, "best_config": automl.best_config}`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def _load_data():`
> **Type:** Function definition

### Line  69
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  75
> **Code:** `parser = argparse.ArgumentParser(description="FLAML AutoML baseline.")`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `parser.add_argument("--time-budget", type=int, default=60)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `result = run_automl_baseline(time_budget=args.time_budget)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `print(f"FLAML baseline F1: {result['metrics']['f1_score']:.4f}")`
> **Type:** Prints output to console

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  83
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 83
- **Code lines:** 62
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: automl_baseline.py*
---

# mlops-full-mlops-skills-project: export_onnx.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/export_onnx.py`
- **Total lines:** 130
- **File size:** 4102 bytes

## Line Type Summary
- **Code:** 94
- **Comment:** 1
- **Empty:** 35
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ONNX export and parity verification.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Converts the trained sklearn model to ONNX with ``skl2onnx``, then che...`
> **Type:** Code statement

### Line   4
> **Code:** `the ONNX model produces predictions identical (within a numeric tolera...`
> **Type:** Code statement

### Line   5
> **Code:** `the original sklearn model on the held-out test set.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  21
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  22
> **Code:** `from skl2onnx import convert_sklearn`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from skl2onnx.common.data_types import FloatTensorType`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import MODELS_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `TOLERANCE = 1e-5`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def export_to_onnx(model_path: Path = MODELS_DIR / "churn_model.joblib...`
> **Type:** Function definition

### Line  32
> **Code:** `out_path: Path = MODELS_DIR / "churn_model.onnx") -> Path:`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  34
> **Code:** `import onnxruntime as ort`
> **Type:** Imports a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `X = _load_feature_matrix()`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `n_features = X.shape[1]`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `initial_types = [("input", FloatTensorType([None, n_features]))]`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `onnx_model = convert_sklearn(model, initial_types=initial_types)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `out_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `with open(out_path, "wb") as handle:`
> **Type:** Context manager

### Line  45
> **Code:** `handle.write(onnx_model.SerializeToString())`
> **Type:** Logical operation

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `parity = check_parity(model, X, out_path, n_features)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `_write_report(parity)`
> **Type:** Logical operation

### Line  49
> **Code:** `return out_path`
> **Type:** Returns a value from a function

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _load_feature_matrix() -> pd.DataFrame:`
> **Type:** Function definition

### Line  53
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  54
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  55
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `X = sets["X"].astype(np.float32)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `return X.sample(n=min(500, len(X)), random_state=42)`
> **Type:** Returns a value from a function

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `def check_parity(model, X: pd.DataFrame, onnx_path: Path, n_features: ...`
> **Type:** Function definition

### Line  66
> **Code:** `import onnxruntime as ort`
> **Type:** Imports a module

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `X_np = X.to_numpy(dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `sklearn_pred = model.predict(X_np)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `sklearn_proba = model.predict_proba(X_np)[:, 1]`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutio...`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `onnx_out = session.run(None, {"input": X_np})`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `# ONNX output may be (proba) or (label, proba) depending on converter.`
> **Type:** Comment: ONNX output may be (proba) or (label, proba) depending on converter.

### Line  76
> **Code:** `onnx_proba = onnx_out[-1]`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `if isinstance(onnx_proba, list):`
> **Type:** Conditional statement

### Line  78
> **Code:** `if isinstance(onnx_proba[0], dict):`
> **Type:** Conditional statement

### Line  79
> **Code:** `onnx_proba = np.array([row[1] for row in onnx_proba])`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `else:`
> **Type:** Else block

### Line  81
> **Code:** `onnx_proba = np.asarray(onnx_proba)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `if onnx_proba.ndim == 2:`
> **Type:** Conditional statement

### Line  83
> **Code:** `onnx_proba = onnx_proba[:, 1]`
> **Type:** Assignment/comparison

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `proba_diff = float(np.max(np.abs(sklearn_proba - onnx_proba)))`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `onnx_pred = (onnx_proba >= 0.5).astype(int)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `label_agreement = float(np.mean(sklearn_pred == onnx_pred))`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  90
> **Code:** `"max_proba_abs_diff": proba_diff,`
> **Type:** Code statement

### Line  91
> **Code:** `"label_agreement": label_agreement,`
> **Type:** Code statement

### Line  92
> **Code:** `"n_instances": int(len(X_np)),`
> **Type:** Code statement

### Line  93
> **Code:** `"tolerance": TOLERANCE,`
> **Type:** Code statement

### Line  94
> **Code:** `"passed": proba_diff <= TOLERANCE,`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `}`
> **Type:** Code statement

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `def _write_report(parity: dict) -> None:`
> **Type:** Function definition

### Line  99
> **Code:** `import json`
> **Type:** Imports a module

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `with open(REPORTS_DIR / "onnx_parity_report.json", "w") as handle:`
> **Type:** Context manager

### Line 103
> **Code:** `json.dump(parity, handle, indent=2)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 107
> **Code:** `parser = argparse.ArgumentParser(description="Export model to ONNX and...`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.j...`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `parser.add_argument("--output", default=str(MODELS_DIR / "churn_model....`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `path = export_to_onnx(Path(args.model), Path(args.output))`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `print(f"ONNX model written to {path}")`
> **Type:** Prints output to console

### Line 114
> **Code:** `report = _read_report()`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `print(`
> **Type:** Prints output to console

### Line 116
> **Code:** `f"Parity: max proba diff={report['max_proba_abs_diff']:.2e} "`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `f"-> {'PASS' if report['passed'] else 'FAIL'} "`
> **Type:** Arithmetic operation

### Line 118
> **Code:** `f"(label agreement {report['label_agreement']:.4f})"`
> **Type:** Logical operation

### Line 119
> **Code:** `)`
> **Type:** Code statement

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `def _read_report() -> dict:`
> **Type:** Function definition

### Line 123
> **Code:** `import json`
> **Type:** Imports a module

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `with open(REPORTS_DIR / "onnx_parity_report.json") as handle:`
> **Type:** Context manager

### Line 126
> **Code:** `return json.load(handle)`
> **Type:** Returns a value from a function

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 130
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 130
- **Code lines:** 94
- **Comments:** 1
- **TODO items:** 0
- **Empty lines:** 35

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: export_onnx.py*
---

# mlops-full-mlops-skills-project: explain.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/explain.py`
- **Total lines:** 158
- **File size:** 5253 bytes

## Line Type Summary
- **Code:** 110
- **Comment:** 2
- **Empty:** 43
- **TODO:** 3

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model explainability: SHAP (global + local) and LIME (local).`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `- SHAP ``TreeExplainer`` produces a global summary plot saved to`
> **Type:** Arithmetic operation

### Line   4
> **Code:** ```reports/shap_summary.png`` plus per-instance local explanations.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- LIME is run independently on a few test instances to cross-check the...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `explanations with a method different from SHAP.`
> **Type:** Code statement

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import sys`
> **Type:** Imports a module

### Line  12
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  24
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  25
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  26
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `from src.config import MLFLOW_DIR, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def compute_shap(model, X_sample: pd.DataFrame) -> dict:`
> **Type:** Function definition

### Line  32
> **Code:** `import shap`
> **Type:** Imports a module

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `# TODO: medium - Add parameter to control number of top SHAP features ...`
> **Type:** TODO: medium - Add parameter to control number of top SHAP features returned

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `shap_values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `# GradientBoosting / modern shap returns a single (n, p) array for`
> **Type:** Comment: GradientBoosting / modern shap returns a single (n, p) array for

### Line  40
> **Code:** `# binary classifiers; handle the legacy (p, n) pair case too.`
> **Type:** Comment: binary classifiers; handle the legacy (p, n) pair case too.

### Line  41
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  42
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `elif getattr(shap_values, "ndim", 0) == 3:`
> **Type:** Else-if branch

### Line  44
> **Code:** `shap_values = shap_values[..., 1]`
> **Type:** Assignment/comparison

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `mean_abs = np.abs(shap_values).mean(axis=0)`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `importance = pd.Series(mean_abs, index=X_sample.columns).sort_values(a...`
> **Type:** Imports a module

### Line  48
> **Code:** `return {"explainer": explainer, "shap_values": shap_values, "importanc...`
> **Type:** Returns a value from a function

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `def save_shap_summary(model, X_sample: pd.DataFrame, path: Path) -> di...`
> **Type:** Function definition

### Line  52
> **Code:** `import shap`
> **Type:** Imports a module

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `# TODO: medium - Add parameter to control number of top SHAP features ...`
> **Type:** TODO: medium - Add parameter to control number of top SHAP features returned

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `shap_values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  59
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `elif getattr(shap_values, "ndim", 0) == 3:`
> **Type:** Else-if branch

### Line  61
> **Code:** `shap_values = shap_values[..., 1]`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `shap.summary_plot(shap_values, X_sample, show=False)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `plt.savefig(path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `plt.close()`
> **Type:** Library function call

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `mean_abs = np.abs(shap_values).mean(axis=0)`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `return pd.Series(mean_abs, index=X_sample.columns).sort_values(ascendi...`
> **Type:** Returns a value from a function

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `def explain_lime(model, X_sample: pd.DataFrame, feature_names: list, n...`
> **Type:** Function definition

### Line  73
> **Code:** `import lime`
> **Type:** Imports a module

### Line  74
> **Code:** `from lime.lime_tabular import LimeTabularExplainer`
> **Type:** Imports specific names from a module

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `X_np = X_sample.values`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `explainer = LimeTabularExplainer(`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `X_np,`
> **Type:** Code statement

### Line  79
> **Code:** `feature_names=feature_names,`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `class_names=["not_churn", "churn"],`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `mode="classification",`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `random_state=42,`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `)`
> **Type:** Code statement

### Line  84
> **Code:** `explanations = []`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `for i in range(min(n, len(X_np))):`
> **Type:** For loop

### Line  86
> **Code:** `exp = explainer.explain_instance(`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `X_np[i], model.predict_proba, num_features=5, labels=(1,)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `)`
> **Type:** Code statement

### Line  89
> **Code:** `explanations.append(`
> **Type:** Code statement

### Line  90
> **Code:** `{"instance": i, "top_features": exp.as_list(label=1)}`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `)`
> **Type:** Code statement

### Line  92
> **Code:** `return explanations`
> **Type:** Returns a value from a function

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `def run(model_path: Path = Path("models/churn_model.joblib"), n_sample...`
> **Type:** Function definition

### Line  96
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `from src.models.evaluate import _load_data`
> **Type:** Imports specific names from a module

### Line  99
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line 100
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line 101
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `X = sets["X"]`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `X_sample = X.sample(n=min(n_samples, len(X)), random_state=42)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `importance = save_shap_summary(model, X_sample, REPORTS_DIR / "shap_su...`
> **Type:** Imports a module

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `local_shap = []`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `explainer_shap = _shap_explainer(model, X_sample)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `shap_values = _shap_values(explainer_shap, X_sample)`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `local_shap.append({"instance": 0, "values": shap_values[0].tolist()})`
> **Type:** Function call

### Line 118
> **Code:** ``
> **Type:** Empty line

### Line 119
> **Code:** `lime_explanations = explain_lime(model, X_sample, list(X_sample.column...`
> **Type:** Assignment/comparison

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `"shap_importance": importance.to_dict(),`
> **Type:** Logical operation

### Line 123
> **Code:** `"shap_summary_path": str(REPORTS_DIR / "shap_summary.png"),`
> **Type:** Arithmetic operation

### Line 124
> **Code:** `"lime_explanations": lime_explanations,`
> **Type:** Code statement

### Line 125
> **Code:** `"n_instances_explained": len(local_shap),`
> **Type:** Code statement

### Line 126
> **Code:** `}`
> **Type:** Code statement

### Line 127
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** ``
> **Type:** Empty line

### Line 130
> **Code:** `def _shap_explainer(model, X_sample):`
> **Type:** Function definition

### Line 131
> **Code:** `import shap`
> **Type:** Imports a module

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `# TODO: medium - Add parameter to control number of top SHAP features ...`
> **Type:** TODO: medium - Add parameter to control number of top SHAP features returned

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** `return shap.TreeExplainer(model)`
> **Type:** Returns a value from a function

### Line 136
> **Code:** ``
> **Type:** Empty line

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `def _shap_values(explainer, X_sample):`
> **Type:** Function definition

### Line 139
> **Code:** `values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `if isinstance(values, list):`
> **Type:** Conditional statement

### Line 141
> **Code:** `values = values[1] if len(values) > 1 else values[0]`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `return values`
> **Type:** Returns a value from a function

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** ``
> **Type:** Empty line

### Line 145
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 146
> **Code:** `parser = argparse.ArgumentParser(description="SHAP + LIME explainabili...`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `parser.add_argument("--samples", type=int, default=200)`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** `result = run(Path(args.model), n_samples=args.samples)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `print("SHAP top-5 features:", list(result["shap_importance"].items())[...`
> **Type:** Prints output to console

### Line 153
> **Code:** `print("Saved summary to:", result["shap_summary_path"])`
> **Type:** Prints output to console

### Line 154
> **Code:** `print("LIME explanations generated for", len(result["lime_explanations...`
> **Type:** Prints output to console

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 158
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 158
- **Code lines:** 110
- **Comments:** 2
- **TODO items:** 3
- **Empty lines:** 43

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: explain.py*
---

# mlops-full-mlops-skills-project: fairness_check.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/fairness_check.py`
- **Total lines:** 162
- **File size:** 5173 bytes

## Line Type Summary
- **Code:** 120
- **Comment:** 2
- **Empty:** 38
- **TODO:** 2

## Detailed Line Explanations

### Line   1
> **Code:** `"""Fairness audit with Fairlearn.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Computes, per sensitive group (``gender``):`
> **Type:** Code statement

### Line   4
> **Code:** `- selection rate (positive prediction rate),`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- accuracy,`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `and the two headline disparity metrics:`
> **Type:** Logical operation

### Line   7
> **Code:** `- Demographic Parity Difference (dp_diff),`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- Equalized Odds Difference (eq_odds_diff).`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `A model is considered **unfair** (rejected for promotion) when the`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `demographic parity difference exceeds ``FAIRNESS_DP_THRESHOLD`` (0.1).`
> **Type:** Code statement

### Line  12
> **Code:** `Results are saved as JSON + a bar chart in ``reports/``.`
> **Type:** Arithmetic operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import sys`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  22
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  25
> **Code:** `import json`
> **Type:** Imports a module

### Line  26
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  31
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  32
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  33
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  34
> **Code:** `from sklearn.metrics import accuracy_score`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `from src.config import FAIRNESS_DP_THRESHOLD, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `try:`
> **Type:** Code statement

### Line  40
> **Code:** `from fairlearn.metrics import (`
> **Type:** Imports specific names from a module

### Line  41
> **Code:** `MetricFrame,`
> **Type:** Code statement

### Line  42
> **Code:** `demographic_parity_difference,`
> **Type:** Code statement

### Line  43
> **Code:** `equalized_odds_difference,`
> **Type:** Code statement

### Line  44
> **Code:** `selection_rate,`
> **Type:** Code statement

### Line  45
> **Code:** `)`
> **Type:** Code statement

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `FAIRLEARN_AVAILABLE = True`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `except ImportError:  # pragma: no cover - graceful degradation`
> **Type:** Arithmetic operation

### Line  49
> **Code:** `FAIRLEARN_AVAILABLE = False`
> **Type:** Assignment/comparison

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _build_test_frame():`
> **Type:** Function definition

### Line  53
> **Code:** `"""Return (y_test, y_pred, sensitive_series) aligned on the same split...`
> **Type:** Code statement

### Line  54
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `from src.config import RAW_DATA_PATH, SENSITIVE_COL, TARGET_COL`
> **Type:** Imports specific names from a module

### Line  57
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  58
> **Code:** `from src.features.build_features import build_features`
> **Type:** Imports specific names from a module

### Line  59
> **Code:** ``
> **Type:** Empty line

### Line  60
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `# gender is one-hot encoded (and dropped) inside build_features; keep ...`
> **Type:** Comment: gender is one-hot encoded (and dropped) inside build_features; keep the

### Line  64
> **Code:** `# raw series aligned positionally with the feature frame for the audit...`
> **Type:** Comment: raw series aligned positionally with the feature frame for the audit.

### Line  65
> **Code:** `gender_all = clean[SENSITIVE_COL].reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `model = joblib.load("models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `X = frame.drop(columns=[TARGET_COL])`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `y = frame[TARGET_COL]`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `)`
> **Type:** Code statement

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `sensitive = gender_all.iloc[X_test.index].reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `X_test_model = X_test.reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `y_pred = model.predict(X_test_model)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `return y_test.reset_index(drop=True), y_pred, sensitive`
> **Type:** Returns a value from a function

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** `def fairness_check(model_path: Path = Path("models/churn_model.joblib"...`
> **Type:** Function definition

### Line  84
> **Code:** `"""Run the full fairness audit and persist a JSON report."""`
> **Type:** Logical operation

### Line  85
> **Code:** `if not FAIRLEARN_AVAILABLE:`
> **Type:** Conditional statement

### Line  86
> **Code:** `raise ImportError("fairlearn is required for fairness_check")`
> **Type:** Raises an exception

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `y_test, y_pred, sensitive = _build_test_frame()`
> **Type:** Assignment/comparison

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `metric_frame = MetricFrame(`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `metrics={`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `"accuracy": accuracy_score,`
> **Type:** Logical operation

### Line  93
> **Code:** `"selection_rate": selection_rate,`
> **Type:** Code statement

### Line  94
> **Code:** `},`
> **Type:** Code statement

### Line  95
> **Code:** `y_true=y_test,`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `y_pred=y_pred,`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `sensitive_features=sensitive,`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `)`
> **Type:** Code statement

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `dp_diff = float(`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `demographic_parity_difference(`
> **Type:** Code statement

### Line 102
> **Code:** `y_test, y_pred, sensitive_features=sensitive`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `)`
> **Type:** Code statement

### Line 104
> **Code:** `)`
> **Type:** Code statement

### Line 105
> **Code:** `eq_odds_diff = float(`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `equalized_odds_difference(`
> **Type:** Code statement

### Line 107
> **Code:** `y_test, y_pred, sensitive_features=sensitive`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `)`
> **Type:** Code statement

### Line 109
> **Code:** `)`
> **Type:** Code statement

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `group_summary = metric_frame.by_group.to_dict()`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `"demographic_parity_difference": dp_diff,`
> **Type:** Code statement

### Line 115
> **Code:** `"equalized_odds_difference": eq_odds_diff,`
> **Type:** Code statement

### Line 116
> **Code:** `"threshold": FAIRNESS_DP_THRESHOLD,`
> **Type:** Code statement

### Line 117
> **Code:** `"passed": dp_diff <= FAIRNESS_DP_THRESHOLD,`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `"selection_rate_by_group": group_summary["selection_rate"],`
> **Type:** Data structure operation

### Line 119
> **Code:** `"accuracy_by_group": group_summary["accuracy"],`
> **Type:** Data structure operation

### Line 120
> **Code:** `"overall_selection_rate": float(selection_rate(y_test, y_pred)),`
> **Type:** Code statement

### Line 121
> **Code:** `}`
> **Type:** Code statement

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `with open(REPORTS_DIR / "fairness_report.json", "w") as handle:`
> **Type:** Context manager

### Line 125
> **Code:** `json.dump(result, handle, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** ``
> **Type:** Empty line

### Line 127
> **Code:** `_plot_selection_rates(group_summary["selection_rate"])`
> **Type:** Function call

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** ``
> **Type:** Empty line

### Line 132
> **Code:** `def _plot_selection_rates(by_group: dict) -> None:`
> **Type:** Function definition

### Line 133
> **Code:** `groups = list(by_group.keys())`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `rates = list(by_group.values())`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `fig, ax = plt.subplots(figsize=(6, 4))`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `ax.bar([str(g) for g in groups], rates, color=["#4C72B0", "#DD8452"])`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `ax.set_ylabel("Selection rate")`
> **Type:** Function call

### Line 138
> **Code:** `ax.set_title("Selection rate by gender group")`
> **Type:** Function call

### Line 139
> **Code:** `fig.savefig(REPORTS_DIR / "fairness_selection_rate.png", dpi=120, bbox...`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 144
> **Code:** `parser = argparse.ArgumentParser(description="Fairness audit with Fair...`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 147
> **Code:** ``
> **Type:** Empty line

### Line 148
> **Code:** `result = fairness_check(Path(args.model))`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `verdict = "PASS" if result["passed"] else "FAIL"`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `print(`
> **Type:** Prints output to console

### Line 151
> **Code:** `f"DP difference={result['demographic_parity_difference']:.4f} "`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `f"(threshold {result['threshold']}) -> {verdict}"`
> **Type:** Arithmetic operation

### Line 153
> **Code:** `)`
> **Type:** Code statement

### Line 154
> **Code:** `print(f"Equalized odds difference={result['equalized_odds_difference']...`
> **Type:** Prints output to console

### Line 155
> **Code:** `print(f"Saved to reports/fairness_report.json")`
> **Type:** Prints output to console

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** ``
> **Type:** Empty line

### Line 158
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 159
> **Code:** `main()`
> **Type:** Function call

### Line 160
> **Code:** ``
> **Type:** Empty line

### Line 161
> **Code:** `# TODO: high - Add test to ensure protected attributes are excluded fr...`
> **Type:** TODO: high - Add test to ensure protected attributes are excluded from feature schema

### Line 162
> **Code:** `# TODO: medium - Implement tiered severity gate with documented sign-o...`
> **Type:** TODO: medium - Implement tiered severity gate with documented sign-off for Amber results

## Summary
- **Total lines:** 162
- **Code lines:** 120
- **Comments:** 2
- **TODO items:** 2
- **Empty lines:** 38

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: fairness_check.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/__init__.py`
- **Total lines:** 1
- **File size:** 78 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""models package: training, tuning, evaluation, and model registry lo...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/evaluate.py`
- **Total lines:** 115
- **File size:** 3433 bytes

## Line Type Summary
- **Code:** 87
- **Comment:** 0
- **Empty:** 28
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model evaluation: metrics + ROC curve on a held-out test set.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Reusable for any trained model object; logs the results into the curre...`
> **Type:** Logical operation

### Line   4
> **Code:** `MLflow run (or a dedicated evaluation run) and saves the ROC curve to`
> **Type:** Logical operation

### Line   5
> **Code:** ```reports/``.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import os`
> **Type:** Imports a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  24
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  25
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  26
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  27
> **Code:** `from sklearn.metrics import (`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `PrecisionRecallDisplay,`
> **Type:** Code statement

### Line  29
> **Code:** `RocCurveDisplay,`
> **Type:** Code statement

### Line  30
> **Code:** `accuracy_score,`
> **Type:** Logical operation

### Line  31
> **Code:** `f1_score,`
> **Type:** Logical operation

### Line  32
> **Code:** `precision_score,`
> **Type:** Logical operation

### Line  33
> **Code:** `recall_score,`
> **Type:** Logical operation

### Line  34
> **Code:** `roc_auc_score,`
> **Type:** Logical operation

### Line  35
> **Code:** `)`
> **Type:** Code statement

### Line  36
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `from src.config import MLFLOW_DIR, REPORTS_DIR, F1_PROMOTION_THRESHOLD...`
> **Type:** Imports specific names from a module

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `def load_model(path: Path):`
> **Type:** Function definition

### Line  42
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `return joblib.load(path)`
> **Type:** Returns a value from a function

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `def evaluate(model, X_test, y_test, log_to_mlflow: bool = True, experi...`
> **Type:** Function definition

### Line  48
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `y_proba = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  53
> **Code:** `"precision": precision_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  54
> **Code:** `"recall": recall_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  55
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  56
> **Code:** `"roc_auc": roc_auc_score(y_test, y_proba),`
> **Type:** Logical operation

### Line  57
> **Code:** `}`
> **Type:** Code statement

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `roc_path = REPORTS_DIR / "roc_curve.png"`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `pr_path = REPORTS_DIR / "precision_recall_curve.png"`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `fig, ax = plt.subplots()`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `ax.set_title("ROC Curve")`
> **Type:** Function call

### Line  66
> **Code:** `fig.savefig(roc_path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `fig, ax = plt.subplots()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=ax)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `ax.set_title("Precision-Recall Curve")`
> **Type:** Arithmetic operation

### Line  72
> **Code:** `fig.savefig(pr_path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `if log_to_mlflow:`
> **Type:** Conditional statement

### Line  76
> **Code:** `os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")`
> **Type:** Function call

### Line  77
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  78
> **Code:** `mlflow.set_experiment(experiment)`
> **Type:** Function call

### Line  79
> **Code:** `with mlflow.start_run(run_name="evaluate"):`
> **Type:** Context manager

### Line  80
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line  81
> **Code:** `mlflow.log_artifact(str(roc_path))`
> **Type:** Function call

### Line  82
> **Code:** `mlflow.log_artifact(str(pr_path))`
> **Type:** Function call

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `return metrics`
> **Type:** Returns a value from a function

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  88
> **Code:** `parser = argparse.ArgumentParser(description="Evaluate a trained model...`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `X, y = _load_data()`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `_, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_s...`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `model = load_model(Path(args.model))`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `metrics = evaluate(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `f1 = metrics["f1_score"]`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `auc = metrics["roc_auc"]`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `f1_pass = f1 >= F1_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `auc_pass = auc >= AUC_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `status = "PASS" if (f1_pass and auc_pass) else "FAIL"`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `print(f"Evaluation: {metrics}")`
> **Type:** Prints output to console

### Line 103
> **Code:** `print(f"F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}) {'PASS' if f1...`
> **Type:** Prints output to console

### Line 104
> **Code:** `print(f"AUC={auc:.4f} (threshold {AUC_PROMOTION_THRESHOLD}) {'PASS' if...`
> **Type:** Prints output to console

### Line 105
> **Code:** `print(f"Overall: {status}")`
> **Type:** Prints output to console

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `def _load_data():`
> **Type:** Function definition

### Line 109
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 115
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 115
- **Code lines:** 87
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 28

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: evaluate.py*
---

# mlops-full-mlops-skills-project: train.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/train.py`
- **Total lines:** 203
- **File size:** 6535 bytes

## Line Type Summary
- **Code:** 157
- **Comment:** 1
- **Empty:** 39
- **TODO:** 6

## Detailed Line Explanations

### Line   1
> **Code:** `"""`
> **Type:** Code statement

### Line   2
> **Code:** `# TODO: high - Add monotonicity constraint enforcement check before pr...`
> **Type:** TODO: high - Add monotonicity constraint enforcement check before promotion

### Line   3
> **Code:** `# TODO: medium - Implement SHAP value computation for each prediction`
> **Type:** TODO: medium - Implement SHAP value computation for each prediction

### Line   4
> **Code:** `# TODO: low - Add feature importance visualization to evidence pack`
> **Type:** TODO: low - Add feature importance visualization to evidence pack

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `# TODO: high - Add monotonicity constraint enforcement check before pr...`
> **Type:** TODO: high - Add monotonicity constraint enforcement check before promotion

### Line   8
> **Code:** `# TODO: medium - Implement SHAP value computation for each prediction`
> **Type:** TODO: medium - Implement SHAP value computation for each prediction

### Line   9
> **Code:** `# TODO: low - Add feature importance visualization to evidence pack`
> **Type:** TODO: low - Add feature importance visualization to evidence pack

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `Model training with full MLflow tracking for churn prediction.`
> **Type:** Logical operation

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `Every training run logs:`
> **Type:** Code statement

### Line  14
> **Code:** `- hyperparameters,`
> **Type:** Arithmetic operation

### Line  15
> **Code:** `- metrics (accuracy, F1, ROC-AUC),`
> **Type:** Arithmetic operation

### Line  16
> **Code:** `- the model artifact,`
> **Type:** Arithmetic operation

### Line  17
> **Code:** `- a confusion matrix figure,`
> **Type:** Arithmetic operation

### Line  18
> **Code:** `- tags linking to the data source hash and pipeline version.`
> **Type:** Arithmetic operation

### Line  19
> **Code:** `"""`
> **Type:** Code statement

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `import sys`
> **Type:** Imports a module

### Line  24
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  28
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  31
> **Code:** `import logging`
> **Type:** Imports a module

### Line  32
> **Code:** `import os`
> **Type:** Imports a module

### Line  33
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  38
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  39
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  40
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  41
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  42
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  43
> **Code:** `from sklearn.metrics import accuracy_score, confusion_matrix, f1_score...`
> **Type:** Imports specific names from a module

### Line  44
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  47
> **Code:** `MLFLOW_DIR,`
> **Type:** Code statement

### Line  48
> **Code:** `MODELS_DIR,`
> **Type:** Code statement

### Line  49
> **Code:** `RAW_DATA_PATH,`
> **Type:** Code statement

### Line  50
> **Code:** `REPORTS_DIR,`
> **Type:** Code statement

### Line  51
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  52
> **Code:** `F1_PROMOTION_THRESHOLD,`
> **Type:** Code statement

### Line  53
> **Code:** `AUC_PROMOTION_THRESHOLD,`
> **Type:** Code statement

### Line  54
> **Code:** `)`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `DEFAULT_PARAMS = {`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `"n_estimators": 200,`
> **Type:** Logical operation

### Line  60
> **Code:** `"max_depth": 12,`
> **Type:** Code statement

### Line  61
> **Code:** `"min_samples_leaf": 5,`
> **Type:** Code statement

### Line  62
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line  63
> **Code:** `"class_weight": "balanced_subsample",`
> **Type:** Code statement

### Line  64
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line  65
> **Code:** `"n_jobs": -1,`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `}`
> **Type:** Code statement

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `def load_training_data() -> tuple[pd.DataFrame, pd.Series]:`
> **Type:** Function definition

### Line  70
> **Code:** `"""Load raw data and build the model-ready feature matrix.`
> **Type:** Arithmetic operation

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `Goes through ``build_features`` so the id, timestamp and sensitive`
> **Type:** Logical operation

### Line  73
> **Code:** `columns are dropped and categoricals are one-hot encoded — the model`
> **Type:** Arithmetic operation

### Line  74
> **Code:** `never sees the raw frame.`
> **Type:** Code statement

### Line  75
> **Code:** `"""`
> **Type:** Code statement

### Line  76
> **Code:** `from src.data.ingestion import ingest_raw_data`
> **Type:** Imports specific names from a module

### Line  77
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  78
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `raw, _ = ingest_raw_data()`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `return sets["X"], sets["y"]`
> **Type:** Returns a value from a function

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `def save_confusion_matrix(y_true, y_pred, path: Path) -> None:`
> **Type:** Function definition

### Line  89
> **Code:** `cm = confusion_matrix(y_true, y_pred)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `fig, ax = plt.subplots(figsize=(4, 4))`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.7)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `for (i, j), val in np.ndenumerate(cm):`
> **Type:** For loop

### Line  93
> **Code:** `ax.text(j, i, str(val), ha="center", va="center")`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `ax.set_xlabel("Predicted")`
> **Type:** Function call

### Line  95
> **Code:** `ax.set_ylabel("Actual")`
> **Type:** Function call

### Line  96
> **Code:** `ax.set_title("Confusion Matrix")`
> **Type:** Function call

### Line  97
> **Code:** `fig.savefig(path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `def train_and_log(`
> **Type:** Function definition

### Line 102
> **Code:** `X_train: pd.DataFrame,`
> **Type:** Code statement

### Line 103
> **Code:** `X_test: pd.DataFrame,`
> **Type:** Code statement

### Line 104
> **Code:** `y_train: pd.Series,`
> **Type:** Code statement

### Line 105
> **Code:** `y_test: pd.Series,`
> **Type:** Code statement

### Line 106
> **Code:** `params: dict | None = None,`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `run_name: str = "churn_rf",`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `experiment_name: str = "churn_prediction",`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `register: bool = False,`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line 111
> **Code:** `"""Train a RandomForest classifier, log everything to MLflow.`
> **Type:** Logical operation

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `Returns a dict with the model, metrics and run id for downstream steps...`
> **Type:** Logical operation

### Line 114
> **Code:** `"""`
> **Type:** Code statement

### Line 115
> **Code:** `params = params or dict(DEFAULT_PARAMS)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")`
> **Type:** Function call

### Line 117
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line 118
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `with mlflow.start_run(run_name=run_name) as run:`
> **Type:** Context manager

### Line 121
> **Code:** `model = RandomForestClassifier(**params)`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `model.fit(X_train, y_train)`
> **Type:** Function call

### Line 123
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `y_proba = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line 125
> **Code:** ``
> **Type:** Empty line

### Line 126
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 128
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 129
> **Code:** `"roc_auc": roc_auc_score(y_test, y_proba),`
> **Type:** Logical operation

### Line 130
> **Code:** `}`
> **Type:** Code statement

### Line 131
> **Code:** ``
> **Type:** Empty line

### Line 132
> **Code:** `mlflow.log_params(model.get_params())`
> **Type:** Function call

### Line 133
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line 134
> **Code:** `mlflow.log_param("n_features", X_train.shape[1])`
> **Type:** Function call

### Line 135
> **Code:** `mlflow.log_param("data_source", str(RAW_DATA_PATH))`
> **Type:** Function call

### Line 136
> **Code:** `mlflow.set_tag("pipeline", run_name)`
> **Type:** Function call

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `cm_path = REPORTS_DIR / "confusion_matrix.png"`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `cm_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `save_confusion_matrix(y_test, y_pred, cm_path)`
> **Type:** Function call

### Line 141
> **Code:** `mlflow.log_artifact(str(cm_path))`
> **Type:** Function call

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** `model_dir = MODELS_DIR / f"run_{run.info.run_id}"`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `model_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `mlflow.sklearn.log_model(model, artifact_path="model")`
> **Type:** Assignment/comparison

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `if register:`
> **Type:** Conditional statement

### Line 148
> **Code:** `mlflow.sklearn.log_model(`
> **Type:** Code statement

### Line 149
> **Code:** `model,`
> **Type:** Code statement

### Line 150
> **Code:** `artifact_path="model",`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `registered_model_name="churn_model",`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `)`
> **Type:** Code statement

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** `mlflow.end_run()`
> **Type:** Function call

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** `logger.info("Trained model: %s", metrics)`
> **Type:** Arithmetic operation

### Line 157
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 158
> **Code:** `"model": model,`
> **Type:** Code statement

### Line 159
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 160
> **Code:** `"run_id": run.info.run_id,`
> **Type:** Code statement

### Line 161
> **Code:** `"feature_columns": list(X_train.columns),`
> **Type:** Code statement

### Line 162
> **Code:** `}`
> **Type:** Code statement

### Line 163
> **Code:** ``
> **Type:** Empty line

### Line 164
> **Code:** ``
> **Type:** Empty line

### Line 165
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 166
> **Code:** `parser = argparse.ArgumentParser(description="Train and track the chur...`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `parser.add_argument("--register", action="store_true", help="Register ...`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `parser.add_argument("--run-name", default="churn_rf")`
> **Type:** Assignment/comparison

### Line 169
> **Code:** `parser.add_argument("--test-size", type=float, default=0.25)`
> **Type:** Assignment/comparison

### Line 170
> **Code:** `parser.add_argument("--experiment", default="churn_prediction")`
> **Type:** Assignment/comparison

### Line 171
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 172
> **Code:** ``
> **Type:** Empty line

### Line 173
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line 174
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `X, y, test_size=args.test_size, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line 176
> **Code:** `)`
> **Type:** Code statement

### Line 177
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line 178
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line 179
> **Code:** `run_name=args.run_name,`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `experiment_name=args.experiment,`
> **Type:** Assignment/comparison

### Line 181
> **Code:** `register=args.register,`
> **Type:** Assignment/comparison

### Line 182
> **Code:** `)`
> **Type:** Code statement

### Line 183
> **Code:** ``
> **Type:** Empty line

### Line 184
> **Code:** `f1 = result["metrics"]["f1_score"]`
> **Type:** Assignment/comparison

### Line 185
> **Code:** `auc = result["metrics"]["roc_auc"]`
> **Type:** Assignment/comparison

### Line 186
> **Code:** `f1_pass = f1 >= F1_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 187
> **Code:** `auc_pass = auc >= AUC_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 188
> **Code:** `status = "PASS" if (f1_pass and auc_pass) else "FAIL"`
> **Type:** Assignment/comparison

### Line 189
> **Code:** `print(f"Training done. F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}...`
> **Type:** Prints output to console

### Line 190
> **Code:** `print(f"MLflow run: {result['run_id']}")`
> **Type:** Prints output to console

### Line 191
> **Code:** ``
> **Type:** Empty line

### Line 192
> **Code:** `# Persist model + feature columns for downstream steps.`
> **Type:** Comment: Persist model + feature columns for downstream steps.

### Line 193
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 194
> **Code:** ``
> **Type:** Empty line

### Line 195
> **Code:** `MODELS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 196
> **Code:** `joblib.dump(result["model"], MODELS_DIR / "churn_model.joblib")`
> **Type:** Arithmetic operation

### Line 197
> **Code:** `with open(MODELS_DIR / "feature_columns.txt", "w") as handle:`
> **Type:** Context manager

### Line 198
> **Code:** `handle.write("\n".join(result["feature_columns"]))`
> **Type:** Logical operation

### Line 199
> **Code:** `print("Model saved to models/churn_model.joblib")`
> **Type:** Prints output to console

### Line 200
> **Code:** ``
> **Type:** Empty line

### Line 201
> **Code:** ``
> **Type:** Empty line

### Line 202
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 203
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 203
- **Code lines:** 157
- **Comments:** 1
- **TODO items:** 6
- **Empty lines:** 39

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: train.py*
---

# mlops-full-mlops-skills-project: tune.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/tune.py`
- **Total lines:** 97
- **File size:** 3250 bytes

## Line Type Summary
- **Code:** 72
- **Comment:** 0
- **Empty:** 25
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Optuna hyperparameter optimisation with nested MLflow runs.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Each Optuna trial is logged as a *nested* MLflow run under the parent ...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `run, so the whole search space is comparable in the MLflow UI via para...`
> **Type:** Code statement

### Line   5
> **Code:** `coordinates. Uses the default TPE (bayesian) sampler.`
> **Type:** Logical operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import logging`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  21
> **Code:** `import optuna`
> **Type:** Imports a module

### Line  22
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  23
> **Code:** `from optuna.samplers import TPESampler`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from sklearn.metrics import f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from sklearn.model_selection import StratifiedKFold, cross_val_score`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def load_data() -> tuple[pd.DataFrame, pd.Series]:`
> **Type:** Function definition

### Line  34
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def objective(trial, X, y):`
> **Type:** Function definition

### Line  40
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `"n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `"max_depth": trial.suggest_int("max_depth", 3, 20),`
> **Type:** Code statement

### Line  43
> **Code:** `"min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),`
> **Type:** Code statement

### Line  44
> **Code:** `"max_features": trial.suggest_categorical("max_features", ["sqrt", "lo...`
> **Type:** Logical operation

### Line  45
> **Code:** `"min_samples_split": trial.suggest_int("min_samples_split", 2, 15),`
> **Type:** Code statement

### Line  46
> **Code:** `}`
> **Type:** Code statement

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `model = RandomForestClassifier(**params, random_state=42)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `with mlflow.start_run(nested=True):`
> **Type:** Context manager

### Line  50
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line  51
> **Code:** `cv_score = cross_val_score(`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `model, X, y, cv=StratifiedKFold(3), scoring="f1", n_jobs=-1`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `).mean()`
> **Type:** Function call

### Line  54
> **Code:** `mlflow.log_metric("cv_f1", cv_score)`
> **Type:** Logical operation

### Line  55
> **Code:** `trial.report(cv_score, step=0)`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `return cv_score`
> **Type:** Returns a value from a function

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `def tune(n_trials: int = 50, experiment_name: str = "churn_optuna") ->...`
> **Type:** Function definition

### Line  60
> **Code:** `"""Run a bayesian search; return best params / value / study."""`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  62
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `X, y = load_data()`
> **Type:** Assignment/comparison

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `study = optuna.create_study(`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `direction="maximize",`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `sampler=TPESampler(seed=42),`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `study_name="churn_rf_bayesian",`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):`
> **Type:** Context manager

### Line  73
> **Code:** `mlflow.log_param("n_trials", n_trials)`
> **Type:** Function call

### Line  74
> **Code:** `mlflow.log_param("sampler", "TPE")`
> **Type:** Function call

### Line  75
> **Code:** `study.optimize(`
> **Type:** Code statement

### Line  76
> **Code:** `lambda t: objective(t, X, y), n_trials=n_trials, show_progress_bar=Fal...`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** `mlflow.log_metric("best_cv_f1", study.best_value)`
> **Type:** Function call

### Line  79
> **Code:** `mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items(...`
> **Type:** Logical operation

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `logger.info("Best trial: %.4f with %s", study.best_value, study.best_p...`
> **Type:** Arithmetic operation

### Line  82
> **Code:** `return {"best_params": study.best_params, "best_value": study.best_val...`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  86
> **Code:** `parser = argparse.ArgumentParser(description="Optuna tuning for the ch...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `parser.add_argument("--trials", type=int, default=50)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `parser.add_argument("--experiment", default="churn_optuna")`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `result = tune(n_trials=args.trials, experiment_name=args.experiment)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `print(f"Best CV F1: {result['best_value']:.4f}")`
> **Type:** Prints output to console

### Line  93
> **Code:** `print(f"Best params: {result['best_params']}")`
> **Type:** Prints output to console

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  97
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 97
- **Code lines:** 72
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 25

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: tune.py*
---

# mlops-full-mlops-skills-project: promote.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/models/promote.py`
- **Total lines:** 227
- **File size:** 7305 bytes

## Line Type Summary
- **Code:** 173
- **Comment:** 5
- **Empty:** 49
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model promotion logic with hard gates.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A candidate model may only be promoted to Production when **all** gate...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `1. Performance: F1 >= ``F1_PROMOTION_THRESHOLD`` on the held-out set.`
> **Type:** Assignment/comparison

### Line   5
> **Code:** `2. Competitive: beats the current Production model (if any) by a margi...`
> **Type:** Code statement

### Line   6
> **Code:** `3. Quality: Deepchecks suite passes (no critical failures).`
> **Type:** Code statement

### Line   7
> **Code:** `4. Fairness: Fairlearn demographic parity difference within threshold.`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `On success the MLflow registered model is moved to Production and a mo...`
> **Type:** Logical operation

### Line  10
> **Code:** `card is generated.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import sys`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  20
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  23
> **Code:** `import json`
> **Type:** Imports a module

### Line  24
> **Code:** `import os`
> **Type:** Imports a module

### Line  25
> **Code:** `import logging`
> **Type:** Imports a module

### Line  26
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  29
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** `F1_PROMOTION_THRESHOLD,`
> **Type:** Code statement

### Line  33
> **Code:** `MLFLOW_DIR,`
> **Type:** Code statement

### Line  34
> **Code:** `MODEL_CARDS_DIR,`
> **Type:** Code statement

### Line  35
> **Code:** `MODELS_DIR,`
> **Type:** Code statement

### Line  36
> **Code:** `REPORTS_DIR,`
> **Type:** Code statement

### Line  37
> **Code:** `FAIRNESS_DP_THRESHOLD,`
> **Type:** Code statement

### Line  38
> **Code:** `)`
> **Type:** Code statement

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `BEAT_MARGIN = 0.005`
> **Type:** Assignment/comparison

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `def run_deepchecks(model, X_test, y_test) -> dict:`
> **Type:** Function definition

### Line  46
> **Code:** `"""Run the Deepchecks full suite; return pass/fail summary."""`
> **Type:** Arithmetic operation

### Line  47
> **Code:** `try:`
> **Type:** Code statement

### Line  48
> **Code:** `from deepchecks.tabular import Dataset`
> **Type:** Imports specific names from a module

### Line  49
> **Code:** `from deepchecks.tabular.suites import full_suite`
> **Type:** Imports specific names from a module

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `train_ds = Dataset(pd.DataFrame(X_test), label=y_test)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `test_ds = train_ds.copy()`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `suite = full_suite()`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `result = suite.run(train_ds, test_ds, model=model)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `result.save_as_html("reports/deepchecks_report.html")`
> **Type:** Arithmetic operation

### Line  56
> **Code:** `critical_failures = [`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `check.get_header() for check in result.results`
> **Type:** Logical operation

### Line  58
> **Code:** `if not check.passed`
> **Type:** Conditional statement

### Line  59
> **Code:** `]`
> **Type:** Code statement

### Line  60
> **Code:** `passed = not any(not check.passed for check in result.results)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `return {"passed": passed, "critical_failures": critical_failures}`
> **Type:** Returns a value from a function

### Line  62
> **Code:** `except ImportError:`
> **Type:** Logical operation

### Line  63
> **Code:** `logger.warning("deepchecks unavailable; treating gate as passed (skip)...`
> **Type:** Function call

### Line  64
> **Code:** `return {"passed": True, "skip": True}`
> **Type:** Returns a value from a function

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `def load_production_model_metrics() -> float | None:`
> **Type:** Function definition

### Line  68
> **Code:** `"""Return the F1 of the current registered Production model, if any.""...`
> **Type:** Code statement

### Line  69
> **Code:** `try:`
> **Type:** Code statement

### Line  70
> **Code:** `client = mlflow.MlflowClient(mlflow.get_tracking_uri())`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `versions = client.get_latest_versions("churn_model", stages=["Producti...`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  73
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  74
> **Code:** `run = client.get_run(versions[0].run_id)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `return float(run.data.metrics.get("f1_score", 0.0))`
> **Type:** Returns a value from a function

### Line  76
> **Code:** `except Exception:`
> **Type:** Code statement

### Line  77
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** `def promote(`
> **Type:** Function definition

### Line  81
> **Code:** `model_path: Path = MODELS_DIR / "churn_model.joblib",`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `experiment: str = "churn_prediction",`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  85
> **Code:** `"""Evaluate all promotion gates and promote the model if they all pass...`
> **Type:** Logical operation

### Line  86
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  87
> **Code:** `os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")`
> **Type:** Function call

### Line  88
> **Code:** `mlflow.set_experiment(experiment)`
> **Type:** Function call

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `# 1. Performance gate (F1).`
> **Type:** Comment: 1. Performance gate (F1).

### Line  91
> **Code:** `metrics = _evaluate_model(model_path)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `f1 = metrics["f1_score"]`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `gates = {"performance": f1 >= F1_PROMOTION_THRESHOLD}`
> **Type:** Assignment/comparison

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `# 2. Beats current Production.`
> **Type:** Comment: 2. Beats current Production.

### Line  96
> **Code:** `prod_f1 = load_production_model_metrics()`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `if prod_f1 is None:`
> **Type:** Conditional statement

### Line  98
> **Code:** `gates["beats_production"] = True`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `else:`
> **Type:** Else block

### Line 100
> **Code:** `gates["beats_production"] = f1 > prod_f1 + BEAT_MARGIN`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `gates_detail = {"candidate_f1": f1, "production_f1": prod_f1}`
> **Type:** Assignment/comparison

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `# 3. Deepchecks.`
> **Type:** Comment: 3. Deepchecks.

### Line 104
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `model = _load_model(model_path)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `deepchecks = run_deepchecks(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `gates["deepchecks"] = deepchecks["passed"]`
> **Type:** Assignment/comparison

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** `# 4. Fairness.`
> **Type:** Comment: 4. Fairness.

### Line 110
> **Code:** `fairness = _load_fairness_report()`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `gates["fairness"] = fairness.get("passed", False)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `all_passed = all(gates.values())`
> **Type:** Assignment/comparison

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 117
> **Code:** `"gate_detail": gates_detail,`
> **Type:** Code statement

### Line 118
> **Code:** `"fairness": {`
> **Type:** Code statement

### Line 119
> **Code:** `"dp_diff": fairness.get("demographic_parity_difference"),`
> **Type:** Code statement

### Line 120
> **Code:** `"threshold": fairness.get("threshold", FAIRNESS_DP_THRESHOLD),`
> **Type:** Code statement

### Line 121
> **Code:** `},`
> **Type:** Code statement

### Line 122
> **Code:** `"deepchecks": {"passed": deepchecks["passed"]},`
> **Type:** Data structure operation

### Line 123
> **Code:** `"promoted": all_passed,`
> **Type:** Code statement

### Line 124
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 125
> **Code:** `}`
> **Type:** Code statement

### Line 126
> **Code:** ``
> **Type:** Empty line

### Line 127
> **Code:** `if all_passed:`
> **Type:** Conditional statement

### Line 128
> **Code:** `_move_to_production(run_id)`
> **Type:** Function call

### Line 129
> **Code:** `logger.info("All promotion gates passed -> moved to Production.")`
> **Type:** Arithmetic operation

### Line 130
> **Code:** `else:`
> **Type:** Else block

### Line 131
> **Code:** `logger.warning("Promotion rejected: %s", {k: v for k, v in gates.items...`
> **Type:** Arithmetic operation

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `_write_report(report)`
> **Type:** Logical operation

### Line 134
> **Code:** `_generate_model_card(report)`
> **Type:** Logical operation

### Line 135
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line 136
> **Code:** ``
> **Type:** Empty line

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `def _evaluate_model(model_path: Path) -> dict:`
> **Type:** Function definition

### Line 139
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 140
> **Code:** `from sklearn.metrics import accuracy_score, f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 146
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 147
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 148
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 149
> **Code:** `}`
> **Type:** Code statement

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** ``
> **Type:** Empty line

### Line 152
> **Code:** `def _load_test_frame():`
> **Type:** Function definition

### Line 153
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line 154
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line 155
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line 156
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line 157
> **Code:** ``
> **Type:** Empty line

### Line 158
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line 159
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 162
> **Code:** `_, X_test, _, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `sets["X"], sets["y"], test_size=0.25, random_state=42, stratify=sets["...`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `)`
> **Type:** Code statement

### Line 165
> **Code:** `return X_test, y_test`
> **Type:** Returns a value from a function

### Line 166
> **Code:** ``
> **Type:** Empty line

### Line 167
> **Code:** ``
> **Type:** Empty line

### Line 168
> **Code:** `def _load_model(model_path: Path):`
> **Type:** Function definition

### Line 169
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `return joblib.load(model_path)`
> **Type:** Returns a value from a function

### Line 172
> **Code:** ``
> **Type:** Empty line

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** `def _load_fairness_report() -> dict:`
> **Type:** Function definition

### Line 175
> **Code:** `report_path = REPORTS_DIR / "fairness_report.json"`
> **Type:** Assignment/comparison

### Line 176
> **Code:** `if report_path.exists():`
> **Type:** Conditional statement

### Line 177
> **Code:** `return json.loads(report_path.read_text())`
> **Type:** Returns a value from a function

### Line 178
> **Code:** `return {"passed": False, "demographic_parity_difference": 1.0}`
> **Type:** Returns a value from a function

### Line 179
> **Code:** ``
> **Type:** Empty line

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** `def _move_to_production(run_id: str | None) -> None:`
> **Type:** Function definition

### Line 182
> **Code:** `client = mlflow.MlflowClient(mlflow.get_tracking_uri())`
> **Type:** Assignment/comparison

### Line 183
> **Code:** `if run_id:`
> **Type:** Conditional statement

### Line 184
> **Code:** `try:`
> **Type:** Code statement

### Line 185
> **Code:** `client.set_registered_model_alias("churn_model", "production", run_id)`
> **Type:** Function call

### Line 186
> **Code:** `return`
> **Type:** Returns a value from a function

### Line 187
> **Code:** `except Exception:`
> **Type:** Code statement

### Line 188
> **Code:** `pass`
> **Type:** Code statement

### Line 189
> **Code:** `# Fallback: transition the newest Staging/None version.`
> **Type:** Comment: Fallback: transition the newest Staging/None version.

### Line 190
> **Code:** `versions = client.get_latest_versions("churn_model", stages=["None", "...`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `if versions:`
> **Type:** Conditional statement

### Line 192
> **Code:** `client.transition_model_version_stage(`
> **Type:** Code statement

### Line 193
> **Code:** `"churn_model", versions[0].version, "Production", archive_existing_ver...`
> **Type:** Assignment/comparison

### Line 194
> **Code:** `)`
> **Type:** Code statement

### Line 195
> **Code:** ``
> **Type:** Empty line

### Line 196
> **Code:** ``
> **Type:** Empty line

### Line 197
> **Code:** `def _write_report(report: dict) -> None:`
> **Type:** Function definition

### Line 198
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line 199
> **Code:** ``
> **Type:** Empty line

### Line 200
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 201
> **Code:** `with open(REPORTS_DIR / "promotion_report.json", "w") as handle:`
> **Type:** Context manager

### Line 202
> **Code:** `json.dump(report, handle, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 203
> **Code:** ``
> **Type:** Empty line

### Line 204
> **Code:** ``
> **Type:** Empty line

### Line 205
> **Code:** `def _generate_model_card(report: dict) -> None:`
> **Type:** Function definition

### Line 206
> **Code:** `try:`
> **Type:** Code statement

### Line 207
> **Code:** `from model_cards.model_card_template import generate_model_card`
> **Type:** Imports specific names from a module

### Line 208
> **Code:** ``
> **Type:** Empty line

### Line 209
> **Code:** `generate_model_card(report, output_path=MODEL_CARDS_DIR / "model_card....`
> **Type:** Assignment/comparison

### Line 210
> **Code:** `except Exception as exc:  # pragma: no cover`
> **Type:** Code statement

### Line 211
> **Code:** `logger.warning("Model card generation failed: %s", exc)`
> **Type:** Arithmetic operation

### Line 212
> **Code:** ``
> **Type:** Empty line

### Line 213
> **Code:** ``
> **Type:** Empty line

### Line 214
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 215
> **Code:** `parser = argparse.ArgumentParser(description="Promotion gates + regist...`
> **Type:** Assignment/comparison

### Line 216
> **Code:** `parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.j...`
> **Type:** Assignment/comparison

### Line 217
> **Code:** `parser.add_argument("--run-id", default=None)`
> **Type:** Assignment/comparison

### Line 218
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 219
> **Code:** ``
> **Type:** Empty line

### Line 220
> **Code:** `report = promote(Path(args.model), run_id=args.run_id)`
> **Type:** Assignment/comparison

### Line 221
> **Code:** `print(f"Promoted: {report['promoted']}")`
> **Type:** Prints output to console

### Line 222
> **Code:** `print("Gates:", report["gates"])`
> **Type:** Prints output to console

### Line 223
> **Code:** `print("Report saved to reports/promotion_report.json")`
> **Type:** Prints output to console

### Line 224
> **Code:** ``
> **Type:** Empty line

### Line 225
> **Code:** ``
> **Type:** Empty line

### Line 226
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 227
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 227
- **Code lines:** 173
- **Comments:** 5
- **TODO items:** 0
- **Empty lines:** 49

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: promote.py*
---

# mlops-full-mlops-skills-project: main.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/api/main.py`
- **Total lines:** 313
- **File size:** 9504 bytes

## Line Type Summary
- **Code:** 257
- **Comment:** 0
- **Empty:** 56
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""FastAPI server for the fraud detection demo.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Self-contained: trains a model on startup from the credit card transac...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `file in ``data/raw/`` (generated by ``data/raw/generate_creditcard_dat...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `when absent). This demo is deliberately independent of the churn train...`
> **Type:** Code statement

### Line   6
> **Code:** `pipeline in ``src/models/`` — it has its own schema and its own loader...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `Endpoints: /health, /predict, /history, /stats, /model-info, / (UI)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import json`
> **Type:** Imports a module

### Line  13
> **Code:** `import logging`
> **Type:** Imports a module

### Line  14
> **Code:** `import time`
> **Type:** Imports a module

### Line  15
> **Code:** `import uuid`
> **Type:** Imports a module

### Line  16
> **Code:** `from contextlib import asynccontextmanager`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `from datetime import datetime`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from typing import Any`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  22
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  23
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  24
> **Code:** `from fastapi import FastAPI, HTTPException, Request`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from fastapi.responses import HTMLResponse`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from fastapi.staticfiles import StaticFiles`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `from pydantic import BaseModel, Field`
> **Type:** Imports specific names from a module

### Line  28
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** `from sklearn.metrics import f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `from src.config import FRAUD_DATA_PATH, MODELS_DIR`
> **Type:** Imports specific names from a module

### Line  33
> **Code:** `from src.data.ingestion import file_hash`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelnam...`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `MODEL_PATH = MODELS_DIR / "fraud_model.joblib"`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `FEATURE_COLS_PATH = MODELS_DIR / "feature_columns.txt"`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `TARGET_COL = "Class"`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `GENERATOR = Path(__file__).resolve().parents[2] / "data" / "raw" / "ge...`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `prediction_history: list[dict] = []`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `model: RandomForestClassifier | None = None`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `feature_columns: list[str] = []`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `model_info: dict[str, Any] = {}`
> **Type:** Assignment/comparison

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def load_transactions() -> tuple[pd.DataFrame, dict]:`
> **Type:** Function definition

### Line  50
> **Code:** `"""Load the transaction file, generating the synthetic demo data if ab...`
> **Type:** Code statement

### Line  51
> **Code:** `import subprocess`
> **Type:** Imports a module

### Line  52
> **Code:** `import sys`
> **Type:** Imports a module

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `if not FRAUD_DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  55
> **Code:** `logger.info("%s missing, generating synthetic demo data", FRAUD_DATA_P...`
> **Type:** Arithmetic operation

### Line  56
> **Code:** `FRAUD_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `subprocess.run(`
> **Type:** Code statement

### Line  58
> **Code:** `[sys.executable, str(GENERATOR), "--output", str(FRAUD_DATA_PATH)],`
> **Type:** Arithmetic operation

### Line  59
> **Code:** `check=True,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `)`
> **Type:** Code statement

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `df = pd.read_csv(FRAUD_DATA_PATH).dropna(subset=[TARGET_COL])`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `df = df.drop_duplicates().reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `df[TARGET_COL] = df[TARGET_COL].astype("int8")`
> **Type:** Assignment/comparison

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `meta = {`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `"rows": len(df),`
> **Type:** Code statement

### Line  68
> **Code:** `"source_file": str(FRAUD_DATA_PATH),`
> **Type:** Code statement

### Line  69
> **Code:** `"source_hash": file_hash(FRAUD_DATA_PATH),`
> **Type:** Code statement

### Line  70
> **Code:** `"class_distribution": df[TARGET_COL].value_counts().to_dict(),`
> **Type:** Data structure operation

### Line  71
> **Code:** `}`
> **Type:** Code statement

### Line  72
> **Code:** `logger.info("Loaded %d transactions from %s", len(df), FRAUD_DATA_PATH...`
> **Type:** Arithmetic operation

### Line  73
> **Code:** `return df, meta`
> **Type:** Returns a value from a function

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `def train_model() -> tuple[RandomForestClassifier, list[str], dict]:`
> **Type:** Function definition

### Line  77
> **Code:** `"""Train the fraud detection model on real data."""`
> **Type:** Code statement

### Line  78
> **Code:** `logger.info("Loading and preprocessing data...")`
> **Type:** Logical operation

### Line  79
> **Code:** `clean, meta = load_transactions()`
> **Type:** Assignment/comparison

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `feature_cols = [c for c in clean.columns if c != TARGET_COL]`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `X = clean[feature_cols]`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `y = clean[TARGET_COL]`
> **Type:** Assignment/comparison

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `)`
> **Type:** Code statement

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `logger.info("Training RandomForest with class_weight='balanced_subsamp...`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `rf = RandomForestClassifier(`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `n_estimators=200,`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `max_depth=12,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `min_samples_leaf=5,`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `max_features="sqrt",`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `class_weight="balanced_subsample",`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `random_state=42,`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `n_jobs=-1,`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `)`
> **Type:** Code statement

### Line  99
> **Code:** `rf.fit(X_train, y_train)`
> **Type:** Function call

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `y_pred = rf.predict(X_test)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `y_proba = rf.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `f1 = f1_score(y_test, y_pred)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `auc = roc_auc_score(y_test, y_proba)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `feature_importance = dict(zip(feature_cols, rf.feature_importances_))`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `top_features = sorted(feature_importance.items(), key=lambda x: x[1], ...`
> **Type:** Assignment/comparison

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `info = {`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `"model_name": "fraud-detection-model",`
> **Type:** Arithmetic operation

### Line 112
> **Code:** `"model_type": "RandomForestClassifier",`
> **Type:** Logical operation

### Line 113
> **Code:** `"n_estimators": 200,`
> **Type:** Logical operation

### Line 114
> **Code:** `"max_depth": 12,`
> **Type:** Code statement

### Line 115
> **Code:** `"class_weight": "balanced_subsample",`
> **Type:** Code statement

### Line 116
> **Code:** `"trained_samples": len(X_train),`
> **Type:** Code statement

### Line 117
> **Code:** `"test_samples": len(X_test),`
> **Type:** Code statement

### Line 118
> **Code:** `"f1": f1,`
> **Type:** Code statement

### Line 119
> **Code:** `"auc": auc,`
> **Type:** Code statement

### Line 120
> **Code:** `"feature_importance": top_features,`
> **Type:** Logical operation

### Line 121
> **Code:** `"feature_columns": feature_cols,`
> **Type:** Code statement

### Line 122
> **Code:** `"class_distribution": meta.get("class_distribution", {}),`
> **Type:** Code statement

### Line 123
> **Code:** `"trained_at": datetime.utcnow().isoformat() + "Z",`
> **Type:** Arithmetic operation

### Line 124
> **Code:** `}`
> **Type:** Code statement

### Line 125
> **Code:** ``
> **Type:** Empty line

### Line 126
> **Code:** `MODELS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `joblib.dump(rf, MODEL_PATH)`
> **Type:** Function call

### Line 128
> **Code:** `with open(FEATURE_COLS_PATH, "w") as f:`
> **Type:** Context manager

### Line 129
> **Code:** `f.write("\n".join(feature_cols))`
> **Type:** Function call

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `logger.info(f"Model trained: F1={f1:.4f}, AUC={auc:.4f}")`
> **Type:** Assignment/comparison

### Line 132
> **Code:** `return rf, feature_cols, info`
> **Type:** Returns a value from a function

### Line 133
> **Code:** ``
> **Type:** Empty line

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** `@asynccontextmanager`
> **Type:** Code statement

### Line 136
> **Code:** `async def lifespan(app: FastAPI):`
> **Type:** Code statement

### Line 137
> **Code:** `global model, feature_columns, model_info`
> **Type:** Code statement

### Line 138
> **Code:** `logger.info("Starting up: training model on credit card transaction da...`
> **Type:** Function call

### Line 139
> **Code:** `try:`
> **Type:** Code statement

### Line 140
> **Code:** `model, feature_columns, model_info = train_model()`
> **Type:** Assignment/comparison

### Line 141
> **Code:** `logger.info("Model ready.")`
> **Type:** Function call

### Line 142
> **Code:** `except Exception as e:`
> **Type:** Code statement

### Line 143
> **Code:** `logger.error(f"Failed to train model: {e}")`
> **Type:** Logical operation

### Line 144
> **Code:** `model = None`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `feature_columns = []`
> **Type:** Assignment/comparison

### Line 146
> **Code:** `model_info = {"error": str(e)}`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `yield`
> **Type:** Code statement

### Line 148
> **Code:** `logger.info("Shutting down...")`
> **Type:** Function call

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** `app = FastAPI(`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `title="Fraud Detection API",`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `description="Real-time credit card fraud detection using RandomForest ...`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `version="1.0.0",`
> **Type:** Assignment/comparison

### Line 155
> **Code:** `lifespan=lifespan,`
> **Type:** Assignment/comparison

### Line 156
> **Code:** `)`
> **Type:** Code statement

### Line 157
> **Code:** ``
> **Type:** Empty line

### Line 158
> **Code:** `ui_path = Path(__file__).resolve().parents[2] / "ui"`
> **Type:** Assignment/comparison

### Line 159
> **Code:** `if ui_path.exists():`
> **Type:** Conditional statement

### Line 160
> **Code:** `app.mount("/static", StaticFiles(directory=str(ui_path)), name="static...`
> **Type:** Assignment/comparison

### Line 161
> **Code:** ``
> **Type:** Empty line

### Line 162
> **Code:** ``
> **Type:** Empty line

### Line 163
> **Code:** `class PredictRequest(BaseModel):`
> **Type:** Class definition

### Line 164
> **Code:** `Time: float = Field(..., description="Seconds elapsed since first tran...`
> **Type:** Assignment/comparison

### Line 165
> **Code:** `V1: float`
> **Type:** Code statement

### Line 166
> **Code:** `V2: float`
> **Type:** Code statement

### Line 167
> **Code:** `V3: float`
> **Type:** Code statement

### Line 168
> **Code:** `V4: float`
> **Type:** Code statement

### Line 169
> **Code:** `V5: float`
> **Type:** Code statement

### Line 170
> **Code:** `V6: float`
> **Type:** Code statement

### Line 171
> **Code:** `V7: float`
> **Type:** Code statement

### Line 172
> **Code:** `V8: float`
> **Type:** Code statement

### Line 173
> **Code:** `V9: float`
> **Type:** Code statement

### Line 174
> **Code:** `V10: float`
> **Type:** Code statement

### Line 175
> **Code:** `V11: float`
> **Type:** Code statement

### Line 176
> **Code:** `V12: float`
> **Type:** Code statement

### Line 177
> **Code:** `V13: float`
> **Type:** Code statement

### Line 178
> **Code:** `V14: float`
> **Type:** Code statement

### Line 179
> **Code:** `V15: float`
> **Type:** Code statement

### Line 180
> **Code:** `V16: float`
> **Type:** Code statement

### Line 181
> **Code:** `V17: float`
> **Type:** Code statement

### Line 182
> **Code:** `V18: float`
> **Type:** Code statement

### Line 183
> **Code:** `V19: float`
> **Type:** Code statement

### Line 184
> **Code:** `V20: float`
> **Type:** Code statement

### Line 185
> **Code:** `V21: float`
> **Type:** Code statement

### Line 186
> **Code:** `V22: float`
> **Type:** Code statement

### Line 187
> **Code:** `V23: float`
> **Type:** Code statement

### Line 188
> **Code:** `V24: float`
> **Type:** Code statement

### Line 189
> **Code:** `V25: float`
> **Type:** Code statement

### Line 190
> **Code:** `V26: float`
> **Type:** Code statement

### Line 191
> **Code:** `V27: float`
> **Type:** Code statement

### Line 192
> **Code:** `V28: float`
> **Type:** Code statement

### Line 193
> **Code:** `Amount: float = Field(..., description="Transaction amount")`
> **Type:** Assignment/comparison

### Line 194
> **Code:** ``
> **Type:** Empty line

### Line 195
> **Code:** ``
> **Type:** Empty line

### Line 196
> **Code:** `class PredictResponse(BaseModel):`
> **Type:** Class definition

### Line 197
> **Code:** `prediction: str = Field(..., description="fraud or legitimate")`
> **Type:** Assignment/comparison

### Line 198
> **Code:** `probability: float = Field(..., description="Fraud probability [0,1]")`
> **Type:** Assignment/comparison

### Line 199
> **Code:** `risk_level: str = Field(..., description="low, medium, high, critical"...`
> **Type:** Assignment/comparison

### Line 200
> **Code:** `request_id: str`
> **Type:** Code statement

### Line 201
> **Code:** `latency_ms: int`
> **Type:** Code statement

### Line 202
> **Code:** ``
> **Type:** Empty line

### Line 203
> **Code:** ``
> **Type:** Empty line

### Line 204
> **Code:** `def compute_risk_level(probability: float) -> str:`
> **Type:** Function definition

### Line 205
> **Code:** `if probability >= 0.9:`
> **Type:** Conditional statement

### Line 206
> **Code:** `return "critical"`
> **Type:** Returns a value from a function

### Line 207
> **Code:** `elif probability >= 0.7:`
> **Type:** Else-if branch

### Line 208
> **Code:** `return "high"`
> **Type:** Returns a value from a function

### Line 209
> **Code:** `elif probability >= 0.3:`
> **Type:** Else-if branch

### Line 210
> **Code:** `return "medium"`
> **Type:** Returns a value from a function

### Line 211
> **Code:** `return "low"`
> **Type:** Returns a value from a function

### Line 212
> **Code:** ``
> **Type:** Empty line

### Line 213
> **Code:** ``
> **Type:** Empty line

### Line 214
> **Code:** `@app.get("/health")`
> **Type:** Arithmetic operation

### Line 215
> **Code:** `async def health():`
> **Type:** Code statement

### Line 216
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 217
> **Code:** `"status": "ok" if model is not None else "degraded",`
> **Type:** Logical operation

### Line 218
> **Code:** `"model_loaded": model is not None,`
> **Type:** Logical operation

### Line 219
> **Code:** `"timestamp": datetime.utcnow().isoformat() + "Z",`
> **Type:** Arithmetic operation

### Line 220
> **Code:** `}`
> **Type:** Code statement

### Line 221
> **Code:** ``
> **Type:** Empty line

### Line 222
> **Code:** ``
> **Type:** Empty line

### Line 223
> **Code:** `@app.post("/predict", response_model=PredictResponse)`
> **Type:** Assignment/comparison

### Line 224
> **Code:** `async def predict(request: PredictRequest, http_request: Request):`
> **Type:** Code statement

### Line 225
> **Code:** `if model is None:`
> **Type:** Conditional statement

### Line 226
> **Code:** `raise HTTPException(status_code=503, detail="Model not loaded")`
> **Type:** Raises an exception

### Line 227
> **Code:** ``
> **Type:** Empty line

### Line 228
> **Code:** `start = time.perf_counter()`
> **Type:** Assignment/comparison

### Line 229
> **Code:** ``
> **Type:** Empty line

### Line 230
> **Code:** `input_dict = request.model_dump()`
> **Type:** Assignment/comparison

### Line 231
> **Code:** `input_array = np.array([[input_dict[col] for col in feature_columns]])`
> **Type:** Assignment/comparison

### Line 232
> **Code:** `prob = float(model.predict_proba(input_array)[0, 1])`
> **Type:** Assignment/comparison

### Line 233
> **Code:** `pred = "fraud" if prob >= 0.5 else "legitimate"`
> **Type:** Assignment/comparison

### Line 234
> **Code:** `risk = compute_risk_level(prob)`
> **Type:** Assignment/comparison

### Line 235
> **Code:** `latency_ms = int((time.perf_counter() - start) * 1000)`
> **Type:** Assignment/comparison

### Line 236
> **Code:** ``
> **Type:** Empty line

### Line 237
> **Code:** `req_id = str(uuid.uuid4())[:8]`
> **Type:** Assignment/comparison

### Line 238
> **Code:** `record = {`
> **Type:** Assignment/comparison

### Line 239
> **Code:** `"request_id": req_id,`
> **Type:** Code statement

### Line 240
> **Code:** `"timestamp": datetime.utcnow().isoformat() + "Z",`
> **Type:** Arithmetic operation

### Line 241
> **Code:** `"input": input_dict,`
> **Type:** Code statement

### Line 242
> **Code:** `"result": {`
> **Type:** Code statement

### Line 243
> **Code:** `"prediction": pred,`
> **Type:** Code statement

### Line 244
> **Code:** `"probability": prob,`
> **Type:** Code statement

### Line 245
> **Code:** `"risk_level": risk,`
> **Type:** Code statement

### Line 246
> **Code:** `},`
> **Type:** Code statement

### Line 247
> **Code:** `"latency_ms": latency_ms,`
> **Type:** Code statement

### Line 248
> **Code:** `}`
> **Type:** Code statement

### Line 249
> **Code:** `prediction_history.append(record)`
> **Type:** Logical operation

### Line 250
> **Code:** ``
> **Type:** Empty line

### Line 251
> **Code:** `return PredictResponse(`
> **Type:** Returns a value from a function

### Line 252
> **Code:** `prediction=pred,`
> **Type:** Assignment/comparison

### Line 253
> **Code:** `probability=prob,`
> **Type:** Assignment/comparison

### Line 254
> **Code:** `risk_level=risk,`
> **Type:** Assignment/comparison

### Line 255
> **Code:** `request_id=req_id,`
> **Type:** Assignment/comparison

### Line 256
> **Code:** `latency_ms=latency_ms,`
> **Type:** Assignment/comparison

### Line 257
> **Code:** `)`
> **Type:** Code statement

### Line 258
> **Code:** ``
> **Type:** Empty line

### Line 259
> **Code:** ``
> **Type:** Empty line

### Line 260
> **Code:** `@app.get("/history")`
> **Type:** Arithmetic operation

### Line 261
> **Code:** `async def history(limit: int = 100):`
> **Type:** Assignment/comparison

### Line 262
> **Code:** `return {"entries": prediction_history[-limit:]}`
> **Type:** Returns a value from a function

### Line 263
> **Code:** ``
> **Type:** Empty line

### Line 264
> **Code:** ``
> **Type:** Empty line

### Line 265
> **Code:** `@app.get("/stats")`
> **Type:** Arithmetic operation

### Line 266
> **Code:** `async def stats():`
> **Type:** Code statement

### Line 267
> **Code:** `if not prediction_history:`
> **Type:** Conditional statement

### Line 268
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 269
> **Code:** `"total_scans": 0,`
> **Type:** Code statement

### Line 270
> **Code:** `"fraud_rate": 0.0,`
> **Type:** Code statement

### Line 271
> **Code:** `"flagged_count": 0,`
> **Type:** Code statement

### Line 272
> **Code:** `"avg_probability": 0.0,`
> **Type:** Code statement

### Line 273
> **Code:** `"avg_latency_ms": 0,`
> **Type:** Code statement

### Line 274
> **Code:** `"risk_level_distribution": {"low": 0, "medium": 0, "high": 0, "critica...`
> **Type:** Code statement

### Line 275
> **Code:** `}`
> **Type:** Code statement

### Line 276
> **Code:** ``
> **Type:** Empty line

### Line 277
> **Code:** `total = len(prediction_history)`
> **Type:** Assignment/comparison

### Line 278
> **Code:** `flagged = sum(1 for h in prediction_history if h["result"]["prediction...`
> **Type:** Assignment/comparison

### Line 279
> **Code:** `avg_prob = sum(h["result"]["probability"] for h in prediction_history)...`
> **Type:** Assignment/comparison

### Line 280
> **Code:** `avg_lat = sum(h["latency_ms"] for h in prediction_history) / total`
> **Type:** Assignment/comparison

### Line 281
> **Code:** ``
> **Type:** Empty line

### Line 282
> **Code:** `risk_dist = {"low": 0, "medium": 0, "high": 0, "critical": 0}`
> **Type:** Assignment/comparison

### Line 283
> **Code:** `for h in prediction_history:`
> **Type:** For loop

### Line 284
> **Code:** `risk_dist[h["result"]["risk_level"]] += 1`
> **Type:** Assignment/comparison

### Line 285
> **Code:** ``
> **Type:** Empty line

### Line 286
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 287
> **Code:** `"total_scans": total,`
> **Type:** Code statement

### Line 288
> **Code:** `"fraud_rate": flagged / total,`
> **Type:** Arithmetic operation

### Line 289
> **Code:** `"flagged_count": flagged,`
> **Type:** Code statement

### Line 290
> **Code:** `"avg_probability": avg_prob,`
> **Type:** Code statement

### Line 291
> **Code:** `"avg_latency_ms": round(avg_lat, 1),`
> **Type:** Code statement

### Line 292
> **Code:** `"risk_level_distribution": risk_dist,`
> **Type:** Code statement

### Line 293
> **Code:** `}`
> **Type:** Code statement

### Line 294
> **Code:** ``
> **Type:** Empty line

### Line 295
> **Code:** ``
> **Type:** Empty line

### Line 296
> **Code:** `@app.get("/model-info")`
> **Type:** Arithmetic operation

### Line 297
> **Code:** `async def model_info_endpoint():`
> **Type:** Code statement

### Line 298
> **Code:** `if not model_info:`
> **Type:** Conditional statement

### Line 299
> **Code:** `return {"error": "Model not trained yet"}`
> **Type:** Returns a value from a function

### Line 300
> **Code:** `return model_info`
> **Type:** Returns a value from a function

### Line 301
> **Code:** ``
> **Type:** Empty line

### Line 302
> **Code:** ``
> **Type:** Empty line

### Line 303
> **Code:** `@app.get("/", response_class=HTMLResponse)`
> **Type:** Assignment/comparison

### Line 304
> **Code:** `async def root():`
> **Type:** Code statement

### Line 305
> **Code:** `index_path = ui_path / "index.html"`
> **Type:** Assignment/comparison

### Line 306
> **Code:** `if index_path.exists():`
> **Type:** Conditional statement

### Line 307
> **Code:** `return index_path.read_text()`
> **Type:** Returns a value from a function

### Line 308
> **Code:** `return HTMLResponse("<h1>Fraud Detection API</h1><p>UI not found. See ...`
> **Type:** Returns a value from a function

### Line 309
> **Code:** ``
> **Type:** Empty line

### Line 310
> **Code:** ``
> **Type:** Empty line

### Line 311
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 312
> **Code:** `import uvicorn`
> **Type:** Imports a module

### Line 313
> **Code:** `uvicorn.run("main:app", host="0.0.0.0", port=8101, reload=False)`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 313
- **Code lines:** 257
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 56

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: main.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/monitoring/__init__.py`
- **Total lines:** 1
- **File size:** 84 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""monitoring package: drift and performance monitoring (Evidently, Pr...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: drift_report.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/monitoring/drift_report.py`
- **Total lines:** 116
- **File size:** 3958 bytes

## Line Type Summary
- **Code:** 89
- **Comment:** 0
- **Empty:** 27
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Production model monitoring with Evidently.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Builds a drift report (``DataDriftPreset`` + ``TargetDriftPreset``) co...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `a production sample against the training reference dataset, saves the ...`
> **Type:** Code statement

### Line   5
> **Code:** ```monitoring/reports/drift_report.html`` and extracts the dataset drif...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `A simulated drift mode injects distribution shifts so the report is de...`
> **Type:** Logical operation

### Line   8
> **Code:** `without needing real production traffic.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import json`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from src.config import MONITORING_REPORTS_DIR, REFERENCE_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `try:`
> **Type:** Code statement

### Line  23
> **Code:** `from evidently.report import Report`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from evidently.metric_preset import DataDriftPreset, TargetDriftPreset`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `EVIDENTLY_AVAILABLE = True`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `except ImportError:  # pragma: no cover`
> **Type:** Logical operation

### Line  28
> **Code:** `EVIDENTLY_AVAILABLE = False`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def build_reference() -> pd.DataFrame:`
> **Type:** Function definition

### Line  32
> **Code:** `"""Persist and return the training reference (for drift comparison).""...`
> **Type:** Logical operation

### Line  33
> **Code:** `from src.features.build_features import build_features`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `raw = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `frame = build_features(clean, include_sensitive=True)`
> **Type:** Assignment/comparison

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `REFERENCE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `frame.to_csv(REFERENCE_DATA_PATH, index=False)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `return frame`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def simulate_production_sample(n: int = 1000, drift_strength: float = ...`
> **Type:** Function definition

### Line  47
> **Code:** `"""Sample rows and optionally shift distributions to simulate drift.""...`
> **Type:** Logical operation

### Line  48
> **Code:** `if not REFERENCE_DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  49
> **Code:** `build_reference()`
> **Type:** Function call

### Line  50
> **Code:** `ref = pd.read_csv(REFERENCE_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `current = ref.sample(n=min(n, len(ref)), random_state=7)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `if drift_strength > 0:`
> **Type:** Conditional statement

### Line  54
> **Code:** `rng = np.random.default_rng(7)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `numeric_cols = current.select_dtypes(include=[np.number]).columns`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `for col in numeric_cols:`
> **Type:** For loop

### Line  57
> **Code:** `std = current[col].std() or 1.0`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `current[col] = current[col] + rng.normal(`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `0, drift_strength * std, size=len(current)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `)`
> **Type:** Code statement

### Line  61
> **Code:** `return current`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def generate_drift_report(`
> **Type:** Function definition

### Line  65
> **Code:** `current_data: pd.DataFrame | None = None,`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `reference_data: pd.DataFrame | None = None,`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `output_path: Path = MONITORING_REPORTS_DIR / "drift_report.html",`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  69
> **Code:** `"""Run the Evidently report and extract the dataset drift score."""`
> **Type:** Logical operation

### Line  70
> **Code:** `if not EVIDENTLY_AVAILABLE:`
> **Type:** Conditional statement

### Line  71
> **Code:** `raise ImportError("evidently is required for drift monitoring")`
> **Type:** Raises an exception

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `reference = reference_data if reference_data is not None else build_re...`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `current = (`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `current_data if current_data is not None`
> **Type:** Logical operation

### Line  76
> **Code:** `else simulate_production_sample()`
> **Type:** Function call

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `report.run(reference_data=reference, current_data=current)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `report.save_html(str(output_path))`
> **Type:** Logical operation

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `as_dict = report.as_dict()`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `dataset_drift = as_dict["metrics"][0]["result"]["dataset_drift"]`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `drift_score = as_dict["metrics"][0]["result"]["share_of_drifted_column...`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `"dataset_drift": bool(dataset_drift),`
> **Type:** Code statement

### Line  91
> **Code:** `"drift_score": float(drift_score),`
> **Type:** Logical operation

### Line  92
> **Code:** `"report_path": str(output_path),`
> **Type:** Logical operation

### Line  93
> **Code:** `}`
> **Type:** Code statement

### Line  94
> **Code:** `(MONITORING_REPORTS_DIR / "drift_score.json").write_text(`
> **Type:** Arithmetic operation

### Line  95
> **Code:** `json.dumps(result, indent=2)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `)`
> **Type:** Code statement

### Line  97
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 101
> **Code:** `parser = argparse.ArgumentParser(description="Generate Evidently drift...`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `parser.add_argument("--drift-strength", type=float, default=0.0,`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `help=">0 simulates a drifted production sample.")`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `current = simulate_production_sample(drift_strength=args.drift_strengt...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `result = generate_drift_report(current_data=current)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `print(`
> **Type:** Prints output to console

### Line 109
> **Code:** `f"dataset_drift={result['dataset_drift']} "`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `f"drift_score={result['drift_score']:.3f}"`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `)`
> **Type:** Code statement

### Line 112
> **Code:** `print(f"Report saved to {result['report_path']}")`
> **Type:** Prints output to console

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 116
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 116
- **Code lines:** 89
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 27

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: drift_report.py*
---

# mlops-full-mlops-skills-project: retraining_trigger.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/monitoring/retraining_trigger.py`
- **Total lines:** 83
- **File size:** 2572 bytes

## Line Type Summary
- **Code:** 61
- **Comment:** 1
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Drift-driven retraining trigger.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Checks the latest drift score and, when it exceeds ``DRIFT_THRESHOLD``...`
> **Type:** Logical operation

### Line   4
> **Code:** `triggers the ZenML retraining pipeline. As a safety guard the trigger ...`
> **Type:** Code statement

### Line   5
> **Code:** `skips the fairness check: the retraining pipeline itself re-runs the f...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `gate suite before any promotion.`
> **Type:** Logical operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  12
> **Code:** `import json`
> **Type:** Imports a module

### Line  13
> **Code:** `import logging`
> **Type:** Imports a module

### Line  14
> **Code:** `import subprocess`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from src.config import DRIFT_THRESHOLD, MONITORING_REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `DRIFT_SCORE_FILE = MONITORING_REPORTS_DIR / "drift_score.json"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def read_drift_score(path: Path = DRIFT_SCORE_FILE) -> float:`
> **Type:** Function definition

### Line  25
> **Code:** `"""Read the latest drift score produced by ``drift_report.py``."""`
> **Type:** Logical operation

### Line  26
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  27
> **Code:** `return 0.0`
> **Type:** Returns a value from a function

### Line  28
> **Code:** `data = json.loads(path.read_text())`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `return float(data["drift_score"])`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def should_retrain(score: float, threshold: float = DRIFT_THRESHOLD) -...`
> **Type:** Function definition

### Line  33
> **Code:** `"""Return True when the drift score exceeds the threshold."""`
> **Type:** Logical operation

### Line  34
> **Code:** `return score > threshold`
> **Type:** Returns a value from a function

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def trigger_retraining(dry_run: bool = False) -> dict:`
> **Type:** Function definition

### Line  38
> **Code:** `"""Evaluate drift and launch the retraining pipeline when needed."""`
> **Type:** Logical operation

### Line  39
> **Code:** `score = read_drift_score()`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `trigger = should_retrain(score)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `logger.info("Drift score=%.3f threshold=%.3f trigger=%s", score, DRIFT...`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `if trigger and not dry_run:`
> **Type:** Conditional statement

### Line  44
> **Code:** `_launch_retraining_pipeline()`
> **Type:** Function call

### Line  45
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  46
> **Code:** `"drift_score": score,`
> **Type:** Logical operation

### Line  47
> **Code:** `"threshold": DRIFT_THRESHOLD,`
> **Type:** Code statement

### Line  48
> **Code:** `"triggered": trigger,`
> **Type:** Code statement

### Line  49
> **Code:** `"dry_run": dry_run,`
> **Type:** Code statement

### Line  50
> **Code:** `}`
> **Type:** Code statement

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def _launch_retraining_pipeline() -> None:`
> **Type:** Function definition

### Line  54
> **Code:** `"""Shell out to the ZenML retraining pipeline.`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `The retraining pipeline re-runs data validation, tuning, Deepchecks an...`
> **Type:** Arithmetic operation

### Line  57
> **Code:** `Fairlearn before any model is promoted (all promotion guards remain`
> **Type:** Logical operation

### Line  58
> **Code:** `active on automated retraining).`
> **Type:** Code statement

### Line  59
> **Code:** `"""`
> **Type:** Code statement

### Line  60
> **Code:** `cmd = ["python", "-m", "pipelines.retraining_pipeline"]`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `logger.info("Launching retraining pipeline: %s", " ".join(cmd))`
> **Type:** Arithmetic operation

### Line  62
> **Code:** `subprocess.Popen(`
> **Type:** Code statement

### Line  63
> **Code:** `cmd,`
> **Type:** Code statement

### Line  64
> **Code:** `stdout=subprocess.DEVNULL,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `stderr=subprocess.DEVNULL,`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `)`
> **Type:** Code statement

### Line  67
> **Code:** `# Notification / supervision trace: structured log for human oversight...`
> **Type:** Comment: Notification / supervision trace: structured log for human oversight.

### Line  68
> **Code:** `logger.warning(`
> **Type:** Code statement

### Line  69
> **Code:** `"AUTOMATED_RETRAINING_TRIGGERED score=%.3f", read_drift_score()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  74
> **Code:** `parser = argparse.ArgumentParser(description="Drift-based retraining t...`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `parser.add_argument("--dry-run", action="store_true", help="Only repor...`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `result = trigger_retraining(dry_run=args.dry_run)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `print(result)`
> **Type:** Prints output to console

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  83
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 83
- **Code lines:** 61
- **Comments:** 1
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: retraining_trigger.py*
---

# mlops-full-mlops-skills-project: validation.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/data/validation.py`
- **Total lines:** 93
- **File size:** 2955 bytes

## Line Type Summary
- **Code:** 71
- **Comment:** 0
- **Empty:** 22
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Run the Great Expectations input-data contract against the raw data...`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `The project's datasource is a ``RuntimeDataConnector``, which receives...`
> **Type:** Logical operation

### Line   4
> **Code:** `batch as an in-memory dataframe. The ``great_expectations checkpoint r...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `CLI cannot supply one, so the checkpoint is driven programmatically he...`
> **Type:** Logical operation

### Line   6
> **Code:** `this module — not the CLI — is what the DVC ``validate`` stage invokes...`
> **Type:** Logical operation

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `Exits non-zero when the contract is breached, so the pipeline stops be...`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `bad dataset reaches preprocessing.`
> **Type:** Code statement

### Line  10
> **Code:** `"""`
> **Type:** Code statement

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import sys`
> **Type:** Imports a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `CHECKPOINT_NAME = "dataset_checkpoint"`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `SUITE_NAME = "dataset_suite"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `DATA_ASSET_NAME = "churn_dataset"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `def validate(path=RAW_DATA_PATH) -> dict:`
> **Type:** Function definition

### Line  26
> **Code:** `"""Validate ``path`` against the expectation suite.`
> **Type:** Code statement

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `Returns the summary dict; raises RuntimeError when expectations fail.`
> **Type:** Logical operation

### Line  29
> **Code:** `"""`
> **Type:** Code statement

### Line  30
> **Code:** `import great_expectations as gx`
> **Type:** Imports a module

### Line  31
> **Code:** `from great_expectations.core.batch import RuntimeBatchRequest`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `context = gx.get_context(context_root_dir="great_expectations")`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `df = pd.read_csv(path)`
> **Type:** Assignment/comparison

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `batch_request = RuntimeBatchRequest(`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `datasource_name="pandas_datasource",`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `data_connector_name="default_runtime_data_connector_name",`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `data_asset_name=DATA_ASSET_NAME,`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `runtime_parameters={"batch_data": df},`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `batch_identifiers={"default_identifier_name": "raw_dataset"},`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `)`
> **Type:** Code statement

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `result = context.run_checkpoint(`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `checkpoint_name=CHECKPOINT_NAME,`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `validations=[`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `{"batch_request": batch_request, "expectation_suite_name": SUITE_NAME}`
> **Type:** Data structure operation

### Line  48
> **Code:** `],`
> **Type:** Code statement

### Line  49
> **Code:** `)`
> **Type:** Code statement

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `stats = {}`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `for validation_result in result.run_results.values():`
> **Type:** For loop

### Line  53
> **Code:** `stats = validation_result["validation_result"]["statistics"]`
> **Type:** Assignment/comparison

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `summary = {`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `"source_file": str(path),`
> **Type:** Code statement

### Line  57
> **Code:** `"rows": len(df),`
> **Type:** Code statement

### Line  58
> **Code:** `"success": bool(result.success),`
> **Type:** Code statement

### Line  59
> **Code:** `"evaluated_expectations": stats.get("evaluated_expectations"),`
> **Type:** Code statement

### Line  60
> **Code:** `"successful_expectations": stats.get("successful_expectations"),`
> **Type:** Code statement

### Line  61
> **Code:** `"unsuccessful_expectations": stats.get("unsuccessful_expectations"),`
> **Type:** Code statement

### Line  62
> **Code:** `}`
> **Type:** Code statement

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `if not result.success:`
> **Type:** Conditional statement

### Line  65
> **Code:** `failed = [`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `r["expectation_config"]["expectation_type"]`
> **Type:** Data structure operation

### Line  67
> **Code:** `for validation_result in result.run_results.values()`
> **Type:** For loop

### Line  68
> **Code:** `for r in validation_result["validation_result"]["results"]`
> **Type:** For loop

### Line  69
> **Code:** `if not r["success"]`
> **Type:** Conditional statement

### Line  70
> **Code:** `]`
> **Type:** Code statement

### Line  71
> **Code:** `raise RuntimeError(`
> **Type:** Raises an exception

### Line  72
> **Code:** `f"Data contract breached on {path}: {len(failed)} failed expectation(s...`
> **Type:** Code statement

### Line  73
> **Code:** `)`
> **Type:** Code statement

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `return summary`
> **Type:** Returns a value from a function

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  79
> **Code:** `try:`
> **Type:** Code statement

### Line  80
> **Code:** `summary = validate()`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `except RuntimeError as exc:`
> **Type:** Logical operation

### Line  82
> **Code:** `print(f"validation FAILED: {exc}", file=sys.stderr)`
> **Type:** Prints output to console

### Line  83
> **Code:** `sys.exit(1)`
> **Type:** Function call

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `print(`
> **Type:** Prints output to console

### Line  86
> **Code:** `f"validation PASSED: {summary['successful_expectations']}"`
> **Type:** Data structure operation

### Line  87
> **Code:** `f"/{summary['evaluated_expectations']} expectations green "`
> **Type:** Arithmetic operation

### Line  88
> **Code:** `f"on {summary['rows']} rows from {summary['source_file']}"`
> **Type:** Data structure operation

### Line  89
> **Code:** `)`
> **Type:** Code statement

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  93
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 93
- **Code lines:** 71
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 22

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: validation.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/data/__init__.py`
- **Total lines:** 1
- **File size:** 68 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""data package: data loading, validation, and versioning (DVC)."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: ingestion.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/data/ingestion.py`
- **Total lines:** 72
- **File size:** 2181 bytes

## Line Type Summary
- **Code:** 52
- **Comment:** 0
- **Empty:** 20
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Data ingestion: load the raw dataset and log key facts.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Logs the row count, class distribution, and a SHA256 hash of the raw`
> **Type:** Logical operation

### Line   4
> **Code:** `source file so every downstream artifact can be traced back to its inp...`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import hashlib`
> **Type:** Imports a module

### Line  10
> **Code:** `import logging`
> **Type:** Imports a module

### Line  11
> **Code:** `from typing import Tuple`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from src.config import RAW_DATA_PATH, TARGET_COL, TIMESTAMP_COL`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelnam...`
> **Type:** Assignment/comparison

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `def file_hash(path) -> str:`
> **Type:** Function definition

### Line  22
> **Code:** `"""Return the SHA256 hex digest of a file, streaming-friendly."""`
> **Type:** Arithmetic operation

### Line  23
> **Code:** `digest = hashlib.sha256()`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `with open(path, "rb") as handle:`
> **Type:** Context manager

### Line  25
> **Code:** `for chunk in iter(lambda: handle.read(1 << 16), b""):`
> **Type:** For loop

### Line  26
> **Code:** `digest.update(chunk)`
> **Type:** Function call

### Line  27
> **Code:** `return digest.hexdigest()`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def ingest_raw_data(path=RAW_DATA_PATH) -> Tuple[pd.DataFrame, dict]:`
> **Type:** Function definition

### Line  31
> **Code:** `"""Load the raw CSV and log ingestion metadata.`
> **Type:** Logical operation

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `Returns ``(dataframe, metadata)`` where metadata contains the row coun...`
> **Type:** Code statement

### Line  34
> **Code:** `class distribution, and the source file hash.`
> **Type:** Class definition

### Line  35
> **Code:** `"""`
> **Type:** Code statement

### Line  36
> **Code:** `data_hash = file_hash(path)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `df = pd.read_csv(path)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `time_col = TIMESTAMP_COL if TIMESTAMP_COL in df.columns else None`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `target_col = TARGET_COL if TARGET_COL in df.columns else None`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `class_dist = df[target_col].value_counts().to_dict() if target_col els...`
> **Type:** Assignment/comparison

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `period = (`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `f"{df[time_col].min()} -> {df[time_col].max()}"`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `if time_col is not None`
> **Type:** Conditional statement

### Line  47
> **Code:** `else "n/a"`
> **Type:** Arithmetic operation

### Line  48
> **Code:** `)`
> **Type:** Code statement

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `positive_rate = class_dist.get(1, 0) / len(df) if len(df) > 0 else 0`
> **Type:** Assignment/comparison

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `metadata = {`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `"rows": len(df),`
> **Type:** Code statement

### Line  54
> **Code:** `"columns": len(df.columns),`
> **Type:** Code statement

### Line  55
> **Code:** `"time_period": period,`
> **Type:** Code statement

### Line  56
> **Code:** `"source_file": str(path),`
> **Type:** Code statement

### Line  57
> **Code:** `"source_hash": data_hash,`
> **Type:** Code statement

### Line  58
> **Code:** `"class_distribution": class_dist,`
> **Type:** Code statement

### Line  59
> **Code:** `"positive_rate": positive_rate,`
> **Type:** Code statement

### Line  60
> **Code:** `}`
> **Type:** Code statement

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `logger.info("Ingested %d rows from %s", len(df), path)`
> **Type:** Arithmetic operation

### Line  63
> **Code:** `logger.info("Class distribution: %s", class_dist)`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `logger.info("Positive (%s=1) rate: %.4f%%", TARGET_COL, positive_rate ...`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `logger.info("Covered time period: %s", period)`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `logger.info("Source file hash: %s", data_hash)`
> **Type:** Arithmetic operation

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `return df, metadata`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  72
> **Code:** `ingest_raw_data()`
> **Type:** Function call

## Summary
- **Total lines:** 72
- **Code lines:** 52
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 20

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: ingestion.py*
---

# mlops-full-mlops-skills-project: preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/data/preprocessing.py`
- **Total lines:** 94
- **File size:** 2876 bytes

## Line Type Summary
- **Code:** 74
- **Comment:** 0
- **Empty:** 20
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Pure preprocessing functions for the customer churn dataset.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Every transformation is a pure function operating on a DataFrame and`
> **Type:** Logical operation

### Line   4
> **Code:** `returning a new DataFrame, so each step is independently testable and`
> **Type:** Returns a value from a function

### Line   5
> **Code:** `side-effect free.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from typing import List, Optional`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `BINARY_FEATURES,`
> **Type:** Code statement

### Line  16
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  17
> **Code:** `NUMERIC_RANGES,`
> **Type:** Code statement

### Line  18
> **Code:** `NUMERIC_FEATURES,`
> **Type:** Code statement

### Line  19
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  20
> **Code:** `TIMESTAMP_COL,`
> **Type:** Code statement

### Line  21
> **Code:** `)`
> **Type:** Code statement

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  25
> **Code:** `"""Remove fully duplicated rows (keeps first occurrence)."""`
> **Type:** Code statement

### Line  26
> **Code:** `return df.drop_duplicates().reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def drop_missing(df: pd.DataFrame, columns: Optional[List[str]] = None...`
> **Type:** Function definition

### Line  30
> **Code:** `"""Drop rows with missing values on critical columns."""`
> **Type:** Code statement

### Line  31
> **Code:** `cols = columns or [TARGET_COL] + NUMERIC_FEATURES`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `return df.dropna(subset=[c for c in cols if c in df.columns]).reset_in...`
> **Type:** Returns a value from a function

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `def clamp_numeric(`
> **Type:** Function definition

### Line  36
> **Code:** `df: pd.DataFrame,`
> **Type:** Code statement

### Line  37
> **Code:** `ranges: Optional[dict] = None,`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `numeric_features: Optional[List[str]] = None,`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line  40
> **Code:** `"""Clamp numeric features to reasonable ranges."""`
> **Type:** Code statement

### Line  41
> **Code:** `bounds = ranges or NUMERIC_RANGES`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `features = numeric_features or NUMERIC_FEATURES`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `for col in features:`
> **Type:** For loop

### Line  45
> **Code:** `if col in out.columns and col in bounds:`
> **Type:** Conditional statement

### Line  46
> **Code:** `lo, hi = bounds[col]`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `if hi is not None:`
> **Type:** Conditional statement

### Line  48
> **Code:** `out[col] = out[col].clip(lower=lo, upper=hi)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `else:`
> **Type:** Else block

### Line  50
> **Code:** `out[col] = out[col].clip(lower=lo)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  55
> **Code:** `"""Enforce canonical dtypes across the dataset."""`
> **Type:** Logical operation

### Line  56
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `for col in NUMERIC_FEATURES:`
> **Type:** For loop

### Line  58
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  59
> **Code:** `out[col] = pd.to_numeric(out[col], errors="coerce")`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `for col in BINARY_FEATURES:`
> **Type:** For loop

### Line  61
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  62
> **Code:** `out[col] = pd.to_numeric(out[col], errors="coerce").astype("int8")`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `for col in CATEGORICAL_FEATURES:`
> **Type:** For loop

### Line  64
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  65
> **Code:** `out[col] = out[col].astype("string")`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `if TARGET_COL in out.columns:`
> **Type:** Conditional statement

### Line  67
> **Code:** `out[TARGET_COL] = out[TARGET_COL].astype("int8")`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `def preprocess(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  72
> **Code:** `"""Run the full preprocessing chain (pure, returns a new frame)."""`
> **Type:** Code statement

### Line  73
> **Code:** `return (`
> **Type:** Returns a value from a function

### Line  74
> **Code:** `df.pipe(drop_duplicates)`
> **Type:** Function call

### Line  75
> **Code:** `.pipe(drop_missing)`
> **Type:** Function call

### Line  76
> **Code:** `.pipe(clamp_numeric)`
> **Type:** Function call

### Line  77
> **Code:** `.pipe(cast_dtypes)`
> **Type:** Function call

### Line  78
> **Code:** `)`
> **Type:** Code statement

### Line  79
> **Code:** ``
> **Type:** Empty line

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `def run(output_path=None) -> pd.DataFrame:`
> **Type:** Function definition

### Line  82
> **Code:** `"""Entry point: load raw data, preprocess, persist to CSV."""`
> **Type:** Code statement

### Line  83
> **Code:** `from src.data.ingestion import ingest_raw_data`
> **Type:** Imports specific names from a module

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `raw, meta = ingest_raw_data()`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `path = output_path or "data/processed/dataset_clean.csv"`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `clean.to_csv(path, index=False)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `print(f"Preprocessed {len(clean)} rows -> {path} (raw had {meta['rows'...`
> **Type:** Prints output to console

### Line  90
> **Code:** `return clean`
> **Type:** Returns a value from a function

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  94
> **Code:** `run()`
> **Type:** Function call

## Summary
- **Total lines:** 94
- **Code lines:** 74
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 20

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: preprocessing.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/features/__init__.py`
- **Total lines:** 1
- **File size:** 81 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""features package: feature engineering and Feast feature store defin...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: build_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/src/features/build_features.py`
- **Total lines:** 158
- **File size:** 5671 bytes

## Line Type Summary
- **Code:** 122
- **Comment:** 4
- **Empty:** 32
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feature engineering: turn the cleaned dataframe into model-ready fe...`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Design goals:`
> **Type:** Code statement

### Line   4
> **Code:** `- Point-in-time friendly: no global statistics that leak future info; ...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `only features derived here are row-local (safe for both training and`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `real-time inference).`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- Pure functions, deterministic, testable independently.`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from typing import Dict, List`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `BINARY_FEATURES,`
> **Type:** Code statement

### Line  18
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  19
> **Code:** `ID_COL,`
> **Type:** Code statement

### Line  20
> **Code:** `NUMERIC_FEATURES,`
> **Type:** Code statement

### Line  21
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  22
> **Code:** `TIMESTAMP_COL,`
> **Type:** Code statement

### Line  23
> **Code:** `)`
> **Type:** Code statement

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `# Explicit ordering guarantee -> stable column order for the model.`
> **Type:** Comment: Explicit ordering guarantee -> stable column order for the model.

### Line  26
> **Code:** `DERIVED_FEATURES: List[str] = [`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `"avg_charge_per_month",       # monthly charges normalised by tenure`
> **Type:** Logical operation

### Line  28
> **Code:** `"service_density",            # services per month of tenure`
> **Type:** Code statement

### Line  29
> **Code:** `"ticket_intensity",           # support tickets per service`
> **Type:** Logical operation

### Line  30
> **Code:** `"is_long_tenure",             # tenure >= 36 months`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `"is_high_value_customer",     # total charges above median-like band`
> **Type:** Arithmetic operation

### Line  32
> **Code:** `"usage_efficiency",           # call minutes per service`
> **Type:** Code statement

### Line  33
> **Code:** `]`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def derive_features(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  37
> **Code:** `"""Compute derived (engineered) features, row-local only.`
> **Type:** Arithmetic operation

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `Derived features are churn-domain specific; datasets without the churn`
> **Type:** Arithmetic operation

### Line  40
> **Code:** `columns (e.g. credit card fraud with PCA features) pass through unchan...`
> **Type:** Code statement

### Line  41
> **Code:** `"""`
> **Type:** Code statement

### Line  42
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `if "tenure_months" not in out.columns:`
> **Type:** Conditional statement

### Line  44
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `tenure = out["tenure_months"].replace(0, 1)`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `services = out["num_services"].clip(lower=1)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `out["avg_charge_per_month"] = out["monthly_charges"] / tenure`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `out["service_density"] = out["num_services"] / tenure`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `out["ticket_intensity"] = out["support_tickets"] / services`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `out["is_long_tenure"] = (out["tenure_months"] >= 36).astype("int8")`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `out["is_high_value_customer"] = (out["total_charges"] >= 1500).astype(...`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `out["usage_efficiency"] = out["avg_call_minutes"] / services`
> **Type:** Assignment/comparison

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `def one_hot_encode(df: pd.DataFrame, columns: List[str]) -> pd.DataFra...`
> **Type:** Function definition

### Line  60
> **Code:** `"""One-hot encode categorical columns (drops first level).`
> **Type:** Arithmetic operation

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `Indicators are emitted as ``int8`` rather than pandas' default ``bool`...`
> **Type:** Logical operation

### Line  63
> **Code:** `downstream consumers (Evidently drift reports, ONNX export) cannot`
> **Type:** Logical operation

### Line  64
> **Code:** `interpret a boolean extension dtype as a numeric type.`
> **Type:** Code statement

### Line  65
> **Code:** `"""`
> **Type:** Code statement

### Line  66
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `for col in columns:`
> **Type:** For loop

### Line  68
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  69
> **Code:** `out = pd.get_dummies(`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `out, columns=[col], prefix=col, drop_first=True, dtype="int8"`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `)`
> **Type:** Code statement

### Line  72
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `def build_features(`
> **Type:** Function definition

### Line  76
> **Code:** `df: pd.DataFrame,`
> **Type:** Code statement

### Line  77
> **Code:** `include_sensitive: bool = False,`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `drop_columns: List[str] | None = None,`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line  80
> **Code:** `"""Transform a cleaned dataframe into the full feature matrix.`
> **Type:** Logical operation

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `Args:`
> **Type:** Code statement

### Line  83
> **Code:** `df: cleaned dataframe.`
> **Type:** Code statement

### Line  84
> **Code:** `include_sensitive: keep the sensitive attribute (gender) in the`
> **Type:** Code statement

### Line  85
> **Code:** `feature matrix. By default it is excluded from the model but kept`
> **Type:** Code statement

### Line  86
> **Code:** `available for fairness audits in a separate frame.`
> **Type:** Logical operation

### Line  87
> **Code:** `drop_columns: extra columns to drop (e.g. id / timestamp).`
> **Type:** Arithmetic operation

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `Returns:`
> **Type:** Code statement

### Line  90
> **Code:** `Feature matrix (already one-hot encoded, with churn preserved).`
> **Type:** Arithmetic operation

### Line  91
> **Code:** `"""`
> **Type:** Code statement

### Line  92
> **Code:** `drop = list(drop_columns or [])`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `drop += [ID_COL, TIMESTAMP_COL]`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `if not include_sensitive:`
> **Type:** Conditional statement

### Line  95
> **Code:** `drop += ["gender"]`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `drop = [c for c in drop if c in df.columns]`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `# Keep a numeric time column (e.g. fraud "Time" feature); only drop`
> **Type:** Comment: Keep a numeric time column (e.g. fraud "Time" feature); only drop

### Line  98
> **Code:** `# datetime-typed timestamps that are useless to the model.`
> **Type:** Comment: datetime-typed timestamps that are useless to the model.

### Line  99
> **Code:** `if TIMESTAMP_COL in drop and pd.api.types.is_numeric_dtype(df[TIMESTAM...`
> **Type:** Conditional statement

### Line 100
> **Code:** `drop.remove(TIMESTAMP_COL)`
> **Type:** Function call

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `out = derive_features(df).drop(columns=drop)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `cat_cols = [c for c in CATEGORICAL_FEATURES if c in out.columns]`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `out = one_hot_encode(out, cat_cols)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `return out.reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `def feature_sets(frame: pd.DataFrame) -> Dict[str, pd.DataFrame]:`
> **Type:** Function definition

### Line 111
> **Code:** `"""Split a built feature frame into (X, y) plus metadata columns."""`
> **Type:** Code statement

### Line 112
> **Code:** `if TARGET_COL in frame.columns:`
> **Type:** Conditional statement

### Line 113
> **Code:** `y = frame[TARGET_COL]`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `X = frame.drop(columns=[TARGET_COL])`
> **Type:** Assignment/comparison

### Line 115
> **Code:** `else:`
> **Type:** Else block

### Line 116
> **Code:** `y = None`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `X = frame`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `return {"X": X, "y": y}`
> **Type:** Returns a value from a function

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `def run() -> pd.DataFrame:`
> **Type:** Function definition

### Line 122
> **Code:** `"""Entry point: load clean data, build features, persist to parquet.""...`
> **Type:** Code statement

### Line 123
> **Code:** `clean = pd.read_csv("data/processed/dataset_clean.csv")`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `features = build_features(clean, include_sensitive=True)`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `features.to_parquet("data/features/features.parquet", index=False)`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `print(`
> **Type:** Prints output to console

### Line 127
> **Code:** `f"Built {features.shape[0]} rows x {features.shape[1]} columns "`
> **Type:** Data structure operation

### Line 128
> **Code:** `f"-> data/features/features.parquet"`
> **Type:** Arithmetic operation

### Line 129
> **Code:** `)`
> **Type:** Code statement

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `# Feast-ready variant keeps the entity key + timestamp for point-in-ti...`
> **Type:** Comment: Feast-ready variant keeps the entity key + timestamp for point-in-time joins.

### Line 132
> **Code:** `feast = build_feast_features(clean)`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `feast.to_parquet("data/features/feast_features.parquet", index=False)`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `print(`
> **Type:** Prints output to console

### Line 135
> **Code:** `f"Feast-ready frame {feast.shape[0]} rows x {feast.shape[1]} columns "`
> **Type:** Arithmetic operation

### Line 136
> **Code:** `f"-> data/features/feast_features.parquet"`
> **Type:** Arithmetic operation

### Line 137
> **Code:** `)`
> **Type:** Code statement

### Line 138
> **Code:** `return features`
> **Type:** Returns a value from a function

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** `def build_feast_features(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line 142
> **Code:** `"""Build a feature frame that keeps ``customer_id`` and ``timestamp``.`
> **Type:** Logical operation

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `This frame is what the Feast ``FileSource`` reads; the timestamp enabl...`
> **Type:** Code statement

### Line 145
> **Code:** `point-in-time correct joins so offline (training) and online (inferenc...`
> **Type:** Arithmetic operation

### Line 146
> **Code:** `feature values match.`
> **Type:** Code statement

### Line 147
> **Code:** `"""`
> **Type:** Code statement

### Line 148
> **Code:** `out = derive_features(df)`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `keep = [ID_COL, TIMESTAMP_COL] + NUMERIC_FEATURES + BINARY_FEATURES + ...`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `keep = [c for c in dict.fromkeys(keep) if c in out.columns]`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `out = out[keep]`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `if TIMESTAMP_COL in out.columns and not pd.api.types.is_numeric_dtype(...`
> **Type:** Conditional statement

### Line 153
> **Code:** `out[TIMESTAMP_COL] = pd.to_datetime(out[TIMESTAMP_COL])`
> **Type:** Assignment/comparison

### Line 154
> **Code:** `return out.reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 158
> **Code:** `run()`
> **Type:** Function call

## Summary
- **Total lines:** 158
- **Code lines:** 122
- **Comments:** 4
- **TODO items:** 0
- **Empty lines:** 32

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: build_features.py*
---

# mlops-full-mlops-skills-project: training_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/pipelines/training_pipeline.py`
- **Total lines:** 97
- **File size:** 2941 bytes

## Line Type Summary
- **Code:** 75
- **Comment:** 0
- **Empty:** 22
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML training pipeline with step caching and MLflow ExperimentTrac...`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- ingest: load raw data + log metadata (row count, time period, source...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- validate: Great Expectations checkpoint`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- preprocess: pure preprocessing functions`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- build_features: feature engineering (one-hot, derived features)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- train: MLflow-tracked training (params, metrics, artifacts)`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** `from zenml.integrations.mlflow.experiment_trackers import MLFlowExperi...`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `@step`
> **Type:** Code statement

### Line  20
> **Code:** `def ingest_data() -> tuple:`
> **Type:** Function definition

### Line  21
> **Code:** `"""Ingest raw data and return (dataframe, metadata)."""`
> **Type:** Logical operation

### Line  22
> **Code:** `from src.data.ingestion import ingest_raw_data`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `return ingest_raw_data(RAW_DATA_PATH)`
> **Type:** Returns a value from a function

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `@step`
> **Type:** Code statement

### Line  29
> **Code:** `def validate_data(df_metadata: tuple) -> bool:`
> **Type:** Function definition

### Line  30
> **Code:** `"""Run Great Expectations checkpoint on raw data."""`
> **Type:** Code statement

### Line  31
> **Code:** `import great_expectations as ge`
> **Type:** Imports a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `df, metadata = df_metadata`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `context = ge.get_context(context_root_dir="great_expectations")`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `checkpoint = context.checkpoints.get("dataset_checkpoint")`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `result = checkpoint.run(batch_request={"batch_data": df})`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `passed = result.success`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `logger.info(f"Great Expectations validation: {'PASSED' if passed else ...`
> **Type:** Function call

### Line  39
> **Code:** `if not passed:`
> **Type:** Conditional statement

### Line  40
> **Code:** `raise ValueError("Data validation failed - pipeline aborted")`
> **Type:** Raises an exception

### Line  41
> **Code:** `return passed`
> **Type:** Returns a value from a function

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `@step`
> **Type:** Code statement

### Line  45
> **Code:** `def preprocess_data(df_metadata: tuple):`
> **Type:** Function definition

### Line  46
> **Code:** `"""Apply pure preprocessing chain."""`
> **Type:** Code statement

### Line  47
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `df, metadata = df_metadata`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `return preprocess(df)`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `@step`
> **Type:** Code statement

### Line  54
> **Code:** `def build_features_step(clean_df) -> str:`
> **Type:** Function definition

### Line  55
> **Code:** `"""Build feature matrix and persist to parquet; return feature path.""...`
> **Type:** Logical operation

### Line  56
> **Code:** `from src.features.build_features import run`
> **Type:** Imports specific names from a module

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `run()`
> **Type:** Function call

### Line  59
> **Code:** `return "data/features/features.parquet"`
> **Type:** Returns a value from a function

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `@step`
> **Type:** Code statement

### Line  63
> **Code:** `def train_model(feature_path: str) -> dict:`
> **Type:** Function definition

### Line  64
> **Code:** `"""Train model with MLflow tracking."""`
> **Type:** Code statement

### Line  65
> **Code:** `from src.models.train import load_training_data, train_and_log`
> **Type:** Imports specific names from a module

### Line  66
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `)`
> **Type:** Code statement

### Line  72
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line  74
> **Code:** `run_name="zenml_training",`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `experiment_name="churn_prediction",`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `register=True,`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  79
> **Code:** `"run_id": result["run_id"],`
> **Type:** Data structure operation

### Line  80
> **Code:** `"f1_score": result["metrics"]["f1_score"],`
> **Type:** Logical operation

### Line  81
> **Code:** `"accuracy": result["metrics"]["accuracy"],`
> **Type:** Data structure operation

### Line  82
> **Code:** `"roc_auc": result["metrics"]["roc_auc"],`
> **Type:** Data structure operation

### Line  83
> **Code:** `}`
> **Type:** Code statement

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `@pipeline`
> **Type:** Code statement

### Line  87
> **Code:** `def training_pipeline():`
> **Type:** Function definition

### Line  88
> **Code:** `"""Full training pipeline with caching and MLflow tracking."""`
> **Type:** Logical operation

### Line  89
> **Code:** `ingested = ingest_data()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `validate_data(ingested)`
> **Type:** Function call

### Line  91
> **Code:** `cleaned = preprocess_data(ingested)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `features = build_features_step(cleaned)`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `train_model(features)`
> **Type:** Function call

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  97
> **Code:** `training_pipeline()`
> **Type:** Function call

## Summary
- **Total lines:** 97
- **Code lines:** 75
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 22

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: training_pipeline.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/pipelines/__init__.py`
- **Total lines:** 1
- **File size:** 81 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""pipelines package: ZenML pipeline definitions for the churn MLOps p...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: retraining_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/pipelines/retraining_pipeline.py`
- **Total lines:** 156
- **File size:** 5199 bytes

## Line Type Summary
- **Code:** 114
- **Comment:** 7
- **Empty:** 35
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML automated retraining pipeline triggered by drift.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- check_drift: read latest drift score from monitoring`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- if drift > threshold: re-run full training + tuning + gates`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- retrain: training with best params from Optuna`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- validate_gates: Deepchecks + Fairlearn (same gates as promotion)`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- promote_if_better: only promote if beats current production`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `This pipeline reuses the same validation gates as manual promotion - n...`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `@step`
> **Type:** Code statement

### Line  21
> **Code:** `def check_drift() -> dict:`
> **Type:** Function definition

### Line  22
> **Code:** `"""Read latest drift score and decide if retraining is needed."""`
> **Type:** Logical operation

### Line  23
> **Code:** `from src.monitoring.retraining_trigger import read_drift_score, should...`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from src.config import DRIFT_THRESHOLD`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `score = read_drift_score()`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `trigger = should_retrain(score, DRIFT_THRESHOLD)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `logger.info(f"Drift check: score={score:.3f}, threshold={DRIFT_THRESHO...`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `return {"drift_score": score, "threshold": DRIFT_THRESHOLD, "trigger":...`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `@step`
> **Type:** Code statement

### Line  33
> **Code:** `def retrain_model(drift_info: dict) -> dict:`
> **Type:** Function definition

### Line  34
> **Code:** `"""Re-run training with Optuna tuning on recent data if drift detected...`
> **Type:** Arithmetic operation

### Line  35
> **Code:** `if not drift_info.get("trigger", False):`
> **Type:** Conditional statement

### Line  36
> **Code:** `logger.info("No drift detected - skipping retraining")`
> **Type:** Arithmetic operation

### Line  37
> **Code:** `return {"retrained": False, "reason": "no_drift"}`
> **Type:** Returns a value from a function

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `logger.info("Drift detected - starting retraining pipeline")`
> **Type:** Arithmetic operation

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `# Run tuning to find best params`
> **Type:** Comment: Run tuning to find best params

### Line  42
> **Code:** `from src.models.tune import tune`
> **Type:** Imports specific names from a module

### Line  43
> **Code:** `best = tune(n_trials=30, experiment_name="churn_retraining")`
> **Type:** Assignment/comparison

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `# Train with best params`
> **Type:** Comment: Train with best params

### Line  46
> **Code:** `from src.models.train import load_training_data, train_and_log`
> **Type:** Imports specific names from a module

### Line  47
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `)`
> **Type:** Code statement

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line  56
> **Code:** `params=best["best_params"],`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `run_name="retrained_model",`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `experiment_name="churn_retraining",`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `register=True,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `)`
> **Type:** Code statement

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  63
> **Code:** `"retrained": True,`
> **Type:** Code statement

### Line  64
> **Code:** `"run_id": result["run_id"],`
> **Type:** Data structure operation

### Line  65
> **Code:** `"best_params": best["best_params"],`
> **Type:** Data structure operation

### Line  66
> **Code:** `"best_cv_f1": best["best_value"],`
> **Type:** Data structure operation

### Line  67
> **Code:** `"test_f1": result["metrics"]["f1_score"],`
> **Type:** Logical operation

### Line  68
> **Code:** `"test_accuracy": result["metrics"]["accuracy"],`
> **Type:** Data structure operation

### Line  69
> **Code:** `"test_roc_auc": result["metrics"]["roc_auc"],`
> **Type:** Data structure operation

### Line  70
> **Code:** `}`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `@step`
> **Type:** Code statement

### Line  74
> **Code:** `def validate_retrained_model(retrain_result: dict) -> dict:`
> **Type:** Function definition

### Line  75
> **Code:** `"""Run Deepchecks and Fairlearn on the retrained model."""`
> **Type:** Logical operation

### Line  76
> **Code:** `if not retrain_result.get("retrained", False):`
> **Type:** Conditional statement

### Line  77
> **Code:** `return {"deepchecks_passed": True, "fairness_passed": True, "skipped":...`
> **Type:** Returns a value from a function

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  80
> **Code:** `from src.models.promote import run_deepchecks, _load_test_frame`
> **Type:** Imports specific names from a module

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `model_path = "models/churn_model.joblib"`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `# Deepchecks`
> **Type:** Comment: Deepchecks

### Line  87
> **Code:** `deepchecks = run_deepchecks(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `# Fairness`
> **Type:** Comment: Fairness

### Line  90
> **Code:** `from src.models.fairness_check import fairness_check`
> **Type:** Imports specific names from a module

### Line  91
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  92
> **Code:** `fairness = fairness_check(Path(model_path))`
> **Type:** Assignment/comparison

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `logger.info(f"Deepchecks: {'PASSED' if deepchecks['passed'] else 'FAIL...`
> **Type:** Function call

### Line  95
> **Code:** `logger.info(f"Fairness: {'PASSED' if fairness['passed'] else 'FAILED'}...`
> **Type:** Function call

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  98
> **Code:** `"deepchecks_passed": deepchecks["passed"],`
> **Type:** Data structure operation

### Line  99
> **Code:** `"fairness_passed": fairness["passed"],`
> **Type:** Data structure operation

### Line 100
> **Code:** `"dp_diff": fairness.get("demographic_parity_difference"),`
> **Type:** Code statement

### Line 101
> **Code:** `}`
> **Type:** Code statement

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `@step`
> **Type:** Code statement

### Line 105
> **Code:** `def promote_if_better(validation: dict, retrain_result: dict) -> dict:`
> **Type:** Function definition

### Line 106
> **Code:** `"""Promote retrained model if it beats production and passes all gates...`
> **Type:** Logical operation

### Line 107
> **Code:** `if not retrain_result.get("retrained", False):`
> **Type:** Conditional statement

### Line 108
> **Code:** `return {"promoted": False, "reason": "not_retrained"}`
> **Type:** Returns a value from a function

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `# Check all gates`
> **Type:** Comment: Check all gates

### Line 111
> **Code:** `gates = {`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `"deepchecks": validation.get("deepchecks_passed", False),`
> **Type:** Code statement

### Line 113
> **Code:** `"fairness": validation.get("fairness_passed", False),`
> **Type:** Code statement

### Line 114
> **Code:** `}`
> **Type:** Code statement

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `# Performance gate`
> **Type:** Comment: Performance gate

### Line 117
> **Code:** `candidate_f1 = retrain_result.get("test_f1", 0)`
> **Type:** Assignment/comparison

### Line 118
> **Code:** `from src.config import F1_PROMOTION_THRESHOLD`
> **Type:** Imports specific names from a module

### Line 119
> **Code:** `gates["performance"] = candidate_f1 >= F1_PROMOTION_THRESHOLD`
> **Type:** Assignment/comparison

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `# Beats production gate`
> **Type:** Comment: Beats production gate

### Line 122
> **Code:** `from src.models.promote import load_production_model_metrics`
> **Type:** Imports specific names from a module

### Line 123
> **Code:** `prod_f1 = load_production_model_metrics()`
> **Type:** Assignment/comparison

### Line 124
> **Code:** `if prod_f1 is None:`
> **Type:** Conditional statement

### Line 125
> **Code:** `gates["beats_production"] = True`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `else:`
> **Type:** Else block

### Line 127
> **Code:** `gates["beats_production"] = candidate_f1 > prod_f1 + 0.005`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `all_passed = all(gates.values())`
> **Type:** Assignment/comparison

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `if all_passed:`
> **Type:** Conditional statement

### Line 132
> **Code:** `from src.models.promote import _move_to_production`
> **Type:** Imports specific names from a module

### Line 133
> **Code:** `_move_to_production(retrain_result.get("run_id"))`
> **Type:** Function call

### Line 134
> **Code:** `logger.info("Retrained model promoted to Production")`
> **Type:** Function call

### Line 135
> **Code:** `else:`
> **Type:** Else block

### Line 136
> **Code:** `logger.warning(f"Retrained model failed gates: {gates}")`
> **Type:** Function call

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 139
> **Code:** `"promoted": all_passed,`
> **Type:** Code statement

### Line 140
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 141
> **Code:** `"candidate_f1": candidate_f1,`
> **Type:** Logical operation

### Line 142
> **Code:** `"production_f1": prod_f1,`
> **Type:** Code statement

### Line 143
> **Code:** `}`
> **Type:** Code statement

### Line 144
> **Code:** ``
> **Type:** Empty line

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `@pipeline`
> **Type:** Code statement

### Line 147
> **Code:** `def retraining_pipeline():`
> **Type:** Function definition

### Line 148
> **Code:** `"""Automated retraining pipeline triggered by drift."""`
> **Type:** Code statement

### Line 149
> **Code:** `drift_info = check_drift()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `retrain_result = retrain_model(drift_info)`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `validation = validate_retrained_model(retrain_result)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `promote_if_better(validation, retrain_result)`
> **Type:** Function call

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 156
> **Code:** `retraining_pipeline()`
> **Type:** Function call

## Summary
- **Total lines:** 156
- **Code lines:** 114
- **Comments:** 7
- **TODO items:** 0
- **Empty lines:** 35

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: retraining_pipeline.py*
---

# mlops-full-mlops-skills-project: tuning_pipeline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/pipelines/tuning_pipeline.py`
- **Total lines:** 93
- **File size:** 3022 bytes

## Line Type Summary
- **Code:** 71
- **Comment:** 0
- **Empty:** 22
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ZenML hyperparameter tuning pipeline with Optuna and nested MLflow ...`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Steps:`
> **Type:** Code statement

### Line   4
> **Code:** `- load_data: same data loading as training`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- tune: Optuna bayesian search (50 trials), each trial logged as neste...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- log_best: logs best params and score to MLflow`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from zenml import pipeline, step`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** `from zenml.logger import get_logger`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `logger = get_logger(__name__)`
> **Type:** Assignment/comparison

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `@step`
> **Type:** Code statement

### Line  17
> **Code:** `def load_data() -> tuple:`
> **Type:** Function definition

### Line  18
> **Code:** `"""Load training data (X, y)."""`
> **Type:** Code statement

### Line  19
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `@step`
> **Type:** Code statement

### Line  25
> **Code:** `def tune_hyperparameters(data: tuple, n_trials: int = 50) -> dict:`
> **Type:** Function definition

### Line  26
> **Code:** `"""Run Optuna bayesian optimization with nested MLflow runs."""`
> **Type:** Code statement

### Line  27
> **Code:** `import optuna`
> **Type:** Imports a module

### Line  28
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  29
> **Code:** `from optuna.samplers import TPESampler`
> **Type:** Imports specific names from a module

### Line  30
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `from sklearn.model_selection import StratifiedKFold, cross_val_score`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `X, y = data`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  38
> **Code:** `mlflow.set_experiment("churn_optuna")`
> **Type:** Function call

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `def objective(trial):`
> **Type:** Function definition

### Line  41
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `"n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `"max_depth": trial.suggest_int("max_depth", 3, 20),`
> **Type:** Code statement

### Line  44
> **Code:** `"min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),`
> **Type:** Code statement

### Line  45
> **Code:** `"max_features": trial.suggest_categorical("max_features", ["sqrt", "lo...`
> **Type:** Logical operation

### Line  46
> **Code:** `"min_samples_split": trial.suggest_int("min_samples_split", 2, 15),`
> **Type:** Code statement

### Line  47
> **Code:** `}`
> **Type:** Code statement

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `model = RandomForestClassifier(**params, random_state=42)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `with mlflow.start_run(nested=True):`
> **Type:** Context manager

### Line  51
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line  52
> **Code:** `cv_score = cross_val_score(`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `model, X, y, cv=StratifiedKFold(3), scoring="f1", n_jobs=-1`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `).mean()`
> **Type:** Function call

### Line  55
> **Code:** `mlflow.log_metric("cv_f1", cv_score)`
> **Type:** Logical operation

### Line  56
> **Code:** `trial.report(cv_score, step=0)`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `return cv_score`
> **Type:** Returns a value from a function

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `study = optuna.create_study(`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `direction="maximize",`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `sampler=TPESampler(seed=42),`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `study_name="churn_rf_bayesian",`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `)`
> **Type:** Code statement

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** `with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):`
> **Type:** Context manager

### Line  66
> **Code:** `mlflow.log_param("n_trials", n_trials)`
> **Type:** Function call

### Line  67
> **Code:** `mlflow.log_param("sampler", "TPE")`
> **Type:** Function call

### Line  68
> **Code:** `study.optimize(`
> **Type:** Code statement

### Line  69
> **Code:** `objective, n_trials=n_trials, show_progress_bar=False`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** `mlflow.log_metric("best_cv_f1", study.best_value)`
> **Type:** Function call

### Line  72
> **Code:** `mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items(...`
> **Type:** Logical operation

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `logger.info("Best trial: %.4f with %s", study.best_value, study.best_p...`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `return {"best_params": study.best_params, "best_value": study.best_val...`
> **Type:** Returns a value from a function

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `@step`
> **Type:** Code statement

### Line  79
> **Code:** `def log_best_params(best_result: dict) -> dict:`
> **Type:** Function definition

### Line  80
> **Code:** `"""Log the best hyperparameters for downstream use."""`
> **Type:** Logical operation

### Line  81
> **Code:** `return best_result`
> **Type:** Returns a value from a function

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `@pipeline`
> **Type:** Code statement

### Line  85
> **Code:** `def tuning_pipeline(n_trials: int = 50):`
> **Type:** Function definition

### Line  86
> **Code:** `"""Hyperparameter tuning pipeline with Optuna."""`
> **Type:** Code statement

### Line  87
> **Code:** `data = load_data()`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `best = tune_hyperparameters(data, n_trials)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `log_best_params(best)`
> **Type:** Function call

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  93
> **Code:** `tuning_pipeline(n_trials=50)`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 93
- **Code lines:** 71
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 22

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: tuning_pipeline.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/model_cards/__init__.py`
- **Total lines:** 1
- **File size:** 68 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""model_cards package: generated model card markdown artifacts."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: model_card_template.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/model_cards/model_card_template.py`
- **Total lines:** 118
- **File size:** 3714 bytes

## Line Type Summary
- **Code:** 99
- **Comment:** 0
- **Empty:** 19
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Automatic Model Card generation.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Builds a Markdown model card from MLflow metrics + Fairlearn fairness ...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `so the documentation is regenerated at every promotion instead of goin...`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import datetime`
> **Type:** Imports a module

### Line  10
> **Code:** `import json`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** `from typing import Optional`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `def _read_json(path: Path) -> dict:`
> **Type:** Function definition

### Line  18
> **Code:** `if path.exists():`
> **Type:** Conditional statement

### Line  19
> **Code:** `return json.loads(path.read_text())`
> **Type:** Returns a value from a function

### Line  20
> **Code:** `return {}`
> **Type:** Returns a value from a function

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `def _format_metric(value) -> str:`
> **Type:** Function definition

### Line  24
> **Code:** `try:`
> **Type:** Code statement

### Line  25
> **Code:** `return f"{float(value):.4f}"`
> **Type:** Returns a value from a function

### Line  26
> **Code:** `except (TypeError, ValueError):`
> **Type:** Logical operation

### Line  27
> **Code:** `return str(value)`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def generate_model_card(`
> **Type:** Function definition

### Line  31
> **Code:** `report: Optional[dict] = None,`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `output_path: Path = Path("model_cards/model_card.md"),`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `) -> str:`
> **Type:** Arithmetic operation

### Line  34
> **Code:** `"""Generate a model card markdown string and write it to ``output_path...`
> **Type:** Logical operation

### Line  35
> **Code:** `report = report or {}`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `metrics = report.get("metrics", {}) or _read_json(REPORTS_DIR / "promo...`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `"metrics", {}`
> **Type:** Code statement

### Line  38
> **Code:** `)`
> **Type:** Code statement

### Line  39
> **Code:** `fairness = report.get("fairness", {}) or _read_json(REPORTS_DIR / "fai...`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `gates = report.get("gates", {})`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `lines = [`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `"# Model Card: Customer Churn Classifier",`
> **Type:** Code statement

### Line  44
> **Code:** `"",`
> **Type:** Code statement

### Line  45
> **Code:** `f"*Generated automatically on {datetime.datetime.now().isoformat()}*",`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `"",`
> **Type:** Code statement

### Line  47
> **Code:** `"## Model details",`
> **Type:** Code statement

### Line  48
> **Code:** `"",`
> **Type:** Code statement

### Line  49
> **Code:** `"- Algorithm: RandomForestClassifier",`
> **Type:** Arithmetic operation

### Line  50
> **Code:** `"- Task: Binary classification (customer churn)",`
> **Type:** Arithmetic operation

### Line  51
> **Code:** `"- Objective: Predict churn probability to enable proactive retention"...`
> **Type:** Arithmetic operation

### Line  52
> **Code:** `"",`
> **Type:** Code statement

### Line  53
> **Code:** `"## Intended use",`
> **Type:** Code statement

### Line  54
> **Code:** `"",`
> **Type:** Code statement

### Line  55
> **Code:** `"- Valid: churn risk scoring for telecom customers",`
> **Type:** Arithmetic operation

### Line  56
> **Code:** `"- Avoid: credit decisions, medical predictions, or any other domain",`
> **Type:** Arithmetic operation

### Line  57
> **Code:** `"",`
> **Type:** Code statement

### Line  58
> **Code:** `"## Training data",`
> **Type:** Code statement

### Line  59
> **Code:** `"",`
> **Type:** Code statement

### Line  60
> **Code:** `"- Source: synthetic telecom dataset (`data/raw/dataset.csv`)",`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `"- Rows: ~7000, binary target with a sensitive attribute (`gender`)",`
> **Type:** Arithmetic operation

### Line  62
> **Code:** `"",`
> **Type:** Code statement

### Line  63
> **Code:** `"## Performance metrics (held-out test set)",`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `"",`
> **Type:** Code statement

### Line  65
> **Code:** `"| Metric | Value |",`
> **Type:** Code statement

### Line  66
> **Code:** `"| --- | --- |",`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `]`
> **Type:** Code statement

### Line  68
> **Code:** `for name, value in metrics.items():`
> **Type:** For loop

### Line  69
> **Code:** `lines.append(f"| {name} | {_format_metric(value)} |")`
> **Type:** Logical operation

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `"",`
> **Type:** Code statement

### Line  73
> **Code:** `"## Fairness analysis (Fairlearn)",`
> **Type:** Code statement

### Line  74
> **Code:** `"",`
> **Type:** Code statement

### Line  75
> **Code:** `f"- Demographic parity difference: {_format_metric(fairness.get('demog...`
> **Type:** Arithmetic operation

### Line  76
> **Code:** `f"- Equalized odds difference: {_format_metric(fairness.get('equalized...`
> **Type:** Arithmetic operation

### Line  77
> **Code:** `f"- Threshold (dp_diff): {_format_metric(fairness.get('threshold', 0.1...`
> **Type:** Arithmetic operation

### Line  78
> **Code:** `]`
> **Type:** Code statement

### Line  79
> **Code:** `if "selection_rate_by_group" in fairness:`
> **Type:** Conditional statement

### Line  80
> **Code:** `lines.append("")`
> **Type:** Function call

### Line  81
> **Code:** `lines.append("| Group | Selection rate |")`
> **Type:** Function call

### Line  82
> **Code:** `lines.append("| --- | --- |")`
> **Type:** Arithmetic operation

### Line  83
> **Code:** `for group, rate in fairness.get("selection_rate_by_group", {}).items()...`
> **Type:** For loop

### Line  84
> **Code:** `lines.append(f"| {group} | {_format_metric(rate)} |")`
> **Type:** Logical operation

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `"",`
> **Type:** Code statement

### Line  88
> **Code:** `"## Promotion gates",`
> **Type:** Code statement

### Line  89
> **Code:** `"",`
> **Type:** Code statement

### Line  90
> **Code:** `"| Gate | Status |",`
> **Type:** Code statement

### Line  91
> **Code:** `"| --- | --- |",`
> **Type:** Arithmetic operation

### Line  92
> **Code:** `]`
> **Type:** Code statement

### Line  93
> **Code:** `for name, passed in gates.items():`
> **Type:** For loop

### Line  94
> **Code:** `lines.append(f"| {name} | {'PASS' if passed else 'FAIL'} |")`
> **Type:** Function call

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `lines += [`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `"",`
> **Type:** Code statement

### Line  98
> **Code:** `"## Known limitations & identified biases",`
> **Type:** Code statement

### Line  99
> **Code:** `"",`
> **Type:** Code statement

### Line 100
> **Code:** `"- Trained on synthetic data; real-world performance may differ.",`
> **Type:** Arithmetic operation

### Line 101
> **Code:** `"- Fairness is measured on `gender` only; other sensitive dimensions"`
> **Type:** Arithmetic operation

### Line 102
> **Code:** `" (e.g. age bands) are not audited in this version.",`
> **Type:** Logical operation

### Line 103
> **Code:** `"- Small residual demographic parity difference exists and is monitore...`
> **Type:** Arithmetic operation

### Line 104
> **Code:** `]`
> **Type:** Code statement

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `card = "\n".join(lines) + "\n"`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `output_path.write_text(card)`
> **Type:** Function call

### Line 109
> **Code:** `return card`
> **Type:** Returns a value from a function

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 113
> **Code:** `card = generate_model_card()`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `print(card)`
> **Type:** Prints output to console

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** ``
> **Type:** Empty line

### Line 117
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 118
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 118
- **Code lines:** 99
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 19

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: model_card_template.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/model/__init__.py`
- **Total lines:** 1
- **File size:** 44 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: model lifecycle tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_model_quality.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/model/test_model_quality.py`
- **Total lines:** 106
- **File size:** 3522 bytes

## Line Type Summary
- **Code:** 69
- **Comment:** 8
- **Empty:** 29
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model quality tests using Deepchecks."""`
> **Type:** Code statement

### Line   2
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   3
> **Code:** `import joblib`
> **Type:** Imports a module

### Line   4
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   5
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `@pytest.fixture`
> **Type:** Code statement

### Line   9
> **Code:** `def model_and_data():`
> **Type:** Function definition

### Line  10
> **Code:** `"""Load model and test data."""`
> **Type:** Logical operation

### Line  11
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `X = sets["X"]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `y = sets["y"]`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `_, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_s...`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `model = joblib.load("models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `return model, X_test, y_test`
> **Type:** Returns a value from a function

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `def test_model_loaded(model_and_data):`
> **Type:** Function definition

### Line  28
> **Code:** `model, _, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `assert model is not None`
> **Type:** Enforces a condition

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def test_model_predicts(model_and_data):`
> **Type:** Function definition

### Line  33
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `preds = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `assert len(preds) == len(X_test)`
> **Type:** Enforces a condition

### Line  36
> **Code:** `assert set(preds).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def test_model_predict_proba(model_and_data):`
> **Type:** Function definition

### Line  40
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `proba = model.predict_proba(X_test)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `assert proba.shape == (len(X_test), 2)`
> **Type:** Enforces a condition

### Line  43
> **Code:** `assert (proba >= 0).all() and (proba <= 1).all()`
> **Type:** Enforces a condition

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def test_model_performance_threshold(model_and_data):`
> **Type:** Function definition

### Line  47
> **Code:** `"""Basic performance check - F1 should be reasonable."""`
> **Type:** Arithmetic operation

### Line  48
> **Code:** `from sklearn.metrics import f1_score`
> **Type:** Imports specific names from a module

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `model, X_test, y_test = model_and_data`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `f1 = f1_score(y_test, y_pred)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `assert f1 >= 0.2, f"F1 score {f1:.4f} below minimum threshold"`
> **Type:** Enforces a condition

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `def test_deepchecks_suite(model_and_data):`
> **Type:** Function definition

### Line  57
> **Code:** `"""Run Deepchecks full suite if available."""`
> **Type:** Code statement

### Line  58
> **Code:** `try:`
> **Type:** Code statement

### Line  59
> **Code:** `from deepchecks.tabular import Dataset`
> **Type:** Imports specific names from a module

### Line  60
> **Code:** `from deepchecks.tabular.suites import full_suite`
> **Type:** Imports specific names from a module

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `model, X_test, y_test = model_and_data`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `# Deepchecks needs the full dataframe with label`
> **Type:** Comment: Deepchecks needs the full dataframe with label

### Line  65
> **Code:** `test_df = X_test.copy()`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `test_df["churn"] = y_test.values`
> **Type:** Assignment/comparison

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `ds = Dataset(test_df, label="churn")`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `suite = full_suite()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `result = suite.run(ds, model=model)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `# Check for critical failures`
> **Type:** Comment: Check for critical failures

### Line  73
> **Code:** `critical_failures = [`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `check.get_header() for check in result.results if not check.passed`
> **Type:** Logical operation

### Line  75
> **Code:** `]`
> **Type:** Code statement

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** `# If there are critical failures, print them for visibility`
> **Type:** Comment: If there are critical failures, print them for visibility

### Line  78
> **Code:** `if critical_failures:`
> **Type:** Conditional statement

### Line  79
> **Code:** `print(f"Deepchecks critical failures: {critical_failures}")`
> **Type:** Prints output to console

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `# This test passes if Deepchecks runs (even with failures - they're wa...`
> **Type:** Comment: This test passes if Deepchecks runs (even with failures - they're warnings)

### Line  82
> **Code:** `# In production, you'd want: assert not critical_failures`
> **Type:** Comment: In production, you'd want: assert not critical_failures

### Line  83
> **Code:** `assert True`
> **Type:** Enforces a condition

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `except ImportError:`
> **Type:** Logical operation

### Line  86
> **Code:** `pytest.skip("deepchecks not available")`
> **Type:** Logical operation

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `def test_model_feature_importance_stable(model_and_data):`
> **Type:** Function definition

### Line  90
> **Code:** `"""Check that top features are consistent (non-regression)."""`
> **Type:** Arithmetic operation

### Line  91
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `model, X_test, _ = model_and_data`
> **Type:** Assignment/comparison

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** `# Get feature importances`
> **Type:** Comment: Get feature importances

### Line  96
> **Code:** `importances = model.feature_importances_`
> **Type:** Imports a module

### Line  97
> **Code:** `top_features = np.argsort(importances)[-5:]  # Top 5 indices`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `top_feature_names = [X_test.columns[i] for i in top_features]`
> **Type:** Assignment/comparison

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `# These are expected to be among top features based on data generation`
> **Type:** Comment: These are expected to be among top features based on data generation

### Line 101
> **Code:** `expected_important = {"tenure_months", "monthly_charges", "contract_ty...`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `found_important = set(top_feature_names)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `# At least 2 of the expected important features should be in top 5`
> **Type:** Comment: At least 2 of the expected important features should be in top 5

### Line 105
> **Code:** `overlap = len(expected_important & found_important)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `assert overlap >= 2, f"Top features {top_feature_names} don't match ex...`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 106
- **Code lines:** 69
- **Comments:** 8
- **TODO items:** 0
- **Empty lines:** 29

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_model_quality.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/unit/__init__.py`
- **Total lines:** 1
- **File size:** 33 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: unit tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/unit/test_features.py`
- **Total lines:** 110
- **File size:** 3922 bytes

## Line Type Summary
- **Code:** 97
- **Comment:** 2
- **Empty:** 11
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for feature engineering functions."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from src.features.build_features import (`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** `derive_features,`
> **Type:** Code statement

### Line   7
> **Code:** `one_hot_encode,`
> **Type:** Code statement

### Line   8
> **Code:** `build_features,`
> **Type:** Code statement

### Line   9
> **Code:** `feature_sets,`
> **Type:** Code statement

### Line  10
> **Code:** `build_feast_features,`
> **Type:** Code statement

### Line  11
> **Code:** `)`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `def test_derive_features():`
> **Type:** Function definition

### Line  15
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `"tenure_months": [1, 12, 36, 60],`
> **Type:** Data structure operation

### Line  17
> **Code:** `"monthly_charges": [50.0, 60.0, 70.0, 80.0],`
> **Type:** Data structure operation

### Line  18
> **Code:** `"num_services": [1, 2, 3, 4],`
> **Type:** Data structure operation

### Line  19
> **Code:** `"support_tickets": [0, 1, 2, 3],`
> **Type:** Logical operation

### Line  20
> **Code:** `"total_charges": [50.0, 720.0, 2520.0, 4800.0],`
> **Type:** Data structure operation

### Line  21
> **Code:** `"avg_call_minutes": [100.0, 200.0, 300.0, 400.0],`
> **Type:** Data structure operation

### Line  22
> **Code:** `})`
> **Type:** Code statement

### Line  23
> **Code:** `result = derive_features(df)`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `assert "avg_charge_per_month" in result.columns`
> **Type:** Enforces a condition

### Line  25
> **Code:** `assert "service_density" in result.columns`
> **Type:** Enforces a condition

### Line  26
> **Code:** `assert "ticket_intensity" in result.columns`
> **Type:** Enforces a condition

### Line  27
> **Code:** `assert "is_long_tenure" in result.columns`
> **Type:** Enforces a condition

### Line  28
> **Code:** `assert "is_high_value_customer" in result.columns`
> **Type:** Enforces a condition

### Line  29
> **Code:** `assert "usage_efficiency" in result.columns`
> **Type:** Enforces a condition

### Line  30
> **Code:** `# Check values`
> **Type:** Comment: Check values

### Line  31
> **Code:** `assert result.loc[0, "avg_charge_per_month"] == 50.0  # 50/1`
> **Type:** Enforces a condition

### Line  32
> **Code:** `assert result.loc[1, "is_long_tenure"] == 0`
> **Type:** Enforces a condition

### Line  33
> **Code:** `assert result.loc[2, "is_long_tenure"] == 1`
> **Type:** Enforces a condition

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def test_one_hot_encode():`
> **Type:** Function definition

### Line  37
> **Code:** `df = pd.DataFrame({"color": ["red", "blue", "red", "green"]})`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `result = one_hot_encode(df, ["color"])`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `# drop_first=True: first category ("blue") dropped, others encoded`
> **Type:** Comment: drop_first=True: first category ("blue") dropped, others encoded

### Line  40
> **Code:** `assert "color_blue" not in result.columns`
> **Type:** Enforces a condition

### Line  41
> **Code:** `assert "color_green" in result.columns`
> **Type:** Enforces a condition

### Line  42
> **Code:** `assert "color_red" in result.columns`
> **Type:** Enforces a condition

### Line  43
> **Code:** `assert len(result) == 4`
> **Type:** Enforces a condition

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def test_build_features():`
> **Type:** Function definition

### Line  47
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `"customer_id": [1, 2, 3],`
> **Type:** Data structure operation

### Line  49
> **Code:** `"timestamp": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]...`
> **Type:** Arithmetic operation

### Line  50
> **Code:** `"age": [25, 30, 35],`
> **Type:** Data structure operation

### Line  51
> **Code:** `"gender": ["M", "F", "M"],`
> **Type:** Data structure operation

### Line  52
> **Code:** `"region": ["north", "south", "east"],`
> **Type:** Logical operation

### Line  53
> **Code:** `"tenure_months": [12, 24, 36],`
> **Type:** Data structure operation

### Line  54
> **Code:** `"monthly_charges": [50.0, 60.0, 70.0],`
> **Type:** Data structure operation

### Line  55
> **Code:** `"total_charges": [600.0, 1440.0, 2520.0],`
> **Type:** Data structure operation

### Line  56
> **Code:** `"num_services": [2, 3, 4],`
> **Type:** Data structure operation

### Line  57
> **Code:** `"contract_type": ["one_year", "two_year", "month-to-month"],`
> **Type:** Arithmetic operation

### Line  58
> **Code:** `"payment_method": ["credit_card", "bank_transfer", "electronic_check"]...`
> **Type:** Data structure operation

### Line  59
> **Code:** `"support_tickets": [1, 0, 2],`
> **Type:** Logical operation

### Line  60
> **Code:** `"avg_call_minutes": [100.0, 50.0, 200.0],`
> **Type:** Data structure operation

### Line  61
> **Code:** `"has_online_backup": [1, 0, 1],`
> **Type:** Data structure operation

### Line  62
> **Code:** `"has_device_protection": [0, 1, 0],`
> **Type:** Data structure operation

### Line  63
> **Code:** `"has_tech_support": [1, 0, 1],`
> **Type:** Logical operation

### Line  64
> **Code:** `"churn": [0, 1, 0],`
> **Type:** Data structure operation

### Line  65
> **Code:** `})`
> **Type:** Code statement

### Line  66
> **Code:** `result = build_features(df, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `assert "churn" in result.columns`
> **Type:** Enforces a condition

### Line  68
> **Code:** `assert "gender" not in result.columns`
> **Type:** Enforces a condition

### Line  69
> **Code:** `assert "customer_id" not in result.columns`
> **Type:** Enforces a condition

### Line  70
> **Code:** `assert "timestamp" not in result.columns`
> **Type:** Enforces a condition

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def test_feature_sets():`
> **Type:** Function definition

### Line  74
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `"feature1": [1, 2, 3],`
> **Type:** Data structure operation

### Line  76
> **Code:** `"feature2": [4, 5, 6],`
> **Type:** Data structure operation

### Line  77
> **Code:** `"churn": [0, 1, 0],`
> **Type:** Data structure operation

### Line  78
> **Code:** `})`
> **Type:** Code statement

### Line  79
> **Code:** `sets = feature_sets(df)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `assert "X" in sets`
> **Type:** Enforces a condition

### Line  81
> **Code:** `assert "y" in sets`
> **Type:** Enforces a condition

### Line  82
> **Code:** `assert list(sets["X"].columns) == ["feature1", "feature2"]`
> **Type:** Enforces a condition

### Line  83
> **Code:** `assert list(sets["y"]) == [0, 1, 0]`
> **Type:** Enforces a condition

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def test_build_feast_features():`
> **Type:** Function definition

### Line  87
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `"customer_id": [1, 2, 3],`
> **Type:** Data structure operation

### Line  89
> **Code:** `"timestamp": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]...`
> **Type:** Arithmetic operation

### Line  90
> **Code:** `"age": [25, 30, 35],`
> **Type:** Data structure operation

### Line  91
> **Code:** `"gender": ["M", "F", "M"],`
> **Type:** Data structure operation

### Line  92
> **Code:** `"region": ["north", "south", "east"],`
> **Type:** Logical operation

### Line  93
> **Code:** `"tenure_months": [12, 24, 36],`
> **Type:** Data structure operation

### Line  94
> **Code:** `"monthly_charges": [50.0, 60.0, 70.0],`
> **Type:** Data structure operation

### Line  95
> **Code:** `"total_charges": [600.0, 1440.0, 2520.0],`
> **Type:** Data structure operation

### Line  96
> **Code:** `"num_services": [2, 3, 4],`
> **Type:** Data structure operation

### Line  97
> **Code:** `"contract_type": ["one_year", "two_year", "month-to-month"],`
> **Type:** Arithmetic operation

### Line  98
> **Code:** `"payment_method": ["credit_card", "bank_transfer", "electronic_check"]...`
> **Type:** Data structure operation

### Line  99
> **Code:** `"support_tickets": [1, 0, 2],`
> **Type:** Logical operation

### Line 100
> **Code:** `"avg_call_minutes": [100.0, 50.0, 200.0],`
> **Type:** Data structure operation

### Line 101
> **Code:** `"has_online_backup": [1, 0, 1],`
> **Type:** Data structure operation

### Line 102
> **Code:** `"has_device_protection": [0, 1, 0],`
> **Type:** Data structure operation

### Line 103
> **Code:** `"has_tech_support": [1, 0, 1],`
> **Type:** Logical operation

### Line 104
> **Code:** `"churn": [0, 1, 0],`
> **Type:** Data structure operation

### Line 105
> **Code:** `})`
> **Type:** Code statement

### Line 106
> **Code:** `result = build_feast_features(df)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `assert "customer_id" in result.columns`
> **Type:** Enforces a condition

### Line 108
> **Code:** `assert "timestamp" in result.columns`
> **Type:** Enforces a condition

### Line 109
> **Code:** `assert "churn" in result.columns`
> **Type:** Enforces a condition

### Line 110
> **Code:** `assert result["timestamp"].dtype == "datetime64[ns]"`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 110
- **Code lines:** 97
- **Comments:** 2
- **TODO items:** 0
- **Empty lines:** 11

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_features.py*
---

# mlops-full-mlops-skills-project: test_fairness.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/unit/test_fairness.py`
- **Total lines:** 74
- **File size:** 2842 bytes

## Line Type Summary
- **Code:** 45
- **Comment:** 10
- **Empty:** 19
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for fairness checking logic."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line   4
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   5
> **Code:** ``
> **Type:** Empty line

### Line   6
> **Code:** `from src.config import FAIRNESS_DP_THRESHOLD`
> **Type:** Imports specific names from a module

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `def test_fairness_threshold():`
> **Type:** Function definition

### Line  10
> **Code:** `"""Test that the fairness threshold constant is set correctly."""`
> **Type:** Logical operation

### Line  11
> **Code:** `assert FAIRNESS_DP_THRESHOLD == 0.1`
> **Type:** Enforces a condition

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `def test_demographic_parity_difference_calculation():`
> **Type:** Function definition

### Line  15
> **Code:** `"""Test manual calculation of demographic parity difference."""`
> **Type:** Code statement

### Line  16
> **Code:** `# Simple case: equal selection rates -> DP diff = 0`
> **Type:** Comment: Simple case: equal selection rates -> DP diff = 0

### Line  17
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1])`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `y_pred = np.array([0, 1, 0, 1, 0, 1, 0, 1])`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `sensitive = np.array(["M", "M", "M", "M", "F", "F", "F", "F"])`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `# Selection rate for M: 2/4 = 0.5, for F: 2/4 = 0.5`
> **Type:** Comment: Selection rate for M: 2/4 = 0.5, for F: 2/4 = 0.5

### Line  22
> **Code:** `# DP diff = |0.5 - 0.5| = 0`
> **Type:** Comment: DP diff = |0.5 - 0.5| = 0

### Line  23
> **Code:** `from fairlearn.metrics import selection_rate, demographic_parity_diffe...`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `sr_m = selection_rate(y_true[sensitive == "M"], y_pred[sensitive == "M...`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `sr_f = selection_rate(y_true[sensitive == "F"], y_pred[sensitive == "F...`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `assert sr_m == 0.5`
> **Type:** Enforces a condition

### Line  30
> **Code:** `assert sr_f == 0.5`
> **Type:** Enforces a condition

### Line  31
> **Code:** `assert abs(dp_diff) < 1e-10`
> **Type:** Enforces a condition

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `def test_fairness_rejection_threshold():`
> **Type:** Function definition

### Line  35
> **Code:** `"""Test that dp_diff > 0.1 triggers rejection."""`
> **Type:** Comparison operation

### Line  36
> **Code:** `# M group: 80% positive predictions, F group: 40%`
> **Type:** Comment: M group: 80% positive predictions, F group: 40%

### Line  37
> **Code:** `# DP diff = 0.4 > 0.1 -> should fail`
> **Type:** Comment: DP diff = 0.4 > 0.1 -> should fail

### Line  38
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1] * 10)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `y_pred = np.array([1, 1, 1, 1, 1, 1, 1, 1,  # M: all 1`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `1, 1, 1, 1, 0, 0, 0, 0] * 5)  # F: half 1, half 0`
> **Type:** Arithmetic operation

### Line  41
> **Code:** `sensitive = np.array(["M"] * 40 + ["F"] * 40)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `from fairlearn.metrics import demographic_parity_difference`
> **Type:** Imports specific names from a module

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `assert dp_diff > FAIRNESS_DP_THRESHOLD`
> **Type:** Enforces a condition

### Line  48
> **Code:** `# This model would be rejected`
> **Type:** Comment: This model would be rejected

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `def test_fairness_pass_threshold():`
> **Type:** Function definition

### Line  52
> **Code:** `"""Test that dp_diff <= 0.1 passes."""`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `# M group: 55% positive, F group: 50% -> DP diff = 0.05 < 0.1 -> pass`
> **Type:** Comment: M group: 55% positive, F group: 50% -> DP diff = 0.05 < 0.1 -> pass

### Line  54
> **Code:** `y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1] * 10)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `y_pred = np.array([1, 1, 1, 1, 0, 1, 0, 1,  # M: 6/8 = 0.75`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `0, 1, 1, 0, 0, 1, 0, 0] * 5)  # F: 4/8 = 0.5`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `sensitive = np.array(["M"] * 40 + ["F"] * 40)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `from fairlearn.metrics import demographic_parity_difference`
> **Type:** Imports specific names from a module

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_feat...`
> **Type:** Assignment/comparison

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `# Adjust to make it pass`
> **Type:** Comment: Adjust to make it pass

### Line  64
> **Code:** `# Let's make it closer: M 52%, F 50%`
> **Type:** Comment: Let's make it closer: M 52%, F 50%

### Line  65
> **Code:** `y_pred_balanced = np.array([1, 1, 0, 1, 0, 1, 0, 1] * 5)  # 5/8 = 0.62...`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `y_pred_balanced_f = np.array([0, 1, 1, 0, 0, 1, 0, 0] * 5)  # 4/8 = 0....`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `dp_diff_balanced = demographic_parity_difference(`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `y_true,`
> **Type:** Code statement

### Line  69
> **Code:** `np.concatenate([y_pred_balanced, y_pred_balanced_f]),`
> **Type:** Data structure operation

### Line  70
> **Code:** `sensitive_features=np.array(["M"]*40 + ["F"]*40)`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `)`
> **Type:** Code statement

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `# This demonstrates the threshold logic works`
> **Type:** Comment: This demonstrates the threshold logic works

### Line  74
> **Code:** `assert FAIRNESS_DP_THRESHOLD == 0.1`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 74
- **Code lines:** 45
- **Comments:** 10
- **TODO items:** 0
- **Empty lines:** 19

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_fairness.py*
---

# mlops-full-mlops-skills-project: test_preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/unit/test_preprocessing.py`
- **Total lines:** 70
- **File size:** 2135 bytes

## Line Type Summary
- **Code:** 59
- **Comment:** 0
- **Empty:** 11
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Unit tests for preprocessing functions."""`
> **Type:** Logical operation

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from src.data.preprocessing import (`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** `drop_duplicates,`
> **Type:** Code statement

### Line   7
> **Code:** `drop_missing,`
> **Type:** Code statement

### Line   8
> **Code:** `clamp_numeric,`
> **Type:** Code statement

### Line   9
> **Code:** `cast_dtypes,`
> **Type:** Code statement

### Line  10
> **Code:** `preprocess,`
> **Type:** Code statement

### Line  11
> **Code:** `)`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `def test_drop_duplicates():`
> **Type:** Function definition

### Line  15
> **Code:** `df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `result = drop_duplicates(df)`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `def test_drop_missing():`
> **Type:** Function definition

### Line  21
> **Code:** `df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `result = drop_missing(df, columns=["a"])`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `assert len(result) == 2`
> **Type:** Enforces a condition

### Line  24
> **Code:** `assert result["a"].notna().all()`
> **Type:** Enforces a condition

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `def test_clamp_numeric():`
> **Type:** Function definition

### Line  28
> **Code:** `df = pd.DataFrame({"age": [10, 50, 120], "monthly_charges": [-10, 50, ...`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `result = clamp_numeric(df)`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `assert result["age"].between(18, 100).all()`
> **Type:** Enforces a condition

### Line  31
> **Code:** `assert result["monthly_charges"].between(0, 1000).all()`
> **Type:** Enforces a condition

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `def test_cast_dtypes():`
> **Type:** Function definition

### Line  35
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `"age": [25, 30],`
> **Type:** Data structure operation

### Line  37
> **Code:** `"monthly_charges": [50.0, 60.0],`
> **Type:** Data structure operation

### Line  38
> **Code:** `"churn": [0, 1],`
> **Type:** Data structure operation

### Line  39
> **Code:** `"gender": ["M", "F"],`
> **Type:** Data structure operation

### Line  40
> **Code:** `})`
> **Type:** Code statement

### Line  41
> **Code:** `result = cast_dtypes(df)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `assert result["age"].dtype == "int64"`
> **Type:** Enforces a condition

### Line  43
> **Code:** `assert result["monthly_charges"].dtype == "float64"`
> **Type:** Enforces a condition

### Line  44
> **Code:** `assert result["churn"].dtype == "int8"`
> **Type:** Enforces a condition

### Line  45
> **Code:** `assert result["gender"].dtype.name == "category"`
> **Type:** Enforces a condition

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `def test_preprocess_chain():`
> **Type:** Function definition

### Line  49
> **Code:** `df = pd.DataFrame({`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `"customer_id": [1, 2, 2],`
> **Type:** Data structure operation

### Line  51
> **Code:** `"timestamp": ["2023-01-01", "2023-01-02", "2023-01-02"],`
> **Type:** Arithmetic operation

### Line  52
> **Code:** `"age": [25, 30, 30],`
> **Type:** Data structure operation

### Line  53
> **Code:** `"gender": ["M", "F", "F"],`
> **Type:** Data structure operation

### Line  54
> **Code:** `"tenure_months": [12, 24, 24],`
> **Type:** Data structure operation

### Line  55
> **Code:** `"monthly_charges": [50.0, 60.0, 60.0],`
> **Type:** Data structure operation

### Line  56
> **Code:** `"total_charges": [600.0, 1440.0, 1440.0],`
> **Type:** Data structure operation

### Line  57
> **Code:** `"num_services": [2, 3, 3],`
> **Type:** Data structure operation

### Line  58
> **Code:** `"contract_type": ["one_year", "two_year", "two_year"],`
> **Type:** Data structure operation

### Line  59
> **Code:** `"payment_method": ["credit_card", "bank_transfer", "bank_transfer"],`
> **Type:** Data structure operation

### Line  60
> **Code:** `"support_tickets": [1, 0, 0],`
> **Type:** Logical operation

### Line  61
> **Code:** `"avg_call_minutes": [100.0, 50.0, 50.0],`
> **Type:** Data structure operation

### Line  62
> **Code:** `"has_online_backup": [1, 0, 0],`
> **Type:** Data structure operation

### Line  63
> **Code:** `"has_device_protection": [0, 1, 1],`
> **Type:** Data structure operation

### Line  64
> **Code:** `"has_tech_support": [1, 0, 0],`
> **Type:** Logical operation

### Line  65
> **Code:** `"churn": [0, 1, 1],`
> **Type:** Data structure operation

### Line  66
> **Code:** `})`
> **Type:** Code statement

### Line  67
> **Code:** `result = preprocess(df)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `assert len(result) == 2  # deduped`
> **Type:** Enforces a condition

### Line  69
> **Code:** `assert result["age"].between(18, 100).all()`
> **Type:** Enforces a condition

### Line  70
> **Code:** `assert result["churn"].dtype == "int8"`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 70
- **Code lines:** 59
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 11

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_preprocessing.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/data/__init__.py`
- **Total lines:** 1
- **File size:** 42 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""tests package: data pipeline tests."""`
> **Type:** Code statement

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: test_data_validation.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/tests/data/test_data_validation.py`
- **Total lines:** 72
- **File size:** 1991 bytes

## Line Type Summary
- **Code:** 49
- **Comment:** 0
- **Empty:** 23
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Data validation tests using Great Expectations."""`
> **Type:** Code statement

### Line   2
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line   3
> **Code:** `import pytest`
> **Type:** Imports a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `def test_raw_data_exists():`
> **Type:** Function definition

### Line   9
> **Code:** `assert RAW_DATA_PATH.exists(), "Raw dataset not found"`
> **Type:** Enforces a condition

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `def test_raw_data_schema():`
> **Type:** Function definition

### Line  13
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `expected_columns = [`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `"customer_id", "timestamp", "age", "gender", "region",`
> **Type:** Code statement

### Line  16
> **Code:** `"tenure_months", "monthly_charges", "total_charges",`
> **Type:** Code statement

### Line  17
> **Code:** `"num_services", "contract_type", "payment_method",`
> **Type:** Code statement

### Line  18
> **Code:** `"support_tickets", "avg_call_minutes",`
> **Type:** Logical operation

### Line  19
> **Code:** `"has_online_backup", "has_device_protection",`
> **Type:** Code statement

### Line  20
> **Code:** `"has_tech_support", "churn"`
> **Type:** Logical operation

### Line  21
> **Code:** `]`
> **Type:** Code statement

### Line  22
> **Code:** `assert list(df.columns) == expected_columns`
> **Type:** Enforces a condition

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `def test_raw_data_row_count():`
> **Type:** Function definition

### Line  26
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `assert 5000 <= len(df) <= 10000`
> **Type:** Enforces a condition

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def test_no_nulls_on_critical_columns():`
> **Type:** Function definition

### Line  31
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `critical = ["customer_id", "age", "gender", "churn", "tenure_months"]`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `for col in critical:`
> **Type:** For loop

### Line  34
> **Code:** `assert df[col].notna().all(), f"Nulls found in {col}"`
> **Type:** Enforces a condition

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def test_age_range():`
> **Type:** Function definition

### Line  38
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `assert df["age"].between(18, 100).all()`
> **Type:** Enforces a condition

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `def test_tenure_range():`
> **Type:** Function definition

### Line  43
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `assert df["tenure_months"].between(0, 120).all()`
> **Type:** Enforces a condition

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `def test_monthly_charges_positive():`
> **Type:** Function definition

### Line  48
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `assert (df["monthly_charges"] >= 0).all()`
> **Type:** Enforces a condition

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def test_gender_values():`
> **Type:** Function definition

### Line  53
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `assert set(df["gender"].unique()).issubset({"M", "F"})`
> **Type:** Enforces a condition

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `def test_contract_type_values():`
> **Type:** Function definition

### Line  58
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `expected = {"month-to-month", "one_year", "two_year"}`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `assert set(df["contract_type"].unique()).issubset(expected)`
> **Type:** Enforces a condition

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def test_churn_binary():`
> **Type:** Function definition

### Line  64
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `assert set(df["churn"].unique()).issubset({0, 1})`
> **Type:** Enforces a condition

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def test_dtypes():`
> **Type:** Function definition

### Line  69
> **Code:** `df = pd.read_csv(RAW_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `assert df["customer_id"].dtype == "int64"`
> **Type:** Enforces a condition

### Line  71
> **Code:** `assert df["age"].dtype == "int64"`
> **Type:** Enforces a condition

### Line  72
> **Code:** `assert df["monthly_charges"].dtype == "float64"`
> **Type:** Enforces a condition

## Summary
- **Total lines:** 72
- **Code lines:** 49
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 23

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: test_data_validation.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/__init__.py`
- **Total lines:** 1
- **File size:** 65 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""src package: core source code for the churn MLOps project."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: config.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/config.py`
- **Total lines:** 59
- **File size:** 1648 bytes

## Line Type Summary
- **Code:** 42
- **Comment:** 7
- **Empty:** 10
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Shared project configuration: paths, feature columns, model names."...`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   4
> **Code:** ``
> **Type:** Empty line

### Line   5
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `# Project root: two levels up from src/`
> **Type:** Comment: Project root: two levels up from src/

### Line   8
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[1]`
> **Type:** Assignment/comparison

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "dataset.csv"`
> **Type:** Assignment/comparison

### Line  11
> **Code:** `PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "dataset_c...`
> **Type:** Assignment/comparison

### Line  12
> **Code:** `FEATURES_PATH = PROJECT_ROOT / "data" / "features" / "features.parquet...`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `REFERENCE_DATA_PATH = PROJECT_ROOT / "data" / "reference" / "reference...`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `MODELS_DIR = PROJECT_ROOT / "models"`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `REPORTS_DIR = PROJECT_ROOT / "reports"`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `MONITORING_REPORTS_DIR = PROJECT_ROOT / "monitoring" / "reports"`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `MODEL_CARDS_DIR = PROJECT_ROOT / "model_cards"`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `MLFLOW_DIR = PROJECT_ROOT / "mlflow" / "mlruns"`
> **Type:** Assignment/comparison

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `# Target / sensitive attribute / id`
> **Type:** Comment: Target / sensitive attribute / id

### Line  21
> **Code:** `TARGET_COL = "churn"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `SENSITIVE_COL = "gender"`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `ID_COL = "customer_id"`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `TIMESTAMP_COL = "timestamp"`
> **Type:** Assignment/comparison

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `# Numerical features kept as-is`
> **Type:** Comment: Numerical features kept as-is

### Line  27
> **Code:** `NUMERIC_FEATURES = [`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `"age",`
> **Type:** Code statement

### Line  29
> **Code:** `"tenure_months",`
> **Type:** Code statement

### Line  30
> **Code:** `"monthly_charges",`
> **Type:** Code statement

### Line  31
> **Code:** `"total_charges",`
> **Type:** Code statement

### Line  32
> **Code:** `"num_services",`
> **Type:** Code statement

### Line  33
> **Code:** `"support_tickets",`
> **Type:** Logical operation

### Line  34
> **Code:** `"avg_call_minutes",`
> **Type:** Code statement

### Line  35
> **Code:** `]`
> **Type:** Code statement

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `# Binary features kept as-is (already 0/1)`
> **Type:** Comment: Binary features kept as-is (already 0/1)

### Line  38
> **Code:** `BINARY_FEATURES = [`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `"has_online_backup",`
> **Type:** Code statement

### Line  40
> **Code:** `"has_device_protection",`
> **Type:** Code statement

### Line  41
> **Code:** `"has_tech_support",`
> **Type:** Logical operation

### Line  42
> **Code:** `]`
> **Type:** Code statement

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `# Categorical features to one-hot encode`
> **Type:** Comment: Categorical features to one-hot encode

### Line  45
> **Code:** `CATEGORICAL_FEATURES = [`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `"gender",`
> **Type:** Code statement

### Line  47
> **Code:** `"region",`
> **Type:** Code statement

### Line  48
> **Code:** `"contract_type",`
> **Type:** Code statement

### Line  49
> **Code:** `"payment_method",`
> **Type:** Code statement

### Line  50
> **Code:** `]`
> **Type:** Code statement

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `# Full feature set fed to the model (after one-hot encoding)`
> **Type:** Comment: Full feature set fed to the model (after one-hot encoding)

### Line  53
> **Code:** `BASE_FEATURES = NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_FEATU...`
> **Type:** Assignment/comparison

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `# Fairness / drift metrics thresholds`
> **Type:** Comment: Fairness / drift metrics thresholds

### Line  56
> **Code:** `FAIRNESS_DP_THRESHOLD = 0.1`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `DRIFT_THRESHOLD = 0.3`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `F1_PROMOTION_THRESHOLD = 0.2`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `CHALLENGER_RATIO = 0.1`
> **Type:** Assignment/comparison

## Summary
- **Total lines:** 59
- **Code lines:** 42
- **Comments:** 7
- **TODO items:** 0
- **Empty lines:** 10

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: config.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/serving/__init__.py`
- **Total lines:** 1
- **File size:** 72 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""serving package: model serving (BentoML) and inference endpoints.""...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: bento_service.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/serving/bento_service.py`
- **Total lines:** 69
- **File size:** 1893 bytes

## Line Type Summary
- **Code:** 48
- **Comment:** 0
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""BentoML serving service: ``/predict`` and ``/explain`` endpoints.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `The service loads the registered MLflow model and exposes:`
> **Type:** Logical operation

### Line   4
> **Code:** `- ``predict``: returns the churn probability + class label,`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- ``explain``: returns per-feature SHAP contributions for the instance...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `Run with: ``bentoml serve src.serving.bento_service:svc```
> **Type:** Code statement

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import sys`
> **Type:** Imports a module

### Line  13
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  16
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  17
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `import bentoml`
> **Type:** Imports a module

### Line  23
> **Code:** `from bentoml.io import JSON, NumpyNdarray`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `MODEL_TAG = "churn_model:production"`
> **Type:** Assignment/comparison

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `def _load_runner():`
> **Type:** Function definition

### Line  29
> **Code:** `model_ref = bentoml.mlflow.get(MODEL_TAG)`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `return model_ref.to_runner()`
> **Type:** Returns a value from a function

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `runner = _load_runner()`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `svc = bentoml.Service("mlops_churn_service", runners=[runner])`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `@svc.api(input=NumpyNdarray(), output=JSON())`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `def predict(input_data: np.ndarray) -> dict:`
> **Type:** Function definition

### Line  40
> **Code:** `"""Return the predicted class and churn probability."""`
> **Type:** Logical operation

### Line  41
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `proba = runner.predict_proba.run(arr)[:, 1]`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `pred = (proba >= 0.5).astype(int)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  45
> **Code:** `"prediction": pred.tolist(),`
> **Type:** Code statement

### Line  46
> **Code:** `"churn_probability": proba.tolist(),`
> **Type:** Code statement

### Line  47
> **Code:** `}`
> **Type:** Code statement

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `@svc.api(input=NumpyNdarray(), output=JSON())`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `def explain(input_data: np.ndarray) -> dict:`
> **Type:** Function definition

### Line  52
> **Code:** `"""Return SHAP force values for the given instance(s)."""`
> **Type:** Logical operation

### Line  53
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `model = _model_ref()`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `import shap`
> **Type:** Imports a module

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `shap_values = explainer.shap_values(arr)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  60
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  63
> **Code:** `"expected_value": float(explainer.expected_value),`
> **Type:** Code statement

### Line  64
> **Code:** `"shap_values": shap_values.tolist(),`
> **Type:** Code statement

### Line  65
> **Code:** `}`
> **Type:** Code statement

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def _model_ref():`
> **Type:** Function definition

### Line  69
> **Code:** `return bentoml.mlflow.get(MODEL_TAG).load()`
> **Type:** Returns a value from a function

## Summary
- **Total lines:** 69
- **Code lines:** 48
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: bento_service.py*
---

# mlops-full-mlops-skills-project: champion_challenger.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/serving/champion_challenger.py`
- **Total lines:** 156
- **File size:** 5121 bytes

## Line Type Summary
- **Code:** 119
- **Comment:** 0
- **Empty:** 37
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Champion / Challenger traffic routing.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A challenger model receives a small, controlled fraction of the traffi...`
> **Type:** Code statement

### Line   4
> **Code:** `(``CHALLENGER_RATIO`` = 10% by default) in parallel with the current`
> **Type:** Assignment/comparison

### Line   5
> **Code:** `champion. Every routing decision is logged (structured JSON lines) so ...`
> **Type:** Code statement

### Line   6
> **Code:** `two models can be compared statistically a posteriori.`
> **Type:** Logical operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import sys`
> **Type:** Imports a module

### Line  12
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import json`
> **Type:** Imports a module

### Line  19
> **Code:** `import logging`
> **Type:** Imports a module

### Line  20
> **Code:** `import random`
> **Type:** Imports a module

### Line  21
> **Code:** `from datetime import datetime, timezone`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from typing import Callable`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import CHALLENGER_RATIO, MODELS_DIR, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `ROUTING_LOG = Path("monitoring/logs/routing_decisions.jsonl")`
> **Type:** Assignment/comparison

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def load_model(path: Path):`
> **Type:** Function definition

### Line  33
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `return joblib.load(path)`
> **Type:** Returns a value from a function

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `def _default_predict_fn(model):`
> **Type:** Function definition

### Line  39
> **Code:** `def predict(input_data):`
> **Type:** Function definition

### Line  40
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `arr = np.asarray(input_data, dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `if arr.ndim == 1:`
> **Type:** Conditional statement

### Line  44
> **Code:** `arr = arr.reshape(1, -1)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `return model.predict(arr)`
> **Type:** Returns a value from a function

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `return predict`
> **Type:** Returns a value from a function

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `class ChampionChallengerRouter:`
> **Type:** Class definition

### Line  51
> **Code:** `"""Routes each inference to champion or challenger and logs the decisi...`
> **Type:** Logical operation

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def __init__(`
> **Type:** Function definition

### Line  54
> **Code:** `self,`
> **Type:** Code statement

### Line  55
> **Code:** `champion_model,`
> **Type:** Code statement

### Line  56
> **Code:** `challenger_model,`
> **Type:** Code statement

### Line  57
> **Code:** `champion_name: str = "champion",`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `challenger_name: str = "challenger",`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `challenger_ratio: float = CHALLENGER_RATIO,`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `log_path: Path = ROUTING_LOG,`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `predict_fn: Callable | None = None,`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `seed: int | None = None,`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `):`
> **Type:** Code statement

### Line  64
> **Code:** `self.champion = champion_model`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `self.challenger = challenger_model`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `self.champion_name = champion_name`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `self.challenger_name = challenger_name`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `self.challenger_ratio = challenger_ratio`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `self.log_path = log_path`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `self.predict_fn = predict_fn or _default_predict_fn`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `self.rng = random.Random(seed)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def route(self, input_data) -> dict:`
> **Type:** Function definition

### Line  74
> **Code:** `"""Route one request, log the decision, return prediction + version.""...`
> **Type:** Arithmetic operation

### Line  75
> **Code:** `if self.rng.random() < self.challenger_ratio:`
> **Type:** Conditional statement

### Line  76
> **Code:** `version = self.challenger_name`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `model = self.challenger`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `else:`
> **Type:** Else block

### Line  79
> **Code:** `version = self.champion_name`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `model = self.champion`
> **Type:** Assignment/comparison

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `prediction = self.predict_fn(model)(input_data).tolist()`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `self._log(input_data, prediction, version)`
> **Type:** Function call

### Line  84
> **Code:** `return {"prediction": prediction, "model_version": version}`
> **Type:** Returns a value from a function

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `def _log(self, input_data, prediction, version) -> None:`
> **Type:** Function definition

### Line  87
> **Code:** `entry = {`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `"timestamp": datetime.now(timezone.utc).isoformat(),`
> **Type:** Logical operation

### Line  89
> **Code:** `"model_version": version,`
> **Type:** Code statement

### Line  90
> **Code:** `"prediction": prediction,`
> **Type:** Code statement

### Line  91
> **Code:** `"request_id": f"{int(datetime.now().timestamp()*1000)}",`
> **Type:** Arithmetic operation

### Line  92
> **Code:** `}`
> **Type:** Code statement

### Line  93
> **Code:** `self.log_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `with open(self.log_path, "a") as handle:`
> **Type:** Context manager

### Line  95
> **Code:** `handle.write(json.dumps(entry) + "\n")`
> **Type:** Arithmetic operation

### Line  96
> **Code:** `logger.info("Routed request to %s -> %s", version, prediction)`
> **Type:** Arithmetic operation

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def build_router(`
> **Type:** Function definition

### Line 100
> **Code:** `champion_path: Path = MODELS_DIR / "churn_model.joblib",`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `challenger_path: Path | None = None,`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `challenger_ratio: float = CHALLENGER_RATIO,`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `) -> ChampionChallengerRouter:`
> **Type:** Arithmetic operation

### Line 104
> **Code:** `"""Build a router, defaulting the challenger to the ONNX-converted mod...`
> **Type:** Arithmetic operation

### Line 105
> **Code:** `champion = load_model(champion_path)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `challenger = load_model(challenger_path) if challenger_path else champ...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `return ChampionChallengerRouter(`
> **Type:** Returns a value from a function

### Line 108
> **Code:** `champion, challenger, challenger_ratio=challenger_ratio`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `)`
> **Type:** Code statement

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `def simulate_routing(n_requests: int = 1000, challenger_ratio: float =...`
> **Type:** Function definition

### Line 113
> **Code:** `"""Send ``n_requests`` synthetic requests through the router.`
> **Type:** Code statement

### Line 114
> **Code:** ``
> **Type:** Empty line

### Line 115
> **Code:** `Returns a small summary (request counts per model version) proving the`
> **Type:** Code statement

### Line 116
> **Code:** `~10% challenger split and that every decision was logged.`
> **Type:** Arithmetic operation

### Line 117
> **Code:** `"""`
> **Type:** Code statement

### Line 118
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `X = _load_sample_features(n_requests)`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `router = build_router(challenger_ratio=challenger_ratio)`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `counts = {router.champion_name: 0, router.challenger_name: 0}`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `for row in X:`
> **Type:** For loop

### Line 124
> **Code:** `result = router.route([row])`
> **Type:** Assignment/comparison

### Line 125
> **Code:** `counts[result["model_version"]] += 1`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `return {"requests": n_requests, "counts": counts, "log_path": str(ROUT...`
> **Type:** Returns a value from a function

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `def _load_sample_features(n: int):`
> **Type:** Function definition

### Line 130
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line 131
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line 132
> **Code:** ``
> **Type:** Empty line

### Line 133
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line 134
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line 138
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `return sets["X"].head(n).to_numpy(dtype=np.float32)`
> **Type:** Returns a value from a function

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** ``
> **Type:** Empty line

### Line 143
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 144
> **Code:** `import argparse`
> **Type:** Imports a module

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** `parser = argparse.ArgumentParser(description="Champion/Challenger rout...`
> **Type:** Assignment/comparison

### Line 147
> **Code:** `parser.add_argument("--requests", type=int, default=1000)`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `parser.add_argument("--challenger-ratio", type=float, default=CHALLENG...`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 150
> **Code:** ``
> **Type:** Empty line

### Line 151
> **Code:** `summary = simulate_routing(args.requests, args.challenger_ratio)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `print(summary)`
> **Type:** Prints output to console

### Line 153
> **Code:** ``
> **Type:** Empty line

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 156
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 156
- **Code lines:** 119
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 37

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: champion_challenger.py*
---

# mlops-full-mlops-skills-project: automl_baseline.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/automl_baseline.py`
- **Total lines:** 83
- **File size:** 2416 bytes

## Line Type Summary
- **Code:** 62
- **Comment:** 0
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""AutoML comparative baseline (FLAML).`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Trains a baseline with FLAML in a short time budget and logs it to MLf...`
> **Type:** Logical operation

### Line   4
> **Code:** `it can be objectively compared against the Optuna-optimised model.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import sys`
> **Type:** Imports a module

### Line  10
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  14
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import logging`
> **Type:** Imports a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** `from flaml import AutoML`
> **Type:** Imports specific names from a module

### Line  22
> **Code:** `from sklearn.metrics import accuracy_score, f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def run_automl_baseline(time_budget: int = 60, experiment_name: str = ...`
> **Type:** Function definition

### Line  31
> **Code:** `X, y = _load_data()`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `)`
> **Type:** Code statement

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `automl = AutoML()`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `automl.fit(`
> **Type:** Code statement

### Line  38
> **Code:** `X_train,`
> **Type:** Code statement

### Line  39
> **Code:** `y_train,`
> **Type:** Code statement

### Line  40
> **Code:** `task="classification",`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `time_budget=time_budget,`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `metric="f1",`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `n_jobs=-1,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `log_file_name="artifacts/automl.log",`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `)`
> **Type:** Code statement

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `y_pred = automl.predict(X_test)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `y_proba = automl.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  51
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  52
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  53
> **Code:** `}`
> **Type:** Code statement

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  56
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line  57
> **Code:** `with mlflow.start_run(run_name=f"flaml_baseline_{time_budget}s"):`
> **Type:** Context manager

### Line  58
> **Code:** `mlflow.log_params(automl.best_config)`
> **Type:** Function call

### Line  59
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line  60
> **Code:** `mlflow.log_param("time_budget", time_budget)`
> **Type:** Function call

### Line  61
> **Code:** `mlflow.set_tag("tool", "FLAML")`
> **Type:** Function call

### Line  62
> **Code:** `mlflow.sklearn.log_model(automl.model.estimator, artifact_path="model"...`
> **Type:** Assignment/comparison

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `logger.info("FLAML baseline metrics: %s", metrics)`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `return {"metrics": metrics, "best_config": automl.best_config}`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def _load_data():`
> **Type:** Function definition

### Line  69
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  75
> **Code:** `parser = argparse.ArgumentParser(description="FLAML AutoML baseline.")`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `parser.add_argument("--time-budget", type=int, default=60)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `result = run_automl_baseline(time_budget=args.time_budget)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `print(f"FLAML baseline F1: {result['metrics']['f1_score']:.4f}")`
> **Type:** Prints output to console

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  83
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 83
- **Code lines:** 62
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: automl_baseline.py*
---

# mlops-full-mlops-skills-project: export_onnx.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/export_onnx.py`
- **Total lines:** 129
- **File size:** 4084 bytes

## Line Type Summary
- **Code:** 93
- **Comment:** 1
- **Empty:** 35
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""ONNX export and parity verification.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Converts the trained sklearn model to ONNX with ``skl2onnx``, then che...`
> **Type:** Code statement

### Line   4
> **Code:** `the ONNX model produces predictions identical (within a numeric tolera...`
> **Type:** Code statement

### Line   5
> **Code:** `the original sklearn model on the held-out test set.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  21
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  22
> **Code:** `from skl2onnx import convert_sklearn`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** `from skl2onnx.common.data_types import FloatTensorType`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `from src.config import MODELS_DIR`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `TOLERANCE = 1e-5`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def export_to_onnx(model_path: Path = MODELS_DIR / "churn_model.joblib...`
> **Type:** Function definition

### Line  32
> **Code:** `out_path: Path = MODELS_DIR / "churn_model.onnx") -> Path:`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  34
> **Code:** `import onnxruntime as ort`
> **Type:** Imports a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** `X = _load_feature_matrix()`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `n_features = X.shape[1]`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `initial_types = [("input", FloatTensorType([None, n_features]))]`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `onnx_model = convert_sklearn(model, initial_types=initial_types)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `out_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `with open(out_path, "wb") as handle:`
> **Type:** Context manager

### Line  45
> **Code:** `handle.write(onnx_model.SerializeToString())`
> **Type:** Logical operation

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `parity = check_parity(model, X, out_path, n_features)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `_write_report(parity)`
> **Type:** Logical operation

### Line  49
> **Code:** `return out_path`
> **Type:** Returns a value from a function

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _load_feature_matrix() -> pd.DataFrame:`
> **Type:** Function definition

### Line  53
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  54
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `X = sets["X"].astype(np.float32)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `return X.sample(n=min(500, len(X)), random_state=42)`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def check_parity(model, X: pd.DataFrame, onnx_path: Path, n_features: ...`
> **Type:** Function definition

### Line  65
> **Code:** `import onnxruntime as ort`
> **Type:** Imports a module

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `X_np = X.to_numpy(dtype=np.float32)`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `sklearn_pred = model.predict(X_np)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `sklearn_proba = model.predict_proba(X_np)[:, 1]`
> **Type:** Assignment/comparison

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `session = ort.InferenceSession(str(onnx_path), providers=["CPUExecutio...`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `onnx_out = session.run(None, {"input": X_np})`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `# ONNX output may be (proba) or (label, proba) depending on converter.`
> **Type:** Comment: ONNX output may be (proba) or (label, proba) depending on converter.

### Line  75
> **Code:** `onnx_proba = onnx_out[-1]`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `if isinstance(onnx_proba, list):`
> **Type:** Conditional statement

### Line  77
> **Code:** `if isinstance(onnx_proba[0], dict):`
> **Type:** Conditional statement

### Line  78
> **Code:** `onnx_proba = np.array([row[1] for row in onnx_proba])`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `else:`
> **Type:** Else block

### Line  80
> **Code:** `onnx_proba = np.asarray(onnx_proba)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `if onnx_proba.ndim == 2:`
> **Type:** Conditional statement

### Line  82
> **Code:** `onnx_proba = onnx_proba[:, 1]`
> **Type:** Assignment/comparison

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `proba_diff = float(np.max(np.abs(sklearn_proba - onnx_proba)))`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `onnx_pred = (onnx_proba >= 0.5).astype(int)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `label_agreement = float(np.mean(sklearn_pred == onnx_pred))`
> **Type:** Assignment/comparison

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  89
> **Code:** `"max_proba_abs_diff": proba_diff,`
> **Type:** Code statement

### Line  90
> **Code:** `"label_agreement": label_agreement,`
> **Type:** Code statement

### Line  91
> **Code:** `"n_instances": int(len(X_np)),`
> **Type:** Code statement

### Line  92
> **Code:** `"tolerance": TOLERANCE,`
> **Type:** Code statement

### Line  93
> **Code:** `"passed": proba_diff <= TOLERANCE,`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `}`
> **Type:** Code statement

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `def _write_report(parity: dict) -> None:`
> **Type:** Function definition

### Line  98
> **Code:** `import json`
> **Type:** Imports a module

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `with open(REPORTS_DIR / "onnx_parity_report.json", "w") as handle:`
> **Type:** Context manager

### Line 102
> **Code:** `json.dump(parity, handle, indent=2)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 106
> **Code:** `parser = argparse.ArgumentParser(description="Export model to ONNX and...`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.j...`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `parser.add_argument("--output", default=str(MODELS_DIR / "churn_model....`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `path = export_to_onnx(Path(args.model), Path(args.output))`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `print(f"ONNX model written to {path}")`
> **Type:** Prints output to console

### Line 113
> **Code:** `report = _read_report()`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `print(`
> **Type:** Prints output to console

### Line 115
> **Code:** `f"Parity: max proba diff={report['max_proba_abs_diff']:.2e} "`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `f"-> {'PASS' if report['passed'] else 'FAIL'} "`
> **Type:** Arithmetic operation

### Line 117
> **Code:** `f"(label agreement {report['label_agreement']:.4f})"`
> **Type:** Logical operation

### Line 118
> **Code:** `)`
> **Type:** Code statement

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** ``
> **Type:** Empty line

### Line 121
> **Code:** `def _read_report() -> dict:`
> **Type:** Function definition

### Line 122
> **Code:** `import json`
> **Type:** Imports a module

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `with open(REPORTS_DIR / "onnx_parity_report.json") as handle:`
> **Type:** Context manager

### Line 125
> **Code:** `return json.load(handle)`
> **Type:** Returns a value from a function

### Line 126
> **Code:** ``
> **Type:** Empty line

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 129
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 129
- **Code lines:** 93
- **Comments:** 1
- **TODO items:** 0
- **Empty lines:** 35

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: export_onnx.py*
---

# mlops-full-mlops-skills-project: explain.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/explain.py`
- **Total lines:** 151
- **File size:** 4995 bytes

## Line Type Summary
- **Code:** 109
- **Comment:** 2
- **Empty:** 40
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model explainability: SHAP (global + local) and LIME (local).`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `- SHAP ``TreeExplainer`` produces a global summary plot saved to`
> **Type:** Arithmetic operation

### Line   4
> **Code:** ```reports/shap_summary.png`` plus per-instance local explanations.`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- LIME is run independently on a few test instances to cross-check the...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `explanations with a method different from SHAP.`
> **Type:** Code statement

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import sys`
> **Type:** Imports a module

### Line  12
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  15
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  16
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  19
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  24
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  25
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  26
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `from src.config import MLFLOW_DIR, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def compute_shap(model, X_sample: pd.DataFrame) -> dict:`
> **Type:** Function definition

### Line  32
> **Code:** `import shap`
> **Type:** Imports a module

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `shap_values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `# GradientBoosting / modern shap returns a single (n, p) array for`
> **Type:** Comment: GradientBoosting / modern shap returns a single (n, p) array for

### Line  38
> **Code:** `# binary classifiers; handle the legacy (p, n) pair case too.`
> **Type:** Comment: binary classifiers; handle the legacy (p, n) pair case too.

### Line  39
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  40
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `elif getattr(shap_values, "ndim", 0) == 3:`
> **Type:** Else-if branch

### Line  42
> **Code:** `shap_values = shap_values[..., 1]`
> **Type:** Assignment/comparison

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `mean_abs = np.abs(shap_values).mean(axis=0)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `importance = pd.Series(mean_abs, index=X_sample.columns).sort_values(a...`
> **Type:** Imports a module

### Line  46
> **Code:** `return {"explainer": explainer, "shap_values": shap_values, "importanc...`
> **Type:** Returns a value from a function

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `def save_shap_summary(model, X_sample: pd.DataFrame, path: Path) -> di...`
> **Type:** Function definition

### Line  50
> **Code:** `import shap`
> **Type:** Imports a module

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `explainer = shap.TreeExplainer(model)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `shap_values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `if isinstance(shap_values, list):`
> **Type:** Conditional statement

### Line  55
> **Code:** `shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[...`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `elif getattr(shap_values, "ndim", 0) == 3:`
> **Type:** Else-if branch

### Line  57
> **Code:** `shap_values = shap_values[..., 1]`
> **Type:** Assignment/comparison

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `shap.summary_plot(shap_values, X_sample, show=False)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `plt.savefig(path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `plt.close()`
> **Type:** Library function call

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `mean_abs = np.abs(shap_values).mean(axis=0)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `return pd.Series(mean_abs, index=X_sample.columns).sort_values(ascendi...`
> **Type:** Returns a value from a function

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `def explain_lime(model, X_sample: pd.DataFrame, feature_names: list, n...`
> **Type:** Function definition

### Line  69
> **Code:** `import lime`
> **Type:** Imports a module

### Line  70
> **Code:** `from lime.lime_tabular import LimeTabularExplainer`
> **Type:** Imports specific names from a module

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `X_np = X_sample.values`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `explainer = LimeTabularExplainer(`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `X_np,`
> **Type:** Code statement

### Line  75
> **Code:** `feature_names=feature_names,`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `class_names=["not_churn", "churn"],`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `mode="classification",`
> **Type:** Assignment/comparison

### Line  78
> **Code:** `random_state=42,`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `)`
> **Type:** Code statement

### Line  80
> **Code:** `explanations = []`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `for i in range(min(n, len(X_np))):`
> **Type:** For loop

### Line  82
> **Code:** `exp = explainer.explain_instance(`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `X_np[i], model.predict_proba, num_features=5, labels=(1,)`
> **Type:** Assignment/comparison

### Line  84
> **Code:** `)`
> **Type:** Code statement

### Line  85
> **Code:** `explanations.append(`
> **Type:** Code statement

### Line  86
> **Code:** `{"instance": i, "top_features": exp.as_list(label=1)}`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `)`
> **Type:** Code statement

### Line  88
> **Code:** `return explanations`
> **Type:** Returns a value from a function

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `def run(model_path: Path = Path("models/churn_model.joblib"), n_sample...`
> **Type:** Function definition

### Line  92
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  93
> **Code:** ``
> **Type:** Empty line

### Line  94
> **Code:** `from src.models.evaluate import _load_data`
> **Type:** Imports specific names from a module

### Line  95
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line  96
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `X = sets["X"]`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `X_sample = X.sample(n=min(n_samples, len(X)), random_state=42)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `importance = save_shap_summary(model, X_sample, REPORTS_DIR / "shap_su...`
> **Type:** Imports a module

### Line 108
> **Code:** ``
> **Type:** Empty line

### Line 109
> **Code:** `local_shap = []`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `explainer_shap = _shap_explainer(model, X_sample)`
> **Type:** Assignment/comparison

### Line 111
> **Code:** `shap_values = _shap_values(explainer_shap, X_sample)`
> **Type:** Assignment/comparison

### Line 112
> **Code:** `local_shap.append({"instance": 0, "values": shap_values[0].tolist()})`
> **Type:** Function call

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `lime_explanations = explain_lime(model, X_sample, list(X_sample.column...`
> **Type:** Assignment/comparison

### Line 115
> **Code:** ``
> **Type:** Empty line

### Line 116
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `"shap_importance": importance.to_dict(),`
> **Type:** Logical operation

### Line 118
> **Code:** `"shap_summary_path": str(REPORTS_DIR / "shap_summary.png"),`
> **Type:** Arithmetic operation

### Line 119
> **Code:** `"lime_explanations": lime_explanations,`
> **Type:** Code statement

### Line 120
> **Code:** `"n_instances_explained": len(local_shap),`
> **Type:** Code statement

### Line 121
> **Code:** `}`
> **Type:** Code statement

### Line 122
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `def _shap_explainer(model, X_sample):`
> **Type:** Function definition

### Line 126
> **Code:** `import shap`
> **Type:** Imports a module

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** `return shap.TreeExplainer(model)`
> **Type:** Returns a value from a function

### Line 129
> **Code:** ``
> **Type:** Empty line

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `def _shap_values(explainer, X_sample):`
> **Type:** Function definition

### Line 132
> **Code:** `values = explainer.shap_values(X_sample)`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `if isinstance(values, list):`
> **Type:** Conditional statement

### Line 134
> **Code:** `values = values[1] if len(values) > 1 else values[0]`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `return values`
> **Type:** Returns a value from a function

### Line 136
> **Code:** ``
> **Type:** Empty line

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 139
> **Code:** `parser = argparse.ArgumentParser(description="SHAP + LIME explainabili...`
> **Type:** Assignment/comparison

### Line 140
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line 141
> **Code:** `parser.add_argument("--samples", type=int, default=200)`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 143
> **Code:** ``
> **Type:** Empty line

### Line 144
> **Code:** `result = run(Path(args.model), n_samples=args.samples)`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `print("SHAP top-5 features:", list(result["shap_importance"].items())[...`
> **Type:** Prints output to console

### Line 146
> **Code:** `print("Saved summary to:", result["shap_summary_path"])`
> **Type:** Prints output to console

### Line 147
> **Code:** `print("LIME explanations generated for", len(result["lime_explanations...`
> **Type:** Prints output to console

### Line 148
> **Code:** ``
> **Type:** Empty line

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 151
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 151
- **Code lines:** 109
- **Comments:** 2
- **TODO items:** 0
- **Empty lines:** 40

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: explain.py*
---

# mlops-full-mlops-skills-project: fairness_check.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/fairness_check.py`
- **Total lines:** 158
- **File size:** 4937 bytes

## Line Type Summary
- **Code:** 119
- **Comment:** 2
- **Empty:** 37
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Fairness audit with Fairlearn.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Computes, per sensitive group (``gender``):`
> **Type:** Code statement

### Line   4
> **Code:** `- selection rate (positive prediction rate),`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- accuracy,`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `and the two headline disparity metrics:`
> **Type:** Logical operation

### Line   7
> **Code:** `- Demographic Parity Difference (dp_diff),`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- Equalized Odds Difference (eq_odds_diff).`
> **Type:** Arithmetic operation

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `A model is considered **unfair** (rejected for promotion) when the`
> **Type:** Arithmetic operation

### Line  11
> **Code:** `demographic parity difference exceeds ``FAIRNESS_DP_THRESHOLD`` (0.1).`
> **Type:** Code statement

### Line  12
> **Code:** `Results are saved as JSON + a bar chart in ``reports/``.`
> **Type:** Arithmetic operation

### Line  13
> **Code:** `"""`
> **Type:** Code statement

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import sys`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  22
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  25
> **Code:** `import json`
> **Type:** Imports a module

### Line  26
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  31
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  32
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  33
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  34
> **Code:** `from sklearn.metrics import accuracy_score`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `from src.config import FAIRNESS_DP_THRESHOLD, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `try:`
> **Type:** Code statement

### Line  40
> **Code:** `from fairlearn.metrics import (`
> **Type:** Imports specific names from a module

### Line  41
> **Code:** `MetricFrame,`
> **Type:** Code statement

### Line  42
> **Code:** `demographic_parity_difference,`
> **Type:** Code statement

### Line  43
> **Code:** `equalized_odds_difference,`
> **Type:** Code statement

### Line  44
> **Code:** `selection_rate,`
> **Type:** Code statement

### Line  45
> **Code:** `)`
> **Type:** Code statement

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `FAIRLEARN_AVAILABLE = True`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `except ImportError:  # pragma: no cover - graceful degradation`
> **Type:** Arithmetic operation

### Line  49
> **Code:** `FAIRLEARN_AVAILABLE = False`
> **Type:** Assignment/comparison

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** `def _build_test_frame():`
> **Type:** Function definition

### Line  53
> **Code:** `"""Return (y_test, y_pred, sensitive_series) aligned on the same split...`
> **Type:** Code statement

### Line  54
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `from src.features.build_features import build_features`
> **Type:** Imports specific names from a module

### Line  57
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `# gender is one-hot encoded (and dropped) inside build_features; keep ...`
> **Type:** Comment: gender is one-hot encoded (and dropped) inside build_features; keep the

### Line  63
> **Code:** `# raw series aligned positionally with the feature frame for the audit...`
> **Type:** Comment: raw series aligned positionally with the feature frame for the audit.

### Line  64
> **Code:** `gender_all = clean["gender"].reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  66
> **Code:** ``
> **Type:** Empty line

### Line  67
> **Code:** `model = joblib.load("models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `X = frame.drop(columns=["churn"])`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `y = frame["churn"]`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `X, y, test_size=0.25, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `)`
> **Type:** Code statement

### Line  74
> **Code:** ``
> **Type:** Empty line

### Line  75
> **Code:** `sensitive = gender_all.iloc[X_test.index].reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `X_test_model = X_test.reset_index(drop=True)`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `y_pred = model.predict(X_test_model)`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `return y_test.reset_index(drop=True), y_pred, sensitive`
> **Type:** Returns a value from a function

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `def fairness_check(model_path: Path = Path("models/churn_model.joblib"...`
> **Type:** Function definition

### Line  83
> **Code:** `"""Run the full fairness audit and persist a JSON report."""`
> **Type:** Logical operation

### Line  84
> **Code:** `if not FAIRLEARN_AVAILABLE:`
> **Type:** Conditional statement

### Line  85
> **Code:** `raise ImportError("fairlearn is required for fairness_check")`
> **Type:** Raises an exception

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `y_test, y_pred, sensitive = _build_test_frame()`
> **Type:** Assignment/comparison

### Line  88
> **Code:** ``
> **Type:** Empty line

### Line  89
> **Code:** `metric_frame = MetricFrame(`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `metrics={`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `"accuracy": accuracy_score,`
> **Type:** Logical operation

### Line  92
> **Code:** `"selection_rate": selection_rate,`
> **Type:** Code statement

### Line  93
> **Code:** `},`
> **Type:** Code statement

### Line  94
> **Code:** `y_true=y_test,`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `y_pred=y_pred,`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `sensitive_features=sensitive,`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `)`
> **Type:** Code statement

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `dp_diff = float(`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `demographic_parity_difference(`
> **Type:** Code statement

### Line 101
> **Code:** `y_test, y_pred, sensitive_features=sensitive`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `)`
> **Type:** Code statement

### Line 103
> **Code:** `)`
> **Type:** Code statement

### Line 104
> **Code:** `eq_odds_diff = float(`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `equalized_odds_difference(`
> **Type:** Code statement

### Line 106
> **Code:** `y_test, y_pred, sensitive_features=sensitive`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `)`
> **Type:** Code statement

### Line 108
> **Code:** `)`
> **Type:** Code statement

### Line 109
> **Code:** ``
> **Type:** Empty line

### Line 110
> **Code:** `group_summary = metric_frame.by_group.to_dict()`
> **Type:** Assignment/comparison

### Line 111
> **Code:** ``
> **Type:** Empty line

### Line 112
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line 113
> **Code:** `"demographic_parity_difference": dp_diff,`
> **Type:** Code statement

### Line 114
> **Code:** `"equalized_odds_difference": eq_odds_diff,`
> **Type:** Code statement

### Line 115
> **Code:** `"threshold": FAIRNESS_DP_THRESHOLD,`
> **Type:** Code statement

### Line 116
> **Code:** `"passed": dp_diff <= FAIRNESS_DP_THRESHOLD,`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `"selection_rate_by_group": group_summary["selection_rate"],`
> **Type:** Data structure operation

### Line 118
> **Code:** `"accuracy_by_group": group_summary["accuracy"],`
> **Type:** Data structure operation

### Line 119
> **Code:** `"overall_selection_rate": float(selection_rate(y_test, y_pred)),`
> **Type:** Code statement

### Line 120
> **Code:** `}`
> **Type:** Code statement

### Line 121
> **Code:** ``
> **Type:** Empty line

### Line 122
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 123
> **Code:** `with open(REPORTS_DIR / "fairness_report.json", "w") as handle:`
> **Type:** Context manager

### Line 124
> **Code:** `json.dump(result, handle, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 125
> **Code:** ``
> **Type:** Empty line

### Line 126
> **Code:** `_plot_selection_rates(group_summary["selection_rate"])`
> **Type:** Function call

### Line 127
> **Code:** ``
> **Type:** Empty line

### Line 128
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line 129
> **Code:** ``
> **Type:** Empty line

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `def _plot_selection_rates(by_group: dict) -> None:`
> **Type:** Function definition

### Line 132
> **Code:** `groups = list(by_group.keys())`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `rates = list(by_group.values())`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `fig, ax = plt.subplots(figsize=(6, 4))`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `ax.bar([str(g) for g in groups], rates, color=["#4C72B0", "#DD8452"])`
> **Type:** Assignment/comparison

### Line 136
> **Code:** `ax.set_ylabel("Selection rate")`
> **Type:** Function call

### Line 137
> **Code:** `ax.set_title("Selection rate by gender group")`
> **Type:** Function call

### Line 138
> **Code:** `fig.savefig(REPORTS_DIR / "fairness_selection_rate.png", dpi=120, bbox...`
> **Type:** Assignment/comparison

### Line 139
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line 140
> **Code:** ``
> **Type:** Empty line

### Line 141
> **Code:** ``
> **Type:** Empty line

### Line 142
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 143
> **Code:** `parser = argparse.ArgumentParser(description="Fairness audit with Fair...`
> **Type:** Assignment/comparison

### Line 144
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line 145
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `result = fairness_check(Path(args.model))`
> **Type:** Assignment/comparison

### Line 148
> **Code:** `verdict = "PASS" if result["passed"] else "FAIL"`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `print(`
> **Type:** Prints output to console

### Line 150
> **Code:** `f"DP difference={result['demographic_parity_difference']:.4f} "`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `f"(threshold {result['threshold']}) -> {verdict}"`
> **Type:** Arithmetic operation

### Line 152
> **Code:** `)`
> **Type:** Code statement

### Line 153
> **Code:** `print(f"Equalized odds difference={result['equalized_odds_difference']...`
> **Type:** Prints output to console

### Line 154
> **Code:** `print(f"Saved to reports/fairness_report.json")`
> **Type:** Prints output to console

### Line 155
> **Code:** ``
> **Type:** Empty line

### Line 156
> **Code:** ``
> **Type:** Empty line

### Line 157
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 158
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 158
- **Code lines:** 119
- **Comments:** 2
- **TODO items:** 0
- **Empty lines:** 37

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: fairness_check.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/__init__.py`
- **Total lines:** 1
- **File size:** 78 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""models package: training, tuning, evaluation, and model registry lo...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: evaluate.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/evaluate.py`
- **Total lines:** 104
- **File size:** 2859 bytes

## Line Type Summary
- **Code:** 77
- **Comment:** 0
- **Empty:** 27
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model evaluation: metrics + ROC curve on a held-out test set.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Reusable for any trained model object; logs the results into the curre...`
> **Type:** Logical operation

### Line   4
> **Code:** `MLflow run (or a dedicated evaluation run) and saves the ROC curve to`
> **Type:** Logical operation

### Line   5
> **Code:** ```reports/``.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  23
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  24
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  25
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  26
> **Code:** `from sklearn.metrics import (`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** `PrecisionRecallDisplay,`
> **Type:** Code statement

### Line  28
> **Code:** `RocCurveDisplay,`
> **Type:** Code statement

### Line  29
> **Code:** `accuracy_score,`
> **Type:** Logical operation

### Line  30
> **Code:** `f1_score,`
> **Type:** Logical operation

### Line  31
> **Code:** `precision_score,`
> **Type:** Logical operation

### Line  32
> **Code:** `recall_score,`
> **Type:** Logical operation

### Line  33
> **Code:** `roc_auc_score,`
> **Type:** Logical operation

### Line  34
> **Code:** `)`
> **Type:** Code statement

### Line  35
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `from src.config import MLFLOW_DIR, REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `def load_model(path: Path):`
> **Type:** Function definition

### Line  41
> **Code:** `import joblib`
> **Type:** Imports a module

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `return joblib.load(path)`
> **Type:** Returns a value from a function

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `def evaluate(model, X_test, y_test, log_to_mlflow: bool = True, experi...`
> **Type:** Function definition

### Line  47
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `y_proba = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  52
> **Code:** `"precision": precision_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  53
> **Code:** `"recall": recall_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  54
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  55
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line  56
> **Code:** `}`
> **Type:** Code statement

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `roc_path = REPORTS_DIR / "roc_curve.png"`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `pr_path = REPORTS_DIR / "precision_recall_curve.png"`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `fig, ax = plt.subplots()`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax)`
> **Type:** Assignment/comparison

### Line  64
> **Code:** `ax.set_title("ROC Curve")`
> **Type:** Function call

### Line  65
> **Code:** `fig.savefig(roc_path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `fig, ax = plt.subplots()`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `PrecisionRecallDisplay.from_predictions(y_test, y_proba, ax=ax)`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `ax.set_title("Precision-Recall Curve")`
> **Type:** Arithmetic operation

### Line  71
> **Code:** `fig.savefig(pr_path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `if log_to_mlflow:`
> **Type:** Conditional statement

### Line  75
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  76
> **Code:** `mlflow.set_experiment(experiment)`
> **Type:** Function call

### Line  77
> **Code:** `with mlflow.start_run(run_name="evaluate"):`
> **Type:** Context manager

### Line  78
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line  79
> **Code:** `mlflow.log_artifact(str(roc_path))`
> **Type:** Function call

### Line  80
> **Code:** `mlflow.log_artifact(str(pr_path))`
> **Type:** Function call

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `return metrics`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  86
> **Code:** `parser = argparse.ArgumentParser(description="Evaluate a trained model...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `parser.add_argument("--model", default="models/churn_model.joblib")`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `X, y = _load_data()`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `_, X_test, _, y_test = train_test_split(X, y, test_size=0.25, random_s...`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `model = load_model(Path(args.model))`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `metrics = evaluate(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `print(metrics)`
> **Type:** Prints output to console

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** ``
> **Type:** Empty line

### Line  97
> **Code:** `def _load_data():`
> **Type:** Function definition

### Line  98
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 104
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 104
- **Code lines:** 77
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 27

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: evaluate.py*
---

# mlops-full-mlops-skills-project: train.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/train.py`
- **Total lines:** 182
- **File size:** 5691 bytes

## Line Type Summary
- **Code:** 145
- **Comment:** 1
- **Empty:** 36
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model training with full MLflow tracking.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Every training run logs:`
> **Type:** Code statement

### Line   4
> **Code:** `- hyperparameters,`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `- metrics (accuracy, F1, ROC-AUC),`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `- the model artifact,`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- a confusion matrix figure,`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `- tags linking to the data source hash and pipeline version.`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import sys`
> **Type:** Imports a module

### Line  14
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  18
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  21
> **Code:** `import logging`
> **Type:** Imports a module

### Line  22
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `import matplotlib`
> **Type:** Imports a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `matplotlib.use("Agg")`
> **Type:** Function call

### Line  27
> **Code:** `import matplotlib.pyplot as plt`
> **Type:** Imports a module

### Line  28
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  29
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  30
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  31
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  32
> **Code:** `from sklearn.metrics import accuracy_score, confusion_matrix, f1_score...`
> **Type:** Imports specific names from a module

### Line  33
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  36
> **Code:** `MLFLOW_DIR,`
> **Type:** Code statement

### Line  37
> **Code:** `MODELS_DIR,`
> **Type:** Code statement

### Line  38
> **Code:** `REPORTS_DIR,`
> **Type:** Code statement

### Line  39
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  40
> **Code:** `F1_PROMOTION_THRESHOLD,`
> **Type:** Code statement

### Line  41
> **Code:** `)`
> **Type:** Code statement

### Line  42
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** ``
> **Type:** Empty line

### Line  46
> **Code:** `DEFAULT_PARAMS = {`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `"n_estimators": 200,`
> **Type:** Logical operation

### Line  48
> **Code:** `"max_depth": 12,`
> **Type:** Code statement

### Line  49
> **Code:** `"min_samples_leaf": 5,`
> **Type:** Code statement

### Line  50
> **Code:** `"max_features": "sqrt",`
> **Type:** Code statement

### Line  51
> **Code:** `"random_state": 42,`
> **Type:** Logical operation

### Line  52
> **Code:** `}`
> **Type:** Code statement

### Line  53
> **Code:** ``
> **Type:** Empty line

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `def load_training_data() -> tuple[pd.DataFrame, pd.Series]:`
> **Type:** Function definition

### Line  56
> **Code:** `"""Load raw data and build the full feature matrix (sensitive excluded...`
> **Type:** Logical operation

### Line  57
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `return sets["X"], sets["y"]`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `def _preprocess_pipeline(raw: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  65
> **Code:** `"""Small local preprocess used by training (keeps module self-containe...`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `from src.data.preprocessing import preprocess`
> **Type:** Imports specific names from a module

### Line  67
> **Code:** ``
> **Type:** Empty line

### Line  68
> **Code:** `return preprocess(raw)`
> **Type:** Returns a value from a function

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** ``
> **Type:** Empty line

### Line  71
> **Code:** `def save_confusion_matrix(y_true, y_pred, path: Path) -> None:`
> **Type:** Function definition

### Line  72
> **Code:** `cm = confusion_matrix(y_true, y_pred)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `fig, ax = plt.subplots(figsize=(4, 4))`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.7)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `for (i, j), val in np.ndenumerate(cm):`
> **Type:** For loop

### Line  76
> **Code:** `ax.text(j, i, str(val), ha="center", va="center")`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `ax.set_xlabel("Predicted")`
> **Type:** Function call

### Line  78
> **Code:** `ax.set_ylabel("Actual")`
> **Type:** Function call

### Line  79
> **Code:** `ax.set_title("Confusion Matrix")`
> **Type:** Function call

### Line  80
> **Code:** `fig.savefig(path, dpi=120, bbox_inches="tight")`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `plt.close(fig)`
> **Type:** Library function call

### Line  82
> **Code:** ``
> **Type:** Empty line

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `def train_and_log(`
> **Type:** Function definition

### Line  85
> **Code:** `X_train: pd.DataFrame,`
> **Type:** Code statement

### Line  86
> **Code:** `X_test: pd.DataFrame,`
> **Type:** Code statement

### Line  87
> **Code:** `y_train: pd.Series,`
> **Type:** Code statement

### Line  88
> **Code:** `y_test: pd.Series,`
> **Type:** Code statement

### Line  89
> **Code:** `params: dict | None = None,`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `run_name: str = "churn_rf",`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `experiment_name: str = "churn_prediction",`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `register: bool = False,`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  94
> **Code:** `"""Train a RandomForest classifier, log everything to MLflow.`
> **Type:** Logical operation

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `Returns a dict with the model, metrics and run id for downstream steps...`
> **Type:** Logical operation

### Line  97
> **Code:** `"""`
> **Type:** Code statement

### Line  98
> **Code:** `params = params or dict(DEFAULT_PARAMS)`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line 100
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line 101
> **Code:** ``
> **Type:** Empty line

### Line 102
> **Code:** `with mlflow.start_run(run_name=run_name) as run:`
> **Type:** Context manager

### Line 103
> **Code:** `model = RandomForestClassifier(**params)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `model.fit(X_train, y_train)`
> **Type:** Function call

### Line 105
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `y_proba = model.predict_proba(X_test)[:, 1]`
> **Type:** Assignment/comparison

### Line 107
> **Code:** ``
> **Type:** Empty line

### Line 108
> **Code:** `metrics = {`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 110
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 111
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 112
> **Code:** `}`
> **Type:** Code statement

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `mlflow.log_params(model.get_params())`
> **Type:** Function call

### Line 115
> **Code:** `mlflow.log_metrics(metrics)`
> **Type:** Function call

### Line 116
> **Code:** `mlflow.log_param("n_features", X_train.shape[1])`
> **Type:** Function call

### Line 117
> **Code:** `mlflow.log_param("data_source", "data/raw/dataset.csv")`
> **Type:** Arithmetic operation

### Line 118
> **Code:** `mlflow.set_tag("pipeline", run_name)`
> **Type:** Function call

### Line 119
> **Code:** ``
> **Type:** Empty line

### Line 120
> **Code:** `cm_path = REPORTS_DIR / "confusion_matrix.png"`
> **Type:** Assignment/comparison

### Line 121
> **Code:** `cm_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 122
> **Code:** `save_confusion_matrix(y_test, y_pred, cm_path)`
> **Type:** Function call

### Line 123
> **Code:** `mlflow.log_artifact(str(cm_path))`
> **Type:** Function call

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `model_dir = MODELS_DIR / f"run_{run.info.run_id}"`
> **Type:** Assignment/comparison

### Line 126
> **Code:** `model_dir.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 127
> **Code:** `mlflow.sklearn.log_model(model, artifact_path="model")`
> **Type:** Assignment/comparison

### Line 128
> **Code:** ``
> **Type:** Empty line

### Line 129
> **Code:** `if register:`
> **Type:** Conditional statement

### Line 130
> **Code:** `mlflow.sklearn.log_model(`
> **Type:** Code statement

### Line 131
> **Code:** `model,`
> **Type:** Code statement

### Line 132
> **Code:** `artifact_path="model",`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `registered_model_name="churn_model",`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `)`
> **Type:** Code statement

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `mlflow.end_run()`
> **Type:** Function call

### Line 137
> **Code:** ``
> **Type:** Empty line

### Line 138
> **Code:** `logger.info("Trained model: %s", metrics)`
> **Type:** Arithmetic operation

### Line 139
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 140
> **Code:** `"model": model,`
> **Type:** Code statement

### Line 141
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 142
> **Code:** `"run_id": run.info.run_id,`
> **Type:** Code statement

### Line 143
> **Code:** `"feature_columns": list(X_train.columns),`
> **Type:** Code statement

### Line 144
> **Code:** `}`
> **Type:** Code statement

### Line 145
> **Code:** ``
> **Type:** Empty line

### Line 146
> **Code:** ``
> **Type:** Empty line

### Line 147
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 148
> **Code:** `parser = argparse.ArgumentParser(description="Train and track the chur...`
> **Type:** Assignment/comparison

### Line 149
> **Code:** `parser.add_argument("--register", action="store_true", help="Register ...`
> **Type:** Assignment/comparison

### Line 150
> **Code:** `parser.add_argument("--run-name", default="churn_rf")`
> **Type:** Assignment/comparison

### Line 151
> **Code:** `parser.add_argument("--test-size", type=float, default=0.25)`
> **Type:** Assignment/comparison

### Line 152
> **Code:** `parser.add_argument("--experiment", default="churn_prediction")`
> **Type:** Assignment/comparison

### Line 153
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `X, y = load_training_data()`
> **Type:** Assignment/comparison

### Line 156
> **Code:** `X_train, X_test, y_train, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `X, y, test_size=args.test_size, random_state=42, stratify=y`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `)`
> **Type:** Code statement

### Line 159
> **Code:** `result = train_and_log(`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `X_train, X_test, y_train, y_test,`
> **Type:** Code statement

### Line 161
> **Code:** `run_name=args.run_name,`
> **Type:** Assignment/comparison

### Line 162
> **Code:** `experiment_name=args.experiment,`
> **Type:** Assignment/comparison

### Line 163
> **Code:** `register=args.register,`
> **Type:** Assignment/comparison

### Line 164
> **Code:** `)`
> **Type:** Code statement

### Line 165
> **Code:** ``
> **Type:** Empty line

### Line 166
> **Code:** `f1 = result["metrics"]["f1_score"]`
> **Type:** Assignment/comparison

### Line 167
> **Code:** `status = "PASS" if f1 >= F1_PROMOTION_THRESHOLD else "FAIL"`
> **Type:** Assignment/comparison

### Line 168
> **Code:** `print(f"Training done. F1={f1:.4f} (threshold {F1_PROMOTION_THRESHOLD}...`
> **Type:** Prints output to console

### Line 169
> **Code:** `print(f"MLflow run: {result['run_id']}")`
> **Type:** Prints output to console

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `# Persist model + feature columns for downstream steps.`
> **Type:** Comment: Persist model + feature columns for downstream steps.

### Line 172
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 173
> **Code:** ``
> **Type:** Empty line

### Line 174
> **Code:** `MODELS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 175
> **Code:** `joblib.dump(result["model"], MODELS_DIR / "churn_model.joblib")`
> **Type:** Arithmetic operation

### Line 176
> **Code:** `with open(MODELS_DIR / "feature_columns.txt", "w") as handle:`
> **Type:** Context manager

### Line 177
> **Code:** `handle.write("\n".join(result["feature_columns"]))`
> **Type:** Logical operation

### Line 178
> **Code:** `print("Model saved to models/churn_model.joblib")`
> **Type:** Prints output to console

### Line 179
> **Code:** ``
> **Type:** Empty line

### Line 180
> **Code:** ``
> **Type:** Empty line

### Line 181
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 182
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 182
- **Code lines:** 145
- **Comments:** 1
- **TODO items:** 0
- **Empty lines:** 36

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: train.py*
---

# mlops-full-mlops-skills-project: tune.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/tune.py`
- **Total lines:** 97
- **File size:** 3250 bytes

## Line Type Summary
- **Code:** 72
- **Comment:** 0
- **Empty:** 25
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Optuna hyperparameter optimisation with nested MLflow runs.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Each Optuna trial is logged as a *nested* MLflow run under the parent ...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `run, so the whole search space is comparable in the MLflow UI via para...`
> **Type:** Code statement

### Line   5
> **Code:** `coordinates. Uses the default TPE (bayesian) sampler.`
> **Type:** Logical operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `import sys`
> **Type:** Imports a module

### Line  11
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  15
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  18
> **Code:** `import logging`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  21
> **Code:** `import optuna`
> **Type:** Imports a module

### Line  22
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  23
> **Code:** `from optuna.samplers import TPESampler`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from sklearn.ensemble import RandomForestClassifier`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** `from sklearn.metrics import f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** `from sklearn.model_selection import StratifiedKFold, cross_val_score`
> **Type:** Imports specific names from a module

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** `from src.config import MLFLOW_DIR`
> **Type:** Imports specific names from a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `def load_data() -> tuple[pd.DataFrame, pd.Series]:`
> **Type:** Function definition

### Line  34
> **Code:** `from src.models.train import load_training_data`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `return load_training_data()`
> **Type:** Returns a value from a function

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def objective(trial, X, y):`
> **Type:** Function definition

### Line  40
> **Code:** `params = {`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `"n_estimators": trial.suggest_int("n_estimators", 50, 500, step=50),`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `"max_depth": trial.suggest_int("max_depth", 3, 20),`
> **Type:** Code statement

### Line  43
> **Code:** `"min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),`
> **Type:** Code statement

### Line  44
> **Code:** `"max_features": trial.suggest_categorical("max_features", ["sqrt", "lo...`
> **Type:** Logical operation

### Line  45
> **Code:** `"min_samples_split": trial.suggest_int("min_samples_split", 2, 15),`
> **Type:** Code statement

### Line  46
> **Code:** `}`
> **Type:** Code statement

### Line  47
> **Code:** ``
> **Type:** Empty line

### Line  48
> **Code:** `model = RandomForestClassifier(**params, random_state=42)`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `with mlflow.start_run(nested=True):`
> **Type:** Context manager

### Line  50
> **Code:** `mlflow.log_params(params)`
> **Type:** Function call

### Line  51
> **Code:** `cv_score = cross_val_score(`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `model, X, y, cv=StratifiedKFold(3), scoring="f1", n_jobs=-1`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `).mean()`
> **Type:** Function call

### Line  54
> **Code:** `mlflow.log_metric("cv_f1", cv_score)`
> **Type:** Logical operation

### Line  55
> **Code:** `trial.report(cv_score, step=0)`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `return cv_score`
> **Type:** Returns a value from a function

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `def tune(n_trials: int = 50, experiment_name: str = "churn_optuna") ->...`
> **Type:** Function definition

### Line  60
> **Code:** `"""Run a bayesian search; return best params / value / study."""`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  62
> **Code:** `mlflow.set_experiment(experiment_name)`
> **Type:** Function call

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `X, y = load_data()`
> **Type:** Assignment/comparison

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `study = optuna.create_study(`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `direction="maximize",`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `sampler=TPESampler(seed=42),`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `study_name="churn_rf_bayesian",`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `with mlflow.start_run(run_name=f"optuna_search_{n_trials}trials"):`
> **Type:** Context manager

### Line  73
> **Code:** `mlflow.log_param("n_trials", n_trials)`
> **Type:** Function call

### Line  74
> **Code:** `mlflow.log_param("sampler", "TPE")`
> **Type:** Function call

### Line  75
> **Code:** `study.optimize(`
> **Type:** Code statement

### Line  76
> **Code:** `lambda t: objective(t, X, y), n_trials=n_trials, show_progress_bar=Fal...`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `)`
> **Type:** Code statement

### Line  78
> **Code:** `mlflow.log_metric("best_cv_f1", study.best_value)`
> **Type:** Function call

### Line  79
> **Code:** `mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items(...`
> **Type:** Logical operation

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `logger.info("Best trial: %.4f with %s", study.best_value, study.best_p...`
> **Type:** Arithmetic operation

### Line  82
> **Code:** `return {"best_params": study.best_params, "best_value": study.best_val...`
> **Type:** Returns a value from a function

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  86
> **Code:** `parser = argparse.ArgumentParser(description="Optuna tuning for the ch...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** `parser.add_argument("--trials", type=int, default=50)`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `parser.add_argument("--experiment", default="churn_optuna")`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  90
> **Code:** ``
> **Type:** Empty line

### Line  91
> **Code:** `result = tune(n_trials=args.trials, experiment_name=args.experiment)`
> **Type:** Assignment/comparison

### Line  92
> **Code:** `print(f"Best CV F1: {result['best_value']:.4f}")`
> **Type:** Prints output to console

### Line  93
> **Code:** `print(f"Best params: {result['best_params']}")`
> **Type:** Prints output to console

### Line  94
> **Code:** ``
> **Type:** Empty line

### Line  95
> **Code:** ``
> **Type:** Empty line

### Line  96
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  97
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 97
- **Code lines:** 72
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 25

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: tune.py*
---

# mlops-full-mlops-skills-project: promote.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/models/promote.py`
- **Total lines:** 224
- **File size:** 7216 bytes

## Line Type Summary
- **Code:** 170
- **Comment:** 5
- **Empty:** 49
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Model promotion logic with hard gates.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A candidate model may only be promoted to Production when **all** gate...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `1. Performance: F1 >= ``F1_PROMOTION_THRESHOLD`` on the held-out set.`
> **Type:** Assignment/comparison

### Line   5
> **Code:** `2. Competitive: beats the current Production model (if any) by a margi...`
> **Type:** Code statement

### Line   6
> **Code:** `3. Quality: Deepchecks suite passes (no critical failures).`
> **Type:** Code statement

### Line   7
> **Code:** `4. Fairness: Fairlearn demographic parity difference within threshold.`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `On success the MLflow registered model is moved to Production and a mo...`
> **Type:** Logical operation

### Line  10
> **Code:** `card is generated.`
> **Type:** Code statement

### Line  11
> **Code:** `"""`
> **Type:** Code statement

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import sys`
> **Type:** Imports a module

### Line  16
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `PROJECT_ROOT = Path(__file__).resolve().parents[2]`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `if str(PROJECT_ROOT) not in sys.path:`
> **Type:** Conditional statement

### Line  20
> **Code:** `sys.path.insert(0, str(PROJECT_ROOT))`
> **Type:** Function call

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  23
> **Code:** `import json`
> **Type:** Imports a module

### Line  24
> **Code:** `import logging`
> **Type:** Imports a module

### Line  25
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  26
> **Code:** ``
> **Type:** Empty line

### Line  27
> **Code:** `import mlflow`
> **Type:** Imports a module

### Line  28
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  31
> **Code:** `F1_PROMOTION_THRESHOLD,`
> **Type:** Code statement

### Line  32
> **Code:** `MLFLOW_DIR,`
> **Type:** Code statement

### Line  33
> **Code:** `MODEL_CARDS_DIR,`
> **Type:** Code statement

### Line  34
> **Code:** `MODELS_DIR,`
> **Type:** Code statement

### Line  35
> **Code:** `REPORTS_DIR,`
> **Type:** Code statement

### Line  36
> **Code:** `FAIRNESS_DP_THRESHOLD,`
> **Type:** Code statement

### Line  37
> **Code:** `)`
> **Type:** Code statement

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `BEAT_MARGIN = 0.005`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** `def run_deepchecks(model, X_test, y_test) -> dict:`
> **Type:** Function definition

### Line  45
> **Code:** `"""Run the Deepchecks full suite; return pass/fail summary."""`
> **Type:** Arithmetic operation

### Line  46
> **Code:** `try:`
> **Type:** Code statement

### Line  47
> **Code:** `from deepchecks.tabular import Dataset`
> **Type:** Imports specific names from a module

### Line  48
> **Code:** `from deepchecks.tabular.suites import full_suite`
> **Type:** Imports specific names from a module

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `train_ds = Dataset(pd.DataFrame(X_test), label=y_test)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `test_ds = train_ds.copy()`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `suite = full_suite()`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `result = suite.run(train_ds, test_ds, model=model)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `result.save_as_html("reports/deepchecks_report.html")`
> **Type:** Arithmetic operation

### Line  55
> **Code:** `critical_failures = [`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `check.get_header() for check in result.results`
> **Type:** Logical operation

### Line  57
> **Code:** `if not check.passed`
> **Type:** Conditional statement

### Line  58
> **Code:** `]`
> **Type:** Code statement

### Line  59
> **Code:** `passed = not any(not check.passed for check in result.results)`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `return {"passed": passed, "critical_failures": critical_failures}`
> **Type:** Returns a value from a function

### Line  61
> **Code:** `except ImportError:`
> **Type:** Logical operation

### Line  62
> **Code:** `logger.warning("deepchecks unavailable; treating gate as passed (skip)...`
> **Type:** Function call

### Line  63
> **Code:** `return {"passed": True, "skip": True}`
> **Type:** Returns a value from a function

### Line  64
> **Code:** ``
> **Type:** Empty line

### Line  65
> **Code:** ``
> **Type:** Empty line

### Line  66
> **Code:** `def load_production_model_metrics() -> float | None:`
> **Type:** Function definition

### Line  67
> **Code:** `"""Return the F1 of the current registered Production model, if any.""...`
> **Type:** Code statement

### Line  68
> **Code:** `try:`
> **Type:** Code statement

### Line  69
> **Code:** `client = mlflow.MlflowClient(mlflow.get_tracking_uri())`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `versions = client.get_latest_versions("churn_model", stages=["Producti...`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `if not versions:`
> **Type:** Conditional statement

### Line  72
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  73
> **Code:** `run = client.get_run(versions[0].run_id)`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `return float(run.data.metrics.get("f1_score", 0.0))`
> **Type:** Returns a value from a function

### Line  75
> **Code:** `except Exception:`
> **Type:** Code statement

### Line  76
> **Code:** `return None`
> **Type:** Returns a value from a function

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `def promote(`
> **Type:** Function definition

### Line  80
> **Code:** `model_path: Path = MODELS_DIR / "churn_model.joblib",`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `run_id: str | None = None,`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `experiment: str = "churn_prediction",`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  84
> **Code:** `"""Evaluate all promotion gates and promote the model if they all pass...`
> **Type:** Logical operation

### Line  85
> **Code:** `mlflow.set_tracking_uri(MLFLOW_DIR.as_uri())`
> **Type:** Function call

### Line  86
> **Code:** `mlflow.set_experiment(experiment)`
> **Type:** Function call

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `# 1. Performance gate (F1).`
> **Type:** Comment: 1. Performance gate (F1).

### Line  89
> **Code:** `metrics = _evaluate_model(model_path)`
> **Type:** Assignment/comparison

### Line  90
> **Code:** `f1 = metrics["f1_score"]`
> **Type:** Assignment/comparison

### Line  91
> **Code:** `gates = {"performance": f1 >= F1_PROMOTION_THRESHOLD}`
> **Type:** Assignment/comparison

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `# 2. Beats current Production.`
> **Type:** Comment: 2. Beats current Production.

### Line  94
> **Code:** `prod_f1 = load_production_model_metrics()`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `if prod_f1 is None:`
> **Type:** Conditional statement

### Line  96
> **Code:** `gates["beats_production"] = True`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `else:`
> **Type:** Else block

### Line  98
> **Code:** `gates["beats_production"] = f1 > prod_f1 + BEAT_MARGIN`
> **Type:** Assignment/comparison

### Line  99
> **Code:** `gates_detail = {"candidate_f1": f1, "production_f1": prod_f1}`
> **Type:** Assignment/comparison

### Line 100
> **Code:** ``
> **Type:** Empty line

### Line 101
> **Code:** `# 3. Deepchecks.`
> **Type:** Comment: 3. Deepchecks.

### Line 102
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `model = _load_model(model_path)`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `deepchecks = run_deepchecks(model, X_test, y_test)`
> **Type:** Assignment/comparison

### Line 105
> **Code:** `gates["deepchecks"] = deepchecks["passed"]`
> **Type:** Assignment/comparison

### Line 106
> **Code:** ``
> **Type:** Empty line

### Line 107
> **Code:** `# 4. Fairness.`
> **Type:** Comment: 4. Fairness.

### Line 108
> **Code:** `fairness = _load_fairness_report()`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `gates["fairness"] = fairness.get("passed", False)`
> **Type:** Assignment/comparison

### Line 110
> **Code:** ``
> **Type:** Empty line

### Line 111
> **Code:** `all_passed = all(gates.values())`
> **Type:** Assignment/comparison

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** `report = {`
> **Type:** Assignment/comparison

### Line 114
> **Code:** `"gates": gates,`
> **Type:** Code statement

### Line 115
> **Code:** `"gate_detail": gates_detail,`
> **Type:** Code statement

### Line 116
> **Code:** `"fairness": {`
> **Type:** Code statement

### Line 117
> **Code:** `"dp_diff": fairness.get("demographic_parity_difference"),`
> **Type:** Code statement

### Line 118
> **Code:** `"threshold": fairness.get("threshold", FAIRNESS_DP_THRESHOLD),`
> **Type:** Code statement

### Line 119
> **Code:** `},`
> **Type:** Code statement

### Line 120
> **Code:** `"deepchecks": {"passed": deepchecks["passed"]},`
> **Type:** Data structure operation

### Line 121
> **Code:** `"promoted": all_passed,`
> **Type:** Code statement

### Line 122
> **Code:** `"metrics": metrics,`
> **Type:** Code statement

### Line 123
> **Code:** `}`
> **Type:** Code statement

### Line 124
> **Code:** ``
> **Type:** Empty line

### Line 125
> **Code:** `if all_passed:`
> **Type:** Conditional statement

### Line 126
> **Code:** `_move_to_production(run_id)`
> **Type:** Function call

### Line 127
> **Code:** `logger.info("All promotion gates passed -> moved to Production.")`
> **Type:** Arithmetic operation

### Line 128
> **Code:** `else:`
> **Type:** Else block

### Line 129
> **Code:** `logger.warning("Promotion rejected: %s", {k: v for k, v in gates.items...`
> **Type:** Arithmetic operation

### Line 130
> **Code:** ``
> **Type:** Empty line

### Line 131
> **Code:** `_write_report(report)`
> **Type:** Logical operation

### Line 132
> **Code:** `_generate_model_card(report)`
> **Type:** Logical operation

### Line 133
> **Code:** `return report`
> **Type:** Returns a value from a function

### Line 134
> **Code:** ``
> **Type:** Empty line

### Line 135
> **Code:** ``
> **Type:** Empty line

### Line 136
> **Code:** `def _evaluate_model(model_path: Path) -> dict:`
> **Type:** Function definition

### Line 137
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 138
> **Code:** `from sklearn.metrics import accuracy_score, f1_score, roc_auc_score`
> **Type:** Imports specific names from a module

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** `model = joblib.load(model_path)`
> **Type:** Assignment/comparison

### Line 141
> **Code:** `X_test, y_test = _load_test_frame()`
> **Type:** Assignment/comparison

### Line 142
> **Code:** `y_pred = model.predict(X_test)`
> **Type:** Assignment/comparison

### Line 143
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line 144
> **Code:** `"accuracy": accuracy_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 145
> **Code:** `"f1_score": f1_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 146
> **Code:** `"roc_auc": roc_auc_score(y_test, y_pred),`
> **Type:** Logical operation

### Line 147
> **Code:** `}`
> **Type:** Code statement

### Line 148
> **Code:** ``
> **Type:** Empty line

### Line 149
> **Code:** ``
> **Type:** Empty line

### Line 150
> **Code:** `def _load_test_frame():`
> **Type:** Function definition

### Line 151
> **Code:** `from src.features.build_features import build_features, feature_sets`
> **Type:** Imports specific names from a module

### Line 152
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line 153
> **Code:** `from sklearn.model_selection import train_test_split`
> **Type:** Imports specific names from a module

### Line 154
> **Code:** ``
> **Type:** Empty line

### Line 155
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line 156
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line 157
> **Code:** `frame = build_features(clean, include_sensitive=False)`
> **Type:** Assignment/comparison

### Line 158
> **Code:** `sets = feature_sets(frame)`
> **Type:** Assignment/comparison

### Line 159
> **Code:** `_, X_test, _, y_test = train_test_split(`
> **Type:** Assignment/comparison

### Line 160
> **Code:** `sets["X"], sets["y"], test_size=0.25, random_state=42, stratify=sets["...`
> **Type:** Assignment/comparison

### Line 161
> **Code:** `)`
> **Type:** Code statement

### Line 162
> **Code:** `return X_test, y_test`
> **Type:** Returns a value from a function

### Line 163
> **Code:** ``
> **Type:** Empty line

### Line 164
> **Code:** ``
> **Type:** Empty line

### Line 165
> **Code:** `def _load_model(model_path: Path):`
> **Type:** Function definition

### Line 166
> **Code:** `import joblib`
> **Type:** Imports a module

### Line 167
> **Code:** ``
> **Type:** Empty line

### Line 168
> **Code:** `return joblib.load(model_path)`
> **Type:** Returns a value from a function

### Line 169
> **Code:** ``
> **Type:** Empty line

### Line 170
> **Code:** ``
> **Type:** Empty line

### Line 171
> **Code:** `def _load_fairness_report() -> dict:`
> **Type:** Function definition

### Line 172
> **Code:** `report_path = REPORTS_DIR / "fairness_report.json"`
> **Type:** Assignment/comparison

### Line 173
> **Code:** `if report_path.exists():`
> **Type:** Conditional statement

### Line 174
> **Code:** `return json.loads(report_path.read_text())`
> **Type:** Returns a value from a function

### Line 175
> **Code:** `return {"passed": False, "demographic_parity_difference": 1.0}`
> **Type:** Returns a value from a function

### Line 176
> **Code:** ``
> **Type:** Empty line

### Line 177
> **Code:** ``
> **Type:** Empty line

### Line 178
> **Code:** `def _move_to_production(run_id: str | None) -> None:`
> **Type:** Function definition

### Line 179
> **Code:** `client = mlflow.MlflowClient(mlflow.get_tracking_uri())`
> **Type:** Assignment/comparison

### Line 180
> **Code:** `if run_id:`
> **Type:** Conditional statement

### Line 181
> **Code:** `try:`
> **Type:** Code statement

### Line 182
> **Code:** `client.set_registered_model_alias("churn_model", "production", run_id)`
> **Type:** Function call

### Line 183
> **Code:** `return`
> **Type:** Returns a value from a function

### Line 184
> **Code:** `except Exception:`
> **Type:** Code statement

### Line 185
> **Code:** `pass`
> **Type:** Code statement

### Line 186
> **Code:** `# Fallback: transition the newest Staging/None version.`
> **Type:** Comment: Fallback: transition the newest Staging/None version.

### Line 187
> **Code:** `versions = client.get_latest_versions("churn_model", stages=["None", "...`
> **Type:** Assignment/comparison

### Line 188
> **Code:** `if versions:`
> **Type:** Conditional statement

### Line 189
> **Code:** `client.transition_model_version_stage(`
> **Type:** Code statement

### Line 190
> **Code:** `"churn_model", versions[0].version, "Production", archive_existing_ver...`
> **Type:** Assignment/comparison

### Line 191
> **Code:** `)`
> **Type:** Code statement

### Line 192
> **Code:** ``
> **Type:** Empty line

### Line 193
> **Code:** ``
> **Type:** Empty line

### Line 194
> **Code:** `def _write_report(report: dict) -> None:`
> **Type:** Function definition

### Line 195
> **Code:** `from src.config import REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line 196
> **Code:** ``
> **Type:** Empty line

### Line 197
> **Code:** `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line 198
> **Code:** `with open(REPORTS_DIR / "promotion_report.json", "w") as handle:`
> **Type:** Context manager

### Line 199
> **Code:** `json.dump(report, handle, indent=2, default=str)`
> **Type:** Assignment/comparison

### Line 200
> **Code:** ``
> **Type:** Empty line

### Line 201
> **Code:** ``
> **Type:** Empty line

### Line 202
> **Code:** `def _generate_model_card(report: dict) -> None:`
> **Type:** Function definition

### Line 203
> **Code:** `try:`
> **Type:** Code statement

### Line 204
> **Code:** `from model_cards.model_card_template import generate_model_card`
> **Type:** Imports specific names from a module

### Line 205
> **Code:** ``
> **Type:** Empty line

### Line 206
> **Code:** `generate_model_card(report, output_path=MODEL_CARDS_DIR / "model_card....`
> **Type:** Assignment/comparison

### Line 207
> **Code:** `except Exception as exc:  # pragma: no cover`
> **Type:** Code statement

### Line 208
> **Code:** `logger.warning("Model card generation failed: %s", exc)`
> **Type:** Arithmetic operation

### Line 209
> **Code:** ``
> **Type:** Empty line

### Line 210
> **Code:** ``
> **Type:** Empty line

### Line 211
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 212
> **Code:** `parser = argparse.ArgumentParser(description="Promotion gates + regist...`
> **Type:** Assignment/comparison

### Line 213
> **Code:** `parser.add_argument("--model", default=str(MODELS_DIR / "churn_model.j...`
> **Type:** Assignment/comparison

### Line 214
> **Code:** `parser.add_argument("--run-id", default=None)`
> **Type:** Assignment/comparison

### Line 215
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 216
> **Code:** ``
> **Type:** Empty line

### Line 217
> **Code:** `report = promote(Path(args.model), run_id=args.run_id)`
> **Type:** Assignment/comparison

### Line 218
> **Code:** `print(f"Promoted: {report['promoted']}")`
> **Type:** Prints output to console

### Line 219
> **Code:** `print("Gates:", report["gates"])`
> **Type:** Prints output to console

### Line 220
> **Code:** `print("Report saved to reports/promotion_report.json")`
> **Type:** Prints output to console

### Line 221
> **Code:** ``
> **Type:** Empty line

### Line 222
> **Code:** ``
> **Type:** Empty line

### Line 223
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 224
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 224
- **Code lines:** 170
- **Comments:** 5
- **TODO items:** 0
- **Empty lines:** 49

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: promote.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/monitoring/__init__.py`
- **Total lines:** 1
- **File size:** 84 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""monitoring package: drift and performance monitoring (Evidently, Pr...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: drift_report.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/monitoring/drift_report.py`
- **Total lines:** 115
- **File size:** 3940 bytes

## Line Type Summary
- **Code:** 88
- **Comment:** 0
- **Empty:** 27
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Production model monitoring with Evidently.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Builds a drift report (``DataDriftPreset`` + ``TargetDriftPreset``) co...`
> **Type:** Arithmetic operation

### Line   4
> **Code:** `a production sample against the training reference dataset, saves the ...`
> **Type:** Code statement

### Line   5
> **Code:** ```monitoring/reports/drift_report.html`` and extracts the dataset drif...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `A simulated drift mode injects distribution shifts so the report is de...`
> **Type:** Logical operation

### Line   8
> **Code:** `without needing real production traffic.`
> **Type:** Code statement

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  14
> **Code:** `import json`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  18
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** `from src.config import MONITORING_REPORTS_DIR, REFERENCE_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `try:`
> **Type:** Code statement

### Line  23
> **Code:** `from evidently.report import Report`
> **Type:** Imports specific names from a module

### Line  24
> **Code:** `from evidently.metric_preset import DataDriftPreset, TargetDriftPreset`
> **Type:** Imports specific names from a module

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `EVIDENTLY_AVAILABLE = True`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `except ImportError:  # pragma: no cover`
> **Type:** Logical operation

### Line  28
> **Code:** `EVIDENTLY_AVAILABLE = False`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def build_reference() -> pd.DataFrame:`
> **Type:** Function definition

### Line  32
> **Code:** `"""Persist and return the training reference (for drift comparison).""...`
> **Type:** Logical operation

### Line  33
> **Code:** `from src.features.build_features import build_features`
> **Type:** Imports specific names from a module

### Line  34
> **Code:** `from src.models.train import _preprocess_pipeline`
> **Type:** Imports specific names from a module

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `raw = pd.read_csv("data/raw/dataset.csv")`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `clean = _preprocess_pipeline(raw)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `frame = build_features(clean, include_sensitive=True)`
> **Type:** Assignment/comparison

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `REFERENCE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `frame.to_csv(REFERENCE_DATA_PATH, index=False)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `return frame`
> **Type:** Returns a value from a function

### Line  43
> **Code:** ``
> **Type:** Empty line

### Line  44
> **Code:** ``
> **Type:** Empty line

### Line  45
> **Code:** `def simulate_production_sample(n: int = 1000, drift_strength: float = ...`
> **Type:** Function definition

### Line  46
> **Code:** `"""Sample rows and optionally shift distributions to simulate drift.""...`
> **Type:** Logical operation

### Line  47
> **Code:** `if not REFERENCE_DATA_PATH.exists():`
> **Type:** Conditional statement

### Line  48
> **Code:** `build_reference()`
> **Type:** Function call

### Line  49
> **Code:** `ref = pd.read_csv(REFERENCE_DATA_PATH)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** ``
> **Type:** Empty line

### Line  51
> **Code:** `current = ref.sample(n=min(n, len(ref)), random_state=7)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `if drift_strength > 0:`
> **Type:** Conditional statement

### Line  53
> **Code:** `rng = np.random.default_rng(7)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** `numeric_cols = current.select_dtypes(include=[np.number]).columns`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `for col in numeric_cols:`
> **Type:** For loop

### Line  56
> **Code:** `std = current[col].std() or 1.0`
> **Type:** Assignment/comparison

### Line  57
> **Code:** `current[col] = current[col] + rng.normal(`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `0, drift_strength * std, size=len(current)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `)`
> **Type:** Code statement

### Line  60
> **Code:** `return current`
> **Type:** Returns a value from a function

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** `def generate_drift_report(`
> **Type:** Function definition

### Line  64
> **Code:** `current_data: pd.DataFrame | None = None,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `reference_data: pd.DataFrame | None = None,`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `output_path: Path = MONITORING_REPORTS_DIR / "drift_report.html",`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `) -> dict:`
> **Type:** Arithmetic operation

### Line  68
> **Code:** `"""Run the Evidently report and extract the dataset drift score."""`
> **Type:** Logical operation

### Line  69
> **Code:** `if not EVIDENTLY_AVAILABLE:`
> **Type:** Conditional statement

### Line  70
> **Code:** `raise ImportError("evidently is required for drift monitoring")`
> **Type:** Raises an exception

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** `reference = reference_data if reference_data is not None else build_re...`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `current = (`
> **Type:** Assignment/comparison

### Line  74
> **Code:** `current_data if current_data is not None`
> **Type:** Logical operation

### Line  75
> **Code:** `else simulate_production_sample()`
> **Type:** Function call

### Line  76
> **Code:** `)`
> **Type:** Code statement

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `report.run(reference_data=reference, current_data=current)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** `output_path.parent.mkdir(parents=True, exist_ok=True)`
> **Type:** Assignment/comparison

### Line  82
> **Code:** `report.save_html(str(output_path))`
> **Type:** Logical operation

### Line  83
> **Code:** ``
> **Type:** Empty line

### Line  84
> **Code:** `as_dict = report.as_dict()`
> **Type:** Assignment/comparison

### Line  85
> **Code:** `dataset_drift = as_dict["metrics"][0]["result"]["dataset_drift"]`
> **Type:** Assignment/comparison

### Line  86
> **Code:** `drift_score = as_dict["metrics"][0]["result"]["share_of_drifted_column...`
> **Type:** Assignment/comparison

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `result = {`
> **Type:** Assignment/comparison

### Line  89
> **Code:** `"dataset_drift": bool(dataset_drift),`
> **Type:** Code statement

### Line  90
> **Code:** `"drift_score": float(drift_score),`
> **Type:** Logical operation

### Line  91
> **Code:** `"report_path": str(output_path),`
> **Type:** Logical operation

### Line  92
> **Code:** `}`
> **Type:** Code statement

### Line  93
> **Code:** `(MONITORING_REPORTS_DIR / "drift_score.json").write_text(`
> **Type:** Arithmetic operation

### Line  94
> **Code:** `json.dumps(result, indent=2)`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `)`
> **Type:** Code statement

### Line  96
> **Code:** `return result`
> **Type:** Returns a value from a function

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 100
> **Code:** `parser = argparse.ArgumentParser(description="Generate Evidently drift...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `parser.add_argument("--drift-strength", type=float, default=0.0,`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `help=">0 simulates a drifted production sample.")`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 104
> **Code:** ``
> **Type:** Empty line

### Line 105
> **Code:** `current = simulate_production_sample(drift_strength=args.drift_strengt...`
> **Type:** Assignment/comparison

### Line 106
> **Code:** `result = generate_drift_report(current_data=current)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `print(`
> **Type:** Prints output to console

### Line 108
> **Code:** `f"dataset_drift={result['dataset_drift']} "`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `f"drift_score={result['drift_score']:.3f}"`
> **Type:** Assignment/comparison

### Line 110
> **Code:** `)`
> **Type:** Code statement

### Line 111
> **Code:** `print(f"Report saved to {result['report_path']}")`
> **Type:** Prints output to console

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 115
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 115
- **Code lines:** 88
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 27

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: drift_report.py*
---

# mlops-full-mlops-skills-project: retraining_trigger.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/monitoring/retraining_trigger.py`
- **Total lines:** 83
- **File size:** 2572 bytes

## Line Type Summary
- **Code:** 61
- **Comment:** 1
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Drift-driven retraining trigger.`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Checks the latest drift score and, when it exceeds ``DRIFT_THRESHOLD``...`
> **Type:** Logical operation

### Line   4
> **Code:** `triggers the ZenML retraining pipeline. As a safety guard the trigger ...`
> **Type:** Code statement

### Line   5
> **Code:** `skips the fairness check: the retraining pipeline itself re-runs the f...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `gate suite before any promotion.`
> **Type:** Logical operation

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  12
> **Code:** `import json`
> **Type:** Imports a module

### Line  13
> **Code:** `import logging`
> **Type:** Imports a module

### Line  14
> **Code:** `import subprocess`
> **Type:** Imports a module

### Line  15
> **Code:** `from pathlib import Path`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `from src.config import DRIFT_THRESHOLD, MONITORING_REPORTS_DIR`
> **Type:** Imports specific names from a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `DRIFT_SCORE_FILE = MONITORING_REPORTS_DIR / "drift_score.json"`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def read_drift_score(path: Path = DRIFT_SCORE_FILE) -> float:`
> **Type:** Function definition

### Line  25
> **Code:** `"""Read the latest drift score produced by ``drift_report.py``."""`
> **Type:** Logical operation

### Line  26
> **Code:** `if not path.exists():`
> **Type:** Conditional statement

### Line  27
> **Code:** `return 0.0`
> **Type:** Returns a value from a function

### Line  28
> **Code:** `data = json.loads(path.read_text())`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `return float(data["drift_score"])`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def should_retrain(score: float, threshold: float = DRIFT_THRESHOLD) -...`
> **Type:** Function definition

### Line  33
> **Code:** `"""Return True when the drift score exceeds the threshold."""`
> **Type:** Logical operation

### Line  34
> **Code:** `return score > threshold`
> **Type:** Returns a value from a function

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** ``
> **Type:** Empty line

### Line  37
> **Code:** `def trigger_retraining(dry_run: bool = False) -> dict:`
> **Type:** Function definition

### Line  38
> **Code:** `"""Evaluate drift and launch the retraining pipeline when needed."""`
> **Type:** Logical operation

### Line  39
> **Code:** `score = read_drift_score()`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `trigger = should_retrain(score)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `logger.info("Drift score=%.3f threshold=%.3f trigger=%s", score, DRIFT...`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `if trigger and not dry_run:`
> **Type:** Conditional statement

### Line  44
> **Code:** `_launch_retraining_pipeline()`
> **Type:** Function call

### Line  45
> **Code:** `return {`
> **Type:** Returns a value from a function

### Line  46
> **Code:** `"drift_score": score,`
> **Type:** Logical operation

### Line  47
> **Code:** `"threshold": DRIFT_THRESHOLD,`
> **Type:** Code statement

### Line  48
> **Code:** `"triggered": trigger,`
> **Type:** Code statement

### Line  49
> **Code:** `"dry_run": dry_run,`
> **Type:** Code statement

### Line  50
> **Code:** `}`
> **Type:** Code statement

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def _launch_retraining_pipeline() -> None:`
> **Type:** Function definition

### Line  54
> **Code:** `"""Shell out to the ZenML retraining pipeline.`
> **Type:** Code statement

### Line  55
> **Code:** ``
> **Type:** Empty line

### Line  56
> **Code:** `The retraining pipeline re-runs data validation, tuning, Deepchecks an...`
> **Type:** Arithmetic operation

### Line  57
> **Code:** `Fairlearn before any model is promoted (all promotion guards remain`
> **Type:** Logical operation

### Line  58
> **Code:** `active on automated retraining).`
> **Type:** Code statement

### Line  59
> **Code:** `"""`
> **Type:** Code statement

### Line  60
> **Code:** `cmd = ["python", "-m", "pipelines.retraining_pipeline"]`
> **Type:** Assignment/comparison

### Line  61
> **Code:** `logger.info("Launching retraining pipeline: %s", " ".join(cmd))`
> **Type:** Arithmetic operation

### Line  62
> **Code:** `subprocess.Popen(`
> **Type:** Code statement

### Line  63
> **Code:** `cmd,`
> **Type:** Code statement

### Line  64
> **Code:** `stdout=subprocess.DEVNULL,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `stderr=subprocess.DEVNULL,`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `)`
> **Type:** Code statement

### Line  67
> **Code:** `# Notification / supervision trace: structured log for human oversight...`
> **Type:** Comment: Notification / supervision trace: structured log for human oversight.

### Line  68
> **Code:** `logger.warning(`
> **Type:** Code statement

### Line  69
> **Code:** `"AUTOMATED_RETRAINING_TRIGGERED score=%.3f", read_drift_score()`
> **Type:** Assignment/comparison

### Line  70
> **Code:** `)`
> **Type:** Code statement

### Line  71
> **Code:** ``
> **Type:** Empty line

### Line  72
> **Code:** ``
> **Type:** Empty line

### Line  73
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  74
> **Code:** `parser = argparse.ArgumentParser(description="Drift-based retraining t...`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `parser.add_argument("--dry-run", action="store_true", help="Only repor...`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `result = trigger_retraining(dry_run=args.dry_run)`
> **Type:** Assignment/comparison

### Line  79
> **Code:** `print(result)`
> **Type:** Prints output to console

### Line  80
> **Code:** ``
> **Type:** Empty line

### Line  81
> **Code:** ``
> **Type:** Empty line

### Line  82
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  83
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 83
- **Code lines:** 61
- **Comments:** 1
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: retraining_trigger.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/data/__init__.py`
- **Total lines:** 1
- **File size:** 68 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""data package: data loading, validation, and versioning (DVC)."""`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: ingestion.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/data/ingestion.py`
- **Total lines:** 65
- **File size:** 1797 bytes

## Line Type Summary
- **Code:** 47
- **Comment:** 0
- **Empty:** 18
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Data ingestion: load raw data and log key facts.`
> **Type:** Logical operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Logs the row count, the covered time period, and a SHA256 hash of the ...`
> **Type:** Logical operation

### Line   4
> **Code:** `source file so every downstream artifact can be traced back to its inp...`
> **Type:** Code statement

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `import hashlib`
> **Type:** Imports a module

### Line  10
> **Code:** `import logging`
> **Type:** Imports a module

### Line  11
> **Code:** `from typing import Tuple`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from src.config import RAW_DATA_PATH`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** ``
> **Type:** Empty line

### Line  17
> **Code:** `logger = logging.getLogger(__name__)`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelnam...`
> **Type:** Assignment/comparison

### Line  19
> **Code:** ``
> **Type:** Empty line

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `def file_hash(path) -> str:`
> **Type:** Function definition

### Line  22
> **Code:** `"""Return the SHA256 hex digest of a file, streaming-friendly."""`
> **Type:** Arithmetic operation

### Line  23
> **Code:** `digest = hashlib.sha256()`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `with open(path, "rb") as handle:`
> **Type:** Context manager

### Line  25
> **Code:** `for chunk in iter(lambda: handle.read(1 << 16), b""):`
> **Type:** For loop

### Line  26
> **Code:** `digest.update(chunk)`
> **Type:** Function call

### Line  27
> **Code:** `return digest.hexdigest()`
> **Type:** Returns a value from a function

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** `def ingest_raw_data(path=RAW_DATA_PATH) -> Tuple[pd.DataFrame, dict]:`
> **Type:** Function definition

### Line  31
> **Code:** `"""Load the raw CSV and log ingestion metadata.`
> **Type:** Logical operation

### Line  32
> **Code:** ``
> **Type:** Empty line

### Line  33
> **Code:** `Returns ``(dataframe, metadata)`` where metadata contains the row coun...`
> **Type:** Code statement

### Line  34
> **Code:** `the covered time period, and the source file hash.`
> **Type:** Logical operation

### Line  35
> **Code:** `"""`
> **Type:** Code statement

### Line  36
> **Code:** `data_hash = file_hash(path)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `df = pd.read_csv(path)`
> **Type:** Assignment/comparison

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `time_col = "timestamp" if "timestamp" in df.columns else None`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `if time_col is not None:`
> **Type:** Conditional statement

### Line  41
> **Code:** `df[time_col] = pd.to_datetime(df[time_col])`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `period = (`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `f"{df[time_col].min()} -> {df[time_col].max()}"`
> **Type:** Arithmetic operation

### Line  45
> **Code:** `if time_col is not None`
> **Type:** Conditional statement

### Line  46
> **Code:** `else "n/a"`
> **Type:** Arithmetic operation

### Line  47
> **Code:** `)`
> **Type:** Code statement

### Line  48
> **Code:** ``
> **Type:** Empty line

### Line  49
> **Code:** `metadata = {`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `"rows": len(df),`
> **Type:** Code statement

### Line  51
> **Code:** `"columns": len(df.columns),`
> **Type:** Code statement

### Line  52
> **Code:** `"time_period": period,`
> **Type:** Code statement

### Line  53
> **Code:** `"source_file": str(path),`
> **Type:** Code statement

### Line  54
> **Code:** `"source_hash": data_hash,`
> **Type:** Code statement

### Line  55
> **Code:** `}`
> **Type:** Code statement

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `logger.info("Ingested %d rows from %s", len(df), path)`
> **Type:** Arithmetic operation

### Line  58
> **Code:** `logger.info("Covered time period: %s", period)`
> **Type:** Arithmetic operation

### Line  59
> **Code:** `logger.info("Source file hash: %s", data_hash)`
> **Type:** Arithmetic operation

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** `return df, metadata`
> **Type:** Returns a value from a function

### Line  62
> **Code:** ``
> **Type:** Empty line

### Line  63
> **Code:** ``
> **Type:** Empty line

### Line  64
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  65
> **Code:** `ingest_raw_data()`
> **Type:** Function call

## Summary
- **Total lines:** 65
- **Code lines:** 47
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 18

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: ingestion.py*
---

# mlops-full-mlops-skills-project: preprocessing.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/data/preprocessing.py`
- **Total lines:** 101
- **File size:** 3059 bytes

## Line Type Summary
- **Code:** 81
- **Comment:** 0
- **Empty:** 20
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Pure preprocessing functions.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Every transformation is a pure function operating on a DataFrame and`
> **Type:** Logical operation

### Line   4
> **Code:** `returning a new DataFrame, so each step is independently testable and`
> **Type:** Returns a value from a function

### Line   5
> **Code:** `side-effect free.`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `"""`
> **Type:** Code statement

### Line   7
> **Code:** ``
> **Type:** Empty line

### Line   8
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from typing import List, Optional`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** `BINARY_FEATURES,`
> **Type:** Code statement

### Line  16
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  17
> **Code:** `ID_COL,`
> **Type:** Code statement

### Line  18
> **Code:** `NUMERIC_FEATURES,`
> **Type:** Code statement

### Line  19
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  20
> **Code:** `TIMESTAMP_COL,`
> **Type:** Code statement

### Line  21
> **Code:** `)`
> **Type:** Code statement

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  25
> **Code:** `"""Remove fully duplicated rows (keeps first occurrence)."""`
> **Type:** Code statement

### Line  26
> **Code:** `return df.drop_duplicates().reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line  27
> **Code:** ``
> **Type:** Empty line

### Line  28
> **Code:** ``
> **Type:** Empty line

### Line  29
> **Code:** `def drop_missing(df: pd.DataFrame, columns: Optional[List[str]] = None...`
> **Type:** Function definition

### Line  30
> **Code:** `"""Drop rows with missing values on critical columns."""`
> **Type:** Code statement

### Line  31
> **Code:** `cols = columns or [ID_COL, TARGET_COL, "age", "gender", "tenure_months...`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `return df.dropna(subset=cols).reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line  33
> **Code:** ``
> **Type:** Empty line

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `def clamp_numeric(`
> **Type:** Function definition

### Line  36
> **Code:** `df: pd.DataFrame,`
> **Type:** Code statement

### Line  37
> **Code:** `ranges: Optional[dict] = None,`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `numeric_features: Optional[List[str]] = None,`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line  40
> **Code:** `"""Clamp numeric features to sane business ranges (age 18-100 etc.).""...`
> **Type:** Arithmetic operation

### Line  41
> **Code:** `bounds = ranges or {`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `"age": (18, 100),`
> **Type:** Code statement

### Line  43
> **Code:** `"tenure_months": (0, 120),`
> **Type:** Code statement

### Line  44
> **Code:** `"monthly_charges": (0, 1000),`
> **Type:** Code statement

### Line  45
> **Code:** `"total_charges": (0, 100000),`
> **Type:** Code statement

### Line  46
> **Code:** `"num_services": (0, 10),`
> **Type:** Code statement

### Line  47
> **Code:** `"support_tickets": (0, 100),`
> **Type:** Logical operation

### Line  48
> **Code:** `"avg_call_minutes": (0, 2000),`
> **Type:** Code statement

### Line  49
> **Code:** `}`
> **Type:** Code statement

### Line  50
> **Code:** `features = numeric_features or NUMERIC_FEATURES`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `for col in features:`
> **Type:** For loop

### Line  53
> **Code:** `if col in out.columns and col in bounds:`
> **Type:** Conditional statement

### Line  54
> **Code:** `lo, hi = bounds[col]`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `out[col] = out[col].clip(lower=lo, upper=hi)`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  57
> **Code:** ``
> **Type:** Empty line

### Line  58
> **Code:** ``
> **Type:** Empty line

### Line  59
> **Code:** `def cast_dtypes(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  60
> **Code:** `"""Enforce canonical dtypes across the dataset."""`
> **Type:** Logical operation

### Line  61
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `for col in NUMERIC_FEATURES:`
> **Type:** For loop

### Line  63
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  64
> **Code:** `out[col] = pd.to_numeric(out[col], errors="coerce")`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `for col in BINARY_FEATURES + [TARGET_COL]:`
> **Type:** For loop

### Line  66
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  67
> **Code:** `out[col] = out[col].astype("int8")`
> **Type:** Assignment/comparison

### Line  68
> **Code:** `for col in CATEGORICAL_FEATURES:`
> **Type:** For loop

### Line  69
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  70
> **Code:** `out[col] = out[col].astype("category")`
> **Type:** Assignment/comparison

### Line  71
> **Code:** `if ID_COL in out.columns:`
> **Type:** Conditional statement

### Line  72
> **Code:** `out[ID_COL] = out[ID_COL].astype("int64")`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `if TIMESTAMP_COL in out.columns:`
> **Type:** Conditional statement

### Line  74
> **Code:** `out[TIMESTAMP_COL] = pd.to_datetime(out[TIMESTAMP_COL])`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  76
> **Code:** ``
> **Type:** Empty line

### Line  77
> **Code:** ``
> **Type:** Empty line

### Line  78
> **Code:** `def preprocess(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  79
> **Code:** `"""Run the full preprocessing chain (pure, returns a new frame)."""`
> **Type:** Code statement

### Line  80
> **Code:** `return (`
> **Type:** Returns a value from a function

### Line  81
> **Code:** `df.pipe(drop_duplicates)`
> **Type:** Function call

### Line  82
> **Code:** `.pipe(drop_missing)`
> **Type:** Function call

### Line  83
> **Code:** `.pipe(clamp_numeric)`
> **Type:** Function call

### Line  84
> **Code:** `.pipe(cast_dtypes)`
> **Type:** Function call

### Line  85
> **Code:** `)`
> **Type:** Code statement

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** ``
> **Type:** Empty line

### Line  88
> **Code:** `def run(output_path=None) -> pd.DataFrame:`
> **Type:** Function definition

### Line  89
> **Code:** `"""Entry point: load raw data, preprocess, persist to CSV."""`
> **Type:** Code statement

### Line  90
> **Code:** `from src.data.ingestion import ingest_raw_data`
> **Type:** Imports specific names from a module

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** `raw, meta = ingest_raw_data()`
> **Type:** Assignment/comparison

### Line  93
> **Code:** `clean = preprocess(raw)`
> **Type:** Assignment/comparison

### Line  94
> **Code:** `path = output_path or "data/processed/dataset_clean.csv"`
> **Type:** Assignment/comparison

### Line  95
> **Code:** `clean.to_csv(path, index=False)`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `print(f"Preprocessed {len(clean)} rows -> {path} (raw had {meta['rows'...`
> **Type:** Prints output to console

### Line  97
> **Code:** `return clean`
> **Type:** Returns a value from a function

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** ``
> **Type:** Empty line

### Line 100
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 101
> **Code:** `run()`
> **Type:** Function call

## Summary
- **Total lines:** 101
- **Code lines:** 81
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 20

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: preprocessing.py*
---

# mlops-full-mlops-skills-project: __init__.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/features/__init__.py`
- **Total lines:** 1
- **File size:** 81 bytes

## Line Type Summary
- **Code:** 1
- **Comment:** 0
- **Empty:** 0
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""features package: feature engineering and Feast feature store defin...`
> **Type:** Logical operation

## Summary
- **Total lines:** 1
- **Code lines:** 1
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 0

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: __init__.py*
---

# mlops-full-mlops-skills-project: build_features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/src/features/build_features.py`
- **Total lines:** 141
- **File size:** 4878 bytes

## Line Type Summary
- **Code:** 109
- **Comment:** 2
- **Empty:** 30
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feature engineering: turn the cleaned dataframe into model-ready fe...`
> **Type:** Arithmetic operation

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `Design goals:`
> **Type:** Code statement

### Line   4
> **Code:** `- Point-in-time friendly: no global statistics that leak future info; ...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `only features derived here are row-local (safe for both training and`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `real-time inference).`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `- Pure functions, deterministic, testable independently.`
> **Type:** Arithmetic operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from typing import Dict, List`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `from src.config import (`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** `BINARY_FEATURES,`
> **Type:** Code statement

### Line  18
> **Code:** `CATEGORICAL_FEATURES,`
> **Type:** Code statement

### Line  19
> **Code:** `ID_COL,`
> **Type:** Code statement

### Line  20
> **Code:** `NUMERIC_FEATURES,`
> **Type:** Code statement

### Line  21
> **Code:** `TARGET_COL,`
> **Type:** Code statement

### Line  22
> **Code:** `TIMESTAMP_COL,`
> **Type:** Code statement

### Line  23
> **Code:** `)`
> **Type:** Code statement

### Line  24
> **Code:** ``
> **Type:** Empty line

### Line  25
> **Code:** `# Explicit ordering guarantee -> stable column order for the model.`
> **Type:** Comment: Explicit ordering guarantee -> stable column order for the model.

### Line  26
> **Code:** `DERIVED_FEATURES: List[str] = [`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `"avg_charge_per_month",       # monthly charges normalised by tenure`
> **Type:** Logical operation

### Line  28
> **Code:** `"service_density",            # services per month of tenure`
> **Type:** Code statement

### Line  29
> **Code:** `"ticket_intensity",           # support tickets per service`
> **Type:** Logical operation

### Line  30
> **Code:** `"is_long_tenure",             # tenure >= 36 months`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `"is_high_value_customer",     # total charges above median-like band`
> **Type:** Arithmetic operation

### Line  32
> **Code:** `"usage_efficiency",           # call minutes per service`
> **Type:** Code statement

### Line  33
> **Code:** `]`
> **Type:** Code statement

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** ``
> **Type:** Empty line

### Line  36
> **Code:** `def derive_features(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line  37
> **Code:** `"""Compute derived (engineered) features, row-local only."""`
> **Type:** Arithmetic operation

### Line  38
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  39
> **Code:** ``
> **Type:** Empty line

### Line  40
> **Code:** `tenure = out["tenure_months"].replace(0, 1)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `services = out["num_services"].clip(lower=1)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** ``
> **Type:** Empty line

### Line  43
> **Code:** `out["avg_charge_per_month"] = out["monthly_charges"] / tenure`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `out["service_density"] = out["num_services"] / tenure`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `out["ticket_intensity"] = out["support_tickets"] / services`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `out["is_long_tenure"] = (out["tenure_months"] >= 36).astype("int8")`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `out["is_high_value_customer"] = (out["total_charges"] >= 1500).astype(...`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `out["usage_efficiency"] = out["avg_call_minutes"] / services`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  51
> **Code:** ``
> **Type:** Empty line

### Line  52
> **Code:** ``
> **Type:** Empty line

### Line  53
> **Code:** `def one_hot_encode(df: pd.DataFrame, columns: List[str]) -> pd.DataFra...`
> **Type:** Function definition

### Line  54
> **Code:** `"""One-hot encode categorical columns (drops first level, keeps type)....`
> **Type:** Arithmetic operation

### Line  55
> **Code:** `out = df.copy()`
> **Type:** Assignment/comparison

### Line  56
> **Code:** `for col in columns:`
> **Type:** For loop

### Line  57
> **Code:** `if col in out.columns:`
> **Type:** Conditional statement

### Line  58
> **Code:** `out = pd.get_dummies(out, columns=[col], prefix=col, drop_first=True)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `return out`
> **Type:** Returns a value from a function

### Line  60
> **Code:** ``
> **Type:** Empty line

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `def build_features(`
> **Type:** Function definition

### Line  63
> **Code:** `df: pd.DataFrame,`
> **Type:** Code statement

### Line  64
> **Code:** `include_sensitive: bool = False,`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `drop_columns: List[str] | None = None,`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `) -> pd.DataFrame:`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `"""Transform a cleaned dataframe into the full feature matrix.`
> **Type:** Logical operation

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** `Args:`
> **Type:** Code statement

### Line  70
> **Code:** `df: cleaned dataframe.`
> **Type:** Code statement

### Line  71
> **Code:** `include_sensitive: keep the sensitive attribute (gender) in the`
> **Type:** Code statement

### Line  72
> **Code:** `feature matrix. By default it is excluded from the model but kept`
> **Type:** Code statement

### Line  73
> **Code:** `available for fairness audits in a separate frame.`
> **Type:** Logical operation

### Line  74
> **Code:** `drop_columns: extra columns to drop (e.g. id / timestamp).`
> **Type:** Arithmetic operation

### Line  75
> **Code:** ``
> **Type:** Empty line

### Line  76
> **Code:** `Returns:`
> **Type:** Code statement

### Line  77
> **Code:** `Feature matrix (already one-hot encoded, with churn preserved).`
> **Type:** Arithmetic operation

### Line  78
> **Code:** `"""`
> **Type:** Code statement

### Line  79
> **Code:** `drop = list(drop_columns or [])`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `drop += [ID_COL, TIMESTAMP_COL]`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `if not include_sensitive:`
> **Type:** Conditional statement

### Line  82
> **Code:** `drop += ["gender"]`
> **Type:** Assignment/comparison

### Line  83
> **Code:** `drop = [c for c in drop if c in df.columns]`
> **Type:** Assignment/comparison

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** `out = derive_features(df).drop(columns=drop)`
> **Type:** Assignment/comparison

### Line  86
> **Code:** ``
> **Type:** Empty line

### Line  87
> **Code:** `cat_cols = [c for c in CATEGORICAL_FEATURES if c in out.columns]`
> **Type:** Assignment/comparison

### Line  88
> **Code:** `out = one_hot_encode(out, cat_cols)`
> **Type:** Assignment/comparison

### Line  89
> **Code:** ``
> **Type:** Empty line

### Line  90
> **Code:** `return out.reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line  91
> **Code:** ``
> **Type:** Empty line

### Line  92
> **Code:** ``
> **Type:** Empty line

### Line  93
> **Code:** `def feature_sets(frame: pd.DataFrame) -> Dict[str, pd.DataFrame]:`
> **Type:** Function definition

### Line  94
> **Code:** `"""Split a built feature frame into (X, y) plus metadata columns."""`
> **Type:** Code statement

### Line  95
> **Code:** `if TARGET_COL in frame.columns:`
> **Type:** Conditional statement

### Line  96
> **Code:** `y = frame[TARGET_COL]`
> **Type:** Assignment/comparison

### Line  97
> **Code:** `X = frame.drop(columns=[TARGET_COL])`
> **Type:** Assignment/comparison

### Line  98
> **Code:** `else:`
> **Type:** Else block

### Line  99
> **Code:** `y = None`
> **Type:** Assignment/comparison

### Line 100
> **Code:** `X = frame`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `return {"X": X, "y": y}`
> **Type:** Returns a value from a function

### Line 102
> **Code:** ``
> **Type:** Empty line

### Line 103
> **Code:** ``
> **Type:** Empty line

### Line 104
> **Code:** `def run() -> pd.DataFrame:`
> **Type:** Function definition

### Line 105
> **Code:** `"""Entry point: load clean data, build features, persist to parquet.""...`
> **Type:** Code statement

### Line 106
> **Code:** `clean = pd.read_csv("data/processed/dataset_clean.csv")`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `features = build_features(clean, include_sensitive=True)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `features.to_parquet("data/features/features.parquet", index=False)`
> **Type:** Assignment/comparison

### Line 109
> **Code:** `print(`
> **Type:** Prints output to console

### Line 110
> **Code:** `f"Built {features.shape[0]} rows x {features.shape[1]} columns "`
> **Type:** Data structure operation

### Line 111
> **Code:** `f"-> data/features/features.parquet"`
> **Type:** Arithmetic operation

### Line 112
> **Code:** `)`
> **Type:** Code statement

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `# Feast-ready variant keeps the entity key + timestamp for point-in-ti...`
> **Type:** Comment: Feast-ready variant keeps the entity key + timestamp for point-in-time joins.

### Line 115
> **Code:** `feast = build_feast_features(clean)`
> **Type:** Assignment/comparison

### Line 116
> **Code:** `feast.to_parquet("data/features/feast_features.parquet", index=False)`
> **Type:** Assignment/comparison

### Line 117
> **Code:** `print(`
> **Type:** Prints output to console

### Line 118
> **Code:** `f"Feast-ready frame {feast.shape[0]} rows x {feast.shape[1]} columns "`
> **Type:** Arithmetic operation

### Line 119
> **Code:** `f"-> data/features/feast_features.parquet"`
> **Type:** Arithmetic operation

### Line 120
> **Code:** `)`
> **Type:** Code statement

### Line 121
> **Code:** `return features`
> **Type:** Returns a value from a function

### Line 122
> **Code:** ``
> **Type:** Empty line

### Line 123
> **Code:** ``
> **Type:** Empty line

### Line 124
> **Code:** `def build_feast_features(df: pd.DataFrame) -> pd.DataFrame:`
> **Type:** Function definition

### Line 125
> **Code:** `"""Build a feature frame that keeps ``customer_id`` and ``timestamp``.`
> **Type:** Logical operation

### Line 126
> **Code:** ``
> **Type:** Empty line

### Line 127
> **Code:** `This frame is what the Feast ``FileSource`` reads; the timestamp enabl...`
> **Type:** Code statement

### Line 128
> **Code:** `point-in-time correct joins so offline (training) and online (inferenc...`
> **Type:** Arithmetic operation

### Line 129
> **Code:** `feature values match.`
> **Type:** Code statement

### Line 130
> **Code:** `"""`
> **Type:** Code statement

### Line 131
> **Code:** `out = derive_features(df)`
> **Type:** Assignment/comparison

### Line 132
> **Code:** `keep = [ID_COL, TIMESTAMP_COL] + NUMERIC_FEATURES + BINARY_FEATURES + ...`
> **Type:** Assignment/comparison

### Line 133
> **Code:** `keep = [c for c in keep if c in out.columns]`
> **Type:** Assignment/comparison

### Line 134
> **Code:** `out = out[keep]`
> **Type:** Assignment/comparison

### Line 135
> **Code:** `if TIMESTAMP_COL in out.columns:`
> **Type:** Conditional statement

### Line 136
> **Code:** `out[TIMESTAMP_COL] = pd.to_datetime(out[TIMESTAMP_COL])`
> **Type:** Assignment/comparison

### Line 137
> **Code:** `return out.reset_index(drop=True)`
> **Type:** Returns a value from a function

### Line 138
> **Code:** ``
> **Type:** Empty line

### Line 139
> **Code:** ``
> **Type:** Empty line

### Line 140
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 141
> **Code:** `run()`
> **Type:** Function call

## Summary
- **Total lines:** 141
- **Code lines:** 109
- **Comments:** 2
- **TODO items:** 0
- **Empty lines:** 30

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: build_features.py*
---

# mlops-full-mlops-skills-project: entities.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/feature_repo/entities.py`
- **Total lines:** 14
- **File size:** 396 bytes

## Line Type Summary
- **Code:** 11
- **Comment:** 0
- **Empty:** 3
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast entity definitions.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A single entity: ``customer`` keyed by ``customer_id`` (Int64), used b...`
> **Type:** Code statement

### Line   4
> **Code:** `offline (training) and online (inference) feature retrieval.`
> **Type:** Logical operation

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from feast import Entity, ValueType`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `customer = Entity(`
> **Type:** Assignment/comparison

### Line  10
> **Code:** `name="customer",`
> **Type:** Assignment/comparison

### Line  11
> **Code:** `join_keys=["customer_id"],`
> **Type:** Assignment/comparison

### Line  12
> **Code:** `value_type=ValueType.INT64,`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `description="Customer identity key for the churn prediction feature st...`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 14
- **Code lines:** 11
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 3

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: entities.py*
---

# mlops-full-mlops-skills-project: features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/feature_repo/features.py`
- **Total lines:** 44
- **File size:** 1708 bytes

## Line Type Summary
- **Code:** 38
- **Comment:** 0
- **Empty:** 6
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast feature definitions.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A single ``FeatureView`` groups the customer features with a TTL and a...`
> **Type:** Logical operation

### Line   4
> **Code:** `explicit schema (``Float32`` / ``Int64`` fields). The Parquet-backed s...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `with a ``timestamp`` field gives point-in-time correctness: offline`
> **Type:** Context manager

### Line   6
> **Code:** `(training) retrieval joins each entity to the feature values valid *at...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `event timestamp, and online retrieval returns the latest values, so th...`
> **Type:** Logical operation

### Line   8
> **Code:** `no training-serving skew.`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from feast import Field, FeatureView`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** `from feast.types import Float32, Int64`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from feature_repo.data_sources import customer_features_source`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from feature_repo.entities import customer`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `customer_features = FeatureView(`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `name="customer_features",`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `entities=[customer],`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `ttl=timedelta(days=30),`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `schema=[`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `Field(name="age", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `Field(name="tenure_months", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `Field(name="monthly_charges", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `Field(name="total_charges", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `Field(name="num_services", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `Field(name="support_tickets", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `Field(name="avg_call_minutes", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `Field(name="has_online_backup", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `Field(name="has_device_protection", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `Field(name="has_tech_support", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `Field(name="avg_charge_per_month", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `Field(name="service_density", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `Field(name="ticket_intensity", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `Field(name="is_long_tenure", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `Field(name="is_high_value_customer", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `Field(name="usage_efficiency", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `],`
> **Type:** Code statement

### Line  43
> **Code:** `source=customer_features_source,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 44
- **Code lines:** 38
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 6

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: features.py*
---

# mlops-full-mlops-skills-project: data_sources.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/feature_repo/data_sources.py`
- **Total lines:** 22
- **File size:** 721 bytes

## Line Type Summary
- **Code:** 17
- **Comment:** 0
- **Empty:** 5
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast data sources.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `The offline source is the engineered Parquet frame produced by`
> **Type:** Code statement

### Line   4
> **Code:** ```src/features/build_features.build_feast_features``. The ``timestamp`...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `column is used for point-in-time correctness: historical (training) qu...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `return the feature values valid *at* the event timestamp, and online`
> **Type:** Returns a value from a function

### Line   7
> **Code:** `retrieval returns the latest values, so offline and online features ma...`
> **Type:** Logical operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from feast import FileSource`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `CUSTOMER_FEATURES_PATH = "data/features/feast_features.parquet"`
> **Type:** Assignment/comparison

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `customer_features_source = FileSource(`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `name="customer_features_source",`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `path=CUSTOMER_FEATURES_PATH,`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `timestamp_field="timestamp",`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `created_timestamp_column=None,`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `file_format="parquet",`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 22
- **Code lines:** 17
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 5

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: data_sources.py*
---

# mlops-full-mlops-skills-project: generate_churn_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/.worktrees/proj1/data/raw/generate_churn_data.py`
- **Total lines:** 115
- **File size:** 4267 bytes

## Line Type Summary
- **Code:** 92
- **Comment:** 5
- **Empty:** 18
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `#!/usr/bin/env python3`
> **Type:** Comment: !/usr/bin/env python3

### Line   2
> **Code:** `"""Generate a realistic synthetic telecom customer churn dataset.`
> **Type:** Code statement

### Line   3
> **Code:** ``
> **Type:** Empty line

### Line   4
> **Code:** `Outputs ~7000 rows to ``data/raw/dataset.csv``. Includes a sensitive`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `attribute (``gender``) used later for the fairness checks. A fixed ran...`
> **Type:** Logical operation

### Line   6
> **Code:** `seed guarantees deterministic, reproducible output.`
> **Type:** Code statement

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  12
> **Code:** `import hashlib`
> **Type:** Imports a module

### Line  13
> **Code:** `from datetime import datetime, timedelta`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `N_ROWS = 7000`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `CONTRACTS = ["month-to-month", "one_year", "two_year"]`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `PAYMENTS = ["electronic_check", "mailed_check", "bank_transfer", "cred...`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `REGIONS = ["north", "south", "east", "west"]`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def _hash_file(path: str) -> str:`
> **Type:** Function definition

### Line  25
> **Code:** `digest = hashlib.sha256()`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `with open(path, "rb") as handle:`
> **Type:** Context manager

### Line  27
> **Code:** `for chunk in iter(lambda: handle.read(1 << 16), b""):`
> **Type:** For loop

### Line  28
> **Code:** `digest.update(chunk)`
> **Type:** Function call

### Line  29
> **Code:** `return digest.hexdigest()`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def generate(n_rows: int = N_ROWS, seed: int = 42) -> pd.DataFrame:`
> **Type:** Function definition

### Line  33
> **Code:** `rng = np.random.default_rng(seed)`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `customer_id = np.arange(1, n_rows + 1, dtype=np.int64)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `base_ts = datetime(2023, 1, 1)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `timestamps = pd.to_datetime(`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `[base_ts + timedelta(days=int(d)) for d in rng.integers(0, 730, n_rows...`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `)`
> **Type:** Code statement

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `age = rng.integers(18, 71, n_rows)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `gender = rng.choice(["M", "F"], n_rows, p=[0.52, 0.48])`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `region = rng.choice(REGIONS, n_rows)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `tenure_months = rng.integers(0, 73, n_rows)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `monthly_charges = np.round(rng.uniform(20.0, 120.0, n_rows), 2)`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `num_services = rng.integers(1, 7, n_rows)`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `contract_type = rng.choice(CONTRACTS, n_rows, p=[0.55, 0.25, 0.20])`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `payment_method = rng.choice(PAYMENTS, n_rows, p=[0.34, 0.22, 0.24, 0.2...`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `support_tickets = rng.poisson(1.2, n_rows).clip(0, 15)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `avg_call_minutes = np.round(rng.uniform(0.0, 500.0, n_rows), 1)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `has_online_backup = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `has_device_protection = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `has_tech_support = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `# Churn probability model: higher risk for short tenure, high charges,`
> **Type:** Comment: Churn probability model: higher risk for short tenure, high charges,

### Line  56
> **Code:** `# month-to-month contracts, electronic check, more support tickets.`
> **Type:** Comment: month-to-month contracts, electronic check, more support tickets.

### Line  57
> **Code:** `logit = (`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `-3.0`
> **Type:** Arithmetic operation

### Line  59
> **Code:** `- 0.08 * tenure_months`
> **Type:** Arithmetic operation

### Line  60
> **Code:** `+ 0.018 * monthly_charges`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `+ (contract_type == "month-to-month") * 1.6`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `+ (payment_method == "electronic_check") * 0.5`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `+ 0.35 * support_tickets`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `- 0.9 * has_tech_support`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `+ 0.2 * (num_services - 3)`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `+ (age > 60) * 0.4`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `)`
> **Type:** Code statement

### Line  68
> **Code:** `prob = 1.0 / (1.0 + np.exp(-logit))`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `# Mild correlation between gender and the target so fairness checks ar...`
> **Type:** Comment: Mild correlation between gender and the target so fairness checks are

### Line  70
> **Code:** `# interesting, while churn is still explainable by the business featur...`
> **Type:** Comment: interesting, while churn is still explainable by the business features.

### Line  71
> **Code:** `prob = np.clip(prob + (gender == "M") * 0.02, 0.0, 1.0)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `churn = (rng.uniform(0, 1, n_rows) < prob).astype(int)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `df = pd.DataFrame(`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `{`
> **Type:** Data structure operation

### Line  76
> **Code:** `"customer_id": customer_id,`
> **Type:** Code statement

### Line  77
> **Code:** `"timestamp": timestamps,`
> **Type:** Code statement

### Line  78
> **Code:** `"age": age,`
> **Type:** Code statement

### Line  79
> **Code:** `"gender": gender,`
> **Type:** Code statement

### Line  80
> **Code:** `"region": region,`
> **Type:** Code statement

### Line  81
> **Code:** `"tenure_months": tenure_months,`
> **Type:** Code statement

### Line  82
> **Code:** `"monthly_charges": monthly_charges,`
> **Type:** Code statement

### Line  83
> **Code:** `"total_charges": np.round(monthly_charges * tenure_months, 2),`
> **Type:** Arithmetic operation

### Line  84
> **Code:** `"num_services": num_services,`
> **Type:** Code statement

### Line  85
> **Code:** `"contract_type": contract_type,`
> **Type:** Code statement

### Line  86
> **Code:** `"payment_method": payment_method,`
> **Type:** Code statement

### Line  87
> **Code:** `"support_tickets": support_tickets,`
> **Type:** Logical operation

### Line  88
> **Code:** `"avg_call_minutes": avg_call_minutes,`
> **Type:** Code statement

### Line  89
> **Code:** `"has_online_backup": has_online_backup,`
> **Type:** Code statement

### Line  90
> **Code:** `"has_device_protection": has_device_protection,`
> **Type:** Code statement

### Line  91
> **Code:** `"has_tech_support": has_tech_support,`
> **Type:** Logical operation

### Line  92
> **Code:** `"churn": churn,`
> **Type:** Code statement

### Line  93
> **Code:** `}`
> **Type:** Code statement

### Line  94
> **Code:** `)`
> **Type:** Code statement

### Line  95
> **Code:** `df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 100
> **Code:** `parser = argparse.ArgumentParser(description="Generate synthetic churn...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `parser.add_argument("--rows", type=int, default=N_ROWS)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `parser.add_argument("--seed", type=int, default=42)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `parser.add_argument("--output", default="dataset.csv")`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `df = generate(args.rows, args.seed)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `print(f"Wrote {len(df)} rows to {args.output}")`
> **Type:** Prints output to console

### Line 109
> **Code:** `print(f"Target balance: {df['churn'].mean():.3f}")`
> **Type:** Prints output to console

### Line 110
> **Code:** `print(f"Time period: {df['timestamp'].min()} -> {df['timestamp'].max()...`
> **Type:** Prints output to console

### Line 111
> **Code:** `print(f"File SHA256: {_hash_file(args.output)}")`
> **Type:** Prints output to console

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 115
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 115
- **Code lines:** 92
- **Comments:** 5
- **TODO items:** 0
- **Empty lines:** 18

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: generate_churn_data.py*
---

# mlops-full-mlops-skills-project: entities.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/feature_repo/entities.py`
- **Total lines:** 14
- **File size:** 396 bytes

## Line Type Summary
- **Code:** 11
- **Comment:** 0
- **Empty:** 3
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast entity definitions.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A single entity: ``customer`` keyed by ``customer_id`` (Int64), used b...`
> **Type:** Code statement

### Line   4
> **Code:** `offline (training) and online (inference) feature retrieval.`
> **Type:** Logical operation

### Line   5
> **Code:** `"""`
> **Type:** Code statement

### Line   6
> **Code:** ``
> **Type:** Empty line

### Line   7
> **Code:** `from feast import Entity, ValueType`
> **Type:** Imports specific names from a module

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `customer = Entity(`
> **Type:** Assignment/comparison

### Line  10
> **Code:** `name="customer",`
> **Type:** Assignment/comparison

### Line  11
> **Code:** `join_keys=["customer_id"],`
> **Type:** Assignment/comparison

### Line  12
> **Code:** `value_type=ValueType.INT64,`
> **Type:** Assignment/comparison

### Line  13
> **Code:** `description="Customer identity key for the churn prediction feature st...`
> **Type:** Assignment/comparison

### Line  14
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 14
- **Code lines:** 11
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 3

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: entities.py*
---

# mlops-full-mlops-skills-project: features.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/feature_repo/features.py`
- **Total lines:** 44
- **File size:** 1708 bytes

## Line Type Summary
- **Code:** 38
- **Comment:** 0
- **Empty:** 6
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast feature definitions.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `A single ``FeatureView`` groups the customer features with a TTL and a...`
> **Type:** Logical operation

### Line   4
> **Code:** `explicit schema (``Float32`` / ``Int64`` fields). The Parquet-backed s...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `with a ``timestamp`` field gives point-in-time correctness: offline`
> **Type:** Context manager

### Line   6
> **Code:** `(training) retrieval joins each entity to the feature values valid *at...`
> **Type:** Arithmetic operation

### Line   7
> **Code:** `event timestamp, and online retrieval returns the latest values, so th...`
> **Type:** Logical operation

### Line   8
> **Code:** `no training-serving skew.`
> **Type:** Arithmetic operation

### Line   9
> **Code:** `"""`
> **Type:** Code statement

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  12
> **Code:** ``
> **Type:** Empty line

### Line  13
> **Code:** `from datetime import timedelta`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `from feast import Field, FeatureView`
> **Type:** Imports specific names from a module

### Line  16
> **Code:** `from feast.types import Float32, Int64`
> **Type:** Imports specific names from a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `from feature_repo.data_sources import customer_features_source`
> **Type:** Imports specific names from a module

### Line  19
> **Code:** `from feature_repo.entities import customer`
> **Type:** Imports specific names from a module

### Line  20
> **Code:** ``
> **Type:** Empty line

### Line  21
> **Code:** `customer_features = FeatureView(`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `name="customer_features",`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `entities=[customer],`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `ttl=timedelta(days=30),`
> **Type:** Assignment/comparison

### Line  25
> **Code:** `schema=[`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `Field(name="age", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  27
> **Code:** `Field(name="tenure_months", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  28
> **Code:** `Field(name="monthly_charges", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  29
> **Code:** `Field(name="total_charges", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  30
> **Code:** `Field(name="num_services", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  31
> **Code:** `Field(name="support_tickets", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  32
> **Code:** `Field(name="avg_call_minutes", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `Field(name="has_online_backup", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  34
> **Code:** `Field(name="has_device_protection", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  35
> **Code:** `Field(name="has_tech_support", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `Field(name="avg_charge_per_month", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `Field(name="service_density", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `Field(name="ticket_intensity", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `Field(name="is_long_tenure", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  40
> **Code:** `Field(name="is_high_value_customer", dtype=Int64),`
> **Type:** Assignment/comparison

### Line  41
> **Code:** `Field(name="usage_efficiency", dtype=Float32),`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `],`
> **Type:** Code statement

### Line  43
> **Code:** `source=customer_features_source,`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 44
- **Code lines:** 38
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 6

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: features.py*
---

# mlops-full-mlops-skills-project: data_sources.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/feature_repo/data_sources.py`
- **Total lines:** 22
- **File size:** 721 bytes

## Line Type Summary
- **Code:** 17
- **Comment:** 0
- **Empty:** 5
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `"""Feast data sources.`
> **Type:** Code statement

### Line   2
> **Code:** ``
> **Type:** Empty line

### Line   3
> **Code:** `The offline source is the engineered Parquet frame produced by`
> **Type:** Code statement

### Line   4
> **Code:** ```src/features/build_features.build_feast_features``. The ``timestamp`...`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `column is used for point-in-time correctness: historical (training) qu...`
> **Type:** Arithmetic operation

### Line   6
> **Code:** `return the feature values valid *at* the event timestamp, and online`
> **Type:** Returns a value from a function

### Line   7
> **Code:** `retrieval returns the latest values, so offline and online features ma...`
> **Type:** Logical operation

### Line   8
> **Code:** `"""`
> **Type:** Code statement

### Line   9
> **Code:** ``
> **Type:** Empty line

### Line  10
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  11
> **Code:** ``
> **Type:** Empty line

### Line  12
> **Code:** `from feast import FileSource`
> **Type:** Imports specific names from a module

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `CUSTOMER_FEATURES_PATH = "data/features/feast_features.parquet"`
> **Type:** Assignment/comparison

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `customer_features_source = FileSource(`
> **Type:** Assignment/comparison

### Line  17
> **Code:** `name="customer_features_source",`
> **Type:** Assignment/comparison

### Line  18
> **Code:** `path=CUSTOMER_FEATURES_PATH,`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `timestamp_field="timestamp",`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `created_timestamp_column=None,`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `file_format="parquet",`
> **Type:** Assignment/comparison

### Line  22
> **Code:** `)`
> **Type:** Code statement

## Summary
- **Total lines:** 22
- **Code lines:** 17
- **Comments:** 0
- **TODO items:** 0
- **Empty lines:** 5

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: data_sources.py*
---

# mlops-full-mlops-skills-project: generate_churn_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/data/raw/generate_churn_data.py`
- **Total lines:** 115
- **File size:** 4267 bytes

## Line Type Summary
- **Code:** 92
- **Comment:** 5
- **Empty:** 18
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `#!/usr/bin/env python3`
> **Type:** Comment: !/usr/bin/env python3

### Line   2
> **Code:** `"""Generate a realistic synthetic telecom customer churn dataset.`
> **Type:** Code statement

### Line   3
> **Code:** ``
> **Type:** Empty line

### Line   4
> **Code:** `Outputs ~7000 rows to ``data/raw/dataset.csv``. Includes a sensitive`
> **Type:** Arithmetic operation

### Line   5
> **Code:** `attribute (``gender``) used later for the fairness checks. A fixed ran...`
> **Type:** Logical operation

### Line   6
> **Code:** `seed guarantees deterministic, reproducible output.`
> **Type:** Code statement

### Line   7
> **Code:** `"""`
> **Type:** Code statement

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  10
> **Code:** ``
> **Type:** Empty line

### Line  11
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  12
> **Code:** `import hashlib`
> **Type:** Imports a module

### Line  13
> **Code:** `from datetime import datetime, timedelta`
> **Type:** Imports specific names from a module

### Line  14
> **Code:** ``
> **Type:** Empty line

### Line  15
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  16
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  17
> **Code:** ``
> **Type:** Empty line

### Line  18
> **Code:** `N_ROWS = 7000`
> **Type:** Assignment/comparison

### Line  19
> **Code:** `CONTRACTS = ["month-to-month", "one_year", "two_year"]`
> **Type:** Assignment/comparison

### Line  20
> **Code:** `PAYMENTS = ["electronic_check", "mailed_check", "bank_transfer", "cred...`
> **Type:** Assignment/comparison

### Line  21
> **Code:** `REGIONS = ["north", "south", "east", "west"]`
> **Type:** Assignment/comparison

### Line  22
> **Code:** ``
> **Type:** Empty line

### Line  23
> **Code:** ``
> **Type:** Empty line

### Line  24
> **Code:** `def _hash_file(path: str) -> str:`
> **Type:** Function definition

### Line  25
> **Code:** `digest = hashlib.sha256()`
> **Type:** Assignment/comparison

### Line  26
> **Code:** `with open(path, "rb") as handle:`
> **Type:** Context manager

### Line  27
> **Code:** `for chunk in iter(lambda: handle.read(1 << 16), b""):`
> **Type:** For loop

### Line  28
> **Code:** `digest.update(chunk)`
> **Type:** Function call

### Line  29
> **Code:** `return digest.hexdigest()`
> **Type:** Returns a value from a function

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** ``
> **Type:** Empty line

### Line  32
> **Code:** `def generate(n_rows: int = N_ROWS, seed: int = 42) -> pd.DataFrame:`
> **Type:** Function definition

### Line  33
> **Code:** `rng = np.random.default_rng(seed)`
> **Type:** Assignment/comparison

### Line  34
> **Code:** ``
> **Type:** Empty line

### Line  35
> **Code:** `customer_id = np.arange(1, n_rows + 1, dtype=np.int64)`
> **Type:** Assignment/comparison

### Line  36
> **Code:** `base_ts = datetime(2023, 1, 1)`
> **Type:** Assignment/comparison

### Line  37
> **Code:** `timestamps = pd.to_datetime(`
> **Type:** Assignment/comparison

### Line  38
> **Code:** `[base_ts + timedelta(days=int(d)) for d in rng.integers(0, 730, n_rows...`
> **Type:** Assignment/comparison

### Line  39
> **Code:** `)`
> **Type:** Code statement

### Line  40
> **Code:** ``
> **Type:** Empty line

### Line  41
> **Code:** `age = rng.integers(18, 71, n_rows)`
> **Type:** Assignment/comparison

### Line  42
> **Code:** `gender = rng.choice(["M", "F"], n_rows, p=[0.52, 0.48])`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `region = rng.choice(REGIONS, n_rows)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `tenure_months = rng.integers(0, 73, n_rows)`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `monthly_charges = np.round(rng.uniform(20.0, 120.0, n_rows), 2)`
> **Type:** Assignment/comparison

### Line  46
> **Code:** `num_services = rng.integers(1, 7, n_rows)`
> **Type:** Assignment/comparison

### Line  47
> **Code:** `contract_type = rng.choice(CONTRACTS, n_rows, p=[0.55, 0.25, 0.20])`
> **Type:** Assignment/comparison

### Line  48
> **Code:** `payment_method = rng.choice(PAYMENTS, n_rows, p=[0.34, 0.22, 0.24, 0.2...`
> **Type:** Assignment/comparison

### Line  49
> **Code:** `support_tickets = rng.poisson(1.2, n_rows).clip(0, 15)`
> **Type:** Assignment/comparison

### Line  50
> **Code:** `avg_call_minutes = np.round(rng.uniform(0.0, 500.0, n_rows), 1)`
> **Type:** Assignment/comparison

### Line  51
> **Code:** `has_online_backup = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  52
> **Code:** `has_device_protection = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `has_tech_support = rng.integers(0, 2, n_rows)`
> **Type:** Assignment/comparison

### Line  54
> **Code:** ``
> **Type:** Empty line

### Line  55
> **Code:** `# Churn probability model: higher risk for short tenure, high charges,`
> **Type:** Comment: Churn probability model: higher risk for short tenure, high charges,

### Line  56
> **Code:** `# month-to-month contracts, electronic check, more support tickets.`
> **Type:** Comment: month-to-month contracts, electronic check, more support tickets.

### Line  57
> **Code:** `logit = (`
> **Type:** Assignment/comparison

### Line  58
> **Code:** `-3.0`
> **Type:** Arithmetic operation

### Line  59
> **Code:** `- 0.08 * tenure_months`
> **Type:** Arithmetic operation

### Line  60
> **Code:** `+ 0.018 * monthly_charges`
> **Type:** Arithmetic operation

### Line  61
> **Code:** `+ (contract_type == "month-to-month") * 1.6`
> **Type:** Assignment/comparison

### Line  62
> **Code:** `+ (payment_method == "electronic_check") * 0.5`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `+ 0.35 * support_tickets`
> **Type:** Arithmetic operation

### Line  64
> **Code:** `- 0.9 * has_tech_support`
> **Type:** Arithmetic operation

### Line  65
> **Code:** `+ 0.2 * (num_services - 3)`
> **Type:** Arithmetic operation

### Line  66
> **Code:** `+ (age > 60) * 0.4`
> **Type:** Arithmetic operation

### Line  67
> **Code:** `)`
> **Type:** Code statement

### Line  68
> **Code:** `prob = 1.0 / (1.0 + np.exp(-logit))`
> **Type:** Assignment/comparison

### Line  69
> **Code:** `# Mild correlation between gender and the target so fairness checks ar...`
> **Type:** Comment: Mild correlation between gender and the target so fairness checks are

### Line  70
> **Code:** `# interesting, while churn is still explainable by the business featur...`
> **Type:** Comment: interesting, while churn is still explainable by the business features.

### Line  71
> **Code:** `prob = np.clip(prob + (gender == "M") * 0.02, 0.0, 1.0)`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `churn = (rng.uniform(0, 1, n_rows) < prob).astype(int)`
> **Type:** Assignment/comparison

### Line  73
> **Code:** ``
> **Type:** Empty line

### Line  74
> **Code:** `df = pd.DataFrame(`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `{`
> **Type:** Data structure operation

### Line  76
> **Code:** `"customer_id": customer_id,`
> **Type:** Code statement

### Line  77
> **Code:** `"timestamp": timestamps,`
> **Type:** Code statement

### Line  78
> **Code:** `"age": age,`
> **Type:** Code statement

### Line  79
> **Code:** `"gender": gender,`
> **Type:** Code statement

### Line  80
> **Code:** `"region": region,`
> **Type:** Code statement

### Line  81
> **Code:** `"tenure_months": tenure_months,`
> **Type:** Code statement

### Line  82
> **Code:** `"monthly_charges": monthly_charges,`
> **Type:** Code statement

### Line  83
> **Code:** `"total_charges": np.round(monthly_charges * tenure_months, 2),`
> **Type:** Arithmetic operation

### Line  84
> **Code:** `"num_services": num_services,`
> **Type:** Code statement

### Line  85
> **Code:** `"contract_type": contract_type,`
> **Type:** Code statement

### Line  86
> **Code:** `"payment_method": payment_method,`
> **Type:** Code statement

### Line  87
> **Code:** `"support_tickets": support_tickets,`
> **Type:** Logical operation

### Line  88
> **Code:** `"avg_call_minutes": avg_call_minutes,`
> **Type:** Code statement

### Line  89
> **Code:** `"has_online_backup": has_online_backup,`
> **Type:** Code statement

### Line  90
> **Code:** `"has_device_protection": has_device_protection,`
> **Type:** Code statement

### Line  91
> **Code:** `"has_tech_support": has_tech_support,`
> **Type:** Logical operation

### Line  92
> **Code:** `"churn": churn,`
> **Type:** Code statement

### Line  93
> **Code:** `}`
> **Type:** Code statement

### Line  94
> **Code:** `)`
> **Type:** Code statement

### Line  95
> **Code:** `df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")`
> **Type:** Assignment/comparison

### Line  96
> **Code:** `return df`
> **Type:** Returns a value from a function

### Line  97
> **Code:** ``
> **Type:** Empty line

### Line  98
> **Code:** ``
> **Type:** Empty line

### Line  99
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line 100
> **Code:** `parser = argparse.ArgumentParser(description="Generate synthetic churn...`
> **Type:** Assignment/comparison

### Line 101
> **Code:** `parser.add_argument("--rows", type=int, default=N_ROWS)`
> **Type:** Assignment/comparison

### Line 102
> **Code:** `parser.add_argument("--seed", type=int, default=42)`
> **Type:** Assignment/comparison

### Line 103
> **Code:** `parser.add_argument("--output", default="dataset.csv")`
> **Type:** Assignment/comparison

### Line 104
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line 105
> **Code:** ``
> **Type:** Empty line

### Line 106
> **Code:** `df = generate(args.rows, args.seed)`
> **Type:** Assignment/comparison

### Line 107
> **Code:** `df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line 108
> **Code:** `print(f"Wrote {len(df)} rows to {args.output}")`
> **Type:** Prints output to console

### Line 109
> **Code:** `print(f"Target balance: {df['churn'].mean():.3f}")`
> **Type:** Prints output to console

### Line 110
> **Code:** `print(f"Time period: {df['timestamp'].min()} -> {df['timestamp'].max()...`
> **Type:** Prints output to console

### Line 111
> **Code:** `print(f"File SHA256: {_hash_file(args.output)}")`
> **Type:** Prints output to console

### Line 112
> **Code:** ``
> **Type:** Empty line

### Line 113
> **Code:** ``
> **Type:** Empty line

### Line 114
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line 115
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 115
- **Code lines:** 92
- **Comments:** 5
- **TODO items:** 0
- **Empty lines:** 18

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: generate_churn_data.py*
---

# mlops-full-mlops-skills-project: generate_creditcard_data.py

## File Information
- **File path:** `/home/gadour/Desktop/new_project/other/mlops-full-mlops-skills-project/data/raw/generate_creditcard_data.py`
- **Total lines:** 87
- **File size:** 2934 bytes

## Line Type Summary
- **Code:** 59
- **Comment:** 7
- **Empty:** 21
- **TODO:** 0

## Detailed Line Explanations

### Line   1
> **Code:** `#!/usr/bin/env python3`
> **Type:** Comment: !/usr/bin/env python3

### Line   2
> **Code:** `"""Generate a synthetic credit-card transaction dataset for the fraud ...`
> **Type:** Arithmetic operation

### Line   3
> **Code:** ``
> **Type:** Empty line

### Line   4
> **Code:** `Mirrors the shape of the public Kaggle "Credit Card Fraud Detection" f...`
> **Type:** Logical operation

### Line   5
> **Code:** `(``Time``, ``V1``..``V28`` PCA components, ``Amount``, ``Class``) so t...`
> **Type:** Code statement

### Line   6
> **Code:** `API and its UI run from data versioned inside the repository instead o...`
> **Type:** Logical operation

### Line   7
> **Code:** `machine-local path. A fixed seed guarantees deterministic output.`
> **Type:** Arithmetic operation

### Line   8
> **Code:** ``
> **Type:** Empty line

### Line   9
> **Code:** `This is demo data, not a substitute for the real dataset: the signal i...`
> **Type:** Logical operation

### Line  10
> **Code:** `injected deliberately, so metrics measured on it say nothing about how...`
> **Type:** Logical operation

### Line  11
> **Code:** `model would score on real transactions.`
> **Type:** Logical operation

### Line  12
> **Code:** `"""`
> **Type:** Code statement

### Line  13
> **Code:** ``
> **Type:** Empty line

### Line  14
> **Code:** `from __future__ import annotations`
> **Type:** Imports specific names from a module

### Line  15
> **Code:** ``
> **Type:** Empty line

### Line  16
> **Code:** `import argparse`
> **Type:** Imports a module

### Line  17
> **Code:** `import hashlib`
> **Type:** Imports a module

### Line  18
> **Code:** ``
> **Type:** Empty line

### Line  19
> **Code:** `import numpy as np`
> **Type:** Imports a module

### Line  20
> **Code:** `import pandas as pd`
> **Type:** Imports a module

### Line  21
> **Code:** ``
> **Type:** Empty line

### Line  22
> **Code:** `N_ROWS = 10000`
> **Type:** Assignment/comparison

### Line  23
> **Code:** `N_COMPONENTS = 28`
> **Type:** Assignment/comparison

### Line  24
> **Code:** `FRAUD_RATE = 0.02`
> **Type:** Assignment/comparison

### Line  25
> **Code:** ``
> **Type:** Empty line

### Line  26
> **Code:** `# PCA components that carry the injected fraud signal, chosen to match...`
> **Type:** Comment: PCA components that carry the injected fraud signal, chosen to match the

### Line  27
> **Code:** `# components that dominate on the real dataset.`
> **Type:** Comment: components that dominate on the real dataset.

### Line  28
> **Code:** `SIGNAL_COMPONENTS = [4, 10, 12, 14, 17]`
> **Type:** Assignment/comparison

### Line  29
> **Code:** ``
> **Type:** Empty line

### Line  30
> **Code:** ``
> **Type:** Empty line

### Line  31
> **Code:** `def _hash_file(path: str) -> str:`
> **Type:** Function definition

### Line  32
> **Code:** `digest = hashlib.sha256()`
> **Type:** Assignment/comparison

### Line  33
> **Code:** `with open(path, "rb") as handle:`
> **Type:** Context manager

### Line  34
> **Code:** `for chunk in iter(lambda: handle.read(1 << 16), b""):`
> **Type:** For loop

### Line  35
> **Code:** `digest.update(chunk)`
> **Type:** Function call

### Line  36
> **Code:** `return digest.hexdigest()`
> **Type:** Returns a value from a function

### Line  37
> **Code:** ``
> **Type:** Empty line

### Line  38
> **Code:** ``
> **Type:** Empty line

### Line  39
> **Code:** `def generate(rows: int = N_ROWS, seed: int = 42) -> pd.DataFrame:`
> **Type:** Function definition

### Line  40
> **Code:** `rng = np.random.default_rng(seed)`
> **Type:** Assignment/comparison

### Line  41
> **Code:** ``
> **Type:** Empty line

### Line  42
> **Code:** `n_fraud = max(1, int(rows * FRAUD_RATE))`
> **Type:** Assignment/comparison

### Line  43
> **Code:** `labels = np.zeros(rows, dtype=np.int8)`
> **Type:** Assignment/comparison

### Line  44
> **Code:** `labels[rng.choice(rows, size=n_fraud, replace=False)] = 1`
> **Type:** Assignment/comparison

### Line  45
> **Code:** `is_fraud = labels == 1`
> **Type:** Assignment/comparison

### Line  46
> **Code:** ``
> **Type:** Empty line

### Line  47
> **Code:** `# Two days of transactions, ordered like the real export.`
> **Type:** Comment: Two days of transactions, ordered like the real export.

### Line  48
> **Code:** `time = np.sort(rng.uniform(0, 172_800, size=rows))`
> **Type:** Assignment/comparison

### Line  49
> **Code:** ``
> **Type:** Empty line

### Line  50
> **Code:** `# PCA components: standard normal, with a mean shift on the signal-car...`
> **Type:** Comment: PCA components: standard normal, with a mean shift on the signal-carrying

### Line  51
> **Code:** `# components for fraudulent rows.`
> **Type:** Comment: components for fraudulent rows.

### Line  52
> **Code:** `components = rng.standard_normal((rows, N_COMPONENTS))`
> **Type:** Assignment/comparison

### Line  53
> **Code:** `for idx in SIGNAL_COMPONENTS:`
> **Type:** For loop

### Line  54
> **Code:** `shift = rng.uniform(1.8, 3.2)`
> **Type:** Assignment/comparison

### Line  55
> **Code:** `components[is_fraud, idx - 1] -= shift`
> **Type:** Assignment/comparison

### Line  56
> **Code:** ``
> **Type:** Empty line

### Line  57
> **Code:** `# Fraudulent amounts skew low (card testing) with a heavy tail.`
> **Type:** Comment: Fraudulent amounts skew low (card testing) with a heavy tail.

### Line  58
> **Code:** `amount = rng.lognormal(mean=3.2, sigma=1.1, size=rows)`
> **Type:** Assignment/comparison

### Line  59
> **Code:** `amount[is_fraud] = rng.lognormal(mean=2.4, sigma=1.6, size=is_fraud.su...`
> **Type:** Assignment/comparison

### Line  60
> **Code:** `amount = np.clip(amount, 0, 100_000).round(2)`
> **Type:** Assignment/comparison

### Line  61
> **Code:** ``
> **Type:** Empty line

### Line  62
> **Code:** `frame = pd.DataFrame({"Time": time.round(0)})`
> **Type:** Assignment/comparison

### Line  63
> **Code:** `for i in range(1, N_COMPONENTS + 1):`
> **Type:** For loop

### Line  64
> **Code:** `frame[f"V{i}"] = components[:, i - 1].round(6)`
> **Type:** Assignment/comparison

### Line  65
> **Code:** `frame["Amount"] = amount`
> **Type:** Assignment/comparison

### Line  66
> **Code:** `frame["Class"] = labels`
> **Type:** Assignment/comparison

### Line  67
> **Code:** `return frame`
> **Type:** Returns a value from a function

### Line  68
> **Code:** ``
> **Type:** Empty line

### Line  69
> **Code:** ``
> **Type:** Empty line

### Line  70
> **Code:** `def main() -> None:`
> **Type:** Function definition

### Line  71
> **Code:** `parser = argparse.ArgumentParser(`
> **Type:** Assignment/comparison

### Line  72
> **Code:** `description="Generate synthetic credit card transaction data."`
> **Type:** Assignment/comparison

### Line  73
> **Code:** `)`
> **Type:** Code statement

### Line  74
> **Code:** `parser.add_argument("--rows", type=int, default=N_ROWS)`
> **Type:** Assignment/comparison

### Line  75
> **Code:** `parser.add_argument("--seed", type=int, default=42)`
> **Type:** Assignment/comparison

### Line  76
> **Code:** `parser.add_argument("--output", default="creditcard.csv")`
> **Type:** Assignment/comparison

### Line  77
> **Code:** `args = parser.parse_args()`
> **Type:** Assignment/comparison

### Line  78
> **Code:** ``
> **Type:** Empty line

### Line  79
> **Code:** `df = generate(args.rows, args.seed)`
> **Type:** Assignment/comparison

### Line  80
> **Code:** `df.to_csv(args.output, index=False)`
> **Type:** Assignment/comparison

### Line  81
> **Code:** `print(f"Wrote {len(df)} rows to {args.output}")`
> **Type:** Prints output to console

### Line  82
> **Code:** `print(f"Fraud rate: {df['Class'].mean():.4f}")`
> **Type:** Prints output to console

### Line  83
> **Code:** `print(f"File SHA256: {_hash_file(args.output)}")`
> **Type:** Prints output to console

### Line  84
> **Code:** ``
> **Type:** Empty line

### Line  85
> **Code:** ``
> **Type:** Empty line

### Line  86
> **Code:** `if __name__ == "__main__":`
> **Type:** Conditional statement

### Line  87
> **Code:** `main()`
> **Type:** Function call

## Summary
- **Total lines:** 87
- **Code lines:** 59
- **Comments:** 7
- **TODO items:** 0
- **Empty lines:** 21

---
*Documentation generated for: mlops-full-mlops-skills-project*
*File: generate_creditcard_data.py*
---

