"""Dump a text layer for every downloaded TMGH primary document.

Text-layer PDFs go through PyMuPDF. Pages whose text layer is thin go through
tesseract at 300 dpi. Both write the same shape of artefact so downstream
parsing does not care which route a page took — but the route IS recorded,
because an OCR'd number and a text-layer number do not carry the same
confidence, and a broken character map yields figures that look perfectly
clean and are wrong.
"""
import os, subprocess, sys, json, tempfile, re
import pymupdf

SRC = os.environ.get("TMGH_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/ba35918b-2c34-5691-9e47-05ae974e86f1/scratchpad/tmgh_src")
OUT = os.path.join(SRC, "text")
MIN_TEXT = 400           # a results/statement page carries far more than this


def ocr_page(page, dpi=300):
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png"))
        png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", "eng", "--psm", "6"],
                           capture_output=True, timeout=300)
        return r.stdout.decode("utf-8", "replace")
    finally:
        os.unlink(png)


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    names = sorted(n for n in os.listdir(SRC) if n.lower().endswith(".pdf"))
    if only:
        names = [n for n in names if only.lower() in n.lower()]
    for i, n in enumerate(names, 1):
        dest = os.path.join(OUT, n[:-4] + ".txt")
        meta = os.path.join(OUT, n[:-4] + ".routes.json")
        if os.path.exists(dest) and os.path.exists(meta):
            manifest[n] = json.load(open(meta))
            continue
        try:
            doc = pymupdf.open(os.path.join(SRC, n))
        except Exception as e:
            manifest[n] = {"error": "%s: %s" % (type(e).__name__, e)}
            continue
        routes, chunks = [], []
        for pno in range(doc.page_count):
            page = doc[pno]
            t = page.get_text("text")
            route = "text"
            if len(t.strip()) < MIN_TEXT:
                try:
                    t2 = ocr_page(page)
                    if len(t2.strip()) > len(t.strip()):
                        t, route = t2, "ocr"
                except Exception as e:
                    route = "text(ocr-failed:%s)" % type(e).__name__
            routes.append(route)
            chunks.append("\n<<<PAGE %d route=%s>>>\n%s" % (pno + 1, route, t))
        doc.close()
        with open(dest, "w") as f:
            f.write("".join(chunks))
        rec = {"pages": len(routes), "routes": routes,
               "ocr_pages": sum(1 for r in routes if r == "ocr")}
        json.dump(rec, open(meta, "w"))
        manifest[n] = rec
        print("[%3d/%3d] %-70s %3d pages, %d OCR" % (i, len(names), n[:70], rec["pages"], rec["ocr_pages"]))
    json.dump(manifest, open(os.path.join(OUT, "_manifest.json"), "w"), indent=1)
    tot = sum(m.get("pages", 0) for m in manifest.values())
    ocr = sum(m.get("ocr_pages", 0) for m in manifest.values())
    err = [k for k, m in manifest.items() if "error" in m]
    print("\n%d documents, %d pages, %d via OCR, %d unreadable" % (len(manifest), tot, ocr, len(err)))
    for k in err:
        print("   UNREADABLE", k, manifest[k]["error"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
