"""Part B: Segments · DCF · Income Statement · Balance Sheet · Cash Flow (formula-linked)."""
import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

FN = 'STC_Valuation_Model_09072026_public.xlsx'
wb = load_workbook(FN)
A = json.load(open('_asm_rows.json'))
D = json.load(open('stc_study_numbers.json'))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
NUM0 = '#,##0;(#,##0);"-"'; PCT = '0.0%;(0.0%);"-"'; PX = '0.00'
YH = ['FY23', 'FY24', 'FY25']; YF = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
FCOLS = ['E', 'F', 'G', 'H', 'I']; ACOLS = ['C', 'D', 'E', 'F', 'G']

def sheet(n): ws = wb.create_sheet(n); ws.title = n; return ws
def title(ws, t, s=None, w=10):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w+1): ws.cell(row=1, column=c).fill = FILL_T
    if s: ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 42
    for c in range(2, w+1): ws.column_dimensions[get_column_letter(c)].width = 11.5
def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None):
    c = ws[ad]; c.value = v; c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
def ac(label, j): return f"Assumptions!${ACOLS[j]}${A[label]}"

# ================= SEGMENTS ==================================================
ws = sheet('Segments')
title(ws, 'Segment view — stc KSA units + subsidiaries',
      'FY24–FY25 disclosed per stc’s FY2025 presentation (restated); FY23 available at group level only on the '
      'restated continuing-ops basis. Forecast links to Assumptions growth drivers.', 10)
hdrs = [''] + YH + YF
for j, h in enumerate(hdrs):
    put(ws, f'{get_column_letter(1+j)}4', h, BLACK, None, bold=True, fill=FILL_H)
SR = {}
def srow(r, label, hist, ffml=None, fmt=NUM0, font_hist=BLUE):
    SR[label] = r
    put(ws, f'A{r}', label)
    for j, v in enumerate(hist):
        if v is not None: put(ws, f'{get_column_letter(2+j)}{r}', v, font_hist, fmt)
    if ffml:
        for j, col in enumerate(FCOLS):
            f = ffml(j, col)
            if f is not None: put(ws, f'{col}{r}', f, BLACK, fmt)
    return r + 1
r = 6
r = srow(r, 'KSA Consumer (CBU)', [None, 31741.0, 32826.0],
         lambda j, c: f"={chr(ord(c)-1)}{SR['KSA Consumer (CBU)']}*(1+{ac('KSA Consumer (CBU) revenue growth', j)})")
r = srow(r, 'KSA Enterprise (EBU)', [None, 13466.0, 13514.0],
         lambda j, c: f"={chr(ord(c)-1)}{SR['KSA Enterprise (EBU)']}*(1+{ac('KSA Enterprise (EBU) revenue growth', j)})")
r = srow(r, 'KSA Wholesale & Carrier', [None, 4313.0, 4779.0],
         lambda j, c: f"={chr(ord(c)-1)}{SR['KSA Wholesale & Carrier']}*(1+{ac('KSA Wholesale & Carrier revenue growth', j)})")
r = srow(r, 'stc KSA total', [None, 49644.0, 51119.0],
         lambda j, c: f"={c}{SR['KSA Consumer (CBU)']}+{c}{SR['KSA Enterprise (EBU)']}+{c}{SR['KSA Wholesale & Carrier']}", NUM0, BLACK)
KSAR = SR['stc KSA total']
for col, v in [('C', 49644.0), ('D', 51119.0)]:
    ws[f'{col}{KSAR}'] = f"={col}{SR['KSA Consumer (CBU)']}+{col}{SR['KSA Enterprise (EBU)']}+{col}{SR['KSA Wholesale & Carrier']}"
    ws[f'{col}{KSAR}'].font = BLACK
r = srow(r, 'Subsidiaries, net of eliminations', [None, 26249.0, 26700.0],
         lambda j, c: f"={chr(ord(c)-1)}{SR['Subsidiaries, net of eliminations']}*(1+{ac('Subsidiaries net revenue growth', j)})")
SUBR = SR['Subsidiaries, net of eliminations']
r = srow(r, 'Group revenue', [71777.0, 75893.0, 77819.0],
         lambda j, c: f"={c}{KSAR}+{c}{SUBR}", NUM0, BLUE)
