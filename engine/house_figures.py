"""
Testahil — house figures. White canvas, teal / gold / brass palette. All charts the study needs:
fan chart (with percentile callouts), the two distribution figures, the touch-probability ladder,
the Step 0 PIT histogram, and the technical MA-stack. Matplotlib (Agg), saved as PNG.
"""
from __future__ import annotations
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEAL = "#0f766e"; TEAL_L = "#5eaaa2"; GOLD = "#d4af37"; BRASS = "#b08d57"
INK = "#1a1a1a"; GRID = "#e8e8e8"; BAND = "#0f766e"

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#cccccc", "axes.grid": True, "grid.color": GRID,
    "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
})


def fan_chart(result, levels, path, ticker=""):
    p = result.paths
    days = np.arange(p.shape[1])
    q = {k: np.percentile(p, k, axis=0) for k in (5, 25, 50, 75, 95)}
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(days, q[5], q[95], color=BAND, alpha=0.10, label="5–95% (90%)")
    ax.fill_between(days, q[25], q[75], color=BAND, alpha=0.28, label="25–75% (50% IQR)")
    ax.plot(days, q[50], color=TEAL, lw=2.2, label="Median")
    ax.axhline(result.anchor, color=INK, lw=1, ls="--", alpha=0.6)
    ax.text(0, result.anchor, f"  spot {result.anchor:.2f}", va="bottom", fontsize=9, color=INK)
    for lv in levels:
        ax.axhline(lv, color=BRASS, lw=0.8, ls=":", alpha=0.7)
    # percentile callouts at T+20 and T+60
    for d in (min(20, result.horizon), result.horizon):
        for k, col in ((95, TEAL_L), (75, TEAL), (50, INK), (25, TEAL), (5, TEAL_L)):
            ax.annotate(f"{q[k][d]:.0f}", (d, q[k][d]), fontsize=7.5, color=col,
                        xytext=(3, 0), textcoords="offset points", va="center")
    ax.set_title(f"{ticker} — Monte Carlo forward cone (T+{result.horizon})")
    ax.set_xlabel("Trading days ahead"); ax.set_ylabel("Price")
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
    return path


def dist_figs(result, path):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for ax, d, name in ((axes[0], min(20, result.horizon), "T+20"), (axes[1], result.horizon, "T+60")):
        col = result.paths[:, d]
        ax.hist(col, bins=60, color=TEAL, alpha=0.75, edgecolor="white", linewidth=0.3)
        for k, c, ls in ((50, GOLD, "-"), (25, BRASS, "--"), (75, BRASS, "--")):
            ax.axvline(np.percentile(col, k), color=c, ls=ls, lw=1.4)
        ax.axvline(result.anchor, color=INK, ls=":", lw=1.2)
        ax.set_title(f"Terminal price distribution — {name}")
        ax.set_xlabel("Price"); ax.set_yticks([])
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
    return path


def touch_ladder(result, levels, path):
    labels, probs = [], []
    for lv in levels:
        labels.append(f"{lv:.0f}")
        probs.append(result.touch_probability(lv, result.horizon))
    fig, ax = plt.subplots(figsize=(7, 0.5 * len(levels) + 1.5))
    y = np.arange(len(levels))
    ax.barh(y, probs, color=[GOLD if lv >= result.anchor else BRASS for lv in levels], alpha=0.85)
    for yi, pr in zip(y, probs):
        ax.text(pr + 0.01, yi, f"{pr:.0%}", va="center", fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlim(0, 1); ax.set_xlabel(f"P(touch by T+{result.horizon})")
    ax.set_title("Level-touch ladder"); ax.grid(axis="y", visible=False)
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
    return path


def pit_hist(pit, path):
    pit = np.asarray(pit, float)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(pit, bins=10, range=(0, 1), color=TEAL, alpha=0.8, edgecolor="white")
    ax.axhline(len(pit) / 10, color=GOLD, ls="--", lw=1.6, label="uniform (calibrated)")
    ax.set_title("Step 0 — PIT histogram (calibration diagnostic)")
    ax.set_xlabel("PIT"); ax.set_ylabel("count"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
    return path


def ma_stack(closes, path, ticker=""):
    c = np.asarray(closes, float)
    x = np.arange(len(c))[-260:]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.plot(x, c[-260:], color=INK, lw=1.6, label="Close")
    for win, col in ((20, GOLD), (50, BRASS), (100, TEAL_L), (200, TEAL)):
        if len(c) >= win:
            ma = np.convolve(c, np.ones(win) / win, mode="valid")
            ax.plot(x[-len(ma[-260:]):], ma[-260:], color=col, lw=1.2, label=f"SMA{win}")
    ax.set_title(f"{ticker} — price vs moving-average stack (last 260 sessions)")
    ax.set_xlabel("Session"); ax.set_ylabel("Price"); ax.legend(fontsize=8, ncol=3)
    fig.tight_layout(); fig.savefig(path, dpi=140); plt.close(fig)
    return path
