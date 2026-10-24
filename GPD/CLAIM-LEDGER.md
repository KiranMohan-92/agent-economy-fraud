# Claim Ledger — Agentic Fraud Economy Research

**Status:** Authoritative research-integrity control  
**Version:** 1.0  
**As of:** 2026-07-10  
**Scope:** Conceptual, empirical, platform, novelty, deployment, and legal claims in this repository

## Authority and use

This ledger sets the maximum defensible wording for the research. Manuscript prose,
presentations, code comments, project summaries, and future GPD artifacts must not exceed
the wording in the **Allowed wording** field. A later result may change a status only when
its named falsifier or decisive test has been addressed with preserved evidence.

External evidence identifiers (`PSE-*`) resolve in
`GPD/PRIMARY-SOURCE-EVIDENCE.md`. Local paths identify repository evidence; they do not
make the corresponding interpretation true by themselves.

## Status vocabulary

- **supported** — directly established within the stated population, task, data version,
  and measurement limits.
- **exploratory** — plausible and partly anchored, but not yet tested by a design that
  identifies the claimed causal or predictive effect.
- **untested** — no adequate experiment or source currently adjudicates the claim.
- **withdrawn** — contradicted, construct-invalid, source-invalid, or materially broader
  than the available evidence. It must not appear as an affirmative conclusion.

## Evidence-coordinate vocabulary

Evidence must be recorded as the vector

\[
\mathcal{E}=(R,W,S,A,C,P,Y,H),
\]

not as an ordinal ladder. Each coordinate is `+` (supported), `-` (independently negated),
`?` (unknown), or `NA` (not applicable):

| Coordinate | Evidence question |
|---|---|
| R | Is the address associated through a named ERC-8004 relation (owner, mint recipient, or `agentWallet`) at the reference time? |
| W | Is the relevant wallet and its control time-correctly verified? |
| S | Is an advertised service and its endpoint operational at the relevant time? |
| A | Is the transaction linked to authenticated evidence of autonomous initiation or execution? |
| C | Is the interaction linked to verified commerce or payment activity rather than generic wallet activity? |
| P | Is person/human control independently verified? |
| Y | Is the task-specific financial-crime outcome independently adjudicated (`Y+` task-positive; `Y-` task-negative)? |
| H | Is a named harm or intervention outcome measured with valid provenance? |

The coordinates are logically independent. `A+` does not require `S+`; a compromised
autonomous wallet can act without a live advertised service. `Y+` does not require `C+`;
wallet compromise or laundering need not be a service exchange. No claim may say that an
observation “reaches” a level. It must name the coordinates it requires.

For H, `H+` means that the named endpoint was measured, not that its magnitude or direction
was favorable. Actual loss, prevented loss, recovery, intervention action, review cost, and
other harm values remain separate typed measurements. Fraud-task discrimination or
calibration requires Y. A claim that a model or intervention reduces harm requires both Y
and H under a design capable of comparing interventions.

The current Stage-2 positive label supports only **R-loader+**: selection through the
loader’s owner/mint-recipient relation. It does not by itself establish transaction-time R+,
and it leaves W, S, A, C, P, Y, and H unknown. The heuristic counterparty label does not
establish P+.

---

## AEF-C001 — Stage 2 validates fraud detection on real data

- **Status:** withdrawn
- **Evidence:** `paper/evaluation.tex` labels registry-associated addresses positive
  regardless of conduct; there are no fraud-versus-legitimate outcome labels.
  `src/a2a_detection/data/erc8004.py` loads registry `owner` or mint-recipient addresses.
- **Falsifier / upgrade gate:** A preserved cohort joining A+ to independently adjudicated
  Y+ and Y- transactions, evaluated without label leakage under a preregistered protocol.
- **Allowed wording:** “No experiment in the current study estimates real-world
  agent-fraud detection performance.”

## AEF-C002 — Stage 2 measures discrimination of registry-associated addresses

- **Status:** supported
- **Evidence:** Stage-2 labels and loader behavior in `paper/evaluation.tex` and
  `src/a2a_detection/data/erc8004.py`; ERC-8004 semantics in PSE-001.
- **Falsifier / downgrade gate:** Reproduction showing that the evaluated positive
  addresses were not the registry owner/mint-recipient addresses described by the loader.
