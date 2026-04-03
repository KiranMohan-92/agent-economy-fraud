"""Signal Fusion and 4-Tier Decision System.

Combines 5 individual signal scores into a composite agent likelihood
score and maps it to one of 4 decision tiers:

    ALLOW:       score < 0.25 — Normal human transaction
    FLAG:        0.25 ≤ score < 0.50 — Elevated monitoring
    INVESTIGATE: 0.50 ≤ score < 0.75 — Manual review required
    BLOCK:       score ≥ 0.75 — High-confidence agent fraud

Signal weights (from Phase 4 implementation guidance):
    Economic Rationality:       0.25
    Network Topology:           0.25
    Value Flow:                 0.20
    Temporal Consistency:       0.20
    Cross-Platform Correlation: 0.10
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
import pandas as pd

from .economic_rationality import EconomicRationalitySignal
from .network_topology import NetworkTopologySignal
from .value_flow import ValueFlowSignal
from .temporal_consistency import TemporalConsistencySignal
from .cross_platform import CrossPlatformSignal


class DecisionTier(str, Enum):
    """4-tier decision system output."""

    ALLOW = "ALLOW"
    FLAG = "FLAG"
    INVESTIGATE = "INVESTIGATE"
    BLOCK = "BLOCK"


@dataclass
class DetectionResult:
    """Result of scoring a single address."""

    address: str
    composite_score: float
    decision: DecisionTier
    signal_scores: dict[str, float]
    confidence: float  # based on data availability

    def to_dict(self) -> dict:
        return {
            "address": self.address,
            "composite_score": round(self.composite_score, 4),
            "decision": self.decision.value,
            "confidence": round(self.confidence, 4),
            **{f"signal_{k}": round(v, 4) for k, v in self.signal_scores.items()},
        }


class SignalFusion:
    """Combines 5 signals into composite score and decision tier.

    The fusion layer is the core of the detection framework. It applies
    weighted combination with confidence adjustment based on data
    availability per signal.
    """

    # Signal weights — restored after Dune real-data validation (2026-04-03)
    # Value Flow restored to 0.20: with real timestamps, F1 triples (0.11 → 0.31)
    # Previous zeroing was due to synthetic data artifact (r=-0.47 with dead signal)
    # Phase 4 original weights: 0.25/0.25/0.20/0.20/0.10
    DEFAULT_WEIGHTS = {
        "economic_rationality": 0.25,
        "network_topology": 0.25,
        "value_flow": 0.20,
        "temporal_consistency": 0.20,
        "cross_platform": 0.10,
    }

    # Decision thresholds — 0.08 optimal on real Dune data (F1: 0.428, R: 0.954)
    # Previous 0.24 was calibrated on synthetic data with wider score spread
    THRESHOLD_FLAG = 0.08
    THRESHOLD_INVESTIGATE = 0.50
    THRESHOLD_BLOCK = 0.75

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()

        # Initialize signal scorers
        self.signals = {
            "economic_rationality": EconomicRationalitySignal(),
            "network_topology": NetworkTopologySignal(),
            "value_flow": ValueFlowSignal(),
            "temporal_consistency": TemporalConsistencySignal(),
            "cross_platform": CrossPlatformSignal(),
        }

    def score_address(
        self,
        address: str,
        transactions: pd.DataFrame,
    ) -> DetectionResult:
        """Score a single address using all 5 signals.

        Args:
            address: Wallet address to evaluate (lowercase hex).
            transactions: Full transaction DataFrame for context.

        Returns:
            DetectionResult with composite score, decision tier, and per-signal breakdown.
        """
        address = address.lower()
        signal_scores: dict[str, float] = {}
        available_weight = 0.0

        # Score each signal
        for name, scorer in self.signals.items():
            try:
                score = scorer.score_address(address, transactions)
                signal_scores[name] = score
                available_weight += self.weights[name]
            except Exception:
                signal_scores[name] = 0.0

        # Confidence = proportion of total weight that could be computed
        total_weight = sum(self.weights.values())
        confidence = available_weight / total_weight if total_weight > 0 else 0.0

        # Weighted fusion (renormalize to available weights)
        if available_weight > 0:
            composite = sum(
                self.weights[name] * signal_scores[name] for name in signal_scores
            ) / available_weight
        else:
            composite = 0.0

        composite = np.clip(composite, 0, 1)

        # Decision tier
        decision = self._classify(composite)

        return DetectionResult(
            address=address,
            composite_score=composite,
            decision=decision,
            signal_scores=signal_scores,
            confidence=confidence,
        )

    def score_batch(
        self,
        addresses: list[str],
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        """Score multiple addresses and return results as DataFrame.

        Optimizes by building the network graph once for all addresses.
        """
        # Pre-build network graph
        self.signals["network_topology"].build_graph(transactions)

        results = []
        for addr in addresses:
            result = self.score_address(addr, transactions)
            results.append(result.to_dict())

        return pd.DataFrame(results)

    def _classify(self, score: float) -> DecisionTier:
        """Map composite score to decision tier."""
        if score >= self.THRESHOLD_BLOCK:
            return DecisionTier.BLOCK
        elif score >= self.THRESHOLD_INVESTIGATE:
            return DecisionTier.INVESTIGATE
        elif score >= self.THRESHOLD_FLAG:
            return DecisionTier.FLAG
        return DecisionTier.ALLOW

    def evaluate(
        self,
        results: pd.DataFrame,
        labels: pd.DataFrame,
        label_column: str = "label",
        positive_label: str = "agent",
    ) -> dict:
        """Evaluate detection performance against ground-truth labels.

        Args:
            results: Output from score_batch().
            labels: DataFrame with address and label columns.
            label_column: Name of the label column.
            positive_label: Label value for agents (positive class).

        Returns:
            Dict with precision, recall, F1, ROC-AUC, and confusion matrix.
        """
        from sklearn.metrics import (
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
            confusion_matrix,
        )

        merged = results.merge(
            labels[["address", label_column]],
            on="address",
            how="inner",
        )

        if len(merged) == 0:
            return {"error": "No matching addresses between results and labels"}

        y_true = (merged[label_column] == positive_label).astype(int)
        y_score = merged["composite_score"]
        y_pred = (y_score >= self.THRESHOLD_FLAG).astype(int)  # binary at FLAG threshold

        metrics = {
            "n_evaluated": len(merged),
            "n_positive": int(y_true.sum()),
            "n_negative": int((1 - y_true).sum()),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        }

        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_score))
        except ValueError:
            metrics["roc_auc"] = None

        # Per-tier breakdown
        for tier in DecisionTier:
            tier_mask = merged["decision"] == tier.value
            metrics[f"tier_{tier.value.lower()}_count"] = int(tier_mask.sum())
            metrics[f"tier_{tier.value.lower()}_agent_rate"] = float(
                y_true[tier_mask].mean()
            ) if tier_mask.any() else 0.0

        return metrics
