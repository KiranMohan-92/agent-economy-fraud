# a2a-fincrime-detection

A 5-signal detection framework for identifying agent-to-agent (A2A) financial crime on blockchain networks. Based on the research paper *"Agent-Invariant Fraud Detection: How Software Agents Break Every Assumption in Banking Fraud Detection"*.

## Background

Modern fraud detection is built on 9 human behavioral invariants — assumptions like biometric uniqueness, geographic constraints, and velocity limits. Software agents (ERC-8004-registered autonomous systems, AI payment agents) violate all of these simultaneously.

This framework implements 5 signals that directly measure these violations on-chain, validated against 81,904 real USDC transactions on Base chain (January 2025 – April 2026).

## Installation

```bash
pip install a2a-fincrime-detection
```

With Dune Analytics data ingestion:

```bash
pip install "a2a-fincrime-detection[dune]"
```

Development install:

```bash
git clone https://github.com/your-org/a2a-fincrime-detection
cd a2a-fincrime-detection/src
pip install -e ".[dev]"
```

## Quick Start

```python
import pandas as pd
from a2a_detection.signals.fusion import SignalFusion

# Load your transaction data
# Required columns: sender, receiver, amount_usdc, timestamp
txns = pd.read_parquet("transactions.parquet")
labels = pd.read_parquet("labels.parquet")  # columns: address, label ("agent"/"human")

# Score all labeled addresses
fusion = SignalFusion()
results = fusion.score_batch(labels["address"].tolist(), txns)

# Evaluate against ground truth
metrics = fusion.evaluate(results, labels)
print(f"Precision: {metrics['precision']:.1%}  Recall: {metrics['recall']:.1%}  F1: {metrics['f1']:.1%}")
```

## The 5 Signals

| Signal | Human Invariant Violated | AUC (real data) | Weight |
|--------|--------------------------|-----------------|--------|
| **Network Topology** | Geographic/network constraints | 0.599 | 0.2739 |
| **Temporal Consistency** | Circadian rhythm, cognitive speed | 0.465 | 0.2505 |
| **Economic Rationality** | Bounded rationality, decision cost | 0.515 | 0.2424 |
| **Value Flow** | No superhuman relay speed | 0.522 | 0.2332 |
| **Cross-Platform Correlation** | Physical location uniqueness | n/a (single-chain) | 0.0000 |

### Signal Details

**1. Economic Rationality** — Detects transactions that no profit-maximizing human would make: circular flows, irrational pricing, zero-utility transfers, and programmatic value splitting.

**2. Network Topology** — Detects anomalous graph centrality around an address (star topologies from swarm controllers, dense cliques from coordinated agents) using degree z-scores.

**3. Value Flow** — Detects rapid relay behavior (funds forwarded within 60 seconds) and layering chains where multiple addresses exhibit balanced pass-through flow patterns.

**4. Temporal Consistency** — Detects circadian violations (24/7 uniform activity), sub-second transaction gaps (impossible for humans), and hourly burst rates exceeding 30 tx/hour.

**5. Cross-Platform Correlation** — Detects same-address activity across multiple chains within 30-second windows (physically impossible without automation). Requires multi-chain transaction data.

## Decision Tiers

The composite score maps to a 4-tier decision system:

```
ALLOW:       score < 0.09  — Normal human transaction
FLAG:        0.09–0.50     — Elevated monitoring
INVESTIGATE: 0.50–0.75     — Manual review required
BLOCK:       ≥ 0.75        — High-confidence agent fraud
```

## Validated Performance

Evaluated on 1,734 labeled addresses (665 ERC-8004 agents, 1,069 active human counterparties, Base chain):

| Metric | Synthetic | Real (cleaned) | Transfer Gap |
|--------|-----------|----------------|--------------|
| Recall | 96.2% | 81.1% | −15.1pp |
| Precision | 82.4% | 42.9% | −39.5pp |
| F1 | 88.7% | 56.1% | −32.6pp |
| ROC-AUC | 0.97 | 0.515 | −0.455 |

**Why precision drops more than recall:** Negative-class label noise. Human counterparties are heuristically labeled — many are automated contracts. Recall (agent detection rate) is label-noise invariant and transfers at −15.1pp. See `analysis/transfer-gap-analysis.md` for full analysis.

## Data Pipeline

To reproduce results with Dune Analytics:

```bash
# 1. Set your Dune API key
export DUNE_API_KEY=your_key_here

# 2. Ingest agent transactions (ERC-8004 on Base chain)
python -m a2a_detection.scripts.fetch_dune_batched

# 3. Validate precision on real data
python -m a2a_detection.scripts.validate_precision

# With EOA contract filtering (reduces false positives):
RPC_URL=https://mainnet.base.org python -m a2a_detection.scripts.validate_precision
```

## Reproducing the Benchmark

```bash
# Run the full validation pipeline (requires data/transactions_dune.parquet and data/labels_dune.parquet)
python -m a2a_detection.scripts.validate_precision

# Output: before/after comparison + data/validation_metrics.json
```

Expected output matches `data/validation_metrics.json`:
- `updated.precision`: 0.4288 (42.9%)
- `updated.recall`: 0.8105 (81.1%)
- `updated.f1`: 0.5609 (56.1%)

## Project Structure

```
src/
├── a2a_detection/
│   ├── __init__.py               # Package entry point
│   ├── signals/
│   │   ├── economic_rationality.py   # Signal 1
│   │   ├── network_topology.py       # Signal 2
│   │   ├── value_flow.py             # Signal 3
│   │   ├── temporal_consistency.py   # Signal 4
│   │   ├── cross_platform.py         # Signal 5
│   │   ├── fusion.py                 # Signal fusion + 4-tier decisions
│   │   └── label_cleaner.py          # Negative-class cleaning utilities
│   ├── data/
│   │   ├── erc8004.py                # ERC-8004 registry client
│   │   └── transactions.py           # Transaction data loader
│   └── scripts/
│       ├── validate_precision.py     # Benchmark runner
│       ├── fetch_dune_batched.py     # Dune data ingestion
│       └── bridge_dune_data.py       # Data format bridge
└── pyproject.toml
```

## Background Research

This framework emerged from the research question:

> *How do the necessary properties of agent-to-agent commerce create fundamental vulnerabilities in banking fraud detection systems?*

Key findings:
- 9 human behavioral invariants underpin all major fraud detection heuristics
- Software agents (ERC-8004, x402 protocol) violate 7/9 invariants by design
- 4 of 5 framework signals achieve AUC > 0.5 on real on-chain data
- Recall transfers at −0.8pp synthetic → real (label-noise invariant)

Full research: `analysis/` directory.

## License

Apache 2.0. See [LICENSE](../LICENSE).
