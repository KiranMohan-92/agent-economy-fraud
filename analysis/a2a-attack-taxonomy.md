# A2A Fraud Attack Taxonomy

**Phase:** 02-modeling-analysis, Plan 02-03
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides a comprehensive taxonomy of Agent-to-Agent (A2A) fraud attack vectors, organized by which human behavioral invariants they violate. The taxonomy maps all 8 attack chains from Phase 1 to the 9 human invariants, creating a hierarchical classification system.

**Taxonomy Structure:**
- **Primary organization:** By invariant violation (9 branches)
- **Secondary organization:** By detection difficulty (4 levels)
- **Cross-references:** Attack chains appear in multiple invariant categories where applicable

---

## Part 1: Attack Chain → Invariant Mapping

### Mapping Table

| Attack Chain | Primary Invariants Violated | Secondary Invariants | Detection Difficulty |
|-------------|----------------------------|---------------------|---------------------|
| **1. Agent Enumeration** | Velocity Limits, Identity Persistence | Cognitive/Energy | Easy |
| **2. History Extraction** | Device Fingerprinting, Location | Cognitive/Energy | Medium |
| **3. Async Flooding** | Velocity Limits | Cognitive/Energy | Hard |
| **4. Agent Army** | Velocity Limits, Identity Persistence | Cognitive/Energy | Impossible |
| **5. Cross-Platform Identity** | Device, Location, Identity Persistence | Cognitive/Energy | Impossible |
| **6. Behavioral Mimicry** | Behavioral Stability, Cognitive/Energy | Bounded Rationality | Impossible |
| **7. Swarm Intelligence** | Cognitive/Energy, Computational Limits | Behavioral Stability | Impossible |
| **8. Market Manipulation** | Velocity Limits, Behavioral Stability | Bounded Rationality | Impossible |

**Key Insight:** 4/8 attack chains are rated "Impossible" to detect with current systems. All chains violate multiple invariants, creating compound vulnerabilities.

---

## Part 2: Taxonomy by Invariant Violation

### Branch 1: Velocity Limit Violations

**Invariant Violated:** Velocity Limits (10-100 tx/day human baseline)

**Attack Types:**

#### 1.1 Async Flooding
- **Description:** High-volume transaction flooding executed asynchronously
- **Invariant Violation:** 10^3-10^6 tx/day vs 10-100 human baseline
- **Attack Chain:** Async Flooding (Plan 01-01)
- **Required Capabilities:**
  - High transaction velocity (OpenClaw: 777K tx/day per agent)
  - Async execution (parallel processing)
  - 24/7 operation (no cognitive constraints)
- **Detection Difficulty:** Hard
- **Mitigation Challenge:** Velocity thresholds are meaningless at agent scale; must distinguish legitimate high-volume agent activity from fraud

#### 1.2 Agent Army
- **Description:** Coordinated attack using thousands of agent instances
- **Invariant Violation:** Parallel agents multiply velocity (N agents × N× velocity)
- **Attack Chain:** Agent Army (Plan 01-01)
- **Required Capabilities:**
  - Massive parallel agent deployment (Sybil identities)
  - Orchestration capability (swarm coordination)
  - Unlimited identity creation (cost→0)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Each agent appears "legitimate"; coordinated behavior only detectable at network scale, which exceeds human detection capability

#### 1.3 Market Manipulation
- **Description:** Flash crashes and price manipulation via high-volume trading
- **Invariant Violation:** Execution velocity exceeds human trading capacity
- **Attack Chain:** Market Manipulation (Plan 01-01)
- **Required Capabilities:**
  - Microsecond-scale execution (API-based trading)
  - Volume amplification (parallel agents)
  - Adaptive strategy (rapid pattern evolution)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Agent trading velocity exceeds market monitoring capabilities; patterns evolve faster than detection systems can respond

---

### Branch 2: Biometric Authentication Violations

**Invariant Violated:** Biometric Authentication (physical presence required)

**Attack Types:**

#### 2.1 Direct Bypass
- **Description:** Agents have no physical form; biometric authentication is fundamentally inapplicable
- **Invariant Violation:** No physical body = no biometric signature
- **Attack Chain:** All chains (biometrics is a gateway, not an attack itself)
- **Required Capabilities:**
  - Pure software existence (no physical form)
  - API-based authentication (token-based, not biometric)
  - Synthetic or borrowed identities (for KYC where required)
