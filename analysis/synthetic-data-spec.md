# Synthetic A2A Transaction Data Specification

**Phase:** 01-discovery-taxonomy, Plan 04, Task 2
**Created:** 2026-03-18
**Grounded in:** Plans 01-01 (OpenClaw), 01-02 (Moltbook), 01-03 (Literature)
**Status:** Specification complete (implementation in later phases)

## Executive Summary

This specification defines synthetic A2A transaction data generation requirements for fraud detection framework validation. All requirements trace to platform analysis findings (OpenClaw, Moltbook) and literature patterns (multi-agent economics, fraud detection).

**Key principle:** Every synthetic data requirement references specific platform capabilities or literature findings. No arbitrary choices.

## 1. Data Requirements from Platform Analysis

### 1.1 OpenClaw Platform Patterns (Plan 01-01)

**Source:** analysis/openclaw-platform-analysis.md

**Transaction velocity capabilities:**
- **API rate limits:** 900 requests/minute per session (OpenClaw retry policy)
- **Parallel sessions:** No limit on concurrent sessions per account
- **Agent-to-agent messaging:** `sessions_send` API enables unrestricted A2A transactions
- **Batch operations:** `sessions_spawn` creates multiple agents simultaneously

**Synthetic requirement:**
```
Agent transaction velocity: 10^3-10^6 transactions/day
Human transaction velocity: 10-100 transactions/day (baseline)
Velocity multiplier: 10^2-10^4× faster than humans
```

**Rationale:** OpenClaw analysis documented 7,500,000× velocity amplification (human: 0.0012 tx/sec → agent: 9,000 tx/sec). Synthetic data must reflect this scale advantage.

**Behavioral patterns from OpenClaw APIs:**
- `sessions_list` - Agent enumeration capability
- `sessions_history` - Transaction history extraction
- `sessions_send` - Direct agent-to-agent transactions
- `sessions_spawn` - Multi-agent creation and coordination

**Synthetic requirement:**
- Include agent enumeration transactions (discovery phase)
- Include transaction history queries (reconnaissance)
- Include direct A2A transfers (primary fraud vector)
- Include swarm coordination patterns (flash attack capability)

**Rationale:** All 4 attack chains from Plan 01-01 must be representable in synthetic data.

### 1.2 Moltbook Platform Patterns (Plan 01-02)

**Source:** analysis/moltbook-platform-analysis.md, analysis/reputation-system-analysis.md

**Reputation system mechanics:**
- **Upvoting:** X-verified users can upvote agents (1 upvote per account)
- **Submolt communities:** Agents can belong to multiple communities
- **Reputation transfer:** Cross-Submolt reputation accumulation possible
- **X verification bottleneck:** Each agent requires unique X account (Sybil resistance constraint)

**Synthetic requirement:**
```
Agent reputation building:
- Initial reputation: 0 for new agents
- Upvote velocity: 10^2-10^3 upvotes/minute (agent) vs 1 upvote/minute (human)
- Parallel aging: 10^3 agents aging simultaneously vs 1 human account
- Scale multiplier: 10^3-10^6× reputation building speed

Sybil attack patterns:
- Identity multiplicity: 1 human → 100 disposable sub-agents
- Coordinated upvoting: 100 agents upvoting 1 target in 1 second
- Cross-Submolt reputation transfer: Reputation built in community A, transferred to community B
```

**Rationale:** Moltbook analysis documented 10^3-10^6× reputation building advantage. Synthetic data must enable reputation manipulation attacks.

### 1.3 Attack Chains from Platform Analysis

**Source:** analysis/attack-chain-mapping.md

**8 attack chains mapped:** Each must be representable in synthetic data

