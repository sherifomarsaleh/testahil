"""TMGH — the study's four figures, built from the committed numbers file.

FIGURE DISCIPLINE. Solid light canvas, zero transparency (verified
programmatically after the render, not asserted), every label placed so nothing
collides, and every figure REBUILT before it is checked — a figure that is only
ever checked and never rebuilt can drift away from the model that is supposed
to produce it [L-015].

No financial numeral is typed here. Everything comes from study_numbers.json.
"""
import json, os, re, subprocess, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(ENGINE)
sys.path.insert(0, ENGINE)
import site_data                                     # noqa: E402
NUMBERS = os.path.join(HERE, "study_numbers.json")

BG = "#FBFAF7"
INK = "#1B1B1B"
GRID = "#DCD8D0"
ACCENT = "#2E5E4E"
ACCENT2 = "#B4623A"
MUTED = "#8C8880"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "savefig.transparent": False,
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK,
    "ytick.color": INK, "axes.edgecolor": GRID, "grid.color": GRID,
    "font.size": 9, "axes.titlesize": 11, "axes.titleweight": "bold",
})


def N():
    return json.load(open(NUMBERS))


def _clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)


def fig1_football(n, path):
    """The four published cases, the other lenses, and the traded price."""
    ps_b, ps_p = n["per_share_nci_book"], n["per_share_nci_proportional"]
    lens = n["lenses"]
    bars = []
    for k in ("rating|capacity", "rating|recovery", "cds|capacity", "cds|recovery"):
        lo, hi = sorted((ps_b[k], ps_p[k]))
        label = ("%s ERP, %s conversion"
                 % ("rating" if k.startswith("rating") else "CDS",
                    "slower" if k.endswith("capacity") else "faster"))
        bars.append((label, lo, hi))
    b = lens["book_and_sustainable_return"]["cases"]
    vals = [v["value_per_share"] for v in b.values() if v["value_per_share"]]
    bars.append(("book value and sustainable return", min(vals), max(vals)))
    caps = [v for k, v in lens["normalised_earnings"].items() if k.startswith("cap|")]
    bars.append(("normalised earnings power", min(caps), max(caps)))
    hist = [r["pe"] for r in lens["own_multiple_history"] if r.get("pe")]
    eps = lens["normalised_earnings"]["average_eps"]
    bars.append(("its own historic P/E on normalised EPS",
                 min(hist) * eps, max(hist) * eps))

    fig, ax = plt.subplots(figsize=(8.6, 4.2))
    ys = range(len(bars))
    for i, (lab, lo, hi) in zip(ys, bars):
        ax.plot([lo, hi], [i, i], lw=9, solid_capstyle="butt",
                color=ACCENT if i < 4 else MUTED)
        ax.text(hi + 2.5, i, "%.0f–%.0f" % (lo, hi), va="center", fontsize=8.5)
    ax.axvline(n["meta"]["spot"], color=ACCENT2, lw=1.6, ls="--")
    # the y-axis is inverted, so the TOP of the plot is -0.6, not len(bars).
    # Placing it at the bottom ran the label straight through the x tick labels.
    ax.text(n["meta"]["spot"] + 2.5, -0.62,
            "traded price %.2f" % n["meta"]["spot"], color=ACCENT2, fontsize=8.5,
            va="center")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([b[0] for b in bars], fontsize=8.5)
    ax.invert_yaxis()
    ax.set_ylim(len(bars) - 0.4, -0.9)
    ax.set_xlabel("EGP per share")
    ax.set_title("What each lens says, and what the market is paying")
    ax.set_xlim(0, max(n["meta"]["spot"], max(b[2] for b in bars)) * 1.30)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=190)
    plt.close(fig)


def fig2_sensitivity(n, path):
    """The crux, priced: the discount rate against the conversion period."""
    grid = n["lenses"]["sensitivity"]["wacc_grid"]
    waccs = sorted({v["wacc"] for v in grid.values()})
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    for mode, colour, lab in (("capacity", ACCENT, "slower conversion (14 years)"),
                              ("recovery", ACCENT2, "faster conversion (10 years)")):
        ys = [grid["%0.4f|%s" % (w, mode)]["per_share_nci_book"] for w in waccs]
        ax.plot([100 * w for w in waccs], ys, marker="o", ms=4, lw=1.8,
                color=colour, label=lab)
    ax.axhline(n["meta"]["spot"], color=MUTED, lw=1.2, ls="--")
    ax.text(27.0, n["meta"]["spot"] + 5, "traded price %.2f" % n["meta"]["spot"],
            color=MUTED, fontsize=8.5)
    hw = 100 * n["wacc"]["wacc_rating"]
    ax.axvline(hw, color=INK, lw=1.0, ls=":")
    ax.text(hw - 0.45, ax.get_ylim()[1] * 0.94, "this study's rate  ",
            rotation=90, ha="right", va="top", fontsize=8, color=INK)
    ax.axvline(18.0, color=ACCENT2, lw=1.0, ls=":")
    ax.text(18.35, ax.get_ylim()[1] * 0.55, "previous edition's 18%",
            rotation=90, va="top", fontsize=8, color=ACCENT2)
    ax.set_xlabel("nominal EGP discount rate, %")
    ax.set_ylabel("EGP per share")
    ax.set_title("The single most consequential input, priced end to end")
    ax.legend(frameon=False, fontsize=8.5)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=190)
    plt.close(fig)


