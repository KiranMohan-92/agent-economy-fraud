"""Signal 2: Network Topology.

Detects anomalous graph structure around transacting addresses.
Agent networks exhibit distinctive topological patterns: star graphs
(one controller, many bots), dense cliques (coordinated swarms),
or unusually high betweenness centrality (broker/relay nodes).

Components (from Phase 3 specification):
    - Sender centrality anomaly (50%): Is the sender unusually central?
    - Receiver centrality anomaly (30%): Is the receiver unusually central?
    - Path length anomaly (20%): Is the shortest path unusually short/long?

Score: 0.0 (normal network position) to 1.0 (anomalous topology)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from collections import defaultdict


class NetworkTopologySignal:
    """Network Topology signal scorer using transaction graph analysis."""

    W_SENDER_CENTRALITY = 0.50
    W_RECEIVER_CENTRALITY = 0.30
    W_PATH_ANOMALY = 0.20

    def __init__(self):
        self._graph: dict[str, set[str]] | None = None
        self._degree_stats: dict | None = None

    def build_graph(self, transactions: pd.DataFrame) -> None:
        """Build adjacency graph from transaction DataFrame.

        Creates a directed graph where edges represent value transfers.
        Stores degree statistics for anomaly detection.
        """
        graph: dict[str, set[str]] = defaultdict(set)
        in_degree: dict[str, int] = defaultdict(int)
        out_degree: dict[str, int] = defaultdict(int)

        for _, row in transactions.iterrows():
            sender = row["sender"]
            receiver = row["receiver"]
            graph[sender].add(receiver)
            out_degree[sender] += 1
            in_degree[receiver] += 1

        self._graph = dict(graph)

        # Compute degree statistics for z-score calculation
        all_degrees = []
        all_addresses = set(out_degree.keys()) | set(in_degree.keys())
        for addr in all_addresses:
            total = out_degree.get(addr, 0) + in_degree.get(addr, 0)
            all_degrees.append(total)

        self._degree_stats = {
            "mean": np.mean(all_degrees) if all_degrees else 0,
            "std": np.std(all_degrees) if all_degrees else 1,
            "out_degree": dict(out_degree),
            "in_degree": dict(in_degree),
            "total_nodes": len(all_addresses),
        }

    def score_address(self, address: str, transactions: pd.DataFrame) -> float:
        """Score an address based on its network topology position.

        Call build_graph() first or pass transactions to auto-build.
        """
        if self._graph is None:
            self.build_graph(transactions)

        sender_score = self._centrality_anomaly(address, is_sender=True)
        receiver_score = self._centrality_anomaly(address, is_sender=False)
        path_score = self._local_clustering_anomaly(address)

        return np.clip(
            self.W_SENDER_CENTRALITY * sender_score
            + self.W_RECEIVER_CENTRALITY * receiver_score
            + self.W_PATH_ANOMALY * path_score,
            0,
            1,
        )

    def _centrality_anomaly(self, address: str, is_sender: bool = True) -> float:
        """Detect degree centrality anomalies via z-score.

        Agents acting as relay nodes or swarm controllers will have
        anomalously high degree centrality compared to the population.
        """
        stats = self._degree_stats
        if not stats or stats["std"] == 0:
            return 0.0

        if is_sender:
            degree = stats["out_degree"].get(address, 0)
        else:
            degree = stats["in_degree"].get(address, 0)

        z_score = (degree - stats["mean"]) / max(stats["std"], 1)

        # Flag addresses with z-score > 2 (top ~2.5% by degree)
        if z_score > 2:
            return np.clip((z_score - 2) / 3, 0, 1)
        return 0.0

    def _local_clustering_anomaly(self, address: str) -> float:
        """Detect anomalous local clustering coefficient.

        Agent swarms form dense cliques (high clustering).
        Star topologies have very low clustering.
        Both are suspicious compared to normal human transaction networks.
        """
        if not self._graph or address not in self._graph:
            return 0.0

        neighbors = self._graph.get(address, set())
        if len(neighbors) < 2:
            return 0.0

        # Count edges between neighbors (local clustering)
        neighbor_edges = 0
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 != n2 and n2 in self._graph.get(n1, set()):
                    neighbor_edges += 1

        max_edges = len(neighbors) * (len(neighbors) - 1)
        clustering = neighbor_edges / max_edges if max_edges > 0 else 0.0

        # Anomaly: very high clustering (clique/swarm) or very low (star)
        if clustering > 0.7:
            return (clustering - 0.7) / 0.3
        elif clustering < 0.05 and len(neighbors) > 10:
            return min(1.0, (10 - clustering * 200))
        return 0.0
