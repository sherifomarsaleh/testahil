#!/usr/bin/env python3
"""[R-SIGCM-02] — THE GROUND-UP CLAUSE IS RUN, NOT COUNTED, AND ITS RECORD IS THE INPUT.

WHY THIS EXISTS. SIGCM clause 2 has required since July 2026 that a forecast be built from
the ground up — product by product, volume times price, cost per unit, margin an OUTPUT —
dropping to the finest sourced level only where the disclosure stops and FLAGGING the gap.
[R-SIGCM-02] then retired the self-attested boolean and replaced it with a record and an
assertion, `research_protocol.assert_ground_up()`, which requires every revenue line to
declare its build level, to cover 100% of revenue, to name the unit and its source and the
price basis where it claims a disclosed-unit build, and to carry a gap note anywhere below
that.

MEASURED 07-09-2026: NO GATE ANYWHERE CALLS IT. Searching every file in scripts/ for
`assert_ground_up` returns one hit, and it is a NAME IN A LIST inside check_protocol_text —
a check that the governing documents do not refer to a function that has ceased to exist.
The assertion is real, correct and run by nobody, which is the composite-beta shape this
repository has now closed a dozen times: a rule that is present and does not execute.

AND THE RECORD MOST STUDIES COMMIT IS THE ASSERTION'S OWN RETURN VALUE. `ground_up` in
ADNOCLS, AMOC and EGCH is the SUMMARY assert_ground_up hands back — ticker, line count,
share by level — and not the DriverLine list it was computed from. An output cannot be
re-run: the shares are there and the units, sources, price bases and gap notes are gone, so
nothing outside the study can ask the questions the assertion asks. That is [R-VCAL-01]'s
finding one artefact over — a panel is not a record a value can be rebuilt from — and it
means a study can commit a perfectly clean-looking summary of a build nobody can inspect.

Exactly ONE study of twenty-four commits the input: STC, as `driver_lines`.

WHAT IT CHECKS.
  1. Where the driver LINES are committed, the assertion is RUN on them [R-ENF-03]. The
     gate runs the instrument; it does not count the file. Treating the record's presence
     as conformance puts a green tick on a red result.
  2. A record that carries only the assertion's OUTPUT is UNREADABLE, never clean
     [R-ENF-04], and is said to be — because a summary is the cheapest possible route past
     a check that cannot see behind it.
  3. A study with no record at all is UNREADABLE too, in the same group, since
     [R-SIGCM-02] retired the flag that used to stand in for one.

WHAT IT DELIBERATELY DOES NOT DO. It does not judge whether a level is the RIGHT one for
that company's disclosure — whether a segment build should have been a unit build is a
judgement about what the filings contain, and a gate cannot read the filings. It asks only
that the record says which level each line is at, that the levels cover the revenue, and
that anything coarser than a unit build says why.

RATCHET [R-ENF-02] in TWO GROUPS that are not interchangeable [R-TERM-01]: one excuses a
study whose committed lines FAIL the assertion, the other one whose record cannot be read
at all. A study moving between them goes red until the move is recorded. Both may only
SHORTEN. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS.

USAGE
    python3 scripts/check_ground_up.py            # gate
    python3 scripts/check_ground_up.py --prune    # rewrite the ratchets SHORTER
"""
from __future__ import annotations

import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit", "ground_up_outstanding.json")
sys.path.insert(0, ENGINE)

# The keys the book actually uses for the LINE list, taken from what is committed rather
# than from what a reader might expect [L-355].
LINE_KEYS = ("driver_lines", "ground_up_lines", "revenue_driver_lines")
# The summary the assertion RETURNS. Committing this and nothing else is the unreadable case.
SUMMARY_MARKERS = ("share_by_level", "unit_share")


def studies(engine=ENGINE):
    out = {}
    for d in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(d)[:-6].upper()
        for n in ("study_numbers.json", "numbers.json"):
            p = os.path.join(d, n)
            if os.path.exists(p):
                out.setdefault(tk, p)
                break
    return out


def find_lines(doc):
    """The committed DriverLine list, under whichever name the study uses."""
    for k in LINE_KEYS:
        v = doc.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict) and "level" in v[0]:
            return k, v
    # AT ANY DEPTH, for the reason summary_only() records: these records are nested
    # under `gates/` and `drivers/gates/` in the studies that carry them.
    found = []

    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if (k in LINE_KEYS or k in ("lines", "driver_lines")) and \
                        isinstance(v, list) and v and isinstance(v[0], dict) \
                        and "level" in v[0]:
                    found.append((path + "/" + k, v))
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, path + "[%d]" % i)

    walk(doc)
    return found[0] if found else (None, None)


def summary_only(doc):
    """Is the assertion's OWN RETURN VALUE committed, at any depth?

    AT ANY DEPTH, and the first draft looked only at the top level and so told AMOC and
    EGCH they commit no record at all — both nest theirs under `gates/`, and EGCH under
    `drivers/gates/` as well. The wrong reason stated confidently is the failure this
    session has met five times; a reader that guesses a location finds nothing and reports
    it as a result [L-355].
    """
    hit = []

    def walk(o):
        if isinstance(o, dict):
            if any(m in o for m in SUMMARY_MARKERS) and "ticker" in o:
                hit.append(True)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(doc)
    return bool(hit)


def load():
    if not os.path.exists(OUTSTANDING):
        return {}, {}
    try:
        d = json.load(open(OUTSTANDING, encoding="utf-8"))
    except Exception:
        return {}, {}
    return d.get("outstanding", {}), d.get("unreadable", {})


