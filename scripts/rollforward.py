#!/usr/bin/env python3
"""rollforward.py — take ONE covered name from a fresh OHLC file to a published
roll-forward, end to end. STEPs 1-7 of Rollforward_and_Grading_Protocol.md, one
command, every fork decided from the data rather than asked about.

WHY THIS EXISTS [R-RF-01, 24-Aug-2026]
--------------------------------------
Reported symptom: "I update the prices for 2 stocks and ask for the calibration
published to the ledger and the prediction rolled forward to the stock page. One
runs smoothly and the other stumbles into many problems and keeps asking
complicated questions."

Both halves of that are real, and neither is randomness in the agent. The tail of
this pipeline has had a driver since 07-Aug-2026 (`publish_site.py`) and runs the
same way every time; the FRONT half — Steps 1 to 6 — had none. It was re-assembled
out of a 329-line prose protocol on each pass, across six tools, and it contains
four forks whose answer is DIFFERENT FOR DIFFERENT NAMES ON THE SAME DAY. Two
stocks posted in one sitting genuinely take two different routes; only one of them
is the route the last roll-forward took, so only one of them feels familiar.

The four forks, measured on the live repo on 24-Aug-2026:

  1. METRONOME vs MID-CYCLE (STEP 0 decision (a)) — the big one. A name whose
     current 1-month has matured must be struck with `rollforward_one.py` (two
     ledger rows); a name whose 1-month has not must be refreshed with
     `refresh_cone_one.py` (no ledger row). Getting it wrong is not cosmetic: the
     wrong tool either strikes a cohort the metronome never called for and breaks
     the lifecycle invariant, or silently skips the strike the ledger was owed. On
     24-Aug-2026 2POINTZERO and ADIBUAE were AT their metronome (1M grade_date
     2026-08-24) while DEWA, PHDC and TMGH were three weeks off it (2026-09-21,
     2026-09-23). The decision is a date comparison the repo can make; there was
     no code that made it, so it was made by reading, or asked about.

  2. THE MATERIALITY FORK, which three documents answered three different ways.
     R-CAL-01 was amended on 23-Aug-2026: material APPLIES and ANNOUNCES, it does
     not block. `auto_refresh.py` and the workflow body implement the amendment.
     But STEP 2 of Rollforward_and_Grading_Protocol.md still read "stop, do not
     proceed to Step 3/4 ... this is a PR-gated event, not an auto-apply one", and
     the calibration workflow's own header comment still described the PR that its
     body no longer opens. An agent that reached the fork through the protocol
     stopped and asked; one that reached it through the digest carried on. Same
     request, same day, opposite behaviour. Both stale texts are corrected in the
     same commit as this file.

  3. SERIES vs SITE KEY. Three of the 93 published names do not sit at
     raw_ohlc/{MARKET}/{KEY}.csv — 2POINTZERO is TWOPOINTZERO, ADIBUAE is AE/ADIB
     (EG/ADIB is a different company), ALRAJHI is SA/RAJHI. The obvious command
     fails on exactly those three, and the map that resolves them existed only
     inside a check script, where the roll-forward tools never looked.

  4. WHAT IS DELIBERATELY NOT TOUCHED — fair{}, the slider's factor-stack
     constants, the backtest PNG. Every pass had to re-derive the list, and STEP 6
     pointed at `ledger_scorer.py` + `viz.py`, which have lived under
     engine/lab/legacy_tooling/ since the PNG regen moved to `metal_backtest.py`.

This module adds NO rule and computes NO number of its own. Every step is the
existing tool, called in the protocol's order with the protocol's arguments; the
only thing that is new is that the sequence and the four forks are executable
instead of remembered. That is the same move this repo has already made three
times — `grade_ledger.py` ("the convention lived in whoever's head was doing it
that day"), `sweep_ledger.py` ("could only be run by hand-rolling a driver each
time"), `refresh_cone_one.py` ("that rule existed only as prose") — applied to
the one thing left over: the orchestration itself.

WHAT IT DOES NOT DECIDE. A genuine judgement still stops the run and says exactly
what it needs, in one line, with the number that forced it: a partial-vs-full OHLC
export that does not splice cleanly (STEP 1), a market that RAISED in the refit, a
name with no 1-month cohort on record (that is a first publish, not a roll-forward),
and a metals 12-month whose annual clock has come round. Those are decisions. The
other four were never decisions; they were lookups.

RUN
    python3 scripts/rollforward.py DEWA                  # dry run, decides + reports
    python3 scripts/rollforward.py DEWA --write          # ...and writes locally
    python3 scripts/rollforward.py DEWA --write --ship   # ...and publishes it live
    python3 scripts/rollforward.py --check-resolver      # CI: all 93 keys resolve

--ship hands off to scripts/publish_site.py, which owns the mechanical tail
(surfaces -> gates -> render-verify -> commit -> push -> PR -> merge -> deploy).

ONE HONEST CAVEAT ON THE DRY RUN. Without --write nothing reaches assets/data.js,
market_profiles.py, fitted_configs.json or any page -- but auto_refresh rebuilds the
content-hashed panel CACHE (engine/panels/, engine/panel_hashes.json) whichever way
it is called, so a dry run against a library you are still testing leaves those two
paths dirty. They are derived and safe to `git checkout --`; saying so here is
cheaper than someone discovering it in `git status` and wondering what else ran.

EVERY STEP FAILS LOUDLY. A roll-forward that half-works is worse than one that stops.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

# The resolution maps live in ONE place each and are imported, never copied --
# the same discipline publish_site.py applies to LEDGER_ALIAS. check_data_freshness
# is the module that already carried SERIES_OVERRIDE and METAL_MARKET; copying them
# here is how the two would drift apart, which is defect class 3 above all over again.
from check_data_freshness import (EXCHANGE_MARKET, LEDGER_ALIAS,  # noqa: E402
                                  METAL_MARKET, SERIES_OVERRIDE)

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# ---------------------------------------------------------------- plumbing
def die(msg: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"\n  STOP  {msg}\n", file=sys.stderr)
    sys.exit(1)


def step(n: str, msg: str) -> None:
    print(f"\n[{n}] {msg}")


def run(cmd: list[str], *, cwd: str = ROOT, check: bool = True,
        echo: bool = True) -> tuple[int, str]:
    """Run a command and stream its output into the report. Non-zero is fatal
    unless check=False -- a step that failed and was not noticed is the whole
    failure mode this file exists to remove."""
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=1800)
    out = (p.stdout or '') + (p.stderr or '')
    if echo:
        for line in out.rstrip().splitlines():
            print(f"      {line}")
    if check and p.returncode != 0:
        die(f"command failed: {' '.join(cmd)}")
    return p.returncode, out


def node_json(script: str) -> dict:
    """Read data.js by LOADING it, never by regex. A regex over a file this size
    has already mis-parsed it twice in this repo's history (the unquoted
    "2POINTZERO" key, the indentation-keyed `dist` span)."""
    js = ("const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);"
          "vm.runInContext(fs.readFileSync('assets/data.js','utf8')"
          "+';globalThis.__T=Object.assign({},typeof METALS!==\"undefined\"?METALS:{},TICKERS)"
          ";globalThis.__L=LEDGER;',c);"
          "const T=c.__T,L=c.__L;" + script)
    p = subprocess.run(['node', '-e', js], cwd=ROOT, text=True,
                       capture_output=True, timeout=300)
    if p.returncode != 0:
        die(f"could not load assets/data.js:\n{(p.stderr or '').strip()[:2000]}")
    return json.loads(p.stdout)


def dmy(iso: str) -> str:
    """ISO -> the DD-Mon-YYYY form rollforward_one/refresh_cone_one take."""
    y, m, d = (int(x) for x in iso.split('-'))
    return f"{d:02d}-{MONTHS[m - 1]}-{y}"


# ---------------------------------------------------------------- step 1
def resolve(key: str) -> tuple[str, str, str]:
    """(market, series, ledger instrument) for a published site key.

    Market comes from the entry's own exchange prefix, series from the one
    published override map. Both are then PROVEN against file placement, which is
    the standing authority ("market and ticker are decided by FILE PLACEMENT").
    ADIB is the case that needs all three: the key exists in AE and EG alike, and
    only the prefix says which company is meant."""
    if key in METAL_MARKET:
        market, series = METAL_MARKET[key]
    else:
        got = node_json(f"const e=T[{json.dumps(key)}];"
                        "process.stdout.write(JSON.stringify(e?{code:e.code||''}:null))")
        if got is None:
            die(f"{key} is not a published name in assets/data.js. "
                f"A new name is a STUDY (see engine/Study_Initiation_Prompt.md), "
                f"not a roll-forward.")
        prefix = str(got['code']).split(':')[0]
        market = EXCHANGE_MARKET.get(prefix)
        if not market:
            die(f"{key}: exchange prefix {prefix!r} maps to no market. Add it to "
                f"EXCHANGE_MARKET in scripts/check_data_freshness.py.")
        series = SERIES_OVERRIDE.get(key, key)

    csv = os.path.join(ENGINE, 'raw_ohlc', market, f'{series}.csv')
    if not os.path.exists(csv):
        die(f"{key}: no library at engine/raw_ohlc/{market}/{series}.csv. "
            f"Post the OHLC export there first -- placing the file IS the "
            f"market/ticker decision and this tool will not guess it.")
    return market, series, LEDGER_ALIAS.get(key, key)


def library_last(market: str, series: str) -> tuple[str, int]:
    """(last session ISO, row count) of the persistent library, read raw. This is
    only used to DECIDE and to REPORT; every number that reaches a published
    surface comes from the engine's own cleaned load."""
    import csv as _csv
    path = os.path.join(ENGINE, 'raw_ohlc', market, f'{series}.csv')
    dates = []
    with open(path, encoding='utf-8-sig', newline='') as fh:
        for row in _csv.DictReader(fh):
            cell = (row.get('Date') or row.get('date') or '').strip().strip('"')
            if not cell:
                continue
            for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%d-%b-%Y', '%b %d, %Y'):
                try:
                    dates.append(datetime.datetime.strptime(cell, fmt).date().isoformat())
                    break
                except ValueError:
                    continue
    if not dates:
        die(f"engine/raw_ohlc/{market}/{series}.csv has no parseable Date column.")
    return max(dates), len(dates)


