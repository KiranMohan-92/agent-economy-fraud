# Agent-Invariant Signal Specifications

**Phase:** 03-detection-framework, Plan 03-02
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document specifies 5 agent-invariant detection signals with detailed measurement protocols, scoring algorithms, and implementation guidance. Each signal is designed to detect fraud patterns that are properties of transactions themselves, not the actors who initiate them.

---

## Signal 1: Economic Rationality

### Definition

**Economic Rationality:** A transaction or transaction pattern is economically rational if all parties receive value commensurate with their contribution. Fraud violates this principle through circular flows, value destruction, or systematic extraction without economic purpose.

**Agent-Invariance Justification:** Economic rationality applies to all rational actors, regardless of whether they are human or AI. Both humans and agents must obey economic constraints: legitimate transactions serve a purpose; fraud requires patterns that violate value conservation.

### Measurement Protocol

#### Step 1: Transaction Graph Construction

For each transaction `t`, construct a directed graph `G = (V, E)` where:
- `V` = set of accounts (parties to transactions)
- `E` = set of transactions (edges with direction: payer → payee)

**Input Data Required:**
```json
{
  "transaction_id": "tx_12345",
  "from_account": "acc_A",
  "to_account": "acc_B",
  "amount": 1000.00,
  "timestamp": "2026-03-22T10:30:00Z",
  "merchant_category": "electronics",
  "settlement_status": "cleared"
}
```

**Graph Features Extracted:**
- `deg_in(v)`: Number of incoming transactions to account `v`
- `deg_out(v)`: Number of outgoing transactions from account `v`
- `flow_through(v)`: Total value flowing through account `v`
- `path_length(u, v)`: Shortest transaction path from `u` to `v`

#### Step 2: Utility Function Estimation

For each account `v`, estimate economic utility:

```
U(v) = Σ (received_value) - Σ (sent_value) + external_benefits(v)
```

Where:
- `received_value` = sum of all incoming transaction amounts
- `sent_value` = sum of all outgoing transaction amounts
- `external_benefits` = estimated value of goods/services received

**Utility Deviation Score:**
```
utility_deviation(v) = |U(v)| / (Σ sent_value + ε)
```

Where `ε = 1.0` prevents division by zero.

**Interpretation:**
- `utility_deviation ≈ 0`: Account is roughly balanced (legitimate commerce)
- `utility_deviation > 0.5`: Account receives more than sends (potential sink)
- `utility_deviation < -0.5`: Account sends more than receives (potential source)

#### Step 3: Circular Flow Detection

Detect cycles in transaction graph using depth-limited search (max depth = 6):

```
circular_flow_score = Σ (amount_in_cycle) / Σ (total_transaction_amount)
```

**Algorithm:**
```python
def detect_circular_flows(graph, max_depth=6):
    cycles = []
    for start_node in graph.nodes:
        visited = {start_node}
        path = [start_node]
        dfs_find_cycles(start_node, start_node, path, visited, cycles, max_depth)
    return cycles

def dfs_find_cycles(current, start, path, visited, cycles, depth):
    if depth == 0:
        return
    for neighbor in graph.outgoing[current]:
        if neighbor == start and len(path) >= 3:
            cycles.append(path + [start])
        elif neighbor not in visited:
            dfs_find_cycles(neighbor, start, path + [neighbor],
                          visited | {neighbor}, cycles, depth - 1)
```

**Circular Flow Flags:**
- `has_cycle`: Boolean indicating presence of cycle
- `cycle_amount`: Total value in detected cycle
- `cycle_participants`: Number of unique accounts in cycle
- `cycle_duration`: Time between first and last transaction in cycle

#### Step 4: Economic Purpose Assessment

Assess whether transaction volume aligns with expected economic purpose:

```
purpose_score = min(1.0, transaction_volume / expected_volume(purpose))
```

**Purpose Categories:**
| Purpose | Expected Volume (tx/day) | Expected Value Distribution |
|---------|--------------------------|----------------------------|
| Consumer retail | 1-10 | $10-$500 per transaction |
| B2B commerce | 10-100 | $1,000-$100,000 per transaction |
| High-frequency trading | 10,000+ | Variable, but has arbitrage purpose |
| Payroll processing | 100-10,000 | Fixed amounts per employee |
| **Suspicious** | **Any** | **Volume without clear purpose** |

### Scoring Algorithm

**Economic Rationality Score (0-1, where 1 = most suspicious):**

```
economic_risk = 0.4 × utility_deviation_normalized
              + 0.3 × circular_flow_normalized
              + 0.2 × purpose_deviation_normalized
              + 0.1 × value_concentration_normalized
```

