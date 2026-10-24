"""Exploratory fusion of candidate transaction features.

The composite is a registry-association research score. It is not a
probability of autonomy or fraud and must not be used as a sole adverse-action,
allow, or block decision.

The default is an untuned equal-weight baseline over the four implemented
single-chain features. ``EXPLORATORY_WEIGHTS`` contains post-hoc weights
developed on the same 1,734-address cohort used for evaluation. They yield an
in-sample AUC of 0.622 and a random-address cross-fitted AUC of 0.612. Both
are provisional until preserved in an immutable end-to-end run manifest
(GPD/CLAIM-LEDGER.md AEF-C006); only the historical composite AUC 0.5147 is
reproduced by the preserved audit. Neither is an external generalization
estimate: cohort construction and graph features leak across random address
folds. Use those weights only for model development.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .cross_platform import CrossPlatformSignal
from .economic_rationality import EconomicRationalitySignal
from .network_topology import NetworkTopologySignal
from .temporal_consistency import TemporalConsistencySignal
from .value_flow import ValueFlowSignal


@dataclass
class DetectionResult:
    """Exploratory score for one address."""

    address: str
    composite_score: float
    above_historical_reference: bool
    signal_scores: dict[str, float]
    confidence: float

    def to_dict(self) -> dict:
        return {
            "address": self.address,
            "composite_score": round(self.composite_score, 4),
            "above_historical_reference": self.above_historical_reference,
            "confidence": round(self.confidence, 4),
            **{f"signal_{key}": round(value, 4) for key, value in self.signal_scores.items()},
        }


class SignalFusion:
    """Combine candidate features into a non-operational research score."""

    # Untuned baseline: no labels are used to choose relative weights.
    DEFAULT_WEIGHTS = {
        "economic_rationality": 0.25,
        "network_topology": 0.25,
        "value_flow": 0.25,
        "temporal_consistency": 0.25,
        "cross_platform": 0.00,
    }

    # Developed and measured on the same cohort. These values are retained for
    # transparent exploratory reproduction, not as confirmatory defaults.
    EXPLORATORY_WEIGHTS = {
        "economic_rationality": 0.1116,
        "network_topology": 0.7269,
        "value_flow": 0.1615,
        "temporal_consistency": 0.0000,
        "cross_platform": 0.00,
    }

    # Historical only. It is not optimal after changing weights and is not an
    # operational threshold.
    HISTORICAL_REFERENCE_THRESHOLD = 0.09

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self._validate_weights()
        self.signals = {
            "economic_rationality": EconomicRationalitySignal(),
            "network_topology": NetworkTopologySignal(),
            "value_flow": ValueFlowSignal(),
            "temporal_consistency": TemporalConsistencySignal(),
            "cross_platform": CrossPlatformSignal(),
        }

    @classmethod
    def exploratory(cls) -> "SignalFusion":
        """Construct the explicitly post-hoc, label-developed configuration."""
        return cls(weights=cls.EXPLORATORY_WEIGHTS.copy())

    def _validate_weights(self) -> None:
        expected = set(self.DEFAULT_WEIGHTS)
        if set(self.weights) != expected:
            missing = sorted(expected - set(self.weights))
            extra = sorted(set(self.weights) - expected)
            raise ValueError(f"Weight keys mismatch; missing={missing}, extra={extra}")
        if any(value < 0 for value in self.weights.values()):
            raise ValueError("Signal weights must be non-negative")
        if sum(self.weights.values()) <= 0:
            raise ValueError("At least one signal weight must be positive")

    def score_address(
        self,
        address: str,
        transactions: pd.DataFrame,
    ) -> DetectionResult:
        """Score one address and return candidate-feature contributions."""
        address = address.lower()
        signal_scores: dict[str, float] = {}
        available_weight = 0.0

        for name, scorer in self.signals.items():
            try:
                score = scorer.score_address(address, transactions)
                signal_scores[name] = score
                available_weight += self.weights[name]
            except Exception:
                signal_scores[name] = 0.0

        total_weight = sum(self.weights.values())
        confidence = available_weight / total_weight if total_weight > 0 else 0.0

        if available_weight > 0:
            composite = sum(
                self.weights[name] * signal_scores[name] for name in signal_scores
            ) / available_weight
        else:
            composite = 0.0

        composite = float(np.clip(composite, 0, 1))
        return DetectionResult(
            address=address,
            composite_score=composite,
            above_historical_reference=(
                composite >= self.HISTORICAL_REFERENCE_THRESHOLD
            ),
            signal_scores=signal_scores,
            confidence=confidence,
        )

    def score_batch(
        self,
        addresses: list[str],
        transactions: pd.DataFrame,
    ) -> pd.DataFrame:
        """Score multiple addresses, building the graph once."""
        self.signals["network_topology"].build_graph(transactions)
        return pd.DataFrame(
            [self.score_address(address, transactions).to_dict() for address in addresses]
        )

    def evaluate(
        self,
        results: pd.DataFrame,
        labels: pd.DataFrame,
        label_column: str = "label",
        positive_label: str = "registry_owner_proxy",
        threshold: float | None = None,
    ) -> dict:
        """Evaluate a proxy-label experiment at an explicit research threshold.

        Historical label files used ``agent`` for the positive proxy. Callers
        reproducing that artifact must pass ``positive_label='agent'``.
        """
        from sklearn.metrics import (
            confusion_matrix,
            f1_score,
            precision_score,
            recall_score,
            roc_auc_score,
        )

        merged = results.merge(
            labels[["address", label_column]], on="address", how="inner"
        )
        if len(merged) == 0:
            return {"error": "No matching addresses between results and labels"}

        decision_threshold = (
            self.HISTORICAL_REFERENCE_THRESHOLD if threshold is None else threshold
        )
        y_true = (merged[label_column] == positive_label).astype(int)
        y_score = merged["composite_score"]
        y_pred = (y_score >= decision_threshold).astype(int)

        metrics = {
            "construct": "registry_owner_proxy_discrimination",
            "threshold": float(decision_threshold),
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
        return metrics
