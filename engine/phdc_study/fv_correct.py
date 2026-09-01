"""Correct PHDC's fair-value movement record. Two errors, one cause.

WHY THIS IS NOT A BREACH OF THE APPEND-ONLY RULE.  That rule protects a record
that is RIGHT from being quietly rewritten. It does not require a record that is
WRONG to be preserved as if it were true. Both corrections here are made in the
open: the superseded record is kept verbatim under `superseded`, exactly as a
replaced calibration config is, and each carries the reason it moved. Nothing is
destroyed and nothing is silently changed.

ERROR 1 — THE BASELINE WAS DECLARED UNRECOVERABLE AND IT IS NOT.  The original
record says every reachable data.js commit already held the post-run number, so
the pre-campaign figure could not be established. That conclusion was drawn from
a SHALLOW CLONE holding 23 commits. Unshallowed, the same file has 281 commits
reaching back to 11 June 2026, and PHDC's fair{} is byte-identical in every one
of them: 7.62 / 15.89 / 24.92, unchanged for the whole period. The number was
always there; the probe could not see it. That is [R-ENF-04] exactly — an empty
result read as a clean one — and the rule that the unrecoverable list may only
ever SHORTEN is what licenses this direction of travel.

ERROR 2 — THE DELIVERED VALUE IS THE PRIOR EDITION'S, NOT THIS STUDY'S.  The
record has 7.62 / 15.89 / 24.92 as edition 1's delivered fair value. PHDC's own
study calls those numbers `prior_edition_fair`, and its section 5 is titled "Why
no single fair value is published": the crux turns on an undisclosed schedule,
the method over-forecast net profit by +1.12 log on this name's own history in
97% of cells, and the per-project table the prior edition rested on is not
disclosed by the company. The study WITHDREW the point estimate on purpose.
Recording the withdrawn number as the new one inverts the finding -- it reports
a rebuild that changed nothing, when what happened is that the number was taken
away.

Left uncorrected the two errors cancel into a 0.0% movement, which is the most
misleading cell the table could carry.
"""

import json
import os
import sys

ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ENGINE, "fv_movement.json")

# Verified against 281 commits of assets/data.js, 11-Jun-2026 to 01-Sep-2026:
# PHDC's fair{} is identical in every one.
RECOVERED = {"bear": 7.62, "base": 15.89, "full": 24.92}
EVIDENCE = ("recovered from assets/data.js history: unchanged across all 281 "
            "commits touching that file between 11-Jun-2026 and 01-Sep-2026. "
            "The original record declared it unrecoverable on the evidence of a "
            "SHALLOW clone holding 23 commits; unshallowing the repository "
            "resolved it. An empty result was read as a clean one.")
WITHDRAWN = ("no single fair value published — the study withdrew the prior "
             "edition's point estimate deliberately (its section 5): the crux "
             "rests on a schedule the company does not disclose, the method "
             "over-forecast net profit on this name's own history by +1.12 log "
             "in 97% of cells, and the per-project table the prior number rested "
             "on is not disclosed. Years 3-5 go out as ranges instead.")


def main():
    d = json.load(open(STORE, encoding="utf-8"))
    e = d["entries"]["PHDC"]
    if e.get("superseded"):
        print("PHDC already carries a correction; nothing to do.")
        return 0

    e["superseded"] = {
        "reason": "baseline wrongly declared unrecoverable from a shallow "
                  "clone, and the prior edition's fair value recorded as this "
                  "edition's delivered value",
        "corrected": "2026-09-01",
        "baseline": json.loads(json.dumps(e["baseline"])),
        "editions": json.loads(json.dumps(e["editions"])),
    }

    e["baseline"]["unrecoverable"] = None
    e["baseline"]["fair"] = dict(RECOVERED)
    e["baseline"]["recovered"] = EVIDENCE

    ed = e["editions"][0]
    ed["fair"] = None
    ed["withdrawn"] = WITHDRAWN
    ed["vs_baseline_pct"] = None
    ed["vs_previous_pct"] = None

    json.dump(d, open(STORE, "w", encoding="utf-8"), indent=1, sort_keys=True)
    open(STORE, "a", encoding="utf-8").write("\n")
    print("PHDC corrected: baseline %s (recovered); edition 1 delivers no "
          "single fair value. Prior record kept under `superseded`."
          % RECOVERED)
    return 0


if __name__ == "__main__":
    sys.exit(main())
