# Phase 1: Discovery and Taxonomy - Research

**Researched:** 2026-03-17
**Domain:** Cybersecurity / Multi-Agent Economic Systems / Fraud Detection
**Confidence:** MEDIUM

## Summary

This phase researches the foundational methods for analyzing agent-to-agent (A2A) commerce vulnerabilities in banking fraud detection systems. The core claim is that financial fraud detection relies on behavioral invariants that are properties of human agents by definition, and AI agents lack these invariants, creating necessary blind spots.

**Primary recommendation:** Use a three-pronged discovery approach combining (1) attack-chain-focused platform documentation analysis, (2) literature survey across multi-agent economics, fraud detection theory, and AI/ML security, and (3) public data sourcing with explicit synthetic fallback documentation.

**Key research constraint:** This is novel territory — A2A commerce is an emerging domain with limited established literature. Platform documentation (OpenClaw/Moltbook) will be primary anchors rather than academic validation. Confidence is MEDIUM due to the emerging nature of the field and rate-limited search capabilities during research.

## User Constraints

See phase CONTEXT.md (`01-CONTEXT.md`) for locked decisions and user constraints that apply to this phase.

**Locked methodological decisions affecting this research:**

1. **Platform Documentation Analysis Depth:** Core transaction paths + behavioral analysis only (NOT full API surface). Focus on agent capability -> API usage -> behavioral pattern -> detection blind spot mapping.

2. **Four "danger zone" capabilities** requiring extra scrutiny:
   - Cross-platform agent identity (persistent reputation across platforms)
   - Human behavioral mimicry (perfect replication of human timing/biometrics)
   - Coordinated swarm intelligence (flash attacks outrunning detection)
   - Financial market integration (HFT/payment rails for economic manipulation)

3. **Literature Survey Scope:** All three subfields (multi-agent economics, fraud detection, AI/ML security) with 3-5 year recency focus and citation-chain following.

4. **Data Acquisition Constraint:** Public datasets only. Synthetic data with explicit gap documentation is the required fallback.

5. **Threat Classification Framework:** Detection difficulty as primary axis. Multi-factor "undetectable" standard (bypasses ALL human behavioral invariants, perfect mimicry, exploits detection latency).

6. **Agent's Discretion Areas:**
   - Specific taxonomic structure for organizing threat vectors
   - Literature prioritization within subfields based on platform analysis findings
   - Synthetic data generation approaches

7. **Deferred Ideas (OUT OF SCOPE):**
   - Formal game-theoretic modeling (Phase 2)
   - Detection framework design (Phase 3)
   - Regulatory/policy analysis
   - Cryptocurrency-specific attacks

## Active Anchor References

| Anchor / Artifact | Type | Why It Matters Here | Required Action | Where It Must Reappear |
| ----------------- | ---- | ------------------- | --------------- | ---------------------- |
| ref-openclaw-docs | Platform documentation | Primary source of agent-to-agent messaging and session management behavior | Read, map API endpoints relevant to A2A commerce | Plan / Execution / Verification |
| ref-moltbook-docs | Platform documentation | Primary source of agent social platform behavior, listings, and reputation systems | Read, map reputation and behavioral constraints | Plan / Execution / Verification |
| ref-agent-econ-lit | Academic literature | Theoretical context for agent economic behavior and transaction patterns | Read, cite, survey for relevant work | Plan / Execution / Writing |

**Missing or weak anchors:**
- **Data sources:** No public A2A transaction datasets have been identified yet. This is a known gap requiring the synthetic data fallback.
- **Platform accessibility:** OpenClaw/Moltbook documentation availability is assumed but not yet verified. If platforms are private or undocumented, this phase becomes significantly more constrained.

## Conventions

| Choice | Convention | Alternatives | Source |
| ---------------- | ------------------ | -------------- | ------------------ |
| Threat model | Attack-chain-first (capability -> API -> behavior -> blind spot) | Capability inventory only, API-surface-first | CONTEXT.md locked decision |
| Detection difficulty axis | Primary organizing principle | CVSS-based, impact-based, exploitability-based | CONTEXT.md locked decision |
| Undetectable standard | Multi-factor (all 3: bypass invariants, perfect mimicry, exploit latency) | Single-factor (any one factor), threshold-based | CONTEXT.md locked decision |
| Literature recency | 3-5 years + citation chains | Historical foundations only, state-of-the-art only | CONTEXT.md locked decision |
| Data sources | Public only, synthetic with gap documentation | Private API access, scraped data, proprietary datasets | CONTEXT.md locked decision |

