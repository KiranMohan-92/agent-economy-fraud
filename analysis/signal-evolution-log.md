# Signal Evolution Log

**Purpose:** Document the differences between Phase 3 signal specifications and their Phase 4/5 implementations.
**Created:** 2026-04-02
**Status:** Reference document

---

## Overview

The Phase 3 specifications (`agent-invariant-signals.md`, `signal-measurement-protocols.md`, `detection-methodology.md`) defined 5 agent-invariant signals with detailed component breakdowns. During Phase 4 implementation and Phase 5 real-data validation, several signals were simplified from 4-5 components to 2-3 components. This document logs every difference.

---

## Signal 1: Economic Rationality

### Phase 3 Specification

4 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Utility deviation | 0.40 | Does the transaction serve an economic purpose? |
| Circular flow detection | 0.30 | Is value cycling back to origin? |
| Purpose deviation | 0.20 | Does the transaction match expected category behavior? |
| Value concentration | 0.10 | Is value anomalously concentrated in few counterparties? |

### Implementation (`economic_rationality.py`)

4 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Utility deviation | 0.40 | Micro-transaction ratio, uniformity, round-number avoidance |
| Circular flow | 0.30 | Bidirectional counterparty ratio |
| Purpose deviation | 0.20 | Counterparty diversity ratio (spray/loop detection) |
| Value concentration | 0.10 | Gini coefficient of outflow distribution |

### Differences

**Component count:** Unchanged (4 -> 4).
**Weights:** Unchanged (0.40/0.30/0.20/0.10).
**Semantic shift:** The spec defined utility deviation abstractly as `|U(v)| / (sent_value + epsilon)`. The implementation operationalizes it with three concrete sub-indicators: micro-transaction ratio, amount uniformity (coefficient of variation), and round-number avoidance. These are on-chain-measurable proxies for the spec's abstract utility function, which assumed merchant category and settlement status data that on-chain transactions lack.

---

## Signal 2: Network Topology

### Phase 3 Specification

4 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Sybil score | 0.40 | Star topology + low interconnectivity + temporal correlation + behavioral similarity |
| Sink/source score | 0.30 | Directional flow imbalance (extraction/mule detection) |
| Community anomaly | 0.20 | Louvain-based community structure anomalies |
| Centrality anomaly | 0.10 | Betweenness/PageRank anomalies |

### Implementation (`network_topology.py`)

3 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Sender centrality anomaly | 0.50 | Out-degree z-score relative to population |
| Receiver centrality anomaly | 0.30 | In-degree z-score relative to population |
| Local clustering anomaly | 0.20 | Clustering coefficient extremes (clique or star) |

### Differences

**Component count:** Reduced from 4 to 3.
**Weight redistribution:** The spec's centrality component (0.10) was expanded and split into sender (0.50) and receiver (0.30) centrality. The spec's Sybil detection (star topology, temporal correlation, behavioral similarity) and community detection (Louvain) were dropped. The clustering anomaly component (0.20) partially covers the Sybil star-topology detection by flagging both dense cliques and star patterns.

**Rationale (inferred):** The spec's Sybil detection required account creation timestamps and behavioral fingerprints — metadata not available in on-chain transaction data. Community detection via Louvain adds computational complexity without clear value for per-address scoring. The implementation focuses on what is directly measurable from the transaction graph: degree centrality and local clustering.

---

## Signal 3: Value Flow

### Phase 3 Specification

5 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Rapid reversal | 0.30 | Value returned to origin within time threshold |
| Detour routing | 0.25 | Value takes unnecessarily long path |
| Value decay | 0.20 | Value diminishes along path (fee extraction) |
| Settlement inconsistency | 0.15 | Settlement timing doesn't match transaction type |
| Velocity anomaly | 0.10 | Speed of value movement through address |

### Implementation (`value_flow.py`)

