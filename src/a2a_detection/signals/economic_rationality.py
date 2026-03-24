"""Signal 1: Economic Rationality.

Detects transactions that deviate from rational economic behavior.
Agents executing automated strategies may exhibit patterns that no
profit-maximizing human would: circular flows, irrational pricing,
zero-utility transfers, or extreme value concentration.

Components (from Phase 3 specification):
    - Utility deviation (40%): Does the transaction serve an economic purpose?
    - Circular flow detection (30%): Is value cycling back to origin?
    - Purpose deviation (20%): Does the transaction match expected category behavior?
    - Value concentration (10%): Is value anomalously concentrated in few counterparties?

Score: 0.0 (fully rational/human-like) to 1.0 (maximally irrational/agent-like)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class EconomicRationalitySignal:
    """Economic Rationality signal scorer for on-chain transactions."""

    # Component weights from Phase 4 implementation guidance
    W_UTILITY = 0.40
    W_CIRCULARITY = 0.30
    W_PURPOSE = 0.20
    W_CONCENTRATION = 0.10

    def score_address(self, address: str, transactions: pd.DataFrame) -> float:
        """Score an address based on its transaction history.

        Args:
            address: The wallet address to evaluate (lowercase hex).
            transactions: DataFrame with columns [sender, receiver, amount_usdc, timestamp].

        Returns:
            Score in [0, 1] where higher = more agent-like.
        """
        addr_txns = transactions[
            (transactions["sender"] == address) | (transactions["receiver"] == address)
        ]

        if len(addr_txns) < 3:
            return 0.0  # insufficient data

        utility = self._utility_deviation(address, addr_txns)
        circularity = self._circular_flow_score(address, addr_txns)
        purpose = self._purpose_deviation(address, addr_txns)
        concentration = self._value_concentration(address, addr_txns)

        return (
            self.W_UTILITY * utility
            + self.W_CIRCULARITY * circularity
            + self.W_PURPOSE * purpose
            + self.W_CONCENTRATION * concentration
        )

    def _utility_deviation(self, address: str, txns: pd.DataFrame) -> float:
        """Detect transactions with no apparent economic utility.

        Human transactions typically have clear utility (goods, services, savings).
        Agent transactions may include zero-value probes, dust amounts, or
        transfers that serve no rational economic purpose.
        """
        sent = txns[txns["sender"] == address]
        if len(sent) == 0:
            return 0.0

        amounts = sent["amount_usdc"].values

        # Indicator 1: High proportion of micro-transactions (<$0.01)
        micro_ratio = np.mean(amounts < 0.01) if len(amounts) > 0 else 0.0

        # Indicator 2: Extremely uniform amounts (programmatic behavior)
        cv = np.std(amounts) / np.mean(amounts) if np.mean(amounts) > 0 else 0.0
        uniformity_score = max(0, 1 - cv)  # low CV = high uniformity = suspicious

        # Indicator 3: Round-number avoidance (humans prefer round numbers)
        round_count = sum(1 for a in amounts if a > 0.01 and (a * 100) % 100 == 0)
        round_ratio = round_count / len(amounts) if len(amounts) > 0 else 0.5
        # Humans have higher round_ratio; low ratio = agent-like
        round_score = max(0, 1 - round_ratio * 2)

        return np.clip(0.4 * micro_ratio + 0.35 * uniformity_score + 0.25 * round_score, 0, 1)

    def _circular_flow_score(self, address: str, txns: pd.DataFrame) -> float:
        """Detect circular value flows (A→B→C→A patterns).

        Agents can create wash-trading loops that cycle value through multiple
        addresses before returning it to the origin. Humans rarely do this
        because it requires coordination and yields no obvious benefit.
        """
        sent_to = set(txns[txns["sender"] == address]["receiver"].unique())
        received_from = set(txns[txns["receiver"] == address]["sender"].unique())

        if not sent_to or not received_from:
            return 0.0

        # Direct circularity: addresses that both send to and receive from this address
        bidirectional = sent_to & received_from
        total_counterparties = sent_to | received_from

        circularity_ratio = len(bidirectional) / len(total_counterparties) if total_counterparties else 0.0

        # Scale: some bidirectional relationships are normal (e.g., employer/vendor)
        # Flag when ratio is unusually high
        return np.clip(circularity_ratio * 2, 0, 1)

    def _purpose_deviation(self, address: str, txns: pd.DataFrame) -> float:
        """Detect deviation from expected transaction purpose patterns.

        On-chain, we approximate purpose by counterparty diversity and
        interaction patterns. Humans typically interact with a mix of
        known contracts (DEXs, lending) and peer addresses.
        """
        sent = txns[txns["sender"] == address]
        if len(sent) < 5:
            return 0.0

        # Diversity of counterparties relative to transaction count
        n_counterparties = sent["receiver"].nunique()
        n_transactions = len(sent)

        # Very low ratio = repeated interactions with same addresses (could be normal)
        # Very high ratio = each tx goes to a new address (agent exploration pattern)
        diversity_ratio = n_counterparties / n_transactions

        # Agent-like: very high diversity (spray pattern) or very low (bot loop)
        if diversity_ratio > 0.8:
            return min(1.0, (diversity_ratio - 0.8) * 5)  # spray pattern
        elif diversity_ratio < 0.1:
            return min(1.0, (0.1 - diversity_ratio) * 10)  # loop pattern
        return 0.0

    def _value_concentration(self, address: str, txns: pd.DataFrame) -> float:
        """Detect anomalous value concentration (Gini coefficient of flows).

        Agents may concentrate nearly all value in a single counterparty
        (task-focused) or distribute perfectly evenly (programmatic splitting).
        Humans typically have moderate concentration.
        """
        sent = txns[txns["sender"] == address].groupby("receiver")["amount_usdc"].sum()
        if len(sent) < 2:
            return 0.0

        values = np.sort(sent.values)
        n = len(values)
        index = np.arange(1, n + 1)
        gini = (2 * np.sum(index * values) - (n + 1) * np.sum(values)) / (n * np.sum(values))

        # Extreme Gini (very high or very low) is suspicious
        # Normal human range: 0.3-0.7
        if gini > 0.9:
            return (gini - 0.9) * 10  # extreme concentration
        elif gini < 0.1:
            return (0.1 - gini) * 10  # extreme uniformity
        return 0.0
