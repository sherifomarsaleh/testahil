"""
Testahil — chart module. EFG teal / brass palette, study-ready PNGs at 200 dpi.
Fonts fall back to a clean sans here; the published studies render in IBM Plex Sans.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

TEAL = "#1B5E5E"; TEAL2 = "#2A8F8F"; BRASS = "#B0894B"
BAND50 = "#2A8F8F"; BAND90 = "#9FC8C8"; INK = "#222222"; GRID = "#D9E2E2"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "figure.dpi": 200,
})


def _pctl_curves(result, qs=(5, 25, 50, 75, 95)):
    days = np.arange(result.horizon + 1)
    curves = {q: np.percentile(result.paths, q, axis=0) for q in qs}
    return days, curves


def fan_chart(result, ax=None, title="Forward price cone"):
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
    days, c = _pctl_curves(result)
    ax.fill_between(days, c[5], c[95], color=BAND90, alpha=0.55, lw=0, label="5–95%")
    ax.fill_between(days, c[25], c[75], color=BAND50, alpha=0.45, lw=0, label="25–75%")
    ax.plot(days, c[50], color=TEAL, lw=2.2, label="Median")
    ax.axhline(result.anchor, color=BRASS, lw=1.3, ls="--", label=f"Anchor {result.anchor:.2f}")
    ax.set_xlim(0, result.horizon); ax.set_xlabel("Trading days forward"); ax.set_ylabel("Price (EGP)")
    ax.set_title(title, color=TEAL, fontweight="bold", loc="left")
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
    if own:
        fig.tight_layout(); return fig
    return ax


def bells(result, ax=None, horizons=None):
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
    if horizons is None:
        horizons = {"T+20": min(20, result.horizon), "T+60": result.horizon}
    cols = [TEAL2, TEAL]
    for i, ((label, day), col) in enumerate(zip(horizons.items(), cols)):
        v = result.paths[:, day]
        ax.hist(v, bins=80, density=True, color=col, alpha=0.45, lw=0)
        ax.axvline(np.median(v), color=col, lw=1.6, ls="-")
        yfrac = 0.92 - 0.08 * i
        ax.text(ax.get_xlim()[1]*0.98, ax.get_ylim()[1]*yfrac,
                f"{label} median {np.median(v):.0f}", color=col, fontsize=8,
                fontweight="bold", ha="right")
    ax.axvline(result.anchor, color=BRASS, lw=1.3, ls="--")
    ax.set_xlabel("Price (EGP)"); ax.set_ylabel("Density")
    ax.set_title("Terminal distributions", color=TEAL, fontweight="bold", loc="left")
    if own:
        fig.tight_layout(); return fig
    return ax


def touch_ladder(result, levels, by_day=None, ax=None):
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(7.2, 4.2))
    by_day = result.horizon if by_day is None else by_day
    levels = sorted(levels)
    probs = [100 * result.touch_probability(l, by_day) for l in levels]
    cols = [BRASS if l >= result.anchor else TEAL2 for l in levels]
    y = np.arange(len(levels))
    ax.barh(y, probs, color=cols, alpha=0.85)
    ax.set_yticks(y); ax.set_yticklabels([f"{l:.0f}" for l in levels])
    for yi, p in zip(y, probs):
        ax.text(p + 1, yi, f"{p:.0f}%", va="center", fontsize=8, color=INK)
    ax.set_xlim(0, 100); ax.set_xlabel("Touch probability by T+%d (%%)" % by_day)
    ax.set_ylabel("Level (EGP)")
    ax.set_title("Level-touch ladder", color=TEAL, fontweight="bold", loc="left")
    if own:
        fig.tight_layout(); return fig
    return ax


def study_panel(result, levels, path, ticker=""):
    fig = plt.figure(figsize=(12.5, 8.0))
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.22)
    fan_chart(result, ax=fig.add_subplot(gs[0, :]))
    bells(result, ax=fig.add_subplot(gs[1, 0]))
    touch_ladder(result, levels, ax=fig.add_subplot(gs[1, 1]))
    head = f"{ticker} — probabilistic study" if ticker else "Probabilistic study"
    fig.suptitle(head, color=TEAL, fontweight="bold", x=0.012, ha="left", fontsize=14)
    fig.text(0.012, 0.005, "Independent Valuation Study — Educational Analysis · distributions, not targets",
             color=BRASS, fontsize=8)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def scorecard_chart(agg, path):
    """Render the ledger aggregate: coverage bars + PIT histogram."""
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2))
    cov = [agg.get("coverage_50_band", 0)*100, agg.get("coverage_90_band", 0)*100]
    a.bar(["50% band", "90% band"], cov, color=[TEAL2, TEAL], alpha=0.85)
    a.axhline(50, color=BRASS, ls="--", lw=1); a.axhline(90, color=BRASS, ls="--", lw=1)
    for i, v in enumerate(cov):
        a.text(i, v+1, f"{v:.0f}%", ha="center", fontsize=9)
    a.set_ylim(0, 105); a.set_ylabel("Realized coverage (%)")
    a.set_title("Band coverage vs target", color=TEAL, fontweight="bold", loc="left")
    ph = agg.get("pit_hist", {})
    b.bar(range(len(ph)), list(ph.values()), color=TEAL2, alpha=0.8)
    b.set_xticks(range(len(ph))); b.set_xticklabels(list(ph.keys()), rotation=45, fontsize=7, ha="right")
    b.set_ylabel("Cohorts"); b.yaxis.set_major_locator(MaxNLocator(integer=True))
    b.set_title("PIT histogram (flat = calibrated)", color=TEAL, fontweight="bold", loc="left")
    fig.tight_layout(); fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)
    return path
