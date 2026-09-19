#!/usr/bin/env python3
"""ADIB (EGX) — the forward ranges years 3-5 are published as.

[R-FCAL-01 §6] "years 3-5 published as RANGES built from this record's own driver-error
distribution, never as points." This is where those ranges come from, and it is the ONLY
sanctioned route into the study's far years.

The distribution used is the LOG ERROR of the mechanical build, per horizon, over every
origin that produced a scorable cell. The band is the 10th-to-90th percentile of that
distribution applied to the study's own point path.

TWO SAMPLES, BOTH PRINTED. The full record includes the FY2014 and FY2015 origins, whose
trailing windows reach into the loss era and whose cost-of-risk driver is a decade out of
line; those origins project a LOSS and their cells are the widest in the record. The
FY2016+ sample is every origin whose five-year window sits inside the profit era. THE
WIDER SAMPLE IS THE ONE THE STUDY USES - a band chosen after seeing which is narrower is
not a band, and the far years are exactly where a study should be least confident.
"""
from __future__ import annotations
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as bu, score  # noqa: E402

LINES = ('np_parent', 'pbt', 'net_funds', 'fin_customers', 'total_assets')


def pct(v, p):
    if not v:
        return None
    v = sorted(v)
    k = (len(v) - 1) * p
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return v[lo] if lo == hi else v[lo] + (v[hi] - v[lo]) * (k - lo)


def dist(rows, line, h, origins=None):
    e = [r['e'] for r in rows
         if r['method'] == 'model' and r['line'] == line and r['h'] == h
         and r['status'] == 'ok' and (origins is None or r['origin'] in origins)]
    if not e:
        return None
    return dict(n=len(e), p10=pct(e, 0.10), p25=pct(e, 0.25), p50=pct(e, 0.50),
                p75=pct(e, 0.75), p90=pct(e, 0.90),
                mean=sum(e) / len(e), mae=sum(abs(x) for x in e) / len(e))


def build():
    rows = score.cells()
    late = set(o for o in bu.ORIGINS if o >= bu.ERA_BREAK)
    out = {'_': __doc__.strip(), 'lines': {}}
    for f in LINES:
        out['lines'][f] = {}
        for h in (1, 2, 3, 4, 5):
            out['lines'][f]['h%d' % h] = dict(
                all_origins=dist(rows, f, h),
                fy2016_plus=dist(rows, f, h, late))
    # THE BAND THE STUDY USES: the p10-p90 of the log error, INVERTED, because the
    # error is projected-over-actual and the band is what the actual could be given a
    # projection. actual = projection / exp(e), so the band on the actual is
    # [proj/exp(p90), proj/exp(p10)].
    band = {}
    for h in (3, 4, 5):
        d = out['lines']['np_parent']['h%d' % h]['all_origins']
        band['h%d' % h] = dict(n=d['n'],
                               low_multiple=math.exp(-d['p90']),
                               high_multiple=math.exp(-d['p10']),
                               median_multiple=math.exp(-d['p50']))
    out['band_on_attributable_profit'] = band
    return out


if __name__ == '__main__':
    d = build()
    json.dump(d, open(os.path.join(HERE, 'forward_ranges.json'), 'w'), indent=1)
    print('%-14s %3s %5s %8s %8s %8s %8s %8s   %s'
          % ('line', 'h', 'n', 'p10', 'p25', 'p50', 'p75', 'p90', 'sample'))
    for f in LINES:
        for h in (1, 2, 3, 4, 5):
            for tag in ('all_origins', 'fy2016_plus'):
                x = d['lines'][f]['h%d' % h][tag]
                if x:
                    print('%-14s %3d %5d %+8.3f %+8.3f %+8.3f %+8.3f %+8.3f   %s'
                          % (f, h, x['n'], x['p10'], x['p25'], x['p50'], x['p75'],
                             x['p90'], tag))
        print()
    print('THE BAND THE STUDY PUBLISHES on attributable profit (multiples on the point path):')
    for h in (3, 4, 5):
        b = d['band_on_attributable_profit']['h%d' % h]
        print('  year %d (n=%d):  low x%.3f   median x%.3f   high x%.3f'
              % (h, b['n'], b['low_multiple'], b['median_multiple'], b['high_multiple']))
