#!/usr/bin/env python3
"""build_three_lens_trial.py — the three-clocks trial canvas (PHDC + GBCO).

WHAT THIS IS
------------
A lab-only display experiment: one canvas per name that lays the three
independent lenses on a single price axis —

  * the TECHNICAL read (days–weeks): the computed S/R ladder as entry/exit
    REFERENCE levels, drawn over the near-term window;
  * the MONTE CARLO cone (1–3 months): the published percentiles of the
    current strike, at their calendar check dates;
  * the FUNDAMENTAL fair-value range (~12 months): the study's bear/base/full,
    drawn as a floating bracket on its own shelf, DELIBERATELY not connected
    to the cone.

THREE-LENS INDEPENDENCE [R-LENS-01] IS PRESERVED BY CONSTRUCTION: this script
reads each lens's PUBLISHED output and draws them side by side. No lens's
output is an input to another here; the page is a comparison surface only
(same standing as fv_overlay — reads outputs, feeds nothing back).

GENERATED, NEVER TYPED: every numeral on the page comes from assets/data.js
(read through a real JS parse, per R-ENF-03), from the LEDGER strike rows, or
from the raw OHLC libraries — and the two sources are asserted against each
other before anything renders. The calibration sentence renders through
engine/band_record.BandRecord.record_clause(), the one sanctioned phrasing.
CALIB is deliberately absent (internal diagnostic; it does not reach a reader).

Regenerate:  python3 engine/lab/three_lens_trial/build_three_lens_trial.py
Outputs:     engine/lab/three_lens_trial/three_lens_trial.html  (standalone)

Lab code is NOT production. Nothing here is imported by the engine, and the
page is not linked from the live site.
"""

import csv
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "engine"))

from band_record import BandRecord  # noqa: E402  (canonical clause phrasing)

DATA_JS = os.path.join(ROOT, "assets", "data.js")
OUT_HTML = os.path.join(HERE, "three_lens_trial.html")

TRIAL = ["PHDC", "GBCO"]
HISTORY_DAYS = 183          # ~6 calendar months of library behind the anchor

# Read data.js through a real JS engine — the R-ENF-03 rule. `this.__*` because
# const never becomes a property of the vm context.
NODE_READ = r'''
const fs = require("fs"), vm = require("vm");
const c = {}; vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[1], "utf8")
  + "\n;this.__T=TICKERS;this.__B=(typeof BANDS!=='undefined')?BANDS:{};this.__L=LEDGER;", c);
console.log(JSON.stringify({tickers: c.__T, bands: c.__B, ledger: c.__L}));
'''

CHECKS = []          # (ticker, what) — every assertion that ran, counted


def note(tk, what):
    CHECKS.append((tk, what))


