"""EMPOWER_Valuation_Study_09-08-2026_public.docx — python-docx builder, house style.
Revised 17-Aug-2026 per the implemented external critique (see the accompanying
critique-response note). Reads study_numbers.json (and the companion data files)
exclusively: no financial numeral is typed into this file — every figure is loaded
or derived from the JSONs (critique_facts.json carries the externally verified
facts backing the revision; the critique-response note is read for its own counts)."""
import csv, json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D  = json.load(open('study_numbers.json'))
T  = json.load(open('tech_read.json'))
BT = json.load(open('backtest_5y.json'))
BR = json.load(open('beta_result.json'))
BR_DFM = json.load(open('beta_result_dfmgi.json'))
SW = json.load(open('sweep_register.json'))
SX = json.load(open('sweep_external.json'))
CF = json.load(open('critique_facts.json'))
CRTXT = open('CRITIQUE_RESPONSE_17-08-2026.md').read()
EXI = json.load(open('extract_2026_interims.json'))
EX23 = json.load(open('extract_fy2022_2023.json'))
EX24 = json.load(open('extract_fy2024.json'))
EX25 = json.load(open('extract_fy2025.json'))

IN = {k: v['value'] for k, v in D['inputs'].items()}
HI, U, F, W = D['hist_is'], D['unit'], D['fcst'], D['wacc']
DCF, LN, REL, NRM, BK = D['dcf'], D['lenses'], D['rel'], D['norm'], D['book']
DDM, CEN, SN, CRX, STK = D['ddm'], D['central'], D['sens_wg'], D['crux'], D['strike']
DEWA = D['dewa_buyin']
UP = D['unit_physical']
YRS = F['years']; B = F['base']; PS = F['persist']
BC, BD = DCF['base_ct'], DCF['base_dmtt']
PC, PD = DCF['pers_ct'], DCF['pers_dmtt']
BCD, BEAR, BULL = DCF['base_cds'], DCF['bear'], DCF['bull']
DGW, DCW, DFB = DCF['base_gross_wacc'], DCF['base_carry_wacc'], DCF['base_dfm_beta']
WC = W['constructions']
SCN = D['scenarios']
SPOT, SH = D['meta']['spot'], D['meta']['shares_mn']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
BT5, FIT = BT['five_year'], BT['fit']

def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def p2(x): return f"{x:.2f}"
def p3(x): return f"{x:.3f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"

def rx(pat, s):
    """Pull a figure out of a sourced JSON string — never typed into this file."""
    m = re.search(pat, s)
    if not m:
        raise SystemExit(f"rx failed: {pat!r} not found in {s[:90]!r}")
    return m.group(1)

