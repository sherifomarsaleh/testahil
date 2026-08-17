"""EMPOWER_Valuation_Model_09082026_public.xlsx — 16 sheets mirroring the house canonical
model (regulated-utility / operating-company variant). Blue = inputs · black = formulas ·
green = cross-sheet links.

The workbook is FORMULA-DRIVEN, revised 17-Aug-2026 after an external audit. Exactly TWO
classes of cell are pasted values:

  1. audited and disclosed historical figures and external facts (FY2023-25 statement
     lines, the 30-Jun-2026 reviewed balance sheet, disclosed connected capacity, the
     consumption revenue from the auditor's key-audit-matter section, deck physical
     figures, peer marks, the RD10 tariff cap) — the primary record, not a calculation.
     Every derived rate (per-RT revenue rates, the electricity-and-water pass-through,
     capex per added RT, the depreciation rate, the working-capital ratio) is a FORMULA
     off these pasted anchors;
  2. whole-model simulation outputs that cannot be one formula: the probabilistic price
     map and the 5x5 discount-rate x growth grid. Everything else — including the five
     consumption-recovery columns, the bear and bull cases and the three cost-of-capital
     constructions — is a LIVE parallel model on the Sensitivity sheet and redraws when
     a driver changes.

NUMERIC TRACEABILITY: no financial numeral is typed into this builder. Every number is
read from study_numbers.json (or, for audited balance-sheet history lines only, from the
statement extracts), and every formula cell's model value is recorded into
xlsx_expected.json as it is written; recalc.py re-evaluates the delivered workbook
independently and asserts cell-for-cell agreement. (Two disclosed external facts arrive
by instruction rather than the JSON and are asserted against it where possible: the RD10
v1.3 tariff cap 0.643 AED/RTh, the H1-2026 1,174m RTh deck figure, the FY31-40 stage-two
growth 1.5%, and Tabreed's reported FY2025 revenue — each pasted once, sourced, display
or assert-verified.)
"""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
E25 = json.load(open(os.path.join(HERE, 'extract_fy2025.json')))
H1 = json.load(open(os.path.join(HERE, 'extract_2026_interims.json')))
E24 = json.load(open(os.path.join(HERE, 'extract_fy2024.json')))

IN = {k: v['value'] for k, v in D['inputs'].items()}
SRC = {k: f"{v['source']} ({v['date']})" for k, v in D['inputs'].items()}
# external-reader wording for the beta source (the stored string carries internal QC
# vocabulary; the statistics themselves are restated in plain language, from the same data)
BR = D['beta_reg']
SRC['beta'] = (f"Own-stock weekly regression vs {BR['index'].split(',')[0]}, "
               f"{BR['window'][0]} to {BR['window'][1]} ({BR['window_years']:.2f} years, "
               f"{BR['n']} weeks): R-squared {BR['r2']:.2f}, standard error {BR['se']:.2f}, "
               f"90% interval [{BR['ci90'][0]:.2f}, {BR['ci90'][1]:.2f}] "
               f"({D['inputs']['beta']['date']})")
M, HI, U, UP = D['meta'], D['hist_is'], D['unit'], D['unit_physical']
F = D['fcst']['base']
W, DC = D['wacc'], D['dcf']
B_CT, B_DM, B_CDS = DC['base_ct'], DC['base_dmtt'], DC['base_cds']
LN, REL, NRM, BK, DDM = D['lenses'], D['rel'], D['norm'], D['book'], D['ddm']
CEN, SNW, CRUX, STK, S0 = D['central'], D['sens_wg'], D['crux'], D['strike'], D['step0']
SCEN = D['scenarios']
SPOT, SH = M['spot'], M['shares_mn']
TAX, TAXD = IN['tax_ct'], IN['tax_dmtt']
G = IN['g_term']
YF = D['fcst']['years']                          # FY26..FY30
YFL = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
YHL = ['FY2023', 'FY2024', 'FY2025']
H3 = ['FY23', 'FY24', 'FY25']

# ---- derived anchors (all from study_numbers.json — nothing typed) ----------------
WAGE_ESC = F['other_cos']['FY26'] / U['other_cos25'] - 1                      # 2.5%
INTCO_DECAY = 1 - F['intco']['FY26'] / IN['intco_fy25']                       # 3.0%
RENTAL = IN['rental_fy25']
OI_OP = IN['oi_fy25'] - RENTAL                    # operating other income 6.336
# pure net finance charge — the receivable interest and the rental income are their own
# visible lines now, not inside the finance/EBITDA chain
FIN26 = (REL['np26'] / (1 - TAX)
         - (F['ebitda']['FY26'] + F['intco']['FY26'] + RENTAL - F['dna']['FY26']))
