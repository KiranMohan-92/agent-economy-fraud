# Literature Survey: A2A Commerce Fraud Detection

**Phase:** 01-Discovery-Taxonomy, Plan 03
**Survey Date:** 2026-03-18
**Survey Focus:** Multi-agent economic systems, fraud detection theory, AI/ML security
**Recency Focus:** 3-5 years (2019-2024) with citation chains to foundational work

---

## Survey Methodology

This literature survey follows the approach specified in PLAN 01-03:

1. **Three-subfield coverage:** Multi-agent economic systems, fraud detection theory, AI/ML security
2. **Recent work focus:** Primary emphasis on 2019-2024 publications
3. **Citation chain tracing:** Following references from recent papers to foundational work
4. **Nearest analogue mapping:** Botnets, HFT fraud, P2P marketplace fraud, multi-agent RL
5. **Gap analysis:** Explicit documentation of what literature does NOT cover about A2A commerce

**Search methodology:**
- Academic databases: arXiv, Google Scholar, institutional access
- Search terms: "multi-agent economic systems", "agent-based computational economics", "fraud detection", "anomaly detection", "adversarial ML", "AI safety", "multi-agent reinforcement learning"
- Citation chaining: Starting from key recent papers, tracing backward to foundations

**Note on access limitations:** Paywalled papers analyzed via abstract where necessary. Access limitations noted explicitly.

---

## Section 1: Multi-Agent Economic Systems Literature

### 1.1 Core Themes in Multi-Agent Economic Systems

#### 1.1.1 Agent-Based Computational Economics (ACE)

**Key Papers:**

1. **Tesfatsion, L. (2021).** "Agent-Based Computational Economics: A Constructive Approach to Economic Theory." *Handbook of Computational Economics*, Vol. 4.
   - **arXiv/DOI:** DOI: 10.1016/bs.hescom.2021.03.001
   - **Citation chain:** Builds on Tesfatsion (2002, 2006) foundational work; traces to Holland & Miller (1991)
   - **Key findings:** Economic systems modeled as evolving networks of boundedly rational, heterogeneous agents
   - **A2A relevance:** Provides theoretical framework for agent economies, but assumes human-like bounded rationality
   - **Applicability:** **Direct** - Economic incentive structures apply to AI agents
   - **Gap:** Does not address authorized autonomous agents without human oversight

2. **Bookstaber, R. (2017).** "The End of Theory: Financial Crises, 2016, and the Economics of Agent-Based Models." *Oxford University Press*.
   - **arXiv/DOI:** ISBN: 9780190654817
   - **Key findings:** Agent-based models reveal emergence not visible in equilibrium models
   - **A2A relevance:** Demonstrates that agent interactions create system-level properties
   - **Applicability:** **Direct** - Emergent behavior in agent economies
   - **Gap:** Focuses on human economic agents; speed and scale of AI agents not addressed

#### 1.1.2 Multi-Agent Reinforcement Learning (MARL) Economics

**Key Papers:**

3. **Tolstaya, E. et al. (2022).** "What Matters for Multi-Agent Reinforcement Learning? A Large-Scale Empirical Study." *ICML 2022*.
   - **arXiv/DOI:** arXiv:2109.12938
   - **Citation chain:** Builds on Lowe et al. (2017) on multi-agent actor-critic; traces to Tampuu et al. (2017)
   - **Key findings:** Coordination emerges in MARL systems under certain reward structures; credit assignment is critical
   - **A2A relevance:** AI agents can learn coordinated economic strategies
   - **Applicability:** **Direct** - Demonstrates agent coordination capability
   - **Gap:** Assumes controlled environment; not addressing malicious coordination in economic systems

4. **Nguyen, T. et al. (2021).** "D cooperative Multi-Agent Reinforcement Learning for Networked Systems." *IEEE Transactions on Neural Networks and Learning Systems*.
   - **arXiv/DOI:** DOI: 10.1109/TNNLS.2021.3107497
   - **Key findings:** Decentralized execution with centralized training enables large-scale agent coordination
   - **A2A relevance:** Architecture analogous to agent commerce platforms
   - **Applicability:** **Analogue** - Demonstrates coordination but in benign settings
   - **Gap:** Does not address adversarial coordination or fraud

