#!/usr/bin/env python3
"""GBCO walk-forward — scores.json, the file lessons_harvest.py reads.

Every figure here is computed from errors.json by score.py's own arithmetic; nothing is
typed. robust_sign is the CONJUNCTION of the block-bootstrap interval excluding zero AND
the sign holding at EVERY cut the data admits [R-FCAL-01 AMENDED 07-09-2026], re-run through
engine/valuation_calibration/boundary_sensitivity.cuts_for() rather than reimplemented.
"""
from __future__ import annotations
import collections, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'valuation_calibration'))
sys.path.insert(0, HERE)          # THIS run's score.py, not the calibration's
import score as S                                              # noqa: E402
import boundary_sensitivity as B                               # noqa: E402
assert hasattr(S, 'DRIVERS'), 'the wrong score module resolved — two modules share the name'


def main():
    rows = [r for r in json.load(open(os.path.join(HERE, 'errors.json')))
            if r.get('err') is not None]
    by_driver, by_horizon, by_era = {}, {}, {}
    for d in S.DRIVERS:
        sub = [r for r in rows if r['driver'] == d]
        if not sub:
            continue
        e = [r['err'] for r in sub]
        bias = sum(e) / len(e)
        pairs = [(r['origin'], r['err']) for r in sub]
        lo, hi = S.boot(pairs)
        # THE PRE-REGISTERED DECISION RULE ASKS A QUESTION THIS RUN WAS NOT ANSWERING.
        # score.boot() draws a block length at random from {2,3,4} per resample and
        # returns ONE pooled interval; decision_rule.is_robust() requires the interval
        # to exclude zero at EVERY block, and se_from_bootstrap() scales the correction
        # by the WIDEST of the three. A pooled interval cannot answer either, so the
        # rule read no standard error at all and declined every driver for want of
        # evidence — which is not the same finding as declining one ON evidence
        # [R-ENF-04]. Each block is now run and recorded separately, under the `boot`
        # key that rule reads, with the pooled interval kept beside it unchanged.
        boot = {}
        for _b in (2, 3, 4):
            _lo, _hi = S.boot(pairs, blocks=(_b,))
            boot[str(_b)] = {'lo': _lo, 'hi': _hi}
        cells = [(r['origin'] + r['h'], r['err']) for r in sub]
        cuts, flipped = B.cuts_for(cells)
        robust = bool(cuts) and not flipped and lo is not None and (lo > 0) == (hi > 0)
        by_driver[d] = {'bias': bias, 'mae': sum(abs(x) for x in e) / len(e),
                        'over': sum(1 for x in e if x > 0) / len(e), 'n': len(e),
                        'ci': [lo, hi], 'boot': boot,
                        'cuts': len(cuts), 'sign_flips': len(flipped),
                        'robust_sign': robust}
        by_horizon[d] = {}
        for h in S.HOR:
            hs = [r for r in sub if r['h'] == h]
            if not hs:
                continue
            mm = sum(abs(r['err']) for r in hs) / len(hs)
            fz = [abs(r['freeze']) for r in hs if r.get('freeze') is not None]
            tr = [abs(r['trend']) for r in hs if r.get('trend') is not None]
            by_horizon[d]['h%d' % h] = {
                'n': len(hs), 'mae': mm,
                'skill_freeze': {'skill': (1 - mm / (sum(fz) / len(fz))) if fz else None},
                'skill_trend': {'skill': (1 - mm / (sum(tr) / len(tr))) if tr else None}}
        # eras: the market's own boundaries — the 2016 float and the 2022-24 devaluations
        era = collections.defaultdict(list)
        for r in sub:
            y = r['origin'] + r['h']
            era['pre-float (<=2016)' if y <= 2016 else
                ('post-float 2017-2021' if y <= 2021 else 'devaluation cycle 2022-2025')
                ].append(r['err'])
        by_era[d] = {k: {'bias': sum(v) / len(v), 'n': len(v)}
                     for k, v in era.items() if len(v) >= 3}

    # macro split — revenue only; every other driver in this model has no inflation term
    macro = {}
    try:
        import macro_split as MS
        known, realised = MS.paths()
        ak, pf = [], []
        for r in rows:
            if r['driver'] != 'revenue' or r['origin'] not in known:
                continue
            try:
                kn = re_ = 1.0
                for y in range(r['origin'] + 1, r['origin'] + r['h'] + 1):
                    kn *= (1 + known[r['origin']][y]); re_ *= (1 + realised[y])
            except KeyError:
                continue
            ak.append(abs(r['err']))
            pf.append(abs(r['err'] + (math.log(re_) - math.log(kn))))
        if ak:
            m = sum(abs(a - b) for a, b in zip(ak, pf)) / len(ak)
            macro['revenue'] = {
                'as_known_mae': sum(ak) / len(ak), 'perfect_mae': sum(pf) / len(pf),
                'macro_share': m / (sum(ak) / len(ak)), 'n': len(ak)}
    except Exception as exc:                                   # reported, never swallowed
        macro['_error'] = str(exc)

    doc = {'_rule': '[R-FCAL-01] GBCO fundamental walk-forward, 07-09-2026',
           'ticker': 'GBCO', 'scope': 'full',
           'origins': S.ORIGINS, 'horizons': S.HOR, 'cells': len(rows),
           'by_driver': by_driver, 'by_horizon': by_horizon,
           'by_era': by_era, 'macro_split': macro}
    json.dump(doc, open(os.path.join(HERE, 'scores.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    for k, v in sorted(by_driver.items()):
        print('%-17s bias %+0.3f mae %0.3f n=%2d cuts=%d flips=%d robust=%s'
              % (k, v['bias'], v['mae'], v['n'], v['cuts'], v['sign_flips'], v['robust_sign']))
    print('\nmacro split:', json.dumps(macro.get('revenue'), indent=1))


if __name__ == '__main__':
    main()