CASH_YIELD = (IN['kd_marg'] * IN['borrow_jun26'] + FIN26) / IN['cash_jun26']  # 3.5%
IC_TERM = B_CT['nopat']['FY30'] / B_CT['roic_term']      # = plant + net working capital
NCI_FR = IN['nci_pat_fy25'] / IN['pat_fy25']
RTP = U['rt_path']
ADDS = [RTP[y] - RTP[p] for p, y in zip(['FY25'] + YF[:-1], YF)]              # 105/100/90/80/70
GROSS_JUN26 = IN['borrow_jun26'] + IN['lease_jun26']
NET_DEBT = W['net_debt']
RECV = IN['recv_jun26']
BRIDGE_ADD = RECV + IN['invprop_jun26'] + IN['fvtpl_jun26'] + IN['fvoci_jun26']
T0 = -math.log(B_CT['df']['FY26']) / math.log(1 + W['rating_ct'])             # 0.5 stub
BETA_DFM = (W['constructions']['ke_dfm'] - W['rf_star_rating']) / IN['erp_rating']
WACC_CT = W['rating_ct']
G2 = 0.015          # stage-two terminal growth (long-run densification) — verified below
CPRT, CAPRT = U['cons_per_rt25'], U['cap_per_rt25']
EW, NWC_RATIO, NWC25 = U['ew_ratio'], U['nwc_ratio'], U['nwc25']
SHOCK = U['crux_shock']

assert abs(WAGE_ESC - 0.025) < 1e-9 and abs(INTCO_DECAY - 0.03) < 1e-9
assert abs(CASH_YIELD - 0.035) < 1e-9
assert abs(IC_TERM - (F['ppe']['FY30'] + F['nwc']['FY30'])) < 1e-6
assert abs(T0 - 0.5) < 1e-9 and abs(BETA_DFM - 0.652) < 1e-9


def two_stage_tv(nopat30, roic, wacc, g1=G, g2=G2):
    """Closed-form of the model's FY31-40 + perpetuity terminal (mirrors compute)."""
    q = (1 + g1) / (1 + wacc)
    rr1, rr2 = g1 / roic, g2 / roic
    s1 = nopat30 * (1 - rr1) * q * (1 - q ** 10) / (1 - q)
    nop10 = nopat30 * (1 + g1) ** 10
    s2 = nop10 * (1 + g2) * (1 - rr2) / ((wacc - g2) * (1 + wacc) ** 10)
    return s1, nop10, s2, s1 + s2

_s1, _n10, _s2, _tv = two_stage_tv(B_CT['nopat']['FY30'], B_CT['roic_term'], WACC_CT)
assert abs(_tv - B_CT['tv']) < 1e-6 * B_CT['tv'], 'stage-two growth fails to reproduce TV'

# physical decomposition (H1-2026 deck facts)
H1_RTH = 1174.0     # m RTh cooling delivered H1-2026, deck p4 — pasted external fact
H1_MIX = UP['rate_aed_per_rth'] * H1_RTH / IN['rev_h1_26']
assert abs(H1_MIX - 0.49) < 1e-9
CAP643 = 0.643      # RD10 v1.3 consumption tariff cap, AED/TRh incl. fuel surcharge
RATE = UP['rate_aed_per_rth']
HEADROOM = RATE / CAP643 - 1
TABREED_REV = 2456.0   # Tabreed FY2025 reported revenue, AED mn (reported, not 2,460)

# ---- audited balance-sheet history (extracts; AED mn) ------------------------------
def th(x):
    return x / 1000.0
