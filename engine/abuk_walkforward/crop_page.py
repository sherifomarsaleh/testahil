"""Render one page of a scanned filing at reading resolution and cut it into
horizontal strips, upscaled, so figures can be read off the pixels.

Every pre-FY2024 ABUK filing is a pure scan in Arabic with Eastern-Arabic
numerals; tesseract's Arabic model runs minutes per page on these and mangles
the digits, so the route for every figure taken from them is
"OCR route: read off rendered pixels" and the strip is the evidence.
"""
import os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/claude-0/-home-user-testahil/82898002-da86-5df7-8203-457959546ece/scratchpad/strips"


def strips(pdf, page, n=3, dpi=400, x0=0.03, x1=0.75, y0=0.10, y1=0.92, tag=""):
    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, f"{tag or os.path.basename(pdf)[:12]}_p{page}")
    if not os.path.exists(base + ".png"):
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page),
                        "-png", "-singlefile", pdf, base], check=True)
    im = Image.open(base + ".png")
    w, h = im.size
    made = []
    span = (y1 - y0) / n
    for k in range(n):
        a = y0 + k * span
        b = min(y1, a + span * 1.08)
        c = im.crop((int(x0 * w), int(a * h), int(x1 * w), int(b * h)))
        sc = min(2.0, 4200 / max(1, c.width))
        c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
        p = f"{base}_s{k+1}.png"
        c.save(p)
        made.append((p, c.size))
    for p, s in made:
        print(p, s)


if __name__ == "__main__":
    a = sys.argv
    strips(a[1], int(a[2]), int(a[3]) if len(a) > 3 else 3,
           tag=a[4] if len(a) > 4 else "")
