#!/usr/bin/env python3
"""ADIB (EGX) — score the FUNDAMENTAL walk-forward. Pre-registration §3.

Log error e = ln(projected / actual) where both are strictly positive. A line whose
projection and actual do not share a sign is recorded SIGN-BROKEN and reported by
count; it is never replaced by a signed percentage and never dropped silently.

Block bootstrap: the resampling unit is the WHOLE ORIGIN, because horizons inside an
origin share that origin's trailing window and are not independent. 10,000 resamples,
seed 20260909, percentile interval.
"""
from __future__ import annotations
import math, os, random, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, bottom_up as bu  # noqa: E402

LINES = ['fin_customers', 'cust_deposits', 'total_assets',
         'fin_income', 'cost_funds', 'net_funds', 'net_fees', 'other_nii',
         'admin', 'other_op', 'ecl', 'pbt', 'np', 'np_parent']

BS_LINES = {'fin_customers', 'cust_deposits', 'total_assets'}


def actual(y, f):
    if f in BS_LINES:
        return panel.BS[bu.fy(y)].get(f)
    if f == 'other_nii':
        return panel.other_nii(bu.fy(y))
    return panel.IS[bu.fy(y)].get(f)


def logerr(proj, act):
    """(e, status). status in {'ok','sign-broken','zero'}."""
    if proj is None or act is None:
        return None, 'missing'
    if act == 0 or proj == 0:
        return None, 'zero'
    if (proj > 0) != (act > 0):
        return None, 'sign-broken'
    return math.log(abs(proj) / abs(act)), 'ok'


def cells(origins=None, hmax=5, cpi_path_fn=None, credit_path_fn=None):
    """Every origin-horizon-line cell for the model and both benchmarks."""
    origins = origins or bu.ORIGINS
    rows = []
    for o in origins:
        kw = {}
        if cpi_path_fn:
            kw['cpi_path'] = cpi_path_fn(o, hmax)
        if credit_path_fn:
            kw['credit_path'] = credit_path_fn(o, hmax)
        m = bu.build(o, hmax, **kw)
        fz = bu.freeze(o, hmax)
        tr = bu.trend(o, hmax)
        if m is None:
            continue
        for h in range(1, hmax + 1):
            y = o + h
            if y > bu.LAST:
                continue
            for f in LINES:
                a = actual(y, f)
                for tag, src in (('model', m.get(y)), ('freeze', fz.get(y)),
                                 ('trend', tr.get(y))):
                    p = (src or {}).get(f)
                    e, st = logerr(p, a)
                    rows.append(dict(origin=o, h=h, year=y, line=f, method=tag,
                                     proj=p, actual=a, e=e, status=st))
    return rows


def _boot(vals_by_origin, stat, n=10000, seed=bu.BOOT_SEED):
    """Block bootstrap over ORIGINS. `vals_by_origin` = {origin: [values]}."""
    keys = sorted(vals_by_origin)
    if not keys:
        return None, None
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        pool = []
        for _ in range(len(keys)):
            pool += vals_by_origin[keys[rng.randrange(len(keys))]]
        if pool:
            out.append(stat(pool))
    if not out:
        return None, None
    out.sort()
    return out[int(0.05 * len(out))], out[int(0.95 * len(out)) - 1]


def summarise(rows, method='model', by_h=True):
    """bias, MAE, CI, over-share, sign-by-era, per line (and per horizon)."""
    res = {}
    keys = set()
    for r in rows:
        if r['method'] != method:
            continue
        keys.add((r['line'], r['h'] if by_h else 0))
    for line, h in sorted(keys):
        sel = [r for r in rows if r['method'] == method and r['line'] == line
               and (not by_h or r['h'] == h)]
        ok = [r for r in sel if r['status'] == 'ok']
        broken = sum(1 for r in sel if r['status'] == 'sign-broken')
        if not ok:
            res[(line, h)] = dict(n=0, sign_broken=broken)
            continue
        es = [r['e'] for r in ok]
        by_o = {}
        for r in ok:
            by_o.setdefault(r['origin'], []).append(r['e'])
        bias = sum(es) / len(es)
        mae = sum(abs(x) for x in es) / len(es)
        lo, hi = _boot(by_o, lambda p: sum(p) / len(p))
        mlo, mhi = _boot(by_o, lambda p: sum(abs(x) for x in p) / len(p))
        early = [r['e'] for r in ok if r['origin'] <= 2017]
        late = [r['e'] for r in ok if r['origin'] >= 2018]
        res[(line, h)] = dict(
            n=len(es), sign_broken=broken, bias=bias, mae=mae,
            bias_lo=lo, bias_hi=hi, mae_lo=mlo, mae_hi=mhi,
            over=sum(1 for x in es if x > 0) / len(es),
            bias_early=(sum(early) / len(early)) if early else None,
            bias_late=(sum(late) / len(late)) if late else None,
            stable=(bool(early) and bool(late)
                    and (sum(early) / len(early)) * (sum(late) / len(late)) > 0))
    return res