1. **Agent Enumeration** (EASY detection) - `sessions_list` scanning
2. **History Extraction** (EASY detection) - `sessions_history` queries
3. **Async Flooding** (MEDIUM detection) - High-velocity `sessions_send`
4. **Agent Army** (HARD detection) - `sessions_spawn` multi-agent coordination
5. **Cross-Platform Identity** (IMPOSSIBLE) - `identityLinks` + `dmScope` persistence
6. **Behavioral Mimicry** (IMPOSSIBLE) - `sessions_history` + `sessions_send` perfect cloning
7. **Swarm Intelligence** (IMPOSSIBLE) - Coordinated `sessions_spawn` + `sessions_send`
8. **Market Manipulation** (IMPOSSIBLE) - `cron` + `tools.browser` + `exec` integration

**Synthetic requirement:**
- All 8 attack chains must have corresponding transaction patterns
- Each chain labeled with detection difficulty (EASY/MEDIUM/HARD/IMPOSSIBLE)
- Include benign agent transactions (non-fraudulent baseline)

**Rationale:** Detection framework must be tested against all attack vectors identified in platform analysis.

## 2. Data Requirements from Literature (Plan 01-03)

### 2.1 Human Behavioral Invariants

**Source:** analysis/literature-survey.md, Section 2 (Fraud Detection Theory)

**4 human invariants documented:**

1. **Velocity limits** (Van Vlasselaer 2017): ~10-100 transactions/day
2. **Biometric authentication** (Jain 2021): Physical presence required
3. **Device fingerprinting** (Mowery 2012): Fixed device identity
4. **Location constraints** (Zhang 2020): Travel time limits

**Synthetic requirement:**
```
Human baseline dataset:
- Transaction velocity: 10-100 transactions/day
- Device consistency: 1 device per user
- Location coherence: Travel time < physical limits
- Session duration: Human-scale (minutes to hours)

Agent dataset (violating all invariants):
- Transaction velocity: 10^3-10^6 transactions/day
- Device rotation: Arbitrary device IDs per transaction
- Location independence: Instant global execution
- Session patterns: Machine-scale (milliseconds to seconds)
```

**Rationale:** Literature establishes that current fraud detection relies on these invariants. Synthetic data must demonstrate agent violations for detection framework testing.

### 2.2 Nearest Analogue Patterns

**Source:** analysis/literature-survey.md, Section 4 (Nearest Analogues)

**Applicable patterns from 4 analogues:**

**Botnet detection (unauthorized → authorized adaptation):**
- Coordinated C2 patterns → Coordinated A2A transactions
- Command timing → Swarm coordination timing
- Scale: 10^3-10^4 nodes

**High-frequency trading fraud:**
- Machine-speed transactions → Agent transaction velocity
- Market manipulation → Cross-platform reputation manipulation
- Latency: Millisecond-scale

**P2P marketplace fraud:**
- Reputation attacks → Sybil attacks on Moltbook
- Fake reviews → Coordinated upvoting
- Identity multiplicity → Disposable agent creation

**Multi-agent RL:**
- Agent-agent interaction → A2A commerce transactions
- Adversarial policies → Fraud detector vs. fraudster dynamics
- Coordination mechanisms → Swarm intelligence patterns

**Synthetic requirement:**
- Include botnet-style coordination patterns (C2 timing adaptation)
- Include HFT-style velocity patterns (millisecond transactions)
- Include P2P reputation attacks (Sybil upvoting)
- Include MARL-style adversarial dynamics (detector vs. attacker)

**Rationale:** Literature provides theoretical frameworks for agent behavior. Synthetic data should instantiate these frameworks.

## 3. Synthetic Data Schema

### 3.1 Core Transaction Schema

