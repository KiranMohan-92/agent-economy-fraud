"""Signal 5: Cross-Platform Correlation.

Detects coordinated activity across multiple blockchain networks.
Agents can operate on Base, Ethereum, BNB, and Solana simultaneously,
which is physically impossible for a single human without automation.

This signal has the lowest weight (0.10) because cross-chain data
is harder to obtain and correlate, but it catches attacks that
single-chain signals miss entirely (e.g., cross-platform identity fraud).

Components:
    - Multi-chain presence (50%): Same address active on multiple chains
    - Temporal cross-chain correlation (50%): Synchronized activity across chains

Score: 0.0 (single-chain, human-like) to 1.0 (multi-chain coordinated)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class CrossPlatformSignal:
    """Cross-Platform Correlation signal scorer.

    Note: This signal requires multi-chain data. If only single-chain
    data is available, the score defaults to 0.0 (insufficient data).
    """

    W_PRESENCE = 0.50
    W_TEMPORAL = 0.50

    def score_address(
        self,
        address: str,
        transactions: pd.DataFrame,
        chain_column: str = "chain",
    ) -> float:
        """Score an address based on cross-platform activity patterns.

        Args:
            address: Wallet address to evaluate.
            transactions: DataFrame with a 'chain' column indicating source network.
            chain_column: Name of the chain identifier column.
        """
        if chain_column not in transactions.columns:
            return 0.0  # single-chain data, cannot evaluate

        addr_txns = transactions[
            (transactions["sender"] == address) | (transactions["receiver"] == address)
        ]

        if len(addr_txns) < 3:
            return 0.0

        presence = self._multi_chain_presence(addr_txns, chain_column)
        temporal = self._cross_chain_temporal_correlation(addr_txns, chain_column)

        return np.clip(
            self.W_PRESENCE * presence + self.W_TEMPORAL * temporal,
            0,
            1,
        )

    def _multi_chain_presence(self, txns: pd.DataFrame, chain_col: str) -> float:
        """Detect activity across multiple chains.

        Most human users operate on 1-2 chains. Active presence on 3+
        chains simultaneously suggests automation.
        """
        chains = txns[chain_col].nunique()

        if chains <= 1:
            return 0.0
        elif chains == 2:
            return 0.3
        elif chains == 3:
            return 0.7
        else:
            return 1.0

    def _cross_chain_temporal_correlation(
        self, txns: pd.DataFrame, chain_col: str
    ) -> float:
        """Detect synchronized transactions across chains.

        If an address transacts on Base and Ethereum within seconds of each
        other, this is physically impossible without automation.
        """
        chains = txns[chain_col].unique()
        if len(chains) < 2:
            return 0.0

        try:
            txns = txns.copy()
            txns["ts"] = pd.to_datetime(txns["timestamp"])
        except Exception:
            return 0.0

        # Compare timestamps across chain pairs
        synchronized_pairs = 0
        total_pairs = 0

        chain_list = list(chains)
        for i, chain_a in enumerate(chain_list):
            for chain_b in chain_list[i + 1 :]:
                times_a = txns[txns[chain_col] == chain_a]["ts"].values
                times_b = txns[txns[chain_col] == chain_b]["ts"].values

                if len(times_a) == 0 or len(times_b) == 0:
                    continue

                total_pairs += 1

                # Check for near-simultaneous transactions (within 30 seconds)
                for ta in times_a:
                    gaps = np.abs((times_b - ta).astype("timedelta64[s]").astype(float))
                    if np.any(gaps < 30):
                        synchronized_pairs += 1
                        break

        if total_pairs == 0:
            return 0.0

        return synchronized_pairs / total_pairs