def published_anchor(key: str) -> str | None:
    """ISO date the PUBLISHED cone is anchored on.

    `spotDate` is prose -- "close 7 Aug 2026", zero-padded on some entries and not
    on others -- so it is parsed by engine/apply_technicals.spotdate_iso(), the
    one place that regex lives, and NOT compared as a raw string. A raw compare
    against an ISO date reads "c" > "2" and answers True for every name on the
    site, which is a check that always passes: the worst kind.
    """
    sys.path.insert(0, ENGINE)
    from apply_technicals import spotdate_iso  # noqa: E402
    raw = node_json(f"const e=T[{json.dumps(key)}];"
                    "process.stdout.write(JSON.stringify(e.spotDate||''))")
    return spotdate_iso(f'spotDate: "{raw}",') if raw else None


# ---------------------------------------------------------------- step 4
def decide(inst: str, key: str, new_anchor: str) -> tuple[str, str, dict]:
    """METRONOME or MID-CYCLE, from the ledger, with the reason that decided it.

    THE RULE (STEP 0 decision (a), made executable): the 1-month maturity is the
    metronome. So the name is at its monthly event iff the CURRENT 1-month row --
    the latest anchor for that instrument at that horizon -- has reached its stored
    calendar grade_date by the new anchor. Anything earlier is mid-cycle data and
    refreshes the displayed cone only.

    The comparison is against the NEW ANCHOR, not against today's wall clock: the
    forecast is a commitment about a date in that name's own trading calendar, and
    a library that runs to Thursday does not become a Friday event because the
    session running it happens to be Friday."""
    rows = node_json(
        f"const inst={json.dumps(inst)};"
        "const rs=L.filter(r=>r.instrument===inst);"
        "process.stdout.write(JSON.stringify(rs.map(r=>({h:r.horizon_label,"
        "a:r.anchor_date,g:r.grade_date,done:r.realized_close!=null,c:r.cycle_no}))))")
    if not rows:
        die(f"{key}: no LEDGER rows for instrument {inst!r}. A name with no cohort "
            f"on record is a FIRST PUBLISH (engine/Publish_Protocol.md), not a "
            f"roll-forward -- this tool will not mint a cycle-1 ledger from a "
            f"price update.")

    ones = [r for r in rows if r['h'] == '1 month']
    if not ones:
        die(f"{key}: {len(rows)} ledger rows but no 1-month cohort, so there is no "
            f"metronome to read. Resolve by hand and say which horizon is current.")
    cur = max(ones, key=lambda r: r['a'])

    extra = {'cur_1m': cur, 'cycle': max((r['c'] or 0) for r in rows)}
    # The metals 12-month rides its own annual clock and is NEVER struck by the
    # monthly path -- rollforward_one emits 1M and 3M only. If its year is up, that
    # is a real decision for a human, so it is reported rather than absorbed.
    twelve = [r for r in rows if r['h'] == '12 months' and not r['done']]
    if twelve:
        t = max(twelve, key=lambda r: r['a'])
        if t['g'] <= new_anchor:
            extra['annual_due'] = t

    if cur['g'] <= new_anchor:
        return ('metronome',
                f"the current 1-month (anchor {cur['a']}) reached its grade date "
                f"{cur['g']} on or before the new anchor {new_anchor}", extra)
    return ('midcycle',
            f"the current 1-month (anchor {cur['a']}) does not mature until "
            f"{cur['g']}, after the new anchor {new_anchor}", extra)