**Component Normalization:**
```python
def normalize_score(value, max_threshold):
    return min(1.0, value / max_threshold)

# Normalization thresholds
utility_threshold = 0.5      # 50% utility deviation
circular_threshold = 0.3     # 30% of transactions in cycles
purpose_threshold = 5.0      # 5× expected volume
concentration_threshold = 0.8 # 80% of value to single counterparty
```

**Risk Classification:**
| Score Range | Classification | Action |
|-------------|----------------|--------|
| 0.0 - 0.3 | Low Risk | Allow |
| 0.3 - 0.6 | Medium Risk | Flag for review |
| 0.6 - 0.8 | High Risk | Block or require additional verification |
| 0.8 - 1.0 | Very High Risk | Block and investigate |

### Implementation Considerations

**Data Requirements:**
- Transaction history: minimum 30 days per account
- Counterparty relationships: full transaction graph
- Merchant categorization: for purpose estimation
- Settlement status: to distinguish cleared from pending

**Computational Complexity:**
- Graph construction: O(V + E) where V = accounts, E = transactions
- Cycle detection: O(V^d) where d = max depth (typically 3-6)
- Utility calculation: O(E) per scoring window

**Real-Time Feasibility:**
- **Streaming mode:** Maintain running utility totals, update on each transaction
- **Batch mode:** Full graph analysis every 5-10 minutes
- **Target latency:** 20-50ms per transaction (streaming mode)

**False Positive Mitigation:**
1. **Whitelist known legitimate high-velocity actors** (exchanges, payroll processors)
2. **Economic purpose validation** (check for clear business purpose)
3. **Temporal smoothing** (require sustained pattern, not single transaction)
4. **Human review loop** (high-risk cases investigated by analysts)

### Detection Capabilities

| Attack Chain | Primary Mechanism | Detection Confidence |
|--------------|-------------------|---------------------|
| Agent Enumeration | Utility deviation (no inflow) | HIGH |
| Async Flooding | Purpose deviation (volume without purpose) | MEDIUM |
| Agent Army | Circular flows + concentration | HIGH |
| Market Manipulation | Value concentration + circular flows | HIGH |

---

## Signal 2: Network Topology

### Definition

**Network Topology:** Legitimate commerce forms distributed, multi-path transaction networks. Fraud creates characteristic anomalous structures: hub-and-spoke (Sybil armies), star patterns (extraction), or disconnected components (money mules).

**Agent-Invariance Justification:** Network topology is independent of actor nature. Whether human or agent, fraudulent coordination leaves structural signatures in the transaction graph.

### Measurement Protocol

#### Step 1: Identity Graph Construction

Construct temporal identity graph `G_t = (V, E_t)` for time window `t`:

```
V = {all accounts with activity in window t}
E_t = {(u, v) | transaction from u to v in window t}
```

**Graph Types:**
1. **Bipartite Graph:** Buyers ↔ Sellers (two-layer)
2. **Ego Network:** Single account + immediate neighbors
3. **Temporal Graph:** Graph evolution over time windows

**Graph Metrics (per account `v`):**

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Degree | `deg(v) = deg_in(v) + deg_out(v)` | Transaction activity level |
| Clustering Coefficient | `CC(v) = 2 × triangles(v) / (deg(v) × (deg(v) - 1))` | Local connectivity density |
| Betweenness Centrality | `BC(v) = Σ (σ_st(v) / σ_st)` for all s,t | Bridge/connector role |
| PageRank | `PR(v) = (1-d)/N + d × Σ PR(u)/deg(u)` | Influence/importance |
| k-Core Decomposition | Largest k where v in k-core | Core/periphery position |

#### Step 2: Sybil Detection via Structural Analysis

**Sybil Army Characteristics:**
- High out-degree from central controller
- Low interconnectivity among Sybil nodes
- Star or hub-and-spoke topology
- Temporal correlation (created simultaneously)

**Sybil Score Calculation:**

```
sybil_score(v) = 0.3 × star_topology_normalized
               + 0.3 × low_interconnectivity_normalized
               + 0.2 × temporal_correlation_normalized
               + 0.2 × behavioral_similarity_normalized
```

**Component Calculations:**

**1. Star Topology Score:**
```python
def star_topology_score(v, graph):
    neighbors = graph.outgoing_neighbors(v)
    if len(neighbors) < 3:
        return 0.0

    # Count edges among neighbors
    internal_edges = 0
    for u in neighbors:
        for w in neighbors:
            if u != w and graph.has_edge(u, w):
                internal_edges += 1

    expected_edges = len(neighbors) * (len(neighbors) - 1)
    return 1.0 - (internal_edges / expected_edges)
```

**2. Low Interconnectivity Score:**
```python
def interconnectivity_score(neighbors, graph):
    if len(neighbors) < 2:
        return 0.0

    # Calculate clustering coefficient of neighbor set
    internal_edges = 0
    for u in neighbors:
        for w in neighbors:
            if u != w and graph.has_edge(u, w):
                internal_edges += 1

    possible_edges = len(neighbors) * (len(neighbors) - 1)
    return 1.0 - (internal_edges / possible_edges)
```

