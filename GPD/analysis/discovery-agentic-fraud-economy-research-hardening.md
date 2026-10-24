# Deep Discovery — Agentic Fraud Economy Research Hardening

**Discovery mode:** Standalone GPD Level 3 deep dive  
**Topic:** Agentic fraud economy research hardening  
**Date:** 2026-07-10  
**Authority:** `analysis/STATUS.md`  
**Claim control:** `GPD/CLAIM-LEDGER.md`  
**External evidence:** `GPD/PRIMARY-SOURCE-EVIDENCE.md`

## Summary recommendation

The project should stop trying to prove that software agents necessarily violate a complete
set of nine human invariants. That explanation is easy to vary, contains counterexamples,
and is not what the empirical work measures.

The research can be made rigorous by changing its objective:

> **Measure whether, where, and why fraud models calibrated on human-controlled execution
> lose calibration or discrimination under verified autonomous execution, and test whether
> principal, mandate, and decision-time runtime, authorization, and settlement context
> restores that performance. Adjudicated outcomes supply labels and evaluation only.**

This replacement is narrower but stronger. It distinguishes actor provenance from conduct,
does not equate automation with fraud, and ties every causal detail to an observable and a
falsifier. Existing data remain useful as a registry-proxy measurement study and as a
design-envelope sanity check. They do not validate real fraud detection.

**Confidence:**

- **High** that the current real-data task is registry-proxy discrimination rather than
  fraud detection.
- **High** that the original OpenClaw-derived financial chains and complete-invariant claims
  require withdrawal or reconstruction.
- **Medium** that scoped domain-shift hypotheses are worth testing; no model/regime effect is
  currently established.
- **Low / unmeasured** for real-agent fraud-detection effectiveness, deployment utility,
  prevalence, and transfer across chains or institutions.

Planning is justified only for evidence-building experiments, not deployment.

---

## 1. Discovery objective

### 1.1 Primary question

For a preregistered model, fraud class, population, execution regime, and materiality margin,
does a frozen model calibrated on human-controlled transactions lose calibration or
discrimination on verified autonomous execution, and can decision-time context recover
performance?

### 1.2 Secondary questions

1. What evidence is sufficient to say that a transaction was autonomously initiated?
2. Which fraud outcomes are in scope: wallet compromise, mandate abuse, deception,
   laundering, market abuse, collusion, or another class?
3. Which observables exist at the identity, control, authorization, settlement, service,
   institutional, and adjudication planes?
4. Which proposed features are causally necessary, merely contingent, or proxies for data
   collection and registry membership?
5. Can context-aware models outperform human-calibrated baselines on independent,
   outcome-labeled agent transactions?
6. Which controls prevent harm by construction, and which only detect activity after the
   fact?
7. Is an observed transport gap caused by execution mode, or by principal, protocol,
   service, mandate selection, time, or other confounding?

### 1.3 Success criterion

The hardened program succeeds only if it produces one of two honest outcomes:

- a reproduced, externally valid performance shift on verified autonomous execution, plus
  a separately tested repair—and, if causal wording is used, the identification conditions
  in Section 4.4; or
- a credible null result showing that ordinary fraud controls transfer adequately once
  principal, mandate, and transaction context are modeled.

Either result is scientifically useful. A registry-owner classifier presented as a fraud
detector is not.

---

## 2. Scope and boundaries

### In scope

- verified autonomous or delegated financial execution;
- fraud and financial-crime outcomes with explicit adjudication criteria;
- identity, mandate, runtime, wallet, settlement, service-delivery, and value-flow evidence;
- model discrimination, calibration, error rates, and operational cost;
- adaptive evasion and population-level coordination;
- on-chain and institutional settings when their observation planes are kept distinct;
- prevention controls as comparators to behavioral detection.

### Out of scope unless separately evidenced

- treating all ERC-8004 registrations as operational agents;
- treating all x402 or stablecoin traffic as autonomous A2A commerce;
- treating automation, agent origin, or unusual behavior as fraud labels;
- claiming banking validity from a public-chain proxy dataset;
- universal claims about production systems or global fraud prevalence;
- platform-specific financial attack claims without an explicit wallet and settlement path;
- categorical legal conclusions across jurisdictions and deployment contexts.

### Unit-of-analysis convention

The unit must be named for every experiment:

- transaction;
- address/account;
- agent identity;
- principal or organization;
- mandate/session;
- service exchange;
- case or campaign;
- population/window.

Metrics from different units are not interchangeable. “One detected address,” “one attack
instance,” and “500 generated transactions” are three different sample sizes.

---

## 3. Construct model: evidence, inference, and unknown

Let:

- \(R=1\): address is associated with an ERC-8004 identity registration;
- \(W=1\): current wallet control is verified;
- \(S=1\): a live service endpoint is verified;
- \(A=1\): authenticated evidence supports autonomous initiation or execution;
- \(C=1\): the interaction is linked to verified commerce or payment activity;
- \(P=1\): person/human control is independently verified;
- \(Y=1\): the task-specific financial-crime outcome is independently adjudicated positive;
- \(H\): a named harm or intervention outcome is measured, such as realized loss, prevented
  loss, recovery, review cost, or action taken;
