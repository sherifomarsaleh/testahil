#!/usr/bin/env python3
"""
build_model_report_docx.py — produce THE MODEL REPORT document from its exemplar.

The model report is ADNOCLS_Valuation_Study_09-08-2026 MINUS the section "What changed in
these editions, and why" [excluded 19-Aug-2026, per instruction]. Rather than describe that
subtraction in prose and leave a future build to guess at it, this script performs it, so the
model report exists as a document a builder can open beside the one it is writing.

Four edits, all surgical, all asserted:

  1. RESCUE one paragraph out of the section before cutting. The note beginning "One further
     change has been made since the corrections above" is not edition history: it discloses
     that the desk's sanctioned beta routine now returns 1.103 on 159 weekly observations
     where every table in the study carries the adopted 1.085, and it widens the interval.
     That is a live discrepancy between an adopted number and the routine that is supposed to
     produce it, which is a CAVEAT. It moves to the end of section 7, with only its opening
     clause re-framed off the edition it referred to.

  2. Remove the section — its heading, its remaining paragraphs and its three tables — from
     after section 7 up to the start of Appendix A.

  3. Remove the fifth paragraph of the READ FIRST box, "This is a twice-corrected edition,
     and both rounds of correction are listed …", which is the same edition history in the
     front matter and closes by pointing at the section being removed.

  4. Repair the one sentence in "About this series" that pointed at it. It promised the
     reader a full list of corrections "under 'What changed in these editions, and why',
     immediately after the caveats". With the section gone that promise dangles, so the
     paragraph is rewritten to state the mechanism the model report actually uses: the
     correction is made at the point it bears on, with the superseded construction reprinted
     beside the new one at full size. Nothing else depends on the removed section.

NOT removed: the inline "an earlier edition of this study …" passages in 1.2, 1.7, 1.8 and 7.
Those are not edition history — each one prices a live construction against the superseded one
at the point the number is used, which is the standing dual-framing rule doing its job. The
instruction was to remove the SECTION.

The published ADNOCLS study is untouched: re-issuing a published study is a separate,
explicitly-requested step. This writes a new file under engine/model_report/.

    python3 engine/model_report/build_model_report_docx.py [--check]
"""

import argparse
import os
import shutil
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "engine/adnocls_study/ADNOCLS_Valuation_Study_09-08-2026_public.docx")
OUT = os.path.join(HERE, "MODEL_REPORT_09-08-2026.docx")

CUT_FROM = "what changed in these editions"
CUT_TO = "appendix a"
POINTER = "what changed in these editions, and why"
FRONT_BOX = "this is a twice-corrected edition"
RESCUE = "one further change has been made since the corrections above"
RESCUE_LEAD = (
    "One measurement in this study comes from method rather than from a reviewer, and it "
    "belongs here on its own. "
)

REPLACEMENT = (
    "The same rule governs correction, and it extends to a study's own words about itself. "
    "Where a study has been reviewed and found wrong, the correction is made at the point it "
    "bears on — in the section whose number it changes, with the superseded construction "
    "reprinted beside the new one at full size rather than quietly replaced — and where a "
    "superseded edition made a CLAIM that later work falsified, the claim is reprinted and "
    "corrected rather than deleted. This edition does that twice: for a caveat that said a "
    "revenue convention could not reach the valuation, and for a cost of debt described as "
    "weighted when it is an average."
)


def _text(p):
    return "".join(t.text or "" for t in p.iter(f"{{{W}}}t"))


