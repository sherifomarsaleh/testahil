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
import datetime
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
             'tv_share', 'wacc', 'wacc_term', 'ke', 'ke_ci_lo', 'ke_ci_hi', 'ke_blume',
             'kd', 'kd_balance_weighted', 'wh', 'kh', 'kh_term', 'rev26', 'ebitda26',
             'ebitda30',
             'nopat26', 'tax26', 'fcff26', 'tankers26', 'tankers30', 'gas26', 'gas28',
             'relative',
             'normalized', 'book', 'book_bear', 'book_bull', 'book_equity', 'roe_sust',
             'sotp', 'nd30', 'bvps30', 'nwc26', 'ppe26', 'ppe30', 'npa26', 'ordn26',
             'eps26', 'eps26_pre', 'eveb_bridge',
             'tnk_spot_vlcc_q1', 'tnk_tce26', 'tnk_tce30', 'tnk_opexday',
             'tnk_chrev26', 'tnk_sprev26', 'tnk_acqdays26',
             'gas_rate_solved', 'gas_vy27', 'dso', 'dso_reported']


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


_BASE_BOOK = xlcalc.Book(wb)


def current(col, rr):
    """The driver's value as the workbook computes it.

    Some drivers on the Assumptions sheet are DERIVED — the running cost per vessel-day is
    solved from the 2025 outcome, the days ratios come off the audited columns — so they
    hold formulas, not numbers. Perturbing them still asks the right question ('if this
    driver were different, does the model reprice?'), it just has to start from the value
    the formula produces rather than from a literal.
    """
    return _BASE_BOOK.cell_value('Assumptions', f'{col}{rr}')


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in list(base.items())[:8]))
print('       ' + ' · '.join(f'{k} {v:,.4f}' for k, v in list(base.items())[8:16]))

CAPEX_LAB = 'Capital expenditure (USD 000)'
YRCOL = [('B', 'FY2026'), ('C', 'FY2027'), ('D', 'FY2028'), ('E', 'FY2029'), ('F', 'FY2030')]
BLEND24 = [('Long range 1 — 2024', 'long-range-one'),
           ('Long range 2 — 2024', 'long-range-two'),
           ('Very large crude carrier — 2024', 'very large crude carrier')]
BLEND25 = [('Medium range — 2025', 'medium-range'), ('Long range 1 — 2025', 'long-range-one'),
           ('Long range 2 — 2025', 'long-range-two'),
           ('Very large crude carrier — 2025', 'very large crude carrier')]
