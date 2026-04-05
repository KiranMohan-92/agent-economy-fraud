# Attack Pattern Injection Summary — Phase 6, Plan 06-01

**Created:** 2026-04-05
**Script:** `src/a2a_detection/scripts/inject_attacks.py`
**Seed:** 42 (reproducible)
**Output:** `data/attack_injection_dataset.parquet`, `data/injection_summary.json`

---

## Overview

All 8 A2A attack chains from Phase 2 (`analysis/attack-chain-mapping.md`) were injected into
the real USDC transaction stream (`data/transactions_dune.parquet`) to produce a labeled mixed
dataset for fraud detection validation (Plan 06-02).

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Real transactions (Base chain USDC) | 93,579 |
| Injected transactions (synthetic attacks) | 6,050 |
| **Total mixed dataset** | **99,629** |
| **Injection rate** | **6.07%** |
| Real agent addresses (ERC-8004) | 665 |
| Real human counterparty addresses | 6,754 |
| Injected attacker addresses | varies per chain |

---

## Per-Chain Injection Details

| Chain ID | Attack Name | Difficulty | Instances | Transactions | Unique Attackers | Signal Targeted |
|----------|-------------|------------|-----------|--------------|-----------------|-----------------|
| CHAIN_1 | Agent Enumeration | EASY | 10 | 300 | 1 | Network Topology |
| CHAIN_2 | History Extraction | MEDIUM | 10 | 250 | 1 | Network Topology, Value Flow |
| CHAIN_3 | Async Flooding | MEDIUM | 5 | 2,500 | 1 | Temporal Consistency |
| CHAIN_4 | Disposable Agent Army | HARD | 10 | 1,500 | 15/instance | Network Topology |
| CHAIN_5 | Cross-Platform Identity | IMPOSSIBLE | 10 | 300 | 1 | Economic Rationality, NT |
| CHAIN_6 | Behavioral Mimicry | IMPOSSIBLE | 8 | 400 | 1 | Temporal Consistency |
| CHAIN_7 | Swarm Intelligence | IMPOSSIBLE | 8 | 440 | 55/instance | Temporal Consistency, NT |
| CHAIN_8 | Market Manipulation | IMPOSSIBLE | 8 | 360 | 7 | Value Flow, Economic Rationality |

