"""build_prototype.py — Move 1 show-piece: the proposed "view layer" ticker card.

STATUS: PROTOTYPE. NOT LIVE, NOT PUBLISHED. Generates a standalone HTML page
showing what a redesigned ticker card would look like, for three real covered
names.

THREE-LENS INDEPENDENCE (design rule, Sherif, 23-Aug-2026): the fundamental
study, the MC price engine, and the technical read are INDEPENDENT lenses —
no lens's output is an input to another. Therefore the direction shown on
this card comes from the MC engine's own price data (the momentum lean the
23-Aug tournament validated, through the engine's existing per-market signal
socket), NEVER from the fundamental fair value. The first cut of this
prototype drew a fan toward the fair value; that is retired. The fundamental
and technical verdicts appear only as a separate side-by-side strip, for
comparison — agreement between independent lenses is information; a blended
lens is just one opinion.

What the card draws:
  * the PUBLISHED cone, typical (middle-half) band leading, 9-in-10 band as
    a faint whisker — asserted to reproduce the live quantiles within 2.5%;
  * the engine's own center, and the ILLUSTRATIVE trend-leaned center:
    alpha = IC x sigma_h x clip(z, +/-2) — the exact Grinold form of the
    engine's existing signal socket — with IC from the tournament's
    surviving 12-month-momentum cell for that market/horizon (zero lean
    where that cell did not survive), and z the name's own momentum vs its
    own history (strictly prior, min 18 monthly points);
  * the actual price line behind it.

COMMITTED DRIFT ADOPTED 23-Aug-2026 (per instruction): the profiles now run
signal_active=True in AE/EG/SA with tournament-measured ICs; this card shows
the production signal_alpha. Live-site numbers change at the next
roll-forward + publish, not before.

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
sys.path.insert(0, os.path.join(ENG, "direction_tournament"))
from fv_overlay import load_tickers                     # noqa: E402
from data_quality import clean_ohlc                     # noqa: E402
from market_profiles import PROFILES                    # noqa: E402
from mc_v3 import signal_alpha                          # noqa: E402

MAX_BAND_DEV = 0.025          # drawn band must reproduce published quantiles
HIST_MONTHS = 9               # actual price shown behind the cone
LEAN_FEATURE = "mom_12_1"     # the only family eligible for the MC lean —
                              # trend200/near52h/rsi belong to the TECHNICAL
                              # lens and are excluded (three-lens independence)
Z_CLIP = 2.0                  # engine's own clip in the signal socket
PCTS = (0.05, 0.25, 0.50, 0.75, 0.95)

TEAL, TEAL2 = "#12796B", "#178A76"
ORANGE = "#D06A2C"            # reserved for the ILLUSTRATIVE leaned center
INK, MUTED, LINE, PAPER = "#0E2726", "#5B7270", "#D9E4E2", "#F6F8F7"


# ------------------------------------------------------------------- helpers
def tq(p: float, nu: float) -> float:
    """Unit-variance Student-t quantile — same convention as fv_overlay §2."""
    return float(np.sqrt((nu - 2) / nu) * stats.t.ppf(p, nu))


def t_cdf_std(x: float, nu: float) -> float:
    """CDF of the unit-variance Student-t at x."""
    return float(stats.t.cdf(x / np.sqrt((nu - 2) / nu), nu))


def interp_mu_var(row: dict, t: float):
    s1, m1 = row["1M"]["sigma_h"], row["1M"]["mu_h"]
    s3, m3 = row["3M"]["sigma_h"], row["3M"]["mu_h"]
    v1, v3 = s1 * s1, s3 * s3
    if t <= 1:
        return m1 * t, v1 * t
    f = (t - 1) / 2
    return m1 + (m3 - m1) * f, v1 + (v3 - v1) * f


def month_curves(row: dict, spot: float, alpha3: float = 0.0):
    """Cone quantiles at fractional months 0..3 through the published anchors.

    alpha3 shifts the drift linearly in time (the leaned variant); alpha3=0
    reproduces the published cone.
    """
    nu = row["engine"]["nu"]
    out = {}
    for t in [i / 4 for i in range(0, 13)]:
        m, v = interp_mu_var(row, t)
        m += alpha3 * (t / 3)
        s = float(np.sqrt(max(v, 0.0)))
        out[t] = {p: spot * float(np.exp(m + s * tq(p, nu))) for p in PCTS}
    return out


def check_band(curves: dict, tick: dict) -> float:
    worst = 0.0
    for t, key in ((1.0, "t20"), (3.0, "t60")):
        pub = tick["dist"][key]
        for p, name in zip(PCTS, ("p5", "p25", "p50", "p75", "p95")):
            worst = max(worst, abs(curves[t][p] / pub[name] - 1))
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
    df = df[df["Date"] >= anchor - pd.DateOffset(months=HIST_MONTHS)]
    df = df.iloc[::5]
    return [(-round((anchor - d).days / 30.44, 2), float(p))
            for d, p in zip(df["Date"], df["Price"])]


def engine_signal(market: str, ticker: str, sigma3: float):
    """The PRODUCTION signal: mc_v3.signal_alpha on the cleaned daily series
    at the latest session, with the market profile as adopted 23-Aug-2026
    (committed drift). Returns (z, alpha3)."""
    path = os.path.join(ENG, "raw_ohlc", market, f"{ticker}.csv")
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _ = clean_ohlc(df, ticker=ticker, verbose=False, market=market)
    close = df["Price"].values
    prof = PROFILES[market]
    a3, z = signal_alpha(prof, close, len(close) - 1, sigma3,
                         ic=(getattr(prof, "ic_by_h", None) or {}).get("3M"))
    return float(z), float(a3)


def fmt(x: float, ref: float) -> str:
    if ref >= 1000:
        return f"{x:,.0f}"
    if ref >= 100:
        return f"{x:,.1f}"
    return f"{x:,.2f}"


# ---------------------------------------------------------------- card build
def build_card(tick: dict, row: dict, hist, tournament: dict) -> tuple[str, dict, float]:
    spot = float(tick["spot"])
    ccy = tick.get("ccy", "")
    market = row["market"]
    nu = row["engine"]["nu"]
    curves = month_curves(row, spot)
    dev = check_band(curves, tick)

    # ---- the MC's own COMMITTED drift (price-native; never the fundamental)
    s3, m3 = row["3M"]["sigma_h"], row["3M"]["mu_h"]
    z, alpha3 = engine_signal(market, tick["_ticker"], s3)
    leaned = month_curves(row, spot, alpha3=alpha3) if alpha3 else None
    p_up_neutral = 1 - t_cdf_std(-m3 / s3, nu)
    p_up_lean = 1 - t_cdf_std(-(m3 + alpha3) / s3, nu)

    call = "UP" if z > 0 else "DOWN"
    if alpha3:
        strength = "strong" if abs(z) > 1.2 else "moderate"
        lean_word = f"commits {call}"
        lean_clause = (f"its last 12 months run {strength} versus its own "
                       f"normal, tilting the 3-month center by "
                       f"{alpha3 * 100:+.1f}%")
    else:
        lean_word = f"calls {call}, weak conviction"
        lean_clause = ("the trend is near flat, so the call carries no tilt "
                       "on the center")
    verdict = (f"The price engine {lean_word}: {lean_clause}. "
               f"Odds of finishing higher in 3 months: "
               f"{p_up_lean * 100:.0f}%"
               + (f" ({p_up_neutral * 100:.0f}% before the tilt)" if alpha3 else "")
               + ". Committed drift adopted 23-Aug-2026 — every call is "
               "graded on its date, publicly.")

    # ---- three independent lenses, side by side ---------------------------
    fv_base = float(tick["fair"]["base"])
    gap = fv_base / spot - 1
    fund_word = ("sees it worth more" if gap > 0.02 else
                 "sees it worth less" if gap < -0.02 else "sees it fairly priced")
    tech_trend = (tick.get("tech") or {}).get("trend", "—")
    lenses = f"""
