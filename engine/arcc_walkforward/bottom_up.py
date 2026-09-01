"""ARCC walk-forward — the ground-up build at every origin.

Implements PRE_REGISTRATION_01-09-2026.md §1 exactly and nothing else.  Every
rule is arithmetic on figures published by the origin date; there is no
judgement driver anywhere in this file, because the exercise tests the METHOD,
not the analyst.

POINT-IN-TIME IS ENFORCED, NOT TRUSTED: `visible()` refuses any year after the
origin, so a rule cannot reach forward even by accident.
"""

import math
import panel as P

W_RAW = 0.79          # note-5 raw-material share of cash cost. Stated, not fitted.
TAX_RATE = 0.225      # Egypt statutory corporate rate, in force at every origin.

M = P.macro()


def visible(origin, year):
    if year > origin:
        raise AssertionError('POINT-IN-TIME VIOLATION: origin %d reached %d'
                             % (origin, year))
    return year


def _cagr(series, origin, n=3):
    """Trailing n-year CAGR of a series, using only years <= origin."""
    a, b = origin - n, origin
    if a not in series or b not in series:
        return 0.0
    va, vb = series[visible(origin, a)], series[visible(origin, b)]
    if va is None or vb is None or va <= 0 or vb <= 0:
        return 0.0
    return (vb / va) ** (1.0 / n) - 1.0


def seg_rev(y):
    return P.OPS[y]['rev_seg'] * 1e6


def other_rev(y):
    """Non-cement revenue: group sales less the cement segment [B-1]."""
    return P.IS[y]['sales'] - seg_rev(y)


def rev_per_tonne(y):
    return seg_rev(y) / (P.OPS[y]['vol_total'] * 1e3)


def cost_per_tonne(y):
    return P.OPS[y]['cash_cost'] * 1e6 / (P.OPS[y]['vol_total'] * 1e3)


def export_share(y):
    o = P.OPS[y]
    if o.get('vol_exp') is None:
        return 0.10
    return o['vol_exp'] / o['vol_total']


def macro_path(origin, h, knowable=True):
    """CPI and FX-depreciation for horizon h.

    KNOWABLE  = the last realised move at the origin, carried flat: what could
                have been believed on the day.  This is the production run.
    FORESIGHT = the realised path.  Used only to split macro from company error.
    """
    if knowable:
        cpi = M['cpi_pct'][visible(origin, origin)] / 100.0
        fxa, fxb = M['egp_usd'][origin - 1], M['egp_usd'][visible(origin, origin)]
        fx = fxb / fxa - 1.0
        return cpi, fx
    y = origin + h
    cpi = M['cpi_pct'].get(y, M['cpi_pct'][origin]) / 100.0
    a, b = M['egp_usd'].get(y - 1), M['egp_usd'].get(y)
    fx = (b / a - 1.0) if (a and b) else 0.0
    return cpi, fx


def capacity(origin):
    """Cement capacity implied by the origin's own disclosed utilisation."""
    for y in range(origin, 2013, -1):
        pr = P.PRODUCTION.get(y)
        if pr and pr.get('cem_util'):
            return pr['cement'] / pr['cem_util']
    return None


