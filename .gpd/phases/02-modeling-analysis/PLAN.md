# Phase 2 Plan: Modeling and Analysis

**Phase:** 02-modeling-analysis
**Created:** 2026-03-21
**Status:** Ready for execution
**Dependencies:** Phase 1 (Discovery and Taxonomy) — COMPLETE

## Overview

Phase 2 develops the formal explanatory framework mapping human behavioral invariants → agent violations → attack taxonomy → hard-to-vary validation. This phase applies Deutsch's hard-to-vary criterion to establish why A2A fraud is fundamentally undetectable by current banking systems.

### Success Criteria

1. ✓ Complete mapping of all 9 human behavioral invariants used in fraud detection
2. ✓ Complete mapping of agent properties that violate each invariant
3. ✓ Taxonomy of A2A fraud attack vectors classified by invariant violation
4. ✓ Hard-to-vary explanation validated — core claim cannot vary while remaining plausible

### Phase 1 Inputs

| Input | Source | Description |
|-------|--------|-------------|
| 9 Human Invariants | Plan 01-03 | 4 external + 5 internal invariants with literature citations |
| 8 Attack Chains | Plan 01-01 | Complete chains with detection difficulty classification |
| Reputation Gaming Vectors | Plan 01-02 | 10^3-10^6× scale advantage, Sybil attack vectors |
| Nearest Analogues | Plan 01-03 | Botnets, HFT, P2P, MARL with applicability mapping |
| Data Gap Analysis | Plan 01-04 | Synthetic data requirements, validation limitations |

---

## Plan 02-01: Human Behavioral Invariant Mapping

**Goal:** Create comprehensive documentation of all 9 human behavioral invariants used in banking fraud detection, with their theoretical foundations, detection mechanisms, and failure modes.

**Deliverables:**
- `analysis/human-invariants-complete.md` — Complete invariant reference
- `analysis/invariant-detection-mechanisms.md` — How each invariant is used in detection

### Task Breakdown

#### Task 1.1: External/Physical Invariants (4)

**From Phase 1 (already documented):**
1. **Velocity Limits** — ~10-100 transactions/day (Van Vlasselaer 2017)
2. **Biometric Authentication** — Physical presence required (Jain 2021)
3. **Device Fingerprinting** — Fixed device identity (Mowery 2012)
4. **Location Constraints** — Travel time limits (Zhang 2020)

**Work:** Consolidate into unified invariant reference with:
- Formal definition
- Fraud detection usage patterns
- Literature citations
- Quantitative bounds where applicable

#### Task 1.2: Internal/Processing Invariants (5)

**From Phase 1 fixes (newly documented):**
1. **Cognitive/Energy Constraints** — Cognitive fatigue, sleep limits, energy depletion
2. **Bounded Rationality** — Limited computational optimization capability
3. **Identity Persistence/Legal Singularity** — Single legal identity, Sybil constraints
4. **Computational Limits** — No massive parallel computation or exhaustive search
5. **Behavioral Pattern Stability** — Patterns stable over time, ML training assumption

**Work:** For each invariant, document:
- Formal definition
- How fraud detection systems depend on it
- Literature citations (from survey)
- Quantitative constraints where applicable
- What breaks when invariant is violated

#### Task 1.3: Cross-Invariant Analysis

**Work:** Document:
- How invariants interact in detection systems
- Which invariants are independent vs. coupled
- Redundancy patterns (do multiple invariants protect same attack surface?)
- Criticality analysis (which invariants are most fundamental)

**Acceptance Criteria:**
- [ ] All 9 invariants documented with formal definitions
- [ ] Each invariant has literature citation
- [ ] Detection mechanism usage patterns documented
- [ ] Cross-invariant analysis complete
- [ ] No gaps vs. fraud detection literature

---

## Plan 02-02: Agent Property Violation Analysis

**Goal:** For each of the 9 human invariants, map agent properties that violate the invariant. Establish why agents are fundamentally different from humans in fraud-relevant ways.

