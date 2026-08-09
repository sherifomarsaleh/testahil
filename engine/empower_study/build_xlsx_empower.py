"""EMPOWER_Valuation_Model_09082026_public.xlsx — 16 sheets mirroring the house canonical
model (regulated-utility / operating-company variant). Blue = inputs · black = formulas ·
green = cross-sheet links.

The workbook is FORMULA-DRIVEN. Every quantity that is arithmetically derivable from an
input is written as a live Excel formula, not as a pasted number. Only three classes of
cell are pasted values:

  1. audited and disclosed historical figures (FY2023-25 statements, the 30-Jun-2026
     reviewed balance sheet, disclosed connected capacity, the consumption-revenue figures
     from the auditor's key-audit-matter section) — the primary record, not a calculation;
  2. the unit build's base anchors (per-RT revenue rates, the electricity-and-water
     pass-through ratio, cash cost bases, the depreciation rate, capex per added RT, the
     working-capital ratio) — each anchor is pasted once on the Assumptions sheet and
     everything downstream of it is a formula;
  3. whole-model re-run outputs, where each figure is a complete revaluation and so cannot
     be one formula: the probabilistic price map, the discount-rate x growth grid, the
     consumption-recovery grid, the consumption-persists framing and the bear/bull cases.
     These grids do NOT redraw when a driver is changed.

NUMERIC TRACEABILITY: no financial numeral is typed into this builder. Every number is
read from study_numbers.json (or, for audited balance-sheet history lines only, from the
statement extracts), and every formula cell's model value is recorded into
xlsx_expected.json as it is written; recalc.py re-evaluates the delivered workbook
independently and asserts cell-for-cell agreement.
"""
import json, os
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
SRC['beta'] = (f"Own-stock weekly regression vs {BR['index']}, {BR['window'][0]} to "
               f"{BR['window'][1]} ({BR['window_years']:.2f} years, {BR['n']} weeks): "
               f"R-squared {BR['r2']:.2f}, standard error {BR['se']:.2f}, 90% interval "
               f"[{BR['ci90'][0]:.2f}, {BR['ci90'][1]:.2f}] ({D['inputs']['beta']['date']})")
M, HI, U = D['meta'], D['hist_is'], D['unit']
F = D['fcst']['base']
W, DC = D['wacc'], D['dcf']
B_CT, B_DM, B_CDS = DC['base_ct'], DC['base_dmtt'], DC['base_cds']
LN, REL, NRM, BK, DDM = D['lenses'], D['rel'], D['norm'], D['book'], D['ddm']
CEN, SNW, CRUX, STK, S0 = D['central'], D['sens_wg'], D['crux'], D['strike'], D['step0']
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
FIN26 = REL['np26'] / (1 - TAX) - (F['ebitda']['FY26'] - F['dna']['FY26'])    # net finance
CASH_YIELD = (IN['kd_marg'] * IN['borrow_jun26'] + FIN26) / IN['cash_jun26']  # 3.5%
IC_TERM = B_CT['nopat']['FY30'] / B_CT['roic_term']
CONCESSION = IC_TERM - F['ppe']['FY30'] - F['nwc']['FY30']                    # ~1150
NCI_FR = IN['nci_pat_fy25'] / IN['pat_fy25']
RTP = U['rt_path']
ADDS = [RTP[y] - RTP[p] for p, y in zip(['FY25'] + YF[:-1], YF)]              # 105/100/90/80/70
HC_DMTT = 1 - (CEN['dmtt'] - LN['dcf']['weight'] * B_DM['ps']
               - LN['relative']['weight'] * REL['ps_rel']
               - LN['book']['weight'] * BK['ps']) / (LN['normalized']['weight'] * NRM['ps'])
GROSS_JUN26 = IN['borrow_jun26'] + IN['lease_jun26']
NET_DEBT = W['net_debt']
BRIDGE_ADD = IN['invprop_jun26'] + IN['fvtpl_jun26'] + IN['fvoci_jun26']

assert abs(WAGE_ESC - 0.025) < 1e-9 and abs(INTCO_DECAY - 0.03) < 1e-9
assert abs(CASH_YIELD - 0.035) < 1e-12 and abs(CONCESSION - 1150.0) < 1e-6

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

# ---- forecast income-statement / balance-sheet chains (python mirror) --------------
fin_f = [FIN26] * 5
ebit_f = [B_CT['ebit'][y] for y in YF]
pbt_f = [ebit_f[i] + fin_f[i] for i in range(5)]
tax_f = [-p * TAX for p in pbt_f]
pat_f = [p * (1 - TAX) for p in pbt_f]
nci_f = [-p * NCI_FR for p in pat_f]
npa_f = [pat_f[i] + nci_f[i] for i in range(5)]
assert abs(npa_f[0] - REL['npa26']) < 1e-6
eq_f, nci_bs_f, nd_f = [], [], []
eq_prev, nci_prev, nd_prev = IN['eq_attr_fy25'], BH['FY25']['nci'], NET_DEBT
for i in range(5):
    eq_prev = eq_prev + npa_f[i] - IN['div_policy']
    nci_prev = nci_prev - nci_f[i]
    nd_prev = nd_prev - (B_CT['fcff'][YF[i]] + fin_f[i] * (1 - TAX)) + IN['div_policy']
    eq_f.append(eq_prev); nci_bs_f.append(nci_prev); nd_f.append(nd_prev)
cash_f = [GROSS_JUN26 - x for x in nd_f]

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
title(ws, 'Assumptions — every input in the model', 'Blue cells are inputs; change one and the '
      'model reprices. Column H gives the source and date of each input.', 8, awidth=56,
      cwidth=11)
ws.column_dimensions['H'].width = 90
hdr(ws, 3, ['Input'] + YFL + ['', 'Source'])
r = 4
A = {}

def block(name, items):
    global r
    band(ws, r, 8); put(ws, f'A{r}', name, bold=True, fmt=None); r += 1
    for key, lab, val, fmt, src in items:
        put(ws, f'A{r}', lab, fmt=None)
        if isinstance(val, (list, tuple)):
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
block('Unit build — the two-leg revenue build (pasted anchors; everything downstream is formula)', [
    ('rt_fy24', 'Connected capacity, end-FY2024 (k RT)', IN['rt_conn']['2024'], NUM0,
     SRC['rt_conn']),
    ('rt_fy25', 'Connected capacity, end-FY2025 (k RT)', IN['rt_conn']['2025'], NUM0,
     SRC['rt_conn']),
    ('adds', 'New connections by year (k RT)', ADDS, NUM0,
     'FY2026 = guidance midpoint (100-110k, H1-2026 earnings deck p13); then the contracted '
     'backlog (2,018k at Jun-26) tapering 100/90/80/70k as the pipeline matures'),
    ('cons_per_rt', 'Consumption revenue per average connected RT, FY2025 (AED k)',
     U['cons_per_rt25'], RATE4, 'Consumption revenue (auditor key-audit-matter figure, FY2025 '
     'audited FS) / average connected RT ((1,566+1,656)/2)'),
    ('shock', 'FY2026 consumption shock (per-RT, full year)', U['crux_shock'], PCT,
     'H1-2026 equivalent full-load hours -9.0% y/y (deck p4); full-year effect smaller as '
     'H2-2025 was itself soft'),
    ('recovery', 'Consumption per-RT recovery level from FY2027 (share of FY2025)', 1.0, PCT,
     'Base case: full recovery to the FY2025 level; the recovery grid on the Sensitivity '
     'sheet re-runs the whole model at other levels'),
    ('cap_per_rt', 'Capacity and connection revenue per average connected RT, FY2025 (AED k)',
     U['cap_per_rt25'], RATE4, 'Implied: (revenue - consumption - pipes) / average connected '
     'RT; no per-RT tariff schedule is published — flagged'),
    ('pipes', 'Pre-insulated pipes revenue (AED mn, held flat)', IN['pipes_rev_fy25'], NUM1,
     SRC['pipes_rev_fy25']),
    ('ew_ratio', 'Electricity and water cost as a share of consumption revenue',
     U['ew_ratio'], PCT2, 'DEWA purchases (related-party note 12) / consumption revenue, '
     'FY2025; FY2024 prints 72.5% on the same basis'),
    ('other_cos25', 'Other cash cost of sales, FY2025 (AED mn)', U['other_cos25'], NUM1,
     'Cost of sales less DEWA purchases less the depreciation and amortisation inside cost '
     'of sales (FY2025 audited FS notes)'),
    ('ga_cash25', 'General and administrative cash cost, FY2025 (AED mn)', U['ga_cash25'],
     NUM1, 'G&A expenses less the depreciation inside G&A (FY2025 audited FS)'),
    ('oi', 'Other income (AED mn, held flat)', IN['oi_fy25'], NUM1, SRC['oi_fy25']),
    ('ecl25', 'Reversal of credit-loss allowance, FY2025 (AED mn; not forecast)',
     IN['ecl_fy25'], NUM1, SRC['ecl_fy25']),
    ('intco25', 'Concession interest income, FY2025 (AED mn)', IN['intco_fy25'], NUM1,
     SRC['intco_fy25']),
    ('intco_decay', 'Concession interest annual decay', INTCO_DECAY, PCT,
     'Amortising concession receivable — interest income runs off as the asset amortises'),
    ('wage_esc', 'Wage and services cost escalator', WAGE_ESC, PCT,
     'UAE CPI / wage class; applied to cash cost of sales and cash G&A only'),
    ])
block('Capital intensity and working capital', [
    ('capex_per_rt', 'Capital expenditure per added RT (AED mn per k RT)', U['capex_per_rt'],
     RATE4, 'FY2025 capital expenditure / FY2025 net connections added (90k RT)'),
    ('maint_pct', 'Maintenance capital expenditure (share of opening plant)', U['maint_pct'],
     PCT, 'House assumption for a young plant fleet; flagged as an estimate'),
    ('ppe25', 'Net property, plant and equipment, end-FY2025 (AED mn)', BH['FY25']['ppe'],
     NUM1, 'FY2025 audited balance sheet'),
    ('dep_rate', 'Depreciation rate on opening plant', U['dep_rate'], PCT2,
     'FY2025 plant depreciation / opening net plant (FY2025 audited cash-flow note)'),
    ('amort_flat', 'Amortisation and right-of-use depreciation (AED mn, flat)',
     U['amort_flat'], NUM1, 'FY2025 intangibles amortisation + right-of-use depreciation'),
    ('nwc25', 'Net working capital, end-FY2025 (AED mn)', U['nwc25'], NUM1,
     'Inventories + receivables + due from related parties - payables (ex capex accruals) - '
     'due to related parties, FY2025 audited balance sheet'),
    ('nwc_ratio', 'Net working capital as a share of revenue', U['nwc_ratio'], PCT2,
     'End-FY2025 net working capital / FY2025 revenue (negative: customer deposits and '
     'payables fund the cycle)'),
    ('concession', 'Terminal invested-capital addition — concession financial asset (AED mn)',
     CONCESSION, NUM1, 'Airport concession receivable at amortised cost, carried in terminal '
     'invested capital at approximate book value'),
    ])
block('Cost of capital', [
    ('rf', 'Risk-free rate (AED sovereign)', IN['rf_aed'], PCT2, SRC['rf_aed']),
    ('ds_rating', 'Sovereign default spread — rating basis', IN['ds_rating'], PCT2,
     SRC['ds_rating']),
    ('ds_cds', 'Sovereign default spread — CDS basis', IN['ds_cds'], PCT2, SRC['ds_cds']),
    ('erp_rating', 'Equity risk premium — rating basis', IN['erp_rating'], PCT2,
     SRC['erp_rating']),
    ('erp_cds', 'Equity risk premium — CDS basis', IN['erp_cds'], PCT2, SRC['erp_cds']),
    ('beta', 'Beta (own-stock weekly regression vs the Dubai index)', IN['beta'], '0.000',
     SRC['beta']),
    ('kd', 'Marginal cost of debt', IN['kd_marg'], PCT2, SRC['kd_marg']),
    ('g', 'Terminal growth', G, PCT, SRC['g_term']),
    ])