# ---------------------------------------------------------------- step 6
def snapshot() -> dict:
    return node_json(
        "const open=L.filter(r=>r.realized_close==null);"
        "const bad=[];const byi={};"
        "for(const r of open){(byi[r.instrument]=byi[r.instrument]||[]).push(r);}"
        "for(const i of Object.keys(byi)){"
        "  const hs=[...new Set(byi[i].map(r=>r.horizon_label))];"
        "  for(const h of hs){const hr=byi[i].filter(r=>r.horizon_label===h);"
        "    const n=Math.max(...hr.map(r=>r.anchor_date));"
        "    const k=hr.filter(r=>r.anchor_date===n).length;"
        "    if(k>1) bad.push(i+' '+h+': '+k+' open rows share the latest anchor '+n);}}"
        "process.stdout.write(JSON.stringify({keys:Object.keys(T).length,"
        "rows:L.length,open:open.length,breaches:bad}))")


def verify(before: dict, expect_new_rows: int) -> None:
    """The standing data.js verification rules, all four, every time.

    node --check proves it parses; LOADING it proves the structure survived (an
    assert-guarded string replacement cannot see a stitch point); the counts are
    taken against a KNOWN TOTAL because three separate tools have reported "0
    skipped" while silently dropping a name; and the lifecycle invariant is
    asserted after every ledger write."""
    for f in ('assets/data.js', 'assets/app.js'):
        run(['node', '--check', f], echo=False)
    after = snapshot()
    if after['keys'] != before['keys']:
        die(f"published-name count moved {before['keys']} -> {after['keys']}")
    if after['rows'] != before['rows'] + expect_new_rows:
        die(f"LEDGER row count moved {before['rows']} -> {after['rows']}, "
            f"expected +{expect_new_rows}")
    new_breach = [b for b in after['breaches'] if b not in before['breaches']]
    if new_breach:
        die("LIFECYCLE INVARIANT BROKEN by this pass:\n        "
            + "\n        ".join(new_breach))
    print(f"      {after['keys']} published names load, {after['rows']} ledger rows "
          f"(+{expect_new_rows}), {after['open']} open")
    if after['breaches']:
        print(f"      {len(after['breaches'])} pre-existing lifecycle breach(es), "
              f"unchanged by this pass and REPORTED not fixed:")
        for b in after['breaches']:
            print(f"        {b}")


