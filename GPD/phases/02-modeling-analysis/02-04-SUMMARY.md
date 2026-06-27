# Plan 02-04 Summary: Hard-to-Vary Validation

**Phase:** 02-modeling-analysis
**Plan:** 02-04 Hard-to-Vary Validation
**Status:** COMPLETE
**Date:** 2026-03-22
**Duration:** ~1 day

---

## Executive Summary

Successfully applied Deutsch's hard-to-vary criterion to validate the core explanation: *"A2A fraud is undetectable by current banking systems because AI agents violate all human behavioral invariants."* Tested 4 alternative explanations against Phase 1 evidence; all 4 rejected with high confidence. Core explanation withstands hard-to-vary testing.

**Deliverables Created:**
- `analysis/core-explanation.md` — Formal explanation with logical dependence chain
- `analysis/hard-to-vary-validation.md` — Variation testing and rejection rationales

---

## Tasks Completed

### Task 4.1: Core Explanation Formulation ✓
- [x] 4.1.1 Created `analysis/core-explanation.md`
- [x] 4.1.2 Drafted core explanation statement
- [x] 4.1.3 Refined into formal explanation with clear claim structure
- [x] 4.1.4 Validated explanation grounded in Phase 1 results

### Task 4.2: Hard-to-Vary Analysis ✓
- [x] 4.2.1 Created `analysis/hard-to-vary-validation.md`
- [x] 4.2.2 Tested Variation 1: "Minor system adjustments sufficient" → REJECTED
- [x] 4.2.3 Tested Variation 2: "Only some invariants matter" → REJECTED
- [x] 4.2.4 Tested Variation 3: "Current systems can be adapted" → REJECTED
- [x] 4.2.5 Tested Variation 4: "New invariants will emerge" → REJECTED
- [x] 4.2.6 Tested edge cases and partial valid concerns (3 identified)

### Task 4.3: Validation Summary ✓
- [x] 4.3.1 Wrote final core explanation statement
- [x] 4.3.2 Documented all tested variations with rejection rationales
- [x] 4.3.3 Assessed confidence in hard-to-vary criterion satisfaction
- [x] 4.3.4 Identified weak points/edge cases (3 partial concerns documented)
- [x] 4.3.5 Validated rejection rationales grounded in Phase 1 evidence
- [x] 4.3.6 Updated `.gpd/phases/02-modeling-analysis/02-04-SUMMARY.md` with results

---

## Deliverables

| Deliverable ID | File | Status | Description |
|----------------|------|--------|-------------|
| deliv-core-explanation | analysis/core-explanation.md | ✓ Complete | Formal explanation with logical chain |
| deliv-hard-to-vary-validation | analysis/hard-to-vary-validation.md | ✓ Complete | Variation testing results |

---

## Key Findings

### Core Explanation Statement

> "Banking fraud detection systems are built on human behavioral assumptions that AI agents systematically violate. Current systems depend on 9 human behavioral invariants—4 external/physical (velocity limits, biometric authentication, device fingerprinting, location constraints) and 5 internal/processing (cognitive/energy constraints, bounded rationality, identity persistence, computational limits, behavioral pattern stability). AI agents violate all 9 of these invariants by their fundamental nature as software entities without physical form, biological constraints, or persistent legal identity. This systematic violation creates fundamental blind spots that cannot be patched without rethinking detection from first principles."

### Logical Dependence Chain

```
P1: Fraud detection → Built on human behavioral assumptions
P2: Human assumptions → Take form of 9 behavioral invariants
P3: AI agents → Violate all 9 invariants by definition
C1: Therefore: Fraud detection → Has fundamental blind spots for agents
C2: Therefore: Current systems → Cannot be patched; must be redesigned
C3: Therefore: Detection → Requires first-principles rethink
```

### Explanation Properties

| Property | Status | Evidence |
|----------|--------|----------|
| **Falsifiability** | ✓ Falsifiable | 0/9 invariants intact; 0/8 chains Easy |
| **Explanatory Power** | ✓ High | Explains why all 8 attack chains fail |
| **Parsimony** | ✓ Parsimonious | More specific than alternatives |
| **Precision** | ✓ Precise | 9 invariants, specific violation types |

### Hard-to-Vary Validation Results

