---
reviewed: 2026-06-27T00:00:00Z
scope: revision_review
round: 2
previous_report: GPD/REFEREE-REPORT.md
recommendation: minor_revision
confidence: high
issues_resolved: 7
issues_partially_resolved: 0
issues_unresolved: 0
new_issues: 3
---

# Referee Report — Round 2

**Paper:** Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection
**Manuscript root:** `/mnt/c/Users/kiran/myprojects/agent-economy-fraud/paper/`
**Previous report:** `GPD/REFEREE-REPORT.md` (recommendation: Minor Revision, April 2026)
**Mode:** Direct revision re-review (staged panel artifacts not expected for this invocation)
**Round:** 2 of 3 maximum
**Target venue:** arXiv cs.CR preprint

## Summary of Revision Assessment

This is a strong revision. The June-2026 refresh is, on the whole, an exercise in
disciplined down-scoping rather than promotion: the authors narrowed the novelty claim,
replaced the "no documented A2A fraud / 6--12 month pre-crime window" framing with a
careful agent-as-victim vs. agent-as-fraudster distinction grounded in two documented
2026 incidents, added a Stage-3 threshold trade-off table that openly shows that high
per-chain recall and a deployable false-positive rate are *not* simultaneously achievable,
and reconciled scale/ecosystem numbers against the broader agent economy. I independently
verified the four focus changes against the committed data (`data/fraud_detection_metrics.json`,
`data/validation_metrics.json`) and the bibliography (`references.bib`). **All four focus
changes are sound.** The new Stage-3 trade-off numbers reproduce the committed metrics
exactly, the new citations are real and correctly identified, and the incident framing is
logically clean and internally consistent across abstract, related work, limitations, and
conclusions.