**CRITICAL:** All findings below use these conventions. Deviating from locked methodological decisions requires explicit user approval.

## Domain-Specific Research Framework

**Note:** This is a cybersecurity/economics domain, not physics. The "Mathematical Framework" section is adapted to "Analytical Frameworks" appropriate for security research and threat modeling.

### Key Analytical Frameworks and Starting Points

| Framework | Description | Source | Role in This Phase |
| ----------------------- | ---------------- | ----------------------- | ------------------ |
| Attack chain mapping | Capability -> API usage -> behavioral pattern -> detection blind spot | CONTEXT.md (locked decision) | Primary organizational method for platform analysis |
| Human behavioral invariants | Velocity limits, biometrics, device fingerprinting, location constraints | PROJECT.md | Baseline for identifying agent violations |
| Deutsch's hard-to-vary criterion | Explanations cannot be varied while remaining falsifiable | PROJECT.md | Validation standard for taxonomy |
| Detection difficulty classification | Easy/medium/hard/impossible based on human invariant violations | CONTEXT.md | Primary axis for threat taxonomy |

### Required Techniques

| Technique | What It Does | Where Applied | Standard Reference |
| --------------------- | ------------- | --------------------- | ------------------ |
| Threat modeling | Systematic identification and assessment of security threats | Platform analysis, attack vector identification | MITRE ATT&CK, STRIDE methodology |
| API surface analysis | Mapping capabilities from documentation to behavioral implications | OpenClaw/Moltbook documentation review | OWASP API Security Top 10 |
| Literature citation chaining | Following reference chains from key papers to foundations | Academic literature survey | Standard academic research methodology |
| Gap analysis documentation | Explicit identification of what cannot be empirically validated | Data acquisition planning | Scientific research standards for reproducibility |

### Approximation Schemes

| Approximation | Scope Limit | Regime of Validity | Error Estimate | Alternatives if Invalid |
| -------------------------- | ---------------- | ------------------ | ---------------- | ----------------------------- |
| Core transaction paths only | NOT full API surface | Commerce and behavior relevance | May miss edge cases | Expand to full API if critical gaps identified |
| Public datasets only | No private/proprietary data | Reproducible research | May not represent real-world patterns | Synthetic with explicit gap documentation |
| 3-5 year literature window | Recent work focus | Emerging A2A domain | May miss foundational theory | Citation chains to older foundations |

## Standard Approaches

### Approach 1: Attack-Chain-First Platform Analysis (RECOMMENDED)

**What:** Map complete kill chains from agent capability through specific API usage to behavioral patterns to detection blind spots, then focus documentation analysis on critical path nodes.

**Why standard:** This prevents getting lost in interesting but non-critical API details. By mapping the attack chain first, we identify which API endpoints actually matter for fraud detection vulnerabilities.

**Track record:** Standard in security research for mapping attack surfaces. Used in threat modeling methodologies like MITRE ATT&CK and kill chain analysis.

**Key steps:**

1. **Capability inventory:** List agent capabilities from platform documentation
2. **Kill chain mapping:** For each capability, trace: capability -> API usage -> behavioral pattern -> detection blind spot
3. **Critical node identification:** Mark which API endpoints are on critical paths
4. **Focused analysis:** Deep-dive documentation only on critical path nodes
5. **Four danger zones:** Extra scrutiny on cross-platform identity, behavioral mimicry, swarm intelligence, financial integration

**Known difficulties at each step:**

- Step 1: Platform documentation may be incomplete or ambiguous. **Mitigation:** Cross-reference multiple documentation sources, flag ambiguities explicitly.
- Step 2: Kill chains may branch or have multiple paths. **Mitigation:** Document all branches, prioritize by detection impact.
- Step 3: Distinguishing critical from non-critical nodes is subjective. **Mitigation:** Use detection difficulty as objective criterion.
- Step 4: Danger zone capabilities may be poorly documented. **Mitigation:** Infer from available APIs, flag speculation explicitly.

### Approach 2: Literature-First Discovery (FALLBACK)

**What:** Begin with literature survey to understand established threats, then map platform capabilities to known threat patterns.