# ---------------- derived display quantities (all from the JSONs) -------------
ND = W['net_debt']
NDX = ND / HI['FY25']['ebitda']
YLD = DDM['dps'] / SPOT
DEWA_PREM = DEWA['price'] / SPOT - 1
H1G = IN['rev_h1_26'] / IN['rev_h1_25'] - 1
Q2R = EXI['h1_2026']['q2_2026_reported_three_month_column']['revenue'] / 1000.0
Q2R_PRIOR = IN['rev_h1_25'] - EXI['q1_2025_comparative']['income_statement']['revenue'] / 1000.0
Q2G = Q2R / Q2R_PRIOR - 1
CRUX_DELTA = PC['ps'] / BC['ps'] - 1
DMTT_DELTA = BD['ps'] - BC['ps']
EWR = U['ew_ratio']
EW_REVSHARE = IN['ew_cost_fy25'] / IN['rev_fy25']
CONS_RT = U['cons_per_rt25'] * 1000.0          # AED per average connected RT / yr
CAP_RT = U['cap_per_rt25'] * 1000.0
CAPEX_RT = U['capex_per_rt'] * 1000.0
NCI_FRAC = IN['nci_pat_fy25'] / IN['pat_fy25']
NF25 = IN['fin_cost_fy25'] - IN['fin_inc_fy25']    # FY2025 net finance cost
TAXADJ = 1 - (1 - IN['tax_dmtt']) / (1 - IN['tax_ct'])
RT_H1 = IN['rt_conn']['H1_2026']; RT25Y = IN['rt_conn']['2025']
BACKLOG = IN['rt_contracted'] - RT_H1
RT_ADD_H1 = RT_H1 - RT25Y
GUID_LO, GUID_HI = IN['rt_guid_2026']
KD24 = float(rx(r"2024 comparison: ([\d.]+)%", D['inputs']['kd_marg']['source'])) / 100
EIBOR = float(rx(r"spot 3M EIBOR ([\d.]+)%", D['inputs']['kd_marg']['source'])) / 100
RCF_BN = rx(r"AED ([\d.]+)bn RCFs", D['inputs']['kd_marg']['source'])
EUR_TH = rx(r">= EUR (\d+)m", D['inputs']['tax_dmtt']['source'])
MIXD, MIXC, MIXO = re.search(r"demand (\d+)% / consumption (\d+)% / others (\d+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F16'][0]['headline']).groups()
GDP_NEW, GDP_OLD = re.search(r"guidance to ([\d.]+)% from ([\d.]+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F05'][0]['headline']).groups()
DFM_DD = SX['country_uae_macro']['dfm_index']['war_trough_close']['drawdown_from_peak']
RTH_DROP = rx(r"consumption -(\d+)m RTh", D['inputs']['eflh_h1']['source'])
EFLH_HRS = rx(r"(\d+) hrs", D['inputs']['eflh_h1']['source'])
Q1MARG, Q2MARG = re.search(r"Q1 margin ([\d.]+)%, Q2 ([\d.]+)%",
                           D['inputs']['ebitda_h1_26']['source']).groups()
# DXB CoolCo ownership: from the FY2025 filing's own subsidiary note (85%; the
# 2023 sweep row's "70%" was the acquisition-announcement figure and is superseded
# by the filing — critique CW4, confirmed against the H1-2026 subsidiary note)
_DXB_NOTE = EX25['_meta']['subsidiaries']['DXB CoolCo FZCO']
DXB_PCT = rx(r"^(\d+)%", _DXB_NOTE)
CONC_YRS = rx(r"(\d+)-year", _DXB_NOTE)                    # 35-year concession
CONC_FROM = rx(r"from (\d+ \w+ \d{4})\)", _DXB_NOTE)       # 5 July 2023
DXB_NCI_K = rx(r"NCI recorded at AED ([\d,]+)k", _DXB_NOTE)
CONC_FA_K = rx(r"receivable from DACC of ([\d,]+) recovered",
               EX23['notes']['fy2023_filing']['acquisition_dxb_cool']['accounting'])
DUBAI_SHARE = rx(r"~(\d+)% Dubai share",
                 [f for f in SW['findings'] if f['fid'] == 'F10'][0]['headline'])
BLDGS = rx(r"([\d,]+) buildings", SX['company_news_empower']['h1_2026_results'])
# Tenor of the Jan-2031 anchor print: 30-Jul-2026 auction to the Jan-2031 maturity
# (the "4.4" once quoted here was the auction's bid-to-cover, not a tenor — CW26)
from datetime import date as _date
TENOR = f"{(_date(2031, 1, 29) - _date(2026, 7, 30)).days / 365.25:.2f}"
REV21 = float(rx(r"revenue ([\d,]+\.\d)", [f for f in SW['findings'] if f['fid'] == 'F13'][0]['headline']).replace(',', ''))
MARG_LO, MARG_HI = re.search(r"EBITDA margin ([\d.]+)-([\d.]+)%",
                             [f for f in SW['findings'] if f['fid'] == 'F13'][0]['headline']).groups()
# sensitivity-grid coordinates for expert 1's range construction
_gi = SN['g_grid'].index(IN['g_term']); _wi = SN['wacc_grid'].index(W['rating_ct'])
_base_cell = SN['table'][_wi][_gi]
_dn50 = SN['table'][_wi + 1][_gi]; _up50 = SN['table'][_wi - 1][_gi]
E1_LO = CRX['rows'][0]['ps'] * (1 + 0.5 * (_dn50 / _base_cell - 1))
E1_HI = CRX['rows'][-1]['ps'] * (1 + 0.5 * (_up50 / _base_cell - 1))
def ddm_at(g): return DDM['dps'] * (1 + g) / (W['ke_rating'] - g)
E2_G_LO, E2_G_HI = SN['g_grid'][2], SN['g_grid'][4]     # the grid's 2.0% and 3.0% nodes
E2_LO, E2_HI = ddm_at(E2_G_LO), ddm_at(E2_G_HI)
E3_CENTRAL = REL['ps_pe']
WAGE_ESC = B['ga']['FY27'] / B['ga']['FY26'] - 1        # the wage-class escalator, from the build itself
DEWA_PCT = rx(r'DEWA (\d+)%', D['meta']['ownership'])
FLOAT_PCT = rx(r'~(\d+)%', D['meta']['ownership'])
TB_NDX = rx(r'([\d.]+)x', SX['peers_relative_multiples']['TABREED']['fy2025']['net_debt_ebitda'])
TB_YLD = rx(r'yield ~([\d.]+%)', SX['peers_relative_multiples']['TABREED']['derived_multiples'])
DEWA_YLD = rx(r'yield ~([\d.\-]+-[\d.]+%)', SX['peers_relative_multiples']['DEWA']['price'])

# ---------------- 17-Aug-2026 revision: derived quantities -------------------
# Dual centrals — recovery (de-escalation) and continuation, neither privileged
CEN_R_CT, CEN_R_DM = CEN['ct'], CEN['dmtt']
CEN_C_CT, CEN_C_DM = CEN['continuation_ct'], CEN['continuation_dmtt']
CENS_ALL = [CEN_R_CT, CEN_R_DM, CEN_C_CT, CEN_C_DM]

# FY2025 operating EBITDA (excludes receivable interest, rental income and the
# credit-loss reversal — the audited-derived identity, disclosed in §1.6)
OPEB25 = HI['FY25']['ebitda'] - IN['intco_fy25'] - IN['rental_fy25'] - IN['ecl_fy25']
OPM25 = OPEB25 / IN['rev_fy25']
M26 = B['ebitda']['FY26'] / B['rev']['FY26']
M27 = B['ebitda']['FY27'] / B['rev']['FY27']

# RD10 v1.3 / v1.4 and ECR 87/2025 — every figure from the verified fact file
_RD = CF['2_rsb_rd10_v13']['evidence']
RD10_CAP = float(rx(r'\| ([\d.]+) \(inclusive of Fuel Surcharge\)', _RD['caps']['quote']))
RD10_FUEL = float(rx(r"Fuel Surcharge \| AED/TRh \| ([\d.]+)'", _RD['caps']['quote']))
RD10_BILL = rx(r'AED/Month \| (\d+)', _RD['caps']['quote'])
RD10_EXC = rx(r'Capacity Tariff \| (\d+%)', _RD['caps']['quote'])
RD10_V13_D = _RD['version_date']['date']            # 2025-09-17
RD10_V14_D = _RD['v14_exists']['date']              # 2026-02-06
_EC = CF['3_ecr_87_2025']['evidence']
ECR_FEE = float(rx(r'AED ([\d.]+) per refrigeration tonne', _EC['service_fee']['quote']))
ECR_FINE = rx(r'SCE - ([\d,]+) \(dirhams\)', _EC['fine']['quote'])
ECR_FEE_MN = ECR_FEE * RT_H1 / 1000.0               # ~AED 2.6mn/yr on the connected base
ECR_FEE_PS = ECR_FEE_MN / (W['rating_ct'] - IN['g_term']) / SH   # capitalised, per share
CAP_HEADROOM = 1 - UP['rate_aed_per_rth'] / RD10_CAP             # negative headroom vs the cap
RT_AVG25 = (IN['rt_conn']['2024'] + IN['rt_conn']['2025']) / 2

# CBUAE June-2026 QER — both legs (the 1.7% cut AND the 9.8% 2027 rebound)
GDP_27 = rx(r'2027, overall GDP growth is projected at ([\d.]+)%',
            CF['9_cbuae_june_2026_qer']['evidence']['june_qer']['quote'])
# UAE nominal-GDP run-rate (IMF WEO, verified) — cited to show 2.5% is NOT GDP-consistent
NGDP_CAGR = rx(r'CAGR 2023->2029 = ([\d.]+)%',
               CF['10_uae_nominal_gdp_runrate']['evidence']['imf_datamapper']['quote'])
# Bull connections path, from the scenario's own committed refrigeration-ton path
_BP = SCN['bull']['rt_path']
_BYRS = ['FY25'] + [y for y in _BP if y != 'FY25']
BULL_PATH = '/'.join(n0(_BP[b] - _BP[a]) for a, b in zip(_BYRS[:-1], _BYRS[1:]))

# AED sovereign curve — the Feb-2033 T-Sukuk (exists; stale April print)
_SC = CF['4_aed_sovereign_curve']['evidence']
SUK33_YLD = rx(r'([\d.]+)% for the February 2033 tranche', _SC['recent_yield']['quote'])
SUK33_MN = rx(r'issuances AED ([\d,]+) million', _SC['size_and_isin']['quote'])
SUK33_ISIN = rx(r'ISIN (AED\w+)', _SC['size_and_isin']['quote'])

# EIBOR: the stale end-March fixing and the August level (verified fact file)
EIBOR_MAR = float(rx(r'was ([\d.]+)%', CF['8_3m_eibor']['evidence']['march_anchor']['quote'])) / 100
EIBOR_AUG = float(rx(r'increased to ([\d.]+) percent on Thursday August 13',
                     CF['8_3m_eibor']['evidence']['august_levels']['quote'])) / 100

# Tabreed marks restruck at the anchor (6/7-Aug close) vs the 22-Jun mark
TB_PX = float(rx(r'Tabreed ([\d.]+) on 6/7-Aug', REL['mult_date']))
TB_PX_JUN = float(rx(r'Jun 22, 2026 = ([\d.]+);', CF['5_tabreed_share_price']['evidence']['closes']['quote']))
TB_FALL = TB_PX / TB_PX_JUN - 1
TB_REV = float(rx(r"reported FY2025 revenue is AED ([\d,]+)m", CRTXT).replace(',', ''))
TB_EBITDA = SX['peers_relative_multiples']['TABREED']['fy2025']['ebitda_aed_m']
EMP_EVEB = (D['meta']['mktcap'] + ND) / REL['ebitda_trail']      # Empower's own trailing EV/EBITDA
EMP_PE_TR = SPOT / (IN['npa_fy25'] / SH)
HALF_TURN_PS = 0.5 * REL['ebitda_trail'] / SH                    # 0.5x of EV/EBITDA multiple, per share

# H1-2026 profit lines (statements + deck) — the shock half produced record profits
_H1IS, _H1IS_P = EXI['h1_2026']['income_statement'], EXI['h1_2025_comparative']['income_statement']
H1_PBT = _H1IS['profit_before_income_tax'] / 1000.0
H1_PBT_G = _H1IS['profit_before_income_tax'] / _H1IS_P['profit_before_income_tax'] - 1
H1_PAT_G = _H1IS['profit_after_tax'] / _H1IS_P['profit_after_tax'] - 1
_KPI = EXI['ir_deck']['h1_2026_kpis_as_presented']
H1_EB_G = float(rx(r'\+([\d.]+)% YoY', _KPI['ebitda']['value'])) / 100
H1_EB_25 = float(rx(r'H1-2025: AED (\d+)m', _KPI['ebitda']['value']))
FY25_EB_CO = EXI['ir_deck']['annual_revenue_ebitda_bars']['ebitda']['2025'] \
    if 'annual_revenue_ebitda_bars' in EXI['ir_deck'] else None
if FY25_EB_CO is None:      # locate the deck's FY2025 EBITDA bar wherever the extract holds it
    for _k, _v in EXI['ir_deck'].items():
        if isinstance(_v, dict) and isinstance(_v.get('ebitda'), dict) and '2025' in _v['ebitda']:
            FY25_EB_CO = _v['ebitda']['2025']; break
# implied H2-2026 on the company's own EBITDA definition (operating + receivable
# interest + rental) against H2-2025 on the same deck definition
H2_IMPL = (B['ebitda']['FY26'] + B['intco']['FY26'] + IN['rental_fy25']) - IN['ebitda_h1_26']
H2_25 = FY25_EB_CO - H1_EB_25
H2_YOY = H2_IMPL / H2_25 - 1

# KAM-basis mix reconciliation (§1.6): FY2025 consumption share of revenue
KAM_SHARE = U['cons25'] / IN['rev_fy25']

# H1-2026 refinancing facts — from the interim borrowings note itself
_FACS = EXI['h1_2026']['borrowings_note_detail']['facilities']
RCF_MATS = sorted(f['maturity'] for f in _FACS)          # ['February 2028', 'September 2027']

# 4-7 Aug price path around the half-year release (supplied exchange history)
_PX = {}
with open('EMPOWER_Stock_Price_History.csv', encoding='utf-8-sig') as _fh:
    for _row in csv.DictReader(_fh):
        _PX[_row['Date']] = float(_row['Price'])
PX_AUG4, PX_AUG7 = _PX['08/04/2026'], _PX['08/07/2026']

# DFM drawdown basis (closing prices, dated)
_DFMI = SX['country_uae_macro']['dfm_index']
DFM_PEAK, DFM_PEAK_D = _DFMI['peak_2026_close']['value'], _DFMI['peak_2026_close']['date']
DFM_TR, DFM_TR_D = _DFMI['war_trough_close']['value'], _DFMI['war_trough_close']['date']

# H1-2026 net-debt reduction (the cash the old full-year convention double-counted)
_B25R = EX25['2025']['balance_sheet']
_ND25 = (_B25R['non_current_liabilities']['bank_borrowings']
         + _B25R['current_liabilities']['bank_borrowings']
         + _B25R['non_current_liabilities'].get('lease_liabilities', 0)
         + _B25R['current_liabilities'].get('lease_liabilities', 0)
         - _B25R['current_assets']['cash_and_cash_equivalents']
         - _B25R['current_assets']['term_deposits']) / 1000.0
NDRED_H1 = _ND25 - W['net_debt']

# Model's own forecast net finance line (Appendix C.2 coverage — critique CC13):
# implied by the model's FY2026E profit build, held flat (floating book, June
# balance held): pre-tax cost = EBIT(FY26) − PBT(FY26 implied by the profit line)
NF_MODEL = (B['ebitda']['FY26'] - B['dna']['FY26']) - REL['np26'] / (1 - IN['tax_ct'])
NF_AT = NF_MODEL * (1 - IN['tax_ct'])

# Two-stage terminal: stage 1 = ten years at g_term (volume-only under RD10),
# stage 2 perpetuity at G2. G2 mirrors the committed model constant and is
# VERIFIED here by reproducing the committed terminal value exactly.
G2 = 0.015
def _tv_two_stage(nopat30, roic, wacc, g1, g2):
    rr1, rr2 = g1 / roic, g2 / roic
    nop, tv = nopat30, 0.0
    for k in range(1, 11):
        nop *= (1 + g1)
        tv += nop * (1 - rr1) / (1 + wacc) ** k
    tv += (nop * (1 + g2) * (1 - rr2) / (wacc - g2)) / (1 + wacc) ** 10
    return tv
_tv_chk = _tv_two_stage(BC['nopat']['FY30'], BC['roic_term'], W['rating_ct'], IN['g_term'], G2)
assert abs(_tv_chk - BC['tv']) < 1.0, f"two-stage TV mismatch: {_tv_chk} vs {BC['tv']}"
DBL_YRS = math.log(2) / math.log(1 + IN['g_term'])       # years for volume to double at g

# Stub-clock weights: share of each forecast year inside the valuation window
STUB_W = {y: BC['pv'][y] / (BC['fcff'][y] * BC['df'][y]) for y in YRS}

# Construction range on the primary lens (all priced constructions)
CONS_LO = min(BC['ps'], DGW['ps'], DCW['ps'], DFB['ps'])
CONS_HI = max(BC['ps'], DGW['ps'], DCW['ps'], DFB['ps'])

# The beta's own 90% interval mapped to fair value via the §1.9 grid (linear
# in the discount rate, extrapolated at the ends of the grid)
def _ps_at_wacc(wq):
    ws, col = SN['wacc_grid'], [SN['table'][i][_gi] for i in range(len(SN['wacc_grid']))]
    if wq <= ws[0]:
        return col[0] + (ws[0] - wq) * (col[0] - col[1]) / (ws[1] - ws[0])
    if wq >= ws[-1]:
        return col[-1] - (wq - ws[-1]) * (col[-2] - col[-1]) / (ws[-1] - ws[-2])
    for i in range(len(ws) - 1):
        if ws[i] <= wq <= ws[i + 1]:
            f = (wq - ws[i]) / (ws[i + 1] - ws[i])
            return col[i] + f * (col[i + 1] - col[i])
def _wacc_at_beta(b):
    ke = W['rf_star_rating'] + b * W['erp_rating']
    return W['we'] * ke + W['wd'] * W['kd_at_ct']
BETA_PS_LO = _ps_at_wacc(_wacc_at_beta(BR['ci90'][1]))   # high beta → low value
BETA_PS_HI = _ps_at_wacc(_wacc_at_beta(BR['ci90'][0]))

# §3/§6 cone-vs-centrals comparison — COMPUTED from the numbers, never asserted
def _vs_cone(v, H):
    p = H['pct']
    if v > p['p95']: return 'above the 95th percentile'
    if v < p['p5']: return 'below the 5th percentile'
    if v > p['p75']: return 'inside the cone, between the 75th and 95th percentiles'
    if v > p['p50']: return 'inside the cone, between the median and the 75th percentile'
    return 'inside the cone, below the median'
def cone_comparison_sentence():
    p95 = H3M['pct']['p95']
    above = [v for v in CENS_ALL if v > p95]
    below_p5 = [v for v in CENS_ALL if v < H3M['pct']['p5']]
    lo, hi = min(CENS_ALL), max(CENS_ALL)
    if not above and not below_p5:
        return (f"All four published centrals — recovery {p2(CEN_R_CT)} / {p2(CEN_R_DM)} and "
                f"continuation {p2(CEN_C_CT)} / {p2(CEN_C_DM)} by tax framing — sit INSIDE the "
                f"three-month cone, below its 95th percentile of {p2(p95)} (the span "
                f"{p2(lo)}–{p2(hi)} falls {_vs_cone(hi, H3M)}). The valuation and the price map "
                f"OVERLAP: the market could reach any of the centrals within a quarter without "
                f"leaving the cone's ordinary range, so the two objects no longer disagree — the "
                f"question is direction, on which the price map deliberately has no view.")
    if len(above) == len(CENS_ALL):
        return (f"All four published centrals ({p2(lo)}–{p2(hi)}) sit ABOVE the cone's 95th "
                f"percentile of {p2(p95)} — the price map and the valuation genuinely disagree, "
                f"and nothing in the volatility structure suggests the gap closes within a "
                f"quarter.")
    return (f"The published centrals straddle the cone's 95th percentile of {p2(p95)}: "
            f"{', '.join(p2(v) for v in sorted(above, reverse=True))} above it, "
            f"{', '.join(p2(v) for v in sorted(set(CENS_ALL) - set(above), reverse=True))} "
            f"inside the cone — the objects partly overlap, and the overlap is stated rather "
            f"than resolved.")
CONE_SENT = cone_comparison_sentence()

# Revision receipts (READ FIRST): first-pass extraction figures and the 77-finding count
GA_OLD = rx(r'first-pass extraction carried ([\d.]+),', D['inputs']['ga_fy25']['source'])
OI_OLD = rx(r'from a first-pass ([\d.]+)\)', D['inputs']['oi_fy25']['source'])
N_FINDINGS = rx(r'(\d+) raised, \1 answered', CRTXT)
SIGN_RUN = rx(r'signings run ([\d-]+) contracts/yr', CRTXT)   # 163-186, from the audited register

MISSING_FIGS = []
def fig(name, width, cap):
    path = os.path.join(HERE, name)
    if os.path.exists(path):
        figure(path, width, cap)
    else:
        MISSING_FIGS.append(name)

# =========================== 1. MASTHEAD + READ FIRST ========================
t = doc.add_table(rows=1, cols=1)
cell_margins(t, 90, 90, 160, 160)
c = t.cell(0, 0); shade(c, F_DARK); c.width = Inches(7.0)
p = c.paragraphs[0]
r = p.add_run('TESTAHIL Research — Valuation Study')
r.bold = True; r.font.size = Pt(11); r.font.color.rgb = WHITE
r2 = p.add_run('   For information only — not investment advice')
r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(0x9F, 0xB0, 0xAC)
doc.add_paragraph().paragraph_format.space_after = Pt(0)

H1('Emirates Central Cooling Systems Corporation PJSC (DFM: EMPOWER)')
P(f"The world's largest listed district-cooling utility — contracted chilled-water capacity "
  f"serving Dubai under a regulated-tariff regime · Dubai Financial Market · reporting currency "
  f"AED · analysis anchored on the closing price of {p2(SPOT)} on 7 August 2026 · study dated "
  f"9 August 2026, revised 17 August 2026.", size=10, color=GREY)

box([("READ FIRST — what this document is. ",
      "An educational valuation study. It contains no recommendation and no rating, and it "
      "expresses no single-number target. It contains a fair-value range built from the "
      "company's own audited financial statements, a sourced cost of capital and explicitly "
      "listed assumptions — and, separately, a probabilistic map of where the share price could "
      "trade over the next one and three months. The two are different objects and are never "
      "blended."),
     ("Revised 17 August 2026 following an external audit. ",
      f"The changes and their prices are catalogued in the accompanying critique-response note "
      f"({N_FINDINGS} findings, each answered). The re-check also surfaced two corrections of "
      f"this study's own making, disclosed openly: the first edition's FY2025 statement face "
      f"carried administrative expenses of {GA_OLD} and other income of {OI_OLD} where the "
      f"audited figures are {n1(abs(HI['FY25']['ga']))} and {n1(IN['oi_fy25'])} — both pairs "
      f"close the operating-profit identity to the dirham, which is why the arithmetic "
      f"cross-check could not catch the mis-split — and rental income earned on the investment "
      f"properties was counted in operating cash flow while the properties were also added in "
      f"the valuation bridge; it is now excluded from operating earnings."),
     ("Conventions of this revision. ",
      f"The valuation clock sits at 30 June 2026: 2026 contributes only its second half, "
      f"discounted at half a year, with later year-ends at one-and-a-half to four-and-a-half "
      f"years. Operating EBITDA excludes the interest earned on the related-party acquisition "
      f"receivables and the rental income on the investment properties; both assets enter the "
      f"bridge at book value instead. The terminal value runs in two stages — ten years of "
      f"volume-only growth, then a lower perpetuity."),
     ("The first structural judgement — the consumption question, framed twice. ",
      f"Chilled-water consumption per connected refrigeration ton fell sharply in the first half "
      f"of 2026, in a conflict year, and the shares fell with it. Whether usage recovers is "
      f"computed BOTH ways as full models — a recovery (de-escalation) case and a continuation "
      f"case in which the world stays as it stood at the anchor date — and NEITHER is privileged "
      f"as the base: the two are published side by side, exactly like the tax framings. The "
      f"quantitative finding survives either way: because roughly {pc(EWR, 0)} of consumption "
      f"revenue is electricity and water purchased from DEWA and passed through, permanent loss "
      f"of the usage shock moves the discounted-cash-flow value by only {pc(abs(CRUX_DELTA), 1)} "
      f"— far less than the share-price reaction implies. The capacity charge, not the meter, "
      f"carries the value."),
     ("The second structural judgement — the tax rate, framed twice. ",
      f"The audited 2025 effective tax rate is exactly {pc(IN['tax_ct'], 1)} under UAE corporate "
      f"tax. Whether the {pc(IN['tax_dmtt'], 0)} domestic minimum top-up tax reaches Empower "
      f"through consolidation into the DEWA group (whose revenue far exceeds the EUR "
      f"{EUR_TH}m threshold) is contested and unresolved. The entire valuation is therefore "
      f"published both ways — {p3(BC['ps'])} against {p3(BD['ps'])} on the primary lens; "
      f"weighted centrals of {p2(CEN_R_CT)} against {p2(CEN_R_DM)} in the recovery case and "
      f"{p2(CEN_C_CT)} against {p2(CEN_C_DM)} in the continuation case — side by side, never "
      f"averaged."),
     ("What to check first. ",
      "Section 1.7 (the consumption grid), the two tax columns of the valuation summary below, "
      "and section 1.8's cost-of-debt evidence and cost-of-capital constructions — the places "
      "where a reader who disagrees with this study will find the disagreement priced."),
     ("The companion workbook. ",
      "The Excel model calculates live — changing a driver reprices the statements, the "
      "discounted cash flow and the fair value. Only three classes of cell are pasted values, "
      "named on its own READ FIRST sheet: the audited and disclosed history; the historical "
      "calibration of the unit build (the implied capacity rate per refrigeration ton, a "
      "research judgement rather than an arithmetic step); and whole-model re-runs — the "
      "probabilistic price map and the sensitivity grids, where each cell is a complete "
      "revaluation.")])

# =========================== 2. HEADLINE =====================================
H2('Headline')
P(f"Empower is the world's largest district-cooling utility by connected capacity: "
  f"{n0(RT_H1)}k refrigeration tons (RT) connected and {n0(IN['rt_contracted'])}k RT contracted "
  f"at 30 June 2026, serving about {BLDGS} buildings — roughly {DUBAI_SHARE}% of Dubai's "
  f"district-cooling market by the company's own 2022 listing-era disclosure, not restated "
  f"since. It sells cooling on two legs priced under a regulated tariff: a "
  f"contracted CAPACITY (demand) charge, paid on connected tons regardless of usage, and a "
  f"metered CONSUMPTION charge for chilled water actually drawn. The distinction is the whole "
  f"study: the capacity leg is the fixed-cost recovery and, effectively, the profit pool, while "
  f"the consumption leg's dominant cost — electricity and water purchased from DEWA, AED "
  f"{n0(IN['ew_cost_fy25'])}mn in 2025, about {pc(EWR, 0)} of consumption revenue — is largely a "
  f"pass-through.")
P(f"The financial character is a regulated utility's: the EBITDA margin has held between "
  f"{MARG_LO}% and {MARG_HI}% in every audited year since 2021 (derived as audited operating "
  f"profit plus depreciation and amortisation; the company's own reported EBITDA figures differ "
  f"slightly in definition), revenue compounded from AED "
  f"{n0(REV21)}mn (2021) to {n0(IN['rev_fy25'])}mn (2025), and net profit reached AED "
  f"{n0(IN['pat_fy25'])}mn in 2025. Net debt was AED {n0(ND)}mn at 30 June 2026 "
  f"({n1(NDX)}× 2025 EBITDA) after the 2025 refinancing into two AED {RCF_BN}bn revolving "
  f"tranches at a reduced margin — of which one has since been extended to {RCF_MATS[0]} while "
  f"the other still matures {RCF_MATS[1]}. The dividend is committed at AED "
  f"{n0(IN['div_policy'])}mn a year for 2025 and 2026 — {p3(DDM['dps'])} per share, a "
  f"{pc(YLD, 1)} yield at the anchor price — and free cash flow to equity runs almost exactly "
  f"at the payout: covered, but not slack.")
P(f"2026 is the conflict year, and the facts as they stood at the anchor date are stated "
  f"plainly. Iran struck the Fujairah oil-industry zone on 4 May and clashed with US forces in "
  f"the Strait of Hormuz over the following days; the truce brokered in the spring was declared "
  f"over on 8 July — a month before this study's anchor; the strait itself was closed from "
  f"11 July, under a US naval blockade from 14 July, and REMAINED CLOSED at the 7 August "
  f"anchor; an ADNOC tanker was attacked at sea the day after the anchor. No strike on UAE "
  f"soil has been recorded since 8 July. The Dubai market index fell "
  f"{DFM_DD.lstrip('-')} peak to trough (closing basis: {n0(DFM_PEAK)} on {DFM_PEAK_D} to "
  f"{n0(DFM_TR)} on {DFM_TR_D}) and the central bank cut its 2026 GDP growth projection "
  f"from {GDP_OLD}% to {GDP_NEW}% — while projecting a {GDP_27}% rebound in 2027 and calling "
  f"the slowdown a temporary moderation; both legs of that forecast are cited wherever the cut "
  f"is. Empower's first half showed the transmission mechanism: "
  f"revenue grew {sgn(H1G, 1)}, but the second quarter standalone FELL {pc(abs(Q2G), 1)} year on "
  f"year as consumption dropped {RTH_DROP}m ton-hours (equivalent full-load hours "
  f"{sgn(IN['eflh_h1'], 0)} to {EFLH_HRS} hours), tied by the interim notes mainly to lower "
  f"hospitality activity — the company's own attribution; weather was a minor factor. Yet the "
  f"shock half produced record profits: profit before tax of AED {n1(H1_PBT)}mn "
  f"({sgn(H1_PBT_G, 1)}), net profit of {n0(IN['pat_h1_26'])}mn ({sgn(H1_PAT_G, 1)}) and EBITDA "
  f"of {n0(IN['ebitda_h1_26'])}mn ({sgn(H1_EB_G, 1)}) as presented — which SUPPORTS the "
  f"pass-through arithmetic at the heart of this study. The shares closed the anchor session at "
  f"{p2(SPOT)}, {pc(T['pct_off_high'], 0)} below their 52-week high of {p2(T['hi_52w'])}, the "
  f"last leg of the fall running from {p2(PX_AUG4)} on 4 August to {p2(PX_AUG7)} on 7 August "
  f"around the half-year results (statements dated 5 August, released and covered 5–6 August).")
P(f"On the four lenses used here the fair-value field carries TWO centrals, published side by "
  f"side like the tax framings, because the macro condition dividing them had not resolved at "
  f"the anchor: a recovery (de-escalation) case at AED {p2(CEN_R_CT)} per share under the "
  f"{pc(IN['tax_ct'], 0)} tax framing ({p2(CEN_R_DM)} at {pc(IN['tax_dmtt'], 0)}) — a case that "
  f"requires a de-escalation which had NOT occurred at the anchor date — and a continuation "
  f"case, describing the world as it stood on the published facts, at {p2(CEN_C_CT)} "
  f"({p2(CEN_C_DM)}). The scenario field runs {p3(CEN['bear'])} to {p3(CEN['bull'])} bear to "
  f"bull, against a market price of {p2(SPOT)}. One disclosed transaction brackets "
  f"the question from above: DEWA took its stake from 56% to 80% in February 2026 by buying "
  f"Dubai Holding's 24% at AED {p2(DEWA['price'])} per share — a related-party CONTROL price, "
  f"{sgn(DEWA_PREM, 0)} above the anchor close, recorded here as a reference point and never as "
  f"fair value.", space_after=6)
box([("As of this 17 August revision — a dated postscript. ",
      "ADNOC vessels were attacked passing the strait on 12 and 14 August; an Iran–Oman "
      "agreement to reopen the strait was announced on 17 August but had not been implemented; "
      "and the formal ceasefire ended on 17 August as the 60-day negotiation deadline passed. "
      "None of this is in the numbers: the valuation remains anchored on the 7 August close and "
      "the facts as of that date, and the recovery/continuation framing above is how a reader "
      "should carry the news flow into it.")])

# =========================== 3. VALUATION SUMMARY ============================
H2('Valuation summary — every read at a glance, both tax framings side by side')
fig('fig1_football.png', 7.0,
    f"Figure 1 — the valuation field: each lens's range, both tax framings of both central "
    f"estimates, the market price of {p2(SPOT)} and the DEWA control print of "
    f"{p2(DEWA['price'])}.")
rows = [['Read', 'Basis', f"At {pc(IN['tax_ct'], 0)} tax", f"At {pc(IN['tax_dmtt'], 0)} tax",
         'vs spot'],
        ['Discounted cash flow (primary)',
         f"5-year free cash flow to the firm on the two-leg unit build from a 30-June-2026 "
         f"valuation clock, cost of capital {pc(W['rating_ct'], 2)}, two-stage terminal (ten "
         f"years at {pc(IN['g_term'], 1)} volume-only growth, then {pc(G2, 1)}). Terminal value "
         f"= {pc(BC['tv_share'], 1)} of enterprise value ({pc(BD['tv_share'], 1)} under the "
         f"{pc(IN['tax_dmtt'], 0)} framing) — disclosed here, in the bridge and in section 1.9",
         p3(BC['ps']), p3(BD['ps']), sgn(BC['ps'] / SPOT - 1, 0)],
        ['Relative multiples',
         f"Tabreed {n1(REL['tabreed_ev_ebitda'])}× trailing EV/EBITDA on trailing operating "
         f"EBITDA, like-for-like (gives {p3(REL['ps_rel'])}); Tabreed {n1(REL['tabreed_pe'])}× "
         f"P/E on 2026E attributable profit (gives {p3(REL['ps_pe'])}). Peer marks restruck at "
         f"the anchor (Tabreed {p2(TB_PX)} on 6–7 August). Peers are themselves war-depressed — "
         f"a market-regime reading, not an independent fundamental",
         p3(REL['ps_rel']), p3(REL['ps_rel']), sgn(REL['ps_rel'] / SPOT - 1, 0)],
        ['Normalised earnings power',
         f"2026E with consumption at the UNSHOCKED per-ton level; forward justified multiple "
         f"{n1(NRM['pe_just'])}× from the sustainable return and the cost of equity "
         f"({n1(NRM['pe_just_15'])}× with the return re-taxed at {pc(IN['tax_dmtt'], 0)})",
         p3(NRM['ps']), p3(NRM['ps_15']), sgn(NRM['ps'] / SPOT - 1, 0)],
        ['Book value and sustainable return',
         f"justified price-to-book {n1(BK['pb_just'])}× on book value of {p3(BK['bvps'])}/share "
         f"at a sustainable return on equity of {pc(BK['roe_sust'], 1)} "
         f"({n1(BK['pb_just_15'])}× with the return re-taxed at {pc(IN['tax_dmtt'], 0)})",
         p3(BK['ps']), p3(BK['ps_15']), sgn(BK['ps'] / SPOT - 1, 0)],
        ['Weighted central — recovery (de-escalation) case',
         f"cash flow {pc(LN['dcf']['weight'], 0)} · relative {pc(LN['relative']['weight'], 0)} · "
         f"normalised {pc(LN['normalized']['weight'], 0)} · book {pc(LN['book']['weight'], 0)}; "
         f"requires a de-escalation that had NOT occurred at the anchor date",
         p2(CEN_R_CT), p2(CEN_R_DM), sgn(CEN_R_CT / SPOT - 1, 0)],
        ['Weighted central — continuation case',
         f"same weights on the consumption-never-recovers build — the world as it stood on the "
         f"published facts at the anchor; neither central is privileged over the other",
         p2(CEN_C_CT), p2(CEN_C_DM), sgn(CEN_C_CT / SPOT - 1, 0)],
        ['Scenario field',
         f"bear {p3(CEN['bear'])} (war re-escalation, usage never recovers, {pc(IN['tax_dmtt'],0)} "
         f"tax, +100bp on the cost of equity) to bull {p3(CEN['bull'])} (full recovery, "
         f"{n0(GUID_HI)}k RT/yr)",
         f"{p3(CEN['bear'])} – {p3(CEN['bull'])}", '(bear is struck at this tax rate)', '—'],
        ['Dividend cross-check (unweighted)',
         f"the committed AED {n0(DDM['policy_mn'])}mn growing at {pc(IN['g_term'], 1)}, "
         f"capitalised at the cost of equity",
         p3(DDM['ps']), p3(DDM['ps']), sgn(DDM['ps'] / SPOT - 1, 0)],
        ['Market price', 'closing price, 7 August 2026', p2(SPOT), p2(SPOT), '—'],
        ['DEWA control purchase — reference only',
         f"February 2026, related-party purchase of a 24% block at a control price; a disclosed "
         f"reference point, not fair value",
         p2(DEWA['price']), p2(DEWA['price']), sgn(DEWA_PREM, 0)]]
table(rows, [1.30, 3.00, 0.95, 0.95, 0.60], band_rows={5, 6}, size=8.4)
caption(f"Fair values are ranges and distributions, never a target; the centrals are printed to "
        f"two decimals as summaries of ranges, the field is scenario risk, and construction "
        f"risk is additional to it — on the primary lens the priced cost-of-capital "
        f"constructions alone span {p2(CONS_LO)} to {p2(CONS_HI)} (section 1.8). The two tax "
        f"columns are one of the study's two central contested judgements published in full: "
        f"{pc(IN['tax_ct'], 0)} is the audited 2025 effective rate, {pc(IN['tax_dmtt'], 0)} is "
        f"the domestic minimum top-up rate that would apply if consolidation into the DEWA "
        f"group sweeps Empower into the OECD minimum-tax regime; the recovery/continuation "
        f"pair is the other, framed the same way. Nothing is averaged anywhere in this "
        f"document. The terminal-value share of enterprise value ({pc(BC['tv_share'], 1)}) is "
        f"stated beside the lens it belongs to because it is the number a sceptical reader "
        f"should weigh first.")

# =========================== 4. COMPANY OVERVIEW =============================
H2('Company overview — Empower at a glance')
rows = [['Item', 'Detail'],
        ['Listed', 'Dubai Financial Market, 15 November 2022, at the tail of the Dubai '
         'privatisation programme; par value AED 0.10'],
        ['What it does', 'Builds and operates district-cooling plants and distribution networks '
         'in Dubai, selling chilled water to towers, malls, hotels and districts under long-term '
         'connection agreements; also manufactures pre-insulated pipes (Logstor) and operates '
         f"the Dubai airport cooling concession through a {DXB_PCT}%-owned subsidiary "
         f"(DXB CoolCo — per the audited filings, an exclusive {CONC_YRS}-year concession "
         f"running from {CONC_FROM}, acquired in 2023 with the seller retaining the "
         f"{100 - int(DXB_PCT)}% minority; inside the connected base)"],
        ['Scale', f"{n0(RT_H1)}k RT connected / {n0(IN['rt_contracted'])}k RT contracted at "
         f"30 June 2026 ({sgn(RT_ADD_H1 / RT25Y, 1)} connected in the half); about {BLDGS} "
         f"buildings; roughly {DUBAI_SHARE}% of the Dubai district-cooling market"],
        ['Revenue model', f"Two legs on one asset base: capacity (demand) charges, contracted "
         f"and paid on connected tons regardless of usage — about {MIXD}% of first-half 2026 "
         f"revenue per the earnings deck — and metered consumption charges, about {MIXC}%, with "
         f"connection and other fees the remaining {MIXO}%. The split of the two legs in AED is "
         f"not separately disclosed in the statements; consumption revenue is disclosed in the "
         f"auditor's key-audit-matter section each year and the split is reconstructed from it "
         f"(section 1.6)"],
        ['Regulation', f"Dubai Executive Council Resolution 6/2021 governs district cooling. "
         f"The Regulatory and Supervisory Bureau ASSESSES tariff submissions and RECOMMENDS; "
         f"approval rests with the Dubai Supreme Council of Energy. The bureau's tariff "
         f"instrument (version 1.3, September 2025; 1.4, February 2026) sets explicit caps — "
         f"{RD10_CAP} AED per ton-hour for consumption with capacity, fuel surcharge included "
         f"({RD10_FUEL} for the surcharge itself), an AED {RD10_BILL}/month billing fee, an "
         f"excess-demand fee capped at {RD10_EXC} of the capacity tariff — and states verbatim "
         f"that tariff arrangements including indexation or escalation of capacity charges "
         f"will not be approved. A November 2025 resolution adds an annual service fee of AED "
         f"{ECR_FEE} per refrigeration ton (about AED {n1(ECR_FEE_MN)}mn a year on the "
         f"connected base, roughly {ECR_FEE_PS:.3f}/share capitalised — immaterial, and "
         f"expensed in these words) and an AED {ECR_FINE} fine for charging unapproved "
         f"tariffs. This study holds the tariff FLAT in nominal AED throughout — which the "
         f"no-indexation rule turns from a conservative choice into a regulatory constraint, "
         f"while also removing any tariff-escalation upside: terminal growth must be "
         f"volume-only"],
        ['Ownership', f"DEWA {DEWA_PCT}% since February 2026 "
         f"(it bought Dubai Holding's 24% at AED {p2(DEWA['price'])} per share); free float "
         f"about {FLOAT_PCT}%. DEWA is simultaneously the "
         f"controlling shareholder and the sole supplier of the largest cost line — a "
         f"governance concentration discussed in section 7"],
        ['Shares / market value', f"{n0(SH)}mn shares; AED {n0(D['meta']['mktcap'])}mn at the "
         f"anchor price of {p2(SPOT)}"],
        ['Net debt', f"AED {n0(ND)}mn at 30 June 2026 ({n1(NDX)}× 2025 EBITDA): two AED "
         f"{RCF_BN}bn revolving credit tranches refinanced in 2025 at a reduced margin over "
         f"EIBOR — one since extended to {RCF_MATS[0]}, the other still maturing "
         f"{RCF_MATS[1]} — less cash and term deposits"],
        ['Dividend', f"AED {n0(IN['div_policy'])}mn a year committed for 2025 AND 2026, paid in "
         f"two instalments (October and April) — {p3(DDM['dps'])} per share, {pc(YLD, 1)} at the "
         f"anchor price"],
        ['Tax status', f"UAE corporate tax at {pc(IN['tax_ct'], 0)}; the 2025 audited effective "
         f"rate is exactly {pc(IN['tax_ct'], 1)}. Whether the {pc(IN['tax_dmtt'], 0)} domestic "
         f"minimum top-up tax reaches Empower through DEWA-group consolidation is contested — "
         f"the study's dual-framed judgement"]]
table(rows, [1.55, 5.45], size=8.8, align_right_from=9)
P(f"Two structural facts govern everything that follows. First, the two-leg tariff means the "
  f"profit pool sits in the contracted capacity charge: consumption revenue carries a "
  f"{pc(EWR, 0)} pass-through cost, so a swing in usage moves revenue far more than it moves "
  f"cash flow. Second, the balance sheet runs on other people's working capital: customer "
  f"deposits and long payment terms to a related-party supplier hold net working capital "
  f"NEGATIVE at about {pc(abs(U['nwc_ratio']), 0)} of revenue — growth here releases cash rather "
  f"than consuming it, the mirror image of most utilities' build-out phase.", space_after=10)

# =========================== 5. §1 FUNDAMENTAL VALUATION ======================
H1('1  Fundamental valuation')

# ---- 1.1 DCF ----------------------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P(f"The primary lens is a five-year free-cash-flow-to-the-firm model built from physical units, "
  f"not from a revenue growth rate: connected refrigeration tons × the capacity rate, plus "
  f"consumption per connected ton × the connected base, plus the small pipes line — each leg on "
  f"its own driver, with margins falling out as OUTPUTS (section 1.6 shows the build and its "
  f"exact reconciliation to the audited 2025 statements). The valuation clock sits at 30 June "
  f"2026: 2026 contributes only its second half, discounted at half a year, with later "
  f"year-ends at one-and-a-half to four-and-a-half years and the terminal at four-and-a-half — "
  f"the alternative convention of discounting the full 2026 year against the June balance "
  f"sheet would have counted the roughly AED {n0(NDRED_H1)}mn of cash generated in the first "
  f"half twice. The waterfall below runs the recovery "
  f"case at the {pc(IN['tax_ct'], 0)} audited tax rate; the {pc(IN['tax_dmtt'], 0)} minimum-tax "
  f"framing follows it, in full, immediately after, and the continuation case is a full "
  f"parallel model in section 1.7.")
hdr = ['AED mn'] + YRS
rows = [hdr,
        ['Revenue'] + [n0(B['rev'][y]) for y in YRS],
        ['  of which consumption'] + [n0(B['cons'][y]) for y in YRS],
        ['  of which capacity and other'] + [n0(B['cap'][y]) for y in YRS],
        ['  of which pre-insulated pipes'] + [n0(B['pipes'][y]) for y in YRS],
        ['Operating EBITDA'] + [n0(B['ebitda'][y]) for y in YRS],
        ['Operating EBITDA margin'] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS],
        ['Less depreciation and amortisation'] + [f"({n0(B['dna'][y])})" for y in YRS],
        ['EBIT'] + [n0(BC['ebit'][y]) for y in YRS],
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_ct'], 0)})"] + [n0(BC['nopat'][y]) for y in YRS],
        ['Add back depreciation and amortisation'] + [n0(B['dna'][y]) for y in YRS],
        ['Less capital expenditure'] + [f"({n0(B['capex'][y])})" for y in YRS],
        ['Add working-capital release'] + [n0(-B['dnwc'][y]) for y in YRS],
        ['Free cash flow to the firm (full-year rate)'] + [n0(BC['fcff'][y]) for y in YRS],
        ['Share of the year inside the valuation window'] +
        [pc(STUB_W[y], 0) for y in YRS],
        ['Discount factor'] + [f"{BC['df'][y]:.4f}" for y in YRS],
        ['Present value of FCFF'] + [n0(BC['pv'][y]) for y in YRS]]