**3. Temporal Correlation Score:**
```python
def temporal_correlation_score(neighbors, account_creation_times):
    if len(neighbors) < 3:
        return 0.0

    times = [account_creation_times[n] for n in neighbors]
    time_span = max(times) - min(times)

    # High correlation if accounts created within short window
    return 1.0 if time_span < 3600 else max(0, 1.0 - time_span / 86400)
```

**4. Behavioral Similarity Score:**
```python
def behavioral_similarity_score(neighbors, transaction_patterns):
    if len(neighbors) < 3:
        return 0.0

    # Compare transaction amount distributions
    patterns = [transaction_patterns[n] for n in neighbors]
    similarities = []

    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            sim = cosine_similarity(patterns[i], patterns[j])
            similarities.append(sim)

    # High similarity = suspicious (coordinated behavior)
    return np.mean(similarities)
```

#### Step 3: Sink/Source Detection

**Sink Node:** Account that receives value but rarely sends (potential fraudster extraction point)

```
sink_score(v) = deg_in(v) / (deg_in(v) + deg_out(v) + ε) × (flow_in(v) / flow_total)
```

**Source Node:** Account that sends value but rarely receives (potential money mule)

```
source_score(v) = deg_out(v) / (deg_in(v) + deg_out(v) + ε) × (flow_out(v) / flow_total)
```

#### Step 4: Community Detection

Use Louvain algorithm to detect communities:

```python
def detect_communities(graph):
    partition = louvain_algorithm(graph)
    modularity = calculate_modularity(graph, partition)
    return partition, modularity
```

**Anomaly Indicators:**
- Very small communities (< 5 nodes) with high internal flow
- Communities with single external connection (potential money mule ring)
- Rapidly changing community structure (evasion behavior)

### Scoring Algorithm

**Network Topology Risk Score (0-1):**

```
network_risk = 0.4 × sybil_score_normalized
             + 0.3 × sink_source_score_normalized
             + 0.2 × community_anomaly_normalized
             + 0.1 × centrality_anomaly_normalized
```

**Component Thresholds:**
- Sybil score > 0.7: High confidence Sybil army
- Sink score > 0.8: Likely extraction point
- Community size < 5 with internal flow > 90%: Suspicious cluster

### Implementation Considerations

**Graph Database Requirements:**
- Neo4j or similar for efficient graph queries
- Minimum 30-day transaction history
- Real-time edge insertion capability

**Computational Complexity:**
- Louvain community detection: O(V log V)
- Centrality calculations: O(V × E)
- Sybil detection: O(deg(v)^2) per account

**Real-Time Feasibility:**
- **Incremental updates:** Recalculate affected neighborhoods only
- **Approximation algorithms:** Use sampling for large graphs
- **Target latency:** 50-100ms for neighborhood queries

**False Positive Mitigation:**
1. **Context-aware thresholds** (business accounts have higher legitimate degree)
2. **Temporal persistence** (require anomalous structure to persist)
3. **Cross-validation** (correlate with Economic Rationality signal)

### Detection Capabilities

| Attack Chain | Primary Mechanism | Detection Confidence |
|--------------|-------------------|---------------------|
| History Extraction | Sink node detection | HIGH |
| Agent Army | Sybil detection + hub topology | VERY HIGH |
| Cross-Platform Identity | Community detection across platforms | MEDIUM |
| Swarm Intelligence | Centrality anomalies + rapid community change | HIGH |

---

## Signal 3: Value Flow

### Definition

**Value Flow:** Legitimate commerce follows predictable value flow patterns: money flows from buyers to sellers, clearing through intermediaries, with settlement within expected timeframes. Fraud requires unusual flow structures: rapid reversals, unexplained detours, or extraction through complex paths.

**Agent-Invariance Justification:** Value flow is governed by economic necessity, not actor properties. Money follows predictable patterns regardless of who initiates transactions.

### Measurement Protocol

#### Step 1: Flow Path Reconstruction

For each transaction, reconstruct the complete value flow path:

```
path = [account_0, account_1, ..., account_n]
value_flow = [amount_0, amount_1, ..., amount_n]
timestamps = [t_0, t_1, ..., t_n]
```

**Path Features:**
- `path_length`: Number of accounts in path
- `total_hops`: Number of transactions
- `value_preservation`: `min(value_flow) / max(value_flow)`
- `time_span`: `t_n - t_0`
- `intermediary_count`: Accounts that are neither origin nor final destination

#### Step 2: Flow Anomaly Detection

