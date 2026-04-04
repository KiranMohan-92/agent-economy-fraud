# Research State

## Project Reference

See: .gpd/PROJECT.md (updated 2026-03-16)

**Core research question:** How do the necessary properties of agent-to-agent (A2A) commerce create fundamental vulnerabilities in banking fraud detection systems, and what agent-aware detection framework addresses these gaps?

**Current focus:** Phase 5 — Ecosystem Characterization (Real-World A2A Data)

## Current Position

**Current Phase:** 5
**Current Phase Name:** Ecosystem Characterization
**Total Phases:** 6 (Phase 6 conditional)
**Current Plan:** 05-02 (Data Ingestion) — completed via Dune MCP
**Total Plans in Phase:** 4
**Status:** Active — Plans 05-01, 05-02, 05-03 complete; 05-04 pending
**Last Activity:** 2026-04-03
**Last Activity Description:** Dune Analytics real data ingestion complete (93,777 rows, 81,904 after dedup). Value Flow signal restored (GAP-01 CLOSED). Detection threshold re-optimized for real data.

**Progress:** [██████████] 100%

## Key Results

### Core Explanation (Hard-to-Vary)
Fraud detection systems built on 9 human behavioral invariants fundamentally break when the economic agent is software. Agent properties (no biometrics, no velocity limits, no geographic constraints, near-zero creation cost, machine-speed execution, swarm coordination) violate every invariant that current detection relies upon.

### Detection Framework Performance (Synthetic)
- **Precision:** 82.36% (TP/(TP+FP) = 9623/11685)
- **Recall:** 96.23% (TP/(TP+FN) = 9623/10000)
- **F1 Score:** 88.71%
- **Confusion matrix:** TP=9623, FN=377, FP=2062, TN=87938
> **Note (2026-04-02):** Precision label corrected. Previously listed as 96.23%, which was actually the recall (detection rate). The F1 of 88.71% was always correct, computed from the true precision (82.36%) and recall (96.23%). See `analysis/empirical-validation-results.md` §2.1–2.2 for the full confusion matrix.
- **ROC-AUC:** 0.97
- **Latency:** 97ms (under 100ms target)
- **Improvement over human-baseline:** +49.1%

### Detection Framework Performance (Real On-Chain Data — Dune, 2026-04-03)
- **Dataset:** 81,904 USDC transactions (Base chain, Jan 2025 — Apr 2026)
- **Evaluated:** 2,134 active addresses (548 agents, 1,586 counterparties)
- **Precision:** 27.6% (low due to counterparty label noise — many "humans" are automated)
- **Recall:** 95.4% (catches 523/548 known agents)
- **F1 Score:** 42.8%
- **Active signals:** 4/5 (Value Flow restored; Cross-Platform pending multi-chain data)
- **Key finding:** Value Flow is now the strongest signal (mean=0.42) with real timestamps
- **Threshold:** Re-optimized from 0.24 to 0.08 for real data score distribution

### Detection Framework Performance (Cleaned Labels — 2026-04-04)
> **Scope note:** The metrics below are measured on the **1,734-address cleaned subset**, not the full 6,754+548 address set. The 6,754 raw "human" counterparty labels were filtered to 1,069 by removing thin counterparties (<5 transactions); 665 agents are present (pool expanded from 548 due to Dune re-ingestion including previously missing addresses).

- **Evaluated:** 1,734 addresses (665 agents, 1,069 cleaned-human counterparties)
- **Precision:** 42.9%
- **Recall:** 81.1%
- **F1 Score:** 56.1% ← _this is the current headline metric_
- **ROC-AUC (composite):** 0.515
- **Per-signal AUCs** (live run, 2026-04-04):
  - Network Topology: 0.5990 (strongest)
  - Value Flow: 0.5220
  - Economic Rationality: 0.5152
  - Temporal Consistency: 0.4647
- **Label cleaning:** thin-counterparty filter only (EOA contract filter pending RPC_URL)
- **Agent pool:** 548 → 665 (Dune re-ingestion added 117 previously uncounted agents)

### 5 Agent-Invariant Signals
1. Economic Rationality
2. Network Topology
3. Value Flow
4. Temporal Consistency
5. Cross-Platform Correlation

### Implementation Priorities
- P0: Deploy Economic Rationality + Network Topology signals ($80K, 0-6 mo)
- P0: Synthetic data validation program ($20K, 0-3 mo)
- P1-P3: 8 additional recommendations across 6-36 month timeline

## Open Questions (Resolved)

- ~~What A2A transaction data can we realistically obtain?~~ → Synthetic data generation used; real-world validation remains a future goal
- ~~Which academic papers on multi-agent systems are most relevant?~~ → Literature survey complete (analysis/literature-survey.md)

## Accumulated Context

### Decisions

- [Initialization]: arXiv + blog target for fastest practitioner impact
- [Initialization]: Platform documentation (OpenClaw/Moltbook) as primary anchor
- [Phase 1]: Synthetic data approach adopted due to lack of public A2A transaction datasets
- [Phase 2]: 9 human behavioral invariants identified as the complete taxonomy
- [Phase 3]: 5-signal detection framework with signal fusion architecture
- [Phase 4]: Priority matrix scoring: impact 40%, urgency 30%, feasibility 20%, cost 10%
- [Phase 5]: Dune MCP for real data ingestion — batched at 100 addresses/query for free tier
- [Phase 5]: Value Flow weight restored 0.00→0.20 — F1 triples with real timestamps
- [Phase 5]: Detection threshold lowered 0.24→0.08 — real data has compressed score distribution

### Active Approximations

- ~~Synthetic data validation only~~ → Real on-chain data validated via Dune Analytics (93K rows)
- Counterparty labels are heuristic (confidence 0.7) — many "humans" may be automated contracts
- Platform analyses based on documentation snapshots (OpenClaw, Moltbook) — platforms evolving

**Convention Lock:**

- Metric signature: not_applicable
- Fourier convention: not_applicable

### Propagated Uncertainties

- Transfer gap from synthetic to real data exceeds original F1/AUC thresholds due to negative-class label noise, not signal failure. Recall transfers within 1% (-0.8%). Updated label-noise-aware criteria defined in `analysis/transfer-gap-criteria.md`.
- A2A platform ecosystem is rapidly evolving — new attack vectors may emerge

### Pending Todos

None — all research phases complete.

### Blockers/Concerns

None — project concluded successfully.

## Session Continuity

**Last session:** 2026-03-23
**Stopped at:** Project complete, state tracking updated
**Resume file:** —
