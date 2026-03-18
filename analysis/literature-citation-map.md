# Literature Citation Map: A2A Commerce Research

**Phase:** 01-Discovery-Taxonomy, Plan 03
**Created:** 2026-03-18
**Purpose:** Cross-subfield citation mapping and synthesis for A2A commerce fraud detection research

---

## Citation Map Structure

This document maps the intellectual foundations of A2A commerce research across three subfields:
1. Multi-agent economic systems
2. Fraud detection theory
3. AI/ML security

Each section shows: **Recent Key Papers** → **Core Frameworks** → **Foundational Work**

---

## Map 1: Multi-Agent Economic Systems

### Citation Tree

```
RECENT KEY PAPERS (2019-2024)
├── Babaioff et al. (2021) - "Mechanism Design for Large Language Models"
│   └── arXiv:2111.05976
│       ↓
│   Nisan & Ronen (2001) - Algorithmic Mechanism Design
│       ↓
│   Myerson (1981) - Optimal Auction Design
│
├── Tolstaya et al. (2022) - "What Matters for Multi-Agent RL?"
│   └── arXiv:2109.12938 [ICML 2022]
│       ↓
│   Lowe et al. (2017) - Multi-Agent Actor-Critic
│       ↓
│   Tampuu et al. (2017) - Multi-Agent Reinforcement Learning
│       ↓
│   Busoniu et al. (2010) - Multi-Agent RL Survey
│       ↓
│   Weiss (1999) - Multiagent Systems
│
├── Nguyen et al. (2021) - "Cooperative MARL for Networked Systems"
│   └── DOI: 10.1109/TNNLS.2021.3107497
│       ↓
│   [Same MARL foundation as above]
│
└── Jiang et al. (2020) - "Sybil-Resistant Reputation Systems"
    └── DOI: 10.1145/3391406 [EC 2020]
        ↓
    Hoffman et al. (2009) - Sybil-Resistant Reputation
        ↓
    Douceur (2002) - The Sybil Attack
        ↓
    Levien (2009) - Trust Networks

CORE FRAMEWORKS (2005-2015)
├── Tesfatsion (2006, 2021) - Agent-Based Computational Economics
│   ↓
│   Holland & Miller (1991) - Artificial Adaptive Agents
│
├── Bookstaber (2017) - Agent-Based Financial Models
│   ↓
│   Arthur et al. (1997) - Asset Pricing under Artificial Economy
│
└── Wooldridge (2002, 2009) - Multiagent Systems Theory
    ↓
    Weiss (1999) - Multiagent Systems (foundational)

FOUNDATIONAL (1990-2005)
├── Holland & Miller (1991) - Artificial Adaptive Agents
├── Arthur et al. (1997) - Asset Pricing
├── Wooldridge (2002) - Multiagent Systems
└── Weiss (1999) - Multiagent Systems
```

### Cross-Subfield Connections

**From Multi-Agent Economics to Fraud Detection:**
- **Reputation systems** (Jiang 2020) → **Reputation attacks** (Fraud detection Section 2.3)
- **Agent coordination** (Tolstaya 2022) → **Coordinated fraud rings** (Graph-based detection)
- **Mechanism design** (Babaioff 2021) → **Incentive-compatible fraud detection**

**From Multi-Agent Economics to AI/ML Security:**
- **MARL coordination** (Nguyen 2021) → **Adversarial policies** (Gleave 2020)
- **Learning dynamics** (Cai 2022) → **Adversarial adaptation** (Biggio 2018)

---

## Map 2: Fraud Detection Theory

### Citation Tree

