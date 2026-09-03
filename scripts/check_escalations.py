#!/usr/bin/env python3
"""[R-IND-01] — the escalation register is checked from outside, and against reality.

Every question that reaches the principal is an artefact with a required shape, and
this gate reads it the way every other [R-ENF-01] gate reads the thing it governs:
from outside, failing rather than warning.

FIVE REFUSALS, each earned by a measured failure rather than imagined:

1. SHAPE. An entry missing any required field FAILS. A question with no recorded
   routes is a question nobody can tell was necessary.

2. THE LADDER WAS CLIMBED. A missing_data escalation records at least three routes,
   and at least one must be a RE-RUN — because an empty result is first evidence
   that the probe did not run [R-ENF-04], and quoting a previous run's outcome is
   quoting a fact about the past. It must also record how many refs it searched:
   on 3 September 2026 this session asked for a series the principal had supplied
   that morning, having searched exactly one.

3. THE ANSWER HAS NOT ALREADY ARRIVED. Every OPEN entry names the condition that
   would resolve it, and this gate re-checks that condition across every live ref.
   An entry still asking for something now present goes RED. THIS IS THE CLAUSE THE
   RULE EXISTS FOR: the register cannot go on asking, because the thing that asks is
   also the thing checked against the world.

4. A RESOLVED ANSWER IS WRITTEN WHERE THE NEXT SESSION READS IT. A resolved entry
   names the file that now carries the answer, and that file must actually contain
   its marker. An answer that lives only in a conversation binds nothing — the
   whole re-ask happened because the archive on main still said "the one thing I
   would ask you for" while the answer sat on a branch.

5. A GATE WITH NO RELEASE IS A STALL [R-CAL-01]. Every entry carries a default and
   the date that default fires. An open entry past its date FAILS: by then the
   default was to be taken and the entry closed, so an open one means the work
   stopped to wait, which is the thing this rule forbids.

There is no ratchet, deliberately. A ratchet exists so a NEW standard does not
redden work that predates it; this register is created by this rule and contains
only entries written under it, so an allowance would exempt the rule from itself.
"""
from __future__ import annotations

import datetime as dt
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
import escalations as E   # noqa: E402

MIN_ROUTES = 3


def main(argv=None) -> int:
    reg = E.load()
    entries = reg.get("entries")
    if entries is None:
        print("FAIL — engine/escalations.json carries no entries list. A register that "
              "cannot be read is not an empty one.")
        return 1

    fails, ok = [], 0
    today = dt.date.today().isoformat()
    print("[R-IND-01] escalation register — %d entr%s, checked against %d live refs"
          % (len(entries), "y" if len(entries) == 1 else "ies", len(E.live_refs())))

    seen = {}
    for e in entries:
        key = e.get("key") or "(unkeyed)"
        bad = []

        for f in E.REQUIRED:
            v = e.get(f)
            if v is None or (isinstance(v, str) and not v.strip()) or v == []:
                bad.append("no %s" % f)

        if e.get("cls") not in E.CLASSES:
            bad.append("class %r is not one of %s" % (e.get("cls"), ", ".join(E.CLASSES)))

        routes = e.get("routes") or []
        if e.get("cls") == "missing_data":
            if len(routes) < MIN_ROUTES:
                bad.append("%d route(s) recorded; a missing_data escalation records at "
                           "least %d, each RUN and not recalled" % (len(routes), MIN_ROUTES))
            if not any(r.get("rerun") for r in routes if isinstance(r, dict)):
                bad.append("no route is marked as a RE-RUN. An empty result is first "
                           "evidence that the probe did not run [R-ENF-04]; a remembered "
                           "failure is a fact about the past.")
        for r in routes:
            if not isinstance(r, dict) or not r.get("route") or not r.get("outcome"):
                bad.append("a route records no route/outcome pair")
                break
        if not isinstance(e.get("refs_searched"), int) or e.get("refs_searched", 0) < 2:
            bad.append("refs_searched is %r. The repository is not one ref: work in "
                       "flight on another branch is work that exists, and on 3 September "
                       "2026 a series already supplied was asked for again after a "
                       "search of exactly one." % e.get("refs_searched"))

        if key in seen:
            bad.append("duplicates an earlier entry (%s). A question already asked is "
                       "not asked again." % seen[key])
        seen[key] = e.get("opened")

        resolved_now, where = E.is_resolved(e)
        status = e.get("status")
        if status == "open":
            if resolved_now:
                bad.append("STILL OPEN AND ALREADY ANSWERED — its own resolves_when "
                           "marker is present on %s. Close it, write the answer where "
                           "the next session reads it, and never ask again." % where)
            dd = e.get("default_date")
            if dd and dd < today:
                bad.append("open past its default_date of %s. By then the default was "
                           "to be taken and the entry closed; an open one means the "
                           "work stopped to wait. A gate with no release is a stall."
                           % dd)
        elif status == "resolved":
            awt = e.get("answer_written_to")
            if not awt:
                bad.append("resolved but names no file the answer was written to. An "
                           "answer that lives only in a conversation binds nothing.")
            elif not resolved_now:
                bad.append("marked resolved, but its own marker is present on no live "
                           "ref (%s). Either the answer was never written down or it "
                           "names the wrong file." % where)
        else:
            bad.append("status %r is neither open nor resolved" % status)

        if bad:
            fails.append((key, bad))
        else:
            ok += 1
            print("  ok    %-46s %s%s" % (key[:46], status,
                                          "" if status != "resolved"
                                          else "  (answer on %s)" % where))

    if fails:
        print("\nFAIL — %d escalation(s) do not hold:" % len(fails))
        for key, bad in fails:
            print("  %s" % key)
            for b in bad:
                print("     - %s" % b)
        return 1
    print("\nOK — %d escalation(s), every one shaped, searched, and still unanswered "
          "or written down." % ok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