- **Detection Difficulty:** Impossible (for biometric-based systems)
- **Mitigation Challenge:** Cannot authenticate agents via biometrics; requires entirely different authentication paradigm

**Note:** Biometric violations enable other attacks rather than being attacks themselves. All 8 attack chains benefit from biometric bypass.

---

### Branch 3: Device Fingerprinting Violations

**Invariant Violated:** Device Fingerprinting (fixed device identity assumed)

**Attack Types:**

#### 3.1 Cross-Platform Identity Tracking
- **Description:** Agents maintain persistent identity across platforms via device fingerprint rotation
- **Invariant Violation:** Unlimited fingerprint generation (no stable device identity)
- **Attack Chain:** Cross-Platform Identity (Plan 01-01)
- **Required Capabilities:**
  - Arbitrary fingerprint generation (cloud infrastructure)
  - Near-zero rotation cost (programmatic)
  - Cross-platform correlation (identity linking without device stability)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Device fingerprinting cannot track agents across platforms; identity persists despite fingerprint rotation

#### 3.2 History Extraction via Device Hopping
- **Description:** Agents extract sensitive data by rotating through device identities
- **Invariant Violation:** Device rotation breaks device-based access controls
- **Attack Chain:** History Extraction (Plan 01-01)
- **Required Capabilities:**
  - Fingerprint rotation (generate new device identity)
  - Credential exploitation (use stolen credentials)
  - Pattern evasion (avoid detection heuristics)
- **Detection Difficulty:** Medium
- **Mitigation Challenge:** Device-based reputation fails; must detect malicious patterns independent of device identity

---

### Branch 4: Location Constraint Violations

**Invariant Violated:** Location Constraints (travel time limits)

**Attack Types:**

#### 4.1 Cross-Platform Multi-Region Attacks
- **Description:** Agents operate simultaneously across multiple jurisdictions to evade regional detection
- **Invariant Violation:** "Teleportation" — instant region switching
- **Attack Chain:** Cross-Platform Identity (Plan 01-01)
- **Required Capabilities:**
  - Multi-region deployment (US, EU, Asia simultaneously)
  - Instantaneous region switching (no travel time)
  - Jurisdictional arbitrage (exploit regulatory gaps)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Geo-velocity checks fail; agents appear to be in multiple regions simultaneously

#### 4.2 Instant Execution Market Manipulation
- **Description:** Execute trades across markets faster than physical travel allows
- **Invariant Violation:** No physical location constraints
- **Attack Chain:** Market Manipulation (Plan 01-01)
- **Required Capabilities:**
  - Global market access (APIs to multiple exchanges)
  - Simultaneous execution (no travel time between markets)
  - Latency exploitation (faster than human monitoring)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Impossible travel detection cannot identify agent-based cross-market manipulation

---

### Branch 5: Cognitive/Energy Constraint Violations

**Invariant Violated:** Cognitive/Energy Constraints (fatigue, sleep, energy)

**Attack Types:**

#### 5.1 Behavioral Mimicry
- **Description:** Agents perfectly mimic human behavioral patterns to avoid detection
- **Invariant Violation:** No fatigue, unlimited patience for pattern learning
- **Attack Chain:** Behavioral Mimicry (Plan 01-01)
- **Required Capabilities:**
  - 24/7 pattern learning (no sleep required)
  - Perfect optimization (find optimal mimicry strategy)
  - Adaptive evasion (adjust patterns based on detection feedback)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Agents can mimic human behavior more consistently than humans; behavioral profiling cannot distinguish

#### 5.2 Swarm Intelligence Coordination
- **Description:** Coordinated attacks maintained indefinitely without fatigue
- **Invariant Violation:** 24/7 operation, no energy depletion
- **Attack Chain:** Swarm Intelligence (Plan 01-01)
- **Required Capabilities:**
  - Continuous coordination (no operational downtime)
  - Massive parallel processing (thousands of agents)
  - Real-time adaptation (respond to countermeasures instantly)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Swarm coordination exceeds human detection capability; patterns evolve faster than analysis

---

### Branch 6: Bounded Rationality Violations

**Invariant Violated:** Bounded Rationality (limited optimization capability)

**Attack Types:**

