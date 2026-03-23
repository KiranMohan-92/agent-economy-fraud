# Signal Measurement Protocols

**Phase:** 03-detection-framework, Plan 03-02
**Created:** 2026-03-22
**Status:** Complete

## Overview

This document provides implementation-level protocols for measuring the 5 agent-invariant signals. Each protocol includes data schemas, algorithms, pseudocode, and computational requirements.

---

## Protocol 1: Economic Rationality Measurement

### Data Schema

```sql
-- Transaction Table
CREATE TABLE transactions (
    transaction_id VARCHAR(64) PRIMARY KEY,
    from_account VARCHAR(64) NOT NULL,
    to_account VARCHAR(64) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_category VARCHAR(32),
    settlement_status ENUM('pending', 'cleared', 'failed', 'reversed'),
    metadata JSON,
    INDEX idx_from_account (from_account),
    INDEX idx_to_account (to_account),
    INDEX idx_timestamp (timestamp)
);

-- Account State Table (for streaming updates)
CREATE TABLE account_state (
    account VARCHAR(64) PRIMARY KEY,
    total_sent DECIMAL(20, 2) DEFAULT 0,
    total_received DECIMAL(20, 2) DEFAULT 0,
    transaction_count INT DEFAULT 0,
    unique_counterparties INT DEFAULT 0,
    last_updated TIMESTAMP,
    utility_score DECIMAL(10, 4) DEFAULT 0
);
```

### Streaming Update Algorithm

```python
def update_account_state(transaction):
    """
    Streaming update: called on each transaction.
    Maintains running totals for economic rationality scoring.
    """
    from_acc = transaction.from_account
    to_acc = transaction.to_account
    amount = transaction.amount

    # Update sender state
    update_account(from_acc, amount_sent=amount)

    # Update receiver state
    update_account(to_acc, amount_received=amount)

    # Calculate utility deviation
    from_utility = calculate_utility_deviation(from_acc)
    to_utility = calculate_utility_deviation(to_acc)

    # Flag if anomalous
    if from_utility > UTILITY_THRESHOLD or to_utility > UTILITY_THRESHOLD:
        flag_for_review(from_acc, to_acc, transaction, from_utility, to_utility)

def update_account(account, amount_sent=0, amount_received=0):
    """
    Atomic update of account state.
    """
    state = get_or_create_account_state(account)

    state.total_sent += amount_sent
    state.total_received += amount_received
    state.transaction_count += 1
    state.utility_score = (state.total_received - state.total_sent) / (
        state.total_sent + state.total_received + 1.0
    )
    state.last_updated = current_timestamp()

    save_account_state(account, state)
```

### Circular Flow Detection (Batch)

```python
def detect_circular_flows(time_window_hours=24, max_depth=6):
    """
    Batch process: runs every 5-10 minutes.
    Detects circular transaction patterns.
    """
    # Get transactions in time window
    transactions = get_transactions_in_window(
        start_time=now() - timedelta(hours=time_window_hours),
        end_time=now()
    )

    # Build directed graph
    graph = build_transaction_graph(transactions)

    # Detect cycles using DFS with depth limit
    cycles = []
    visited_global = set()

    for start_node in graph.nodes():
        if start_node not in visited_global:
            path = [start_node]
            visited_local = {start_node}
            dfs_cycles(graph, start_node, start_node, path,
                      visited_local, visited_global, cycles, max_depth)

    # Score cycles
    for cycle in cycles:
        cycle_amount = sum(edge_amount for edge_amount in cycle_path_amounts(cycle))
        if cycle_amount > CYCLE_AMOUNT_THRESHOLD:
            alert_circular_flow(cycle, cycle_amount)

def dfs_cycles(graph, current, start, path, visited_local,
              visited_global, cycles, depth):
    """
    Depth-limited DFS for cycle detection.
    """
    if depth == 0:
        return

    visited_global.add(current)

    for neighbor in graph.neighbors(current):
        if neighbor == start and len(path) >= 3:
            # Found cycle
            cycles.append(path + [start])
        elif neighbor not in visited_local:
            dfs_cycles(graph, neighbor, start, path + [neighbor],
                     visited_local | {neighbor}, visited_global,
                     cycles, depth - 1)
```

### Scoring Function

