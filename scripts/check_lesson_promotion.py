#!/usr/bin/env python3
"""[R-LESSON-02] A LESSON SAYS WHETHER IT REACHES THE LAYER THAT BINDS, AND THE DEBT
IS COUNTED.

[R-LESSON-01] settles that the register binds nothing, and this gate does not move
that by an inch: it enforces no lesson on any study, it consults no study, and a
provisional lesson is skipped rather than declared. What it counts is the
CONVERSION -- how many lessons that could have been made arithmetic have been, and
how many are waiting.

WHY IT EXISTS, MEASURED RATHER THAN ARGUED. On 18-09-2026, with the register's own
machinery excluded from the probe, 19 of 312 lessons reached the binding layer at
all -- 6.1%. The cost of that is already recorded in this house's own words: [L-048]
and [L-055] were registered, correct, and re-violated by the studies delivered after
them, which is why [R-MACRO-01] exists and says so. The debt was real, it was
growing, and nothing could name it, because nothing distinguished a lesson a rule
enforces from a lesson that genuinely cannot be enforced from a lesson somebody meant
to get to.

THE FIRST MEASUREMENT OF THAT 6.1% WAS WRONG AND THE CORRECTION IS THE REASON THIS
GATE'S PROBE NAMES ITS EXCLUSIONS: the probe searched scripts/ and engine/ for each
lesson id and reported 312 of 312, because lessons_register.py lives in engine/ and
every id matched its own source. [L-355] on the instrument again -- a reader that
finds what it planted. The exclusion list below is therefore explicit and each entry
is the register's own machinery, named rather than pattern-matched.

WHAT IT CHECKS, AND IT IS THE EASIER HALF [R-ASSET-02]: that a lesson claiming
enforcement NAMES SOMETHING THAT EXISTS -- a rule id resolving in a governing
document, or a file on disk. IT DOES NOT CHECK THAT THE NAMED THING BINDS THAT
LESSON, which is judgement, and a gate asserting it would be making a claim it cannot
support. The half it does check still catches the rot that matters: a rule retired,
or a module deleted, leaves a lesson reading as enforced while nothing enforces it.

RATCHETED [R-ENF-02]: 209 ALL-scope adopted lessons carried no declaration when this
rule was adopted, and requiring one of all of them at once would be red from the day
it was written. They are listed and the list MAY ONLY SHORTEN. A lesson added AFTER
adoption with no declaration is a NEW breach -- which is the whole point, because the
debt this rule is about is the one that grows.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS: zero lessons read fails, and zero ELIGIBLE
lessons read across a register that is present fails -- a reader whose eligibility
test stopped matching looks exactly like a register with nothing in it.
"""
import json
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))

import lessons_register as LR          # noqa: E402
import lesson_promotion as LP          # noqa: E402

RATCHET = os.path.join(ROOT, "engine", "build_depth_audit",
                       "lesson_promotion_outstanding.json")


def governing_text():
    t = open(os.path.join(ROOT, "engine", "Standing_Research_Protocol.md"),
             encoding="utf-8").read()
    digests = glob.glob(os.path.join(ROOT, "engine", "PROJECT_INSTRUCTIONS_*.md"))
    if len(digests) != 1:
        raise SystemExit("FAIL — %d files match the digest pattern; exactly one is "
                         "expected and the resolver is what failed, not the book"
                         % len(digests))
    return t + open(digests[0], encoding="utf-8").read()


def main(prune=False):
    ratchet = (json.load(open(RATCHET)) if os.path.exists(RATCHET)
               else {"outstanding": []})
    listed = set(ratchet.get("outstanding", []))

    lessons = LR.LESSONS
    if not lessons:
        print("FAIL — zero lessons read. The register resolver is broken, not the "
              "book. [R-ENF-04]")
        return 1
    eligible = [l for l in lessons if LP.eligible(l)]
    if not eligible:
        print("FAIL — %d lessons are present and ZERO are eligible. The eligibility "
              "test stopped matching, which reads exactly like a register with "
              "nothing in it. [R-ENF-04]" % len(lessons))
        return 1

    doc = governing_text()
    buckets = {k: [] for k in ("enforced", "prose", "outstanding")}
    problems = []
    for l in eligible:
        state, detail = LP.classify(l, doc)
        if state in buckets:
            buckets[state].append((l["id"], detail))
        else:
            problems.append((l["id"], state, detail))

    skipped = len(lessons) - len(eligible)
    print("LESSON PROMOTION — [R-LESSON-02]")
    print("read %d lessons; %d eligible (ALL scope, adopted); %d skipped "
          "(CLASS, STOCK or provisional — out of scope by the promotion rule)"
          % (len(lessons), len(eligible), skipped))
    print()
    print("   enforced by a rule or an instrument : %3d" % len(buckets["enforced"]))
    print("   prose, with its reason              : %3d" % len(buckets["prose"]))
    print("   OUTSTANDING — testable, not built   : %3d" % len(buckets["outstanding"]))
    for lid, note in sorted(buckets["outstanding"]):
        print("        %-8s %s" % (lid, note or "(no note)"))
    print()

    undeclared = [p for p in problems if p[1] == "undeclared"]
    other = [p for p in problems if p[1] != "undeclared"]
    known = [p for p in undeclared if p[0] in listed]
    new = [p for p in undeclared if p[0] not in listed]

    print("   undeclared, on the ratchet          : %3d" % len(known))
    if new:
        print("   undeclared, NEW                     : %3d" % len(new))
        for lid, _, _ in sorted(new):
            print("        NEW   %s carries no promotion declaration" % lid)
    for lid, state, detail in sorted(other):
        print("        RED   %-8s %s — %s" % (lid, state, detail))

    if prune:
        still = {p[0] for p in undeclared}
        kept = sorted(still & listed)
        dropped = sorted(listed - still)
        ratchet["outstanding"] = kept
        json.dump(ratchet, open(RATCHET, "w"), indent=1)
        print("\npruned: %d dropped (%s); the list may only ever SHORTEN"
              % (len(dropped), ", ".join(dropped) or "none"))
        return 0

    stale = sorted(listed - {p[0] for p in undeclared})
    if stale:
        print("\nFAIL — %d lesson(s) on the ratchet now carry a declaration and were "
              "not pruned: %s" % (len(stale), ", ".join(stale)))
        return 1
    if new or other:
        print("\nFAIL — %d new undeclared lesson(s) and %d broken declaration(s)."
              % (len(new), len(other)))
        return 1
    print("OK — no new undeclared lesson and no broken declaration. %d on the "
          "ratchet, which may only SHORTEN." % len(known))
    return 0


if __name__ == "__main__":
    sys.exit(main(prune="--prune" in sys.argv))
