"""Dump a text layer for every downloaded AMOC primary document.

AMOC files its statements as SCANS.  Of the annual consolidated filings only
one carries a usable text layer; the rest are images of paper.  So the default
route here is OCR, and the exception is the text layer — the opposite of the
usual arrangement, and worth stating because it sets what the parsing layer is
allowed to trust.

Both routes write the same artefact so downstream parsing does not care which
one a page took, but the route IS recorded per page: an OCR'd figure and a
text-layer figure do not carry the same confidence, and neither is believed
until it foots against its own arithmetic (the arbiter is the arithmetic, not
the extractor's confidence).
"""
import os, subprocess, json, tempfile
import pymupdf

SRC = os.environ.get("AMOC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/50e83873-11d1-59bd-8752-622f52dccf21/scratchpad/amoc_src")
OUT = os.path.join(SRC, "text")
MIN_TEXT = 250          # a statement page carries far more than this


def ocr_page(page, dpi=300, lang="eng"):
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png"))
        png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", lang, "--psm", "6"],
                           capture_output=True, timeout=600)
        return r.stdout.decode("utf-8", "replace")
    finally:
        os.unlink(png)


def main(only=None, lang="eng"):
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    names = sorted(n for n in os.listdir(SRC) if n.lower().endswith(".pdf"))
    if only:
        names = [n for n in names if only in n]
    for i, n in enumerate(names, 1):
        dest = os.path.join(OUT, n[:-4] + ".txt")
        meta = os.path.join(OUT, n[:-4] + ".routes.json")
        if os.path.exists(dest) and os.path.exists(meta):
            manifest[n] = json.load(open(meta))
            continue
        try:
            doc = pymupdf.open(os.path.join(SRC, n))
        except Exception as e:
            manifest[n] = {"error": str(e)}
            continue
        pages, routes = [], []
        for pno, page in enumerate(doc):
            txt = page.get_text()
            route = "text"
            if len(txt.strip()) < MIN_TEXT:
                txt = ocr_page(page, lang=lang)
                route = "ocr300"
            routes.append(route)
            pages.append("\n<<<PAGE %d route=%s>>>\n%s" % (pno + 1, route, txt))
        with open(dest, "w") as f:
            f.write("".join(pages))
        rec = {"pages": len(doc), "routes": routes,
               "ocr": routes.count("ocr300"), "text": routes.count("text")}
        json.dump(rec, open(meta, "w"))
        manifest[n] = rec
        print("[%3d/%d] %-40s %3d pages  ocr=%-3d text=%-3d"
              % (i, len(names), n[:40], len(doc), rec["ocr"], rec["text"]), flush=True)
    json.dump(manifest, open(os.path.join(OUT, "_manifest.json"), "w"), indent=1)
    return manifest


if __name__ == "__main__":
    import sys
    main(only=sys.argv[1] if len(sys.argv) > 1 else None,
         lang=sys.argv[2] if len(sys.argv) > 2 else "eng")
