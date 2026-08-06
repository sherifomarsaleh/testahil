"""fv_overlay.py — Phase A of the Fundamental / Monte-Carlo Integration Protocol.

Canonical spec: engine/Fundamental_MC_Integration_Protocol.md (PROPOSED, 6-Aug-2026).

WHAT THIS DOES
--------------
For every covered name in a market, reads the PUBLISHED cone and the PUBLISHED
fair value and emits the diagnostic overlay defined by the protocol: reachability
G, terminal and touch convergence probabilities, the required-CAGR-vs-cash read,
and the tail-asymmetry flag.

WHAT THIS DOES NOT DO
---------------------
It does not touch the cone. No fundamental input reaches `drift`, `sigma_h`, `nu`
or `width_cal`; nothing here re-simulates a published forecast or writes to
`assets/data.js`. The overlay is a strictly downstream annotation, and every
number it emits is reproducible from what is already published.

sigma SOURCE — A CORRECTION TO PROTOCOL §2
------------------------------------------
The protocol as first written named the engine panel as the primary source for
`sigma_h`, with quantile inversion as a fallback. Implementation showed that is
backwards for a LIVE overlay, and the protocol has been amended to match this
module rather than the other way round:

  * `engine/panels/EG_*.csv` hold BACKTEST origins. The last EG origin is
    2026-04-12; the live ELEC anchor is 2026-08-05. The panel simply does not
    contain the live strike.
  * EG runs with `width_overlay_active=True`, so the published quantiles carry
    the per-name adaptive-width overlay. Inverting them recovers the EFFECTIVE
    sigma that actually shaped the published cone.
  * A native re-fit could therefore disagree with what was published — and an
    overlay that annotates a ledger row must be consistent with THAT row, not
    with a fresh fit of the same name.

So inversion from the published p5/p95 is the primary and faithful source here.
`sigma_src` records which path was taken on every row, and `selftest_max_dev`
proves the reconstruction reproduces the published quantiles.

Usage
-----
    python3 engine/fv_overlay.py --market EG
    python3 engine/fv_overlay.py --market EG --ticker ELEC --verbose
    python3 engine/fv_overlay.py --market EG --json out.json --md out.md
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from market_profiles import PROFILES          # noqa: E402
from mc_v3 import simulate_paths_v3           # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JS = os.path.join(REPO, "assets", "data.js")

# Protocol §4 — bands calibrated on the live 31-name EGX panel, not invented.
BAND_EDGES = ((1.0, "IN-REACH"), (2.0, "STRETCH"), (4.0, "OUT-OF-REACH"))
BAND_SUPPRESSED = "NOT-EXPRESSIBLE"

N_PATHS = 50_000        # production config
SEED = 42               # production seed
SELFTEST_TOL = 0.02     # 2% max relative deviation on reconstructed quantiles

# Invariant 7 (protocol §1): a fair value older than this at the anchor is STALE.
# The overlay still computes — a stale read is better than none on a site surface
# — but the row is flagged everywhere and excluded from the Phase C panel.
FV_STALE_DAYS = 183

# Below this |G| the fair value is inside the horizon's own noise: spot and fair
# value are not distinguishable, so P(touch) approaches 1 for the trivial reason
# that the level is already where the price is. Found in the first full EG run —
# EFID (gap -0%) reported P(touch)=85%/90%, which reads as a strong signal and is
# in fact the absence of one. The probability is correct; it just is not evidence.
# Flagged rather than suppressed: "already converged" is a real, useful state.
TRIVIAL_G = 0.25


# ----------------------------------------------------------------- data load
def load_tickers(data_js: str = DATA_JS) -> dict:
    """Evaluate data.js and return TICKERS as a dict.

    data.js is JavaScript with comments, not JSON, so it is evaluated by node
    rather than regex-parsed. node is already a build dependency of this repo
    (scripts/generate_feed.js, scripts/generate_seo.js).
    """
    script = (
        "const fs=require('fs'),vm=require('vm');const s={};vm.createContext(s);"
        f"vm.runInContext(fs.readFileSync({json.dumps(data_js)},'utf8')"
        "+';globalThis.__T=TICKERS;',s);"
        "process.stdout.write(JSON.stringify(s.__T));"
    )
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True,
                         check=True)
    return json.loads(out.stdout)


_FILE_DATE = re.compile(r"(\d{2})-(\d{2})-(\d{4})")


def parse_fv_asof(files: dict | None) -> _dt.date | None:
    """Fair-value publication date, from the study filename (DD-MM-YYYY).

    House filename convention, e.g. ELEC_Valuation_Study_05-08-2026_public.docx.
    This is the only machine-readable provenance for when a fair value was
    struck — `TICKERS[t].fair` carries no date field, and `asof` covers the MC
    and technical reads only. Returns None when no date can be sourced; the
    caller BLOCKS rather than guessing (protocol invariant 3).
    """
    if not files:
        return None
    for key in ("study", "pdf", "model", "biblio"):
        m = _FILE_DATE.search(files.get(key, "") or "")
        if m:
            d, mo, y = (int(x) for x in m.groups())
            try:
                return _dt.date(y, mo, d)
            except ValueError:
                continue
    return None


def parse_anchor(t: dict) -> _dt.date | None:
    """Cone anchor date, preferring the structured `asof.mc.data` stamp."""
    stamp = (((t.get("asof") or {}).get("mc") or {}).get("data")) or ""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", stamp)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        return _dt.date(y, mo, d)
    return None


# ------------------------------------------------------- standardized-t maths
def std_t_q(p: float, nu: float) -> float:
    """Quantile of the engine's UNIT-VARIANCE Student-t.

    simulate_terminal_v3 draws z * sqrt((nu-2)/chi2_nu), which is a t_nu scaled
    to unit variance — so its quantiles are sqrt((nu-2)/nu) * t_inv(p, nu).
    """
    return math.sqrt((nu - 2.0) / nu) * float(stats.t.ppf(p, nu))


def std_t_sf(z: float, nu: float) -> float:
    """P(X > z) for that same unit-variance t."""
    return float(stats.t.sf(z / math.sqrt((nu - 2.0) / nu), nu))


def invert_sigma(p5: float, p95: float, nu: float) -> float:
    """Effective horizon sigma implied by the published 90% band."""
    return (math.log(p95) - math.log(p5)) / (2.0 * std_t_q(0.95, nu))


def band_for(g: float) -> str:
    for edge, name in BAND_EDGES:
        if abs(g) <= edge:
            return name
    return BAND_SUPPRESSED


# ------------------------------------------------------------------- overlay
def horizon_overlay(spot, dist_h, h_sessions, nu, fair, yearfrac, rf,
                    n_paths=N_PATHS, seed=SEED):
    """Overlay for ONE name at ONE horizon. Returns a dict of protocol §3 measures."""
    p5, p50, p95 = dist_h["p5"], dist_h["p50"], dist_h["p95"]
    sigma = invert_sigma(p5, p95, nu)
    mu = math.log(p50 / spot)                 # = carry; alpha is 0 by design

    # --- G, per level (protocol §3.1) — drift-free distance in own vol units
    g = {k: math.log(v / spot) / sigma for k, v in fair.items()}
    band = band_for(g["base"])

    # --- terminal convergence probability (§3.2)
    def p_term(level):
        z = (math.log(level / spot) - mu) / sigma
        # "reach" means at/beyond fair value in the direction it lies from spot
        return std_t_sf(z, nu) if level >= spot else 1.0 - std_t_sf(z, nu)

    # --- touch probability (§3.3) — simulated, reflection does not hold here
    daily_var = (sigma ** 2) / h_sessions     # sigma already embeds width_cal
    paths = simulate_paths_v3(spot, daily_var, int(h_sessions), mu, nu=nu,
                              n_paths=n_paths, seed=seed, width_cal=1.0)
    run_max, run_min = paths.max(axis=1), paths.min(axis=1)
    term = paths[:, -1]

    def p_touch(level):
        hit = run_max >= level if level >= spot else run_min <= level
        return float(hit.mean())

    # --- self-test: does the reconstruction reproduce the published cone?
    rec = np.percentile(term, [5, 50, 95])
    dev = max(abs(rec[0] / p5 - 1), abs(rec[1] / p50 - 1), abs(rec[2] / p95 - 1))

    # --- required CAGR vs the cash hurdle (§3.4)
    req = {k: (v / spot) ** (1.0 / yearfrac) - 1.0 for k, v in fair.items()}

    # --- tail asymmetry (§3.5)
    if fair["base"] > p95:
        asym = "base above p95"
    elif fair["base"] < p5:
        asym = "base below p5"
    else:
        asym = "base inside 90% band"

    suppressed = band == BAND_SUPPRESSED
    trivial = abs(g["base"]) <= TRIVIAL_G
    return {
        "h_sessions": int(h_sessions),
        "sigma_h": round(sigma, 6),
        "mu_h": round(mu, 6),
        "G": {k: round(v, 2) for k, v in g.items()},
        "band": band,
        # False when the gap is inside the horizon's noise (|G| <= TRIVIAL_G) or
        # beyond its reach (suppressed): in both states the probability carries
        # no information about the fundamental thesis.
        "informative": not (suppressed or trivial),
        "already_converged": trivial,
        "p_term": None if suppressed else {k: round(p_term(v), 4) for k, v in fair.items()},
        "p_touch": None if suppressed else {k: round(p_touch(v), 4) for k, v in fair.items()},
        "required_cagr": {k: round(v, 4) for k, v in req.items()},
        "hurdle_rf": rf,
        "beats_cash": bool(req["base"] > rf),
        "asymmetry": asym,
        "selftest_max_dev": round(float(dev), 5),
    }


def overlay_for_ticker(tkr, t, profile, n_paths=N_PATHS, seed=SEED):
    """Full overlay for one name, or a BLOCKED row explaining why not."""
    spot = t.get("spot")
    fair_raw = t.get("fair") or {}
    fair = {k: fair_raw[k] for k in ("bear", "base", "full") if fair_raw.get(k)}
    dist, hz = t.get("dist") or {}, t.get("hz") or {}
    anchor, fv_asof = parse_anchor(t), parse_fv_asof(t.get("files"))

    def blocked(reason):
        return {"ticker": tkr, "overlay_status": f"BLOCKED — {reason}",
                "fv_asof": fv_asof.isoformat() if fv_asof else None,
                "anchor_date": anchor.isoformat() if anchor else None}

    # --- protocol Step 0 preconditions
    if not spot or len(fair) != 3:
        return blocked("no spot or incomplete fair value")
    if not dist.get("t20") or not dist.get("t60"):
        return blocked("cone missing a horizon")
    if fv_asof is None:
        return blocked("fv_asof unknown — cannot enforce point-in-time")
    if anchor is None:
        return blocked("anchor date unknown")
    if fv_asof > anchor:
        return blocked(f"look-ahead: fair value {fv_asof} post-dates anchor {anchor}")

    h1 = hz.get("h1") or 21
    h3 = hz.get("h3") or 63
    row = {
        "ticker": tkr, "name": t.get("name"), "code": t.get("code"),
        "ccy": t.get("ccy"), "spot": spot,
        "anchor_date": anchor.isoformat(), "fv_asof": fv_asof.isoformat(),
        "fv_lag_days": (anchor - fv_asof).days,
        "fv_stale": (anchor - fv_asof).days > FV_STALE_DAYS,
        "fv_bear": fair["bear"], "fv_base": fair["base"], "fv_full": fair["full"],
        "gap_base_pct": round((fair["base"] / spot - 1) * 100, 1),
        "sigma_src": "quantile_inversion",
        "engine": {"nu": profile.nu, "width_cal": profile.width_cal,
                   "width_overlay_active": profile.width_overlay_active,
                   "n_paths": n_paths, "seed": seed},
        "overlay_status": "PROVISIONAL — value-gap IC unmeasured",
        "realized_vs_fv": None, "converged": None,
    }
    for tag, key, yf in (("t20", "1M", 1 / 12), ("t60", "3M", 0.25)):
        row[key] = horizon_overlay(spot, dist[tag], h1 if key == "1M" else h3,
                                   profile.nu, fair, yf, profile.rf_live,
                                   n_paths=n_paths, seed=seed)
    return row


def run_market(market="EG", only=None, n_paths=N_PATHS, seed=SEED):
    profile = PROFILES[market]
    prefix = {"EG": "EGX"}.get(market)
    tickers = load_tickers()
    rows = []
    for tkr, t in tickers.items():
        if prefix and not str(t.get("code", "")).startswith(prefix):
            continue
        if only and tkr != only:
            continue
        rows.append(overlay_for_ticker(tkr, t, profile, n_paths=n_paths, seed=seed))
    rows.sort(key=lambda r: abs(r.get("3M", {}).get("G", {}).get("base", 1e9)))
    return {
        "protocol": "Fundamental_MC_Integration_Protocol.md (PROPOSED 6-Aug-2026)",
        "phase": "A", "market": market,
        "generated_from": "assets/data.js",
        "engine_config": {"nu": profile.nu, "width_cal": profile.width_cal,
                          "rf_live": profile.rf_live,
                          "width_overlay_active": profile.width_overlay_active},
        "n": len(rows), "rows": rows,
    }


# -------------------------------------------------------------------- report
def to_markdown(res: dict) -> str:
    rows = [r for r in res["rows"] if "1M" in r]
    blocked = [r for r in res["rows"] if "1M" not in r]
    rf = res["engine_config"]["rf_live"]
    L = [f"# Fair-value / MC overlay — {res['market']} (Phase A)", "",
         f"Protocol: `{res['protocol']}`  ",
         f"Engine: nu={res['engine_config']['nu']}, "
         f"width_cal={res['engine_config']['width_cal']}, "
         f"overlay_active={res['engine_config']['width_overlay_active']}, "
         f"cash hurdle rf={rf:.2%}  ",
         f"Names: {len(rows)} computed, {len(blocked)} blocked", "",
         "`G` is the fair-value gap in the name's own horizon volatility "
         "(drift-free). Probabilities are suppressed in NOT-EXPRESSIBLE per "
         "protocol §4.", "",
         "| Ticker | Gap% | G 1M | band 1M | G 3M | band 3M | "
         "P(touch base) 1M | P(touch base) 3M | beats cash |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        a, b = r["1M"], r["3M"]

        def f(h):
            if h["p_touch"] is None:
                return "—"
            # dagger: probability is real but uninformative (already converged)
            return f"{h['p_touch']['base']:.0%}" + ("&dagger;" if h["already_converged"] else "")

        L.append(f"| {r['ticker']} | {r['gap_base_pct']:+.0f}% | "
                 f"{a['G']['base']:+.2f} | {a['band']} | "
                 f"{b['G']['base']:+.2f} | {b['band']} | "
                 f"{f(a)} | {f(b)} | "
                 f"{'yes' if b['beats_cash'] else 'no'} |")
    for band in ("IN-REACH", "STRETCH", "OUT-OF-REACH", BAND_SUPPRESSED):
        n1 = sum(1 for r in rows if r["1M"]["band"] == band)
        n3 = sum(1 for r in rows if r["3M"]["band"] == band)
        L.append("") if band == "IN-REACH" else None
        L.append(f"- **{band}** — 1M: {n1}/{len(rows)}, 3M: {n3}/{len(rows)}")
    stale = [r["ticker"] for r in rows if r.get("fv_stale")]
    if stale:
        L += ["", f"⚠ **STALE fair values** (older than {FV_STALE_DAYS} days at anchor — "
              f"invariant 7 breach, re-study due): {', '.join(stale)}"]
    inf1 = sum(1 for r in rows if r["1M"]["informative"])
    inf3 = sum(1 for r in rows if r["3M"]["informative"])
    L += ["",
          f"&dagger; already converged (|G| <= {TRIVIAL_G}): the fair value sits "
          "inside the horizon's own noise, so a high P(touch) means spot is "
          "already at fair value — the probability is correct but carries no "
          "information about the thesis.", "",
          f"**Informative rows** (neither suppressed nor already converged) — "
          f"1M: {inf1}/{len(rows)}, 3M: {inf3}/{len(rows)}."]
    worst = max((r["1M"]["selftest_max_dev"] for r in rows), default=0)
    worst3 = max((r["3M"]["selftest_max_dev"] for r in rows), default=0)
    L += ["", f"Self-test — reconstructed cone vs published, worst relative "
              f"deviation: 1M {worst:.3%}, 3M {worst3:.3%} "
              f"(tolerance {SELFTEST_TOL:.0%}).", ""]
    if blocked:
        L += ["## Blocked", ""] + [f"- **{r['ticker']}** — {r['overlay_status']}"
                                   for r in blocked] + [""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Phase A fair-value / MC overlay")
    ap.add_argument("--market", default="EG")
    ap.add_argument("--ticker", default=None)
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--md", dest="md_out", default=None)
    ap.add_argument("--paths", type=int, default=N_PATHS)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()

    res = run_market(a.market, only=a.ticker, n_paths=a.paths)
    md = to_markdown(res)

    fails = [r["ticker"] for r in res["rows"] if "1M" in r
             and max(r["1M"]["selftest_max_dev"], r["3M"]["selftest_max_dev"]) > SELFTEST_TOL]
    if fails:
        print(f"SELF-TEST FAIL (>{SELFTEST_TOL:.0%}): {', '.join(fails)}",
              file=sys.stderr)

    if a.json_out:
        with open(a.json_out, "w") as fh:
            json.dump(res, fh, indent=1)
        print(f"wrote {a.json_out}")
    if a.md_out:
        with open(a.md_out, "w") as fh:
            fh.write(md)
        print(f"wrote {a.md_out}")
    if a.verbose or not (a.json_out or a.md_out):
        print(md)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