**1. Rapid Reversal Detection:**
```python
def rapid_reversal_score(path, value_flow, timestamps, threshold_hours=24):
    if len(path) < 3:
        return 0.0

    # Look for value returning to near-origin account
    for i in range(2, len(path)):
        time_diff = (timestamps[i] - timestamps[0]).total_seconds() / 3600
        if time_diff < threshold_hours:
            # Check if value returned to account close to origin
            if similar_account(path[0], path[i]):
                return 1.0  # Definite rapid reversal

    return 0.0
```

**2. Detour Detection:**
```python
def detour_score(path, merchant_categories):
    """
    Detect unnecessary intermediaries in transaction path.
    Legitimate: Consumer → Payment Processor → Merchant
    Suspicious: Consumer → Processor 1 → Processor 2 → ... → Merchant
    """
    # Count payment processors in path
    processor_count = sum(1 for account in path
                         if merchant_categories[account] == 'payment_processor')

    # Legitimate paths have at most 1-2 processors
    if processor_count <= 2:
        return 0.0
    else:
        return min(1.0, (processor_count - 2) / 5)
```

**3. Value Decay Detection:**
```python
def value_decay_score(value_flow):
    """
    Detect value decreasing along path (fee structure abnormal).
    Legitimate: Fees are predictable percentage
    Suspicious: Excessive or unpredictable value loss
    """
    if len(value_flow) < 3:
        return 0.0

    decay_rates = []
    for i in range(1, len(value_flow)):
        decay = (value_flow[i-1] - value_flow[i]) / value_flow[i-1]
        decay_rates.append(decay)

    # High variance in decay rates = suspicious
    return np.std(decay_rates) if len(decay_rates) > 0 else 0.0
```

#### Step 3: Settlement Analysis

**Settlement Consistency:**
```python
def settlement_consistency(transactions):
    """
    Check if transactions settle consistently with their stated purpose.
    """
    unsettled_ratio = count_unsettled(transactions) / len(transactions)
    chargeback_ratio = count_chargebacks(transactions) / len(transactions)
    reversal_ratio = count_reversals(transactions) / len(transactions)

    return 1.0 - (unsettled_ratio + chargeback_ratio + reversal_ratio) / 3
```

#### Step 4: Flow Velocity Analysis

**Flow Velocity:** Speed at which value moves through the system

```python
def flow_velocity_score(path, timestamps, amounts):
    """
    High velocity with large amounts = suspicious (layering)
    """
    velocities = []
    for i in range(1, len(timestamps)):
        time_diff = (timestamps[i] - timestamps[i-1]).total_seconds()
        velocity = amounts[i] / time_diff  # $ per second
        velocities.append(velocity)

    # Normalize by median velocity
    if len(velocities) == 0:
        return 0.0

    median_vel = np.median(velocities)
    if median_vel == 0:
        return 0.0

    # High velocity = suspicious
    return max(0, 1.0 - (1 / (1 + median_vel / 1000)))
```

### Scoring Algorithm

**Value Flow Risk Score (0-1):**

```
value_flow_risk = 0.3 × rapid_reversal_normalized
                + 0.25 × detour_normalized
                + 0.2 × value_decay_normalized
                + 0.15 × settlement_inconsistency_normalized
                + 0.1 × velocity_anomaly_normalized
```

### Implementation Considerations

**Data Requirements:**
- Complete transaction chains (may require inter-bank data)
- Merchant category codes
- Settlement status tracking
- Chargeback and reversal records

**Real-Time Feasibility:**
- **Streaming mode:** Analyze individual transactions as they arrive
- **Batch mode:** Reconstruct paths periodically (hourly/daily)
- **Target latency:** 30-50ms per transaction

**False Positive Mitigation:**
1. **Business type awareness** (crypto exchanges have legitimate high velocity)
2. **Known corridor whitelisting** (established payment routes)
3. **Amount thresholding** (focus on high-value transactions)

### Detection Capabilities

| Attack Chain | Primary Mechanism | Detection Confidence |
|--------------|-------------------|---------------------|
| Async Flooding | Velocity anomaly | HIGH |
| Agent Army | Detour + rapid reversal | MEDIUM |
| Market Manipulation | Value decay + settlement inconsistency | HIGH |

---

## Signal 4: Temporal Consistency

### Definition

**Temporal Consistency:** Legitimate activity exhibits temporal coherence—patterns that make sense given the actor's nature. Humans have circadian patterns; legitimate automation has consistent timing. Fraud requires detectable coordination: precise timing, cross-platform synchronization, or arbitrage patterns.

**Agent-Invariance Justification:** Time is a universal constraint. Coordination leaves detectable temporal signatures regardless of actor type.

### Measurement Protocol

#### Step 1: Temporal Pattern Extraction

For each account, extract temporal features:

