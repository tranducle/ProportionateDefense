# Proportionate Defense: Reproducibility Materials

[![Paper Status](https://img.shields.io/badge/status-revision-yellow)](https://github.com/tranducle/ProportionateDefense)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository contains the public reproducibility materials for:

> **Proportionate Defense: A NIST-Aligned Cyber Risk Scoring Model for Resource-Constrained Enterprises**

## Current model scope

The Proportionate Defense Scoring Model (`M_PDS`) combines:

- a transparent weighted base score over technical, human, and governance domains;
- a binary Critical Failure Constraint (`Omega`) that makes declared survival-critical failures non-compensatory; and
- a multiplicative Shadow IT modifier (`Psi`) based on unmanaged SaaS exposure.

The reported study evaluates structural score behavior on a frozen population of 1,000 synthetic SME profiles. The results do **not** establish real-world breach prediction, calibration, causal risk reduction, or empirical superiority over CIS IG1.

## Repository structure

```text
Supplementary/
├── generate_sme_data.py             # Generate new synthetic populations
├── simulate_scores.py               # Apply the M_PDS scoring formula
├── synthetic_sme_dataset.csv        # Frozen 1,000-profile dataset used in the paper
├── simulation_results.csv           # Frozen M_PDS results for that dataset
├── nist_csf_2_mapping.md            # Current compact NIST CSF 2.0 mapping
├── weighting_justification.md       # Weight rationale and sensitivity boundary
├── fig_decay_function.tex           # TikZ source for the Shadow IT decay curve
├── fig_sensitivity_heatmap.tex      # TikZ source for the sensitivity visualization
├── fig_sensitivity_heatmap.pdf      # Compiled sensitivity figure
├── fig_additive_ablation.tex        # TikZ source for paired divergence/ablation figure
└── validation/
    ├── compare_additive_baseline.py # Paired additive-baseline + ablation analysis
    ├── mechanism_robustness_check.py# Mechanism identities + weight robustness
    └── results/                     # Reproduced comparison artifacts
```

The repository intentionally excludes the journal manuscript source and author-identifying submission files. The public artifact focuses on code, data, model documentation, and reproducibility outputs.

## Requirements

```bash
python -m pip install numpy pandas
```

Python 3.8 or newer is recommended.

## Reproduce the reported M_PDS scores

From the repository root:

```bash
cd Supplementary
python simulate_scores.py \
  --input synthetic_sme_dataset.csv \
  --output simulation_results_reproduced.csv
```

The reproduced `final_risk_score` values should match `simulation_results.csv` to floating-point precision.

## Reproduce the paired additive-baseline and ablation analysis

```bash
python validation/compare_additive_baseline.py \
  --input synthetic_sme_dataset.csv \
  --existing-results simulation_results.csv \
  --outdir validation/results

python validation/mechanism_robustness_check.py \
  --input validation/results/per_profile_scores.csv \
  --outdir validation/results
```

The controlled additive comparator uses the same three domain scores and the same weighting budget as `M_PDS`. It is labeled an **IG1-style additive baseline** because CIS IG1 provides prioritized safeguards rather than an official scalar scoring equation. The comparator is therefore a controlled surrogate used to isolate the effects of `Omega` and `Psi`.

## Headline reproducibility checks

On the frozen 1,000-profile dataset, the current scripts reproduce the revised manuscript values:

| Quantity | Value |
| --- | ---: |
| Mean additive score | 65.25 |
| Mean full `M_PDS` score | 44.06 |
| Profiles changing rating band | 766 / 1,000 |
| Additive score >= 70 but full score < 50 | 107 |
| `Omega = 0` profiles | 43 |
| `Omega = 1` and `R_shadow >= 1` profiles | 219 |
| Spearman association, additive vs. full | 0.522 |

These values describe the frozen synthetic population and scoring rules only.

## Generate a new synthetic population

The frozen dataset is the source for the paper's reported values. To create a new synthetic population for sensitivity analysis without overwriting the paper dataset:

```bash
python generate_sme_data.py --seed 2026 --output synthetic_sme_dataset_generated.csv
```

Omit `--seed` for a stochastic sample. Results from a newly generated population will generally differ from the paper's frozen results.

## Model formula

```text
S_base  = 0.40*S_tech + 0.35*S_human + 0.25*S_gov
Omega   = 0 if a declared critical prerequisite fails, else 1
Psi     = exp(-0.5*R_shadow)
S_total = Omega * S_base * Psi
```

The weights and `lambda = 0.5` are modeling parameters rather than empirically estimated optima.

## NIST CSF 2.0 mapping

The current implementation uses a compact assessment surface rather than claiming full CSF Core coverage. See `Supplementary/nist_csf_2_mapping.md` for the 13 mapped observations, the perimeter-integrity check, the derived Shadow IT ratio, and the interpretation boundary.

## Data provenance

The public repository preserves the exact frozen input and scored-result artifacts used by the revised paired comparison:

```text
synthetic_sme_dataset.csv
SHA-256: bfe2ed0a1c475d6b1b1f07b36584b90f905d4719cb3868534fcdf21923036786

simulation_results.csv
SHA-256: e10c857e76c98f079696ba32857d4a69c92377dd578e4c3643e6b46d3ef4844e
```

## License

The software and repository materials are distributed under the MIT License. See [LICENSE](LICENSE).
