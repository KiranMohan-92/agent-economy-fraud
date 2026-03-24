"""5-signal agent-invariant detection framework.

Each signal scores a transaction or address on a [0, 1] scale where:
    0.0 = fully consistent with human behavior
    1.0 = maximally agent-like / suspicious

Signals are fused via weighted combination into a composite score,
which feeds the 4-tier decision system.

Signal weights (from Phase 4 implementation guidance):
    Economic Rationality:       0.25
    Network Topology:           0.25
    Value Flow:                 0.20
    Temporal Consistency:       0.20
    Cross-Platform Correlation: 0.10
"""

from .economic_rationality import EconomicRationalitySignal
from .network_topology import NetworkTopologySignal
from .value_flow import ValueFlowSignal
from .temporal_consistency import TemporalConsistencySignal
from .cross_platform import CrossPlatformSignal
from .fusion import SignalFusion, DecisionTier

__all__ = [
    "EconomicRationalitySignal",
    "NetworkTopologySignal",
    "ValueFlowSignal",
    "TemporalConsistencySignal",
    "CrossPlatformSignal",
    "SignalFusion",
    "DecisionTier",
]
