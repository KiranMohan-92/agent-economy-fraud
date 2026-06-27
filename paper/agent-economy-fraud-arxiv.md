# Agent-to-Agent Commerce and Human Behavioral Invariants in Banking Fraud Detection

**Draft for arXiv preprint - June 2026**

This Markdown artifact is the review-facing synchronized copy of the LaTeX manuscript in `paper/main.tex`. The LaTeX source remains canonical for equations, tables, figures, appendices, and bibliography. (June-2026 refresh: repositioned against concurrent agentic-commerce-security prior work, documented-incident framing, and Stage-3 threshold transparency — see `GPD/literature/june-2026-prior-work-and-landscape-refre-REVIEW.md`.)

## Abstract

Financial fraud detection systems often rely on behavioral invariants that describe human actors: velocity limits, biometric authentication, device fingerprinting, geographic constraints, cognitive and energy constraints, identity persistence, behavioral stability, computational limits, and bounded rationality. We show that AI agents executing agent-to-agent (A2A) commerce stress all nine invariants, creating systematic blind spots when detectors rely only on human behavioral assumptions.

Using OpenClaw and Moltbook as platform case studies, we derive an eight-chain taxonomy of A2A fraud attack vectors grounded in platform capabilities. We design a five-signal agent-invariant detection framework and validate it across synthetic data, real Base-chain USDC transactions from 665 ERC-8004 registered agents, and a mixed dataset with injected attack patterns.

The empirical result is intentionally scoped. Synthetic validation reaches F1 = 88.71% and ROC-AUC = 0.97. Real-data transfer is partial: raw-label recall is 61.4% at the fixed synthetic threshold and reaches 95.4% after threshold re-optimization (81.1% on cleaned labels), while cleaned-label composite ROC-AUC is 0.515. Attack-injection validation detects 7 of 8 injected attack chains at 100% per-chain recall. The eighth chain, coordinated swarm behavior, reveals an architectural gap in per-address scoring.

We provide an open-source reference implementation and distinguish framework-supported banking recommendations from longer-horizon policy proposals. As of mid-2026, agent impersonation and agent-wallet theft are already documented, while systematic A2A-commerce fraud exploiting the specific invariant blind spots modeled here remains undocumented and is the threat model's decisive future test.

## 1. Introduction

Autonomous AI agents are already transacting on-chain. As of early 2026, ERC-8004-registered agents on Base have executed tens of thousands of USDC transactions, and platform primitives such as session enumeration, history extraction, message dispatch, sub-agent creation, and identity linking make autonomous economic activity operational rather than hypothetical.

The core claim is narrow:

> Fraud detection systems that rely only on human behavioral invariants have systematic blind spots under the A2A scenarios tested here.

The claim is structural where the monitored signal presupposes human embodiment, but the empirical claims are bounded by observed platforms, noisy labels, and attack-injection experiments.

### Contributions

1. **Nine-invariant taxonomy.** A formal mapping of human behavioral invariants to agent-era failure modes.
2. **Eight-chain attack taxonomy.** A taxonomy of A2A fraud attack vectors classified by invariant violation and detection difficulty: easy, medium, hard, and out of scope for current human-assumption or per-address systems.
3. **Five-signal detection framework.** An agent-invariant detection methodology grounded in on-chain observables rather than human behavioral assumptions.
4. **Three-stage empirical validation.** Synthetic validation, real on-chain transfer analysis, and attack-injection testing with explicit caveats.
5. **Collective detection gap.** Identification of coordinated swarm attacks as requiring population-level detection beyond per-address scoring.
6. **Banking recommendations.** Prioritized implementation guidance that separates validated signal overlays from policy hypotheses.

## 2. Background

The paper surveys three A2A commerce surfaces: gateway platforms such as OpenClaw, social/reputation platforms such as Moltbook, and on-chain identity standards such as ERC-8004. Together, these surfaces span discovery, negotiation, execution, and settlement.

Fraud detection historically depends on nine human behavioral invariants:

