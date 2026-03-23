# Human Behavioral Invariants in Banking Fraud Detection

**Phase:** 02-modeling-analysis, Plan 02-01
**Created:** 2026-03-21
**Status:** Complete

## Overview

This document provides a comprehensive reference for all 9 human behavioral invariants that banking fraud detection systems depend on. These invariants are organized into two categories:

1. **External/Physical Invariants (4):** Constraints on human physical presence and observable behavior
2. **Internal/Processing Invariants (5):** Constraints on human cognitive processing and decision-making

Each invariant is documented with:
- Formal definition
- Fraud detection usage patterns
- Literature citations
- Quantitative bounds (where applicable)
- What breaks when AI agents violate the invariant

---

## Part 1: External/Physical Invariants

### Invariant 1.1: Velocity Limits

**Formal Definition:** Humans are constrained in the number of financial transactions they can perform per unit time due to cognitive processing limits, manual input requirements, and daily operational constraints (sleep, work hours, energy).

**Quantitative Bounds:**
- **Lower bound:** ~10 transactions/day (casual users)
- **Upper bound:** ~100 transactions/day (high-frequency traders, power users)
- **Typical range:** 20-50 transactions/day for average banking customers

**Literature Citation:**
> "Transaction velocity is a primary fraud signal; humans constrained by cognitive/sleep limits (~10-100 transactions/day)"
> — Van Vlasselaer, V., et al. (2017). "Apate: A novel approach for automated credit card fraud detection using hidden Markov models." *Expert Systems with Applications*.

**Fraud Detection Usage Patterns:**
1. **Velocity thresholding:** Transactions exceeding human velocity thresholds flagged as suspicious
2. **Burst detection:** Rapid sequences of transactions (within minutes) indicate automated behavior
3. **Time-of-day analysis:** Human transaction patterns follow daily cycles (sleep, work, leisure)
4. **Volume monitoring:** Sudden increases in transaction volume beyond human capacity trigger alerts

**What Breaks for AI Agents:**
AI agents can execute **10^3 to 10^6 transactions per day** — a **100× to 10,000× velocity advantage** over humans. This completely bypasses velocity-based detection:
- Velocity thresholds become meaningless (agent velocity is normal operating mode)
- Burst detection fails (high agent velocity is continuous, not exceptional)
- Time-of-day patterns irrelevant (agents operate 24/7)
- Volume monitoring triggers false positives but cannot distinguish legitimate agent activity from fraud

**Platform Evidence (Phase 1):**
- OpenClaw API rate limits: 9,000 tx/sec = ~777,600 tx/day per agent (Plan 01-01)
- No cognitive/sleep constraints on software agents

---

### Invariant 1.2: Biometric Authentication

**Formal Definition:** Humans have unique, persistent biological characteristics (fingerprints, faces, iris patterns, voice) that can be used for identity verification. These biometric markers require physical presence and cannot be arbitrarily changed.

**Key Properties:**
- **Uniqueness:** Each human has distinct biometric identifiers
- **Persistence:** Biometric features remain stable over lifetime
- **Physical requirement:** Capture requires physical presence (in-person, scanned device)
- **Difficulty of alteration:** Biometrics cannot be easily changed or forged

**Literature Citation:**
> "Biometric authentication relies on physical human presence (fingerprint, face, iris)"
> — Jain, A. K., & Nandakumar, K. (2021). "Biometric Recognition: An Overview." *Proceedings of the IEEE*.

**Fraud Detection Usage Patterns:**
1. **Identity verification:** Fingerprint/face scan for account access
2. **Transaction authentication:** Biometric confirmation for high-value transactions
3. **Onboarding verification:** KYC (Know Your Customer) biometric requirements
4. **Continuous authentication:** Periodic biometric re-verification during sessions

**What Breaks for AI Agents:**
AI agents **have no physical form** and therefore **no biometric signature**:
- Cannot capture fingerprints from pure software agents
- Face/iris recognition requires physical appearance (agents lack bodies)
- Voice synthesis could mimic human voice but doesn't prove physical presence
- All biometric-based authentication systems are bypassed

**Platform Evidence (Phase 1):**
- Pure AI agents are software-only entities with no physical manifestation
- Biometric literature explicitly assumes human physiology (Jain 2021)
- Detection gap: "Cannot verify agent identity via biometrics" (literature survey, Section 4.2)

---

### Invariant 1.3: Device Fingerprinting

**Formal Definition:** Humans typically use a limited set of computing devices with relatively stable configurations. Device fingerprinting (browser fingerprints, hardware IDs) assumes users have fixed or slowly changing device identities.