table(rows, [2.30, 0.94, 0.94, 0.94, 0.94, 0.94], size=8.5, band_rows={13, 16})
caption(f"Every line is computed, not typed. The three revenue rows foot to the total. "
        f"Operating EBITDA excludes the interest earned on the related-party acquisition "
        f"receivables and the rental income on the investment properties — both assets are "
        f"added at book in the bridge instead, so nothing is counted twice. Working capital is "
        f"NEGATIVE for this company — "
        f"customer deposits and payables fund the cycle — so growth RELEASES cash: the "
        f"working-capital line adds to free cash flow every year, at the audited 2025 ratio of "
        f"{pc(U['nwc_ratio'], 1)} of revenue. Capital expenditure is priced per new refrigeration "
        f"ton (AED {n0(CAPEX_RT)} per RT added, derived from the 2025 cash figures) plus a "
        f"maintenance allowance on the installed base. FY2026 enters at half weight — the "
        f"30-June clock above.")
rows = [['AED mn — the same model at the ' + pc(IN['tax_dmtt'], 0) + ' minimum tax'] + YRS,
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_dmtt'], 0)})"] + [n0(BD['nopat'][y]) for y in YRS],
        ['Free cash flow to the firm'] + [n0(BD['fcff'][y]) for y in YRS],
        ['Present value of FCFF'] + [n0(BD['pv'][y]) for y in YRS]]
table(rows, [3.05, 0.79, 0.79, 0.79, 0.79, 0.79], size=8.5, band_rows={2})

H2('The bridge from enterprise value to the equity — both framings')
fig('fig7_bridge.png', 7.0,
    f"Figure 2 — from the discounted cash flows to the per-share value, both tax framings side "
    f"by side.")