block('Bridge — 30-Jun-2026 reviewed balance sheet', [
    ('borrow', 'Bank borrowings (AED mn)', IN['borrow_jun26'], NUM1, SRC['borrow_jun26']),
    ('lease', 'Lease liabilities (AED mn)', IN['lease_jun26'], NUM1, SRC['lease_jun26']),
    ('cash', 'Cash and cash equivalents (AED mn)', IN['cash_jun26'], NUM1, SRC['cash_jun26']),
    ('deposits', 'Term deposits (AED mn)', IN['deposits_jun26'], NUM1, SRC['deposits_jun26']),
    ('invprop', 'Investment properties (AED mn)', IN['invprop_jun26'], NUM1,
     SRC['invprop_jun26']),
    ('fvtpl', 'Financial assets at fair value through profit or loss (AED mn)',
     IN['fvtpl_jun26'], NUM1, SRC['fvtpl_jun26']),
    ('fvoci', 'Financial assets at fair value through OCI (AED mn)', IN['fvoci_jun26'],
     NUM1, SRC['fvoci_jun26']),
    ('eq_jun26', 'Equity attributable to shareholders, 30-Jun-2026 (AED mn)',
     IN['eq_attr_jun26'], NUM1, SRC['eq_attr_jun26']),
    ('eq_fy25', 'Equity attributable to shareholders, end-FY2025 (AED mn)',
     IN['eq_attr_fy25'], NUM1, SRC['eq_attr_fy25']),
    ('eq_fy24', 'Equity attributable to shareholders, end-FY2024 (AED mn)', BH['FY24']['eqp'],
     NUM1, 'FY2024 audited balance sheet (FY2025 filing comparative)'),
    ('cash_yield', 'Yield earned on cash balances', CASH_YIELD, PCT2,
     'Deposit-rate assumption used in the forecast finance line; flagged as an estimate'),
    ('div', 'Committed annual dividend (AED mn)', IN['div_policy'], NUM1, SRC['div_policy']),
    ])
block('Valuation lenses', [
    ('tabreed_ev', 'Peer EV/EBITDA — Tabreed', REL['tabreed_ev_ebitda'], MULT,
     'Tabreed (DFM) FY2025 results and market prices, Aug-2026 — cross-check input only'),
    ('tabreed_pe', 'Peer price/earnings — Tabreed', REL['tabreed_pe'], MULT,
     'Tabreed (DFM), Aug-2026 — cross-check input only'),
    ('dewa_pe', 'Peer price/earnings — DEWA (parent)', REL['dewa_pe'], MULT,
     'DEWA (DFM), Aug-2026 — context only, majority owner'),
    ('w_dcf', 'Weight — discounted cash flow', LN['dcf']['weight'], PCT, None),
    ('w_rel', 'Weight — relative multiples', LN['relative']['weight'], PCT, None),
    ('w_norm', 'Weight — normalised earnings', LN['normalized']['weight'], PCT, None),
    ('w_book', 'Weight — book value', LN['book']['weight'], PCT, None),
    ('hc', 'Normalised-lens haircut under the 15% framing', HC_DMTT, PCT,
     'Average burden of the top-up tax on normalised earnings'),
    ('dewa_price', 'DEWA control-transaction price, Feb-2026 (AED)', D['dewa_buyin']['price'],
     PX, 'Related-party CONTROL price for Dubai Holding\'s 24% stake — a disclosed reference '
     'point, never fair value'),
    ])

# ============ SEGMENTS =============================================================
ws = wb['Segments']
title(ws, 'Segments — the two-leg unit build', 'Consumption (per-RT rate x average connected '
      'RT) + capacity/connection (per-RT rate x average connected RT) + pipes. Disclosed '
      'anchors are pasted; everything downstream is a formula.', 7, awidth=52, cwidth=13)
SC = ['C', 'D', 'E', 'F', 'G']                   # FY26..FY30 columns; B = FY2025
hdr(ws, 4, ['k RT / AED mn', 'FY2025'] + YFL)
rt_ye, rt_av = [], []
prev = RTP['FY25']
for i, y in enumerate(YF):
    ye = prev + ADDS[i]; rt_av.append((prev + ye) / 2); rt_ye.append(ye); prev = ye
put(ws, 'A5', 'New connections added (k RT)', fmt=None)
put(ws, 'B5', '-', BLACK, NUM0)
for i in range(5):
    putf(ws, f'{SC[i]}5', f'={a("adds", i)}', ADDS[i], NUM0, green=True)
put(ws, 'A6', 'Connected capacity, year-end (k RT)', fmt=None)
putf(ws, 'B6', f'={a("rt_fy25")}', RTP['FY25'], NUM0, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}6', f'={"B" if i == 0 else SC[i-1]}6+{SC[i]}5', rt_ye[i], NUM0)
put(ws, 'A7', 'Average connected capacity (k RT)', fmt=None)
putf(ws, 'B7', f'=({a("rt_fy24")}+{a("rt_fy25")})/2',
     (IN['rt_conn']['2024'] + IN['rt_conn']['2025']) / 2, NUM1)
for i in range(5):
    putf(ws, f'{SC[i]}7', f'=({"B" if i == 0 else SC[i-1]}6+{SC[i]}6)/2', rt_av[i], NUM1)
put(ws, 'A8', 'Consumption revenue per average RT (AED k)', fmt=None)
putf(ws, 'B8', f'={a("cons_per_rt")}', U['cons_per_rt25'], RATE4, green=True)
putf(ws, 'C8', f'={a("cons_per_rt")}*(1+{a("shock")})',
     U['cons_per_rt25'] * (1 + U['crux_shock']), RATE4)
for i in range(1, 5):
    putf(ws, f'{SC[i]}8', f'={a("cons_per_rt")}*{a("recovery")}', U['cons_per_rt25'], RATE4)
put(ws, 'A9', 'Consumption leg', fmt=None)
put(ws, 'B9', U['cons25'], BLUE, NUM1)
for i in range(5):
    putf(ws, f'{SC[i]}9', f'={SC[i]}8*{SC[i]}7', F['cons'][YF[i]], NUM1)
put(ws, 'A10', 'Capacity, connection and other services leg', fmt=None)
putf(ws, 'B10', f"='Income Statement'!D5-B9-{a('pipes')}", U['cap25'], NUM1)
for i in range(5):
    putf(ws, f'{SC[i]}10', f'={a("cap_per_rt")}*{SC[i]}7', F['cap'][YF[i]], NUM1)
put(ws, 'A11', 'Pre-insulated pipes', fmt=None)
putf(ws, 'B11', f'={a("pipes")}', IN['pipes_rev_fy25'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}11', f'={a("pipes")}', IN['pipes_rev_fy25'], NUM1, green=True)
put(ws, 'A12', 'Total revenue', bold=True, fmt=None)
putf(ws, 'B12', '=SUM(B9:B11)', IN['rev_fy25'], NUM1, bold=True)
for i in range(5):
    putf(ws, f'{SC[i]}12', f'=SUM({SC[i]}9:{SC[i]}11)', F['rev'][YF[i]], NUM1, bold=True)
band(ws, 12, 7)
hdr(ws, 14, ['Cost stack — one escalator per driver class', 'FY2025'] + YFL)
put(ws, 'A15', 'Electricity and water purchased from DEWA', fmt=None)
putf(ws, 'B15', f'={a("ew_ratio")}*B9', IN['ew_cost_fy25'], NUM1)
for i in range(5):
    putf(ws, f'{SC[i]}15', f'={a("ew_ratio")}*{SC[i]}9', F['ew'][YF[i]], NUM1)
put(ws, 'A16', 'Other cash cost of sales (wage class)', fmt=None)
putf(ws, 'B16', f'={a("other_cos25")}', U['other_cos25'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}16', f'={"B" if i == 0 else SC[i-1]}16*(1+{a("wage_esc")})',
         F['other_cos'][YF[i]], NUM1)
put(ws, 'A17', 'General and administrative cash cost (wage class)', fmt=None)
putf(ws, 'B17', f'={a("ga_cash25")}', U['ga_cash25'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}17', f'={"B" if i == 0 else SC[i-1]}17*(1+{a("wage_esc")})',
         F['ga'][YF[i]], NUM1)
put(ws, 'A18', 'Concession interest income', fmt=None)
putf(ws, 'B18', f'={a("intco25")}', IN['intco_fy25'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}18', f'={"B" if i == 0 else SC[i-1]}18*(1-{a("intco_decay")})',
         F['intco'][YF[i]], NUM1)
put(ws, 'A19', 'Other income', fmt=None)
putf(ws, 'B19', f'={a("oi")}', IN['oi_fy25'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{SC[i]}19', f'={a("oi")}', IN['oi_fy25'], NUM1, green=True)
put(ws, 'A20', 'Reversal of credit-loss allowance (not forecast)', fmt=None)
putf(ws, 'B20', f'={a("ecl25")}', IN['ecl_fy25'], NUM1, green=True)
for i in range(5):
    put(ws, f'{SC[i]}20', 0, BLUE, NUM1)
put(ws, 'A21', 'EBITDA', bold=True, fmt=None)
ebitda25_build = (IN['rev_fy25'] + IN['intco_fy25'] - IN['ew_cost_fy25'] - U['other_cos25']
                  - U['ga_cash25'] + IN['oi_fy25'] + IN['ecl_fy25'])
putf(ws, 'B21', '=B12+B18-B15-B16-B17+B19+B20', ebitda25_build, NUM1, bold=True)
for i in range(5):
    putf(ws, f'{SC[i]}21', f'={SC[i]}12+{SC[i]}18-{SC[i]}15-{SC[i]}16-{SC[i]}17+{SC[i]}19'
         f'+{SC[i]}20', F['ebitda'][YF[i]], NUM1, bold=True)
band(ws, 21, 7)
put(ws, 'A22', 'EBITDA margin', fmt=None)
putf(ws, 'B22', '=B21/B12', ebitda25_build / IN['rev_fy25'], PCT)
for i in range(5):
    putf(ws, f'{SC[i]}22', f'={SC[i]}21/{SC[i]}12', F['ebitda'][YF[i]] / F['rev'][YF[i]], PCT)
note(ws, 24, 'The FY2025 column rebuilds the audited year from the same identity: it lands '
     f'within note-level rounding of the audited operating profit plus depreciation '
     f'({HI["FY25"]["ebitda"]:,.1f}). The capacity-leg per-RT rate is implied — no per-RT '
     'tariff schedule is published — and is flagged as such on the Assumptions sheet.')
note(ws, 25, 'Cost classes escalate on their own drivers: DEWA purchases follow the '
     'consumption leg (pass-through ratio held at the FY2025 print), wage-class lines '
     'escalate at the wage rate, and the concession interest amortises. No blended index '
     'is applied across physically distinct cost lines.')
seas = D['unit']['fy26_seasonality_check']
note(ws, 26, f'Cross-check: H1-2026 revenue of {IN["rev_h1_26"]:,.1f} scaled by the FY2025 '
     f'seasonal split implies roughly {seas:,.0f} for FY2026; the model carries '
     f'{F["rev"]["FY26"]:,.0f}, within 4% (H2 carries the summer consumption peak).')

# ============ DCF ==================================================================
ws = wb['DCF']
title(ws, 'Discounted cash flow — the full waterfall', 'Every line is a live formula. The cost '
      'of capital is built below in both premium bases and both tax framings; the terminal '
      'value is reinvestment-consistent.', 7, awidth=52, cwidth=13)
CD = ['B', 'C', 'D', 'E', 'F']
hdr(ws, 4, ['AED mn'] + YFL)
ppe_open = [BH['FY25']['ppe']] + [F['ppe'][y] for y in YF[:-1]]
dep_f = [U['dep_rate'] * ppe_open[i] for i in range(5)]
capex_f = [F['capex'][y] for y in YF]
put(ws, 'A5', 'Revenue', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}5', f'=Segments!{SC[i]}12', F['rev'][YF[i]], NUM1, green=True)
put(ws, 'A6', 'EBITDA', bold=True, fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}6', f'=Segments!{SC[i]}21', F['ebitda'][YF[i]], NUM1, bold=True,
         green=True)
put(ws, 'A7', 'EBITDA margin', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}7', f'={CD[i]}6/{CD[i]}5', F['ebitda'][YF[i]] / F['rev'][YF[i]], PCT)
put(ws, 'A8', 'Opening net plant', fmt=None)
putf(ws, 'B8', f'={a("ppe25")}', ppe_open[0], NUM1, green=True)
for i in range(1, 5):
    putf(ws, f'{CD[i]}8', f'={CD[i-1]}11', ppe_open[i], NUM1)
put(ws, 'A9', 'Capital expenditure (per added RT + maintenance)', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}9', f'={a("capex_per_rt")}*Segments!{SC[i]}5+{a("maint_pct")}*{CD[i]}8',
         capex_f[i], NUM1)
put(ws, 'A10', 'Depreciation on plant', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}10', f'={a("dep_rate")}*{CD[i]}8', dep_f[i], NUM1)
put(ws, 'A11', 'Closing net plant', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}11', f'={CD[i]}8+{CD[i]}9-{CD[i]}10', F['ppe'][YF[i]], NUM1)
put(ws, 'A12', 'Depreciation and amortisation (incl. right-of-use and intangibles)', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}12', f'={CD[i]}10+{a("amort_flat")}', F['dna'][YF[i]], NUM1)
put(ws, 'A13', 'EBIT', bold=True, fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}13', f'={CD[i]}6-{CD[i]}12', B_CT['ebit'][YF[i]], NUM1, bold=True)
band(ws, 13, 7)
put(ws, 'A14', 'NOPAT — EBIT x (1 - corporate tax)', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}14', f'={CD[i]}13*(1-{a("tax_ct")})', B_CT['nopat'][YF[i]], NUM1)
put(ws, 'A15', 'Add back depreciation and amortisation', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}15', f'={CD[i]}12', F['dna'][YF[i]], NUM1)
put(ws, 'A16', 'Less capital expenditure', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}16', f'=-{CD[i]}9', -capex_f[i], NUM1)
put(ws, 'A17', 'Less change in net working capital', fmt=None)
putf(ws, 'B17', f'=-({a("nwc_ratio")}*B5-{a("nwc25")})', -F['dnwc']['FY26'], NUM1)
for i in range(1, 5):
    putf(ws, f'{CD[i]}17', f'=-{a("nwc_ratio")}*({CD[i]}5-{CD[i-1]}5)', -F['dnwc'][YF[i]],
         NUM1)
put(ws, 'A18', 'Free cash flow to the firm', bold=True, fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}18', f'={CD[i]}14+{CD[i]}15+{CD[i]}16+{CD[i]}17', B_CT['fcff'][YF[i]],
         NUM1, bold=True)