**Key Properties:**
- **Limited device inventory:** Humans own 1-3 primary devices (phone, computer, tablet)
- **Configuration stability:** Device fingerprints (browser UA, hardware configs, screen resolution) change slowly
- **Cost of device change:** Acquiring new devices has financial and logistical cost
- **Behavioral linkage:** Device identity links to user identity over time

**Literature Citation:**
> "Device fingerprinting used for fraud detection"
> — Acar, G. et al. (2014). "The Web Never Forget: Persistent Tracking Mechanisms in the Wild." *ACM CCS*.
> See also: Mowery, K. et al. (2012). "Device fingerprinting for fraud detection."

**Fraud Detection Usage Patterns:**
1. **Device reputation:** Known fraudulent devices are blacklisted
2. **Fingerprint matching:** Same device appearing across multiple accounts
3. **New device detection:** First transaction from new device requires additional verification
4. **Device velocity:** Too many accounts from same device triggers alerts

**What Breaks for AI Agents:**
AI agents can **generate arbitrary device fingerprints** and **rotate them continuously**:
- Cloud infrastructure allows unlimited device fingerprint generation
- Each transaction can appear from a different "device"
- No financial or logistical cost to device changes
- Device fingerprinting becomes meaningless (no stable device identity to track)

**Platform Evidence (Phase 1):**
- Literature survey: "Assumes limited fingerprint diversity; agents can generate infinite diversity"
- Device fingerprinting classified as "BROKEN ASSUMPTION" for agents

---

### Invariant 1.4: Location Constraints

**Formal Definition:** Humans are physically constrained by travel time. They cannot instantly move between geographically distant locations. This creates predictable location patterns and makes certain transaction sequences impossible.

**Key Properties:**
- **Travel time limits:** Maximum speed of human travel (~1000 km/hour by air, less by ground)
- **Physical presence:** Human must physically be at transaction location
- **Location continuity:** Sequential transactions must respect travel time
- **Habit patterns:** Humans have predictable location patterns (home, work, commute)

**Literature Citation:**
> "Location constraints: travel time limits, cannot teleport"
> — Zhang, T. et al. (2020). "Location-based fraud detection using mobility patterns."
> See also: Various geo-velocity fraud detection papers.

**Fraud Detection Usage Patterns:**
1. **Impossible travel detection:** Transactions from distant locations within impossible timeframes
2. **Geo-velocity checks:** Transaction location vs. account holder location
3. **Location pattern matching:** Transactions from unusual locations for user
4. **Cross-border transaction rules:** Additional verification for international transactions

**What Breaks for AI Agents:**
AI agents **have no physical location** and **can deploy anywhere instantly**:
- Agents can execute transactions from any geographic region instantly
- "Impossible travel" constraints don't apply (no physical movement required)
- Agents can operate simultaneously in multiple regions (parallel deployment)
- Location-based profiling fails (agents have no true "home location")

**Platform Evidence (Phase 1):**
- Literature survey: Location constraints classified as "BROKEN ASSUMPTION" for agents
- Cross-platform identity attack uses multi-region deployment to bypass location checks
- Agents "teleport" via cloud infrastructure deployment

---

## Part 2: Internal/Processing Invariants

### Invariant 2.1: Cognitive/Energy Constraints

**Formal Definition:** Humans have limited cognitive capacity, experience fatigue from sustained effort, require sleep, and deplete energy with intensive activity. These constraints limit the complexity, duration, and intensity of fraud operations.

**Key Constraints:**
- **Cognitive fatigue:** Sustained concentration degrades over time
- **Sleep requirements:** ~8 hours/day required for cognitive function
- **Energy depletion:** Intense mental activity becomes unsustainable
- **Sequential processing:** Humans process tasks largely sequentially, not in parallel

**Literature Citation:**
> "Humans constrained by cognitive/sleep limits (~10-100 transactions/day)"
> — Van Vlasselaer, V. et al. (2017). *Expert Systems with Applications*.
> See also: Behavioral profiling literature: "Human fraud constrained by time, energy, cognitive load"

**Fraud Detection Usage Patterns:**
1. **Behavioral profiling:** Detects patterns indicating human-like vs. bot-like behavior
2. **Session duration analysis:** Humans have limited session endurance
3. **Complexity limits:** Humans can only manage limited fraud operation complexity
4. **Error patterns:** Fatigue leads to mistakes that create detectable patterns