**When to switch:** When platform documentation is inaccessible, incomplete, or when the attack-chain approach yields insufficient critical nodes.

**Tradeoffs:**
- **Gain:** Leverages established threat categories from academic research
- **Loss:** May miss novel threats specific to A2A commerce that literature hasn't addressed yet

### Approach 3: Synthetic Data Modeling (FALLBACK if no public A2A datasets)

**What:** Generate realistic synthetic A2A transaction patterns based on platform documentation and literature insights.

**When to switch:** When no viable public A2A transaction datasets exist (identified in DISC-04 research).

**Tradeoffs:**
- **Gain:** Enables empirical framework development despite data gaps
- **Loss:** Validation uncertainty — synthetic patterns may not capture emergent properties of real agent behavior

### Anti-Patterns to Avoid

- **Full API surface analysis without prioritization:** Why it fails — wastes time on non-critical endpoints, obscures the actual threat vectors. What to do instead — Use attack-chain mapping to identify critical nodes first.
- **Generic AI security research without A2A specificity:** Why it fails — produces recommendations that don't address the unique properties of agent commerce. What to do instead — Ground all analysis in platform documentation and human behavioral invariant violations.
- **Theoretical framework without empirical testing:** Why it fails — False progress indicator per contract. What to do instead — Maintain explicit data acquisition plan, document gaps honestly, use synthetic data with clear limitations.
- **Taxonomy without detection difficulty axis:** Why it fails — Violates locked decision, produces unactionable classification. What to do instead — Always classify by detection difficulty as primary axis.

## Existing Results to Leverage

**This section is MANDATORY.** Since this is novel territory with limited established literature, this becomes "Nearest Analogues and Mathematical Scaffolding" — list the closest solved problems and how they inform the approach.

### Established Results (DO NOT RE-DERIVE)

| Result | Exact Form / Reference | Source | How to Use |
| ------------------------- | ------------------- | ---------------------------- | -------------------- |
| Human behavioral invariants in fraud detection | Velocity limits, biometric signatures, device fingerprinting, location constraints | Banking/fraud detection industry practice | Baseline for identifying agent violations |
| Kill chain methodology | Reconnaissance -> Weaponization -> Delivery -> Exploitation -> Installation -> C2 -> Actions on Objectives | Lockheed Martin (2011) | Framework for mapping agent attack chains |
| MITRE ATT&CK framework | Tactics, techniques, and procedures (TTPs) for adversarial behavior | MITRE | Standard vocabulary for threat classification |
| STRIDE threat modeling | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege | Microsoft (1999) | Comprehensive threat category checklist |

**Key insight:** Re-deriving these established frameworks would waste context. Use them as scaffolding and focus novelty on the A2A-specific violations.

### Nearest Analogues (for Novel Territory)

| Domain | What It Gives You | Source | Conditions / Mapping |
| ------------------------ | ------------------------- | ---------------- | ------------ |
| Botnet detection | Coordinated automated behavior patterns at scale | Security literature (2015-2020) | Agents are authorized, botnets are unauthorized — key difference in detection approach |
| High-frequency trading (HFT) fraud | Market manipulation at machine timescales | Financial security research | Legitimate HFT vs. malicious agent transactions — regulatory context differs |
| API security | Rate limiting, authentication, session management best practices | OWASP API Security Top 10 | Direct mapping to OpenClaw/Moltbook API surface |
| Multi-agent reinforcement learning | Emergent coordination behaviors | AI/ML literature (2018-2024) | Economic incentives differ between MARL research and A2A commerce |
| Peer-to-peer (P2P) marketplace fraud | Reputation system vulnerabilities, sybil attacks | Trust/reputation literature | Direct mapping to Moltbook reputation systems |

### Relevant Prior Work

| Paper/Result | Authors | Year | Relevance | What to Extract |
| ------------ | --------- | ------ | -------------- | ------------------------------------ |
| "The Adversarial Resilience of Learning-Based奥秘detectors" | Multiple | 2020-2023 | Adversarial ML applicable to agent-aware detection | Robustness methodologies, evasion techniques |
| Fraud detection with graph neural networks | Multiple | 2019-2024 | Transaction pattern analysis at scale | Graph-based detection architectures |
| Sybil-resistant reputation systems | Multiple | 2005-2020 | Moltbook reputation vulnerabilities | Identity verification approaches, attack resistance |
| Multi-agent economic systems surveys | Various | 2018-2024 | Theoretical context for agent economics | Game-theoretic models, incentive analysis |

