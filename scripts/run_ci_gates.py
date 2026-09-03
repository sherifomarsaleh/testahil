#!/usr/bin/env python3
"""Run exactly what CI runs, by reading CI's own definition.

WHY THIS EXISTS. On 3 September 2026 I reported "every gate green" after running
the scripts/check_*.py suite by hand, and CI was red — had been red for a day — on
a step that lives inline in the workflow rather than in a check script. The claim
was not a lie and it was not true either: I had run a DIFFERENT POPULATION from
the one CI runs, and my sweep could not see the difference because it was built
from a list I maintained rather than from the workflow.

That is [R-ENF-04] in its usual costume. The fix is the usual one: anchor the
population somewhere else. This script parses the workflow YAML and executes every
`run:` step it finds, so it cannot drift from CI — a step added to the workflow is
a step this runs, without anyone remembering to add it here.

It is a convenience, not a gate: CI remains the authority, and a green run here is
evidence, not a substitute.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")

# Steps that cannot run outside the runner (they need the network, a token, or a
# deploy target). Skipped LOUDLY and counted, because a silent skip is how a
# runner like this starts reporting on less than it claims.
# A step that writes to a runner-provided file handle, or that interpolates a
# ${{ }} expression the runner resolves before bash ever sees it, CANNOT run here
# — not "fails here", cannot run. monthly-backup.yml reported two RED steps on
# `GITHUB_OUTPUT: unbound variable` and a `${{ steps.build.outputs.date }}` that
# bash read as a bad substitution; both are this runner's absence, not a defect
# in the repository, and a red that means "not applicable" is the permanently-red
# check [R-ENF-02] forbids. They are skipped LOUDLY, like every other skip.
CANNOT_RUN_LOCALLY = ("actions/", "deploy", "upload-artifact", "peaceiris",
                      "GITHUB_TOKEN", "gh api", "curl ",
                      "${{", "GITHUB_OUTPUT", "GITHUB_ENV", "GITHUB_STEP_SUMMARY")

# A CI STEP ASSUMES A DISPOSABLE RUNNER, AND THIS ONE IS NOT DISPOSABLE.
#
# The first version of this script had a --all mode that ran every workflow's
# steps against the live working tree. It got as far as a workflow that rebases
# and auto-commits before it was stopped: the checkout was left mid-rebase on a
# detached HEAD, engine/valuation_calibration/ was emptied on disk, and an
# unrelated auto-refresh commit swept an uncommitted file in under a message that
# described something else entirely. Nothing was lost — every commit was already
# on the remote, which is the only reason this is an anecdote rather than an
# incident — but that was luck about push timing, not a property of the design.
#
# So: any step that could mutate the repository is REFUSED rather than run. The
# list is of VERBS, not of workflows, because a new workflow is written without
# anyone thinking of this file. --all is gone with it: a runner that executes
# arbitrary committed shell against a working tree it does not own is a footgun
# whose safe configuration nobody can remember.
MUTATES_THE_REPO = (
    "git commit", "git push", "git rebase", "git merge", "git reset",
    "git checkout", "git switch", "git cherry-pick", "git apply", "git am",
    "git clean", "git stash", "git tag", "git branch", "git rm", "git add",
    "auto_refresh", "publish_site", "rm -rf", "mv ",
)


def steps(path):
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    for jobname, job in (doc.get("jobs") or {}).items():
        for st in (job.get("steps") or []):
            if "run" in st:
                yield jobname, st.get("name") or "(unnamed)", st["run"], st.get("if")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow", nargs="?", default="study-provenance.yml",
                    help="one workflow file. There is deliberately no --all: see "
                         "MUTATES_THE_REPO above.")
    a = ap.parse_args()
    files = [os.path.join(WORKFLOWS, a.workflow)]

    red, green, skipped = [], 0, []
    for f in files:
        if not os.path.exists(f):
            print("FAIL — no such workflow: %s" % f)
            return 1
        for job, name, script, cond in steps(f):
            label = "%s / %s" % (os.path.basename(f), name)
            # A CONDITIONAL STEP IS NOT UNCONDITIONALLY PART OF THE RUN, and this
            # runner cannot evaluate GitHub's expression language. Running one
            # anyway grades a branch CI would not have taken: testahil-calibration's
            # two failure handlers (`if: ...exit_code != '0'`) both end in `exit 1`,
            # so they reported RED on a repository with no error file to their name,
            # while deploy-pages' retry sleeps reported GREEN and inflated the count.
            # Every gate in these workflows is unconditional; the conditional ones
            # are failure handlers and retry pauses. Skipped LOUDLY, never evaluated.
            if cond is not None:
                skipped.append((label, "conditional (if: %s) — not evaluable outside "
                                       "the runner" % str(cond)[:60]))
                continue
            mut = [t for t in MUTATES_THE_REPO if t in script]
            if mut:
                skipped.append((label, "REFUSED — would mutate this checkout (%s). "
                                       "A CI step assumes a disposable runner; "
                                       "this tree is not one." % ", ".join(mut[:3])))
                continue
            if any(t in script for t in CANNOT_RUN_LOCALLY):
                skipped.append((label, "needs the runner (network, token or deploy)"))
                continue
            r = subprocess.run(["bash", "-e", "-c", script], cwd=ROOT,
                               capture_output=True, text=True, timeout=1800)
            if r.returncode == 0:
                green += 1
                print("  GREEN  %s" % label[:90])
            else:
                red.append((label, (r.stdout + r.stderr).strip().splitlines()[-6:]))
                print("  RED    %s   exit %d" % (label[:90], r.returncode))

    print("\nran %d steps from %d workflow(s): %d green, %d red, %d skipped"
          % (green + len(red), len(files), green, len(red), len(skipped)))
    for label, why in skipped:
        print("  skipped  %-60s %s" % (label[:60], why))
    for label, tail in red:
        print("\nRED — %s" % label)
        for line in tail:
            print("     " + line[:160])
    if red:
        print("\nCI would be red. This ran CI's OWN step list, so a green sweep of "
              "the check scripts alone is not the same claim.")
        return 1
    if green == 0:
        # [R-ENF-04]: an empty result is not a clean result. A workflow whose every
        # step is runner-only ran NOTHING here, and saying "every step passes" of a
        # population of zero is the absent answer wearing the costume of a clean one.
        print("\nNOTHING RAN — every step is runner-only, so this workflow is "
              "UNCHECKED here, not green.")
        return 0
    print("\nOK — every locally-runnable CI step passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
