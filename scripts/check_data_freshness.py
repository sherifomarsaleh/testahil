#!/usr/bin/env python3
"""Freshness / provenance gate for assets/data.js.

WHY THIS EXISTS
---------------
On 29-Jul-2026 the computed technical read and the two-date as-of stamps were
adopted and fanned out to all 74 covered names (commit fcee684d, 08:44). Three
hours later a merge that reconciled a concurrent branch (c33b3ada, 11:27)
silently reverted 9 of those blocks to their pre-adoption state: the `asof`
stamp was dropped entirely and the hand-authored `levels`/`tech` came back.
The 9 were exactly the IN/US/KR names -- TMPV, RELIANCE, INFY, AAPL, NVDA,
TSLA, SAMSUNG, KAKAO, LGES.

Nothing caught it. That merge's own commit message records the verification it
did run -- "71 tickers before/after (none lost) ... COMI confirmed
byte-identical" -- which counted tickers and spot-checked a name the merge had
never touched. Counting the containers cannot see fields disappearing from
inside them, and a byte-compare against an untouched name cannot see a
regression in a touched one.

The rule was written down (Standing_Research_Protocol.md: "when the library
moves, the technical read moves with it, IN THE SAME PASS") but lived only as
prose. This script is that rule made executable.

The same pass also found:
  * PLATINUM stamped mc.computed "2012-01-05" -- apply_technicals.py scraped
    the first dd-Mon-yyyy out of the ledger note, and platinum's note opens
    with its calibration SAMPLE START ("origins 05-Jan-2012"). Fixed by
    reading an explicit run_date field instead of parsing prose (check 3).
  * GOLD publishing spot 4090.87 labelled "close 28 Jul 2026" when 4090.87 is
    the 27-Jul close and the library has no 28-Jul row at all (check 7).
  * QNB and PLATINUM still publishing retired session-counted resolve dates
    (2026-08-02 / 2026-09-27 and 2026-08-17 / 2026-10-12) against calendar
    horizons of 2026-08-05 / 2026-10-05 and 2026-08-20 / 2026-10-20 (check 5).

BOUNDARY: this is a static check of data.js against the raw libraries and
engine/horizons.py. It does not re-run the MC engine and cannot tell you a
cone is WRONG -- only that it is stale, unstamped, unsourced, or internally
inconsistent with the data it claims to stand on.

Exit 0 = clean, exit 1 = at least one FAIL.
"""
from __future__ import annotations

import os as _os, sys as _sys                                   # noqa: E402
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # noqa: E402
from coverage_floor import assert_examined                      # noqa: E402  [R-ENF-04]

import csv
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import horizons  # noqa: E402
import technicals as TA  # noqa: E402

DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
RAW = os.path.join(ROOT, 'engine', 'raw_ohlc')

# Kept in step with engine/apply_technicals.py -- if a market is added there
# it must be added here, or its names silently drop out of every check below.
EXCHANGE_MARKET = {'EGX': 'EG', 'ADX': 'AE', 'DFM': 'AE', 'TADAWUL': 'SA',
                   'KRX': 'KR', 'NASDAQ': 'US', 'NYSE': 'US',
                   'NSE': 'IN', 'BSE': 'IN', 'QSE': 'QA', 'QE': 'QA'}
SERIES_OVERRIDE = {'ALRAJHI': 'RAJHI', 'ADIBUAE': 'ADIB',
                   '2POINTZERO': 'TWOPOINTZERO'}
METAL_MARKET = {'GOLD': ('XAU', 'GOLD'), 'SILVER': ('XAU', 'SILVER'),
                'PLATINUM': ('XPT', 'PLATINUM')}
LEDGER_ALIAS = {'GOLD': 'Gold', 'SILVER': 'Silver', 'PLATINUM': 'Platinum',
                'SAMSUNG': 'Samsung', 'KAKAO': 'Kakao'}

