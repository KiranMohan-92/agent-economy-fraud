#!/usr/bin/env python3
"""Generate publication-quality figures for the A2A fraud detection paper.

Produces four PDF figures suitable for arXiv submission:
  1. fig_invariant_violations.pdf  -- heatmap of invariant violations per chain
  2. fig_validation_stages.pdf     -- grouped bar chart of validation metrics
  3. fig_chain_recall.pdf          -- horizontal bar chart of per-chain recall
  4. fig_signal_weights.pdf        -- radar chart of signal weights

Usage:
    python generate_figures.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.size": 10,
    "font.family": "serif",
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype": 42,       # TrueType fonts in PDF (better for arXiv)
    "ps.fonttype": 42,
})

OUTDIR = Path(__file__).resolve().parent

# Colorblind-safe palette (Tableau 10)
CB_PALETTE = plt.cm.tab10.colors

# ---------------------------------------------------------------------------
# Figure 1 -- Invariant-violation heatmap
# ---------------------------------------------------------------------------

def fig_invariant_violations():
    chains = [
        "CHAIN_1\nEnumeration",
        "CHAIN_2\nHistory Extract",
        "CHAIN_3\nAsync Flooding",
        "CHAIN_4\nAgent Army",
        "CHAIN_5\nCross-Platform",
        "CHAIN_6\nBehav. Mimicry",
        "CHAIN_7\nSwarm Intel.",
        "CHAIN_8\nMarket Manip.",
    ]
    invariants = [
        "I1\nVelocity",
        "I2\nIdentity",
        "I3\nMessage\nIntegrity",
        "I4\nAuth.\nScope",
        "I5\nCapability\nBound",
        "I6\nRate\nLimit",
        "I7\nInfo.\nBound",
        "I8\nValue\nConserv.",
        "I9\nBounded\nRational.",
    ]

    # Severity encoding: 0=NONE, 1=MODERATE, 2=SEVERE, 3=CATASTROPHIC
    data = np.zeros((8, 9), dtype=int)
    # CHAIN_1
    data[0, 5] = 2   # I6 SEVERE
    data[0, 6] = 1   # I7 MODERATE
    # CHAIN_2
    data[1, 6] = 2   # I7 SEVERE
    data[1, 8] = 1   # I9 MODERATE
    # CHAIN_3
    data[2, 0] = 3   # I1 CATASTROPHIC
    data[2, 2] = 3   # I3 CATASTROPHIC
    data[2, 7] = 2   # I8 SEVERE
    # CHAIN_4
    data[3, 5] = 3   # I6 CATASTROPHIC
    data[3, 1] = 2   # I2 SEVERE
    data[3, 4] = 2   # I5 SEVERE
    # CHAIN_5
    data[4, 3] = 2   # I4 SEVERE
    data[4, 4] = 2   # I5 SEVERE
    data[4, 5] = 1   # I6 MODERATE
    # CHAIN_6
    data[5, 6] = 3   # I7 CATASTROPHIC
    data[5, 7] = 2   # I8 SEVERE
    # CHAIN_7
    data[6, 0] = 2   # I1 SEVERE
    data[6, 5] = 2   # I6 SEVERE
    data[6, 7] = 3   # I8 CATASTROPHIC
    # CHAIN_8
    data[7, 7] = 3   # I8 CATASTROPHIC
    data[7, 8] = 2   # I9 SEVERE
    data[7, 0] = 1   # I1 MODERATE

    # Custom colormap: white -> yellow -> orange -> dark red
    cmap = mcolors.ListedColormap(["#ffffff", "#fee08b", "#f46d43", "#a50026"])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots(figsize=(7, 3.8))
    im = ax.imshow(data, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(9))
    ax.set_xticklabels(invariants, ha="center")
    ax.set_yticks(range(8))
    ax.set_yticklabels(chains, va="center")

    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Cell text annotations
    severity_labels = {0: "", 1: "MOD", 2: "SEV", 3: "CAT"}
    for i in range(8):
        for j in range(9):
            val = data[i, j]
            if val > 0:
                color = "white" if val == 3 else "black"
                ax.text(j, i, severity_labels[val], ha="center", va="center",
                        fontsize=7, fontweight="bold", color=color)

    # Grid
    ax.set_xticks(np.arange(9) - 0.5, minor=True)
    ax.set_yticks(np.arange(8) - 0.5, minor=True)
    ax.grid(which="minor", color="#cccccc", linewidth=0.5)
    ax.tick_params(which="minor", size=0)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3], shrink=0.8, pad=0.02)
    cbar.ax.set_yticklabels(["None", "Moderate", "Severe", "Catastrophic"],
                            fontsize=7)

    ax.set_title("Invariant Violations by Attack Chain", pad=50, fontsize=11)

    fig.savefig(OUTDIR / "fig_invariant_violations.pdf")
    plt.close(fig)
    print("  -> fig_invariant_violations.pdf")


# ---------------------------------------------------------------------------
# Figure 2 -- Validation-stage performance
# ---------------------------------------------------------------------------

def fig_validation_stages():
    metrics = ["Precision", "Recall", "F1-Score"]
    synthetic   = [82.36, 96.23, 88.71]
    real_clean  = [42.9,  81.1,  56.1]
    injection   = [87.5,  87.5,  77.7]   # Per-chain recall, recall, ROC-AUC

    x = np.arange(len(metrics))
    width = 0.22

    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    bars1 = ax.bar(x - width, synthetic,  width, label="Synthetic (Phase 4)",
                   color=CB_PALETTE[0], edgecolor="black", linewidth=0.4)
    bars2 = ax.bar(x,         real_clean, width, label="Real On-Chain (Phase 5)",
                   color=CB_PALETTE[1], edgecolor="black", linewidth=0.4)
    bars3 = ax.bar(x + width, injection,  width, label="Injection (Phase 6)",
                   color=CB_PALETTE[2], edgecolor="black", linewidth=0.4)

    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 105)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=7)

    # Value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 1.0,
                    f"{h:.1f}", ha="center", va="bottom", fontsize=6)

    ax.set_title("Detection Performance Across Validation Stages")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.savefig(OUTDIR / "fig_validation_stages.pdf")
    plt.close(fig)
    print("  -> fig_validation_stages.pdf")


# ---------------------------------------------------------------------------
# Figure 3 -- Per-chain recall
# ---------------------------------------------------------------------------

def fig_chain_recall():
    chains = [
        "CHAIN_1 (Enumeration)",
        "CHAIN_2 (History Extract)",
        "CHAIN_3 (Async Flooding)",
        "CHAIN_4 (Agent Army)",
        "CHAIN_5 (Cross-Platform)",
        "CHAIN_6 (Behav. Mimicry)",
        "CHAIN_7 (Swarm Intel.)",
        "CHAIN_8 (Market Manip.)",
    ]
    recall = [100, 100, 100, 100, 100, 100, 0, 100]

    # Difficulty colors (colorblind-friendly choices)
    diff_colors = {
        "EASY":       "#4daf4a",   # green
        "MEDIUM":     "#ffff33",   # yellow
        "HARD":       "#ff7f00",   # orange
        "IMPOSSIBLE": "#e41a1c",   # red
    }
    difficulties = [
        "EASY", "MEDIUM", "MEDIUM", "HARD",
        "IMPOSSIBLE", "IMPOSSIBLE", "IMPOSSIBLE", "IMPOSSIBLE",
    ]
    colors = [diff_colors[d] for d in difficulties]

    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    y_pos = np.arange(len(chains))

    bars = ax.barh(y_pos, recall, color=colors, edgecolor="black", linewidth=0.4,
                   height=0.6)

    # Hatch CHAIN_7 (index 6) to mark 0% distinctly
    bars[6].set_hatch("///")
    bars[6].set_edgecolor("black")
    bars[6].set_linewidth(0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(chains, fontsize=7)
    ax.set_xlabel("Recall (%)")
    ax.set_xlim(0, 115)
    ax.invert_yaxis()

    # Annotations
    for i, (r, d) in enumerate(zip(recall, difficulties)):
        label = f"{r}%" if r > 0 else "0% (undetected)"
        x_pos = r + 1.5 if r > 0 else 1.5
        ax.text(x_pos, i, label, va="center", fontsize=7)

    # Legend for difficulty levels
    import matplotlib.patches as mpatches
    legend_handles = [
        mpatches.Patch(facecolor=diff_colors["EASY"], edgecolor="black",
                       linewidth=0.4, label="Easy"),
        mpatches.Patch(facecolor=diff_colors["MEDIUM"], edgecolor="black",
                       linewidth=0.4, label="Medium"),
        mpatches.Patch(facecolor=diff_colors["HARD"], edgecolor="black",
                       linewidth=0.4, label="Hard"),
        mpatches.Patch(facecolor=diff_colors["IMPOSSIBLE"], edgecolor="black",
                       linewidth=0.4, label="Impossible"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=7,
              frameon=True, framealpha=0.9, title="Difficulty", title_fontsize=7)

    ax.set_title("Per-Chain Recall at Threshold 0.09")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.savefig(OUTDIR / "fig_chain_recall.pdf")
    plt.close(fig)
    print("  -> fig_chain_recall.pdf")


# ---------------------------------------------------------------------------
# Figure 4 -- Signal weights (radar chart)
# ---------------------------------------------------------------------------

def fig_signal_weights():
    labels = [
        "Network\nTopology",
        "Temporal\nConsistency",
        "Economic\nRationality",
        "Value\nFlow",
        "Cross-\nPlatform",
    ]
    values = [0.2739, 0.2505, 0.2424, 0.2332, 0.00]

    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()

    # Close the polygon
    values_closed = values + [values[0]]
    angles_closed = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw={"polar": True})

    ax.fill(angles_closed, values_closed, color=CB_PALETTE[0], alpha=0.25)
    ax.plot(angles_closed, values_closed, color=CB_PALETTE[0], linewidth=1.5,
            marker="o", markersize=4)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 0.32)
    ax.set_yticks([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    ax.set_yticklabels(["0.05", "0.10", "0.15", "0.20", "0.25", "0.30"],
                       fontsize=6, color="grey")
    ax.set_rlabel_position(30)

    # Annotate each point with its value
    for angle, val in zip(angles, values):
        ha = "center"
        offset = 0.025
        ax.text(angle, val + offset, f"{val:.4f}", ha=ha, va="bottom",
                fontsize=7, fontweight="bold")

    ax.set_title("Learned Signal Weights", y=1.08)
    ax.grid(color="#cccccc", linewidth=0.5)

    fig.savefig(OUTDIR / "fig_signal_weights.pdf")
    plt.close(fig)
    print("  -> fig_signal_weights.pdf")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating figures...")
    fig_invariant_violations()
    fig_validation_stages()
    fig_chain_recall()
    fig_signal_weights()
    print("Done. All figures saved to:", OUTDIR)
