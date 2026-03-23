# Synthetic A2A Transaction Data Generation

**Phase:** 04-validation-recommendations, Plan 04-01, Task 1.1
**Created:** 2026-03-23
**Grounded in:** synthetic-data-spec.md (Phase 1), platform analysis (Phase 1)

## Executive Summary

This document describes the implementation of synthetic A2A transaction data generation for validating the agent-aware fraud detection framework. The synthetic data is grounded in platform capabilities analysis (OpenClaw, Moltbook) and literature findings on multi-agent economic systems.

**Key principle:** Every synthetic data generation rule traces back to specific platform capabilities or literature findings. No arbitrary patterns.

---

## 1. Data Generation Framework

### 1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Synthetic Data Generator                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ Benign       │  │ Attack       │  │ Human        │            │
│  │ Generator    │  │ Generator    │  │ Baseline    │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                 │                   │
│         └─────────────────┴─────────────────┘                   │
│                           │                                       │
│                    ┌──────▼───────┐                                │
│                    │  Dataset     │                                │
│                    │  Assembler   │                                │
│                    └──────┬───────┘                                │
│                           │                                       │
└───────────────────────────┼───────────────────────────────────────┘
                            │
                    ┌──────▼───────┐
                    │  Labeled     │
                    │  Validation  │
                    │  Dataset    │
                    └──────────────┘
```

### 1.2 Generator Components

**Benign Agent Transaction Generator:**
- Generates legitimate A2A commerce transactions
- Follows economic rationality principles
- Respects platform rate limits and constraints

**Attack Pattern Generator:**
- Generates all 8 attack chains from attack-chain-mapping.md
- Varies sophistication levels (basic to advanced)
- Includes stealthy patterns that evade simple detection

**Human Baseline Generator:**
- Generates human transaction patterns for comparison
- Uses established velocity and behavioral constraints from literature
- Provides ground truth for "normal" transaction patterns

---

## 2. Synthetic Data Schema

### 2.1 Transaction Record

Each synthetic transaction includes:

```python
@dataclass
class SyntheticTransaction:
    # Core transaction fields
    transaction_id: str                    # Unique identifier
    timestamp: datetime                    # Transaction timestamp
    amount: Decimal                        # Transaction amount
    currency: str                          # Currency code (USD, EUR, etc.)

    # Actor information
    sender_id: str                         # Sender identifier
    sender_type: ActorType                 # HUMAN or AGENT
    receiver_id: str                       # Receiver identifier
    receiver_type: ActorType               # HUMAN or AGENT

    # Transaction metadata
    transaction_type: TransactionType      # PAYMENT, TRANSFER, etc.
    platform: str                          # OpenClaw, Moltbook, or BRIDGE
    purpose: str                            # Transaction purpose/label

    # Behavioral features
    velocity_context: VelocityContext       # Recent transaction count
    device_fingerprint: Optional[str]       # Device ID (humans only)
    location: Optional[Location]           # Location data (humans only)
    session_age: timedelta                # Account/session age

    # Network features
    sender_centrality: float               # Network centrality score
    receiver_centrality: float             # Network centrality score
    path_length: int                       # Transaction path length

    # Value flow features
    circular_flow_score: float             # Circular flow detection
    settlement_velocity: timedelta         # Time to settlement

    # Temporal features
    cross_platform_timing: Optional[timedelta]  # Sync with other platforms

    # Labels (for supervised learning)
    is_fraud: bool                         # Ground truth label
    attack_chain: Optional[str]             # Attack chain ID if fraud
    attack_sophistication: Optional[int]   # 1-5 sophistication level
```

### 2.2 Enum Definitions

```python
class ActorType(Enum):
    HUMAN = "HUMAN"
    AGENT = "AGENT"

