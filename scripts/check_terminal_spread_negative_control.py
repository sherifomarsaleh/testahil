#!/usr/bin/env python3
"""Negative control for check_terminal_spread.py.

ELEVEN CONDITIONS, SIX RED AND FIVE CLEAN. The clean half carries the discriminations this
gate has to make and that a cruder one would get wrong: a terminal earning BELOW its cost
of capital while reinvesting NOTHING must not fire — that is MODON, and it is not a defect,
because a spread nothing is invested at compounds nothing — and a terminal that declares
the spread with a mechanism must not fire either.

The defects are lifted from the real records at run time rather than transcribed, and every
mutation ASSERTS THAT IT LANDED. NOTHING IS WRITTEN INTO THE REAL TREE: fixtures are built
inside a temporary directory and the gate is pointed at it, so there is no undo to run.
"""
from __future__ import annotations

import copy
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "engine")
CASES = 11

# THE TALLY IS A SHARED INSTRUMENT, NOT A LINE EACH CONTROL PRINTS FOR ITSELF.
# Six controls here printed the DECLARED CONSTANT twice — "cases run: N
# (declared N)" — which is true whatever ran, and beside it a hand-typed red/clean
# split that had stopped matching. engine/control_tally.py counts what actually
# ran and refuses a count that moved [R-ENF-04].
sys.path.insert(0, ROOT)
from engine.control_tally import Tally          # noqa: E402

T = Tally(CASES, subject="check_terminal_spread.py")


def real(tk):
    for n in ("study_numbers.json", "numbers.json"):
        p = os.path.join(ENGINE, "%s_study" % tk.lower(), n)
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    for p in sorted(glob.glob(os.path.join(ENGINE, "%s_study" % tk.lower(),
                                           "*numbers*.json"))):
        return json.load(open(p, encoding="utf-8"))
    raise SystemExit("control cannot run: %s has no numbers file" % tk)


def build(tmp, docs, bad, unread):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(repo, "engine", "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_terminal_spread.py"),
                os.path.join(repo, "scripts", "check_terminal_spread.py"))
    for tk, doc in docs.items():
        d = os.path.join(repo, "engine", "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w",
                            encoding="utf-8"), indent=1, default=float)
    json.dump({"outstanding": sorted(bad), "unreadable": sorted(unread)},
              open(os.path.join(repo, "engine", "build_depth_audit",
                                "terminal_spread_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable,
                        os.path.join(repo, "scripts", "check_terminal_spread.py")],
                       capture_output=True, text=True, cwd=repo, timeout=120)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, docs, bad, unread, expect_red, landed, results):
    T.case(name, expect_red)
    tmp = tempfile.mkdtemp(prefix="tspread_nc_")
    try:
        repo = build(tmp, docs, bad, unread)
        ok, why = landed(repo)
        if not ok:
            results.append((name, "MUTATION DID NOT LAND: " + why))
            return
        red, out = run(repo)
        if red != expect_red:
            results.append((name, "expected %s, got %s\n%s"
                            % ("RED" if expect_red else "GREEN",
                               "RED" if red else "GREEN", out[-600:])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def flat(doc, key, val):
    d = copy.deepcopy(doc)
    d[key] = val
    return d


def main():
    results = []
    ARCC, PHAR, MODON, SAV = (real(t) for t in ("arcc", "phar", "modon", "savola"))

    def has(doc, k):
        return json.dumps(doc).find('"%s"' % k) >= 0

    # ---------- RED ----------
    case("1 PHAR's undeclared negative spread, exactly as it stands",
         {"AAA": PHAR}, set(), set(), True,
         lambda r: (has(PHAR, "roic_term") and has(PHAR, "reinvest_rate"),
                    "PHAR lacks the terminal fields"), results)

    case("2 ARCC's reinvestment of -191.88 — not a rate",
         {"BBB": ARCC}, set(), set(), True,
         lambda r: (has(ARCC, "reinvestment"), "ARCC lacks a reinvestment figure"), results)

    R_NO_COST = {k: v for k, v in copy.deepcopy(PHAR).items()}
    R_NO_COST = json.loads(json.dumps(R_NO_COST).replace('"wacc_term"', '"wacc_x"'))
    case("3 a terminal that reinvests and commits no cost of capital",
         {"CCC": R_NO_COST}, set(), set(), True,
         lambda r: (not has(R_NO_COST, "wacc_term") and has(R_NO_COST, "reinvest_rate"),
                    "the cost key survived"), results)

    R_NO_RET = json.loads(json.dumps(copy.deepcopy(PHAR)).replace('"roic_term"', '"roic_x"'))
    case("4 a terminal that reinvests and commits no return",
         {"DDD": R_NO_RET}, set(), set(), True,
         lambda r: (not has(R_NO_RET, "roic_term") and has(R_NO_RET, "reinvest_rate"),
                    "the return key survived"), results)

    case("5 ZERO study directories [R-ENF-04]",
         {}, set(), set(), True,
         lambda r: (not glob.glob(os.path.join(r, "engine", "*_study")),
                    "study directories present"), results)

    case("6 a study MOVED between the two groups",
         {"AAA": PHAR}, set(), {"AAA"}, True,
         lambda r: (has(PHAR, "roic_term"), "PHAR lacks the terminal fields"), results)

    # ---------- CLEAN ----------
    case("7 MODON: a negative spread reinvesting NOTHING must not fire",
         {"EEE": MODON, "FFF": SAV}, set(), set(), False,
         lambda r: (not any(k in json.dumps(MODON) for k in
                            ('"reinvest"', '"reinvestment"', '"reinvest_rate"',
                             '"reinvestment_rate"', '"reinvest_term"')),
                    "MODON commits a reinvestment rate after all"), results)

    DECL = copy.deepcopy(PHAR)
    DECL["terminal_spread_reason"] = ("regulated returns are set below the market cost of "
                                      "capital and the licence obliges continued capital "
                                      "programmes; the obligation is disclosed in note 21")
    case("8 the same negative spread, DECLARED with a mechanism",
         {"GGG": DECL}, set(), set(), False,
         lambda r: (bool(DECL.get("terminal_spread_reason")), "no reason set"), results)

    EMPTY = copy.deepcopy(PHAR)
    EMPTY["terminal_spread_reason"] = "   "
    case("9 an EMPTY reason has switched the check off, not declared it",
         {"HHH": EMPTY}, set(), set(), True,
         lambda r: (EMPTY.get("terminal_spread_reason", "x").strip() == "",
                    "the reason is not empty"), results)

    case("10 SAVOLA: reinvesting at a POSITIVE spread must not fire",
         {"III": SAV}, set(), set(), False,
         lambda r: (has(SAV, "reinvest_term") and has(SAV, "roic_term"),
                    "SAVOLA lacks the terminal fields"), results)

    case("11 the same two studies, both on their own ratchet group",
         {"AAA": PHAR, "BBB": ARCC}, {"AAA", "BBB"}, set(), False,
         lambda r: (has(PHAR, "roic_term") and has(ARCC, "reinvestment"),
                    "fixtures missing their fields"), results)

    return T.report(results)


if __name__ == "__main__":
    sys.exit(main())
