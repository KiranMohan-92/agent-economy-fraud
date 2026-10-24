> [!CAUTION]
> **WITHDRAWN DRAFT (July 2026): Stage 1 results are withdrawn; see
> [README](../README.md) and [GPD/CLAIM-LEDGER.md](../GPD/CLAIM-LEDGER.md).
> Kept for the record.**

# Registry-Associated Wallet Ranking in Early ERC-8004 Data

## A construct audit and agentic-payment threat model

Kiran Mohan — Independent Researcher  
Research-integrity revision: 9 July 2026

> **Status:** This revision supersedes the earlier submission-ready claim. It
> is a construct audit and research protocol, not a validated fraud detector,
> bank study, adversarial-robustness result, or deployment guide.

## Abstract

This paper audits a prototype originally described as an agentic-fraud
detector. Its real-data labels do not encode fraud, autonomous execution, or
human control. The positive class contains 665 historical ERC-8004 registry
owner/default-wallet proxies and the comparison class contains 1,069 active
counterparties of unknown type. On the retained local snapshot, the original
composite ranks these classes at ROC-AUC 0.514719. A full-sample, post-hoc
reweighting reaches 0.622281; five-fold random-address cross-fitting gives
pooled out-of-fold AUC 0.612179, and a logistic combiner gives 0.650263. These
corrected results are provisional until preserved in an immutable end-to-end
run manifest; only the historical 0.514719 is reproduced by the preserved audit.
They also remain exploratory because feature design, graph construction,
cohort cleaning, and model selection were informed by the same connected
population. At a training-fold threshold selected for a nominal 5% comparison-
class rate, held-out proxy recall is 7.52%, proxy precision 48.08%, F1 13.00%,
and unknown-counterparty alert rate 5.05%.

The audit finds two decisive provenance defects. A historical bridge
deduplicated ERC-20 events by transaction hash, discarding 13,539 of 107,118
rows, including 10,626 distinct transfer-event tuples. The synthetic motif
generator also reused attacker addresses across instances; correcting it
changes 82 historical attack senders to 689 and invalidates every reported
motif-performance metric. A separate synthetic benchmark lacks its generator,
row-level scores, and benchmark log and is withdrawn. None of these artifacts
supports fraud accuracy, banking generalization, adversarial robustness, or an
operational threshold.

We replace the easy-to-vary claim that agents are intrinsically fraudulent
with a causal explanation: loss becomes possible when the chain from an
authenticated controller and bounded mandate, through instruction provenance
and tool/wallet authorization, to settlement is not preserved. Automation
changes speed, scale, delegation depth, and coordination; it does not turn
actor type into fraud. The repaired contribution is an explicit evidence
vector, threat-role and observation-plane model, claim ledger, fail-closed
research score, and preregisterable validation design.

## 1. The actual research objective

The original project asked how agents break assumptions in banking fraud
detection. That wording presupposed both the existence and completeness of
“human behavioral invariants” and a causal banking gap. The available evidence
cannot test either proposition.

The repaired objective is:

> Determine which facts can be established from registry and transaction
> evidence; explain where delegated software execution creates preventable
> loss mechanisms; and specify the observations and experiments required to
> test attribution, control failure, fraud, AML, and market-abuse hypotheses
> without conflating them.

This objective preserves what matters—agentic execution changes control and
response requirements—while removing the unsupported inference `agent = fraud`.

## 2. First principles and the hard-to-vary explanation

### 2.1 Necessary causal chain

An agent cannot settle value merely because it can exchange messages. A
financial action needs a causal path:

```text
legal/accountable principal
  -> bounded mandate
  -> authenticated instruction and provenance
  -> agent/runtime decision
  -> tool authorization
  -> wallet/key policy and signature
  -> payment rail, nonce and inclusion
  -> settlement/finality
  -> counterparty or victim consequence
  -> case/outcome evidence
```

Every link has a distinct trust boundary and observable. Messaging APIs can
support orchestration, but they do not by themselves prove wallet creation,
signing authority, balances, policy bypass, transaction inclusion, or harm.

### 2.2 Hard-to-vary thesis

> Financial loss becomes possible where the chain from controller intent and
> mandate, through instruction provenance and tool/wallet authorization, to
> settlement is not cryptographically and operationally preserved.
> Automation can amplify speed, scale, delegation depth, and coordination; it
> does not make actor type fraudulent. Controls must bind actions to an
> authenticated controller and bounded mandate, enforce least privilege and
> payment limits, preserve provenance, and monitor value, counterparty, and
> graph outcomes independently of executor substrate.