class TransactionType(Enum):
    PAYMENT = "PAYMENT"           # Standard payment
    TRANSFER = "TRANSFER"         # Account transfer
    DEPOSIT = "DEPOSIT"           # Deposit to account
    WITHDRAWAL = "WITHDRAWAL"     # Withdrawal from account
    DISBURSEMENT = "DISBURSEMENT" # Payout/distribution
    REPUTATION = "REPUTATION"     # Moltbook upvote
    LISTING_POST = "LISTING"      # Moltbook listing
    LISTING_ACCEPT = "ACCEPT"     # Moltbook accept

class Platform(Enum):
    OPENCLAW = "OPENCLAW"         # Agent gateway
    MOLTBOOK = "MOLTBOOK"         # Agent social platform
    BANKING = "BANKING"           # Traditional banking
    BRIDGE = "BRIDGE"             # Cross-platform bridge
```

---

## 3. Benign Agent Transaction Generation

### 3.1 Legitimate Agent Behavior Model

**Economic Rationality Principle:**
Agents maximize utility within constraints. Benign transactions have clear economic purpose.

**Generation Algorithm:**

```python
def generate_benign_agent_transaction(
    agent_id: str,
    time: datetime,
    network_state: NetworkState
) -> SyntheticTransaction:
    """
    Generate a benign A2A transaction following economic rationality.
    """
    # Select transaction purpose from economic activities
    purpose = random.choice([
        "service_payment",      # Payment for service
        "goods_purchase",       # Purchase goods
        "investment",           # Investment allocation
        "settlement",           # Contract settlement
        "revenue_share"         # Revenue distribution
    ])

    # Amount follows power law (most transactions small, few large)
    amount = generate_power_law_amount(
        min_amount=Decimal("0.01"),
        max_amount=Decimal("10000"),
        exponent=1.5  # Pareto distribution
    )

    # Receiver selection based on network position
    receiver_id = select_economic_counterparty(
        agent_id,
        network_state,
        purpose
    )

    # Velocity follows OpenClaw capabilities
    # (agent can transact up to 900/minute, but benign usage is lower)
    velocity_multiplier = random.uniform(10, 1000)  # 10-1000× human baseline

    return SyntheticTransaction(
        transaction_id=generate_uuid(),
        timestamp=time,
        amount=amount,
        currency="USD",
        sender_id=agent_id,
        sender_type=ActorType.AGENT,
        receiver_id=receiver_id,
        receiver_type=ActorType.AGENT,
        transaction_type=TransactionType.PAYMENT,
        platform=Platform.OPENCLAW,
        purpose=purpose,
        velocity_context=VelocityContext(
            daily_count=random.randint(100, 100000),  # Agent velocity
            weekly_count=random.randint(1000, 500000),
            velocity_multiplier=velocity_multiplier
        ),
        # Agents don't have device/location
        device_fingerprint=None,
        location=None,
        session_age=timedelta(days=random.randint(1, 365)),
        # Network features
        sender_centrality=network_state.get_centrality(agent_id),
        receiver_centrality=network_state.get_centrality(receiver_id),
        path_length=network_state.get_shortest_path_length(agent_id, receiver_id),
        # Value flow features
        circular_flow_score=0.0,  # Benign has low circularity
        settlement_velocity=timedelta(seconds=random.randint(1, 3600)),
        # Labels
        is_fraud=False,
        attack_chain=None,
        attack_sophistication=None
    )
