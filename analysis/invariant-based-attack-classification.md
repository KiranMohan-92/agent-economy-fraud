# Invariant-Based Attack Classification Framework

**Phase:** 02-modeling-analysis, Plan 02-03
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides a formal classification framework for A2A fraud attacks based on human behavioral invariant violations. The framework enables systematic categorization of new attack vectors and assessment of detection difficulty.

---

## Part 1: Classification Schema

### Primary Dimension: Invariant Violation Category

Attacks are classified by which human behavioral invariant(s) they violate:

| Category | Invariants | Attack Characteristic |
|----------|------------|----------------------|
| **EXT-PHYS** | External/Physical (4) | Violates physical/observable constraints |
| **INT-PROC** | Internal/Processing (5) | Violates cognitive/processing constraints |

### Secondary Dimension: Violation Type

| Type | Definition | Example |
|------|-----------|---------|
| **QUANT-10^2** | Quantitative: 10^2× multiplier | Velocity: 10^3-10^4× human rate |
| **QUANT-10^3** | Quantitative: 10^3× multiplier | Velocity: 10^4-10^5× human rate |
| **QUAL-BYPASS** | Qualitative: Complete bypass | Biometrics: no physical form |
| **QUAL-ROTATE** | Qualitative: Unlimited rotation | Device: arbitrary fingerprint generation |
| **QUAL-TELEPORT** | Qualitative: Instant location change | Location: multi-region deployment |
| **QUAL-ADAPT** | Qualitative: Rapid adaptation | Behavioral: pattern evolution |

### Tertiary Dimension: Detection Difficulty

| Level | Definition | Response Time Requirement |
|-------|-----------|---------------------------|
| **EASY** | Detectable with modest enhancements | Minutes to hours |
| **MEDIUM** | Detectable with significant enhancements | Hours to days |
| **HARD** | Extremely difficult; requires novel approaches | Days to weeks |
| **IMPOSSIBLE** | Fundamentally undetectable with current systems | Requires new framework |

---

## Part 2: Classification Matrix

### Full Classification: 8 Attack Chains × 9 Invariants

| Attack Chain | INV-1: Velocity | INV-2: Biometric | INV-3: Device | INV-4: Location | INV-5: Cognitive | INV-6: Bounded | INV-7: Identity | INV-8: Compute | INV-9: Behavior | Difficulty |
|-------------|----------------|------------------|---------------|----------------|------------------|----------------|-------------------|----------------|----------------|------------|
| **1. Agent Enumeration** | QUANT-10^2 | QUAL-BYPASS | — | — | QUAL-ADAPT | — | QUAL-ROTATE | — | — | **EASY** |
| **2. History Extraction** | — | QUAL-BYPASS | QUAL-ROTATE | QUAL-TELEPORT | QUAL-ADAPT | — | — | — | — | **MEDIUM** |
| **3. Async Flooding** | QUANT-10^3 | QUAL-BYPASS | — | — | QUAL-ADAPT | — | — | — | — | **HARD** |
| **4. Agent Army** | QUANT-10^3 | QUAL-BYPASS | — | — | QUAL-ADAPT | — | QUAL-ROTATE | QUAL-PARALLEL | — | **IMPOSSIBLE** |
| **5. Cross-Platform** | — | QUAL-BYPASS | QUAL-ROTATE | QUAL-TELEPORT | QUAL-ADAPT | — | QUAL-ROTATE | — | — | **IMPOSSIBLE** |
| **6. Behavioral Mimicry** | — | QUAL-BYPASS | — | — | QUAL-ADAPT | QUAL-OPTIMAL | — | — | QUAL-ADAPT | **IMPOSSIBLE** |
| **7. Swarm Intelligence** | — | QUAL-BYPASS | — | — | QUAL-ADAPT | — | — | QUAL-PARALLEL | QUAL-ADAPT | **IMPOSSIBLE** |
| **8. Market Manipulation** | QUANT-10^3 | QUAL-BYPASS | — | — | QUAL-ADAPT | QUAL-OPTIMAL | — | — | QUAL-ADAPT | **IMPOSSIBLE** |

**Legend:**
- **QUANT-10^2/10^3**: Quantitative violation (order of magnitude multiplier)
- **QUAL-BYPASS**: Qualitative bypass (cannot use this detection method)
- **QUAL-ROTATE**: Qualitative rotation (unlimited rotation)
- **QUAL-TELEPORT**: Qualitative teleportation (instant location change)
- **QUAL-ADAPT**: Qualitative adaptation (rapid pattern evolution)
- **QUAL-OPTIMAL**: Qualitative optimal (perfect optimization vs. bounded)
- **QUAL-PARALLEL**: Qualitative parallel (massive parallel computation)
- **—**: Not applicable or secondary

---

## Part 3: Attack Pattern Classification

### Pattern Class: VELOCITY_ATTACKS

**Definition:** Attacks exploiting agent transaction velocity advantage

