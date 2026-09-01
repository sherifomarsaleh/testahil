"""Record this run in the fair-value movement register.

The campaign's rule is FREEZE THE OLD FAIR VALUE FIRST, because a rebuild is
the one sanctioned thing that moves TICKERS.TMGH.fair and a baseline read
afterwards is a fabricated zero.  This run is the case that rule allows: it was
run under the standing fundamental-calibration instruction, which says nothing
reaches the live site, so assets/data.js was never written.  TMGH's fair{} on
this branch is byte-identical to the one on the default branch, so the baseline
frozen here is the genuine pre-run number and not a post-run reading of our own
output.  That is stated rather than assumed, because the whole point of the
register is that a baseline taken at the wrong moment looks exactly like one
taken at the right moment.

THE BASE LEG IS NOT A DELIVERED NUMBER.  The study publishes FOUR cases and no
point estimate -- two cost-of-capital bases against two readings of the crux,
held apart under the dual-framing rule and never averaged into one answer.  The
register stores three legs, so bear and full are the study's own published
extremes and the base leg is the median of the four cases, recorded only so a
movement can be computed against the old triple.  It is not quoted anywhere a
reader can see it and it is not the study's answer.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fv_movement as FV

# The four published per-share cases, minority framed at book.  Read from the
# study's own committed numbers file rather than typed: numeric traceability
# applies to this record exactly as it does to the delivered documents.
NUMBERS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "study_numbers.json")

LESSONS = ["L-043", "L-044", "L-045", "L-046", "L-047", "L-117", "L-118"]


def legs():
    import json
    cases = sorted(json.load(open(NUMBERS, encoding="utf-8"))
                   ["per_share_nci_book"].values())
    assert len(cases) == 4, cases
    return round(cases[0], 3), round((cases[1] + cases[2]) / 2.0, 3), \
        round(cases[-1], 3)


if __name__ == "__main__":
    bear, base, full = legs()
    FV.record("TMGH", bear, base, full, "full", "FY2015-FY2024, h=1-5", LESSONS)
    FV.build()
    raise SystemExit(FV.check())