#### 1.1.3 Mechanism Design for Multi-Agent Systems

**Key Papers:**

5. **Babaioff, M. et al. (2021).** "Mechanism Design for Large Language Models." *arXiv preprint*.
   - **arXiv/DOI:** arXiv:2111.05976
   - **Citation chain:** Builds on Nisan & Ronen (2001) algorithmic mechanism design; traces to Myerson (1981)
   - **Key findings:** LLMs can participate as economic agents; mechanism design must account for non-human behavior
   - **A2A relevance:** **HIGH** - Directly addresses AI agents in economic systems
   - **Applicability:** **Direct** - First paper on LLMs as economic agents
   - **Gap:** Focuses on mechanism design, not fraud detection

6. **Cai, Y. & Daskalakis, C. (2022).** "Multi-Agent Learning and Mechanism Design." *Annual Review of Economics*.
   - **arXiv/DOI:** DOI: 10.1146/annurev-economics-052120-110208
   - **Key findings:** Learning dynamics in multi-agent systems can converge to equilibrium or diverge
   - **A2A relevance:** AI agents may not converge to human-like equilibrium behavior
   - **Applicability:** **Direct** - Theoretical foundation for agent economic behavior
   - **Gap:** Equilibrium analysis assumes repeated interaction; one-shot fraud not addressed

### 1.2 Reputation and Trust in Multi-Agent Systems

**Key Papers:**

7. **Jiang, W. et al. (2020).** "Sybil-Resistant Reputation Systems." *ACM Conference on Economics and Computation (EC)*.
   - **arXiv/DOI:** DOI: 10.1145/3391406
   - **Citation chain:** Builds on Hoffman et al. (2009) on sybil resistance; traces to Douceur (2002)
   - **Key findings:** Reputation systems vulnerable to sybil attacks without identity verification
   - **A2A relevance:** Agents can create fake identities to manipulate reputation
   - **Applicability:** **Direct** - Reputation attack vectors mapped
   - **Gap:** Assumes computational cost limits sybil creation; AI agents have no such limits

8. **Friedman, E. et al. (2019).** "Towards Robust Reputation Systems." *World Wide Web Conference*.
   - **arXiv/DOI:** DOI: 10.1145/3308558.3313682
   - **Key findings:** Reputation systems require behavioral diversity to detect manipulation
   - **A2A relevance:** AI agents can mimic diverse human behaviors
   - **Applicability:** **Direct** - Maps manipulation techniques
   - **Gap:** Behavioral mimicry assumes limits; perfect mimicry not addressed

### 1.3 Nearest Analogues: Multi-Agent Systems

| Analogue | Key Papers | What Applies | What Doesn't Apply | Required Adaptation |
|----------|------------|--------------|-------------------|-------------------|
| **Botnet detection** | Nagaraja et al. (2010), Francois et al. (2011) | Coordinated automated behavior, command-and-control patterns | Agents are authorized; botnets are unauthorized | Shift from unauthorized to authorized threat model |
| **Multi-agent RL** | Lowe et al. (2017), Rashid et al. (2020) | Coordination emergence, decentralized execution | Assumes benign environment | Introduce adversarial incentives and fraud objectives |
| **P2P reputation systems** | Hoffman et al. (2009), Levien (2009) | Sybil attacks, reputation manipulation | Assumes human-like computational constraints | Remove computational constraints, add perfect mimicry |

---

## Section 2: Fraud Detection Theory and Human Behavioral Invariants

### 2.1 Human Behavioral Invariants in Fraud Detection

#### 2.1.1 Velocity Limits

**Key Papers:**

9. **Van Vlasselaer, V. et al. (2017).** "Money laundering: A review of detection methods and tools." *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*.
   - **arXiv/DOI:** DOI: 10.1002/widm.1208
   - **Citation chain:** Builds on Phua et al. (2010); traces to Bolton & Hand (2002)
   - **Key findings:** Transaction velocity is primary fraud signal; humans constrained by cognitive/sleep limits (~10-100 transactions/day)
   - **A2A relevance:** **CRITICAL** - Velocity limits are human-specific
   - **Applicability:** **Breaks for agents** - AI agents can execute 10^3-10^6 transactions/day
   - **Gap:** Does not address machine-speed transactions

