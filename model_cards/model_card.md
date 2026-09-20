# Model Card: Customer Churn Classifier (Attest demo artifact)

*Generated automatically on 2026-09-20T06:47:21.832735*

> Auto-generated demo artifact of the Attest model-risk platform (see
> `mlops-full-mlops-skills-project.md`). The platform's target use case is model risk
> & AI compliance; this churn model exercises the platform's governance pipeline.

## Model details

- Algorithm: RandomForestClassifier
- Task: Binary classification (customer churn)
- Objective: Predict churn probability to enable proactive retention

## Intended use

- Valid: churn risk scoring for telecom customers (demo only)
- Avoid: credit decisions, medical predictions, or any other domain

## Training data

- Source: synthetic telecom dataset (`data/raw/dataset.csv`)
- Rows: ~7000, binary target with a sensitive attribute (`gender`)

## Performance metrics (held-out test set)

| Metric | Value |
| --- | --- |
| accuracy | 0.7672 |
| f1_score | 0.5572 |
| roc_auc | 0.6986 |

## Fairness analysis (Fairlearn)

- Demographic parity difference: None
- Equalized odds difference: None
- Threshold (dp_diff): 0.1000

## Promotion gates

| Gate | Status |
| --- | --- |
| performance | PASS |
| beats_production | PASS |
| deepchecks | PASS |
| fairness | PASS |

## Known limitations & identified biases

- Trained on synthetic data; real-world performance may differ.
- Fairness is measured on `gender` only; other sensitive dimensions (e.g. age bands) are not audited in this version.
- Small residual demographic parity difference exists and is monitored.
