"""Part 2: Segments and DCF — the GB Auto operating leg, built as a live formula model.

Nothing in this part changed construction in the 07-09-2026 rebuild: the auto leg was
already a units x ASP build discounted on the house cost-of-capital schedule, one forward
rate per explicit year with the terminal brought home on the same cumulative factor as the
last explicit year. What changed is that the forward rates are now marked as the INPUTS
they are and the first of them is reconciled against the WACC the Assumptions sheet builds
from rf* + beta x ERP, so a reader can see that the two agree rather than being told.

DISCLOSED HISTORY. Every FY2023-FY2025 figure on these sheets is company disclosure from
GB Corp's own 4Q23 / 4Q24 / 4Q25 earnings releases (committed under src/). Where the
study's committed numbers file carries the figure it is READ from there; the segment lines
it does not carry are marked in the block below and are the residue of this rebuild.
"""
import os as _os_pathfix
_HERE = _os_pathfix.path.dirname(_os_pathfix.path.abspath(__file__))
_os_pathfix.chdir(_HERE)
import sys as _sys_pathfix
_sys_pathfix.path.insert(0, _HERE)
_sys_pathfix.path.insert(0, _os_pathfix.path.join(_HERE, '..'))

import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

OUT = 'GBCO_Valuation_Model_07092026_public.xlsx'
wb = load_workbook(OUT)
A = json.load(open('_asm_rows.json'))
D = json.load(open('study_numbers.json'))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
NUM = '#,##0.0;(#,##0.0);"-"'; NUM0 = '#,##0;(#,##0);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%;(0.00%);"-"'; PX = '0.00'

_DD = D['disclosed_drivers']

# ---- DISCLOSED HISTORY -------------------------------------------------------------
# READ from the committed record wherever it carries the figure.
PC_VOL = [_DD['pc_volume_units'][y] for y in ('FY23', 'FY24', 'FY25')]
PC_REV = [_DD['pc_revenue'][y] for y in ('FY23', 'FY24', 'FY25')]
CV_VOL_FY25 = _DD['cv_volume_units']['FY25']; CV_REV_FY25 = _DD['cv_revenue']['FY25']
LM_VOL_FY25 = _DD['lm_volume_units']['FY25']; LM_REV_FY25 = _DD['lm_revenue']['FY25']
TR_REV_FY25 = _DD['trading_revenue']['FY25']
AUTO_REV_FY25 = _DD['auto_revenue_fy2025']
CAP_REV_FY25 = D['group_forecast']['drivers']['capital_revenue_fy2025']
GRP_REV = [D['history']['income_statement'][y]['revenue'] for y in ('2023', '2024', '2025')]
# THE RESIDUE, STATED RATHER THAN HIDDEN: the FY2023 and FY2024 segment splits and the auto
# leg's own historical gross profit, D&A and EBIT are in the company's releases and are NOT
# carried in this study's committed numbers file, so they are typed here from those releases
# with their source named. Closing this means adding them to the record the model computes
# from, which is a change to the study's own generator rather than to its workbook.
H_CV_VOL = [2273, 2096]; H_CV_REV = [2323.0, 3984.5]
H_LM_VOL = [13610, 20189]; H_LM_REV = [854.2, 1378.2]
H_TR_REV = [2506.8, 3815.5]
H_AUTO_REV = [23854.0, 47065.0]
H_CAP_REV = [4950.9, 7383.6]
H_AUTO_GP = [5813.1, 9057.4, 9837.1]
H_AUTO_EBIT = [3460.9, 5564.9, 5830.9]
H_AUTO_DNA = [374.3, 525.7, 683.3]
H_CAP_OP = [243.7, 380.1, 788.5]
H_CAP_NP = [1207.6, 1091.5, 1365.9]
H_CAP_BOOK = [8980.5, 13183.4, 19495.2]


def sheet(name):
    """Replace the sheet if it is already there. These parts run in order on one file, and a
    part re-run on its own used to APPEND a second copy under a suffixed name — a workbook
    that opens perfectly, carries every sheet twice and fails the sheet-list standard for a
    reason nothing in the run explains."""
    if name in wb.sheetnames:
        del wb[name]
    ws = wb.create_sheet(name); ws.title = name; return ws


def title(ws, text, sub=None, width=10):
    ws['A1'] = text; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, width + 1): ws.cell(row=1, column=c).fill = FILL_T
    if sub: ws['A2'] = sub; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 44
    for c in range(2, width + 1): ws.column_dimensions[get_column_letter(c)].width = 11.5


