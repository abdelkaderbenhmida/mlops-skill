"""Unit tests for preprocessing functions."""
import pandas as pd
import pytest

from src.data.preprocessing import (
    drop_duplicates,
    drop_missing,
    clamp_numeric,
    cast_dtypes,
    preprocess,
)


def test_drop_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    result = drop_duplicates(df)
    assert len(result) == 2


def test_drop_missing():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})
    result = drop_missing(df, columns=["a"])
    assert len(result) == 2
    assert result["a"].notna().all()


def test_clamp_numeric():
    df = pd.DataFrame({"Time": [-10.0, 100.0, 5000.0], "Amount": [-50.0, 250.0, 250000.0]})
    result = clamp_numeric(df)
    assert (result["Time"] >= 0).all()
    assert result["Amount"].between(0, 100000).all()


def test_cast_dtypes():
    df = pd.DataFrame({
        "Time": [0.0, 10.0],
        "Amount": [50.0, 60.0],
        "V1": [-1.2, 0.5],
        "Class": [0, 1],
    })
    result = cast_dtypes(df)
    assert result["Time"].dtype == "float64"
    assert result["Amount"].dtype == "float64"
    assert result["V1"].dtype == "float64"
    assert result["Class"].dtype == "int8"


def test_preprocess_chain():
    df = pd.DataFrame({
        "Time": [0.0, 10.0, 10.0],
        "Amount": [50.0, -20.0, -20.0],
        "V1": [1.1, 2.2, 2.2],
        "V2": [0.5, -0.3, -0.3],
        "Class": [0, 1, 1],
    })
    result = preprocess(df)
    assert len(result) == 2  # deduped
    assert (result["Amount"] >= 0).all()
    assert result["Class"].dtype == "int8"