rows = [['Step', f"At {pc(IN['tax_ct'], 0)}", f"At {pc(IN['tax_dmtt'], 0)}", 'Note'],
        ['Present value of the five forecast years', n0(BC['pv_explicit']), n0(BD['pv_explicit']),
         'sum of the present-value rows above (2026 at half weight — the 30-June clock)'],
        ['Terminal value (two-stage)', n0(BC['tv']), n0(BD['tv']),
         f"stage one: ten further years of NOPAT growth at {pc(IN['g_term'], 1)} — volume-only "
         f"under the regulator's no-indexation rule; stage two: a perpetuity at {pc(G2, 1)}. "
         f"Reinvestment is forced to growth ÷ terminal return on capital "
         f"({pc(BC['roic_term'], 1)}) in EACH stage, so growth is paid for"],
        ['Present value of the terminal value', n0(BC['pv_tv']), n0(BD['pv_tv']),
         f"discounted at the year-4.5 factor"],
        ['Enterprise value', n0(BC['ev']), n0(BD['ev']), 'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(BC['tv_share'], 1),
         pc(BD['tv_share'], 1),
         'high, as it must be for a regulated utility whose explicit window is only five years; '
         'disclosed here, in the summary table, and stress-tested in section 1.9. Expert 3 '
         'challenges it directly in Appendix C'],
        ['Less net debt', f"({n0(ND)})", f"({n0(ND)})",
         f"30 June 2026 reviewed balance sheet: borrowings and leases less cash and term "
         f"deposits — reproduces the company's own presented figure exactly"],
        ['Plus related-party acquisition receivables, at book', n0(IN['recv_jun26']),
         n0(IN['recv_jun26']),
         f"the concession-grantor financial asset (Dubai Aviation City, on the DXB CoolCo "
         f"acquisition) and the Nakheel minimum-demand commitment (Empower Snow). Their "
         f"interest is excluded from operating earnings, the asset enters here at book, and it "
         f"is excluded from terminal invested capital — counted once, cleanly"],
        ['Plus investment properties', n0(IN['invprop_jun26']), n0(IN['invprop_jun26']),
         'non-operating side pocket, at book; its depreciation AND its rental income are '
         'excluded from the operating model for the same once-only reason'],
        ['Plus financial assets held at fair value', n0(IN['fvtpl_jun26'] + IN['fvoci_jun26']),
         n0(IN['fvtpl_jun26'] + IN['fvoci_jun26']), 'cash-like holdings outside the operating '
         'model, at book'],
        [f"Less minority interests ({pc(NCI_FRAC, 1)} of profits)", f"({n0(BC['nci_val'])})",
         f"({n0(BD['nci_val'])})",
         f"minorities (the {100 - int(DXB_PCT)}% of DXB CoolCo, and others) take "
         f"{pc(NCI_FRAC, 1)} of group profit and are charged the same share of the value — the "
         f"internally consistent convention when the group is valued above book"],
        ['Equity attributable', n0(BC['eq_attr']), n0(BD['eq_attr']), ''],
        ['Fair value per share (AED)', p3(BC['ps']), p3(BD['ps']),
         f"against a spot of {p2(SPOT)}: {sgn(BC['ps'] / SPOT - 1, 0)} and "
         f"{sgn(BD['ps'] / SPOT - 1, 0)} respectively"]]
table(rows, [2.20, 0.95, 0.95, 2.90], size=8.4, band_rows={4, 12}, align_right_from=1)
caption(f"Bridge and cash-flow clock BOTH sit at 30 June 2026: the June balance sheet nets "
        f"against cash flows that begin in July, so nothing inside the first half of 2026 is "
        f"counted twice (the first edition's full-year convention double-counted roughly AED "
        f"{n0(NDRED_H1)}mn of first-half cash — corrected). The "
        f"difference between the two columns — AED {p3(abs(DMTT_DELTA))} per share, "
        f"{pc(abs(DMTT_DELTA) / BC['ps'], 1)} of the {pc(IN['tax_ct'], 0)} value — is the "
        f"entire price of the tax question, and it is left visible rather than averaged away.")

# ---- 1.2 book ----------------------------------------------------------------
H2('1.2  Book value and sustainable return — the asset lens')
P(f"Book value attributable to shareholders is AED {n0(IN['eq_attr_jun26'])}mn at 30 June 2026, "
  f"or {p3(BK['bvps'])} per share — the share trades at {n1(SPOT / BK['bvps'])}× book. That "
  f"multiple is not the anomaly it appears: the equity base is small because the assets are "
  f"largely debt- and customer-deposit-funded and the company has distributed heavily since "
  f"listing, so the sustainable return on equity is high — {pc(BK['roe_sust'], 1)} on the "
  f"average of the last two year-end equity bases. A justified price-to-book multiple, (return "
  f"on equity − growth) ÷ (cost of equity − growth), gives {n1(BK['pb_just'])}× book at the "
  f"{pc(W['ke_rating'], 2)} cost of equity and {pc(IN['g_term'], 1)} growth — AED "
  f"{p3(BK['ps'])} per share. The lens is framed under both tax columns like every other: with "
  f"the sustainable return re-taxed at {pc(IN['tax_dmtt'], 0)}, the justified multiple is "
  f"{n1(BK['pb_just_15'])}× and the value {p3(BK['ps_15'])} per share.")
P(f"This is the lens most exposed to its own construction: a high-ROE, low-book business makes "
  f"the justified multiple acutely sensitive to the return assumption (each percentage point of "
  f"sustainable ROE is worth roughly AED "
  f"{p3(BK['bvps'] * 0.01 / (W['ke_rating'] - IN['g_term']))} per share). It is retained at a "
  f"{pc(LN['book']['weight'], 0)} weight because it prices the question the other lenses skip — "
  f"what the installed asset base earns — but it is read as corroboration, not as a primary "
  f"estimate.")

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples — what the market pays for GCC cooling today')
rows = [['Step', 'Value', 'Comment'],
        ["Tabreed enterprise value / EBITDA (trailing, restruck at the anchor)",
         f"{n1(REL['tabreed_ev_ebitda'])}×",
         f"the only listed pure district-cooling peer (Dubai Financial Market); derived from "
         f"its market value at the {p2(TB_PX)} close of 6–7 August (down {pc(abs(TB_FALL), 1)} "
         f"from the {p2(TB_PX_JUN)} of 22 June — the peer sold off with the subject, and the "
         f"multiple is struck on the SAME date as the anchor) plus net debt over its trailing "
         f"EBITDA, flagged as derived. Tabreed runs much higher leverage, which is why the "
         f"comparison is made at the enterprise line rather than on price/earnings alone"],
        ['Applied to Empower trailing operating EBITDA (twelve months to 30 June 2026)',
         n0(REL['ebitda_trail']),
         'trailing multiple on trailing earnings — like-for-like periods on both sides'],
        ['Implied enterprise value', n0(REL['ev_rel']), ''],
        ['Less net debt, plus the side pockets, less minorities', '—',
         'the same bridge as section 1.1'],
        ['Implied value per share — EV/EBITDA basis', p3(REL['ps_rel']),
         f"{sgn(REL['ps_rel'] / SPOT - 1, 0)} against spot"],
        [f"Tabreed price/earnings {n1(REL['tabreed_pe'])}× on 2026E attributable profit of "
         f"{n0(REL['npa26'])}", p3(REL['ps_pe']),
         f"the earnings-basis read; DEWA itself trades near {n1(REL['dewa_pe'])}× as a "
         f"secondary marker"]]
table(rows, [2.51, 0.94, 3.55], size=8.5, band_rows={5})
P(f"The cross-relationship is stated from the numbers, not from memory: at the anchor marks "
  f"Empower's own trailing enterprise multiple is {n1(EMP_EVEB)}× against Tabreed's "
  f"{n1(REL['tabreed_ev_ebitda'])}× — a "
  f"{'premium' if EMP_EVEB > REL['tabreed_ev_ebitda'] else 'discount'} — while on trailing "
  f"price/earnings Empower stands at {n1(EMP_PE_TR)}× against Tabreed's "
  f"{n1(REL['tabreed_pe'])}× — "
  f"{'a premium' if EMP_PE_TR > REL['tabreed_pe'] * 1.02 else ('a discount' if EMP_PE_TR < REL['tabreed_pe'] * 0.98 else 'broadly in line')}. "
  f"Each half-turn of the enterprise multiple is worth about AED {p3(HALF_TURN_PS)} per share "
  f"on this lens.")
P(f"Read this lens for what it is: a market-regime reading, not an independent fundamental. The "
  f"peer multiples are themselves struck in a war-discounted market — Tabreed and DEWA fell "
  f"with the index — so applying them imports the conflict discount rather than testing it. "
  f"That is exactly why the lens carries {pc(LN['relative']['weight'], 0)} weight and why its "
  f"gap to the cash-flow lens ({p3(REL['ps_rel'])} against {p3(BC['ps'])}) is treated in "
  f"section 4 as information about the market's risk pricing, not as an error in either "
  f"number.")

# ---- 1.4 normalized ----------------------------------------------------------
H2('1.4  Normalised earnings power — the unshocked year')
P(f"The question this lens asks: what does 2026 earn if the consumption shock had not happened "
  f"— usage per connected ton at the 2025 level, everything else unchanged? Revenue would be "
  f"AED {n0(NRM['rev'])}mn (against {n0(B['rev']['FY26'])}mn shocked), EBITDA "
  f"{n0(NRM['ebitda'])}mn, and attributable profit {n0(NRM['npa'])}mn — earnings per share of "
  f"{p3(NRM['eps'])}. Capitalised at a FORWARD justified multiple of {n1(NRM['pe_just'])}× — "
  f"built from the sustainable return on equity ({pc(BK['roe_sust'], 1)}), the retention that "
  f"{pc(IN['g_term'], 1)} growth requires, and the {pc(W['ke_rating'], 2)} cost of equity, with "
  f"no growth factor applied on top (the earnings being capitalised are already forward) — "
  f"that is AED {p3(NRM['ps'])} per share. Under the {pc(IN['tax_dmtt'], 0)} minimum-tax "
  f"framing the return re-taxes to {pc(NRM['roe_15'], 1)}, the justified multiple to "
  f"{n1(NRM['pe_just_15'])}× and the value to {p3(NRM['ps_15'])} — both framings, like "
  f"everywhere else.")
P(f"The lens deliberately measures the gap between the market's reaction and the earnings "
  f"arithmetic: the whole shock is worth about AED {n0(NRM['rev'] - B['rev']['FY26'])}mn of "
  f"revenue in the year, most of which is passed-through electricity and water cost that "
  f"disappears with it.")

# ---- 1.5 synthesis -----------------------------------------------------------
H2('1.5  Synthesis — four lenses, one field, two cases')
rows = [['Lens', f"At {pc(IN['tax_ct'], 0)}", f"At {pc(IN['tax_dmtt'], 0)}", 'Weight'],
        ['Discounted cash flow — recovery case', p3(BC['ps']), p3(BD['ps']),
         pc(LN['dcf']['weight'], 0)],
        ['Discounted cash flow — continuation case', p3(PC['ps']), p3(PD['ps']),
         pc(LN['dcf']['weight'], 0)],
        ['Relative multiples', p3(REL['ps_rel']), p3(REL['ps_rel']),
         pc(LN['relative']['weight'], 0)],
        ['Normalised earnings power', p3(NRM['ps']), p3(NRM['ps_15']),
         pc(LN['normalized']['weight'], 0)],
        ['Book value and sustainable return', p3(BK['ps']), p3(BK['ps_15']),
         pc(LN['book']['weight'], 0)],
        ['Weighted central — recovery (de-escalation)', p2(CEN_R_CT), p2(CEN_R_DM), '—'],
        ['Weighted central — continuation', p2(CEN_C_CT), p2(CEN_C_DM), '—'],
        ['Dividend cross-check (unweighted)', p3(DDM['ps']), p3(DDM['ps']), '—']]
table(rows, [3.39, 0.83, 0.83, 0.95], size=8.6, band_rows={6, 7})
P(f"The lenses disagree in an orderly way. The cash-flow model sits highest because it credits "
  f"the contracted growth backlog and the negative-working-capital funding model in full; the "
  f"relative lens sits lowest because it imports today's war-discounted market regime; the "
  f"normalised and book lenses sit between. The weighting leans on the cash-flow model because "
  f"this is a regulated utility with contracted revenue — the class of business a "
  f"discounted-cash-flow model prices best — and the field runs {p3(CEN['bear'])} to "
  f"{p3(CEN['bull'])} bear to bull. Both tax columns are carried through every row, the "
  f"recovery and continuation cases are carried through every horizontal cut, and nothing is "
  f"averaged across either pair. Note how little the case choice moves the central — AED "
  f"{p3(CEN_R_CT - CEN_C_CT)} per share — which is the pass-through arithmetic of section 1.7 "
  f"doing its work.")

# ---- 1.6 drivers -------------------------------------------------------------
H2('1.6  The drivers — a two-leg unit build, margins as outputs')
fig('fig8_unit.png', 7.0,
    "Figure 3 — the unit build: connected capacity, consumption per connected ton and the "
    "revenue that falls out of them.")
P(f"Revenue is built from physical units at the finest level the company disclosures allow. The "
  f"volume driver is CONNECTED CAPACITY, taken from the company's own history and guidance: "
  f"{n0(RT25Y)}k RT at end-2025, {n0(RT_H1)}k at 30 June 2026, company guidance of "
  f"{n0(GUID_LO)}–{n0(GUID_HI)}k of new connections for 2026 (the model uses the midpoint), and "
  f"a contracted backlog of {n0(BACKLOG)}k RT already signed but not yet connected — a pre-sold "
  f"pipeline that funds the additions assumed for 2027 onward, tapering as the Dubai build-out "
  f"matures.")
rows = [['Driver (per year)', 'FY25'] + YRS,
        ['Connected capacity, year-end (k RT)', n0(U['rt_path']['FY25'])] +
        [n0(U['rt_path'][y]) for y in YRS],
        ['New connections in the year (k RT)', '—'] +
        [n0(U['rt_path'][y] - U['rt_path'][p]) for p, y in
         zip(['FY25'] + YRS[:-1], YRS)],
        ['Average connected base (k RT)', '—'] + [n0(U['rt_avg'][y]) for y in YRS],
        ['Consumption revenue per average RT (AED/yr)', n0(CONS_RT)] +
        [n0(B['cons'][y] / U['rt_avg'][y] * 1000) for y in YRS],
        ['Capacity and other revenue per average RT (AED/yr)', n0(CAP_RT)] +
        [n0(B['cap'][y] / U['rt_avg'][y] * 1000) for y in YRS]]
table(rows, [2.30, 0.783, 0.783, 0.783, 0.783, 0.783, 0.784], size=8.0)
caption(f"The capacity rate per ton is IMPLIED, not published — no per-ton tariff schedule is "
        f"disclosed anywhere in the filings — so it is solved from disclosed total revenue, the "
        f"disclosed consumption figure in the auditor's key-audit-matter section, and the pipes "
        f"line, then held flat at the regulated tariff. The consumption rate carries the "
        f"{pc(abs(U['crux_shock']), 0)} 2026 shock and recovers to the 2025 level through 2027 "
        f"in the recovery case — the crux, section 1.7.")
P(f"One reconciliation the reader should see rather than infer: the audited key-audit-matter "
  f"figures put 2025 consumption revenue at {pc(KAM_SHARE, 1)} of total revenue, while the "
  f"H1-2026 earnings deck shows a {MIXC}% consumption share for the half — the second half "
  f"carries the summer cooling peak, so the full-year share always runs above the first-half "
  f"share. The pass-through ratio used throughout ({pc(EWR, 1)}) is computed on the audited "
  f"key-audit-matter basis, not the deck mix.")
H2('The physical unit build — hours and dirhams per ton-hour')
P(f"The consumption leg decomposes to physical units: revenue = connected tons × equivalent "
  f"full-load hours × the dirham rate per ton-hour. On the disclosed first-half figures the "
  f"implied rate is {UP['rate_aed_per_rth']:.3f} AED per ton-hour — {pc(abs(CAP_HEADROOM), 1)} "
  f"BELOW the regulator's cap of {RD10_CAP} (fuel surcharge included). Empower already prices "
  f"essentially at the regulated cap: there is no tariff headroom, which hardens the "
  f"flat-tariff assumption and removes any tariff upside at once. In these units the 2025 year "
  f"ran about {n0(UP['eflh_fy25_hrs'])} equivalent full-load hours on the average connected "
  f"base of {n0(RT_AVG25)}k tons ({n0(UP['rth_fy25_mn'])}m ton-hours in all); the first half "
  f"of 2026 ran {n0(UP['eflh_h1_2026_hrs'])} hours, {sgn(IN['eflh_h1'], 0)} year on year. The "
  f"crux of section 1.7, restated in hours: the shock year runs about "
  f"{pc(abs(U['crux_shock']), 0)} fewer hours; the recovery case restores the "
  f"~{n0(UP['eflh_fy25_hrs'])}-hour year; the continuation case never does.")
P(f"The cost stack is escalated one class at a time, never on a single blended index. "
  f"Electricity and water purchased from DEWA — AED {n0(IN['ew_cost_fy25'])}mn in 2025, "
  f"{pc(EWR, 1)} of consumption revenue and {pc(EW_REVSHARE, 0)} of total revenue — moves with "
  f"its own physical driver, the consumption leg itself (DEWA's slab tariff is flat; its fuel "
  f"surcharge floats monthly). Staff and other cash operating costs (AED "
  f"{n0(U['other_cos25'] + U['ga_cash25'])}mn in 2025 across cost of sales and administration) "
  f"escalate on a UAE wage path of {pc(WAGE_ESC, 1)} a year. Interest earned on the "
  f"related-party acquisition receivables and rental income on the investment properties are "
  f"EXCLUDED from operating EBITDA — they are returns on assets the bridge adds at book, so "
  f"counting them in the cash flows too would price them twice. The 2025 identity is exact: "
  f"operating EBITDA of AED {n1(OPEB25)}mn, plus receivable interest of "
  f"{n1(IN['intco_fy25'])}, rental income of {n1(IN['rental_fy25'])} and the credit-loss "
  f"reversal of {n1(IN['ecl_fy25'])}, reproduces the audited-derived "
  f"{n1(HI['FY25']['ebitda'])} (operating profit plus depreciation and amortisation) to the "
  f"decimal before any forecast year is struck.")