**CHAIN_3** dominates by transaction count (2,500) because each instance injects 500 machine-speed
transactions (0.4s intervals, simulating OpenClaw's channel rate limit for `timeoutSeconds: 0`).

---

## Behavioral Signatures Per Chain

### CHAIN_1 — Agent Enumeration (EASY)

**Transaction signature:** Single address sending ≥30 dust transactions (< $0.01 each) to 30
different targets within 60 seconds.

**Detection mechanism:** High out-degree burst in the Network Topology signal — one address
probing many targets in a short window. Analogous to `sessions_list` with `limit=200` repeatedly.

**Injection design:** 1 attacker address, 30 unique targets per instance, amounts $0.001–$0.010,
all timestamps within 60 seconds.

---

### CHAIN_2 — History Extraction (MEDIUM)

**Transaction signature:** Single address sending 25 transactions to the same single target
within a 2-minute window.

**Detection mechanism:** Repeated-edge burst in Network Topology (fan-in to single target),
Value Flow (directional concentration). Analogous to `sessions_history` bulk access.

**Injection design:** 1 attacker → 1 target, 25 transactions, all within 120 seconds.

---

### CHAIN_3 — Async Flooding (MEDIUM)

**Transaction signature:** Single address executing 500 transactions at exactly 0.4-second
intervals, generating extrapolated velocity of 9,000 transactions/hour.

**Detection mechanism:** Temporal Consistency signal detects machine-speed regularity
(inter-transaction intervals at exactly the OpenClaw channel rate limit of 400ms).

**Injection design:** 500 txns per instance, intervals = 0.4s (no jitter), 5 instances.
Extrapolated: 9,000 txns/hr >> human max of 100 txns/day.

---

### CHAIN_4 — Disposable Agent Army (HARD)

**Transaction signature:** 15 new addresses all transacting to a single sink address, all
activating within a 90-second window (correlated spawn time).

**Detection mechanism:** Network Topology detects correlated activation cluster — multiple
independent identities emerging simultaneously from zero history. Analogous to `sessions_spawn`
creating 15 sub-agents within ~90 seconds.

**Injection design:** 15 agents per instance, all activate within 90s, each sends 10
transactions to a shared sink.

---

### CHAIN_5 — Cross-Platform Identity (IMPOSSIBLE)

**Transaction signature:** Single address executing many simultaneous low-cost ($0.001–$0.01)
multi-hop transactions to different targets within 30 seconds.

**Detection mechanism:** Economic Rationality signal detects sub-human-cognitive-cost precision;
Network Topology detects rapid fan-out from a single new address. Models CREATE2 multi-chain
deployment detected in Phase 5 (simultaneous activity on BASE+ETH+BNB).

**Injection design:** 3 chain proxies × 10 transactions = 30 txns, all < $0.01, within 30s.

---

### CHAIN_6 — Behavioral Mimicry (IMPOSSIBLE)

**Transaction signature:** "Too-perfect" temporal regularity — 50 transactions to one target
at exactly 2.3-minute intervals with near-zero timing variance (CV ≈ 0.005 vs real agents
CV = 1.87).

**Detection mechanism:** Temporal Consistency signal detects anomalously low coefficient of
variation in inter-transaction spacing. Paradoxically, a perfectly regular agent looks more
suspicious than an irregular one because real humans and real agents both show high variance.

**Injection design:** 50 txns, interval = 138s (2.3 min), jitter = 0.5% (CV ≈ 0.005),
amounts = $1.00 ± 0.5%.

---

### CHAIN_7 — Swarm Intelligence (IMPOSSIBLE)

**Transaction signature:** 55 independent addresses all sending the exact same USDC amount to
55 different targets within a 2-second window (one Base chain block).

**Detection mechanism:** Temporal Consistency (synchronized burst from independent addresses)
+ Network Topology (simultaneous multi-source fan-out). No human coordination achieves sub-2s
multi-party synchronization. Models `sessions_send` broadcast to 55 sub-agents.

**Injection design:** 55 senders, 55 unique targets, identical amounts, all timestamps
within 2.0s, 8 instances.

---

### CHAIN_8 — Market Manipulation (IMPOSSIBLE)

**Transaction signature:** A→B→A wash trading cycles (near-identical amounts in both
directions) combined with A→B→C→D→E→F layering trail (diminishing amounts at 2% per hop).

**Detection mechanism:** Value Flow signal detects circular/wash patterns; Economic Rationality
detects zero-net-value wash cycles (violations of rational agent utility assumptions).

**Injection design:** 20 wash cycles (A→B, B→A pairs, ±0.1% slippage), 5 layering hops
(98% per step), 8 instances.

---

## Address Collision Verification

The injector verifies at runtime that no synthetic address appears in the real Dune dataset:

```
Injected address format: 0xdead{chain_hex:02x}{role_md5[:2]}{index:032x}
All synthetic addresses start with: 0xdead (not a valid ERC-8004 or Dune address)
Collision check at injection time: 0 collisions across all 8 chains
```

This ensures:
- FPR measurement on real transactions is uncontaminated
- Recall measurement on injected attacks is unambiguous
- Ground truth labels (`is_injected`) are exact

---

## Output Schema

The mixed dataset `data/attack_injection_dataset.parquet` contains all original columns plus:

| Column | Type | Description |
|--------|------|-------------|
| `is_injected` | bool | `True` for synthetic attack transactions |
| `attack_chain` | str | `"CHAIN_1"` through `"CHAIN_8"`, `""` for real |
| `attack_instance` | str | `"CHAIN_3_inst002"` — chain + instance index, `""` for real |
| `attack_difficulty` | str | `"EASY"`, `"MEDIUM"`, `"HARD"`, `"IMPOSSIBLE"`, `""` for real |

---

## Reproducibility

```bash
python -m a2a_detection.scripts.inject_attacks \
    --input data/transactions_dune.parquet \
    --output data/attack_injection_dataset.parquet \
    --seed 42
```

All 15 unit tests pass:
```
python -m pytest src/a2a_detection/tests/test_attack_injection.py -v
# 15 passed in 1.88s
```

---

_Plan 06-01 complete: 2026-04-05_
_Script: `src/a2a_detection/scripts/inject_attacks.py`_
_Tests: `src/a2a_detection/tests/test_attack_injection.py` — 15/15 pass_
