# Dataset Construction: Base Chain A2A Transaction Dataset

**Plan:** 05-02
**Constructed:** 2026-03-27
**Status:** COMPLETE

---

## Overview

This document describes the construction of the labeled transaction dataset used for Phase 5 signal validation. The dataset captures real-world USDC transfer activity on Base chain for 1,505 ERC-8004 registered agents and their human counterparties.

---

## Source Data

| Source | Description |
|--------|-------------|
| `data/base_erc8004_agents.json` | 1,505 ERC-8004 agent addresses from Base chain (Plan 05-01) |
| Dune Analytics `erc20_base.evt_transfer` | Base chain ERC-20 transfer events |
| USDC contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (Base USDC) |

---

## Ingestion Procedure

### Step 1: Batch Query Construction

The 1,505 agent addresses were split into batches of 100 to stay within the Dune community-tier query engine memory limit. Each batch used the following SQL pattern:

```sql
WITH agents(addr) AS (
  VALUES (0x...), (0x...), ...  -- 100 addresses per batch
)
SELECT
    t.evt_tx_hash,
    t.evt_block_number,
    t.evt_block_time,
    t."from" AS sender,
    t."to"   AS receiver,
    CAST(t.value AS DOUBLE) / 1e6 AS amount_usdc
FROM erc20_base.evt_transfer t
INNER JOIN agents a ON t."from" = a.addr
WHERE t.contract_address = 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
  AND t.evt_block_date >= DATE '2025-01-01'

UNION ALL

-- Receiver-side transfers (same filter, t."to" = a.addr)
```

The UNION ALL captures both outbound and inbound flows, giving the full bilateral picture needed for Value Flow and Network Topology signals.

### Step 2: Execution and Collection

- **Tool:** Dune MCP (`createDuneQuery` → `executeQueryById` → `getExecutionResults`)
- **Script:** `src/a2a_detection/scripts/fetch_dune_batched.py`
- **Batches:** 16 (15 × 100 addresses + 1 × 5 addresses)
- **Poll interval:** 10s, max wait 600s per batch
- **Output:** `data/dune_agent_transactions.csv` (81,904 rows)

### Step 3: Preprocessing to Parquet

Raw CSV was preprocessed into `data/transactions_dune.parquet` with standardized column types for fast loading in the signal computation pipeline:

| Column | Type | Description |
|--------|------|-------------|
| `evt_tx_hash` | string | Transaction hash |
| `evt_block_number` | int64 | Block number |
| `evt_block_time` | datetime64[ns] | Block timestamp (UTC) |
| `sender` | string | Sender address (checksummed) |
| `receiver` | string | Receiver address (checksummed) |
| `amount_usdc` | float64 | Transfer amount in USDC |

---

## Label Assignment

### Agent Labels

An address is labeled **agent** if it appears in `data/base_erc8004_agents.json` (ERC-8004 Identity Registry, Base chain). This is a ground-truth positive label: registry membership requires an on-chain registration transaction and is publicly verifiable.

- **665** agent addresses from the 1,505 registry entries had at least one transaction in the dataset window.

### Human Counterparty Labels

An address is labeled **human** if it:
1. Appears as `sender` or `receiver` in the transaction dataset, AND
2. Does NOT appear in the ERC-8004 registry

This is a **proxy label**, not ground truth. Known label noise sources:

| Noise Type | Example | Estimated Prevalence |
|------------|---------|---------------------|
| DEX routers | Uniswap Universal Router | High |
| MEV bots | Flashbots searchers | Moderate |
| Bridge contracts | Base Bridge | Low |
| Other smart contracts | Multisigs, DAO treasuries | Moderate |

Label noise in the negative class (humans) is the primary driver of the precision transfer gap documented in `analysis/transfer-gap-analysis.md`.

- **1,069** human counterparty addresses extracted

### Label Table Schema

`data/labels_dune.parquet`:

| Column | Type | Values |
|--------|------|--------|
| `address` | string | Checksummed ERC-55 address |
| `label` | string | `"agent"` or `"human"` |
| `source` | string | `"erc8004_registry"` or `"counterparty"` |

---

## Dataset Statistics

| Metric | Value |
|--------|-------|
| Total transactions | 81,904 |
| Date range | 2025-01-01 – 2026-03-27 |
| Unique addresses | 1,734 |
| Agent addresses | 665 (38.3%) |
| Human addresses | 1,069 (61.7%) |
| Median tx per agent | ~123 |
| Median tx per human | ~28 |
| Total USDC volume | ~$2.1M (estimated) |

---

## Reproducibility

To re-run the ingestion:

```bash
# Requires: DUNE_API_KEY set in fetch_dune_batched.py (or env var)
python -m a2a_detection.scripts.fetch_dune_batched
```

Output: `data/dune_agent_transactions.csv`

To re-run preprocessing (CSV → Parquet + labels):

```bash
python -m a2a_detection.scripts.bridge_dune_data
```

Output: `data/transactions_dune.parquet`, `data/labels_dune.parquet`

---

## Limitations

1. **Single chain only** — Base USDC transfers only; Ethereum and Arbitrum deferred. Cross-Platform signal remains inactive.
2. **Label noise in negatives** — ~20–40% of "human" addresses are estimated to be smart contracts. See transfer-gap-analysis.md §4.
3. **Temporal resolution** — Dune batches block timestamps; sub-second inter-transaction timing is not recoverable, limiting Temporal Consistency signal accuracy.
4. **Window start** — 2025-01-01 cutoff excludes early agent activity; agents registered before this date may appear to have fewer transactions than they actually have.

---

**Document Status:** COMPLETE
**Related Plans:** 05-01 (address acquisition), 05-02 (ingestion), 05-03 (invariant measurement), 05-04 (signal validation)
