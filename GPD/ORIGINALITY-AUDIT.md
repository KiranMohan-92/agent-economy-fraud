# Originality / Plagiarism Audit

**Manuscript:** *Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection* (`paper/main.tex` + all `\input` sections)
**Auditor role:** GPD literature-context reviewer (novelty + citation context)
**Date:** 2026-06-27
**Method class:** idea-level novelty audit (GPD core competence) + best-effort web-only verbatim spot-check + local internal-reuse scan
**Important:** GPD has **no licensed text-similarity scanner** (iThenticate / Turnitin / arXiv full-text similarity). This audit is **not** a certified plagiarism scan. See Method Limitations (§4) before relying on the verdict.

---

## Bottom line

| Dimension | Risk for arXiv submission |
|---|---|
| Verbatim text copying (Check 2) | **LOW** |
| Idea-level originality / uncited-derivative (Check 1) | **LOW–MEDIUM** (2 missing citations, no contribution-collapsing overlap) |
| Self-plagiarism / internal reuse (Check 3) | **LOW** (normal cross-referencing, not padding) |
| **Overall** | **LOW**, conditional on adding the missing citations in §1.3 |

No fabricated matches. Every match or non-match below is grounded in an executed search or a fetched source; where I found nothing, I say so plainly. A clean verbatim result is the expected and acceptable outcome for original AI-and-human-authored prose, and that is what I found.

---

## Check 1 — Idea-level originality / novelty overlap

**Verdict: PASS with two required citation additions.** The paper's central constructs are presented as its own contributions and, on inspection against the closest prior work, hold up as genuine synthesis. The bibliography already cites the closest competitors (`zhang2026sok`, `mao2026sok`, `li2026a402`) and positions against them honestly in `related_work.tex` §6.7. Two ideas invoke prior results without attribution.

### Claim-by-claim assessment

**(a) Nine human behavioral invariants** — *Original synthesis; adequately attributed at the component level.*
No prior source presenting a "nine behavioral invariants" taxonomy was found (searched; only generic behavioral-fraud and behavioral-biometrics literature surfaced). The constituent concepts are standard and broadly attributed in-text (velocity/device-fingerprint = standard fraud practice; KYC/AML → `bsa1970`; bounded rationality / prospect theory → `kahneman2011`). The framing of the nine as *necessary consequences of human embodiment* (background §2.2) is the paper's own organizing move. **Minor gap:** Invariant I9 "bounded rationality / satisficing, not optimizing" is Herbert Simon's concept; the paper cites Kahneman (prospect theory) but not Simon. Optional citation, not load-bearing.

**(b) Eight-chain A2A attack taxonomy** — *Original; overlap with `mao2026sok` / `zhang2026sok` explicitly disclosed.* `related_work.tex` lines 182–199 already concede the overlaps (their *market manipulation* ↔ Chain_8; *inter-agent trust* ↔ Chain_4/Chain_5; their *misuse under valid authorization* ↔ identity-persistence) and frame the contribution as operationalizing/detecting a subset rather than re-deriving the taxonomy. This is the correct handling; not uncited-derivative. Chain_4 (Disposable Agent Army) is correctly identified as a machine-speed Sybil attack and cites `douceur2002`.

**(c) Five-signal agent-native detection** — *Original.* No prior five-signal agent-invariant detector found. Derived from the paper's own on-chain validation.

**(d) "Behavioral Mimicry Paradox"** — *Original coinage, but invokes an uncited impossibility result.* The term itself returns no prior match (Check 2). However, `evaluation.tex` line 258 states the finding "aligns with the broader impossibility result that perfect behavioral mimicry requires genuine stochasticity, which deterministic agents cannot produce." A **real, directly-on-point theoretical result exists** — Simchowitz et al., *The Pitfalls of Imitation Learning when Actions are Continuous* (arXiv:2503.09722): a smooth deterministic imitator cannot match a stochastic expert without state-dependent stochasticity. The paper invokes "the broader impossibility result" in the singular **without citing anything.** This is a **missing citation**, not plagiarism (the wording is not lifted), but it should be added so the claim is anchored rather than gestural.