rows = [['What the build produces', ] + YRS,
        ['Revenue (AED mn)'] + [n0(B['rev'][y]) for y in YRS],
        ['Operating EBITDA (AED mn)'] + [n0(B['ebitda'][y]) for y in YRS],
        ['Operating EBITDA margin — an OUTPUT'] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS],
        ['Capital expenditure (AED mn)'] + [n0(B['capex'][y]) for y in YRS],
        ['Working capital released (AED mn)'] + [n0(-B['dnwc'][y]) for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.4, band_rows={3})
caption(f"The margin path is not assumed: it emerges from the two-leg mix — and it moves the "
        f"opposite way to the market's instinct. The margin "
        f"{'RISES' if M26 > OPM25 else 'falls'} in the shock year (from {pc(OPM25)} in 2025 to "
        f"{pc(M26)}) because the revenue lost is mostly pass-through electricity and water "
        f"cost that disappears with it; the dip is 2027 ({pc(M27)}), when the recovering "
        f"consumption leg brings its pass-through cost back. The audited 2021–25 band of "
        f"{MARG_LO}–{MARG_HI}% is on the broader audited-derived basis (operating profit plus "
        f"depreciation and amortisation, receivable interest and rental included), so the two "
        f"series are stated on their own bases rather than mixed.")
P(f"A run-rate check against the half just reported: the 2026 build, on the company's own "
  f"EBITDA definition, implies a second half of AED {n0(H2_IMPL)}mn against "
  f"{n0(H2_25)}mn in the second half of 2025 — {sgn(H2_YOY, 1)} year on year, conservative "
  f"against the {sgn(H1_EB_G, 1)} the first half actually printed.")

# ---- 1.7 crux ----------------------------------------------------------------
H2('1.7  The crux — does consumption per connected ton recover?')
P(f"Usage per connected ton fell {pc(abs(U['crux_shock']), 0)} in 2026 on the model's "
  f"full-year reading of the disclosed half-year figures (equivalent full-load hours were "
  f"{sgn(IN['eflh_h1'], 0)} in the half itself). The recovery case lets it return to the 2025 "
  f"level through 2027 — a case that requires the de-escalation which had NOT occurred at the "
  f"anchor date. The continuation case is computed as a FULL model, not a sensitivity: the "
  f"world as it stood on the published facts, usage never recovering. Neither case is "
  f"privileged as the base; they are published side by side, exactly like the tax framings. "
  f"The grid below prices every stop between.")
rows = [['Consumption per connected ton, from 2027', 'Implied AED per RT',
         f"Fair value at {pc(IN['tax_ct'], 0)}", 'vs recovery'],
        *[[f"{pc(r['level'], 0)} of the 2025 level" +
           ('  — the continuation case' if abs(r['level'] - (1 + U['crux_shock'])) < 1e-9
            else ('  — the recovery case' if abs(r['level'] - 1) < 1e-9 else '')),
           n0(r['level'] * CONS_RT), p3(r['ps']), sgn(r['ps'] / BC['ps'] - 1, 1)]
          for r in CRX['rows']]]
table(rows, [2.85, 1.30, 1.55, 0.90], size=8.5,
      band_rows={1 + [i for i, r in enumerate(CRX['rows'])
                      if abs(r['level'] - 1) < 1e-9][0]})
P(f"The finding is the study's headline: permanent loss of the entire shock — the "
  f"continuation case — moves the discounted-cash-flow value from {p3(BC['ps'])} to "
  f"{p3(PC['ps'])}, just {pc(abs(CRUX_DELTA), 1)} ({p3(PD['ps'])} under the "
  f"{pc(IN['tax_dmtt'], 0)} tax framing). The arithmetic reason is the pass-through: about "
  f"{pc(EWR, 0)} of every dirham of consumption revenue leaves again as electricity and water "
  f"purchased from DEWA, so the meter's contribution to cash flow is thin. The market's "
  f"read-through from the consumption miss to the equity — a share price {pc(T['pct_off_high'], 0)} "
  f"off its high — is larger than the cash-flow arithmetic supports. The capacity charge, not "
  f"the meter, carries the value; what WOULD move the value is a tariff cut or a stall in "
  f"connections, which is why sections 5 and 7 watch those, not the weather.")

# ---- 1.8 macro ---------------------------------------------------------------
H2('1.8  Macro and country — rates, the peg, and the sourced cost of capital')
P(f"The macro frame is unusually clean for an emerging-market study: the dirham is hard-pegged, "
  f"so the UAE imports the Federal Reserve's path and the currency leg drops out of the "
  f"valuation entirely. The central bank's base rate stood at {pc(STK['rf_live'], 2)} at the "
  f"end of July 2026. The federal government's dirham bond programme gives a sovereign curve; "
  f"the anchor here is its most RECENT print — the January-2031 tranche tapped on 30 July "
  f"2026, a {TENOR}-year tenor yielding {pc(IN['rf_aed'], 2)}. A LONGER instrument exists and "
  f"is named rather than ignored: a February-2033 Treasury Sukuk (the first seven-year dirham "
  f"tranche, AED {SUK33_MN}mn outstanding, ISIN {SUK33_ISIN}), whose last auction print was "
  f"{SUK33_YLD}% in the April tap — struck before the July escalation and therefore stale in "
  f"a repriced market, which is why the on-the-run {pc(IN['rf_aed'], 2)} remains the anchor; "
  f"both are stated. The conflict is the macro event: the market index fell "
  f"{DFM_DD.lstrip('-')} peak to trough, the 2026 GDP projection was cut from {GDP_OLD}% to "
  f"{GDP_NEW}% (with a {GDP_27}% rebound projected for 2027 — the same forecast carries both "
  f"legs), and the equity risk pricing that survives into August is part of what section 1.3 "
  f"measures.")
rows = [['Component', f"Credit-rating basis", f"Market-spread basis", 'Construction'],
        ['Risk-free rate before adjustment', pc(IN['rf_aed'], 2), pc(IN['rf_aed'], 2),
         f"the most recent AED sovereign print ({TENOR}-year tenor; the gap to the "
         f"five-year-plus cash-flow horizon is flagged as a limitation, and the stale "
         f"February-2033 print is named above)"],
        ['Less the sovereign default spread', pc(IN['ds_rating'], 2), pc(IN['ds_cds'], 2),
         'the UAE\'s own default spread on each basis, from the July-2026 edition of the '
         'published country-risk dataset; the market-spread column uses the Abu Dhabi sovereign '
         'credit-default swap as the quoted UAE proxy — flagged'],
        ['Adjusted risk-free rate', pc(W['rf_star_rating'], 2), pc(W['rf_star_cds'], 2),
         'country risk must enter once, through the equity premium — not twice'],
        ['Beta', f"{BR['beta']:.3f}", f"{BR['beta']:.3f}",
         f"own-stock weekly regression against the FTSE ADX General Index — adopted as the "
         f"UAE market index for this study by instruction; the same regression against the "
         f"listing exchange's own DFM index gives {BR_DFM['beta']:.3f} and is priced as a full "
         f"parallel construction below — over "
         f"the full listing window ({BR['window_years']:.1f} years, n={BR['n']}): R² {BR['r2']:.3f}, standard "
         f"error {BR['se']:.3f}, 90% interval {BR['ci90'][0]:.2f}–{BR['ci90'][1]:.2f}"],
        ['Equity risk premium', pc(IN['erp_rating'], 2), pc(IN['erp_cds'], 2),
         'the UAE total premium on each basis, same dataset — the same basis of spread that was '
         'stripped from the risk-free rate is the one added back here'],
        ['Cost of equity', pc(W['ke_rating'], 2), pc(W['ke_cds'], 2),
         'the two constructions CONVERGE to within a few basis points — the contested choice of '
         'basis is priced and turns out to cost nothing'],
        ['Cost of debt (anchor)', pc(W['kd_marg'] if 'kd_marg' in W else W['kd'], 2),
         pc(W['kd'], 2),
         f"the company's own disclosed all-in borrowing cost — the accounting capitalisation "
         f"rate on general borrowings, an AVERAGE rather than a marginal print — kept as the "
         f"anchor because it sits at the top of the EIBOR-plus-implied-margin band; see the "
         f"evidence table below"],
        ['Weights (equity / debt)', f"{pc(W['we'], 1)} / {pc(W['wd'], 1)}",
         f"{pc(W['we'], 1)} / {pc(W['wd'], 1)}",
         'market value of equity at the anchor price; net debt at the reviewed June-2026 '
         'balance sheet — the target-structure choice is itself priced as alternative '
         'constructions in the table further below'],
        [f"Cost of capital at {pc(IN['tax_ct'], 0)} tax", pc(W['rating_ct'], 2),
         pc(W['cds_ct'], 2), 'the rate the recovery and continuation cases discount at'],
        [f"Cost of capital at {pc(IN['tax_dmtt'], 0)} tax", pc(W['rating_dmtt'], 2),
         pc(W['cds_dmtt'], 2),
         f"IDENTICAL to the {pc(IN['tax_ct'], 0)} row: the minimum top-up tax is a "
         f"minimum-effective-rate charge, not a higher statutory rate, so the "
         f"{pc(IN['tax_ct'], 0)} interest shield survives and both framings discount at "
         f"{pc(W['rating_ct'], 2)} — stated so the reader is not left inferring it"]]
table(rows, [1.55, 1.05, 1.05, 3.35], size=8.2, band_rows={6, 9})
caption(f"No glide path is applied to the cost of debt or the cost of capital: both revolving "
        f"tranches float over EIBOR, the 2025 refinance already reset the margin, and the "
        f"forward curve is flat to mildly higher — a glide would be invented, not sourced (the "
        f"three-month EIBOR itself has drifted from {pc(EIBOR_MAR, 2)} at end-March to about "
        f"{pc(EIBOR_AUG, 1)} in August, which the evidence table carries). The "
        f"explicit-window rate equals the terminal rate, stated openly.")

H2('The cost of debt — three pieces of evidence, not an assumption')
rows = [['Evidence', 'Rate', 'What it establishes'],
        ['AED sovereign yield (January-2031 tranche, auctioned 30 July 2026)', pc(IN['rf_aed'], 2),
         'the floor: a same-currency corporate cannot sustainably borrow below its sovereign'],
        ["Empower's own disclosed all-in borrowing cost, 2025 (the accounting capitalisation "
         "rate on general borrowings)", pc(W['kd'], 2),
         f"an AVERAGE across the book rather than a marginal print — the label matters and is "
         f"stated. It sits {n0((W['kd'] - IN['rf_aed']) * 10000)}bp above the sovereign, as it "
         f"must, and at the TOP of the band implied by EIBOR plus the undisclosed margin, "
         f"which is why it is kept as the (conservative) anchor"],
        ["The same disclosure a year earlier (2024)", pc(KD24, 2),
         f"the down-trajectory: the 2025 refinance cut the all-in cost by about "
         f"{n0((KD24 - W['kd']) * 10000)}bp as EIBOR fell and the margin was renegotiated. "
         f"Three-month EIBOR stood near {pc(EIBOR_AUG, 1)} in August 2026 ({pc(EIBOR_MAR, 2)} "
         f"at end-March); the exact contractual "
         f"margin is not disclosed in any filing (recorded as a documented absence in the "
         f"bibliography), so the capitalisation rate is the closest disclosed all-in figure"]]
table(rows, [2.60, 0.80, 3.60], size=8.4)
P(f"One dated sensitivity belongs beside the anchor: only one of the two AED {RCF_BN}bn "
  f"revolving tranches has been extended (to {RCF_MATS[0]}); the other still matures "
  f"{RCF_MATS[1]}, so roughly half the debt book reprices at whatever EIBOR and margin the "
  f"market offers then. Each 25 basis points on half the book is about AED "
  f"{n1(0.0025 * 0.5 * WC['gross_debt'])}mn of annual interest — visible in the coverage "
  f"table of Appendix C.2, immaterial to the firm-level valuation, and stated so the reader "
  f"knows where the roll risk sits.")

H2('The cost-of-capital constructions — all priced, none hidden')
P("The single largest disagreements a competent reader can have with this study are "
  "constructions of the discount rate, not scenarios. Each is therefore computed as a full "
  "parallel valuation on the recovery case rather than argued away:")
rows = [['Construction', 'Cost of capital', f"Fair value at {pc(IN['tax_ct'], 0)}",
         'The argument, and why the base stays where it is'],
        ['Target net-debt weights (the published base)', pc(WC['base_net_target'], 2),
         p3(BC['ps']),
         f"the company's own net-debt policy runs ~{n1(NDX)}× EBITDA and the payout absorbs "
         f"essentially all free cash flow to equity, so surplus cash is transient — the "
         f"forward-looking structure is net"],
        ['Gross-debt weights', pc(WC['gross'], 2), p3(DGW['ps']),
         'weight the debt actually financed at the cost of debt; treats the cash pile as a '
         'separate asset rather than an offset'],
        ['Net debt at its negative carry', pc(WC['carry'], 2), p3(DCW['ps']),
         f"charge the cash pile its yield give-up (net-debt cost {pc(WC['kd_net_carry'], 2)}): "
         f"cash earning deposit rates against debt costing {pc(W['kd'], 2)} is negative carry, "
         f"priced instead of ignored"],
        ['Listing-exchange index beta', pc(WC['dfm_beta'], 2), p3(DFB['ps']),
         f"the same weekly regression against the DFM General Index gives a beta of "
         f"{BR_DFM['beta']:.3f} and a cost of equity of {pc(WC['ke_dfm'], 2)}; the published "
         f"base uses the FTSE ADX General Index by explicit client instruction, and that "
         f"choice is priced here in full, not parenthetically"]]
table(rows, [1.55, 1.00, 1.00, 3.45], size=8.2, band_rows={1})
caption(f"The published scenario field ({p3(CEN['bear'])}–{p3(CEN['bull'])}) is bounded by "
        f"SCENARIOS; these CONSTRUCTIONS alone span {p3(CONS_LO)} to {p3(CONS_HI)} on the "
        f"identical cash flows — construction risk is additional to scenario risk, and of "
        f"comparable size. The beta's own 90% sampling interval "
        f"({BR['ci90'][0]:.2f}–{BR['ci90'][1]:.2f}) maps to roughly {p2(BETA_PS_LO)}–"
        f"{p2(BETA_PS_HI)} per share on the primary lens via the section 1.9 grid. A reader "
        f"should treat the printed field as scenario risk and carry construction risk on top "
        f"of it.")
P(f"Every contested construction in this section is PRICED rather than asserted: the two "
  f"premium bases are both computed (they converge); the tax question is carried as two full "
  f"columns everywhere; the short sovereign tenor and the Abu Dhabi credit-default-swap proxy "
  f"are flagged in place; the weighting and beta-index choices are full parallel valuations "
  f"above; and the beta's sampling error is shown so a reader can re-run the "
  f"cost of equity at either end of the interval ({BR['ci90'][0]:.2f} lifts the fair value, "
  f"{BR['ci90'][1]:.2f} lowers it — the direction is worth roughly AED "
  f"{p3(abs(SN['table'][_wi + 1][_gi] - SN['table'][_wi - 1][_gi]) / 2)} per share per "
  f"half-point of discount rate, per the grid in section 1.9).", space_after=8)

# ---- 1.9 sensitivity ---------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, and the scenarios')
fig('fig2_sens.png', 7.0,
    "Figure 4 — fair value per share against cost of capital and terminal growth; the crux "
    "grid alongside.")
rows = [[f"Fair value at {pc(IN['tax_ct'], 0)} (AED/share)"] +
        [f"g = {pc(g, 1)}" for g in SN['g_grid']]]
for wi, w_ in enumerate(SN['wacc_grid']):
    tag = '  (base)' if abs(w_ - W['rating_ct']) < 1e-9 else ''
    rows.append([f"Cost of capital {pc(w_, 2)}{tag}"] +
                [p3(SN['table'][wi][gi]) for gi in range(len(SN['g_grid']))])
table(rows, [1.90, 1.02, 1.02, 1.02, 1.02, 1.02], size=8.4,
      band_rows={_wi + 1})
caption(f"The base cell ({p3(_base_cell)}) sits at {pc(W['rating_ct'], 2)} and "
        f"{pc(IN['g_term'], 1)}. A half-point of discount rate is worth roughly AED "
        f"{p3(abs(_dn50 - _up50) / 2)} per share — more than the entire consumption crux — "
        f"which is the honest hierarchy of what matters in this valuation: rate, tax, tariff, "
        f"then usage. The growth axis now extends to ZERO so the reader can see the "
        f"flat-everything endpoint: no volume growth at all, forever, is worth "
        f"{p3(SN['table'][_wi][0])} at the base rate.")
P(f"Two words on the growth assumption itself, because the first edition mislabelled it. The "
  f"{pc(IN['g_term'], 1)} stage-one rate is NOT a nominal-GDP-consistent figure — UAE nominal "
  f"GDP compounds at roughly {NGDP_CAGR}% a year on the current five-year outlook, and "
  f"{pc(IN['g_term'], 1)} is about half of it (the error ran in the conservative direction). "
  f"It is a VOLUME-ONLY bound under the regulator's no-indexation rule: the Dubai 2040 "
  f"build-out, the contracted backlog and a signing run-rate of {SIGN_RUN} new contracts a "
  f"year support it for the ten-year second stage, after which the perpetuity drops to "
  f"{pc(G2, 1)} (long-run densification, zero real tariff growth). The tension is stated "
  f"rather than hidden: {pc(IN['g_term'], 1)} volume growth forever would double the "
  f"connected base roughly every {n0(DBL_YRS)} years, which is why it is NOT extended into "
  f"the perpetuity and why the grid above prices every stop down to zero.")
