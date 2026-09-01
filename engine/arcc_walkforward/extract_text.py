"""Dump a text layer for every ARCC primary document.

EVERY page of every ARCC statement filing is a SCAN — 100% of the pages of the
annual and interim consolidated accounts carry no text layer at all.  So the
default route here is OCR and the exception is the text layer, which is the
opposite of the usual arrangement and sets what the parsing layer is allowed to
trust: the ROUTE IS RECORDED PER PAGE, and no figure is believed until it foots
against its own arithmetic.  [R-FCAL-01]: arithmetic is the arbiter, not the
extractor's confidence.
"""
import os, re, sys, json, subprocess, tempfile
from multiprocessing import Pool
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.join(HERE, "..", "arcc_study")
SCRATCH = os.environ.get("ARCC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/arcc_src")
OUT = os.path.join(SCRATCH, "text")
MIN_TEXT = 250
# Below this many word-like tokens a page is re-read at 90 and 270 degrees and
# the best reading kept.  Set from the measured pair above (25 wrong / 93 right)
# with room on both sides; a genuine cover page scores low, tries the rotations,
# and keeps its upright reading because the rotations score lower still.
UPRIGHT_MIN = 45


# Tesseract flags, chosen by MEASUREMENT on the worst page in the archive
# (FY2021 note page, a heavy scan) rather than by habit.  On that page the
# default invocation ran 144s and the settings below ran 33s and returned a
# BYTE-IDENTICAL 1,598 characters: the cost was tesseract's legacy engine and
# its inverted-image retry pass, neither of which this archive needs.  A
# 133-document OCR at the default would have taken most of a day; the flags are
# a speed choice, not a fidelity one, and the equality of output is the evidence.
OCR_FLAGS = ["--psm", "6", "--oem", "1", "-c", "tessedit_do_invert=0"]

# ONE OpenMP thread per tesseract, and this is the whole difference between a
# twelve-minute extraction and one that never finishes.  Tesseract 5 threads
# each page across every core it can see; four workers each doing that on a
# four-core box oversubscribes it four times over, and the symptom is not an
# error but a page that took two seconds alone taking two MINUTES in the pool
# while the log printed nothing.  Measured both ways on the same document:
# 20 pages in 40s single-process, against 1 page in ~120s inside the pool.
# The parallelism belongs to the pool, not to tesseract.
OCR_ENV = dict(os.environ, OMP_THREAD_LIMIT="1", OMP_NUM_THREADS="1")


def _score(txt):
    """How much of this looks like English words rather than table wreckage.

    A LANDSCAPE page rendered upright OCRs into noise that is still full of
    characters, so length proves nothing: the H1-2026 profit-and-loss page came
    back with 2,444 characters and 25 word-like tokens, while the same page
    turned 90 degrees gave 1,889 characters and 93.  Fewer characters, and the
    right ones."""
    return sum(1 for w in txt.split() if w.isalpha() and len(w) >= 4)


def _ocr(page, dpi, lang, secs, rot=0):
    z = dpi / 72.0
    m = pymupdf.Matrix(z, z) * pymupdf.Matrix(rot)
    pix = page.get_pixmap(matrix=m, colorspace=pymupdf.csGRAY)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png")); png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", lang, *OCR_FLAGS],
                           capture_output=True, timeout=secs, env=OCR_ENV)
        return r.stdout.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return None
    finally:
        os.unlink(png)


def ocr_page(page, dpi=300, lang="eng"):
    """OCR one page, BOUNDED, with the route recorded.

    Most pages in this archive run in one to two seconds.  A handful — dense
    full-page note tables photographed at an angle — run for minutes at 300 dpi
    and would hold a worker indefinitely while the log showed nothing, which is
    an absent answer rather than a slow one [R-ENF-04].  So the page is given 90
    seconds at 300 dpi, then 120 at 150 dpi, and if it still will not resolve it
    is recorded as ocr-failed WITH ITS PAGE NUMBER rather than silently
    returning empty text: a page nobody could read is a fact the panel must
    carry, not a gap it should hide.
    """
    t = _ocr(page, dpi, lang, 90)
    if t is not None and _score(t) >= UPRIGHT_MIN:
        return t, "ocr%d" % dpi
    # Either the page would not resolve upright, or it resolved into wreckage.
    # These filings set their landscape statements sideways in a portrait page
    # box, and every one of them is a PRIMARY statement — the profit and loss,
    # the changes in equity, a note table.  Losing them silently would have left
    # the panel short of exactly the pages it exists to read.
    best, best_rot, best_score = t, 0, _score(t or "")
    for rot in (90, 270):
        r = _ocr(page, dpi, lang, 90, rot=rot)
        if r is not None and _score(r) > best_score:
            best, best_rot, best_score = r, rot, _score(r)
    if best is not None and best_rot:
        return best, "ocr%d-rot%d" % (dpi, best_rot)
    if best is not None:
        return best, "ocr%d" % dpi
    t = _ocr(page, 150, lang, 120)
    if t is not None:
        return t, "ocr150-fallback"
    return "", "ocr-failed"


