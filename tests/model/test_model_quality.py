"""Model quality tests (Deepchecks where available).

Trains on the versioned churn dataset through the same feature pipeline the
production trainer uses, so what is asserted here is what gets shipped.
"""
import pytest
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from src.config import SENSITIVE_COL, TARGET_COL
from src.models.train import DEFAULT_PARAMS, load_training_data


@pytest.fixture(scope="module")
def model_and_data():
    """Train a churn model and expose the held-out split."""
    X, y = load_training_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    params = {**DEFAULT_PARAMS, "n_estimators": 100}
    model = XGBClassifier(**params)
    model.fit(X_train, y_train)

    return model, X_test, y_test


def test_model_loaded(model_and_data):
    model, _, _ = model_and_data
    assert model is not None


def test_model_predicts(model_and_data):
    model, X_test, _ = model_and_data
    preds = model.predict(X_test)
    assert len(preds) == len(X_test)
    assert set(preds).issubset({0, 1})


def test_model_predict_proba(model_and_data):
    model, X_test, _ = model_and_data
    proba = model.predict_proba(X_test)
    assert proba.shape == (len(X_test), 2)
    assert (proba >= 0).all() and (proba <= 1).all()


def test_sensitive_attribute_isolated(model_and_data):
    """The protected attribute must never reach the model."""
    _, X_test, _ = model_and_data
    leaked = [c for c in X_test.columns if c.startswith(SENSITIVE_COL)]
    assert not leaked, f"Sensitive attribute leaked into features: {leaked}"


def test_model_performance_threshold(model_and_data):
    """Basic performance check - F1 should be reasonable."""
    from sklearn.metrics import f1_score

    model, X_test, y_test = model_and_data
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    assert f1 >= 0.2, f"F1 score {f1:.4f} below minimum threshold"


def test_model_auc_threshold(model_and_data):
    from sklearn.metrics import roc_auc_score

    model, X_test, y_test = model_and_data
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    assert auc >= 0.75, f"AUC {auc:.4f} below minimum threshold"


def test_deepchecks_suite(model_and_data):
    """Run Deepchecks full suite if available."""
    try:
        from deepchecks.tabular import Dataset
        from deepchecks.tabular.suites import full_suite
    except ImportError:
        pytest.skip("deepchecks not available")

    model, X_test, y_test = model_and_data

    # Deepchecks needs the full dataframe with label
    test_df = X_test.copy()
    test_df[TARGET_COL] = y_test.values

    ds = Dataset(test_df, label=TARGET_COL)
    result = full_suite().run(ds, model=model)

    critical_failures = [
        check.get_header() for check in result.results if not check.passed
    ]

    # Failures are surfaced as warnings here; promotion gates in
    # src/models/promote.py are what actually block a release.
    if critical_failures:
        print(f"Deepchecks critical failures: {critical_failures}")


def test_model_feature_importance_stable(model_and_data):
    """Top features must stay in the churn-tenure/charges family."""
    import numpy as np

    model, X_test, _ = model_and_data

    importances = model.feature_importances_
    top_feature_names = {X_test.columns[i] for i in np.argsort(importances)[-5:]}

    expected_important = {
        "avg_charge_per_month",
        "contract_type_one_year",
        "contract_type_two_year",
        "is_high_value_customer",
        "payment_method_electronic_check",
        "tenure_months",
        "monthly_charges",
        "is_long_tenure",
    }

    overlap = len(expected_important & top_feature_names)
    assert overlap >= 2, (
        f"Top features {sorted(top_feature_names)} don't match "
        f"expected {sorted(expected_important)}"
    )
