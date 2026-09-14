"""Score every driver at every origin-horizon cell, against both naive benchmarks.

log error e = ln(projected / actual). A cell whose actual is zero, negative or absent is
NOT SCORED AND IS COUNTED, because a denominator that quietly shrinks is how a bad driver
looks good.

Block bootstrap over ORIGINS, block lengths {2,3,4}, 2000 resamples, seed 42 — all
pre-registered.
"""
import json, os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B

OUT = os.path.join(HERE, 'scores.json')
CELLS = os.path.join(HERE, 'error_cells.json')
DRIVERS = ['D1_cable_volume_t', 'D2_cable_price_t', 'D3_cable_cost_t',
           'D4_cables_revenue', 'D5_contracting_revenue', 'D6_other_revenue',
           'D7_cables_cost', 'D8_contracting_cost', 'D9_other_cost',
           'D10_sga', 'D11_depreciation', 'D12_capex',
           'D13_other_operating_income', 'D14_other_operating_expense',
           'D15_finance_costs', 'D16_finance_income',
           'A_revenue', 'A_cost_of_revenue', 'A_gross_profit']
# The eras are named in the pre-registration, cut at the two Egyptian devaluations.
def era(target):
    if target <= 2016:
        return 'pre-float'
    if target <= 2021:
        return 'first float'
    return 'second float'


def freeze(o, key):
    a = B.actual(o)
    return a.get(key)


def trend(o, key):
    """Trailing CAGR over the longest window available at o, capped at three years."""
    vals = []
    for y in range(o - 3, o + 1):
        v = B.actual(y).get(key)
        if v is None or v <= 0:
            return None, 0
        vals.append(v)
    if len(vals) < 2:
        return None, 0
    n = len(vals) - 1
    g = (vals[-1] / vals[0]) ** (1.0 / n) - 1.0
    return vals[-1], n, g


def build_cells(w_metal=B.W_METAL):
    cells, skipped = [], []
    for o in B.ORIGINS:
        proj_cache = {h: B.project(o, h, w_metal)[0] for h in B.HORIZONS}
        for h in B.HORIZONS:
            t = o + h
            if t > 2025:
                continue
            act = B.actual(t)
            pr = proj_cache[h]
            fz = B.actual(o)
            tr = {}
            for k in DRIVERS:
                r = trend(o, k)
                if r and r[0]:
                    tr[k] = r[0] * (1 + r[2]) ** h
            for k in DRIVERS:
                a, p = act.get(k), pr.get(k)
                if a is None or a <= 0 or p is None or p <= 0:
                    skipped.append(dict(origin=o, h=h, target=t, driver=k,
                                        why='actual absent or not positive' if (a is None or a <= 0)
                                            else 'projection absent or not positive'))
                    continue
                # `setting` is carried so the SHARED boundary-sensitivity instrument
                # can read this run through a NAMED adapter of the shape it already
                # uses for the other five, rather than guessing [R-ENF-03].
                cell = dict(origin=o, h=h, target=t, driver=k, era=era(t),
                            setting='asknown', projected=p, actual=a, e=math.log(p / a))
                f = fz.get(k)
                if f and f > 0:
                    cell['freeze'] = f
                    cell['e_freeze'] = math.log(f / a)
                if tr.get(k) and tr[k] > 0:
                    cell['trend'] = tr[k]
                    cell['e_trend'] = math.log(tr[k] / a)
                cells.append(cell)
    return cells, skipped


