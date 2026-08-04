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
LEDGER_ALIAS = {'GOLD': 'Gold', 'SILVER': 'Silver', 'PLATINUM': 'XPTUSD',
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
             'realized': g(r, 'realized_close')}
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
            for field, months in (('h1', 1), ('h3', 3)):
                m = re.search(field + r'\s*:\s*(\d+)', body)
                want = horizons.resolve(mkt, anchor, months)['h']
                if not m:
                    fail(key, f'hz.{field} missing')
                elif int(m.group(1)) != want:
                    fail(key, f'hz.{field} is {m.group(1)} but this name\'s own '
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
    #        instrument key is XPTUSD, and the key was never added to the set.
    #        The image was an orphan from the day it landed and the panel
    #        silently omitted the whole block.
    #      * ADIBUAE and LULU: images present and correctly named, keys simply
    #        never added -- two panels' backtests invisible for weeks.
    #    A listed key with no file is the mirror defect: a broken <img>.
    #    Counting one side alone cannot see either, which is the same lesson
    #    check 1 encodes for published-vs-ledger names.
    ledger_html = os.path.join(ROOT, 'ledger.html')
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

    for w in warns:
        print(f'WARN  {w}')
    for f in fails:
        print(f'FAIL  {f}')
    print(f'\n{len(entries)} entries checked -- '
          f'{len(fails)} failure(s), {len(warns)} warning(s)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
