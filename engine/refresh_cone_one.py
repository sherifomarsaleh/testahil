"""refresh_cone_one.py — MID-CYCLE cone refresh for ONE covered name.

STEP 0 decision (a) of the Roll-Forward & Grading Protocol: OHLC that arrives
between monthly events refreshes the DISPLAYED cone and the technical read
only. It mints no LEDGER row, because ledger strikes stay on the 1-month
maturity metronome — otherwise 1M tails accumulate and the rhythm breaks.

That rule existed only as prose, so the only single-name tool on hand was
`rollforward_one.py`, which always appends two ledger rows. Running it
mid-cycle would strike a cohort the metronome did not call for and break the
lifecycle invariant (exactly one open row at the latest anchor per
(instrument, horizon)). This module is that rule made executable.

The cone itself is struck by the identical production chain — Step 0.0 gate ->
YZ variance proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50,000 paths, seed 42, signal per the profile — and the
ticker entry is rewritten by `rollforward_one.restrike_entry`, the same
function the monthly path uses, so the two cannot publish differently-shaped
cones. The ONLY difference between the two tools is whether a LEDGER row is
struck; that is asserted here, not assumed.

Rewrites spot / spotDate / dist / hz / touch and SITE.updated. Touch is
recomputed at the SAME absolute levels already on the page, never re-picked.
fair{} (the two-clocks rule), the slider's factor-stack constants and files
are untouched. levels/tech/asof and the chart belong to apply_technicals.py +
ta_chart.py, which must be run after this — "when the library moves, the
technical read moves with it, IN THE SAME PASS".

Run:  python3 refresh_cone_one.py IN TMPV TMPV --today 03-Aug-2026
      python3 refresh_cone_one.py IN TMPV TMPV --today 03-Aug-2026 --write
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pandas as pd                                          # noqa: E402

from strike_cohorts import strike                             # noqa: E402
from rollforward_one import restrike_entry, report_strike     # noqa: E402
from apply_rollforward import (ticker_blocks, bump_site_updated,       # noqa: E402
                               fmt_price, fmt_spot)

DATA_JS = os.path.join(ROOT, 'assets', 'data.js')
import site_data                                             # noqa: E402


def _ledger(src: str) -> str:
    i = src.find('const LEDGER')
    return src[i:src.find('\n];', i)]


def run(market: str, series: str, key: str, today: str,
        q_annual: float = 0.0, write: bool = False):
    src = open(DATA_JS, encoding='utf-8').read()
    blocks = ticker_blocks(src)
    if key not in blocks:
        raise SystemExit(f'{key} not found in TICKERS')
    a, b = blocks[key]

    r = strike(market, series, q_annual=q_annual)
    report_strike(key, market, series, r)

    out = src[:a] + restrike_entry(
        src[a:b], r,
        run_date=pd.Timestamp(today.replace('-', ' ')).date().isoformat()
    ) + src[b:]
    out = bump_site_updated(out, pd.Timestamp(today.replace('-', ' '))
                            .date().isoformat())

    # The defining property of a mid-cycle pass, checked rather than trusted.
    if _ledger(out) != _ledger(src):
        raise SystemExit('LEDGER changed — a mid-cycle refresh must never '
                         'strike a cohort. Aborted, nothing written.')
    print('  LEDGER byte-identical — no cohort struck (mid-cycle, '
          'STEP 0 decision (a))')
    print('  fair{}, slider constants, levels/tech/asof, files: untouched')

    if write:
        ledger_before = site_data.read_list('LEDGER', DATA_JS)
        open(DATA_JS, 'w', encoding='utf-8').write(out)
        # VERIFIED BY THE PARSER [R-ENF-03]. This module had NO post-write check of any
        # kind — not even `node --check` — and it is a cone writer, which is the thing a
        # reader is shown. Its pre-write LEDGER comparison is a TEXT comparison of the
        # string it is about to write; that cannot see a duplicated key, which is valid
        # JavaScript and leaves the parser taking the other one.
        h1v, h3v = r['horizons']['1M'], r['horizons']['3M']
        site_data.assert_written(
            'TICKERS', key,
            {'spot': float(fmt_spot(r['spot'])),
             'dist': {t: {'label': h['label'], 'resolve': h['grade_date'],
                          **{q: float(fmt_price(h['pct'][q], r['spot']))
                             for q in ('p5', 'p25', 'p50', 'p75', 'p95')}}
                      for t, h in (('t20', h1v), ('t60', h3v))}}, DATA_JS)
        # the defining property of a mid-cycle pass, now checked against the PARSED
        # ledger rather than against the text that was about to be written
        if site_data.read_list('LEDGER', DATA_JS) != ledger_before:
            raise SystemExit('LEDGER changed on disk — a mid-cycle refresh must never '
                             'strike a cohort.')
        site_data.assert_ledger_lifecycle(DATA_JS)
        print('  verified through a real parse; LEDGER unchanged and the lifecycle '
              'invariant holds')
        print(f'  wrote {DATA_JS}')
    else:
        print('  DRY RUN — nothing written')
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('market'); ap.add_argument('series'); ap.add_argument('key')
    ap.add_argument('--today', required=True)
    ap.add_argument('--q-annual', type=float, default=0.0)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    run(args.market, args.series, args.key, args.today,
        q_annual=args.q_annual, write=args.write)
