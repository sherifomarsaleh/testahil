"""value_gap_backtest.py — Phase C of the Fundamental / Monte-Carlo Integration Protocol.

Canonical spec: engine/Fundamental_MC_Integration_Protocol.md §8.

THE QUESTION
------------
Do Testahil's own ground-up fair values predict forward returns? If they do, the
value gap is the stock picker the engine has never had, and the measured IC is the
number that belongs in `profile.ic` at `mc_v3.py:114`. If they do not, that is the
most valuable negative result available to this project, because it is a direct
test of whether the research process adds return.

This module answers it with whatever evidence exists, and refuses to answer past
that point. It scores through `direction_score.py` (Phase B), never through CRPS —
scoring a directional signal on a distributional loss is the recorded cause of the
last ablation.

POINT-IN-TIME CONSTRUCTION
--------------------------
The signal at date t may only use a fair value PUBLICLY VISIBLE at t. There is no
historical fair-value table in this repo, so the source of truth is the git history
of `assets/data.js`: a fair value is treated as known from the EARLIEST COMMIT that
carries it. That is conservative (the study predates the commit) and auditable
(every observation traces to a SHA). No fair value is ever applied to an origin
before its own commit.

WHY THE ENGINE IS NOT TOUCHED
-----------------------------
The protocol sketches Phase C as "add kind == 'value_gap' to signal_z". It is
deliberately NOT added here. `signal_z(close, idx, kind)` takes price history only
and structurally cannot see an exogenous fundamental, so wiring it would mean
changing a signature in a file whose fit notes record a bit-for-bit regression
requirement — for a signal whose IC has not been established. Measurement first,
promotion second. `grinold_alpha()` below is the adapter, tested and ready to lift
into `signal_alpha` on the day an IC survives this gate.

Usage
-----
    python3 engine/value_gap_backtest.py --market EG
    python3 engine/value_gap_backtest.py --market EG --md report.md --json out.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import direction_score as ds                       # noqa: E402
from market_profiles import PROFILES               # noqa: E402
from mc_v3 import calendar_horizons, carry_log_h   # noqa: E402
from panel_refresh import load_ohlc                # noqa: E402
from primitives import trailing_cc_vol             # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA_JS_REL = "assets/data.js"
OHLC = os.path.join(HERE, "raw_ohlc")
MARKET_PREFIX = {"EG": "EGX"}


# ------------------------------------------------- point-in-time fair values
_NODE = (
    "const fs=require('fs'),vm=require('vm');const s={};vm.createContext(s);"
    "try{vm.runInContext(fs.readFileSync(process.argv[1],'utf8')"
    "+';globalThis.__T=TICKERS;',s)}catch(e){process.exit(0)}"
    "const o=[];for(const[k,v]of Object.entries(s.__T||{})){"
    "if(!v||!v.code||!v.fair||v.fair.base==null||!v.spot)continue;"
    "o.push([k,String(v.code),v.fair.base,v.spot]);}"
    "process.stdout.write(JSON.stringify(o));"
)


def _commits_touching_data_js() -> int:
    """How many commits in THIS clone touch data.js. Part of the cache key below."""
    out = subprocess.run(
        ["git", "-C", REPO, "log", "--format=%H", "--", DATA_JS_REL],
        capture_output=True, text=True)
    return len([x for x in out.stdout.split("\n") if x.strip()])


def assert_full_history() -> None:
    """RAISE if this clone cannot see the history the point-in-time signal is built from.

    The docstring above names the git history of `assets/data.js` as the source of
    truth for what was publicly visible when. A SHALLOW clone truncates exactly that
    source, and it does so without any error: every fair value then appears to have
    become visible at the shallow boundary, every origin lands after it, no origin has
    a matured forward window, and the harness reports

        INSUFFICIENT-POWER — no observation has a realized outcome yet

    which is CHARACTER-FOR-CHARACTER what it reports when the evidence genuinely has
    not accrued yet. Two different states, one message, no way to tell them apart.

    Measured on 24-Aug-2026 in a fresh remote session: the shallow clone carried 27
    commits touching data.js and returned n=0 at both horizons; the same commit
    unshallowed carried 241 and returned n=32, IC -0.140, PARITY. A caller reading the
    first result would have concluded the sample had not grown since 6-Aug, when it had
    in fact grown six-fold — and would have concluded it again on every future run,
    because nothing about a shallow clone gets better with time.

    So this FAILS rather than warns, per [R-ENF-01]: a check that cannot distinguish
    "no evidence" from "no history to look in" is not a check. `git fetch --unshallow`
    is the whole remedy, and CI must set `fetch-depth: 0` (generate-seo.yml already
    does, for the same underlying reason, on a different derived date).
    """
    shallow = subprocess.run(
        ["git", "-C", REPO, "rev-parse", "--is-shallow-repository"],
        capture_output=True, text=True).stdout.strip()
    if shallow == "true":
        raise RuntimeError(
            "SHALLOW CLONE — Phase C cannot run. The point-in-time signal is "
            "reconstructed from the git history of assets/data.js, and this clone "
            f"holds only {_commits_touching_data_js()} commits touching it. Every "
            "fair value would appear to become visible at the shallow boundary and "
            "the run would report INSUFFICIENT-POWER for a reason that is an "
            "artefact of the checkout. Run `git fetch --unshallow` (CI: "
            "fetch-depth: 0) and re-run."
        )


def pit_fair_values(market="EG", cache=None, verbose=True):
    """Earliest commit date at which each distinct fair value became visible.

    Returns {ticker: [(iso_date, fair_base), ...]} sorted by date.
    """
    assert_full_history()
    # The cache is keyed to the LAST COMMIT touching data.js. Without that key a
    # stale cache silently omits every fair value published since it was written
    # — a wrong answer that looks exactly like a right one, which is the worst
    # failure mode available to a backtest.
    head = subprocess.run(
        ["git", "-C", REPO, "log", "-1", "--format=%H", "--", DATA_JS_REL],
        capture_output=True, text=True).stdout.strip()
    depth = _commits_touching_data_js()
    if cache and os.path.exists(cache):
        with open(cache) as fh:
            blob = json.load(fh)
        # The HEAD sha alone is NOT a sufficient key: it is identical on a shallow
        # and a full clone of the same commit, so a cache built on truncated history
        # would be accepted here and silently reused. The commit COUNT is what differs
        # (27 vs 241 on 24-Aug-2026), so it is part of the key.
        if (blob.get("_data_js_head") == head and blob.get("_market") == market
                and blob.get("_commits_parsed") == depth):
            return {k: [tuple(x) for x in v] for k, v in blob["values"].items()}
        if verbose:
            why = ("history depth changed" if blob.get("_data_js_head") == head
                   else "data.js moved")
            print(f"[pit] cache stale ({why}) — rebuilding", file=sys.stderr)

    prefix = MARKET_PREFIX.get(market)
    shas = subprocess.run(
        ["git", "-C", REPO, "log", "--format=%H %ad", "--date=short",
         "--reverse", "--", DATA_JS_REL],
        capture_output=True, text=True, check=True).stdout.split("\n")

    tmp = os.path.join(HERE, ".pit_tmp_data.js")
    first: dict[tuple[str, float], str] = {}
    seen = 0
    for line in shas:
        if not line.strip():
            continue
        sha, date = line.split()[0], line.split()[1]
        blob = subprocess.run(["git", "-C", REPO, "show", f"{sha}:{DATA_JS_REL}"],
                              capture_output=True, text=True)
        if blob.returncode != 0:
            continue
        with open(tmp, "w") as fh:
            fh.write(blob.stdout)
        out = subprocess.run(["node", "-e", _NODE, tmp], capture_output=True, text=True)
        if not out.stdout.strip():
            continue
        seen += 1
        for tkr, code, fair, _spot in json.loads(out.stdout):
            if prefix and not code.startswith(prefix):
                continue
            first.setdefault((tkr, float(fair)), date)   # --reverse => earliest wins
    if os.path.exists(tmp):
        os.remove(tmp)

    byt: dict[str, list] = {}
    for (tkr, fair), date in first.items():
        byt.setdefault(tkr, []).append((date, fair))
    for v in byt.values():
        v.sort()
    if verbose:
        print(f"[pit] {seen} commits parsed, {len(byt)} names, "
              f"{sum(len(v) for v in byt.values())} distinct fair-value vintages",
              file=sys.stderr)
    if cache:
        with open(cache, "w") as fh:
            json.dump({"_data_js_head": head, "_market": market,
                       "_commits_parsed": seen, "values": byt}, fh, indent=1)
    return byt


# ------------------------------------------------------------ Grinold adapter
def grinold_alpha(ic, sigma_h, g, dead=0.5, clipz=2.0):
    """Log-drift shift implied by a value gap — the form used at mc_v3.py:114.

    Kept here, unwired, so promotion into signal_alpha is a lift-and-drop rather
    than a rewrite. Returns 0 inside the dead zone, exactly as the engine does.
    """
    if abs(g) < dead:
        return 0.0
    a = ic * sigma_h * float(np.clip(g, -clipz, clipz))
    return float(np.clip(a, -0.5 * sigma_h, 0.5 * sigma_h))


# Invariant 7 / §1b: a vintage stops minting observations once it is older than
# this at the origin. Past the cap the numerator of G is frozen history and the
# experiment silently changes from "does the valuation predict" to "does price
# mean-revert to an old number".
FV_STALE_DAYS = 183

# §10.2: observations accrue on MEASUREMENT dates, not study dates. Each vintage
# mints a fresh observation every ~month (21 sessions) while it stays fresh —
# the mechanism that makes the committed monthly price update actually build the
# Phase C sample. Same-vintage observations share a numerator, so they carry a
# vintage id for the honesty of any later autocorrelation adjustment.
REMEASURE_STEP_SESSIONS = 21


# ------------------------------------------------------------- panel assembly
def build_panel(market="EG", months=1, cache=None, verbose=True):
    """Observations for every (name, vintage, measurement date) with a realized
    outcome: origins step every REMEASURE_STEP_SESSIONS from the vintage date
    until the vintage goes stale, a newer vintage supersedes it, or OHLC ends."""
    profile = PROFILES[market]
    fvs = pit_fair_values(market, cache=cache, verbose=verbose)
    rows, skipped = [], []

    for tkr, vintages in sorted(fvs.items()):
        path = os.path.join(OHLC, market, f"{tkr}.csv")
        if not os.path.exists(path):
            skipped.append((tkr, "no OHLC"))
            continue
        df = load_ohlc(path, tkr, market=market)
        dates_s = df["Date"]                  # calendar_horizons wants the Series
        dates = dates_s.values
        close = df["Price"].values

        for vi, (fv_date, fair) in enumerate(vintages):
            # a vintage is live until the next vintage's date supersedes it
            succ = (np.datetime64(vintages[vi + 1][0])
                    if vi + 1 < len(vintages) else None)
            start = int(np.searchsorted(dates, np.datetime64(fv_date), side="left"))
            if start >= len(dates) or start < 260:
                skipped.append((tkr, f"{fv_date}: no origin / <260 history"))
                continue

            idx = start
            while idx < len(dates):
                d64 = dates[idx]
                if succ is not None and d64 >= succ:
                    break                                     # superseded — newer FV rules
                age = int((d64 - np.datetime64(fv_date))
                          / np.timedelta64(1, "D"))
                if age > FV_STALE_DAYS:
                    skipped.append((tkr, f"{fv_date}: stale at {str(d64)[:10]}"))
                    break                                     # invariant 7
                hz = calendar_horizons(dates_s, idx, months)
                if hz is None:
                    break                                     # +N months beyond OHLC
                h_grade, h_size = hz
                s0, sT = float(close[idx]), float(close[idx + h_grade])
                sigma_d = trailing_cc_vol(close, idx)
                sigma_h = sigma_d * math.sqrt(h_size)
                if s0 > 0 and sT > 0 and sigma_h > 0:
                    yearfrac = months / 12.0
                    carry = carry_log_h(profile, str(d64)[:10], 0.0, h_size,
                                        yearfrac=yearfrac)
                    rows.append({
                        "ticker": tkr, "fv_date": fv_date,
                        "vintage_id": f"{tkr}@{fv_date}",
                        "origin": str(d64)[:10],
                        "grade": str(dates[idx + h_grade])[:10],
                        "h_grade": int(h_grade), "h_size": int(h_size),
                        "fv_age_days": age,
                        "spot": s0, "fair_base": fair, "realized": sT,
                        "sigma_h": sigma_h,
                        "G": math.log(fair / s0) / sigma_h,
                        "fwd_log": math.log(sT / s0),
                        "carry_log": float(carry),
                        "fwd_excess": math.log(sT / s0) - float(carry),
                    })
                idx += REMEASURE_STEP_SESSIONS
    return rows, skipped, profile


# -------------------------------------------------------------------- report
def run(market="EG", cache=None, verbose=True):
    res = {"protocol": "Fundamental_MC_Integration_Protocol.md §8 (Phase C)",
           "market": market, "horizons": {}}
    for months in (1, 3):
        rows, skipped, profile = build_panel(market, months, cache=cache,
                                             verbose=verbose)
        key = f"{months}M"
        if not rows:
            res["horizons"][key] = {"n": 0, "verdict": "INSUFFICIENT-POWER",
                                    "note": "no observation has a realized outcome yet",
                                    "skipped": len(skipped)}
            continue
        g = [r["G"] for r in rows]
        ex = [r["fwd_excess"] for r in rows]
        nm = [r["ticker"] for r in rows]
        sc = ds.score(g, ex, names=nm)
        sc["skipped"] = len(skipped)
        # Sign balance: a cross-section that is all-undervalued cannot test the
        # short side at all, and the IC then reduces to a magnitude ordering
        # within one sign. Reported because a "balanced" IC and a one-sided one
        # are not the same evidence even at equal n.
        npos = sum(1 for x in g if x > 0)
        sc["sign_balance"] = {"positive": npos, "negative": len(g) - npos,
                              "one_sided": npos in (0, len(g))}
        sc["distinct_origins"] = len(sorted({r["origin"] for r in rows}))
        sc["origin_span"] = [min(r["origin"] for r in rows),
                             max(r["origin"] for r in rows)]
        res["horizons"][key] = sc
        res.setdefault("rows", {})[key] = rows
        res.setdefault("skipped_detail", {})[key] = skipped[:40]
    res["engine_hook"] = {
        "wired": False,
        "reason": "no IC has cleared the Phase B gate; promotion requires a "
                  "verdict other than INSUFFICIENT-POWER",
        "adapter": "value_gap_backtest.grinold_alpha (mirrors mc_v3.signal_alpha)",
    }
    return res


def to_markdown(res: dict) -> str:
    L = [f"# Value-gap backtest — {res['market']} (Phase C)", "",
         f"Protocol: `{res['protocol']}`  ",
         "Signal: `G = ln(fair_base / spot) / sigma_h`, point-in-time from the git "
         "history of `assets/data.js`.  ",
         "Scored against forward log return **net of carry** via "
         "`direction_score.py` (Phase B). CRPS is not used.", ""]
    for key in ("1M", "3M"):
        h = res["horizons"].get(key)
        if not h:
            continue
        L.append(ds.format_report(h, f"{key} horizon"))
        if h.get("n"):
            sb = h["sign_balance"]
            L += [f"- distinct origin dates: {h['distinct_origins']} "
                  f"({h['origin_span'][0]} → {h['origin_span'][1]})",
                  f"- sign balance: {sb['positive']} positive / {sb['negative']} negative"
                  + ("  **— ONE-SIDED: the short side is untested, so the IC is a "
                     "magnitude ordering within a single sign**" if sb["one_sided"] else ""),
                  f"- observations dropped for lack of a realized outcome: {h['skipped']}",
                  ""]
    hook = res["engine_hook"]
    L += ["## Engine hook", "",
          f"- wired into the engine: **{hook['wired']}**",
          f"- reason: {hook['reason']}",
          f"- adapter ready at `{hook['adapter']}`", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Phase C value-gap backtest")
    ap.add_argument("--market", default="EG")
    ap.add_argument("--cache", default=os.path.join(HERE, ".pit_fair_values_EG.json"))
    ap.add_argument("--json", dest="json_out", default=None)
    ap.add_argument("--md", dest="md_out", default=None)
    a = ap.parse_args()

    res = run(a.market, cache=a.cache)
    md = to_markdown(res)
    if a.json_out:
        slim = {k: v for k, v in res.items() if k != "rows"}
        slim["rows"] = res.get("rows", {})
        with open(a.json_out, "w") as fh:
            json.dump(slim, fh, indent=1, default=str)
        print(f"wrote {a.json_out}")
    if a.md_out:
        with open(a.md_out, "w") as fh:
            fh.write(md)
        print(f"wrote {a.md_out}")
    if not (a.json_out or a.md_out):
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
