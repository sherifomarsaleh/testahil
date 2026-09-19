#!/usr/bin/env python3
"""Negative control for the flat-nominal claim check [R-ENF-01].

Twelve conditions, five red and SEVEN CLEAN, and the clean half decides this one: 361
quantities in this book are held flat and 351 of them say nothing false about it. A
control that only proved the denial fires would say nothing about the studies that get
it right -- and TWO STUDIES ALREADY DO, in their own words, which is why their passages
are the fixtures rather than invented ones.

It writes nothing: every fixture is a string handed to engine/flat_nominal_claim.py.
EVERY MUTATION ASSERTS THAT IT LANDED.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import flat_nominal_claim as FN                                    # noqa: E402

CASES = 12


def main() -> int:
    ok, bad = 0, []

    def case(n, what, want_red, text, landed):
        nonlocal ok
        if not landed(text):
            bad.append('%d %s — THE FIXTURE DID NOT LAND' % (n, what))
            return
        red = bool(FN.passages(text))
        if red == want_red:
            ok += 1
        else:
            bad.append('%d %s — wanted %s, got %s'
                       % (n, what, 'RED' if want_red else 'quiet',
                          'RED' if red else 'quiet'))

    says = lambda s: (lambda t: s in t)                            # noqa: E731

    # ---- RED: the passages as the two studies ship them
    case(1, "AMOC's crude convention as delivered", True,
         "the slate is priced off the same barrel, with crude held FLAT in dollars — "
         "no forecast of it is defensible — and the pound depreciates at the inflation "
         "differential.", says('no forecast of it is defensible'))
    case(2, "EGCH's export price as delivered", True,
         "Held FLAT in nominal dollars at US$530 a tonne, the level at which the last "
         "contract settled. No forecast of a traded commodity price is defensible, "
         "which is the convention this house applies elsewhere.",
         says('US$530'))
    case(3, "EGCH's 'not contested' framing, which also removes it from the sign test",
         True,
         "Holding a traded commodity price flat rather than forecasting it is settled "
         "house convention and is not contested. WHICH price is the contested part.",
         says('rather than forecasting it'))
    case(4, 'a study claiming it expresses no view', True,
         "Revenue per tonne is held flat across the window; the model expresses no view "
         "on the direction of the price.", says('expresses no view'))
    case(5, 'the denial phrased as the absence of a forecast', True,
         "The day rate is kept flat, which is the absence of a forecast rather than a "
         "forecast of decline.", says('the absence of a forecast'))

    # ---- CLEAN: everything the book does correctly
    case(6, 'a study that NAMES the real decline, as GBCO ships it', False,
         "EGP 3,664.2mn a year, flat in nominal terms, which is a REAL DECLINE across "
         "the window and is stated as one rather than left implied.",
         says('REAL DECLINE'))
    case(7, "ADNOCDRILL's own diagnostic naming the same thing", False,
         "holding earnings flat in NOMINAL terms while discounting at a NOMINAL rate is "
         "a real-terms decline and is priced as one.",
         says('flat in NOMINAL terms'))
    case(8, 'held flat AND escalated at US inflation — the view-free choice', False,
         "The dollar price is held flat in REAL terms, escalated at US inflation, which "
         "is the choice with no forecast in it.", says('flat in REAL terms'))
    case(9, 'held flat with NO claim about it at all — out of scope', False,
         "Headcount is held flat across the forecast window at 4,120.",
         says('held flat'))
    case(10, 'a denial with nothing held flat near it', False,
          "No forecast of the political settlement is defensible, so the study prices "
          "both outcomes and publishes the disagreement.",
          says('No forecast of the political settlement'))
    case(11, 'the word defensible in an unrelated sentence beside a flat path', False,
          "Working capital is held flat as a share of revenue. Reading the disclosure "
          "the way its own primary source does is a defensible treatment.",
          lambda t: 'held flat' in t and 'defensible' in t)
    case(12, 'text with neither', False,
          "Revenue grows at the house nominal ladder in every forecast year.",
          lambda t: 'flat' not in t)

    print('flat nominal claim negative control — %s %d/%d'
          % ('PASS' if not bad else 'FAILED', ok, CASES))
    for b in bad:
        print('  - ' + b)
    if ok + len(bad) != CASES:
        print('  - CASE COUNT: %d ran against a declared %d' % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