```python
Transaction = {
    # Core fields
    'transaction_id': str,           # Unique identifier
    'timestamp': datetime,           # ISO 8601 (UTC)
    'sender_agent_id': str,          # Agent identifier
    'receiver_agent_id': str,        # Agent identifier
    'amount': float,                 # Transaction amount (USD)
    'transaction_type': str,         # Type (see categories below)

    # Agent metadata
    'sender_type': str,              # 'human' | 'agent'
    'receiver_type': str,            # 'human' | 'agent'
    'sender_platform': str,          # 'OpenClaw' | 'Moltbook' | 'Other'
    'receiver_platform': str,        # Platform identifier

    # Behavioral features
    'device_id': str,                # Device fingerprint
    'location': tuple,               # (lat, lon) or None for agents
    'session_id': str,               # Session identifier

    # Fraud labels (ground truth)
    'is_fraud': bool,                # Fraud/no-fraud label
    'fraud_type': str | None,        # Attack chain ID if fraud
    'detection_difficulty': str,     # 'EASY' | 'MEDIUM' | 'HARD' | 'IMPOSSIBLE'

    # Reputation (Moltbook-specific)
    'reputation_change': float | None,  # Reputation delta
    'upvote_count': int | None,      # Number of upvotes
}
```

**Rationale for schema fields:**
- `transaction_type`: Enables attack chain categorization (see 3.2)
- `sender_type`/`receiver_type`: Human vs. agent distinction for detection
- `device_id`/`location`: Human invariant violation features
- `fraud_type`/`detection_difficulty`: Ground truth for detection testing

### 3.2 Transaction Categories

**Benign transactions (baseline):**
1. `normal_human` - Regular human-to-human transaction
2. `normal_agent` - Legitimate agent-to-agent transaction
3. `agent_service` - Agent providing service (non-fraud)
4. `human_to_agent` - Human purchasing from agent (non-fraud)

**Fraud transactions (by attack chain):**
1. `agent_enumeration` - Chain 1: Agent discovery (EASY)
2. `history_extraction` - Chain 2: Reconnaissance (EASY)
3. `async_flooding` - Chain 3: Velocity attack (MEDIUM)
4. `agent_army` - Chain 4: Multi-agent coordination (HARD)
5. `cross_platform_identity` - Chain 5: Identity persistence (IMPOSSIBLE)
6. `behavioral_mimicry` - Chain 6: Perfect cloning (IMPOSSIBLE)
7. `swarm_intelligence` - Chain 7: Flash attack (IMPOSSIBLE)
8. `market_manipulation` - Chain 8: Economic manipulation (IMPOSSIBLE)

**Rationale:** Mapping to 8 attack chains from Plan 01-01 ensures detection framework coverage.

### 3.3 Agent Identity Schema

```python
Agent = {
    'agent_id': str,                 # Unique identifier
    'type': str,                     # 'human' | 'agent' | 'sybil_agent'
    'platform': str,                 # 'OpenClaw' | 'Moltbook' | 'Both'
    'created_at': datetime,          # Agent creation timestamp
    'creator_agent_id': str | None,  # For spawned agents (sybil tracking)

    # Moltbook-specific
    'x_verified': bool,              # X verification status
    'reputation_score': float,       # Current reputation
    'submolts': list[str],           # Community memberships

    # OpenClaw-specific
    'session_count': int,            # Number of active sessions
    'identity_links': list[str],     # Cross-platform identities

    # Behavioral features
    'transaction_velocity': float,   # Transactions/day
    'last_transaction': datetime,    # Most recent activity
}
```

**Rationale:** Agent identity schema enables cross-platform identity attacks (Chain 5) and Sybil detection.

## 4. Scale and Scope

### 4.1 Dataset Size

**Minimum requirements:**
- **Total transactions:** 1,000,000 transactions
  - 800,000 benign (80%)
  - 200,000 fraud (20%)
- **Time span:** 30 days of synthetic activity
- **Agent count:** 10,000 agents
  - 9,000 legitimate agents (90%)
  - 1,000 fraudulent agents (10%)
- **Human count:** 1,000 humans (for baseline comparison)

**Rationale:** Sufficient scale for ML-based detection training while computationally manageable for research.

### 4.2 Temporal Distribution

**Transaction velocity patterns:**

```
Human baseline:
- 10-100 transactions/day per human
- Poisson distributed over waking hours (6am-10pm)
- Weekend reduction: 50% velocity

Legitimate agents:
- 100-1,000 transactions/day (moderate automation)
- Uniform distribution (24/7 operation)
- No weekend/weekday distinction

Fraudulent agents:
- 10^3-10^6 transactions/day during attacks
- Burst patterns: Attacks clustered in short windows
- Flash attacks: 10,000+ transactions in <1 second
```

