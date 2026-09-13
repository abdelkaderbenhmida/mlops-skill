# Attest — Modèle de Risque & Compliance IA (README détaillé)

> Documentation complète du code source de **Attest** (répertoire
> `mlops-full-mlops-skills-project`) : description du projet, outils, fonctionnement interne
> étape par étape, et procédure de test. Complète la [README principale](./README.md) et
> la [spécification produit](./mlops-full-mlops-skills-project.md).

---

## 1. Vue d'ensemble

**Attest** est une plateforme de **gouvernance de modèle réglementée** pour la décision de
crédit. Le document de validation de modèle devient un **artefact de build** : chaque
promotion génère automatiquement un **Evidence Pack** (lignage, performance, équité,
explicabilité, stabilité, model card) signé et versionné. Chaque décision de production est
écrite dans un **Decision Ledger** append-only hash-chainé, et les contributions SHAP sont
compilées en **reason codes** (motifs de décision défavorable) acceptables par un régulateur.

**Règle d'or** : aucun modèle n'atteint la Production sans Evidence Pack généré **et**
approbation humaine enregistrée. La promotion automatique en Production est impossible.

Cas d'usage initial : churn télécom (dataset synthétique). Les composants de contrôle
(ledger, fairness gate, reason codes, evidence pack) sont agnostiques au cas d'usage.

---

## 2. Stack technique et rôle de chaque outil

| Domaine | Outil | Rôle dans Attest |
|---|---|---|
| Versioning données | **DVC** | Reproductibilité réglementaire — hash de dataset lié à chaque run (`dvc.yaml`, 3 étages) |
| Qualité des données | **Great Expectations** | Contrat de données d'entrée ; échecs logués comme défauts de contrôle |
| Feature store | **Feast** (offline + online) | Exactitude point-in-time anti fuite de cible (`feature_repo/`) |
| Orchestration | **ZenML** | Pipelines versionnés et cachables (training, tuning, retraining) |
| Tracking | **MLflow** | Système d'enregistrement : décision → modèle → run → hash données → commit |
| Tuning | **Optuna** (bayésien TPE) | Recherche auto, loguée en sous-runs MLflow |
| Registry | **MLflow Registry** | Cycle de vie Staging/Production avec enregistrements d'approbation |
| Validation modèle | **Deepchecks** | Suite de validation automatisée remplaçant les items de checklist manuels |
| Explicabilité | **SHAP** (global + local) + LIME | Entrée du Reason Code Engine |
| Équité | **Fairlearn** (gate à seuils) | **Livrable central** — Green/Amber/Red avec sign-off |
| Ledger de décision | Stockage append-only hash-chainé | Enregistrement immuable + vérification par rejeu (moat) |
| Reason codes | Couche de mapping SHAP → texte | Motifs de décision défavorable top-4 |
| Supervision humaine | Console d'oversight | Art. 14 AI Act ; overrides logués et monitorés |
| Serving | **BentoML** (predict + explain) | Écrit chaque décision dans le ledger |
| Champion/Challenger | Routeur custom + log ledger | Shadow-mode d'abord |
| Monitoring | **Evidently** (3 types de drift) + PSI | Preuve de monitoring post-marché |
| Model cards | Auto-générées (MLflow + Fairlearn) | Documentation réglementaire dans l'Evidence Pack |
| Réentraînement | Déclenché par drift (ZenML) | Promotion Staging seule ; Production = evidence + approbation |
| Automatisations cut | AutoML, LIME, ONNX, K8s/Terraform/Vault | **Hors périmètre** (voir README principale) |

---

## 3. Structure du dépôt (détaillée)