```python
def calculate_economic_risk(account, time_window_hours=24):
    """
    Calculate comprehensive economic risk score for account.
    Returns: 0.0 - 1.0 (higher = more risky)
    """
    state = get_account_state(account)
    transactions = get_account_transactions(
        account,
        start_time=now() - timedelta(hours=time_window_hours)
    )

    if not transactions:
        return 0.0

    # Component 1: Utility Deviation
    utility_dev = abs(state.utility_score)

    # Component 2: Circular Flow
    circular_tx = detect_cycles_involving_account(account, transactions)
    circular_ratio = sum(tx.amount for tx in circular_tx) / (
        sum(tx.amount for tx in transactions) + 1.0
    )

    # Component 3: Purpose Deviation
    expected_volume = get_expected_volume_for_account_type(account)
    actual_volume = len(transactions)
    purpose_dev = min(1.0, actual_volume / (expected_volume + 1))

    # Component 4: Value Concentration
    amounts_by_counterparty = group_amounts_by_counterparty(transactions)
    max_amount = max(amounts_by_counterparty.values())
    total_amount = sum(amounts_by_counterparty.values())
    concentration = max_amount / (total_amount + 1.0)

    # Weighted combination
    risk = (
        0.4 * utility_dev +
        0.3 * circular_ratio +
        0.2 * purpose_dev +
        0.1 * concentration
    )

    return min(1.0, risk)
```

### Computational Requirements

| Operation | Complexity | Frequency | Latency Target |
|-----------|------------|-----------|----------------|
| Account state update | O(1) | Per transaction | 5-10ms |
| Utility calculation | O(1) | Per transaction | <5ms |
| Circular flow detection | O(V^d) | Every 5 min | 1-5s (batch) |
| Risk scoring | O(E) | Per account | 20-30ms |

---

## Protocol 2: Network Topology Measurement

### Data Schema (Graph Database)

```cypher
-- Neo4j/Cypher schema

-- Account nodes
CREATE (acc:Account {
    id: "acc_12345",
    type: "individual|business",
    created_at: timestamp(),
    risk_score: 0.0,
    last_activity: timestamp()
})

-- Transaction relationships
CREATE (acc1)-[:SENT {
    amount: 1000.00,
    currency: "USD",
    timestamp: timestamp(),
    merchant_category: "retail"
}]->(acc2)

-- Account attributes
CREATE (acc)-[:HAS_ATTRIBUTE {
    attribute: "kyc_verified",
    value: true,
    since: timestamp()
}]->(:Attribute)
```

### Sybil Detection Algorithm

```python
def detect_sybil_accounts(target_account, lookback_days=30):
    """
    Detect if target_account is part of Sybil army.
    Returns: sybil_score (0.0 - 1.0)
    """
    # Get ego network: target + 2-hop neighbors
    ego_network = get_ego_network(target_account, hops=2)

    if len(ego_network) < 3:
        return 0.0

    # Calculate components

    # 1. Star topology score
    star_score = calculate_star_topology(target_account, ego_network)

    # 2. Interconnectivity among neighbors
    neighbors = get_immediate_neighbors(target_account)
    interconnect_score = calculate_interconnectivity(neighbors, ego_network)

    # 3. Temporal correlation (account creation times)
    creation_times = {acc: acc.created_at for acc in neighbors}
    temporal_score = calculate_temporal_correlation(creation_times)

    # 4. Behavioral similarity
    behaviors = {acc: get_behavioral_fingerprint(acc) for acc in neighbors}
    similarity_score = calculate_behavioral_similarity(behaviors)

    # Weighted combination
    sybil_score = (
        0.3 * star_score +
        0.3 * (1.0 - interconnect_score) +
        0.2 * temporal_score +
        0.2 * similarity_score
    )

    return sybil_score

def calculate_star_topology(center, ego_network):
    """
    High score if neighbors don't connect to each other (star pattern).
    """
    neighbors = get_immediate_neighbors(center)
    if len(neighbors) < 3:
        return 0.0

    # Count edges among neighbors
    internal_edges = 0
    for n1 in neighbors:
        for n2 in neighbors:
            if n1 != n2 and has_edge(n1, n2):
                internal_edges += 1

    # Expected edges in random graph
    expected_edges = len(neighbors) * (len(neighbors) - 1)

    if expected_edges == 0:
        return 0.0

    return 1.0 - (internal_edges / expected_edges)

def calculate_temporal_correlation(creation_times, window_hours=24):
    """
    High score if accounts created within short time window.
    """
    if len(creation_times) < 3:
        return 0.0

    times = list(creation_times.values())
    time_span = max(times) - min(times)

    # Convert to hours
    span_hours = time_span.total_seconds() / 3600

    if span_hours < window_hours:
        return 1.0
    else:
        return max(0.0, 1.0 - span_hours / (24 * 7))  # Decay over week
```