def die(msg):
    print(f"BUILD FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)


def must(cond, tk, what):
    if not cond:
        die(f"[{tk}] {what}")
    note(tk, what)


# ---------------------------------------------------------------- data intake

def load_data_js():
    p = subprocess.run(["node", "-e", NODE_READ, DATA_JS], capture_output=True, text=True)
    if p.returncode != 0:
        die(f"node could not load data.js:\n{p.stderr.strip()}")
    return json.loads(p.stdout)


def read_library(tk, anchor_iso):
    """Last ~6 months of closes from the persistent library, ascending."""
    path = os.path.join(ROOT, "engine", "raw_ohlc", "EG", f"{tk}.csv")
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = datetime.strptime(r["Date"], "%m/%d/%Y").date()
            rows.append((d, float(r["Price"].replace(",", ""))))
    rows.sort()
    must(len(set(d for d, _ in rows)) == len(rows), tk, "library has no duplicate dates")
    anchor = date.fromisoformat(anchor_iso)
    lo = anchor - timedelta(days=HISTORY_DAYS)
    hist = [(d, c) for d, c in rows if lo <= d <= anchor]
    must(len(hist) >= 100, tk, f"history slice holds {len(hist)} sessions (>=100)")
    must(hist[-1][0] == anchor, tk, "library's last session IS the strike anchor date")
    return hist


LEDGER_NOTE_RX = {
    "direction": re.compile(r"Direction call (UP|DOWN)"),
    "mult": re.compile(r"live_width_mult\(\) returns ([0-9.]+)"),
    "eff": re.compile(r"effective width_cal of ([0-9.]+)"),
    "tilt": re.compile(r"tilt ([+\-][0-9.]+)% at 1M and ([+\-][0-9.]+)% at 3M"),
    "rf": re.compile(r"rf_live ([0-9.]+)%"),
}


def extract(tk, data):
    t = data["tickers"][tk]
    b = data["bands"].get(tk)
    must(b is not None, tk, "BANDS carries a published record")
    must(t["hz"].get("cal") is True, tk, "horizons are calendar-resolved")

    # -- the two current strike rows, asserted against the page dist ---------
    anchor_iso = t["asof"]["mc"]["data"]
    open_rows = [r for r in data["ledger"]
                 if r.get("instrument") == tk and r.get("realized_close") is None
                 and r.get("anchor_date") == anchor_iso]
    rows = {r["horizon_label"]: r for r in open_rows}
    must(sorted(rows) == ["1 month", "3 months"] and len(open_rows) == 2, tk,
         "exactly one open row per horizon at the latest anchor (lifecycle read)")
    for lbl, dk in (("1 month", "t20"), ("3 months", "t60")):
        r, d = rows[lbl], t["dist"][dk]
        for q in ("p5", "p25", "p50", "p75", "p95"):
            must(abs(r[q] - d[q]) < 1e-9, tk, f"{lbl} {q}: ledger == page ({d[q]})")
        must(r["grade_date"] == d["resolve"], tk, f"{lbl} check date == page resolve date")
        ps = [d[q] for q in ("p5", "p25", "p50", "p75", "p95")]
        must(ps == sorted(ps) and len(set(ps)) == 5, tk, f"{lbl} percentiles strictly ascending")
        must(abs(r["anchor_price"] - t["spot"]) < 0.005, tk, f"{lbl} anchor price == page spot")

    n1 = rows["1 month"]["note"]
    parsed = {}
    for k, rx in LEDGER_NOTE_RX.items():
        m = rx.search(n1)
        must(m is not None, tk, f"strike note carries {k}")
        parsed[k] = m.groups() if len(m.groups()) > 1 else m.group(1)

    # -- technical ladder / fair range sanity --------------------------------
    res, sup = t["levels"]["res"], t["levels"]["sup"]
    must(res == sorted(res) and sup == sorted(sup, reverse=True), tk,
         "resistances ascend, supports descend")
    # R1-above / S1-below the narrative's own close is enforced repo-wide by
    # scripts/check_technical_read.py [R-ENF-03]; not re-asserted here.
    f = t["fair"]
    must(f["bear"] < f["base"] < f["full"], tk, "fair bear < base < full")

    # -- band record through the canonical object ----------------------------
    must(abs(b["hits"] / b["n"] - b["c90"]) < 0.005, tk, "hits/n reproduces c90")
    rec = BandRecord(instrument=tk, market=b["mkt"], n=b["n"], hits=b["hits"],
                     cov50=b["c50"], cov80=b["c80"], cov90=b["c90"],
                     width=b["width"], strength=b["strength"], flag=b["flag"],
                     p_value=None)

    hist = read_library(tk, anchor_iso)
    study_m = re.search(r"_(\d{2})-(\d{2})-(\d{4})_", t["files"]["study"])
    must(study_m is not None, tk, "study date derivable from the delivered filename")
    dd, mm, yyyy = study_m.groups()
    study_date = f"{int(dd)} {MONTHS[int(mm) - 1]} {yyyy}"

    return {
        "tk": tk, "t": t, "b": b, "rec": rec, "rows": rows, "hist": hist,
        "anchor": date.fromisoformat(anchor_iso),
        "study_date": study_date,
        "direction": parsed["direction"],
        "signal_z": rows["1 month"]["signal_z"],
        "tilt1": parsed["tilt"][0], "tilt3": parsed["tilt"][1],
        "mult": float(parsed["mult"]), "eff": float(parsed["eff"]),
        "rf": parsed["rf"],
        "cycle": rows["1 month"]["cycle_no"],
        "run_date": rows["1 month"]["run_date"],
    }


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def dshort(d):
    if isinstance(d, str):
        d = date.fromisoformat(d)
    return f"{d.day} {MONTHS[d.month - 1]}"


def dlong(d):
    if isinstance(d, str):
        d = date.fromisoformat(d)
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def f2(v):
    return f"{v:,.2f}"


def pct_vs(spot, v):
    return f"{(v / spot - 1) * 100:+.1f}%"


# ---------------------------------------------------------------- geometry

VB_W, VB_H = 1120, 520
PLOT_TOP, PLOT_BOT = 44, 452
AXIS_Y = 470                    # first axis-label baseline
X_YAXIS = 56
X_HIST0, X_HIST1 = 56, 336      # history zone; NOW at its right edge
X_F0, X_F1 = 336, 776           # forecast window, calendar-linear
X_LBL1 = 788                    # 3M percentile label gutter
X_BREAK = 874                   # clock break
X_SHELF0, X_SHELF1 = 874, 1120
X_SPINE = 968                   # fundamental bracket spine


def nice_ticks(lo, hi, target=7):
    span = hi - lo
    raw = span / target
    mag = 10 ** len(str(int(raw))) / 10 if raw >= 1 else 0.1
    step = min((s for s in (1, 2, 2.5, 5, 10) if s * mag >= raw), default=10) * mag
    t0 = (int(lo / step) + (0 if lo % step == 0 else 1)) * step
    ticks, v = [], t0
    while v <= hi + 1e-9:
        ticks.append(round(v, 2))
        v += step
    return ticks


def build_geometry(m):
    t, hist = m["t"], m["hist"]
    d1, d3 = t["dist"]["t20"], t["dist"]["t60"]
    prices = ([c for _, c in hist]
              + [d3["p5"], d3["p95"], d1["p5"], d1["p95"]]
              + t["levels"]["res"] + t["levels"]["sup"]
              + [t["fair"]["bear"], t["fair"]["full"], t["spot"]])
    lo, hi = min(prices), max(prices)
    pad = (hi - lo) * 0.05
    lo, hi = lo - pad, hi + pad

    def Y(p):
        return PLOT_BOT - (p - lo) / (hi - lo) * (PLOT_BOT - PLOT_TOP)

    n = len(hist)

    def XH(i):
        return X_HIST0 + i / (n - 1) * (X_HIST1 - X_HIST0)

    anchor = m["anchor"]
    r1 = date.fromisoformat(d1["resolve"])
    r3 = date.fromisoformat(d3["resolve"])
    span = (r3 - anchor).days

    def XF(d):
        return X_F0 + (d - anchor).days / span * (X_F1 - X_F0)

    return {"Y": Y, "XH": XH, "XF": XF, "lo": lo, "hi": hi,
            "x1m": XF(r1), "x3m": XF(r3), "r1": r1, "r3": r3}


# ---------------------------------------------------------------- svg pieces

def svg_canvas(m):
    t, g = m["t"], build_geometry(m)
    Y, XH, XF = g["Y"], g["XH"], g["XF"]
    hist, spot = m["hist"], t["spot"]
    d1, d3 = t["dist"]["t20"], t["dist"]["t60"]
    x1m, x3m = g["x1m"], g["x3m"]
    e = []

    # gridlines + y labels
    for v in nice_ticks(g["lo"], g["hi"]):
        y = Y(v)
        e.append(f'<line x1="{X_YAXIS}" y1="{y:.1f}" x2="{X_SHELF1 - 8}" y2="{y:.1f}" class="grid"/>')
        e.append(f'<text x="{X_YAXIS - 6}" y="{y + 3.5:.1f}" class="tick num" text-anchor="end">{v:g}</text>')
    e.append(f'<text x="{X_YAXIS - 6}" y="{PLOT_TOP - 12}" class="cap" text-anchor="end">{t["ccy"]}</text>')

    # zone captions
    for x0, x1, lab in ((X_HIST0, X_HIST1, "PRICE HISTORY · 6 MONTHS"),
                        (X_F0, X_F1, "FORECAST WINDOW · NOW → 3 MONTHS"),
                        (X_SHELF0 + 14, X_SHELF1, "≈ 12 MONTHS")):
        e.append(f'<text x="{(x0 + x1) / 2:.0f}" y="{PLOT_TOP - 12}" class="cap" text-anchor="middle">{lab}</text>')

    # baseline + clock break glyph
    e.append(f'<line x1="{X_YAXIS}" y1="{PLOT_BOT}" x2="{X_BREAK - 7}" y2="{PLOT_BOT}" class="axis"/>')
    e.append(f'<line x1="{X_BREAK + 7}" y1="{PLOT_BOT}" x2="{X_SHELF1 - 8}" y2="{PLOT_BOT}" class="axis"/>')
    for dx in (-3, 3):
        e.append(f'<line x1="{X_BREAK + dx - 4}" y1="{PLOT_BOT + 6}" x2="{X_BREAK + dx + 4}" y2="{PLOT_BOT - 6}" class="axisbreak"/>')
    e.append(f'<line x1="{X_BREAK}" y1="{PLOT_TOP}" x2="{X_BREAK}" y2="{PLOT_BOT - 14}" class="zoneline"/>')

    # month ticks in history (label suppressed where it would crowd the NOW label)
    for i in range(1, len(hist)):
        if hist[i][0].month != hist[i - 1][0].month:
            x = XH(i)
            e.append(f'<line x1="{x:.1f}" y1="{PLOT_BOT}" x2="{x:.1f}" y2="{PLOT_BOT + 5}" class="axis"/>')
            if X_F0 - x > 40:
                e.append(f'<text x="{x:.1f}" y="{AXIS_Y}" class="tick" text-anchor="middle">{MONTHS[hist[i][0].month - 1]}</text>')

    # history line + anchor dot
    pts = " ".join(f"{XH(i):.1f},{Y(c):.1f}" for i, (_, c) in enumerate(hist))
    e.append(f'<polyline points="{pts}" class="hist"/>')
    e.append(f'<line x1="{X_F0}" y1="{PLOT_TOP}" x2="{X_F0}" y2="{PLOT_BOT}" class="nowline"/>')

    # MC cone: 90% then 50% wash, median line — anchor -> 1M -> 3M
    def poly(loq, hiq, cls):
        p = (f"{X_F0:.1f},{Y(spot):.1f} {x1m:.1f},{Y(d1[loq]):.1f} {x3m:.1f},{Y(d3[loq]):.1f} "
             f"{x3m:.1f},{Y(d3[hiq]):.1f} {x1m:.1f},{Y(d1[hiq]):.1f}")
        return f'<polygon points="{p}" class="{cls}"/>'
    e.append(poly("p5", "p95", "cone90"))
    e.append(poly("p25", "p75", "cone50"))
    e.append(f'<path d="M {X_F0:.1f} {Y(spot):.1f} L {x1m:.1f} {Y(d1["p50"]):.1f} L {x3m:.1f} {Y(d3["p50"]):.1f}" class="median"/>')

    # check-date columns
    for x, dt, lab in ((x1m, g["r1"], "1M check"), (x3m, g["r3"], "3M check")):
        e.append(f'<line x1="{x:.1f}" y1="{PLOT_TOP}" x2="{x:.1f}" y2="{PLOT_BOT}" class="checkline"/>')
        e.append(f'<text x="{x:.1f}" y="{AXIS_Y}" class="tick" text-anchor="middle">{dshort(dt)}</text>')
        e.append(f'<text x="{x:.1f}" y="{AXIS_Y + 14}" class="cap" text-anchor="middle">{lab}</text>')
    e.append(f'<text x="{X_F0:.1f}" y="{AXIS_Y}" class="tick" text-anchor="middle">{dshort(m["anchor"])}</text>')
    e.append(f'<text x="{X_F0:.1f}" y="{AXIS_Y + 14}" class="cap" text-anchor="middle">close</text>')

    # 3M percentile end labels (the published claim, directly labeled)
    for q, tag in (("p95", "p95"), ("p75", "p75"), ("p50", "median"), ("p25", "p25"), ("p5", "p5")):
        y = Y(d3[q])
        cls = "endlab num strong" if q == "p50" else "endlab num"
        e.append(f'<line x1="{x3m + 3:.1f}" y1="{y:.1f}" x2="{X_LBL1 - 3}" y2="{y:.1f}" class="leader mc"/>')
        e.append(f'<text x="{X_LBL1}" y="{y + 3.5:.1f}" class="{cls} halo">{f2(d3[q])}<tspan class="qtag"> {tag}</tspan></text>')
    e.append(f'<circle cx="{x3m:.1f}" cy="{Y(d3["p50"]):.1f}" r="4.5" class="dot mc"/>')
    e.append(f'<circle cx="{XH(len(hist) - 1):.1f}" cy="{Y(spot):.1f}" r="4.5" class="dot inkdot"/>')

    # technical ladder: NOW -> 1M, staggered labels
    for i, (v, kind) in enumerate([(v, "R") for v in t["levels"]["res"]]
                                  + [(v, "S") for v in t["levels"]["sup"]]):
        j = i if i < 3 else i - 3
        y = Y(v)
        op = "" if j == 0 else ' style="opacity:.62"'
        e.append(f'<line x1="{X_F0 + 2:.1f}" y1="{y:.1f}" x2="{x1m:.1f}" y2="{y:.1f}" class="talvl"{op}/>')
        lx = X_F0 + 8 + j * 66
        dy = -5 if kind == "R" else 12.5
        e.append(f'<text x="{lx:.1f}" y="{y + dy:.1f}" class="lvllab halo"><tspan class="lvlkey">{kind}{j + 1}</tspan> <tspan class="num">{f2(v)}</tspan></text>')

    # fundamental shelf: floating bracket, own clock
    f = t["fair"]
    yb, ybase, yf = Y(f["bear"]), Y(f["base"]), Y(f["full"])
    e.append(f'<line x1="{X_BREAK + 14}" y1="{Y(spot):.1f}" x2="{X_SHELF1 - 8}" y2="{Y(spot):.1f}" class="spotref"/>')
    e.append(f'<text x="{X_BREAK + 16}" y="{Y(spot) - 5:.1f}" class="cap halo" text-anchor="start">spot {f2(spot)}</text>')
    e.append(f'<rect x="{X_SPINE - 17}" y="{yf:.1f}" width="34" height="{yb - yf:.1f}" rx="8" class="fvwash"/>')
    e.append(f'<line x1="{X_SPINE}" y1="{yf:.1f}" x2="{X_SPINE}" y2="{yb:.1f}" class="fvspine"/>')
    for v, y, tag in ((f["full"], yf, "full"), (f["base"], ybase, "base"), (f["bear"], yb, "bear")):
        e.append(f'<line x1="{X_SPINE - 9}" y1="{y:.1f}" x2="{X_SPINE + 9}" y2="{y:.1f}" class="fvtick"/>')
        cls = "endlab num strong" if tag == "base" else "endlab num"
        e.append(f'<text x="{X_SPINE + 24}" y="{y + 3.5:.1f}" class="{cls} halo">{f2(v)}<tspan class="qtag"> {tag}</tspan></text>')
    e.append(f'<circle cx="{X_SPINE}" cy="{ybase:.1f}" r="5" class="dot fv"/>')
    e.append(f'<text x="{X_SPINE}" y="{AXIS_Y}" class="tick" text-anchor="middle">no date</text>')
    e.append(f'<text x="{X_SPINE}" y="{AXIS_Y + 14}" class="cap" text-anchor="middle">value anchor · study clock</text>')

    # hover hit zones + crosshair (front)
    e.append(f'<line id="xh-{m["tk"]}" x1="0" y1="{PLOT_TOP}" x2="0" y2="{PLOT_BOT}" class="crosshair" style="display:none"/>')
    for cid, x0h, x1h in (("hist", X_HIST0, X_HIST1), ("cone", X_F0 - 1, X_LBL1 + 60), ("shelf", X_BREAK, X_SHELF1)):
        e.append(f'<rect data-zone="{cid}" x="{x0h}" y="{PLOT_TOP}" width="{x1h - x0h}" height="{PLOT_BOT - PLOT_TOP}" class="hit" tabindex="0"/>')

    return (f'<svg viewBox="0 0 {VB_W} {VB_H}" role="img" preserveAspectRatio="xMidYMid meet" '
            f'aria-label="Three-lens canvas for {t["name"]}: price history, technical ladder, '
            f'Monte Carlo cone and fundamental fair-value range on one price axis">'
            + "".join(e) + "</svg>"), g


def hover_json(m, g):
    """Everything the hover layer may say — machine-sourced, snapped to published points."""
    t = m["t"]
    d1, d3 = t["dist"]["t20"], t["dist"]["t60"]
    Y, XH = g["Y"], g["XH"]
    sess = [{"x": round(XH(i), 1), "d": dlong(d), "c": f2(c)} for i, (d, c) in enumerate(m["hist"])]

    def col(x, title, d):
        return {"x": round(x, 1), "title": title,
                "rows": [["p95", f2(d["p95"])], ["p75", f2(d["p75"])], ["median", f2(d["p50"])],
                         ["p25", f2(d["p25"])], ["p5", f2(d["p5"])]]}
    cols = [{"x": X_F0, "title": f"anchor · close {dshort(m['anchor'])}", "rows": [["close", f2(t["spot"])]]},
            col(g["x1m"], f"1-month check · {dshort(g['r1'])}", d1),
            col(g["x3m"], f"3-month check · {dshort(g['r3'])}", d3)]
    f = t["fair"]
    shelf = {"x": X_SPINE, "title": f"fair value · study {m['study_date']}",
             "rows": [["full", f2(f["full"])], ["base", f2(f["base"])], ["bear", f2(f["bear"])]]}
    return {"sessions": sess, "cols": cols, "shelf": shelf,
            "plotTop": PLOT_TOP, "plotBot": PLOT_BOT, "vbw": VB_W}


# ---------------------------------------------------------------- html pieces

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def touch_table(t):
    spot = t["spot"]
    r = []
    for lvl, p1, p3 in t["touch"]:
        arrow = "▲" if lvl >= spot else "▼"
        cls = "up" if lvl >= spot else "dn"
        r.append(f'<tr><td class="num"><span class="tarr {cls}">{arrow}</span> {f2(lvl)}</td>'
                 f'<td class="num">{p1}%</td><td class="num">{p3}%</td></tr>')
    return ('<table class="mini"><thead><tr><th>Level</th><th>P(touch) ≤ 1M</th>'
            '<th>≤ 3M</th></tr></thead><tbody>' + "".join(r) + "</tbody></table>")


def dist_table(m):
    t = m["t"]
    r = []
    for dk in ("t20", "t60"):
        d = t["dist"][dk]
        r.append(f'<tr><td>{d["label"]}<span class="sub">checks {dshort(d["resolve"])}</span></td>'
                 + "".join(f'<td class="num">{f2(d[q])}</td>' for q in ("p5", "p25", "p50", "p75", "p95")) + "</tr>")
    return ('<table class="mini"><thead><tr><th>Horizon</th><th>p5</th><th>p25</th>'
            '<th>median</th><th>p75</th><th>p95</th></tr></thead><tbody>' + "".join(r) + "</tbody></table>")


def stamp(a):
    return (f'data {dlong(a["data"])} · computed {dlong(a["computed"])}')


FUND_PROSE = {
    "PHDC": (
        "<p>A sum-of-the-parts / RNAV build for a land-bank developer: the projects and land "
        "priced leg by leg, netted to an equity value per share, bracketed by a risk-adjusted "
        "bear case and a full-execution case. The spread between them is wide because execution, "
        "not the asset base, is the question.</p>"),
    "GBCO": (
        "<p>A split-the-legs build: the Auto business on discounted cash flow, GB Capital on "
        "adjusted book, and the confirmed MNT-Halan stake marked off its June-2026 funding "
        "round, less a complexity discount — cross-checked against pre-discount NAV, relative "
        "multiples and normalised earnings.</p>"
        "<p class=\"crux\"><b>The crux:</b> taken at the round&rsquo;s face value, the MNT-Halan stake alone "
        "accounts for most of GB Corp&rsquo;s entire market capitalisation. Either the market applies a far "
        "steeper discount to that private mark than the study does, or the name is meaningfully "
        "mispriced. The stake-blind lenses are the conservative anchor if you side with the "
        "market&rsquo;s scepticism.</p>"
        "<p class=\"caveat\">Caveat: the study&rsquo;s cost of capital predates the house&rsquo;s current method and "
        "is queued for re-issue. The retired construction double-counted sovereign risk — a "
        "discount rate set too high — so the error, if any, runs conservative.</p>"),
}


def ticker_section(m, g, svg):
    t, tk, rec = m["t"], m["tk"], m["rec"]
    spot, f = t["spot"], t["fair"]
    d3 = t["dist"]["t60"]
    res, sup = t["levels"]["res"], t["levels"]["sup"]
    dirword = "Upward" if m["direction"] == "UP" else "Downward"
    strength = {"long": "long record", "short": "short record", "market-only": "market record only"}[m["b"]["strength"]]

    align = (
        f'<div class="align">'
        f'<span class="al-item"><span class="k ink">Spot</span><span class="v num">{f2(spot)}</span></span>'
        f'<span class="al-arrow">→</span>'
        f'<span class="al-item"><span class="k mc">MC median · 3M</span><span class="v num">{f2(d3["p50"])}'
        f'<em>{pct_vs(spot, d3["p50"])}</em></span></span>'
        f'<span class="al-arrow">→</span>'
        f'<span class="al-item"><span class="k fv">Fair base · study</span><span class="v num">{f2(f["base"])}'
        f'<em>{pct_vs(spot, f["base"])}</em></span></span>'
        f'<span class="al-item wide"><span class="k fv">Fair range</span><span class="v num">{f2(f["bear"])} – {f2(f["full"])}'
        f'<em>{pct_vs(spot, f["bear"])} … {pct_vs(spot, f["full"])}</em></span></span>'
        f'</div>')

    tech_card = f'''
      <article class="card lens-ta">
        <header><span class="lensdot ta"></span><h3>Technical</h3><span class="htag">days – weeks</span></header>
        <p class="trend">{esc(t["tech"]["trend"])}.</p>
        <p class="body">{esc(t["tech"]["summary"])}</p>
        <div class="lvlgrid">
          <div><span class="lvlhead">Exit / trim references (resistance)</span>
            <span class="num lvlrow">R1 {f2(res[0])} · R2 {f2(res[1])} · R3 {f2(res[2])}</span></div>
          <div><span class="lvlhead">Entry / stop references (support)</span>
            <span class="num lvlrow">S1 {f2(sup[0])} · S2 {f2(sup[1])} · S3 {f2(sup[2])}</span></div>
        </div>
        <p class="trigger"><b>Bull trigger:</b> {esc(t["tech"]["bull"])}</p>
        <p class="trigger"><b>Bear trigger:</b> {esc(t["tech"]["bear"])}</p>
        <p class="fine">Computed reference levels from the published ladder — not advice. Levels move with the library.</p>
        <p class="stamp">{stamp(t["asof"]["tech"])}</p>
      </article>'''

    mc_card = f'''
      <article class="card lens-mc">
        <header><span class="lensdot mc"></span><h3>Monte Carlo</h3><span class="htag">1 – 3 months</span></header>
        <p class="dirchip"><span class="dirsign">{"▲" if m["direction"] == "UP" else "▼"} {m["direction"]}</span> —
           {dirword.lower()} direction call from this name’s own momentum (z {m["signal_z"]:+.2f});
           tilt {m["tilt1"]}% at 1M, {m["tilt3"]}% at 3M. Cycle {m["cycle"]},
           struck {dlong(m["run_date"])} on the {dlong(m["anchor"])} close.</p>
        {dist_table(m)}
        <details class="touch"><summary>Probability of touching a level</summary>{touch_table(t)}</details>
        <p class="body">{rec.record_clause()} {rec.width_clause()} <span class="chip">{strength}</span></p>
        <ul class="fineul">
          <li>Carry-anchored drift at rf {m["rf"]}%; dividend yield held at zero (house convention — the centre is gross of dividend, overstated by roughly the yield).</li>
          <li>Per-name width overlay applied: this name’s own resolved history sets the cone {"narrower" if m["mult"] < 1 else "wider"} than the pooled market fit (multiplier {m["mult"]:.4f}, effective width {m["eff"]:.4f}).</li>
          <li>Check dates are calendar commitments — the forecast grades on the stated date, however many sessions the window held.</li>
        </ul>
        <p class="stamp">{stamp(t["asof"]["mc"])}</p>
      </article>'''

    fv_card = f'''
      <article class="card lens-fv">
        <header><span class="lensdot fv"></span><h3>Fundamental</h3><span class="htag">≈ 12 months</span></header>
        <div class="fvhero">
          <div class="fvcell"><span class="k">bear</span><span class="v num">{f2(f["bear"])}</span><span class="d num">{pct_vs(spot, f["bear"])}</span></div>
          <div class="fvcell base"><span class="k">base</span><span class="v num">{f2(f["base"])}</span><span class="d num">{pct_vs(spot, f["base"])}</span></div>
          <div class="fvcell"><span class="k">full</span><span class="v num">{f2(f["full"])}</span><span class="d num">{pct_vs(spot, f["full"])}</span></div>
        </div>
        {FUND_PROSE[tk]}
        <p class="fine">Fair value is a value anchor, not a dated price forecast: it is where the study says value
        sits if the thesis holds, shown on the 12-month shelf for horizon context. It moves on its own study
        clock — a cone re-strike never touches it.</p>
        <p class="stamp">study {m["study_date"]} · <a href="https://testahil.com/{tk.lower()}.html">full study &amp; open model</a></p>
      </article>'''

    return f'''
  <section class="ticker" id="{tk}">
    <div class="thead">
      <h2>{esc(t["name"])} <span class="code num">{esc(t["code"])}</span></h2>
      <span class="spotchip num">{f2(spot)} {t["ccy"]} · {esc(t["spotDate"])}</span>
    </div>
    <div class="canvas-wrap" data-tk="{tk}">
      <div class="canvas-scroll">{svg}</div>
      <div class="tip" id="tip-{tk}" hidden><div class="tiptitle"></div><div class="tiprows"></div></div>
    </div>
    {align}
    <p class="alignnote">Three independent computations — nothing above feeds anything else. Agreement between
    the lenses is information; disagreement is a question worth asking.</p>
    <div class="cards">{tech_card}{mc_card}{fv_card}</div>
  </section>'''


# ---------------------------------------------------------------- page shell

CSS = """
:root{
  --paper:#F6F8F7; --card:#FFFFFF; --ink:#0E2726; --muted:#5B7270;
  --line:#D9E4E2; --tint:#E6F2EE; --brand:#12796B; --brand2:#178A76;
  --lens-mc:#0B8A71; --lens-ta:#B8860B; --lens-fv:#5B6FC0;
  --wash-mc:rgba(11,138,113,.10); --wash-mc2:rgba(11,138,113,.16);
  --wash-fv:rgba(91,111,192,.12); --halo:#FFFFFF;
  --up:#2E7D5B; --dn:#B5483A;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#0D1F1D; --card:#15302D; --ink:#E7EFEC; --muted:#9DB3AF;
    --line:#26433F; --tint:#1B3B37; --brand:#4FB3A4; --brand2:#63C7B8;
    --lens-mc:#3AA491; --lens-ta:#B28A28; --lens-fv:#6F84D8;
    --wash-mc:rgba(58,164,145,.14); --wash-mc2:rgba(58,164,145,.22);
    --wash-fv:rgba(111,132,216,.16); --halo:#15302D;
    --up:#54B583; --dn:#E07767;
  }
}
:root[data-theme="dark"]{
  --paper:#0D1F1D; --card:#15302D; --ink:#E7EFEC; --muted:#9DB3AF;
  --line:#26433F; --tint:#1B3B37; --brand:#4FB3A4; --brand2:#63C7B8;
  --lens-mc:#3AA491; --lens-ta:#B28A28; --lens-fv:#6F84D8;
  --wash-mc:rgba(58,164,145,.14); --wash-mc2:rgba(58,164,145,.22);
  --wash-fv:rgba(111,132,216,.16); --halo:#15302D;
  --up:#54B583; --dn:#E07767;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,sans-serif;font-size:.95rem;line-height:1.55}
.wrap{max-width:1120px;margin:0 auto;padding:28px 20px 64px}
h1,h2,h3{font-family:"Alexandria","IBM Plex Sans",sans-serif;margin:0}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.num{font-family:"IBM Plex Mono",ui-monospace,monospace;font-feature-settings:"tnum"}
.masthead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.masthead h1{font-weight:800;font-size:1.9rem;color:var(--brand)}
.trialtag{font-size:.7rem;letter-spacing:.12em;font-weight:600;color:var(--lens-ta);
  border:1px solid currentColor;border-radius:999px;padding:2px 10px;text-transform:uppercase}
.lede{max-width:70ch;color:var(--ink);margin:.6em 0 0}
.lede b{color:var(--brand)}
.howto{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:18px 0 6px}
@media(max-width:760px){.howto{grid-template-columns:1fr}}
.howto div{background:var(--tint);border-radius:10px;padding:10px 14px;font-size:.85rem}
.howto b{display:block;font-family:"Alexandria",sans-serif}
.howto .mc b{color:var(--lens-mc)}.howto .ta b{color:var(--lens-ta)}.howto .fv b{color:var(--lens-fv)}
.legend{display:flex;gap:18px;flex-wrap:wrap;margin:16px 0 4px;font-size:.82rem;color:var(--muted)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.key{display:inline-block;width:20px;height:0;border-top:2.5px solid}
.key.ink{border-color:var(--ink)}.key.ta{border-color:var(--lens-ta)}
.key.fv{border-color:var(--lens-fv)}
.key.mcband{width:20px;height:12px;border:0;background:var(--wash-mc2);border-radius:3px}
.key.mcline{border-color:var(--lens-mc)}
.ticker{margin-top:40px}
.thead{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin-bottom:10px}
.thead h2{font-size:1.35rem;font-weight:700}
.thead .code{font-size:.8rem;color:var(--muted);font-weight:400}
.spotchip{margin-inline-start:auto;background:var(--tint);border-radius:999px;padding:3px 14px;font-size:.82rem}
.canvas-wrap{position:relative;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px 6px 6px}
.canvas-scroll{overflow-x:auto}
.canvas-scroll svg{display:block;min-width:880px;width:100%;height:auto}
svg text{font-family:"IBM Plex Sans",system-ui,sans-serif;fill:var(--ink)}
svg .num,svg .endlab{font-family:"IBM Plex Mono",ui-monospace,monospace}
.grid{stroke:var(--line);stroke-width:1;opacity:.55}
.axis{stroke:var(--line);stroke-width:1.2}
.axisbreak{stroke:var(--muted);stroke-width:1.4}
.zoneline{stroke:var(--line);stroke-width:1.2}
.tick{font-size:10.5px;fill:var(--muted)}
.cap{font-size:9.5px;fill:var(--muted);letter-spacing:.09em}
.hist{fill:none;stroke:var(--ink);stroke-width:1.8;stroke-linejoin:round;opacity:.82}
.nowline{stroke:var(--muted);stroke-width:1;opacity:.55}
.checkline{stroke:var(--line);stroke-width:1;opacity:.8}
.cone90{fill:var(--wash-mc)}.cone50{fill:var(--wash-mc2)}
.median{fill:none;stroke:var(--lens-mc);stroke-width:2.2;stroke-linecap:round}
.talvl{stroke:var(--lens-ta);stroke-width:2;stroke-linecap:round}
.lvllab{font-size:10.5px}.lvlkey{fill:var(--lens-ta);font-weight:600}
.leader{stroke-width:1;opacity:.5}.leader.mc{stroke:var(--lens-mc)}
.endlab{font-size:11px}.endlab.strong{font-weight:600}
.qtag{fill:var(--muted);font-size:9px;letter-spacing:.04em}
.fvwash{fill:var(--wash-fv)}
.fvspine{stroke:var(--lens-fv);stroke-width:2.4;stroke-linecap:round}
.fvtick{stroke:var(--lens-fv);stroke-width:2}
.spotref{stroke:var(--muted);stroke-width:1;opacity:.5}
.dot{stroke:var(--card);stroke-width:2}
.dot.mc{fill:var(--lens-mc)}.dot.fv{fill:var(--lens-fv)}.dot.inkdot{fill:var(--ink)}
.halo{paint-order:stroke fill;stroke:var(--halo);stroke-width:3px;stroke-linejoin:round}
.crosshair{stroke:var(--muted);stroke-width:1;opacity:.65;pointer-events:none}
.hit{fill:transparent;outline:none}
.hit:focus-visible{fill:var(--tint);opacity:.25}
.tip{position:absolute;pointer-events:none;background:var(--card);border:1px solid var(--line);
  border-radius:9px;box-shadow:0 6px 18px rgba(0,0,0,.14);padding:8px 11px;min-width:150px;z-index:5}
.tiptitle{font-size:.72rem;color:var(--muted);margin-bottom:4px}
.tiprows div{display:flex;justify-content:space-between;gap:16px;font-size:.8rem}
.tiprows .tl{color:var(--muted)}
.tiprows .tv{font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:600}
.align{display:flex;align-items:stretch;gap:10px;flex-wrap:wrap;margin:16px 2px 0}
.al-item{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:7px 14px;
  display:flex;flex-direction:column;gap:1px}
.al-item .k{font-size:.68rem;letter-spacing:.07em;text-transform:uppercase;font-weight:600;color:var(--muted)}
.al-item .k.mc{color:var(--lens-mc)}.al-item .k.fv{color:var(--lens-fv)}.al-item .k.ink{color:var(--muted)}
.al-item .v{font-size:1.05rem;font-weight:600}
.al-item .v em{font-style:normal;font-size:.72rem;color:var(--muted);margin-inline-start:7px}
.al-arrow{align-self:center;color:var(--muted)}
.alignnote{font-size:.8rem;color:var(--muted);margin:8px 2px 0;max-width:80ch}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}
@media(max-width:920px){.cards{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 16px 12px;
  border-top:3px solid var(--line)}
.card.lens-ta{border-top-color:var(--lens-ta)}
.card.lens-mc{border-top-color:var(--lens-mc)}
.card.lens-fv{border-top-color:var(--lens-fv)}
.card header{display:flex;align-items:baseline;gap:8px;margin-bottom:8px}
.card h3{font-size:1rem;font-weight:700}
.htag{margin-inline-start:auto;font-size:.7rem;color:var(--muted);letter-spacing:.05em}
.lensdot{width:9px;height:9px;border-radius:50%;align-self:center}
.lensdot.ta{background:var(--lens-ta)}.lensdot.mc{background:var(--lens-mc)}.lensdot.fv{background:var(--lens-fv)}
.trend{font-weight:600;margin:.1em 0 .4em}
.body{font-size:.85rem;margin:.4em 0}
.lvlgrid{display:grid;gap:8px;margin:10px 0}
.lvlhead{display:block;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600}
.lvlrow{font-size:.88rem}
.trigger{font-size:.83rem;margin:.35em 0}
.fine{font-size:.74rem;color:var(--muted);margin:.6em 0 0}
.fineul{font-size:.74rem;color:var(--muted);padding-inline-start:18px;margin:.6em 0 0}
.fineul li{margin:.25em 0}
.stamp{font-size:.7rem;color:var(--muted);border-top:1px solid var(--line);margin:.9em -16px 0;padding:8px 16px 0}
.card .stamp{margin-bottom:0}
.dirchip{font-size:.82rem;margin:.2em 0 .7em}
.dirsign{font-weight:700;color:var(--lens-mc);letter-spacing:.04em}
.chip{display:inline-block;background:var(--tint);border-radius:999px;padding:0 10px;font-size:.72rem;color:var(--brand)}
table.mini{width:100%;border-collapse:collapse;font-size:.8rem;margin:.4em 0}
table.mini th{font-size:.68rem;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);
  font-weight:600;text-align:right;padding:3px 6px;border-bottom:1px solid var(--line)}
table.mini th:first-child,table.mini td:first-child{text-align:left}
table.mini td{padding:4px 6px;text-align:right;border-bottom:1px solid var(--line)}
table.mini td .sub{display:block;font-size:.68rem;color:var(--muted);font-family:"IBM Plex Sans",sans-serif}
.tarr.up{color:var(--up)}.tarr.dn{color:var(--dn)}
details.touch{margin:.5em 0}
details.touch summary{cursor:pointer;font-size:.78rem;color:var(--brand);font-weight:600}
.fvhero{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:.2em 0 .8em}
.fvcell{background:var(--tint);border-radius:10px;padding:8px 10px;text-align:center}
.fvcell.base{outline:2px solid var(--lens-fv);outline-offset:-2px}
.fvcell .k{display:block;font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}
.fvcell .v{display:block;font-size:1.05rem;font-weight:600}
.fvcell .d{display:block;font-size:.7rem;color:var(--muted)}
.crux,.caveat{font-size:.8rem;margin:.5em 0}
.caveat{color:var(--muted)}
.foot{margin-top:44px;border-top:1px solid var(--line);padding-top:14px;font-size:.74rem;color:var(--muted);max-width:90ch}
.foot p{margin:.35em 0}
@media (prefers-reduced-motion: no-preference){.tip{transition:opacity .1s linear}}
"""

JS = r"""
(function(){
  function wire(wrap){
    var tk = wrap.getAttribute('data-tk');
    var D = TL_DATA[tk];
    var svg = wrap.querySelector('svg');
    var tip = document.getElementById('tip-'+tk);
    var xh = document.getElementById('xh-'+tk);
    var title = tip.querySelector('.tiptitle');
    var rowsEl = tip.querySelector('.tiprows');
    function setRows(t, rows){
      title.textContent = t;
      rowsEl.textContent = '';
      rows.forEach(function(r){
        var d=document.createElement('div'), a=document.createElement('span'), b=document.createElement('span');
        a.className='tl'; a.textContent=r[0]; b.className='tv'; b.textContent=r[1];
        d.appendChild(a); d.appendChild(b); rowsEl.appendChild(d);
      });
    }
    function place(svgX, clientY){
      var r = svg.getBoundingClientRect(), wr = wrap.getBoundingClientRect();
      var px = r.left - wr.left + svgX / D.vbw * r.width;
      tip.hidden = false;
      var w = tip.offsetWidth;
      tip.style.left = Math.max(4, Math.min(px + 14, wr.width - w - 8)) + 'px';
      tip.style.top = (clientY - wr.top - tip.offsetHeight - 14) + 'px';
      xh.setAttribute('x1', svgX); xh.setAttribute('x2', svgX); xh.style.display = '';
    }
    function nearest(arr, x, key){
      var best = null, bd = 1e9;
      arr.forEach(function(o){ var d = Math.abs(o[key] - x); if (d < bd){ bd = d; best = o; } });
      return best;
    }
    function show(zone, svgX, clientY){
      if (zone === 'hist'){
        var s = nearest(D.sessions, svgX, 'x');
        if (!s) return;
        setRows(s.d, [['close', s.c]]);
        place(s.x, clientY);
      } else if (zone === 'cone'){
        var c = nearest(D.cols, svgX, 'x');
        setRows(c.title, c.rows);
        place(c.x, clientY);
      } else {
        setRows(D.shelf.title, D.shelf.rows);
        place(D.shelf.x, clientY);
      }
    }
    function svgXof(ev){
      var r = svg.getBoundingClientRect();
      return (ev.clientX - r.left) / r.width * D.vbw;
    }
    wrap.querySelectorAll('.hit').forEach(function(h){
      var zone = h.getAttribute('data-zone');
      h.addEventListener('pointermove', function(ev){ show(zone, svgXof(ev), ev.clientY); });
      h.addEventListener('pointerleave', function(){ tip.hidden = true; xh.style.display = 'none'; });
      h.addEventListener('focus', function(){
        var mid = zone==='hist' ? D.sessions[D.sessions.length-1] : zone==='cone' ? D.cols[2] : D.shelf;
        show(zone, mid.x, wrap.getBoundingClientRect().top + 170);
      });
      h.addEventListener('blur', function(){ tip.hidden = true; xh.style.display = 'none'; });
    });
  }
  document.querySelectorAll('.canvas-wrap').forEach(wire);
})();
"""


def render_inner(models, blobs, sha, today):
    tks = [m["tk"] for m in models]
    names = " and ".join(m["t"]["name"] for m in models)
    sections = "".join(m["_section"] for m in models)
    inner = f'''
<div class="wrap">
  <header class="masthead">
    <h1>Three clocks, one tape</h1>
    <span class="trialtag">trial · {" + ".join(tks)}</span>
  </header>
  <p class="lede">One canvas per name, three <b>independent</b> reads of the same stock on one price axis.
  Each is computed on its own clock, by its own method, and none feeds another — so where they agree,
  that agreement is evidence, not an echo.</p>
  <div class="howto">
    <div class="ta"><b>Technical · days–weeks</b>The computed support / resistance ladder over the near-term
      window: exit and trim references above the price, entry and stop references below, with the bull and bear
      triggers spelled out.</div>
    <div class="mc"><b>Monte Carlo · 1–3 months</b>The published probability cone of the current strike:
      the 90% band, the central 50%, and the median path to the two calendar check dates — plus this
      name’s own track record of how often those bands held.</div>
    <div class="fv"><b>Fundamental · ≈ 12 months</b>The study’s fair-value range — bear, base,
      full — drawn as a floating bracket on its own shelf. A value anchor on the study’s clock, deliberately
      not connected to the cone.</div>
  </div>
  <div class="legend">
    <span><span class="key ink"></span>price history</span>
    <span><span class="key ta"></span>technical ladder</span>
    <span><span class="key mcband"></span>MC 90% / central 50% band</span>
    <span><span class="key mcline"></span>MC median</span>
    <span><span class="key fv"></span>fair-value range</span>
  </div>
  {sections}
  <footer class="foot">
    <p><b>Provenance.</b> Generated by <span class="num">engine/lab/three_lens_trial/build_three_lens_trial.py</span>
    on {today} from <span class="num">assets/data.js</span> and the raw price libraries at commit
    <span class="num">{sha}</span>; the calibration sentences render through the house
    <span class="num">band_record</span> phrasing. Every number is machine-read and cross-asserted
    ({len(CHECKS)} checks passed); nothing is typed. Regenerate rather than edit.</p>
    <p><b>Standing caveats.</b> Fundamental ranges are shown as published, on their own study clocks; studies
    predating the current build standard are queued for re-issue under it. Probability bands and fair-value
    ranges only — never a rating, never a price target. Trial surface: {names}; not linked from the live site.
    Educational analysis, not investment advice.</p>
  </footer>
</div>
<script>var TL_DATA = {json.dumps({k: blobs[k] for k in tks})};</script>
<script>{JS}</script>'''
    return inner


HEAD_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
              '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
              '<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@700;800&'
              'family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">')


