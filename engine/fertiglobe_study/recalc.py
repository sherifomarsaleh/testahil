"""Recalculate the delivered xlsx and reconcile it cell-by-cell against study_numbers.json.

Verification runs on the DELIVERED FILE, not on the builder. The workbook is re-evaluated by
the explicit evaluator in xlcalc.py — an independent reimplementation of the arithmetic, so
the check is not the writing library confirming its own output. Anything the evaluator cannot
parse is reported as a FAILURE, never skipped.

Three gates, in increasing strength:

  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for it — the
     builder records them into xlsx_expected.json as it writes. This is the gate that makes a
     formula-driven workbook safe: a formula that computes the right thing the wrong way, or
     points one row off, fails here rather than silently shipping a number the study does not
     carry. The converse is checked too — no formula cell may be left unchecked;
  3. headline reconciliations against study_numbers.json, an independent cross-check on the
     expected map itself.
"""
import json
import os

import openpyxl

import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'Fertiglobe_Valuation_Model_09-08-2026.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']

DA, DB = D['dcf_A'], D['dcf_B']
BA, BB, BAK = D['bridge_A'], D['bridge_B'], D['bridge_A_book']
W, LN, FA = D['wacc'], D['lenses'], D['frame_A']
HI = D['hist_is']

BK = xlcalc.Book(wb)
g = BK.cell_value

# ---- gate 1: every formula must evaluate ------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        g(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)


# ---- gate 2: every formula cell must reproduce the model's own value --------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = g(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:25]:
    shown = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={shown} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3: headline reconciliations against study_numbers.json ------------
BR = 'SOTP Bridge'
FV = 'Fundamental Valuation'
RN = 'Relative & Normalized'
checks = [
    ('DCF enterprise value — framing A', g('DCF', ANCH['dcf_ev_a']), DA['ev'], 1.0),
    ('DCF enterprise value — framing B', g('DCF', ANCH['dcf_ev_b']), DB['ev'], 1.0),
    ('DCF present value of the explicit years — A', g('DCF', 'C57'), DA['pv_explicit'], 1.0),
    ('DCF present value of the terminal value — A', g('DCF', 'C58'), DA['pv_tv'], 1.0),
    ('DCF terminal value share — A', g('DCF', ANCH['dcf_tvs_a']), DA['tv_share'], 0.002),
    ('DCF cost of capital, explicit window', g('DCF', ANCH['dcf_wacc']),
     W['wacc_rating'], 0.0002),
    ('DCF cost of capital, terminal', g('DCF', ANCH['dcf_wacc_term']),
     W['wacc_term_rating'], 0.0002),
    ('DCF forecast tax rate', g('DCF', ANCH['dcf_tax']), D['tax_rate'], 0.0005),
    ('DCF terminal return on capital — A (in-sheet average of three bases)',
     g('DCF', 'C51'), DA['roic_term'], 0.001),
    ('DCF terminal reinvestment rate — A', g('DCF', 'C53'), DA['rr_term'], 0.001),
    ('DCF terminal value — A', g('DCF', 'C56'), DA['tv'], 1.0),
    ('Bridge enterprise value — A', g(BR, 'B7'), BA['ev'], 1.0),
    ('Bridge equity attributable — A', g(BR, 'B11'), BA['eq_attr'], 1.0),
    ('Bridge value per share (AED) — A', g(BR, ANCH['bridge_psa_a']), BA['ps_aed'], 0.02),
    ('Bridge value per share (AED) — B', g(BR, ANCH['bridge_psa_b']), BB['ps_aed'], 0.02),
    ('Bridge terminal value share — A', g(BR, ANCH['bridge_tvs_a']), BA['tv_share'], 0.002),
    ('Bridge value per share, minorities at book — A',
     g(BR, ANCH['bridge_psb_a']), BAK['ps_aed'], 0.02),
    ('Cash-flow lens — the average of the two framings',
     g(BR, ANCH['bridge_dcf_ps']), D['dcf_ps_aed'], 0.02),
    ('Fundamental — cash-flow lens', g(FV, 'B5'), LN['dcf']['value'], 0.02),
    ('Fundamental — relative lens', g(FV, 'B6'), LN['relative']['value'], 0.02),
    ('Fundamental — normalised lens', g(FV, 'B7'), LN['normalized']['value'], 0.02),
    ('Fundamental — book lens', g(FV, 'B8'), LN['book']['value'], 0.02),
    ('Fundamental — weighted central', g(FV, ANCH['fv_central']), D['central'], 0.02),
    ('Fundamental — lowest of the lenses and framings', g(FV, 'B10'), D['span'][0], 0.02),
    ('Fundamental — highest of the lenses and framings', g(FV, 'B11'), D['span'][1], 0.02),
    # The panel's three methods are worked in AED per share; the cash-flow method must be the
    # bridge's own framing-A answer, and the panel centre must be their live median.
    ('Panel — the cash-flow method equals the bridge', g(FV, 'D24'), BA['ps_aed'], 0.005),
    ('Panel — median of the three methods', g(FV, ANCH['panel_median']),
     sorted(g(FV, f'D{r}') for r in (23, 24, 25))[1], 0.005),
    ('Summary weighted central', g('Summary', ANCH['summary_central']), D['central'], 0.02),
    ('Summary lens weights sum to one', g('Summary', 'C9'), 1.0, 0.0005),
    ('Summary market price (AED)', g('Summary', ANCH['summary_spot']), D['spot'], 0.005),
    ('Relative lens implied value', g(RN, ANCH['rel_ps']), D['rel']['ps_aed'], 0.02),
    ('Normalised lens implied value', g(RN, ANCH['norm_ps']), D['norm']['ps_aed'], 0.02),
    ('Book lens implied value', g(RN, ANCH['book_ps']), D['book']['ps_aed'], 0.02),
    ('Income statement FY2025 revenue (audited)',
     g('Income Statement', ANCH['is_rev']), HI['FY25']['rev'], 0.5),
    ('Balance sheet FY2030E equity attributable',
     g('Balance Sheet', ANCH['bs_eq30']), FA['equity'][4], 1.0),
    ('Balance sheet FY2030E net debt',
     g('Balance Sheet', ANCH['bs_nd30']), FA['net_debt'][4], 1.0),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    bad += 0 if ok else 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={float(got):,.4f} "
          f"model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'\nRECALC OK — {nform} of {nform} formula cells reproduce the model, 0 unresolvable, '
      f'0 unchecked; {len(checks)} headline reconciliations passed')
