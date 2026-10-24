"""Candidate transaction features for registry-association research.

Scores are engineered feature values, not calibrated probabilities of agent
control, fraud, or suspicion. Fusion produces a research score and no adverse-
action decision.

The default fusion is an untuned equal-weight baseline over the four
implemented single-chain features. A post-hoc exploratory configuration is
available explicitly from ``SignalFusion.exploratory()``.
"""

from .economic_rationality import EconomicRationalitySignal
from .network_topology import NetworkTopologySignal
from .value_flow import ValueFlowSignal
from .temporal_consistency import TemporalConsistencySignal
from .cross_platform import CrossPlatformSignal
from .fusion import DetectionResult, SignalFusion

__all__ = [
    "EconomicRationalitySignal",
    "NetworkTopologySignal",
    "ValueFlowSignal",
    "TemporalConsistencySignal",
    "CrossPlatformSignal",
    "SignalFusion",
    "DetectionResult",
]