def wrap_standalone(inner, title):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
{HEAD_FONTS}
<script>(function(){{try{{var t=localStorage.getItem('theme');if(t==='dark'){{document.documentElement.setAttribute('data-theme','dark');}}else if(t==='light'){{document.documentElement.setAttribute('data-theme','light');}}}}catch(e){{}}}})();</script>
<style>{CSS}</style>
</head>
<body>
{inner}
</body>
</html>'''


def wrap_fragment(inner, title):
    """Body-content page for surfaces that supply their own document skeleton."""
    return f'''<title>{title}</title>
{HEAD_FONTS}
<style>{CSS}
body{{background:var(--paper)}}</style>
{inner}'''


def build_pages(models):
    blobs = {}
    for m in models:
        svg, g = svg_canvas(m)
        m["_section"] = ticker_section(m, g, svg)
        blobs[m["tk"]] = hover_json(m, g)
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip() or "worktree"
    today = dlong(date.today().isoformat())
    standalone = wrap_standalone(render_inner(models, blobs, sha, today), "Three Clocks")
    fragments = {m["tk"]: wrap_fragment(render_inner([m], blobs, sha, today),
                                        f"Three Clocks · {m['tk']}")
                 for m in models}
    return standalone, fragments


def main():
    data = load_data_js()
    models = [extract(tk, data) for tk in TRIAL]
    standalone, fragments = build_pages(models)
    for s in [standalone] + list(fragments.values()):
        must(">None<" not in s and ">None " not in s, "page", "no Python None leaked into markup")
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(standalone)
    frag_dir = os.environ.get("TL_FRAGMENT_DIR")
    if frag_dir:
        for tk, frag in fragments.items():
            with open(os.path.join(frag_dir, f"three_clocks_{tk.lower()}.html"), "w", encoding="utf-8") as f:
                f.write(frag)
    print(f"wrote {os.path.relpath(OUT_HTML, ROOT)}  ({len(standalone):,} bytes)"
          + (f" + {len(fragments)} per-ticker fragments -> {frag_dir}" if frag_dir else ""))
    print(f"{len(CHECKS)} assertions passed across {', '.join(TRIAL)}")


if __name__ == "__main__":
    main()
