"""Plan 05-01: Go/No-Go Gate — ERC-8004 ↔ Transaction Overlap Analysis.

This script executes the critical go/no-go gate for Phase 5.
It determines whether ERC-8004 registered agents have measurable
on-chain transaction activity, which is required for real-world validation.

Usage:
    python -m a2a_detection.scripts.run_overlap_gate

    # Or with explicit Dune API key:
    DUNE_API_KEY=your_key python -m a2a_detection.scripts.run_overlap_gate

Required environment variables:
    DUNE_API_KEY: Dune Analytics API key (get from dune.com/settings/api)

Output:
    - analysis/overlap-analysis.md: Full overlap report
    - data/erc8004_agents.parquet: Agent address list
    - data/overlap_results.parquet: Cross-reference results
    - GO/NO-GO decision printed to stdout
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
QUERIES_DIR = PROJECT_ROOT / "queries"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
logger = logging.getLogger("overlap-gate")

# Go/No-Go thresholds
MIN_OVERLAP_ADDRESSES = 500
MIN_LABELED_TRANSACTIONS = 1000
LABEL_RELIABILITY_THRESHOLD = 0.70


async def run_gate():
    """Execute the go/no-go gate analysis."""
    from a2a_detection.data.erc8004 import fetch_all_agents
    from a2a_detection.data.transactions import DuneClient

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    # ─── Step 1: Fetch ERC-8004 agent addresses ───
    logger.info("=" * 60)
    logger.info("STEP 1: Fetching ERC-8004 registered agent addresses")
    logger.info("=" * 60)

    registry = await fetch_all_agents(chains=["base", "ethereum", "bnb"])
    registry.save(DATA_DIR / "erc8004_agents.parquet")

    agent_addresses = registry.addresses
    logger.info(f"Total unique agent addresses: {len(agent_addresses)}")
    for chain, agents in registry.by_chain.items():
        logger.info(f"  {chain}: {len(agents)} registrations")

    # ─── Step 2: Query x402/USDC transaction participants ───
    logger.info("=" * 60)
    logger.info("STEP 2: Querying on-chain transaction participants")
    logger.info("=" * 60)

    dune = DuneClient()

    # Run the overlap analysis query
    overlap_sql = (QUERIES_DIR / "03_overlap_analysis.sql").read_text()
    logger.info("Running overlap analysis query on Dune (this may take a few minutes)...")

    try:
        overlap_results = await dune.run_sql(overlap_sql)
        overlap_results.to_parquet(DATA_DIR / "overlap_results.parquet", index=False)
        logger.info(f"Overlap query returned {len(overlap_results)} rows")
    except Exception as e:
        logger.warning(f"Dune SQL query failed: {e}")
        logger.info("Falling back to address-level analysis...")
        overlap_results = pd.DataFrame()

    # ─── Step 3: Compute overlap metrics ───
    logger.info("=" * 60)
    logger.info("STEP 3: Computing overlap metrics")
    logger.info("=" * 60)

    if len(overlap_results) > 0:
        metrics = overlap_results.iloc[0].to_dict()
    else:
        # Fallback: manual cross-reference
        metrics = {
            "total_erc8004_agents": len(agent_addresses),
            "agents_with_usdc_activity": "REQUIRES_DUNE_QUERY",
            "agents_with_any_base_activity": "REQUIRES_DUNE_QUERY",
            "pct_agents_with_usdc": "REQUIRES_DUNE_QUERY",
            "note": "Dune query failed — run queries/03_overlap_analysis.sql manually on dune.com",
        }

    for k, v in metrics.items():
        logger.info(f"  {k}: {v}")

    # ─── Step 4: Go/No-Go Decision ───
    logger.info("=" * 60)
    logger.info("STEP 4: GO / NO-GO DECISION")
    logger.info("=" * 60)

    overlap_count = metrics.get("agents_with_usdc_activity", 0)
    if isinstance(overlap_count, str):
        logger.warning("Cannot compute go/no-go automatically — Dune query needs manual execution.")
        logger.info(f"Run queries/03_overlap_analysis.sql on dune.com")
        logger.info(f"GO threshold: ≥ {MIN_OVERLAP_ADDRESSES} agents with USDC activity")
        decision = "MANUAL_REVIEW_REQUIRED"
    elif overlap_count >= MIN_OVERLAP_ADDRESSES:
        decision = "GO"
        logger.info(f"✓ GO — {overlap_count} agents with USDC activity (threshold: {MIN_OVERLAP_ADDRESSES})")
    else:
        logger.info(f"✗ Overlap below threshold ({overlap_count} < {MIN_OVERLAP_ADDRESSES})")
        logger.info("  Checking expansion sources (Virtuals, Moltbook)...")
        decision = "EXPAND_SOURCES"

    # ─── Step 5: Generate report ───
    report = f"""# Overlap Analysis Report — Go/No-Go Gate (Plan 05-01)

**Generated:** {pd.Timestamp.now().isoformat()}
**Decision:** {decision}

---

## ERC-8004 Agent Registry

| Metric | Value |
|--------|-------|
| Total unique agent addresses | {len(agent_addresses)} |
"""
    for chain, agents in registry.by_chain.items():
        report += f"| Agents on {chain} | {len(agents)} |\n"

    report += f"""
## Overlap Metrics

"""
    for k, v in metrics.items():
        report += f"| {k} | {v} |\n"

    report += f"""
## Go/No-Go Decision

**Threshold:** ≥ {MIN_OVERLAP_ADDRESSES} agents with USDC activity on Base
**Result:** {decision}

### Next Steps

"""
    if decision == "GO":
        report += """- Proceed to Plan 05-02: Data Ingestion Pipeline
- Build labeled dataset from cross-referenced addresses
- Target: ≥10K agent transactions
"""
    elif decision == "EXPAND_SOURCES":
        report += """- Expand to additional data sources:
  1. Virtuals Protocol agent token transactions
  2. Moltbook MOLT token interactions
  3. Behavioral heuristics (velocity, timing patterns)
- Re-evaluate with expanded address set
"""
    else:
        report += f"""- Run queries/03_overlap_analysis.sql manually on dune.com
- Compare results against threshold: ≥ {MIN_OVERLAP_ADDRESSES}
- Update this report with results
"""

    (ANALYSIS_DIR / "overlap-analysis.md").write_text(report)
    logger.info(f"Report saved to analysis/overlap-analysis.md")
    logger.info(f"FINAL DECISION: {decision}")

    return decision


def main():
    """Entry point."""
    decision = asyncio.run(run_gate())
    sys.exit(0 if decision in ("GO", "MANUAL_REVIEW_REQUIRED") else 1)


if __name__ == "__main__":
    main()
