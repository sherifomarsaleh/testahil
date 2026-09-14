#!/usr/bin/env python3
"""GBCO walk-forward — mechanical build at every origin, and the score.

Every rule here is the one written in PRE_REGISTRATION_07-09-2026.md before a single
error was computed. Nothing is fitted. The two naive benchmarks are computed on the same
cells so the skill comparison is like for like.
"""
from __future__ import annotations
import json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, 'panel.json')
ORIGINS = list(range(2016, 2025))
HOR = [1, 2, 3, 4, 5]
LAST = 2025


def load():
    d = json.load(open(PANEL, encoding='utf-8'))['years']
    out = {}
    for y, b in d.items():
        v = dict(b['is'])
        y = int(y)
        v['sga'] = (v.get('selling') or 0) + (v.get('admin') or 0)
        if v.get('revenue'):
            v['gross_margin'] = v['gross_profit'] / v['revenue']
            v['sga_ratio'] = -v['sga'] / v['revenue']
            v['oi_ratio'] = (v.get('other_income') or 0) / v['revenue']
            v['prov_ratio'] = -(v.get('provisions') or 0) / v['revenue']
            v['fin_ratio'] = -(v.get('finance_net') or 0) / v['revenue']
        out[y] = v
    return out


def cagr(a, b, n):
    if a is None or b is None or a <= 0 or b <= 0 or n <= 0:
        return None
    return (b / a) ** (1.0 / n) - 1.0


def mean3(P, t, key):
    xs = [P[y].get(key) for y in (t - 2, t - 1, t) if y in P and P[y].get(key) is not None]
    return sum(xs) / len(xs) if xs else None


TAX = lambda y: 0.225 if y >= 2015 else 0.25


def project(P, t):
    """The pre-registered mechanical model at origin t. Sees only years <= t."""
    rev0 = P[t]['revenue']
    g3 = cagr(P[t - 3]['revenue'], rev0, 3) if (t - 3) in P else None
    span = min(5, t - min(P))
    gL = cagr(P[t - span]['revenue'], rev0, span) if (t - span) in P else None
    if g3 is None or gL is None:
        return None
    gm = mean3(P, t, 'gross_margin')
    sga = mean3(P, t, 'sga_ratio')
    oi = mean3(P, t, 'oi_ratio')
    pv = mean3(P, t, 'prov_ratio')
    fr = mean3(P, t, 'fin_ratio')
    out, rev = {}, rev0
    for h in HOR:
        w = 0.8 ** (h - 1)
        g = w * g3 + (1 - w) * gL
        rev = rev * (1 + g)
        gp = rev * gm
        op = gp - rev * sga + rev * oi - rev * pv
        fin = rev * fr
        np_ = (op - fin) * (1 - TAX(t + h))
        out[h] = {'revenue': rev, 'gross_profit': gp, 'gross_margin': gm,
                  'operating_profit': op, 'finance_cost': fin, 'net_profit': np_,
                  'sga': rev * sga}
    return out


def freeze(P, t):
    a = P[t]
    base = {'revenue': a['revenue'], 'gross_profit': a['gross_profit'],
            'gross_margin': a['gross_margin'], 'operating_profit': a['operating_profit'],
            'finance_cost': -(a.get('finance_net') or 0), 'net_profit': a.get('net_profit'),
            'sga': -a['sga']}
    return {h: dict(base) for h in HOR}


def trend(P, t):
    g = cagr(P[t - 3]['revenue'], P[t]['revenue'], 3) if (t - 3) in P else None
    if g is None:
        return None
    out = {}
    for h in HOR:
        f = (1 + g) ** h
        out[h] = {k: (None if v is None else v * f) for k, v in freeze(P, t)[1].items()}
        out[h]['gross_margin'] = P[t]['gross_margin']
    return out


def actual(P, y):
    a = P.get(y)
    if not a:
        return None
    return {'revenue': a['revenue'], 'gross_profit': a['gross_profit'],
            'gross_margin': a['gross_margin'], 'operating_profit': a['operating_profit'],
            'finance_cost': -(a.get('finance_net') or 0), 'net_profit': a.get('net_profit'),
            'sga': -a['sga']}


DRIVERS = ['revenue', 'gross_margin', 'gross_profit', 'sga', 'operating_profit',
           'finance_cost', 'net_profit']


def cells():
    P = load()
    rows = []
    for t in ORIGINS:
        m, f, tr = project(P, t), freeze(P, t), trend(P, t)
        if m is None:
            continue
        for h in HOR:
            y = t + h
            if y > LAST:
                continue
            a = actual(P, y)
            for d in DRIVERS:
                av, mv = a.get(d), m[h].get(d)
                if av is None or mv is None:
                    continue
                if av <= 0 or mv <= 0:
                    rows.append(dict(origin=t, h=h, driver=d, actual=av, model=mv,
                                     err=None, sign_only=True))
                    continue
                r = dict(origin=t, h=h, driver=d, actual=av, model=mv,
                         err=math.log(mv / av))
                for nm, bench in (('freeze', f), ('trend', tr)):
                    bv = bench[h].get(d) if bench else None
                    r[nm] = math.log(bv / av) if (bv and bv > 0) else None
                rows.append(r)
    return rows


def boot(xs, blocks=(2, 3, 4), n=2000, seed=42):
    """Block bootstrap over ORIGINS — cells inside one origin are not independent."""
    if len(xs) < 3:
        return None, None
    rnd = random.Random(seed)
    keys = sorted({o for o, _ in xs})
    by = {k: [v for o, v in xs if o == k] for k in keys}
    out = []
    for _ in range(n):
        b = rnd.choice(blocks)
        vals = []
        while len(vals) < len(keys):
            i = rnd.randrange(len(keys))
            for k in keys[i:i + b]:
                vals.extend(by[k])
        m = [v for v in vals[:sum(len(by[k]) for k in keys)]]
        if m:
            out.append(sum(m) / len(m))
    out.sort()
    return out[int(0.025 * len(out))], out[int(0.975 * len(out))]


def main():
    rows = cells()
    json.dump(rows, open(os.path.join(HERE, 'errors.json'), 'w'), indent=1)
    print('GBCO FUNDAMENTAL walk-forward — scored cells: %d\n' % len(rows))
    print('%-17s %2s %4s %8s %8s %18s %9s %9s' %
          ('driver', 'h', 'n', 'bias', 'MAE', '95% block-bootstrap', 'freeze', 'trend'))
    for d in DRIVERS:
        for h in HOR:
            sub = [r for r in rows if r['driver'] == d and r['h'] == h and r.get('err') is not None]
            if not sub:
                continue
            e = [r['err'] for r in sub]
            bias = sum(e) / len(e)
            mae = sum(abs(x) for x in e) / len(e)
            lo, hi = boot([(r['origin'], r['err']) for r in sub])
            fz = [abs(r['freeze']) for r in sub if r.get('freeze') is not None]
            tr = [abs(r['trend']) for r in sub if r.get('trend') is not None]
            fzm = sum(fz) / len(fz) if fz else float('nan')
            trm = sum(tr) / len(tr) if tr else float('nan')
            print('%-17s %2d %4d %+8.3f %8.3f  [%+7.3f,%+7.3f] %9.3f %9.3f%s%s'
                  % (d, h, len(e), bias, mae, lo or float('nan'), hi or float('nan'),
                     fzm, trm,
                     '  BEATS-FREEZE' if mae < fzm else '  loses-to-freeze',
                     ' BEATS-TREND' if mae < trm else ' loses-to-trend'))
        print()


if __name__ == '__main__':
    main()
