---
phase: 06-fraud-validation
plan: 06
type: execute
wave: 1
depends_on: [05-ecosystem-characterization]
files_modified:
  - src/a2a_detection/scripts/inject_attacks.py
  - src/a2a_detection/scripts/validate_fraud_detection.py
  - analysis/real-world-fraud-cases.md
  - paper/agent-economy-fraud-arxiv.md
interactive: false

conventions:
  time_notation: "ISO 8601 for timestamps; seconds for timing intervals"
  address_notation: "0x-prefixed EVM addresses; 0xdead prefix for injected synthetic addresses"
  metric_notation: "recall, precision, ROC-AUC, and false-positive rate reported as unitless ratios or percentages"
  chain_notation: "CHAIN_1 through CHAIN_8 attack-chain identifiers"

contract:
  schema_version: 1
  scope:
    question: "Can the fraud detection framework validate injected or adjacent-domain A2A fraud patterns against real agent transaction data?"
    in_scope:
      - "Inject all eight attack chains into real transaction streams."
      - "Evaluate detection recall and false-positive rate on mixed real and injected data."
      - "Document real-world or adjacent-domain fraud evidence and synthesize the paper draft."
    out_of_scope:
      - "Claiming production-ready fraud prevention for attack classes not represented by the injection or adjacent-domain evidence."
    unresolved_questions:
      - "Confirmed real-world A2A fraud cases remain unavailable in the nascent ecosystem."
      - "Chain 7 swarm detection requires group-level scoring beyond the current per-address detector."
  context_intake:
    must_include_prior_outputs:
      - "GPD/phases/05-ecosystem-characterization/05-VERIFICATION.md"
      - "GPD/phases/06-fraud-validation/06-01-SUMMARY.md"
      - "GPD/phases/06-fraud-validation/06-02-SUMMARY.md"
      - "GPD/phases/06-fraud-validation/06-03-SUMMARY.md"
      - "GPD/phases/06-fraud-validation/06-04-SUMMARY.md"
    user_asserted_anchors:
      - "data/fraud_detection_metrics.json"
      - "analysis/real-world-fraud-cases.md"
      - "paper/agent-economy-fraud-arxiv.md"
    context_gaps:
      - "No confirmed real-world A2A fraud cases are available for direct validation."
      - "The current per-address scorer structurally misses one-transaction swarm addresses."
  claims:
    - id: claim-06-injection
      statement: "All 8 attack chains are injected into a real transaction stream with isolated synthetic addresses and reproducible generation code."
      claim_kind: other
      deliverables: [deliv-injector-script]
      acceptance_tests: [at-06-all-chains]
      references: [ref-06-metrics]
    - id: claim-06-detection
      statement: "The framework detects 7 of 8 injected attack chains at 100% per-chain recall, identifies the Chain 7 structural gap, and achieves false-positive rate below 5% at the operating threshold."
      claim_kind: other
      deliverables: [deliv-validation-script]
      acceptance_tests: [at-06-recall, at-06-fpr]
      references: [ref-06-metrics]
    - id: claim-06-real-world
      statement: "Because confirmed A2A fraud cases are not yet available, adjacent-domain fraud cases are mapped to the attack taxonomy and preserve the Chain 7 gap as a live limitation."
      claim_kind: other
      deliverables: [deliv-fraud-cases]
      acceptance_tests: [at-06-real-world]
    - id: claim-06-paper
      statement: "The arXiv paper draft synthesizes the six-phase methodology, validation results, limitations, and recommendations."
      claim_kind: other
      deliverables: [deliv-arxiv-paper]
      acceptance_tests: [at-06-paper]
  deliverables:
    - id: deliv-injector-script
      kind: code
      path: "src/a2a_detection/scripts/inject_attacks.py"
      description: "Attack injection script that generates all eight synthetic fraud chains in the real transaction stream."
      must_contain:
        - "All eight attack chains"
        - "Synthetic address isolation"
        - "Configurable injection parameters"
    - id: deliv-validation-script
      kind: code
      path: "src/a2a_detection/scripts/validate_fraud_detection.py"
      description: "Fraud detection validation script that runs SignalFusion and computes recall, ROC-AUC, and false-positive metrics."
      must_contain:
        - "Per-chain recall"
        - "Threshold sweep"
        - "False-positive rate calculation"
    - id: deliv-fraud-cases
      kind: report
      path: "analysis/real-world-fraud-cases.md"
      description: "Adjacent-domain fraud case mapping against the attack-chain taxonomy."
      must_contain:
        - "Case-to-chain mapping"
        - "Absence of confirmed A2A fraud noted"
        - "Chain 7 gap evidence"
    - id: deliv-arxiv-paper
      kind: report
      path: "paper/agent-economy-fraud-arxiv.md"
      description: "Complete arXiv-oriented paper draft covering phases 1 through 6."
      must_contain:
        - "Methodology"
        - "Evaluation"
        - "Limitations"
        - "Recommendations"
  references:
    - id: ref-06-metrics
      kind: dataset
      locator: "data/fraud_detection_metrics.json"
      role: benchmark
      why_it_matters: "Primary metrics artifact used to verify recall, ROC-AUC, confusion matrix arithmetic, and false-positive rate."
      applies_to: [claim-06-injection, claim-06-detection]
      carry_forward_to: [verification, writing]
      must_surface: true
      required_actions: [use, compare]
  acceptance_tests:
    - id: at-06-recall
      subject: claim-06-detection
      kind: benchmark
      procedure: "Recompute per-chain TP/FN totals from the metrics artifact."
      pass_condition: "Seven of eight chains have recall equal to 1.0 and the Chain 7 failure is explicitly documented."
      evidence_required: [deliv-validation-script, ref-06-metrics]
      automation: hybrid
    - id: at-06-all-chains
      subject: claim-06-injection
      kind: consistency
      procedure: "Confirm all eight attack chains are present in injection and validation outputs."
      pass_condition: "All eight chain identifiers are present and scored."
      evidence_required: [deliv-injector-script, deliv-validation-script, ref-06-metrics]
      automation: hybrid
    - id: at-06-fpr
      subject: claim-06-detection
      kind: benchmark
      procedure: "Recompute false-positive rate at the selected operating threshold."
      pass_condition: "FPR is less than or equal to 5% at threshold 0.29."
      evidence_required: [deliv-validation-script, ref-06-metrics]
      automation: hybrid
    - id: at-06-paper
      subject: claim-06-paper
      kind: existence
      procedure: "Verify the paper draft exists and covers the full six-phase methodology, results, limitations, and recommendations."
      pass_condition: "The draft includes methodology, evaluation, recommendations, limitations, and conclusion sections."
      evidence_required: [deliv-arxiv-paper]
      automation: hybrid
    - id: at-06-real-world
      subject: claim-06-real-world
      kind: consistency
      procedure: "Verify adjacent-domain cases are mapped to the attack taxonomy and that absence of confirmed A2A fraud is explicit."
      pass_condition: "Adjacent-domain cases cover the attack taxonomy and the Chain 7 limitation remains visible."
      evidence_required: [deliv-fraud-cases]
      automation: hybrid
  forbidden_proxies:
    - id: fp-06-synthetic-overgeneralization
      subject: claim-06-detection
      proxy: "Treating injected-pattern recall as proof of deployment-ready real-world fraud detection."
      reason: "The ecosystem lacks confirmed A2A fraud cases and synthetic regularity may overstate real-world robustness."
    - id: fp-06-chain7-omission
      subject: claim-06-detection
      proxy: "Claiming full attack-chain coverage while ignoring the Chain 7 swarm limitation."
      reason: "The validator records Chain 7 as a structural miss under per-address scoring."
  uncertainty_markers:
    weakest_anchors:
      - "No confirmed real-world A2A fraud cases were available; validation relies on injection and adjacent-domain evidence."
      - "Chain 7 swarm attacks remain outside the current detector architecture."
    unvalidated_assumptions:
      - "Injected attack parameters are representative of plausible early A2A fraud."
      - "Adjacent-domain fraud cases transfer meaningfully to agent-economy fraud mechanisms."
    competing_explanations:
      - "Synthetic injection regularity may explain part of the high recall on 7 of 8 chains."
      - "Benign label noise may affect measured false-positive rate."
    disconfirming_observations:
      - "Chain 7 recall is 0/55 under per-address scoring."
      - "Direct confirmed A2A fraud cases were not available."
  links:
    - id: link-06-detection-metrics
      source: ref-06-metrics
      target: claim-06-detection
      relation: benchmarks
      verified_by: [at-06-recall, at-06-fpr]
    - id: link-06-paper-synthesis
      source: deliv-arxiv-paper
      target: claim-06-paper
      relation: supports
      verified_by: [at-06-paper]
