#!/usr/bin/env python3
"""
Build assets/markets.js — the ticker -> market registry the site groups by.

WHY THIS EXISTS
---------------
ledger.html used to decide which tab group a name belonged to by reading
`asset_class` off the first LEDGER row it happened to encounter for that name:

    equity -> "EGX"        other -> "International markets"      metal -> "Metals"

That overloaded a genuine asset-class field ("is this an equity or a metal?")
to also carry a market flag ("is this Egyptian?"). It held only while every
non-Egyptian equity was mislabelled `other`. On 28-Jul-2026 the market-wide
re-strike wrote the semantically CORRECT value — Aramco is an equity — and on
29-Jul the ledger cleanup deleted the older `other`-tagged rows that had been
propping the grouping up. 34 international names (all 18 UAE, all 11 Tadawul,
AAPL/NVDA/TSLA, INFY/RELIANCE, QGTS) silently fell into the EGX tab.

Nothing threw. The page rendered. It was simply wrong, and only a human
reading the tab bar could see it.

THE FIX
-------
Market is decided by FILE PLACEMENT — engine/raw_ohlc/{MARKET}/{TICKER}.csv —
exactly as the standing protocol already says for the unattended pipeline.
This script reads that directory tree and emits the registry. asset_class goes
back to meaning asset class, and can never again decide what country a stock
trades in.

Run:  python3 scripts/build_market_registry.py [--write]
Verify by IMPORT, not by parse: the script loads assets/data.js in node and
asserts every LEDGER instrument resolves to exactly one market.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "engine", "raw_ohlc")
OUT = os.path.join(ROOT, "assets", "markets.js")

# Library file stem -> the instrument name the SITE uses in LEDGER/TICKERS.
# Only the genuine mismatches; everything else maps to itself. A stem that
# needs an alias and does not have one is caught by the coverage assert, not
# silently dropped — the "0 skipped" failure mode the protocol warns about.
ALIAS = {
    "AE/TWOPOINTZERO": "2POINTZERO",   # JS identifiers cannot start with a digit; the key is quoted in data.js
    "AE/ADIB":         "ADIBUAE",      # distinct from EG/ADIB (ADIB-Egypt) — same stem, two different banks
    "SA/RAJHI":        "ALRAJHI",
    "KR/KAKAO":        "Kakao",
    "KR/SAMSUNG":      "Samsung",
    "XAU/GOLD":        "Gold",
    "XAU/SILVER":      "Silver",
    "XPT/PLATINUM":    "Platinum",
}

# Display order and labels for the tab groups. `group` collapses the two metal
# directories into one visual block.
MARKET_META = [
    ("EG",  {"label": "EGX — Egypt",              "group": "EG"}),
    ("AE",  {"label": "UAE — ADX & DFM",          "group": "AE"}),
    ("SA",  {"label": "Saudi Arabia — Tadawul",   "group": "SA"}),
    ("QA",  {"label": "Qatar — QSE",              "group": "QA"}),
    ("IN",  {"label": "India — NSE",              "group": "IN"}),
    ("KR",  {"label": "South Korea — KOSPI",      "group": "KR"}),
    ("US",  {"label": "United States",            "group": "US"}),
    ("XAU", {"label": "Metals",                   "group": "METALS"}),
    ("XPT", {"label": "Metals",                   "group": "METALS"}),
]
ORDER = [m for m, _ in MARKET_META]


def scan():
    """ticker -> market, from file placement only."""
    reg, dupes = {}, []
    for market in sorted(os.listdir(RAW)):
        d = os.path.join(RAW, market)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".csv"):
                continue
            stem = fn[:-4]
            ticker = ALIAS.get(f"{market}/{stem}", stem)
            if ticker in reg and reg[ticker] != market:
                dupes.append((ticker, reg[ticker], market))
            reg[ticker] = market
    if dupes:
        raise SystemExit(f"FAIL — ticker claimed by two markets, add an ALIAS: {dupes}")
    return reg


def ticker_keys():
    """Load assets/data.js in node and return its TICKERS keys.

    LEDGER and TICKERS do not always spell a name the same way: the ledger carries
    `Samsung` and `Kakao` (and `Gold`), while TICKERS keys them `SAMSUNG` and `KAKAO`.
    The registry is built from library filenames through ALIAS, which lands on the LEDGER
    spelling — so a page looking a TICKERS key up in MARKET_OF got nothing back for those
    names and fell through to whatever its fallback was. Asserting only against LEDGER
    could never see that; this is the second known total to count against.
    """
    js = (
        "const fs=require('fs'),vm=require('vm');"
        "const c=vm.createContext({console,globalThis:undefined});"
        "vm.runInContext(\"var globalThis=this;\"+fs.readFileSync(process.argv[1],'utf8')"
        "+'\\n;globalThis.__T=TICKERS;',c);"
        "console.log(JSON.stringify(Object.keys(c.__T)));"
    )
    p = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "data.js")],
                       capture_output=True, text=True)
    if p.returncode:
        raise SystemExit("FAIL — could not IMPORT assets/data.js:\n" + p.stderr)
    return json.loads(p.stdout)


def ledger_instruments():
    """Load assets/data.js in node and return its LEDGER instruments + count."""
    js = (
        "const fs=require('fs'),vm=require('vm');"
        "const c=vm.createContext({console,globalThis:undefined});"
        "vm.runInContext(\"var globalThis=this;\"+fs.readFileSync(process.argv[1],'utf8')"
        "+'\\n;globalThis.__L=LEDGER;',c);"
        "console.log(JSON.stringify([...new Set(c.__L.map(r=>r.instrument))]));"
    )
    p = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "data.js")],
                       capture_output=True, text=True)
    if p.returncode:
        raise SystemExit("FAIL — could not IMPORT assets/data.js:\n" + p.stderr)
    return json.loads(p.stdout)


def main():
    write = "--write" in sys.argv
    reg = scan()
    inst = ledger_instruments()

    # COUNT AGAINST A KNOWN TOTAL — never trust a tool's own "0 skipped".
    missing = sorted(t for t in inst if t not in reg)
    extra = sorted(t for t in reg if t not in inst)
    print(f"libraries scanned : {len(reg)}")
    print(f"LEDGER instruments: {len(inst)}")
    if missing:
        raise SystemExit(
            "FAIL — these LEDGER instruments have no library and therefore no market.\n"
            "       Place the CSV under engine/raw_ohlc/{MARKET}/ or add an ALIAS:\n"
            f"       {missing}")
    if extra:
        print(f"note: libraries with no ledger rows yet (kept in the registry): {extra}")

    # Second known total: every TICKERS key must resolve too, case-insensitively.
    ci = {t.upper(): m for t, m in reg.items()}
    tks = ticker_keys()
    unresolved = sorted(t for t in tks if t not in reg and t.upper() not in ci)
    print(f"TICKERS keys      : {len(tks)}")
    if unresolved:
        raise SystemExit(
            "FAIL — these TICKERS keys resolve to no market, so every surface that\n"
            "       sections by market would drop them:\n"
            f"       {unresolved}")
    cased = sorted(t for t in tks if t not in reg)
    if cased:
        print(f"note: resolved only case-insensitively (LEDGER vs TICKERS spelling): {cased}")

    counts = {}
    for t, m in reg.items():
        counts[m] = counts.get(m, 0) + 1
    for m in ORDER:
        if counts.get(m):
            print(f"  {m:4s} {counts[m]:3d}  {dict(MARKET_META)[m]['label']}")
    unknown = [m for m in counts if m not in ORDER]
    if unknown:
        raise SystemExit(f"FAIL — market directory with no MARKET_META entry: {unknown}")

    body = (
        "// GENERATED by scripts/build_market_registry.py — DO NOT HAND-EDIT.\n"
        "// Market is decided by FILE PLACEMENT: engine/raw_ohlc/{MARKET}/{TICKER}.csv.\n"
        "// Never infer a stock's market from asset_class again — see the script header\n"
        "// for the 29-Jul-2026 failure where 34 international names fell into the EGX tab.\n"
        "const MARKET_OF = " + json.dumps(dict(sorted(reg.items())), indent=1) + ";\n\n"
        "const MARKET_META = " + json.dumps(dict(MARKET_META), indent=1) + ";\n\n"
        "// Tab-group render order.\n"
        "const MARKET_ORDER = " + json.dumps(ORDER) + ";\n\n"
        "// Resolver — USE THIS, not MARKET_OF directly. The keys above are the LEDGER\n"
        "// spelling of each name; TICKERS spells three of them differently (SAMSUNG vs\n"
        "// Samsung, KAKAO vs Kakao). A page that indexed MARKET_OF straight with a\n"
        "// TICKERS key got undefined for those and quietly grouped them somewhere else.\n"
        "const MARKET_OF_CI = " + json.dumps(
            {t.upper(): m for t, m in sorted(reg.items())}, indent=1) + ";\n"
        "function marketOf(tk){\n"
        "  if (!tk) return null;\n"
        "  return MARKET_OF[tk] || MARKET_OF_CI[String(tk).toUpperCase()] || null;\n"
        "}\n"
        "function marketLabel(m){\n"
        "  return (MARKET_META[m] && MARKET_META[m].label) || m;\n"
        "}\n"
        "function marketRank(m){\n"
        "  var i = MARKET_ORDER.indexOf(m);\n"
        "  return i < 0 ? 99 : i;\n"
        "}\n"
    )

    if write:
        with open(OUT, "w") as f:
            f.write(body)
        chk = subprocess.run(["node", "--check", OUT], capture_output=True, text=True)
        if chk.returncode:
            raise SystemExit("FAIL — emitted markets.js does not parse:\n" + chk.stderr)
        # verify by IMPORT, not by parse
        imp = subprocess.run(
            ["node", "-e",
             "const fs=require('fs'),vm=require('vm');"
             "const c=vm.createContext({console,globalThis:undefined});"
             "vm.runInContext(\"var globalThis=this;\"+fs.readFileSync(process.argv[1],'utf8')"
             "+'\\n;globalThis.__M=MARKET_OF;globalThis.__O=MARKET_ORDER;',c);"
             "if(Object.keys(c.__M).length<1)throw new Error('empty registry');"
             "console.log('imported OK — '+Object.keys(c.__M).length+' tickers, '+c.__O.length+' markets');",
             OUT], capture_output=True, text=True)
        if imp.returncode:
            raise SystemExit("FAIL — emitted markets.js does not IMPORT:\n" + imp.stderr)
        print(f"wrote {os.path.relpath(OUT, ROOT)} — {imp.stdout.strip()}")
    else:
        print("\n(dry run — pass --write to emit assets/markets.js)")


if __name__ == "__main__":
    main()