```python
temporal_features = {
    'activity_hours': hours_with_activity(account),
    'inter_transaction_times': [t_i - t_{i-1} for all transactions],
    'burstiness': burstiness_score(transactions),
    'periodicity': autocorrelation(transactions),
    'weekend_ratio': weekend_tx / total_tx,
    'night_ratio': night_tx / total_tx
}
```

**Feature Calculations:**

**1. Burstiness Score:**
```python
def burstiness_score(transactions):
    """
    Measure whether transactions are bursty or evenly distributed.
    Fraud: Highly bursty (coordinated attacks)
    Legitimate: More even distribution
    """
    if len(transactions) < 2:
        return 0.0

    intervals = [(t[i] - t[i-1]).total_seconds()
                 for i in range(1, len(transactions))]

    mean_interval = np.mean(intervals)
    std_interval = np.std(intervals)

    if mean_interval == 0:
        return 1.0  # Maximum burstiness

    # Coefficient of variation
    cv = std_interval / mean_interval
    return min(1.0, cv / 2)  # Normalize
```

**2. Periodicity Detection:**
```python
def periodicity_score(timestamps):
    """
    Detect regular patterns (e.g., daily, weekly).
    Legitimate automation: High periodicity
    Fraud adaptation: Low periodicity
    """
    if len(timestamps) < 10:
        return 0.0

    # Convert to seconds since epoch
    seconds = [t.timestamp() for t in timestamps]

    # Autocorrelation at various lags
    max_correlation = 0
    for lag in [3600, 86400, 604800]:  # 1 hour, 1 day, 1 week
        correlation = autocorrelation(seconds, lag)
        max_correlation = max(max_correlation, correlation)

    return max_correlation
```

#### Step 2: Cross-Platform Synchronization Detection

Detect whether accounts on different platforms coordinate activity:

```python
def cross_platform_sync(accounts_by_platform, time_window_seconds=60):
    """
    Detect transactions across platforms occurring within short time window.
    """
    all_txs = []
    for platform, account in accounts_by_platform.items():
        all_txs.extend([(tx, platform) for tx in account.transactions])

    # Sort by timestamp
    all_txs.sort(key=lambda x: x[0].timestamp)

    # Look for clusters of transactions across platforms
    synchronized_clusters = []
    current_cluster = [all_txs[0]]

    for tx, platform in all_txs[1:]:
        time_diff = (tx.timestamp - current_cluster[0][0].timestamp).total_seconds()

        if time_diff < time_window_seconds:
            current_cluster.append((tx, platform))
        else:
            if len(current_cluster) > 1:
                synchronized_clusters.append(current_cluster)
            current_cluster = [(tx, platform)]

    # Score based on cluster properties
    if not synchronized_clusters:
        return 0.0

    # High score if many platforms in clusters
    max_platforms_in_cluster = max(len(set(p for _, p in cluster))
                                   for cluster in synchronized_clusters)

    return min(1.0, (max_platforms_in_cluster - 1) / 5)
```

#### Step 3: Arbitrage Pattern Detection

Detect temporal arbitrage (exploiting timing differences):

```python
def arbitrage_score(transactions_by_platform, time_window_seconds=10):
    """
    Detect near-simultaneous transactions across platforms
    that could indicate arbitrage.
    """
    # Group transactions by time windows
    time_bins = {}
    for platform, txs in transactions_by_platform.items():
        for tx in txs:
            bin_key = int(tx.timestamp.timestamp() / time_window_seconds)
            if bin_key not in time_bins:
                time_bins[bin_key] = []
            time_bins[bin_key].append((tx, platform))

    # Look for bins with multiple platforms
    multi_platform_bins = [bin for bin in time_bins.values()
                          if len(set(p for _, p in bin)) > 1]

    if not multi_platform_bins:
        return 0.0

    # Calculate value flow direction
    arbitrage_events = 0
    for bin in multi_platform_bins:
        amounts_by_platform = {}
        for tx, platform in bin:
            if platform not in amounts_by_platform:
                amounts_by_platform[platform] = 0
            amounts_by_platform[platform] += tx.amount

        # Check if value flows in opposing directions
        # (buy on one platform, sell on another)
        values = list(amounts_by_platform.values())
        if any(v < 0 for v in values) and any(v > 0 for v in values):
            arbitrage_events += 1

    return min(1.0, arbitrage_events / len(multi_platform_bins))
```

#### Step 4: Coherence Analysis

**Temporal Coherence:** Activity makes sense given context