- **Allowed wording:** “Stage 2 measures discrimination of ERC-8004
  registry-associated address proxies from a heuristic counterparty class.”

## AEF-C003 — Stage-2 positives are verified autonomous agents

- **Status:** withdrawn
- **Evidence:** The loader does not retrieve current `agentWallet`, endpoint reachability,
  mandates, or execution traces. PSE-001 separates registry ownership from current wallet
  state and does not guarantee advertised capability. PSE-009 and PSE-010 report that early
  ERC-8004 registrations are often placeholders or operationally shallow.
- **Falsifier / upgrade gate:** A+ for each claimed transaction, including authenticated
  execution provenance and time-correct address or wallet linkage. W+ and S+ may strengthen
  attribution but are not prerequisites unless the scoped mechanism requires them.
- **Allowed wording:** “The positive class is registry-associated, not a verified-autonomy
  class.”

## AEF-C004 — Stage-2 counterparties are human-controlled wallets

- **Status:** untested
- **Evidence:** The negative label is inferred from counterparty status. No proof of human
  control is present; contracts, relayers, bots, exchanges, and other automation may be
  included.
- **Falsifier / upgrade gate:** P+ for the sampled negative transactions through a blinded
  ownership-control audit using defensible human, contract, service, and automation
  evidence, with uncertainty retained rather than forced binary labels.
- **Allowed wording:** “Counterparties are heuristic negatives of unknown control type.”

## AEF-C005 — Agent identification is a necessary precondition for fraud detection

- **Status:** withdrawn
- **Evidence:** Fraud detection can be actor-agnostic and can operate on transaction,
  account, mandate, or loss evidence without first classifying an actor as an agent.
- **Falsifier / upgrade gate:** A formal result or operational constraint showing that the
  target fraud class is unidentifiable without an agent-origin variable.
- **Allowed wording:** “Agent attribution may be a useful auxiliary stratification feature;
  it is not logically necessary for fraud detection.”

## AEF-C006 — The corrected composite has modest registry-proxy ranking power

- **Status:** exploratory
- **Evidence:** `GPD/verification/research-audit-results.json` (SHA-256
  `c5185d10c6d6beae31bd6c6581d02e20d772c5d7af8b2303cd72d32e71a2950f`) deterministically
  preserves the legacy composite proxy-rank ROC-AUC 0.514718977 on 665 registry-proxy and
  1,069 counterparty rows and marks the construct invalid for operational claims. A separate
  post-hoc working-tree recombination of the same signal columns with
  `max(0, signal_AUC - 0.5)` weights reports 0.6223, approximately 0.6118 ± 0.024 under
  five-fold cross-validation. That correction is not present in the preserved scored
  artifact or bound to an end-to-end manifest containing repository revision, data hashes,
  cohort and split definition, seed, command, environment, and output checksum.
- **Falsifier / upgrade gate:** Upgrade requires an end-to-end manifest reproducing a
  prespecified corrected fusion under grouped temporal validation with no address,
  controller, or graph-neighborhood leakage. Failure to reproduce, or demonstrated leakage,
  withdraws the corrected-performance claim.
- **Allowed wording:** “A preserved audit reproduces the legacy proxy-rank ROC-AUC 0.5147.
  A post-hoc local reweighting reports proxy-ranking AUC about 0.62 and out-of-fold AUC about
  0.61, but that corrected result remains provisional until preserved in an end-to-end
  immutable run manifest. Neither measures fraud or deployment performance.”

## AEF-C007 — The corrected fusion transfers to future agents, chains, or institutions

- **Status:** untested
- **Evidence:** Evaluation is single-chain, proxy-labeled, and tied to an early ERC-8004
  cohort. No external temporal, protocol, chain, or institutional validation exists.
- **Falsifier / upgrade gate:** Locked temporal holdout plus external-chain and
  institutionally sourced validation with calibration and prevalence-aware metrics.
- **Allowed wording:** “Transfer beyond the evaluated Base cohort is unknown.”

## AEF-C008 — Synthetic attack injection validates real-world adversarial robustness

- **Status:** withdrawn
- **Evidence:** Injected attackers are generated by the detector authors, use clean
  synthetic motifs, and frequently collapse multiple nominal instances into one scored
  address. `paper/evaluation.tex` and `src/a2a_detection/scripts/inject_attacks.py` define
  this design.
