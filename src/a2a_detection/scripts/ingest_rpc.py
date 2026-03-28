"""Data ingestion via public RPCs (no API keys required).

Collects ERC-20 Transfer events for known ERC-8004 agents using
eth_getLogs batched in 10k-block windows across multiple RPCs.

Outputs:
    data/agent_transfers_raw.json  — raw transfer events
    data/transactions.parquet      — framework-ready transactions
    data/labels.parquet            — agent/human address labels
"""

from __future__ import annotations

import json
import logging
import ssl
import time
import urllib.request
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Public Base RPCs (round-robin for rate limit distribution)
RPCS = [
    "https://1rpc.io/base",
    "https://base.drpc.org",
    "https://base-rpc.publicnode.com",
]

# Well-known contracts
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

# Known token decimals on Base
TOKEN_DECIMALS = {
    USDC_BASE.lower(): 6,
    "0x50c5725949a6f0c72e6c4a641f24049a917db0cb": 18,  # DAI
    "0x4200000000000000000000000000000000000006": 18,  # WETH
    "0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec22": 18,  # cbETH
    "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca": 6,   # USDbC
}

SSL_CTX = ssl.create_default_context()


class RPCClient:
    """Round-robin JSON-RPC client across multiple public endpoints."""

    def __init__(self, rpcs: list[str] | None = None):
        self.rpcs = rpcs or RPCS
        self._idx = 0

    def call(self, method: str, params: list, retries: int = 3) -> dict | None:
        for attempt in range(retries):
            rpc = self.rpcs[self._idx % len(self.rpcs)]
            self._idx += 1
            try:
                payload = json.dumps(
                    {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
                ).encode()
                req = urllib.request.Request(
                    rpc,
                    data=payload,
                    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                )
                resp = urllib.request.urlopen(req, timeout=15, context=SSL_CTX)
                data = json.loads(resp.read())
                if "error" in data:
                    logger.debug(f"RPC error from {rpc}: {data['error']}")
                    time.sleep(0.5)
                    continue
                return data
            except Exception as e:
                logger.debug(f"RPC exception from {rpc}: {e}")
                time.sleep(0.5)
        return None

    def get_block_number(self) -> int:
        res = self.call("eth_blockNumber", [])
        return int(res["result"], 16) if res else 0


def collect_transfers(
    rpc: RPCClient,
    agents: list[str],
    scan_depth: int = 100_000,
    delay: float = 0.2,
) -> list[dict]:
    """Collect ERC-20 Transfer events for a list of agent addresses.

    Scans the last `scan_depth` blocks in 10k-block windows.
    Returns raw transfer records.
    """
    current_block = rpc.get_block_number()
    start_block = current_block - scan_depth
    all_transfers = []

    logger.info(f"Scanning blocks {start_block}..{current_block} for {len(agents)} agents")

    for i, agent_addr in enumerate(agents):
        addr_padded = "0x" + agent_addr[2:].zfill(64)
        agent_before = len(all_transfers)

        for chunk_start in range(start_block, current_block, 10_000):
            chunk_end = min(chunk_start + 9_999, current_block)

            # Inbound transfers (to=agent)
            res = rpc.call("eth_getLogs", [{
                "fromBlock": hex(chunk_start),
                "toBlock": hex(chunk_end),
                "topics": [TRANSFER_TOPIC, None, addr_padded],
            }])
            if res and "result" in res:
                for log in res["result"]:
                    sender = "0x" + log["topics"][1][26:] if len(log["topics"]) > 1 else ""
                    value = int(log["data"], 16) if log["data"] != "0x" else 0
                    all_transfers.append({
                        "block": int(log["blockNumber"], 16),
                        "tx_hash": log["transactionHash"],
                        "token_contract": log["address"].lower(),
                        "sender": sender.lower(),
                        "receiver": agent_addr,
                        "value_raw": str(value),
                        "direction": "in",
                        "agent": agent_addr,
                    })
            time.sleep(delay)

            # Outbound transfers (from=agent)
            res2 = rpc.call("eth_getLogs", [{
                "fromBlock": hex(chunk_start),
                "toBlock": hex(chunk_end),
                "topics": [TRANSFER_TOPIC, addr_padded, None],
            }])
            if res2 and "result" in res2:
                for log in res2["result"]:
                    receiver = "0x" + log["topics"][2][26:] if len(log["topics"]) > 2 else ""
                    value = int(log["data"], 16) if log["data"] != "0x" else 0
                    all_transfers.append({
                        "block": int(log["blockNumber"], 16),
                        "tx_hash": log["transactionHash"],
                        "token_contract": log["address"].lower(),
                        "sender": agent_addr,
                        "receiver": receiver.lower(),
                        "value_raw": str(value),
                        "direction": "out",
                        "agent": agent_addr,
                    })
            time.sleep(delay)

        agent_count = len(all_transfers) - agent_before
        logger.info(f"  [{i+1}/{len(agents)}] {agent_addr[:12]}...: {agent_count} transfers")

    logger.info(f"Total transfers collected: {len(all_transfers)}")
    return all_transfers


def transfers_to_dataset(
    transfers: list[dict],
    agent_addresses: set[str],
    overlap_data: dict | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Convert raw transfers to framework-ready transactions + labels DataFrames.

    Args:
        transfers: Raw transfer records from collect_transfers().
        agent_addresses: Full set of known ERC-8004 agent addresses.
        overlap_data: Optional overlap_results.json data for enrichment.

    Returns:
        (transactions_df, labels_df) ready for TransactionDataset.
    """
    if not transfers:
        return pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(transfers)

    # Convert raw values to USDC-equivalent amounts
    df["decimals"] = df["token_contract"].map(
        lambda c: TOKEN_DECIMALS.get(c, 18)
    )
    df["amount_raw"] = df["value_raw"].astype(float)
    df["amount"] = df["amount_raw"] / (10 ** df["decimals"])

    # For USDC, amount is already in USD. For others, we'd need price feeds.
    # For now, flag USDC transactions and use raw amount for others.
    df["is_usdc"] = df["token_contract"] == USDC_BASE.lower()
    df["amount_usdc"] = df.apply(
        lambda r: r["amount"] if r["is_usdc"] else 0.0, axis=1
    )

    # Build transactions DataFrame
    transactions = df[[
        "tx_hash", "block", "sender", "receiver",
        "amount_usdc", "token_contract", "amount", "direction",
    ]].copy()
    transactions.rename(columns={"block": "block_number"}, inplace=True)

    # Approximate timestamp from block number (Base: ~2s blocks)
    # Use a reference point for estimation
    if len(transactions) > 0:
        max_block = transactions["block_number"].max()
        import datetime
        now_ts = int(datetime.datetime.now().timestamp())
        transactions["timestamp"] = transactions["block_number"].apply(
            lambda b: str(datetime.datetime.fromtimestamp(
                now_ts - (max_block - b) * 2
            ))
        )

    # Build labels DataFrame
    all_addresses = set(df["sender"].unique()) | set(df["receiver"].unique())
    agent_addrs_lower = {a.lower() for a in agent_addresses}

    labels_records = []
    for addr in all_addresses:
        if not addr or addr == "0x" + "0" * 40:
            continue
        is_agent = addr.lower() in agent_addrs_lower
        labels_records.append({
            "address": addr.lower(),
            "label": "agent" if is_agent else "human",
            "source": "erc8004_registry" if is_agent else "counterparty",
            "confidence": 1.0 if is_agent else 0.7,
        })

    labels = pd.DataFrame(labels_records)

    # Enrich with overlap data if available
    if overlap_data:
        balance_map = {}
        for entry in overlap_data.get("top_tx_count", []):
            balance_map[entry["address"]] = {
                "usdc_balance": entry.get("usdc_balance", 0),
                "eth_balance": entry.get("eth_balance", 0),
                "known_tx_count": entry.get("tx_count", 0),
            }
        for entry in overlap_data.get("top_usdc_holders", []):
            if entry["address"] not in balance_map:
                balance_map[entry["address"]] = {
                    "usdc_balance": entry.get("usdc_balance", 0),
                    "eth_balance": entry.get("eth_balance", 0),
                    "known_tx_count": entry.get("tx_count", 0),
                }

    logger.info(
        f"Dataset: {len(transactions)} transactions, "
        f"{len(labels)} labeled addresses "
        f"({len(labels[labels['label']=='agent'])} agents, "
        f"{len(labels[labels['label']=='human'])} human)"
    )

    return transactions, labels


def run_ingestion(
    data_dir: Path,
    agents_file: str = "base_erc8004_agents.json",
    overlap_file: str = "overlap_results.json",
    max_agents: int = 20,
    scan_depth: int = 100_000,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Full ingestion pipeline: RPC → parquet files.

    Returns (transactions_df, labels_df).
    """
    data_dir = Path(data_dir)

    # Load agent addresses
    with open(data_dir / agents_file) as f:
        agent_data = json.load(f)
    all_agent_addrs = set(a.lower() for a in agent_data["addresses"])

    # Load overlap data for prioritization
    with open(data_dir / overlap_file) as f:
        overlap = json.load(f)

    # Prioritize most active agents
    priority = [
        a["address"] for a in overlap["top_tx_count"]
        if a["tx_count"] > 0
    ][:max_agents]

    logger.info(f"Ingesting {len(priority)} priority agents from {len(all_agent_addrs)} total")

    # Collect transfers
    rpc = RPCClient()
    transfers = collect_transfers(rpc, priority, scan_depth=scan_depth)

    # Save raw
    with open(data_dir / "agent_transfers_raw.json", "w") as f:
        json.dump(transfers, f)

    # Convert to dataset format
    transactions, labels = transfers_to_dataset(transfers, all_agent_addrs, overlap)

    # Save as parquet
    if len(transactions) > 0:
        transactions.to_parquet(data_dir / "transactions.parquet", index=False)
    if len(labels) > 0:
        labels.to_parquet(data_dir / "labels.parquet", index=False)

    logger.info(f"Saved to {data_dir}/transactions.parquet and labels.parquet")
    return transactions, labels


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    data_dir = Path(__file__).resolve().parents[3] / "data"
    run_ingestion(data_dir)
