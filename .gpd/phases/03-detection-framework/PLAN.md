# Plan: Phase 3 - Detection Framework Design

**Phase:** 03-detection-framework
**Created:** 2026-03-22
**Status:** Active

---

## Overview

Phase 3 designs an agent-aware fraud detection framework that addresses the fundamental blind spots identified in Phase 2. The core challenge: current systems depend on 9 human behavioral invariants that AI agents systematically violate. We need detection signals that are both (a) agent-invariant (apply equally to humans and agents) and (b) measurable from transaction data.

**From Phase 2:**
- 9 invariants violated at MODERATE or higher severity
- 50% of attack chains rated "Impossible" to detect with current systems
- Core explanation validated: current systems cannot be patched; require first-principles redesign

---

## Phase 3 Contract

### Requirements

| Requirement | Description |
|-------------|-------------|
| **FRAM-01** | Detection methodology addresses all 9 invariant violations identified in Phase 2 |
| **FRAM-02** | Agent-invariant signals specified for fraudulent transaction detection |
| **FRAM-03** | Privacy preservation analysis confirms compliance with banking data protection requirements |
| **FRAM-04** | Computational requirements specified for real-time implementation feasibility |

### Success Criteria

1. **Coverage:** Detection methodology addresses all 9 invariant violations
2. **Signal Specification:** Agent-invariant signals defined with measurement protocols
3. **Privacy:** Framework operates within banking data protection constraints (GDPR, CCPA, etc.)
4. **Feasibility:** Computational requirements enable real-time transaction scoring

### Deliverables

| ID | Deliverable | Description |
|----|-------------|-------------|
| **deliv-detection-methodology** | Detection framework design | Agent-aware detection methodology addressing all invariants |
| **deliv-invariant-signals** | Signal specifications | Agent-invariant detection signals with measurement protocols |
| **deliv-privacy-analysis** | Privacy preservation analysis | Compliance analysis and privacy-preserving design |
| **deliv-computational-analysis** | Computational requirements | Resource requirements and feasibility assessment |

### Acceptance Tests

| Test | Description |
|------|-------------|
| **FRAM-01** | All 9 invariant violations have corresponding detection mechanisms |
| **FRAM-02** | At least 3 agent-invariant signals specified with measurement protocols |
| **FRAM-03** | Privacy analysis identifies no showstopper compliance issues |
| **FRAM-04** | Computational requirements allow real-time scoring (<100ms per transaction) |

---

## Plan 03-01: Agent-Aware Detection Methodology Design

**Status:** Pending
**Duration:** ~3 days
**Dependencies:** Phase 2 complete

### Objective

Design detection methodology that addresses all 9 invariant violations by shifting from human-behavioral assumptions to agent-invariant signals.

### Tasks

#### Task 1.1: Detection Paradigm Formulation
- [ ] 1.1.1 Document paradigm shift: human-behavioral → agent-invariant detection
- [ ] 1.1.2 Define agent-invariant detection principles
- [ ] 1.1.3 Map invariant violations to detection gaps
- [ ] 1.1.4 Create detection methodology overview

#### Task 1.2: Multi-Modal Detection Framework Design
- [ ] 1.2.1 Design signal fusion architecture
- [ ] 1.2.2 Define modalities (economic, network, value flow, temporal)
- [ ] 1.2.3 Document detection pipeline stages
- [ ] 1.2.4 Specify feedback and adaptation mechanisms

#### Task 1.3: Detection Coverage Validation
- [ ] 1.3.1 Map each invariant violation to detection mechanism
- [ ] 1.3.2 Verify all 8 attack chains covered
- [ ] 1.3.3 Assess coverage completeness
- [ ] 1.3.4 Document residual risks

### Deliverables

- `analysis/detection-methodology.md` — Complete detection framework design
- `analysis/invariant-coverage-mapping.md` — Invariant → Detection mechanism mapping

### Acceptance Criteria

