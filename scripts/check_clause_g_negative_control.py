#!/usr/bin/env python3
"""Negative control for [R-VCAL-02 CLAUSE THREE]'s clause G.

A check nobody has seen fail is not evidence. Every mutation below ASSERTS THAT IT
LANDED before the clause runs, because this project has four times caught a control
passing a fixture that never injected its condition — a green that proves only that
nothing changed.

IT NEVER WRITES INTO THE REAL TREE [R-ENF-01, 07-09-2026]. The audit file the clause
reads is pointed at a temporary directory; the committed one is never opened for
writing, and that is asserted after every case. A test that mutates production state
and undoes it afterwards is correct exactly as often as it completes.

The CLEAN half is the half that matters here, because the bar is ONE-SIDED by
instruction: a cell far ABOVE its price must NOT fire, and a control that only
proved the red cases would leave that untested.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine", "method_reassessment"))
sys.path.insert(0, os.path.join(ROOT, "engine", "valuation_calibration"))

import criterion3 as C3   # noqa: E402

REAL_AUDIT = C3._audit_path()[0]
assert REAL_AUDIT, "control cannot run: the audit does not resolve"
AUDIT_NAME = os.path.basename(REAL_AUDIT)
CASES = 9


def _cell(tk, origin, gap):
    """A scored cell whose fair value sits `gap` from its price."""
    return {"ticker": tk, "origin": origin, "price": 100.0,
            "fv": 100.0 * (1.0 + gap), "log": 0.0}


def _run(cells, audit_text, tmp):
    """Run the clause with its audit pointed at a temp file, never the real one."""
    p = os.path.join(tmp, AUDIT_NAME)
    if audit_text is None:
        if os.path.exists(p):
            os.remove(p)
    else:
        open(p, "w", encoding="utf-8").write(audit_text)
    real_resolver = C3._audit_path
    C3._audit_path = lambda: ((p, None) if os.path.exists(p)
                              else (None, "no committed audit on %s" % C3.AUDIT_GLOB))
    try:
        return C3.clause_g({"cells": cells})
    finally:
        C3._audit_path = real_resolver


def main():
    before = hashlib.sha256(open(REAL_AUDIT, "rb").read()).hexdigest()
    tmp = tempfile.mkdtemp(prefix="clause_g_nc_")
    ok = True
    ran = 0
    try:
        AUD = "## 1. ARCC 2019 — audited\n## 2. PHDC 2019 — audited\n"

        cases = [
            # --------------------------------------------------------- RED
            ("a breaching cell the audit does not name",
             [_cell("ARCC", 2019, -0.30), _cell("SWDY", 2021, -0.40)], AUD, False,
             lambda c, a: "SWDY 2021" not in a and c[1]["fv"] / c[1]["price"] - 1 < -C3.AUDIT_BAR),
            ("no audit committed at all",
             [_cell("ARCC", 2019, -0.30)], None, False,
             lambda c, a: a is None),
            ("an audit that names nothing",
             [_cell("ARCC", 2019, -0.30)], "# empty\n", False,
             lambda c, a: "ARCC 2019" not in a),
            ("a run that scored no cell — empty is not clean [R-ENF-04]",
             [], AUD, False, lambda c, a: not c),
            ("a cell just past the bar, unnamed",
             [_cell("TMGH", 2020, -0.1001)], AUD, False,
             lambda c, a: "TMGH 2020" not in a),
            # ------------------------------------------------------- CLEAN
            ("every breaching cell named",
             [_cell("ARCC", 2019, -0.30), _cell("PHDC", 2019, -0.55)], AUD, True,
             lambda c, a: all(("%s %d" % (r["ticker"], r["origin"])) in a for r in c)),
            ("a cell far ABOVE its price MUST NOT FIRE — the bar is one-sided",
             [_cell("ARCC", 2019, +2.40)], "# names nothing\n", True,
             lambda c, a: c[0]["fv"] / c[0]["price"] - 1 > 1.0),
            ("a cell exactly AT the bar must not fire",
             [_cell("ARCC", 2019, -0.10)], "# names nothing\n", True,
             lambda c, a: abs((c[0]["fv"] / c[0]["price"] - 1) + 0.10) < 1e-12),
            ("an audit naming a cell that no longer breaches is not an error",
             [_cell("ARCC", 2019, +0.05)], AUD, True,
             lambda c, a: "ARCC 2019" in a and c[0]["fv"] / c[0]["price"] - 1 > 0),
        ]
        assert len(cases) == CASES, "case count moved: %d against a declared %d" % (
            len(cases), CASES)

        for name, cells, audit, expect_met, landed in cases:
            if not landed(cells, audit):
                print("  [FIXTURE DID NOT LAND] %s" % name)
                ok = False
                continue
            met, lines = _run(cells, audit, tmp)
            ran += 1
            got = met is True
            if got != expect_met:
                print("  [WRONG] %-58s expected %s, got %s"
                      % (name, "MET" if expect_met else "NOT MET",
                         "MET" if got else "NOT MET"))
                for l in lines:
                    print("          %s" % l)
                ok = False
            else:
                print("  [ok]    %-58s %s" % (name, "MET" if got else "NOT MET"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    after = hashlib.sha256(open(REAL_AUDIT, "rb").read()).hexdigest()
    if before != after:
        print("  [FAIL] THE CONTROL MODIFIED THE REAL AUDIT FILE")
        ok = False
    else:
        print("  [ok]    the committed audit is byte-identical after the run")

    print()
    print("clause G negative control — %d case(s) run of %d declared, %s"
          % (ran, CASES, "OK" if ok else "FAILED"))
    return 0 if (ok and ran == CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