### Community Detection (Louvain)

```python
def detect_fraud_communities(graph, min_community_size=3):
    """
    Use Louvain algorithm to detect anomalous communities.
    """
    # Run Louvain community detection
    partition = louvain(graph)

    # Analyze each community
    anomalous_communities = []

    for community_id in set(partition.values()):
        members = [node for node, comm in partition.items()
                   if comm == community_id]

        if len(members) < min_community_size:
            continue

        # Calculate community metrics
        internal_flow = calculate_internal_flow(members, graph)
        external_flow = calculate_external_flow(members, graph)
        flow_ratio = internal_flow / (internal_flow + external_flow + 1)

        # Check for anomalous patterns
        if flow_ratio > 0.9:  # 90% internal flow = suspicious
            anomalous_communities.append({
                'id': community_id,
                'members': members,
                'size': len(members),
                'internal_flow_ratio': flow_ratio,
                'anomaly_type': 'closed_group'
            })

    return anomalous_communities
```

### Sink/Source Detection

```python
def detect_sink_source_accounts(time_window_days=7, threshold_ratio=0.8):
    """
    Detect sink (receives mostly) and source (sends mostly) accounts.
    """
    accounts = get_active_accounts(
        start_time=now() - timedelta(days=time_window_days)
    )

    sinks = []
    sources = []

    for account in accounts:
        stats = get_account_flow_stats(account, time_window_days)

        # Sink: receives much more than sends
        if stats['total_received'] > 0:
            receive_ratio = stats['total_inflow'] / (
                stats['total_inflow'] + stats['total_outflow'] + 1.0
            )
            if receive_ratio > threshold_ratio:
                sinks.append({
                    'account': account,
                    'ratio': receive_ratio,
                    'total_received': stats['total_received']
                })

        # Source: sends much more than receives
        if stats['total_sent'] > 0:
            send_ratio = stats['total_outflow'] / (
                stats['total_inflow'] + stats['total_outflow'] + 1.0
            )
            if send_ratio > threshold_ratio:
                sources.append({
                    'account': account,
                    'ratio': send_ratio,
                    'total_sent': stats['total_sent']
                })

    return sinks, sources
```

### Computational Requirements

| Operation | Complexity | Frequency | Latency Target |
|-----------|------------|-----------|----------------|
| Ego network query | O(k^d) where k=avg degree, d=hops | On demand | 50-100ms |
| Sybil detection | O(deg(v)^2) | Per account | 30-50ms |
| Louvain community | O(V log V) | Hourly | 5-30s |
| Sink/source detection | O(V + E) | Hourly | 1-5s |

---

## Protocol 3: Value Flow Measurement

### Data Schema

```sql
-- Transaction Chain Table
CREATE TABLE transaction_chains (
    chain_id VARCHAR(64) PRIMARY KEY,
    origin_account VARCHAR(64) NOT NULL,
    final_account VARCHAR(64),
    hop_count INT NOT NULL,
    total_amount DECIMAL(20, 2) NOT NULL,
    final_amount DECIMAL(20, 2),
    value_decay DECIMAL(10, 4),
    duration_seconds INT,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    INDEX idx_origin (origin_account),
    INDEX idx_final (final_account)
);

-- Chain Steps (for path reconstruction)
CREATE TABLE chain_steps (
    step_id VARCHAR(64) PRIMARY KEY,
    chain_id VARCHAR(64) NOT NULL,
    step_order INT NOT NULL,
    from_account VARCHAR(64) NOT NULL,
    to_account VARCHAR(64) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_category VARCHAR(32),
    FOREIGN KEY (chain_id) REFERENCES transaction_chains(chain_id),
    INDEX idx_chain_order (chain_id, step_order)
);
```

### Path Reconstruction Algorithm

```python
def reconstruct_value_flow(transaction, max_hops=10, max_age_hours=168):
    """
    Reconstruct complete value flow path starting from transaction.
    """
    path = []
    visited = set()
    current_tx = transaction

    while current_tx and len(path) < max_hops:
        path.append({
            'tx_id': current_tx.id,
            'from': current_tx.from_account,
            'to': current_tx.to_account,
            'amount': current_tx.amount,
            'timestamp': current_tx.timestamp
        })

        visited.add(current_tx.id)

        # Find incoming transaction to current_tx.from_account
        # (money coming into sender)
        incoming_tx = find_incoming_transaction(
            account=current_tx.from_account,
            after_timestamp=current_tx.timestamp - timedelta(hours=max_age_hours),
            exclude=visited
        )

        current_tx = incoming_tx

    # Reverse path (we traced backwards)
    path.reverse()

    return path

def find_incoming_transaction(account, after_timestamp, exclude):
    """
    Find transaction that brought money INTO account.
    """
    query = """
        SELECT * FROM transactions
        WHERE to_account = %s
          AND timestamp > %s
          AND settlement_status = 'cleared'
        ORDER BY timestamp ASC
        LIMIT 1
    """

    results = execute_query(query, (account, after_timestamp))

    for tx in results:
        if tx.id not in exclude:
            return tx

    return None
```

