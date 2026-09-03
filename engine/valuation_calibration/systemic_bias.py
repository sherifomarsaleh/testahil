"""PROJECTED VERSUS ACTUAL — the systemic biases, line by line.

WHY THIS EXISTS, in the principal's own words: "learn from the projected financials vs. the
actual financials to determine systemic biases". Every fundamental walk-forward [R-FCAL-01]
rebuilds the driver model at a past origin, projects it forward, and scores each line
against what the company actually reported. That is a large body of projected-versus-actual
evidence about this house's own forecasting, and it had never been read ACROSS names.

`driver_bias_census.py` pools the AGGREGATED bias by axis. This module goes to the CELLS —
one row per (origin, horizon, line, projected, actual) — and pools them onto a COMMON LINE
TAXONOMY so a bias on cost of sales at PHDC is comparable with one at TMGH. Mapping is BY
HAND, in the table below, because a regex on driver names would silently merge a unit cost
with a total cost and manufacture the finding.

WHAT IT CAN AND CANNOT SEE, stated first because the limit is the most important output.
Only TWO of the five completed runs commit their per-cell projected-versus-actual pairs.
AMOC, ARCC and EGCH commit the aggregated statistics — bias, MAE, over-share, bootstrap
interval, by driver and by horizon and by era — and NOT the cells those were computed from.
So the cell-level analysis rests on PHDC and TMGH, and the other three enter only through
their aggregates.

THAT IS [R-FCAL-01 AMENDED]'S OWN LESSON ARRIVING A SECOND TIME: what a process commits
decides what can ever be asked of it later, and nobody notices the missing field until the
question arrives. The amendment was written about VALUATION INPUTS — cash, debt, capex,
share count — after a scorer tried to rebuild a fair value at a past origin and found the
inputs were not there. This is the identical shape one layer along: the runs recorded the
SCORES and not the OBSERVATIONS, so a question about which LINES are biased can be answered
on two names and not five. The cells cost nothing to keep; they were simply not asked for.

Registered rather than worked around. It binds forward, not backward, per [R-ENF-02]: the
three runs get their cell export at their next run.

HOW TO READ THE OUTPUT. Bias is mean log(projected / actual), so POSITIVE means the forecast
was TOO HIGH. Three things are reported for every line and none is a substitute for the
others:

  * the pooled bias, with the share of cells over-forecast — direction and consistency;
  * the HORIZON SLOPE, because a level error is flat across horizons and a RATE error grows.
    These have completely different remedies and the same appearance in a pooled mean;
  * ERA STABILITY, because [R-FCAL-01] holds that a bias changing sign between eras is not a
    bias and must be reported rather than corrected for. Egypt's own record splits hard —
    CPI averaged 8.5% over 2018-21 and 22.5% over 2022-25 — so a pooled figure on Egyptian
    names measures an era at least as much as a method.

WHAT THE FIRST RUN FOUND, AND IT INVERTS THE FRAMING THIS REASSESSMENT BEGAN WITH.

On 867 committed cells the single most robust bias in this house's record is that PROFIT IS
FORECAST AT ABOUT TWICE WHAT THE COMPANY REPORTS: pooled +0.8084 in log terms, x2.24 of
actual, too high in 89% of cells, on BOTH names (PHDC +1.107 with 60 of 62 cells too high;
TMGH +0.264 with 25 of 34). It is FLAT across horizons — +0.859 at one year, +0.719 at five
— so it is a LEVEL error rather than a rate error, and it does NOT change sign between
eras, which is the one test that separates a bias from a regime. Gross profit is the same
shape, +0.2303, x1.26 of actual, also flat and also sign-stable.

THIS HOUSE IS NOT PESSIMISTIC ABOUT PROFIT. IT IS OPTIMISTIC ABOUT PROFIT BY ROUGHLY A
FACTOR OF TWO, AND ITS VALUATIONS NEVERTHELESS COME OUT BELOW THE MARKET. Those two facts
together locate the pessimism, and they locate it away from the forecasts: it lives in the
VALUATION MACHINERY, which is exactly where [R-TERM-01] found a terminal charging g x IC for
ever on an asset life that was the reciprocal of the inflation rate.

The mechanism behind the profit optimism is legible in the lines it is built from, and each
step is small:

  REVENUE         -0.2243   x0.80 of actual, and it COMPOUNDS: -0.023 at h1 to -0.348 at h5
  COST_OF_SALES   -0.1309   x0.88 of actual — under-forecast, but LESS than revenue is
  GROSS_PROFIT    +0.2303   so the forecast MARGIN is too wide, by construction
  FINANCE_COST    -1.1465   x0.32 of actual, 61 of 62 cells too low, worsening with horizon
  PROFIT          +0.8084   x2.24 of actual

Revenue growth is under-forecast, which is a RATE error; cost is under-forecast by less, so
the margin comes out too wide; and finance cost is forecast at a third of what is actually
incurred. The profit line inherits all three.

THE FINANCE-COST FIGURE IS MOSTLY ERA AND IS NOT CORRECTED FOR. It compounds savagely
(-0.513 at one year to -2.010 at five) and 61 of 62 cells run the same way, which looks like
the strongest finding here — and its sign CHANGES across eras (E1 +0.032, E2 -0.951, E3
-1.361). Egyptian policy rates went from single digits to 27% inside the window these
origins span, and no point-in-time model could have seen it. [R-FCAL-01] is explicit: a bias
that changes sign between eras is not a bias, the average of two opposite regimes was true
in neither, and it is REPORTED rather than corrected for. Eight of the ten lines here change
sign across eras. TWO DO NOT — profit and gross profit — and those two are the finding.

THE LIMIT, STATED PLAINLY: both names carrying cells are Egyptian real-estate developers.
The profit-optimism finding is robust across those two, across horizons and across eras, and
it is NOT yet a claim about this book. Whether it generalises is what the three runs that
commit no cells would have told us, and what the next ones will.

NOTHING HERE IS A CORRECTION. It is a measurement, and [R-FCAL-01]'s promotion rules decide
what may ever be done with it: expanding window only, half strength by default, applied only
where the bias holds its sign across eras, and consistent with how the driver class is built
across the whole book — the second clause being the one that has already caught a
convincing-looking correction that was arithmetic rather than evidence.
"""
from __future__ import annotations

