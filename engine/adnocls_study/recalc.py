"""Recalculate the DELIVERED xlsx and reconcile it cell-by-cell against the model.

Recalculation is done by the explicit evaluator in xlcalc.py over the formula set the
builder actually emits, independently of the library that wrote the file. Anything the
evaluator does not understand is reported as a FAILURE rather than skipped.

Three gates run here, in increasing strength:

  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for that cell —
     the builder records them in xlsx_expected.json as it writes. This is the gate that
     makes a formula-driven workbook safe: a formula that computes the right thing the
     wrong way, or points one row off, fails here rather than silently shipping a different
     number from the study;
  3. a hand-written set of headline reconciliations against study_numbers.json, kept as an
     independent cross-check on the expected map itself.

Every formula cell must also be COVERED by the expected map. An unchecked formula is a
failure, not a skip.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, DCFA, LN, WACC = D['dcf'], D['dcf_asset_beta'], D['lenses'], D['wacc']
HI, HB, FC, FIN, FBS = D['hist_is'], D['hist_bs'], D['fcst'], D['fin'], D['fcst_bs']
REL, NRM, BK, SOTP = D['rel'], D['norm'], D['book'], D['sotp']
SH = D['meta']['shares_mn']

BK_ = xlcalc.Book(wb)
cell_value = BK_.cell_value

SHEETS = ['READ FIRST', 'Summary', 'Fundamental Valuation', 'Assumptions', 'SOTP Bridge',
          'Segments', 'Relative & Normalized', 'DCF', 'Income Statement', 'Balance Sheet',
          'Cash Flow', 'Summary Financials', 'Monte Carlo', 'Sensitivity',
          'Per-Share & Ratios', 'Peer & Sector']
assert wb.sheetnames == SHEETS, f'sheet list/order wrong: {wb.sheetnames}'

# ---- gate 1: every formula must evaluate -------------------------------------
nform, errors = 0, []
for sh, coord in BK_.formula_cells():
    nform += 1
    try:
        cell_value(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
for e in errors[:20]:
    print('  UNRESOLVABLE', e)

# ---- gate 2: every formula cell must reproduce the model's own value ----------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        try:
            got = cell_value(sh, coord)
        except Exception as ex:
            drift.append((sh, coord, f'ERROR {ex}', want)); continue
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
for sh, coord, got, want in drift[:30]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'  DISAGREES {sh}!{coord}: workbook={g} model={want:,.6f}')

# every formula cell must be covered by the expected map — no unchecked formulas
uncovered = [f'{sh}!{coord}' for sh, coord in BK_.formula_cells()
             if coord not in EXPECT.get(sh, {})]
for u in uncovered[:20]:
    print('  UNCHECKED', u)

# ---- gate 3: headline reconciliations against study_numbers.json --------------
def g(sheet, cell):
    return cell_value(sheet, cell)


checks = [
    ('DCF present value of the explicit years', g('DCF', 'C45'), DCF['pv_explicit'], 1.0),
    ('DCF present value of the terminal value', g('DCF', 'C46'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share of enterprise value', g('DCF', 'C48'), DCF['tv_share'],
     0.0005),
    ('DCF enterprise value', g('DCF', 'C50'), DCF['ev'], 1.0),
    ('DCF equity attributable to ordinary shareholders', g('DCF', 'C55'), DCF['equity'],
     1.0),
    ('DCF fair value per share (AED)', g('DCF', 'C57'), DCF['fv_aed'], 0.005),
    ('DCF terminal return on invested capital', g('DCF', 'C41'), DCF['roic_terminal'],
     0.0005),
    ('DCF required reinvestment rate', g('DCF', 'C42'), DCF['reinvest'], 0.0005),
    ('Cost of equity', g('DCF', 'C65'), WACC['ke'], 0.00005),
    ('Cost of debt — method 1', g('DCF', 'C70'), WACC['kd_method1'], 0.00005),
    ('Cost of debt — method 2', g('DCF', 'C86'), WACC['kd_method2'], 0.00005),
    ('Cost of debt — method 3', g('DCF', 'C87'), WACC['kd_method3'], 0.00005),
    ('Cost of debt — the three averaged', g('DCF', 'C88'), WACC['kd'], 0.00005),
    ('Equity weight', g('DCF', 'C95'), WACC['we'], 0.00005),
    ('Cost of capital — explicit window', g('DCF', 'C97'), WACC['wacc'], 0.00005),
    ('Cost of capital — terminal', g('DCF', 'C102'), WACC['wacc_term'], 0.00005),
    ('Cost of equity on the asset-risk beta', g('DCF', 'C106'), WACC['ke_beta1'], 0.00005),
    ('DCF fair value per share — asset-risk beta (AED)', g('DCF', 'C121'), DCFA['fv_aed'],
     0.005),
    ('DCF terminal value share — asset-risk beta', g('DCF', 'C118'), DCFA['tv_share'],
     0.0005),
    ('Bridge equity attributable', g('SOTP Bridge', 'C15'), DCF['equity'], 1.0),
    ('Bridge terminal value share', g('SOTP Bridge', 'C8'), DCF['tv_share'], 0.0005),
    ('Bridge fair value per share (AED)', g('SOTP Bridge', 'C17'), DCF['fv_aed'], 0.005),
    ('Sum-of-the-parts enterprise value of the legs', g('SOTP Bridge', 'D23'),
     SOTP['ev_ops'], 1.0),
    ('Sum-of-the-parts equity', g('SOTP Bridge', 'C39'), SOTP['equity'], 1.0),
    ('Sum-of-the-parts fair value per share (AED)', g('SOTP Bridge', 'C40'),
     SOTP['fv_aed'], 0.005),
    ('Shipping multiple, built on the sheet', g('SOTP Bridge', 'C29'),
     REL['blend_ev_ebitda'], 0.0005),
    ('Segments FY2026E Tankers EBITDA', g('Segments', 'B51'),
     D['fcst_seg']['Tankers']['ebitda'][0], 1.0),
    ('Segments FY2026E Tankers revenue', g('Segments', 'B53'),
     D['fcst_seg']['Tankers']['rev'][0], 1.0),
    ('Segments FY2026E Gas Carriers EBITDA', g('Segments', 'B60'),
     D['fcst_seg']['Gas Carriers']['ebitda'][0], 1.0),
    ('Segments FY2026E total revenue', g('Segments', 'B82'), FC['revenue'][0], 1.0),
    ('Segments FY2030E total EBITDA', g('Segments', 'F92'), FC['ebitda'][4], 1.0),
    ('Relative lens value per share', g('Relative & Normalized', 'C19'),
     LN['relative']['base'], 0.005),
    ('Normalised lens value per share', g('Relative & Normalized', 'C41'),
     LN['normalized']['base'], 0.005),
    ('Book lens value per share', g('Relative & Normalized', 'C52'), LN['book']['base'],
     0.005),
    ('Sustainable return on equity', g('Relative & Normalized', 'C48'),
     BK['roe_sustainable'], 0.0005),
    ('Justified price / book', g('Relative & Normalized', 'C51'), BK['pb_fair'], 0.005),
    ('Realised vessel price over carrying value', g('Relative & Normalized', 'C58'),
     BK['vessel_value_to_book'], 0.005),
    ('Own enterprise value / trailing EBITDA', g('Relative & Normalized', 'C27'),
     REL['own_ev_ebitda_ttm'], 0.005),
    ('Own price / 2025 ordinary earnings', g('Relative & Normalized', 'C29'),
     REL['own_pe_ttm'], 0.005),
    ('Summary weighted central', g('Summary', ANCH['summary_central']), D['central'],
     0.005),
    ('Summary weighted central — asset-risk beta',
     g('Summary', ANCH['summary_central_asset']), D['central_asset_beta'], 0.005),
    ('Summary expert panel average', g('Summary', 'C15'), D['panel_centre'], 0.005),
    ('Income statement FY2025 EBITDA (operating)', g('Income Statement', 'D14'),
     HI['ebitda_op'][2], 1.0),
    ('Income statement FY2025 EBITDA as reported', g('Income Statement', 'D16'),
     HI['ebitda_reported'][2], 1.0),
    ('Income statement FY2025 profit before tax', g('Income Statement', 'D24'),
     HI['pbt'][2], 1.0),
    ('Income statement FY2030E attributable profit', g('Income Statement', 'I28'),
     FIN['npa'][4], 1.0),
    ('Balance sheet FY2025 net working capital', g('Balance Sheet', 'D16'), HB['nwc'][2],
     1.0),
    ('Balance sheet FY2030E net debt', g('Balance Sheet', 'I18'), FIN['net_debt'][4], 1.0),
    ('Balance sheet FY2030E equity attributable', g('Balance Sheet', 'I21'),
     FBS[4]['equity_parent'], 1.0),
    ('Balance sheet FY2030E invested capital', g('Balance Sheet', 'I26'),
     FBS[4]['invested_capital'], 1.0),
    ('Balance sheet FY2026E return on equity', g('Balance Sheet', 'E28'), FBS[0]['roe'],
     0.0005),
    ('Cash flow FY2026E free cash flow to the firm', g('Cash Flow', 'E15'), FC['fcff'][0],
     1.0),
    ('Summary financials FY2030E revenue', g('Summary Financials', 'I5'), FC['revenue'][4],
     1.0),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
        print(f'  [BAD] {name}: workbook={got:,.4f} model={float(want):,.4f}')

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'{nchk} of {nform} formula cells reproduce the model, 0 unresolvable, 0 unchecked')
print(f'RECALC OK — {len(checks)} headline reconciliations against study_numbers.json '
      f'passed')
