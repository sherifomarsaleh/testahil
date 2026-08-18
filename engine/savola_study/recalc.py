"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for
     that cell (xlsx_expected.json, written by the builder);
  3. a hand-written set of headline reconciliations against study_numbers.json,
     kept as an independent cross-check on the expected map itself.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'du_study'))
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'SAVOLA_Valuation_Model_18082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, LN, HI, F, W = D['dcf'], D['lenses'], D['hist_is'], D['fcst'], D['wacc']
SH = D['meta']['shares_wavg_mn']

BK = xlcalc.Book(wb)
cell_value = BK.cell_value

# ---- gate 1: every formula must evaluate -------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cell_value(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)

# ---- gate 2: every formula cell must reproduce the model's own value ----------
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
for sh, coord, got, want in drift[:30]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:40]:
    print('  ', u)

# ---- gate 3: headline reconciliations against study_numbers.json --------------
def g(sheet, cell):
    return cell_value(sheet, cell)

checks = [
    ('DCF enterprise value', g('DCF', ANCH['dcf_ev'].split('!')[1]), DCF['ev'], 1.0),
    ('DCF fair value per share at the anchor', g('DCF', ANCH['dcf_ps'].split('!')[1]),
     DCF['ps'], 0.02),
    ('Bridge equity value', g('SOTP Bridge', ANCH['bridge_eq'].split('!')[1]),
     DCF['eq_val'], 1.0),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Summary Framing B', g('Summary', 'C11'), DCF['framingB'], 0.02),
    ('Relative lens', g('Relative & Normalized', ANCH['rel_row']),
     LN['relative']['base'], 0.02),
    ('Normalised lens', g('Relative & Normalized', ANCH['norm_row']),
     LN['normalized']['base'], 0.02),
    ('Book lens', g('Relative & Normalized', ANCH['book_row']), LN['book']['base'], 0.02),
    ('Panel median', g('Fundamental Valuation', ANCH['fv_panel']), D['panel_median'], 0.02),
    ('Framing gap', g('Fundamental Valuation', ANCH['fv_gap']), DCF['framing_gap'], 0.02),
    ('Income statement FY2025 EBITDA', g('Income Statement', ANCH['is_ebitda_d'].split('!')[1]),
     HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E attributable profit',
     g('Income Statement', ANCH['is_np_i'].split('!')[1]), F['np'][4], 1.0),
    ('Income statement FY2026E EPS', g('Income Statement', ANCH['is_eps_e'].split('!')[1]),
     F['eps'][0], 0.01),
    ('Segments group revenue FY2026E', g('Segments', ANCH['seg_grev_b'].split('!')[1]),
     F['rev'][0], 1.0),
    ('Segments group EBITDA FY2030E', g('Segments', ANCH['seg_geb_f'].split('!')[1]),
     F['ebitda'][4], 1.0),
    ('Balance sheet foot check FY2030E', g('Balance Sheet', ANCH['bs_foot_i'].split('!')[1]),
     0.0, 0.01),
    ('Balance sheet FY2030E cash', g('Balance Sheet', ANCH['bs_cash_i'].split('!')[1]),
     F['cash'][4], 1.0),
    ('Cash flow FY2026E closing cash', g('Cash Flow', ANCH['cf_cash_b'].split('!')[1]),
     F['cash'][0], 1.0),
    ('DCF FY2026E free cash flow', g('DCF', ANCH['dcf_fcff_b'].split('!')[1]),
     F['fcff'][0], 1.0),
    ('DCF cost of capital — explicit', g('DCF', ANCH['dcf_wacc'].split('!')[1]),
     W['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', ANCH['dcf_wacct'].split('!')[1]),
     W['wacc_term'], 0.0002),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={got:,.4f} model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'RECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements with the '
      f'model, {len(checks)} headline reconciliations passed')