def project(origin, h, knowable=True):
    """One origin, one horizon, every driver.  Returns the full income statement."""
    nat = {y: v['national'] for y, v in P.MARKET.items() if y <= origin}
    g_nat = _cagr(nat, origin) if len(nat) >= 4 else 0.0

    # D1 volume — exogenous anchor, capped at disclosed capacity (amendment A-1)
    share = P.ACC_VOL[origin]['dom'] / P.MARKET[origin]['national']
    dom = P.MARKET[origin]['national'] * (1 + g_nat) ** h * share
    rest = P.ACC_VOL[origin]['rest']
    vol = dom + rest                                                   # kt
    cap = capacity(origin)
    if cap:
        vol = min(vol, cap)

    # D2 price / D3 cost — one escalator per driver class
    w_exp = export_share(origin)
    rpt, cpt = rev_per_tonne(origin), cost_per_tonne(origin)
    other = other_rev(origin)
    for k in range(1, h + 1):
        cpi, fx = macro_path(origin, k, knowable)
        rpt *= (1 - w_exp) * (1 + cpi) + w_exp * (1 + fx)
        cpt *= W_RAW * (1 + fx) + (1 - W_RAW) * (1 + cpi)
        other *= (1 + cpi)                                            # D4

    seg = vol * 1e3 * rpt
    sales = seg + other
    cash_cost = vol * 1e3 * cpt
    dna = P.OPS[origin]['dna'] * 1e6                                  # D6, flat [L-028]
    cogs = cash_cost + dna
    ga = (P.IS[origin]['ga'] / P.IS[origin]['sales']) * sales         # D5

    # D7 finance costs — from the borrowings that actually bear interest [L-002]
    d0, d1 = P.DEBT_SERIES[origin - 1] * 1e6, P.DEBT_SERIES[origin] * 1e6
    base = (d0 + d1) / 2.0
    rate = (P.IS[origin]['fin'] / base) if base > 0 else 0.0
    reds = [max(0.0, (P.DEBT_SERIES[y - 1] - P.DEBT_SERIES[y]) * 1e6)
            for y in range(origin - 2, origin + 1)]
    amort = sum(reds) / len(reds)
    debt = max(0.0, d1 - h * amort)
    fin = debt * rate

    fx_line = 0.0                                                     # D8, stated
    pbt = sales - cogs - ga + fx_line - fin
    tax = -TAX_RATE * max(0.0, pbt)                                   # D9
    npat = pbt + tax                                                  # D10

    return dict(vol=vol, rpt=rpt, cpt=cpt, seg=seg, other=other, sales=sales,
                cash_cost=cash_cost, dna=dna, cogs=cogs, ga=ga, fin=fin,
                debt=debt, rate=rate, pbt=pbt, tax=tax, npat=npat,
                gp=sales - cogs)


def actual(year):
    r, o = P.IS[year], P.OPS[year]
    return dict(vol=o['vol_total'], rpt=rev_per_tonne(year), cpt=cost_per_tonne(year),
                seg=seg_rev(year), other=other_rev(year), sales=r['sales'],
                cash_cost=o['cash_cost'] * 1e6, dna=o['dna'] * 1e6, cogs=r['cogs'],
                ga=r['ga'], fin=r['fin'], pbt=r['pbt'], tax=r['tax'],
                npat=r['npat'], gp=r['gp'])


def freeze(origin, h):
    """Naive benchmark 1 — every line flat at the origin's last actual."""
    return actual(origin)


def trend(origin, h):
    """Naive benchmark 2 — every line at its own trailing 3-year CAGR."""
    out = {}
    for k in ('vol', 'rpt', 'cpt', 'seg', 'other', 'sales', 'cash_cost', 'dna',
              'cogs', 'ga', 'fin', 'pbt', 'npat', 'gp'):
        ser = {}
        for y in range(origin - 3, origin + 1):
            try:
                ser[y] = actual(y)[k]
            except (KeyError, ZeroDivisionError):
                pass
        g = _cagr(ser, origin)
        base = ser.get(origin)
        out[k] = base * (1 + g) ** h if base is not None else None
    return out


ORIGINS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
LAST_ACTUAL = 2025
DRIVERS = ('vol', 'rpt', 'cpt', 'seg', 'other', 'sales', 'cash_cost', 'ga',
           'fin', 'gp', 'pbt', 'npat')


def cells(knowable=True):
    """Every (origin, horizon) the panel can grade."""
    for o in ORIGINS:
        for h in range(1, 6):
            y = o + h
            if y > LAST_ACTUAL:
                continue
            yield o, h, y, project(o, h, knowable), actual(y)


if __name__ == '__main__':
    P.check()
    n = 0
    print('%-7s %-3s %-6s %10s %10s %10s %10s' %
          ('origin', 'h', 'year', 'sales_p', 'sales_a', 'npat_p', 'npat_a'))
    for o, h, y, p, a in cells():
        n += 1
        print('%-7d %-3d %-6d %10.0f %10.0f %10.0f %10.0f' %
              (o, h, y, p['sales'] / 1e6, a['sales'] / 1e6,
               p['npat'] / 1e6, a['npat'] / 1e6))
    print('\n%d graded cells' % n)
    print('\nimplied borrowing rate at each origin [L-002 denominator]:')
    for o in ORIGINS:
        print('  %d  %.1f%%  (debt %.0f -> %.0f EGPmn)'
              % (o, project(o, 1)['rate'] * 100,
                 P.DEBT_SERIES[o - 1], P.DEBT_SERIES[o]))
