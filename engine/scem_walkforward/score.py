#!/usr/bin/env python3
"""SCEM walk-forward — the score, exactly as pre-registered.

Log error e = ln(projected / actual), defined only where BOTH are strictly positive.
Where either crosses zero the cell is DROPPED AND COUNTED, and reported separately on a
signed relative error against the absolute actual — pretending a loss-making year is on
a log scale would be arithmetic wearing the costume of a measurement, and this company
lost money in three of its five years.
"""
import json
import math
import os
import random

import bottom_up as BU
import macro as M
import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(42)

ORIGINS = P.YEARS
HORIZONS = (1, 2, 3)
ERA = {"FY2021": "E1", "FY2022": "E1", "FY2023": "E2", "FY2024": "E2", "FY2025": "E2"}


def cells(projector=None, label='as_known'):
    """Every resolved (origin, horizon, driver) cell."""
    out = []
    for o in ORIGINS:
        proj = BU.project(o, HORIZONS) if projector is None else projector(o)
        for h in HORIZONS:
            p = proj.get(h)
            if p is None:
                continue
            a = BU.actual(p['year'])
            if a is None:
                continue                       # not matured
            for k in BU.DRIVERS:
                if k not in p or k not in a:
                    continue
                pv, av = p[k], a[k]
                cell = dict(origin=o, h=h, year=p['year'], driver=k,
                            projected=pv, actual=av, era=ERA[o], leg=label)
                if pv > 0 and av > 0:
                    cell['log_error'] = math.log(pv / av)
                    cell['scale'] = 'log'
                else:
                    cell['rel_error'] = ((pv - av) / abs(av)) if av else None
                    cell['scale'] = 'signed_relative'
                    cell['why_not_log'] = (
                        'the %s is not strictly positive in both legs (projected %.1f, '
                        'actual %.1f), so a log ratio is undefined' % (k, pv, av))
                out.append(cell)
    return out


def _boot(vals, blocks=(2, 3), n=2000):
    """Block bootstrap over origins. Blocks {2,3} only: with five origins a block of
    four leaves one degree of freedom and what it returns is not an interval."""
    if len(vals) < 3:
        return None
    lo_hi = {}
    for L in blocks:
        means = []
        nb = max(1, int(math.ceil(len(vals) / float(L))))
        for _ in range(n):
            s = []
            for _ in range(nb):
                i = random.randrange(0, max(1, len(vals) - L + 1))
                s.extend(vals[i:i + L])
            s = s[:len(vals)]
            if s:
                means.append(sum(s) / len(s))
        means.sort()
        lo_hi[L] = (means[int(0.025 * len(means))], means[int(0.975 * len(means))])
    lo = min(v[0] for v in lo_hi.values())
    hi = max(v[1] for v in lo_hi.values())
    return dict(lo=lo, hi=hi, by_block={str(k): v for k, v in lo_hi.items()},
                same_sign_across_blocks=all(v[0] * v[1] > 0 for v in lo_hi.values()))


def summarise(cs, scale='log'):
    key = 'log_error' if scale == 'log' else 'rel_error'
    by = {}
    for c in cs:
        if c.get('scale') != scale or c.get(key) is None:
            continue
        by.setdefault(c['driver'], []).append(c)
    out = {}
    for k, rows in sorted(by.items()):
        e = [r[key] for r in rows]
        n = len(e)
        bias = sum(e) / n
        mae = sum(abs(x) for x in e) / n
        over = sum(1 for x in e if x > 0) / float(n)
        eras = {}
        for r in rows:
            eras.setdefault(r['era'], []).append(r[key])
        era_bias = {k2: sum(v) / len(v) for k2, v in eras.items()}
        out[k] = dict(n=n, bias=bias, mae=mae, share_over=over,
                      share_under=1 - over,
                      by_era=era_bias,
                      era_sign_flips=(len(set(1 if v > 0 else -1
                                              for v in era_bias.values())) > 1),
                      by_horizon={str(h): (lambda v: sum(v) / len(v) if v else None)(
                          [r[key] for r in rows if r['h'] == h]) for h in HORIZONS},
                      ci=_boot(e))
    return out


def benchmark_mae(cs, which):
    """MAE of a naive benchmark on exactly the cells the model was scored on."""
    out = {}
    for c in cs:
        if c.get('scale') != 'log':
            continue
        o, h, k, av = c['origin'], c['h'], c['driver'], c['actual']
        b = BU.freeze(o)[h] if which == 'freeze' else (BU.trend(o) or {}).get(h)
        if b is None:
            out.setdefault(k, {}).setdefault('undefined', 0)
            out[k]['undefined'] += 1
            continue
        pv = b.get(k)
        if pv is None or pv <= 0 or av <= 0:
            out.setdefault(k, {}).setdefault('undefined', 0)
            out[k]['undefined'] += 1
            continue
        out.setdefault(k, {}).setdefault('e', []).append(abs(math.log(pv / av)))
    return {k: dict(mae=(sum(v['e']) / len(v['e'])) if v.get('e') else None,
                    n=len(v.get('e', [])), undefined=v.get('undefined', 0))
            for k, v in out.items()}


