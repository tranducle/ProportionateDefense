# Supplementary Materials

These files support the revised manuscript **Proportionate Defense: A NIST-Aligned Cyber Risk Scoring Model for Resource-Constrained Enterprises**.

## Frozen paper artifacts

- `synthetic_sme_dataset.csv`: the 1,000-profile synthetic population used for the reported analyses.
- `simulation_results.csv`: the corresponding `M_PDS` scores and rating bands.

The frozen artifacts are kept separate from newly generated samples so that the manuscript results remain directly reproducible.

## Core scripts

### `simulate_scores.py`

Applies the current scoring rule:

```text
S_total = Omega * (0.40*S_tech + 0.35*S_human + 0.25*S_gov) * exp(-0.5*R_shadow)
```

Example:

```bash
python simulate_scores.py \
  --input synthetic_sme_dataset.csv \
  --output simulation_results_reproduced.csv
```

### `generate_sme_data.py`

Generates a new synthetic population using the distributions described in the manuscript. It does not overwrite the frozen paper dataset by default.

```bash
python generate_sme_data.py --seed 2026 --output synthetic_sme_dataset_generated.csv
```

Use a fixed seed when repeatability of a newly generated population is required.

## Comparative validation introduced during revision

The revised manuscript adds a paired comparison with a controlled IG1-style additive baseline, plus `Omega`-only and `Psi`-only ablations.

Run:

```bash
python validation/compare_additive_baseline.py \
  --input synthetic_sme_dataset.csv \
  --existing-results simulation_results.csv \
  --outdir validation/results

python validation/mechanism_robustness_check.py \
  --input validation/results/per_profile_scores.csv \
  --outdir validation/results
```

The comparator is a controlled additive surrogate. It is not an official CIS IG1 numerical score.

## Documentation

- `nist_csf_2_mapping.md`: current compact NIST CSF 2.0 traceability mapping and scope boundary.
- `weighting_justification.md`: current parameter rationale and weight-sensitivity interpretation.

## Figure sources

- `fig_decay_function.tex`: TikZ source for the Shadow IT decay function.
- `fig_sensitivity_heatmap.tex`: TikZ source for the current sensitivity visualization.
- `fig_sensitivity_heatmap.pdf`: compiled sensitivity figure.
- `fig_additive_ablation.tex`: TikZ source for the paired divergence and component-ablation figure added during revision.
- `fig_additive_ablation.pdf`: compiled paired divergence and component-ablation figure.

## Requirements

```bash
python -m pip install numpy pandas
```

## Interpretation boundary

The repository reproduces structural results on the stated synthetic data and scoring rules. It does not provide evidence of real-world breach prediction, calibration, causal security improvement, or deployment effectiveness.
