#!/usr/bin/env python3
"""[R-LENS-03] read off the DELIVERED DOCUMENT, not off the record.

WHY THIS EXISTS, AND IT IS THE [R-ENF-03] SPECIES. [R-LENS-03] retired the typed
multi-lens blend on 02-09-2026: one class primary IS the central, every other lens
is a cross-check published beside it. `check_lens_design.py` enforces that — on
each study's committed `lens_record`. A reader does not receive the lens record.
They receive a Word document and a PDF.

Scanned on the day this was written, FOURTEEN of twenty-four delivered documents
still told their readers there is a weighted central, and two of them were studies
RE-ISSUED AFTER the rule was adopted: ARCC's 02-09-2026 edition prints "END — this
study's weighted central 54.65 · four lenses, weighted" on 50/20/22/8 weights
while its lens record names the cash-flow lens as the primary and its numbers file
carries 53.46; AMOC's 01-09-2026 edition reasons throughout from "the weighted
central" on 45/20/20/15. The record conformed and the document did not, and every
gate that could see the difference was looking at the record.

WHAT IT DOES NOT DO. It does not flag a study for DESCRIBING the retirement. A
document that says "the retired blend weighted a justified price-to-book of zero
at 15%" is doing exactly what the rule wants — publishing the disagreement — and a
gate that went red on it would be the check that cries wolf, which [R-CAL-02]
names as the one everybody learns to ignore. So a hit is discounted when a
retirement marker sits near it, and the negative control carries that case
explicitly.

RATCHET [R-ENF-02] · POPULATION ANCHORED [R-ENF-04]: the population is the
delivered documents on disk. A run that scanned zero documents REFUSES.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
OUTSTANDING = os.path.join(ENGINE, "build_depth_audit",
                           "lens_vocabulary_outstanding.json")

# The retired architecture asserting itself as the study's own answer.
BLEND = re.compile(
    r"weighted central|the central weights|weights the reads|on stated weights|"
    r"four lenses,\s*weighted|weighted average of the (?:four|three)|"
    r"blend(?:ed)?\s+(?:of\s+)?(?:the\s+)?(?:four|three)\s+lenses|"
    r"\b\d{1,2}/\d{1,2}/\d{1,2}/\d{1,2}\s+weights", re.I)

# The same words used to explain that the construction was retired. Not an escape
# hatch: it only discounts a hit that sits WITHIN `WINDOW` characters of one.
RETIRED = re.compile(
    r"retired|previous edition|earlier edition|no longer|never averaged|"
    r"rather than blended|is not (?:a )?blend|was withdrawn|prohibit|"
    r"the blend this study does not|used to", re.I)
WINDOW = 260

DATED = re.compile(r"(\d{2})-(\d{2})-(\d{4})")


def _key(path):
    m = DATED.search(os.path.basename(path))
    return (int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else (0, 0, 0)


def documents(engine=ENGINE):
    """{ticker: latest delivered study PDF}. The PDF is what a reader opens."""
    out = {}
    for sd in sorted(glob.glob(os.path.join(engine, "*_study"))):
        tk = os.path.basename(sd).replace("_study", "").upper()
        pdfs = glob.glob(os.path.join(sd, "*Valuation_Study*.pdf"))
        if pdfs:
            out[tk] = max(pdfs, key=_key)
    return out


def text_of(pdf):
    try:
        return subprocess.run(["pdftotext", pdf, "-"], capture_output=True,
                              text=True, timeout=300).stdout or ""
    except Exception:
        return ""


def scan(pdf):
    """(hits asserting the blend, hits explained as retired)."""
    t = text_of(pdf)
    asserting, explained = [], 0
    for m in BLEND.finditer(t):
        lo, hi = max(0, m.start() - WINDOW), m.end() + WINDOW
        if RETIRED.search(t[lo:hi]):
            explained += 1
            continue
        asserting.append(re.sub(r"\s+", " ", t[max(0, m.start() - 90):
                                              m.end() + 90]).strip())
    return asserting, explained


def load_outstanding():
    if not os.path.exists(OUTSTANDING):
        return {}
    try:
        return json.load(open(OUTSTANDING, encoding="utf-8")).get("outstanding", {})
    except Exception:
        return {}


def main(argv):
    prune = "--prune" in argv
    engine = ENGINE
    for a in argv:
        if a.startswith("--engine="):
            engine = a.split("=", 1)[1]
    docs = documents(engine)
    if not docs:
        print("REFUSED: no delivered documents were scanned. An empty population "
              "is not a clean result [R-ENF-04].")
        return 2

    outstanding = load_outstanding()
    stale = [tk for tk in outstanding if tk not in docs]
    clean, dirty = [], {}
    for tk, pdf in sorted(docs.items()):
        asserting, explained = scan(pdf)
        if asserting:
            dirty[tk] = (os.path.basename(pdf), asserting, explained)
        else:
            clean.append((tk, os.path.basename(pdf), explained))

    print("lens vocabulary in the DELIVERED documents [R-LENS-03]\n")
    print("  documents scanned  %d" % len(docs))
    print("  clean              %d" % len(clean))
    for tk, f, ex in clean:
        print("     %-11s %s%s" % (tk, f[:46],
                                   "   (%d retirement mention(s))" % ex if ex else ""))
    new = {tk: v for tk, v in dirty.items() if tk not in outstanding}
    waived = {tk: v for tk, v in dirty.items() if tk in outstanding}
    if waived:
        print("  waived on the ratchet  %d" % len(waived))
        for tk, (f, a, ex) in sorted(waived.items()):
            print("     %-11s %d assertion(s)  %s" % (tk, len(a), f[:40]))
    if new:
        print("  NEW  %d" % len(new))
        for tk, (f, a, ex) in sorted(new.items()):
            print("     %-11s %d assertion(s) in %s" % (tk, len(a), f[:40]))
            for s in a[:2]:
                print("        ...%s..." % s[:150])
    if stale:
        print("\n  REFUSED: the ratchet names studies with no delivered document: %s"
              % ", ".join(sorted(stale)))
        return 2

    if prune:
        keep = {tk: outstanding[tk] for tk in outstanding if tk in dirty}
        json.dump({"_": ("Delivered documents still printing the retired weighted "
                         "blend as the study's own central. Each clears when that "
                         "study is re-issued. THE LIST MAY ONLY SHORTEN "
                         "[R-ENF-02]."),
                   "outstanding": keep},
                  open(OUTSTANDING, "w", encoding="utf-8"), indent=1,
                  ensure_ascii=False)
        print("\n  pruned: %d document(s) remain outstanding" % len(keep))

    if new:
        print("\nFAILED — a delivered document may not publish a weighted blend of "
              "lenses as its central. One class primary IS the central "
              "[R-LENS-03].")
        return 1
    print("\nOK — no delivered document newly publishes the retired blend.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