def skill(rows, line, h=None):
    """MAE of the model against each benchmark on the CELLS ALL THREE CAN SCORE.

    Comparing a model MAE computed on 45 cells with a benchmark MAE computed on 31 is
    not a skill measure, so the intersection is taken first and its size is reported.
    """
    def key(r):
        return (r['origin'], r['h'], r['line'])
    idx = {}
    for r in rows:
        if r['line'] != line or (h and r['h'] != h):
            continue
        idx.setdefault(key(r), {})[r['method']] = r
    common = [k for k, v in idx.items()
              if all(v.get(m, {}).get('status') == 'ok' for m in ('model', 'freeze', 'trend'))]
    if not common:
        return None
    out = dict(n=len(common))
    for m in ('model', 'freeze', 'trend'):
        es = [abs(idx[k][m]['e']) for k in common]
        out[m] = sum(es) / len(es)
    out['vs_freeze'] = 1.0 - out['model'] / out['freeze'] if out['freeze'] else None
    out['vs_trend'] = 1.0 - out['model'] / out['trend'] if out['trend'] else None
    by_o = {}
    for k in common:
        by_o.setdefault(k[0], []).append(abs(idx[k]['model']['e']) - abs(idx[k]['freeze']['e']))
    lo, hi = _boot(by_o, lambda p: sum(p) / len(p))
    out['model_minus_freeze_mae_ci'] = (lo, hi)
    return out


def main():
    rows = cells()
    json.dump(rows, open(os.path.join(HERE, 'error_cells.json'), 'w'), indent=0)
    print('cells: %d  (model %d / freeze %d / trend %d)  sign-broken %d  missing %d'
          % (len(rows), sum(1 for r in rows if r['method'] == 'model'),
             sum(1 for r in rows if r['method'] == 'freeze'),
             sum(1 for r in rows if r['method'] == 'trend'),
             sum(1 for r in rows if r['status'] == 'sign-broken'),
             sum(1 for r in rows if r['status'] == 'missing')))
    print()
    s = summarise(rows, 'model', by_h=False)
    print('%-15s %4s %8s %8s %18s %8s %8s %7s %7s %s'
          % ('driver', 'n', 'bias', 'MAE', 'bias 90% CI', 'early', 'late', 'over%', 'brk', 'stable'))
    for (line, _), v in sorted(s.items()):
        if not v.get('n'):
            print('%-15s %4d  (no scorable cells; sign-broken %d)' % (line, 0, v['sign_broken']))
            continue
        print('%-15s %4d %+8.3f %8.3f  [%+6.3f,%+6.3f] %+8.3f %+8.3f %7.0f %7d %s'
              % (line, v['n'], v['bias'], v['mae'], v['bias_lo'], v['bias_hi'],
                 v['bias_early'] if v['bias_early'] is not None else float('nan'),
                 v['bias_late'] if v['bias_late'] is not None else float('nan'),
                 100 * v['over'], v['sign_broken'], 'yes' if v['stable'] else 'NO'))
    print()
    print('SKILL — MAE, model vs both naive benchmarks, on cells all three can score')
    print('%-15s %4s %8s %8s %8s %10s %10s %s'
          % ('driver', 'n', 'model', 'freeze', 'trend', 'vs freeze', 'vs trend', 'm-f MAE 90% CI'))
    for line in LINES:
        k = skill(rows, line)
        if not k:
            print('%-15s  (no cells all three methods can score)' % line)
            continue
        lo, hi = k['model_minus_freeze_mae_ci']
        print('%-15s %4d %8.3f %8.3f %8.3f %9.0f%% %9.0f%%  [%+.3f,%+.3f]'
              % (line, k['n'], k['model'], k['freeze'], k['trend'],
                 100 * k['vs_freeze'], 100 * k['vs_trend'], lo, hi))
    return rows


if __name__ == '__main__':
    main()