### Rapid Reversal Detection

```python
def detect_rapid_reversal(path, threshold_hours=24):
    """
    Detect if value returns to near-origin in short time.
    """
    if len(path) < 3:
        return {'detected': False, 'score': 0.0}

    origin = path[0]['from']
    origin_similar = [origin]  # Could include related accounts

    for i in range(2, len(path)):
        current = path[i]

        # Check if recipient is similar to origin
        if current['to'] in origin_similar:
            time_diff = (current['timestamp'] - path[0]['timestamp']).total_seconds() / 3600

            if time_diff < threshold_hours:
                return {
                    'detected': True,
                    'score': 1.0 - (time_diff / threshold_hours),
                    'cycle_length': i,
                    'amount_returned': current['amount']
                }

    return {'detected': False, 'score': 0.0}
```

### Detour Detection

```python
def detect_detours(path, merchant_categories):
    """
    Detect unnecessary intermediaries in transaction path.
    """
    if len(path) < 3:
        return {'detected': False, 'score': 0.0}

    # Count payment processors in path
    processor_count = 0
    for step in path:
        cat = merchant_categories.get(step['to'], 'unknown')
        if cat == 'payment_processor':
            processor_count += 1

    # Legitimate: at most 1-2 processors (sender -> processor -> receiver)
    # Suspicious: many processors (layering)
    if processor_count <= 2:
        return {'detected': False, 'score': 0.0}

    excess_processors = processor_count - 2
    score = min(1.0, excess_processors / 5)

    return {
        'detected': True,
        'score': score,
        'processor_count': processor_count,
        'excess_processors': excess_processors
    }
```

### Settlement Analysis

```python
def analyze_settlement_risk(account, days=30):
    """
    Analyze settlement patterns for account.
    """
    txs = get_account_transactions(account, days=days)

    if not txs:
        return 0.0

    counts = {
        'unsettled': 0,
        'chargeback': 0,
        'reversed': 0,
        'total': len(txs)
    }

    for tx in txs:
        if tx.settlement_status == 'pending':
            counts['unsettled'] += 1
        elif tx.settlement_status == 'reversed':
            counts['reversed'] += 1
        elif tx.settlement_status == 'chargeback':
            counts['chargeback'] += 1

    # Calculate risk
    unsettled_ratio = counts['unsettled'] / counts['total']
    problem_ratio = (counts['chargeback'] + counts['reversed']) / counts['total']

    risk_score = 0.5 * unsettled_ratio + 0.5 * problem_ratio

    return min(1.0, risk_score * 5)  # Amplify for significance
```

### Computational Requirements

| Operation | Complexity | Frequency | Latency Target |
|-----------|------------|-----------|----------------|
| Path reconstruction | O(hops × query) | Per transaction | 30-50ms |
| Rapid reversal check | O(path_length) | Per path | <10ms |
| Detour detection | O(path_length) | Per path | <10ms |
| Settlement analysis | O(txs) | Hourly per account | 20-40ms |

---

## Protocol 4: Temporal Consistency Measurement

### Data Schema

```sql
-- Temporal Features Table (pre-computed)
CREATE TABLE temporal_features (
    account VARCHAR(64) PRIMARY KEY,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,

    -- Activity metrics
    transaction_count INT NOT NULL,
    unique_days INT NOT NULL,

    -- Timing metrics
    avg_interval_seconds DECIMAL(15, 2),
    std_interval_seconds DECIMAL(15, 2),
    burstiness_score DECIMAL(10, 4),

    -- Hour of day distribution (24 buckets)
    hour_distribution JSON,

    -- Day of week distribution (7 buckets)
    dow_distribution JSON,

    -- Coherence metrics
    expected_hours JSON,  -- {start, end} based on business type
    hour_coherence DECIMAL(10, 4),
    weekend_coherence DECIMAL(10, 4),

    last_updated TIMESTAMP,
    INDEX idx_window (window_start, window_end)
);
```

