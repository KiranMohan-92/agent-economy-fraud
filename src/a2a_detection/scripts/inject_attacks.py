"""Attack Pattern Injector — Phase 6, Plan 06-01.

Injects synthetic instances of all 8 A2A attack chains (from Phase 2 taxonomy)
into the real USDC transaction stream, producing a labeled mixed dataset for
fraud detection validation.

Attack Chains Implemented:
    CHAIN 1  — Agent Enumeration Attack (EASY)
    CHAIN 2  — Transaction History Extraction Attack (MEDIUM)
    CHAIN 3  — Asynchronous Transaction Flooding Attack (MEDIUM)
    CHAIN 4  — Disposable Agent Army Attack (HARD)
    CHAIN 5  — Cross-Platform Identity Persistence Attack (IMPOSSIBLE)
    CHAIN 6  — Human Behavioral Mimicry Attack (IMPOSSIBLE)
    CHAIN 7  — Coordinated Swarm Intelligence Attack (IMPOSSIBLE)
    CHAIN 8  — Financial Market Manipulation Attack (IMPOSSIBLE)

Output Schema (extends real transaction schema):
    All original columns plus:
        is_injected       bool   — True for synthetic attack transactions
        attack_chain      str    — 'CHAIN_1' through 'CHAIN_8', empty for real
        attack_instance   str    — unique ID per attack instance
        attack_difficulty str    — EASY/MEDIUM/HARD/IMPOSSIBLE, empty for real

Usage:
    python -m a2a_detection.scripts.inject_attacks
    python -m a2a_detection.scripts.inject_attacks --input data/transactions_dune.parquet \
        --output data/attack_injection_dataset.parquet --seed 42
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USDC_CONTRACT = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
INJECTED_ADDR_PREFIX = "0xdead"   # clearly fake; not in ERC-8004 registry or Dune data

CHAIN_DIFFICULTIES = {
    "CHAIN_1": "EASY",
    "CHAIN_2": "MEDIUM",
    "CHAIN_3": "MEDIUM",
    "CHAIN_4": "HARD",
    "CHAIN_5": "IMPOSSIBLE",
    "CHAIN_6": "IMPOSSIBLE",
    "CHAIN_7": "IMPOSSIBLE",
    "CHAIN_8": "IMPOSSIBLE",
}


# ---------------------------------------------------------------------------
# Address generation helpers
# ---------------------------------------------------------------------------

def _synthetic_addr(chain_id: str, index: int, role: str = "") -> str:
    """Generate a deterministic fake address that cannot collide with real data.

    Format: 0xdead<chain_hex><role_byte><index_hex>
    All synthetic addresses start with 0xdead, which is not a valid ERC-8004
    address and is not present in the Dune dataset.
    """
    chain_num = int(chain_id.split("_")[1])
    role_byte = hashlib.md5(role.encode()).hexdigest()[:2] if role else "00"
    # 42-char Ethereum address: "0x" (2) + 40 hex chars.
    # Prefix uses 10 chars ("0xdead" + chain_num 2-hex + role_byte 2-hex),
    # leaving exactly 32 chars for the index — no truncation needed.
    suffix = f"{index:032x}"
    return f"{INJECTED_ADDR_PREFIX}{chain_num:02x}{role_byte}{suffix}"


# ---------------------------------------------------------------------------
# Per-chain injectors
# ---------------------------------------------------------------------------

@dataclass
class InjectionResult:
    """Injected transactions for a single attack instance."""

    chain_id: str
    instance_id: str
    transactions: pd.DataFrame


def _base_txrow(
    sender: str,
    receiver: str,
    timestamp: pd.Timestamp,
    amount: float,
    chain_id: str,
    instance_id: str,
    block_offset: int = 0,
    ref_block: int = 27_000_000,
) -> dict:
    """Build a single synthetic transaction row."""
    tx_bytes = f"{chain_id}:{instance_id}:{sender}:{receiver}:{timestamp}:{amount}"
    tx_hash = "0x" + hashlib.sha256(tx_bytes.encode()).hexdigest()
    return {
        "tx_hash": tx_hash,
        "block_number": ref_block + block_offset,
        "timestamp": timestamp,
        "sender": sender,
        "receiver": receiver,
        "amount_usdc": round(amount, 6),
        "token_contract": USDC_CONTRACT,
        "direction": "outbound",
        "is_injected": True,
        "attack_chain": chain_id,
        "attack_instance": instance_id,
        "attack_difficulty": CHAIN_DIFFICULTIES[chain_id],
    }


def inject_chain1_enumeration(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_probes: int = 30,
) -> InjectionResult:
    """CHAIN 1 — Agent Enumeration Attack (EASY).

    Behavioral signature: Single attacker address probing many target addresses
    via tiny (dust) transactions in rapid succession — simulates sessions_list
    enumeration followed by contact probing. Detectable via high out-degree
    within a short time window.

    Detection signal: Network Topology (high out-degree, short window)
    """
    attacker = _synthetic_addr("CHAIN_1", 0, "attacker")
    rows = []
    for i in range(n_probes):
        target = _synthetic_addr("CHAIN_1", i + 1, "target")
        ts = base_time + timedelta(seconds=int(rng.integers(0, 60)))
        amount = rng.uniform(0.001, 0.010)   # dust probes
        rows.append(_base_txrow(attacker, target, ts, amount, "CHAIN_1", instance_id, i))
    return InjectionResult("CHAIN_1", instance_id, pd.DataFrame(rows))


def inject_chain2_history_extraction(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_reads: int = 25,
) -> InjectionResult:
    """CHAIN 2 — Transaction History Extraction Attack (MEDIUM).

    Behavioral signature: Single attacker repeatedly transacting with the same
    target in a short window (simulates sessions_history bulk access pattern).
    Detectable as repeated-edge burst in graph.

    Detection signal: Network Topology (repeated edge), Value Flow (fan-in)
    """
    attacker = _synthetic_addr("CHAIN_2", 0, "attacker")
    target = _synthetic_addr("CHAIN_2", 1, "target")
    rows = []
    for i in range(n_reads):
        ts = base_time + timedelta(seconds=int(rng.integers(0, 120)))
        amount = rng.uniform(0.01, 0.05)
        rows.append(_base_txrow(attacker, target, ts, amount, "CHAIN_2", instance_id, i))
    return InjectionResult("CHAIN_2", instance_id, pd.DataFrame(rows))


def inject_chain3_async_flooding(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_flood_txns: int = 500,
) -> InjectionResult:
    """CHAIN 3 — Asynchronous Transaction Flooding Attack (MEDIUM).

    Behavioral signature: Single attacker sends ≥500 transactions within a 1-hour
    window at uniform machine-speed intervals (~0.4s apart — OpenClaw channel rate
    limit). Models sessions_send with timeoutSeconds=0 fire-and-forget mode.
    Extrapolated rate: 500/hr → 9,000/day >> human max of 100/day.

    Detection signal: Temporal Consistency (machine-speed burst)
    """
    attacker = _synthetic_addr("CHAIN_3", 0, "attacker")
    rows = []
    # Machine-speed: 0.4 second intervals (OpenClaw channel rate limit)
    for i in range(n_flood_txns):
        ts = base_time + timedelta(seconds=i * 0.4)
        amount = rng.uniform(0.001, 1.0)
        target = _synthetic_addr("CHAIN_3", (i % 20) + 1, "target")
        rows.append(_base_txrow(attacker, target, ts, amount, "CHAIN_3", instance_id, i))
    return InjectionResult("CHAIN_3", instance_id, pd.DataFrame(rows))


def inject_chain4_agent_army(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_agents: int = 15,
    txns_per_agent: int = 10,
) -> InjectionResult:
    """CHAIN 4 — Disposable Agent Army Attack (HARD).

    Behavioral signature: ≥15 new addresses all activated within a 90-second
    window, each transacting to the same sink address. Models sessions_spawn
    creating disposable sub-agents with cleanup:delete. Detectable by correlated
    activation timing across unrelated addresses.

    Detection signal: Network Topology (coordinated activation cluster)
    """
    sink = _synthetic_addr("CHAIN_4", 0, "sink")
    rows = []
    for agent_idx in range(n_agents):
        agent = _synthetic_addr("CHAIN_4", agent_idx + 1, "agent")
        # All agents activate within 90 seconds of each other
        activation_offset = rng.integers(0, 90)
        for txn_idx in range(txns_per_agent):
            ts = base_time + timedelta(
                seconds=activation_offset + txn_idx * rng.uniform(1.0, 5.0)
            )
            amount = rng.uniform(0.1, 5.0)
            block_off = agent_idx * txns_per_agent + txn_idx
            rows.append(_base_txrow(agent, sink, ts, amount, "CHAIN_4", instance_id, block_off))
    return InjectionResult("CHAIN_4", instance_id, pd.DataFrame(rows))


def inject_chain5_cross_platform_identity(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_chains: int = 3,
    txns_per_chain: int = 10,
) -> InjectionResult:
    """CHAIN 5 — Cross-Platform Identity Persistence Attack (IMPOSSIBLE).

    Behavioral signature: Same CREATE2-derived address appearing simultaneously
    active on multiple chains within the same block range. On Base data this
    manifests as an address with unusually precise near-zero creation cost
    ($0.001–0.01) transacting to targets across different contract types.
    Proxy signal: extremely low-cost address creation + high multi-hop activity.

    Detection signal: Economic Rationality (below-human-cognitive-cost precision),
    Network Topology (multi-hop fan-out from a single new address)
    """
    # One attacker address active from multiple "chains" (simulated via identical address)
    attacker = _synthetic_addr("CHAIN_5", 0, "attacker")
    rows = []
    block_off = 0
    for chain_idx in range(n_chains):
        # Simultaneous activity: all chains within same 30-second window
        for txn_idx in range(txns_per_chain):
            ts = base_time + timedelta(seconds=chain_idx * 2 + txn_idx * 0.5)
            amount = rng.uniform(0.001, 0.01)  # near-zero cost (cross-platform precision)
            target = _synthetic_addr("CHAIN_5", chain_idx * 10 + txn_idx + 1, "target")
            rows.append(_base_txrow(attacker, target, ts, amount, "CHAIN_5", instance_id, block_off))
            block_off += 1
    return InjectionResult("CHAIN_5", instance_id, pd.DataFrame(rows))


def inject_chain6_behavioral_mimicry(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_txns: int = 50,
    victim_mean_interval_s: float = 138.0,  # 2.3 min — typical human spacing
) -> InjectionResult:
    """CHAIN 6 — Human Behavioral Mimicry Attack (IMPOSSIBLE).

    Behavioral signature: Agent mimics a human victim's timing with perfect
    regularity (CV ≈ 0.01 vs real agents CV=1.87). The key signature is
    "too-perfect" temporal regularity — no variance in spacing, no circadian
    pattern, identical amounts. Real humans and real agents both show high
    variance; perfect mimicry shows near-zero variance.

    Detection signal: Temporal Consistency (CV too low = suspicious uniformity)
    """
    attacker = _synthetic_addr("CHAIN_6", 0, "attacker")
    target = _synthetic_addr("CHAIN_6", 1, "target")
    rows = []
    # Perfect timing: identical intervals with CV < 0.02
    interval_s = victim_mean_interval_s
    for i in range(n_txns):
        # Near-zero variance: tiny jitter (CV ≈ 0.005)
        jitter = rng.normal(0, interval_s * 0.005)
        ts = base_time + timedelta(seconds=i * interval_s + jitter)
        # Near-identical amounts (perfect rational optimization, CV ≈ 0.005)
        amount = 1.0 + rng.normal(0, 0.005)
        rows.append(_base_txrow(attacker, target, ts, amount, "CHAIN_6", instance_id, i))
    return InjectionResult("CHAIN_6", instance_id, pd.DataFrame(rows))


def inject_chain7_swarm_intelligence(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_agents: int = 55,
    identical_amount: float | None = None,
) -> InjectionResult:
    """CHAIN 7 — Coordinated Swarm Intelligence Attack (IMPOSSIBLE).

    Behavioral signature: ≥50 addresses all sending the exact same amount to
    different targets within a 2-second window (1 block on Base ≈ 2s).
    Models sessions_send broadcast: attacker sends one command, 50+ sub-agents
    execute simultaneously. No human coordination achieves this.

    Detection signal: Temporal Consistency (synchronized burst), Network
    Topology (simultaneous multi-source fan-out)
    """
    if identical_amount is None:
        # Pick a "round" amount to make the pattern conspicuous
        identical_amount = round(rng.choice([0.5, 1.0, 5.0, 10.0, 50.0]), 2)
    rows = []
    for i in range(n_agents):
        agent = _synthetic_addr("CHAIN_7", i, "agent")
        target = _synthetic_addr("CHAIN_7", n_agents + i, "target")
        # All within 2-second window (one Base block)
        ts = base_time + timedelta(seconds=rng.uniform(0, 2.0))
        rows.append(_base_txrow(agent, target, ts, identical_amount, "CHAIN_7", instance_id, i))
    return InjectionResult("CHAIN_7", instance_id, pd.DataFrame(rows))


def inject_chain8_market_manipulation(
    rng: np.random.Generator,
    base_time: pd.Timestamp,
    instance_id: str,
    n_wash_cycles: int = 20,
    n_layering_steps: int = 5,
) -> InjectionResult:
    """CHAIN 8 — Financial Market Manipulation Attack (IMPOSSIBLE).

    Behavioral signature: Wash trading (A→B→A cycles with same amounts) plus
    layering (A→B→C→D→A with diminishing amounts — simulates HFT accumulation).
    Models cron-triggered HFT strategy with coordinated buy/sell cycles.

    Detection signal: Value Flow (circular/wash patterns), Economic Rationality
    (zero-net-value cycles violate rational agent assumptions)
    """
    rows = []
    block_off = 0

    # Wash trading component: A→B→A with near-identical amounts
    wash_a = _synthetic_addr("CHAIN_8", 0, "wash_a")
    wash_b = _synthetic_addr("CHAIN_8", 1, "wash_b")
    for cycle in range(n_wash_cycles):
        amount = round(rng.uniform(10.0, 100.0), 2)
        t1 = base_time + timedelta(seconds=cycle * 4.0)
        t2 = t1 + timedelta(seconds=rng.uniform(0.5, 1.5))
        rows.append(_base_txrow(wash_a, wash_b, t1, amount, "CHAIN_8", instance_id, block_off))
        block_off += 1
        # Return leg: same amount (±0.1% slippage)
        return_amount = amount * (1 + rng.uniform(-0.001, 0.001))
        rows.append(_base_txrow(wash_b, wash_a, t2, return_amount, "CHAIN_8", instance_id, block_off))
        block_off += 1

    # Layering component: A→B→C→D→E (diminishing) — obfuscation trail
    layer_addrs = [_synthetic_addr("CHAIN_8", 10 + i, "layer") for i in range(n_layering_steps + 1)]
    base_amount = rng.uniform(50.0, 200.0)
    for step in range(n_layering_steps):
        ts = base_time + timedelta(seconds=step * 2.0 + rng.uniform(0, 0.5))
        # Each hop takes a 2% fee (layering trace)
        layer_amount = base_amount * (0.98 ** step)
        rows.append(_base_txrow(
            layer_addrs[step], layer_addrs[step + 1],
            ts, round(layer_amount, 4), "CHAIN_8", instance_id, block_off
        ))
        block_off += 1

    return InjectionResult("CHAIN_8", instance_id, pd.DataFrame(rows))


# ---------------------------------------------------------------------------
# Main injection driver
# ---------------------------------------------------------------------------

INJECTORS = {
    "CHAIN_1": inject_chain1_enumeration,
    "CHAIN_2": inject_chain2_history_extraction,
    "CHAIN_3": inject_chain3_async_flooding,
    "CHAIN_4": inject_chain4_agent_army,
    "CHAIN_5": inject_chain5_cross_platform_identity,
    "CHAIN_6": inject_chain6_behavioral_mimicry,
    "CHAIN_7": inject_chain7_swarm_intelligence,
    "CHAIN_8": inject_chain8_market_manipulation,
}

# How many instances of each chain to inject (configurable)
DEFAULT_INSTANCES_PER_CHAIN = {
    "CHAIN_1": 10,
    "CHAIN_2": 10,
    "CHAIN_3": 5,   # each instance = 500 transactions; 5 × 500 = 2,500
    "CHAIN_4": 10,
    "CHAIN_5": 10,
    "CHAIN_6": 8,
    "CHAIN_7": 8,   # each instance = 55 transactions
    "CHAIN_8": 8,
}


def inject_all_chains(
    real_transactions: pd.DataFrame,
    instances_per_chain: dict[str, int] | None = None,
    seed: int = 42,
) -> tuple[pd.DataFrame, dict]:
    """Inject all 8 attack chains into the real transaction stream.

    Args:
        real_transactions: The real Dune USDC transaction DataFrame.
        instances_per_chain: Override default instance counts per chain.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (mixed_dataset, summary_dict).
        mixed_dataset has all real rows plus injected rows (with extra label columns).
        summary_dict contains counts and metadata for the injection report.
    """
    rng = np.random.default_rng(seed)
    if instances_per_chain is None:
        instances_per_chain = DEFAULT_INSTANCES_PER_CHAIN.copy()

    # Add label columns to real data
    real_df = real_transactions.copy()
    real_df["is_injected"] = False
    real_df["attack_chain"] = ""
    real_df["attack_instance"] = ""
    real_df["attack_difficulty"] = ""

    # Sample anchor timestamps from real data range for injection windows
    ts_min = real_df["timestamp"].min()
    ts_max = real_df["timestamp"].max()
    ts_range_s = (ts_max - ts_min).total_seconds()

    all_injected: List[pd.DataFrame] = []
    summary: dict = {
        "real_transactions": len(real_df),
        "chains": {},
        "total_injected": 0,
        "injection_rate_pct": 0.0,
    }

    # Verify injected addresses don't collide with real addresses
    real_addresses = set(real_df["sender"].str.lower()).union(
        set(real_df["receiver"].str.lower())
    )

    for chain_id, n_instances in instances_per_chain.items():
        injector = INJECTORS[chain_id]
        chain_rows = []

        for inst_idx in range(n_instances):
            # Random anchor time within real data range
            offset_s = float(rng.uniform(3600, ts_range_s - 7200))  # keep away from edges
            base_time = ts_min + timedelta(seconds=offset_s)
            instance_id = f"{chain_id}_inst{inst_idx:03d}"

            result = injector(rng, base_time, instance_id)
            chain_rows.append(result.transactions)

        chain_df = pd.concat(chain_rows, ignore_index=True)

        # Verify no address collision
        injected_addrs = set(chain_df["sender"].str.lower()).union(
            set(chain_df["receiver"].str.lower())
        )
        collisions = injected_addrs & real_addresses
        if collisions:
            raise ValueError(
                f"{chain_id}: {len(collisions)} injected addresses collide with real data. "
                "This should not happen — check INJECTED_ADDR_PREFIX."
            )

        all_injected.append(chain_df)
        summary["chains"][chain_id] = {
            "instances": n_instances,
            "transactions": len(chain_df),
            "difficulty": CHAIN_DIFFICULTIES[chain_id],
            "unique_attacker_addresses": chain_df["sender"].nunique(),
        }
        summary["total_injected"] += len(chain_df)

    injected_df = pd.concat(all_injected, ignore_index=True)

    # Ensure timestamp timezone consistency
    if injected_df["timestamp"].dt.tz is None:
        injected_df["timestamp"] = injected_df["timestamp"].dt.tz_localize("UTC")

    # Merge real + injected, sort by timestamp
    mixed_df = pd.concat([real_df, injected_df], ignore_index=True)
    mixed_df = mixed_df.sort_values("timestamp").reset_index(drop=True)

    summary["injection_rate_pct"] = round(
        100.0 * summary["total_injected"] / len(mixed_df), 2
    )
    summary["total_transactions"] = len(mixed_df)

    return mixed_df, summary


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inject A2A attack patterns into real transaction stream (Phase 6 Plan 06-01)"
    )
    parser.add_argument(
        "--input",
        default="data/transactions_dune.parquet",
        help="Path to real transaction Parquet file",
    )
    parser.add_argument(
        "--output",
        default="data/attack_injection_dataset.parquet",
        help="Path to write mixed dataset Parquet",
    )
    parser.add_argument(
        "--summary",
        default="data/injection_summary.json",
        help="Path to write injection summary JSON",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[3]

    input_path = Path(args.input) if Path(args.input).is_absolute() else repo_root / args.input
    output_path = Path(args.output) if Path(args.output).is_absolute() else repo_root / args.output
    summary_path = Path(args.summary) if Path(args.summary).is_absolute() else repo_root / args.summary

    print(f"Loading real transactions from {input_path}...")
    real_df = pd.read_parquet(input_path)
    print(f"  Loaded {len(real_df):,} transactions")

    print("Injecting attack patterns...")
    mixed_df, summary = inject_all_chains(real_df, seed=args.seed)

    print(f"\nInjection summary:")
    print(f"  Real transactions:     {summary['real_transactions']:,}")
    print(f"  Injected transactions: {summary['total_injected']:,}")
    print(f"  Total:                 {summary['total_transactions']:,}")
    print(f"  Injection rate:        {summary['injection_rate_pct']:.2f}%")
    print()
    for chain_id, stats in summary["chains"].items():
        print(f"  {chain_id} ({stats['difficulty']:10s}): "
              f"{stats['instances']:2d} instances, "
              f"{stats['transactions']:5d} transactions, "
              f"{stats['unique_attacker_addresses']:3d} unique addresses")

    print(f"\nSaving mixed dataset to {output_path}...")
    mixed_df.to_parquet(output_path, index=False)

    print(f"Saving summary to {summary_path}...")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