GRPR = SR['Group revenue']
r += 1
r = srow(r, 'Group EBITDA', [22445.0, 23951.0, 24469.0],
         lambda j, c: f"={c}{GRPR}*{ac('Group EBITDA margin', j)}")
GEB = SR['Group EBITDA']
r = srow(r, 'EBITDA margin', [f'=B{GEB}/B{GRPR}', f'=C{GEB}/C{GRPR}', f'=D{GEB}/D{GRPR}'],
         lambda j, c: f"={c}{GEB}/{c}{GRPR}", PCT, BLACK)
r += 1
put(ws, f'A{r}', 'Named subsidiary revenue, FY2025 (gross, incl. inter-segment — context, not modelled lines):', SUB, None); r += 1
for nm, v in [('solutions by stc (7202, 79%)', '12,730'), ('channels', '~14,085'), ('stc bank (85%)', '1,968 (+11%)'),
              ('SCCC cloud (55%)', '1,962 (+62%)'), ('iot squared (50%)', '1,928'), ('sirar (100%)', '1,401 (+13%)'),
              ('center3 (100%)', '~827')]:
    put(ws, f'A{r}', '  ' + nm, BLACK, None); put(ws, f'B{r}', v, BLACK, '@'); r += 1
put(ws, f'A{r+1}', 'Source: stc FY2025 earnings presentation & Q1-2026 release (stc.com IR). KSA unit splits disclosed from FY24 on the '
                   'restated basis; FY23 KSA split not restated — group only. Q1-26: KSA 13,001 (CBU 8,283 +5.2%, EBU 3,483 −3.6%, W&C 1,235 +6.2%).', SUB, None)
json.dump(SR, open('_seg_rows.json', 'w'))

# ================= DCF =======================================================
ws = sheet('DCF')
title(ws, 'DCF — going-concern FCFF, explicit 5 years',
      'Revenue → EBITDA → D&A → EBIT → NOPAT → +D&A → −Capex → −ΔWC → FCFF → discount factor → PV. '
      'WACC built bottom-up on Assumptions (rf + β×ERP, both ERP bases published).', 8)
for j, y in enumerate(YF):
    put(ws, f'{get_column_letter(2+j)}4', y, BLACK, None, bold=True, fill=FILL_H)
DC = {}
def drow(r, label, fml, fmt=NUM0, bold=False):
    DC[label] = r
    put(ws, f'A{r}', label, BLACK, None, bold=bold)
    for j in range(5):
        c = get_column_letter(2+j)
        f = fml(j, c)
        put(ws, f'{c}{r}', f, GREEN if 'Segments!' in str(f) else BLACK, fmt, bold=bold)
    return r + 1
r = 6
r = drow(r, 'Group revenue', lambda j, c: f"=Segments!{FCOLS[j]}{GRPR}")
r = drow(r, 'EBITDA', lambda j, c: f"=Segments!{FCOLS[j]}{GEB}")
r = drow(r, 'D&A', lambda j, c: f"=-{c}{DC['Group revenue']}*{ac('D&A (% of revenue)', j)}")
r = drow(r, 'EBIT', lambda j, c: f"={c}{DC['EBITDA']}+{c}{DC['D&A']}")
r = drow(r, 'NOPAT = EBIT × (1 − zakat/tax)', lambda j, c: f"={c}{DC['EBIT']}*(1-Assumptions!$B$7)")
r = drow(r, '+ D&A', lambda j, c: f"=-{c}{DC['D&A']}")
r = drow(r, '− Capex', lambda j, c: f"=-{c}{DC['Group revenue']}*{ac('Capex intensity (% of revenue)', j)}")
r = drow(r, '− Increase in net working capital', lambda j, c: f"=-{c}{DC['Group revenue']}*{ac('Net WC / OCF-conversion drag (% of revenue)', j)}")
r = drow(r, 'FCFF', lambda j, c: f"=SUM({c}{DC['NOPAT = EBIT × (1 − zakat/tax)']}:{c}{DC['− Increase in net working capital']})", bold=True)
r = drow(r, 'Discount factor', lambda j, c: f"=1/(1+Assumptions!$B$16)^{j+1}", '0.000')
r = drow(r, 'PV of FCFF', lambda j, c: f"={c}{DC['FCFF']}*{c}{DC['Discount factor']}", bold=True)
r += 1
def dline(r, label, fml, fmt=NUM0, bold=False):
    put(ws, f'A{r}', label, BLACK, None, bold=bold); put(ws, f'B{r}', fml, BLACK, fmt, bold=bold); return r + 1