<div class="lenses">
  <div class="lens"><div class="ll">Fundamental study <span>separate lens</span></div>
    <div class="lv">{fund_word} — {fmt(fv_base, spot)} {ccy} base vs {fmt(spot, spot)}</div></div>
  <div class="lens on"><div class="ll">Price engine <span>this card</span></div>
    <div class="lv">{call}{f" — {alpha3 * 100:+.1f}% tilt on the 3-month center" if alpha3 else " (weak, no tilt)"}</div></div>
  <div class="lens"><div class="ll">Technical read <span>separate lens</span></div>
    <div class="lv">{html.escape(tech_trend)}</div></div>
</div>
<p class="lenscap">Three lenses, computed independently on purpose — none feeds
another, so agreement between them is information, not an echo.</p>"""

    # ---- chart geometry ---------------------------------------------------
    # The SYSTEM cone: with a lean, the whole distribution (bands included)
    # shifts — that is what an engine with drift does. `curves` (alpha=0)
    # stays as the published-fidelity check; `draw` is what the card shows.
    draw = leaned if leaned else curves
    W, H, L, R, T, B = 860, 380, 64, 150, 18, 40
    ys = ([p for _, p in hist] + [v for c in curves.values() for v in c.values()]
          + ([v for c in leaned.values() for v in c.values()] if leaned else []))
    ylo, yhi = min(ys), max(ys)
    pad = (yhi - ylo) * 0.07
    ylo, yhi = ylo - pad, yhi + pad
    x0, x1 = -HIST_MONTHS, 4.0

    def X(m): return L + (m - x0) / (x1 - x0) * (W - L - R)
    def Y(p): return T + (yhi - p) / (yhi - ylo) * (H - T - B)

    def path(pts, close_to=None):
        d = "M" + " L".join(f"{X(m):.1f},{Y(p):.1f}" for m, p in pts)
        if close_to is not None:
            d += " L" + " L".join(f"{X(m):.1f},{Y(p):.1f}"
                                  for m, p in reversed(close_to)) + " Z"
        return d

    tg = sorted(draw)
    band90 = path([(t, draw[t][0.95]) for t in tg],
                  close_to=[(t, draw[t][0.05]) for t in tg])
    band50 = path([(t, draw[t][0.75]) for t in tg],
                  close_to=[(t, draw[t][0.25]) for t in tg])
    median = path([(t, draw[t][0.50]) for t in tg])
    leanp = path([(t, leaned[t][0.50]) for t in tg]) if leaned else None
    histp = path(hist)

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
        f'<text x="{X(m):.1f}" y="{H-B+18}" text-anchor="middle" class="ax">{lab}</text>'
        for m, lab in [(-6, "6m ago"), (-3, "3m ago"), (0, "today"),
                       (1, "+1m"), (3, "+3 months")])

    p25, p75 = draw[3.0][0.25], draw[3.0][0.75]
    p5, p95 = draw[3.0][0.05], draw[3.0][0.95]
    rlab = (f'<text x="{X(3)+8:.1f}" y="{Y(p75)-7:.1f}" class="fl" fill="{TEAL}">'
            f'typical {fmt(p25, spot)}–{fmt(p75, spot)}</text>'
            f'<text x="{X(3)+8:.1f}" y="{Y(p5)+10:.1f}" class="fl" fill="{MUTED}">'
            f'9-in-10 {fmt(p5, spot)}–{fmt(p95, spot)}</text>')
    if leaned:
        lv = leaned[3.0][0.50]
        rlab += (f'<text x="{X(3)+8:.1f}" y="{Y(lv)+4:.1f}" class="fl" '
                 f'fill="{ORANGE}">center {fmt(lv, spot)}</text>')

    tid = tick["_ticker"]
    svg = f"""
