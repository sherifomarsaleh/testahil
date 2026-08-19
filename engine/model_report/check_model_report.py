#!/usr/bin/env python3
"""
check_model_report.py — the model-report gate, run against DELIVERED files.

    python3 engine/model_report/check_model_report.py \
        --study  engine/xxx_study/XXX_Valuation_Study_DD-MM-YYYY_public.docx \
        --xlsx   engine/xxx_study/XXX_Valuation_Model_DDMMYYYY_public.xlsx \
        --biblio engine/xxx_study/XXX_Bibliography_DD-MM-YYYY.docx

Prints a per-item evidence table and exits non-zero on any FAIL. Paste the output into the
study's QC gate file against item (a) — that item is no longer satisfiable by attestation.

    --self-test   run the negative control: the model report must PASS, and the 18-Aug-2026
                  study (the shallow delivery this gate was written for) must FAIL.

Nothing else in the repo catches this. The 16-section skeleton and the 16-sheet workbook are
identical in a 30,000-word study and a 4,400-word one; only counting what is actually in the
delivered file tells them apart.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_report_spec import (          # noqa: E402
    MODEL_REPORT, check_study_docx, check_workbook, check_bibliography,
)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# The model report is the exemplar MINUS the excluded section — build it with
# build_model_report_docx.py, which is what makes the exemplar satisfy its own contract.
MODEL_FILES = {
    "study": "engine/model_report/MODEL_REPORT_09-08-2026.docx",
    "xlsx": "engine/adnocls_study/ADNOCLS_Valuation_Model_09082026_public.xlsx",
    "biblio": "engine/adnocls_study/ADNOCLS_Bibliography_09-08-2026.docx",
}
CONTROL_FILES = {
    "study": "engine/riyadhcable_study/RIYADHCABLE_Valuation_Study_18-08-2026_public.docx",
    "xlsx": "engine/riyadhcable_study/RIYADHCABLE_Valuation_Model_18082026_public.xlsx",
    "biblio": "engine/riyadhcable_study/RIYADHCABLE_Bibliography_18-08-2026.docx",
}


def run(study=None, xlsx=None, biblio=None):
    findings = []
    if study:
        findings += check_study_docx(study)
    if xlsx:
        findings += check_workbook(xlsx)
    if biblio:
        findings += check_bibliography(biblio)
    return findings


def report(findings, label=""):
    fails = [f for f in findings if f["status"] == "FAIL"]
    width = 46
    if label:
        print(f"\n{'=' * 100}\n{label}\n{'=' * 100}")
    cur = None
    for f in findings:
        if f["section"] != cur:
            cur = f["section"]
            print(f"\n{cur}")
        mark = "FAIL" if f["status"] == "FAIL" else "PASS"
        detail = f["detail"]
        print(f"  [{mark}] {f['item']:<{width}} {detail[:150]}")
        if len(detail) > 150:
            for i in range(150, len(detail), 130):
                print(f"         {' ' * width} {detail[i:i + 130]}")
    print(f"\n{'-' * 100}")
    print(f"MODEL-REPORT CONTRACT: {'FAIL' if fails else 'PASS'} "
          f"({len(fails)} unmet of {len(findings)} checked)")
    return len(fails)


def self_test():
    ok = True
    m = run(**{k: os.path.join(REPO, v) for k, v in MODEL_FILES.items()})
    n_model = report(m, f"NEGATIVE CONTROL 1/2 — the model report itself "
                        f"({MODEL_REPORT['reference']}) must PASS")
    if n_model:
        print("SELF-TEST FAIL: the model report does not satisfy its own contract.")
        ok = False

    c = run(**{k: os.path.join(REPO, v) for k, v in CONTROL_FILES.items()})
    n_ctrl = report(c, "NEGATIVE CONTROL 2/2 — RIYADHCABLE 18-08-2026, the delivery this "
                       "gate was written for, must FAIL")
    if not n_ctrl:
        print("SELF-TEST FAIL: the shallow delivery passed — the gate has no teeth.")
        ok = False

    print(f"\n{'=' * 100}")
    print(f"SELF-TEST: {'PASS' if ok else 'FAIL'} — model report {n_model} unmet, "
          f"control {n_ctrl} unmet")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--study")
    ap.add_argument("--xlsx")
    ap.add_argument("--biblio")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not any((a.study, a.xlsx, a.biblio)):
        ap.error("give at least one of --study / --xlsx / --biblio, or --self-test")
    return 1 if report(run(a.study, a.xlsx, a.biblio),
                       f"MODEL-REPORT CONTRACT — {a.study or a.xlsx or a.biblio}") else 0


if __name__ == "__main__":
    sys.exit(main())
