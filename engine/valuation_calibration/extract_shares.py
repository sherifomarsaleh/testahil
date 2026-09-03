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


# ---------------------------------------------------------------------------
# Parsing the note into a number that FOOTS
# ---------------------------------------------------------------------------
# The sentence these filings actually use is:
#   "issued and paid in capital amounts to EGP 4 344 640 000 representing
#    2 172 320 000 shares with a par value of EGP 2 per share"
# Three numbers, one identity: capital / par = shares. That identity is the whole
# check. OCR misreads digits in ways that look entirely plausible — a 3 for an 8,
# a lost separator — and the only thing that catches it is arithmetic the document
# supplies itself.
#
# The note also RECITES the company's capital history, one board resolution per
# paragraph, going back years. Those recitals are not the current count and must
# not be read as one, which is why the parser anchors on the CURRENT-capital
# sentence ("issued and paid in/up capital amounts to") and never on a bare
# "representing N shares" anywhere on the page.

CURRENT_CAP = re.compile(
    r"issued\s+and\s+paid[\s\-]*(?:in|up)?\s+capital[^0-9]{0,40}"
    r"([\d][\d\s,\.]{6,})\s*(?:representing|,)?\s*([\d][\d\s,\.]{6,})?\s*shares?"
    r"[^0-9]{0,60}?par\s+value[^0-9]{0,20}([\d][\d\s,\.]{0,12})",
    re.I | re.S)


def _n(s):
    if s is None:
        return None
    s = re.sub(r"[^\d.]", "", s.replace(" ", ""))
    s = s.rstrip(".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_note(text):
    """(shares, capital, par, how) from the CURRENT-capital sentence, or Nones."""
    flat = re.sub(r"\s+", " ", text)
    m = CURRENT_CAP.search(flat)
    if not m:
        return None, None, None, "no current-capital sentence on the page"
    cap, sh, par = _n(m.group(1)), _n(m.group(2)), _n(m.group(3))
    if not (cap and sh and par):
        return None, None, None, "the sentence is there and a number in it did not read"
    return sh, cap, par, "issued-and-paid-in-capital sentence"


def foots(shares, capital, par, tol=1e-6):
    """capital / par must reproduce the stated share count. No tolerance worth the
    name: these are exact figures in the document and a mismatch is an OCR error,
    not a rounding one."""
    if not (shares and capital and par):
        return False, "a figure is missing"
    implied = capital / par
    if abs(implied - shares) <= max(tol * shares, 1.0):
        return True, "capital %.0f / par %.4g = %.0f, matching the stated count" % (
            capital, par, implied)
    return False, ("capital %.0f / par %.4g = %.0f against a stated %.0f — the "
                   "document does not foot against itself, so this is an OCR "
                   "misread and the year is dropped"
                   % (capital, par, implied, shares))


def parse_all(ticker="PHDC"):
    p = os.path.join(HERE, "_shares_ocr_%s.json" % ticker.lower())
    src = json.load(open(p, encoding="utf-8"))
    out = {"ticker": ticker, "shares_mn": {}, "dropped": {},
           "rule": ("recorded only where issued capital divided by par value "
                    "reproduces the share count the same document states")}
    for y, rec in sorted(src.get("read", {}).items()):
        best = None
        for pg, txt in rec["text"].items():
            sh, cap, par, how = parse_note(txt)
            ok, why = foots(sh, cap, par)
            if ok:
                best = {"shares_mn": sh / 1e6, "issued_capital": cap, "par_value": par,
                        "page": int(pg), "file": rec["file"], "check": why,
                        "how": how}
                break
            if best is None:
                best = {"failed": why or how, "page": int(pg), "file": rec["file"]}
        if best and "shares_mn" in best:
            out["shares_mn"][y] = best
            print("  %s  %10.2f mn shares   (%s, p%d)"
                  % (y, best["shares_mn"], best["file"][:34], best["page"]))
        else:
            out["dropped"][y] = best or {"failed": "no note text"}
            print("  %s  DROPPED — %s" % (y, (best or {}).get("failed", "?")[:90]))
    q = os.path.join(HERE, "shares_%s.json" % ticker.lower())
    json.dump(out, open(q, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nwrote %s — %d year(s) footed, %d dropped"
          % (os.path.basename(q), len(out["shares_mn"]), len(out["dropped"])))
    return out