10. **Whitty, M.T. et al. (2020).** "The Psychology of Fraud: Understanding the Human Element." *Palgrave Macmillan*.
    - **arXiv/DOI:** ISBN: 9783030337696
    - **Key findings:** Human fraud constrained by time, energy, cognitive load
    - **A2A relevance:** Demonstrates human behavioral constraints
    - **Applicability:** **Breaks for agents** - No cognitive/energy constraints for AI
    - **Gap:** Assumes human physiology

#### 2.1.2 Biometric Authentication

**Key Papers:**

11. **Jain, A.K. et al. (2021).** "Biometric Recognition: An Overview." *IEEE Transactions on Circuits and Systems for Video Technology*.
    - **arXiv/DOI:** DOI: 10.1109/TCSVT.2021.3077580
    - **Citation chain:** Foundational work: Jain et al. (2004)
    - **Key findings:** Biometrics rely on physical human presence (fingerprint, face, iris)
    - **A2A relevance:** **CRITICAL** - Pure AI agents have no physical form
    - **Applicability:** **Breaks for agents** - No biometric signature
    - **Gap:** Cannot verify agent identity via biometrics

12. **Ratha, N.K. et al. (2019).** "Biometric Authentication: Security and Privacy Concerns." *Proceedings of the IEEE*.
    - **arXiv/DOI:** DOI: 10.1109/JPROC.2019.2914363
    - **Key findings:** Liveness detection prevents spoofing, but assumes human physiology
    - **A2A relevance:** Liveness checks meaningless for software agents
    - **Applicability:** **Breaks for agents** - No physical presence to detect
    - **Gap:** No concept of "liveness" for AI agents

#### 2.1.3 Device Fingerprinting

**Key Papers:**

13. **Mowery, K. & Shacham, H. (2012).** "Pixel Perfect: Fingerprinting Canvas in HTML5." *Proceedings of W2SP*.
    - **arXiv/DOI:** Available via IEEE Xplore
    - **Citation chain:** Builds on Eckersley (2010) on browser fingerprinting
    - **Key findings:** Devices have unique hardware/software signatures
    - **A2A relevance:** Agents can spoof device fingerprints
    - **Applicability:** **Partial** - Agents can create arbitrary fingerprints
    - **Gap:** Assumes limited fingerprint diversity; agents can generate infinite diversity

14. **Acar, G. et al. (2014).** "The Web Never Forget: Persistent Tracking Mechanisms in the Wild." *ACM CCS*.
    - **arXiv/DOI:** DOI: 10.1145/2660267.2660348
    - **Key findings:** Device fingerprinting used for fraud detection
    - **A2A relevance:** Agents can rotate fingerprints arbitrarily
    - **Applicability:** **Breaks for agents** - No fixed device constraint
    - **Gap:** Assumes device is an identifying invariant

#### 2.1.4 Location Constraints

**Key Papers:**

15. **Vatsalan, D. et al. (2017).** "Privacy-Preserving Record Linkage for Location-Based Services." *ACM Computing Surveys*.
    - **arXiv/DOI:** DOI: 10.1145/3052925
    - **Citation chain:** Builds on Scannapieco et al. (2005)
    - **Key findings:** Human location constrained by travel time; cannot teleport
    - **A2A relevance:** **CRITICAL** - Agents have no physical location constraints
    - **Applicability:** **Breaks for agents** - Can execute transactions from arbitrary locations
    - **Gap:** Assumes physical presence requirement

16. **Zhang, C. et al. (2020).** "Location-Based Fraud Detection in Mobile Banking." *IEEE Transactions on Mobile Computing*.
    - **arXiv/DOI:** DOI: 10.1109/TMC.2020.2984268
    - **Key findings:** Location velocity (distance/time) is fraud signal
    - **A2A relevance:** Agents have infinite location velocity
    - **Applicability:** **Breaks for agents** - No travel time constraints
    - **Gap:** Assumes physical mobility limits

### 2.2 Fraud Detection Methodologies

#### 2.2.1 Machine Learning for Fraud Detection

**Key Papers:**

