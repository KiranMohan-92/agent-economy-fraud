# GPD Peer-Review Panel -- Referee Report

**Paper:** Agent-to-Agent Commerce and the Collapse of Human Behavioral Invariants in Banking Fraud Detection
**Venue:** arXiv cs.CR preprint, April 2026
**Review date:** 2026-04-05

---

## 1. Reader Perspective

**Rating: Accept**

1.1. The paper is well-motivated and clearly written. The central thesis -- that fraud detection systems fail against AI agents *necessarily* rather than contingently -- is stated early, repeated with precision, and supported throughout. A security researcher unfamiliar with blockchain analytics can follow the argument without difficulty because the nine-invariant taxonomy (Table 1) provides an intuitive bridge from familiar fraud-detection concepts to the new agent-era failure modes.

1.2. The eight attack chains are grounded in specific, named API calls (e.g., `sessions_send` with `timeoutSeconds=0`), which makes them concrete rather than abstract. This is a strength: the reader can verify each claim against the cited platform documentation.

1.3. One weakness in accessibility: the paper oscillates between three different dataset sizes (81,904 transactions, 93,579 transactions, 100,000 synthetic addresses) across sections without a single consolidated data-flow diagram. A reader who skips ahead to the evaluation will struggle to reconcile the numbers. A figure showing the three-stage pipeline with dataset sizes at each stage would significantly improve navigability.

---

## 2. Literature Positioning

**Rating: Weak Accept**

2.1. The related work section covers four relevant threads (multi-agent economics, fraud detection, blockchain analytics, AI agent security) and correctly identifies the gap at their intersection. The Sybil-attack lineage from Douceur through Jiang is appropriate, and the connection to prompt-injection work (Greshake, Carlini) is well-placed.

2.2. **Missing comparison: adversarial ML for transaction monitoring.** The paper does not engage with the substantial literature on adversarial evasion of ML-based transaction-monitoring systems (e.g., Cartella et al. 2021 on adversarial attacks against credit card fraud detectors; Aleskerov et al. on neural network-based fraud detection). The behavioral mimicry paradox (CHAIN_6) would be strengthened by explicit comparison to adversarial example generation in this domain.

2.3. **Missing comparison: bot detection in Web2.** The problem of distinguishing automated actors from humans has decades of history in web security (CAPTCHAs, behavioral biometrics for bot detection, device fingerprinting). The paper's nine invariants overlap significantly with the assumptions underlying these systems. Failing to cite this body of work (e.g., Bursztein et al. on reCAPTCHA, Iliou et al. on web bot detection) weakens the novelty claim and misses an opportunity to draw on known evasion/counter-evasion dynamics.

---

## 3. Mathematical / Technical Rigor

**Rating: Weak Accept**

3.1. **Velocity arithmetic is correct but misleading.** Equation 2 computes a velocity amplification factor of ~2.16 million by comparing peak agent throughput (9,000 tx/h) against average human throughput (100 tx/day). This is an apples-to-oranges comparison: peak vs. average. A fairer comparison would use peak human throughput (e.g., a power user doing 20 tx/hour through a banking app) vs. peak agent throughput. The qualitative conclusion (orders-of-magnitude difference) survives, but the specific number is inflated and should be reframed.

3.2. **The fusion formula (Eq. 5) is underspecified.** The paper states weights are "AUC-proportional" but does not define the normalization. The four active weights sum to 1.0 (0.2739 + 0.2505 + 0.2424 + 0.2332 = 1.0000), suggesting w_i = AUC_i / sum(AUC_j). But AUC values near 0.5 mean the signals are barely above chance. AUC-proportional weighting when all AUCs are in the 0.46-0.60 range produces near-uniform weights, which is what we observe (sigma = 0.015). The paper should acknowledge that this weighting scheme is effectively uniform and that its theoretical justification (rewarding more discriminative signals) has minimal practical effect here.

3.3. **The CV threshold for mimicry detection (CV < 0.05) is asserted but not derived.** The paper presents CV = 1.87 for real agents and CV < 0.005 for mimics, but the decision boundary of 0.05 appears without justification. How was this threshold chosen? What is the false-positive rate at this threshold against legitimate automated systems (e.g., market makers, scheduled payments)? The two-tailed design (Eq. 3) is a good idea, but the thresholds need empirical grounding.

---

## 4. Empirical Validity

**Rating: Borderline**

4.1. **The headline recall of 95.4% is solid, but the ROC-AUC of 0.515 is barely above chance.** The paper acknowledges this (Section 5.2) and attributes it to negative-class contamination. This attribution is plausible but unverified -- the 0.7 confidence estimate on label quality is itself a guess. The honest thing to do is report the AUC prominently (it is somewhat buried) and state clearly that the framework's ranking ability on real data is not demonstrated. The paper currently emphasizes recall at a cherry-picked threshold while downplaying the AUC.

4.2. **Stage 3 attack injection is self-validating.** The attack transactions are synthetic, generated by the same team that designed the detector. The 100% recall on 7/8 chains is therefore expected: the detector was designed to catch exactly these patterns. The paper would be substantially stronger if it included attacks designed by an independent red team, or if the attack patterns were drawn from documented real-world exploit transactions rather than synthetic generation.

