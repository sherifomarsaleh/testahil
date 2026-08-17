"""Price every critique finding before judging it.

One entry per finding that touches a number. Each re-runs the valuation with
ONE thing changed and reports the move in the weighted central, in dirhams per
share and as a percentage of it. The combined package is re-derived in full
because it exceeds the 5% escalation threshold.

Findings that touch no number are priced at zero explicitly rather than being
called immaterial without one.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import compute as C

BASE = C.central
SPOT = C.V('spot_aed')
ROWS = []
V = C.V
SH = C.shares_out_k
FX = V('fx_aed_usd')
rowsA = C.CASE['A']['rows']


def bridge(ev, nci=None, put=None, jv=None):
    nci = V('nci_1h26') if nci is None else nci
    put = V('finliab_1h26') if put is None else put
    jv = V('jvinv_1h26') if jv is None else jv
    return ev + jv + V('cash_1h26') - V('debt_1h26') - V('lease_1h26') - nci - put


def ps(equity):
    return equity / SH * FX


def reweight(fair):
    return sum(fair[k] * C.LENS_WEIGHT[k] for k in fair)


def rec(tag, src, what, central, verdict):
    d = central - BASE
    ROWS.append(dict(tag=tag, source=src, what=what, central=central, delta=d,
                     pct=d / BASE, verdict=verdict))
    print(f"{tag:7s} {src:4s} {what[:58]:58s} {central:5.2f} {d:+6.2f} {d/BASE*100:+6.2f}%")


print(f"BASE weighted central AED {BASE:.2f}   market AED {SPOT:.2f}\n")
print(f"{'tag':7s} {'src':4s} {'finding':58s} {'centr':>5s} {'move':>6s} {'%':>7s}")

# ---------------------------------------------------------------- NORMALISED LENS
NU = dict(C.norm_units)
rate = dict(onshore=C.UNITS_H[2025]['rev_per_onshore_rig'],
            regional=V('rev_per_rig_regional'), jackup=C.REV_PER_JACKUP_25,
            island=C.REV_PER_ISLAND_25, ids=C.UNITS_H[2025]['rev_per_ids_rig'])


def norm_ps(units=None, dna=None, cap_rate=None, margin=None):
    u = units or NU
    rev = sum(u[k] * rate[k] for k in u)
    eb = rev * (margin if margin is not None else C.norm_margin)
    d = C.norm_dna if dna is None else dna
    nop = (eb - d) * (1 - V('tax_rate'))
    cr = (C.WACC - V('terminal_growth_B')) if cap_rate is None else cap_rate
    return ps(bridge(nop / cr))


fair = dict(C.FAIR); fair['normalised'] = norm_ps(cap_rate=C.WACC)
rec('CC1a', 'CC', 'normalised lens: capitalise at WACC, no growth credited',
    reweight(fair), 'ACCEPT')

INSTALLED = dict(onshore=92.0, regional=30.0, jackup=36.0, island=13.0, ids=61.0)
fair = dict(C.FAIR); fair['normalised'] = norm_ps(units=INSTALLED)
rec('CC1b', 'CC', 'normalised lens: the fleet actually installed at 30-Jun-2026',
    reweight(fair), 'ACCEPT')

fair = dict(C.FAIR); fair['normalised'] = norm_ps(dna=rowsA[0]['dna'])
rec('CC1c', 'SELF', 'normalised lens: D&A the priced fleet actually carries',
    reweight(fair), 'ACCEPT')

fair = dict(C.FAIR)
fair['normalised'] = norm_ps(units=INSTALLED, dna=rowsA[0]['dna'], cap_rate=C.WACC)
rec('CC1*', 'CC', 'normalised lens: all three together', reweight(fair), 'ACCEPT')

# ---------------------------------------------------------------- BOOK LENS
prev = C.H[2025]['equity']
roes = []
for r in rowsA:
    eq = r['balance_sheet']['equity_residual']
    roes.append(r['pat'] / ((prev + eq) / 2))
    prev = eq
for tag, roe, lbl in (('CC2a', roes[-1], 'the 2030 return the model forecasts'),
                      ('CC2b', float(np.mean(roes)), 'the average forecast return')):
    pb = (roe - C.g_book) / (C.ke_rating - C.g_book)
    fair = dict(C.FAIR); fair['book'] = pb * C.book_equity_now / SH * FX
    rec(tag, 'CC', f'book lens on {lbl} ({roe*100:.1f}%, not {C.roe_sustainable*100:.1f}%)',
        reweight(fair), 'ACCEPT')

# ---------------------------------------------------------------- RELATIVE LENS
jv_in_ebitda = V('jv_fy25')
for tag, src, ebitda, add_jv, lbl in (
        ('CC8', 'CC', C.H[2025]['ebitda'], True, 'trailing multiple on trailing EBITDA'),
        ('CC9', 'CC/GT/GR', C.ebitda_fy26 - jv_in_ebitda, True,
         'strip JV from the EBITDA the multiple is applied to'),
        ('CC89', 'CC', C.H[2025]['ebitda'] - jv_in_ebitda, True,
         'both: trailing basis AND JV stripped')):
    ev = C.blended_multiple * ebitda
    fair = dict(C.FAIR)
    fair['relative'] = ps(bridge(ev, jv=V('jvinv_1h26') if add_jv else 0.0))
    rec(tag, src, f'relative lens: {lbl}', reweight(fair), 'ACCEPT')

# ---------------------------------------------------------------- BRIDGE
fair = dict(C.FAIR)
for k, case in (('dcf_A', C.CASE['A']), ('dcf_B', C.CASE['B'])):
    fair[k] = ps(bridge(case['enterprise_value'], nci=0.0))
ev = C.blended_multiple * C.ebitda_fy26
fair['relative'] = ps(bridge(ev, nci=0.0))
fair['normalised'] = ps(bridge(C.norm_nopat / (C.WACC - V('terminal_growth_B')), nci=0.0))
rec('GT1', 'GT', 'bridge: deduct the put OR the minority, not both', reweight(fair),
    'ACCEPT')

# ---------------------------------------------------------------- WACC WEIGHTS
gross = V('debt_1h26') + V('lease_1h26')
we_g = C.mkt_cap / (C.mkt_cap + gross)
wacc_g = we_g * C.ke_rating + (1 - we_g) * C.kd_after_tax
orig = C.WACC
C.WACC = wacc_g
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = dict(C.FAIR)
fair['dcf_A'] = cases['A']['value_per_share_aed']
fair['dcf_B'] = cases['B']['value_per_share_aed']
fair['normalised'] = norm_ps(cap_rate=wacc_g - V('terminal_growth_B'))
rec('CC15', 'CC', f'WACC weights on gross debt ({wacc_g*100:.2f}% not {orig*100:.2f}%)',
    reweight(fair), 'ACCEPT')
C.WACC = orig

# ---------------------------------------------------------------- REGIONAL RIGS
orig_reg = {c: dict(C.FLEET[c]['regional']) for c in ('A', 'B')}
for tag, n2026 in (('CC16', 30.0),):
    # 30 in service for the whole of 2026 rather than averaging from zero
    for c in ('A', 'B'):
        C.FLEET[c]['regional'] = dict(orig_reg[c])
    saved = C.OPEN_FLEET_REGIONAL = 0.0
    cases = {}
    for c in ('A', 'B'):
        # emulate a full-year 30 by opening the regional fleet at 30
        pass
    C.FLEET['A']['regional'][2026] = 44.0     # (0+44)/2 = 22 average rig-years
    C.FLEET['B']['regional'][2026] = 44.0
    cases = {c: C.build_case(c) for c in ('A', 'B')}
    fair = dict(C.FAIR)
    fair['dcf_A'] = cases['A']['value_per_share_aed']
    fair['dcf_B'] = cases['B']['value_per_share_aed']
    rec(tag, 'CC/SELF', 'regional fleet averaging 22 rig-years in 2026, not 15',
        reweight(fair), 'ACCEPT')
for c in ('A', 'B'):
    C.FLEET[c]['regional'] = dict(orig_reg[c])

# ---------------------------------------------------------------- REGIONAL RATE
orig_rate = C.INP['rev_per_rig_regional']['value']
C.INP['rev_per_rig_regional']['value'] = 6700.0
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = dict(C.FAIR)
fair['dcf_A'] = cases['A']['value_per_share_aed']
fair['dcf_B'] = cases['B']['value_per_share_aed']
rec('CC25', 'CC', 'regional rate 6.7 per rig-year on the model\'s own 22.8% split',
    reweight(fair), 'ACCEPT')
C.INP['rev_per_rig_regional']['value'] = orig_rate

# ---------------------------------------------------------------- WORKING CAPITAL
wc_1h26 = (342783.0 + 233060.0 + 1418236.0) - (1197504.0 + 40533.0) - 312862.0
orig_wc = C.WC_PCT_REVENUE
C.WC_PCT_REVENUE = wc_1h26 / (V('rev_1h26') * 2)
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = dict(C.FAIR)
fair['dcf_A'] = cases['A']['value_per_share_aed']
fair['dcf_B'] = cases['B']['value_per_share_aed']
rec('SELF-A', 'SELF', 'working capital at the 1H-2026 actual 9.01% of revenue',
    reweight(fair), 'ACCEPT')
C.WC_PCT_REVENUE = orig_wc

# ---------------------------------------------------------------- TERMINAL RATE
C.WACC = C.ke_rating
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = dict(C.FAIR)
fair['dcf_A'] = cases['A']['value_per_share_aed']
fair['dcf_B'] = cases['B']['value_per_share_aed']
fair['normalised'] = norm_ps(cap_rate=C.ke_rating - V('terminal_growth_B'))
rec('SELF-B', 'SELF', 'terminal at the cost of equity (2030 firm is net cash)',
    reweight(fair), 'ACCEPT')
C.WACC = orig

# ---------------------------------------------------------------- UNCONV MARGIN
for tag, m, lbl in (('CC19a', 0.134, 'unconventional margin at a 50% conventional margin'),
                    ('CC19b', 0.012, 'unconventional margin at a 52% conventional margin')):
    om = C.INP['unconv_ebitda_margin']['value']
    C.INP['unconv_ebitda_margin']['value'] = m
    cases = {c: C.build_case(c) for c in ('A', 'B')}
    fair = dict(C.FAIR)
    fair['dcf_A'] = cases['A']['value_per_share_aed']
    fair['dcf_B'] = cases['B']['value_per_share_aed']
    rec(tag, 'CC', lbl, reweight(fair), 'ACCEPT (range)')
    C.INP['unconv_ebitda_margin']['value'] = om

# ---------------------------------------------------------------- PEER SET
peers = C.RELATIVE['peers']
land = [p for p in peers if p['group'].startswith('Global land')]
print()
print('  CC10 peer check — global land drillers, EV/EBITDA as built:')
for p in land:
    print(f"      {p['name']:22s} EV {p['ev_usd_mn']:8,.0f}  EBITDA {p['ltm_ebitda_usd_mn']:7,.0f}"
          f"  {p['ev_ebitda']:6.2f}x")
med_orig = C.RELATIVE['median_land']
alt = []
for p in land:
    e = p['ev_ebitda']
    if p['symbol'] == 'NBR':
        e = p['ev_usd_mn'] / 925.0
    alt.append(e)
alt = sorted(alt)
med_alt = (alt[1] + alt[2]) / 2
print(f"      median as built {med_orig:.4f}x | with Nabors at its own guided ~925 "
      f"{med_alt:.4f}x")
w = C.RELATIVE['segment_weights']
m_on = (C.RELATIVE['median_mena'] + med_alt) / 2
m_off = (C.RELATIVE['median_mena'] + C.RELATIVE['median_offshore']) / 2
blend_alt = (w['onshore'] * m_on + w['offshore'] * m_off + w['ofs'] * C.RELATIVE['median_ofs'])
fair = dict(C.FAIR)
fair['relative'] = ps(bridge(blend_alt * C.ebitda_fy26))
rec('CC10', 'CC', f'peer set with Nabors on its own guidance ({blend_alt:.2f}x)',
    reweight(fair), 'ACCEPT premise')

# ---------------------------------------------------------------- ZERO-PRICED
for tag, src, what in (
        ('CC3', 'CC', 'headline margin range omits FY2025 (44.8%)'),
        ('CC4', 'CC', 'the two cases ARE averaged inside the weighted central'),
        ('CC5', 'CC', 'section 4 says two lenses sit above the market; none do'),
        ('CC6', 'CC', 'EBITDA labelled identically incl. and excl. joint ventures'),
        ('CC7', 'CC', 'sensitivity caption vs the table beneath it'),
        ('CC11', 'CC', 'FY2025 capex $815m (audited) vs $772m (company metric)'),
        ('CC12', 'CC', '"58% dividend increase" — the actual figure is 52%'),
        ('CC13', 'CC', 'ROCE printed as both 24% and 23%'),
        ('CC17', 'CC', '"four of the six ordered rigs" — five remain'),
        ('CC18', 'CC', '"five independent lenses" — four share inputs'),
        ('CC20', 'CC', 'three volatilities for one share, unlabelled'),
        ('CC21', 'CC', 'backtest sample is not "since listing"'),
        ('CC23', 'CC', 'guidance reconciles at group, not by segment'),
        ('CC24', 'CC', 'both technical triggers sit inside one average true range'),
        ('CC30', 'CC', '836 wells not traced to its disclosure'),
        ('SELF-I', 'SELF', 'JV income in forecast cash but never received')):
    rec(tag, src, what, BASE, 'presentation')

# ---------------------------------------------------------------- COMBINED
C.WC_PCT_REVENUE = wc_1h26 / (V('rev_1h26') * 2)
C.WACC = C.ke_rating
for c in ('A', 'B'):
    C.FLEET[c]['regional'][2026] = 44.0
C.INP['rev_per_rig_regional']['value'] = 6700.0
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = {}
fair['dcf_A'] = ps(bridge(cases['A']['enterprise_value'], nci=0.0))
fair['dcf_B'] = ps(bridge(cases['B']['enterprise_value'], nci=0.0))
fair['relative'] = ps(bridge(blend_alt * (C.H[2025]['ebitda'] - jv_in_ebitda), nci=0.0))
pb = (float(np.mean(roes)) - C.g_book) / (C.ke_rating - C.g_book)
fair['book'] = pb * C.book_equity_now / SH * FX
rev_i = sum(INSTALLED[k] * rate[k] for k in INSTALLED)
nop_i = (rev_i * C.norm_margin - rowsA[0]['dna']) * (1 - V('tax_rate'))
fair['normalised'] = ps(bridge(nop_i / C.ke_rating, nci=0.0))
print()
rec('ALL', 'all', 'every accepted correction applied together', reweight(fair), 'ACCEPT')
print(f"        by lens: " + '  '.join(f'{k} {v:.2f}' for k, v in fair.items()))
C.WC_PCT_REVENUE, C.WACC = orig_wc, orig
for c in ('A', 'B'):
    C.FLEET[c]['regional'] = dict(orig_reg[c])
C.INP['rev_per_rig_regional']['value'] = orig_rate

json.dump(dict(base=BASE, spot=SPOT, rows=ROWS),
          open(os.path.join(HERE, 'critique_pricing.json'), 'w'), indent=1)