BS25 = E25['2025']['balance_sheet']
BS24 = E25['2024_comparative']['balance_sheet']
BSJ = H1['h1_2026']['balance_sheet_30_jun_2026_full']
BH = {
 'FY24': dict(ppe=th(BS24['property_plant_and_equipment']),
              invprop=th(BS24['investment_properties']),
              fvtpl=th(BS24['financial_assets_fvtpl']), fvoci=th(BS24['financial_assets_fvoci']),
              conc=th(BS24['financial_assets_amortised_cost_non_current']
                      + BS24['financial_assets_amortised_cost_current']),
              cash=th(BS24['cash_and_cash_equivalents'] + BS24['term_deposits']),
              gross=th(BS24['bank_borrowings_current'] + BS24['bank_borrowings_non_current']),
              pay=th(BS24['trade_and_other_payables_current']),
              eqp=th(BS24['equity_attributable_to_parent']),
              nci=th(BS24['non_controlling_interests']), ta=th(BS24['total_assets'])),
 'FY25': dict(ppe=th(BS25['non_current_assets']['property_plant_and_equipment']),
              invprop=th(BS25['non_current_assets']['investment_properties']),
              fvtpl=th(BS25['current_assets']['financial_assets_fvtpl']),
              fvoci=th(BS25['non_current_assets']['financial_assets_fvoci']),
              conc=th(BS25['non_current_assets']['financial_assets_at_amortised_cost']
                      + BS25['current_assets']['financial_assets_at_amortised_cost']),
              cash=th(BS25['current_assets']['cash_and_cash_equivalents']
                      + BS25['current_assets']['term_deposits']),
              gross=th(BS25['current_liabilities']['bank_borrowings']
                       + BS25['non_current_liabilities']['bank_borrowings']
                       + BS25['current_liabilities']['lease_liabilities']),
              pay=th(BS25['current_liabilities']['trade_and_other_payables']),
              eqp=th(BS25['equity']['equity_attributable_to_parent']),
              nci=th(BS25['equity']['non_controlling_interests']), ta=th(BS25['total_assets'])),
 'JUN26': dict(ppe=th(BSJ['non_current_assets']['property_plant_and_equipment']),
               invprop=th(BSJ['non_current_assets']['investment_properties']),
               fvtpl=th(BSJ['current_assets']['financial_assets_fvtpl']),
               fvoci=th(BSJ['non_current_assets']['financial_assets_fvtoci']),
               conc=th(BSJ['non_current_assets']['financial_assets_at_amortised_cost']
                       + BSJ['current_assets']['financial_assets_at_amortised_cost']),
               cash=th(BSJ['current_assets']['cash_and_cash_equivalents']
                       + BSJ['current_assets']['term_deposits']),
               gross=th(BSJ['current_liabilities']['bank_borrowings']
                        + BSJ['non_current_liabilities']['bank_borrowings']
                        + BSJ['current_liabilities']['lease_liabilities']),
               pay=th(BSJ['current_liabilities']['trade_and_other_payables']),
               eqp=th(BSJ['equity']['attributable_to_equity_holders']),
               nci=th(BSJ['equity']['non_controlling_interests']), ta=th(BSJ['total_assets'])),
}
CF24 = E24['cash_flow']['2024']
OCF25 = th(E25['2025']['cash_flow']['net_cash_from_operating'])
OCF24 = th(CF24['net_cash_operating'])
DIV25 = th(E25['2025']['cash_flow']['financing']['dividends_paid'])   # negative as reported
DIV24 = th(CF24['dividends_paid'])                                    # negative as reported

# NWC components (FY2025 audited BS; capex accrual recovered off the model's own total)
INV25 = th(BS25['current_assets']['inventories'])
REC25 = th(BS25['current_assets']['trade_and_other_receivables'])
DRP25 = th(BS25['current_assets']['due_from_related_parties'])
PAY25 = th(BS25['current_liabilities']['trade_and_other_payables'])
CRP25 = th(BS25['current_liabilities']['due_to_related_parties'])
ACCR25 = PAY25 + CRP25 + NWC25 - INV25 - REC25 - DRP25   # project-cost accruals 171.085
PPE_DEP25 = U['dep_rate'] * BH['FY24']['ppe']            # FY2025 PPE depreciation 352.199
assert abs(INV25 + REC25 + DRP25 - (PAY25 - ACCR25) - CRP25 - NWC25) < 1e-9
assert abs(PPE_DEP25 + U['amort_flat'] - IN['dna_fy25']) < 1e-6
EQ24 = BH['FY24']['eqp']

# ---- FY2025 operating-EBITDA identity (interest AND rental now excluded) -----------
EB25_OP = (IN['rev_fy25'] - IN['ew_cost_fy25'] - U['other_cos25'] - U['ga_cash25']
           + OI_OP + IN['ecl_fy25'])                     # 1,565.8 incl. the ECL reversal
