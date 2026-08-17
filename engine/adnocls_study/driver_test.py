"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

The READ FIRST sheet tells the reader that changing a blue cell on Assumptions reprices the
model. That is a claim about the DELIVERED file, so it is tested on the delivered file: each
driver below is perturbed IN PLACE, the whole workbook is re-evaluated from scratch, and the
test asserts that the headline moves, and moves in the asserted DIRECTION.

A driver that fails to move the valuation means a chain was broken somewhere between the
Assumptions sheet and the answer — exactly the failure a pasted-value workbook hides. The
dead-input sweep at the foot catches the same failure for every driver not named above.

Where an expectation and the model disagree, the FIRST hypothesis is that the expectation is
wrong and the model is right. Four drivers in this model behave that way — the statutory tax
rate, the sovereign default spread, the revenue gross-up and the depreciation rate. Each is
decomposed in a comment beside its case below, and the ASSERTION was changed, never the
model.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(
    os.path.join(HERE, 'ADNOCLS_Valuation_Model_09082026_public.xlsx'))
ANCH = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']

A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str) and c.value.strip():
        A.setdefault(c.value, c.row)

HEADLINES = ['fv', 'fv_beta_alt', 'central', 'central_beta_alt', 'pv_expl', 'tv', 'ev',
             'tv_share', 'wacc', 'wacc_term', 'ke', 'ke_ci_lo', 'ke_ci_hi', 'ke_dimson',
             'kd', 'rev26', 'ebitda26', 'ebitda30',
             'nopat26', 'tax26', 'fcff26', 'tankers26', 'tankers30', 'gas28', 'relative',
             'normalized', 'book', 'book_bear', 'book_bull', 'roe_sust', 'sotp', 'nd30',
             'bvps30', 'nwc26', 'ppe30', 'npa26', 'ordn26']


def split(ref):
    sh, coord = ref.rsplit('!', 1)
    return sh.strip("'"), coord


def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return {k: bk.cell_value(*split(ANCH[k])) for k in HEADLINES}


def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in list(base.items())[:8]))
print('       ' + ' · '.join(f'{k} {v:,.4f}' for k, v in list(base.items())[8:16]))

MID = 'Mid-cycle rate anchor (USD per day)'
CAPEX_LAB = 'Capital expenditure (USD 000)'
CLSCOL = [('B', 'handysize'), ('C', 'medium range'), ('D', 'long range 1'),
          ('E', 'long range 2'), ('F', 'very large crude carrier')]
YRCOL = [('B', 'FY2026'), ('C', 'FY2027'), ('D', 'FY2028'), ('E', 'FY2029'), ('F', 'FY2030')]

