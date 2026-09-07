# NIST CSF 2.0 Mapping for the Proportionate Defense Model

## Scope

This document records the compact NIST CSF 2.0 mapping used by the current implementation of the Proportionate Defense Scoring Model (`M_PDS`). It is an operational subset, not a claim of complete CSF Core coverage, certification, or conformance.

The manager-facing assessment surface contains:

- 13 NIST-mapped observations: five governance, five technical, and three human observations;
- one additional perimeter-integrity critical check; and
- the derived Shadow IT ratio `R_shadow`.

The critical gate `Omega` is derived from the backup-integrity and perimeter-integrity checks. It is not collected as an independent self-reported variable.

## Governance observations (`S_gov`)

| Variable | NIST CSF 2.0 reference | Operational role |
| --- | --- | --- |
| G1. Incident response plan | **RS.MA-01** | Establishes an executable incident-response path and coordination process. |
| G2. Vendor check | **GV.SC-06** | Supports supplier and third-party risk management. |
| G3. Cyber insurance / risk-transfer evidence | **GV.RM-04** | Records organizational risk-response and risk-tolerance context. |
| G4. Access review | **PR.AA-05** | Reviews and manages permissions, entitlements, and access authorization. |
| G5. Asset inventory | **ID.AM-02** | Tracks software, services, systems, and related assets relevant to the assessment. |

## Technical observations (`S_tech`)

| Variable | NIST CSF 2.0 reference | Operational role |
| --- | --- | --- |
| T1. Endpoint protection / monitoring | **DE.CM-09** | Monitors computing hardware, software, runtime environments, and their data for potentially adverse events. |
| T2. Patch management | **PR.PS-02** | Maintains software and installs updates according to risk. |
| T3. Backup integrity | **RC.RP-03** | Supports recovery by verifying protected backup and restoration capability; also contributes to `Omega`. |
| T4. MFA | **PR.AA-03** | Supports authentication of users, services, and hardware through appropriate authentication mechanisms. |
| T5. DNS / malicious-domain restriction | **PR.PS-05** | Restricts installation and execution of unauthorized software and access to malicious resources through protective controls. |

## Human observations (`S_human`)

| Variable | NIST CSF 2.0 reference | Operational role |
| --- | --- | --- |
| H1. Phishing measure | **PR.AT-01** | Provides a measurable awareness-related input when a controlled phishing assessment is available. |
| H2. Training frequency | **PR.AT-01** | Records general cybersecurity awareness and training activity. |
| H3. Reporting route | **PR.AT-01** | Records whether personnel know how to recognize and report suspicious activity. In the current model this remains a mapped diagnostic observation and is not an independently weighted term in the Human Factor equation. |

## Additional structural quantities

### Perimeter-integrity critical check

The current implementation includes a separate check for trivial or uncontrolled internet-facing access. Together with backup integrity, this check determines the binary critical gate `Omega`.

### Shadow IT ratio

`R_shadow` is derived from managed and unmanaged SaaS subscription counts:

```text
R_shadow = N_unmanaged / max(N_managed, 1)
```

The ratio is used by the multiplicative modifier:

```text
Psi(R_shadow) = exp(-lambda * R_shadow)
```

with `lambda = 0.5` in the reported experiments. This value is a modeling parameter, not an empirically estimated optimum.

## Interpretation boundary

This mapping deliberately narrows the assessment surface. NIST CSF 2.0 contains many outcomes that are outside the current score and may remain important in a detailed organizational assessment. The mapping should therefore be interpreted as a traceability aid for the model inputs, not as evidence that `M_PDS` implements or measures the full CSF Core.
