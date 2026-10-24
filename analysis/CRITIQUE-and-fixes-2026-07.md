> [!WARNING]
> **SUPERSEDED for theory and allowed wording (2026-07-10).** This 2026-07-09 critique is kept
> as numerical-audit input only. Its framing of Stage 2 as agent/human identification, its
> claim that agent identification is a "necessary precondition" for fraud detection (withdrawn,
> AEF-C005), its verdict that the nine-invariant theory is sound and hard to vary (withdrawn,
> AEF-C012), its "FIXED" label for the 0.62 fusion result (exploratory and provisional,
> AEF-C006), and its recommended abstract must not be reused. See
> [`analysis/STATUS.md`](STATUS.md) and [`GPD/CLAIM-LEDGER.md`](../GPD/CLAIM-LEDGER.md).

# Deep Critique and Fixes — Agent Economy Fraud Research (2026-07-09)

**Reviewer stance:** First-principles + Deutsch hard-to-vary, from the perspective of
agentic-AI, financial-crime, and ML-evaluation expertise. Cross-checked by an independent
GPT-5.6 (Codex) adversarial read. Every empirical claim below was reproduced from committed
data, not taken from the project's own reports.

**Bottom line:** The project's *theoretical* contribution is sound and hard-to-vary. Its
*empirical* apparatus does not test what the paper claims it tests, and one concrete code
defect was silently halving the headline ranking metric. The prior verification
(`.gpd/VERIFICATION-FINAL.md`, "PASSED, 0 blocking issues") was wrong to pass these.

---

## Tier 0 — The load-bearing problem (no code fix repairs it)

### F0. Construct-validity failure: the real-data task is agent-ID, not fraud detection

The Stage-2 "real on-chain validation" labels **agents vs. human counterparties**. Every one
of the 665 ERC-8004 agents is a positive *regardless of whether it ever committed fraud*.
So the experiment measures **agent identification**, not **fraud detection**. Being an agent
is not being a fraudster.

- Stage 1 (synthetic) — fraud labels exist, but the data is fabricated by the authors.
- Stage 2 (real) — labels are agent/human, i.e. identity, not fraud.
- Stage 3 (injection) — separates the authors' own synthetic attacks from real agents.

**No experiment in the paper detects real agent fraud on real data.** This is a category
error in the measurement, independently flagged by GPT-5.6 as "the fatal construct-validity
flaw." It cannot be fixed by re-weighting, re-thresholding, or better labels — only by
acquiring ground-truth *fraud* labels (adjudicated cases), which do not currently exist.

**Required reframe:** state plainly that the framework is validated as an *agent-identification*
overlay — a necessary-but-not-sufficient precondition for agent-fraud detection — and that
fraud-detection effectiveness on real data is **unvalidated**.

---

## Tier 1 — Concrete defects (fixable; some fixed here)

### F1. The fusion layer was destroying signal — FIXED

`data/validation_metrics.json` reports composite ROC-AUC **0.5147**, but Network Topology
alone scores **0.5990**. A fusion whose output ranks *worse than its best input* is
subtracting information.

**Mechanism (reproduced):** Temporal Consistency has real-data AUC **0.4647 — below chance**
(anti-correlated with being an agent), yet the shipped "AUC-proportional" scheme gave it the
**second-largest weight (0.2505)**. Adding an anti-signal drags the composite down. A logistic
combiner confirms the mechanism: it assigns TC a **negative** coefficient (−1.3) while NT gets
+4.6.

**The docstring's AUCs were phantom.** `fusion.py` derived its weights from
{NT 0.6214, TC 0.5683, ER 0.5497, VF 0.5290}. Those numbers **do not reproduce** from the
committed data. The reproducible AUCs (from `data/detection_results_dune.csv` ⨝
`data/labels_dune.parquet`) are {NT 0.5990, VF 0.5220, ER 0.5152, TC 0.4647} — matching
`validation_metrics.json` exactly.

**Fix applied** (`src/a2a_detection/signals/fusion.py`): weights ∝ max(0, AUC−0.5), so a
below-chance signal earns zero weight.

| Fusion | Composite real-data AUC |
|--------|--------------------------|
| Shipped (old, phantom-AUC weights) | 0.5147 |
| Drop TC, equal-weight the other 3 | 0.5249 |
| **(AUC−0.5) weights, TC→0 (applied)** | **0.6223** (0.6118 ± 0.024, 5-fold CV) |
| Logistic regression (5-fold OOF) | 0.6505 (learnable ceiling) |
| Network Topology alone | 0.5990 |

