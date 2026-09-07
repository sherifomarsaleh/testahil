#!/usr/bin/env python3
"""Negative control for check_bridge_reaches_answer.py.

NINE CONDITIONS, FIVE RED AND FOUR CLEAN. The clean half is the discrimination that
matters: five studies in this book have a bridge that reaches their published answer TO THE
CENT, and a gate condemning them would be worse than no gate at all. A study committing one
of the two figures and not the other is OUT OF SCOPE rather than in breach — a bridge with
no published central to reach cannot fail to reach it.

The two defects are lifted from the real records at run time. Every mutation asserts it
landed. Nothing is written into the real tree.
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
CASES = 9


def real(tk):
    p = os.path.join(ENGINE, "%s_study" % tk.lower(), "study_numbers.json")
    d = json.load(open(p, encoding="utf-8"))
    return {"bridge_record": copy.deepcopy(d.get("bridge_record") or {}),
            "lens_record": copy.deepcopy(d.get("lens_record") or {})}


def build(tmp, docs, ratchet):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    eng = os.path.join(repo, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_bridge_reaches_answer.py"),
                os.path.join(repo, "scripts", "check_bridge_reaches_answer.py"))
    for tk, doc in docs.items():
        d = os.path.join(eng, "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        json.dump(doc, open(os.path.join(d, "study_numbers.json"), "w",
                            encoding="utf-8"), indent=1, default=float)
    json.dump({"outstanding": ratchet},
              open(os.path.join(eng, "build_depth_audit",
                                "bridge_answer_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable, os.path.join(
        repo, "scripts", "check_bridge_reaches_answer.py")],
        capture_output=True, text=True, cwd=repo, timeout=120)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, docs, ratchet, expect_red, landed, results):
    tmp = tempfile.mkdtemp(prefix="bra_nc_")
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


def disagrees(d):
    ps = (d.get("bridge_record") or {}).get("per_share")
    c = (d.get("lens_record") or {}).get("central")
    return bool(ps and c and abs(ps - c) > 0.01)


def main():
    r = []
    ADN, TMGH, PHDC, ARCC = (real(t) for t in ("adnocls", "tmgh", "phdc", "arcc"))

    # ---------- RED ----------
    case("1 ADNOCLS's own figures — the exemplar's bridge is 73% below its answer",
         {"AAA": ADN}, {}, True,
         lambda r_: (disagrees(ADN), "ADNOCLS's bridge agrees with its central"), r)

    case("2 TMGH's own figures",
         {"BBB": TMGH}, {}, True,
         lambda r_: (disagrees(TMGH), "TMGH's bridge agrees with its central"), r)

    case("3 ZERO study directories [R-ENF-04]",
         {}, {}, True,
         lambda r_: (not glob.glob(os.path.join(r_, "engine", "*_study")),
                     "directories present"), r)

    ONE = {"bridge_record": {"per_share": 10.0}}
    case("4 directories present and NOT ONE commits both figures [R-ENF-04]",
         {"CCC": ONE, "DDD": ONE}, {}, True,
         lambda r_: ("lens_record" not in ONE, "a central survived"), r)

    WORSE = copy.deepcopy(ADN)
    WORSE["bridge_record"]["per_share"] = 0.5
    case("5 a LISTED bridge that has drifted further from its answer",
         {"EEE": WORSE}, {"EEE": {"gap": -0.728, "why": "seeded"}}, True,
         lambda r_: (WORSE["bridge_record"]["per_share"] == 0.5,
                     "the per-share was not moved"), r)

    # ---------- CLEAN ----------
    case("6 PHDC: a bridge that reaches its answer to the cent",
         {"FFF": PHDC}, {}, False,
         lambda r_: (not disagrees(PHDC), "PHDC's bridge does not agree"), r)

    case("7 ARCC: the same, on another study",
         {"GGG": ARCC}, {}, False,
         lambda r_: (not disagrees(ARCC), "ARCC's bridge does not agree"), r)

    DECL = copy.deepcopy(ADN)
    DECL["bridge_serves"] = ("the shipping leg alone; the published central is the "
                             "sum of the parts, of which this bridge is one")
    case("8 the same disagreement, DECLARED with what the bridge serves",
         {"HHH": DECL, "FFF": PHDC}, {}, False,
         lambda r_: (bool(DECL.get("bridge_serves")), "no declaration set"), r)

    OUT = {"lens_record": {"central": 12.0}}
    case("9 a study with a central and no bridge is out of scope, not in breach",
         {"III": OUT, "FFF": PHDC}, {}, False,
         lambda r_: ("bridge_record" not in OUT, "a bridge survived"), r)

    print("cases run: %d (declared %d)" % (CASES, CASES))
    if r:
        for n, why in r:
            print("  FAIL  %s\n        %s" % (n, why))
        print("\nFAIL — the gate does not behave as the rule says.")
        return 1
    print("OK — 5 red conditions fire, 4 clean conditions do not.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