```

### 3.2 Economic Rationality Validation

Each benign transaction is validated for economic rationality:

1. **Utility Maximization:** Both parties benefit (or appear to)
2. **Value Conservation:** Money flows toward value creation
3. **Network Efficiency:** Transactions follow efficient network paths
4. **Purpose Clarity:** Transaction has clear economic purpose

**Rejection Criteria:**
- Circular money flows (A→B→C→A without value creation)
- Systematic value extraction without service
- Transactions that destroy value for all parties

---

## 4. Attack Pattern Generation

### 4.1 Attack Chain Implementations

All 8 attack chains from attack-chain-mapping.md are implemented:

#### Attack Chain 1: Agent Enumeration (EASY detection)

```python
def generate_agent_enumeration_attack(
    attacker_id: str,
    time: datetime,
    network_state: NetworkState
) -> SyntheticTransaction:
    """
    Attack: Agent enumerates other agents via sessions_list.
    Pattern: Many small transactions to different recipients.
    """
    victims = network_state.get_random_agents(count=1000)

    return SyntheticTransaction(
        transaction_id=generate_uuid(),
        timestamp=time,
        amount=Decimal("0.001"),  # Minimum probing amount
        sender_id=attacker_id,
        sender_type=ActorType.AGENT,
        receiver_id=random.choice(victims),
        receiver_type=ActorType.AGENT,
        transaction_type=TransactionType.PAYMENT,
        platform=Platform.OPENCLAW,
        purpose="enumeration_probe",
        # Behavioral signature: many tiny transactions
        velocity_context=VelocityContext(
            daily_count=10000,
            weekly_count=50000,
            velocity_multiplier=100000
        ),
        # Attack indicators
        circular_flow_score=0.9,  # High circularity (probing)
        path_length=1,  # Direct to random victims
        # Labels
        is_fraud=True,
        attack_chain="agent_enumeration",
        attack_sophistication=1  # Low sophistication
    )
```

#### Attack Chain 5: Cross-Platform Identity (IMPOSSIBLE for humans)

```python
def generate_cross_platform_attack(
    attacker_id: str,
    time: datetime,
    moltbook_reputation: float,
    openclaw_sessions: List[str]
) -> List[SyntheticTransaction]:
    """
    Attack: Agent maintains persistent identity across Moltbook and OpenClaw.
    Pattern: Build reputation on Moltbook, then exploit on OpenClaw.

    This is IMPOSSIBLE for humans (requires 1000× speedup).
    """
    transactions = []

    # Phase 1: Rapid reputation building on Moltbook
    for _ in range(10000):  # 10K upvotes in <1 hour
        transactions.append(SyntheticTransaction(
            transaction_id=generate_uuid(),
            timestamp=time + timedelta(microseconds=random.randint(0, 1000000)),
            amount=Decimal("0"),
            sender_id=attacker_id,
            sender_type=ActorType.AGENT,
            receiver_id=f"victim_{random.randint(1, 10000)}",
            receiver_type=ActorType.AGENT,
            transaction_type=TransactionType.REPUTATION,
            platform=Platform.MOLTBOOK,
            purpose="reputation_building",
            velocity_context=VelocityContext(
                daily_count=10000,
                velocity_multiplier=1000000  # Machine-scale
            ),
            # Attack indicators
            circular_flow_score=0.95,
            # Labels
            is_fraud=True,
            attack_chain="cross_platform_identity",
            attack_sophistication=5  # Maximum sophistication
        ))

    # Phase 2: Exploit on OpenClaw using earned reputation
    for session_id in openclaw_sessions:
        transactions.append(SyntheticTransaction(
            transaction_id=generate_uuid(),
            timestamp=time + timedelta(hours=1),
            amount=Decimal("1000"),
            sender_id=attacker_id,
            sender_type=ActorType.AGENT,
            receiver_id=session_id,
            receiver_type=ActorType.AGENT,
            transaction_type=TransactionType.TRANSFER,
            platform=Platform.OPENCLAW,
            purpose="reputation_exploit",
            velocity_context=VelocityContext(
                daily_count=10000,
                velocity_multiplier=1000000
            ),
            # Cross-platform timing signature
            cross_platform_timing=timedelta(seconds=0.001),  # Near-instant coordination
            # Labels
            is_fraud=True,
            attack_chain="cross_platform_identity",
            attack_sophistication=5
        ))

    return transactions