- \(X\): observed transaction and graph features;
- \(Z_{pre}\): context fixed before execution, such as principal, task, mandate, service,
  asset, policy, and eligibility;
- \(Z_{post}\): runtime, authorization, and settlement telemetry generated after execution
  begins but available before the operational decision, where applicable.

The evidence state is \(\mathcal{E}=(R,W,S,A,C,P,Y,H)\), with each coordinate marked
supported, negated, unknown, or not applicable. These are independent coordinates, not a
ladder: autonomy does not require a live advertised service, and fraud does not require an
A2A service exchange.

Y and H are never prediction inputs. Y supplies the adjudicated task label and evaluation
endpoint. H supplies a separately named harm or intervention endpoint; `H+` denotes that a
measurement exists, not its value or direction. Case outcomes, disputes, recovery, action
results, or investigator artifacts observed after the decision time must not enter \(X\),
\(Z_{pre}\), or \(Z_{post}^{decision}\).

### 3.1 What the current real-data task estimates

The current task approximates ranking by registry proxy:

\[
\operatorname{AUC}_{R}
= \Pr\bigl(s(X_{R=1}) > s(X_{R=0})\bigr),
\]

where \(R=0\) is a heuristic counterparty class rather than verified \(P=1\).

### 3.2 What a fraud claim would require

A fraud detector for verified agent activity must estimate something like:

\[
\Pr(Y=1 \mid X,Z,A=1)
\]

and validate ranking or decisions against \(Y\), not \(R\). Registry discrimination does not
identify this quantity without strong, currently unsupported assumptions connecting registry
membership to autonomy and fraud.

This Y-labeled design can estimate task discrimination or calibration. It cannot establish
effectiveness or harm reduction. Those claims additionally require a named H endpoint and a
comparative intervention design, for example

\[
\Delta_H
= \mathbb{E}[H \mid \text{intervention}]
- \mathbb{E}[H \mid \text{comparator}],
\]

with the sign interpreted from the preregistered endpoint definition.

### 3.3 Evidence presently available

- R-loader+ selection for the positive proxy class, with transaction-time R and W, S, A, C,
  P, Y, and H unknown unless reconstructed separately;
- public-chain transaction histories for sampled addresses;
- candidate graph, value, and timing features;
- synthetic scenarios generated by the detector authors;
- a locally reported corrected modest ranking signal on the registry-proxy task, pending an
  immutable run manifest;
- official documentation that constrains ERC-8004 and OpenClaw interpretations.

### 3.4 Inferences presently made but not identified

- registry association implies a working autonomous agent;
- counterparties are human-controlled;
- observed USDC transfers were initiated by an agent;
- registry discrimination is a precondition for fraud detection;
- synthetic motif detection transfers to adaptive fraud;
- graph and timing patterns are unavoidable agent signatures;
- public-chain results transfer to banking systems.

### 3.5 Critical unknowns

- current historical `agentWallet` state at each transaction timestamp;
- endpoint availability and service use at each timestamp;
- P evidence separating person/human, script, agent, or contract control of each address;
- mandate and authorization state;
- autonomous versus human-approved initiation;
- A2A purpose and service-delivery outcome;
- fraud outcome and loss;
- target-population prevalence;
- cross-chain and institutional transfer;
- decision cost, review capacity, and harm from false positives.

---

## 4. Replacement mechanistic explanation and causal boundary

### 4.1 Hardened thesis

> Fraud models that place material predictive weight on embodiment-dependent features may
> undergo calibration or error-rate shift when execution is delegated to autonomous
> software. The shift is not caused by “software nature” alone; it depends on the principal,
> mandate, runtime, authorization, settlement, service, and adversary regime. Models that
> observe decision-time context may or may not recover performance; recovery is a separate
> empirical claim.

### 4.2 Scoped hypothesis contract

AEF-C013 is a research-program hypothesis, not a free-floating existential claim. Every
test must allocate the next never-reused `AEF-C013-T###` child ID before data or outcome
inspection, enter it in the all-results registry in `GPD/CLAIM-LEDGER.md`, and fix this tuple:

\[
T_k=(f_k, y_k, p_k, r_k, t_k, o_k, L_k, \delta_k),
\]

where \(f\) is the frozen model/version, \(y\) the fraud class, \(p\) the target population,
\(r\) the execution regime, \(t\) the time window, \(o\) the operating point, \(L\) the
primary loss, and \(\delta\) the minimum operationally material degradation. A null in one
tuple rejects that scoped hypothesis; it cannot be rescued by switching model, outcome, or
regime. One positive tuple does not establish a universal agentic-fraud effect. The registry
must also fix the preregistration artifact and hash, creation time, primary or family role,
comparator, required evidence coordinates, sampling and split plan, estimator, confidence or
equivalence rule, power and sample-size target, and multiplicity policy. Initiated null,
failed, and abandoned tests remain visible under a run-outcome field separate from claim
status.