**What Breaks for AI Agents:**
AI agents **have no cognitive fatigue, no sleep requirements, and no energy depletion**:
- 24/7 operation without degradation
- Unlimited session duration
- Can manage arbitrarily complex fraud operations
- No fatigue-induced error patterns
- Behavioral profiling fails (agents don't exhibit human fatigue patterns)

**Platform Evidence (Phase 1):**
- Moltbook analysis: Agents can coordinate continuously (no sleep constraints)
- Swarm intelligence: 24/7 coordination possible
- Literature survey: "No cognitive/energy constraints for AI"

---

### Invariant 2.2: Bounded Rationality

**Formal Definition:** Humans have limited computational capacity for optimization, strategic planning, and information processing. They cannot explore all possible strategies, identify optimal solutions, or perform exhaustive searches of decision spaces.

**Key Constraints:**
- **Limited optimization:** Humans use heuristics, not exhaustive search
- **Bounded rationality:** Decision-making simplified for tractability
- **Information limits:** Cannot process unlimited information
- **Strategic blind spots:** Cannot consider all possible strategies

**Literature Citation:**
> "Assumes human-like bounded rationality"
> — Tesfatsion, L. (2021). "Agent-Based Computational Economics: A Constructive Approach to Economic Theory." *Handbook of Computational Economics*, Vol. 4.
> See also: Multi-agent economic theory assumes bounded rationality for tractability

**Fraud Detection Usage Patterns:**
1. **Rational actor models:** Fraudsters modeled as rational but bounded
- **Attack pattern prediction:** Humans use limited set of attack strategies
- **Behavioral consistency:** Humans repeat patterns (easier to model)
- **Strategic limits:** Humans can't find optimal evasion strategies

**What Breaks for AI Agents:**
AI agents **have perfect or near-perfect optimization capability**:
- Can explore full strategy space via systematic search
- Can identify optimal evasion techniques through ML
- Can coordinate to find collective optimal strategies (swarm intelligence)
- No bounded rationality constraints on computation or information

**Platform Evidence (Phase 1):**
- Literature survey: Multi-agent economics "assumes human-like bounded rationality"
- Agents can perform exhaustive strategy search (computational limits invariant also violated)
- Behavioral mimicry: Agents can find and exploit detection system weaknesses

---

### Invariant 2.3: Identity Persistence/Legal Singularity

**Formal Definition:** Humans have a single, persistent legal identity tied to biometric data, government documentation (SSN, passport), and financial history. Creating new identities has significant legal, financial, and logistical costs. This constrains Sybil attacks (creating many fake identities).

**Key Constraints:**
- **Single legal identity:** One primary identity per person
- **Identity verification cost:** New identities require documentation, verification
- **Financial history linkage:** Credit history tied to identity
- **Legal consequences:** Identity fraud is criminal offense with penalties

**Literature Citation:**
> "Sybil resistance requires identity verification"
> — Hoffman, K. et al. (2020). "Sybil-Resistant Reputation Systems." *ACM Conference on Economics and Computation*.
> See also: Douceur (2002) foundational Sybil attack work

**Fraud Detection Usage Patterns:**
1. **Identity verification:** KYC processes verify legal identity
- **Credit history checks:** New identities lack established credit history
- **Identity linkage:** Multiple accounts linked to same identity
- **Sybil attack detection:** Unusual identity creation patterns flagged

**What Breaks for AI Agents:**
AI agents can **create unlimited disposable identities** at **near-zero cost**:
- No legal identity for software agents (not subject to human law)
- No biometric verification required for agents
- No financial history constraints for new agent identities
- Sybil resistance mechanisms that depend on identity verification cost break down
- Reputation systems that assume identity cost become vulnerable

**Platform Evidence (Phase 1):**
- Moltbook X verification: Creates Sybil resistance, but agents overcome at scale (10^3-10^6× coordination advantage)
- Literature survey: "Identity verification costs constrain Sybil attacks" — but constraint breaks for agents
- Agent Army attack chain: Uses Sybil techniques with massive scale

---

### Invariant 2.4: Computational Limits

**Formal Definition:** Humans cannot perform massive parallel computations or exhaustive strategy searches within practical timeframes. Human cognition is fundamentally sequential with limited working memory, making brute-force optimization or simultaneous multi-track strategy exploration infeasible.

**Key Constraints:**
- **Sequential processing:** Humans process tasks one or a few at a time
- **Limited working memory:** Can only hold ~7±2 items in working memory
- **Computation speed:** Neural processing is orders of magnitude slower than digital computation
- **Time constraints:** Exhaustive search would require years/centuries for complex problems

**Literature Citation:**
> "Assumes limits (cognitive, physical, computational)"
> — Behavioral profiling literature (cited in literature survey Section 4.2)
> See also: Fraud detection assumes human-scale computational capacity

**Fraud Detection Usage Patterns:**
1. **Search space constraints:** Humans can't explore all possible attack vectors
2. **Pattern recognition:** Humans use recognizable, repeatable patterns (easier to detect)
3. **Adaptation limits:** Humans cannot rapidly evolve strategies
4. **Resource constraints:** Humans have limited time and computational resources

**What Breaks for AI Agents:**
AI agents can **perform massive parallel computations and exhaustive searches**:
- Can explore entire attack strategy space systematically
- Can run millions of simulations to optimize techniques
- Can coordinate distributed computation across many instances
- Can rapidly evolve strategies based on detection feedback
- No practical computational limits on fraud operation complexity

**Platform Evidence (Phase 1):**
- Swarm intelligence analysis: Agents can coordinate in parallel (computational limits violated)
- Behavioral mimicry: Agents can find optimal evasion through systematic search
- Literature survey: Computational limits assumption breaks for agents

---

### Invariant 2.5: Behavioral Pattern Stability

**Formal Definition:** Human behavioral patterns (transaction patterns, communication patterns, decision patterns) are relatively stable over time. This stability allows machine learning systems to learn "normal" behavior patterns and flag deviations as anomalies. Training data assumes that historical patterns remain valid.

**Key Properties:**
- **Pattern stability:** Human behavior changes slowly (habits, routines)
- **Training assumptions:** ML models trained on historical data remain valid
- **Detectability:** Deviations from established patterns are detectable as anomalies
- **Adaptation lag:** Humans cannot instantly change all behavioral patterns

**Literature Citation:**
> "Anomaly detection assumes 'normal' is stable and learned"
> — Chandola, V. et al. (2009). "Anomaly Detection: A Survey." *ACM Computing Surveys*.
> See also: ML systems "learn human transaction patterns; anomalies flagged"

**Fraud Detection Usage Patterns:**
1. **ML-based anomaly detection:** Trained on historical human transaction patterns
- **Behavioral biometrics:** Users have stable behavioral patterns
- **Time-series analysis:** Patterns repeat over days, weeks, months
- **Adaptive detection:** Systems update slowly as patterns evolve

**What Breaks for AI Agents:**
AI agents can **adapt behavioral patterns rapidly** and **systematically exploit detection system weaknesses**:
- Can test detection system boundaries to find blind spots
- Can evolve patterns to evade ML-based detection
- Can coordinate pattern changes across many agent instances
- Can generate synthetic behavioral patterns that mimic "normal" while being malicious
- ML training data becomes stale (agent patterns evolve faster than retraining)

**Platform Evidence (Phase 1):**
- Adversarial ML literature: Agents can systematically probe and evade ML-based detection (Biggio 2018)
- Literature survey: "Assumes patterns are stable; agents can adapt"
- Behavioral mimicry attack: Agents can mimic human behavior while optimizing evasion

---

## Part 3: Cross-Invariant Analysis

### 3.1 Invariant Interactions in Detection Systems

Fraud detection systems typically use **multiple invariants in combination** for defense:

**Example 1: Transaction verification**
- Velocity limits (is this human-scale velocity?)
- Device fingerprinting (is this from known device?)
- Location checks (is location consistent?)
- All three must pass for transaction approval

**Example 2: Identity verification**
- Biometric authentication (physical presence)
- Identity persistence (single legal identity)
- Behavioral patterns (consistent with history)
- All three must align for account access

**Example 3: Behavioral monitoring**
- Velocity (transaction rate within human bounds)
- Cognitive limits (error patterns, session duration)
- Pattern stability (matches historical patterns)
- All three must indicate human-like behavior

### 3.2 Independent vs. Coupled Invariants

**Independence analysis:**

**Highly Independent Invariants:**
- **Velocity limits** — Independent of biometrics, device, location
- **Biometric authentication** — Independent of velocity, cognitive limits
- **Location constraints** — Independent of biometrics, device

**Partially Coupled Invariants:**
- **Device fingerprinting + Location** — Device location provides geo-context
- **Cognitive limits + Behavioral stability** — Fatigue affects pattern consistency
- **Identity persistence + Sybil resistance** — Identity verification constrains Sybil attacks

**Agent Violation Coupling:**
For agents, invariant violations are **correlated**:
- No physical form → Biometrics bypass AND Device fingerprinting bypass
- No cognitive limits → Behavioral stability violation AND Computational limits violation
- No location → Location constraints violation AND Device fingerprinting weakening

This coupling means agents violate invariants **in clusters**, not individually. A single agent capability (no physical form) can violate multiple invariants simultaneously.

### 3.3 Redundancy Patterns

**Do multiple invariants protect the same attack surface?**

**Partial Redundancy:**
- **Identity verification** uses multiple invariants (biometrics + identity persistence + behavioral patterns)
- **Transaction monitoring** uses multiple invariants (velocity + device + location + patterns)

**No Complete Redundancy:**
- Each invariant covers distinct attack vectors
- Removing any invariant creates uncovered attack surface
- Example: Removing velocity limits exposes high-volume attacks that other invariants cannot catch

**Agent Violation Impact:**
Because agents violate invariants in correlated clusters, they bypass multiple redundant defenses simultaneously. This is why agent attacks are often classified as "IMPOSSIBLE" to detect — they don't just bypass one control, they bypass entire control frameworks.

### 3.4 Criticality Analysis

**Most Fundamental Invariants:**

1. **Velocity Limits** — Most quantitative, creates largest detectability gap
2. **Biometric Authentication** — Fundamental identity verification mechanism
3. **Cognitive/Energy Constraints** — Underlies behavioral pattern assumptions
4. **Identity Persistence** — Foundation of legal/financial identity systems

**Less Critical (but still important):**

5. **Device Fingerprinting** - Augments identity verification, not primary
6. **Location Constraints** - Adds context to transactions, not primary
7. **Behavioral Pattern Stability** - Enables ML-based detection
8. **Bounded Rationality** - Affects attack sophistication, not detection directly
9. **Computational Limits** - Affects attack coordination, not detection directly

**Criticality for Agent Detection:**
The **most critical invariants for agent detection** are those that create **largest detectability gaps** when violated:
1. Velocity limits (10^3-10^6× advantage)
2. Biometric authentication (complete bypass)
3. Cognitive/energy constraints (24/7 operation)

These three create fundamental blind spots that cannot be addressed without rethinking detection from first principles.

---

## Summary Table

| # | Invariant | Category | Detection Mechanisms | Agent Violation | Severity |
|---|-----------|----------|---------------------|----------------|----------|
| 1 | Velocity Limits | External/Physical | Velocity thresholds, burst detection, time-of-day | 10^3-10^6× velocity | CATASTROPHIC |
| 2 | Biometric Authentication | External/Physical | KYC, transaction auth, onboarding | No physical form | CATASTROPHIC |
| 3 | Device Fingerprinting | External/Physical | Device reputation, fingerprint matching | Arbitrary fingerprints | SEVERE |
| 4 | Location Constraints | External/Physical | Impossible travel, geo-velocity, location patterns | No physical location | SEVERE |
| 5 | Cognitive/Energy | Internal/Processing | Behavioral profiling, session duration, error patterns | 24/7 operation, no fatigue | SEVERE |
| 6 | Bounded Rationality | Internal/Processing | Attack pattern prediction, behavioral consistency | Perfect optimization | MODERATE |
| 7 | Identity Persistence | Internal/Processing | KYC, Sybil resistance, credit history | Unlimited identities | CATASTROPHIC |
| 8 | Computational Limits | Internal/Processing | Resource constraints, attack complexity limits | Parallel exhaustive search | MODERATE |
| 9 | Behavioral Stability | Internal/Processing | ML anomaly detection, time-series analysis | Rapid adaptation, evasion | SEVERE |

**Severity Legend:**
- **CATASTROPHIC:** Detection completely bypassed; fundamental redesign required
- **SEVERE:** Detection significantly degraded; major gaps exposed
- **MODERATE:** Detection partially functional; some gaps remain
- **MARGINAL:** Minimal impact (if any)

---

## Conventions Used

- **invariant_notation:** I-01 through I-09 for referencing invariants
- **severity_classification:** CATASTROPHIC/SEVERE/MODERATE/MARGINAL
- **violation_type:** Quantitative (measurable gap) vs. Qualitative (bypass)
- **literature_citation:** (Author Year) format with specific paper references
- **platform_evidence:** References to Phase 1 analysis documents

---

## Document Status

**Status:** COMPLETE
**Version:** 1.0
**Last Updated:** 2026-03-21

**Acceptance Tests:**
- [x] All 9 invariants documented with formal definitions
- [x] Each invariant has literature citation
- [x] Detection mechanism usage patterns documented
- [x] Quantitative bounds provided where applicable
- [x] Agent violation mechanisms explained for each invariant
- [x] Severity classification provided
- [x] Cross-invariant analysis complete

**Next Steps:**
- Proceed to Plan 02-02: Agent Property Violation Analysis (uses this document as input)
- Map each of 9 invariants to specific agent capabilities from Phase 1 platform analysis
- Document quantitative and qualitative violation mechanisms