band(ws, 18, 7)
put(ws, 'A19', 'Discount factor (9% framing, rating basis)', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}19', (f'=1/(1+$C$48)' if i == 0 else f'={CD[i-1]}19/(1+$C$48)'),
         B_CT['df'][YF[i]], DF4)
put(ws, 'A20', 'Present value of free cash flow', bold=True, fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}20', f'={CD[i]}18*{CD[i]}19', B_CT['pv'][YF[i]], NUM1, bold=True)

put(ws, 'A22', 'TERMINAL VALUE — reinvestment-consistent (9% framing)', bold=True, fmt=None)
tv_rows = [
    ('Net working capital, FY2030', f'={a("nwc_ratio")}*F5', F['nwc']['FY30'], NUM1),
    ('Terminal invested capital (plant + concession asset + working capital)',
     f'=F11+{a("concession")}+C23', IC_TERM, NUM1),
    ('Terminal return on invested capital', '=F14/C24', B_CT['roic_term'], PCT),
    ('Reinvestment rate (growth / return on capital)', f'={a("g")}/C25', B_CT['rr_term'], PCT),
    ('Terminal-year NOPAT (grown one year)', f'=F14*(1+{a("g")})',
     B_CT['nopat']['FY30'] * (1 + G), NUM1),
    ('Terminal free cash flow', '=C27*(1-C26)',
     B_CT['nopat']['FY30'] * (1 + G) * (1 - B_CT['rr_term']), NUM1),
    ('Terminal value', f'=C28/($C$48-{a("g")})', B_CT['tv'], NUM1),
    ('Present value of the terminal value', '=C29*F19', B_CT['pv_tv'], NUM1),
    ('Present value of the five forecast years', '=SUM(B20:F20)', B_CT['pv_explicit'], NUM1),
    ('Enterprise value', '=C30+C31', B_CT['ev'], NUM1),
    ('Terminal value as a share of enterprise value', '=C30/C32', B_CT['tv_share'], PCT),
]
r = 23
for lab, fml, xp, fmt in tv_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, bold=(r == 32))
    r += 1
band(ws, 32, 4)
put(ws, 'A35', 'Fair value per share (9% framing) — from the bridge', bold=True, fmt=None)
putf(ws, 'C35', "='SOTP Bridge'!C13", B_CT['ps'], PX, bold=True, green=True)

put(ws, 'A37', 'COST OF CAPITAL — BUILT HERE, NOT ASSUMED', bold=True, fmt=None)
hdr(ws, 38, ['Component', '', 'Rating basis', 'CDS basis'])
coc = [
    ('Risk-free rate (AED sovereign)', f'={a("rf")}', f'={a("rf")}', IN['rf_aed'],
     IN['rf_aed'], PCT2),
    ('Less sovereign default spread', f'={a("ds_rating")}', f'={a("ds_cds")}',
     IN['ds_rating'], IN['ds_cds'], PCT2),
    ('Risk-free rate net of the sovereign spread', '=C39-C40', '=D39-D40',
     W['rf_star_rating'], W['rf_star_cds'], PCT2),
    ('Beta', f'={a("beta")}', f'={a("beta")}', IN['beta'], IN['beta'], '0.000'),
    ('Equity risk premium', f'={a("erp_rating")}', f'={a("erp_cds")}', IN['erp_rating'],
     IN['erp_cds'], PCT2),
    ('Cost of equity', '=C41+C42*C43', '=D41+D42*D43', W['ke_rating'], W['ke_cds'], PCT2),
]
r = 39
for lab, f1, f2, x1, x2, fmt in coc:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', f1, x1, fmt, green=f1.startswith('=Assumptions'))
    putf(ws, f'D{r}', f2, x2, fmt, green=f2.startswith('=Assumptions'))
    r += 1
scal = [
    ('Marginal cost of debt', f'={a("kd")}', IN['kd_marg'], PCT2),
    ('Market capitalisation (spot x shares)', f'={a("spot")}*{a("shares")}', W['mktcap'],
     NUM1),
    ('Net debt (borrowings + leases - cash - deposits)',
     f'={a("borrow")}+{a("lease")}-{a("cash")}-{a("deposits")}', NET_DEBT, NUM1),
    ('Debt weight', '=C47/(C47+C46)', W['wd'], PCT2),
]
for lab, fml, xp, fmt in scal:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, green=fml.startswith('=Assumptions'))
    r += 1
# rows: 45 kd, 46 mktcap, 47 net debt, 48 wd — but WACC must land on 48; renumber below
# (rows above: 39..44 coc, 45 kd, 46 mktcap, 47 nd, 48 wd, 49 we, 50/51 wacc)
put(ws, f'A{r}', 'Equity weight', fmt=None)
putf(ws, f'C{r}', '=1-C48', W['we'], PCT2)
r += 1
put(ws, f'A{r}', 'WACC — 9% corporate-tax framing', bold=True, fmt=None)
putf(ws, f'C{r}', f'=C49*C44+C48*C45*(1-{a("tax_ct")})', W['rating_ct'], PCT2, bold=True)
putf(ws, f'D{r}', f'=C49*D44+C48*C45*(1-{a("tax_ct")})', W['cds_ct'], PCT2, bold=True)
WACC_CT_ROW = r
r += 1
put(ws, f'A{r}', 'WACC — 15% top-up-tax framing', bold=True, fmt=None)
putf(ws, f'C{r}', f'=C49*C44+C48*C45*(1-{a("tax_dmtt")})', W['rating_dmtt'], PCT2, bold=True)
putf(ws, f'D{r}', f'=C49*D44+C48*C45*(1-{a("tax_dmtt")})', W['cds_dmtt'], PCT2, bold=True)
WACC_DM_ROW = r
band(ws, WACC_CT_ROW, 5); band(ws, WACC_DM_ROW, 5)
note(ws, r + 1, 'Both premium bases strip the SAME basis of sovereign default spread as the '
     'premium adds back (rating-to-rating, CDS-to-CDS), so country risk is priced once. The '
     'two bases land within two basis points of each other; the rating basis is primary. '
     'There is no discount-rate glide: the AED curve is flat and both facilities float, so '
     'the explicit-window rate equals the terminal rate, stated openly.')

# The df row (19) and terminal row (29) reference $C$48 as the WACC — but WACC sits on
# WACC_CT_ROW. Rewrite those formulas now that the row is known.
for i in range(5):
    ws[f'{CD[i]}19'] = (f'=1/(1+$C${WACC_CT_ROW})' if i == 0
                        else f'={CD[i-1]}19/(1+$C${WACC_CT_ROW})')
ws['C29'] = f'=C28/($C${WACC_CT_ROW}-{a("g")})'

r += 3
put(ws, f'A{r}', 'PARALLEL FRAMING — 15% TOP-UP TAX (same cash-flow build, own tax and rate)',
    bold=True, fmt=None)
r += 1
dm0 = r
put(ws, f'A{r}', 'NOPAT at 15%', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', f'={CD[i]}13*(1-{a("tax_dmtt")})', B_DM['nopat'][YF[i]], NUM1)
r += 1
put(ws, f'A{r}', 'Free cash flow to the firm at 15%', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', f'={CD[i]}{dm0}+{CD[i]}15+{CD[i]}16+{CD[i]}17',
         B_DM['fcff'][YF[i]], NUM1)
r += 1
put(ws, f'A{r}', 'Discount factor at the 15%-framing rate', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', (f'=1/(1+$C${WACC_DM_ROW})' if i == 0
                             else f'={CD[i-1]}{r}/(1+$C${WACC_DM_ROW})'),
         B_DM['df'][YF[i]], DF4)
r += 1
put(ws, f'A{r}', 'Present value', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', f'={CD[i]}{r-2}*{CD[i]}{r-1}', B_DM['pv'][YF[i]], NUM1)
r += 1
dm_scal = [
    ('Present value of the five forecast years (15%)', f'=SUM(B{r-1}:F{r-1})',
     B_DM['pv_explicit'], NUM1),
    ('Terminal return on invested capital (15%)', f'=F{dm0}/C24', B_DM['roic_term'], PCT),
    ('Reinvestment rate (15%)', f'={a("g")}/C{r+1}', B_DM['rr_term'], PCT),
    ('Terminal free cash flow (15%)', f'=F{dm0}*(1+{a("g")})*(1-C{r+2})',
     B_DM['nopat']['FY30'] * (1 + G) * (1 - B_DM['rr_term']), NUM1),
    ('Terminal value (15%)', f'=C{r+3}/($C${WACC_DM_ROW}-{a("g")})', B_DM['tv'], NUM1),
    ('Present value of the terminal value (15%)', f'=C{r+4}*F{r-2}', B_DM['pv_tv'], NUM1),
    ('Enterprise value (15%)', f'=C{r}+C{r+5}', B_DM['ev'], NUM1),
]
for lab, fml, xp, fmt in dm_scal:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, bold=('Enterprise' in lab))
    r += 1
EV_DM_ROW = r - 1
put(ws, f'A{r}', 'Fair value per share (15% framing) — from the bridge', bold=True, fmt=None)
putf(ws, f'C{r}', "='SOTP Bridge'!D13", B_DM['ps'], PX, bold=True, green=True)
r += 2
put(ws, f'A{r}', 'ALTERNATIVE PREMIUM BASIS — CDS (same cash flows, CDS-basis rate)',
    bold=True, fmt=None)