def build(src=SRC, out=OUT):
    if not os.path.exists(src):
        sys.exit(f"exemplar not found: {src}")
    zin = zipfile.ZipFile(src)
    doc = ET.fromstring(zin.read("word/document.xml"))
    body = doc.find(f"{{{W}}}body")
    kids = list(body)

    start = end = None
    for i, el in enumerate(kids):
        if el.tag != f"{{{W}}}p":
            continue
        low = _text(el).strip().lower()
        if start is None and low.startswith(CUT_FROM):
            start = i
        elif start is not None and low.startswith(CUT_TO):
            end = i
            break
    if start is None:
        sys.exit(f"nothing to cut — no heading starting {CUT_FROM!r} in {src}")
    if end is None:
        sys.exit(f"could not find the following heading {CUT_TO!r}; refusing to cut to the end")

    cut = kids[start:end]

    # (1) Rescue the live caveat out of the section before the section goes.
    rescued = None
    for el in cut:
        if el.tag == f"{{{W}}}p" and _text(el).strip().lower().startswith(RESCUE):
            rescued = el
            break
    if rescued is None:
        sys.exit(f"expected to rescue a paragraph starting {RESCUE!r}; it is not in the section")
    ts = rescued.findall(f".//{{{W}}}t")
    head = ts[0].text or ""
    dot = head.find(". ")
    if dot < 0:
        sys.exit("could not re-frame the rescued paragraph: no sentence boundary in its first run")
    ts[0].text = RESCUE_LEAD + head[dot + 2:]
    ts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    cut.remove(rescued)

    n_tbl = sum(1 for e in cut if e.tag == f"{{{W}}}tbl")
    n_par = sum(1 for e in cut if e.tag == f"{{{W}}}p")
    for el in cut:
        body.remove(el)
    body.remove(rescued)
    # Section 7 closes on "What would change our mind, specifically"; the rescued caveat is a
    # caveat, so it goes with the others, ahead of that closing paragraph.
    closing = [i for i, e in enumerate(list(body))
               if e.tag == f"{{{W}}}p"
               and _text(e).strip().lower().startswith("what would change our mind")]
    if not closing:
        sys.exit("section 7 has no 'what would change our mind' paragraph to sit ahead of")
    body.insert(closing[-1], rescued)

    # (3) The same edition history in the READ FIRST box.
    dropped_box = 0
    for tbl in body.iter(f"{{{W}}}tbl"):
        for cell in tbl.iter(f"{{{W}}}tc"):
            for p in list(cell.findall(f"{{{W}}}p")):
                if _text(p).strip().lower().startswith(FRONT_BOX):
                    cell.remove(p)
                    dropped_box += 1
    if dropped_box != 1:
        sys.exit(f"expected exactly one READ FIRST edition paragraph, found {dropped_box}")

    fixed = 0
    for el in body:
        if el.tag != f"{{{W}}}p":
            continue
        if POINTER in _text(el).lower():
            runs = el.findall(f"{{{W}}}r")
            if not runs:
                continue
            first, rest = runs[0], runs[1:]
            ts = first.findall(f"{{{W}}}t")
            if not ts:
                continue
            ts[0].text = REPLACEMENT
            ts[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            for extra in ts[1:]:
                first.remove(extra)
            for r in rest:
                el.remove(r)
            fixed += 1
    if fixed != 1:
        sys.exit(f"expected exactly one paragraph pointing at the removed section, found {fixed}")

    xml = ET.tostring(doc, encoding="UTF-8", xml_declaration=True)
    tmp = out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = xml if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    shutil.move(tmp, out)
    zin.close()

    # Verify the delivered file, never the intent.
    z = zipfile.ZipFile(out)
    body2 = ET.fromstring(z.read("word/document.xml")).find(f"{{{W}}}body")
    txt = " ".join(_text(p) for p in body2.iter(f"{{{W}}}p")).lower()
    assert CUT_FROM not in txt, "the excluded section survived the cut"
    assert FRONT_BOX not in txt, "the front-matter edition box survived"
    assert "appendix a" in txt and "disclosure" in txt, "the cut removed too much"
    assert REPLACEMENT[:60].lower() in txt, "the About paragraph was not repaired"
    assert RESCUE_LEAD.strip().lower()[:40] in txt, "the rescued caveat was lost"
    assert "1.103" in txt, "the rescued caveat lost its numbers"
    print(f"model report written: {os.path.relpath(out, ROOT)}")
    print(f"  removed:  {n_par} paragraphs + {n_tbl} tables (the excluded section)")
    print(f"  removed:  1 edition paragraph from the READ FIRST box")
    print(f"  rescued:  1 live beta caveat, moved into section 7 with the other caveats")
    print(f"  repaired: 1 paragraph in About this series that pointed at the section")
    return out


def check(out=OUT):
    if not os.path.exists(out):
        sys.exit(f"model report not built: {out}")
    z = zipfile.ZipFile(out)
    body = ET.fromstring(z.read("word/document.xml")).find(f"{{{W}}}body")
    txt = " ".join(_text(p) for p in body.iter(f"{{{W}}}p")).lower()
    bad = [s for s in (CUT_FROM, POINTER, FRONT_BOX) if s in txt]
    if bad:
        sys.exit(f"FAIL — the model report still carries: {bad}")
    print("model report OK — the excluded section is absent and nothing points at it")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="verify an already-built model report")
    a = ap.parse_args()
    check() if a.check else build()