| Variation | Claim | Test Result | Rejection Confidence |
|-----------|-------|-------------|---------------------|
| **Variation 1** | Minor adjustments sufficient | **REJECTED** — 9/9 adjustments are MAJOR | HIGH |
| **Variation 2** | Only some invariants matter | **REJECTED** — All 9 have independent attack vectors | HIGH |
| **Variation 3** | Adaptation sufficient | **REJECTED** — 9/9 require fundamental redesign | HIGH |
| **Variation 4** | New invariants will emerge | **REJECTED** — No viable candidates identified | HIGH |

**Result:** ✓ Core explanation passes hard-to-vary criterion

---

## Variation Testing Summary

### Variation 1: "Minor System Adjustments"

**Claim:** A2A fraud detectable with minor adjustments (raise thresholds, update rules, improve ML)

**Why It Fails:**
- 9/9 required adjustments are MAJOR system replacements
- Biometric replacement impossible (agents have no physical form)
- Device fingerprinting cannot handle unlimited rotation
- Location detection cannot apply to locationless entities
- Even with 10^6× velocity threshold expansion, legitimate agent activity indistinguishable from fraud

**Rejection Confidence:** HIGH

### Variation 2: "Only Some Invariants Matter"

**Claim:** Not all 9 invariants are equally important; could focus on critical few

**Why It Fails:**
- All 9 invariants have independent attack vectors (documented in Plan 02-03)
- Removing any invariant leaves specific attack types uncovered
- Focusing on 3 "critical" invariants still leaves 50% of attack chains exposed
- Agent violations are correlated (no physical form breaks 3 invariants simultaneously)

**Rejection Confidence:** HIGH

### Variation 3: "Current Systems Can Be Adapted"

**Claim:** Incremental adaptation sufficient; no need for complete redesign

**Why It Fails:**
- 9/9 invariants require fundamental redesign, not incremental adaptation
- For adaptive invariants (behavioral, cognitive), agents adapt faster than systems can update (arms race)
- Economic fundamentals (identity cost→0) cannot be adapted away
- Indistinguishability problem persists even with adaptations

**Rejection Confidence:** HIGH

### Variation 4: "New Invariants Will Emerge"

**Claim:** As A2A commerce grows, new human/agent invariants will emerge for detection

**Why It Fails:**
- Phase 1 literature survey was comprehensive (37 papers across multiple domains)
- No additional human invariants found (9 invariants cover all major approaches)
- No agent-specific invariants identified that are both (a) inherent to agents and (b) useful for detection
- Confuses technical characteristics with behavioral invariants

**Rejection Confidence:** HIGH

---

## Edge Cases and Partial Valid Concerns

### Partial Valid Concern 1: Hybrid Human-Agent Systems

**Concern:** Systems involving both humans and agents

**Analysis:**
- Hybrid systems exist (humans use agent tools)
- However, fraud detection must still distinguish human vs. agent-perpetrated fraud
- Hybrid nature doesn't solve detection problem

**Verdict:** Important nuance, but not a refutation.

### Partial Valid Concern 2: Regulatory Constraints

**Concern:** Legal/regulatory constraints on agents

**Analysis:**
- Regulations may emerge (agent disclosure requirements)
- However: (a) Enforcement requires detection (circular), (b) Bad actors ignore regulations, (c) Jurisdictional arbitrage possible
- Regulations constrain legitimate actors more than fraudsters

**Verdict:** Important complement, but doesn't solve detection.

### Partial Valid Concern 3: Economic Rationality

**Concern:** Economic rationality as new detection invariant

**Analysis:**
- Economic rationality (transactions must make economic sense) is candidate signal
- However: Not a behavioral invariant (humans also irrational); applies to both humans and agents
- Useful detection signal, but doesn't invalidate core explanation

**Verdict:** Valuable detection signal for Phase 3, but not a refutation.

---

## Confidence Assessment

### Overall Confidence in Core Explanation

**Confidence Level:** HIGH

**Supporting Factors:**
1. ✓ Comprehensive evidence base (Phase 1: 37 papers, 2 platforms, 8 chains)
2. ✓ Logical rigor (clear dependence chain from premises to conclusions)
3. ✓ Survived falsification attempts (all 4 alternatives rejected)
4. ✓ Precise claims (9 invariants, specific violation types)
5. ✓ No cherry-picking (all evidence considered, including negative results)

### Confidence in Hard-to-Vary Validation

**Confidence Level:** HIGH