**Rationale:** Reflects OpenClaw velocity analysis (7,500,000× amplification) and human constraints from literature.

### 4.3 Fraud Type Distribution

**200,000 fraud transactions distributed as:**
- Agent enumeration (EASY): 20,000 (10%)
- History extraction (EASY): 20,000 (10%)
- Async flooding (MEDIUM): 40,000 (20%)
- Agent army (HARD): 30,000 (15%)
- Cross-platform identity (IMPOSSIBLE): 25,000 (12.5%)
- Behavioral mimicry (IMPOSSIBLE): 25,000 (12.5%)
- Swarm intelligence (IMPOSSIBLE): 20,000 (10%)
- Market manipulation (IMPOSSIBLE): 20,000 (10%)

**Rationale:** Higher-weight for IMPOSSIBLE attacks (critical to detect) and MEDIUM (most common real-world scenario).

## 5. Generation Approach

### 5.1 Implementation Framework

**Language:** Python 3.10+
**Libraries:**
- `pandas` - Data frame manipulation
- `numpy` - Random number generation, numerical operations
- `networkx` - Transaction graph construction
- `datetime` - Timestamp generation

**Script structure:**
```python
# scripts/generate_synthetic_a2a_data.py

def generate_human_baseline(n_humans, days):
    """Generate human transaction patterns (literature-based)"""
    # Velocity: 10-100 tx/day (Van Vlasselaer 2017)
    # Device: 1 device per human (Mowery 2012)
    # Location: Travel time constraints (Zhang 2020)
    pass

def generate_legitimate_agents(n_agents, days):
    """Generate legitimate agent transactions"""
    # Velocity: 100-1,000 tx/day (moderate automation)
    # Platform: OpenClaw + Moltbook patterns
    pass

def generate_fraud_patterns(attack_chain_id, n_transactions):
    """Generate fraud transactions for specific attack chain"""
    # Maps to 8 attack chains from Plan 01-01
    # Each chain has distinct behavioral signature
    pass

def generate_sybil_agents(n_sybils, creator_agent):
    """Generate Sybil agent network"""
    # Reputation manipulation (Moltbook 01-02)
    # Cross-Submolt coordination
    pass

def apply_fraud_labels(transactions, attack_chains):
    """Label transactions with fraud type and detection difficulty"""
    # Ground truth for detection testing
    pass
```

**Rationale:** Modular structure enables traceability from platform analysis to generation code.

### 5.2 Random Seed Configuration

**Reproducibility requirement:**
```python
import random
random.seed(42)  # Fixed seed for reproducibility
np.random.seed(42)
```

**Rationale:** Scientific reproducibility requirement. All synthetic data generation must be reproducible.

### 5.3 Validation Criteria

**Statistical realism checks:**

1. **Distribution validation:**
   - Human transaction amounts: Log-normal distribution (matches real financial data)
   - Agent transaction amounts: Uniform or multi-modal (distinct from humans)
   - Inter-transaction times: Exponential (Poisson process)

2. **Scale validation:**
   - Human velocity: 10-100 tx/day (matches literature)
   - Agent velocity: 10^3-10^6 tx/day during attacks (matches OpenClaw)
   - Reputation building: 10^3-10^6× speedup (matches Moltbook)

3. **Attack coverage:**
   - All 8 attack chains represented
   - Detection difficulty labels applied correctly
   - Ground truth consistency (no benign transactions labeled fraud)

**Rationale:** Ensures synthetic data meets all platform-grounded requirements.

## 6. Attack Coverage Specification

### 6.1 Chain 1: Agent Enumeration (EASY)

**Pattern:** `sessions_list` scanning
**Synthetic generation:**
- 1 agent queries 10,000 other agents via enumeration API
- Transaction type: `agent_enumeration`
- Detection difficulty: EASY (obvious API abuse pattern)