**Note:** Due to search rate limiting, specific paper citations could not be retrieved. This represents the *types* of prior work that should be consulted. The literature survey (DISC-03) will identify specific papers with arXiv IDs and DOIs.

## Computational Tools

### Core Tools

| Tool | Version/Module | Purpose | Why Standard |
| ------------- | -------------- | -------------- | -------------------- |
| Python 3.10+ | Standard library | Data analysis, synthetic data generation | Universal, reproducible |
| pandas | 2.0+ | Tabular data manipulation for transaction datasets | Industry standard for financial data |
| networkx | 3.0+ | Graph analysis for transaction networks and reputation systems | Standard for network-based fraud detection |
| matplotlib / seaborn | Latest | Visualization of transaction patterns and behavioral clusters | Standard plotting libraries |
| requests / httpx | Latest | API interaction for platform documentation retrieval | Standard HTTP clients |

### Supporting Tools

| Tool | Purpose | When to Use |
| ------------------ | --------------- | ------------------- |
| Jupyter notebooks | Interactive exploration and documentation | Data analysis, synthetic data development |
| pytest | Unit testing for synthetic data generation | Validation of data generation logic |
| scipy | Statistical analysis of transaction patterns | Anomaly detection benchmarking |
| yaml / toml | Configuration management for analysis parameters | Reproducible analysis pipelines |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
| ---------- | ------------- | ------------------------------ |
| pandas | Polars, dask | Polars is faster for large data; dask for distributed. pandas is standard and sufficient for initial analysis. |
| networkx | igraph, graph-tool | igraph/graph-tool faster for large graphs; networkx has better pure-Python integration. |
| matplotlib | plotly, bokeh | Interactive vs. static. matplotlib sufficient for research analysis. |

### Computational Feasibility

| Computation | Estimated Cost | Bottleneck | Mitigation |
| -------------------------------------- | -------------- | ------------------ | --------------- |
| Platform documentation analysis | Low (hours) | Manual reading time | Structured extraction templates |
| Literature survey | Medium (days) | Access to paywalled papers | Use arXiv, institutional access |
| Public dataset search | Low (hours) | Data availability | Explicit gap documentation, synthetic fallback |
| Synthetic data generation | Medium (days) | Capturing emergent properties | Iterative validation against platform analysis |

**Installation / Setup:**
```bash
# Python packages for data analysis and synthetic generation
pip install pandas networkx matplotlib seaborn requests httpx scipy

# Jupyter for interactive analysis
pip install jupyter notebook

# Testing framework
pip install pytest
```

**DO NOT install silently:** Per shared protocols, ask user before any installation.

## Validation Strategies

### Internal Consistency Checks

| Check | What It Validates | How to Perform | Expected Result |
| --------------------- | ------------------ | --------------- | ------------------------- |
| Attack chain completeness | All capabilities mapped through to blind spots | Trace each agent capability through API -> behavior -> detection | No dead-end chains |
| Human invariant coverage | All detection invariants identified | Cross-reference with industry fraud detection practices | Velocity, biometrics, device, location all covered |
| Platform grounding | No abstract analysis without platform basis | Verify each claim references specific platform capability | Every blind spot maps to documented API |
| Taxonomy Deutsch criterion | Hard-to-vary explanation test | Vary explanation elements — does it become implausible? | Core explanation robust to variation |

### Known Limits and Benchmarks

| Limit | Parameter Regime | Known Result | Source |
| ------------------------------ | ---------------- | --------------------- | ----------- |
| Human transaction velocity | ~10-100 transactions/day | Cognitive and sleep constraints | Banking industry standards |
| Detection latency | Minutes to hours | Human monitoring + batch processing | Industry practice |
| Agent-only velocity | Machine-speed limited only by API rate limits | 10^3-10^6 transactions/day possible | Platform API rate limits |
| Biometric presence | Present (humans), Absent (pure agents) | Fundamental physical constraint | Biology vs. software |

### Numerical Validation

| Test | Method | Tolerance | Reference Value |
| --------------------------- | -------------- | ------------------ | --------------- |
| Synthetic data sanity check | Statistical distribution matching | Order-of-magnitude | Real-world transaction statistics |
| Kill chain connectivity | Graph traversal to verify no orphaned nodes | 100% connectivity | All chains must reach blind spots |
| Detection difficulty ranking | Cross-rater consistency (if multiple analysts) | Cohen's kappa > 0.7 | Inter-rater reliability standard |

