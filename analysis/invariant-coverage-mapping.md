# Invariant Coverage Mapping: From Violations to Detection Mechanisms

**Phase:** 03-detection-framework, Plan 03-01
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides a detailed mapping from each of the 9 human behavioral invariants (identified in Phase 2) to the agent-invariant detection mechanisms that address them. For each invariant, we document: the violation type, why current systems fail, and what agent-invariant detection replaces it.

---

## Summary Table

| Invariant | Category | Violation Severity | Addressable | Replacement Mechanism |
|-----------|----------|-------------------|------------|----------------------|
| **1. Velocity Limits** | External | SEVERE | ✓ Yes | Economic Rationality |
| **2. Biometric Authentication** | External | CATASTROPHIC | ✗ No | Network-based identity |
| **3. Device Fingerprinting** | External | SEVERE | ✓ Yes | Network Topology |
| **4. Location Constraints** | External | MODERATE | ✗ No | Network routing analysis |
| **5. Cognitive/Energy** | Internal | SEVERE | ✓ Yes | Temporal Consistency |
| **6. Bounded Rationality** | Internal | CATASTROPHIC | ✓ Yes | Economic Rationality |
| **7. Identity Persistence** | Internal | CATASTROPHIC | ✓ Yes | Network Topology |
| **8. Computational Limits** | Internal | MODERATE | ✓ Yes | Network + Temporal |
| **9. Behavioral Stability** | Internal | SEVERE | ✓ Yes | Cross-Platform Correlation |

**Coverage:** 7/9 invariants addressable (77.8%), 2/9 fundamentally incompatible (22.2%)

---

## Detailed Coverage Analysis

### Invariant 1: Velocity Limits

**Human Baseline:** Humans transact at limited velocity (~10-100 transactions/day) due to cognitive processing, fatigue, and daily routine constraints.

**Agent Violation (from 02-02):**
- **Capability:** OpenClaw enables 777,600 tx/day per agent (9,000 tx/sec)
- **Violation Type:** QUANT-10^3-10^4 (10^3-10^4× human baseline)
- **Severity:** SEVERE
- **Detection Impact:** Velocity thresholds become meaningless at agent scale

**Why Current Systems Fail:**
```
Current Logic: IF tx_count > threshold THEN flag_as_fraud
Problem: Legitimate agent commerce operates at 10^6 tx/day
Result: Cannot distinguish fraud from legitimate high-velocity activity
```

**Agent-Invariant Replacement: Economic Rationality**
```
New Logic: IF tx_volume > economic_purpose_requires THEN flag_as_suspicious
Rationale: High transaction volume is only suspicious if it lacks economic purpose
Example: 1M tx/day serving 1M customers = legitimate
         1M tx/day circular among 10 accounts = fraud
```

**Detection Mechanism:**
- **Signal:** Economic Purpose Deviation
- **Measurement:** Compare transaction volume to expected economic utility
- **Agent-Invariance:** Economic purpose applies to all rational actors
- **Coverage:** Addresses Async Flooding, Agent Army, Market Manipulation chains

---

### Invariant 2: Biometric Authentication

**Human Baseline:** Humans have unique physical biometrics (fingerprint, face, iris) that can be captured and verified for authentication.

**Agent Violation (from 02-02):**
- **Capability:** Agents are pure software with no physical form
- **Violation Type:** QUAL-BYPASS (complete bypass)
- **Severity:** CATASTROPHIC
- **Detection Impact:** Biometric authentication cannot work

**Why Current Systems Fail:**
```
Current Logic: IF biometric_match THEN authorized
Problem: Agents have no physical form to capture
Result: Biometric authentication is fundamentally incompatible
```

**Agent-Invariant Replacement: Network-Based Identity**
```
New Logic: IF identity_graph_consistent THEN authorized
Rationale: Identity exists as a pattern in transaction networks, not physical body
Example: Human identity = biometric + history
         Agent identity = cryptographic signature + network behavior
```

**Detection Mechanism:**
- **Signal:** Identity Graph Consistency
- **Measurement:** Analyze transaction patterns for identity coherence
- **Agent-Invariance:** Identity is a network pattern, not a physical property
- **Limitation:** Cannot prevent identity theft (compromised human credentials)

