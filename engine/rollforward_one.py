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
from apply_rollforward import (ticker_blocks, parse_touch_levels,  # noqa: E402
                               fmt_price, prior_anchor, js_row,
                               bump_site_updated, MONTHS, RF_SRC)

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


def run(market: str, series: str, key: str, today: str,
        q_annual: float = 0.0, write: bool = False):
    src = open(DATA_JS, encoding='utf-8').read()
    blocks = ticker_blocks(src)
    if key not in blocks:
        raise SystemExit(f'{key} not found in TICKERS')
    a, b = blocks[key]
    blk = src[a:b]

    r = strike(market, series, q_annual=q_annual)
    prof = MP.PROFILES[market]
    spot = r['spot']
    anchor = pd.Timestamp(r['anchor_date'])
    sd = f'close {anchor.day:02d} {MONTHS[anchor.month - 1]} {anchor.year}'
    h1, h3 = r['horizons']['1M'], r['horizons']['3M']
    ccy = (re.search(r'ccy:\s*"([^"]+)"', blk) or [None, '?'])[1]
    prior = prior_anchor(src, key)
    cyc = prior[1] + 1 if prior else 2

    print(f'{key} ({market}/{series})')
    print(f'  prior cycle {prior} -> new cycle {cyc}')
    print(f'  anchor {r["anchor_date"]} @ {spot}  ({r["rows_out"]} clean rows)')
    for tag, h in (('1M', h1), ('3M', h3)):
        print(f'  {tag}: {h["label"]:9s} h={h["h"]:3d} grade {h["grade_date"]} '
              f'p5..p95 ' + ' '.join(f'{h["pct"][q]:.2f}'
                                     for q in ('p5', 'p25', 'p50', 'p75', 'p95')))

    # ---- ticker entry: spot / spotDate / dist+hz / touch, nothing else
    new = blk
    new = re.sub(r'\n    spot: [\d.,]+,', f'\n    spot: {fmt_price(spot, spot)},',
                 new, count=1)
    new = re.sub(r'\n    spotDate: "[^"]*",', f'\n    spotDate: "{sd}",',
                 new, count=1)

    def row(tag, h, pad):
        p, f = h['pct'], lambda v: fmt_price(v, spot)      # noqa: E731
        return (f'      {tag}: {{ label:"{h["label"]}",{pad}'
                f'p5:{f(p["p5"])}, p25:{f(p["p25"])}, p50:{f(p["p50"])}, '
                f'p75:{f(p["p75"])}, p95:{f(p["p95"])}, '
                f'resolve:"{h["grade_date"]}" }}')
    dist = ('    dist: {\n' + row('t20', h1, '   ') + ',\n'
            + row('t60', h3, '  ') + '\n    },\n'
            + f'    hz: {{ h1:{h1["h"]}, h3:{h3["h"]}, '
              f'l1:"{h1["label"]}", l3:"{h3["label"]}", cal:true }},')
    new = re.sub(r'\n    dist: \{.*?\n    \},(?:\n    hz: \{[^}]*\},)?',
                 '\n' + dist, new, count=1, flags=re.S)

    levels, comment = parse_touch_levels(blk)
    if levels:
        t1 = touch_probs(h1['_paths'], spot, levels)
        t3 = touch_probs(h3['_paths'], spot, levels)
        cells = ', '.join(f'[{fmt_price(lv, spot)}, {t1[float(lv)]}, {t3[float(lv)]}]'
                          for lv in levels)
        new = re.sub(r'\n    touch: \[.*?\n    \]',
                     f'\n    touch: [ {comment}\n      {cells}\n    ]',
                     new, count=1, flags=re.S)
        print(f'  touch recomputed at the SAME {len(levels)} absolute levels: {levels}')

    d = anchor
    note = (
        f'Cycle {cyc} roll-forward, {today} — struck on the {d.day:02d}-'
        f'{MONTHS[d.month - 1]}-{d.year} close, the latest session in this '
        f'name’s library. This name was NOT in the 28-Jul-2026 market-wide '
        f'EG/AE/SA re-strike, so its published cone had been anchored '
        f'{prior[0] if prior else "?"} against a library that had already moved '
        f'on — the gap the as-of stamps adopted 29-Jul-2026 made visible. '
        f'Cycle {prior[1] if prior else 1} stays OPEN and grades on its own '
        f'terms; nothing retro-edited. Production chain, no approximation: '
        f'Step 0.0 data-quality gate → YZ variance proxy → fit_har_v3 '
        f'→ har_forecast_v3 → carry drift ln(1+rf_live)−ln(1+q) '
        f'→ simulate_paths_v3, 50,000 paths, seed 42, signal '
        f'{"ON" if prof.signal_active else "OFF"}. q_annual={q_annual:g} '
        f'(FLAGGED — house convention; the drift is a GROSS-OF-DIVIDEND '
        f'price carry and overstates the centre by roughly the yield). '
        f'{market} live fit nu={prof.nu}, width_cal={prof.width_cal}; rf_live '
        f'{RF_SRC.get(market, f"{prof.rf_live:.2%} profile rf_live")}. Horizon '
        f'resolved by horizons.resolve() on {market}’s own realized '
        f'calendar, not a session count. This cohort also brings the name onto '
        f'the calendar 1M/3M convention it had never been migrated to.')

    rows = []
    for tag, h in (('1M', h1), ('3M', h3)):
        rows.append(dict(
            instrument=key, asset_class='equity', anchor_date=r['anchor_date'],
            anchor_price=round(spot, 4), ccy=ccy, horizon_label=h['label'],
            grade_date=h['grade_date'], grade_basis=h['basis'],
            horizon_days=h['h'], cycle_no=cyc,
            reanchor_from=(prior[0] if prior else None),
            anchor_vol=round(h['anchor_vol_ann'], 4), note=note,
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
