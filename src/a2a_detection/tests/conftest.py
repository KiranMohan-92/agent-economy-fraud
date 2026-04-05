"""Shared test fixtures for A2A detection signal tests.

Fixtures provide minimal transaction DataFrames that represent
clear agent-like or human-like behavioral patterns.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def _make_txns(rows: list[dict]) -> pd.DataFrame:
    """Build a transaction DataFrame from a list of row dicts."""
    df = pd.DataFrame(rows)
    df["sender"] = df["sender"].str.lower()
    df["receiver"] = df["receiver"].str.lower()
    return df


@pytest.fixture
def agent_addr() -> str:
    return "0xagent000000000000000000000000000000000001"


@pytest.fixture
def human_addr() -> str:
    return "0xhuman000000000000000000000000000000000001"


@pytest.fixture
def relay_agent_txns(agent_addr) -> pd.DataFrame:
    """Agent that receives and immediately re-forwards value (relay pattern).

    Rapid consecutive send/receive within seconds — a human can't do this
    because the physical reaction time and network latency floor is ~2s.
    """
    base_time = pd.Timestamp("2026-01-01T12:00:00Z")
    rows = []
    for i in range(10):
        # Receive value
        rows.append({
            "sender": f"0xsource{i:04x}",
            "receiver": agent_addr,
            "amount_usdc": 50.0,
            "timestamp": base_time + pd.Timedelta(seconds=i * 5),
        })
        # Immediately forward (within 5 seconds of receiving)
        rows.append({
            "sender": agent_addr,
            "receiver": f"0xdest{i:04x}",
            "amount_usdc": 49.9,
            "timestamp": base_time + pd.Timedelta(seconds=i * 5 + 3),
        })
    return _make_txns(rows)


@pytest.fixture
def human_txns(human_addr) -> pd.DataFrame:
    """Human with irregular, widely-spaced, purposeful transactions.

    Transactions happen once or twice a day with human-scale gaps (hours).
    Amounts are round numbers; counterparties are all distinct.
    """
    base_time = pd.Timestamp("2026-01-01T10:00:00Z")
    rows = []
    for i in range(8):
        rows.append({
            "sender": human_addr,
            "receiver": f"0xmerchant{i:04x}",
            "amount_usdc": float(10 * (i + 1)),  # round numbers: 10, 20, 30, ...
            "timestamp": base_time + pd.Timedelta(hours=i * 24 + i),
        })
    return _make_txns(rows)


@pytest.fixture
def burst_agent_txns(agent_addr) -> pd.DataFrame:
    """Agent that executes 200 transactions within a single hour.

    Burst rate of 200/h far exceeds the human ceiling of 30/h.
    """
    base_time = pd.Timestamp("2026-01-15T03:00:00Z")  # 3 AM UTC (sleep hours)
    rows = []
    for i in range(200):
        rows.append({
            "sender": agent_addr,
            "receiver": f"0xtarget{i:04x}",
            "amount_usdc": 1.00,
            "timestamp": base_time + pd.Timedelta(seconds=i * 17),  # ~200 per hour
        })
    return _make_txns(rows)


@pytest.fixture
def circular_flow_txns(agent_addr) -> pd.DataFrame:
    """Agent involved in circular value flows (A→B→C→A).

    Every counterparty that receives funds also sends funds back —
    a wash-trading pattern that serves no rational economic purpose.
    """
    partners = [f"0xpartner{i:04x}" for i in range(5)]
    base_time = pd.Timestamp("2026-01-01T08:00:00Z")
    rows = []
    for i, partner in enumerate(partners):
        # agent sends to partner
        rows.append({
            "sender": agent_addr,
            "receiver": partner,
            "amount_usdc": 100.0,
            "timestamp": base_time + pd.Timedelta(minutes=i * 2),
        })
        # partner sends back (bidirectional = circular)
        rows.append({
            "sender": partner,
            "receiver": agent_addr,
            "amount_usdc": 99.0,
            "timestamp": base_time + pd.Timedelta(minutes=i * 2 + 1),
        })
    return _make_txns(rows)


@pytest.fixture
def multichain_txns(agent_addr) -> pd.DataFrame:
    """Agent active on 3 chains within seconds of each other.

    Physical impossibility: a single human cannot submit transactions
    on Base, Ethereum, and Arbitrum within 10-second windows.
    """
    base_time = pd.Timestamp("2026-01-01T10:00:00Z")
    rows = []
    for i in range(5):
        t = base_time + pd.Timedelta(minutes=i * 10)
        for chain, delta in [("base", 0), ("ethereum", 5), ("arbitrum", 9)]:
            rows.append({
                "sender": agent_addr,
                "receiver": f"0xdest{chain}{i:04x}",
                "amount_usdc": 25.0,
                "timestamp": t + pd.Timedelta(seconds=delta),
                "chain": chain,
            })
    return _make_txns(rows)
