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
CANNOT_RUN_LOCALLY = ("actions/", "deploy", "upload-artifact", "peaceiris",
                      "GITHUB_TOKEN", "gh api", "curl ")


def steps(path):
    doc = yaml.safe_load(open(path, encoding="utf-8"))
    for jobname, job in (doc.get("jobs") or {}).items():
        for st in (job.get("steps") or []):
            if "run" in st:
                yield jobname, st.get("name") or "(unnamed)", st["run"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow", nargs="?", default="study-provenance.yml")
    ap.add_argument("--all", action="store_true",
                    help="every workflow, not just the study gates")
    a = ap.parse_args()

    files = (sorted(os.path.join(WORKFLOWS, f) for f in os.listdir(WORKFLOWS)
                    if f.endswith((".yml", ".yaml")))
             if a.all else [os.path.join(WORKFLOWS, a.workflow)])

    red, green, skipped = [], 0, []
    for f in files:
        if not os.path.exists(f):
            print("FAIL — no such workflow: %s" % f)
            return 1
        for job, name, script in steps(f):
            label = "%s / %s" % (os.path.basename(f), name)
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
    print("\nOK — every locally-runnable CI step passes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
