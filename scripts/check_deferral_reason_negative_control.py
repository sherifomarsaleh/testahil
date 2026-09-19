#!/usr/bin/env python3
"""Negative control for the deferral-reason check [R-REBUILD-01 CLAUSE TWO].

Thirteen conditions, six red and SEVEN CLEAN. The clean half is the half this turns
on: a passage that EXPLAINS the promotion guard, quotes it as an analogy, or records
that this very misreading was corrected is ordinary and correct, and a gate that could
not tell those from a false reason would push builders to stop explaining things. The
first draft fired on engine/gbco_study/rebuild_levers.py, whose docstring opens by
explaining [R-REBUILD-01] BY the guard -- the rule's own reasoning, correctly stated,
in the ledger that rule created -- and it was re-pointed rather than widened
[R-COC-01].

THE RED HALF IS THE BOOK'S OWN TEXT AS IT STOOD THIS MORNING, quoted verbatim from the
four passages corrected today, so the control reproduces a defect that really shipped
rather than one invented for it.

It writes nothing: every fixture is a string handed to engine/deferral_reason.py.
EVERY MUTATION ASSERTS THAT IT LANDED.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'engine'))

import deferral_reason as DR                                        # noqa: E402

CASES = 13


def main() -> int:
    ok, bad = 0, []

    def case(n, what, want_red, text, landed):
        nonlocal ok
        if not landed(text):
            bad.append('%d %s — THE FIXTURE DID NOT LAND' % (n, what))
            return
        found = DR.passages(text)
        red = bool(found)
        if red == want_red:
            ok += 1
        else:
            bad.append('%d %s — wanted %s, got %s%s'
                       % (n, what, 'RED' if want_red else 'quiet',
                          'RED' if red else 'quiet',
                          (': ' + found[0][1][:60]) if found else ''))

    says = lambda s: (lambda t: s in t)                              # noqa: E731

    # ---- RED: the four passages as they stood this morning, verbatim
    case(1, "AMOC's forecast-anchor comment as it stood", True,
         "So the honest state is: this forecast opens 22% relatively below the latest "
         "reviewed period and CANNOT name a mechanism the filings support. The reason "
         "it is not simply re-anchored is [R-VCAL-01]'s one-lever-at-a-time guard -- "
         "the move is priced at +55% in the contested judgements.",
         says("one-lever-at-a-time guard"))
    case(2, "AMOC's anchor RATCHET entry as it stood", True,
         "It is not simply re-anchored because [R-VCAL-01]'s one-lever-at-a-time guard "
         "forbids it in this pass: the move is priced at +55% in AMOC's contested "
         "judgements and would carry the study from 12.3% below the price to 35.9% "
         "above it in one edition.",
         says("forbids it in this pass"))
    case(3, "FERTIGLOBE's two-levers comment as it stood", True,
         "Correcting it RAISES the value, as does the net-weights finding recorded in "
         "the bridge; two levers pointing the same way in one pass is what the "
         "promotion guard forbids, so both are named and neither is taken here.",
         says("neither is taken here"))
    case(4, "FERTIGLOBE's macro-record comment as it stood", True,
         "moving the number to meet the path would be a second lever in the same pass "
         "as the terminal rebuild, which the promotion guard forbids. It is named "
         "here, left to the cost-of-capital pass, and the study stays on the macro "
         "ratchet until then.",
         says("left to the cost-of-capital pass"))
    # ---- RED: constructed
    case(5, "a correction withheld on the guard, in a committed note", True,
         "The bridge deduction is understated by EGP 300mn. It is not applied because "
         "the one-lever-at-a-time guard forbids a second move in this pass.",
         says("not applied"))
    case(6, "the guard named by rule id alone beside a deferral", True,
         "This is deferred: [R-VCAL-01]'s guard means only one lever may move.",
         says("[R-VCAL-01]"))

    # ---- CLEAN: correct uses that must stay silent
    case(7, "GBCO's rebuild ledger docstring, which EXPLAINS the guard", False,
         "[R-VCAL-01]'s promotion guard is explicit about stacking: one lever at a "
         "time, in an order fixed in advance, and the running total looked at more "
         "than once. A REBUILD is the same shape and was governed by nothing until "
         "this rule.",
         says("is explicit about stacking"))
    case(8, "the clause's own statement of what the guard governs", False,
         "[R-VCAL-01]'s one-lever-at-a-time guard governs LEVERS PROMOTED FROM THE "
         "VALUATION CALIBRATION and does not govern corrections to defects, so a "
         "correction is not deferred on it.",
         says("does not govern"))
    case(9, "a record noting this very misreading was CORRECTED", False,
         "THE REASON THIS ENTRY GAVE WAS FALSE AND IS CORRECTED: it read 'not simply "
         "re-anchored because the one-lever-at-a-time guard forbids it'. The "
         "measurement is unchanged at +55%.",
         says("CORRECTED"))
    case(10, "the guard described with no deferral anywhere near it", False,
          "[R-VCAL-01]'s promotion guard stays symmetric: a positive bias is a finding "
          "exactly as a negative one is.",
          says("stays symmetric"))
    case(11, "a deferral recorded as a DECISION with its measurement, naming no rule",
          False,
          "The re-anchor is priced at +55% and is not taken in this pass: it belongs "
          "with the four other corrections that stack with it, which is a re-issue "
          "rather than a field.",
          says("is not taken in this pass"))
    case(12, "the guard named far away from an unrelated deferral", False,
          "[R-VCAL-01]'s promotion guard is symmetric." + (" " * 900)
          + "Separately, the workbook rebuild is deferred to the next edition.",
          lambda t: "promotion guard" in t and "deferred" in t)
    case(13, "text with no guard reference at all", False,
          "The correction is priced at +17.8% and is applied in this pass.",
          lambda t: "guard" not in t)

    print('deferral reason negative control — %s %d/%d'
          % ('PASS' if not bad else 'FAILED', ok, CASES))
    for b in bad:
        print('  - ' + b)
    if ok + len(bad) != CASES:
        print('  - CASE COUNT: %d ran against a declared %d' % (ok + len(bad), CASES))
        return 1
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
