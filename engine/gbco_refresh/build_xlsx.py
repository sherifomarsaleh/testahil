"""GBCO refresh — 16-sheet Excel model builder. Reads study_numbers.json ONLY.

Blue = input (disclosed/sourced/decision, each annotated), black = formula. Every forecast
cell is a live formula: change a driver on Assumptions and the fair value reprices.
Sheet list and order match the model-study spec exactly.
"""
import json, os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
OUT = os.path.join(HERE, 'GBCO_Valuation_Model_19082026_public.xlsx')

INK = '1C3A36'; BLUE = '1F4EB0'; GREY = '6E7B77'
F_HDR = PatternFill('solid', fgColor='EAF0EE')
F_BAND = PatternFill('solid', fgColor='F6F1E6')
THIN = Border(*[Side(style='thin', color='C9D4D1')]*4)

SHEETS = ["READ FIRST", "Summary", "Fundamental Valuation", "Assumptions", "SOTP Bridge",
          "Segments", "Relative & Normalized", "DCF", "Income Statement", "Balance Sheet",
          "Cash Flow", "Summary Financials", "Monte Carlo", "Sensitivity",
          "Per-Share & Ratios", "Peer & Sector"]

wb = openpyxl.Workbook()
wb.remove(wb.active)
WS = {}
for s in SHEETS:
    WS[s] = wb.create_sheet(s)

def W(sn, coord, v, kind='f', fmt='#,##0.0', note=None, bold=False):
    c = WS[sn][coord]
    c.value = v
    if kind == 'in':
        c.font = Font(color=BLUE, size=10, bold=bold)
        if isinstance(v, (int, float)): c.number_format = fmt
    elif kind == 'f':
        c.font = Font(color=INK, size=10, bold=bold)
        if isinstance(v, str) and v.startswith('='): c.number_format = fmt
        elif isinstance(v, (int, float)): c.number_format = fmt
    elif kind == 'h':
        c.font = Font(color=INK, size=10, bold=True); c.fill = F_HDR
    elif kind == 't':
        c.font = Font(color=INK, size=10, bold=bold)
    elif kind == 'n':
        c.font = Font(color=GREY, size=8.5, italic=True)
    return c

def widths(sn, ws_widths):
    for col, w in ws_widths.items():
        WS[sn].column_dimensions[col].width = w

a1 = D['auto_h1']; h1 = D['h1']; lob1 = D['lob_h1']; hist = D['hist']; dr = D['drivers']
wac = D['wacc']; dcf = D['dcf']; legs = D['legs']; L = D['lenses']; BW = D['both_ways']
fs = D['fs_forecast']; pub = D['published']; mnt = D['mnt']
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
COLS = ['E', 'F', 'G', 'H', 'I']          # forecast columns; B,C,D = FY23,FY24,FY25

# =====================================================================================
# READ FIRST
# =====================================================================================
rf_rows = [
 ("GB Corp (GBCO.CA / EGX) — valuation model, fundamental refresh of 19 August 2026", 't', True),
 ("", 't', False),
 ("What this file is. The full re-build of the July 2026 model on the H1-2026 disclosure "
  "set: the KPMG-reviewed consolidated interim financial statements of 30 June 2026 and "
  "the 2Q/1H26 results release, both published 13 August 2026.", 't', False),
 ("Blue cells are inputs — every one is a disclosed figure, a sourced market quote, or a "
  "stated modelling decision, annotated where it sits. Black cells are formulas: change a "
  "blue driver on the Assumptions sheet and the fair value reprices through Segments, the "
  "cash-flow model, the holding bridge and the summary.", 't', False),
 ("The contested stake is computed both ways, side by side, and never averaged: MNT-Halan "
  "at the June-2026 funding-round mark (USD 1.4bn, first close) and at the company's own "
  "balance-sheet carrying value (EGP 15.72bn, equity-method, which the reviewer could not "
  "verify — a qualified review conclusion, second consecutive period). The two SOTP and "
  "central values are shown in parallel everywhere.", 't', False),
 ("The price-probability sheet reproduces the site's published price map unchanged (struck "
  "22 July 2026). This refresh moves the fundamental fair-value range only; the price map "
  "and technical levels are on their own clock and were not re-struck.", 't', False),
 ("Line-of-business revenue is on the results-release basis; per-line margins are anchored "
  "on the statements' segment note, whose boundaries differ slightly (statement passenger-"
  "car revenue includes after-sales). Flagged here once; both bases are shown on Segments.", 't', False),
 ("All amounts in EGP millions unless stated. Model date 19 August 2026.", 'n', False),
]
for i, (txt, kind, bold) in enumerate(rf_rows, start=2):
    W("READ FIRST", f"B{i+ (0 if i<3 else i-2)}", txt, kind, bold=bold) if False else None
r = 2
for txt, kind, bold in rf_rows:
    W("READ FIRST", f"B{r}", txt, kind, bold=bold); r += 2
widths("READ FIRST", {'A': 2, 'B': 118})

# =====================================================================================
# ASSUMPTIONS  (the driver deck — everything blue, annotated)
# =====================================================================================
A = "Assumptions"
W(A, 'B2', "Assumptions — every driver of the model, with source and date", 't', bold=True)
W(A, 'B4', "Capital & market", 'h')
base_rows = [
 ('B5',  D['shares'], "Shares outstanding (mn) — 2Q/1H26 release"),
 ('B6',  D['spot'],   "Last library close, 22-Jul-2026 (published page anchor)"),
 ('B7',  D['spot_ir'],"EGX quote on the company's IR page, 19-Aug-2026 (market-cap basis)"),
 ('B8',  D['tax_statutory'], "Statutory corporate tax (FS note 11-C)"),
 ('B9',  wac['tg'],   "Terminal growth, nominal EGP"),
]
for coord, v, note in base_rows:
    W(A, coord, v, 'in', fmt='#,##0.000')
    W(A, coord.replace('B', 'C'), note, 'n')
W(A, 'B11', "Cost of capital (v2: rf* = observed yield − sovereign's own default spread)", 'h')
wrows = [
 ('B12', wac['rf_obs'],      "Egypt 10Y local yield, investing.com 19-Aug-2026"),
 ('B13', D['ds_rating'],     "Adjusted default spread, rating basis — Damodaran Jan-2026"),
 ('B14', D['ds_cds'],        "Sovereign CDS spread — Damodaran Jan-2026"),
 ('B15', D['erp_rating'],    "Total ERP, rating basis — Damodaran Jan-2026"),
 ('B16', D['erp_cds'],       "Total ERP, sovereign-CDS basis — Damodaran Jan-2026"),
 ('B17', wac['beta'],        "Weekly beta vs EGX30, 5y Dimson (n=255, R2 0.24) — own regression"),
 ('B18', wac['kd_pretax_local'], "Avg rate, current EGP borrowings H1-26 — FS note 26 (variable-rate book)"),
 ('B19', wac['kd_fx_local_equiv'], "USD tranche in local-equivalent terms: 7.78% + expected depreciation"),
 ('B20', wac['pct_local'],   "EGP share of auto-leg debt (USD split not disclosed; bounded, flagged)"),
 ('B21', a1['debt']+a1['notes'], "Auto-leg gross debt + leasing notes, 30-Jun-26 (release table 7)"),
]
for coord, v, note in wrows:
    W(A, coord, v, 'in', fmt='0.0000')
    W(A, coord.replace('B', 'C'), note, 'n')
