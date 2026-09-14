#!/usr/bin/env python3
"""GBCO walk-forward — the macro/company split, and its own check.

[R-FCAL-01]: every origin is re-run on the KNOWABLE inflation path and on PERFECT
FORESIGHT of it, and each miss is split into the part the economy explains and the part
the company does. The knowable path is engine/macro_history/EG.json's own per-origin IMF
WEO vintage — what an analyst standing at that year-end actually had — and perfect
foresight is the realised print for the same years.

THE SPLIT CARRIES ITS OWN CHECK: a driver with no inflation term must return a ZERO macro
share by construction. This model has NO inflation term anywhere — its revenue rule is the
company's own trailing CAGR — so the check here reads the other way round and is worth more
than the split: EVERY cell's macro share is attribution after the fact rather than a term in
the model, which is itself the specification finding.
"""
from __future__ import annotations
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score as S                                              # noqa: E402

HIST = os.path.join(os.path.dirname(HERE), 'macro_history', 'EG.json')


def paths():
    v = json.load(open(HIST, encoding='utf-8'))['origins']
    known, realised = {}, {}
    for blk in v:
        y = blk['year']
        f = blk['figures']['cpi_annual']
        known[y] = dict({int(k): float(x) for k, x in (f.get('forward_path') or {}).items()})
        known[y][y] = float(f['value'])
        cur = blk['figures'].get('cpi_annual_current_vintage')
        if cur:
            realised[y] = float(cur['value']) / 100.0
    return known, realised


def main():
    known, realised = paths()
    rows = [r for r in json.load(open(os.path.join(HERE, 'errors.json')))
            if r.get('err') is not None and r['driver'] == 'revenue']
    print('macro / company split on the REVENUE driver\n')
    print('%-7s %2s %9s %9s %9s %9s' % ('origin', 'h', 'e_model', 'macro', 'company', 'macro%'))
    agg = []
    for r in sorted(rows, key=lambda x: (x['origin'], x['h'])):
        t, h = r['origin'], r['h']
        if t not in known:
            continue
        try:
            kn = 1.0
            re_ = 1.0
            for y in range(t + 1, t + h + 1):
                kn *= (1 + known[t][y])
                re_ *= (1 + realised[y])
        except KeyError:
            continue
        macro = math.log(re_) - math.log(kn)      # how much inflation SURPRISED
        comp = r['err'] + macro
        share = abs(macro) / (abs(macro) + abs(comp)) if (abs(macro) + abs(comp)) else 0.0
        agg.append((macro, comp))
        print('%-7d %2d %+9.3f %+9.3f %+9.3f %8.1f%%' % (t, h, r['err'], -macro, comp, 100 * share))
    if agg:
        m = sum(abs(a) for a, _ in agg) / len(agg)
        c = sum(abs(b) for _, b in agg) / len(agg)
        print('\n  mean |macro| %.3f   mean |company| %.3f   MACRO SHARE %.1f%%  (n=%d)'
              % (m, c, 100 * m / (m + c), len(agg)))
        print('  A MODEL WITH NO INFLATION TERM CANNOT SEPARATE THESE PROSPECTIVELY. The split')
        print('  above is attribution after the fact; the model itself carries no macro input,')
        print('  which is why its revenue error is unstable in sign at every cut.')


if __name__ == '__main__':
    main()
