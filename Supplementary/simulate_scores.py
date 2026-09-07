#!/usr/bin/env python3
"""Apply the Proportionate Defense scoring model to an SME profile CSV."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import pandas as pd

W_TECH = 0.40
W_HUMAN = 0.35
W_GOV = 0.25
SHADOW_LAMBDA = 0.5


def calculate_score(row: pd.Series) -> float:
    """Calculate the final M_PDS score for one SME profile."""
    omega = 0.0 if bool(row["has_critical_failure"]) else 1.0
    base_score = (
        W_TECH * row["tech_score"]
        + W_HUMAN * row["human_score"]
        + W_GOV * row["gov_score"]
    )
    psi = math.exp(-SHADOW_LAMBDA * row["shadow_it_ratio"])
    return omega * base_score * psi


def get_rating(score: float) -> str:
    if score >= 90:
        return "Resilient"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "At Risk"
    return "Critical"


def run_simulation(input_path: Path, output_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    required = {
        "id",
        "sector",
        "size",
        "tech_score",
        "human_score",
        "gov_score",
        "shadow_it_ratio",
        "has_critical_failure",
    }
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["final_risk_score"] = df.apply(calculate_score, axis=1)
    df["rating"] = df["final_risk_score"].map(get_rating)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("synthetic_sme_dataset.csv"),
        help="Input SME profile CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("simulation_results_reproduced.csv"),
        help="Output scored CSV",
    )
    args = parser.parse_args()

    results = run_simulation(args.input, args.output)
    print(f"Scored {len(results)} profiles -> {args.output}")
    print(results["final_risk_score"].describe().to_string())
    print("\nRating distribution:")
    print(results["rating"].value_counts().to_string())


if __name__ == "__main__":
    main()