**Deliverables:**
- `analysis/agent-invariant-violations.md` — Complete violation mapping
- `analysis/agent-capabilities-vs-humans.md` — Comparative analysis

### Task Breakdown

#### Task 2.1: External/Physical Invariant Violations

**For each of 4 external invariants:**

| Invariant | Human Property | Agent Property | Violation Type |
|-----------|---------------|---------------|----------------|
| Velocity limits | 10-100 tx/day | 10^3-10^6 tx/day | Quantitative (10^2-10^4×) |
| Biometrics | Physical presence | No physical form | Qualitative (bypass) |
| Device | Fixed device | Arbitrary fingerprints | Qualitative (rotation) |
| Location | Travel time limits | No physical location | Qualitative (teleport) |

**Work:** Document for each:
- Human baseline (with literature support)
- Agent capability (with platform evidence from Phase 1)
- Violation mechanism (how/why detection fails)
- Quantification where possible

#### Task 2.2: Internal/Processing Invariant Violations

**For each of 5 internal invariants:**

| Invariant | Human Property | Agent Property | Violation Type |
|-----------|---------------|---------------|----------------|
| Cognitive/Energy | Fatigue, sleep, energy | No fatigue, 24/7 operation | Qualitative |
| Bounded rationality | Limited optimization | Perfect optimization | Qualitative |
| Identity persistence | Single identity, cost to create new | Unlimited disposable identities | Quantitative (cost→0) |
| Computational limits | Sequential thinking | Parallel computation | Qualitative/quantitative |
| Behavioral stability | Stable patterns | Adaptive patterns | Qualitative |

**Work:** Document for each:
- Human constraint (what limits humans)
- Agent capability (what agents can do)
- Why violation matters for fraud detection
- Platform/literature evidence

#### Task 2.3: Violation Severity Classification

**Work:** Classify violations by impact on detection:
- **CATASTROPHIC** — Detection completely bypassed (e.g., velocity)
- **SEVERE** — Detection significantly degraded (e.g., behavioral stability)
- **MODERATE** — Detection partially functional (e.g., device fingerprinting)
- **MARGINAL** — Minimal impact (if any)

**Acceptance Criteria:**
- [ ] All 9 invariants have violation mappings
- [ ] Agent capabilities grounded in Phase 1 platform analysis
- [ ] Violation mechanisms explained
- [ ] Severity classification with justification

---

## Plan 02-03: A2A Fraud Attack Taxonomy Development

**Goal:** Create taxonomy of A2A fraud attack vectors organized by which human invariant(s) they violate. Map 8 attack chains from Phase 1 to invariant violations.

**Deliverables:**
- `analysis/a2a-attack-taxonomy.md` — Complete taxonomy
- `analysis/invariant-based-attack-classification.md` — Classification framework

### Task Breakdown

#### Task 3.1: Attack Chain → Invariant Mapping

**From Phase 1 attack chains (8 total):**

| Chain | Primary Invariant(s) Violated | Detection Difficulty |
|-------|------------------------------|---------------------|
| Agent Enumeration | Velocity, Identity persistence | Easy |
| History Extraction | Device, Location | Medium |
| Async Flooding | Velocity | Hard |
| Agent Army | Velocity, Identity persistence | Impossible |
| Cross-Platform Identity | Device, Location, Identity persistence | Impossible |
| Behavioral Mimicry | Cognitive, Behavioral stability | Impossible |
| Swarm Intelligence | Cognitive, Computational | Impossible |
| Market Manipulation | Velocity, Behavioral stability | Impossible |

**Work:** For each chain:
- Identify which invariants are violated
- Explain why violation enables the attack
- Link detection difficulty to invariant violations
- Document secondary invariant violations

#### Task 3.2: Taxonomy Structure

**Hierarchical taxonomy:**