**(e) Collective / swarm detection gap** — *Empirical demonstration is original; the general observation is not novel and is mostly, but not fully, hedged.* The specific contribution — Chain_7 achieving 0% recall under per-address scoring on injected swarm data — is the paper's own measurement and is legitimately novel. But the *general* claim that per-address/individual scoring is blind to coordinated multi-agent behavior is well-trodden in the multi-agent-security literature (e.g., arXiv:2505.02077 "Open Challenges in Multi-Agent Security"; arXiv:2502.14143 "Multi-Agent Risks from Advanced AI"). The paper does cite `lazer2026agentic` for collective-behavior risk at the security level (related_work line 164), which covers the obligation adequately. Recommend (optional) one additional multi-agent-security citation to avoid any "we first identified" reading; the current text is already hedged ("known gap," "no validated implementation exists").

### Idea-level conclusion
No prior work contains the paper's main result (empirical, behavioral-invariant on-chain detection with the reported metrics). Novelty framing is **not materially false** — in fact the paper is unusually self-critical (AUC 0.515, Chain_7 0% recall, transfer-gap analysis). No escalation to reject or major_revision on novelty grounds. Two citations should be added (Simchowitz et al. = required; a multi-agent-security cite and Simon = optional).

---

## Check 2 — Text-level verbatim-copy spot-check (best effort)

**Verdict: NO VERBATIM MATCH FOUND on any of the 15 probes.** Distinctive prose, definitions, the invariant framing, the mimicry-paradox wording, and the methodology descriptions are original. Platform descriptions (the flagged higher-risk area) are paraphrases of documented facts with proper citation, not lifted text.

| # | Probe (location) | Search outcome | Verdict |
|---|---|---|---|
| 1 | "machines that attempt to mimic human behavior execute their mimicry too perfectly" (`evaluation.tex` 252) | No source contains this sentence | No match |
| 2 | "Behavioral Mimicry Paradox" + CV (coined term) | No prior use of the term in this sense | No match (original coinage) |
| 3 | OpenClaw `sessions_*` API descriptions (`background.tex` 22–44) | OpenClaw docs exist (docs.openclaw.ai) and were **fetched directly**; docs use terse wording ("set `timeoutSeconds: 0` to enqueue and return immediately"); paper paraphrases the documented fact and adds its own adversarial gloss ("market surveillance," "forensic destruction") | No verbatim copy; properly cited to `openclaw2026` |
| 4 | "no body to tire, no device to fingerprint, no geographic location to constrain" (`introduction.tex` 18) | No source match | No match |
| 5 | "machine regularity is a detection signal, not camouflage" / "anomalous regularity is equally diagnostic" | No source match | No match |
| 6 | "deterministic imitation of a stochastic process" impossibility claim | No verbatim match; a *real uncited result* exists (see Check 1d) | No match (but add citation) |
| 7 | Moltbook reputation/listings description (`background.tex` 46–57) | Moltbook is real (moltbook.com, Wikipedia, CNN); paper's reputation-rate-asymmetry argument ($10^3$–$10^6\times$) is its own analysis, not doc text | No match; cited to `moltbook2026` |
| 8 | Nine-invariant abstract opener (`abstract.tex` 1–4) | No source match | No match |
| 9 | "capabilities of a high-frequency trading desk" (`background.tex` 24) | Generic HFT-desk content only; no match to the sentence | No match |
| 10 | Velocity amplification 450× / 9,000 tx/h arithmetic (`threat_model.tex` 84–110) | Generic velocity-rule patents only; the arithmetic is the paper's own | No match |
| 11 | ERC-8004 CREATE2 "identical addresses across multiple chains" (`background.tex` 73–81) | Public, widely-documented ERC-8004/CREATE2 fact; cited to `erc8004` | No match (public fact, cited) |
| 12 | "per-address scoring is blind to coordinated multi-agent attacks" (`abstract.tex` 24) | Concept appears in multi-agent-security literature but no verbatim sentence match | No match (see Check 1e) |
| 13 | "too perfect" timing / CV<0.05 threshold derivation (`threat_model.tex` 200–225) | No source match | No match |
| 14 | "Know Your Agent" framing | Matches `financialbrand2026` — which **is the cited source title**, not copying | Expected match (own citation) |
| 15 | x402 "100 million agentic payments" | Matches `chainalysis2026x402` — **cited source** | Expected match (own citation) |

