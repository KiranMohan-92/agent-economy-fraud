"""Transaction data ingestion from Dune Analytics and block explorers.

Fetches on-chain transaction data for labeled agent and human addresses,
producing the raw dataset for signal computation and detection validation.

Primary data sources:
    - Dune Analytics API (queries in /queries/ directory)
    - BaseScan API (fallback for individual address lookups)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# USDC contract on Base
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


@dataclass
class Transaction:
    """A single on-chain transaction."""

    tx_hash: str
    block_number: int
    timestamp: str
    sender: str
    receiver: str
    amount_usdc: float
    gas_used: int | None = None
    contract_address: str | None = None


@dataclass
class TransactionDataset:
    """Labeled transaction dataset for detection framework evaluation."""

    transactions: pd.DataFrame  # columns: tx_hash, timestamp, sender, receiver, amount_usdc, ...
    labels: pd.DataFrame  # columns: address, label (agent/human/unknown), source, confidence

    @property
    def agent_transactions(self) -> pd.DataFrame:
        agent_addrs = set(self.labels[self.labels["label"] == "agent"]["address"])
        mask = self.transactions["sender"].isin(agent_addrs) | self.transactions[
            "receiver"
        ].isin(agent_addrs)
        return self.transactions[mask]

    @property
    def human_transactions(self) -> pd.DataFrame:
        human_addrs = set(self.labels[self.labels["label"] == "human"]["address"])
        mask = self.transactions["sender"].isin(human_addrs) | self.transactions[
            "receiver"
        ].isin(human_addrs)
        return self.transactions[mask]

    @property
    def stats(self) -> dict:
        return {
            "total_transactions": len(self.transactions),
            "total_labeled_addresses": len(self.labels),
            "agent_addresses": len(self.labels[self.labels["label"] == "agent"]),
            "human_addresses": len(self.labels[self.labels["label"] == "human"]),
            "unknown_addresses": len(self.labels[self.labels["label"] == "unknown"]),
            "agent_transactions": len(self.agent_transactions),
            "human_transactions": len(self.human_transactions),
            "date_range": (
                str(self.transactions["timestamp"].min()),
                str(self.transactions["timestamp"].max()),
            ),
        }

    def save(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        self.transactions.to_parquet(directory / "transactions.parquet", index=False)
        self.labels.to_parquet(directory / "labels.parquet", index=False)
        logger.info(f"Saved dataset to {directory}: {self.stats}")

    @classmethod
    def load(cls, directory: Path) -> TransactionDataset:
        transactions = pd.read_parquet(directory / "transactions.parquet")
        labels = pd.read_parquet(directory / "labels.parquet")
        return cls(transactions=transactions, labels=labels)


class DuneClient:
    """Minimal Dune Analytics API client for running saved queries.

    Requires DUNE_API_KEY environment variable or explicit key.
    Uses the Dune API v1 execution endpoint.
    """

    BASE_URL = "https://api.dune.com/api/v1"

    def __init__(self, api_key: str | None = None):
        import os

        self.api_key = api_key or os.environ.get("DUNE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Dune API key required. Set DUNE_API_KEY env var or pass api_key parameter."
            )

    async def execute_query(self, query_id: int, parameters: dict | None = None) -> pd.DataFrame:
        """Execute a saved Dune query and return results as DataFrame."""
        import httpx

        headers = {"X-Dune-API-Key": self.api_key}

        async with httpx.AsyncClient(timeout=300) as client:
            # Start execution
            exec_payload = {}
            if parameters:
                exec_payload["query_parameters"] = parameters

            resp = await client.post(
                f"{self.BASE_URL}/query/{query_id}/execute",
                headers=headers,
                json=exec_payload,
            )
            resp.raise_for_status()
            execution_id = resp.json()["execution_id"]
            logger.info(f"Dune execution started: {execution_id}")

            # Poll for completion
            import asyncio

            while True:
                status_resp = await client.get(
                    f"{self.BASE_URL}/execution/{execution_id}/status",
                    headers=headers,
                )
                status_resp.raise_for_status()
                state = status_resp.json()["state"]

                if state == "QUERY_STATE_COMPLETED":
                    break
                elif state == "QUERY_STATE_FAILED":
                    raise RuntimeError(f"Dune query failed: {status_resp.json()}")

                logger.info(f"Query state: {state}, waiting...")
                await asyncio.sleep(5)

            # Fetch results
            results_resp = await client.get(
                f"{self.BASE_URL}/execution/{execution_id}/results",
                headers=headers,
            )
            results_resp.raise_for_status()
            rows = results_resp.json()["result"]["rows"]

        df = pd.DataFrame(rows)
        logger.info(f"Dune query returned {len(df)} rows")
        return df

    async def run_sql(self, sql: str) -> pd.DataFrame:
        """Execute raw SQL on Dune (requires Plus plan)."""
        import httpx

        headers = {"X-Dune-API-Key": self.api_key}

        async with httpx.AsyncClient(timeout=300) as client:
            resp = await client.post(
                f"{self.BASE_URL}/query/execute/sql",
                headers=headers,
                json={"query_sql": sql},
            )
            resp.raise_for_status()
            execution_id = resp.json()["execution_id"]

            import asyncio

            while True:
                status_resp = await client.get(
                    f"{self.BASE_URL}/execution/{execution_id}/status",
                    headers=headers,
                )
                status_resp.raise_for_status()
                state = status_resp.json()["state"]

                if state == "QUERY_STATE_COMPLETED":
                    break
                elif state == "QUERY_STATE_FAILED":
                    raise RuntimeError(f"Dune query failed: {status_resp.json()}")
                await asyncio.sleep(5)

            results_resp = await client.get(
                f"{self.BASE_URL}/execution/{execution_id}/results",
                headers=headers,
            )
            results_resp.raise_for_status()
            rows = results_resp.json()["result"]["rows"]

        return pd.DataFrame(rows)