```python
def temporal_coherence(account, context):
    """
    Check if account's activity aligns with:
    - Stated business type
    - Geographic location
    - Known behavioral patterns
    """
    # Business type expectations
    business_expectations = {
        'retail': {'hours': (8, 20), 'weekend_activity': True},
        'crypto_exchange': {'hours': (0, 24), 'weekend_activity': True},
        'payroll': {'hours': (0, 6), 'weekly_pattern': True},
        'restaurant': {'hours': (10, 23), 'weekend_activity': True}
    }

    if account.business_type not in business_expectations:
        return 0.5  # Unknown

    expected = business_expectations[account.business_type]
    actual_hours = account.activity_hours
    actual_weekend = account.weekend_ratio

    # Check hour alignment
    hour_coherence = 1.0 - (abs(actual_hours[0] - expected['hours'][0]) +
                            abs(actual_hours[1] - expected['hours'][1])) / 24

    # Check weekend alignment
    if 'weekend_activity' in expected:
        expected_weekend = 0.3 if expected['weekly_pattern'] else 0.2
        weekend_coherence = 1.0 - abs(actual_weekend - expected_weekend)
    else:
        weekend_coherence = 0.5

    return (hour_coherence + weekend_coherence) / 2
```

### Scoring Algorithm

**Temporal Consistency Risk Score (0-1):**

```
temporal_risk = 0.3 × synchronization_normalized
             + 0.25 × burstiness_normalized
             + 0.2 × arbitrage_normalized
             + 0.15 × incoherence_normalized
             + 0.1 × periodicity_break_normalized
```

**Component Interpretations:**
- **High synchronization:** Coordinated attack (suspicious)
- **High burstiness:** Fraud pattern (suspicious)
- **High arbitrage:** Market manipulation (suspicious)
- **High incoherence:** Activity doesn't match stated business (suspicious)
- **Low periodicity:** Behavioral adaptation/evasion (suspicious)

### Implementation Considerations

**Data Requirements:**
- Precise timestamps (millisecond granularity preferred)
- Cross-platform transaction correlation (requires data sharing)
- Account business type metadata

**Real-Time Feasibility:**
- **Sliding window:** Maintain temporal features over rolling window
- **Approximate synchronization:** Use time bins rather than exact matching
- **Target latency:** 20-40ms per transaction

**False Positive Mitigation:**
1. **Business type whitelisting** (legitimate high-frequency trading)
2. **Geographic awareness** (different time zones)
3. **Known event awareness** (scheduled bulk processing)

### Detection Capabilities

| Attack Chain | Primary Mechanism | Detection Confidence |
|--------------|-------------------|---------------------|
| Swarm Intelligence | Synchronization + burstiness | VERY HIGH |
| Behavioral Mimicry | Periodicity break + adaptation | HIGH |
| Cross-Platform Identity | Cross-platform sync detection | HIGH |
| Async Flooding | Burstiness + incoherence | MEDIUM |

---

## Signal 5: Cross-Platform Correlation

### Definition

**Cross-Platform Correlation:** Legitimate actors have consistent identity and behavior across platforms. Fraudsters engage in platform-hopping—creating new identities per platform to evade detection. Cross-platform correlation tracks identity across platforms and detects evasion patterns.

**Agent-Invariance Justification:** Legitimate economic entities have reasons for multi-platform presence (business needs, customer access). Fraud creates fragmented, inconsistent cross-platform patterns.

### Measurement Protocol

#### Step 1: Identity Linkage

**Privacy-Preserving Identity Linkage:**

**Approach 1: Cryptographic Hashing**
```python
def create_identity_hash(account_data, salt):
    """
    Create deterministic hash from identity attributes
    without exposing raw data.
    """
    # Hash of stable identity attributes
    attributes = {
        'legal_name': account_data.legal_name,
        'tax_id': account_data.tax_id,
        'business_registration': account_data.registration_number
    }

    # Canonicalize and hash
    canonical = json.dumps(attributes, sort_keys=True)
    hash_value = hashlib.sha256((canonical + salt).encode()).hexdigest()

    return hash_value
```

**Approach 2: Behavioral Fingerprinting**
```python
def behavioral_fingerprint(transactions):
    """
    Create fingerprint from behavioral patterns (not PII).
    """
    features = {
        'transaction_amount_distribution': quantile_bins(transactions.amounts),
        'timing_pattern': histogram(transactions.timestamps, bins=24),
        'counterparty_distribution': top_counterparties(transactions, n=10),
        'merchant_category_distribution': category_counts(transactions)
    }

    # Vectorize and hash
    vector = vectorize(features)
    fingerprint = hashlib.sha256(vector.tobytes()).hexdigest()

    return fingerprint
```

#### Step 2: Correlation Scoring

