#!/usr/bin/env python3
"""GBCO walk-forward — the corrections, under BOTH clauses of [R-FCAL-01].

CLAUSE ONE  the bias holds its sign AT EVERY CUT THE DATA ADMITS
            [R-FCAL-01 AMENDED 07-09-2026], every boundary leaving at least five
            cells on each side. A driver too thin to cut is UNTESTABLE, never
            counted stable, because an absence of contrary evidence is not
            evidence [R-ENF-04].
CLAUSE TWO  the correction is consistent with how that driver class is built
            across the market's book. It is not a formality: a finance-cost
            correction once passed clause one convincingly and failed this one,
            and that failure is what exposed a specification error underneath.

WHY THIS FILE EXISTS AT ALL. This run scored 225 cells across seven drivers on
7 September 2026 and then stopped: it produced errors.json and scores.json and
never recorded a DECISION about any of them, so check_walkforward_actuation was
right to refuse it — a walk-forward that measures and never acts is a diary. The
step was missing, not the evidence.

THE ARITHMETIC IS NOT REIMPLEMENTED HERE. cuts_for() is imported from the shared
boundary module so this run is held to the same measurement every other run is
[R-ENF-03]; a checker or a caller that models a measurement is testing a
different measurement from the one that ships.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'valuation_calibration'))
import boundary_sensitivity as BSEN     # noqa: E402

HALF_STRENGTH = 0.5

AGGREGATES = ('gross_profit', 'operating_profit', 'net_profit')

# CLAUSE TWO, PER DRIVER, WRITTEN AGAINST THE BOOK RATHER THAN AGAINST THIS NAME.
CLAUSE_TWO = {
    'revenue': "Revenue is built bottom-up from volume and price on every name in "
               "this book, so a scalar applied to the revenue LINE would sit on "
               "top of drivers that are themselves corrected — the same error "
               "counted twice.",
    'gross_margin': "Margins are OUTPUTS of the cost build in this house and never "
                    "inputs. Correcting a margin directly reverses that and would "
                    "make the cost side unfalsifiable.",
    'sga': "An overhead line carried per unit of revenue across the book, so a "
           "correction here is admissible in principle — and this is the ONLY "
           "driver in this run that passes clause one, stable at all six "
           "admissible cuts. It is still not promoted, and the reason is a gap "
           "in the run rather than a verdict on the driver: scores.json carries "
           "no block-bootstrap standard error, so the pre-registered decision "
           "rule cannot establish robustness and declines. UNESTABLISHED IS NOT "
           "REFUTED, and recording it as though the evidence were against the "
           "driver would misstate what was measured [R-ENF-04]. The CI is owed "
           "to this run.",
    'finance_cost': "THE TRAP THIS RULE NAMES BY NAME. Interest comes from the "
                    "borrowings that actually bear it, and GB Corp carries a "
                    "captive lender whose funding sits beside trade balances that "
                    "pay nothing. A correction on this line is refused until the "
                    "denominator is established from the facility note, because a "
                    "bias measured on the wrong denominator looks exactly like "
                    "evidence.",
    'gross_profit': "An AGGREGATE. Corrections are applied to drivers and "
                    "aggregates are REBUILT from them; correcting an aggregate "
                    "directly is forbidden.",
    'operating_profit': "An AGGREGATE, and the same refusal.",
    'net_profit': "An AGGREGATE, and the same refusal.",
}


def cells_by_driver():
    rows = json.load(open(os.path.join(HERE, 'errors.json'), encoding='utf-8'))
    by = collections.defaultdict(list)
    for c in rows:
        e = c.get('err')
        y = c.get('origin')
        if e is None or y is None:
            continue
        by[c['driver']].append((int(y), float(e)))
    return by


def expanding(cells):
    """Expanding window only: at each origin the correction may use ONLY errors
    that had already resolved by then. Half strength by default."""
    out, years = {}, sorted({y for y, _ in cells})
    for o in years:
        prior = [e for y, e in cells if y < o]
        out[o] = dict(prior_cells=len(prior),
                      adjustment_log=(-HALF_STRENGTH * sum(prior) / len(prior))
                      if prior else 0.0)
    return out


if __name__ == '__main__':
    by = cells_by_driver()
    if not by:
        raise SystemExit('errors.json yielded no scored cells — an empty result '
                         'is not a clean result [R-ENF-04].')

    log = {"_rule": "[R-FCAL-01] expanding window only, half strength by default, "
                    "applied only where the bias holds its sign at EVERY cut the "
                    "data admits, and consistent with how the driver class is "
                    "built across the market's book.",
           "built": "2026-09-07",
           "half_strength": HALF_STRENGTH,
           "candidates": {}}

    print('%-20s %4s %8s %6s %6s  %s'
          % ('driver', 'n', 'bias', 'cuts', 'flips', 'verdict'))
    for k in sorted(by):
        v = by[k]
        bias = sum(e for _, e in v) / len(v)
        cuts, flipped = BSEN.cuts_for(v)
        aggregate = k in AGGREGATES
        clause_one = bool(cuts) and not flipped
        if aggregate:
            verdict = 'REFUSED — an aggregate; corrections apply to drivers'
            disposition = 'refused'
        elif not cuts:
            verdict = ('WATCH FLAG — clause one UNTESTABLE at %d cell(s), no '
                       'boundary leaves %d each side' % (len(v), BSEN.MIN_SIDE))
            disposition = 'watch_flag'
        elif flipped:
            verdict = ('WATCH FLAG — the sign flips at %d of %d admissible cuts'
                       % (len(flipped), len(cuts)))
            disposition = 'watch_flag'
        else:
            verdict = ('clause one PASSES at %d of %d cuts; clause two decides'
                       % (len(cuts), len(cuts)))
            disposition = 'watch_flag'
        log['candidates'][k] = dict(
            n=len(v), bias=bias, admissible_cuts=len(cuts), flips=len(flipped),
            clause_one=clause_one,
            clause_one_reason=("no boundary leaves %d cells on both sides — "
                               "UNTESTABLE, never counted stable" % BSEN.MIN_SIDE)
            if not cuts else ("stable at every admissible cut" if not flipped
                              else "the sign depends on where the line is drawn"),
            clause_two=CLAUSE_TWO.get(k, ''),
            by_origin=expanding(v),
            promoted=False,
            disposition=disposition,
            verdict=verdict)
        print('%-20s %4d %+8.4f %6d %6d  %s'
              % (k, len(v), bias, len(cuts), len(flipped), verdict[:46]))

    # THE SHARED GATES READ A RUN'S DECISION THROUGH A NAMED PER-RUN ADAPTER
    # [R-FCAL-01 AMENDED]: five records carried five shapes and a reader that
    # guesses silently finds nothing. Both keys are EMPTY here rather than
    # absent — silence and "none adopted" are the same file to a reader and
    # different facts about the work.
    log['adopted'] = []
    log['promoted'] = []
    n_watch = sum(1 for c in log['candidates'].values()
                  if c['disposition'] == 'watch_flag')
    n_ref = sum(1 for c in log['candidates'].values()
                if c['disposition'] == 'refused')
    log['summary'] = ("%d candidates measured, 0 promoted, %d recorded as watch "
                      "flags, %d refused as aggregates. Nothing from this run "
                      "enters the live drivers."
                      % (len(log['candidates']), n_watch, n_ref))
    log['guidance_ledger'] = {
        "entries": [],
        "note": "EMPTY. GB Corp publishes quarterly earnings releases with an "
                "operating review but no forward numeric guidance in any of the "
                "releases this run parsed, so the guidance-is-scored-never-"
                "consumed clause has nothing to score and no driver here can "
                "have inherited a management lean."}
    json.dump(log, open(os.path.join(HERE, 'corrections_log.json'), 'w'),
              indent=1)
    print('\n' + log['summary'])
