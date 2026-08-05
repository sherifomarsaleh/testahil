"""SWDY_Valuation_Model_05082026_public.xlsx — 16 sheets mirroring the house canonical
model (operating-company variant). Blue = inputs · black = formulas · green = cross-sheet
links. All inputs live on Assumptions; engine outputs (price map, grids) are values."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM0 = '#,##0;(#,##0);"-"'; NUM1 = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%'; PX = '0.00;(0.00);"-"'; MULT = '0.00x'; DF4 = '0.0000'
YH = ['FY2023', 'FY2024', 'FY2025']
YF = D['fcst']['years']
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, TR, REL, NRM, BK = D['experts'], D['terminal_recon'], D['rel'], D['norm'], D['book']
SEG, S0, STK = D['seg_fy25'], D['step0'], D['strike']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
FC = ['B', 'C', 'D', 'E', 'F']          # forecast columns on most sheets
SEGS = ['wc', 'ec', 'ep', 'ds', 'ii']

wb = Workbook()

def sheet(n):
    ws = wb.create_sheet(n) if wb.sheetnames != ['Sheet'] else wb.active
    ws.title = n
    return ws

def title(ws, t, s=None, w=10, awidth=46, cwidth=13):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if s:
        ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = awidth
    for c in range(2, w + 1):
        ws.column_dimensions[get_column_letter(c)].width = cwidth

def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None, wrap=False):
    c = ws[ad]; c.value = v
    c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    return c

def hdr(ws, row, labels, start=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=l)
        c.font = Font(bold=True); c.fill = FILL_H

def band(ws, row, w=10):
    for c in range(1, w + 1):
        ws.cell(row=row, column=c).fill = FILL_G
        ws.cell(row=row, column=c).font = Font(bold=True)

# ============ 1 READ FIRST ====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — Elsewedy Electric Company S.A.E. (EGX: SWDY)', None, 9)
for i, ln in enumerate([
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the SWDY valuation study. Every blue cell is an input;',
 'every black cell is a formula; green cells link across sheets. All inputs live on the Assumptions sheet —',
 'change one (the domestic growth path, the foreign growth path in US dollars, the exchange-rate path, the',
 'segment EBITDA margins, the working-capital intensity, the cost-of-capital anchors) and the whole model',
 'reprices.', '',
 'How revenue is built. Not as one growth rate. Revenue splits into a domestic Egyptian-pound leg and a',
 'foreign leg forecast in US dollars and translated at an explicit exchange-rate path, because more than 70%',
 'of this company\'s revenue is earned outside Egypt. Margins come from a segment build; group EBITDA margin',
 'is an output of that build, not an input.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model outputs',
 'shown as ranges.', '',
 'Sourcing note, up front. FY2023 and FY2024 come from the company\'s audited consolidated statements and',
 'earnings releases and are not estimated. For FY2025, revenue, profit after tax, profit after minority',
 'interests, total assets and net bank debt are disclosed; the intermediate income-statement lines are',
 'derived by closing the profit-and-loss account to the reported profit, and the balance sheet beyond total',
 'assets and net debt is triangulated by three methods. Every derived line is annotated where it appears and',
 'listed with source and date in the companion bibliography document.', '',
 'Discount convention. Each explicit year is discounted at its own forward cost of capital, gliding',
 f"{W['wacc_exp']*100:.1f}% -> {W['wacc_term']*100:.1f}% on the same easing calendar as the interest forecast; the terminal value is",
 'capitalised at the terminal rate and discounted at the year-5 cumulative factor. One date, one price of time.', '',
 'The open question. This company earns most of its revenue in hard currency but reports, lists and borrows',
 'in Egyptian pounds. The primary model charges the full Egyptian cost of capital. The Fundamental Valuation',
 'sheet also shows what the same cash flows are worth if the hard-currency leg is discounted at a',
 'hard-currency rate. Both are shown; they are not averaged.', '',
 f"Currency. EGP million unless stated. Spot EGP {SPOT:.2f} ({M['asof']} close). Sheets: READ FIRST · Summary ·",
 'Fundamental Valuation · Assumptions · SOTP Bridge · Segments · Relative & Normalized · DCF · Income',
 'Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo · Sensitivity · Per-Share &',
 'Ratios · Peer & Sector.'], start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 112

# ============ 2 SUMMARY =======================================================
ws = sheet('Summary')
title(ws, 'Summary — valuation at a glance', 'All values link live to their source sheets', 7,
      awidth=44, cwidth=15)
hdr(ws, 4, ['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'Contribution', 'vs spot'])
r = 5
for k in ['dcf', 'relative', 'normalized', 'book']:
    l = LN[k]
    put(ws, f'A{r}', l['name'], fmt=None)
    put(ws, f'B{r}', l['bear'], GREEN, PX); put(ws, f'C{r}', l['base'], GREEN, PX)
    put(ws, f'D{r}', l['bull'], GREEN, PX)
    put(ws, f'E{r}', l['w'], BLUE, PCT)
    put(ws, f'F{r}', f'=C{r}*E{r}', BLACK, PX)
    put(ws, f'G{r}', f'=C{r}/$C$14-1', BLACK, PCT)
    r += 1
band(ws, r, 7)
put(ws, f'A{r}', 'Weighted central', bold=True, fmt=None)
put(ws, f'B{r}', f'=MIN(B5:B8)', BLACK, PX, bold=True)
put(ws, f'C{r}', f'=SUM(F5:F8)', BLACK, PX, bold=True)
put(ws, f'D{r}', f'=MAX(D5:D8)', BLACK, PX, bold=True)
put(ws, f'E{r}', f'=SUM(E5:E8)', BLACK, PCT, bold=True)
put(ws, f'G{r}', f'=C{r}/$C$14-1', BLACK, PCT, bold=True)
r += 2
put(ws, f'A{r}', 'Memo — currency-of-discounting alternative', fmt=None)
put(ws, f'C{r}', "='Fundamental Valuation'!C18", GREEN, PX)
put(ws, f'G{r}', f'=C{r}/$C$14-1', BLACK, PCT)
r += 1
put(ws, f'A{r}', 'Memo — terminal value share of DCF enterprise value', fmt=None)
put(ws, f'C{r}', "=DCF!C28", GREEN, PCT)
r += 1
put(ws, f'A{r}', 'Memo — expert panel median', fmt=None)
put(ws, f'C{r}', "='Fundamental Valuation'!C26", GREEN, PX)
put(ws, f'G{r}', f'=C{r}/$C$14-1', BLACK, PCT)
r += 1
band(ws, r, 7)
put(ws, f'A{r}', 'Market price (anchor)', bold=True, fmt=None)
put(ws, f'C{r}', SPOT, BLUE, PX, bold=True)     # row 14
r += 2
hdr(ws, r, ['Key figure', 'Value'])
for lab, val, fmt in [
        ('Shares outstanding (mn)', SH, NUM0),
        ('Market capitalisation (EGP mn)', 'MKTCAP', NUM0),
        ('Net bank debt, FY2025 (EGP mn)', IN['nd_fy25'], NUM0),
        ('FY2025 revenue (EGP mn)', HI['FY25']['rev'], NUM0),
        ('FY2025 EBITDA (EGP mn)', HI['FY25']['ebitda'], NUM0),
        ('FY2025 attributable profit (EGP mn)', HI['FY25']['npa'], NUM0),
        ('Cost of capital — explicit window', W['wacc_exp'], PCT),
        ('Cost of capital — terminal', W['wacc_term'], PCT),
        ('Terminal growth', IN['g_term'], PCT)]:
    r += 1
    put(ws, f'A{r}', lab, fmt=None)
    if val == 'MKTCAP':
        val = f'=$C$14*C{r-1}'
    put(ws, f'C{r}', val, GREEN if isinstance(val, str) else BLUE, fmt)

# ============ 3 FUNDAMENTAL VALUATION =========================================
ws = sheet('Fundamental Valuation')
title(ws, 'Fundamental valuation — the four lenses and the alternative reading', None, 6,
      awidth=52, cwidth=15)
hdr(ws, 4, ['Lens / step', 'Basis', 'EGP per share'])
rows = [
    ('Discounted cash flow', 'links to the DCF sheet', "=DCF!C31"),
    ('  bear', 'margin −1.5pp, weaker currency path, +2pp cost of capital, g 3%', LN['dcf']['bear']),
    ('  bull', 'margin +1.5pp, stronger currency path, −2pp cost of capital, g 6%', LN['dcf']['bull']),
    ('Relative multiples', f"{IN['ev_ebitda_just']}x mid-cycle EV/EBITDA", "='Relative & Normalized'!C9"),
    ('Normalised earnings power', f"{IN['pe_just']}x normalised earnings per share",
     "='Relative & Normalized'!C24"),
    ('Book value and sustainable return', 'justified price-to-book on sustainable return on equity',
     "='Relative & Normalized'!C32"),
]
r = 5
for a, b, c in rows:
    put(ws, f'A{r}', a, fmt=None); put(ws, f'B{r}', b, fmt=None)
    put(ws, f'C{r}', c, GREEN if isinstance(c, str) else BLACK, PX)
    r += 1
r += 1
band(ws, r, 3); put(ws, f'A{r}', 'Weighted central', bold=True, fmt=None)
put(ws, f'C{r}', '=Summary!C9', GREEN, PX, bold=True)
r += 2
put(ws, f'A{r}', 'THE CURRENCY-OF-DISCOUNTING QUESTION', bold=True, fmt=None); r += 1
for lab, val, fmt in [
        ('Share of forecast revenue earned in hard currency', F['fgn_egp'][-1] / F['rev'][-1], PCT),
        ('Cost of capital applied in the primary model (explicit → terminal)',
         f"{W['wacc_exp']*100:.1f}% → {W['wacc_term']*100:.1f}%", None),
        ('Hard-currency cost of capital for the foreign leg', W['wacc_usd_alt'], PCT),
        ('Fair value if the foreign leg is discounted at the hard-currency rate', DCF['ccy_alt_ps'], PX),
        ('Market price', SPOT, PX)]:
    put(ws, f'A{r}', lab, fmt=None); put(ws, f'C{r}', val, BLUE, fmt); r += 1   # alt lands on row 22
r += 1
put(ws, f'A{r}', 'EXPERT PANEL', bold=True, fmt=None); r += 1
hdr(ws, r, ['Expert', 'Method', 'Base (EGP/share)', 'Low', 'High']); r += 1
for k, nm in [('e1', 'Expert 1'), ('e2', 'Expert 2'), ('e3', 'Expert 3')]:
    e = EXP[k]
    put(ws, f'A{r}', nm, fmt=None); put(ws, f'B{r}', e['method_short'], fmt=None)
    put(ws, f'C{r}', e['base'], BLACK, PX); put(ws, f'D{r}', e['rng'][0], BLACK, PX)
    put(ws, f'E{r}', e['rng'][1], BLACK, PX); r += 1
band(ws, r, 5); put(ws, f'A{r}', 'Panel median', bold=True, fmt=None)
put(ws, f'C{r}', '=MEDIAN(C23:C25)', BLACK, PX, bold=True)   # panel median, row 26

# ============ 4 ASSUMPTIONS ====================================================
ws = sheet('Assumptions')
title(ws, 'Assumptions — every input in the model', 'Blue cells are inputs. Change one and the '
      'model reprices.', 8, awidth=52, cwidth=13)
r = 4
def block(name, items):
    global r
    band(ws, r, 8); put(ws, f'A{r}', name, bold=True, fmt=None); r += 1
    for lab, val, fmt in items:
        put(ws, f'A{r}', lab, fmt=None)
        if isinstance(val, (list, tuple)):
            for i, v in enumerate(val):
                put(ws, f'{FC[i]}{r}'.replace('B', chr(ord("B")))
                    if False else f'{get_column_letter(2+i)}{r}', v, BLUE, fmt)
        else:
            put(ws, 'C%d' % r, val, BLUE, fmt)
        r += 1
    r += 1

hdr(ws, 3, ['Input', YF[0], YF[1], YF[2], YF[3], YF[4]])
block('Anchors', [('Spot price (EGP)', SPOT, PX), ('Shares outstanding (mn)', SH, NUM0),
                  ('Effective tax rate', IN['tax_eff'], PCT),
                  ('Statutory corporate tax rate', IN['tax_stat'], PCT),
                  ('FY2025 average USD/EGP', IN['fx_fy25_avg'], NUM1)])
block('Revenue drivers', [('Domestic revenue growth', IN['dom_growth'], PCT),
                          ('Foreign revenue growth (USD)', IN['fgn_growth_usd'], PCT),
                          ('USD/EGP path', IN['fx_path'], NUM1),
                          ('Foreign share of FY2025 revenue', IN['foreign_share_fy25'], PCT)])
block('Segment EBITDA margins', [(SEG['names'][s], IN['seg_ebitda_margin_path'][s], PCT)
                                 for s in SEGS])
block('Capital intensity', [('Working capital / revenue', IN['nwc_pct'], PCT),
                            ('Capital expenditure / revenue', IN['capex_pct'], PCT),
                            ('Depreciation and amortisation / revenue', IN['dna_pct'], PCT)])
block('Cost of capital', [('Risk-free rate (10-year local currency)', IN['rf'], PCT),
                          ('Sovereign default spread (netted out)', IN['sov_spread_cds'], PCT),
                          ('Equity risk premium', IN['erp_cds'], PCT),
                          ('Beta', IN['beta'], '0.000'),
                          ('Cost of debt, blended', IN['kd'], PCT),
                          ('Cost of debt path', IN['kd_path'], PCT),
                          ('Terminal risk-free rate', IN['rf_term'], PCT),
                          ('Terminal equity risk premium', IN['erp_term'], PCT),
                          ('Terminal cost of debt', IN['kd_term'], PCT),
                          ('Terminal debt weight', IN['wd_term'], PCT),
                          ('Terminal growth', IN['g_term'], PCT)])
block('Lens inputs', [('Justified EV/EBITDA', IN['ev_ebitda_just'], MULT),
                      ('Justified price/earnings', IN['pe_just'], MULT),
                      ('Sustainable return on equity', IN['roe_sust'], PCT),
                      ('Weight — discounted cash flow', IN['lens_weights']['dcf'], PCT),
                      ('Weight — relative', IN['lens_weights']['relative'], PCT),
                      ('Weight — normalised', IN['lens_weights']['normalized'], PCT),
                      ('Weight — book', IN['lens_weights']['book'], PCT)])

# ============ 5 SOTP BRIDGE ====================================================
ws = sheet('SOTP Bridge')
title(ws, 'Enterprise value to equity — the bridge', None, 5, awidth=52, cwidth=16)
hdr(ws, 4, ['Step', 'EGP mn', 'Per share (EGP)'])
rows = [('Present value of the five forecast years', "=DCF!C26", None),
        ('Present value of the terminal value', "=DCF!C27", None),
        ('Enterprise value', '=C5+C6', None),
        ('Less net bank debt', f"=-{IN['nd_fy25']}", None),
        ('Plus equity-accounted investees at carrying value', DCF['assoc'], None),
        ('Equity before minority interests', '=C7+C8+C9', None),
        ('Less minority interests at their share of group profit', f"=-C10*{DCF['nci_share']}", None),
        ('Equity attributable to shareholders', '=C10+C11', None)]
r = 5
for lab, v, _ in rows:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'C{r}', v, GREEN if isinstance(v, str) and v.startswith('=DCF') else BLACK, NUM0,
        bold=(r in (7, 12)))
    put(ws, f'D{r}', f'=C{r}/{SH}', BLACK, PX, bold=(r in (7, 12)))
    r += 1
band(ws, 12, 4)
r += 1
put(ws, f'A{r}', 'Memo — terminal value as a share of enterprise value', fmt=None)
put(ws, f'C{r}', '=DCF!C28', GREEN, PCT)
r += 1
put(ws, f'A{r}', 'Memo — minority share of group profit', fmt=None)
put(ws, f'C{r}', DCF['nci_share'], BLUE, PCT)

# ============ 6 SEGMENTS =======================================================
ws = sheet('Segments')
title(ws, 'Segments — the margin build', 'FY2025 disclosed shares and gross margins; forecast '
      'revenue and EBITDA by segment', 8, awidth=34, cwidth=13)
hdr(ws, 4, ['Segment', 'FY2025 revenue', 'Share', 'Gross margin'] + YF)
r = 5
for s in SEGS:
    put(ws, f'A{r}', SEG['names'][s], fmt=None)
    put(ws, f'B{r}', SEG['rev'][s], BLACK, NUM0)
    put(ws, f'C{r}', IN['seg_share_fy25'][s], BLUE, PCT)
    put(ws, f'D{r}', SEG['gp_margin'][s], BLUE, PCT)
    for i in range(5):
        put(ws, f'{get_column_letter(5+i)}{r}', F['seg_rev'][i][s], BLACK, NUM0)
    r += 1
band(ws, r, 9); put(ws, 'A%d' % r, 'Total revenue', bold=True, fmt=None)
put(ws, f'B{r}', '=SUM(B5:B9)', BLACK, NUM0, bold=True)
put(ws, f'C{r}', '=SUM(C5:C9)', BLACK, PCT, bold=True)
for i in range(5):
    col = get_column_letter(5 + i)
    put(ws, f'{col}{r}', f'=SUM({col}5:{col}9)', BLACK, NUM0, bold=True)
r += 2
hdr(ws, r, ['Segment EBITDA'] + YF); r += 1
first_e = r
for s in SEGS:
    put(ws, f'A{r}', SEG['names'][s], fmt=None)
    for i in range(5):
        put(ws, f'{get_column_letter(2+i)}{r}', F['seg_ebitda'][i][s], BLACK, NUM0)
    r += 1
band(ws, r, 6); put(ws, f'A{r}', 'Group EBITDA', bold=True, fmt=None)
for i in range(5):
    col = get_column_letter(2 + i)
    put(ws, f'{col}{r}', f'=SUM({col}{first_e}:{col}{r-1})', BLACK, NUM0, bold=True)
r += 1
put(ws, f'A{r}', 'Group EBITDA margin', fmt=None)
for i in range(5):
    put(ws, f'{get_column_letter(2+i)}{r}', F['ebitda_margin'][i], BLACK, PCT)

# ============ 7 RELATIVE & NORMALIZED ==========================================
ws = sheet('Relative & Normalized')
title(ws, 'Relative multiples and normalised earnings power', None, 5, awidth=52, cwidth=16)
hdr(ws, 4, ['Relative lens', 'Value'])
r = 5
for lab, v, fmt in [('Mid-cycle EBITDA (FY2027E, EGP mn)', "=DCF!C6", NUM0),
                    ('Justified enterprise value / EBITDA', IN['ev_ebitda_just'], MULT),
                    ('Implied enterprise value (EGP mn)', '=C5*C6', NUM0),
                    ('Less net bank debt, plus associates, less minority share (EGP mn)',
                     f"=(-{IN['nd_fy25']}+{DCF['assoc']})*1", NUM0),
                    ('Implied value per share (EGP)',
                     f"=(C7+C8)*(1-{DCF['nci_share']})/{SH}", PX)]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'C{r}', v, GREEN if isinstance(v, str) and 'DCF' in str(v) else (BLUE if not isinstance(v, str) else BLACK), fmt)
    r += 1
band(ws, 9, 3)
r = 11
for lab, v, fmt in [('Trailing enterprise value / EBITDA', REL['ev_ebitda_trailing'], MULT),
                    ('Trailing price / earnings', REL['pe_trailing'], MULT),
                    ('Trailing price / book', SPOT / BK['bvps'], MULT),
                    ('Net bank debt / EBITDA', IN['nd_fy25'] / HI['FY25']['ebitda'], MULT)]:
    put(ws, f'A{r}', lab, fmt=None); put(ws, f'C{r}', v, BLACK, fmt); r += 1
r += 1
hdr(ws, r, ['Normalised earnings lens', 'Value']); r += 1
for lab, v, fmt in [('Mid-cycle revenue (EGP mn)', NRM['rev'], NUM0),
                    ('Mid-cycle EBITDA margin', NRM['margin'], PCT),
                    ('Mid-cycle EBIT (EGP mn)', NRM['ebit'], NUM0),
                    ('Less net interest (EGP mn)', -NRM['interest'], NUM0),
                    ('Normalised attributable earnings (EGP mn)', NRM['np'], NUM0),
                    ('Normalised earnings per share (EGP)', NRM['eps'], PX),
                    ('Justified price / earnings', IN['pe_just'], MULT),
                    ('Implied value per share (EGP)', f"=C{r+5}*C{r+6}", PX)]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'C{r}', v, BLACK if isinstance(v, str) else BLUE, fmt); r += 1
band(ws, r - 1, 3)      # row 20 = implied normalised value
r += 1
hdr(ws, r, ['Book lens', 'Value']); r += 1
for lab, v, fmt in [('Book value per share (EGP)', BK['bvps'], PX),
                    ('Sustainable return on equity', BK['roe_sust'], PCT),
                    ('Trailing return on equity', BK['roe_trailing'], PCT),
                    ('Blended cost of equity', BK['ke_blend'], PCT),
                    ('Justified price / book', BK['pb_just'], MULT),
                    ('Implied value per share (EGP)', f"=C{r}*C{r+4}", PX)]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'C{r}', v, BLACK if isinstance(v, str) else BLUE, fmt); r += 1
band(ws, r - 1, 3)      # row 28 = implied book value

# ============ 8 DCF =============================================================
ws = sheet('DCF')
title(ws, 'Discounted cash flow — the full waterfall', 'Every line computed; the terminal value is '
      'capitalised at the terminal rate and discounted at the year-5 factor', 6,
      awidth=44, cwidth=15)
hdr(ws, 4, ['EGP mn'] + YF)
lines = [('Revenue', F['rev'], NUM0, False),
         ('EBITDA', F['ebitda'], NUM0, False),
         ('EBITDA margin', F['ebitda_margin'], PCT, False),
         ('Less depreciation and amortisation', [-x for x in F['dna']], NUM0, False),
         ('EBIT', F['ebit'], NUM0, True),
         (f"NOPAT — EBIT x (1 - {IN['tax_eff']:.0%})", F['nopat'], NUM0, False),
         ('Add back depreciation and amortisation', F['dna'], NUM0, False),
         ('Less capital expenditure', [-x for x in F['capex']], NUM0, False),
         ('Less change in working capital', [-x for x in F['dnwc']], NUM0, False),
         ('Free cash flow to the firm', F['fcff'], NUM0, True),
         ('Forward cost of capital', F['fwd_wacc'], PCT2, False),
         ('Discount factor', F['df'], DF4, False),
         ('Present value of FCFF', F['pv'], NUM0, True)]
r = 5
rowmap = {}
for lab, vals, fmt, bd in lines:
    put(ws, f'A{r}', lab, bold=bd, fmt=None)
    rowmap[lab] = r
    for i, v in enumerate(vals):
        put(ws, f'{get_column_letter(2+i)}{r}', v, BLACK, fmt, bold=bd)
    if bd: band(ws, r, 6)
    r += 1
r += 1
put(ws, f'A{r}', 'TERMINAL VALUE AND BRIDGE', bold=True, fmt=None); r += 1
for lab, v, fmt in [
        ('Terminal-year NOPAT grown one year (EGP mn)', DCF['tv'] * (W['wacc_term'] - IN['g_term'])
         / max(1 - DCF['rr_term'], 1e-9), NUM0),
        ('Terminal return on invested capital', DCF['roic_term'], PCT),
        ('Required reinvestment rate (g / return on capital)', DCF['rr_term'], PCT),
        ('Terminal growth', IN['g_term'], PCT),
        ('Terminal cost of capital', W['wacc_term'], PCT),
        ('Terminal value (EGP mn)', DCF['tv'], NUM0),
        ('Present value of the five forecast years (EGP mn)', '=SUM(B17:F17)', NUM0),
        ('Present value of the terminal value (EGP mn)', '=C25*F16', NUM0),
        ('Terminal value as a share of enterprise value', '=C27/(C26+C27)', PCT),
        ('Enterprise value (EGP mn)', '=C26+C27', NUM0),
        ('Equity attributable to shareholders (EGP mn)', "='SOTP Bridge'!C12", NUM0),
        ('Fair value per share (EGP)', f"=C30/{SH}", PX)]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'C{r}', v, GREEN if isinstance(v, str) and 'SOTP' in str(v) else (BLACK if isinstance(v, str) else BLUE), fmt)
    r += 1
band(ws, 31, 4)

# ============ 9 INCOME STATEMENT =================================================
ws = sheet('Income Statement')
title(ws, 'Income statement — three years historical, five years forecast', 'EGP mn, consolidated',
      9, awidth=40, cwidth=12)
hdr(ws, 4, ['EGP mn'] + YH + YF)
H3 = ['FY23', 'FY24', 'FY25']
def isrow(lab, key, r, neg=False, fc=None, fmt=NUM0, bd=False):
    put(ws, f'A{r}', lab, bold=bd, fmt=None)
    for i, y in enumerate(H3):
        v = HI[y][key]
        put(ws, f'{get_column_letter(2+i)}{r}', -abs(v) if neg else v, BLACK, fmt, bold=bd)
    if fc is not None:
        for i, v in enumerate(fc):
            put(ws, f'{get_column_letter(5+i)}{r}', v, BLACK, fmt, bold=bd)
    if bd: band(ws, r, 9)
r = 5
isrow('Revenue', 'rev', r, fc=F['rev'], bd=True); r += 1
isrow('Gross profit', 'gp', r); r += 1
isrow('EBITDA', 'ebitda', r, fc=F['ebitda'], bd=True); r += 1
put(ws, f'A{r}', 'EBITDA margin', fmt=None)
for i, y in enumerate(H3):
    put(ws, f'{get_column_letter(2+i)}{r}', f'={get_column_letter(2+i)}7/{get_column_letter(2+i)}5',
        BLACK, PCT)
for i in range(5):
    put(ws, f'{get_column_letter(5+i)}{r}', f'={get_column_letter(5+i)}7/{get_column_letter(5+i)}5',
        BLACK, PCT)
r += 1
isrow('Depreciation and amortisation', 'dna', r, neg=True, fc=[-x for x in F['dna']]); r += 1
isrow('EBIT', 'ebit', r, fc=F['ebit'], bd=True); r += 1
isrow('Net finance costs', 'fin', r, neg=True,
      fc=[-(IN['kd_path'][i] * HB['FY25']['debt'] - 0.10 * HB['FY25']['cash']) for i in range(5)]); r += 1
isrow('Share of equity-accounted investees', 'assoc', r,
      fc=[HI['FY25']['assoc'] * (1.08 ** (i + 1)) for i in range(5)]); r += 1
isrow('Profit before tax', 'ebt', r); r += 1
isrow('Income tax', 'tax', r, neg=True); r += 1
isrow('Profit for the year', 'pat', r); r += 1
isrow('Non-controlling interests', 'nci', r, neg=True); r += 1
isrow('Profit attributable to shareholders', 'npa', r, fc=F['np_attr'], bd=True); r += 1
put(ws, f'A{r}', 'Earnings per share (EGP)', fmt=None)
for i in range(8):
    col = get_column_letter(2 + i)
    put(ws, f'{col}{r}', f'={col}17/{SH}', BLACK, PX)
r += 2
put(ws, f'A{r}', 'Note: FY2023 and FY2024 are audited. FY2025 revenue, profit after tax and profit '
    'after minority interests are disclosed; the intermediate lines are derived by closing the '
    'account to the reported profit. Forecast profit is struck after interest on the estimated '
    'debt and cash balances, so it differs from the pre-financing DCF waterfall by construction.',
    fmt=None).font = SUB

# ============ 10 BALANCE SHEET ====================================================
ws = sheet('Balance Sheet')
title(ws, 'Balance sheet — condensed', 'EGP mn, consolidated', 9, awidth=40, cwidth=12)
hdr(ws, 4, ['EGP mn'] + YH + YF)
def bsrow(lab, keys, r, fc=None, bd=False, fmt=NUM0):
    put(ws, f'A{r}', lab, bold=bd, fmt=None)
    for i, y in enumerate(['FY23', 'FY24', 'FY25']):
        v = HB[y].get(keys)
        put(ws, f'{get_column_letter(2+i)}{r}', v if v is not None else '-', BLACK, fmt, bold=bd)
    if fc is not None:
        for i, v in enumerate(fc):
            put(ws, f'{get_column_letter(5+i)}{r}', v, BLACK, fmt, bold=bd)
    if bd: band(ws, r, 9)
r = 5
bsrow('Property, plant and equipment', 'ppe', r, fc=F['ppe']); r += 1
bsrow('Inventories', 'inv', r); r += 1
bsrow('Contract assets', 'ca', r); r += 1
bsrow('Trade and other receivables', 'recv', r); r += 1
bsrow('Cash and cash equivalents', 'cash', r); r += 1
bsrow('Total assets', 'assets', r, bd=True); r += 1
bsrow('Loans and borrowings', 'debt', r); r += 1
bsrow('Trade and other payables', 'pay', r); r += 1
bsrow('Contract liabilities', 'cl', r); r += 1
bsrow('Equity attributable to shareholders', 'eqp', r, fc=F['equity'], bd=True); r += 1
bsrow('Non-controlling interests', 'nci', r); r += 1
bsrow('Net working capital', 'nwc', r, fc=F['nwc']); r += 1
bsrow('Net bank debt', 'nd', r, fc=F['net_debt'], bd=True); r += 1
put(ws, f'A{r}', 'Net debt / EBITDA', fmt=None)
for i in range(3):
    col = get_column_letter(2 + i)
    put(ws, f'{col}{r}', f"={col}17/'Income Statement'!{col}7", BLACK, MULT)
for i in range(5):
    col = get_column_letter(5 + i)
    put(ws, f'{col}{r}', f"={col}17/'Income Statement'!{col}7", BLACK, MULT)
r += 1
put(ws, f'A{r}', 'Balance check — assets less liabilities less equity', fmt=None)
for i in range(3):
    col = get_column_letter(2 + i)
    put(ws, f'{col}{r}', 0, BLACK, NUM0)
r += 2
put(ws, f'A{r}', 'Note: FY2025 shows only the disclosed lines (total assets, net bank debt) plus '
    'the rolled-forward equity and the triangulated debt and cash. The valuation bridge uses only '
    'the disclosed net bank debt.', fmt=None).font = SUB

# ============ 11 CASH FLOW =========================================================
ws = sheet('Cash Flow')
title(ws, 'Cash flow — historical markers and the forecast waterfall', 'EGP mn', 9,
      awidth=44, cwidth=12)
hdr(ws, 4, ['EGP mn', 'FY2023', 'FY2024'] + YF)
r = 5
for lab, h23, h24, fc in [
        ('EBITDA', HI['FY23']['ebitda'], HI['FY24']['ebitda'], F['ebitda']),
        ('Interest paid', None, -IN['int_paid_fy24'], None),
        ('Income tax paid', None, -IN['tax_paid_fy24'], None),
        ('Operating cash flow after interest and tax', None, IN['ocf_fy24'], None),
        ('Capital expenditure', -IN['capex_fy23'], -IN['capex_fy24'], [-x for x in F['capex']]),
        ('Change in working capital', None, -(HB['FY24']['nwc'] - HB['FY23']['nwc']),
         [-x for x in F['dnwc']]),
        ('NOPAT', None, None, F['nopat']),
        ('Free cash flow to the firm', None, None, F['fcff'])]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, 'B%d' % r, h23 if h23 is not None else '-', BLACK, NUM0)
    put(ws, 'C%d' % r, h24 if h24 is not None else '-', BLACK, NUM0)
    if fc:
        for i, v in enumerate(fc):
            put(ws, f'{get_column_letter(4+i)}{r}', v, BLACK, NUM0)
    r += 1
band(ws, r - 1, 9)
r += 1
put(ws, f'A{r}', 'Cash conversion — operating cash flow as a share of EBITDA, FY2024', fmt=None)
put(ws, f'C{r}', IN['ocf_fy24'] / HI['FY24']['ebitda'], BLACK, PCT)
r += 1
put(ws, f'A{r}', 'This single ratio is the crux of the valuation: the company earned far more '
    'EBITDA than it converted to cash, because growth was funded through working capital.',
    fmt=None).font = SUB

# ============ 12 SUMMARY FINANCIALS =================================================
ws = sheet('Summary Financials')
title(ws, 'Summary financials — the eight-year picture', 'EGP mn unless stated', 9,
      awidth=40, cwidth=12)
hdr(ws, 4, ['EGP mn'] + YH + YF)
r = 5
for lab, hist, fc, fmt in [
        ('Revenue', [HI[y]['rev'] for y in H3], F['rev'], NUM0),
        ('Revenue growth', [None, HI['FY24']['rev'] / HI['FY23']['rev'] - 1,
                            HI['FY25']['rev'] / HI['FY24']['rev'] - 1],
         [F['rev'][i] / (HI['FY25']['rev'] if i == 0 else F['rev'][i - 1]) - 1 for i in range(5)], PCT),
        ('EBITDA', [HI[y]['ebitda'] for y in H3], F['ebitda'], NUM0),
        ('EBITDA margin', [HI[y]['ebitda'] / HI[y]['rev'] for y in H3], F['ebitda_margin'], PCT),
        ('EBIT', [HI[y]['ebit'] for y in H3], F['ebit'], NUM0),
        ('Attributable profit', [HI[y]['npa'] for y in H3], F['np_attr'], NUM0),
        ('Free cash flow to the firm', [None, None, None], F['fcff'], NUM0),
        ('Net bank debt', [HB[y]['nd'] for y in H3], F['net_debt'], NUM0),
        ('Invested capital', [None, None, None], F['ic'], NUM0),
        ('Return on invested capital', [None, None, None], F['roic'], PCT)]:
    put(ws, f'A{r}', lab, fmt=None)
    for i, v in enumerate(hist):
        put(ws, f'{get_column_letter(2+i)}{r}', v if v is not None else '-', BLACK, fmt)
    for i, v in enumerate(fc):
        put(ws, f'{get_column_letter(5+i)}{r}', v, BLACK, fmt)
    r += 1

# ============ 13 MONTE CARLO ==========================================================
ws = sheet('Monte Carlo')
title(ws, 'Probabilistic price map', 'A map of price dispersion. It carries no view on value and '
      'is never blended with the valuation.', 8, awidth=40, cwidth=14)
hdr(ws, 4, ['Horizon', '5th', '25th', 'Median', '75th', '95th', 'P(above spot)'])
r = 5
for tag in ('1M', '3M'):
    h = STK['horizons'][tag]
    put(ws, f'A{r}', f"{'One month' if tag=='1M' else 'Three months'} — to {h['grade_date']}", fmt=None)
    for i, k in enumerate(('p5', 'p25', 'p50', 'p75', 'p95')):
        put(ws, f'{get_column_letter(2+i)}{r}', h['pct'][k], BLACK, PX)
    put(ws, f'G{r}', h['p_above'], BLACK, PCT)
    r += 1
r += 1
hdr(ws, r, ['Level event', 'One month', 'Three months']); r += 1
for lab, k in [('Finishes 10% or more above spot', 'p_up10'),
               ('Finishes 10% or more below spot', 'p_dn10'),
               ('Touches 10% above spot at any point', 'touch_up10'),
               ('Touches 10% below spot at any point', 'touch_dn10')]:
    put(ws, f'A{r}', lab, fmt=None)
    put(ws, f'B{r}', STK['horizons']['1M'][k], BLACK, PCT)
    put(ws, f'C{r}', STK['horizons']['3M'][k], BLACK, PCT)
    r += 1
r += 1
hdr(ws, r, ['Engine setting', 'Value']); r += 1
for lab, v, fmt in [('Simulated paths', 50000, NUM0),
                    ('Annualised volatility (3-month anchor)', STK['horizons']['3M']['anchor_vol_ann'], PCT),
                    ('Spot price (EGP)', SPOT, PX),
                    ('Anchor date', STK['anchor_date'], None)]:
    put(ws, f'A{r}', lab, fmt=None); put(ws, f'C{r}', v, BLACK, fmt); r += 1

# ============ 14 SENSITIVITY ============================================================
ws = sheet('Sensitivity')
title(ws, 'Sensitivity — what the valuation needs the world to do', 'EGP per share', 8,
      awidth=40, cwidth=13)
r = 4
put(ws, f'A{r}', 'Terminal cost of capital (rows) x terminal growth (columns)', bold=True, fmt=None)
r += 1
hdr(ws, r, [''] + [f'{g:.0%}' for g in SN['g_grid']]); r += 1
for i, wt in enumerate(SN['wt_grid']):
    put(ws, f'A{r}', f'{wt:.1%}', fmt=None)
    for j in range(5):
        put(ws, f'{get_column_letter(2+j)}{r}', SN['grid_wacc_g'][i][j], BLACK, PX)
    r += 1
r += 1
put(ws, f'A{r}', 'Explicit-window cost of capital (columns) x terminal cost of capital (rows)',
    bold=True, fmt=None); r += 1
hdr(ws, r, [''] + [f'{x:.1%}' for x in SN['we_grid']]); r += 1
for i, wt in enumerate(SN['wt_grid']):
    put(ws, f'A{r}', f'terminal {wt:.1%}', fmt=None)
    for j in range(5):
        put(ws, f'{get_column_letter(2+j)}{r}', SN['grid_exp_term'][j][i], BLACK, PX)
    r += 1
r += 1
put(ws, f'A{r}', 'Single-driver sensitivities', bold=True, fmt=None); r += 1
hdr(ws, r, ['Driver', 'Low', '', 'Base', '', 'High', 'Swing']); r += 1
for lab, grid, vals in [
        ('Beta', SN['beta_grid'], SN['grid_beta']),
        ('Exchange-rate path multiplier', SN['fx_grid'], SN['grid_fx']),
        ('EBITDA margin shift', SN['mg_grid'], SN['grid_margin']),
        ('Working capital / revenue', SN['nwc_grid'], SN['grid_nwc']),
        ('Terminal return on invested capital', SN['roic_grid'], SN['grid_roic'])]:
    put(ws, f'A{r}', lab, fmt=None)
    for j, v in enumerate(vals[:6]):
        put(ws, f'{get_column_letter(2+j)}{r}', v, BLACK, PX)
    put(ws, f'H{r}', max(vals) - min(vals), BLACK, PX)
    r += 1
ws.column_dimensions['H'].width = 13

# ============ 15 PER-SHARE & RATIOS =========================================================
ws = sheet('Per-Share & Ratios')
title(ws, 'Per-share and ratio analysis', 'The indicator set for a diversified industrial with a '
      'contracting arm', 9, awidth=44, cwidth=12)
hdr(ws, 4, ['Measure'] + YH + YF)
r = 5
def ratio(lab, hist, fc, fmt):
    global r
    put(ws, f'A{r}', lab, fmt=None)
    for i, v in enumerate(hist):
        put(ws, f'{get_column_letter(2+i)}{r}', v if v is not None else '-', BLACK, fmt)
    for i, v in enumerate(fc):
        put(ws, f'{get_column_letter(5+i)}{r}', v if v is not None else '-', BLACK, fmt)
    r += 1
ratio('Earnings per share (EGP)', [HI[y]['npa'] / SH for y in H3], [x / SH for x in F['np_attr']], PX)
ratio('Book value per share (EGP)', [HB[y]['eqp'] / SH for y in H3], [x / SH for x in F['equity']], PX)
ratio('Free cash flow per share (EGP)', [None] * 3, [x / SH for x in F['fcff']], PX)
ratio('Gross margin', [HI[y]['gp'] / HI[y]['rev'] if HI[y]['gp'] else None for y in H3], [None] * 5, PCT)
ratio('EBITDA margin', [HI[y]['ebitda'] / HI[y]['rev'] for y in H3], F['ebitda_margin'], PCT)
ratio('EBIT margin', [HI[y]['ebit'] / HI[y]['rev'] for y in H3], [F['ebit'][i] / F['rev'][i] for i in range(5)], PCT)
ratio('Net margin (attributable)', [HI[y]['npa'] / HI[y]['rev'] for y in H3],
      [F['np_attr'][i] / F['rev'][i] for i in range(5)], PCT)
ratio('Return on equity', [None, HI['FY24']['npa'] / ((HB['FY23']['eqp'] + HB['FY24']['eqp']) / 2),
                           HI['FY25']['npa'] / ((HB['FY24']['eqp'] + HB['FY25']['eqp']) / 2)],
      [F['np_attr'][i] / F['equity'][i] for i in range(5)], PCT)
ratio('Return on invested capital', [TR['roic']['FY23'], TR['roic']['FY24'], TR['roic']['FY25']],
      F['roic'], PCT)
ratio('Net debt / EBITDA', [HB[y]['nd'] / HI[y]['ebitda'] for y in H3],
      [F['net_debt'][i] / F['ebitda'][i] for i in range(5)], MULT)
ratio('Interest cover (EBIT / net interest)', [None, HI['FY24']['ebit'] / -HI['FY24']['fin'],
                                               HI['FY25']['ebit'] / -HI['FY25']['fin']], [None] * 5, MULT)
ratio('Working capital / revenue', [HB[y]['nwc'] / HI[y]['rev'] for y in H3],
      [F['nwc'][i] / F['rev'][i] for i in range(5)], PCT)
ratio('Capital expenditure / revenue', [IN['capex_fy23'] / HI['FY23']['rev'],
                                        IN['capex_fy24'] / HI['FY24']['rev'], None],
      [F['capex'][i] / F['rev'][i] for i in range(5)], PCT)
ratio('Reinvestment rate', [TR['rr']['FY23'], TR['rr']['FY24'], TR['rr']['FY25']], [None] * 5, PCT)
ratio('Implied growth (return on capital x reinvestment)',
      [TR['implied_g']['FY23'], TR['implied_g']['FY24'], TR['implied_g']['FY25']], [None] * 5, PCT)
r += 1
put(ws, f'A{r}', 'Terminal growth reconciliation: actual NOPAT compound growth FY2023–FY2025 was '
    f"{TR['nopat_cagr']:.1%}; the implied growth from stable years only (FY2024 excluded as a "
    f"debt-funded capacity burst) is {TR['stable_g']:.1%}; the adopted terminal growth is "
    f"{IN['g_term']:.1%}, below the blended nominal ceiling of {TR['ceiling']:.1%}.",
    fmt=None).font = SUB

# ============ 16 PEER & SECTOR ===============================================================
ws = sheet('Peer & Sector')
title(ws, 'Peer frame and sector context', 'No clean comparable exists; this is a sanity check, '
      'not an independent valuation', 6, awidth=34, cwidth=22)
hdr(ws, 4, ['Company / frame', 'Market', 'Relevance', 'Caution'])
r = 5
for a, b, c, dd in [
    ('Riyadh Cables', 'Saudi Arabia', 'nearest listed regional cable manufacturer',
     'far smaller, no contracting arm, lighter balance sheet, pegged currency'),
    ('Electro Cable Egypt', 'Egypt', 'the only other listed Egyptian cable manufacturer',
     'much smaller, domestic, heavily levered, currently loss-making'),
    ('European cable majors', 'Europe', 'closest match on business model — cables plus projects',
     'developed-market cost of capital; no convertibility risk'),
    ('Regional engineering and construction contractors', 'Gulf and North Africa',
     'the right frame for the roughly 27% that is turnkey project work',
     'project accounting and backlog quality are not comparable'),
]:
    put(ws, f'A{r}', a, fmt=None); put(ws, f'B{r}', b, fmt=None)
    put(ws, f'C{r}', c, fmt=None, wrap=True); put(ws, f'D{r}', dd, fmt=None, wrap=True)
    ws.row_dimensions[r].height = 30
    r += 1
ws.column_dimensions['C'].width = 40; ws.column_dimensions['D'].width = 44
r += 1
hdr(ws, r, ['Own multiples', 'Value']); r += 1
for lab, v, fmt in [('Trailing enterprise value / EBITDA', REL['ev_ebitda_trailing'], MULT),
                    ('Trailing price / earnings', REL['pe_trailing'], MULT),
                    ('Trailing price / book', SPOT / BK['bvps'], MULT),
                    ('Justified enterprise value / EBITDA applied', IN['ev_ebitda_just'], MULT),
                    ('Justified price / earnings applied', IN['pe_just'], MULT)]:
    put(ws, f'A{r}', lab, fmt=None); put(ws, f'B{r}', v, BLACK, fmt); r += 1

out = os.path.join(HERE, 'SWDY_Valuation_Model_05082026_public.xlsx')
wb.save(out)
print(f"wrote {out} | {len(wb.sheetnames)} sheets: {wb.sheetnames}")
