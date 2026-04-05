# Phase 6 TODO: Fraud Validation

**Created:** 2026-04-05
**Status:** Active — Go/no-go: GO (see `06-GO-NO-GO.md`)
**Based on:** Phase 6 plan, Phase 5 results, 8-chain attack taxonomy (Phase 2)

---

## Plan 06-01: Attack Pattern Injection

**Goal:** Inject synthetic instances of all 8 attack chains into the real transaction stream,
producing a labeled mixed dataset for fraud detection validation.

**Inputs:**
- `data/transactions_dune.parquet` — 81,904 real USDC transactions
- `analysis/attack-chain-mapping.md` — 8 attack chains with behavioral signatures
- `src/a2a_detection/` — detection framework (pip-installable)

**Output:** `data/attack_injection_dataset.parquet` — real + injected transactions, labeled

### Task 1.1: Injection Framework Design
- [ ] 1.1.1 Design `AttackInjector` class with `inject(chain_id, transactions, n_attacks)` API
- [ ] 1.1.2 Define injected transaction schema: all real fields + `is_injected`, `attack_chain`, `attack_instance_id`
- [ ] 1.1.3 Define injection rate: 5% of transaction volume per chain (≈4,095 injected transactions total)

### Task 1.2: Implement Chain-Specific Injectors
- [ ] 1.2.1 CHAIN 1 — Agent Enumeration: inject burst session_list-like probing (≥10 queries/minute from one address)
- [ ] 1.2.2 CHAIN 2 — History Extraction: inject bulk repeated reads of same address in short window
- [ ] 1.2.3 CHAIN 3 — Async Flooding: inject velocity burst (>9,000 txns/hour simulation on 1-hour clip)
- [ ] 1.2.4 CHAIN 4 — Agent Army: inject correlated cluster of ≥10 new addresses transacting simultaneously
- [ ] 1.2.5 CHAIN 5 — Cross-Platform Identity: inject multi-chain simultaneous txns from same CREATE2 address
- [ ] 1.2.6 CHAIN 6 — Behavioral Mimicry: inject "too-perfect" temporal clone (CV < 0.05 vs real agents CV=1.87)
- [ ] 1.2.7 CHAIN 7 — Swarm Intelligence: inject ≥50 addresses sending identical amounts within 2-second window
- [ ] 1.2.8 CHAIN 8 — Market Manipulation: inject wash trading pattern (A→B→A cycles, layered amounts)

### Task 1.3: Build Mixed Dataset
- [ ] 1.3.1 Inject all 8 attack chains into real transaction stream
- [ ] 1.3.2 Shuffle mixed dataset (preserve temporal ordering within injection instances)
- [ ] 1.3.3 Save to `data/attack_injection_dataset.parquet`
- [ ] 1.3.4 Produce injection summary: counts per chain, overall injection rate

### Task 1.4: Unit Tests
- [ ] 1.4.1 Test each injector produces correct behavioral signatures
- [ ] 1.4.2 Test injected addresses are not in real address set
- [ ] 1.4.3 Test total injection rate is ≤10% of real transaction volume

### Plan 06-01 Acceptance Verification
- [ ] Verify: All 8 attack chains injected, each with ≥50 transaction instances
- [ ] Verify: `data/attack_injection_dataset.parquet` exists with `is_injected` label column
- [ ] Verify: Unit tests pass for all injectors
- [ ] Create `analysis/attack-injection-summary.md` documenting injection methodology
- [ ] Create `.gpd/phases/06-fraud-validation/06-01-SUMMARY.md`

---

## Plan 06-02: Detection Validation

**Goal:** Run the 5-signal framework on the mixed dataset; verify ≥90% recall on injected
attacks and ≤5% FPR on real benign agent transactions.

**Inputs:**
- `data/attack_injection_dataset.parquet` (from 06-01)
- `src/a2a_detection/` — detection framework

**Output:** `data/fraud_detection_results.parquet`, `analysis/fraud-detection-validation.md`

### Task 2.1: Per-Chain Detection Analysis
- [ ] 2.1.1 Score all addresses in mixed dataset using `AgentFraudDetector`
- [ ] 2.1.2 Compute per-chain recall (TP / (TP + FN)) for each of the 8 attack chains
- [ ] 2.1.3 Compute overall recall across all injected attacks
- [ ] 2.1.4 Compute FPR on real benign agent transactions (FP / (FP + TN))

### Task 2.2: Threshold Analysis
- [ ] 2.2.1 Sweep threshold from 0.05 to 0.50 (step 0.01)
- [ ] 2.2.2 Find optimal threshold maximizing recall subject to FPR ≤ 5%
- [ ] 2.2.3 Report operating point: recall, precision, F1, FPR at chosen threshold

### Task 2.3: Chain-Difficulty Correlation
- [ ] 2.3.1 Compare per-chain recall to Phase 2 difficulty classification (EASY/MEDIUM/HARD/IMPOSSIBLE)
- [ ] 2.3.2 Check: EASY chains should have recall ≥95%, MEDIUM ≥90%, HARD ≥80%, IMPOSSIBLE ≥50%
- [ ] 2.3.3 Document any mismatches as research findings

### Task 2.4: Signal Contribution Analysis
- [ ] 2.4.1 For each attack chain, identify which signal contributes most to detection
- [ ] 2.4.2 Validate that chain-signal correspondence matches theoretical predictions from Phase 2:
        - Velocity attacks (3,7) → Temporal Consistency signal
        - Identity attacks (4,5) → Network Topology signal
        - Economic attacks (8) → Economic Rationality + Value Flow signals
        - Enumeration attacks (1,2) → Network Topology signal