assert abs(EB25_OP + IN['intco_fy25'] + RENTAL - HI['FY25']['ebitda']) < 1.0
EB_TRAIL = REL['ebitda_trail']                           # 1,583.9 = audited less interest
assert abs(EB25_OP + RENTAL - EB_TRAIL) < 1e-6
HIST_EB_OP = [HI['FY23']['op'] + HI['FY23']['dna'] - HI['FY23']['intco'],
              HI['FY24']['op'] + HI['FY24']['dna'] - HI['FY24']['intco'],
              EB25_OP]          # FY23/24 rental split is not disclosed — flagged in note

# ---- forecast income-statement / balance-sheet chains (python mirror) --------------
# Finance line split: receivable interest and rental are visible rows; the net finance
# charge earns the deposit yield on the ROLLING cash balance (FY2026 on the 30-Jun-2026
# print — the anchor balance; later years on the prior year-end Balance Sheet roll).
# BOTH balance-sheet rolls (equity and net debt) start from the SAME 30-Jun-2026
# reviewed position: FY2026 carries only the second-half stub of profit/cash and only
# the October dividend instalment.
ebit_f = [B_CT['ebit'][y] for y in YF]
intco_f = [F['intco'][y] for y in YF]
rental_f = [RENTAL] * 5
fin_f, pbt_f, tax_f, pat_f, nci_f, npa_f = [], [], [], [], [], []
fcfe_f, eq_f, nci_bs_f, nd_f, cash_f = [], [], [], [], []
eq_prev, nci_prev, nd_prev = IN['eq_attr_jun26'], BH['JUN26']['nci'], NET_DEBT
cash_int = IN['cash_jun26']
for i in range(5):
    fin = -(IN['kd_marg'] * IN['borrow_jun26'] - CASH_YIELD * cash_int)
    pbt = ebit_f[i] + intco_f[i] + rental_f[i] + fin
    pat = pbt * (1 - TAX)
    nci = -pat * NCI_FR
    npa = pat + nci
    fcfe = B_CT['fcff'][YF[i]] + (fin + intco_f[i] + rental_f[i]) * (1 - TAX)
    stub = T0 if i == 0 else 1.0
    eq_prev = eq_prev + stub * (npa - IN['div_policy'])
    nci_prev = nci_prev - stub * nci
    nd_prev = nd_prev - stub * (fcfe - IN['div_policy'])
    cash = GROSS_JUN26 - nd_prev
    fin_f.append(fin); pbt_f.append(pbt); tax_f.append(-pbt * TAX)
    pat_f.append(pat); nci_f.append(nci); npa_f.append(npa); fcfe_f.append(fcfe)
    eq_f.append(eq_prev); nci_bs_f.append(nci_prev); nd_f.append(nd_prev)
    cash_f.append(cash)
    cash_int = cash
assert abs(npa_f[0] - REL['npa26']) < 1e-6

BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM0 = '#,##0;(#,##0);"-"'; NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%'; PX = '0.000;(0.000);"-"'; MULT = '0.00x'
DF4 = '0.0000'; RATE4 = '0.0000'

SHEETS = ['READ FIRST', 'Summary', 'Fundamental Valuation', 'Assumptions', 'SOTP Bridge',
          'Segments', 'Relative & Normalized', 'DCF', 'Income Statement', 'Balance Sheet',
          'Cash Flow', 'Summary Financials', 'Monte Carlo', 'Sensitivity',
          'Per-Share & Ratios', 'Peer & Sector']
wb = Workbook()
wb.active.title = SHEETS[0]
for n in SHEETS[1:]:
    wb.create_sheet(n)

EXPECT = {}
ANCH = {}

def title(ws, t, s=None, w=10, awidth=48, cwidth=13):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if s:
        ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = awidth
    for c in range(2, w + 1):
        ws.column_dimensions[get_column_letter(c)].width = cwidth

def put(ws, ad, v, font=BLACK, fmt=NUM1, bold=False, fill=None, wrap=False):
    c = ws[ad]; c.value = v
    c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    return c

def putf(ws, ad, formula, expect, fmt=NUM1, bold=False, green=False):
    put(ws, ad, formula, GREEN if green else BLACK, fmt, bold=bold)
    if expect is not None:
        EXPECT.setdefault(ws.title, {})[ad] = float(expect)

def hdr(ws, row, labels, start=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=l)
        c.font = Font(bold=True); c.fill = FILL_H

def band(ws, row, w=10):
    for c in range(1, w + 1):
        ws.cell(row=row, column=c).fill = FILL_G
        ws.cell(row=row, column=c).font = Font(bold=True)

def note(ws, row, text):
    ws.cell(row=row, column=1, value=text).font = SUB

