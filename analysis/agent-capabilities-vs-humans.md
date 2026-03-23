# Agent Capabilities vs. Humans: Comparative Analysis

**Phase:** 02-modeling-analysis, Plan 02-02
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides side-by-side comparison of human behavioral constraints versus AI agent capabilities across all 9 invariants. Each comparison includes quantitative metrics where applicable.

---

## Comparison Table: All 9 Invariants

| # | Invariant | Category | Human Property | Agent Capability | Violation Type | Severity |
|---|-----------|----------|-----------------|-----------------|----------------|----------|
| 1 | **Velocity Limits** | External/Physical | 10-100 tx/day (Van Vlasselaer 2017) | 10^3-10^6 tx/day (OpenClaw: 777K/day) | Quantitative (10^2-10^4×) | **CATASTROPHIC** |
| 2 | **Biometric Authentication** | External/Physical | Physical presence required (Jain 2021) | No physical form (pure software) | Qualitative (bypass) | **CATASTROPHIC** |
| 3 | **Device Fingerprinting** | External/Physical | 1-3 devices, stable fingerprints (Mowery 2012) | Unlimited fingerprints, arbitrary rotation | Qualitative (rotation) | **SEVERE** |
| 4 | **Location Constraints** | External/Physical | Travel time limits (Zhang 2020) | No physical location ("teleportation") | Qualitative (teleport) | **SEVERE** |
| 5 | **Cognitive/Energy** | Internal/Processing | Fatigue, 8h sleep, energy depletion | 24/7 operation, no fatigue | Qualitative (no limits) | **SEVERE** |
| 6 | **Bounded Rationality** | Internal/Processing | Limited optimization (Tesfatsion 2021) | Perfect optimization, exhaustive search | Qualitative (unbounded) | **MODERATE** |
| 7 | **Identity Persistence** | Internal/Processing | Single legal identity, Sybil cost (Hoffman 2020) | Unlimited disposable identities, cost→0 | Quantitative (cost→0) | **CATASTROPHIC** |
| 8 | **Computational Limits** | Internal/Processing | Sequential thinking, limited parallel | Massive parallel computation | Qualitative/quantitative | **MODERATE** |
| 9 | **Behavioral Stability** | Internal/Processing | Stable patterns over time (Chandola 2009) | Rapid adaptation, evasion | Qualitative (adaptive) | **SEVERE** |

---

## Detailed Comparisons

### External/Physical Invariants (4)

#### 1. Velocity Limits

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Transactions per day** | 10-100 | 10^3-10^6 | **10^2-10^4×** |
| **Cognitive constraints** | Manual input required | API calls automated | Complete bypass |
| **Sleep requirements** | ~8 hours/day unconscious | 24/7 operation | 3× time advantage |
| **Energy constraints** | Mental fatigue limits tx rate | No fatigue | Unlimited |
| **Literature source** | Van Vlasselaer 2017 | OpenClaw API docs | — |
| **Detection impact** | Velocity thresholds work | Thresholds meaningless | **CATASTROPHIC** |

**Key Insight:** Velocity advantage is the most straightforward violation to measure. Agent transaction velocity is 100-10,000× higher than human capability, making velocity-based fraud detection completely ineffective.

---

#### 2. Biometric Authentication

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Physical form** | Biological body | Pure software | **Fundamental difference** |
| **Biometric modalities** | Fingerprint, face, iris, voice | None | **Complete absence** |
| **Authentication method** | Physical presence required | API token authentication | Incompatible |
| **Forge resistance** | High (biometrics hard to forge) | N/A (no biometrics to forge) | N/A |
| **Literature source** | Jain 2021 | Platform analysis | — |
| **Detection impact** | Biometric auth works | Cannot authenticate agents | **CATASTROPHIC** |

**Key Insight:** This is a categorical difference, not just quantitative. Agents lack the physical substrate required for biometric authentication entirely. No amount of technical adaptation can make biometric systems work for pure software agents.

---

#### 3. Device Fingerprinting

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Device inventory** | 1-3 primary devices | Unlimited (cloud instances) | **Unbounded** |
| **Fingerprint stability** | Stable over months | Can rotate arbitrarily | Complete flexibility |
| **Rotation cost** | Financial (~$500-$2000/device) | Near-zero (programmatic) | **Cost→0** |
| **Behavioral linkage** | Device → User identity | No persistent linkage | Broken |
| **Literature source** | Mowery 2012 | Platform analysis | — |
| **Detection impact** | Device reputation works | Fingerprint rotation breaks tracking | **SEVERE** |

**Key Insight:** Device fingerprinting fails because agents can generate arbitrary fingerprints at cloud scale. The "rotation cost" that constrains humans to stable device identities is near-zero for software agents.

---

#### 4. Location Constraints

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Physical location** | Single location at any time | No physical location | **Fundamental difference** |
| **Travel speed** | Max ~900 km/h (commercial flight) | Instantaneous ("teleport") | Infinite speed |
| **Geo-consistency** | Must obey travel time | Can switch regions instantly | Broken |
| **Geo-fencing** | Physically constrained | Can deploy anywhere | Unconstrained |
| **Literature source** | Zhang 2020 | Platform analysis | — |
| **Detection impact** | Impossible travel works | Agents "teleport" normally | **SEVERE** |

