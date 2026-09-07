# Weighting Rationale for the Proportionate Defense Model

## Current weighting vector

The reported implementation uses:

```text
W = [w_tech, w_human, w_gov] = [0.40, 0.35, 0.25]
```

These values are modeling parameters. They are not presented as empirically optimal weights.

## Technical domain (`w_tech = 0.40`)

The technical domain receives the largest share because the model is intended to preserve the effect of controls that operate continuously and can directly interrupt or contain technical compromise. The current technical observations include endpoint protection/monitoring, patch management, backup integrity, MFA, and DNS or malicious-domain restriction.

The value `0.40` is a design choice rather than an estimate learned from incident data.

## Human domain (`w_human = 0.35`)

The human-domain weight reflects the prominence of the human element in breach reporting and prior socio-technical SME cybersecurity research. In small organizations, individual users may also hold broad access or administrative privileges, which increases the practical importance of phishing susceptibility, training, and reporting behavior.

The current Human Factor equation uses a controlled phishing failure measure when available and normalized training frequency. The mapped reporting observation remains diagnostic and is not added as a separate weighted term in the current implementation.

## Governance domain (`w_gov = 0.25`)

Governance remains part of the base score because incident planning, supplier review, risk-transfer evidence, access review, and asset inventory affect how an SME prepares for and manages cyber risk. The current model assigns governance a smaller share than the technical and human domains to keep the compact score focused on operational security conditions while still retaining governance visibility.

This value is likewise a modeling choice rather than an empirical estimate of the marginal effect of governance activity on breach probability or loss.

## Sensitivity analysis

The revised analysis evaluates the default vector alongside three alternatives:

| Configuration | `w_tech` | `w_human` | `w_gov` |
| --- | ---: | ---: | ---: |
| Default | 0.40 | 0.35 | 0.25 |
| Equal | 0.33 | 0.33 | 0.34 |
| Technology-heavy | 0.50 | 0.30 | 0.20 |
| Human-centric | 0.30 | 0.45 | 0.25 |

On the frozen 1,000-profile synthetic population, the qualitative divergence between the additive comparator and the full model remains similar across these configurations. The analysis is intended to characterize sensitivity, not identify an optimal weighting vector.

The exact outputs are reproduced by:

```bash
python validation/mechanism_robustness_check.py \
  --input validation/results/per_profile_scores.csv \
  --outdir validation/results
```

## Interpretation boundary

The weights should be recalibrated before operational deployment when suitable empirical incident, claims, or field data are available. The current study supports statements about score behavior under the stated synthetic assumptions, not causal claims about the security effect of any particular weight.
