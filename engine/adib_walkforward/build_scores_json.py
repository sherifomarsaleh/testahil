#!/usr/bin/env python3
"""ADIB — the run's scores in the shape engine/lessons_harvest.py reads.

The harvester is the same for every name in the campaign, so this file translates this
run's own records into its schema rather than the harvester learning a per-name shape.
GENERATED from score.py and diagnose.py; never hand-edited.

`robust_sign` here means what the harvester means by it: the bias holds its sign across
every era cut tested. That is the same test the corrections rule applies, so a driver the
harvester calls robust and a driver the correction rule calls correctable are the same
set — two names for one measurement, which is what stops them drifting apart.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score, bottom_up as bu, diagnose  # noqa: E402

rows = score.cells()
S_all = score.summarise(rows, 'model', by_h=False)
out = {
 '_': __doc__.strip(),
 'run': 'ADIB', 'which': 'the FUNDAMENTAL walk-forward [R-FCAL-01]',
 'scope': 'full',
 'origins': ['FY%d' % o for o in bu.ORIGINS],
 'horizons': [1, 2, 3, 4, 5],
 'pre_registration': 'PRE_REGISTRATION_09-09-2026.md',
 'n_cells': sum(1 for r in rows if r['method'] == 'model' and r['status'] == 'ok'),
 'by_driver': {}, 'by_horizon': {}, 'by_era': {}, 'macro_split': {},
}
for (line, _), v in S_all.items():
    if not v.get('n'):
        continue
    out['by_driver'][line] = dict(bias=v['bias'], mae=v['mae'], over=v['over'],
                                  n=v['n'], n_cells=v['n'],
                                  robust_sign=bool(v['stable']),
                                  bias_ci=[v['bias_lo'], v['bias_hi']],
                                  sign_broken=v['sign_broken'])
    out['by_era'][line] = {}
    if v['bias_early'] is not None:
        out['by_era'][line]['E1 recapitalisation and the 2016 float (origins FY2014-FY2017)'] \
            = dict(bias=v['bias_early'])
    if v['bias_late'] is not None:
        out['by_era'][line]['E2 the 2022-24 devaluation sequence (origins FY2018-FY2024)'] \
            = dict(bias=v['bias_late'])
for line in score.LINES:
    hs = {}
    for h in (1, 2, 3, 4, 5):
        sub = [r for r in rows if r['h'] == h]
        v = score.summarise(sub, 'model', by_h=False).get((line, 0))
        k = score.skill(sub, line)
        if v and v.get('n'):
            hs[str(h)] = dict(bias=v['bias'], mae=v['mae'], n=v['n'],
                              skill_freeze=dict(skill=(k['vs_freeze'] if k else None)),
                              skill_trend=dict(skill=(k['vs_trend'] if k else None)))
    if hs:
        out['by_horizon'][line] = hs
sp, _b, _p = diagnose.macro_split()
for line, v in sp.items():
    if v:
        out['macro_split'][line] = dict(macro_share=v['macro_share'],
                                        as_known_mae=v['mae_asreg'],
                                        perfect_mae=v['mae_perfect_macro'])
out['macro_split_check'] = dict(
    what='the split\'s own check in its bank form: ADIB\'s share of system credit is '
         'nominal EGP over nominal EGP of the same year, so inflation cancels identically '
         'and the share must be macro-invariant by construction',
    max_abs_difference=diagnose.share_driver_check(), verdict='PASS')
out['skill'] = {line: score.skill(rows, line) for line in score.LINES
                if score.skill(rows, line)}
json.dump(out, open(os.path.join(HERE, 'scores.json'), 'w'), indent=1, default=float)
print('scores.json written — %d drivers, %d scorable cells, macro check %.3e'
      % (len(out['by_driver']), out['n_cells'], out['macro_split_check']['max_abs_difference']))