Contextual recovery must be registered as a separate comparison with its own loss and
materiality margin. It is not implied by finding degradation.

### 4.3 Why each detail is load-bearing

1. **A model must actually rely on embodiment-dependent features.** If it does not, the
   proposed mechanism cannot explain a performance shift.
2. **Execution must be verified as autonomous.** Registry ownership or protocol use alone
   cannot identify the treatment.
3. **A fraud outcome must be observed.** Otherwise the study measures actor or registry
   attribution rather than financial harm.
4. **The execution regime must change the feature–outcome relation.** Mere marginal feature
   shift is insufficient if calibration and discrimination remain stable.
5. **Any claimed repair must add decision-time information.** If a locked context-aware
   model adds no calibration or decision value, that scoped repair claim is rejected.

Removing any of these conditions changes or destroys the explanation. That makes the new
thesis harder to vary than the original nine-item account.

### 4.4 Primary estimands

The quantities below are **transport gaps**, not causal effects. A claim that execution mode
caused a shift requires a target-trial or DAG specification covering eligibility, treatment,
time zero, outcome, estimand, exchangeability, positivity/overlap, time-varying treatment,
interference among agents, negative controls, and sensitivity analysis. Prefer a randomized
or paired crossover holding principal, task, service, asset, and policy fixed.

Use \(Z_{pre}\) for confounding control. Do not adjust for \(Z_{post}\) when estimating the
total causal effect: runtime, authorization, or settlement variables may be mediators.
Those variables may enter a predictive repair model only if they exist at the decision time
and are audited for post-outcome leakage. An observational human-versus-agent comparison may
establish a deployment-domain gap; it must not silently become a causal effect.

For a human-controlled domain \(D_H\) and verified-autonomous domain \(D_A\):

\[
\Delta_{\mathrm{ECE}}
= \mathrm{ECE}(f;D_A)-\mathrm{ECE}(f;D_H),
\]

\[
\Delta_{\mathrm{FPR}}
= \mathrm{FPR}(f;D_A)-\mathrm{FPR}(f;D_H),
\qquad
\Delta_{\mathrm{FNR}}
= \mathrm{FNR}(f;D_A)-\mathrm{FNR}(f;D_H).
\]

The repair estimand compares a human-calibrated baseline \(f(X)\) with a context-aware model
\(g(X,Z_{pre},Z_{post}^{decision})\) on a locked autonomous holdout:

\[
\Delta_{\mathrm{repair}}
= L(f;D_A)-L(g;D_A),
\]

where \(L\) is preregistered and should include calibration and decision cost, not only ROC-AUC.

### 4.5 Decisive null result

If the preregistered primary loss remains within \(\delta_k\), or the interval excludes the
registered material degradation after the specified adjustment, that scoped hypothesis is
rejected. The result may not be moved to another metric or regime. The correct conclusion is
that the frozen method transfers adequately for the registered tuple, within its uncertainty.

---

## 5. Causal stack

The research should model a transaction as a causally ordered stack rather than as a property
of an abstract “agent.”

| Layer | State or transition | Key questions | Candidate evidence |
|---|---|---|---|
| 1. Principal | Human or legal entity supplies objective and bears authority/accountability | Who controls the system and bears loss or duty? | KYC/KYB, ownership, organization, beneficial controller |
| 2. Mandate | Scope, budget, asset, counterparty, time, and revocation constraints | What was the agent allowed to do? | Signed mandate, policy version, spend limits, allowlists |
| 3. Runtime | Model, prompt, memory, tools, dependencies, and execution environment | Was intent corrupted or tooling compromised? | Attestation, prompt/tool logs, dependency provenance, policy decisions |
| 4. Credential and wallet | Key custody, signer policy, nonce, approval, authentication intent | Who or what could authorize state change? | Wallet policy, signature provenance, key attestation, approval event |
| 5. Settlement | Transaction propagation, inclusion, finality, fees, chain or rail | What value-changing state transition occurred? | Signed transaction, RPC trace, ledger event, finality record |
| 6. Counterparty and service | Discovery, negotiation, delivery, dispute, refund | Was a real service requested and delivered? | Agent card, invoice, receipt, result hash, service proof |
| 7. Task adjudication (Y) | Task-specific fraud, attempted fraud, laundering, market abuse, or legitimate conduct | What financial-crime label is independently supported? | Case file, investigator decision, typology evidence, external evidence |
| 8. Harm and intervention (H) | Realized loss, prevented loss, recovery, review cost, alert action, blocking, remediation | What harm or intervention endpoint was measured, when, and by whom? | Ledger/account loss, recovery record, action log, review time/cost, counterfactual design |

### 5.1 Cross-layer attack principle

A complete attack explanation identifies:

1. the compromised or abused layer;
2. the trust boundary crossed;
3. the authorization state before and after the action;
4. the value-changing transition;
5. the observable emitted at each plane;
6. the Y task outcome and any separately measured H harm/intervention outcome;
7. the control that could prevent or detect it.

