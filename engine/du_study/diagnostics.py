"""DU — the study's own audit of its ANSWER: the reverse read and the sign test [R-ENF-05].

ADDED 08-09-2026, critique response finding S14. This study published a fair value 46% above
the market and never once solved what the market must believe under its own drivers. An
outside auditor did it for us, in its Section E, and landed on a perfectly ordinary number.
That is the wrong way round: a study that will not state its own disagreement in the market's
units is asking a reader to take the conclusion on trust.

THE READ IS KEPT OUT OF THE MODEL, STRUCTURALLY. It lives here and in diagnostics.json, never
in study_numbers.json, and no builder reads it back: a quantity solved from a price and then
used in the valuation is the reverse-engineered rate the cost-of-capital procedure prohibits
outright, arriving through a side door.

Run AFTER compute.py.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import terminal_value as TERMVAL                                        # noqa: E402

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
W, DCF, F = D['wacc'], D['dcf'], D['fcst']
TR = D['terminal_record']['inputs']
SH = D['inputs']['shares_mn']['value']
SPOT = D['spot']
LEASE, NETCASH, INV = DCF['lease'], DCF['net_cash'], DCF['investees']
DIV, DAYS = DCF['div_between'], DCF['anchor_days']
G, GLIDE, FCFF = DCF['g'], W['glide_frac'], F['fcff']


def _value_at_beta(b):
    """The whole model re-read at one beta, on the study's own construction."""
    ke = W['rf_star'] + b * W['erp_market_basis']
    we_ = W['we_exp'] * ke + W['wd_exp'] * W['kd_at']
    wt_ = ((1 - 0.05) * ((W['rf_path'][-1] - W['sov_spread_market_observed'])
                         + b * W['erp_market_basis'])
           + 0.05 * W['kd_term_at'])
    dfs, cc = [], 1.0
    for fr in GLIDE:
        cc /= (1 + (we_ - (we_ - wt_) * fr))
        dfs.append(cc)
    t = TERMVAL.build(TERMVAL.TerminalInputs(
        nopat=F['nopat'][-1], wacc=wt_, inflation=TR['inflation'],
        real_growth=TR['real_growth'], dna_book=TR['dna_book'],
        useful_life_years=TR['useful_life_years'],
        useful_life_source=TR['useful_life_source'],
        maintenance_basis='book_dna_escalated', working_capital=F['nwc'][-1],
        incremental_capital_per_unit_growth=TR['incremental_capital_per_unit_growth']))
    ev = sum(f * x for f, x in zip(FCFF, dfs)) + t.tv * dfs[-1]
    return (ev - LEASE + NETCASH + INV) / SH * ((1 + ke) ** (DAYS / 365)) - DIV


def _solve(fn, target, lo, hi, n=90):
    for _ in range(n):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
    return lo


implied_beta = _solve(_value_at_beta, SPOT, 0.20, 4.0)
implied_ke = W['rf_star'] + implied_beta * W['erp_market_basis']

# ---- the contested judgements, both framings, and the sign test -------------------
# [R-ENF-05]: any single contested choice is defensible; what is not is a study resolving
# every one of them the same way and never noticing. Each row is a judgement worth more
# than 5% of the central, with BOTH framings' values and the side this study took.
CENTRAL = D['central']
J = [
    dict(name='The required return — capitalise at the measured cost of capital, or hold '
              "du's own current EBITDA multiple into perpetuity",
         adopted=CENTRAL, alternative=DCF['ps_mkt_term'], side='higher',
         why='the cash-flow lens is the central and the market-multiple terminal is '
             'published beside it at its own value, never averaged'),
    dict(name='Post-2029 fiscal regime — the extended 38%+9% construction, or reversion to '
              'the pre-2024 15%-of-revenue + 30%-of-profit one',
         adopted=CENTRAL, alternative=DCF['ps_framing_b'], side='higher',
         why='du disclosed the 2027-2029 extension itself on 24-Jul-2026; reversion after '
             '2029 is a named tail, priced, not a coin-flip'),
    dict(name='Risk-free tenor — the Jan-2031 T-bond at 4.48%, or the Feb-2033 sukuk tap '
              'at 4.13%',
         adopted=CENTRAL, alternative=DCF['ps_rf_long'], side='lower',
         why='the most recent primary print on the longest liquid tenor; the sukuk is a '
             'different instrument type and its debut print is five months stale'),
    dict(name='Blended ARPU — held roughly flat, or eroding at the per-leg rate the '
              'postpaid-mix decomposition implies once the tailwind exhausts',
         adopted=CENTRAL, alternative=D['sens']['grid_drift'][0], side='higher',
         why='the disclosed path is flat-to-slightly-up; the erosion case is priced as the '
             'largest operating downside in the study rather than assumed away'),
    dict(name='Terminal maintenance — replacement cost over the derived 16.70-year life, or '
              'over the 22.97-year second reading of the same notes',
         adopted=CENTRAL, alternative=D['sens']['grid_life'][-1], side='lower',
         why='the gross-cost-over-charge route validates against the 10.1-year lease term '
             'note 7 discloses directly; the accumulated-depreciation route does not'),
    dict(name='Beta — the own-stock Dimson-corrected regression, or a sector-implied 0.80 '
              'prior',
         adopted=CENTRAL, alternative=D['sens']['grid_beta'][-1], side='higher',
         why='SIGCM takes the own-stock regression wherever it clears the usability gate; '
             'the prior is priced, not adopted'),
    dict(name='Terminal real growth — zero, stated, and charged for the capital it would '
              'consume, or the +0.49% real the retired typed 2.5% nominal implied',
         adopted=CENTRAL, alternative=D['sens']['grid_wacc_g'][2][2], side='lower',
         why='a real rate nobody has quantified is written down as zero rather than left '
             'as the residue of typing a nominal'),
]
for j in J:
    j['move_pct'] = j['alternative'] / CENTRAL - 1.0
    j['material'] = abs(j['move_pct']) > 0.05

