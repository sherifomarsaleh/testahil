"""Every gate on disk runs in some workflow.  [R-ENF-01]

ADOPTED 18-09-2026 ON A MEASURED OMISSION. Six gates were written, negative-controlled and
committed that day -- check_real_terms_paths, check_flat_nominal_claim,
check_lesson_promotion, check_beta_estimator_disclosure, check_deferral_reason and
check_study_debt -- and NOT ONE of them was in a workflow. scripts/repair_loop.py finds
gates by glob and picked all six up; CI is a TYPED LIST and picked up none.

A GATE OUTSIDE A WORKFLOW IS ENFORCEMENT THAT RUNS WHEN SOMEBODY REMEMBERS, which is
exactly what the enforcement layer exists to replace, and [R-MERGE-01] says green means
EVERY gate rather than a subset. The omission was silent by construction: a typed list
says nothing about what is not in it, so no amount of reading this workflow would reveal
a gate that is missing from it. The only way to see it is to anchor on the OTHER
population -- the files on disk -- which is [R-ENF-04] one level up.

THIS CLOSES THE CLASS RATHER THAN THE INSTANCE. Adding the six by hand fixes today and
guarantees nothing about the next gate somebody writes at midnight.

EXCLUSIONS ARE NAMED WITH THEIR REASONS AND THEIR NAMES MUST RESOLVE ON DISK, because an
allowance nobody has to justify is where the next omission hides, and one naming a file
that no longer exists is an allowance for nothing.
"""
from __future__ import annotations

import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# Each with a reason. A gate here is one whose SUBJECT is not a repository state that a
# scheduled run can check, or one another gate already invokes.
EXCLUDED = {
    "check_publish_block.py":
        "invoked by scripts/publish_site.py as STEP 0/6, ahead of the build, which is "
        "where [R-GAP-02] puts it: it governs a PUBLISH rather than a commit, and a name "
        "that may not publish should cost nothing to discover. Running it here as well "
        "would report the book's standing hold as a broken build on every push.",
    "check_workflows_complete_negative_control.py":
        "invoked by nothing else BY DESIGN: it runs this gate as a subprocess against "
        "sandboxes, and listing it here as well would be the gate proving itself.",
}


def gates():
    return sorted(os.path.basename(p)
                  for p in glob.glob(os.path.join(HERE, "check_*.py")))


def invoked():
    """Every script name any workflow actually invokes, by a real `run:` line."""
    seen = set()
    for p in sorted(glob.glob(os.path.join(WORKFLOWS, "*.yml"))
                    + glob.glob(os.path.join(WORKFLOWS, "*.yaml"))):
        body = open(p, encoding="utf-8").read()
        for m in re.finditer(r"scripts/(check_[A-Za-z0-9_]+\.py)", body):
            # ONLY a line that RUNS it counts. The workflow also lists scripts under
            # `paths:` so a change to one triggers the job, and a name appearing there
            # and nowhere else is a TRIGGER rather than a check -- which reads identical
            # to being covered and is exactly the shape this gate exists to refuse.
            line = body[body.rfind("\n", 0, m.start()) + 1: m.end()]
            if re.search(r"(?:^|\s)(?:run:|python3?\s)", line):
                seen.add(m.group(1))
    return seen


def main(argv=None):
    argv = argv or sys.argv[1:]
    on_disk = gates()
    if not on_disk:
        print("FAIL - zero gates found on disk. The population resolver is broken, not "
              "the repository. [R-ENF-04]")
        return 1
    if not os.path.isdir(WORKFLOWS):
        print("FAIL - no workflow directory, so nothing runs anything. [R-ENF-04]")
        return 1
    ran = invoked()
    if not ran:
        print("FAIL - zero gate invocations read across the workflows. A reader that "
              "stopped matching reads exactly like a repository that runs nothing "
              "[R-ENF-04].")
        return 1

    stale = sorted(n for n in EXCLUDED if not os.path.exists(os.path.join(HERE, n)))
    empty = sorted(n for n, why in EXCLUDED.items() if not str(why).strip())
    missing = [n for n in on_disk if n not in ran and n not in EXCLUDED]

    print("[R-ENF-01] every gate on disk runs in some workflow")
    print("  gates on disk            : %d" % len(on_disk))
    print("  invoked by a workflow    : %d" % len([n for n in on_disk if n in ran]))
    print("  excluded, with a reason  : %d" % len(EXCLUDED))
    print("  not run anywhere         : %d" % len(missing))

    if stale:
        print("\nFAIL - excluded and not on disk: %s. An allowance for a file that does "
              "not exist is an allowance for nothing." % ", ".join(stale))
        return 1
    if empty:
        print("\nFAIL - excluded with an EMPTY reason: %s. An empty reason has switched "
              "the check off rather than declared it." % ", ".join(empty))
        return 1
    if missing:
        for n in missing:
            print("  FAIL  %s runs in no workflow" % n)
        print("\nFAIL - a gate outside a workflow is enforcement that runs when somebody "
              "remembers. Add it to a workflow in the commit that writes it, or exclude "
              "it here WITH ITS REASON.")
        return 1
    print("\nOK - every gate on disk is invoked somewhere, or excluded with a reason that "
          "resolves.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
