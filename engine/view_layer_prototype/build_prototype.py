"""build_prototype.py — Move 1 show-piece: the proposed "view layer" ticker card.

STATUS: PROTOTYPE. NOT LIVE, NOT PUBLISHED. Generates a standalone HTML page
showing what a redesigned ticker card would look like, for three real covered
names, built ONLY from numbers already published on the site:

  * assets/data.js            spot, spotDate, dist (published cone), fair values
  * fv_overlay output         P(touch fair value), reachability band, sigma/mu
  * engine/raw_ohlc           the actual price line behind the fan (cleaned)

Nothing is refit and nothing published is modified. The intermediate months of
the cone are drawn by interpolating the published anchors with the same
standardized-t quantile math fv_overlay uses; the drawn band is asserted to
reproduce the PUBLISHED p5/p25/p50/p75/p95 at 1M and 3M within 2.5%.

Design decisions the prototype demonstrates (client critique, 23-Aug-2026):
  1. The TYPICAL range (middle-half band) leads; the 9-in-10 band becomes a
     thin whisker — same information, honest hierarchy.
  2. A second object carries DIRECTION: the valuation path from today's price
     to the study's bear/base/full values over 12 months (teal = market's
     odds, orange = our view; palette validated for color-vision safety).
  3. A plain-English verdict line whose every number is computed from the
     data, never typed.

Usage
-----
    python3 engine/fv_overlay.py --json /tmp/overlay.json
    python3 engine/view_layer_prototype/build_prototype.py \
        --overlay /tmp/overlay.json \
        --tournament engine/direction_tournament/RESULTS_23-08-2026.json \
        --out engine/view_layer_prototype/PROTOTYPE_23-08-2026.html \
        --tickers ETEL,ADNOCDRILL,EMFD
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

ENG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ENG)
from fv_overlay import load_tickers                     # noqa: E402
from data_quality import clean_ohlc                     # noqa: E402

MAX_BAND_DEV = 0.025          # drawn band must reproduce published quantiles
HIST_MONTHS = 9               # actual price shown behind the fan
VIEW_MONTHS = 12              # valuation path horizon
PCTS = (0.05, 0.25, 0.50, 0.75, 0.95)

TEAL, TEAL2 = "#12796B", "#178A76"
ORANGE = "#D06A2C"            # site hue (gauge gradient); validated vs teal
INK, MUTED, LINE, PAPER = "#0E2726", "#5B7270", "#D9E4E2", "#F6F8F7"


# ------------------------------------------------------------------- helpers
def tq(p: float, nu: float) -> float:
    """Unit-variance Student-t quantile — same convention as fv_overlay §2."""
    return float(np.sqrt((nu - 2) / nu) * stats.t.ppf(p, nu))


def month_curves(row: dict, spot: float):
    """Cone quantiles at fractional months 0..3, through the published anchors.

    Variance and drift are interpolated linearly BETWEEN the two published
    anchors (sqrt-time below 1M), then mapped through the same standardized-t
    the engine simulates with. The result is checked against the published
    quantiles at both anchors by the caller.
    """
    nu = row["engine"]["nu"]
    s1, m1 = row["1M"]["sigma_h"], row["1M"]["mu_h"]
    s3, m3 = row["3M"]["sigma_h"], row["3M"]["mu_h"]
    v1, v3 = s1 * s1, s3 * s3
    out = {}
    for t in [i / 4 for i in range(0, 13)]:             # 0, .25 … 3.0 months
        if t <= 1:
            v, m = v1 * t, m1 * t
        else:
            f = (t - 1) / 2
            v, m = v1 + (v3 - v1) * f, m1 + (m3 - m1) * f
        s = float(np.sqrt(max(v, 0.0)))
        out[t] = {p: spot * float(np.exp(m + s * tq(p, nu))) for p in PCTS}
    return out


def check_band(curves: dict, tick: dict) -> float:
    """Max relative deviation of the drawn band vs the PUBLISHED quantiles."""
    worst = 0.0
    for t, key in ((1.0, "t20"), (3.0, "t60")):
        pub = tick["dist"][key]
        for p, name in zip(PCTS, ("p5", "p25", "p50", "p75", "p95")):
            dev = abs(curves[t][p] / pub[name] - 1)
            worst = max(worst, dev)
    return worst


def price_history(market: str, ticker: str, anchor: pd.Timestamp):
    path = os.path.join(ENG, "raw_ohlc", market, f"{ticker}.csv")
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _ = clean_ohlc(df, ticker=ticker, verbose=False, market=market)
    df = df[df["Date"] <= anchor]
    start = anchor - pd.DateOffset(months=HIST_MONTHS)
    df = df[df["Date"] >= start]
    df = df.iloc[::5]                                   # weekly-ish sampling
    return [(-round((anchor - d).days / 30.44, 2), float(p))
            for d, p in zip(df["Date"], df["Price"])]


def fmt(x: float, ref: float) -> str:
    if ref >= 1000:
        return f"{x:,.0f}"
    if ref >= 100:
        return f"{x:,.1f}"
    return f"{x:,.2f}"


def odds_words(p: float | None, band: str) -> str:
    if p is None:
        return "not measurable on a 3-month clock"
    if p < 0.01:
        return "under 1 in 100"
    if p < 0.05:
        return f"about 1 in {round(1 / p)}"
    return f"about {round(p * 100)}%"


# ---------------------------------------------------------------- card build
def build_card(tick: dict, row: dict, hist) -> tuple[str, dict, float]:
    spot = float(tick["spot"])
    ccy = tick.get("ccy", "")
    fv = {k: float(tick["fair"][k]) for k in ("bear", "base", "full")}
    curves = month_curves(row, spot)
    dev = check_band(curves, tick)

    gap = fv["base"] / spot - 1
    p_touch = (row["3M"].get("p_touch") or {}).get("base")
    band3 = row["3M"]["band"]
    dir_word = "worth more than today's price" if gap > 0.02 else (
        "worth less than today's price" if gap < -0.02 else
        "roughly fairly priced today")
    story = ""
    if band3 in ("OUT-OF-REACH", "NOT-EXPRESSIBLE") and abs(gap) > 0.2:
        story = (" A move that size almost never happens in three months in "
                 "this stock — this is a 12-month story, not a quarter trade.")
    verdict = (f"Our view: {dir_word}. We value it at "
               f"{fmt(fv['base'], spot)} {ccy} "
               f"(range {fmt(fv['bear'], spot)}–{fmt(fv['full'], spot)}), "
               f"{'+' if gap >= 0 else '−'}{abs(gap) * 100:.0f}% vs the market. "
               f"Odds the price {'reaches' if gap >= 0 else 'falls to'} our "
               f"value within 3 months: {odds_words(p_touch, band3)}.{story}")

    # ---- chart geometry -----------------------------------------------------
    W, H, L, R, T, B = 860, 380, 64, 118, 18, 40
    view = {t: {k: spot * (fv[k] / spot) ** (t / VIEW_MONTHS)
                for k in ("bear", "base", "full")}
            for t in [i / 2 for i in range(0, VIEW_MONTHS * 2 + 1)]}
    ys = ([p for _, p in hist]
          + [v for c in curves.values() for v in c.values()]
          + [v for c in view.values() for v in c.values()])
    ylo, yhi = min(ys), max(ys)
    pad = (yhi - ylo) * 0.07
    ylo, yhi = ylo - pad, yhi + pad
    x0, x1 = -HIST_MONTHS, VIEW_MONTHS

    def X(m): return L + (m - x0) / (x1 - x0) * (W - L - R)
    def Y(p): return T + (yhi - p) / (yhi - ylo) * (H - T - B)

    def path(pts, close_to=None):
        d = "M" + " L".join(f"{X(m):.1f},{Y(p):.1f}" for m, p in pts)
        if close_to is not None:
            d += " L" + " L".join(f"{X(m):.1f},{Y(p):.1f}"
                                  for m, p in reversed(close_to))
            d += " Z"
        return d

    tgrid = sorted(curves)
    band90 = path([(t, curves[t][0.95]) for t in tgrid],
                  close_to=[(t, curves[t][0.05]) for t in tgrid])
    band50 = path([(t, curves[t][0.75]) for t in tgrid],
                  close_to=[(t, curves[t][0.25]) for t in tgrid])
    median = path([(t, curves[t][0.50]) for t in tgrid])
    vgrid = sorted(view)
    wedge = path([(t, view[t]["full"]) for t in vgrid],
                 close_to=[(t, view[t]["bear"]) for t in vgrid])
    vbase = path([(t, view[t]["base"]) for t in vgrid])
    histp = path(hist)

    # y gridlines: 5 round steps
    step = (yhi - ylo) / 5
    mag = 10 ** np.floor(np.log10(step))
    step = float(np.ceil(step / mag) * mag)
    gys = np.arange(np.ceil(ylo / step) * step, yhi, step)
    grid = "".join(
        f'<line x1="{L}" x2="{W-R}" y1="{Y(g):.1f}" y2="{Y(g):.1f}" '
        f'stroke="{LINE}" stroke-width="1" opacity=".6"/>'
        f'<text x="{L-8}" y="{Y(g)+4:.1f}" text-anchor="end" class="ax">'
        f'{fmt(g, spot)}</text>' for g in gys)
    xt = "".join(
        f'<line x1="{X(m):.1f}" x2="{X(m):.1f}" y1="{H-B}" y2="{H-B+5}" '
        f'stroke="{MUTED}"/>'
        f'<text x="{X(m):.1f}" y="{H-B+18}" text-anchor="middle" class="ax">'
        f'{lab}</text>'
        for m, lab in [(-6, "6m ago"), (-3, "3m ago"), (0, "today"),
                       (3, "+3 months"), (6, "+6 months"), (12, "+12 months")])

    # right-edge direct labels for the view fan
    fanlab = "".join(
        f'<text x="{X(12)+6:.1f}" y="{Y(view[12][k])+4:.1f}" class="fl" '
        f'fill="{ORANGE}">{lab} {fmt(fv[k], spot)}</text>'
        for k, lab in (("full", "high"), ("base", "base"), ("bear", "low")))

    p25, p75 = tick["dist"]["t60"]["p25"], tick["dist"]["t60"]["p75"]
    p5, p95 = tick["dist"]["t60"]["p5"], tick["dist"]["t60"]["p95"]
    bandlab = (f'<text x="{X(3)+6:.1f}" y="{Y(p75)-7:.1f}" class="fl" '
               f'fill="{TEAL}">typical {fmt(p25, spot)}–{fmt(p75, spot)}</text>'
               f'<text x="{X(3)+6:.1f}" y="{Y(p5)+10:.1f}" class="fl" '
               f'fill="{MUTED}">9-in-10 {fmt(p5, spot)}–{fmt(p95, spot)}</text>')

    tid = tick["_ticker"]
    svg = f"""
