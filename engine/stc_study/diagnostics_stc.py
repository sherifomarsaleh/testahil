"""STC — the two output records [R-ENF-05]: the reverse read, and the sign test.

WHAT THESE ARE FOR. Every gate in this repository examines how a study was BUILT. These
two look at the ANSWER. The first states what the PRICE believes under this study's own
drivers, which turns a disagreement into a measurable one — not "we are 13% below" but
"the price is paying for a beta of 0.53 against the 0.71 this stock's own five-year
weekly regression gives, 1.7 standard errors apart". The second records every judgement
this study made where the evidence permits more than one answer, priced BOTH WAYS, and
counts which direction they were resolved in: any single contested choice is defensible,
what is not is a study resolving every one of them the same way and never noticing.

THE HARD PART IS KEEPING THE REVERSE READ OUT OF THE MODEL. A rate solved from a price
and then used anywhere in a valuation is the reverse-engineered terminal this house
prohibits outright, arriving through a side door. So it is written HERE, to its own file,
and no builder reads it back — a fact checked from outside rather than promised.

THE SOLVE RUNS ON THE MODEL'S OWN FUNCTION. It imports stc_compute and bisects
dcf_ps_at(), rather than interpolating the published sensitivity grid or
re-implementing the discounted cash flow. A re-implementation would grade something
other than what ships.
"""
import io
import contextlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))

# Importing the model re-runs it. That is deliberate and it is safe: the run is
# deterministic — verified byte-for-byte on the committed numbers file — so this cannot
# move the study, and it guarantees the solve is against the model as it actually stands
# rather than against a copy of its outputs.
with contextlib.redirect_stdout(io.StringIO()):
    import stc_compute as M                                            # noqa: E402

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
C = D['coc_record']
BETA_REG = D['dcf']['wacc_build']['beta_reg']
SPOT = D['spot']
WE, KD_AT = C['weight_equity'], C['kd_aftertax']


def beta_to_wacc(b):
    """The schedule's own arithmetic, not a second copy of it."""
    return WE * (C['rf_star'] + b * C['erp']) + (1.0 - WE) * KD_AT


def wacc_to_beta(w):
    return ((w - (1.0 - WE) * KD_AT) / WE - C['rf_star']) / C['erp']


assert abs(beta_to_wacc(C['beta']) - C['wacc_exp']) < 1e-9, \
    'the reconstruction must reproduce the committed schedule before it is trusted'


def solve_wacc_for(price, lo=0.02, hi=None, iters=200):
    """The cost of capital at which this model returns `price`."""
    hi = M.WACC if hi is None else hi
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if M.dcf_ps_at(mid, M.TG) > price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


W_IMPLIED = solve_wacc_for(SPOT)
B_IMPLIED = wacc_to_beta(W_IMPLIED)
assert abs(M.dcf_ps_at(W_IMPLIED, M.TG) - SPOT) < 0.01, 'the solve must reproduce the price'

# WHAT THE PRICE CANNOT BE PAYING FOR, WHICH IS THE MORE USEFUL HALF. This study's own
# crux names capital intensity as the swing driver, and the reverse read shows the
# disagreement is not there at all: two full percentage points of revenue below the
# modelled intensity — further than any of the three filed years ran — still lands well
# short of the market price. The disagreement lives in the discount rate.
CAPEX_FLOOR = M.dcf_ps_at(M.WACC, M.TG, capex_shift=-0.02)

