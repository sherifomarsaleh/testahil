#!/usr/bin/env python3
"""refresh_pages.py — bring EVERY published page back onto the current library.

WHY THIS EXISTS
---------------
Posting an OHLC file already fires `testahil-calibration.yml`, which refits that
stock's whole market and commits. Measured on 25-Aug-2026, that workflow writes
ONLY under `engine/` — `market_profiles.py`, `fitted_configs.json`, the panels,
`PENDING_REVIEW`. It never touches `assets/data.js`. So an upload updated the
MODEL and left every price a visitor sees exactly where it was.

The site still deployed: `deploy-pages.yml` fires on any push to main, and the
`page-integrity` job that DOES catch this ("technical read is on X but the
cleaned library now ends Y") is deliberately non-blocking. Net effect — upload a
CSV, the calibration commits, that commit deploys, the pages show last month's
prices, and a red X sits in the Actions tab saying so.

Every per-name tool needed to fix that already existed. What did not exist was
the thing that decides WHICH names need it and runs them in the right order with
the gates attached. That is all this is: an orchestrator over
`refresh_cone_one` -> `apply_technicals` -> `ta_chart` ->
`build_name_calibration` -> the overlay gate -> `check_data_freshness`. No new
cone mathematics, no new technical construction.

WHAT IT WILL NOT DO
-------------------
* It never strikes a LEDGER row. Ledger strikes belong to the 1-month maturity
  metronome (Roll-Forward & Grading Protocol STEP 0); a mid-cycle data arrival
  refreshes the displayed cone and the technical read and nothing else.
  `refresh_cone_one` asserts this per name; this module asserts it again across
  the whole pass, because a per-name check cannot see a row appearing elsewhere.
* It never touches `fair{}`, the slider's factor-stack constants, or `files`.
  Fair value runs on its own clock and moves only in a study refresh.
* It REFUSES a name whose dividend yield it cannot source rather than defaulting
  it to zero. See `recover_q()` — this is the one input that would silently move
  a published cone, and a bulk tool guessing it 90 times is precisely the kind of
  quiet wrongness the rest of this repo is built to prevent.
* It does not refresh METALS cones. `refresh_cone_one` is bounded to the TICKERS
  object by construction (metals carry a different, t252 twelve-month shape on
  their own annual clock). Metals still get their technical read and chart from
  `apply_technicals`/`ta_chart` below, and are reported as cone-skipped rather
  than passed over in silence.

Run:  python3 scripts/refresh_pages.py                 # plan only, writes nothing
      python3 scripts/refresh_pages.py --write         # apply, with every gate
      python3 scripts/refresh_pages.py --only COMI ABUK
      python3 scripts/refresh_pages.py --write --q TSLA=0.0 --q NVDA=0.0003
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'engine')
DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
sys.path.insert(0, ENGINE)

import technicals as TA                                          # noqa: E402
from apply_technicals import (EXCHANGE_MARKET, SERIES_OVERRIDE,  # noqa: E402
                              METAL_MARKET)
import refresh_cone_one                                          # noqa: E402
from market_profiles import PROFILES                              # noqa: E402
from auto_refresh import BAND_TOL, band_halfwidth                 # noqa: E402
from strike_cohorts import load_clean                             # noqa: E402
import adaptive_width as AW                                       # noqa: E402

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# ------------------------------------------------------------------ data.js IO
_NODE_READ = (
    "const fs=require('fs'),vm=require('vm');const s={};vm.createContext(s);"
    "vm.runInContext(fs.readFileSync(process.argv[1],'utf8')"
    "+';globalThis.__T=TICKERS;globalThis.__L=LEDGER;"
    "globalThis.__M=(typeof METALS!==\"undefined\")?METALS:{};',s);"
    "process.stdout.write(JSON.stringify({t:s.__T,l:s.__L,m:s.__M}));"
)


def read_data_js() -> dict:
    """Load data.js by EVALUATING it, never by regex.

    data.js is JavaScript with comments; and per the standing rule a string
    replacement that asserts its old text existed still cannot see whether the
    surrounding structure survived. Loading it in node and asserting on the
    parsed objects is the only check that can.
    """
    out = subprocess.run(['node', '-e', _NODE_READ, DATA_JS],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f'data.js will not evaluate in node:\n{out.stderr}')
    return json.loads(out.stdout)


def counts(d: dict) -> tuple[int, int, int]:
    return len(d['t']), len(d['m']), len(d['l'])


# ------------------------------------------------------------------- discovery
def market_series(key: str, entry: dict) -> tuple[str, str] | None:
    """(market folder, library series name) for a site key, or None."""
    if key in METAL_MARKET:
        return METAL_MARKET[key]
    code = str(entry.get('code') or '')
    mkt = EXCHANGE_MARKET.get(code.split(':')[0])
    if not mkt:
        return None
    return mkt, SERIES_OVERRIDE.get(key, key)


def stale_names(data: dict, only: list[str] | None, today_iso: str) -> tuple[list, list]:
    """Names whose CLEANED library now ends past their published cone anchor.

    Compared against the CLEANED series — the same Step 0.0 gate the engine runs
    — and not the raw tail. A raw comparison cries wolf: LCSW's raw file once
    ended on a stale no-trade print the gate drops, so the raw last row and the
    correct read date legitimately differ. This mirrors check 3 of
    check_data_freshness.py rather than inventing a second definition of "stale".
    """
    due, notes = [], []
    entries = list(data['t'].items()) + list(data['m'].items())
    for key, e in sorted(entries):
        if only and key not in only:
            continue
        ms = market_series(key, e)
        if not ms:
            notes.append((key, 'no market resolved from its code: prefix'))
            continue
        mkt, series = ms
        published = (((e.get('asof') or {}).get('mc') or {}).get('data')) or ''
        try:
            clean_last = TA.compute(mkt, series, computed_on=today_iso)['data_date']
        except Exception as exc:                                  # noqa: BLE001
            notes.append((key, f'technicals.compute failed: {type(exc).__name__}: {exc}'))
            continue
        if not published:
            notes.append((key, 'no asof.mc.data stamp — cannot tell if it is stale'))
            continue
        if clean_last > published:
            due.append({'key': key, 'market': mkt, 'series': series,
                        'published': published, 'library': clean_last,
                        'is_metal': key in METAL_MARKET})
    return due, notes


# ---------------------------------------------------------------- dividend yield
# The value is bounded so a SENTENCE-ENDING PERIOD is not swallowed into it:
# the notes read 'q_annual=0.0511.' and a greedy [0-9.]+ captures '0.0511.',
# which float() rejects — so the whole pass died on the SIXTH name rather
# than on the first, i.e. after it had already looked correct.
#
# Same defect class as the fit-drift regex in this file, which was written
# bounded for exactly this reason; this one was not, and nothing compared
# them. Now \d+(?:\.\d+)? in both.
_Q = re.compile(r'q[_ ]?annual\s*[=:]\s*(\d+(?:\.\d+)?)', re.I)


def recover_q(data: dict, key: str) -> float | None:
    """The dividend yield this name's own last published strike was built on.

    The carry drift is ln(1+rf) - ln(1+q), so q is not decoration: getting it
    wrong moves the centre of the published cone. The protocol permits defaulting
    it to 0 WITH A FLAG when it is genuinely unsourceable — that is a considered,
    per-name decision, and a bulk tool applying it silently to ninety names is not
    the same act. So this returns None and the caller REFUSES the name.

    Source of record is the newest LEDGER note that states one, which is where
    strike_cohorts writes it. Measured 25-Aug-2026: recoverable for 85 of 93
    instruments; the 8 without carry an EMPTY note (TMPV, INFY, RELIANCE, AAPL,
    NVDA, TSLA, QGTS, IQCD) and are exactly the long-stale IN/US/QA names, so no
    older row helps either. Pass --q KEY=VALUE to supply one deliberately.

    THE LEDGER INSTRUMENT IS NOT THE TICKERS KEY AND MUST NOT BE ASSUMED TO BE
    [01-Sep-2026]. Five instruments are written in title case (Gold, Silver,
    Platinum, Kakao, Samsung) against upper-case object keys. A hand-kept alias
    covered the three metals and not the two Korean equities, so KAKAO and
    SAMSUNG matched NO ledger row and this function returned None — reported by
    the caller as "no sourced q_annual", which reads as a considered refusal and
    was in fact an empty lookup ([R-ENF-04]). Both names state q_annual in their
    own newest note. Resolution is now case-insensitive over the ledger's own
    instrument set, and AMBIGUITY REFUSES rather than guesses: if two distinct
    instruments differed only by case, no lookup here could tell them apart, so
    the name is returned unresolved and the caller refuses it as before.
    Measured on adoption: 93 instruments, no case-insensitive collision, and the
    unresolved set falls from 10 back to the 8 the paragraph above names.
    """
    want_ci = key.upper()
    matched = {r.get('instrument') for r in data['l']
               if isinstance(r.get('instrument'), str)
               and r['instrument'].upper() == want_ci}
    if len(matched) > 1:                      # two names one lookup cannot separate
        return None
    rows = [r for r in data['l'] if r.get('instrument') in matched]
    rows.sort(key=lambda r: r.get('anchor_date') or '', reverse=True)
    for r in rows:
        m = _Q.search(r.get('note') or '')
        if m:
            return float(m.group(1))
    return None


# ------------------------------------------------------------------ fit drift
_FIT = re.compile(r'([A-Z]{2,3})\s+live fit\s+nu=(\d+(?:\.\d+)?),\s*'
                  r'width_cal=(\d+(?:\.\d+)?)', re.I)


def fit_drift(data: dict) -> tuple[list, list]:
    """Names whose published cone stands on a fit that has since moved.

    A SECOND axis of staleness. A cone is re-struck when PRICES arrive; the
    market fit is re-estimated whenever any name in that market is posted. The
    two are not the same event, so a refit silently leaves every already-
    published cone standing on the fit it was struck under.

    READ OFF THE ENTRY'S OWN `fit` STAMP, not the ledger note. The note was the
    only record available before restrike_entry stamped the entry, and it was
    wrong twice over: it carries the POOLED width_cal and never the per-name
    overlay multiplier, and a mid-cycle refresh writes no ledger row at all, so
    the newest note can describe a strike the page no longer shows. Measured
    against a full re-strike of all 90 names on 25-Aug-2026
    (engine/fit_drift_audit/), the note MISSED 4 and FALSE-ALARMED on 1. The
    stamp has neither defect: it records `eff` = width_cal * overlay multiplier,
    which is what actually scaled the published cone.

    MATERIALITY IS THE ENGINE'S OWN METRIC, imported rather than reimplemented —
    auto_refresh.band_halfwidth on cal * q95(t(nu)), thresholded at BAND_TOL.
    nu and width_cal TRADE OFF against each other, so comparing them separately
    both misses real changes and fires on noise; the published 90% cone is the
    thing a reader sees and the thing measured here.

    Returns (material, sub_threshold, unstamped). A name with no stamp yet is
    NOT guessed at from its note — it is reported as unstamped and left alone,
    because the note cannot answer the question and pretending otherwise is how
    the previous version got it wrong. Every entry acquires a stamp at its next
    strike.
    """
    material, sub, unstamped = [], [], []
    for key, e in sorted(list(data['t'].items()) + list(data['m'].items())):
        code = str(e.get('code') or '')
        mkt = EXCHANGE_MARKET.get(code.split(':')[0]) or (
            METAL_MARKET.get(key, (None, None))[0])
        p = PROFILES.get(mkt)
        if not p:
            continue
        f = e.get('fit')
        if not isinstance(f, dict) or f.get('eff') is None or f.get('nu') is None:
            unstamped.append(key)
            continue
        struck = band_halfwidth(float(f['nu']), float(f['eff']))
        live_eff = p.width_cal * _live_mult(key, e, mkt, p)
        live = band_halfwidth(p.nu, live_eff)
        if not struck or not live:
            continue
        rel = (live - struck) / struck
        row = {'ledger_key': key, 'market': mkt, 'rel': rel,
               'struck': f"nu={f['nu']}/eff={f['eff']}",
               'live': f"nu={p.nu}/eff={_fmt(live_eff)}"}
        if abs(rel) > BAND_TOL:
            material.append(row)
        elif abs(rel) > 1e-4:          # a cone standing on today's fit has NOT drifted
            sub.append(row)
    return material, sub, unstamped


def _fmt(v) -> str:
    return f'{float(v):.6g}'


def _live_mult(key: str, entry: dict, mkt: str, profile) -> float:
    """TODAY's per-name width multiplier — RECOMPUTED, never read off a record.

    [R-WIDTH-01]: overlay state is read live by recomputing, never inferred. The
    multiplier is a function of BOTH the name's own library and the market fit,
    so a refit alone can move it with no new prices — which is precisely the case
    the library-staleness check cannot see, and precisely why three EG names were
    material on 25-Aug-2026 while their market fit had moved less than 1%.

    Free where it is free: the overlay is per-market, and where it is off the
    multiplier is EXACTLY 1.0 by construction (adaptive_width.live_width_mult
    returns the exact baseline on flag_off), so no library is touched at all.
    Only overlay-active markets pay the load, and this pass already loads every
    library once in stale_names().
    """
    if not getattr(profile, 'width_overlay_active', False):
        return 1.0
    ms = market_series(key, entry)
    if not ms:
        return 1.0
    try:
        df, _ = load_clean(ms[0], ms[1])
        return float(AW.live_width_mult(df, profile))
    except Exception as exc:                                   # noqa: BLE001
        raise SystemExit(f'{key}: cannot recompute the live width overlay '
                         f'({type(exc).__name__}: {exc}). Refusing to report '
                         'drift from a stale or assumed multiplier.')


# --------------------------------------------------------------- shell helpers
def sh(cmd: list[str], cwd: str = ROOT, check: bool = True) -> int:
    print(f'    $ {" ".join(cmd)}')
    p = subprocess.run(cmd, cwd=cwd)
    if check and p.returncode != 0:
        raise SystemExit(f'FAILED ({p.returncode}): {" ".join(cmd)}')
    return p.returncode


def rebuild_name_calibration(check_only: bool = False) -> bool:
    """[R-REC-01] The per-name calibration record, regenerated in THIS pass.

    Every stock's page carries its own record — how many resolved three-month
    tests its history holds and how often the middle and wide bands caught the
    close — and `engine/build_name_calibration.py` computes it from the
    committed panels under the LIVE (nu, width_cal). R-REC-01 requires it
    regenerated "in the same pass as any refit, reshape, panel rebuild or
    roll-forward", for the same reason the technical read is: a page that states
    a fact which moves must not be the thing that remembers it.

    Nothing called it. Not this orchestrator, not testahil-calibration.yml — so
    the record was regenerated only when a human happened to remember, while its
    sibling BANDS record is rebuilt-and-compared from outside by
    check_band_vocabulary.py on every push. The asymmetry is the whole defect.

    IT IS NOT ENOUGH TO RUN THIS ONLY WHEN A PAGE IS STALE. The record is a
    function of the FIT, and the fit is re-estimated on a different trigger than
    the prices: auto_refresh.py refits a whole market and commits, and every
    page can still stand on its own library afterwards. That is exactly the run
    this orchestrator used to end with "Nothing to do" — the one case where the
    record moves and nothing else does.

    The builder self-verifies (node --check on data.js, then LOAD it and assert
    CALIB covers every TICKERS entry, counted against the known total), so a
    clean exit here is that assertion having passed, not this function's opinion.
    """
    cmd = [sys.executable, 'build_name_calibration.py'] + (['--check'] if check_only else [])
    return sh(cmd, cwd=ENGINE, check=not check_only) == 0


def _free_port() -> int:
    import socket as _s
    with _s.socket() as sk:
        sk.bind(('127.0.0.1', 0))
        return sk.getsockname()[1]


def overlay_gate(timeout_s: int = 600) -> None:
    """Render every charted page and fail if an S/R line escapes the viewBox.

    Nothing else catches this: injectLevels() draws outside the 0..320 viewBox
    without throwing, and the page looks fine. Served over HTTP rather than
    file:// because the check drives real pages in a real browser.

    Readiness is probed with a RAW SOCKET, never urllib: urlopen honours
    HTTP(S)_PROXY, so on a proxied runner a probe of 127.0.0.1 is dispatched to
    the proxy and hangs there — which is exactly how this step hung for 15
    minutes against a server that was already up and answering in 1.5ms. The
    port is chosen from the ephemeral range for the same reason a fixed one bit:
    a previous run's socket in TIME_WAIT makes the bind fail, and the gate then
    tests nothing while looking like it ran.
    """
    import socket as _s
    gate = os.path.join(ROOT, 'scripts', 'check_ta_chart_overlay.js')
    if not os.path.exists(gate):
        print('    ! overlay gate script missing — SKIPPED')
        return
    port = _free_port()
    base = f'http://127.0.0.1:{port}'
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=ROOT, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    try:
        deadline = __import__('time').monotonic() + 30
        while True:
            if srv.poll() is not None:
                raise SystemExit(f'the page server died before it served anything '
                                 f'(exit {srv.returncode}) — overlay gate not run')
            try:
                with _s.create_connection(('127.0.0.1', port), timeout=1):
                    break
            except OSError:
                if __import__('time').monotonic() > deadline:
                    raise SystemExit('page server never came up — overlay gate not run')
                __import__('time').sleep(0.2)
        print(f'    $ node {gate} {base}')
        p = subprocess.run(['node', gate, base], cwd=ROOT, timeout=timeout_s)
        if p.returncode != 0:
            raise SystemExit(f'FAILED ({p.returncode}): chart-overlay gate')
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=10)
        except subprocess.TimeoutExpired:
            srv.kill()


# --------------------------------------------------------------------- the pass
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true',
                    help='apply; without it the pass plans and writes nothing')
    ap.add_argument('--only', nargs='*', help='limit to these site keys')
    ap.add_argument('--q', action='append', default=[], metavar='KEY=VALUE',
                    help='supply a dividend yield the ledger cannot source')
    ap.add_argument('--today', help='DD-Mon-YYYY; defaults to today')
    ap.add_argument('--skip-overlay', action='store_true',
                    help='skip the browser chart-overlay gate (needs playwright)')
    ap.add_argument('--restrike-fit-drift', action='store_true',
                    help='also re-strike cones standing on a superseded market fit, '
                         'even where no new prices arrived (republishes a different '
                         'forecast on the same data — a decision, not a refresh)')
    args = ap.parse_args()

    today = (args.today or
             f'{date.today().day:02d}-{MONTHS[date.today().month - 1]}-{date.today().year}')
    today_iso = date.today().isoformat()
    q_override = {}
    for item in args.q:
        k, _, v = item.partition('=')
        q_override[k.strip()] = float(v)

    data = read_data_js()
    before = counts(data)
    print(f'data.js loaded — {before[0]} tickers, {before[1]} metals, '
          f'{before[2]} ledger rows\n')

    due, notes = stale_names(data, args.only, today_iso)
    for key, why in notes:
        print(f'  note  {key}: {why}')
    if notes:
        print()

    material, sub, unstamped = fit_drift(data)
    n_sync = len(data['t']) + len(data['m']) - len(material) - len(sub) - len(unstamped)
    print(f'fit drift: {len(material)} MATERIAL by the [R-CAL-01] gate (90% cone '
          f'moves >{BAND_TOL:.0%}); {len(sub)} drifted sub-threshold; {n_sync} on '
          f'today\'s fit; {len(unstamped)} carry no fit stamp yet')
    if sub:
        print(f'  sub-threshold, reported only: '
              f'{max(abs(d["rel"]) for d in sub):.2%} worst — not acted on, which '
              'is what the materiality gate is for.')
    if unstamped:
        print(f'  unstamped (no `fit` on the entry — each acquires one at its next '
              f'strike; the ledger note cannot answer this and is NOT guessed from): '
              f'{len(unstamped)}')
    drift = material            # only MATERIAL drift is ever acted on
    if drift and not args.restrike_fit_drift:
        by_market: dict[str, int] = {}
        for d in drift:
            by_market[d['market']] = by_market.get(d['market'], 0) + 1
        print('  by market: ' + ', '.join(f'{k} {v}' for k, v in sorted(by_market.items())))
        print('  not acted on — pass --restrike-fit-drift to re-strike them.')
    if args.restrike_fit_drift:
        keyed = {k.upper(): k for k in list(data['t']) + list(data['m'])}
        for d in drift:
            key = keyed.get(d['ledger_key'].upper())
            if not key or (args.only and key not in args.only):
                continue
            if any(x['key'] == key for x in due):
                continue
            e = data['t'].get(key) or data['m'].get(key)
            ms = market_series(key, e)
            if not ms:
                continue
            published = (((e.get('asof') or {}).get('mc') or {}).get('data')) or ''
            due.append({'key': key, 'market': ms[0], 'series': ms[1],
                        'published': published, 'library': published,
                        'is_metal': key in METAL_MARKET, 'reason': 'fit drift'})
    print()

    if not due:
        print('Every page already stands on the current library — no cone and no '
              'technical read needs refreshing.')
        # [R-REC-01] But the per-name record is a function of the FIT, not of the
        # library, so this is precisely the run in which it can be stale while
        # nothing else is. Report it in a dry run; regenerate it under --write.
        if not args.write:
            print('\n--- per-name calibration record [R-REC-01] ---')
            fresh = rebuild_name_calibration(check_only=True)
            print('\nDRY RUN — nothing written.' if fresh else
                  '\nDRY RUN — nothing written. The record above is STALE; '
                  're-run with --write to regenerate it.')
            return 0
        print('\n--- per-name calibration record [R-REC-01] ---')
        ledger_before = json.dumps(data['l'], sort_keys=True)
        rebuild_name_calibration()
        after_data = read_data_js()
        after = counts(after_data)
        if after != before:
            raise SystemExit(f'entry count moved {before} -> {after} — aborting.')
        if json.dumps(after_data['l'], sort_keys=True) != ledger_before:
            raise SystemExit('LEDGER CHANGED while regenerating the per-name '
                             'record — it may only ever rewrite the CALIB block.')
        print(f'    counts unchanged: {after[0]} tickers, {after[1]} metals, '
              f'{after[2]} ledger rows')
        print('    LEDGER byte-identical — no cohort struck')
        return 0

    n_price = sum(1 for d in due if d.get('reason') != 'fit drift')
    n_fit = len(due) - n_price
    parts = ([f'{n_price} behind their library'] if n_price else []) + \
            ([f'{n_fit} on a superseded fit'] if n_fit else [])
    print(f'{len(due)} name(s) to act on — ' + ', '.join(parts) + ':\n')
    plan, refused, metals = [], [], []
    for d in due:
        q = q_override.get(d['key'], recover_q(data, d['key']))
        if d['is_metal']:
            metals.append(d)
            print(f"  SKIP-CONE {d['key']:12s} {d['published']} -> {d['library']}"
                  '  (metals run their own annual clock; technicals still refresh)')
            continue
        if q is None:
            refused.append(d)
            print(f"  REFUSE    {d['key']:12s} {d['published']} -> {d['library']}"
                  '  (no sourced q_annual — pass --q ' f"{d['key']}=VALUE)")
            continue
        d['q'] = q
        plan.append(d)
        why = '  [fit drift]' if d.get('reason') == 'fit drift' else ''
        print(f"  REFRESH   {d['key']:12s} {d['published']} -> {d['library']}"
              f"  q={q:.4f}{why}")

    print(f'\n{len(plan)} to refresh, {len(refused)} refused, '
          f'{len(metals)} metals cone-skipped')

    if not args.write:
        print('\nDRY RUN — nothing written. Re-run with --write to apply.')
        return 0

    ledger_before = json.dumps(data['l'], sort_keys=True)

    print('\n--- cone refresh (mid-cycle; no LEDGER rows) ---')
    for d in plan:
        print(f"  {d['key']}")
        refresh_cone_one.run(d['market'], d['series'], d['key'], today,
                             q_annual=d['q'], write=True)

    print('\n--- technical read + as-of stamps (all names, idempotent) ---')
    sh([sys.executable, 'apply_technicals.py', '--write'], cwd=ENGINE)

    print('\n--- chart SVGs, from the same library ---')
    sh([sys.executable, 'ta_chart.py', '--write'], cwd=ENGINE)

    # [R-REC-01] In the SAME pass, never a step someone remembers separately.
    print('\n--- per-name calibration record [R-REC-01] ---')
    rebuild_name_calibration()

    print('\n--- gates ---')
    after_data = read_data_js()
    after = counts(after_data)
    if after != before:
        raise SystemExit(f'entry count moved {before} -> {after} — aborting. '
                         'Counting against a known total is the only thing that '
                         'catches a silently dropped entry.')
    print(f'    counts unchanged: {after[0]} tickers, {after[1]} metals, '
          f'{after[2]} ledger rows')

    if json.dumps(after_data['l'], sort_keys=True) != ledger_before:
        raise SystemExit('LEDGER CHANGED during a mid-cycle refresh — no cohort '
                         'may be struck outside the monthly metronome.')
    print('    LEDGER byte-identical — no cohort struck')

    sh(['node', '--check', DATA_JS])
    if not args.skip_overlay:
        overlay_gate()
    sh([sys.executable, os.path.join(ROOT, 'scripts', 'check_data_freshness.py')])

    print(f'\nRefreshed {len(plan)} name(s). '
          f'{len(refused)} refused for an unsourced dividend yield.')
    if refused:
        print('Refused: ' + ' '.join(d['key'] for d in refused))
    return 0


if __name__ == '__main__':
    sys.exit(main())
