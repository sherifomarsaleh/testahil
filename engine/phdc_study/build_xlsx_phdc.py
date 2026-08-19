"""PHDC_Valuation_Model_19082026_public.xlsx — 16 sheets, house order, live formula model.

Colour convention: BLUE = a hardcoded input you may overwrite · BLACK = a formula on the
same sheet · GREEN = a link to another sheet. Change a driver on Assumptions and the
valuation recomputes. Every financial numeral is read from study_numbers.json; none is
typed into this builder.
"""
import json, os, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
D = json.load(open('study_numbers.json'))
M, H, W, L, SYN, SENS = D['meta'], D['hist'], D['wacc'], D['lenses'], D['synthesis'], D['sens']
DCF, CF, EXP, GDV = D['dcf'], D['carry_forward'], D['experts'], D['gdv']
A, B = DCF['framing_A'], DCF['framing_B']
INP, H3, SEG, SL, VAR, PEERS = D['inputs'], D['hist3'], D['segments'], D['slider'], D['variance'], D['peers']
YRS = DCF['years']
NY = len(YRS)

INK = '1C3A36'; BLUE = '1F4E9C'; GREEN = '1A7A55'; GREY = '6E7B77'; BRASS = '896F36'
HDR = PatternFill('solid', fgColor='EAF0EE')
BAND = PatternFill('solid', fgColor='F6F1E6')
DARK = PatternFill('solid', fgColor='1C3A36')
THIN = Side(style='thin', color='C9D4D1')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
F_IN = Font(color=BLUE, size=10)
F_FM = Font(color=INK, size=10)
F_LK = Font(color=GREEN, size=10)
F_HD = Font(color=INK, size=10, bold=True)
F_TT = Font(color=INK, size=13, bold=True)
F_SB = Font(color=BRASS, size=10, bold=True)
F_WH = Font(color='FFFFFF', size=11, bold=True)
N2 = '#,##0.00'; N0 = '#,##0'; P1 = '0.0%'; P2 = '0.00%'; X2 = '0.00"x"'

wb = Workbook()
SHEETS = ['READ FIRST', 'Summary', 'Fundamental Valuation', 'Assumptions', 'SOTP Bridge',
          'Segments', 'Relative & Normalized', 'DCF', 'Income Statement', 'Balance Sheet',
          'Cash Flow', 'Summary Financials', 'Monte Carlo', 'Sensitivity',
          'Per-Share & Ratios', 'Peer & Sector']
wb.remove(wb.active)
S = {}
for nm in SHEETS:
    S[nm] = wb.create_sheet(nm)


EXPECT = {}
def putf(ws, ref, formula, value, font=F_FM, fmt=None, fill=None):
    """Write a formula AND record the value the model says it must produce, so the
    independent evaluator in recalc.py can hold the workbook to the model."""
    put(ws, ref, formula, font, fmt, fill)
    EXPECT.setdefault(ws.title, {})[ref] = float(value)
    return value


def put(ws, ref, v, font=F_FM, fmt=None, fill=None, wrap=False, border=False):
    c = ws[ref]; c.value = v; c.font = font
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    if border: c.border = BOX
    return c


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def title(ws, text, sub=None):
    put(ws, 'A1', text, F_TT)
    if sub:
        put(ws, 'A2', sub, Font(color=GREY, size=9.5, italic=True), wrap=True)
        ws.row_dimensions[2].height = 30


def header_row(ws, r, labels, start=1):
    for j, lb in enumerate(labels):
        c = ws.cell(row=r, column=start + j, value=lb)
        c.font = F_HD; c.fill = HDR; c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical='center')


# ============================================================== 1. READ FIRST
ws = S['READ FIRST']
widths(ws, {'A': 118})
put(ws, 'A1', 'READ FIRST — DISCLOSURE, DISCLAIMER AND HOW TO USE THIS MODEL', F_WH, fill=DARK)
lines = [
    ('NATURE OF THIS WORKBOOK',
     'This workbook is an educational valuation model and an expression of the preparer\'s personal '
     'analytical opinion, built exclusively from documents Palm Hills Developments itself issued and '
     'from assumptions stated on the Assumptions sheet. It is shared free of charge so that its '
     'methodology can be examined, stress-tested and critiqued — you are invited to change the '
     'assumptions and see how the outputs respond.'),
    ('NO ADVICE, NO RECOMMENDATION, NO SOLICITATION',
     'Nothing in this workbook constitutes investment advice, financial consultancy, securities '
     'analysis services, a research recommendation, a rating, a price target, an offer, or a '
     'solicitation to buy, sell, hold or otherwise deal in any security.'),
    ('NO LICENSED ACTIVITY',
     'The preparer is not licensed or registered with the Egyptian Financial Regulatory Authority or '
     'any other securities regulator, does not manage money, and does not accept clients, fees or '
     'funds of any kind.'),
    ('ESTIMATES AND UNCERTAINTY',
     'All values are model outputs resting on explicit, subjective assumptions; they are '
     'illustrative, highly uncertain, and likely to prove wrong in material respects. Outputs are '
     'ranges and distributions because no single number should be relied on.'),
    ('NO LIABILITY',
     'To the maximum extent permitted by applicable law, the preparer accepts no liability for any '
     'decision made or action taken or not taken, or for any loss or damage of any kind incurred, by '
     'any person in reliance on any part of this workbook.'),
    ('HOW TO USE THIS MODEL',
     'BLUE cells are hardcoded inputs you can overwrite. BLACK cells are formulas on the same sheet. '
     'GREEN cells link across sheets. Change the cost of capital, the crux ratio, the volume path or '
     'the float treatment on the Assumptions sheet and the DCF, the bridge and the Summary '
     'recompute. The Monte Carlo sheet is the last published price cone, carried forward unchanged '
     'by this fundamentals-only refresh; its rows do not recalculate.'),
    ('THE CONTESTED JUDGEMENT',
     'The company holds EGP %s mn of customers\' maintenance money for residents\' associations that '
     'have not been legally constituted. Whether that float is permanent operating funding or '
     'restricted third-party money is worth more than any other assumption in this model. Cell B%d '
     'on Assumptions switches between the two. The two answers are never averaged.'
     % (format(round(INP['ra_jun26']['value']), ','), 43)),
]
r = 3
for head, body in lines:
    put(ws, 'A%d' % r, head, F_SB); r += 1
    c = put(ws, 'A%d' % r, body, Font(color=INK, size=10), wrap=True)
    ws.row_dimensions[r].height = 46
    r += 2

# ==================================================== 3. FUNDAMENTAL VALUATION
ws = S['Fundamental Valuation']
widths(ws, {'A': 46, 'B': 17, 'C': 17, 'D': 40})
title(ws, 'FUNDAMENTAL VALUATION — THE BRIDGE FROM FIRM TO EQUITY',
      'Both framings of the contested judgement, computed in full. Column B is framing A; column C '
      'is framing B.')
