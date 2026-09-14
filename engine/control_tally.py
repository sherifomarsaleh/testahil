#!/usr/bin/env python3
"""A NEGATIVE CONTROL'S OWN REPORT IS A CLAIM, AND FIVE OF THEM WERE PROVING NOTHING.

    from engine.control_tally import Tally

WHY THIS EXISTS. Every negative control in this repository ends by printing what it did,
and six of them printed a DECLARED CONSTANT rather than a COUNT:

    print("cases run: %d (declared %d)" % (CASES, CASES))

That line is true whatever ran. Delete half the cases and it still reports a full house;
delete all of them and it reports a full house. It was found by reading the output of one
of them — "cases run: 15 (declared 15)" sitting above "OK — 6 red conditions fire, 4 clean
conditions do not", a tally that had been hand-typed once and never moved again, so the
two lines disagreed about how many cases existed and neither was measured.

THIS IS THE FOURTH AND FIFTH TIME THIS PROJECT HAS CAUGHT A CONTROL PASSING ON SOMETHING
IT DID NOT DO — a fixture that never injected its condition, a mutation blinded by a regex
that matched nothing, a splice scan sampling every tenth offset, a control that deleted
three cases and reported three of three clean. The repeated shape is not carelessness: A
CONTROL IS THE ONE PIECE OF CODE NOBODY WRITES A CONTROL FOR, so a defect in it is
invisible by construction and looks exactly like evidence.

THE INSTRUMENT IS SHARED RATHER THAN COPIED, for the reason [R-ENF-01 EXTENDED] gives of
the prose-figure and sweep-register instruments: porting one correct implementation into
six files produces six hand-maintained tallies with six different holes, which is the same
lesson those extensions were adopted on.

WHAT IT REFUSES, none of it a threshold:

  * a case count that MOVED from the declaration — fewer OR more, because a control that
    silently gained a case is as unreadable as one that lost one;
  * a run with NO cases at all [R-ENF-04], which is the state a broken harness reaches
    and the state that reads most like success;
  * a tally line HAND-TYPED rather than derived — there is no way to type one here.

USAGE

    T = Tally(declared=16)
    ...
    T.case("1 the defect exactly as it shipped", expect_red=True)   # per case
    ...
    return T.report(failures)
"""
from __future__ import annotations

from typing import List, Sequence, Tuple


class Tally:
    """What a control ACTUALLY ran, counted rather than asserted."""

    def __init__(self, declared: int, subject: str = "the gate"):
        self.declared = int(declared)
        self.subject = subject
        self.ran: List[Tuple[str, bool]] = []

    def case(self, name: str, expect_red: bool) -> None:
        self.ran.append((str(name), bool(expect_red)))

    @property
    def red(self) -> int:
        return sum(1 for _, e in self.ran if e)

    @property
    def clean(self) -> int:
        return len(self.ran) - self.red

    def report(self, failures: Sequence[Tuple[str, str]]) -> int:
        """Print the tally and return the exit code. 0 only if everything held."""
        n = len(self.ran)
        print("cases run: %d (declared %d) — %d red, %d clean"
              % (n, self.declared, self.red, self.clean))
        if n == 0:
            print("FAIL — the control ran ZERO cases. An empty result is not a clean "
                  "result [R-ENF-04], and a harness that stopped building fixtures reads "
                  "exactly like a gate with nothing to catch.")
            return 1
        if n != self.declared:
            print("FAIL — the case count MOVED: %d ran, %d declared. A control that "
                  "quietly loses a case reports fewer-of-fewer and reads as clean; one "
                  "that quietly gains a case is reporting on work nobody declared."
                  % (n, self.declared))
            return 1
        if failures:
            for name, why in failures:
                print("  FAIL  %s\n        %s" % (name, why))
            print("\nFAIL — %s does not behave as the rule says." % self.subject)
            return 1
        print("OK — %d red conditions fire, %d clean conditions do not."
              % (self.red, self.clean))
        return 0
