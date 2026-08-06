"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the DELIVERED file, so it is tested on the delivered file: each
driver below is perturbed in place, the whole workbook is re-evaluated from scratch, and
the test asserts the headline moves in the asserted DIRECTION. A dead-input sweep bumps
every remaining driver and requires it to move something.

ONE DIRECTION HERE IS THE OPPOSITE OF THE TEXTBOOK ONE, AND IT IS NOT A BUG. Raising
terminal growth LOWERS this company's value. Terminal return on invested capital is 9.4%
against a terminal cost of capital of 16.3%, so the reinvestment that growth requires
(RR = g / ROIC) earns less than it costs. Asserting the conventional +1 here would be
asserting the wrong expectation, and the mechanism was decomposed before the sign was
set — not after the test failed.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'SCEM_Valuation_Model_06082026_public.xlsx'))
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
    return dict(dcf=bk.cell_value('DCF', 'B39'),
                central=bk.cell_value('Fundamental Valuation', 'D10'),
                pv_expl=bk.cell_value('DCF', 'B30'),
                tv=bk.cell_value('DCF', 'B26'),
                ebitda26=bk.cell_value('DCF', 'B7'),
                rev26=bk.cell_value('DCF', 'B5'),
                wacc=bk.cell_value('DCF', 'C46'),
                wacc_term=bk.cell_value('DCF', 'C53'),
                cash30=bk.cell_value('Balance Sheet', 'I7'),
                eq30=bk.cell_value('Balance Sheet', 'I12'),
                asset_lens=bk.cell_value('Relative & Normalized', 'B33'),
                rel_lens=bk.cell_value('Relative & Normalized', 'B12'),
                norm_lens=bk.cell_value('Relative & Normalized', 'B22'),
                roic=bk.cell_value('DCF', 'B24'),
                netcash=bk.cell_value('DCF', 'B36'),
                ebitda23=bk.cell_value('Income Statement', 'B6'),
                util23=bk.cell_value('Unit Build', 'B8'),
                util24=bk.cell_value('Unit Build', 'C8'),
                price23=bk.cell_value('Unit Build', 'B9'),
                util26=bk.cell_value('Unit Build', 'E8'),
                nopat26=bk.cell_value('DCF', 'B11'))


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, column, bump, headline it must move, required direction, why
CASES = [
    ('Terminal growth', 'B', +0.01, 'dcf', -1,
     'terminal ROIC 9.4% is BELOW terminal WACC 16.3%, so growth must be bought with '
     'reinvestment that earns less than it costs — higher g LOWERS the value'),
    ('Beta', 'B', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Risk-free rate (EGP 10-year)', 'B', +0.02, 'dcf', -1,
     'a higher risk-free rate raises the explicit cost of capital and must lower the value'),
    ('Sovereign default spread (CDS basis)', 'B', +0.01, 'dcf', +1,
     'a wider spread is netted OUT of the risk-free rate, so it LOWERS the cost of equity'),
    ('Equity risk premium (CDS basis)', 'B', +0.02, 'dcf', -1,
     'a higher equity risk premium must lower the valuation'),
    ('Terminal risk-free rate', 'B', +0.02, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Terminal equity risk premium', 'B', +0.02, 'dcf', -1,
     'a higher terminal premium must lower the valuation'),
    ('Terminal debt weight', 'B', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Terminal cost of debt', 'B', +0.03, 'wacc_term', +1,
     'a dearer terminal debt must raise the terminal cost of capital'),
    ('Pre-tax cost of debt', 'B', +0.05, 'wacc', +1,
     'a higher cost of debt must raise the explicit cost of capital, even if barely'),
    # The tax rate pulls the two halves of the model in OPPOSITE directions and BOTH legs
    # are asserted, so neither can silently break. Operating: a higher rate cuts NOPAT
    # (-6.5%), the present value of the explicit years (-6.7%) and the terminal value
    # (-12.6%). Derived cash: FY2024 treasury income is SOLVED as (disclosed profit less
    # the disposal gain) / (1 - t) less EBIT, so a higher assumed rate means more pre-tax
    # income was needed to produce the disclosed after-tax profit — treasury income rises
    # +16.8% and with it the derived cash balance. Net cash is 37% of equity value, so on
    # the per-share headline the cash leg wins by a nose (+0.7%). The model is right; the
    # conventional single-signed expectation was wrong.
    ('Corporate tax rate', 'B', +0.05, 'pv_expl', -1,
     'a higher tax rate must lower NOPAT and the present value of the explicit years'),
    ('Corporate tax rate', 'B', +0.05, 'tv', -1,
     'a higher tax rate must lower terminal NOPAT and the terminal value'),
    ('Corporate tax rate', 'B', +0.05, 'netcash', +1,
     'the derived FY2024 treasury income is grossed up at (1 - t), so a higher rate '
     'implies a LARGER cash balance behind the same disclosed profit'),
    ('Delta working capital / delta revenue', 'B', +0.05, 'dcf', -1,
     'more working capital absorbs cash and must lower the valuation'),
    ('Nameplate capacity', 'B', +0.5, 'asset_lens', +1,
     'more capacity at the same value per tonne must raise the asset lens'),
    # Clean and one-directional: only the terminal block moves. Explicit-window present
    # value, net cash and the cost of capital are all untouched.
    ('Replacement cost of capacity', 'B', +20.0, 'dcf', -1,
     'a dearer replacement cost raises terminal invested capital, which LOWERS terminal '
     'return on capital (-13.3%) and so RAISES the reinvestment rate g/ROIC (+15.4%), '
     'cutting the terminal value (-17.4%) and the value per share'),
    ('Replacement cost of capacity', 'B', +20.0, 'roic', -1,
     'more invested capital against the same terminal NOPAT must lower the return on it'),
    ('Justified EV per tonne of capacity', 'B', +10.0, 'asset_lens', +1,
     'a higher justified value per tonne must raise the asset lens'),
    ('Justified EV/EBITDA', 'B', +1.0, 'rel_lens', +1,
     'a higher justified multiple must raise the relative lens'),
    ('Justified price/earnings', 'B', +1.0, 'norm_lens', +1,
     'a higher justified price/earnings must raise the normalised lens'),
    ('Mid-cycle EBITDA margin', 'B', +0.02, 'rel_lens', +1,
     'a richer mid-cycle margin must raise the relative lens'),
    ('Dividend payout ratio', 'B', +0.20, 'cash30', -1,
     'paying more out must leave less cash at the end of the forecast'),
    ('Gross debt', 'B', +2000.0, 'dcf', -1,
     'more debt against the same cash must leave less for shareholders'),
    ('Shares outstanding', 'B', +20.0, 'dcf', -1,
     'the same equity value across more shares must lower the value per share'),
    ('FY2025 cash as a multiple of FY2024 cash', 'B', +0.20, 'dcf', +1,
     'a larger opening cash balance flows straight through the bridge'),
    # FY2023 treasury income is consumed ONLY by the FY2023 income statement — the cash
    # chain runs off FY2024. It is asserted where it actually acts rather than on a
    # headline it does not touch.
    ('FY2023 treasury income', 'B', +100.0, 'ebitda23', -1,
     'FY2023 EBIT is solved as the disclosed loss LESS treasury income, so more treasury '
     'income means a worse underlying FY2023 and a lower derived EBITDA'),
]