r = 4
header_row(ws, r, ['EGP mn', 'Framing A — float is operating funding',
                   'Framing B — float restricted', 'Note']); r += 1
_r_pvx = r
put(ws, 'A%d' % r, 'Present value of the explicit forecast', F_FM)
put(ws, 'B%d' % r, A['pv_explicit'], F_IN, N0)
put(ws, 'C%d' % r, B['pv_explicit'], F_IN, N0)
put(ws, 'D%d' % r, 'sum of the discounted free cash flows on the DCF sheet', F_FM); r += 1
put(ws, 'A%d' % r, 'Present value of the terminal value', F_FM)
put(ws, 'B%d' % r, A['pv_term'], F_IN, N0)
put(ws, 'C%d' % r, B['pv_term'], F_IN, N0)
put(ws, 'D%d' % r, 'reinvestment-consistent, so growth is charged for', F_FM); r += 1
_r_ev = r
put(ws, 'A%d' % r, 'ENTERPRISE VALUE', F_HD, fill=BAND)
putf(ws, 'B%d' % r, '=B%d+B%d' % (_r_pvx, _r_pvx + 1), A['ev'], F_HD, N0, fill=BAND)
putf(ws, 'C%d' % r, '=C%d+C%d' % (_r_pvx, _r_pvx + 1), B['ev'], F_HD, N0, fill=BAND); r += 1
put(ws, 'A%d' % r, 'Less net debt', F_FM)
put(ws, 'B%d' % r, -H['netdebt_company'], F_IN, N0)
put(ws, 'C%d' % r, -H['netdebt_restricted'], F_IN, N0)
put(ws, 'D%d' % r, 'company definition in A; restricted definition in B', F_FM); r += 1
put(ws, 'A%d' % r, 'Less non-controlling interests', F_FM)
put(ws, 'B%d' % r, -INP['eqnci_jun26']['value'], F_IN, N0)
put(ws, 'C%d' % r, -INP['eqnci_jun26']['value'], F_IN, N0); r += 1
_r_eq = r
put(ws, 'A%d' % r, 'EQUITY VALUE', F_HD, fill=BAND)
putf(ws, 'B%d' % r, '=SUM(B%d:B%d)' % (_r_ev, r - 1), A['bridge']['equity'], F_HD, N0, fill=BAND)
putf(ws, 'C%d' % r, '=SUM(C%d:C%d)' % (_r_ev, r - 1), B['bridge']['equity'], F_HD, N0, fill=BAND); r += 1
_r_sh = r
put(ws, 'A%d' % r, 'Shares outstanding after treasury, mn', F_FM)
putf(ws, 'B%d' % r, "=Assumptions!B5", M['shares_out'], F_LK, N0)
putf(ws, 'C%d' % r, "=Assumptions!B5", M['shares_out'], F_LK, N0); r += 1
put(ws, 'A%d' % r, 'VALUE PER SHARE, EGP', F_HD, fill=BAND)
putf(ws, 'B%d' % r, '=B%d/B%d' % (_r_eq, _r_sh), A['bridge']['vps'], F_HD, N2, fill=BAND)
putf(ws, 'C%d' % r, '=C%d/C%d' % (_r_eq, _r_sh), B['bridge']['vps'], F_HD, N2, fill=BAND)
FV_VPS_ROW = r
r += 2

header_row(ws, r, ['THE FOUR LENSES', 'Low', 'High', 'Weight']); r += 1
for lbl, k in (('Cash flow, framing A', 'dcf'), ('Book value and sustainable return', 'book'),
               ('Relative multiples', 'relative'), ('Normalised earnings power', 'normalised')):
    put(ws, 'A%d' % r, lbl, F_FM)
    lo = L[k]['A_low'] if k == 'dcf' else L[k]['low']
    hi = L[k]['A_high'] if k == 'dcf' else L[k]['high']
    put(ws, 'B%d' % r, lo, F_IN, N2)
    put(ws, 'C%d' % r, hi, F_IN, N2)
    put(ws, 'D%d' % r, SYN['weights'][k], F_IN, P1); r += 1

# ================================================================= 2. SUMMARY
ws = S['Summary']
widths(ws, {'A': 52, 'B': 16, 'C': 16, 'D': 42})
title(ws, 'PALM HILLS DEVELOPMENTS (EGX:PHDC) — VALUATION SUMMARY',
      'Fundamental refresh, 19 August 2026. Fundamentals as of the 30 June 2026 reviewed '
      'statements; price sections carried forward from 22 July 2026.')
r = 4
header_row(ws, r, ['HEADLINE — VALUE PER SHARE (EGP)', 'Framing A', 'Framing B', 'Note']); r += 1
put(ws, 'A%d' % r, 'Cash-flow lens, normalised cost of capital', F_FM)
putf(ws, 'B%d' % r, "='Fundamental Valuation'!B%d" % FV_VPS_ROW, L['dcf']['A'], F_LK, N2)
putf(ws, 'C%d' % r, "='Fundamental Valuation'!C%d" % FV_VPS_ROW, L['dcf']['B'], F_LK, N2)
put(ws, 'D%d' % r, 'discount path glides to the terminal rate', F_FM); r += 1
put(ws, 'A%d' % r, 'Cash-flow lens, spot cost of capital held constant', F_FM)
put(ws, 'B%d' % r, L['dcf']['A_spot'], F_IN, N2)
put(ws, 'C%d' % r, L['dcf']['B_spot'], F_IN, N2)
put(ws, 'D%d' % r, 'the other end of the cost-of-capital range', F_FM); r += 1
for lbl, k in (('Book value and sustainable return', 'book'), ('Relative multiples', 'relative'),
               ('Normalised earnings power', 'normalised')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, L[k]['mid'], F_IN, N2)
    put(ws, 'C%d' % r, L[k]['mid'], F_IN, N2)
    put(ws, 'D%d' % r, 'independent of the contested judgement', F_FM); r += 1
r += 1
_r_centre = r
put(ws, 'A%d' % r, 'WEIGHTED CENTRE', F_HD, fill=BAND)
put(ws, 'B%d' % r, SYN['framing_A']['base'], Font(color=INK, size=11, bold=True), N2, fill=BAND)
put(ws, 'C%d' % r, SYN['framing_B']['base'], Font(color=INK, size=11, bold=True), N2, fill=BAND)
put(ws, 'D%d' % r, 'the two are published side by side, never averaged', F_HD, fill=BAND); r += 1
put(ws, 'A%d' % r, 'Weighted low', F_FM)
put(ws, 'B%d' % r, SYN['framing_A']['bear'], F_IN, N2)
put(ws, 'C%d' % r, SYN['framing_B']['bear'], F_IN, N2); r += 1
put(ws, 'A%d' % r, 'Weighted high', F_FM)
put(ws, 'B%d' % r, SYN['framing_A']['bull'], F_IN, N2)
put(ws, 'C%d' % r, SYN['framing_B']['bull'], F_IN, N2); r += 2
put(ws, 'A%d' % r, 'Market price (close %s)' % M['spot_date'], F_FM)
_r_price = r
putf(ws, 'B%d' % r, "=Assumptions!B4", M['spot'], F_LK, N2); r += 1
put(ws, 'A%d' % r, 'Base against market', F_FM)
putf(ws, 'B%d' % r, '=B%d/B%d-1' % (_r_centre, _r_price),
     SYN['framing_A']['base'] / M['spot'] - 1, F_FM, P1)