Verification: all 47 unit tests pass; two tests that had hard-coded the phantom AUCs were
rewritten to assert the reproducible behavior (TC weight must be 0; NT must dominate).

**Honest characterization even after the fix:** ~0.62 AUC is *weak-but-real* ranking, not
strong detection. Bootstrap 95% CI [0.594, 0.650] — the lower bound excludes chance, so the
lift over the old 0.515 is statistically real, but the ceiling is modest. It should be reported
as such.

**Threshold caveat:** the corrected composite is NT-dominated, so its score distribution
differs from the old composite; the old FLAG threshold (0.09) is no longer calibrated. Report
the corrected result as an AUC (threshold-independent); any target operating point requires a
fresh threshold sweep. The old recall figures (95.4% / 81.1%) belong to the old composite and
are not comparable to the corrected one.

### F2. Attack injection is self-validating AND statistically underpowered

- **Circularity:** every injected attacker (`0xdead…`) transacts *only with other injected
  addresses*. An attacker's entire on-chain history IS the attack pattern (e.g. CHAIN_3's
  attacker = exactly 500 machine-speed txns, nothing else). Real agents have messy mixed
  histories; these are noise-free and trivially separable. The detector is never tested
  against realistic evasion.
- **Underpowered / address collapse:** `_synthetic_addr(chain_id, index, role)` ignores
  `instance_id`, so all N injected *instances* of a chain reuse the **same** attacker
  addresses. That is why `fraud_detection_metrics.json` shows `instances_scored: 1` for
  CHAIN_1/2/3/5/6. "100% per-chain recall" for those chains = detecting **one** hand-built
  address. This is not evidence; it is a definitional restatement of the injection.