DIAG = {
    'published_central': D['central'],
    'published_spot': SPOT,
    'spot': SPOT,
    'spot_date': D['spot_date'],
    'implied': {
        'quantity': 'the equity beta the traded price implies, through the cost of '
                    'capital that reproduces it on this study\'s own drivers',
        'value': B_IMPLIED,
        'study_value': C['beta'],
        'solved_on': 'stc_compute.dcf_ps_at() by bisection on the weighted cost of '
                     'capital, holding the terminal growth, the forecast drivers and '
                     'every other input at their published values; the beta is then '
                     'recovered from that rate through the schedule\'s own arithmetic, '
                     'which is asserted to reproduce the committed cost of capital '
                     'before it is used backwards.',
    },
    'implied_wacc': W_IMPLIED,
    'study_wacc': C['wacc_exp'],
    'beta_standard_errors_apart': (C['beta'] - B_IMPLIED) / BETA_REG['se'],
    'reading': (
        'The price is paying for a beta of %.4f. This stock\'s own %.2f-year weekly '
        'regression against its exchange\'s published index gives %.4f with a standard '
        'error of %.4f, so the market\'s implied beta sits %.2f standard errors below '
        'the point estimate — inside what the regression cannot rule out, and not what '
        'it measures. THAT IS THE WHOLE DISAGREEMENT, and it is a disagreement about '
        'the price of risk rather than about the business.'
        % (B_IMPLIED, BETA_REG['window_years'], C['beta'], BETA_REG['se'],
           (C['beta'] - B_IMPLIED) / BETA_REG['se'])),
    'not_the_crux': (
        'The study\'s own crux names capital intensity as the swing driver, and the '
        'price is NOT paying for a lighter one: two percentage points of revenue below '
        'the modelled intensity — lighter than any of the three filed years ran — '
        'reaches only SAR %.2f against a market price of %.2f. No capital-spending '
        'assumption inside this company\'s own history closes the gap, which is worth '
        'knowing precisely because the crux says otherwise.' % (CAPEX_FLOOR, SPOT)),
    'used_by': 'NOTHING. This file is a diagnostic and no builder reads it; a quantity '
               'solved from a price and fed back into a valuation is the '
               'reverse-engineered rate this house prohibits outright.',
}

# ---------------------------------------------------------------- the sign test
# A contested judgement is one where the EVIDENCE PERMITS MORE THAN ONE ANSWER and no
# standing rule settles it. Corrections applied under a binding rule are not judgements —
# there was no choice — so the rebuild's fourteen levers are recorded in the rebuild
# ledger and deliberately not here.
_base = D['central']
_bshift = M.dcf_ps_at(beta_to_wacc(C['beta'] + BETA_REG['se']), M.TG)
_guided_mid = sum(D['drivers']['capex_guidance_band']) / 2.0
_guided = M.dcf_ps_at(M.WACC, M.TG,
                      capex_shift=_guided_mid - D['drivers']['capex_pct'][0])
_glide = M.dcf_ps_at(M.WACC, M.TG,
                     ebitda_shift=0.325 - D['drivers']['ebitda_m'][-1])
_tg_real = M.dcf_ps_at(M.WACC, M.TG + 0.005)
_br = D['bridge_record']
_nci_book = (_br['equity_value'] + _br['nci']['deduction']
             - _br['nci']['book']) / _br['shares_mn']

