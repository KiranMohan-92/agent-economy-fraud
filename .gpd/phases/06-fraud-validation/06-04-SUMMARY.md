---
plan: 06-04
title: arXiv Paper Draft
status: COMPLETE
completed: 2026-04-05
---

# Plan 06-04 Summary: arXiv Paper Draft

## What Was Done

Synthesized all Phase 1–6 research findings into a complete arXiv-ready paper draft.
Integrated theoretical framework (Phase 2), detection design (Phase 3), synthetic validation
(Phase 4), real-world characterization (Phase 5), and fraud injection/detection results
(Phase 6 Plans 06-01–06-03) into a unified 9-section academic paper.

## Deliverable

`paper/agent-economy-fraud-arxiv.md`

## Paper Structure

| Section | Content |
|---------|---------|
| §1 Abstract | 3-stage validation, key finding (7/8 chains), ROC-AUC 0.777, Chain 7 gap |
| §2 Introduction | Problem framing, agent economy context, research contributions |
| §3 Background | ERC-8004, OpenClaw, Moltbook, x402, human invariant survey |
| §4 Threat Model | 8 A2A attack chains with OpenClaw API mappings and difficulty tiers |
| §5 Detection Framework | 5 signals, AUC-proportional fusion weights, 4-tier decision system |
| §6 Evaluation | Phase 4 synthetic + Phase 5 real + Phase 6 injection; per-chain recall table |
| §7 Recommendations | P0–P3 banking recommendations across 0–36 month timeline |
| §8 Limitations & Future Work | Frontier limitations, testable predictions, next-gen architecture |
| §9 Conclusion | Hard-to-vary framing of pre-crime research value |
| Appendices | Signal specs, dataset summary, reproducibility commands |

## Key Paper Findings

1. **7/8 attack chains detectable** at 100% per-chain recall using the 5-signal framework
2. **Chain 6 paradox** — "too perfect" behavioral mimicry (CV≈0.005) is detectable because
   machine regularity is MORE anomalous than human variance (CV=1.87)
3. **Chain 7 collective detection gap** — per-address scoring structurally cannot detect
   swarm attacks; next-gen group-level detector architecture required
4. **Pre-crime research window** — 6–12 months before systematic exploitation based on
   historical fraud lag from comparable platform launches (DeFi, NFT, LLM agents)
5. **Testable prediction** — TC-canary signal (Friday 3–5pm spike) will degrade measurably
   within 18 months as agents proliferate; detectable with 3-period Chow test

## Validation Chain

The paper is supported by 3 independent validation stages:
- **Theoretical**: 9/9 invariants predicted violated → 7/9 confirmed in real Phase 5 data
- **Injection**: 7/8 chains detectable at 100% per-chain recall; 1 (Chain 7) requires collective detection
- **Adjacent domain**: All 8 chains have confirmed analogues (Telegram bots, ERC-4337, Virtuals Protocol)

---

_Plan 06-04 complete: 2026-04-05_
