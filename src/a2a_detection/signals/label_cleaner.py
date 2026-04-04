"""Label cleaner for improving negative-class quality.

The "human" negative labels in our dataset are derived from
counterparty_default (confidence=0.70) — i.e., addresses that appeared
on the other side of transactions with known ERC-8004 agents. This is a
weak signal: smart contracts, MEV bots, DEX pools, and thin counterparties
all get labeled "human" by this heuristic.

Two cleaning passes are applied in order:

1. EOA Verification (requires web3 RPC):
   Any address with non-zero bytecode (eth_getCode != "0x") is a smart
   contract, not an EOA, and should be removed from the negative class.
   If no RPC endpoint is configured, this pass is skipped with a warning.

2. Minimum Activity Filter (always available):
   Addresses with fewer than MIN_TX_COUNT transactions over fewer than
   MIN_DAYS_ACTIVE days are thin counterparties — unreliable as negatives
   because their behavior sample is too small to characterize.
   Default: MIN_TX_COUNT=5, MIN_DAYS_ACTIVE=1 (any activity threshold).
"""

from __future__ import annotations

import logging
import os
from typing import Callable

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Minimum activity thresholds for a valid negative label
MIN_TX_COUNT = 5      # fewer than this → thin counterparty, remove
MIN_DAYS_ACTIVE = 1   # require at least N distinct calendar days of activity


def filter_thin_counterparties(
    labels: pd.DataFrame,
    transactions: pd.DataFrame,
    min_tx_count: int = MIN_TX_COUNT,
    min_days_active: int = MIN_DAYS_ACTIVE,
    label_column: str = "label",
    human_label: str = "human",
) -> tuple[pd.DataFrame, dict]:
    """Remove thin human-labeled counterparties from the negative class.

    An address is considered a thin counterparty if it has fewer than
    min_tx_count total transactions (in+out) across the dataset. These
    addresses were likely on the receiving end of a single agent transfer
    and carry no reliable behavioral signal.

    Args:
        labels: DataFrame with 'address' and label columns.
        transactions: Full transaction DataFrame (sender/receiver columns).
        min_tx_count: Minimum total transactions to keep a human label.
        min_days_active: Minimum distinct active days (if timestamp available).
        label_column: Name of the label column.
        human_label: Value identifying human/negative-class addresses.

    Returns:
        (cleaned_labels, stats) where stats reports how many were removed.
    """
    txns = transactions.copy()
    txns["sender"] = txns["sender"].str.lower()
    txns["receiver"] = txns["receiver"].str.lower()

    # Count total transactions per address (sender + receiver appearances)
    addr_tx_counts = (
        pd.concat([txns["sender"], txns["receiver"]])
        .value_counts()
        .rename("tx_count")
    )

    # Optionally count distinct active days
    days_active: pd.Series | None = None
    if "timestamp" in txns.columns:
        txns["_date"] = pd.to_datetime(txns["timestamp"]).dt.date
        addr_dates = (
            txns.melt(id_vars=["_date"], value_vars=["sender", "receiver"], value_name="address")
            [["address", "_date"]]
            .drop_duplicates()
        )
        days_active = addr_dates.groupby("address")["_date"].nunique().rename("days_active")

    # Annotate labels with activity metrics
    df = labels.copy()
    df["address_lc"] = df["address"].str.lower()
    df["_tx_count"] = df["address_lc"].map(addr_tx_counts).fillna(0).astype(int)
    if days_active is not None:
        df["_days_active"] = df["address_lc"].map(days_active).fillna(0).astype(int)
    else:
        df["_days_active"] = 1  # unknown → assume meets threshold

    human_mask = df[label_column] == human_label
    thin_mask = human_mask & (
        (df["_tx_count"] < min_tx_count) |
        (df["_days_active"] < min_days_active)
    )

    n_human_before = human_mask.sum()
    n_removed = thin_mask.sum()

    cleaned = df[~thin_mask].drop(columns=["address_lc", "_tx_count", "_days_active"])

    stats = {
        "human_labels_before": int(n_human_before),
        "thin_counterparties_removed": int(n_removed),
        "human_labels_after": int(n_human_before - n_removed),
        "pct_removed": round(n_removed / n_human_before * 100, 1) if n_human_before > 0 else 0.0,
        "min_tx_count_threshold": min_tx_count,
        "min_days_active_threshold": min_days_active,
    }

    logger.info(
        f"Thin counterparty filter: removed {n_removed}/{n_human_before} "
        f"human labels ({stats['pct_removed']}%) with <{min_tx_count} txs"
    )
    return cleaned, stats