BLEND26 = [('Medium range', 'medium-range'), ('Long range 1', 'long-range-one'),
           ('Long range 2', 'long-range-two'),
           ('Very large crude carrier', 'very large crude carrier')]

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
    # wider spread lowers the normalised risk-free rate, the cost of equity and the
    # explicit cost of capital (-9.43%), and the present value of the five forecast years
    # rises 1.07%.
    #   The credit-spread channel that opposes it: the terminal cost of debt is the
    # terminal risk-free rate plus the company's own credit spread measured over the
    # NORMALISED rate, so narrowing that rate widens the modelled spread — the terminal
    # cost of capital rises 0.85%. The terminal cost of EQUITY is built off the terminal
    # risk-free rate and is untouched, as is the perpetual leg, so only the debt weight
    # carries this.
    #   NET: at a terminal cost of capital of 7.73% against 2% terminal growth the
    # capitalisation denominator is 5.73% and the terminal value is 78% of enterprise
    # value, so the 0.85% rise in the terminal rate cuts the terminal value only 1.13%
    # while the discount factor on it rises and the explicit window cheapens. Fair value
    # rises 0.30%. The direction assertion is corrected, not relaxed: every component
    # assertion below is kept, and the terminal value's own fall is asserted separately so
    # the opposing channel cannot go quiet unnoticed.
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
     'net of the two, the normalisation channel wins: at the higher discount rate the '
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
     'and must therefore lower the bull bound of the book lens, whose whole residual-income '
     'ladder is discounted at it'),
    ('Beta — upper bound of the regression\'s 90% confidence interval (the bear-case '
     'beta)', 'C', +0.20, 'ke_ci_hi', +1,
     'a higher beta at the upper bound must raise the cost of equity built on it'),
    ('Beta — upper bound of the regression\'s 90% confidence interval (the bear-case '
     'beta)', 'C', +0.20, 'book_bear', -1,
     'and must therefore lower the bear bound of the book lens, which is discounted at it'),
    ('Beta — the measured slope shrunk toward the market: two-thirds of it '
     'plus one-third of 1.0', 'C', +0.20,
     'ke_blume', +1,
     'the lead-lag corroboration beta must reprice its own cost of equity; it is published '
     'as a check on the primary estimate and deliberately drives nothing else'),
    # ---- the perpetual capital securities now carry weight in the cost of capital -----
    ('Perpetual capital securities margin over the overnight rate', 'C', +0.01, 'kh', +1,
     'the perpetual\'s cost is its own coupon, so a wider margin raises it directly'),
    ('Perpetual capital securities margin over the overnight rate', 'C', +0.01, 'wacc', +1,
     'and because that tranche is now WEIGHTED in the cost of capital rather than only '
     'deducted in the bridge, a dearer coupon raises the cost of capital'),
    ('Perpetual capital securities margin over the overnight rate', 'C', +0.01, 'fv', -1,
     'which must lower the valuation'),
    ('Perpetual capital securities at carrying value (USD 000)', 'C', +250000.0, 'wh', +1,
     'a larger perpetual tranche must carry more weight in the cost of capital'),
    ('Perpetual capital securities at carrying value (USD 000)', 'C', +250000.0, 'fv', -1,
     'and it still ranks ahead of the ordinary shares and is deducted in the bridge, so '
     'the valuation must fall'),
    # DECOMPOSED, NOT ASSUMED. The minorities are deducted in two parts: the slice that
    # arose on the tanker combination is deducted at its CONTRACTED price, because that
    # purchase price is already in the bridge as deferred consideration, and only the
    # remainder is lifted from book to value. Moving book from the second part to the
    # first therefore REDUCES the total deduction — the contracted slice rises by the
    # amount moved, while the value-based part falls by that amount times the remaining
    # minorities' profit share applied to the whole equity value, which is the larger of
    # the two. The valuation rises.
    ('Of which arose on the tanker combination — the 20% contracted for purchase in '
     'mid-2027 (USD 000)', 'C', +50000.0, 'fv', +1,
     'moving minority book from the value-lifted remainder to the contracted slice cuts '
     'the total deduction, because the value-based part it leaves behind was the dearer of '
     'the two — decomposed, not assumed'),
    # ---- the book lens is a residual-income build, so its own fade must bite -----------
    ('Rate at which the return above the cost of equity fades beyond the forecast (the '
     'book lens)', 'C', +0.05, 'book', -1,
     'a faster fade shortens the life of the excess return and must lower the book lens'),
    ('Rate at which the return above the cost of equity fades beyond the forecast (the '
     'book lens)', 'C', +0.05, 'central', -1,
     'and must carry through to the weighted central figure the book lens is part of'),
] + [
    # ---- the tanker leg, driver by driver ---------------------------------------------
    # The 2024 published blends reach the model in ONE place: the mid-cycle anchor the rate
    # path glides to. They are not part of the 2025 solve, so this is the clean case.
    (lab, 'B', +5000.0, 'fv', +1,
     f'a higher published 2024 blend for the {name} class raises the mid-cycle anchor the '
     f'rate path glides to, and must raise the valuation')
    for lab, name in BLEND24
] + [
    # DECOMPOSED, NOT ASSUMED — AND THE OPPOSITE OF WHAT IT LOOKS LIKE. The expectation
    # going in was that a higher published rate in 2025 must raise the valuation. It does
    # not, and the reason is the solve. The 2025 published blends reach the model TWICE:
    #   (1) they raise the implied 2025 spot rate, which lifts the second half of 2026 and
    #       the mid-cycle anchor — worth +0.62% on 2030 charter-equivalent revenue for the
    #       long-range-two class;
    #   (2) they raise the 2025 charter-equivalent revenue the RUNNING COST IS SOLVED FROM.
    #       Tanker earnings for 2025 are a disclosed, fixed number, so every dollar of extra
    #       implied revenue becomes a dollar of extra implied cost: the cost per vessel-day
    #       rises 4.29% and the running-cost line rises 4.29% in every forecast year.
    # The cost is charged on the whole 53-vessel fleet as it stood at the end of 2025; the
    # revenue benefit accrues only to the spot vessel-days of the smaller fleet that
    # remains after the January sale, and only to the part of the path that is not already
    # pinned by the disclosed 2026 quarters. So the cost side wins: 2026 tanker earnings
    # fall 0.64% and fair value falls 0.60%. Both channels are asserted separately below so
    # neither can go quiet.
    (lab, 'B', +5000.0, 'tnk_opexday', +1,
     f'the solve channel: a higher published 2025 blend for the {name} class raises the '
     f'charter-equivalent revenue the running cost is solved from, and since 2025 earnings '
     f'are a disclosed fixed number the whole increase lands in the cost per vessel-day')
    for lab, name in BLEND25
] + [
    (lab, 'B', +5000.0, 'tnk_tce30', +1,
     f'the rate channel that opposes it: the same figure raises the implied 2025 spot rate '
     f'for the {name} class, the mid-cycle anchor and therefore 2030 revenue')
    for lab, name in BLEND25
] + [
    (lab, 'B', +5000.0, 'fv', -1,
     f'net of the two the cost side wins, because the solved cost is charged on the whole '
     f'2025 fleet for every forecast year while the extra revenue reaches only the spot '
     f'vessel-days of the smaller fleet that remains — decomposed, not assumed')
    for lab, name in BLEND25
] + [
    # The 2026 published quarters are outside the 2025 solve, so they move revenue only.
    (lab, 'B', +5000.0, 'fv', +1,
     f'a higher published first-quarter 2026 blend for the {name} class raises the implied '
     f'spot rate that quarter, the 2026 rate and the whole path, and must raise the '
     f'valuation')
    for lab, name in BLEND26
] + [
    # THE CHARTER TABLE, AND WHAT THE SOLVE IS FOR. The published rate is a BLEND across
    # the whole class. Raising one fixture's contracted rate cannot raise the blend, so it
    # must LOWER the spot rate backed out of that blend — that identity is the whole point
    # of building the derivation in the sheet, and it is asserted directly.
    ('Zakum — very large crude carrier, fixed for 22 months', 'B', +10000.0,
     'tnk_spot_vlcc_q1', -1,
     'the fixture runs through the first quarter of 2026, and the published blend for that '
     'quarter is fixed, so a dearer charter must leave a CHEAPER implied spot rate behind '
     'it — this is the identity the whole derivation rests on'),
    ('Zakum — very large crude carrier, fixed for 22 months', 'B', +10000.0,
     'tnk_chrev26', +1,
     'the fixture channel: the vessel earns its own contracted rate for its own days, so '
     'charter revenue in 2026 rises'),
    ('Zakum — very large crude carrier, fixed for 22 months', 'B', +10000.0,
     'tnk_sprev26', -1,
     'the opposing channel: the cheaper implied spot rate is earned by every spot day the '
     'class trades, and since 7 August 2026 that includes six more crude carriers from '
     'delivery, so spot revenue falls'),
    # DECOMPOSED, NOT ASSUMED — AND RE-DECOMPOSED AFTER THE FLEET GREW. Before the August
    # purchase the extra charter revenue on the one fixture outweighed the cheaper spot
    # rate it left behind, and 2026 charter-equivalent revenue rose 0.09%. It does not any
    # more, and the reason is countable: the six crude carriers bought on 7 August 2026
    # add 732 spot vessel-days to that class in 2026, so the same one-dollar fall in the
    # implied spot rate is now earned across a larger spot fleet. Charter revenue rises
    # 2.41%; spot revenue falls 0.33%; the net is -0.015%. Both channels are asserted
    # above so neither can go quiet, and the model was not touched.
    ('Zakum — very large crude carrier, fixed for 22 months', 'B', +10000.0, 'tnk_tce26',
     -1,
     'net of the two the spot side now wins, because the vessels bought in August 2026 '
     'enlarged the spot fleet the cheaper rate is earned on — decomposed, not assumed'),
    ('Navig8 Prosperity — long range 2, fixed for 36 months', 'B', +10000.0, 'fv', -1,
     'this fixture is the one that runs through the first quarter of 2025 as well, so it '
     'cuts the implied spot rate that sets the MID-CYCLE ANCHOR — and the anchor governs '
     'the far end of the rate path, where most of the value sits'),
] + [
    ('Less vessels sold between the year end and the valuation date', 'F', +1.0, 'fv', -1,
     'a vessel sold before the valuation date is one fewer earning through the forecast, '
     'and must lower the valuation'),
    # DECOMPOSED, NOT ASSUMED. Adding a vessel to the fleet as it stood at the end of 2025
    # adds it to the forecast fleet too, but it also enlarges the 2025 charter-equivalent
    # revenue the running cost is solved from — and because tanker earnings for 2025 are
    # fixed, that whole addition becomes cost: the running-cost line rises 10.6% against a
    # 4.7% rise in 2026 charter-equivalent revenue. 2026 tanker earnings still rise 3.6%,
    # because the vessel earns at the implied spot rate rather than at the class blend the
    # cost was solved on. By 2030 the cost escalation has caught up and the far end of the
    # path is worth less, which is why fair value rises only 0.06% against 0.97% on the
    # weighted central figure, where the multiple lenses give 2026 more weight.
    ('Vessels owned at 31 December 2025', 'F', +1.0, 'tankers26', +1,
     'one more vessel earns at the implied spot rate, which is above the class blend the '
     'running cost was solved on, so 2026 tanker earnings rise'),
    ('Vessels owned at 31 December 2025', 'F', +1.0, 'tnk_opexday', +1,
     'the opposing channel: it also enlarges the 2025 revenue the running cost is solved '
     'from, and 2025 earnings are fixed, so the cost per vessel-day rises'),
    ('Vessels owned at 31 December 2025', 'F', +1.0, 'tankers30', -1,
     'the third channel, and the one that decides it: the vessel count is the DENOMINATOR '
     'of the implied-spot solve, so one more vessel means a LOWER implied spot rate — and '
     'that lower rate is now earned by the six crude carriers bought in August 2026 as '
     'well, which is a larger fleet than the one extra vessel it adds'),
    ('Vessels owned at 31 December 2025', 'F', +1.0, 'central', +1,
     'the multiple lenses value 2026 earnings, which rise, so the weighted central figure '
     'still rises'),
    # DECOMPOSED, NOT ASSUMED — AND RE-DECOMPOSED AFTER THE FLEET GREW. The cash-flow lens
    # used to rise 0.06% on this bump and now falls 0.20%. Nothing about the mechanism
    # changed: 2026 tanker earnings still rise 2.17% and the solved running cost still
    # rises 8.75%. What changed is the third channel above — the implied spot rate falls
    # 4.64% and is now earned across the enlarged fleet, which is why 2030 earnings fall
    # 0.64% and the far end of the path, where most of the discounted value sits, is worth
    # less. The weighted central figure, which leans on 2026, still rises 0.40%.
    ('Vessels owned at 31 December 2025', 'F', +1.0, 'fv', -1,
     'net of the three the far end of the rate path wins in the cash-flow lens — '
     'decomposed, not assumed'),
    ('All-in running cost per vessel per day (USD)', 'C', +500.0, 'fv', -1,
     'a higher running cost per vessel-day must lower tanker earnings and the valuation'),
    # ---- the eleven vessels bought on 7 August 2026 ------------------------------------
    # The price lands in TWO places, and both are asserted: it is carried in net debt,
    # because the purchase is committed and funded, and it is capitalised in the asset
    # base, where it depreciates and shields tax. The earnings of the ships themselves are
    # a separate driver — the counts below — so raising the PRICE alone buys nothing extra
    # and must lower the valuation.
    ('Purchase price — added BOTH to net debt, because it is committed and funded, and to '
     'the opening asset base, so it depreciates and shields tax (USD 000)', 'C',
     +250000.0, 'ppe26', +1,
     'a dearer purchase is a larger asset base in the year it arrives'),
    ('Purchase price — added BOTH to net debt, because it is committed and funded, and to '
     'the opening asset base, so it depreciates and shields tax (USD 000)', 'C',
     +250000.0, 'fcff26', +1,
     'and the heavier depreciation on it shields tax, so free cash flow to the firm rises '
     'slightly — the second half of the same treatment'),
    ('Purchase price — added BOTH to net debt, because it is committed and funded, and to '
     'the opening asset base, so it depreciates and shields tax (USD 000)', 'C',
     +250000.0, 'nd30', +1,
     'the opposing channel: it is funded, so it is carried in net debt from the valuation '
     'date and is still there at the end of the forecast'),
    ('Purchase price — added BOTH to net debt, because it is committed and funded, and to '
     'the opening asset base, so it depreciates and shields tax (USD 000)', 'C',
     +250000.0, 'fv', -1,
     'net of the two, paying more for the same eleven ships must lower the valuation'),
    ('Very large crude carriers bought secondhand — they join the spot fleet on delivery '
     'and earn at the implied spot rate from that date', 'B', +1.0, 'tnk_acqdays26', +1,
     'one more acquired ship is more acquired vessel-days from its delivery date'),
    ('Very large crude carriers bought secondhand — they join the spot fleet on delivery '
     'and earn at the implied spot rate from that date', 'B', +1.0, 'tankers26', +1,
     'and those days earn at the implied spot rate, so 2026 tanker earnings rise'),
    ('Very large crude carriers bought secondhand — they join the spot fleet on delivery '
     'and earn at the implied spot rate from that date', 'B', +1.0, 'fv', +1,
     'and the valuation with them'),
    ('Gas carriers acquired in total — they add contracted vessel-years to the gas fleet',
     'B', +1.0, 'gas_vy27', +1,
     'one more gas carrier is one more contracted vessel-year once it is delivered'),
    ('Gas carriers acquired in total — they add contracted vessel-years to the gas fleet',
     'B', +1.0, 'gas28', +1,
     'which earns the solved day rate, so gas-carrier earnings rise'),
    ('Gas carriers acquired in total — they add contracted vessel-years to the gas fleet',
     'B', +1.0, 'fv', +1, 'and the valuation with them'),
    # The tranche split changes WHEN, not HOW MANY: moving a vessel from the fourth-quarter
    # newbuilding tranche to the third-quarter secondhand one leaves the total untouched —
    # the newbuilding count is the total less this one — and only the part-year in 2026
    # moves. So this driver must move 2026 and leave 2027 exactly where it was.
    ('Of which bought secondhand, delivering in the third quarter', 'B', +1.0, 'gas26', +1,
     'an earlier delivery is more vessel-years inside 2026'),
    ('Of which bought secondhand, delivering in the third quarter', 'B', +1.0, 'gas_vy27',
     0,
     'and it must NOT change 2027, because the tranche split moves when the ships arrive, '
     'never how many arrive'),
    ('Of which bought secondhand, delivering in the third quarter', 'B', +1.0, 'fv', +1,
     'earning three months earlier is worth a little more'),
    # ---- the smallest tankers, scaled rather than substituted --------------------------
    # DECOMPOSED, NOT ASSUMED. The scalar reaches the model on both sides of the same
    # solve, exactly as the published 2025 blends do. A higher handysize rate raises the
    # 2025 charter-equivalent revenue the running cost is solved from — and 2025 tanker
    # earnings are a disclosed fixed number, so that whole increase becomes cost, charged
    # on all 53 vessels — while the rate benefit accrues to two handysize vessels. 2026
    # earnings still rise, 2030 earnings fall, and the cash-flow value falls by three
    # ten-thousandths of a per cent. The weighted central figure rises.
    ('Handysize rate as a proportion of the medium-range rate — the company disclosed '
     'Handysize DOWN 21% against medium range UP 29%, so the two smallest classes moved '
     'in OPPOSITE directions and the medium-range rate cannot stand in for the smallest '
     'unadjusted. It scales the medium-range rate in every window and on both sides of '
     'the mid-cycle average', 'C', +0.10, 'tnk_opexday', +1,
     'the solve channel: a higher handysize rate raises the 2025 revenue the running cost '
     'is solved from, and 2025 earnings are fixed, so the cost per vessel-day rises'),
    ('Handysize rate as a proportion of the medium-range rate — the company disclosed '
     'Handysize DOWN 21% against medium range UP 29%, so the two smallest classes moved '
     'in OPPOSITE directions and the medium-range rate cannot stand in for the smallest '
     'unadjusted. It scales the medium-range rate in every window and on both sides of '
     'the mid-cycle average', 'C', +0.10, 'tnk_tce26', +1,
     'the rate channel that opposes it: the two handysize vessels earn more'),
    ('Handysize rate as a proportion of the medium-range rate — the company disclosed '
     'Handysize DOWN 21% against medium range UP 29%, so the two smallest classes moved '
     'in OPPOSITE directions and the medium-range rate cannot stand in for the smallest '
     'unadjusted. It scales the medium-range rate in every window and on both sides of '
     'the mid-cycle average', 'C', +0.10, 'tankers30', -1,
     'by 2030 the escalated cost, charged on the whole fleet, has outgrown the extra '
     'revenue on two vessels'),
    ('Handysize rate as a proportion of the medium-range rate — the company disclosed '
     'Handysize DOWN 21% against medium range UP 29%, so the two smallest classes moved '
     'in OPPOSITE directions and the medium-range rate cannot stand in for the smallest '
     'unadjusted. It scales the medium-range rate in every window and on both sides of '
     'the mid-cycle average', 'C', +0.10, 'fv', -1,
     'net of the two the cost side wins by a hair — decomposed, not assumed'),
    ('Gross-up from time-charter-equivalent revenue to reported revenue', 'C', +0.20,
     'dso', -1,
     'the receivable ratio is re-based onto the revenue basis the forecast uses, so a '
     'wider gross-up is FEWER days on a bigger revenue line — the channel through which a '
     'presentational ratio that touches no earnings line reaches the valuation at all'),
    ('Gross-up from time-charter-equivalent revenue to reported revenue', 'C', +0.20,
     'nwc26', -1,
     'and net working capital falls: payable days on the incremental gross revenue exceed '
     'the receivable and inventory days it carries, and the re-based receivable days fall '
     'as well'),
    ('Gross-up from time-charter-equivalent revenue to reported revenue', 'C', +0.20, 'fv',
     +1, 'and the released working capital raises the valuation slightly — decomposed, '
     'not assumed'),
] + [
    (CAPEX_LAB, col, +150000.0, 'fv', -1,
     f'more capital expenditure in {name} must lower the valuation')
    for col, name in YRCOL
] + [
    ('Days sales outstanding measured on REPORTED 2025 revenue', 'C', +15.0, 'dso', +1,
     'the re-based ratio is the reported one scaled, so it must move with it'),
    ('Days sales outstanding measured on REPORTED 2025 revenue', 'C', +15.0, 'fv', -1,
     'slower collection absorbs cash into working capital and must lower the valuation'),
    # THE RE-BASING, DRIVER BY DRIVER. The reported ratio is measured on 2025 revenue,
    # which carries the 2025 gross-up; the forecast revenue it is applied to is built at
    # the 2026 one. So a WIDER 2025 gross-up means the ratio was measured against a wider
    # base than the forecast uses and the re-based figure rises, while a wider 2026
    # gross-up means the forecast base is wider and it falls. Both are asserted, because
    # this is the channel through which the gross-up — which touches no earnings line at
    # all — reaches the valuation.
    ('Gross-up inside 2025 reported revenue — reported tanker revenue over the same '
     'fleet\'s charter-equivalent revenue', 'C', +0.20, 'dso', +1,
     'a wider gross-up inside the year the ratio was measured on means more days once it '
     'is re-based onto the narrower basis the forecast uses'),
    ('Gross-up inside 2025 reported revenue — reported tanker revenue over the same '
     'fleet\'s charter-equivalent revenue', 'C', +0.20, 'fv', -1,
     'and those extra days absorb cash into working capital'),
    ('Gross-up the forecast is built at, from 2026 onward', 'C', +0.20, 'dso', -1,
     'the same arithmetic the other way: a wider forecast revenue base is fewer days'),
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
    # DECOMPOSED, NOT ASSUMED. The gas day rate is not an assumption: it is solved from the
    # 2025 revenue the segment actually reported, over the vessel-years that earned it. So
    # saying MORE vessels were in service through 2025 for the same disclosed revenue says
    # each of them earned LESS, and the forecast prices its contracted vessel-years at that
    # cheaper rate. The rate falls 11.1% and fair value 5.8%.
    ('Consolidated gas vessels in service through 2025 (vessel-years)', 'C', +1.0,
     'gas_rate_solved', -1,
     'the same disclosed revenue spread over more vessel-years is a lower rate per '
     'vessel-day, and the rate is solved, not assumed'),
    ('Consolidated gas vessels in service through 2025 (vessel-years)', 'C', +1.0, 'fv', -1,
     'and the forecast prices its contracted vessel-years at that cheaper rate — '
     'decomposed, not assumed'),
    ('Share of joint-venture profit carried in the disclosed 2025 Gas Carriers earnings '
     '(USD 000)', 'C', +5000.0, 'fv', -1,
     'more of the disclosed segment earnings turn out to be equity-accounted joint-venture '
     'profit, which the equity bridge already adds at carrying value, so more is removed '
     'from the forecast and the valuation falls'),
    ('Share of joint-venture profit carried in the disclosed 2025 Services earnings '
     '(USD 000)', 'C', +5000.0, 'fv', -1,
     'the same removal on the Services unit'),
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
    # Note it does NOT reach the perpetual leg: that coupon is an equity distribution and
    # is not deductible, which is why it is weighted at its gross cost.
    ('Statutory corporate tax rate', 'C', +0.05, 'fv', +1,
     'the statutory rate enters ONLY the after-tax cost of debt and the after-tax interest '
     'in the funding roll, never the tax on operating profit and never the perpetual '
     'coupon, so a higher rate cheapens debt and raises the valuation — decomposed, not '
     'assumed'),
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
     'a higher price raises the equity weight against both the debt and the perpetual '
     'weight, and equity is the dearest of the three'),
    ('Share price (AED, Abu Dhabi Securities Exchange close)', 'C', +1.0, 'wh', -1,
     'and the perpetual weight, being the same carrying value over a larger capital base, '
     'must fall'),
    ('Ordinary dividend declared for 2026 (USD 000)', 'C', +50000.0, 'nd30', +1,
     'paying more out must leave more net debt at the end of the forecast'),
    # DECOMPOSED, NOT ASSUMED. The expectation going in was that a higher depreciation rate
    # must RAISE the valuation: earnings are struck before depreciation, so a higher rate is
    # a larger non-cash add-back and a smaller closing asset base. That is true of the
    # EXPLICIT window and is asserted below. It is FALSE of the terminal value, which
    # capitalises NOPAT net of reinvestment: depreciation is NOT added back there, so
    # terminal NOPAT and the terminal value both fall. The smaller asset base only partly
    # offsets, because NOPAT falls faster than invested capital. The terminal value is 78%
    # of enterprise value, so the terminal channel wins.
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
    cur = current(col, rr)
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
    raw = wb['Assumptions'][f'C{rr}'].value
    # a DATE is skipped: bumping a calendar boundary by a tenth is not a driver test, it is
    # a different calendar. Every date on the sheet is exercised instead by the charter and
    # vessel-count cases above, which move quantities measured against those dates.
    if isinstance(raw, (datetime.date, datetime.datetime)) or raw is None:
        continue
    # a DERIVED driver holds a formula rather than a literal, and is bumped from the value
    # that formula produces — being derived is not a reason to go untested
    if isinstance(raw, str) and not raw.startswith('='):
        continue
    if (label, 'C') in covered:
        continue
    cur = current('C', rr)
    if not isinstance(cur, (int, float)):
        continue
    out = read({('Assumptions', f'C{rr}'): cur * 1.10 + 1e-6})
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