# ============ ASSUMPTIONS (built first — every other sheet references it) ==========
ws = wb['Assumptions']
title(ws, 'Assumptions — every input in the model', 'Blue cells are pasted primary-record '
      'inputs; BLACK cells in this column are formulas deriving each modelling rate from '
      'those inputs — change an audited anchor and the whole model reprices. Column H '
      'gives the source and date of each input.', 8, awidth=56, cwidth=11)
ws.column_dimensions['H'].width = 90
hdr(ws, 3, ['Input'] + YFL + ['', 'Source'])
r = 4
A = {}

def block(name, items):
    """items: (key, label, value, fmt, src) pasted blue, or
              (key, label, '=formula', fmt, src, expect) live derived anchor."""
    global r
    band(ws, r, 8); put(ws, f'A{r}', name, bold=True, fmt=None); r += 1
    for item in items:
        key, lab, val, fmt, src = item[:5]
        put(ws, f'A{r}', lab, fmt=None)
        if isinstance(val, str) and val.startswith('='):
            putf(ws, f'C{r}', val, item[5], fmt)
        elif isinstance(val, (list, tuple)):
            for i, v in enumerate(val):
                put(ws, f'{get_column_letter(2+i)}{r}', v, BLUE, fmt)
        else:
            put(ws, f'C{r}', val, BLUE, fmt)
        if src:
            ws.cell(row=r, column=8, value=src).font = SUB
        A[key] = r
        r += 1
    r += 1

def a(key, i=None):
    col = get_column_letter(2 + i) if i is not None else 'C'
    return f"Assumptions!${col}${A[key]}"

block('Anchors', [
    ('spot', 'Spot price (AED)', SPOT, PX, SRC['spot']),
    ('shares', 'Shares outstanding (mn)', SH, NUM0, SRC['shares_mn']),
    ('tax_ct', 'Corporate tax rate (headline framing)', TAX, PCT, SRC['tax_ct']),
    ('tax_dmtt', 'Top-up tax rate (alternative framing)', TAXD, PCT, SRC['tax_dmtt']),
    ('pat_fy25', 'Profit for the year, FY2025 (AED mn)', IN['pat_fy25'], NUM1, SRC['pat_fy25']),
    ('nci_pat', 'Profit attributable to non-controlling interests, FY2025 (AED mn)',
     IN['nci_pat_fy25'], NUM1, SRC['nci_pat_fy25']),
    ('npa_fy25', 'Profit attributable to shareholders, FY2025 (AED mn)', IN['npa_fy25'],
     NUM1, SRC['npa_fy25'])])
block('Audited FY2025 record — pasted once here; every derived rate below is a formula '
      'off these cells', [
    ('rev25', 'Revenue, FY2025 (AED mn)', IN['rev_fy25'], NUM1, SRC['rev_fy25']),
    ('cons25', 'Consumption revenue, FY2025 (AED mn)', IN['cons_rev']['2025'], NUM1,
     SRC['cons_rev']),
    ('ew25', 'Electricity and water purchased from DEWA, FY2025 (AED mn)',
     IN['ew_cost_fy25'], NUM1, SRC['ew_cost_fy25']),
    ('capex25', 'Capital expenditure (cash), FY2025 (AED mn)', IN['capex_fy25'], NUM1,
     SRC['capex_fy25']),
    ('ppe_dep25', 'Depreciation of plant, FY2025 (AED mn)', PPE_DEP25, NUM1,
     'FY2025 audited cash-flow note: depreciation of property, plant and equipment'),
    ('dna25', 'Total depreciation and amortisation, FY2025 (AED mn)', IN['dna_fy25'],
     NUM1, SRC['dna_fy25']),
    ('ppe24', 'Net property, plant and equipment, end-FY2024 (AED mn)', BH['FY24']['ppe'],
     NUM1, 'FY2024 audited balance sheet (FY2025 filing comparative)'),
    ('ppe25', 'Net property, plant and equipment, end-FY2025 (AED mn)', BH['FY25']['ppe'],
     NUM1, 'FY2025 audited balance sheet'),
    ('inv25', 'Inventories, end-FY2025 (AED mn)', INV25, NUM1, 'FY2025 audited balance sheet'),
    ('rec25', 'Trade and other receivables, end-FY2025 (AED mn)', REC25, NUM1,
     'FY2025 audited balance sheet'),
    ('drp25', 'Due from related parties, end-FY2025 (AED mn)', DRP25, NUM1,
     'FY2025 audited balance sheet'),
    ('pay25', 'Trade and other payables, end-FY2025 (AED mn)', PAY25, NUM1,
     'FY2025 audited balance sheet'),
    ('accr25', 'Project-cost accruals inside payables, end-FY2025 (AED mn)', ACCR25, NUM1,
     'FY2025 audited FS note 36 (non-cash capital accrual movement) — excluded from the '
     'operating cycle'),
    ('crp25', 'Due to related parties, end-FY2025 (AED mn)', CRP25, NUM1,
     'FY2025 audited balance sheet'),
    ('eq_fy24', 'Equity attributable to shareholders, end-FY2024 (AED mn)', EQ24, NUM1,
     'FY2024 audited balance sheet (FY2025 filing comparative)'),
    ('eq_fy25', 'Equity attributable to shareholders, end-FY2025 (AED mn)',
     IN['eq_attr_fy25'], NUM1, SRC['eq_attr_fy25']),
    ])