Three defects were introduced or left standing by the revision, all of them local and
fixable without new experiments. The most important is a **numerical miscount in the new
Stage-3 sample-size caveat** (it says "six of the eight chains" have a single injected
address and omits Chain 8's seven addresses; the data show *five* single-address chains).
The other two are labeling/disambiguation issues around the real-data recall headline
(95.4% is a raw, contaminated-label number; the abstract and introduction do not tag it as
such, although the conclusions section does). None of these rise to the level of an
unsupported central claim, and the honest numbers are already present in the manuscript's
own tables. The revision did not introduce any new overclaim; if anything it removed
several. I recommend **minor revision**.

## Recommendation

**MINOR REVISION**

The seven changes mandated by the round-1 report are all resolved, and the additional
voluntary edits (novelty narrowing, incident framing, Stage-3 trade-off table, ecosystem
contextualization) materially improved the manuscript's intellectual honesty. What remains
is a small set of local fixes: one introduced numerical miscount, one carried-over
table-caption/threshold mismatch, and one cross-section labeling inconsistency about
whether the 95.4% recall headline is on raw or cleaned labels. Because the corrected
numbers already appear in the manuscript's tables and conclusions, these are clarification
and bookkeeping fixes, not a narrowing of any central scientific claim — which is exactly
the profile that justifies minor rather than major revision.

## Confirmation of the Four Focus Changes

### Focus Change 1 — Novelty narrowing and the new "Agentic Commerce Security" subsection: SOUND

`related_work.tex` adds `\subsection{Agentic Commerce Security}` citing `zhang2026sok`
(SoK: Blockchain Agent-to-Agent Payments, arXiv:2604.03733), `mao2026sok` (SoK: Security of
Autonomous LLM Agents in Agentic Commerce, arXiv:2604.15367), and `li2026a402`
(A402, arXiv:2603.01179). I confirmed all three keys resolve in `references.bib` with full
author lists and matching eprint IDs — these are real entries, not stubs.

The differentiation paragraph was narrowed from an absolute "no prior work combines..." to:
*"this is the only work that pairs a behavioral-invariant account of detection failure with
empirical on-chain detection metrics on real agent transactions."* This narrowed claim is
**defensible** given the cited competitors: zhang2026sok and mao2026sok are systematization
papers (lifecycle taxonomies, cross-layer attack enumerations, layered defense
architectures) with no empirical on-chain detection measurement, and li2026a402 is a
*prevention*-side protocol (TEE-assisted atomic service channels), not a detector. The text
correctly characterizes each: "these works taxonomize the threat and protocol surface, but
neither measures whether agent activity is distinguishable on real transaction data." The
concrete overlap mapping (mao's *market manipulation* ~ Chain 8, *inter-agent trust* ~
Chain 4/Chain 5) is appropriately specific rather than hand-waving, and the A402 framing as
a *non-competing, complementary* prevention layer is fair. The claim retains a "To our
knowledge" hedge. No overclaim. **Confirmed sound.**

### Focus Change 2 — "Threat-Model Validity" rewrite (agent-as-victim vs. agent-as-fraudster): SOUND

`limitations.tex` §"Threat-Model Validity: From Pre-Crime to Early Documented Crime"
replaces the old undocumented-fraud claim with a precise distinction. It acknowledges the
documented May-2026 prompt-injection drain of ~\$150K--\$200K from an agent-controlled wallet
on Base (`grokbankr2026`) and DataDome's 16.4M spoofed agent requests over a two-month
window (`datadome2026`), then distinguishes both as out-of-scope for the paper's specific
model: the Base incident is *agent-as-victim* (external prompt injection capturing one
agent's wallet — squarely in the Greshake indirect-prompt-injection thread), and the
DataDome figures are *Web2 HTTP-layer* impersonation, "adjacent to but not identical with
our on-chain payment model."

The logic is clean and non-contradictory: the section claims only that these incidents
"corroborate the underlying invariant-failure mechanism (I2, I5, I6) without validating our
detection framework against an in-scope incident," and flags "a confirmed in-scope
A2A-commerce fraud case as the decisive future falsification test." This is the correct
epistemic posture — it does not claim the incidents validate the framework, and it does not
claim A2A fraud is still entirely undocumented. The same distinction is mirrored
consistently in the abstract (closing sentence), `related_work.tex` (AI Agent Security
subsection), and `conclusions.tex`. The bib notes match the prose (grokbankr \$150K--200K,
2026-05-04; DataDome 16.4M spoofed, Jan--Feb 2026). The only soft spot is the mapping of a
prompt-injection wallet drain onto invariants I2/I5/I6 (biometric/device/identity), which is
a defensible-but-loose association; it is not load-bearing and does not need to change.
**Confirmed sound, logically clean, no overclaim.**

### Focus Change 3 — Stage-3 honesty fix (`tab:stage3_tradeoff`): SOUND, with one introduced miscount

I reproduced every number in the new `tab:stage3_tradeoff` against
`data/fraud_detection_metrics.json`:

| Quantity | Paper | Data file | Match |
|---|---|---|---|
| θ=0.09 injected recall | 32.9% | 0.3293 | ✓ |
| θ=0.09 FPR | 21.8% | 0.2179 | ✓ |
| θ=0.09 precision | 1.6% | 0.0164 | ✓ |
| θ=0.29 injected recall | 7.3% | 0.0732 | ✓ |
| θ=0.29 FPR | 3.8% | 0.0381 | ✓ |
| ROC-AUC (mixed corpus) | 0.777 | 0.7771 | ✓ |

The surrounding text ("high per-chain recall and a low false-positive rate are *not*
simultaneously achievable here"; "no single threshold delivers both high recall and a
deployable false-positive rate") is internally consistent with the table and with the data,
and it correctly defuses the apparent tension between "7/8 chains at 100% recall" and a
deployable operating point. This is a genuine, well-executed honesty improvement, and the
paper no longer juxtaposes incompatible thresholds misleadingly in the body. **The
mechanism of the fix is sound.**

However, the new sample-size caveat that accompanies the table contains an **introduced
numerical error** (see Issue REF-R2-001 below): it states "six of the eight chains are
represented by a single injected attack address each (Chain 4 by 15 and Chain 7 by 55)."
The committed data show single-address chains are 1, 2, 3, 5, 6 = **five**, while Chain 8
has **seven** addresses (omitted from the parenthetical). This is a miscount inside the very
paragraph added for honesty and should be corrected.

### Focus Change 4 — Scale/ecosystem updates and AUC reconciliation: SOUND

- `introduction.tex` contextualizes the 665-agent / 81,904-transaction Base slice against
  ~176M ecosystem transactions (`usdcagentpayments2026`, "98.6% in USDC" — matches the bib
  title) and x402 100M+ payments (`chainalysis2026x402`). Agent counts are consistent across
  abstract, introduction, evaluation, and conclusions (665 agents; 81,904 transactions).
- The ERC-8004 mainnet date (2026-01-29) is footnoted in `background.tex`, and the footnote
  cleanly resolves the Jan-2025 data anachronism: the January-2025 window start "reflects the
  *full* USDC history of addresses that later registered under ERC-8004, not their
  registration dates." `evaluation.tex` ("spanning January 2025 through April 2026") is
  consistent with this footnote. Good.
- x402/AP2 payment rails are added as a new `background.tex` paragraph; the x402 100M+ figure
  is consistent between background and introduction.
- `limitations.tex` now states "best single-signal AUC of 0.599 (Network Topology)," which
  matches `tab:signal_auc` (NT = 0.5990) and `validation_metrics.json` (0.599). The earlier
  round's risk of a stray AUC value here is resolved.

No new internal numerical contradiction in agent counts, AUC values, or ecosystem figures.
**Confirmed sound.**

## Issue Resolution Tracker (Round-1 Required Changes)

| ID | Round-1 Required Change | Status | Evidence |
|----|-------------------------|--------|----------|
| REF-001 | Report ROC-AUC 0.515 prominently in abstract/intro | resolved | Abstract reports "composite ROC-AUC is 0.515 on cleaned labels"; intro contribution 4 repeats it and calls it a "central limitation" |
| REF-002 | Add fixed-threshold transfer-gap analysis | resolved | `tab:transfer_gap` reports both θ=0.24 (fixed) and θ=0.08; see Issue REF-R2-002 for a residual labeling defect |
| REF-003 | Justify CV=0.05 boundary empirically | resolved | `threat_model.tex` §"Empirical justification of the CV=0.05 threshold" gives per-population CV distributions, the 0.19% FPR, and the natural-gap argument |
| REF-004 | Correct/reframe velocity amplification factor | resolved | `threat_model.tex` Eq. (velocity_amp) now uses peak-to-peak (450×), reports avg-to-avg (~2,143×), and explicitly disowns the 10^6 apples-to-oranges figure |
| REF-005 | Add adversarial-ML and Web2 bot-detection related work | resolved | New subsections "Adversarial ML for Transaction Monitoring" and "Web2 Bot Detection" with specific citations |
| REF-006 | Add data-flow diagram reconciling 81,904 / 93,579 / 100,000 | resolved | `fig:dataflow` (TikZ three-stage pipeline) with the three counts explicitly reconciled in its caption |
| REF-007 | Acknowledge AUC-proportional weighting is effectively uniform | resolved | `evaluation.tex` §"Signal Weight Distribution" notes σ_w = 0.015 near-uniform spread |

All seven round-1 items are resolved.

## New / Residual Issues Introduced or Left by the Revision

### Issue REF-R2-001: Stage-3 sample-size caveat miscounts single-address chains

**Dimension:** correctness (internal numerical consistency)
**Severity:** Minor (does not change any conclusion; appears in a caveat)
**Status:** new-issue (introduced by the Focus-Change-3 honesty paragraph)
**Location:** `paper/evaluation.tex`, paragraph following `tab:stage3_tradeoff` (the
"further caveat bounds the per-chain figures" sentence).

**Quoted claim:** "six of the eight chains are represented by a single injected attack
address each (Chain~4 by 15 and Chain~7 by 55), so the 100\% per-chain recall entries are
separability indicators over few samples..."

**Description:** Per `data/fraud_detection_metrics.json` (`per_chain.instances_scored`):
CHAIN_1=1, CHAIN_2=1, CHAIN_3=1, CHAIN_4=15, CHAIN_5=1, CHAIN_6=1, CHAIN_7=55, CHAIN_8=7.
The single-address chains are 1, 2, 3, 5, 6 — that is **five**, not six. Chain 8 is
represented by **seven** addresses and is silently dropped from the parenthetical list of
multi-address chains. (The total, 5×1 + 15 + 55 + 7 = 82, matches the stated 82 attack
addresses, so the error is purely in the prose breakdown.)

**Impact:** Self-contradiction inside the paragraph added specifically to bolster honesty.
A careful reader cross-checking against the released data will catch it, which undercuts the
section's credibility precisely where it is trying to earn trust.

**Suggested fix:** Replace with: "five of the eight chains are represented by a single
injected attack address each (Chain~4 by 15, Chain~8 by 7, and Chain~7 by 55)."

### Issue REF-R2-002: `tab:transfer_gap` is captioned "cleaned labels" but its θ=0.08 column reproduces raw-label metrics, and the stated threshold conflicts with the data

**Dimension:** correctness / clarity (real-data results bookkeeping)
**Severity:** Minor-to-moderate (numbers are real; the defect is mislabeling, not a wrong result)
**Status:** carried-over from round 1 (the table was added to satisfy REF-002), now more
load-bearing because the abstract was reframed around these numbers.
**Location:** `paper/evaluation.tex`, `tab:transfer_gap` (caption and θ=0.08 column) and the
adjacent "re-optimized from the synthetic-calibrated value of 0.24 to 0.08" sentence.

**Description:** `tab:transfer_gap` is captioned "...on real on-chain data (cleaned
labels)." Its θ=0.08 column reads Recall 95.4% / Precision 27.6% / F1 42.8%. Those three
values are exactly the **raw** (uncleaned) results in `validation_metrics.json`
(`baseline`: recall 0.9544, precision 0.2757, f1 0.4278, `label_cleaning: "none"`,
`threshold: 0.08`). The actual **cleaned** re-optimized point in the data
(`updated`: `label_cleaning: "min_5_txs"`, `threshold: 0.09`) is recall 0.8105 /
precision 0.4288 / F1 0.5609 — i.e., recall 81.1%, not 95.4%. So (a) the θ=0.08 column is
raw-label data mislabeled as cleaned, and (b) the cleaned set's threshold is 0.09 in the
data, not 0.08 as the text states. `tab:real_results` already correctly lists 95.4% under
"Raw Labels" and 81.1% under "Cleaned Labels," so `tab:transfer_gap` contradicts the table
two paragraphs above it.

**Impact:** Across the real-data results the reader cannot tell whether the headline 95.4%
recall is a raw or cleaned figure, because the manuscript labels it both ways. The
underlying science is unaffected (every number is genuine and present in the data), but the
raw/cleaned provenance of the central empirical headline is currently ambiguous.

**Suggested fix:** Either (i) relabel the `tab:transfer_gap` caption to "raw labels" if both
columns are computed on the raw set at a fixed vs. re-optimized threshold, or (ii) recompute
the θ-sweep on the cleaned set and report the cleaned re-optimized point (recall 81.1% at
θ=0.09). In both cases, reconcile the "0.24 to 0.08" sentence with the data's 0.09 cleaned
threshold, and make the θ=0.24 column's label set explicit.

### Issue REF-R2-003: Abstract and introduction do not tag the 95.4% recall headline as a raw / contaminated-label number, while the conclusions section does

**Dimension:** clarity / presentation honesty
**Severity:** Minor (the conclusions already model the correct phrasing)
**Status:** carried-over; the round-2 abstract reframe leans on 95.4% without the raw tag.
**Location:** `paper/abstract.tex` ("recall of 95.4% only after threshold re-optimization");
`paper/introduction.tex` contribution 4 ("95.4% only after re-optimization"). Contrast with
`paper/conclusions.tex`, which correctly writes "95.4% recall on the raw evaluation set
(81.1% after label cleaning)."

**Description:** The 95.4% figure is the raw-label, contaminated-negative result; the
cleaned-label re-optimized recall is 81.1%. The abstract does say the real-data figures
reflect "a noisy-label operating point, not mature ranking performance," which is a partial
acknowledgment, but it never states that 95.4% specifically is the *raw*-label number while
0.515 AUC and the more conservative recall are the *cleaned*-label numbers. The conclusions
section gets this exactly right, so the manuscript is internally inconsistent in how it
presents its own central number.

**Impact:** A reader of the abstract/intro alone will take 95.4% as the framework's
real-data recall without realizing it is measured against a negative class the paper itself
describes as contaminated. This is the same selective-favorability pattern the round-1
report flagged (REF-001/4.1); the AUC was surfaced, but the recall headline still lacks its
raw-label qualifier.

**Suggested fix:** In the abstract and introduction, mirror the conclusions phrasing:
"95.4% recall on the raw (contaminated-negative) evaluation set, 81.1% after label
cleaning, at a re-optimized threshold." One clause each; no new analysis required.

## Detailed Evaluation (revision-scoped)

Only dimensions touched by the revision were re-evaluated; unchanged dimensions assessed
satisfactory in round 1 were not re-litigated.

### Novelty: ADEQUATE (improved)
The narrowed differentiation claim (Focus Change 1) is now proportionate to the evidence and
correctly positioned against the concurrent SoK literature. The contribution is a
detection-side empirical complement, honestly framed as such. No residual novelty overclaim.

### Correctness: MOSTLY CORRECT (one introduced miscount)
All Stage-3 trade-off numbers and the per-signal AUCs reproduce the committed data exactly.
The single introduced error is the five-vs-six single-address-chain miscount (REF-R2-001).
The transfer-gap table raw/cleaned labeling (REF-R2-002) is a provenance-labeling defect
rather than a wrong computation.

### Clarity: GOOD (one cross-section inconsistency)
The new data-flow figure and the Stage-3 trade-off narrative substantially improve
navigability. The residual clarity problem is the raw-vs-cleaned 95.4% inconsistency between
abstract/intro and conclusions (REF-R2-003), plus the transfer-gap caption.

### Completeness: MOSTLY COMPLETE
The Stage-3 trade-off table and the n-per-chain caveat close the most important round-1
completeness gap (the cherry-picked-threshold concern, round-1 §4.1/§4.2). The self-
validation caveat for injected attacks is now explicit ("separability indicators over few
samples rather than population recall estimates").

### Significance: MEDIUM
Unchanged from round 1 and unaffected by the revision. The conceptual taxonomy and the
behavioral-mimicry-paradox result remain the durable contributions; the empirical detection
result is honestly presented as a first-generation prototype with a near-chance real-data
AUC.

### Literature Context: ADEQUATE-to-THOROUGH (improved)
The new Agentic Commerce Security subsection and the documented-incident citations close the
round-1 related-work gaps and correctly situate the work against concurrent 2026 SoKs and
prevention protocols.

### Reproducibility: MOSTLY REPRODUCIBLE
Strengthened: the Stage-3 numbers are traceable to `fraud_detection_metrics.json` and the
Stage-2 numbers to `validation_metrics.json`. The one reproducibility friction is REF-R2-002:
the transfer-gap table's label set and threshold do not match the committed Stage-2 metrics,
which a reproducer will notice immediately.

### Presentation Quality: NEEDS POLISHING (minor)
Compiles cleanly per the brief. The three local fixes above are the remaining polish items.

### Technical Soundness: SOUND
Methodology unchanged and appropriate. The incident-framing distinction (Focus Change 2) is
logically sound.

### Publishability: Minor revision. With REF-R2-001 corrected and REF-R2-002/003 reconciled,
this is a publishable arXiv cs.CR preprint whose empirical claims are honestly bounded.

## Physics/Quantitative Checklist (revision-scoped)

| Check | Status | Notes |
|-------|--------|-------|
| Stage-3 trade-off numbers vs. data | pass | All six values match `fraud_detection_metrics.json` |
| Stage-2 raw vs. cleaned numbers vs. data | fail (labeling) | `tab:transfer_gap` θ=0.08 column = raw `baseline`, mislabeled "cleaned"; threshold 0.08 vs. data's cleaned 0.09 (REF-R2-002) |
| Per-chain address-count caveat | fail (miscount) | "six...single" should be five; Chain 8 n=7 omitted (REF-R2-001) |
| New citation keys resolve | pass | zhang2026sok/mao2026sok/li2026a402 + incident refs present with matching eprint IDs |
| Best single-signal AUC consistency | pass | limitations 0.599 = `tab:signal_auc` NT 0.5990 |
| Agent/transaction counts across sections | pass | 665 agents, 81,904 txns consistent abstract→evaluation→conclusions |
| ERC-8004 date anachronism | pass | 2026-01-29 footnote cleanly explains Jan-2025 window |
| Incident framing internal consistency | pass | agent-as-victim/Web2 distinction consistent across abstract, related_work, limitations, conclusions |
| Abstract recall headline labeled raw/cleaned | fail (clarity) | 95.4% not tagged raw in abstract/intro; conclusions does it right (REF-R2-003) |

## Remaining Actionable Items

```yaml
actionable_items:
  - id: "REF-R2-001"
    finding: "Stage-3 caveat says 'six of eight chains' have a single injected address and omits Chain 8 (n=7); data show five single-address chains"
    severity: "minor"
    from_round: 2
    specific_file: "paper/evaluation.tex"
    specific_change: "Change 'six of the eight chains are represented by a single injected attack address each (Chain 4 by 15 and Chain 7 by 55)' to 'five of the eight chains ... (Chain 4 by 15, Chain 8 by 7, and Chain 7 by 55)'"
    estimated_effort: "trivial"
    blocks_publication: false
  - id: "REF-R2-002"
    finding: "tab:transfer_gap captioned 'cleaned labels' but its theta=0.08 column reproduces raw-label metrics (95.4/27.6/42.8); cleaned set in data uses threshold 0.09 with recall 81.1%"
    severity: "minor"
    from_round: 1
    specific_file: "paper/evaluation.tex"
    specific_change: "Relabel tab:transfer_gap to the correct label set, make both columns' label set explicit, and reconcile the 'from 0.24 to 0.08' sentence with the data's cleaned threshold 0.09 (validation_metrics.json updated.threshold)"
    estimated_effort: "small"
    blocks_publication: false
  - id: "REF-R2-003"
    finding: "Abstract and introduction present 95.4% recall without tagging it as the raw/contaminated-label figure; conclusions correctly says '95.4% raw, 81.1% cleaned'"
    severity: "minor"
    from_round: 1
    specific_file: "paper/abstract.tex"
    specific_change: "Add a clause tagging 95.4% as the raw-label re-optimized recall and 81.1% as the cleaned-label figure, mirroring conclusions.tex; apply the same to introduction.tex contribution 4"
    estimated_effort: "trivial"
    blocks_publication: false
```

## Confidence Self-Assessment

| Dimension | Confidence | Notes |
|-----------|-----------|-------|
| Focus-change soundness (1–4) | HIGH | Verified against committed data and bib |
| Stage-3 numerical reproduction | HIGH | Exact match to fraud_detection_metrics.json |
| REF-R2-001 miscount | HIGH | Direct count from data file per_chain.instances_scored |
| REF-R2-002 raw/cleaned mislabel | HIGH | θ=0.08 column matches validation_metrics.json baseline exactly |
| Incident-framing logic | HIGH | Cross-checked four sections |
| Significance / venue fit | MEDIUM | Unchanged from round 1; not re-litigated |

---

_Round 2 review: 2026-06-27_
_Reviewer: GPD referee agent (direct revision re-review)_
_Disclaimer: This is an AI-generated mock referee report. It supplements but does not replace expert peer review._