```
mlops-full-project/
├── data/
│   ├── raw/
│   │   ├── generate_churn_data.py      # ~7000 lignes, seed 42, attribut sensible: gender
│   │   └── generate_creditcard_data.py # 10 000 lignes, 2.2% fraude (format Kaggle PCA)
│   ├── processed/ model_dataset_clean.csv
│   ├── reference/                      # dataset de référence (drift)
│   └── features/                       # features.parquet + feast_features.parquet
├── feature_repo/                       # Feast
│   ├── feature_store.yaml
│   ├── entities.py                     # entité `customer` (customer_id)
│   ├── features.py                     # FeatureView customer_features (16 champs, TTL 30 j)
│   └── data_sources.py                 # FileSource → feast_features.parquet
├── pipelines/                          # ZenML
│   ├── training_pipeline.py           # ingest→validate(GE)→preprocess→features→train
│   ├── tuning_pipeline.py             # Optuna 50 essais, sous-runs MLflow
│   └── retraining_pipeline.py         # check_drift→retrain→validate→promote_if_better
├── src/
│   ├── config.py                       # hub central : chemins + seuils
│   ├── data/
│   │   ├── ingestion.py               # log row count/période/hash SHA256
│   │   ├── preprocessing.py           # fonctions pures : dédup→missing→clamp→dtypes
│   │   └── validation.py               # pilotage programme GE (RuntimeBatchRequest)
│   ├── features/build_features.py      # 6 features dérivées row-local ; one-hot int8
│   ├── models/
│   │   ├── train.py                    # RF + tracking MLflow + registry
│   │   ├── tune.py                     # Optuna TPE, 3-fold CV F1
│   │   ├── evaluate.py                 # ROC/PR PNG, PASS/FAIL vs seuils
│   │   ├── explain.py                  # SHAP global+local, LIME cross-check
│   │   ├── fairness_check.py           # Fairlearn, DP Diff / Equalized Odds
│   │   ├── promote.py                  # 4 gates avant promotion + model card
│   │   ├── export_onnx.py              # skl2onnx + vérification de parité (hors scope README)
│   │   └── automl_baseline.py          # FLAML baseline (hors scope README)
│   ├── ledger/
│   │   ├── schema.sql                  # append-only, hash-chainé
│   │   ├── writer.py                   # écriture write-once
│   │   └── replay.py                   # rejeu + détection de mismatch P1
│   ├── serving/
│   │   ├── bento_service.py            # /predict + /explain (BentoML)
│   │   └── champion_challenger.py      # routeur 10% challenger, log JSONL
│   ├── oversight/console.py           # file de supervision + analytics d'override
│   ├── monitoring/
│   │   ├── drift_report.py            # Evidently DataDrift + TargetDrift
│   │   └── retraining_trigger.py      # lance ZenML si drift_score > seuil
│   └── api/main.py                    # app FastAPI fraude (port 8101)
├── api/main.py                         # app FastAPI fraude parallèle (port 8001, StandardScaler)
├── model_cards/model_card_template.py  # auto-génération Markdown
├── evidence/                           # Evidence Packs par modèle/version
├── tests/  (unit/, data/, model/)
├── report/, ui/, notebooks/
├── requirements.txt, pyproject.toml, dvc.yaml, Dockerfile.bento
```

---

## 4. Fonctionnement pas à pas

### 4.1 Données synthétiques

```bash
python data/raw/generate_churn_data.py          # → data/raw/dataset.csv (~7000 lignes)
python data/raw/generate_creditcard_data.py     # → data/raw/creditcard.csv (fraude)
```
Générateurs déterministes (`seed=42`) : churn logit corrélé à tenure/charges, avec corrélation
cible voulue sur `gender` (pour donner du signal à l'audit d'équité).

### 4.2 Pipeline DVC (`dvc.yaml`)

- **validate** : `src.data.ingestion` + `src.data.validation` (GE checkpoint, batch en mémoire).
- **preprocess** : déduplication → suppression des valeurs manquantes → clamp des bornes
  numériques → enforcement des dtypes → `dataset_clean.csv`.
- **build_features** : `src.features.build_features` — 6 features dérivées row-local,
  one-hot encoding (drop_first, int8) → `features.parquet` + `feast_features.parquet`.

### 4.3 Feature store (Feast)

`entities.py` (entité `customer`), `features.py` (single FeatureView `customer_features`,
16 champs typés, TTL 30 j), `data_sources.py` (FileSource avec `timestamp_field`, garantit
point-in-time correctness offline==online).

### 4.4 Entraînement + tracking (MLflow)

```bash
python -m src.models.train --register --run-name demo_model
# ou via ZenML : python -m pipelines.training_pipeline
```
RandomForest (200 arbres, max_depth 12). Loge params, métriques, matrice de confusion,
tag de source de données. Enregistre au registry + `models/churn_model.joblib`.

### 4.5 Tuning (Optuna)

```bash
python -m src.models.tune --trials 50
# ou : python -m pipelines.tuning_pipeline
```
TPE bayésien, objectif F1 (3-fold stratified CV), chaque essai logué en **sous-run** MLflow
(parallélisable en coordonnées).

### 4.6 Explicabilité (SHAP + LIME)

```bash
python -m src.models.explain
# → reports/shap_summary.png ; valeurs SHAP par décision
```

### 4.7 Équité — gate à seuils (Fairlearn)

```bash
python -m src.models.fairness_check
```
Calcule le taux de sélection par groupe, la **Demographic Parity Difference** et l'**Equalized
Odds Difference**. `passed = dp_diff <= 0.1`. Génère `fairness_report.json` +
`fairness_selection_rate.png`. (La spec définit le gate **tiered Green/Amber/Red** fondé sur la
règle des 4/5 qui supplante le seuil binaire simple en production.)

### 4.8 Promotion — 4 gates