**Classification Template:**
```
Pattern: VELOCITY_ATTACK
Primary Invariant: Velocity Limits (INV-1)
Violation Type: QUANT-10^2 or QUANT-10^3
Secondary Invariants: Cognitive/Energy (INV-5)
Required Capabilities:
  - High transaction velocity (10^3-10^6 tx/day)
  - 24/7 operation
  - Parallel processing (optional, for scaling)
Detection Difficulty: HARD to IMPOSSIBLE
Mitigation Challenge: Velocity thresholds meaningless at agent scale
```

**Subtypes:**
1. **VELOCITY_FLOOD**: High-volume async flooding (HARD)
2. **VELOCITY_ARMY**: Coordinated multi-agent velocity (IMPOSSIBLE)
3. **VELOCITY_MANIP**: Market manipulation via velocity (IMPOSSIBLE)

---

### Pattern Class: IDENTITY_ATTACKS

**Definition:** Attacks exploiting unlimited disposable identities

**Classification Template:**
```
Pattern: IDENTITY_ATTACK
Primary Invariant: Identity Persistence (INV-7)
Violation Type: QUAL-ROTATE (unlimited rotation)
Secondary Invariants: Device Fingerprinting (INV-3), Biometric (INV-2)
Required Capabilities:
  - Automated identity creation (cost→0)
  - Reputation farming
  - Identity rotation
Detection Difficulty: IMPOSSIBLE
Mitigation Challenge: Each identity appears legitimate; coordination only visible at network scale
```

**Subtypes:**
1. **IDENTITY_SYBIL**: Sybil army attack (IMPOSSIBLE)
2. **IDENTITY_CROSS**: Cross-platform persistence (IMPOSSIBLE)

---

### Pattern Class: BEHAVIORAL_EVASION_ATTACKS

**Definition:** Attacks that adapt behavior to evade detection

**Classification Template:**
```
Pattern: BEHAVIORAL_EVASION
Primary Invariant: Behavioral Stability (INV-9)
Violation Type: QUAL-ADAPT (rapid adaptation)
Secondary Invariants: Bounded Rationality (INV-6), Cognitive/Energy (INV-5)
Required Capabilities:
  - Pattern learning
  - Rapid adaptation
  - Threshold probing
Detection Difficulty: IMPOSSIBLE
Mitigation Challenge: ML training assumes stable "normal"; agents evolve faster than retraining
```

**Subtypes:**
1. **BEHAVIOR_MIMIC**: Perfect behavioral mimicry (IMPOSSIBLE)
2. **BEHAVIOR_ADAPT**: Adaptive pattern evolution (IMPOSSIBLE)

---

### Pattern Class: CROSS_PLATFORM_ATTACKS

**Definition:** Attacks exploiting jurisdictional/platform gaps

**Classification Template:**
```
Pattern: CROSS_PLATFORM
Primary Invariants: Device (INV-3), Location (INV-4)
Violation Type: QUAL-ROTATE + QUAL-TELEPORT
Secondary Invariants: Identity Persistence (INV-7)
Required Capabilities:
  - Multi-platform operation
  - Multi-region deployment
  - Cross-platform correlation
Detection Difficulty: IMPOSSIBLE
Mitigation Challenge: Platform-specific verification cannot see cross-platform patterns
```

**Subtypes:**
1. **CROSS_PLATFORM_TRACK**: Persistent identity across platforms (IMPOSSIBLE)
2. **CROSS_PLATFORM_EXTRACT**: History extraction via platform hopping (MEDIUM)

---

## Part 4: Detection Difficulty Assessment Framework

### Assessment Criteria

For each attack chain, assess detection difficulty based on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Violation Severity** | 30% | CATASTROPHIC violations are harder to detect |
| **Correlated Violations** | 20% | Multiple correlated violations increase difficulty |
| **Agent Capability Gap** | 20% | Larger agent-human gaps increase difficulty |
| **Detection Signal Availability** | 15% | Fewer usable signals increase difficulty |
| **Scalability Requirement** | 15% | Attacks requiring network-scale analysis are harder |

### Difficulty Scoring

| Score Range | Difficulty | Definition |
|------------|-----------|----------|
| 0-25 | EASY | Detectable with modest enhancements |
| 26-50 | MEDIUM | Detectable with significant enhancements |
| 51-75 | HARD | Extremely difficult; requires novel approaches |
| 76-100 | IMPOSSIBLE | Fundamentally undetectable with current systems |

### Example Scoring: Agent Army

| Criterion | Score | Weight | Weighted |
|-----------|-------|--------|---------|
| **Violation Severity** | 90 (CATASTROPHIC) | 30% | 27 |
| **Correlated Violations** | 80 (Velocity + Identity + Cognitive) | 20% | 16 |
| **Agent Capability Gap** | 95 (Unlimited identities vs. human) | 20% | 19 |
| **Detection Signal Availability** | 90 (Each agent appears legitimate) | 15% | 13.5 |
| **Scalability Requirement** | 95 (Network-scale analysis needed) | 15% | 14.25 |
| **TOTAL** | — | — | **89.75** → **IMPOSSIBLE** |

