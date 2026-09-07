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
CASES = 16

# The closed mechanism list is IMPORTED from the gate rather than copied here: a control
# holding its own copy of a standard stops testing the standard the moment one of them
# moves, which is this repository's own rule about a check that keeps a copy of a key set.
_spec = __import__("importlib.util", fromlist=["util"]).spec_from_file_location(
    "_ca", os.path.join(HERE, "check_anchor_ordering.py"))
ca = __import__("importlib.util", fromlist=["util"]).module_from_spec(_spec)
_spec.loader.exec_module(ca)


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


RAN = []            # what ACTUALLY ran, counted rather than declared


def case(name, docs, ratchet, expect_red, landed, results):
    RAN.append((name, expect_red))
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

    # INVERTED 07-09-2026 rather than deleted, the precedent [R-GAP-01] set when its
    # trigger went two-sided. This case asserted that a bare SENTENCE releases the study,
    # which was correct evidence for the gate as first written and is exactly what the
    # strengthening removed: a reason with no measurement is an assertion, and this rule's
    # own parent says THE MEASUREMENT IS THE CLAUSE THAT DOES THE WORK.
    DECL = copy.deepcopy(ADN)
    DECL["anchor_ordering_reason"] = ("the 31-March filing is a balance-sheet-only interim "
                                      "under the exchange's quarterly rule; no income "
                                      "statement for the quarter was published")
    case("9 a bare SENTENCE no longer releases — it is an assertion, not a measurement",
         {"FFF": DECL, "GGG": PHDC}, {}, True,
         lambda r: (isinstance(DECL.get("anchor_ordering_reason"), str)
                    and DECL["anchor_ordering_reason"].strip() != "", "no reason set"),
         results)

    def declared(later, anchor, **kw):
        d = copy.deepcopy(ADN)
        d["anchor_ordering_reason"] = dict(
            {"reason": "a single reviewed quarter is a point on a seasonal path rather "
                       "than a rate the business runs at",
             "later_period": "1Q2026, reviewed",
             "later_rate": later, "anchor_rate": anchor}, **kw)
        return d

    # THE DECISIVE CLEAN CASE — anchored on the LOWER of the two figures the study holds,
    # so the forecast faces the stricter comparison and the choice cannot be flattering it.
    LOWER = declared(0.3273, 0.2928)
    case("11 anchored on the LOWER of two figures held — the strict side, must stay green",
         {"III": LOWER}, {}, False,
         lambda r: (LOWER["anchor_ordering_reason"]["later_rate"]
                    > LOWER["anchor_ordering_reason"]["anchor_rate"],
                    "the later rate is not the higher one"), results)

    # THE CASE THE RULE EXISTS FOR: two figures held, the HIGHER one adopted as the anchor.
    HIGHER = declared(0.2100, 0.2928)
    case("12 anchored on the HIGHER of two figures held, with no mechanism",
         {"JJJ": HIGHER}, {}, True,
         lambda r: (HIGHER["anchor_ordering_reason"]["later_rate"]
                    < HIGHER["anchor_ordering_reason"]["anchor_rate"],
                    "the later rate is not the lower one"), results)

    OFFLIST = declared(0.2100, 0.2928, mechanism="the quarter looked unrepresentative",
                       mechanism_disclosure="stated in the body")
    case("13 the higher anchor released by a mechanism off the closed list",
         {"KKK": OFFLIST}, {}, True,
         lambda r: (OFFLIST["anchor_ordering_reason"]["mechanism"] not in ca.MECHANISMS,
                    "the mechanism is on the list"), results)

    NODISC = declared(0.2100, 0.2928, mechanism="seasonality", mechanism_disclosure="  ")
    case("14 a mechanism named with no disclosure establishing it from the filings",
         {"LLL": NODISC}, {}, True,
         lambda r: (not NODISC["anchor_ordering_reason"]["mechanism_disclosure"].strip(),
                    "the disclosure is not empty"), results)

    OK_MECH = declared(0.2100, 0.2928, mechanism="seasonality",
                       mechanism_disclosure="the segment note discloses the quarter's "
                                            "dry-docking days against the year's average")
    case("15 the higher anchor released by a mechanism WITH its disclosure",
         {"MMM": OK_MECH}, {}, False,
         lambda r: (OK_MECH["anchor_ordering_reason"]["mechanism"] in ca.MECHANISMS
                    and bool(OK_MECH["anchor_ordering_reason"]["mechanism_disclosure"]
                             .strip()), "the mechanism case was not built"), results)

    # NO measurement at all, only a reason — the shape case 9 used to release on.
    NOMEAS = copy.deepcopy(ADN)
    NOMEAS["anchor_ordering_reason"] = {"reason": "a quarter is not a year"}
    case("9b a dict reason with no rates to read a direction from",
         {"NNN": NOMEAS}, {}, True,
         lambda r: ("later_rate" not in NOMEAS["anchor_ordering_reason"],
                    "the rates were not removed"), results)

    EMPTY = copy.deepcopy(ADN)
    EMPTY["anchor_ordering_reason"] = "  "
    case("10 an EMPTY reason has switched the check off, not declared it",
         {"HHH": EMPTY}, {}, True,
         lambda r: (EMPTY.get("anchor_ordering_reason", "x").strip() == "",
                    "the reason is not empty"), results)

    # COUNTED, NOT DECLARED. This line used to print the declared constant TWICE — "cases
    # run: 15 (declared 15)" — which is true whatever ran, so deleting a case left the
    # control reporting a full house. That is the shape this repository has caught four
    # times: a control whose own report proves nothing about what it did.
    nred = sum(1 for _, e in RAN if e)
    print("cases run: %d (declared %d)" % (len(RAN), CASES))
    if len(RAN) != CASES:
        print("FAIL — the case count moved: %d ran, %d declared. A control that quietly "
              "loses cases reports fewer-of-fewer and reads as clean." % (len(RAN), CASES))
        return 1
    if results:
        for n, why in results:
            print("  FAIL  %s\n        %s" % (n, why))
        print("\nFAIL — the gate does not behave as the rule says.")
        return 1
    print("OK — %d red conditions fire, %d clean conditions do not."
          % (nred, len(RAN) - nred))
    return 0


if __name__ == "__main__":
    sys.exit(main())