def put(ws, addr, v, font=BLACK, fmt=NUM, bold=False, fill=None):
    c = ws[addr]; c.value = v
    c.font = Font(color=(font.color if font else '000000'), bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill


def ac(label, col):
    return "Assumptions!$%s$%d" % (col, A[label])


YH = ['FY23', 'FY24', 'FY25']; YF = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
FCOLS = ['E', 'F', 'G', 'H', 'I']; ACOLS = ['C', 'D', 'E', 'F', 'G']

# ================= SEGMENTS ==================================================
ws = sheet('Segments')
title(ws, 'Segment view — the units x ASP build',
      'Volumes and average selling prices per line of business, FY23-FY30E. The forecast '
      'links to the drivers on Assumptions; nothing on this sheet is a hardcoded forecast.', 10)
for j, h in enumerate([''] + YH + YF):
    put(ws, '%s4' % get_column_letter(1 + j), h, BLACK, None, bold=True, fill=FILL_H)
SR = {}


def srow(r, label, hist, ffml=None, fmt=NUM, font_hist=BLUE, bold=False):
    SR[label] = r
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    for j, v in enumerate(hist):
        if v is not None:
            f = BLACK if (isinstance(v, str) and v.startswith('=')) else font_hist
            put(ws, '%s%d' % (get_column_letter(2 + j), r), v, f, fmt, bold=bold)
    if ffml:
        for j, col in enumerate(FCOLS):
            f = ffml(j, col)
            if f is not None:
                put(ws, '%s%d' % (col, r), f, BLACK, fmt, bold=bold)
    return r + 1


r = 6
r = srow(r, 'PC volume (units)', PC_VOL,
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['PC volume (units)'],
                                        ac('PC volume growth', ACOLS[j])), NUM0)
PCV = SR['PC volume (units)']
r = srow(r, 'PC revenue', PC_REV, None, NUM0)
PCR = SR['PC revenue']
r = srow(r, 'PC ASP (EGP mn/unit)',
         ['=B%d/B%d' % (PCR, PCV), '=C%d/C%d' % (PCR, PCV), '=D%d/D%d' % (PCR, PCV)],
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['PC ASP (EGP mn/unit)'],
                                        ac('PC ASP growth', ACOLS[j])), PX)
ASP = SR['PC ASP (EGP mn/unit)']
for j, c in enumerate(FCOLS):     # PC revenue forecast IS volume x price
    put(ws, '%s%d' % (c, PCR), "=%s%d*%s%d" % (c, PCV, c, ASP), BLACK, NUM0)
r = srow(r, 'CV&CE volume (units)', H_CV_VOL + [CV_VOL_FY25],
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['CV&CE volume (units)'],
                                        ac('CV&CE volume growth', ACOLS[j])), NUM0)
r = srow(r, 'CV&CE revenue', H_CV_REV + [CV_REV_FY25],
         lambda j, c: "=%s%d*(1+%s)*(1+%s)" % (chr(ord(c) - 1), SR['CV&CE revenue'],
                                               ac('CV&CE volume growth', ACOLS[j]),
                                               ac('CV&CE ASP growth', ACOLS[j])), NUM0)
r = srow(r, 'Light-Mobility volume (units)', H_LM_VOL + [LM_VOL_FY25],
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['Light-Mobility volume (units)'],
                                        ac('Light-Mobility volume growth', ACOLS[j])), NUM0)
r = srow(r, 'Light-Mobility revenue', H_LM_REV + [LM_REV_FY25],
         lambda j, c: "=%s%d*(1+%s)*(1+%s)" % (chr(ord(c) - 1), SR['Light-Mobility revenue'],
                                               ac('Light-Mobility volume growth', ACOLS[j]),
                                               ac('Light-Mobility ASP growth', ACOLS[j])), NUM0)
r = srow(r, 'Trading revenue (tires + parts)', H_TR_REV + [TR_REV_FY25],
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['Trading revenue (tires + parts)'],
                                        ac('Trading revenue growth', ACOLS[j])), NUM0)
# 'Other Auto' is the RESIDUAL against the disclosed segment total, so the column foots to
# the figure the company published rather than to the four lines this study models.
r = srow(r, 'Other Auto / after-sales & regional adj.',
         [None, None, None], lambda j, c: '=0', NUM0)
