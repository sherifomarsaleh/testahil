"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place, the whole workbook is re-evaluated from
scratch, and the test asserts that the headline moves, moves in the right
DIRECTION, and moves by a nonzero amount. A driver that fails to move the
valuation means a chain was broken somewhere between the Assumptions sheet and
the answer — exactly the failure a pasted-value workbook hides.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'du_study'))
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'SAVOLA_Valuation_Model_19082026_public.xlsx'))
ANCH = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']
A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str):
        A[c.value] = c.row

def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]

PATH_COLS = ['B', 'C', 'D', 'E', 'F']

def ref(key):
    sh, cell = ANCH[key].split('!')
    return sh, cell

def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    out = {}
    for k, akey in [('dcf', 'dcf_ps'), ('central', None), ('rev26', 'seg_grev_b'),
                    ('ebitda26', 'seg_geb_b'), ('pvexp', 'dcf_pvexp'),
                    ('wacc', 'dcf_wacc'), ('wacccds', 'dcf_wacccds'),
                    ('cash30', 'bs_cash_i'), ('roic26', 'sf_roic_c'),
                    ('eps26', 'is_eps_e')]:
        if akey is None:
            out[k] = bk.cell_value('Summary', 'C9')
        else:
            sh, cell = ref(akey)
            out[k] = bk.cell_value(sh, cell)
    return out

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, cell column ('C' scalar or 'PATH'), bump, headline, required direction, why
CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta (SAVOLA weekly vs TASI, 5y, Dimson)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Risk-free rate: PUBLISHED SAR sovereign curve, FTSE SAGBI 7-10y YTM '
     '(31-Jul-2026 factsheet)', 'C',
     +0.005, 'dcf', -1, 'a higher risk-free rate must lower the valuation'),
    ('Combined zakat + income tax rate on core profit', 'C', +0.05, 'dcf', -1,
     'a heavier fiscal take must lower NOPAT and the valuation'),
    ('Capital expenditure (SAR mn, incl. intangibles)', 'PATH', +50.0, 'dcf', -1,
     'heavier capex must absorb cash and lower the valuation'),
    ('Days inventory outstanding', 'C', +5.0, 'dcf', -1,
     'more days of inventory absorb cash and must lower the valuation'),
    ('Days payable outstanding', 'C', +5.0, 'dcf', +1,
     'longer payable days release cash and must raise the valuation'),
    ('Days sales outstanding', 'C', +2.0, 'dcf', -1,
     'more receivable days absorb cash and must lower the valuation'),
    ('Contract liabilities / revenue', 'C', +0.002, 'dcf', +1,
     'a larger customer-prepayment float must raise the valuation'),
    ('Oil gross profit per tonne (SAR/t)', 'PATH', +20.0, 'dcf', +1,
     'unit build: a better oil GP/tonne must raise EBITDA and the valuation'),
    ('Sugar gross profit per tonne (SAR/t)', 'PATH', +10.0, 'dcf', +1,
     'unit build: a better sugar GP/tonne must raise the valuation'),
    ('Pasta gross profit per tonne (SAR/t)', 'PATH', +25.0, 'dcf', +1,
     'unit build: a better pasta GP/tonne must raise the valuation'),
    ('Oil volume growth', 'PATH', +0.01, 'dcf', +1,
     'unit build: more oil tonnes at a positive GP/tonne must raise the valuation'),
    ('Sugar volume growth', 'PATH', +0.01, 'dcf', +1,
     'unit build: more sugar tonnes must raise the valuation'),
    ('Pasta volume growth', 'PATH', +0.01, 'dcf', +1,
     'unit build: more pasta tonnes must raise the valuation'),
    ('Oil revenue-per-tonne growth', 'PATH', +0.005, 'dcf', -1,
     'pass-through pricing with GP/tonne held: higher revenue per tonne only scales the '
     'revenue-linked operating costs, so it must LOWER the valuation — the sign that '
     'proves margin is an output, not an input'),
    ('Nuts & spices revenue path (Mehbaj folded in, flagged)', 'PATH', +30.0, 'dcf', +1,
     'the nuts margin (26.5% gross vs 23.5% opex) is positive at the EBITDA line'),
    ('Nuts & spices gross margin path', 'PATH', +0.01, 'dcf', +1,
     'a richer nuts mix must raise the valuation'),
    ('Store count, end of year (company guidance 20+/yr; +8/yr run-rate variant priced '
     'on Sensitivity)', 'PATH', +10.0, 'dcf', +1,
     'more stores at a positive store margin must raise the valuation'),
    ('Sales-per-average-store growth (Framing A; opening measured as a range -7.1% to '
     '-6.0% over the undisclosed Jun-2025 count)', 'PATH', +0.01,
     'dcf', +1, 'better sales density must raise the valuation'),
    ('Panda gross margin (H1-2026 actual, held)', 'C', +0.005, 'dcf', +1,
     'a better Panda gross margin must raise the valuation'),
    ('Panda store-opex / revenue (measured H1-2026)', 'C', +0.005, 'dcf', -1,
     'heavier store opex must lower the valuation'),
    ('Framing A scale gain on the opex ratio from FY2028 (per year)', 'C', +0.001, 'dcf',
     +1, 'a bigger scale gain must raise the valuation'),
    ('Herfy revenue growth', 'PATH', +0.01, 'dcf', +1,
     'Herfy revenue at a positive EBITDA margin must raise the valuation'),
    ('Herfy EBITDA margin (H1-2026 actual 18.7%, held FLAT — a margin INPUT at the '
     'finest disclosed level, flagged)', 'C', +0.01, 'dcf', +1,
     'a better Herfy margin must raise the valuation'),
    ('Al Kabeer revenue growth', 'PATH', +0.01, 'dcf', +1,
     'Al Kabeer growth must raise the valuation'),
    ('Eliminations / Food-Processing segment revenue (measured FY2025)', 'C', +0.005,
     'rev26', +1, 'a smaller elimination must raise group revenue'),
    ('Unallocated corporate costs (SAR mn)', 'PATH', +20.0, 'dcf', -1,
     'heavier corporate costs must lower the valuation'),
    ('Owned-PP&E depreciation rate on opening balance (measured FY2025)', 'C', +0.01,
     'pvexp', +1,
     'within a fixed EBITDA, faster depreciation is a larger tax shield on the explicit '
     'window'),
    ('Right-of-use / lease growth (store-driven)', 'PATH', +0.01, 'dcf', -1,
     'a faster-growing lease charge must lower the valuation'),
    ('Lease effective interest rate (measured FY2025)', 'C', +0.01, 'dcf', -1,
     'a costlier lease book must raise the cost of capital and lower the valuation'),
    ('Marginal SAR cost of debt (SAIBOR + murabaha spread)', 'C', +0.01, 'wacc', +1,
     'a higher cost of debt must raise the explicit-window cost of capital'),
    ('Saudi sovereign CDS spread (CDS basis — JANUARY-2026 vintage, flagged)', 'C', +0.005, 'wacccds', -1,
     'a wider CDS strips more from rf on the CDS basis and must lower that cost of '
     'capital'),
    ('Dividend payout (stated policy 50-60% of net profit; midpoint)', 'C', -0.10,
     'cash30', +1, 'paying out less must leave more cash on the FY2030 balance sheet'),
    ('Dividend gone ex between valuation date and anchor (SAR/share)', 'C', +0.10, 'dcf',
     -1, 'a larger dividend already out of the price is value that left the share'),
    ('Days from the 31-Dec-2025 valuation date to the 18-Aug-2026 anchor', 'C', +100.0,
     'dcf', +1, 'a later anchor accretes more value at the cost of equity'),
    ("Herfy share price (its own Tadawul listing, 18-Aug-2026)", 'C', +2.0, 'dcf', -1,
     "a dearer Herfy raises the 51% outside interest deducted in the bridge"),
    ("Kinan share of results, H1-2026 actual (SAR mn)", 'C', +5.0, 'dcf', +1,
     'a stronger Kinan raises the capitalized associate value in the bridge'),
    ('Other net liabilities (tax/zakat accruals + DTL − DTA − other assets)', 'C', +100.0,
     'dcf', -1, 'more debt-like accruals must leave less for shareholders'),
    ('Conglomerate / EM-mix discount on the peer-mix multiple', 'C', +0.05, 'central', -1,
     'a deeper discount must lower the relative and normalised lenses and the central'),
    ('Normalised mid-cycle operating EBITDA margin', 'C', +0.002, 'central', +1,
     'a richer normalised margin must raise the central'),
    ('Weight — discounted cash flow', 'C', +0.05, 'central', +1,
     'more weight on a positive lens must raise the weighted central'),
    ('Recurring net income H1-2026 (company net-income analysis)', 'C', +20.0,
     'central', +1, 'a higher trailing recurring base must raise the relative lens'),
    ('Tiryaki sale-proceeds receivable (on the 31-Dec-2025 balance sheet; settled in '
     'Tiryaki shares H1-2026)', 'C', +100.0, 'dcf', +1,
     'a larger bridge asset must raise equity value'),
    ('Al Mehbaj consideration (Q2-2026 interims note 19: 5.4 paid + 6.0 deferred)', 'C',
     +10.0, 'dcf', -1, 'a larger acquisition consideration is a claim on equity'),
    ('Loans and borrowings at 30-Jun-2026 (WACC weight leg, reviewed interims)', 'C',
     +500.0, 'wacc', -1,
     'more of the cheaper debt in the weights must lower the blended cost of capital'),
    ('Equity attributable to owners, 30-Jun-2026 (reviewed; book-lens base)', 'C',
     +500.0, 'central', +1, 'a larger book base must raise the book lens'),
    ('Terminal equity weight', 'C', +0.05, 'dcf', -1,
     'more of the dearer equity in the terminal mix must raise the terminal rate and '
     'lower the valuation'),
    ('Panda (Retail) segment revenue FY2025', 'C', +200.0, 'dcf', +1,
     'a larger measured store-revenue base lifts every forecast year'),
]