**Supporting Factors:**
1. ✓ All 4 variations tested systematically
2. ✓ Rejection rationales grounded in Phase 1 evidence
3. ✓ Variations become less plausible when specified
4. ✓ Edge cases acknowledged (3 partial valid concerns)
5. ✓ No alternative explanations remain plausible

### Identified Weak Points

**Weak Point 1:** Economic Rationality Signal
- Not a behavioral invariant (applies to both humans and agents)
- Could be valuable for Phase 3 detection framework design
- Does not refute core explanation

**Weak Point 2:** Regulatory Approaches
- Regulations may complement detection
- Does not solve detection problem itself
- Important for comprehensive solution, but orthogonal to core explanation

**Weak Point 3:** Hybrid Detection
- May combine human and agent detection approaches
- Doesn't address pure agent-perpetrated fraud
- Partial solution, not refutation

**Assessment:** Weak points are not refutations; they represent complementary approaches that don't invalidate the core explanation.

---

## Phase 2 Completion Summary

### All Plans Completed

| Plan | Status | Deliverables |
|------|--------|-------------|
| **02-01** | ✓ Complete | human-invariants-complete.md |
| **02-02** | ✓ Complete | agent-invariant-violations.md, agent-capabilities-vs-humans.md |
| **02-03** | ✓ Complete | a2a-attack-taxonomy.md, invariant-based-attack-classification.md |
| **02-04** | ✓ Complete | core-explanation.md, hard-to-vary-validation.md |

### Contract Claims Validated

| Claim | Status | Evidence |
|-------|--------|----------|
| **claim-02-invariants** | ✓ Validated | All 9 invariants formalized with citations |
| **claim-02-violations** | ✓ Validated | Agent violations systematically mapped |
| **claim-02-taxonomy** | ✓ Validated | Taxonomy by invariant violation complete |
| **claim-02-hard-to-vary** | ✓ Validated | Core explanation validated against Deutsch's criterion |

### Deliverables Verification

| Deliverable | File | Status |
|------------|------|--------|
| deliv-invariants-complete | analysis/human-invariants-complete.md | ✓ Created |
| deliv-invariant-violations | analysis/agent-invariant-violations.md | ✓ Created |
| deliv-attack-taxonomy | analysis/a2a-attack-taxonomy.md | ✓ Created |
| deliv-invariant-classification | analysis/invariant-based-attack-classification.md | ✓ Created |
| deliv-core-explanation | analysis/core-explanation.md | ✓ Created |
| deliv-hard-to-vary-validation | analysis/hard-to-vary-validation.md | ✓ Created |

### Acceptance Tests Status

| Test | Status |
|------|--------|
| **TAXO-01:** Invariant mapping complete | ✓ PASSED |
| **TAXO-02:** Violation mapping complete | ✓ PASSED |
| **TAXO-03:** Taxonomy complete | ✓ PASSED |
| **TAXO-04:** Hard-to-vary validation complete | ✓ PASSED |

---

## Implications for Phase 3

### Input to Phase 3: Detection Framework Design

**Core Explanation Implications:**
1. Current systems are fundamentally incompatible with A2A commerce
2. Incremental improvements are insufficient
3. First-principles redesign is required

**Required for Phase 3:**
1. **Agent-invariant detection signals** — Economic rationality, network topology, value flow
2. **Multi-modal detection framework** — Combine multiple signals for robustness
3. **Adaptive detection paradigms** — Systems must adapt faster than agents
4. **Cross-platform correlation** — Must track across jurisdictional boundaries

**Key Question for Phase 3:** What detection signals are both (a) agent-invariant and (b) measurable from transaction data?

---

## Conclusion

**Phase 2 Status:** COMPLETE

**Achievement:**
- All 9 human behavioral invariants documented and formalized
- All 9 agent property violations mapped with severity assessment
- All 8 attack chains mapped to invariant violations
- Comprehensive taxonomy with dual organization (by invariant, by difficulty)
- Core explanation validated against hard-to-vary criterion

**Next Phase:** Phase 3 — Detection Framework Design

**Phase 3 Objective:** Design agent-aware fraud detection framework based on agent-invariant signals.

---

**Acceptance Test:** TAXO-04 (Hard-to-Vary Validation) ✓ PASSED
**Phase 2 Status:** READY FOR HANDOFF TO PHASE 3
