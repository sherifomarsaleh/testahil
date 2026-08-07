"""Gate (s) — every label must describe its own row.

Gates (q) and (r) are both value-oriented: (q) checks that each formula reproduces the
model, (r) that each driver propagates. Neither looks at column A, so a workbook can pass
both with ten consecutive rows labelled one row above their contents — which is exactly
what revision 3 shipped, and what three reviewers found before I did.

The test: for each labelled row, the value in that row must agree with what the label
says it is, computed independently from study_numbers.json.
"""
import json, sys, openpyxl, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
D = json.load(open('study_numbers.json'))
H, F, DCF, UC = D['history'], D['forecast'], D['dcf'], D['unit_calibration']
IN = {k: v['value'] for k, v in D['inputs'].items()}
wb = openpyxl.load_workbook('ARCC_Valuation_Model_06082026_public.xlsx')
XP = json.load(open('xlsx_expected.json'))


def val(sheet, addr):
    return XP.get(sheet, {}).get(addr)


CASES = [
    # sheet, label cell, value cell, what the label promises, the independent figure
    ('Income Statement', 'A5',  'D5',  'Revenue',            H['revenue'][2]),
    ('Income Statement', 'A11', 'D11', 'OPERATING PROFIT',   H['ebit'][2]),
    ('Income Statement', 'A13', 'D13', 'D&A',                H['dna'][2]),
    ('Income Statement', 'A14', 'D14', 'EBITDA',             H['ebitda'][2]),
    ('Income Statement', 'A15', 'D15', 'EBITDA margin',      H['margin'][2]),
    ('Income Statement', 'A20', 'D20', 'Attributable profit', H['pat'][2]),
    ('Income Statement', 'A21', 'D21', 'Earnings per share', H['eps'][2]),
    ('Balance Sheet',    'A9',  'D9',  'Cash and bank balances', IN['cash_fy25']),
    ('Balance Sheet',    'A10', 'D10', 'Inventories, receivables and debtors',
     IN['inv_fy25'] + IN['recv_fy25'] + IN['debtors_fy25']),
    ('Balance Sheet',    'A11', 'D11', 'TOTAL ASSETS',       IN['ta_fy25']),
    ('DCF',              'A33', 'B33', 'Enterprise value',   DCF['ev']),
    ('DCF',              'A42', 'B42', 'Equity value',       DCF['equity']),
    ('DCF',              'A43', 'B43', 'Shares outstanding', D['meta']['shares_mn']),
    ('DCF',              'A44', 'B44', 'FAIR VALUE PER SHARE', DCF['fv']),
    ('Unit Build',       'A18', 'B18', 'TOTAL DESPATCHES',   UC['vol_fy25']),
    ('Unit Build',       'A22', 'B22', 'LOCAL CEMENT PRICE', UC['price_loc_derived']),
    ('Unit Build',       'A12', 'B12', 'Cement produced',    UC['cem_prod']),
    ('Unit Build',       'A7',  'B7',  'Clinker produced',   UC['clk_prod']),
]
fails, checked = [], 0
print('LABEL GATE — does each label describe its own row?\n')
for sh, lab_ad, val_ad, promise, truth in CASES:
    ws = wb[sh]
    label = str(ws[lab_ad].value or '')
    got = val(sh, val_ad)
    checked += 1
    ok = got is not None and abs(got - truth) <= max(1e-6, abs(truth) * 1e-6)
    tag = 'OK ' if ok else 'FAIL'
    if not ok:
        fails.append((sh, lab_ad, label, promise, got, truth))
    print(f"  [{tag}] {sh:18s} {lab_ad:4s} '{label[:42]:44s}' -> {val_ad}: "
          f"{got if got is not None else 'MISSING'} vs {truth:,.4f}")
print()
if fails:
    for f in fails:
        print('  MISLABELLED:', f)
    sys.exit(f'LABEL GATE FAILED — {len(fails)} of {checked} labels do not describe their row')
print(f'LABEL GATE OK — {checked} labels checked, every one describes its own row')