Each term does explanatory work:

- If mandate, provenance, and authorization remain intact, fast and 24/7
  execution can be legitimate.
- If they fail, unauthorized risk exists whether execution is by a person,
  script, compromised application, or language-model agent.
- Speed and scale change loss accumulation and response time, not the legal or
  factual definition of fraud.
- The thesis predicts evidence at specific control points and can be falsified
  by showing that loss occurs with every link intact, or that breaking a link
  does not change unauthorized-loss risk under controlled conditions.

The earlier nine “human invariants” fail this standard. They mix biological
constraints, authentication methods, telemetry, legal identity, and empirical
hypotheses. Removing biometrics, geography, or device fingerprints leaves the
existing experiment unchanged. Replacing “AI agent” with “registry-associated
wallet” makes the experiment more accurate without changing a row. Those
details were therefore easy to vary and could not carry the explanation.

### 2.3 Physics-style constraints versus behavioral regularities

Unavoidable constraints in a digital payment system include authorization,
key custody, budgets or value conservation, nonces/order, network capacity,
settlement, and irreversible or costly state transitions. Transaction volume,
hub structure, low amounts, timing regularity, and 24/7 activity are contingent
regularities. Legitimate automation can exhibit them; a patient adversary can
avoid them. They can be useful features but not necessary signatures.

## 3. Construct and evidence audit

### 3.1 Evidence vector

Evidence dimensions are independent, so they must not be treated as a maturity
ladder.  For each address, event, or case we record
`{R,W,S,A,C,P,Y,H}`: registry record, current verified wallet association, live
service, authenticated autonomous-execution trace, commerce/payment chain,
independently verified person/human control, independently adjudicated
task-specific financial-crime outcome, and measured harm or intervention
outcome. Each dimension is `present`, `absent`, or `unknown`, with source and
time.  A claim must name the exact conjunction it requires, and requirements are
claim-specific. For example, registry association requires `R`; current
wallet-control association requires `W`; observed autonomous execution requires
`A` (authenticated execution provenance with time-correct address or wallet
linkage), adding `W` or `S` only when the scoped mechanism depends on them; a
delegated-payment claim additionally requires `C`; a verified-human comparison
requires `P`; task-specific fraud evaluation requires `Y`; and effectiveness or
harm-reduction claims require `Y+H`. No component implies another.

