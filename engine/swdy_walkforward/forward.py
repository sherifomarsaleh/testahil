"""Years 3-5 as RANGES, from THIS record's own driver-error distribution.

[R-FCAL-01] requires the delivered study to publish years three to five as ranges and
never as points. [R-FCAL-01 AMENDED 07-09-2026] requires the published band to declare,
per driver and horizon, its BASIS from a closed list (percentile / span / factor), its
COUNT, and its ORIENTATION from the closed pair.

ORIENTATION IS DECLARED BECAUSE A RECIPROCAL IS THE MOST DANGEROUS UNIT ERROR THERE IS.
The five runs before this one published multipliers three ways: one as actual over
forecast, two as forecast over actual, all three labelled "multipliers to apply to a
point projection", and the third carried no note at all. A factor of 0.4 and a factor of
2.5 are each an ordinary thing to read in a band and only the arithmetic says which is
meant. THIS RECORD PUBLISHES ACTUAL OVER FORECAST: multiply the point projection by the
band to get the range the outturn is expected to fall in.

BASIS IS DECLARED BECAUSE A SPAN IS NOT A PERCENTILE. Nine or more observations support
a p10-p90; below that the SPAN of the observations is what the record supports and
calling it a percentile would be the free parameter this method forbids.
"""
import json, os, sys, math, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score as S

OUT = os.path.join(HERE, 'forward_ranges.json')
MIN_FOR_PERCENTILE = 9


def band(errs):
    """(low, high, basis, n) — ACTUAL OVER FORECAST, so exp(-e) since e = ln(proj/act)."""
    fac = sorted(math.exp(-e) for e in errs)
    n = len(fac)
    if n >= MIN_FOR_PERCENTILE:
        lo = statistics.quantiles(fac, n=10, method='inclusive')[0]
        hi = statistics.quantiles(fac, n=10, method='inclusive')[8]
        return lo, hi, 'percentile', n
    return fac[0], fac[-1], 'span', n


def main():
    cells = json.load(open(os.path.join(HERE, 'error_cells.json')))['cells']
    out = {}
    for k in S.DRIVERS:
        per_h = {}
        for h in (3, 4, 5):
            es = [c['e'] for c in cells if c['driver'] == k and c['h'] == h]
            if not es:
                continue
            lo, hi, basis, n = band(es)
            per_h[str(h)] = dict(low=lo, high=hi, basis=basis, count=n,
                                 orientation='actual_over_forecast',
                                 median=statistics.median(math.exp(-e) for e in es))
        if per_h:
            out[k] = per_h
    rec = dict(
        _='SWDY forward ranges for years 3-5, from this run\'s own driver-error '
          'distribution. The study applies these to its point path; the point path is '
          'not published alone for those years.',
        built='2026-09-07',
        orientation='actual_over_forecast',
        orientation_note='MULTIPLY a point projection by the band. A band of 1.4 to 1.8 '
                         'says the outturn is expected between 1.4x and 1.8x the point, '
                         'i.e. the point UNDER-forecasts. The reciprocal convention '
                         '(forecast over actual) is NOT used here and the two are not '
                         'interchangeable.',
        basis_rule='percentile at %d observations or more, otherwise the SPAN of the '
                   'observations. A span over four observations is the range of four '
                   'numbers and is not a p10-p90.' % MIN_FOR_PERCENTILE,
        bands=out)
    json.dump(rec, open(OUT, 'w'), indent=1)
    print('%-28s %-3s %-6s %5s   %-18s' % ('driver', 'h', 'basis', 'n', 'band (act/fcst)'))
    for k, per_h in out.items():
        for h, b in sorted(per_h.items()):
            print('%-28s %-3s %-6s %5d   %.3f - %.3f  (median %.3f)'
                  % (k, h, b['basis'], b['count'], b['low'], b['high'], b['median']))
    return rec


if __name__ == '__main__':
    main()
