"""Synthetic transaction-motif sensitivity study.

The module keeps its historical filename for import compatibility. It scores
hand-authored injected transaction motifs and compares them with real,
unlabeled addresses. The comparison is a code-path stress test only: it has no
verified negative class and cannot establish deployment error rates, outcome
detection, or robustness to independent attacks.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from a2a_detection.signals.fusion import SignalFusion

STUDY_TYPE = "synthetic_transaction_motif_sensitivity"
DEFAULT_REFERENCE_THRESHOLD = SignalFusion.HISTORICAL_REFERENCE_THRESHOLD


def _required_columns(frame: pd.DataFrame, required: set[str], name: str) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")


def _as_bool(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    return series.astype(str).str.lower().isin({"true", "1", "yes"})


def score_dataset(
    mixed_df: pd.DataFrame,
    reference_threshold: float = DEFAULT_REFERENCE_THRESHOLD,
) -> pd.DataFrame:
    """Score synthetic motif senders and real unlabeled participants.

    ``reference_threshold`` is a historical descriptive reference. It is not a
    calibrated action threshold.
    """
    _required_columns(
        mixed_df,
        {"sender", "receiver", "is_injected", "attack_chain"},
        "mixed dataset",
    )
    frame = mixed_df.copy()
    frame["is_injected"] = _as_bool(frame["is_injected"])
    if "attack_difficulty" not in frame.columns:
        frame["attack_difficulty"] = ""
    if "attack_instance" not in frame.columns:
        frame["attack_instance"] = ""

    injected = frame[frame["is_injected"]]
    real = frame[~frame["is_injected"]]
    if injected.empty:
        raise ValueError("mixed dataset contains no injected transaction motifs")

    motif_addresses = (
        injected.groupby("sender", sort=True)
        .agg(
            attack_chain=("attack_chain", "first"),
            attack_difficulty=("attack_difficulty", "first"),
            attack_instance_count=("attack_instance", "nunique"),
            injected_transaction_count=("sender", "size"),
        )
        .reset_index()
        .rename(columns={"sender": "address"})
    )
    motif_addresses["synthetic_motif"] = True
    motif_addresses["cohort"] = "synthetic_motif_sender"

    motif_set = set(motif_addresses["address"])
    real_addresses = sorted(
        {
            address
            for address in set(real["sender"]) | set(real["receiver"])
            if pd.notna(address) and address not in motif_set
        }
    )
    unlabeled = pd.DataFrame(
        {
            "address": real_addresses,
            "attack_chain": "",
            "attack_difficulty": "",
            "attack_instance_count": 0,
            "injected_transaction_count": 0,
            "synthetic_motif": False,
            "cohort": "real_unlabeled",
        }
    )
    addresses = pd.concat([motif_addresses, unlabeled], ignore_index=True)
    addresses = addresses.sort_values(["synthetic_motif", "address"], ascending=[False, True])

    print(
        "  Addresses to score: "
        f"{len(addresses):,} ({len(motif_addresses):,} synthetic motif senders, "
        f"{len(unlabeled):,} real unlabeled)"
    )
    fusion = SignalFusion()
    rows: list[dict] = []
    for item in addresses.itertuples(index=False):
        result = fusion.score_address(item.address, frame)
        record = result.to_dict()
        record.pop("above_historical_reference", None)
        record.update(
            {
                "cohort": item.cohort,
                "synthetic_motif": bool(item.synthetic_motif),
                "attack_chain": item.attack_chain,
                "attack_difficulty": item.attack_difficulty,
                "attack_instance_count": int(item.attack_instance_count),
                "injected_transaction_count": int(item.injected_transaction_count),
                "above_reference": result.composite_score >= reference_threshold,
                "reference_threshold": float(reference_threshold),
            }
        )
        rows.append(record)
    return pd.DataFrame(rows)


def compute_metrics(
    scores_df: pd.DataFrame,
    reference_threshold: float | None = None,
    *,
    threshold: float | None = None,
) -> dict:
    """Compute descriptive motif sensitivity and unlabeled alert rate.

    ``threshold`` is accepted as a compatibility alias. Neither argument is an
    operational calibration.
    """
    if reference_threshold is not None and threshold is not None:
        raise ValueError("provide reference_threshold or threshold, not both")
    if reference_threshold is None:
        reference_threshold = (
            DEFAULT_REFERENCE_THRESHOLD if threshold is None else float(threshold)
        )
    _required_columns(scores_df, {"composite_score", "attack_chain"}, "scores")

    work = scores_df.copy()
    if "synthetic_motif" in work.columns:
        work["synthetic_motif"] = _as_bool(work["synthetic_motif"])
    elif "is_injected" in work.columns:
        work["synthetic_motif"] = _as_bool(work["is_injected"])
    else:
        raise ValueError("scores missing synthetic_motif/is_injected cohort marker")
    if "attack_difficulty" not in work.columns:
        work["attack_difficulty"] = ""
    work["above_reference"] = work["composite_score"] >= reference_threshold

    motif = work[work["synthetic_motif"]]
    unlabeled = work[~work["synthetic_motif"]]
    motif_above = int(motif["above_reference"].sum())
    unlabeled_above = int(unlabeled["above_reference"].sum())
    sensitivity = motif_above / len(motif) if len(motif) else 0.0
    alert_rate = unlabeled_above / len(unlabeled) if len(unlabeled) else 0.0

    rank_auc: float | None = None
    if len(motif) and len(unlabeled):
        rank_auc = float(
            roc_auc_score(
                work["synthetic_motif"].astype(int),
                work["composite_score"],
            )
        )

    per_chain: dict[str, dict] = {}
    for chain_id in sorted(motif["attack_chain"].dropna().astype(str).unique()):
        chain = motif[motif["attack_chain"].astype(str) == chain_id]
        above = int(chain["above_reference"].sum())
        per_chain[chain_id] = {
            "generator_difficulty": str(chain["attack_difficulty"].iloc[0]),
            "synthetic_senders_scored": int(len(chain)),
            "above_reference": above,
            "below_reference": int(len(chain) - above),
            "motif_sensitivity": round(above / len(chain), 4) if len(chain) else 0.0,
        }

    return {
        "study_type": STUDY_TYPE,
        "reference_threshold": float(reference_threshold),
        "reference_threshold_is_operational": False,
        "synthetic_motif_senders": int(len(motif)),
        "real_unlabeled_addresses": int(len(unlabeled)),
        "synthetic_motif_above_reference": motif_above,
        "real_unlabeled_above_reference": unlabeled_above,
        "motif_sensitivity": round(sensitivity, 4),
        "unlabeled_alert_rate": round(alert_rate, 4),
        "synthetic_vs_unlabeled_rank_auc": (
            round(rank_auc, 4) if rank_auc is not None else None
        ),
        "negative_ground_truth_available": False,
        "operational_claims_valid": False,
        "per_chain": per_chain,
    }


def threshold_sweep(
    scores_df: pd.DataFrame,
    lo: float = 0.01,
    hi: float = 0.60,
    step: float = 0.01,
) -> list[dict]:
    """Describe sensitivity/alert-rate tradeoffs over reference values."""
    if step <= 0 or hi < lo:
        raise ValueError("invalid sweep bounds")
    return [
        compute_metrics(scores_df, reference_threshold=round(float(value), 8))
        for value in np.arange(lo, hi + step / 2, step)
    ]


def write_report(
    metrics: dict,
    sweep: list[dict],
    reference_point: dict | None,
    output_path: str,
) -> None:
    """Write a bounded, non-operational Markdown sensitivity report."""
    del reference_point  # retained only for call-signature compatibility
    chain_rows = "\n".join(
        "| {chain} | {count} | {above} | {sensitivity:.1f}% |".format(
            chain=chain,
            count=values["synthetic_senders_scored"],
            above=values["above_reference"],
            sensitivity=values["motif_sensitivity"] * 100,
        )
        for chain, values in sorted(metrics["per_chain"].items())
    )
    if not chain_rows:
        chain_rows = "| (none) | 0 | 0 | 0.0% |"

    sweep_rows = "\n".join(
        "| {reference:.2f} | {sensitivity:.1f}% | {alert_rate:.1f}% |".format(
            reference=item["reference_threshold"],
            sensitivity=item["motif_sensitivity"] * 100,
            alert_rate=item["unlabeled_alert_rate"] * 100,
        )
        for item in sweep
    )
    if not sweep_rows:
        sweep_rows = "| (not run) | - | - |"

    auc = metrics["synthetic_vs_unlabeled_rank_auc"]
    auc_text = "not available" if auc is None else f"{auc:.3f}"
    report = f"""# Synthetic Transaction-Motif Sensitivity

