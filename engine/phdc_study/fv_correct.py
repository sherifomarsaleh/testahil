"""Correct PHDC's fair-value movement record. Three errors, one cause each.

WHY THIS IS NOT A BREACH OF THE APPEND-ONLY RULE.  That rule protects a record
that is RIGHT from being quietly rewritten. It does not require a record that is
WRONG to be preserved as if it were true. Every correction is made in the open:
the superseded record is kept verbatim under a `superseded` key, exactly as a
replaced calibration config is, and carries the reason it moved.

ERROR 1 — THE BASELINE WAS DECLARED UNRECOVERABLE AND IT IS NOT.  The original
record says every reachable data.js commit already held the post-run number, so
the pre-campaign figure could not be established. That was read off a SHALLOW
CLONE holding 23 commits. Unshallowed, the same file has 281 commits back to
11 June 2026 and PHDC's fair{} is byte-identical in every one:
7.62 / 15.89 / 24.92. The number was always on the site; the probe could not see
it. That is [R-ENF-04] -- an empty result read as a clean one -- and the rule
that the unrecoverable list may only ever SHORTEN is what licenses the fix.

ERROR 2 — THE DELIVERED VALUE WAS THE PRIOR EDITION'S.  The record had
7.62 / 15.89 / 24.92 as edition 1's delivered value. PHDC's own numbers file
calls those `prior_edition_fair`. They are the BEFORE figures, sitting in the
after column, which reported a rebuild that changed nothing.

ERROR 3 — AND THE FIX FOR ERROR 2 WAS ALSO WRONG.  Reading the study's section
5, "Why no single fair value is published", the after value was first recorded
as WITHDRAWN. That misread it. The study withholds a single POINT; it publishes
a RANGE, and prominently -- its valuation summary carries the four-lens weighted
read as bear 4.60 / central 10.94 / full 23.33, and its headline states the crux
at EGP 4.29 low to EGP 35.14 high. "No single value" was both wrong and useless
to a reader: A RANGE IS A VALUE, and refusing to print it says nothing while
sounding careful -- the cautious-sounding claim that never gets audited, which
this project has already been caught by once.
"""

import json
import os
import sys

ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ENGINE, "fv_movement.json")
NUMBERS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "study_numbers.json")

# Verified against 281 commits of assets/data.js, 11-Jun-2026 to 01-Sep-2026.
RECOVERED = {"bear": 7.62, "base": 15.89, "full": 24.92}
EVIDENCE = ("recovered from assets/data.js history: unchanged across all 281 "
            "commits touching that file between 11-Jun-2026 and 01-Sep-2026. "
            "The original record declared it unrecoverable on the evidence of a "
            "SHALLOW clone holding 23 commits; unshallowing the repository "
            "resolved it. An empty result was read as a clean one.")


def delivered():
    """The range the study actually publishes, read from its own numbers file.

    lens_weighted is the four-lens weighted synthesis printed in the study's
    valuation summary -- the same bear/base/full shape assets/data.js carries,
    so the before and after are the same kind of object and can be compared.
    """
    d = json.load(open(NUMBERS, encoding="utf-8"))
    w = d["lens_weighted"]
    return {k: round(w[k], 2) for k in ("bear", "base", "full")}


def main():
    d = json.load(open(STORE, encoding="utf-8"))
    e = d["entries"]["PHDC"]
    new = delivered()

    if not e.get("superseded"):
        e["superseded"] = {
            "reason": "baseline wrongly declared unrecoverable from a shallow "
                      "clone, and the prior edition's fair value recorded as "
                      "this edition's delivered value",
            "corrected": "2026-09-01",
            "baseline": json.loads(json.dumps(e["baseline"])),
            "editions": json.loads(json.dumps(e["editions"])),
        }

    e["baseline"]["unrecoverable"] = None
    e["baseline"]["fair"] = dict(RECOVERED)
    e["baseline"]["recovered"] = EVIDENCE

    ed = e["editions"][0]
    ed.pop("withdrawn", None)
    ed["fair"] = new
    ed["basis"] = ("four-lens weighted synthesis, the range the study's own "
                   "valuation summary publishes. The study withholds a single "
                   "POINT estimate (its section 5) and publishes this range.")
    ed["vs_baseline_pct"] = {k: round(100.0 * (new[k] - RECOVERED[k])
                                      / RECOVERED[k], 1)
                             for k in ("bear", "base", "full")}
    ed["vs_previous_pct"] = None

    json.dump(d, open(STORE, "w", encoding="utf-8"), indent=1, sort_keys=True)
    open(STORE, "a", encoding="utf-8").write("\n")
    print("PHDC corrected: before %s -> after %s (%+.1f%% on the central leg)"
          % (RECOVERED, new, ed["vs_baseline_pct"]["base"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