An API capability without this bridge is not a financial attack chain.

---

## 6. Actor roles

| Role | Definition | Must not be conflated with |
|---|---|---|
| Principal | Human or legal entity that defines goals and authority | Runtime process or wallet address |
| Agent runtime | Software that reasons, plans, or calls tools | Legal customer, signer, or fraudster |
| Orchestrator | System coordinating sessions, agents, or jobs | Settlement rail |
| Wallet / key custodian | Component controlling signatures and spend policy | Identity NFT owner or service endpoint |
| Service provider | Entity delivering data, computation, goods, or execution | Payment recipient without service evidence |
| Counterparty | Address or entity interacting financially | Human by default |
| Settlement network | Chain, bank rail, processor, or ledger applying state transitions | Agent platform |
| Attacker | Party exploiting prompt, runtime, credential, mandate, counterparty, or market | Agent merely because it is software |
| Monitoring institution | Bank, exchange, wallet provider, protocol, or investigator | Universal observer of every plane |
| Adjudicator | Independent role determining fraud outcome | Model prediction or registry label |

The same entity may occupy several roles, but the evidence must say which role is observed.

---

## 7. Observation planes

| Plane | Observable examples | Present in current study? | Consequence |
|---|---|---:|---|
| Identity / reputation | Registry owner, current wallet, metadata, endpoint, reputation | Partial: owner/mint proxy | Cannot infer autonomy or conduct |
| Control / session | Prompt, message, tool call, policy decision, session visibility | No | Cannot validate OpenClaw attack mechanism |
| Authorization / custody | Mandate, approval, signer, wallet policy, key attestation | No | Cannot distinguish authorized, compromised, or autonomous execution |
| Transaction / settlement | Sender, recipient, amount, token, time, graph, finality | Yes, public-chain subset | Supports transaction-feature analysis only |
| Service delivery | Request, invoice, result, receipt, dispute | No | Cannot establish commerce or payment–service abuse |
| Institutional / off-chain | Customer, account, fiat flows, alerts, cases, losses | No | Cannot establish banking performance |
| Task adjudication (Y) | Financial-crime label, typology, reviewer evidence, outcome time | No | Cannot estimate fraud-task discrimination or calibration |
| Harm / intervention (H) | Realized or prevented loss, recovery, action, review cost, intervention assignment | No | Cannot estimate effectiveness or harm reduction |

### 7.1 Observation-plane rule

A detector can only claim to detect a mechanism if its input contains an observable caused
by that mechanism. API enumeration cannot be validated by injecting an unrelated transaction
motif unless the causal mapping between the two is measured.

---

## 8. Regimes of validity

| Regime | Control pattern | Expected feature behavior | Research implication |
|---|---|---|---|
| R0 Manual human | Human initiates and approves each action | Human interaction and timing features may be informative | Baseline only; not universal human truth |
| R1 Scripted automation | Deterministic or scheduled software under fixed rules | High regularity or throughput is possible without AI | Separates automation from autonomy |
| R2 Supervised agent | Agent proposes; human or policy approves | Mixed human/software signals | Attribution requires approval telemetry |
| R3 Bounded autonomous agent | Agent acts within signed mandate, budgets, and allowlists | Machine cadence with strong authorization context | Primary safe evaluation regime |
| R4 Open autonomous agent | Broad tool and wallet authority | Larger control and compromise surface | Requires custody and mandate evidence |
| R5 Coordinated multi-agent system | Multiple runtimes share objective or controller | Population effects may exceed per-address evidence | Requires group/window unit of analysis |

Results from one regime must not be generalized to another without a transfer test.

### 8.1 On-chain versus banking regime

Public-chain data expose settlement but usually omit customer identity, mandate, service
delivery, and adjudication. Banking systems observe more customer and case context but may not
observe agent runtime state. These are complementary observation regimes, not substitutes.

### 8.2 Throughput convention

For a named rail, end-to-end financial throughput is bounded by the slowest required stage:

\[
\lambda_{\mathrm{settle}}
\leq \min(
\lambda_{\mathrm{orchestration}},
\lambda_{\mathrm{policy}},
\lambda_{\mathrm{credential\ authorization}},
\lambda_{\mathrm{payment\ instruction}},
\lambda_{\mathrm{rail\ acceptance}},
\lambda_{\mathrm{clearing/settlement}}
).
\]

The required stages and capacities must be instantiated for the rail. EVM execution may use
signing, nonce, RPC, inclusion, and finality; institutional rails may instead use payment
instruction validation, sanctions/fraud controls, acceptance, clearing, posting, and
finality. Message-return latency cannot be substituted for settled-transaction throughput.

---

## 9. Necessary constraints versus contingent features

### 9.1 Causally necessary constraints in a state-changing payment

Within a specified settlement protocol, the useful “physics-like” constraints are:

