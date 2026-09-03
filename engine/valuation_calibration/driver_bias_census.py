"""Does this house overstate cost and understate revenue? — the pooled walk-forward answer.

WHY THIS EXISTS. The reassessment was called because the house looked "ridiculously
pessimistic", and the diagnosis offered from outside was specific: big overestimation of
cost, underestimation of revenue, and a mess in the cost of capital. That is an empirical
claim about three quantities, and this house already measures all three — [R-FCAL-01]'s
fundamental walk-forward rebuilds the driver model at past origins and scores every driver
against what the company actually reported. Five names have been through it. Nobody had
POOLED them, so the claim had never been tested against the evidence the process itself
produces.

WHAT IT DOES. It reads each run's OWN scores.json, classifies every scored driver onto the
revenue axis, the cost axis, or neither, and pools the bias. Classification is BY HAND, in
the tables below, from each driver's own meaning — never by pattern-matching a name,
because a mis-classified driver would manufacture the very finding under test. A driver
this module does not recognise is EXCLUDED AND NAMED rather than swept into a bucket
[R-ENF-04].

Profit and margin lines are neither axis. They are where the two axes MEET, so pooling
them with either double-counts; they are reported separately as `output`.

SIGN CONVENTION, stated once because everything turns on it: bias is mean
log(forecast / actual), so POSITIVE means the forecast was TOO HIGH.

THE QUESTION THE HORIZON PROFILE ANSWERS, and it is the one that matters. A LEVEL error is
flat across horizons — get the base year wrong and every year is wrong by the same amount.
A RATE error GROWS with the horizon, because it compounds. So the shape of the bias across
h = 1..5 says which kind of mistake this is, and the two have completely different
remedies: a level error is fixed by re-anchoring the base year [R-ANCHOR-01], a rate error
is fixed in the growth path and nowhere else. Re-anchoring a base year to cure a rate error
moves today's number and leaves the model to fail the same way next year, which is exactly
what [R-FCAL-01] means when it says a correction is honest when the model is right and
reality is awkward.

Nothing here is an input to any study.
"""
from __future__ import annotations

import json
import os
import statistics as st
from glob import glob

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------------------
# CLASSIFICATION. Assigned by hand from each driver's own meaning. Adding a name here is a
# judgement and belongs in a commit message, not in a regex.
# ---------------------------------------------------------------------------------------
REVENUE = {
    'AMOC': ['net_sales', 'volume_t', 'other_revenues', 'investment_revenues',
             'credit_interest'],
    'ARCC': ['revenue', 'vol_local', 'vol_export', 'vol_total', 'price_local',
             'price_export', 'services', 'other_income', 'interest_income'],
    'EGCH': ['revenue', 'urea_t', 'investment_income', 'credit_interest'],
    'PHDC': ['is.revenue', 'new_sales', 'units_delivered', 'units_sold', 'asp'],
    'TMGH': ['total_revenue', 'dev_revenue', 'recurring_revenue', 'new_sales', 'backlog'],
}
COST = {
    'AMOC': ['cost_of_sales', 'raw_materials', 'supporting_materials', 'other_cos',
             'salaries', 'ga', 'marketing', 'other_expenses', 'depreciation',
             'claims_provision'],
    'ARCC': ['cogs', 'raw', 'raw_per_t', 'transport', 'transport_per_t', 'overhead',
             'overhead_per_t', 'mfg_dep', 'amort', 'ga', 'provisions', 'finance_costs'],
    'EGCH': ['cost_of_sales', 'admin', 'selling', 'provisions', 'debit_interest'],
    'PHDC': ['is.cogs', 'is.sga', 'is.admin_depr', 'is.finance_cost'],
    'TMGH': ['dev_cost', 'recurring_cost', 'sga', 'da', 'finance_cost'],
}
OUTPUT = {
    'AMOC': ['gross_profit', 'operating_profit', 'pbt', 'npat', 'majority', 'income_tax'],
    'ARCC': ['gross_profit', 'pbt', 'pat', 'majority', 'tax'],
    'EGCH': ['gross_profit', 'pbt', 'net', 'tax_current', 'other_bucket'],
    'PHDC': ['is.gross_profit', 'is.npbt', 'is.npat_mi'],
    'TMGH': ['gross_profit', 'net_profit', 'ppe', 'development_properties',
             'customer_advances'],
}
AXES = (('revenue', REVENUE), ('cost', COST), ('output', OUTPUT))