<svg viewBox="0 0 {W} {H}" role="img" data-chart="{tid}"
     aria-label="{html.escape(tick['name'])} — market range and valuation path">
  <style>.ax{{font:11px 'IBM Plex Mono',monospace;fill:{MUTED}}}
         .fl{{font:600 11px 'IBM Plex Sans',sans-serif}}</style>
  {grid}{xt}
  <line x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{T}" y2="{H-B}" stroke="{MUTED}"
        stroke-dasharray="3 4" opacity=".7"/>
  <path d="{band90}" fill="{TEAL}" opacity="0.10"/>
  <path d="{band50}" fill="{TEAL}" opacity="0.28"/>
  <path d="{median}" fill="none" stroke="{TEAL}" stroke-width="1.5"
        stroke-dasharray="5 4" opacity=".8"/>
  <path d="{wedge}" fill="{ORANGE}" opacity="0.13"/>
  <path d="{vbase}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>
  <path d="{histp}" fill="none" stroke="{INK}" stroke-width="2"/>
  <circle cx="{X(0):.1f}" cy="{Y(spot):.1f}" r="5" fill="#fff"
          stroke="{INK}" stroke-width="2.5"/>
  {fanlab}{bandlab}
  <line class="cx" x1="0" x2="0" y1="{T}" y2="{H-B}" stroke="{INK}"
        opacity="0" stroke-width="1"/>