**Residual Risk:** Agents using compromised human identities (hybrid attack) require behavioral analysis, not biometric verification.

---

### Invariant 3: Device Fingerprinting

**Human Baseline:** Humans typically use 1-3 devices consistently; device fingerprinting provides stable identity correlation.

**Agent Violation (from 02-02):**
- **Capability:** Agents can rotate unlimited devices via cloud infrastructure
- **Violation Type:** QUAL-ROTATE (unlimited rotation)
- **Severity:** SEVERE
- **Detection Impact:** Device fingerprinting cannot track agents

**Why Current Systems Fail:**
```
Current Logic: IF device_fingerprint_stable THEN legitimate_user
Problem: Agents rotate devices faster than tracking can update
Result: Device fingerprinting provides no stability
```

**Agent-Invariant Replacement: Network Topology**
```
New Logic: IF transaction_pattern_consistent THEN legitimate_actor
Rationale: Actors leave network patterns regardless of device count
Example: Human uses 3 devices but consistent merchant network
         Agent uses 10,000 devices but consistent transaction graph
```

**Detection Mechanism:**
- **Signal:** Transaction Graph Consistency
- **Measurement:** Analyze ego-network structure for stability across devices
- **Agent-Invariance:** Network patterns exist independent of device count
- **Coverage:** Addresses History Extraction, Cross-Platform Identity chains

---

### Invariant 4: Location Constraints

**Human Baseline:** Humans cannot be in multiple locations simultaneously; travel time creates geographic constraints.

**Agent Violation (from 02-02):**
- **Capability:** Agents operate from cloud infrastructure; no physical location
- **Violation Type:** QUAL-BYPASS (complete bypass)
- **Severity:** MODERATE
- **Detection Impact:** Location-based checks cannot apply

**Why Current Systems Fail:**
```
Current Logic: IF location_consistent THEN legitimate
Problem: Agents have no location; cloud infrastructure is globally distributed
Result: Location checks are meaningless
```

**Agent-Invariant Replacement: Network Routing Analysis**
```
New Logic: IF network_path_consistent THEN legitimate
Rationale: Network routing path substitutes for physical location
Example: Human location = GPS coordinates
         Agent location = IP geolocation + routing path
```

**Detection Mechanism:**
- **Signal:** Network Path Consistency
- **Measurement:** Analyze IP routing and network infrastructure paths
- **Agent-Invariance:** Network routing applies to all transactions
- **Limitation:** Cloud infrastructure creates legitimate path diversity

**Residual Risk:** Legitimate cloud-based services create complex routing patterns that may appear suspicious.

---

### Invariant 5: Cognitive/Energy Constraints

**Human Baseline:** Humans require sleep, experience fatigue, and have limited cognitive processing capacity.

**Agent Violation (from 02-02):**
- **Capability:** Agents operate 24/7 without fatigue
- **Violation Type:** QUAL-BYPASS (complete bypass)
- **Severity:** SEVERE
- **Detection Impact:** Temporal patterns based on human circadian rhythms fail

**Why Current Systems Fail:**
```
Current Logic: IF activity_follows_human_patterns THEN legitimate
Problem: Agents operate continuously with no fatigue patterns
Result: Temporal signatures are fundamentally different
```

**Agent-Invariant Replacement: Temporal Consistency**
```
New Logic: IF activity_temporally_coherent THEN legitimate
Rationale: Coherence applies regardless of activity level
Example: Human = sleep/wake cycles
         Agent = continuous operation (still coherent)
         Fraud = coordinated bursts (incoherent)
```

**Detection Mechanism:**
- **Signal:** Temporal Coherence
- **Measurement:** Analyze activity timing for coordination signatures
- **Agent-Invariance:** Temporal coherence is independent of activity level
- **Coverage:** Addresses Behavioral Mimicry, Swarm Intelligence chains

---

### Invariant 6: Bounded Rationality

**Human Baseline:** Humans have bounded rationality—limited cognitive capacity, incomplete information, emotional influences.