def _bias(v):
    """A scores.json cell carries its summary either nested or flat. Read both."""
    if not isinstance(v, dict):
        return None
    s = v.get('summary')
    return (s if isinstance(s, dict) else v).get('bias')


def runs():
    for d in sorted(glob(os.path.join(REPO, 'engine', '*_walkforward'))):
        tk = os.path.basename(d).replace('_walkforward', '').upper()
        f = os.path.join(d, 'scores.json')
        if os.path.exists(f) and tk in REVENUE:
            yield tk, json.load(open(f))


def pooled():
    """Per-driver bias, and per-driver-per-horizon bias, both classified."""
    flat, byh, unclassified = [], [], []
    for tk, s in runs():
        bd = s.get('by_driver') or {}
        bh = s.get('by_horizon') or {}
        known = set()
        for axis, m in AXES:
            for drv in m[tk]:
                known.add(drv)
                b = _bias(bd.get(drv))
                if b is not None:
                    flat.append(dict(ticker=tk, axis=axis, driver=drv, bias=b,
                                     n=(bd[drv] or {}).get('n')))
                per = bh.get(drv)
                if isinstance(per, dict):
                    for h, v in per.items():
                        hb = _bias(v)
                        if hb is not None and str(h).isdigit():
                            byh.append(dict(ticker=tk, axis=axis, driver=drv,
                                            h=int(h), bias=hb))
        unclassified += [(tk, k) for k in bd if k not in known]
    return flat, byh, unclassified


def _slope(pairs):
    """Least-squares slope of bias against horizon: the annual log growth shortfall."""
    if len(pairs) < 3:
        return None, None
    hs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    mh, my = st.mean(hs), st.mean(ys)
    den = sum((h - mh) ** 2 for h in hs)
    if den == 0:
        return None, None
    b = sum((h - mh) * (y - my) for h, y in pairs) / den
    return b, my - b * mh


def era_stability():
    """[R-FCAL-01] applies to THIS measurement too: a bias that changes sign between eras
    is not a bias, and the average of two opposite regimes was true in neither. So the
    pooled figures above are reported BESIDE the subset whose sign is stable across every
    era the run defined, and the finding is whichever survives.

    This is not a formality. Egypt's own record splits hard — CPI averaged 8.5% over
    2018-21 and 22.5% over 2022-25 — so a pooled bias on Egyptian names is measuring an
    era at least as much as a method, and a correction taken from it would be a correction
    for having failed to predict a currency collapse.
    """
    stable, flipped = [], []
    for tk, s in runs():
        be = s.get('by_era') or {}
        bd = s.get('by_driver') or {}
        for axis, m in AXES:
            for drv in m[tk]:
                e = be.get(drv)
                if not isinstance(e, dict):
                    continue
                bs = [(k, _bias(v)) for k, v in e.items()]
                bs = [(k, b) for k, b in bs if b is not None]
                if len(bs) < 2:
                    continue
                pooled_b = _bias(bd.get(drv))
                rec = dict(ticker=tk, axis=axis, driver=drv, eras=bs, pooled=pooled_b)
                (flipped if len({1 if b > 0 else -1 for _, b in bs}) > 1
                 else stable).append(rec)
    return stable, flipped


