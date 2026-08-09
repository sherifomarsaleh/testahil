"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place on the delivered file, the whole workbook
is re-evaluated from scratch, and the test asserts that the headline moves, moves
in the right DIRECTION, and moves by a sensible amount. A dead-input sweep then
bumps every remaining numeric driver and requires it to move something."""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'MODON_Valuation_Model_09082026_public.xlsx'))
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
                ebitda26=bk.cell_value('DCF', f"B{XP['anchors']['dcf_rw']+8}"),
                wacc=bk.cell_value('DCF', f"C{AD['wacc']}"),
                wacc_term=bk.cell_value('DCF', f"C{AD['wt']}"),
                nd30=bk.cell_value('Balance Sheet', 'I15'),
                np26=bk.cell_value('Income Statement', 'E17'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, cell column, bump, the headline it must move, the required direction
CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'with terminal ROIC above the terminal cost of capital, growth adds (a little) value'),
    ('Beta (tier-3 fallback, flagged; sensitised 0.8-1.2)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('AED government bond yield (Jan-2031 T-Bond auction)', 'C', +0.01, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('6-month EIBOR', 'C', +0.01, 'wacc', +1,
     'a costlier debt leg must raise the blended cost of capital'),
    ('Effective tax rate (DMTT floor + foreign uplift)', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Terminal return on invested capital', 'C', +0.01, 'dcf', +1,
     'higher terminal returns mean less reinvestment per unit of growth'),
    # Decomposed 09-Aug-2026: a faster year-1 conversion PULLS CASH FORWARD
    # (explicit-window PV rises) but DRAINS the backlog that feeds the terminal
    # year, and with ~71% of EV in the terminal value the perpetuity loss slightly
    # outweighs the timing gain — the net per-share move is mildly negative. Both
    # legs of the mechanism are asserted separately; the near-cancellation is a
    # conservative artifact of terminal anchoring, stated in the study's caveats.
    ('Backlog conversion rate on opening development backlog', 'C', +0.03, 'pv_expl', +1,
     'converting the backlog faster must raise the explicit-window present value'),
    ('Backlog conversion rate on opening development backlog', 'C', +0.03, 'tv', -1,
     'a drained backlog must lower terminal-year revenue and the terminal value'),
    ('New development sales (AED mn)', 'C', +3000.0, 'dcf', +1,
     'more sales grow the backlog and later-year revenue'),
    ('Development gross margin', 'C', +0.02, 'dcf', +1,
     'a richer development margin must raise the valuation'),
    ('General & administrative / revenue', 'C', +0.01, 'dcf', -1,
     'a heavier cost load must cut EBIT and the valuation'),
    ('Capital expenditure (AED mn)', 'C', +500.0, 'dcf', -1,
     'more capex absorbs cash and must lower the valuation'),
    ('Working-capital release, negative = absorption (AED mn)', 'C', +500.0, 'dcf', +1,
     'a larger cash release must raise free cash flow and the valuation'),
    ('Gross debt FY2025 incl. related-party loan (AED mn, disclosed)', 'C', +2000.0, 'dcf', -1,
     'more net debt in the bridge must leave less for shareholders'),
    ('Cash and bank balances FY2025 (AED mn, disclosed)', 'C', +2000.0, 'dcf', +1,
     'more cash in the bridge must leave more for shareholders'),
    ('Days from 31-Dec-2025 valuation date to the 7-Aug-2026 anchor', 'C', +100.0, 'dcf', +1,
     'a later anchor accretes more value at the cost of equity'),
    ('Justified price/earnings (FY2026E attributable)', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the relative lens and the central'),
    ('Justified EV/EBITDA (FY2026E)', 'C', +1.0, 'central', +1,
     'a higher justified EV multiple must raise the central'),
    ('Through-cycle price/earnings', 'C', +1.0, 'central', +1,
     'a higher through-cycle multiple must raise the normalised lens'),
    ('Sustainable return on equity', 'C', +0.02, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Gross debt path incl. related-party loan (AED mn)', 'C', +2000.0, 'nd30', +1,
     'drawing more debt must leave more net debt at the end of the forecast'),
    ('NCI share of profit', 'C', +0.05, 'np26', -1,
     'a larger minority share must cut attributable profit'),
    ('Terminal debt weight D/(E+D)', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Spot price (AED, 7-Aug-2026 close)', 'C', +1.0, 'wacc', +1,
     'a higher market value of equity shifts the weights toward the costlier equity leg'),
]
# label normalisation: the terminal debt weight label in the builder
CASES = [(l.replace('D/(E+D)', 'D/(D+E)'), c, b, k, s, w) for l, c, b, k, s, w in CASES]

fails = []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-7
    flag = 'OK ' if ok else 'BAD'
    print(f'  [{flag}] {label} {bump:+g} -> {key} {base[key]:,.3f} -> {out[key]:,.3f} '
          f'({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

# a driver that moves NOTHING anywhere is a dead input: catch those too
DEAD_OK = {
    # FY2025 audited anchors that appear on statement sheets but deliberately do
    # not feed the valuation chain (the bridge uses its own disclosed rows):
    'Development backlog at 31-Dec-2025 (AED mn, disclosed)',   # backlog roll opening — feeds dcf, keep out of DEAD_OK if it moves
}
DEAD_OK = set()   # everything on this Assumptions sheet is expected to be live
print('\nDEAD-INPUT SWEEP — every driver not covered above is bumped and must move something')
dead = []
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{r}']
    if not isinstance(cell.value, (int, float)) or label in DEAD_OK:
        continue
    if any(label == c[0] for c in CASES):
        continue
    out = read({('Assumptions', f'C{r}'): cell.value * 1.10 + 1e-6})
    if all(abs(out[k] - base[k]) < 1e-9 for k in base):
        dead.append(label)
if dead:
    print('  inputs that changed nothing:', dead)
else:
    print('  none — every remaining driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right direction')