def skill_by_horizon(cs, which):
    """1 - MAE_model / MAE_benchmark, per horizon, on the cells both can score."""
    out = {}
    for h in HORIZONS:
        num, den = [], []
        for c in cs:
            if c.get('scale') != 'log' or c['h'] != h:
                continue
            o, k, av = c['origin'], c['driver'], c['actual']
            b = BU.freeze(o)[h] if which == 'freeze' else (BU.trend(o) or {}).get(h)
            if b is None:
                continue
            pv = b.get(k)
            if pv is None or pv <= 0 or av <= 0:
                continue
            num.append(abs(c['log_error']))
            den.append(abs(math.log(pv / av)))
        if num and sum(den):
            out[str(h)] = dict(n=len(num), model_mae=sum(num) / len(num),
                               benchmark_mae=sum(den) / len(den),
                               skill=1 - (sum(num) / len(num)) / (sum(den) / len(den)))
    return out


def macro_split(cs):
    """Re-run every origin on the outturn path and see how much of the miss goes."""
    def pf_inflation(o):
        return BU.project(o, HORIZONS, macro_override=lambda y: dict(
            cpi=M.outturn(y)['cpi'],
            real_gdp_growth=M.path(o, HORIZONS)[
                [h for h in HORIZONS if int(o[2:]) + h == y][0]]['real_gdp_growth']))

    def pf_both(o):
        return BU.project(o, HORIZONS, macro_override=lambda y: M.outturn(y))

    base = summarise(cs)
    infl = summarise(cells(pf_inflation, 'perfect_inflation'))
    both = summarise(cells(pf_both, 'perfect_both'))
    out = {}
    for k in base:
        b = base[k]['mae']
        out[k] = dict(
            mae_as_known=b,
            mae_perfect_inflation=infl.get(k, {}).get('mae'),
            mae_perfect_both=both.get(k, {}).get('mae'),
            macro_share_inflation=(None if not b or k not in infl
                                   else (b - infl[k]['mae']) / b),
            macro_share_both=(None if not b or k not in both
                              else (b - both[k]['mae']) / b))
    return out


if __name__ == '__main__':
    P.verify()
    cs = cells()
    logs = summarise(cs, 'log')
    rels = summarise(cs, 'signed_relative')
    rec = dict(cells=cs, log_scale=logs, signed_relative=rels,
               skill_vs_freeze=skill_by_horizon(cs, 'freeze'),
               skill_vs_trend=skill_by_horizon(cs, 'trend'),
               benchmark_freeze=benchmark_mae(cs, 'freeze'),
               benchmark_trend=benchmark_mae(cs, 'trend'),
               macro_split=macro_split(cs))
    json.dump(rec, open(os.path.join(HERE, 'scores.json'), 'w'), indent=1)
    json.dump(cs, open(os.path.join(HERE, 'error_cells.json'), 'w'), indent=1)

    print('LOG-SCALE DRIVERS  (bias<0 = the model forecast BELOW what happened)\n')
    print('%-18s %3s %8s %8s %8s  %-22s %s'
          % ('driver', 'n', 'bias', 'MAE', 'x', '95% block CI', 'era signs'))
    for k, v in sorted(logs.items(), key=lambda kv: kv[1]['bias']):
        ci = v['ci']
        cis = ('[%+.3f, %+.3f]%s' % (ci['lo'], ci['hi'],
                                     ' *' if ci['same_sign_across_blocks'] else '')
               ) if ci else 'n<3'
        eras = ' '.join('%s%+.2f' % (e, b) for e, b in sorted(v['by_era'].items()))
        print('%-18s %3d %+8.3f %8.3f %8.2f  %-22s %s%s'
              % (k, v['n'], v['bias'], v['mae'], math.exp(-v['bias']), cis, eras,
                 '  FLIPS' if v['era_sign_flips'] else ''))
    print('\nCELLS NOT ON A LOG SCALE (a sign change in one leg or both)\n')
    print('%-18s %3s %10s %10s' % ('driver', 'n', 'bias(rel)', 'MAE(rel)'))
    for k, v in sorted(rels.items()):
        print('%-18s %3d %+10.3f %10.3f' % (k, v['n'], v['bias'], v['mae']))
    print('\nSKILL AGAINST THE TWO NAIVE BENCHMARKS  (>0 = the method is better)\n')
    for name, sk in (('freeze', rec['skill_vs_freeze']), ('trend', rec['skill_vs_trend'])):
        print('  vs %-7s %s' % (name, '  '.join(
            'h%s n=%d skill %+0.3f' % (h, v['n'], v['skill']) for h, v in sorted(sk.items()))))
    print('\nMACRO vs COMPANY  (share of the miss that perfect foresight removes)\n')
    print('%-18s %10s %10s %10s' % ('driver', 'as known', 'infl PF', 'share'))
    for k, v in sorted(rec['macro_split'].items(),
                       key=lambda kv: -(kv[1]['macro_share_inflation'] or -9)):
        if v['mae_as_known'] is None:
            continue
        print('%-18s %10.3f %10s %9s'
              % (k, v['mae_as_known'],
                 '%.3f' % v['mae_perfect_inflation'] if v['mae_perfect_inflation'] else '-',
                 '%+.1f%%' % (100 * v['macro_share_inflation'])
                 if v['macro_share_inflation'] is not None else '-'))
