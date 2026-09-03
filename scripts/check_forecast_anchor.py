#!/usr/bin/env python3
"""[R-ANCHOR-01] THE FORECAST IS ANCHORED ON THE LATEST REVIEWED PERIOD, AND A
DECLINE AWAY FROM IT IS A CLAIM THAT NAMES ITS MECHANISM.

    python3 scripts/check_forecast_anchor.py [--prune]

WHY THIS EXISTS, AND IT IS NOT A NEW IDEA -- THAT IS THE POINT.

The rule has been in both governing documents since 07-Aug-2026, in these words:
"A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE: anchor every unit
rate on the most recent reviewed period and let it DRIFT only where a named
structural mechanism has a MEASURED like-for-like direction in the company's own
period pair; hold everything else flat INCLUDING observed improvements."

It was correct, it was registered, and on 3 September 2026 THREE separate studies
in one market violated it in three different costumes, all in the same direction:

  AMOC   forecast gross margin 9.494% falling to 8.764% against a base year of
         9.653% and a FILED first half of 12.428% -- an implied second half of
         6.56%, half what the company had just reported. The mechanism was an
         unsourced real cost drift: pound conversion legs escalated at the full
         domestic inflation ladder while realised price grew only at the currency
         differential, +2.7 points a year for ever. The study's OWN registered
         principle said the spread was held flat in real terms.

  EGCH   forecast gross margin 45.66% falling to 33.02% on flat revenue, from a
         typed array carrying the dollar export price down 17% over five years
         against a dollar-linked input held flat -- source layer "Constructed",
         no marginal cash cost quoted, no institution publishing it.

  ARCC   the reverse shape and worth naming: the forecast opened at 39.03%
         against a filed peak of 39.25% and rose to 40.4%. Nothing was wrong with
         it, and nothing in the study TOLD A READER the forecast sat at the top
         of the company's own filed range. A gate that only catches declines
         would have said nothing here either, so the record is printed for every
         study whether or not it fires.

Every one of these lowered the value. None was declared. Each was found by a
person reading the numbers, which is the thing [R-ENF-01] says not to rely on:
"a rule that can be checked must be checked from outside the thing it governs,
and a self-attested boolean is never a check." The lesson [L-048] was registered
after the first occurrence and bound nothing, which is [R-MACRO-01]'s general
lesson exactly -- a lesson that binds nothing is advice, and advice loses to the
next deadline. So the rule becomes arithmetic.

WHAT IT CHECKS. A study commits a `forecast_anchor` record: the latest reviewed
period with its date and its rate, the first forecast year's rate, and -- where
the forecast sits BELOW the latest reviewed period by more than the tolerance --
a named mechanism from a CLOSED list, the disclosure establishing it, and the
LIKE-FOR-LIKE measurement in the company's own period pair that gives it a
direction. An open list would let any study opt out by inventing a reason, and
"the rate looked wrong" is not a mechanism. The same closed-list discipline as
[R-COC-01 AMENDED]'s cost-of-debt exception, and for the same reason.

THE MEASUREMENT MUST AGREE WITH THE MECHANISM. This is the clause that does the
work: a study may declare "input costs rising faster than realised price" and
supply a period pair in which cost per unit of revenue FELL. AMOC did exactly
that -- 93.146% to 87.572% across its five filed periods while the model asserted
a rise. So the gate compares the declared direction against the measured one and
refuses when they disagree. A mechanism contradicted by the company's own filings
is not a mechanism; it is the assumption wearing one.

WHAT IT DOES NOT DO. It does not require a forecast to equal the latest period --
mean reversion is a real thing, and a refiner's spread is volatile. It requires
the claim to be NAMED, SOURCED and MEASURED, which is all any of these gates ever
requires. Nor does it fire on a forecast ABOVE the latest period: that direction
is audited by [R-GAP-01]'s two-sided trigger and by the sign test, and a gate
firing in both directions here would collide with them.

Ratcheted [R-ENF-02], population-anchored [R-ENF-04], negative-controlled by
scripts/check_forecast_anchor_negative_control.py.
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'anchor_outstanding.json')

# How far below the latest reviewed period a forecast may open with no mechanism.
#
# THE FIRST DRAFT OF THIS GATE GOT THIS WRONG AND ITS OWN NEGATIVE CONTROL CAUGHT
# IT, WHICH IS THE ARGUMENT FOR NEGATIVE CONTROLS. It used an ABSOLUTE 0.002 with
# the stated reason "the rounding width of a rate quoted to two decimal places,
# doubled". That reason supports 0.0001, not 0.002 -- a number chosen and then
# given a justification, which is the free-parameter offence in better clothes and
# which the promotion rule forbids. It then fired on ARCC, whose forecast opens
# 0.22 points below its filed peak for no reason but the arithmetic of the build.
#
# The answer was not to widen it. [R-COC-01]'s lesson: when a check fires on work
# that is right, widening is a free parameter and moving the work corrupts what is
# measured; the third option is to establish the check is pointed at the WRONG
# MEASUREMENT and re-point it.
#
# It is RELATIVE, and the threshold is one this house already uses rather than a
# new one minted here: 5% is the materiality line the protocol applies to a
# contested judgement, and a driver moved less than 5% relative does not clear it.
# On the three cases that provoked this rule it separates them by wide margins:
# AMOC 9.494% against a filed 12.428% is 23.6% relatively below; EGCH 33.02%
# against 45.66% is 27.7% below; ARCC 39.03% against 39.25% is 0.56% below. There
# is no threshold between 5% and 20% that would classify any of them differently,
# which is the test of whether a cutoff is doing work or merely existing.
#
# A small ABSOLUTE floor rides with it so a genuinely tiny rate -- a refiner on a
# half-point spread -- does not trip on arithmetic noise.
TOL_REL = 0.05
TOL_ABS = 0.0005

# The closed list. Adding to it is a rule amendment, not a study's decision.
MECHANISMS = {
    'input_cost_outpacing_price':
        'a disclosed input whose price rises faster than the realised output price',
    'contracted_price_step_down':
        'a contracted or administered price that steps down on a disclosed date',
    'capacity_commissioning_drag':
        'a disclosed programme whose commissioning costs land before its revenue',
    'subsidy_or_levy_withdrawal':
        'a disclosed subsidy, levy or quota change with a stated effective date',
    'mix_shift_to_lower_margin':
        'a disclosed shift in product or geographic mix, measured in the filings',
    'one_off_in_the_latest_period':
        'a non-recurring item inside the latest reviewed period, quantified from '
        'the filing that discloses it',
}

REQUIRED = ('latest_reviewed_period', 'latest_reviewed_date', 'latest_reviewed_rate',
            'first_forecast_rate', 'rate_name')


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def check(record, ticker='?'):
    """Raise unless the study's forecast anchor obeys [R-ANCHOR-01]."""
    fails = []
    r = record or {}
    for k in REQUIRED:
        if r.get(k) in (None, ''):
            fails.append('the forecast anchor names no %s. The rule is that a near-term '
                         'reviewed actual outranks a stale full-year rate, and a record '
                         'that does not say what the latest reviewed actual WAS cannot be '
                         'held to it.' % k)
    if fails:
        raise AssertionError('ANCHOR FAIL -- %s:\n  - %s' % (ticker, '\n  - '.join(fails)))

    latest = _f(r['latest_reviewed_rate'])
    first = _f(r['first_forecast_rate'])
    if latest is None or first is None:
        raise AssertionError('ANCHOR FAIL -- %s:\n  - the rates do not parse as numbers' % ticker)

    gap = first - latest
    r['_gap'] = gap
    tol = max(TOL_ABS, TOL_REL * abs(latest))
    r['_tol'] = tol
    if gap >= -tol:
        return r                                   # at or inside the tolerance

    mech = r.get('mechanism') or {}
    name = str(mech.get('name') or '').strip()
    if not name:
        fails.append(
            'the forecast opens at %.4f against a latest reviewed %.4f -- %.2f points '
            'below it, %.1f%% RELATIVE -- and names no mechanism. A forecast that '
            'reverses what the company has just filed is a claim about the world and it '
            'is named, sourced and measured, or it is not made.'
            % (first, latest, -100 * gap, -100 * gap / abs(latest)))
    elif name not in MECHANISMS:
        fails.append(
            'mechanism %r is not on the closed list (%s). An open list lets any study opt '
            'out by inventing a reason, and adding to the list is a rule amendment.'
            % (name, ', '.join(sorted(MECHANISMS))))
    else:
        if not str(mech.get('disclosure') or '').strip():
            fails.append('mechanism %r carries no disclosure. It must come from the '
                         'filings, not be asserted.' % name)
        # THE CLAUSE THAT DOES THE WORK
        pair = mech.get('like_for_like') or {}
        need = ('period_a', 'period_b', 'value_a', 'value_b', 'measures')
        missing = [k for k in need if pair.get(k) in (None, '')]
        if missing:
            fails.append(
                'mechanism %r supplies no like-for-like measurement (%s). The rule permits '
                'a drift only where the mechanism has a MEASURED direction in the '
                "company's own period pair, and a mechanism with no measurement is the "
                'assumption wearing one.' % (name, ', '.join(missing)))
        else:
            a, b = _f(pair['value_a']), _f(pair['value_b'])
            if a is None or b is None:
                fails.append('the like-for-like values do not parse as numbers')
            else:
                # the declared direction must be the measured one: a mechanism that
                # makes the forecast rate FALL must show the driver moving the way
                # that would make it fall, in the company's own filings
                measured_worse = b > a if pair.get('higher_is_worse', True) else b < a
                if not measured_worse:
                    fails.append(
                        'mechanism %r says the forecast rate falls, and the like-for-like '
                        'measurement in the company\'s own filings runs the OTHER WAY: %s '
                        'moved from %.6f (%s) to %.6f (%s). A mechanism contradicted by '
                        'the filings is not a mechanism. This is AMOC\'s own case: cost '
                        'per unit of revenue fell from 93.146%% to 87.572%% across five '
                        'filed periods while the model asserted it rises 2.7 points a '
                        'year for ever.'
                        % (name, pair['measures'], a, pair['period_a'], b, pair['period_b']))
    if fails:
        raise AssertionError('ANCHOR FAIL -- %s:\n  - %s' % (ticker, '\n  - '.join(fails)))
    return r