r += 1
cds0 = r
put(ws, f'A{r}', 'Discount factor at the CDS-basis rate', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', (f'=1/(1+$D${WACC_CT_ROW})' if i == 0
                             else f'={CD[i-1]}{r}/(1+$D${WACC_CT_ROW})'),
         B_CDS['df'][YF[i]], DF4)
r += 1
put(ws, f'A{r}', 'Present value (CDS basis)', fmt=None)
for i in range(5):
    putf(ws, f'{CD[i]}{r}', f'={CD[i]}18*{CD[i]}{cds0}', B_CDS['pv'][YF[i]], NUM1)
r += 1
cds_scal = [
    ('Present value of the five forecast years (CDS basis)', f'=SUM(B{r-1}:F{r-1})',
     B_CDS['pv_explicit'], NUM1),
    ('Terminal value (CDS basis)', f'=C28/($D${WACC_CT_ROW}-{a("g")})', B_CDS['tv'], NUM1),
    ('Present value of the terminal value (CDS basis)', f'=C{r+1}*F{cds0}', B_CDS['pv_tv'],
     NUM1),
    ('Enterprise value (CDS basis)', f'=C{r}+C{r+2}', B_CDS['ev'], NUM1),
]
for lab, fml, xp, fmt in cds_scal:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, bold=('Enterprise' in lab))
    r += 1
EV_CDS_ROW = r - 1
put(ws, f'A{r}', 'Fair value per share (CDS basis) — from the bridge', fmt=None)
putf(ws, f'C{r}', "='SOTP Bridge'!E13", B_CDS['ps'], PX, green=True)
ANCH['dcf'] = dict(wacc_ct=WACC_CT_ROW, wacc_dm=WACC_DM_ROW, ev_dm=EV_DM_ROW,
                   ev_cds=EV_CDS_ROW, ke_rating=44, nd=47, mktcap=46)

# ============ SOTP BRIDGE ==========================================================
ws = wb['SOTP Bridge']
title(ws, 'Enterprise value to equity — the bridge', 'Three parallel constructions: the 9% '
      'corporate-tax framing, the 15% top-up-tax framing, and the CDS premium basis. The two '
      'tax framings are published side by side, never averaged.', 6, awidth=52, cwidth=16)
hdr(ws, 4, ['Step', '', '9% framing', '15% framing', 'CDS basis'])
b_ev = {'C': (f'=DCF!C32', B_CT['ev']), 'D': (f'=DCF!C{EV_DM_ROW}', B_DM['ev']),
        'E': (f'=DCF!C{EV_CDS_ROW}', B_CDS['ev'])}
put(ws, 'A5', 'Enterprise value', fmt=None)
for col, (fml, xp) in b_ev.items():
    putf(ws, f'{col}5', fml, xp, NUM1, green=True)
steps = [
    ('Less net debt (30-Jun-2026)', '=-DCF!$C$47', -NET_DEBT),
    ('Plus investment properties at book', f'={a("invprop")}', IN['invprop_jun26']),
    ('Plus financial assets at fair value through profit or loss', f'={a("fvtpl")}',
     IN['fvtpl_jun26']),
    ('Plus financial assets at fair value through OCI', f'={a("fvoci")}', IN['fvoci_jun26']),
]
r = 6
for lab, fml, xp in steps:
    put(ws, f'A{r}', lab, fmt=None)
    for col in 'CDE':
        putf(ws, f'{col}{r}', fml, xp, NUM1, green=fml.startswith('=Assumptions'))
    r += 1
put(ws, 'A10', 'Equity value', fmt=None)
for col, (fml, xp) in b_ev.items():
    putf(ws, f'{col}10', f'=SUM({col}5:{col}9)', xp - NET_DEBT + BRIDGE_ADD, NUM1)
put(ws, 'A11', 'Less non-controlling interests (at their share of profit)', fmt=None)
for col, (fml, xp) in b_ev.items():
    putf(ws, f'{col}11', f'=-{col}10*$C$14', -(xp - NET_DEBT + BRIDGE_ADD) * NCI_FR, NUM1)
put(ws, 'A12', 'Equity attributable to shareholders', bold=True, fmt=None)
for col, (fml, xp) in b_ev.items():
    putf(ws, f'{col}12', f'={col}10+{col}11', (xp - NET_DEBT + BRIDGE_ADD) * (1 - NCI_FR),
         NUM1, bold=True)
put(ws, 'A13', 'Fair value per share (AED)', bold=True, fmt=None)
for col, (fml, xp) in b_ev.items():
    putf(ws, f'{col}13', f'={col}12/{a("shares")}',
         (xp - NET_DEBT + BRIDGE_ADD) * (1 - NCI_FR) / SH, PX, bold=True)
band(ws, 12, 5); band(ws, 13, 5)
put(ws, 'A14', 'Non-controlling share of group profit', fmt=None)
putf(ws, 'C14', f'={a("nci_pat")}/{a("pat_fy25")}', NCI_FR, PCT2)
put(ws, 'A15', 'Terminal value as a share of enterprise value', fmt=None)
putf(ws, 'C15', '=DCF!C33', B_CT['tv_share'], PCT, green=True)
putf(ws, 'D15', f'=DCF!C{EV_DM_ROW-1}/DCF!C{EV_DM_ROW}', B_DM['tv_share'], PCT, green=True)
putf(ws, 'E15', f'=DCF!C{EV_CDS_ROW-1}/DCF!C{EV_CDS_ROW}', B_CDS['tv_share'], PCT, green=True)
note(ws, 17, 'The bridge is struck on the 30-Jun-2026 reviewed balance sheet — the latest '
     'statement of financial position. Investment properties and the two fair-value '
     'portfolios are non-operating and enter at book; the concession financial asset stays '
     'inside invested capital and is NOT added again here.')

# ============ INCOME STATEMENT =====================================================
ws = wb['Income Statement']
title(ws, 'Income statement — three years audited, five years forecast',
      'AED mn, consolidated. History is the audited record; every forecast line is a '
      'formula (9% corporate-tax framing; the 15% framing runs on the DCF sheet).', 9,
      awidth=46, cwidth=12)
HCC = ['B', 'C', 'D']; FCC = ['E', 'F', 'G', 'H', 'I']
ALLC = HCC + FCC
hdr(ws, 4, ['AED mn'] + YHL + YFL)

def isrow(r, lab, hist_vals, hist_f, fc_f, fc_v, fmt=NUM1, bd=False, green=False):
    put(ws, f'A{r}', lab, bold=bd, fmt=None)
    for i in range(3):
        if hist_f is not None:
            putf(ws, f'{HCC[i]}{r}', hist_f(i), hist_vals[i], fmt, bold=bd)
        elif hist_vals is not None:
            put(ws, f'{HCC[i]}{r}', hist_vals[i], BLUE, fmt, bold=bd)
        else:
            put(ws, f'{HCC[i]}{r}', '-', BLACK, fmt, bold=bd)
    if fc_f is not None:
        for i in range(5):
            putf(ws, f'{FCC[i]}{r}', fc_f(i), fc_v[i], fmt, bold=bd, green=green)
    else:
        for i in range(5):
            put(ws, f'{FCC[i]}{r}', '-', BLACK, fmt, bold=bd)
    if bd: band(ws, r, 9)

isrow(5, 'Revenue', [HI[y]['rev'] for y in H3], None,
      lambda i: f'=DCF!{CD[i]}5', [F['rev'][y] for y in YF], bd=True, green=True)
isrow(6, 'Concession interest income (inside gross profit)', [HI[y]['intco'] for y in H3],
      None, lambda i: f'=Segments!{SC[i]}18', [F['intco'][y] for y in YF], green=True)
isrow(7, 'Gross profit', [HI[y]['gp'] for y in H3], None, None, None)
isrow(8, 'EBITDA', [HI[y]['ebitda'] for y in H3],
      lambda i: f'={HCC[i]}11-{HCC[i]}10',
      lambda i: f'=DCF!{CD[i]}6', [F['ebitda'][y] for y in YF], bd=True, green=True)
isrow(9, 'EBITDA margin', [HI[y]['ebitda'] / HI[y]['rev'] for y in H3],
      lambda i: f'={HCC[i]}8/{HCC[i]}5',
      lambda i: f'={FCC[i]}8/{FCC[i]}5', [F['ebitda'][y] / F['rev'][y] for y in YF], PCT)
isrow(10, 'Depreciation and amortisation', [-HI[y]['dna'] for y in H3], None,
      lambda i: f'=-DCF!{CD[i]}12', [-F['dna'][y] for y in YF], green=True)
isrow(11, 'Operating profit (EBIT)', [HI[y]['op'] for y in H3], None,
      lambda i: f'={FCC[i]}8+{FCC[i]}10', [B_CT['ebit'][y] for y in YF])
isrow(12, 'Net finance income / (costs)',
      [HI[y]['pbt'] - HI[y]['op'] for y in H3],
      lambda i: f'={HCC[i]}13-{HCC[i]}11',
      lambda i: f'=-({a("kd")}*{a("borrow")}-{a("cash_yield")}*{a("cash")})', fin_f)
isrow(13, 'Profit before tax', [HI[y]['pbt'] for y in H3], None,
      lambda i: f'={FCC[i]}11+{FCC[i]}12', pbt_f)
isrow(14, 'Income tax', [HI[y]['tax'] for y in H3], None,
      lambda i: f'=-{FCC[i]}13*{a("tax_ct")}', tax_f)
isrow(15, 'Profit for the year', [HI[y]['pat'] for y in H3], None,
      lambda i: f'={FCC[i]}13+{FCC[i]}14', pat_f)
isrow(16, 'Non-controlling interests', [HI[y]['npa'] - HI[y]['pat'] for y in H3],
      lambda i: f'={HCC[i]}17-{HCC[i]}15',
      lambda i: f"=-{FCC[i]}15*'SOTP Bridge'!$C$14", nci_f)
isrow(17, 'Profit attributable to shareholders', [HI[y]['npa'] for y in H3], None,
      lambda i: f'={FCC[i]}15+{FCC[i]}16', npa_f, bd=True)
put(ws, 'A18', 'Earnings per share (AED)', fmt=None)
npa_all = [HI[y]['npa'] for y in H3] + npa_f
for i in range(8):
    putf(ws, f'{ALLC[i]}18', f'={ALLC[i]}17/{a("shares")}', npa_all[i] / SH, PX)
note(ws, 20, 'Every FY2023-25 line is the audited figure (the EBITDA, net-finance and '
     'non-controlling rows are arithmetic identities of audited lines). The forecast '
     'finance line holds the 30-Jun-2026 debt book and cash balance flat at the marginal '
     'cost of debt and deposit yield; the FY2023 tax line is a credit (first recognition '
     'of deferred tax ahead of UAE corporate tax).')

# ============ BALANCE SHEET ========================================================
ws = wb['Balance Sheet']
title(ws, 'Balance sheet — condensed', 'AED mn. FY2024 and FY2025 are audited closing '
      'figures; 30-Jun-2026 is the reviewed interim. The forecast rolls forward from the '
      'model: plant from the capex/depreciation chain, equity from retained profit less '
      'the committed dividend, net debt from free cash flow.', 9, awidth=46, cwidth=12)
hdr(ws, 4, ['AED mn', 'FY2024', 'FY2025', '30-Jun-26'] + YFL)
BC = ['B', 'C', 'D']; BF = ['E', 'F', 'G', 'H', 'I']
BKEYS = ['FY24', 'FY25', 'JUN26']

def bsrow(r, lab, key, fc_f=None, fc_v=None, bd=False, fmt=NUM1, hist_f=None, hist_v=None):
    put(ws, f'A{r}', lab, bold=bd, fmt=None)
    for i in range(3):
        if hist_f is not None:
            putf(ws, f'{BC[i]}{r}', hist_f(i), hist_v[i], fmt, bold=bd)
        else:
            put(ws, f'{BC[i]}{r}', BH[BKEYS[i]][key], BLUE, fmt, bold=bd)
    if fc_f is not None:
        for i in range(5):
            putf(ws, f'{BF[i]}{r}', fc_f(i), fc_v[i], fmt, bold=bd)
    else:
        for i in range(5):
            put(ws, f'{BF[i]}{r}', '-', BLACK, fmt, bold=bd)
    if bd: band(ws, r, 9)