fails = []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    if col == 'PATH':
        ov = {}
        for _c in PATH_COLS:
            _v = wb['Assumptions'][f'{_c}{r}'].value
            if isinstance(_v, (int, float)):
                ov[('Assumptions', f'{_c}{r}')] = _v + bump
        assert ov, f'{label!r} is not a path input'
        out = read(ov)
    else:
        cur = wb['Assumptions'][f'C{r}'].value
        assert isinstance(cur, (int, float)), (label, cur)
        out = read({('Assumptions', f'C{r}'): cur + bump})
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
    # informational base shown beside the build; the nuts path is a direct driver
    'Nuts & spices revenue FY2025 (residual to the audited segment)',
    # surplus-cash yield: the walk stays in NET DEBT in every base-case year, so the
    # MAX(−netdebt,0) leg it multiplies is zero throughout — disclosed, not hidden
    'Yield on surplus cash (observed 1Y SAR sovereign)',
    # Almarai is quoted in the peer table but deliberately excluded from both multiple
    # legs (dairy-platform premium); the exclusion is stated on the lens sheet
    'Peer P/E — Almarai (settled 18-Aug close)',
    # the 10.5% terminal-return VARIANT is display-only by design: the base terminal
    # return is COMPUTED on the DCF sheet from the model's own invested capital, and
    # the variant fair value is a whole-model engine re-run (pasted, stated)
    'Terminal return on capital — 10.5% UPSIDE VARIANT (the base is COMPUTED as '
    'year-5 NOPAT on year-5 opening invested capital, on the DCF sheet)',
    # Expert 1's Herfy carve-out inputs feed the expert appendix, whose values are
    # whole-model engine outputs on the Fundamental Valuation sheet (pasted, stated)
    'Herfy non-current liabilities (note 20; Expert-1 carve-out)',
    'Herfy current lease portion, CONSTRUCTED estimate (flagged)',
    'Herfy cash, CONSTRUCTED estimate (flagged)',
    # intangibles are held flat BY CONVENTION (intangible capex = amortisation), so the
    # balance stays in total assets and the foot check but cancels out of every value
    # chain — value-neutral by construction, stated on the Balance Sheet
    'Intangible assets and goodwill',
    # the right-of-use BALANCE enters total assets and the foot check; the value chain
    # runs off the right-of-use CHARGE (its own driver above) — balance is display/foot
    'Right-of-use assets',
    # spot: moves the market-value WACC weights and every vs-spot cell; asserted as a
    # real driver would be circular (fair value responding to price), so it is exempted
    'Spot price (SAR, SETTLED 18-Aug-2026 close)',
}
print('\nDEAD-INPUT SWEEP — every scalar driver not covered above is bumped and must move '
      'something')
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
    print('  none — every remaining scalar driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right '
      'direction; dead-input sweep clean')