MONTHS = {m: i + 1 for i, m in enumerate(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}
ISO = re.compile(r'^\d{4}-\d{2}-\d{2}$')
# t252 (metals, 12 months) rides its own annual clock and is NOT
# re-anchored by a mid-cycle spot refresh, so it is checked against its
# own LEDGER row rather than against the page's current spotDate.
HORIZON_MONTHS = {'t20': 1, 't60': 3}

fails: list[str] = []
warns: list[str] = []


def fail(name: str, msg: str) -> None:
    fails.append(f'{name}: {msg}')


def warn(name: str, msg: str) -> None:
    warns.append(f'{name}: {msg}')


# --------------------------------------------------------------- js scanning
def _match_brace(src: str, i: int) -> int:
    """Index just past the object that opens at src[i] == '{'."""
    depth, in_s, esc, in_c = 0, None, False, None
    while i < len(src):
        c = src[i]
        if in_c == '//':
            if c == '\n':
                in_c = None
        elif in_c == '/*':
            if c == '*' and src[i + 1:i + 2] == '/':
                in_c, i = None, i + 1
        elif in_s:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_s:
                in_s = None
        elif c in '"\'':
            in_s = c
        elif c == '/' and src[i + 1:i + 2] in ('/', '*'):
            in_c, i = '/' + src[i + 1], i + 1
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError('unbalanced braces')


def top_level_blocks(src: str, decl: str) -> dict[str, str]:
    """{key: block source} for one level inside a `const X = {` declaration."""
    i = src.index(decl) + len(decl) - 1
    end = _match_brace(src, i)
    body, out, k = src[i + 1:end - 1], {}, 0
    # keys may be quoted -- "2POINTZERO" MUST be, a JS identifier cannot
    # start with a digit, and an unquoted-only pattern silently drops it.
    pat = re.compile(r'\n\s*(?:"([A-Za-z0-9_]+)"|([A-Za-z_][A-Za-z0-9_]*))\s*:\s*\{')
    while True:
        m = pat.search(body, k)
        if not m:
            break
        s = m.end() - 1
        e = _match_brace(body, s)
        out[m.group(1) or m.group(2)] = body[s:e]
        k = e
    return out


def ledger_rows(src: str) -> list[dict]:
    i = src.index('const LEDGER = [')
    j = src.index('\n];', i)
    body, rows, k = src[i:j], [], 0
    starts = [m.start() for m in re.finditer(r'\n  \{', body)]
    for s in starts:
        s = body.index('{', s)
        e = _match_brace(body, s)
        rows.append(body[s:e])
        k = e

    def g(r, key):
        m = re.search(key + r'\s*:\s*("([^"]*)"|[-\d.]+|null)', r)
        if not m:
            return None
        return m.group(2) if m.group(2) is not None else m.group(1)

    return [{'raw': r, 'instrument': g(r, 'instrument'),
             'horizon': g(r, 'horizon_label'), 'anchor': g(r, 'anchor_date'),
             'grade': g(r, 'grade_date'), 'run': g(r, 'run_date'),
             'realized': g(r, 'realized_close'),
             # the STRIKE-TIME horizon record, for check 5b: what resolve()
             # returned on the day the cone was struck, and whether that session
             # count was a projection or a realized count.
             'horizon_days': g(r, 'horizon_days'),
             'grade_basis': g(r, 'grade_basis')}
            for r in rows if g(r, 'instrument')]


def _read_csv(market: str, series: str):
    """(rows, date_col, price_col). Real CSV parsing -- these exports quote
    comma-thousands ("4,090.87"), so a naive line.split(',') reads gold's
    close as 4.0 and LG Energy's 314,000 as 314."""
    path = os.path.join(RAW, market, series + '.csv')
    if not os.path.exists(path):
        return [], None, None
    with open(path, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return [], None, None
    hdr = [h.strip().strip('"').lower() for h in rows[0]]
    dcol = next((i for i, h in enumerate(hdr) if 'date' in h), None)
    pcol = next((i for i, h in enumerate(hdr)
                 if h in ('price', 'close', 'last', 'adj close')), None)
    return rows[1:], dcol, pcol


def _iso(cell: str):
    cell = cell.strip().strip('"')
    m = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', cell)
    if m:
        return f'{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}'
    return cell if ISO.match(cell) else None


def library_dates(market: str, series: str) -> list[str]:
    rows, dcol, _ = _read_csv(market, series)
    if dcol is None:
        return []
    return sorted(d for d in (_iso(r[dcol]) for r in rows if len(r) > dcol) if d)


def spot_on(market: str, series: str, iso: str):
    """(close, session_exists) -- used to prove a published spot is real."""
    rows, dcol, pcol = _read_csv(market, series)
    if dcol is None:
        return None, False
    for r in rows:
        if len(r) > dcol and _iso(r[dcol]) == iso:
            if pcol is None or len(r) <= pcol:
                return None, True
            try:
                return float(r[pcol].strip().strip('"').replace(',', '')), True
            except ValueError:
                return None, True
    return None, False


# -------------------------------------------------------------------- checks
def main() -> int:
    src = open(DATA_JS, encoding='utf-8').read()
    entries = {}
    for key, blk in top_level_blocks(src, 'const TICKERS = {').items():
        pre = re.search(r'code:\s*"([A-Z0-9]+):', blk)
        mkt = EXCHANGE_MARKET.get(pre.group(1)) if pre else None
        entries[key] = (blk, mkt, SERIES_OVERRIDE.get(key, key))
    for key, blk in top_level_blocks(src, 'const METALS = {').items():
        if key in METAL_MARKET:
            entries[key] = (blk, *METAL_MARKET[key])

    rows = ledger_rows(src)
    by_inst: dict[str, list[dict]] = {}
    for r in rows:
        by_inst.setdefault(r['instrument'], []).append(r)

    print(f'data.js: {len(entries)} published entries, {len(rows)} ledger rows, '
          f'{len(by_inst)} ledger instruments')

    # 1. every published name reaches a ledger instrument, and vice versa.
    #    Counting one side alone is what let 9 names rot unnoticed.
    mapped = {k: LEDGER_ALIAS.get(k, k) for k in entries}
    for k, inst in mapped.items():
        if inst not in by_inst:
            fail(k, f'published but no LEDGER instrument "{inst}"')
    for inst in by_inst:
        if inst not in set(mapped.values()):
            fail(inst, 'in LEDGER but not published in TICKERS/METALS')

    today = date.today().isoformat()

    for key, (blk, mkt, series) in sorted(entries.items()):
        if not mkt:
            fail(key, 'no market resolved from its code: prefix')
            continue
        lib = library_dates(mkt, series)
        if not lib:
            fail(key, f'no raw library at raw_ohlc/{mkt}/{series}.csv')
            continue
        last_session = lib[-1]

        # 2. the as-of stamp must be complete. This is the check that fires on
        #    a merge that drops the block -- the 29-Jul regression.
        a = re.search(r'asof:\s*\{(.*?)\n\s*\}', blk, re.S)
        if not a:
            fail(key, 'no asof stamp')
            continue
        got = dict(re.findall(r'(data|computed):\s*"([\d-]+)"', a.group(1)))
        pairs = re.findall(r'(mc|tech):\s*\{\s*data:\s*"([\d-]+)"\s*,\s*'
                           r'computed:\s*"([\d-]+)"\s*\}', a.group(1))
        stamp = {p[0]: (p[1], p[2]) for p in pairs}
        if set(stamp) != {'mc', 'tech'}:
            fail(key, f'asof incomplete -- has {sorted(stamp) or sorted(got)}')
            continue
        for kind, (d, c) in stamp.items():
            if not (ISO.match(d) and ISO.match(c)):
                fail(key, f'asof.{kind} not ISO: {d}/{c}')
            elif c < d:
                fail(key, f'asof.{kind}.computed {c} precedes its data {d} '
                          '-- impossible')
            elif c > today:
                fail(key, f'asof.{kind}.computed {c} is in the future')

        # 2b. WHERE THE ENTRY RECORDS ITS OWN STRIKE DATE, THE STAMP MUST AGREE.
        #     `fit.on` is written by rollforward_one.restrike_entry at the moment
        #     the cone is struck; asof.mc.computed is written later by
        #     apply_technicals. Before this check the latter was INFERRED from the
        #     newest LEDGER row's run_date, and a mid-cycle re-strike mints no
        #     ledger row -- so a re-strike that did not move the anchor was
        #     invisible and the page kept publishing the old compute date. On
        #     25-Aug-2026 all 21 re-struck cones were stale this way, by up to
        #     four weeks, and NOTHING failed: every other check here compares a
        #     stamp against the LIBRARY, and the library had not moved. This is
        #     the [R-ENF-01] move -- the rule checked from outside the tool that
        #     implements it, failing rather than warning.
        #
        #     An entry with no `fit` stamp yet is NOT failed: it predates the
        #     field and acquires one at its next strike. Silence there is the
        #     honest answer, not a pass.
        fo = re.search(r'fit:\s*\{[^{}]*?\bon:\s*"([\d-]+)"[^{}]*?\}', blk)
        if fo and 'mc' in stamp and fo.group(1) != stamp['mc'][1]:
            fail(key, f'asof.mc.computed {stamp["mc"][1]} disagrees with the '
                      f'strike date the entry itself records, fit.on '
                      f'{fo.group(1)} -- the cone was struck on a day the page '
                      'does not admit to')

        # 3. the technical read must stand on the CURRENT library. "When the
        #    library moves, the technical read moves with it, in the same pass."
        #    Compared against the CLEANED series (the same Step 0.0 gate the
        #    engine runs), not the raw tail: LCSW's raw file ends 2026-07-22
        #    but that row is a stale/no-trade print the gate drops, so 07-21
        #    is the correct read date and a raw comparison would cry wolf.
        try:
            clean_last = TA.compute(mkt, series, computed_on=today)['data_date']
        except Exception as e:                                    # noqa: BLE001
            fail(key, f'technicals.compute failed: {type(e).__name__}: {e}')
            clean_last = None
        if clean_last and stamp['tech'][0] != clean_last:
            fail(key, f'technical read is on {stamp["tech"][0]} but the '
                      f'cleaned library now ends {clean_last} -- re-run '
                      'apply_technicals.py + ta_chart.py')

        # 4. cone older than its own technical read: report, never reconcile
        #    silently inside a technicals pass.
        if stamp['mc'][0] < stamp['tech'][0]:
            warn(key, f'published cone is anchored {stamp["mc"][0]} while the '
                      f'technical read is on {stamp["tech"][0]} -- the cone is '
                      'stale relative to its own library')

        # 5. horizons are CALENDAR-ONLY. A retired session-counted resolve
        #    date is a protocol violation, not a rounding difference.
        sd = re.search(r'spotDate:\s*"close (\d{1,2}) (\w{3}) (\d{4})"', blk)
        if not sd:
            fail(key, 'spotDate not in the "close D Mon YYYY" form')
            continue
        anchor = (f'{sd.group(3)}-{MONTHS[sd.group(2)]:02d}-'
                  f'{int(sd.group(1)):02d}')
        for field, months in HORIZON_MONTHS.items():
            m = re.search(field + r':\s*\{[^}]*resolve:\s*"([\d-]+)"', blk)
            if not m:
                continue
            want = horizons.resolve(mkt, anchor, months)['grade_date']
            if m.group(1) != want:
                fail(key, f'{field} resolve {m.group(1)} != calendar '
                          f'{want} (anchor {anchor} + {months}m)')

        # 5b. the fan's session anchors must be this name's OWN projected
        #     spans. Six entries (IQCD/QNB/QGTS, gold, silver, platinum) shipped
        #     with no hz block at all and silently fell back to app.js's
        #     HZ_LEGACY {h1:20, h3:60, cal:false} -- so their published
        #     percentiles were pinned at 20/60 sessions when the real spans are
        #     22/63 and 23/66, and their axis and prose rendered the retired
        #     session naming. A missing hz is invisible on the page; it just
        #     draws the wrong cone.
        hz = re.search(r'hz:\s*\{([^}]*)\}', blk)
        if not hz:
            fail(key, 'no hz block -- falls back to the retired 20/60 session '
                      'grid in app.js and mislabels its own axis')
        else:
            body = hz.group(1)
            if 'cal:true' not in body.replace(' ', ''):
                fail(key, 'hz.cal is not true -- renders the retired session naming')
            #     A PUBLISHED SESSION COUNT IS A STRIKE-TIME PROJECTION, AND A
            #     PROJECTION THAT LATER RESOLVES ONE SESSION AWAY IS NOT A DEFECT
            #     (23-Aug-2026). This compared the published h against resolve()
            #     re-run TODAY, which is the same error the grading rule forbids one
            #     field over: "grade against the stored calendar grade_date ...
            #     never re-derive the target by counting rows." resolve() returns a
            #     PROJECTED h while the library is short of the target and a REALIZED
            #     h once it covers it, and markets share one realized calendar — so
            #     the moment ANY name's library runs ahead of its peers, every
            #     still-stale name in that market re-resolves onto the realized
            #     branch and fails a check about a number nobody got wrong.
            #
            #     That is not hypothetical: merging one month of ABUK extended EG's
            #     calendar to 2026-08-23, and 24 EG names struck 2026-07-22 with a
            #     projected h1 of 20 were suddenly measured against a realized 21.
            #     Every one of them had committed to the CORRECT grade date
            #     (2026-08-23) and every published percentile was untouched. It
            #     would fire the same way in any market, on any roll-forward.
            #
            #     So the published h is held to what was knowable AT STRIKE, whose
            #     durable record is the LEDGER row's own horizon_days/grade_basis.
            #     The guard is the GRADE DATE: a resolved projection is forgiven only
            #     while the commitment it was made for still resolves to the same
            #     date. If that moved, the entry is genuinely wrong and still fails.
            inst_l = LEDGER_ALIAS.get(key, key)
            for field, months, hlabel in (('h1', 1, '1 month'),
                                          ('h3', 3, '3 months')):
                m = re.search(field + r'\s*:\s*(\d+)', body)
                res = horizons.resolve(mkt, anchor, months)
                want = res['h']
                if not m:
                    fail(key, f'hz.{field} missing')
                    continue
                got_h = int(m.group(1))
                if got_h == want:
                    continue
                struck = next((r for r in by_inst.get(inst_l, [])
                               if r['horizon'] == hlabel and r['anchor'] == anchor),
                              None)
                if (struck and struck['grade_basis'] == 'projected'
                        and struck['horizon_days'] is not None
                        and int(float(struck['horizon_days'])) == got_h
                        and struck['grade'] == res['grade_date']):
                    warn(key, f'hz.{field} is {got_h}, the projection made at strike; '
                              f'the span has since resolved to {want} sessions. Grade '
                              f'date {struck["grade"]} is unchanged, so the commitment '
                              f'stands and the cone is not re-sized.')
                    continue
                #     THE SAME FORGIVENESS, FOR A ROW STRUCK BEFORE THE DURABLE
                #     RECORD EXISTED (01-Sep-2026). horizon_days/grade_basis are
                #     what the branch above reads to prove the published h was a
                #     projection, and rows struck before those fields were emitted
                #     carry neither -- so the branch could not fire for them and
                #     the check hard-FAILED on a number nobody got wrong. Real
                #     case: splicing one month of TSLA extended the US calendar to
                #     2026-09-01, and AAPL and NVDA -- struck 2026-07-27, h1=22,
                #     grade date 2026-08-27 -- were re-measured against a realized
                #     23. Identical in shape to the ABUK case above, blocked only
                #     by the age of the row.
                #
                #     THE GUARD IS UNCHANGED AND IS STILL THE GRADE DATE. This
                #     forgives only where the ledger row for that exact strike
                #     exists, its commitment still resolves to the same date, and
                #     the disagreement comes from resolve() having crossed to its
                #     REALIZED branch. A moved grade date, a missing row, or a
                #     durable record that disagrees all still FAIL.
                if (struck and struck['horizon_days'] is None
                        and struck['grade'] == res['grade_date']
                        and res['basis'] == 'realized'):
                    warn(key, f'hz.{field} is {got_h}, the projection made at strike; '
                              f'the span has since resolved to {want} sessions. This '
                              f'row predates the horizon_days/grade_basis record, so '
                              f'the grade date is the whole guard: {struck["grade"]} '
                              f'is unchanged, so the commitment stands and the cone '
                              f'is not re-sized.')
                    continue
                fail(key, f'hz.{field} is {got_h} but this name\'s own '
                          f'{months}-month span projects to {want} sessions')

        # 6. published spot must be a real close in the library on the date
        #    the page claims. Gold published the 27-Jul close as "28 Jul".
        sp = re.search(r'spot:\s*([\d.]+)', blk)
        close, found = spot_on(mkt, series, anchor)
        if not found:
            fail(key, f'spotDate claims {anchor} but the library has no such '
                      'session')
        elif sp and close is not None and close:
            # relative tolerance: pages round for display (RELIANCE shows
            # 1272 for a 1271.8 close). 0.1% catches a wrong DAY, not rounding.
            if abs(float(sp.group(1)) - close) / abs(close) > 0.001:
                fail(key, f'published spot {sp.group(1)} != library close '
                          f'{close} on {anchor}')

    # 6b. the chart CAPTION must name the same session the chart is drawn to.
    #     ta_chart regenerates the <svg>, but the caption lives in the
    #     <figcaption> outside it and is a separate substitution -- one that
    #     required the HTML entity "&middot;" while 8 pages use a literal
    #     U+00B7. On those the caption froze: phdc.html labelled a 22-Jul chart
    #     "last 500 sessions to 17 Jun 2026", 35 days out, and the page still
    #     reported success. check_ta_chart_overlay cannot see this -- it only
    #     tests that level lines land inside the viewBox.
    pages = [f for f in sorted(os.listdir(ROOT)) if f.endswith('.html')]
    key_re = re.compile(r'(?:TICKERS|METALS)(?:\.([A-Za-z_][A-Za-z0-9_]*)'
                        r'|\[["\']([A-Za-z0-9_]+)["\']\])')
    for f in pages:
        html = open(os.path.join(ROOT, f), encoding='utf-8',
                    errors='replace').read()
        cap = re.search(r'last 500 sessions to (\d{1,2}) (\w{3}) (\d{4})', html)
        if not cap:
            continue
        keys = {(a or b) for a, b in key_re.findall(html)} & set(entries)
        if len(keys) != 1:
            continue
        key = keys.pop()
        cap_iso = (f'{cap.group(3)}-{MONTHS[cap.group(2)]:02d}-'
                   f'{int(cap.group(1)):02d}')
        st = re.search(r'tech:\s*\{\s*data:"([\d-]+)"', entries[key][0])
        if st and cap_iso != st.group(1):
            fail(key, f'{f} chart caption says {cap_iso} but the chart and read '
                      f'are on {st.group(1)} -- re-run ta_chart.py')

    # 7. every ledger row: sourced run_date, calendar grade_date.
    for r in rows:
        tag = f'{r["instrument"]}/{r["horizon"]}@{r["anchor"]}'
        if not r['run'] or not ISO.match(r['run']):
            fail(tag, 'no sourced run_date -- the strike date must be a field, '
                      'never scraped out of the note prose')
        elif r['run'] < r['anchor']:
            fail(tag, f'run_date {r["run"]} precedes anchor {r["anchor"]}')
        months = {'1 month': 1, '3 months': 3, '12 months': 12}.get(r['horizon'])
        key = next((k for k, v in LEDGER_ALIAS.items()
                    if v == r['instrument']), r['instrument'])
        ent = entries.get(key)
        if months and ent and ent[1]:
            want = horizons.resolve(ent[1], r['anchor'], months)['grade_date']
            if r['grade'] == want:
                continue
            if r['realized'] not in (None, 'null'):
                # Already graded. Ledgers are append-only -- a published
                # forecast is never retro-edited -- and an unscheduled closure
                # legitimately moves the graded date, provided the row says so.
                if 'grade_note' not in r['raw']:
                    fail(tag, f'graded on {r["grade"]} instead of the calendar '
                              f'{want} with no grade_note explaining why')
            else:
                fail(tag, f'grade_date {r["grade"]} != calendar {want}')

    # 8. lifecycle invariant: exactly one open latest-anchor row per
    #    (instrument, horizon).
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault((r['instrument'], r['horizon']), []).append(r)
    for (inst, hz), v in sorted(groups.items()):
        openr = [x for x in v if x['realized'] in (None, 'null')]
        if not openr:
            continue
        latest = max(x['anchor'] for x in openr)
        n = sum(1 for x in openr if x['anchor'] == latest)
        if n != 1:
            fail(f'{inst}/{hz}', f'{n} open rows at the latest anchor {latest} '
                                 '-- lifecycle invariant is one')

    # 9. the calibration-backtest panel and its image must agree, BOTH ways.
    #    ledger.html renders that section only for instruments listed in its
    #    hand-maintained HAS_BACKTEST set, and builds the path from the LEDGER
    #    instrument key: assets/calibration_{key}.png. Two silent failures had
    #    already shipped by 04-Aug-2026 and neither was visible on the page --
    #    a missing section looks exactly like a section that was never meant
    #    to be there:
    #      * PLATINUM: image committed as calibration_Platinum.png while the
    #        instrument key is Platinum, and the key was never added to the set.
    #        The image was an orphan from the day it landed and the panel
    #        silently omitted the whole block.
    #      * ADIBUAE and LULU: images present and correctly named, keys simply
    #        never added -- two panels' backtests invisible for weeks.
    #    A listed key with no file is the mirror defect: a broken <img>.
    #    Counting one side alone cannot see either, which is the same lesson
    #    check 1 encodes for published-vs-ledger names.
    # Since the 30-Aug-2026 cutover, root ledger.html is a redirect stub and the
    # hand-maintained HAS_BACKTEST registry lives on the preserved page at
    # legacy/ledger.html (still served, still the page that renders the panel).
    # Root is preferred if it ever carries the set again.
    ledger_html = os.path.join(ROOT, 'ledger.html')
    _root_has_set = (os.path.exists(ledger_html)
                     and 'HAS_BACKTEST' in open(ledger_html, encoding='utf-8').read())
    if not _root_has_set and os.path.exists(os.path.join(ROOT, 'legacy', 'ledger.html')):
        ledger_html = os.path.join(ROOT, 'legacy', 'ledger.html')
    if os.path.exists(ledger_html):
        html = open(ledger_html, encoding='utf-8').read()
        m = re.search(r'const HAS_BACKTEST = new Set\(\[(.*?)\]\);', html, re.S)
        if not m:
            fail('ledger.html', 'no HAS_BACKTEST set found')
        else:
            listed = set(re.findall(r'"([^"]+)"', m.group(1)))
            have = {f[len('calibration_'):-len('.png')]
                    for f in os.listdir(os.path.join(ROOT, 'assets'))
                    if f.startswith('calibration_') and f.endswith('.png')}
            for k in sorted(listed - have):
                fail(f'HAS_BACKTEST/{k}', 'listed but assets/calibration_'
                                         f'{k}.png does not exist -- broken image')
            for k in sorted(have - listed):
                fail(f'HAS_BACKTEST/{k}', f'assets/calibration_{k}.png exists but '
                                          'the key is not in HAS_BACKTEST -- the '
                                          'panel silently omits its backtest')

    # 9. every published equity/metal reaches assets/markets.js, so the ledger can
    #    put it in a MARKET tab group. [ADDED 05-Aug-2026]
    #    Why: the ELEC publish placed engine/raw_ohlc/EG/ELEC.csv and regenerated
    #    the sitemap, the feed and the footer strip, but NOT the registry -- so
    #    MARKET_OF['ELEC'] was undefined, marketOf() returned null, and ledger.html
    #    rendered ELEC OUTSIDE the "EGX -- Egypt" group. Nothing threw; the markup
    #    was well-formed; only a DOM read of the rendered tab groups showed it.
    #    That is exactly the failure the registry itself was introduced to close
    #    (29-Jul-2026: 34 international names rendered under the EGX heading), so
    #    the rebuild is checked here rather than trusted to a checklist.
    #    Compare on the LEDGER INSTRUMENT name, not the data.js key: ledger.html
    #    calls marketOf() with the instrument ("Gold", "Samsung", "Platinum"), which
    #    is what build_market_registry.py keys on. Comparing TICKERS keys instead
    #    reports five phantom failures on exactly those differently-cased names.
    markets_js = os.path.join(ROOT, 'assets', 'markets.js')
    if not os.path.exists(markets_js):
        fail('assets/markets.js', 'missing -- run scripts/build_market_registry.py --write')
    else:
        reg = set(re.findall(r'"([^"]+)"\s*:\s*"[A-Z]{2,3}"',
                             open(markets_js, encoding='utf-8').read()))
        for inst in sorted(set(by_inst) - reg):
            fail(f'markets.js/{inst}', 'on the ledger but absent from the market '
                                       'registry -- it renders OUTSIDE its exchange '
                                       'tab group (run scripts/build_market_registry.py '
                                       '--write after placing the OHLC file)')

    for w in warns:
        print(f'WARN  {w}')
    for f in fails:
        print(f'FAIL  {f}')
    # [R-ENF-04] A gate must never report clean having examined nothing.
    pop = assert_examined(len(entries), 'check_data_freshness')
    print(f'\n{len(entries)} entries checked against {pop} libraries -- '
          f'{len(fails)} failure(s), {len(warns)} warning(s)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