**Identity Consistency Score:**
```python
def identity_consistency_score(identity_by_platform):
    """
    Measure how consistent identity is across platforms.
    """
    platforms = list(identity_by_platform.keys())

    if len(platforms) < 2:
        return 1.0  # Single platform = N/A

    scores = []

    # Compare each pair of platforms
    for i, p1 in enumerate(platforms):
        for p2 in platforms[i + 1:]:
            id1 = identity_by_platform[p1]
            id2 = identity_by_platform[p2]

            # Check if identities match
            if id1['identity_hash'] == id2['identity_hash']:
                # Same legal entity
                scores.append(1.0)
            elif id1['behavioral_fp'] == id2['behavioral_fp']:
                # Likely same entity (behavioral match)
                scores.append(0.8)
            else:
                # Different entities
                scores.append(0.0)

    return np.mean(scores)
```

**Behavioral Correlation Score:**
```python
def behavioral_correlation_score(behaviors_by_platform):
    """
    Measure correlation of behavioral patterns across platforms.
    """
    platforms = list(behaviors_by_platform.keys())

    if len(platforms) < 2:
        return 1.0

    correlations = []

    for i, p1 in enumerate(platforms):
        for p2 in platforms[i + 1:]:
            b1 = behaviors_by_platform[p1]
            b2 = behaviors_by_platform[p2]

            # Correlate feature vectors
            corr = cosine_similarity(b1['feature_vector'], b2['feature_vector'])
            correlations.append(corr)

    return np.mean(correlations)
```

#### Step 3: Platform-Hopping Detection

**Platform-Hopping Pattern:** Rapid creation of new identities on different platforms

```python
def platform_hopping_score(identity_timeline):
    """
    Detect rapid identity creation across platforms.
    """
    if len(identity_timeline) < 2:
        return 0.0

    # Sort by creation time
    timeline = sorted(identity_timeline, key=lambda x: x['created_at'])

    # Calculate time between identity creations
    intervals = []
    for i in range(1, len(timeline)):
        interval = (timeline[i]['created_at'] -
                   timeline[i-1]['created_at']).total_seconds()
        intervals.append(interval)

    # Short intervals = suspicious
    short_intervals = [i for i in intervals if i < 86400]  # < 1 day
    score = len(short_intervals) / len(intervals)

    return score
```

#### Step 4: Evasion Pattern Detection

**Evasion Indicators:**
- Identity closed on one platform, opened on another
- Similar behavioral pattern but different identity
- Timing correlation between platform exit and new platform entry

```python
def evasion_score(platform_history):
    """
    Detect evasion patterns across platforms.
    """
    evasion_indicators = []

    for event in platform_history:
        # Check for exit followed by new entry
        if event['action'] == 'closed':
            # Look for new account creation within 7 days
            subsequent_creates = [e for e in platform_history
                                if e['action'] == 'created' and
                                0 < (e['timestamp'] - event['timestamp']).total_seconds() < 604800]

            if subsequent_creates:
                evasion_indicators.append(1.0)

        # Check for behavioral similarity with different identity
        if event.get('behavioral_mismatch', False):
            evasion_indicators.append(1.0)

    if not evasion_indicators:
        return 0.0

    return np.mean(evasion_indicators)
```

### Scoring Algorithm

**Cross-Platform Risk Score (0-1):**

```
cross_platform_risk = 0.4 × platform_hopping_normalized
                   + 0.3 × evasion_normalized
                   + 0.2 × identity_inconsistency_normalized
                   + 0.1 × behavioral_mismatch_normalized
```

### Implementation Considerations

**Privacy Preservation:**
- Use cryptographic hashing, not raw identity data
- Federated learning: Compute correlations without data sharing
- Secure multi-party computation for cross-platform queries

**Data Sharing Requirements:**
- Cross-platform data sharing agreements
- API access to other platforms' identity hashes
- Real-time or batch correlation updates

**Real-Time Feasibility:**
- **Batch mode:** Daily correlation updates (privacy-preserving)
- **Real-time mode:** Hash-based queries for known identities
- **Target latency:** 100-200ms for cross-platform lookup

**False Positive Mitigation:**
1. **Legitimate multi-platform business** (whitelist known entities)
2. **Business expansion** (new platforms for legitimate reasons)
3. **Mergers and acquisitions** (identity consolidation)

### Detection Capabilities

| Attack Chain | Primary Mechanism | Detection Confidence |
|--------------|-------------------|---------------------|
| Cross-Platform Identity | Platform-hopping + evasion | VERY HIGH |
| Behavioral Mimicry | Behavioral mismatch + evasion | HIGH |
| Agent Army | Identity inconsistency | MEDIUM |

---

## Signal Integration and Fusion

### Fusion Architecture

**Layer 1: Signal Normalization**
```python
def normalize_signals(signals):
    """
    Normalize all signals to [0, 1] range with consistent interpretation
    (0 = low risk, 1 = high risk).
    """
    normalized = {}
    for name, value in signals.items():
        if name in signal_ranges:
            min_val, max_val = signal_ranges[name]
            normalized[name] = (value - min_val) / (max_val - min_val)
        else:
            normalized[name] = value  # Already normalized
    return normalized
```

