---
phase: 07-research-integrity-repair
plan: 07-01
title: Construct, provenance, implementation, and manuscript repair
status: COMPLETE
completed: 2026-07-09
---

# Plan 07-01 summary

## Outcome

The historical detector story was not rescued. It was replaced with the
strongest explanation and empirical boundary the evidence can support.

## Completed repairs

- Registry owner/default-wallet proxy and unknown-counterparty labels replace
  agent/human ground truth.
- Fraud decisions and operational tiers are removed from the score.
- Event identity is `(chain, tx_hash, evt_index)` and missing/conflicting
  identity fails closed.
- Injection senders include instance identity; old metrics are stale.
- Dune credentials are environment-only; owner rotation remains required.
- Stage 1 is withdrawn; Stage 2 is exploratory proxy ranking; Stage 3 is motif
  sensitivity only.
- The central explanation is the controller/mandate/provenance to
  tool-wallet/settlement causal chain.
- Paper, project state, claim ledger, source record, data manifest, and legacy
  status are repaired.

## Verification evidence

The current evidence and residual failures are recorded in
`GPD/VERIFICATION-2026-07-09.md`. Software tests cannot satisfy the missing
construct/data gates, and those blockers are carried forward to Phase 8.

## Authoritative deliverables

- `paper/agent-economy-fraud-arxiv.md`
- `GPD/analysis/discovery-agentic-fraud-economy-research-hardening.md`
- `GPD/CLAIM-LEDGER.md`
- `GPD/PRIMARY-SOURCE-EVIDENCE.md`
- `data/MANIFEST.md`
- `src/a2a_detection/scripts/audit_research_claims.py`