def block_bootstrap(cells, key='e', blocks=(2, 3, 4), n=2000, seed=42):
    """Moving-block bootstrap over ORIGINS. Returns the union interval across blocks."""
    by_o = {}
    for c in cells:
        by_o.setdefault(c['origin'], []).append(c[key])
    os_ = sorted(by_o)
    if len(os_) < 2:
        return None
    rng = random.Random(seed)
    lo, hi = [], []
    for L in blocks:
        if L > len(os_):
            continue
        means = []
        nb = max(1, len(os_) // L)
        for _ in range(n):
            samp = []
            for _ in range(nb):
                s = rng.randrange(0, len(os_) - L + 1)
                for oo in os_[s:s + L]:
                    samp.extend(by_o[oo])
            if samp:
                means.append(sum(samp) / len(samp))
        means.sort()
        lo.append(means[int(0.025 * len(means))])
        hi.append(means[int(0.975 * len(means))])
    if not lo:
        return None
    return dict(lo=min(lo), hi=max(hi), blocks=list(blocks), resamples=n, seed=seed)


def summarise(cells, skipped):
    out = {}
    for k in DRIVERS:
        cs = [c for c in cells if c['driver'] == k]
        if not cs:
            out[k] = dict(n=0, unscoreable=sum(1 for s in skipped if s['driver'] == k))
            continue
        es = [c['e'] for c in cs]
        bias = sum(es) / len(es)
        mae = sum(abs(e) for e in es) / len(es)
        ci = block_bootstrap(cs)
        byh, byera = {}, {}
        for h in B.HORIZONS:
            hh = [c['e'] for c in cs if c['h'] == h]
            if hh:
                byh[h] = dict(n=len(hh), bias=sum(hh) / len(hh),
                              mae=sum(abs(e) for e in hh) / len(hh))
        for e_ in ('pre-float', 'first float', 'second float'):
            ee = [c['e'] for c in cs if c['era'] == e_]
            if ee:
                byera[e_] = dict(n=len(ee), bias=sum(ee) / len(ee))
        fz = [c for c in cs if 'e_freeze' in c]
        tr = [c for c in cs if 'e_trend' in c]
        out[k] = dict(
            n=len(cs), unscoreable=sum(1 for s in skipped if s['driver'] == k),
            bias=bias, mae=mae, ci=ci,
            share_over=sum(1 for e in es if e > 0) / len(es),
            by_horizon=byh, by_era=byera,
            mae_freeze=(sum(abs(c['e_freeze']) for c in fz) / len(fz)) if fz else None,
            mae_trend=(sum(abs(c['e_trend']) for c in tr) / len(tr)) if tr else None,
            skill_vs_freeze=((sum(abs(c['e_freeze']) for c in fz) / len(fz)
                              - sum(abs(c['e']) for c in fz) / len(fz))
                             / (sum(abs(c['e_freeze']) for c in fz) / len(fz))) if fz else None,
            skill_vs_trend=((sum(abs(c['e_trend']) for c in tr) / len(tr)
                             - sum(abs(c['e']) for c in tr) / len(tr))
                            / (sum(abs(c['e_trend']) for c in tr) / len(tr))) if tr else None)
    return out


def skill_by_horizon(cells, key):
    out = {}
    for h in B.HORIZONS:
        cs = [c for c in cells if c['driver'] == key and c['h'] == h and 'e_freeze' in c]
        if not cs:
            continue
        mm = sum(abs(c['e']) for c in cs) / len(cs)
        mf = sum(abs(c['e_freeze']) for c in cs) / len(cs)
        tr = [c for c in cs if 'e_trend' in c]
        mt = (sum(abs(c['e_trend']) for c in tr) / len(tr)) if tr else None
        out[h] = dict(n=len(cs), mae=mm, mae_freeze=mf, mae_trend=mt,
                      skill_vs_freeze=(mf - mm) / mf if mf else None,
                      skill_vs_trend=((mt - mm) / mt) if mt else None)
    return out


def main():
    cells, skipped = build_cells()
    summ = summarise(cells, skipped)
    sens = {}
    for w in (0.5, 0.7, 0.9):
        cw, sw = build_cells(w)
        sens['w=%.1f' % w] = {k: dict(bias=summarise(cw, sw)[k]['bias'],
                                      mae=summarise(cw, sw)[k]['mae'],
                                      n=summarise(cw, sw)[k]['n'])
                              for k in ('A_revenue', 'A_gross_profit', 'D4_cables_revenue',
                                        'D7_cables_cost')}
    out = dict(_='SWDY fundamental walk-forward scores. INTERNAL.', built='2026-09-07',
               w_metal=B.W_METAL, origins=B.ORIGINS, horizons=list(B.HORIZONS),
               n_cells=len(cells), n_unscoreable=len(skipped),
               drivers=summ,
               skill_revenue=skill_by_horizon(cells, 'A_revenue'),
               skill_gross_profit=skill_by_horizon(cells, 'A_gross_profit'),
               sensitivity_w=sens)
    json.dump(out, open(OUT, 'w'), indent=1)
    json.dump(dict(cells=cells, skipped=skipped), open(CELLS, 'w'), indent=1)
    print('scored %d cells, %d unscoreable' % (len(cells), len(skipped)))
    print('%-28s %4s %8s %8s %20s %8s %8s' % ('driver', 'n', 'bias', 'MAE', '95% CI',
                                              'vsFRZ', 'vsTRD'))
    for k in DRIVERS:
        d = summ[k]
        if not d.get('n'):
            print('%-28s %4d  — not scoreable —' % (k, 0))
            continue
        ci = d['ci']
        print('%-28s %4d %8.3f %8.3f  [%7.3f,%7.3f] %7s %7s' % (
            k, d['n'], d['bias'], d['mae'], ci['lo'] if ci else float('nan'),
            ci['hi'] if ci else float('nan'),
            ('%+.1f%%' % (100 * d['skill_vs_freeze'])) if d['skill_vs_freeze'] is not None else '—',
            ('%+.1f%%' % (100 * d['skill_vs_trend'])) if d['skill_vs_trend'] is not None else '—'))
    return out


if __name__ == '__main__':
    main()