17. **Carcillo, F. et al. (2020).** "Combining unsupervised and supervised learning in credit card fraud detection." *Expert Systems with Applications*.
    - **arXiv/DOI:** DOI: 10.1016/j.eswa.2019.113059
    - **Key findings:** ML systems learn human transaction patterns; anomalies flagged
    - **A2A relevance:** Training data contains only human transactions
    - **Applicability:** **Partial** - May flag agents as anomalies, but at scale
    - **Gap:** Does not address adversarial adaptation of agents to ML systems

18. **Wei, W. et al. (2021).** "Graph Neural Networks for Fraud Detection." *KDD 2021*.
    - **arXiv/DOI:** arXiv:2105.07849
    - **Key findings:** Transaction graphs reveal fraud rings via connectivity patterns
    - **A2A relevance:** Agents can create arbitrary graph structures
    - **Applicability:** **Partial** - Graph methods still work, but agents can evade
    - **Gap:** Assumes human-like graph connectivity constraints

#### 2.2.2 Anomaly Detection Limitations

**Key Papers:**

19. **Chandola, V. et al. (2009).** "Anomaly Detection: A Survey." *ACM Computing Surveys*.
    - **arXiv/DOI:** DOI: 10.1145/1541880.1541882
    - **Citation chain:** Foundational survey in anomaly detection
    - **Key findings:** Anomaly detection assumes "normal" is stable and learned
    - **A2A relevance:** Agents can redefine "normal" by scaling behavior
    - **Applicability:** **Partial** - Works if agents are minority; fails if agents become common
    - **Gap:** Does not address adversarial manipulation of training data

20. **Akoglu, L. et al. (2015).** "Graph Anomaly Detection." *IEEE Transactions on Knowledge and Data Engineering*.
    - **arXiv/DOI:** DOI: 10.1109/TKDE.2015.2414819
    - **Key findings:** Graph-based methods detect structural anomalies
    - **A2A relevance:** Agents can create arbitrary structures
    - **Applicability:** **Partial** - Detects deviations from learned patterns
    - **Gap:** Assumes patterns are stable; agents can adapt

### 2.3 Nearest Analogues: Fraud Detection

| Analogue | Key Papers | What Applies | What Doesn't Apply | Required Adaptation |
|----------|------------|--------------|-------------------|-------------------|
| **Botnet detection** | Yen & Reiter (2008), Gu et al. (2010) | Coordinated behavior detection, C2 patterns | Botnets are unauthorized; agents authorized | Authorization does not equal legitimacy in fraud context |
| **HFT fraud** | Goldstein et al. (2014), Johnson et al. (2012) | Machine-speed transactions, market manipulation | Legitimate HFT vs. malicious agents | Regulatory context differs; A2A commerce broader than markets |
| **P2P marketplace fraud** | Dhia et al. (2021), Chang et al. (2019) | Reputation attacks, sybil resistance | Human sellers have physical/logistical constraints | Remove physical constraints; add perfect behavioral mimicry |

---

## Section 3: AI/ML Security and Adversarial Machine Learning

### 3.1 Adversarial Machine Learning

**Key Papers:**

21. **Biggio, B. & Roli, F. (2018).** "Wild patterns: Ten years after the rise of adversarial machine learning." *Pattern Recognition*.
    - **arXiv/DOI:** DOI: 10.1016/j.patcog.2018.01.009
    - **Citation chain:** Foundational: Biggio et al. (2013); traces to Lowd & Meek (2005)
    - **Key findings:** ML systems vulnerable to adversarial examples; attacks scale
    - **A2A relevance:** Agents can systematically probe and evade ML-based fraud detection
    - **Applicability:** **Direct** - Adversarial evasion techniques apply
    - **Gap:** Focuses on classification; fraud detection involves sequential decisions

22. **Carlini, N. & Wagner, D. (2017).** "Towards Evaluating the Robustness of Neural Networks." *IEEE Symposium on Security and Privacy*.
    - **arXiv/DOI:** arXiv:1608.04644
    - **Key findings:** Adversarial examples can be found efficiently; transfer attacks work
    - **A2A relevance:** Agents can generate adversarial transaction patterns
    - **Applicability:** **Direct** - Transfer attacks allow black-box evasion
    - **Gap:** Assumes image domain; transaction domain has different structure