- [ ] All 9 invariants have corresponding detection mechanisms
- [ ] All 8 attack chains covered by detection framework
- [ ] Multi-modal architecture documented
- [ ] Paradigm shift clearly articulated

---

## Plan 03-02: Agent-Invariant Signal Specification

**Status:** Pending
**Duration:** ~3 days
**Dependencies:** Plan 03-01 complete

### Objective

Specify detection signals that are (a) agent-invariant (apply equally to humans and agents) and (b) measurable from transaction data.

### Tasks

#### Task 2.1: Signal Discovery and Evaluation
- [ ] 2.1.1 Identify candidate agent-invariant signals
- [ ] 2.1.2 Evaluate each signal for agent-invariance
- [ ] 2.1.3 Assess measurability from transaction data
- [ ] 2.1.4 Rank signals by detection value

#### Task 2.2: Signal Specification (Top 3-5)
- [ ] 2.2.1 Specify **Economic Rationality Signal**
  - Definition: Transactions must make economic sense for rational actors
  - Measurement: Utility function deviation, circular flow detection
  - Agent-invariance: Applies to both humans and agents
- [ ] 2.2.2 Specify **Network Topology Signal**
  - Definition: Fraud creates characteristic network patterns
  - Measurement: Centrality anomalies, clique detection, flow analysis
  - Agent-invariance: Network structure independent of actor type
- [ ] 2.2.3 Specify **Value Flow Signal**
  - Definition: Money flows follow rational economic patterns
  - Measurement: Flow directionality, velocity clustering, destination analysis
  - Agent-invariance: Value flow laws apply regardless of actor
- [ ] 2.2.4 Specify **Temporal Consistency Signal**
  - Definition: Legitimate activity has temporal coherence
  - Measurement: Cross-platform timing, settlement consistency, causal chains
  - Agent-invariance: Time is universal constraint
- [ ] 2.2.5 Specify **Cross-Platform Correlation Signal**
  - Definition: Fraud requires coordination across platforms
  - Measurement: Identity linkage, behavioral correlation, platform bridging
  - Agent-invariance: Platform-spanning behavior detectable

#### Task 2.3: Signal Integration Design
- [ ] 2.3.1 Design signal combination logic
- [ ] 2.3.2 Specify confidence scoring
- [ ] 2.3.3 Define threshold strategies
- [ ] 2.3.4 Document false positive mitigation

### Deliverables

- `analysis/agent-invariant-signals.md` — Complete signal specifications
- `analysis/signal-measurement-protocols.md` — Measurement procedures for each signal

### Acceptance Criteria

- [ ] At least 3 agent-invariant signals fully specified
- [ ] Each signal has measurement protocol
- [ ] Signal integration logic documented
- [ ] False positive mitigation addressed

---

## Plan 03-03: Privacy Preservation Analysis

**Status:** Pending
**Duration:** ~2 days
**Dependencies:** Plan 03-02 complete

### Objective

Analyze privacy implications of agent-aware detection framework and ensure compliance with banking data protection requirements.

### Tasks

#### Task 3.1: Privacy Impact Assessment
- [ ] 3.1.1 Identify data requirements for each signal
- [ ] 3.1.2 Assess privacy sensitivity of required data
- [ ] 3.1.3 Map to regulatory requirements (GDPR, CCPA, GLBA, etc.)
- [ ] 3.1.4 Identify showstopper issues (if any)

#### Task 3.2: Privacy-Preserving Design
- [ ] 3.2.1 Design data minimization approach
- [ ] 3.2.2 Specify pseudonymization/anonymization techniques
- [ ] 3.2.3 Design cross-platform privacy-preserving correlation
- [ ] 3.2.4 Document consent and data governance requirements

#### Task 3.3: Compliance Validation
- [ ] 3.3.1 Validate against GDPR requirements
- [ ] 3.3.2 Validate against US banking regulations (GLBA, Reg E)
- [ ] 3.3.3 Assess AML/KYC data sharing permissibility
- [ ] 3.3.4 Document compliance roadmap

