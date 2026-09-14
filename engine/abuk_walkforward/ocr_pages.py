"""Render and OCR pages of a scanned filing.

Every older ABUK filing on the archive shelf is a pure scan (0 characters of
text layer across every page), so every figure taken from one is read off the
rendered pixels.  Route is recorded per figure in the panel.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def ocr(pdf, first, last, dpi=200, lang="ara+eng", psm="6", tag=None):
    base = os.path.splitext(os.path.basename(pdf))[0]
    outdir = os.path.join(HERE, "ocr", tag or base)
    os.makedirs(outdir, exist_ok=True)
    texts = {}
    for p in range(first, last + 1):
        png = os.path.join(outdir, f"p{p:03d}")
        if not os.path.exists(png + ".png"):
            subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(p), "-l", str(p),
                            "-png", "-singlefile", pdf, png], check=True)
        txt = os.path.join(outdir, f"p{p:03d}.{lang}.txt")
        if not os.path.exists(txt):
            r = subprocess.run(["tesseract", png + ".png", "stdout", "-l", lang,
                                "--psm", psm], capture_output=True)
            open(txt, "w").write(r.stdout.decode("utf8", "replace"))
        texts[p] = open(txt).read()
    return texts


if __name__ == "__main__":
    pdf, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    lang = sys.argv[5] if len(sys.argv) > 5 else "ara+eng"
    t = ocr(pdf, first, last, dpi, lang)
    for p, txt in t.items():
        print(f"===== page {p} =====")
        print(txt[:1500])