The Stage 2 snapshot supplies only `R-loader+` evidence for the proxy cohort
(selection through the loader's owner/mint-recipient relation), not
transaction-time `R+`, and leaves `W,S,A,C,P,Y,H` unknown. Registration does not guarantee a
functional or non-malicious service. ERC-8004 also treats `agentWallet` as
separate state: it begins as the owner, changes require proof, and it is cleared
on identity-token transfer. A historical owner or mint recipient is therefore
not a guaranteed current wallet, much less an autonomous executor.

### 3.2 What was actually labeled

The retained label artifact contains:

- 665 `registry_owner_proxy` addresses; and
- 1,069 `counterparty_unknown` addresses.

Unknown counterparties can be people, contracts, exchanges, bridges, routers,
bots, relayers, or unregistered agents. Calling them “human” makes precision,
specificity, false-positive rate, and calibration claims invalid. Filtering
thin counterparties changes the selected population; it does not clean unknowns
into verified humans.

### 3.3 Four tasks that must remain separate

1. **Registry/automation attribution:** verified human, service, contract,
   exchange, generic automation, verified autonomous agent, or unknown.
2. **Agent control-plane security:** mandate escalation, instruction injection,
   provenance breaks, tool abuse, key theft, and policy bypass.
3. **Fraud/scam detection:** independently adjudicated unauthorized or
   deceptive loss, with customer, beneficiary, case, and intervention outcomes.
4. **AML/market-abuse surveillance:** separate suspicion/manipulation labels,
   entity resolution, graph or order-book data, legal hypotheses, and
   investigator outcomes.

Attribution can support segmentation, but it is not logically necessary for
actor-agnostic fraud controls. An institution can detect an unauthorized
payment without proving whether a person, script, or AI agent executed it.

## 4. Threat model

### 4.1 Roles

The minimum role model is:

- accountable principal/controller;
- delegated agent or ordinary automated process;
- runtime/orchestrator and model provider;
- tool or plugin provider;
- wallet, key custodian, and payment service;
- legitimate or malicious counterparty;
- compromised agent/wallet as victim;
- human or organizational victim;
- investigator, institution, and regulator.

“Agent attack” is too coarse. A malicious controller using a correct agent, a
compromised legitimate agent, and colluding counterparties have different
controls and evidence.

### 4.2 Observation planes

| Plane | Relevant evidence | Examples of hypotheses |
|---|---|---|
| Control | instruction, session, model/tool call, provenance, policy decision | injection, enumeration, privilege escalation |
| Wallet/authorization | mandate, scope, key event, signature, limit, nonce | unauthorized signing, key theft, policy bypass |
| Settlement | transaction event, rail, amount, beneficiary, finality | unauthorized transfer, scam payment, rapid extraction |
| Entity/network | ownership, funding, counterparties, cross-chain resolution | laundering, Sybil control, coordinated value movement |
| Market | orders, trades, price impact, venue and beneficial ownership | wash trading, manipulation |
| Outcome | claim, victim, case, disposition, proceeds, intervention | fraud/legitimate, suspicious/not suspicious, harm avoided |

A transfer-only detector cannot validate control-plane enumeration or history
access. A low-value cross-chain proxy cannot validate cross-chain identity. A
transfer graph alone cannot establish market manipulation without trade,
ownership, and price-impact evidence.

### 4.3 Scenario schema

Every future scenario must specify:

`role -> precondition -> trust boundary -> action -> asset -> authorization
state -> victim/harm -> observable plane -> benign twin -> control -> evasion ->
ground-truth source`.

Without that chain, an item is a motif or risk hypothesis—not a fraud attack
validated by data.

## 5. Research score

The code retains four active transaction-feature families: economic heuristics
(ER), network topology (NT), value flow (VF), and temporal consistency (TC).
Cross-platform correlation is inactive. These are established descriptive
feature families with benign and malicious counterexamples, not “agent
invariants.”

The fail-closed default is an untuned reference average:

```text
S0 = 0.25 ER + 0.25 NT + 0.25 VF + 0.25 TC
```

For forensic comparison only, the code exposes the post-hoc exploratory rule:

```text
S_exp = 0.1116 ER + 0.7269 NT + 0.1615 VF
```

The latter uses positive full-sample values of `AUC_i - 0.5`. It is not a
confirmatory model because the same population selected and evaluated the
weights. The historical threshold `0.09` is retained only to reconstruct old
reports. There are no `ALLOW`, `INVESTIGATE`, or `BLOCK` tiers.

## 6. Empirical audit

### 6.1 Stage 1 — withdrawn

The repository lacks the synthetic generator, generated rows, row-level scores,
and latency harness. From the stated confusion matrix (`TP=9,623`, `FN=377`,
`FP=2,062`, `TN=87,938`):

| Metric | Positive class | True macro average |
|---|---:|---:|
| Precision | 82.353% | 90.963% |
| Recall | 96.230% | 96.969% |
| F1 | 88.753% | 93.692% |

The reported 88.71% was approximately positive-class F1, not macro F1. One
confusion matrix cannot reconstruct ROC-AUC 0.97. The 97 ms latency is
unsupported. Stage 1 is withdrawn until the exact generator, seed, rows,
scores, environment, and timing harness are released.

### 6.2 Stage 2 — exploratory registry-proxy ranking

Independent recomputation from the retained local artifacts gives:

- `N=1,734`: 665 registry proxies and 1,069 unknown counterparties;
- historical composite ROC-AUC `0.51471898`;
- at historical reference `0.09`: `TP=539`, `FP=718`, `FN=126`, `TN=351`;
- per-feature AUC: ER `0.515167`, NT `0.599050`, VF `0.522026`, TC `0.464749`;
- post-hoc full-sample AUC `0.622281`, nominal address-bootstrap 95% interval
  `[0.5951, 0.6494]`;
- random-address cross-fit pooled AUC `0.612179`; fold mean `0.614406`, SD
  `0.037857`;
- random-address cross-fit logistic AUC `0.650263`, nominal interval
  `[0.6227, 0.6778]`.

Only the historical composite AUC is reproduced by the preserved audit artifact
(`GPD/verification/research-audit-results.json`). The corrected (post-hoc,
cross-fit, and logistic) results are provisional until preserved in an immutable
end-to-end run manifest with revision, data hashes, cohort and split, seed,
command, environment, and output checksum (claim AEF-C006).

These are optimistic exploratory estimates. Feature design and model selection
used the dataset; the graph was computed before splitting; random addresses
share transactions/components; cohort cleaning and thresholds were selected on
the same population. An address bootstrap does not capture these dependencies.

When the threshold targeting a nominal 5% comparison-class rate is selected in
each training fold, held-out proxy recall is 7.52%, proxy precision 48.08%, F1
13.00%, and unknown-counterparty alert rate 5.05%. “FPR” is deliberately not
used because the comparison class is not verified negative ground truth.

### 6.3 Event-loss defect

The historical raw CSV contains 107,118 rows and 93,579 unique transaction
hashes. Deduplicating by hash discarded 13,539 rows (12.64%). Only 2,913 were
exact duplicates. The remaining 10,626 discarded rows were distinct
transfer-event tuples across 8,321 multi-event transaction hashes.

The repaired SQL carries `evt_index`; the bridge deduplicates on
`(tx_hash, evt_index)` (plus chain when applicable) and refuses a source without
event identity. Existing parquet and metric artifacts remain invalid and must
be regenerated from an immutable bounded query.

### 6.4 Stage 3 — stale motif sensitivity

The eight injected patterns were designed from the detector's own hypotheses
and do not independently generate authorization failures, deception, victim
harm, money laundering, or market manipulation. The old generator also reused
addresses because its address hash omitted `instance_id`.

| Motif | Old interpretation | Corrected unique senders |
|---:|---|---:|
| 1 | enumeration-like dust | 10 |
| 2 | history-extraction-like repetition | 10 |
| 3 | async-flood-like burst | 5 |
| 4 | disposable-address fan-out | 150 |
| 5 | cross-platform proxy | 10 |
| 6 | periodic mimicry | 8 |
| 7 | distributed swarm | 440 |
| 8 | circular/wash-like flow | 56 |
| **Total** | hand-authored transaction motifs | **689** |

The historical artifact contains 82 unique senders. Every old Stage 3 score,
AUC, recall, and threshold result is stale. Real comparison addresses are also
unlabeled; their above-threshold fraction is an unlabeled alert rate, not a
false-positive rate. A corrected rerun can establish only code sensitivity to
the programmed motifs.

The old “mimicry paradox” also does not generalize. Its generator deliberately
used nearly identical intervals and amounts. A stochastic policy can sample a
target distribution. The bounded finding is only that this periodic generator
has very low timing variation and is detectable by the chosen heuristic.

## 7. Confirmatory research program

### 7.1 Dataset and label contract

A valid replacement must publish or escrow:

- chain, contract, exact versioned SQL/query ID, extraction time, and inclusive
  start/exclusive end block or timestamp;
- event identity `(chain, tx_hash, evt_index)` and raw/derived schema;
- address/entity inclusion flow and post-registration observation window;
- registry owner, current verified wallet, live endpoint, signed mandate,
  execution trace, settlement, and outcome evidence as separate fields;
- explicit `unknown` class, source, confidence, reviewer, and timestamp;
- exclusions, license, privacy controls, file sizes, and SHA-256 hashes.

### 7.2 Leakage-safe evaluation

Before opening the final holdout, preregister:

1. construct and unit of analysis;
2. cohort and label adjudication;
3. time and graph-component boundaries;
4. feature definitions and predicted directions;
5. benign twins and evasion generators;
6. missing-data and entity-resolution policy;
7. baselines, model family, calibration, and threshold;
8. investigator capacity and intervention;
9. PR-AUC, ROC-AUC, calibration, precision/recall at capacity, uncertainty,
   incremental lift, and avoided-loss metrics;
10. kill criteria and post-hoc-analysis labeling.

Cohort cleaning, graph construction, feature extraction, weight fitting,
calibration, and threshold selection must occur entirely inside an outer
temporal or connected-component training split. The untouched test remains
sealed until all choices are frozen.

### 7.3 Decisive experiments

| Hypothesis | Required comparison | Decisive falsifier |
|---|---|---|
| Human-calibrated models shift under verified autonomous execution | Matched human-controlled, generic automated, and verified-autonomous legitimate/fraud cohorts | No material calibration or error-rate interaction by executor class |
| Mandate/provenance controls reduce unauthorized agentic loss | Randomized or strong quasi-experimental policy rollout | No reduction in unauthorized attempts, settlements, or loss at comparable exposure |
| Agent-aware features add value | Frozen incumbent controls versus incumbent + features | No out-of-sample incremental lift or intervention benefit |
| Population features detect coordination missed per-address | Held-out coordinated attacks and benign campaigns | No capacity-adjusted gain after entity/component controls |
| Timing regularity is robust | Periodic, resampled, Hawkes, throttled, and adaptive generators plus legitimate schedulers | Signal collapses or false alerts dominate under realistic twins |

Negative results should be retained. A below-chance signal is evidence against
its preregistered direction; it should not receive a new story after testing.

## 8. Control implications

The threat model supports control hypotheses even though detector performance
is unproven:

1. authenticate the accountable principal and bind every action to a scoped,
   expiring, inspectable mandate;
2. apply least privilege, beneficiary allowlists, value/velocity budgets,
   simulation, step-up approval, and revocation at the wallet/payment layer;
3. preserve tamper-evident instruction, model/tool, policy, signature, and
   settlement provenance with cross-plane correlation IDs;
4. separate legitimate automation from suspicious outcomes rather than
   penalizing speed, low value, or 24/7 operation by default;
5. monitor value and entity networks independently of executor substrate;
6. treat agents as possible victims as well as possible instruments;
7. evaluate in offline or shadow mode until outcome, calibration, capacity,
   privacy, fairness, model-risk, and intervention gates pass.

The current research score must never be the sole basis for blocking a payment,
restricting an account, accusing a customer, filing a regulatory report, or
making a law-enforcement referral.

## 9. Limitations and final verdict

The study has only loader-level registry evidence (`R-loader+`) but lacks verified
`W,S,A,C,P,Y,H`; it also has a lossy historical corpus, unknown
comparison labels, connected post-hoc evaluation, detector-informed synthetic
motifs, no banking data, no fraud outcomes, and no immutable clean-clone data
release. Public transfers do not reveal controller intent, mandate, tool
provenance, key compromise, victim harm, beneficial ownership, or order-book
effects. On-chain addresses can also remain personal data when linkable, so
entity resolution and profiling require privacy and governance review.

What survives is useful but narrower:

- the original empirical claims are not supported;
- one conventional graph feature shows weak exploratory association with the
  selected registry proxy;
- software delegation creates important authorization, provenance, and
  response-time control problems;
- per-address-only analysis can miss population structure, but that hypothesis
  remains unvalidated here;
- the repaired causal explanation and research protocol define how stronger
  claims could be earned.

The repository is **not publication-ready as an empirical detection paper and
not deployment-ready**. Publication requires an event-complete immutable
release, verified execution/control evidence, adjudicated outcomes, an untouched
confirmatory evaluation, clean-checkout reproduction, and independent review.

## Primary sources

- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004)
- [OpenClaw session tools](https://docs.openclaw.ai/concepts/session-tool)
- [Google AP2 announcement and mandate model](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
- [FATF risk-based approach for banking](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Risk-based-approach-banking-sector.html)
- [FATF cyber-enabled fraud report](https://www.fatf-gafi.org/en/publications/Methodsandtrends/cyber-enabled-fraud-digitalisation-ml-tf-pf-risks.html)
- [FinCEN Section 314(b) information sharing](https://www.fincen.gov/resources/section-314b)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [EDPB blockchain personal-data guidance](https://www.edpb.europa.eu/documents/guideline/guidelines-on-processing-of-personal-data-through-blockchain-technologies_en)
- [Early ERC-8004 ecosystem study, arXiv:2606.26028](https://arxiv.org/abs/2606.26028)
- [ERC-8004 operational-depth study, arXiv:2606.12128](https://arxiv.org/abs/2606.12128)
- [Weber et al., graph convolution for Bitcoin AML](https://research.ibm.com/publications/anti-money-laundering-in-bitcoin-experimenting-with-graph-convolutional-networks-for-financial-forensics)
- [Song et al., money-laundering subgraphs](https://research.ibm.com/publications/identifying-money-laundering-subgraphs-on-the-blockchain)