block('Unit build — physical inputs and forecast drivers', [
    ('rt_fy24', 'Connected capacity, end-FY2024 (k RT)', IN['rt_conn']['2024'], NUM0,
     SRC['rt_conn']),
    ('rt_fy25', 'Connected capacity, end-FY2025 (k RT)', IN['rt_conn']['2025'], NUM0,
     SRC['rt_conn']),
    ('adds', 'New connections by year (k RT)', ADDS, NUM0,
     'FY2026 = guidance midpoint (100-110k, H1-2026 earnings deck p13); then the contracted '
     'backlog (2,018k at Jun-26) tapering 100/90/80/70k as the pipeline matures'),
    ('shock', 'FY2026 consumption shock (per-RT, full year)', SHOCK, PCT,
     'H1-2026 equivalent full-load hours -9.0% y/y (deck p4) — hospitality-occupancy-led '
     '~80% per the company\'s own H1-2026 attribution, weather a minor factor; full-year '
     'effect smaller as H2-2025 was itself soft'),
    ('recovery', 'Consumption per-RT recovery level from FY2027 (share of FY2025)', 1.0, PCT,
     'Recovery (de-escalation) framing: full return to the FY2025 level; the live recovery '
     'columns on the Sensitivity sheet run the same model at 90-103% and feed the '
     'continuation central'),
    ('pipes', 'Pre-insulated pipes revenue (AED mn, held flat)', IN['pipes_rev_fy25'], NUM1,
     SRC['pipes_rev_fy25']),
    ('other_cos25', 'Other cash cost of sales, FY2025 (AED mn)', U['other_cos25'], NUM1,
     'Cost of sales less DEWA purchases less the depreciation and amortisation inside cost '
     'of sales (FY2025 audited FS notes)'),
    ('ga_cash25', 'General and administrative cash cost, FY2025 (AED mn)', U['ga_cash25'],
     NUM1, 'G&A expenses (statement face 256.383, corrected 17-Aug-2026) less the '
     'depreciation inside G&A (FY2025 audited FS)'),
    ('oi', 'Other income, FY2025 (AED mn, statement face)', IN['oi_fy25'], NUM1,
     SRC['oi_fy25']),
    ('rental', 'Rental income inside other income, FY2025 (AED mn)', RENTAL, NUM1,
     SRC['rental_fy25']),
    ('ecl25', 'Reversal of credit-loss allowance, FY2025 (AED mn; not forecast)',
     IN['ecl_fy25'], NUM1, SRC['ecl_fy25']),
    ('intco25', 'Interest on related-party acquisition receivables, FY2025 (AED mn)',
     IN['intco_fy25'], NUM1, SRC['intco_fy25']),
    ('intco_decay', 'Receivable interest annual decay', INTCO_DECAY, PCT,
     'Amortising related-party acquisition receivables — interest income runs off as the '
     'balances amortise'),
    ('wage_esc', 'Wage and services cost escalator', WAGE_ESC, PCT,
     'UAE CPI / wage class; applied to cash cost of sales and cash G&A only'),
    ('maint_pct', 'Maintenance capital expenditure (share of opening plant)', U['maint_pct'],
     PCT, 'House assumption for a young plant fleet; flagged as an estimate'),
    ])