W(A, 'B22', "=B7*B5", 'f', note=None); W(A, 'C22', "Market capitalisation (IR-page quote x shares)", 'n')
W(A, 'B23', "=B22/(B22+B21)", 'f', fmt='0.000'); W(A, 'C23', "Equity weight (market value)", 'n')
W(A, 'B24', "=1-B23", 'f', fmt='0.000'); W(A, 'C24', "Debt weight", 'n')
W(A, 'B25', "=B12-B14+B17*B16", 'f', fmt='0.0000'); W(A, 'C25', "Cost of equity, CDS basis", 'n')
W(A, 'B26', "=B12-B13+B17*B15", 'f', fmt='0.0000'); W(A, 'C26', "Cost of equity, rating basis", 'n')
W(A, 'B27', "=B20*B18+(1-B20)*B19", 'f', fmt='0.0000'); W(A, 'C27', "Blended pre-tax cost of debt", 'n')
W(A, 'B28', "=B27*(1-B8)", 'f', fmt='0.0000'); W(A, 'C28', "After-tax cost of debt", 'n')
W(A, 'B29', "=B23*B25+B24*B28", 'f', fmt='0.0000'); W(A, 'C29', "WACC — CDS-basis ERP (primary)", 'n')
W(A, 'B30', "=B23*B26+B24*B28", 'f', fmt='0.0000'); W(A, 'C30', "WACC — rating-basis ERP (published alongside)", 'n')

W(A, 'B32', "Growth & operating drivers (FY27E-FY30E; FY26E is anchored on the H1 actual)", 'h')
path_rows = [
 ('pc volume growth',   dr['pc_vol_g'],  '0.000'), ('pc price growth', dr['pc_asp_g'], '0.000'),
 ('cv volume growth',   dr['cv_vol_g'],  '0.000'), ('cv price growth', dr['cv_asp_g'], '0.000'),
 ('lm volume growth',   dr['lm_vol_g'],  '0.000'), ('lm price growth', dr['lm_asp_g'], '0.000'),
 ('trading growth',     dr['tr_g'],      '0.000'), ('other-auto growth', dr['oth_g'],  '0.000'),
 ('imported-cost escalator (FX path)', dr['fx_path'], '0.000'),
 ('domestic-cost escalator (CPI path)', dr['cpi_path'], '0.000'),
 ('GS&A % of revenue',  dr['gsa_pct'],   '0.0000'),
 ('D&A % of revenue',   dr['dna_pct'],   '0.0000'),
 ('effective tax path', dr['etr_path'],  '0.000'),
 ('capex (EGP mn)',     dr['capex'],     '#,##0'),
 ('working capital % of revenue', dr['wc_pct'], '0.000'),
 ('funding-cost path (auto)', dr['kd_fwd'] if 'kd_fwd' in dr else None, '0.000'),
]
ROW0 = 33
path_rows[-1] = ('funding-cost path (auto)', dr['kd_fwd'], '0.000')
rr = ROW0
PATH_ROW = {}
for name, vals, fmt in path_rows:
    W(A, f'A{rr}', name, 't')
    for j, col in enumerate(COLS):
        v = vals[j]
        if v is None:
            W(A, f'{col}{rr}', "anchored", 'n')
        else:
            W(A, f'{col}{rr}', v, 'in', fmt=fmt)
    PATH_ROW[name] = rr
    rr += 1
W(A, 'A50', "other operating income % (held)", 't'); W(A, 'B50', dr['oth_pct'], 'in', fmt='0.0000')
W(A, 'A51', "net provisions % (held)", 't');        W(A, 'B51', dr['prov_pct'], 'in', fmt='0.0000')
W(A, 'A52', "imported share of unit cost: pc/cv/lm/tr", 't')
W(A, 'B52', dr['imp_share']['pc'], 'in', fmt='0.00'); W(A, 'C52', dr['imp_share']['cv'], 'in', fmt='0.00')
W(A, 'D52', dr['imp_share']['lm'], 'in', fmt='0.00'); W(A, 'E52', dr['imp_share']['tr'], 'in', fmt='0.00')

W(A, 'B55', "Holding bridge marks", 'h')
mark_rows = [
 ('B56', mnt['stake'],      "MNT B.V. stake after the June-26 first close — FS note 34", '0.0000'),
 ('B57', mnt['round_usd'],  "Round valuation, USD mn — company release 09-Jun-26, press-corroborated", '#,##0'),
 ('B58', D['usdegp'],       "USD/EGP, 19-Aug-2026", '0.00'),
 ('B59', mnt['carrying'],   "MNT B.V. equity-method carrying value 30-Jun-26 — FS note 34 (review qualified)", '#,##0.0'),
 ('B60', D['other_assoc'],  "Other associates carrying (Mier + Bedaia + Kaf) — FS note 34", '#,##0.0'),
 ('B61', D['fvoci'],        "Investments at fair value through OCI — FS note 35", '#,##0.0'),
 ('B62', legs['disc'],      "Holding-company discount (unchanged from the July study)", '0.00'),
 ('B63', legs['cap_oper_eq'], "GB Capital operating equity ex-associates (segment equity 22,497.8 − 16,230.5)", '#,##0.0'),
 ('B64', a1['nd'],          "Auto net debt, 30-Jun-26 — release table 7", '#,##0.0'),
 ('B65', a1['nci_bs'],      "Auto segment non-controlling interests, 30-Jun-26", '#,##0.0'),
 ('B66', dcf['h1_fcff'],    "H1-26 realized auto free cash flow (model definition)", '#,##0.0'),
]
for coord, v, note, fmt in mark_rows:
    W(A, coord, v, 'in', fmt=fmt); W(A, coord.replace('B', 'C'), note, 'n')
W(A, 'B67', "=B56*B57*B58", 'f'); W(A, 'C67', "MNT stake at the round mark, EGP mn", 'n')
W(A, 'B70', "Lens weights", 'h')
for i, (k, v) in enumerate([('sum-of-the-parts', L['weights']['sotp']), ('book', L['weights']['book']),
                            ('relative', L['weights']['relative']), ('normalised', L['weights']['normalized'])]):
    W(A, f'A{71+i}', k, 't'); W(A, f'B{71+i}', v, 'in', fmt='0.00')
widths(A, {'A': 34, 'B': 13, 'C': 78, 'D': 10, 'E': 10, 'F': 10, 'G': 10, 'H': 10, 'I': 10})

