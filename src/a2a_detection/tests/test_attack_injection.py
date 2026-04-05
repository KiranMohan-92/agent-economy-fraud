"""Unit tests for the attack pattern injector (Phase 6, Plan 06-01).

Tests verify:
1. Each injector produces transactions with the correct behavioral signatures.
2. Injected addresses never collide with a sample of real addresses.
3. Total injection rate is ≤10% of real transaction volume.
4. All 8 attack chains are injectable.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import numpy as np
from datetime import timezone

from a2a_detection.scripts.inject_attacks import (
    inject_chain1_enumeration,
    inject_chain2_history_extraction,
    inject_chain3_async_flooding,
    inject_chain4_agent_army,
    inject_chain5_cross_platform_identity,
    inject_chain6_behavioral_mimicry,
    inject_chain7_swarm_intelligence,
    inject_chain8_market_manipulation,
    inject_all_chains,
    INJECTED_ADDR_PREFIX,
    CHAIN_DIFFICULTIES,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def rng():
    return np.random.default_rng(42)


@pytest.fixture
def base_time():
    return pd.Timestamp("2025-06-15 12:00:00", tz="UTC")


@pytest.fixture
def minimal_real_df():
    """Minimal real-transaction DataFrame for integration tests."""
    n = 200
    rng = np.random.default_rng(0)
    addrs = [f"0xreal{i:036x}" for i in range(n)]
    return pd.DataFrame({
        "tx_hash": [f"0xhash{i:062x}" for i in range(n)],
        "block_number": rng.integers(24_000_000, 28_000_000, size=n),
        "timestamp": pd.date_range("2025-01-01", periods=n, freq="10min", tz="UTC"),
        "sender": addrs,
        "receiver": [f"0xrealtarget{i:030x}" for i in range(n)],
        "amount_usdc": rng.uniform(0.01, 100.0, size=n),
        "token_contract": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
        "direction": "outbound",
    })


# ---------------------------------------------------------------------------
# Per-chain behavioral signature tests
# ---------------------------------------------------------------------------

def test_chain1_produces_dust_probes_to_many_targets(rng, base_time):
    result = inject_chain1_enumeration(rng, base_time, "test_inst", n_probes=20)
    df = result.transactions
    assert len(df) == 20
    # All transactions from one attacker address
    assert df["sender"].nunique() == 1
    # Many different targets (simulates enumeration)
    assert df["receiver"].nunique() == 20
    # Dust amounts (< $0.01 each)
    assert (df["amount_usdc"] < 0.011).all()
    # All within 60 seconds
    span = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    assert span <= 60.0


def test_chain2_repeated_edge_to_same_target(rng, base_time):
    result = inject_chain2_history_extraction(rng, base_time, "test_inst", n_reads=15)
    df = result.transactions
    assert len(df) == 15
    # One attacker → one target (bulk repeated access)
    assert df["sender"].nunique() == 1
    assert df["receiver"].nunique() == 1
    # Within 2-minute window
    span = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    assert span <= 120.0


def test_chain3_machine_speed_flooding(rng, base_time):
    result = inject_chain3_async_flooding(rng, base_time, "test_inst", n_flood_txns=100)
    df = result.transactions
    assert len(df) == 100
    # Machine-speed: extrapolated velocity >> human max
    span_s = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    velocity_per_hour = 3600.0 / (span_s / len(df))
    assert velocity_per_hour > 1000, f"Expected >1000/hr, got {velocity_per_hour:.0f}"


def test_chain4_correlated_agent_cluster(rng, base_time):
    result = inject_chain4_agent_army(rng, base_time, "test_inst", n_agents=10, txns_per_agent=5)
    df = result.transactions
    assert len(df) == 50  # 10 × 5
    # Multiple agents
    assert df["sender"].nunique() == 10
    # All to same sink
    assert df["receiver"].nunique() == 1
    # All agents activate within 90-second window
    per_agent_first_tx = df.groupby("sender")["timestamp"].min()
    activation_span = (per_agent_first_tx.max() - per_agent_first_tx.min()).total_seconds()
    assert activation_span <= 90.0


def test_chain5_near_zero_cost_multi_hop(rng, base_time):
    result = inject_chain5_cross_platform_identity(rng, base_time, "test_inst")
    df = result.transactions
    # Near-zero amounts (below human cognitive cost threshold)
    assert (df["amount_usdc"] < 0.015).all()
    # Multi-hop: many different targets
    assert df["receiver"].nunique() >= 5


def test_chain6_too_perfect_uniformity(rng, base_time):
    result = inject_chain6_behavioral_mimicry(rng, base_time, "test_inst", n_txns=30)
    df = result.transactions.sort_values("timestamp")
    # Coefficient of variation of inter-transaction intervals should be tiny
    intervals = df["timestamp"].diff().dt.total_seconds().dropna()
    cv = intervals.std() / intervals.mean()
    assert cv < 0.05, f"Expected CV < 0.05, got {cv:.4f}"
    # Amount uniformity
    amount_cv = df["amount_usdc"].std() / df["amount_usdc"].mean()
    assert amount_cv < 0.02, f"Expected amount CV < 0.02, got {amount_cv:.4f}"


def test_chain7_synchronized_identical_amounts(rng, base_time):
    result = inject_chain7_swarm_intelligence(rng, base_time, "test_inst", n_agents=50)
    df = result.transactions
    assert len(df) == 50
    # All amounts identical
    assert df["amount_usdc"].nunique() == 1
    # All within 2-second block window
    span = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    assert span <= 2.0, f"Expected ≤2s window, got {span:.2f}s"
    # Many different agents (not one sender)
    assert df["sender"].nunique() == 50


def test_chain8_wash_trading_circular_flows(rng, base_time):
    result = inject_chain8_market_manipulation(rng, base_time, "test_inst", n_wash_cycles=10)
    df = result.transactions
    # Find all address pairs (A, B) where A→B AND B→A both exist (true wash cycle).
    edge_pairs = set(zip(df["sender"], df["receiver"]))
    wash_cycles = [(a, b) for (a, b) in edge_pairs if (b, a) in edge_pairs]
    assert len(wash_cycles) >= 2, (
        f"Expected ≥2 bidirectional edge pairs (wash cycle), found: {wash_cycles}"
    )
    # Check that at least one wash cycle has near-equal amounts in both directions
    a, b = wash_cycles[0]
    a_to_b = df[(df["sender"] == a) & (df["receiver"] == b)]["amount_usdc"].values
    b_to_a = df[(df["sender"] == b) & (df["receiver"] == a)]["amount_usdc"].values
    n = min(len(a_to_b), len(b_to_a))
    assert n > 0
    assert np.allclose(a_to_b[:n], b_to_a[:n], rtol=0.002), (
        "Wash cycle amounts should be near-equal (within 0.2%)"
    )


# ---------------------------------------------------------------------------
# Address safety tests
# ---------------------------------------------------------------------------

def test_all_injected_addresses_use_prefix(rng, base_time):
    """All synthetic addresses must start with INJECTED_ADDR_PREFIX."""
    for chain_id, injector in [
        ("CHAIN_1", inject_chain1_enumeration),
        ("CHAIN_3", inject_chain3_async_flooding),
        ("CHAIN_7", inject_chain7_swarm_intelligence),
    ]:
        result = injector(rng, base_time, f"test_{chain_id}")
        senders = result.transactions["sender"].str.lower()
        receivers = result.transactions["receiver"].str.lower()
        all_addrs = pd.concat([senders, receivers])
        assert all_addrs.str.startswith(INJECTED_ADDR_PREFIX).all(), (
            f"{chain_id}: some addresses don't start with {INJECTED_ADDR_PREFIX}"
        )


def test_inject_all_chains_no_address_collision(minimal_real_df):
    """Injected addresses must not collide with real transaction addresses."""
    mixed_df, summary = inject_all_chains(minimal_real_df, seed=123)
    real_addrs = set(minimal_real_df["sender"]).union(set(minimal_real_df["receiver"]))
    injected = mixed_df[mixed_df["is_injected"]]
    injected_addrs = set(injected["sender"]).union(set(injected["receiver"]))
    collisions = real_addrs & injected_addrs
    assert len(collisions) == 0, f"Address collision: {collisions}"


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------

@pytest.mark.skipif(
    not (Path(__file__).resolve().parents[3] / "data" / "transactions_dune.parquet").exists(),
    reason="Real Dune dataset not available",
)
def test_inject_all_chains_rate_below_10_pct():
    """Total injection rate on real data (93K rows) must be ≤10%.

    Only runs when the actual Dune dataset is present. The default injection
    produces ~6,050 injected transactions; on 93,579 real rows that is 6.07%,
    well under the 10% limit. This constraint is only meaningful at realistic scale.
    """
    from pathlib import Path as _Path
    repo_root = _Path(__file__).resolve().parents[3]
    real_df = pd.read_parquet(repo_root / "data" / "transactions_dune.parquet")
    _, summary = inject_all_chains(real_df, seed=42)
    assert summary["injection_rate_pct"] <= 10.0, (
        f"Injection rate {summary['injection_rate_pct']:.1f}% exceeds 10%"
    )


def test_inject_all_chains_all_8_present(minimal_real_df):
    """All 8 attack chains must be present in the mixed dataset."""
    mixed_df, summary = inject_all_chains(minimal_real_df, seed=0)
    injected = mixed_df[mixed_df["is_injected"]]
    chains_present = set(injected["attack_chain"].unique())
    assert chains_present == set(CHAIN_DIFFICULTIES.keys()), (
        f"Missing chains: {set(CHAIN_DIFFICULTIES.keys()) - chains_present}"
    )


def test_inject_all_chains_label_columns_correct(minimal_real_df):
    """Real rows must have empty attack labels; injected rows must have correct labels."""
    mixed_df, _ = inject_all_chains(minimal_real_df, seed=0)
    real_rows = mixed_df[~mixed_df["is_injected"]]
    injected_rows = mixed_df[mixed_df["is_injected"]]

    # Real rows: empty labels
    assert (real_rows["attack_chain"] == "").all()
    assert (real_rows["attack_instance"] == "").all()

    # Injected rows: populated labels
    assert injected_rows["attack_chain"].ne("").all()
    assert injected_rows["attack_difficulty"].ne("").all()
    assert injected_rows["attack_instance"].ne("").all()


def test_inject_all_chains_minimum_instances_per_chain(minimal_real_df):
    """Each chain must have ≥5 instances injected."""
    mixed_df, summary = inject_all_chains(minimal_real_df, seed=0)
    for chain_id, stats in summary["chains"].items():
        assert stats["instances"] >= 5, (
            f"{chain_id}: only {stats['instances']} instances injected"
        )


def test_inject_all_chains_difficulty_labels_correct(minimal_real_df):
    """Difficulty labels on injected rows must match CHAIN_DIFFICULTIES."""
    mixed_df, _ = inject_all_chains(minimal_real_df, seed=0)
    injected = mixed_df[mixed_df["is_injected"]]
    for chain_id, expected_diff in CHAIN_DIFFICULTIES.items():
        chain_rows = injected[injected["attack_chain"] == chain_id]
        if len(chain_rows) > 0:
            assert (chain_rows["attack_difficulty"] == expected_diff).all(), (
                f"{chain_id}: expected difficulty {expected_diff}"
            )
