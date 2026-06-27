# Referee Report

**Recommendation:** major revision  
**Confidence:** medium  
**Manuscript:** $manuscript

## Summary

The manuscript identifies a timely and plausible security problem: A2A commerce breaks several assumptions behind human-oriented fraud detection. The taxonomy, five-signal framework, and CHAIN_7 negative result are useful. The paper is not ready in its current form because the title, abstract, and conclusion make stronger necessity, novelty, and deployment-timing claims than the standalone artifact supports.

## Major Issues

1. **Claim scope is too strong.** The paper repeatedly frames the result as necessary, fundamental, and likely to create systematic exploitation within 6-12 months. The reviewed artifact supports a narrower claim: current human-assumption detectors have clear blind spots under the tested A2A scenarios.

2. **Literature positioning is incomplete.** The references section remains partly placeholder-like and explicitly says additional references must be completed. The novelty claim needs concrete comparison to fraud detection, botnet, HFT manipulation, marketplace fraud, reputation/Sybil, and adversarial-ML literature.

3. **The hard-to-vary and completeness arguments need a claim-test map.** The manuscript should map each central claim to the dataset, threshold, acceptance test, and disconfirming result that supports it.

4. **Empirical claims need stronger caveats.** The cleaned real-data AUC is 0.515, precision is label-noise-limited, and Cross-Platform is inactive. The abstract and conclusion should carry those limitations, not only the headline recall and injection recall.

5. **Venue/readiness framing should shift.** The paper is interesting as an early measurement and detection-framework preprint. It should not read as a mature production validation until negative labels, confidence intervals, and collective detection are stronger.

## Minor Issues

- Reconcile the implementation test count: the body says 32 unit tests while Appendix C says 47 tests pass.
- Separate recommendations validated by the five-signal framework from broader policy proposals such as biometric mandates for agent-platform transactions.

## Required Revision Direction

A successful revision should narrow the main claim, complete the bibliography, add a claim-evidence table, move label-noise and inactive-signal caveats into the abstract/results, and present CHAIN_7 as the most important architectural gap rather than a footnote to otherwise complete detection.