**Features:**
- High query rate (10,000 queries in 1 second)
- No monetary transactions (read-only operations)
- Sequential agent IDs (enumeration signature)

### 6.2 Chain 2: History Extraction (EASY)

**Pattern:** `sessions_history` reconnaissance
**Synthetic generation:**
- Agent extracts transaction history from 1,000 victims
- Transaction type: `history_extraction`
- Detection difficulty: EASY (unusual read pattern)

**Features:**
- Read-heavy transaction profile (99% queries, 1% transfers)
- Sequential victim targeting
- Large data volume (extracting 30-day histories)

### 6.3 Chain 3: Async Flooding (MEDIUM)

**Pattern:** High-velocity `sessions_send` transactions
**Synthetic generation:**
- Agent sends 10,000 transactions in 10 seconds
- Transaction type: `async_flooding`
- Detection difficulty: MEDIUM (velocity detection required)

**Features:**
- Velocity: 1,000 tx/second (violates human limits)
- Small amounts: $0.01-$1.00 (evades threshold-based detection)
- Single victim (focused attack)

### 6.4 Chain 4: Agent Army (HARD)

**Pattern:** `sessions_spawn` multi-agent coordination
**Synthetic generation:**
- 1 human creates 100 sybil agents
- 100 agents execute coordinated transactions
- Transaction type: `agent_army`
- Detection difficulty: HARD (individual agents look legitimate)

**Features:**
- Creator-traceable agent IDs (sybil network structure)
- Coordinated timing: 100 agents transact simultaneously
- Cross-platform identity: Same agent on OpenClaw + Moltbook

### 6.5 Chain 5: Cross-Platform Identity (IMPOSSIBLE)

**Pattern:** `identityLinks` + `dmScope` persistence
**Synthetic generation:**
- Agent builds reputation on OpenClaw
- Agent migrates to Moltbook, imports reputation
- Transaction type: `cross_platform_identity`
- Detection difficulty: IMPOSSIBLE (identity looks legitimate on both platforms)

**Features:**
- Linked agent IDs across platforms
- Reputation history transfer
- No behavioral anomalies (mimics legitimate agent)

### 6.6 Chain 6: Behavioral Mimicry (IMPOSSIBLE)

**Pattern:** `sessions_history` + `sessions_send` perfect cloning
**Synthetic generation:**
- Agent extracts victim's transaction history
- Agent replicates victim's behavior pattern
- Transaction type: `behavioral_mimicry`
- Detection difficulty: IMPOSSIBLE (indistinguishable from victim)

**Features:**
- Behavioral cloning: Matches victim's velocity, amount, timing
- Device rotation: Copies victim's device ID
- Location spoofing: Matches victim's location

### 6.7 Chain 7: Swarm Intelligence (IMPOSSIBLE)

**Pattern:** Coordinated `sessions_spawn` + `sessions_send` flash attack
**Synthetic generation:**
- 1,000 agents execute 10,000 transactions in 1 second
- Transaction type: `swarm_intelligence`
- Detection difficulty: IMPOSSIBLE (outruns reactive detection)

**Features:**
- Flash timing: All transactions within 1-second window
- Coordinated targeting: Single victim
- Swarm coordination: No central command (distributed)

### 6.8 Chain 8: Market Manipulation (IMPOSSIBLE)

**Pattern:** `cron` + `tools.browser` + `exec` economic manipulation
**Synthetic generation:**
- Agents manipulate synthetic market prices
- Transaction type: `market_manipulation`
- Detection difficulty: IMPOSSIBLE (requires market understanding)

**Features:**
- Cron-based execution: Periodic manipulation attempts
- Cross-platform: OpenClaw (execution) + Moltbook (reputation laundering)
- Economic complexity: Multi-step manipulation chains

## 7. Limitations Section

### 7.1 What Synthetic Data CAN'T Capture