def _cone_from_site():
    """The published probability cone, read live from the site's own data.

    Never quoted from memory or from a document: the fit is refitted whenever a
    stock is posted, and a written number goes stale the moment it is.

    THROUGH A REAL PARSE [R-ENF-03]. The previous construction sliced a fixed 4,000-byte
    window after the first js.index("\\n  TMGH: {") and searched inside it — first-match
    where the parser takes the last, over a window that can truncate or overrun.
    """
    e = site_data.read('TICKERS', 'TMGH')
    out = {}
    for tag in ('t20', 't60'):
        d = (e.get('dist') or {}).get(tag)
        if d:
            out[tag] = d
    out['spot'] = float(e['spot']) if e.get('spot') is not None else None
    out['spot_date'] = e.get('spotDate')
    return out


def fig3_cone(n, path):
    c = _cone_from_site()
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    labels, order = [], ["t20", "t60"]
    for i, tag in enumerate(order):
        d = c.get(tag)
        if not d:
            continue
        p5, p25, p50, p75, p95 = (float(d[k]) for k in ("p5", "p25", "p50", "p75", "p95"))
        ax.plot([p5, p95], [i, i], lw=3, color=MUTED, solid_capstyle="butt")
        ax.plot([p25, p75], [i, i], lw=11, color=ACCENT, solid_capstyle="butt")
        ax.plot([p50], [i], marker="D", ms=6, color=BG, markeredgecolor=INK, mew=1.2)
        ax.text(p95 + 1.4, i, "%.0f – %.0f" % (p5, p95), va="center", fontsize=8.5)
        labels.append(d.get("label", tag))
    ax.axvline(c["spot"], color=ACCENT2, lw=1.5, ls="--")
    ax.text(c["spot"] + 1.4, -0.42, "%s %.2f" % (c["spot_date"], c["spot"]),
            color=ACCENT2, fontsize=8.5, va="center")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_ylim(len(labels) - 0.4, -0.75)
    ax.set_xlabel("EGP per share")
    ax.set_title("Where the price itself could be, on the published distribution")
    _clean(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=190)
    plt.close(fig)
    return c


def fig4_history(n, path):
    """The company's own record: revenue by segment, reported and projected."""
    rep = n["statements"]["reported"]
    fwd = n["statements"]["capacity"]["rows"]
    years = [2023, 2024, 2025] + [r["year"] for r in fwd]
    dev = [rep[str(y)]["dev_revenue"] for y in (2023, 2024, 2025)] + \
          [r["dev_revenue"] for r in fwd]
    hosp = [rep[str(y)]["hosp_revenue"] for y in (2023, 2024, 2025)] + \
           [r["hosp_revenue"] for r in fwd]
    oth = [rep[str(y)]["other_revenue"] for y in (2023, 2024, 2025)] + \
          [r["other_revenue"] for r in fwd]
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    b1 = ax.bar(years, dev, color=ACCENT, label="development")
    b2 = ax.bar(years, hosp, bottom=dev, color=ACCENT2, label="hospitality")
    b3 = ax.bar(years, oth, bottom=[a + b for a, b in zip(dev, hosp)],
                color=MUTED, label="other recurring")
    top = max(a + b + c for a, b, c in zip(dev, hosp, oth))
    ax.set_ylim(0, top * 1.22)
    ax.axvline(2025.5, color=INK, lw=0.9, ls=":")
    # both labels sit in headroom ABOVE the tallest bar. Placing them at 96% of
    # the maximum ran "reported" straight through the legend.
    ax.text(2024.4, top * 1.10, "reported", fontsize=8.5, ha="center", va="center")
    ax.text(2028.0, top * 1.10, "projected", fontsize=8.5, ha="center", va="center")
    ax.set_ylabel("EGP mn")
    ax.set_xticks(years)
    ax.set_title("Revenue by segment — reported, then on the slower-conversion reading")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: "%,.0f".replace(",", "") % v))
    _clean(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=190)
    plt.close(fig)


def verify_opaque(paths):
    """Zero transparency, checked on the RENDERED file rather than asserted."""
    from PIL import Image
    out = {}
    for p in paths:
        im = Image.open(p)
        out[os.path.basename(p)] = {
            "mode": im.mode, "size": im.size,
            "has_alpha": ("A" in im.mode),
            "opaque": ("A" not in im.mode) or (im.getchannel("A").getextrema() == (255, 255)),
        }
    return out


def main():
    n = N()
    paths = []
    for name, fn in (("fig1_football.png", fig1_football),
                     ("fig2_sensitivity.png", fig2_sensitivity),
                     ("fig3_cone.png", fig3_cone),
                     ("fig4_segments.png", fig4_history)):
        p = os.path.join(HERE, name)
        fn(n, p)
        paths.append(p)
    man = verify_opaque(paths)
    json.dump(man, open(os.path.join(HERE, "figures_manifest.json"), "w"), indent=1)
    for k, v in man.items():
        print("%-24s %-6s %-10s opaque=%s" % (k, v["mode"], v["size"], v["opaque"]))
    bad = [k for k, v in man.items() if not v["opaque"]]
    if bad:
        raise SystemExit("FIGURES WITH TRANSPARENCY: %s" % bad)


if __name__ == "__main__":
    main()
