"""ERC-8004 Identity Registry client.

Queries the on-chain ERC-8004 (Trustless Agents) Identity Registry to extract
all registered agent addresses. These serve as ground-truth labels for the
agent-vs-human classification task.

Registry contract: 0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
Chains: Ethereum, Base, BNB (same address via CREATE2)
Standard: ERC-721 + URIStorage

Data sources (in priority order):
    1. The Graph subgraphs (github.com/agent0lab/subgraph)
    2. Direct RPC via web3.py
    3. 8004scan.io API (if available)
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import pandas as pd

logger = logging.getLogger(__name__)

# ERC-8004 Identity Registry — same address on all deployed chains (CREATE2)
IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432"
REPUTATION_REGISTRY = "0x8004BAa17C55a88189AE136b182e5fdA19dE9b63"

# The Graph subgraph endpoints (from github.com/agent0lab/subgraph)
SUBGRAPH_URLS = {
    "ethereum": "https://api.thegraph.com/subgraphs/name/agent0lab/erc8004-ethereum",
    "base": "https://api.thegraph.com/subgraphs/name/agent0lab/erc8004-base",
    "bnb": "https://api.thegraph.com/subgraphs/name/agent0lab/erc8004-bnb",
}

# ERC-721 Transfer event signature for direct RPC fallback
TRANSFER_EVENT_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


@dataclass
class AgentRegistration:
    """A single ERC-8004 agent registration."""

    address: str
    token_id: int
    chain: str
    registration_time: str | None = None
    registration_tx: str | None = None
    metadata_uri: str | None = None
    metadata: dict | None = None


@dataclass
class AgentRegistry:
    """Collection of all registered agents across chains."""

    agents: list[AgentRegistration] = field(default_factory=list)

    @property
    def addresses(self) -> set[str]:
        return {a.address.lower() for a in self.agents}

    @property
    def by_chain(self) -> dict[str, list[AgentRegistration]]:
        result: dict[str, list[AgentRegistration]] = {}
        for agent in self.agents:
            result.setdefault(agent.chain, []).append(agent)
        return result

    def to_dataframe(self) -> pd.DataFrame:
        records = [
            {
                "address": a.address.lower(),
                "token_id": a.token_id,
                "chain": a.chain,
                "registration_time": a.registration_time,
                "registration_tx": a.registration_tx,
                "metadata_uri": a.metadata_uri,
            }
            for a in self.agents
        ]
        return pd.DataFrame(records)

    def save(self, path: Path) -> None:
        df = self.to_dataframe()
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, index=False)
        logger.info(f"Saved {len(df)} agent registrations to {path}")

    @classmethod
    def load(cls, path: Path) -> AgentRegistry:
        df = pd.read_parquet(path)
        agents = [
            AgentRegistration(
                address=row["address"],
                token_id=row["token_id"],
                chain=row["chain"],
                registration_time=row.get("registration_time"),
                registration_tx=row.get("registration_tx"),
                metadata_uri=row.get("metadata_uri"),
            )
            for _, row in df.iterrows()
        ]
        return cls(agents=agents)


async def fetch_agents_subgraph(
    chain: str = "base",
    batch_size: int = 1000,
    max_agents: int | None = None,
) -> list[AgentRegistration]:
    """Fetch all ERC-8004 registrations from The Graph subgraph.

    Uses pagination to handle large result sets. The subgraph indexes
    all Transfer events from address(0) on the Identity Registry contract.
    """
    url = SUBGRAPH_URLS.get(chain)
    if not url:
        raise ValueError(f"No subgraph URL for chain '{chain}'. Available: {list(SUBGRAPH_URLS)}")

    agents: list[AgentRegistration] = []
    last_id = ""

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            # GraphQL query with cursor-based pagination
            query = """
            {
                agents(
                    first: %d,
                    where: { id_gt: "%s" },
                    orderBy: id,
                    orderDirection: asc
                ) {
                    id
                    owner
                    tokenId
                    registeredAt
                    registrationTx
                    metadataURI
                }
            }
            """ % (batch_size, last_id)

            response = await client.post(url, json={"query": query})
            response.raise_for_status()
            data = response.json()

            batch = data.get("data", {}).get("agents", [])
            if not batch:
                break

            for item in batch:
                agents.append(
                    AgentRegistration(
                        address=item["owner"],
                        token_id=int(item["tokenId"]),
                        chain=chain,
                        registration_time=item.get("registeredAt"),
                        registration_tx=item.get("registrationTx"),
                        metadata_uri=item.get("metadataURI"),
                    )
                )

            last_id = batch[-1]["id"]
            logger.info(f"[{chain}] Fetched {len(agents)} agents so far...")

            if max_agents and len(agents) >= max_agents:
                agents = agents[:max_agents]
                break

    logger.info(f"[{chain}] Total: {len(agents)} registered agents")
    return agents


async def fetch_agents_rpc(
    rpc_url: str,
    chain: str = "base",
    from_block: int = 0,
) -> list[AgentRegistration]:
    """Fallback: Fetch ERC-8004 registrations via direct RPC eth_getLogs.

    Queries Transfer(address(0), to, tokenId) events on the Identity Registry.
    Use this if The Graph subgraph is unavailable.
    """
    async with httpx.AsyncClient(timeout=60) as client:
        # Zero-padded address(0) for topic[1] (from = address(0) means mint)
        zero_topic = "0x" + ZERO_ADDRESS[2:].zfill(64)

        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getLogs",
            "params": [
                {
                    "address": IDENTITY_REGISTRY,
                    "topics": [TRANSFER_EVENT_TOPIC, zero_topic],
                    "fromBlock": hex(from_block),
                    "toBlock": "latest",
                }
            ],
            "id": 1,
        }

        response = await client.post(rpc_url, json=payload)
        response.raise_for_status()
        result = response.json().get("result", [])

    agents = []
    for log in result:
        # topic[2] = to address (agent owner), topic[3] or data = tokenId
        to_address = "0x" + log["topics"][2][-40:]
        token_id = int(log["topics"][3], 16) if len(log["topics"]) > 3 else 0

        agents.append(
            AgentRegistration(
                address=to_address,
                token_id=token_id,
                chain=chain,
                registration_tx=log.get("transactionHash"),
            )
        )

    logger.info(f"[{chain}] Fetched {len(agents)} agents via RPC")
    return agents


async def fetch_all_agents(chains: list[str] | None = None) -> AgentRegistry:
    """Fetch agent registrations from all specified chains.

    Default chains: base, ethereum, bnb (in order of agent count).
    """
    if chains is None:
        chains = ["base", "ethereum", "bnb"]

    all_agents: list[AgentRegistration] = []
    for chain in chains:
        try:
            agents = await fetch_agents_subgraph(chain)
            all_agents.extend(agents)
        except Exception as e:
            logger.warning(f"Failed to fetch from {chain} subgraph: {e}")

    registry = AgentRegistry(agents=all_agents)
    logger.info(
        f"Total: {len(registry.agents)} agents across {len(chains)} chains, "
        f"{len(registry.addresses)} unique addresses"
    )
    return registry