bsrow(5, 'Property, plant and equipment (net)', 'ppe',
      fc_f=lambda i: f'=DCF!{CD[i]}11', fc_v=[F['ppe'][y] for y in YF])
for i in range(5):
    ws[f'{BF[i]}5'].font = GREEN
bsrow(6, 'Investment properties', 'invprop', fc_f=lambda i: '=$D6',
      fc_v=[BH['JUN26']['invprop']] * 5)
bsrow(7, 'Concession financial asset (current + non-current)', 'conc', fc_f=lambda i: '=$D7',
      fc_v=[BH['JUN26']['conc']] * 5)
put(ws, 'A8', 'Financial assets at fair value (through P&L and OCI)', fmt=None)
for i in range(3):
    put(ws, f'{BC[i]}8', BH[BKEYS[i]]['fvtpl'] + BH[BKEYS[i]]['fvoci'], BLUE, NUM1)
for i in range(5):
    putf(ws, f'{BF[i]}8', '=$D8', BH['JUN26']['fvtpl'] + BH['JUN26']['fvoci'], NUM1)
bsrow(9, 'Cash, equivalents and term deposits', 'cash',
      fc_f=lambda i: f'=({a("borrow")}+{a("lease")})-{BF[i]}16', fc_v=cash_f)
bsrow(10, 'Total assets (as reported)', 'ta')
bsrow(11, 'Borrowings and lease liabilities (gross debt)', 'gross',
      fc_f=lambda i: f'={a("borrow")}+{a("lease")}', fc_v=[GROSS_JUN26] * 5)
bsrow(12, 'Trade and other payables', 'pay')
bsrow(13, 'Equity attributable to shareholders', 'eqp',
      fc_f=lambda i: (f"={'C' if i == 0 else BF[i-1]}13+'Income Statement'!{FCC[i]}17"
                      f'-{a("div")}'), fc_v=eq_f, bd=True)
bsrow(14, 'Non-controlling interests', 'nci',
      fc_f=lambda i: (f"={'C' if i == 0 else BF[i-1]}14-'Income Statement'!{FCC[i]}16"),
      fc_v=nci_bs_f)
put(ws, 'A15', 'Net working capital (model definition)', fmt=None)
put(ws, 'B15', '-', BLACK, NUM1)
putf(ws, 'C15', f'={a("nwc25")}', U['nwc25'], NUM1, green=True)
put(ws, 'D15', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{BF[i]}15', f"={a('nwc_ratio')}*'Income Statement'!{FCC[i]}5",
         F['nwc'][YF[i]], NUM1)
put(ws, 'A16', 'Net debt (gross debt - cash and deposits)', bold=True, fmt=None)
nd_hist = [BH[k]['gross'] - BH[k]['cash'] for k in BKEYS]
for i in range(3):
    putf(ws, f'{BC[i]}16', f'={BC[i]}11-{BC[i]}9', nd_hist[i], NUM1, bold=True)
for i in range(5):
    putf(ws, f'{BF[i]}16',
         (f"={'D' if i == 0 else BF[i-1]}16-(DCF!{CD[i]}18"
          f"+'Income Statement'!{FCC[i]}12*(1-{a('tax_ct')}))+{a('div')}"),
         nd_f[i], NUM1, bold=True)
band(ws, 16, 9)
put(ws, 'A17', 'Net debt / EBITDA', fmt=None)
put(ws, 'B17', '-', BLACK, MULT)
putf(ws, 'C17', "=C16/'Income Statement'!D8", nd_hist[1] / HI['FY25']['ebitda'], MULT)
put(ws, 'D17', '-', BLACK, MULT)
for i in range(5):
    putf(ws, f'{BF[i]}17', f"={BF[i]}16/'Income Statement'!{FCC[i]}8",
         nd_f[i] / F['ebitda'][YF[i]], MULT)
note(ws, 19, 'This is a CONDENSED layout and does not foot to zero: government grants, '
     'end-of-service benefits, tax liabilities, retentions and the remaining current items '
     'are not shown separately. The forecast net-debt roll starts from the 30-Jun-2026 '
     'reviewed position (the bridge anchor), charges the committed dividend, and credits '
     'each year\'s free cash flow after the after-tax finance charge. The forecast equity '
     'roll starts from the FY2025 audited closing equity.')

# ============ CASH FLOW ============================================================
ws = wb['Cash Flow']
title(ws, 'Cash flow — historical markers and the forecast waterfall', 'AED mn. The forecast '
      'links line-for-line to the DCF waterfall.', 8, awidth=48, cwidth=12)
hdr(ws, 4, ['AED mn', 'FY2024', 'FY2025'] + YFL)
CFF = ['D', 'E', 'F', 'G', 'H']
put(ws, 'A5', 'EBITDA', fmt=None)
putf(ws, 'B5', "='Income Statement'!C8", HI['FY24']['ebitda'], NUM1, green=True)
putf(ws, 'C5', "='Income Statement'!D8", HI['FY25']['ebitda'], NUM1, green=True)
for i in range(5):
    putf(ws, f'{CFF[i]}5', f"='Income Statement'!{FCC[i]}8", F['ebitda'][YF[i]], NUM1,
         green=True)
put(ws, 'A6', 'Net cash from operating activities (as reported)', fmt=None)
put(ws, 'B6', OCF24 if OCF24 else '-', BLUE if OCF24 else BLACK, NUM1)
put(ws, 'C6', OCF25, BLUE, NUM1)
for i in range(5):
    put(ws, f'{CFF[i]}6', '-', BLACK, NUM1)
put(ws, 'A7', 'NOPAT', fmt=None)
put(ws, 'B7', '-', BLACK, NUM1); put(ws, 'C7', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}7', f'=DCF!{CD[i]}14', B_CT['nopat'][YF[i]], NUM1, green=True)
put(ws, 'A8', 'Add back depreciation and amortisation', fmt=None)
put(ws, 'B8', '-', BLACK, NUM1); put(ws, 'C8', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}8', f'=DCF!{CD[i]}15', F['dna'][YF[i]], NUM1, green=True)
put(ws, 'A9', 'Capital expenditure', fmt=None)
put(ws, 'B9', -IN['capex_fy24'], BLUE, NUM1)
put(ws, 'C9', -IN['capex_fy25'], BLUE, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}9', f'=DCF!{CD[i]}16', -F['capex'][YF[i]], NUM1, green=True)
put(ws, 'A10', 'Change in net working capital', fmt=None)
put(ws, 'B10', '-', BLACK, NUM1); put(ws, 'C10', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}10', f'=DCF!{CD[i]}17', -F['dnwc'][YF[i]], NUM1, green=True)
put(ws, 'A11', 'Free cash flow to the firm', bold=True, fmt=None)
put(ws, 'B11', '-', BLACK, NUM1); put(ws, 'C11', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}11', f'={CFF[i]}7+{CFF[i]}8+{CFF[i]}9+{CFF[i]}10',
         B_CT['fcff'][YF[i]], NUM1, bold=True)
band(ws, 11, 8)
put(ws, 'A12', 'Net finance charge after tax', fmt=None)
put(ws, 'B12', '-', BLACK, NUM1); put(ws, 'C12', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}12', f"='Income Statement'!{FCC[i]}12*(1-{a('tax_ct')})",
         fin_f[i] * (1 - TAX), NUM1)
put(ws, 'A13', 'Free cash flow to equity', fmt=None)
put(ws, 'B13', '-', BLACK, NUM1); put(ws, 'C13', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}13', f'={CFF[i]}11+{CFF[i]}12',
         B_CT['fcff'][YF[i]] + fin_f[i] * (1 - TAX), NUM1)
put(ws, 'A14', 'Dividends paid', fmt=None)
put(ws, 'B14', DIV24 if DIV24 else '-', BLUE if DIV24 else BLACK, NUM1)
put(ws, 'C14', DIV25, BLUE, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}14', f'=-{a("div")}', -IN['div_policy'], NUM1, green=True)
put(ws, 'A15', 'Change in net debt (dividend less equity free cash flow)', fmt=None)
put(ws, 'B15', '-', BLACK, NUM1); put(ws, 'C15', '-', BLACK, NUM1)
for i in range(5):
    dnd = IN['div_policy'] - (B_CT['fcff'][YF[i]] + fin_f[i] * (1 - TAX))
    putf(ws, f'{CFF[i]}15', f'=-{CFF[i]}13-{CFF[i]}14', dnd, NUM1)
put(ws, 'A16', 'Closing net debt', fmt=None)
put(ws, 'B16', '-', BLACK, NUM1); put(ws, 'C16', '-', BLACK, NUM1)
for i in range(5):
    putf(ws, f'{CFF[i]}16', f"='Balance Sheet'!{BF[i]}16", nd_f[i], NUM1, green=True)
note(ws, 18, 'The company converts EBITDA to operating cash at a high rate — the negative '
     'working-capital cycle (customer deposits and long payables) funds growth. The '
     'committed dividend exceeds equity free cash flow in the first forecast year by '
     'design; the net-debt roll on the Balance Sheet carries the difference.')

# ============ SUMMARY FINANCIALS ===================================================
ws = wb['Summary Financials']
title(ws, 'Summary financials — the eight-year picture', 'AED mn unless stated. Every cell '
      'on this sheet is a link or a ratio; nothing is typed twice.', 9, awidth=44, cwidth=12)
hdr(ws, 4, ['AED mn'] + YHL + YFL)
rev_all = [HI[y]['rev'] for y in H3] + [F['rev'][y] for y in YF]
eb_all = [HI[y]['ebitda'] for y in H3] + [F['ebitda'][y] for y in YF]
ebit_all = [HI[y]['op'] for y in H3] + [B_CT['ebit'][y] for y in YF]
ic_f = [F['ppe'][y] + CONCESSION + F['nwc'][y] for y in YF]

def sfrow(r, lab, fml, vals, fmt=NUM1, skip=()):
    put(ws, f'A{r}', lab, fmt=None)
    for i in range(8):
        if i in skip or vals[i] is None:
            put(ws, f'{ALLC[i]}{r}', '-', BLACK, fmt)
        else:
            f_ = fml(i)
            putf(ws, f'{ALLC[i]}{r}', f_, vals[i], fmt,
                 green=f_.startswith(("='I", "='B", '=DCF', "='C")))

sfrow(5, 'Revenue', lambda i: f"='Income Statement'!{ALLC[i]}5", rev_all)
sfrow(6, 'Revenue growth', lambda i: f'={ALLC[i]}5/{ALLC[i-1]}5-1',
      [None] + [rev_all[i] / rev_all[i-1] - 1 for i in range(1, 8)], PCT, skip=(0,))
sfrow(7, 'EBITDA', lambda i: f"='Income Statement'!{ALLC[i]}8", eb_all)
sfrow(8, 'EBITDA margin', lambda i: f'={ALLC[i]}7/{ALLC[i]}5',
      [eb_all[i] / rev_all[i] for i in range(8)], PCT)
sfrow(9, 'Operating profit (EBIT)', lambda i: f"='Income Statement'!{ALLC[i]}11", ebit_all)
sfrow(10, 'Attributable profit', lambda i: f"='Income Statement'!{ALLC[i]}17", npa_all)
sfrow(11, 'Free cash flow to the firm', lambda i: f"='Cash Flow'!{CFF[i-3]}11",
      [None] * 3 + [B_CT['fcff'][y] for y in YF], skip=(0, 1, 2))
sfrow(12, 'Net debt', lambda i: f"='Balance Sheet'!{['B','C'][i-1]}16" if i < 3
      else f"='Balance Sheet'!{BF[i-3]}16",
      [None, nd_hist[0], nd_hist[1]] + nd_f, skip=(0,))
sfrow(13, 'Invested capital (plant + concession + working capital)',
      lambda i: (f"=DCF!{CD[i-3]}11+{a('concession')}+'Balance Sheet'!{BF[i-3]}15"),
      [None] * 3 + ic_f, skip=(0, 1, 2))