**Higher-risk area finding (platform docs):** OpenClaw documentation is live and was fetched. The paper's API descriptions are paraphrase + original adversarial interpretation, properly attributed to `openclaw2026`. No documentation text was lifted verbatim. Separately, the doc page fetched did **not** surface `cleanup: "delete"`, `pruneAfter: "1h"`, or `identityLinks` (paper `background.tex` 34–39, `threat_model.tex` 132–136); these may live on other doc pages or may need a factual re-verification before submission — that is an **accuracy** concern, **not** a plagiarism concern, and is out of scope here but flagged for the verification lane.

---

## Check 3 — Self-plagiarism / internal reuse

**Verdict: LOW. Normal cross-referencing, not padding.** Recurring figures and phrases appear across sections because they are the same empirical findings restated where relevant, not large copied text blocks.

| Recurring item | Locations | Assessment |
|---|---|---|
| Agent tx value range \$0.06–\$0.91 | intro 6, background 227, detection 139, appendix_signals 35 | Same empirical finding cited in 4 contexts (contribution claim, evidence, threshold derivation, appendix spec). Legitimate. |
| CV ≈ 1.87 (genuine agents) | threat_model 189/195/205, evaluation 252, appendix_signals 141 | Core empirical anchor of the mimicry paradox; restatement is expected. |
| "machine speed" phrasing | introduction 7, related_work 35/158, detection 235 | Common term, not block reuse. |
| Mimicry-paradox statement | threat_model §3.3, evaluation §5.4.1 | Set up in threat model, validated in evaluation — standard paper structure, not duplication. |

No verbatim multi-sentence block was found duplicated across sections. Material in `analysis/` (the working notes) is the source substrate for the paper, as expected; that is normal author-to-own-manuscript flow, not self-plagiarism of a *published* work.

**Minor internal-consistency nit (not a plagiarism issue):** `threat_model.tex` line 214 gives simulated mimicry "maximum CV = 0.008," while `evaluation.tex` line 252/255 and `appendix_signals.tex` 141 use CV < 0.005. Slight inconsistency in the stated mimicry-CV bound; worth a one-line reconciliation in the revision lane.

---

## 4. Method limitations (read before relying on this audit)

1. **No licensed corpus.** GPD has no iThenticate / Turnitin / arXiv full-text overlap engine. This audit cannot produce a similarity percentage and cannot certify the manuscript against the paywalled, closed, or non-indexed corpora those tools cover.
2. **Web-only, sampled spot-check.** Check 2 tested ~15 of the most distinctive passages, not every sentence. A clean result lowers but does not eliminate the probability of an unsampled near-duplicate.
3. **Search-engine blind spots.** `WebSearch` is US-region, English-biased, and indexes a subset of the web; it can miss non-English sources, recently removed pages, content behind logins, and full PDF bodies (it often matches titles/abstracts, not interior text).
4. **Live-platform dependency.** OpenClaw/Moltbook are fast-moving startups; their documentation can change after this audit's fetch date (2026-06-27), which would affect re-checks of the platform-description paragraphs.
5. **This is the originality lane only.** Factual accuracy of platform parameters (e.g., `pruneAfter`, `identityLinks`), metric correctness, and statistical validity are out of scope and belong to the verification/referee lanes.

**Recommended escalation if certainty is required:** run one licensed iThenticate/Turnitin pass before submission. Given the consistently clean web spot-check and the original character of the prose, I assess the residual probability of an undetected verbatim lift as low, but only a licensed scan can close item 1.

---

## Disposition

- **Verbatim plagiarism:** no evidence found; **LOW** risk.
- **Idea-level originality:** sound; add **Simchowitz et al. (arXiv:2503.09722)** for the impossibility-result claim (required) and optionally one multi-agent-security cite + Simon for bounded rationality. No contribution-collapsing overlap; **no reject / no major_revision** on novelty grounds.
- **Self-plagiarism:** none of concern; **LOW**.
- **Overall arXiv risk: LOW**, conditional on the one required citation.

This artifact is decisive on novelty and citation context. Per panel protocol, it does **not** issue the final referee recommendation.
