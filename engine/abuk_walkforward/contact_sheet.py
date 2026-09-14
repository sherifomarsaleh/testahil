"""Contact sheet of a scanned filing, to LOCATE pages before reading them.

Arabic OCR on these scans runs minutes per page and mangles Eastern-Arabic
numerals, so figures are read off the rendered pixels directly.  This builds a
low-resolution grid so the primary statements can be found without rendering
every page at reading resolution.
"""
import os, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def sheet(pdf, first, last, out, cols=5, thumb=430, dpi=45):
    tmp = os.path.join(HERE, "ocr", "_sheet")
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(first), "-l", str(last),
                    "-png", pdf, os.path.join(tmp, "s")], check=True)
    files = sorted(f for f in os.listdir(tmp) if f.startswith("s-") or f.startswith("s"))
    files = [f for f in files if f.endswith(".png")]
    ims = []
    for f in files:
        im = Image.open(os.path.join(tmp, f))
        im.thumbnail((thumb, thumb))
        ims.append((f, im))
    if not ims:
        raise SystemExit("no pages rendered")
    w = max(i.width for _, i in ims)
    h = max(i.height for _, i in ims)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * (w + 6), rows * (h + 18)), "white")
    from PIL import ImageDraw
    d = ImageDraw.Draw(canvas)
    for k, (f, im) in enumerate(ims):
        r, c = divmod(k, cols)
        x, y = c * (w + 6), r * (h + 18)
        canvas.paste(im, (x, y + 16))
        num = "".join(ch for ch in f if ch.isdigit())
        d.text((x + 3, y + 2), f"p{int(num)}", fill="black")
    canvas.save(out)
    for f in files:
        os.remove(os.path.join(tmp, f))
    print(out, canvas.size, len(ims), "pages")


if __name__ == "__main__":
    sheet(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
