# Numerical Consistency Audit — agent-economy-fraud

**Scope:** paper/*.tex, paper/agent-economy-fraud-arxiv.md, .gpd/STATE.md, .gpd/PROJECT.md,
.gpd/VERIFICATION-FINAL.md, .gpd/REFEREE-REPORT.md, data/validation_metrics.json,
data/fraud_detection_metrics.json, src/a2a_detection/signals/fusion.py, plus supporting
grep sweeps of appendix_dataset.tex, appendix_signals.tex, related_work.tex, recommendations.tex,
limitations.tex, background.tex, introduction.tex, conclusions.tex, threat_model.tex.

**Method:** every numeric claim was traced to its file:line, grouped by the underlying
real-world quantity it purports to measure, and cross-checked against the JSON/code that
generated it. A CONTRADICTION is two sources reporting a different value for the *same*
quantity on the *same* dataset/stage/threshold. LEGITIMATE means the values differ because
they describe different datasets, stages, or thresholds and the paper says so.

---

## 1. Number of ERC-8004 agents

| File:line | Value | Context/dataset |
|---|---|---|
| paper/abstract.tex:14 | 665 | Stage 2 real validation, positives |
| paper/introduction.tex:5 | 665 | "have executed over 81,000 USDC transactions" |
| paper/evaluation.tex:24, 117, 120 | 665 | Stage 2 dataset description + "2,134 scored addresses in the initial run" |
| paper/appendix_dataset.tex:9, 45, 49, 83 | 1,505 → 665 | 1,505 extracted from registry; reduced to 665 "due to addresses with insufficient transaction history" |
| paper/appendix_signals.tex:5 | 665 | "cleaned dataset (665 agents, 1,069 human counterparties)" |
| paper/threat_model.tex:204 | 665 | CV-threshold empirical justification, "ERC-8004 registered agents (n=665)" |
| paper/limitations.tex:9 | 665 | "positive class — 665 ERC-8004-registered agents" |
| paper/conclusions.tex:7 | 665 | "665 ERC-8004-registered agents" |
| .gpd/PROJECT.md:130, 151, 153, 189 | 665 | Phase 5 summary, "final" dataset |
| .gpd/DECISIONS.md:12 | 665 | D-08 decision record |
| **.gpd/STATE.md:41** | **548** | "Evaluated: 2,134 active addresses (548 agents, 1,586 counterparties)" — the *raw* Dune pull, dated 2026-04-03 |
| **.gpd/STATE.md:43** | **523/548** | "catches 523/548 known agents" (raw recall numerator/denominator) |
| **.gpd/STATE.md:63** | **548 → 665** | "Agent pool: 548 → 665 (Dune re-ingestion added 117 previously uncounted agents)" |
| **data/validation_metrics.json:8** (`baseline.n_positive`) | **548** | baseline/raw evaluation run |
| **data/validation_metrics.json:10** (`baseline.tp`) | **523** | baseline run true positives |
| data/validation_metrics.json:34 (`updated.n_positive`) | 665 | cleaned evaluation run |
| data/base_erc8004_agents.json:2 | 1505 | raw registry extraction, `"count": 1505` |
| data/overlap_results.json:3 | 1505 | `"total_population": 1505` |

**CONTRADICTION (load-bearing).** `evaluation.tex:120` states the Stage-2 pipeline is one
continuous cleaning process over a constant 665-agent positive class: "*The final evaluation
set comprises 1,734 addresses (665 agents + 1,069 cleaned humans) across 2,134 scored
addresses in the initial run.*" That sentence requires the 2,134-address "initial run" to
contain 665 agents (665 + 1,469 raw counterparties = 2,134). But `.gpd/STATE.md:41` and
`data/validation_metrics.json` (`baseline` block) show the actual 2,134-address raw run used
only **548** agent positives (548 + 1,586 = 2,134, verified: `523 tp + 25 fn = 548`, exactly
matching the paper's own raw recall of 95.4% at `evaluation.tex:123`). `.gpd/STATE.md:63`
explicitly states the agent pool grew from 548 → 665 via a **separate, later Dune
re-ingestion** — i.e., the "raw" and "cleaned" Stage-2 tables in the paper (`tab:real_results`)
are built from two different agent-registry snapshots pulled on different dates, not one
constant 665-agent set filtered two ways. The paper's raw-label recall/precision/F1 headline
(95.4% / 27.6% / 42.8%) is therefore computed against **548** agents while every prose
description of Stage 2 — including the sentence immediately describing that same table —
says **665**.

**Secondary narrative inconsistency.** `appendix_dataset.tex:49` gives a *different* causal
story for how 665 was reached ("reduction from 1,505 to 665 agents is due to addresses with
insufficient transaction history" — i.e., filtering **down**), while `.gpd/STATE.md:63` says
665 was reached by adding 117 previously-missed agents to a 548 base **(growing up)**. Both
cannot be the literal mechanism; at most one describes what actually happened to the reported
numbers.

---

## 2. Number of transactions

| File:line | Value | Context |
|---|---|---|
| paper/abstract.tex:14 | 81,904 | Stage 2 real transactions |
| paper/evaluation.tex:20 | 100,000 | Stage 1 synthetic addresses |
| paper/evaluation.tex:24, 117 | 81,904 | Stage 2 |
| paper/evaluation.tex:28, 191 | 93,579 real + 6,050 injected = 99,629 | Stage 3 |
| paper/appendix_dataset.tex:19-20 | 81,904 | "raw result comprised 81,904 transaction rows" |
| paper/appendix_reproducibility.tex:81 | 81,904 | code comment, `load_transactions()` |
| paper/detection_framework.tex:78, 277, 399 | 81,904 | fusion weight derivation, package validation |
| .gpd/PROJECT.md:130, 150 | 81,904 | Phase 5 |
| .gpd/PROJECT.md:131 | 93,579 real + 6,050 injected | Phase 6 |
| .gpd/STATE.md:40 | 81,904 | Phase 5 dataset |
| .gpd/STATE.md:20 | 6,050 injected into 93,579 | Phase 6 |
| .gpd/VERIFICATION-FINAL.md:100, 114 | 81,904 / 99,629 | cross-phase trajectory |
| .gpd/REFEREE-REPORT.md:17, 109 | 81,904 / 93,579 / 100,000 | flags exactly this three-way spread as a readability problem |

**LEGITIMATE.** All three counts (100,000 / 81,904 / 93,579+6,050=99,629) are consistently
used for three genuinely different datasets (synthetic / real / real+injected), and
`evaluation.tex:42-48` (Figure 1 caption) explicitly reconciles them. No numeric contradiction
found here — this was already flagged by the referee as a *presentation* clarity issue, not
an arithmetic one, and the June-2026 revision added the explanatory figure caption to address
it.

---

## 3. Per-signal ROC-AUC — CRITICAL

| File:line | NT | TC | ER | VF | Source/date |
|---|---|---|---|---|---|
| paper/evaluation.tex:143, 153-157 (`tab:signal_auc`) | 0.5990 | 0.4647 | 0.5152 | 0.5220 | "Stage 2 cleaned evaluation set" |
| paper/appendix_signals.tex:80, 111, 149, 39 | 0.5990 | 0.4647 | 0.5152 | 0.5220 | Phase 5 performance, per-signal sections |
| paper/appendix_signals.tex:183-189 (`tab:weight-evolution`) | 0.5990 | 0.4647 | 0.5152 | 0.5220 | Phase 5 AUC column |
| paper/limitations.tex:25, 29 | 0.599 (NT) / 0.5683→0.4647 (TC) | — | — | — | "AUC drops from 0.5683 to 0.4647" (TC, pre/post cleaning) |
| paper/recommendations.tex:35-36, 110 | 0.5990 (NT), 0.5152 (ER) | — | — | — | priority rationale |
| data/validation_metrics.json:47-51 (`per_signal_aucs`) | 0.599 | 0.4647 | 0.5152 | 0.522 | matches paper exactly |
| .gpd/STATE.md:58-61 | 0.5990 | 0.4647 | 0.5152 | 0.5220 | "live run, 2026-04-04" |
| **src/a2a_detection/signals/fusion.py:12-16 (docstring)** | **0.6214** | **0.5683** | **0.5497** | **0.5290** | "Signal weights (updated 2026-04-04, AUC-proportional)" |
| **src/a2a_detection/signals/fusion.py:73-76 (comment)** | **0.6214** | **0.5683** | **0.5497** | **0.5290** | "AUC values measured: network_topology=0.6214, temporal_consistency=0.5683, economic_rationality=0.5497, value_flow=0.5290 (sum=2.2684)" |

**CONTRADICTION (the critical one named in the task).** The paper (all `.tex` files),
`STATE.md`, and `validation_metrics.json` unanimously report per-signal AUCs of
NT=0.599, TC=0.4647, ER=0.5152, VF=0.522 (sum ≈ 2.1009). The shipped source code's own
docstring and inline comment — dated the *same day*, 2026-04-04 — assert a different set:
NT=0.6214, TC=0.5683, ER=0.5497, VF=0.5290 (sum = 2.2684). These are not rounding artifacts;
`limitations.tex:29` independently corroborates the paper's TC value by noting it "drops from
0.5683 to 0.4647" — meaning **0.5683 is the paper's own *pre-cleaning* TC AUC**, while
fusion.py cites 0.5683 as the *current* value backing today's weights. This strongly suggests
fusion.py's comment was never updated after the Phase-5 label-cleaning re-run: it still
reflects the pre-cleaning (or an intermediate) AUC measurement, while the paper and
`validation_metrics.json` reflect the final cleaned-label run.

**Compounding arithmetic problem.** The weight vector actually shipped in
`fusion.py:81-87` (0.2739 / 0.2505 / 0.2424 / 0.2332) is mathematically exact when derived
from fusion.py's *own* stated AUCs (0.6214/2.2684 = 0.2739, 0.5683/2.2684 = 0.2505, etc.),
**not** from the paper's published AUCs. If the weights were instead computed
"AUC-proportional" from the paper's own published per-signal AUCs (0.599, 0.4647, 0.5152,
0.522; sum 2.1009), the result would be NT=0.2851, TC=0.2212, ER=0.2453, VF=0.2485 — visibly
different from the 0.2739/0.2505/0.2424/0.2332 vector the paper claims is "AUC-proportional"
(`detection_framework.tex:280-287`, `evaluation.tex:271`). In other words, the paper's stated
derivation method does not reproduce the paper's own stated weights when applied to the
paper's own stated AUCs — the weights only reconcile against the AUC set living in the code
comment, which never made it into the manuscript.

---

## 4. Composite / overall ROC-AUC

| File:line | Value | Dataset/stage |
|---|---|---|
| paper/evaluation.tex:102-104, 109 (`tab:synthetic_results`) | 0.97 | Stage 1 synthetic |
| paper/evaluation.tex:137 (`tab:real_results`) | 0.515 | Stage 2 cleaned labels |
| paper/evaluation.tex:183, 220, 288 | 0.515 / 0.777 | Stage 2 cleaned / Stage 3 mixed |
| paper/agent-economy-fraud-arxiv.md:116 | "not reported" (raw) / — | raw labels column explicitly blank |
| paper/limitations.tex — (implicit via 0.599 best single-signal) | — | — |
| data/validation_metrics.json:6 (`baseline.roc_auc`) | **0.59** | raw/548-agent baseline run — **never surfaced in any paper file** |
| data/validation_metrics.json:32 (`updated.roc_auc`) | 0.5147 → reported as 0.515 | cleaned run, matches paper |
| data/fraud_detection_metrics.json:14, 86 | 0.7771 → reported as 0.777 | Stage 3 mixed corpus |
| .gpd/VERIFICATION-FINAL.md:104, 117 | 0.515 / 0.777 | cross-phase trajectory |

**LEGITIMATE split with one flag.** 0.97 / 0.515 / 0.777 are three different stages and are
consistently reported everywhere they appear. **Flag (not a hard contradiction):** the raw
(548-agent) Stage-2 run has a composite ROC-AUC of **0.59** sitting in
`validation_metrics.json:6`, which is *higher* than the 0.515 the paper prints as its
headline "composite ROC-AUC" — but the paper only ever reports the cleaned-label 0.515 and
explicitly marks the raw column "not reported" (`agent-economy-fraud-arxiv.md:116`). This is
technically true (it is not reported) but it means a more favorable, actually-computed AUC
value was available and omitted in favor of the weaker one, which is the opposite of the
usual cherry-picking direction and worth a footnote given the referee report's concern
(`.gpd/REFEREE-REPORT.md:49`) that the paper "downplays" the weak AUC — here there was in
fact a stronger, unreported number sitting in the data.

---

## 5. Recall

| File:line | Value | Threshold/dataset |
|---|---|---|
| paper/evaluation.tex:89, 100 (`tab:synthetic_results`) | 96.23% | Stage 1 synthetic |
| paper/evaluation.tex:123, 135 (`tab:real_results`, raw) | 95.4% | Stage 2, raw labels, θ=0.08 |
| paper/evaluation.tex:123, 135 (`tab:real_results`, cleaned) | 81.1% | Stage 2, cleaned labels, θ=0.09 |
| paper/evaluation.tex:173, 181 (`tab:transfer_gap`) | 61.4% | Stage 2, raw labels, **fixed** synthetic θ=0.24 |
| paper/evaluation.tex:231 (`tab:stage3_tradeoff`) | 32.9% (θ=0.09) / 7.3% (θ=0.29) | Stage 3 aggregate (NOT per-chain) |
| data/validation_metrics.json:4 (`baseline.recall`) | 0.9544 → 95.4% | matches paper raw |
| data/validation_metrics.json:26 (`updated.recall`) | 0.8105 → 81.1% | matches paper cleaned |
| data/fraud_detection_metrics.json:11 (`primary_threshold.recall`) | 0.3293 → 32.9% | θ=0.09 aggregate, matches paper |
| data/fraud_detection_metrics.json:82 (`operating_point.recall`) | 0.0732 → 7.3% | θ=0.29 aggregate, matches paper |
| .gpd/STATE.md:43 | 95.4% (523/548) | raw, but denominator is 548 not 665 (see §1) |

**LEGITIMATE**, given each figure is tied to an explicit threshold/label-set the paper names,
**except** that the 95.4%/61.4% figures inherit the §1 agent-count contradiction (548 vs 665
denominator).

Note: 100% per-chain recall (7/8 chains) is a **different, non-comparable** quantity from the
32.9%/7.3% aggregate recall figures above — `evaluation.tex:238` explicitly warns that 5 of 8
chains have only 1 injected address each, so "100% recall" there means "1/1", not a
population-level rate. The paper is internally careful about this distinction
(`evaluation.tex:238`); no contradiction, but it is easy to misread the two recall families as
comparable, which the referee-style audit should flag as a readability risk.

---

## 6. Precision

| File:line | Value | Dataset |
|---|---|---|
| paper/evaluation.tex:89, 99 | 82.36% | Stage 1 synthetic |
| paper/evaluation.tex:123, 134 | 27.6% | Stage 2 raw |
| paper/evaluation.tex:123, 134 | 42.9% | Stage 2 cleaned |
| paper/evaluation.tex:175 (`tab:transfer_gap`) | 52.1% (θ=0.24) / 27.6% (θ=0.08) | Stage 2 raw, two thresholds |
| paper/limitations.tex:11 | "60–80% range" (estimated, not measured) | hypothetical clean-EOA precision |
| data/validation_metrics.json:3 | 0.2757 → 27.6% | matches |
| data/validation_metrics.json:25 | 0.42879... → 42.9% | matches |
| data/fraud_detection_metrics.json:11 | 0.0164 → 1.6% | Stage 3 aggregate, matches `evaluation.tex:233` |

**LEGITIMATE.** No contradiction — each value is tied to a named dataset/threshold and
matches its JSON source exactly, including the 52.1% transfer-gap-table entry, which is
distinct from but consistent with (not contradicting) the 27.6% headline since they are
different thresholds (0.24 vs 0.08) on the same raw set.

---

## 7. Fusion threshold

| File:line | Value | Role |
|---|---|---|
| paper/evaluation.tex:123, 162, 166, 171 | 0.24 | synthetic-calibrated threshold (fixed, for transfer-gap test) |
| paper/evaluation.tex:123, 166, 171 | 0.08 | raw-label re-optimized threshold |
| paper/evaluation.tex:123, 198, 217, 220, 229 | 0.09 | cleaned-label / Stage 3 per-chain operating threshold |
| paper/detection_framework.tex:358, 369-370 | 0.09 | ALLOW/FLAG decision-tier boundary |
| paper/evaluation.tex:220, 229 | 0.29 | Stage 3 FPR≤5%-constrained operating point |
| src/a2a_detection/signals/fusion.py:89-92 | 0.09 | `THRESHOLD_FLAG`, "0.09 optimal on real Dune data (2026-04-04)... Previous 0.08 was the initial real-data optimum" |
| data/validation_metrics.json:14 (`baseline.threshold`) | 0.08 | raw/548-agent run |
| data/validation_metrics.json:36 (`updated.threshold`) | 0.09 | cleaned/665-agent run |
| data/fraud_detection_metrics.json:3, 75 | 0.09 / 0.29 | Stage 3 primary/operating-point thresholds |
| appendix_signals.tex:108 | "0.24 (Phase 4) to 0.08 (Phase 5)" | matches evolution described in fusion.py |

**LEGITIMATE.** All four threshold values (0.24 / 0.08 / 0.09 / 0.29) are distinct, named
operating points, and every file that cites one ties it to the same stage/purpose as every
other file. This is the one quantity in the audit with zero contradictions across all seven
sources checked.

---

## 8. Fusion weights

| File:line | NT | TC | ER | VF | CP | Context |
|---|---|---|---|---|---|---|
| paper/detection_framework.tex:280-287 (Eq. fusion) | 0.2739 | 0.2505 | 0.2424 | 0.2332 | 0.0000 | current/published |
| paper/evaluation.tex:271 (Eq. signal_weights) | 0.2739 | 0.2505 | 0.2424 | 0.2332 | 0.00 | current/published |
| paper/agent-economy-fraud-arxiv.md:88 | 0.2739 | 0.2505 | 0.2424 | 0.2332 | 0.0000 | current/published |
| src/a2a_detection/signals/fusion.py:82-86 (`DEFAULT_WEIGHTS`) | 0.2739 | 0.2505 | 0.2424 | 0.2332 | 0.00 | matches paper exactly |
| data/validation_metrics.json:39-44 (`updated.weights`) | 0.2739 | 0.2505 | 0.2424 | 0.2332 | — | matches paper exactly |
| data/validation_metrics.json:15-20 (`baseline.weights`) | 0.25 | 0.2 | 0.3 | 0.25 | — | **superseded 2026-04-03 weights**, correctly labeled "baseline"/not current anywhere |
| paper/appendix_signals.tex:183-189 | "0.20" (Phase 3-4, uniform) → "AUC-prop." (Phase 5) | | | | | evolution table, qualitative only, no numeric clash |
| src/a2a_detection/signals/fusion.py:78 (comment) | "Previous weights (2026-04-03): econ=0.30, topo=0.25, flow=0.25, temp=0.20" | | | | | matches `baseline.weights` in JSON exactly |

**LEGITIMATE for the weight *values* themselves** — paper, fusion.py, and the JSON `updated`
block all agree on 0.2739/0.2505/0.2424/0.2332, and the superseded 0.30/0.25/0.25/0.20 set is
consistently labeled as historical everywhere it appears, never presented as current. **The
problem is not the weight numbers — it is that the weights' stated *justification* (AUC
values) contradicts the paper's own published AUC table, per §3 above.**

---

## 9. Test count

| File:line | Value |
|---|---|
| paper/detection_framework.tex:396 | 47 tests |
| paper/appendix_reproducibility.tex:69 | 47 tests ("All 47 tests should pass") |
| paper/agent-economy-fraud-arxiv.md:91 | 47 tests |
| **.gpd/PROJECT.md:152** | **32 unit tests** |
| `pytest --collect-only` (verified live, 2026-07-09) | **47 tests collected** |

**CONTRADICTION (minor, easily fixed).** `.gpd/PROJECT.md:152` says "32 unit tests"; the
paper says 47 in three places, and running the actual test suite
(`src/a2a_detection/tests/test_attack_injection.py` + `test_signals.py`) collects exactly 47
tests. The paper and the code agree; `.gpd/PROJECT.md` is stale (likely predates the addition
of `test_attack_injection.py`'s 15 Phase-6 tests, since `.gpd/ROADMAP.md:147` separately notes
"15 tests pass" for that file, and 32 + 15 = 47 — consistent with PROJECT.md simply never
being updated after the Phase 6 test file was added).

---

## 10. Attack chain difficulty labels

| File:line | Labels used |
|---|---|
| paper/threat_model.tex:41-61 (`tab:attack_chains`) | Easy / Medium / Medium / Hard / Out-of-scope* / Out-of-scope* / Out-of-scope† / Out-of-scope* |
| paper/evaluation.tex:194, 204-211 (`tab:attack_chain_recall`) | EASY / MEDIUM / MEDIUM / HARD / OOS* / OOS* / OOS† / OOS* |
| paper/agent-economy-fraud-arxiv.md:62-69, 126-133 | Easy / Medium / Medium / Hard / "Out of scope for human-assumption detectors" (×3) / "Out of scope for per-address scoring" (Chain 7) |
| data/fraud_detection_metrics.json:17-138 | EASY / MEDIUM / MEDIUM / HARD / **IMPOSSIBLE** ×4 (Chains 5,6,7,8 all labeled "IMPOSSIBLE", no OOS*/OOS† distinction) |

