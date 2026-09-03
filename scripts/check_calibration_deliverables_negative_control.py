#!/usr/bin/env python3
"""Negative control for check_calibration_deliverables.py.

A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. Each case builds a temporary engine
tree, injects one condition, and asserts the checker goes RED or stays GREEN as
stated. The clean cases matter as much as the defects: a gate that fires on a
correct delivery is the permanently-red check [R-ENF-02] forbids, and the two that
would most easily produce one — a bibliography named Sources rather than
Bibliography, and a superseded edition sitting beside a current one — are both
here.

The defects are not invented. The date-drift case is the exact condition this gate
found on its FIRST run: TMGH's edition 2 shipped with edition 1's QC gate beside it.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import check_calibration_deliverables as G  # noqa: E402

EDITION = "02-09-2026"
COMPACT = "02092026"


def files(stamp=EDITION, compact=COMPACT, biblio="Bibliography", qc=None):
    return ["TK_Valuation_Study_%s.docx" % stamp,
            "TK_Valuation_Study_%s.pdf" % stamp,
            "TK_Valuation_Model_%s.xlsx" % compact,
            "TK_%s_%s.docx" % (biblio, stamp),
            "QC_GATE_%s.md" % (qc or stamp)]


def tree(names=("TK",), study_files=None, ratchet=None, no_study=False):
    d = tempfile.mkdtemp()
    eng = os.path.join(d, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    for n in names:
        os.makedirs(os.path.join(eng, "%s_walkforward" % n.lower()))
        if no_study:
            continue
        sd = os.path.join(eng, "%s_study" % n.lower())
        os.makedirs(sd)
        for f in (study_files if study_files is not None else files()):
            open(os.path.join(sd, f.replace("TK", n)), "w").write("x")
    json.dump({"outstanding": ratchet or {}},
              open(os.path.join(eng, "build_depth_audit",
                                "deliverables_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return d, eng


def run(eng):
    old = G.OUTSTANDING
    G.OUTSTANDING = os.path.join(eng, "build_depth_audit",
                                 "deliverables_outstanding.json")
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = G.main(["--engine=%s" % eng])
        return rc, buf.getvalue()
    finally:
        G.OUTSTANDING = old


CASES = []


def case(name, red, build):
    CASES.append((name, red, build))


# ---- defects ---------------------------------------------------------------
case("a calibrated name with no study directory at all", True,
     lambda: tree(no_study=True))

for label, drop in (("no Word report", 0), ("no rendered PDF", 1),
                    ("no workbook", 2), ("no standalone bibliography", 3),
                    ("no QC gate", 4)):
    def _b(drop=drop):
        f = files()
        del f[drop]
        return tree(study_files=f)
    case("a delivered edition with %s" % label, True, _b)

case("a QC gate one edition behind the report — the condition this gate found on "
     "its first run", True,
     lambda: tree(study_files=files(qc="01-09-2026")))


def _stale_workbook():
    f = files()
    f[2] = "TK_Valuation_Model_01092026.xlsx"
    return tree(study_files=f)
case("a current report beside last edition's workbook", True, _stale_workbook)


def _stale_biblio():
    f = files()
    f[3] = "TK_Bibliography_01-09-2026.docx"
    return tree(study_files=f)
case("a current report beside last edition's bibliography", True, _stale_biblio)

case("a ratchet naming a name that is not calibrated", True,
     lambda: tree(ratchet={"GHOST": "not on disk"}))

case("a population of zero calibrated names", True, lambda: tree(names=()))


# ---- clean cases -----------------------------------------------------------
case("a complete, self-consistent edition", False, lambda: tree())

case("a bibliography named Sources rather than Bibliography — TMGH's convention",
     False, lambda: tree(study_files=files(biblio="Sources")))


def _superseded_beside_current():
    f = files() + ["TK_Valuation_Study_06-08-2026.docx",
                   "TK_Valuation_Study_06-08-2026.pdf",
                   "TK_Valuation_Model_06082026.xlsx",
                   "TK_Bibliography_06-08-2026.docx",
                   "QC_GATE_06-08-2026.md"]
    return tree(study_files=f)
case("a superseded edition sitting beside a complete current one", False,
     _superseded_beside_current)

case("an incomplete edition that is listed on the ratchet", False,
     lambda: tree(study_files=files()[:-1], ratchet={"TK": "queued for the audit"}))


def main():
    caught = passed = 0
    red = sum(1 for _, r, _ in CASES if r)
    green = len(CASES) - red
    for name, expect_red, build in CASES:
        d, eng = build()
        try:
            rc, out = run(eng)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = (rc != 0) == expect_red
        if ok:
            caught += 1 if expect_red else 0
            passed += 0 if expect_red else 1
        print("  %-6s %s" % ("CAUGHT" if (ok and expect_red) else
                             "PASSED" if ok else "MISSED", name))
        if not ok:
            print(out)
    print("\ndefects caught %d/%d | clean cases passed %d/%d"
          % (caught, red, passed, green))
    return 0 if (caught == red and passed == green) else 1


if __name__ == "__main__":
    raise SystemExit(main())
