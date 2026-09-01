#!/usr/bin/env python3
"""EMFD — page extraction: text layer where there is one, OCR off the pixels
where there is not.

[R-FCAL-01] §1: "a page that does not foot is re-read by OCR off the rendered
pixels and the route each figure came by is recorded — ARITHMETIC IS THE
ARBITER, NOT THE EXTRACTOR'S CONFIDENCE."

Four of the eight year-end statements in the company's own register are scans
with no text layer at all, and several of the statement pages inside otherwise
text-layer files are images too. The wide statements (profit or loss, changes in
equity, cash flows) are printed LANDSCAPE and stored rotated, so an OCR pass that
assumes portrait returns fluent-looking garbage rather than an error — which is
why the rotation is chosen by measurement (how many money figures the page
yields) and not assumed.

Everything is cached to the scratch directory: OCR is slow and re-running it on
an unchanged page would change nothing.
"""
import hashlib, json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get(
    "EMFD_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/5c3bac54-80e7-5e98-82bb-8cfd0b2244dd"
    "/scratchpad/emfd_src/pdfs")
CACHE = os.path.join(os.path.dirname(SCRATCH), "ocr_cache")

# A money figure on these statements is at least four digits with thousand
# separators. OCR occasionally drops a space into a group ("2,259,142, 109"), so
# the separator class allows a space and the cleaner closes it up again.
MONEY = re.compile(r"\d{1,3}(?:[,٬]\s?\d{3})+(?:\.\d+)?")


def clean(tok):
    return float(tok.replace(",", "").replace("٬", "").replace(" ", ""))


def money(text):
    return [clean(m.group(0)) for m in MONEY.finditer(text)]


def _ocr(png, lang, psm):
    return subprocess.run(["tesseract", png, "stdout", "-l", lang,
                           "--psm", str(psm)],
                          capture_output=True, text=True).stdout


def page(path, i, lang="eng", dpi=300, force_ocr=False):
    """Return (text, route, rotation).

    route is 'text' when the PDF carried a text layer for this page and 'ocr'
    when the pixels had to be read. The rotation is the one that yielded the most
    money figures; ties keep the lower rotation. Portrait pages therefore stay
    portrait without a special case, and a landscape statement is found by
    measurement rather than by a rule about page numbers.
    """
    import pymupdf
    doc = pymupdf.open(path)
    if not force_ocr:
        t = doc[i].get_text()
        if t.strip():
            return t, "text", 0

    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha256(("%s|%d|%s|%d" % (os.path.basename(path), i, lang,
                                           dpi)).encode()).hexdigest()[:24]
    cached = os.path.join(CACHE, key + ".json")
    if os.path.exists(cached):
        d = json.load(open(cached))
        return d["text"], "ocr", d["rotation"]

    best = None
    for rot in (0, 90, 180, 270):
        m = pymupdf.Matrix(dpi / 72.0, dpi / 72.0).prerotate(rot)
        png = os.path.join(CACHE, key + ".png")
        doc[i].get_pixmap(matrix=m).save(png)
        t = _ocr(png, lang, 6)
        n = len(MONEY.findall(t))
        if best is None or n > best[0]:
            best = (n, rot, t)
        if rot == 0 and n >= 8:
            break                      # portrait and clearly readable; stop
    os.path.exists(os.path.join(CACHE, key + ".png")) and \
        os.remove(os.path.join(CACHE, key + ".png"))
    json.dump({"text": best[2], "rotation": best[1]}, open(cached, "w"))
    return best[2], "ocr", best[1]


def find_statement(path, patterns, lang="eng", pages=14, min_money=8,
                   dpi=300):
    """First page that matches one of `patterns` AND carries enough money
    figures to be the statement rather than the table of contents naming it."""
    import pymupdf
    doc = pymupdf.open(path)
    for i in range(min(pages, doc.page_count)):
        text, route, rot = page(path, i, lang, dpi=dpi)
        if len(MONEY.findall(text)) < min_money:
            continue
        for p in patterns:
            if re.search(p, text, re.I):
                return i, text, route, rot
    return None, None, None, None


PL = [r"STATEMENT\s+OF\s+PROFIT\s+OR\s+LOSS", r"INCOME\s+STATEMENT",
      r"قائمة\s+الدخل"]
BS = [r"STATEMENT\s+OF\s+FINANCIAL\s+POSITION", r"BALANCE\s+SHEET",
      r"الميزانية"]
CF = [r"STATEMENT\s+OF\s+CASH\s+FLOWS?",
      r"قائمة\s+التدفقات"]


if __name__ == "__main__":
    import sys
    f = os.path.join(SCRATCH, sys.argv[1])
    lang = sys.argv[2] if len(sys.argv) > 2 else "eng"
    for name, pats in (("profit or loss", PL), ("financial position", BS),
                       ("cash flows", CF)):
        i, t, route, rot = find_statement(f, pats, lang)
        print("== %-20s page %s route %s rot %s money %s"
              % (name, i, route, rot, len(MONEY.findall(t or ""))))
        if t and "-v" in sys.argv:
            print(t[:1500])
