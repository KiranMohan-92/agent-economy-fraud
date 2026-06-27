# Plan 05-02: Dune Data Ingestion — Summary

**Plan:** 05-02
**Completed:** 2026-03-27
**Status:** COMPLETE

---

## Claim Validated

**claim-05-data:** Sufficient real-world A2A transaction data can be ingested from Base chain to construct a labeled dataset suitable for signal validation.

---

## Execution Summary

### Method

Batch Dune Analytics queries via MCP against the Base chain USDC transfer event log (`erc20_base.evt_transfer`). The 1,505 ERC-8004 agent addresses from Plan 05-01 were split into 16 batches of 100 (community-tier memory limit). Each batch queried both inbound and outbound USDC transfers (UNION ALL) for transactions from 2025-01-01 onwards. Results were combined into a single CSV, then preprocessed into Parquet format with address-level label assignment.

### Key Results

| Metric | Value |
|--------|-------|
| Agent addresses queried | 1,505 |
| Batches executed | 16 |
| Raw transactions ingested | 81,904 |
| Date range | 2025-01-01 – 2026-03-27 |
| USDC contract (Base) | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Unique addresses in dataset | 1,734 |
| Labeled agents (ERC-8004) | 665 |
| Labeled human counterparties | 1,069 |

### Dataset Construction

Human counterparty labels were assigned by extracting all unique sender/receiver addresses that appeared in the transaction graph but were not in the ERC-8004 registry. This produces a naturally-labeled dataset without external annotation: registry membership is ground truth for agents; non-membership is the human proxy label (subject to label noise from DEX contracts, MEV bots, and other non-human non-agent addresses).

---

## Deliverables Created

1. **data/dune_agent_transactions.csv** — 81,904 raw USDC transfer events (tx hash, block number, block time, sender, receiver, amount_usdc)
2. **data/transactions_dune.parquet** — Preprocessed transaction table (same schema, Parquet format for fast loading)
3. **data/labels_dune.parquet** — Address label table: 1,734 addresses × {address, label, source}
4. **src/a2a_detection/scripts/fetch_dune_batched.py** — Reproducible ingestion script (batch MCP calls, poll-to-completion, CSV assembly)
5. **analysis/dataset-construction.md** — Dataset construction methodology, schema, and label assignment rationale

---

## Acceptance Verification

| Test | Target | Actual | Status |
|------|--------|--------|--------|
| Transaction count | ≥ 10,000 rows | 81,904 | ✓ PASS |
| Agent coverage | ≥ 500 labeled agents | 665 | ✓ PASS |
| Human counterparties | ≥ 500 labeled humans | 1,069 | ✓ PASS |
| Reproducible script | Committed, runnable | `fetch_dune_batched.py` committed | ✓ PASS |
| Parquet output | Machine-readable for Plans 05-03/05-04 | transactions_dune.parquet + labels_dune.parquet | ✓ PASS |

---

## Notable Findings

1. **Community-tier memory limit** — Queries over ~200 addresses trigger OOM on Dune free tier; batching at 100 was reliable throughout
2. **Cross-batch duplication** — A2A transactions where both sender and receiver are agents appear in two batches; this is intentional (each row represents a directional flow event)
3. **Label noise in negatives** — 1,069 "human" addresses include DEX routers, MEV bots, and bridge contracts — a known limitation documented in Plan 05-04's transfer gap analysis

---

**Document Status:** COMPLETE
**Phase 5 Progress:** Plans 05-01 ✓, 05-02 ✓, 05-03 ✓, 05-04 ✓