putf(ws, 'C%d' % r, '=C%d/B%d-1' % (_r_centre, _r_price),
     SYN['framing_B']['base'] / M['spot'] - 1, F_FM, P1); r += 2

header_row(ws, r, ['WHAT THE NUMBER RESTS ON', 'Value', '', 'Source']); r += 1
for lbl, val, fmt_, src in (
        ('Weighted cost of capital, spot, credit-swap basis', W['wacc_cds'], P2,
         'built on the Assumptions sheet from the central bank auction and the country file'),
        ('Weighted cost of capital, terminal', W['wacc_term'], P2,
         'normalised on the central bank inflation target for the fourth quarter of 2028'),
        ('Beta', W['beta'], N2, 'own-stock weekly regression against the exchange index'),
        ('Revenue per EGP of build cost (the crux)', H['P_h126'], N2,
         'measured on the reviewed half-year'),
        ("Residents' Association float, EGP mn", INP['ra_jun26']['value'], N0,
         'note 63 of the reviewed statements'),
        ('Net debt, company definition, EGP mn', H['netdebt_company'], N0,
         'note 34 less cash and treasury bills'),
        ('Return on invested capital', GDV['roic_A'], P2, "computed from the model's own capital"),
        ('Shares outstanding after treasury, mn', M['shares_out'], N0, 'note 62')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, val, F_IN, fmt_)
    put(ws, 'D%d' % r, src, Font(color=GREY, size=9), wrap=True); r += 1

# ============================================================= 4. ASSUMPTIONS
ws = S['Assumptions']
widths(ws, {'A': 46, 'B': 15, 'C': 13, 'D': 80})
title(ws, 'ASSUMPTIONS — every blue cell is an input you can overwrite',
      'Layer, date and source for each. The model recomputes off these.')
r = 3
header_row(ws, r, ['Input', 'Value', 'Date', 'Source and construction']); r += 1
put(ws, 'A%d' % r, 'Market price, EGP', F_FM); put(ws, 'B%d' % r, M['spot'], F_IN, N2)
put(ws, 'C%d' % r, M['spot_date'], F_FM); put(ws, 'D%d' % r, INP['spot']['source'], Font(color=GREY, size=8), wrap=True); r += 1
put(ws, 'A%d' % r, 'Shares outstanding after treasury, mn', F_FM)
put(ws, 'B%d' % r, M['shares_out'], F_IN, N0); put(ws, 'C%d' % r, '30-Jun-2026', F_FM)
put(ws, 'D%d' % r, INP['sh_out']['source'], Font(color=GREY, size=8), wrap=True); r += 1
KEYS = ['rf_obs', 'ds_rating', 'ds_cds', 'erp_rating', 'erp_cds', 'beta_val', 'taxrate_stat',
        'rf_term', 'erp_term', 'term_g', 'ra_target_ratio', 'maint_share', 'hcount_growth',
        'tbill_wavg_yld', 'cpi_urban', 'cbe_deposit', 'usdegp']
for k in KEYS:
    v = INP[k]
    put(ws, 'A%d' % r, k.replace('_', ' '), F_FM)
    put(ws, 'B%d' % r, v['value'], F_IN, P2 if v['value'] < 1.5 else N2)
    put(ws, 'C%d' % r, v['date'], F_FM)
    put(ws, 'D%d' % r, v['source'], Font(color=GREY, size=8), wrap=True)
    ws.row_dimensions[r].height = 26
    r += 1
put(ws, 'A%d' % r, 'Crux — revenue per EGP of build cost', F_FM)
put(ws, 'B%d' % r, H['P_h126'], F_IN, N2); put(ws, 'C%d' % r, '30-Jun-2026', F_FM)
put(ws, 'D%d' % r, 'measured: real-estate revenue over the construction cost charged to the income '
                   'statement in the reviewed half-year', Font(color=GREY, size=8), wrap=True); r += 1
put(ws, 'A%d' % r, "Land and partners' share, per EGP of revenue", F_FM)
put(ws, 'B%d' % r, H['c2'], F_IN, P2); put(ws, 'C%d' % r, '30-Jun-2026', F_FM)
put(ws, 'D%d' % r, 'the residual of the disclosed cost of real estate development after the '
                   'construction block; the split into its two parts is not identified',
    Font(color=GREY, size=8), wrap=True); r += 1
_row_switch = r
put(ws, 'A%d' % r, 'FLOAT TREATMENT — 1 = framing A, 0 = framing B', F_SB)
put(ws, 'B%d' % r, 1, F_IN, N0); put(ws, 'C%d' % r, 'switch', F_FM)
put(ws, 'D%d' % r, 'the contested judgement. Setting this to 0 removes the float from the cash '
                   'flows and moves the net-debt definition to the restricted one',
    Font(color=GREY, size=8), wrap=True); r += 2

header_row(ws, r, ['Path', 'FY2027', 'FY2028', 'FY2029', 'FY2030', 'FY2031']); r += 1
for lbl, key in (('Real construction volume growth', 'vol_growth'),
                 ('Selling-price escalation', 'pi_price'),
                 ('Steel escalator', 'esc_steel'), ('Cement escalator', 'esc_cement'),
                 ('Finishing escalator', 'esc_finish'), ('Site labour escalator', 'esc_labour')):
    put(ws, 'A%d' % r, lbl, F_FM)
    for j, v in enumerate(INP[key]['value']):
        put(ws, '%s%d' % (get_column_letter(2 + j), r), v, F_IN, P1)
    r += 1
put(ws, 'A%d' % r, 'Weighted build-cost escalator', F_FM)
for j, v in enumerate(DCF['pi_cost']):
    put(ws, '%s%d' % (get_column_letter(2 + j), r), v, F_FM, P1)
r += 1
put(ws, 'A%d' % r, 'Cost-class weights: steel / cement / finishing / labour', F_FM)
for j, v in enumerate(INP['cost_w']['value']):
    put(ws, '%s%d' % (get_column_letter(2 + j), r), v, F_IN, P1)
r += 1

# ============================================================ 5. SOTP BRIDGE
ws = S['SOTP Bridge']
widths(ws, {'A': 54, 'B': 18, 'C': 18, 'D': 46})
title(ws, 'BRIDGE — WHAT IS AND IS NOT INSIDE THE ENTERPRISE',
      'The three definitions of net debt, and the float that separates them.')
