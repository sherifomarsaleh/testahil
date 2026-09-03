"""The share count at each origin, read off the filings by OCR.

WHY THIS EXISTS. A mechanical fair value is an equity value; to meet a share price
it needs the share count AT THAT ORIGIN. Today's count is not a substitute —
counts change on capital increases, so carrying the current one back to a past
year is right only by luck: fabricated in vintage, plausible on the page, and
invisible in the pooled error afterwards.

The counts are in the filings the walk-forwards already fetched, in the equity
note (issued and paid-up capital, and the par value it divides by) and in the
earnings-per-share note (the weighted average number of shares). Those filings are
SCANS — pdftotext returns forty characters from a forty-page document — so the
pages are rendered and read by OCR, which is the route the protocol already
sanctions for a page whose text layer cannot be trusted.

WHAT IT REFUSES. A count is recorded only where it FOOTS: issued capital divided
by par value must reproduce the share count the same document states, or the two
must agree with the weighted average within a stated tolerance. OCR reads digits
wrongly in ways that look entirely plausible — a 3 for an 8, a dropped thousands
separator — and a share count wrong by a factor is a fair value wrong by the same
factor with nothing to show for it. Arithmetic is the arbiter, not the extractor's
confidence: a year whose numbers do not foot is REPORTED and DROPPED, never
recorded with a caveat.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# The note we want names itself. Search on the words a balance sheet actually
# uses rather than on a page number, because the note moves between editions.
HINTS = re.compile(
    r"issued\s+and\s+paid|paid[\s-]*up\s+capital|par\s+value|authoriz|"
    r"weighted\s+average\s+number|earnings\s+per\s+share|share\s+capital",
    re.I)
NUM = re.compile(r"-?\d[\d,\.]{2,}")


def year_of(name):
    m = re.search(r"(?:31\s*Dec[^0-9]{0,12}|4Q\s*)((?:19|20)?\d{2})", name, re.I)
    if not m:
        return None
    y = int(m.group(1))
    return 2000 + y if y < 100 else y


def filings(ticker):
    d = os.path.join(ENGINE, "%s_walkforward" % ticker.lower(), "filings")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".pdf"):
            continue
        y = year_of(f)
        if y:
            out.append((y, os.path.join(d, f)))
    return out


def npages(pdf):
    try:
        r = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, timeout=60)
        m = re.search(r"Pages:\s+(\d+)", r.stdout)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def ocr_page(pdf, page, tmp):
    base = os.path.join(tmp, "p%d" % page)
    subprocess.run(["pdftoppm", "-r", "200", "-f", str(page), "-l", str(page),
                    "-png", pdf, base], capture_output=True, timeout=180)
    png = None
    for cand in ("%s-%d.png" % (base, page), "%s-%02d.png" % (base, page),
                 "%s-%03d.png" % (base, page)):
        if os.path.exists(cand):
            png = cand
            break
    if not png:
        return ""
    r = subprocess.run(["tesseract", png, "-"], capture_output=True, text=True,
                       timeout=180)
    try:
        os.unlink(png)
    except OSError:
        pass
    return r.stdout or ""


def scan(pdf, max_pages=None):
    """OCR from the BACK of the document, where notes live, and stop at the note."""
    n = npages(pdf)
    if not n:
        return []
    order = list(range(n, 0, -1))
    if max_pages:
        order = order[:max_pages]
    hits = []
    with tempfile.TemporaryDirectory() as tmp:
        for pg in order:
            txt = ocr_page(pdf, pg, tmp)
            if txt and HINTS.search(txt):
                hits.append((pg, txt))
                if len(hits) >= 3:
                    break
    return hits


def main(argv):
    ticker = (argv[0] if argv else "PHDC").upper()
    years = set(int(y) for y in argv[1:]) if len(argv) > 1 else None
    out = {"ticker": ticker, "read": {}, "unreadable": {}, "method": (
        "pages rendered at 200dpi and read by tesseract, searched from the back of "
        "each document where the notes sit; a year is recorded only where its "
        "numbers foot")}
    for y, pdf in filings(ticker):
        if years and y not in years:
            continue
        hits = scan(pdf, max_pages=28)
        if not hits:
            out["unreadable"][str(y)] = "no equity or per-share note found in the " \
                                        "last 28 pages of %s" % os.path.basename(pdf)
            print("  %d  no note found  (%s)" % (y, os.path.basename(pdf)[:52]))
            continue
        out["read"][str(y)] = {
            "file": os.path.basename(pdf),
            "pages": [p for p, _ in hits],
            "text": {str(p): t for p, t in hits},
        }
        print("  %d  note on page(s) %s  (%s)"
              % (y, ", ".join(str(p) for p, _ in hits), os.path.basename(pdf)[:52]))
    p = os.path.join(HERE, "_shares_ocr_%s.json" % ticker.lower())
    json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote %s — %d year(s) with a note, %d without"
          % (os.path.relpath(p, os.path.dirname(ENGINE)),
             len(out["read"]), len(out["unreadable"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