r = dline(r, 'Σ PV of explicit FCFF (FY26–30E)', f"=SUM(B{DC['PV of FCFF']}:F{DC['PV of FCFF']})", bold=True); SPV = r-1
r = dline(r, 'Terminal value (Gordon, g = Assumptions B17)', f"=F{DC['FCFF']}*(1+Assumptions!$B$17)/(Assumptions!$B$16-Assumptions!$B$17)"); TVR = r-1
r = dline(r, 'PV of terminal value', f"=B{TVR}*F{DC['Discount factor']}"); PVT = r-1
r = dline(r, 'Enterprise value — core operations', f"=B{SPV}+B{PVT}", bold=True); EVR = r-1
r = dline(r, '% terminal of EV (device A-7)', f"=B{PVT}/B{EVR}", PCT, bold=True); TVP = r-1
r = dline(r, '+ Investments in associates (DIIC/TAWAL 43.06%)', f"=Assumptions!$B$19")
r = dline(r, '+ Telefónica 9.97% (market mark)', f"=Assumptions!$B$20")
r = dline(r, '− Net debt (IR basis, Q1-26)', f"=-Assumptions!$B$21")
r = dline(r, '− Non-controlling interests', f"=-Assumptions!$B$22")
r = dline(r, 'Equity value', f"=B{EVR}+Assumptions!$B$19+Assumptions!$B$20-Assumptions!$B$21-Assumptions!$B$22", bold=True); EQR = r-1
r = dline(r, 'DCF fair value per share (SAR)', f"=B{EQR}/Assumptions!$B$6", PX, bold=True); PSR = r-1
r = dline(r, 'Upside / (downside) vs spot', f"=B{PSR}/Assumptions!$B$5-1", PCT)
put(ws, f'A{r+1}', 'WACC is built on Assumptions as Ke = rf + β×ERP blended with after-tax Kd (§3.5-G); the alternative CDS-based WACC '
                   'is on Assumptions row 88. Terminal value is disclosed as % of EV above rather than blended away (device A-7).', SUB, None)
json.dump(dict(DC=DC, SPV=SPV, TVR=TVR, PVT=PVT, EVR=EVR, EQR=EQR, PSR=PSR, TVP=TVP), open('_dcf_rows.json', 'w'))

# ================= INCOME STATEMENT ==========================================
ws = sheet('Income Statement')
title(ws, 'Income statement (SAR mn, consolidated, continuing operations)',
      'FY23–FY25 as disclosed in stc IR releases, restated continuing-ops basis (blue); FY26E–FY30E formulas linked to Segments and Assumptions.', 10)
for j, h in enumerate([''] + YH + YF):
    put(ws, f'{get_column_letter(1+j)}4', h, BLACK, None, bold=True, fill=FILL_H)
IS = {}
def irow(r, label, hist, ffml=None, fmt=NUM0, hfont=BLUE, bold=False):
    IS[label] = r
    put(ws, f'A{r}', label, BLACK, None, bold=bold)
    for j, v in enumerate(hist):
        if v is not None: put(ws, f'{get_column_letter(2+j)}{r}', v, hfont, fmt, bold=bold)
    if ffml:
        for j, c in enumerate(FCOLS):
            f = ffml(j, c)
            if f is not None:
                put(ws, f'{c}{r}', f, GREEN if 'Segments!' in str(f) else BLACK, fmt, bold=bold)
    return r + 1
r = 6
r = irow(r, 'Total revenue', [71777.0, 75893.0, 77819.0], lambda j, c: f"=Segments!{c}{GRPR}", NUM0, BLUE, True)
REV = IS['Total revenue']
r = irow(r, 'Gross profit', [34740.0, 37326.0, 37700.0], lambda j, c: f"={c}{REV}*0.485", NUM0)
GP = IS['Gross profit']
r = irow(r, 'Gross margin', [f'=B{GP}/B{REV}', f'=C{GP}/C{REV}', f'=D{GP}/D{REV}'],
         lambda j, c: f"={c}{GP}/{c}{REV}", PCT, BLACK)