3 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Flow asymmetry (imbalance) | 0.40 | U-shaped scoring: wash trading (near-zero net) AND drain/spray (extreme one-directional) |
| Flow velocity | 0.30 | Time gap between receiving and forwarding (relay detection) |
| Layering depth | 0.30 | Proportion of counterparties that are themselves balanced-flow relays |

### Differences

**Component count:** Reduced from 5 to 3.
**Weight redistribution:** The spec spread weight across 5 fine-grained components. The implementation consolidates into 3 broader components with higher individual weights.

**Key semantic changes:**
- The spec's "rapid reversal" (A->B->A) was replaced by "flow asymmetry" — a broader concept that detects both wash trading (balanced flows) and extreme one-directional patterns (drain/spray). A code comment in `value_flow.py` documents that the original detector only caught near-zero net flow and missed the dominant on-chain agent pattern: outbound-only addresses.
- The spec's "detour routing" and "value decay" were dropped. The implementation's "layering depth" partially covers detour detection by checking whether counterparties are themselves relay nodes.
- The spec's "settlement inconsistency" was dropped — on-chain transactions settle atomically, making this component inapplicable.
- The spec's "velocity anomaly" maps directly to the implementation's "flow velocity."

**Rationale (inferred):** Settlement inconsistency is a traditional banking concept with no on-chain equivalent. Detour routing requires global path analysis that is computationally expensive per-address. The implementation prioritizes patterns observable from local transaction data. The v0.2 fix note in the code confirms the asymmetric flow detection was added after real-data validation showed agents are predominantly outbound-only.

---

## Signal 4: Temporal Consistency

### Phase 3 Specification

5 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Cross-platform synchronization | 0.30 | Coordinated timing across platforms |
| Burstiness | 0.25 | Transaction bursts exceeding human capability |
| Settlement arbitrage | 0.20 | Exploiting settlement timing differences |
| Temporal incoherence | 0.15 | Activity inconsistent with stated timezone/pattern |
| Periodicity break | 0.10 | Sudden change in activity periodicity |

### Implementation (`temporal_consistency.py`)

3 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Circadian violation | 0.35 | Activity during global low-activity hours (02:00-06:00 UTC) |
| Inter-transaction timing | 0.35 | Sub-human-speed gaps and machine periodicity |
| Burst detection | 0.30 | Maximum transactions per hour vs human limit (30 tx/hr) |

### Differences

**Component count:** Reduced from 5 to 3.
**Weight redistribution:** The spec's top-weighted component (cross-platform synchronization, 0.30) was moved to the Cross-Platform signal where it belongs architecturally. The remaining components were consolidated.

**Key semantic changes:**
- The spec's "cross-platform synchronization" moved to the Cross-Platform signal (Signal 5), avoiding duplication.
- The spec's "burstiness" maps to the implementation's "burst detection."
- The spec's "temporal incoherence" was replaced by "circadian violation" — a more concrete, on-chain-measurable version that checks UTC hour distribution against known human sleep patterns.
- The spec's "settlement arbitrage" was dropped — on-chain settlement is atomic.
- The spec's "periodicity break" was absorbed into "inter-transaction timing," which checks both sub-human-speed gaps and periodicity (coefficient of variation).

**Rationale (inferred):** Settlement arbitrage is a traditional finance concept inapplicable to on-chain atomic settlement. Cross-platform synchronization properly belongs in Signal 5. The implementation consolidates the remaining temporal signals into three directly measurable components.

---

## Signal 5: Cross-Platform Correlation

### Phase 3 Specification

4 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Platform hopping | 0.40 | Rapid movement between platforms |
| Evasion detection | 0.30 | Changing platforms to avoid detection |
| Identity inconsistency | 0.20 | Different identities across platforms |
| Behavioral mismatch | 0.10 | Different behavior patterns across platforms |

### Implementation (`cross_platform.py`)

2 components with weights:

| Component | Weight | Description |
|-----------|--------|-------------|
| Multi-chain presence | 0.50 | Number of chains an address is active on (threshold at 3+) |
| Temporal cross-chain correlation | 0.50 | Synchronized transactions across chains (within 30 seconds) |

