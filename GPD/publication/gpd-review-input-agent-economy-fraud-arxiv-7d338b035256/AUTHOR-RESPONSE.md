# Author Response

**Manuscript:** `paper/main.tex` and synchronized review copy `paper/agent-economy-fraud-arxiv.md`  
**Prior referee report:** `GPD/publication/gpd-review-input-agent-economy-fraud-arxiv-7d338b035256/REFEREE-REPORT.md`  
**Revision date:** 2026-05-03

## Summary of Revision

We revised the manuscript to align the claim scope with the evidence. The central claim is now that fraud detection systems relying only on human behavioral invariants have systematic blind spots under the A2A scenarios tested here. We removed the stronger necessity and timing framing from the title, abstract, introduction, evaluation summary, limitations, conclusions, and Markdown review copy.

The revision also foregrounds the weak real-data ranking result, the fixed-threshold transfer gap, label noise, inactive cross-platform correlation, and the Chain 7 population-detection gap.

## Responses to Referee Issues

### REF-001: Claim scope too strong

**Action taken:** Addressed.

The title was changed from "Agent-to-Agent Commerce and the Collapse of Human Behavioral Invariants in Banking Fraud Detection" to "Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection." The abstract, introduction, background, evaluation, limitations, conclusions, and Markdown review copy now describe a narrower claim: human-invariant-only detectors have systematic blind spots under tested A2A scenarios.

Timing language was demoted from a prediction to a planning scenario. The conclusions now state that the timing remains uncertain and that the 6-12 month window is not a validated forecast.

### REF-002: Literature positioning incomplete

**Action taken:** Addressed within the current manuscript scope.

The related-work section was revised to position the paper against agent-based computational economics, multi-agent reinforcement learning, financial fraud detection, blockchain analytics, adversarial machine learning, Web2 bot detection, and AI agent security.

The bibliography was updated to replace the incorrect Tesfatsion entry and add verified references for anomaly detection, credit-card fraud detection, adversarial machine learning, and adversarial policies. The stale Markdown statement that additional references remained to be completed was removed.

### REF-003: Need claim-test map

**Action taken:** Addressed.

A new claim-evidence table was added to `paper/evaluation.tex` (`tab:claim_evidence`). It maps the central claims to supporting evidence and boundaries:

- Human-invariant-only detectors have A2A blind spots.
- Agent-native signals detect many agent patterns.
- Real-data transfer is partial.
- Per-address scoring has a structural boundary.

The table explicitly lists the caveats for platform scope, synthetic and injected attacks, real-data threshold re-optimization, label noise, and Chain 7.

### REF-004: Empirical caveats too weak

**Action taken:** Addressed.

The abstract now reports both the fixed-threshold recall (61.4%) and re-optimized recall (95.4%), and states that cleaned composite ROC-AUC is 0.515. The evaluation section now states that the re-optimized result carries a substantially higher false-positive rate and that the fixed-threshold comparison is the more honest measure of generalization.

The conclusions now describe the framework as a first-generation research prototype rather than mature production validation.

### REF-005: Recommendations not all validated

**Action taken:** Addressed.

The recommendations section now separates P0/P1 recommendations directly supported by implemented signals or measured gaps from P2/P3 policy and infrastructure hypotheses. The prior biometric-mandate framing was replaced with controller step-up authentication, with modality selection deferred to privacy and accessibility review.

### REF-006: Test count inconsistency

**Action taken:** Addressed.

The implementation section now reports 47 tests, matching the synchronized review copy and Phase 6 verification artifacts.

### REF-007: Venue/readiness framing

**Action taken:** Addressed.

The abstract, evaluation summary, limitations, conclusions, and Markdown review copy now frame the work as an early measurement and detection-framework study. The manuscript reserves the strongest claims for the attack chains and datasets actually tested.

## Files Revised

- `paper/main.tex`
- `paper/abstract.tex`
- `paper/introduction.tex`
- `paper/background.tex`
- `paper/threat_model.tex`
- `paper/detection_framework.tex`
- `paper/evaluation.tex`
- `paper/related_work.tex`
- `paper/recommendations.tex`
- `paper/limitations.tex`
- `paper/conclusions.tex`
- `paper/references.bib`
- `paper/agent-economy-fraud-arxiv.md`

## Remaining Constraints

The revision does not add new experiments, confidence intervals, or multi-chain data. It narrows the manuscript accordingly. PDF compilation could not be performed in the current environment because `pdflatex` and `bibtex` are not available on PATH.
