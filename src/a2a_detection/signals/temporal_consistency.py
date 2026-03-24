"""Signal 4: Temporal Consistency.

Detects inhuman timing patterns that reveal automated/agent behavior.
Humans have circadian rhythms, reaction time limits, and cognitive
constraints that produce characteristic temporal signatures.
Agents violate these constraints.

Components:
    - Circadian violation (35%): Activity during human sleep hours
    - Inter-transaction timing (35%): Sub-second or perfectly periodic timing
    - Burst detection (30%): Transaction bursts exceeding human capability

Score: 0.0 (human-like timing) to 1.0 (machine-like timing)
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class TemporalConsistencySignal:
    """Temporal Consistency signal scorer for detecting automated timing."""

    W_CIRCADIAN = 0.35
    W_TIMING = 0.35
    W_BURST = 0.30

    # Human baseline parameters
    HUMAN_MIN_GAP_SECONDS = 2.0  # fastest human transaction gap
    HUMAN_MAX_TX_PER_HOUR = 30  # upper bound for human activity
    SLEEP_HOURS = (2, 6)  # UTC hours with lowest global human activity

    def score_address(self, address: str, transactions: pd.DataFrame) -> float:
        """Score an address based on its temporal transaction patterns."""
        addr_txns = transactions[
            (transactions["sender"] == address) | (transactions["receiver"] == address)
        ].copy()

        if len(addr_txns) < 5:
            return 0.0

        try:
            addr_txns["ts"] = pd.to_datetime(addr_txns["timestamp"])
        except Exception:
            return 0.0

        addr_txns = addr_txns.sort_values("ts")

        circadian = self._circadian_violation(addr_txns)
        timing = self._inter_transaction_timing(addr_txns)
        burst = self._burst_detection(addr_txns)

        return np.clip(
            self.W_CIRCADIAN * circadian
            + self.W_TIMING * timing
            + self.W_BURST * burst,
            0,
            1,
        )

    def _circadian_violation(self, txns: pd.DataFrame) -> float:
        """Detect activity that violates human circadian patterns.

        Humans exhibit reduced activity during sleep hours (roughly 02:00-06:00
        local time). Agents show uniform 24/7 activity distribution.
        Blockchain timestamps are UTC, so we look at global sleep patterns.
        """
        hours = txns["ts"].dt.hour
        total = len(hours)

        if total == 0:
            return 0.0

        # Proportion of transactions during global low-activity hours
        sleep_start, sleep_end = self.SLEEP_HOURS
        sleep_txns = hours.between(sleep_start, sleep_end).sum()
        sleep_ratio = sleep_txns / total

        # Expected ratio for uniform distribution over 4 hours: 4/24 = 0.167
        # Humans: much lower (near 0.02-0.05)
        # Agents: near 0.167 (uniform)
        expected_uniform = (sleep_end - sleep_start) / 24

        if sleep_ratio > expected_uniform * 0.8:
            # Activity is near-uniform across hours — agent-like
            return min(1.0, sleep_ratio / expected_uniform)
        return 0.0

    def _inter_transaction_timing(self, txns: pd.DataFrame) -> float:
        """Detect machine-speed or perfectly periodic transaction timing.

        Humans have variable reaction times (seconds to minutes).
        Agents can transact in milliseconds with machine precision.
        """
        if len(txns) < 3:
            return 0.0

        timestamps = txns["ts"].values
        gaps = np.diff(timestamps).astype("timedelta64[ms]").astype(float) / 1000  # seconds

        if len(gaps) == 0:
            return 0.0

        scores = []

        # Component 1: Sub-human-speed gaps
        fast_ratio = np.mean(gaps < self.HUMAN_MIN_GAP_SECONDS)
        scores.append(fast_ratio)

        # Component 2: Periodicity (low coefficient of variation in gaps)
        if np.mean(gaps) > 0:
            cv = np.std(gaps) / np.mean(gaps)
            # Very low CV = highly periodic = programmatic
            if cv < 0.1:
                scores.append(1.0)
            elif cv < 0.3:
                scores.append((0.3 - cv) / 0.2)
            else:
                scores.append(0.0)
        else:
            scores.append(0.0)

        return np.mean(scores)

    def _burst_detection(self, txns: pd.DataFrame) -> float:
        """Detect transaction bursts exceeding human capability.

        Count maximum transactions per rolling hour window.
        Humans rarely exceed 30 tx/hour; agents can do thousands.
        """
        if len(txns) < 5:
            return 0.0

        txns_hourly = txns.set_index("ts").resample("1h").size()

        if len(txns_hourly) == 0:
            return 0.0

        max_hourly = txns_hourly.max()

        if max_hourly > self.HUMAN_MAX_TX_PER_HOUR:
            # Scale: 30-100 = moderate, 100+ = extreme
            return np.clip((max_hourly - self.HUMAN_MAX_TX_PER_HOUR) / 100, 0, 1)
        return 0.0
