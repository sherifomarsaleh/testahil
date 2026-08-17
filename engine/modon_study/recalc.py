"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json (revision 2). Three gates: every formula evaluates; every
formula cell reproduces the model's own value; headline reconciliations."""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'MODON_Valuation_Model_10082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, LN, HI, HB, F = D['dcf'], D['lenses'], D['hist_is'], D['hist_bs'], D['fcst']
W, REL, NRM, BK = D['wacc'], D['rel'], D['norm'], D['book']
HA = D['h1_anchors']
SH = D['meta']['shares_mn']
AD = ANCH['dcf']

BK_ = xlcalc.Book(wb)
cell_value = BK_.cell_value

nform, errors = 0, []
for sh, coord in BK_.formula_cells():
    nform += 1
    try:
        cell_value(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)

def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)

nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = cell_value(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:25]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK_.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

def g(sheet, cell):
    return cell_value(sheet, cell)

rw = ANCH['dcf_rw']
checks = [
    ('DCF enterprise value', g('DCF', f"C{AD['ev']}"), DCF['ev'], 1.0),
    ('DCF PV of explicit periods', g('DCF', f"C{AD['pex']}"), DCF['pv_explicit'], 1.0),
    ('DCF PV of terminal value', g('DCF', f"C{AD['ptv']}"), DCF['pv_tv'], 1.0),
    ('DCF terminal value share', g('DCF', f"C{AD['tvs']}"), DCF['tv_share'], 0.002),
    ('DCF terminal debt weight (derived)', g('DCF', f"C{AD['wdt']}"), W['wd_term'], 0.001),
    ('DCF fair value per share at 30-Jun-2026', g('DCF', f"C{AD['psd']}"), DCF['ps_jun'], 0.02),
    ('DCF anchor accretion factor', g('DCF', f"C{AD['roll']}"), DCF['roll'], 0.0005),
    ('DCF fair value per share at the anchor', g('DCF', f"C{AD['ps']}"), DCF['ps'], 0.02),
    ('DCF cost of capital — explicit', g('DCF', f"C{AD['wacc']}"), W['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', f"C{AD['wt']}"), W['wacc_term'], 0.0002),
    ('DCF cost of equity (beta 1.03)', g('DCF', f"C{AD['ke']}"), W['ke_exp'], 0.0002),
    ('DCF reinvestment rate = g/ROIC', g('DCF', f"C{AD['rr']}"), DCF['rr_term'], 0.001),
    ('DCF NCI capitalised', g('DCF', f"C{ANCH['nci_row']}"), -DCF['nci_val'], 1.0),
    ('Bridge equity attributable', g('SOTP Bridge', f"C{ANCH['sotp_eq']}"), DCF['eq_attr'], 1.0),
    ('Bridge segment weights sum to EV',
     sum(g('SOTP Bridge', f'C{i}') for i in (6, 7, 8, 9)), DCF['ev'], 1.5),
    ('Fundamental — DCF lens', g('Fundamental Valuation', 'C5'), DCF['ps'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', 'C10'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', 'C11'), LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', 'C12'), LN['book']['base'], 0.02),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Summary market capitalisation', g('Summary', ANCH['summary_mktcap']),
     D['meta']['mktcap'], 1.0),
    ('Relative lens (P/E leg)', g('Relative & Normalized', 'C11'), LN['relative']['base'], 0.02),
    ('Normalised lens', g('Relative & Normalized', 'C28'), LN['normalized']['base'], 0.02),
    ('Book lens (rolled)', g('Relative & Normalized', 'C36'), LN['book']['base'], 0.02),
    ('Segments group FY2025 revenue', g('Segments', f"B{ANCH['seg_rev_tot']}"),
     HI['FY25']['rev'], 1.0),
    ('Segments FY2030E closing backlog', g('Segments', f"F{ANCH['bl_row'] + 3}"),
     F['bl_close'][4], 1.0),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D7'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E attributable profit', g('Income Statement', 'J17'),
     F['np_attr'][4], 1.0),
    ('Balance sheet 30-Jun-26 NWC (components)', g('Balance Sheet', 'E8'),
     F['nwc_30jun'], 1.0),
    ('Balance sheet FY2030E net debt', g('Balance Sheet', 'J13'), F['net_debt'][4], 1.5),
    ('Balance sheet FY2030E cash', g('Balance Sheet', 'J9'), F['cash'][4], 1.5),
    ('Cash flow H2-2026E FCFF', g('Cash Flow', 'E13'), F['fcff'][0], 1.0),
    ('Summary financials FY2030E invested capital', g('Summary Financials', 'J13'),
     F['ic'][4], 1.0),
    ('Peer sheet — Aldar attributable P/E formula', g('Peer & Sector', 'F5'),
     61171.0 / 7548.0, 0.05),
    ('Peer sheet — MODON attributable trailing P/E', g('Peer & Sector', 'F8'),
     D['meta']['mktcap'] / D['inputs']['npa_fy25']['value'], 0.02),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={float(got):,.4f} model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'RECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements, '
      f'{len(checks)} headline reconciliations passed')