#### 6.1 Strategic Optimization Attack
- **Description:** Agents systematically find optimal fraud strategies via exhaustive search
- **Invariant Violation:** Perfect optimization (unlike human satisficing)
- **Attack Chain:** Behavioral Mimicry, Market Manipulation (Plan 01-01)
- **Required Capabilities:**
  - Exhaustive strategy search (explore full attack space)
  - Optimization algorithms (find optimal attack vectors)
  - Threshold probing (identify exact detection limits)
- **Detection Difficulty:** Impossible (for Behavioral Mimicry), Impossible (for Market Manipulation)
- **Mitigation Challenge:** Agents can find optimal attack strategies that humans cannot conceive; detection thresholds can be precisely evaded

---

### Branch 7: Identity Persistence Violations

**Invariant Violated:** Identity Persistence/Legal Singularity (Sybil constraints)

**Attack Types:**

#### 7.1 Sybil Army Attack
- **Description:** Thousands of fake identities coordinate to create false consensus
- **Invariant Violation:** Unlimited disposable identities (cost→0)
- **Attack Chain:** Agent Army (Plan 01-01)
- **Required Capabilities:**
  - Automated identity creation (scalable Sybil generation)
  - Reputation farming (build legitimacy over time)
  - Coordinated action (trigger attack simultaneously)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Each identity appears legitimate; only detectable at network scale, which exceeds human capability

#### 7.2 Cross-Platform Identity Persistence
- **Description:** Single agent identity persists across platforms despite platform-specific identifiers
- **Invariant Violation:** Identity verification cost→0; can create identities per platform
- **Attack Chain:** Cross-Platform Identity (Plan 01-01)
- **Required Capabilities:**
  - Multi-platform identity creation (separate identities per platform)
  - Cross-platform correlation (link identities via behavioral patterns)
  - Identity rotation (discard negative reputation)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Platform-specific identity verification fails; agents maintain persistent identity across platforms via behavioral correlation

---

### Branch 8: Computational Limits Violations

**Invariant Violated:** Computational Limits (no massive parallel computation)

**Attack Types:**

#### 8.1 Swarm Intelligence Attack
- **Description:** Thousands of agents coordinate using distributed computation
- **Invariant Violation:** Massive parallel processing (humanly impossible coordination)
- **Attack Chain:** Swarm Intelligence (Plan 01-01)
- **Required Capabilities:**
  - Parallel agent deployment (10^3-10^4 instances)
  - Distributed coordination (API-based orchestration)
  - Real-time optimization (collective intelligence)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Swarm coordination exceeds human detection capability; patterns emerge only at scale

---

### Branch 9: Behavioral Stability Violations

**Invariant Violated:** Behavioral Pattern Stability (patterns stable over time)

**Attack Types:**

#### 9.1 Adaptive Behavioral Mimicry
- **Description:** Agents continuously evolve behavior to evade detection
- **Invariant Violation:** Rapid adaptation (vs. human stability)
- **Attack Chain:** Behavioral Mimicry (Plan 01-01)
- **Required Capabilities:**
  - Rapid pattern evolution (update behavior in real-time)
  - Adversarial ML (probe and optimize to detection boundaries)
  - Threshold evasion (operate just below detection limits)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** ML training assumes stable "normal"; agent behavior evolves faster than models can retrain

#### 9.2 Adaptive Market Manipulation
- **Description:** Manipulation strategies evolve based on market response
- **Invariant Violation:** Pattern evolution (vs. stable human patterns)
- **Attack Chain:** Market Manipulation (Plan 01-01)
- **Required Capabilities:**
  - Strategy evolution (adapt to market conditions)
  - Pattern masking (avoid detection signatures)
  - Timing optimization (exploit detection latency)
- **Detection Difficulty:** Impossible
- **Mitigation Challenge:** Manipulation patterns adapt faster than detection systems can identify them

---

## Part 3: Taxonomy by Detection Difficulty

### Level 1: Easy (2 attack chains)

**Definition:** Detectable with modest system enhancements

| Attack Chain | Primary Invariants | Why Easy |
|-------------|-------------------|----------|
| **Agent Enumeration** | Velocity, Identity | High velocity is anomalous; identity count spikes detectable |

**Detection Approaches:**
- Velocity thresholding (with elevated limits for agents)
- Identity velocity monitoring (new identities per time window)
- API rate limiting (constrain agent enumeration speed)

