# Phase 5 TODO: Ecosystem Characterization

**Created:** 2026-03-24
**Status:** Active
**Based on:** Phase plan, GPD verification results, on-chain data research

---

## Plan 05-01: Go/No-Go Gate — ERC-8004 ↔ x402 Overlap Analysis

### Task 1.1: ERC-8004 Agent Address Extraction
- [ ] 1.1.1 Query ERC-8004 Identity Registry on Ethereum mainnet for all registered agent addresses
- [ ] 1.1.2 Query ERC-8004 on Base chain (contract `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`)
- [ ] 1.1.3 Query ERC-8004 on BNB Chain
- [ ] 1.1.4 Deduplicate cross-chain addresses, produce master agent address list

### Task 1.2: x402 Transaction Identification
- [ ] 1.2.1 Identify x402 facilitator contract addresses on Base
- [ ] 1.2.2 Query USDC transfers routed through x402 facilitators on Dune Analytics
- [ ] 1.2.3 Extract unique sender/receiver addresses from x402 transactions
- [ ] 1.2.4 Estimate genuine vs testing/wash transaction ratio

### Task 1.3: Overlap Analysis (GO/NO-GO GATE)
- [ ] 1.3.1 Cross-reference ERC-8004 agent addresses with x402 transaction participants
- [ ] 1.3.2 Calculate overlap percentage and absolute count
- [ ] 1.3.3 If overlap ≥ 500 addresses: GO — proceed to Plan 05-02
- [ ] 1.3.4 If overlap < 500: Expand to Virtuals Protocol + Moltbook MOLT token + behavioral heuristics
- [ ] 1.3.5 If total labeled agent transactions < 1,000 after expansion: STOP — document and reassess

### Task 1.4: Label Quality Validation
- [ ] 1.4.1 Sample 50 ERC-8004 registered addresses
- [ ] 1.4.2 Analyze their on-chain behavior (tx frequency, amounts, patterns)
- [ ] 1.4.3 Verify they exhibit agent-like behavior (high velocity, programmatic patterns)
- [ ] 1.4.4 Calculate label reliability score (% that behave as agents)
- [ ] 1.4.5 If label reliability < 70%: flag as risk, document behavioral supplement strategy

### Plan 05-01 Acceptance Verification
- [ ] Verify: Overlap quantified with exact numbers
- [ ] Verify: Go/no-go decision documented with evidence
- [ ] Verify: Label quality assessed on sample
- [ ] Create `analysis/overlap-analysis.md`
- [ ] Create `.gpd/phases/05-ecosystem-characterization/05-01-SUMMARY.md`

---

## Plan 05-02: Data Ingestion Pipeline

### Task 2.1: ERC-8004 Registry Ingestion
- [ ] 2.1.1 Build The Graph subgraph query for ERC-8004 Identity Registry events
- [ ] 2.1.2 Extract all agent registrations: address, tokenId, URI metadata, registration timestamp
- [ ] 2.1.3 Fetch agent metadata from tokenURI (agent type, capabilities, owner)
- [ ] 2.1.4 Store in structured format (Parquet/CSV)

### Task 2.2: Transaction Data Ingestion
- [ ] 2.2.1 Build Dune SQL queries for x402 facilitator USDC transfers on Base
- [ ] 2.2.2 Build queries for Virtuals Protocol agent token transactions
- [ ] 2.2.3 Build queries for MOLT token transactions (Moltbook)
- [ ] 2.2.4 Extract: timestamp, sender, receiver, amount, gas, contract interactions

### Task 2.3: Dataset Construction
- [ ] 2.3.1 Join agent registry with transaction data (label: agent/human/unknown)
- [ ] 2.3.2 Engineer features matching the 5 detection signals
- [ ] 2.3.3 Calculate behavioral features (velocity, value distribution, temporal patterns)
- [ ] 2.3.4 Produce labeled dataset with ≥10K agent transactions
- [ ] 2.3.5 Document dataset schema, statistics, and known biases

### Task 2.4: Reference Implementation — Data Pipeline
- [ ] 2.4.1 Python package structure with data ingestion modules
- [ ] 2.4.2 ERC-8004 registry client (The Graph / direct RPC)
- [ ] 2.4.3 Dune Analytics query runner
- [ ] 2.4.4 Dataset builder and feature engineering pipeline
- [ ] 2.4.5 Export to standard ML formats (Parquet, CSV)

### Plan 05-02 Acceptance Verification
- [ ] Verify: ≥10K labeled agent transactions in dataset
- [ ] Verify: Dataset schema documented with feature descriptions
- [ ] Verify: Pipeline reproducible from source
- [ ] Create `analysis/dataset-construction.md`
- [ ] Create `.gpd/phases/05-ecosystem-characterization/05-02-SUMMARY.md`

---

## Plan 05-03: Invariant Violation Measurement

### Task 3.1: Velocity Invariant (Invariant #1)
- [ ] 3.1.1 Measure transaction velocity distribution for ERC-8004 agents vs labeled human wallets
- [ ] 3.1.2 Compare against predicted range (agents: 10³-10⁶ tx/day vs humans: 10-100 tx/day)
- [ ] 3.1.3 Statistical test for distribution separation

### Task 3.2: Geographic/Location Invariant (#4)
- [ ] 3.2.1 Analyze cross-chain activity patterns (agents transacting on multiple chains simultaneously)
- [ ] 3.2.2 Measure geographic impossibility signals (transactions across chains within impossible timeframes)