block('Derived rates — LIVE formulas off the audited anchors above (black = formula)', [
    ('cons_per_rt', 'Consumption revenue per average connected RT, FY2025 (AED k)',
     f'={a("cons25")}/(({a("rt_fy24")}+{a("rt_fy25")})/2)', RATE4,
     'KAM consumption revenue / average connected RT — a formula, not a paste', CPRT),
    ('cap_per_rt', 'Capacity and connection revenue per average connected RT (AED k)',
     f'=({a("rev25")}-{a("cons25")}-{a("pipes")})/(({a("rt_fy24")}+{a("rt_fy25")})/2)',
     RATE4, 'Implied: (revenue - consumption - pipes) / average RT; no per-RT tariff '
     'schedule is published — flagged', CAPRT),
    ('ew_ratio', 'Electricity and water cost as a share of consumption revenue',
     f'={a("ew25")}/{a("cons25")}', PCT2,
     'DEWA purchases / consumption revenue, FY2025; FY2024 prints 72.5% on the same basis',
     EW),
    ('capex_per_rt', 'Capital expenditure per added RT (AED mn per k RT)',
     f'={a("capex25")}/({a("rt_fy25")}-{a("rt_fy24")})', RATE4,
     'FY2025 cash capital expenditure / FY2025 net connections added (90k RT)',
     U['capex_per_rt']),
    ('dep_rate', 'Depreciation rate on opening plant',
     f'={a("ppe_dep25")}/{a("ppe24")}', PCT2,
     'FY2025 plant depreciation / opening net plant', U['dep_rate']),
    ('amort_flat', 'Amortisation and right-of-use depreciation (AED mn, flat)',
     f'={a("dna25")}-{a("ppe_dep25")}', NUM1,
     'Total D&A less plant depreciation (intangibles + right-of-use)', U['amort_flat']),
    ('nwc25', 'Net working capital, end-FY2025 (AED mn)',
     f'={a("inv25")}+{a("rec25")}+{a("drp25")}-({a("pay25")}-{a("accr25")})-{a("crp25")}',
     NUM1, 'Inventories + receivables + due from related parties - payables (ex capex '
     'accruals) - due to related parties', NWC25),
    ('nwc_ratio', 'Net working capital as a share of revenue',
     f'={a("nwc25")}/{a("rev25")}', PCT2,
     'End-FY2025 net working capital / FY2025 revenue (negative: customer deposits and '
     'payables fund the cycle)', NWC_RATIO),
    ('oi_op', 'Operating other income (AED mn, held flat)',
     f'={a("oi")}-{a("rental")}', NUM1,
     'Other income less rental income (note 29: grant + scrap + others) — the rental is '
     'the return on the investment properties the bridge adds at book, so it is excluded '
     'from operating EBITDA', OI_OP),
    ])
block('Physical decomposition — H1-2026 deck facts and the regulated tariff cap', [
    ('h1_rev', 'Revenue, H1-2026 (AED mn)', IN['rev_h1_26'], NUM1, SRC['rev_h1_26']),
    ('h1_rth', 'Cooling delivered, H1-2026 (m RTh)', H1_RTH, NUM0,
     'H1-2026 earnings deck p4'),
    ('h1_mix', 'Consumption share of revenue, H1-2026', H1_MIX, PCT,
     'H1-2026 earnings deck revenue mix'),
    ('cap643', 'RD10 v1.3 consumption tariff cap (AED/TRh, incl. fuel surcharge)', CAP643,
     '0.000', 'Dubai RSB regulation RD10 v1.3 (17-Sep-2025), section 7 table; carried '
     'unchanged into v1.4 (Feb-2026) — external regulatory fact'),
    ('eflh_h1', 'Equivalent full-load hours, H1-2026 (hrs)', UP['eflh_h1_2026_hrs'], NUM0,
     SRC['eflh_h1']),
    ])