- **Falsifier / upgrade gate:** Independent red-team generation or documented incident
  traces mixed into realistic benign histories, with unseen generators and powered sample
  sizes.
- **Allowed wording:** “The injection stage does not establish external adversarial
  robustness.”

## AEF-C009 — Synthetic injection is a design-envelope sanity check

- **Status:** supported
- **Evidence:** The detector responds to several signatures it was explicitly designed to
  score, while the coordinated synthetic swarm exposes the per-address architecture’s
  limitation.
- **Falsifier / downgrade gate:** Reproduction fails to activate the intended signal paths
  or the injected labels do not match the generation logic.
- **Allowed wording:** “Injection confirms that selected hand-built motifs activate the
  intended detector paths; it is a sanity check, not a robustness estimate.”

## AEF-C010 — Eight financial attack chains follow directly from OpenClaw APIs

- **Status:** withdrawn
- **Evidence:** PSE-002–PSE-005 show that the cited APIs provide policy-scoped session
  messaging, transcript access, sub-agent orchestration, and channel routing. They do not
  themselves sign transactions, create wallets, expose arbitrary financial histories, or
  erase all traces.
- **Falsifier / upgrade gate:** A documented OpenClaw configuration and reproducible trace
  showing the complete path from allowed session operation to authorized signature and
  settlement for each claimed chain.
- **Allowed wording:** “OpenClaw illustrates an orchestration control plane; financial
  consequences require an explicit, separately authorized settlement bridge.”

## AEF-C011 — An OpenClaw-to-payment chain must model the control-to-financial-state bridge

- **Status:** supported
- **Evidence:** PSE-002–PSE-005 delimit the OpenClaw orchestration layer; PSE-001 and PSE-019
  show that, for the cited blockchain setting, identity, authorization, payment, and
  service-delivery controls are distinct layers.
- **Falsifier / downgrade gate:** A reproduced configuration in which the cited OpenClaw
  session operation is itself a payment-rail state-transition primitive, with no separate
  authority, credential, instruction, or rail acceptance step.
- **Allowed wording:** “A complete OpenClaw-to-payment chain specifies delegated authority,
  policy, credential or custody use, payment instruction, rail-specific acceptance,
  clearing or settlement, and retained audit evidence. EVM chains additionally require the
  applicable signer, nonce, RPC, inclusion, and finality steps.”

## AEF-C012 — The nine human invariants are complete and necessary

- **Status:** withdrawn
- **Evidence:** The taxonomy mixes actor properties, legal constructs, authentication
  controls, and behavioral observations. Internal attack tables introduce additional
  categories outside the nine. Agents may be hardware-bound, geographically constrained,
  rate-limited, identity-persistent, stochastic, and bounded by budgets or mandates.
  PSE-006 and PSE-007 also refute biometrics and geography as necessary authentication or
  identity-verification mechanisms.
- **Falsifier / upgrade gate:** A derivation from explicit axioms plus exhaustive inclusion
  criteria, independence analysis, and counterexample testing across relevant agent and
  human regimes.
- **Allowed wording:** “The nine items are illustrative human-calibrated feature
  assumptions, not a complete set of necessary invariants.”

## AEF-C013 — Replacement domain-shift thesis

- **Status:** exploratory
- **Evidence:** Some legacy features plausibly depend on human embodiment or interaction,
  and the real proxy task shows weak/modest distributional differences. No matched
  fraud-labeled transfer experiment yet identifies the resulting calibration failure.
- **Falsifier / upgrade gate:** Before testing, create a stable child claim that fixes the
  model family and version, fraud class, population, execution regime, time window,
  operating point, primary loss, materiality margin, comparator, evidence-coordinate
  eligibility, sampling/split plan, estimator, confidence or equivalence rule, power and
  sample-size target, and multiplicity policy. A powered null rejects that scoped child
  claim; it may not be rescued by switching regimes. A positive result supports only that
  child claim, not AEF-C013 universally. Contextual recovery requires its own locked child
  comparison and cannot be inferred from degradation alone.
