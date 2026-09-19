#!/usr/bin/env python3
"""ADIB (EGX) — the ground-up build at every origin, exactly as pre-registered.

Rules R1-R15 of PRE_REGISTRATION_09-09-2026.md, implemented here and nowhere else.
NO JUDGEMENT DRIVERS: every input to every rule is a figure published on or before its
own origin.

THE TWO TRAPS, OBEYED STRUCTURALLY RATHER THAN REMEMBERED:

  (i)  THE FUNDING COST'S DENOMINATOR IS `interest_bearing(y)` AND NOTHING ELSE -
       customers' deposits + due to banks + subordinated financing. For an industrial
       company the protocol's rule EXCLUDES customer deposits; for a bank it INCLUDES
       them, because they are exactly what bears the charge. The rule is the same; the
       example inverts. Total liabilities is never used as a rate base anywhere here.

  (ii) EVERY RATE IS APPLIED TO AN AVERAGE OF OPENING AND CLOSING BALANCES, never to a
       closing balance. This is the bank-shaped form of "revenue and cost on the same
       recognition clock": a bank that grows its balance sheet 33% in a year earns its
       yield on roughly the mean of the two, and crediting a full year of income to a
       closing balance would inflate projected profit by a large, robust, entirely
       spurious margin. `_avg()` is the only route from a balance to a rate base.

MARGINS ARE OUTPUTS [L-005]. NIM, cost-to-income, ROA and ROE are computed from the
driver outputs and are never inputs.
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, macro  # noqa: E402

ORIGINS = list(range(2014, 2025))          # FY2014 .. FY2024
HORIZONS = [1, 2, 3, 4, 5]
LAST = 2025
K = 3                                       # the trailing window, fixed in §1
ERA_BREAK = 2016                            # first origin whose whole window is post-B2
TAX_CLIP = (0.0, 0.80)
BOOT_SEED = 20260909


def fy(y):
    return 'FY%d' % y


# ---------------------------------------------------------------- panel accessors
def _bs(y, f):
    return panel.BS[fy(y)].get(f)


def _is(y, f):
    return panel.IS[fy(y)].get(f)


def interest_bearing(y):
    """Trap (i): the liabilities that ACTUALLY BEAR the cost of deposits.

    Customers' deposits + due to banks + subordinated financing. Nothing else. At
    FY2025 this is EGP 293.7bn against total liabilities of EGP 312.1bn; using the
    latter would understate the funding rate by 6% of itself, and the gap is wider in
    the years with large 'other liabilities'.
    """
    b = panel.BS[fy(y)]
    v = b.get('cust_deposits')
    if v is None:
        return None
    return v + (b.get('due_to_banks') or 0.0) + (b.get('subordinated') or 0.0)


def _avg(f, y):
    """Trap (ii): the ONLY route from a balance to a rate base."""
    a, b = _bs(y - 1, f), _bs(y, f)
    if a is None or b is None:
        return None
    return (a + b) / 2.0


def avg_ibl(y):
    a, b = interest_bearing(y - 1), interest_bearing(y)
    if a is None or b is None:
        return None
    return (a + b) / 2.0


def share_of_system(y):
    """R2. ADIB net customer financing (EGP '000) over system credit (EGP)."""
    f = _bs(y, 'fin_customers')
    s = macro.SYSTEM_CREDIT.get(y)
    if f is None or not s:
        return None
    return f * 1000.0 / s


# ---------------------------------------------------------------- trailing windows
def window(o, k=K, need=None):
    """The k years ending at o for which every field in `need` exists."""
    ys = []
    for y in range(o - k + 1, o + 1):
        if fy(y) not in panel.IS or fy(y) not in panel.BS:
            continue
        if need and any(n(y) is None for n in need):
            continue
        ys.append(y)
    return ys


def tmean(o, fn, k=K):
    ys = [y for y in range(o - k + 1, o + 1) if fn(y) is not None]
    if not ys:
        return None
    return sum(fn(y) for y in ys) / len(ys)


# ---------------------------------------------------------------- the driver ratios
def r_yield(y):
    a = _avg('total_assets', y)
    return None if not a else _is(y, 'fin_income') / a


def r_cof(y):
    a = avg_ibl(y)
    return None if not a else -_is(y, 'cost_funds') / a


def r_fees(y):
    if y < 2012:                      # break B3 - the fee window opens at FY2012
        return None
    a = _avg('total_assets', y)
    return None if not a else _is(y, 'net_fees') / a


def r_onii(y):
    if y < 2012:
        return None
    a = _avg('total_assets', y)
    return None if not a else panel.other_nii(fy(y)) / a


def r_otherop(y):
    a = _avg('total_assets', y)
    return None if not a else _is(y, 'other_op') / a


def r_cor(y):
    a = _avg('fin_customers', y)
    return None if not a else -_is(y, 'ecl') / a


def r_ldr(y):
    d = _bs(y, 'cust_deposits')
    f = _bs(y, 'fin_customers')
    return None if not d or f is None else f / d


def r_assets_dep(y):
    d = _bs(y, 'cust_deposits')
    return None if not d else _bs(y, 'total_assets') / d


def r_ibl_dep(y):
    d = _bs(y, 'cust_deposits')
    ib = interest_bearing(y)
    return None if not d or ib is None else ib / d


def r_tax(y):
    p = _is(y, 'pbt')
    return None if not p or p <= 0 else -_is(y, 'tax') / p


def r_nci(y):
    n = _is(y, 'np')
    return None if not n or n == 0 else _is(y, 'nci') / n


# ---------------------------------------------------------------- R10, overheads
def admin_params(o, k=K):
    """R10. OLS of REAL admin on REAL average assets over the trailing k+1 years.

    Both series are deflated to origin-year money with the published CPI index, so the
    intercept is a real fixed base and the slope is a real variable rate. Returns
    (F_o, v_o, 'ols') or (None, None, 'cpi-only') when the branch conditions fail.
    """
    ys = [y for y in range(o - k, o + 1)
          if fy(y) in panel.IS and _avg('total_assets', y) is not None]
    pts = []
    for y in ys:
        idx = macro.cpi_index(y, o)          # y-money -> o-money
        if idx is None:
            continue
        pts.append((_avg('total_assets', y) * idx, -_is(y, 'admin') * idx))
    if len(pts) < 3:
        return None, None, 'cpi-only(<3 points)'
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    if sxx <= 0:
        return None, None, 'cpi-only(degenerate)'
    v = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
    F = my - v * mx
    if v < 0 or F < 0:
        return None, None, 'cpi-only(negative %s)' % ('slope' if v < 0 else 'intercept')
    return F, v, 'ols'


# ---------------------------------------------------------------- the build
def build(o, hmax=5, cpi_path=None, credit_path=None, k=K):
    """Project ADIB from origin `o`. Returns {year: {line: value}} plus a meta block.

    `cpi_path` / `credit_path` override the mechanical macro (R1, R15) and are how the
    PERFECT MACRO re-run of §4 is done. Passing neither is the pre-registered run.
    """
    sysc = credit_path or macro.projected_system_credit(o, hmax, k)
    cpip = cpi_path or macro.projected_cpi_path(o, hmax, k)
    if sysc is None or cpip is None:
        return None

    share = share_of_system(o)
    ldr = tmean(o, r_ldr, k)
    m_ad = tmean(o, r_assets_dep, k)
    m_ib = tmean(o, r_ibl_dep, k)
    yld = tmean(o, r_yield, k)
    cof = tmean(o, r_cof, k)
    fee = tmean(o, r_fees, k)
    oni = tmean(o, r_onii, k)
    oop = tmean(o, r_otherop, k)
    cor = tmean(o, r_cor, k)
    txr = tmean(o, r_tax, k)
    nci = tmean(o, r_nci, k)
    F, v, branch = admin_params(o, k)

    if None in (share, ldr, m_ad, m_ib, yld, cof, cor):
        return None
    txr = 0.0 if txr is None else min(max(txr, TAX_CLIP[0]), TAX_CLIP[1])
    nci = 0.0 if nci is None else nci
    fee = fee if fee is not None else 0.0
    oni = oni if oni is not None else 0.0
    oop = oop if oop is not None else 0.0

    # CPI index from the origin, on the projected path
    # The path may run out before hmax - a PERFECT-MACRO re-run can only use years
    # that have actually happened. Projection stops where the path stops; it is never
    # extended by carrying the last value forward, which would fabricate the cell.
    idx = {o: 1.0}
    reach = o
    for h in range(1, hmax + 1):
        if (o + h) not in cpip or (o + h) not in sysc:
            break
        idx[o + h] = idx[o + h - 1] * (1.0 + cpip[o + h] / 100.0)
        reach = o + h
    hmax = reach - o

    prev = dict(fin_customers=_bs(o, 'fin_customers'),
                cust_deposits=_bs(o, 'cust_deposits'),
                total_assets=_bs(o, 'total_assets'),
                ibl=interest_bearing(o))
    out = {}
    for h in range(1, hmax + 1):
        y = o + h
        fin = sysc[y] * share / 1000.0                       # R1 x R2, back to EGP '000
        dep = fin / ldr                                      # R3
        ta = dep * m_ad                                      # R4
        ibl = dep * m_ib                                     # R5

        avg_ta = (prev['total_assets'] + ta) / 2.0           # trap (ii)
        avg_ib = (prev['ibl'] + ibl) / 2.0
        avg_fin = (prev['fin_customers'] + fin) / 2.0

        fin_income = yld * avg_ta                            # R6
        cost_funds = -cof * avg_ib                           # R7
        net_funds = fin_income + cost_funds                  # OUTPUT
        net_fees = fee * avg_ta                              # R8
        other_nii = oni * avg_ta                             # R9
        other_op = oop * avg_ta                              # R11
        ecl = -cor * avg_fin                                 # R12
        if branch == 'ols':                                  # R10
            admin = -(F + v * avg_ta)
        else:
            admin = _is(o, 'admin') * idx[y]
        pbt = net_funds + net_fees + other_nii + other_op + ecl + admin
        tax = -txr * pbt
        np_ = pbt + tax
        np_parent = np_ * (1.0 - nci)

        out[y] = dict(fin_customers=fin, cust_deposits=dep, total_assets=ta,
                      interest_bearing=ibl, avg_total_assets=avg_ta,
                      fin_income=fin_income, cost_funds=cost_funds,
                      net_funds=net_funds, net_fees=net_fees, other_nii=other_nii,
                      other_op=other_op, admin=admin, ecl=ecl,
                      pbt=pbt, tax=tax, np=np_, np_parent=np_parent,
                      # outputs, never inputs
                      nim=net_funds / avg_ta,
                      cost_income=-admin / (net_funds + net_fees + other_nii),
                      roa=np_ / avg_ta)
        prev = dict(fin_customers=fin, cust_deposits=dep, total_assets=ta, ibl=ibl)

    out['_meta'] = dict(origin=o, share_of_system=share, ldr=ldr, assets_per_dep=m_ad,
                        ibl_per_dep=m_ib, asset_yield=yld, cost_of_funds=cof,
                        fee_ratio=fee, onii_ratio=oni, otherop_ratio=oop,
                        cost_of_risk=cor, tax_rate=txr, nci_share=nci,
                        admin_branch=branch, admin_F=F, admin_v=v,
                        credit_cagr=macro.system_credit_cagr(o, k),
                        cpi_trailing=macro.trailing_mean_cpi(o, k))
    return out


# ---------------------------------------------------------------- benchmarks
def freeze(o, hmax=5):
    """Every line flat at its last actual."""
    base = {}
    for f in ('fin_income', 'cost_funds', 'net_funds', 'net_fees', 'other_op',
              'admin', 'ecl', 'pbt', 'tax', 'np', 'np_parent'):
        base[f] = _is(o, f)
    base['other_nii'] = panel.other_nii(fy(o))
    for f in ('fin_customers', 'cust_deposits', 'total_assets'):
        base[f] = _bs(o, f)
    return {o + h: dict(base) for h in range(1, hmax + 1)}


def _cagr(a, b, k):
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return (b / a) ** (1.0 / k) - 1.0


def trend(o, hmax=5, k=K):
    """Every line grown at its own trailing k-year CAGR. Sign-crossing lines drop out."""
    out = {o + h: {} for h in range(1, hmax + 1)}
    fields = ('fin_income', 'cost_funds', 'net_funds', 'net_fees', 'other_nii',
              'other_op', 'admin', 'ecl', 'pbt', 'tax', 'np', 'np_parent',
              'fin_customers', 'cust_deposits', 'total_assets')
    for f in fields:
        def get(y, f=f):
            if f == 'other_nii':
                return panel.other_nii(fy(y)) if fy(y) in panel.IS else None
            if f in panel.IS.get(fy(y), {}):
                return _is(y, f)
            return _bs(y, f)
        a, b = get(o - k), get(o)
        if a is None or b is None:
            continue
        sgn = 1.0 if b >= 0 else -1.0
        g = _cagr(abs(a) if a * b > 0 else None, abs(b), k)
        if g is None:
            continue
        for h in range(1, hmax + 1):
            out[o + h][f] = sgn * abs(b) * (1.0 + g) ** h
    return out


if __name__ == '__main__':
    print('%-8s %8s %8s %8s %8s %8s %8s %8s %-22s' %
          ('origin', 'share%', 'LDR', 'yield%', 'CoF%', 'CoR%', 'tax%', 'fee%', 'admin branch'))
    for o in ORIGINS:
        m = build(o)['_meta']
        print('%-8s %8.3f %8.3f %8.3f %8.3f %8.3f %8.1f %8.3f %-22s' %
              (fy(o), 100 * m['share_of_system'], m['ldr'], 100 * m['asset_yield'],
               100 * m['cost_of_funds'], 100 * m['cost_of_risk'], 100 * m['tax_rate'],
               100 * m['fee_ratio'], m['admin_branch']))