- valid authorization or successful exploitation of an authorization boundary;
- credential or key use sufficient to cause the state change;
- ordered state transition with nonce, replay, or idempotency semantics;
- conservation or accounting of value within the observed ledger boundary;
- protocol fees, balances, limits, and finality rules;
- a causal trace from objective or compromise to action and outcome, if the relevant planes
  are instrumented.

These constraints follow from the mechanism. They do not identify fraud by themselves.

### 9.2 Contingent, evadable, or non-exclusive features

- high velocity;
- low-value micropayments;
- graph hubs, fans, cycles, or chains;
- low or high timing variance;
- multi-chain presence;
- lack of circadian rhythm;
- device, IP, or geographic stability;
- identity age or persistence;
- apparent economic optimality.

These may be useful predictors in a defined population. They are not universal invariants of
agents or fraud.

---

## 10. Financial-crime outcome taxonomy

Actor type, task outcome, and harm/intervention outcome must be labeled separately. The table
below defines Y. H is a distinct measured endpoint and must not be inferred from Y: a
task-positive case may cause no realized loss, while an intervention may impose review cost
or prevent harm.

| Outcome class | Minimal outcome evidence | Relevant planes |
|---|---|---|
| Unauthorized wallet use | Signature or transfer outside valid authority, plus controller evidence | Mandate, custody, settlement, adjudication |
| Compromised-agent execution | Runtime/tool compromise causally linked to unauthorized action | Control, runtime, custody, settlement |
| Mandate abuse | Formally authorized action violates principal intent, duty, or policy | Principal, mandate, service, adjudication |
| Service/payment deception | Payment or service result is withheld, falsified, or misrepresented | Service delivery, settlement, dispute |
| Laundering/layering | Illicit-source or concealment evidence across transactions/cases | Settlement, institutional, adjudication |
| Market abuse | Manipulative intent/conduct and market-effect evidence under applicable rules | Control, market, settlement, adjudication |
| Coordinated fraud | Common controller/objective and joint harmful outcome | Control, population, settlement, adjudication |
| Identity/reputation manipulation | False identity or feedback used to induce reliance or evade controls | Identity, reputation, service, outcome |

Transaction shape alone is normally insufficient for Y adjudication. Claims about loss,
prevention, recovery, or operational effectiveness additionally require H measurement.

---

## 11. Hard-to-vary stress test

### 11.1 Why the original explanation fails

| Variation | Observed results change? | Verdict |
|---|---:|---|
| Remove biometrics, geography, and device fingerprinting | No current empirical result changes | Details are not load-bearing |
| Replace “AI agents” with “registry-associated or automated wallets” | Stage-2 data and ranking remain | The narrower explanation fits better |
| Replace OpenClaw with a generic scheduler | Injected transaction motifs remain | Platform detail is not causal in the experiment |
| Replace “fraud” with “registry-proxy discrimination” | Stage-2 evidence remains | Fraud interpretation is not identified |
| Permit hardware-bound, rate-limited, stochastic, identity-persistent agents | Claimed necessity disappears | Nine invariants admit counterexamples |

### 11.2 Falsifiers for the replacement thesis

The following falsifiers apply to each preregistered \(T_k\). A null rejects that tuple; it
does not permit a post-hoc move to another regime. The broad research program remains a set
of open scoped hypotheses, not a claim that one favorable regime must exist:

1. models using embodiment-dependent features show no meaningful calibration or error-rate
   shift on verified-autonomous, fraud-labeled activity;
2. any shift disappears after ordinary covariate matching and is explained by protocol,
   service, or sampling artifacts;
3. a separately locked context-aware repair does not improve the preregistered loss beyond
   its materiality margin on an autonomous holdout;
4. agent execution is not a stable or measurable treatment because human approval dominates;
5. fraud outcomes are too sparse or ambiguous to distinguish the proposed regimes;
6. simple established AML baselines match or outperform the proposed architecture.

### 11.3 Predictions that would support it

Support for one scoped child claim requires all of the following in a locked study:

- verified separation of execution regimes;
- adjudicated fraud outcomes;
- measurable degradation of a human-calibrated baseline in at least one autonomous regime;
- a locked EXP-3B intervention attributing any claimed embodiment mechanism rather than
  relying on post-hoc error analysis;
- improved calibration or cost from context-aware features on held-out entities and time,
  if a separate repair child claim was registered.

---

## 12. Decisive experiments

### EXP-1 — Evidence-coordinate reconstruction

**Question:** For each evaluated address or transaction, which of R, W, S, A, C, P, Y, and H
is supported, negated, unknown, or not applicable, and which combinations actually occur?

**Design:**

1. preserve address and transaction timestamps;
2. reconstruct ERC-8004 ownership and `agentWallet` state by block;
3. resolve registration metadata as it existed at the relevant time;
4. retain contemporaneous endpoint evidence where it exists; otherwise measure current
   reachability separately with dated, reproducible rules and mark historical reachability
   unknown;
5. separate EOAs, contracts, services, and known infrastructure;
6. record each coordinate independently without imputing one from another.