```
A2A Fraud Taxonomy
├── By Invariant Violation
│   ├── Velocity Violations
│   │   ├── Async flooding (high-volume tx)
│   │   ├── Agent army (parallel accounts)
│   │   └── Market manipulation (flash crashes)
│   ├── Biometric Violations
│   │   └── (Direct bypasses — no physical form)
│   ├── Device Fingerprinting Violations
│   │   ├── Cross-platform identity (fingerprint rotation)
│   │   └── History extraction (device hopping)
│   ├── Location Constraint Violations
│   │   ├── Cross-platform identity (multi-region)
│   │   └── Market manipulation (instant execution)
│   ├── Cognitive/Energy Violations
│   │   ├── Behavioral mimicry (perfect pattern matching)
│   │   └── Swarm intelligence (24/7 coordination)
│   ├── Bounded Rationality Violations
│   │   └── Strategic optimization (exhaustive search)
│   ├── Identity Persistence Violations
│   │   ├── Agent army (Sybil identities)
│   │   └── Cross-platform identity (persistent tracking)
│   ├── Computational Limits Violations
│   │   └── Swarm intelligence (parallel optimization)
│   └── Behavioral Stability Violations
│       ├── Behavioral mimicry (adaptive patterns)
│       └── Market manipulation (pattern evolution)
└── By Detection Difficulty
    ├── Easy (2 chains)
    ├── Medium (2 chains)
    ├── Hard (2 chains)
    └── Impossible (4 chains)
```

#### Task 3.3: Attack Pattern Analysis

**Work:** For each taxonomy node:
- Formal definition of attack pattern
- Required agent capabilities
- Invariant violations exploited
- Detection difficulty assessment
- Mitigation challenges (why current systems fail)

**Acceptance Criteria:**
- [ ] All 8 attack chains mapped to invariant violations
- [ ] Hierarchical taxonomy structure complete
- [ ] Alternative views (by invariant, by difficulty) provided
- [ ] Attack patterns formally defined
- [ ] Mitigation challenges documented

---

## Plan 02-04: Hard-to-Vary Validation

**Goal:** Apply Deutsch's hard-to-vary criterion to validate the core explanation: "A2A fraud is undetectable by current banking systems because AI agents violate all human behavioral invariants that fraud detection depends on."

**Deliverables:**
- `analysis/hard-to-vary-validation.md` — Validation analysis
- `analysis/core-explanation.md` — Formal statement of core explanation

### Task Breakdown

#### Task 4.1: Core Explanation Formulation

**Draft explanation:**
> "Banking fraud detection systems are built on human behavioral assumptions. AI agents violate all 9 of these assumptions — 4 external/physical (velocity, biometrics, device, location) and 5 internal/processing (cognitive, bounded rationality, identity persistence, computational limits, behavioral stability). This systematic violation creates fundamental blind spots that cannot be patched without rethinking detection from first principles."

**Work:** Refine into formal explanation with:
- Clear claim structure
- Evidence backing (from Phase 1)
- Logical dependence chain

#### Task 4.2: Hard-to-Vary Analysis

**Deutsch's criterion:** An explanation is hard-to-vary if attempting to vary it while maintaining consistency with evidence makes it less plausible or incoherent.

**Variations to test:**

1. **"A2A fraud is detectable with minor system adjustments"**
   - Test: Can we identify specific adjustments that would enable detection?
   - If variation requires changing 9/9 invariants simultaneously → hard-to-vary
   - If variation is vague ("better ML") → insufficient specificity

2. **"Only some invariants matter, not all 9"**
   - Test: Can we remove invariants while maintaining explanatory power?
   - Each invariant has independent attack vectors (Phase 1 evidence)
   - Removing any invariant leaves attack surface uncovered

3. **"Current systems can be adapted rather than replaced"**
   - Test: Can incremental adaptation address invariant violations?
   - Velocity: 10^2-10^4× gap requires fundamental rethinking
   - Biometrics: No physical form → cannot be patched
   - Cognitive: Perfect optimization vs. human limits → qualitative difference

