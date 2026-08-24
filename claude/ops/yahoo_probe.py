#!/usr/bin/env python3
"""
STEP 1 — Does Yahoo actually carry Testahil's covered names?

READ-ONLY. This script never writes to engine/raw_ohlc/ and never touches
assets/data.js. It writes exactly one new file, yahoo_probe_results.csv, in
whatever directory you run it from.

WHAT IT DOES
  For every library file under engine/raw_ohlc/{MARKET}/{TICKER}.csv it:
    1. builds candidate Yahoo symbols from that name's exchange code
       (EGX -> .CA, Tadawul -> .SR/.SAU, ADX -> .AD, DFM -> .DU/.AE,
        QSE -> .QA, KRX -> .KS, NSE -> .NS, NASDAQ -> bare, metals -> futures)
    2. pulls ~2 years of daily closes from Yahoo's public chart endpoint
    3. joins on date against the last 250 sessions already in the library
    4. reports how far apart the two vendors are, per name

WHY THE COMPARISON MATTERS
  The library is investing.com format and the standing merge rule requires
  overlapping dates to agree to the 4th decimal. A different vendor will not
  agree by default. This measures the disagreement BEFORE anything is spliced,
  so the decision to adopt Yahoo (per name) rests on evidence, not on the fact
  that a symbol resolved.

VERDICTS
  MATCH      median abs diff <= 0.10% and max <= 1.0%   -> safe to feed
  CLOSE      median <= 0.50%                            -> inspect before use
  DRIFT      worse than that                            -> do not feed
  NO_OVERLAP symbol resolved but no shared dates        -> wrong instrument?
  NOT_FOUND  no candidate symbol returned data          -> stays manual

USAGE
  python3 scripts/yahoo_probe.py                  # all names
  python3 scripts/yahoo_probe.py --market AE      # one market
  python3 scripts/yahoo_probe.py --dry            # no network; check wiring
Standard library only. No pip install, no API key.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def _repo_root(start: str) -> str:
    """Walk up until engine/raw_ohlc is found.

    The original resolved ROOT as dirname(HERE), which is only correct while the
    script sits exactly one level below the repo root (scripts/). It lives two
    levels down at claude/ops/, where that assumption reads assets/data.js out of
    claude/ and dies. Searching for the marker directory makes the script
    indifferent to where it is filed.
    """
    d = start
    while True:
        if os.path.isdir(os.path.join(d, "engine", "raw_ohlc")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("cannot find engine/raw_ohlc above " + start)
        d = parent


ROOT = _repo_root(HERE)
RAW = os.path.join(ROOT, "engine", "raw_ohlc")
OUT = os.path.join(os.getcwd(), "yahoo_probe_results.csv")

CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=2y&interval=1d"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Library filename -> assets/data.js key, where the two disagree.
FILE_ALIAS = {"TWOPOINTZERO": "2POINTZERO", "RAJHI": "ALRAJHI", ("AE", "ADIB"): "ADIBUAE"}

# Yahoo suffix per exchange. Two entries = try in order, first with data wins.
SUFFIX = {
    "EGX": [".CA"],
    "TADAWUL": [".SR", ".SAU"],
    "ADX": [".AD", ".AE"],      # .AD unconfirmed — this probe is the test
    "DFM": [".DU", ".AE"],
    "QSE": [".QA"],
    "KRX": [".KS"],
    "NSE": [".NS"],
    "NASDAQ": [""],
}
METALS = {"GOLD": ["GC=F", "XAUUSD=X"],
          "SILVER": ["SI=F", "XAGUSD=X"],
          "PLATINUM": ["PL=F", "XPTUSD=X"]}


def load_codes() -> dict:
    """Pull {KEY: 'EXCHANGE:SYMBOL'} straight out of assets/data.js."""
    path = os.path.join(ROOT, "assets", "data.js")
    codes = {}
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    import re
    # Each ticker block opens with  KEY: {  and carries a  code: "EX:SYM"  line.
    for m in re.finditer(r'(?m)^\s*"?([A-Za-z0-9_]+)"?\s*:\s*\{', src):
        key = m.group(1)
        window = src[m.end():m.end() + 4000]
        c = re.search(r'code\s*:\s*"([A-Z]+):([^"]+)"', window)
        if c:
            codes.setdefault(key, f"{c.group(1)}:{c.group(2)}")
    return codes


def library_closes(path: str, limit: int = 250) -> dict:
    """{date -> close} for the most recent `limit` sessions in the library.

    Row order is NOT assumed. Some libraries are stored newest-first
    (investing.com's own order) and some oldest-first; taking the first N rows
    would silently compare 2012 against Yahoo's 2026 on the ascending ones.
    Every row is read, then the newest `limit` dates are kept.
    """
    out = {}
    with open(path, encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            raw_date = (row.get("Date") or "").strip().strip('"')
            raw_px = (row.get("Price") or "").strip().strip('"').replace(",", "")
            if not raw_date or not raw_px:
                continue
            for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
                try:
                    d = datetime.strptime(raw_date, fmt).date()
                    break
                except ValueError:
                    d = None
            if d is None:
                continue
            try:
                out[d.isoformat()] = float(raw_px)
            except ValueError:
                continue
    keep = sorted(out, reverse=True)[:limit]
    return {d: out[d] for d in keep}


class RateLimited(Exception):
    """Yahoo answered 429 on every attempt for this symbol."""


def _fetch(symbol: str) -> dict:
    req = urllib.request.Request(CHART.format(sym=urllib.parse.quote(symbol)),
                                 headers={"User-Agent": UA, "Accept": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        payload = json.load(resp)
    result = (payload.get("chart") or {}).get("result")
    if not result:
        return {}
    r = result[0]
    stamps = r.get("timestamp") or []
    quote = (r.get("indicators") or {}).get("quote") or [{}]
    closes = quote[0].get("close") or []
    out = {}
    for ts, px in zip(stamps, closes):
        if px is None:
            continue
        d = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
        out[d] = float(px)
    return out


def yahoo_closes(symbol: str, retries: int = 4) -> dict:
    """{date -> close} from Yahoo. Empty dict = Yahoo HAS no data for this symbol.

    Raises RateLimited if every attempt came back 429. The original caught 429,
    slept 5s and moved on to the next candidate, so a throttled name was written
    down as NOT_FOUND -- indistinguishable in the results table from a symbol
    Yahoo genuinely does not carry. Step 2 adopts per name off this table, so that
    false negative is the one error that must not be silent: a 404 is evidence, a
    429 is the absence of evidence.
    """
    delay = 5.0
    for attempt in range(retries):
        try:
            return _fetch(symbol)
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                if attempt == retries - 1:
                    raise RateLimited(symbol)
                time.sleep(delay)
                delay *= 2
                continue
            if exc.code in (400, 404):
                return {}          # Yahoo answered: no such symbol.
            raise
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2
    return {}


def compare(lib: dict, yah: dict) -> dict:
    shared = sorted(set(lib) & set(yah))
    if not shared:
        return {"n": 0, "median_pct": None, "max_pct": None, "verdict": "NO_OVERLAP"}
    diffs = []
    for d in shared:
        base = lib[d]
        if base == 0:
            continue
        diffs.append(abs(yah[d] - base) / base * 100.0)
    if not diffs:
        return {"n": 0, "median_pct": None, "max_pct": None, "verdict": "NO_OVERLAP"}
    diffs.sort()
    mid = diffs[len(diffs) // 2]
    worst = diffs[-1]
    if mid <= 0.10 and worst <= 1.0:
        verdict = "MATCH"
    elif mid <= 0.50:
        verdict = "CLOSE"
    else:
        verdict = "DRIFT"
    return {"n": len(diffs), "median_pct": round(mid, 4),
            "max_pct": round(worst, 4), "verdict": verdict}


def candidates(market: str, name: str, code: str | None) -> list[str]:
    if market in ("XAU", "XPT") or name in METALS:
        return METALS.get(name, [])
    if not code:
        return []
    exchange, symbol = code.split(":", 1)
    return [symbol + sfx for sfx in SUFFIX.get(exchange, [])]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--market", help="probe one market folder only, e.g. AE")
    ap.add_argument("--dry", action="store_true", help="skip the network entirely")
    ap.add_argument("--sleep", type=float, default=0.6, help="seconds between calls")
    ap.add_argument("--retries", type=int, default=4, help="attempts per symbol on HTTP 429")
    ap.add_argument("--abort-after", type=int, default=8,
                    help="stop the run after N consecutive rate-limited names")
    args = ap.parse_args()

    codes = load_codes()
    rows = []
    consecutive_429 = 0
    markets = [args.market] if args.market else sorted(os.listdir(RAW))

    for market in markets:
        mdir = os.path.join(RAW, market)
        if not os.path.isdir(mdir):
            continue
        for fname in sorted(os.listdir(mdir)):
            if not fname.endswith(".csv"):
                continue
            stem = fname[:-4]
            key = FILE_ALIAS.get((market, stem)) or FILE_ALIAS.get(stem) or stem
            code = codes.get(key)
            cands = candidates(market, key, code)
            lib = library_closes(os.path.join(mdir, fname))
            lib_last = max(lib) if lib else ""

            row = {"market": market, "library_file": fname, "data_js_key": key,
                   "exchange_code": code or "", "symbol_tried": "|".join(cands),
                   "symbol_used": "", "library_last_date": lib_last,
                   "yahoo_last_date": "", "overlap_days": 0,
                   "median_diff_pct": "", "max_diff_pct": "", "verdict": ""}

            if not cands:
                row["verdict"] = "NO_SYMBOL_RULE"
                rows.append(row)
                continue
            if args.dry:
                row["verdict"] = "DRY"
                rows.append(row)
                continue

            got, used, throttled = {}, "", False
            for sym in cands:
                try:
                    got = yahoo_closes(sym, retries=args.retries)
                except RateLimited:
                    got, throttled = {}, True
                except Exception:
                    got = {}
                time.sleep(args.sleep)
                if got:
                    used = sym
                    break

            if not got:
                row["verdict"] = "RATE_LIMITED" if throttled else "NOT_FOUND"
                rows.append(row)
                print(f"  {market}/{stem:<14} {row['verdict']:<12} tried {'|'.join(cands)}")
                # A throttled probe produces a table that LOOKS like a coverage
                # finding. Better to end the run red than to hand Step 2 a page of
                # NOT_FOUNDs that were never actually asked.
                consecutive_429 = consecutive_429 + 1 if throttled else 0
                if consecutive_429 >= args.abort_after:
                    print(f"\n!! {consecutive_429} consecutive rate-limited names — aborting.")
                    print("   Yahoo is throttling this runner; the partial table is not evidence.")
                    return 2
                continue
            consecutive_429 = 0

            res = compare(lib, got)
            row.update({"symbol_used": used, "yahoo_last_date": max(got),
                        "overlap_days": res["n"],
                        "median_diff_pct": res["median_pct"] if res["median_pct"] is not None else "",
                        "max_diff_pct": res["max_pct"] if res["max_pct"] is not None else "",
                        "verdict": res["verdict"]})
            rows.append(row)
            print(f"  {market}/{stem:<14} {res['verdict']:<10} {used:<14} "
                  f"n={res['n']:<4} med={res['median_pct']} max={res['max_pct']} "
                  f"yahoo_last={max(got)} lib_last={lib_last}")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [])
        w.writeheader()
        w.writerows(rows)

    tally = {}
    for r in rows:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print("\n=== SUMMARY ===")
    for k in sorted(tally, key=lambda x: -tally[x]):
        print(f"  {k:<15} {tally[k]}")
    print(f"\nwrote {OUT}  ({len(rows)} names)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