**Agent Violation (from 02-02):**
- **Capability:** Agents optimize perfectly within defined constraints
- **Violation Type:** QUAL-BYPASS (complete bypass)
- **Severity:** CATASTROPHIC
- **Detection Impact:** Perfect optimization is undetectable by human-baseline systems

**Why Current Systems Fail:**
```
Current Logic: IF behavior_human_like THEN legitimate
Problem: Agent behavior is mathematically optimal, not human-like
Result: Optimized transactions evade human-baseline detection
```

**Agent-Invariant Replacement: Economic Rationality**
```
New Logic: IF transaction_economically_rational THEN legitimate
Rationale: Economic rationality is independent of optimization level
Example: Human impulse buy = irrational but legitimate
         Agent arbitrage = optimal but legitimate
         Fraud circular flow = irrational AND illegitimate
```

**Detection Mechanism:**
- **Signal:** Economic Rationality Deviation
- **Measurement:** Analyze transactions for economic purpose and utility
- **Agent-Invariance:** Economic rationality applies to all actors
- **Key Insight:** Fraud violates economic rationality, not optimization level

---

### Invariant 7: Identity Persistence / Legal Singularity

**Human Baseline:** Humans have persistent legal identity tied to physical person; creating new identities is costly.

**Agent Violation (from 02-02):**
- **Capability:** Agents create unlimited identities at zero marginal cost
- **Violation Type:** QUANT-∞ (unbounded)
- **Severity:** CATASTROPHIC
- **Detection Impact:** Sybil resistance fails; identity verification overwhelmed

**Why Current Systems Fail:**
```
Current Logic: IF identity_verified_kyc THEN legitimate
Problem: Agents create 10^6 identities faster than KYC can process
Result: Identity verification bottleneck; Sybil armies undetectable
```

**Agent-Invariant Replacement: Network Topology (Identity Graphs)**
```
New Logic: IF identity_graph_healthy THEN legitimate
Rationale: Identity exists as network pattern, not KYC status
Example: Human identity = single connected component in transaction graph
         Sybil army = star topology with central fraudster
         Fraud = disconnected or highly centralized components
```

**Detection Mechanism:**
- **Signal:** Identity Graph Topology
- **Measurement:** Analyze transaction network for Sybil patterns
- **Agent-Invariance:** Network topology is independent of identity count
- **Coverage:** Addresses Agent Army, Cross-Platform Identity chains

---

### Invariant 8: Computational Limits

**Human Baseline:** Humans have limited parallel processing; can only manage handful of simultaneous interactions.

**Agent Violation (from 02-02):**
- **Capability:** Agents coordinate millions of parallel operations
- **Violation Type:** QUANT-10^6 (massive scale)
- **Severity:** MODERATE
- **Detection Impact:** Swarm coordination undetectable by human-scale systems

**Why Current Systems Fail:**
```
Current Logic: IF interaction_count_human_scale THEN legitimate
Problem: Agent swarm coordinates 10^6+ parallel transactions
Result: Swarm detection requires network-scale analysis
```

**Agent-Invariant Replacement: Network + Temporal (Swarm Detection)**
```
New Logic: IF coordination_pattern_natural THEN legitimate
Rationale: Coordination leaves detectable signatures at network scale
Example: Human crowd = emergent coordination
         Agent swarm = precise synchronization
         Fraud swarm = unnatural correlation patterns
```

**Detection Mechanism:**
- **Signal:** Coordination Pattern Analysis
- **Measurement:** Detect unnatural synchronization across network
- **Agent-Invariance:** Coordination patterns exist regardless of actor count
- **Coverage:** Addresses Swarm Intelligence chain

---

### Invariant 9: Behavioral Pattern Stability

**Human Baseline:** Humans exhibit stable behavioral patterns over time (spending habits, merchant preferences, temporal patterns).

**Agent Violation (from 02-02):**
- **Capability:** Agents rapidly adapt behavior to evade detection
- **Violation Type:** QUAL-ADAPT (continuous adaptation)
- **Severity:** SEVERE
- **Detection Impact:** Behavioral ML models become stale faster than retraining possible