</svg>"""

    tiles = f"""
<div class="tiles">
  <div class="tile"><div class="tl">Our value (base)</div>
    <div class="tv num">{fmt(fv['base'], spot)} {ccy}</div>
    <div class="ts">full range {fmt(fv['bear'], spot)}–{fmt(fv['full'], spot)}</div></div>
  <div class="tile"><div class="tl">Typical range, next 3 months</div>
    <div class="tv num">{fmt(p25, spot)}–{fmt(p75, spot)}</div>
    <div class="ts">1-in-10 above {fmt(p95, spot)}, 1-in-10 below {fmt(p5, spot)}</div></div>
  <div class="tile"><div class="tl">Odds of {'reaching' if gap >= 0 else 'falling to'} our value in 3M</div>
    <div class="tv num">{odds_words(p_touch, band3)}</div>
    <div class="ts">graded publicly when the date arrives</div></div>
</div>"""

    hover = {"x0": x0, "x1": x1, "L": L, "R": R, "W": W, "spot": spot,
             "hist": hist,
             "band": {str(t): [curves[t][p] for p in PCTS] for t in tgrid},
             "view": {str(t): [view[t][k] for k in ("bear", "base", "full")]
                      for t in vgrid}}

    card = f"""
<section class="card">
  <div class="head">
    <div><span class="tk">{tid}</span> <span class="nm">{html.escape(tick['name'])}</span>
      <span class="ex">{html.escape(tick.get('code', ''))}</span></div>
    <div class="px num">{fmt(spot, spot)} {ccy}
      <span class="pxd">{html.escape(str(tick.get('spotDate', '')))}</span></div>
  </div>
  <p class="verdict">{verdict}</p>
  <div class="legend">
    <span><i style="background:{TEAL};opacity:.35"></i> market's likely range (next 3M)</span>
    <span><i style="background:{ORANGE}"></i> our valuation path (12M)</span>
    <span><i style="background:{INK}"></i> actual price (last {HIST_MONTHS}M)</span>
  </div>
  <div class="chartwrap">{svg}<div class="tip" hidden></div></div>
  {tiles}
  <p class="foot">Valuation dated {row['fv_asof']} · market range struck {row['anchor_date']} ·
  every number above is already published on the live page today — this card only re-arranges them.</p>