### Red Flags During Computation

- **If analysis produces generic AI security advice without A2A specificity:** Indicates drift from locked methodological decision. Re-ground in platform documentation.
- **If no detection blind spots are identified:** Indicates analysis failed to identify agent violations of human invariants. Re-examine the four danger zone capabilities.
- **If synthetic data is generated without gap documentation:** Violates public-data constraint. Explicitly document what cannot be validated.
- **If literature survey focuses on general adversarial ML without agent economics:** Indicates scope creep. Refocus on A2A-specific research.

## Common Pitfalls

### Pitfall 1: Full API Surface Analysis Without Prioritization

**What goes wrong:** Spending weeks cataloging every API endpoint, most of which are irrelevant to fraud detection.

**Why it happens:** Natural tendency toward completeness; documentation is structured as API reference, not threat model.

**How to avoid:** Attack-chain-first approach. Map kill chains first, then only analyze endpoints on critical paths.

**Warning signs:** Analysis document organized by API module (auth, sessions, messaging) rather than by attack chain (identity spoofing -> session hijack -> transaction fraud).

**Recovery:** Re-structure analysis by attack chains. Mark non-critical APIs as "out of scope for this phase."

### Pitfall 2: Generic AI Security Without Platform Grounding

**What goes wrong:** Producing recommendations about "adversarial examples" or "model poisoning" that don't apply to A2A commerce.

**Why it happens:** A2A commerce is a new domain; existing literature focuses on traditional AI security.

**How to avoid:** Every finding must trace back to a specific platform capability from OpenClaw or Moltbook documentation.

**Warning signs:** Claims that don't reference specific API endpoints or platform behaviors.

**Recovery:** Re-examine platform documentation. Map each claim to documented agent capabilities.

### Pitfall 3: Ignoring the Data Gap

**What goes wrong:** Proceeding as if empirical validation is possible when no public A2A datasets exist.

**Why it happens:** Desire for rigor; reluctance to acknowledge limitations.

**How to avoid:** Explicit gap documentation. If using synthetic data, clearly state what real-world properties it cannot capture.

**Warning signs:** Data acquisition plan assumes access to private datasets or API data without explicit access pathway.

**Recovery:** Document the data gap explicitly. Use synthetic data with clear limitations section.

### Pitfall 4: Violating Locked Methodological Decisions

**What goes wrong:** Drifting into formal modeling (Phase 2) or detection framework design (Phase 3).

**Why it happens:** The phases are intellectually related; it's easy to continue thinking ahead.

**How to avoid:** Regular review of CONTEXT.md locked decisions. Stop at "what exists" not "how to detect it."

**Warning signs:** Analysis includes game-theoretic models or detection algorithms.

**Recovery:** Extract only the mapping/analysis components. Defer modeling and detection to later phases.

## Level of Rigor

**Required for this phase:** Documentary evidence with reproducible methodology (not formal proof, not numerical evidence)

**Justification:** This is a discovery phase. We are establishing what exists in platform documentation and literature, not proving theorems or running experiments. Rigor comes from thorough documentation, traceability to sources, and explicit acknowledgment of gaps.

**What this means concretely:**

- All claims must reference specific documentation sections or literature citations
- Attack chains must be traceable from capability through API to blind spot
- Data gaps must be documented explicitly, not glossed over
- Synthetic data limitations must be stated clearly
- Literature searches must follow citation chains systematically

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
| ------------ | ---------------- | ------------ | ------------------------------ |
| Rule-based fraud detection | ML/AI-based anomaly detection | 2010-2020 | Human-invariant assumptions embedded in ML training data |
| Single-agent threat modeling | Multi-agent coordinated threats | Emerging | Attackers already use botnets; agents add legitimacy and authorization |
| Human-only transaction models | Human + agent transaction models | Emerging (this research) | Banking systems not adapted |

**Superseded approaches to avoid:**

- **Rule-based detection signatures:** Why outdated — Agents can vary behavior to avoid fixed rules. Modern approach uses behavioral anomaly detection, which creates new vulnerabilities when agents lack human invariants.
- **Static API threat modeling:** Why outdated — Doesn't capture behavioral emergence from agent coordination. Modern approach considers multi-agent interaction patterns.