**Why Current Systems Fail:**
```
Current Logic: IF behavior_matches_learned_patterns THEN legitimate
Problem: Agents adapt faster than ML models retrain
Result: Behavioral detection is in constant arms race (agents win)
```

**Agent-Invariant Replacement: Cross-Platform Correlation**
```
New Logic: IF behavior_correlated_across_platforms THEN legitimate
Rationale: Legitimate actors have consistent cross-platform presence
Example: Human = consistent identity across platforms
         Adaptive agent = new identity per platform (correlation breaks)
         Fraud = platform-hopping to evade detection
```

**Detection Mechanism:**
- **Signal:** Cross-Platform Identity Correlation
- **Measurement:** Track identity across platforms; detect platform-hopping
- **Agent-Invariance:** Cross-platform consistency is independent of behavior
- **Coverage:** Addresses Behavioral Mimicry, Cross-Platform Identity chains

---

## Coverage Matrix: Invariants × Attack Chains

| Invariant | Agent Enumeration | History Extraction | Async Flooding | Agent Army | Cross-Platform | Behavioral Mimicry | Swarm Intelligence | Market Manipulation |
|-----------|------------------|-------------------|----------------|-----------|----------------|-------------------|-------------------|-------------------|
| **1. Velocity** | ✓ | ✓ | ✓ | ✓ | - | - | ✓ | ✓ |
| **2. Biometric** | - | - | - | - | - | - | - | - |
| **3. Device** | - | ✓ | - | - | ✓ | - | - | - |
| **4. Location** | - | - | - | - | ✓ | - | - | ✓ |
| **5. Cognitive** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **6. Bounded Rationality** | - | - | - | - | - | ✓ | - | ✓ |
| **7. Identity** | ✓ | - | - | ✓ | ✓ | - | - | - |
| **8. Computational** | - | - | - | - | - | - | ✓ | - |
| **9. Behavioral** | - | - | - | - | ✓ | ✓ | - | ✓ |

**Legend:** ✓ = Invariant exploited by attack chain, - = Not applicable

**Key Insight:** Cognitive/Energy constraints (Invariant 5) are exploited by ALL 8 attack chains—most commonly targeted invariant.

---

## Detection Mechanism Priority

### High Priority (Addresses 3+ attack chains)

| Mechanism | Attack Chains Addressed | Implementation Complexity |
|-----------|------------------------|--------------------------|
| **Economic Rationality** | 4 (Enumeration, Flooding, Army, Manipulation) | Moderate |
| **Network Topology** | 5 (History, Army, Cross-Platform, Swarm, Mimicry via identity) | High |
| **Temporal Consistency** | 6 (all except Army/Cross-Platform) | Moderate |

### Medium Priority (Addresses 2 attack chains)

| Mechanism | Attack Chains Addressed | Implementation Complexity |
|-----------|------------------------|--------------------------|
| **Cross-Platform Correlation** | 3 (Cross-Platform, Mimicry, Army) | High |
| **Value Flow Analysis** | 2 (Flooding, Manipulation) | Low |

---

## Implementation Roadmap

### Phase 3A: Foundation (Signals 1-2)
- Economic Rationality Signal
- Temporal Consistency Signal
- **Coverage:** 6/8 attack chains

### Phase 3B: Network Analysis (Signal 3)
- Network Topology Signal
- **Coverage:** +2 attack chains (total 8/8)

### Phase 3C: Advanced Correlation (Signals 4-5)
- Cross-Platform Correlation Signal
- Value Flow Signal
- **Coverage:** Enhanced detection for remaining gaps

---

## Validation

**Requirement FRAM-01:** All 9 invariants addressed
- ✓ 7/9 invariants have detection mechanisms
- ✓ 2/9 invariants acknowledged as incompatible
- ✓ Replacement strategies documented

**Coverage Analysis:**
- 8/8 attack chains have at least one detection mechanism
- 0/8 attack chains rated "Impossible" to detect (vs. 4/8 in Phase 2)

---

**Document Status:** COMPLETE
**Companion Document:** `analysis/detection-methodology.md` (framework overview)
