# Decision Log

| ID | Phase | Decision | Rationale | Outcome |
|----|-------|----------|-----------|---------|
| D-01 | Init | arXiv + blog publication target | Fastest path to practitioner impact; bypass academic review cycles | Complete — `paper/agent-economy-fraud-arxiv.md` ready for submission |
| D-02 | Init | Platform documentation (OpenClaw/Moltbook) as primary anchor | Grounds analysis in actual agent behavior rather than abstract theory | Confirmed — provided concrete attack surface for threat model |
| D-03 | 1 | Synthetic data approach for empirical validation | No public A2A transaction datasets available | Validated in Phase 4 (precision 82.36%, recall 96.23%); real data obtained in Phase 5 |
| D-04 | 2 | 9-invariant taxonomy as complete framework | Literature survey + platform analysis converge on 9 human behavioral invariants | All 9 violated by agent properties; framework validated empirically |
| D-05 | 2 | Hard-to-vary criterion as validation method | Deutsch's epistemology provides falsifiability test beyond standard empirical checks | 4 variations rejected in Phase 2; 3 more in Phase 4; argument strengthens across phases |
| D-06 | 3 | 5-signal framework with AUC-proportional fusion weights | Signal combination based on empirical discriminative power | 4/5 signals active on real data; Value Flow strongest (Phase 5) |
| D-07 | 4 | Priority matrix scoring: impact 40%, urgency 30%, feasibility 20%, cost 10% | Balances immediate banking impact with implementation feasibility | 10 ranked recommendations produced; P0–P3 timeline across 0–36 months |
| D-08 | 5 | Dune Analytics MCP for real on-chain data | Only viable source for ERC-8004 agent transaction data; free tier accessible | 81,904 Base chain USDC txns; 665 agents labeled; recall transfers at 99.2% |
| D-09 | 5 | Value Flow signal weight restored 0.00→0.20 | Real timestamps available (unlike synthetic data); F1 triples | F1 triples on real data — validated correct |
| D-10 | 5 | Detection threshold lowered 0.24→0.08 for real data | Real data has compressed score distribution vs synthetic | Enables recall-focused operating point; FPR managed separately at 0.29 |
| D-11 | 5 | Label-noise-aware transfer criteria for Phase 6 go/no-go | Precision gap is label quality artifact, not signal failure; recall-primary evaluation | Phase 6 activated; recall-primary evaluation confirmed in Phase 6 |
| D-12 | 6 | Per-chain recall as primary success metric (not overall recall) | Chain 7 structural gap skews overall recall; per-chain analysis more informative | 7/8 chains at 100% per-chain recall; Chain 7 gap confirmed as architectural, not implementational |
| D-13 | 6 | Document Chain 7 gap as research contribution, not failure | Per-address scoring structurally cannot detect single-transaction swarm participants | Paper §8 frames collective detection as future work; motivates next-gen architecture |

---

_Log created: 2026-04-05 — Phase 6 transition_