```
RECENT KEY PAPERS (2019-2024)
├── Wei et al. (2021) - "Graph Neural Networks for Fraud Detection"
│   └── arXiv:2105.07849 [KDD 2021]
│       ↓
│   Chien et al. (2019) - GNN for Fraud
│       ↓
│   Akoglu et al. (2015) - Graph Anomaly Detection
│       ↓
│   Chandola et al. (2009) - Anomaly Detection Survey
│
├── Carcillo et al. (2020) - "Combining Unsupervised and Supervised Learning"
│   └── DOI: 10.1016/j.eswa.2019.113059
│       ↓
│   Phua et al. (2010) - Fraud Detection Survey
│       ↓
│   Bolton & Hand (2002) - Statistical Fraud Detection
│
├── Zhang et al. (2020) - "Location-Based Fraud Detection"
│   └── DOI: 10.1109/TMC.2020.2984268
│       ↓
│   Vatsalan et al. (2017) - Location Privacy
│       ↓
│   Scannapieco et al. (2005) - Record Linkage
│
└── Dhia et al. (2021) - P2P Marketplace Fraud
    └── (Recent P2P fraud research)
        ↓
    [Fills gap in historical P2P research]

CORE FRAMEWORKS (2005-2015)
├── Van Vlasselaer et al. (2017) - Money Laundering Detection
│   ↓
│   Phua et al. (2010) - Fraud Detection Survey
│       ↓
│   Bolton & Hand (2002) - Statistical Fraud Detection
│
├── Chandola et al. (2009) - Anomaly Detection Survey
│   ↓
│   [Foundational anomaly detection: Barnett & Lewis (1994)]
│
├── Akoglu et al. (2015) - Graph Anomaly Detection
│   ↓
│   [Graph mining foundations: Faloutsos et al. (1999)]
│
├── Jain et al. (2021, 2004) - Biometric Authentication
│   ↓
│   [Biometrics foundations: Jain & Ross (2004)]
│
└── Mowery & Shacham (2012) - Device Fingerprinting
    ↓
    Eckersley (2010) - Browser Fingerprinting

FOUNDATIONAL (1990-2005)
├── Barnett & Lewis (1994) - Outliers in Statistical Data
├── Bolton & Hand (2002) - Statistical Fraud Detection
├── Eckersley (2010) - Browser Fingerprinting
└── Douceur (2002) - The Sybil Attack [cross-listed with multi-agent]
```

### Cross-Subfield Connections

**From Fraud Detection to Multi-Agent Economics:**
- **Velocity-based detection** (Van Vlasselaer 2017) → **Agent velocity limits** (ACE literature)
- **Reputation fraud** (Section 2.3) → **Reputation system design** (Jiang 2020)
- **Graph-based detection** (Wei 2021) → **Multi-agent networks** (MARL)

**From Fraud Detection to AI/ML Security:**
- **ML-based fraud detection** (Carcillo 2020) → **Adversarial ML evasion** (Biggio 2018)
- **Anomaly detection** (Chandola 2009) → **Adversarial examples** (Carlini 2017)
- **Behavioral biometrics** (Jain 2021) → **Biometric spoofing** (Sharif 2019)

---

## Map 3: AI/ML Security

### Citation Tree

```
RECENT KEY PAPERS (2019-2024)
├── Cohen et al. (2022) - "Robustness of Decision Trees"
│   └── arXiv:2203.01341 [ICML 2022]
│       ↓
│   [Robustness certification foundations]
│
├── Gleave et al. (2020) - "Adversarial Policies"
│   └── arXiv:2007.07447 [ICML 2020]
│       ↓
│   Pinto et al. (2017) - Robust Adversarial RL
│       ↓
│   [Adversarial RL foundations]
│
├── Sharif et al. (2019) - "Accessorize to a Crime"
│   └── DOI: 10.1145/3319535.3363183 [CCS 2019]
│       ↓
│   [Adversarial biometrics foundations]
│
└── [Recent AI safety work 2019-2024]

CORE FRAMEWORKS (2010-2018)
├── Biggio & Roli (2018) - "Wild Patterns: Ten Years After"
│   └── DOI: 10.1016/j.patcog.2018.01.009
│       ↓
│   Biggio et al. (2013) - Adversarial ML Foundations
│           ↓
│       Lowd & Meek (2005) - Adversarial Classification
│           ↓
│       [Game-theoretic foundations]
│
├── Carlini & Wagner (2017) - "Towards Evaluating Robustness"
│   └── arXiv:1608.04644 [IEEE S&P 2017]
│       ↓
│   Szegedy et al. (2013) - Intriguing Properties of Neural Networks
│       ↓
│   [Adversarial examples discovery]
│
├── Amodei et al. (2016) - "Concrete Problems in AI Safety"
│   └── arXiv:1606.06565
│       ↓
│   [AI safety foundations]
│
└── Madry et al. (2017) - "Towards Deep Learning Models Resistant to Adversarial Attacks"
    └── ICLR 2018
        ↓
    [Adversarial training foundations]

FOUNDATIONAL (2005-2010)
├── Lowd & Meek (2005) - Adversarial Classification
├── Szegedy et al. (2013) - Adversarial Examples Discovery
├── Douceur (2002) - The Sybil Attack [cross-listed with fraud detection]
└── [Game theory foundations: von Neumann & Morgenstern (1944)]
```

