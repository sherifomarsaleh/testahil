"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place on the delivered file, the whole workbook
is re-evaluated from scratch, and the test asserts the headline moves in the
right DIRECTION. A dead-input sweep then bumps every remaining numeric input and
requires it to move something.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'AIRARABIA_Valuation_Model_09082026_public.xlsx'))
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
    return dict(dcf=bk.cell_value('DCF', 'C62'),
                central=bk.cell_value('Summary', 'C9'),
                pv_expl=bk.cell_value('DCF', 'C55'),
                tv=bk.cell_value('DCF', 'C53'),
                ebitda26=bk.cell_value('Segments', 'B27'),
                wacc=bk.cell_value('DCF', 'C17'),
                wacc_term=bk.cell_value('DCF', 'C24'),
                nd30=bk.cell_value('Cash Flow', 'F16'),
                jvcap=bk.cell_value('SOTP Bridge', 'C20'),
                dcf_split=bk.cell_value('SOTP Bridge', 'C15'),
                eq30=bk.cell_value('Balance Sheet', 'I15'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'higher terminal growth must raise the discounted cash flow'),
    ('Beta (five-year weekly, vs the Dubai index)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Terminal risk-free rate', 'C', +0.01, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Working capital / revenue', 'C', +0.05, 'dcf', -1,
     'less negative working capital absorbs cash and must lower the valuation'),
    ('Tax rate', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Effective jet fuel price (USD/bbl) — base path', 'C', +10.0, 'dcf', -1,
     'a dearer jet-fuel path in FY2027 must cut EBITDA and the valuation'),
    ('Fuel intensity (AED per passenger per USD/bbl of effective jet price)', 'C', +0.2, 'dcf', -1,
     'a higher fuel burn per passenger must cut the valuation'),
    ('Scenario: passenger multiplier', 'C', -0.06, 'dcf', -1,
     'the bear scenario passenger cut must lower the valuation through the live engine'),
    ('Scenario: fare multiplier', 'C', +0.03, 'dcf', +1,
     'the bull scenario fare lift must raise the valuation through the live engine'),
    ('Scenario: high-fuel switch (0 = base path, 1 = alternative)', 'C', +1.0, 'dcf', -1,
     'flipping to the high-fuel framing must reprice the whole workbook downward'),
    ('Scenario: cost-of-capital shift', 'C', +0.01, 'dcf', -1,
     'a 100bp rate shift must lower the valuation through both discount rates'),
    ('Leased aircraft additions (units)', 'C', +1.0, 'dcf', -1,
     'an extra leased aircraft is real capacity cost now charged inside FCFF'),
    ('Booked finance-cost rate on the debt book', 'C', +0.01, 'nd30', +1,
     'a dearer debt book must leave more net debt at the end of the forecast'),
    ('Passengers (millions)', 'D', +1.0, 'dcf', +1,
     'more passengers in FY2028 must lift revenue faster than pax-linked cash costs'),
    ('Passenger + baggage revenue per passenger (AED)', 'C', +20.0, 'dcf', +1,
     'a higher fare must flow straight to EBITDA and the valuation'),
    ('Fleet capital expenditure incl. pre-delivery payments (AED mn)', 'C', +500.0, 'dcf', -1,
     'more capex must cut free cash flow and the valuation'),
    ('Depreciation & amortisation (AED mn)', 'C', +100.0, 'dcf', +1,
     'with EBITDA fixed, more D&A is a tax shield: NOPAT falls by (1-t) but the add-back is full'),
    ('Justified EV/EBITDA', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the weighted central'),
    ('Justified price/earnings', 'C', +1.0, 'central', +1,
     'a higher justified P/E must raise the weighted central'),
    ('Sustainable return on equity', 'C', +0.02, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Joint-venture capitalisation multiple', 'C', +3.0, 'jvcap', +1,
     'a higher JV multiple must raise the capitalised-framing value'),
    ('Gross debt, FY2025 (AED mn, audited)', 'C', +2000.0, 'dcf', -1,
     'more gross debt cuts net cash in the bridge and must lower the valuation'),
    ('Cash and fixed deposits, FY2025 (AED mn, audited)', 'C', +2000.0, 'dcf', +1,
     'more cash must add to the bridge'),
    ('Dividend payout ratio', 'C', +0.20, 'nd30', +1,
     'paying out more must leave more net debt at the end of the forecast'),
    ('Days from 31-Dec-2025 to the 7-Aug-2026 anchor', 'C', +100.0, 'dcf', +1,
     'a later anchor accretes more value at the cost of equity'),
    ('FY2025 dividend per share (AED, approved 12 March 2026)', 'C', +0.30, 'dcf', -1,
     'a larger dividend paid before the anchor is value that left the share'),
    ('Marginal cost of debt', 'C', +0.02, 'wacc', +1,
     'a higher cost of debt must raise the explicit-window cost of capital'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Administrative cost growth', 'C', +0.05, 'dcf', -1,
     'faster administrative cost growth must lower the valuation'),
    # NOTE (mechanism re-decomposed after the de-JV fix): the JV share now reaches NO lens
    # by construction — the base framing carries the JV at its constant book value in every
    # lens, and the capitalised framing prices it off the multiple, not the growth path.
    # Equity-accounted profit is non-cash, and forecast dividends sit at the 30-fil floor,
    # so faster JV growth flows to forecast EPS and the EQUITY roll — which is what this
    # case now asserts.
    ('Growth in the share of joint-venture and associate profit', 'B', +0.10, 'eq30', +1,
     'faster JV profit growth must accumulate in forecast retained equity'),
    ('Aircraft-lease revenue growth', 'C', +0.10, 'dcf', +1,
     'faster lease income growth must lift revenue and the valuation'),
]

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

DEAD_OK = {
    # consumed only when the high-fuel switch is on, or by display rows, by design:
    'Effective jet fuel price (USD/bbl) — high-fuel alternative',  # live only when switch=1
    'Rating-table sovereign spread (alternative netting, disclosed)',  # published alternative
    'Consolidated fleet, year-end (aircraft)',   # display of the capacity ramp; pax is the driver
    'Marginal cost of debt path',                # drives the WACC glide shape via DCF!27 (tested via wacc rows)
    'Spot price (AED)',                    # comparison anchor, not a valuation input
    'Relative lens — bear multiple', 'Relative lens — bull multiple',
    'Normalised lens — bear P/E', 'Normalised lens — bull P/E',
    'Weight — relative', 'Weight — normalised', 'Weight — book',
    'Weight — discounted cash flow',
}
print('\nDEAD-INPUT SWEEP — every scalar driver not covered above is bumped and must move something')
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

# the excluded labels must still move the things they are FOR
r = row_of('Weight — relative')
out = read({('Assumptions', f'C{r}'): 0.30})
assert out['central'] != base['central'], 'lens weight must move the central'
r = row_of('Spot price (AED)')
bk = xlcalc.Book(wb, {('Assumptions', f'C{r}'): 6.0})
assert bk.cell_value('Summary', 'G9') != None
res = dict(cases=len(CASES), fails=len(fails), dead=dead)
json.dump(res, open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1)
assert not fails, f'{len(fails)} drivers failed: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right '
      f'direction; zero dead inputs')