# label, column, bump, headline it must move, required direction, why
CASES = [
    ('Terminal growth', 'C', +0.005, 'fv', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta — own-stock weekly regression against the published index of its own exchange',
     'C', +0.20, 'fv', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Terminal risk-free rate', 'C', +0.01, 'fv', -1,
     'a higher terminal risk-free rate raises the terminal cost of capital and must lower '
     'the valuation'),
    ('Equity risk premium (mature premium plus country risk)', 'C', +0.01, 'fv', -1,
     'a higher equity risk premium must lower the valuation'),
    # DECOMPOSED, NOT ASSUMED — AND RE-DECOMPOSED AFTER THE BETA CHANGED, BECAUSE THE NET
    # SIGN FLIPPED. Both channels below are unchanged in mechanism and both are still
    # asserted; what changed is which one wins, and it changed for a reason the model can
    # be made to show.
    #   The normalisation channel: the spread is subtracted from the observed yield, so a
    # wider spread lowers the normalised risk-free rate (-24.6%), the cost of equity
    # (-10.7%) and the explicit cost of capital (-10.2%), and the present value of the five
    # forecast years rises 1.24%.
    #   The credit-spread channel that opposes it: the terminal cost of debt is the
    # terminal risk-free rate plus the company's own credit spread measured over the
    # NORMALISED rate, so narrowing that rate widens the modelled spread — the terminal
    # cost of debt rises 19.9% and the terminal cost of capital 0.91%. The terminal cost of
    # EQUITY is built off the terminal risk-free rate and is untouched, so only the debt
    # weight carries this.
    #   WHY THE NET SIGN MOVED. Under the previous beta the terminal cost of capital was
    # 6.51% against 2% terminal growth, a capitalisation denominator of 4.51%, and the
    # terminal value was 84% of enterprise value. On the FTSE ADX General Index beta the
    # terminal cost of capital is 8.21%, the denominator 6.21%, and the terminal value 78%.
    # The SAME 0.91% rise in the terminal rate now cuts the terminal value by only 1.20%
    # instead of ~1.7%, because a wider denominator is proportionally less sensitive — and
    # it is cutting a smaller share of the answer. Meanwhile the discount factor on that
    # terminal value RISES 1.33%, because the glide starts from an explicit rate that fell
    # 0.92 percentage points. The two together leave the present value of the terminal
    # value 0.12% HIGHER, not lower, so the normalisation channel now wins outright and
    # fair value rises 0.44%. The direction assertion is corrected, not relaxed: every
    # component assertion below is kept, and the terminal value's own fall is now asserted
    # separately so the opposing channel cannot go quiet unnoticed.
    ('Sovereign default spread (netted out of the risk-free rate)', 'C', +0.01, 'wacc', -1,
     'the normalisation channel: the spread is subtracted from the observed yield, so a '
     'wider spread lowers the normalised risk-free rate and the explicit cost of capital'),
    ('Sovereign default spread (netted out of the risk-free rate)', 'C', +0.01, 'pv_expl',
     +1, 'and therefore raises the present value of the five forecast years'),
    ('Sovereign default spread (netted out of the risk-free rate)', 'C', +0.01,
     'wacc_term', +1,
     'the credit-spread channel that opposes it: the terminal cost of debt is the '
     'terminal risk-free rate plus the credit spread measured over the NORMALISED rate, so '
     'narrowing that rate widens the spread and raises the terminal cost of capital'),
    ('Sovereign default spread (netted out of the risk-free rate)', 'C', +0.01, 'tv', -1,
     'and that dearer terminal rate must still cut the terminal value itself — the '
     'opposing channel is asserted in its own right, not inferred from the net'),
    ('Sovereign default spread (netted out of the risk-free rate)', 'C', +0.01, 'fv', +1,
     'net of the two, the normalisation channel now wins: at the higher discount rate the '
     'terminal capitalisation denominator is wider and the terminal value is a smaller '
     'share of the answer, so the terminal cut no longer outweighs the cheaper explicit '
     'window and the larger discount factor it produces — decomposed, not assumed'),
    ('Beta — the same regression against an equal-weight composite of that exchange\'s '
     'names (the disclosed alternative)', 'C', +0.20, 'fv_beta_alt', -1,
     'the contested alternative construction must reprice its own leg of the model'),
    ('Beta — the same regression against an equal-weight composite of that exchange\'s '
     'names (the disclosed alternative)', 'C', +0.20, 'fv', 0,
     'and it must NOT touch the primary reading — the two constructions are carried side '
     'by side, never blended'),
    # The two ends of the regression's own 90% confidence interval. They set the bear and
    # bull discount rates, so each must move its own cost of equity UP and the bound that
    # is discounted at it DOWN. This pair of assertions is what would have caught the
    # inversion that appeared when the low bound was built on the alternative index
    # construction instead: that construction now carries the LOWER beta, so it stopped
    # being the demanding case the moment the regressor changed.
    ('Beta — lower bound of the regression\'s 90% confidence interval (the bull-case '
     'beta)', 'C', +0.20, 'ke_ci_lo', +1,
     'a higher beta at the lower bound must raise the cost of equity built on it'),
    ('Beta — lower bound of the regression\'s 90% confidence interval (the bull-case '
     'beta)', 'C', +0.20, 'book_bull', -1,
     'and must therefore lower the bull bound of the book lens, which is discounted at it'),
    ('Beta — upper bound of the regression\'s 90% confidence interval (the bear-case '
     'beta)', 'C', +0.20, 'ke_ci_hi', +1,
     'a higher beta at the upper bound must raise the cost of equity built on it'),
    ('Beta — upper bound of the regression\'s 90% confidence interval (the bear-case '
     'beta)', 'C', +0.20, 'book_bear', -1,
     'and must therefore lower the bear bound of the book lens, which is discounted at it'),
    ('Beta — lead-lag sum beta from the same series, one lead and two lags', 'C', +0.20,
     'ke_dimson', +1,
     'the lead-lag corroboration beta must reprice its own cost of equity; it is published '
     'as a check on the primary estimate and deliberately drives nothing else'),
] + [
    (MID, col, +5000.0, 'fv', +1,
     f'a higher mid-cycle anchor for the {name} class must raise the valuation')
    for col, name in CLSCOL
] + [
    ('All-in running cost per vessel per day (USD)', 'C', +500.0, 'fv', -1,
     'a higher running cost per vessel-day must lower tanker earnings and the valuation'),
] + [
    (CAPEX_LAB, col, +150000.0, 'fv', -1,
     f'more capital expenditure in {name} must lower the valuation')
    for col, name in YRCOL
] + [
    ('Days sales outstanding', 'C', +15.0, 'fv', -1,
     'slower collection absorbs cash into working capital and must lower the valuation'),
    ('Days payable outstanding', 'C', +15.0, 'fv', +1,
     'slower payment releases cash from working capital and must raise the valuation'),
    ('Days inventory outstanding', 'C', +5.0, 'fv', -1,
     'more inventory absorbs cash and must lower the valuation'),
] + [
    (f'{seg} — earnings margin', 'C', +0.05, 'fv', +1,
     f'a higher {seg} margin must raise the valuation')
    for seg in ['Offshore Contracting', 'Offshore Services', 'Offshore Projects',
                'Dry-Bulk and Containers', 'Services']
] + [
    ('Gas carriers — earnings margin', 'C', +0.05, 'fv', +1,
     'a higher gas-carrier margin must raise the valuation'),
    ('Gas carriers — contracted vessel-years', 'C', +2.0, 'fv', +1,
     'more contracted gas vessel-years must raise the valuation'),
] + [
    ('Integrated Logistics — income tax rate', 'C', +0.05, 'fv', -1,
     'a higher tax rate on the logistics units must lower NOPAT and the valuation'),
    ('Shipping — income tax rate', 'C', +0.05, 'fv', -1,
     'a higher tax rate on the shipping units must lower NOPAT and the valuation'),
    ('Services — income tax rate', 'C', +0.05, 'fv', -1,
     'a higher tax rate on the services unit must lower NOPAT and the valuation'),
    # DECOMPOSED, NOT ASSUMED. The statutory rate does NOT tax operating profit in this
    # model — the tax on NOPAT is the business-unit mix above, at the rates each unit
    # actually bears. The statutory rate appears only in the after-tax cost of debt and in
    # the after-tax interest inside the funding roll. A higher statutory rate therefore
    # makes debt cheaper after tax, LOWERS the cost of capital and RAISES the valuation.
    # The expectation "a higher tax rate must lower the valuation" is wrong for THIS cell;
    # it is right for the three business-unit rates above, which is where NOPAT is taxed.
    ('Statutory corporate tax rate', 'C', +0.05, 'fv', +1,
     'the statutory rate enters ONLY the after-tax cost of debt and the after-tax interest '
     'in the funding roll, never the tax on operating profit, so a higher rate cheapens '
     'debt and raises the valuation — decomposed, not assumed'),
    ('Statutory corporate tax rate', 'C', +0.05, 'wacc', -1,
     'the same cell, seen at the cost of capital: a higher rate lowers the after-tax cost '
     'of debt'),
] + [
    ('Weight on the enterprise multiple within the relative lens', 'C', +0.10, 'relative',
     +1, 'the enterprise multiple values the shares above the earnings multiple, so more '
     'weight on it must raise the relative lens'),
    ('Share of 2026 earnings exposed to spot rates', 'C', +0.10, 'relative', -1,
     'more spot exposure pulls the blend toward the cheaper spot-tanker multiple'),
    ('Share price (AED, Abu Dhabi Securities Exchange close)', 'C', +1.0, 'wacc', +1,
     'a higher price raises the equity weight, and equity is the dearer of the two'),
    # DECOMPOSED, NOT ASSUMED. The expectation going in was that grossing up reported
    # revenue must LOWER the valuation, because revenue drives receivables. It does not.
    # The gross-up leaves earnings untouched, so it raises reported revenue AND total
    # operating cost by the same absolute amount. Receivables run at 108.4 days of revenue
    # and inventories at 14.1 days of operating cost, but payables run at 131.7 days of the
    # same operating cost — so the incremental gross revenue releases more payable days
    # than it absorbs in receivable and inventory days. Net working capital FALLS 1.1%,
    # 2026 free cash flow to the firm rises 1.9%, and fair value rises 0.03%.
    ('Gross-up from time-charter-equivalent revenue to reported revenue', 'C', +0.20,
     'nwc26', -1,
     'payable days on the incremental gross revenue exceed the receivable and inventory '
     'days it carries, so grossing up releases working capital'),
    ('Gross-up from time-charter-equivalent revenue to reported revenue', 'C', +0.20, 'fv',
     +1, 'and the released working capital raises the valuation slightly — decomposed, '
     'not assumed'),
    ('Perpetual capital securities at carrying value (USD 000)', 'C', +250000.0, 'fv', -1,
     'the securities rank ahead of the ordinary shares and are deducted in the bridge'),
    ('Ordinary dividend declared for 2026 (USD 000)', 'C', +50000.0, 'nd30', +1,
     'paying more out must leave more net debt at the end of the forecast'),
    # DECOMPOSED, NOT ASSUMED. The expectation going in was that a higher depreciation rate
    # must RAISE the valuation: earnings are struck before depreciation, so a higher rate is
    # a larger non-cash add-back and a smaller closing asset base. That is true of the
    # EXPLICIT window and is asserted below — depreciation rises 13.2%, the tax charge falls
    # 6.6% on the shield, 2026 free cash flow rises 1.1% and the present value of the five
    # forecast years rises 0.4%. It is FALSE of the terminal value, which capitalises NOPAT
    # net of reinvestment: depreciation is NOT added back there, so terminal NOPAT falls
    # 5.8% and the terminal value 6.3%. The smaller asset base only partly offsets, because
    # NOPAT falls faster than invested capital (the return on invested capital falls 2.3%).
    # The terminal value is 78% of enterprise value, so the net effect is a 5.9% fall.
    ('Depreciation rate on property, plant and equipment', 'C', +0.01, 'fcff26', +1,
     'the explicit-window channel: depreciation is added back, so only its tax shield '
     'reaches free cash flow, and free cash flow rises'),
    ('Depreciation rate on property, plant and equipment', 'C', +0.01, 'tv', -1,
     'the terminal channel: the terminal value capitalises NOPAT net of reinvestment and '
     'does NOT add depreciation back, so a heavier charge cuts it'),
    ('Depreciation rate on property, plant and equipment', 'C', +0.01, 'fv', -1,
     'net of the two, the terminal channel wins — decomposed, not assumed'),
]