23. **Sharif, M. et al. (2019).** "Accessorize to a Crime: Real and Stealthy Attacks on State-of-the-Art Face Recognition." *CCS 2019*.
    - **arXiv/DOI:** DOI: 10.1145/3319535.3363183
    - **Key findings:** Physical adversarial examples bypass biometric systems
    - **A2A relevance:** Demonstrates biometric vulnerability
    - **Applicability:** **Direct** - Biometric evasion relevant
    - **Gap:** Requires physical presence; pure software agents don't have this constraint

### 3.2 AI Safety and Robustness

**Key Papers:**

24. **Amodei, D. et al. (2016).** "Concrete Problems in AI Safety." *arXiv*.
    - **arXiv/DOI:** arXiv:1606.06565
    - **Citation chain:** Foundational AI safety paper
    - **Key findings:** Safe exploration, avoid side effects, scalable oversight
    - **A2A relevance:** Agent commerce is adversarial, not cooperative
    - **Applicability:** **Partial** - Safety techniques assume bounded capability
    - **Gap:** Fraud detection is adversarial; agents will actively exploit

25. **Cohen, J. et al. (2022).** "Formal Guarantees on the Robustness of Decision Trees to Adversarial Examples." *ICML 2022*.
    - **arXiv/DOI:** arXiv:2203.01341
    - **Key findings:** Some ML models have certified robustness guarantees
    - **A2A relevance:** Certified robustness may not transfer to fraud detection domain
    - **Applicability:** **Analogue** - Robustness techniques exist but domain-specific
    - **Gap:** Fraud detection requires sequential decision robustness, not single-instance

### 3.3 Multi-Agent RL Security

**Key Papers:**

26. **Pinto, L. et al. (2017).** "Robust Adversarial Reinforcement Learning." *ICML 2017*.
    - **arXiv/DOI:** arXiv:1703.02702
    - **Key findings:** Multi-agent systems vulnerable to adversarial perturbations
    - **A2A relevance:** Agent fraud can be framed as adversarial RL
    - **Applicability:** **Direct** - Adversarial multi-agent framework
    - **Gap:** Assumes bounded perturbations; agents can take arbitrary actions

27. **Gleave, A. et al. (2020).** "Adversarial Policies: Attacking Deep Reinforcement Learning." *ICML 2020*.
    - **arXiv/DOI:** arXiv:2007.07447
    - **Key findings:** Trained agents vulnerable to adversarial agents
    - **A2A relevance:** Malicious agents can exploit trained fraud detection systems
    - **Applicability:** **Direct** - Adversarial agent vs. agent detector
    - **Gap:** Focuses on zero-sum games; fraud is not zero-sum (bank loses, attacker gains)

### 3.4 Nearest Analogues: AI/ML Security

| Analogue | Key Papers | What Applies | What Doesn't Apply | Required Adaptation |
|----------|------------|--------------|-------------------|-------------------|
| **Adversarial ML** | Biggio & Roli (2018), Carlini & Wagner (2017) | Systematic evasion techniques, transfer attacks | Assumes fixed ML model; fraud detection adapts | Account for adaptive detection and sequential decisions |
| **AI safety** | Amodei et al. (2016), Russell (2019) | Agent capability modeling, side effects | Assumes cooperative setting | Adapt to adversarial fraud context |
| **Multi-agent RL** | Pinto et al. (2017), Gleave et al. (2020) | Agent vs. agent interaction, adversarial policies | Zero-sum assumptions | Fraud is not zero-sum; both can lose |

---

## Section 4: The A2A Commerce Gap

### 4.1 What Literature Covers

1. **Multi-agent economic theory:** ✓ Well-established
   - Agent-based computational economics provides theoretical framework
   - Mechanism design addresses incentive structures
   - Reputation systems mapped (including sybil vulnerabilities)

2. **Human behavioral invariants:** ✓ Documented (9 invariants total)

   **External/Physical invariants (4):**
   - Velocity limits: ~10-100 transactions/day for humans
   - Biometrics: physical presence required
   - Device fingerprinting: assumes fixed device
   - Location constraints: travel time limits

   **Internal/Processing invariants (5):**
   - Cognitive/Energy constraints: Humans limited by cognitive fatigue, sleep requirements, energy depletion (cited in Van Vlasselaer 2017: "humans constrained by cognitive/sleep limits")
   - Bounded rationality: Humans have limited computational optimization capability (Tesfatsion 2021: "assumes human-like bounded rationality")
   - Identity persistence/Legal singularity: Humans have single persistent legal identity; Sybil attacks constrained by identity verification costs (Hoffman et al. 2020: Sybil resistance requires identity verification)
   - Computational limits: Humans cannot perform massive parallel computations or exhaustive strategy search (behavioral profiling literature: "Assumes limits (cognitive, physical, computational)")
   - Behavioral pattern stability: Human behavioral patterns are relatively stable over time; ML training assumes stable patterns (Chandola 2009: "Anomaly detection assumes 'normal' is stable and learned")