def measure():
    """(failing, unreadable, ran) — the assertion RUN wherever the lines exist."""
    import research_protocol as rp
    failing, unreadable, ran = {}, {}, 0
    for tk, path in sorted(studies().items()):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception as exc:
            unreadable[tk] = "the committed numbers file will not parse: %s" % exc
            continue
        key, raw = find_lines(doc)
        if raw is None:
            if summary_only(doc):
                unreadable[tk] = ("commits the assertion's OUTPUT (share_by_level) and not "
                                  "the driver lines it was computed from, so nothing "
                                  "outside the study can re-run it")
            else:
                unreadable[tk] = ("commits no driver-line record at all; [R-SIGCM-02] "
                                  "retired the boolean that used to stand in for one")
            continue
        try:
            lines = [rp.DriverLine(**{f: l.get(f) for f in
                                      ("name", "level", "share_of_revenue", "unit",
                                       "unit_source", "price_basis", "cost_basis",
                                       "gap_note")}) for l in raw]
        except Exception as exc:
            unreadable[tk] = "%s does not build into driver lines: %s" % (key, exc)
            continue
        ran += 1
        try:
            rp.assert_ground_up(lines, ticker=tk)
        except AssertionError as exc:
            failing[tk] = str(exc)
            continue
        except Exception as exc:
            unreadable[tk] = "the assertion could not run: %s" % exc
            continue
        # MARGIN IS AN OUTPUT OR THE COST SIDE IS NOT BUILT, and cost_basis was DECLARED on
        # DriverLine and inspected by nothing. The standing rule is explicit: "a
        # contribution or gross margin set as an INPUT is a QC FAIL wherever the filings
        # disclose enough to build cost PER UNIT instead". A line that names how its revenue
        # was built and says nothing about its cost has left the margin somewhere nobody can
        # point at, and an absent basis looks identical from outside to a margin typed in.
        #
        # IT IS CHECKED HERE AND NOT INSIDE THE ASSERTION, and that was decided by trying
        # the other way first. Put into assert_ground_up() it fired at BUILD time and made
        # EGCH's generator refuse — a real finding on one of its lines, and a rule that
        # stops an existing study being rebuilt at all, which is the permanently-red check
        # [R-ENF-02] forbids and worse: the only ways out would be to invent a cost basis
        # (SIGCM clause 1 prohibits it) or to delete the line. In the gate it is ratcheted,
        # countable and binds forward, which is what a new requirement on delivered work
        # gets.
        #
        # THE FIELD DOES NOT HAVE TO SAY THE COST IS PER-UNIT: "held flat, the segment note
        # discloses no cost split" is a perfectly good answer and is the one most of the
        # book would give. What it may not be is ABSENT.
        missing = [l.name for l in lines if not (l.cost_basis or "").strip()]
        if missing:
            failing[tk] = ("GROUND-UP COST FAIL — %s: %d line(s) name how revenue was built "
                           "and nothing about how cost was: %s. Margin is an OUTPUT or the "
                           "cost side is not built."
                           % (tk, len(missing), ", ".join(missing[:4])))
    return failing, unreadable, ran


def main(argv):
    prune = "--prune" in argv
    all_st = studies()
    if not all_st:
        print("FAIL — examined zero study directories [R-ENF-04].")
        return 1

    failing, unreadable, ran = measure()
    if ran == 0 and not unreadable:
        print("FAIL — %d study directories and the assertion ran on none of them. A run "
              "that attempted nothing is not a run that found nothing [R-ENF-04]."
              % len(all_st))
        return 1

    known_bad, known_un = load()

    if prune:
        json.dump({"rule": "R-SIGCM-02 — the ground-up clause, run rather than counted",
                   "note": "Two groups, NOT interchangeable: one excuses committed lines "
                           "that FAIL the assertion, the other a record that cannot be "
                           "read at all. Both may only SHORTEN.",
                   "outstanding": failing, "unreadable": unreadable},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1, sort_keys=True)
        print("pruned: failing %d -> %d, unreadable %d -> %d"
              % (len(known_bad), len(failing), len(known_un), len(unreadable)))
        return 0

    print("[R-SIGCM-02] the ground-up clause, run rather than counted")
    print("  study directories examined : %d" % len(all_st))
    print("  assertions actually RUN    : %d" % ran)
    print("  passing                    : %d" % (ran - len(failing)))
    print("  unreadable                 : %d" % len(unreadable))

    new = sorted(set(failing) - set(known_bad))
    new_un = sorted(set(unreadable) - set(known_un))
    moved = sorted((set(failing) & set(known_un)) | (set(unreadable) & set(known_bad)))

    for tk in sorted(failing):
        print("  %-6s %-13s %s" % ("NEW" if tk in new else "known", tk,
                                   failing[tk][:150]))
    for tk in sorted(unreadable):
        print("  %-6s %-13s %s" % ("NEW" if tk in new_un else "known", tk,
                                   unreadable[tk][:150]))

    rc = 0
    if new:
        print("\nFAIL — %d study/studies whose committed driver lines fail the ground-up "
              "assertion: %s" % (len(new), ", ".join(new)))
        rc = 1
    if new_un:
        print("\nFAIL — %d study/studies whose ground-up record cannot be read: %s"
              % (len(new_un), ", ".join(new_un)))
        print("   An absent answer is not a clean one [R-ENF-04]. Commit the driver LINES, "
              "not the summary the assertion returns.")
        rc = 1
    if moved:
        print("\nFAIL — %d study/studies MOVED between the groups: %s"
              % (len(moved), ", ".join(moved)))
        rc = 1
    if rc:
        return rc
    print("\nOK — every committed driver-line record passes the ground-up assertion when "
          "it is actually run.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
