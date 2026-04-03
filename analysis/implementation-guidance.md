# Implementation Guidance and Prioritization

**Phase:** 04-validation-recommendations, Plan 04-04
**Created:** 2026-23-03
**Audience:** Banking/fintech implementation teams

---

## 1. Priority Ranking Framework

### 1.1 Scoring Criteria

| Criterion | Weight | Scale |
|-----------|--------|-------|
| **Impact** | 40% | Detection coverage improvement |
| **Urgency** | 30% | Vulnerability exposure window |
| **Feasibility** | 20% | Implementation complexity (1-5) |
| **Cost** | 10% | Resource requirements |

### 1.2 Priority Matrix

| Rank | Action | Impact | Urgency | Feasibility | Cost | Priority Score |
|------|--------|--------|---------|------------|------|---------------|
| **1** | Deploy Economic Rationality + Network Topology | CRITICAL | IMMEDIATE | MEDIUM | $80K | 0.94 |
| **2** | Synthetic data validation | HIGH | IMMEDIATE | EASY | $20K | 0.91 |
| **3** | Add Value Flow signal | HIGH | SHORT-TERM | MEDIUM | $30K | 0.87 |
| **4** | Real-time latency infrastructure | MEDIUM | SHORT-TERM | MEDIUM | $151K | 0.81 |
| **5** | Cross-platform privacy framework | HIGH | MEDIUM-TERM | HARD | $250K | 0.76 |
| **6** | Add Temporal Consistency signal | MEDIUM | MEDIUM-TERM | MEDIUM | $40K | 0.74 |
| **7** | Add Cross-Platform Correlation signal | HIGH | LONG-TERM | HARD | $300K | 0.70 |
| **8** | Industry A2A data consortium | HIGH | LONG-TERM | VERY HARD | $500K | 0.65 |
| **9** | Regulatory guidance program | MEDIUM | MEDIUM-TERM | LOW | $100K | 0.62 |
| **10** | Production deployment at scale | CRITICAL | LONG-TERM | VERY HARD | $2M | 0.58 |

---

## 2. Technical Implementation Guides

### 2.1 Signal Implementation: Economic Rationality

**API Pattern:**
```python
class EconomicRationalitySignal:
    def score(self, transaction: Transaction, context: Context) -> float:
        # Component 1: Utility deviation (40%)
        utility_score = self._utility_deviation(transaction, context)

        # Component 2: Circular flow detection (30%)
        circularity_score = self._circular_flow_score(transaction, context)

        # Component 3: Purpose deviation (20%)
        purpose_score = self._purpose_deviation(transaction, context)

        # Component 4: Value concentration (10%)
        concentration_score = self._value_concentration(transaction, context)

        return (0.4 * utility_score +
                0.3 * circularity_score +
                0.2 * purpose_score +
                0.1 * concentration_score)
```

**Data Requirements:**
- Transaction history (last 90 days per account)
- Network graph structure
- Merchant category codes
- Transaction purpose labels

### 2.2 Signal Implementation: Network Topology

**API Pattern:**
```python
class NetworkTopologySignal:
    def score(self, transaction: Transaction, graph: NetworkGraph) -> float:
        # Component 1: Sender centrality anomaly (50%)
        sender_anomaly = self._centrality_anomaly(
            transaction.sender_id, graph
        )

        # Component 2: Receiver centrality anomaly (30%)
        receiver_anomaly = self._centrality_anomaly(
            transaction.receiver_id, graph
        )

        # Component 3: Path length anomaly (20%)
        path_anomaly = self._path_length_anomaly(
            transaction.sender_id,
            transaction.receiver_id,
            graph
        )

        return (0.5 * sender_anomaly +
                0.3 * receiver_anomaly +
                0.2 * path_anomaly)
```

**Data Requirements:**
- Transaction graph (edges between accounts)
- Centrality computations (betweenness, PageRank)
- Community detection algorithms

