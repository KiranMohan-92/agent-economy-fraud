"""Bridge Dune Analytics CSV output to detection pipeline parquet format.

Converts Dune query results (real evt_block_time timestamps) into the
framework-ready format expected by the signal scorers:
    - transactions.parquet: tx_hash, block_number, timestamp, sender,
      receiver, amount_usdc, token_contract, direction [, chain]
    - labels.parquet: address, label, source, confidence

Registry ownership is emitted as a proxy label, never as autonomous-agent or
fraud ground truth. Counterparties remain unknown rather than being called
human.

Replaces synthetic timestamps from ingest_rpc.py with real on-chain
timestamps, closing GAP-01 (Value Flow) and GAP-02 (Temporal Consistency).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from a2a_detection.signals.label_cleaner import (
    COUNTERPARTY_UNKNOWN_LABEL,
    REGISTRY_OWNER_PROXY_LABEL,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

USDC_BASE = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"


def load_registry_owner_proxies() -> set[str]:
    """Load historical ERC-8004 registry owner/default-wallet proxies."""
    path = DATA_DIR / "base_erc8004_agents.json"
    with open(path) as f:
        data = json.load(f)
    return {a.lower() for a in data["addresses"]}


def load_agent_addresses() -> set[str]:
    """Compatibility alias returning registry-owner proxies, not agent truth."""
    return load_registry_owner_proxies()


def _validate_event_identity(frame: pd.DataFrame, identity_columns: list[str]) -> None:
    """Fail closed unless every identity column is present, non-null, and non-blank.

    Must run on the raw frame, before any ``astype(str)`` normalization: that
    conversion turns a missing hash into the literal string ``"nan"``/``"none"``,
    which would then pass as a valid identity.
    """
    missing = [column for column in identity_columns if column not in frame.columns]
    if missing:
        raise ValueError(
            "Missing evt_index/event_index. Refusing lossy transaction-hash "
            "deduplication; rerun the versioned query."
        )
    identity = frame[identity_columns]
    blank = identity.apply(
        lambda column: column.map(lambda value: isinstance(value, str) and not value.strip())
    )
    if identity.isna().any().any() or blank.any().any():
        raise ValueError(
            f"Null event identity in {identity_columns}; refusing ambiguous deduplication"
        )


def _dedupe_events(frame: pd.DataFrame, identity_columns: list[str]) -> pd.DataFrame:
    """Deduplicate UNION copies only when event identity is complete and consistent."""
    _validate_event_identity(frame, identity_columns)

    duplicate_identities = frame[frame.duplicated(identity_columns, keep=False)]
    if not duplicate_identities.empty:
        distinct_rows = duplicate_identities.drop_duplicates()
        if distinct_rows.duplicated(identity_columns, keep=False).any():
            raise ValueError(
                "Conflicting rows share the same event identity; refusing to choose one"
            )
    return frame.drop_duplicates(subset=identity_columns)


def bridge_base_transactions(csv_path: Path, registry_proxies: set[str]) -> pd.DataFrame:
    """Convert Query 04 CSV (Base USDC histories) to pipeline format."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path.name}")

    # Normalize column names (Dune returns lowercase)
    col_map = {
        "evt_tx_hash": "tx_hash",
        "evt_index": "event_index",
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

    # Validate event identity on raw values, before string normalization.
    _validate_event_identity(df, ["tx_hash", "event_index"])

    # Normalize addresses to lowercase
    df["sender"] = df["sender"].astype(str).str.lower()
    df["receiver"] = df["receiver"].astype(str).str.lower()
    df["tx_hash"] = df["tx_hash"].astype(str).str.lower()

    # Add token_contract (all USDC on Base)
    df["token_contract"] = USDC_BASE

    # Add direction relative to registry-owner proxies.
    df["direction"] = df.apply(
        lambda row: "outbound" if row["sender"] in registry_proxies else "inbound",
        axis=1,
    )

    # UNION ALL duplicates a proxy-to-proxy event once through each join. Event
    # identity is (transaction hash, event index); transaction hash alone is not
    # unique because one transaction may emit multiple legitimate transfers.
    before = len(df)
    df = _dedupe_events(df, ["tx_hash", "event_index"])
    if before > len(df):
        print(
            f"  Deduped: {before} -> {len(df)} rows "
            f"({before - len(df)} proxy-to-proxy UNION copies)"
        )

    # Parse timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def bridge_multichain(csv_path: Path, registry_proxies: set[str]) -> pd.DataFrame:
    """Convert Query 05 CSV (multi-chain) to pipeline format with chain column."""
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from {csv_path.name}")

    col_map = {
        "evt_tx_hash": "tx_hash",
        "evt_index": "event_index",
        "evt_block_number": "block_number",
        "evt_block_time": "timestamp",
        "sender": "sender",
        "receiver": "receiver",
        "amount_usdc": "amount_usdc",
        "chain": "chain",
    }
    df = df.rename(columns=col_map)

    # Validate event identity on raw values, before string normalization.
    _validate_event_identity(df, ["chain", "tx_hash", "event_index"])

    df["sender"] = df["sender"].astype(str).str.lower()
    df["receiver"] = df["receiver"].astype(str).str.lower()
    df["tx_hash"] = df["tx_hash"].astype(str).str.lower()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df["direction"] = df.apply(
        lambda row: "outbound" if row["sender"] in registry_proxies else "inbound",
        axis=1,
    )

    before = len(df)
    df = _dedupe_events(df, ["chain", "tx_hash", "event_index"])
    if before > len(df):
        print(f"  Deduped: {before} -> {len(df)} rows")

    return df


def build_labels(transactions: pd.DataFrame, registry_proxies: set[str]) -> pd.DataFrame:
    """Build registry-owner-proxy and unknown-counterparty labels."""
    participants = pd.concat(
        [transactions["sender"], transactions["receiver"]], ignore_index=True
    )
    all_addresses = set(participants.dropna().astype(str).str.lower())

    normalized_proxies = {address.lower() for address in registry_proxies}
    records = []
    for addr in sorted(all_addresses):
        if not addr or addr == "0x" + "0" * 40:
            continue
        if addr in normalized_proxies:
            records.append({
                "address": addr,
                "label": REGISTRY_OWNER_PROXY_LABEL,
                "source": "erc8004_owner_or_mint_recipient",
                # Confidence is in registry-proxy membership only.
                "confidence": 1.0,
            })
        else:
            records.append({
                "address": addr,
                "label": COUNTERPARTY_UNKNOWN_LABEL,
                "source": "transaction_counterparty",
                "confidence": 0.0,
            })

    labels = pd.DataFrame(records)
    proxy_count = (labels["label"] == REGISTRY_OWNER_PROXY_LABEL).sum()
    unknown_count = (labels["label"] == COUNTERPARTY_UNKNOWN_LABEL).sum()
    print(
        f"Labels: {proxy_count} registry-owner proxies, "
        f"{unknown_count} unknown counterparties ({len(labels)} total)"
    )
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
    registry_proxies = load_registry_owner_proxies()
    print(f"Loaded {len(registry_proxies)} registry-owner proxy addresses\n")

    # Bridge Base chain transactions (Query 04)
    base_csv = DATA_DIR / "dune_agent_transactions.csv"
    if base_csv.exists():
        print("=" * 60)
        print("Bridging Query 04: Base USDC Transaction Histories")
        print("=" * 60)
        base_txns = bridge_base_transactions(base_csv, registry_proxies)
        validate_timestamps(base_txns)

        out_path = DATA_DIR / "transactions_dune.parquet"
        base_txns.to_parquet(out_path, index=False)
        print(f"  Saved: {out_path} ({len(base_txns)} rows)\n")

        # Build labels
        labels = build_labels(base_txns, registry_proxies)
        labels_path = DATA_DIR / "labels_dune.parquet"
        labels.to_parquet(labels_path, index=False)
        print(f"  Saved: {labels_path}\n")
    else:
        print(f"Skipping Query 04 — {base_csv} not found")

    # Bridge multi-chain transactions (Query 05)
    multi_csv = DATA_DIR / "dune_multichain_activity.csv"
    if multi_csv.exists():
        print("=" * 60)
        print("Bridging Query 05: Multi-Chain Registry-Proxy Activity")
        print("=" * 60)
        multi_txns = bridge_multichain(multi_csv, registry_proxies)

        chains = multi_txns["chain"].value_counts()
        print(f"  Chain distribution: {dict(chains)}")

        multi_participants = set(multi_txns["sender"].unique()) | set(
            multi_txns["receiver"].unique()
        )
        multi_chain_proxies = set()
        for addr in multi_participants & registry_proxies:
            addr_chains = multi_txns[
                (multi_txns["sender"] == addr) | (multi_txns["receiver"] == addr)
            ]["chain"].nunique()
            if addr_chains > 1:
                multi_chain_proxies.add(addr)
        print(f"  Registry-owner proxies on 2+ chains: {len(multi_chain_proxies)}")

        out_path = DATA_DIR / "transactions_multichain_dune.parquet"
        multi_txns.to_parquet(out_path, index=False)
        print(f"  Saved: {out_path} ({len(multi_txns)} rows)\n")
    else:
        print(f"Skipping Query 05 — {multi_csv} not found")

    print("Bridge complete.")


if __name__ == "__main__":
    main()
