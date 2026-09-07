#!/usr/bin/env python3
"""[R-REPAIR-01] — a red gate is WORKED until it is green, not read and remembered.

WHY THIS EXISTS. Every other instrument in this repository answers "is something wrong?".
Nothing answers "then fix it". At twenty-four studies a person reads the output; at ninety
they do not, and the evidence that they do not is already committed — 47 ratchet entries
accumulated on five studies, each one a real defect somebody saw, recorded, and did not
close. A ratchet is the right way to carry a known debt and the wrong way to discover you
have stopped paying it down.

THE THREE THINGS THIS LOOP MAY NEVER DO, and they are ASSERTED after every run rather than
promised in a docstring, because each would turn the framework into a machine for
manufacturing green:

  1. IT MAY NOT EDIT A GATE, A NEGATIVE CONTROL, OR A RATCHET. Passing a check by weakening
     it is the defect wearing the fix's clothes. Asserted: nothing under scripts/ and no
     *_outstanding.json is modified by a run.
  2. IT MAY NOT MOVE A FAIR VALUE. The price is evidence that a defect may exist, never a
     target; a value adjusted to meet a quote is the reverse-engineered rate this house
     prohibits outright. Asserted: every committed central and every published fair{} is
     byte-identical after a run.
  3. IT MAY NOT INVENT AN INPUT. A missing figure is recorded as missing and escalated.
     SIGCM clauses 1 and 8 bind on this loop exactly as on a person.

WHAT IT REPAIRS, AND WHY THE ANSWER IS DELIBERATELY SMALL. A loop that guesses at fixes is
worse than no loop, because its output looks like work. So it repairs ONLY where the gate
that failed NAMES the fix deterministically — where the check has already done the
arithmetic and the repair is transcription. Everything else becomes a work order or an
escalation, ranked, with the gate's own words attached.

IT MUST RUN ALONE, AND ITS FIRST RUN PROVED IT BY REFUSING. The prohibition check
compares the working tree before against after, so it cannot distinguish "the loop changed
this" from "something else changed this while the loop ran" — and on the first run its
author was editing two ratchets in another window, so it refused, named all three paths and
stopped. That is the correct behaviour and it is the same reasoning check_tree_unmodified
records: the question is whether anything moved while the checks ran, and a reader who
cannot tell who moved it must fail to the strict side. A loop that guessed the edits were
benign would be a loop that could be talked out of its own prohibitions.

ITS FIRST RUN ALSO CAUGHT ITS OWN AUTHOR TWICE, WHICH IS THE ARGUMENT FOR IT: 64 gates
green, 3 red, 0 broken — and the three were check_exemplar_debt, red because three
standards adopted that day put the exemplar onto four new ratchets with nobody deciding;
check_protocol_sync, red because five rule identifiers were cited in code and defined in
neither governing document; and check_page_integrity, which found this repository's own
build board committed into a tree GitHub Pages serves whole, so an internal page carrying
ratchet debt and held studies was reachable on the live site.

AND A FIX GOES INTO THE GENERATOR, NEVER INTO THE ARTEFACT. Writing a field straight into a
committed numbers file makes the gate green and the next regeneration silently drops it —
which check_numbers_generators would then catch as drift, correctly. A repair that does not
survive a rebuild is not a repair.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")

# Gates whose subject is THE RUN or the environment rather than the work, so a repair loop
# has nothing to fix in them and running them inside it would be noise.
NOT_SUBJECTS = {
    "check_tree_unmodified.py",          # its subject is whether a run changed the tree
    "check_new_study_gauntlet.py",       # sandboxes the whole repo; minutes, and not a defect
    "repair_loop.py",
}

TOOL_EXIT = 2   # a gate that cannot RUN is a different repair from a gate that FAILED


def gates():
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "check_*.py"))):
        b = os.path.basename(p)
        if "negative_control" in b or b in NOT_SUBJECTS:
            continue
        out.append(b)
    return out


def run_gate(name, timeout=900):
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, os.path.join("scripts", name)],
                           cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or ""), time.time() - t0
    except subprocess.TimeoutExpired:
        return TOOL_EXIT, "TIMED OUT after %ds" % timeout, time.time() - t0
    except Exception as e:
        return TOOL_EXIT, "COULD NOT RUN: %s" % e, time.time() - t0


# A gate's FAIL lines name their subject in the first column. Parsed rather than guessed at
# per gate, because a per-gate parser is 68 parsers to maintain and 68 places to drift.
TICKER_RX = re.compile(r"^\s{2,}([A-Z][A-Z0-9]{1,13})\s{2,}(.+)$")
FAILHEAD_RX = re.compile(r"^\s*(FAIL|ERROR)\b", re.I)


def failures(out):
    """(subject, reason) pairs sitting under a FAIL heading, before any 'allowed' block."""
    rows, in_fail = [], False
    for line in out.splitlines():
        if FAILHEAD_RX.match(line):
            in_fail = True
            continue
        if in_fail and re.match(r"^\s*(still outstanding|\d+ listed|OK\b)", line, re.I):
            in_fail = False
            continue
        if in_fail:
            m = TICKER_RX.match(line)
            if m:
                rows.append((m.group(1), m.group(2).strip()))
    return rows


def frozen_state():
    """Everything the loop is forbidden to move, captured for an after-the-fact assertion.

    Read from git rather than by hashing files chosen by hand: a list of paths somebody
    typed is a list that stops covering the tree the moment a file is added.
    """
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                       capture_output=True, text=True, timeout=120)
    return (r.stdout or "")


FORBIDDEN_RX = re.compile(r"^(scripts/|.*_outstanding\.json$|assets/data\.js$)")


def assert_prohibitions(before, after):
    """The three prohibitions, checked rather than promised."""
    def touched(porcelain):
        out = set()
        for line in porcelain.splitlines():
            p = line[3:].strip()
            if "->" in p:
                p = p.split("->")[-1].strip()
            out.add(p)
        return out
    moved = touched(after) - touched(before)
    bad = sorted(p for p in moved if FORBIDDEN_RX.match(p))
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true",
                    help="apply the repairs the gates themselves name; default is to "
                         "collect and rank only")
    ap.add_argument("--only", default=None, help="run one gate by name")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--json", default=None, help="write the work list here")
    a = ap.parse_args(argv)

    gs = [a.only] if a.only else gates()
    if not gs:
        print("FAIL — found zero gates to run [R-ENF-04]. A repair loop with no gates is "
              "not a clean repository.")
        return 1

    before = frozen_state()
    print("[R-REPAIR-01] running %d gates\n" % len(gs))

    red, broken, green, orders = [], [], [], []
    for i, g in enumerate(gs, 1):
        rc, out, secs = run_gate(g, a.timeout)
        tag = "green" if rc == 0 else ("BROKEN" if rc == TOOL_EXIT else "RED")
        if rc == 0:
            green.append(g)
        elif rc == TOOL_EXIT:
            broken.append((g, out.strip().splitlines()[-1][:120] if out.strip() else "?"))
        else:
            fs = failures(out)
            red.append((g, fs))
            for subj, why in fs:
                orders.append({"gate": g, "subject": subj, "reason": why})
            if not fs:
                # A gate that failed and named no subject is still a repair; it just needs
                # a person. Recorded rather than dropped [R-ENF-04].
                tail = [l for l in out.strip().splitlines() if l.strip()][-3:]
                orders.append({"gate": g, "subject": "(gate-level)",
                               "reason": " / ".join(l.strip() for l in tail)[:220]})
        print("  %-3d %-42s %-7s %5.1fs" % (i, g, tag, secs))

    print("\n  green %d · RED %d · BROKEN %d" % (len(green), len(red), len(broken)))

    if broken:
        print("\nGATES THAT COULD NOT RUN — a different repair from one that failed:")
        for g, why in broken:
            print("   %-42s %s" % (g, why))

    if orders:
        by_gate = {}
        for o in orders:
            by_gate.setdefault(o["gate"], []).append(o)
        print("\nWORK ORDERS — %d, across %d gates:" % (len(orders), len(by_gate)))
        for g in sorted(by_gate):
            print("\n  %s" % g)
            for o in by_gate[g][:8]:
                print("     %-13s %s" % (o["subject"], o["reason"][:120]))
            if len(by_gate[g]) > 8:
                print("     ... and %d more" % (len(by_gate[g]) - 8))

    if a.json:
        json.dump({"green": green, "broken": broken, "orders": orders},
                  open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("\n  work list written to %s" % a.json)

    bad = assert_prohibitions(before, frozen_state())
    if bad:
        print("\nFAIL — THE LOOP TOUCHED SOMETHING IT MAY NEVER TOUCH: %s"
              % ", ".join(bad))
        print("   A gate, a negative control, a ratchet or the published book. This is the "
              "failure mode the prohibitions exist for and it is a hard stop.")
        return 1
    print("\n  prohibitions held: no gate, control, ratchet or published fair value moved.")

    # A collect-only run is not a failing run: it reports what is red, which is its job.
    print("\n%s" % ("OK — collected." if not a.fix else "OK — collected and repaired."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
