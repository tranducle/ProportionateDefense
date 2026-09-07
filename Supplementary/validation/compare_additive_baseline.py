#!/usr/bin/env python3
"""Paired additive-baseline and component-ablation analysis for M_PDS.

The additive comparator is a controlled surrogate that uses the same three
M_PDS domain scores and weights. It is not an official CIS IG1 scoring formula.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

W_TECH = 0.40
W_HUMAN = 0.35
W_GOV = 0.25
LAMBDA = 0.5
EXPECTED_ROWS = 1000


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rating(score: float) -> str:
    if score >= 90:
        return "Resilient"
    if score >= 70:
        return "Good"
    if score >= 50:
        return "At Risk"
    return "Critical"


def spearman(x: pd.Series, y: pd.Series) -> float:
    rx = x.rank(method="average")
    ry = y.rank(method="average")
    return float(np.corrcoef(rx.to_numpy(float), ry.to_numpy(float))[0, 1])


def summarize_variant(df: pd.DataFrame, col: str, name: str) -> dict:
    s = df[col]
    r = s.map(rating)
    return {
        "variant": name,
        "mean": float(s.mean()),
        "median": float(s.median()),
        "std": float(s.std(ddof=1)),
        "min": float(s.min()),
        "max": float(s.max()),
        "critical_n": int((r == "Critical").sum()),
        "critical_pct": float(100 * (r == "Critical").mean()),
        "at_risk_n": int((r == "At Risk").sum()),
        "good_n": int((r == "Good").sum()),
        "resilient_n": int((r == "Resilient").sum()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--existing-results", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    existing = pd.read_csv(args.existing_results)
    required = [
        "id", "sector", "size", "tech_score", "human_score", "gov_score",
        "shadow_it_ratio", "has_critical_failure",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if len(df) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS} rows, found {len(df)}")
    if not df["id"].equals(existing["id"]):
        raise ValueError("Stored input and scored-result IDs/order differ")

    base = W_TECH * df.tech_score + W_HUMAN * df.human_score + W_GOV * df.gov_score
    omega = (~df.has_critical_failure.astype(bool)).astype(int)
    psi = np.exp(-LAMBDA * df.shadow_it_ratio)

    out = df.copy()
    out["omega"] = omega
    out["psi"] = psi
    out["additive_score"] = base
    out["omega_only_score"] = omega * base
    out["psi_only_score"] = base * psi
    out["mpds_score"] = omega * base * psi

    max_error = float(np.max(np.abs(out.mpds_score - existing.final_risk_score)))
    if max_error > 1e-10:
        raise ValueError(f"M_PDS recomputation mismatch: max abs error={max_error}")

    for col in ["additive_score", "omega_only_score", "psi_only_score", "mpds_score"]:
        out[col.replace("_score", "_rating")] = out[col].map(rating)

    out["additive_rank"] = out.additive_score.rank(method="average", ascending=False)
    out["mpds_rank"] = out.mpds_score.rank(method="average", ascending=False)
    out["absolute_rank_shift"] = (out.additive_rank - out.mpds_rank).abs()

    args.outdir.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.outdir / "per_profile_scores.csv", index=False)

    variants = [
        ("IG1-style additive baseline", "additive_score"),
        ("Omega-only", "omega_only_score"),
        ("Psi-only", "psi_only_score"),
        ("Full M_PDS", "mpds_score"),
    ]
    summary = pd.DataFrame([summarize_variant(out, c, n) for n, c in variants])
    summary.to_csv(args.outdir / "ablation_summary.csv", index=False)

    order = ["Critical", "At Risk", "Good", "Resilient"]
    migration = pd.crosstab(out.additive_rating, out.mpds_rating).reindex(
        index=order, columns=order, fill_value=0
    )
    migration.to_csv(args.outdir / "rating_migration.csv")

    omega0 = out.omega.eq(0)
    omega1 = out.omega.eq(1)
    high_shadow = out.shadow_it_ratio.ge(1.0)
    add_ge50 = out.additive_score.ge(50)
    add_ge70 = out.additive_score.ge(70)
    full_critical = out.mpds_score.lt(50)

    report = {
        "baseline_name": "IG1-style additive baseline",
        "baseline_boundary": "Controlled additive surrogate; not an official CIS numerical score.",
        "input": {
            "rows": int(len(df)),
            "input_sha256": sha256_file(args.input),
            "existing_results_sha256": sha256_file(args.existing_results),
            "max_abs_recomputation_error": max_error,
        },
        "comparison": {
            "mean_additive": float(out.additive_score.mean()),
            "mean_full": float(out.mpds_score.mean()),
            "spearman_additive_vs_full": spearman(out.additive_score, out.mpds_score),
            "rating_changed_n": int((out.additive_rating != out.mpds_rating).sum()),
            "rating_changed_pct": float(100 * (out.additive_rating != out.mpds_rating).mean()),
            "additive_ge70_to_full_critical_n": int((add_ge70 & full_critical).sum()),
            "omega_failure_n": int(omega0.sum()),
            "omega_failure_additive_ge50_n": int((omega0 & add_ge50).sum()),
            "omega_failure_additive_ge70_n": int((omega0 & add_ge70).sum()),
            "omega_ok_high_shadow_n": int((omega1 & high_shadow).sum()),
            "omega_ok_high_shadow_additive_ge50_to_full_critical_n": int(
                (omega1 & high_shadow & add_ge50 & full_critical).sum()
            ),
            "omega_ok_high_shadow_additive_ge70_to_full_critical_n": int(
                (omega1 & high_shadow & add_ge70 & full_critical).sum()
            ),
            "omega_ok_high_shadow_mean_additive": float(
                out.loc[omega1 & high_shadow, "additive_score"].mean()
            ),
            "omega_ok_high_shadow_mean_full": float(
                out.loc[omega1 & high_shadow, "mpds_score"].mean()
            ),
            "median_abs_rank_shift": float(out.absolute_rank_shift.median()),
            "p95_abs_rank_shift": float(out.absolute_rank_shift.quantile(0.95)),
            "max_abs_rank_shift": float(out.absolute_rank_shift.max()),
        },
        "claim_boundary": [
            "These are structural comparisons on the frozen synthetic population.",
            "They do not establish breach prediction, calibration, causality, or superiority over CIS IG1.",
        ],
    }
    (args.outdir / "comparison_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
