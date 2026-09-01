"""Pull candidate statement lines out of the OCR'd ARCC filings.

THIS MODULE PROPOSES; IT NEVER DECIDES.  Every ARCC statement page is a scan,
so each figure arrives by OCR and the extractor's confidence is worth nothing.
What this does is produce, for each filing, the labelled lines of the primary
statements with their two columns, so that `panel.py` can carry them with a
source and a page and then FOOT them.  Where the arithmetic refuses, the page
is re-read.  Arithmetic is the arbiter [R-FCAL-01] §1.

The number grammar is deliberately forgiving in one direction only: OCR splits
and joins the thousands separators of these filings freely (12 447 320 081 is
printed correctly, 1160 135 122 has lost a space, 3 222 781.048 has gained a
stop, 5.744. is both).  So digits are read with separators STRIPPED and the
result is checked by footing, never by the shape of what was printed.
"""
import os, re, sys, json

SCRATCH = os.environ.get("ARCC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/arcc_src")
TEXT = os.path.join(SCRATCH, "text")

NUM = re.compile(r"\(?-{0,2}\d[\d  .,]*\d\)?|\(?\d\)?")


def numbers(s):
    """Every number-shaped token on a line, as (value, raw).

    Separators are stripped rather than interpreted: these pages print groups
    with spaces, and OCR turns some of those spaces into stops and drops
    others.  A token is taken as an integer of its digits; a genuine decimal
    (EPS, a ratio) is recovered by the caller from context, never guessed here.
    """
    out = []
    for m in NUM.finditer(s):
        raw = m.group(0)
        neg = raw.startswith("(") or raw.startswith("-")
        digits = re.sub(r"[^\d]", "", raw)
        if not digits:
            continue
        v = int(digits)
        out.append((-v if neg else v, raw))
    return out


def pages(doc):
    """Split an extracted document into (page_no, route, text)."""
    txt = open(os.path.join(TEXT, doc + ".txt"), encoding="utf-8",
               errors="replace").read()
    # The route token carries hyphens once a page has been recovered by
    # rotation (ocr300-rot90) or by the low-dpi fallback, so \w+ silently
    # matched nothing and the whole document came back as one unsplit blob —
    # a parser that returns "no pages" for exactly the pages that needed the
    # most work [R-ENF-04].
    parts = re.split(r"\n<<<PAGE (\d+) route=([\w.-]+)>>>\n", txt)
    out = []
    for i in range(1, len(parts), 3):
        out.append((int(parts[i]), parts[i + 1], parts[i + 2]))
    return out


def find(doc, *needles, limit=None):
    """Pages whose text carries every needle (case-insensitive)."""
    hits = []
    for no, route, t in pages(doc):
        low = t.lower()
        if all(n.lower() in low for n in needles):
            hits.append((no, route, t))
            if limit and len(hits) >= limit:
                break
    return hits


def show(doc, *needles, chars=2600, limit=2):
    for no, route, t in find(doc, *needles, limit=limit):
        print("=" * 70)
        print("%s  page %d  route=%s" % (doc, no, route))
        print("=" * 70)
        print(t[:chars])


def docs():
    return sorted(n[:-4] for n in os.listdir(TEXT) if n.endswith(".txt"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        show(sys.argv[1], *sys.argv[2:])
    else:
        for d in docs():
            print(d)