import json
import math
import os
import statistics as st
from glob import glob

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------------------------------
# THE COMMON LINE TAXONOMY. Assigned by hand from each line's own meaning. A line this
# table does not name is EXCLUDED AND REPORTED, never bucketed [R-ENF-04].
# ---------------------------------------------------------------------------------------
LINES = {
    'REVENUE':        {'is.revenue', 'revenue', 'total_revenue', 'dev_revenue',
                       'recurring_revenue', 'net_sales', 'new_sales'},
    'VOLUME':         {'units_sold', 'units_delivered', 'volume_t', 'urea_t',
                       'vol_local', 'vol_export', 'vol_total'},
    'PRICE':          {'asp', 'price_local', 'price_export'},
    'COST_OF_SALES':  {'is.cogs', 'cogs', 'cost_of_sales', 'dev_cost', 'recurring_cost',
                       'raw', 'raw_materials', 'supporting_materials', 'other_cos',
                       'transport', 'overhead'},
    'UNIT_COST':      {'raw_per_t', 'transport_per_t', 'overhead_per_t'},
    'GROSS_PROFIT':   {'is.gross_profit', 'gross_profit'},
    'OPEX':           {'is.sga', 'sga', 'ga', 'admin', 'selling', 'marketing',
                       'other_expenses', 'services'},
    'DEPRECIATION':   {'is.admin_depr', 'da', 'dna', 'depreciation', 'mfg_dep', 'amort'},
    'FINANCE_COST':   {'is.finance_cost', 'finance_cost', 'finance_costs', 'debit_interest'},
    'FINANCE_INCOME': {'interest_income', 'credit_interest', 'investment_income',
                       'investment_revenues', 'other_income', 'other_revenues'},
    'TAX':            {'tax', 'tax_current', 'income_tax'},
    'PROFIT':         {'is.npbt', 'is.npat_mi', 'net_profit', 'npat', 'pbt', 'pat',
                       'operating_profit', 'majority', 'net'},
    'PROVISION':      {'provisions', 'claims_provision'},
    'BALANCE':        {'ppe', 'development_properties', 'customer_advances', 'backlog'},
}
_OF = {v: k for k, vs in LINES.items() for v in vs}

# The cell files, and the field names each uses. Two shapes, both read.
CELL_FILES = {
    'PHDC': ('error_cells.json', 'as_known', 'field', 'h', 'proj', 'actual', 'e'),
    'TMGH': ('error_cells.json', None, 'driver', 'horizon', 'projected', 'actual',
             'log_error'),
}
# Only the AS-KNOWN setting is pooled: a perfect-foresight run answers a different question
# (how much of the miss was macro) and mixing the two would double-count every cell.
ASKNOWN = {'asknown', 'as_known', 'known', ''}


def cells():
    """Every committed projected-versus-actual cell, on the common taxonomy."""
    out, unmapped, missing = [], set(), []
    for d in sorted(glob(os.path.join(REPO, 'engine', '*_walkforward'))):
        tk = os.path.basename(d).replace('_walkforward', '').upper()
        spec = CELL_FILES.get(tk)
        if spec is None:
            if os.path.exists(os.path.join(d, 'scores.json')):
                missing.append(tk)
            continue
        fn, key, ffield, fh, fproj, fact, ferr = spec
        j = json.load(open(os.path.join(d, fn)))
        rows = j[key] if key else j
        for r in rows:
            setting = str(r.get('setting', '')).lower()
            if setting and setting not in ASKNOWN:
                continue
            fld = r.get(ffield)
            line = _OF.get(fld)
            if line is None:
                unmapped.add(f'{tk}:{fld}')
                continue
            p, a = r.get(fproj), r.get(fact)
            e = r.get(ferr)
            if e is None and p and a and p > 0 and a > 0:
                e = math.log(p / a)
            if e is None:
                continue
            out.append(dict(ticker=tk, line=line, field=fld, h=int(r.get(fh) or 0),
                            origin=r.get('origin'), era=r.get('era', ''),
                            projected=p, actual=a, e=float(e)))
    return out, sorted(unmapped), missing