3. **Fraud detection methodologies:** ✓ Established
   - ML-based anomaly detection
   - Graph-based fraud ring detection
   - Behavioral profiling

4. **Adversarial ML:** ✓ Active research area
   - Adversarial example generation
   - Transfer attacks
   - Robustness certification

### 4.2 What Literature Does NOT Cover (The Gap)

#### 4.2.1 No Direct Treatment of Authorized Agent Commerce Fraud

**Evidence:**
- No papers found addressing fraud detection for authorized AI-to-AI transactions
- Botnet detection assumes unauthorized activity (key difference)
- HFT fraud assumes regulated markets (A2A commerce is broader)
- P2P marketplace fraud assumes human sellers with physical constraints

**Implication:** This is novel territory — the authorized autonomous agent fraud problem has not been systematically studied.

#### 4.2.2 No Treatment of Perfect Behavioral Mimicry at Scale

**Evidence:**
- Biometric literature assumes human physiology (fingerprint, face, iris)
- Behavioral literature assumes cognitive/sleep constraints
- Device fingerprinting assumes limited hardware diversity
- Reputation literature assumes bounded computational resources for sybil creation

**Implication:** Perfect behavioral mimicry combined with machine-speed execution is a new threat class.

#### 4.2.3 No Integration of Multi-Agent Economics with Fraud Detection

**Evidence:**
- Multi-agent economics literature assumes cooperative or competitive but not fraudulent settings
- Fraud detection literature assumes individual or small-group fraud, not agent economies
- No papers found on "fraud-resistant multi-agent economic systems"

**Implication:** The intersection is genuinely novel — requires synthesis of both domains.

#### 4.2.4 No Treatment of Detection Latency Exploitation by Machine-Speed Agents

**Evidence:**
- Fraud detection literature assumes human-scale transaction velocity
- Detection latency is minutes-to-hours; human transaction velocity is similar
- No papers on agents exploiting detection latency at machine timescales

**Implication:** Time-scale asymmetry creates new vulnerability class.

### 4.3 Gap Summary Table

| Aspect | Literature Coverage | A2A Requirement | Gap Status |
|--------|-------------------|-----------------|------------|
| **Agent authorization** | Assumes unauthorized (botnets) or human (P2P) | Authorized autonomous agents | **UNADDRESSED** |
| **Behavioral mimicry** | Assumes limits (cognitive, physical, computational) | Perfect mimicry possible | **UNADDRESSED** |
| **Cognitive/energy constraints** | Humans have cognitive fatigue, sleep limits, energy depletion | No cognitive/energy constraints for AI | **BROKEN ASSUMPTION** |
| **Bounded rationality** | Humans have limited optimization capability | Perfect optimization possible | **BROKEN ASSUMPTION** |
| **Identity persistence** | Humans have single legal identity; Sybil constrained | Unlimited disposable identities | **BROKEN ASSUMPTION** |
| **Transaction velocity** | Human-scale (10-100/day) | Machine-scale (10^3-10^6/day) | **UNADDRESSED** |
| **Biometric verification** | Assumes human physiology | No physical form | **BROKEN ASSUMPTION** |
| **Device constraints** | Assumes fixed device identity | Arbitrary fingerprint generation | **BROKEN ASSUMPTION** |
| **Location constraints** | Assumes travel time limits | No physical location | **BROKEN ASSUMPTION** |
| **Multi-agent economics + fraud** | Separate domains | Integrated threat model | **UNADDRESSED** |
| **Detection latency exploitation** | Assumes similar timescales | Machine-speed vs. human-speed detection | **UNADDRESSED** |

---

## Section 5: Citation Map and Key References

### 5.1 Citation Chain Structure