OTH = SR['Other Auto / after-sales & regional adj.']
# THE FIVE REVENUE LINES BY NAME, never a range: the volume and average-price rows sit
# between them, and a contiguous SUM would add units to pounds. It evaluates perfectly and
# is wrong by a multiple, which is the shape of error a total has to be built to refuse.
r = srow(r, 'GB Auto total revenue', H_AUTO_REV + [AUTO_REV_FY25],
         lambda j, c: "=%s%d+%s%d+%s%d+%s%d+%s%d"
         % (c, PCR, c, SR['CV&CE revenue'], c, SR['Light-Mobility revenue'],
            c, SR['Trading revenue (tires + parts)'], c, OTH), NUM0, bold=True)
AUTOR = SR['GB Auto total revenue']
for j, col in enumerate('BCD'):   # the residual, so the printed column foots to the total
    put(ws, '%s%d' % (col, OTH),
        "=%s%d-%s%d-%s%d-%s%d-%s%d" % (col, AUTOR, col, PCR, col, SR['CV&CE revenue'],
                                       col, SR['Light-Mobility revenue'],
                                       col, SR['Trading revenue (tires + parts)']), BLACK, NUM0)
r = srow(r, 'GB Capital revenue', H_CAP_REV + [CAP_REV_FY25],
         lambda j, c: "=%s%d*(1+%s)" % (chr(ord(c) - 1), SR['GB Capital revenue'],
                                        ac('GB Capital revenue growth', ACOLS[j])), NUM0)
CAPR = SR['GB Capital revenue']
r = srow(r, 'Intercompany eliminations', [None, None, None],
         lambda j, c: "=-(%s%d+%s%d)*%s" % (c, AUTOR, c, CAPR,
                                            ac('Intercompany eliminations (% of gross revenue)',
                                               ACOLS[j])), NUM0)
ELIM = SR['Intercompany eliminations']
r = srow(r, 'Group revenue', GRP_REV,
         lambda j, c: "=%s%d+%s%d+%s%d" % (c, AUTOR, c, CAPR, c, ELIM), NUM0, bold=True)
GRPR = SR['Group revenue']
for col in 'BCD':   # historically the eliminations are the residual against disclosed group revenue
    put(ws, '%s%d' % (col, ELIM), "=%s%d-%s%d-%s%d" % (col, GRPR, col, AUTOR, col, CAPR),
        BLACK, NUM0)
r += 1
r = srow(r, 'Auto gross profit', H_AUTO_GP,
         lambda j, c: "=%s%d*%s" % (c, AUTOR, ac('Auto gross margin', ACOLS[j])), NUM0)
AGP = SR['Auto gross profit']
r = srow(r, 'Auto gross margin',
         ['=B%d/B%d' % (AGP, AUTOR), '=C%d/C%d' % (AGP, AUTOR), '=D%d/D%d' % (AGP, AUTOR)],
         lambda j, c: "=%s%d/%s%d" % (c, AGP, c, AUTOR), PCT2)
r = srow(r, 'Auto EBIT (operating profit)', H_AUTO_EBIT,
         lambda j, c: "=%s%d-%s%d*%s+%s%d*%s+%s%d*%s"
         % (c, AGP, c, AUTOR, ac('Auto GS&A (% of revenue)', ACOLS[j]),
            c, AUTOR, ac('Auto other operating income (% rev)', ACOLS[j]),
            c, AUTOR, ac('Auto provisions (% rev)', ACOLS[j])), NUM0)
AEBIT = SR['Auto EBIT (operating profit)']
r = srow(r, 'Auto D&A', H_AUTO_DNA,
         lambda j, c: "=%s%d*%s" % (c, AUTOR, ac('Auto D&A (% of revenue)', ACOLS[j])), NUM0)
ADNA = SR['Auto D&A']
r = srow(r, 'Auto EBITDA',
         ['=B%d+B%d' % (AEBIT, ADNA), '=C%d+C%d' % (AEBIT, ADNA), '=D%d+D%d' % (AEBIT, ADNA)],
         lambda j, c: "=%s%d+%s%d" % (c, AEBIT, c, ADNA), NUM0)
AEBITDA = SR['Auto EBITDA']
r = srow(r, 'Auto EBITDA margin',
         ['=B%d/B%d' % (AEBITDA, AUTOR), '=C%d/C%d' % (AEBITDA, AUTOR),
          '=D%d/D%d' % (AEBITDA, AUTOR)],
         lambda j, c: "=%s%d/%s%d" % (c, AEBITDA, c, AUTOR), PCT2)
