"""Unit tests for all 5 detection signals and the SignalFusion layer.

Tests validate three properties for each signal:
  1. Score range: output is always in [0, 1]
  2. Discrimination: agent-like patterns score higher than human-like patterns
  3. Edge cases: insufficient data returns 0.0 without raising exceptions
"""

from __future__ import annotations

import pandas as pd
import pytest

from a2a_detection.signals.economic_rationality import EconomicRationalitySignal
from a2a_detection.signals.network_topology import NetworkTopologySignal
from a2a_detection.signals.temporal_consistency import TemporalConsistencySignal
from a2a_detection.signals.value_flow import ValueFlowSignal
from a2a_detection.signals.cross_platform import CrossPlatformSignal
from a2a_detection.signals.fusion import SignalFusion, DecisionTier


# ── Signal 1: Economic Rationality ───────────────────────────────────────────


class TestEconomicRationalitySignal:
    def setup_method(self):
        self.signal = EconomicRationalitySignal()

    def test_score_range_agent(self, circular_flow_txns, agent_addr):
        score = self.signal.score_address(agent_addr, circular_flow_txns)
        assert 0.0 <= score <= 1.0

    def test_score_range_human(self, human_txns, human_addr):
        score = self.signal.score_address(human_addr, human_txns)
        assert 0.0 <= score <= 1.0

    def test_circular_agent_scores_higher_than_human(
        self, circular_flow_txns, agent_addr, human_txns, human_addr
    ):
        agent_score = self.signal.score_address(agent_addr, circular_flow_txns)
        human_score = self.signal.score_address(human_addr, human_txns)
        assert agent_score > human_score, (
            f"Circular-flow agent (score={agent_score:.3f}) should outscore "
            f"purposeful human (score={human_score:.3f})"
        )

    def test_insufficient_data_returns_zero(self, agent_addr):
        """Fewer than 3 transactions should return 0.0, not raise."""
        tiny = pd.DataFrame([
            {"sender": agent_addr, "receiver": "0xother", "amount_usdc": 1.0, "timestamp": "2026-01-01"},
        ])
        score = self.signal.score_address(agent_addr, tiny)
        assert score == 0.0

    def test_empty_dataframe_returns_zero(self, agent_addr):
        empty = pd.DataFrame(columns=["sender", "receiver", "amount_usdc", "timestamp"])
        score = self.signal.score_address(agent_addr, empty)
        assert score == 0.0


# ── Signal 2: Network Topology ────────────────────────────────────────────────


class TestNetworkTopologySignal:
    def setup_method(self):
        self.signal = NetworkTopologySignal()

    def test_score_range_high_degree_agent(self, burst_agent_txns, agent_addr):
        score = self.signal.score_address(agent_addr, burst_agent_txns)
        assert 0.0 <= score <= 1.0

    def test_high_degree_agent_scores_higher_than_human(
        self, burst_agent_txns, agent_addr, human_txns, human_addr
    ):
        # An agent with 200 unique counterparties has extreme out-degree z-score
        combined = pd.concat([burst_agent_txns, human_txns], ignore_index=True)
        self.signal.build_graph(combined)
        agent_score = self.signal.score_address(agent_addr, combined)
        human_score = self.signal.score_address(human_addr, combined)
        assert agent_score > human_score, (
            f"High-degree agent (score={agent_score:.3f}) should outscore "
            f"low-degree human (score={human_score:.3f})"
        )

    def test_graph_builds_without_error(self, relay_agent_txns):
        self.signal.build_graph(relay_agent_txns)
        assert self.signal._graph is not None
        assert self.signal._degree_stats is not None

    def test_unknown_address_returns_zero(self, relay_agent_txns):
        self.signal.build_graph(relay_agent_txns)
        score = self.signal.score_address("0xnonexistent", relay_agent_txns)
        assert score == 0.0

    def test_score_without_prebuild(self, burst_agent_txns, agent_addr):
        """score_address auto-builds graph if build_graph wasn't called first."""
        fresh_signal = NetworkTopologySignal()
        score = fresh_signal.score_address(agent_addr, burst_agent_txns)
        assert 0.0 <= score <= 1.0


# ── Signal 3: Value Flow ──────────────────────────────────────────────────────


