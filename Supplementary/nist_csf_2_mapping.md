# NIST CSF 2.0 Alignment Matrix for Proportionate Defense Model

**Status:** Draft v1.0
**Target Journal:** IEEE Transactions on Information Forensics and Security / Computers & Security
**Framework Version:** NIST CSF 2.0 (Feb 2024)

## 1. Abstract of Alignment
This document formalizes the mapping between the variables of the *Proportionate Defense Scoring Model* ($\mathcal{M}_{PDS}$) and the Categories/Subcategories of the NIST Cybersecurity Framework 2.0. By selecting a high-impact *subset* of NIST controls, we demonstrate how resource-constrained SMEs can achieve "Functional Alignment" without the administrative overhead of full "Comprehensive Compliance."

## 2. The NIST CSF 2.0 Core Functions
The model covers all six functions of NIST CSF 2.0, distributed across our three scoring domains:
1.  **GOVERN (GV)** $\rightarrow$ Mapped to $S_{gov}$
2.  **IDENTIFY (ID)** $\rightarrow$ Mapped to $S_{gov}$ (Asset Awareness)
3.  **PROTECT (PR)** $\rightarrow$ Mapped to $S_{tech}$ and $S_{human}$
4.  **DETECT (DE)** $\rightarrow$ Mapped to $S_{tech}$
5.  **RESPOND (RS)** $\rightarrow$ Mapped to $S_{gov}$ (Planning)
6.  **RECOVER (RC)** $\rightarrow$ Mapped to $S_{tech}$ (Backups)

---

## 3. Detailed Variable Mapping

### 3.1 Domain A: Governance & Process ($S_{gov}$)
*Objective:* Establish the organizational context and risk management strategy (NIST Functions: GOVERN, IDENTIFY, RESPOND).

| Model Variable | NIST 2.0 Reference | Subcategory Description | Justification for SME Inclusion |
| :--- | :--- | :--- | :--- |
| **G1. Incident Response Plan** | **GV.OC-04** | "Critical mission functions and mission essential functions are identified and prioritized." | Essential. SMEs fail not because of the breach, but the chaotic response. A simple 1-page "Call List" satisfies this for Micro-SMEs. |
| **G1. Incident Response Plan** | **RS.MA-01** | "Incident response plan is executed... in coordination with relevant third parties." | Ensures the plan isn't just a document but an actionable logic flow. |
| **G2. Vendor Risk Check** | **GV.SC-06** | "Supply chain risks are integrated into the organization’s cybersecurity risk management strategy." | Addresses the "Supply Chain" risk factor. Requires a simple "Red/Yellow/Green" rating for vendors. |
| **G3. Cyber Insurance** | **GV.RM-04** | "Strategic direction describes the organization’s risk appetite and risk tolerance." | Insurance is the primary mechanism for *Risk Transfer* in SMEs, acting as a financial safety net. |
| **G4. Access Review** | **PR.AA-01** | "Identities and credentials are managed." | Periodic review prevents "privilege creep," a common issue in flat hierarchies. |
| **G5. Asset Inventory** | **ID.AM-01** | "Inventories of hardware... are maintained." | You cannot defend what you cannot see. This is the foundation of the Shadow IT penalty logic. |

### 3.2 Domain B: Technical Safeguards ($S_{tech}$)
*Objective:* Implement static defenses and automated sensing capabilities (NIST Functions: PROTECT, DETECT, RECOVER).

| Model Variable | NIST 2.0 Reference | Subcategory Description | Justification for SME Inclusion |
| :--- | :--- | :--- | :--- |
| **T1. Endpoint Protection** | **PR.PS-08** | "Platforms are managed to reduce the attack surface." | Automated block-and-tackle (EDR/AV) is the minimum viable defense against commodity malware. |
| **T2. Patch Management** | **PR.PS-02** | "Software is maintained and replaced... and updates are installed." | Exploitation of unpatched vulnerabilities is the #1 vector for automated ransomware. |
| **T3. Backup Integrity** | **RC.RP-03** | "Backups of data are protected from unauthorized access/modification (Immutable)." | The only defense against "Double Extortion" ransomware. Must be offline/immutable. |
| **T4. MFA Implementation** | **PR.AA-03** | "Authenticators and credentials are issued, managed, and authenticated (MFA)." | Single most effective control against credential stuffing and phishing aftermath. |
| **T5. Perimeter/DNS** | **PR.DS-11** | "Data in transit is protected." (DNS Filtering context) | DNS filtering blocks C2 (Command & Control) callbacks, stopping an infection from becoming a breach. |
| **T6. Logging/Detection** | **DE.CM-01** | "The physical environment and computing devices are monitored." | Lightweight log aggregation allows for forensic analysis post-incident. |

### 3.3 Domain C: Human Factor ($S_{human}$)
*Objective:* Strengthen the human firewall and minimize user error (NIST Function: PROTECT - Awareness).

| Model Variable | NIST 2.0 Reference | Subcategory Description | Justification for SME Inclusion |
| :--- | :--- | :--- | :--- |
| **H1. Phishing Simulation** | **PR.AT-01** | "Personnel are provided with awareness and training... on a periodic basis." | Simulation ($P_{phish}$) provides the quantitative metric for this control, moving beyond "attendance sheets." |
| **H2. Training Frequency** | **PR.AT-02** | "Specialized role-based training is provided." | Ensures training isn't just annual compliance, but continuous reinforcement. |
| **H3. Culture/Reporting** | **GV.OC-01** | "Organizational mission, objectives, and high-level priorities... are understood." | Measures if employees feel safe reporting errors (Self-Reporting) vs. hiding them. |

---

## 4. The "Proportionate" Exclusion Logic
To defend the scientific rigor of this model for a high-quality journal, we must explicitly state what we **Excluded** and why. We do not map 100% of NIST CSF 2.0 because:

1.  **GV.PO (Policy):** Extensive policy documentation is excluded as it has low correlation with actual security outcomes in teams <50 people.
2.  **DE.AE (Adverse Event Analysis):** Advanced forensic analysis is assumed to be outsourced to Incident Response (IR) retainers, not handled internally.
3.  **RC.IM (Improvements):** "Lessons Learned" phases are simplified into the Governance review cycle to reduce bureaucratic load.

## 5. Conclusion on Alignment
The $\mathcal{M}_{PDS}$ model achieves **Coverage of 100% of NIST CSF 2.0 Functions** while reducing the **Subcategory Complexity by ~85%**. This reduction is the mathematical definition of "Proportionate Defense" for the resource-constrained enterprise.
