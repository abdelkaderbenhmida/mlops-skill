# Projet MLOps Complet — Maximisation des Skills & Outils MLOps

> Périmètre volontairement **100% MLOps** : cycle de vie de la donnée et du modèle, expérimentation, feature engineering, optimisation, explicabilité, équité, serving, monitoring modèle et réentraînement.
> **Exclu volontairement** : Kubernetes, Terraform/Ansible, gestion de secrets type Vault, scan de sécurité (bandit/trivy), monitoring infra générique (Prometheus/Grafana bas niveau) — ce sont des sujets DevOps/DevSecOps, pas MLOps.

---

## Table des matières

1. [Vue d'ensemble](#1-vue-densemble)
2. [Cartographie complète des skills MLOps couverts](#2-cartographie-complète-des-skills-mlops-couverts)
3. [Architecture globale](#3-architecture-globale)
4. [Structure du dépôt](#4-structure-du-dépôt)
5. [Ingestion & gestion des données](#5-ingestion--gestion-des-données)
6. [Validation de la qualité des données](#6-validation-de-la-qualité-des-données)
7. [Versioning des données (DVC)](#7-versioning-des-données-dvc)
8. [Feature Engineering & Feature Store (Feast)](#8-feature-engineering--feature-store-feast)
9. [Orchestration ML-native (ZenML / Metaflow)](#9-orchestration-ml-native-zenml--metaflow)
10. [Expérimentation & Tracking (MLflow)](#10-expérimentation--tracking-mlflow)
11. [Optimisation d'hyperparamètres (Optuna)](#11-optimisation-dhyperparamètres-optuna)
12. [AutoML (optionnel, comparatif)](#12-automl-optionnel-comparatif)
13. [Model Registry & cycle de vie](#13-model-registry--cycle-de-vie)
14. [Validation & tests du modèle (Deepchecks)](#14-validation--tests-du-modèle-deepchecks)
15. [Explicabilité (SHAP / LIME)](#15-explicabilité-shap--lime)
16. [Équité & détection de biais (Fairlearn)](#16-équité--détection-de-biais-fairlearn)
17. [Packaging & interopérabilité (ONNX)](#17-packaging--interopérabilité-onnx)
18. [Serving ML-natif (BentoML)](#18-serving-ml-natif-bentoml)
19. [Monitoring du modèle en production (Evidently)](#19-monitoring-du-modèle-en-production-evidently)
20. [Stratégie Champion / Challenger & A/B Testing](#20-stratégie-champion--challenger--ab-testing)
21. [Model Cards & documentation du modèle](#21-model-cards--documentation-du-modèle)
22. [Réentraînement automatique piloté par le drift](#22-réentraînement-automatique-piloté-par-le-drift)
23. [Tests automatisés du pipeline ML](#23-tests-automatisés-du-pipeline-ml)
24. [Plan de mise en œuvre](#24-plan-de-mise-en-œuvre)
25. [Critères de succès / Definition of Done](#25-critères-de-succès--definition-of-done)
26. [Glossaire](#26-glossaire)

---

## 1. Vue d'ensemble

### 1.1 Objectif

Construire un projet qui couvre **le maximum de compétences et d'outils spécifiquement MLOps** — c'est-à-dire tout ce qui concerne le cycle de vie de la donnée et du modèle (et non l'infrastructure générique). L'accent est mis sur la **profondeur ML** : feature store, tuning, explicabilité, équité, monitoring de drift, champion/challenger — des sujets souvent absents des projets MLOps "basiques" qui se contentent de Docker + CI/CD.

### 1.2 Ce qui différencie ce projet

| Projet MLOps "basique" | Ce projet |
|---|---|
| Un seul modèle entraîné une fois | Plusieurs candidats comparés via tuning automatisé |
| Pas de feature store | Feature Store réel (Feast) avec vues online/offline |
| Tracking simple | Tracking + Registry + Model Cards + Explicabilité |
| Pas de vérif équité | Suite de tests de fairness avant promotion |
| Déploiement figé | Champion/Challenger avec bascule progressive du trafic |
| Monitoring absent ou générique | Monitoring de drift **spécifique au ML** (data + concept + prédiction) |

### 1.3 Cas d'usage recommandé

Un cas de classification avec **enjeu d'équité identifiable** valorise davantage le projet : ex. **scoring de crédit**, **acceptation de prêt**, ou **churn client** (variables sensibles simulées : âge, genre, région).

---

## 2. Cartographie complète des skills MLOps couverts

| Domaine MLOps | Outil(s) | Statut dans ce projet |
|---|---|---|
| Versioning des données | DVC | ✅ Inclus |
| Validation de la qualité des données | Great Expectations | ✅ Inclus |
| Feature Engineering | pandas / scikit-learn pipelines | ✅ Inclus |
| Feature Store (online + offline) | Feast | ✅ Inclus |
| Orchestration de pipeline ML-native | ZenML (ou Metaflow) | ✅ Inclus |
| Tracking d'expériences | MLflow | ✅ Inclus |
| Optimisation d'hyperparamètres | Optuna | ✅ Inclus |
| AutoML comparatif | AutoGluon ou FLAML | ✅ Inclus (optionnel) |
| Model Registry | MLflow Registry | ✅ Inclus |
| Tests automatisés du modèle | Deepchecks | ✅ Inclus |
| Explicabilité globale/locale | SHAP, LIME | ✅ Inclus |
| Détection de biais / équité | Fairlearn | ✅ Inclus |
| Packaging portable | ONNX + onnxruntime | ✅ Inclus |
| Serving ML-natif | BentoML | ✅ Inclus |
| Monitoring de drift (données/concept/prédiction) | Evidently | ✅ Inclus |
| Champion/Challenger, A/B testing modèle | Logique custom + MLflow | ✅ Inclus |
| Documentation modèle | Model Cards (Google Model Card Toolkit) | ✅ Inclus |
| Réentraînement piloté par le drift | Script Python + condition | ✅ Inclus |
| Tests unitaires/intégration ML | pytest | ✅ Inclus |
| ~~Kubernetes~~ | — | ❌ Exclu (DevOps) |
| ~~Terraform / Ansible~~ | — | ❌ Exclu (DevOps) |
| ~~Vault / gestion secrets~~ | — | ❌ Exclu (DevSecOps) |
| ~~Scan sécurité (bandit/trivy)~~ | — | ❌ Exclu (DevSecOps) |
| ~~Prometheus/Grafana infra~~ | — | ❌ Exclu (DevOps, remplacé par monitoring ML) |

> Docker est conservé au strict minimum (packaging du service de serving BentoML), car il s'agit d'un standard incontournable pour livrer un modèle — mais aucune orchestration de conteneurs n'est traitée ici.

---

## 3. Architecture globale

```
┌─────────────┐   ┌──────────────────┐   ┌───────────────────┐
│ Données     │──▶│ Great Expectations│──▶│  DVC (versioning)  │
│ brutes      │   │ (validation)      │   │                    │
└─────────────┘   └──────────────────┘   └───────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │ Feature Engineering│
                                          └───────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │  Feast              │
                                          │  (Feature Store)    │
                                          │  offline + online   │
                                          └───────────────────┘
                                                     │
                        ┌────────────────────────────┼────────────────────────────┐
                        ▼                             ▼                             ▼
              ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
              │ Optuna            │───────▶│ MLflow Tracking   │◀───────│ AutoML (optionnel)│
              │ (tuning)          │        │ (tous les runs)   │        │                    │
              └──────────────────┘        └──────────────────┘        └──────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │ Deepchecks          │
                                          │ (validation modèle) │
                                          └───────────────────┘
                                                     │
                                          ┌──────────┼──────────┐
                                          ▼                     ▼
                                ┌──────────────────┐  ┌──────────────────┐
                                │ SHAP / LIME        │  │ Fairlearn          │
                                │ (explicabilité)    │  │ (équité)           │
                                └──────────────────┘  └──────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │ MLflow Registry     │
                                          │ (Staging/Production)│
                                          └───────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │ ONNX export         │
                                          │ (packaging portable)│
                                          └───────────────────┘
                                                     │
                                                     ▼
                                          ┌───────────────────┐
                                          │ BentoML              │
                                          │ (serving ML-natif)   │
                                          └───────────────────┘
                                                     │
                                     ┌───────────────┼───────────────┐
                                     ▼                               ▼
                          ┌──────────────────┐          ┌──────────────────┐
                          │ Champion (v_n-1)   │          │ Challenger (v_n)   │
                          │  90% du trafic      │          │  10% du trafic      │
                          └──────────────────┘          └──────────────────┘
                                     │                               │
                                     └───────────────┬───────────────┘
                                                      ▼
                                          ┌───────────────────┐
                                          │ Evidently            │
                                          │ (drift + perf)        │
                                          └───────────────────┘
                                                      │
                                                      ▼ (si drift/dégradation)
                                          ┌───────────────────┐
                                          │ Réentraînement       │
                                          │ automatique           │
                                          └───────────────────┘
```

---

## 4. Structure du dépôt

```
mlops-full-project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/                      # dataset de référence pour le drift
│
├── great_expectations/
│   └── expectations/
│       └── dataset_suite.json
│
├── feature_repo/                       # dépôt Feast
│   ├── feature_store.yaml
│   ├── entities.py
│   ├── features.py
│   └── data_sources.py
│
├── pipelines/                          # pipelines ZenML
│   ├── training_pipeline.py
│   ├── tuning_pipeline.py
│   └── retraining_pipeline.py
│
├── src/
│   ├── data/
│   │   ├── ingestion.py
│   │   └── preprocessing.py
│   │
│   ├── features/
│   │   └── build_features.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── tune.py                     # Optuna
│   │   ├── automl_baseline.py          # comparatif AutoML
│   │   ├── evaluate.py
│   │   ├── explain.py                  # SHAP / LIME
│   │   ├── fairness_check.py           # Fairlearn
│   │   ├── export_onnx.py
│   │   └── promote.py
│   │
│   ├── serving/
│   │   ├── bento_service.py
│   │   └── champion_challenger.py
│   │
│   └── monitoring/
│       ├── drift_report.py             # Evidently
│       └── retraining_trigger.py
│
├── model_cards/
│   └── model_card_template.py
│
├── tests/
│   ├── unit/
│   │   ├── test_preprocessing.py
│   │   ├── test_features.py
│   │   └── test_fairness.py
│   ├── model/
│   │   └── test_model_quality.py       # Deepchecks
│   └── data/
│       └── test_data_validation.py     # Great Expectations
│
├── notebooks/
│   └── exploration.ipynb
│
├── mlflow/
│   └── mlruns/                         # ou serveur local sqlite
│
├── dvc.yaml
├── requirements.txt
├── pyproject.toml
├── Dockerfile.bento                    # packaging minimal du service
└── README.md
```

---

## 5. Ingestion & gestion des données

### 5.1 Rôle

Récupérer les données brutes (fichier local, API publique, ou base simulée) et les préparer pour la suite du pipeline.

### 5.2 Bonnes pratiques

- Séparation stricte `raw/` (jamais modifié) vs `processed/` (généré)
- Chaque transformation est une fonction pure, testable indépendamment
- Le script d'ingestion logue le nombre de lignes, la période couverte, et un hash du fichier source

---

## 6. Validation de la qualité des données

### 6.1 Rôle (Great Expectations)

Garantir qu'aucune donnée corrompue ou hors-norme n'entre dans le pipeline d'entraînement — **avant** même le feature engineering.

### 6.2 Exemples d'attentes définies

- Absence de valeurs nulles sur les colonnes critiques
- Plage de valeurs attendue pour chaque variable numérique (ex : âge entre 18 et 100)
- Cohérence des types de colonnes
- Volume minimal de lignes attendu

### 6.3 Intégration

Ce contrôle est la **première étape** de tout pipeline (`training_pipeline`, `retraining_pipeline`) — si la validation échoue, le pipeline s'arrête avant de gaspiller du calcul sur un entraînement inutile.

---

## 7. Versioning des données (DVC)

### 7.1 Rôle

Assurer la reproductibilité exacte : quel dataset a produit quel modèle.

### 7.2 Pipeline DVC

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

---

## 8. Feature Engineering & Feature Store (Feast)

### 8.1 Pourquoi un feature store ici

C'est l'un des composants les **plus spécifiquement MLOps** et souvent absent des projets portfolio — il garantit la cohérence entre les features utilisées à l'entraînement (offline) et celles utilisées en inférence temps réel (online), en évitant le "training-serving skew".

### 8.2 Composants Feast

| Fichier | Rôle |
|---|---|
| `entities.py` | Définit les clés d'entité (ex : `customer_id`) |
| `data_sources.py` | Pointe vers le fichier Parquet/offline store |
| `features.py` | Définit les `FeatureView` (groupes de features avec TTL) |
| `feature_store.yaml` | Configuration du store (offline = fichier local, online = SQLite/Redis léger) |

### 8.3 Exemple conceptuel de `FeatureView`

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

### 8.4 Utilisation

- **Entraînement** : `store.get_historical_features(...)` récupère les features au bon timestamp (point-in-time correctness — évite le data leakage temporel)
- **Inférence** : `store.get_online_features(...)` récupère les dernières valeurs en quelques millisecondes

### 8.5 Ce que ça démontre

La maîtrise du concept de **point-in-time join**, une des difficultés les plus sous-estimées du ML en production, et directement valorisable en entretien.

---

## 9. Orchestration ML-native (ZenML / Metaflow)

### 9.1 Pourquoi pas Airflow ici

Airflow est un orchestrateur généraliste (proche du data engineering/DevOps). **ZenML** et **Metaflow** sont conçus spécifiquement pour les workflows ML : gestion native des artefacts, du versioning de pipeline, et intégration directe avec MLflow/Feast.

### 9.2 Rôle de ZenML

- Définit les pipelines comme des fonctions Python décorées (`@step`, `@pipeline`)
- Trace automatiquement chaque exécution (artefacts, paramètres, métadonnées)
- S'intègre nativement avec MLflow comme "Experiment Tracker" et avec Evidently comme "Data Validator"

### 9.3 Exemple conceptuel

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

### 9.4 Bénéfice

Contrairement à un simple script séquentiel, chaque `step` est mis en cache : si les données n'ont pas changé, ZenML réutilise le résultat précédent — gain de temps considérable en itération.

---

## 10. Expérimentation & Tracking (MLflow)

### 10.1 Rôle

Centraliser tous les runs (tuning, AutoML, entraînements manuels) pour comparaison objective.

### 10.2 Ce qui est loggé pour chaque run

- Hyperparamètres complets
- Métriques (accuracy, F1, AUC, ou RMSE selon le cas)
- Artefacts : modèle, matrice de confusion, courbe ROC, rapport SHAP, rapport de fairness
- Tags : source des données (hash DVC), version du pipeline ZenML

### 10.3 Comparaison de runs

L'UI MLflow permet de trier tous les runs (manuels + Optuna + AutoML) sur un même graphique parallèle de coordonnées — utile pour visualiser l'effet de chaque hyperparamètre sur la métrique cible.

---

## 11. Optimisation d'hyperparamètres (Optuna)

### 11.1 Rôle

Automatiser la recherche du meilleur jeu d'hyperparamètres via une recherche bayésienne (bien plus efficace qu'un grid search classique).

### 11.2 Intégration avec MLflow

Chaque essai (`trial`) d'Optuna est loggé comme un run MLflow enfant, permettant de visualiser toute la recherche dans l'UI MLflow.

### 11.3 Exemple conceptuel (`tune.py`)

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
        mlflow.log_metric("f1_score", score)
    return score

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
```

### 11.4 Ce que ça démontre

La capacité à automatiser une phase souvent faite "à la main" — un vrai gain de crédibilité technique pour un projet MLOps avancé.

---

## 12. AutoML (optionnel, comparatif)

### 12.1 Rôle

Comparer le modèle optimisé manuellement (Optuna) à une baseline AutoML (**FLAML** ou **AutoGluon**), pour valider que l'effort d'ingénierie apporte un gain réel.

### 12.2 Utilisation

```python
from flaml import AutoML

automl = AutoML()
automl.fit(X_train, y_train, task="classification", time_budget=120)
```

### 12.3 Ce que ça démontre

Une compréhension mature du MLOps : ne pas sur-ingénierer quand une solution automatisée suffit, mais savoir le prouver par la mesure plutôt que par supposition.

---

## 13. Model Registry & cycle de vie

### 13.1 Rôle

Gérer les versions et les stages (`Staging` → `Production` → `Archived`) du modèle final retenu (issu d'Optuna ou d'AutoML, selon lequel est meilleur).

### 13.2 Critères de promotion (`promote.py`)

Un modèle n'est promu que s'il passe **toutes** ces portes :
1. Performance ≥ seuil minimal (ex : F1 > 0.85)
2. Meilleur que le modèle en Production actuel
3. Tests Deepchecks passés (section 14)
4. Tests de fairness passés (section 16)

### 13.3 Traçabilité complète

Chaque version enregistrée est liée à : un commit Git, un hash DVC des données, un run MLflow complet, un rapport SHAP, et un rapport de fairness — traçabilité de bout en bout.

---

## 14. Validation & tests du modèle (Deepchecks)

### 14.1 Rôle

Aller au-delà d'une simple métrique de performance : Deepchecks exécute une suite de vérifications automatisées sur les données ET le modèle.

### 14.2 Types de vérifications incluses

| Catégorie | Exemples de checks |
|---|---|
| Intégrité des données | Doublons, valeurs manquantes, types incohérents |
| Distribution train/test | Vérifie que le split est représentatif |
| Performance du modèle | Comparaison à une baseline naïve |
| Robustesse | Sensibilité à un bruit léger sur les features |
| Overfitting | Écart de performance train vs test |

### 14.3 Intégration

```python
from deepchecks.tabular.suites import full_suite

suite = full_suite()
result = suite.run(train_dataset, test_dataset, model)
result.save_as_html("reports/deepchecks_report.html")
```

Le pipeline bloque la promotion si le suite Deepchecks contient un échec critique.

---

## 15. Explicabilité (SHAP / LIME)

### 15.1 Rôle

Comprendre **pourquoi** le modèle prend chaque décision — indispensable pour la confiance métier et, dans certains contextes (crédit, santé, RH), une exigence réglementaire.

### 15.2 SHAP (explicabilité globale et locale)

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Importance globale des features
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("reports/shap_summary.png")

# Explication d'une prédiction individuelle
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])
```

### 15.3 LIME (explication locale alternative)

Utilisé en complément pour vérifier la cohérence des explications sur des cas individuels avec une méthode indépendante de SHAP (utile pour la robustesse de l'analyse).

### 15.4 Intégration dans l'API/service

Un endpoint `/explain` (dans le service BentoML) peut retourner les contributions SHAP pour une prédiction donnée, en plus de la prédiction elle-même.

---

## 16. Équité & détection de biais (Fairlearn)

### 16.1 Rôle

Vérifier que le modèle ne discrimine pas systématiquement un sous-groupe (ex : genre, âge, région), même si cette variable n'est pas utilisée directement comme feature (biais indirect via des variables corrélées).

### 16.2 Métriques calculées

| Métrique | Ce qu'elle mesure |
|---|---|
| Demographic Parity Difference | Écart de taux de prédictions positives entre groupes |
| Equalized Odds Difference | Écart de taux de vrais/faux positifs entre groupes |
| Selection Rate par groupe | Taux d'acceptation par sous-population |

### 16.3 Exemple conceptuel (`fairness_check.py`)

```python
from fairlearn.metrics import MetricFrame, demographic_parity_difference

metric_frame = MetricFrame(
    metrics={"accuracy": accuracy_score, "selection_rate": selection_rate},
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=X_test["gender"]
)

dp_diff = demographic_parity_difference(y_test, y_pred, sensitive_features=X_test["gender"])
```

### 16.4 Intégration au pipeline de promotion

Si `dp_diff` dépasse un seuil défini (ex : 0.1), le modèle est automatiquement rejeté de la promotion, même si sa performance globale est excellente — **la performance seule ne suffit pas**.

---

## 17. Packaging & interopérabilité (ONNX)

### 17.1 Rôle

Exporter le modèle final dans un format standardisé, indépendant du framework d'entraînement (scikit-learn, XGBoost, LightGBM) — utile pour la portabilité et des inférences plus rapides.

### 17.2 Exemple conceptuel (`export_onnx.py`)

```python
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

onnx_model = convert_sklearn(
    model, initial_types=[("input", FloatTensorType([None, n_features]))]
)
with open("models/model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

### 17.3 Vérification de la conversion

Un test compare les prédictions du modèle original et du modèle ONNX sur le même jeu de test, pour garantir que la conversion n'a pas dégradé les résultats (tolérance numérique définie).

### 17.4 Ce que ça démontre

La compréhension des enjeux d'interopérabilité entre écosystèmes ML — un skill recherché quand plusieurs équipes/langages coexistent (ex : entraînement en Python, inférence en Java/C++).

---

## 18. Serving ML-natif (BentoML)

### 18.1 Pourquoi BentoML plutôt que FastAPI seul

BentoML est un framework **spécifiquement conçu pour le serving de modèles ML** : il gère nativement le versioning des modèles, le batching adaptatif des requêtes, la génération automatique de l'image de service, et l'intégration directe avec le Model Registry MLflow.

### 18.2 Définition du service (`bento_service.py`)

```python
import bentoml
from bentoml.io import JSON

model_ref = bentoml.mlflow.get("mon_modele:latest")
runner = model_ref.to_runner()

svc = bentoml.Service("mlops_service", runners=[runner])

@svc.api(input=JSON(), output=JSON())
def predict(input_data: dict):
    result = runner.predict.run([list(input_data.values())])
    return {"prediction": result.tolist()}

@svc.api(input=JSON(), output=JSON())
def explain(input_data: dict):
    # Retourne les valeurs SHAP pour cette prédiction
    ...
```

### 18.3 Bénéfices spécifiques MLOps

- **Batching adaptatif** : regroupe automatiquement plusieurs requêtes simultanées pour optimiser le débit d'inférence
- **Versioning natif des "Bento"** (paquet de service) lié directement à la version du modèle dans MLflow
- Génère automatiquement un `Dockerfile.bento` minimal si besoin d'un packaging portable

---

## 19. Monitoring du modèle en production (Evidently)

### 19.1 Rôle

Surveiller **trois types de dérive**, spécifiquement ML (pas de l'infra) :

| Type de dérive | Ce qui est surveillé |
|---|---|
| **Data drift** | Distribution des features en entrée a changé |
| **Concept drift** | La relation features → cible a changé |
| **Prediction drift** | La distribution des prédictions elle-même a changé |

### 19.2 Rapport généré (`drift_report.py`)

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

report = Report(metrics=[DataDriftPreset(), TargetDriftPreset()])
report.run(reference_data=reference_df, current_data=production_sample_df)
report.save_html("monitoring/reports/drift_report.html")

drift_score = report.as_dict()["metrics"][0]["result"]["dataset_drift"]
```

### 19.3 Suivi de la performance réelle (si labels disponibles a posteriori)

Quand le vrai label devient disponible (ex : défaut de paiement constaté 30 jours après la prédiction), un job compare la prédiction historique au résultat réel et recalcule les métriques de performance réelles en production — la vérification la plus fiable de la santé du modèle.

---

## 20. Stratégie Champion / Challenger & A/B Testing

### 20.1 Rôle

Ne jamais remplacer brutalement un modèle en production : le nouveau modèle ("Challenger") reçoit d'abord une fraction du trafic, en parallèle du modèle actuel ("Champion").

### 20.2 Logique (`champion_challenger.py`)

```python
import random

def route_prediction(input_data, challenger_ratio=0.1):
    if random.random() < challenger_ratio:
        model_version = "challenger"
        prediction = challenger_model.predict(input_data)
    else:
        model_version = "champion"
        prediction = champion_model.predict(input_data)

    log_prediction(input_data, prediction, model_version)  # pour analyse a posteriori
    return prediction, model_version
```

### 20.3 Analyse comparative

Après une période définie (ex : 2 semaines), comparaison statistique des performances Champion vs Challenger (test de significativité) avant de décider une promotion complète.

### 20.4 Ce que ça démontre

La maîtrise d'un déploiement progressif **piloté par les données**, plutôt qu'un remplacement risqué en un seul coup — pratique standard chez les équipes ML matures.

---

## 21. Model Cards & documentation du modèle

### 21.1 Rôle

Produire une documentation standardisée et lisible par des non-experts, décrivant : l'objectif du modèle, les données d'entraînement, les métriques de performance, les résultats de fairness, et les limites connues.

### 21.2 Contenu type d'une Model Card

- **Détails du modèle** : algorithme, version, date d'entraînement
- **Usage prévu** : cas d'usage validés / cas d'usage à éviter
- **Données d'entraînement** : source, période, taille
- **Métriques de performance** : globales et par sous-groupe
- **Analyse d'équité** : résultats Fairlearn résumés
- **Limites connues et biais identifiés**

### 21.3 Génération automatique

Un script (`model_cards/model_card_template.py`) récupère automatiquement les métriques depuis MLflow et les résultats Fairlearn pour générer la Model Card en Markdown/HTML à chaque promotion — évite la documentation obsolète.

---

## 22. Réentraînement automatique piloté par le drift

### 22.1 Séquence complète

```
1. drift_report.py s'exécute périodiquement (cron ou déclenchement manuel)
        ↓
2. Si dataset_drift == True ou drift_score > seuil
        ↓
3. Déclenchement de retraining_pipeline (ZenML)
        ↓
4. Nouveau tuning Optuna sur les données récentes
        ↓
5. Nouveau passage Deepchecks + Fairlearn
        ↓
6. Comparaison au Champion actuel
        ↓
7. Si meilleur ET équitable → promotion en Challenger (10% du trafic)
        ↓
8. Suivi 2 semaines → promotion complète si validé
```

### 22.2 Garde-fous

- Un modèle réentraîné automatiquement ne saute **jamais** l'étape Fairlearn, même en cas d'urgence
- Conservation des 3 dernières versions Production pour rollback immédiat
- Notification (log structuré / webhook) à chaque promotion automatique pour garder une supervision humaine

---

## 23. Tests automatisés du pipeline ML

### 23.1 Pyramide de tests spécifique MLOps

```
        ┌───────────────────────────┐
        │ Tests de fairness           │  (Fairlearn)
        ├───────────────────────────┤
        │ Tests de qualité modèle     │  (Deepchecks)
        ├───────────────────────────┤
        │ Tests de qualité données    │  (Great Expectations)
        ├───────────────────────────┤
        │ Tests unitaires classiques  │  (pytest)
        └───────────────────────────┘
```

### 23.2 Exemple de test de non-régression sur l'explicabilité

```python
def test_shap_top_feature_stable():
    """Vérifie que la feature la plus importante reste cohérente
    d'une version à l'autre du modèle (détecte un changement de comportement suspect)."""
    shap_values = compute_shap(model, X_sample)
    top_feature = get_top_feature(shap_values)
    assert top_feature in EXPECTED_TOP_FEATURES
```

---

## 24. Plan de mise en œuvre

| Étape | Livrable | Durée |
|---|---|---|
| 1 | Setup projet + DVC + Great Expectations | 1 jour |
| 2 | Feature engineering + Feast (feature store) | 1.5 jour |
| 3 | Pipelines ZenML (training + retraining) | 1 jour |
| 4 | Entraînement + tracking MLflow | 0.5 jour |
| 5 | Tuning Optuna + comparatif AutoML | 1 jour |
| 6 | Model Registry + promote.py | 0.5 jour |
| 7 | Deepchecks (validation modèle) | 0.5 jour |
| 8 | SHAP + LIME (explicabilité) | 1 jour |
| 9 | Fairlearn (équité) | 1 jour |
| 10 | Export ONNX + vérification | 0.5 jour |
| 11 | Service BentoML (predict + explain) | 1 jour |
| 12 | Champion/Challenger + logging | 1 jour |
| 13 | Monitoring Evidently (3 types de drift) | 1 jour |
| 14 | Model Cards automatiques | 0.5 jour |
| 15 | Boucle de réentraînement complète | 1 jour |
| 16 | Tests globaux + README + démo | 1 jour |

**Durée totale estimée : ~14-15 jours** pour une implémentation complète et rigoureuse.

---

## 25. Critères de succès / Definition of Done

- [ ] `dvc repro` reproduit exactement les mêmes métriques
- [ ] Le feature store Feast retourne des features cohérentes en mode offline et online
- [ ] Le pipeline ZenML s'exécute de bout en bout avec cache actif sur les étapes inchangées
- [ ] Tous les runs (manuels, Optuna, AutoML) apparaissent comparables dans MLflow
- [ ] Un modèle ne peut pas être promu s'il échoue Deepchecks ou Fairlearn
- [ ] Un rapport SHAP et un rapport de fairness sont générés pour chaque version en Production
- [ ] Le modèle ONNX produit des prédictions identiques (± tolérance) au modèle original
- [ ] Le service BentoML répond sur `/predict` et `/explain`
- [ ] Le routage Champion/Challenger fonctionne et logue chaque décision
- [ ] Un rapport Evidently détecte correctement un drift simulé (data, concept, prédiction)
- [ ] Une Model Card à jour est générée automatiquement à chaque promotion
- [ ] Le réentraînement se déclenche automatiquement sur drift simulé et respecte tous les garde-fous

---

## 26. Glossaire

| Terme | Définition |
|---|---|
| **Point-in-time correctness** | Garantie que les features utilisées à l'entraînement reflètent l'état des données au moment exact de l'événement, sans fuite d'information future |
| **Training-serving skew** | Différence entre les transformations appliquées à l'entraînement et à l'inférence, source fréquente de bugs silencieux |
| **Champion/Challenger** | Stratégie de déploiement où un nouveau modèle est testé en parallèle de l'ancien sur une fraction du trafic |
| **Demographic Parity** | Métrique d'équité mesurant si le taux de prédictions positives est similaire entre sous-groupes |
| **Data drift** | Changement de distribution des données d'entrée en production par rapport à l'entraînement |
| **Concept drift** | Changement de la relation entre les features et la cible |
| **Model Card** | Document standardisé décrivant les caractéristiques, performances et limites d'un modèle |
| **Batching adaptatif** | Regroupement automatique de requêtes d'inférence simultanées pour optimiser le débit |
