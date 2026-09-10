"""Part 3: Income Statement, Balance Sheet and Cash Flow — the clean-surplus construction.

The historical income statement is now READ from the study's committed record rather than
typed into this builder. That is not cosmetic: the superseded builder carried FY2023 gross
profit of 6,884.3 against a committed 6,884.5, other income of 518.8 against 523.2 and an
EBIT of 4,769.5 against 4,769.7 — small, and the document and the workbook were therefore
two separate transcriptions of one arithmetic with nothing comparing them.

ONE DEFINITION DOWN THE COLUMN. GB Corp's own releases print FY2023 and FY2024 operating
profit BEFORE provisions and FY2025 AFTER them. A reader adding the printed rows has to
arrive at the printed total, so operating profit is computed here from the components
printed above it, on one definition for all three years, and the difference from the
company's own caption is stated below the table rather than absorbed silently.
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

import json as _json_ed, os as _os_ed
_ED = _json_ed.load(open(_os_ed.path.join(
    _os_ed.path.dirname(_os_ed.path.abspath(__file__)),
    'study_numbers.json'), encoding='utf-8'))['edition']
OUT = 'GBCO_Valuation_Model_%s_public.xlsx' % ''.join(_ED.split('-')[::-1])
wb = load_workbook(OUT)
A = json.load(open('_asm_rows.json')); SR = json.load(open('_seg_rows.json'))
DCJ = json.load(open('_dcf_rows.json'))
D = json.load(open('study_numbers.json'))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
NUM0 = '#,##0;(#,##0);"-"'; PCT2 = '0.00%;(0.00%);"-"'
YH = ['FY23', 'FY24', 'FY25']; YF = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
FCOLS = ['E', 'F', 'G', 'H', 'I']; ACOLS = ['C', 'D', 'E', 'F', 'G']
AUTOR, CAPR, GRPR = SR['GB Auto total revenue'], SR['GB Capital revenue'], SR['Group revenue']
AGP, AEBIT, ADNA = (SR['Auto gross profit'], SR['Auto EBIT (operating profit)'],
                    SR['Auto D&A'])
HIS = D['history']['income_statement']
HY = ('2023', '2024', '2025')
INP = D['inputs']


def h(field):
    return [HIS[y][field] for y in HY]


def sheet(n):
    """Replace the sheet if it is already there. These parts run in order on one file, and a
    part re-run on its own used to APPEND a second copy under a suffixed name — a workbook
    that opens perfectly, carries every sheet twice and fails the sheet-list standard for a
    reason nothing in the run explains."""
    if n in wb.sheetnames:
        del wb[n]
    ws = wb.create_sheet(n); ws.title = n; return ws


def title(ws, t, s=None, w=10):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1): ws.cell(row=1, column=c).fill = FILL_T
    if s: ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 46
    for c in range(2, w + 1): ws.column_dimensions[get_column_letter(c)].width = 11.5


def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None):
    c = ws[ad]; c.value = v; c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill


def ac(label, j):
    return "Assumptions!$%s$%d" % (ACOLS[j], A[label])


# ================= INCOME STATEMENT =========================================
ws = sheet('Income Statement')
title(ws, 'Income statement (EGP mn, consolidated)',
      'FY23-FY25 as reported (blue, read from the study record); FY26E-FY30E formulas '
      'linking to Segments and to the drivers on Assumptions.', 10)
for j, hh in enumerate([''] + YH + YF):
    put(ws, '%s4' % get_column_letter(1 + j), hh, BLACK, None, bold=True, fill=FILL_H)
IS = {}


def irow(r, label, hist, ffml=None, fmt=NUM0, hfont=BLUE, bold=False):
    IS[label] = r
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    for j, v in enumerate(hist):
        if v is not None:
            f = BLACK if (isinstance(v, str) and v.startswith('=')) else hfont
            put(ws, '%s%d' % (get_column_letter(2 + j), r), v, f, fmt, bold=bold)
    if ffml:
        for j, c in enumerate(FCOLS):
            f = ffml(j, c)
            if f is not None:
                put(ws, '%s%d' % (c, r), f,
                    GREEN if 'Segments!' in str(f) else BLACK, fmt, bold=bold)
    return r + 1


r = 6
r = irow(r, 'GB Auto revenue', [None] * 3, lambda j, c: "=Segments!%s%d" % (c, AUTOR))
for j, col in enumerate('BCD'):
    put(ws, '%s%d' % (col, IS['GB Auto revenue']), "=Segments!%s%d" % (col, AUTOR), GREEN, NUM0)
r = irow(r, 'GB Capital revenue', [None] * 3, lambda j, c: "=Segments!%s%d" % (c, CAPR))
for j, col in enumerate('BCD'):
    put(ws, '%s%d' % (col, IS['GB Capital revenue']), "=Segments!%s%d" % (col, CAPR), GREEN, NUM0)
r = irow(r, 'Intercompany eliminations', [None] * 3,
         lambda j, c: "=Segments!%s%d" % (c, SR['Intercompany eliminations']))
for j, col in enumerate('BCD'):
    put(ws, '%s%d' % (col, IS['Intercompany eliminations']),
        "=Segments!%s%d" % (col, SR['Intercompany eliminations']), GREEN, NUM0)
r = irow(r, 'Total revenue', [None] * 3,
         lambda j, c: "=SUM(%s%d:%s%d)" % (c, IS['GB Auto revenue'],
                                           c, IS['Intercompany eliminations']), bold=True)
REV = IS['Total revenue']
for col in 'BCD':
    put(ws, '%s%d' % (col, REV), "=SUM(%s%d:%s%d)"
        % (col, IS['GB Auto revenue'], col, IS['Intercompany eliminations']), BLACK, NUM0, True)
r = irow(r, 'Gross profit', h('gross_profit'),
         lambda j, c: "=Segments!%s%d+Segments!%s%d*%s+Segments!%s%d*0.2"
         % (c, AGP, c, CAPR, ac('GB Capital gross margin', j), c,
            SR['Intercompany eliminations']))
GP = IS['Gross profit']
r = irow(r, 'Gross profit margin',
         ['=B%d/B%d' % (GP, REV), '=C%d/C%d' % (GP, REV), '=D%d/D%d' % (GP, REV)],
         lambda j, c: "=%s%d/%s%d" % (c, GP, c, REV), PCT2)
r = irow(r, 'Selling, marketing & administration',
         [HIS[y]['selling'] + HIS[y]['admin'] for y in HY],
         lambda j, c: "=-%s%d*%s" % (c, REV, ac('Group opex S&M+Admin (% of group rev)', j)))
r = irow(r, 'Other operating income', h('other_income'),
         lambda j, c: "=%s%d*%s" % (c, REV, ac('Group other income (% of group rev)', j)))
r = irow(r, 'Provisions (net)', h('provisions'),
         lambda j, c: "=%s%d*%s" % (c, REV, ac('Group provisions (% of group rev)', j)))
# GROSS PROFIT PLUS THE THREE ROWS BELOW IT, and not SUM(gp, range): the gross-margin row
# sits between them, so a single contiguous range would sweep a percentage into a total.
r = irow(r, 'Operating profit', [None] * 3,
         lambda j, c: "=%s%d+SUM(%s%d:%s%d)"
         % (c, GP, c, IS['Selling, marketing & administration'], c, IS['Provisions (net)']),
         bold=True)
OP = IS['Operating profit']
for col in 'BCD':
    put(ws, '%s%d' % (col, OP), "=%s%d+SUM(%s%d:%s%d)"
        % (col, GP, col, IS['Selling, marketing & administration'],
           col, IS['Provisions (net)']), BLACK, NUM0, True)
r = irow(r, 'Investment gains from associates', h('associates'),
         lambda j, c: "=%s" % ac('Associates income (EGP mn)', j))
r = irow(r, 'EBIT', [None] * 3,
         lambda j, c: "=%s%d+%s%d" % (c, OP, c, IS['Investment gains from associates']),
         bold=True)
EBIT = IS['EBIT']
for col in 'BCD':
    put(ws, '%s%d' % (col, EBIT), "=%s%d+%s%d"
        % (col, OP, col, IS['Investment gains from associates']), BLACK, NUM0, True)
# Group depreciation: the FY2025 figure is the audited consolidated cash-flow line and is
# committed; FY2023 and FY2024 are NOT carried in this study's record and are left EMPTY
# rather than invented (SIGCM clause 8 — a missing item is recorded as missing).
r = irow(r, 'Group D&A', [None, None, INP['dep_fy2025']['value']],
         lambda j, c: "=Segments!%s%d+%s" % (c, ADNA, ac('GB Capital D&A (EGP mn)', j)))
DNA = IS['Group D&A']
r = irow(r, 'EBITDA (EBIT + D&A)', [None, None, '=D%d+D%d' % (EBIT, DNA)],
         lambda j, c: "=%s%d+%s%d" % (c, EBIT, c, DNA))
EBITDA = IS['EBITDA (EBIT + D&A)']
r = irow(r, 'Foreign exchange gains (losses)', h('fx'), lambda j, c: '=0')
r = irow(r, 'Net finance cost', h('finance_net'),
         lambda j, c: "=%s" % ac('Net finance cost (EGP mn)', j))
r = irow(r, 'Earnings before tax', [None] * 3,
         lambda j, c: "=%s%d+%s%d+%s%d"
         % (c, EBIT, c, IS['Foreign exchange gains (losses)'], c, IS['Net finance cost']),
         bold=True)
EBT = IS['Earnings before tax']
for col in 'BCD':
    put(ws, '%s%d' % (col, EBT), "=%s%d+%s%d+%s%d"
        % (col, EBIT, col, IS['Foreign exchange gains (losses)'],
           col, IS['Net finance cost']), BLACK, NUM0, True)
r = irow(r, 'Income taxes', h('tax'), lambda j, c: "=-%s%d*Assumptions!$B$7" % (c, EBT))
r = irow(r, 'Net profit before minority interest', [None] * 3,
         lambda j, c: "=%s%d+%s%d" % (c, EBT, c, IS['Income taxes']), bold=True)
NPBM = IS['Net profit before minority interest']
for col in 'BCD':
    put(ws, '%s%d' % (col, NPBM), "=%s%d+%s%d" % (col, EBT, col, IS['Income taxes']),
        BLACK, NUM0, True)
r = irow(r, 'Minority interest', h('minority'),
         lambda j, c: "=%s%d*%s" % (c, NPBM, ac('Minority interest (% of NP before MI)', j)))
r = irow(r, 'Net profit (attributable)', [None] * 3,
         lambda j, c: "=%s%d+%s%d" % (c, NPBM, c, IS['Minority interest']), bold=True)
NP = IS['Net profit (attributable)']
for col in 'BCD':
    put(ws, '%s%d' % (col, NP), "=%s%d+%s%d" % (col, NPBM, col, IS['Minority interest']),
        BLACK, NUM0, True)
r = irow(r, 'Net profit margin',
         ['=B%d/B%d' % (NP, REV), '=C%d/C%d' % (NP, REV), '=D%d/D%d' % (NP, REV)],
         lambda j, c: "=%s%d/%s%d" % (c, NP, c, REV), PCT2)
put(ws, 'A%d' % (r + 1),
    'Source: GB Corp 4Q23 / 4Q24 / 4Q25 earnings releases, group income statement and the '
    'segment income statement, read from this study\'s committed record. Operating profit '
    'is computed AFTER provisions in all three years so that the column foots on one '
    'definition; the company\'s own FY2023 and FY2024 captions state it before provisions, '
    'which is why its printed figure for those two years is higher by the provisions line '
    'directly above. Group depreciation for FY2023 and FY2024 is not carried in the study\'s '
    'record and is left empty rather than estimated.', SUB, None)
json.dump(IS, open('_is_rows.json', 'w'), indent=1, sort_keys=True)

# ================= BALANCE SHEET ============================================
ws = sheet('Balance Sheet')
title(ws, 'Balance sheet (EGP mn, consolidated)',
      'FY23-FY25 grouped from the disclosed segment balance sheets to a house layout (blue). '
      'The forecast rolls forward and the check row is zero by clean-surplus construction.', 10)
for j, hh in enumerate([''] + YH + YF):
    put(ws, '%s4' % get_column_letter(1 + j), hh, BLACK, None, bold=True, fill=FILL_H)
BS = {}


def brow(r, label, hist, ffml=None, fmt=NUM0, hfont=BLUE, bold=False):
    BS[label] = r
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    for j, v in enumerate(hist):
        if v is not None:
            f = BLACK if (isinstance(v, str) and v.startswith('=')) else hfont
            put(ws, '%s%d' % (get_column_letter(2 + j), r), v, f, fmt, bold=bold)
    if ffml:
        for j, c in enumerate(FCOLS):
            f = ffml(j, c)
            if f is not None:
                put(ws, '%s%d' % (c, r), f,
                    GREEN if ('Cash Flow' in str(f) or 'Income' in str(f)
                              or 'Segments' in str(f)) else BLACK, fmt, bold=bold)
    return r + 1


r = 6
r = brow(r, 'PP&E, intangibles, right-of-use & investment property', [6937.4, 10360.6, 13389.1],
         lambda j, c: "=%s%d+%s+%s-'Income Statement'!%s%d"
         % (chr(ord(c) - 1), BS['PP&E, intangibles, right-of-use & investment property'],
            ac('Auto capex (EGP mn)', j), ac('Rental-fleet & other capex (EGP mn)', j), c, DNA))
r = brow(r, 'Investments in associates (MNT-Halan, Bedaya, Kaf)', [10732.4, 11743.6, 13689.5],
         lambda j, c: "=%s%d+%s"
         % (chr(ord(c) - 1), BS['Investments in associates (MNT-Halan, Bedaya, Kaf)'],
            ac('Associates income (EGP mn)', j)))
r = brow(r, 'GB Capital loan book (on balance sheet)', [7681.4, 11483.0, 17518.3],
         lambda j, c: "=%s%d*(1+%s)"
         % (chr(ord(c) - 1), BS['GB Capital loan book (on balance sheet)'],
            ac('GB Capital loan-book growth', j)))
r = brow(r, 'Inventories', [6366.1, 21134.3, 24649.7],
         lambda j, c: "=Segments!%s%d*%s" % (c, AUTOR, ac('Auto inventory (% of Auto rev)', j)))
r = brow(r, 'Trade receivables — Auto', [1743.5, 3708.7, 5316.9],
         lambda j, c: "=Segments!%s%d*%s" % (c, AUTOR, ac('Auto receivables (% of Auto rev)', j)))
r = brow(r, 'Advances, debtors & other current', [1039.1, 2942.2, 4670.6],
         lambda j, c: "=Segments!%s%d*%s" % (c, AUTOR, ac('Auto advances & debtors (% rev)', j)))
r = brow(r, 'Cash & cash equivalents', [4504.2, 7420.9, INP['cash_dec2025']['value']],
         lambda j, c: "='Cash Flow'!%s22" % c)      # re-pointed once the CF rows are known
CASH = BS['Cash & cash equivalents']
r = brow(r, 'Other assets (deferred tax, held-for-sale, miscellaneous)', [3581.4, 3931.9, 2601.3],
         lambda j, c: "=%s%d" % (chr(ord(c) - 1),
                                 BS['Other assets (deferred tax, held-for-sale, miscellaneous)']))
LASTA = BS['Other assets (deferred tax, held-for-sale, miscellaneous)']
r = brow(r, 'TOTAL ASSETS', [None] * 3,
         lambda j, c: "=SUM(%s%d:%s%d)"
         % (c, BS['PP&E, intangibles, right-of-use & investment property'], c, LASTA),
         NUM0, BLACK, True)
TA = BS['TOTAL ASSETS']
for col in 'BCD':
    put(ws, '%s%d' % (col, TA), "=SUM(%s%d:%s%d)"
        % (col, BS['PP&E, intangibles, right-of-use & investment property'], col, LASTA),
        BLACK, NUM0, True)
r += 1
r = brow(r, 'Equity attributable to shareholders', [19838.8, 25438.5, 28788.7], None)
EQ = BS['Equity attributable to shareholders']
r = brow(r, 'Non-controlling interests', [1363.0, 1978.4, 1801.4],
         lambda j, c: "=%s%d-'Income Statement'!%s%d"
         % (chr(ord(c) - 1), BS['Non-controlling interests'], c, IS['Minority interest']))
r = brow(r, 'Total equity', [None] * 3,
         lambda j, c: "=%s%d+%s%d" % (c, EQ, c, BS['Non-controlling interests']),
         NUM0, BLACK, True)
TEQ = BS['Total equity']
for col in 'BCD':
    put(ws, '%s%d' % (col, TEQ), "=%s%d+%s%d" % (col, EQ, col, BS['Non-controlling interests']),
        BLACK, NUM0, True)
r = brow(r, 'Borrowings (loans, overdrafts & bonds)',
         [12517.7, 22608.7, INP['debt_dec2025']['value']],
         lambda j, c: "=%s%d+%s" % (chr(ord(c) - 1), BS['Borrowings (loans, overdrafts & bonds)'],
                                    ac('Increase in borrowings, net (EGP mn)', j)))
r = brow(r, 'Trade & notes payables', [7398.7, 19717.6, 18436.5], None)
PAY = BS['Trade & notes payables']
r = brow(r, 'Lease obligations', [371.3, 1123.8, 1554.3],
         lambda j, c: "=%s%d" % (chr(ord(c) - 1), BS['Lease obligations']))
r = brow(r, 'Provisions', [347.7, 709.9, 794.9],
         lambda j, c: "=%s%d" % (chr(ord(c) - 1), BS['Provisions']))
r = brow(r, 'Other liabilities', [415.2, 746.2, 1178.2],
         lambda j, c: "=%s%d" % (chr(ord(c) - 1), BS['Other liabilities']))
r = brow(r, 'Deferred tax liabilities', [333.1, 402.0, 763.5],
         lambda j, c: "=%s%d" % (chr(ord(c) - 1), BS['Deferred tax liabilities']))
DTL = BS['Deferred tax liabilities']
r = brow(r, 'TOTAL EQUITY & LIABILITIES', [None] * 3, None, NUM0, BLACK, True)
TLE = BS['TOTAL EQUITY & LIABILITIES']
for col in list('BCD') + FCOLS:
    put(ws, '%s%d' % (col, TLE), "=%s%d+SUM(%s%d:%s%d)"
        % (col, TEQ, col, BS['Borrowings (loans, overdrafts & bonds)'], col, DTL),
        BLACK, NUM0, True)
r += 1
# THE CHECK ROW IS NOT ASSERTED TO BE ZERO, IT IS ASSERTED TO BE CONSTANT, and the
# difference is the honest one. The company's own grouped segment balance sheets carry a
# 0.1 rounding at FY2024 and FY2025 — its disclosed total equity is one decimal above the
# sum of its two disclosed components — and a builder that made that vanish would be
# editing a disclosed figure to make its own check look better. It carries forward
# unchanged, which is exactly what a clean-surplus forecast does with an opening
# difference: every year of the forecast closes, and this row says so by not moving.
r = brow(r, 'Balance check (assets less equity & liabilities) — constant, never growing', [None] * 3,
         lambda j, c: "=%s%d-%s%d" % (c, TA, c, TLE), NUM0, BLACK, True)
CHK = BS['Balance check (assets less equity & liabilities) — constant, never growing']
for col in 'BCD':
    put(ws, '%s%d' % (col, CHK), "=%s%d-%s%d" % (col, TA, col, TLE), BLACK, NUM0, True)
r = brow(r, 'Group net debt (borrowings less cash)', [None] * 3,
         lambda j, c: "=%s%d-%s%d" % (c, BS['Borrowings (loans, overdrafts & bonds)'], c, CASH),
         NUM0, BLACK)
ND = BS['Group net debt (borrowings less cash)']
for col in 'BCD':
    put(ws, '%s%d' % (col, ND), "=%s%d-%s%d"
        % (col, BS['Borrowings (loans, overdrafts & bonds)'], col, CASH), BLACK, NUM0)
r += 1
# The non-Auto payables block was a numeral typed INSIDE two formulas in the superseded
# builder. It is an input, so it is an input cell.
put(ws, 'A%d' % r, 'memo: non-Auto trade payables, held flat across the forecast')
put(ws, 'B%d' % r, 2716.3, BLUE, NUM0)
put(ws, 'C%d' % r, 'the payables block that does not move with Auto revenue; held flat, '
                   'which is conservative for working capital.', SUB, None)
BS['memo: non-Auto trade payables, held flat across the forecast'] = r
NONAUTO = r
r += 1
for j, c in enumerate(FCOLS):
    put(ws, '%s%d' % (c, PAY), "=Segments!%s%d*%s+$B$%d"
        % (c, AUTOR, ac('Auto payables (% of Auto rev)', j), NONAUTO), BLACK, NUM0)
r = brow(r, 'Net Auto working capital (inventory + receivables + advances less payables)',
         [None] * 3,
         lambda j, c: "=%s%d+%s%d+%s%d-(%s%d-$B$%d)"
         % (c, BS['Inventories'], c, BS['Trade receivables — Auto'],
            c, BS['Advances, debtors & other current'], c, PAY, NONAUTO), NUM0, BLACK)
NWC = BS['Net Auto working capital (inventory + receivables + advances less payables)']
for col in 'BCD':
    put(ws, '%s%d' % (col, NWC), "=%s%d+%s%d+%s%d-(%s%d-$B$%d)"
        % (col, BS['Inventories'], col, BS['Trade receivables — Auto'],
           col, BS['Advances, debtors & other current'], col, PAY, NONAUTO), BLACK, NUM0)
r = brow(r, 'Increase in net Auto working capital', [None] * 3,
         lambda j, c: "=%s%d-%s%d" % (c, NWC, chr(ord(c) - 1), NWC), NUM0, BLACK)
DNWC = BS['Increase in net Auto working capital']
put(ws, 'A%d' % (r + 1),
    'Historic mapping note: lines grouped from the disclosed 4Q23 / 4Q24 / 4Q25 segment '
    'balance sheets to one house layout. "GB Capital loan book (on balance sheet)" is notes '
    'receivable plus GB Capital trade receivables net of eliminations; the portfolio metric '
    'the company reports differs by provisions and presentation. Cash at 31-Dec-2025 and '
    'borrowings at 31-Dec-2025 are read from the study\'s committed input register.',
    SUB, None)
json.dump(dict(BS=BS, NWC=NWC, DNWC=DNWC, CASH=CASH, EQ=EQ, TA=TA, TLE=TLE, CHK=CHK, ND=ND,
               NONAUTO=NONAUTO, PAY=PAY),
          open('_bs_rows.json', 'w'), indent=1, sort_keys=True)

# the DCF's change-in-working-capital row now points at the row that carries it
dws = wb['DCF']; DC = DCJ['DC']
for j, c in enumerate(['B', 'C', 'D', 'E', 'F']):
    cell = '%s%d' % (c, DC['- Increase in net working capital'])
    dws[cell] = "=-'Balance Sheet'!%s%d" % (FCOLS[j], DNWC)
    dws[cell].font = GREEN

# ================= CASH FLOW =================================================
ws = sheet('Cash Flow')
title(ws, 'Cash flow (EGP mn, forecast)',
      'Derived from the Income Statement and the Balance Sheet. Closing cash ties back to '
      'the Balance Sheet, and every balance-sheet movement is captured, so the balance '
      'check on that sheet is zero.', 10)
for j, hh in enumerate([''] + YF):
    put(ws, '%s4' % get_column_letter(4 + j), hh, BLACK, None, bold=True, fill=FILL_H)
CF = {}


def crow(r, label, ffml, fmt=NUM0, bold=False):
    CF[label] = r
    put(ws, 'A%d' % r, label, BLACK, None, bold=bold)
    for j, c in enumerate(FCOLS):
        f = ffml(j, c)
        if f is not None:
            put(ws, '%s%d' % (c, r), f, GREEN if '!' in str(f) else BLACK, fmt, bold=bold)
    return r + 1


r = 6
r = crow(r, 'Net profit before minority interest', lambda j, c: "='Income Statement'!%s%d" % (c, NPBM))
r = crow(r, '+ D&A', lambda j, c: "='Income Statement'!%s%d" % (c, DNA))
r = crow(r, '- Associates income (non-cash)',
         lambda j, c: "=-'Income Statement'!%s%d" % (c, IS['Investment gains from associates']))
r = crow(r, '- Increase in net Auto working capital',
         lambda j, c: "=-'Balance Sheet'!%s%d" % (c, DNWC))
r = crow(r, '- Increase in the GB Capital loan book',
         lambda j, c: "=-('Balance Sheet'!%s%d-'Balance Sheet'!%s%d)"
         % (c, BS['GB Capital loan book (on balance sheet)'],
            chr(ord(c) - 1), BS['GB Capital loan book (on balance sheet)']))
r = crow(r, 'Operating cash flow',
         lambda j, c: "=SUM(%s%d:%s%d)" % (c, CF['Net profit before minority interest'],
                                           c, CF['- Increase in the GB Capital loan book']),
         bold=True)
r = crow(r, '- Capex (Auto + rental fleet)',
         lambda j, c: "=-%s-%s" % (ac('Auto capex (EGP mn)', j),
                                   ac('Rental-fleet & other capex (EGP mn)', j)))
r = crow(r, 'Free cash flow',
         lambda j, c: "=%s%d+%s%d" % (c, CF['Operating cash flow'],
                                      c, CF['- Capex (Auto + rental fleet)']), bold=True)
r = crow(r, '+ Increase in borrowings (net)',
         lambda j, c: "=%s" % ac('Increase in borrowings, net (EGP mn)', j))
r = crow(r, '- Dividends paid',
         lambda j, c: "=-'Income Statement'!%s%d*%s"
         % (c, NP, ac('Dividend payout (of attributable NP)', j)))
DIVR = CF['- Dividends paid']
r = crow(r, 'Net change in cash',
         lambda j, c: "=%s%d+%s%d+%s%d" % (c, CF['Free cash flow'],
                                           c, CF['+ Increase in borrowings (net)'], c, DIVR),
         bold=True)
r = crow(r, 'Opening cash', lambda j, c: None)
OPEN = CF['Opening cash']
r = crow(r, 'Closing cash', lambda j, c: "=%s%d+%s%d" % (c, OPEN, c, CF['Net change in cash']),
         bold=True)
CLOSE = CF['Closing cash']
put(ws, 'E%d' % OPEN, "='Balance Sheet'!D%d" % CASH, GREEN, NUM0)
for c in FCOLS[1:]:
    put(ws, '%s%d' % (c, OPEN), "=%s%d" % (chr(ord(c) - 1), CLOSE), BLACK, NUM0)
# the Balance Sheet's cash and equity rows now point at the rows that carry them
bws = wb['Balance Sheet']
for j, c in enumerate(FCOLS):
    put(bws, '%s%d' % (c, CASH), "='Cash Flow'!%s%d" % (c, CLOSE), GREEN, NUM0)
    put(bws, '%s%d' % (c, EQ), "=%s%d+'Income Statement'!%s%d+'Cash Flow'!%s%d"
        % (chr(ord(c) - 1), EQ, c, NP, c, DIVR), GREEN, NUM0)
put(ws, 'A%d' % (r + 1),
    'Historical group cash-flow statements are published per segment in the company\'s own '
    'releases; the forecast here is the consolidated clean-surplus build, which is what the '
    'balance check on the previous sheet tests.', SUB, None)
json.dump(dict(CF=CF, CLOSE=CLOSE, DIVR=DIVR, OPEN=OPEN), open('_cf_rows.json', 'w'),
          indent=1, sort_keys=True)
wb.save(OUT)
print('part3 ok — IS/BS/CF; net profit row %d, working-capital row %d, closing cash row %d'
      % (NP, DNWC, CLOSE))