- **Stage-3 AUC 0.777 measures the wrong contrast:** injected-synthetic-attacks vs.
  real-agents, not agents-vs-humans and not fraud-vs-legit (the script's own note admits this).

**Required reframe:** demote Stage 3 from "validation" to "sanity check that the injected
signatures are within the detector's design envelope," report per-chain N honestly, and stop
citing "7/8 at 100%" as an empirical result.

### F3. Metric contradictions across artifacts (see `.gpd/AUDIT-metric-consistency.md`)

Four hard contradictions confirmed by dedicated audit:

1. **665 vs 548 agents on the *same* 2,134-address run.** `evaluation.tex:120` says 665;
   `validation_metrics.json` `baseline.n_positive` = 548 (523 tp + 25 fn — the exact
   denominator of the 95.4% headline). Two different Dune snapshots are described as one.
2. **Two mutually-exclusive derivation stories for "665":** `appendix_dataset.tex:49` (filtered
   *down* from 1,505) vs. `STATE.md:63` (grown *up* from 548 via re-ingestion).
3. **Test count 32 (`PROJECT.md:152`) vs 47 (paper + live `pytest`).** 47 is correct.
4. **Raw-stage composite AUC 0.59 computed but marked "not reported"** in the paper while the
   less favorable 0.515 cleaned figure is headline — a more favorable number was omitted.

### F4. Temporal Consistency's design assumption is invalid against this negative class

TC's `_circadian_violation` assumes the negative class sleeps (low activity 02:00–06:00 UTC).
The negatives are on-chain counterparties that are largely automated, so the assumption fails —
which is *the paper's own thesis* turned on the paper's own signal. This is the root cause of
F1's below-chance TC. Keep TC for genuinely-human negatives (Stage 1); zero it on real Base
data (done in the fix).

---

## Tier 2 — Rigor gaps (from referee report, partially addressed in prose)

- **Velocity amplification 2.16M** compares peak-agent vs. average-human throughput
  (apples-to-oranges). Reframe as peak-vs-peak or state the comparison explicitly.
- **CV<0.05 mimicry threshold** asserted, not derived; no FPR against legitimate automated
  systems (market makers, scheduled payments).
- **No confidence intervals anywhere.** With 665 positives, AUC 0.62 needs a CI
  (bootstrap ≈ ±0.02–0.03); "0.515 vs 0.599" differences are meaningless without one.
- **"+49.1% over human baseline"** — baseline system unspecified (NOTE-02, still open).

## Tier 3 — Citations (verified 2026-07-09 via arXiv + source pages)

**One fabricated citation found and FIXED; two metadata errors FIXED; rest verified real.**

### FABRICATED (fixed)
- **`cartella2021`** — bib claimed *Marco Cartella, Olivier Hubert, Yann-Aël Le Borgne,
  Gianluca Bontempi, "Adversarial Attacks Against Credit Card Fraud Detection Systems,"
  IEEE Access vol. 9, pp. 128630–128643.* No such paper. The real work (the one the referee
  meant) is **Francesco Cartella, Orlando Anunciação, Yuki Funabiki, Daisuke Yamaguchi,
  Toru Akishita, Olivier Elshocht, "Adversarial Attacks for Tabular Data," SafeAI @ AAAI-21,
  arXiv:2101.08030.** Wrong first name, 3 invented co-authors (Le Borgne & Bontempi are real
  ULB fraud researchers grafted on), fabricated venue/volume/pages. **Corrected in
  `references.bib`.** Lesson: this was inserted to satisfy the referee's request without
  pulling the actual paper — check any other referee-response additions the same way.

### METADATA ERRORS (fixed)
- **`chainalysis2026x402`** — real post, wrong title. Was "Inside x402: 100M+ Agentic
  Payments on Base"; actual title "Agentic Payments Cross the Threshold: Inside x402's Path
  to Meaningful Adoption" (Chainalysis, 2026-06-03). 100M+ figure corroborated. Fixed.
- **`zhang2026sok`** — real paper, but primaryClass was `cs.CR`; arXiv lists it under
  `q-fin.GN`. Fixed.

### VERIFIED REAL (author lists / titles matched against source)
- `zhang2026sok` arXiv:2604.03733 — exact 11-author match ✓
- `mao2026sok` arXiv:2604.15367 — exact 6-author match ✓ (v2, revised 2026-05-01)
- `li2026a402` arXiv:2603.01179 — exact 7-author match ✓
- `lazer2026agentic` arXiv:2601.05293 — exact 4-author match ✓
- `simchowitz2025imitation` arXiv:2503.09722 — exact match ✓
- `grokbankr2026` — OECD.AI incident page confirms Morse-code prompt injection draining
  ~$150K–200K in DRB tokens via Grok/Bankrbot on Base, May 2026 ✓ (exact match)
- Classic refs (`aleskerov1997` CARDWATCH, `bursztein2014`, `iliou2021`, `gleave2020`,
  `biggio2013/2018`, `greshake2023`, `carlini2023`, `douceur2002`, `chandola2009`,
  `tesfatsion2006`) — well-known real works, high confidence ✓

### COULD NOT AUTO-VERIFY (manual check advised)
- **`datadome2026`** — source page returns HTTP 403 (bot-blocked; ironic for a bot-detection
  vendor). Not disproven, but manually confirm the "16.4M spoofed Meta-ExternalAgent requests
  / 7.9B agent requests" figures before relying on them in the limitations section.

### Literature-gap status (referee §2.2–2.3)
The referee's requested additions are **already present and now verified real**: adversarial-ML
(`cartella2021` now corrected, `biggio2013/2018`, `aleskerov1997`) and Web2 bot detection
(`bursztein2014`, `iliou2021`, `jonker2019`). The gap the referee flagged has been closed.

---

## What survives, and what to claim

**Survives (hard-to-vary):** The nine-invariant taxonomy and the structural argument that
detectors monitoring only human-embodiment signals have *necessary* blind spots against
software agents. This follows from the definition of the invariants and does not depend on the
weak empirics. GPT-5.6 concurs: "a plausible structural hypothesis … but this paper does not
empirically establish it."

**Honest one-paragraph abstract (recommended):** "Five behavioral signals show
limited-to-moderate ability to distinguish registered Base agents from human counterparties
(composite ROC-AUC 0.62 after correcting a fusion defect that had depressed it to 0.51);
learned fusion improves ranking further (0.65). This is *agent identification*, a precondition
for—but not equivalent to—agent-fraud detection, which remains unvalidated on real data because
all evaluated attacks are synthetic. The contribution is a hard-to-vary conceptual framework
plus a first-generation, honestly-bounded signal overlay, not a deployment-ready fraud
detector."

---

## Fix status

| Item | Status |
|------|--------|
| F1 fusion defect | **FIXED** in `fusion.py` (+tests); AUC 0.515→0.622, verified |
| F1 phantom AUC docstring | **FIXED** (reproducible AUCs documented) |
| F0 construct validity | Reframe applied to paper abstract + limitations |
| F2 injection circularity | Reframe applied to paper §5.3 + limitations |
| F3 metric contradictions | 665/548 + test-count fixes applied; see audit for full list |
| Tier 2 rigor / Tier 3 citations | Flagged for author action (CIs, citation verification) |

_Reproduction scripts: `scratchpad/refute.py`, `refute2.py`. Evidence: committed parquet/csv._
