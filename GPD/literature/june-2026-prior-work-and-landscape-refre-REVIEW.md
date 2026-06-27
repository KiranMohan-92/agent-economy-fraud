---
topic: June 2026 prior-work and landscape refresh for "Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection"
date: 2026-06-27
depth: standard
paper_count: 14 new/updated sources
tier1_count: 5
tier2_count: 6
tier3_count: 3
field_assessment: active_research
status: completed
---

# Literature Review: June 2026 Prior-Work and Landscape Refresh

Targeted repositioning review for the existing, complete manuscript (`paper/main.tex`, drafted "April 2026").
Scope is deliberately narrow: what changed between April 2026 and June 2026, and how the manuscript must
reposition before arXiv submission. This is not a from-scratch survey; the paper's 43-entry bibliography and
core thesis are taken as given. All new sources below were verified via arXiv abstract pages or primary
publisher pages on 2026-06-27.

## Executive Summary

1. **The "agentic commerce security" space has crowded fast.** Between January and April 2026 at least three
   systematization papers (SoK 2604.03733, A402 2603.01179, SoK 2604.15367) and one cybersecurity survey
   (2601.05293) appeared that taxonomize agent-payment protocols, threat classes, and defenses. None performs
   empirical on-chain fraud **detection** on real agent transaction data, and none defines behavioral
   invariants. The paper's detection-side contribution survives as a genuine complement, but its
   "first to model A2A fraud" and "open and urgent gap" framing in `related_work.tex` is now contestable and
   must be softened.

2. **The "no documented A2A fraud / pre-crime window" framing is now stale.** As of June 2026 there are
   documented on-chain AI-agent payment-fraud incidents (Grok/Bankr Morse-code prompt-injection theft of
   ~$150K-200K on Base, 4 May 2026; malicious LLM-router wallet drains ~$500K, April 2026) and documented
   agent-impersonation fraud at massive scale (DataDome: 16.4M spoofed Meta-ExternalAgent requests,
   Jan-Feb 2026). The narrow claim "no confirmed *systematic A2A-commerce* fraud exploiting this paper's
   specific invariant blind spots" is still defensible, but the broad "no documented cases / 6-12 month
   pre-crime window" framing is **partially false** and must be retired.

3. **Ecosystem scale has moved by ~3 orders of magnitude past the paper's dataset.** ERC-8004 reached
   Ethereum mainnet on 29 Jan 2026 and now has official registries on 10+ chains. A Coinbase/Tempo/Virtuals
   report documents ~176M agent transactions settling ~$73M (98.6% USDC) between May 2025 and April 2026;
   x402 alone reports 100M+ payments (~119M on Base + ~35M on Solana by March 2026). The paper's single-chain
   665-agent / 81,904-transaction Base slice is now a tiny fraction of an instrumented, multi-chain economy.
   This **strengthens** the relevance argument but **inverts** the "Cross-Platform signal inactive / multi-chain
   is future work" limitation: multi-chain is now the dominant reality, not a near-term scenario.