**Primary outputs:** coordinate marginals, co-occurrence matrix, missingness patterns,
temporal validity, concentration by owner, and sensitivity analyses. Do not use an attrition
funnel, because the coordinates are not ordered prerequisites.

**Decision gate:** If A+ cannot be established for the relevant transactions, retire “real
agent transactions” and retain “registry-associated addresses” throughout. S+ or W+ alone
does not substitute for A+.

### EXP-2 — Three-regime actor-provenance benchmark

**Question:** Can features distinguish verified human control, scripted automation, and
verified autonomous execution?

**Design:** Build matched R0/R1/R3 cohorts with entity-group and temporal splits. Match chain,
asset, service type, activity, account age, and value scale. Use provenance evidence rather
than behavioral circularity for labels; R0 requires P+ rather than a counterparty proxy.

**Primary metrics:** macro-F1, classwise precision/recall, calibration, abstention coverage,
and robustness across services.

**Falsifier:** Performance collapses under entity/time holdout or is entirely explained by
service/protocol tags.

**Interpretation limit:** Even success validates actor-provenance classification, not fraud.

### EXP-3 — Human-to-autonomous fraud-model transfer

**Question:** Do outcome-labeled fraud models degrade under verified autonomous execution?

**Design:** Train a baseline on adjudicated R0 activity, freeze it, and evaluate on matched
R2/R3/R4 fraud-labeled activity. Compare against ordinary automation and against a model
augmented with decision-time \(Z_{pre}\) and eligible \(Z_{post}\) context. Predefine fraud
class and exclude post-outcome leakage. This
primary design estimates transport, not causation. Where safe and feasible, add a paired
controlled study that randomly assigns the same principal, task, service, asset, and policy
to human or autonomous execution. Keep that controlled result separate from real-world
prevalence and effectiveness estimates.

Before data inspection, register \(T_k\), its stable child claim ID, materiality margin, and
primary loss. For a causal sub-study, publish the target-trial/DAG specification and test
overlap, negative controls, time-varying execution mode, and cross-agent interference. Use
only pre-execution covariates for total-effect adjustment; audit decision-time telemetry
separately as a predictive repair.

**Y-based task metrics:** PR-AUC at target prevalence, ROC-AUC, Brier score, ECE, and
classwise FPR/FNR against independently adjudicated Y.

**H-based effectiveness metrics:** Realized loss, prevented loss, recovery, review workload,
action cost, and other preregistered endpoints only where H is measured. These require a
separate effectiveness child claim and comparative intervention design; predicted scores or
Y labels cannot substitute for H.

**Decisive transport result:** The frozen baseline degrades beyond the registered
materiality margin on the locked autonomous holdout.

**Decisive repair result:** A separately registered repair child improves its locked loss
beyond its own margin on the same eligible holdout. Transport degradation can be supported
when repair fails, and repair cannot be inferred from degradation.

**Decisive harm-reduction result:** A separately registered effectiveness child shows a
material improvement in its H endpoint under a design with Y and H evidence. Predictive
repair does not by itself establish harm reduction.

**Null:** No operationally meaningful degradation. Publish the null and withdraw the
structural-failure thesis for that regime.

### EXP-3B — Embodiment-mechanism intervention

**Question:** Is any registered transport gap actually carried by the claimed
embodiment-dependent features rather than by protocol, service, population, or collection
proxies?

**Operational classification rule:** A candidate is embodiment-dependent only when its
preregistered causal provenance requires a human biological, sensorimotor, or cognitive
process rather than merely an actor label, protocol, service, or collection pipeline. It is
verified as embodiment-dependent for a scoped study only if a controlled executor-mode
intervention changes it beyond a declared margin while principal, task, service, asset,
protocol, and policy are held fixed. Two independent reviewers classify features before
outcome access; disagreements and features that cannot be intervened on enter an ambiguous
stratum and cannot support the mechanism claim.

**Design:** Before outcome inspection, create feature-level provenance recording source,
availability time, transformation, missingness, classification, and independent review.
Lock three comparisons: the full frozen model; an ablation removing the verified
embodiment-dependent features; and a counterfactual-harmonization test that equalizes or
replays those features across R0 and the autonomous regime while preserving eligible
non-embodiment covariates. Compare against protocol-tag-only and service-tag-only baselines.

**Mechanism estimand:** The reduction in the registered transport gap after the locked
ablation or harmonization, with its own materiality margin and uncertainty interval.

**Falsifier:** The gap persists after embodiment-feature removal/harmonization, or is
explained equally well by protocol/service tags. In that case, embodiment does not explain
the scoped result even if a predictive transport gap exists.

### EXP-4 — Independent fraud adjudication study

**Question:** Which flagged and unflagged cases are actually fraudulent?

**Design:** Stratified, blinded sampling across score bands; two independent investigators;
predefined typology and outcome rubric; conflict adjudication; external evidence preserved;
reviewers blinded to model internals where feasible.