r = srow(r, 'GB Capital operating profit', H_CAP_OP, None, NUM0)
r = srow(r, 'GB Capital net profit (after NCI)', H_CAP_NP, None, NUM0)
r = srow(r, 'GB Capital on-book loan portfolio', H_CAP_BOOK, None, NUM0)
r += 1
put(ws, 'A%d' % r,
    'GB Auto 1H2026 reviewed gross margin — the forecast anchor', BLACK, None)
put(ws, 'B%d' % r, D['forecast_anchor']['latest_reviewed_rate'], BLUE, PCT2)
SR['GB Auto 1H2026 reviewed gross margin — the forecast anchor'] = r
put(ws, 'C%d' % r,
    'The latest reviewed period, from the segment income statement in the 2Q26 release: '
    'revenue 40,021.5 and gross profit 5,722.1. The forecast OPENS BELOW it, at %.2f%%, '
    'and the gap is 3.5%% relative — inside the 5%% materiality line, so no mechanism is '
    'claimed for it.' % (D['forecast_anchor']['first_forecast_rate'] * 100), SUB, None)
r += 1
put(ws, 'A%d' % r,
    'Source: GB Corp 4Q23 / 4Q24 / 4Q25 earnings releases. "Other Auto" is the residual '
    'against the disclosed segment total, so each historical column foots to the revenue '
    'the company published; it is set to zero in the forecast, which is conservative. '
    'Historical eliminations are likewise the residual against disclosed group revenue.',
    SUB, None)
json.dump(SR, open('_seg_rows.json', 'w'), indent=1, sort_keys=True)

# ================= DCF (the GB Auto operating leg) ===========================
ws = sheet('DCF')
title(ws, 'DCF — GB Auto operating leg, explicit five-year free cash flow to the firm',
      'Revenue -> EBITDA -> D&A -> EBIT -> NOPAT -> +D&A -> -capex -> -change in working '
      'capital -> FCFF -> discount factor -> present value. Links to Segments, the Balance '
      'Sheet and Assumptions.', 8)
for j, y in enumerate(YF):
    put(ws, '%s4' % get_column_letter(2 + j), y, BLACK, None, bold=True, fill=FILL_H)
DC = {}


def drow(r, label, fml, fmt=NUM0, bold=False, font=None):
    DC[label] = r
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    for j in range(5):
        c = get_column_letter(2 + j)
        f = fml(j, c)
        fo = font or (GREEN if 'Segments!' in str(f) or 'Balance Sheet' in str(f) else BLACK)
        put(ws, '%s%d' % (c, r), f, fo, fmt, bold=bold)
    return r + 1


r = 6
r = drow(r, 'Auto revenue', lambda j, c: "=Segments!%s%d" % (FCOLS[j], AUTOR))
r = drow(r, 'EBITDA', lambda j, c: "=Segments!%s%d" % (FCOLS[j], AEBITDA))
r = drow(r, 'D&A', lambda j, c: "=-Segments!%s%d" % (FCOLS[j], ADNA))
r = drow(r, 'EBIT', lambda j, c: "=Segments!%s%d" % (FCOLS[j], AEBIT))
r = drow(r, 'NOPAT = EBIT x (1 - tax)',
         lambda j, c: "=%s%d*(1-Assumptions!$B$7)" % (c, DC['EBIT']))
r = drow(r, '+ D&A', lambda j, c: "=Segments!%s%d" % (FCOLS[j], ADNA))
r = drow(r, '- Capex', lambda j, c: "=-%s" % ac('Auto capex (EGP mn)', ACOLS[j]))
r = drow(r, '- Increase in net working capital',
         lambda j, c: "='Balance Sheet'!%s40*-1" % FCOLS[j])   # re-pointed in part 3
DWC = DC['- Increase in net working capital']
r = drow(r, 'FCFF', lambda j, c: "=SUM(%s%d:%s%d)"
         % (c, DC['NOPAT = EBIT x (1 - tax)'], c, DWC), bold=True)
