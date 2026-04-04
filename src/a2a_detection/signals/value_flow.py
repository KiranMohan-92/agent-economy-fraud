"""Signal 3: Value Flow.

Detects suspicious value flow patterns including wash trading,
layering (rapid movement through multiple accounts), and
rapid relay behavior.

On-chain, this signal is particularly powerful because the full
transaction graph is visible — unlike traditional banking where
inter-bank flows are opaque.

Components:
    - Flow velocity (50%): Speed of value movement through an address
    - Layering depth (50%): Number of hops value takes before settling

Score: 0.0 (normal value flow) to 1.0 (suspicious flow pattern)

Sub-signal history:
    v0.1: _net_flow_imbalance only (detected wash trading, missed drain/spray)
    v0.2: Added asymmetric drain/spray detection; F1 improved 0.11 → 0.31
    v0.3: Removed _net_flow_imbalance entirely (2026-04-04).
          On-chain validation showed it fires MORE on humans than agents:
          most human counterparties appear receive-only (net_ratio=1.0)
          because they transact once with an agent then never again.
          This inverse discrimination made it the largest single source
          of false positives (drove 35%+ of FP addresses to score > 0.4).
          _flow_velocity discriminates 14/18 agents vs 0/7 humans and
          is retained. Weight redistributed equally to velocity+layering.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class ValueFlowSignal:
    """Value Flow signal scorer for detecting wash trading and layering."""

    W_VELOCITY = 0.50
    W_LAYERING = 0.50

    def score_address(self, address: str, transactions: pd.DataFrame) -> float:
        """Score an address based on its value flow patterns."""
        addr_txns = transactions[
            (transactions["sender"] == address) | (transactions["receiver"] == address)
        ]

        if len(addr_txns) < 3:
            return 0.0

        velocity = self._flow_velocity(address, addr_txns)
        layering = self._layering_indicator(address, addr_txns, transactions)

        return np.clip(
            self.W_VELOCITY * velocity
            + self.W_LAYERING * layering,
            0,
            1,
        )

    def _net_flow_imbalance(self, address: str, txns: pd.DataFrame) -> float:
        """Detect abnormal flow directionality (both wash trading AND drain/spray).

        Suspicious patterns detected:
        1. Near-zero net flow (wash trading): balanced in/out with high volume
        2. Extreme one-directional flow (drain/spray): nearly all outbound OR
           all inbound — agents often spray funds to many addresses or drain
           from one source. Humans have a natural mix of income and spending.

        The score is U-shaped: high at both extremes of net_ratio (0.0 and 1.0),
        low in the normal human range (0.2-0.8).
        """
        inflow = txns[txns["receiver"] == address]["amount_usdc"].sum()
        outflow = txns[txns["sender"] == address]["amount_usdc"].sum()
        gross = inflow + outflow

        if gross == 0:
            return 0.0

        net = abs(inflow - outflow)
        net_ratio = net / gross  # 0 = perfectly balanced, 1 = one-directional

        # U-shaped scoring: suspicious at BOTH extremes
        # Low end (wash trading): net_ratio < 0.1 with meaningful volume
        if net_ratio < 0.1 and gross > 10:
            return min(1.0, (0.1 - net_ratio) * 10)

        # High end (drain/spray): net_ratio > 0.9 means extreme asymmetry
        # Agents that only send (or only receive) score high
        if net_ratio > 0.9:
            return min(1.0, (net_ratio - 0.9) * 10)

        # Moderately asymmetric (0.8-0.9): mild suspicion
        if net_ratio > 0.8:
            return (net_ratio - 0.8) * 5  # scales 0.0 to 0.5

        # Normal human range (0.1-0.8): no signal
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
