# Attest — Model Risk & AI Compliance Platform for Regulated Credit Decisioning

> **Target product name: Attest** — an evidence-generating model governance layer for regulated credit decisioning.
>
> This document is the enterprise rewrite of the original "MLOps Skills Showcase" spec.
> The tool list barely changes. The *reason each tool exists* changes completely, and that
> is what makes this an enterprise platform instead of a portfolio piece: every component
> is justified by *"this satisfies a requirement someone is legally or financially
> accountable for"* rather than *"this demonstrates a skill."*
>
> **Scope remains 100% MLOps** (data/model lifecycle, feature store, tuning, explainability,
> fairness, serving, monitoring, champion/challenger). **Excluded**: Kubernetes,
> Terraform/Ansible, secrets management (Vault), security scanning (bandit/trivy),
> generic infra monitoring (Prometheus/Grafana) — DevOps/DevSecOps topics, not MLOps.

---

## Table of contents

1. [Overview: from skills showcase to compliance product](#1-overview-from-skills-showcase-to-compliance-product)
2. [The enterprise problem](#2-the-enterprise-problem)
3. [Who pays, and how much](#3-who-pays-and-how-much)
4. [Target use case: consumer credit decisioning](#4-target-use-case-consumer-credit-decisioning)
5. [What changes versus the original spec](#5-what-changes-versus-the-original-spec)
6. [Model choice, revised](#6-model-choice-revised)
7. [Architecture, revised](#7-architecture-revised)
8. [Enterprise components in depth](#8-enterprise-components-in-depth)
9. [The Evidence Pack](#9-the-evidence-pack)
10. [Scope statement](#10-scope-statement)
11. [Repository structure](#11-repository-structure)
12. [Data ingestion & management](#12-data-ingestion--management)
13. [Input data contracts (Great Expectations)](#13-input-data-contracts-great-expectations)
14. [Regulatory data versioning (DVC)](#14-regulatory-data-versioning-dvc)
15. [Feature engineering & Feature Store (Feast)](#15-feature-engineering--feature-store-feast)
16. [ML-native orchestration (ZenML / Metaflow — pick one)](#16-ml-native-orchestration-zenml--metaflow--pick-one)
17. [Experimentation & system of record (MLflow)](#17-experimentation--system-of-record-mlflow)
18. [Hyperparameter optimisation (Optuna)](#18-hyperparameter-optimisation-optuna)
19. [AutoML — cut, with documented reasoning](#19-automl--cut-with-documented-reasoning)
20. [Model Registry & promotion lifecycle](#20-model-registry--promotion-lifecycle)
21. [Automated model validation (Deepchecks)](#21-automated-model-validation-deepchecks)
22. [Explainability (SHAP) & reason-code pipeline](#22-explainability-shap--reason-code-pipeline)
23. [Fairness as a control (Fairlearn, tiered gate)](#23-fairness-as-a-control-fairlearn-tiered-gate)
24. [Packaging — ONNX deferred, with documented reasoning](#24-packaging--onnx-deferred-with-documented-reasoning)
25. [Decision service (BentoML)](#25-decision-service-bentoml)
26. [Post-market monitoring (Evidently)](#26-post-market-monitoring-evidently)
27. [Controlled model change management (Champion/Challenger)](#27-controlled-model-change-management-championchallenger)
28. [Regulator-facing Model Cards](#28-regulator-facing-model-cards)
29. [Drift-triggered retraining loop](#29-drift-triggered-retraining-loop)
30. [Test pyramid & enterprise test guarantees](#30-test-pyramid--enterprise-test-guarantees)
31. [Success metrics that a buyer recognises](#31-success-metrics-that-a-buyer-recognises)
32. [Implementation plan, revised](#32-implementation-plan-revised)
33. [Definition of Done](#33-definition-of-done)
34. [Honest risks](#34-honest-risks)
35. [Glossary](#35-glossary)

---

## 1. Overview: from skills showcase to compliance product

### 1.1 Why this project needed a business anchor

The original spec was technically excellent and unusually deep: Feast, Optuna, Deepchecks,
SHAP, Fairlearn, ONNX, BentoML, Evidently, champion/challenger, Model Cards, and a
drift-triggered retraining loop. Its one structural weakness: every component was justified
by *"this demonstrates a skill"* rather than *"this satisfies a requirement someone is
legally or financially accountable for."* That distinction is the whole difference between
a demo and a product.

The good news: the exact tools chosen are the tools a regulated lender needs. The fairness
suite, the explainability layer, the model cards, and the promotion gates are not optional
extras in credit — **they are the deliverable**. So the upgrade is not a rewrite, it is a
reframing plus four new components (see [§5](#5-what-changes-versus-the-original-spec)
and [§8](#8-enterprise-components-in-depth)).

### 1.2 What Attest is

Attest turns the model-validation document into a **build artifact**. Today a model
validation team writes a 60-page Word document per model, per year. It takes 6-10 weeks,
it is stale the moment the model is retrained, and it silently blocks the data science team
from shipping — because every retrain restarts the paperwork.

**Attest: evidence is generated by the pipeline, versioned with the model, and regenerated
automatically on every promotion.** The evidence pack is always current.

### 1.3 What differentiates this project

| Portfolio MLOps project | Attest |
|---|---|
| One model trained once | Candidate ladder (logistic baseline → monotonic GBM → research ensemble) compared via automated tuning |
| No feature store | Feature store (Feast) with online/offline views; point-in-time correctness prevents target leakage |
| Simple tracking | Tracking + Registry + Model Cards + Evidence Pack, linked decision → model → data |
| Fairness as a check | Fairness as a **tiered control** (green/amber/red) with recorded sign-off and protected-attribute isolation |
| Explainability as a report | SHAP values compiled into **adverse-action reason codes** sent to declined applicants |
| Every decision unlogged | Append-only **Decision Ledger** with hash chaining and replay verification |
| Deployment frozen at promotion | Champion/Challenger with shadow-mode-first rollout and documented rollback |
| Monitoring generic or absent | ML-specific monitoring (data/concept/prediction drift) + vintage backtesting, per AI Act Art. 72 |
| "Impossible" to explain why | "Right to explanation" answered end-to-end in < 5 seconds |

---

## 2. The enterprise problem

**Consumer credit decisioning under the EU AI Act and existing banking model-risk rules.**

Automated credit scoring is explicitly classified as a **high-risk AI system** under
Annex III of the EU AI Act. In the US, the equivalent pressure comes from **ECOA/Regulation B
adverse action notices** and **SR 11-7** model risk management guidance. In both regimes a
lender that uses a model to decline an applicant must be able to produce, on demand:

1. A specific, human-readable reason the individual applicant was declined.
2. Evidence that the model was tested for discriminatory impact across protected classes.
3. A record of which exact model version made the decision, trained on which exact data.
4. Proof that a human can review and override the decision.
5. Documentation of the model's intended purpose, limits, and known failure modes.
6. Continuous monitoring evidence that the model still behaves as validated.

Today, most lenders produce this by hand: a 60-page Word document per model, per year,
6-10 weeks of validation work, stale the moment the model is retrained, and every retrain
restarts the paperwork.

---

## 3. Who pays, and how much

| Buyer | Their pain | Willingness to pay |
|---|---|---|
| Chief Risk Officer / Model Risk Management | Regulatory exam findings, remediation orders | High — a single adverse exam finding costs more than the platform |
| Head of Data Science | Cannot ship; 6-week validation queue per model | High — this is their throughput ceiling |
| Compliance / Legal | Cannot answer "why was this person declined?" within the statutory window | High |
| Internal Audit | No reproducible trail from decision back to training data | Medium-high |

Concrete economics for a mid-size lender running 8 credit models:

- Model validation cost today: roughly 6 weeks of a 3-person validation team per model
  per year. At a fully loaded €120k/year per validator, that is ~€41k per model per year,
  so ~€330k/year across the portfolio.
- Time-to-production for a retrained model: 6-10 weeks. Every week of delay on a model
  that improves approval rate by even 1 point on a €200M annual origination book is
  meaningful revenue left on the table.
- Regulatory downside: EU AI Act penalties for non-compliance with high-risk obligations
  reach up to **€15M or 3% of global turnover**.

**The pitch is not "we do MLOps." The pitch is: "Your model validation cycle goes from six
weeks to one pipeline run, and the evidence pack is always current."**

---

## 4. Target use case: consumer credit decisioning

The demo implementation uses a **synthetic credit-application dataset** (the repository's
bundled synthetic data generator; sensitive attributes simulated: gender, age band). The
platform's purpose, components, and evidence artifacts are built for credit decisioning;
nothing about the design is generic.

- **Use case**: automated accept/decline scoring of consumer credit applications.
- **Outcome of each decision**: score → policy rules → outcome → SHAP → reason codes →
  ledger record → (if needed) human override.
- **High-risk obligations triggered**: EU AI Act Annex III high-risk system requirements
  (Art. 9 risk management, Art. 10 data governance, Art. 11 technical documentation,
  Art. 14 human oversight, Art. 22 right to contest automated decisions), ECOA/Reg B
  adverse action notices (US), SR 11-7 model risk management (US).

### 4.1 Evidence a lender must produce on demand

Every requirement above maps to a specific component of this platform:

| # | Evidence required | Produced by |
|---|---|---|
| 1 | Specific, human-readable decline reason | Reason Code Engine ([§8.2](#82-reason-code-engine)) |
| 2 | Discriminatory-impact testing | Fairness gate ([§8.3](#83-fairness-gate-with-tiered-severity)) |
| 3 | Which model version, trained on which data | Decision Ledger + DVC/MLflow lineage ([§8.1](#81-decision-ledger)) |
| 4 | Human review & override capability | Human Oversight Console ([§8.4](#84-human-oversight-console)) |
| 5 | Purpose, limits, failure modes | Model Card in the Evidence Pack ([§9](#9-the-evidence-pack)) |
| 6 | Continuous monitoring evidence | Evidently + vintage backtesting ([§26](#26-post-market-monitoring-evidently)) |

---

## 5. What changes versus the original spec

### 5.1 Kept — unchanged in tooling, re-scoped in purpose

| Component | Original justification | Enterprise justification |
|---|---|---|
| Great Expectations | "data quality skill" | Input data contract — a failed expectation blocks promotion and is logged as a control failure |
| DVC | "data versioning skill" | Regulatory reproducibility — auditor asks "rebuild the model that declined this applicant in March"; you can |
| Feast | "feature store skill" | Point-in-time correctness prevents target leakage, which is a *findable* model-risk defect, not just an accuracy problem |
| MLflow Registry | "registry skill" | System of record linking decision → model version → training run → dataset hash → Git commit |
| Deepchecks | "model testing skill" | Automated model validation suite; replaces manual validation checklist items |
| Fairlearn | "fairness skill" | **Core deliverable.** Disparate impact testing is legally required, not nice-to-have |
| SHAP | "explainability skill" | **Core deliverable.** Generates the adverse action reason codes sent to the declined applicant |
| Model Cards | "documentation skill" | The regulator-facing model documentation, auto-generated per version |
| Evidently | "drift monitoring skill" | Ongoing monitoring evidence required by SR 11-7 / AI Act Art. 72 post-market monitoring |
| Champion/Challenger | "A/B skill" | Controlled model change management with a documented rollback path |

### 5.2 New components required to make it real

These four additions are what convert the project from "very good MLOps" to "sellable":

| New component | One-line role |
|---|---|
| **Decision Ledger** ([§8.1](#81-decision-ledger)) | Append-only, hash-chained record of every production decision; the product's moat |
| **Reason Code Engine** ([§8.2](#82-reason-code-engine)) | Turns SHAP contributions into regulator-acceptable adverse-action reason codes |
| **Fairness Gate with tiered severity** ([§8.3](#83-fairness-gate-with-tiered-severity)) | A real control with defined thresholds and an escalation path |
| **Human Oversight Console** ([§8.4](#84-human-oversight-console)) | AI Act Art. 14 human oversight + override analytics |

### 5.3 Components cut or deferred

| Original component | Verdict | Reason |
|---|---|---|
| AutoML (AutoGluon/FLAML) | **Cut** | Unexplainable ensembles are effectively unusable in regulated credit. The validation burden exceeds the accuracy gain |
| ONNX export | **Defer** | Justified by latency or cross-runtime portability. Credit decisioning is not latency-bound at the millisecond level; adds a conversion-fidelity risk you must then test for. Reintroduce only if serving moves to a non-Python runtime |
| ZenML | **Keep, but pick one** | ZenML or Metaflow, decided once and documented. Do not leave the choice open in a spec meant to be executed |
| LIME | **Cut** | SHAP alone is sufficient and defensible; maintaining two explainers means reconciling disagreements between them, which is work with no regulatory upside |

Cutting is a signal of seniority. A spec that includes every tool reads as inexperienced;
a spec that explicitly rejects tools with stated reasoning reads as someone who has shipped.

---

## 6. Model choice, revised

Random forest / gradient boosting remain reasonable, but the enterprise version needs an
explicit **model complexity ladder** because regulated lenders often cannot deploy the most
accurate model:

| Tier | Model | Use |
|---|---|---|
| Baseline | Logistic regression with WoE-binned features | The scorecard the risk team already trusts; the benchmark every challenger must beat |
| Production | Gradient-boosted trees with monotonic constraints | Monotonic constraints on features like income and delinquency count are essential — they guarantee "more income never lowers your score," which is both intuitively correct and a defence against nonsensical explanations |
| Research | Unconstrained ensemble | Measured, documented, but shipped only with explicit MRM approval |

**Monotonicity constraints are the single highest-value technical detail in this section.**
`xgboost` and `lightgbm` both support them directly (`monotone_constraints`). They cost a
small amount of AUC and buy an enormous amount of explainability defensibility. Example:

```python
import lightgbm as lgb

# positive: feature 0 (income) and feature 3 (delinquency count) must move the score
# monotonically up / down; -1 inverts the direction.
params = {
    "objective": "binary",
    "monotone_constraints": [1, 0, 0, -1, 0],  # [income, ... , delinquency_count, ...]
    "monotone_constraints_method": "advanced",
}
model = lgb.train(params, lgb.Dataset(X_train, y_train))
```

An automated test asserts the monotonicity contract holds on the test set (a strictly
increasing score for increasing income), and the violation check is part of the Deepchecks
suite ([§21](#21-automated-model-validation-deepchecks)).

---

## 7. Architecture, revised

```
                       ┌────────────────────────────────────────┐
                       │        Loan Origination System          │
                       │        (system of engagement)           │
                       └───────────────┬────────────────────────┘
                                       │ scoring request
                       ┌───────────────▼────────────────────────┐
                       │      Decision Service (BentoML)         │
                       │  ┌──────────────────────────────────┐   │
   Feast online  ──────┼─▶│ features → model → score          │   │
   store              │  │ → policy rules → outcome          │   │
                       │  │ → SHAP → reason codes            │   │
                       │  └──────────────┬───────────────────┘   │
                       └─────────────────┼───────────────────────┘
                                         │ every decision
                       ┌─────────────────▼───────────────────────┐
                       │      DECISION LEDGER (append-only)      │
                       │  hash-chained · 7-year retention        │
                       └──┬──────────────┬─────────────────┬─────┘
                          │              │                 │
              ┌───────────▼──┐  ┌────────▼────────┐  ┌────▼──────────────┐
              │ Evidently    │  │ Human Oversight │  │ Audit / Regulator │
              │ drift + perf │  │ Console         │  │ export API        │
              └───────┬──────┘  └─────────────────┘  └───────────────────┘
                      │ drift breach or scheduled review
              ┌───────▼─────────────────────────────────────────┐
              │  Retraining pipeline (ZenML)                     │
              │  GE → DVC → Feast → train → Optuna → Deepchecks  │
              │  → Fairlearn gate → SHAP → Model Card → Registry │
              └───────┬─────────────────────────────────────────┘
                      │ Staging, never auto-Production
              ┌───────▼──────────────────────────────────────────┐
              │  Evidence Pack generated + MRM approval required  │
              └──────────────────────────────────────────────────┘
```

**The one architectural rule that defines the product: no model reaches Production without
a generated evidence pack and a recorded human approval.** Automatic promotion to Staging
is fine and desirable. Automatic promotion to Production is exactly what regulators prohibit.

---

## 8. Enterprise components in depth

### 8.1 Decision Ledger (the single most important addition)

An append-only, immutable store where every production decision is written:

```
decision_id, timestamp, applicant_pseudonymous_id, model_name, model_version,
feature_vector_hash, feature_snapshot_ref, raw_score, threshold_applied, outcome,
top_5_shap_contributions, adverse_action_codes, policy_rules_fired,
human_override (bool), override_reason, override_user_id
```

Requirements that make it enterprise-grade rather than "a Postgres table":

- **Write-once.** Postgres with an append-only trigger and no UPDATE/DELETE grants for the
  application role, or a ledger database. Every row is hash-chained to the previous row so
  tampering is detectable.
- **Retention aligned to statute.** Credit decision records are typically retained 5-7 years
  depending on jurisdiction. Design for cold storage tiering from day one.
- **Queryable by applicant.** "Show me every decision about this person" must return in
  seconds, because GDPR Art. 15 gives you 30 days and Art. 22 gives the applicant a right
  to contest automated decisions.
- **Reproducible.** Given a `decision_id`, a single command re-runs that exact model version
  against that exact stored feature vector and asserts the score matches to floating-point
  tolerance. If it does not match, that is a **P1 incident** — your production system is not
  the system you validated.

```python
def replay_decision(decision_id: str, tolerance: float = 1e-6) -> dict:
    """Re-run the exact model version against the stored feature vector."""
    row = ledger_store.get(decision_id)                       # ledger record
    model = registry.load(row.model_name, row.model_version)  # MLflow registry
    feature_vector = feature_snapshot.load(row.feature_snapshot_ref)
    score = model.predict_proba(feature_vector)[0, 1]
    assert abs(score - row.raw_score) <= tolerance, (
        f"P1: replay mismatch on {decision_id}"
    )
    return {"score": score, "ledger": row.raw_score, "match": True}
```

This one component is the product's moat. Every other tool in the stack already exists as
open source; the ledger is what a bank cannot easily assemble itself.

### 8.2 Reason Code Engine

SHAP values are not regulator-acceptable output. "Feature `f_tenure_bucket_3` contributed
-0.34" is meaningless to a declined applicant and fails the "specific and principal reason"
standard.

Build a mapping layer:

```
SHAP contribution → feature group → human-readable reason template → ranked reason codes
```

Example transformation:

| SHAP output | Delivered reason |
|---|---|
| `credit_utilisation_ratio: -0.41` | "Your balances are high relative to your available credit limits." |
| `months_since_delinquency: -0.28` | "There is a recent missed payment on your credit file." |
| `income_verification_flag: -0.19` | "We could not verify the income you reported." |

Rules for correctness:

- Reasons are ranked by absolute SHAP magnitude, **top 4 returned** (US ECOA convention).
- The mapping table is **versioned alongside the model** — a retrained model with new
  features must ship an updated mapping or promotion fails.
- A test asserts every feature in the model has a mapping entry. **No orphan features.**
- Reasons must be *actionable* — never surface a proxy feature the applicant cannot change,
  and never surface anything that leaks a protected characteristic.

```python
def adverse_action_codes(shap_values: dict[str, float], mapping: ReasonMapping, top_n: int = 4) -> list[str]:
    ranked = sorted(shap_values.items(), key=lambda kv: -abs(kv[1]))
    return [mapping.feature_to_code(feature) for feature, _ in ranked[:top_n]
            if mapping.is_actionable(feature) and mapping.is_safe(feature)]
```

### 8.3 Fairness Gate with tiered severity

A hard binary gate will either be too loose to matter or so tight that nothing ever ships.
Make fairness a real control with defined thresholds and an escalation path:

| Metric | Green | Amber (requires documented sign-off) | Red (promotion blocked) |
|---|---|---|---|
| Demographic parity ratio | ≥ 0.90 | 0.80 – 0.90 | < 0.80 |
| Equalised odds difference | ≤ 0.05 | 0.05 – 0.10 | > 0.10 |
| Approval-rate gap vs. reference group | ≤ 3 pts | 3 – 8 pts | > 8 pts |

The **0.80 red line intentionally mirrors the "four-fifths rule,"** the long-standing US
adverse-impact heuristic, which gives the threshold external defensibility rather than being
a number you invented.

Critical design detail: **protected attributes are used for testing only, never as model
features.** The pipeline reads them from a separately access-controlled table, computes
fairness metrics, and the training feature set provably excludes them. Enforce this with a
test that fails if any protected column appears in the feature schema:

```python
PROTECTED_COLUMNS = {"gender", "age_band"}

def test_protected_attributes_excluded_from_feature_schema():
    schema = feast_store.get_training_feature_names()
    assert not PROTECTED_COLUMNS & set(schema), (
        "Protected attribute leaked into the training feature set"
    )
```

Amber results do not silently pass. They open a **sign-off record in the ledger**, naming
the approver, with the mitigation rationale attached to the model version.

### 8.4 Human Oversight Console

The AI Act requires meaningful human oversight of high-risk systems. A queue interface
where a credit officer sees:

- The application, the score, the decision, and the ranked reasons.
- The SHAP waterfall for that individual decision.
- Comparable historical cases and how they were decided.
- Override buttons that require a **typed justification**.

Every override writes to the ledger. Overrides are then analysed as their own signal:
a sustained rise in override rate for a segment is early evidence the model is degrading in
a way drift metrics have not yet caught, because humans notice a shift before a KS statistic
crosses its threshold.

```python
# Override-rate monitoring: an early-warning signal drift metrics often miss.
def override_alert(window: pd.DataFrame, threshold: float = 0.15) -> bool:
    return window["human_override"].mean() > threshold  # segment-level
```

---

## 9. The Evidence Pack

The deliverable artifact. Generated on every promotion, versioned, immutable:

```
evidence/{model_name}/{version}/
├── model_card.md                  # purpose, limits, intended use, out-of-scope use
├── data_lineage.json              # DVC hashes, Feast feature views, date ranges
├── training_report.html           # hyperparameters, Optuna search space + trials
├── performance.json               # AUC, KS, Gini, PSI, by segment and overall
├── fairness_report.html           # Fairlearn metrics, all protected groups, gate result
├── explainability_report.html     # global SHAP, per-decile SHAP, feature interactions
├── stability_report.html          # PSI vs. development sample, backtest by vintage
├── deepchecks_suite.html          # data + model validation suite results
├── reason_code_mapping.csv        # feature → reason text, with coverage assertion
├── approvals.json                 # who approved, when, on what basis
└── manifest.json                  # SHA-256 of every file above, signed
```

Two notes on realism:

- **Gini, KS, and PSI are the metrics credit risk teams actually use.** Presenting only AUC
  and F1 marks the project as coming from a general ML background rather than a credit
  background.
- **Backtesting by vintage** — measuring performance on applications from each origination
  month separately — is standard credit practice, because performance on a blended test set
  can hide sharp degradation in recent cohorts.

---

## 10. Scope statement

| MLOps capability | Tool(s) | Status in this project |
|---|---|---|
| Data versioning | DVC | ✅ Included |
| Data quality validation | Great Expectations | ✅ Included |
| Feature engineering | pandas / scikit-learn pipelines | ✅ Included |
| Feature store (online + offline) | Feast | ✅ Included |
| ML-native pipeline orchestration | ZenML (or Metaflow — pick one) | ✅ Included |
| Experiment tracking | MLflow | ✅ Included |
| Hyperparameter optimisation | Optuna | ✅ Included |
| AutoML comparative | AutoGluon / FLAML | ❌ Cut (see [§19](#19-automl--cut-with-documented-reasoning)) |
| Model registry | MLflow Registry | ✅ Included |
| Automated model tests | Deepchecks | ✅ Included |
| Explainability global/local | SHAP | ✅ Included (LIME cut) |
| Bias detection / fairness | Fairlearn (tiered gate) | ✅ Included — core deliverable |
| Portable packaging | ONNX | ⏸ Deferred (see [§24](#24-packaging--onnx-deferred-with-documented-reasoning)) |
| ML-native serving | BentoML | ✅ Included |
| Drift monitoring (data/concept/prediction) | Evidently + PSI/vintage backtesting | ✅ Included |
| Champion/Challenger, model A/B | Custom logic + MLflow | ✅ Included (shadow-mode-first) |
| Model documentation | Model Cards | ✅ Included — regulator-facing |
| Drift-triggered retraining | Python script + condition (ZenML) | ✅ Included — Staging-only |
| Decision ledger | Append-only hash-chained store | ✅ Included — new |
| Reason code engine | SHAP → mapping layer | ✅ Included — new |
| Human oversight | Oversight console + override analytics | ✅ Included — new |
| Unit/integration tests | pytest | ✅ Included |
| ~~Kubernetes~~ | — | ❌ Excluded (DevOps) |
| ~~Terraform / Ansible~~ | — | ❌ Excluded (DevOps) |
| ~~Vault / secrets management~~ | — | ❌ Excluded (DevSecOps) |
| ~~Security scanning (bandit/trivy)~~ | — | ❌ Excluded (DevSecOps) |
| ~~Prometheus/Grafana infra~~ | — | ❌ Excluded (DevOps, replaced by ML monitoring) |

> Docker is kept to the strict minimum (packaging the BentoML serving service), as it is an
> unavoidable standard for delivering a model — but no container orchestration is covered here.

---

## 11. Repository structure

```
mlops-full-project/
│
├── data/
│   ├── raw/                      # immutable raw data (dataset.csv + generator)
│   ├── processed/                # cleaned data
│   ├── reference/                # reference dataset for drift detection
│   └── features/                 # engineered features (parquet)
│
├── great_expectations/
│   └── expectations/
│       └── dataset_suite.json    # the input data contract
│
├── feature_repo/                 # Feast repository
│   ├── feature_store.yaml
│   ├── entities.py
│   ├── features.py
│   └── data_sources.py
│
├── pipelines/                    # ZenML pipelines
│   ├── training_pipeline.py
│   ├── tuning_pipeline.py
│   └── retraining_pipeline.py
│
├── src/
│   ├── data/
│   │   ├── ingestion.py          # logs row count, time period, source hash
│   │   └── preprocessing.py      # pure functions
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py              # MLflow tracking, monotonic constraints
│   │   ├── tune.py               # Optuna bayesian search
│   │   ├── evaluate.py           # AUC, KS, Gini, PSI, vintage backtest
│   │   ├── explain.py            # SHAP
│   │   ├── fairness_check.py     # Fairlearn, tiered gate
│   │   ├── reason_codes.py       # reason code mapping + coverage assertion
│   │   ├── evidence_pack.py      # evidence pack generator + signed manifest
│   │   └── promote.py            # promotion gates incl. approval record
│   ├── ledger/
│   │   ├── schema.sql            # append-only, hash-chained
│   │   ├── writer.py             # ledger writer (write-once)
│   │   └── replay.py             # decision replay + P1 mismatch detection
│   ├── serving/
│   │   ├── bento_service.py      # BentoML /predict + /explain + ledger write
│   │   └── champion_challenger.py
│   ├── oversight/
│   │   └── console.py            # human oversight queue + override analytics
│   └── monitoring/
│       ├── drift_report.py       # Evidently
│       └── retraining_trigger.py
│
├── model_cards/
│   └── model_card_template.py    # auto-generated from MLflow + Fairlearn
│
├── evidence/                     # generated Evidence Packs per model/version
│
├── tests/
│   ├── unit/
│   │   ├── test_preprocessing.py
│   │   ├── test_features.py
│   │   ├── test_fairness.py      # incl. protected-attribute isolation
│   │   ├── test_reason_codes.py  # coverage assertion
│   │   ├── test_ledger.py        # hash-chain + replay
│   │   └── test_monotonicity.py
│   ├── model/
│   │   └── test_model_quality.py # Deepchecks
│   └── data/
│       └── test_data_validation.py  # Great Expectations
│
├── notebooks/
│   └── exploration.ipynb
│
├── mlflow/
│   └── mlruns/
│
├── dvc.yaml
├── requirements.txt
├── pyproject.toml
├── Dockerfile.bento              # minimal packaging of the serving service
└── README.md
```

---

## 12. Data ingestion & management

### 12.1 Role

Retrieve raw data (local file, public API, or simulated base) and prepare it for the rest
of the pipeline. In the demo, the bundled generator produces the synthetic credit dataset.

### 12.2 Good practices

- Strict separation of `raw/` (never modified) vs `processed/` (generated).
- Every transformation is a pure function, independently testable.
- The ingestion script logs the number of rows, the covered period, and a hash of the
  source file — the first link in the audit chain from decision back to training data.

---

## 13. Input data contracts (Great Expectations)

### 13.1 Role

Guarantee that no corrupted or out-of-norm data enters the training pipeline — **before**
feature engineering. The expectation suite is an **input data contract**: a failed
expectation blocks promotion and is logged as a control failure (enterprise justification),
not merely a data-quality exercise.

### 13.2 Examples of defined expectations

- No null values on critical columns
- Expected value range for each numeric variable (e.g. age between 18 and 100)
- Consistent column types
- Minimum expected row volume

### 13.3 Integration

This control is the **first step of every pipeline** (`training_pipeline`,
`retraining_pipeline`) — if validation fails, the pipeline stops before wasting compute on
a useless training run.

---

## 14. Regulatory data versioning (DVC)

### 14.1 Role

Ensure exact reproducibility: which dataset produced which model. Enterprise justification:
an auditor asks "rebuild the model that declined this applicant in March" — you can, byte
for byte, because the data is versioned and linked to the run.

### 14.2 DVC pipeline

```yaml
stages:
  validate:
    cmd: python src/data/ingestion.py && great_expectations checkpoint run dataset_checkpoint
    outs: [data/raw/dataset.csv]

  preprocess:
    cmd: python src/data/preprocessing.py
    deps: [data/raw/dataset.csv]
    outs: [data/processed/dataset_clean.csv]

  build_features:
    cmd: python src/features/build_features.py
    deps: [data/processed/dataset_clean.csv]
    outs: [data/features/features.parquet]
```

Every data hash flows into the MLflow run tags ([§17](#17-experimentation--system-of-record-mlflow))
and the Evidence Pack's `data_lineage.json`.

---

## 15. Feature engineering & Feature Store (Feast)

### 15.1 Why a feature store here

It is one of the most specifically-MLOps components and it carries a direct risk-control
justification: it guarantees consistency between features used at training (offline) and
at inference time (online), avoiding the "training-serving skew" — and its point-in-time
correctness prevents **target leakage**, which is a *findable* model-risk defect, not just
an accuracy problem.

### 15.2 Feast components

| File | Role |
|---|---|
| `entities.py` | Defines entity keys (e.g. `customer_id`) |
| `data_sources.py` | Points to the Parquet file / offline store |
| `features.py` | Defines `FeatureView`s (feature groups with TTL) |
| `feature_store.yaml` | Store configuration (offline = local file, online = lightweight SQLite/Redis) |

### 15.3 Conceptual `FeatureView` example

```python
customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=30),
    schema=[
        Field(name="avg_transaction_amount", dtype=Float32),
        Field(name="num_transactions_30d", dtype=Int64),
    ],
    source=customer_stats_source,
)
```

### 15.4 Usage

- **Training**: `store.get_historical_features(...)` retrieves features at the correct
  timestamp (point-in-time correctness — avoids temporal data leakage).
- **Inference**: `store.get_online_features(...)` retrieves the latest values in
  milliseconds.

---

## 16. ML-native orchestration (ZenML / Metaflow — pick one)

### 16.1 Why not Airflow

Airflow is a general-purpose orchestrator (close to data engineering/DevOps). **ZenML** and
**Metaflow** are designed specifically for ML workflows: native artifact management, pipeline
versioning, and direct integration with MLflow/Feast.

### 16.2 Decision: pick one and document it

The original spec left the choice open. In an executable spec, **choose ZenML** (or
Metaflow), record the decision in the repo's architecture notes, and do not revisit it —
switching costs are real and there is no regulatory upside to keeping the choice open.

### 16.3 Role of ZenML

- Defines pipelines as decorated Python functions (`@step`, `@pipeline`).
- Automatically traces every run (artifacts, parameters, metadata).
- Integrates natively with MLflow as "Experiment Tracker" and with Evidently as
  "Data Validator".

### 16.4 Conceptual example

```python
@step
def load_data() -> pd.DataFrame: ...

@step
def validate_data(df: pd.DataFrame) -> pd.DataFrame: ...

@step
def train_model(df: pd.DataFrame) -> Model: ...

@pipeline
def training_pipeline():
    df = load_data()
    df = validate_data(df)
    model = train_model(df)
```

### 16.5 Benefit

Each `step` is cached: if the data has not changed, ZenML reuses the previous result —
a considerable iteration-time gain, and cache hits are themselves audit evidence of what
did (and did not) change between two validations.

---

## 17. Experimentation & system of record (MLflow)

### 17.1 Role

Centralise all runs (tuning, manual training, retrains) for objective comparison. Enterprise
justification: MLflow Registry is the **system of record** linking decision → model version
→ training run → dataset hash → Git commit.

### 17.2 What is logged for each run

- Full hyperparameters
- Metrics (Gini, KS, PSI, AUC, F1 — credit metrics first, see [§9](#9-the-evidence-pack))
- Artifacts: model, confusion matrix, ROC curve, SHAP report, fairness report
- Tags: data source (DVC hash), ZenML pipeline version, monotonicity flag, reason-code
  mapping version

### 17.3 Run comparison

The MLflow UI sorts all runs (manual + Optuna) on a parallel-coordinates chart — useful to
visualise the effect of each hyperparameter on the target metric.

---

## 18. Hyperparameter optimisation (Optuna)

### 18.1 Role

Automate the search for the best hyperparameter set via Bayesian search (far more efficient
than grid search).

### 18.2 Integration with MLflow

Each Optuna `trial` is logged as a child MLflow run, so the whole search is visible in the
MLflow UI.

### 18.3 Conceptual example (`tune.py`)

```python
import optuna
import mlflow

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 20),
        "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.3, log=True),
    }
    with mlflow.start_run(nested=True):
        mlflow.log_params(params)
        model = train_with_params(params)
        score = evaluate(model)
        mlflow.log_metric("gini_score", score)
    return score

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
```

---

## 19. AutoML — cut, with documented reasoning

**Verdict: cut.** Unexplainable ensembles (AutoGluon/FLAML output) are effectively unusable
in regulated credit: the validation burden exceeds the accuracy gain. Every promotion of a
black-box ensemble would require the model validation team to reverse-engineer decisions
the candidate ladder's logistic/monotonic models already explain. This is an explicit,
documented rejection — see [§5.3](#53-components-cut-or-deferred) for the full reasoning.

---

## 20. Model Registry & promotion lifecycle

### 20.1 Role

Manage versions and stages (`Staging` → `Production` → `Archived`) of the retained model
(the candidate from the complexity ladder that passes every gate).

### 20.2 Promotion criteria (`promote.py`)

A model is promoted only if it passes **all** these gates:

1. Performance ≥ minimum threshold (Gini/KS on holdout **and** by vintage, [§26](#26-post-market-monitoring-evidently))
2. Better than the current Production model on the comparison set
3. Deepchecks suite passed ([§21](#21-automated-model-validation-deepchecks))
4. Fairness gate not Red; if Amber, a **recorded sign-off** in the ledger ([§8.3](#83-fairness-gate-with-tiered-severity))
5. Reason-code mapping covers every model feature ([§8.2](#82-reason-code-engine))
6. Monotonicity contract enforced and verified ([§6](#6-model-choice-revised))
7. **Evidence Pack generated with a signed manifest** ([§9](#9-the-evidence-pack))
8. **A recorded human (MRM) approval** — automatic promotion to Production is impossible
   by construction

### 20.3 Full traceability

Each registered version is linked to: a Git commit, a DVC data hash, a complete MLflow run,
a SHAP report, a fairness report, a reason-code mapping version, and its evidence pack —
end-to-end traceability from decision back to training data.

---

## 21. Automated model validation (Deepchecks)

### 21.1 Role

Go beyond a single performance metric: Deepchecks runs a suite of automated checks on the
data AND the model — replacing manual validation checklist items (enterprise justification).

### 21.2 Types of checks included

| Category | Example checks |
|---|---|
| Data integrity | Duplicates, missing values, inconsistent types |
| Train/test distribution | Verifies the split is representative |
| Model performance | Comparison to a naive baseline |
| Robustness | Sensitivity to light feature noise |
| Overfitting | Train vs test performance gap |
| Monotonicity | Constraint contract holds on the test set |

### 21.3 Integration

```python
from deepchecks.tabular.suites import full_suite

suite = full_suite()
result = suite.run(train_dataset, test_dataset, model)
result.save_as_html("reports/deepchecks_suite.html")
```

The pipeline blocks promotion if the Deepchecks suite contains a critical failure, and the
HTML report is embedded in the Evidence Pack.

---

## 22. Explainability (SHAP) & reason-code pipeline

### 22.1 Role

Understand **why** the model made each decision — in regulated credit, an explicit
regulatory requirement, not a trust nicety.

### 22.2 SHAP (global and local)

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Global feature importance
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("reports/shap_summary.png")

# Individual decision explanation (feeds the Human Oversight Console waterfall)
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### 22.3 From SHAP to reason codes

SHAP values are the input to the Reason Code Engine ([§8.2](#82-reason-code-engine)) which
translates them into the adverse-action codes delivered to declined applicants. Per-decision
SHAP is also stored in the Decision Ledger (`top_5_shap_contributions`) and rendered as a
waterfall in the Human Oversight Console.

### 22.4 LIME — cut, with documented reasoning

SHAP alone is sufficient and defensible; maintaining two explainers means reconciling
disagreements between them, which is work with no regulatory upside. See
[§5.3](#53-components-cut-or-deferred).

---

## 23. Fairness as a control (Fairlearn, tiered gate)

### 23.1 Role

Verify the model does not systematically discriminate against a subgroup (e.g. gender, age
band), even when the variable is not used directly as a feature (indirect bias via
correlated variables). This is the **core deliverable**: disparate-impact testing is legally
required, not nice-to-have.

### 23.2 Metrics computed

| Metric | What it measures |
|---|---|
| Demographic Parity Difference / Ratio | Gap in positive-prediction rates between groups |
| Equalized Odds Difference | Gap in true/false positive rates between groups |
| Selection rate per group | Approval rate per sub-population |

### 23.3 Conceptual example (`fairness_check.py`)

```python
from fairlearn.metrics import MetricFrame, demographic_parity_difference

metric_frame = MetricFrame(
    metrics={"accuracy": accuracy_score, "selection_rate": selection_rate},
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=X_test["gender"]
)

dp_ratio = metric_frame.ratio()  # tiered gate, see below
```

### 23.4 Tiered gate and escalation

Results are classified **Green / Amber / Red** against the thresholds in
[§8.3](#83-fairness-gate-with-tiered-severity):

- **Green** → proceeds.
- **Amber** → promotion requires a documented sign-off record in the ledger, naming the
  approver and the mitigation rationale.
- **Red** → promotion blocked, regardless of overall performance — **performance alone is
  not sufficient**.

Protected attributes are read from a separately access-controlled table, used for testing
only, and provably absent from the training feature set (enforced by the isolation test in
[§8.3](#83-fairness-gate-with-tiered-severity)).

---

## 24. Packaging — ONNX deferred, with documented reasoning

**Verdict: deferred.** ONNX is justified by latency or cross-runtime portability. Credit
decisioning is not latency-bound at the millisecond level, and ONNX adds a
conversion-fidelity risk you must then test for. Reintroduce only if serving moves to a
non-Python runtime. See [§5.3](#53-components-cut-or-deferred).

If reintroduced, the original parity requirement is kept: a test compares the original and
ONNX model predictions on the same test set within a defined numeric tolerance.

---

## 25. Decision service (BentoML)

### 25.1 Why BentoML rather than FastAPI alone

BentoML is **specifically designed for ML model serving**: native model versioning, adaptive
request batching, automatic service-image generation, and direct integration with the MLflow
Registry.

### 25.2 Service definition (`bento_service.py`)

The service is not just `/predict`: every decision it makes is **written to the Decision
Ledger** with reasons, and `/explain` returns the per-decision SHAP waterfall.

```python
import bentoml
from bentoml.io import JSON

model_ref = bentoml.mlflow.get("credit_model:latest")
runner = model_ref.to_runner()

svc = bentoml.Service("attest_decision_service", runners=[runner])

@svc.api(input=JSON(), output=JSON())
def predict(input_data: dict):
    result = runner.predict.run([list(input_data.values())])
    reasons = reason_codes.for_decision(result, shap_values)
    ledger.write(decision=result, reasons=reasons, model_version="latest")
    return {"prediction": result.tolist(), "adverse_action_codes": reasons}

@svc.api(input=JSON(), output=JSON())
def explain(input_data: dict):
    # Returns the SHAP waterfall for this decision (feeds the Oversight Console)
    ...
```

### 25.3 Specific MLOps benefits

- **Adaptive batching**: automatically groups simultaneous requests to optimise inference
  throughput.
- **Native "Bento" versioning** linked directly to the MLflow model version.
- Minimal `Dockerfile.bento` generation if portable packaging is needed.

---

## 26. Post-market monitoring (Evidently)

### 26.1 Role

Monitor three types of ML-specific drift — this is the **ongoing monitoring evidence**
required by SR 11-7 and AI Act Art. 72 post-market monitoring:

| Drift type | What is monitored |
|---|---|
| **Data drift** | Input feature distribution has changed |
| **Concept drift** | The features → target relationship has changed |
| **Prediction drift** | The prediction distribution itself has changed |

### 26.2 Generated report (`drift_report.py`)

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=reference_df, current_data=production_sample_df)
report.save_html("monitoring/reports/drift_report.html")

drift_score = report.as_dict()["metrics"][0]["result"]["dataset_drift"]
```

### 26.3 Real-performance tracking & vintage backtesting

When the true label becomes available (e.g. default observed 30-90 days after the
prediction), a job compares the historical prediction to the actual outcome and recomputes
real production metrics — the most reliable verification of model health. Performance is
**backtested by vintage** (each origination month separately), not only on a blended
holdout, because a blended test set can hide sharp degradation in recent cohorts. PSI is
computed against the development sample and reported in the Evidence Pack
(`stability_report.html`).

---

## 27. Controlled model change management (Champion/Challenger)

### 27.1 Role

Never brutally replace a production model: the new model ("Challenger") first receives a
fraction of traffic alongside the current model ("Champion"). Enterprise justification:
controlled change management with a **documented rollback path**.

### 27.2 Shadow-mode-first rollout

Before any traffic is routed to the Challenger, it runs in **shadow mode** — scoring the
same requests without affecting outcomes — while its decisions (and the Champion's) are
written to the ledger for comparison. Only after the shadow comparison is reviewed does
routing begin.

### 27.3 Logic (`champion_challenger.py`)

```python
import random

def route_prediction(input_data, challenger_ratio=0.1):
    if random.random() < challenger_ratio:
        model_version = "challenger"
        prediction = challenger_model.predict(input_data)
    else:
        model_version = "champion"
        prediction = champion_model.predict(input_data)

    log_prediction(input_data, prediction, model_version)  # ledger write, not a log file
    return prediction, model_version
```

### 27.4 Comparative analysis

After a defined period (e.g. 2 weeks), statistical comparison of Champion vs Challenger
performance (significance test) before deciding full promotion. Every routed decision is in
the ledger, so the comparison is auditable.

---

## 28. Regulator-facing Model Cards

### 28.1 Role

Produce standardised documentation readable by non-experts, describing: the model's purpose,
training data, performance metrics, fairness results, and known limits — the
**regulator-facing model documentation**, auto-generated per version.

### 28.2 Typical Model Card content

- **Model details**: algorithm, version, training date
- **Intended use**: validated use cases / use cases to avoid
- **Training data**: source, period, size
- **Performance metrics**: overall and per subgroup (Gini, KS, PSI, AUC)
- **Fairness analysis**: summarised Fairlearn results with gate status (Green/Amber/Red)
- **Known limitations and identified biases** (including the SHAP-is-not-causal caveat,
  [§34](#34-honest-risks))

### 28.3 Automatic generation

`model_cards/model_card_template.py` automatically retrieves metrics from MLflow and
Fairlearn results to generate the Model Card in Markdown/HTML at every promotion — avoiding
stale documentation. The card is part of the Evidence Pack ([§9](#9-the-evidence-pack)).

---

## 29. Drift-triggered retraining loop

### 29.1 Complete sequence

```
1. drift_report.py runs periodically (cron or manual trigger)
        ↓
2. If dataset_drift == True or drift_score > threshold
        ↓
3. Retraining pipeline triggered (ZenML)
        ↓
4. New Optuna tuning on recent data
        ↓
5. New Deepchecks + Fairlearn (tiered gate) passes
        ↓
6. Comparison to current Champion (shadow mode first)
        ↓
7. If better AND equitable → promoted to Challenger (fraction of traffic)
        ↓
8. 2-week review → full promotion, Evidence Pack regenerated
```

### 29.2 Guardrails

- An automatically retrained model **never** skips the Fairlearn gate, even in an emergency.
- Automatic promotion is allowed **to Staging only**. Production requires the generated
  Evidence Pack and a **recorded human (MRM) approval** — the architectural rule in
  [§7](#7-architecture-revised).
- Last 3 Production versions retained for immediate rollback.
- Notification (structured log / webhook) at every promotion, keeping human supervision.

---

## 30. Test pyramid & enterprise test guarantees

### 30.1 MLOps-specific test pyramid

```
        ┌────────────────────────────────────────────┐
        │ Evidence Pack manifest + approval checks     │
        ├────────────────────────────────────────────┤
        │ Decision Ledger: hash-chain + replay tests   │  (P1 mismatch detection)
        ├────────────────────────────────────────────┤
        │ Reason-code coverage + monotonicity tests    │
        ├────────────────────────────────────────────┤
        │ Protected-attribute isolation test           │  (schema-level)
        ├────────────────────────────────────────────┤
        │ Fairness gate tests                          │  (Fairlearn, tiered)
        ├────────────────────────────────────────────┤
        │ Model quality tests                          │  (Deepchecks)
        ├────────────────────────────────────────────┤
        │ Data quality tests                           │  (Great Expectations)
        ├────────────────────────────────────────────┤
        │ Classic unit tests                           │  (pytest)
        └────────────────────────────────────────────┘
```

### 30.2 Enterprise test guarantees

| Guarantee | Test |
|---|---|
| Tamper-proof ledger | Hash-chain verification test — deleting/editing any row breaks the chain |
| Reproducible decisions | Replay test — re-runs exact model version on stored feature vector, asserts score within tolerance |
| No orphan features | Coverage test — every model feature has a reason-code mapping entry |
| No protected leakage | Isolation test — fails if any protected column appears in the feature schema |
| Monotonicity respected | Contract test — score is non-decreasing in income, non-increasing in delinquency |
| No automatic production promotion | Pipeline test — Production transition requires evidence pack + approval record |

### 30.3 Example: explainability non-regression

```python
def test_shap_top_feature_stable():
    """Verifies the most important feature stays consistent across model versions
    (detects a suspicious behaviour change)."""
    shap_values = compute_shap(model, X_sample)
    top_feature = get_top_feature(shap_values)
    assert top_feature in EXPECTED_TOP_FEATURES
```

---

## 31. Success metrics that a buyer recognises

| Metric | Baseline (manual) | Target with Attest |
|---|---|---|
| Model validation cycle time | 6-10 weeks | < 1 day (pipeline run + review) |
| Time to answer "why was applicant X declined?" | 2-5 business days | < 5 seconds |
| Evidence pack freshness | Annual, stale between refreshes | Current with every deployed version |
| Reproducibility of any historical decision | Best-effort, frequently fails | 100%, asserted by automated test |
| Models in production per data scientist per year | 1-2 | 6-8 |
| Audit findings related to model documentation | Recurring | Zero |

---

## 32. Implementation plan, revised

The original 15-day plan was ordered by tool. This plan is **ordered by risk** — build the
thing that is hard to retrofit first. The ledger is nearly impossible to add later because
you cannot retroactively create records of decisions you did not log.

| Phase | Deliverable | Days |
|---|---|---|
| 0 | Decision ledger schema, hash chaining, retention policy, replay test | 3 |
| 1 | Data contracts (GE) + DVC + Feast with point-in-time correctness test | 3 |
| 2 | Training pipeline (ZenML) + MLflow + monotonic GBM + logistic baseline | 3 |
| 3 | Deepchecks + Fairlearn tiered gate + protected-attribute isolation test | 3 |
| 4 | SHAP + Reason Code Engine + coverage assertion | 2 |
| 5 | BentoML decision service writing to the ledger, with replay verification | 2 |
| 6 | Evidence Pack generator + signed manifest | 2 |
| 7 | Evidently monitoring + PSI/vintage backtesting + drift alerting | 2 |
| 8 | Human Oversight Console + override analytics | 3 |
| 9 | Champion/Challenger with shadow-mode-first rollout | 2 |
| 10 | Regulator export API + end-to-end audit simulation | 2 |

**Total: ~27 days.** Longer than the original 15, and that is the correct trade — the extra
12 days are entirely spent on the parts that make it a product.

### 32.1 Final acceptance: mock regulatory exam

Run a **mock regulatory exam** as the final acceptance test. Have someone play the examiner
and ask, cold: "Show me the model that declined this applicant on this date, prove it was
tested for bias, and show me who approved it." If the answer takes more than five minutes,
the system is not done.

---

## 33. Definition of Done

- [ ] Every production decision is in the ledger with model version, feature hash, and reasons
- [ ] Any historical decision replays and reproduces the identical score
- [ ] Ledger tampering is detectable via hash chain verification
- [ ] Protected attributes are provably absent from the feature set, asserted by a test
- [ ] Fairness gate blocks promotion at Red and requires recorded sign-off at Amber
- [ ] Every model feature has a reason-code mapping; a missing mapping fails the build
- [ ] Monotonic constraints are enforced and violations are caught in testing
- [ ] Evidence pack generates automatically on promotion with a signed manifest
- [ ] No path exists to promote to Production without a recorded human approval
- [ ] Human overrides are logged and surfaced as a monitoring signal
- [ ] Performance is backtested by vintage, not only on a blended holdout
- [ ] "Right to explanation" request answered end-to-end in under 5 seconds
- [ ] Mock regulatory exam passed in under 5 minutes per question

---

## 34. Honest risks

**Regulatory claims are a liability.** Never claim the platform "makes you AI Act compliant."
It generates evidence that supports compliance. Compliance is a legal determination made by
the customer's counsel. Getting this wrong in marketing is how a vendor gets sued.

**Fairness metrics conflict with each other.** Demographic parity and equalised odds cannot
generally both be satisfied simultaneously — this is a proven impossibility result, not an
engineering gap. The platform must present the trade-off and record which the institution
chose and why. Any tool claiming to "fix bias" automatically is selling something false.

**SHAP is an approximation, not ground truth.** For tree ensembles TreeSHAP is exact with
respect to the model, but it explains the model, not the world. Correlated features split
credit arbitrarily between themselves. Document this in the model card rather than letting
a business user believe the reasons are causal.

**Protected attribute data is itself hazardous.** You need it to test fairness and are often
restricted from collecting it. Handle via separate access-controlled storage, a documented
lawful basis, and in some jurisdictions statistical proxy methods (BISG) instead — noting
that proxies introduce their own measurement error which must be disclosed.

**The build is not the hard part.** Selling into risk and compliance functions means long
procurement cycles, security reviews, and pilot-to-production timelines measured in quarters.
Budget for that reality.

---

## 35. Glossary

| Term | Definition |
|---|---|
| **Adverse action notice** | ECOA/Reg B requirement: a lender must tell a declined applicant the specific, principal reasons for the decision |
| **Annex III (EU AI Act)** | The list of high-risk AI systems, including credit scoring; high-risk obligations carry penalties up to €15M or 3% of global turnover |
| **Batching adaptatif (adaptive batching)** | Automatic grouping of simultaneous inference requests to optimise throughput |
| **BISG** | Bayesian Improved Surname Geocoding — a statistical proxy method used to estimate protected attributes for fairness testing when they cannot be collected |
| **Champion/Challenger** | Deployment strategy where a new model is tested in parallel with the incumbent on a fraction of traffic |
| **Concept drift** | Change in the relationship between features and the target |
| **Data drift** | Change in the distribution of production input data versus training |
| **Decision Ledger** | Append-only, hash-chained store of every production decision, with replay verification |
| **Demographic parity** | Fairness metric measuring whether positive-prediction rates are similar across subgroups |
| **Evidence Pack** | Versioned, immutable, signed bundle of all validation evidence generated at each promotion |
| **Equalised odds** | Fairness metric measuring whether true/false positive rates are similar across subgroups |
| **Four-fifths rule** | Long-standing US adverse-impact heuristic (0.80 ratio); the external anchor for this platform's Red threshold |
| **Gini / KS** | Standard credit-risk discrimination metrics (Gini = 2·AUC − 1; KS = max separation between score distributions) |
| **High-risk AI system** | EU AI Act category (Annex III) imposing risk management, data governance, documentation, human oversight and monitoring obligations |
| **Model Card** | Standardised document describing a model's characteristics, performance and limits |
| **Monotonic constraints** | Model constraint guaranteeing the score moves in a fixed direction with a feature (e.g. income) |
| **Point-in-time correctness** | Guarantee that training features reflect the state of data at the exact event time, without future information leakage |
| **PSI** | Population Stability Index — measures feature/score distribution shift versus the development sample |
| **Reason code** | Human-readable, ranked, actionable explanation delivered to a declined applicant |
| **Replay** | Re-running the exact model version on a stored feature vector and asserting score equality |
| **SR 11-7** | US supervisory guidance on model risk management (validation, monitoring, governance) |
| **Training-serving skew** | Difference between transformations applied at training and at inference; a frequent source of silent bugs |
| **TreeSHAP** | Exact (with respect to the model) SHAP computation for tree ensembles; explains the model, not the world |
| **Vintage backtesting** | Measuring performance separately on each origination month's applications, standard credit practice |
