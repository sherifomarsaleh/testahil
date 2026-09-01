"""ARCC walk-forward — scoring and skill, exactly as pre-registered.

Log error e = ln(projected / actual), per driver per horizon.  Bias, MAE,
share over-forecast, sign by era, and a MOVING-BLOCK BOOTSTRAP OVER ORIGINS at
block lengths {2,3,4} -- blocks over origins because horizons inside an origin
share an origin and are not independent.  A finding is robust only if its sign
holds at all three block lengths.

SIGN CASES ARE NEVER SILENTLY DROPPED.  Net profit changes sign in this history
(FY2020 is a loss of EGP 122.8mn), so the log is undefined for some cells.  They
are counted, listed and reported with their signed levels.  Dropping the loss
year would delete the single hardest thing this method had to forecast and would
flatter every statistic that survived it.
"""

import json
import math
import random

import bottom_up as B
import panel as P

random.seed(42)
BLOCKS = (2, 3, 4)
NBOOT = 2000
ERAS = {'E2 post-float': range(2017, 2022), 'E3 devaluation': range(2022, 2026)}


def era_of(year):
    for name, rng in ERAS.items():
        if year in rng:
            return name
    return 'E1 pre-float'


def logerr(p, a):
    if p is None or a is None:
        return None
    if p <= 0 or a <= 0:
        return None
    return math.log(p / a)


def build(knowable=True):
    """Every cell, for the build and for both naive benchmarks."""
    rows = []
    for o, h, y, proj, act in B.cells(knowable):
        fz, tr = B.freeze(o, h), B.trend(o, h)
        for d in B.DRIVERS:
            a = act.get(d)
            rows.append(dict(origin=o, h=h, year=y, driver=d,
                             proj=proj.get(d), actual=a,
                             e=logerr(proj.get(d), a),
                             e_freeze=logerr(fz.get(d), a),
                             e_trend=logerr(tr.get(d), a),
                             era=era_of(y),
                             sign_case=(proj.get(d) is not None and a is not None
                                        and (proj.get(d) <= 0 or a <= 0))))
    return rows


def _boot(vals_by_origin, block):
    """Moving-block bootstrap over origins."""
    origins = sorted(vals_by_origin)
    if len(origins) < block:
        return (None, None)
    starts = [i for i in range(len(origins) - block + 1)]
    need = math.ceil(len(origins) / block)
    out = []
    for _ in range(NBOOT):
        pool = []
        for _ in range(need):
            s = random.choice(starts)
            for o in origins[s:s + block]:
                pool.extend(vals_by_origin[o])
        if pool:
            out.append(sum(pool) / len(pool))
    if not out:
        return (None, None)
    out.sort()
    return (out[int(0.025 * len(out))], out[int(0.975 * len(out))])


def summarise(rows, field='e'):
    """Per driver, per horizon and pooled."""
    out = {}
    for d in B.DRIVERS:
        sub = [r for r in rows if r['driver'] == d]
        got = [r for r in sub if r[field] is not None]
        signs = [r for r in sub if r['sign_case']]
        rec = {'n': len(got), 'n_cells': len(sub), 'sign_cases': len(signs)}
        if got:
            es = [r[field] for r in got]
            rec['bias'] = sum(es) / len(es)
            rec['mae'] = sum(abs(x) for x in es) / len(es)
            rec['over'] = sum(1 for x in es if x > 0) / len(es)
            byo = {}
            for r in got:
                byo.setdefault(r['origin'], []).append(r[field])
            rec['ci'] = {b: _boot(byo, b) for b in BLOCKS}
            rec['robust'] = all(
                rec['ci'][b][0] is not None
                and (rec['ci'][b][0] > 0) == (rec['ci'][b][1] > 0)
                and (rec['ci'][b][0] > 0) == (rec['bias'] > 0)
                for b in BLOCKS)
            rec['by_h'] = {}
            for h in range(1, 6):
                hs = [r[field] for r in got if r['h'] == h]
                if hs:
                    rec['by_h'][h] = dict(n=len(hs), bias=sum(hs) / len(hs),
                                          mae=sum(abs(x) for x in hs) / len(hs))
            rec['by_era'] = {}
            for name in list(ERAS) + ['E1 pre-float']:
                xs = [r[field] for r in got if r['era'] == name]
                if xs:
                    rec['by_era'][name] = dict(n=len(xs), bias=sum(xs) / len(xs))
            eras = [v['bias'] for v in rec['by_era'].values()]
            rec['sign_stable'] = (len(eras) < 2) or all(x > 0 for x in eras) or all(x < 0 for x in eras)
        out[d] = rec
    return out


def skill(rows):
    """Beat 'no change'?  MAE of the build against each naive benchmark."""
    out = {}
    for d in B.DRIVERS:
        rec = {}
        for h in list(range(1, 6)) + ['all']:
            sub = [r for r in rows if r['driver'] == d
                   and (h == 'all' or r['h'] == h)
                   and r['e'] is not None and r['e_freeze'] is not None
                   and r['e_trend'] is not None]
            if not sub:
                continue
            m = lambda k: sum(abs(r[k]) for r in sub) / len(sub)
            rec[h] = dict(n=len(sub), mae=m('e'), mae_freeze=m('e_freeze'),
                          mae_trend=m('e_trend'),
                          beats_freeze=m('e') < m('e_freeze'),
                          beats_trend=m('e') < m('e_trend'))
        out[d] = rec
    return out


