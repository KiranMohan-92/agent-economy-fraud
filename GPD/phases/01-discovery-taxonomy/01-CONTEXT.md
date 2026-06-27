# Phase 1: Discovery and Taxonomy - Context

**Gathered:** 2026-03-16
**Status:** Ready for planning

## Phase Boundary

Establish empirical grounding for A2A fraud detection analysis through platform documentation analysis, academic literature survey, and data source identification. This phase maps the attack surface: what agents can do (OpenClaw/Moltbook), how they behave, what academic research tells us, and what data we can access.

Requirements: [DISC-01, DISC-02, DISC-03, DISC-04]

## Contract Coverage

- **Claim/main**: Financial fraud detection systems rely on behavioral invariants that are properties of human agents by definition. AI agents lack these invariants, creating necessary blind spots in human-based detection.
- **Deliverables**: Platform analysis, literature survey, data acquisition plan
- **Acceptance signal**: Platform analysis complete, literature survey identifies relevant multi-agent/fraud detection research, viable data sources identified
- **False progress to reject**: Abstract analysis without platform grounding, generic AI security without A2A specificity

## User Guidance To Preserve

- **User-stated observables:** Set of necessary properties of A2A commerce that create blind spots in human-based fraud detection
- **User-stated deliverables:** Taxonomy of A2A fraud attack vectors, agent-aware fraud detection framework design, industry recommendations for banking/fintech
- **Must-have references:** OpenClaw platform documentation, Moltbook platform documentation, academic literature on multi-agent economic systems
- **Stop / rethink conditions:** If recommendations fail when tested against real A2A transaction data; if data acquisition research reveals no viable data sources

## Methodological Decisions

### Platform Documentation Analysis

**Depth: Core transaction paths + behavioral analysis**
- Focus on A2A commerce-enabling features: listings, requests, transactions
- Focus on agent behavioral patterns: velocity limits, coordination capabilities, reputation gaming
- NOT full API surface analysis — prioritize commerce and behavioral relevance

**Strategy: Attack chain focus**
- Map complete kill chains first: agent capability → specific API usage → behavioral pattern → detection blind spot
- Then focus documentation analysis on critical path nodes
- This prevents getting lost in interesting but non-critical API details

**Danger zone capabilities** (all four fundamentally change threat model):
- Cross-platform agent identity (persistent reputation across platforms)
- Human behavioral mimicry (perfect replication of human timing/biometrics)
- Coordinated swarm intelligence (flash attacks outrunning detection)
- Financial market integration (HFT/payment rails for economic manipulation)

### Literature Survey

**Scope: All three subfields with weighted depth**
- Multi-agent economic systems: agent economics, game theory, mechanism design
- Fraud detection theory: banking fraud detection, anomaly detection, financial crime prevention
- AI/ML security: adversarial ML, AI safety, robustness to manipulation

**Strategy: Recent + citation chains**
- Recent work focus: last 3-5 years (when agent commerce emerged)
- Citation-chain following: start with key papers, trace intellectual foundations systematically
- Adaptive weighting: prioritize depth in subfields based on what platform analysis reveals

### Data Acquisition Strategy

**Constraint: Public datasets only**
- Use only publicly available datasets — no private API access, no proprietary data
- This keeps research reproducible but may limit direct testability

**Fallback strategy (if no public A2A datasets exist):**
- Document the data gap explicitly as a research limitation
- Build realistic synthetic test cases based on platform documentation analysis
- This maintains scientific honesty while enabling framework development

### Threat Classification Framework

**Organizing principle: Detection difficulty**
- Threat-model-first approach: classify by how hard attacks are to detect with current systems
- This directly supports industry recommendations by prioritizing what to address first

**"Truly undetectable" standard (high bar):**
- Bypasses ALL human behavioral invariants that detection relies on
- Perfect mimicry of legitimate human behavior at all detection layers
- Exploits detection latency (faster than system response time)
- All three factors required — multi-factor definition

**Taxonomy structure:**
- Primary axis: detection difficulty (easy/medium/hard/impossible)
- Secondary dimensions: invariant violated, attack vector, required capabilities
- Multi-dimensional matrix: invariant × vector × detectability for comprehensive coverage

## Physical Assumptions

- **OpenClaw/Moltbook APIs accessible**: Platform documentation is publicly available and analyzable | **Breaks if:** Platforms are private, undocumented, or API access requires credentials we cannot obtain
- **Agent commerce exists**: A2A transactions are occurring or will occur | **Breaks if:** Agents remain purely theoretical with no real-world deployment
- **Human fraud detection invariant-dependence**: Current systems rely on specific human behavioral properties | **Breaks if:** Banking systems have already adapted to non-human patterns (unlikely but possible)
- **Academic literature exists**: Relevant research on multi-agent systems and fraud detection | **Breaks if:** Literature is silent on these intersection topics
- **Public data gap addressable**: Synthetic data can adequately represent real A2A patterns | **Breaks if:** Synthetic patterns fail to capture critical emergent properties of real agent behavior

## Expected Limiting Behaviors

- **When agents → humans**: If we apply the framework to human-only transactions, it should either work (demonstrating compatibility) or flag false positives (demonstrating agent-specificity)
- **When platform → public docs**: Analysis should be reproducible by anyone reading the same documentation
- **When synthetic → real**: Framework tested on synthetic data should generalize to real A2A patterns (or explicitly flag where generalization is uncertain)
- **Literature consistency**: Findings should be consistent with established multi-agent and fraud detection theory (or explicitly identify where we diverge)

## Active Anchor Registry

- **ref-openclaw-docs** (OpenClaw GitHub documentation)
  - Why it matters: Primary source of agent-to-agent messaging and session management behavior
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use

- **ref-moltbook-docs** (Moltbook platform documentation)
  - Why it matters: Primary source of agent social platform behavior, listings, and reputation systems
  - Carry forward: planning, execution, verification, writing
  - Required action: read, use

- **ref-agent-econ-lit** (Academic literature on multi-agent economic systems)
  - Why it matters: Theoretical context for agent economic behavior and transaction patterns
  - Carry forward: planning, execution, writing
  - Required action: read, cite

## Skeptical Review

- **Weakest anchor**: Data access — public A2A transaction datasets may not exist; we may be relying entirely on synthetic data for validation
- **Unvalidated assumptions**: OpenClaw/Moltbook documentation will be publicly accessible and sufficiently detailed; synthetic data can capture emergent agent behavior
- **Competing explanation**: Banking fraud detection may already be adaptable to agent patterns without fundamental redesign (our core claim may be wrong)
- **Disconfirming check**: Literature reveals that current systems already handle multi-agent transactions effectively (would falsify the "blind spot" thesis)
- **False progress to reject**: Theoretical framework without empirical testing; generic AI security advice without A2A specificity; taxonomy without clear mapping to detection difficulty

## Deferred Ideas

- **Formal modeling phase**: Agent game-theoretic models of fraud detection (belongs to Phase 2)
- **Detection framework design**: Specific algorithmic approaches for agent-aware detection (belongs to Phase 3)
- **Regulatory/policy analysis**: Legal frameworks for agent commerce liability (explicitly out of scope)
- **Cryptocurrency-specific attacks**: Focus on banking rails, not blockchain (unless illustrative of A2A principles)

---

_Phase: 01-discovery-taxonomy_
_Context gathered: 2026-03-16_
