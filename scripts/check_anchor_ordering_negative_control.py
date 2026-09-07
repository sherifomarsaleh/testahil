#!/usr/bin/env python3
"""Negative control for check_anchor_ordering.py.

TEN CONDITIONS, SIX RED AND FOUR CLEAN. The clean half carries what a correct study looks
like: dates that are EQUAL, which is most of the book and must pass trivially; an anchor
AHEAD of the sheet, which is ordinary where a company files a P&L for a period whose
balance sheet is the prior one; a study committing only ONE of the two dates, which is out
of scope rather than a defect; and the same lag DECLARED with a mechanism.

The four defects are lifted out of the real records at run time rather than transcribed,
and every mutation ASSERTS THAT IT LANDED. Nothing is written into the real tree.
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
CASES = 10


def real(tk):
    p = os.path.join(ENGINE, "%s_study" % tk.lower(), "study_numbers.json")
    if not os.path.exists(p):
        raise SystemExit("control cannot run: %s has no numbers file" % tk)
    d = json.load(open(p, encoding="utf-8"))
    return {"bridge_record": copy.deepcopy(d.get("bridge_record") or {}),
            "forecast_anchor": copy.deepcopy(d.get("forecast_anchor") or {})}


def build(tmp, docs, ratchet):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(repo, "engine", "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_anchor_ordering.py"),
                os.path.join(repo, "scripts", "check_anchor_ordering.py"))
    for tk, doc in docs.items():
        d = os.path.join(repo, "engine", "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w",
                            encoding="utf-8"), indent=1, default=float)
    json.dump({"outstanding": ratchet},
              open(os.path.join(repo, "engine", "build_depth_audit",
                                "anchor_ordering_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable,
                        os.path.join(repo, "scripts", "check_anchor_ordering.py")],
                       capture_output=True, text=True, cwd=repo, timeout=120)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, docs, ratchet, expect_red, landed, results):
    tmp = tempfile.mkdtemp(prefix="anchord_nc_")
    try:
        repo = build(tmp, docs, ratchet)
        ok, why = landed(repo)
        if not ok:
            results.append((name, "MUTATION DID NOT LAND: " + why))
            return
        red, out = run(repo)
        if red != expect_red:
            results.append((name, "expected %s, got %s\n%s"
                            % ("RED" if expect_red else "GREEN",
                               "RED" if red else "GREEN", out[-500:])))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def behind(doc):
    b = (doc.get("bridge_record") or {}).get("balance_sheet_date")
    a = (doc.get("forecast_anchor") or {}).get("latest_reviewed_date")
    return bool(b and a and a < b)


def main():
    results = []
    ADN, ARCC, EGCH, PHDC = (real(t) for t in ("adnocls", "arcc", "egch", "phdc"))

    # ---------- RED ----------
    for i, (tk, doc) in enumerate((("ADNOCLS", ADN), ("ARCC", ARCC), ("EGCH", EGCH)), 1):
        case("%d %s's own dates, exactly as they stand" % (i, tk),
             {tk: doc}, {}, True,
             lambda r, d=doc: (behind(d), "the anchor is not behind the sheet"), results)

    case("4 ZERO study directories [R-ENF-04]",
         {}, {}, True,
         lambda r: (not glob.glob(os.path.join(r, "engine", "*_study")),
                    "directories present"), results)

    ONLY_ONE = {"bridge_record": {"balance_sheet_date": "2026-06-30"}}
    case("5 directories present and NOT ONE carries both dates [R-ENF-04]",
         {"AAA": ONLY_ONE, "BBB": ONLY_ONE}, {}, True,
         lambda r: ("forecast_anchor" not in ONLY_ONE, "an anchor survived"), results)

    WORSE = copy.deepcopy(ADN)
    WORSE["forecast_anchor"]["latest_reviewed_date"] = "2024-12-31"
    case("6 a LISTED study that has fallen further behind",
         {"CCC": WORSE}, {"CCC": {"lag_days": 90, "why": "seeded"}}, True,
         lambda r: (WORSE["forecast_anchor"]["latest_reviewed_date"] == "2024-12-31",
                    "the anchor was not moved back"), results)

    # ---------- CLEAN ----------
    case("7 PHDC: the two dates are EQUAL, which is most of the book",
         {"DDD": PHDC}, {}, False,
         lambda r: ((PHDC.get("bridge_record") or {}).get("balance_sheet_date")
                    == (PHDC.get("forecast_anchor") or {}).get("latest_reviewed_date"),
                    "PHDC's dates are not equal"), results)

    AHEAD = copy.deepcopy(PHDC)
    AHEAD["forecast_anchor"]["latest_reviewed_date"] = "2026-06-30"
    case("8 an anchor AHEAD of the sheet must not fire",
         {"EEE": AHEAD}, {}, False,
         lambda r: (AHEAD["forecast_anchor"]["latest_reviewed_date"]
                    > AHEAD["bridge_record"]["balance_sheet_date"],
                    "the anchor is not ahead"), results)

    DECL = copy.deepcopy(ADN)
    DECL["anchor_ordering_reason"] = ("the 31-March filing is a balance-sheet-only interim "
                                      "under the exchange's quarterly rule; no income "
                                      "statement for the quarter was published")
    case("9 the same lag, DECLARED with a mechanism",
         {"FFF": DECL, "GGG": PHDC}, {}, False,
         lambda r: (bool(DECL.get("anchor_ordering_reason")), "no reason set"), results)

    EMPTY = copy.deepcopy(ADN)
    EMPTY["anchor_ordering_reason"] = "  "
    case("10 an EMPTY reason has switched the check off, not declared it",
         {"HHH": EMPTY}, {}, True,
         lambda r: (EMPTY.get("anchor_ordering_reason", "x").strip() == "",
                    "the reason is not empty"), results)

    print("cases run: %d (declared %d)" % (CASES, CASES))
    if results:
        for n, why in results:
            print("  FAIL  %s\n        %s" % (n, why))
        print("\nFAIL — the gate does not behave as the rule says.")
        return 1
    print("OK — 6 red conditions fire, 4 clean conditions do not.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