def filter_smart_contracts(
    labels: pd.DataFrame,
    rpc_url: str | None = None,
    label_column: str = "label",
    human_label: str = "human",
    batch_size: int = 50,
) -> tuple[pd.DataFrame, dict]:
    """Remove smart contract addresses from the negative (human) class.

    Uses eth_getCode via web3 to check if an address has deployed bytecode.
    Any address with non-empty bytecode is a contract, not an EOA, and is
    removed from the human negative class.

    Requires a working Ethereum/Base RPC endpoint. If none is configured,
    this function logs a warning and returns the labels unchanged.

    Args:
        labels: DataFrame with 'address' and label columns.
        rpc_url: HTTP(S) RPC endpoint URL. Falls back to RPC_URL env var.
        label_column: Name of the label column.
        human_label: Value identifying human/negative-class addresses.
        batch_size: Addresses to check per RPC batch (rate limiting).

    Returns:
        (cleaned_labels, stats) where stats reports how many contracts found.
    """
    rpc_url = rpc_url or os.environ.get("RPC_URL") or os.environ.get("BASE_RPC_URL")

    if not rpc_url:
        logger.warning(
            "EOA filter skipped: no RPC_URL configured. "
            "Set RPC_URL=https://... environment variable to enable contract filtering. "
            "Falling back to minimum-activity filter only."
        )
        return labels, {
            "eoa_filter_applied": False,
            "reason": "no RPC_URL configured",
            "contracts_removed": 0,
        }

    try:
        from web3 import Web3
    except ImportError:
        logger.warning("EOA filter skipped: web3 not installed (pip install web3).")
        return labels, {
            "eoa_filter_applied": False,
            "reason": "web3 not installed",
            "contracts_removed": 0,
        }

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        logger.warning(f"EOA filter skipped: cannot connect to RPC at {rpc_url}")
        return labels, {
            "eoa_filter_applied": False,
            "reason": f"RPC connection failed: {rpc_url}",
            "contracts_removed": 0,
        }

    human_labels = labels[labels[label_column] == human_label]
    addresses = human_labels["address"].str.lower().unique().tolist()
    logger.info(f"EOA check: querying {len(addresses)} human-labeled addresses via RPC...")

    contract_addresses: set[str] = set()
    for i in range(0, len(addresses), batch_size):
        batch = addresses[i : i + batch_size]
        for addr in batch:
            try:
                code = w3.eth.get_code(Web3.to_checksum_address(addr))
                if code and code != b"" and code != b"0x":
                    contract_addresses.add(addr)
            except Exception as e:
                logger.debug(f"eth_getCode failed for {addr}: {e}")

    is_contract = labels["address"].str.lower().isin(contract_addresses)
    is_human = labels[label_column] == human_label
    remove_mask = is_contract & is_human

    n_removed = remove_mask.sum()
    cleaned = labels[~remove_mask]

    stats = {
        "eoa_filter_applied": True,
        "addresses_checked": len(addresses),
        "contracts_found": len(contract_addresses),
        "contracts_removed": int(n_removed),
        "rpc_url": rpc_url,
    }

    logger.info(
        f"EOA filter: found {len(contract_addresses)} contracts among human labels, "
        f"removed {n_removed} rows"
    )
    return cleaned, stats


def clean_labels(
    labels: pd.DataFrame,
    transactions: pd.DataFrame,
    rpc_url: str | None = None,
    min_tx_count: int = MIN_TX_COUNT,
    min_days_active: int = MIN_DAYS_ACTIVE,
    label_column: str = "label",
    human_label: str = "human",
) -> tuple[pd.DataFrame, dict]:
    """Apply full label cleaning pipeline (EOA check + activity filter).

    Applies both cleaning passes in priority order:
    1. EOA verification (removes smart contracts if RPC available)
    2. Minimum activity filter (removes thin counterparties)

    Args:
        labels: DataFrame with 'address' and label columns.
        transactions: Full transaction DataFrame.
        rpc_url: Optional RPC endpoint for EOA checking.
        min_tx_count: Minimum transactions for a valid human label.
        min_days_active: Minimum active days for a valid human label.
        label_column: Name of the label column in the DataFrame.
        human_label: Value identifying negative-class addresses.

    Returns:
        (cleaned_labels, stats) combining stats from both passes.
    """
    all_stats: dict = {"n_labels_original": len(labels)}

    # Pass 1: EOA verification
    labels, eoa_stats = filter_smart_contracts(
        labels, rpc_url=rpc_url,
        label_column=label_column, human_label=human_label,
    )
    all_stats["eoa_filter"] = eoa_stats

    # Pass 2: minimum activity filter
    labels, activity_stats = filter_thin_counterparties(
        labels, transactions,
        min_tx_count=min_tx_count, min_days_active=min_days_active,
        label_column=label_column, human_label=human_label,
    )
    all_stats["activity_filter"] = activity_stats
    all_stats["n_labels_after_cleaning"] = len(labels)

    return labels, all_stats
