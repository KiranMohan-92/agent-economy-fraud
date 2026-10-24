"""Cohort filters for explicit registry-proxy and counterparty-unknown labels.

The source data establishes only two facts:

* ``registry_owner_proxy``: the address appears in the historical registry
  owner/default-wallet extraction.
* ``counterparty_unknown``: the address transacted with a registry proxy but
  has no verified operator type or outcome label.

Filtering contracts or low-activity addresses can make a descriptive
comparison cohort less heterogeneous. It never turns an unknown counterparty
into a verified human, a verified negative, or outcome ground truth.
"""

from __future__ import annotations

import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)

REGISTRY_OWNER_PROXY_LABEL = "registry_owner_proxy"
COUNTERPARTY_UNKNOWN_LABEL = "counterparty_unknown"

MIN_TX_COUNT = 5
MIN_DAYS_ACTIVE = 1


def _validate_columns(frame: pd.DataFrame, required: set[str], frame_name: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{frame_name} missing required columns: {missing}")


def _require_explicit_labels(labels: pd.DataFrame, label_column: str) -> None:
    """Reject the historical agent/human schema instead of silently reusing it."""
    _validate_columns(labels, {"address", label_column}, "labels")
    observed = set(labels[label_column].dropna().astype(str).unique())
    legacy = observed & {"agent", "human"}
    if legacy:
        raise ValueError(
            "Legacy agent/human labels are not construct-valid. Rebuild labels "
            "as registry_owner_proxy/counterparty_unknown before cleaning."
        )


def filter_thin_counterparties(
    labels: pd.DataFrame,
    transactions: pd.DataFrame,
    min_tx_count: int = MIN_TX_COUNT,
    min_days_active: int = MIN_DAYS_ACTIVE,
    label_column: str = "label",
    counterparty_label: str = COUNTERPARTY_UNKNOWN_LABEL,
) -> tuple[pd.DataFrame, dict]:
    """Exclude thin unknown counterparties from a descriptive comparison cohort.

    The retained rows remain ``counterparty_unknown``. Activity is a sampling
    sufficiency rule, not evidence about operator identity or outcome status.
    """
    _validate_columns(labels, {"address", label_column}, "labels")
    _validate_columns(transactions, {"sender", "receiver"}, "transactions")
    if min_tx_count < 0 or min_days_active < 0:
        raise ValueError("activity thresholds must be non-negative")

    txns = transactions.copy()
    txns["sender"] = txns["sender"].astype(str).str.lower()
    txns["receiver"] = txns["receiver"].astype(str).str.lower()

    addr_tx_counts = pd.concat([txns["sender"], txns["receiver"]]).value_counts()

    days_active: pd.Series | None = None
    if "timestamp" in txns.columns:
        txns["_date"] = pd.to_datetime(txns["timestamp"], utc=True).dt.date
        addr_dates = (
            txns.melt(
                id_vars=["_date"],
                value_vars=["sender", "receiver"],
                value_name="address",
            )[["address", "_date"]]
            .drop_duplicates()
        )
        days_active = addr_dates.groupby("address")["_date"].nunique()

    frame = labels.copy()
    frame["_address_lc"] = frame["address"].astype(str).str.lower()
    frame["_tx_count"] = frame["_address_lc"].map(addr_tx_counts).fillna(0).astype(int)
    if days_active is None:
        frame["_days_active"] = 1
    else:
        frame["_days_active"] = (
            frame["_address_lc"].map(days_active).fillna(0).astype(int)
        )

    comparison_mask = frame[label_column] == counterparty_label
    thin_mask = comparison_mask & (
        (frame["_tx_count"] < min_tx_count)
        | (frame["_days_active"] < min_days_active)
    )
    before = int(comparison_mask.sum())
    removed = int(thin_mask.sum())
    cleaned = frame.loc[~thin_mask].drop(
        columns=["_address_lc", "_tx_count", "_days_active"]
    )

    stats = {
        "counterparty_label": counterparty_label,
        "counterparty_unknown_before": before,
        "thin_counterparties_removed": removed,
        "counterparty_unknown_after": before - removed,
        "pct_removed": round(removed / before * 100, 1) if before else 0.0,
        "min_tx_count_threshold": min_tx_count,
        "min_days_active_threshold": min_days_active,
        "remaining_counterparties_are_verified_humans": False,
        "remaining_counterparties_are_verified_negatives": False,
    }
    logger.info(
        "Thin-counterparty cohort filter removed %s/%s unknown counterparties",
        removed,
        before,
    )
    return cleaned, stats


def filter_smart_contracts(
    labels: pd.DataFrame,
    rpc_url: str | None = None,
    label_column: str = "label",
    counterparty_label: str = COUNTERPARTY_UNKNOWN_LABEL,
    batch_size: int = 50,
) -> tuple[pd.DataFrame, dict]:
    """Exclude bytecode-bearing addresses from the unknown-counterparty cohort.

    An empty-code response is evidence only that no bytecode was observed at
    the queried block. It is not evidence that a human controls the address.
    """
    _validate_columns(labels, {"address", label_column}, "labels")
    rpc_url = rpc_url or os.environ.get("RPC_URL") or os.environ.get("BASE_RPC_URL")
    base_stats = {
        "counterparty_label": counterparty_label,
        "remaining_counterparties_are_verified_humans": False,
        "remaining_counterparties_are_verified_negatives": False,
    }

    if not rpc_url:
        logger.warning("Contract-code filter skipped: no RPC URL configured")
        return labels, {
            **base_stats,
            "contract_code_filter_applied": False,
            "reason": "no RPC URL configured",
            "contracts_removed": 0,
        }

    try:
        from web3 import Web3
    except ImportError:
        logger.warning("Contract-code filter skipped: web3 is not installed")
        return labels, {
            **base_stats,
            "contract_code_filter_applied": False,
            "reason": "web3 not installed",
            "contracts_removed": 0,
        }

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        logger.warning("Contract-code filter skipped: RPC connection failed")
        return labels, {
            **base_stats,
            "contract_code_filter_applied": False,
            "reason": "RPC connection failed",
            "contracts_removed": 0,
        }

    comparison = labels[labels[label_column] == counterparty_label]
    addresses = comparison["address"].astype(str).str.lower().unique().tolist()
    contract_addresses: set[str] = set()
    failures = 0
    for start in range(0, len(addresses), batch_size):
        for address in addresses[start : start + batch_size]:
            try:
                code = w3.eth.get_code(Web3.to_checksum_address(address))
                if code and bytes(code) not in {b"", b"0x"}:
                    contract_addresses.add(address)
            except Exception as exc:  # an unknown RPC result must stay unknown
                failures += 1
                logger.debug("eth_getCode failed for %s: %s", address, exc)

    remove_mask = (
        labels["address"].astype(str).str.lower().isin(contract_addresses)
        & (labels[label_column] == counterparty_label)
    )
    removed = int(remove_mask.sum())
    cleaned = labels.loc[~remove_mask]
    return cleaned, {
        **base_stats,
        "contract_code_filter_applied": True,
        "addresses_checked": len(addresses),
        "rpc_failures": failures,
        "contracts_found": len(contract_addresses),
        "contracts_removed": removed,
    }


def clean_labels(
    labels: pd.DataFrame,
    transactions: pd.DataFrame,
    rpc_url: str | None = None,
    min_tx_count: int = MIN_TX_COUNT,
    min_days_active: int = MIN_DAYS_ACTIVE,
    label_column: str = "label",
    counterparty_label: str = COUNTERPARTY_UNKNOWN_LABEL,
) -> tuple[pd.DataFrame, dict]:
    """Apply descriptive cohort filters without manufacturing ground truth."""
    _require_explicit_labels(labels, label_column)
    stats: dict = {
        "n_labels_original": len(labels),
        "label_semantics": {
            "positive_proxy": REGISTRY_OWNER_PROXY_LABEL,
            "comparison_cohort": counterparty_label,
            "verified_human_negative_class_available": False,
            "outcome_ground_truth_available": False,
        },
    }

    filtered, contract_stats = filter_smart_contracts(
        labels,
        rpc_url=rpc_url,
        label_column=label_column,
        counterparty_label=counterparty_label,
    )
    filtered, activity_stats = filter_thin_counterparties(
        filtered,
        transactions,
        min_tx_count=min_tx_count,
        min_days_active=min_days_active,
        label_column=label_column,
        counterparty_label=counterparty_label,
    )
    stats["contract_code_filter"] = contract_stats
    stats["activity_filter"] = activity_stats
    stats["n_labels_after_cleaning"] = len(filtered)
    return filtered, stats
