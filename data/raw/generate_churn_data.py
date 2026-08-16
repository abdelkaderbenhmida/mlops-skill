#!/usr/bin/env python3
"""Generate a realistic synthetic telecom customer churn dataset.

Outputs ~7000 rows to ``data/raw/dataset.csv``. Includes a sensitive
attribute (``gender``) used later for the fairness checks. A fixed random
seed guarantees deterministic, reproducible output.
"""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

N_ROWS = 7000
CONTRACTS = ["month-to-month", "one_year", "two_year"]
PAYMENTS = ["electronic_check", "mailed_check", "bank_transfer", "credit_card"]
REGIONS = ["north", "south", "east", "west"]


def _hash_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate(n_rows: int = N_ROWS, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    customer_id = np.arange(1, n_rows + 1, dtype=np.int64)
    base_ts = datetime(2023, 1, 1)
    timestamps = pd.to_datetime(
        [base_ts + timedelta(days=int(d)) for d in rng.integers(0, 730, n_rows)]
    )

    age = rng.integers(18, 71, n_rows)
    gender = rng.choice(["M", "F"], n_rows, p=[0.52, 0.48])
    region = rng.choice(REGIONS, n_rows)
    tenure_months = rng.integers(0, 73, n_rows)
    monthly_charges = np.round(rng.uniform(20.0, 120.0, n_rows), 2)
    num_services = rng.integers(1, 7, n_rows)
    contract_type = rng.choice(CONTRACTS, n_rows, p=[0.55, 0.25, 0.20])
    payment_method = rng.choice(PAYMENTS, n_rows, p=[0.34, 0.22, 0.24, 0.20])
    support_tickets = rng.poisson(1.2, n_rows).clip(0, 15)
    avg_call_minutes = np.round(rng.uniform(0.0, 500.0, n_rows), 1)
    has_online_backup = rng.integers(0, 2, n_rows)
    has_device_protection = rng.integers(0, 2, n_rows)
    has_tech_support = rng.integers(0, 2, n_rows)

    # Churn probability model: higher risk for short tenure, high charges,
    # month-to-month contracts, electronic check, more support tickets.
    logit = (
        -3.0
        - 0.08 * tenure_months
        + 0.018 * monthly_charges
        + (contract_type == "month-to-month") * 1.6
        + (payment_method == "electronic_check") * 0.5
        + 0.35 * support_tickets
        - 0.9 * has_tech_support
        + 0.2 * (num_services - 3)
        + (age > 60) * 0.4
    )
    prob = 1.0 / (1.0 + np.exp(-logit))
    # Mild correlation between gender and the target so fairness checks are
    # interesting, while churn is still explainable by the business features.
    prob = np.clip(prob + (gender == "M") * 0.02, 0.0, 1.0)
    churn = (rng.uniform(0, 1, n_rows) < prob).astype(int)

    df = pd.DataFrame(
        {
            "customer_id": customer_id,
            "timestamp": timestamps,
            "age": age,
            "gender": gender,
            "region": region,
            "tenure_months": tenure_months,
            "monthly_charges": monthly_charges,
            "total_charges": np.round(monthly_charges * tenure_months, 2),
            "num_services": num_services,
            "contract_type": contract_type,
            "payment_method": payment_method,
            "support_tickets": support_tickets,
            "avg_call_minutes": avg_call_minutes,
            "has_online_backup": has_online_backup,
            "has_device_protection": has_device_protection,
            "has_tech_support": has_tech_support,
            "churn": churn,
        }
    )
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic churn data.")
    parser.add_argument("--rows", type=int, default=N_ROWS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="dataset.csv")
    args = parser.parse_args()

    df = generate(args.rows, args.seed)
    df.to_csv(args.output, index=False)
    print(f"Wrote {len(df)} rows to {args.output}")
    print(f"Target balance: {df['churn'].mean():.3f}")
    print(f"Time period: {df['timestamp'].min()} -> {df['timestamp'].max()}")
    print(f"File SHA256: {_hash_file(args.output)}")


if __name__ == "__main__":
    main()
