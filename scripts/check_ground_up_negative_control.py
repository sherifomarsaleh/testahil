#!/usr/bin/env python3
"""Negative control for check_ground_up.py.

ELEVEN CONDITIONS, SEVEN RED AND FOUR CLEAN. The clean half carries the two things a correct
study looks like and the two the first draft got wrong: STC's real driver lines must PASS
when the assertion is actually run, and a record NESTED under `gates/` must be found rather
than reported absent — the first draft read only the top level and told AMOC and EGCH they
commit no record at all, which is the wrong reason stated confidently.

The defects are lifted from real records at run time; every mutation asserts it landed;
nothing is written into the real tree.
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


def real_lines():
    d = json.load(open(os.path.join(ENGINE, "stc_study", "study_numbers.json"),
                       encoding="utf-8"))
    v = d.get("driver_lines")
    if not v:
        raise SystemExit("control cannot run: STC commits no driver_lines")
    return copy.deepcopy(v)


def build(tmp, docs, bad, unread):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    eng = os.path.join(repo, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_ground_up.py"),
                os.path.join(repo, "scripts", "check_ground_up.py"))
    for m in ("research_protocol.py", "lessons_register.py", "ratchet_shape.py",
              "asset_base.py", "macro_path.py", "cost_of_capital.py",
              "terminal_value.py", "numbers_generators.py", "research_sweep.py"):
        s = os.path.join(ENGINE, m)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(eng, m))
    for sub in ("macro_paths",):
        s = os.path.join(ENGINE, sub)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(eng, sub))
    for tk, doc in docs.items():
        d = os.path.join(eng, "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w",
                            encoding="utf-8"), indent=1, default=float)
    json.dump({"outstanding": bad, "unreadable": unread},
              open(os.path.join(eng, "build_depth_audit", "ground_up_outstanding.json"),
                   "w", encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable, os.path.join(repo, "scripts",
                                                     "check_ground_up.py")],
                       capture_output=True, text=True, cwd=repo, timeout=180)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, docs, bad, unread, expect_red, landed, results):
    tmp = tempfile.mkdtemp(prefix="gu_nc_")
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


def main():
    r = []
    L = real_lines()
    GOOD = {"driver_lines": L}
    SUMMARY = {"gates": {"ground_up": {"ticker": "X", "lines": 5,
                                       "share_by_level": {"unit": 1.0}, "unit_share": 1.0}}}

    # ---------- RED ----------
    short = copy.deepcopy(L)
    short = short[:-1]
    case("1 driver lines that do not cover 100% of revenue",
         {"AAA": {"driver_lines": short}}, {}, {}, True,
         lambda r_: (abs(sum(x["share_of_revenue"] for x in short) - 1.0) > 0.01,
                     "the shares still sum to one"), r)

    unit_bad = copy.deepcopy(L)
    for x in unit_bad:
        x["level"], x["unit_source"] = "unit", None
    case("2 a line claiming a disclosed-unit build and naming no source",
         {"BBB": {"driver_lines": unit_bad}}, {}, {}, True,
         lambda r_: (all(x["level"] == "unit" and not x["unit_source"] for x in unit_bad),
                     "the unit sources survived"), r)

    nogap = copy.deepcopy(L)
    for x in nogap:
        x["level"], x["gap_note"] = "topdown", None
    case("3 a coarser build that goes quiet about the gap",
         {"CCC": {"driver_lines": nogap}}, {}, {}, True,
         lambda r_: (all(x["level"] == "topdown" and not x["gap_note"] for x in nogap),
                     "the gap notes survived"), r)

    nocost = copy.deepcopy(L)
    for x in nocost:
        x["cost_basis"] = None
    case("4b a line that names how revenue was built and nothing about cost",
         {"HHH": {"driver_lines": nocost}}, {}, {}, True,
         lambda r_: (all(not x.get("cost_basis") for x in nocost),
                     "the cost bases survived"), r)

    case("4 a record that is only the assertion's OUTPUT, nested under gates/",
         {"DDD": SUMMARY}, {}, {}, True,
         lambda r_: ("share_by_level" in json.dumps(SUMMARY)
                     and "driver_lines" not in json.dumps(SUMMARY),
                     "the fixture is not summary-only"), r)

    case("5 ZERO study directories [R-ENF-04]",
         {}, {}, {}, True,
         lambda r_: (not glob.glob(os.path.join(r_, "engine", "*_study")),
                     "directories present"), r)

    case("6 a study MOVED between the two groups",
         {"AAA": {"driver_lines": short}}, {}, {"AAA": "seeded"}, True,
         lambda r_: (abs(sum(x["share_of_revenue"] for x in short) - 1.0) > 0.01,
                     "the shares still sum to one"), r)

    # ---------- CLEAN ----------
    case("7 STC's real driver lines, run rather than counted",
         {"EEE": GOOD}, {}, {}, False,
         lambda r_: (len(L) > 1 and "level" in L[0], "the fixture is not driver lines"), r)

    case("8 the same lines nested under gates/, which must be FOUND",
         {"FFF": {"gates": {"driver_lines": copy.deepcopy(L)}}}, {}, {}, False,
         lambda r_: (len(L) > 1, "the fixture is not driver lines"), r)

    case("9 a summary-only record that is on the unreadable ratchet",
         {"GGG": SUMMARY, "EEE": GOOD}, {}, {"GGG": "seeded"}, False,
         lambda r_: ("share_by_level" in json.dumps(SUMMARY),
                     "the fixture is not summary-only"), r)

    case("10 failing lines that are on the failing ratchet",
         {"AAA": {"driver_lines": short}, "EEE": GOOD}, {"AAA": "seeded"}, {}, False,
         lambda r_: (abs(sum(x["share_of_revenue"] for x in short) - 1.0) > 0.01,
                     "the shares still sum to one"), r)

    print("cases run: %d (declared %d)" % (CASES, CASES))
    if r:
        for n, why in r:
            print("  FAIL  %s\n        %s" % (n, why))
        print("\nFAIL — the gate does not behave as the rule says.")
        return 1
    print("OK — 7 red conditions fire, 4 clean conditions do not.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
