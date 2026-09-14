#!/usr/bin/env python3
"""Negative control for check_bridge_reaches_answer.py.

ELEVEN CONDITIONS, FIVE RED AND SIX CLEAN, one of them INVERTED. The clean half is the discrimination that
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
CASES = 11

# THE TALLY IS A SHARED INSTRUMENT, NOT A LINE EACH CONTROL PRINTS FOR ITSELF.
# Six controls here printed the DECLARED CONSTANT twice — "cases run: N
# (declared N)" — which is true whatever ran, and beside it a hand-typed red/clean
# split that had stopped matching. engine/control_tally.py counts what actually
# ran and refuses a count that moved [R-ENF-04].
sys.path.insert(0, ROOT)
from engine.control_tally import Tally          # noqa: E402

T = Tally(CASES, subject="check_bridge_reaches_answer.py")


def real(tk):
    p = os.path.join(ENGINE, "%s_study" % tk.lower(), "study_numbers.json")
    d = json.load(open(p, encoding="utf-8"))
    return {"bridge_record": copy.deepcopy(d.get("bridge_record") or {}),
            "lens_record": copy.deepcopy(d.get("lens_record") or {}),
            # META TRAVELS WITH THE FIXTURE, because the currency clause lives there and a
            # fixture that dropped it would test the gate without the thing under test.
            "meta": copy.deepcopy(d.get("meta") or {})}


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
    T.case(name, expect_red)
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
    # INVERTED RATHER THAN DELETED, on the precedent [R-GAP-01] set when its trigger went
    # two-sided: this case asserted the exemplar was RED, which was correct evidence for the
    # first draft and is now wrong, because that draft had no notion of a study reporting in
    # one currency and listing in another. Keeping the construction and flipping the
    # expectation is the only way the re-pointing is tested where it matters; deleting it
    # would leave the change untested exactly there.
    case("1 the exemplar reconciles once its own declared conversion is read",
         {"AAA": ADN}, {}, False,
         lambda r_: (disagrees(ADN), "ADNOCLS's raw bridge figure equals its central, so "
                                     "the fixture no longer carries the condition"), r)

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

    # REBASED ON TMGH, which reports and lists in one currency, because the drift test must
    # isolate DRIFT and the exemplar now reconciles through its declared conversion.
    WORSE = copy.deepcopy(TMGH)
    WORSE["bridge_record"]["per_share"] = 5.0
    case("5 a LISTED bridge that has drifted further from its answer",
         {"EEE": WORSE}, {"EEE": {"gap": -0.290, "why": "seeded"}}, True,
         lambda r_: (WORSE["bridge_record"]["per_share"] == 5.0,
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

    # ---------- the currency clause, which the first draft did not have ----------
    # ADNOC L&S reports in USD and lists in AED and commits all three facts. Its bridge
    # arrives at 1.5263 USD and the study publishes 5.6054 AED — the same number, converted.
    # The first draft of this gate called that the largest disagreement in the book. The
    # case is here verbatim so the re-pointing cannot be quietly undone.
    ADN_FX = copy.deepcopy(ADN)
    case("10 the exemplar: a bridge in the REPORTING currency, published in the LISTING one",
         {"JJJ": ADN_FX}, {}, False,
         lambda r_: (((ADN_FX.get("meta") or {}).get("reporting_currency")
                      != (ADN_FX.get("meta") or {}).get("listing_currency")
                      and float((ADN_FX.get("meta") or {}).get("fx", 0)) > 0),
                     "the fixture does not declare two currencies and a rate"), r)

    # A DECLARED RATE THAT DOES NOT RECONCILE IS STILL A BREACH — the release is reading a
    # declaration, not accepting any pair of numbers that carry one.
    BAD_FX = copy.deepcopy(ADN)
    BAD_FX["meta"]["fx"] = 1.5
    case("11 two currencies declared and a rate that does NOT reconcile them",
         {"KKK": BAD_FX}, {}, True,
         lambda r_: (abs(float(BAD_FX["meta"]["fx"]) - 1.5) < 1e-9,
                     "the rate was not moved"), r)

    return T.report(r)


if __name__ == "__main__":
    sys.exit(main())
