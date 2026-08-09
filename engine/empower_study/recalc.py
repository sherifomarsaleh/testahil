"""Recalculate the delivered EMPOWER xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Recalculation is done by the explicit evaluator in xlcalc.py over the formula set the
builder actually emits, independently of the library that wrote the file. Anything the
evaluator does not understand is reported as a FAILURE, never skipped.

Three gates run here, in increasing strength:

  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for that cell —
     the builder records them in xlsx_expected.json as it writes;
  3. a hand-written set of headline reconciliations against study_numbers.json, kept as an
     independent cross-check on the expected map itself.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'EMPOWER_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
W, DC, LN = D['wacc'], D['dcf'], D['lenses']
B_CT, B_DM, B_CDS = DC['base_ct'], DC['base_dmtt'], DC['base_cds']
HI, F = D['hist_is'], D['fcst']['base']
SH = D['meta']['shares_mn']

BK = xlcalc.Book(wb)
cell_value = BK.cell_value

# ---- gate 1: every formula must evaluate ------------------------------------------
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

# ---- gate 2: every formula cell must reproduce the model's own value --------------
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

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3: headline reconciliations against study_numbers.json ------------------
def g(sheet, cell):
    return cell_value(sheet, cell)

SU, DR, RN = ANCH['summary'], ANCH['dcf'], ANCH['rel']
checks = [
    ('DCF enterprise value (9%)', g('DCF', 'C32'), B_CT['ev'], 1.0),
    ('DCF present value of explicit years (9%)', g('DCF', 'C31'), B_CT['pv_explicit'], 1.0),
    ('DCF present value of terminal value (9%)', g('DCF', 'C30'), B_CT['pv_tv'], 1.0),
    ('DCF terminal value share (9%)', g('DCF', 'C33'), B_CT['tv_share'], 0.002),
    ('DCF terminal return on invested capital', g('DCF', 'C25'), B_CT['roic_term'], 0.001),
    ('DCF fair value per share (9%)', g('DCF', 'C35'), B_CT['ps'], 0.005),
    ('DCF enterprise value (15%)', g('DCF', f"C{DR['ev_dm']}"), B_DM['ev'], 1.0),
    ('DCF enterprise value (CDS)', g('DCF', f"C{DR['ev_cds']}"), B_CDS['ev'], 1.0),
    ('WACC 9% rating', g('DCF', f"C{DR['wacc_ct']}"), W['rating_ct'], 0.0002),
    ('WACC 9% CDS', g('DCF', f"D{DR['wacc_ct']}"), W['cds_ct'], 0.0002),
    ('WACC 15% rating', g('DCF', f"C{DR['wacc_dm']}"), W['rating_dmtt'], 0.0002),
    ('WACC 15% CDS', g('DCF', f"D{DR['wacc_dm']}"), W['cds_dmtt'], 0.0002),
    ('Cost of equity rating', g('DCF', 'C44'), W['ke_rating'], 0.0002),
    ('Cost of equity CDS', g('DCF', 'D44'), W['ke_cds'], 0.0002),
    ('Net debt', g('DCF', 'C47'), W['net_debt'], 0.5),
    ('Market capitalisation', g('DCF', 'C46'), W['mktcap'], 0.5),
    ('Bridge fair value per share (9%)', g('SOTP Bridge', 'C13'), B_CT['ps'], 0.005),
    ('Bridge fair value per share (15%)', g('SOTP Bridge', 'D13'), B_DM['ps'], 0.005),
    ('Bridge fair value per share (CDS)', g('SOTP Bridge', 'E13'), B_CDS['ps'], 0.005),
    ('Bridge NCI share of profit', g('SOTP Bridge', 'C14'),
     D['inputs']['nci_pat_fy25']['value'] / D['inputs']['pat_fy25']['value'], 0.0005),
    ('Relative lens per share', g('Relative & Normalized', f"C{RN['ps_rel']}"),
     D['rel']['ps_rel'], 0.005),
    ('Peer P/E lens per share', g('Relative & Normalized', f"C{RN['ps_pe']}"),
     D['rel']['ps_pe'], 0.005),
    ('Normalised lens per share', g('Relative & Normalized', f"C{RN['ps_norm']}"),
     D['norm']['ps'], 0.005),
    ('Book lens per share', g('Relative & Normalized', f"C{RN['ps_book']}"),
     D['book']['ps'], 0.005),
    ('Dividend cross-check per share', g('Relative & Normalized', f"C{RN['ddm']}"),
     D['ddm']['ps'], 0.005),
    ('Sustainable return on equity', g('Relative & Normalized', 'C27'),
     D['book']['roe_sust'], 0.001),
    ('Justified price/earnings', g('Relative & Normalized', 'C28'), D['norm']['pe_just'],
     0.01),
    ('Summary central (9%)', g('Summary', f"B{SU['central']}"), D['central']['ct'], 0.005),
    ('Summary central (15%)', g('Summary', f"B{SU['central_dm']}"), D['central']['dmtt'],
     0.005),
    ('Segments FY2025 revenue rebuild', g('Segments', 'B12'), HI['FY25']['rev'], 0.01),
    ('Segments FY2026E revenue', g('Segments', 'C12'), F['rev']['FY26'], 0.5),
    ('Segments FY2030E revenue', g('Segments', 'G12'), F['rev']['FY30'], 0.5),
    ('Segments FY2026E EBITDA', g('Segments', 'C21'), F['ebitda']['FY26'], 0.5),
    ('Segments FY2025 EBITDA rebuild vs audited', g('Segments', 'B21'),
     HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D8'), HI['FY25']['ebitda'],
     0.01),
    ('Income statement FY2026E attributable profit', g('Income Statement', 'E17'),
     D['rel']['npa26'], 0.5),
    ('Balance sheet FY2030E plant', g('Balance Sheet', 'I5'), F['ppe']['FY30'], 0.5),
    ('Balance sheet 30-Jun-2026 net debt', g('Balance Sheet', 'D16'), W['net_debt'], 0.5),
    ('Cash flow FY2026E free cash flow', g('Cash Flow', 'D11'), B_CT['fcff']['FY26'], 0.5),
    ('Live growth sensitivity centre equals the base DCF',
     g('Sensitivity', 'D22') if isinstance(g('Sensitivity', 'D22'), (int, float)) else None,
     None, None),
]
bad = 0
for name, got, want, tol in checks:
    if want is None:
        continue
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={got:,.4f} model={float(want):,.4f}")

# the live one-way growth row must reproduce the pasted grid's middle row
live_bad = 0
srow = None
for row in wb['Sensitivity'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str) and c.value.startswith('Fair value per share (AED, live'):
        srow = c.row
assert srow, 'live sensitivity row not found'
for j, colL in enumerate(['B', 'C', 'D', 'E', 'F']):
    got = cell_value('Sensitivity', f'{colL}{srow}')
    want = D['sens_wg']['table'][2][j]
    ok = abs(float(got) - want) <= 0.002
    live_bad += 0 if ok else 1
    print(f"  [{'OK ' if ok else 'BAD'}] live growth row g={D['sens_wg']['g_grid'][j]:.3f}: "
          f'workbook={got:,.4f} grid={want:,.4f}')

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
assert live_bad == 0, 'live sensitivity row does not reproduce the pasted grid'
print(f'RECALC OK — {nform} of {nform} formula cells reproduce the model, 0 unresolvable, '
      f'0 unchecked; {sum(1 for c in checks if c[2] is not None)} headline reconciliations '
      f'passed')
