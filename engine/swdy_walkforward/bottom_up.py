"""The mechanical driver model, rebuilt AT EVERY ORIGIN, exactly as pre-registered.

No judgement drivers. No rule reads guidance. Every macro term uses only what had been
published at the origin. The rules and their parameters are in
PRE_REGISTRATION_07-09-2026.md and are not restated here as anything other than code.
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PANEL = json.load(open(os.path.join(HERE, 'panel.json')))
MACRO = json.load(open(os.path.join(HERE, 'macro.json')))['series']
YEARS = PANEL['years']

ORIGINS = list(range(2014, 2026))
HORIZONS = (1, 2, 3, 4, 5)
W_METAL = 0.7                       # pre-registered, stated, never fitted
UNIT_WINDOW = (2012, 2020)          # the investor sheets' own definition window


# The releases and the audited statements name the same line differently by vintage:
# "Interest Expense" / "Interest Income" in the releases, "Finance costs" / "Finance
# income" in the audited statements. One spelling reads half the window as absent.
ALIASES = {'finance_cost': ('finance_cost', 'interest_exp'),
           'finance_inc': ('finance_inc', 'interest_inc'),
           'dna': ('dna', 'depreciation'),
           'npat_owners': ('npat_owners', 'net_income')}


def val(y, key):
    for k in ALIASES.get(key, (key,)):
        r = YEARS.get(str(y), {}).get(k)
        if r:
            return r['value']
    return None


def leg(y, kind, name):
    r = YEARS.get(str(y), {}).get('legs', {}).get(kind, {}).get(name)
    return r['value'] if r else None


def seg(y, name, field):
    r = YEARS.get(str(y), {}).get('segment_sheet', {}).get(name, {}).get(field)
    return r['value'] if r else None


def unit(y, key):
    r = YEARS.get(str(y), {}).get('units', {}).get(key)
    return r['value'] if r else None


def m(series, y):
    v = MACRO[series]['values'].get(str(y))
    return float(v) if v is not None else None


def known_at(series, o):
    """The last published value of a macro series at origin o. The World Bank publishes
    a year's figure in the following year, so an origin at 31 December of year o sees
    the figure for o-1 as its last PUBLISHED annual reading; o's own is not out yet."""
    for y in range(o - 1, o - 6, -1):
        v = m(series, y)
        if v is not None:
            return v, y
    return None, None


def paths(o):
    """The origin's own macro multipliers, from what was published at o."""
    cpi, cpi_y = known_at('cpi_pct', o)
    gdp, gdp_y = known_at('gdp_g', o)
    fx_now, _ = known_at('egp_usd', o)
    fx_prev = m('egp_usd', (o - 2))
    fx = (fx_now / fx_prev - 1.0) if (fx_now and fx_prev) else 0.0
    return dict(cpi=cpi / 100.0 if cpi is not None else 0.0, cpi_year=cpi_y,
                gdp=gdp / 100.0 if gdp is not None else 0.0, gdp_year=gdp_y,
                fx=fx, copper=m('copper', o), aluminum=m('aluminum', o))


