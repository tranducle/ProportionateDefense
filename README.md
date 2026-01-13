# Supplementary Materials: Proportionate Defense

[![Paper Status](https://img.shields.io/badge/status-under%20review-yellow)](https://arxiv.org/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains the **supplementary materials** (simulation code and dataset) for the research paper:

> **Proportionate Defense: A NIST-Aligned Cyber Risk Scoring Model for Resource-Constrained Enterprises**

## Abstract

Small and Medium Enterprises (SMEs) face a "Security Paradox": they are high-value targets for cybercriminals but lack the resources for enterprise-grade defense. This paper proposes the **Proportionate Defense Scoring Model (M_PDS)**, a lightweight, NIST-aligned framework designed for organizational survival. We introduce:

- A **Critical Failure Constraint (Ω)** to enforce a survival hierarchy
- A novel **Shadow IT Decay Function (Ψ)** to model non-linear risk of unmanaged SaaS adoption
- A **Behavioral Weighting Vector** optimized for flat SME hierarchies

## Repository Structure

```
├── Supplementary/               # Reproducibility materials
│   ├── simulate_scores.py       # Monte Carlo simulation engine
│   ├── generate_sme_data.py     # Synthetic SME profile generator
│   ├── synthetic_sme_dataset.csv # 1,000 SME profiles
│   ├── nist_csf_2_mapping.md    # NIST CSF 2.0 variable mapping
│   ├── weighting_justification.md # Domain weight rationale
│   ├── fig_decay_function.tex   # TikZ source for decay curve
│   └── fig_sensitivity_heatmap.tex # TikZ source for heatmap
│
└── README.md                    # This file
```

## Quick Start

### Requirements

```bash
pip install numpy pandas
```

### Reproduce Simulation Results

```bash
cd Supplementary

# Generate synthetic SME dataset
python generate_sme_data.py

# Run Monte Carlo simulation (N=1000)
python simulate_scores.py
```

## Key Model Components

### 1. Total Risk Score Formula

```
S_total = Ω × (Σ w_i × S_i) × Ψ(R_shadow)
```

Where:

- **Ω ∈ {0, 1}**: Critical Failure Constraint (binary kill-switch)
- **w = [0.40, 0.35, 0.25]**: Domain weighting vector [Tech, Human, Gov]
- **Ψ(x) = e^(-λx)**: Shadow IT Decay Function (λ=0.5)

### 2. Critical Controls (C_crit)

The model enforces two survival-critical controls:

- **Immutable Backups**: Recovery capability against ransomware
- **Perimeter Integrity**: Prevention of trivial remote access (e.g., open RDP)

If either control is missing, Ω = 0 → S_total = 0.

## Dataset Description

The `synthetic_sme_dataset.csv` contains 1,000 profiles with:

| Column | Description |
|--------|-------------|
| `id` | Unique identifier |
| `sector` | FinTech (20%), Retail (30%), Manufacturing (20%), Services (30%) |
| `size` | Micro (<10), Small (10-50), Medium (50-250) |
| `tech_score` | Technical security maturity (0-100) |
| `human_score` | Human factor score (0-100) |
| `gov_score` | Governance maturity (0-100) |
| `shadow_it_ratio` | Unmanaged/Managed asset ratio |
| `has_critical_failure` | Boolean flag for Ω constraint |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