def load_outstanding():
    d = json.load(open(OUTSTANDING, encoding='utf-8'))
    return d, set(d.get('outstanding', []))


def main(argv):
    prune = '--prune' in argv
    d, known = load_outstanding()
    dirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))

    # [R-ENF-04]: the population is anchored somewhere else and a run that examined
    # nothing FAILS rather than reporting clean
    if not dirs:
        print('FAIL - examined zero studies. An empty result is not a clean result.')
        return 1
    on_disk = {os.path.basename(p)[:-6].upper() for p in dirs}
    ghosts = sorted(known - on_disk)
    if ghosts:
        print('FAIL - the outstanding list names studies that are not on disk: %s'
              % ', '.join(ghosts))
        return 1

    ok, bad, missing, conform = [], [], [], []
    for sdir in dirs:
        tk = os.path.basename(sdir)[:-6].upper()
        p = os.path.join(sdir, 'study_numbers.json')
        if not os.path.exists(p):
            missing.append((tk, 'no committed numbers file')); continue
        try:
            doc = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            bad.append((tk, 'study_numbers.json will not parse: %s' % e)); continue
        rec = doc.get('forecast_anchor')
        if rec is None:
            missing.append((tk, 'carries no forecast_anchor record')); continue
        try:
            rec = check(rec, tk)
        except AssertionError as e:
            bad.append((tk, str(e).replace('\n', '  '))); continue
        ok.append((tk, rec))
        conform.append(tk)

    print('[R-ANCHOR-01] the forecast anchor, checked from outside the study\n')
    print('  examined %d study directories\n' % len(dirs))
    if ok:
        print('  CONFORMING (%d) - forecast rate against the latest reviewed period:' % len(ok))
        for tk, rec in ok:
            g = rec['_gap']
            flag = ('' if g >= -rec['_tol']
                    else '  (mechanism: %s)' % rec['mechanism']['name'])
            print('   %-12s %-26s latest %7.4f  forecast %7.4f  %+7.2fpp%s'
                  % (tk, str(rec['rate_name'])[:26], rec['latest_reviewed_rate'],
                     rec['first_forecast_rate'], 100 * g, flag))
        print()
    newbad = [(t, w) for t, w in bad + missing if t not in known]
    if missing:
        print('  NO RECORD (%d):' % len(missing))
        for tk, why in missing:
            print('   %-12s %s%s' % (tk, why, '' if tk not in known else '   [outstanding]'))
        print()
    if newbad:
        print('FAIL - %d new violation(s):' % len(newbad))
        for tk, why in newbad:
            print('   %-12s %s' % (tk, why))
        print('\nA forecast that reverses what the company has just filed is a claim about '
              'the world. Name the mechanism, source it, and measure its direction in the '
              "company's own filings - or anchor on the latest reviewed period.")
        return 1
    if prune:
        keep = sorted(known - set(conform))
        d['outstanding'] = keep
        json.dump(d, open(OUTSTANDING, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print('pruned - now %d entries' % len(keep))
    print('OK - no new violations.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