```

#### Attack Chain 8: Market Manipulation (IMPOSSIBLE for humans)

```python
def generate_market_manipulation_attack(
    attacker_id: str,
    time: datetime,
    target_asset: str
) -> List[SyntheticTransaction]:
    """
    Attack: Coordinated market manipulation via cron + browser + exec.
    Pattern: Flash crash, pump-and-dump, or wash trading.

    This is IMPOSSIBLE for humans (requires 24/7 monitoring + coordination).
    """
    transactions = []

    # Phase 1: Accumulation (buy low)
    for _ in range(100):
        transactions.append(SyntheticTransaction(
            transaction_id=generate_uuid(),
            timestamp=time + timedelta(seconds=random.randint(0, 60)),
            amount=Decimal("100") * Decimal(random.randint(1, 10)),
            sender_id=attacker_id,
            sender_type=ActorType.AGENT,
            receiver_id=f"market_maker_{random.randint(1, 100)}",
            receiver_type=ActorType.AGENT,
            transaction_type=TransactionType.PAYMENT,
            platform=Platform.OPENCLAW,
            purpose="accumulation",
            velocity_context=VelocityContext(
                daily_count=10000,
                velocity_multiplier=100000
            ),
            # Value flow signature: money flows to control price
            circular_flow_score=0.8,
            # Labels
            is_fraud=True,
            attack_chain="market_manipulation",
            attack_sophistication=5
        ))

    # Phase 2: Pump (drive up price)
    pump_price_multiplier = random.uniform(1.5, 3.0)

    # Phase 3: Dump (sell at peak)
    for _ in range(100):
        transactions.append(SyntheticTransaction(
            transaction_id=generate_uuid(),
            timestamp=time + timedelta(minutes=30),
            amount=Decimal("100") * Decimal(random.randint(1, 10)),
            sender_id=attacker_id,
            sender_type=ActorType.AGENT,
            receiver_id=f"victim_{random.randint(1, 1000)}",
            receiver_type=ActorType.AGENT,
            transaction_type=TransactionType.SALE,
            platform=Platform.OPENCLAW,
            purpose="dump_distribution",
            velocity_context=VelocityContext(
                daily_count=10000,
                velocity_multiplier=100000
            ),
            # Labels
            is_fraud=True,
            attack_chain="market_manipulation",
            attack_sophistication=5
        ))

    return transactions
```

### 4.2 Attack Sophistication Levels

| Level | Description | Detection Difficulty |
|-------|-------------|----------------------|
| 1 | Simple, obvious patterns | EASY |
| 2 | Basic obfuscation | MEDIUM |
| 3 | Mimics benign behavior | HARD |
| 4 | Adaptive evasion | VERY HARD |
| 5 | Multi-stage coordinated | IMPOSSIBLE (for humans) |

**Sophistication Techniques:**
- Random timing between transactions
- Amount randomization within ranges
- Mixed attack chains (combination of 2+ patterns)
- "Slow and steady" approach (gradual buildup)
- Burst patterns followed by dormancy

---

## 5. Human Baseline Generation

### 5.1 Human Behavioral Constraints

From literature (data-acquisition-plan.md, Section 2.2):

```python
def generate_human_transaction(
    user_id: str,
    time: datetime,
    network_state: NetworkState
) -> SyntheticTransaction:
    """
    Generate human transaction following literature-established constraints.
    """
    # Human velocity: 10-100 transactions/day (Van Vlasselaer 2017)
    daily_count = random.randint(10, 100)

    # Human behavioral constraints
    device_fingerprint = f"device_{hash(user_id) % 10000}"  # Stable device
    location = generate_realistic_location()  # Physical location

    # Amount follows log-normal distribution (human spending patterns)
    amount = generate_log_normal_amount(
        mean=Decimal("50"),
        std_dev=Decimal("200")
    )

    # Transaction timing respects human constraints
    # (sleep, work hours, etc.)
    hour = time.hour
    if 0 <= hour < 6:  # Sleeping hours - low probability
        if random.random() > 0.1:
            return None  # Skip transaction (human asleep)

    return SyntheticTransaction(
        transaction_id=generate_uuid(),
        timestamp=time,
        amount=amount,
        currency="USD",
        sender_id=user_id,
        sender_type=ActorType.HUMAN,
        receiver_id=random.choice(network_state.get_connections(user_id)),
        receiver_type=ActorType.HUMAN,
        transaction_type=random.choice([
            TransactionType.PAYMENT,
            TransactionType.TRANSFER,
            TransactionType.WITHDRAWAL
        ]),
        platform=Platform.BANKING,
        purpose=random.choice([
            "retail_purchase",
            "bill_payment",
            "transfer",
            "cash_withdrawal"
        ]),
        velocity_context=VelocityContext(
            daily_count=daily_count,
            weekly_count=daily_count * 7,
            velocity_multiplier=1.0  # Baseline
        ),
        # Human-specific features
        device_fingerprint=device_fingerprint,
        location=location,
        session_age=timedelta(days=random.randint(30, 365)),
        # Network features
        sender_centrality=network_state.get_centrality(user_id),
        receiver_centrality=network_state.get_centrality(
            random.choice(network_state.get_connections(user_id))
        ),
        path_length=network_state.get_shortest_path_length(
            user_id,
            random.choice(network_state.get_connections(user_id))
        ),
        # Value flow features
        circular_flow_score=0.0,  # Humans have low circularity
        settlement_velocity=timedelta(hours=random.randint(1, 72)),
        # Labels
        is_fraud=False,
        attack_chain=None,
        attack_sophistication=None
    )