---

# Phase 6: Fraud Validation (Conditional on Phase 5)

**Goal:** Validate the fraud detection capability of the framework against real or realistically-injected attack patterns

**Depends on:** Phase 5 (Ecosystem Characterization) — proceeds only if Phase 5 confirms agent signals are detectable in real data

**Requirements:** EXT-01 (continued), original VALD-01 acceptance signal

**Entry Criteria** (ALL must be TRUE from Phase 5):

1. Labeled dataset constructed with ≥10K agent transactions
2. At least 3 of 5 detection signals show measurable effectiveness on real data
3. Transfer gap is bounded (real precision/recall ≥ 70% of synthetic benchmarks)
4. At least 5 of 9 invariant violations confirmed in real agent data

**Success Criteria:**

1. Framework detects injected attack patterns in real transaction streams with ≥90% recall
2. All 8 attack chains tested (via injection or real examples)
3. False positive rate on real benign agent transactions ≤ 5%
4. arXiv paper drafted with complete methodology and results

**Plans:**

- 06-01: Attack pattern injection — Inject synthetic fraud patterns into real transaction streams
- 06-02: Detection validation — Run framework on mixed real+injected data, measure fraud detection performance
- 06-03: Real-world fraud case analysis — If real A2A fraud cases emerge, validate against those
- 06-04: arXiv paper — Complete paper with Phase 5 + 6 results

**Conditional Activation:**

This phase activates ONLY when Phase 5 handoff confirms entry criteria are met.
If Phase 5 results are insufficient, this phase converts to future work in the arXiv paper.

---

_Phase created: 2026-03-24_
_Status: CONDITIONAL — awaiting Phase 5 results_