def _slope(pts):
    if len(pts) < 3:
        return None
    hs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mh, my = st.mean(hs), st.mean(ys)
    den = sum((h - mh) ** 2 for h in hs)
    return None if den == 0 else sum((h - mh) * (y - my) for h, y in pts) / den


def report():
    rows, unmapped, missing = cells()
    print('PROJECTED VERSUS ACTUAL — SYSTEMIC BIAS BY LINE  [R-FCAL-01]')
    print('   bias = mean log(projected / actual): POSITIVE = the forecast was TOO HIGH')
    print('   %d committed cells from %s'
          % (len(rows), ', '.join(sorted({r['ticker'] for r in rows}))))
    if missing:
        print('\n   COMMITS NO CELLS, so it enters only through its aggregates: %s'
              % ', '.join(missing))
        print('   [R-FCAL-01 AMENDED] arriving a second time — what a process commits')
        print('   decides what can ever be asked of it later. Registered, binds forward.')

    print('\n  %-16s%5s%11s%11s%9s%11s%9s' % ('line', 'n', 'bias', 'median',
                                              'too high', 'slope/yr', 'x at h5'))
    print('  ' + '-' * 74)
    order = sorted({r['line'] for r in rows},
                   key=lambda L: -abs(st.mean([r['e'] for r in rows if r['line'] == L])))
    for L in order:
        a = [r for r in rows if r['line'] == L]
        b = [r['e'] for r in a]
        hi = sum(1 for x in b if x > 0)
        pts = [(h, st.mean([r['e'] for r in a if r['h'] == h]))
               for h in sorted({r['h'] for r in a}) if h]
        sl = _slope(pts)
        h1 = next((y for h, y in pts if h == 1), None)
        h5 = next((y for h, y in pts if h == 5), None)
        mult = (h5 / h1) if (h1 and h5 and h1 != 0) else None
        print('  %-16s%5d%+11.4f%+11.4f%8.0f%%%s%s'
              % (L, len(b), st.mean(b), st.median(b), 100.0 * hi / len(b),
                 ('%+11.4f' % sl) if sl is not None else ('%11s' % '—'),
                 ('%9.2f' % mult) if mult is not None else ('%9s' % '—')))

    print('\n  THE TWO QUESTIONS THAT MATTER, and they have different remedies:')
    lvl = [L for L in order
           if (_slope([(h, st.mean([r['e'] for r in rows if r['line'] == L and r['h'] == h]))
                       for h in sorted({r['h'] for r in rows if r['line'] == L}) if h]) or 0)
           and abs(_slope([(h, st.mean([r['e'] for r in rows if r['line'] == L and r['h'] == h]))
                           for h in sorted({r['h'] for r in rows if r['line'] == L}) if h])) > 0.05]
    print('    RATE errors (slope beyond 5 log points a year, so they COMPOUND): %s'
          % (', '.join(lvl) or 'none'))
    print('      -> the remedy is in the growth PATH. Re-anchoring a base year cannot fix a')
    print('         rate error: it moves today\'s number and leaves next year identical.')
    print('    LEVEL errors (flat across horizons): %s'
          % (', '.join(L for L in order if L not in lvl) or 'none'))
    print('      -> the remedy is the base year [R-ANCHOR-01], and only that.')

    print('\n  ERA STABILITY — [R-FCAL-01]: a bias that CHANGES SIGN between eras is not a')
    print('  bias, and the average of two opposite regimes was true in neither.')
    print('  %-16s%9s%s' % ('line', 'eras', '   bias in each'))
    print('  ' + '-' * 74)
    for L in order:
        a = [r for r in rows if r['line'] == L and r['era']]
        eras = sorted({r['era'] for r in a})
        if len(eras) < 2:
            continue
        per = [(e, st.mean([r['e'] for r in a if r['era'] == e])) for e in eras]
        flip = len({1 if v > 0 else -1 for _, v in per}) > 1
        print('  %-16s%9d   %s%s' % (L, len(eras),
                                     '  '.join('%s %+.3f' % (e.split()[0], v) for e, v in per),
                                     '   SIGN CHANGES — report, never correct' if flip else ''))

    if unmapped:
        print('\n  EXCLUDED, not bucketed — a line this taxonomy does not name is reported')
        print('  rather than guessed at [R-ENF-04]: %s' % ', '.join(unmapped))
    return rows


if __name__ == '__main__':
    report()