_mat = [j for j in J if j['material']]
_hi = sum(1 for j in _mat if j['side'] == 'higher')
_lo = len(_mat) - _hi


def _binom_two_sided(k, n):
    from math import comb
    if n == 0:
        return 1.0
    p = [comb(n, i) / 2 ** n for i in range(n + 1)]
    return min(1.0, sum(v for i, v in enumerate(p) if v <= p[k] + 1e-15))


OUT = dict(
    published_central=CENTRAL,
    published_spot=SPOT,
    spot=SPOT,
    spot_date=D['inputs']['spot']['date'],
    implied=dict(
        quantity='equity beta (and therefore the required return), holding every other '
                 'driver at its published value',
        value=implied_beta,
        study_value=W['beta']['beta'],
        solved_on='this study\'s own model: the same five-year FCFF path, the same '
                  'sanctioned terminal on the same derived asset life, the same bridge and '
                  'the same anchor roll, with only the beta moved until the answer meets '
                  'the traded price',
        implied_cost_of_equity=implied_ke,
        study_cost_of_equity=W['ke_exp'],
        reading='At AED %.2f the market is paying for an equity beta of %.2f — a required '
                'return of %.2f%% — against the %.2f the regression measures and the %.2f%% '
                'it produces. That is not an absurd number for a single-market, '
                'single-licence operator, and saying so is the point: the disagreement is '
                'about the price of risk, not about the cash flows. The regression\'s own '
                '90%% interval tops out at %.2f, so the price sits OUTSIDE it — but only '
                'just, and a reader who thinks a licensed duopoly deserves a market beta '
                'has a coherent position this study does not hold.'
                % (SPOT, implied_beta, implied_ke * 100, W['beta']['beta'],
                   W['ke_exp'] * 100, W['beta']['ci90'][1]),
    ),
    sign_test=dict(
        judgements=J,
        material_count=len(_mat),
        resolved_higher=_hi,
        resolved_lower=_lo,
        p_two_sided=_binom_two_sided(_hi, len(_mat)),
        reading='%d judgements worth more than 5%% of the central, %d resolved toward a '
                'higher value and %d toward a lower one, two-sided binomial p = %.2f. '
                'FLAGGED, never failed: a company can genuinely deserve a consistent read, '
                'and a gate that failed on one would push a study to resolve judgements '
                'inconsistently to stay green.'
                % (len(_mat), _hi, _lo, _binom_two_sided(_hi, len(_mat))),
    ),
)

def build():
    """The reverse read and the sign test, as a dict.

    EXPOSED AS A FUNCTION ON PURPOSE. The study document has to be able to PRINT what the
    price believes -- that is the whole point of [R-ENF-05] -- while nothing may read a
    price-solved quantity back into the valuation. A builder importing this function gets
    the numbers for a sentence; there is one implementation and no second solver, and
    study_numbers.json, which every builder reads, carries none of it."""
    return OUT


# ---- the contested-judgement record, in the shared instrument's own shape --------
# The same seven judgements, keyed the way assert_contested_judgements() reads them, so the
# repo-level job can run the sign test from OUTSIDE this study rather than trusting the
# sentence the study prints about itself.
CONTESTED = dict(
    ticker='DU', published_central=CENTRAL, published_spot=SPOT,
    judgements=[dict(name=j['name'],
                     adopted='this study\'s construction',
                     alternative='the other framing, computed and published beside it',
                     value_adopted=j['adopted'], value_alternative=j['alternative'],
                     why=j['why']) for j in J],
    note='every judgement worth more than 5% of the central, both framings computed on the '
         'same model and never averaged into one number')

if __name__ == '__main__':
    json.dump(CONTESTED, open(os.path.join(HERE, 'contested_judgements.json'), 'w'),
              indent=1, default=float)
    json.dump(OUT, open(os.path.join(HERE, 'diagnostics.json'), 'w'), indent=1, default=float)
    print('REVERSE READ  implied beta %.4f (Ke %.4f%%) against the measured %.4f (Ke %.4f%%) '
          'at spot %.2f' % (implied_beta, implied_ke * 100, W['beta']['beta'],
                            W['ke_exp'] * 100, SPOT))
    print('SIGN TEST     %d material judgements, %d higher / %d lower, p = %.2f'
          % (len(_mat), _hi, _lo, OUT['sign_test']['p_two_sided']))
    for j in J:
        print('   %-6s %+7.1f%%  %s' % ('MAT' if j['material'] else '-',
                                        100 * j['move_pct'], j['name'][:78]))
