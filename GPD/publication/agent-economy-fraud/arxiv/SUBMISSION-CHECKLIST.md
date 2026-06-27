# arXiv Submission Checklist

**Paper:** Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection
**Package:** `GPD/publication/agent-economy-fraud/arxiv/arxiv-submission.tar.gz` (≈126 KB)
**Prepared:** 2026-06-27 (June-2026 refresh round)

## Build & package verification (DONE — machine-checked)

- [x] LaTeX compiles clean: `pdflatex` ×3 + `bibtex`, exit 0, **no undefined references or citations**.
- [x] **Clean-room test passed**: tarball extracted to an empty dir compiles to PDF using only its own contents — both with a `bibtex` run and using the bundled `main.bbl` alone.
- [x] `main.tex` is at the tar root (arXiv auto-detects `\documentclass`).
- [x] `main.bbl` bundled (arXiv runs bibtex, but bundling guarantees the bibliography renders).
- [x] 4 figures included as PDF (`figures/*.pdf`) — PDFLaTeX-compatible.
- [x] No aux/log/backup files in the tree; placeholder scan (TODO/FIXME/MISSING/empty cites) **clean**.
- [x] Package size 126 KB — far under the 50 MB arXiv limit.
- [x] 47 references resolve; 15 new June-2026 sources verified (4 arXiv IDs confirmed via arXiv; industry/incident sources cited as dated `@misc` with access dates).
- [x] 47/47 unit tests pass; Stage-3 metrics reproduced bit-for-bit from committed data.

## Round-2 referee pass (DONE)

- [x] GPD referee re-reviewed the revised manuscript (`GPD/REFEREE-REPORT-R2.md`): **minor revision**, all 7 round-1 changes confirmed resolved, all 4 June-2026 focus changes verified sound against committed data.
- [x] All 3 referee-flagged residual issues fixed: REF-R2-001 (Stage-3 single-address-chain miscount: "six"→"five", Chain 8 n=7 added), REF-R2-002 (`tab:transfer_gap` relabeled raw-label set; θ=0.08 raw vs θ=0.09 cleaned reconciled with `validation_metrics.json`), REF-R2-003 (95.4% tagged raw / 81.1% cleaned in abstract + intro).

## Manual steps required before upload

- [x] **Author byline decided:** independent-researcher submission — `main.tex` now reads `Kiran Mohan / Independent Researcher`. *(Confirm exact name spelling; optionally add contact email + ORCID — one-line TODO marked in `main.tex`.)*
- [x] **arXiv primary category decided:** **`cs.CR`** (Cryptography and Security).
- [x] **Cross-list decided:** **`q-fin.RM`** (Risk Management).
- [ ] **License:** confirm arXiv license selection (the implementation is Apache-2.0; the paper text license is the author's choice — arXiv default non-exclusive is fine).
- [ ] **Abstract for the arXiv web form:** copy from `abstract.tex` (plain text; check it is within arXiv's ~1920-char metadata limit).
- [ ] **Acknowledgments:** `main.tex` references contract `0x8004...9432` and Dune Analytics — confirm wording/attribution is acceptable.
- [ ] **GitHub repo URL:** `appendix_reproducibility.tex` uses a `<repo>` placeholder for the source/PyPI package — fill in the real public URL (or remove the install-from-source block) before upload.

## Note on author identity (genuine decision)

The byline is intentionally left as a placeholder because it is yours to set and has real
implications — in particular whether to submit as an **independent researcher** or under an
**institutional affiliation**. This is a fraud-detection paper; an employer affiliation may
carry review/disclosure considerations. This was not auto-filled by design.

## Recommended category rationale (hard-to-vary)

- **`cs.CR` primary:** the paper's core artifact is a security threat model + detection
  framework with empirical on-chain evaluation — squarely Cryptography and Security, and the
  venue where the directly-competing SoKs (2604.03733, 2604.15367) sit.
- **`q-fin.RM` cross-list:** the application domain is banking fraud / financial-crime risk,
  and the recommendations target financial institutions — the right secondary audience.
