#!/usr/bin/env python3
"""Negative control for check_output_sanity.py.

TWELVE CONDITIONS, SEVEN RED AND FIVE CLEAN. The clean half is the half this turns on,
because the whole risk in a relationship check is condemning work that is right: ARCC's
record misses its own operands by 0.0006 against 0.4869 allowed by the precision those
operands are printed to, and the FIRST DRAFT OF THIS GATE FAILED IT. That case is here
verbatim so the re-pointing cannot be quietly undone.

THE DEFECTS ARE LIFTED OUT OF THE REAL RECORDS AT RUN TIME rather than transcribed — a
transcribed fixture tests the transcription — and every mutation ASSERTS THAT IT LANDED
before the gate runs. NOTHING IS WRITTEN INTO THE REAL TREE: the fixtures are built inside
a temporary directory and the gate is pointed at it, so there is no undo that has to run.
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

# THE TALLY IS A SHARED INSTRUMENT, NOT A LINE EACH CONTROL PRINTS FOR ITSELF.
# Six controls here printed the DECLARED CONSTANT twice — "cases run: N
# (declared N)" — which is true whatever ran, and beside it a hand-typed red/clean
# split that had stopped matching. engine/control_tally.py counts what actually
# ran and refuses a count that moved [R-ENF-04].
sys.path.insert(0, ROOT)
from engine.control_tally import Tally          # noqa: E402

T = Tally(CASES, subject="check_output_sanity.py")


def real(tk):
    """A study's committed lens record, as it stands today."""
    for n in ("study_numbers.json", "numbers.json"):
        p = os.path.join(ENGINE, "%s_study" % tk.lower(), n)
        if os.path.exists(p):
            d = json.load(open(p, encoding="utf-8"))
            if isinstance(d.get("lens_record"), dict):
                return copy.deepcopy(d["lens_record"])
    raise SystemExit("control cannot run: %s has no lens record to lift" % tk)


