"""cone_overlay_chart.py — every graded name's cone on ONE chart, in per cent.

TWO FIGURES, AND THEY ARE NOT THE SAME OBJECT
---------------------------------------------
  --mode graded  (the default)  THE FROZEN COHORT AGAINST WHAT HAPPENED.
      Every LEDGER row carrying a realized close: the cone exactly as it was
      published at its anchor, and the close that actually landed, marked on it.
      All fourteen graded rows are 1-MONTH cohorts, so one panel is all there is
      to draw — no 3-month cohort has matured, and an outcome cannot be invented
      for one that has not.
  --mode live    THE CURRENT CONES, 1 month and 3 months, NO outcome.
      The cones on the ticker pages today. These are open forecasts anchored on
      the latest close; nothing has been realized against them, and drawing a
      realized close on one would attach an outcome to a forecast that did not
      make it.

Keeping them apart is the point. The graded cones are anchored 11-Jun to
20-Jul-2026; the live cones are anchored 22-Jul to 21-Aug-2026. They are
different forecasts from different dates and only the first kind can be scored.

WHAT THIS DRAWS
---------------
The fourteen instruments that carry at least one GRADED ledger row — the only
names whose cones have actually been checked against a realized close — plotted
together on a single pair of axes. The y-axis is PER CENT away from each name's
own last close, never price, so a EGP 15 Egyptian developer and a $4,091 ounce
of gold are on the same scale and the only thing being compared is the SHAPE and
WIDTH of the probability cone.

THE CONE SHAPE IS THE WEBSITE'S OWN, NOT AN APPROXIMATION OF IT
--------------------------------------------------------------
`fit_power_law` and `fan_val` below are ports of the identically-named functions
in assets/app.js, which is what draws every fan on every ticker page: each
quantile follows y(t) = a * t**b in LOG space, with (a, b) fitted so the curve
passes exactly through the published percentile points, and the same
piecewise-linear-in-log fallback when a quantile sits on the anchor and the power
law degenerates. A cone is a cone because b is near 0.5 on the band edges —
spread grows with the square root of time — while the median runs at b near 1.0
because it is carry drift, which grows with time itself. Straight lines from the
anchor, which the first cut of this chart drew, get both wrong.

A GRADED COHORT PUBLISHES ONE HORIZON, SO ONE NUMBER IS BORROWED AND SAID SO.
Eleven of the fourteen graded rows have no same-anchor 3-month sibling to fit
against (they predate the lifecycle rule that strikes both horizons together).
The ENDPOINT is never borrowed — it is that cohort's own published p5..p95. Only
the exponent b, which sets the curvature BETWEEN anchor and horizon, is taken
from the nearest available fit: the cohort's own 3-month sibling where one
exists (Platinum, Silver, QNB), otherwise the same instrument's current
published two-horizon cone. Every curve therefore lands exactly on its published
percentiles whatever b is; only the shape of the interior is inherited, and the
figure says which names inherited it.

This module has no engine in it and never simulates. It reads the cones that are
already published.

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
import math
from dataclasses import dataclass
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(ROOT, "assets", "data.js")
OUT_PNG = os.path.join(ROOT, "assets", "cone_overlay_live.png")
OUT_GRADED_PNG = os.path.join(ROOT, "assets", "cone_vs_actual_graded.png")

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
    y1: dict            # log-return at the 1-month horizon, per quantile
    b: dict             # power-law exponent per quantile (None = degenerate)

    @property
    def stale_vs_library(self) -> bool:
        """asof.mc.data older than asof.tech.data — the published cone is stale
        relative to its own library. Reported, never silently reconciled."""
        return bool(self.mc_data and self.tech_data and self.mc_data < self.tech_data)


def _pct(dist: dict, spot: float) -> dict:
    return {q: (dist[q] / spot - 1.0) * 100.0 for q in QUANTS}


# ------------------------------------------------------------------- fan math
# Ports of fitPowerLaw / fanVal in assets/app.js. Every fan on every ticker page
# is drawn by those two functions; reproducing them here rather than
# approximating them is what makes this chart the same shape as the website.
def fit_exponents(near: dict, far: dict, spot: float,
                  h_near: float, h_far: float) -> dict:
    """Per-quantile power-law exponent b, fitted through two published horizons.

    app.js: b = ln(|y_far| / |y_near|) / ln(h_far / h_near), where y = ln(q/spot).
    Returns None for a quantile whose fit is degenerate — a quantile sitting
    exactly on the anchor sends y_near to 0 and b to +/-inf, which is the case
    app.js handles with its piecewise-linear-in-log fallback.
    """
    import math
    out = {}
    for q in QUANTS:
        y_n = math.log(near[q] / spot)
        y_f = math.log(far[q] / spot)
        try:
            b = math.log(abs(y_f) / abs(y_n)) / math.log(h_far / h_near)
        except (ValueError, ZeroDivisionError):
            b = None
        out[q] = b if (b is not None and math.isfinite(b)) else None
    return out


def fan_pct(y_ref: float, b: Optional[float], us) -> list:
    """Per cent from the anchor along the fan, at fractions `us` of the reference
    horizon (u = t / h_ref, so u = 1 IS the published point).

    y(u) = y_ref * u**b in log space, which is app.js's spot*exp(a*t**b) with
    a = y_ref / h_ref**b — identical, and independent of h_ref, so a cohort whose
    session count was never recorded still draws exactly. b None (degenerate)
    falls back to linear in log, the same fallback app.js takes.
    """
    import math
    out = []
    for u in us:
        if u <= 0 or y_ref == 0:
            y = 0.0
        elif b is None:
            y = y_ref * u
        else:
            y = y_ref * (u ** b)
        out.append((math.exp(y) - 1.0) * 100.0)
    return out


def _months_to_u(m: float, h1: float, h3: float) -> float:
    """Calendar months -> fraction of the 1-month horizon, in SESSIONS.

    The fan is session-indexed (app.js plots it that way) while a horizon is a
    calendar commitment, so the two committed points anchor the map — m=1 is h1
    sessions and m=3 is h3 — and it runs linearly between them. Both published
    points are hit exactly; only the interior spacing is linear.
    """
    t = h1 * m if m <= 1.0 else h1 + (h3 - h1) * (m - 1.0) / 2.0
    return t / h1


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
            y1={q: math.log(dist["t20"][q] / spot) for q in QUANTS},
            b=fit_exponents(dist["t20"], dist["t60"], spot,
                            hz.get("h1") or 21, hz.get("h3") or 63),
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


def draw_live(cones: list[Cone], out_png: str = OUT_PNG) -> str:
    order = sorted(range(len(cones)),
                   key=lambda i: cones[i].m3["p95"] - cones[i].m3["p5"],
                   reverse=True)
    cones = [cones[i] for i in order]
    colors = {c.key: PALETTE[i % len(PALETTE)] for i, c in enumerate(cones)}

    fig = plt.figure(figsize=(19.0, 10.4), dpi=170, facecolor=BG)
    gs = fig.add_gridspec(1, 3, width_ratios=[0.82, 1.42, 0.94],
                          left=0.045, right=0.988, top=0.845, bottom=0.152,
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

    # ---- the cones themselves, drawn as the website draws them: a per-quantile
    # power law in log space through the published points, not a straight line
    # from the anchor. Only the p25-p75 half-mass is filled -- fourteen
    # overlapping p5-p95 fills stack into an unreadable smear, and the outer
    # bound reads better as a crisp line than as the edge of a wash.
    for ax, mmax in ((ax1, 1.0), (ax3, 3.0)):
        ms = [mmax * i / 120.0 for i in range(121)]
        for c in cones:
            col = colors[c.key]
            ls = (0, (5, 2.4)) if c.is_metal else "-"
            us = [_months_to_u(m, c.h1 or 21, c.h3 or 63) for m in ms]
            curve = {q: fan_pct(c.y1[q], c.b[q], us) for q in QUANTS}
            ax.fill_between(ms, curve["p25"], curve["p75"], color=col,
                            alpha=0.05, lw=0, zorder=3)
            ax.plot(ms, curve["p95"], color=col, lw=1.8, ls=ls, zorder=6,
                    solid_capstyle="round")
            ax.plot(ms, curve["p5"], color=col, lw=1.8, ls=ls, zorder=6,
                    solid_capstyle="round")
            ax.plot(ms, curve["p50"], color=col, lw=0.9, ls=(0, (1.6, 2.2)),
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
        "Cone shape is the website's own fan — a per-quantile power law in log space through the published points (assets/app.js fitPowerLaw/fanVal), so the band edges spread with roughly the square root of time while the median runs on carry drift.",
        f"Horizons are calendar horizons: the {h1s[0]}–{h1s[-1]} and {h3s[0]}–{h3s[-1]} session counts the cones were sized over differ by exchange calendar and are not what the forecast is graded on.",
        f"Each cone is anchored on its OWN last close and those closes span {spans[0]} to {spans[-1]} — the cones are not simultaneous. Dashed = metals (Gold, Silver, Platinum), the weakest calibration in the system:",
        "gold is a single-name self-fit and silver is published on gold's fit, so read those three with less confidence than the equities, not the same."
        + (f"  † published cone older than its own technical library ({', '.join(stale)})." if stale else ""),
    ]
    fig.text(0.045, 0.108, "\n".join(lines), fontsize=9.2, color=MUTED,
             va="top", linespacing=1.72)

    handles = [Line2D([0], [0], color=INK, lw=1.8, ls="-", label="equity"),
               Line2D([0], [0], color=INK, lw=1.8, ls=(0, (5, 2.4)), label="metal")]
    ax1.legend(handles=handles, loc="lower left", frameon=False, fontsize=9.2,
               labelcolor=MUTED, handlelength=2.4)

    fig.savefig(out_png, facecolor=BG, edgecolor="none", transparent=False, dpi=170)
    plt.close(fig)
    _assert_opaque(out_png)
    return out_png


# ============================================================ graded cohorts
@dataclass
class Graded:
    key: str
    label: str
    is_metal: bool
    anchor_date: str
    grade_date: str
    anchor_price: float
    ccy: str
    cycle_no: int
    horizon_label: str
    cone: dict          # published p5..p95, PER CENT from anchor_price
    y1: dict            # published p5..p95 as log returns from anchor_price
    b: dict             # power-law exponent per quantile
    b_source: str       # 'own' (same-anchor 3M sibling) | 'live' (current cone)
    actual: float       # realized close, PER CENT from anchor_price
    pit: Optional[float]
    in_90: bool
    in_50: bool


def collect_graded(tickers: dict, metals: dict, ledger: list) -> list[Graded]:
    """Every graded LEDGER row, with the cone it published and where it landed.

    The cone is the FROZEN one — the percentiles exactly as struck, never
    re-simulated and never re-anchored. The only thing not taken from the row
    itself is the power-law exponent that sets the curvature between anchor and
    horizon, because a 1-month row publishes one horizon and a curve needs two
    points. Preference order, recorded per name on the figure:

      'own'   the same cohort's own 3-month sibling row (same instrument, same
              anchor date) — this is app.js's fit exactly, nothing borrowed;
      'live'  that instrument's current published two-horizon cone — same name,
              same engine, same market profile, a different anchor.

    Either way the curve passes through the row's OWN published percentiles at
    the horizon: b bends the interior, it cannot move the endpoint.
    """
    out: list[Graded] = []
    for row in ledger:
        if row.get("realized_close") is None:
            continue
        inst, anchor = row["instrument"], float(row["anchor_price"])
        sib = next((x for x in ledger
                    if x["instrument"] == inst
                    and x["anchor_date"] == row["anchor_date"]
                    and x["horizon_label"] == "3 months"), None)
        entry, is_metal = None, False
        for container, metal in ((tickers, False), (metals, True)):
            for key in (inst, inst.upper()):
                if key in container:
                    entry, is_metal = container[key], metal
                    break
            if entry is not None:
                break
        if entry is None:
            raise SystemExit(f"{inst}: graded but no published cone to take a "
                             "cone shape from — refusing to guess one")
        if sib is not None and row.get("horizon_days") and sib.get("horizon_days"):
            b = fit_exponents(row, sib, anchor,
                              row["horizon_days"], sib["horizon_days"])
            b_source = "own"
        else:
            hz = entry.get("hz") or {}
            b = fit_exponents(entry["dist"]["t20"], entry["dist"]["t60"],
                              float(entry["spot"]),
                              hz.get("h1") or 21, hz.get("h3") or 63)
            b_source = "live"
        out.append(Graded(
            key=inst,
            label=entry.get("name", inst) if is_metal else inst,
            is_metal=is_metal,
            anchor_date=row["anchor_date"],
            grade_date=row["grade_date"],
            anchor_price=anchor,
            ccy=row.get("ccy", ""),
            cycle_no=row.get("cycle_no", 1),
            horizon_label=row["horizon_label"],
            cone={q: (row[q] / anchor - 1.0) * 100.0 for q in QUANTS},
            y1={q: math.log(row[q] / anchor) for q in QUANTS},
            b=b, b_source=b_source,
            actual=(float(row["realized_close"]) / anchor - 1.0) * 100.0,
            pit=row.get("realized_quantile"),
            in_90=bool(row.get("in_90")),
            in_50=bool(row.get("in_50")),
        ))
    return out


def draw_graded(gs: list[Graded], out_png: str = OUT_GRADED_PNG) -> str:
    """The frozen cone each name was graded on, and the close that landed."""
    gs = sorted(gs, key=lambda g: g.cone["p95"] - g.cone["p5"], reverse=True)
    colors = {g.key: PALETTE[i % len(PALETTE)] for i, g in enumerate(gs)}

    fig = plt.figure(figsize=(19.0, 10.4), dpi=170, facecolor=BG)
    grid = fig.add_gridspec(1, 2, width_ratios=[1.58, 1.0],
                            left=0.045, right=0.988, top=0.812, bottom=0.135,
                            wspace=0.14)
    ax = fig.add_subplot(grid[0, 0], facecolor=BG)
    axt = fig.add_subplot(grid[0, 1], facecolor=BG)

    lo = min(min(g.cone["p5"] for g in gs), min(g.actual for g in gs)) - 7
    hi = max(max(g.cone["p95"] for g in gs), max(g.actual for g in gs)) + 7
    ax.set_xlim(-0.02, 1.34)
    ax.set_ylim(lo, hi)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["anchor\n(the close it was struck on)",
                        "1 month\n(the date it was graded on)"],
                       fontsize=10.5, color=MUTED)
    ax.axhline(0, color=ZERO, lw=1.1, zorder=2)
    ax.axvline(1.0, color=GRID, lw=1.0, zorder=1)
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=10.5, length=0)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:+.0f}%".replace("+0%", "0%"))
    ax.set_ylabel("per cent from the close the forecast was struck on",
                  fontsize=11, color=MUTED, labelpad=8)

    ms = [i / 120.0 for i in range(121)]
    for g in gs:
        col = colors[g.key]
        ls = (0, (5, 2.4)) if g.is_metal else "-"
        curve = {q: fan_pct(g.y1[q], g.b[q], ms) for q in QUANTS}
        ax.fill_between(ms, curve["p25"], curve["p75"], color=col, alpha=0.05,
                        lw=0, zorder=3)
        ax.plot(ms, curve["p95"], color=col, lw=1.7, ls=ls, zorder=5)
        ax.plot(ms, curve["p5"], color=col, lw=1.7, ls=ls, zorder=5)
        ax.plot(ms, curve["p50"], color=col, lw=0.9, ls=(0, (1.6, 2.2)),
                alpha=0.8, zorder=4)

    # ---- what actually happened. A miss is drawn as a ring, not a dot: the one
    # outcome that fell outside its own 90% band should be findable at a glance.
    for g in gs:
        col = colors[g.key]
        if g.in_90:
            ax.plot([1.0], [g.actual], "o", ms=8.4, mfc=col, mec=BG, mew=1.6,
                    zorder=9)
        else:
            ax.plot([1.0], [g.actual], "o", ms=11.0, mfc="none", mec=col,
                    mew=2.4, zorder=9)
            ax.plot([1.0], [g.actual], "x", ms=6.0, mec=col, mew=2.0, zorder=10)

    gap = (hi - lo) * 0.0255
    ys = [g.actual for g in gs]
    placed = _dodge(ys, gap, lo + gap * 0.6, hi - gap * 0.6)
    for g, y0, y1 in zip(gs, ys, placed):
        col = colors[g.key]
        ax.plot([1.012, 1.05], [y0, y1], color=col, lw=0.7, alpha=0.6, zorder=8)
        flag = "" if g.in_90 else "  · outside 90%"
        ax.text(1.062, y1, f"{g.label} {y0:+.1f}%{flag}", fontsize=9.2,
                color=col, va="center", ha="left", zorder=9,
                fontweight="bold" if not g.in_90 else "normal")

    ax.set_title("the cone as published, and the close that landed",
                 fontsize=13.5, color=INK, fontweight="bold", loc="left", pad=10)

    handles = [
        Line2D([0], [0], color=INK, lw=1.7, ls="-", label="equity cone"),
        Line2D([0], [0], color=INK, lw=1.7, ls=(0, (5, 2.4)), label="metal cone"),
        Line2D([0], [0], color=INK, lw=0, marker="o", ms=8, mfc=INK, mec=BG,
               label="realized close, inside the 90% band"),
        Line2D([0], [0], color=INK, lw=0, marker="o", ms=9.5, mfc="none",
               mec=INK, mew=2.0, label="realized close, outside it"),
    ]
    ax.legend(handles=handles, loc="lower left", frameon=False, fontsize=9.2,
              labelcolor=MUTED, handlelength=2.2)

    # ---- the numbers. Axes fraction throughout.
    axt.set_axis_off()
    axt.set_xlim(0, 1)
    axt.set_ylim(0, 1)
    T = axt.transAxes

    def t(x, y, s_, **kw):
        kw.setdefault("transform", T)
        kw.setdefault("clip_on", False)
        return axt.text(x, y, s_, **kw)

    row_h = 0.0525
    top = 0.985
    t(0.0, top, "what was forecast, and what happened", fontsize=10.6,
      color=INK, fontweight="bold", va="top")
    t(0.0, top - 0.036, "per cent from the anchor close; PIT is where the "
      "outcome fell in its own cone", fontsize=9.2, color=MUTED, va="top")
    hdr = top - 0.098
    for x, lab, ha in ((0.0, "", "left"), (0.30, "p5", "center"),
                       (0.415, "p50", "center"), (0.53, "p95", "center"),
                       (0.665, "actual", "center"), (0.785, "PIT", "center"),
                       (0.90, "in 90 / 50", "center")):
        t(x, hdr, lab, fontsize=9.0, color=INK, fontweight="bold", va="top",
          ha=ha)
    t(0.185, hdr, "struck", fontsize=9.0, color=MUTED, va="top", ha="center")
    rule = hdr - 0.030
    axt.plot([0.0, 1.0], [rule, rule], color=GRID, lw=1.0, transform=T,
             clip_on=False)
    y = rule - 0.030
    for g in gs:
        col = colors[g.key]
        axt.plot([0.0, 0.026], [y - 0.013, y - 0.013], color=col, lw=2.4,
                 ls=(0, (2.2, 1.2)) if g.is_metal else "-", transform=T,
                 clip_on=False, solid_capstyle="butt")
        t(0.038, y, g.label, fontsize=9.0, color=INK, va="top")
        t(0.185, y, g.anchor_date[5:].replace("-", "/"), fontsize=8.6,
          color=MUTED, va="top", ha="center")
        for x, v in ((0.30, g.cone["p5"]), (0.415, g.cone["p50"]),
                     (0.53, g.cone["p95"])):
            t(x, y, f"{v:+.1f}", fontsize=9.0, color=INK, va="top", ha="center")
        t(0.665, y, f"{g.actual:+.1f}", fontsize=9.0, color=col, va="top",
          ha="center", fontweight="bold")
        t(0.785, y, f"{g.pit:.2f}" if g.pit is not None else "<0.05",
          fontsize=9.0, color=INK if g.pit is not None else col, va="top",
          ha="center")
        marks = ("\u2713" if g.in_90 else "\u2717") + " / " + ("\u2713" if g.in_50 else "\u2717")
        t(0.90, y, marks, fontsize=9.0, va="top", ha="center",
          color=INK if g.in_90 else col)
        y -= row_h

    n = len(gs)
    n90 = sum(1 for g in gs if g.in_90)
    n50 = sum(1 for g in gs if g.in_50)
    pits = [g.pit for g in gs if g.pit is not None]
    y -= 0.012
    axt.plot([0.0, 1.0], [y + 0.014, y + 0.014], color=GRID, lw=1.0,
             transform=T, clip_on=False)
    t(0.038, y - 0.008, f"{n90} of {n} inside the 90% band, {n50} of {n} inside "
      f"the 50%; mean PIT {sum(pits) / len(pits):.3f} on the {len(pits)} scored.",
      fontsize=9.2, color=INK, va="top")

    # ---- masthead + caveats
    fig.text(0.045, 0.965,
             "The cone each name was graded on, and where the price landed",
             fontsize=22, color=INK, fontweight="bold", va="top")
    anchors = sorted(g.anchor_date for g in gs)
    fig.text(0.045, 0.922,
             f"All {n} graded cohorts on the public ledger — every one a 1-month forecast, "
             f"struck between {anchors[0]} and {anchors[-1]} and scored against the close on "
             "its own grade date.\nNo 3-month cohort has matured, so there is no 3-month "
             "outcome to draw and none is invented.",
             fontsize=11.6, color=MUTED, va="top", linespacing=1.5)

    borrowed = [g.label for g in gs if g.b_source == "live"]
    own = [g.label for g in gs if g.b_source == "own"]
    lines = [
        "Frozen percentiles exactly as published — nothing is re-simulated and nothing is re-anchored. Lines are p5 and p95, the shaded band is p25–p75, the dotted line is the median path.",
        "Cone shape is the website's own fan (assets/app.js fitPowerLaw/fanVal): a per-quantile power law in log space, so the band edges spread with roughly the square root of time while the median runs on carry drift.",
        f"Every curve passes exactly through its own published percentiles; only the curvature BETWEEN anchor and horizon needs a second point. {', '.join(own)} take it from their own 3-month sibling row — the site's fit exactly.",
        f"The other {len(borrowed)} have no same-anchor sibling and inherit the exponent from that same instrument's current published cone; the endpoint is never inherited. Dashed = metals, the weakest calibration in the system.",
    ]
    fig.text(0.045, 0.092, "\n".join(lines), fontsize=9.2, color=MUTED,
             va="top", linespacing=1.72)

    fig.savefig(out_png, facecolor=BG, edgecolor="none", transparent=False,
                dpi=170)
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
    ap.add_argument("--mode", choices=("graded", "live", "both"), default="graded",
                    help="graded = frozen cohorts vs the realized close (default); "
                         "live = the current open cones, 1 and 3 months")
    ap.add_argument("--out", default=None)
    ap.add_argument("--write", action="store_true",
                    help="write the PNG (default is a dry run that only reports)")
    a = ap.parse_args()
    tickers, metals, ledger = load_site_data()

    if a.mode in ("graded", "both"):
        gs = collect_graded(tickers, metals, ledger)
        n90 = sum(1 for g in gs if g.in_90)
        n50 = sum(1 for g in gs if g.in_50)
        print(f"{len(gs)} graded cohorts — {n90} inside the 90% band, {n50} "
              f"inside the 50%")
        for g in sorted(gs, key=lambda x: x.cone["p95"] - x.cone["p5"],
                        reverse=True):
            pit = f"{g.pit:.3f}" if g.pit is not None else "<0.05 (censored)"
            print(f"  {g.label:<9} {g.horizon_label:<8} cyc{g.cycle_no} "
                  f"{g.anchor_date} -> {g.grade_date}  "
                  f"cone {g.cone['p5']:+6.1f}/{g.cone['p50']:+5.1f}/"
                  f"{g.cone['p95']:+6.1f}  actual {g.actual:+6.1f}  "
                  f"PIT {pit:<16} b:{g.b_source}"
                  f"{'' if g.in_90 else '  <-- OUTSIDE THE 90% BAND'}")
        if a.write:
            print("wrote " + draw_graded(gs, a.out or OUT_GRADED_PNG))

    if a.mode in ("live", "both"):
        cones = collect(tickers, metals, ledger)
        print(f"{len(cones)} live cones: " + ", ".join(c.label for c in cones))
        if a.write:
            print("wrote " + draw_live(cones, a.out or OUT_PNG))


if __name__ == "__main__":
    main()