### Temporal Feature Extraction

```python
def extract_temporal_features(account, window_hours=24):
    """
    Extract temporal features for account over sliding window.
    """
    transactions = get_account_transactions(
        account,
        start_time=now() - timedelta(hours=window_hours)
    )

    if not transactions:
        return None

    timestamps = [tx.timestamp for tx in transactions]

    # Basic metrics
    tx_count = len(transactions)
    unique_days = len(set(ts.date() for ts in timestamps))

    # Inter-transaction times
    if len(timestamps) > 1:
        intervals = [(timestamps[i] - timestamps[i-1]).total_seconds()
                    for i in range(1, len(timestamps))]
        avg_interval = np.mean(intervals)
        std_interval = np.std(intervals)

        # Burstiness (Fano factor: variance / mean)
        burstiness = (std_interval ** 2) / (avg_interval + 1) if avg_interval > 0 else 0
    else:
        avg_interval = 0
        std_interval = 0
        burstiness = 0

    # Hour distribution
    hour_dist = [0] * 24
    for ts in timestamps:
        hour_dist[ts.hour] += 1
    hour_dist = [count / tx_count for count in hour_dist]

    # Day of week distribution
    dow_dist = [0] * 7
    for ts in timestamps:
        dow_dist[ts.weekday()] += 1
    dow_dist = [count / tx_count for count in dow_dist]

    # Calculate activity hours (peak hours)
    hour_sums = [0] * 24
    for ts in timestamps:
        hour_sums[ts.hour] += 1

    # Find contiguous block containing 80% of activity
    sorted_hours = sorted(range(24), key=lambda h: hour_sums[h], reverse=True)
    top_hours = sorted_hours[:int(0.8 * len([h for h in hour_sums if h > 0]))]

    if top_hours:
        activity_hours = (min(top_hours), max(top_hours))
    else:
        activity_hours = (9, 17)  # Default business hours

    return {
        'account': account,
        'window_start': min(timestamps),
        'window_end': max(timestamps),
        'transaction_count': tx_count,
        'unique_days': unique_days,
        'avg_interval_seconds': avg_interval,
        'std_interval_seconds': std_interval,
        'burstiness_score': min(1.0, burstiness),
        'hour_distribution': hour_dist,
        'dow_distribution': dow_dist,
        'activity_hours': activity_hours
    }
```

### Cross-Platform Synchronization

```python
def detect_cross_platform_sync(account_identities, time_window_seconds=60):
    """
    Detect synchronized transactions across platforms.
    """
    # Collect all transactions across platforms
    all_transactions = []
    for platform, account_id in account_identities.items():
        txs = get_cross_platform_transactions(
            platform,
            account_id,
            start_time=now() - timedelta(hours=24)
        )
        for tx in txs:
            all_transactions.append({
                'tx': tx,
                'platform': platform
            })

    # Sort by timestamp
    all_transactions.sort(key=lambda x: x['tx'].timestamp)

    # Find clusters of transactions within time window
    clusters = []
    current_cluster = [all_transactions[0]]

    for item in all_transactions[1:]:
        time_diff = (item['tx'].timestamp -
                    current_cluster[0]['tx'].timestamp).total_seconds()

        if time_diff < time_window_seconds:
            current_cluster.append(item)
        else:
            if len(current_cluster) > 1:
                clusters.append(current_cluster)
            current_cluster = [item]

    if len(current_cluster) > 1:
        clusters.append(current_cluster)

    # Score based on cluster properties
    if not clusters:
        return 0.0

    # Maximum platforms in any cluster
    max_platforms = max(len(set(item['platform'] for item in cluster))
                       for cluster in clusters)

    # Normalize (3+ platforms = high suspicion)
    return min(1.0, (max_platforms - 1) / 3)
```

### Arbitrage Detection

```python
def detect_arbitrage(account_identities, time_window_seconds=300):
    """
    Detect potential arbitrage: near-simultaneous transactions
    across platforms with opposing value flows.
    """
    # Group transactions by time bins
    bin_size = time_window_seconds
    time_bins = {}

    for platform, account_id in account_identities.items():
        txs = get_cross_platform_transactions(platform, account_id)

        for tx in txs:
            bin_key = int(tx.timestamp.timestamp() / bin_size)
            if bin_key not in time_bins:
                time_bins[bin_key] = []
            time_bins[bin_key].append({
                'platform': platform,
                'amount': tx.amount,
                'direction': 'out' if tx.from_account == account_id else 'in',
                'timestamp': tx.timestamp
            })

    # Look for bins with multi-platform activity
    arbitrage_events = 0
    multi_platform_bins = {k: v for k, v in time_bins.items()
                          if len(set(item['platform'] for item in v)) > 1}

    for bin_items in multi_platform_bins.values():
        # Check for opposing flows
        inflows = sum(item['amount'] for item in bin_items if item['direction'] == 'in')
        outflows = sum(item['amount'] for item in bin_items if item['direction'] == 'out')

        # If both inflows and outflows, potential arbitrage
        if inflows > 0 and outflows > 0:
            arbitrage_events += 1

    if not multi_platform_bins:
        return 0.0

    return min(1.0, arbitrage_events / len(multi_platform_bins))
```