**Key Insight:** Location-based detection assumes physical presence in space-time. Software agents exist in cloud infrastructure with no meaningful location constraint, making all geo-based checks inapplicable.

---

### Internal/Processing Invariants (5)

#### 5. Cognitive/Energy Constraints

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Cognitive fatigue** | Performance degrades with effort | No fatigue | Continuous performance |
| **Sleep requirements** | ~8 hours/day | 24/7 operation | 3× time advantage |
| **Energy depletion** | Limited daily decision energy | Unlimited (compute resources) | Unbounded |
| **Operational hours** | ~8-10 hours/day | 24/7 | 2.4× time advantage |
| **Error patterns** | Fatigue-driven errors | No fatigue patterns | Different signature |
| **Literature source** | Van Vlasselaer 2017 | Platform analysis | — |
| **Detection impact** | Behavioral profiling works | No fatigue/sleep patterns | **SEVERE** |

**Key Insight:** The absence of fatigue, sleep, and energy constraints means agents exhibit fundamentally different temporal patterns than humans. Behavioral profiling that expects human operational cycles will fail.

---

#### 6. Bounded Rationality

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Optimization capability** | Limited (heuristics, satisficing) | Can find optimal solutions | Qualitative difference |
| **Strategy exploration** | Cannot explore full space | Exhaustive search possible | Complete coverage |
| **Decision quality** | Bounded by cognition | Machine-optimized | Superior optimization |
| **Learning rate** | Slow (months/years) | Instantaneous | Rapid adaptation |
| **Literature source** | Tesfatsion 2021 | Literature/ML research | — |
| **Detection impact** | Assumes bounded attackers | Unbounded optimization possible | **MODERATE** |

**Key Insight:** Bounded rationality violations enable more sophisticated attacks, but don't completely bypass detection. Attackers still need to find profitable targets; optimization alone doesn't guarantee success.

---

#### 7. Identity Persistence/Legal Singularity

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Legal identity** | Single persistent identity (SSN, tax ID) | Ambiguous/no persistent identity | **Fundamental difference** |
| **Sybil creation cost** | High (legal paperwork, verification) | Near-zero (automated) | **Cost→0** |
| **Identity verification** | KYC processes constrain creation | Automation overcomes KYC | Scalable |
| **Reputation persistence** | Reputation tied to identity | Disposable identities | Broken |
| **Literature source** | Hoffman et al. 2020 | Moltbook analysis | — |
| **Detection impact** | Sybil resistance works | Unlimited Sybil attacks | **CATASTROPHIC** |

**Key Insight:** Sybil resistance is foundational to fraud detection. When identity creation cost approaches zero, Sybil attacks become trivial. Agents can create new identities faster than systems can respond.

---

#### 8. Computational Limits

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Parallel processing** | Limited (1-2 complex tasks) | Massive (thousands of instances) | **10^3×** |
| **Computation speed** | ~100 ops/sec (complex tasks) | Millions of ops/sec | **10^4×** |
| **Exhaustive search** | Impossible for large spaces | Systematic exploration possible | Qualitative difference |
| **Coordination** | Difficult at scale | Trivial (API-based) | Fundamental difference |
| **Literature source** | Behavioral profiling literature | Swarm intelligence analysis | — |
| **Detection impact** | Resource constraints help defense | Cloud provides unbounded resources | **MODERATE** |

**Key Insight:** Computational limits enable more sophisticated and coordinated attacks, but don't completely bypass detection. The impact is significant but not categorical like velocity or biometrics.

---

#### 9. Behavioral Pattern Stability

| Aspect | Human Baseline | Agent Capability | Gap |
|--------|---------------|-----------------|-----|
| **Pattern stability** | Stable over months/years | Can adapt instantly | **Rapid evolution** |
| **ML assumption** | "Normal" is learnable from history | "Normal" evolves continuously | Core assumption violated |
| **Adaptation rate** | Slow (cultural change) | Instantaneous (code update) | Orders of magnitude |
| **Adversarial capability** | Limited probing | Can probe exact thresholds | Systematic optimization |
| **Literature source** | Chandola 2009 | Adversarial ML literature | — |
| **Detection impact** | ML anomaly detection works | Training data becomes stale | **SEVERE** |

**Key Insight:** The core assumption of ML-based anomaly detection is that "normal" behavior is stable and learnable. Agents that can adapt faster than detection systems can retrain break this assumption.

---

## Quantitative Gap Analysis

### Numerical Comparisons (Where Applicable)