### Plan 06-02 Acceptance Verification
- [ ] Verify: Overall recall on injected attacks ≥90%
- [ ] Verify: All 8 chains tested (via injection; Chain 5/6/7/8 "IMPOSSIBLE" chains given special analysis)
- [ ] Verify: FPR on real benign agents ≤5% at chosen threshold
- [ ] Create `analysis/fraud-detection-validation.md` with full metrics table
- [ ] Create `data/fraud_detection_results.parquet`
- [ ] Create `.gpd/phases/06-fraud-validation/06-02-SUMMARY.md`

---

## Plan 06-03: Real-World Fraud Case Analysis

**Goal:** Document any known real A2A fraud cases; confirm or note absence for the paper.

### Task 3.1: Literature and News Search
- [ ] 3.1.1 Search for reported A2A agent fraud incidents (2024–2026) in academic and industry sources
- [ ] 3.1.2 Check the 8 attack chain signatures against any known incidents
- [ ] 3.1.3 Document: case count, chain types, whether framework would have caught them

### Task 3.2: Absence Documentation (if no cases found)
- [ ] 3.2.1 Document that ecosystem is nascent (ERC-8004 launched ~2025, Base A2A commerce < 2 years old)
- [ ] 3.2.2 Note: absence of known cases does not negate attack surface — validates "pre-crime" framing
- [ ] 3.2.3 Identify leading indicators (rising agent-registered addresses, USDC volume growth) as predictors

### Plan 06-03 Acceptance Verification
- [ ] Create `analysis/real-world-fraud-cases.md`
- [ ] Create `.gpd/phases/06-fraud-validation/06-03-SUMMARY.md`

---

## Plan 06-04: arXiv Paper

**Goal:** Draft complete arXiv preprint with full methodology, empirical results, and
recommendations. Target: 10–15 pages, NeurIPS workshop format.

**Output:** `paper/agent-economy-fraud-arxiv.md` (Markdown, LaTeX-convertible)

### Task 4.1: Paper Structure and Sections
- [ ] 4.1.1 Abstract (250 words): problem, approach, key results, contribution
- [ ] 4.1.2 §1 Introduction: A2A commerce growth, fraud detection gap, contributions
- [ ] 4.1.3 §2 Background: human behavioral invariants, A2A platform primitives (OpenClaw/Moltbook)
- [ ] 4.1.4 §3 Threat Model: 8 attack chains, detection difficulty taxonomy
- [ ] 4.1.5 §4 Framework: 5-signal detection methodology, signal specifications, fusion
- [ ] 4.1.6 §5 Evaluation: synthetic (Phase 4) + real-world (Phase 5) + fraud injection (Phase 6) results
- [ ] 4.1.7 §6 Recommendations: P0–P3 implementation guidance for banking/fintech
- [ ] 4.1.8 §7 Limitations and Future Work: label quality, Cross-Platform signal, TC canary insight
- [ ] 4.1.9 §8 Conclusion
- [ ] 4.1.10 References (key: ERC-8004, OpenClaw, Moltbook, multi-agent fraud literature)

### Task 4.2: Key Figures and Tables
- [ ] 4.2.1 Figure 1: 9 human behavioral invariants vs agent properties (violation heatmap)
- [ ] 4.2.2 Figure 2: 5-signal detection framework architecture
- [ ] 4.2.3 Table 1: Synthetic vs real vs fraud-injection performance comparison
- [ ] 4.2.4 Table 2: Per-chain detection recall vs difficulty classification
- [ ] 4.2.5 Figure 3: Precision-recall curve on mixed dataset (Phase 6)

### Task 4.3: Hard-to-Vary Validation in Paper
- [ ] 4.3.1 State core explanation: "Fraud detection built on human invariants fails against agents"
- [ ] 4.3.2 Document 4 Phase 2 variations rejected (behavioral → structural, detection → prevention, etc.)
- [ ] 4.3.3 Document 3 Phase 4 empirical variations rejected
- [ ] 4.3.4 Show empirical evidence strengthens the hard-to-vary argument

### Plan 06-04 Acceptance Verification
- [ ] Verify: Paper covers all 8 attack chains
- [ ] Verify: All three evaluation stages present (synthetic, real, injected)
- [ ] Verify: Hard-to-vary argument stated and defended
- [ ] Verify: All key references cited
- [ ] Create `paper/agent-economy-fraud-arxiv.md`
- [ ] Create `.gpd/phases/06-fraud-validation/06-04-SUMMARY.md`

---

## Phase 6 Completion Checklist

### Contract Claims Verification
- [ ] claim-06-injection: All 8 attack chains injected into real data stream
- [ ] claim-06-recall: ≥90% recall on injected attacks at FPR ≤5%
- [ ] claim-06-chains: All 8 attack chains tested and documented
- [ ] claim-06-paper: arXiv paper drafted with full methodology and results

### Deliverables Verification
- [ ] deliv-injection-dataset: data/attack_injection_dataset.parquet
- [ ] deliv-detection-results: data/fraud_detection_results.parquet
- [ ] deliv-injection-summary: analysis/attack-injection-summary.md
- [ ] deliv-validation-analysis: analysis/fraud-detection-validation.md
- [ ] deliv-fraud-cases: analysis/real-world-fraud-cases.md
- [ ] deliv-paper: paper/agent-economy-fraud-arxiv.md

### Phase 6 Handoff
- [ ] All 4 plan SUMMARY.md files created
- [ ] STATE.md updated with Phase 6 completion
- [ ] ROADMAP.md updated with Phase 6 completion
- [ ] Paper submitted to arXiv (or marked ready for submission)

---

_Phase 6 activated: 2026-04-05_
_Go/no-go: GO (see `06-GO-NO-GO.md`)_