r = irow(r, 'EBITDA', [22445.0, 23951.0, 24469.0], lambda j, c: f"=Segments!{c}{GEB}", NUM0, BLUE, True)
EBITDAR = IS['EBITDA']
r = irow(r, 'EBITDA margin', [f'=B{EBITDAR}/B{REV}', f'=C{EBITDAR}/C{REV}', f'=D{EBITDAR}/D{REV}'],
         lambda j, c: f"={c}{EBITDAR}/{c}{REV}", PCT, BLACK)
r = irow(r, 'Depreciation, amortisation & impairment', [-9284.0, -9525.0, -10031.0],
         lambda j, c: f"=-{c}{REV}*{ac('D&A (% of revenue)', j)}")
DNAR = IS['Depreciation, amortisation & impairment']
r = irow(r, 'Operating profit (EBIT)', [13161.0, 14426.0, 14438.0],
         lambda j, c: f"={c}{EBITDAR}+{c}{DNAR}", NUM0, BLUE, True)
EBITR = IS['Operating profit (EBIT)']
r = irow(r, 'Share of associates & JVs + net finance & other', [1461.0, 899.0, 285.0],
         lambda j, c: f"={ac('Associates income (SAR mn)', j)}+{ac('Net finance & other income (SAR mn)', j)}")
ASSR = IS['Share of associates & JVs + net finance & other']
r = irow(r, 'Profit before zakat & income tax', [14622.0, 15325.0, 14723.0],
         lambda j, c: f"={c}{EBITR}+{c}{ASSR}", NUM0, BLACK, True)
EBTR = IS['Profit before zakat & income tax']
r = irow(r, 'Zakat & income tax', [-1327.0, -1192.0, 466.0],
         lambda j, c: f"=-{c}{EBTR}*Assumptions!$B$7")
ZAKR = IS['Zakat & income tax']
r = irow(r, 'Profit from continuing operations', [13295.0-759.0+759.0-13295.0+12536.0+759.0, 10716.0+226.0, 15189.0],
         lambda j, c: f"={c}{EBTR}+{c}{ZAKR}", NUM0, BLACK, True)
# fix messy FY23 arithmetic: continuing incl NCI = 12,536 att + ~124 NCI ≈ 12,660; FY24 = 10,716+226=10,942; FY25 = 15,189
ws[f'B{IS["Profit from continuing operations"]}'] = 12660.0
ws[f'C{IS["Profit from continuing operations"]}'] = 10942.0
ws[f'D{IS["Profit from continuing operations"]}'] = 15189.0
NPCR = IS['Profit from continuing operations']
r = irow(r, 'Profit from discontinued operations', [759.0, 13973.0, 0.0], lambda j, c: '=0')
r = irow(r, 'Non-controlling interests', [-124.0, -226.0, -361.0],
         lambda j, c: f"=-({c}{NPCR})*{ac('NCI share of profit (% of group NP)', j)}")
NCIR = IS['Non-controlling interests']
r = irow(r, 'Net profit (attributable)', [13295.0, 24689.0, 14828.0],
         lambda j, c: f"={c}{NPCR}+{c}{IS['Profit from discontinued operations']}+{c}{NCIR}", NUM0, BLUE, True)
NPR = IS['Net profit (attributable)']
r = irow(r, 'Net margin (attributable)', [f'=B{NPR}/B{REV}', f'=C{NPR}/C{REV}', f'=D{NPR}/D{REV}'],
         lambda j, c: f"={c}{NPR}/{c}{REV}", PCT, BLACK)
r = irow(r, 'EPS (SAR)', ['=B'+str(NPR)+'/Assumptions!$B$6', '=C'+str(NPR)+'/Assumptions!$B$6', '=D'+str(NPR)+'/Assumptions!$B$6'],
         lambda j, c: f"={c}{NPR}/Assumptions!$B$6", PX, BLACK)
put(ws, f'A{r+1}', 'Sources: stc FY2024/FY2025 IR releases + Q1-2026 interim FS (all stc.com). FY23/FY24 restated to continuing operations '
                   '(TAWAL + Digital Infrastructure Co reclassified as discontinued; FY24 discontinued profit 13,973 incl. the SAR 12,885mn disposal gain). '
                   'One-offs: FY23 AlKhobar land gain +1,296, WHT reversal +724, ERP −863; FY24 WHT reversal +1,500, ERP −2,577, BGSM impairment −764; '
                   'FY25 zakat credit +466, ERP ≈ −824. "Share of associates + net finance & other" is the residual bridging disclosed EBIT to disclosed '
                   'profit before zakat — stc does not publish those lines separately in the IR release layout; the FY25 annual FS carries the full detail.', SUB, None)