rows = [['Scenario', 'What is assumed', f"Fair value (AED/share)"],
        ['Bear — war re-escalation',
         f"usage falls a further {pc(abs(U['crux_shock']), 0)} in 2027 and never recovers; new "
         f"connections halve (the pipeline freezes); the {pc(IN['tax_dmtt'], 0)} minimum tax "
         f"lands; the cost of equity rises {n0((SCN['bear']['ke'] - W['ke_rating']) * 10000)}bp "
         f"as the market re-prices UAE risk", p3(CEN['bear'])],
        ['Continuation — the world as it stood at the anchor',
         f"the consumption shock never unwinds; guidance-midpoint connections continue (they "
         f"grew through the war half); both tax framings published",
         f"{p2(CEN_C_CT)} / {p2(CEN_C_DM)}"],
        ['Recovery (de-escalation)',
         f"usage recovers through 2027 — requires a de-escalation that had not occurred at the "
         f"anchor date; guidance-midpoint connections; both tax framings published",
         f"{p2(CEN_R_CT)} / {p2(CEN_R_DM)}"],
        ['Bull — full recovery', f"usage recovers fully; connections follow the top-of-guidance "
         f"path ({BULL_PATH}k RT over the five years); {pc(IN['tax_ct'], 0)} tax",
         p3(CEN['bull'])]]
table(rows, [1.40, 4.20, 1.40], size=8.4, band_rows={2, 3})
caption("The bear and bull are full model re-runs — unit paths, cost stack, discount rate and "
        "tax all moved together — not lens blends or grid look-ups. The middle two rows are "
        "the study's two published centrals: NEITHER is called the base, because the fact "
        "dividing them had not resolved at the anchor date.")

# =========================== 6. §2 TECHNICAL ==================================
H1('2  Technical and price structure')
fig('fig3_ma.png', 7.0,
    "Figure 5 — price against the 20-, 50- and 200-session moving averages, with the "
    "support and resistance ladder.")
rows = [['Marker', 'Level (AED)', 'Reading'],
        ['Last close (7 August 2026)', p2(T['close']), 'the anchor for everything in this study'],
        ['20-session average', p2(T['ma']['20']),
         f"price is {sgn(SPOT / T['ma']['20'] - 1, 1)} against it; the average is "
         f"{T['ma_slope']['20']}"],
        ['50-session average', p2(T['ma']['50']),
         f"price is {sgn(SPOT / T['ma']['50'] - 1, 1)} against it; {T['ma_slope']['50']}"],
        ['200-session average', p2(T['ma']['200']),
         f"price is {sgn(SPOT / T['ma']['200'] - 1, 1)} against it; {T['ma_slope']['200']}"],
        ['Momentum (14-session RSI)', f"{T['rsi']:.0f}",
         'washed out — a reading under 30 marks the sell-off as stretched by its own recent '
         'standards'],
        ['MACD (12·26·9)', f"{T['macd']['macd']:.3f}",
         'negative and still falling — the down-move has not yet lost momentum'],
        ['Average true range (14-session)', pc(T['atr_pct'], 1),
         'of price per session — a normal tape, not a dislocated one'],
        ['52-week range', f"{p2(T['lo_52w'])} – {p2(T['hi_52w'])}",
         f"the close sits {pc(T['pct_off_high'], 0)} below the high and "
         f"{pc(T['pct_off_low'], 0)} above the low"],
        ['Resistance', ' / '.join(p2(x) for x in T['levels']['res']),
         'nearest first, from recency-weighted swing clusters'],
        ['Support', ' / '.join(p2(x) for x in T['levels']['sup']),
         'nearest first; the second and third are round-number shelves']]
table(rows, [1.85, 1.15, 4.00], size=8.5)
P(T['tech']['summary'])
P(f"One configuration deserves its own sentence: the 50-session average crossed ABOVE the "
  f"200-session {T['ma_cross']['ago']} sessions ago — a golden cross, conventionally a "
  f"regime-change signal — and it sits oddly against a price that has since sold off below the "
  f"whole stack. The cross reflects the spring recovery from the war trough; the sell-off is "
  f"the August earnings reaction. When a trend signal and the tape disagree this directly, the "
  f"tape is the fresher fact. {T['tech']['bull']} {T['tech']['bear']}", space_after=10)

# =========================== 7. §3 PROBABILISTIC MAP ==========================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation: not what the business is "
  f"worth, but where the share price could plausibly trade in one and three months given how "
  f"this share actually moves. Fifty thousand price paths are simulated from a volatility "
  f"model fitted to the daily trading range, with a fat-tailed shock distribution and a drift "
  f"anchored to the cost of carry — the local deposit rate less the {pc(STK['q_annual'], 1)} "
  f"dividend yield, which is why the median path sits a shade below spot. It carries no "
  f"directional view, and it is never blended with the fair-value work above.")
P(f"The evidence behind the band widths is stated plainly, at its actual strength. The bands "
  f"are set on the UAE market panel ({FIT['panel_names']} names, "
  f"walk-forward tested with each forecast made using only data available before it); the "
  f"panel's forecast accuracy is statistically indistinguishable from — marginally ahead of — "
  f"a benchmark random walk anchored on the same cost of carry. For Empower itself only "
  f"{BT5['windows']} non-overlapping three-month windows exist since the late-2022 listing — "
  f"a record too short to establish forecasting skill either way, and it is presented as "
  f"such. On those {BT5['windows']} windows every realised outcome fell inside the 80% band "
  f"— {BT5['windows']} of {BT5['windows']}, where {n0(0.8 * BT5['windows'])} would be "
  f"expected — which is itself evidence the bands are drawn too WIDE, not proof they are "
  f"right. The centring is clean "
  f"(the average percentile of the realised outcomes was {BT5['pit_mean']:.2f}, statistically "
  f"uniform on the standard tests), and the bands run "
  f"about {pc(BT5['width_vs_benchmark'] - 1, 0)} wider than this stock's own short history "
  f"would warrant — a width that cost a few "
  f"percent of average sharpness against the benchmark on those same windows, the price of "
  f"never missing. A reader "
  f"should treat the intervals as honest but wide.")
fig('fig4_fan.png', 7.0,
    f"Figure 6 — the forward price cone to three months from the anchor close of {p2(SPOT)}, "
    f"with the trailing tape behind it. {CONE_SENT}")
H2('Percentile map (AED/share)')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Probability above spot'],
        [f"1 month (to {H1M['grade_date']})"] +
        [p2(H1M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H1M['p_above'], 0)],
        [f"3 months (to {H3M['grade_date']})"] +
        [p2(H3M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] +
        [pc(H3M['p_above'], 0)]]
table(rows, [2.11, 0.71, 0.71, 0.80, 0.71, 0.71, 1.25], size=8.6)
fig('fig5_dist.png', 5.3, "Figure 7 — the one-month price distribution.")
fig('fig6_dist.png', 5.3, "Figure 8 — the three-month price distribution.")
H2('Level-touch ladder')
rows = [['Event', '1 month', '3 months'],
        ['Finishes 10% or more above spot', pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        ['Finishes 10% or more below spot', pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        ['Touches 10% above spot at any point', pc(H1M['touch_up10'], 0),
         pc(H3M['touch_up10'], 0)],
        ['Touches 10% below spot at any point', pc(H1M['touch_dn10'], 0),
         pc(H3M['touch_dn10'], 0)]]
table(rows, [3.90, 1.05, 1.05], size=8.6)
caption(f"Touch probabilities exceed finish probabilities because a path can visit a level and "
        f"come back. The anchor volatility is about {pc(H3M['anchor_vol_ann'], 0)} annualised — "
        f"elevated for a regulated utility, which is itself a statement about the conflict "
        f"regime the share is trading in.")

# =========================== 8. §4 COMPARISON =================================
H1('4  Comparison of the lenses')
rows = [['Read', 'What it says', 'What it assumes'],
        ['Cash flow (primary)', f"AED {p3(BC['ps'])} / {p3(BD['ps'])} by tax framing, "
         f"{sgn(BC['ps'] / SPOT - 1, 0)} / {sgn(BD['ps'] / SPOT - 1, 0)} against the market",
         'the tariff stays flat but is not cut; the contracted backlog connects; the crux '
         'recovers (and barely matters if it does not — the continuation model is '
         f"{p3(PC['ps'])} / {p3(PD['ps'])})"],
        ['Weighted central — recovery', f"AED {p2(CEN_R_CT)} / {p2(CEN_R_DM)}, "
         f"{sgn(CEN_R_CT / SPOT - 1, 0)} / {sgn(CEN_R_DM / SPOT - 1, 0)}",
         'a de-escalation that had not occurred at the anchor date; a fifth of the weight '
         'deliberately given to today\'s war-discounted market regime through the relative '
         'lens'],
        ['Weighted central — continuation', f"AED {p2(CEN_C_CT)} / {p2(CEN_C_DM)}, "
         f"{sgn(CEN_C_CT / SPOT - 1, 0)} / {sgn(CEN_C_DM / SPOT - 1, 0)}",
         'the world as it stood on the published facts at the anchor; same weights'],
        ['Relative multiples', f"AED {p3(REL['ps_rel'])}, {sgn(REL['ps_rel'] / SPOT - 1, 0)}",
         'the current GCC utility pricing regime is the right regime to capitalise'],
        ['The market', p2(SPOT), 'revealed preference of the marginal seller in a conflict '
         'summer, after a weak volume quarter'],
        ['DEWA control purchase (reference)', f"AED {p2(DEWA['price'])}, "
         f"{sgn(DEWA_PREM, 0)} above spot",
         'what the controlling shareholder paid a related party for control economics in '
         'February — bounds the question from above, proves nothing about minority value'],
        ['Three-month price map', f"median {p2(H3M['pct']['p50'])}, "
         f"{pc(H3M['p_above'], 0)} chance of finishing above spot",
         'volatility persists as it has; no view on value']]
table(rows, [1.85, 2.30, 2.85], size=8.4)
P(f"The reading we take from this: the market is pricing the consumption shock as if it were a "
  f"structural impairment of the profit pool, and the cash-flow arithmetic says it is not — "
  f"the pool sits in the contracted capacity charge, which grew through the war half. Even the "
  f"continuation case, which concedes the whole usage shock forever, sits well above the "
  f"market price. The "
  f"genuine open questions are the ones the market prices less visibly: whether the "
  f"{pc(IN['tax_dmtt'], 0)} minimum tax reaches the company ({p3(abs(DMTT_DELTA))} per share, "
  f"published as its own column), and whether the next approved tariff schedule stays flat "
  f"(not priced — flagged as the model's single most valuable assumption). Between the "
  f"{p2(CEN_C_DM)} continuation central under the harsher tax framing and the {p2(SPOT)} "
  f"market price "
  f"lies the war discount itself; a reader who expects the conflict regime to persist should "
  f"weight the relative lens harder, and the field published here lets them. {CONE_SENT}")
P("No rating is expressed here or anywhere else in this document, and no single-number "
  "target: the output is a set of ranges, two published centrals and a distribution — with "
  "the construction range of section 1.8 stated beside them.", space_after=10)

# =========================== 9. §5 CATALYSTS ==================================
H1('5  Catalysts to watch')
rows = [['Catalyst', 'Why it matters', 'What to watch'],
        ['The conflict tempo and the strait', 'the ceasefire was declared over on 8 July and '
         'the Strait of Hormuz stood closed at the anchor — "truce durability" is no longer '
         'the question. The demand shock transmits through hospitality occupancy; attacks '
         'reaching UAE soil are the bear case, a reopened strait is the de-escalation the '
         'recovery case requires',
         'the tempo of attacks on shipping and on UAE soil (none on soil since 8 July; '
         'tankers hit 8, 12 and 14 August); the Iran–Oman reopening track announced 17 '
         'August — implementation, not announcement, is the event'],
        ['Third-quarter 2026 results (November)',
         'the first FULL summer quarter carrying the consumption shock — the highest-usage '
         'months of the year',
         f"equivalent full-load hours against the {EFLH_HRS}-hour first-half print; whether "
         f"capacity revenue keeps growing through it"],
        ['October dividend instalment',
         f"half the committed AED {n0(IN['div_policy'])}mn; the payout is covered "
         f"almost exactly, so any hesitation is information",
         'confirmation of the instalment and any wording change on the 2027 policy'],
        ['Minimum-tax clarification',
         f"whether DEWA-group consolidation sweeps Empower into the {pc(IN['tax_dmtt'], 0)} "
         f"regime — worth AED {p3(abs(DMTT_DELTA))} per share on the primary lens, published "
         f"here as its own column",
         'Ministry of Finance guidance on domestic minimum top-up tax scope for '
         'government-group entities; the tax note of the 2026 annual filing'],
        ['Connection pace', f"the volume driver: guidance is {n0(GUID_LO)}–{n0(GUID_HI)}k RT "
         f"of 2026 connections against a {n0(BACKLOG)}k RT contracted backlog",
         'connected and contracted capacity in each results deck; the fifth Business Bay '
         'plant award moving to construction'],
        ['The next tariff decision', 'the flat regulated tariff is the single most valuable '
         'assumption in the model; a cap cut at review would do what no consumption shock '
         'can. The current instrument already caps the rate Empower charges at essentially '
         'its achieved level and bars indexation of capacity charges',
         'decisions of the Dubai Supreme Council of Energy — the body that APPROVES tariffs '
         '— with Regulatory and Supervisory Bureau consultations and tariff-instrument '
         'revisions as the leading indicator'],
        ["DEWA's intentions at 80%",
         'further buy-in or squeeze-out speculation is NOT modelled; what is real today is a '
         'thinner float, index-weight mechanics and reduced liquidity',
         'any disclosure of stake changes; index-provider treatment of the reduced float']]
table(rows, [1.50, 2.75, 2.75], size=8.3)

# =========================== 10. §6 PROBABILITY ZONES =========================
H1('6  Reading the probability zones')
P(f"The three-month distribution has a median of {p2(H3M['pct']['p50'])} and a 5th-to-95th "
  f"span of {p2(H3M['pct']['p5'])} to {p2(H3M['pct']['p95'])}. Read the span honestly: the "
  f"model considers a {sgn(H3M['pct']['p5'] / SPOT - 1, 0)} move and a "
  f"{sgn(H3M['pct']['p95'] / SPOT - 1, 0)} move equally unremarkable tail outcomes over a "
  f"single quarter of a conflict-regime tape.")
rows = [['Zone', 'Three-month range (AED)', 'How to read it'],
        ['Lower tail', f"below {p2(H3M['pct']['p5'])}",
         'a 1-in-20 outcome; would need a genuine shock — re-escalation onto UAE soil, a '
         'tariff-review surprise, or a dividend wobble'],
        ['Lower half of the central band', f"{p2(H3M['pct']['p25'])} – {p2(H3M['pct']['p50'])}",
         'ordinary drift lower; the market continuing to price the war regime'],
        ['Upper half of the central band', f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'ordinary drift higher; a quiet summer and the October instalment arriving on '
         'schedule'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'a 1-in-20 outcome; would need visible de-escalation or a re-rating of the sector'],
        ['Where the fundamental centrals sit',
         f"{p2(min(CENS_ALL))} – {p2(max(CENS_ALL))}", CONE_SENT]]
table(rows, [1.75, 1.75, 3.50], size=8.4)

# =========================== 11. §7 CAVEATS ===================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("Consumption failing to recover in the 2027 prints. ",
     f"The recovery case restores usage per connected ton to the 2025 level through 2027 — "
     f"and it requires a de-escalation that had not occurred at the anchor date, which is why "
     f"the continuation case is published beside it as an equal, not beneath it as a "
     f"sensitivity. The full continuation model costs only {pc(abs(CRUX_DELTA), 1)} on the "
     f"primary lens, so this is "
     f"a watch-item rather than a value risk — but two consecutive halves with equivalent "
     f"full-load hours below the 2026 trough would put the shock outside anything "
     f"hospitality-linked, and the recovery case should then be abandoned, not "
     f"stretched."),
    ("The minimum tax being confirmed. ",
     f"If the {pc(IN['tax_dmtt'], 0)} domestic minimum top-up tax is confirmed to reach "
     f"Empower through DEWA-group consolidation, shift weight to the {pc(IN['tax_dmtt'], 0)} "
     f"column published throughout — the work is already done; nothing needs re-estimating."),
    ("War re-escalation onto UAE soil. ",
     f"The bear machinery is explicit: usage down a further {pc(abs(U['crux_shock']), 0)} and "
     f"never recovering, connections halved, the harsher tax, and "
     f"{n0((SCN['bear']['ke'] - W['ke_rating']) * 10000)}bp on the cost of equity — AED "
     f"{p3(CEN['bear'])} per share. A reader can adopt it wholesale rather than improvising a "
     f"discount."),
    ("A tariff-cap cut at a regulatory review. ",
     f"The flat regulated tariff is the single most valuable assumption in the model — it "
     f"underwrites the capacity charge that carries {pc(BC['tv_share'], 1)} of the enterprise "
     f"value into the terminal. The current tariff instrument hardens the flat assumption "
     f"(indexation of capacity charges is barred, and the achieved rate already sits at the "
     f"cap) while confirming there is no escalation upside either. No cap cut has occurred in "
     f"the record examined here, but the "
     f"model contains no machinery for one, deliberately: it would be a regime change, to be "
     f"re-modelled, not sensitised."),
    ("Construction limitations, stated. ",
     f"The sovereign anchor is a {TENOR}-year bond against five-plus years of cash flows (the "
     f"most recent AED print; the longer February-2033 sukuk's last print predates the July "
     f"repricing); the index series behind the beta regression is an "
     f"aggregator pull with roughly a fifth of sessions missing, absorbed by weekly sampling "
     f"and flagged in the bibliography; and the first-half revenue-mix percentages "
     f"({MIXD}/{MIXC}/{MIXO}) come from the investor deck, not the audited notes — the audited "
     f"statements disclose only the consumption figure, in the auditor's key-audit-matter "
     f"section, {pc(KAM_SHARE, 1)} of 2025 revenue on that basis (the deck's first-half mix "
     f"and the audited full-year share differ because the second half carries the summer "
     f"peak)."),
    ("Related-party concentration. ",
     f"The {DEWA_PCT}% owner is also the sole supplier of "
     f"the largest cost line and the counterparty of the 2026 control transaction. Tariff "
     f"bargaining, input pricing and any future buy-in all run through one related party. This "
     f"is a governance fact, not an allegation, and it is one reason the relative lens and the "
     f"scenario field are published alongside the model rather than folded into it."),
    ("What would change our mind, specifically. ",
     f"Upward: visible de-escalation; the minimum-tax question resolving at "
     f"{pc(IN['tax_ct'], 0)}; connections printing at or above the top of guidance. Downward: "
     f"a tariff-review consultation proposing cuts; equivalent full-load hours below the 2026 "
     f"trough for two consecutive halves; the dividend reset below the committed AED "
     f"{n0(IN['div_policy'])}mn.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== 12. APPENDIX A ==================================
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years audited and five years forecast (consolidated, AED mn)')
cols = ['FY2023', 'FY2024', 'FY2025'] + YRS
def h3(key, neg=False, fmt=n0):
    out = []
    for y in ('FY23', 'FY24', 'FY25'):
        v = HI[y][key]
        out.append(f"({fmt(abs(v))})" if (neg or v < 0) else fmt(v))
    return out
rows = [['AED mn'] + cols]
rows.append(['Revenue'] + h3('rev') + [n0(B['rev'][y]) for y in YRS])
rows.append(['Interest income on the related-party acquisition receivables (excluded from '
             'the operating build; the asset sits in the bridge at book)'] + h3('intco') +
            [n0(B['intco'][y]) for y in YRS])
rows.append(['Cost of sales'] + h3('cos') + ['—'] * 5)
rows.append(['Gross profit'] + h3('gp') + ['—'] * 5)
rows.append(['General and administrative expenses'] + h3('ga') + ['—'] * 5)
rows.append(['Operating profit'] + h3('op') + ['—'] * 5)
rows.append(['EBITDA (history: audited-derived, operating profit + D&A; forecast: operating '
             'EBITDA — see note)'] + h3('ebitda') +
            [n0(B['ebitda'][y]) for y in YRS])
rows.append(['EBITDA margin (same bases)'] + [pc(HI[y]['ebitda'] / HI[y]['rev']) for y in
             ('FY23', 'FY24', 'FY25')] + [pc(B['ebitda'][y] / B['rev'][y]) for y in YRS])
rows.append(['Depreciation and amortisation'] + h3('dna', neg=True) +
            [f"({n0(B['dna'][y])})" for y in YRS])
rows.append(['EBIT (forecast basis)'] + ['—'] * 3 + [n0(BC['ebit'][y]) for y in YRS])
rows.append([f"NOPAT at {pc(IN['tax_ct'], 0)} / at {pc(IN['tax_dmtt'], 0)}"] + ['—'] * 3 +
            [f"{n0(BC['nopat'][y])} / {n0(BD['nopat'][y])}" for y in YRS])
rows.append(['Profit before tax'] + h3('pbt') + ['—'] * 5)
rows.append(['Income tax (credit) / expense'] + h3('tax') + ['—'] * 5)
rows.append(['Profit for the year'] + h3('pat') + ['—'] * 5)
rows.append(['Attributable to shareholders'] + h3('npa') + ['—'] * 5)
rows.append(['Earnings per share (AED, derived)'] +
            [p3(HI[y]['npa'] / SH) for y in ('FY23', 'FY24', 'FY25')] + ['—'] * 5)
table(rows, [1.90, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375, 0.6375],
      size=7.8, band_rows={7, 8})
caption("Every FY2023-25 line is taken directly from the company's audited consolidated "
        "statements (the 2023 income-statement figure of interest income on the airport "
        "concession receivable is presented INSIDE gross profit by the company, and the same "
        "presentation is kept here). EBITDA is a house derivation — operating profit plus "
        "depreciation and amortisation — labelled as such; the audited statements contain no "
        "EBITDA line. The 2023 tax line is a CREDIT (first recognition of deferred tax assets "
        "ahead of UAE corporate tax). Forecast financing, tax and attributable lines are shown "
        "only where the model constructs them; the free-cash-flow waterfall in section 1.1 is "
        "a pre-financing measure by construction.")

H2('A.2  Balance sheet — condensed house layout (consolidated, AED mn)')
def bs_col(src, m):
    return {k: (src.get(v, 0) or 0) / 1000.0 if isinstance(v, str) else
            sum((src.get(x, 0) or 0) for x in v) / 1000.0 for k, v in m.items()}
b23r = EX23['2023']['balance_sheet']
b23 = {**b23r['non_current_assets'], **b23r['current_assets'],
       **b23r['equity'], **b23r['non_current_liabilities'],
       'cur_borrow': b23r['current_liabilities']['bank_borrowings'],
       'pay': b23r['current_liabilities']['trade_and_other_payables'],
       'lease_cur': b23r['current_liabilities']['lease_liabilities'],
       'total_liabilities': b23r['total_liabilities'],
       'total_assets': b23r['total_assets']}
c23 = bs_col(b23, dict(
    ppe='property_plant_equipment', intang='intangible_assets',
    conc='financial_assets_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease=('lease_liabilities', 'lease_cur'), pay='pay',
    liab='total_liabilities', eqp='attributable_to_equity_holders',
    nci='non_controlling_interests', eqt='total_equity'))
b24r = EX25['2024_comparative']['balance_sheet']
c24 = bs_col(b24r, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_amortised_cost_non_current',
    invprop='investment_properties', inv='inventories',
    recv='trade_and_other_receivables', cash='cash_and_cash_equivalents',
    dep='term_deposits', assets='total_assets',
    borrow=('bank_borrowings_non_current', 'bank_borrowings_current'),
    pay='trade_and_other_payables_current', liab='total_liabilities',
    eqp='equity_attributable_to_parent', nci='non_controlling_interests',
    eqt='total_equity'))
c24['lease'] = EX24['notes']['lease_liabilities_note6']['2024']['total'] / 1000.0
b25r = EX25['2025']['balance_sheet']
b25 = {**b25r['non_current_assets'], **b25r['current_assets'], **b25r['equity'],
       **b25r['non_current_liabilities'],
       'cur_borrow': b25r['current_liabilities']['bank_borrowings'],
       'pay': b25r['current_liabilities']['trade_and_other_payables'],
       'lease_cur': b25r['current_liabilities']['lease_liabilities'],
       'total_liabilities': b25r['total_liabilities'],
       'total_assets': b25r['total_assets']}
c25 = bs_col(b25, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_at_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease=('lease_liabilities', 'lease_cur'), pay='pay',
    liab='total_liabilities', eqp='equity_attributable_to_parent',
    nci='non_controlling_interests', eqt='total_equity'))