def sources():
    """Primary documents only — our own delivered study and bibliography are
    output, not evidence, and are excluded by name."""
    out, seen = [], set()
    for d in (STUDY, SCRATCH):
        if not os.path.isdir(d):
            continue
        for n in sorted(os.listdir(d)):
            if not n.lower().endswith(".pdf") or n in seen:
                continue
            if "Valuation_Study" in n or "Bibliography" in n:
                continue
            seen.add(n); out.append(os.path.join(d, n))
    # The ANNUAL consolidated filings and the two current-year interims are the
    # panel's backbone, so they are OCR'd first: a run interrupted part-way then
    # leaves the scoreable window complete rather than the quarterlies complete.
    def rank(p):
        n = os.path.basename(p)
        annual = re.search(r"(FY[_ -]?20\d\d|4Q2023|FY2023|FY2024|FY2025)", n, re.I)
        current = re.search(r"(Q1-2026|Q1_2026|2Q2026)", n, re.I)
        return (0 if current else 1 if annual else 2, n)
    return sorted(out, key=rank)


def one(p):
    n = os.path.basename(p)
    dest = os.path.join(OUT, n[:-4] + ".txt")
    meta = os.path.join(OUT, n[:-4] + ".routes.json")
    if os.path.exists(dest) and os.path.exists(meta):
        return n, json.load(open(meta))
    try:
        doc = pymupdf.open(p)
    except Exception as e:
        return n, {"error": str(e)}
    pages, routes = [], []
    for pno, page in enumerate(doc):
        txt = page.get_text(); route = "text"
        if len(txt.strip()) < MIN_TEXT:
            txt, route = ocr_page(page)
        routes.append(route)
        pages.append("\n<<<PAGE %d route=%s>>>\n%s" % (pno + 1, route, txt))
    open(dest, "w").write("".join(pages))
    rec = {"src": p, "pages": len(doc), "routes": routes,
           "ocr": sum(1 for r in routes if r.startswith("ocr")),
           "text": routes.count("text"),
           "failed": [i + 1 for i, r in enumerate(routes) if r == "ocr-failed"],
           "fallback": [i + 1 for i, r in enumerate(routes) if r == "ocr150-fallback"],
           "rotated": [i + 1 for i, r in enumerate(routes) if "rot" in r]}
    json.dump(rec, open(meta, "w"))
    return n, rec


def main(workers=4):
    os.makedirs(OUT, exist_ok=True)
    paths = sources()
    manifest = {}
    with Pool(workers) as pool:
        for i, (n, rec) in enumerate(pool.imap_unordered(one, paths, chunksize=1), 1):
            manifest[n] = rec
            print("[%3d/%d] %-52s pages=%-4s ocr=%-4s fb=%-3s failed=%s"
                  % (i, len(paths), n[:52], rec.get("pages", "ERR"),
                     rec.get("ocr", "-"), len(rec.get("fallback", [])),
                     rec.get("failed", [])) + "  rot=%s" % (rec.get("rotated") or ""), flush=True)
    json.dump(manifest, open(os.path.join(OUT, "_manifest.json"), "w"), indent=1)
    tot = sum(r.get("pages", 0) for r in manifest.values())
    ocr = sum(r.get("ocr", 0) for r in manifest.values())
    print("\n%d documents, %d pages, %d OCR (%.0f%%)"
          % (len(manifest), tot, ocr, 100.0 * ocr / max(tot, 1)))
    return manifest


if __name__ == "__main__":
    main(workers=int(sys.argv[1]) if len(sys.argv) > 1 else 4)
