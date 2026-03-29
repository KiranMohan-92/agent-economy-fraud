"""
GPD Error Propagation: A2A Fincrime Detection Framework
========================================================
Monte Carlo uncertainty propagation through the 5-signal fusion pipeline.

Traces how 7 input uncertainty sources flow through to the final
detection metrics (Precision, Recall, F1, ROC-AUC).

Usage: python3 analysis/error_propagation.py

Output: .gpd/phases/05-ecosystem-characterization/ERROR-BUDGET.md
"""

import csv
import json
import math
import os
import sys
from pathlib import Path
from datetime import datetime

import numpy as np

# ─── Configuration ───────────────────────────────────────────
N_TRIALS = 10_000
SEED = 42
FLAG_THRESHOLD = 0.25

WEIGHTS = {
    "economic_rationality": 0.25,
    "network_topology": 0.25,
    "value_flow": 0.20,
    "temporal_consistency": 0.20,
    "cross_platform": 0.10,
}
SIGNAL_NAMES = list(WEIGHTS.keys())
WEIGHT_ARRAY = np.array([WEIGHTS[s] for s in SIGNAL_NAMES])

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / ".gpd" / "phases" / "05-ecosystem-characterization"


# ─── Load Data ───────────────────────────────────────────────
def load_data():
    """Load detection results and extract signal matrix + labels."""
    rows = []
    with open(DATA_DIR / "detection_results.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    n = len(rows)
    signals = np.zeros((n, len(SIGNAL_NAMES)))
    labels = np.zeros(n, dtype=int)  # 1=agent, 0=human

    for i, row in enumerate(rows):
        labels[i] = 1 if row["label"] == "agent" else 0
        for j, sig in enumerate(SIGNAL_NAMES):
            signals[i, j] = float(row[f"signal_{sig}"])

    return signals, labels, n


# ─── Metric Computation ─────────────────────────────────────
def compute_metrics(signals, labels, weights, threshold):
    """Compute composite scores and classification metrics."""
    w = weights / weights.sum()
    composites = signals @ w

    y_pred = (composites >= threshold).astype(int)
    y_true = labels

    tp = ((y_true == 1) & (y_pred == 1)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    tn = ((y_true == 0) & (y_pred == 0)).sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    # Manual AUC
    auc = manual_auc(composites, y_true)

    return {"precision": precision, "recall": recall, "f1": f1, "auc": auc}


def manual_auc(scores, labels):
    """Compute AUC via Mann-Whitney U statistic."""
    pos_scores = scores[labels == 1]
    neg_scores = scores[labels == 0]
    if len(pos_scores) == 0 or len(neg_scores) == 0:
        return 0.5
    u_sum = 0
    for ps in pos_scores:
        u_sum += (neg_scores < ps).sum() + 0.5 * (neg_scores == ps).sum()
    return u_sum / (len(pos_scores) * len(neg_scores))


# ─── Perturbation Functions ─────────────────────────────────
def perturb_bootstrap(signals, labels, rng):
    """U1: Bootstrap resample addresses."""
    n = len(labels)
    idx = rng.choice(n, size=n, replace=True)
    return signals[idx], labels[idx]


def perturb_label_noise(signals, labels, rng, noise_rate=0.05):
    """U2: Flip a fraction of agent labels to human."""
    noisy_labels = labels.copy()
    agent_idx = np.where(labels == 1)[0]
    n_flip = max(1, int(len(agent_idx) * noise_rate))
    flip_idx = rng.choice(agent_idx, size=n_flip, replace=False)
    noisy_labels[flip_idx] = 0
    return signals, noisy_labels


def perturb_human_noise(signals, labels, rng, sigma=0.05):
    """U3: Add Gaussian noise to synthetic human signal scores."""
    noisy_signals = signals.copy()
    human_idx = np.where(labels == 0)[0]
    noise = rng.normal(0, sigma, size=(len(human_idx), signals.shape[1]))
    noisy_signals[human_idx] = np.clip(noisy_signals[human_idx] + noise, 0, 1)
    return noisy_signals, labels


def perturb_weights(weights, rng, concentration=50):
    """U4: Dirichlet perturbation of signal weights."""
    alpha = concentration * weights
    alpha = np.maximum(alpha, 0.1)  # avoid zero alpha
    return rng.dirichlet(alpha)


def perturb_dead_signals(signals, labels, rng):
    """U6: Simulate activation of dead signals (Value Flow + Cross-Platform)."""
    activated = signals.copy()
    agent_idx = np.where(labels == 1)[0]
    human_idx = np.where(labels == 0)[0]

    # Value Flow (col 2): agents get U(0.2, 0.7), humans get U(0.0, 0.3)
    activated[agent_idx, 2] = rng.uniform(0.2, 0.7, size=len(agent_idx))
    activated[human_idx, 2] = rng.uniform(0.0, 0.3, size=len(human_idx))

    # Cross-Platform (col 4): agents get U(0.1, 0.5), humans get U(0.0, 0.1)
    activated[agent_idx, 4] = rng.uniform(0.1, 0.5, size=len(agent_idx))
    activated[human_idx, 4] = rng.uniform(0.0, 0.1, size=len(human_idx))

    return activated, labels


# ─── Run Monte Carlo ─────────────────────────────────────────
def run_source(name, perturb_fn, signals, labels, rng, n_trials=N_TRIALS):
    """Run MC trials for a single uncertainty source."""
    f1s = []
    precs = []
    recs = []
    aucs = []

    for _ in range(n_trials):
        s, l = perturb_fn(signals, labels, rng)
        m = compute_metrics(s, l, WEIGHT_ARRAY.copy(), FLAG_THRESHOLD)
        f1s.append(m["f1"])
        precs.append(m["precision"])
        recs.append(m["recall"])
        aucs.append(m["auc"])

    return {
        "name": name,
        "f1_mean": np.mean(f1s),
        "f1_std": np.std(f1s),
        "f1_ci_lo": np.percentile(f1s, 2.5),
        "f1_ci_hi": np.percentile(f1s, 97.5),
        "prec_mean": np.mean(precs),
        "prec_std": np.std(precs),
        "rec_mean": np.mean(recs),
        "rec_std": np.std(recs),
        "auc_mean": np.mean(aucs),
        "auc_std": np.std(aucs),
        "f1_var": np.var(f1s),
    }


def run_weight_sensitivity(signals, labels, rng, n_trials=N_TRIALS):
    """U4: Weight perturbation with Dirichlet."""
    f1s = []
    weight_samples = []

    for _ in range(n_trials):
        w = perturb_weights(WEIGHT_ARRAY, rng)
        m = compute_metrics(signals, labels, w, FLAG_THRESHOLD)
        f1s.append(m["f1"])
        weight_samples.append(w)

    weight_samples = np.array(weight_samples)
    f1s = np.array(f1s)

    # Per-weight sensitivity (correlation of weight_i with F1)
    sensitivities = {}
    for i, name in enumerate(SIGNAL_NAMES):
        corr = np.corrcoef(weight_samples[:, i], f1s)[0, 1]
        sensitivities[name] = corr

    return {
        "name": "U4: Signal weight sensitivity",
        "f1_mean": np.mean(f1s),
        "f1_std": np.std(f1s),
        "f1_ci_lo": np.percentile(f1s, 2.5),
        "f1_ci_hi": np.percentile(f1s, 97.5),
        "f1_var": np.var(f1s),
        "sensitivities": sensitivities,
        "prec_mean": 0, "prec_std": 0,
        "rec_mean": 0, "rec_std": 0,
        "auc_mean": 0, "auc_std": 0,
    }


def run_threshold_sweep(signals, labels):
    """U5: Deterministic threshold sweep."""
    thresholds = np.arange(0.10, 0.51, 0.01)
    results = []
    for t in thresholds:
        m = compute_metrics(signals, labels, WEIGHT_ARRAY.copy(), t)
        results.append({"threshold": round(t, 2), **m})
    return results


def run_joint(signals, labels, rng, n_trials=N_TRIALS):
    """U7: Joint perturbation — all sources simultaneously."""
    f1s = []
    for _ in range(n_trials):
        s, l = perturb_bootstrap(signals, labels, rng)
        s, l = perturb_label_noise(s, l, rng, noise_rate=0.05)
        s, l = perturb_human_noise(s, l, rng, sigma=0.05)
        w = perturb_weights(WEIGHT_ARRAY, rng, concentration=50)
        m = compute_metrics(s, l, w, FLAG_THRESHOLD)
        f1s.append(m["f1"])

    return {
        "name": "U7: Joint (all sources)",
        "f1_mean": np.mean(f1s),
        "f1_std": np.std(f1s),
        "f1_ci_lo": np.percentile(f1s, 2.5),
        "f1_ci_hi": np.percentile(f1s, 97.5),
        "f1_var": np.var(f1s),
        "prec_mean": 0, "prec_std": 0,
        "rec_mean": 0, "rec_std": 0,
        "auc_mean": 0, "auc_std": 0,
    }


# ─── Sensitivity Coefficients ────────────────────────────────
def compute_sensitivity_coefficients(signals, labels):
    """Finite-difference sensitivity of F1 to each weight."""
    base = compute_metrics(signals, labels, WEIGHT_ARRAY.copy(), FLAG_THRESHOLD)
    base_f1 = base["f1"]
    delta = 0.02

    coefficients = {}
    for i, name in enumerate(SIGNAL_NAMES):
        w_plus = WEIGHT_ARRAY.copy()
        w_minus = WEIGHT_ARRAY.copy()
        w_plus[i] += delta
        w_minus[i] -= delta

        f1_plus = compute_metrics(signals, labels, w_plus, FLAG_THRESHOLD)["f1"]
        f1_minus = compute_metrics(signals, labels, w_minus, FLAG_THRESHOLD)["f1"]

        df_dw = (f1_plus - f1_minus) / (2 * delta)
        S = (WEIGHT_ARRAY[i] / base_f1) * df_dw if base_f1 > 0 else 0
        coefficients[name] = {"df_dw": df_dw, "S": S, "weight": WEIGHT_ARRAY[i]}

    return coefficients, base_f1


# ─── Main ────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("GPD ERROR PROPAGATION: A2A Fincrime Detection Framework")
    print("=" * 70)

    signals, labels, n = load_data()
    rng = np.random.default_rng(SEED)

    print(f"Loaded: {n} addresses ({labels.sum()} agents, {(1-labels).sum()} humans)")
    print(f"Signals: {SIGNAL_NAMES}")
    print(f"Weights: {WEIGHT_ARRAY}")
    print(f"Threshold: {FLAG_THRESHOLD}")

    # Baseline metrics
    base = compute_metrics(signals, labels, WEIGHT_ARRAY.copy(), FLAG_THRESHOLD)
    print(f"\nBaseline: P={base['precision']:.3f} R={base['recall']:.3f} "
          f"F1={base['f1']:.3f} AUC={base['auc']:.3f}")

    # ── Run all uncertainty sources ──
    print(f"\nRunning {N_TRIALS} MC trials per source...")

    sources = []

    # U1: Bootstrap
    print("  U1: Bootstrap resampling...")
    u1 = run_source("U1: Sample (bootstrap)", perturb_bootstrap, signals, labels, rng)
    sources.append(u1)

    # U2: Label noise
    print("  U2: Label noise (5% flip)...")
    u2 = run_source("U2: Label noise (5%)", perturb_label_noise, signals, labels, rng)
    sources.append(u2)

    # U3: Human baseline noise
    print("  U3: Human baseline noise...")
    u3 = run_source("U3: Synthetic human noise", perturb_human_noise, signals, labels, rng)
    sources.append(u3)

    # U4: Weight sensitivity
    print("  U4: Weight sensitivity (Dirichlet)...")
    u4 = run_weight_sensitivity(signals, labels, rng)
    sources.append(u4)

    # U5: Threshold sweep (deterministic)
    print("  U5: Threshold sweep...")
    threshold_results = run_threshold_sweep(signals, labels)

    # U6: Dead signal activation
    print("  U6: Dead signal activation...")
    u6 = run_source("U6: Dead signal activation", perturb_dead_signals, signals, labels, rng)
    sources.append(u6)

    # U7: Joint
    print("  U7: Joint perturbation...")
    u7 = run_joint(signals, labels, rng)
    sources.append(u7)

    # ── Sensitivity coefficients ──
    print("\nComputing sensitivity coefficients...")
    sens_coeffs, base_f1 = compute_sensitivity_coefficients(signals, labels)

    # ── Rank sources by F1 variance contribution ──
    total_joint_var = u7["f1_var"]
    print(f"\n{'='*70}")
    print("ERROR BUDGET (ranked by F1 variance contribution)")
    print(f"{'='*70}")
    print(f"{'Source':<35} {'F1 Mean':>8} {'F1 Std':>8} {'F1 Var':>10} {'% of Joint':>10}")
    print("-" * 75)

    for s in sorted(sources[:-1], key=lambda x: -x["f1_var"]):
        pct = 100 * s["f1_var"] / total_joint_var if total_joint_var > 0 else 0
        print(f"{s['name']:<35} {s['f1_mean']:8.3f} {s['f1_std']:8.3f} "
              f"{s['f1_var']:10.6f} {pct:9.1f}%")

    print("-" * 75)
    print(f"{'U7: Joint (all sources)':<35} {u7['f1_mean']:8.3f} {u7['f1_std']:8.3f} "
          f"{u7['f1_var']:10.6f} {'100.0':>9}%")

    # ── Sensitivity coefficients ──
    print(f"\n{'='*70}")
    print("SENSITIVITY COEFFICIENTS (∂F1/∂w_i)")
    print(f"{'='*70}")
    print(f"{'Signal':<30} {'Weight':>8} {'∂F1/∂w':>10} {'S (dim-less)':>12}")
    print("-" * 65)
    for name in SIGNAL_NAMES:
        c = sens_coeffs[name]
        print(f"{name:<30} {c['weight']:8.2f} {c['df_dw']:10.4f} {c['S']:12.4f}")

    # ── Threshold sensitivity ──
    print(f"\n{'='*70}")
    print("THRESHOLD SENSITIVITY")
    print(f"{'='*70}")
    print(f"{'Threshold':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
    print("-" * 45)
    for t in threshold_results:
        marker = " ◄" if abs(t["threshold"] - FLAG_THRESHOLD) < 0.005 else ""
        print(f"{t['threshold']:10.2f} {t['precision']:10.3f} {t['recall']:10.3f} "
              f"{t['f1']:10.3f}{marker}")

    # ── Find optimal threshold ──
    best_t = max(threshold_results, key=lambda x: x["f1"])
    print(f"\nOptimal threshold for F1: {best_t['threshold']:.2f} "
          f"(F1={best_t['f1']:.3f}, P={best_t['precision']:.3f}, R={best_t['recall']:.3f})")
    print(f"Current threshold: {FLAG_THRESHOLD} (F1={base['f1']:.3f})")

    # ── Weight correlation analysis ──
    if "sensitivities" in u4:
        print(f"\n{'='*70}")
        print("WEIGHT-F1 CORRELATION (from Dirichlet MC)")
        print(f"{'='*70}")
        for name, corr in sorted(u4["sensitivities"].items(), key=lambda x: -abs(x[1])):
            direction = "↑" if corr > 0 else "↓"
            print(f"  {name:<30} r={corr:+.3f} {direction}")

    # ── Dominant source ──
    dominant = max(sources[:-1], key=lambda x: x["f1_var"])
    print(f"\n{'='*70}")
    print(f"DOMINANT ERROR SOURCE: {dominant['name']}")
    print(f"  F1 variance contribution: {dominant['f1_var']:.6f}")
    print(f"  F1 std: ±{dominant['f1_std']:.3f}")
    print(f"  95% CI: [{dominant['f1_ci_lo']:.3f}, {dominant['f1_ci_hi']:.3f}]")
    print(f"{'='*70}")

    # ── Generate ERROR-BUDGET.md ──
    generate_report(base, sources, threshold_results, sens_coeffs, u4, dominant, best_t)
    print(f"\nReport written to: {OUTPUT_DIR}/ERROR-BUDGET.md")


def generate_report(base, sources, threshold_results, sens_coeffs, u4, dominant, best_threshold):
    """Generate the ERROR-BUDGET.md report."""
    total_joint_var = sources[-1]["f1_var"]  # U7 is last
    now = datetime.now().strftime("%Y-%m-%d")

    lines = [
        "---",
        f"target: Detection F1 Score",
        f"phases: 1-5",
        f"date: {now}",
        f"dominant_source: {dominant['name']}",
        f"total_fractional_error: {sources[-1]['f1_std'] / base['f1']:.4f}" if base['f1'] > 0 else "total_fractional_error: N/A",
        "---",
        "",
        "# Error Budget: A2A Fincrime Detection Framework",
        "",
        f"**Target:** Detection metrics (Precision, Recall, F1, ROC-AUC)",
        f"**Baseline:** P={base['precision']:.3f}, R={base['recall']:.3f}, F1={base['f1']:.3f}, AUC={base['auc']:.3f}",
        f"**Method:** Monte Carlo perturbation ({N_TRIALS:,} trials per source)",
        f"**Date:** {now}",
        "",
        "## Derivation Chain",
        "",
        "```",
        "INPUTS (with uncertainty)             SIGNALS (5-signal fusion)        METRICS",
        "├─ 74 sampled agents (±10.9%)         ├─ Econ. Rationality (0.25) ✓    ├─ Precision ± δ",
        "├─ 100 synthetic humans               ├─ Network Topology  (0.25) ✓    ├─ Recall ± δ",
        "├─ ERC-8004 labels (~5% noise)        ├─ Value Flow        (0.20) ✗    ├─ F1 ± δ",
        "└─ Profile-based synthetic txns       ├─ Temporal Consist. (0.20) ~    └─ AUC ± δ",
        "                                      └─ Cross-Platform    (0.10) ✗",
        "```",
        "",
        "## Error Budget Table",
        "",
        "| # | Source | F1 Mean | F1 Std | F1 Variance | % of Joint Var |",
        "|---|--------|---------|--------|-------------|----------------|",
    ]

    for i, s in enumerate(sorted(sources[:-1], key=lambda x: -x["f1_var"]), 1):
        pct = 100 * s["f1_var"] / total_joint_var if total_joint_var > 0 else 0
        lines.append(
            f"| {i} | {s['name']} | {s['f1_mean']:.3f} | ±{s['f1_std']:.3f} | "
            f"{s['f1_var']:.6f} | **{pct:.1f}%** |"
        )

    lines.append(
        f"| — | **Joint (all sources)** | {sources[-1]['f1_mean']:.3f} | "
        f"±{sources[-1]['f1_std']:.3f} | {sources[-1]['f1_var']:.6f} | **100%** |"
    )

    lines.extend([
        "",
        f"**F1 with full uncertainty: {sources[-1]['f1_mean']:.3f} ± {sources[-1]['f1_std']:.3f} "
        f"(95% CI: [{sources[-1]['f1_ci_lo']:.3f}, {sources[-1]['f1_ci_hi']:.3f}])**",
        "",
        "## Dominant Error Source",
        "",
        f"**{dominant['name']}** contributes the most variance to F1.",
        "",
        f"- F1 std from this source alone: ±{dominant['f1_std']:.3f}",
        f"- 95% CI: [{dominant['f1_ci_lo']:.3f}, {dominant['f1_ci_hi']:.3f}]",
        "",
    ])

    # Sensitivity coefficients
    lines.extend([
        "## Sensitivity Coefficients",
        "",
        "| Signal | Weight | ∂F1/∂w | S (dimensionless) |",
        "|--------|--------|--------|-------------------|",
    ])
    for name in SIGNAL_NAMES:
        c = sens_coeffs[name]
        lines.append(f"| {name} | {c['weight']:.2f} | {c['df_dw']:+.4f} | {c['S']:+.4f} |")

    # Weight-F1 correlation
    if "sensitivities" in u4:
        lines.extend([
            "",
            "## Weight-F1 Correlation (Dirichlet MC)",
            "",
            "| Signal | Correlation with F1 | Interpretation |",
            "|--------|---------------------|----------------|",
        ])
        for name, corr in sorted(u4["sensitivities"].items(), key=lambda x: -abs(x[1])):
            interp = "More weight → higher F1" if corr > 0.1 else "More weight → lower F1" if corr < -0.1 else "Minimal effect"
            lines.append(f"| {name} | {corr:+.3f} | {interp} |")

    # Threshold sensitivity
    lines.extend([
        "",
        "## Threshold Sensitivity",
        "",
        "| Threshold | Precision | Recall | F1 |",
        "|-----------|-----------|--------|-----|",
    ])
    for t in threshold_results:
        marker = " ◄ current" if abs(t["threshold"] - FLAG_THRESHOLD) < 0.005 else ""
        marker2 = " ◄ optimal" if abs(t["threshold"] - best_threshold["threshold"]) < 0.005 and marker == "" else ""
        lines.append(
            f"| {t['threshold']:.2f}{marker}{marker2} | {t['precision']:.3f} | "
            f"{t['recall']:.3f} | {t['f1']:.3f} |"
        )

    lines.extend([
        "",
        f"**Optimal threshold:** {best_threshold['threshold']:.2f} "
        f"(F1={best_threshold['f1']:.3f}, P={best_threshold['precision']:.3f}, "
        f"R={best_threshold['recall']:.3f})",
        f"**Current threshold:** {FLAG_THRESHOLD} (F1={base['f1']:.3f})",
        "",
    ])

    # Recommendations
    lines.extend([
        "## Recommendations",
        "",
        f"1. **Fix dominant error source ({dominant['name']})** — this would most reduce F1 uncertainty",
        f"2. **Activate dead signals** — Value Flow and Cross-Platform carry 30% of designed weight but contribute zero discrimination",
        f"3. **Optimize threshold** — if {best_threshold['threshold']:.2f} outperforms {FLAG_THRESHOLD}, "
        f"consider adjusting (F1 gain: {best_threshold['f1'] - base['f1']:+.3f})",
        f"4. **Replace synthetic humans** — real on-chain human baseline would reduce U3 uncertainty",
        f"5. **Increase sample size** — more than 74 successful queries would tighten bootstrap CIs",
        "",
        "---",
        "",
        f"_Generated by analysis/error_propagation.py on {now}_",
        f"_Monte Carlo trials: {N_TRIALS:,} per source, seed={SEED}_",
    ])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "ERROR-BUDGET.md", "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    main()
