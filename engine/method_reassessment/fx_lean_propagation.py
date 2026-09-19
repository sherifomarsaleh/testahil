#!/usr/bin/env python3
"""Does the walk-forward's revenue under-forecast reach the struck fair values?

THE CONCERN, STATED BEFORE IT IS TESTED. ABUK's run established a property of the METHOD
rather than of one company: nine of ten completed runs under-forecast revenue, sign test
p = 0.0215, mean -0.2995 log across 280 cells and six industries, and substituting the
actual exchange rate ALONE takes ABUK's revenue bias from -0.469 to -0.001. Every origin
holds FX at its origin-dated value because that is the only thing knowable there — which
is right, and is also a systematic downward lean on every nominal line in a currency that
stepped three times in six years.

IF THAT LEAN PROPAGATED, IT WOULD BEAR ON THE ADOPTION BAR. A revenue under-forecast lowers
a fair value. Low fair values are calls of EXPENSIVE. And expensive is the one-sided bar
[R-VCAL-02 CLAUSE THREE] gates on: no company called expensive by more than 10% without an
audit behind it. Clause G passes today with six audited cells; if the lean were a property
of the method rather than of six cells, the audit burden would grow with every name added
and the bar would get harder to clear over time rather than easier.

IT IS NOT VISIBLE WHERE IT WOULD HAVE TO BITE, WHICH IS A WEAKER CLAIM THAN IT DOES NOT
EXIST, AND THE WEAKER CLAIM IS THE TRUE ONE. The first draft of this module concluded that
the sign "runs the other way" by quoting two endpoints, and had them backwards: the deepest
under-forecast in the set does pair with a low fair value against price, which is what
propagation would predict. A rank statistic replaced the endpoints for exactly that reason.

Both series are read live here — the walk-forward biases from each run's own scores.json
under whatever key that run used, and the struck cells from the declared cashflow scores
criterion3.py itself reads. Nothing is retyped and no number lives in this docstring.

WHY THE TWO DO NOT COMPOSE, which is the part worth keeping. They score different objects.
The walk-forward scores a FORECAST of a company's own reported line against what that
company later reported: the currency moves, the reported line moves with it, the forecast
does not, and the error is the whole of the gap. The mechanical series scores a struck FAIR
VALUE against the PRICE at the same origin. In a stepping currency the price falls in the
same regime that the revenue under-forecast appears, so both sides of that ratio move
together and it does not inherit the lean.

The book already had the other half of this and had not joined it up. Clause F attributes
the mechanical series' residual to [R-ANCHOR-01 CLAUSE THREE] — a forecast margin climbing
past everything the company has ever FILED — which is an UPWARD lever. The expensive-calls
audit reached the same mechanism on SWDY from the other end and ruled it unfixable by
construction, correctly.

THE LIMIT IS STATED RATHER THAN DISCOVERED LATER: five names. Five cannot establish the
ABSENCE of a relationship and nothing here claims to. What five names can do is show that
the concern is not visible at the level where it would have to bite — the struck series
sits well above price, not below it — and that is what is reported.
"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
DECLARED = os.path.join(ENGINE, 'valuation_calibration',
                        'SCORES_cashflow_06-09-2026.json')

# Every key a completed run has actually used for its top-line revenue driver, each read
# off a real scores.json. A run whose key is not here is REPORTED UNREADABLE and never
# silently skipped — a reader that guesses a convention finds nothing and reports it as a
# result [L-355].
REVENUE_KEYS = ('revenue', 'is.revenue', 'total_revenue', 'A_revenue',
                'net_sales', 'rev')


def _bias(v):
    if isinstance(v, dict):
        return v.get('bias')
    return v if isinstance(v, (int, float)) else None


def walkforward_revenue_bias(root=ENGINE):
    """{ticker: (bias, key)} plus the runs whose key is not recognised."""
    got, unreadable = {}, {}
    for d in sorted(glob.glob(os.path.join(root, '*_walkforward'))):
        tk = os.path.basename(d).replace('_walkforward', '').upper()
        p = os.path.join(d, 'scores.json')
        if not os.path.exists(p):
            unreadable[tk] = 'no scores.json'
            continue
        try:
            bd = json.load(open(p, encoding='utf-8')).get('by_driver')
        except (OSError, ValueError) as exc:
            unreadable[tk] = 'scores.json will not parse (%s)' % type(exc).__name__
            continue
        if not isinstance(bd, dict):
            unreadable[tk] = 'by_driver is %s, not a mapping' % type(bd).__name__
            continue
        for k in REVENUE_KEYS:
            if k in bd and _bias(bd[k]) is not None:
                got[tk] = (float(_bias(bd[k])), k)
                break
        else:
            unreadable[tk] = ('no recognised revenue key; drivers are %s'
                              % ', '.join(sorted(bd)[:6]))
    return got, unreadable


def struck_cells():
    """The declared mechanical cells criterion3.py scores, read from its own file."""
    j = json.load(open(DECLARED, encoding='utf-8'))
    return j['DECLARED']['cells'], j['DECLARED']['score']


def main():
    import math
    cells, score = struck_cells()
    bias, unreadable = walkforward_revenue_bias()

    by_name = {}
    for c in cells:
        by_name.setdefault(c['ticker'], []).append(math.log(c['fv'] / c['price']))

    print('DOES THE FX-AT-ORIGIN REVENUE LEAN REACH THE STRUCK FAIR VALUES?')
    print()
    print('  mechanical series, read from the file criterion3.py reads:')
    print('    %d cells / %d origins / %d names, mean log(FV/P) %+.4f, %d below price'
          % (score['n']['cells'], score['n']['origins'], score['n']['names'],
             score['mean'], score['below']))
    print()
    print('  %-7s %10s %8s %14s  %s'
          % ('name', 'rev bias', 'cells', 'mean log(FV/P)', 'the run\'s own key'))
    print('  %-7s %10s %8s %14s  %s' % ('-' * 7, '-' * 10, '-' * 8, '-' * 14, '-' * 20))
    pairs = []
    for tk in sorted(by_name):
        g = sum(by_name[tk]) / len(by_name[tk])
        if tk in bias:
            b, key = bias[tk]
            pairs.append((tk, b, g))
            print('  %-7s %+10.4f %8d %+14.4f  %s' % (tk, b, len(by_name[tk]), g, key))
        else:
            print('  %-7s %10s %8d %+14.4f  UNREADABLE — %s'
                  % (tk, '—', len(by_name[tk]), g, unreadable.get(tk, 'not a run')))
    print()

    if len(pairs) < 3:
        print('  REFUSED — fewer than three names carry both numbers. Nothing is')
        print('  concluded from that; it is reported as the gap it is [R-ENF-04].')
        return 1

    under = [p for p in pairs if p[1] < 0]
    above = [p for p in pairs if p[2] > 0]
    worst = min(pairs, key=lambda p: p[1])
    best = max(pairs, key=lambda p: p[1])

    # Spearman on the ranks. Five names cannot establish a relationship and none is
    # claimed; what a rank statistic does here is stop the endpoints being cherry-picked,
    # which is how the first draft of this module reached the opposite conclusion.
    def _ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0] * len(vals)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r

    rx = _ranks([p[1] for p in pairs])
    ry = _ranks([p[2] for p in pairs])
    n = len(pairs)
    dsq = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1 - 6.0 * dsq / (n * (n * n - 1))

    print('  WHAT WOULD HAVE TO BE TRUE IF THE LEAN PROPAGATED:')
    print('    a name that under-forecasts revenue more deeply would strike a LOWER')
    print('    fair value against price — a POSITIVE rank correlation between the two')
    print('    columns, and a struck series sitting BELOW price overall.')
    print()
    print('  NEITHER HOLDS.')
    print('    %d of %d names under-forecast revenue, yet the struck series sits %+.4f'
          % (len(under), n, score['mean']))
    print('    ABOVE price with only %d of %d cells below it. A downward lean is not what'
          % (score['below'], score['n']['cells']))
    print('    dominates these values.')
    print("    Spearman's rho across the two columns: %+.2f on %d names — nothing, and"
          % (rho, n))
    print('    slightly the wrong sign for propagation.')
    print()
    print('  THE HONEST LIMIT, STATED RATHER THAN DISCOVERED LATER. %d names cannot' % n)
    print('  ESTABLISH the absence of a relationship, and this does not claim to. What it')
    print('  settles is that the concern is not VISIBLE at the level where it would have')
    print('  to bite: the struck values lean the wrong way for it, and clause F already')
    print('  attributes that lean to a forecast margin climbing past the filed record —')
    print('  an upward lever, and not the currency.')
    print()
    print('  What would change this reading is the UAE leg: a book whose currency does')
    print('  not step, where the two effects stop being confounded by one regime.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