fails, table = [], []
for label, col, bump, key, sign, why in CASES:
    rr = row_of(label)
    cur = wb['Assumptions'][f'{col}{rr}'].value
    out = read({('Assumptions', f'{col}{rr}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    # sign 0 is an ISOLATION assertion, not a weaker one: the driver must leave this
    # headline exactly where it was. It is how the two beta constructions are held apart —
    # if one ever leaked into the other's leg, they would be blended rather than published
    # side by side, which is the one thing this study says it never does.
    ok = (abs(delta) < 1e-12) if sign == 0 else ((delta * sign > 0) and abs(rel) > 1e-9)
    table.append((label, col, bump, key, base[key], out[key], rel, sign, ok, why))
    print(f"  [{'OK ' if ok else 'BAD'}] {label[:52]:54s} {col} {bump:+11g} -> {key:14s} "
          f'{base[key]:>12,.4f} -> {out[key]:>12,.4f} ({rel:+.3%})')
    if not ok:
        fails.append((label, col, key, delta, why))

# a driver that moves NOTHING anywhere is a dead input: catch those too
print('\nDEAD-INPUT SWEEP — every driver not covered above is bumped and must move '
      'something')
covered = {(c[0], c[1]) for c in CASES}
dead = []
for label, rr in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{rr}']
    if not isinstance(cell.value, (int, float)):
        continue
    if (label, 'C') in covered:
        continue
    out = read({('Assumptions', f'C{rr}'): cell.value * 1.10 + 1e-6})
    if all(abs(out[k] - base[k]) < 1e-12 for k in base):
        dead.append(label)
if dead:
    print('  INPUTS THAT CHANGED NOTHING:', dead)
else:
    print('  none — every remaining driver reprices the model')

json.dump([dict(driver=t[0], column=t[1], bump=t[2], headline=t[3], base=t[4], bumped=t[5],
                relative=t[6], expected_sign=t[7], ok=t[8], why=t[9]) for t in table],
          open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1)

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction, 0 dead inputs')
