#!/usr/bin/env python3
"""GBCO — the external-reader scrub. Depth-bar standard 4.

A DELIVERED DOCUMENT IS WRITTEN FOR SOMEBODY WHO DOES NOT WORK HERE, and the words
this house uses about its own procedure are meaningless to them at best. The shared
gate (scripts/check_delivered_vocabulary.py) matches a standing-rule identifier and a
repository path BY SHAPE, and says of itself that it does NOT replace this: those two
shapes cannot occur innocently, while a PROCEDURE NOUN can, and telling the two apart
is a judgement about ordinary senses that only a study can make about its own pages.

THIS STUDY HAD NO SCRUB AT ALL and an outside audit found six hits in the delivered
bibliography — five of one term and one of another — while the shared gate listed this
study as clean and was right to.

THE EXCEPTIONS ARE THE WHOLE DIFFICULTY AND THEY ARE DECLARED WITH THEIR REASONS. Some
of this vocabulary is the MODEL REPORT'S OWN reader-facing structure: the expert
valuation PANEL is an appendix a reader is meant to read, and the risk REGISTER and the
research REGISTER are two of the three parts the standard names for Appendix B. A scrub
that banned those words would be demanding the study stop printing sections the
standard requires, which is the check firing on work that is right — so the ordinary
senses are named here rather than the terms dropped, and each one says where it is
allowed to appear.

    python3 engine/gbco_study/scrub.py          # zero hits, or a nonzero exit
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Each entry: (pattern, why it is internal). Matched case-insensitively on word
# boundaries where the term is a word; a hyphenated term is matched as written.
BANNED = [
    (r"walk[- ]forward",      "names one of this house's three internal tests; a reader "
                              "cannot tell which and is not owed the distinction"),
    (r"valuation[- ]input block", "an internal record's name"),
    (r"hard gate",            "procedure vocabulary; the reader is owed the requirement, "
                              "not the machinery that enforces it"),
    (r"\bSIGCM\b",            "an internal mandate's acronym"),
    (r"depth[- ]bar",         "the internal standard a study is held to"),
    (r"\bQC gate\b",          "an internal artefact"),
    (r"negative control",     "the machinery behind a check, not a finding"),
    (r"promotion rule",       "an internal rule"),
    (r"\bratchet(ed|s)?\b",   "an internal allowance list"),
    (r"Step 0\.0|Step 2A",    "internal step numbering"),
    (r"sweep register",       "an internal register"),
    # RE-POINTED ON ITS OWN FIRST RUN, per the house rule that a check firing on work
    # that is right is re-pointed rather than widened or answered by deleting the
    # sentence. `four[- ]field` caught three passages, and all three were the documents
    # EXPLAINING THEMSELVES to a reader — "with its own four fields", and a bibliography
    # heading that names them in the next breath ("the value, the source, the date...").
    # A plain noun phrase that then ENUMERATES what it means is ordinary English about
    # the table on the page. THE HYPHENATED ADJECTIVE IS THE INTERNAL ONE: "four-field
    # complete", "the four-field register" — shorthand a reader cannot decode, and the
    # form this house actually uses about itself.
    (r"four-field",           "internal shorthand for an input record's shape; the plain "
                              "phrase 'four fields', which the documents then enumerate, "
                              "is ordinary English and is deliberately not matched"),
    (r"\bCRPS\b",             "a scoring rule this house retired from every reader-facing "
                              "surface"),
    (r"\bPARITY\b",           "a retired verdict token, matched in caps because the "
                              "lowercase word is ordinary English (a currency parity)"),
    (r"prose[_ ]figures|table[_ ]footing|table[_ ]residual|research[_ ]protocol",
                              "engine module names"),
]

# ---- DECLARED ORDINARY SENSES, each with its reason and where it may appear ----------
# A term below is NOT scrubbed. Every one is vocabulary the MODEL REPORT ITSELF puts in
# front of a reader, so banning it would mean not printing a section the standard names.
ALLOWED = [
    ("panel",    "the EXPERT VALUATION PANEL is Appendix C in the standard's own section "
                 "list, and a reader is meant to read it. The internal sense of the word "
                 "— a table of scored history — no longer appears in either document."),
    ("register", "the RISK REGISTER and the RESEARCH REGISTER are two of the three parts "
                 "the standard names for Appendix B."),
    ("gate",     "permitted only inside the phrases the standard puts to a reader; the "
                 "internal senses are caught above as `hard gate` and `QC gate`."),
]

DOCS = ("*Valuation_Study*.docx", "*Bibliography*.docx")


def latest(patterns):
    """The newest-dated delivered file for each pattern — a scrub of a superseded
    edition is the L-066/L-067 defect and reports on nothing a reader receives."""
    out = []
    for pat in patterns:
        best, key = None, None
        for f in glob.glob(os.path.join(HERE, pat)):
            m = re.search(r"(\d{2})[-_]?(\d{2})[-_]?(\d{4})", os.path.basename(f))
            if not m:
                continue
            d, mo, y = (int(x) for x in m.groups())
            if key is None or (y, mo, d) > key:
                best, key = f, (y, mo, d)
        if best:
            out.append(best)
    return out


def text_of(path):
    """The words a READER sees, taken out of the delivered file itself.

    Reading the BUILDER instead would miss anything the builder assembles at run time
    and would scrub a file nobody receives — the builder-versus-page distinction this
    house already records of tables.
    """
    pdf = os.path.splitext(path)[0] + ".pdf"
    if os.path.exists(pdf):
        r = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                           capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > 500:
            return r.stdout
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    return re.sub(r"<[^>]+>", " ", xml)


# ---- THE CONTROL, BESIDE THE INSTRUMENT --------------------------------------------
# A CHECK NOBODY HAS SEEN FAIL IS NOT EVIDENCE. The red half carries the six passages
# that ACTUALLY SHIPPED in the delivered bibliography, verbatim, because a fixture
# somebody invented tests the fixture; the clean half carries the ordinary senses and
# the three passages this scrub's own first run wrongly flagged, which is what stops
# the re-point from being quietly widened back.
RED_FIXTURES = [
    "Every historical figure in this study and in the walk-forward behind it comes from "
    "a document GB Corp published itself",
    "The three reported years the study prints come from the walk-forward panel",
    "The panel behind the walk-forward runs from FY2012",
    "The walk-forward targets as long a sourceable history as the filings support",
    "recorded as MISSING with that reason in the walk-forward\u2019s valuation-input "
    "block, and never estimated",
    "which is a hard gate rather than a preference",
]
CLEAN_FIXTURES = [
    "Appendix C \u2014 the expert valuation panel, three methods in one room",
    "Appendix B carries the risk register and the research register",
    "every input carries its own four fields: the value, the source, the date and the "
    "layer it came from",
    "the pound traded at parity with nothing; the peg is not a parity here",
    "the enterprise gate at the plant is not this kind of gate",
]


def self_test():
    bad = []
    for f in RED_FIXTURES:
        if not any(re.search(p, f, 0 if p == r"\bPARITY\b" else re.I)
                   for p, _ in BANNED):
            bad.append("SHIPPED PASSAGE NOT CAUGHT: %s" % f[:78])
    for f in CLEAN_FIXTURES:
        hit = [p for p, _ in BANNED
               if re.search(p, f, 0 if p == r"\bPARITY\b" else re.I)]
        if hit:
            bad.append("ORDINARY SENSE FLAGGED by %s: %s" % (hit[0], f[:60]))
    print("scrub self-test — %d passages that shipped, %d ordinary senses"
          % (len(RED_FIXTURES), len(CLEAN_FIXTURES)))
    for b in bad:
        print("   FAIL  " + b)
    if bad:
        return 1
    print("   every shipped passage is caught; no ordinary sense fires")
    return 0


def main():
    if "--self-test" in sys.argv:
        return self_test()
    files = latest(DOCS)
    if not files:
        print("REFUSED: no delivered document found. An empty population is not a clean "
              "result.")
        return 2
    hits, scanned = [], 0
    for f in files:
        txt = text_of(f)
        if len(txt) < 500:
            print("REFUSED: %s yielded %d characters. A reader that stopped reading "
                  "looks exactly like a clean document."
                  % (os.path.basename(f), len(txt)))
            return 2
        scanned += 1
        for pat, why in BANNED:
            flags = 0 if pat == r"\bPARITY\b" else re.I
            for m in re.finditer(pat, txt, flags):
                a = max(0, m.start() - 60)
                hits.append((os.path.basename(f), m.group(0), why,
                             " ".join(txt[a:m.end() + 60].split())))
    print("external-reader scrub — GBCO")
    print("  documents scanned      %d   %s"
          % (scanned, ", ".join(os.path.basename(f) for f in files)))
    print("  patterns               %d banned, %d ordinary senses declared"
          % (len(BANNED), len(ALLOWED)))
    for term, why in ALLOWED:
        print("     allowed: %-9s %s" % (term, why.split(".")[0]))
    if hits:
        print("\n  HITS %d" % len(hits))
        for fn, term, why, ctx in hits:
            print("     %-42s %-22s %s" % (fn, term, why))
            print("        ...%s..." % ctx)
        print("\nFAILED — a delivered document carries internal-procedure vocabulary.")
        return 1
    print("\n  hits                   0")
    print("\nOK — nothing a reader receives names this house's own procedure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