def project(o, h, w_metal=W_METAL):
    """Every pre-registered driver, projected h years forward from origin o."""
    p = paths(o)
    CPI = (1 + p['cpi']) ** h
    GDP = (1 + p['gdp']) ** h
    FX = (1 + p['fx']) ** h
    METAL = w_metal * FX + (1 - w_metal) * CPI      # metal held flat in USD, converted

    d = {}
    in_units = UNIT_WINDOW[0] <= o <= UNIT_WINDOW[1]
    if in_units and unit(o, 'cable_volume_t'):
        d['D1_cable_volume_t'] = unit(o, 'cable_volume_t') * GDP
        d['D2_cable_price_t'] = unit(o, 'cable_price_t') * METAL
        d['D3_cable_cost_t'] = unit(o, 'cable_cost_t') * METAL
        d['D4_cables_revenue'] = d['D1_cable_volume_t'] * d['D2_cable_price_t']
        d['D7_cables_cost'] = d['D1_cable_volume_t'] * d['D3_cable_cost_t']
        d['_cables_basis'] = 'unit'
    else:
        cab = leg(o, 'revenue', 'cables')
        if cab:
            d['D4_cables_revenue'] = cab * GDP * CPI
            gp = leg(o, 'gross_profit', 'cables') or seg(o, 'cables', 'gross_profit')
            if gp is not None:
                d['D7_cables_cost'] = (cab - gp) * GDP * METAL
        d['_cables_basis'] = 'segment'

    con = leg(o, 'revenue', 'contracting')
    if con:
        d['D5_contracting_revenue'] = con * GDP * CPI
        gp = leg(o, 'gross_profit', 'contracting') or seg(o, 'contracting', 'gross_profit')
        if gp is not None:
            d['D8_contracting_cost'] = (con - gp) * GDP * CPI
    oth = leg(o, 'revenue', 'other')
    if oth:
        d['D6_other_revenue'] = oth * GDP * CPI
        gp = leg(o, 'gross_profit', 'other') or seg(o, 'other', 'gross_profit')
        if gp is not None:
            d['D9_other_cost'] = (oth - gp) * GDP * CPI

    sga = val(o, 'sga')
    if sga is not None:
        d['D10_sga'] = abs(sga) * CPI

    # D11 / D12: PP&E roll-forward on the DISCLOSED useful life, capex an input
    life = json.load(open(os.path.join(HERE, '..', 'swdy_study', 'useful_lives.json'))
                     )['adopted_for_terminal']['years']
    vi = json.load(open(os.path.join(HERE, 'valuation_inputs.json')))
    blk = vi['origins'].get(str(o)) or vi['prior_year_anchor'].get(str(o)) or {}
    ppe0 = (blk.get('ppe') or blk.get('ppe_or_fixed_assets') or {}).get('value')
    capex0 = (blk.get('capex') or {}).get('value')
    if ppe0 and capex0:
        ppe, dep = ppe0, None
        for k in range(1, h + 1):
            dep = ppe / life
            ppe = ppe + capex0 * ((1 + p['cpi']) ** k) - dep
        d['D11_depreciation'] = dep
        d['D12_capex'] = capex0 * CPI

    for src, key in (('other_op_inc', 'D13_other_operating_income'),
                     ('other_op_exp', 'D14_other_operating_expense'),
                     ('finance_cost', 'D15_finance_costs'),
                     ('finance_inc', 'D16_finance_income')):
        v = val(o, src)
        if v is not None:
            d[key] = abs(v)
    d['D17_fx_differences'] = 0.0

    # revenue and cost aggregates, built from the legs and never from a group margin
    rev = sum(d.get(k, 0.0) for k in ('D4_cables_revenue', 'D5_contracting_revenue',
                                      'D6_other_revenue'))
    cost = sum(d.get(k, 0.0) for k in ('D7_cables_cost', 'D8_contracting_cost',
                                       'D9_other_cost'))
    if rev:
        d['A_revenue'] = rev
    if cost:
        d['A_cost_of_revenue'] = cost
        d['A_gross_profit'] = rev - cost
    return d, p


def borrowing_rate(o):
    """D15's own rate: the finance charge over THE BORROWINGS THAT BEAR IT."""
    vi = json.load(open(os.path.join(HERE, 'valuation_inputs.json')))
    blk = vi['origins'].get(str(o)) or vi['prior_year_anchor'].get(str(o)) or {}
    debt = (blk.get('interest_bearing_debt') or {}).get('value')
    fc = val(o, 'finance_cost')
    if not debt or fc is None:
        return None
    return abs(fc) / debt


def actual(y):
    """The scored quantities as the company reported them for year y."""
    a = {}
    if unit(y, 'cable_volume_t'):
        a['D1_cable_volume_t'] = unit(y, 'cable_volume_t')
        a['D2_cable_price_t'] = unit(y, 'cable_price_t')
        a['D3_cable_cost_t'] = unit(y, 'cable_cost_t')
    for k, kind, name in (('D4_cables_revenue', 'revenue', 'cables'),
                          ('D5_contracting_revenue', 'revenue', 'contracting'),
                          ('D6_other_revenue', 'revenue', 'other')):
        v = leg(y, kind, name)
        if v is not None:
            a[k] = v
    for k, name in (('D7_cables_cost', 'cables'), ('D8_contracting_cost', 'contracting'),
                    ('D9_other_cost', 'other')):
        rev = leg(y, 'revenue', name)
        gp = leg(y, 'gross_profit', name) or seg(y, name, 'gross_profit')
        if rev is not None and gp is not None:
            a[k] = rev - gp
    for src, key in (('sga', 'D10_sga'), ('dna', 'D11_depreciation'),
                     ('other_op_inc', 'D13_other_operating_income'),
                     ('other_op_exp', 'D14_other_operating_expense'),
                     ('finance_cost', 'D15_finance_costs'),
                     ('finance_inc', 'D16_finance_income'),
                     ('revenue', 'A_revenue'), ('gross_profit', 'A_gross_profit'),
                     ('npat_owners', 'A_net_profit_owners')):
        v = val(y, src)
        if v is not None:
            a[key] = abs(v)
    if 'A_revenue' in a and 'A_gross_profit' in a:
        a['A_cost_of_revenue'] = a['A_revenue'] - a['A_gross_profit']
    vi = json.load(open(os.path.join(HERE, 'valuation_inputs.json')))
    blk = vi['origins'].get(str(y)) or {}
    cx = (blk.get('capex') or {}).get('value')
    if cx:
        a['D12_capex'] = cx
    return a