4. **"New invariants will emerge to detect agents"**
   - Test: Are there undiscovered human invariants that could help?
   - Phase 1 literature survey was comprehensive
   - 9 invariants cover all major fraud detection approaches

**Work:** For each variation:
- State the variation clearly
- Test against Phase 1 evidence
- Assess whether variation is plausible or loses coherence
- Document why variation fails hard-to-vary test

#### Task 4.3: Validation Summary

**Work:** Produce:
- Statement of core explanation
- List of tested variations with rejection rationale
- Confidence assessment in hard-to-vary criterion
- Identification of any weak points or edge cases

**Acceptance Criteria:**
- [ ] Core explanation formally stated
- [ ] Major variations tested and rejected
- [ ] Rejection rationales grounded in Phase 1 evidence
- [ ] Hard-to-vary criterion satisfied
- [ ] Weak points/edge cases acknowledged

---

## Contract: Phase 2 Acceptance Tests

### Test TAXO-01: Invariant Mapping Completeness
**Summary:** All 9 human behavioral invariants documented with formal definitions, detection mechanisms, and literature citations.

### Test TAXO-02: Violation Mapping Completeness
**Summary:** All 9 invariants have agent property violation mappings with platform evidence and violation mechanisms.

### Test TAXO-03: Taxonomy Completeness
**Summary:** All 8 attack chains mapped to invariant violations; hierarchical taxonomy with alternative views provided.

### Test TAXO-04: Hard-to-Vary Validation
**Summary:** Core explanation formulated; major variations tested and rejected with evidence-based rationales.

---

## Forbidden Proxies

**fp-201:** Abstract invariant analysis without fraud detection grounding
**fp-202:** Violation claims without platform/literature evidence
**fp-203:** Taxonomy without invariant-attack chain linkage
**fp-204:** Hard-to-vary claims without variation testing

---

## Execution Order

**Sequential dependencies:**
1. 02-01 must complete first (provides invariant definitions)
2. 02-02 depends on 02-01 (uses invariant definitions)
3. 02-03 depends on 02-01 and 02-02 (uses both invariants and violations)
4. 02-04 depends on all previous (uses complete explanatory framework)

**Parallel opportunities:**
- Within each plan, tasks can proceed in parallel where independent
- 02-02 and 02-03 could partially overlap (preliminary taxonomy work)

---

## Timeline Estimate

- **02-01:** 2-3 days (consolidating existing documentation + new invariants)
- **02-02:** 2-3 days (mapping violations, requires careful analysis)
- **02-03:** 3-4 days (taxonomy development, multiple views)
- **02-04:** 3-4 days (hard-to-vary is intellectually demanding)

**Total:** 10-14 days for complete Phase 2

---

## Phase 2 Contract

### Claims

**claim-02-invariants:** Human behavioral invariants used in banking fraud detection comprehensively documented with all 9 invariants (4 external, 5 internal) formalized with literature citations.

**claim-02-violations:** Agent properties that violate each human invariant systematically mapped with platform evidence and violation mechanisms.

**claim-02-taxonomy:** A2A fraud attack taxonomy organized by invariant violation, covering all 8 attack chains with hierarchical classification and detection difficulty mapping.

**claim-02-hard-to-vary:** Core explanation that "A2A fraud is undetectable by current banking systems because agents violate all human behavioral invariants" validated against Deutsch's hard-to-vary criterion.

### Deliverables

- `deliv-invariants-complete`: Complete invariant reference document
- `deliv-invariant-violations`: Agent violation mapping document
- `deliv-attack-taxonomy`: A2A fraud taxonomy document
- `deliv-hard-to-vary-validation`: Validation analysis document

### References

- `ref-invariants`: Phase 1 literature survey (human invariants with citations)
- `ref-platform-analysis`: Phase 1 platform analysis (OpenClaw, Moltbook)
- `ref-attack-chains`: Phase 1 attack chain mapping (8 chains)

---

**Plan Status:** READY FOR EXECUTION
**Next Step:** Begin Plan 02-01 (Human Behavioral Invariant Mapping)