### Deliverables

- `analysis/privacy-preservation-analysis.md` — Complete privacy assessment
- `analysis/privacy-compliance-roadmap.md` — Compliance requirements and path

### Acceptance Criteria

- [ ] No showstopper compliance issues identified
- [ ] Data minimization approach documented
- [ ] Cross-border data transfer addressed
- [ ] AML/KYC sharing within regulatory bounds

---

## Plan 03-04: Computational Requirements Analysis

**Status:** Pending
**Duration:** ~2 days
**Dependencies:** Plan 03-02 complete

### Objective

Specify computational requirements for real-time implementation of agent-aware detection framework.

### Tasks

#### Task 4.1: Resource Requirements Analysis
- [ ] 4.1.1 Estimate per-transaction compute requirements
- [ ] 4.1.2 Estimate storage requirements for signal data
- [ ] 4.1.3 Estimate network bandwidth for cross-platform correlation
- [ ] 4.1.4 Assess scaling requirements

#### Task 4.2: Real-Time Feasibility Assessment
- [ ] 4.2.1 Define real-time latency targets (<100ms per tx)
- [ ] 4.2.2 Assess each signal against latency targets
- [ ] 4.2.3 Identify bottlenecks and optimization strategies
- [ ] 4.2.4 Specify streaming vs. batch architecture

#### Task 4.3: Implementation Architecture
- [ ] 4.3.1 Design detection service architecture
- [ ] 4.3.2 Specify data flow and processing stages
- [ ] 4.3.3 Define scalability approach (horizontal scaling, caching, etc.)
- [ ] 4.3.4 Document deployment considerations

### Deliverables

- `analysis/computational-requirements.md` — Complete resource analysis
- `analysis/implementation-architecture.md` — System architecture for deployment

### Acceptance Criteria

- [ ] Real-time latency targets achievable
- [ ] Scaling path documented
- [ ] Architecture enables incremental deployment
- [ ] Cost estimates within banking industry feasibility

---

## Phase 3 Dependencies

```
Phase 1 (Discovery) ──┐
                      ├───▶ Phase 2 (Analysis) ──▶ Phase 3 (Design) ──▶ Phase 4 (Validation)
Phase 0 (Context)     ──┘
```

**Phase 3 Inputs:**
- 9 invariant violations from Plan 02-02
- 8 attack chains from Plan 02-03
- Core explanation validation from Plan 02-04

**Phase 3 Outputs:**
- Detection methodology (Plan 03-01)
- Agent-invariant signals (Plan 03-02)
- Privacy analysis (Plan 03-03)
- Computational requirements (Plan 03-04)

---

## Verification Strategy

### In-Phase Verification
- After each plan: Validate outputs against requirements
- After Phase 3: Comprehensive verification of all deliverables

### Verification Checklist
- [ ] FRAM-01: All 9 invariants addressed
- [ ] FRAM-02: ≥3 agent-invariant signals specified
- [ ] FRAM-03: No showstopper privacy issues
- [ ] FRAM-04: Real-time feasibility confirmed

### Risk Mitigation
- **Risk:** Agent-invariant signals may not exist
  - **Mitigation:** Plan 03-02 includes fallback to hybrid approaches
- **Risk:** Privacy constraints may block detection
  - **Mitigation:** Plan 03-03 includes privacy-preserving techniques
- **Risk:** Computational requirements may be prohibitive
  - **Mitigation:** Plan 03-04 includes staged deployment approach

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Invariant Coverage | 9/9 addressed | Count of invariants with detection mechanisms |
| Signal Count | ≥3 specified | Number of fully-specified agent-invariant signals |
| Privacy Showstoppers | 0 identified | Privacy assessment review |
| Latency Target | <100ms/tx | Computational analysis validation |

---

**Plan Status:** READY FOR EXECUTION
**Next Step:** Begin Plan 03-01: Agent-Aware Detection Methodology Design