<svg viewBox="0 0 {W} {H}" role="img" data-chart="{tid}"
     aria-label="{html.escape(tick['name'])} — published range and the engine's own lean">
  <style>.ax{{font:11px 'IBM Plex Mono',monospace;fill:{MUTED}}}
         .fl{{font:600 11px 'IBM Plex Sans',sans-serif}}</style>
  {grid}{xt}
  <line x1="{X(0):.1f}" x2="{X(0):.1f}" y1="{T}" y2="{H-B}" stroke="{MUTED}"
        stroke-dasharray="3 4" opacity=".7"/>
  <path d="{band90}" fill="{TEAL}" opacity="0.10"/>
  <path d="{band50}" fill="{TEAL}" opacity="0.28"/>
  <path d="{median}" fill="none" stroke="{TEAL}" stroke-width="1.5"
        stroke-dasharray="5 4" opacity=".85"/>
  {f'<path d="{leanp}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>' if leanp else ''}
  <path d="{histp}" fill="none" stroke="{INK}" stroke-width="2"/>
  <circle cx="{X(0):.1f}" cy="{Y(spot):.1f}" r="5" fill="#fff"
          stroke="{INK}" stroke-width="2.5"/>
  {rlab}
  <line class="cx" x1="0" x2="0" y1="{T}" y2="{H-B}" stroke="{INK}"
        opacity="0" stroke-width="1"/>