4.3. **The "transfer gap" metric (recall drop of 0.83 pp) is misleading.** Comparing recall on synthetic data (where both classes are cleanly defined) to recall on real data (where the positive class is clean but the threshold has been re-optimized from 0.24 to 0.08) is not a fair transfer measurement. The threshold re-optimization absorbs much of the distributional shift. A genuine transfer metric would hold the threshold fixed and report the resulting recall and FPR.

4.4. **Limitations are honestly stated.** Section 8 is unusually candid: it acknowledges label noise, the collective detection gap, the TC canary degradation, and the pre-crime research validity concern. The testable prediction (TC AUC will fall to <= 0.52 within 12 months, NT will remain >= 0.58) is commendable -- few papers offer falsifiable predictions about their own framework's degradation. This honesty is a genuine strength.

---

## 5. Significance

**Rating: Accept**

5.1. The paper identifies a real and timely problem. A2A commerce is growing, and the structural mismatch between human-assumption fraud detection and agent behavior is genuine. The nine-invariant taxonomy alone is a useful conceptual contribution that practitioners can apply immediately as a risk-assessment checklist.

5.2. The open-source implementation with reproducibility appendix, Parquet data files, and a pip-installable package lowers the barrier to adoption. The recommendations section (P0-P3 roadmap with cost estimates) is practitioner-oriented and actionable, which is rare in academic security papers.

5.3. The behavioral mimicry paradox (Section 5.4.1) is an intellectually interesting result with implications beyond this specific domain: deterministic imitation of a stochastic process produces detectable regularity. This insight could inform bot-detection research more broadly.

---

## Overall Recommendation: Minor Revision

The paper addresses an important and timely problem with a well-structured argument, an honest evaluation, and practical deliverables. However, the empirical evidence is weaker than the presentation suggests (AUC of 0.515, self-validating attack injection, re-optimized thresholds), and the related work has notable gaps. With targeted revisions, this would be a solid contribution.

---

## Top 3 Strengths

1. **Conceptual clarity.** The nine-invariant taxonomy and the distinction between contingent and necessary failure modes provide a durable analytical framework that will outlast the specific detection signals proposed.

2. **Intellectual honesty.** The limitations section, the 0% recall on CHAIN_7, the TC-canary prediction, and the pre-crime validity discussion set a high standard for self-critical reporting in security research.

3. **Practitioner orientation.** The open-source package, reproducibility appendix, prioritized recommendation roadmap with cost estimates, and compliance mappings make this immediately useful to financial institutions, not just academics.

---

## Top 3 Weaknesses

1. **Empirical evidence does not support the claimed detection power.** A composite ROC-AUC of 0.515 on real data is barely above random. The paper emphasizes recall at a re-optimized threshold while the AUC tells a very different story. The Stage 3 attack injection is self-validating (detector catches attacks it was designed to catch), providing limited evidence of real-world robustness.

2. **Related work gaps.** The paper ignores the adversarial ML literature on evasion of transaction-monitoring models and the extensive Web2 bot-detection literature, both of which are directly relevant and would contextualize the novelty claims more accurately.

3. **Key thresholds and metrics lack rigorous justification.** The CV threshold of 0.05, the velocity amplification comparison (peak vs. average), the 0.7 confidence label-quality estimate, and the AUC-proportional weighting (which is effectively uniform) are all under-justified. Individually, each is minor; collectively, they erode confidence in the quantitative claims.

---

## Specific Required Changes

1. **Report the ROC-AUC of 0.515 prominently in the abstract and introduction**, not buried in Section 5.2. The abstract currently reports recall of 95.4% without mentioning the AUC. This is misleading by omission.

2. **Add a transfer-gap analysis with a fixed threshold.** Report recall and FPR on real data using the synthetic-calibrated threshold of 0.24, *then* report the results at the re-optimized threshold of 0.08. Both numbers are informative; reporting only the latter obscures the distributional shift.

3. **Justify the CV = 0.05 decision boundary** with an empirical analysis: plot the CV distribution for known agents, known humans, and (if available) known automated-but-legitimate systems (market makers, bridge relayers). Report the false-positive rate at the chosen threshold.

4. **Correct or reframe the velocity amplification factor.** Either compare peak-to-peak and average-to-average, or explicitly state that Equation 2 compares peak agent throughput to average human throughput and explain why this is the relevant comparison.

5. **Add related work on adversarial ML for fraud detection and Web2 bot detection.** At minimum, cite 2-3 papers from each domain and explain how your invariant-collapse argument differs from or extends the evasion dynamics studied in those settings.

6. **Add a data-flow diagram** showing the three evaluation stages, their dataset sizes, and the label-construction pipeline. This would resolve the confusion caused by different transaction counts appearing across sections (81,904 vs. 93,579 vs. 100,000).

7. **Acknowledge that AUC-proportional weighting is effectively uniform** given the narrow AUC spread (0.4647 to 0.5990). Discuss whether an alternative weighting scheme (e.g., excluding TC given its below-chance AUC, or using AUC - 0.5 as weights) would be more principled.

---

*End of referee report.*
