#!/usr/bin/env python3
"""Check deterministic mechanism identities and domain-weight robustness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

WEIGHTS = {
    "default": (0.40, 0.35, 0.25),
    "equal": (0.33, 0.33, 0.34),
    "tech_heavy": (0.50, 0.30, 0.20),
    "human_centric": (0.30, 0.45, 0.25),
}
LAMBDA = 0.5


def rating(score: float) -> str:
    if score >= 90:
        return "Resilient"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "At Risk"
    return "Critical"


def spearman(x: pd.Series, y: pd.Series) -> float:
    return float(
        np.corrcoef(
            x.rank(method="average").to_numpy(float),
            y.rank(method="average").to_numpy(float),
        )[0, 1]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="per_profile_scores.csv")
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()

    d = pd.read_csv(args.input)
    required = [
        "tech_score", "human_score", "gov_score", "shadow_it_ratio", "omega",
        "psi", "additive_score", "omega_only_score", "psi_only_score", "mpds_score",
    ]
    missing = [c for c in required if c not in d.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    omega0 = d.omega.eq(0)
    omega1 = d.omega.eq(1)
    high_shadow = d.shadow_it_ratio.ge(1.0)

    factorial_interaction = (
        d.mpds_score - d.omega_only_score - d.psi_only_score + d.additive_score
    )
    args.outdir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "id": d.id,
            "omega": d.omega,
            "shadow_it_ratio": d.shadow_it_ratio,
            "factorial_interaction": factorial_interaction,
        }
    ).to_csv(args.outdir / "factorial_interaction.csv", index=False)

    mechanism = {
        "omega0_n": int(omega0.sum()),
        "omega1_n": int(omega1.sum()),
        "omega0_full_zero_max_abs_error": float(np.abs(d.loc[omega0, "mpds_score"]).max()),
        "omega0_omega_only_zero_max_abs_error": float(
            np.abs(d.loc[omega0, "omega_only_score"]).max()
        ),
        "omega1_full_equals_psi_only_max_abs_error": float(
            np.abs(d.loc[omega1, "mpds_score"] - d.loc[omega1, "psi_only_score"]).max()
        ),
        "omega1_additive_equals_omega_only_max_abs_error": float(
            np.abs(d.loc[omega1, "additive_score"] - d.loc[omega1, "omega_only_score"]).max()
        ),
        "omega1_high_shadow_n": int((omega1 & high_shadow).sum()),
        "omega1_high_shadow_full_critical_n": int(
            (omega1 & high_shadow & d.mpds_score.lt(50)).sum()
        ),
        "omega1_high_shadow_additive_ge50_to_full_critical_n": int(
            (omega1 & high_shadow & d.additive_score.ge(50) & d.mpds_score.lt(50)).sum()
        ),
        "omega1_high_shadow_additive_ge70_to_full_critical_n": int(
            (omega1 & high_shadow & d.additive_score.ge(70) & d.mpds_score.lt(50)).sum()
        ),
        "factorial_interaction_nonzero_n": int((np.abs(factorial_interaction) > 1e-12).sum()),
    }

    rows = []
    for name, (wt, wh, wg) in WEIGHTS.items():
        additive = wt * d.tech_score + wh * d.human_score + wg * d.gov_score
        full = d.omega * additive * np.exp(-LAMBDA * d.shadow_it_ratio)
        add_rating = additive.map(rating)
        full_rating = full.map(rating)
        rows.append(
            {
                "weighting": name,
                "w_tech": wt,
                "w_human": wh,
                "w_gov": wg,
                "mean_additive": float(additive.mean()),
                "mean_full": float(full.mean()),
                "mean_reduction": float((additive - full).mean()),
                "spearman_additive_vs_full": spearman(additive, full),
                "rating_changed_n": int((add_rating != full_rating).sum()),
                "rating_changed_pct": float(100 * (add_rating != full_rating).mean()),
                "additive_ge70_to_full_critical_n": int(
                    (additive.ge(70) & full.lt(50)).sum()
                ),
                "full_critical_n": int(full.lt(50).sum()),
                "full_critical_pct": float(100 * full.lt(50).mean()),
            }
        )

    pd.DataFrame(rows).to_csv(args.outdir / "weight_robustness.csv", index=False)
    report = {
        "mechanism_identity": mechanism,
        "weight_robustness": rows,
        "claim_boundary": (
            "Mechanism identities and weight sensitivity on the frozen synthetic profiles only; "
            "no predictive-validity claim."
        ),
    }
    (args.outdir / "mechanism_robustness_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