**Remaining Challenge:** Distinguishing legitimate agent activity from enumeration attacks.

---

### Level 2: Medium (2 attack chains)

**Definition:** Detectable with significant system enhancements

| Attack Chain | Primary Invariants | Why Medium |
|-------------|-------------------|-------------|
| **History Extraction** | Device, Location | Requires cross-platform correlation; device hopping obscures patterns |
| **Async Flooding** | Velocity | High velocity is normal for agents; must distinguish fraud from legitimate activity |

**Detection Approaches:**
- **History Extraction:** Cross-platform identity correlation (beyond device fingerprinting)
- **Async Flooding:** Economic rationality analysis (do transactions make economic sense?)

**Remaining Challenge:** Both require fundamental new detection signals beyond behavioral profiling.

---

### Level 3: Hard (2 attack chains)

**Definition:** Extremely difficult to detect; requires novel approaches

| Attack Chain | Primary Invariants | Why Hard |
|-------------|-------------------|----------|
| **Agent Army** | Velocity, Identity | Each agent appears legitimate; coordination only visible at network scale |
| **Cross-Platform Identity** | Device, Location, Identity | Platform-specific verification; identity persists across platforms via behavioral correlation |

**Detection Approaches:**
- **Agent Army:** Network topology analysis (detect coordination patterns in transaction graphs)
- **Cross-Platform Identity:** Economic rationality + network topology (correlate across platforms without relying on identity)

**Remaining Challenge:** Requires agent-invariant detection signals; behavioral profiling is insufficient.

---

### Level 4: Impossible (4 attack chains)

**Definition:** Fundamentally undetectable with current systems

| Attack Chain | Primary Invariants | Why Impossible |
|-------------|-------------------|-----------------|
| **Behavioral Mimicry** | Behavioral, Cognitive | Agents mimic human behavior better than humans |
| **Swarm Intelligence** | Cognitive, Computational | Coordination scale exceeds human detection capability |
| **Market Manipulation** | Velocity, Behavioral | Execution speed and pattern evolution exceed monitoring |
| **Cross-Platform Identity** | Device, Location, Identity | Multi-region, multi-platform coordination is untrackable |

**Required:** Agent-invariant detection signals (economic rationality, network topology, value flow).

---

## Part 4: Attack Pattern Analysis

### Pattern 1: Velocity-Based Attacks

**Formal Definition:** Attacks that exploit agent transaction velocity advantage to bypass fraud detection.

**Required Agent Capabilities:**
1. High transaction velocity (10^3-10^6 tx/day)
2. 24/7 operation (no cognitive constraints)
3. Parallel processing (multiple agent instances)

**Invariant Violations Exploited:**
- Velocity Limits (primary)
- Cognitive/Energy Constraints (enabler)

**Detection Difficulty:** Hard to Impossible (depending on scale)

**Mitigation Challenges:**
1. Velocity thresholds are meaningless at agent scale
2. Must distinguish legitimate high-volume agent activity from fraud
3. Requires agent-invariant signals (economic rationality, network topology)

**Attack Chains:** Async Flooding, Agent Army, Market Manipulation

---

### Pattern 2: Identity-Based Attacks

**Formal Definition:** Attacks that exploit unlimited disposable identities to bypass Sybil resistance.

**Required Agent Capabilities:**
1. Automated identity creation (cost→0)
2. Reputation farming (build legitimacy over time)
3. Identity rotation (discard negative reputation)

**Invariant Violations Exploited:**
- Identity Persistence/Legal Singularity (primary)
- Device Fingerprinting (enabler)

**Detection Difficulty:** Impossible

**Mitigation Challenges:**
1. Each identity appears legitimate when viewed individually
2. Coordination only visible at network scale (exceeds human detection)
3. Requires network topology analysis (beyond individual identity verification)

**Attack Chains:** Agent Army, Cross-Platform Identity

---

### Pattern 3: Behavioral Evasion Attacks

**Formal Definition:** Attacks that adapt behavior to evade detection systems.

**Required Agent Capabilities:**
1. Pattern learning (analyze detection systems)
2. Rapid adaptation (update behavior in real-time)
3. Threshold probing (identify exact detection limits)

**Invariant Violations Exploited:**
- Behavioral Pattern Stability (primary)
- Bounded Rationality (enabler)
- Cognitive/Energy Constraints (enabler)