**LEGITIMATE (terminology mapping, not a value contradiction), with one clarity gap worth
flagging.** The paper subdivides its "out of scope" tier into two flavors — OOS*
(human-assumption detectors) for Chains 5/6/8 and OOS† (per-address scoring) for Chain 7 —
while the underlying `data/fraud_detection_metrics.json` uses a single flat `"IMPOSSIBLE"`
difficulty string for all four of those chains, with no field distinguishing the */†
subtypes. The mapping is consistent (every chain the paper calls OOS*-or-OOS† is exactly the
set the JSON calls IMPOSSIBLE, and vice versa), so there is no numeric contradiction, but the
finer-grained OOS*/OOS† distinction that carries real evaluative weight in the paper (Chain 7
is a structural/architectural gap; Chains 5/6/8 are "merely" outside current human-assumption
baselines but *are* detected) does not exist as a queryable field anywhere in the data layer —
it is a manuscript-only overlay on top of a coarser code-level label.

---

## Summary Table: Contradiction vs Legitimate

| # | Quantity | Verdict | Severity |
|---|---|---|---|
| 1 | ERC-8004 agent count (665 vs 548/523) | **CONTRADICTION** | High — undermines Stage-2 headline recall provenance |
| 1b | 665-derivation narrative (filter-down 1,505→665 vs. grow-up 548→665) | **CONTRADICTION** | Medium — two mutually exclusive methodology stories |
| 2 | Transaction counts (100,000 / 81,904 / 93,579+6,050) | LEGITIMATE | — (readability issue only, already flagged by referee) |
| 3 | Per-signal AUCs (fusion.py vs. paper/validation_metrics.json) | **CONTRADICTION** | Critical — stale code comment, and the weight-derivation math only reconciles against the comment's numbers, not the paper's |
| 4 | Composite ROC-AUC (0.97/0.515/0.777) | LEGITIMATE | — (flag: unreported 0.59 raw AUC exceeds reported 0.515 cleaned AUC) |
| 5 | Recall (96.23/95.4/81.1/61.4/32.9/7.3%) | LEGITIMATE | — (inherits agent-count issue from #1) |
| 6 | Precision (82.36/27.6/42.9/52.1/1.6%) | LEGITIMATE | — |
| 7 | Fusion threshold (0.24/0.08/0.09/0.29) | LEGITIMATE | — (cleanest quantity in the audit) |
| 8 | Fusion weights | LEGITIMATE (values) / see #3 for justification issue | — |
| 9 | Test count (47 vs 32) | **CONTRADICTION** | Low — stale `.gpd/PROJECT.md`, code and paper agree at 47 |
| 10 | Attack chain difficulty labels | LEGITIMATE | — (terminology granularity gap, not a value clash) |

**Total true contradictions found: 4** (agent count 665-vs-548, the 665-derivation narrative
clash, per-signal AUC fusion.py-vs-paper, and test count 47-vs-32 in PROJECT.md).