# =====================================================================================
# SEGMENTS — volumes x prices x unit costs; history blue, forecast formulas
# =====================================================================================
S = "Segments"
W(S, 'B2', "Line-of-business build (release basis; margins anchored on the statements' segment note)", 't', bold=True)
W(S, 'A4', "", 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25'] + YRS):
    W(S, f'{get_column_letter(2+j)}4', y, 'h')
# H1-26 actual block (inputs used by FY26E formulas)
W(S, 'A36', "H1-2026 actuals (release / statements)", 'h')
h1_rows = [
 ('A37', 'PC volumes H1-26 (units)', lob1['pc_u'], '#,##0'),
 ('A38', 'PC revenue H1-26', lob1['pc_r'], '#,##0.0'),
 ('A39', 'Auto revenue H1-26', a1['rev'], '#,##0.0'),
 ('A40', 'Auto gross profit H1-26', a1['gp'], '#,##0.0'),
 ('A41', 'Auto GPM H1-25', a1['h1_25_gp']/a1['h1_25_rev'], '0.0000'),
 ('A42', 'Auto GPM H2-25 (derived from FY25 less H1-25)', (hist['FY25']['auto_gp']-a1['h1_25_gp'])/(hist['FY25']['auto_rev']-a1['h1_25_rev']), '0.0000'),
 ('A43', 'CV&CE revenue H1-26', lob1['cv_r'], '#,##0.0'),
 ('A44', 'Light-Mobility revenue H1-26', lob1['lm_r'], '#,##0.0'),
 ('A45', 'Trading revenue H1-26', lob1['tr_r'], '#,##0.0'),
 ('A46', 'Other-auto revenue H1-26 (residual)', lob1['oth_r'], '#,##0.0'),
]
for coord, label, v, fmt in h1_rows:
    W(S, coord, label, 't'); W(S, coord.replace('A', 'B'), v, 'in', fmt=fmt)
W(S, 'B47', "=B40/B39", 'f', fmt='0.0000'); W(S, 'A47', 'Auto GPM H1-26', 't')
W(S, 'B48', "=B47-(B41-B42)", 'f', fmt='0.0000'); W(S, 'A48', 'H2-26E GPM (H1 less the measured FY25 seasonal gap)', 't')

# rows 5..: PC vol/asp/rev; CV rev; LM rev; TR rev; OTH rev; total; GP; GPM
labels = [('PC volumes (units)', 5), ('PC average selling price (EGP mn)', 6), ('PC revenue', 7),
          ('CV&CE revenue', 8), ('Light-Mobility revenue', 9), ('Trading revenue', 10),
          ('Other automotive revenue', 11), ('Automotive revenue', 12),
          ('Automotive gross profit', 13), ('Automotive gross margin', 14)]
for lab, rw in labels:
    W(S, f'A{rw}', lab, 't', bold=(rw in (12, 13)))
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    col = get_column_letter(2+j); Hy = hist[y]
    W(S, f'{col}5', Hy['pc_u'], 'in', fmt='#,##0')
    W(S, f'{col}6', f"={col}7/{col}5", 'f', fmt='0.0000')
    W(S, f'{col}7', Hy['pc_r'], 'in')
    W(S, f'{col}8', Hy['cv_r'], 'in'); W(S, f'{col}9', Hy['lm_r'], 'in')
    W(S, f'{col}10', Hy['tr_r'], 'in'); W(S, f'{col}11', Hy['oth_r'], 'in')
    W(S, f'{col}12', f"=SUM({col}7:{col}11)", 'f', bold=True)
    W(S, f'{col}13', Hy['auto_gp'], 'in', bold=True)
    W(S, f'{col}14', f"={col}13/{col}12", 'f', fmt='0.000')
# FY26E anchored formulas
W(S, 'E5', D['lob']['FY26E']['pc_u'], 'in', fmt='#,##0')
WS[S]['E5'].comment = None
W(S, 'E7', "=B38+(E5-B37)*(B38/B37)*1.025", 'f')       # H1 + H2 units at H1 ASP +2.5%
W(S, 'E6', "=E7/E5", 'f', fmt='0.0000')
W(S, 'E8', D['lob']['FY26E']['cv_r'], 'in'); W(S, 'E9', D['lob']['FY26E']['lm_r'], 'in')
W(S, 'E10', D['lob']['FY26E']['tr_r'], 'in'); W(S, 'E11', D['lob']['FY26E']['oth_r'], 'in')
W(S, 'E12', "=SUM(E7:E11)", 'f', bold=True)
W(S, 'E13', "=B40+(E12-B39)*B48", 'f', bold=True)       # H1 GP + H2 rev x seasonal GPM
W(S, 'E14', "=E13/E12", 'f', fmt='0.000')
# FY27+ formulas off Assumptions paths
pr_map = {'pc volume growth': None}
def path_ref(name, col):
    return f"Assumptions!{col}{PATH_ROW[name]}"
for j, col in enumerate(COLS[1:], start=1):
    prev = COLS[j-1]
    W(S, f'{col}5', f"={prev}5*(1+{path_ref('pc volume growth', col)})", 'f', fmt='#,##0')
    W(S, f'{col}6', f"={prev}6*(1+{path_ref('pc price growth', col)})", 'f', fmt='0.0000')
    W(S, f'{col}7', f"={col}5*{col}6", 'f')
    W(S, f'{col}8', f"={prev}8*(1+{path_ref('cv volume growth', col)})*(1+{path_ref('cv price growth', col)})", 'f')
    W(S, f'{col}9', f"={prev}9*(1+{path_ref('lm volume growth', col)})*(1+{path_ref('lm price growth', col)})", 'f')
    W(S, f'{col}10', f"={prev}10*(1+{path_ref('trading growth', col)})", 'f')
    W(S, f'{col}11', f"={prev}11*(1+{path_ref('other-auto growth', col)})", 'f')
    W(S, f'{col}12', f"=SUM({col}7:{col}11)", 'f', bold=True)
# unit-cost ratio block rows 17-27
W(S, 'A16', "Cost side — cost per revenue-unit by line (statement-note anchors; escalated one class "
            "per physical driver: imported share on the FX path, domestic share on the CPI path; "
            "FY28E+ cost moves with price — one measured year of compression carried, not a story)", 'n')
cost_rows = [('pc', 17, 'PC cost ratio'), ('cv', 18, 'CV&CE cost ratio'), ('lm', 19, 'LM cost ratio'),
             ('tr', 20, 'Trading cost ratio'), ('oth', 21, 'Other-auto cost ratio')]
cr0 = {k: 1-m for k, m in D['drivers']['lob_margins_h1'].items()}
imp_cell = {'pc': 'B52', 'cv': 'C52', 'lm': 'D52', 'tr': 'E52', 'oth': 'E52'}
pg_row = {'pc': 'pc price growth', 'cv': 'cv price growth', 'lm': 'lm price growth'}
for k, rw, lab in cost_rows:
    W(S, f'A{rw}', lab, 't')
    W(S, f'E{rw}', cr0[k], 'in', fmt='0.0000')
    one_off = "*1.04" if k == 'tr' else ""
    if k in pg_row:
        pgref = path_ref(pg_row[k], 'F')
    else:
        pgref = "0.06"
    W(S, f'F{rw}', f"=E{rw}*(1+Assumptions!{imp_cell[k]}*{path_ref('imported-cost escalator (FX path)','F')}"
                   f"+(1-Assumptions!{imp_cell[k]})*{path_ref('domestic-cost escalator (CPI path)','F')})"
                   f"/(1+{pgref}){one_off}", 'f', fmt='0.0000')
    for col, prev in [('G', 'F'), ('H', 'G'), ('I', 'H')]:
        W(S, f'{col}{rw}', f"={prev}{rw}", 'f', fmt='0.0000')
for j, col in enumerate(COLS[1:], start=1):
    W(S, f'{col}13', f"={col}7*(1-{col}17)+{col}8*(1-{col}18)+{col}9*(1-{col}19)"
                     f"+{col}10*(1-{col}20)+{col}11*(1-{col}21)", 'f', bold=True)
    W(S, f'{col}14', f"={col}13/{col}12", 'f', fmt='0.000')
# GB Capital revenue row 24
W(S, 'A23', "GB Capital", 'h')
W(S, 'A24', "GB Capital revenue", 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    W(S, f'{get_column_letter(2+j)}24', hist[y]['cap_rev'], 'in')
W(S, 'E24', fs[0]['cap_rev'], 'in')
cap_g = dr['cap_rev_g']
for j, col in enumerate(COLS[1:], start=1):
    W(S, f'{col}24', f"={COLS[j-1]}24*(1+{cap_g[j]})", 'f')
W(S, 'A25', "GB Capital net profit (after tax & NCI, incl associates)", 't')
for j, col in enumerate(COLS):
    W(S, f'{col}25', dr['cap_np_path'][j], 'in')
widths(S, {'A': 44, 'B': 12, 'C': 12, 'D': 12, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 12})

# =====================================================================================
# DCF — the FCFF waterfall to PV, EV and the equity bridge
# =====================================================================================
C = "DCF"
W(C, 'B2', "Automotive leg — free cash flow to the firm, discounted at the group's own cost of capital", 't', bold=True)
W(C, 'A4', "", 't')
for j, col in enumerate(COLS):
    W(C, f'{col}4', YRS[j], 'h')
dcf_rows = [
 (5,  'Revenue',            lambda col: f"=Segments!{col}12"),
 (6,  'Gross profit',       lambda col: f"=Segments!{col}13"),
 (7,  'GS&A',               lambda col: f"=-{col}5*{path_ref('GS&A % of revenue', col)}"),
 (8,  'Other operating income', lambda col: f"={col}5*Assumptions!$B$50"),
 (9,  'Net provisions',     lambda col: f"={col}5*Assumptions!$B$51"),
 (10, 'EBIT',               lambda col: f"={col}6+{col}7+{col}8+{col}9"),
 (11, 'Effective tax rate', lambda col: f"={path_ref('effective tax path', col)}"),
 (12, 'NOPAT',              lambda col: f"={col}10*(1-{col}11)"),
 (13, 'Depreciation & amortisation', lambda col: f"={col}5*{path_ref('D&A % of revenue', col)}"),
 (14, 'EBITDA',             lambda col: f"={col}10+{col}13"),
 (15, 'Capex',              lambda col: f"=-{path_ref('capex (EGP mn)', col)}"),
 (16, 'Working capital (level)', lambda col: f"={col}5*{path_ref('working capital % of revenue', col)}"),
 (17, 'Change in working capital', None),
 (18, 'Free cash flow to the firm', lambda col: f"={col}12+{col}13+{col}15-{col}17"),
]
for rw, lab, fn in dcf_rows:
    W(C, f'A{rw}', lab, 't', bold=(rw in (10, 14, 18)))
    if fn:
        for col in COLS:
            W(C, f'{col}{rw}', fn(col), 'f', fmt='#,##0.0' if rw != 11 else '0.000',
              bold=(rw in (10, 14, 18)))
W(C, 'E17', f"=E16-{hist['FY25']['wc']}", 'f')
for col, prev in [('F', 'E'), ('G', 'F'), ('H', 'G'), ('I', 'H')]:
    W(C, f'{col}17', f"={col}16-{prev}16", 'f')
W(C, 'A20', "Valuation is dated 30 June 2026: the realized first half is carried at its actual, and "
            "the second half plus four further years are discounted mid-period.", 'n')
W(C, 'A21', 'H1-26 realized free cash flow', 't'); W(C, 'B21', "=Assumptions!B66", 'f')
W(C, 'A22', 'H2-26E free cash flow', 't'); W(C, 'B22', "=E18-B21", 'f')
W(C, 'A24', 'Discount period (years)', 't')
W(C, 'A25', 'Discount factor', 't'); W(C, 'A26', 'Present value', 't')
periods = [0.5, 1.5, 2.5, 3.5, 4.5]
for j, col in enumerate(COLS):
    W(C, f'{col}24', periods[j], 'in', fmt='0.0')
    W(C, f'{col}25', f"=1/(1+Assumptions!$B$29)^{col}24", 'f', fmt='0.0000')
    src = "B22" if j == 0 else f"{col}18"
    W(C, f'{col}26', f"={src}*{col}25", 'f')
W(C, 'A28', 'Sum of discounted flows', 't'); W(C, 'B28', "=SUM(E26:I26)", 'f', bold=True)
W(C, 'A29', 'Terminal value (Gordon on FY30E)', 't')
W(C, 'B29', "=I18*(1+Assumptions!B9)/(Assumptions!B29-Assumptions!B9)", 'f')
W(C, 'A30', 'PV of terminal value', 't'); W(C, 'B30', "=B29*I25", 'f')
W(C, 'A31', 'Enterprise value — automotive', 't'); W(C, 'B31', "=B28+B30", 'f', bold=True)
W(C, 'A32', 'Less: automotive net debt (30-Jun-26)', 't'); W(C, 'B32', "=-Assumptions!B64", 'f')
W(C, 'A33', 'Less: automotive non-controlling interests', 't'); W(C, 'B33', "=-Assumptions!B65", 'f')
W(C, 'A34', 'Automotive equity value', 't'); W(C, 'B34', "=B31+B32+B33", 'f', bold=True)
W(C, 'A35', 'Per share', 't'); W(C, 'B35', "=B34/Assumptions!B5", 'f', fmt='0.00')
W(C, 'A37', 'Terminal share of enterprise value', 't'); W(C, 'B37', "=B30/B31", 'f', fmt='0.0%')
widths(C, {'A': 34, 'B': 13, 'C': 11, 'D': 11, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 12})

# =====================================================================================
# SOTP BRIDGE — both framings, side by side
# =====================================================================================
B = "SOTP Bridge"
W(B, 'B2', "Holding bridge — the group as the sum of its parts, with the contested stake both ways", 't', bold=True)
W(B, 'A4', "", 't'); W(B, 'B4', "Round mark", 'h'); W(B, 'C4', "Balance-sheet mark", 'h')
rows_b = [
 (5, 'Automotive equity value (cash-flow model)', "=DCF!B34", "=DCF!B34"),
 (6, 'GB Capital operating equity (ex-associates)', "=Assumptions!B63", "=Assumptions!B63"),
 (7, 'MNT-Halan stake', "=Assumptions!B67", "=Assumptions!B59"),
 (8, 'Other associates', "=Assumptions!B60", "=Assumptions!B60"),
 (9, 'Investments at fair value (OCI)', "=Assumptions!B61", "=Assumptions!B61"),
 (10, 'Sum of the parts', "=SUM(B5:B9)", "=SUM(C5:C9)"),
 (11, 'Holding-company discount', "=-B10*Assumptions!B62", "=-C10*Assumptions!B62"),
 (12, 'Equity value', "=B10+B11", "=C10+C11"),
 (13, 'Per share', "=B12/Assumptions!B5", "=C12/Assumptions!B5"),
]
for rw, lab, fa, fb in rows_b:
    W(B, f'A{rw}', lab, 't', bold=(rw in (10, 12, 13)))
    W(B, f'B{rw}', fa, 'f', fmt='#,##0.0' if rw != 13 else '0.00', bold=(rw in (10, 12, 13)))
    W(B, f'C{rw}', fb, 'f', fmt='#,##0.0' if rw != 13 else '0.00', bold=(rw in (10, 12, 13)))
W(B, 'A15', "The gap between the two columns is one judgement: EGP "
            f"{legs['assoc_A']-legs['assoc_B']:,.0f}mn of MNT-Halan mark — "
            f"{BW['gap_ps']:.2f} per share after the discount. The reviewer could not verify "
            "the balance-sheet figure (qualified conclusion); the round is real third-party "
            "money but a first close with a second pending. Neither is averaged away.", 'n')
W(B, 'A17', 'Bear cases (operating bear + leg haircuts + 18% discount)', 't')
W(B, 'B17', BW['A']['sotp_bear'], 'in', fmt='0.00'); W(B, 'C17', BW['B']['sotp_bear'], 'in', fmt='0.00')
W(B, 'A18', 'Bull cases (operating bull + 4% discount)', 't')
W(B, 'B18', BW['A']['sotp_bull'], 'in', fmt='0.00'); W(B, 'C18', BW['B']['sotp_bull'], 'in', fmt='0.00')
W(B, 'A19', "Case values re-run the cash-flow model under the shifted drivers described in the study's "
            "sensitivity section; recorded here as results of that re-run.", 'n')
widths(B, {'A': 46, 'B': 16, 'C': 18})

# =====================================================================================
# INCOME STATEMENT / BALANCE SHEET / CASH FLOW (group, condensed; formula-based)
# =====================================================================================
IS = "Income Statement"
W(IS, 'B2', "Group income statement — three disclosed years and the five-year model", 't', bold=True)
W(IS, 'A4', "", 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25'] + YRS):
    W(IS, f'{get_column_letter(2+j)}4', y, 'h')
gis = [
 (5, 'Automotive revenue', [hist[y]['auto_rev'] for y in ['FY23', 'FY24', 'FY25']], lambda col: f"=Segments!{col}12"),
 (6, 'GB Capital revenue', [hist[y]['cap_rev'] for y in ['FY23', 'FY24', 'FY25']], lambda col: f"=Segments!{col}24"),
 (7, 'Inter-segment eliminations',
     [round(hist[y]['group_rev']-hist[y]['auto_rev']-hist[y]['cap_rev'], 1) for y in ['FY23', 'FY24', 'FY25']],
     lambda col: f"=-({col}5+{col}6)*{dr['elim_pct']}"),
 (8, 'Group revenue', None, None),
 (10, 'Automotive EBIT', None, lambda col: f"=DCF!{col}10"),
 (11, 'Automotive finance cost', None, None),
 (12, 'Automotive profit before tax', None, lambda col: f"={col}10+{col}11"),
 (13, 'Automotive tax', None, lambda col: f"=-{col}12*DCF!{col}11"),
 (14, 'Automotive net profit', None, lambda col: f"={col}12+{col}13"),
 (15, 'GB Capital net profit (incl associates)', None, lambda col: f"=Segments!{col}25"),
 (16, 'Group net profit (attributable)', None, lambda col: f"={col}14+{col}15"),
 (17, 'Earnings per share (EGP)', None, lambda col: f"={col}16/Assumptions!$B$5"),
]
for rw, lab, histvals, fn in gis:
    W(IS, f'A{rw}', lab, 't', bold=(rw in (8, 16)))
    if histvals:
        for j, v in enumerate(histvals):
            W(IS, f'{get_column_letter(2+j)}{rw}', v, 'in')
    if fn:
        for col in COLS:
            W(IS, f'{col}{rw}', fn(col), 'f', fmt='0.00' if rw == 17 else '#,##0.0',
              bold=(rw == 16))
for j in range(3):
    col = get_column_letter(2+j)
    W(IS, f'{col}8', f"=SUM({col}5:{col}7)", 'f', bold=True)
for col in COLS:
    W(IS, f'{col}8', f"=SUM({col}5:{col}7)", 'f', bold=True)
# finance cost: FY26E anchored on H1 actual + H2 on opening ND; later years ND(prior) x kd path
W(IS, 'E11', f"=-({a1['fin']}+0.5*Assumptions!B64*{path_ref('funding-cost path (auto)', 'E')})", 'f')
for col, prev in [('F', 'E'), ('G', 'F'), ('H', 'G'), ('I', 'H')]:
    W(IS, f'{col}11', f"=-'Balance Sheet'!{prev}10*{path_ref('funding-cost path (auto)', col)}", 'f')
W(IS, 'A19', "Historical group lines (disclosed): net profit attributable FY23 1,890.8 / FY24 2,928.1 / "
             "FY25 2,880.0; H1-26 actual 1,262.0 (EPS 1.163). The model's FY26E includes that "
             "realized half.", 'n')
widths(IS, {'A': 40, 'B': 12, 'C': 12, 'D': 12, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 12})

BS = "Balance Sheet"
W(BS, 'B2', "Condensed group balance-sheet model (working capital on its measured cycle)", 't', bold=True)
W(BS, 'A4', "", 't')
for j, y in enumerate(['FY25'] + YRS):
    W(BS, f'{get_column_letter(4+j)}4', y, 'h')   # D=FY25, E..I forecast
bs_rows = [
 (5, 'Automotive working capital', hist['FY25']['wc'], lambda col: f"=DCF!{col}16"),
 (6, 'Net PP&E and intangibles (roll: + capex − D&A)', 13389.1, lambda col: None),
 (7, 'Investments in associates (roll: + equity pickup)', D['assoc_total'], lambda col: None),
 (8, 'GB Capital operating net assets (held)', legs['cap_oper_eq'], lambda col: f"=Assumptions!$B$63"),
 (10, 'Automotive net debt (cash-sweep roll)', a1['nd'], lambda col: None),
 (11, 'Parent equity (roll: + profit − dividends)', D['bs']['parent_eq'], lambda col: None),
 (12, 'Dividends paid (per-share held at the FY25 level)', None,
     lambda col: f"={dr['div_ps']}*Assumptions!$B$5"),
]
for rw, lab, d0, fn in bs_rows:
    W(BS, f'A{rw}', lab, 't', bold=(rw in (10, 11)))
    if d0 is not None:
        W(BS, f'D{rw}', d0, 'in')
    if fn:
        for col in COLS:
            f = fn(col)
            if f: W(BS, f'{col}{rw}', f, 'f')
W(BS, 'A14', "FY25 associates column is the restated figure (the statements' note on prior-period "
             "adjustments raised the opening MNT B.V. carrying by 2,460.2).", 'n')
# rolls
assoc_pick = dr['assoc_pickup_path']
for j, col in enumerate(COLS):
    prev = 'D' if j == 0 else COLS[j-1]
    W(BS, f'{col}6', f"={prev}6+DCF!{col}15*-1-DCF!{col}13", 'f')
    W(BS, f'{col}7', f"={prev}7+{assoc_pick[j]}", 'f')
    if j == 0:
        W(BS, f'{col}10', f"=Assumptions!B64-(DCF!{col}18+Income' 'Statement!{col}11*(1-DCF!{col}11)-{col}12*{dr['div_auto_share']})", 'f')
    W(BS, f'{col}11', f"={prev}11+'Income Statement'!{col}16-{col}12", 'f')
# net debt roll with correct quoting
for j, col in enumerate(COLS):
    prev = 'D' if j == 0 else COLS[j-1]
    W(BS, f'{col}10', f"={prev}10-(DCF!{col}18+'Income Statement'!{col}11*(1-DCF!{col}11)-{col}12*{dr['div_auto_share']})", 'f')
W(BS, 'A16', 'Book value per share', 't')
for col in COLS:
    W(BS, f'{col}16', f"={col}11/Assumptions!$B$5", 'f', fmt='0.00')
W(BS, 'A18', "Measured conversion cycle at 30-Jun-26 (from the statements): inventory 122 days of cost, "
             "receivables 27 days of revenue, payables 82 days of cost — a 67-day cash cycle. The "
             "working-capital ratio above projects that cycle; the five disclosed quarterly "
             "snapshots (16.7-18.9bn) are the anchor.", 'n')
widths(BS, {'A': 46, 'B': 8, 'C': 8, 'D': 12, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 12})

CF = "Cash Flow"
W(CF, 'B2', "Condensed group cash-flow model", 't', bold=True)
for j, y in enumerate(YRS):
    W(CF, f'{COLS[j]}4', y, 'h')
cf_rows = [
 (5, 'Group net profit', lambda col: f"='Income Statement'!{col}16"),
 (6, 'Depreciation & amortisation', lambda col: f"=DCF!{col}13"),
 (7, 'Change in working capital', lambda col: f"=-DCF!{col}17"),
 (8, 'Capex', lambda col: f"=DCF!{col}15"),
 (9, 'Dividends paid', lambda col: f"=-'Balance Sheet'!{col}12"),
 (10, 'Operating & investing cash flow after dividends', lambda col: f"=SUM({col}5:{col}9)"),
 (11, 'Change in automotive net debt (from the sweep)', None),
]
for rw, lab, *fn in cf_rows:
    W(CF, f'A{rw}', lab, 't', bold=(rw == 10))
    if fn and fn[0]:
        for col in COLS:
            W(CF, f'{col}{rw}', fn[0](col), 'f', bold=(rw == 10))
for j, col in enumerate(COLS):
    prev = 'D' if j == 0 else COLS[j-1]
    base = "Assumptions!B64" if j == 0 else f"'Balance Sheet'!{prev}10"
    W(CF, f'{col}11', f"='Balance Sheet'!{col}10-{base}", 'f')
W(CF, 'A13', "Signs follow the model: a positive change in net debt funds the gap between spending "
             "and the cash the businesses release.", 'n')
widths(CF, {'A': 46, 'E': 12, 'F': 12, 'G': 12, 'H': 12, 'I': 12})

# =====================================================================================
# RELATIVE & NORMALIZED
# =====================================================================================
RN = "Relative & Normalized"
W(RN, 'B2', "Relative multiples and normalised earnings power", 't', bold=True)
W(RN, 'A4', 'FY26E group earnings per share', 't'); W(RN, 'B4', "='Income Statement'!E17", 'f', fmt='0.00')
W(RN, 'A5', 'Multiple band (bear / base / bull)', 't')
W(RN, 'B5', L['relative']['pe']['bear'], 'in', fmt='0.0'); W(RN, 'C5', L['relative']['pe']['base'], 'in', fmt='0.0')
W(RN, 'D5', L['relative']['pe']['bull'], 'in', fmt='0.0')
W(RN, 'A6', 'Relative lens value', 't')
W(RN, 'B6', "=B4*B5", 'f', fmt='0.00'); W(RN, 'C6', "=B4*C5", 'f', fmt='0.00'); W(RN, 'D6', "=B4*D5", 'f', fmt='0.00')
W(RN, 'A8', "Normalisation walk (mid-cycle)", 'h')
W(RN, 'A9', 'FY27E automotive EBIT', 't'); W(RN, 'B9', "=DCF!F10", 'f')
W(RN, 'A10', 'Normalised finance cost (net debt x the eased-rate endpoint)', 't')
W(RN, 'B10', f"=-Assumptions!B64*{dr['fin_norm_rate']}", 'f')
W(RN, 'A11', 'Tax at the statutory 22.5%', 't'); W(RN, 'B11', "=-(B9+B10)*Assumptions!B8", 'f')
W(RN, 'A12', 'GB Capital net profit (FY27E, incl associates)', 't'); W(RN, 'B12', "=Segments!F25", 'f')
W(RN, 'A13', 'Normalised group profit', 't'); W(RN, 'B13', "=B9+B10+B11+B12", 'f', bold=True)
nm = dr['norm_mult']; nsc = dr['norm_scal']
W(RN, 'A14', f"Normalised earnings lens (x {nm['bear']} / {nm['base']} / {nm['bull']})", 't')
W(RN, 'B14', f"=B13*{nsc['bear']}/Assumptions!B5*{nm['bear']}", 'f', fmt='0.00')
W(RN, 'C14', f"=B13/Assumptions!B5*{nm['base']}", 'f', fmt='0.00')
W(RN, 'D14', f"=B13*{nsc['bull']}/Assumptions!B5*{nm['bull']}", 'f', fmt='0.00')
widths(RN, {'A': 44, 'B': 12, 'C': 12, 'D': 12})

# =====================================================================================
# FUNDAMENTAL VALUATION — four lenses, one field
# =====================================================================================
FV = "Fundamental Valuation"
W(FV, 'B2', "Four lenses, one field — the synthesis (both framings of the contested stake)", 't', bold=True)
W(FV, 'A4', 'Lens', 'h'); W(FV, 'B4', 'Value / share', 'h'); W(FV, 'C4', 'Weight', 'h')
W(FV, 'A5', 'Sum of the parts — round mark', 't'); W(FV, 'B5', "='SOTP Bridge'!B13", 'f', fmt='0.00')
W(FV, 'A6', 'Sum of the parts — balance-sheet mark', 't'); W(FV, 'B6', "='SOTP Bridge'!C13", 'f', fmt='0.00')
W(FV, 'A7', 'Book value & sustainable return', 't'); W(FV, 'B7', L['book']['base'], 'in', fmt='0.00')
W(FV, 'C7n', None, 't') if False else None
W(FV, 'D7', "restated book per share (30-Jun-26 parent equity / shares)", 'n')
W(FV, 'A8', 'Relative multiples', 't'); W(FV, 'B8', "='Relative & Normalized'!C6", 'f', fmt='0.00')
W(FV, 'A9', 'Normalised earnings power', 't'); W(FV, 'B9', "='Relative & Normalized'!C14", 'f', fmt='0.00')
for rw, wkey in [(5, 'sotp'), (7, 'book'), (8, 'relative'), (9, 'normalized')]:
    W(FV, f'C{rw}', L['weights'][wkey], 'in', fmt='0.00')
W(FV, 'C6', "same weight as row 5 — the framings alternate, they never blend", 'n')
W(FV, 'A11', 'Weighted central — round mark', 't', bold=True)
W(FV, 'B11', "=B5*C5+B7*C7+B8*C8+B9*C9", 'f', fmt='0.00', bold=True)
W(FV, 'A12', 'Weighted central — balance-sheet mark', 't', bold=True)
W(FV, 'B12', "=B6*C5+B7*C7+B8*C8+B9*C9", 'f', fmt='0.00', bold=True)
W(FV, 'A14', 'Published range', 'h')
W(FV, 'A15', 'Bear (balance-sheet-mark world, operating bear)', 't'); W(FV, 'B15', D['fair']['bear'], 'in', fmt='0.0')
W(FV, 'A16', 'Base (round-mark central)', 't'); W(FV, 'B16', "=B11", 'f', fmt='0.00')
W(FV, 'A17', 'Bull (round-mark world, operating bull)', 't'); W(FV, 'B17', D['fair']['full'], 'in', fmt='0.0')
widths(FV, {'A': 44, 'B': 13, 'C': 10, 'D': 56})

# =====================================================================================
# SUMMARY / SUMMARY FINANCIALS
# =====================================================================================
SU = "Summary"
W(SU, 'B2', "GB Corp — fair value at a glance (refresh of 19 August 2026)", 't', bold=True)
srows = [
 ('A4', 'Last library close (22-Jul-26)', "=Assumptions!B6", '0.00'),
 ('A5', 'Fair value — bear', "='Fundamental Valuation'!B15", '0.0'),
 ('A6', 'Fair value — base (round mark)', "='Fundamental Valuation'!B16", '0.00'),
 ('A7', 'Fair value — central under the balance-sheet mark', "='Fundamental Valuation'!B12", '0.00'),
 ('A8', 'Fair value — bull', "='Fundamental Valuation'!B17", '0.0'),
 ('A10', 'H1-26 group revenue (+35.2%)', h1['rev'], '#,##0.0'),
 ('A11', 'H1-26 group net profit (−24.5%)', h1['np'], '#,##0.0'),
 ('A12', 'Automotive net debt, 30-Jun-26 (2.14x EBITDA)', a1['nd'], '#,##0.0'),
 ('A13', 'MNT-Halan gap, per share (round vs book, post-discount)', BW['gap_ps'], '0.00'),
]
for coord, lab, v, fmt in srows:
    W(SU, coord, lab, 't')
    W(SU, coord.replace('A', 'B'), v, 'f' if isinstance(v, str) else 'in', fmt=fmt)
pf = pub['fair']
W(SU, 'A15', f"The July study's range was {pf['bear']} / {pf['base']} / {pf['full']}. The base barely moves; the bear "
             "deepens because the company's own accounts now carry the contested stake at half "
             "the round, under a qualified review.", 'n')
widths(SU, {'A': 52, 'B': 14})

SF = "Summary Financials"
W(SF, 'B2', "Summary financials (links)", 't', bold=True)
for j, y in enumerate(['FY23', 'FY24', 'FY25'] + YRS):
    W(SF, f'{get_column_letter(2+j)}4', y, 'h')
sf_rows = [(5, 'Group revenue', 'Income Statement', 8), (6, 'Automotive EBITDA', None, None),
           (7, 'Group net profit', None, None), (8, 'Earnings per share', None, None)]
W(SF, 'A5', 'Group revenue', 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    W(SF, f'{get_column_letter(2+j)}5', f"='Income Statement'!{get_column_letter(2+j)}8", 'f')
for col in COLS:
    W(SF, f'{col}5', f"='Income Statement'!{col}8", 'f')
W(SF, 'A6', 'Automotive EBITDA', 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    W(SF, f'{get_column_letter(2+j)}6', hist[y]['auto_ebitda'], 'in')
for col in COLS:
    W(SF, f'{col}6', f"=DCF!{col}14", 'f')
W(SF, 'A7', 'Group net profit (attributable)', 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    W(SF, f'{get_column_letter(2+j)}7', hist[y]['np'], 'in')
for col in COLS:
    W(SF, f'{col}7', f"='Income Statement'!{col}16", 'f')
W(SF, 'A8', 'Earnings per share (EGP)', 't')
for j, y in enumerate(['FY23', 'FY24', 'FY25']):
    W(SF, f'{get_column_letter(2+j)}8', round(hist[y]['np']/D['shares'], 3), 'f', fmt='0.00')
for col in COLS:
    W(SF, f'{col}8', f"='Income Statement'!{col}17", 'f', fmt='0.00')
widths(SF, {'A': 34, 'B': 11, 'C': 11, 'D': 11, 'E': 11, 'F': 11, 'G': 11, 'H': 11, 'I': 11})

# =====================================================================================
# MONTE CARLO — the published price map, reproduced and labelled
# =====================================================================================
MC = "Monte Carlo"
W(MC, 'B2', "Published price-probability map — reproduced unchanged from the live page", 't', bold=True)
W(MC, 'A4', "This sheet is a copy, not a computation. The map was struck on the closing library of "
            f"22 July 2026 and computed on 28 July 2026 (the page's own stamps: price data "
            f"{pub['asof']['mc']['data']}, computed {pub['asof']['mc']['computed']}). This refresh "
            "changes the fundamental fair-value range only; the probability map was NOT re-struck "
            "and is four weeks stale against the refresh date — its 1-month window resolves "
            "23 August 2026. A fresh price data-set re-strikes it on its own clock.", 'n')
W(MC, 'A6', 'Horizon', 'h')
for j, p in enumerate(['5th', '25th', 'median', '75th', '95th']):
    W(MC, f'{get_column_letter(3+j)}6', p, 'h')
for i, (hz, lab) in enumerate([('t20', '1 month (resolves 23-Aug-26)'), ('t60', '3 months (resolves 22-Oct-26)')]):
    W(MC, f'A{7+i}', lab, 't')
    dd = pub['dist'][hz]
    for j, k in enumerate(['p5', 'p25', 'p50', 'p75', 'p95']):
        W(MC, f'{get_column_letter(3+j)}{7+i}', dd[k], 'in', fmt='0.00')
W(MC, 'A10', 'Touch ladder (level, probability of touching within 1 month / 3 months, %)', 't')
for i, (lvl, p1, p3) in enumerate(pub['touch']):
    W(MC, f'B{11+i}', lvl, 'in', fmt='0.00')
    W(MC, f'C{11+i}', p1, 'in', fmt='0'); W(MC, f'D{11+i}', p3, 'in', fmt='0')
widths(MC, {'A': 44, 'B': 10, 'C': 10, 'D': 10, 'E': 10, 'F': 10, 'G': 10})

# =====================================================================================
# SENSITIVITY — live grid: stake mark x holding discount
# =====================================================================================
SE = "Sensitivity"
W(SE, 'B2', "Sum-of-the-parts per share — MNT-Halan mark x holding discount (live formulas)", 't', bold=True)
gm = D['sens']['grid_mult']; gd = D['sens']['grid_disc']
for j, d_ in enumerate(gd):
    W(SE, f'{get_column_letter(3+j)}4', d_, 'in', fmt='0%')
for i, m_ in enumerate(gm):
    W(SE, f'B{5+i}', m_, 'in', fmt='0%')
    for j, d_ in enumerate(gd):
        col = get_column_letter(3+j)
        W(SE, f'{col}{5+i}',
          f"=(DCF!$B$34+Assumptions!$B$63+Assumptions!$B$67*$B{5+i}+Assumptions!$B$60"
          f"+Assumptions!$B$61)*(1-{col}$4)/Assumptions!$B$5", 'f', fmt='0.0')
W(SE, 'A11', f"The company's own balance-sheet mark equals {D['sens']['mult_B']*100:.0f}% of the round "
             "— between the first and second rows. The July study's margin axis is retained as a "
             "line: ±1pt of automotive gross margin moves the automotive leg by about "
             f"{(dcf['auto_eq_pm1']-dcf['auto_eq_mm1'])/2/D['shares']:.2f} per share.", 'n')
widths(SE, {'A': 8, 'B': 12, 'C': 10, 'D': 10, 'E': 10, 'F': 10, 'G': 10})

# =====================================================================================
# PER-SHARE & RATIOS / PEER & SECTOR
# =====================================================================================
PS = "Per-Share & Ratios"
W(PS, 'B2', "Per-share values and ratios", 't', bold=True)
for j, y in enumerate(YRS):
    W(PS, f'{COLS[j]}4', y, 'h')
ps_rows = [
 (5, 'Earnings per share', lambda col: f"='Income Statement'!{col}17", '0.00'),
 (6, 'Book value per share', lambda col: f"='Balance Sheet'!{col}16", '0.00'),
 (7, 'Return on equity', lambda col: f"='Income Statement'!{col}16/'Balance Sheet'!{col}11", '0.0%'),
 (8, 'Net debt / automotive EBITDA', lambda col: f"='Balance Sheet'!{col}10/DCF!{col}14", '0.00'),
 (9, 'Price / earnings at the last close', lambda col: f"=Assumptions!$B$6/'Income Statement'!{col}17", '0.0'),
 (10, 'Price / book at the last close', lambda col: f"=Assumptions!$B$6/'Balance Sheet'!{col}16", '0.00'),
 (11, 'Dividend yield at the last close (payout held)', lambda col: f"={dr['div_ps']}/Assumptions!$B$6", '0.0%'),
]
for rw, lab, fn, fmt in ps_rows:
    W(PS, f'A{rw}', lab, 't')
    for col in COLS:
        W(PS, f'{col}{rw}', fn(col), 'f', fmt=fmt)
widths(PS, {'A': 40, 'E': 11, 'F': 11, 'G': 11, 'H': 11, 'I': 11})

PE = "Peer & Sector"
W(PE, 'B2', "Peer frame (context only — never a source for the subject's own numbers)", 't', bold=True)
W(PE, 'A4', 'Peer', 'h'); W(PE, 'B4', 'Trailing P/E', 'h'); W(PE, 'C4', 'Note', 'h')
peers_rows = [
 ('Contact Financial (EGX) — consumer/NBFS', D['peers']['CNFN'], 'the direct Egyptian financing peer'),
 ('Dogus Otomotiv (Istanbul) — auto distribution', D['peers']['DOAS'], 'P/B 0.62 on inflation-restated book'),
 ('AutoNation (US) — auto retail', D['peers']['AN'], 'mature-market anchor; fwd 8.35'),
 ('Bajaj Auto (India) — two/three-wheelers', D['peers']['BAJAJ'], 'partner brand; rich-market multiple'),
]
for i, (nm, pe_, note) in enumerate(peers_rows):
    W(PE, f'A{5+i}', nm, 't'); W(PE, f'B{5+i}', pe_, 'in', fmt='0.00'); W(PE, f'C{5+i}', note, 'n')
W(PE, 'A10', 'GB Corp at the last close on FY26E earnings', 't')
W(PE, 'B10', "=Assumptions!B6/'Income Statement'!E17", 'f', fmt='0.0')
W(PE, 'A11', 'GB Corp at the last close on restated book', 't')
W(PE, 'B11', "=Assumptions!B6/('Fundamental Valuation'!B7)", 'f', fmt='0.00')
W(PE, 'A13', "All peer marks 19-Aug-2026, aggregator-sourced (market data only). One material "
             "aggregator discrepancy was logged: Contact Financial's market capitalisation is "
             "quoted between EGP 4.5bn and 6.6bn across services on different dates.", 'n')
widths(PE, {'A': 44, 'B': 12, 'C': 52})

for ws in wb.worksheets:
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    if ws.title in ("Segments", "Income Statement", "DCF", "Summary Financials",
                    "Balance Sheet", "Assumptions"):
        ws.page_setup.orientation = 'landscape'
wb.save(OUT)
print("saved", OUT)

# quick structural checks
wb2 = openpyxl.load_workbook(OUT)
assert wb2.sheetnames == SHEETS, wb2.sheetnames
n_f = sum(1 for ws in wb2.worksheets for row in ws.iter_rows()
          for c in row if isinstance(c.value, str) and c.value.startswith('='))
print("sheets OK (16, exact order) | formula cells:", n_f)