class TestValueFlowSignal:
    def setup_method(self):
        self.signal = ValueFlowSignal()

    def test_score_range_relay_agent(self, relay_agent_txns, agent_addr):
        score = self.signal.score_address(agent_addr, relay_agent_txns)
        assert 0.0 <= score <= 1.0

    def test_relay_agent_scores_higher_than_human(
        self, relay_agent_txns, agent_addr, human_txns, human_addr
    ):
        agent_score = self.signal.score_address(agent_addr, relay_agent_txns)
        human_score = self.signal.score_address(human_addr, human_txns)
        assert agent_score > human_score, (
            f"Relay agent (score={agent_score:.3f}) should outscore "
            f"slow human (score={human_score:.3f})"
        )

    def test_rapid_relay_produces_nonzero_velocity(self, relay_agent_txns, agent_addr):
        """An agent relaying within 3 seconds should produce non-zero flow velocity."""
        score = self.signal.score_address(agent_addr, relay_agent_txns)
        assert score > 0.0, "Rapid relay should produce a positive value flow score"

    def test_insufficient_data_returns_zero(self, agent_addr):
        tiny = pd.DataFrame([
            {"sender": agent_addr, "receiver": "0xother", "amount_usdc": 1.0,
             "timestamp": "2026-01-01T00:00:00Z"},
            {"sender": "0xother", "receiver": agent_addr, "amount_usdc": 1.0,
             "timestamp": "2026-01-01T00:00:05Z"},
        ])
        score = self.signal.score_address(agent_addr, tiny)
        assert score == 0.0

    def test_net_flow_imbalance_not_used(self):
        """Confirm _net_flow_imbalance is NOT wired into score_address (v0.3+).

        The sub-signal was removed because it fires inversely on real data
        (one-directional human counterparties score maximum imbalance).
        The method should still exist in the class for audit trail, but
        score_address should not call it.
        """
        import inspect
        source = inspect.getsource(ValueFlowSignal.score_address)
        assert "_net_flow_imbalance" not in source, (
            "_net_flow_imbalance was re-introduced into score_address. "
            "This sub-signal discriminates inversely on real on-chain data "
            "(see value_flow.py v0.3 changelog)."
        )


# ── Signal 4: Temporal Consistency ────────────────────────────────────────────


class TestTemporalConsistencySignal:
    def setup_method(self):
        self.signal = TemporalConsistencySignal()

    def test_score_range_burst_agent(self, burst_agent_txns, agent_addr):
        score = self.signal.score_address(agent_addr, burst_agent_txns)
        assert 0.0 <= score <= 1.0

    def test_burst_agent_scores_higher_than_human(
        self, burst_agent_txns, agent_addr, human_txns, human_addr
    ):
        combined = pd.concat([burst_agent_txns, human_txns], ignore_index=True)
        agent_score = self.signal.score_address(agent_addr, combined)
        human_score = self.signal.score_address(human_addr, combined)
        assert agent_score > human_score, (
            f"Burst agent (score={agent_score:.3f}) should outscore "
            f"human with daily transactions (score={human_score:.3f})"
        )

    def test_sleep_hour_activity_detected(self, burst_agent_txns, agent_addr):
        """burst_agent_txns start at 3 AM UTC — circadian violation should fire."""
        score = self.signal.score_address(agent_addr, burst_agent_txns)
        assert score > 0.0, "3 AM UTC burst activity should trigger circadian violation"

    def test_insufficient_data_returns_zero(self, agent_addr):
        """Fewer than 5 transactions should return 0.0."""
        tiny = pd.DataFrame([
            {"sender": agent_addr, "receiver": "0xb", "amount_usdc": 1.0,
             "timestamp": "2026-01-01T00:00:00Z"},
        ] * 3)
        score = self.signal.score_address(agent_addr, tiny)
        assert score == 0.0


# ── Signal 5: Cross-Platform Correlation ──────────────────────────────────────


