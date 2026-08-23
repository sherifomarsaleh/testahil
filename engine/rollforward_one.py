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
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pandas as pd                                        # noqa: E402

from strike_cohorts import strike, touch_probs, rel_touch   # noqa: E402
import market_profiles as MP                                # noqa: E402
import adaptive_width as AW                                # noqa: E402
from apply_rollforward import (ticker_blocks, fmt_price,  # noqa: E402
                               prior_anchor, js_row,
                               bump_site_updated, MONTHS, RF_SRC)
from apply_technicals import (LEDGER_ALIAS,               # noqa: E402
                              top_level_blocks, match_brace)

# Market codes whose covered names are not equities. asset_class was hardcoded
# 'equity' below, so a metals roll-forward mislabelled its own ledger rows.
METAL_MARKETS = {'XAU', 'XPT'}


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


def restrike_entry(blk: str, r: dict, verbose: bool = True) -> str:
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
                      lambda m: f'spot:{m.group(1)}{fmt_price(spot, spot)},',
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
    dist = (f'{ind}dist: {{\n' + ',\n'.join(lines) + f'\n{ind}}},\n'
            + f'{ind}hz: {{ h1:{h1["h"]}, h3:{h3["h"]}, '
              f'l1:"{h1["label"]}", l3:"{h3["label"]}", cal:true }},')
    # `dist` and `hz` are emitted as one unit, so hz must be the field that
    # immediately follows. That holds on all 71 ticker entries; if a future
    # entry breaks it, say so rather than silently leaving a stale hz behind
    # the fresh cone — a wrong hz draws the wrong fan with no visible tell.
    hz_span = _span_of_key(new, 'hz')
    if not hz_span or new[e0:hz_span[0]].strip() != '':
        raise ValueError('hz does not immediately follow dist on this entry')
    new = new[:s0] + '\n' + dist.lstrip('\n') + new[hz_span[1]:]

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


def _prior_1m_matured(src: str, instrument: str, prior_cycle, anchor_date: str):
    """The prior cycle's 1-month grade date, IF it has come due by this anchor.

    Returns the grade date (str) when this strike lands on the monthly metronome —
    STEP 0 rule 2, "the 1-month maturity is the metronome" — and None when it does
    not. Read off the ledger rather than assumed, because the note that quotes it
    is published and a wrong claim there is invisible to every other check.
    """
    if prior_cycle is None:
        return None
    i = src.find('const LEDGER')
    led = src[i:src.find('\n];', i)]
    for m in re.finditer(r'instrument:"' + re.escape(instrument) + r'"(.{0,900})',
                         led, re.S):
        e = m.group(1)
        cy = re.search(r'cycle_no:(\d+)', e)
        hl = re.search(r'horizon_label:"([^"]+)"', e)
        gd = re.search(r'grade_date:"([^"]+)"', e)
        if cy and hl and gd and int(cy.group(1)) == prior_cycle \
                and hl.group(1) == '1 month' and gd.group(1) <= anchor_date:
            return gd.group(1)
    return None


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
    new = restrike_entry(blk, r)

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
    metro = _prior_1m_matured(src, inst, prior[1] if prior else None, r['anchor_date'])
    event = ('at the monthly metronome — the prior cycle’s 1-month matured on '
             f'{metro} and is graded in this same pass' if metro else
             'off the monthly metronome — the prior cycle’s 1-month has not yet '
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
    # The published note quoted the POOLED width_cal as though it were the width the
    # cone was built on. For any name past the adaptive overlay's history gate that is
    # simply false: strike() multiplies width_cal by live_width_mult() before
    # simulating, and ADIB (58 resolved windows against MIN_WINDOWS=28) has been
    # clearing that gate silently. A note that states a number the run did not use is
    # the "number stated in prose must be computed, not typed" defect, so the clause is
    # DERIVED from the value strike() actually applied and disappears when it is 1.0.
    wmult = r.get('width_overlay_mult', 1.0)
    wnote = '' if abs(wmult - 1.0) < 1e-9 else (
        f' PER-NAME WIDTH OVERLAY APPLIED (engine/adaptive_width.py): this name has '
        f'cleared the {AW.MIN_WINDOWS}-window history gate, so live_width_mult() returns '
        f'{wmult:.4f} on its OWN resolved 3-month residuals and the cone was simulated at '
        f'an effective width_cal of {prof.width_cal * wmult:.4f}, not the pooled '
        f'{prof.width_cal}. It is an OVERLAY, NOT A REFIT: the pooled (nu, width_cal), the '
        f'carry drift and the tail nu are untouched by it.'
    )
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
        f'{market} live fit nu={prof.nu}, width_cal={prof.width_cal}.{wnote} rf_live '
        f'{RF_SRC.get(market, f"{prof.rf_live:.2%} profile rf_live")}. Horizons '
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
            anchor_vol=round(h['anchor_vol_ann'], 4), note=note,
            # Recorded per [R-DRIFT-01]; null (not 0.0) when the socket is OFF,
            # because signal_alpha() returns a placeholder 0.0 z in that case and
            # storing it would assert a measurement that was never made.
            signal_z=(round(h['signal_z'], 4) if prof.signal_active else None),
            signal_alpha=(round(h['signal_alpha'], 5)
                          if prof.signal_active else None),
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