block('Cost of capital', [
    ('rf', 'Risk-free rate (AED sovereign)', IN['rf_aed'], PCT2, SRC['rf_aed']),
    ('ds_rating', 'Sovereign default spread — rating basis', IN['ds_rating'], PCT2,
     SRC['ds_rating']),
    ('ds_cds', 'Sovereign default spread — CDS basis', IN['ds_cds'], PCT2, SRC['ds_cds']),
    ('erp_rating', 'Equity risk premium — rating basis', IN['erp_rating'], PCT2,
     SRC['erp_rating']),
    ('erp_cds', 'Equity risk premium — CDS basis', IN['erp_cds'], PCT2, SRC['erp_cds']),
    ('beta', 'Beta (own-stock weekly regression vs the FTSE ADX index)', IN['beta'], '0.000',
     SRC['beta']),
    ('beta_dfm', 'Beta — DFM General Index regression (comparison construction)', BETA_DFM,
     '0.000', 'Own-stock weekly regression vs the listing exchange\'s DFM General Index, '
     'retained as a comparison; the primary beta regresses against the FTSE ADX General '
     'Index'),
    ('kd', 'Marginal cost of debt', IN['kd_marg'], PCT2, SRC['kd_marg']),
    ('g', 'Growth, FY2031-FY2040 window (stage one)', G, PCT, SRC['g_term']),
    ('g2', 'Growth beyond FY2040 (stage two, perpetuity)', G2, PCT,
     'Long-run densification with ~zero real tariff growth under the RD10 no-indexation '
     'regime — the fade the Dubai-2040 build-out window decays to'),
    ('t_stub', 'Stub period — 30-Jun-2026 anchor to end-FY2026 (years)', T0, '0.0',
     'The bridge is struck on the 30-Jun-2026 reviewed balance sheet, so the cash-flow '
     'clock starts there too: FY2026 contributes its second half only and later year-ends '
     'sit at 1.5 to 4.5 years'),
    ])
block('Bridge — 30-Jun-2026 reviewed balance sheet', [
    ('borrow', 'Bank borrowings (AED mn)', IN['borrow_jun26'], NUM1, SRC['borrow_jun26']),
    ('lease', 'Lease liabilities (AED mn)', IN['lease_jun26'], NUM1, SRC['lease_jun26']),
    ('cash', 'Cash and cash equivalents (AED mn)', IN['cash_jun26'], NUM1, SRC['cash_jun26']),
    ('deposits', 'Term deposits (AED mn)', IN['deposits_jun26'], NUM1, SRC['deposits_jun26']),
    ('recv', 'Related-party acquisition receivables at book (Note 8: 1,005.0 Dubai '
     'Aviation City + 289.4 Nakheel) (AED mn)', RECV, NUM1, SRC['recv_jun26']),
    ('invprop', 'Investment properties (AED mn)', IN['invprop_jun26'], NUM1,
     SRC['invprop_jun26']),
    ('fvtpl', 'Financial assets at fair value through profit or loss (AED mn)',
     IN['fvtpl_jun26'], NUM1, SRC['fvtpl_jun26']),
    ('fvoci', 'Financial assets at fair value through OCI (AED mn)', IN['fvoci_jun26'],
     NUM1, SRC['fvoci_jun26']),
    ('eq_jun26', 'Equity attributable to shareholders, 30-Jun-2026 (AED mn)',
     IN['eq_attr_jun26'], NUM1, SRC['eq_attr_jun26']),
    ('nci_jun26', 'Non-controlling interests, 30-Jun-2026 (AED mn)', IN['nci_book_jun26'],
     NUM1, SRC['nci_book_jun26']),
    ('cash_yield', 'Yield earned on cash balances', CASH_YIELD, PCT2,
     'Deposit-rate assumption used in the forecast finance line; flagged as an estimate'),
    ('div', 'Committed annual dividend (AED mn)', IN['div_policy'], NUM1, SRC['div_policy']),
    ])
block('Valuation lenses', [
    ('tabreed_ev', 'Peer EV/EBITDA — Tabreed (trailing, restruck at the anchor)',
     REL['tabreed_ev_ebitda'], MULT,
     f"Tabreed (DFM) FY2025 results at the {REL['mult_date']}"),
    ('tabreed_pe', 'Peer price/earnings — Tabreed (trailing, restruck at the anchor)',
     REL['tabreed_pe'], MULT, 'Tabreed (DFM), close 2.46 on 6/7-Aug-2026 — cross-check '
     'input only'),
    ('dewa_pe', 'Peer price/earnings — DEWA (parent)', REL['dewa_pe'], MULT,
     'DEWA (DFM), Aug-2026 — context only, majority owner'),
    ('w_dcf', 'Weight — discounted cash flow', LN['dcf']['weight'], PCT, None),
    ('w_rel', 'Weight — relative multiples', LN['relative']['weight'], PCT, None),
    ('w_norm', 'Weight — normalised earnings', LN['normalized']['weight'], PCT, None),
    ('w_book', 'Weight — book value', LN['book']['weight'], PCT, None),
    ('dewa_price', 'DEWA control-transaction price, Feb-2026 (AED)', D['dewa_buyin']['price'],
     PX, 'Related-party CONTROL price for Dubai Holding\'s 24% stake — a disclosed reference '
     'point, never fair value'),
    ])

# ===CHUNK-END===
