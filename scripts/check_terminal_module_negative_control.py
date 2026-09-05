#!/usr/bin/env python3
"""[R-ENF-01] — engine/terminal_value.py's own REFUSALS, negative-controlled.

WHY THIS EXISTS SEPARATELY FROM scripts/check_terminal_floor_negative_control.py. That one
controls the GATE: it plants mutations in a sandboxed copy of the repository and asserts the
gate goes red. It says nothing about the MODULE, whose enforcement is a different species —
the module refuses at BUILD TIME, inside a study, before any number is committed, so no gate
ever sees the study it stopped.

The module carried nine refusal conditions and not one of them had ever been seen to fire.
A check nobody has watched fail is not evidence, and that applies to a raise exactly as it
applies to a gate. Every condition below is reinjected and asserted to refuse; every clean
case is asserted to BUILD, because a module that refused everything would also pass a file
that only tested refusals.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'engine'))
import terminal_value as TV                                          # noqa: E402

# A terminal that builds. Every case below is this, with one thing changed.
GOOD = dict(nopat=1000.0, wacc=0.18, inflation=0.07, real_growth=0.0,
            dna_book=200.0, useful_life_years=22.0,
            maintenance_basis='book_dna_escalated', working_capital=300.0)

REFUSE = [
    ('a rate that is not a rate', dict(wacc=1.4)),
    ('growth at or above the terminal rate', dict(real_growth=0.20)),
    ('a maintenance basis outside the closed list', dict(maintenance_basis='whatever_works')),
    ('the disclosed-life basis with no replacement-cost base',
     dict(maintenance_basis='disclosed_life', ic_replacement=None,
          useful_life_source='note 5')),
    ('a life this desk chose — no source on it',
     dict(maintenance_basis='disclosed_life', ic_replacement=8000.0,
          useful_life_source='')),
    ('real growth stated with no incremental capital behind it',
     dict(real_growth=0.02, incremental_capital_per_unit_growth=None)),
    ('a terminal that consumes cash for ever', dict(dna_book=20.0, nopat=100.0,
                                                    working_capital=9000.0)),
    # THE FIRST DRAFT OF THIS CASE DID NOT LAND AND THE CONTROL CAUGHT IT. It set a huge
    # book charge on a one-year life, reasoning that the add-back would exceed profit —
    # but on this basis maintenance is the charge ESCALATED, so it always exceeds the
    # add-back and free cash flow can never rise above NOPAT. The condition is only
    # reachable where maintenance is supplied DIRECTLY and is small against the add-back,
    # which is exactly the shape a study could construct by mistake.
    ('a terminal distributing more than it earns',
     dict(maintenance_basis='disclosed_capex', maintenance_capex=1.0,
          dna_book=900.0, working_capital=0.0)),
    # --- the age branch, re-pointed 4 September 2026 --------------------------------
    ('an age supplied with no source', dict(average_age_years=4.45)),
    ('an age that is not an age', dict(average_age_years=-1.0,
                                       average_age_source='note 6')),
    ('an absurd age', dict(average_age_years=500.0, average_age_source='note 6')),
    ('neither a measured age nor a life to halve', dict(useful_life_years=None)),
]

# THE CONVENTION ITSELF, asserted rather than described. `nopat` is the LAST EXPLICIT
# YEAR's figure and the module grows the free cash flow once; six of eight callers read the
# old field comment ("terminal-year NOPAT") the other way and overstated their terminals by
# exactly (1+g). A comment cannot stop that recurring. This can.
def convention():
    g_real, pi = 0.0, 0.02
    a = TV.build(TV.TerminalInputs(**GOOD))
    grown = dict(GOOD)
    f = (1.0 + pi) * (1.0 + g_real)
    for k in ('nopat', 'dna_book', 'working_capital'):
        grown[k] = GOOD[k] * f
    b = TV.build(TV.TerminalInputs(**grown))
    ratio = b.tv / a.tv
    ok = abs(ratio - f) < 1e-9
    print('%s     handing in figures already grown by (1+g) overstates the terminal by '
          'exactly (1+g): %.6f vs %.6f' % ('PASS' if ok else 'FAIL', ratio, f))
    return 0 if ok else 1


CLEAN = [
    ('the base case', {}),
    ('a MEASURED age, sourced — the re-pointed branch',
     dict(average_age_years=4.45,
          average_age_source="note 6, accumulated depreciation over the year's own charge")),
    ('an age of zero: a brand-new base costs its book cost to replace',
     dict(average_age_years=0.0, average_age_source='note 6')),
    ('the disclosed-life basis, properly supplied',
     dict(maintenance_basis='disclosed_life', ic_replacement=6000.0,
          useful_life_source='note 5-2 depreciation rates')),
    ('the company\'s own stated maintenance capex',
     dict(maintenance_basis='disclosed_capex', maintenance_capex=400.0)),
    ('real growth WITH the capital it needs',
     dict(real_growth=0.01, incremental_capital_per_unit_growth=5000.0)),
]


def main():
    bad = 0
    print('[R-ENF-01] engine/terminal_value.py — the module\'s own refusals\n')
    for i, (name, change) in enumerate(REFUSE, 1):
        kw = dict(GOOD); kw.update(change)
        try:
            TV.build(TV.TerminalInputs(**kw))
            print('FAIL %2d. %-56s BUILT — it should have refused' % (i, name)); bad += 1
        except TV.TerminalRefused:
            print('PASS %2d. %-56s refused' % (i, name))
        except TypeError as e:
            print('FAIL %2d. %-56s the case is malformed: %s' % (i, name, e)); bad += 1

    print()
    for j, (name, change) in enumerate(CLEAN, len(REFUSE) + 1):
        kw = dict(GOOD); kw.update(change)
        try:
            t = TV.build(TV.TerminalInputs(**kw))
            print('PASS %2d. %-56s built (tv %,.0f)'.replace(',.0f', '.0f')
                  % (j, name, t.tv))
        except TV.TerminalRefused as e:
            print('FAIL %2d. %-56s REFUSED a clean case: %s' % (j, name, e)); bad += 1

    # THE FALLBACK MUST NOT HAVE MOVED. The re-pointing is additive: a record that supplies
    # no age gets half the life exactly as before, so no committed answer moves.
    t = TV.build(TV.TerminalInputs(**GOOD))
    want = GOOD['dna_book'] * (1.0 + GOOD['inflation']) ** (GOOD['useful_life_years'] / 2.0)
    same = abs(t.maintenance - want) < 1e-9
    print('\n%s     the half-of-life fallback still reproduces the pre-amendment charge '
          'exactly' % ('PASS' if same else 'FAIL'))
    if not same:
        bad += 1
    if t.record.get('maintenance_age_basis') != 'half_of_life':
        print('FAIL     the record does not say WHICH age it used'); bad += 1
    else:
        print('PASS     and the record says which age it used, so an assumption is '
              'distinguishable from a measurement')

    print()
    bad += convention()

    n = len(REFUSE) + len(CLEAN) + 3
    print('\n%d/%d cases behaved as specified' % (n - bad, n))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