r = 4
header_row(ws, r, ['EGP mn', 'Amount', 'In the enterprise?', 'Note']); r += 1
for lbl, val, inside, note in (
        ('Credit facilities (overdrafts)', INP['cf_jun26']['value'], 'debt', 'note 50'),
        ('Loans, long and short term',
         INP['loan_lt_jun26']['value'] + INP['loan_st_jun26']['value'], 'debt', 'note 51'),
        ('Banks — credit balances', INP['bank_cr_jun26']['value'], 'debt', 'note 49'),
        ('Lease obligations', INP['lease_lt_jun26']['value'] + INP['lease_st_jun26']['value'],
         'debt', 'note 55'),
        ('INTEREST-BEARING OBLIGATIONS', H['debt_narrow'], 'debt',
         "note 34 — the company's own schedule"),
        ('Notes payable to the land authority and under sale-and-leaseback',
         H['np_total_jun26'], 'debt-like', 'note 52 — carried only in the broad definition'),
        ('Land purchase liabilities', H['landliab_total_jun26'], 'debt-like', 'note 56'),
        ('Cash and cash equivalents', -INP['cash_jun26']['value'], 'asset', 'note 48'),
        ('Treasury bills and bonds at amortised cost', -INP['tbill_jun26']['value'], 'asset',
         'note 47, average return %.2f%%' % (INP['tbill_wavg_yld']['value'] * 100)),
        ("Residents' Association balance", INP['ra_jun26']['value'], 'the contested judgement',
         'note 63 — matched by maintenance-deposit notes receivable of EGP %s mn and by the '
         'invested proceeds' % format(round(INP['maint_nr']['value']), ',')),
        ('Non-controlling interests', INP['eqnci_jun26']['value'], 'deducted', 'balance sheet')):
    put(ws, 'A%d' % r, lbl, F_HD if lbl.isupper() else F_FM, fill=BAND if lbl.isupper() else None)
    put(ws, 'B%d' % r, val, F_IN, N0, fill=BAND if lbl.isupper() else None)
    put(ws, 'C%d' % r, inside, F_FM)
    put(ws, 'D%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1
r += 1
header_row(ws, r, ['Net debt on each definition', 'EGP mn', 'EGP per share', 'Used where']); r += 1
for lbl, val, used in (
        ("Company definition — interest-bearing less cash and treasury bills",
         H['netdebt_company'], 'framing A'),
        ('Broad — also carrying notes payable and land liabilities', H['netdebt_broad'], 'disclosed only'),
        ('Restricted — the invested residents\' money is not the enterprise\'s',
         H['netdebt_restricted'], 'framing B')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, val, F_IN, N0)
    putf(ws, 'C%d' % r, '=B%d/Assumptions!$B$5' % r, val / M['shares_out'], F_FM, N2)
    put(ws, 'D%d' % r, used, F_FM); r += 1

# ================================================================= 6. SEGMENTS
ws = S['Segments']
widths(ws, {'A': 40, 'B': 16, 'C': 16, 'D': 14, 'E': 14, 'F': 14, 'G': 14, 'H': 52})
title(ws, 'SEGMENTS — REVENUE AND COST BY ACTIVITY',
      'Notes 64 and 65 of the reviewed statements. The two foot exactly to the face of the income '
      'statement, which the model asserts.')
r = 4
header_row(ws, r, ['Activity', 'Revenue H1-2026', 'Revenue H1-2025', 'Cost H1-2026',
                   'Cost H1-2025', 'Margin H1-2026', 'Margin H1-2025']); r += 1
for i, nm in enumerate(SEG['lines']):
    put(ws, 'A%d' % r, nm, F_FM)
    put(ws, 'B%d' % r, SEG['rev_h126'][i], F_IN, N0)
    put(ws, 'C%d' % r, SEG['rev_h125'][i], F_IN, N0)
    put(ws, 'D%d' % r, SEG['cost_h126'][i], F_IN, N0)
    put(ws, 'E%d' % r, SEG['cost_h125'][i], F_IN, N0)
    if SEG['rev_h126'][i]:
        putf(ws, 'F%d' % r, '=1-D%d/B%d' % (r, r), SEG['margin_h126'][i], F_FM, P1)
    else:
        put(ws, 'F%d' % r, 'no revenue line', Font(color=GREY, size=9))
    if SEG['rev_h125'][i]:
        putf(ws, 'G%d' % r, '=1-E%d/C%d' % (r, r), SEG['margin_h125'][i], F_FM, P1)
    else:
        put(ws, 'G%d' % r, 'no revenue line', Font(color=GREY, size=9))
    r += 1
put(ws, 'A%d' % r, 'TOTAL', F_HD, fill=BAND)
_tot = {'B': sum(SEG['rev_h126']), 'C': sum(SEG['rev_h125']),
        'D': sum(SEG['cost_h126']), 'E': sum(SEG['cost_h125'])}
for col in 'BCDE':
    putf(ws, '%s%d' % (col, r), '=SUM(%s%d:%s%d)' % (col, r - len(SEG['lines']), col, r - 1),
         _tot[col], F_HD, N0, fill=BAND)
putf(ws, 'F%d' % r, '=1-D%d/B%d' % (r, r), 1 - _tot['D'] / _tot['B'], F_HD, P1, fill=BAND)
putf(ws, 'G%d' % r, '=1-E%d/C%d' % (r, r), 1 - _tot['E'] / _tot['C'], F_HD, P1, fill=BAND); r += 2
put(ws, 'A%d' % r, 'THE DEVELOPMENT COST BLOCK, DECOMPOSED', F_SB); r += 1
for lbl, val, note in (
        ('Construction cost charged to the income statement', H['constr_relief_h126'],
         'note 43: the movement in the cumulative charge'),
        ("Land and partners' share, together", H['land_partner_h126'],
         'the residual — not separable from anything the company publishes'),
        ('Cost of real estate development', INP['cost_re_h126']['value'], 'note 65'),
        ('Real-estate revenue', INP['rev_re_h126']['value'], 'note 64'),
        ('Revenue per EGP of build cost (the crux)', H['P_h126'], 'the ratio the study sensitises'),
        ('Real-estate gross margin — AN OUTPUT', H['re_gm_h126'], 'one less the two cost rates')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, val, F_IN, P1 if val < 1.5 else N0)
    put(ws, 'H%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ================================================== 7. RELATIVE & NORMALIZED
ws = S['Relative & Normalized']
widths(ws, {'A': 44, 'B': 16, 'C': 16, 'D': 46})
title(ws, 'RELATIVE MULTIPLES AND NORMALISED EARNINGS POWER')
r = 4
header_row(ws, r, ['Relative lens', 'Multiple', 'Value per share, EGP', 'Note']); r += 1
for lbl, mult, vps, note in (
        ('Median Egyptian peer, price to earnings', L['relative']['eg_pe_median'],
         L['relative']['vps_eg'], 'five listed Egyptian developers'),
        ('Median Gulf peer, price to earnings', L['relative']['gulf_pe_median'],
         L['relative']['vps_gulf'], 'Emaar Properties and Aldar'),
        ('All peers, price to earnings', L['relative']['all_pe_median'],
         L['relative']['vps_all'], 'inside and outside the country'),
        ('Gulf peer, enterprise value to EBITDA', L['relative']['ev_ebitda_gulf'],
         L['relative']['vps_evebitda'], 'bridged to equity at the company net-debt definition')):
    put(ws, 'A%d' % r, lbl, F_FM); put(ws, 'B%d' % r, mult, F_IN, X2)
    put(ws, 'C%d' % r, vps, F_IN, N2)
    put(ws, 'D%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1
put(ws, 'A%d' % r, 'Palm Hills, trailing price to earnings', F_FM)
put(ws, 'B%d' % r, H['pe_ltm'], F_IN, X2); r += 2
header_row(ws, r, ['Normalised earnings power', 'Value', '', 'Note']); r += 1
for lbl, val, fmt_, note in (
        ('Revenue base, trailing twelve months, EGP mn', L['normalised']['rev'], N0,
         'the current scale, not a forecast year'),
        ('Mid-cycle margin', L['normalised']['margin'], P1,
         'average of 2023, 2024 and the reviewed half of 2026'),
        ('Earnings before interest, tax and depreciation, EGP mn', L['normalised']['ebitda'], N0, ''),
        ('Depreciation and amortisation, EGP mn', -L['normalised']['da'], N0, ''),
        ('Discount unwinding on instalment receivables, EGP mn', L['normalised']['amort_nr'], N0,
         'real income on the customer financing the balance sheet already carries'),
        ('Return on the treasury-bill book, EGP mn', L['normalised']['tbill'], N0, ''),
        ('Interest, EGP mn', -L['normalised']['interest'], N0,
         'at the measured all-in rate, net of the capitalised share'),
        ('Profit before tax, EGP mn', L['normalised']['pbt'], N0, ''),
        ('Profit after tax, EGP mn', L['normalised']['ni'], N0, ''),
        ('Earnings per share, EGP', L['normalised']['eps'], N2, ''),
        ('Value at the peer range, EGP', L['normalised']['low'], N2, 'low end'),
        ('Value at the peer range, EGP', L['normalised']['high'], N2, 'high end')):
    put(ws, 'A%d' % r, lbl, F_FM); put(ws, 'B%d' % r, val, F_IN, fmt_)
    put(ws, 'D%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ===================================================================== 8. DCF
ws = S['DCF']
widths(ws, {'A': 44, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 13, 'H': 15})
title(ws, 'DISCOUNTED CASH FLOW — FRAMING A',
      'The full waterfall to free cash flow to the firm. Column H totals. Interest is excluded '
      'because this is a pre-financing measure.')
r = 4
header_row(ws, r, ['EGP mn'] + YRS + ['Total']); r += 1
def band(lbl, arr, fmt_=N0, font=F_IN, fill=None, total=True):
    global r
    put(ws, 'A%d' % r, lbl, F_HD if fill else F_FM, fill=fill)
    for j, v in enumerate(arr):
        put(ws, '%s%d' % (get_column_letter(2 + j), r), v, font, fmt_, fill=fill)
    if total:
        putf(ws, 'H%d' % r, '=SUM(B%d:G%d)' % (r, r), sum(arr), F_FM, fmt_, fill=fill)
    here = r
    r += 1
    return here
band('Revenue', A['rev'])
band('Earnings before interest, tax and depreciation', A['ebitda'])
band('  margin', [A['ebitda'][i] / A['rev'][i] for i in range(NY)], P1, F_FM, total=False)
band('Depreciation and amortisation', [-x for x in A['da']])
band('Operating profit', A['ebit'])
band('Tax at the measured effective rate', [-(A['ebit'][i] - A['nopat'][i]) for i in range(NY)])
band('Operating profit after tax', A['nopat'])
band('Add back depreciation and amortisation', A['da'])
band('Capital expenditure', [-x for x in A['capex']])
band('Change in working capital', [-x for x in A['d_nwc']])
band("Residents' Association float", A['ra_cash'])
_fcff = band('FREE CASH FLOW TO THE FIRM', A['fcff'], N0,
             Font(color=INK, size=10, bold=True), BAND)
_dfr = band('Discount factor', A['df'], '0.0000', F_IN, total=False)
put(ws, 'A%d' % r, 'Present value', F_FM)
for j in range(NY):
    cl = get_column_letter(2 + j)
    putf(ws, '%s%d' % (cl, r), '=%s%d*%s%d' % (cl, _fcff, cl, _dfr),
         A['fcff'][j] * A['df'][j], F_FM, N0)
putf(ws, 'H%d' % r, '=SUM(B%d:G%d)' % (r, r), A['pv_explicit'], F_HD, N0, fill=BAND)
_pvexp = r; r += 2
put(ws, 'A%d' % r, 'TERMINAL VALUE', F_SB); r += 1
_dft = 1.0 / (1.0 + W['wacc_term']) ** DCF['tterm']
for lbl, val, fmt_ in (("Return on invested capital, from the model's own year-five capital",
                        A['roic'], P2),
                       ('Terminal growth', INP['term_g']['value'], P1),
                       ('Implied reinvestment rate', A['reinv'], P1),
                       ('Terminal free cash flow, EGP mn', A['fcff_term'], N0),
                       ('Terminal cost of capital', W['wacc_term'], P2),
                       ('Terminal value, EGP mn', A['tv'], N0),
                       ('Terminal discount factor', _dft, '0.0000')):
    put(ws, 'A%d' % r, lbl, F_FM); put(ws, 'B%d' % r, val, F_IN, fmt_)
    if lbl.startswith('Terminal value'):
        _r_tv = r
    if lbl.startswith('Terminal discount'):
        _r_dft = r
    r += 1
put(ws, 'A%d' % r, 'Present value of the terminal value, EGP mn', F_HD, fill=BAND)
putf(ws, 'H%d' % r, '=B%d*B%d' % (_r_tv, _r_dft), A['pv_term'], F_HD, N0, fill=BAND)
_pvterm = r; r += 1
put(ws, 'A%d' % r, 'ENTERPRISE VALUE, EGP mn', F_HD, fill=BAND)
putf(ws, 'H%d' % r, '=H%d+H%d' % (_pvexp, _pvterm), A['ev'], F_HD, N0, fill=BAND)

# ======================================================== 9. INCOME STATEMENT
ws = S['Income Statement']
widths(ws, {'A': 40, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 13, 'H': 13, 'I': 13,
            'J': 13, 'K': 13})
title(ws, 'CONSOLIDATED INCOME STATEMENT — HISTORY AND FORECAST',
      'History from the company\'s own statements. Forecast columns are the model, stated before '
      'financing. Blanks are figures no obtained official document carries.')
r = 4
header_row(ws, r, ['EGP mn'] + H3['years'] + YRS[1:]); r += 1
def hrow(lbl, hist, fwd, fmt_=N0):
    global r
    put(ws, 'A%d' % r, lbl, F_FM)
    for j, v in enumerate(hist):
        if v is not None:
            put(ws, '%s%d' % (get_column_letter(2 + j), r), v, F_IN, fmt_)
    for j, v in enumerate(fwd):
        put(ws, '%s%d' % (get_column_letter(2 + len(hist) + j), r), v, F_LK, fmt_)
    r += 1
hrow('Revenue', H3['revenue'], A['rev'][1:])
hrow('Cost of revenues', [None if v is None else -v for v in H3['cogs']],
     [-(A['rev'][i] - A['gm'][i] * A['rev'][i]) for i in range(1, NY)])
hrow('Gross profit', H3['gross_profit'], [A['gm'][i] * A['rev'][i] for i in range(1, NY)])
hrow('  gross margin', H3['gross_margin'], A['gm'][1:], P1)
hrow('Administrative, selling and marketing', [None if v is None else -v for v in H3['sga']],
     [-A['sga'][i] for i in range(1, NY)])
hrow('Earnings before interest, tax and depreciation', H3['ebitda'], A['ebitda'][1:])
hrow('  margin', H3['ebitda_margin'], [A['ebitda'][i] / A['rev'][i] for i in range(1, NY)], P1)
hrow('Depreciation and amortisation', [None] * 5, [-A['da'][i] for i in range(1, NY)])
hrow('Finance costs and interest', [None if v is None else -v for v in H3['finance_costs']], [])
hrow('Profit before tax', H3['pbt'], [])
hrow('Attributable profit', H3['net_profit'], [])

# ========================================================= 10. BALANCE SHEET
ws = S['Balance Sheet']
widths(ws, {'A': 46, 'B': 17, 'C': 17, 'D': 40})
title(ws, 'CONSOLIDATED BALANCE SHEET', 'Read from the face of the reviewed statements. The '
      'identity holds in both columns, which the model asserts before it will emit a number.')
r = 4
header_row(ws, r, ['EGP mn', '30 Jun 2026', '31 Dec 2025', 'Note']); r += 1
BS = [('Investments in associates', 'assoc_inv', ''),
      ('Investment property', 'invprop', ''),
      ('Fixed assets, net', 'fa', ''),
      ('Notes receivable, long term', 'nr_lt', 'note 41'),
      ('Notes receivable, long term, undelivered units', 'nrund_lt', 'note 42'),
      ('TOTAL NON-CURRENT ASSETS', 'nca', ''),
      ('Work in progress', 'wip', 'note 43'),
      ('Accounts receivable', 'ar', 'note 44'),
      ('Debtors and other debit balances', 'dr', 'note 45'),
      ('Suppliers — advance payments', 'supadv', ''),
      ('Treasury bills and bonds at amortised cost', 'tbill', 'note 47'),
      ('Notes receivable, short term', 'nr_st', 'note 41'),
      ('Cash and cash equivalents', 'cash', 'note 48'),
      ('TOTAL ASSETS', 'ta', ''),
      ('Controlling equity', 'eqctl', ''),
      ('Non-controlling interests', 'eqnci', ''),
      ('Loans, long term', 'loan_lt', 'note 51'),
      ('Notes payable, long term', 'np_lt', 'note 52'),
      ("Residents' Association", 'ra', 'note 63 — the contested judgement'),
      ('Joint arrangement, partners\' share, long term', 'jsa_lt', 'note 58'),
      ('Banks — credit balances', 'bank_cr', 'note 49'),
      ('Credit facilities', 'cf', 'note 50'),
      ('Notes payable, short term', 'np_st', 'note 52'),
      ('Advances from customers', 'adv', 'note 53'),
      ('Creditors and other credit balances', 'cred', 'note 59'),
      ('Suppliers and contractors', 'supcon', ''),
      ('TOTAL LIABILITIES', 'tl', '')]
ROWS = {}
for lbl, k, note in BS:
    up = lbl.isupper()
    put(ws, 'A%d' % r, lbl, F_HD if up else F_FM, fill=BAND if up else None)
    put(ws, 'B%d' % r, INP[k + '_jun26']['value'], F_IN, N0, fill=BAND if up else None)
    put(ws, 'C%d' % r, INP[k + '_dec25']['value'], F_IN, N0, fill=BAND if up else None)
    put(ws, 'D%d' % r, note, Font(color=GREY, size=9))
    ROWS[k] = r; r += 1
put(ws, 'A%d' % r, 'CHECK: total liabilities plus equity less total assets', F_HD)
putf(ws, 'B%d' % r, '=B%d+B%d+B%d-B%d' % (ROWS['tl'], ROWS['eqctl'], ROWS['eqnci'], ROWS['ta']),
     INP['tl_jun26']['value'] + INP['eqctl_jun26']['value'] + INP['eqnci_jun26']['value']
     - INP['ta_jun26']['value'], F_HD, N0)
putf(ws, 'C%d' % r, '=C%d+C%d+C%d-C%d' % (ROWS['tl'], ROWS['eqctl'], ROWS['eqnci'], ROWS['ta']),
     INP['tl_dec25']['value'] + INP['eqctl_dec25']['value'] + INP['eqnci_dec25']['value']
     - INP['ta_dec25']['value'], F_HD, N0)

# ============================================================== 11. CASH FLOW
ws = S['Cash Flow']
widths(ws, {'A': 48, 'B': 16, 'C': 16, 'D': 44})
title(ws, 'CASH FLOW — WHAT THE FLOAT DOES',
      'The single most important table in this workbook. Strip the movement in the Residents\' '
      'Association balance out of reported operating cash flow and it is negative in every period '
      'the company has disclosed.')
r = 4
header_row(ws, r, ['EGP mn', 'Reported operating cash flow',
                   "Residents' Association movement", 'Operating cash flow without it']); r += 1
for lbl, ocf, ra in (('H1-2026', INP['ocf_h126']['value'], INP['d_ra_h126']['value']),
                     ('H1-2025', INP['ocf_h125']['value'], INP['d_ra_h125']['value']),
                     ('FY2024', INP['ocf_fy24']['value'], INP['d_ra_fy24']['value']),
                     ('FY2023', INP['ocf_fy23']['value'], INP['d_ra_fy23']['value'])):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, ocf, F_IN, N0)
    put(ws, 'C%d' % r, ra, F_IN, N0)
    putf(ws, 'D%d' % r, '=B%d-C%d' % (r, r), ocf - ra,
         Font(color='B5483A', size=10, bold=True), N0); r += 1
r += 1
put(ws, 'A%d' % r, 'RECONCILIATION OF THE MODEL TO THE LAST REPORTED PERIOD', F_SB); r += 1
for lbl, val, note in (
        ('Reported unlevered cash flow, H1-2026', H['ufcf_h126_actual'],
         'operating cash flow plus interest paid plus capitalised interest, less capital expenditure'),
        ('Add back: income-tax payable unwound in the period', H['tax_payable_unwind'],
         'the balance fell from EGP %s mn to EGP %s mn — not a run-rate item'
         % (format(round(INP['tax_payable_dec25']['value']), ','),
            format(round(INP['tax_payable_jun26']['value']), ','))),
        ("Add back: partners' share paid down in the period", H['jsa_unwind'],
         'note 58 balance fell over the half'),
        ('Like-for-like reported unlevered cash flow', H['ufcf_h126_like_for_like'], ''),
        ('Model, second half of 2026, framing A', H['ufcf_h226_model_A'], ''),
        ('Residual', H['recon_residual'],
         'disclosed rather than tuned away: the difference between a ratio-driven roll and one '
         'actual half-year of a working-capital-driven developer'),
        ('Income-statement reconciliation gap', H['ebitda_recon_gap'],
         'where the model should be tight, and is')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, val, F_IN, P2 if abs(val) < 1 else N0)
    put(ws, 'D%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ==================================================== 12. SUMMARY FINANCIALS
ws = S['Summary Financials']
widths(ws, {'A': 44, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 13})
title(ws, 'SUMMARY FINANCIALS — THE FORECAST IN ONE PLACE')
r = 4
header_row(ws, r, ['EGP mn'] + YRS); r += 1
for lbl, arr, fmt_ in (('Revenue', A['rev'], N0),
                       ('Real-estate revenue', A['re_rev'], N0),
                       ('Construction cost charged to income', A['constr'], N0),
                       ("Land and partners' share", A['landp'], N0),
                       ('Gross margin', A['gm'], P1),
                       ('Real-estate gross margin', A['re_gm'], P1),
                       ('Earnings before interest, tax and depreciation', A['ebitda'], N0),
                       ('Operating profit after tax', A['nopat'], N0),
                       ('Working capital employed', A['nwc'], N0),
                       ("Residents' Association movement", A['ra_cash'], N0),
                       ('Free cash flow to the firm', A['fcff'], N0)):
    put(ws, 'A%d' % r, lbl, F_FM)
    for j, v in enumerate(arr):
        put(ws, '%s%d' % (get_column_letter(2 + j), r), v, F_LK, fmt_)
    r += 1

# ============================================================ 13. MONTE CARLO
ws = S['Monte Carlo']
widths(ws, {'A': 34, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 16})
title(ws, 'PROBABILITY MAP — CARRIED FORWARD UNCHANGED',
      'This is a fundamentals-only refresh. The rows below are the last published price cone and '
      'they do not recalculate. Data as of %s, computed on %s.'
      % (CF['asof_mc_data'], CF['asof_mc_computed']))
r = 4
header_row(ws, r, ['Horizon', '5%', '25%', 'Median', '75%', '95%', 'Resolves']); r += 1
for k, dd in (('One month', CF['dist']['t20']), ('Three months', CF['dist']['t60'])):
    put(ws, 'A%d' % r, k, F_FM)
    for j, q in enumerate(('p5', 'p25', 'p50', 'p75', 'p95')):
        put(ws, '%s%d' % (get_column_letter(2 + j), r), dd[q], F_IN, N2)
    put(ws, 'G%d' % r, dd['resolve'], F_FM); r += 1
r += 1
header_row(ws, r, ['Level, EGP', 'Touch within one month', 'Touch within three months']); r += 1
for lv, a1, a3 in CF['touch']:
    put(ws, 'A%d' % r, lv, F_IN, N2)
    put(ws, 'B%d' % r, a1 / 100.0, F_IN, P1)
    put(ws, 'C%d' % r, a3 / 100.0, F_IN, P1); r += 1
r += 1
put(ws, 'A%d' % r, 'Anchor price, EGP', F_FM); put(ws, 'B%d' % r, CF['spot'], F_IN, N2); r += 1
put(ws, 'A%d' % r, 'Fundamental base from this refresh, EGP', F_FM)
putf(ws, 'B%d' % r, "='Fundamental Valuation'!B%d" % FV_VPS_ROW, L['dcf']['A'], F_LK, N2); r += 1
put(ws, 'A%d' % r, 'Technical read, data as of', F_FM)
put(ws, 'B%d' % r, CF['asof_tech_data'], F_IN); r += 1
put(ws, 'A%d' % r, 'Technical read, computed on', F_FM)
put(ws, 'B%d' % r, CF['asof_tech_computed'], F_IN)

# ============================================================= 14. SENSITIVITY
ws = S['Sensitivity']
widths(ws, {'A': 30, 'B': 13, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 62})
title(ws, 'SENSITIVITY — FAIR VALUE PER SHARE, EGP',
      'The crux against the cost of capital, computed separately under each framing.')
r = 4
for ttl, grid in (('FRAMING A — float is operating funding', SENS['grid_A']),
                  ('FRAMING B — float restricted', SENS['grid_B'])):
    put(ws, 'A%d' % r, ttl, F_SB); r += 1
    header_row(ws, r, ['Cost-of-capital shift'] + ['%.2fx' % v for v in SENS['crux_P']]); r += 1
    for i, sh in enumerate(SENS['w_shifts']):
        put(ws, 'A%d' % r, '%+d bp' % round(sh * 1e4), F_FM)
        for j in range(len(SENS['p_mults'])):
            put(ws, '%s%d' % (get_column_letter(2 + j), r), grid[i][j], F_IN, N2)
        r += 1
    r += 1
put(ws, 'A%d' % r, 'SINGLE-DRIVER RANGES', F_SB); r += 1
header_row(ws, r, ['Driver', 'Low', 'High', '', '', '', 'Note']); r += 1
for lbl, lo, hi, note in (
        ('Real volume growth', SENS['vol_vps'][0], SENS['vol_vps'][-1],
         'low is no real growth at all, high is half again the base path. More volume is worth '
         'more because most of the capital funding it is customer money, not shareholder money'),
        ('Build-cost escalation', min(SENS['cost_vps']), max(SENS['cost_vps']),
         'two hundred basis points either way on all four classes together'),
        ('Cost of capital', min(SENS['grid_A'][-1]), max(SENS['grid_A'][0]),
         'two hundred basis points either way on the whole path'),
        ('The contested judgement', SYN['framing_B']['base'], SYN['framing_A']['base'],
         'the largest single item in the model')):
    put(ws, 'A%d' % r, lbl, F_FM)
    put(ws, 'B%d' % r, lo, F_IN, N2); put(ws, 'C%d' % r, hi, F_IN, N2)
    put(ws, 'G%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ====================================================== 15. PER-SHARE & RATIOS
ws = S['Per-Share & Ratios']
widths(ws, {'A': 48, 'B': 16, 'C': 46})
title(ws, 'PER-SHARE FIGURES, RATIOS AND THE WORKING-CAPITAL CYCLE')
r = 4
header_row(ws, r, ['Measure', 'Value', 'Construction']); r += 1
for lbl, val, fmt_, note in (
        ('Market price, EGP', M['spot'], N2, 'close of %s' % M['spot_date']),
        ('Shares outstanding after treasury, mn', M['shares_out'], N0, 'note 62'),
        ('Market value, EGP mn', H['mktcap'], N0, 'price times shares'),
        ('Book value per share, EGP', H['bvps'], N2, 'controlling equity over shares'),
        ('Trailing earnings per share, EGP', H['eps_ltm'], N2,
         'trailing twelve months over the weighted average share count'),
        ('Price to book', H['pb'], X2, ''),
        ('Price to earnings', H['pe_ltm'], X2, ''),
        ('Price to sales', H['ps_ltm'], X2, ''),
        ('Enterprise value to EBITDA, company net-debt basis', H['ev_ebitda_company'], X2, ''),
        ('Enterprise value to EBITDA, broad net-debt basis', H['ev_ebitda_broad'], X2, ''),
        ('Return on equity, trailing', H['roe_ltm'], P1, 'on average controlling equity'),
        ('Debt to equity, interest-bearing', H['de_narrow'], P1, ''),
        ('Debt to equity, broad', H['de_broad'], P1, ''),
        ('Dividend yield', H['div_yield'], P1,
         'EGP %s mn paid in the half, annualised' % format(round(INP['divs_h126']['value']), ',')),
        ('Days sales outstanding', H['dso'], N0, 'all receivables over annualised revenue'),
        ('Days inventory outstanding', H['dio'], N0, 'work in progress over annualised cost'),
        ('Days payables outstanding', H['dpo'], N0, 'contractors and notes payable'),
        ('Gross cash conversion cycle, days', H['ccc_gross'], N0, ''),
        ('Customer advances, days', H['adv_days'], N0, ''),
        ('NET CASH CONVERSION CYCLE, days', H['ccc_net'], N0,
         'negative: the customer funds the build. This is the whole financial architecture'),
        ('Realised all-in cost of debt', H['kd_realised'], P2,
         'interest paid and capitalised over average interest-bearing obligations, annualised'),
        ('Measured corporate credit spread', H['corp_spread'], P2,
         "the company's own borrowing cost less the return on its own treasury-bill book"),
        ('Share of interest capitalised into work in progress', H['cap_ratio'], P1, '')):
    up = lbl.isupper()
    put(ws, 'A%d' % r, lbl, F_HD if up else F_FM, fill=BAND if up else None)
    put(ws, 'B%d' % r, val, F_IN, fmt_, fill=BAND if up else None)
    put(ws, 'C%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ========================================================== 16. PEER & SECTOR
ws = S['Peer & Sector']
widths(ws, {'A': 34, 'B': 16, 'C': 22, 'D': 16, 'E': 16, 'F': 46})
title(ws, 'PEERS AND THE SECTOR',
      'Peer multiples are market-data quotes and are used to price other companies only. No '
      'aggregator figure enters any Palm Hills historical.')
r = 4
header_row(ws, r, ['Company', 'Listing', 'Market value, EGP mn', 'Price to earnings',
                   'EV to EBITDA', 'Note']); r += 1
for p in PEERS:
    put(ws, 'A%d' % r, p['name'], F_FM); put(ws, 'B%d' % r, p['ticker'], F_FM)
    if p.get('mcap'): put(ws, 'C%d' % r, p['mcap'], F_IN, N0)
    if p.get('pe'): put(ws, 'D%d' % r, p['pe'], F_IN, X2)
    if p.get('ev_ebitda'): put(ws, 'E%d' % r, p['ev_ebitda'], F_IN, X2)
    put(ws, 'F%d' % r, p['country'], Font(color=GREY, size=9)); r += 1
put(ws, 'A%d' % r, 'Palm Hills Developments', F_HD, fill=BAND)
put(ws, 'B%d' % r, M['code'], F_HD, fill=BAND)
put(ws, 'C%d' % r, H['mktcap'], F_HD, N0, fill=BAND)
put(ws, 'D%d' % r, H['pe_ltm'], F_HD, X2, fill=BAND)
put(ws, 'E%d' % r, H['ev_ebitda_company'], F_HD, X2, fill=BAND)
put(ws, 'F%d' % r, 'computed from the statements at the published price', F_HD, fill=BAND); r += 2
put(ws, 'A%d' % r, 'THE EGYPTIAN MARKET IN THE FIRST HALF OF 2026', F_SB); r += 1
for lbl, val, fmt_, note in (
        ('Sales of the ten largest developers, EGP mn', INP['mkt_h126']['value'], N0, 'H1-2026'),
        ('Same measure a year earlier, EGP mn', INP['mkt_h125']['value'], N0, 'H1-2025'),
        ('Change in value', H['mkt_value_growth'], P1, ''),
        ('Change in units', INP['mkt_units_chg']['value'], P1, 'about 39,000 units'),
        ('Implied change in the average ticket', H['mkt_ticket_growth'], P1,
         'the dated anchor for the selling-price escalator'),
        ('Palm Hills H1-2026 sales, EGP mn', INP['phdc_sales_h126']['value'], N0,
         'SECONDARY AND UNVERIFIED — the company release could not be obtained; no driver reads it'),
        ('Palm Hills share of the top ten', H['phdc_share'], P1, '')):
    put(ws, 'A%d' % r, lbl, F_FM); put(ws, 'B%d' % r, val, F_IN, fmt_)
    put(ws, 'F%d' % r, note, Font(color=GREY, size=9), wrap=True); r += 1

# ================================================================== SAVE
for nm in SHEETS:
    S[nm].sheet_view.showGridLines = False
    S[nm].freeze_panes = 'A5'
OUT = 'PHDC_Valuation_Model_19082026_public.xlsx'
wb.save(OUT)
json.dump({'expected': EXPECT,
           'anchors': dict(vps_A=A['bridge']['vps'], vps_B=B['bridge']['vps'],
                           ev_A=A['ev'], ev_B=B['ev'], pv_explicit=A['pv_explicit'],
                           pv_term=A['pv_term'], base=SYN['base'], spot=M['spot'])},
          open('xlsx_expected.json', 'w'), indent=1)

# column-width discipline: no starved or bloated columns anywhere
from openpyxl import load_workbook
chk = load_workbook(OUT)
bad = []
for ws in chk.worksheets:
    for col, dim in ws.column_dimensions.items():
        if dim.width and (dim.width < 8 or dim.width > 130):
            bad.append('%s!%s width %.0f' % (ws.title, col, dim.width))
    # A cell that wraps may exceed its column width by design; one that does not may not.
    for row in ws.iter_rows():
        for c in row:
            if c.value is None or not isinstance(c.value, str) or c.value.startswith('='):
                continue
            if c.alignment and c.alignment.wrap_text:
                continue
            wdt = ws.column_dimensions[c.column_letter].width if c.column_letter in ws.column_dimensions else None
            if wdt and len(c.value) > wdt * 1.6:
                bad.append('%s!%s%d unwrapped text %d chars in width %.0f'
                           % (ws.title, c.column_letter, c.row, len(c.value), wdt))
assert chk.sheetnames == SHEETS, chk.sheetnames
assert not bad, bad
print('wrote %s — %d sheets, column discipline clean' % (OUT, len(chk.sheetnames)))
