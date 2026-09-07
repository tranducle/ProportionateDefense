#!/usr/bin/env python3
"""Generate synthetic SME profiles for Proportionate Defense experiments.

The paper's reported results use the frozen ``synthetic_sme_dataset.csv``
shipped with this repository. This generator is provided for sensitivity and
replication studies with newly sampled populations. Use ``--seed`` when a
repeatable new sample is required.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

N_SAMPLES = 1000
SECTORS = ["FinTech", "Retail", "Manufacturing", "Services"]
SIZES = ["Micro (<10)", "Small (10-50)", "Medium (50-250)"]
P_SECTOR = [0.20, 0.30, 0.20, 0.30]
P_SIZE = [0.50, 0.35, 0.15]


def generate_dataset(n_samples: int = N_SAMPLES, seed: Optional[int] = None) -> pd.DataFrame:
    """Generate a synthetic SME population using the manuscript distributions."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(index=range(n_samples))
    df["id"] = [f"sme_{i:04d}" for i in range(n_samples)]

    # Sector and size labels are sampled independently of score inputs.
    df["sector"] = rng.choice(SECTORS, n_samples, p=P_SECTOR)
    df["size"] = rng.choice(SIZES, n_samples, p=P_SIZE)

    mean = [70, 55]
    cov = [[150, 60], [60, 200]]
    tech_scores, human_scores = rng.multivariate_normal(mean, cov, n_samples).T
    gov_scores = rng.beta(a=5, b=2, size=n_samples) * 100

    df["tech_score"] = np.clip(tech_scores, 10, 100)
    df["human_score"] = np.clip(human_scores, 0, 90)
    df["gov_score"] = np.clip(gov_scores, 20, 100)

    df["shadow_it_ratio"] = rng.lognormal(mean=-0.5, sigma=0.7, size=n_samples)
    df["has_critical_failure"] = rng.choice(
        [True, False], n_samples, p=[0.05, 0.95]
    )
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=N_SAMPLES, help="Number of profiles")
    parser.add_argument("--seed", type=int, default=None, help="Optional NumPy RNG seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("synthetic_sme_dataset_generated.csv"),
        help="Output CSV. The frozen paper dataset is not overwritten by default.",
    )
    args = parser.parse_args()

    df = generate_dataset(args.rows, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Generated {len(df)} profiles -> {args.output}")
    if args.seed is None:
        print("No seed supplied; this generated population is intentionally stochastic.")
    else:
        print(f"Seed: {args.seed}")


if __name__ == "__main__":
    main()
