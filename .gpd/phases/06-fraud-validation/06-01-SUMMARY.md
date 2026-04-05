---
plan: 06-01
title: Attack Pattern Injection
status: COMPLETE
completed: 2026-04-05
---

# Plan 06-01 Summary: Attack Pattern Injection

## What Was Done

Implemented and executed attack pattern injection for all 8 A2A attack chains from the Phase 2
taxonomy (`analysis/attack-chain-mapping.md`). Injected synthetic attack transactions into the
real Base chain USDC dataset to produce a labeled mixed dataset for fraud detection validation.

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Injector script | `src/a2a_detection/scripts/inject_attacks.py` | ✓ Created |
| Unit tests | `src/a2a_detection/tests/test_attack_injection.py` | ✓ 15/15 pass |
| Mixed dataset | `data/attack_injection_dataset.parquet` | ✓ Generated |
| Injection summary JSON | `data/injection_summary.json` | ✓ Generated |
| Injection summary doc | `analysis/attack-injection-summary.md` | ✓ Created |

## Dataset Statistics

| Metric | Value |
|--------|-------|
| Real transactions | 93,579 |
| Injected transactions | 6,050 |
| Total | 99,629 |
| Injection rate | 6.07% |

## Per-Chain Injection

| Chain | Difficulty | Instances | Transactions |
|-------|------------|-----------|--------------|
| CHAIN_1 (Enumeration) | EASY | 10 | 300 |
| CHAIN_2 (History Extraction) | MEDIUM | 10 | 250 |
| CHAIN_3 (Async Flooding) | MEDIUM | 5 | 2,500 |
| CHAIN_4 (Agent Army) | HARD | 10 | 1,500 |
| CHAIN_5 (Cross-Platform) | IMPOSSIBLE | 10 | 300 |
| CHAIN_6 (Behavioral Mimicry) | IMPOSSIBLE | 8 | 400 |
| CHAIN_7 (Swarm Intelligence) | IMPOSSIBLE | 8 | 440 |
| CHAIN_8 (Market Manipulation) | IMPOSSIBLE | 8 | 360 |

## Key Design Decisions

1. **Address isolation**: All injected addresses start with `0xdead` prefix — verified to have
   zero collision with real Dune addresses. Ensures clean FPR/recall separation.

2. **Chain 3 volume**: 2,500 transactions (5 instances × 500 txns) because the flooding pattern
   requires sustained high velocity to be detectable — single instances would look like outlier
   noise rather than systematic attack.

3. **Address fix**: `_synthetic_addr` uses `f"{index:032x}"` (32-char suffix) exactly filling
   the 40-char hex portion of the Ethereum address. Earlier version used 33-char suffix causing
   the distinguishing digit to be truncated — all indices 0-15 produced identical addresses.

4. **Chain 6 (Mimicry) paradox**: Too-perfect regularity (CV = 0.005) is detectable because real
   agents show HIGH variance (CV = 1.87). Perfect mimicry is a detectable signal, not a perfect
   evasion — this supports the TC-as-canary insight from Phase 5 FINDING-01.

## Acceptance Criteria

- [x] All 8 attack chains injected, each with ≥5 instances
- [x] `data/attack_injection_dataset.parquet` exists with `is_injected` label column
- [x] 15 unit tests pass for behavioral signatures and address safety
- [x] `analysis/attack-injection-summary.md` documents injection methodology
- [x] Injection rate 6.07% ≤ 10% limit (verified against real 93K dataset)

---

_Plan 06-01 complete: 2026-04-05_
