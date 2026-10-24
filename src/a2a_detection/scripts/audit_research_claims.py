"""Deterministic local audit of research metric and data-lineage artifacts.

The script reproduces historical arithmetic where possible while keeping the
validity boundary machine-readable. It does not convert registry proxies,
unknown counterparties, or self-generated motifs into verified outcome data.

By default the audit is read-only and prints stable JSON. Use ``--output`` to
write that JSON and ``--strict`` to return a non-zero status when an artifact is
missing, stale, or construct-invalid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Callable

import pandas as pd
from sklearn.metrics import roc_auc_score

from a2a_detection.signals.label_cleaner import (
    COUNTERPARTY_UNKNOWN_LABEL,
    REGISTRY_OWNER_PROXY_LABEL,
)

AUDIT_SCHEMA_VERSION = 1
DEFAULT_REFERENCE_THRESHOLD = 0.09


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source(path: Path) -> dict:
    return {"file": path.name, "sha256": _sha256(path)}


def _read_frame(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix == ".json":
        return pd.read_json(path)
    raise ValueError(f"unsupported artifact format: {path.suffix}")


def _safe_auc(labels: pd.Series, scores: pd.Series) -> float | None:
    if labels.nunique() != 2:
        return None
    return float(roc_auc_score(labels.astype(int), scores.astype(float)))


def audit_stage2_metrics(
    scores_path: str | Path,
    labels_path: str | Path,
    reference_threshold: float = DEFAULT_REFERENCE_THRESHOLD,
) -> dict:
    """Audit Stage-2 arithmetic without endorsing its historical label names."""
    scores_path = Path(scores_path)
    labels_path = Path(labels_path)
    scores = _read_frame(scores_path)
    labels = _read_frame(labels_path)
    required_scores = {"address", "composite_score"}
    required_labels = {"address", "label"}
    if not required_scores.issubset(scores.columns):
        raise ValueError(f"scores missing columns: {sorted(required_scores - set(scores.columns))}")
    if not required_labels.issubset(labels.columns):
        raise ValueError(f"labels missing columns: {sorted(required_labels - set(labels.columns))}")

    scores = scores.copy()
    labels = labels.copy()
    scores["address"] = scores["address"].astype(str).str.lower()
    labels["address"] = labels["address"].astype(str).str.lower()
    if scores["address"].duplicated().any() or labels["address"].duplicated().any():
        raise ValueError("Stage-2 address artifacts must contain one row per address")

    merged = scores.merge(labels[["address", "label"]], on="address", how="inner")
    observed = set(merged["label"].dropna().astype(str).unique())
    explicit = {REGISTRY_OWNER_PROXY_LABEL, COUNTERPARTY_UNKNOWN_LABEL}
    legacy = {"agent", "human"}
    if explicit.issubset(observed) and observed.issubset(explicit):
        status = "descriptive_proxy_comparison_only"
        positive_label = REGISTRY_OWNER_PROXY_LABEL
        comparison_label = COUNTERPARTY_UNKNOWN_LABEL
        legacy_semantics = False
    elif legacy.issubset(observed) and observed.issubset(legacy):
        status = "invalid_legacy_label_semantics"
        positive_label = "agent"
        comparison_label = "human"
        legacy_semantics = True
    else:
        return {
            "status": "invalid_unsupported_label_schema",
            "observed_labels": sorted(observed),
            "fraud_ground_truth_available": False,
            "verified_human_negative_class_available": False,
            "valid_for_operational_claims": False,
            "sources": [_source(scores_path), _source(labels_path)],
        }

    cohort = merged[merged["label"].isin({positive_label, comparison_label})].copy()
    y_proxy = (cohort["label"] == positive_label).astype(int)
    score = cohort["composite_score"].astype(float)
    above = score >= reference_threshold
    proxy_mask = y_proxy.astype(bool)
    comparison_mask = ~proxy_mask

    per_signal_auc: dict[str, float | None] = {}
    for column in sorted(c for c in cohort.columns if c.startswith("signal_")):
        per_signal_auc[column.removeprefix("signal_")] = _safe_auc(
            y_proxy, cohort[column]
        )

    result = {
        "status": status,
        "construct": "registry_owner_proxy_vs_counterparty_comparison",
        "reference_threshold": float(reference_threshold),
        "reference_threshold_is_operational": False,
        "addresses_scored": int(len(scores)),
        "labels_available": int(len(labels)),
        "addresses_evaluated": int(len(cohort)),
        "unmatched_score_rows": int(len(scores) - len(merged)),
        "unmatched_label_rows": int(len(labels) - len(merged)),
        "registry_proxy_rows": int(proxy_mask.sum()),
        "counterparty_comparison_rows": int(comparison_mask.sum()),
        "registry_proxy_above_reference_rate": round(
            float(above[proxy_mask].mean()) if proxy_mask.any() else 0.0, 8
        ),
        "counterparty_above_reference_rate": round(
            float(above[comparison_mask].mean()) if comparison_mask.any() else 0.0,
            8,
        ),
        "composite_proxy_rank_auc": _safe_auc(y_proxy, score),
        "per_signal_proxy_rank_auc": per_signal_auc,
        "fraud_ground_truth_available": False,
        "verified_human_negative_class_available": False,
        "valid_for_operational_claims": False,
        "sources": [_source(scores_path), _source(labels_path)],
    }

    if legacy_semantics:
        tp = int((above & proxy_mask).sum())
        fn = int((~above & proxy_mask).sum())
        fp = int((above & comparison_mask).sum())
        tn = int((~above & comparison_mask).sum())
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        fpr = fp / (fp + tn) if fp + tn else 0.0
        result["historical_metric_reproduction"] = {
            "warning": (
                "Arithmetic only: historical agent/human names do not establish "
                "outcome truth or a verified negative class."
            ),
            "tp": tp,
            "fn": fn,
            "fp": fp,
            "tn": tn,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "fpr": fpr,
            "roc_auc": _safe_auc(y_proxy, score),
            "valid_for_operational_claims": False,
        }
    return result


def audit_event_identity(raw_transactions_path: str | Path) -> dict:
    """Quantify event loss from transaction-hash-only deduplication."""
    path = Path(raw_transactions_path)
    frame = _read_frame(path)
    hash_column = next(
        (column for column in ("evt_tx_hash", "tx_hash") if column in frame.columns),
        None,
    )
    if hash_column is None:
        raise ValueError("raw transactions missing evt_tx_hash/tx_hash")

    rows = int(len(frame))
    unique_hashes = int(frame[hash_column].nunique(dropna=False))
    exact_duplicates = int(frame.duplicated().sum())
    base = {
        "rows": rows,
        "unique_transaction_hashes": unique_hashes,
        "historical_hash_only_rows_discarded": rows - unique_hashes,
        "exact_duplicate_rows": exact_duplicates,
        "source": _source(path),
    }
    event_column = next(
        (column for column in ("evt_index", "event_index") if column in frame.columns),
        None,
    )
    if event_column is None:
        tuple_columns = [
            column
            for column in (
                hash_column,
                "chain",
                "evt_block_number",
                "block_number",
                "evt_block_time",
                "block_time",
                "timestamp",
                "sender",
                "receiver",
                "amount_usdc",
            )
            if column in frame.columns
        ]
        distinct_tuples = int(frame.drop_duplicates(subset=tuple_columns).shape[0])
        return {
            **base,
            "status": "invalid_missing_event_index",
            "event_identity_available": False,
            "safe_event_dedupe_possible": False,
            "distinct_observed_event_tuples": distinct_tuples,
            "minimum_distinct_events_lost_by_hash_dedupe": max(
                0, distinct_tuples - unique_hashes
            ),
        }

    identity = [hash_column, event_column]
    if "chain" in frame.columns:
        identity.insert(0, "chain")
    identity_frame = frame[identity]
    blank_identity = identity_frame.apply(
        lambda column: column.map(lambda value: isinstance(value, str) and not value.strip())
    )
    # Null or whitespace-only identity values are both unusable event keys.
    null_identity_rows = int((identity_frame.isna() | blank_identity).any(axis=1).sum())
    duplicate_identity = frame[frame.duplicated(identity, keep=False)]
    conflicting = 0
    if not duplicate_identity.empty:
        distinct_rows = duplicate_identity.drop_duplicates()
        conflicting = int(
            distinct_rows.loc[
                distinct_rows.duplicated(identity, keep=False), identity
            ]
            .drop_duplicates()
            .shape[0]
        )
    valid = null_identity_rows == 0 and conflicting == 0
    return {
        **base,
        "status": "valid_event_identity" if valid else "invalid_conflicting_event_identity",
        "event_identity_available": True,
        "safe_event_dedupe_possible": valid,
        "event_identity_columns": identity,
        "null_event_identity_rows": null_identity_rows,
        "conflicting_event_identities": conflicting,
        "rows_after_event_identity_dedupe": int(frame.drop_duplicates(identity).shape[0]),
    }


def audit_injection_sender_uniqueness(injection_path: str | Path) -> dict:
    """Detect sender reuse that collapses nominal motif instances."""
    path = Path(injection_path)
    frame = _read_frame(path)
    required = {"sender", "is_injected", "attack_chain", "attack_instance"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"injection artifact missing columns: {missing}")
    injected_mask = (
        frame["is_injected"]
        if pd.api.types.is_bool_dtype(frame["is_injected"])
        else frame["is_injected"].astype(str).str.lower().isin({"true", "1", "yes"})
    )
    injected = frame[injected_mask].copy()
    pairs = injected[["sender", "attack_instance"]].drop_duplicates()
    sender_instance_counts = pairs.groupby("sender")["attack_instance"].nunique()
    reused = int((sender_instance_counts > 1).sum())

    chains: dict[str, dict] = {}
    for chain_id in sorted(injected["attack_chain"].dropna().astype(str).unique()):
        chain = injected[injected["attack_chain"].astype(str) == chain_id]
        chain_pairs = chain[["sender", "attack_instance"]].drop_duplicates()
        chain_reused = int(
            (chain_pairs.groupby("sender")["attack_instance"].nunique() > 1).sum()
        )
        chains[chain_id] = {
            "rows": int(len(chain)),
            "instances": int(chain["attack_instance"].nunique()),
            "unique_senders": int(chain["sender"].nunique()),
            "unique_sender_instance_pairs": int(len(chain_pairs)),
            "senders_reused_across_instances": chain_reused,
            "instance_specific_sender_identity": chain_reused == 0,
        }

    status = "invalid_pseudoreplication" if reused else "descriptive_self_generated_only"
    return {
        "status": status,
        "injected_rows": int(len(injected)),
        "attack_instances": int(injected["attack_instance"].nunique()),
        "unique_senders": int(injected["sender"].nunique()),
        "unique_sender_instance_pairs": int(len(pairs)),
        "senders_reused_across_instances": reused,
        "independent_attack_population_established": False,
        "external_validity_established": False,
        "outcome_ground_truth_available": False,
        "chains": chains,
        "source": _source(path),
    }


def _safe_section(name: str, function: Callable[[], dict]) -> dict:
    try:
        return function()
    except FileNotFoundError as exc:
        return {"status": "missing_artifact", "section": name, "error": str(exc)}
    except Exception as exc:
        return {"status": "invalid_artifact", "section": name, "error": str(exc)}


def run_audit(
    scores_path: str | Path,
    labels_path: str | Path,
    raw_transactions_path: str | Path,
    injection_path: str | Path,
    reference_threshold: float = DEFAULT_REFERENCE_THRESHOLD,
) -> dict:
    """Run all deterministic audit sections."""
    stage2 = _safe_section(
        "stage2",
        lambda: audit_stage2_metrics(scores_path, labels_path, reference_threshold),
    )
    event_identity = _safe_section(
        "event_identity", lambda: audit_event_identity(raw_transactions_path)
    )
    injection = _safe_section(
        "injection_sender_uniqueness",
        lambda: audit_injection_sender_uniqueness(injection_path),
    )
    sections = {
        "stage2": stage2,
        "event_identity": event_identity,
        "injection_sender_uniqueness": injection,
    }
    invalid = any(
        str(section.get("status", "")).startswith(("invalid", "missing"))
        for section in sections.values()
    )
    return {
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "deterministic_output": True,
        "overall_status": "invalid_or_stale_artifacts" if invalid else "descriptive_only",
        "valid_for_operational_claims": False,
        "claims_not_established": [
            "verified outcome detection",
            "verified human-negative error rates",
            "independent attack robustness",
            "production action thresholds",
        ],
        "sections": sections,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", default="data/detection_results_dune.csv")
    parser.add_argument("--labels", default="data/labels_dune.parquet")
    parser.add_argument("--raw-transactions", default="data/dune_agent_transactions.csv")
    parser.add_argument("--injection", default="data/attack_injection_dataset.parquet")
    parser.add_argument(
        "--reference-threshold", type=float, default=DEFAULT_REFERENCE_THRESHOLD
    )
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when any section is invalid, stale, or missing",
    )
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[3]

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else repo_root / path

    audit = run_audit(
        resolve(args.scores),
        resolve(args.labels),
        resolve(args.raw_transactions),
        resolve(args.injection),
        args.reference_threshold,
    )
    rendered = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if args.output:
        output = resolve(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    if args.strict and audit["overall_status"] == "invalid_or_stale_artifacts":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
