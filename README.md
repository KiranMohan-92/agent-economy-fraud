# Agentic fraud economy research — integrity-repaired status

> [!IMPORTANT]
> **Status, July 2026: the detector claim is withdrawn.**
>
> - **What this is:** exploratory research on agentic payments. It computes
>   transaction features for ERC-8004 registry-associated wallets on Base, audits
>   the original evaluation, and sets out a threat model and validation protocol.
>   It is not a fraud detector.
> - **Withdrawn:** the author's own July 2026 integrity review withdrew the
>   Stage 1 synthetic-benchmark result. Its generator, rows, scores and latency
>   harness are not in this repository. Stage 2 became exploratory registry-proxy
>   ranking, and the Stage 3 injection metrics were withdrawn
>   (`paper/evaluation.tex`, audit-disposition table and Stage 1 subsection;
>   `GPD/VERIFICATION-2026-07-09.md`).
> - **The "88.7%":** earlier versions reported F1 = 88.71% and called it
>   "macro-averaged". It was approximately the positive-class F1 on the
>   synthetic benchmark: the stated confusion matrix gives 88.753%
>   positive-class and 93.692% true macro (`paper/evaluation.tex`, Stage 1). It
>   cannot be reproduced from this repository. On real Base USDC data, the
>   historical composite score ranked 665 registry proxies against 1,069
>   counterparties of unknown type at ROC-AUC 0.515 (0.5147). That is a ranking
>   result, not fraud detection (`GPD/CLAIM-LEDGER.md` AEF-C006;
>   `GPD/verification/research-audit-results.json`). The old raw-label Stage 2
>   F1 of 42.8% was computed on 548 registry-proxy positives, although the text
>   said 665 (`.gpd/AUDIT-metric-consistency.md` §1).
> - **What the claim ledger still supports:** Stage 2 measures how well the
>   features separate ERC-8004 registry-associated address proxies from a
>   heuristic counterparty class (AEF-C002). Injection only checks that
>   hand-built motifs trigger the intended code paths; it is a sanity check, not
>   a robustness estimate (AEF-C009). A complete OpenClaw-to-payment chain must
>   specify delegated authority, policy, credential or custody use, payment
>   instruction, rail acceptance and settlement (AEF-C011). Two results are
>   exploratory only. Network topology shows modest descriptive separation on
>   this registry-proxy cohort (AUC 0.599, AEF-C015). A post-hoc reweighting
>   reaches about 0.62 (about 0.61 out-of-fold) and stays provisional until it is
>   bound to an immutable run manifest (AEF-C006). In the ledger's words, "No
>   experiment in the current study estimates real-world agent-fraud detection
>   performance" (AEF-C001).
> - **Read next:** [`GPD/CLAIM-LEDGER.md`](GPD/CLAIM-LEDGER.md) ·
>   [`analysis/STATUS.md`](analysis/STATUS.md) ·
>   [`analysis/CRITIQUE-and-fixes-2026-07.md`](analysis/CRITIQUE-and-fixes-2026-07.md) ·
>   [`.gpd/AUDIT-metric-consistency.md`](.gpd/AUDIT-metric-consistency.md).
>   Older files kept for traceability still show the withdrawn numbers. These
>   are the project-state and phase records under `.gpd/` and `GPD/` (including
>   `GPD/review-input/` and the June 2026 arXiv package in `GPD/publication/`),
>   the notes under `analysis/`, and the figures in `paper/figures/`. They are
>   history, not current claims.

This repository now has a narrower, defensible objective:

> Determine what the existing evidence can actually establish about
> ERC-8004 registry-associated transaction behavior, and define a falsifiable
> research program for agentic-payment control failures and financial crime.

The earlier framing—complete “human invariants,” a validated agentic-fraud
detector, banking generalization, adversarial robustness, and arXiv readiness—
is withdrawn. The empirical target was a historical registry-owner/default-
wallet proxy versus active counterparties of unknown type. It was not autonomy,
humanity, fraud, AML, or market-abuse ground truth.

## Current verdict

| Question | Status |
|---|---|
| Does the code compute transaction features? | Supported by implementation; final rerun evidence is tracked separately. |
| Does one feature weakly rank registry proxies over selected counterparties? | Exploratory only; connected and post-hoc snapshot. |
| Does the research identify autonomous agents? | No. |
| Does it detect fraud or prove a banking control gap? | No. |
| Are the synthetic attacks independent robustness evidence? | No; they are detector-informed transaction motifs. |
| Is the empirical paper publication-ready? | No; the data/provenance and construct gates are closed. |
| Is anything deployment-ready? | No. Offline research only. |

## Hard-to-vary explanation

Financial loss becomes possible when the chain from an authenticated
controller and bounded mandate, through instruction provenance and tool/wallet
authorization, to settlement is not preserved. Automation can amplify speed,
scale, delegation depth, and coordination, but actor type is not fraud. If the
authorization chain remains intact, high-speed 24/7 activity can be legitimate;
if it breaks, unauthorized risk exists whether execution is by a human, script,
compromised application, or language-model agent.

This explanation predicts concrete control points and failure evidence. It
also keeps four tasks separate: registry/automation attribution, agent
control-plane security, fraud/scam detection, and AML/market-abuse surveillance.

## Authoritative artifacts

- `paper/agent-economy-fraud-arxiv.md` and `paper/main.tex`: July 2026
  integrity revision of the withdrawn draft (not publication-ready).
- `GPD/analysis/discovery-agentic-fraud-economy-research-hardening.md`: deep
  first-principles/GPD discovery.
- `GPD/CLAIM-LEDGER.md`: exactly what is supported, exploratory, withdrawn, or
  still untested.
- `GPD/PRIMARY-SOURCE-EVIDENCE.md`: primary-source evidence boundary.
- `data/MANIFEST.md`: forensic identity and invalidity status of local data.
- `analysis/STATUS.md`: status of legacy analysis files.
- `src/a2a_detection/scripts/audit_research_claims.py`: deterministic local
  audit entry point.

Historical files remain for traceability, not as current evidence.

## Research and safety gates

Stronger claims require all of the following:

1. an immutable, event-complete release with `(chain, tx_hash, evt_index)`,
   cutoff, query provenance, license, and SHA-256 manifest;
2. verified controller, current wallet, mandate, execution, and settlement
   evidence with an explicit unknown class;
3. independently adjudicated outcome labels for each separate financial-crime
   task;
4. outer temporal or connected-component holdouts with cleaning, graph
   construction, feature design, fitting, and threshold selection inside
   training data;
5. preregistered baselines, capacity-aware metrics, uncertainty, benign twins,
   and kill criteria;
6. clean-checkout reproduction and independent adversarial review.

Never use the current score for payment blocking, account restriction,
customer accusation, regulatory filing, or law-enforcement referral.

## Local software setup

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e "src[dev]"
.venv\Scripts\python -m pytest -q -p no:cacheprovider src/a2a_detection/tests
```

Large historical data files are intentionally not treated as a released
benchmark. See `data/MANIFEST.md` before running any empirical script.