</svg>"""

    tiles = f"""
<div class="tiles">
  <div class="tile"><div class="tl">Typical range, next 3 months</div>
    <div class="tv num">{fmt(p25, spot)}–{fmt(p75, spot)}</div>
    <div class="ts">1-in-10 above {fmt(p95, spot)}, 1-in-10 below {fmt(p5, spot)} — graded when the date arrives</div></div>
  <div class="tile"><div class="tl">Committed call (3M)</div>
    <div class="tv num">{call}{f" · {alpha3 * 100:+.1f}%" if alpha3 else " · weak"}</div>
    <div class="ts">from this stock's own price history only — graded on its date</div></div>
  <div class="tile"><div class="tl">Odds of finishing higher in 3M</div>
    <div class="tv num">{p_up_lean * 100:.0f}%</div>
    <div class="ts">under the committed drift; graded like every forecast</div></div>
</div>"""

    hover = {"x0": x0, "x1": x1, "L": L, "R": R, "W": W, "spot": spot,
             "hist": hist,
             "band": {str(t): [curves[t][p] for p in PCTS] for t in tg},
             "lean": ({str(t): leaned[t][0.50] for t in tg} if leaned else None)}

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
    <span><i style="background:{TEAL};opacity:.35"></i> likely range with the lean (next 3M)</span>
    <span><i style="background:{ORANGE}"></i> engine's committed center</span>
    <span><i style="background:{INK}"></i> actual price (last {HIST_MONTHS}M)</span>
  </div>
  <div class="chartwrap">{svg}<div class="tip" hidden></div></div>
  {tiles}
  {lenses}
  <p class="foot">The band is today's published forecast tilted by the engine's
  committed drift (the untilted cone is reproduced within {dev:.2%} before the
  tilt). Committed drift is adopted engine behavior as of 23-Aug-2026 and
  reaches the live site at the next roll-forward + publish. The fundamental and
  technical verdicts are displayed for comparison only; they are never inputs
  to this cone.</p>
</section>"""
    return card, hover, dev


