#!/usr/bin/env python3
"""SCEM walk-forward — the driver model, rebuilt mechanically at every origin.

EXACTLY THE RULES PRE-REGISTERED IN PRE_REGISTRATION_07-09-2026.md, and nothing else.
No judgement driver stands at a historical origin: every input below is either a figure
the origin could read off its own filing, or an exogenous index from the IMF edition
that existed at that year-end. Parameters are stated, never fitted.

TRAP (i) IS HONOURED BY CONSTRUCTION: the borrowing rate is the finance charge over the
borrowings that ACTUALLY BEAR IT.
TRAP (ii) IS HONOURED BY CONSTRUCTION: this issuer recognises revenue on despatch and
its cost of sales in the same period, and panel.py asserts the cost note foots to the
face of the profit and loss account in every year, so the two sit on one clock.
"""
import json
import os

import macro as M
import panel as P

HERE = os.path.dirname(os.path.abspath(__file__))

TAX_STATUTORY = 0.225        # Egypt, the regime known at every origin in this window
DEP_RATE_ON_GROSS = 0.038626  # note 3/2's disclosed rates on note 4's own gross-cost mix

DRIVERS = ["revenue", "materials", "cogs_wages", "cogs_maintenance", "transport",
           "ga", "dna", "finance_expense", "interest_income", "capex",
           "working_capital", "ebitda", "pat"]

VARIABLE = {"revenue", "materials", "transport"}      # volume x price
REAL_FLAT = {"cogs_wages", "cogs_maintenance", "ga", "capex"}   # price only


def project(origin, horizons=(1, 2, 3), macro_override=None):
    """The model as it stood at `origin`, run forward h years.

    macro_override: None for 'as known', or a callable year -> dict(real_gdp_growth, cpi)
    for the perfect-foresight legs.
    """
    d = P.derived()[origin]
    b = P.BS[origin]
    believed = M.path(origin, horizons)
    y0 = int(origin[2:])

    # the origin's own realised rates, on the right denominators
    kd = d.get('kd_on_borrowings')
    if kd is None:                       # FY2021 has no prior year in this panel
        kd = P.IS[origin]['finance'] / (b['bank_facilities'] + b['lt_loans']
                                        + b['st_loans_affiliates'])
    rdep = d.get('deposit_rate')
    if rdep is None:
        rdep = (P.IS[origin]['interest_income']
                / (b['cash'] + b['cash_blocked'])) if (b['cash'] + b['cash_blocked']) else 0.0

    debt = d['interest_bearing_debt']
    cash = d['cash']
    ppe_dep = d['dna']
    capex_prev = d['capex']

    out = {}
    V = P_ = 1.0
    for h in sorted(horizons):
        y = y0 + h
        if macro_override is None:
            m = believed[h]
        else:
            m = macro_override(y)
        if m['cpi'] is None or m['real_gdp_growth'] is None:
            out[h] = None                # RECORDED AS UNAVAILABLE, never filled
            continue
        V *= (1.0 + m['real_gdp_growth'])
        P_ *= (1.0 + m['cpi'])

        rev = d['revenue'] * V * P_
        mat = d['materials'] * V * P_
        wag = d['cogs_wages'] * P_
        mnt = d['cogs_maintenance'] * P_
        trn = d['transport'] * V * P_
        ga = d['ga'] * P_
        cpx = d['capex'] * P_
        # D&A: a PP&E roll-forward off the DISCLOSED rate. Last year's charge plus the
        # rate applied to last year's capital spending. No CPI term in year one, which
        # is the macro split's own internal control.
        dep = ppe_dep + capex_prev * DEP_RATE_ON_GROSS
        fin = kd * debt                  # debt held flat at the origin's level
        iinc = rdep * cash
        # every other operating cost the cost note carries, held flat in real terms
        other_cost = (d['cogs'] - d['materials'] - d['cogs_wages']
                      - d['cogs_maintenance']
                      - P.COST_NOTES[origin]['industrial_depreciation'] / 1e6)
        other_cost *= P_
        selling_other = (d['selling'] - d['transport']) * P_
        ebitda = rev - mat - wag - mnt - trn - ga - other_cost - selling_other
        pbt = ebitda - dep - fin + iinc
        tax = TAX_STATUTORY * pbt if pbt > 0 else 0.0
        pat = pbt - tax

        out[h] = dict(year=y, V=V, P=P_,
                      revenue=rev, materials=mat, cogs_wages=wag,
                      cogs_maintenance=mnt, transport=trn, ga=ga,
                      dna=dep, finance_expense=fin, interest_income=iinc,
                      capex=cpx, working_capital=d['wc_pct_revenue'] * rev,
                      ebitda=ebitda, pbt=pbt, tax=tax, pat=pat,
                      cpi=m['cpi'], real_gdp_growth=m['real_gdp_growth'])
        ppe_dep, capex_prev, cash = dep, cpx, cash + max(pat, 0.0)
    return out


def actual(year):
    """What the company reported for that year, on the same driver definitions."""
    y = "FY%d" % year
    if y not in P.YEARS:
        return None
    d = P.derived()[y]
    return dict(revenue=d['revenue'], materials=d['materials'],
                cogs_wages=d['cogs_wages'], cogs_maintenance=d['cogs_maintenance'],
                transport=d['transport'], ga=d['ga'], dna=d['dna'],
                finance_expense=d['finance_expense'],
                interest_income=d['interest_income'], capex=d['capex'],
                working_capital=d['working_capital'], ebitda=d['ebitda'],
                pat=d['pat'],
                pat_ex_oneoff=d['pat'] - (P.IS[y].get('gain_on_sale_of_investments', 0)
                                          / 1e6))


# --------------------------------------------------------------------------- benchmarks
def freeze(origin, horizons=(1, 2, 3)):
    d = P.derived()[origin]
    base = {k: d[k] for k in DRIVERS if k in d}
    return {h: dict(base) for h in horizons}


def trend(origin, horizons=(1, 2, 3)):
    """Trailing 3-year CAGR, shortened to the longest window available, minimum two
    points. UNDEFINED where only one point exists — recorded, never filled."""
    i = P.YEARS.index(origin)
    hist = P.YEARS[max(0, i - 3):i + 1]
    if len(hist) < 2:
        return None
    n = len(hist) - 1
    der = P.derived()
    out = {}
    for h in horizons:
        row = {}
        for k in DRIVERS:
            a, b = der[hist[0]].get(k), der[origin].get(k)
            if a is None or b is None or a <= 0 or b <= 0:
                row[k] = None           # a CAGR across a sign change is not a CAGR
                continue
            g = (b / a) ** (1.0 / n) - 1.0
            row[k] = b * (1.0 + g) ** h
        out[h] = row
    return out


if __name__ == '__main__':
    P.verify()
    rec = {}
    for o in P.YEARS:
        rec[o] = {'as_known': project(o),
                  'freeze': freeze(o),
                  'trend': trend(o)}
    json.dump(rec, open(os.path.join(HERE, 'projections.json'), 'w'), indent=1,
              default=lambda x: None)
    print('%-8s %-6s %10s %10s %10s %10s   %s'
          % ('origin', 'h', 'revenue', 'EBITDA', 'PAT', 'actual PAT', 'target'))
    for o in P.YEARS:
        for h in (1, 2, 3):
            p = rec[o]['as_known'][h]
            if p is None:
                continue
            a = actual(p['year'])
            print('%-8s h=%-4d %10.1f %10.1f %10.1f %10s   FY%d'
                  % (o, h, p['revenue'], p['ebitda'], p['pat'],
                     ('%.1f' % a['pat']) if a else 'pending', p['year']))