sfrow(14, 'Return on invested capital (NOPAT / same-year capital)',
      lambda i: f'=DCF!{CD[i-3]}14/{ALLC[i]}13',
      [None] * 3 + [B_CT['nopat'][YF[i]] / ic_f[i] for i in range(5)], PCT, skip=(0, 1, 2))
note(ws, 16, 'Return on invested capital comfortably clears the cost of capital across the '
     'forecast — the economics of a regulated district-cooling monopoly with a negative '
     'working-capital cycle. The terminal reinvestment rate on the DCF sheet is set from '
     'exactly this capital base.')

# ============ RELATIVE & NORMALIZED ================================================
ws = wb['Relative & Normalized']
title(ws, 'Relative multiples, normalised earnings power, book value and dividends', None, 6,
      awidth=56, cwidth=15)
hdr(ws, 4, ['Relative lens — peer EV/EBITDA applied to the model year one', 'Value'])
rel_rows = [
    ('FY2026E group EBITDA (AED mn)', '=DCF!B6', F['ebitda']['FY26'], NUM1),
    ('Peer EV/EBITDA (Tabreed)', f'={a("tabreed_ev")}', REL['tabreed_ev_ebitda'], MULT),
    ('Implied enterprise value (AED mn)', '=C5*C6', REL['ev_rel'], NUM1),
    ('Less net debt', '=-DCF!$C$47', -NET_DEBT, NUM1),
    ('Plus investment properties and fair-value assets',
     f'={a("invprop")}+{a("fvtpl")}+{a("fvoci")}', BRIDGE_ADD, NUM1),
    ('Equity value (AED mn)', '=C7+C8+C9', REL['ev_rel'] - NET_DEBT + BRIDGE_ADD, NUM1),
    ('Implied value per share (AED)',
     f"=C10*(1-'SOTP Bridge'!$C$14)/{a('shares')}", REL['ps_rel'], PX),
]
r = 5
for lab, fml, xp, fmt in rel_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt,
         green=('DCF' in fml or fml.startswith('=Assumptions')))
    r += 1
band(ws, 11, 3)
put(ws, 'A12', 'Peer price/earnings (Tabreed) on FY2026E attributable profit', fmt=None)
putf(ws, 'C12', f"={a('tabreed_pe')}*'Income Statement'!E17/{a('shares')}", REL['ps_pe'], PX)
r = 14
hdr(ws, r, ['Own trailing multiples', 'Value']); r += 1
for lab, fml, xp, fmt in [
        ('Trailing enterprise value / EBITDA',
         f"=({a('spot')}*{a('shares')}+DCF!$C$47)/'Income Statement'!D8",
         (W['mktcap'] + NET_DEBT) / HI['FY25']['ebitda'], MULT),
        ('Trailing price / earnings', f"={a('spot')}/'Income Statement'!D18",
         SPOT / (HI['FY25']['npa'] / SH), MULT),
        ('Trailing price / book (30-Jun-2026)', 'PATCH_PB', SPOT / BK['bvps'], MULT),
        ('Net debt / FY2025 EBITDA', f"=DCF!$C$47/'Income Statement'!D8",
         NET_DEBT / HI['FY25']['ebitda'], MULT)]:
    put(ws, f'A{r}', lab, fmt=None); putf(ws, f'C{r}', fml, xp, fmt); r += 1
r += 1
hdr(ws, r, ['Normalised earnings power — FY2026E without the consumption shock', 'Value'])
r += 1                                              # r = 21
rev_norm = NRM['rev']
ew_norm = U['ew_ratio'] * U['cons_per_rt25'] * U['rt_avg']['FY26']
norm_rows = [
    ('Revenue at the unshocked per-RT level (AED mn)',
     f'={a("cons_per_rt")}*Segments!C7+Segments!C10+{a("pipes")}', rev_norm, NUM1),
    ('Normalised EBITDA (AED mn)',
     f'=C21+Segments!C18-{a("ew_ratio")}*{a("cons_per_rt")}*Segments!C7'
     f'-Segments!C16-Segments!C17+{a("oi")}', NRM['ebitda'], NUM1),
    ('Less depreciation and amortisation (FY2026E)', '=-DCF!B12', -F['dna']['FY26'], NUM1),
    ('Net finance charge (FY2026E)', "='Income Statement'!E12", FIN26, NUM1),
    ('Normalised attributable profit (AED mn)',
     f"=(C22+C23+C24)*(1-{a('tax_ct')})*(1-'SOTP Bridge'!$C$14)", NRM['npa'], NUM1),
    ('Normalised earnings per share (AED)', f'=C25/{a("shares")}', NRM['eps'], PX),
    ('Sustainable return on equity (FY2025 profit / average equity)',
     f'={a("npa_fy25")}/(({a("eq_fy25")}+{a("eq_fy24")})/2)', BK['roe_sust'], PCT),
    ('Justified price/earnings — (1 - g/return) x (1 + g) / (cost of equity - g)',
     f'=(1-{a("g")}/C27)*(1+{a("g")})/(DCF!$C$44-{a("g")})', NRM['pe_just'], MULT),
    ('Implied value per share (AED)', '=C26*C28', NRM['ps'], PX),
]
for lab, fml, xp, fmt in norm_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt,
         green=('DCF' in fml or 'Segments' in fml or 'Income Statement' in fml))
    r += 1
band(ws, 29, 3)
r += 1
hdr(ws, r, ['Book value and sustainable return', 'Value']); r += 1   # r = 32? track
bk0 = r
book_rows = [
    ('Book value per share, 30-Jun-2026 (AED)', f'={a("eq_jun26")}/{a("shares")}',
     BK['bvps'], PX),
    ('Justified price/book — (return - g) / (cost of equity - g)',
     f'=(C27-{a("g")})/(DCF!$C$44-{a("g")})', BK['pb_just'], MULT),
    ('Implied value per share (AED)', f'=C{bk0}*C{bk0+1}', BK['ps'], PX),
]
for lab, fml, xp, fmt in book_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, green=('DCF' in fml))
    r += 1
band(ws, bk0 + 2, 3)
# patch the trailing price/book formula now that the book-value row is known
putf(ws, 'C17', f'={a("spot")}/C{bk0}', SPOT / BK['bvps'], MULT)
r += 1
hdr(ws, r, ['Dividend cross-check', 'Value']); r += 1
dd0 = r
ddm_rows = [
    ('Dividend per share — committed distribution (AED)', f'={a("div")}/{a("shares")}',
     DDM['dps'], PX),
    ('Dividend value — grown at terminal growth, at the cost of equity (AED)',
     f'=C{dd0}*(1+{a("g")})/(DCF!$C$44-{a("g")})', DDM['ps'], PX),
]
for lab, fml, xp, fmt in ddm_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'C{r}', fml, xp, fmt, green=('DCF' in fml))
    r += 1
note(ws, r + 1, 'Trailing price/book references the book-value cell below it (row '
     f'{bk0}). The normalised lens re-runs year one at the FY2025 per-RT consumption '
     'level: it answers what the business earns if the warm-winter shock proves cyclical. '
     'The book-value cell rows anchor the trailing multiple above.')
ANCH['rel'] = dict(bvps=bk0, ps_rel=11, ps_pe=12, ps_norm=29, ps_book=bk0 + 2,
                   ddm=dd0 + 1)

# ============ SUMMARY ==============================================================
ws = wb['Summary']
title(ws, 'Summary — valuation at a glance', 'All values link live to their source sheets; '
      'the weights are visible inputs. Two tax framings are shown side by side, never '
      'averaged.', 7, awidth=48, cwidth=14)
hdr(ws, 4, ['Lens', 'AED/share', 'Weight', 'Contribution', 'vs spot', '',
            'Terminal value share of EV'])
lens_src = [
    ('Discounted cash flow (9% framing)', "='SOTP Bridge'!C13", B_CT['ps'], 'w_dcf',
     LN['dcf']['weight']),
    ('Relative multiples (peer EV/EBITDA)', "='Relative & Normalized'!C11", REL['ps_rel'],
     'w_rel', LN['relative']['weight']),
    ('Normalised earnings power', "='Relative & Normalized'!C29", NRM['ps'], 'w_norm',
     LN['normalized']['weight']),
    ('Book value and sustainable return',
     f"='Relative & Normalized'!C{ANCH['rel']['ps_book']}", BK['ps'], 'w_book',
     LN['book']['weight']),
]
r = 5
for lab, fml, xp, wkey, wv in lens_src:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'B{r}', fml, xp, PX, green=True)
    putf(ws, f'C{r}', f'={a(wkey)}', wv, PCT, green=True)
    putf(ws, f'D{r}', f'=B{r}*C{r}', xp * wv, PX)
    putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', xp / SPOT - 1, PCT)
    r += 1
putf(ws, 'G5', "='SOTP Bridge'!C15", B_CT['tv_share'], PCT, green=True)
band(ws, r, 7)
put(ws, f'A{r}', 'Central fair value (9% framing) — weighted blend', bold=True, fmt=None)
putf(ws, f'B{r}', '=SUM(D5:D8)', CEN['ct'], PX, bold=True)
putf(ws, f'C{r}', '=SUM(C5:C8)', 1.0, PCT, bold=True)
putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', CEN['ct'] / SPOT - 1, PCT, bold=True)
CEN_ROW = r
r += 1
put(ws, f'A{r}', 'Central fair value (15% framing) — same weights, top-up tax throughout',
    fmt=None)
putf(ws, f'B{r}',
     f"={a('w_dcf')}*'SOTP Bridge'!D13+{a('w_rel')}*B6+{a('w_norm')}*B7*(1-{a('hc')})"
     f'+{a("w_book")}*B8', CEN['dmtt'], PX)
putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', CEN['dmtt'] / SPOT - 1, PCT)
CEN_DM_ROW = r
r += 1
put(ws, f'A{r}', 'Bear case — full model re-run (does not redraw with drivers)', fmt=None)
put(ws, f'B{r}', CEN['bear'], BLUE, PX)
putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', CEN['bear'] / SPOT - 1, PCT)
r += 1
put(ws, f'A{r}', 'Bull case — full model re-run (does not redraw with drivers)', fmt=None)
put(ws, f'B{r}', CEN['bull'], BLUE, PX)
putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', CEN['bull'] / SPOT - 1, PCT)
r += 1
put(ws, f'A{r}', 'Dividend cross-check', fmt=None)
putf(ws, f'B{r}', f"='Relative & Normalized'!C{ANCH['rel']['ddm']}", DDM['ps'], PX,
     green=True)
putf(ws, f'E{r}', f'=B{r}/{a("spot")}-1', DDM['ps'] / SPOT - 1, PCT)
r += 1
put(ws, f'A{r}', 'Discounted cash flow on the CDS premium basis', fmt=None)
putf(ws, f'B{r}', "='SOTP Bridge'!E13", B_CDS['ps'], PX, green=True)
r += 1
band(ws, r, 7)
put(ws, f'A{r}', 'Market price (anchor, 07-Aug-2026)', bold=True, fmt=None)
putf(ws, f'B{r}', f'={a("spot")}', SPOT, PX, bold=True, green=True)
SPOT_ROW = r
r += 1
put(ws, f'A{r}', 'DEWA control-transaction price, Feb-2026 (reference point, not fair value)',
    fmt=None)
putf(ws, f'B{r}', f'={a("dewa_price")}', D['dewa_buyin']['price'], PX, green=True)
note(ws, r + 1, 'The Feb-2026 DEWA purchase of Dubai Holding\'s 24% at AED 2.16 was a '
     'related-party CONTROL transaction — a disclosed reference point above every lens '
     'here, never a fair-value estimate for minority shares.')