FCFF = DC['FCFF']
# ONE FORWARD RATE PER YEAR, NOT ONE RATE COMPOUNDED FIVE TIMES. Discounting a five-year
# forecast and a perpetuity alike at one crisis-level rate asserts that this economy's cost
# of capital never normalises, against the central bank's own published disinflation path.
_SCH = D['cost_of_capital_record']
r = drow(r, "Cost of capital — this year's forward rate",
         lambda j, c: _SCH['forward_wacc'][j], PCT2, font=BLUE)
FWD = DC["Cost of capital — this year's forward rate"]
r = drow(r, 'Discount factor (cumulative on the schedule)',
         lambda j, c: ("=1/(1+%s%d)" % (c, FWD) if j == 0
                       else "=%s%d/(1+%s%d)" % (get_column_letter(1 + j), r, c, FWD)), '0.0000')
DF = DC['Discount factor (cumulative on the schedule)']
r = drow(r, 'PV of FCFF', lambda j, c: "=%s%d*%s%d" % (c, FCFF, c, DF), bold=True)
PVR = DC['PV of FCFF']
r += 1


def dline(r, label, f, fmt=NUM0, bold=False, note=None, font=BLACK):
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    put(ws, 'B%d' % r, f, font, fmt, bold=bold)
    if note: put(ws, 'C%d' % r, note, SUB, None)
    DC[label] = r
    return r + 1


r = dline(r, 'Sum of the present values, FY26-30E', "=SUM(B%d:F%d)" % (PVR, PVR), bold=True)
SPV = r - 1
r = dline(r, 'Cost of capital — terminal (norm-built)', _SCH['wacc_terminal'], PCT2,
          font=BLUE,
          note='the norm-built terminal rate the schedule glides to; the terminal is brought '
               'home on the SAME cumulative factor as the last explicit year — one date, one '
               'price of time.')
WTR = r - 1
r = dline(r, 'Terminal value (on the terminal rate)',
          "=F%d*(1+Assumptions!$B$17)/(B%d-Assumptions!$B$17)" % (FCFF, WTR))
TVR = r - 1
r = dline(r, 'PV of the terminal value', "=B%d*F%d" % (TVR, DF))
PVT = r - 1
r = dline(r, 'Enterprise value — GB Auto leg', "=B%d+B%d" % (SPV, PVT), bold=True)
EVR = r - 1
r = dline(r, 'Terminal share of enterprise value', "=B%d/B%d" % (PVT, EVR), PCT2)
r = dline(r, 'less: GB Auto net debt (30 June 2026)', '=-Assumptions!$B$19')
r = dline(r, 'less: GB Auto non-controlling interests', '=-Assumptions!$B$20')
r = dline(r, 'GB Auto equity value', "=B%d-Assumptions!$B$19-Assumptions!$B$20" % EVR,
          bold=True)
AEQ = r - 1
r += 1
r = dline(r, 'check: year-1 forward rate less the WACC built on Assumptions',
          "=B%d-Assumptions!$B$16" % FWD, PCT2,
          note='ZERO by construction: the schedule\'s first year and rf* + beta x ERP blended '
               'with after-tax debt are the same rate, and this row is what says so.')
r = dline(r, 'Enterprise value per +1pp of Auto gross margin (helper)',
          "=0.01*(1-Assumptions!$B$7)*(SUMPRODUCT(B%d:F%d,B%d:F%d)"
          "+F%d*(1+Assumptions!$B$17)/(B%d-Assumptions!$B$17)*F%d)"
          % (DC['Auto revenue'], DC['Auto revenue'], DF, DF, DC['Auto revenue'], WTR, DF),
          note='EXACT rather than approximate: a margin shift moves cost only, so it moves '
               'every year\'s free cash flow by revenue x shift x (1 - tax) and nothing else. '
               'The Sensitivity sheet is built on this row.')
EVPP = r - 1
put(ws, 'A%d' % (r + 1),
    'The discount factors are the cost-of-capital schedule\'s own cumulative factors. The '
    'terminal growth rate on the Assumptions sheet is stored as a REAL rate on the house '
    'Egyptian inflation path and recomputed to its nominal value.', SUB, None)
json.dump(dict(DC=DC, SPV=SPV, TVR=TVR, PVT=PVT, EVR=EVR, AEQ=AEQ, EVPP=EVPP,
               FCFF=FCFF, DF=DF, FWD=FWD, WTR=WTR), open('_dcf_rows.json', 'w'),
          indent=1, sort_keys=True)
wb.save(OUT)
print('part2 ok — Segments + DCF; auto revenue row %d, auto equity row %d' % (AUTOR, AEQ))