```

---

## 6. Dataset Assembly

### 6.1 Dataset Composition

| Category | Count | Percentage |
|----------|-------|------------|
| Benign Human | 50,000 | 50% |
| Benign Agent | 40,000 | 40% |
| Fraud (all chains) | 10,000 | 10% |

**Fraud Distribution by Attack Chain:**

| Attack Chain | Count | Sophistication |
|--------------|-------|----------------|
| Agent Enumeration | 2,000 | 1 |
| History Extraction | 1,000 | 1 |
| Async Flooding | 2,000 | 2 |
| Agent Army | 1,500 | 2 |
| Cross-Platform Identity | 1,000 | 5 |
| Behavioral Mimicry | 500 | 4 |
| Swarm Intelligence | 1,000 | 5 |
| Market Manipulation | 1,000 | 5 |

### 6.2 Temporal Distribution

- **Time span:** 30 days of synthetic transaction activity
- **Distribution:** Transactions distributed across time zones
- **Seasonality:** Weekend/holiday patterns included

---

## 7. Validation Features

### 7.1 Agent-Invariant Signal Features

Each transaction includes features for all 5 agent-invariant signals:

**1. Economic Rationality Signal Features:**
- `utility_deviation`: Deviation from rational utility
- `circular_flow_score`: Circular flow detection (0-1)
- `purpose_deviation`: Purpose mismatch score
- `value_concentration`: Concentration of value to few recipients

**2. Network Topology Signal Features:**
- `sender_centrality`: Betweenness centrality (0-1)
- `receiver_centrality`: Betweenness centrality (0-1)
- `path_length`: Shortest path length
- `clique_membership`: Number of cliques involved

**3. Value Flow Signal Features:**
- `flow_directionality`: Net flow direction
- `settlement_velocity`: Time to settlement
- `destination_concentration`: HHI of destinations

**4. Temporal Consistency Signal Features:**
- `cross_platform_timing`: Sync with other platforms
- `settlement_consistency`: Settlement time patterns
- `causal_chain_consistency`: Logical transaction sequencing

**5. Cross-Platform Correlation Signal Features:**
- `identity_persistence`: Same identity across platforms
- `behavioral_correlation`: Correlated behavior patterns
- `platform_bridge_count`: Number of platforms used

### 7.2 Label Format

```python
@dataclass
class TransactionLabels:
    is_fraud: bool
    attack_chain: Optional[str]
    attack_sophistication: Optional[int]
    human_detectable: bool  # Would human systems detect this?
    agent_invariant_detectable: bool  # Would agent-invariant systems detect this?