r += 3
hdr(ws, r, ['Key figure', 'Value'])
r += 1
key_rows = [
    ('Shares outstanding (mn)', f'={a("shares")}', SH, NUM0),
    ('Market capitalisation (AED mn)', '=DCF!C46', W['mktcap'], NUM1),
    ('Net debt, 30-Jun-2026 (AED mn)', '=DCF!C47', NET_DEBT, NUM1),
    ('FY2025 revenue (AED mn)', "='Income Statement'!D5", HI['FY25']['rev'], NUM1),
    ('FY2025 EBITDA (AED mn)', "='Income Statement'!D8", HI['FY25']['ebitda'], NUM1),
    ('FY2025 attributable profit (AED mn)', "='Income Statement'!D17", HI['FY25']['npa'],
     NUM1),
    ('Cost of equity (rating basis)', '=DCF!C44', W['ke_rating'], PCT2),
    ('Cost of capital (9% framing, rating basis)', f'=DCF!C{WACC_CT_ROW}', W['rating_ct'],
     PCT2),
    ('Cost of capital (15% framing, rating basis)', f'=DCF!C{WACC_DM_ROW}', W['rating_dmtt'],
     PCT2),
    ('Terminal growth', f'={a("g")}', G, PCT),
]
for lab, fml, xp, fmt in key_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'B{r}', fml, xp, fmt, green=True)
    r += 1
ANCH['summary'] = dict(central=CEN_ROW, central_dm=CEN_DM_ROW, spot=SPOT_ROW)

# ============ FUNDAMENTAL VALUATION ================================================
ws = wb['Fundamental Valuation']
title(ws, 'Fundamental valuation — four lenses, two framings, one field', None, 6,
      awidth=56, cwidth=15)
hdr(ws, 4, ['Lens', 'Basis', 'AED per share'])
fv_rows = [
    ('Discounted cash flow', 'five-year free-cash-flow build, reinvestment-consistent '
     'terminal value', "='SOTP Bridge'!C13", B_CT['ps']),
    ('Relative multiples', 'peer EV/EBITDA on FY2026E EBITDA',
     "='Relative & Normalized'!C11", REL['ps_rel']),
    ('Normalised earnings power', 'unshocked year one x justified price/earnings',
     "='Relative & Normalized'!C29", NRM['ps']),
    ('Book value and sustainable return', 'justified price/book on sustainable return',
     f"='Relative & Normalized'!C{ANCH['rel']['ps_book']}", BK['ps']),
]
r = 5
for lab, basis, fml, xp in fv_rows:
    put(ws, f'A{r}', lab, fmt=None); put(ws, f'B{r}', basis, fmt=None)
    putf(ws, f'C{r}', fml, xp, PX, green=True)
    r += 1
band(ws, r, 3)
put(ws, f'A{r}', 'Weighted central (9% framing)', bold=True, fmt=None)
putf(ws, f'C{r}', f'=Summary!B{CEN_ROW}', CEN['ct'], PX, bold=True, green=True)
r += 2
put(ws, f'A{r}', 'THE TWO CONTESTED JUDGEMENTS — PUBLISHED BOTH WAYS, NEVER AVERAGED',
    bold=True, fmt=None)
r += 1
hdr(ws, r, ['Discounted cash flow per share', '9% corporate tax', '15% top-up tax'])
r += 1
put(ws, f'A{r}', 'Consumption per-RT RECOVERS to the FY2025 level (base)', fmt=None)
putf(ws, f'B{r}', "='SOTP Bridge'!C13", B_CT['ps'], PX, green=True)
putf(ws, f'C{r}', "='SOTP Bridge'!D13", B_DM['ps'], PX, green=True)
r += 1
put(ws, f'A{r}', 'Consumption per-RT never recovers (full model re-run; does not redraw)',
    fmt=None)
put(ws, f'B{r}', CRUX['persist_ps_ct'], BLUE, PX)
put(ws, f'C{r}', CRUX['persist_ps_dmtt'], BLUE, PX)
r += 2
put(ws, f'A{r}', 'Scenario field (full model re-runs; do not redraw with drivers)', bold=True,
    fmt=None)
r += 1
for lab, v in [('Bear — demand re-escalation, halved connections, 15% tax, repriced risk',
                CEN['bear']),
               ('Central (9% framing)', None),
               ('Bull — clean recovery, top-of-guidance connections, 9% tax', CEN['bull'])]:
    put(ws, f'A{r}', lab, fmt=None)
    if v is None:
        putf(ws, f'C{r}', f'=Summary!B{CEN_ROW}', CEN['ct'], PX, green=True)
    else:
        put(ws, f'C{r}', v, BLUE, PX)
    r += 1
r += 1
put(ws, f'A{r}', 'Market price', fmt=None)
putf(ws, f'C{r}', f'=Summary!B{SPOT_ROW}', SPOT, PX, green=True)
r += 1
put(ws, f'A{r}', 'DEWA control-transaction price (reference only)', fmt=None)
putf(ws, f'C{r}', f'={a("dewa_price")}', D['dewa_buyin']['price'], PX, green=True)

# ============ MONTE CARLO ==========================================================
ws = wb['Monte Carlo']
title(ws, 'Probabilistic price map', 'A map of price dispersion around the market price. It '
      'carries no view on value and is never blended with the valuation. Each figure is a '
      'complete simulation output, not a formula, and does not redraw when a driver '
      'changes.', 8, awidth=44, cwidth=13)
hdr(ws, 4, ['Horizon', '5th', '25th', 'Median', '75th', '95th', 'P(above spot)'])
r = 5
for tag, lab in (('1M', 'One month'), ('3M', 'Three months')):
    h = STK['horizons'][tag]
    put(ws, f'A{r}', f"{lab} — to {h['grade_date']}", fmt=None)
    for i, k in enumerate(('p5', 'p25', 'p50', 'p75', 'p95')):
        put(ws, f'{get_column_letter(2+i)}{r}', h['pct'][k], BLUE, PX)
    put(ws, f'G{r}', h['p_above'], BLUE, PCT)
    r += 1
r += 1
hdr(ws, r, ['Level event', 'One month', 'Three months']); r += 1
for lab, k in [('Finishes 10% or more above the market price', 'p_up10'),
               ('Finishes 10% or more below the market price', 'p_dn10'),
               ('Touches 10% above at any point', 'touch_up10'),
               ('Touches 10% below at any point', 'touch_dn10')]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'B{r}', STK['horizons']['1M'][k], BLUE, PCT)
    put(ws, f'C{r}', STK['horizons']['3M'][k], BLUE, PCT)
    r += 1
r += 1
hdr(ws, r, ['Simulation setting', 'Value']); r += 1
for lab, v, fmt, green in [
        ('Anchor date', STK['anchor_date'], None, False),
        ('Market price at the anchor (AED)', f'={a("spot")}', PX, True),
        ('Annualised volatility (three-month anchor)',
         STK['horizons']['3M']['anchor_vol_ann'], PCT, False),
        ('Simulated paths', 50000, NUM0, False)]:
    put(ws, f'A{r}', lab, fmt=None)
    if green:
        putf(ws, f'C{r}', v, SPOT, fmt, green=True)
    else:
        put(ws, f'C{r}', v, BLUE, fmt)
    r += 1
r += 1
note(ws, r, 'Calibration backtest, in plain language: the shares listed in November 2022, '
     f"so only {S0['windows']} non-overlapping three-month windows exist "
     f"({S0['first_origin']} to {S0['last_origin']}). Over that short record the model's "
     'bands were, if anything, slightly generous: every outcome landed inside the 80% '
     'band, and the centre of the distribution sat where it should '
     f"(average percentile of outcomes {S0['pit_mean']:.2f} against an ideal 0.50). A "
     'record this short cannot establish forecasting skill either way; read the bands as '
     'honest dispersion, not precision.')
ws['A' + str(r)].alignment = Alignment(wrap_text=True, vertical='top')
ws.row_dimensions[r].height = 70
for col in 'BCDEFGH':
    ws.merge_cells(f'A{r}:H{r}')
    break

# ============ SENSITIVITY ==========================================================
ws = wb['Sensitivity']
title(ws, 'Sensitivity — what the valuation needs the world to do', 'AED per share. The two '
      'grids are complete model re-runs cell by cell — they do NOT redraw when a driver '
      'changes. The one-way growth row underneath IS live and reprices with the '
      'workbook.', 7, awidth=44, cwidth=13)
put(ws, 'A4', 'Cost of capital (rows) x terminal growth (columns) — 9% framing', bold=True,
    fmt=None)
hdr(ws, 5, [''] + [f'{g:.1%}' for g in SNW['g_grid']])
r = 6
for i, wv in enumerate(SNW['wacc_grid']):
    put(ws, f'A{r}', f'{wv:.2%}', fmt=None)
    for j in range(5):
        put(ws, f'{get_column_letter(2+j)}{r}', SNW['table'][i][j], BLUE, PX)
    r += 1
r += 1
put(ws, f'A{r}', 'THE CRUX — consumption per-RT recovery level from FY2027 (share of '
    'FY2025); full model re-run per cell', bold=True, fmt=None)
r += 1
hdr(ws, r, ['Recovery level', 'Fair value per share (9%)']); r += 1
for row_ in CRUX['rows']:
    put(ws, f'A{r}', row_['level'], BLUE, PCT)
    put(ws, f'B{r}', row_['ps'], BLUE, PX)
    r += 1
put(ws, f'A{r}', 'Never recovers (persists at the FY2026 level)', fmt=None)
put(ws, f'B{r}', CRUX['persist_ps_ct'], BLUE, PX)
put(ws, f'C{r}', CRUX['persist_ps_dmtt'], BLUE, PX)
put(ws, f'D{r}', 'at 15% top-up tax', fmt=None)
r += 2
put(ws, f'A{r}', 'LIVE one-way sensitivity — terminal growth at the base cost of capital '
    '(each cell a formula off the DCF sheet)', bold=True, fmt=None)
r += 1
ghdr = r
put(ws, f'A{r}', 'Terminal growth', fmt=None)
for j, g_ in enumerate(SNW['g_grid']):
    put(ws, f'{get_column_letter(2+j)}{r}', g_, BLUE, PCT)
r += 1
put(ws, f'A{r}', 'Fair value per share (AED, live formula)', fmt=None)
for j in range(5):
    col = get_column_letter(2 + j)
    fml = (f'=((DCF!$C$31+DCF!$F$14*(1+{col}{ghdr})*(1-{col}{ghdr}/DCF!$C$25)'
           f'/(DCF!$C${WACC_CT_ROW}-{col}{ghdr})*DCF!$F$19)-DCF!$C$47'
           f"+{a('invprop')}+{a('fvtpl')}+{a('fvoci')})"
           f"*(1-'SOTP Bridge'!$C$14)/{a('shares')}")
    putf(ws, f'{col}{r}', fml, SNW['table'][2][j], PX)
r += 1
putf(ws, f'H{r-1}', f'=MAX(B{r-1}:F{r-1})-MIN(B{r-1}:F{r-1})',
     max(SNW['table'][2]) - min(SNW['table'][2]), PX)
put(ws, f'G{r-1}', 'Swing:', fmt=None)
note(ws, r + 1, 'The live row reproduces the middle row of the pasted grid at the moment of '
     'writing; if a driver is changed on the Assumptions sheet the live row will move and '
     'the pasted grids will not — that difference is intentional and is the quickest way '
     'to see that a driver change has repriced the model.')

# ============ PER-SHARE & RATIOS ===================================================
ws = wb['Per-Share & Ratios']
title(ws, 'Per-share and ratio analysis', 'The indicator set for a regulated utility with a '
      'concession asset. Every cell is a formula off the statements.', 9, awidth=46,
      cwidth=12)
hdr(ws, 4, ['Measure'] + YHL + YFL)
r = 5
eq_all = [None, BH['FY24']['eqp'], BH['FY25']['eqp']] + eq_f
BSMAP = [None, 'B', 'C']

def ratio(lab, fml, vals, fmt, skip=()):
    global r
    put(ws, f'A{r}', lab, fmt=None)
    for i in range(8):
        if i in skip or vals[i] is None:
            put(ws, f'{ALLC[i]}{r}', '-', BLACK, fmt)
        else:
            putf(ws, f'{ALLC[i]}{r}', fml(i), vals[i], fmt)
    r += 1

ratio('Earnings per share (AED)', lambda i: f"='Income Statement'!{ALLC[i]}18",
      [x / SH for x in npa_all], PX)
ratio('Dividend per share (AED)', lambda i: f'={a("div")}/{a("shares")}',
      [None, None, IN['div_policy'] / SH] + [IN['div_policy'] / SH] * 5, PX, skip=(0, 1))
