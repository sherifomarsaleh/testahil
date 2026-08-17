"""Prove the delivered workbook is a LIVE DRIVER model (revision 2).

Each driver is perturbed in place, the whole workbook re-evaluated, and the test
asserts the headline moves in the asserted direction. The dead-input sweep bumps
every remaining numeric driver and requires it to move something — EXCEPT the
'scenario:' rows, which are published driver vectors for the pasted engine
re-runs (reproducibility inputs, not live-chain inputs) and are asserted dead
BY DESIGN."""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'MODON_Valuation_Model_10082026_public.xlsx'))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
AD = XP['anchors']['dcf']
A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str):
        A[c.value] = c.row

def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]

def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(dcf=bk.cell_value('DCF', f"C{AD['ps']}"),
                central=bk.cell_value('Summary', 'C9'),
                pv_expl=bk.cell_value('DCF', f"C{AD['pex']}"),
                tv=bk.cell_value('DCF', f"C{AD['tv']}"),
                wacc=bk.cell_value('DCF', f"C{AD['wacc']}"),
                wacc_term=bk.cell_value('DCF', f"C{AD['wt']}"),
                nd30=bk.cell_value('Balance Sheet', 'J13'),
                np27=bk.cell_value('Income Statement', 'G17'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    # decomposed 09-Aug and RE-DECOMPOSED 10-Aug: at revision 2 the terminal ROIC (8.5%)
    # sat within 21bp of the derived terminal WACC (8.71%), so extra terminal growth was
    # value-NEUTRAL and the case asserted a bounded near-zero move. The revision-3 beta
    # lifts the terminal WACC to 11.92% while the terminal ROIC is unchanged at 8.5%, so
    # the terminal block now reinvests BELOW its cost of capital and the growth gradient
    # INVERTS: more growth destroys value. The sign flip is the model behaving correctly
    # under a changed premise, not a regression — the expectation was re-derived first,
    # exactly as the standing rule requires, and the study's own figure caption was
    # corrected in the same pass.
    ('Terminal growth', 'C', +0.005, 'dcf', -1,
     'terminal ROIC 8.5% now sits BELOW the terminal WACC 11.92%, so growth reinvested '
     'at a sub-WACC return must SUBTRACT value'),
    ('Beta (own-stock regression vs the published FTSE ADX General index)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('AED government bond yield (Jan-2031 T-Bond auction)', 'C', +0.01, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('6-month EIBOR (31-Mar-2026 fixing, dated)', 'C', +0.01, 'wacc', +1,
     'a costlier debt leg must raise the blended cost of capital'),
    ('Effective tax rate (DMTT floor + foreign uplift)', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Terminal return on invested capital', 'C', +0.01, 'dcf', +1,
     'higher terminal returns mean less reinvestment per unit of growth'),
    ('New development sales (AED mn)', 'D', +3000.0, 'dcf', +1,
     'more FY2027 sales grow the backlog and later-year revenue'),
    ('Development gross margin', 'D', +0.02, 'dcf', +1,
     'a richer development margin must raise the valuation'),
    ('General & administrative / revenue', 'D', +0.01, 'dcf', -1,
     'a heavier cost load must cut EBIT and the valuation'),
    ('Capital expenditure (AED mn)', 'D', +500.0, 'dcf', -1,
     'more capex absorbs cash and must lower the valuation'),
    ('Receivable days (incl. related-party) on revenue', 'D', +30.0, 'dcf', -1,
     'slower collections absorb working capital and must lower the valuation'),
    ('Payables + advances cover of annual direct costs (×)', 'D', +0.10, 'dcf', +1,
     'more customer-advance funding releases working capital and must raise the valuation'),
    ('Land-bank/WIP share of development cost of sales', 'C', +0.05, 'dcf', +1,
     'drawing more cost of sales from the existing land bank releases inventory'),
    ('New WIP added per AED of new development sales', 'C', +0.05, 'dcf', -1,
     'more mobilisation spend per sale absorbs working capital'),
    ('Unrestricted (available) cash at 30-Jun-2026 (disclosed)', 'C', +2000.0, 'dcf', +1,
     'more available cash in the bridge must leave more for shareholders'),
    ('Gross debt incl. related-party loan at 30-Jun-2026 (disclosed)', 'C', +2000.0, 'dcf', -1,
     'more debt in the bridge must leave less for shareholders'),
    ('Development backlog at 30-Jun-2026 (65.4bn × 95%, disclosed)', 'C', +5000.0, 'dcf', +1,
     'a larger contracted backlog must raise development revenue and the valuation'),
    ('Days from the 30-Jun-2026 valuation date to the 7-Aug anchor', 'C', +100.0, 'dcf', +1,
     'a later anchor accretes more value at the cost of equity'),
    ('Justified price/earnings (FY2026E attributable)', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the relative lens and the central'),
    ('Through-cycle price/earnings', 'C', +1.0, 'central', +1,
     'a higher through-cycle multiple must raise the normalised lens'),
    ('Sustainable return on equity', 'C', +0.02, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Gross debt path incl. related-party loan (AED mn)', 'G', +2000.0, 'nd30', +1,
     'drawing more debt must leave more net debt at the end of the forecast'),
    ('NCI share of profit', 'C', +0.05, 'np27', -1,
     'a larger minority share must cut attributable profit'),
    ('Spot price (AED, 7-Aug-2026 close)', 'C', +1.0, 'wacc', +1,
     'a higher market equity value shifts the weights toward the costlier equity leg'),
    ('H1-2026 revenue (actual)', 'C', +1000.0, 'dcf', +1,
     'decomposed: extra revenue raises stub receivables (+DSO/365 per dirham) but its '
     'direct costs draw MORE advance funding (cover 1.86x) — net working-capital release'),
]

fails = []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    if sign == 0:
        ok = abs(rel) < 0.01 and abs(delta) > 1e-9   # asserted near-neutral, but live
    else:
        ok = (delta * sign > 0) and abs(rel) > 1e-7
    flag = 'OK ' if ok else 'BAD'
    print(f'  [{flag}] {label} ({col}) {bump:+g} -> {key} {base[key]:,.3f} -> {out[key]:,.3f} '
          f'({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

EXPECT = XP['expected']
def probe_all(overrides):
    bk = xlcalc.Book(wb, overrides)
    return {(sh, coord): bk.cell_value(sh, coord)
            for sh, cells in EXPECT.items() for coord in cells}
base_all = probe_all(None)

print('\nDEAD-INPUT SWEEP (probe = every formula cell in the workbook)')
dead, scenario_dead = [], []
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{r}']
    if not isinstance(cell.value, (int, float)):
        continue
    if any(label == c[0] for c in CASES):
        continue
    out_all = probe_all({('Assumptions', f'C{r}'): cell.value * 1.10 + 1e-6})
    moved = any(abs(out_all[k] - base_all[k]) > 1e-9 for k in base_all
                if isinstance(out_all[k], (int, float)) and isinstance(base_all[k], (int, float)))
    if not moved:
        # vector rows carry their live years in D..G (the stub column may be a
        # placeholder zero) — bump the first numeric later column before judging
        for colx in ('D', 'E', 'F', 'G'):
            cx = wb['Assumptions'][f'{colx}{r}']
            if isinstance(cx.value, (int, float)):
                out_all = probe_all({('Assumptions', f'{colx}{r}'): cx.value * 1.10 + 1e-6})
                moved = any(abs(out_all[k] - base_all[k]) > 1e-9 for k in base_all
                            if isinstance(out_all[k], (int, float))
                            and isinstance(base_all[k], (int, float)))
                if moved:
                    break
    if label.startswith('scenario:'):
        if moved:
            fails.append((label, 'scenario-vector', 0,
                          'published scenario vectors must NOT feed the live chain'))
            print(f'  [BAD] {label}: moved the live model — must be display-only')
        else:
            scenario_dead.append(label)
    elif not moved:
        dead.append(label)
if dead:
    print('  live inputs that changed nothing:', dead)
else:
    print(f'  every live driver reprices the model; {len(scenario_dead)} scenario '
          f'vectors correctly dead-by-design')

assert not fails, f'{len(fails)} failures: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers reprice the workbook in the asserted '
      f'direction; zero dead live inputs')