**Layer 2: Weighted Ensemble**
```python
def weighted_ensemble(normalized_signals, weights):
    """
    Combine signals using learned weights.
    """
    risk_score = 0.0
    for signal_name, weight in weights.items():
        if signal_name in normalized_signals:
            risk_score += weight * normalized_signals[signal_name]

    # Normalize weights
    total_weight = sum(weights.values())
    return risk_score / total_weight
```

**Default Weights:**
```python
default_weights = {
    'economic_rationality': 0.25,
    'network_topology': 0.25,
    'value_flow': 0.20,
    'temporal_consistency': 0.15,
    'cross_platform': 0.15
}
```

**Layer 3: Adaptive Weighting**
```python
def adaptive_weights(performance_history):
    """
    Adjust weights based on historical performance.
    Signals with higher precision get higher weights.
    """
    base_weights = default_weights.copy()

    for signal_name, history in performance_history.items():
        # Calculate precision (TP / (TP + FP))
        precision = history['true_positives'] / (history['true_positives'] +
                                                 history['false_positives'] + 1)

        # Adjust weight based on precision
        adjustment = precision / 0.5  # 0.5 is baseline
        base_weights[signal_name] *= adjustment

    # Re-normalize
    total = sum(base_weights.values())
    return {k: v / total for k, v in base_weights.items()}
```

### Confidence Estimation

```python
def estimate_confidence(risk_score, signals, calibration_data):
    """
    Estimate confidence in risk score based on:
    1. Signal agreement (do signals agree?)
    2. Historical calibration (how accurate is this score range?)
    """
    # 1. Signal agreement (std dev of normalized signals)
    signal_values = list(signals.values())
    agreement = 1.0 - np.std(signal_values)

    # 2. Historical calibration
    score_range = int(risk_score * 10)  # 0-10 bins
    calibration = calibration_data[score_range]['accuracy']

    # Combine
    confidence = (agreement + calibration) / 2

    return confidence
```

### Threshold Strategy

**Dynamic Thresholding:**
```python
def dynamic_threshold(risk_scores, confidence_scores, target_fpr=0.01):
    """
    Set threshold to achieve target false positive rate.
    """
    # Sort by risk score
    sorted_indices = np.argsort(risk_scores)

    # Find threshold where predicted FPR matches target
    cumulative_fpr = 0.0
    threshold_idx = 0

    for idx in sorted_indices:
        # Weight FPR contribution by confidence
        cumulative_fpr += (1 - confidence_scores[idx]) / len(risk_scores)

        if cumulative_fpr > target_fpr:
            threshold_idx = idx
            break

    threshold = risk_scores[sorted_indices[threshold_idx]]
    return threshold
```

**Threshold Tiers:**
| Tier | Risk Range | Action |
|------|-----------|--------|
| **ALLOW** | 0.0 - 0.3 | Process normally |
| **FLAG** | 0.3 - 0.6 | Queue for review |
| **BLOCK** | 0.6 - 0.8 | Block, require verification |
| **INVESTIGATE** | 0.8 - 1.0 | Block, escalate to fraud team |

---

## Summary and Validation

### Signal Specification Summary

| Signal | Agent-Invariance | Data Requirements | Latency Target |
|--------|------------------|-------------------|----------------|
| Economic Rationality | Economic necessity | 30-day tx history | 20-50ms |
| Network Topology | Network structure | Transaction graph | 50-100ms |
| Value Flow | Value conservation | Transaction chains | 30-50ms |
| Temporal Consistency | Time universality | Precise timestamps | 20-40ms |
| Cross-Platform | Platform-spanning | Cross-platform data | 100-200ms |

### Acceptance Test Results

**FRAM-02: Agent-Invariant Signals Specified ✓ PASSED**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| ≥3 agent-invariant signals specified | ✓ PASS | 5 signals fully specified |
| Each signal has measurement protocol | ✓ PASS | All 5 have detailed protocols |
| Agent-invariance justified | ✓ PASS | Each signal justified with necessity |
| Signal integration logic documented | ✓ PASS | Fusion architecture specified |
| False positive mitigation addressed | ✓ PASS | Mitigation strategies for each signal |

### Implementation Readiness

**Ready for Implementation:**
- Economic Rationality Signal (clear protocols, low latency)
- Temporal Consistency Signal (well-defined features)
- Network Topology Signal (established algorithms)

**Requires Additional Design:**
- Cross-Platform Correlation (privacy-preserving protocols)
- Value Flow (inter-bank data requirements)

**Next Phase:** Plan 03-03 will address privacy preservation requirements and constraints.

---

**Document Status:** COMPLETE
**Companion Document:** `analysis/signal-measurement-protocols.md` (implementation details)
