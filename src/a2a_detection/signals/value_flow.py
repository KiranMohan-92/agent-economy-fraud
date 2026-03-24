"""Signal 3: Value Flow.

Detects suspicious value flow patterns including wash trading,
layering (rapid movement through multiple accounts), and
value extraction schemes.

On-chain, this signal is particularly powerful because the full
transaction graph is visible — unlike traditional banking where
inter-bank flows are opaque.

Components:
    - Net flow imbalance (40%): Ratio of inflow to outflow per address
    - Flow velocity (30%): Speed of value movement through an address
    - Layering depth (30%): Number of hops value takes before settling

Score: 0.0 (normal value flow) to 1.0 (suspicious flow pattern)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class ValueFlowSignal:
    """Value Flow signal scorer for detecting wash trading and layering."""

    W_IMBALANCE = 0.40
    W_VELOCITY = 0.30
    W_LAYERING = 0.30

    def score_address(self, address: str, transactions: pd.DataFrame) -> float:
        """Score an address based on its value flow patterns."""
        addr_txns = transactions[
            (transactions["sender"] == address) | (transactions["receiver"] == address)
        ]

        if len(addr_txns) < 3:
            return 0.0

        imbalance = self._net_flow_imbalance(address, addr_txns)
        velocity = self._flow_velocity(address, addr_txns)
        layering = self._layering_indicator(address, addr_txns, transactions)

        return np.clip(
            self.W_IMBALANCE * imbalance
            + self.W_VELOCITY * velocity
            + self.W_LAYERING * layering,
            0,
            1,
        )

    def _net_flow_imbalance(self, address: str, txns: pd.DataFrame) -> float:
        """Detect near-zero net flow (wash trading indicator).

        Wash trading produces roughly equal inflows and outflows.
        A net flow near zero with high gross volume is suspicious.
        Humans typically have asymmetric flows (income vs spending).
        """
        inflow = txns[txns["receiver"] == address]["amount_usdc"].sum()
        outflow = txns[txns["sender"] == address]["amount_usdc"].sum()
        gross = inflow + outflow

        if gross == 0:
            return 0.0

        net = abs(inflow - outflow)
        net_ratio = net / gross  # 0 = perfectly balanced, 1 = one-directional

        # Suspicious: very balanced flows (net_ratio < 0.1) with meaningful volume
        if net_ratio < 0.1 and gross > 10:
            return min(1.0, (0.1 - net_ratio) * 10)
        return 0.0

    def _flow_velocity(self, address: str, txns: pd.DataFrame) -> float:
        """Detect rapid value pass-through (relay/layering behavior).

        Agents acting as relays receive and forward value within seconds.
        Measure the time gap between receiving and sending for the same address.
        """
        txns_sorted = txns.sort_values("timestamp")

        received = txns_sorted[txns_sorted["receiver"] == address]
        sent = txns_sorted[txns_sorted["sender"] == address]

        if len(received) == 0 or len(sent) == 0:
            return 0.0

        # Convert timestamps to datetime if needed
        try:
            received_times = pd.to_datetime(received["timestamp"])
            sent_times = pd.to_datetime(sent["timestamp"])
        except Exception:
            return 0.0

        # For each sent transaction, find the nearest prior received transaction
        rapid_forwards = 0
        for send_time in sent_times:
            prior_receives = received_times[received_times <= send_time]
            if len(prior_receives) == 0:
                continue
            gap = (send_time - prior_receives.max()).total_seconds()
            if gap < 60:  # forwarded within 60 seconds
                rapid_forwards += 1

        rapid_ratio = rapid_forwards / len(sent) if len(sent) > 0 else 0.0

        # High rapid-forward ratio = relay behavior
        return np.clip(rapid_ratio * 1.5, 0, 1)

    def _layering_indicator(
        self, address: str, addr_txns: pd.DataFrame, all_txns: pd.DataFrame
    ) -> float:
        """Detect layering — value moving through chains of addresses.

        Check if an address's counterparties also exhibit high-frequency,
        balanced flow patterns (suggesting they're part of a layering chain).
        """
        sent = addr_txns[addr_txns["sender"] == address]
        receivers = sent["receiver"].unique()

        if len(receivers) == 0:
            return 0.0

        # Check each receiver's flow balance
        suspicious_receivers = 0
        for recv in receivers[:20]:  # cap to avoid expensive computation
            recv_txns = all_txns[
                (all_txns["sender"] == recv) | (all_txns["receiver"] == recv)
            ]
            if len(recv_txns) < 3:
                continue

            recv_in = recv_txns[recv_txns["receiver"] == recv]["amount_usdc"].sum()
            recv_out = recv_txns[recv_txns["sender"] == recv]["amount_usdc"].sum()
            recv_gross = recv_in + recv_out

            if recv_gross > 0:
                recv_net_ratio = abs(recv_in - recv_out) / recv_gross
                if recv_net_ratio < 0.15:  # balanced = relay
                    suspicious_receivers += 1

        chain_ratio = suspicious_receivers / len(receivers) if len(receivers) > 0 else 0.0
        return np.clip(chain_ratio * 2, 0, 1)
