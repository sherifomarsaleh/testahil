#!/usr/bin/env python3
"""Run only the gates that touch what you changed, BEFORE you commit.

WHY THIS EXISTS, measured on 14-09-2026. Publishing SWDY's dissent link took three
failed publish attempts. Two were ordinary mistakes — a new gate that read
assets/data.js by regular expression where the repository requires
engine/site_data.py, and a new gate registered in none of the three lists the
new-study gauntlet keeps. Both are detectable in about a second. Both were found
instead by a twenty-minute recorded gate run, after a commit, inside a publish.

THE COST OF A WRONG GUESS SET THE PACE OF THE WORK. In a repository where a
mistake costs seconds, exploring by doing is cheap and correct. Here the full gate
set takes 20-25 minutes and the record is invalidated by every commit, so the same
habit costs an hour to learn what a minute would have taught. That is not a
discipline problem to be promised away; it is a feedback loop to be shortened.

WHAT THIS IS NOT. It is not a replacement for the recorded run and it never
reports "green". CI remains the authority, the recorded run remains what the
publish block reads, and this says one thing only: of the gates that plausibly
touch your changes, here is what passes right now.

WHAT IT REFUSES TO DO. It will not report clean over files it has no rule for.
Every changed path that matches no rule is NAMED, because a check that quietly
examines nothing reads exactly like one that examined everything and found nothing
[R-ENF-04] — which is the failure this repository keeps closing, and the failure a
"quick check" is most likely to reintroduce.

    python3 scripts/preflight.py              # working tree vs HEAD
    python3 scripts/preflight.py --since-main # everything since origin/main
    python3 scripts/preflight.py --list       # what it would run, and why
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import run_ci_gates  # noqa: E402  — CI's own step list, never a second copy of it

WORKFLOWS = run_ci_gates.WORKFLOWS

# CHANGED PATH -> the gates that have something to say about it.
#
# The VALUES are substrings matched against a step's actual shell command, so a
# rule cannot name a gate that does not run in CI: if the workflow stops running
# it, the rule selects nothing and the completeness report below says so.
#
# THIS TABLE IS HAND-MAINTAINED AND WILL GO STALE. That is survivable only because
# an unmatched file is reported rather than passed, so the table failing to grow
# makes this louder rather than quieter.
RULES: list[tuple[str, list[str], str]] = [
    (r"^scripts/check_.*\.py$",
     ["check_site_data_reader.py", "check_new_study_gauntlet.py"],
     "a new or edited gate must not read data.js by regex, and must be registered "
     "in exactly one of the gauntlet's three lists"),
    (r"^(assets|legacy/assets)/data\.js$",
     ["check_fv_vintages.py", "check_data_freshness.py", "check_dissent_published.py"],
     "the vintage archive, the freshness gate and the dissent link all read data.js"),
    (r"^(assets|legacy/assets)/.*\.js$",
     ["check_legacy_assets_sync.py"],
     "assets/ and legacy/assets/ are mirrors and drift silently"),
    (r"^engine/(Standing_Research_Protocol|PROJECT_INSTRUCTIONS_).*\.md$",
     ["check_protocol_sync.py"],
     "both governing documents must carry the same rules and the same stamp"),
    (r"^engine/[a-z0-9]+_study/MARKET_DISSENT_.*\.md$",
     ["check_dissent_published.py"],
     "a filed case must be reachable from its ticker page"),
    (r"^engine/[a-z0-9]+_study/.*\.json$",
     ["check_output_sanity.py", "check_terminal_spread.py"],
     "a study's committed figures are read by the sanity and terminal gates"),
    (r"^engine/escalations\.json$",
     ["check_escalations.py"],
     "the escalation register has its own gate"),
    (r".*/study/index\.html$|^legacy/.*\.html$",
     ["check_page_integrity.py"],
     "ticker pages are template plus per-ticker edits, and integrity diffs them"),
    # CI HAS NO check_imports.py. It does this INLINE — python3 -c "import
    # wacc_builder, research_protocol, ..." — and the first draft of this table named
    # a script that does not exist, which the completeness report below caught on its
    # own first run. The substring matches the real step's command instead.
    (r"^engine/.*\.py$|^scripts/.*\.py$",
     ["import wacc_builder"],
     "a module that parses but will not import is the bug that reached main once"),
]


def changed(since_main: bool) -> list[str]:
    """Every path this working tree changes, including untracked files."""
    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, text=True,
                              capture_output=True).stdout.splitlines()
    if since_main:
        subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=ROOT,
                       capture_output=True)
        paths = git("diff", "--name-only", "origin/main...HEAD")
    else:
        paths = git("diff", "--name-only", "HEAD")
    paths += git("ls-files", "--others", "--exclude-standard")
    return sorted({p.strip() for p in paths if p.strip()})


def select(paths: list[str]):
    """(wanted-substrings, why-by-substring, files matching no rule)."""
    wanted: set[str] = set()
    why: dict[str, set[str]] = {}
    matched: set[str] = set()
    for p in paths:
        for pattern, gates, reason in RULES:
            if re.match(pattern, p):
                matched.add(p)
                for g in gates:
                    wanted.add(g)
                    why.setdefault(g, set()).add(reason)
    return wanted, why, [p for p in paths if p not in matched]


def ci_steps():
    """Every step CI runs, as (name, command)."""
    out = []
    for fn in sorted(os.listdir(WORKFLOWS)):
        if not fn.endswith((".yml", ".yaml")):
            continue
        for _job, name, run, _if in run_ci_gates.steps(os.path.join(WORKFLOWS, fn)):
            out.append((name, run))
    return out


def _report_unmatched(unmatched: list[str]) -> None:
    if not unmatched:
        return
    print("\nNO RULE COVERS %d CHANGED FILE(S) — this preflight says NOTHING about "
          "them:" % len(unmatched))
    for p in unmatched[:12]:
        print("    %s" % p)
    if len(unmatched) > 12:
        print("    ... and %d more" % (len(unmatched) - 12))
    if any(p.startswith(".github/workflows/") for p in unmatched):
        print("    A CHANGED WORKFLOW CHANGES THE POPULATION ITSELF. Nothing short of "
              "the full recorded run is evidence about it.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since-main", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--timeout", type=int, default=180)
    a = ap.parse_args()

    paths = changed(a.since_main)
    if not paths:
        print("PREFLIGHT — nothing changed against %s. Nothing to check, and that is "
              "not the same as clean." % ("origin/main" if a.since_main else "HEAD"))
        return 0

    wanted, why, unmatched = select(paths)
    allsteps = ci_steps()
    chosen = [(n, c) for n, c in allsteps if any(w in c for w in wanted)]

    print("PREFLIGHT — the gates that touch what you changed")
    print("  changed files      : %d" % len(paths))
    print("  CI steps in total  : %d" % len(allsteps))
    print("  selected to run    : %d" % len(chosen))
    for g in sorted(wanted):
        if not any(g in c for _n, c in allsteps):
            print("  NOT IN CI          : %s — a rule names a gate the workflow does "
                  "not run" % g)
    if a.list:
        for n, _c in chosen:
            print("    would run  %s" % n)
        for g in sorted(why):
            print("    because    %s" % "; ".join(sorted(why[g])))
        # --list USED TO STAY SILENT ABOUT UNMATCHED FILES while the run path named
        # them, so the mode most likely to be read quickly was the one that told the
        # smaller truth. Caught on this script's own first run against itself: it
        # edited a workflow, matched no rule, and said nothing about it.
        _report_unmatched(unmatched)
        return 0

    rc, failed, slow = 0, [], []
    for n, cmd in chosen:
        t0 = time.time()
        try:
            p = subprocess.run(cmd, cwd=ROOT, shell=True, text=True,
                               capture_output=True, timeout=a.timeout)
            ok = p.returncode == 0
        except subprocess.TimeoutExpired:
            slow.append(n)
            print("  SLOW  %-52s over %ds — NOT ESTABLISHED" % (n[:52], a.timeout))
            continue
        print("  %-4s  %-52s %5.1fs" % ("ok" if ok else "FAIL", n[:52],
                                        time.time() - t0))
        if not ok:
            failed.append((n, (p.stdout or "") + (p.stderr or "")))
            rc = 1

    for n, out in failed:
        print("\n--- %s ---" % n)
        print("\n".join(out.strip().splitlines()[-12:]))

    _report_unmatched(unmatched)
    print()
    if slow:
        print("%d gate(s) ran past the timeout and were NOT established: %s"
              % (len(slow), ", ".join(slow)))

    print("\n%s — %d of %d CI steps ran. THIS IS NOT A GREEN TREE: only the recorded "
          "run over every gate is that."
          % ("FAIL" if rc else "clear so far", len(chosen), len(allsteps)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