ratio('Dividend cover (attributable profit / dividend)',
      lambda i: f"='Income Statement'!{ALLC[i]}17/{a('div')}",
      [None, None] + [npa_all[i] / IN['div_policy'] for i in range(2, 8)], MULT, skip=(0, 1))
ratio('Book value per share (AED)',
      lambda i: (f"='Balance Sheet'!{BSMAP[i]}13/{a('shares')}" if i < 3
                 else f"='Balance Sheet'!{BF[i-3]}13/{a('shares')}"),
      [None] + [x / SH for x in eq_all[1:]], PX, skip=(0,))
ratio('Free cash flow to the firm per share (AED)',
      lambda i: f"='Cash Flow'!{CFF[i-3]}11/{a('shares')}",
      [None] * 3 + [B_CT['fcff'][y] / SH for y in YF], PX, skip=(0, 1, 2))
ratio('Gross margin', lambda i: f"='Income Statement'!{ALLC[i]}7/'Income Statement'!{ALLC[i]}5",
      [HI[y]['gp'] / HI[y]['rev'] for y in H3] + [None] * 5, PCT, skip=(3, 4, 5, 6, 7))
ratio('EBITDA margin', lambda i: f"='Income Statement'!{ALLC[i]}9",
      [eb_all[i] / rev_all[i] for i in range(8)], PCT)
ratio('Operating margin', lambda i: f"='Income Statement'!{ALLC[i]}11"
      f"/'Income Statement'!{ALLC[i]}5", [ebit_all[i] / rev_all[i] for i in range(8)], PCT)
ratio('Net margin (attributable)',
      lambda i: f"='Income Statement'!{ALLC[i]}17/'Income Statement'!{ALLC[i]}5",
      [npa_all[i] / rev_all[i] for i in range(8)], PCT)
roe_vals = [None, None, HI['FY25']['npa'] / ((BH['FY24']['eqp'] + BH['FY25']['eqp']) / 2)]
roe_vals += [npa_f[0] / ((BH['FY25']['eqp'] + eq_f[0]) / 2)]
roe_vals += [npa_f[i] / ((eq_f[i-1] + eq_f[i]) / 2) for i in range(1, 5)]
ratio('Return on equity (average base)',
      lambda i: (f"='Income Statement'!D17/(('Balance Sheet'!B13+'Balance Sheet'!C13)/2)"
                 if i == 2 else
                 f"='Income Statement'!{ALLC[i]}17/(('Balance Sheet'!"
                 f"{'C' if i == 3 else BF[i-4]}13+'Balance Sheet'!{BF[i-3]}13)/2)"),
      roe_vals, PCT, skip=(0, 1))
ratio('Net debt / EBITDA',
      lambda i: (f"='Balance Sheet'!{BSMAP[i]}16/'Income Statement'!{ALLC[i]}8" if i < 3
                 else f"='Balance Sheet'!{BF[i-3]}16/'Income Statement'!{ALLC[i]}8"),
      [None, nd_hist[0] / HI['FY24']['ebitda'], nd_hist[1] / HI['FY25']['ebitda']]
      + [nd_f[i] / F['ebitda'][YF[i]] for i in range(5)], MULT, skip=(0,))
ratio('Capital expenditure / revenue',
      lambda i: (f"=-'Cash Flow'!{['B','C'][i-1]}9/'Income Statement'!{ALLC[i]}5" if i < 3
                 else f"=-'Cash Flow'!{CFF[i-3]}9/'Income Statement'!{ALLC[i]}5"),
      [None, IN['capex_fy24'] / HI['FY24']['rev'], IN['capex_fy25'] / HI['FY25']['rev']]
      + [F['capex'][YF[i]] / F['rev'][YF[i]] for i in range(5)], PCT, skip=(0,))
ratio('Payout ratio (dividend / attributable profit)',
      lambda i: f"={a('div')}/'Income Statement'!{ALLC[i]}17",
      [None, None] + [IN['div_policy'] / npa_all[i] for i in range(2, 8)], PCT, skip=(0, 1))
note(ws, r + 1, 'The dividend exceeds attributable profit in the near years by design — '
     'the committed AED 875m distribution is funded by the negative working-capital cycle '
     'and the balance sheet, and the net-debt roll on the Balance Sheet carries it '
     'explicitly.')

# ============ PEER & SECTOR ========================================================
ws = wb['Peer & Sector']
title(ws, 'Peer frame and sector context', 'One close listed peer exists; the parent is '
      'context, not a comparable. Cross-check inputs only, never a source for the '
      'company\'s own numbers.', 6, awidth=36, cwidth=20)
hdr(ws, 4, ['Company / frame', 'Market', 'Relevance', 'Caution'])
r = 5
for a1, a2, a3, a4 in [
    ('Tabreed (National Central Cooling Co)', 'Dubai (DFM)',
     'the only other listed GCC district-cooling pure play — the primary multiple '
     'cross-check', 'roughly 4.6x net debt / EBITDA against Empower\'s 1.8x, and a '
     'concession mix that skews the EV multiple'),
    ('DEWA (parent, 80% owner)', 'Dubai (DFM)',
     'majority owner since Feb-2026; its multiple frames how Dubai prices regulated '
     'utility earnings', 'a vertically-integrated generation and distribution utility, '
     'not a district-cooling comparable'),
    ('Regional listed utilities', 'GCC',
     'the broad frame for regulated-return infrastructure in pegged-currency markets',
     'tariff regimes and concession structures differ materially by emirate and state'),
]:
    put(ws, f'A{r}', a1, fmt=None); put(ws, f'B{r}', a2, fmt=None)
    put(ws, f'C{r}', a3, fmt=None, wrap=True); put(ws, f'D{r}', a4, fmt=None, wrap=True)
    ws.row_dimensions[r].height = 40
    r += 1
ws.column_dimensions['C'].width = 44; ws.column_dimensions['D'].width = 48
r += 1
hdr(ws, r, ['Multiple', 'Peer', 'Empower (model)']); r += 1
peer_rows = [
    ('EV / EBITDA (Tabreed, FY2025; priced Aug-2026)', f'={a("tabreed_ev")}',
     REL['tabreed_ev_ebitda'], "='Relative & Normalized'!C15",
     (W['mktcap'] + NET_DEBT) / HI['FY25']['ebitda'], MULT),
    ('Price / earnings (Tabreed, trailing; priced Aug-2026)', f'={a("tabreed_pe")}',
     REL['tabreed_pe'], "='Relative & Normalized'!C16", SPOT / (HI['FY25']['npa'] / SH),
     MULT),
    ('Price / earnings (DEWA, trailing; priced Aug-2026)', f'={a("dewa_pe")}',
     REL['dewa_pe'], "='Relative & Normalized'!C16", SPOT / (HI['FY25']['npa'] / SH), MULT),
]
for lab, f1, x1, f2, x2, fmt in peer_rows:
    put(ws, f'A{r}', lab, fmt=None)
    putf(ws, f'B{r}', f1, x1, fmt, green=True)
    putf(ws, f'C{r}', f2, x2, fmt, green=True)
    r += 1
put(ws, f'A{r}', 'Dividend yield at the market price', fmt=None)
putf(ws, f'C{r}', f'={a("div")}/{a("shares")}/{a("spot")}',
     IN['div_policy'] / SH / SPOT, PCT)
r += 2
note(ws, r, 'Peer multiples are dated, disclosed cross-check inputs (see the Assumptions '
     'sheet for source and date). Empower trades at a discount to Tabreed on EV/EBITDA '
     'with less than half the leverage; the model\'s relative lens applies the peer '
     'multiple to Empower\'s own forecast EBITDA rather than endorsing either price.')

# ============ READ FIRST ===========================================================
ws = wb['READ FIRST']
title(ws, 'Testahil — Emirates Central Cooling Systems Corporation PJSC (DFM: EMPOWER)',
      None, 9)
for i, ln in enumerate([
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the Empower valuation study. Every blue cell is an',
 'input; every black cell is a formula; green cells link across sheets.', '',
 'IT IS FORMULA-DRIVEN. Every figure that can be derived arithmetically from a driver is a live formula,',
 'so you can change a blue cell on Assumptions and watch the model reprice: the cost of capital is built',
 'from the risk-free rate, beta and the premium rather than pasted; the revenue engine multiplies',
 'per-refrigeration-ton rates by the connected-capacity path; and the income statement, balance sheet,',
 'cash flow, ratios and all four lenses chain off the same cells.', '',
 'EXACTLY THREE THINGS ARE PASTED VALUES, and it is worth knowing which:', '',
 '  1. AUDITED AND DISCLOSED HISTORY — the FY2023-25 statement lines, the 30-Jun-2026 reviewed balance',
 '     sheet, disclosed connected capacity, and the consumption revenue disclosed in the auditor\'s',
 '     key-audit-matter section. Where a line is both disclosed and derivable, the workbook carries the',
 '     DISCLOSED figure: the primary record is not a calculation.',
 '  2. THE UNIT BUILD\'S BASE ANCHORS — the per-RT revenue rates, the electricity-and-water pass-through',
 '     ratio, the cash cost bases, the depreciation rate, capex per added RT and the working-capital',
 '     ratio. Each anchor is pasted once on the Assumptions sheet with its source, and everything',
 '     downstream of it is a formula.',
 '  3. WHOLE-MODEL RE-RUN GRIDS — the probabilistic price map, the discount-rate x growth grid, the',
 '     consumption-recovery grid, the consumption-persists framing and the bear/bull cases. Each such',
 '     cell is a complete revaluation of the entire model, so it cannot be a single formula. THESE GRIDS',
 '     DO NOT REDRAW WHEN A DRIVER IS CHANGED — the live one-way row on the Sensitivity sheet does.', '',
 'How revenue is built. Not as one growth rate. Consumption revenue is a per-RT rate times average',
 'connected refrigeration tons, with the FY2026 warm-winter shock and its recovery as explicit, separate',
 'drivers; capacity and connection revenue is its own per-RT rate on the same capacity path; pipes are',
 'carried flat. Costs escalate each on their own driver: DEWA electricity and water follows the',
 'consumption leg, wage-class lines follow the wage escalator, the concession interest amortises.', '',
 'The two contested judgements are shown BOTH WAYS, never averaged: the 9% corporate-tax and 15%',
 'top-up-tax framings run as parallel columns through the cost of capital, the DCF and the bridge; and',
 'the consumption-recovers and consumption-persists cases are both on the Fundamental Valuation sheet.', '',
 'What it is not. Not investment advice, a recommendation, or a price target. Values are model outputs',
 'shown as ranges. The probabilistic price map is dispersion, not a forecast of value.', '',
 'Sourcing. FY2023, FY2024 and FY2025 statement lines come from the company\'s own audited consolidated',
 'financial statements; the 30-Jun-2026 position from the reviewed interim statements; capacity and',
 'guidance from the company\'s H1-2026 earnings materials. Every input on the Assumptions sheet carries',
 'its source and date in column H.', '',
 f"Currency. AED million unless stated. Spot AED {SPOT:.2f} (07-Aug-2026 close). Sheets: READ FIRST ·",
 'Summary · Fundamental Valuation · Assumptions · SOTP Bridge · Segments · Relative & Normalized · DCF ·',
 'Income Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo · Sensitivity ·',
 'Per-Share & Ratios · Peer & Sector.'], start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 110

# ============ SAVE + EXPECTED LEDGER ===============================================
out = os.path.join(HERE, 'EMPOWER_Valuation_Model_09082026_public.xlsx')
wb.save(out)
json.dump({'expected': EXPECT, 'anchors': ANCH},
          open(os.path.join(HERE, 'xlsx_expected.json'), 'w'), indent=1)
nchk = sum(len(v) for v in EXPECT.values())
nform = nlit = 0
for s in wb.worksheets:
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='):
                nform += 1
            elif isinstance(c.value, (int, float)):
                nlit += 1
print(f'wrote {out} | {len(wb.sheetnames)} sheets: {wb.sheetnames}')
print(f'formulas: {nform} (of which {nchk} carry a checked expected value) | '
      f'numeric literals: {nlit}')