| # | Invariant | Detection method | Human basis |
|---|-----------|------------------|-------------|
| I1 | Velocity limits | Rate thresholds | Cognitive throughput and fatigue |
| I2 | Biometric authentication | Fingerprint, face, voice | Biological phenotype |
| I3 | Cognitive and energy constraints | Session and activity patterns | Sleep cycles and finite attention |
| I4 | Geographic binding | IP, device, card-present logic | Embodied location |
| I5 | Device fingerprint | Browser and device identifiers | Owned hardware |
| I6 | Identity persistence | KYC/AML, history depth | Costly legal identity |
| I7 | Behavioral stability | Baseline deviation scoring | Habitual spending patterns |
| I8 | Computational limits | CAPTCHA and timing checks | Human reaction time |
| I9 | Bounded rationality | Anomaly detection on value flows | Satisficing rather than optimization |

The hard-to-vary explanation is that detectors which monitor only those human properties lose coverage when the actor is software. The repair is not to discard fraud detection; it is to measure agent-native properties such as graph topology, value flow, timing regularity, economic rationality, and cross-platform correlation.

## 3. Threat Model

The paper defines eight attack chains grounded in documented A2A platform capabilities:

| Chain | Attack | Main violated assumption | Detection status |
|-------|--------|--------------------------|------------------|
| CHAIN_1 | Agent enumeration | Account visibility | Easy |
| CHAIN_2 | History extraction | Transaction privacy | Medium |
| CHAIN_3 | Async flooding | Velocity | Medium |
| CHAIN_4 | Disposable agent army | Identity persistence | Hard |
| CHAIN_5 | Cross-platform identity | Channel isolation | Out of scope for human-assumption detectors |
| CHAIN_6 | Behavioral mimicry | Unique fingerprint | Out of scope for human-assumption detectors |
| CHAIN_7 | Swarm intelligence | Coordination latency | Out of scope for per-address scoring |
| CHAIN_8 | Market manipulation | Reaction time | Out of scope for human-assumption detectors |

The difficulty labels describe the baseline detector being exceeded, not a proof of absolute undetectability.

## 4. Detection Framework

The framework uses five agent-native signals:

| Signal | Role |
|--------|------|
| Economic Rationality | Detects economically unusual micro-transactions, circular flows, and concentration patterns. |
| Network Topology | Detects hub, fan-out, path, and centrality anomalies. |
| Value Flow | Detects rapid extraction, layering, and flow velocity. |
| Temporal Consistency | Detects both machine-speed activity and overly regular mimicry. |
| Cross-Platform Correlation | Defined architecturally but inactive in the current single-chain deployment. |

The current fusion vector is:

```text
S = 0.2739 * NT + 0.2505 * TC + 0.2424 * ER + 0.2332 * VF + 0.0000 * CP
```

The reference implementation includes 47 tests covering signal computation, edge cases, threshold calibration, attack injection, label loading, and fusion arithmetic.

## 5. Evaluation

### Stage 1: Synthetic Validation

Synthetic validation uses 100,000 addresses: 10,000 synthetic agent addresses and 90,000 synthetic human addresses.

| Metric | Value |
|--------|-------|
| Precision | 82.36% |
| Recall | 96.23% |
| F1 | 88.71% |
| ROC-AUC | 0.97 |
| Median latency | 97 ms |

### Stage 2: Real On-Chain Validation

Real validation uses 81,904 Base-chain USDC transactions with 665 ERC-8004 registered agents as positives and 1,069 cleaned human-labeled counterparties as negatives.

| Metric | Raw labels | Cleaned labels |
|--------|------------|----------------|
| Precision | 27.6% | 42.9% |
| Recall | 95.4% | 81.1% |
| F1 | 42.8% | 56.1% |
| ROC-AUC | not reported | 0.515 |

The transfer gap is material. At the fixed synthetic threshold, recall is 61.4%. The 95.4% recall headline requires re-optimizing the threshold to 0.08 and accepting a higher false-positive rate. The low cleaned-label AUC and noisy negative class are central limitations.

### Stage 3: Attack Injection Validation

Attack injection uses 93,579 real transactions plus 6,050 injected attack transactions. Seven of eight attack chains are detected at 100% recall at the tested operating threshold; Chain 7 is not detected by per-address scoring.

| Chain | Status | Recall |
|-------|--------|--------|
| CHAIN_1 | Easy | 100% |
| CHAIN_2 | Medium | 100% |
| CHAIN_3 | Medium | 100% |
| CHAIN_4 | Hard | 100% |
| CHAIN_5 | Out of scope for human-assumption detectors | 100% |
| CHAIN_6 | Out of scope for human-assumption detectors | 100% |
| CHAIN_7 | Out of scope for per-address scoring | 0% |
| CHAIN_8 | Out of scope for human-assumption detectors | 100% |