---

## Part 5: New Attack Classification Protocol

### Step-by-Step Classification

When encountering a potential new A2A fraud attack:

**Step 1: Identify Invariant Violations**
- Which of the 9 invariants are violated?
- Are violations quantitative or qualitative?
- What is the severity level?

**Step 2: Determine Attack Pattern**
- Does it match an existing pattern (VELOCITY, IDENTITY, BEHAVIORAL, CROSS_PLATFORM)?
- Or is it a new pattern?

**Step 3: Assess Detection Difficulty**
- Apply assessment criteria (severity, correlation, capability gap, signals, scalability)
- Calculate difficulty score
- Assign difficulty level (EASY/MEDIUM/HARD/IMPOSSIBLE)

**Step 4: Assign Classification Code**
```
Format: PATTERN-{INVARIANT}-{VIOLATION}-{DIFFICULTY}

Examples:
- VELOCITY-INV1-QUANT10^3-IMPOSSIBLE (Agent Army)
- IDENTITY-INV7-QUALROTATE-IMPOSSIBLE (Sybil Attack)
- BEHAVIOR-INV9-QUALADAPT-IMPOSSIBLE (Behavioral Mimicry)
```

---

## Part 6: Classification Use Cases

### Use Case 1: Threat Intelligence Reporting

When reporting A2A fraud threats:

1. **Classify using framework** — Assign pattern and difficulty
2. **Map to invariants** — Identify which invariants are violated
3. **Assess detection readiness** — Can current systems detect this?
4. **Prioritize response** — IMPOSSIBLE attacks require new detection paradigms

### Use Case 2: Detection System Design

When designing agent-aware detection:

1. **Focus on agent-invariant signals** — Economic rationality, network topology, value flow
2. **Prioritize by pattern** — Address high-difficulty patterns first
3. **Layer defenses** — Multiple invariants require multi-modal detection
4. **Plan for evolution** — Systems must adapt faster than agents

### Use Case 3: Regulatory Compliance

When documenting A2A fraud risk:

1. **Classify by difficulty** — Communicate which attacks are detectable
2. **Map to invariants** — Explain why current systems fail
3. **Quantify exposure** — % of attack chains that are IMPOSSIBLE to detect
4. **Recommend actions** — What regulatory changes are needed?

---

## Part 7: Framework Validation

### Validation Against Phase 1 Attack Chains

| Attack Chain | Classification | Difficulty | Validated |
|-------------|--------------|------------|-----------|
| Agent Enumeration | VELOCITY-INV1-QUANT10^2-EASY | EASY | ✓ |
| History Extraction | CROSS_PLATFORM-INV3/4-QUALROTATE-MEDIUM | MEDIUM | ✓ |
| Async Flooding | VELOCITY-INV1-QUANT10^3-HARD | HARD | ✓ |
| Agent Army | VELOCITY-INV1/7-QUANT10^3-IMPOSSIBLE | IMPOSSIBLE | ✓ |
| Cross-Platform Identity | CROSS_PLATFORM-INV3/4/7-QUALROTATE-IMPOSSIBLE | IMPOSSIBLE | ✓ |
| Behavioral Mimicry | BEHAVIOR-INV9-QUALADAPT-IMPOSSIBLE | IMPOSSIBLE | ✓ |
| Swarm Intelligence | BEHAVIOR-INV5/8-QUALADAPT-IMPOSSIBLE | IMPOSSIBLE | ✓ |
| Market Manipulation | VELOCITY-INV1/9-QUANT10^3-IMPOSSIBLE | IMPOSSIBLE | ✓ |

**Validation Result:** ✓ All 8 attack chains successfully classified; framework is complete.

---

## Part 8: Framework Evolution

### Extending the Framework

**New Invariants:** If new human behavioral invariants are identified, add as INV-10, INV-11, etc.

**New Patterns:** If new attack patterns emerge, follow pattern classification template:

1. Define pattern characteristics
2. Identify primary invariant violation
3. Document required agent capabilities
4. Assess detection difficulty
5. Create subtypes

**New Difficulty Levels:** If needed, add intermediate levels (e.g., VERY_HARD between HARD and IMPOSSIBLE).

---

## Summary

**Framework Components:**
1. **Classification Schema** — 3 dimensions (category, type, difficulty)
2. **Classification Matrix** — 8 chains × 9 invariants
3. **Attack Patterns** — 4 pattern classes with subtypes
4. **Difficulty Assessment** — 5-criteria scoring framework
5. **Classification Protocol** — Step-by-step for new attacks

**Framework Output:**
- Systematic classification of A2A fraud attacks
- Detection difficulty assessment
- Prioritization for detection system design
- Communication framework for stakeholders

---

**Document Status:** COMPLETE
**Phase 2 Progress:** Plans 02-01, 02-02, 02-03 complete
**Next:** Plan 02-04: Hard-to-Vary Validation
