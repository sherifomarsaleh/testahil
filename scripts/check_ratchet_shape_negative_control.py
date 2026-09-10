#!/usr/bin/env python3
"""Negative control for [R-ENF-08]'s module — the one that decides what gets EXCUSED.

WHY THIS IS THE MOST SAFETY-CRITICAL CONTROL WRITTEN TODAY. Every other instrument here
decides whether something is WRONG. This one decides whether a wrong thing is ALLOWED, and
a bug in it fails silently in the worst direction: a real breach quietly excused reads
exactly like a book in good order. It is also the newest code in the repository and the
only module with no gate of its own, because it is a library a gate calls rather than a
gate — which is precisely the shape that goes unchecked.

TWO PROPERTIES, AND BOTH DIRECTIONS OF EACH ARE TESTED, because a matcher can fail two ways
and only one of them is loud. TOO STRICT and a ratchet stops excusing the thing it was
seeded for, which goes red and gets noticed within a day. TOO LOOSE and a new breach is
absorbed by an old allowance, which goes green and is noticed by nobody. So every case
below states which side it guards.

EVERY FIXTURE ASSERTS ITS OWN CONDITION FIRST and the case count is asserted against a
declared constant, for the reason this project has now been bitten by four times: a control
whose fixture never injects its condition reports green and proves only that nothing
changed.
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(os.path.dirname(HERE), "engine")
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)

import ratchet_shape as rs                    # noqa: E402

DECLARED_CASES = 18

# Two real failure messages this book produces, kept verbatim so the control tests the
# strings the gates actually emit rather than strings written to be easy.
GAP = ("asset base as at 2024-12-31 is BEHIND the information set ending 1Q2026, and the "
       "study declares no not_restated_since")
GAP_MOVED = ("asset base as at 2025-06-30 is BEHIND the information set ending 2Q2026, and "
             "the study declares no not_restated_since")
MISSING = "asset_base_record is missing disclosure"
KE_SAME = ("ke_terminal names no construction. The record must declare one of "
           "['same_beta', 'relevered']; it reproduces under 'same_beta'")
KE_RELV = ("ke_terminal names no construction. The record must declare one of "
           "['same_beta', 'relevered']; it reproduces under 'relevered' at an implied tax "
           "rate of 22.50%, which the record does not state")

CASES = []


def case(name, guards, fn, want, injected):
    CASES.append((name, guards, fn, want, injected))


# ---- excused(): must NOT excuse -----------------------------------------
case("a different claim on a listed study", "too loose",
     lambda: rs.excused({"reason": "x", "signature": GAP}, MISSING)[0], False,
     lambda: rs.fingerprint(GAP) != rs.fingerprint(MISSING))

case("same_beta seeded, relevered now reported", "too loose",
     lambda: rs.excused({"reason": "x", "signature": KE_SAME}, KE_RELV)[0], False,
     lambda: rs.fingerprint(KE_SAME) != rs.fingerprint(KE_RELV))

# FOUND BY WRITING THIS CONTROL. The first draft of the module treated a BLANK signature
# as an ABSENT one and excused the study — the cheapest possible route back to the old
# blindness, and inconsistent with every other release in this repository, each of which
# says an EMPTY reason has switched the check off rather than declared it.
case("a BLANK signature is not an absent one", "too loose",
     lambda: rs.excused({"reason": "x", "signature": ""}, MISSING)[0], False,
     lambda: True)

case("whitespace-only is blank too", "too loose",
     lambda: rs.excused({"reason": "x", "signature": "   "}, MISSING)[0], False,
     lambda: True)

case("a MISSING signature key still keeps the old behaviour", "too strict",
     lambda: rs.excused({"reason": "predates the rule"}, MISSING)[0], True,
     lambda: True)

case("a stale seed against a failure that gained a clause", "too loose",
     lambda: rs.excused({"reason": "x", "signature": GAP},
                        GAP + "; and the record names no disclosure")[0], False,
     lambda: True)

# ---- excused(): must excuse ---------------------------------------------
case("the SAME claim with every number moved", "too strict",
     lambda: rs.excused({"reason": "x", "signature": GAP}, GAP_MOVED)[0], True,
     lambda: GAP != GAP_MOVED and rs.fingerprint(GAP) == rs.fingerprint(GAP_MOVED))

case("the same claim, byte-identical", "too strict",
     lambda: rs.excused({"reason": "x", "signature": GAP}, GAP)[0], True,
     lambda: True)

case("an entry with no signature keeps the OLD behaviour", "too strict",
     lambda: rs.excused({"reason": "predates the rule"}, MISSING)[0], True,
     lambda: True)

case("a bare string entry keeps the OLD behaviour", "too strict",
     lambda: rs.excused("predates the rule", MISSING)[0], True,
     lambda: True)

case("whitespace and case differences do not break a match", "too strict",
     lambda: rs.excused({"reason": "x", "signature": GAP},
                        "  " + GAP.upper().replace(", AND", ",   AND") + " ")[0], True,
     lambda: True)

# ---- worsened(): must NOT excuse ----------------------------------------
case("a deviation far beyond what was recorded", "too loose",
     lambda: rs.worsened({"magnitude": 0.108}, -0.60, 0.05)[0], True,
     lambda: abs(-0.60) > abs(0.108) + 0.05)

case("just OUTSIDE the tolerance", "too loose",
     lambda: rs.worsened({"magnitude": 0.108}, 0.1581, 0.05)[0], True,
     lambda: abs(0.1581) > abs(0.108) + 0.05)

case("a sign flip of the same size is NOT worse", "too strict",
     lambda: rs.worsened({"magnitude": 0.108}, -0.108, 0.05)[0], False,
     lambda: abs(-0.108) == abs(0.108))

# ---- worsened(): must excuse --------------------------------------------
case("within the tolerance", "too strict",
     lambda: rs.worsened({"magnitude": 0.108}, 0.13, 0.05)[0], False,
     lambda: abs(0.13) <= abs(0.108) + 0.05)

case("exactly ON the tolerance edge", "too strict",
     lambda: rs.worsened({"magnitude": 0.108}, 0.158, 0.05)[0], False,
     lambda: abs(0.158) <= abs(0.108) + 0.05 + 1e-12)

case("an improvement is never a new breach", "too strict",
     lambda: rs.worsened({"magnitude": 0.60}, 0.02, 0.05)[0], False,
     lambda: True)

case("an entry with no magnitude keeps the OLD behaviour", "too strict",
     lambda: rs.worsened({"reason": "x"}, -0.99, 0.05)[0], False,
     lambda: True)


def main():
    print("[R-ENF-08] negative control — the module that decides what is EXCUSED\n")
    assert len(CASES) == DECLARED_CASES, (
        "case count moved: %d present, %d declared" % (len(CASES), DECLARED_CASES))
    bad = 0
    for name, guards, fn, want, injected in CASES:
        if not injected():
            print("  FIXTURE  %-52s CONDITION NOT INJECTED" % name)
            bad += 1
            continue
        got = fn()
        ok = (got == want)
        print("  %-6s %-9s %-52s -> %s"
              % ("ok" if ok else "WRONG", "[%s]" % guards, name, got))
        if not ok:
            bad += 1
    loose = sum(1 for c in CASES if c[1] == "too loose")
    print("\n%d case(s): %d guard against being TOO LOOSE (a real breach silently "
          "excused), %d against being TOO STRICT (a seeded allowance stopping working)"
          % (len(CASES), loose, len(CASES) - loose))
    if bad:
        print("FAIL — %d case(s) did not behave as declared." % bad)
        return 1
    print("OK — excuses what it recorded and nothing else.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