- **Allowed wording:** “Some human-trained fraud models could exhibit a deployment-domain
  performance shift under a specified autonomous-execution regime. No regime-specific
  shift or contextual recovery is currently established; each instance requires a
  preregistered scoped claim.”

## AEF-C014 — The five proposed signals are unavoidable agent invariants

- **Status:** withdrawn
- **Evidence:** Profitable attacks need not be high-volume; graph interaction is not unique
  to agents; timing distributions can be sampled or throttled; value can move off-chain,
  later, or through privacy-preserving mechanisms. PSE-013–PSE-015 show that graph and flow
  features are established financial-crime methods rather than agent-exclusive invariants.
- **Falsifier / upgrade gate:** Formal necessity proofs under stated attacker objectives and
  budgets, validated against adaptive red-team strategies.
- **Allowed wording:** “The five modules are candidate graph, value, timing, and contextual
  features; none is presently proven unavoidable or agent-exclusive.”

## AEF-C015 — Network topology has modest descriptive separation on this proxy task

- **Status:** exploratory
- **Evidence:** The preserved audit under AEF-C006 reports proxy-rank ROC-AUC 0.5990 for
  network topology, 0.5220 for value flow, 0.5152 for economic rationality, 0.4647 for
  temporal consistency, and 0.5000 for cross-platform activity. PSE-013–PSE-015 establish
  only the broader AML provenance of graph and subgraph methods; they do not validate this
  local construct or fraud interpretation.
- **Falsifier / upgrade gate:** Upgrade requires a preserved, leakage-free grouped temporal
  reproduction under a prespecified proxy task. Reduction to chance, or explanation by
  registry, service, or data-collection artifacts, rejects predictive interpretation.
- **Allowed wording:** “Network topology showed modest descriptive separation on this
  registry-proxy cohort. The other local signals were near or below chance, and none
  establishes fraud detection.”

## AEF-C016 — The framework is ready for banking deployment or transaction blocking

- **Status:** withdrawn
- **Evidence:** There are no real fraud labels, institutional banking data, prospective
  validation, cost model, calibrated operating point under target prevalence, or governance
  evaluation.
- **Falsifier / upgrade gate:** Prospective bank or regulated-payment evaluation with
  Y-labeled adjudicated outcomes plus H-measured harm/intervention endpoints, calibration,
  operational cost, fairness, privacy, and model-risk controls.
- **Allowed wording:** “The framework is a research prototype and must not be used as a
  basis for blocking or deployment claims.”

## AEF-C017 — No production system performs collective detection at Base granularity

- **Status:** untested
- **Evidence:** The repository contains no systematic production-system survey capable of
  supporting this universal negative. Graph and subgraph AML systems already exist in the
  literature (PSE-013–PSE-015).
- **Falsifier / upgrade gate:** A documented search protocol across vendors, patents,
  papers, and operational systems, with explicit definitions of “collective” and
  “production.”
- **Allowed wording:** “Collective detection is not implemented or validated in this work.”

## AEF-C018 — Current per-address scoring misses the injected swarm construction

- **Status:** exploratory
- **Evidence:** A live, not-yet-checksummed implementation-level rescore places all 55 unique
  senders in the
  specific self-generated CHAIN-7 construction below the historical 0.09 reference
  threshold; each score is 0.01075688. The preserved audit records that those 55 senders are
  reused across eight nominal instances, so the result is one bounded construction rather
  than eight independent campaigns.
- **Falsifier / upgrade gate:** Upgrade requires a preserved rescore manifest with code
  revision, input and output hashes, command, environment, threshold definition, and all 55
  scores. A clean reproduction above the stated reference rejects the current observation.
- **Allowed wording:** “A live, unpreserved rescore provisionally placed all 55 unique
  senders in the specific self-generated CHAIN-7 construction below the historical
  reference. This is not yet a supported numerical result, general swarm blindness, or
  operating performance.”

## AEF-C019 — Network topology, value flow, and temporal features are novel inventions here

- **Status:** withdrawn
- **Evidence:** PSE-013–PSE-015 document graph, subgraph, and real-time feature extraction
  for blockchain financial-crime detection before this work.
- **Falsifier / upgrade gate:** A feature-by-feature prior-art analysis identifies a precise
  implementation or theoretical element absent from prior methods.
