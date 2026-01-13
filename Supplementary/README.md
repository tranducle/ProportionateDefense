# Supplementary Materials

**Manuscript:** Proportionate Defense: A NIST-Aligned Cyber Risk Scoring Model for Resource-Constrained Enterprises

## Contents

### 1. Simulation Code

- `simulate_scores.py` - Monte Carlo simulation engine implementing the $\mathcal{M}_{PDS}$ scoring algorithm
- `generate_sme_data.py` - Synthetic SME profile generator

### 2. Dataset

- `synthetic_sme_dataset.csv` - 1,000 synthetic SME profiles with the following columns:
  - `id`: Unique identifier
  - `sector`: FinTech, Retail, Manufacturing, or Services
  - `size`: Micro (<10), Small (10-50), or Medium (50-250)
  - `tech_score`: Technical security maturity (0-100)
  - `human_score`: Human factor score (0-100)
  - `gov_score`: Governance maturity (0-100)
  - `shadow_it_ratio`: Unmanaged/Managed asset ratio
  - `has_critical_failure`: Boolean flag for Ω constraint

### 3. Parameter Justification

- `weighting_justification.md` - Theoretical basis for the [0.40, 0.35, 0.25] weighting vector
- `nist_csf_2_mapping.md` - Complete mapping of model variables to NIST CSF 2.0 subcategories

### 4. TikZ Figures

- `fig_decay_function.tex` - LaTeX/TikZ source for the Shadow IT Decay Function curve
- `fig_sensitivity_heatmap.tex` - Sensitivity analysis visualization

## Usage

To reproduce the simulation results:

```bash
# Generate synthetic dataset
python generate_sme_data.py

# Run Monte Carlo simulation
python simulate_scores.py
```

## Requirements

- Python 3.8+
- pandas
- numpy

## License

Supplementary materials are provided for peer review purposes.

---
*Prepared: 2026-01-12*
