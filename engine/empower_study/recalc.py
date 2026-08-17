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
     independent cross-check on the expected map itself — including the live scenario
     blocks (recovery ladder, bear, bull, constructions) and both centrals to 3 decimals.
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
CRUX, CEN = D['crux'], D['central']

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
BRG, SN = ANCH['bridge'], ANCH['sens']
checks = [
    ('DCF enterprise value (9%)', g('DCF', f"C{DR['ev']}"), B_CT['ev'], 1.0),
    ('DCF present value of explicit years (9%)', g('DCF', f"C{DR['pvex']}"),
     B_CT['pv_explicit'], 1.0),
    ('DCF present value of terminal value (9%)', g('DCF', f"C{DR['pvtv']}"),
     B_CT['pv_tv'], 1.0),
    ('DCF two-stage terminal value (9%)', g('DCF', f"C{DR['tv']}"), B_CT['tv'], 1.0),
    ('DCF terminal value share (9%)', g('DCF', f"C{DR['tvsh']}"), B_CT['tv_share'], 0.002),
    ('DCF terminal return on invested capital', g('DCF', f"C{DR['roic']}"),
     B_CT['roic_term'], 0.001),
    ('DCF fair value per share (9%)', g('DCF', f"C{DR['ps']}"), B_CT['ps'], 0.005),
    ('DCF enterprise value (15%)', g('DCF', f"C{DR['ev_dm']}"), B_DM['ev'], 1.0),
    ('DCF enterprise value (CDS)', g('DCF', f"C{DR['ev_cds']}"), B_CDS['ev'], 1.0),
    ('WACC 9% rating', g('DCF', f"C{DR['wacc_ct']}"), W['rating_ct'], 0.0002),
    ('WACC 9% CDS', g('DCF', f"D{DR['wacc_ct']}"), W['cds_ct'], 0.0002),
    ('WACC 15% rating (same rate — 9% shield)', g('DCF', f"C{DR['wacc_dm']}"),
     W['rating_dmtt'], 0.0002),
    ('WACC 15% CDS', g('DCF', f"D{DR['wacc_dm']}"), W['cds_dmtt'], 0.0002),
    ('WACC construction — gross-debt weights', g('DCF', f"B{DR['con0']+1}"),
     W['constructions']['gross'], 0.0002),
    ('WACC construction — negative carry', g('DCF', f"B{DR['con0']+2}"),
     W['constructions']['carry'], 0.0002),
    ('WACC construction — DFM beta', g('DCF', f"B{DR['con0']+3}"),
     W['constructions']['dfm_beta'], 0.0002),
    ('Cost of equity rating', g('DCF', f"C{DR['ke']}"), W['ke_rating'], 0.0002),
    ('Cost of equity CDS', g('DCF', f"D{DR['ke']}"), W['ke_cds'], 0.0002),
    ('Net debt', g('DCF', f"C{DR['nd']}"), W['net_debt'], 0.5),
    ('Market capitalisation', g('DCF', f"C{DR['mktcap']}"), W['mktcap'], 0.5),
    ('Bridge fair value per share (9%)', g('SOTP Bridge', f"C{BRG['ps']}"), B_CT['ps'],
     0.005),
    ('Bridge fair value per share (15%)', g('SOTP Bridge', f"D{BRG['ps']}"), B_DM['ps'],
     0.005),
    ('Bridge fair value per share (CDS)', g('SOTP Bridge', f"E{BRG['ps']}"), B_CDS['ps'],
     0.005),
    ('Bridge NCI share of profit', g('SOTP Bridge', f"C{BRG['nci']}"),
     D['inputs']['nci_pat_fy25']['value'] / D['inputs']['pat_fy25']['value'], 0.0005),
    ('Relative lens per share', g('Relative & Normalized', f"C{RN['ps_rel']}"),
     D['rel']['ps_rel'], 0.005),
    ('Relative lens trailing operating EBITDA', g('Relative & Normalized', 'C5'),
     D['rel']['ebitda_trail'], 0.5),
    ('Peer P/E lens per share', g('Relative & Normalized', f"C{RN['ps_pe']}"),
     D['rel']['ps_pe'], 0.005),
    ('Normalised lens per share', g('Relative & Normalized', f"C{RN['ps_norm']}"),
     D['norm']['ps'], 0.005),
    ('Normalised lens per share, 15%', g('Relative & Normalized', f"C{RN['ps_norm15']}"),
     D['norm']['ps_15'], 0.005),
    ('Book lens per share', g('Relative & Normalized', f"C{RN['ps_book']}"),
     D['book']['ps'], 0.005),
    ('Book lens per share, 15%', g('Relative & Normalized', f"C{RN['ps_book15']}"),
     D['book']['ps_15'], 0.005),
    ('Dividend cross-check per share', g('Relative & Normalized', f"C{RN['ddm']}"),
     D['ddm']['ps'], 0.005),
    ('Sustainable return on equity', g('Relative & Normalized', f"C{RN['roe']}"),
     D['book']['roe_sust'], 0.001),
    ('Justified forward price/earnings', g('Relative & Normalized', f"C{RN['pe_just']}"),
     D['norm']['pe_just'], 0.01),
    ('Summary central — recovery 9% (3dp)', g('Summary', f"B{SU['central']}"),
     CEN['ct'], 0.0005),
    ('Summary central — continuation 9% (3dp)', g('Summary', f"B{SU['central_cont']}"),
     CEN['continuation_ct'], 0.0005),
    ('Summary central — recovery 15% (3dp)', g('Summary', f"B{SU['central_dm']}"),
     CEN['dmtt'], 0.0005),
    ('Summary central — continuation 15% (3dp)',
     g('Summary', f"B{SU['central_cont_dm']}"), CEN['continuation_dmtt'], 0.0005),
    ('Segments FY2025 revenue rebuild', g('Segments', 'B12'), HI['FY25']['rev'], 0.01),
    ('Segments FY2025 operating EBITDA + interest + rental = audited',
     g('Segments', 'B24'), HI['FY25']['ebitda'], 1.0),
    ('Segments realised tariff vs RD10 cap headroom', g('Segments', 'C28'),
     D['unit_physical']['rate_aed_per_rth'] / 0.643 - 1, 0.001),
    ('Segments implied FY2025 full-load hours', g('Segments', 'C30'),
     D['unit_physical']['eflh_fy25_hrs'], 1.0),
    ('Segments FY2026E revenue', g('Segments', 'C12'), F['rev']['FY26'], 0.5),
    ('Segments FY2030E revenue', g('Segments', 'G12'), F['rev']['FY30'], 0.5),
    ('Segments FY2026E operating EBITDA', g('Segments', 'C22'), F['ebitda']['FY26'], 0.5),
    ('Income statement FY2025 operating EBITDA', g('Income Statement', 'D9'),
     D['rel']['ebitda_trail'] - D['inputs']['rental_fy25']['value'], 0.01),
    ('Income statement FY2026E attributable profit', g('Income Statement', 'E18'),
     D['rel']['npa26'], 0.5),
    ('Balance sheet FY2030E plant', g('Balance Sheet', 'I5'), F['ppe']['FY30'], 0.5),
    ('Balance sheet 30-Jun-2026 net debt', g('Balance Sheet', 'D16'), W['net_debt'], 0.5),
    ('Cash flow FY2026E free cash flow', g('Cash Flow', 'D11'), B_CT['fcff']['FY26'], 0.5),
    ('Live recovery ladder at 100% equals the base DCF',
     g('Sensitivity', f"E{SN['crux_ps']}"), B_CT['ps'], 0.005),
    ('Live continuation (94%) per share', g('Sensitivity', f"C{SN['crux_ps']}"),
     CRUX['persist_ps_ct'], 0.005),
    ('Live continuation at 15% per share', g('Sensitivity', f"C{SN['crux_ps15']}"),
     CRUX['persist_ps_dmtt'], 0.005),
    ('Live bear per share', g('Sensitivity', f"C{SN['bear_ps']}"), CEN['bear'], 0.005),
    ('Live bull per share', g('Sensitivity', f"C{SN['bull_ps']}"), CEN['bull'], 0.005),
    ('Live construction per share — gross', g('Sensitivity', f"B{SN['con_ps']}"),
     DC['base_gross_wacc']['ps'], 0.005),
    ('Live construction per share — carry', g('Sensitivity', f"C{SN['con_ps']}"),
     DC['base_carry_wacc']['ps'], 0.005),
    ('Live construction per share — DFM beta', g('Sensitivity', f"D{SN['con_ps']}"),
     DC['base_dfm_beta']['ps'], 0.005),
]
for j, lvl in enumerate(CRUX['levels']):
    col = ['B', 'C', 'D', 'E', 'F'][j]
    checks.append((f'Live recovery ladder at {lvl:.0%}',
                   g('Sensitivity', f"{col}{SN['crux_ps']}"), CRUX['rows'][j]['ps'],
                   0.005))
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and isinstance(got, (int, float)) and \
        abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    gs = f'{got:,.4f}' if isinstance(got, (int, float)) else repr(got)
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={gs} model={float(want):,.4f}")

# the live one-way growth row must reproduce the pasted grid's middle row
live_bad = 0
for j, colL in enumerate(['B', 'C', 'D', 'E', 'F']):
    got = cell_value('Sensitivity', f"{colL}{SN['live']}")
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
      f'0 unchecked; {len(checks)} headline reconciliations passed (both centrals to 3dp)')