def macro_split():
    """The part of the error that disappears under perfect macro foresight.

    CARRIES ITS OWN NEGATIVE CONTROL: volume has no inflation and no FX term in
    its rule, so it MUST return a macro share of exactly zero.  If it does not,
    the split is wired wrong and the whole decomposition is void."""
    k = {(r['origin'], r['h'], r['driver']): r['e'] for r in build(True)}
    f = {(r['origin'], r['h'], r['driver']): r['e'] for r in build(False)}
    out = {}
    for d in B.DRIVERS:
        pairs = [(abs(k[key]), abs(f[key])) for key in k
                 if key[2] == d and k[key] is not None and f.get(key) is not None]
        if not pairs:
            continue
        mk = sum(x for x, _ in pairs) / len(pairs)
        mf = sum(y for _, y in pairs) / len(pairs)
        out[d] = dict(n=len(pairs), mae_knowable=mk, mae_foresight=mf,
                      macro_share=(mk - mf) / mk if mk > 0 else 0.0)
    ctrl = out.get('vol', {}).get('macro_share')
    if ctrl is None or abs(ctrl) > 1e-9:
        raise SystemExit('MACRO SPLIT IS WIRED WRONG: volume has no macro term '
                         'in its rule and must return a zero macro share by '
                         'construction; it returned %r. The decomposition is '
                         'void until this is fixed.' % ctrl)
    out['_negative_control'] = 'volume macro share = 0 exactly, as required'
    return out


if __name__ == '__main__':
    rows = build(True)
    s, sk, ms = summarise(rows), skill(rows), macro_split()
    # scores.json is written in the shape engine/lessons_harvest.py reads.
    # THE HARVESTER'S SELECTION RULES ARE FIXED AHEAD OF ANY RUN so they cannot
    # be tuned once its numbers are visible -- so the run emits the contract,
    # never the other way round.
    by_driver = {d: dict(robust_sign=bool(s[d].get('robust')),
                         bias=s[d].get('bias'), mae=s[d].get('mae'),
                         over=s[d].get('over'), n=s[d].get('n'))
                 for d in B.DRIVERS if s[d].get('n')}
    by_horizon = {}
    for d in B.DRIVERS:
        hs = {}
        for h in range(1, 6):
            r = sk.get(d, {}).get(h)
            if not r:
                continue
            sf = ((r['mae_freeze'] - r['mae']) / r['mae_freeze']) if r['mae_freeze'] else 0.0
            st = ((r['mae_trend'] - r['mae']) / r['mae_trend']) if r['mae_trend'] else 0.0
            hs[str(h)] = dict(n=r['n'], skill_freeze=dict(skill=sf),
                              skill_trend=dict(skill=st))
        if hs:
            by_horizon[d] = hs
    macro_split = {d: dict(macro_share=v['macro_share'],
                           as_known_mae=v['mae_knowable'],
                           perfect_mae=v['mae_foresight'])
                   for d, v in ms.items() if isinstance(v, dict)}
    by_era = {d: {nm: dict(bias=e['bias'], n=e['n'])
                  for nm, e in s[d].get('by_era', {}).items()}
              for d in B.DRIVERS if s[d].get('by_era')}
    json.dump({'by_driver': by_driver, 'by_horizon': by_horizon,
               'macro_split': macro_split, 'by_era': by_era,
               'cells': rows, 'summary': s, 'skill': sk, 'macro': ms},
              open('scores.json', 'w'), indent=1, default=str)

    print('=== PER-DRIVER LOG ERROR (build, knowable macro) ===')
    print('%-10s %4s %8s %8s %6s %7s %-8s %s' %
          ('driver', 'n', 'bias', 'MAE', 'over', 'signs', 'robust', 'era-stable'))
    for d in B.DRIVERS:
        r = s[d]
        if not r['n']:
            continue
        print('%-10s %4d %8.3f %8.3f %5.0f%% %7d %-8s %s' %
              (d, r['n'], r['bias'], r['mae'], 100 * r['over'], r['sign_cases'],
               'YES' if r['robust'] else 'no',
               'yes' if r['sign_stable'] else 'NO — unstable'))

    print('\n=== SKILL vs THE TWO NAIVE BENCHMARKS (MAE, pooled) ===')
    print('%-10s %4s %8s %8s %8s  %s' %
          ('driver', 'n', 'build', 'freeze', 'trend', 'verdict'))
    for d in B.DRIVERS:
        r = sk.get(d, {}).get('all')
        if not r:
            continue
        v = ('beats both' if r['beats_freeze'] and r['beats_trend'] else
             'beats freeze only' if r['beats_freeze'] else
             'beats trend only' if r['beats_trend'] else 'LOSES TO BOTH')
        print('%-10s %4d %8.3f %8.3f %8.3f  %s' %
              (d, r['n'], r['mae'], r['mae_freeze'], r['mae_trend'], v))

    print('\n=== MACRO vs COMPANY ===')
    print('%-10s %4s %9s %10s %8s' % ('driver', 'n', 'knowable', 'foresight', 'macro%'))
    for d in B.DRIVERS:
        r = ms.get(d)
        if not r:
            continue
        print('%-10s %4d %9.3f %10.3f %7.0f%%' %
              (d, r['n'], r['mae_knowable'], r['mae_foresight'], 100 * r['macro_share']))
    print('negative control:', ms['_negative_control'])
