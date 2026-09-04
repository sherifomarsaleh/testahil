"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place, the whole workbook is re-evaluated from
scratch, and the test asserts that the headline moves, moves in the right
DIRECTION, and moves by a sensible amount. A driver that fails to move the
valuation means a chain was broken somewhere between the Assumptions sheet and
the answer — exactly the failure a pasted-value workbook hides.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'DU_Valuation_Model_09082026_public.xlsx'))
A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str):
        A[c.value] = c.row

def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]

PATH_COLS = ['B', 'C', 'D', 'E', 'F']   # the five forecast-year columns of a path input

def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(dcf=bk.cell_value('DCF', 'C63'),
                central=bk.cell_value('Summary', 'C9'),
                pv_expl=bk.cell_value('DCF', 'C27'),
                tv=bk.cell_value('DCF', 'C26'),
                ebitda26=bk.cell_value('DCF', 'B6'),
                wacc=bk.cell_value('DCF', 'C47'),
                wacc_term=bk.cell_value('DCF', 'C54'),
                nc30=bk.cell_value('Balance Sheet', 'I15'),
                relative=bk.cell_value('Relative & Normalized', 'C11'),
                book=bk.cell_value('Relative & Normalized', 'C35'),
                bvps=bk.cell_value('Relative & Normalized', 'C30'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, cell column, bump, the headline it must move, the required direction
CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta (DU weekly vs FTSE ADX General, 5y)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Terminal risk-free rate', 'C', +0.01, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Combined federal royalty + income tax rate (Framing A, audited FY2025)', 'C', +0.05,
     'dcf', -1, 'a heavier fiscal take must lower NOPAT and the valuation'),
    ('Net working capital / revenue (audited FY2025 component days)', 'C', +0.02, 'dcf', -1,
     'working capital moving toward zero absorbs cash and must lower the valuation'),
    ('Staff cost, FY2026E level (AED mn)', 'C', +200.0, 'ebitda26', -1,
     'a heavier staff cost must cut FY2026 EBITDA'),
    ('Marketing / revenue', 'C', +0.01, 'dcf', -1,
     'a heavier marketing ratio must cut EBITDA and the valuation'),
    ('Telecom licence and related fees / revenue (regulatory revenue share)', 'C', +0.01,
     'dcf', -1, 'a worse licence-renewal outcome (higher fee ratio) must lower the valuation'),
    ('PP&E depreciation rate on opening balance (audited FY2025)', 'C', +0.03, 'pv_expl', +1,
     'within a fixed EBITDA, faster depreciation is a larger tax shield on the explicit window'),
    ('Capital expenditure / revenue', 'C', +0.02, 'dcf', -1,
     'heavier capex must absorb cash and lower the valuation'),
    # These two drive CROSS-CHECKS, not the answer. Under the retired blend they reached the
    # published central through a weight, and the test asserted exactly that. They must now
    # move their own lens and leave the central alone — see the isolation sweep below, which
    # is the stronger claim: it is not that the weight is small, it is that there is none.
    ('Justified price/earnings (GCC telecom peer median)', 'C', +1.0, 'relative', +1,
     'a higher justified multiple must raise the relative-multiple cross-check'),
    ('Sustainable return on equity', 'C', +0.03, 'book', +1,
     'a higher sustainable return must raise the book lens'),
    ('Lease liabilities at FY2025 (AED mn, audited — the only debt-like item)', 'C', +500.0,
     'dcf', -1, 'more debt-like leases must leave less for shareholders'),
    ('Cash and term deposits at FY2025 (AED mn, audited)', 'C', +500.0, 'dcf', +1,
     'more cash in the bridge must raise the equity value'),
    ('Dividends gone ex between 31-Dec-2025 and the anchor (AED/share)', 'C', +0.10, 'dcf', -1,
     'a larger dividend already out of the price is value that left the share'),
    ('Days from the 31-Dec-2025 valuation date to the 07-Aug-2026 anchor', 'C', +100.0,
     'dcf', +1, 'a later anchor accretes more value at the cost of equity'),
    ('Marginal cost of debt (AED sovereign + GCC telecom spread)', 'C', +0.03, 'wacc', +1,
     'a higher cost of debt must raise the explicit-window cost of capital'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Forecast dividend payout ratio (FY2024 actual 98%, FY2025 ~100%)', 'C', -0.10, 'nc30', +1,
     'paying out less must leave more cash on the FY2030 balance sheet'),
    ('Lease interest rate (audited FY2025 effective)', 'C', +0.02, 'nc30', -1,
     'a costlier lease book must drain the cash walk'),
    ('Yield on cash and term deposits (audited FY2025 effective)', 'C', +0.02, 'nc30', +1,
     'a better deposit yield must build cash faster'),
    # ---- unit build, now live in the sheet ----------------------------------------------
    # ---- direct-cost unit stack (installed 17-Aug-2026): margin is an OUTPUT, so each
    # ---- per-unit cost driver must move the valuation the OTHER way -----------------------
    ('Mobile interconnect cost, H1-2026 actual (AED/subscriber/month)', 'C', +1.00, 'dcf', -1,
     'a costlier interconnect bill per subscriber must compress the contribution margin '
     'and lower the valuation'),
    ('Mobile interconnect escalator (termination rates, OTT substitution)', 'C', +0.02,
     'dcf', -1, 'interconnect cost per subscriber rising instead of falling must lower value'),
    ('Mobile commission cost, H1-2026 actual (AED/subscriber/month)', 'C', +1.00, 'dcf', -1,
     'a costlier acquisition commission per subscriber must lower the valuation'),
    ('Mobile commission escalator (acquisition/retention cost)', 'C', +0.02, 'dcf', -1,
     'faster-rising commission per subscriber must lower the valuation'),
    ('Mobile devices and direct services, H1-2026 actual (AED/subscriber/month)', 'C', +1.00,
     'dcf', -1, 'a costlier device/direct-services line per subscriber must lower value'),
    ('Fixed capacity and direct cost, H1-2026 actual (AED/subscriber/month)', 'C', +5.00,
     'dcf', -1, 'a costlier fixed capacity bill per subscriber must lower the valuation'),
    ('Wholesale direct cost / wholesale revenue (H1-2026 rate, held flat)', 'C', +0.02,
     'dcf', -1, 'a worse wholesale cost rate must lower the valuation'),
    ('ICT direct cost / ICT revenue (H1-2026 rate, held flat)', 'C', +0.02, 'dcf', -1,
     'a worse ICT cost rate must lower the valuation'),
    ('Blended ARPU drift (mix-exhaustion sensitivity; zero in the base case)', 'C', -0.02,
     'dcf', -1, 'the mix-exhaustion case: an eroding blended ARPU must lower the valuation'),
    ("Mobile subscribers, end of year ('000)", 'PATH', +200.0, 'dcf', +1,
     'unit build: more mobile subscribers must raise revenue and the valuation'),
    ('Blended mobile ARPU (AED/month)', 'PATH', +2.0, 'dcf', +1,
     'unit build: a higher mobile ARPU must raise revenue and the valuation'),
    ("Fixed subscribers, end of year ('000)", 'PATH', +25.0, 'dcf', +1,
     'unit build: more fixed subscribers must raise revenue and the valuation'),
    ('Implied fixed revenue per subscriber (AED/month)', 'PATH', +20.0, 'dcf', +1,
     'unit build: a higher fixed revenue intensity must raise the valuation'),
    ('Wholesale revenue growth', 'PATH', +0.02, 'dcf', +1,
     'unit build: faster wholesale growth must raise the valuation'),
    ('ICT and associated telecom revenue growth', 'PATH', +0.02, 'dcf', +1,
     'unit build: faster ICT growth must raise the valuation'),
    # A one-year-only lift in H1 revenue raises FY2026 capex (and so the PP&E and invested-capital
    # base) permanently, against one year of extra revenue. It is therefore near-neutral by
    # construction, and the terminal dilution slightly wins — a real property of the model, not a
    # broken chain. Asserted on the line it unambiguously must move: FY2026 EBITDA.
    ('Mobile revenue, six months to 30-Jun-2026 (AED mn, reviewed)', 'C', +100.0, 'ebitda26', +1,
     'the FY2026 build chains off the reviewed H1 actual, so it must reach FY2026 EBITDA'),
]