### Computational Requirements

| Operation | Complexity | Frequency | Latency Target |
|-----------|------------|-----------|----------------|
| Temporal feature extraction | O(n log n) for sorting | Per transaction (sliding) | 15-25ms |
| Synchronization detection | O(n log n) | Hourly | 100-200ms |
| Arbitrage detection | O(n) | Hourly | 50-100ms |

---

## Protocol 5: Cross-Platform Correlation Measurement

### Privacy-Preserving Identity Hashing

```python
import hashlib
import json
from cryptography.fernet import Fernet

# Platform-shared secret (established via key exchange)
PLATFORM_SALT = b'shared_secret_key_12345'

def create_identity_hash(account_data, use_fernet=True):
    """
    Create privacy-preserving identity hash.
    Same account data produces same hash across platforms.
    """
    # Stable identity attributes (PII-free where possible)
    stable_attributes = {
        # Use hashed identifiers instead of raw PII
        'legal_name_hash': hash_string(account_data.legal_name),
        'tax_id_hash': hash_string(account_data.tax_id),
        'business_reg_hash': hash_string(account_data.registration_number),
        'country': account_data.country,
        'entity_type': account_data.entity_type  # individual/corporate
    }

    # Canonicalize
    canonical = json.dumps(stable_attributes, sort_keys=True)

    if use_fernet:
        # Encrypt for additional privacy
        f = Fernet(PLATFORM_SALT)
        encrypted = f.encrypt(canonical.encode())
        hash_value = hashlib.sha256(encrypted).hexdigest()
    else:
        # Simple hash with salt
        hash_value = hashlib.sha256((canonical + PLATFORM_SALT.decode()).encode()).hexdigest()

    return hash_value

def hash_string(value):
    """One-way hash for PII."""
    return hashlib.sha256(value.encode()).hexdigest()[:16]
```

### Behavioral Fingerprinting

```python
def create_behavioral_fingerprint(transactions):
    """
    Create fingerprint from transaction behavior (no PII).
    Same behavior patterns produce similar fingerprints.
    """
    if not transactions:
        return None

    # Extract behavioral features
    amounts = [tx.amount for tx in transactions]

    features = {
        # Amount distribution (quantiles)
        'amount_q25': np.percentile(amounts, 25),
        'amount_q50': np.percentile(amounts, 50),
        'amount_q75': np.percentile(amounts, 75),
        'amount_std': np.std(amounts),

        # Timing pattern
        'hour_peak': np.argmax([hour_bucket_count(transactions, h) for h in range(24)]),
        'dow_peak': np.argmax([dow_bucket_count(transactions, d) for d in range(7)]),

        # Counterparty distribution
        'unique_counterparties': len(set(tx.to_account for tx in transactions)),
        'top_counterparty_ratio': top_counterparty_ratio(transactions),

        # Merchant categories
        'category_entropy': calculate_category_entropy(transactions)
    }

    # Vectorize and hash
    vector = np.array(list(features.values()))
    normalized = (vector - vector.min()) / (vector.max() - vector.min() + 1e-10)

    fingerprint = hashlib.sha256(normalized.tobytes()).hexdigest()

    return {
        'fingerprint': fingerprint,
        'features': features,
        'vector': normalized.tolist()
    }
```

### Platform-Hopping Detection

```python
def detect_platform_hopping(account_timeline, suspicious_threshold_hours=24):
    """
    Detect rapid identity creation across platforms.
    """
    if len(account_timeline) < 2:
        return {'detected': False, 'score': 0.0}

    # Sort by creation time
    sorted_timeline = sorted(account_timeline, key=lambda x: x['created_at'])

    # Calculate intervals between identity creations
    intervals = []
    for i in range(1, len(sorted_timeline)):
        interval = (sorted_timeline[i]['created_at'] -
                   sorted_timeline[i-1]['created_at']).total_seconds() / 3600
        intervals.append(interval)

    # Count short intervals
    short_intervals = [i for i in intervals if i < suspicious_threshold_hours]

    if not intervals:
        return {'detected': False, 'score': 0.0}

    score = len(short_intervals) / len(intervals)

    return {
        'detected': score > 0.3,  # 30% rapid hops = suspicious
        'score': score,
        'short_interval_count': len(short_intervals),
        'total_intervals': len(intervals),
        'avg_interval_hours': np.mean(intervals)
    }
```