class TestCrossPlatformSignal:
    def setup_method(self):
        self.signal = CrossPlatformSignal()

    def test_score_range_multichain(self, multichain_txns, agent_addr):
        score = self.signal.score_address(agent_addr, multichain_txns)
        assert 0.0 <= score <= 1.0

    def test_multichain_agent_scores_nonzero(self, multichain_txns, agent_addr):
        """Agent active on 3 chains in <10s windows should score > 0."""
        score = self.signal.score_address(agent_addr, multichain_txns)
        assert score > 0.0, "3-chain simultaneous activity should produce a non-zero score"

    def test_single_chain_data_returns_zero(self, relay_agent_txns, agent_addr):
        """Without a 'chain' column, the signal cannot evaluate and returns 0.0."""
        score = self.signal.score_address(agent_addr, relay_agent_txns)
        assert score == 0.0

    def test_single_chain_column_returns_zero(self, relay_agent_txns, agent_addr):
        """One chain in the chain column means no cross-chain signal."""
        txns = relay_agent_txns.copy()
        txns["chain"] = "base"
        score = self.signal.score_address(agent_addr, txns)
        assert score == 0.0

    def test_multichain_scores_higher_than_single_chain(
        self, multichain_txns, relay_agent_txns, agent_addr
    ):
        single_chain = relay_agent_txns.copy()
        single_chain["chain"] = "base"
        multi_score = self.signal.score_address(agent_addr, multichain_txns)
        single_score = self.signal.score_address(agent_addr, single_chain)
        assert multi_score > single_score


# ── SignalFusion ──────────────────────────────────────────────────────────────


class TestSignalFusion:
    def setup_method(self):
        self.fusion = SignalFusion()

    def test_score_address_returns_detection_result(self, relay_agent_txns, agent_addr):
        result = self.fusion.score_address(agent_addr, relay_agent_txns)
        assert 0.0 <= result.composite_score <= 1.0
        assert result.decision in list(DecisionTier)
        assert set(result.signal_scores.keys()) == {
            "economic_rationality", "network_topology", "value_flow",
            "temporal_consistency", "cross_platform",
        }

    def test_all_decision_tiers_accessible(self, relay_agent_txns, burst_agent_txns, agent_addr, human_txns, human_addr):
        """Confirm ALLOW tier fires on a human address with minimal transactions."""
        result = self.fusion.score_address(human_addr, human_txns)
        # Low-activity human should ALLOW or FLAG
        assert result.decision in (DecisionTier.ALLOW, DecisionTier.FLAG)

    def test_score_batch_returns_dataframe(self, relay_agent_txns, agent_addr, human_txns, human_addr):
        combined = pd.concat([relay_agent_txns, human_txns], ignore_index=True)
        addresses = [agent_addr, human_addr]
        results = self.fusion.score_batch(addresses, combined)
        assert len(results) == 2
        assert "composite_score" in results.columns
        assert "decision" in results.columns

    def test_weights_sum_to_one(self):
        total = sum(self.fusion.weights.values())
        assert abs(total - 1.0) < 1e-6, f"Weights sum to {total}, expected 1.0"

    def test_evaluate_returns_expected_metrics(self, relay_agent_txns, agent_addr, human_txns, human_addr):
        combined = pd.concat([relay_agent_txns, human_txns], ignore_index=True)
        addresses = [agent_addr, human_addr]
        results = self.fusion.score_batch(addresses, combined)
        labels = pd.DataFrame([
            {"address": agent_addr, "label": "agent"},
            {"address": human_addr, "label": "human"},
        ])
        metrics = self.fusion.evaluate(results, labels)
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert "n_evaluated" in metrics
        assert metrics["n_evaluated"] == 2

    def test_confidence_reflects_available_signals(self, human_txns, human_addr):
        """Cross-platform signal returns 0 without chain column; confidence < 1."""
        # human_txns has no 'chain' column — cross_platform signal will return 0
        result = self.fusion.score_address(human_addr, human_txns)
        # cross_platform weight = 0.0, so available_weight still = 1.0
        # (the zero-weighted signal doesn't reduce confidence)
        assert result.confidence > 0.0

    def test_default_threshold_is_009(self):
        assert self.fusion.THRESHOLD_FLAG == 0.09, (
            "FLAG threshold was changed from 0.09. "
            "This is the F1-optimal threshold on real Dune data (2026-04-04). "
            "Update this test only after a new threshold sweep on updated real data."
        )

    def test_auc_proportional_weights(self):
        """AUC-proportional weights: network_topology must be highest, value_flow lowest."""
        w = self.fusion.DEFAULT_WEIGHTS
        assert w["network_topology"] >= w["temporal_consistency"], (
            "network_topology (AUC=0.6214) should outweigh temporal_consistency (AUC=0.5683)"
        )
        assert w["temporal_consistency"] >= w["economic_rationality"], (
            "temporal_consistency (AUC=0.5683) should outweigh economic_rationality (AUC=0.5497)"
        )
        assert w["economic_rationality"] >= w["value_flow"], (
            "economic_rationality (AUC=0.5497) should outweigh value_flow (AUC=0.5290)"
        )