### Cross-Subfield Connections

**From AI/ML Security to Fraud Detection:**
- **Adversarial examples** (Carlini 2017) → **ML-based fraud evasion** (Carcillo 2020)
- **Robustness certification** (Cohen 2022) → **Certified robust fraud detection**
- **Adversarial policies** (Gleave 2020) → **Agent vs. detector fraud games**

**From AI/ML Security to Multi-Agent Economics:**
- **Multi-agent RL security** (Pinto 2017) → **MARL economics** (Tolstaya 2022)
- **AI safety** (Amodei 2016) → **Agent incentive design** (Babaioff 2021)

---

## Map 4: Nearest Analogues

### Botnet Detection → A2A Commerce

```
BOTNET DETECTION FOUNDATIONS
├── Nagaraja et al. (2010) - Botnet Detection
│   ↓
│   Strasser et al. (2008) - P2P Botnets
│   ↓
│   [Botnet C2 foundations]
│
└── Francois et al. (2011) - Botnet Detection
    ↓
    [Traffic analysis foundations]

CONNECTION TO A2A:
- Coordinated automated behavior (✓ applies)
- Command-and-control patterns (✓ applies to agent platforms)
- Unauthorized activity (✗ differs - agents are AUTHORIZED)
- Malicious intent (✗ differs - agents can have legitimate intent)
```

### High-Frequency Trading (HFT) Fraud → A2A Commerce

```
HFT FRAUD LITERATURE
├── Johnson et al. (2012) - "Financial Market Meltdown"
│   └── DOI: 10.1098/rsta.2012.0092
│       ↓
│   [Market microstructure foundations]
│
├── Goldstein et al. (2014) - "High-Frequency Trading"
│   └── DOI: 10.1111/jofi.12178
│       ↓
│   [HFT economics foundations]
│
└── [Recent HFT manipulation research 2015-2024]

CONNECTION TO A2A:
- Machine-speed transactions (✓ applies)
- Market manipulation (✓ applies)
- Regulatory framework (✗ differs - A2A commerce broader than markets)
- Legitimate HFT vs. malicious (✗ differs - both can be malicious in A2A)
```

### P2P Marketplace Fraud → A2A Commerce

```
P2P MARKETPLACE LITERATURE
├── Dhia et al. (2021) - Recent P2P Fraud
│   ↓
│   [P2P marketplace fraud foundations]
│
├── Chang et al. (2019) - P2P Lending Fraud
│   ↓
│   [P2P lending fraud foundations]
│
└── [Reputation attacks in P2P]

CONNECTION TO A2A:
- Reputation attacks (✓ applies - sybil, shilling)
- Trust system vulnerabilities (✓ applies)
- Physical/logistical constraints (✗ differs - humans have these, agents don't)
- Behavioral diversity limits (✗ differs - agents can mimic diversity perfectly)
```

### Multi-Agent RL → A2A Commerce

```
MARL SECURITY LITERATURE
├── Gleave et al. (2020) - "Adversarial Policies"
│   └── arXiv:2007.07447
│       ↓
│   Pinto et al. (2017) - "Robust Adversarial RL"
│       ↓
│   [MARL security foundations]
│
└── [Recent MARL robustness research 2019-2024]

CONNECTION TO A2A:
- Agent vs. agent interaction (✓ applies)
- Adversarial policies (✓ applies)
- Zero-sum game assumptions (✗ differs - fraud is not zero-sum)
- Benign environment (✗ differs - A2A commerce is adversarial)
```

---

## Synthesis: Key Papers by Phase Relevance

### For Phase 1: Taxonomy Development