## Open Questions

1. **Platform documentation accessibility**
   - What we know: OpenClaw GitHub is referenced in PROJECT.md; Moltbook documentation is mentioned but location unspecified
   - What's unclear: Are these platforms publicly accessible? Is documentation complete?
   - Impact on this phase: If platforms are private or undocumented, we lose primary empirical anchors
   - Recommendation: Begin with OpenClaw GitHub; if inaccessible, flag immediately and shift to literature-first approach

2. **Public A2A dataset existence**
   - What we know: No public datasets were identified in project scoping
   - What's unclear: Has anyone published A2A transaction data? Can we access historical data from platforms?
   - Impact on this phase: Determines whether we use synthetic data as fallback or if there are real data sources
   - Recommendation: Document search methodology explicitly; if no datasets found, proceed with synthetic approach and clear gap documentation

3. **Literature specificity for A2A commerce**
   - What we know: Literature exists on multi-agent systems, fraud detection, and AI security
   - What's unclear: How much directly addresses A2A commerce vs. adjacent problems (botnets, HFT, P2P markets)?
   - Impact on this phase: Affects how much nearest-analogue mapping is needed
   - Recommendation: Use citation chaining from the most relevant papers; expect significant mapping effort

## Alternative Approaches if Primary Fails

| If This Fails | Because Of | Switch To | Cost of Switching |
| ---------------- | -------------- | ------------------- | ----------------- |
| Attack-chain platform analysis | Platform documentation inaccessible or incomplete | Literature-first discovery using nearest analogues | Medium — lose empirical grounding, gain theoretical breadth |
| Public A2A dataset search | No datasets exist | Synthetic data with explicit gap documentation | Low — already the planned fallback |
| Four danger zone analysis | Capabilities not documented in platform APIs | Infer from available APIs + literature, flag speculation explicitly | Medium — increased uncertainty, requires explicit confidence downgrade |

**Decision criteria:**
- If platform documentation is inaccessible: Switch to literature-first approach immediately; don't waste time on inaccessible sources.
- If no A2A datasets exist after exhaustive search: Proceed with synthetic data; explicit gap documentation is required per locked decision.
- If literature is silent on A2A commerce: Use nearest analogues (botnets, HFT, P2P) and document the mapping.

## Sources

### Primary (HIGH confidence)

- PROJECT.md, REQUIREMENTS.md, ROADMAP.md (project definition, locked decisions)
- 01-CONTEXT.md (locked methodological decisions for this phase)
- Established frameworks: MITRE ATT&CK, STRIDE, Kill Chain methodology
- Industry fraud detection practices (human behavioral invariants)

### Secondary (MEDIUM confidence)

- Platform documentation: OpenClaw GitHub, Moltbook platform docs (to be accessed in execution)
- Academic literature on multi-agent economic systems (to be surveyed in DISC-03)
- OWASP API Security Top 10

### Tertiary (LOW confidence)

- **Note:** Due to search rate limiting (service limit exhausted 2026-03-17), web search could not be performed to retrieve specific paper citations. Literature survey (DISC-03) will establish specific citations with arXiv IDs and DOIs.
- Nearest analogue domains (botnets, HFT, P2P markets) — direct mapping to A2A commerce is novel and requires validation

## Metadata

**Confidence breakdown:**

- Analytical frameworks: HIGH — Established threat modeling methodologies (MITRE ATT&CK, STRIDE, Kill Chain) are well-grounded
- Standard approaches: MEDIUM — Attack-chain-first approach is standard in security research but adaptation to A2A commerce is novel
- Computational tools: HIGH — Python/pandas/networkx are industry standards; no novel tools required
- Validation strategies: MEDIUM — Internal consistency checks are sound; empirical validation limited by data availability
- Literature citations: LOW — Rate limiting prevented search; specific paper citations deferred to DISC-03 execution

**Research date:** 2026-03-17
**Valid until:** Platform documentation changes (OpenClaw/Moltbook updates) or major breakthrough in A2A security literature. The analytical frameworks are stable; the novel territory aspects (A2A-specific threats) may evolve rapidly.

**External tool failure note:** Web search was rate-limited during this research phase. Research proceeded using established domain knowledge and project context. Literature survey (DISC-03) will establish specific citations. Confidence in novel aspects is reduced to LOW/MEDIUM accordingly.