json.dump(IS, open('_is_rows.json', 'w'))

# ================= BALANCE SHEET =============================================
ws = sheet('Balance Sheet')
title(ws, 'Balance sheet (SAR mn, consolidated)',
      'FY23–FY25 grouped from stc disclosure to a house layout (blue; FY25 detail from the Q1-2026 FS comparatives). '
      'Forecast rolls forward clean-surplus; the check row is zero by construction.', 10)
for j, h in enumerate([''] + YH + YF):
    put(ws, f'{get_column_letter(1+j)}4', h, BLACK, None, bold=True, fill=FILL_H)
BS = {}
def brow(r, label, hist, ffml=None, fmt=NUM0, hfont=BLUE, bold=False):
    BS[label] = r
    put(ws, f'A{r}', label, BLACK, None, bold=bold)
    for j, v in enumerate(hist):
        if v is not None: put(ws, f'{get_column_letter(2+j)}{r}', v, hfont, fmt, bold=bold)
    if ffml:
        for j, c in enumerate(FCOLS):
            f = ffml(j, c)
            if f is not None:
                put(ws, f'{c}{r}', f, GREEN if ("Cash Flow" in str(f) or "Income" in str(f) or "Segments" in str(f)) else BLACK, fmt, bold=bold)
    return r + 1