4. **Net assessment (confirms the requester's hypothesis): the new landscape STRENGTHENS the thesis and
   WEAKENS the positioning.** Industry has independently converged on the paper's core claim — that
   human-identity-assumption detection breaks for agents ("Know Your Agent," DataDome "80% of sites do not
   verify agent identity," TRM "agents compress financial-crime timelines"). But the first-mover, pre-crime,
   and sole-gap claims are no longer defensible. The repair is to reposition from "first to identify the gap"
   to "the empirical, behavioral-invariant **detection** complement to a now-active protocol-security and
   taxonomy literature."

5. **Highest-confidence benchmark facts** for downstream use: ERC-8004 mainnet 2026-01-29 (HIGH); x402 100M+
   payments in ~6 months (HIGH); AP2 announced 2025-09-16, donated to FIDO Alliance 2026-04-28 (HIGH);
   MetaMask Agent Wallet 2026-06-08 (HIGH); Grok/Bankr incident 2026-05-04 (HIGH); DataDome 16.4M spoofed
   Meta-ExternalAgent requests Jan-Feb 2026 (HIGH).

Field assessment: **active_research** (was implicitly framed as "speculative / pre-crime" in the manuscript).

---

## A. New / Updated Sources Table

Position is exactly one of COMPLEMENT (we do X they do not), OVERLAP (genuine collision; novelty risk), or
CORROBORATION (independent evidence for our thesis).

| # | Source | Type | Verified identifier | One-line scope | Our position | Proposed bibtex key |
|---|--------|------|---------------------|----------------|--------------|---------------------|
| 1 | SoK: Blockchain Agent-to-Agent Payments | arXiv (SoK) | arXiv:2604.03733 (submitted 2026-04-04) | Systematizes A2A payments over a discovery/authorization/execution/accounting lifecycle; threat classes (weak intent binding, misuse under valid authorization, payment-service decoupling, limited accountability) | COMPLEMENT (+ partial OVERLAP on threat taxonomy) | zhang2026sok |
| 2 | A402: Binding Cryptocurrency Payments to Service Execution for Agentic Commerce | arXiv | arXiv:2603.01179 (submitted 2026-03-01) | TEE-assisted atomic service channels that bind x402 payments to verified service execution | COMPLEMENT | li2026a402 |
| 3 | A Survey of Agentic AI and Cybersecurity | arXiv (survey) | arXiv:2601.05293 (submitted 2026-01-08) | Broad agentic-AI cybersecurity survey: agent collusion, memory poisoning, governance gaps; not finance-specific | CORROBORATION (peripheral) | lazer2026agentic |
| 4 | SoK: Security of Autonomous LLM Agents in Agentic Commerce | arXiv (SoK) | arXiv:2604.15367 (submitted 2026-04, v2) | Unified 5-dimension security framework, 12 cross-layer attack vectors across ERC-8004/AP2/x402/ACP/MPP; layered defense architecture | OVERLAP (closest competitor; novelty risk) | mao2026sok |
| 5 | DataDome AI Traffic Report 2026 | Industry report | datadome.co/threat-research/ai-traffic-report (March 2026) | 7.9B agent requests Jan-Feb 2026; 16.4M spoofed Meta-ExternalAgent; 80% of agents do not self-identify, 80% of sites do not verify | CORROBORATION | datadome2026 |
| 6 | TRM Labs — Autonomous AI Agents and Financial Crime | Industry report | trmlabs.com (2026-04-01) | Agents compress financial-crime timelines; signing-authority agents are high-value targets; accountability analysis | CORROBORATION | trmlabs2026 |
| 7 | The Financial Brand — "Know Your Agent" | Industry/trade press | thefinancialbrand.com (2026-02-24) | Argues banks must move from AI-assisted to AI-executed fraud posture via "Know Your Agent" behavioral monitoring | CORROBORATION | financialbrand2026 |
| 8 | x402 adoption (Chainalysis "Inside x402") | Industry analytics | chainalysis.com (2026) | 100M+ agentic payments; ~119M Base + ~35M Solana by March 2026; ~$600M annualized | CORROBORATION (scale) | chainalysis2026x402 |
| 9 | x402 Foundation (Cloudflare/Coinbase) | Standard/announcement | blog.cloudflare.com/x402 (2026) | x402 Foundation; members incl. Google, Visa, AWS, Circle, Anthropic, Stripe | CORROBORATION (scale) | x402foundation2026 |
| 10 | Google Agent Payments Protocol (AP2) | Standard | cloud.google.com AP2 blog (announced 2025-09-16; donated to FIDO Alliance 2026-04-28, v0.2 "Human Not Present") | Mandate-based agent payment standard; 60+ partners incl. MetaMask/Coinbase stablecoin rails | CORROBORATION (scale) | ap2protocol2025 |
| 11 | MetaMask Agent Wallet | Industry/product | metamask.io / coindesk.com (2026-06-08) | Self-custodial agent wallet with Guard Mode, daily-outflow limits, allowlists, 2FA step-up | CORROBORATION (also validates P2 controller step-up recommendation) | metamask2026agentwallet |
| 12 | USDC AI-agent payments report (Coinbase/Tempo/Virtuals) | Industry data | cryptocurrencyhelp.com summary of co-published report (2026) | ~176M agent transactions, ~$73M settled, 98.6% USDC, May 2025-April 2026 | CORROBORATION (scale; reframes dataset size) | usdcagentpayments2026 |
| 13 | Grok / Bankr prompt-injection wallet theft | Documented incident | OECD.AI incident 2026-05-04-4a73; SlowMist analysis (May 2026) | Morse-code prompt injection via X drained ~3B DRB tokens (~$150K-200K) from an agent wallet on Base | CORROBORATION (documented agent-payment fraud) | grokbankr2026 |
| 14 | Unit 42 — OpenClaw Skill Marketplace AI supply-chain threat | Industry security research | unit42.paloaltonetworks.com (2026) | Palo Alto Unit 42 threat analysis of OpenClaw's skill marketplace as an AI supply-chain attack surface | CORROBORATION (validates OpenClaw case study) | unit42openclaw2026 |

Verified-but-excluded-from-positioning (background only, not load-bearing): arXiv:2601.04583 "Autonomous Agents
on Blockchains: Standards, Execution…" (Jan 2026, CORROBORATION/background); arXiv:2603.25100 "From Logic
Monopoly to Social Contract … Autonomous Agent Economies" (governance, peripheral); arXiv:2507.19550 "Towards
Multi-Agent Economies: … A2A with Ledger-Anchored Identities and x402 Micropayments" (July 2025, infrastructure
COMPLEMENT). These are listed for completeness but are not required citations.

---

## B. Per-Source Positioning Paragraphs (falsifiable)

### 1. SoK: Blockchain Agent-to-Agent Payments — arXiv:2604.03733 — COMPLEMENT (+ partial threat-taxonomy OVERLAP)
Zhang et al. systematize blockchain A2A payments along a four-stage lifecycle (discovery, authorization,
execution, accounting) and name four challenge classes: weak intent binding, misuse under valid authorization,
payment-service decoupling, and limited accountability. It is a systematization of protocol designs, not an
empirical study: it runs no on-chain experiment, reports no detection metric (no precision/recall/AUC), uses no
real transaction dataset, and defines no human behavioral invariants. Our position is the detection-side
complement: where 2604.03733 maps *what can go wrong* in the payment lifecycle, we measure *whether agent
activity is distinguishable on-chain* using five agent-native signals validated on 665 Base agents and an
attack-injection corpus. Falsifier: if a reader finds a precision/recall/AUC table or a labeled on-chain
detection experiment anywhere in 2604.03733, this positioning is wrong. The partial overlap to flag: their
"misuse under valid authorization" challenge overlaps conceptually with our Invariant I6 (identity persistence)
and CHAIN_4 (disposable agent army); we should cite them and state that we operationalize and *detect* a subset
of their threat classes rather than re-derive the taxonomy.

### 2. A402 — arXiv:2603.01179 — COMPLEMENT
Li et al. build A402, a protocol layer that binds cryptocurrency payment finalization to verified service
execution using TEE-assisted adaptor signatures and "Atomic Service Channels," fixing x402's lack of
end-to-end atomicity across execution, payment, and result delivery. This is *prevention by construction*
(make unauthorized payment release cryptographically impossible), operating at the protocol layer before any
fraud occurs. We are the *post-hoc behavioral detection* complement, operating at the observability layer on
agents and protocols that do **not** have such guarantees (the 665 Base agents we study transact over plain
USDC, not A402). The two are non-competing and ideally co-deployed. Falsifier: if A402 were shown to perform
behavioral anomaly detection on a population of independent addresses, the "prevention vs. detection" framing
would collapse — it does not; it secures a single payment-service binding.

### 3. A Survey of Agentic AI and Cybersecurity — arXiv:2601.05293 — CORROBORATION (peripheral)
Lazer et al. survey agentic-AI cybersecurity broadly: threat hunting, reconnaissance/exploitation, agent
collusion, and memory poisoning, with three use-case prototypes. It is not finance-specific and does no
on-chain payment analysis, so it neither competes with nor directly supports our empirical claims. Its value
is a single corroborating citation that "agent collusion" is a recognized systemic risk class — which is
exactly our CHAIN_7 swarm/collective-detection gap framed from the security side. Use it only as a one-line
supporting reference in the AI-Agent-Security subsection; do not lean on it for novelty.

### 4. SoK: Security of Autonomous LLM Agents in Agentic Commerce — arXiv:2604.15367 — OVERLAP (closest competitor)
Mao et al. are the most direct collision and the primary novelty risk. They build a "unified security
framework" organizing threats along five dimensions and enumerate 12 cross-layer attack vectors spanning agent
integrity, transaction authorization, inter-agent trust, market manipulation, and regulatory compliance,
explicitly covering ERC-8004, AP2, x402, ACP, ERC-8183, and MPP — substantially the same protocol surface and
several of the same threat categories as our eight-chain taxonomy (their "market manipulation" ≈ our CHAIN_8;
their "inter-agent trust" ≈ our CHAIN_5/CHAIN_4). The decisive distinction that preserves our contribution:
2604.15367 is a taxonomy + *layered defense architecture* paper with **no empirical on-chain detection, no real
transaction dataset, no detection metrics, and no behavioral-invariant formalism**. Our differentiator narrows
to exactly three things they lack: (i) the nine human behavioral invariants as the *generative* explanation of
why detection fails, (ii) five concrete on-chain signals with a fusion model, and (iii) three-stage empirical
validation (synthetic F1=88.7%, real Base AUC=0.515 reported honestly, 7/8 injected chains). This paper MUST be
cited and explicitly distinguished; failing to do so is the single largest reviewer-rejection risk. Falsifier:
if 2604.15367 contains any labeled on-chain detection experiment with reported metrics, our "only empirical
detection paper" claim fails and the contribution must be re-scoped further.

### 5. DataDome AI Traffic Report 2026 — CORROBORATION
DataDome's March 2026 report (covering Jan-Feb 2026 traffic) is the strongest single corroboration of our core
thesis from operational data. It records 7.9B agent requests in two months, identifies 16.4M spoofed
Meta-ExternalAgent requests (with ChatGPT-User at 7.9M and PerplexityBot the most-impersonated by rate), and
finds that **80% of AI agents do not properly identify themselves and 80% of sites do not verify agent
identity**. That is a direct, large-N empirical instance of our central claim — identity- and
embodiment-assumption controls fail when the actor is software — and it documents *agent-impersonation fraud*
as a present, not future, phenomenon. Caveat to state honestly in-paper: this is Web2 HTTP-layer agent
spoofing, not on-chain A2A *payment* fraud; it corroborates the invariant-failure mechanism (I2/I5/I6) but is
adjacent to our on-chain threat model. Use it to replace the now-false "no documented agent fraud" framing,
not as direct evidence of on-chain A2A fraud.

### 6. TRM Labs — Autonomous AI Agents and Financial Crime — CORROBORATION
TRM's 1 April 2026 report states that autonomous agents "compress financial-crime timelines" — layering and
cross-chain dispersion can occur in seconds, narrowing detection windows — and that an agent holding signing
authority over treasury/operational wallets "becomes a high-value target." This independently corroborates our
velocity-invariant (I1) and detection-latency arguments and our P1 velocity-threshold recommendation. It is
analysis/forecast, not a documented case ledger, so it supports the *mechanism* and *urgency*, not the
existence of confirmed A2A-commerce fraud. It is the right citation to anchor a reframed Limitations §
"Pre-Crime Research Validity" paragraph that concedes the window has effectively arrived.

### 7. The Financial Brand — "Know Your Agent" — CORROBORATION
This 24 Feb 2026 trade article argues that fraud prevention must "evolve from stopping AI-assisted fraud to
preparing for AI-executed fraud" and adopt a "Know Your Agent" posture of continuous behavioral monitoring as
agents drift or are compromised. This is the banking-practitioner restatement of our entire thesis and our
P0/P1 agent-native-overlay recommendations. It is the best citation to show our recommendations are aligned
with where the industry is already moving — but it also means we can no longer claim to be first to call for
agent-native detection; we must cite it and position our framework as a concrete, validated instantiation of
the "Know Your Agent" principle.

### 8-12. Scale corroboration (x402, AP2, MetaMask Agent Wallet, USDC report) — CORROBORATION
These five sources jointly retire the "is the surface big enough to matter?" question (the paper's variation V4
in `background.tex`). Verified: ERC-8004 mainnet 2026-01-29 with 10+ official chain registries; x402 100M+
payments in ~6 months (~119M Base + ~35M Solana by March 2026, ~$600M annualized) under an x402 Foundation
backed by Google/Visa/AWS/Circle/Anthropic/Stripe/Coinbase/Cloudflare; AP2 announced 2025-09-16 with 60+
partners and donated to the FIDO Alliance 2026-04-28 (v0.2 added "Human Not Present" pre-authorized flows);
MetaMask Agent Wallet launched 2026-06-08 with Guard Mode, daily-outflow limits, allowlists, and 2FA step-up;
and a Coinbase/Tempo/Virtuals report documenting ~176M agent transactions settling ~$73M (98.6% USDC), May
2025-April 2026. Two notable consequences: MetaMask's 2FA step-up is a live commercial implementation of our P2
"controller step-up authentication" recommendation (strengthens that recommendation, weakens its novelty); and
AP2 "Human Not Present" flows are a concrete instance of the human-oversight removal our threat model assumes.

### 13. Grok / Bankr prompt-injection wallet theft — CORROBORATION (documented incident)
On 4 May 2026, an attacker embedded a hidden Morse-code instruction in an X reply; Grok (assisting Bankr/Bankrbot)
executed a transfer of ~3B DRB tokens (reported ~$150K-200K) from a verified agent wallet on Base. Logged in the
OECD.AI incident registry and analyzed by SlowMist as "AI agent permission-chain abuse." Importance for us: it is
a *documented, on-chain, agent-mediated payment-fraud incident on the very chain we study*, which directly
falsifies any blanket "no documented agent-payment fraud" sentence. Critical honesty caveat for the rewrite: this
is agent-as-*victim* (external prompt injection hijacking one agent's wallet — squarely in the Greshake et al.
indirect-prompt-injection thread the paper already cites), **not** agent-as-*fraudster* executing
behavioral-invariant-violating A2A commerce. We must cite it as evidence that agent-payment fraud is now real and
on-chain, while explicitly distinguishing it from our threat model rather than claiming it as a validation of our
detection framework.

### 14. Unit 42 — OpenClaw Skill Marketplace threat — CORROBORATION (validates platform case study)
Palo Alto Unit 42 published a threat analysis of OpenClaw's skill marketplace as an emerging AI supply-chain
attack surface. Since OpenClaw is one of the paper's two named platform case studies, an independent enterprise
security team treating OpenClaw as a real attack surface corroborates the platform-capability grounding of our
threat model. Cite it in §2 (Background, OpenClaw) and §6 to show external validation of the platform choice.

---

## C. Stale-Claims Ledger

Priority order: (1) "no documented cases / pre-crime window" framing, (2) scale/single-chain figures,
(3) related-work omissions. "Current text" is quoted or closely paraphrased from the manuscript.

| # | Claim (current text) | File / locator | Why it is stale | Replacement direction |
|---|----------------------|----------------|-----------------|-----------------------|
| C1 | "As of April 2026, no documented case of systematic agent-to-agent fraud exploitation exists in the public record." | `paper/limitations.tex` §Pre-Crime Research Validity (line ~35) | Documented on-chain agent-payment fraud now exists (Grok/Bankr 2026-05-04; malicious LLM-router drains ~$500K April 2026); agent-impersonation fraud documented at scale (DataDome 16.4M spoofed requests). | Narrow the claim: "no documented case of *systematic A2A-commerce fraud exploiting the specific behavioral-invariant blind spots modeled here*." Add a sentence acknowledging documented agent-payment fraud (Grok/Bankr, LLM routers) and agent-impersonation fraud (DataDome), distinguishing them as agent-as-victim / Web2-layer rather than our on-chain agent-as-fraudster model. Cite grokbankr2026, datadome2026. |
| C2 | "We therefore treat the next 6-12 months as a planning scenario rather than a validated prediction." / abstract: "The 6-12 month A2A fraud window is treated as a planning scenario." | `paper/limitations.tex` §Pre-Crime (line ~37); `paper/agent-economy-fraud-arxiv.md` Abstract | The window has effectively arrived: documented incidents + full industry pivot (TRM, Financial Brand "Know Your Agent," Experian forecast, FIS/CommBank deployments) within 2-4 months of the draft. | Reframe from "6-12 month future window" to "the transition is already underway in 2026." Keep epistemic honesty but drop the specific forward-dated window. Cite trmlabs2026, financialbrand2026. |
| C3 | "Agent-to-agent (A2A) commerce is not a forecast---it is an empirical fact… limited fraud-monitoring practice designed around autonomous transactors." | `paper/introduction.tex` (lines 3-7) | Partially overtaken: fraud-monitoring practice for agents is now actively emerging (Know Your Agent, MetaMask Guard Mode, FIS+Anthropic financial-crime agents, CommBank fraud agent). "Limited practice" understates June-2026 activity. | Soften "limited fraud-monitoring practice" to "fraud-monitoring practice for autonomous transactors is nascent and rapidly forming," cite financialbrand2026, metamask2026agentwallet. Strengthens relevance while staying accurate. |
| C4 | "665 agents registered under the ERC-8004 identity standard on the Base blockchain have executed over 81,000 USDC transactions" framed as the headline scale. | `paper/introduction.tex` (lines 3-5); arxiv.md §1 | Now a tiny slice: ~176M agent transactions / ~$73M settled across the multi-chain ecosystem (Coinbase/Tempo/Virtuals); x402 alone 100M+ payments. | Keep the 665/81,904 figures as *our studied sample* but add one sentence contextualizing it against the documented ~176M-transaction, multi-chain ecosystem so reviewers see the dataset is a deliberate single-chain slice, not the whole field. Cite usdcagentpayments2026, chainalysis2026x402. |
| C5 | "As of April 2026, the registry reports 16,549 agents on Base chain, 14,000 on Ethereum mainnet, and 34,278 on BNB Chain." and "over 65,000 agents across three chains." | `paper/background.tex` §2.1 (lines 59-71) and §2.3 V4 (line ~211) | Date-sensitive and now under-counts the chain set: ERC-8004 has official registries on 10+ chains (Ethereum, Base, BNB, Gnosis, Polygon, Avalanche, Taiko, Optimism, Arbitrum, Linea, Monad) as of June 2026. The specific per-chain figures could not be independently re-verified at June 2026 and should be re-checked. | Re-verify the three per-chain counts at submission time; broaden "across three chains" to "across 10+ official chain registries"; add the multi-chain registry list. Cite a current registry/explorer snapshot dated at submission. |
| C6 | Data range "Base chain USDC A2A volume: 81,904 txns, Jan 2025-Apr 2026 (15 months)" attributed to "ERC-8004 registered agents." | `analysis/real-world-fraud-cases.md` §1; `paper/dune2026` bib note "Jan 2025-Apr 2026"; `paper/introduction.tex` | Datestamp tension: ERC-8004 reached mainnet only 2026-01-29 (introduced as draft Aug 2025). Attributing Jan-2025 transactions to "ERC-8004-registered agents" is anachronistic on its face. | Add a clarifying footnote: registration is recent (post-Jan-2026 mainnet); the Jan-2025 start reflects the *full USDC transaction history of addresses that later registered*, not registration date. This pre-empts an easy reviewer objection. |
| C7 | "Cross-Platform correlation is architecturally defined but inactive because the evaluation dataset is single-chain… Multi-chain evaluation data… is a near-term priority." | `paper/limitations.tex` §Cross-Platform; arxiv.md §4 & §8 | The framing treats multi-chain as future work, but multi-chain (CREATE2 same-address deployment, 10+ registries, AP2/x402 cross-rail) is now the *dominant* operating reality of the ecosystem. | Re-frame from "future near-term priority" to "the single most consequential gap, because the ecosystem is now predominantly multi-chain." Strengthens the limitation's stated importance and motivates the P3 multi-chain recommendation. |
| C8 | "To our knowledge, no prior work combines (1) documented A2A platform capabilities as the basis for a threat model, (2) formal invariant analysis… and (3) real on-chain validation… The intersection… remains an open and urgent research gap." | `paper/related_work.tex` §Key differentiation (lines 161-167) | Contestable: SoKs 2604.03733 and 2604.15367 now cover A2A platform capabilities + threat taxonomy; the "open gap" language overclaims. | Narrow the novelty claim to the part still unoccupied: "we are, to our knowledge, the only work that pairs a behavioral-invariant account with *empirical on-chain detection metrics on real agent transactions*; recent SoKs taxonomize the threat and protocol surface but report no detection results." Cite zhang2026sok, mao2026sok, li2026a402. |
| C9 | Related Work omits all 2026 agentic-commerce-security literature; newest agent-security cites are Greshake 2023 / Carlini 2023 / a2aprotocol2025 / mcp2024. | `paper/related_work.tex` §AI Agent Security (lines 139-159); `paper/references.bib` | For a June-2026 arXiv submission, omitting the three named SoKs/protocol papers and the industry reports is a glaring currency gap reviewers will flag immediately. | Add the new Related Work paragraphs in Section D below; add bib entries for zhang2026sok, li2026a402, lazer2026agentic, mao2026sok, and the key industry sources. |
| C10 | "The prior mandatory-biometrics framing has been narrowed to controller step-up authentication" (P2) presented as a forward proposal. | `paper/agent-economy-fraud-arxiv.md` §7; `paper/recommendations` | MetaMask Agent Wallet (2026-06-08) ships exactly this: 2FA step-up for out-of-policy agent transactions. AP2 v0.2 adds consent mandates. | Note that controller step-up is now *implemented in production* (MetaMask Guard Mode), upgrading P2 from "policy proposal" toward "validated by deployment," and cite metamask2026agentwallet, ap2protocol2025. |

---

## D. Required Related Work Additions (drop-in ready)

Insert into `paper/related_work.tex`. New keys must be added to `references.bib` (see sidecar). Each paragraph
is written to be dropped under the indicated subsection.

**D1 — New subsection or paragraph under §6 "Agentic Commerce Security" (new):**
> Concurrent with this work, a systematization literature on agentic-commerce security has emerged. Zhang
> \etal\cite{zhang2026sok} systematize blockchain agent-to-agent payments across a discovery--authorization--
> execution--accounting lifecycle and identify failure classes including weak intent binding and misuse under
> valid authorization. Mao \etal\cite{mao2026sok} build a unified security framework spanning ERC-8004, AP2,
> x402, and related standards, enumerating twelve cross-layer attack vectors and a layered defense
> architecture. These works taxonomize the threat and protocol surface but report no empirical on-chain
> detection: they neither measure whether agent activity is distinguishable on real transaction data nor define
> the behavioral invariants whose failure explains why human-assumption detectors miss agents. Our contribution
> is complementary and detection-side---we operationalize a subset of these threat classes as five on-chain
> signals and report three-stage empirical validation, including an intentionally weak real-data ranking result
> (AUC = 0.515) that the taxonomy literature has no mechanism to surface.

**D2 — Paragraph under §6 (protocol-layer prevention):**
> On the prevention side, Li \etal\cite{li2026a402} propose A402, which binds payment finalization to verified
> service execution using TEE-assisted atomic service channels, closing the payment--service decoupling that
> plain x402 leaves open. A402 prevents unauthorized release by construction at the protocol layer; our
> framework instead provides post-hoc behavioral detection over agents and protocols that lack such guarantees,
> including the plain-USDC Base population we study. The two approaches are non-competing and most effective in
> combination.

**D3 — Paragraph under §6.6 "AI Agent Security" (extend existing):**
> Beyond external compromise of individual agents, the broader systemic risks of agentic AI---including agent
> collusion and coordinated multi-agent behavior---have been surveyed by Lazer
> \etal\cite{lazer2026agentic}, which frames at the security level the same collective-behavior problem our
> CHAIN\_7 swarm gap targets at the detection level. Documented incidents now exist: a May 2026 prompt-injection
> attack drained roughly \$150K--\$200K from an agent-controlled wallet on Base\cite{grokbankr2026}. Such
> incidents are agent-as-victim hijackings rather than the agent-as-fraudster A2A commerce our threat model
> addresses, but they confirm that agent-mediated on-chain payment fraud has moved from hypothesis to public
> record.

**D4 — Replacement for the "Key differentiation" paragraph (lines 161-167), and a sentence for §1/§8 to
retire the pre-crime framing:**
> To our knowledge, this is the only work that pairs a behavioral-invariant account of detection failure with
> empirical on-chain detection metrics on real agent transactions. Recent systematizations\cite{zhang2026sok,
> mao2026sok} catalog the threat and protocol surface, and protocol designs\cite{li2026a402} harden individual
> payments, but none reports detection performance on observed agent activity. The transition we anticipated is
> already underway in 2026: industry guidance now calls explicitly for ``Know Your Agent'' behavioral
> monitoring\cite{financialbrand2026}, operational telemetry documents agent-impersonation fraud at
> scale\cite{datadome2026}, and risk analyses report that autonomous agents compress financial-crime
> timelines\cite{trmlabs2026}. We therefore position this paper not as a first warning but as an early
> empirical, detection-side complement to a now-active agentic-commerce-security literature.

---

## E. Net Assessment: Strengthen or Weaken?

**Verdict: the June-2026 landscape STRENGTHENS the paper's core thesis and WEAKENS its positioning. This
confirms the requester's hypothesis, and the evidence supports it on both halves.**

**Strengthens the thesis** ("human-invariant-only detection has structural blind spots for agents"):
- DataDome operational data: 80% of sites do not verify agent identity; 16.4M spoofed Meta-ExternalAgent
  requests — a large-N instance of the identity/embodiment invariants (I2/I5/I6) failing in production.
- The Financial Brand "Know Your Agent" and TRM Labs independently restate the thesis in banking/AML language,
  including the velocity-invariant (I1) and detection-latency arguments.
- Documented on-chain agent-payment fraud (Grok/Bankr) and Unit 42's OpenClaw threat analysis convert two of
  the paper's load-bearing assumptions (agent wallets are attackable; OpenClaw is a real attack surface) from
  asserted to evidenced.
- MetaMask Guard Mode and AP2 consent mandates are live implementations of the paper's P2 controller-step-up
  recommendation — the recommendations are now validated by deployment.

**Weakens the positioning** (first-mover / pre-crime / sole-gap):
- "No documented cases / 6-12 month pre-crime window" is partially false (C1, C2) — documented incidents and a
  full industry pivot exist within months of the draft.
- The "open and urgent gap / no prior work combines…" novelty claim (C8) is contested by two SoKs
  (2604.03733, 2604.15367) and A402 covering the same protocol/threat surface.
- The single-chain 665-agent dataset (C4) is dwarfed by a documented ~176M-transaction, multi-chain ecosystem,
  and the "multi-chain is future work" limitation (C7) is inverted by current reality.

**What survives as defensible, narrowed novelty:** the paper is (to current knowledge) the only work pairing a
*behavioral-invariant explanation* of detection failure with *empirical on-chain detection metrics on real
agent transactions*, and the only one to honestly report the weak real-data transfer (AUC 0.515) and the
swarm/collective-detection gap (CHAIN_7). The recommended repositioning is a net win: trading an
overclaimed-and-now-falsifiable first-mover frame for a corroborated, evidence-backed detection-complement
frame makes the paper *more* defensible at review, not less. Risk if unchanged: a reviewer who knows
2604.15367 or the Grok/Bankr incident will read the current pre-crime and sole-gap language as out of date and
discount the whole contribution.

---

## Active Anchor Registry

| Anchor ID | Anchor | Type | Source / Locator | Why It Matters | Contract Subject IDs | Required Action | Carry Forward To |
|-----------|--------|------|------------------|----------------|----------------------|-----------------|------------------|
| anc-mao2026sok | SoK: Security of Autonomous LLM Agents in Agentic Commerce | benchmark/prior-work | arXiv:2604.15367 | Closest competitor; must be cited + distinguished or risk rejection | related_work.tex §6; C8 | cite + distinguish | writing |
| anc-zhang2026sok | SoK: Blockchain A2A Payments | prior-work | arXiv:2604.03733 | Threat-taxonomy overlap; detection-side complement | related_work.tex §6; C8 | cite + distinguish | writing |
| anc-li2026a402 | A402 protocol | prior-work | arXiv:2603.01179 | Prevention-vs-detection complement | related_work.tex §6 | cite | writing |
| anc-grokbankr | Grok/Bankr on-chain theft (2026-05-04) | documented incident | OECD.AI 2026-05-04-4a73; SlowMist | Falsifies "no documented agent-payment fraud" | limitations.tex C1; intro | cite + reframe | writing/verification |
| anc-datadome | DataDome AI Traffic Report | corroboration/benchmark | datadome.co (Mar 2026) | Large-N evidence invariants fail; retires "no cases" | limitations.tex C1; intro | cite | writing |
| anc-erc8004-mainnet | ERC-8004 mainnet date | benchmark fact | 2026-01-29 (crypto.news, eips.ethereum.org) | Datestamp tension with Jan-2025 data range | background.tex; C6 | verify + footnote | writing/verification |
| anc-scale-176m | ~176M agent tx / ~$73M / 98.6% USDC | benchmark scale | Coinbase/Tempo/Virtuals report (2026) | Reframes 665-agent dataset as a slice | intro C4 | cite + contextualize | writing |
| anc-metamask-aw | MetaMask Agent Wallet 2FA step-up | corroboration | metamask.io; coindesk (2026-06-08) | Validates P2 controller step-up recommendation | recommendations C10 | cite | writing |

`Carry Forward To` names workflow stages only.

---

## Machine-Readable Summary

```yaml
---
review_summary:
  topic: "June 2026 prior-work and landscape refresh for A2A commerce fraud-detection manuscript"
  key_papers: 14
  open_questions: 3
  consensus_level: "active"
  benchmark_values:
    - quantity: "ERC-8004 Ethereum mainnet launch date"
      value: "2026-01-29"
      source: "crypto.news / eips.ethereum.org"
    - quantity: "x402 cumulative agentic payments"
      value: "100M+ in ~6 months (~119M Base + ~35M Solana by Mar 2026)"
      source: "Chainalysis Inside x402"
    - quantity: "Agent transactions settled (ecosystem)"
      value: "~176M transactions, ~$73M, 98.6% USDC (May 2025-Apr 2026)"
      source: "Coinbase/Tempo/Virtuals report"
    - quantity: "Spoofed Meta-ExternalAgent requests"
      value: "16.4M (Jan-Feb 2026)"
      source: "DataDome AI Traffic Report 2026"
    - quantity: "Grok/Bankr on-chain agent-wallet theft"
      value: "~$150K-200K, Base, 2026-05-04"
      source: "OECD.AI incident 2026-05-04-4a73 / SlowMist"
    - quantity: "MetaMask Agent Wallet launch"
      value: "2026-06-08 (Guard Mode, 2FA step-up)"
      source: "metamask.io / CoinDesk"
  active_anchors:
    - anchor_id: "anc-mao2026sok"
      anchor: "SoK: Security of Autonomous LLM Agents in Agentic Commerce"
      locator: "arXiv:2604.15367"
      type: "prior artifact"
      why_it_matters: "Closest competitor; novelty risk; must cite and distinguish"
      contract_subject_ids: ["related_work", "C8"]
      required_action: "cite"
      carry_forward_to: "writing"
    - anchor_id: "anc-grokbankr"
      anchor: "Grok/Bankr on-chain agent-wallet theft"
      locator: "OECD.AI 2026-05-04-4a73"
      type: "benchmark"
      why_it_matters: "Falsifies the no-documented-cases framing"
      contract_subject_ids: ["C1", "limitations"]
      required_action: "compare"
      carry_forward_to: "writing"
    - anchor_id: "anc-datadome"
      anchor: "DataDome AI Traffic Report 2026"
      locator: "datadome.co/threat-research/ai-traffic-report"
      type: "background"
      why_it_matters: "Large-N corroboration that identity invariants fail in production"
      contract_subject_ids: ["C1", "C3"]
      required_action: "cite"
      carry_forward_to: "writing"
  recommended_methods:
    - method: "Reposition as empirical detection-side complement to taxonomy/protocol-security SoKs"
      regime: "Related Work and Introduction framing"
      confidence: "HIGH"
    - method: "Retire pre-crime/6-12-month-window framing; cite documented incidents"
      regime: "Introduction, Limitations, Abstract"
      confidence: "HIGH"
    - method: "Contextualize single-chain 665-agent dataset against multi-chain 176M-tx ecosystem"
      regime: "Introduction, Limitations (Cross-Platform)"
      confidence: "HIGH"
---
```

## Recommended Reading Path (for the rewrite)

1. arXiv:2604.15367 (Mao et al.) — read first; it is the closest competitor and dictates the differentiation paragraph.
2. arXiv:2604.03733 (Zhang et al.) and arXiv:2603.01179 (Li et al.) — for the complement/prevention distinctions.
3. DataDome AI Traffic Report + The Financial Brand "Know Your Agent" — the corroboration to replace the "no cases" framing.
4. TRM Labs report + Grok/Bankr incident (OECD.AI / SlowMist) — for the reframed Limitations §Pre-Crime.
5. Coinbase/Tempo/Virtuals USDC report + Chainalysis x402 + MetaMask Agent Wallet — for the scale and P2-recommendation updates.

## Verification Status

All 14 positioned sources verified on 2026-06-27 via arXiv abstract pages (papers) or primary publisher pages
(industry reports/products). Not independently re-verified at June 2026 and flagged for re-check at submission:
the manuscript's per-chain agent counts (16,549 Base / 14,000 Ethereum / 34,278 BNB), and the user-supplied
"$24M within 7 months" x402 figure (my sources report 100M+ payments / ~$600M annualized / $73M settled, but
not the $24M snapshot). The "~130k total agents" figure in the task brief is internally inconsistent with its
own per-chain breakdown (~64.5k) and with launch-week registry counts (~24.5k late Jan 2026); treat total
agent count as date-sensitive and cite a dated registry snapshot rather than a single headline number.