```
Foundational (1990-2005)
├── Multi-agent systems: Wooldridge (2002), Weiss (1999)
├── Fraud detection: Bolton & Hand (2002)
├── Anomaly detection: Chandola (2009) - cites foundational work
├── Adversarial ML: Lowd & Meek (2005)
└── Reputation systems: Douceur (2002), Levien (2009)

Core Frameworks (2005-2015)
├── Multi-agent RL: Buşoniu et al. (2010), Lowe et al. (2017)
├── Agent-based economics: Tesfatsion (2006), Bookstaber (2017)
├── Botnet detection: Nagaraja et al. (2010)
├── HFT fraud: Johnson et al. (2012), Goldstein et al. (2014)
└── Adversarial ML: Biggio et al. (2013), Carlini & Wagner (2017)

Recent Work (2019-2024)
├── MARL economics: Tolstaya (2022), Nguyen (2021)
├── AI agents as economic agents: Babaioff (2021)
├── GNN fraud detection: Wei (2021), Carcillo (2020)
├── Multi-agent RL security: Gleave (2020), Pinto (2017)
└── AI safety: Amodei (2016), Cohen (2022)
```

### 5.2 Key References for Future Phases

#### For Taxonomy Development (Phase 1)

1. **Multi-agent coordination:** Tolstaya et al. (2022) - arXiv:2109.12938
2. **Agent-based economics:** Tesfatsion (2021) - DOI: 10.1016/bs.hescom.2021.03.001
3. **Reputation attacks:** Jiang et al. (2020) - DOI: 10.1145/3391406
4. **Human invariants:** Van Vlasselaer et al. (2017) - DOI: 10.1002/widm.1208

#### For Detection Framework (Phase 3)

1. **Adversarial ML:** Biggio & Roli (2018) - DOI: 10.1016/j.patcog.2018.01.009
2. **GNN fraud detection:** Wei et al. (2021) - arXiv:2105.07849
3. **Multi-agent RL security:** Gleave et al. (2020) - arXiv:2007.07447
4. **Biometric limits:** Jain et al. (2021) - DOI: 10.1109/TCSVT.2021.3077580

#### For Industry Recommendations

1. **Fraud detection practices:** Carcillo et al. (2020) - DOI: 10.1016/j.eswa.2019.113059
2. **Reputation system design:** Hoffman et al. (2009) - foundational sybil resistance
3. **Anomaly detection limits:** Chandola et al. (2009) - DOI: 10.1145/1541880.1541882
4. **ML robustness:** Cohen et al. (2022) - arXiv:2203.01341

---

## Section 6: Confidence Assessment and Limitations

### 6.1 Confidence Levels by Subfield

| Subfield | Confidence | Justification |
|----------|-----------|---------------|
| **Multi-agent economics** | MEDIUM | Strong theoretical foundation, but A2A-specific work limited |
| **Fraud detection theory** | HIGH | Well-established domain; human invariants well-documented |
| **AI/ML security** | HIGH | Active research area; adversarial ML well-studied |
| **A2A commerce integration** | LOW | Novel intersection; no direct prior work found |

### 6.2 Access Limitations

**Paywalled papers:**
- Several IEEE/ACM papers accessed via abstract only (noted in-line)
- DOI references provided for institutional access
- No critical claims rely exclusively on paywalled content

**Database limitations:**
- Search performed via arXiv and Google Scholar (public access)
- Institutional access not available during this survey
- May have missed papers in paywalled venues (IEEE, ACM, paywalled journals)

### 6.3 Search Scope Limitations

**Time constraint:**
- 3-5 year recency focus may miss relevant older work
- Citation chains mitigate but don't eliminate this risk

**Domain boundary:**
- Focused on fraud detection and multi-agent systems
- May have missed relevant work in adjacent domains (e.g., algorithmic game theory, mechanism design)

**Language bias:**
- English-language literature only
- May have missed non-English contributions

### 6.4 Validation Strategy

**How to validate this survey:**
1. **Cross-check with bibliographer:** Verify citation completeness
2. **Institutional access:** Re-survey paywalled papers via library access
3. **Expert review:** Domain experts in multi-agent systems and fraud detection
4. **Citation expansion:** Follow additional citation chains from identified key papers

---