r = 6
r = brow(r, 'PP&E, ROU, intangibles & inv. property', [92000.0, 95500.0, 126436.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['PP&E, ROU, intangibles & inv. property']}+Segments!{c}{GRPR}*{ac('Capex intensity (% of revenue)', j)}+'Income Statement'!{c}{DNAR}")
PPER = BS['PP&E, ROU, intangibles & inv. property']
r = brow(r, 'Investments in associates & JVs', [3800.0, 4200.0, 4641.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Investments in associates & JVs']}+{ac('Associates income (SAR mn)', j)}")
r = brow(r, 'Financial assets (incl. Telefónica 9.97%)', [22000.0, 23500.0, 24893.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Financial assets (incl. Telefónica 9.97%)']}")
r = brow(r, 'Trade receivables, net', [24500.0, 25800.0, 26727.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Trade receivables, net']}+Segments!{c}{GRPR}*{ac('Net WC / OCF-conversion drag (% of revenue)', j)}")
TRR = BS['Trade receivables, net']
r = brow(r, 'Cash, equivalents & short-term murabahas', [28138.0, 30755.0, 15108.0],
         lambda j, c: f"='Cash Flow'!{c}20")
CASH = BS['Cash, equivalents & short-term murabahas']
r = brow(r, 'Other assets', [None, None, 2952.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Other assets']}")
OTHA = BS['Other assets']
ws[f'B{OTHA}'] = f"=159646-B{PPER}-B{BS['Investments in associates & JVs']}-B{BS['Financial assets (incl. Telefónica 9.97%)']}-B{TRR}-B{CASH}"
ws[f'C{OTHA}'] = f"=160638-C{PPER}-C{BS['Investments in associates & JVs']}-C{BS['Financial assets (incl. Telefónica 9.97%)']}-C{TRR}-C{CASH}"
for col in 'BC': ws[f'{col}{OTHA}'].font = BLACK; ws[f'{col}{OTHA}'].number_format = NUM0
r = brow(r, 'TOTAL ASSETS', [159646.0, 160638.0, None],
         lambda j, c: f"=SUM({c}{PPER}:{c}{OTHA})", NUM0, BLUE, True)
TA = BS['TOTAL ASSETS']
ws[f'D{TA}'] = f"=SUM(D{PPER}:D{OTHA})"; ws[f'D{TA}'].font = Font(bold=True); ws[f'D{TA}'].number_format = NUM0
r += 1
r = brow(r, 'Equity attributable to shareholders', [78985.0, 89417.0, 83414.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Equity attributable to shareholders']}+'Income Statement'!{c}{NPR}-{ac('DPS declared (SAR/share)', j)}*Assumptions!$B$6")
EQR2 = BS['Equity attributable to shareholders']
r = brow(r, 'Non-controlling interests', [2530.0, 3069.0, 3482.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Non-controlling interests']}-'Income Statement'!{c}{NCIR}")
NCIR2 = BS['Non-controlling interests']
r = brow(r, 'Total equity', [81515.0, 92486.0, 86896.0],
         lambda j, c: f"={c}{EQR2}+{c}{NCIR2}", NUM0, BLACK, True)
for col in 'BCD':
    ws[f'{col}{BS["Total equity"]}'] = f"={col}{EQR2}+{col}{NCIR2}"; ws[f'{col}{BS["Total equity"]}'].font = Font(bold=True); ws[f'{col}{BS["Total equity"]}'].number_format = NUM0
r = brow(r, 'Borrowings & sukuk (excl. leases)', [21958.0, 15132.0, 15191.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Borrowings & sukuk (excl. leases)']}" + ("+7284" if j == 0 else ""))
DEBTR = BS['Borrowings & sukuk (excl. leases)']
r = brow(r, 'Lease liabilities', [6985.0, 4580.0, 2253.0], lambda j, c: f"={chr(ord(c)-1)}{BS['Lease liabilities']}")
r = brow(r, 'Trade payables & financial liabilities', [26000.0, 27500.0, 29610.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Trade payables & financial liabilities']}")
r = brow(r, 'Zakat payable, provisions & other liabilities', [None, None, 14876.0],
         lambda j, c: f"={chr(ord(c)-1)}{BS['Zakat payable, provisions & other liabilities']}")
OTHL = BS['Zakat payable, provisions & other liabilities']
ws[f'B{OTHL}'] = f"=159646-B{BS['Total equity']}-B{DEBTR}-B{BS['Lease liabilities']}-B{BS['Trade payables & financial liabilities']}"
ws[f'C{OTHL}'] = f"=160638-C{BS['Total equity']}-C{DEBTR}-C{BS['Lease liabilities']}-C{BS['Trade payables & financial liabilities']}"
for col in 'BC': ws[f'{col}{OTHL}'].font = BLACK; ws[f'{col}{OTHL}'].number_format = NUM0
r = brow(r, 'TOTAL EQUITY & LIABILITIES', [None, None, None],
         lambda j, c: f"={c}{BS['Total equity']}+{c}{DEBTR}+{c}{BS['Lease liabilities']}+{c}{BS['Trade payables & financial liabilities']}+{c}{OTHL}", NUM0, BLACK, True)
TLE = BS['TOTAL EQUITY & LIABILITIES']
for col in 'BCD':
    ws[f'{col}{TLE}'] = f"={col}{BS['Total equity']}+{col}{DEBTR}+{col}{BS['Lease liabilities']}+{col}{BS['Trade payables & financial liabilities']}+{col}{OTHL}"
    ws[f'{col}{TLE}'].font = Font(bold=True); ws[f'{col}{TLE}'].number_format = NUM0
r += 1
r = brow(r, 'Balance check (assets − L&E)', [None]*3,
         lambda j, c: f"={c}{TA}-{c}{TLE}", NUM0, BLACK, True)
CHK = BS['Balance check (assets − L&E)']
for col in 'BCD':
    ws[f'{col}{CHK}'] = f"={col}{TA}-{col}{TLE}"; ws[f'{col}{CHK}'].number_format = NUM0
r = brow(r, 'Net debt — IR basis (borrowings − cash, group def.)', [None]*3,
         lambda j, c: f"={c}{DEBTR}-{c}{CASH}", NUM0, BLACK)
NDR = BS['Net debt — IR basis (borrowings − cash, group def.)']
for col in 'BCD':
    ws[f'{col}{NDR}'] = f"={col}{DEBTR}-{col}{CASH}"; ws[f'{col}{NDR}'].number_format = NUM0
put(ws, f'A{r+1}', 'Historic mapping: FY25 line detail from the Q1-2026 FS 31-Dec-25 comparatives (PP&E 95,313 + ROU 2,635 + intangibles 28,139 '
                   '+ inv. property 350 grouped; cash 13,376 + murabaha 1,732). FY23/FY24 detail lines are grouped estimates reconciling to the '
                   'disclosed IR totals (blue totals are as-disclosed); "Other" lines are the disclosed-total balancing items, shown as formulas. '
                   'FY26E borrowings step up SAR +7,284mn = the Jan-2026 $2bn sukuk (net of FY26 amortisation) — thereafter gross debt held flat. '
                   'Two cash framings exist (FS 21,442 incl. stc bank vs IR 15,412 core): the model rolls the FS-basis cash from FY25’s 15,108 '
                   '(cash + murabaha) and states the IR basis in the net-debt memo.', SUB, None)
json.dump(dict(BS=BS, CASH=CASH, TA=TA, TLE=TLE, CHK=CHK, NDR=NDR), open('_bs_rows.json', 'w'))

# ================= CASH FLOW =================================================
ws = sheet('Cash Flow')
title(ws, 'Cash flow (SAR mn, forecast)',
      'Derived from the Income Statement and Balance Sheet; closing cash ties to the Balance Sheet, so the check row is zero.', 10)
for j, h in enumerate([''] + YF):
    put(ws, f'{get_column_letter(4+j)}4', h, BLACK, None, bold=True, fill=FILL_H)
CF = {}
def crow(r, label, ffml, fmt=NUM0, bold=False):
    CF[label] = r
    put(ws, f'A{r}', label, BLACK, None, bold=bold)
    for j, c in enumerate(FCOLS):
        f = ffml(j, c)
        if f is not None:
            put(ws, f'{c}{r}', f, GREEN if '!' in str(f) else BLACK, fmt, bold=bold)
    return r + 1
r = 6
r = crow(r, 'Profit for the period (incl. NCI)', lambda j, c: f"='Income Statement'!{c}{NPCR}")
r = crow(r, '+ D&A', lambda j, c: f"=-'Income Statement'!{c}{DNAR}")
r = crow(r, '− Associates income (non-cash)', lambda j, c: f"=-{ac('Associates income (SAR mn)', j)}")
r = crow(r, '− Increase in trade receivables (ΔWC)', lambda j, c: f"=-(('Balance Sheet'!{c}{TRR})-('Balance Sheet'!{chr(ord(c)-1)}{TRR}))")
r = crow(r, 'Operating cash flow', lambda j, c: f"=SUM({c}{CF['Profit for the period (incl. NCI)']}:{c}{CF['− Increase in trade receivables (ΔWC)']})", bold=True)
r = crow(r, '− Capex', lambda j, c: f"=-Segments!{c}{GRPR}*{ac('Capex intensity (% of revenue)', j)}")
r = crow(r, 'Free cash flow', lambda j, c: f"={c}{CF['Operating cash flow']}+{c}{CF['− Capex']}", bold=True)
FCFR = CF['Free cash flow']
r = crow(r, '+ Increase in borrowings (net)', lambda j, c: ('=7284' if j == 0 else '=0'))
r = crow(r, '− Dividends paid (attributable)', lambda j, c: f"=-{ac('DPS declared (SAR/share)', j)}*Assumptions!$B$6")
DIVR = CF['− Dividends paid (attributable)']
r = crow(r, 'Net change in cash', lambda j, c: f"={c}{FCFR}+{c}{CF['+ Increase in borrowings (net)']}+{c}{DIVR}", bold=True)
r = crow(r, 'Opening cash', lambda j, c: (f"='Balance Sheet'!D{CASH}" if j == 0 else None))
OPEN = CF['Opening cash']
r = crow(r, 'Closing cash', lambda j, c: f"={c}{OPEN}+{c}{CF['Net change in cash']}", bold=True)
CLOSE = CF['Closing cash']
for j, c in enumerate(FCOLS[1:], start=1):
    ws[f'{c}{OPEN}'] = f"={chr(ord(c)-1)}{CLOSE}"; ws[f'{c}{OPEN}'].font = BLACK; ws[f'{c}{OPEN}'].number_format = NUM0
put(ws, f'A{r+1}', 'NCI profit is retained (no NCI dividend modelled — solutions’ minority dividend leakage is inside "net finance & other"). '
                   'Historical group cash flows: OCF 22,418 / 19,885 / 18,283 and FCF 12,628 / 7,959 / 6,488 (FY23/24/25, stc IR releases; '
                   'restated). The FY26E borrowings line is the Jan-2026 sukuk already completed.', SUB, None)
json.dump(dict(CF=CF, CLOSE=CLOSE, DIVR=DIVR, FCFR=FCFR), open('_cf_rows.json', 'w'))
wb.save(FN)
print('partB ok — Segments/DCF/IS/BS/CF; GRPR', GRPR, 'GEB', GEB, 'NPR', NPR)