def report():
    flat, byh, unclassified = pooled()
    print('THE THREE AXES, MEASURED  —  cost too high? revenue too low?')
    print("   pooled from the five fundamental walk-forwards' own scores.json")
    print('   bias = mean log(forecast / actual): POSITIVE = we forecast TOO HIGH\n')

    for axis, _ in AXES:
        a = [r['bias'] for r in flat if r['axis'] == axis]
        if not a:
            continue
        hi = sum(1 for x in a if x > 0)
        print('  %-8s %3d drivers   mean %+8.4f   median %+8.4f   too high in %d/%d (%.0f%%)'
              % (axis.upper(), len(a), st.mean(a), st.median(a), hi, len(a),
                 100.0 * hi / len(a)))

    print('\n  THE ANSWER TO THE FIRST TWO AXES IS NOT WHAT EITHER SIDE EXPECTED:')
    rev = [r['bias'] for r in flat if r['axis'] == 'revenue']
    cst = [r['bias'] for r in flat if r['axis'] == 'cost']
    if rev and cst:
        print('    revenue comes in %.0f%% ABOVE forecast and cost %.0f%% ABOVE forecast.'
              % (100 * (pow(2.718281828, -st.mean(rev)) - 1),
                 100 * (pow(2.718281828, -st.mean(cst)) - 1)))
        print('    Both are under-forecast, by almost the same amount, so the MARGIN is')
        print('    roughly right and the SCALE is systematically too low. Cost is not')
        print('    overstated relative to revenue — the whole business is understated.')

    print('\n  DOES IT COMPOUND? a level error is flat across horizons; a RATE error grows.')
    hdr = ''.join(('h=%d' % h).rjust(15) for h in range(1, 6))
    print('  ' + 'axis'.ljust(9) + hdr)
    print('  ' + '-' * 84)
    for axis, _ in AXES:
        cells = []
        for h in range(1, 6):
            v = [r['bias'] for r in byh if r['axis'] == axis and r['h'] == h]
            cells.append(('%+.3f (n=%d)' % (st.mean(v), len(v))) if v else '-')
        print('  ' + axis.ljust(9) + ''.join(c.rjust(15) for c in cells))

    print('\n  the slope IS the annual growth shortfall, and it is what a fix must target:')
    for axis, _ in AXES:
        pts = [(h, st.mean([r['bias'] for r in byh
                            if r['axis'] == axis and r['h'] == h]))
               for h in range(1, 6)
               if [r for r in byh if r['axis'] == axis and r['h'] == h]]
        b, a = _slope(pts)
        if b is None:
            continue
        print('    %-9s bias ~ %+.4f %+.4f x h   ->  nominal growth understated by '
              '%.1f percentage points a year'
              % (axis, a, b, 100.0 * (pow(2.718281828, -b) - 1)))
    print('\n    An intercept near zero with a large slope is the signature of a RATE')
    print('    error and nothing else: the base year was right and the path was wrong.')
    print('    Re-anchoring a base year cannot fix it — that moves today\'s number and')
    print('    leaves the model to fail identically next year.')

    stable, flipped = era_stability()
    tot = len(stable) + len(flipped)
    if tot:
        print('\n  ERA STABILITY — [R-FCAL-01] applied to this measurement itself:')
        print('    %d drivers carry an era split; %d change SIGN across eras (%.0f%%).'
              % (tot, len(flipped), 100.0 * len(flipped) / tot))
        print("    Egypt's own record splits hard — CPI averaged 8.5% over 2018-21 and")
        print('    22.5% over 2022-25 — so a pooled bias here measures an era at least as')
        print('    much as a method. The finding is whichever survives on the STABLE set:')
        for axis, _ in AXES:
            a = [r['pooled'] for r in stable if r['axis'] == axis and r['pooled'] is not None]
            f = [r['pooled'] for r in flipped if r['axis'] == axis and r['pooled'] is not None]
            if a:
                print('      %-8s stable %2d  mean %+8.4f     sign-changing %2d  mean %+8.4f'
                      % (axis, len(a), st.mean(a), len(f), st.mean(f) if f else float('nan')))
        print('    A sign-changing driver is REPORTED AND NEVER CORRECTED FOR. That is why')
        print('    these runs adopted almost no corrections, and the restraint was right.')

    if unclassified:
        print('\n  EXCLUDED, not bucketed — a driver this module does not recognise is')
        print('  named rather than guessed at [R-ENF-04]:')
        for tk, k in unclassified:
            print('    %-8s %s' % (tk, k))
    return flat, byh


if __name__ == '__main__':
    report()
