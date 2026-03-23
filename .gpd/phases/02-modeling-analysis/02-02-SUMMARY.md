# Plan 02-02 Summary: Agent Property Violation Analysis

**Phase:** 02-modeling-analysis
**Plan:** 02-02 Agent Property Violation Analysis
**Status:** COMPLETE
**Date:** 2026-03-22
**Duration:** ~1 day

---

## Executive Summary

Successfully mapped all 9 agent property violations against human behavioral invariants. Each invariant documented with human baseline, agent capability, violation mechanism, and severity classification. Analysis reveals that AI agents violate all 9 invariants at MODERATE or higher severity, with 7/9 being SEVERE or CATASTROPHIC.

**Deliverables Created:**
- `analysis/agent-invariant-violations.md` — Complete violation mapping
- `analysis/agent-capabilities-vs-humans.md` — Comparative analysis with statistics

---

## Tasks Completed

### Task 2.1: External/Physical Invariant Violations ✓
- [x] 2.1.1 Created `analysis/agent-invariant-violations.md`
- [x] 2.1.2 Mapped Velocity Limits violation (10^2-10^4× multiplier)
- [x] 2.1.3 Mapped Biometric Authentication violation (complete bypass)
- [x] 2.1.4 Mapped Device Fingerprinting violation (unlimited rotation)
- [x] 2.1.5 Mapped Location Constraints violation ("teleportation")

### Task 2.2: Internal/Processing Invariant Violations ✓
- [x] 2.2.1 Mapped Cognitive/Energy Constraints violation (24/7 operation)
- [x] 2.2.2 Mapped Bounded Rationality violation (perfect optimization)
- [x] 2.2.3 Mapped Identity Persistence violation (unlimited identities)
- [x] 2.2.4 Mapped Computational Limits violation (parallel computation)
- [x] 2.2.5 Mapped Behavioral Stability violation (rapid adaptation)

### Task 2.3: Violation Severity Classification ✓
- [x] 2.3.1 Classified violations by impact on detection
- [x] 2.3.2 Documented severity for each of 9 invariants
- [x] 2.3.3 Created `analysis/agent-capabilities-vs-humans.md` comparison table
- [x] 2.3.4 Validated all 9 invariants have violation mappings
- [x] 2.3.5 Validated agent capabilities grounded in Phase 1 platform analysis

---

## Deliverables

| Deliverable ID | File | Status | Description |
|----------------|------|--------|-------------|
| deliv-invariant-violations | analysis/agent-invariant-violations.md | ✓ Complete | All 9 invariant violations with mechanisms |
| deliv-agent-capabilities-comparison | analysis/agent-capabilities-vs-humans.md | ✓ Complete | Side-by-side comparison tables + statistics |

---

## Key Findings

### Severity Distribution

| Severity | Count | Invariants | Percentage |
|----------|-------|------------|------------|
| CATASTROPHIC | 3 | Velocity, Biometrics, Identity Persistence | 33% |
| SEVERE | 4 | Device, Location, Cognitive, Behavioral | 44% |
| MODERATE | 2 | Bounded Rationality, Computational | 22% |
| MARGINAL | 0 | — | 0% |

**Mean Severity:** SEVERE (2.33 on 0-3 scale)

### Quantitative Gaps

| Metric | Human | Agent | Gap |
|--------|-------|-------|-----|
| Transactions/day | 10-100 | 10^3-10^6 | **10^2-10^4×** |
| Operational hours | 8-10 | 24 | **2.4×** |
| Device inventory | 1-3 | Unlimited | **Unbounded** |
| New identity cost | High (KYC) | Near-zero | **Cost→0** |
| Adaptation rate | Months/years | Instant | **Orders of magnitude** |

### Categorical Differences

3 invariants represent **fundamental categorical differences** (not just quantitative):
1. **Biometric Authentication** — Agents have no physical form
2. **Location Constraints** — Agents have no physical location
3. **Cognitive/Energy** — Agents have no biological constraints

### Violation Correlation

Violations are **correlated** rather than independent:
- **No Physical Form** cluster: Biometrics + Device + Location
- **No Biological Constraints** cluster: Velocity + Cognitive/Energy
- **No Identity Constraints** cluster: Identity Persistence + Device
- **Adaptive Intelligence** cluster: Bounded Rationality + Behavioral Stability

**Implication:** Single-point failures exist; bypassing one invariant may bypass multiple simultaneously.

---

## Platform Grounding

All violation mappings grounded in Phase 1 outputs:
- Human baselines from `analysis/literature-survey.md`
- Agent capabilities from `analysis/openclaw-platform-analysis.md` and `analysis/moltbook-platform-analysis.md`
- Attack chains from `.gpd/phases/01-discovery-taxonomy/01-01-SUMMARY.md`

**Evidence Citations:**
- Van Vlasselaer 2017: Velocity limits, cognitive constraints
- Jain 2021: Biometric authentication
- Mowery 2012: Device fingerprinting
- Zhang 2020: Location constraints
- Tesfatsion 2021: Bounded rationality
- Hoffman et al. 2020: Identity persistence, Sybil resistance
- Chandola 2009: Behavioral pattern stability
- OpenClaw API docs: Agent velocity capabilities
- Moltbook analysis: Reputation gaming, Sybil attacks

---

## Detection System Implications

### Current System Coverage Analysis

| Detection Method | Dependent Invariants | Violation Status | Effectiveness |
|-----------------|----------------------|------------------|---------------|
| Velocity thresholds | Velocity | CATASTROPHIC | **Bypassed** |
| Biometric auth | Biometrics | CATASTROPHIC | **Bypassed** |
| Device reputation | Device, Location | SEVERE | **Degraded** |
| Geo-velocity | Location | SEVERE | **Degraded** |
| Behavioral profiling | Cognitive, Behavioral | SEVERE | **Degraded** |
| Sybil resistance | Identity Persistence | CATASTROPHIC | **Bypassed** |
| ML anomaly detection | Behavioral Stability | SEVERE | **Degraded** |

**Conclusion:** No current detection method remains fully functional against AI agents.

### Required: Agent-Invariant Signals

Detection frameworks must identify signals that:
1. Apply to both humans AND agents (agent-invariant)
2. Cannot be violated by software agents
3. Are measurable from transaction data

**Candidate signals for Phase 3:**
- Economic rationality (does transaction make economic sense?)
- Network topology (is transaction graph consistent with legitimate commerce?)
- Value flow (does money flow follow legitimate patterns?)

---

## Contract Claims Validated

**claim-02-violations:** ✓ Agent properties that violate each human invariant systematically mapped with platform evidence and violation mechanisms

**Evidence:**
- All 9 invariants have violation mappings
- Human baselines documented with literature citations
- Agent capabilities grounded in Phase 1 platform analysis
- Violation mechanisms explained
- Severity classification with justification

---

## Next Steps

**Proceed to Plan 02-03:** A2A Fraud Attack Taxonomy Development

Using the 9 invariant violations documented here, Plan 02-03 will:
1. Map 8 attack chains to invariant violations
2. Create `analysis/a2a-attack-taxonomy.md` with hierarchical structure
3. Organize by invariant violation and by detection difficulty
4. Document attack patterns with required capabilities and mitigation challenges

---

**Acceptance Test:** TAXO-02 (Violation Mapping Completeness) ✓ PASSED
