#!/usr/bin/env python3
"""Fail-fast checks for the frozen Proportionate Defense reproducibility package."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "validation" / "results"

EXPECTED = {
    "mean_additive": 65.24505174633856,
    "mean_full": 44.060873749364504,
    "spearman_additive_vs_full": 0.5224588612067366,
    "rating_changed_n": 766,
    "additive_ge70_to_full_critical_n": 107,
    "omega_failure_n": 43,
    "omega_ok_high_shadow_n": 219,
}


def main() -> None:
    frozen = pd.read_csv(ROOT / "simulation_results.csv")
    if len(frozen) != 1000:
        raise AssertionError(f"Expected 1000 frozen rows, found {len(frozen)}")

    report = json.loads((RESULTS / "comparison_report.json").read_text(encoding="utf-8"))
    comparison = report["comparison"]

    for key, expected in EXPECTED.items():
        actual = comparison[key]
        if isinstance(expected, float):
            if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=1e-10):
                raise AssertionError(f"{key}: expected {expected}, got {actual}")
        elif actual != expected:
            raise AssertionError(f"{key}: expected {expected}, got {actual}")

    robustness = pd.read_csv(RESULTS / "weight_robustness.csv")
    expected_names = {"default", "equal", "tech_heavy", "human_centric"}
    if set(robustness["weighting"]) != expected_names:
        raise AssertionError("Unexpected weight-robustness configurations")

    print("PASS: frozen reproducibility checks match the revised manuscript values.")


if __name__ == "__main__":
    main()
