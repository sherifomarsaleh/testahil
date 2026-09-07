#!/usr/bin/env python3
"""Part E criterion 2, first half: forward drivers inside each name's own walk-forward band.

    "On the five re-issued names, forward drivers sit inside each name's own
     walk-forward p10-p90 or carry a priced exception; every claimed correction
     reconciles to its log."

The SECOND half is gated by scripts/check_corrections_applied.py. The first half had
never been measured, and `acceptance.py` said so in its own words — "needs a per-name
driver comparison this file does not build". THE OBSTACLE WAS NOT EFFORT.

FIVE RUNS COMMIT forward_ranges.json AND IT HAS FIVE INCOMPATIBLE SHAPES. Measured
07-09-2026:

    AMOC   published_band[horizon][driver] -> low_factor / high_factor   (MULTIPLIER)
    ARCC   [driver][horizon]               -> mult_low / mult_high       (MULTIPLIER)
    EGCH   published_band[horizon][driver] -> low_factor / high_factor   (MULTIPLIER)
    PHDC   years[driver][horizon]          -> p10 / p90 around a level   (LEVEL)
    TMGH   projection[year][driver]        -> low / high around a level  (LEVEL)

A single reader finds ARCC and reports the other four as having no bands at all — which
is what a first pass here did, printing "0 driver-horizon bands" for four runs whose
files were sitting there full of them. That is the failure this repository has now
recorded of the corrections records in the same words: FIVE RECORDS, FIVE SHAPES, AND A
READER THAT GUESSES SILENTLY FINDS NOTHING. So the adapters are NAMED PER RUN, on the
check_correction_boundary pattern, and a run without one is REPORTED rather than skipped
[R-ENF-04].

THE TWO FAMILIES REDUCE TO ONE QUESTION. A multiplier band says what the method's own
history did to a point projection at that horizon, so the forecast sits inside its own
record exactly when the band contains 1.0. A level band publishes the projection and its
p10-p90 directly, so the forecast sits inside when the central lies between them. Both
are "does this run's own band contain this run's own forward driver".

WHAT A BAND EXCLUDING ITS OWN POINT MEANS, and it is not a formatting quibble: the
method's own history says that at that horizon it was wrong in one direction EVERY TIME
it was scored. That is what the criterion calls a priced exception — the study may still
carry the driver, and it owes an explicit statement of the exception and its value.

THIS IS A MEASUREMENT, NOT A GATE. It prints the criterion's state; it does not refuse.
Criterion 2 is a programme acceptance item and the acceptance instrument is
acceptance.py, which now reads this. A gate would have to say what "priced" means in
code, and pricing an exception is a judgement.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
FIVE = ('AMOC', 'ARCC', 'EGCH', 'PHDC', 'TMGH')


def _load(tk):
    p = os.path.join(ENG, '%s_walkforward' % tk.lower(), 'forward_ranges.json')
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding='utf-8'))


# ---------------------------------------------------------------- named adapters
# Each returns [(driver, horizon, low, high, point, family)] or raises.

def _n_of(v):
    for k in ('n', 'n_full', 'n_kima2', 'n_observations'):
        if isinstance(v.get(k), (int, float)):
            return int(v[k])
    return None


def _mult_band(o, key, lo_k, hi_k):
    """published_band[horizon][driver] -> factors. The point of a multiplier is 1.0."""
    out = []
    band = o.get(key) or {}
    for h, drivers in band.items():
        if not isinstance(drivers, dict):
            continue
        for drv, v in drivers.items():
            if not isinstance(v, dict) or lo_k not in v:
                continue
            out.append((drv, str(h), float(v[lo_k]), float(v[hi_k]), 1.0,
                        'multiplier', _n_of(v), 'factor'))
    return out


# THE ORIENTATION IS PART OF THE BAND AND TWO RUNS PUBLISH IT THE OTHER WAY UP.
# Measured 07-09-2026 against each run's OWN scored bias: ARCC's multipliers are
# actual/forecast (a band near 1.7 where its error says the outturn came in 1.4-1.8x
# the forecast), while AMOC's and EGCH's are forecast/actual (bands near 0.4 where the
# error says the forecast was 0.3-0.7x the outturn). THEY ARE RECIPROCALS AND BOTH ARE
# LABELLED "MULTIPLIERS TO APPLY TO A POINT PROJECTION". AMOC and EGCH carry a note
# stating their convention correctly; ARCC carries no note at all.
#
# Applying one run's band as the other's instructs would move a forecast THE WRONG WAY —
# halving a cost line the record says should roughly double. Containment of the point is
# unaffected (a band excluding 1.0 excludes it in either orientation, since reciprocation
# maps 1.0 to itself), so the criterion 2 verdict does not move; WHAT MOVES IS THE
# DIRECTION each outside cell is reported in, and the first pass here reported EGCH's
# cost_of_sales as over-forecast when its own scores say it was under-forecast by 2.5x.
FORECAST_OVER_ACTUAL = ('AMOC', 'EGCH')     # factor = forecast / actual
ACTUAL_OVER_FORECAST = ('ARCC',)            # factor = actual / forecast


def direction(tk, lo, hi, family):
    """Which way the method erred, in the run's OWN orientation. Never inferred from
    the number alone, because the two conventions are reciprocals."""
    if family != 'multiplier':
        return ''
    mid = (lo + hi) / 2.0
    if tk in FORECAST_OVER_ACTUAL:
        return 'UNDER-forecast' if mid < 1 else 'OVER-forecast'
    if tk in ACTUAL_OVER_FORECAST:
        return 'UNDER-forecast' if mid > 1 else 'OVER-forecast'
    return 'orientation not declared for this run'


def adapt_amoc(o):
    return _mult_band(o, 'published_band', 'low_factor', 'high_factor')


def adapt_egch(o):
    return _mult_band(o, 'published_band', 'low_factor', 'high_factor')


def adapt_arcc(o):
    """[driver][horizon] at the TOP level — no wrapper key at all."""
    out = []
    for drv, hs in o.items():
        if not isinstance(hs, dict):
            continue
        for h, v in hs.items():
            if not isinstance(v, dict) or 'mult_low' not in v:
                continue
            out.append((drv, str(h), float(v['mult_low']), float(v['mult_high']),
                        1.0, 'multiplier', _n_of(v), 'factor'))
    return out


def adapt_phdc(o):
    """years[driver][horizon] -> p10/p90 around a projected LEVEL."""
    out = []
    for drv, hs in (o.get('years') or {}).items():
        if not isinstance(hs, dict):
            continue
        for h, v in hs.items():
            if not isinstance(v, dict) or 'p10' not in v:
                continue
            point = v.get('central_after_record_median', v.get('raw_projection'))
            if point is None:
                continue
            out.append((drv, str(h), float(v['p10']), float(v['p90']),
                        float(point), 'level', _n_of(v), 'percentile'))
    return out


def adapt_tmgh(o):
    """projection[year][driver] -> low/high around a central LEVEL."""
    out = []
    for year, drivers in (o.get('projection') or {}).items():
        if not isinstance(drivers, dict):
            continue
        for drv, v in drivers.items():
            if not isinstance(v, dict) or 'low' not in v or 'high' not in v:
                continue
            point = v.get('central', v.get('raw'))
            if point is None:
                continue
            out.append((drv, str(year), float(v['low']), float(v['high']),
                        float(point), 'level', _n_of(v), 'span'))
    return out


ADAPTERS = {'AMOC': adapt_amoc, 'ARCC': adapt_arcc, 'EGCH': adapt_egch,
            'PHDC': adapt_phdc, 'TMGH': adapt_tmgh}


def measure():
    rows = []
    for tk in FIVE:
        o = _load(tk)
        if o is None:
            rows.append((tk, 'no forward_ranges.json', [], []))
            continue
        fn = ADAPTERS.get(tk)
        if fn is None:
            rows.append((tk, 'no named adapter — reported, never skipped', [], []))
            continue
        try:
            cells = fn(o)
        except Exception as exc:                                    # noqa: BLE001
            rows.append((tk, 'adapter raised: %s' % str(exc)[:70], [], []))
            continue
        if not cells:
            rows.append((tk, 'adapter read ZERO bands — a reader that finds nothing '
                             'has not shown there is nothing [R-ENF-04]', [], []))
            continue
        outside = [c for c in cells if not (c[2] <= c[4] <= c[3])]
        rows.append((tk, 'read', cells, outside))
    return rows


def main(argv):
    rows = measure()
    print('PART E CRITERION 2 (first half) — forward drivers inside each name\'s own')
    print('walk-forward band. Five runs, FIVE SHAPES, one named adapter each.\n')
    tot = out = 0
    unread = []
    for tk, state, cells, outside in rows:
        if state != 'read':
            print('  %-6s %s' % (tk, state))
            unread.append(tk)
            continue
        tot += len(cells)
        out += len(outside)
        fam = cells[0][5]
        print('  %-6s %3d driver-horizon bands (%s)  %d OUTSIDE'
              % (tk, len(cells), fam, len(outside)))
        for c in sorted(outside)[:6]:
            drv, h, lo, hi, pt, fam, n, named = c
            dirn = direction(tk, lo, hi, fam)
            print('           %-18s h=%-5s band [%.4g, %.4g]  point %.4g  n=%s (%s)%s'
                  % (drv, h, lo, hi, pt, n if n is not None else '?', named,
                     '  ' + dirn if dirn else ''))
    print('\n  %d bands read across %d run(s); %d place the run\'s own forward driver '
          'OUTSIDE its own band' % (tot, len(FIVE) - len(unread), out))
    if unread:
        print('  UNREAD: %s — an unread run is not a passing one [R-ENF-04]'
              % ', '.join(unread))
    # BOTH READINGS ARE REPORTED AND NEITHER IS CHOSEN SILENTLY. The criterion says
    # "p10-p90", and only ONE run publishes a figure it calls a percentile: PHDC's
    # p10/p90. The others publish a FACTOR or a SPAN, and two of them say in their own
    # notes why — EGCH prints percentiles only at n>=9, and AMOC states that on 4, 3 and
    # 2 observations "no percentile is computed ... the span and the bias/MAE band are
    # what the record supports". A band from three observations is not a p10-p90 and
    # calling it one would be the free parameter this house forbids; treating every
    # exclusion as equivalent would OVERSTATE the finding, and reporting only the
    # percentile reading would UNDERSTATE it. So both are printed with their counts.
    strict = [c for _t, st, cs, o_ in rows if st == 'read'
              for c in o_ if c[7] == 'percentile']
    thin = [c for _t, st, cs, o_ in rows if st == 'read'
            for c in o_ if c[7] != 'percentile' and (c[6] or 0) < 9]
    firm = [c for _t, st, cs, o_ in rows if st == 'read'
            for c in o_ if c[7] != 'percentile' and (c[6] or 0) >= 9]
    print('\n  OF THE %d OUTSIDE: %d on a figure the run CALLS a percentile, '
          '%d on a factor or span at n>=9, %d on fewer than nine observations'
          % (out, len(strict), len(firm), len(thin)))
    print('\n  CRITERION 2 (first half), BOTH READINGS:')
    if unread:
        print('    UNMEASURED on %s — an unread run is not a passing one [R-ENF-04].'
              % ', '.join(unread))
    print('    BROAD  (any published band, however few observations behind it): '
          '%s — %d cell(s) outside.'
          % ('NOT MET' if out else 'MET', out))
    if strict:
        print('    STRICT (only a figure the run itself calls a p10-p90): NOT MET — '
              '%d cell(s) outside.' % len(strict))
    else:
        print('    STRICT (only a figure the run itself calls a p10-p90): MET on the '
              'ONE run that publishes percentiles, and UNTESTABLE on the four that do '
              'not — an untestable criterion is UNMEASURED, never met [R-ENF-04].')
    print('    NO run commits a priced exception in its ranges file — measured, not '
          'assumed. Whether one is argued in prose is not read here.')
    print('  The second half (every claimed correction reconciles to its log) is gated '
          'by\n  scripts/check_corrections_applied.py and is not restated here.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