```bash
python -m src.models.promote
```
Tous doivent passer :
1. **F1 ≥ 0.25**
2. **Bat la production actuelle** (marge 0.005)
3. **Deepchecks** full suite sans échec
4. **Fairness** DP diff ≤ seuil
→ alias/transition MLflow vers Production, écriture `promotion_report.json`, génération du
model card.

### 4.9 Serving (BentoML)

```bash
bentoml serve src.serving.bento_service:svc
# POST /predict  → {prediction, adverse_action_codes}
# POST /explain  → {expected_value, shap_values}  (waterfall pour l'Oversight Console)
```
Chaque décision est écrite dans le **Decision Ledger**. Model tag `churn_model:production`.

### 4.10 Champion/Challenger

```bash
python -m src.serving.champion_challenger --requests 1000
```
Routage ~10% vers le challenger (shadow-mode d'abord), chaque décision loguée
(`monitoring/logs/routing_decisions.jsonl`).

### 4.11 Drift (Evidently) + réentraînement

```bash
python -m src.monitoring.drift_report --drift-strength 0.5
# → monitoring/reports/drift_report.html
python -m src.monitoring.retraining_trigger --dry-run
# lance la pipeline ZenML si drift_score > 0.3 ; promotion Staging SEULEMENT
```

---

## 5. Procédure de test

```bash
# Tests unitaires  (ledger hash-chain/replay, reason-code coverage,
#   isolation attribut protégé, monotonicité, features, preprocessing, équité)
pytest tests/unit/

# Tests de validation des données
pytest tests/data/

# Tests de qualité modèle (Deepchecks)
pytest tests/model/
```

- `tests/unit/test_fairness.py` — seuil == 0.1, DP diff == 0 à taux égaux, rejet > seuil,
  construction scénario pass.
- `tests/unit/test_preprocessing.py` et `test_features.py` — fonctions pures, pureté entrée.
- `tests/data/test_data_validation.py` — miroir de la suite GE : ordre du schéma, plage
  lignes, pas de nulls, unicité customer_id, types, niveaux catégoriels.
- `tests/model/test_model_quality.py` — l'attribut sensible `gender` **n'atteint jamais le
  modèle** ; F1 ≥ 0.2, AUC ≥ 0.75 ; stabilité du top-5 des importances (≥2 parmi la famille
  churn/tenure/charges) ; Deepchecks (skip si absente).

**Validation de données indépendante** :
```bash
python3 -m src.data.validation
```

> Le checkpoint `dataset_checkpoint` s'appuie sur un `RuntimeDataConnector` (batch
> in-memory) : il ne peut pas être piloté via le CLI `great_expectations checkpoint run`.
> Le contrat est exécuté par `src/data/validation.py` (et par le stage DVC `validate`).

---

## 6. Config et seuils de référence

Tous dans `src/config.py` :
```python
FAIRNESS_DP_THRESHOLD = 0.1   # Demographic parity diff (hard gate)
DRIFT_THRESHOLD = 0.3         # Seuil de déclenchement drift
F1_PROMOTION_THRESHOLD = 0.25
AUC_PROMOTION_THRESHOLD = 0.80
CHALLENGER_RATIO = 0.1        # 10% du trafic vers challenger
```
> La spec §8.3 définit le gate tiered (Green/Amber/Red, règle des 4/5) qui supplante le seuil
> binaire comme contrôle de production.

---

## 7. Points d'attention (audit du code)

1. **Deux APIs FastAPI fraude quasi-dupliquées** : `src/api/main.py` (port 8101, sans scaling)
   et `api/main.py` (port 8001, avec `StandardScaler`, bands de risque différentes) — chemins
   de serving séparés de BentoML (churn).
2. **Empreinte de scaling machine** : StandardScaler présent dans une API mais pas l'autre ;
   veiller à la parité train/inférence.
3. **Seuils binaires** dans le code vs **gate tiered** de la spec (Green/Amber/Red) — le code
   actif applique encore le seuil binaire, la spec documente le gate tiered.
4. **Fichiers hors périmètre README** : `export_onnx.py`, `automl_baseline.py` et le drift
   FEM existent dans le code mais sont **exclus du périmètre déclaré** de la version officielle.
5. **Graceful degradation** via flags `EVIDENTLY_AVAILABLE`, `FAIRLEARN_AVAILABLE`, skip
   Deepchecks à l'ImportError — utile pour des environnements sans libs lourdes, mais à noter.

---

## 8. Références

- [README principale](./README.md) — vue d'ensemble et démarrage rapide.
- [`mlops-full-mlops-skills-project.md`](./mlops-full-mlops-skills-project.md) — spec produit
  complète (Evidence Pack, ledger, reason codes, gate tiered).
- [`ENTERPRISE-UPGRADE.md`](./ENTERPRISE-UPGRADE.md) — montée en version enterprise.
- `Dockerfile.bento` — conteneur BentoML (python:3.10-slim, `bentoml build/serve`).
