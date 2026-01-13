# Justification of Model Weighting Distribution

## 1. The Proposed Distribution
The Composite Risk Score ($S_{total}$) uses the following weighting vector:
$$ W = [w_{tech}, w_{human}, w_{gov}] = [0.40, 0.35, 0.25] $$

## 2. Theoretical Basis & Evidence

### 2.1 Technical Security ($w_T = 0.40$)
**Rationale:** Technical controls represent the "hard" exterior of the organization. While human error is a common *entry vector*, technical controls (firewalls, patching, EDR) are the only mechanism to *stop* an active attack once initiated.
*   **Evidence:**
    *   **NIST CSF Alignment:** The "Protect" and "Detect" functions are predominantly technical. Since our model is "NIST-Aligned," technical controls must hold the plurality of weight.
    *   **Automation:** Technical controls function 24/7 without fatigue, unlike human monitoring.

### 2.2 Human Factor ($w_H = 0.35$)
**Rationale:** This weight is significantly higher than in traditional enterprise models (which often weight GRC higher). This reflects the specific reality of SMEs where the "Human Firewall" is often the *only* line of defense against social engineering.
*   **Evidence:**
    *   **Boletsis et al. (2021):** Emphasize that SMEs "rarely conduct thorough risk assessment" and rely on "socio-technical" factors.
    *   **Industry Data:** Verizon DBIR consistently attributes ~74-82% of breaches to the "Human Element" (Errors + Social Engineering).
    *   **SME Context:** In flat hierarchies (noted in `sme_risk_factors.md`), a single employee often has administrative privileges, magnifying the impact of a single human error.

### 2.3 Governance & Compliance ($w_G = 0.25$)
**Rationale:** Governance is weighted lowest not because it is unimportant, but because it is a *lagging indicator* of security in SMEs. A policy document does not stop ransomware; an offline backup (Technical) does.
*   **Evidence:**
    *   **NIS2 Governance Design (2025):** Notes that "formal compliance is burdensome" for micro-SMEs. Over-weighting governance would bias the score against smaller, agile firms that might be technically secure but document-poor.
    *   **"Proportionate" Defense:** To be "proportionate" (Title), we must prioritize *action* (Tech/Human) over *documentation* (Gov).

## 3. Sensitivity Analysis Plan
To ensure robustness, we will perform a sensitivity analysis in **Phase 4 (Simulation)**:
1.  **Scenario A (Tech-Heavy):** Shift weights to $[0.60, 0.20, 0.20]$.
    *   *Hypothesis:* Will over-score SMEs with good tools but poor culture (the "Maginot Line" effect).
2.  **Scenario B (Human-Centric):** Shift weights to $[0.20, 0.60, 0.20]$.
    *   *Hypothesis:* Will over-score SMEs with great awareness but obsolete hardware.

## 4. Conclusion
The $[0.40, 0.35, 0.25]$ distribution represents a **"Survival-First"** approach tailored to the resource-constrained SME, prioritizing the actual capabilities to resist attacks (Tech + Human) over the administrative layer (Gov).
