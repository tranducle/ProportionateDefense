# Comparative Validation and Ablation Package

This directory reproduces the paired structural comparison added during manuscript revision.

## Scope

The analysis compares four deterministic score variants on the same frozen 1,000 synthetic SME profiles:

1. **IG1-style additive baseline**: `S_add`
2. **Omega-only**: `Omega * S_add`
3. **Psi-only**: `S_add * Psi(R_shadow)`
4. **Full M_PDS**: `Omega * S_add * Psi(R_shadow)`

The additive baseline is a controlled checklist-style surrogate. CIS Implementation Group 1 does not define an official scalar organizational score, so these results must not be interpreted as an empirical benchmark against an official CIS scoring equation.

## Run the paired comparison

From `Supplementary/`:

```bash
python validation/compare_additive_baseline.py \
  --input synthetic_sme_dataset.csv \
  --existing-results simulation_results.csv \
  --outdir validation/results
```

The script verifies that recomputation of the full model matches the frozen `simulation_results.csv` to floating-point precision before producing the comparative outputs.

## Run mechanism and weight checks

```bash
python validation/mechanism_robustness_check.py \
  --input validation/results/per_profile_scores.csv \
  --outdir validation/results
```

This checks the exact mechanism identities implied by the frozen formulas and repeats the comparison for the default, equal, technology-heavy, and human-centric weight vectors used in the revised manuscript.

## Run the frozen-result check

```bash
python validation/validate_reproduction.py
```

The check fails if the key frozen metrics differ from the revised manuscript values.

## Generated files

- `results/per_profile_scores.csv`
- `results/ablation_summary.csv`
- `results/rating_migration.csv`
- `results/comparison_report.json`
- `results/factorial_interaction.csv`
- `results/weight_robustness.csv`
- `results/mechanism_robustness_report.json`

## Headline checks

The frozen data should reproduce:

- mean additive score: **65.2451**
- mean full score: **44.0609**
- Spearman association: **0.52246**
- rating changes: **766 / 1,000**
- additive score >= 70 to full Critical: **107**
- `Omega = 0`: **43** profiles
- `Omega = 1` and `R_shadow >= 1`: **219** profiles
- among the high-Shadow-IT subset, additive >= 50 to full Critical: **203**
- among the high-Shadow-IT subset, additive >= 70 to full Critical: **55**

## Evidence boundary

These outputs characterize how the scoring rules behave on the frozen synthetic population. They do not establish real-world predictive accuracy, calibration, causal security improvement, or superiority over CIS IG1.
