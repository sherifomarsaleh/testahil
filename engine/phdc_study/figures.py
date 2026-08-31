"""PHDC study figures.

House figure discipline: solid light canvas, zero transparency (asserted
programmatically at the end of this module), no label collisions, every figure
inspected as a rendered image before it ships.

Palette is fixed and ORDERED — slots are assigned in sequence, never cycled —
and was validated before use against the lightness band, chroma floor, adjacent
CVD separation, normal-vision floor and surface contrast. Sequential magnitude
uses one hue light-to-dark; categorical identity uses the four slots below.
Text stays in ink; a coloured mark beside it carries the identity.
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

CAT = ["#1D6FA3", "#B03A2E", "#7E4A94", "#4F7A21"]
INK, MUTED, FAINT = "#1A1D21", "#5B6570", "#9AA3AC"
RULE, CANVAS = "#DCE1E5", "#FCFCFB"
SEQ = LinearSegmentedColormap.from_list("phdc_seq", ["#EAF2F7", "#1D6FA3", "#0C3D5C"])

plt.rcParams.update({
    "figure.facecolor": CANVAS, "axes.facecolor": CANVAS, "savefig.facecolor": CANVAS,
    "savefig.transparent": False, "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": RULE, "axes.labelcolor": MUTED, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlecolor": INK,
    "axes.grid": True, "grid.color": "#EDF0F2", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
})


def _save(fig, name):
    p = os.path.join(HERE, name)
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor=CANVAS, transparent=False)
    plt.close(fig)
    return p


def fig1_football(bars, spot, prior):
    """The value of each lens as a range, against spot and the prior edition.

    A football field, because the job is comparing RANGES on one axis — not a
    point per case, which is the claim this study explicitly does not make.

    bars is a list of (label, low, high, mid_or_None, colour_index). Every
    number in it is COMPUTED by the caller from the published sensitivity grid,
    so the figure and the table beneath it cannot drift apart; the labels used
    to carry the conversion rates as typed text and would have kept printing
    the old rates after the model changed.
    """
    fig, ax = plt.subplots(figsize=(7.6, 3.5))
    n = len(bars)
    for i, (label, lo, hi, mid, ci) in enumerate(bars):
        y = n - 1 - i
        c = CAT[ci]
        if hi > lo:
            ax.barh(y, hi - lo, left=lo, height=0.42, color=c, zorder=3)
            if mid is not None:
                ax.plot([mid], [y], marker="|", ms=16, mew=2.2, color="#FFFFFF",
                        zorder=5)
            ax.text(lo - 0.6, y, "%.2f" % lo, va="center", ha="right",
                    fontsize=8.5, color=INK)
            ax.text(hi + 0.6, y, "%.2f" % hi, va="center", ha="left",
                    fontsize=8.5, color=INK)
        else:
            ax.plot([lo], [y], marker="D", ms=8, color=c, zorder=3)
            ax.text(lo + 1.1, y, "%.2f" % lo, va="center", ha="left",
                    fontsize=8.5, color=INK)
    # The close and the prior edition's base sit close together, so inline
    # labels on the two lines would overlap each other and whichever bar end
    # lands between them. Both are keyed once, in the empty upper-right.
    ax.axvline(spot, color=INK, lw=1.6, zorder=4)
    ax.axvline(prior, color=FAINT, lw=1.2, ls=(0, (4, 3)), zorder=2)
    xmax = max(max(b[2] for b in bars), spot) * 1.18
    ax.plot([xmax * 0.62], [n - 0.30], marker="|", ms=11, mew=1.6, color=INK)
    ax.text(xmax * 0.645, n - 0.30, "close %.2f (23 Aug 2026)" % spot,
            color=INK, fontsize=8.5, va="center", ha="left")
    ax.plot([xmax * 0.62], [n - 0.62], marker="|", ms=11, mew=1.4, color=FAINT)
    ax.text(xmax * 0.645, n - 0.62, "prior edition base %.2f" % prior,
            color=MUTED, fontsize=8.5, va="center", ha="left")
    ax.set_yticks(range(n))
    ax.set_yticklabels([b[0] for b in reversed(bars)], fontsize=8.5, color=INK)
    ax.set_xlabel("EGP per share")
    ax.set_title("Value across the range of the crux",
                 fontsize=10.5, pad=12, loc="left")
    ax.set_xlim(0, xmax)
    ax.set_ylim(-0.7, n - 0.02)
    ax.grid(axis="y", visible=False)
    return _save(fig, "fig1_football.png")


def fig2_sensitivity(waccs, cfos, grid, spot):
    """Value per share across the two axes that move it. Sequential, one hue."""
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    g = np.array(grid)
    im = ax.imshow(g, cmap=SEQ, aspect="auto", origin="lower")
    ax.set_xticks(range(len(waccs)))
    ax.set_xticklabels(["%.2f%%" % (w * 100) for w in waccs])
    ax.set_yticks(range(len(cfos)))
    ax.set_yticklabels(["%.1f%%" % (c * 100) for c in cfos])
    ax.set_xlabel("WACC")
    ax.set_ylabel("cash conversion (CFO / revenue)")
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            v = g[i, j]
            # contrast from the cell's ACTUAL colour, not from where the value
            # sits in the range — a midpoint rule puts white on mid-tones
            rgb = SEQ((v - g.min()) / (g.max() - g.min()))[:3]
            lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
            ax.text(j, i, "%.2f" % v, ha="center", va="center", fontsize=8.5,
                    color=INK if lum > 0.55 else "#FFFFFF",
                    fontweight="bold" if abs(v - spot) < 1.2 else "normal")
    ax.set_title("Fair value per share (EGP) — bold where the cell brackets the "
                 "EGP %.2f close" % spot, fontsize=10.5, pad=12, loc="left")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, pad=0.02)
    cb.set_label("EGP per share", color=MUTED)
    cb.outline.set_edgecolor(RULE)
    return _save(fig, "fig2_sensitivity.png")


def fig3_cone(dist, spot, touch):
    """The published probability cone. Bands, because the job is a distribution.

    Horizons are calendar months. The two keys used to be the retired
    session-counted names, which is why this figure could not be rebuilt from
    the current numbers file at all.
    """
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    xs = [0, 1, 3]
    p5 = [spot, dist["m1"]["p5"], dist["m3"]["p5"]]
    p25 = [spot, dist["m1"]["p25"], dist["m3"]["p25"]]
    p50 = [spot, dist["m1"]["p50"], dist["m3"]["p50"]]
    p75 = [spot, dist["m1"]["p75"], dist["m3"]["p75"]]
    p95 = [spot, dist["m1"]["p95"], dist["m3"]["p95"]]
    ax.fill_between(xs, p5, p95, color="#D7E6EF", zorder=1, label="5th–95th percentile")
    ax.fill_between(xs, p25, p75, color="#9CC2D8", zorder=2, label="25th–75th percentile")
    ax.plot(xs, p50, color=CAT[0], lw=2.0, zorder=3, label="median")
    ax.axhline(spot, color=INK, lw=1.1, ls=(0, (4, 3)), zorder=4)
    ax.text(0.06, spot + 0.18, "close %.2f" % spot, color=INK, fontsize=8.5,
            va="bottom", ha="left")
    for x in (1, 3):
        ax.axvline(x, color=RULE, lw=0.9, zorder=0)
    # percentile labels go BESIDE their vertical, not above and below it, so
    # they cannot collide with the axis tick labels or the plot edge
    for x, arr, ha, dx in ((1, "m1", "right", -0.06), (3, "m3", "left", 0.06)):
        ax.text(x + dx, dist[arr]["p95"], "%.2f" % dist[arr]["p95"],
                ha=ha, va="center", fontsize=8, color=MUTED)
        ax.text(x + dx, dist[arr]["p5"], "%.2f" % dist[arr]["p5"],
                ha=ha, va="center", fontsize=8, color=MUTED)
    ax.set_xticks(xs)
    ax.set_xticklabels(["today", "1 month", "3 months"])
    ax.set_ylabel("EGP per share")
    ax.set_title("Published price cone — the engine's distribution, not a forecast",
                 fontsize=10.5, pad=12, loc="left")
    ax.set_xlim(-0.08, 3.30)
    ax.set_ylim(min(p5) - 0.9, max(p95) + 0.9)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK)
    ax.grid(axis="x", visible=False)
    return _save(fig, "fig3_cone.png")


SHORT = {"PHDC": "Palm Hills", "TMGH": "Talaat Moustafa Group",
         "ORHD": "Orascom Development Egypt", "EMFD": "Emaar Misr",
         "OCDI": "SODIC", "HELI": "Heliopolis Housing",
         "PRDC": "Pioneers Properties"}


def fig4_peers(rows):
    """Peer betas, same procedure for every name, with the standard error shown."""
    rows = sorted([r for r in rows if "beta" in r], key=lambda r: r["beta"])
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ys = range(len(rows))
    cols = [CAT[1] if r["ticker"] == "PHDC" else "#B9C4CC" for r in rows]
    ax.barh(list(ys), [r["beta"] for r in rows], height=0.55, color=cols, zorder=3)
    ax.errorbar([r["beta"] for r in rows], list(ys),
                xerr=[r["se"] for r in rows], fmt="none",
                ecolor=MUTED, elinewidth=1.0, capsize=3, zorder=4)
    for i, r in enumerate(rows):
        ax.text(r["beta"] + r["se"] + 0.05, i, "%.2f" % r["beta"], va="center",
                fontsize=8.5, color=INK,
                fontweight="bold" if r["ticker"] == "PHDC" else "normal")
    ax.set_yticks(list(ys))
    ax.set_yticklabels(["%s  %s" % (r["ticker"], SHORT.get(r["ticker"], r["name"]))
                        for r in rows], fontsize=8.5, color=INK)
    ax.axvline(1.0, color=FAINT, lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.text(1.0, -0.72, "market", color=MUTED, fontsize=8, va="center", ha="center")
    ax.set_xlabel("beta vs EGX30, weekly, Dimson-adjusted (bars show ±1 standard error)")
    ax.set_title("Egyptian listed developers — every beta from the same procedure",
                 fontsize=10.5, pad=12, loc="left")
    ax.set_xlim(0, max(r["beta"] + r["se"] for r in rows) * 1.25)
    ax.set_ylim(-1.0, len(rows) - 0.4)
    ax.grid(axis="y", visible=False)
    return _save(fig, "fig4_peers.png")


def assert_opaque(paths):
    """Zero transparency, verified rather than asserted."""
    from PIL import Image
    bad = []
    for p in paths:
        im = Image.open(p)
        if im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255:
            bad.append(os.path.basename(p))
    if bad:
        raise AssertionError("figures carry transparency: %s" % bad)
    return True
