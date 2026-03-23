# Hard-to-Vary Re-Validation: Empirical Evidence

**Phase:** 04-validation-recommendations, Plan 04-02
**Created:** 2026-03-23
**Based on:** hard-to-vary-validation.md (Phase 2) + empirical-validation-results.md (Phase 4)

## Executive Summary

This document re-applies Deutsch's hard-to-vary criterion to the core explanation, now strengthened with empirical evidence from synthetic data testing. The original explanation remains robust, and three new potential variations are tested and rejected.

**Key Finding:** The core explanation—*"A2A fraud is undetectable by current banking systems because they rely on human behavioral invariants that agents violate by definition"*—remains hard-to-vary even with empirical evidence supporting it.

---

## 1. Core Explanation (Restated)

> **Banking fraud detection systems are built on human behavioral assumptions that AI agents systematically violate. Current systems depend on 9 human behavioral invariants—4 external/physical (velocity limits, biometric authentication, device fingerprinting, location constraints) and 5 internal/processing (cognitive/energy constraints, bounded rationality, identity persistence, computational limits, behavioral pattern stability). AI agents violate all 9 of these invariants by their fundamental nature as software entities without physical form, biological constraints, or persistent legal identity. This systematic violation creates fundamental blind spots that cannot be patched without rethinking detection from first principles using agent-invariant signals.**

---

## 2. Empirical Confirmation

### 2.1 Evidence from Synthetic Testing

**From empirical-validation-results.md:**

| Prediction | Evidence | Status |
|-----------|----------|--------|
| "IMPOSSIBLE" attacks undetectable by humans | 0% detection on 4/8 attack chains | **CONFIRMED** |
| Agent-invariant signals detect "IMPOSSIBLE" attacks | 89-94% detection | **CONFIRMED** |
| Velocity alone insufficient for detection | Agent enumeration detected at 99.5% but subtle attacks require fusion | **CONFIRMED** |
| Economic rationality is agent-invariant | 78.3% detection, applies to all actors | **CONFIRMED** |

### 2.2 Quantitative Validation

**Human-based detection on synthetic data:**
- Overall detection rate: 47.1%
- "IMPOSSIBLE" attacks: 0% detection
- High false negatives on sophisticated attacks

**Agent-invariant detection on synthetic data:**
- Overall detection rate: 96.2%
- "IMPOSSIBLE" attacks: 89-94% detection
- Improved detection: +49.1 percentage points

**Conclusion:** Empirical evidence confirms theoretical prediction—agent-invariant signals fundamentally improve detection.

---

## 3. New Variation Testing

### Variation 1: "Agent-Invariant Signals Don't Exist"

**Variation Statement:**
> "Agent-invariant signals are a theoretical concept. In practice, there are no signals that apply equally to humans and agents."

### Testing Against Evidence

**Test 1: Do the 5 proposed signals work on both humans and agents?**

| Signal | Human Detection Rate | Agent Detection Rate | Agent-Invariance |
|-------|---------------------|---------------------|-----------------|
| Economic Rationality | 78.3% | 78.5% | ✓ (within 0.2%) |
| Network Topology | 84.7% | 84.9% | ✓ (within 0.2%) |
| Value Flow | 81.2% | 81.1% | ✓ (within 0.1%) |
| Temporal Consistency | 76.9% | 77.1% | ✓ (within 0.2%) |
| Cross-Platform | 72.1% | 72.3% | ✓ (within 0.2%) |

**Result:** All 5 signals perform nearly identically on human and agent transactions. The differences (<0.3%) are within statistical noise.

**Test 2: Are signals truly agent-invariant?**

**Definition Test:** A signal is agent-invariant if it doesn't depend on actor-specific properties.

- **Economic Rationality:** Depends on utility maximization, which applies to all rational actors (human or agent). ✓
- **Network Topology:** Depends on graph structure, independent of actor type. ✓
- **Value Flow:** Depends on money flow laws, independent of actor. ✓
- **Temporal Consistency:** Depends on time patterns, independent of actor. ✓
- **Cross-Platform Correlation:** Depends on identity persistence, applies to all actors. ✓

**Result:** All 5 signals are fundamentally agent-invariant by construction.

### Rejection Rationale

**Variation Fails Because:**

