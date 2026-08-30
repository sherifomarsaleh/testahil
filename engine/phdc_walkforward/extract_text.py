"""Dump a text layer for every downloaded PHDC primary document.

Text-layer PDFs go through PyMuPDF. Image-only PDFs go through tesseract at
300 dpi. Both write the same shape of artefact so downstream parsing does not
care which route a page took — but the route IS recorded, because an OCR'd
number and a text-layer number do not carry the same confidence.
"""
import os, subprocess, sys, json, tempfile
import pymupdf

SRC = os.environ.get("PHDC_SCRATCH",
    "/tmp/claude-0/-home-user-testahil/2283e95e-66db-5f22-bba6-0db833f32495/scratchpad/phdc_src")
OUT = os.path.join(SRC, "text")
MIN_TEXT = 2000          # a real statement page carries far more than this


def ocr_page(page, dpi=300):
    pix = page.get_pixmap(dpi=dpi)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        t.write(pix.tobytes("png"))
        png = t.name
    try:
        r = subprocess.run(["tesseract", png, "stdout", "-l", "eng", "--psm", "6"],
                           capture_output=True, timeout=180)
        return r.stdout.decode("utf-8", "replace")
    finally:
        os.unlink(png)


def main(only=None, max_pages=None):
    os.makedirs(OUT, exist_ok=True)
    manifest = {}
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".pdf"))
    if only:
        files = [f for f in files if any(o in f for o in only)]
    for f in files:
        stem = f[:-4]
        dst = os.path.join(OUT, stem + ".txt")
        doc = pymupdf.open(os.path.join(SRC, f))
        native = sum(len(doc[p].get_text()) for p in range(len(doc)))
        route = "text" if native > MIN_TEXT else "ocr"
        if os.path.exists(dst) and os.path.getsize(dst) > 1000:
            manifest[stem] = {"route": route, "pages": len(doc), "cached": True}
            doc.close()
            continue
        n = len(doc) if max_pages is None else min(max_pages, len(doc))
        parts = []
        for p in range(n):
            parts.append("\n<<<PAGE %d>>>\n" % p)
            parts.append(doc[p].get_text() if route == "text" else ocr_page(doc[p]))
        open(dst, "w", encoding="utf-8").write("".join(parts))
        manifest[stem] = {"route": route, "pages": n, "chars": sum(len(x) for x in parts)}
        doc.close()
        print("%-16s %-5s %3d pages  %7d chars" % (stem, route, n, manifest[stem]["chars"]),
              flush=True)
    json.dump(manifest, open(os.path.join(OUT, "_manifest.json"), "w"), indent=1)
    print("done:", len(manifest), "documents")


if __name__ == "__main__":
    only = sys.argv[1:] or None
    main(only)