**Primary metrics:** inter-rater agreement, prevalence by stratum, precision with intervals,
false-positive typology, and adjudication uncertainty.

**Stop condition:** If reliable adjudication is not possible, do not estimate fraud
performance. Reframe as unsupervised risk discovery.

### EXP-5 — Independent adaptive red team

**Question:** Do candidate features survive plausible adaptive behavior?

**Design:** A team independent of detector authors generates attacks mixed into realistic
histories using empirical resampling, seeded pseudorandom timing, Hawkes or burst processes,
throttling, counterparty diversification, low-volume strategies, and benign automated
controls. Generators remain hidden until evaluation is locked.

**Primary metrics:** detection by unseen generator, FPR against legitimate automation,
attack-cost curves, and performance by history contamination level.

**Falsifier:** Hand-built-scenario performance fails to transfer to unseen adaptive
generators.

### EXP-6 — Population versus per-address detection

**Question:** Does a population-level model add value beyond per-address scoring?

**Design:** Compare the current per-address baseline with sliding-window transaction graphs,
activation correlation, amount synchronization, and community or subgraph methods. Split by
campaign/controller and time, not random transaction rows.

**Primary metrics:** campaign recall, address-level FPR, detection delay, alert volume, and
incremental value over established graph baselines.

**Falsifier:** Population models do not outperform simple per-address or established
subgraph baselines on held-out coordinated campaigns.

### EXP-7 — Control-to-settlement feasibility trace

**Question:** Which platform capabilities can actually cause a financial state change?

**Design:** In an isolated, no-real-funds environment, instrument the path from session
message through tool policy, delegated authority, credential or custody use, payment
instruction, rail acceptance, clearing or settlement, and retained audit log. Test denied,
allowed, revoked, and compromised-control cases. Instantiate rail-specific substeps: for an
EVM case, signer, nonce, RPC, inclusion, and finality; for an institutional rail, instruction
validation, control screening, acceptance, posting, clearing, and finality as applicable.

**Primary outputs:** causal trace, required permissions, latency distribution, audit
retention, and prevention points.

**Decision gate:** Only mechanisms reproduced end to end may be called platform-grounded
financial attack chains.

---

## 13. Baselines and validation principles

### Required baselines

- simple amount, count, age, and degree models;
- established transaction-graph and subgraph AML features;
- service/protocol-tag-only classifier;
- registry-membership or owner-concentration baseline;
- human-versus-automation baseline where actor provenance is studied;
- per-address versus population model comparison;
- calibrated logistic model before complex learners.

### Split discipline

- split by entity or principal, not transaction rows;
- use temporal holdouts after label and feature construction;
- keep owner-linked or controller-linked identities in one fold;
- ensure registry and metadata observations are time-correct;
- prevent counterparties shared across train and test from leaking graph structure;
- reserve at least one external chain, service, or institution for final validation.

### Metric discipline

- use PR-AUC and operating-point precision at realistic prevalence;
- report ROC-AUC only with intervals and task definition;
- report calibration, FPR/FNR, abstention, review volume, and expected cost;
- keep transaction-, address-, campaign-, and case-level metrics separate;
- publish thresholds only after target-population calibration;
- preserve null and negative results.

### Label discipline

- labels must represent the claimed construct;
- label uncertainty must remain explicit;
- registry evidence must not label fraud;
- model outputs must not be recycled as ground truth;
- investigator adjudication must be independent of score where feasible;
- Y must name the task-specific financial-crime outcome and its adjudication time;
- H must name the harm/intervention endpoint, unit, direction, measurement window, and
  provenance;
- neither Y nor H may be used as a prospective feature, and their observation times must be
  audited against the prediction time.

---

## 14. Failure modes and controls

| Failure mode | Why it matters | Required control |
|---|---|---|
| Registry-label circularity | Detects registration ecosystem rather than autonomy | Evidence coordinates and provenance audit |
| Human-negative contamination | Automation appears as false human ground truth | Multi-class control provenance and uncertainty |
| Outcome substitution | Agent identity is treated as fraud | Independent fraud adjudication |
| Harm substitution | Y labels or model scores are treated as prevented loss | Separate H measurement and comparative intervention design |
| Generator–detector circularity | Synthetic attacks restate feature definitions | Independent hidden red team |
| Entity leakage | Same principal or graph neighborhood appears in train/test | Grouped temporal splits |
| Post-outcome leakage | Investigation artifacts inflate predictive performance | Feature-time audit |
| Protocol confounding | Model identifies x402/USDC/service rather than behavior | Protocol-tag baseline and matched cohorts |
| Threshold shopping | Recall and FPR are optimized on the test set | Preregistered calibration and final holdout |
| Base-rate neglect | High AUC still produces unusable alerts | Prevalence-aware precision and cost |
| Platform misdescription | Threat chain lacks actual capability | Official docs and end-to-end trace |
| Categorical legal claim | Privacy duties vary by context | Deployment-specific legal analysis |
| Novelty gerrymandering | “Only work” is made true by excessive conjunction | Feature-level prior-art comparison |