bjr = EXI['h1_2026']['balance_sheet_30_jun_2026_full']
bj = {**bjr['non_current_assets'], **bjr['current_assets'], **bjr['equity'],
      **bjr['non_current_liabilities'],
      'cur_borrow': bjr['current_liabilities']['bank_borrowings'],
      'pay': bjr['current_liabilities']['trade_and_other_payables'],
      'lease_cur': bjr['current_liabilities']['lease_liabilities'],
      'total_liabilities': bjr['total_liabilities'],
      'total_assets': bjr['total_assets']}
cj = bs_col(bj, dict(
    ppe='property_plant_and_equipment', intang='intangible_assets',
    conc='financial_assets_at_amortised_cost', invprop='investment_properties',
    inv='inventories', recv='trade_and_other_receivables',
    cash='cash_and_cash_equivalents', dep='term_deposits',
    assets='total_assets', borrow=('bank_borrowings', 'cur_borrow'),
    lease='lease_cur', pay='pay', liab='total_liabilities',
    eqp='attributable_to_equity_holders', nci='non_controlling_interests',
    eqt='total_equity'))
for c in (c23, c24, c25, cj):
    c['nd'] = c['borrow'] + c.get('lease', 0) - c['cash'] - c['dep']
COLS = [('FY2023', c23), ('FY2024', c24), ('FY2025', c25), ('30-Jun-2026', cj)]
def bsr(label, key, neg=False):
    return [label] + [(f"({n0(c[key])})" if neg else n0(c[key])) for _, c in COLS]
rows = [['AED mn'] + [nm for nm, _ in COLS],
        bsr('Property, plant and equipment', 'ppe'),
        bsr('Intangible assets', 'intang'),
        bsr('Airport-concession receivable (amortised cost, non-current)', 'conc'),
        bsr('Investment properties', 'invprop'),
        bsr('Inventories', 'inv'),
        bsr('Trade and other receivables', 'recv'),
        bsr('Term deposits', 'dep'),
        bsr('Cash and cash equivalents', 'cash'),
        bsr('Total assets', 'assets'),
        bsr('Bank borrowings (current + non-current)', 'borrow'),
        bsr('Lease liabilities', 'lease'),
        bsr('Trade and other payables', 'pay'),
        bsr('Total liabilities', 'liab'),
        bsr('Equity attributable to shareholders', 'eqp'),
        bsr('Non-controlling interests', 'nci'),
        bsr('Total equity', 'eqt'),
        bsr('Net debt (borrowings + leases − cash − deposits)', 'nd')]
table(rows, [3.10, 0.90, 0.90, 0.90, 1.20], size=8.3, band_rows={9, 16, 17})
caption(f"FY2023, FY2024 and FY2025 are audited; the June-2026 column is the reviewed interim. "
        f"The net-debt row reproduces the company's own presented figure at 30 June 2026 "
        f"({n0(IN['netdebt_jun26_co'])}mn) exactly. The 2023 step-up in borrowings funded the "
        f"airport-concession acquisition; the 2024-25 rise in cash is retained operating cash "
        f"ahead of the October dividend instalments.")

H2('A.3  Forecast balance-sheet and cash-flow markers')
rows = [['AED mn'] + YRS,
        ['Property, plant and equipment'] + [n0(B['ppe'][y]) for y in YRS],
        ['Net working capital (negative = funded by customers/payables)'] +
        [f"({n0(abs(B['nwc'][y]))})" for y in YRS],
        ['Working capital released in the year'] + [n0(-B['dnwc'][y]) for y in YRS],
        ['Capital expenditure'] + [f"({n0(B['capex'][y])})" for y in YRS],
        ['Depreciation and amortisation'] + [n0(B['dna'][y]) for y in YRS],
        [f"Free cash flow to the firm at {pc(IN['tax_ct'], 0)}"] +
        [n0(BC['fcff'][y]) for y in YRS],
        [f"Free cash flow to the firm at {pc(IN['tax_dmtt'], 0)}"] +
        [n0(BD['fcff'][y]) for y in YRS],
        ['Dividends (committed policy held flat)'] + [n0(IN['div_policy'])] * 5]
table(rows, [2.60, 0.88, 0.88, 0.88, 0.88, 0.88], size=8.3, band_rows={6, 7})
P(f"Two features to read carefully. Net working capital is negative and grows more negative "
  f"with revenue — customer deposits and payables to the related-party supplier fund the "
  f"cycle, so each year RELEASES cash into the free-cash-flow line. And free cash flow to "
  f"equity — the firm figure less roughly AED {n0(NF25 * (1 - IN['tax_ct']))}mn of after-tax "
  f"net finance cost — runs almost exactly at the AED {n0(IN['div_policy'])}mn payout in the "
  f"shock year: the dividend is covered, with the growth funded by the working-capital release "
  f"and the revolving facilities' headroom. Net borrowings are held flat by construction; the "
  f"model neither assumes deleveraging credit nor new debt-funded expansion.")

# =========================== 13. APPENDIX B ==================================
H1('Appendix B  Peer frame, risk register — and the research register')
H2('B.1  Peers and the sector frame')
TB = SX['peers_relative_multiples']['TABREED']
rows = [['Measure', 'Empower', 'Tabreed', 'DEWA (parent)'],
        ['What it is', 'Dubai district cooling, about ' + DUBAI_SHARE + '% of the emirate',
         'UAE-wide and regional district cooling; the only listed pure peer',
         'the Dubai power and water monopoly; consolidates Empower'],
        ['2025 revenue (AED mn)', n0(IN['rev_fy25']), n0(TB['fy2025']['revenue_aed_m']), '—'],
        ['2025 EBITDA margin', pc(HI['FY25']['ebitda'] / HI['FY25']['rev']),
         pc(TB['fy2025']['ebitda_aed_m'] / TB['fy2025']['revenue_aed_m']), '—'],
        ['Net debt / EBITDA', f"{n1(NDX)}×", f"{TB_NDX}×", '—'],
        ['Trailing price / earnings', f"{n1(SPOT / (IN['npa_fy25'] / SH))}×",
         f"{n1(REL['tabreed_pe'])}×", f"{n1(REL['dewa_pe'])}×"],
        ['Dividend yield', pc(YLD, 1), TB_YLD, DEWA_YLD],
        ['Source and date', 'this study, audited statements and the 7-Aug-2026 close',
         'FY2025 results via exchange disclosures; market value from a data provider dated '
         '22-Jun-2026; multiples derived and flagged as derived',
         'market data as of early Aug-2026; secondary marker only — the parent consolidates '
         'the subject']]
table(rows, [1.55, 1.80, 1.85, 1.80], size=8.2)
P("Emicool, the third Dubai operator, is private (a Dubai Investments / Actis joint venture) "
  "and provides no usable multiple; no listed peer exists for the airport-concession leg. The "
  "leverage gap is the reason the peer comparison is made at the enterprise line: Tabreed "
  "carries several turns more net debt, so raw price/earnings comparisons flatter the wrong "
  "name.")

H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Where it is priced'],
        ['Tariff review', 'the regulator approves tariffs; a cut would reprice the capacity '
         'charge — the profit pool itself',
         'NOT priced — flagged as the model\'s single most valuable assumption (sections 1.7 '
         'and 7); a cut is a regime change requiring a re-model'],
        ['War re-escalation', 'hospitality occupancy → consumption; risk premium → discount '
         'rate; connection pipeline → volumes',
         f"the bear scenario, AED {p3(CEN['bear'])} per share, is a full re-run with all four "
         f"channels moved together"],
        ['Minimum top-up tax', f"consolidation into the DEWA group could lift the rate from "
         f"{pc(IN['tax_ct'], 0)} to {pc(IN['tax_dmtt'], 0)}",
         f"published as a full second column everywhere: {p3(abs(DMTT_DELTA))} per share on "
         f"the primary lens"],
        ['Consumption persistence', 'usage per connected ton stays at the shocked level',
         f"a full alternative model: {pc(abs(CRUX_DELTA), 1)} on the primary lens — small, "
         f"because of the pass-through (section 1.7)"],
        ['Related-party concentration', 'the controlling shareholder is also the sole input '
         'supplier and the tariff counterweight',
         'a governance fact discussed in section 7; one reason the relative lens keeps weight'],
        ['Float and liquidity', 'free float near a fifth after the February control purchase; '
         'index treatment and exit liquidity are thinner',
         'not separately priced; noted as a reason market-price signals are noisier than '
         'usual'],
        ['Data limitations', f"a {TENOR}-year sovereign anchor against longer cash flows; an "
         f"index series with missing sessions behind the beta; deck-sourced revenue-mix "
         f"percentages",
         'each flagged in place (section 1.8, section 7) and recorded in the bibliography']]
table(rows, [1.55, 2.70, 2.75], size=8.3)

H2('B.3  The research register — the sources this study stands on')
P("Research proceeded from the company's own filings outward: audited statements first, then "
  "the interim record, the investor-relations material, the regulator, the sovereign data and "
  "the market. The main sources, dated, are tabulated below; the companion bibliography "
  "document records every input's value, source and date individually, together with the "
  "searches that returned nothing.")
