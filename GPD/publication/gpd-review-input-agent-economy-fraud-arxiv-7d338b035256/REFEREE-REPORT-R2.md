# Referee Report R2

**Recommendation:** minor revision  
**Confidence:** high  
**Manuscript:** `GPD/review-input/agent-economy-fraud-arxiv.md`  
**SHA-256:** `3246d71037387a1d5bafc76becd9cdb40b7cac1179f8c60f7a2867a8f79c6f5b`

## Summary

The revision resolves the blocking issues from the first review round. The manuscript no longer claims necessary failure, absolute impossibility, production readiness, or a validated 6-12 month exploitation forecast. It now reads as an early measurement and detection-framework preprint with explicit empirical boundaries.

The strongest evidence remains the synthetic validation and attack-injection evaluation. The weak cleaned real-data AUC, noisy negative labels, threshold re-optimization, inactive Cross-Platform signal, and Chain 7 collective-detection gap are now visible in the abstract, evaluation, limitations, and conclusion.

## Resolved Major Issues

- **Claim scope:** resolved. The central claim is narrowed to human-invariant-only detectors under tested A2A scenarios.
- **Literature positioning:** materially improved for the narrowed scope.
- **Claim-test mapping:** resolved by the new claim-evidence map in the evaluation section.
- **Empirical caveats:** resolved. Fixed-threshold recall, re-optimized recall, cleaned AUC, label noise, and inactive CP are foregrounded.
- **Venue/readiness framing:** resolved. The paper is now framed as early measurement and framework work.

## Minor Remaining Issue

1. **Archive platform documentation before external submission.** OpenClaw and Moltbook are current platform sources. For long-term reproducibility, the authors should archive or snapshot the exact source versions used for the threat model. Tracked as `REF-R2-LIT-001`.

## Recommendation

Minor revision. The remaining issue is archival and reproducibility-related rather than conceptual. The manuscript's revised claim scope is proportionate to the evidence.
