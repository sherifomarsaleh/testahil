"""STC_Valuation_Model_09072026_public.xlsx — part A: READ FIRST, Assumptions, Segments,
DCF, Income Statement, Balance Sheet, Cash Flow. 16 sheets mirroring the TMPV canonical model.
Blue = inputs · black = formulas · green = cross-sheet links. All inputs live on Assumptions."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

D = json.load(open('study_numbers.json'))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM = '#,##0.0;(#,##0.0);"-"'; NUM0 = '#,##0;(#,##0);"-"'; PCT = '0.0%;(0.0%);"-"'
PCT2 = '0.00%;(0.00%);"-"'; MULT = '0.00x'; PX = '0.00'
FN = 'STC_Valuation_Model_09072026_public.xlsx'

wb = Workbook()

def sheet(name):
    ws = wb.create_sheet(name) if wb.sheetnames != ['Sheet'] else wb.active
    ws.title = name
    return ws

def title(ws, text, sub=None, width=10):
    ws['A1'] = text; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, width + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if sub:
        ws['A2'] = sub; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 44
    for c in range(2, width + 1):
        ws.column_dimensions[get_column_letter(c)].width = 12.5

def put(ws, addr, val, font=BLACK, fmt=None, bold=False, fill=None):
    c = ws[addr]; c.value = val
    c.font = Font(color=(font.color if font else '000000'), bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c

YH = ['FY23', 'FY24', 'FY25']; YF = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
FCOLS = ['E', 'F', 'G', 'H', 'I']; ACOLS = ['C', 'D', 'E', 'F', 'G']

# ============ READ FIRST =====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — Saudi Telecom Company (Tadawul: 7010)', width=9)
lines = [
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the stc valuation study. Every blue cell is an input; every',
 'black cell is a formula; green cells link across sheets. All inputs live on the Assumptions sheet — change one',
 '(the EBITDA margin path, capex intensity, the beta, terminal growth, a stake mark) and the whole model reprices.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model outputs shown',
 'as ranges. The preparer is not licensed by any securities regulator and may hold a position in the security.', '',
 'Entity note. Saudi Telecom Company (stc Group) is the Kingdom’s incumbent operator: stc KSA (consumer,',
 'enterprise, wholesale) plus subsidiaries — solutions by stc (79%, listed 7202), stc bank (85%, SAMA-licensed',
 'Jan-2025), stc Kuwait (51.8%), stc Bahrain (100%), center3 (data centres), sirar, iot squared (50% PIF JV) —',
 'and minority stakes: 43.06% of Digital Infrastructure Co (TAWAL+GLIC towers, PIF-controlled) and 9.97% of',
 'Telefónica. House lens: going-concern FCFF DCF (primary), cross-checked by the dividend-policy DDM,',
 'relative multiples and normalized earnings; the tower and Telefónica stakes are bridge items marked separately.', '',
 'Currency. SAR million unless stated. Spot SAR 43.58 (7 Jul 2026 close, from the attached daily history).',
 'Historical financials are stc’s own IR disclosure (FY23–FY25 releases, restated continuing-ops basis;',
 'Q1-26 release 28 Apr 2026); balance-sheet detail from the Q1-2026 interim FS (31-Dec-25 comparatives).', '',
 'Sheets: Summary · Fundamental Valuation · Assumptions · Valuation Bridge · Segments · Relative & Normalized ·',
 'DCF · Income Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo · Sensitivity ·',
 'Per-Share & Ratios · Peer & Sector.']
for i, ln in enumerate(lines, start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 118

# ============ ASSUMPTIONS ====================================================
wa = sheet('Assumptions')
title(wa, 'Assumptions — the single input layer', 'All blue cells are inputs. Every other sheet links here.', 9)
r = 4
def hdr(ws_, row, text):
    put(ws_, f'A{row}', text, bold=True, fill=FILL_H); return row + 1
def inp(ws_, row, label, val, fmt=NUM, note=None):
    put(ws_, f'A{row}', label)
    put(ws_, f'B{row}', val, BLUE, fmt)
    if note: put(ws_, f'C{row}', note, SUB)
    return row + 1
r = hdr(wa, r, 'ANCHORS')                                                  # 4
r = inp(wa, r, 'Spot price (SAR/share)', 43.58, PX, '7 Jul 2026 close, attached daily history')   # B5
r = inp(wa, r, 'Shares outstanding (mn)', 4989.8, NUM0, '5,000mn issued − ~10.2mn treasury; 26mn ESIP buyback approved 7-May-2026 not yet netted')  # B6
r = inp(wa, r, 'Normalized effective zakat & income tax', 0.097, PCT,
        'stc is a zakat payer (statutory 2.5% on the zakat base) plus foreign-subsidiary income taxes/WHT. Both framings: '
        'statutory 2.5% vs normalized effective ~9.7% (FY23 9.5%, FY24 9.8%; FY25 was a one-off net CREDIT of SAR 466mn '
        'from prior-year provision reversals). The model uses the normalized effective rate.')      # B7
r = hdr(wa, r, 'COST OF CAPITAL — bottom-up, sourced (house rule §3.5-G; full sourcing rows 84+)')  # 8
r = inp(wa, r, 'Risk-free rate (SAR 10Y sovereign, derived 8-Jul-2026)', 0.055, PCT2,
        'DERIVED: KSA govt-guaranteed USD 10Y priced UST+95bp on 8-Jul-2026 (SRC $1.5bn 10y sukuk; UST 10Y 4.45%) = 5.40%, '
        'plus the SAR-over-USD sovereign pickup documented in the Saudi Exchange "KSA Sovereign Local Currency Debt Primer '
        'Update" (21-May-2026); cross-checked vs FAB Securities 5.5% SAR rf (Feb-2026). No free live SAR 10Y screen quote '
        'exists — flagged as derived, not a screen print. NEVER shortcut to UST (peg ≠ equivalence).')  # B9
r = inp(wa, r, 'Equity beta (regressed vs TASI — see row 88)', 0.48, '0.00',
        'GENUINE REGRESSION: daily stc-vs-TASI, n=40 paired sessions (5-May→7-Jul-2026): beta 0.475, R²=0.143, SE=0.189 — '
        'passes the house usability gate (n≥24, R²≥5%, SE<|β|, β>0). Flag: 9-week window (longer TASI history not '
        'programmatically accessible); the beta sensitivity grid below is therefore mandatory reading.')  # B10
r = inp(wa, r, 'Equity risk premium — Saudi Arabia, rating-based (primary; CDS alt. row 86)', 0.0501, PCT2,
        'Damodaran ORIGINAL file (ctryprem.html), Saudi Arabia row, "Last updated: January 5, 2026": Moody’s Aa3, '
        'CRP 0.78% + mature-market 4.23% = 5.01%. Rating-based = "standard practice" primary; the CDS-based 5.72% is the '
        '"more current" alternative (note: for Saudi the CDS basis is HIGHER, unlike Egypt).')  # B11
put(wa, f'A{r}', 'Cost of equity Ke = rf + β × ERP'); put(wa, f'B{r}', '=B9+B10*B11', BLACK, PCT2)
put(wa, f'C{r}', 'Primary Ke (rating-based ERP), used in the base-case WACC.', SUB); r += 1   # B12
r = inp(wa, r, 'Pre-tax cost of debt (blended, sourced — row 89)', 0.050, PCT2,
        "stc's own instruments: Jan-2026 $2bn sukuk 4.489% (5y, T+75) / 5.083% (10y, T+90); 2019 $1.25bn sukuk 3.89%; "
        'SAR murabaha ≈ 3M SAIBOR 4.79% (Apr-2026) + 60–100bp. Weighted outstanding ≈ 5.0% pre-tax.')  # B13
put(wa, f'A{r}', 'After-tax Kd'); put(wa, f'B{r}', '=B13*(1-B7)', BLACK, PCT2); r += 1        # B14
put(wa, f'A{r}', 'Debt weight D/(D+E) — computed, never assumed')
put(wa, f'B{r}', '=22475/(B5*B6+22475)', BLACK, PCT2)
put(wa, f'C{r}', 'Market cap = spot × shares = SAR 217.5bn; total debt = Q1-26 IR-disclosed SAR 22,475mn '
                 '(post Jan-26 $2bn sukuk; excludes leases 2,296).', SUB); r += 1              # B15
put(wa, f'A{r}', 'WACC (rating-based ERP, primary)'); put(wa, f'B{r}', '=(1-B15)*B12+B15*B14', BLACK, PCT2); r += 1  # B16
r = inp(wa, r, 'Terminal growth g (nominal SAR)', 0.025, PCT2, '≈ Saudi long-run nominal GDP-lite for a mature telecom; sensitized §1.9')  # B17
r = hdr(wa, r, 'EV → EQUITY BRIDGE (marks)')                                # 18
r = inp(wa, r, 'Investments in associates & JVs (incl. 43.06% DIIC/TAWAL)', 4641.0, NUM0, '31-Dec-25, Q1-26 FS comparative (carrying value)')  # B19
r = inp(wa, r, 'Telefónica 9.97% stake (market mark)', 8630.0, NUM0,
        '561mn shares × €3.50 (6-Jul-26) × 4.40 SAR/EUR ≈ SAR 8.6bn; cost €2.1bn (Sep-2023) ≈ SAR 8.5bn')  # B20
r = inp(wa, r, 'Net debt (IR basis, Q1-2026)', 7063.0, NUM0,
        'Total debt 22,475 − IR cash 15,412 (IR cash excludes ~SAR 6.0bn stc bank banking-operations cash). '
        'Two framings: FS cash+murabaha 21,442 → net debt ~1,033; IR basis 7,063 used (conservative, core-group).')  # B21
r = inp(wa, r, 'Non-controlling interests (book)', 2335.0, NUM0, '31-Mar-26 FS')  # B22
r = hdr(wa, r, 'DDM (the locked SAR 0.55/quarter policy)')                  # 23
put(wa, f'A{r}', 'DPS path FY26E–FY30E (SAR)', BLACK);
for j, v in enumerate([2.20, 2.20, 2.30, 2.40, 2.55]):
    put(wa, f'{get_column_letter(3+j)}{r}', v, BLUE, PX)
DPS_ROW = r; r += 1                                                          # 24
r = inp(wa, r, 'DDM terminal dividend growth', 0.030, PCT2, 'post-policy (2027+) payout growth ≈ EPS growth at ~75% payout')  # B25
r = hdr(wa, r, 'RELATIVE & NORMALIZED')                                     # 26
r = inp(wa, r, 'Justified EV/EBITDA (base)', 9.0, MULT, 'GCC band ~8–10×; stc trades ~9.5× trailing')  # B27
r = inp(wa, r, 'FY26E net profit for the relative P/E cross-check', 14090.0, NUM0, 'IS-build aligned (attributable)')  # B28
r = inp(wa, r, 'Normalized PAT (ex one-offs)', 14400.0, NUM0, 'FY25 14,828 less the +466 zakat credit ≈ 14,360; mid-cycle margins')  # B29
r = inp(wa, r, 'Justified through-cycle P/E', 15.0, MULT)                   # B30
r = hdr(wa, r, 'SYNTHESIS WEIGHTS')                                         # 31
r = inp(wa, r, 'FCFF DCF weight', 0.35, PCT)                                # B32
r = inp(wa, r, 'DDM weight', 0.25, PCT)                                     # B33
r = inp(wa, r, 'Relative weight', 0.20, PCT)                                # B34
r = inp(wa, r, 'Normalized-earnings weight', 0.20, PCT)                     # B35
r = hdr(wa, r, 'MONTE CARLO (YZ-HAR v2 — engine outputs on the Monte Carlo sheet)')  # 36
r = inp(wa, r, 'Anchor volatility (HAR forecast, annualized)', round(D['engine']['anchor_vol'], 4), PCT)  # B37
r = inp(wa, r, 'Secular drift (daily) — zero-drift class', 0.0, '0.0000%', 'International/GCC name: zero drift passed Step 0; secular drift failed (−4.8%)')  # B38
r = inp(wa, r, 'Net factor drift per quarter (16-factor stack)', round(D['engine']['factor_drift_q'], 4), PCT)  # B39
r = inp(wa, r, 'Paths / seed', '50,000 / 42', '@')                          # B40
r = hdr(wa, r, 'FORECAST DRIVERS (FY26E–FY30E) — top-down (§3.5-C gate: subs × ARPU not disclosed)')  # 41
put(wa, f'A{r}', 'Driver \\ year', bold=True)
for j, y in enumerate(YF):
    put(wa, f'{get_column_letter(3+j)}{r}', y, bold=True, fill=FILL_H)
r += 1
DRV = {}
def drv(row, label, vals, fmt=PCT):
    put(wa, f'A{row}', label)
    for j, v in enumerate(vals):
        put(wa, f'{get_column_letter(3+j)}{row}', v, BLUE, fmt)
    DRV[label] = row
    return row + 1
dr = D['drivers']
r = drv(r, 'KSA Consumer (CBU) revenue growth', dr['g_cbu'])
r = drv(r, 'KSA Enterprise (EBU) revenue growth', dr['g_ebu'])
r = drv(r, 'KSA Wholesale & Carrier revenue growth', dr['g_wc'])
r = drv(r, 'Subsidiaries net revenue growth', dr['g_sub'])
r = drv(r, 'Group EBITDA margin', dr['ebitda_m'])
r = drv(r, 'D&A (% of revenue)', dr['dna_pct'])
r = drv(r, 'Capex intensity (% of revenue)', dr['capex_pct'])
r = drv(r, 'Net WC / OCF-conversion drag (% of revenue)', dr['wc_out_pct'])
r = drv(r, 'Associates income (SAR mn)', [500, 530, 560, 590, 620], NUM0)
r = drv(r, 'Net finance & other income (SAR mn)', [200, 220, 240, 260, 280], NUM0)
r = drv(r, 'NCI share of profit (% of group NP)', [0.025]*5)
r = drv(r, 'DPS declared (SAR/share)', dr['payout_dps'], PX)
wa.column_dimensions['C'].width = 11

# ===== WACC BUILD — FULL DETAIL & SOURCING (rows 84-92) ======================
r = hdr(wa, 84, 'WACC BUILD — FULL DETAIL & SOURCING (feeds rows 9-17; reference only)')
put(wa, f'A{r}', 'rf source')
put(wa, f'C{r}', 'Derived SAR 10Y sovereign: SRC (govt-guaranteed) $1.5bn 10y sukuk priced UST+95bp on 8-Jul-2026; UST 10Y '
                  '4.45% → 5.40% USD basis; the Saudi Exchange "KSA Sovereign Local Currency Debt Primer Update" (21-May-2026) '
                  'documents SAR sovereign yields sitting ABOVE the USD curve through 10Y → 5.4–5.6% band, 5.5% point. '
                  'Cross-check: FAB Securities stc note (27-Feb-2026) uses 5.5%. Per house rule the SAR-USD peg does NOT '
                  'make UST a substitute — this is a documented named mistake in professional practice.', SUB)
r += 1
r = inp(wa, r, 'ERP — CDS-based (Damodaran, "more current" alternative)', 0.0572, PCT2,
        'Same original file, Saudi row, CDS column: sovereign CDS 0.98% → ERP 5.72%. For Saudi the CDS basis is ABOVE the '
        'rating basis (CDS prices more risk than Aa3 implies) — the alternative WACC below is therefore the HIGHER one.')   # B86
put(wa, f'A{r}', 'Ke, alternative (CDS-based ERP)'); put(wa, f'B{r}', '=B9+B10*B86', BLACK, PCT2); r += 1   # B87
put(wa, f'A{r}', 'WACC, alternative (CDS-based ERP)'); put(wa, f'B{r}', '=(1-B15)*B87+B15*B14', BLACK, PCT2); r += 1  # B88
put(wa, f'A{r}', 'Beta — regression detail')
put(wa, f'C{r}', 'Daily stc-vs-TASI OLS, n=40 paired sessions 5-May→7-Jul-2026 (TASI closes: investing.com historical table; '
                  'stc: the attached price history): beta 0.475 (SE 0.189), R² 14.3%, alpha ≈ 0. Ex-Eid-gap robustness: 0.494. '
                  'Passes RegressionBetaAttempt.is_usable() (n≥24, R²≥5%, SE<|β|, β>0). Honest flag: a 9-week daily window is '
                  'the best obtainable (Yahoo/stooq/WSJ TASI history all blocked programmatically; Saudi Exchange login-gated); '
                  'a 2–5yr weekly regression should replace it when accessible. Sensitivity: at β=1.0, Ke 10.51%, WACC 9.90% '
                  '(rating basis) — the DCF grid in §1.9 spans this.', SUB)
r += 1
put(wa, f'A{r}', 'Kd source & currency-mix evidence')
put(wa, f'C{r}', 'Named instruments: May-2019 $1.25bn 10y sukuk at 3.89% (matures 2029); Jan-2026 $2bn dual-tranche sukuk '
                  '4.489% (5y, T+75) / 5.083% (10y, T+90) under the $5bn programme (books $5.4bn); Mar-2021 ECA loan $584mn; '
                  'remainder SAR murabaha/facilities (3M SAIBOR 4.79% Apr-2026 + 60–100bp). USD-linked ≈ 55–60% of gross '
                  'debt; SAR pegged 3.75 → USD legs economically quasi-SAR, single blended Kd 5.0% used (no floating-FX '
                  'tranche modelled).', SUB)
r += 1
put(wa, f'A{r}', 'Weights source')
put(wa, f'C{r}', 'Market cap = 43.58 × 4,989.8mn = SAR 217,455mn; total debt = SAR 22,475mn (Q1-2026 IR release, post the '
                  'Jan-2026 $2bn sukuk; excludes lease liabilities 2,296). E/(D+E) = 90.6%.', SUB)
r += 1
put(wa, f'A{r}', 'Full reference & cache')
put(wa, f'C{r}', 'See Cost_of_Capital_Reference.md (Saudi Arabia row, filled 09-07-2026) and wacc_builder.py for the standing '
                  'method. Both ERP-basis WACCs are published per protocol.', SUB)

json.dump(DRV, open('_asm_rows.json', 'w'))
json.dump(dict(DPS_ROW=DPS_ROW), open('_asm_extra.json', 'w'))
wb.save(FN)
print('partA1 ok; drivers:', len(DRV))