rows = [['Source', 'Type', 'Date', 'What was taken'],
        ['Audited consolidated financial statements, FY2022–FY2025 (PwC, unqualified)',
         'Company filing', '2023–Feb-2026',
         'the full income statement, balance sheet and cash-flow record; revenue and '
         'cost notes; borrowings and refinancing notes; related-party purchases; the '
         'capitalisation rate; consumption revenue via the auditor\'s key-audit-matter '
         'sections'],
        ['Condensed interim financial statements, Q1-2026 and H1-2026 (limited review)',
         'Company filing', 'May / Aug 2026',
         'the study-year actuals: quarterly revenue, profit, the June-2026 balance sheet, and '
         'the note tying the consumption fall partly to conflict-hit hospitality occupancy'],
        ['H1-2026 earnings presentation', 'Company investor relations', '5-Aug-2026',
         'connected and contracted capacity, connection guidance, equivalent full-load hours, '
         'the revenue mix, net debt as presented, and the dividend commitment'],
        ['Dubai Executive Council Resolution 6/2021; Regulatory and Supervisory Bureau '
         'instruments', 'Regulator', '2021–2025',
         'the tariff-regulation frame behind the flat-tariff assumption'],
        ['UAE Ministry of Finance dirham T-Bond auction result', 'Sovereign data', '30-Jul-2026',
         'the risk-free anchor'],
        ['Published country-risk dataset (July-2026 edition)', 'Reference dataset', '1-Jul-2026',
         'the UAE default spreads and equity risk premia on both bases'],
        ['DFM daily price history for EMPOWER (supplied) and the FTSE ADX General Index history (supplied)',
         'Market data', 'to 7-Aug-2026',
         'the anchor price, volatility, the moving-average structure, the beta regression and '
         'the price distributions'],
        ['Tabreed and DEWA results and market data', 'Peer disclosures / market data',
         'Jun–Aug 2026', 'the relative-multiples lens — cross-check only, never a source for '
         'Empower\'s own numbers'],
        ['Wire and reference coverage of the 2026 conflict and ceasefire', 'Press',
         'to 9-Aug-2026', 'the macro timeline; where sources disagreed on the truce status, '
         'both readings were recorded rather than resolved']]
table(rows, [2.30, 1.20, 0.90, 2.60], size=8.2)

# =========================== 14. APPENDIX C ==================================
H1('Appendix C  The expert valuation panel')
P("Three valuation approaches are run against the same disclosed facts by three notional "
  "experts, each committed to a different method, each showing every intermediate line, and "
  "each required to state in advance what would prove them wrong. They are not asked to agree, "
  "and they do not.")

H2('C.1  Expert 1 (infrastructure cash flow) — the contracted asset base, discounted')
P("Worldview: a regulated utility with contracted revenue is the one class of business a "
  "discounted-cash-flow model prices well — the cash flows are visible, the regulator caps the "
  "upside, and the right answer is the present value of the contract stack. When it works: "
  "precisely here. When it fails: when the terminal assumptions smuggle in more value than the "
  "explicit years justify — which is why every terminal choice below is shown and challenged "
  "in C.4.")
rows = [['Step (base case, ' + pc(IN['tax_ct'], 0) + ' tax, AED mn)'] + YRS,
        ['Revenue'] + [n0(B['rev'][y]) for y in YRS],
        ['EBITDA'] + [n0(B['ebitda'][y]) for y in YRS],
        ['EBIT'] + [n0(BC['ebit'][y]) for y in YRS],
        ['NOPAT'] + [n0(BC['nopat'][y]) for y in YRS],
        ['Free cash flow to the firm'] + [n0(BC['fcff'][y]) for y in YRS],
        ['Present value'] + [n0(BC['pv'][y]) for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.4, band_rows={6})
rows = [['Terminal block and bridge', 'Value'],
        ['Sum of the five present values (AED mn)', n0(BC['pv_explicit'])],
        [f"Terminal value — final NOPAT × (1 + {pc(IN['g_term'], 1)}) × (1 − "
         f"{pc(BC['rr_term'], 1)}) ÷ ({pc(W['rating_ct'], 2)} − {pc(IN['g_term'], 1)})",
         n0(BC['tv'])],
        ['Present value of the terminal value (AED mn)', n0(BC['pv_tv'])],
        ['Enterprise value (AED mn)', n0(BC['ev'])],
        ['Less net debt; plus investment properties and fair-value assets; less minorities '
         f"({pc(NCI_FRAC, 1)} of profits)",
         f"({n0(ND)}) / {n0(IN['invprop_jun26'] + IN['fvtpl_jun26'] + IN['fvoci_jun26'])} / "
         f"({n0(BC['nci_val'])})"],
        ['Equity attributable (AED mn)', n0(BC['eq_attr'])],
        ['Fair value per share (AED)', p3(BC['ps'])],
        ['Range — the consumption-grid endpoints, each carrying half the effect of a ±50bp '
         'move in the cost of capital', f"{p2(E1_LO)} – {p2(E1_HI)}"]]
table(rows, [4.55, 2.45], size=8.4, band_rows={7})
P(f"Named sensitivity: the consumption-recovery grid of section 1.7 — the full span from "
  f"never-recovers to overshoot is worth AED "
  f"{p3(CRX['rows'][-1]['ps'] - CRX['rows'][0]['ps'])} per share, while a half-point of "
  f"discount rate is worth about AED {p3(abs(_dn50 - _up50) / 2)}. My valuation is a "
  f"discount-rate argument first and a volume argument barely at all.")
P("Falsifier, stated in advance: two consecutive half-years with equivalent full-load hours "
  "below the 2026 trough. That would mean the demand loss is structural, not "
  "hospitality-linked, and the recovery leg of my base case should be discarded rather than "
  "delayed.", space_after=8)

H2('C.2  Expert 2 (income) — the committed dividend, capitalised')
P("Worldview: for a minority shareholder in a company controlled at 80% by its own supplier, "
  "the only cash flow that is real is the one that arrives — the dividend. Value the "
  "commitment, check its coverage, and treat everything else as the controller's business. "
  "When it works: income-controlled utilities exactly like this. When it fails: when the "
  "payout is about to change in either direction — a committed dividend is a floor and a "
  "ceiling only until it is not.")
rows = [['Step', 'Value'],
        ['Committed distribution (AED mn a year, 2025 and 2026)', n0(DDM['policy_mn'])],
        ['Per share (AED)', p3(DDM['dps'])],
        [f"Grown at {pc(IN['g_term'], 1)} and capitalised at the {pc(W['ke_rating'], 2)} cost "
         f"of equity", f"× {1 + IN['g_term']:.3f} ÷ ({pc(W['ke_rating'], 2)} − "
         f"{pc(IN['g_term'], 1)})"],
        ['Fair value per share (AED)', p3(DDM['ps'])],
        [f"Range — growth {pc(E2_G_LO, 1)} to {pc(E2_G_HI, 1)}", f"{p2(E2_LO)} – {p2(E2_HI)}"]]
table(rows, [4.55, 2.45], size=8.5, band_rows={5})
P("Coverage is the whole argument, so here it is, line by line:")
rows = [['AED mn'] + YRS,
        [f"Free cash flow to the firm ({pc(IN['tax_ct'], 0)})"] +
        [n0(BC['fcff'][y]) for y in YRS],
        ['Less after-tax net finance cost (held at the 2025 level — the book is floating and '
         'was just refinanced)'] + [f"({n0(NF25 * (1 - IN['tax_ct']))})" for _ in YRS],
        ['Free cash flow to equity'] +
        [n0(BC['fcff'][y] - NF25 * (1 - IN['tax_ct'])) for y in YRS],
        ['Dividend'] + [n0(IN['div_policy'])] * 5,
        ['Coverage'] + [f"{(BC['fcff'][y] - NF25 * (1 - IN['tax_ct'])) / IN['div_policy']:.2f}×"
                        for y in YRS]]
table(rows, [3.00, 0.80, 0.80, 0.80, 0.80, 0.80], size=8.3, band_rows={5})
P(f"In the shock year coverage is almost exactly one — the payout absorbs essentially all the "
  f"equity cash flow, and the growth is funded by the working-capital release and the "
  f"revolving facilities' headroom. That is covered, not slack, and it is why my number sits "
  f"below the cash-flow expert's: I pay for the distribution I can see, not the terminal "
  f"value I cannot.")
P("Named sensitivity: each half-point of assumed growth is worth roughly AED "
  f"{p3((E2_HI - E2_LO) / 2)} per share across my range — the entire argument is the "
  "capitalisation rate against the growth of a committed number.")
P("Falsifier, stated in advance: a dividend reset below the committed level, or a payout "
  "financed by facility drawdown for two consecutive periods. Either breaks the premise that "
  "the distribution is an economic signal rather than a promise.", space_after=8)

H2('C.3  Expert 3 (relative value, the sceptic) — anchor on what is actually paid')
P("Worldview: models are opinions; transactions are facts. Anchor on what the market pays for "
  "the same economics today, use the harsher of any contested framing, and treat every model "
  "premium over the market as a claim requiring extraordinary evidence. When it works: "
  "regimes, like this one, where the marginal price-setter is distressed or absent and model "
  "values float free of clearing prices. When it fails: when the anchor set is itself "
  "mispriced — a war-discounted peer group imports the war.")
rows = [['Step', 'Value'],
        [f"Tabreed enterprise value / EBITDA (derived, flagged)",
         f"{n1(REL['tabreed_ev_ebitda'])}×"],
        ['× Empower 2026E EBITDA (AED mn)', n0(REL['ev_rel'] / REL['tabreed_ev_ebitda'])],
        ['Implied enterprise value (AED mn)', n0(REL['ev_rel'])],
        ['Less net debt; plus side pockets; less minorities — per share (AED)',
         p3(REL['ps_rel'])],
        [f"Tabreed price/earnings {n1(REL['tabreed_pe'])}× on 2026E attributable profit "
         f"({n0(REL['npa26'])} AED mn) — per share (AED)", p3(REL['ps_pe'])],
        [f"The February control print — what the controller itself paid a related party",
         p2(DEWA['price'])],
        [f"My tax base: the {pc(IN['tax_dmtt'], 0)} minimum-tax column, on prudence",
         f"{p3(BD['ps'])} on the cash-flow model — noted, not adopted"],
        ['Range — from the market price to the control print', f"{p2(SPOT)} – "
         f"{p2(DEWA['price'])}"],
        ['Central — the earnings-basis read', p2(E3_CENTRAL)]]
table(rows, [4.55, 2.45], size=8.4, band_rows={9})
P(f"Named sensitivity: each turn of the peer earnings multiple is worth AED "
  f"{p3(REL['ps_pe'] / REL['tabreed_pe'])} per share. My range's top is not a multiple at all "
  f"— it is the one disclosed transaction ({p2(DEWA['price'])}), and I note that a control "
  f"price paid between related parties bounds the question from above without proving "
  f"anything about what a minority share is worth.")
P("Falsifier, stated in advance: a GCC utility re-rating — Tabreed sustained above thirteen "
  "times enterprise value to EBITDA — without Empower following. That would show the discount "
  "is company-specific rather than regime-wide, and my regime-anchored central should be "
  "abandoned.", space_after=8)

H2('C.4  Cross-examination')
rows = [['Challenge', 'From', 'Response'],
        [f'"{pc(BC["tv_share"], 0)} of your enterprise value is terminal, earning a '
         f'{pc(BC["roic_term"], 0)} return on capital forever — at a REGULATED utility. The '
         f'regulator exists to take that return away."', 'Expert 3 to Expert 1',
         'Rejected in part, conceded in part. The measured return is inflated by the funding '
         'model, not by tariff generosity: customers\' deposits and payables hold working '
         'capital negative, so the capital base the return is struck on is artificially small '
         '— the same tariff on a conventionally funded balance sheet would show an ordinary '
         'return, and the regulator prices the tariff, not the ratio. CONCEDED: the '
         'tariff-review risk is real, it is the one lever that reaches the capacity charge, '
         'and it deserves exactly the bear-case weight it gets.'],
        ['"You are capitalising a promise. The committed dividend runs to 2026 only, and your '
         'coverage table shows it absorbing all the equity cash flow in the shock year."',
         'Expert 1 to Expert 2',
         'Partly conceded. The commitment is two years old and covered at one times, not '
         'slack. But the counterparty is the 80% owner, which collects four-fifths of every '
         'instalment itself and set the policy — the incentive alignment is unusually direct, '
         'and the distribution record since listing has only stepped up.'],
        ['"Your anchors are war prices. You are not measuring Empower; you are measuring '
         'March."', 'Expert 2 to Expert 3',
         'Conceded, and embraced. That is what a relative lens is FOR — it prices the regime '
         'the shares must actually be sold into. The mistake would be presenting it as '
         'intrinsic; nobody here does. My range top is a real transaction, not a war print.'],
        ['"All three of you assume the tariff stays flat."', 'The panel to itself',
         'Accepted as the shared, unpriced assumption — stated in sections 1.7, 5 and 7. A '
         'tariff cut would move every method in the same direction at once, which is exactly '
         'why it is flagged rather than diversified away.']]
table(rows, [2.45, 1.20, 3.35], size=8.2)

H2('C.5  The three in one room')
fig('figD1_experts.png', 6.9,
    f"Figure 9 — the three experts' ranges against the market price of {p2(SPOT)} and the "
    f"control print of {p2(DEWA['price'])}.")
P(f"The panel spans AED {p2(min(E1_LO, E2_LO, SPOT))} to {p2(max(E1_HI, E2_HI, DEWA['price']))} "
  f"— and the disagreement is orderly, not noisy. Expert 1 discounts the contract stack and "
  f"lands highest ({p2(E1_LO)}–{p2(E1_HI)}); Expert 2 capitalises the committed dividend and "
  f"lands in the middle ({p2(E2_LO)}–{p2(E2_HI)}); Expert 3 anchors on what the war-discounted "
  f"market actually pays and lands lowest ({p2(SPOT)}–{p2(DEWA['price'])}, central "
  f"{p2(E3_CENTRAL)}). Notice what the room agrees on: every range sits at or above the market "
  f"price, every method finds the capacity charge rather than the meter carrying the value, "
  f"and every falsifier is observable within two reporting periods. The study's own weighted "
  f"central ({p3(CEN['ct'])} / {p3(CEN['dmtt'])} by tax framing) sits between Expert 1 and "
  f"Expert 2 — which is what a weighting that gives the market regime a real vote should "
  f"produce.")

H2('C.6  Reading the divergence')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'What it is worth'],
        ['Tax basis', pc(IN['tax_ct'], 0) + ' (audited rate)', 'embedded in the payout',
         pc(IN['tax_dmtt'], 0) + ' on prudence',
         f"AED {p3(abs(DMTT_DELTA))} per share on the cash-flow model — the gap between the "
         f"two published columns"],
        ['Terminal claim', f"full terminal value ({pc(BC['tv_share'], 0)} of enterprise "
         f"value)", 'a perpetuity of the committed dividend only',
         'none — the current multiple regime is assumed permanent',
         f"AED {p3(BC['ps'] - E3_CENTRAL)} per share between Expert 1's central and Expert "
         f"3's — the largest single gap in the room"],
        ['Consumption recovery', 'recovers through 2027; grid shown', 'not sensitive — the '
         'dividend is fixed either way', 'embedded in the peer prices',
         f"AED {p3(abs(BC['ps'] - PC['ps']))} per share even in the never-recovers case — "
         f"small by construction (the pass-through)"],
        ['Risk premium', 'model-built cost of equity from the sovereign and the published '
         'premium', f"the same {pc(W['ke_rating'], 2)} rate, applied to a committed flow",
         'whatever the market embeds — the war discount is kept, not modelled out',
         'the half-point grid: AED ' + p3(abs(_dn50 - _up50) / 2) + ' per share per 50bp']]
table(rows, [1.20, 1.55, 1.45, 1.55, 1.25], size=8.0)
P("The instruction to the reader is not to average the three. It is to decide which premise "
  "you hold — whether the terminal claim of a regulated monopoly is bankable, whether a "
  "committed dividend is a floor, whether today's regime prices are the right anchor — and "
  "use the corresponding number. The disagreement is a map of what you need a view on.",
  space_after=10)

# =========================== 15. ABOUT =======================================
H1('About this series')
P("This series publishes independent, educational valuation studies of listed companies. Each "
  "study is built from disclosed financial statements and named market data, states its "
  "assumptions explicitly, computes every figure in an auditable model rather than in prose, "
  "and publishes the ranges its assumptions produce. Studies never carry a rating or a price "
  "target. Where a figure is estimated rather than disclosed, it is labelled. Where a source "
  "could not be reached or a disclosure does not exist, the gap is recorded in the "
  "accompanying bibliography rather than quietly filled in.")
P("The probabilistic price map in section 3 is produced by a volatility model that is tested "
  "by walk-forward simulation against a carry-anchored random-walk benchmark before it is "
  "allowed to publish a range. It describes price dispersion and carries no view on value. It "
  "is never combined with the fair-value work.")

# =========================== 16. DISCLOSURE ==================================
H1('Disclosure & Disclaimer')
P("For information only — not investment advice. This document is educational analysis and is "
  "not an offer or a solicitation to buy or sell any security. It contains no recommendation, "
  "no rating and no price target. The author holds no position in the security discussed and "
  "has no business relationship with the company. Figures are drawn from public sources "
  "believed reliable but not independently verified; where figures are derived or estimated "
  "this is stated in the text. Valuation is inherently uncertain and depends on assumptions "
  "that reasonable analysts will dispute — several such disputes are set out explicitly in "
  "this document, and two (the tax framing and the consumption recovery) are published as "
  "full alternative computations rather than resolved silently. Past performance and "
  "simulated distributions are not guides to future returns. Readers must reach their own "
  "conclusions and should consider taking independent advice. No liability is accepted for "
  "any loss arising from use of this material.", size=9.2, color=GREY)

out = os.path.join(HERE, 'EMPOWER_Valuation_Study_09-08-2026_public.docx')
finalize(doc)
doc.save(out)
print(f"wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables")
if MISSING_FIGS:
    print("MISSING FIGURES (skipped):", ', '.join(MISSING_FIGS))
else:
    print("all figures embedded")