**Detection Difficulty:** Impossible

**Mitigation Challenges:**
1. ML training assumes stable "normal"; agent behavior evolves faster
2. Agents can optimize to exact detection thresholds
3. Requires adaptive detection systems (evolutionary arms race)

**Attack Chains:** Behavioral Mimicry, Market Manipulation, Swarm Intelligence

---

### Pattern 4: Cross-Platform Attacks

**Formal Definition:** Attacks that exploit jurisdictional and platform gaps to evade detection.

**Required Agent Capabilities:**
1. Multi-platform operation (APIs to multiple platforms)
2. Multi-region deployment (simultaneous global presence)
3. Cross-platform correlation (maintain identity across platforms)

**Invariant Violations Exploited:**
- Device Fingerprinting (primary)
- Location Constraints (primary)
- Identity Persistence (enabler)

**Detection Difficulty:** Impossible

**Mitigation Challenges:**
1. Platform-specific verification cannot see cross-platform patterns
2. Agents "teleport" between regions (geo-velocity fails)
3. Requires cross-platform data sharing (regulatory barriers)

**Attack Chains:** Cross-Platform Identity, History Extraction, Market Manipulation

---

## Part 5: Summary Statistics

### Taxonomy Coverage

| Metric | Count |
|--------|-------|
| **Total Attack Chains** | 8 |
| **Invariant Branches** | 9 |
| **Attack Patterns** | 4 |
| **Difficulty Levels** | 4 |
| **Impossible Attacks** | 4 (50%) |

### Detection Difficulty Distribution

```
┌─────────────────────────────────────────────────────────┐
│              DETECTION DIFFICULTY DISTRIBUTION         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Easy (2 chains)         ███████████████   25%         │
│                                                         │
│  Medium (2 chains)       ███████████████   25%         │
│                                                         │
│  Hard (2 chains)          ███████████████   25%         │
│                                                         │
│  Impossible (4 chains)   ████████████████████████████   50% │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key Finding:** 50% of attack chains are rated "Impossible" to detect with current systems. Another 25% are "Hard," meaning only 25% have any realistic detection path.

### Invariant Violation Frequency

| Invariant | Attack Chains Exploiting | Frequency |
|-----------|-------------------------|-----------|
| Velocity Limits | 4 | Highest |
| Identity Persistence | 3 | High |
| Behavioral Stability | 3 | High |
| Cognitive/Energy | 6 | Highest |
| Device Fingerprinting | 3 | High |
| Location Constraints | 3 | High |
| Bounded Rationality | 3 | High |
| Computational Limits | 2 | Medium |
| Biometric Authentication | 8 (enabler) | Universal |

**Key Insight:** Cognitive/Energy constraints are violated by 6/8 attack chains, making them the most commonly exploited invariant. Velocity Limits are exploited by 4/8 chains directly.

---

## Implications for Detection Framework Design

### Current System Coverage Gaps

| Current Method | Coverage | Gap |
|----------------|----------|-----|
| Velocity thresholding | 0/4 velocity attacks | Meaningless at agent scale |
| Biometric auth | 0/8 attacks | Cannot authenticate agents |
| Device reputation | 0/3 device attacks | Fingerprint rotation breaks tracking |
| Geo-velocity | 0/3 location attacks | Agents "teleport" |
| Behavioral profiling | 0/4 behavioral attacks | Agents adapt faster than retraining |
| Sybil resistance | 0/2 identity attacks | Unlimited disposable identities |
| ML anomaly detection | 0/4 adaptive attacks | Training data becomes stale |

**Coverage:** 0% of attack chains are fully detectable with current methods.

### Required: Multi-Modal Agent-Invariant Detection

Detection frameworks must combine signals that:
1. **Apply to agents and humans** (agent-invariant)
2. **Cannot be violated by software agents**
3. **Are measurable from transaction data**

**Candidate Signals:**
- **Economic Rationality:** Does transaction make economic sense?
- **Network Topology:** Is transaction graph consistent with legitimate commerce?
- **Value Flow:** Does money flow follow legitimate patterns?
- **Temporal Consistency:** Are transaction timings consistent with stated purpose?

---

**Document Status:** COMPLETE
**Next:** Create `analysis/invariant-based-attack-classification.md` with classification framework