### Task 3.3: Identity Persistence Invariant (#6)
- [ ] 3.3.1 Track wallet creation patterns (age, reuse, disposability)
- [ ] 3.3.2 Measure Sybil indicators (clusters of new wallets with coordinated behavior)

### Task 3.4: Remaining Invariants (#2,3,5,7,8,9)
- [ ] 3.4.1 Behavioral stability: measure transaction pattern consistency over time
- [ ] 3.4.2 Cognitive/energy limits: measure 24/7 activity patterns vs human sleep cycles
- [ ] 3.4.3 Computational constraints: measure transaction complexity and parallelism
- [ ] 3.4.4 Bounded rationality: measure arbitrage efficiency and market response times
- [ ] 3.4.5 Document which invariants are measurable from on-chain data vs which require off-chain signals

### Task 3.5: Invariant Violation Summary
- [ ] 3.5.1 Compile violation evidence for each of 9 invariants
- [ ] 3.5.2 Compare real-world violations against synthetic predictions from Phase 2
- [ ] 3.5.3 Identify invariants that are stronger/weaker discriminators than predicted
- [ ] 3.5.4 Update invariant taxonomy with real-world evidence

### Plan 05-03 Acceptance Verification
- [ ] Verify: All 9 invariants tested (or documented as unmeasurable from on-chain data)
- [ ] Verify: Statistical significance reported for measurable invariants
- [ ] Verify: Comparison with Phase 2 synthetic predictions documented
- [ ] Create `analysis/real-world-invariant-violations.md`
- [ ] Create `.gpd/phases/05-ecosystem-characterization/05-03-SUMMARY.md`

---

## Plan 05-04: Signal Validation and Transfer Gap

### Task 4.1: Reference Implementation — 5-Signal Detection Framework
- [ ] 4.1.1 Implement Economic Rationality signal scorer
- [ ] 4.1.2 Implement Network Topology signal scorer
- [ ] 4.1.3 Implement Value Flow signal scorer
- [ ] 4.1.4 Implement Temporal Consistency signal scorer
- [ ] 4.1.5 Implement Cross-Platform Correlation signal scorer
- [ ] 4.1.6 Implement signal fusion algorithm
- [ ] 4.1.7 Implement 4-tier decision system (ALLOW/FLAG/BLOCK/INVESTIGATE)

### Task 4.2: Real-Data Evaluation
- [ ] 4.2.1 Run detection framework on labeled real-world dataset
- [ ] 4.2.2 Calculate precision, recall, F1, ROC-AUC on real data
- [ ] 4.2.3 Calculate per-signal effectiveness on real data
- [ ] 4.2.4 Measure per-transaction latency

### Task 4.3: Transfer Gap Analysis
- [ ] 4.3.1 Compare real-data metrics against synthetic benchmarks (96.23% precision/recall)
- [ ] 4.3.2 Identify which signals degrade most on real data
- [ ] 4.3.3 Analyze root causes of degradation (data quality, behavioral differences, label noise)
- [ ] 4.3.4 Propose signal recalibration based on real-world findings

### Task 4.4: Open-Source Package
- [ ] 4.4.1 Package Python library with pip-installable structure
- [ ] 4.4.2 Write usage documentation and examples
- [ ] 4.4.3 Include dataset download/construction scripts
- [ ] 4.4.4 Add benchmark scripts for reproducibility
- [ ] 4.4.5 License selection (Apache 2.0 / MIT)

### Plan 05-04 Acceptance Verification
- [ ] Verify: All 5 signals implemented and tested
- [ ] Verify: Real-data precision/recall measured and compared to synthetic
- [ ] Verify: Transfer gap quantified with root cause analysis
- [ ] Verify: Open-source package functional and documented
- [ ] Create `analysis/transfer-gap-analysis.md`
- [ ] Create `.gpd/phases/05-ecosystem-characterization/05-04-SUMMARY.md`

---

## Phase 5 Completion Checklist

### Contract Claims Verification
- [ ] claim-05-dataset: Labeled A2A transaction dataset constructed with ≥10K transactions
- [ ] claim-05-invariants: Real-world invariant violations measured and compared to predictions
- [ ] claim-05-signals: Detection framework validated on real data
- [ ] claim-05-gap: Synthetic-to-real transfer gap quantified

### Deliverables Verification
- [ ] deliv-overlap-analysis created and validated
- [ ] deliv-dataset created and documented
- [ ] deliv-invariant-measurements created and validated
- [ ] deliv-transfer-gap created and validated
- [ ] deliv-open-source-package functional

### Phase 5 Handoff
- [ ] All 4 plan SUMMARY.md files created
- [ ] Roadmap updated with Phase 5 completion
- [ ] Go/no-go decision for Phase 6 documented

---

## Usage Notes

**Execution order:** Plan 05-01 is a GATE — if it fails, Plans 05-02 through 05-04 are blocked.
Plans 05-02, 05-03, 05-04 have dependencies: 05-02 must complete before 05-03 and 05-04 can run.
05-03 and 05-04 can partially parallelize once dataset is available.

**Go/No-Go Criteria:**
- 05-01 overlap ≥ 500 addresses OR expanded sources yield ≥ 1,000 labeled agent txns → GO
- Otherwise → STOP, document, reassess data strategy