**Emergent behavior:**
- Real agent systems may exhibit complex emergent behaviors not predicted by platform documentation
- Swarm intelligence may be more sophisticated than synthetic patterns
- Cross-platform synergies may emerge unpredictably

**Real-world complexity:**
- Platform-specific edge cases and bugs not documented
- Network latency effects on coordination timing
- Resource constraints (memory, CPU) affecting agent behavior

**Adversarial adaptation:**
- Real attackers adapt to detection systems in arms race
- Synthetic patterns assume static attack strategies
- No co-evolution of attacker and defender

### 7.2 Validation Uncertainty

**Generalization risk:**
- Detection framework trained on synthetic data may not generalize to real A2A transactions
- Performance on synthetic patterns ≠ performance in production
- False positive/negative rates uncertain for real-world deployment

**Confidence qualifiers required:**
- "Framework detects 95% of **synthetic** attack patterns"
- "Results **suggest** the approach is promising"
- NOT "Framework validates against real A2A transactions"

### 7.3 Real Data Prerequisites

**What would enable full validation:**
1. **Platform partnerships:** Access to anonymized OpenClaw/Moltbook transaction logs
2. **Industry collaboration:** Banking/fintech A2A fraud case data
3. **Research consortia:** Multi-institution A2A dataset creation
4. **Timeline:** 12-36 months for real data acquisition

**Until then:**
- Synthetic data enables framework development
- All validation explicitly labeled as synthetic-only
- Production deployment requires real-world testing

## 8. Traceability Matrix

| Synthetic Requirement | Platform Source | Literature Source | Implementation Location |
| --------------------- | --------------- | ----------------- | ---------------------- |
| Transaction velocity 10^3-10^6 tx/day | OpenClaw 01-01 (retry policy, sessions_send) | Van Vlasselaer 2017 (human baseline) | `generate_fraud_patterns()` |
| Reputation building 10^3-10^6× speedup | Moltbook 01-02 (upvoting, parallel aging) | - | `generate_sybil_agents()` |
| Device fingerprint violation | OpenClaw 01-01 (no device constraint) | Mowery 2012 (device invariant) | `generate_human_baseline()` |
| Location independence | OpenClaw 01-01 (no location constraint) | Zhang 2020 (location invariant) | `generate_fraud_patterns()` |
| Swarm coordination timing | OpenClaw 01-01 (sessions_spawn parallel) | Tolstaya 2022 (MARL coordination) | Chain 7 generation |
| Sybil attack patterns | Moltbook 01-02 (X verification bypass) | Jiang 2020 (Sybil-resistant reputation) | `generate_sybil_agents()` |
| Cross-platform identity | OpenClaw 01-01 (identityLinks) | - | Chain 5 generation |
| Behavioral cloning | OpenClaw 01-01 (sessions_history) | - | Chain 6 generation |
| 8 attack chains | OpenClaw 01-01 attack chain mapping | - | All 8 chain functions |
| Human baseline (10-100 tx/day) | - | Van Vlasselaer 2017 | `generate_human_baseline()` |

**Rationale:** Every synthetic data requirement traces to platform analysis or literature finding. No arbitrary assumptions.

## 9. Summary

**Synthetic data specification complete with:**
- ✅ All requirements grounded in platform analysis (Plans 01-01, 01-02)
- ✅ All requirements grounded in literature findings (Plan 01-03)
- ✅ Attack coverage for all 8 attack chains from Plan 01-01
- ✅ Scale and velocity based on OpenClaw/Moltbook analysis
- ✅ Human behavioral invariants from literature incorporated
- ✅ Explicit limitations section documenting what synthetic can't capture
- ✅ Validation criteria defined for generation process
- ✅ Traceability matrix ensures no arbitrary choices

**Next step:** Task 3 - Document overall validation strategy and confidence implications

---

**Document status:** COMPLETE
**Confidence:** MEDIUM-HIGH (platform-grounded, but synthetic validity uncertain)
**Implementation:** Deferred to appropriate phase (specification only)

