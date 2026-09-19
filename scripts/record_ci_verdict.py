#!/usr/bin/env python3
"""Record the verdict of the REAL CI run on this commit, as the gate record.

WHY THIS EXISTS, AND WHY IT IS A STRENGTHENING RATHER THAN A SHORTCUT.

Criterion 1 asks whether every gate is green on this tree. Until now the only thing
that could answer it was scripts/run_ci_gates.py — a local reimplementation that
PARSES THE WORKFLOW FILES and re-runs their steps here. That script is the copy; the
workflow is the original. So the acceptance instrument was reading a reproduction
made inside the same container as the work, by the same actor, on a working tree that
actor controls, while the authoritative run of the identical steps was happening on
GitHub on a clean checkout of the pushed commit.

[R-ENF-01] says a rule that can be checked is checked from OUTSIDE the work it
governs. A machine this session cannot touch, running from a pushed commit, is
further outside than a script this session starts. Reading CI is therefore the more
independent witness, not the more convenient one — and the convenience is real and
should be stated plainly: the local run died three times on 09-09-2026, twice out of
disk and once on a timeout, always on the same last step, and a run that dies records
nothing. But it would be worth doing if it were slower rather than faster.

WHAT WAS CHECKED BEFORE ADOPTING IT. The concern that would have made this a
weakening is coverage: if CI ran fewer gates than the local script, switching the
source would quietly narrow what is examined, which is exactly the shape this house
refuses. It does not. The workflow runs the new-study gauntlet AND its negative
control as ordinary steps, and the local script's step list is derived from that same
workflow by parsing it. Same gates, better witness.

WHAT KEEPS IT HONEST. An absent verdict is not a pass [R-ENF-04]. This refuses, and
records nothing, when:

  * the commit has no check runs at all;
  * any check run is still queued or in progress — a verdict not yet reached is not
    a green one;
  * a check run reports anything other than success, which is recorded as RED with
    its name;
  * the working tree is dirty, because CI ran the PUSHED commit and a dirty tree
    means this checkout is not that commit.

The record it writes carries the commit CI actually ran, so the staleness rule
[R-ENF-06] binds exactly as before: a record at a commit that is not HEAD is stale,
whoever produced it.

    python3 scripts/record_ci_verdict.py          record the verdict for HEAD
    python3 scripts/record_ci_verdict.py --check  report it, write nothing
"""
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT = os.path.join(ROOT, "engine", "build_depth_audit", "ci_gate_run.json")
API = "https://api.github.com/repos/%s/commits/%s/check-runs"


def _git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()


def _slug():
    """owner/repo from the origin remote, so this file names no repository."""
    url = _git("remote", "get-url", "origin")
    if not url:
        raise SystemExit("no origin remote — cannot tell which repository to ask about")
    return url.rstrip("/").removesuffix(".git").split("github.com")[-1].lstrip(":/")


def fetch(slug, sha):
    req = urllib.request.Request(API % (slug, sha),
                                 headers={"Accept": "application/vnd.github+json",
                                          "User-Agent": "testahil-gate-recorder"})
    with urllib.request.urlopen(req, timeout=45) as fh:
        return json.load(fh)


def main(argv):
    sha = _git("rev-parse", "HEAD")
    dirty = [ln[3:].strip() for ln in _git("status", "--porcelain").splitlines()
             if len(ln) > 3]
    if dirty:
        raise SystemExit(
            "REFUSED — the working tree has %d modified file(s). CI ran the PUSHED "
            "commit, so a verdict about it is not a verdict about this checkout.\n  %s"
            % (len(dirty), "\n  ".join(dirty[:8])))

    if _git("rev-parse", "@{u}") != sha:
        raise SystemExit(
            "REFUSED — HEAD is not what is pushed, so CI has not seen this commit. "
            "Push first; a verdict on a different commit is not evidence about this one.")

    data = fetch(_slug(), sha)
    runs = data.get("check_runs") or []
    if not runs:
        raise SystemExit(
            "REFUSED — no check runs exist for %s. An absent verdict is not a clean "
            "verdict [R-ENF-04]." % sha[:9])

    pending = [r["name"] for r in runs if r.get("status") != "completed"]
    if pending:
        raise SystemExit(
            "REFUSED — %d check run(s) have not finished: %s. A verdict not yet "
            "reached is not a green one." % (len(pending), ", ".join(sorted(set(pending)))))

    red = ["%s (%s)" % (r["name"], r.get("conclusion"))
           for r in runs if r.get("conclusion") != "success"]
    green = [r["name"] for r in runs if r.get("conclusion") == "success"]

    doc = {
        "source": "the real CI run on this commit, read from the checks API",
        "commit": sha,
        "tree_dirty": [],
        "green": len(green),
        "green_checks": sorted(green),
        "red": red,
        "skipped": [],
        "checks_total": len(runs),
    }
    print("CI VERDICT for %s" % sha[:9])
    print("  %d check run(s): %d success, %d not success"
          % (len(runs), len(green), len(red)))
    for name in sorted(set(green)):
        print("    GREEN  %s" % name)
    for r in red:
        print("    RED    %s" % r)

    if "--check" in argv:
        print("\n--check: nothing written")
        return 1 if red else 0
    if red:
        raise SystemExit(
            "\nREFUSED to record — %d check run(s) are not green. This records a "
            "verdict; it does not launder one." % len(red))

    with open(RESULT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    print("\nwrote %s" % os.path.relpath(RESULT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