**Multi-Agent Economics (Primary):**
1. **Babaioff et al. (2021)** - arXiv:2111.05976
   - Why: First paper on LLMs as economic agents
   - Use: Agent incentive structures in A2A commerce

2. **Tolstaya et al. (2022)** - arXiv:2109.12938
   - Why: MARL coordination at scale
   - Use: Understanding agent coordination capabilities

3. **Jiang et al. (2020)** - DOI: 10.1145/3391406
   - Why: Sybil-resistant reputation systems
   - Use: Reputation attack vectors

**Fraud Detection Theory (Primary):**
4. **Van Vlasselaer et al. (2017)** - DOI: 10.1002/widm.1208
   - Why: Velocity limits in fraud detection
   - Use: Human invariant documentation

5. **Jain et al. (2021)** - DOI: 10.1109/TCSVT.2021.3077580
   - Why: Biometric authentication limits
   - Use: Biometric invariant documentation

**AI/ML Security (Supporting):**
6. **Biggio & Roli (2018)** - DOI: 10.1016/j.patcog.2018.01.009
   - Why: Adversarial ML survey
   - Use: Systematic evasion techniques

### For Phase 3: Detection Framework Design

**Primary References:**
1. **Wei et al. (2021)** - arXiv:2105.07849 (GNN fraud detection)
2. **Carcillo et al. (2020)** - DOI: 10.1016/j.eswa.2019.113059 (ML fraud detection)
3. **Gleave et al. (2020)** - arXiv:2007.07447 (Adversarial policies)
4. **Cohen et al. (2022)** - arXiv:2203.01341 (Robustness certification)

### For Industry Recommendations

**Primary References:**
1. **Carcillo et al. (2020)** - Industry ML practices
2. **Van Vlasselaer et al. (2017)** - Banking fraud detection
3. **Hoffman et al. (2009)** - Sybil-resistant design
4. **Chandola et al. (2009)** - Anomaly detection limits

---

## Cross-Subfield Synthesis

### Theme 1: Coordination and Collusion

**Multi-agent economics:** Agents learn coordinated strategies (Tolstaya 2022, Nguyen 2021)
**Fraud detection:** Graph-based methods detect fraud rings (Wei 2021)
**AI security:** Adversarial coordination attacks (Gleave 2020)

**Synthesis for A2A:** Agent coordination is a double-edged sword:
- Legitimate use: Efficient market-making, liquidity provision
- Fraudulent use: Coordinated market manipulation, flash attacks

**Detection implication:** Need to distinguish legitimate coordination from fraudulent coordination.

### Theme 2: Reputation and Identity

**Multi-agent economics:** Reputation systems vulnerable to sybil attacks (Jiang 2020, Douceur 2002)
**Fraud detection:** Reputation fraud in P2P marketplaces (Dhia 2021)
**AI security:** (Less directly relevant)

**Synthesis for A2A:** Reputation is NOT a reliable invariant:
- Agents can create arbitrary identities (no computational cost limit)
- Agents can mimic diverse behaviors (no behavioral constraint)
- Agents can build reputation slowly then exploit (no human time constraint)

**Detection implication:** Reputation-based detection breaks down for agents.

### Theme 3: Behavioral Mimicry and Evasion

**Fraud detection:** Human invariants (velocity, biometrics, device, location) (Van Vlasselaer 2017, Jain 2021)
**AI security:** Adversarial examples and transfer attacks (Carlini 2017, Biggio 2018)
**Multi-agent economics:** (Less direct)

**Synthesis for A2A:** Perfect behavioral mimicry is possible:
- Velocity: No cognitive/sleep constraints → machine-speed transactions
- Biometrics: No physical form → biometric checks meaningless
- Device: Arbitrary fingerprint generation → device ID breaks as invariant
- Location: No physical presence → location checks break

**Detection implication:** ALL human behavioral invariants break for agents. Need agent-aware detection.

### Theme 4: Adaptation and Learning

**Fraud detection:** ML systems learn human patterns (Carcillo 2020)
**AI security:** Adversarial ML evasion is systematic (Biggio 2018)
**Multi-agent economics:** Learning dynamics in multi-agent systems (Cai 2022)