def overlay_gate(only: list[str] | None = None) -> tuple[int, str]:
    """Run the MANDATORY chart-overlay gate, including the server it needs.

    The gate loads every page carrying a chart over HTTP and fails if an injected
    level line escapes the viewBox. Nothing else catches that: no exception is
    raised and the page looks fine. It has always required a static server on
    :8765 that nobody automated -- publish_site.py's gates() runs the freshness
    and page-integrity checks and not this one -- so the gate the protocol calls
    MANDATORY ran only when someone remembered to start a server first. Starting
    it here is the same move as the rest of this file: a step that is required
    every time is performed, not remembered.
    """
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'],
                           cwd=ROOT, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    try:
        import urllib.request
        for _ in range(60):
            try:
                urllib.request.urlopen('http://localhost:8765/', timeout=1).read(1)
                break
            except Exception:
                time.sleep(0.25)
        else:
            return 1, 'could not start a static server on :8765 for the overlay gate'
        cmd = ['node', 'scripts/check_ta_chart_overlay.js']
        if only:
            cmd += ['http://localhost:8765', '--only'] + list(only)
        return run(cmd, check=False)
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=10)
        except subprocess.TimeoutExpired:
            srv.kill()


# ---------------------------------------------------------------- resolver check
def check_resolver() -> int:
    """[R-ENF-01] The rule checked from OUTSIDE the thing it governs: every
    published key must resolve to a raw library that exists. Runs in CI, so a name
    added with a mismatched stem fails on the commit that adds it rather than on
    the first person who tries to roll it forward."""
    # One node call, not 93: the check runs on every push touching data.js.
    codes = node_json("const o={};for(const k of Object.keys(T))o[k]=T[k].code||'';"
                      "process.stdout.write(JSON.stringify(o))")
    bad = []
    for k in sorted(codes):
        if k in METAL_MARKET:
            market, series = METAL_MARKET[k]
        else:
            market = EXCHANGE_MARKET.get(str(codes[k]).split(':')[0])
            series = SERIES_OVERRIDE.get(k, k)
        if not market:
            bad.append(f'{k}: no market from code prefix')
            continue
        if not os.path.exists(os.path.join(ENGINE, 'raw_ohlc', market, f'{series}.csv')):
            bad.append(f'{k}: no raw_ohlc/{market}/{series}.csv '
                       f'(add a SERIES_OVERRIDE entry if the stem differs)')
    print(f'resolver: {len(codes)} published names, {len(codes) - len(bad)} resolve')
    for b in bad:
        print(f'  FAIL {b}')
    return 1 if bad else 0


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(
        description='One command for STEPs 1-7 of the roll-forward protocol.')
    ap.add_argument('ticker', nargs='?', help='published site key, e.g. DEWA')
    ap.add_argument('--write', action='store_true',
                    help='write locally (default is a full dry run)')
    ap.add_argument('--ship', action='store_true',
                    help='hand off to publish_site.py --ship when the pass is clean')
    ap.add_argument('--q-annual', type=float, default=0.0,
                    help='sourced dividend yield; 0 is flagged in the note, never split')
    ap.add_argument('--mode', choices=('auto', 'metronome', 'midcycle'), default='auto',
                    help='override the metronome decision (records the override)')
    ap.add_argument('--check-resolver', action='store_true',
                    help='CI mode: assert every published key resolves to a library')
    args = ap.parse_args()

    if args.check_resolver:
        return check_resolver()
    if not args.ticker:
        ap.error('a ticker is required (or --check-resolver)')

    key = args.ticker.upper()
    wrote = '' if args.write else '   [DRY RUN — nothing will be written]'
    print(f"\n=== ROLL-FORWARD {key}{wrote} ===")

    # -------------------------------------------------- 1: resolve
    step('1/7', 'resolving the name against file placement (STEP 1)')
    market, series, inst = resolve(key)
    last, nrows = library_last(market, series)
    print(f"      {key}: market {market}, series {series}, ledger instrument {inst}")
    print(f"      library engine/raw_ohlc/{market}/{series}.csv — "
          f"{nrows} rows, last session {last}")
    before = snapshot()
    published = published_anchor(key)
    print(f"      published cone anchored {published or '(none)'}")
    if published and published >= last:
        print(f"      NOTE: the library does not advance past the published cone. "
              f"Steps 4/5 are idempotent; nothing will move.")

    # -------------------------------------------------- 2: calibration
    step('2/7', 'Step 0.0 gate + full-panel refit (STEP 2)')
    print("      R-CAL-01: a MATERIAL change APPLIES and is ANNOUNCED — it does not "
          "block.\n      Run engine/auto_refresh.py --halt-on-material for the "
          "pre-23-Aug behaviour.")
    cmd = ['python3', 'auto_refresh.py'] + (['--apply'] if args.write else [])
    rc, out = run(cmd, cwd=ENGINE, check=False)
    mat = os.path.join(ENGINE, 'PENDING_REVIEW', 'LAST_RUN_MATERIAL.txt')
    if os.path.exists(mat) and os.path.getsize(mat):
        print("      MATERIAL — applied and announced. Reasons:")
        for line in open(mat, encoding='utf-8').read().rstrip().splitlines():
            print(f"        {line}")
    if rc != 0:
        # ONE BLOCKED MARKET MUST NEVER FREEZE THE OTHERS. Only a raise in OUR
        # market stops this run; another market's traceback is reported and passed.
        if f'=== {market}:' in out and 'PIPELINE ERROR' in out.split(f'=== {market}:')[-1].split('\n===')[0]:
            die(f"{market} RAISED in the refit — its production config is untouched. "
                f"See engine/PENDING_REVIEW/{market}_*-ERROR.md. An exception is not "
                f"evidence; this name cannot be struck on it.")
        print("      another market raised (not this one) — reported, continuing")
    run(['python3', '-c', 'import market_profiles, mc_v3, data_quality, adaptive_width; '
         'from market_profiles import PROFILES; '
         'print("engine imports cleanly;", len(PROFILES), "profiles")'], cwd=ENGINE)

    # -------------------------------------------------- 3: grade
    step('3/7', 'grading every now-matured cohort (STEP 3)')
    today = datetime.date.today().isoformat()
    run(['python3', 'scripts/sweep_ledger.py', '--today', today]
        + (['--write'] if args.write else []))

    # -------------------------------------------------- 4: decide + strike
    step('4/7', 'metronome or mid-cycle? (STEP 0 decision (a)) — then STEP 4/5')
    mode, why, extra = decide(inst, key, last)
    if args.mode != 'auto' and args.mode != mode:
        print(f"      computed {mode.upper()} ({why})")
        print(f"      OVERRIDDEN to {args.mode.upper()} by --mode. The override is "
              f"recorded here and nowhere else — it does not reach the ledger note.")
        mode = args.mode
    else:
        print(f"      {mode.upper()}: {why}")
    if 'annual_due' in extra:
        a = extra['annual_due']
        print(f"      SEPARATE ITEM — the 12-month cohort (anchor {a['a']}) reached "
              f"{a['g']} and is DUE. It rides its own annual clock and is not struck "
              f"here; grade and re-strike it as its own pass.")

    tool = 'rollforward_one.py' if mode == 'metronome' else 'refresh_cone_one.py'
    expect_rows = 2 if mode == 'metronome' else 0
    if published and published >= last and mode == 'midcycle':
        print("      skipped — the cone is already anchored on the last session")
        expect_rows = 0
    else:
        run(['python3', tool, market, series, key, '--today', dmy(last),
             '--q-annual', str(args.q_annual)] + (['--write'] if args.write else []),
            cwd=ENGINE)
    if not args.write:
        expect_rows = 0

    # -------------------------------------------------- 5: technicals + chart
    step('5/7', 'technical read, chart, overlay gate (STEP 5B) — same pass, always')
    run(['python3', 'apply_technicals.py', '--only', key]
        + (['--write'] if args.write else []), cwd=ENGINE)
    run(['python3', 'ta_chart.py', '--only', key]
        + (['--write'] if args.write else []), cwd=ENGINE)
    if args.write:
        # THE GATE'S OUTPUT IS NEVER SWALLOWED. Nothing else catches a level line
        # drawn outside the viewBox -- no exception is raised and the page looks
        # fine -- so hiding this step's output on the grounds that it usually
        # passes would rebuild the exact blindness it was written to remove.
        rc, out = overlay_gate([key])
        if rc != 0:
            if 'Cannot find module' in out:
                die("the chart-overlay gate could not run: its dependency is not "
                    "installed here (npm i playwright). The pass is INCOMPLETE -- "
                    "a gate that did not run is not a gate that passed, and this "
                    "one is the only thing that catches a level line drawn outside "
                    "the viewBox.")
            die("chart-overlay gate FAILED — a published level line escapes its "
                "viewBox. Do not publish: a fresh level on a frozen chart is worse "
                "than leaving both stale.")
        print('      overlay gate PASSED — no level line escapes any viewBox')
    else:
        print('      overlay gate deferred (nothing written to render)')

    # -------------------------------------------------- 6: verify
    step('6/7', 'verifying assets/data.js by LOAD, against known totals')
    if args.write:
        verify(before, expect_rows)
        run(['python3', 'scripts/check_data_freshness.py'])
    else:
        print('      nothing written — verification runs on the --write pass')

    # -------------------------------------------------- 7: report / ship
    step('7/7', 'report')
    print(f"      {key} ({market}/{series}) rolled forward to {last} via {tool}")
    print(f"      mode {mode.upper()} — {why}")
    print(f"      CHANGED: spot, spotDate, dist (both horizons), touch (at the SAME "
          f"absolute levels), levels, tech, asof, the chart"
          + (", and 2 LEDGER rows" if expect_rows else ""))
    print(f"      DELIBERATELY UNTOUCHED: fair{{bear,base,full}} (the fundamental "
          f"clock — it moves only on a real study refresh), the interactive slider's "
          f"factor-stack constants (CONT_FIXED/EV_FIXED/GEO_MEAN/... — fit once to the "
          f"study's driver stack, re-fitting them is a study task), and every open "
          f"cohort on an earlier cycle (they stay open and grade on their own terms).")
    print(f"      BACKTEST PNG assets/calibration_{key}.png: a coarse ~quarterly "
          f"construct spanning years — a single new cohort essentially never moves it. "
          f"Regenerate deliberately with `python3 engine/metal_backtest.py {key}` if "
          f"this name's own library or fit actually moved, not by default.")

    if args.ship:
        if not args.write:
            die('--ship needs --write: there is nothing in the working tree to publish.')
        step('ship', 'handing off to publish_site.py (STEP 7)')
        run(['python3', 'scripts/publish_site.py', '--ticker', key,
             '--ship', '--republish'])
    elif args.write:
        print(f"\n      Local only. To publish: "
              f"python3 scripts/publish_site.py --ticker {key} --ship --republish")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
