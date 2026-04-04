"""Precision Validation Script -- On-Chain Data Re-Scoring.

Re-scores all labeled addresses against real Dune transaction data using
the current signal configuration and reports before/after metrics.

This script implements the full validation pipeline:
    1. Load transactions (transactions_dune.parquet) and labels (labels_dune.parquet)
    2. Clean negative labels via EOA filter (if RPC configured) + activity filter
    3. Re-score all labeled addresses using SignalFusion
    4. Save results to data/detection_results_dune.csv
    5. Print a side-by-side before/after metrics comparison

Usage:
    python -m a2a_detection.scripts.validate_precision

    # With RPC for EOA contract filtering:
    RPC_URL=https://mainnet.base.org python -m a2a_detection.scripts.validate_precision

    # Custom activity threshold:
    MIN_TX_COUNT=10 python -m a2a_detection.scripts.validate_precision

Output:
    - data/detection_results_dune.csv (updated scores)
    - Printed metrics table to stdout
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("validate-precision")


# -- Baseline snapshot (recorded before code changes, 2026-04-04) ------------
BASELINE = {
    "precision": 0.2757,
    "recall":    0.9544,
    "f1":        0.4278,
    "roc_auc":   0.5900,
    "n_evaluated": 2134,
    "n_positive":   548,
    "n_negative":  1586,
    "tp": 523, "fp": 1374, "fn": 25, "tn": 212,
    "threshold": 0.08,
    "weights": {
        "economic_rationality": 0.30,
        "network_topology":     0.25,
        "value_flow":           0.25,
        "temporal_consistency": 0.20,
    },
    "label_cleaning": "none",
    "value_flow_subweights": "imbalance=0.40, velocity=0.30, layering=0.30",
}


def compute_metrics(
    y_true: pd.Series,
    y_score: pd.Series,
    threshold: float,
) -> dict:
    """Compute precision, recall, F1, AUC and confusion matrix."""
    y_pred = (y_score >= threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, int(y_true.sum()))

    metrics = {
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall":    float(recall_score(y_true, y_pred, zero_division=0)),
        "f1":        float(f1_score(y_true, y_pred, zero_division=0)),
        "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
    }
    try:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_score))
    except ValueError:
        metrics["roc_auc"] = None

    return metrics


def print_comparison(baseline: dict, updated: dict, label_stats: dict) -> None:
    """Print a formatted before/after comparison table."""
    def fmt(v, pct=False):
        if v is None:
            return "N/A"
        return f"{v*100:.2f}%" if pct else f"{v:.4f}"

    lines = [
        "",
        "=" * 68,
        "  PRECISION VALIDATION -- BEFORE vs AFTER",
        "=" * 68,
        f"  {'Metric':<28} {'BEFORE':>10}  {'AFTER':>10}  {'Delta':>8}",
        "-" * 68,
    ]

    metric_rows = [
        ("Precision",    "precision",  True),
        ("Recall",       "recall",     True),
        ("F1 Score",     "f1",         True),
        ("ROC-AUC",      "roc_auc",    False),
        ("True Positives",  "tp",      False),
        ("False Positives", "fp",      False),
        ("False Negatives", "fn",      False),
        ("True Negatives",  "tn",      False),
    ]

    for label, key, is_pct in metric_rows:
        b = baseline.get(key)
        u = updated.get(key)
        if b is None or u is None:
            delta = "N/A"
        elif is_pct:
            delta = f"{(u - b)*100:+.2f}pp"
        else:
            delta = f"{u - b:+d}" if isinstance(u, int) else f"{u - b:+.4f}"

        bstr = fmt(b, is_pct) if isinstance(b, float) else str(b) if b is not None else "N/A"
        ustr = fmt(u, is_pct) if isinstance(u, float) else str(u) if u is not None else "N/A"
        lines.append(f"  {label:<28} {bstr:>10}  {ustr:>10}  {delta:>8}")

    lines += [
        "-" * 68,
        f"  {'N evaluated':<28} {baseline.get('n_evaluated', '?'):>10}  {updated.get('n_evaluated', '?'):>10}",
        f"  {'  Agents (positive)':<28} {baseline.get('n_positive', '?'):>10}  {updated.get('n_positive', '?'):>10}",
        f"  {'  Humans (negative)':<28} {baseline.get('n_negative', '?'):>10}  {updated.get('n_negative', '?'):>10}",
        "-" * 68,
        "  CHANGES APPLIED",
        "-" * 68,
        f"  Threshold:    {baseline['threshold']} -> {updated.get('threshold', '?')}",
        f"  Label cleaning: {baseline['label_cleaning']} -> {updated.get('label_cleaning', '?')}",
        f"  Value flow:   {baseline['value_flow_subweights']}",
        f"              -> {updated.get('value_flow_subweights', '?')}",
        "  Weights (before -> after):",
    ]
    for sig, old_w in baseline["weights"].items():
        new_w = updated.get("weights", {}).get(sig, "?")
        lines.append(f"    {sig:<30} {old_w:.4f} -> {new_w:.4f}")

    if label_stats:
        lines += [
            "-" * 68,
            "  LABEL CLEANING STATS",
            "-" * 68,
        ]
        act = label_stats.get("activity_filter", {})
        eoa = label_stats.get("eoa_filter", {})
        if eoa.get("eoa_filter_applied"):
            lines.append(f"  EOA contracts removed: {eoa.get('contracts_removed', 0)}")
        else:
            lines.append(f"  EOA filter: skipped ({eoa.get('reason', 'no RPC')})")
        lines.append(
            f"  Thin counterparties removed: {act.get('thin_counterparties_removed', 0)}"
            f" / {act.get('human_labels_before', 0)}"
            f" ({act.get('pct_removed', 0)}%)"
            f" [threshold: <{act.get('min_tx_count_threshold', '?')} txs]"
        )

    lines += ["=" * 68, ""]
    print("\n".join(lines))


def main() -> None:
    # -- Load data ------------------------------------------------------------
    txns_path   = DATA_DIR / "transactions_dune.parquet"
    labels_path = DATA_DIR / "labels_dune.parquet"
    results_path = DATA_DIR / "detection_results_dune.csv"

    if not txns_path.exists():
        logger.error(f"Transactions not found: {txns_path}")
        sys.exit(1)
    if not labels_path.exists():
        logger.error(f"Labels not found: {labels_path}")
        sys.exit(1)

    logger.info("Loading transaction data...")
    txns = pd.read_parquet(txns_path)
    txns["sender"]   = txns["sender"].str.lower()
    txns["receiver"] = txns["receiver"].str.lower()
    logger.info(f"Loaded {len(txns):,} transactions")

    logger.info("Loading labels...")
    labels = pd.read_parquet(labels_path)
    labels["address"] = labels["address"].str.lower()
    logger.info(
        f"Loaded {len(labels):,} labels -- "
        f"{(labels['label']=='agent').sum()} agents, "
        f"{(labels['label']=='human').sum()} humans"
    )

    # -- Clean labels ---------------------------------------------------------
    from a2a_detection.signals.label_cleaner import clean_labels

    min_tx_count = int(os.environ.get("MIN_TX_COUNT", "5"))
    rpc_url      = os.environ.get("RPC_URL") or os.environ.get("BASE_RPC_URL")

    logger.info(f"Cleaning labels (min_tx_count={min_tx_count}, rpc={'yes' if rpc_url else 'no'})...")
    labels_clean, label_stats = clean_labels(
        labels, txns,
        rpc_url=rpc_url,
        min_tx_count=min_tx_count,
    )
    logger.info(
        f"Labels after cleaning: {len(labels_clean):,} "
        f"({(labels_clean['label']=='agent').sum()} agents, "
        f"{(labels_clean['label']=='human').sum()} humans)"
    )

    # -- Score addresses -------------------------------------------------------
    from a2a_detection.signals.fusion import SignalFusion

    fusion = SignalFusion()
    logger.info(
        f"Scoring with weights: "
        + ", ".join(f"{k}={v:.4f}" for k, v in fusion.weights.items() if v > 0)
    )
    logger.info(f"FLAG threshold: {fusion.THRESHOLD_FLAG}")

    # Score only addresses that appear in cleaned labels
    addresses_to_score = labels_clean["address"].unique().tolist()
    logger.info(f"Scoring {len(addresses_to_score):,} unique addresses...")

    results_df = fusion.score_batch(addresses_to_score, txns)
    results_df["address"] = results_df["address"].str.lower()

    # Save updated results
    results_df.to_csv(results_path, index=False)
    logger.info(f"Results saved to {results_path}")

    # -- Evaluate --------------------------------------------------------------
    merged = results_df.merge(
        labels_clean[["address", "label"]], on="address", how="inner"
    )
    logger.info(f"Evaluation set: {len(merged):,} addresses after merge")

    y_true  = (merged["label"] == "agent").astype(int)
    y_score = merged["composite_score"]

    updated_metrics = compute_metrics(y_true, y_score, fusion.THRESHOLD_FLAG)
    updated_metrics.update({
        "n_evaluated": len(merged),
        "n_positive":  int(y_true.sum()),
        "n_negative":  int((~y_true.astype(bool)).sum()),
        "threshold":   fusion.THRESHOLD_FLAG,
        "label_cleaning": f"min_{min_tx_count}_txs" + ("+eoa" if label_stats.get("eoa_filter", {}).get("eoa_filter_applied") else ""),
        "value_flow_subweights": "velocity=0.50, layering=0.50 (imbalance removed)",
        "weights": {k: v for k, v in fusion.weights.items() if v > 0},
    })

    # -- Individual signal AUCs ------------------------------------------------
    logger.info("\n--- Individual Signal AUCs (updated) ---")
    for sig in ["signal_economic_rationality", "signal_network_topology",
                "signal_value_flow", "signal_temporal_consistency"]:
        try:
            auc = roc_auc_score(y_true, merged[sig])
            logger.info(f"  {sig}: AUC={auc:.4f}")
        except Exception:
            pass

    # -- Print comparison ------------------------------------------------------
    print_comparison(BASELINE, updated_metrics, label_stats)

    # Also save metrics as JSON for traceability
    metrics_out = {
        "baseline": BASELINE,
        "updated": updated_metrics,
        "label_cleaning_stats": label_stats,
    }
    metrics_path = DATA_DIR / "validation_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics_out, f, indent=2, default=str)
    logger.info(f"Metrics saved to {metrics_path}")


if __name__ == "__main__":
    main()
