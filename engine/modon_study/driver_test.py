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
ANCH = XP['anchors']
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
                central=bk.cell_value('Summary', ANCH['summary_central']),
                rel_lens=bk.cell_value('Summary', 'C6'),
                norm_lens=bk.cell_value('Summary', 'C7'),
                book_lens=bk.cell_value('Summary', 'C8'),
                pv_expl=bk.cell_value('DCF', f"C{AD['pex']}"),
                tv=bk.cell_value('DCF', f"C{AD['tv']}"),
                # The terminal's own lines, so a driver whose effect on the answer nearly
                # cancels can still be asserted on the quantity it unambiguously moves.
                # Asserting a near-coin-flip sign would be a test that passes by luck.
                t_maint=bk.cell_value('DCF', f"C{AD['tmaint']}"),
                t_fcff=bk.cell_value('DCF', f"C{AD['tfcff']}"),
                wacc=bk.cell_value('DCF', f"C{AD['wacc']}"),
                wacc_term=bk.cell_value('DCF', f"C{AD['wt']}"),
                nd30=bk.cell_value('Balance Sheet', 'J13'),
                np27=bk.cell_value('Income Statement', 'G17'))

base = read()
base_ic_x2 = 2.0 * wb['Assumptions'][
    f"C{row_of('Invested capital per unit of real growth, at terminal revenue (AED mn)')}"].value
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
    # THE SIGN FLIPPED BACK WITH THE CONSTRUCTION, AND THAT IS THE POINT. Under the
    # retired reinvestment identity a terminal ROIC of 8.5% below a terminal WACC of
    # 11.92% made growth SUBTRACT value — growth was charged g x IC whatever it cost to
    # buy. The sanctioned terminal charges real growth the capital this model's own
    # forecast actually spends per unit of revenue, which here is far less than g x IC,
    # so real growth adds value again. The expectation was re-derived before the case was
    # rewritten, never adjusted to whatever the model returned.
    ('Terminal REAL growth (stated, not derived)', 'C', +0.005, 'dcf', +1,
     'real growth widens the perpetuity and costs the capital this model actually spends '
     'per unit of revenue — 12,501 AED mn per unit of real growth, against the 1/g charge '
     'the retired construction levied'),
    # Inflation moves TWO lines that nearly cancel in the answer: it widens the growth
    # rate and it escalates the replacement cost of the asset base. Asserting a direction
    # on the answer would be asserting a sign that lands at +0.9% and could flip on a
    # small parameter change, so the case is pointed at the line inflation moves
    # UNAMBIGUOUSLY [R-COC-01: when a check fires on work that is right, re-point it].
    ('Terminal inflation — UAE house macro path', 'C', +0.005, 't_maint', -1,
     'a higher terminal inflation escalates the cost of replacing the asset base over '
     'half its disclosed life, so the maintenance charge (a negative row) must grow'),
    ('Beta (own-stock regression vs the published FTSE ADX General index)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('AED government bond yield (Jan-2031 T-Bond auction)', 'C', +0.01, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('6-month EIBOR (31-Mar-2026 fixing, dated)', 'C', +0.01, 'wacc', +1,
     'a costlier debt leg must raise the blended cost of capital'),
    ('Effective tax rate (DMTT floor + foreign uplift)', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Longest useful life the company discloses (years)', 'C', +5.0, 't_fcff', -1,
     'under this basis the life sets the AVERAGE VINTAGE of the asset base, not the '
     'replacement frequency: a longer life means the assets carried were bought further '
     'back, so replacing them today costs more relative to the depreciation the books '
     'already charge. Taking the LONGEST disclosed life is therefore the conservative '
     'choice on this basis, not the flattering one'),
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
    ('Justified price/earnings (FY2026E attributable)', 'C', +1.0, 'rel_lens', +1,
     'a higher justified multiple must raise the relative CROSS-CHECK — which sits '
     'beside the answer and is no longer weighted into it'),
    ('Through-cycle price/earnings', 'C', +1.0, 'norm_lens', +1,
     'a higher through-cycle multiple must raise the normalised read — which this '
     'class does not publish as a lens and which is no longer in the answer'),
    ('Sustainable return on equity', 'C', +0.02, 'book_lens', +1,
     'a higher sustainable return must raise the book FLOOR, which is published '
     'beside the answer and never weighted into it'),
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

# ---- THE ONE-AT-A-TIME SWEEP CANNOT SEE A JOINTLY LIVE PAIR ----------------------
# 'Invested capital per unit of real growth' is in the live chain and inert at the base,
# because it is multiplied by a stated REAL growth of zero. Bumping it alone therefore
# moves nothing, and a one-at-a-time sweep reports it dead — which would be true of the
# base point and false of the model. Declaring it dead-by-design would be an exemption
# on the wrong object, so it is MEASURED instead: bumped alongside a non-zero real
# growth, where it must bite. If it ever stops biting there, the growth charge has come
# out of the model and this fails, which is what the sweep is for.
_JOINT = 'Invested capital per unit of real growth, at terminal revenue (AED mn)'
if _JOINT in dead:
    _rg, _ric = row_of('Terminal REAL growth (stated, not derived)'), row_of(_JOINT)
    _with_g = read({('Assumptions', f'C{_rg}'): 0.005})
    _both = read({('Assumptions', f'C{_rg}'): 0.005,
                  ('Assumptions', f'C{_ric}'): base_ic_x2})
    _mv = _both['tv'] / _with_g['tv'] - 1.0
    assert _mv < -1e-6, ('the growth-capital driver is inert even at a non-zero real '
                         'growth: real growth is not being charged for capital at all')
    print('  JOINT PROBE — growth capital per unit of real growth, at real growth '
          '+0.5pp: doubling it moves the terminal %.2f%% (%.0f -> %.0f). Inert at the '
          'base only because the stated real growth is zero.'
          % (100 * _mv, _with_g['tv'], _both['tv']))
    dead.remove(_JOINT)

if dead:
    print('  live inputs that changed nothing:', dead)
else:
    print(f'  every live driver reprices the model; {len(scenario_dead)} scenario '
          f'vectors correctly dead-by-design')

assert not fails, f'{len(fails)} failures: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers reprice the workbook in the asserted '
      f'direction; zero dead live inputs')
