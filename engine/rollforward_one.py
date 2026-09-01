"""rollforward_one.py — roll ONE covered name forward, end to end.

apply_rollforward.py is the record of the 28-Jul-2026 market-wide re-strike: its
header comment and per-row note are hardcoded to that pass, so re-running it for
a single name would stamp today's cohort with last week's story. This module is
the general single-name tool, reusing that file's parsing and emitting helpers
rather than reimplementing them.

It runs the ACTUAL production chain via strike_cohorts.strike() — Step 0.0 gate
-> YZ variance proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50,000 paths, seed 42, signal per the profile — never an
approximation.

Rewrites ONLY spot / spotDate / dist / hz / touch on the ticker entry and
appends one LEDGER row per horizon. Touch probabilities are recomputed at the
SAME absolute levels already on the page, never re-picked. fair{}, the slider's
factor-stack constants and files are untouched. `levels`/`tech`/`asof` are left
to apply_technicals.py, which should be run after this.

Open cohorts on earlier cycles are NOT touched: they stay open and grade on
their own terms. Append-only, always.

Run:  python3 rollforward_one.py AE TWOPOINTZERO 2POINTZERO
      python3 rollforward_one.py AE TWOPOINTZERO 2POINTZERO --write
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import datetime as _dt
import pandas as pd                                        # noqa: E402

from strike_cohorts import strike, touch_probs, rel_touch   # noqa: E402
import market_profiles as MP                                # noqa: E402
import adaptive_width as AW                                # noqa: E402
from apply_rollforward import (ticker_blocks, fmt_price, fmt_spot,  # noqa: E402
                               prior_anchor, js_row,
                               bump_site_updated, MONTHS, RF_SRC)
from apply_technicals import (LEDGER_ALIAS,               # noqa: E402
                              top_level_blocks, match_brace)

# Market codes whose covered names are not equities. asset_class was hardcoded
# 'equity' below, so a metals roll-forward mislabelled its own ledger rows.
METAL_MARKETS = {'XAU', 'XPT'}


def name_calibration(market: str, series: str, profile, wmult: float = 1.0):
    """(cal flag, prose) for the name being struck — DERIVED, never typed.

    Publish_Protocol.md fixes the semantics: the row's `cal` field is set ONLY for
    matches / untested / fail, and ABSENT MEANS PASS. Until now only first-publish
    rows carried it, so once a covered name's own verdict turned FAIL every later
    roll-forward emitted a row asserting PASS by omission. That is the silence
    R-CAL-01 exists to prevent, arriving through the one surface a reader actually
    sees. Real case: CLHO turned FAIL on 24-Aug-2026 when its panel was rebuilt
    under the committed tilt, three cycles after it was published as PARITY.

    PARITY and BOUNDARY(PARITY-flagged) deliberately return no flag — level with
    the benchmark is the unremarkable case, 30 of EG's 37 names sit there, and
    labelling them all would be noise rather than disclosure. Only a verdict that
    contradicts the absent-means-PASS default is announced.

    The name being rolled forward always has a FRESH panel: its raw CSV changed,
    so panel_refresh rebuilt it and its market was refit in the same pass. Other
    names' registry records may lag; none is read here.
    """
    try:
        rec = json.load(open(os.path.join(HERE, 'fitted_configs.json'),
                             encoding='utf-8'))[market]['per_name'][series]
    except (OSError, ValueError, KeyError):
        return None, ''
    verdict = str(rec.get('verdict', ''))
    head = verdict.split('(')[0].strip().upper()
    if head == 'PROVISIONAL':
        return 'untested', (f' NAME-LEVEL CALIBRATION: {verdict} — this name has too few '
                            f'resolved windows for the robust bar to be evaluated at all, '
                            f'so its cone is published untested at the name level.')
    if head != 'FAIL':
        return None, ''

    from panel_refresh import panel_path, apply_breaks                   # noqa: E402
    sc = apply_breaks(pd.read_csv(panel_path(market, series, '3m')), profile)
    cov90, cov50 = 100 * sc['in90'].mean(), 100 * sc['in50'].mean()
    pit = float(sc['pit'].mean())
    wr = float((sc['w90'] / sc['w90_b']).mean())
    ci = rec.get('ci_block2') or [float('nan'), float('nan')]
    if abs(pit - 0.5) > 0.05:
        shape = (f'The cone is MIS-CENTRED: PIT mean {pit:.3f} where 0.5 is centred, '
                 f'with {cov90:.0f}% coverage against a 90% target and {cov50:.0f}% '
                 f'against 50%')
    elif cov90 >= 90:
        shape = (f'The cone is TOO WIDE, not mis-centred: {cov90:.0f}% coverage against '
                 f'a 90% target and {cov50:.0f}% against 50%, PIT mean {pit:.3f} where '
                 f'0.5 is centred, width {wr:.2f}x the carry-anchored benchmark')
    else:
        shape = (f'The cone is TOO NARROW: only {cov90:.0f}% coverage against a 90% '
                 f'target and {cov50:.0f}% against 50%, PIT mean {pit:.3f}')
    over = ''
    if abs(wmult - 1.0) > 1e-9:
        over = (f' The verdict is measured on the POOLED width; the cone published here '
                f'is narrower than the one scored, at the overlay\u2019s effective width.')
    return 'fail', (f' NAME-LEVEL CALIBRATION: FAIL, robustly — skill '
                    f'{rec.get("skill"):+.4f} over {len(sc)} scored windows, negative '
                    f'under every bootstrap block size {{2,3,4}} (block-2 CI '
                    f'[{ci[0]:+.3f},{ci[1]:+.3f}]). {shape}. Read the bands as an OUTER '
                    f'bound.{over}')


def _ledger_rows(src: str, instrument: str):
    """Every LEDGER row for `instrument`, each as its own brace-matched object text.

    VERIFY BY PARSING THE ROW, NOT BY GUESSING ITS LENGTH. This replaced
    `re.finditer(r'instrument:"X"(.{0,900})')`, which read a FIXED 900-character
    window after each hit. re.finditer returns NON-OVERLAPPING matches, so once a
    row grew past 900 characters its window ran on into the NEXT row and consumed
    that row's own `instrument:` marker — the scanner then stepped straight over
    it and never looked at it at all.

    A row crosses 900 characters exactly when it is GRADED: grading appends the
    realized fields to a row that already carries a long note. So the rows this
    silently skipped were the graded ones — which is precisely the set
    _prior_1m_matured exists to find. Measured on the 01-Sep-2026 GOLD strike:
    four Gold rows in the ledger, three inspected, and the one skipped was the
    cycle-2 1-month graded minutes earlier in the same pass. The note therefore
    published "off the monthly metronome — the prior cycle's 1-month has not yet
    matured" over a cohort that had matured on 2026-08-27 and been graded that
    morning, into an append-only record that is never retro-edited.

    This is the third appearance of one defect — a pattern standing in for a
    parser, dropping whichever entries happen to be shaped differently (the
    unquoted-key regex that dropped 2POINTZERO; the indentation-keyed `dist` span
    that deleted three fields on nine entries). Per [R-ENF-01] the class is closed
    here rather than the instance: rows are delimited by matching their braces, so
    a row of any length is read whole or not at all.
    """
    i = src.find('const LEDGER')
    if i < 0:
        return
    led = src[i:src.find('\n];', i)]
    needle = f'instrument:"{instrument}"'
    j = 0
    while True:
        k = led.find(needle, j)
        if k < 0:
            return
        o = led.rfind('{', 0, k)          # the row object this marker sits in
        if o < 0:
            return
        end = match_brace(led, o)
        yield led[o:end]
        j = max(end, k + len(needle))     # never re-scan inside a row already read


def ledger_instrument(key: str) -> str:
    """The LEDGER's name for a site key -- NOT always the site key itself.

    Platinum publishes under TICKERS.PLATINUM but grades under
    instrument:"Platinum"; gold/silver/Samsung/Kakao differ in case. This tool
    used `key` directly for the ledger row AND for both history lookups
    (prior_anchor, _prior_1m_matured), so on any aliased name it would write an
    orphan instrument, find no prior cycle, set reanchor_from=null, and publish
    a note asserting the prior 1-month had NOT matured -- the exact "stamps
    today's cohort with last week's story" defect this module's own docstring
    says apply_rollforward.py has. A tool written to fix that bug must not carry
    it. The map already existed in apply_technicals and metal_backtest; it is
    imported here rather than copied a third time.
    """
    return LEDGER_ALIAS.get(key, key)

DATA_JS = os.path.join(ROOT, 'assets', 'data.js')


def insert_rows(src: str, rows, header: str) -> str:
    """Append LEDGER rows under their own dated header. Never reorders.

    The separator matters: the array's last element ends with a bare `}` and no
    trailing comma, so an insertion that leads with a comment produces
    `}  /* comment */  {` — valid-looking text, invalid JavaScript. Emit the
    comma explicitly when the preceding element needs one. This is the stitch
    point an assert-guarded string replacement cannot see; only `node --check`
    catches it, which is why that check is mandatory here.
    """
    i = src.find('const LEDGER')
    j = src.find('\n];', i)
    sep = ',' if src[:j].rstrip().endswith('}') else ''
    body = ',\n'.join(js_row(r) for r in rows)
    return src[:j] + sep + header + body + src[j:]


def entry_blocks(src: str):
    """{key: (start, end)} across BOTH published objects, TICKERS and METALS.

    Metals are covered names with ledger cohorts, but they do not live in
    TICKERS — gold, silver and platinum are entries of `const METALS = {...}`,
    written in the compact one-space style and carrying a t252 twelve-month
    cone that no ticker entry has. ticker_blocks() used to sweep past the end
    of TICKERS and return them anyway, which is how this tool came to locate
    PLATINUM at all; with that scan correctly bounded it would find nothing.
    Both objects are enumerated here, explicitly, so a metals roll-forward is
    a supported path rather than an accident of an over-broad regex.
    """
    out = dict(top_level_blocks(src, 'const TICKERS = {'))
    for k, v in top_level_blocks(src, 'const METALS = {').items():
        out[k] = v
    return out


def _span_of_key(blk: str, key: str):
    """(start, end) of `\\n    {key}: {...},` by BRACE MATCHING, not indentation.

    The pattern this replaces — `\\n    dist: \\{.*?\\n    \\},` — closed on the
    first 4-space-indented `},` it could find. Nine entries (RELIANCE, IQCD,
    SAMSUNG, KAKAO, LGES, TMPV, QGTS, AAPL, TSLA — the IN/US/KR/QA cluster)
    close their dist block at TWO spaces, so on those the non-greedy match ran
    past dist and stopped at the `tech` block's closer instead, and a
    roll-forward silently DELETED touch, levels and tech from the entry. It
    left valid JavaScript and a page that still rendered, which is why nothing
    caught it: the levels and narrative simply vanished. Same family of defect
    as the unquoted-key regex that dropped 2POINTZERO from the 28-Jul pass —
    a hand-rolled pattern standing in for a parser.
    """
    # ANY indent, not four spaces. TICKERS writes fields at four, METALS at
    # one; hardcoding four raised 'no dist block on this entry' on every
    # metal. The brace-matched span below already made the CLOSER robust —
    # leaving the OPENER indent-sensitive left the layout still deciding
    # whether a field gets refreshed, which is the rule this file records.
    m = re.search(r'\n[ \t]*' + key + r':\s*\{', blk)
    if not m:
        return None
    i = blk.index('{', m.start())
    depth, in_s, esc = 0, None, False
    while i < len(blk):
        c = blk[i]
        if in_s:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == in_s:
                in_s = None
        elif c in '"\'':
            in_s = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                if blk[end:end + 1] == ',':
                    end += 1
                return m.start(), end
        i += 1
    raise ValueError(f'unbalanced braces in {key}')


def _touch_ladder(blk: str):
    """(span, levels, comment) for the entry's `touch: [...]` array.

    `apply_rollforward.parse_touch_levels` requires the MULTI-LINE form
    (`\\n    touch: [` ... `\\n    ]`) and returns None for the single-line one.
    19 of the 71 entries — RELIANCE, IQCD, RAYA, JUFO, EGAL, BTFH, ETEL, FWRY,
    ABUK, ADIB, HRHO, ORWE, SAMSUNG, KAKAO, LGES, TMPV, QGTS, AAPL, TSLA —
    write it on one line, so a roll-forward on any of them moved spot and the
    cone while leaving the touch table exactly as it was: a stale probability
    ladder sitting under a fresh forecast, with nothing to show it had not been
    recomputed. Bracket-matched here so the layout stops deciding whether the
    numbers get refreshed. The ladder is rewritten in the canonical multi-line
    form; the LEVELS themselves are never re-picked (STEP 5 — comparability
    across cycles beats re-centring on the new spot).
    """
    m = re.search(r'\n[ \t]*touch:\s*\[', blk)
    if not m:
        return None, None, None
    i = blk.index('[', m.start())
    depth = 0
    for j in range(i, len(blk)):
        if blk[j] == '[':
            depth += 1
        elif blk[j] == ']':
            depth -= 1
            if depth == 0:
                inner = blk[i + 1:j]
                lv = [float(x) for x in re.findall(r'\[\s*(-?[\d.]+)\s*,', inner)]
                c = re.search(r'/\*.*?\*/', inner, re.S)
                return (m.start(), j + 1), lv, (c.group(0) if c else
                                                '/* descending high -> low */')
    raise ValueError('unbalanced brackets in touch')


def _nice(v) -> str:
    """Shortest exact-enough literal for the fit stamp (0.965, 1, 4.5)."""
    f = float(v)
    return str(int(f)) if f == int(f) else f'{f:.6g}'


def restrike_entry(blk: str, r: dict, verbose: bool = True,
                   run_date: str = None) -> str:
    """Rewrite ONLY spot / spotDate / dist+hz / touch on one TICKERS entry.

    Shared by the monthly roll-forward below and by the mid-cycle cone refresh
    (refresh_cone_one.py) — STEP 0 decision (a) of the Roll-Forward & Grading
    Protocol, under which a data arrival that is not the current 1M's maturity
    refreshes the displayed cone and nothing else. Kept in ONE place so the two
    paths cannot drift into publishing differently-shaped cones; the difference
    between them is whether a LEDGER row is struck, never how the entry is written.

    fair{}, the slider's factor-stack constants, levels/tech/asof and files are
    untouched here by construction.
    """
    spot = r['spot']
    anchor = pd.Timestamp(r['anchor_date'])
    sd = f'close {anchor.day:02d} {MONTHS[anchor.month - 1]} {anchor.year}'
    h1, h3 = r['horizons']['1M'], r['horizons']['3M']

    new = blk
    # Rewrite at WHATEVER indent and spacing the field was found on, rather than
    # assuming the TICKERS layout. METALS writes `\n spot:1608.37,` — no space
    # after the colon and one space of indent — so the four-space patterns below
    # matched nothing and a metals roll-forward silently left spot and spotDate
    # at their old values while moving the cone. Failing to match must not be
    # silent either: both fields are asserted to have been rewritten.
    # Matched on a FIELD BOUNDARY, not a line start: METALS packs several fields
    # onto one line (`name:"Platinum", code:"XPT/USD", spot:1608.37, ...`), so a
    # \n-anchored pattern finds neither. The lookbehind stops `spot:` matching
    # inside a longer identifier, and requiring the colon immediately after keeps
    # it off `spotDate:`. Spacing after the colon is captured and replayed so the
    # entry keeps its own house style.
    new, n1 = re.subn(r'(?<![\w.$])spot:([ \t]*)[\d.,]+,',
                      lambda m: f'spot:{m.group(1)}{fmt_spot(spot)},',
                      new, count=1)
    new, n2 = re.subn(r'(?<![\w.$])spotDate:([ \t]*)"[^"]*",',
                      lambda m: f'spotDate:{m.group(1)}"{sd}",', new, count=1)
    if not (n1 and n2):
        raise ValueError(f'spot/spotDate not rewritten (spot={n1}, spotDate={n2})')

    span = _span_of_key(new, 'dist')
    if not span:
        raise ValueError('no dist block on this entry')
    s0, e0 = span
    ind = re.match(r'\n([ \t]*)', new[s0:]).group(1)

    # HORIZONS THIS TOOL DOES NOT STRIKE MUST SURVIVE IT. The metals pages carry a
    # t252 twelve-month cone on its own annual clock (STEP 0 decision (b) of the
    # Roll-Forward & Grading Protocol: one open 12M per metal, graded at maturity
    # then re-struck, never part of the monthly strike). This function rebuilt the
    # dist object from t20 + t60 alone, so running it on a metal would have DELETED
    # that cone from the page — silently, leaving valid JavaScript and a page that
    # still renders, which is exactly how the nine-entry `dist` defect of
    # 03-Aug-2026 went unnoticed. Any key other than t20/t60 is carried through
    # verbatim; only the two horizons actually re-simulated here are rewritten.
    old_dist = new[s0:e0]
    carried = [ln for ln in old_dist.splitlines()
               if re.match(r'\s*t(?!20\b|60\b)\w+\s*:', ln)]

    def row(tag, h, pad):
        p, f = h['pct'], lambda v: fmt_price(v, spot)      # noqa: E731
        return (f'{ind}  {tag}: {{ label:"{h["label"]}",{pad}'
                f'p5:{f(p["p5"])}, p25:{f(p["p25"])}, p50:{f(p["p50"])}, '
                f'p75:{f(p["p75"])}, p95:{f(p["p95"])}, '
                f'resolve:"{h["grade_date"]}" }}')
    lines = [row('t20', h1, '   '), row('t60', h3, '  ')]
    for ln in carried:
        lines.append(f'{ind}  ' + ln.strip().rstrip(','))
        if verbose:
            print(f'  carried through untouched: {ln.strip()[:40]}...')
    # THE EFFECTIVE FIT THIS CONE WAS BUILT ON, stamped on the entry itself.
    # Without it the only record of the fit behind a published cone was the
    # newest LEDGER note, and that is not the same thing twice over: the note
    # carries the POOLED width_cal and never the per-name overlay multiplier
    # ([R-WIDTH-01] — the pooled figure is not the width the cone was built on),
    # and a mid-cycle refresh writes NO ledger row at all, so the newest note can
    # describe a strike the page no longer shows. Measured 25-Aug-2026 across the
    # book, reading the note MISSED 4 drifted cones and FALSE-ALARMED on 1.
    # `eff` is what actually scaled the cone: width_cal * overlay multiplier.
    #
    # `on` IS THE DAY THIS STRIKE RAN, and it exists because nothing else records
    # it. apply_technicals stamps asof.mc.computed by reading the newest LEDGER
    # row's run_date, and a mid-cycle re-strike mints no LEDGER row — so a
    # re-strike that does NOT move the anchor is invisible to every existing
    # signal and the page keeps publishing the OLD compute date under a cone
    # computed today. Measured 25-Aug-2026: all 21 re-struck cones claimed
    # compute dates from 27-Jul to 17-Aug, up to four weeks stale, and every one
    # matched its ledger row's run_date exactly. The mid-cycle branch in
    # apply_technicals only fires when the ANCHOR moved, which is precisely what
    # a fit-drift re-strike does not do. Recorded here, where it is known,
    # rather than inferred downstream from a proxy that cannot see it.
    _cal = float(r['width_cal']); _mult = float(r['width_overlay_mult'])
    _on = run_date or _dt.date.today().isoformat()
    fit = (f'{ind}fit: {{ nu:{_nice(r["nu"])}, cal:{_nice(_cal)}, '
           f'mult:{_nice(_mult)}, eff:{_nice(_cal * _mult)}, on:"{_on}" }},')
    dist = (f'{ind}dist: {{\n' + ',\n'.join(lines) + f'\n{ind}}},\n'
            + f'{ind}hz: {{ h1:{h1["h"]}, h3:{h3["h"]}, '
              f'l1:"{h1["label"]}", l3:"{h3["label"]}", cal:true }},\n'
            + fit)
    # `dist` and `hz` are emitted as one unit, so hz must be the field that
    # immediately follows. That holds on all 71 ticker entries; if a future
    # entry breaks it, say so rather than silently leaving a stale hz behind
    # the fresh cone — a wrong hz draws the wrong fan with no visible tell.
    hz_span = _span_of_key(new, 'hz')
    if not hz_span or new[e0:hz_span[0]].strip() != '':
        raise ValueError('hz does not immediately follow dist on this entry')
    # dist + hz + fit are emitted as ONE unit, so an existing `fit` stamp
    # immediately after hz is CONSUMED rather than left behind — otherwise a
    # second strike would append a duplicate key, and a JS object literal takes
    # the LAST one while every regex-based tool reads the FIRST ([R-ENF-03]).
    tail = hz_span[1]
    fit_span = _span_of_key(new, 'fit')
    if fit_span and new[hz_span[1]:fit_span[0]].strip() == '':
        tail = fit_span[1]
    new = new[:s0] + '\n' + dist.lstrip('\n') + new[tail:]

    span, levels, comment = _touch_ladder(new)
    if levels:
        t1 = touch_probs(h1['_paths'], spot, levels)
        t3 = touch_probs(h3['_paths'], spot, levels)
        cells = ', '.join(f'[{fmt_price(lv, spot)}, {t1[float(lv)]}, {t3[float(lv)]}]'
                          for lv in levels)
        ti = re.match(r'\n([ \t]*)', new[span[0]:]).group(1)
        new = (new[:span[0]] + f'\n{ti}touch: [ {comment}\n{ti}  {cells}\n{ti}]'
               + new[span[1]:])
        if verbose:
            print(f'  touch recomputed at the SAME {len(levels)} absolute '
                  f'levels: {levels}')
    elif verbose:
        print('  NO touch ladder on this entry — nothing to recompute')
    return new


def _prior_1m_matured(src: str, instrument: str, prior_cycle, as_of: str,
                      anchor_date: str = None):
    """The prior cycle's 1-month grade date and whether it is yet GRADABLE.

    Returns (grade_date, gradable) when this strike lands on the monthly metronome —
    STEP 0 rule 2, "the 1-month maturity is the metronome" — and (None, False) when
    it does not. Read off the ledger rather than assumed, because the note that
    quotes it is published and a wrong claim there is invisible to every other check.

    MATURITY IS MEASURED AGAINST TODAY, NOT AGAINST THE ANCHOR (24-Aug-2026). The
    horizon is a CALENDAR COMMITMENT — `horizons.resolve()` sets a date and the row
    is graded ON it regardless of how many sessions the window held. This function
    compared the grade date against the strike's ANCHOR instead, which is the last
    SESSION in the library, so a cohort whose calendar grade date had arrived read
    as un-matured whenever the library ran even one session short of it. On the
    24-Aug-2026 DEWA strike that published exactly the wrong claim: the cycle-2
    1-month came due 2026-08-24, the strike ran on 2026-08-24, and the note said
    "off the monthly metronome — the prior cycle's 1-month has not yet matured".
    Two different facts had been collapsed into one test.

    So they are now two returns. MATURED is a calendar fact (grade_date <= today).
    GRADABLE is a data fact (the library reaches that date, i.e. grade_date <=
    anchor_date, the last session held). A cohort can be the first without being
    the second, and that third state — matured, waiting on its close — is real and
    is what the note must say instead of denying the maturity.
    """
    if prior_cycle is None:
        return None, False
    for e in _ledger_rows(src, instrument):
        cy = re.search(r'cycle_no:(\d+)', e)
        hl = re.search(r'horizon_label:"([^"]+)"', e)
        gd = re.search(r'grade_date:"([^"]+)"', e)
        if cy and hl and gd and int(cy.group(1)) == prior_cycle \
                and hl.group(1) == '1 month' and gd.group(1) <= as_of:
            gradable = anchor_date is None or gd.group(1) <= anchor_date
            return gd.group(1), gradable
    return None, False


def report_strike(key: str, market: str, series: str, r: dict) -> None:
    print(f'{key} ({market}/{series})')
    print(f'  anchor {r["anchor_date"]} @ {r["spot"]}  ({r["rows_out"]} clean rows)')
    for tag in ('1M', '3M'):
        h = r['horizons'][tag]
        print(f'  {tag}: {h["label"]:9s} h={h["h"]:3d} grade {h["grade_date"]} '
              f'p5..p95 ' + ' '.join(f'{h["pct"][q]:.2f}'
                                     for q in ('p5', 'p25', 'p50', 'p75', 'p95')))


def run(market: str, series: str, key: str, today: str,
        q_annual: float = 0.0, write: bool = False):
    src = open(DATA_JS, encoding='utf-8').read()
    blocks = entry_blocks(src)
    if key not in blocks:
        raise SystemExit(f'{key} not found in TICKERS or METALS')
    a, b = blocks[key]
    blk = src[a:b]

    r = strike(market, series, q_annual=q_annual)
    prof = MP.PROFILES[market]
    spot = r['spot']
    anchor = pd.Timestamp(r['anchor_date'])
    h1, h3 = r['horizons']['1M'], r['horizons']['3M']
    ccy = (re.search(r'ccy:\s*"([^"]+)"', blk) or [None, '?'])[1]
    inst = ledger_instrument(key)
    aclass = 'metal' if market in METAL_MARKETS else 'equity'
    prior = prior_anchor(src, inst)
    cyc = prior[1] + 1 if prior else 2

    report_strike(key, market, series, r)
    print(f'  prior cycle {prior} -> new cycle {cyc}')

    # ---- ticker entry: spot / spotDate / dist+hz / touch, nothing else
    new = restrike_entry(blk, r, run_date=pd.Timestamp(
        today.replace('-', ' ')).date().isoformat())

    d = anchor
    # EVERY CLAUSE BELOW IS DERIVED. The retired text hardcoded two claims about a
    # specific historical pass — "this name was NOT in the 28-Jul-2026 market-wide
    # EG/AE/SA re-strike" and "this cohort also brings the name onto the calendar
    # 1M/3M convention it had never been migrated to". Both were true only of the
    # 29-Jul gap-closing cohort this tool was first written for. On the 05-Aug-2026
    # QNB strike the first was true by luck and the second was flatly FALSE (QNB's
    # cycle 1 was already calendar-native — its grade dates were recomputed by
    # horizons.resolve on 29-Jul). That is precisely the defect this module's own
    # docstring says apply_rollforward.py has: re-running it for one name "stamps
    # today's cohort with last week's story". A tool written to fix that bug must
    # not carry it. Whether this strike sits on the monthly metronome is now READ
    # from the ledger, not assumed.
    # THREE STATES, NOT TWO. Maturity is a calendar fact and gradability is a data
    # fact; see _prior_1m_matured. Collapsing them denied a maturity that had in
    # fact arrived whenever the library ran short of the grade date.
    # Same expression the row's own run_date is built from, so the maturity test and
    # the stamp on the row can never disagree about what "today" is.
    as_of = pd.Timestamp(today.replace('-', ' ')).date().isoformat()
    metro, gradable = _prior_1m_matured(src, inst, prior[1] if prior else None,
                                        as_of, r['anchor_date'])
    if metro and gradable:
        event = ('at the monthly metronome — the prior cycle’s 1-month matured on '
                 f'{metro} and is graded in this same pass')
    elif metro:
        event = ('at the monthly metronome — the prior cycle’s 1-month matured on '
                 f'{metro}, but this name’s library ends {r["anchor_date"]}, so that '
                 'cohort is not gradable yet: it stays OPEN and is graded on its own '
                 'date once its close lands')
    else:
        event = ('off the monthly metronome — the prior cycle’s 1-month has not yet '
                 'matured, so no cohort of that horizon is graded here')
    # The q_annual disclosure is CLASS-DEPENDENT. The retired text asserted a
    # gross-of-dividend overstatement unconditionally. On a zero-yield spot metal
    # that is not a flag on a defaulted input -- it is the sourced value -- and the
    # sentence was simply false.
    qnote = ('(q=0 is SOURCED, not defaulted: a spot metal pays no holder yield '
             '\u2014 the lease rate is a borrower\u2019s cost, not a return to the '
             'holder \u2014 so the carry is rf alone.)'
             if aclass == 'metal' and q_annual == 0 else
             '(FLAGGED \u2014 house convention; the drift is a GROSS-OF-DIVIDEND '
             'price carry and overstates the centre by roughly the yield.)')
    # THE DIRECTION CALL IS STATED ON EVERY NAME [R-DRIFT-01], including inside the
    # dead zone, where it prints WEAK against a tilt of exactly zero. It is DERIVED
    # from the strike's own z and alpha, never asserted — a call typed into a
    # published note could disagree with the cone beneath it and nothing here would
    # see it. The ceiling clause is stated because the rule is that the tilt never
    # exceeds ic x sigma x z: past that a bigger number is a deliberately worse
    # forecast, not more conviction, and the reader is told so plainly.
    z1 = h1['signal_z']
    if not prof.signal_active:
        call = ('No direction call: this market carries no surviving momentum cell, '
                'so the cone is carry-centered.')
    else:
        side = 'UP' if z1 > 0 else ('DOWN' if z1 < 0 else 'FLAT')
        if abs(z1) < 0.25:
            call = (f'Direction call {side} but WEAK — this name\u2019s own '
                    f'{prof.signal_type} z is {z1:+.3f}, inside the 0.25 dead zone, '
                    f'so the tilt applied is exactly 0 and the cone is carry-centered.')
        else:
            a1 = (math.exp(h1['signal_alpha']) - 1) * 100
            a3 = (math.exp(h3['signal_alpha']) - 1) * 100
            call = (f'Direction call {side}, from this name\u2019s own '
                    f'{prof.signal_type} z of {z1:+.3f} (outside the 0.25 dead zone); '
                    f'tilt {a1:+.2f}% at 1M and {a3:+.2f}% at 3M, applied through the '
                    f'engine\u2019s per-market signal socket at the horizon\u2019s own '
                    f'measured ic and capped at ic x sigma x z.')
    # The note quoted the POOLED width_cal as though it were the width the cone was
    # built on. For any name past the adaptive overlay's history gate that is simply
    # false: strike() multiplies width_cal by live_width_mult() before simulating, and
    # ADIB (58 resolved windows against MIN_WINDOWS=28) has been clearing that gate
    # silently — so the standing note that EG's overlay is dormant is stale for it.
    # A number stated in prose must be COMPUTED, not typed, so the clause is DERIVED
    # from the value strike() actually applied and disappears when it is exactly 1.0.
    wmult = r.get('width_overlay_mult', 1.0)
    wnote = '' if abs(wmult - 1.0) < 1e-9 else (
        f' PER-NAME WIDTH OVERLAY APPLIED (engine/adaptive_width.py): this name has '
        f'cleared the {AW.MIN_WINDOWS}-window history gate, so live_width_mult() returns '
        f'{wmult:.4f} on its OWN resolved 3-month residuals and the cone was simulated at '
        f'an effective width_cal of {prof.width_cal * wmult:.4f}, not the pooled '
        f'{prof.width_cal}. It is an OVERLAY, NOT A REFIT: the pooled (nu, width_cal), the '
        f'carry drift and the tail nu are untouched by it.'
    )
    calflag, calnote = name_calibration(market, series, prof, wmult)
    note = (
        f'Cycle {cyc} roll-forward, {today} — struck on the {d.day:02d}-'
        f'{MONTHS[d.month - 1]}-{d.year} close, the latest session in this '
        f'name’s library, {event}. The previous cone was anchored '
        f'{prior[0] if prior else "?"}; every still-open cohort on cycle '
        f'{prior[1] if prior else 1} stays OPEN and grades on its own '
        f'terms; nothing retro-edited. Production chain, no approximation: '
        f'Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 '
        f'→ har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) '
        f'→ simulate_paths_v3, 50,000 paths, seed 42, signal '
        f'{"ON" if prof.signal_active else "OFF"}. q_annual={q_annual:g} '
        f'{qnote} '
        f'{market} live fit nu={prof.nu}, width_cal={prof.width_cal}.{wnote}{calnote} rf_live '
        f'{RF_SRC.get(market, f"{prof.rf_live:.2%} profile rf_live")}. {call} Horizons '
        f'resolved by horizons.resolve() on {market}’s own realized calendar — '
        f'a calendar commitment, not a session count; the session counts '
        f'(h={h1["h"]} / {h3["h"]}) size the cone only.')

    rows = []
    for tag, h in (('1M', h1), ('3M', h3)):
        rows.append(dict(
            instrument=inst, asset_class=aclass, anchor_date=r['anchor_date'],
            run_date=pd.Timestamp(today.replace('-', ' ')).date().isoformat(),
            anchor_price=round(spot, 4), ccy=ccy, horizon_label=h['label'],
            grade_date=h['grade_date'], grade_basis=h['basis'],
            horizon_days=h['h'], cycle_no=cyc,
            reanchor_from=(prior[0] if prior else None),
            anchor_vol=round(h['anchor_vol_ann'], 4),
            cal=calflag,
            signal_z=round(h['signal_z'], 4),
            signal_alpha=round(h['signal_alpha'], 6), note=note,
            p5=round(h['pct']['p5'], 2), p25=round(h['pct']['p25'], 2),
            p50=round(h['pct']['p50'], 2), p75=round(h['pct']['p75'], 2),
            p95=round(h['pct']['p95'], 2),
            touch=rel_touch(h['_paths'], spot)))

    header = (f'\n\n  // ---- {today} single-name roll-forward: {key}, struck on '
              f'its own\n  //      latest library close. Append-only.\n')
    out = src[:a] + new + src[b:]
    out = insert_rows(out, rows, header)
    # SITE.updated is ISO on every other entry — the human "29-Jul-2026" form is
    # for prose notes only. Writing the prose form here would silently change a
    # field convention the rest of the site reads.
    d0 = pd.Timestamp(today.replace('-', ' '))
    out = bump_site_updated(out, d0.date().isoformat())

    if write:
        open(DATA_JS, 'w', encoding='utf-8').write(out)
        print(f'  wrote {DATA_JS} (+{len(rows)} ledger rows)')
    else:
        print('  DRY RUN — nothing written')
    return out, rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('market'); ap.add_argument('series'); ap.add_argument('key')
    ap.add_argument('--today', required=True)
    ap.add_argument('--q-annual', type=float, default=0.0)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    run(args.market, args.series, args.key, args.today,
        q_annual=args.q_annual, write=args.write)