```

---

## 8. Generation Code Structure

```
synthetic_data/
├── generators/
│   ├── base_generator.py          # Base transaction generator
│   ├── benign_agent_generator.py   # Benign agent transactions
│   ├── human_baseline_generator.py  # Human baseline
│   └── attack_generator.py         # Attack pattern generators
├── models/
│   └── transaction.py             # Data models
├── network/
│   ├── network_state.py           # Network topology management
│   └── graph_analytics.py        # Network feature calculation
├── validators/
│   ├── economic_rationality.py    # Economic rationality validation
│   └── label_consistency.py        # Label validation
└── main.py                         # Dataset assembly
```

---

## 9. Usage Example

```python
from synthetic_data import generate_validation_dataset

# Generate 100K transaction dataset
dataset = generate_validation_dataset(
    n_benign_human=50000,
    n_benign_agent=40000,
    n_fraud=10000,
    time_span_days=30,
    random_seed=42
)

# Split into train/validation/test
train, val, test = dataset.split([0.7, 0.15, 0.15])

# Export to Parquet
train.to_parquet("synthetic_train.parquet")
val.to_parquet("synthetic_val.parquet")
test.to_parquet("synthetic_test.parquet")

# Generate summary statistics
summary = dataset.summary_statistics()
print(summary)
```

---

## 10. Quality Validation

### 10.1 Validation Checks

**Data Quality Checks:**
- [ ] No duplicate transaction IDs
- [ ] Timestamps are monotonically increasing within generator
- [ ] Amounts are positive and reasonable
- [ ] Network connectivity is consistent
- [ ] Labels are consistent with generation rules

**Attack Chain Validation:**
- [ ] Each attack chain exhibits expected patterns
- [ ] Sophistication levels match expected detectability
- [ ] IMPOSSIBLE attacks are truly impossible for humans

**Feature Distribution Validation:**
- [ ] Agent transactions have higher velocity than humans
- [ ] Fraud transactions have higher circular flow scores
- [ ] Network features match attack patterns
- [ ] Cross-platform attacks have timing signatures

### 10.2 Statistical Validation

**Expected Statistics (from platform analysis):**

| Statistic | Human | Agent (Benign) | Agent (Fraud) |
|-----------|-------|---------------|--------------|
| Daily tx count | 10-100 | 10^3-10^6 | 10^3-10^6 |
| Velocity multiplier | 1× | 10^2-10^4× | 10^2-10^4× |
| Device consistency | High | None | None |
| Location consistency | High | None | None |
| Circular flow score | 0-0.1 | 0-0.3 | 0.5-1.0 |
| Network centrality | Low | Medium | High (hub) |

---

## 11. Limitations and Caveats

**Explicit limitations that must be documented:**

1. **Synthetic patterns may not capture emergent real-world behavior**
   - Real agents may develop strategies not anticipated in platform analysis
   - Multi-agent coordination may have more complex dynamics

2. **Attack patterns are theoretical**
   - Real fraudsters may adapt in unexpected ways
   - Sophistication levels are approximations

3. **Network topology is simplified**
   - Real A2A networks may have more complex structure
   - Cross-platform linkages are approximated

4. **Economic rationality assumptions are simplified**
   - Real agents may have more complex utility functions
   - Market dynamics are simplified

**Required language in reporting:**
> "This research validated the detection framework against synthetic A2A transaction patterns generated from platform documentation analysis. While the framework achieved X% detection on synthetic attack patterns, these patterns may not capture emergent properties of real-world agent behavior. Empirical validation against real A2A transaction data is required before production deployment."

---

**Document Status:** COMPLETE
**Next Step:** Implement detection framework and run validation tests
