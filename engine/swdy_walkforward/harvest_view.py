"""The SHARED harvester's own shape, emitted from this run's own numbers.

engine/lessons_harvest.py reads scores.json BY KEY — by_driver / by_horizon /
macro_split / by_era, with `robust_sign`, `over`, `skill_freeze.skill`,
`macro_share`, `as_known_mae`, `perfect_mae` — and this run wrote `drivers`,
`skill_revenue` and a separate diagnostics.json. A reader that guesses a naming
convention silently finds nothing AND REPORTS THAT AS A RESULT [L-355]: the first
harvest of this run returned "0 candidate lessons", which is indistinguishable
from a run that taught nothing.

THE FIX IS TO EMIT THE SHARED SHAPE, NOT TO TEACH THE SHARED READER A NEW ONE. A
harvester carrying one adapter per run is five readers that drift; a run carrying
the reader's shape is one. Nothing is recomputed here — every figure is copied
from scores.json and diagnostics.json, which is why this file computes nothing.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SC = os.path.join(HERE, 'scores.json')
DG = os.path.join(HERE, 'diagnostics.json')


def main():
    S = json.load(open(SC))
    D = json.load(open(DG))
    drv = S['drivers']
    ci_holds = lambda c: bool(c) and ((c['lo'] > 0) == (c['hi'] > 0))

    by_driver, by_horizon, by_era = {}, {}, {}
    for k, r in drv.items():
        if not r.get('n'):
            continue
        by_driver[k] = dict(bias=r['bias'], mae=r['mae'], over=r['share_over'],
                            n=r['n'], n_cells=r['n'],
                            # ROBUST means the bootstrap interval does not cover zero
                            # AND the sign survives every admissible cut, which is the
                            # amended test rather than the era boundary alone.
                            robust_sign=(ci_holds(r.get('ci'))
                                         and not D['stability'].get(k, {}).get('flips')
                                         and bool(D['stability'].get(k, {}).get('n_cuts'))))
        hs = {}
        for h, v in (r.get('by_horizon') or {}).items():
            hs[str(h)] = dict(bias=v['bias'], mae=v['mae'], n=v['n'])
        for h, v in (S.get('skill_revenue') if k == 'A_revenue'
                     else S.get('skill_gross_profit') if k == 'A_gross_profit'
                     else {}).items():
            if str(h) in hs and v.get('skill_vs_freeze') is not None:
                hs[str(h)]['skill_freeze'] = dict(skill=v['skill_vs_freeze'])
        # every other driver carries its POOLED skill at every horizon it scored,
        # because the run computes skill per driver pooled and per horizon only on
        # the two aggregates; a horizon with no skill figure carries none rather
        # than inheriting one.
        if k not in ('A_revenue', 'A_gross_profit') and r.get('skill_vs_freeze') is not None:
            for h in hs:
                hs[h]['skill_freeze'] = dict(skill=r['skill_vs_freeze'])
        if hs:
            by_horizon[k] = hs
        if r.get('by_era'):
            by_era[k] = {nm: dict(bias=v['bias'], n=v['n'])
                         for nm, v in r['by_era'].items()}

    macro_split = {}
    for k, m in (D.get('macro_split') or {}).items():
        macro_split[k] = dict(macro_share=m.get('macro_share_inflation') or 0.0,
                              as_known_mae=drv.get(k, {}).get('mae'),
                              perfect_mae=drv.get(k, {}).get('mae'))
    S.update(by_driver=by_driver, by_horizon=by_horizon, by_era=by_era,
             macro_split=macro_split,
             _harvest_view='emitted by harvest_view.py in the shape '
                           'engine/lessons_harvest.py reads; nothing here is recomputed')
    json.dump(S, open(SC, 'w'), indent=1)
    print('harvest view: %d drivers, %d with a horizon skill, %d with eras'
          % (len(by_driver), len(by_horizon), len(by_era)))


if __name__ == '__main__':
    main()