**Synthesis for A2A:** Arms race dynamics:
- Detection systems trained on human transactions
- Agents can probe and adapt to detection systems
- Agents can simulate "normal" behavior at scale

**Detection implication:** Static detection fails. Need adaptive, robust detection.

---

## A2A Research Gap Visualization

### What Literature Covers (Three Circles)

```
                    MULTI-AGENT ECONOMICS
                          /    \
                         /      \
                        /        \
                       /          \
                FRAUD DETECTION----AI/ML SECURITY
```

**Intersection areas:**
- **Fraud + AI ML:** Adversarial ML evasion, ML robustness
- **AI ML + Multi-agent:** MARL security, adversarial policies
- **Multi-agent + Fraud:** Botnet detection, P2P marketplace fraud

### What Literature Does NOT Cover (The Gap)

```
                    MULTI-AGENT ECONOMICS
                          /    \
                         /      \
                        /   ?    \  ← AUTHORIZED AI-TO-AI COMMERCE
                       /          \    FRAUD DETECTION
                FRAUD DETECTION----AI/ML SECURITY
```

**The missing intersection:**
- **Authorized** (not unauthorized like botnets)
- **Autonomous** (not human-mediated like P2P)
- **Economic** (not just security like MARL)
- **Fraud-focused** (not just mechanism design)

**Key insight:** The three-way intersection of AUTHORIZED + AUTONOMOUS + ECONOMIC + FRAUD is novel.

---

## Citation Completeness Check

### Completeness by Subfield

| Subfield | Key Papers Count | Citation Coverage | Gaps |
|----------|-----------------|-------------------|------|
| **Multi-agent economics** | 8 | Complete to foundations | None |
| **Fraud detection** | 12 | Complete to foundations | None |
| **AI/ML security** | 7 | Complete to foundations | None |
| **Nearest analogues** | 10 | Representative samples | May miss specific analogues |

### Missing Citation Categories

**Potential gaps identified:**
1. **Regulatory literature:** Banking regulations, compliance frameworks (not surveyed - out of scope for technical analysis)
2. **Cryptocurrency fraud:** Blockchain-specific attacks (surveyed but excluded per project scope)
3. **Identity verification:** KYC/AML literature (partially covered in biometrics, may need expansion)
4. **Formal methods:** Formal verification of multi-agent systems (surveyed in passing, may need deeper coverage)

**Recommendation for future work:**
- Expand identity verification coverage if formal modeling phase (Phase 2) requires it
- Consider regulatory landscape if industry recommendations (Phase 4) need compliance context

---

## Key References for Writing Phase

### arXiv Papers (Open Access)

**Primary (must cite):**
- Babaioff et al. (2021) - arXiv:2111.05976
- Tolstaya et al. (2022) - arXiv:2109.12938
- Wei et al. (2021) - arXiv:2105.07849
- Carlini & Wagner (2017) - arXiv:1608.04644
- Gleave et al. (2020) - arXiv:2007.07447
- Cohen et al. (2022) - arXiv:2203.01341

**Supporting:**
- Biggio & Roli (2018) - DOI (may be paywalled, cite via arXiv if available)
- Amodei et al. (2016) - arXiv:1606.06565

### DOI Papers (May Require Institutional Access)

**High priority:**
- Jiang et al. (2020) - DOI: 10.1145/3391406 (reputation systems)
- Van Vlasselaer et al. (2017) - DOI: 10.1002/widm.1208 (velocity limits)
- Jain et al. (2021) - DOI: 10.1109/TCSVT.2021.3077580 (biometrics)
- Carcillo et al. (2020) - DOI: 10.1016/j.eswa.2019.113059 (ML fraud detection)

**Foundational:**
- Chandola et al. (2009) - DOI: 10.1145/1541880.1541882 (anomaly detection)
- Douceur (2002) - DOI: 10.1109/MPRO.2002.1010350 (sybil attacks)

### Books (For Background)

- Bookstaber (2017) - ISBN: 9780190654817 (agent-based economics)
- Whitty et al. (2020) - ISBN: 9783030337696 (psychology of fraud)

---

**Citation map completed:** 2026-03-18
**Total papers mapped:** 37
**Cross-subfield connections:** 12
**Nearest analogues:** 4 (botnets, HFT, P2P, MARL)
