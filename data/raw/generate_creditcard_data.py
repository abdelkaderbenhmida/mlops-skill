#!/usr/bin/env python3
"""Generate a synthetic credit-card transaction dataset for the fraud demo.

Mirrors the shape of the public Kaggle "Credit Card Fraud Detection" file
(``Time``, ``V1``..``V28`` PCA components, ``Amount``, ``Class``) so the demo
API and its UI run from data versioned inside the repository instead of a
machine-local path. A fixed seed guarantees deterministic output.

This is demo data, not a substitute for the real dataset: the signal is
injected deliberately, so metrics measured on it say nothing about how a
model would score on real transactions.
"""

from __future__ import annotations

import argparse
import hashlib

import numpy as np
import pandas as pd

N_ROWS = 10000
N_COMPONENTS = 28
FRAUD_RATE = 0.02

# PCA components that carry the injected fraud signal, chosen to match the
# components that dominate on the real dataset.
SIGNAL_COMPONENTS = [4, 10, 12, 14, 17]


def _hash_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate(rows: int = N_ROWS, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    n_fraud = max(1, int(rows * FRAUD_RATE))
    labels = np.zeros(rows, dtype=np.int8)
    labels[rng.choice(rows, size=n_fraud, replace=False)] = 1
    is_fraud = labels == 1

    # Two days of transactions, ordered like the real export.
    time = np.sort(rng.uniform(0, 172_800, size=rows))

    # PCA components: standard normal, with a mean shift on the signal-carrying
    # components for fraudulent rows.
    components = rng.standard_normal((rows, N_COMPONENTS))
    for idx in SIGNAL_COMPONENTS:
        shift = rng.uniform(1.8, 3.2)
        components[is_fraud, idx - 1] -= shift

    # Fraudulent amounts skew low (card testing) with a heavy tail.
    amount = rng.lognormal(mean=3.2, sigma=1.1, size=rows)
    amount[is_fraud] = rng.lognormal(mean=2.4, sigma=1.6, size=is_fraud.sum())
    amount = np.clip(amount, 0, 100_000).round(2)

    frame = pd.DataFrame({"Time": time.round(0)})
    for i in range(1, N_COMPONENTS + 1):
        frame[f"V{i}"] = components[:, i - 1].round(6)
    frame["Amount"] = amount
    frame["Class"] = labels
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic credit card transaction data."
    )
    parser.add_argument("--rows", type=int, default=N_ROWS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="creditcard.csv")
    args = parser.parse_args()

    df = generate(args.rows, args.seed)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} rows to {args.output}")
    print(f"Fraud rate: {df['Class'].mean():.4f}")
    print(f"File SHA256: {_hash_file(args.output)}")


if __name__ == "__main__":
    main()