- **Allowed wording:** “The contribution is an application and synthesis of established
  feature families, not their invention.”

## AEF-C020 — The application to ERC-8004 registry proxies is first-of-kind

- **Status:** exploratory
- **Evidence:** PSE-009–PSE-011 establish a rapidly developing ERC-8004 empirical literature.
  The current repository has not published a reproducible systematic search sufficient to
  prove a universal priority claim.
- **Falsifier / upgrade gate:** Any earlier work applying equivalent detection features and
  evaluation to the same construct; conversely, upgrade requires a dated, reproducible
  search protocol and tightly defined novelty clause.
- **Allowed wording:** “Among the sources documented in
  `GPD/PRIMARY-SOURCE-EVIDENCE.md` through 2026-07-10, we did not identify an identical
  registry-proxy evaluation; this is not a universal priority claim.”

## AEF-C021 — Pseudonymous public-chain data are categorically outside GDPR

- **Status:** withdrawn
- **Evidence:** PSE-008 states that public keys or related identifiers can be personal data
  when a natural person is reasonably identifiable.
- **Falsifier / upgrade gate:** Jurisdiction- and processing-specific legal analysis showing
  that no data subject is reasonably identifiable in the exact deployment context.
- **Allowed wording:** “Whether wallet and graph data are personal data is context-dependent;
  pseudonymity and public availability do not categorically remove data-protection duties.”

## AEF-C022 — Biometrics, device binding, and geography are mandatory foundations of KYC

- **Status:** withdrawn
- **Evidence:** PSE-006 recognizes cryptographic authenticators and treats biometrics as an
  optional factor, not a stand-alone authenticator. PSE-007 permits risk-based identity
  verification, including digital certificates.
- **Falsifier / upgrade gate:** A precisely scoped statute or rule requiring those exact
  modalities for the target product, jurisdiction, customer, and assurance level.
- **Allowed wording:** “Identity and authentication obligations are risk- and
  context-dependent; biometrics, device, and geography are possible controls, not universal
  legal invariants.”

## AEF-C023 — The existing study contains adjudicated real-agent fraud labels

- **Status:** withdrawn
- **Evidence:** No such label source, adjudication protocol, or case-level outcome table is
  present. Stage 1 and Stage 3 are synthetic; Stage 2 is registry-proxy classification.
- **Falsifier / upgrade gate:** Release of event-level A+ and Y+/Y- evidence with provenance,
  outcome definition, reviewer independence, and time-correct transaction linkage.
- **Allowed wording:** “Adjudicated real-agent fraud labels are absent from the current
  study.”

## Scoped child-claim registry for AEF-C013

Child IDs use `AEF-C013-T001`, `AEF-C013-T002`, and so on, allocated sequentially and never
reused. A child must be registered before data or outcome inspection with:

1. UTC creation timestamp and parent `AEF-C013`;
2. complete \(H_k\) tuple: frozen model/version, fraud class, population, regime, time
   window, operating point, primary loss, and materiality margin;
3. comparator definition and required R/W/S/A/C/P/Y/H evidence-coordinate eligibility;
4. sampling frame, grouped temporal split, estimator, interval or equivalence rule, power
   calculation, and sample-size target;
5. immutable preregistration path or URL plus SHA-256;
6. designation as the family’s primary claim or a named secondary claim;
7. family membership and multiplicity policy fixed before testing;
8. claim status from the controlled vocabulary, exact evidence, falsifier, and allowed
   wording;
9. result-artifact path and hash when execution begins; and
10. separate **run outcome**: completed-positive, completed-null, failed, or abandoned.

Every initiated child remains in the all-results register. Nulls and failures cannot be
deleted, renumbered, or replaced by a post-hoc child. **No AEF-C013 child claim is registered
as of 2026-07-10.** Run outcome is not claim status. A completed null normally withdraws the
scoped child; failed or abandoned execution remains untested; a positive result becomes
supported only if its predeclared gate and preservation requirements are satisfied.

## Change-control rule

Any status change must record:

1. the claim ID;
2. the old and new status;
3. the exact new evidence and preserved artifact;
4. the falsifier or upgrade gate that was passed;
5. the population, time window, chain or institution, and outcome definition;
6. the resulting allowed wording.

Absent that record, this ledger remains controlling.
