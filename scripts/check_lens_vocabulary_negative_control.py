#!/usr/bin/env python3
"""Negative control for check_lens_vocabulary.py.

Built on real sentences rather than invented ones. The defect cases are lifted
from documents that shipped — ARCC's own "END — this study's weighted central
54.65 · four lenses, weighted", ADNOCLS's weight tuple — and the clean cases are
the sentences a CORRECT study writes about the same subject, because the whole
risk in a vocabulary gate is that it goes red on a study doing exactly what the
rule asks. PHDC and TMGH both discuss the retired blend at length and both must
stay green.

The documents are made as text files rather than PDFs and read through a stubbed
extractor: what is under test is the RULE that separates asserting a blend from
explaining its retirement, and rendering a PDF to test a regular expression would
only add a way for the test to fail for reasons that are not the rule's.
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

import check_lens_vocabulary as G  # noqa: E402

ASSERTS_ARCC = (
    "Other three lenses -0.73  50/20/22/8 weights and share count  "
    "END - this study's weighted central 54.65  four lenses, weighted. "
    "Table 14 - the reconciliation bridge.")
ASSERTS_TUPLE = ("Read Basis. Weighted central: discounted cash flow 40 percent, "
                 "relative 25 percent, normalised 20 percent, book 15 percent. "
                 "45/20/20/15 weights carried from the prior edition.")
ASSERTS_PLAIN = ("The valuation. Weighted central AED 13.90 per share against a "
                 "spot of AED 12.30, a premium of 13 percent.")
EXPLAINS = (
    "One class primary is the central and every other lens is a cross-check. The "
    "retired blend weighted a justified price-to-book of zero at 15 per cent under "
    "this name, which is a derived valuation wearing the name of a disclosed "
    "figure; the previous edition published a weighted central and it is withdrawn. "
    "The two readings are published side by side and never averaged.")
CLEAN = ("The cash-flow lens is the central. Book value is published as a "
         "disclosed floor and never weighted into the answer. Where the lenses "
         "disagree the disagreement is published and the answer is the primary.")

CASES = []


def case(name, red, body, ratchet=None, docs=1, workbook=None):
    CASES.append((name, red, body, ratchet, docs, workbook))


case("a delivered document publishing a weighted central as its own answer", True,
     ASSERTS_ARCC)
case("a delivered document carrying the retired weight tuple", True, ASSERTS_TUPLE)
case("a plain 'Weighted central X per share against a spot of Y'", True,
     ASSERTS_PLAIN)
case("an assertion buried in an otherwise conforming document", True,
     CLEAN + " " + ASSERTS_PLAIN)

case("a document EXPLAINING that the blend was retired", False, EXPLAINS)
case("a conforming document that never mentions a blend", False, CLEAN)
case("a conforming document that both explains the retirement and states its "
     "primary", False, CLEAN + " " + EXPLAINS)
case("a listed document, still asserting, waived on the ratchet", False,
     ASSERTS_ARCC, ratchet={"TK": "clears at re-issue"})
case("a population of zero delivered documents", True, "", docs=0)
case("a ratchet naming a study with no delivered document", True, CLEAN,
     ratchet={"GHOST": "no document"})


def build(body, ratchet, docs, workbook=None):
    d = tempfile.mkdtemp()
    eng = os.path.join(d, "engine")
    os.makedirs(os.path.join(eng, "build_depth_audit"))
    if docs:
        sd = os.path.join(eng, "tk_study")
        os.makedirs(sd)
        open(os.path.join(sd, "TK_Valuation_Study_02-09-2026.pdf"), "w").write(body)
        # THE WORKBOOK IS A DELIVERED ARTEFACT TOO, and the gate reads it. AMOC's
        # document came back clean on 03-09-2026 while its workbook computed a
        # 45/20/20/15 blend into three cells labelled WEIGHTED CENTRAL, so a gate
        # that read only the PDF passed a study that shipped the retired
        # architecture to any reader who opened the model.
        if workbook is not None:
            open(os.path.join(sd, "TK_Valuation_Model_02092026.xlsx"),
                 "w").write(workbook)
    json.dump({"outstanding": ratchet or {}},
              open(os.path.join(eng, "build_depth_audit",
                                "lens_vocabulary_outstanding.json"), "w",
                   encoding="utf-8"), indent=1)
    return d, eng


# ---- the two false negatives, in AMOC's own words -------------------------
# Both of these were WAIVED by this gate on 03-09-2026 and AMOC was pruned off the
# ratchet as fixed on the strength of it. They are the sharpest cases here because
# they are not invented: the first is the sentence that fooled the 260-character
# window, the second is the row the layout split around its figures.
ASSERTS_THEN_EXPLAINS = (
    "Table 1 - the four lenses. The bear and bull columns of the weighted row are "
    "WEIGHTED with the same 45/20/20/15 weights as the base column. The previous "
    "edition labelled a row \"weighted central\" and then took the minimum and "
    "maximum across all four lenses, both of which came from the cash-flow lens "
    "alone, overstating the published spread by about two and a half times.")
SPLIT_ROW = (
    "Book and sustainable return  justified price-to-book  4.74 6.23 7.12 15% "
    "-31.6%  WEIGHTED  the four, weighted  4.93 9.91 16.73  100%  8.9%  CENTRAL")

case("a caption asserting the CURRENT weighting with a 'previous edition' "
     "sentence right after it — the 260-character window waived this", True,
     ASSERTS_THEN_EXPLAINS)
case("a table row whose label the layout splits around its own figures", True,
     SPLIT_ROW)


# ---- the widened scope: the workbook is read too --------------------------
WB_DIRTY = ("Lens · Value per share · WEIGHTED CENTRAL · "
            "=B10*0.45+C11*0.2+D12*0.2+E13*0.15 · against spot")
WB_CLEAN = ("Lens · Value per share · CENTRAL - the cash-flow lens · =B10 · "
            "the retired 45/20/20/15 blend, published beside the answer and unused")

case("a clean document beside a workbook that computes a weighted central — the "
     "condition the widened scope was built for", True, CLEAN, workbook=WB_DIRTY)
case("a clean document beside a workbook whose central IS the class primary",
     False, CLEAN, workbook=WB_CLEAN)


def main():
    real_text, real_out = G.text_of, G.OUTSTANDING
    # the extractor is stubbed: what is under test is the rule, not pdftotext
    G.text_of = lambda p: open(p, encoding="utf-8").read()
    caught = passed = 0
    red = sum(1 for c in CASES if c[1])
    green = len(CASES) - red
    try:
        for name, expect_red, body, ratchet, docs, workbook in CASES:
            d, eng = build(body, ratchet, docs, workbook)
            G.OUTSTANDING = os.path.join(eng, "build_depth_audit",
                                         "lens_vocabulary_outstanding.json")
            try:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = G.main(["--engine=%s" % eng])
                out = buf.getvalue()
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
    finally:
        G.text_of, G.OUTSTANDING = real_text, real_out
    print("\ndefects caught %d/%d | clean cases passed %d/%d"
          % (caught, red, passed, green))
    return 0 if (caught == red and passed == green) else 1


if __name__ == "__main__":
    raise SystemExit(main())
