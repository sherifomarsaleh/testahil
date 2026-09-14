"""Re-state ADIB's per-origin correction record under the PRE-REGISTERED rule.

WHY THIS EXISTS. corrections_log.json carries two things that no longer agree.
Its summary says what it has always said and what is still true -- 14 candidates
tested, ZERO promoted -- while its per-origin `log` records eight drivers as
`applied`, each at three or more resolved cells and half strength. That was the
rule in force when the run was made. It is not the rule now: decision_rule.py
adopts NONE of ADIB's 14 drivers, and check_walkforward_actuation reads the
per-origin record, not the summary, so the run reads as applying corrections the
rule declines.

WHAT THIS DOES NOT DO. It does not re-score the walk-forward and it moves no
number anybody reads. The corrections were never promoted (`adopted: 0`), the
study takes only `candidates`, `watch_flags` and `refused_as_aggregates` from
this file for a note, and ADIB publishes no fair value at all. What changes is
what the record CLAIMS about its own decisions.

WHY NOT corrections.py. That script writes a different, thinner shape and would
drop `candidates`, `watch_flags`, `refused_as_aggregates`, `declined_on_own_test`,
`not_a_bias`, `second_clause` and `first_clause` -- three of which the ADIB study
reads. The generator that produced the file on disk is not in this repository, so
the summary is PRESERVED here rather than recomputed: this script rewrites the
per-origin decisions and touches nothing else.

`n_resolved` is a MEASUREMENT and is carried through unchanged; a rule change
does not alter how many cells had resolved. `applied` becomes false and
`outcome_mae_change` becomes 0.0 because nothing is applied. The factor the
PREVIOUS rule applied is kept under `superseded_factor` rather than deleted, so
the change is legible in the record itself.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, os.path.join(ENGINE, "walkforward"))

import decision_rule as DR  # noqa: E402

LOG = os.path.join(HERE, "corrections_log.json")
SCORES = os.path.join(HERE, "scores.json")
REASON = ("the pre-registered rule does not adopt this driver "
          "[decision_rule.py]; measured and not acted on")


def main():
    doc = json.load(open(LOG, encoding="utf-8"))
    adopted = set(DR.summary(DR.run(json.load(open(SCORES, encoding="utf-8"))))["adopted"])

    entries = doc.get("log") or []
    if not isinstance(entries, list):
        raise SystemExit("FATAL: `log` is %s, not the per-origin list this script "
                         "re-states. Refusing to guess." % type(entries).__name__)

    changed = 0
    for e in entries:
        for drv, c in (e.get("corrections") or {}).items():
            if drv in adopted:
                continue                       # the rule adopts it: leave it alone
            was = c.get("applied")
            if isinstance(was, bool) or not was:
                continue                       # already not applied
            c["applied"] = False
            c["reason"] = REASON
            c["outcome_mae_change"] = 0.0
            c["superseded_factor"] = was       # what the PREVIOUS rule applied
            changed += 1

    doc["rule"] = ("pre-registered decision rule (decision_rule.py) — adopts %d of "
                   "the %d candidates on this name"
                   % (len(adopted), doc.get("candidates", 0)))
    doc["restated"] = ("per-origin decisions re-stated under the pre-registered rule by "
                       "rebuild_corrections_log.py; summary fields preserved as generated")
    json.dump(doc, open(LOG, "w", encoding="utf-8"), indent=1)
    print("adopted by the rule: %d" % len(adopted))
    print("per-origin corrections re-stated as not applied: %d" % changed)


if __name__ == "__main__":
    main()