---

## 15. Confidence by finding

| Finding | Confidence | Strongest anchor | Weakest remaining point |
|---|---|---|---|
| Stage 2 is not fraud detection | High | Label definition and absence of fraud outcome | None material for current task definition |
| Positive class is not verified autonomy | High | Loader plus PSE-001, PSE-009, PSE-010 | Exact historical wallet state still unmeasured |
| Counterparties are not verified humans | High | No human-control evidence | Actual composition unknown |
| OpenClaw chains are not directly derived as written | High | PSE-002–PSE-005 | A custom wallet integration could create a separate bridge |
| Nine-item taxonomy is not complete/necessary | High | Counterexamples and internal category mismatch | A narrower taxonomy could still be useful |
| Network topology has descriptive registry-proxy separation | Provisional and construct-limited | Preserved proxy-rank AUC 0.5990 | Other signals are near/below chance; corrected fusion, leakage, and transfer remain unresolved |
| A scoped domain-shift hypothesis will show material degradation | Unmeasured | Mechanistic plausibility only | No registered model/regime/outcome experiment |
| A scoped context-aware repair will improve fraud models | Unmeasured | Mechanistic rationale only | No separately locked repair experiment |
| Population detection will improve coordinated-fraud detection | Low-medium | Synthetic architecture gap and prior graph methods | No independent coordinated-fraud corpus |
| Banking deployment utility | Low | No institutional validation | Nearly all decisive evidence absent |

---

## 16. Open questions

1. Can historical `agentWallet` state be reconstructed at every evaluated transaction block?
2. How many registry owners transferred the identity token, and when?
3. Which registrations had valid metadata and reachable services during the evaluation
   window?
4. Can any transaction be linked to an authenticated autonomous execution trace?
5. What fraction of counterparties are contracts, exchanges, routers, relayers, bots,
   services, or human-controlled EOAs?
6. Which precise fraud outcome is the first target, and why is it decision-relevant?
7. Who can supply independent adjudication and external case evidence?
8. What is the target deployment population and expected fraud prevalence?
9. Which human-calibrated fraud model is available for a true transfer experiment?
10. Which features in that model genuinely depend on human embodiment rather than ordinary
    account, service, or protocol behavior?
11. Can principal and mandate identifiers be linked across addresses without violating
    privacy or creating leakage?
12. What observation planes would a bank, wallet provider, chain monitor, or agent platform
    actually control?
13. Which prevention controls eliminate risk before detection, and what residual risk remains?
14. How should legitimate high-frequency automation be represented in the negative class?
15. Can a fully independent red team and final holdout be funded and preserved?
16. What minimum evidence would justify moving any claim from exploratory to supported?

---

## 17. Recommended research sequence

1. **Freeze terminology and claims** using `GPD/CLAIM-LEDGER.md`.
2. **Run EXP-1** before further model tuning; label validity dominates algorithm choice.
3. **Choose one fraud outcome** and write an adjudication rubric before collecting features.
4. **Build EXP-2 controls** to separate human, automation, and autonomous execution.
5. **Acquire or construct outcome evidence** for EXP-3/EXP-4; if impossible, retain the
   registry-proxy scope.
6. **Run EXP-3B** before attributing any transfer gap to embodiment-dependent features.
7. **Reproduce established baselines** before proposing an agent-specific architecture.
8. **Run independent EXP-5 and EXP-6** only after labels, units, and operating points are
   locked.
9. **Use EXP-7** to rebuild platform-specific threat chains from actual causal traces.
10. **Attempt external validation** on a later time window and another chain or institution.
11. **Update claim statuses** only through the ledger’s change-control rule.

## 18. Stop-and-rethink conditions

Stop escalation toward a fraud-detector claim if:

- no A+ autonomous-execution evidence can be obtained for the relevant transactions;
- no independent fraud outcomes can be adjudicated;
- proxy performance disappears under grouped temporal validation;
- simple graph or protocol-tag baselines explain all apparent lift;
- the actor-provenance task has no decision value for the target institution;
- legal or privacy constraints prevent defensible linkage;
- adaptive red-team performance collapses at an operational FPR;
- the expected review burden exceeds available capacity or expected loss reduction.

In those cases, publish the work as a construct-validity and measurement study rather than
stretching it into a deployment claim.

---

## 19. Discovery conclusion

The project’s central objective is still valuable: financial systems need to understand
delegated and autonomous execution. The route to a rock-solid result is not a stronger
assertion that agents lack human biology. It is a more exact chain from principal and mandate
through runtime and authorization to settlement and adjudicated outcome.

The existing work supplies a useful starting artifact: a registry-proxy dataset, candidate
transaction features, a locally reported corrected ranking result pending immutable run
evidence, and a set of synthetic detector-path checks. The next scientific milestone is not
another threshold or taxonomy. It is A+ autonomy evidence joined to Y+/Y- outcome evidence
under a scoped design that can reject its hypothesis without switching regimes.