</section>"""
    return card, hover, dev


# -------------------------------------------------------------- tournament §
def tournament_section(path: str | None) -> str:
    if not path or not os.path.exists(path):
        return ""
    with open(path) as f:
        tr = json.load(f)
    rows = []
    for mk in tr["markets"]:
        for key, cell in (mk.get("results") or {}).items():
            ts, xs = cell.get("TS") or {}, cell.get("XS") or {}
            if "ic_spearman" not in ts and not xs:
                continue
            feat, hz = key.split("|")
            rows.append({
                "mkt": mk["market"], "feat": feat, "hz": hz,
                "n": ts.get("n"), "ic": ts.get("ic_spearman"),
                "v": ts.get("verdict", "—"), "hit": ts.get("hit_rate"),
                "xsic": xs.get("mean_ic"), "xsv": xs.get("verdict", "—"),
                "sp": xs.get("tercile_spread_mean_pct")})
    if not rows:
        return ""
    core = [r for r in rows if r["mkt"] in ("EG", "AE", "SA")]
    strongest = sorted((r for r in core if r["ic"] is not None),
                       key=lambda r: -abs(r["ic"]))[:8]
    trs = "".join(
        f"<tr><td>{r['mkt']}</td><td>{FEAT_WORDS.get(r['feat'], r['feat'])}</td>"
        f"<td>{r['hz']}</td><td class='num'>{r['n'] or '—'}</td>"
        f"<td class='num'>{r['ic']:+.3f}</td><td>{VERDICT_WORDS.get(r['v'], r['v'])}</td>"
        f"<td class='num'>{r['hit']:.0%}</td>"
        f"<td class='num'>{('%+.3f' % r['xsic']) if r['xsic'] is not None else '—'}</td>"
        f"<td class='num'>{('%+.2f%%' % r['sp']) if r['sp'] is not None else '—'}</td></tr>"
        for r in strongest if r["ic"] is not None and r["hit"] is not None)
    surv = tr.get("survivors") or []
    if surv:
        sv = ("<p><b>Survivors:</b> " + "; ".join(
            f"{s['feature']} at {s['horizon']} in {s['market']} "
            f"(IC {s['pooled_ic']:+.3f}, n={s['n']})" for s in surv) +
            ". A survivor is a candidate for the standing out-of-sample "
            "promotion gate — not an adoption.</p>")
    else:
        sv = ("<p><b>Result: no survivor.</b> None of the six indicators "
              "predicts 1- or 3-month direction reliably enough to tilt a "
              "cone, in any market, once we demand the same evidence in both "
              "halves of history and from every angle at once. That is a "
              "finding, not a failure: it is why the honest direction on "
              "these pages comes from the valuation work (the orange path), "
              "not from chart patterns.</p>")
    return f"""
<section class="card">
  <h2>Part 2 — Can price history give the cone a lean? We tested it.</h2>
  <p>Six standard direction indicators (momentum over 12 and 6 months,
  last-month reversal, distance from the 52-week high, distance from the
  200-day average, and RSI), tested on our own cleaned price library —
  {sum(mk.get('names') or 0 for mk in tr['markets'])} names — at the same
  1-month and 3-month clocks the site publishes, judged by a test that
  rewards <em>getting direction right</em>, with the sample split in half to
  catch flukes. Strongest eight readings in the three core markets:</p>
  <div class="tblwrap"><table>
    <thead><tr><th>market</th><th>indicator</th><th>clock</th><th>obs</th>
    <th>rank skill</th><th>verdict</th><th>direction hit rate</th>
    <th>cross-name skill</th><th>top-vs-bottom third, per period</th></tr></thead>
    <tbody>{trs}</tbody>
  </table></div>
  {sv}
  <p class="foot">Full tables: engine/direction_tournament/RESULTS_23-08-2026.md ·
  research only — nothing adopted, nothing published.</p>