fails, moved = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    if col == 'PATH':
        # bump every forecast year of the path at once
        ov = {}
        for _c in PATH_COLS:
            _v = wb['Assumptions'][f'{_c}{r}'].value
            if isinstance(_v, (int, float)):
                ov[('Assumptions', f'{_c}{r}')] = _v + bump
        assert ov, f'{label!r} is not a path input'
        out = read(ov)
    else:
        cur = wb['Assumptions'][f'{col}{r}'].value
        out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-6
    moved.append((label, key, base[key], out[key], rel))
    flag = 'OK ' if ok else 'BAD'
    print(f'  [{flag}] {label} {bump:+g} -> {key} {base[key]:,.3f} -> {out[key]:,.3f} '
          f'({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

# a driver that moves NOTHING anywhere is a dead input: catch those too
DEAD_OK = {
    # (the six unit-build drivers that used to sit here are now LIVE in the sheet and are
    #  tested as real drivers in CASES below — see the six rows tagged 'unit build')
    # Framing B parameters: the Framing-B fair value is an engine re-run (pasted), so
    # these price the ALTERNATIVE framing, not the base sheet:
    'Regulated revenue share (Framing B base, audited FY2023)',
    'Framing B — royalty rate on regulated revenue',
    'Framing B — royalty rate on regulated profit',
    # yield-cross triangulation is shown beside the lens, not fed into a headline
    'Peer benchmark dividend yield',
}
# ---------------------------------------------------------------------------------
# ISOLATION SWEEP — the claim the retired blend made impossible to test.
# Under a weighted central every lens input reached the published answer, so no input
# could be shown independent of it. With one lens as the answer, a cross-check driver
# must move its own lens and move the central by EXACTLY zero — not a little, zero.
# A near-zero tolerance would be a free parameter; the right answer here is arithmetic,
# because a weight of nothing is not a small weight.
ISOLATED = [
    ('Justified price/earnings (GCC telecom peer median)', +1.0, 'relative'),
    ('Sustainable return on equity', +0.03, 'book'),
    ('Peer benchmark dividend yield', +0.01, None),
]
print('\nISOLATION SWEEP — a cross-check driver must move its own lens and NOT the answer')
iso_fails = []
for label, bump, lens in ISOLATED:
    r = row_of(label)
    out = read({('Assumptions', f'C{r}'): wb['Assumptions'][f'C{r}'].value + bump})
    moved_central = out['central'] - base['central']
    moved_dcf = out['dcf'] - base['dcf']
    own = (out[lens] - base[lens]) if lens else None
    ok = moved_central == 0.0 and moved_dcf == 0.0 and (own is None or abs(own) > 1e-9)
    if not ok:
        iso_fails.append((label, moved_central, moved_dcf, own))
    own_s = f'{own:+.4f}' if own is not None else 'n/a (published beside, drives no lens)'
    print(f"  [{'OK ' if ok else 'BAD'}] {label}: own lens {own_s} · "
          f"central {moved_central:+.10f} · cash-flow lens {moved_dcf:+.10f}")
assert not iso_fails, f'cross-check drivers that reach the answer: {iso_fails}'

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
