"""The macro-versus-company split, and the cut-invariant stability test.

THE SPLIT. Every origin is re-run (a) on the macro path KNOWN at the origin, which is
the base run, and (b) on PERFECT FORESIGHT of the same series — the inflation, currency
and activity that actually happened. The difference is the macro share; the residual is
the company share.

THE SPLIT CARRIES ITS OWN CHECK: a driver with no inflation term must return a ZERO
inflation-macro share by construction. D1, cable volume, is escalated on real GDP alone
and carries no CPI or FX term, so re-running it on perfect-foresight INFLATION must move
it by exactly nothing. If it moves, the split is wrong rather than interesting.

THE STABILITY TEST is [R-FCAL-01 AMENDED 07-09-2026]: the sign must hold at EVERY cut
the data admits, not at the market's own currency boundary. The arithmetic is IMPORTED
from engine/valuation_calibration/boundary_sensitivity.py rather than reimplemented — a
checker that models a measurement is checking a different measurement [R-ENF-03].
"""
import json, os, sys, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ENG, 'valuation_calibration'))
import bottom_up as B
import score as S
from boundary_sensitivity import cuts_for, MIN_SIDE

OUT = os.path.join(HERE, 'diagnostics.json')


def project_foresight(o, h, which):
    """The same rules, on the path that ACTUALLY happened rather than the one known at o.

    `which` names the series given foresight: 'inflation' (CPI and the currency, which
    move together through relative purchasing power), 'activity' (real GDP), or 'all'.
    """
    p_known = B.paths(o)
    t = o + h

    def realised(series, start, end):
        a, b = B.m(series, start), B.m(series, end)
        if a in (None, 0) or b is None:
            return None
        return (b / a) ** (1.0 / max(end - start, 1)) - 1.0

    p = dict(p_known)
    if which in ('inflation', 'all'):
        cpi = realised('cpi_index', o, t)
        fx = realised('egp_usd', o, t)
        if cpi is not None:
            p['cpi'] = cpi
        if fx is not None:
            p['fx'] = fx
    if which in ('activity', 'all'):
        gs = [B.m('gdp_g', y) for y in range(o + 1, t + 1)]
        gs = [g for g in gs if g is not None]
        if gs:
            p['gdp'] = sum(gs) / len(gs) / 100.0
    saved = B.paths
    B.paths = lambda oo, _p=p: _p
    try:
        d, _ = B.project(o, h)
    finally:
        B.paths = saved
    return d


def macro_split():
    cells, _ = S.build_cells()
    rows = []
    for c in cells:
        o, h, k, a = c['origin'], c['h'], c['driver'], c['actual']
        out = dict(origin=o, h=h, driver=k, e_known=c['e'])
        for which in ('inflation', 'activity', 'all'):
            d = project_foresight(o, h, which)
            p = d.get(k)
            out['e_' + which] = math.log(p / a) if (p and p > 0) else None
        rows.append(out)
    agg = {}
    for k in S.DRIVERS:
        rs = [r for r in rows if r['driver'] == k and r['e_all'] is not None]
        if not rs:
            continue
        ek = sum(r['e_known'] for r in rs) / len(rs)
        ei = sum(r['e_inflation'] for r in rs) / len(rs)
        ea = sum(r['e_all'] for r in rs) / len(rs)
        agg[k] = dict(n=len(rs), bias_as_known=ek, bias_perfect_inflation=ei,
                      bias_perfect_all=ea,
                      macro_share_inflation=(ek - ei) / ek if ek else None,
                      macro_share_all=(ek - ea) / ek if ek else None,
                      company_share=ea / ek if ek else None)
    return agg, rows


def stability():
    """Every admissible cut, per driver, through the SHARED instrument."""
    raw = json.load(open(os.path.join(HERE, 'error_cells.json')))['cells']
    by = collections.defaultdict(list)
    for r in raw:
        by[r['driver']].append((int(r['target']), float(r['e'])))
    out = {}
    for drv, cells in sorted(by.items()):
        cuts, flipped = cuts_for(cells)
        out[drv] = dict(n=len(cells), n_cuts=len(cuts),
                        cuts=[dict(boundary=b, before=a, after=c) for b, a, c in cuts],
                        flips=[dict(boundary=b, before=a, after=c) for b, a, c in flipped],
                        verdict=('UNTESTABLE — no cut leaves %d cells each side' % MIN_SIDE
                                 if not cuts else
                                 'SIGN FLIPS at %d of %d cuts — an instability, not a bias'
                                 % (len(flipped), len(cuts)) if flipped else
                                 'sign survives all %d cuts' % len(cuts)))
    return out


def main():
    agg, rows = macro_split()
    st = stability()
    # THE SPLIT'S OWN CHECK
    v = agg.get('D1_cable_volume_t')
    check = None
    if v:
        ok = abs(v['macro_share_inflation']) < 1e-9
        check = dict(driver='D1_cable_volume_t',
                     macro_share_inflation=v['macro_share_inflation'],
                     verdict='PASS — a volume driver carries no inflation term and moved '
                             'by exactly nothing under perfect-foresight inflation' if ok
                             else 'FAIL — a volume driver moved under perfect-foresight '
                                  'inflation, so the split is wrong rather than interesting')
    out = dict(_='SWDY walk-forward diagnostics. INTERNAL.', built='2026-09-07',
               macro_split=agg, split_own_check=check, stability=st)
    json.dump(out, open(OUT, 'w'), indent=1)

    print('MACRO vs COMPANY (share of the as-known bias removed by perfect foresight)')
    print('%-28s %4s %9s %9s %9s %9s' % ('driver', 'n', 'as-known', 'perf infl',
                                         'perf all', 'macro%'))
    for k in S.DRIVERS:
        d = agg.get(k)
        if not d:
            continue
        print('%-28s %4d %9.3f %9.3f %9.3f %8.1f%%' % (
            k, d['n'], d['bias_as_known'], d['bias_perfect_inflation'],
            d['bias_perfect_all'], 100 * (d['macro_share_all'] or 0)))
    print('\nSPLIT CHECK: %s' % (check['verdict'] if check else 'not computable'))
    print('\nCUT-INVARIANT STABILITY [R-FCAL-01 AMENDED 07-09-2026]')
    for k in S.DRIVERS:
        d = st.get(k)
        if not d:
            continue
        print('  %-28s %s' % (k, d['verdict']))
    return out


if __name__ == '__main__':
    main()