def build(tmp, studies, ratchet):
    repo = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(repo, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(repo, "engine", "build_depth_audit"), exist_ok=True)
    shutil.copy(os.path.join(HERE, "check_output_sanity.py"),
                os.path.join(repo, "scripts", "check_output_sanity.py"))
    for tk, lr in studies.items():
        d = os.path.join(repo, "engine", "%s_study" % tk.lower())
        os.makedirs(d, exist_ok=True)
        body = {"lens_record": lr} if lr is not None else {"central": 1.0}
        json.dump(body, open(os.path.join(d, "study_numbers.json"), "w",
                             encoding="utf-8"), indent=1)
    json.dump({"outstanding": ratchet},
              open(os.path.join(repo, "engine", "build_depth_audit",
                                "output_sanity_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return repo


def run(repo):
    p = subprocess.run([sys.executable,
                        os.path.join(repo, "scripts", "check_output_sanity.py")],
                       capture_output=True, text=True, cwd=repo, timeout=120)
    return p.returncode != 0, (p.stdout + p.stderr)


def case(name, studies, ratchet, expect_red, landed, results):
    T.case(name, expect_red)
    tmp = tempfile.mkdtemp(prefix="outsan_nc_")
    try:
        repo = build(tmp, studies, ratchet)
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


def central_below_floor(lr):
    c = lr.get("central")
    c = c.get("value") if isinstance(c, dict) else c
    if not isinstance(c, (int, float)):
        c = (lr.get("primary") or {}).get("value")
    for x in (lr.get("cross_checks") or []):
        if x.get("kind") == "book_value" and isinstance(x.get("value"), (int, float)):
            return isinstance(c, (int, float)) and c < x["value"]
    return False


def rel(lr):
    for x in (lr.get("cross_checks") or []):
        if x.get("kind") == "relative_multiple":
            return x
    return {}


def main():
    results = []
    AIR, EGCH, ADN, ARCC, PHDC, MODON = (real(t) for t in
                                         ("airarabia", "egch", "adnocls",
                                          "arcc", "phdc", "modon"))

    # ---------- RED ----------
    case("1 AIRARABIA's central below its own published floor, exactly as it stands",
         {"AAA": AIR}, {}, True,
         lambda r: (central_below_floor(AIR), "AIRARABIA is not below its floor"), results)

    case("2 EGCH's central below its own published floor, exactly as it stands",
         {"BBB": EGCH}, {}, True,
         lambda r: (central_below_floor(EGCH), "EGCH is not below its floor"), results)

    # CORRECTED 07-09-2026. This case read the exemplar's live record and asserted it must
    # go RED. That was true of the record as it stood — the operands mixed an AED spot with
    # a share count in millions against USD thousands — and the study has since been
    # corrected AND the gate re-pointed, so reading the live record now proves nothing. The
    # CONSTRUCTIONS are kept as FROZEN FIXTURES and their expectations set from what each
    # actually is, rather than the case being deleted: a control that reads whatever the
    # book currently holds stops being a control the moment the book is fixed.
    def unit_error():
        """The exemplar's block as it stood: AED spot, shares in millions, USD thousands."""
        lr = copy.deepcopy(ADN)
        c = rel(lr)
        c.pop("construction", None)
        c["circularity"] = {"spot": 6.16, "shares": 7398.498764,
                            "net_debt": 2021329.0, "metric_value": 2085941.8878816736}
        return lr
    UNIT = unit_error()
    case("3 the exemplar's circularity block AS IT STOOD — three bases in one identity",
         {"CCC": UNIT}, {}, True,
         lambda r: (rel(UNIT)["circularity"]["shares"] < 1e5
                    and "construction" not in rel(UNIT),
                    "the unit error was not injected"), results)

    # THE DECISIVE CLEAN CASE — the exemplar's record as it stands now: two declared routes
    # weighting to one and reproducing the published figure. A control carrying only the red
    # half proves the gate refuses a figure from nowhere and says nothing about whether it
    # accepts the lens that legitimately has two routes.
    case("13 the exemplar's DECLARED two-route construction — must stay green",
         {"CCC": ADN}, {}, False,
         lambda r: (len((rel(ADN).get("construction") or {}).get("routes") or []) == 2,
                    "ADNOCLS declares no two-route construction"), results)

    # THE ARITHMETIC IS THE CLOSURE. Declaring a route has to be paid for twice — the
    # weights must sum to one and the routes must reproduce the published figure — so a
    # study cannot buy slack by naming one. These three prove it cannot.
    def route_weights_wrong():
        lr = copy.deepcopy(ADN)
        rel(lr)["construction"]["routes"][0]["weight"] = 0.9      # 0.9 + 0.3 = 1.2
        return lr
    RW = route_weights_wrong()
    case("14 declared routes whose weights do not sum to one",
         {"CCC": RW}, {}, True,
         lambda r: (abs(sum(x["weight"] for x in rel(RW)["construction"]["routes"]) - 1.0)
                    > 1e-6, "the weights were not moved"), results)

    def route_value_wrong():
        lr = copy.deepcopy(ADN)
        rel(lr)["construction"]["routes"][0]["value"] = \
            float(rel(ADN)["construction"]["routes"][0]["value"]) * 2.0
        return lr
    RV = route_value_wrong()
    case("15 a declared route whose value no longer reaches the published figure",
         {"CCC": RV}, {}, True,
         lambda r: (rel(RV)["construction"]["routes"][0]["value"]
                    > 1.9 * rel(ADN)["construction"]["routes"][0]["value"],
                    "the route value was not moved"), results)

    def route_unreadable():
        lr = copy.deepcopy(ADN)
        rel(lr)["construction"]["routes"][1].pop("value")
        return lr
    RU = route_unreadable()
    case("16 a declared route with no value — a construction that cannot be read",
         {"CCC": RU}, {}, True,
         lambda r: ("value" not in rel(RU)["construction"]["routes"][1],
                    "the route value was not removed"), results)

    def drifted():
        lr = copy.deepcopy(ARCC)
        c = rel(lr)
        c["multiple"] = float(c["multiple"]) * 3.0        # far from its own operands
        return lr
    DRIFT = drifted()
    case("4 a LISTED record drifting FURTHER from its own operands",
         {"DDD": DRIFT},
         {"DDD": {"claims": {"reproduce": {"ratio": 1.02, "why": "seeded"}},
                  "reason": "seeded"}},
         True,
         lambda r: (abs(float(rel(DRIFT)["multiple"]) / float(rel(ARCC)["multiple"]) - 3.0)
                    < 1e-9, "the multiple was not tripled"), results)

    case("5 ZERO study directories [R-ENF-04]",
         {}, {}, True,
         lambda r: (not glob.glob(os.path.join(r, "engine", "*_study")),
                    "study directories still present"), results)

    case("6 study directories present and ZERO lens records read [R-ENF-04]",
         {"EEE": None, "FFF": None}, {}, True,
         lambda r: (glob.glob(os.path.join(r, "engine", "*_study")) != [] and
                    "lens_record" not in open(os.path.join(
                        r, "engine", "eee_study", "study_numbers.json")).read(),
                    "a lens record survived"), results)

    def floor_by_note():
        lr = copy.deepcopy(AIR)
        for x in (lr.get("cross_checks") or []):
            if x.get("kind") == "book_value":
                x["kind"] = "asset_backing"          # not the reserved kind
                x["note"] = "the disclosed floor for this company"
        return lr
    NOTE = floor_by_note()
    case("7 a floor named only in the note, not by its kind",
         {"GGG": NOTE}, {}, True,
         lambda r: (all(x.get("kind") != "book_value" for x in NOTE["cross_checks"]),
                    "book_value kind survived"), results)

    # ---------- CLEAN ----------
    case("8 ARCC's record exactly as it stands — the first draft wrongly failed it",
         {"HHH": ARCC}, {}, False,
         lambda r: (bool(rel(ARCC).get("circularity")), "ARCC has no circularity block"),
         results)

    case("9 PHDC's record exactly as it stands — reproduces to the cent",
         {"III": PHDC}, {}, False,
         lambda r: (bool(rel(PHDC).get("circularity")), "PHDC has no circularity block"),
         results)

    def above_floor():
        lr = copy.deepcopy(ARCC)
        cen = (lr.get("primary") or {}).get("value") or 100.0
        lr.setdefault("cross_checks", []).append(
            {"kind": "book_value", "value": float(cen) * 0.4,
             "note": "a disclosed floor, published as such"})
        return lr
    ABOVE = above_floor()
    case("10 a central comfortably ABOVE its own floor must not fire",
         {"JJJ": ABOVE}, {}, False,
         lambda r: (any(x.get("kind") == "book_value" for x in ABOVE["cross_checks"]),
                    "no book_value cross-check added"), results)

    def declared():
        # MODON rather than AIRARABIA: this case must isolate the REPRODUCTION release, and
        # AIRARABIA carries the floor breach too, so a fixture built on it would go red for
        # the other claim and read exactly like the release failing. MODON is above its own
        # floor and misses its operands by 1.077x, which is the one condition wanted here.
        lr = copy.deepcopy(MODON)
        rel(lr)["value_adjustment"] = ("the management fee stream, valued separately and "
                                       "added to the multiple leg — the circularity block "
                                       "carries the ex-fee metric on purpose")
        return lr
    DECL = declared()
    case("11 a record that does NOT reproduce but NAMES what separates it",
         {"KKK": DECL}, {}, False,
         lambda r: (bool(rel(DECL).get("value_adjustment")), "no value_adjustment set"),
         results)

    case("12 a LISTED record that has moved TOWARD its own operands",
         {"LLL": ARCC},
         {"LLL": {"claims": {"reproduce": {"ratio": 4.0, "why": "seeded"}},
                  "reason": "seeded"}},
         False,
         lambda r: (bool(rel(ARCC).get("circularity")), "ARCC has no circularity block"),
         results)

    return T.report(results)


if __name__ == "__main__":
    sys.exit(main())
