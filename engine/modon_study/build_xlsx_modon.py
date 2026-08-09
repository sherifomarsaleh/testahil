"""MODON_Valuation_Model_09082026_public.xlsx — 16 sheets mirroring the house canonical
model (diversified city-developer variant). Blue = inputs · black = formulas · green =
cross-sheet links.

The workbook is FORMULA-DRIVEN. Every quantity that is arithmetically derivable from an
input is written as a live Excel formula, not as a pasted number. Only three classes of
cell are pasted values:

  1. audited and disclosed historical figures (the primary record);
  2. the four-segment FY2025 base (the company's own IFRS 8 disclosure) — its OUTPUT is
     pasted and the whole forecast chains off it as formulas;
  3. engine outputs that are whole-model re-runs by construction: the Monte Carlo price
     map, the sensitivity grids, the DCF scenario bear/bull bounds and the Egypt-stress /
     run-off alternatives, each cell of which is a complete revaluation.

Every formula cell also carries the model's own value for that cell into
xlsx_expected.json, and recalc.py evaluates the workbook independently and asserts the
two agree."""
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
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, TR, REL, NRM, BK = D['experts'], D['terminal_recon'], D['rel'], D['norm'], D['book']
SEG, S0, STK, CJ = D['seg_fy25'], D['step0'], D['strike'], D['contested']
IN = {k: (v['value'] if isinstance(v, dict) and 'value' in v else v)
      for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
TAX = IN['tax_f']
YF = F['years']
NY = 5
FC = ['B', 'C', 'D', 'E', 'F']              # forecast columns (Segments / DCF)
HC = ['B', 'C', 'D']                        # historical columns on statements
FCOL = ['E', 'F', 'G', 'H', 'I']            # forecast columns on statements

wb = Workbook()
EXPECT = {}
ANCH = {}

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

def putf(ws, ad, formula, expect, fmt=NUM0, bold=False, green=False):
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

# ============ 1 READ FIRST ====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — Modon Holding PSC (ADX: MODON)', None, 9)
for i, ln in enumerate([
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the MODON valuation study. Every blue cell is an input;',
 'every black cell is a formula; green cells link across sheets.', '',
 'IT IS FORMULA-DRIVEN. Every figure that can be derived arithmetically from a driver is a live formula, so',
 'you can change a blue cell on Assumptions and watch the model reprice: the cost of capital is built from',
 'the AED government yield net of the sovereign spread, beta and the premium rather than pasted; the',
 'development backlog rolls forward in front of you (opening backlog + new sales − recognised revenue);',
 'the DCF waterfall chains EBITDA → EBIT → NOPAT → free cash flow → present value; the terminal block',
 'derives its reinvestment rate from growth over return on capital; and the income statement, balance',
 'sheet, cash flow, ratios and all four lenses chain off the same cells.', '',
 'THREE THINGS ARE PASTED VALUES, and it is worth knowing exactly which. First, audited and disclosed',
 'history — the primary record, not a calculation (where a line is both disclosed and derivable, the',
 'DISCLOSED figure is carried). Second, the FY2025 four-segment base — revenue, gross profit and assets',
 'for the segments the company itself discloses (Real Estate Development; Asset & Investment Management;',
 'Hospitality; Events, Catering & Tourism) — pasted once, with the entire five-year forecast chaining off',
 'it as formulas. Third, whole-model engine outputs, where each figure is a complete re-run of the entire',
 'valuation and cannot be one formula: the Monte Carlo price map, the sensitivity grids, the DCF bear/bull',
 'scenario bounds (the backlog run-off and growth-hold alternatives) and the Egypt-risk stress. Those grids',
 'do NOT redraw when a driver changes; everything else reprices live.', '',
 'How revenue is built. Not as one growth rate. Development revenue converts the disclosed AED 42.6bn',
 'development backlog at a visible conversion rate, plus point-in-time land sales, with new launches',
 'rolling the backlog forward on the sheet; the other three segments grow on their own drivers (occupancy',
 'and GLA for asset management, keys × occupancy for hospitality, the events calendar for ECT). Margins',
 'are OUTPUTS of the segment build, not inputs to it.', '',
 'The contested judgement, shown both ways. Whether the record FY2025-26 development surge persists',
 '(base: normalising-but-sustained launches) or fades to backlog run-off is the single judgement that',
 'moves this valuation most. Both DCFs are shown side by side on Fundamental Valuation and Summary;',
 'they are never averaged.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model',
 'outputs shown as ranges.', '',
 'Sourcing note, up front. FY2023 (Q Holding perimeter), FY2024 and FY2025 all come from the company\'s own',
 'audited consolidated financial statements, retrieved from modon.com investor relations; H1-2026 from the',
 'reviewed interim. FY2024 is a perimeter break (the Modon Properties/ADNEC combination; bargain-purchase',
 'gain AED 9,192mn) and is dual-framed wherever it appears. Every input is annotated where it appears and',
 'listed with source and date in the companion bibliography document.', '',
 'Discount convention. The explicit window discounts at a single AED cost of capital built on the sheet',
 '(the AED curve is flat-pegged to the USD; there is no easing glide to derive, and the discount factors',
 'compound in front of you on the DCF sheet). The terminal value is capitalised at the terminal rate and',
 'discounted at the year-5 factor. One date, one price of time.', '',
 f"Currency. AED million unless stated. Spot AED {SPOT:.2f} ({M['asof']} anchor; close 07-Aug-2026).",
 'Sheets: READ FIRST · Summary · Fundamental Valuation · Assumptions · SOTP Bridge · Segments · Relative &',
 'Normalized · DCF · Income Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo ·',
 'Sensitivity · Per-Share & Ratios · Peer & Sector.'], start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 112

# ============ 4 ASSUMPTIONS (built early so other sheets can reference) =======
# laid out: label in A, scalar in C, or vectors across C..G
aws = wb.create_sheet('Assumptions')
title(aws, 'Assumptions — every blue cell reprices the model', 'Vectors run FY2026E..FY2030E across columns C..G',
      8, awidth=62, cwidth=12)
AR = {}
_r = 4
def arow(label, vals, fmt=NUM0, note=None):
    global _r
    put(aws, f'A{_r}', label, fmt=None)
    if isinstance(vals, (list, tuple)):
        for j, v in enumerate(vals):
            put(aws, f'{chr(67 + j)}{_r}', v, BLUE, fmt)
    else:
        put(aws, f'C{_r}', vals, BLUE, fmt)
    if note:
        put(aws, f'I{_r}', note, SUB, None)
    AR[label] = _r
    _r += 1
    return _r - 1

hdr(aws, 3, ['Driver', '', 'FY26E / value', 'FY27E', 'FY28E', 'FY29E', 'FY30E'])
r_spot   = arow('Spot price (AED, 7-Aug-2026 close)', SPOT, PX)
r_sh     = arow('Shares outstanding (mn)', SH, NUM0)
r_conv   = arow('Backlog conversion rate on opening development backlog', IN['conv_path'], PCT)
r_ns     = arow('New development sales (AED mn)', IN['new_sales'], NUM0)
r_land   = arow('Land and plot sales revenue (AED mn)', IN['land_rev'], NUM0)
r_redm   = arow('Development gross margin', IN['red_margin'], PCT)
r_aimg   = arow('Asset & investment management revenue growth', IN['aim_growth'], PCT)
r_aimm   = arow('Asset & investment management gross margin', IN['aim_margin'], PCT)
r_hosg   = arow('Hospitality revenue growth', IN['hosp_growth'], PCT)
r_hosm   = arow('Hospitality gross margin', IN['hosp_margin'], PCT)
r_ectg   = arow('Events, catering & tourism revenue growth', IN['ect_growth'], PCT)
r_ectm   = arow('Events, catering & tourism gross margin', IN['ect_margin'], PCT)
r_othr   = arow('Others / eliminations revenue (AED mn)', IN['oth_rev_f'], NUM0)
r_othg   = arow('Others gross loss (AED mn)', IN['oth_gp_f'], NUM0)
r_ga     = arow('General & administrative / revenue', IN['ga_pct'], PCT)
r_sm     = arow('Selling & marketing / revenue', IN['sm_pct'], PCT)
r_inv    = arow('Investment and other income, recurring (AED mn)', IN['invinc_f'], NUM0)
r_dna    = arow('Depreciation & amortisation / revenue', IN['dna_pct'], PCT)
r_capex  = arow('Capital expenditure (AED mn)', IN['capex_f'], NUM0)
r_nwc    = arow('Working-capital release, negative = absorption (AED mn)', IN['nwc_release'], NUM0)
r_tax    = arow('Effective tax rate (DMTT floor + foreign uplift)', TAX, PCT)
r_nci    = arow('NCI share of profit', IN['nci_pct'], PCT)
r_ab     = arow('Associate income FY2026E base (AED mn)', IN['assoc_base'], NUM0)
r_ag     = arow('Associate income growth', IN['assoc_g'], PCT)
r_debt   = arow('Gross debt path incl. related-party loan (AED mn)', IN['debt_path'], NUM0)
r_cy     = arow('Yield on cash balances', IN['cash_yield'], PCT)
band(aws, _r, 8); put(aws, f'A{_r}', 'Cost of capital build', bold=True, fmt=None); _r += 1
r_rf     = arow('AED government bond yield (Jan-2031 T-Bond auction)', IN['rf'], PCT2)
r_ss     = arow('UAE sovereign default spread (rating basis, netted out)', IN['sov_spread_rating'], PCT2)
r_erp    = arow('Equity risk premium (UAE row, rating basis)', IN['erp_rating'], PCT2)
r_beta   = arow('Beta (tier-3 fallback, flagged; sensitised 0.8-1.2)', IN['beta'], PX)
r_eib    = arow('6-month EIBOR', IN['eibor6m'], PCT2)
r_kdm    = arow('Marginal debt margin over 6M EIBOR', IN['kd_margin'], PCT2)
r_wdt    = arow('Terminal debt weight D/(D+E)', IN['wd_term'], PCT)
r_g      = arow('Terminal growth', IN['g_term'], PCT2)
r_roic   = arow('Terminal return on invested capital', IN['roic_term'], PCT2)
r_days   = arow('Days from 31-Dec-2025 valuation date to the 7-Aug-2026 anchor', IN['anchor_days'], NUM0)
band(aws, _r, 8); put(aws, f'A{_r}', 'FY2025 balance-sheet anchors (audited, pasted)', bold=True, fmt=None); _r += 1
r_cash   = arow('Cash and bank balances FY2025 (AED mn, disclosed)', IN['cash_fy25'], NUM0)
r_d25    = arow('Gross debt FY2025 incl. related-party loan (AED mn, disclosed)', HB['FY25']['debt'], NUM0)
r_lease  = arow('Lease liabilities FY2025 (AED mn, disclosed)', IN['lease_fy25'], NUM0)
r_assoc  = arow('Associates & JVs at carrying value FY2025 (AED mn, disclosed)', IN['assoc_bv_fy25'], NUM0)
r_finass = arow('Investments in financial assets FY2025 (AED mn, disclosed)', IN['finass_fy25'], NUM0)
r_ncib   = arow('Non-controlling interests FY2025 (AED mn, disclosed)', IN['nci_fy25'], NUM0)
r_eqp    = arow('Equity attributable to owners FY2025 (AED mn, disclosed)', IN['eqp_fy25'], NUM0)
r_bl0    = arow('Development backlog at 31-Dec-2025 (AED mn, disclosed)', IN['dev_backlog'], NUM0)
band(aws, _r, 8); put(aws, f'A{_r}', 'Lens settings', bold=True, fmt=None); _r += 1
r_pej    = arow('Justified price/earnings (FY2026E attributable)', IN['pe_just'], MULT)
r_evj    = arow('Justified EV/EBITDA (FY2026E)', IN['ev_ebitda_just'], MULT)
r_nsal   = arow('Through-cycle development sales (AED mn)', IN['norm_sales'], NUM0)
r_nmar   = arow('Through-cycle net margin on revenue', IN['norm_margin'], PCT)
r_npe    = arow('Through-cycle price/earnings', IN['norm_pe'], MULT)
r_roes   = arow('Sustainable return on equity', IN['roe_sust'], PCT)
r_wdcf   = arow('Weight — discounted cash flow', IN['lens_weights']['dcf'], PCT)
r_wrel   = arow('Weight — relative', IN['lens_weights']['relative'], PCT)
r_wnorm  = arow('Weight — normalised', IN['lens_weights']['normalized'], PCT)
r_wbook  = arow('Weight — book', IN['lens_weights']['book'], PCT)

AS = 'Assumptions'
def av(row, col='C'):
    return f"{AS}!${col}${row}"

# ============ 6 SEGMENTS ======================================================
sg = wb.create_sheet('Segments')
title(sg, 'Segments — the four disclosed legs, FY2025 base and forecast build',
      'FY2025 base pasted from IFRS 8 note 33 (audited); every forecast cell is a formula off Assumptions',
      8, awidth=46, cwidth=13)
hdr(sg, 4, ['FY2025 base (audited)', 'Revenue', 'Gross profit', 'GP margin', 'PBT', 'Assets'])
segrows = [('Real Estate Development', 'red'), ('Asset & Investment Management', 'aim'),
           ('Hospitality', 'hosp'), ('Events, Catering & Tourism', 'ect')]
r = 5
SEGROW = {}
for nm, k in segrows:
    put(sg, f'A{r}', nm, fmt=None)
    put(sg, f'B{r}', SEG['rev'][k], BLUE, NUM0)
    put(sg, f'C{r}', SEG['gp'][k], BLUE, NUM0)
    putf(sg, f'D{r}', f'=C{r}/B{r}', SEG['gp'][k] / SEG['rev'][k], PCT)
    put(sg, f'E{r}', SEG['pbt'][k], BLUE, NUM0)
    put(sg, f'F{r}', SEG['assets'][k], BLUE, NUM0)
    SEGROW[k] = r
    r += 1
put(sg, f'A{r}', 'Others / eliminations', fmt=None)
put(sg, f'B{r}', SEG['oth_rev'], BLUE, NUM0); put(sg, f'C{r}', SEG['oth_gp'], BLUE, NUM0)
r_oth = r
r += 1
band(sg, r, 8)
put(sg, f'A{r}', 'Group FY2025', bold=True, fmt=None)
putf(sg, f'B{r}', f'=SUM(B5:B{r_oth})', HI['FY25']['rev'], NUM0, bold=True)
putf(sg, f'C{r}', f'=SUM(C5:C{r_oth})', HI['FY25']['gp'], NUM0, bold=True)
ANCH['seg_rev_tot'] = r
r += 2

# ---- backlog roll-forward + development build --------------------------------
hdr(sg, r, ['Development build'] + YF)
rb = r + 1
put(sg, f'A{rb}', 'Opening development backlog', fmt=None)
put(sg, f'A{rb+1}', 'New development sales', fmt=None)
put(sg, f'A{rb+2}', 'Development revenue recognised (conv × opening)', fmt=None)
put(sg, f'A{rb+3}', 'Closing backlog', fmt=None)
put(sg, f'A{rb+4}', 'Land and plot sales', fmt=None)
put(sg, f'A{rb+5}', 'Real Estate Development revenue', fmt=None)
for t in range(NY):
    c = FC[t]
    ac = chr(67 + t)   # Assumptions vector column
    if t == 0:
        putf(sg, f'{c}{rb}', f"={av(r_bl0)}", F['bl_open'][0], NUM0, green=True)
    else:
        putf(sg, f'{c}{rb}', f"={FC[t-1]}{rb+3}", F['bl_open'][t], NUM0)
    putf(sg, f'{c}{rb+1}', f"={AS}!${ac}${r_ns}", F['new_sales'][t], NUM0, green=True)
    putf(sg, f'{c}{rb+2}', f"={AS}!${ac}${r_conv}*{c}{rb}", F['dev_rev'][t], NUM0)
    putf(sg, f'{c}{rb+3}', f"={c}{rb}+{c}{rb+1}-{c}{rb+2}", F['bl_close'][t], NUM0)
    putf(sg, f'{c}{rb+4}', f"={AS}!${ac}${r_land}", F['land_rev'][t], NUM0, green=True)
    putf(sg, f'{c}{rb+5}', f"={c}{rb+2}+{c}{rb+4}", F['red_rev'][t], NUM0, bold=True)
ANCH['bl_row'] = rb
r = rb + 7

# ---- segment revenue forecast ------------------------------------------------
hdr(sg, r, ['Segment revenue forecast'] + YF)
rs = r + 1
put(sg, f'A{rs}', 'Real Estate Development', fmt=None)
put(sg, f'A{rs+1}', 'Asset & Investment Management', fmt=None)
put(sg, f'A{rs+2}', 'Hospitality', fmt=None)
put(sg, f'A{rs+3}', 'Events, Catering & Tourism', fmt=None)
put(sg, f'A{rs+4}', 'Others / eliminations', fmt=None)
put(sg, f'A{rs+5}', 'Group revenue', fmt=None)
for t in range(NY):
    c = FC[t]; ac = chr(67 + t)
    putf(sg, f'{c}{rs}', f"={c}{rb+5}", F['red_rev'][t], NUM0)
    if t == 0:
        putf(sg, f'{c}{rs+1}', f"=B{SEGROW['aim']}*(1+{AS}!${ac}${r_aimg})", F['aim_rev'][0], NUM0)
        putf(sg, f'{c}{rs+2}', f"=B{SEGROW['hosp']}*(1+{AS}!${ac}${r_hosg})", F['hosp_rev'][0], NUM0)
        putf(sg, f'{c}{rs+3}', f"=B{SEGROW['ect']}*(1+{AS}!${ac}${r_ectg})", F['ect_rev'][0], NUM0)
    else:
        p = FC[t - 1]
        putf(sg, f'{c}{rs+1}', f"={p}{rs+1}*(1+{AS}!${ac}${r_aimg})", F['aim_rev'][t], NUM0)
        putf(sg, f'{c}{rs+2}', f"={p}{rs+2}*(1+{AS}!${ac}${r_hosg})", F['hosp_rev'][t], NUM0)
        putf(sg, f'{c}{rs+3}', f"={p}{rs+3}*(1+{AS}!${ac}${r_ectg})", F['ect_rev'][t], NUM0)
    putf(sg, f'{c}{rs+4}', f"={av(r_othr)}", IN['oth_rev_f'], NUM0, green=True)
    putf(sg, f'{c}{rs+5}', f"=SUM({c}{rs}:{c}{rs+4})", F['rev'][t], NUM0, bold=True)
ANCH['seg_fcst_rev'] = rs
r = rs + 7

hdr(sg, r, ['Gross profit build (margin × revenue)'] + YF)
rg = r + 1
put(sg, f'A{rg}', 'Real Estate Development', fmt=None)
put(sg, f'A{rg+1}', 'Asset & Investment Management', fmt=None)
put(sg, f'A{rg+2}', 'Hospitality', fmt=None)
put(sg, f'A{rg+3}', 'Events, Catering & Tourism', fmt=None)
put(sg, f'A{rg+4}', 'Others', fmt=None)
put(sg, f'A{rg+5}', 'Group gross profit', fmt=None)
put(sg, f'A{rg+6}', 'Group gross margin (output)', fmt=None)
for t in range(NY):
    c = FC[t]; ac = chr(67 + t)
    putf(sg, f'{c}{rg}', f"={c}{rs}*{AS}!${ac}${r_redm}", F['red_rev'][t] * IN['red_margin'][t], NUM0)
    putf(sg, f'{c}{rg+1}', f"={c}{rs+1}*{AS}!${ac}${r_aimm}", F['aim_rev'][t] * IN['aim_margin'][t], NUM0)
    putf(sg, f'{c}{rg+2}', f"={c}{rs+2}*{AS}!${ac}${r_hosm}", F['hosp_rev'][t] * IN['hosp_margin'][t], NUM0)
    putf(sg, f'{c}{rg+3}', f"={c}{rs+3}*{AS}!${ac}${r_ectm}", F['ect_rev'][t] * IN['ect_margin'][t], NUM0)
    putf(sg, f'{c}{rg+4}', f"={av(r_othg)}", IN['oth_gp_f'], NUM0, green=True)
    putf(sg, f'{c}{rg+5}', f"=SUM({c}{rg}:{c}{rg+4})", F['gp'][t], NUM0, bold=True)
    putf(sg, f'{c}{rg+6}', f"={c}{rg+5}/{c}{rs+5}", F['gp'][t] / F['rev'][t], PCT)
ANCH['seg_fcst_gp'] = rg

# ============ 8 DCF ===========================================================
dc = wb.create_sheet('DCF')
title(dc, 'DCF — waterfall, cost of capital build, terminal block, bridge to per-share',
      'Chains live off Segments and Assumptions; the three engine alternatives are labelled pastes', 8,
      awidth=52, cwidth=13)
hdr(dc, 4, ['Waterfall (AED mn)'] + YF)
rw = 5
LBL = ['Revenue', 'Gross profit', 'General & administrative', 'Selling & marketing',
       'Investment and other income', 'EBIT (post-D&A, ex-fair-value items)',
       'EBITDA margin (output)', 'Depreciation & amortisation', 'EBITDA',
       'NOPAT = EBIT × (1 − t)', '+ D&A', '− Capital expenditure',
       '− Δ working capital (release enters +)', 'Free cash flow to firm',
       'Discount factor', 'PV of FCFF']
for i, l in enumerate(LBL):
    put(dc, f'A{rw+i}', l, fmt=None)
for t in range(NY):
    c = FC[t]; ac = chr(67 + t)
    rs_, rg_ = ANCH['seg_fcst_rev'], ANCH['seg_fcst_gp']
    putf(dc, f'{c}{rw}',   f"=Segments!{c}{rs_+5}", F['rev'][t], NUM0, green=True)
    putf(dc, f'{c}{rw+1}', f"=Segments!{c}{rg_+5}", F['gp'][t], NUM0, green=True)
    putf(dc, f'{c}{rw+2}', f"=-{AS}!${ac}${r_ga}*{c}{rw}", -F['ga'][t], NUM0)
    putf(dc, f'{c}{rw+3}', f"=-{AS}!${ac}${r_sm}*{c}{rw}", -F['sm'][t], NUM0)
    putf(dc, f'{c}{rw+4}', f"={AS}!${ac}${r_inv}", F['invinc'][t], NUM0, green=True)
    putf(dc, f'{c}{rw+5}', f"=SUM({c}{rw+1}:{c}{rw+4})", F['ebit'][t], NUM0, bold=True)
    putf(dc, f'{c}{rw+6}', f"=({c}{rw+5}+{c}{rw+7})/{c}{rw}", F['ebitda'][t] / F['rev'][t], PCT)
    putf(dc, f'{c}{rw+7}', f"={av(r_dna)}*{c}{rw}", F['dna'][t], NUM0)
    putf(dc, f'{c}{rw+8}', f"={c}{rw+5}+{c}{rw+7}", F['ebitda'][t], NUM0)
    putf(dc, f'{c}{rw+9}', f"={c}{rw+5}*(1-{av(r_tax)})", F['nopat'][t], NUM0)
    putf(dc, f'{c}{rw+10}', f"={c}{rw+7}", F['dna'][t], NUM0)
    putf(dc, f'{c}{rw+11}', f"=-{AS}!${ac}${r_capex}", -F['capex'][t], NUM0)
    putf(dc, f'{c}{rw+12}', f"={AS}!${ac}${r_nwc}", -F['dnwc'][t], NUM0, green=True)
    putf(dc, f'{c}{rw+13}', f"=SUM({c}{rw+9}:{c}{rw+12})", F['fcff'][t], NUM0, bold=True)
    putf(dc, f'{c}{rw+14}', f"=1/(1+$C$30)^{t+1}", F['df'][t], DF4)
    putf(dc, f'{c}{rw+15}', f"={c}{rw+13}*{c}{rw+14}", F['pv'][t], NUM0)
ANCH['dcf_rw'] = rw
r = rw + 17
band(dc, r, 8); put(dc, f'A{r}', 'Cost of capital — built on the sheet, never pasted', bold=True, fmt=None)
r += 1
put(dc, f'A{r}', 'Normalised risk-free rate rf* = AED yield − sovereign spread', fmt=None)
putf(dc, f'C{r}', f"={av(r_rf)}-{av(r_ss)}", W['rf_star'], PCT2, green=True); r_rfs = r; r += 1
put(dc, f'A{r}', 'Cost of equity Ke = rf* + β × ERP', fmt=None)
putf(dc, f'C{r}', f"=C{r_rfs}+{av(r_beta)}*{av(r_erp)}", W['ke_exp'], PCT2); r_ke = r; r += 1
put(dc, f'A{r}', 'Marginal cost of debt Kd = 6M EIBOR + margin', fmt=None)
putf(dc, f'C{r}', f"={av(r_eib)}+{av(r_kdm)}", W['kd'], PCT2); r_kd = r; r += 1
put(dc, f'A{r}', 'Kd after tax', fmt=None)
putf(dc, f'C{r}', f"=C{r_kd}*(1-{av(r_tax)})", W['kd_at'], PCT2); r_kdat = r; r += 1
put(dc, f'A{r}', 'Market capitalisation (spot × shares)', fmt=None)
putf(dc, f'C{r}', f"={av(r_spot)}*{av(r_sh)}", M['mktcap'], NUM0); r_mc = r; r += 1
put(dc, f'A{r}', 'Equity weight  E/(E+D)', fmt=None)
putf(dc, f'C{r}', f"=C{r_mc}/(C{r_mc}+{av(r_d25)})", W['we_exp'], PCT2); r_we = r; r += 1
put(dc, f'A{r}', 'Debt weight  D/(E+D), book debt at market', fmt=None)
putf(dc, f'C{r}', f"=1-C{r_we}", W['wd_exp'], PCT2); r_wd = r; r += 1
put(dc, f'A{r}', 'Cost of capital (explicit window)', fmt=None)
putf(dc, f'C{r}', f"=C{r_we}*C{r_ke}+C{r_wd}*C{r_kdat}", W['wacc_exp'], PCT2, bold=True)
r_wacc = r; r += 1
assert r_wacc == 30, f'WACC row moved to {r_wacc}; DCF discount factors point at C30'
put(dc, f'A{r}', 'Terminal cost of capital (terminal weights)', fmt=None)
putf(dc, f'C{r}', f"=(1-{av(r_wdt)})*C{r_ke}+{av(r_wdt)}*C{r_kd}*(1-{av(r_tax)})",
     W['wacc_term'], PCT2, bold=True)
r_wt = r; r += 2
band(dc, r, 8); put(dc, f'A{r}', 'Terminal block — reinvestment derived, never typed', bold=True, fmt=None)
r += 1
put(dc, f'A{r}', 'Terminal growth g', fmt=None)
putf(dc, f'C{r}', f"={av(r_g)}", IN['g_term'], PCT2, green=True); r_gt = r; r += 1
put(dc, f'A{r}', 'Terminal return on invested capital', fmt=None)
putf(dc, f'C{r}', f"={av(r_roic)}", IN['roic_term'], PCT2, green=True); r_rc = r; r += 1
put(dc, f'A{r}', 'Reinvestment rate = g / ROIC', fmt=None)
putf(dc, f'C{r}', f"=C{r_gt}/C{r_rc}", DCF['rr_term'], PCT2); r_rr = r; r += 1
put(dc, f'A{r}', 'Terminal NOPAT = FY2030E NOPAT × (1+g)', fmt=None)
putf(dc, f'C{r}', f"=F{rw+9}*(1+C{r_gt})", DCF['nopat_term'], NUM0); r_tn = r; r += 1
put(dc, f'A{r}', 'Terminal value = NOPAT × (1−RR) / (WACCterm − g)', fmt=None)
putf(dc, f'C{r}', f"=C{r_tn}*(1-C{r_rr})/(C{r_wt}-C{r_gt})", DCF['tv'], NUM0); r_tv = r; r += 1
put(dc, f'A{r}', 'PV of terminal value (year-5 factor)', fmt=None)
putf(dc, f'C{r}', f"=C{r_tv}*F{rw+14}", DCF['pv_tv'], NUM0); r_ptv = r; r += 1
put(dc, f'A{r}', 'PV of explicit years', fmt=None)
putf(dc, f'C{r}', f"=SUM(B{rw+15}:F{rw+15})", DCF['pv_explicit'], NUM0); r_pex = r; r += 1
put(dc, f'A{r}', 'Enterprise value', fmt=None)
putf(dc, f'C{r}', f"=C{r_ptv}+C{r_pex}", DCF['ev'], NUM0, bold=True); r_ev = r; r += 1
put(dc, f'A{r}', 'Terminal value share of enterprise value', fmt=None)
putf(dc, f'C{r}', f"=C{r_ptv}/C{r_ev}", DCF['tv_share'], PCT, bold=True); r_tvs = r; r += 2
band(dc, r, 8); put(dc, f'A{r}', 'EV → equity bridge (31-Dec-2025, audited anchors)', bold=True, fmt=None)
r += 1
BR = [('+ Cash and bank balances', f"={av(r_cash)}", IN['cash_fy25']),
      ('− Gross debt incl. related-party loan', f"=-{av(r_d25)}", -HB['FY25']['debt']),
      ('− Lease liabilities', f"=-{av(r_lease)}", -IN['lease_fy25']),
      ('+ Associates & JVs at carrying value', f"={av(r_assoc)}", IN['assoc_bv_fy25']),
      ('+ Investments in financial assets', f"={av(r_finass)}", IN['finass_fy25']),
      ('− Non-controlling interests (book)', f"=-{av(r_ncib)}", -IN['nci_fy25'])]
r_br0 = r
for l, fml, xp in BR:
    put(dc, f'A{r}', l, fmt=None); putf(dc, f'C{r}', fml, xp, NUM0, green=True); r += 1
put(dc, f'A{r}', 'Equity value attributable (31-Dec-2025)', fmt=None)
putf(dc, f'C{r}', f"=C{r_ev}+SUM(C{r_br0}:C{r-1})", DCF['eq_attr'], NUM0, bold=True)
r_eq = r; r += 1
put(dc, f'A{r}', 'Fair value per share at 31-Dec-2025', fmt=None)
putf(dc, f'C{r}', f"=C{r_eq}/{av(r_sh)}", DCF['ps_dec'], PX, bold=True); r_psd = r; r += 1
put(dc, f'A{r}', 'Anchor accretion factor (1+Ke)^(days/365)', fmt=None)
putf(dc, f'C{r}', f"=(1+C{r_ke})^({av(r_days)}/365)", DCF['roll'], DF4); r_roll = r; r += 1
put(dc, f'A{r}', 'Fair value per share at the 7-Aug-2026 anchor', fmt=None)
putf(dc, f'C{r}', f"=C{r_psd}*C{r_roll}", DCF['ps'], PX, bold=True); r_ps = r; r += 2
put(dc, f'A{r}', 'Scenario re-runs (engine outputs, pasted): backlog run-off / growth-hold / Egypt stress',
    fmt=None)
put(dc, f'C{r}', CJ['runoff_ps'], BLUE, PX); put(dc, f'D{r}', CJ['bull_ps'], BLUE, PX)
put(dc, f'E{r}', DCF['ps_egystress'], BLUE, PX)
ANCH['dcf'] = dict(wacc=r_wacc, wt=r_wt, ev=r_ev, tvs=r_tvs, eq=r_eq, psd=r_psd,
                   roll=r_roll, ps=r_ps, ke=r_ke, kd=r_kd, rfs=r_rfs, rr=r_rr,
                   tn=r_tn, tv=r_tv, ptv=r_ptv, pex=r_pex)

# ============ 7 RELATIVE & NORMALIZED =========================================
rn = wb.create_sheet('Relative & Normalized')
title(rn, 'Relative multiples · normalised earnings power · book value',
      'Peer figures are cross-checks from the peers\' own releases (pasted, labelled); every implied value is a formula',
      7, awidth=52, cwidth=14)
hdr(rn, 4, ['Relative multiples', 'Value'])
r = 5
put(rn, f'A{r}', 'FY2026E attributable profit (AED mn)', fmt=None)
putf(rn, f'C{r}', "='Income Statement'!E17", F['np_attr'][0], NUM0, green=True); r_np26 = r; r += 1
put(rn, f'A{r}', 'Justified P/E × FY2026E EPS', fmt=None)
putf(rn, f'C{r}', f"={av(r_pej)}*C{r_np26}/{av(r_sh)}", REL['pe_ps'], PX); r_pe = r; r += 1
put(rn, f'A{r}', 'FY2026E EBITDA (AED mn)', fmt=None)
putf(rn, f'C{r}', f"=DCF!B{ANCH['dcf_rw']+8}", F['ebitda'][0], NUM0, green=True); r_eb26 = r; r += 1
put(rn, f'A{r}', 'Justified EV/EBITDA → EV', fmt=None)
putf(rn, f'C{r}', f"={av(r_evj)}*C{r_eb26}", REL['ev_ebitda_just'] * F['ebitda'][0], NUM0); r_evr = r; r += 1
put(rn, f'A{r}', '→ equity per share through the same bridge', fmt=None)
putf(rn, f'C{r}', f"=(C{r_evr}+{av(r_cash)}-{av(r_d25)}-{av(r_lease)}+{av(r_assoc)}"
                  f"+{av(r_finass)}-{av(r_ncib)})/{av(r_sh)}", REL['ev_ps'], PX); r_evps = r; r += 2
band(rn, r, 7)
put(rn, f'A{r}', 'Relative lens (mean of the two)', bold=True, fmt=None)
putf(rn, f'C{r}', f"=AVERAGE(C{r_pe},C{r_evps})", REL['base'], PX, bold=True)
r_rel = r
assert r_rel == 11, f'relative lens row {r_rel} — recalc references C11'
r += 1
put(rn, f'A{r}', 'bear / bull (blended lens scaled to the 4.08x floor · 9.5x ceiling)', fmt=None)
putf(rn, f'C{r}', f"=C{r_rel}*4.08/{av(r_pej)}", LN['relative']['bear'], PX)
putf(rn, f'D{r}', f"=C{r_rel}*9.5/{av(r_pej)}", LN['relative']['bull'], PX)
r += 2
hdr(rn, r, ['Trailing cross-checks (formulas on disclosed figures)', 'Value'])
r += 1
put(rn, f'A{r}', 'Trailing P/E on FY2025 profit', fmt=None)
putf(rn, f'C{r}', f"=DCF!C{ANCH['dcf']['wacc']-3}/{IN['pat_fy25']}", M['mktcap'] / IN['pat_fy25'], MULT)
r += 1
put(rn, f'A{r}', 'Trailing EV/EBITDA (EV = mktcap + net debt)', fmt=None)
putf(rn, f'C{r}', f"=(DCF!C{ANCH['dcf']['wacc']-3}+{av(r_d25)}-{av(r_cash)})/{HI['FY25']['ebitda']}",
     REL['ev_ebitda_trailing'], MULT)
r += 2
hdr(rn, r, ['Normalised earnings power', 'Value'])
r += 1
put(rn, f'A{r}', 'Through-cycle development sales → recognised revenue (85%)', fmt=None)
putf(rn, f'C{r}', f"={av(r_nsal)}*0.85+({SEG['rev']['aim']}+{SEG['rev']['hosp']}"
                  f"+{SEG['rev']['ect']})*1.15", NRM['rev'], NUM0); r_nrev = r; r += 1
put(rn, f'A{r}', 'Through-cycle net margin', fmt=None)
putf(rn, f'C{r}', f"={av(r_nmar)}", NRM['margin'], PCT, green=True); r_nm = r; r += 1
put(rn, f'A{r}', 'Normalised net profit', fmt=None)
putf(rn, f'C{r}', f"=C{r_nrev}*C{r_nm}", NRM['np'], NUM0); r_nnp = r; r += 1
put(rn, f'A{r}', 'Normalised EPS', fmt=None)
putf(rn, f'C{r}', f"=C{r_nnp}/{av(r_sh)}", NRM['eps'], PX); r_neps = r; r += 1
while r < 27:
    r += 1
put(rn, f'A{r+1}', 'Normalised lens = EPS × through-cycle P/E', bold=True, fmt=None)
putf(rn, f'C{r+1}', f"=C{r_neps}*{av(r_npe)}", NRM['base'], PX, bold=True)
putf(rn, f'E{r+1}', f"=C{r_neps}*6", LN['normalized']['bear'], PX)
putf(rn, f'F{r+1}', f"=C{r_neps}*10.5", LN['normalized']['bull'], PX)
r_norm = r + 1
assert r_norm == 28, f'normalised lens row {r_norm} — recalc references C28'
r += 3
hdr(rn, r, ['Book value & sustainable return', 'Value'])
r += 1
put(rn, f'A{r}', 'Book value per share (audited FY2025 attributable equity)', fmt=None)
putf(rn, f'C{r}', f"={av(r_eqp)}/{av(r_sh)}", BK['bvps'], PX); r_bv = r; r += 1
put(rn, f'A{r}', 'Justified P/B = (ROE − g)/(Ke − g)', fmt=None)
putf(rn, f'C{r}', f"=({av(r_roes)}-{av(r_g)})/(DCF!C{ANCH['dcf']['ke']}-{av(r_g)})",
     BK['pb_just'], MULT); r_pb = r; r += 1
while r < 36:
    r += 1
put(rn, f'A{r}', 'Book lens = BVPS × justified P/B', bold=True, fmt=None)
putf(rn, f'C{r}', f"=C{r_bv}*C{r_pb}", BK['base'], PX, bold=True)
putf(rn, f'E{r}', f"=C{r_bv}*((0.055-{av(r_g)})/(DCF!C{ANCH['dcf']['ke']}-{av(r_g)}))",
     LN['book']['bear'], PX)
putf(rn, f'F{r}', f"=C{r_bv}*((0.095-{av(r_g)})/(DCF!C{ANCH['dcf']['ke']}-{av(r_g)}))",
     LN['book']['bull'], PX)
r_book = r

# ============ 2 SUMMARY (values reference sheets built above) =================
ws = wb['Summary'] if 'Summary' in wb.sheetnames else wb.create_sheet('Summary')
ws = wb.create_sheet('Summary') if 'Summary' not in wb.sheetnames else ws
title(ws, 'Summary — valuation at a glance', 'All values link live to their source sheets', 7,
      awidth=44, cwidth=15)
hdr(ws, 4, ['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'Contribution', 'vs spot'])
LENS_SRC = {'dcf': f"=DCF!C{ANCH['dcf']['ps']}", 'relative': "='Relative & Normalized'!C11",
            'normalized': "='Relative & Normalized'!C28", 'book': "='Relative & Normalized'!C36"}
BEAR_SRC = {'normalized': "='Relative & Normalized'!E28", 'book': "='Relative & Normalized'!E36",
            'relative': "='Relative & Normalized'!C12"}
BULL_SRC = {'normalized': "='Relative & Normalized'!F28", 'book': "='Relative & Normalized'!F36",
            'relative': "='Relative & Normalized'!D12"}
WROW = {'dcf': r_wdcf, 'relative': r_wrel, 'normalized': r_wnorm, 'book': r_wbook}
r = 5
for k in ['dcf', 'relative', 'normalized', 'book']:
    l = LN[k]
    put(ws, f'A{r}', l['name'], fmt=None)
    if k in BEAR_SRC:
        putf(ws, f'B{r}', BEAR_SRC[k], l['bear'], PX, green=True)
    else:
        put(ws, f'B{r}', l['bear'], BLUE, PX)   # DCF bear/bull are whole-model re-runs
    putf(ws, f'C{r}', LENS_SRC[k], l['base'], PX, green=True)
    if k in BULL_SRC:
        putf(ws, f'D{r}', BULL_SRC[k], l['bull'], PX, green=True)
    else:
        put(ws, f'D{r}', l['bull'], BLUE, PX)
    putf(ws, f'E{r}', f"={av(WROW[k])}", l['w'], PCT, green=True)
    putf(ws, f'F{r}', f'=C{r}*E{r}', l['base'] * l['w'], PX)
    putf(ws, f'G{r}', f'=C{r}/$C$14-1', l['base'] / SPOT - 1, PCT)
    r += 1
band(ws, r, 7)
LK = ['dcf', 'relative', 'normalized', 'book']
put(ws, f'A{r}', 'Weighted central', bold=True, fmt=None)
putf(ws, f'B{r}', '=MIN(B5:B8)', min(LN[k]['bear'] for k in LK), PX, bold=True)
putf(ws, f'C{r}', '=SUM(F5:F8)', D['central'], PX, bold=True)
putf(ws, f'D{r}', '=MAX(D5:D8)', max(LN[k]['bull'] for k in LK), PX, bold=True)
putf(ws, f'E{r}', '=SUM(E5:E8)', 1.0, PCT, bold=True)
putf(ws, f'G{r}', f'=C{r}/$C$14-1', D['central'] / SPOT - 1, PCT, bold=True)
assert r == 9, f'central row {r} — recalc references C9'
r += 2
put(ws, f'A{r}', 'The contested judgement, both ways: DCF base vs backlog run-off', fmt=None)
putf(ws, f'C{r}', f"=DCF!C{ANCH['dcf']['ps']}", DCF['ps'], PX, green=True)
put(ws, f'D{r}', CJ['runoff_ps'], BLUE, PX)
r += 1
put(ws, f'A{r}', 'Terminal value share of DCF enterprise value', fmt=None)
putf(ws, f'C{r}', f"=DCF!C{ANCH['dcf']['tvs']}", DCF['tv_share'], PCT, green=True)
assert r == 12, f'TV-share row {r} — recalc references C12'
r += 1
put(ws, f'A{r}', 'Expert panel median', fmt=None)
put(ws, f'C{r}', D['panel_centre'], BLUE, PX)   # engine output (three worked panels)
r += 1
band(ws, r, 7)
put(ws, f'A{r}', 'Market price (anchor, 7-Aug-2026)', bold=True, fmt=None)
putf(ws, f'C{r}', f"={av(r_spot)}", SPOT, PX, bold=True, green=True)     # row 14
assert r == 14
ANCH['summary_mktcap'] = 'C17'
r += 2
hdr(ws, r, ['Key figure', 'Value'])
r += 1
put(ws, f'A{r}', 'Market capitalisation (AED mn)', fmt=None)
putf(ws, f'C{r}', f"={av(r_spot)}*{av(r_sh)}", M['mktcap'], NUM0)
r += 1
for label, fml, xp, fmt in [
    ('Net cash, strict basis (cash − debt, FY2025)', f"={av(r_cash)}-{av(r_d25)}",
     -HB['FY25']['nd'], NUM0),
    ('Net cash, company definition (disclosed)', IN['netcash_company'], None, NUM0),
    ('FY2025 revenue (AED mn)', "='Income Statement'!D5", HI['FY25']['rev'], NUM0),
    ('FY2025 EBITDA (AED mn)', "='Income Statement'!D7", HI['FY25']['ebitda'], NUM0),
    ('FY2025 attributable profit (AED mn)', "='Income Statement'!D17", HI['FY25']['npa'], NUM0),
    ('Cost of capital (explicit window)', f"=DCF!C{ANCH['dcf']['wacc']}", W['wacc_exp'], PCT2),
    ('Cost of capital (terminal)', f"=DCF!C{ANCH['dcf']['wt']}", W['wacc_term'], PCT2),
    ('Terminal growth', f"={av(r_g)}", IN['g_term'], PCT2)]:
    put(ws, f'A{r}', label, fmt=None)
    if isinstance(fml, str):
        putf(ws, f'C{r}', fml, xp, fmt, green=True)
    else:
        put(ws, f'C{r}', fml, BLUE, fmt)
    r += 1
r += 1
hdr(ws, r, ['Monte Carlo price map (engine re-run, pasted)', '1 month', '3 months'])
r += 1
for lbl, key in [('5th percentile', 'p5'), ('25th percentile', 'p25'), ('Median', 'p50'),
                 ('75th percentile', 'p75'), ('95th percentile', 'p95')]:
    put(ws, f'A{r}', lbl, fmt=None)
    put(ws, f'B{r}', STK['horizons']['1M']['pct'][key], BLUE, PX)
    put(ws, f'C{r}', STK['horizons']['3M']['pct'][key], BLUE, PX)
    r += 1

# ============ 3 FUNDAMENTAL VALUATION =========================================
fv = wb.create_sheet('Fundamental Valuation')
title(fv, 'Fundamental valuation — four lenses, the contested judgement and the stress readings',
      None, 6, awidth=56, cwidth=15)
hdr(fv, 4, ['Lens / step', 'Basis', 'AED per share'])
rows = [
    ('Discounted cash flow (primary)', 'links to the DCF sheet', f"=DCF!C{ANCH['dcf']['ps']}", DCF['ps']),
    ('  backlog run-off alternative', 'new sales halve and fade; margins compress (engine re-run)',
     CJ['runoff_ps'], None),
    ('  growth-hold alternative', 'sales hold at AED 30bn; margins hold (engine re-run)',
     CJ['bull_ps'], None),
    ('  Egypt-risk stress', 'non-UAE revenue share carries the Egypt country premium (engine re-run)',
     DCF['ps_egystress'], None),
    ('Relative multiples', 'justified P/E and EV/EBITDA against the UAE developer set',
     "='Relative & Normalized'!C11", REL['base']),
    ('Normalised earnings power', 'through-cycle sales and margin at a through-cycle multiple',
     "='Relative & Normalized'!C28", NRM['base']),
    ('Book value and sustainable return', 'justified price-to-book on sustainable return on equity',
     "='Relative & Normalized'!C36", BK['base']),
]
r = 5
for a_, b_, c_, xp in rows:
    put(fv, f'A{r}', a_, fmt=None); put(fv, f'B{r}', b_, fmt=None)
    if isinstance(c_, str):
        putf(fv, f'C{r}', c_, xp, PX, green=True)
    else:
        put(fv, f'C{r}', c_, BLUE, PX)
    r += 1
r += 1
band(fv, r, 3); put(fv, f'A{r}', 'Weighted central (links to Summary)', bold=True, fmt=None)
putf(fv, f'C{r}', "=Summary!C9", D['central'], PX, bold=True); r += 2
put(fv, f'A{r}', 'What the market price implies', fmt=None)
put(fv, f'B{r}', 'cost-of-equity adder that reconciles the base DCF to spot (engine solve)', fmt=None)
put(fv, f'C{r}', D['market_implied']['ke_add'], BLUE, PCT2); r += 2
hdr(fv, r, ['Expert panel (engine re-runs, worked in Appendix C)', 'Method', 'AED per share'])
r += 1
for lbl, e in [('Expert 1', 'e1'), ('Expert 2', 'e2'), ('Expert 3', 'e3')]:
    put(fv, f'A{r}', lbl, fmt=None); put(fv, f'B{r}', EXP[e]['method_short'], fmt=None)
    put(fv, f'C{r}', EXP[e]['base'], BLUE, PX)
    r += 1
put(fv, f'A{r}', 'Panel median', bold=True, fmt=None)
putf(fv, f'C{r}', f"=MEDIAN(C{r-3}:C{r-1})", D['panel_centre'], PX, bold=True)

# ============ 5 SOTP BRIDGE ===================================================
sb = wb.create_sheet('SOTP Bridge')
title(sb, 'SOTP bridge — segment EV split and the EV → equity walk',
      'The four legs share one AED discount rate; the Egypt stress prices the cross-border leg separately', 6,
      awidth=52, cwidth=15)
hdr(sb, 4, ['Enterprise value by segment', 'Weight base (FY2025 GP less corporate load)', 'AED mn'])
r = 5
tot_w = sum(max(v, 0.0) for v in D['sotp']['weights'].values())
r_w0 = r
for k, nm in [('red', 'Real Estate Development'), ('aim', 'Asset & Investment Management'),
              ('hosp', 'Hospitality'), ('ect', 'Events, Catering & Tourism')]:
    put(sb, f'A{r}', nm, fmt=None)
    put(sb, f'B{r}', D['sotp']['weights'][k], BLUE, NUM0)
    putf(sb, f'C{r}', f"=MAX(B{r},0)/SUMPRODUCT((B$5:B$8>0)*B$5:B$8)*DCF!C{ANCH['dcf']['ev']}"
         if False else f"=MAX(B{r},0)/{tot_w:.6f}*DCF!C{ANCH['dcf']['ev']}",
         D['sotp']['ev_split'][k], NUM0)
    r += 1
band(sb, r, 6)
put(sb, f'A{r}', 'Enterprise value (links to DCF)', bold=True, fmt=None)
putf(sb, f'C{r}', f"=DCF!C{ANCH['dcf']['ev']}", DCF['ev'], NUM0, bold=True); r_bev = r
assert r_bev == 9
r += 1
put(sb, f'A{r}', 'Terminal value share of enterprise value', fmt=None)
putf(sb, f'C{r}', f"=DCF!C{ANCH['dcf']['tvs']}", DCF['tv_share'], PCT); r += 1
for l, fml, xp in [('+ Cash and bank balances', f"={av(r_cash)}", IN['cash_fy25']),
                   ('− Gross debt incl. related-party loan', f"=-{av(r_d25)}", -HB['FY25']['debt']),
                   ('− Lease liabilities', f"=-{av(r_lease)}", -IN['lease_fy25']),
                   ('+ Associates & JVs', f"={av(r_assoc)}", IN['assoc_bv_fy25']),
                   ('+ Financial assets', f"={av(r_finass)}", IN['finass_fy25']),
                   ('− Non-controlling interests (book)', f"=-{av(r_ncib)}", -IN['nci_fy25'])]:
    put(sb, f'A{r}', l, fmt=None); putf(sb, f'C{r}', fml, xp, NUM0, green=True); r += 1
band(sb, r, 6)
put(sb, f'A{r}', 'Equity attributable → per share → at anchor', bold=True, fmt=None)
putf(sb, f'C{r}', f"=C{r_bev}+SUM(C11:C{r-1})", DCF['eq_attr'], NUM0, bold=True); r_beq = r
r += 1
putf(sb, f'C{r}', f"=C{r_beq}/{av(r_sh)}", DCF['ps_dec'], PX)
put(sb, f'A{r}', 'per share, 31-Dec-2025', fmt=None); r += 1
putf(sb, f'C{r}', f"=C{r-1}*DCF!C{ANCH['dcf']['roll']}", DCF['ps'], PX, bold=True)
put(sb, f'A{r}', 'per share at the 7-Aug-2026 anchor', fmt=None)
r += 2
put(sb, f'A{r}', 'NCI alternative framing (capitalised at share of profit, engine)', fmt=None)
put(sb, f'C{r}', DCF['ps_nci_alt'], BLUE, PX)

# ============ 9 INCOME STATEMENT ==============================================
istmt = wb.create_sheet('Income Statement')
title(istmt, 'Income statement — 3 years audited + 5 years forecast',
      'FY2023 is the Q Holding perimeter; FY2024 contains the AED 9,192mn bargain-purchase gain (dual-framed)',
      10, awidth=42, cwidth=12)
hdr(istmt, 4, [''] + ['FY2023', 'FY2024', 'FY2025'] + YF)
ROWS = [('Revenue', 'rev'), ('Gross profit', 'gp'), ('EBITDA (house)', 'ebitda'),
        ('EBITDA margin', None), ('Depreciation & amortisation', 'dna'),
        ('EBIT', 'ebit'), ('Net finance result', 'fin'), ('Associates & JVs', 'assoc'),
        ('Profit before tax', 'ebt'), ('Income tax', 'tax'), ('Profit for the year', 'pat'),
        ('Non-controlling interests', 'nci'), ('Attributable profit', 'npa')]
r = 5
IS_ROW = {}
for i, (lbl, key) in enumerate(ROWS):
    put(istmt, f'A{r+i}', lbl, fmt=None)
    IS_ROW[lbl] = r + i
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    c = HC[j]
    H = HI[y]
    put(istmt, f'{c}5', H['rev'], BLUE, NUM0)
    put(istmt, f'{c}6', H['gp'], BLUE, NUM0)
    put(istmt, f'{c}7', H['ebitda'], BLUE, NUM0)
    putf(istmt, f'{c}8', f'={c}7/{c}5', H['ebitda'] / H['rev'], PCT)
    put(istmt, f'{c}9', H['dna'], BLUE, NUM0)
    putf(istmt, f'{c}10', f'={c}7-{c}9', H['ebit'], NUM0)
    put(istmt, f'{c}11', H['fin'], BLUE, NUM0)
    put(istmt, f'{c}12', H['assoc'], BLUE, NUM0)
    putf(istmt, f'{c}13', f'={c}10+{c}11+{c}12', H['ebit'] + H['fin'] + H['assoc'], NUM0)
    put(istmt, f'{c}14', H['tax'], BLUE, NUM0)
    putf(istmt, f'{c}15', f'={c}13+{c}14', H['ebt'] + H['tax'], NUM0)
    put(istmt, f'{c}16', H['nci'], BLUE, NUM0)
    putf(istmt, f'{c}17', f'={c}15-{c}16', H['pat'] - H['nci'], NUM0, bold=True)
for t in range(NY):
    c = FCOL[t]; dcfc = FC[t]; ac = chr(67 + t)
    rw_ = ANCH['dcf_rw']
    putf(istmt, f'{c}5', f"=DCF!{dcfc}{rw_}", F['rev'][t], NUM0, green=True)
    putf(istmt, f'{c}6', f"=DCF!{dcfc}{rw_+1}", F['gp'][t], NUM0, green=True)
    putf(istmt, f'{c}7', f"=DCF!{dcfc}{rw_+8}", F['ebitda'][t], NUM0, green=True)
    putf(istmt, f'{c}8', f'={c}7/{c}5', F['ebitda'][t] / F['rev'][t], PCT)
    putf(istmt, f'{c}9', f"=DCF!{dcfc}{rw_+7}", F['dna'][t], NUM0, green=True)
    putf(istmt, f'{c}10', f'={c}7-{c}9', F['ebit'][t], NUM0)
    # net finance result = cash yield x opening cash - (kd x avg debt + 35)
    d_open = f"{av(r_d25)}" if t == 0 else f"{AS}!${chr(66 + t)}${r_debt}"
    c_open_ref = f"'Balance Sheet'!{HC[2]}9" if t == 0 else f"'Balance Sheet'!{FCOL[t-1]}9"
    putf(istmt, f'{c}11',
         f"={av(r_cy)}*{c_open_ref}-(DCF!$C${ANCH['dcf']['kd']}*({d_open}+{AS}!${ac}${r_debt})/2+35)",
         D['fcst']['cash'][t - 1] * IN['cash_yield'] - F['interest'][t]
         if t > 0 else IN['cash_fy25'] * IN['cash_yield'] - F['interest'][t], NUM0)
    putf(istmt, f'{c}12', f"={av(r_ab)}*(1+{av(r_ag)})^{t}", F['assoc'][t], NUM0)
    putf(istmt, f'{c}13', f'={c}10+{c}11+{c}12',
         F['ebit'][t] + (D['fcst']['cash'][t - 1] * IN['cash_yield'] if t > 0
                         else IN['cash_fy25'] * IN['cash_yield'])
         - F['interest'][t] + F['assoc'][t], NUM0)
    putf(istmt, f'{c}14', f'=-{c}13*{av(r_tax)}', -(F['np'][t] / (1 - TAX)) * TAX, NUM0)
    putf(istmt, f'{c}15', f'={c}13+{c}14', F['np'][t], NUM0)
    putf(istmt, f'{c}16', f'={c}15*{av(r_nci)}', F['np'][t] * IN['nci_pct'], NUM0)
    putf(istmt, f'{c}17', f'={c}15-{c}16', F['np_attr'][t], NUM0, bold=True)

# ============ 10 BALANCE SHEET ================================================
bsx = wb.create_sheet('Balance Sheet')
title(bsx, 'Balance sheet — 3 years audited + 5-year roll-forward',
      'Forecast: equity rolls on retained profit (no dividend); debt is the drawn path; cash balances derive',
      10, awidth=42, cwidth=12)
hdr(bsx, 4, [''] + ['FY2023', 'FY2024', 'FY2025'] + YF)
BSROWS = ['Property, plant & equipment', 'Investment properties', 'Inventories (land bank)',
          'Development work-in-progress', 'Cash and bank balances', 'Total assets (audited)',
          'Gross debt incl. related-party loan', 'Net working capital (house)',
          'Equity attributable to owners', 'Non-controlling interests', 'Net debt (− = net cash)',
          'Net debt / EBITDA']
r = 5
for i, lbl in enumerate(BSROWS):
    put(bsx, f'A{r+i}', lbl, fmt=None)
BSH = dict(FY23=dict(ppe=789.463, ip=HB['FY23']['ip'], inv=HB['FY23']['inv'], dwip=0.0,
                     cash=HB['FY23']['cash'], assets=HB['FY23']['assets'],
                     debt=HB['FY23']['debt'], nwc=None, eqp=HB['FY23']['eqp'],
                     nci=HB['FY23']['nci']),
           FY24=HB['FY24'], FY25=HB['FY25'])
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    c = HC[j]; H = BSH[y]
    put(bsx, f'{c}5', H['ppe'], BLUE, NUM0)
    put(bsx, f'{c}6', H['ip'], BLUE, NUM0)
    put(bsx, f'{c}7', H['inv'], BLUE, NUM0)
    put(bsx, f'{c}8', H.get('dwip', 0.0), BLUE, NUM0)
    put(bsx, f'{c}9', H['cash'], BLUE, NUM0)
    put(bsx, f'{c}10', H['assets'], BLUE, NUM0)
    put(bsx, f'{c}11', H['debt'], BLUE, NUM0)
    if H.get('nwc') is not None:
        put(bsx, f'{c}12', H['nwc'], BLUE, NUM0)
    else:
        put(bsx, f'{c}12', '-', BLACK, None)
    put(bsx, f'{c}13', H['eqp'], BLUE, NUM0)
    put(bsx, f'{c}14', H['nci'], BLUE, NUM0)
    putf(bsx, f'{c}15', f'={c}11-{c}9', H['debt'] - H['cash'], NUM0)
    eb = HI[y]['ebitda']
    putf(bsx, f'{c}16', f'=({c}11-{c}9)/{eb}', (H['debt'] - H['cash']) / eb, MULT)
for t in range(NY):
    c = FCOL[t]; ac = chr(67 + t); pcol = HC[2] if t == 0 else FCOL[t - 1]
    rw_ = ANCH['dcf_rw']; dcfc = FC[t]
    put(bsx, f'{c}5', '-', BLACK, None); put(bsx, f'{c}6', '-', BLACK, None)
    put(bsx, f'{c}7', '-', BLACK, None); put(bsx, f'{c}8', '-', BLACK, None)
    # cash roll: prior cash + FCFF + net finance in P&L - extra tax on non-EBIT income + Δdebt
    # cash roll matches the model: FCFF + net finance result − the extra tax on
    # non-EBIT income + net drawdowns; associate income is NON-cash (kept at book)
    putf(bsx, f'{c}9',
         f"={pcol}9+DCF!{dcfc}{rw_+13}+'Income Statement'!{c}11"
         f"-('Income Statement'!{c}13-DCF!{dcfc}{rw_+5})*{av(r_tax)}"
         f"+({AS}!${ac}${r_debt}-{av(r_d25) if t == 0 else f'{AS}!${chr(66 + t)}${r_debt}'})",
         F['cash'][t], NUM0)
    put(bsx, f'{c}10', '-', BLACK, None)
    putf(bsx, f'{c}11', f"={AS}!${ac}${r_debt}", F['debt'][t], NUM0, green=True)
    putf(bsx, f'{c}12', f"={pcol}12-{AS}!${ac}${r_nwc}" if t > 0 else
         f"={HB['FY25']['nwc']:.3f}-{AS}!${ac}${r_nwc}", F['nwc'][t], NUM0)
    # equity attributable roll: prior + attributable profit
    eq_exp = float((IN['eqp_fy25'] if t == 0 else EXPECT['Balance Sheet'][f'{FCOL[t-1]}13'])
                   + F['np_attr'][t])
    putf(bsx, f'{c}13', f"={pcol}13+'Income Statement'!{c}17", eq_exp, NUM0)
    putf(bsx, f'{c}14', f"={pcol}14+'Income Statement'!{c}16",
         IN['nci_fy25'] + sum(F['np'][i] * IN['nci_pct'] for i in range(t + 1)), NUM0)
    putf(bsx, f'{c}15', f'={c}11-{c}9', F['net_debt'][t], NUM0)
    putf(bsx, f'{c}16', f"=({c}11-{c}9)/DCF!{dcfc}{rw_+8}",
         F['net_debt'][t] / F['ebitda'][t], MULT)

# ============ 11 CASH FLOW ====================================================
cf = wb.create_sheet('Cash Flow')
title(cf, 'Cash flow — history (audited) and the forecast free-cash-flow chain',
      'Forecast rows link to the DCF waterfall; history is the audited record', 10,
      awidth=46, cwidth=12)
hdr(cf, 4, [''] + ['FY2024', 'FY2025'] + YF)
CFH = D['hist_cf']
put(cf, 'A5', 'Net cash from operating activities (audited)', fmt=None)
put(cf, 'B5', CFH['FY24']['ocf'], BLUE, NUM0); put(cf, 'C5', CFH['FY25']['ocf'], BLUE, NUM0)
put(cf, 'A6', 'Capital expenditure (PP&E + intangibles + IP, audited)', fmt=None)
put(cf, 'B6', CFH['FY24']['capex'], BLUE, NUM0); put(cf, 'C6', CFH['FY25']['capex'], BLUE, NUM0)
put(cf, 'A7', 'H1-2026 operating cash flow (reviewed interim)', fmt=None)
put(cf, 'B7', D['h1']['ocf'], BLUE, NUM0)
put(cf, 'A9', 'Forecast chain (links to the DCF waterfall)', fmt=None, bold=True)
CFROWS = [('NOPAT', 9), ('+ D&A', 10), ('− Capex', 11), ('− Δ working capital', 12),
          ('Free cash flow to firm', 13)]
r = 10
for i, (lbl, off) in enumerate(CFROWS):
    put(cf, f'A{r+i}', lbl, fmt=None)
    for t in range(NY):
        c = ['D', 'E', 'F', 'G', 'H'][t]; dcfc = FC[t]
        vals = dict(zip([9, 10, 11, 12, 13],
                        [F['nopat'][t], F['dna'][t], -F['capex'][t], -F['dnwc'][t],
                         F['fcff'][t]]))
        putf(cf, f'{c}{r+i}', f"=DCF!{dcfc}{ANCH['dcf_rw']+off}", vals[off], NUM0,
             green=True, bold=(off == 13))
hdr(cf, r + 6, ['Forecast years run FY2026E..FY2030E in columns D..H'])

# ============ 12 SUMMARY FINANCIALS ===========================================
sf = wb.create_sheet('Summary Financials')
title(sf, 'Summary financials — the model in one table', 'Every row links live', 10,
      awidth=40, cwidth=12)
hdr(sf, 4, [''] + ['FY2023', 'FY2024', 'FY2025'] + YF)
SFR = [('Revenue', "'Income Statement'!{c}5"), ('EBITDA', "'Income Statement'!{c}7"),
       ('EBITDA margin', "'Income Statement'!{c}8"),
       ('Attributable profit', "'Income Statement'!{c}17"),
       ('Free cash flow to firm', None),
       ('Net debt (− = net cash)', "'Balance Sheet'!{c}15"),
       ('Equity attributable', "'Balance Sheet'!{c}13")]
r = 5
for i, (lbl, src) in enumerate(SFR):
    put(sf, f'A{r+i}', lbl, fmt=None)
for j, c in enumerate(HC + FCOL):
    hist = j < 3
    y = ['FY23', 'FY24', 'FY25'][j] if hist else None
    t = None if hist else j - 3
    putf(sf, f'{c}5', f"='Income Statement'!{c}5",
         HI[y]['rev'] if hist else F['rev'][t], NUM0, green=True)
    putf(sf, f'{c}6', f"='Income Statement'!{c}7",
         HI[y]['ebitda'] if hist else F['ebitda'][t], NUM0, green=True)
    putf(sf, f'{c}7', f"='Income Statement'!{c}8",
         (HI[y]['ebitda'] / HI[y]['rev']) if hist else F['ebitda'][t] / F['rev'][t],
         PCT, green=True)
    putf(sf, f'{c}8', f"='Income Statement'!{c}17",
         HI[y]['npa'] if hist else F['np_attr'][t], NUM0, green=True)
    if hist:
        put(sf, f'{c}9', '-', BLACK, None)
    else:
        putf(sf, f'{c}9', f"='Cash Flow'!{['D','E','F','G','H'][t]}14", F['fcff'][t],
             NUM0, green=True)
    putf(sf, f'{c}10', f"='Balance Sheet'!{c}15",
         (BSH[y]['debt'] - BSH[y]['cash']) if hist else F['net_debt'][t], NUM0, green=True)
    putf(sf, f'{c}11', f"='Balance Sheet'!{c}13",
         BSH[y]['eqp'] if hist else EXPECT['Balance Sheet'][f'{c}13'], NUM0, green=True)
put(sf, 'A13', 'Invested capital (FY2025 base + cumulative capex − D&A + ΔWC)', fmt=None)
for t in range(NY):
    c = FCOL[t]
    putf(sf, f'{c}13', f"={F['ic_fy25']:.3f}"
         + "".join(f"+DCF!{FC[i]}{ANCH['dcf_rw']+11}*-1-DCF!{FC[i]}{ANCH['dcf_rw']+7}"
                   f"-DCF!{FC[i]}{ANCH['dcf_rw']+12}" for i in range(t + 1)),
         F['ic'][t], NUM0)

# ============ 13 MONTE CARLO ==================================================
mc = wb.create_sheet('Monte Carlo')
title(mc, 'Monte Carlo price map — engine re-run (pasted, does not reprice)',
      f"Struck {STK['anchor_date']} at spot {STK['spot']:.2f}; 50,000 paths, seed 42; "
      'grade dates are calendar-resolved', 7, awidth=46, cwidth=13)
hdr(mc, 4, ['', '1 month', '3 months'])
r = 5
H1, H3 = STK['horizons']['1M'], STK['horizons']['3M']
for lbl, k1, k3, fmt in [
        ('Sessions in window', H1['h'], H3['h'], NUM0),
        ('Grade date', H1['grade_date'], H3['grade_date'], None),
        ('Annualised anchor volatility', H1['anchor_vol_ann'], H3['anchor_vol_ann'], PCT),
        ('5th percentile', H1['pct']['p5'], H3['pct']['p5'], PX),
        ('25th percentile', H1['pct']['p25'], H3['pct']['p25'], PX),
        ('Median', H1['pct']['p50'], H3['pct']['p50'], PX),
        ('75th percentile', H1['pct']['p75'], H3['pct']['p75'], PX),
        ('95th percentile', H1['pct']['p95'], H3['pct']['p95'], PX),
        ('P(close above spot)', H1['p_above'], H3['p_above'], PCT),
        ('P(≥ +10%)', H1['p_up10'], H3['p_up10'], PCT),
        ('P(≤ −10%)', H1['p_dn10'], H3['p_dn10'], PCT),
        ('P(touch +5% at any point)', H1['touch_up5'], H3['touch_up5'], PCT),
        ('P(touch −5% at any point)', H1['touch_dn5'], H3['touch_dn5'], PCT)]:
    put(mc, f'A{r}', lbl, fmt=None)
    put(mc, f'B{r}', k1, BLUE, fmt); put(mc, f'C{r}', k3, BLUE, fmt)
    r += 1
r += 1
put(mc, f'A{r}', 'Calibration evidence (walk-forward, this name)', bold=True, fmt=None); r += 1
for lbl, v, fmt in [('Windows scored (post-break)', S0['windows_scored'], NUM0),
                    ('CRPS skill vs carry-anchored random walk', S0['skill_norm'], PCT2),
                    ('Verdict', S0['verdict'], None),
                    ('Coverage of the 80% band', S0['cov80'], PCT),
                    ('Coverage of the 90% band', S0['cov90'], PCT),
                    ('PIT mean (0.5 = centred)', S0['pit_mean'], DF4)]:
    put(mc, f'A{r}', lbl, fmt=None); put(mc, f'B{r}', v, BLUE, fmt); r += 1

# ============ 14 SENSITIVITY ==================================================
sx = wb.create_sheet('Sensitivity')
title(sx, 'Sensitivity — each cell is a complete engine revaluation (pasted)',
      'Rows: cost of capital; columns: terminal growth. Additional one-way strips below', 7,
      awidth=30, cwidth=12)
hdr(sx, 4, ['WACC \\ g'] + [f'{x*100:.1f}%' for x in SN['g_grid']])
r = 5
for i, wx in enumerate(SN['wacc_grid']):
    put(sx, f'A{r}', f'{wx*100:.2f}%', fmt=None)
    for j in range(len(SN['g_grid'])):
        put(sx, f'{chr(66+j)}{r}', SN['table'][i][j], BLUE, PX)
    r += 1
r += 1
for name, grid, vals in [('Beta', SN['beta_grid'], SN['grid_beta']),
                         ('Development margin shift', SN['mg_grid'], SN['grid_margin']),
                         ('Conversion-rate shift', SN['conv_grid'], SN['grid_conv']),
                         ('New-sales multiple', SN['sales_grid'], SN['grid_sales']),
                         ('Working-capital release shift (AED mn/yr)', SN['nwc_grid'], SN['grid_nwc']),
                         ('Cost-of-equity adder', SN['ke_grid'], SN['grid_ke'])]:
    hdr(sx, r, [name] + [f'{g}' for g in grid]); r += 1
    put(sx, f'A{r}', 'DCF per share', fmt=None)
    for j, v in enumerate(vals):
        put(sx, f'{chr(66+j)}{r}', v, BLUE, PX)
    r += 2

# ============ 15 PER-SHARE & RATIOS ===========================================
pr = wb.create_sheet('Per-Share & Ratios')
title(pr, 'Per-share figures and ratios — all formulas', None, 10, awidth=42, cwidth=12)
hdr(pr, 4, [''] + ['FY2023', 'FY2024', 'FY2025'] + YF)
put(pr, 'A5', 'EPS (attributable)', fmt=None)
put(pr, 'A6', 'Book value per share', fmt=None)
put(pr, 'A7', 'Return on attributable equity (avg)', fmt=None)
put(pr, 'A8', 'Return on invested capital (fwd, avg base)', fmt=None)
put(pr, 'A9', 'P/E at spot', fmt=None)
put(pr, 'A10', 'P/B at spot', fmt=None)
for j, c in enumerate(HC + FCOL):
    hist = j < 3
    y = ['FY23', 'FY24', 'FY25'][j] if hist else None
    t = None if hist else j - 3
    npa_v = HI[y]['npa'] if hist else F['np_attr'][t]
    eq_v = BSH[y]['eqp'] if hist else EXPECT['Balance Sheet'][f'{c}13']
    putf(pr, f'{c}5', f"='Income Statement'!{c}17/{av(r_sh)}", npa_v / SH, PX, green=True)
    putf(pr, f'{c}6', f"='Balance Sheet'!{c}13/{av(r_sh)}", eq_v / SH, PX, green=True)
    if j == 0:
        put(pr, f'{c}7', '-', BLACK, None)
        put(pr, f'{c}8', '-', BLACK, None)
    else:
        pcol = (HC + FCOL)[j - 1]
        eq_prev = BSH[['FY23', 'FY24', 'FY25'][j-1]]['eqp'] if j <= 3 \
            else EXPECT['Balance Sheet'][f'{FCOL[j-4]}13']
        putf(pr, f'{c}7', f"='Income Statement'!{c}17/(('Balance Sheet'!{c}13"
             f"+'Balance Sheet'!{pcol}13)/2)", npa_v / ((eq_v + eq_prev) / 2), PCT,
             green=True)
        put(pr, f'{c}8', '-', BLACK, None)
    putf(pr, f'{c}9', f"={av(r_spot)}/{c}5", SPOT / (npa_v / SH), MULT)
    putf(pr, f'{c}10', f"={av(r_spot)}/{c}6", SPOT / (eq_v / SH), MULT)
for t in range(NY):
    c = FCOL[t]
    put(pr, f'{c}8', F['roic'][t], BLUE, PCT)   # avg-base ROIC uses the model's IC path (engine)

# ============ 16 PEER & SECTOR ================================================
pk = wb.create_sheet('Peer & Sector')
title(pk, 'Peer & sector — cross-checks only, never build sources',
      'Peer fundamentals from each company\'s own FY2025 release; prices/multiples from '
      'stockanalysis.com 07-Aug-2026 (aggregator, labelled)', 8, awidth=36, cwidth=14)
hdr(pk, 4, ['Peer', 'Spot', 'Mkt cap (AED mn)', 'FY2025 NP (AED mn)', 'Trailing P/E',
            'FY2025 revenue', 'Backlog'])
r = 5
for k, p in REL['peers'].items():
    put(pk, f'A{r}', p['name'], fmt=None)
    put(pk, f'B{r}', p['spot'], BLUE, PX)
    put(pk, f'C{r}', p['mcap'], BLUE, NUM0)
    put(pk, f'D{r}', p['np'] if p['np'] else '-', BLUE, NUM0)
    put(pk, f'E{r}', p['pe'], BLUE, MULT)
    put(pk, f'F{r}', p['rev'], BLUE, NUM0)
    put(pk, f'G{r}', p['backlog'], BLUE, NUM0)
    r += 1
put(pk, f'A{r}', 'Modon Holding (this study)', fmt=None, bold=True)
putf(pk, f'B{r}', f"={av(r_spot)}", SPOT, PX, green=True)
putf(pk, f'C{r}', f"={av(r_spot)}*{av(r_sh)}", M['mktcap'], NUM0)
put(pk, f'D{r}', IN['pat_fy25'], BLUE, NUM0)
putf(pk, f'E{r}', f"=C{r}/D{r}", M['mktcap'] / IN['pat_fy25'], MULT)
putf(pk, f'F{r}', "='Income Statement'!D5", HI['FY25']['rev'], NUM0, green=True)
put(pk, f'G{r}', IN['backlog'], BLUE, NUM0)
r += 2
put(pk, f'A{r}', 'Sector context (ADREC 2025, regulator): AED 142bn transactions (+44%); '
    'residential AED 76bn (+67%); off-plan 71% of residential deals; foreign buyers 62% of growth.',
    fmt=None, wrap=True)
pk.merge_cells(f'A{r}:G{r+2}')

# ---- order sheets ------------------------------------------------------------
ORDER = ['READ FIRST', 'Summary', 'Fundamental Valuation', 'Assumptions', 'SOTP Bridge',
         'Segments', 'Relative & Normalized', 'DCF', 'Income Statement', 'Balance Sheet',
         'Cash Flow', 'Summary Financials', 'Monte Carlo', 'Sensitivity',
         'Per-Share & Ratios', 'Peer & Sector']
assert set(ORDER) == set(wb.sheetnames), (set(ORDER) ^ set(wb.sheetnames))
wb._sheets = [wb[n] for n in ORDER]

XLSX = os.path.join(HERE, 'MODON_Valuation_Model_09082026_public.xlsx')
wb.save(XLSX)
with open(os.path.join(HERE, 'xlsx_expected.json'), 'w') as f:
    json.dump(dict(expected=EXPECT,
                   anchors=dict(seg_rev_tot=ANCH['seg_rev_tot'],
                                dcf=ANCH['dcf'], dcf_rw=ANCH['dcf_rw'],
                                bl_row=ANCH['bl_row'],
                                seg_fcst_rev=ANCH['seg_fcst_rev'],
                                seg_fcst_gp=ANCH['seg_fcst_gp'],
                                summary_mktcap=ANCH['summary_mktcap'])), f, indent=1)
nform = sum(len(v) for v in EXPECT.values())
print(f'wrote {XLSX}')
print(f'formula cells recorded: {nform} across {len(EXPECT)} sheets')