# -------------------------------------------------------------- tournament §
def tournament_section(tr: dict) -> str:
    rows = []
    for mk in tr["markets"]:
        for key, cell in (mk.get("results") or {}).items():
            ts, xs = cell.get("TS") or {}, cell.get("XS") or {}
            if "ic_spearman" not in ts and not xs:
                continue
            feat, hz = key.split("|")
            rows.append({"mkt": mk["market"], "feat": feat, "hz": hz,
                         "n": ts.get("n"), "ic": ts.get("ic_spearman"),
                         "v": ts.get("verdict", "—"), "hit": ts.get("hit_rate"),
                         "xsic": xs.get("mean_ic"),
                         "sp": xs.get("tercile_spread_mean_pct")})
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
    mom = [s for s in tr.get("survivors", [])
           if s["feature"] in ("mom_12_1", "mom_6_1")]
    sv = ("<p><b>Eligible for the MC lean (momentum family only):</b> " +
          "; ".join(f"{FEAT_WORDS[s['feature']]} at {s['horizon']} in "
                    f"{s['market']} (rank skill {s['pooled_ic']:+.3f}, "
                    f"n={s['n']})" for s in mom) +
          ". The other survivors (200-day trend, 52-week-high distance) also "
          "tested well but belong to the TECHNICAL lens, so they are excluded "
          "from the engine's lean — the three lenses stay independent. All of "
          "this is a candidate for the standing out-of-sample safety test, "
          "not an adoption.</p>") if mom else ""
    return f"""
<section class="card">
  <h2>Part 2 — Where the lean comes from: we tested the engine's own data.</h2>
  <p>Six standard direction indicators, tested on our cleaned price library —
  {sum(mk.get('names') or 0 for mk in tr['markets'])} names, 15 years — at the
  site's own 1-month and 3-month clocks, judged by a test that rewards
  <em>getting direction right</em>, with the sample split in half to catch
  flukes. Strongest eight readings in the three core markets:</p>
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
VERDICT_WORDS = {"PASS": "reliable", "FAIL": "reliable (inverse)",
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
.dim{{color:var(--muted);font-weight:400;font-size:.8em}}
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
.lenses{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:12px;margin-top:14px}}
.lens{{border:1px dashed var(--line);border-radius:10px;padding:9px 13px}}
.lens.on{{border:1.5px solid {TEAL};background:#F2FAF8}}
.ll{{font-size:.72rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase}}
.ll span{{color:var(--muted);font-weight:500;text-transform:none;letter-spacing:0;margin-left:6px}}
.lv{{font-size:.86rem;margin-top:2px}}
.lenscap{{color:var(--muted);font-size:.75rem;margin:6px 0 0}}
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
  const nearest = (arr, m) => arr.reduce((p,c)=>Math.abs(c-m)<Math.abs(p-m)?c:p);
  const fmt = x => d.spot>=1000 ? Math.round(x).toLocaleString('en')
             : d.spot>=100 ? x.toFixed(1) : x.toFixed(2);
  svg.addEventListener('mousemove', ev => {
    const r = svg.getBoundingClientRect();
    const px = (ev.clientX - r.left) / r.width * d.W;
    const m = d.x0 + (px - d.L) / (d.W - d.L - d.R) * (d.x1 - d.x0);
    if (m < d.x0 || m > 3) { tip.hidden = true; cx.setAttribute('opacity',0); return; }
    cx.setAttribute('x1', px.toFixed(1)); cx.setAttribute('x2', px.toFixed(1));
    cx.setAttribute('opacity', .35);
    let lines = [];
    if (m <= 0) {
      let best = d.hist.length ? d.hist.reduce((p,c)=>Math.abs(c[0]-m)<Math.abs(p[0]-m)?c:p) : null;
      if (best) lines.push(Math.abs(best[0]).toFixed(1)+'m ago  price '+fmt(best[1]));
    } else {
      const k = String(nearest(bt, m));
      const b = d.band[k];
      lines.push('+'+m.toFixed(1)+' months');
      lines.push('typical '+fmt(b[1])+'\\u2013'+fmt(b[3]));
      lines.push('9-in-10 '+fmt(b[0])+'\\u2013'+fmt(b[4]));
      if (d.lean) lines.push('leaned center '+fmt(d.lean[k]));
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
    ap.add_argument("--tournament", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tickers", default="ETEL,ADNOCDRILL,EMFD")
    args = ap.parse_args()

    with open(args.overlay) as f:
        overlay = {r["ticker"]: r for r in json.load(f)["rows"]}
    with open(args.tournament) as f:
        tournament = json.load(f)
    ticks = load_tickers()

    cards, hovers, devs = [], {}, {}
    for tk in args.tickers.split(","):
        tk = tk.strip()
        tick = dict(ticks[tk]); tick["_ticker"] = tk
        row = overlay[tk]
        hist = price_history(row["market"], tk, pd.Timestamp(row["anchor_date"]))
        card, hover, dev = build_card(tick, row, hist, tournament)
        cards.append(card)
        hovers[tk] = hover
        devs[tk] = dev
        assert dev <= MAX_BAND_DEV, (
            f"{tk}: drawn band deviates {dev:.2%} from the published cone")
        print(f"[{tk}] band reproduces published quantiles within {dev:.2%}")

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TESTAHIL — view-layer prototype (not live)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;800&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <div class="mast"><span class="brand">تستاهل TESTAHIL</span>
    <span class="badge">COMMITTED DRIFT · ADOPTED 23-AUG-2026 · NOT YET PUBLISHED</span></div>
  <p class="lede">Proposed ticker card. The <b style="color:{TEAL}">teal band</b>
  is today's published forecast with the typical range leading (the faint band
  is the 9-in-10 range — the crash guard, demoted from headline to whisker).
  The <b style="color:{ORANGE}">orange line</b> is the engine's committed
  direction — every stock gets a call, UP or DOWN, from its own price history
  alone, never from the fundamental study or the technical read: the three
  lenses stay independent and appear side by side below each chart. Hover any
  chart for the numbers at that date.</p>
  {''.join(cards)}
  {tournament_section(tournament)}
  <p class="foot">Built {pd.Timestamp.now().date()} from assets/data.js +
  engine/fv_overlay.py output (used for the published cone's shape parameters
  only) + the cleaned price library + the 23-Aug tournament results. Worst
  band deviation this build: {max(devs.values()):.2%}. Reproduce:
  engine/view_layer_prototype/build_prototype.py.</p>
</div>
<script>{JS.replace("__DATA__", json.dumps(hovers))}</script>
</body></html>"""

    with open(args.out, "w") as f:
        f.write(doc)
    print(f"wrote {args.out} ({os.path.getsize(args.out) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
