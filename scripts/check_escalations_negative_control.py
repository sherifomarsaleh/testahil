#!/usr/bin/env python3
"""Negative control for [R-IND-01]. A check nobody has seen fail is not evidence.

Every condition the gate claims to refuse is reinjected here and asserted RED, and
the legitimate constructions are asserted GREEN — because a gate that reddens on an
honest escalation teaches the operator to stop registering them, which is worse
than the failure it was written for.

THE HEADLINE CASE IS THE REAL ONE: the 3 September 2026 re-ask, rebuilt exactly as
it would have been written — an open entry for a series the principal had already
supplied — must go RED on this gate. That is the whole rule in one case.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "scripts", "check_escalations.py")
REG = os.path.join(ROOT, "engine", "escalations.json")

GOOD = {
    "key": "NC-example",
    "opened": "2026-09-03",
    "cls": "missing_data",
    "question": "a figure that cannot be obtained from any route",
    "routes": [
        {"route": "the issuer's own investor-relations archive", "when": "2026-09-03",
         "outcome": "connect rejected at the proxy", "rerun": True},
        {"route": "the regulator's filing portal", "when": "2026-09-03",
         "outcome": "404 for every document id tried", "rerun": False},
        {"route": "a headless browser against the JavaScript-rendered aggregator",
         "when": "2026-09-03", "outcome": "renders, but publishes no history before 2019",
         "rerun": False},
    ],
    "refs_searched": 22,
    "why_only_the_principal": "an official filing the principal can request directly",
    "done_meanwhile": "every other period was sourced and the window shortened",
    "default_if_no_answer": "drop the period and shorten the window",
    "default_date": "2099-01-01",
    "status": "open",
    "resolves_when": {"file": "engine/escalations.json",
                      "must_contain": "NC-marker-that-does-not-appear"},
}


def run(entries) -> tuple:
    """Run the gate against a temporary register, restoring the real one after."""
    backup = tempfile.mktemp(suffix=".json")
    shutil.copy(REG, backup)
    try:
        json.dump({"_": "negative control", "entries": entries},
                  open(REG, "w", encoding="utf-8"), indent=1)
        r = subprocess.run([sys.executable, GATE], cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        tail = (r.stdout + r.stderr).strip().splitlines()
        return r.returncode, (tail[-1] if tail else "")
    finally:
        shutil.copy(backup, REG)
        os.unlink(backup)


def case(name, entries, expect_red, results):
    rc, last = run(entries)
    red = rc != 0
    results.append((name, red == expect_red, rc, last))


def main() -> int:
    results = []

    def broken(mutate):
        e = copy.deepcopy(GOOD)
        mutate(e)
        return [e]

    # --- the case the rule was written for -----------------------------------
    def m_the_reask(e):
        # 3 September 2026, rebuilt: an OPEN escalation for the sovereign and policy
        # series, whose answer was already on a live ref when it was written.
        e["key"] = "EG-sovereign-and-policy-rates-2013-2023"
        e["status"] = "open"
        e["resolves_when"] = {"file": "engine/macro_history/EG.json",
                              "must_contain": "resolved_03_09_2026"}

    def m_one_ref(e):
        e["refs_searched"] = 1

    def m_two_routes(e):
        e["routes"] = e["routes"][:2]

    def m_no_rerun(e):
        for r in e["routes"]:
            r["rerun"] = False

    def m_route_no_outcome(e):
        e["routes"][0].pop("outcome")

    def m_no_default(e):
        e["default_if_no_answer"] = "  "

    def m_past_default(e):
        e["default_date"] = "2020-01-01"

    def m_bad_class(e):
        e["cls"] = "just_checking"

    def m_no_question(e):
        e["question"] = ""

    def m_resolved_no_file(e):
        e["status"] = "resolved"
        e.pop("answer_written_to", None)

    def m_resolved_not_written(e):
        e["status"] = "resolved"
        e["answer_written_to"] = "engine/macro_history/EG.json"
        e["resolves_when"] = {"file": "engine/macro_history/EG.json",
                              "must_contain": "a marker nobody ever wrote"}

    def m_bad_status(e):
        e["status"] = "pending"

    for nm, mut in (
        ("THE RE-ASK: open, already answered on a live ref", m_the_reask),
        ("searched one ref", m_one_ref),
        ("two routes on a missing_data escalation", m_two_routes),
        ("no route was re-run", m_no_rerun),
        ("a route with no outcome", m_route_no_outcome),
        ("no default if no answer comes", m_no_default),
        ("open past its own default date", m_past_default),
        ("an unregistered class", m_bad_class),
        ("no question", m_no_question),
        ("resolved, naming no file", m_resolved_no_file),
        ("resolved, but the answer is nowhere", m_resolved_not_written),
        ("a status that is neither open nor resolved", m_bad_status),
    ):
        case(nm, broken(mut), True, results)

    # duplicates
    def dup():
        a, b = copy.deepcopy(GOOD), copy.deepcopy(GOOD)
        return [a, b]
    case("the same question asked twice", dup(), True, results)

    # an unreadable register is not an empty one
    case("register with no entries list", None, True, results)

    # --- the clean cases -----------------------------------------------------
    case("clean: a properly exhausted open escalation", [copy.deepcopy(GOOD)],
         False, results)

    def c_resolved():
        e = copy.deepcopy(GOOD)
        e["status"] = "resolved"
        e["answer_written_to"] = "engine/macro_history/EG.json"
        e["resolves_when"] = {"file": "engine/macro_history/EG.json",
                              "must_contain": "resolved_03_09_2026"}
        return [e]
    case("clean: resolved, with the answer written down", c_resolved(), False, results)

    def c_instruction():
        e = copy.deepcopy(GOOD)
        e["key"] = "NC-a-decision-reserved-to-the-principal"
        e["cls"] = "instruction"
        e["routes"] = [{"route": "the plan and both governing documents",
                        "when": "2026-09-03",
                        "outcome": "neither decides it; it is a standing-rule change",
                        "rerun": True}]
        return [e]
    case("clean: an instruction class needs no route ladder", c_instruction(),
         False, results)

    # an empty register is a legitimate state — nothing has been escalated
    case("clean: an empty register", [], False, results)

    print("\nNEGATIVE CONTROL — scripts/check_escalations.py")
    for name, good, rc, last in results:
        print("  %-48s %-4s exit %d   %s" % (name[:48], "ok" if good else "MISS",
                                             rc, last[:60]))
    bad = [n for n, good, _, _ in results if not good]
    if bad:
        print("\nFAILED on: %s" % ", ".join(bad))
        return 1
    print("\nAll %d conditions behave as claimed." % len(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
