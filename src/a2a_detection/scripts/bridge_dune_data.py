"""Bridge Dune Analytics CSV output to detection pipeline parquet format.

Converts Dune query results (real evt_block_time timestamps) into the
framework-ready format expected by the signal scorers:
    - transactions.parquet: tx_hash, block_number, timestamp, sender,
      receiver, amount_usdc, token_contract, direction [, chain]
    - labels.parquet: address, label, source, confidence

Replaces synthetic timestamps from ingest_rpc.py with real on-chain
timestamps, closing GAP-01 (Value Flow) and GAP-02 (Temporal Consistency).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"


def load_agent_addresses() -> set[str]:
    """Load known ERC-8004 agent addresses."""
    path = DATA_DIR / "base_erc8004_agents.json"
    with open(path) as f:
        data = json.load(f)
    return {a.lower() for a in data["addresses"]}


def bridge_base_transactions(csv_path: Path, agents: set[str]) -> pd.DataFrame:
    """Convert Query 04 CSV (Base USDC histories) to pipeline format."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path.name}")

    # Normalize column names (Dune returns lowercase)
    col_map = {
        "evt_tx_hash": "tx_hash",
        "evt_block_number": "block_number",
        "evt_block_time": "timestamp",
        "sender": "sender",
        "receiver": "receiver",
        "amount_usdc": "amount_usdc",
    }
    df = df.rename(columns=col_map)

    # Ensure required columns exist
    for col in ["tx_hash", "block_number", "timestamp", "sender", "receiver", "amount_usdc"]:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}. Available: {list(df.columns)}")

    # Normalize addresses to lowercase
    df["sender"] = df["sender"].astype(str).str.lower()
    df["receiver"] = df["receiver"].astype(str).str.lower()
    df["tx_hash"] = df["tx_hash"].astype(str).str.lower()

    # Add token_contract (all USDC on Base)
    df["token_contract"] = USDC_BASE

    # Add direction relative to known agents
    df["direction"] = df.apply(
        lambda r: "outbound" if r["sender"] in agents else "inbound",
        axis=1,
    )

    # Deduplicate (UNION ALL in query may produce duplicates for agent-to-agent txns)
    before = len(df)
    df = df.drop_duplicates(subset="tx_hash")
    if before > len(df):
        print(f"  Deduped: {before} -> {len(df)} rows ({before - len(df)} agent-to-agent dupes)")

    # Parse timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def bridge_multichain(csv_path: Path, agents: set[str]) -> pd.DataFrame:
    """Convert Query 05 CSV (multi-chain) to pipeline format with chain column."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path.name}")

    col_map = {
        "evt_tx_hash": "tx_hash",
        "evt_block_number": "block_number",
        "evt_block_time": "timestamp",
        "sender": "sender",
        "receiver": "receiver",
        "amount_usdc": "amount_usdc",
        "chain": "chain",
    }
    df = df.rename(columns=col_map)

    df["sender"] = df["sender"].astype(str).str.lower()
    df["receiver"] = df["receiver"].astype(str).str.lower()
    df["tx_hash"] = df["tx_hash"].astype(str).str.lower()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["direction"] = df.apply(
        lambda r: "outbound" if r["sender"] in agents else "inbound",
        axis=1,
    )

    before = len(df)
    df = df.drop_duplicates(subset=["tx_hash", "chain"])
    if before > len(df):
        print(f"  Deduped: {before} -> {len(df)} rows")

    return df


def build_labels(transactions: pd.DataFrame, agents: set[str]) -> pd.DataFrame:
    """Build labels DataFrame from transaction participants."""
    all_addresses = set(transactions["sender"].unique()) | set(transactions["receiver"].unique())

    records = []
    for addr in all_addresses:
        if not addr or addr == "0x" + "0" * 40:
            continue
        if addr in agents:
            records.append({
                "address": addr,
                "label": "agent",
                "source": "erc8004_registry",
                "confidence": 1.0,
            })
        else:
            records.append({
                "address": addr,
                "label": "human",
                "source": "counterparty_default",
                "confidence": 0.7,
            })

    labels = pd.DataFrame(records)
    agent_count = (labels["label"] == "agent").sum()
    human_count = (labels["label"] == "human").sum()
    print(f"Labels: {agent_count} agents, {human_count} humans ({len(labels)} total)")
    return labels


def validate_timestamps(df: pd.DataFrame) -> None:
    """Verify timestamps are real (not synthetic uniform spacing)."""
    ts = pd.to_datetime(df["timestamp"])
    gaps = ts.sort_values().diff().dropna().dt.total_seconds()

    unique_gaps = gaps.nunique()
    std_gap = gaps.std()

    print(f"  Timestamp validation:")
    print(f"    Date range: {ts.min()} to {ts.max()}")
    print(f"    Unique gap values: {unique_gaps} (synthetic would be ~1)")
    print(f"    Gap std dev: {std_gap:.1f}s (synthetic would be ~0)")
    print(f"    Min gap: {gaps.min():.1f}s, Max gap: {gaps.max():.1f}s")

    if unique_gaps < 5:
        print("    WARNING: Low timestamp diversity — may still be synthetic!")
    else:
        print("    PASS: Real timestamps confirmed")


def main():
    agents = load_agent_addresses()
    print(f"Loaded {len(agents)} agent addresses\n")

    # Bridge Base chain transactions (Query 04)
    base_csv = DATA_DIR / "dune_agent_transactions.csv"
    if base_csv.exists():
        print("=" * 60)
        print("Bridging Query 04: Base USDC Transaction Histories")
        print("=" * 60)
        base_txns = bridge_base_transactions(base_csv, agents)
        validate_timestamps(base_txns)

        out_path = DATA_DIR / "transactions_dune.parquet"
        base_txns.to_parquet(out_path, index=False)
        print(f"  Saved: {out_path} ({len(base_txns)} rows)\n")

        # Build labels
        labels = build_labels(base_txns, agents)
        labels_path = DATA_DIR / "labels_dune.parquet"
        labels.to_parquet(labels_path, index=False)
        print(f"  Saved: {labels_path}\n")
    else:
        print(f"Skipping Query 04 — {base_csv} not found")

    # Bridge multi-chain transactions (Query 05)
    multi_csv = DATA_DIR / "dune_multichain_activity.csv"
    if multi_csv.exists():
        print("=" * 60)
        print("Bridging Query 05: Multi-Chain Agent Activity")
        print("=" * 60)
        multi_txns = bridge_multichain(multi_csv, agents)

        chains = multi_txns["chain"].value_counts()
        print(f"  Chain distribution: {dict(chains)}")

        multi_agents = set(multi_txns["sender"].unique()) | set(multi_txns["receiver"].unique())
        multi_chain_agents = set()
        for addr in multi_agents & agents:
            addr_chains = multi_txns[
                (multi_txns["sender"] == addr) | (multi_txns["receiver"] == addr)
            ]["chain"].nunique()
            if addr_chains > 1:
                multi_chain_agents.add(addr)
        print(f"  Agents on 2+ chains: {len(multi_chain_agents)}")

        out_path = DATA_DIR / "transactions_multichain_dune.parquet"
        multi_txns.to_parquet(out_path, index=False)
        print(f"  Saved: {out_path} ({len(multi_txns)} rows)\n")
    else:
        print(f"Skipping Query 05 — {multi_csv} not found")

    print("Bridge complete.")


if __name__ == "__main__":
    main()