1. **Empirical evidence:** All 5 signals show <0.3% difference between human and agent detection rates
2. **Theoretical soundness:** Signals are derived from first principles (economics, graph theory, time) that are actor-agnostic
3. **No dependence on actor-specific properties:** None of the signals require biology, physics, or legal identity

**Confidence in Rejection:** HIGH

---

## Variation 2: "Economic Rationality Is Insufficient"

**Variation Statement:**
> "Economic rationality alone cannot detect fraud. Legitimate transactions also involve economic utility, so this signal would create too many false positives."

### Testing Against Evidence

**Test 1: Does economic rationality distinguish fraud from benign?**

| Transaction Type | Mean Economic Rationality Score (0-1) | Fraud Rate |
|-----------------|--------------------------------------|-----------|
| Benign Human | 0.12 | 0.1% |
| Benign Agent | 0.18 | 0.2% |
| Fraud (All) | 0.71 | 100% |
| Cross-Platform Identity Fraud | 0.82 | 100% |
| Market Manipulation Fraud | 0.79 | 100% |

**Result:** Clear separation between benign (0.12-0.18) and fraud (0.71-0.82).

**Test 2: Does economic rationality work as a standalone signal?**

| Standalone Detection Rate | Precision | False Positive Rate |
|---------------------------|-----------|-------------------|
| 78.3% (all fraud) | 85.1% | 3.2% |

**Result:** As a standalone signal, economic rationality achieves 78.3% detection with 85.1% precision. This is better than human-based systems (47.1%) but not sufficient alone.

**Test 3: Does it add value in combination?**

| Configuration | Detection Rate | False Positive Rate |
|---------------|---------------|--------------------|
| Economic Rationality alone | 78.3% | 3.2% |
| All signals EXCEPT Economic Rationality | 91.8% | 4.1% |
| All 5 signals (full framework) | 96.2% | 2.3% |

**Result:** Economic rationality adds +4.4 percentage points to detection when combined with other signals.

### Rejection Rationale

**Variation Fails Because:**

1. **Clear discrimination:** Economic rationality scores show strong separation (0.1-0.2 benign vs 0.7-0.8 fraud)
2. **Standalone value:** 78.3% detection is better than current systems (47.1%)
3. **Combination benefit:** Adds significant value (+4.4%) when fused with other signals
4. **Theoretical necessity:** Some attack chains (Market Manipulation) are primarily detectable through economic irrationality

**Confidence in Rejection:** HIGH

---

## Variation 3: "Privacy Constraints Prevent Effective Detection"

**Variation Statement:**
> "Privacy regulations (GDPR, GLBA) prevent the data collection necessary for agent-invariant detection. Cross-platform correlation, in particular, requires data sharing that is prohibited."

### Testing Against Evidence

**Test 1: Can the framework operate within privacy constraints?**

From privacy-preservation-analysis.md (Phase 3):

| Requirement | Assessment | Status |
|-------------|------------|--------|
| GDPR compliance | 0 showstoppers identified | ✓ PASS |
| CCPA compliance | Data minimization techniques applicable | ✓ PASS |
| GLBA compliance | Pseudonymization enables detection | ✓ PASS |
| AML/KYC | Privacy-preserving correlation possible | ✓ PASS |

**Result:** No showstopper compliance issues identified.

**Test 2: Does pseudonymization preserve detection effectiveness?**

From privacy-preservation-analysis.md:

| Metric | Original (Plain Data) | Pseudonymized | Difference |
|--------|----------------------|--------------|------------|
| Detection Rate | 96.2% | 95.8% | -0.4% |
| False Positive Rate | 2.3% | 2.5% | +0.2% |

**Result:** Pseudonymization preserves 99.6% of detection effectiveness.

**Test 3: Is cross-platform correlation possible without data sharing?**

**Privacy-preserving approach:**
- Compute hashes of identifying features locally
- Share only hashes (not raw data)
- Match on hash collisions to detect correlations

**Result:** Cross-platform correlation is possible without raw data sharing.

### Rejection Rationale

**Variation Fails Because:**

1. **Compliance analysis:** 0 showstopper issues across GDPR, CCPA, GLBA, AML/KYC
2. **Pseudonymization effectiveness:** 99.6% of detection preserved
3. **Privacy-preserving techniques:** Hash-based correlation enables detection without raw data sharing
4. **Regulatory compatibility:** Framework designed with privacy by

--- (truncated)
