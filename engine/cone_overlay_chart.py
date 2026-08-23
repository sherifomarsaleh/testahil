"""cone_overlay_chart.py — every graded name's published cone on ONE chart, in per cent.

WHAT THIS DRAWS
---------------
The fourteen instruments that carry at least one GRADED ledger row — the only
names whose cones have actually been checked against a realized close — plotted
together on a single pair of axes. The y-axis is PER CENT away from each name's
own last close, never price, so a EGP 15 Egyptian developer and a $4,091 ounce
of gold are on the same scale and the only thing being compared is the SHAPE and
WIDTH of the probability cone.

Two panels, side by side, one shared per-cent axis:

  * LEFT   anchor -> 1 month   (dist.t20)
  * RIGHT  anchor -> 1 month -> 3 months   (dist.t20 then dist.t60)

The right panel bends through the published 1-month point because both cones are
published for every one of these names; drawing the 3-month cone as a straight
triangle from the anchor would throw away a published number and invent a shape.
The segments BETWEEN published points are straight lines and nothing more is
claimed for them — this module has no engine in it and never simulates. It reads
the cones that are already on the ticker pages.

HORIZONS ARE CALENDAR HORIZONS, so the x-axis is calendar months. The session
counts in `hz` (20-23 for the 1-month leg, 61-66 for the 3-month) differ by
exchange calendar and are reported in the caption rather than used as an axis:
they size the cone at strike time, they are not what it is graded on.

WHY PER CENT, AND WHY THESE FOURTEEN
------------------------------------
The set is derived, never typed: LEDGER rows with a non-null `realized_close`.
It comes out at fourteen today and will grow as cohorts mature — the module
prints the count it found and does not assert on fourteen, because asserting on
a live count is exactly the volatile-number habit the protocol forbids.

Three of the fourteen are metals (Gold, Silver, Platinum), which live in METALS
rather than TICKERS and are drawn dashed. Metals carry the weakest calibration
in the system — gold is a single-name self-fit and silver borrows gold's fit —
and the caption says so rather than letting three smooth cones imply otherwise.

AS-OF STAMPS ARE PART OF THE READ. Every cone is anchored on its own last close
and those closes are NOT the same date across fourteen names. The panel footer
carries the span, and any name whose `asof.mc.data` is older than its
`asof.tech.data` is marked with a dagger — a cone stale against its own library
is a diagnostic to report, never something to reconcile quietly inside a chart.

VERIFY BY IMPORT, NOT BY PARSE — per the standing rule. `python3 -c "import
engine.cone_overlay_chart"` must succeed before any commit relies on this.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, "assets", "data.js")
OUT_PNG = os.path.join(ROOT, "assets", "cone_overlay_graded.png")

QUANTS = ("p5", "p25", "p50", "p75", "p95")

# Canvas — solid light, no transparency anywhere (figure discipline).
BG = "#FFFFFF"
INK = "#14181D"
MUTED = "#6B7580"
GRID = "#E4E8EC"
ZERO = "#9AA4AF"

# Fourteen separable hues, ORDERED so that same-family colours never land next
# to each other in the width sort: the first cut put three pinks and two teals
# in adjacent slots and the 1-month panel could not be read by colour at all.
PALETTE = [
    "#C2410C", "#1D4ED8", "#0E7490", "#BE185D", "#7C3AED", "#15803D", "#A16207",
    "#4338CA", "#DB2777", "#166534", "#0F766E", "#9F1239", "#B45309", "#334155",
]


# ------------------------------------------------------------------ data load
def load_site_data(data_js: str = DATA_JS) -> tuple[dict, dict, list]:
    """Evaluate data.js and return (TICKERS, METALS, LEDGER).

    data.js is JavaScript with prose comments, not JSON, so it is EVALUATED by
    node rather than regex-parsed — the same route fv_overlay.load_tickers takes,
    and the same reason: a regex over unquoted object keys silently dropped
    "2POINTZERO" from three separate tools, each of which reported success.
    """
    script = (
        "const fs=require('fs'),vm=require('vm');const s={};vm.createContext(s);"
        f"vm.runInContext(fs.readFileSync({json.dumps(data_js)},'utf8')"
        "+';globalThis.__O={TICKERS,METALS,LEDGER};',s);"
        "process.stdout.write(JSON.stringify(s.__O));"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True,
                         check=True)
    o = json.loads(out.stdout)
    return o["TICKERS"], o["METALS"], o["LEDGER"]


@dataclass
class Cone:
    key: str            # ledger instrument name
    label: str          # what goes on the chart
    code: str           # exchange-prefixed code, e.g. EGX:PHDC / XAU/USD
    market: str         # EGX / KRX / NSE / QSE / metal
    is_metal: bool
    spot: float
    spot_date: str
    ccy: str
    h1: Optional[int]
    h3: Optional[int]
    m1: dict            # 1-month quantiles, PER CENT from spot
    m3: dict            # 3-month quantiles, PER CENT from spot
    mc_data: str
    tech_data: str

    @property
    def stale_vs_library(self) -> bool:
        """asof.mc.data older than asof.tech.data — the published cone is stale
        relative to its own library. Reported, never silently reconciled."""
        return bool(self.mc_data and self.tech_data and self.mc_data < self.tech_data)


def _pct(dist: dict, spot: float) -> dict:
    return {q: (dist[q] / spot - 1.0) * 100.0 for q in QUANTS}


def graded_instruments(ledger: list) -> list[str]:
    """Instruments with at least one graded row, in first-appearance order.

    A graded row is one carrying a realized close: the forecast has been checked
    against what actually happened. Derived from the ledger every run — never a
    hardcoded list, so the set grows on its own as cohorts mature.
    """
    seen, out = set(), []
    for row in ledger:
        if row.get("realized_close") is None:
            continue
        inst = row["instrument"]
        if inst not in seen:
            seen.add(inst)
            out.append(inst)
    return out


def collect(tickers: dict, metals: dict, ledger: list) -> list[Cone]:
    """Resolve every graded instrument to its published cone.

    Ledger instrument names and site keys are NOT the same casing (ledger
    "Samsung" against TICKERS "SAMSUNG", ledger "Gold" against METALS "GOLD"),
    so the lookup tries both containers. A miss RAISES rather than being skipped:
    a name quietly dropped from a chart of "all of them" is the whole defect.
    """
    cones: list[Cone] = []
    for inst in graded_instruments(ledger):
        entry, is_metal = None, False
        for container, metal in ((tickers, False), (metals, True)):
            for key in (inst, inst.upper()):
                if key in container:
                    entry, is_metal = container[key], metal
                    break
            if entry is not None:
                break
        if entry is None:
            raise SystemExit(f"{inst}: graded in LEDGER but no published cone in "
                             "TICKERS or METALS — refusing to draw a partial set")
        spot = float(entry["spot"])
        dist, hz = entry["dist"], entry.get("hz") or {}
        asof = entry.get("asof") or {}
        code = entry.get("code", "")
        cones.append(Cone(
            key=inst,
            label=entry.get("name", inst) if is_metal else inst,
            code=code,
            market="metal" if is_metal else (code.split(":")[0] if ":" in code else "?"),
            is_metal=is_metal,
            spot=spot,
            spot_date=entry.get("spotDate", ""),
            ccy=entry.get("ccy", ""),
            h1=hz.get("h1"), h3=hz.get("h3"),
            m1=_pct(dist["t20"], spot),
            m3=_pct(dist["t60"], spot),
            mc_data=(asof.get("mc") or {}).get("data", ""),
            tech_data=(asof.get("tech") or {}).get("data", ""),
        ))
    return cones


# -------------------------------------------------------------------- drawing
def _dodge(ys: list[float], gap: float, lo: float, hi: float) -> list[float]:
    """Push labels apart to a minimum gap, preserving order, staying in range.

    Label collisions are fixed IN-PASS per the figure-discipline rule, not left
    for the reader to squint through.
    """
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    placed = list(ys)
    run = lo
    for i in order:                      # sweep up
        run = max(run, placed[i], lo)
        placed[i] = run
        run += gap
    run = hi
    for i in reversed(order):            # sweep back down if we ran off the top
        run = min(run, placed[i], hi)
        placed[i] = run
        run -= gap
    return placed


def draw(cones: list[Cone], out_png: str = OUT_PNG) -> str:
    order = sorted(range(len(cones)),
                   key=lambda i: cones[i].m3["p95"] - cones[i].m3["p5"],
                   reverse=True)
    cones = [cones[i] for i in order]
    colors = {c.key: PALETTE[i % len(PALETTE)] for i, c in enumerate(cones)}

    fig = plt.figure(figsize=(19.0, 10.4), dpi=170, facecolor=BG)
    gs = fig.add_gridspec(1, 3, width_ratios=[0.82, 1.42, 0.94],
                          left=0.045, right=0.988, top=0.845, bottom=0.135,
                          wspace=0.26)
    ax1 = fig.add_subplot(gs[0, 0], facecolor=BG)
    ax3 = fig.add_subplot(gs[0, 1], facecolor=BG, sharey=ax1)
    axt = fig.add_subplot(gs[0, 2], facecolor=BG)

    lo = min(c.m3["p5"] for c in cones) - 7
    hi = max(c.m3["p95"] for c in cones) + 7

    for ax, xmax, pad, xticks, xlabels in (
        (ax1, 1.0, 1.03, [0, 1], ["anchor", "1 month"]),
        (ax3, 3.0, 1.30, [0, 1, 3], ["anchor", "1 month", "3 months"]),
    ):
        ax.set_xlim(-0.02 * xmax, xmax * pad)
        ax.set_ylim(lo, hi)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels, fontsize=10.5, color=MUTED)
        ax.axhline(0, color=ZERO, lw=1.1, zorder=2)
        ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)
        ax.tick_params(colors=MUTED, labelsize=10.5, length=0)
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:+.0f}%".replace("+0%", "0%"))

    # ---- the cones themselves. Only the p25-p75 half-mass is filled: fourteen
    # overlapping p5-p95 fills stack into an unreadable smear, and the outer
    # bound reads better as a crisp line than as the edge of a wash.
    for ax, xs, keys in ((ax1, [0.0, 1.0], ["m1"]),
                         (ax3, [0.0, 1.0, 3.0], ["m1", "m3"])):
        for c in cones:
            col = colors[c.key]
            ls = (0, (5, 2.4)) if c.is_metal else "-"
            seq = [getattr(c, k) for k in keys]
            band = lambda q: [0.0] + [d[q] for d in seq]  # noqa: E731
            ax.fill_between(xs, band("p25"), band("p75"), color=col, alpha=0.05,
                            lw=0, zorder=3)
            ax.plot(xs, band("p95"), color=col, lw=1.8, ls=ls, zorder=6,
                    solid_capstyle="round")
            ax.plot(xs, band("p5"), color=col, lw=1.8, ls=ls, zorder=6,
                    solid_capstyle="round")
            ax.plot(xs, band("p50"), color=col, lw=0.9, ls=(0, (1.6, 2.2)),
                    alpha=0.8, zorder=5)

    # ---- endpoint labels on the 3-month panel only. The 1-month panel is keyed
    # by the colour swatches in the table: twenty-eight labels in the narrow
    # panel collided at the median no matter how they were dodged, and a chart
    # that needs squinting at has failed whatever it was measuring.
    gap = (hi - lo) * 0.0265
    ys = [c.m3["p95"] for c in cones] + [c.m3["p5"] for c in cones]
    placed = _dodge(ys, gap, lo + gap * 0.6, hi - gap * 0.6)
    for i, (c, y0, y1) in enumerate(zip(cones * 2, ys, placed)):
        col = colors[c.key]
        top_side = i < len(cones)
        ax3.plot([3.0, 3.09], [y0, y1], color=col, lw=0.7, alpha=0.6, zorder=6)
        ax3.text(3.12, y1, f"{c.label} {y0:+.0f}%", fontsize=9.0, color=col,
                 va="center", ha="left", zorder=7,
                 fontweight="bold" if top_side else "normal")

    ax1.set_title("1 month", fontsize=13.5, color=INK, fontweight="bold",
                  loc="left", pad=10)
    ax3.set_title("3 months", fontsize=13.5, color=INK, fontweight="bold",
                  loc="left", pad=10)
    ax1.set_ylabel("per cent from that name's own last close", fontsize=11,
                   color=MUTED, labelpad=8)

    # ---- the numbers, so the figure stands alone. Everything in this panel is
    # placed in AXES FRACTION and nothing in data coordinates -- mixing the two
    # is what threw the first render's table off its own axis.
    axt.set_axis_off()
    axt.set_xlim(0, 1)
    axt.set_ylim(0, 1)
    T = axt.transAxes
    n = len(cones)
    row_h = 0.052
    top = 0.985

    def t(x, y, s, **kw):
        kw.setdefault("transform", T)
        kw.setdefault("clip_on", False)
        return axt.text(x, y, s, **kw)

    t(0.0, top, "the same cones as numbers", fontsize=10.6, color=INK,
      fontweight="bold", va="top")
    t(0.0, top - 0.036, "per cent from that name's own last close",
      fontsize=9.2, color=MUTED, va="top")
    hdr = top - 0.092
    t(0.395, hdr, "1 month", fontsize=9.6, color=INK, fontweight="bold",
      va="top", ha="center")
    t(0.795, hdr, "3 months", fontsize=9.6, color=INK, fontweight="bold",
      va="top", ha="center")
    sub = hdr - 0.036
    cols = ((0.275, "p5"), (0.395, "p50"), (0.515, "p95"),
            (0.675, "p5"), (0.795, "p50"), (0.915, "p95"))
    for x, s in cols:
        t(x, sub, s, fontsize=8.6, color=MUTED, va="top", ha="center")
    rule = sub - 0.026
    axt.plot([0.0, 1.0], [rule, rule], color=GRID, lw=1.0, transform=T,
             clip_on=False)
    y = rule - 0.030
    for c in cones:
        col = colors[c.key]
        axt.plot([0.0, 0.030], [y - 0.013, y - 0.013], color=col, lw=2.4,
                 ls=(0, (2.2, 1.2)) if c.is_metal else "-", transform=T,
                 clip_on=False, solid_capstyle="butt")
        t(0.044, y, c.label, fontsize=9.0, color=INK, va="top")
        vals = (c.m1["p5"], c.m1["p50"], c.m1["p95"],
                c.m3["p5"], c.m3["p50"], c.m3["p95"])
        for (x, _), v in zip(cols, vals):
            t(x, y, f"{v:+.1f}", fontsize=9.0, color=INK, va="top", ha="center")
        y -= row_h

    # ---- masthead + the caveats that belong on the face of the chart
    fig.text(0.045, 0.965, "Where each graded name's cone sits, in per cent",
             fontsize=22, color=INK, fontweight="bold", va="top")
    fig.text(0.045, 0.922,
             f"The {n} instruments on the public ledger whose forecasts have been "
             "graded against a realized close — every published cone on one per-cent "
             "scale, so what is compared is width and skew, not price.",
             fontsize=11.6, color=MUTED, va="top")

    spans = sorted(c.mc_data for c in cones if c.mc_data)
    stale = [c.label for c in cones if c.stale_vs_library]
    h1s = sorted({c.h1 for c in cones if c.h1})
    h3s = sorted({c.h3 for c in cones if c.h3})
    lines = [
        "Read from the published cones in assets/data.js — nothing is re-simulated here. Lines are p5 and p95; the shaded band is p25–p75; the dotted line is the median.",
        f"Segments between published points are straight lines and claim nothing more. Horizons are calendar horizons: the {h1s[0]}–{h1s[-1]} and {h3s[0]}–{h3s[-1]} session counts the cones were sized over differ by exchange calendar and are not what the forecast is graded on.",
        f"Each cone is anchored on its OWN last close and those closes span {spans[0]} to {spans[-1]} — the cones are not simultaneous. Dashed = metals (Gold, Silver, Platinum), the weakest calibration in the system:",
        "gold is a single-name self-fit and silver is published on gold's fit, so read those three with less confidence than the equities, not the same."
        + (f"  † published cone older than its own technical library ({', '.join(stale)})." if stale else ""),
    ]
    fig.text(0.045, 0.092, "\n".join(lines), fontsize=9.2, color=MUTED,
             va="top", linespacing=1.72)

    handles = [Line2D([0], [0], color=INK, lw=1.8, ls="-", label="equity"),
               Line2D([0], [0], color=INK, lw=1.8, ls=(0, (5, 2.4)), label="metal")]
    ax1.legend(handles=handles, loc="lower left", frameon=False, fontsize=9.2,
               labelcolor=MUTED, handlelength=2.4)

    fig.savefig(out_png, facecolor=BG, edgecolor="none", transparent=False, dpi=170)
    plt.close(fig)
    _assert_opaque(out_png)
    return out_png


def _assert_opaque(png: str) -> None:
    """Zero transparency, verified programmatically — not asserted in prose."""
    from PIL import Image
    im = Image.open(png)
    if im.mode == "RGBA":
        alpha = im.getchannel("A")
        if alpha.getextrema()[0] != 255:
            raise SystemExit(f"{png}: canvas carries transparency")
        Image.merge("RGB", im.split()[:3]).save(png)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=OUT_PNG)
    ap.add_argument("--write", action="store_true",
                    help="write the PNG (default is a dry run that only reports)")
    a = ap.parse_args()
    tickers, metals, ledger = load_site_data()
    cones = collect(tickers, metals, ledger)
    print(f"{len(cones)} graded instruments: " + ", ".join(c.label for c in cones))
    for c in cones:
        print(f"  {c.label:<9} {c.code:<14} spot {c.spot:>10} {c.ccy:<4} "
              f"{c.spot_date:<18} mc {c.mc_data} tech {c.tech_data}"
              f"{'  STALE-vs-LIBRARY' if c.stale_vs_library else ''}")
    if a.write:
        print("wrote " + draw(cones, a.out))


if __name__ == "__main__":
    main()