</section>"""


FEAT_WORDS = {"mom_12_1": "12-month momentum", "mom_6_1": "6-month momentum",
              "rev_1m": "1-month reversal", "near52h": "near 52-week high",
              "trend200": "above/below 200-day avg", "rsi14": "RSI(14)"}
VERDICT_WORDS = {"PASS": "predicts UP-side", "FAIL": "predicts DOWN-side",
                 "PARITY": "no reliable signal",
                 "BOUNDARY(PARITY-flagged)": "borderline",
                 "INSUFFICIENT-POWER": "too little data to judge"}


# ------------------------------------------------------------------- doc
CSS = f"""
:root{{--paper:{PAPER};--ink:{INK};--teal:{TEAL};--muted:{MUTED};--line:{LINE}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);
  font:16px/1.55 'IBM Plex Sans',system-ui,sans-serif}}
.num{{font-family:'IBM Plex Mono',monospace;font-feature-settings:'tnum'}}
.wrap{{max-width:960px;margin:0 auto;padding:28px 20px 60px}}
.mast{{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:8px}}
.brand{{font-weight:800;font-size:1.7rem;color:var(--teal)}}
.badge{{background:#FBEFD9;color:#8A6A2E;border:1px solid #E4CFA0;
  font:600 .72rem/1 'IBM Plex Mono',monospace;padding:5px 10px;border-radius:99px}}
.lede{{color:var(--muted);max-width:70ch}}
.card{{background:#fff;border:1px solid var(--line);border-radius:12px;
  padding:20px 22px;margin:22px 0}}
.head{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap}}
.tk{{font:800 1.25rem 'IBM Plex Sans';color:var(--teal)}}
.nm{{font-weight:600}} .ex{{color:var(--muted);font-size:.8rem;margin-left:6px}}
.px{{font-size:1.2rem;font-weight:600}} .pxd{{color:var(--muted);font-size:.72rem;font-weight:400;margin-left:6px}}
.verdict{{font-size:1.02rem;max-width:75ch;margin:.5em 0 .4em}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:.78rem;margin:6px 0 2px}}
.legend i{{display:inline-block;width:14px;height:8px;border-radius:2px;margin-right:5px}}
.chartwrap{{position:relative}}
.chartwrap svg{{width:100%;height:auto;display:block}}
.tip{{position:absolute;pointer-events:none;background:#fff;border:1px solid var(--line);
  border-radius:8px;box-shadow:0 4px 14px rgba(0,0,0,.08);padding:7px 10px;
  font:12px 'IBM Plex Mono',monospace;white-space:pre;z-index:5}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:12px;margin-top:10px}}
