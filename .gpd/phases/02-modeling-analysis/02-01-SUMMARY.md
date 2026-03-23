# Plan 02-01 Summary: Human Behavioral Invariant Mapping

**Phase:** 02-modeling-analysis
**Plan:** 02-01 Human Behavioral Invariant Mapping
**Status:** COMPLETE
**Date:** 2026-03-22
**Duration:** ~1 day

---

## Executive Summary

Successfully documented all 9 human behavioral invariants that banking fraud detection systems depend on. The invariants are categorized into External/Physical (4) and Internal/Processing (5), with complete formal definitions, literature citations, fraud detection usage patterns, and AI agent violation analysis.

**Deliverable Created:** `analysis/human-invariants-complete.md` (comprehensive reference document)

---

## Tasks Completed

### Task 1.1: External/Physical Invariants (4) ✓
- [x] 1.1.1 Created `analysis/human-invariants-complete.md` with unified invariant structure
- [x] 1.1.2 Documented Velocity Limits invariant (Van Vlasselaer 2017)
- [x] 1.1.3 Documented Biometric Authentication invariant (Jain 2021)
- [x] 1.1.4 Documented Device Fingerprinting invariant (Mowery 2012)
- [x] 1.1.5 Documented Location Constraints invariant (Zhang 2020)

### Task 1.2: Internal/Processing Invariants (5) ✓
- [x] 1.2.1 Documented Cognitive/Energy Constraints invariant (Van Vlasselaer 2017)
- [x] 1.2.2 Documented Bounded Rationality invariant (Tesfatsion 2021)
- [x] 1.2.3 Documented Identity Persistence/Legal Singularity invariant (Hoffman et al. 2020)
- [x] 1.2.4 Documented Computational Limits invariant (behavioral profiling literature)
- [x] 1.2.5 Documented Behavioral Pattern Stability invariant (Chandola 2009)

### Task 1.3: Cross-Invariant Analysis ✓
- [x] 1.3.1 Analyzed invariant interactions in detection systems
- [x] 1.3.2 Documented independent vs. coupled invariants
- [x] 1.3.3 Identified redundancy patterns
- [x] 1.3.4 Criticality analysis (most fundamental invariants identified)
- [x] 1.3.5 Wrote cross-invariant analysis section

### Acceptance Verification ✓
- [x] Verify: All 9 invariants documented with formal definitions
- [x] Verify: Each invariant has literature citation
- [x] Verify: Detection mechanism usage patterns documented
- [x] Verify: Cross-invariant analysis complete
- [x] Verify: No gaps vs. fraud detection literature

---

## Deliverables

| Deliverable ID | File | Status | Description |
|----------------|------|--------|-------------|
| deliv-invariants-complete | analysis/human-invariants-complete.md | ✓ Complete | Comprehensive reference for all 9 human behavioral invariants |

---

## Key Findings

### 9 Human Behavioral Invariants Documented

**External/Physical Invariants (4):**
1. **Velocity Limits** — Humans constrained to ~10-100 tx/day
2. **Biometric Authentication** — Physical presence required
3. **Device Fingerprinting** — Fixed device identity assumed
4. **Location Constraints** — Travel time limits apply

**Internal/Processing Invariants (5):**
5. **Cognitive/Energy Constraints** — Humans limited by fatigue, sleep, energy
6. **Bounded Rationality** — Limited computational optimization capability
7. **Identity Persistence/Legal Singularity** — Single legal identity, Sybil constraints
8. **Computational Limits** — No massive parallel computation
9. **Behavioral Pattern Stability** — Patterns stable over time

### Severity Classification

| Severity | Invariants | Count |
|----------|------------|-------|
| CATASTROPHIC | Velocity, Biometrics, Identity Persistence | 3 |
| SEVERE | Device, Location, Cognitive, Behavioral Stability | 4 |
| MODERATE | Bounded Rationality, Computational Limits | 2 |
| MARGINAL | None | 0 |

### Cross-Invariant Analysis

**Independent Invariants:** Velocity, Biometrics (no coupling)
**Coupled Invariants:** Device+Location, Cognitive+Behavioral Stability, Identity+Sybil
**Most Fundamental:** Velocity Limits (enables most attack chains)
**Redundancy:** Some coverage overlap (Device/Location both protect physical access)

---

## Contract Claims Validated

**claim-02-invariants:** ✓ All 9 human behavioral invariants formalized with literature citations

**Evidence:**
- All 9 invariants have formal definitions
- Each invariant includes literature citation
- Detection mechanism usage patterns documented
- Cross-invariant analysis complete
- No gaps vs. Phase 1 literature survey

---

## Platform Grounding

All invariant documentation grounded in Phase 1 outputs:
- Literature citations from `analysis/literature-survey.md`
- Platform capabilities from `analysis/openclaw-platform-analysis.md`
- Attack chains from `.gpd/phases/01-discovery-taxonomy/01-01-SUMMARY.md`

---

## Next Steps

**Proceed to Plan 02-02:** Agent Property Violation Analysis

Using the 9 invariants documented here, Plan 02-02 will:
1. Map agent properties that violate each invariant
2. Create `analysis/agent-invariant-violations.md`
3. Create `analysis/agent-capabilities-vs-humans.md` comparison
4. Classify violation severity (CATASTROPHIC/SEVERE/MODERATE/MARGINAL)

---

**Acceptance Test:** TAXO-01 (Invariant Mapping Completeness) ✓ PASSED
