#!/usr/bin/env python3
"""ADIB — the FUNDAMENTAL walk-forward's headline numbers, committed once.

The study reads THIS, so no figure about the run is ever typed into a document.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score, bottom_up as bu  # noqa: E402

rows = score.cells()
s_all = score.summarise(rows, 'model', by_h=False)
out = dict(
    which='the FUNDAMENTAL walk-forward [R-FCAL-01] — drivers projected from a past origin '
          'and scored against what the company reported. Not the price-engine walk-forward '
          '(band coverage on the Monte Carlo cone) and not the technical one.',
    scope='full', span='FY2010-FY2025, 16 consolidated fiscal years, every one footing',
    origins=len(bu.ORIGINS), horizons='1-5',
    cells_per_driver=sum(1 for r in rows if r['method'] == 'model' and r['line'] == 'pbt'),
    drivers=len(score.LINES),
    sign_broken=sum(1 for r in rows if r['status'] == 'sign-broken'),
    per_driver={}, skill={}, by_horizon={})
for (line, _), v in s_all.items():
    if v.get('n'):
        out['per_driver'][line] = {k: v[k] for k in
                                   ('n', 'bias', 'mae', 'bias_lo', 'bias_hi', 'over',
                                    'bias_early', 'bias_late', 'stable', 'sign_broken')}
for line in score.LINES:
    k = score.skill(rows, line)
    if k:
        out['skill'][line] = k
for h in (1, 2, 3, 4, 5):
    sh = score.summarise([r for r in rows if r['h'] == h], 'model', by_h=False)
    v = sh.get(('np_parent', 0))
    if v and v.get('n'):
        out['by_horizon']['h%d' % h] = dict(n=v['n'], bias=v['bias'], mae=v['mae'])
json.dump(out, open(os.path.join(HERE, 'walkforward_summary.json'), 'w'), indent=1,
          default=float)
print('written; %d cells per driver, %d drivers, skill on np_parent vs freeze %+.0f%%, '
      'vs trend %+.0f%%'
      % (out['cells_per_driver'], out['drivers'],
         100 * out['skill']['np_parent']['vs_freeze'],
         100 * out['skill']['np_parent']['vs_trend']))