JUDGEMENTS = {
    'published_central': D['central'],
    'published_spot': SPOT,
    'threshold': 0.05,
    'judgements': [
        {'name': 'which lens is the answer',
         'adopted': 'the cash-flow model is the central',
         'alternative': 'the enterprise multiple on this company\'s own trading history',
         'value_adopted': _base,
         'value_alternative': D['lenses']['relative']['base'],
         'why': 'One class primary IS the central and the rest are cross-checks '
                'published beside it; no weights are applied anywhere, because a number '
                'produced by averaging several methods is a new method with parameters '
                'nobody tested. This is the study\'s most consequential contested '
                'judgement and both reads are published side by side rather than '
                'averaged. The multiple lens capitalises what the company earns today at '
                'what the market has paid for it; the cash-flow lens charges for the '
                'capital it must keep spending to go on earning it.'},
        {'name': 'the beta: the point estimate, or shrunk toward the market prior',
         'adopted': 'the own-stock regression at its point estimate',
         'alternative': 'one standard error toward the market prior, which the '
                        'cost-of-capital procedure permits for a noisy beta',
         'value_adopted': _base,
         'value_alternative': _bshift,
         'why': 'The regression is the first tier of the house preference order and it '
                'passes its usability gate, so the point estimate is what the method '
                'returns. It is recorded as contested rather than settled because the '
                'regression explains under a third of this stock\'s variance, and a '
                'shrinkage toward the prior is expressly permitted for exactly that '
                'condition. Adopting the raw estimate is the higher-value choice and it '
                'is not a free one.'},
        {'name': 'capital intensity: the filed years, or management\'s guided band',
         'adopted': 'the three filed years\' own mean, measured from the statements',
         'alternative': 'the midpoint of the band management guides to',
         'value_adopted': _base, 'value_alternative': _guided,
         'why': 'Guidance is SCORED against what happens and never consumed as an input, '
                'because a forward target leans the same way an optimistic model does. '
                'The guided midpoint is nonetheless a real alternative a reader may '
                'prefer, and it is worth less than the materiality line either way.'},
        {'name': 'the margin: an output of the cost build, or an assumed improvement',
         'adopted': 'an output — the cost stack decides it, and it runs flat',
         'alternative': 'the mix-driven improvement to 32.5% an earlier edition assumed',
         'value_adopted': _base, 'value_alternative': _glide,
         'why': 'Margins are outputs wherever the filings disclose enough to build cost '
                'per unit, and they do here. The alternative is what this study itself '
                'published before the cost stack was rebuilt, so it is the honest '
                'counterfactual rather than an invented one.'},
        {'name': 'the debt tax shield: the statutory rate, or the effective one',
         'adopted': 'the statutory rate, which is the marginal rate an authority allows',
         'alternative': 'the effective rate the three filed years actually bore',
         'value_adopted': _base, 'value_alternative': 37.8397,
         'why': 'An effective rate is the average a company paid and a shield is the '
                'marginal rate allowed on the income-tax portion of its base; the two '
                'are not required to agree. What is genuinely unsourced is the split '
                'between zakat and income tax by ownership, which would place the true '
                'shield below the statutory rate. The change was made, measured and '
                'withdrawn rather than left as a bare constant.'},
        {'name': 'terminal real growth',
         'adopted': 'zero real growth, stated',
         'alternative': 'half a point of real growth in perpetuity',
         'value_adopted': _base, 'value_alternative': _tg_real,
         'why': 'Terminal growth is stored as a real rate on the house macro path and '
                'recomputes to its nominal, so the judgement is the REAL number and it '
                'is written down as the number it is. Zero is the default and a positive '
                'real rate would need incremental capital behind it that nothing '
                'discloses.'},
        {'name': 'the minority interest: its share of value, or its book cost',
         'adopted': 'a value-share proxy from the minority\'s own disclosed profit share',
         'alternative': 'the book value carried on the latest balance sheet',
         'value_adopted': _base, 'value_alternative': _nci_book,
         'why': 'The model capitalises 100% of subsidiary cash flow, so the minority\'s '
                'claim is worth its share of THAT value rather than what it historically '
                'cost. Book is published beside it so a reader sees the choice and not '
                'only its result, and the deduction is taken from equity value rather '
                'than from enterprise value.'},
    ],
}

if __name__ == '__main__':
    import research_protocol as RP
    with open(os.path.join(HERE, 'diagnostics.json'), 'w') as f:
        json.dump(DIAG, f, indent=1)
    with open(os.path.join(HERE, 'contested_judgements.json'), 'w') as f:
        json.dump(JUDGEMENTS, f, indent=1)
    RP.assert_reverse_dcf(DIAG, HERE, ticker='STC')
    res = RP.assert_contested_judgements(JUDGEMENTS, ticker='STC')
    print('implied beta %.4f against the study\'s %.4f (%.2f standard errors)'
          % (B_IMPLIED, C['beta'], DIAG['beta_standard_errors_apart']))
    print('implied cost of capital %.4f%% against %.4f%%'
          % (W_IMPLIED * 100, C['wacc_exp'] * 100))
    print('judgements %d, material %d, resolved upward %d, sign test p=%s, flag %s'
          % (res['judgements'], res['material'], res['resolved_upward'],
             'n/a' if res['sign_test_p'] is None else '%.2f' % res['sign_test_p'],
             res['flag']))