| Metric | Human | Agent | Gap |
|--------|-------|-------|-----|
| **Transactions/day** | 10-100 | 10^3-10^6 | **10^2-10^4×** |
| **Operational hours/day** | 8-10 | 24 | **2.4×** |
| **Device inventory** | 1-3 | Unlimited | **Unbounded** |
| **Device rotation cost** | $500-2000 | $0 | **Cost→0** |
| **New identity cost** | High (KYC) | Near-zero (automated) | **Cost→0** |
| **Travel speed** | 900 km/h | Instantaneous | **Infinite** |
| **Parallel processing** | 1-2 tasks | Thousands | **10^3×** |
| **Computation speed** | ~100 ops/sec | Millions/sec | **10^4×** |
| **Adaptation rate** | Months/years | Instantaneous | **Orders of magnitude** |

### Qualitative Differences (Cannot Be Quantified)

| Invariant | Human | Agent | Nature of Difference |
|-----------|-------|-------|---------------------|
| **Biometric Authentication** | Physical body | Pure software | **Categorical** |
| **Location** | Physical presence | No location | **Categorical** |
| **Cognitive/Energy** | Biological constraints | None | **Categorical** |
| **Bounded Rationality** | Limited optimization | Perfect optimization | **Qualitative** |

---

## Severity Distribution

```
┌─────────────────────────────────────────────────────────┐
│                    SEVERITY DISTRIBUTION                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CATASTROPHIC (3)                                       │
│  ████████████████████   Velocity, Biometrics, Identity │
│                                                         │
│  SEVERE (4)                                             │
│  █████████████████████████████████   Device, Location,  │
│                                Cognitive, Behavioral    │
│                                                         │
│  MODERATE (2)                                           │
│  ██████████████   Bounded Rationality, Computational   │
│                                                         │
│  MARGINAL (0)                                           │
│  ░░░░░░░░░░░░░░   None                                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Key Insight:** No invariant has MARGINAL impact. All 9 invariants are violated at MODERATE or higher severity, with 7/9 being SEVERE or CATASTROPHIC.

---

## Correlation Analysis: Coupled Violations

For AI agents, invariant violations are **correlated** rather than independent:

### Violation Clusters

| Cluster | Violations | Common Cause |
|---------|------------|--------------|
| **No Physical Form** | Biometrics, Device, Location | Agents are pure software |
| **No Biological Constraints** | Velocity, Cognitive/Energy | No fatigue/sleep limits |
| **No Identity Constraints** | Identity Persistence, Device | Unlimited disposable identities |
| **Adaptive Intelligence** | Bounded Rationality, Behavioral Stability | Can optimize and adapt |

### Detection Implications

**Correlated violations mean:**
1. **Single-point failures exist** — Bypassing one invariant may bypass multiple
2. **Redundancy is limited** — Multiple invariants may fail simultaneously
3. **Defense-in-depth is weaker** — Layers that appear independent may all fail

**Example:** An agent with no physical form simultaneously bypasses:
- Biometric authentication (no body)
- Device fingerprinting (no fixed device)
- Location constraints (no location)

This correlated failure creates **compound vulnerabilities** greater than the sum of individual violations.

---

## Detection System Implications

### Current System Coverage

| Detection Method | Invariants It Depends On | Violation Status | Effectiveness |
|-----------------|-------------------------|------------------|---------------|
| Velocity thresholds | Velocity | CATASTROPHIC | **Bypassed** |
| Biometric auth | Biometrics | CATASTROPHIC | **Bypassed** |
| Device reputation | Device, Location | SEVERE | **Degraded** |
| Geo-velocity | Location | SEVERE | **Degraded** |
| Behavioral profiling | Cognitive, Behavioral | SEVERE | **Degraded** |
| Sybil resistance | Identity Persistence | CATASTROPHIC | **Bypassed** |
| ML anomaly detection | Behavioral Stability | SEVERE | **Degraded** |
| Resource constraints | Computational | MODERATE | **Partially functional** |

### Required: Agent-Invariant Signals

Detection frameworks must identify signals that:
1. **Apply to both humans and agents** — Work regardless of entity type
2. **Cannot be violated by software agents** — Agent-invariant by design
3. **Are measurable from transaction data** — Practically implementable

**Candidate signals (for Phase 3 exploration):**
- Economic rationality: Does transaction make economic sense?
- Network topology: Is the transaction graph consistent with legitimate commerce?
- Value flow: Does money flow follow legitimate patterns?
- Temporal consistency: Are transaction timing patterns consistent with stated purpose?

---

## Summary Statistics

| Statistic | Value |
|-----------|-------|
| **Total invariants** | 9 |
| **Catastrophic violations** | 3 (33%) |
| **Severe violations** | 4 (44%) |
| **Moderate violations** | 2 (22%) |
| **Marginal violations** | 0 (0%) |
| **Quantitative violations** | 4 |
| **Qualitative violations** | 5 |
| **Categorical differences** | 3 (Biometrics, Location, Cognitive) |
| **Mean severity** | SEVERE (2.33 on 0-3 scale) |

**Conclusion:** AI agents violate all 9 human behavioral invariants at MODERATE or higher severity. Current fraud detection systems are fundamentally incompatible with agent-based commerce.

---

**Document Status:** COMPLETE
**Next:** Plan 02-03: A2A Fraud Attack Taxonomy Development