The Behavioral Mimicry Paradox is bounded to the tested timing model: deterministic mimicry can become too regular, making it detectable by temporal consistency checks. The Collective Detection Gap is the main architectural limitation: single-transaction swarm members do not contain enough per-address history to score.

## 6. Related Work

The manuscript positions this work relative to agent-based computational economics, multi-agent reinforcement learning, financial fraud detection, blockchain analytics, adversarial machine learning, Web2 bot detection, AI agent security, and the concurrent agentic-commerce-security literature. The June-2026 revision adds a dedicated *Agentic Commerce Security* subsection distinguishing this paper from the systematization/protocol work that appeared alongside it — the A2A-payments SoK (Zhang et al., arXiv:2604.03733), the agentic-commerce-security SoK (Mao et al., arXiv:2604.15367), and the A402 prevention protocol (Li et al., arXiv:2603.01179) — none of which reports empirical on-chain detection metrics. The narrowed novelty claim is that this is the only work pairing a behavioral-invariant account of detection failure with empirical on-chain detection on real agent transactions.

The revised bibliography removes weakly grounded positioning and adds verified references for:

- Tesfatsion's agent-based computational economics chapter.
- Chandola et al.'s anomaly-detection survey.
- Carcillo et al.'s supervised/unsupervised credit-card fraud work.
- Biggio and Roli's adversarial-machine-learning review.
- Gleave et al.'s adversarial policies for deep reinforcement learning.

## 7. Industry Recommendations

P0 and P1 recommendations are directly supported by implemented signals or measured gaps. P2 and P3 recommendations are policy and infrastructure hypotheses requiring independent legal, privacy, and operational validation.

| Tier | Recommendation | Status |
|------|----------------|--------|
| P0 | Economic Rationality + Network Topology overlays | Directly supported by measured signals |
| P0 | Agent-platform metadata detection | Directly supported by platform capability analysis |
| P1 | Velocity threshold adjustment for identified agent addresses | Supported by threat model and timing measurements |
| P1 | Cross-channel identity correlation | Supported by platform capability analysis |
| P1 | Collective-behavior detection prototype | Motivated by Chain 7 failure |
| P2 | Controller step-up authentication | Policy proposal |
| P2 | Forensic data retention | Policy proposal |
| P2 | Agent KYC framework | Policy proposal |
| P3 | Multi-chain monitoring integration | Infrastructure proposal |
| P3 | Industry agent-transaction labeling | Standards proposal |

The prior mandatory-biometrics framing has been narrowed to controller step-up authentication, with modality selection deferred to privacy and accessibility review.

## 8. Limitations

The main limitations are:

- Negative-class labels are heuristic and likely contaminated by automated non-ERC-8004 entities.
- Cross-platform correlation is architecturally defined but inactive because the evaluation dataset is single-chain.
- Temporal Consistency may degrade first as agents learn to mimic human timing distributions.
- Chain 7 requires population-level graph detection and is not solved by the current per-address framework.
- The invariant-failure *mechanism* is now evidenced in production (documented agent-wallet theft and large-scale agent impersonation), but systematic *in-scope* A2A-commerce fraud exploiting the specific blind spots modeled here is not yet documented; a confirmed in-scope case is the threat model's decisive falsification test.

Rather than a forward-dated 6-12 month window, the paper frames the transition as already underway in 2026 and supplies the detection framework needed to measure the in-scope attack surface as it is exercised. Multi-chain behavior is now the dominant operating reality, which makes the inactive Cross-Platform signal the single most consequential gap in the current single-chain evaluation.

## 9. Conclusion

Autonomous AI agents stress the behavioral invariants that many banking fraud detectors assume. The paper does not claim mature production readiness. It claims that human-invariant-only detectors have measurable blind spots under documented A2A capabilities, and that agent-native signals provide a first-generation detection framework with explicit limits.

The strongest empirical findings are the synthetic and attack-injection results. The most important caveats are the weak real-data ranking result, the noisy negative labels, threshold re-optimization, inactive cross-platform correlation, and the Chain 7 collective-detection gap.

The practical result is a bounded research and implementation agenda: deploy the low-regret P0/P1 overlays, build population-level detection for swarms, collect cleaner labels, activate multi-chain correlation, and treat longer-horizon policy recommendations as hypotheses requiring separate validation.