### Cross-Platform Query Interface

```python
class CrossPlatformCorrelation:
    """
    Interface for privacy-preserving cross-platform queries.
    """

    def __init__(self, platform_endpoints):
        """
        platform_endpoints: dict of {platform_name: api_endpoint}
        """
        self.endpoints = platform_endpoints
        self.cache = {}  # TTL cache

    def query_identity_hash(self, identity_hash, cache_ttl_seconds=300):
        """
        Query all platforms for matching identity hash.
        Returns: dict of {platform: match_info}
        """
        cache_key = f"hash_{identity_hash}"

        if cache_key in self.cache:
            cached, cached_time = self.cache[cache_key]
            if time.time() - cached_time < cache_ttl_seconds:
                return cached

        results = {}
        for platform, endpoint in self.endpoints.items():
            try:
                response = self._make_platform_query(
                    endpoint,
                    {'identity_hash': identity_hash}
                )
                if response.get('found'):
                    results[platform] = response['data']
            except Exception as e:
                # Log error but continue
                log_error(f"Platform query failed for {platform}: {e}")

        self.cache[cache_key] = (results, time.time())
        return results

    def query_behavioral_fingerprint(self, fingerprint, cache_ttl_seconds=300):
        """
        Query all platforms for similar behavioral fingerprints.
        Uses fuzzy matching.
        """
        results = {}
        for platform, endpoint in self.endpoints.items():
            try:
                response = self._make_platform_query(
                    endpoint,
                    {'behavioral_fingerprint': fingerprint,
                     'fuzzy_match': True,
                     'similarity_threshold': 0.8}
                )
                if response.get('found'):
                    results[platform] = response['data']
            except Exception as e:
                log_error(f"Fingerprint query failed for {platform}: {e}")

        return results

    def _make_platform_query(self, endpoint, params):
        """
        Make API request to platform endpoint.
        Implements rate limiting and retry logic.
        """
        # Implementation would use requests/httpx with retry logic
        pass
```

### Computational Requirements

| Operation | Complexity | Frequency | Latency Target |
|-----------|------------|-----------|----------------|
| Identity hash creation | O(1) | Per account | <5ms |
| Behavioral fingerprint | O(n log n) | Daily per account | 50-100ms |
| Platform hopping detection | O(n log n) | Daily | 20-30ms |
| Cross-platform query | O(P) where P=platforms | On demand | 100-200ms |

---

## Signal Fusion and Scoring

### Fusion Algorithm

```python
class SignalFusion:
    """
    Combines all 5 signals into unified risk score.
    """

    def __init__(self, weights=None):
        self.weights = weights or {
            'economic_rationality': 0.25,
            'network_topology': 0.25,
            'value_flow': 0.20,
            'temporal_consistency': 0.15,
            'cross_platform': 0.15
        }

    def calculate_risk_score(self, account, transaction=None):
        """
        Calculate unified risk score for account/transaction.
        Returns: dict with score, confidence, breakdown
        """
        # Collect all signal scores
        signals = {
            'economic_rationality': self.get_economic_score(account, transaction),
            'network_topology': self.get_network_score(account),
            'value_flow': self.get_value_flow_score(account, transaction),
            'temporal_consistency': self.get_temporal_score(account),
            'cross_platform': self.get_cross_platform_score(account)
        }

        # Normalize signals to [0, 1]
        normalized = self.normalize_signals(signals)

        # Calculate weighted score
        weighted_score = sum(
            self.weights.get(signal, 0) * value
            for signal, value in normalized.items()
        )

        # Calculate confidence
        confidence = self.calculate_confidence(normalized)

        # Determine tier
        tier = self.determine_tier(weighted_score)

        return {
            'risk_score': weighted_score,
            'confidence': confidence,
            'tier': tier,
            'signal_breakdown': normalized,
            'timestamp': current_timestamp()
        }

    def normalize_signals(self, signals):
        """
        Ensure all signals are in [0, 1] range.
        """
        normalized = {}
        for name, value in signals.items():
            if value is None:
                normalized[name] = 0.0
            elif isinstance(value, dict):
                # Handle nested signal results
                normalized[name] = value.get('score', 0.0)
            else:
                normalized[name] = max(0.0, min(1.0, float(value)))
        return normalized

    def calculate_confidence(self, normalized_signals):
        """
        Estimate confidence based on signal agreement.
        """
        values = list(normalized_signals.values())

        if not values:
            return 0.0

        # Agreement = 1 - std_dev (high agreement = low std_dev)
        std_dev = np.std(values)
        agreement = max(0.0, 1.0 - std_dev)

        # Availability = what fraction of signals returned valid data
        available = sum(1 for v in values if v > 0 or v < 0)  # Not None
        availability = available / len(values)

        return (agreement + availability) / 2

    def determine_tier(self, score):
        """
        Determine risk tier from score.
        """
        if score < 0.3:
            return 'ALLOW'
        elif score < 0.6:
            return 'FLAG'
        elif score < 0.8:
            return 'BLOCK'
        else:
            return 'INVESTIGATE'
```