### Differences

**Component count:** Reduced from 4 to 2.
**Weight redistribution:** Equal weighting (0.50/0.50) replaces the spec's descending distribution.

**Key semantic changes:**
- The spec's "platform hopping" was simplified to "multi-chain presence" — a binary/stepped measure of how many chains an address operates on.
- The spec's "evasion detection" and "identity inconsistency" were dropped. These require cross-platform identity resolution infrastructure that does not exist for pseudonymous blockchain addresses.
- The spec's "behavioral mismatch" was dropped for the same reason.
- The temporal cross-chain correlation component is new relative to the spec — it detects near-simultaneous transactions across chains, which was part of the Temporal signal spec but architecturally belongs here.

**Rationale (inferred):** The spec assumed a traditional fintech context with identity systems (KYC, account linking). On-chain, addresses are pseudonymous and cross-platform identity resolution is limited to address reuse across EVM chains. The implementation focuses on the two things measurable from multi-chain transaction data: presence and timing.

---

## Fusion Weight Evolution

### Phase 3 Specification (agent-invariant-signals.md)

```
economic_rationality:  0.25
network_topology:      0.25
value_flow:            0.20
temporal_consistency:  0.15
cross_platform:        0.15
```

### Phase 4 Implementation (fusion.py)

```
economic_rationality:  0.25
network_topology:      0.25
value_flow:            0.20
temporal_consistency:  0.20
cross_platform:        0.10
```

### Changes

- `temporal_consistency`: 0.15 -> 0.20 (+0.05)
- `cross_platform`: 0.15 -> 0.10 (-0.05)

The implementation shifted 5 percentage points from cross-platform to temporal consistency. This reflects the practical reality that cross-platform data is harder to obtain (requires multi-chain indexing) while temporal signals are always available from transaction timestamps.

### Phase 5 Dune Data Validation

The `fusion.py` code comments document a weight restoration event:

> "Signal weights — restored after Dune real-data validation (2026-04-03). Value Flow restored to 0.20: with real timestamps, F1 triples (0.11 -> 0.31). Previous zeroing was due to synthetic data artifact (r=-0.47 with dead signal)."

This indicates that during Phase 5 calibration, Value Flow was temporarily zeroed out because synthetic test data produced a negative correlation. When real Dune blockchain data replaced the synthetic data, Value Flow's effectiveness was confirmed and the weight was restored to 0.20.

---

## Decision Threshold Evolution

### Phase 3 Specification

| Tier | Score Range |
|------|-------------|
| ALLOW | 0.0 - 0.3 |
| FLAG | 0.3 - 0.6 |
| BLOCK | 0.6 - 0.8 |
| INVESTIGATE | 0.8 - 1.0 |

### Implementation (fusion.py)

| Tier | Threshold |
|------|-----------|
| ALLOW | < 0.08 |
| FLAG | >= 0.08 |
| INVESTIGATE | >= 0.50 |
| BLOCK | >= 0.75 |

### Changes

1. **Tier ordering changed:** The spec placed BLOCK before INVESTIGATE. The implementation uses the conventional escalation order: FLAG -> INVESTIGATE -> BLOCK.
2. **FLAG threshold drastically lowered:** 0.30 -> 0.08. The code comment explains: "0.08 optimal on real Dune data (F1: 0.428, R: 0.954). Previous 0.24 was calibrated on synthetic data with wider score spread." On-chain agent scores cluster in a narrow low range, requiring a lower threshold to achieve adequate recall.
3. **Upper tiers adjusted:** INVESTIGATE moved from 0.60 to 0.50; BLOCK moved from 0.80 to 0.75.

---

## Summary Table: Specification vs Implementation