fails, rows = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-9
    rows.append(dict(driver=label, bump=bump, headline=key, base=base[key],
                     bumped=out[key], rel=rel, direction=('up' if sign > 0 else 'down'),
                     passed=bool(ok), why=why))
    print(f"  [{'OK ' if ok else 'BAD'}] {label} {bump:+g} -> {key} {base[key]:,.3f} -> "
          f"{out[key]:,.3f} ({rel:+.3%})")
    if not ok:
        fails.append((label, key, delta, why))

# ---- dead-input sweep --------------------------------------------------------
# Two inputs legitimately do not move the valuation, and the reason is stated rather than
# waved through: the spot price is the thing fair value is COMPARED with, and the tender
# offer price is a disclosed reference point the model deliberately consumes nowhere.
#
# A NOTED DESIGN PROPERTY, not a broken chain. The market-size and share pairs move
# capacity utilisation and realised price per tonne but NOT value, and that is correct:
# the unit build DECOMPOSES disclosed revenue rather than driving it. Volume is market x
# share and realised price is then solved as revenue / volume, so raising market size
# raises volume and lowers price by exactly the same factor. Forecast revenue compounds
# off the FY2025 product, which is therefore unchanged too. Valuation leverage comes from
# the volume-GROWTH and price-GROWTH drivers, not from the level split between them. The
# sweep below still requires these inputs to move something, and they do.
DEAD_OK = {
    'Spot price',
    'Vicat tender offer price',
}
print('\nDEAD-INPUT SWEEP — every remaining driver is bumped and must move something')
dead = []
seen = {c[0] for c in CASES}
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    if label in seen or label in DEAD_OK:
        continue
    for col in ('B', 'C', 'D', 'E', 'F'):
        cell = wb['Assumptions'][f'{col}{r}']
        if not isinstance(cell.value, (int, float)):
            continue
        out = read({('Assumptions', f'{col}{r}'): cell.value * 1.10 + 1e-6})
        if all(abs(out[k] - base[k]) < 1e-9 for k in base):
            dead.append(f'{label} [{col}{r}]')
        break
if dead:
    print('  inputs that changed nothing:', dead)
else:
    print('  none — every remaining driver reprices the model')

json.dump(dict(base=base, cases=rows, dead=dead,
               n_cases=len(CASES), n_failed=len(fails)),
          open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1, default=float)

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction; 0 dead inputs')