### Real-Time Scoring Pipeline

```python
def realtime_scoring_pipeline(transaction):
    """
    Real-time scoring: runs on each transaction.
    Target: <100ms end-to-end.
    """
    start_time = time.time()

    # Step 1: Extract basic features (5ms)
    basic_features = extract_basic_features(transaction)

    # Step 2: Update account states (10ms)
    update_account_state(transaction)

    # Step 3: Calculate Economic Rationality (15ms)
    economic_score = calculate_economic_risk_online(transaction)

    # Step 4: Get cached Network Topology score (20ms)
    network_score = get_cached_network_score(transaction.from_account)

    # Step 5: Get cached Temporal Consistency score (15ms)
    temporal_score = get_cached_temporal_score(transaction.from_account)

    # Step 6: Get cached Cross-Platform score (15ms)
    cross_platform_score = get_cached_cross_platform_score(transaction.from_account)

    # Step 7: Get cached Value Flow score (15ms)
    value_flow_score = get_cached_value_flow_score(transaction)

    # Step 8: Fuse signals (5ms)
    fusion = SignalFusion()
    result = fusion.calculate_risk_score(
        transaction.from_account,
        transaction
    )

    # Step 9: Apply decision rules (5ms)
    decision = apply_decision_rules(result)

    latency_ms = (time.time() - start_time) * 1000

    return {
        'decision': decision,
        'risk_score': result['risk_score'],
        'confidence': result['confidence'],
        'latency_ms': latency_ms
    }

def apply_decision_rules(result):
    """
    Apply tier-based decision rules.
    """
    tier = result['tier']
    confidence = result['confidence']

    # Low confidence: default to more conservative
    if confidence < 0.5:
        if tier == 'ALLOW':
            tier = 'FLAG'
        elif tier == 'FLAG':
            tier = 'BLOCK'

    # Apply tier logic
    if tier == 'ALLOW':
        return {'action': 'allow', 'reason': 'low_risk'}
    elif tier == 'FLAG':
        return {'action': 'flag', 'reason': 'medium_risk_review_recommended'}
    elif tier == 'BLOCK':
        return {'action': 'block', 'reason': 'high_risk_verification_required'}
    else:  # INVESTIGATE
        return {'action': 'block_and_investigate', 'reason': 'very_high_risk_escalate'}
```

---

## Implementation Checklist

### Phase 1: Infrastructure Setup

- [ ] Set up streaming database (account state table)
- [ ] Set up graph database (Neo4j or similar)
- [ ] Set up batch processing pipeline (for heavy computations)
- [ ] Set up caching layer (Redis)
- [ ] Set up monitoring and alerting

### Phase 2: Signal Implementation

- [ ] Economic Rationality: streaming updates + batch cycle detection
- [ ] Network Topology: graph queries + Sybil detection
- [ ] Value Flow: path reconstruction + reversal detection
- [ ] Temporal Consistency: feature extraction + synchronization detection
- [ ] Cross-Platform: identity hashing + platform hopping detection

### Phase 3: Integration

- [ ] Signal fusion algorithm
- [ ] Real-time scoring pipeline
- [ ] Decision rule engine
- [ ] Feedback and adaptation mechanism

### Phase 4: Validation

- [ ] Unit tests for each signal
- [ ] Integration tests for pipeline
- [ ] Performance benchmarks (latency targets)
- [ ] False positive rate analysis

---

**Document Status:** COMPLETE
**Companion Document:** `analysis/agent-invariant-signals.md` (signal specifications)