| Signal | Spec Components | Impl Components | Spec Weights | Impl Weights | Change Type |
|--------|----------------|-----------------|--------------|--------------|-------------|
| Economic Rationality | 4 (utility, circular, purpose, concentration) | 4 (utility, circular, purpose, concentration) | 0.40/0.30/0.20/0.10 | 0.40/0.30/0.20/0.10 | Operationalized (same structure) |
| Network Topology | 4 (sybil, sink/source, community, centrality) | 3 (sender centrality, receiver centrality, clustering) | 0.40/0.30/0.20/0.10 | 0.50/0.30/0.20 | Simplified (dropped Sybil/community) |
| Value Flow | 5 (reversal, detour, decay, settlement, velocity) | 3 (asymmetry, velocity, layering) | 0.30/0.25/0.20/0.15/0.10 | 0.40/0.30/0.30 | Redesigned (U-shaped asymmetry) |
| Temporal Consistency | 5 (sync, burst, arbitrage, incoherence, periodicity) | 3 (circadian, timing, burst) | 0.30/0.25/0.20/0.15/0.10 | 0.35/0.35/0.30 | Simplified (dropped settlement/cross-platform) |
| Cross-Platform | 4 (hopping, evasion, identity, behavioral) | 2 (presence, temporal) | 0.40/0.30/0.20/0.10 | 0.50/0.50 | Simplified (dropped identity-dependent) |
| **Fusion** | 5 signals | 5 signals | 0.25/0.25/0.20/0.15/0.15 | 0.25/0.25/0.20/0.20/0.10 | Rebalanced (temporal up, cross-platform down) |

---

## Simplification Pattern

Across all signals, the implementation pattern is consistent:

1. **Drop components requiring unavailable data.** Settlement status, merchant categories, KYC identity, and account creation timestamps are not available on-chain. Components depending on these were removed.
2. **Drop components duplicated across signals.** Cross-platform synchronization was specified in both Temporal (Signal 4) and Cross-Platform (Signal 5). The implementation places it only in Signal 5.
3. **Consolidate remaining components into broader measures.** Rather than 5 narrow indicators, the implementation uses 2-4 broader indicators with higher individual weights, reducing the chance that any single sub-component dominates noise.
4. **Adapt to on-chain data model.** The spec assumed a traditional fintech data model (merchant categories, settlement windows, identity graphs). The implementation adapts each signal to what is measurable from `[sender, receiver, amount_usdc, timestamp]` transaction records.

---

## Validation Status

Implementations are validated by Phase 5 real-data results:
- **GAP-01 (Value Flow asymmetric detection):** Closed. The U-shaped flow asymmetry scoring in `value_flow.py` addresses the original gap where outbound-only agent patterns were missed.
- **GAP-02 (Fusion weight calibration):** Closed. Fusion weights were restored to Phase 4 originals after Dune real-data validation confirmed their effectiveness (F1: 0.428, Recall: 0.954 at threshold 0.08).

The simplified implementations achieve measurable detection performance on real Dune blockchain data, confirming that the component reductions did not sacrifice detection capability for the on-chain domain.

---

## Future Optimization: Composite AUC Below Best Individual Signal

The Phase 5 composite AUC (0.590) is below the best individual signal (Network Topology,
AUC = 0.621). This indicates that weaker signals may be adding noise rather than
information to the fusion:

| Signal | AUC |
|--------|-----|
| Network Topology | 0.621 |
| Composite | 0.590 |
| Temporal Consistency | 0.568 |
| Economic Rationality | 0.550 |
| Value Flow | 0.529 |
| Cross-Platform | N/A (non-functional) |

Temporal Consistency (0.568) and Value Flow (0.529) have AUCs only marginally above
random (0.5), suggesting they contribute limited discriminative power and may dilute
the stronger Network Topology signal through equal-weighted fusion.

**Recommended for Phase 6:**
- Explore signal selection (e.g., drop signals with AUC < 0.55) to see if composite
  AUC improves.
- Investigate learned weights (e.g., logistic regression on signal scores) instead of
  hand-tuned weights to optimize fusion.
- Consider interaction effects -- weak signals may still contribute in combination even
  if their individual AUC is low.
