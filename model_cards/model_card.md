# Model Card: Customer Churn Classifier (Attest demo artifact)

*Generated automatically on 2026-08-17T13:10:39.187911*

> This card is the auto-generated Evidence Pack artifact for the **demo model** bundled with
> the Attest platform (see `mlops-full-mlops-skills-project.md`). The platform's target use
> case is consumer credit decisioning; the demo model below is a churn classifier trained on
> synthetic telecom-style data. Regenerated at every promotion by
> `model_cards/model_card_template.py`.

## Model details

- Algorithm: RandomForestClassifier
- Task: Binary classification (customer churn)
- Objective: Predict churn probability to enable proactive retention

## Intended use

- Valid: churn risk scoring for telecom customers
- Avoid: credit decisions, medical predictions, or any other domain

## Training data

- Source: synthetic telecom dataset (`data/raw/dataset.csv`)
- Rows: ~7000, binary target with a sensitive attribute (`gender`)

## Performance metrics (held-out test set)

| Metric | Value |
| --- | --- |
| accuracy | 0.8994 |
| f1_score | 0.2542 |
| roc_auc | 0.5736 |

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
