# Phase 5: Ecosystem Characterization (Real-World A2A Data)

**Goal:** Validate agent detection signals against real on-chain A2A transaction data by constructing the first labeled agent-vs-human transaction dataset

**Depends on:** Phase 4 (Validation and Recommendations), On-chain data research (2026-03-24)

**Requirements:** EXT-01 (Empirical validation with production-scale A2A transaction data)

**Success Criteria** (what must be TRUE):

1. Go/no-go gate passed: ERC-8004 registered agents have measurable overlap with x402/DeFi transaction activity
2. Labeled dataset of ≥10K agent transactions with ground-truth labels constructed
3. All 9 human behavioral invariant violations measured in real agent data
4. 5-signal detection framework tested on real data with measurable precision/recall
5. Synthetic-to-real transfer gap quantified explicitly

**Contract Coverage:**

- Decisive outputs: Labeled A2A dataset, real-world signal measurements, transfer gap analysis
- Anchors: ERC-8004 registry (contract `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`), x402 facilitator transactions, Dune Analytics
- Forbidden proxies: Scraping without validation; assuming synthetic results transfer without measurement; using ERC-8004 labels without verifying behavioral consistency

**Plans:**

- 05-01: Go/No-Go Gate — ERC-8004 ↔ x402 overlap analysis (Dune SQL)
- 05-02: Data ingestion pipeline — ERC-8004 agent registry + x402 transactions + Virtuals Protocol
- 05-03: Invariant violation measurement — Test 9 human invariants against real agent behavior
- 05-04: Signal validation — Run 5-signal detection framework on real data, measure transfer gap

**GPD Verification Flags (from pre-phase verification):**

| Risk | Severity | Mitigation |
|------|----------|------------|
| Label_Accuracy → 0: ERC-8004 labels may not correlate with actual agent behavior | CRITICAL | Validate sample of ERC-8004 addresses behave as agents on-chain (Plan 05-01) |
| Fraud_Rate → 0: No real fraud in early ecosystem | HIGH | Reframe as agent detection validation, not fraud detection (Phase 5 scope) |
| Data_Volume → 0 after filtering: Genuine A2A commerce may be minimal | HIGH | Set 10K labeled txn minimum as go/no-go; expand to Virtuals + Moltbook if needed |
| ERC8004_x402_Overlap → 0: Cross-reference may fail | MEDIUM | Check overlap FIRST (Plan 05-01 is the gate) |
| Label bias: Registered agents skew legitimate | MEDIUM | Supplement with behavioral heuristics for unregistered agents |

---

_Phase created: 2026-03-24_