This is a deterministic code-path stress test using hand-authored transaction
motifs. The real-address comparison cohort is unlabeled. The study does not
establish outcome error rates, independent-attack performance, or deployment
readiness.

## Descriptive summary

| Measure | Value |
|---|---:|
| Historical reference value | {metrics['reference_threshold']:.2f} |
| Synthetic motif senders | {metrics['synthetic_motif_senders']:,} |
| Real unlabeled addresses | {metrics['real_unlabeled_addresses']:,} |
| Motif sensitivity | {metrics['motif_sensitivity'] * 100:.1f}% |
| Unlabeled alert rate | {metrics['unlabeled_alert_rate'] * 100:.1f}% |
| Synthetic-vs-unlabeled rank AUC | {auc_text} |

The reference value is historical and non-operational. The unlabeled alert
rate is not an error rate because the comparison addresses have no verified
outcome labels.

## Per-motif-family sensitivity

| Motif family | Synthetic senders | Above reference | Sensitivity |
|---|---:|---:|---:|
{chain_rows}

## Reference sweep

| Reference | Motif sensitivity | Unlabeled alert rate |
|---:|---:|---:|
{sweep_rows}

## Validity boundary

1. Motifs were authored by the same project that implements the score.
2. Real addresses are unlabeled and may include automated or anomalous actors.
3. Generator difficulty tags are metadata, not independently measured levels.
4. No action policy or production decision should be derived from this study.
"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Descriptive sensitivity study for synthetic transaction motifs"
    )
    parser.add_argument("--input", default="data/attack_injection_dataset.parquet")
    parser.add_argument("--output", default="data/motif_sensitivity_results.parquet")
    parser.add_argument("--report", default="data/motif_sensitivity_report.md")
    parser.add_argument("--metrics", default="data/motif_sensitivity_metrics.json")
    parser.add_argument(
        "--reference-threshold",
        "--threshold",
        dest="reference_threshold",
        type=float,
        default=DEFAULT_REFERENCE_THRESHOLD,
        help="Historical descriptive reference; not an action threshold",
    )
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[3]

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else repo_root / path

    input_path = resolve(args.input)
    output_path = resolve(args.output)
    report_path = resolve(args.report)
    metrics_path = resolve(args.metrics)

    print(f"Loading mixed motif dataset from {input_path}...")
    mixed = pd.read_parquet(input_path)
    scores = score_dataset(mixed, reference_threshold=args.reference_threshold)
    metrics = compute_metrics(scores, reference_threshold=args.reference_threshold)
    sweep = threshold_sweep(scores)

    print(f"  Motif sensitivity: {metrics['motif_sensitivity'] * 100:.1f}%")
    print(f"  Unlabeled alert rate: {metrics['unlabeled_alert_rate'] * 100:.1f}%")
    print("  Valid for operational claims: no")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    scores.to_parquet(output_path, index=False)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(
        json.dumps(
            {"primary_reference": metrics, "reference_sweep": sweep},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    write_report(metrics, sweep, None, str(report_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