.tile{{background:#F4F8F7;border:1px solid var(--line);border-radius:10px;padding:10px 14px}}
.tl{{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
.tv{{font-size:1.15rem;font-weight:700;margin:2px 0}}
.ts{{font-size:.75rem;color:var(--muted)}}
.foot{{color:var(--muted);font-size:.75rem;border-top:1px dashed var(--line);
  padding-top:8px;margin:12px 0 0}}
h2{{font-size:1.2rem;margin:.2em 0 .5em}}
.tblwrap{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:.82rem;min-width:720px}}
th,td{{text-align:left;padding:6px 10px;border-bottom:1px solid var(--line)}}
th{{color:var(--muted);font-weight:600;font-size:.72rem;text-transform:uppercase}}
td.num,th.num{{font-family:'IBM Plex Mono',monospace}}
"""

JS = """
const D = __DATA__;
document.querySelectorAll('[data-chart]').forEach(svg => {
  const d = D[svg.dataset.chart]; if (!d) return;
  const wrap = svg.parentElement, tip = wrap.querySelector('.tip'),
        cx = svg.querySelector('.cx');
  const bt = Object.keys(d.band).map(Number).sort((a,b)=>a-b);
  const vt = Object.keys(d.view).map(Number).sort((a,b)=>a-b);
  const nearest = (arr, m) => arr.reduce((p,c)=>Math.abs(c-m)<Math.abs(p-m)?c:p);
  const fmt = x => d.spot>=1000 ? Math.round(x).toLocaleString('en')
             : d.spot>=100 ? x.toFixed(1) : x.toFixed(2);
  svg.addEventListener('mousemove', ev => {
    const r = svg.getBoundingClientRect();
    const px = (ev.clientX - r.left) / r.width * d.W;
    const m = d.x0 + (px - d.L) / (d.W - d.L - d.R) * (d.x1 - d.x0);
    if (m < d.x0 || m > d.x1) { tip.hidden = true; cx.setAttribute('opacity',0); return; }
    cx.setAttribute('x1', px.toFixed(1)); cx.setAttribute('x2', px.toFixed(1));
    cx.setAttribute('opacity', .35);
    let lines = [];
    if (m <= 0) {
      let best = d.hist.length ? d.hist.reduce((p,c)=>Math.abs(c[0]-m)<Math.abs(p[0]-m)?c:p) : null;
      if (best) lines.push(Math.abs(best[0]).toFixed(1)+'m ago  price '+fmt(best[1]));
    } else {
      lines.push('+'+m.toFixed(1)+' months');
      if (m <= 3) {
        const b = d.band[String(nearest(bt, m))];
        lines.push('typical '+fmt(b[1])+'\\u2013'+fmt(b[3]));
        lines.push('9-in-10 '+fmt(b[0])+'\\u2013'+fmt(b[4]));
      }
      const v = d.view[String(nearest(vt, m))];
      lines.push('our path '+fmt(v[1])+'  (low '+fmt(v[0])+' / high '+fmt(v[2])+')');
    }
    tip.textContent = lines.join('\\n');
    tip.hidden = false;
    const tw = tip.offsetWidth;
    tip.style.left = Math.min(px / d.W * r.width + 14, r.width - tw - 6) + 'px';
    tip.style.top = '18px';
  });
  svg.addEventListener('mouseleave', () => { tip.hidden = true; cx.setAttribute('opacity',0); });
});
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--overlay", required=True)
    ap.add_argument("--tournament", default=None)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tickers", default="ETEL,ADNOCDRILL,EMFD")
    args = ap.parse_args()

    with open(args.overlay) as f:
        overlay = {r["ticker"]: r for r in json.load(f)["rows"]}
    ticks = load_tickers()

    cards, hovers, devs = [], {}, {}
    for tk in args.tickers.split(","):
        tk = tk.strip()
        tick = dict(ticks[tk]); tick["_ticker"] = tk
        row = overlay[tk]
        anchor = pd.Timestamp(row["anchor_date"])
        hist = price_history(row["market"], tk, anchor)
        card, hover, dev = build_card(tick, row, hist)
        cards.append(card)
        hovers[tk] = hover
        devs[tk] = dev
        assert dev <= MAX_BAND_DEV, (
            f"{tk}: drawn band deviates {dev:.2%} from the published cone "
            f"(limit {MAX_BAND_DEV:.1%}) — do not show")
        print(f"[{tk}] band reproduces published quantiles within {dev:.2%}")

    tsec = tournament_section(args.tournament)

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TESTAHIL — view-layer prototype (not live)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;800&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <div class="mast"><span class="brand">تستاهل TESTAHIL</span>
    <span class="badge">PROTOTYPE · NOT LIVE · NOT PUBLISHED</span></div>
  <p class="lede">Proposed ticker card, drawn entirely from numbers already
  published today. Two objects, one picture: the <b style="color:{TEAL}">teal
  band</b> is what the market could plausibly do (the middle-half range leads;
  the faint band is the 9-in-10 range — the crash guard, demoted from headline
  to whisker). The <b style="color:{ORANGE}">orange path</b> is what <i>we</i>
  think it is worth and the road there over 12 months — the direction the
  current pages never show. Hover any chart for the numbers at that date.</p>
  {''.join(cards)}
  {tsec}
  <p class="foot">Built {pd.Timestamp.now().date()} from assets/data.js +
  engine/fv_overlay.py output + the cleaned price library. The drawn market
  band is asserted to reproduce the published cone at both struck horizons
  (worst deviation this build:
  {max(devs.values()):.2%}). Reproduce: engine/view_layer_prototype/build_prototype.py.</p>
</div>
<script>{JS.replace("__DATA__", json.dumps(hovers))}</script>
</body></html>"""

    with open(args.out, "w") as f:
        f.write(doc)
    print(f"wrote {args.out} ({os.path.getsize(args.out) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