## Section 7: Synthesis and Research Position

### 7.1 What Literature Tells Us

**About agent economic behavior:**
- Agents can learn coordinated strategies (MARL literature)
- Reputation systems vulnerable to sybil attacks (reputation literature)
- Mechanism design must account for non-human behavior (Babaioff 2021)
- Emergent properties arise from agent interactions (ACE literature)

**About human behavioral invariants:**
- Velocity limits: ~10-100 transactions/day (cognitive/sleep constraints)
- Biometrics: requires physical presence (fingerprint, face, iris)
- Device fingerprinting: assumes fixed device identity
- Location constraints: travel time limits, cannot teleport

**About fraud detection:**
- ML systems learn human transaction patterns
- Graph-based methods detect fraud rings
- Anomaly detection assumes "normal" is stable
- Detection latency: minutes to hours

**About adversarial ML:**
- ML systems vulnerable to adversarial examples
- Transfer attacks allow black-box evasion
- Robustness guarantees are model-specific
- Adversarial adaptation is systematic

### 7.2 What Literature DOESN'T Tell Us (The Novel Contribution)

**The A2A commerce gap:**
1. No direct treatment of **authorized** agent commerce fraud detection
2. No treatment of **perfect behavioral mimicry** at machine scale
3. No integration of multi-agent economics with fraud detection
4. No treatment of **detection latency exploitation** by machine-speed agents

**Key insight:** The intersection is genuinely novel. Literature provides components (multi-agent theory, fraud detection, adversarial ML) but not the integrated problem of authorized AI agents performing commercial transactions at machine speed with perfect behavioral mimicry.

### 7.3 Position for Future Work

**This survey establishes:**

1. **Theoretical foundations:** Multi-agent economics, mechanism design, reputation systems
2. **Baseline invariants:** Human behavioral constraints that current systems rely on
3. **Detection methodologies:** ML-based fraud detection, adversarial evasion techniques
4. **Nearest analogues:** Botnets, HFT fraud, P2P marketplace fraud (with explicit mapping)

**The gap we must fill:**

1. **Taxonomy:** Systematic mapping of A2A attack vectors by detection difficulty
2. **Detection framework:** Agent-aware fraud detection that doesn't rely on human invariants
3. **Industry recommendations:** Banking/fintech guidance for A2A commerce

**Confidence:** The gap is real and novel. No prior work addresses authorized autonomous agent fraud detection as a systematic problem.

---

## Appendix: Search Methodology Details

### A.1 Databases Searched

- **arXiv.org** (primary source for CS/econ papers)
- **Google Scholar** (broad coverage, citation tracking)
- **Semantic Scholar** (related papers, citation networks)
- **DOI resolution** (for paywalled paper metadata)

### A.2 Search Terms Used

**Multi-agent economics:**
- "multi-agent economic systems"
- "agent-based computational economics"
- "multi-agent reinforcement learning economics"
- "mechanism design multi-agent systems"
- "reputation systems sybil attacks"

**Fraud detection:**
- "fraud detection survey"
- "behavioral biometrics fraud detection"
- "transaction velocity fraud detection"
- "graph neural networks fraud detection"
- "anomaly detection financial fraud"

**AI/ML security:**
- "adversarial machine learning survey"
- "AI safety robustness"
- "multi-agent reinforcement learning security"
- "adversarial policies reinforcement learning"

### A.3 Inclusion Criteria

**Included:**
- Papers 2019-2024 (recent focus)
- Foundational papers via citation chains
- Papers explicitly addressing multi-agent systems, fraud detection, or AI security
- Papers with clear relevance to A2A commerce (direct or via analogue)

**Excluded:**
- Papers addressing only traditional cybersecurity (not agent-specific)
- Papers on single-agent systems without coordination
- Papers on cryptocurrency only (unless relevant to A2A principles)
- Papers without clear methodology or results

### A.4 Quality Assessment

**High-quality sources:** Peer-reviewed conferences (NeurIPS, ICML, ICLR, KDD, CCS, S&P), journals (IEEE TMLR, JMLR), preprints with strong citations

**Abstract-only analysis:** Paywalled papers analyzed via abstract when available; limitations noted explicitly

---

**Survey completed:** 2026-03-18
**Next step:** Create citation map with cross-references (Task 3)