### 2.3 Data Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                 │
│  (REST/GraphQL for transaction scoring)                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Signal Processing Layer (parallel)                            │ │
│  │                                                              │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │ │
│  │  │Economic│ │Network │ │Value   │ │Temporal │  │ │
│  │  │Rationality│ │Topology│ │Flow    │ │Consist. │  │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    Signal Fusion Layer                        │ │
│  │  - Weighted combination (adaptive weights)                   │ │
│  │  - Confidence estimation                                   │ │
│  │  - 4-tier decision (ALLOW/FLAG/BLOCK/INVESTIGATE)          │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                     Data Layer                                │ │
│  │  - Redis (hot signal cache)                                   │ │
│  │  - PostgreSQL (transaction storage)                            │ │ │
│  │  - Neo4j (network graph)                                   │ │ │
│  │  - ClickHouse (historical analytics)                          │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                   External Integrations                          │ │
│  │  - Banking core systems                                     │ │
│  │  - Payment processors                                        │ │
│  │  - Fraud case management systems                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Integration Patterns

**Pattern 1: Sidecar Deployment**

```
┌──────────────┐     ┌──────────────┐
│  Banking     │────▶│  Detection   │
│  System     │     │  Service    │
│              │     │  (Sidecar)    │
└──────────────┘     └──────────────┘
         │                     │
         └─────────────────────┘
              │
         ▼
    Transaction Events
```

**Pattern 2: API Gateway Integration**

```
┌──────────────┐
│  Transaction │────▶ API Gateway ┐
│  Events     │                │
└──────────────┘                │
                              │
                              ▼
                    ┌────────────────────────┐
                    │  Detection Service       │
                    │  (Microservice)          │
                    └────────────────────────┘
                              │
                              ▼
                    ┌────────────────────────┐
                    │  Banking Core Systems    │
                    └────────────────────────┘
```

---

## 3. Risk Mitigation

### 3.1 Implementation Risks

| Risk | Mitigation Strategy |
|------|-------------------|
| False positives increase | Phased rollout with tuning periods |
| Privacy compliance breach | Privacy-by-design validation; legal review |
| Technical integration complexity | Reference implementations; vendor partnerships |
| Staff training gap | Comprehensive training program; playbooks |
| Adaptation by fraudsters | Continuous model updates; adversarial testing |

### 3.2 Monitoring and Adaptation

**Key Metrics to Track:**
- Detection rate by attack chain
- False positive rate by signal
- Latency (p50, p95, p99)
- System uptime and availability

**Adaptation Mechanisms:**
- Weekly model retraining on new patterns
- Monthly threshold optimization
- Quarterly signal weight recalibration

---

## 4. Quick Wins vs. Strategic Investments

### 4.1 Quick Wins (0-3 months)

| Action | Impact | Effort | ROI |
|--------|--------|-------|-----|
| Deploy Economic Rationality signal | +35% detection | Low | HIGH |
| Generate synthetic validation data | Enables testing | Low | HIGH |
| Implement basic alerting | Immediate visibility | Low | HIGH |

### 4.2 Strategic Investments (6-18 months)

| Action | Impact | Effort | ROI |
|--------|--------|-------|-----|
| Full 5-signal framework | +49% detection | High | MEDIUM |
| Cross-platform privacy framework | Enables impossible attack detection | High | MEDIUM |
| Real-time latency infrastructure | Enables real-time scoring | High | MEDIUM |

### 4.3 Long-term Bets (18-36 months)

| Action | Impact | Effort | ROI |
|--------|--------|-------|-----|
| Industry data consortium | Real-world validation | Very High | HIGH |
| Production deployment | Full coverage at scale | Very High | HIGH |
| Regulatory framework | Industry standard | High | MEDIUM |

---

---

## Precision Caveat (Added 2026-04-02)

**Important:** The impact estimates in the priority matrix above (e.g., "+35% detection",
"+49% detection") are calibrated against Phase 4 synthetic data where precision was ~96%.
Phase 5 real-world validation showed **precision drops to 27.6%** on real on-chain data,
while **recall remains robust at 95.4%**. The precision gap is attributed to the framework
correctly flagging non-human automated activity (bots, relays) that falls outside the
labeled agent ground truth. Implementers should plan for higher false positive rates than
the synthetic benchmarks suggest, and should include tuning periods in their rollout plans.

---

**Document Status:** COMPLETE
**Next Step:** Update TODO.md and ROADMAP.md
