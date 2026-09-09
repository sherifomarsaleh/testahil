#!/usr/bin/env python3
"""ADIB walk-forward — dump the primary statement pages of every filing, with the
route each page came by recorded.

[R-FCAL-01 §1] "Accept a statement only if it foots against its own arithmetic ...
re-read any page that does not foot from the rendered pixels, and record which route
each figure came by."

Routes
  text  the PDF's own text layer carries the figures (>= 60 digits on the page)
  ocr   the figures are a raster; the largest embedded image is taken at its NATIVE
        resolution, upscaled 4x LANCZOS, binarised at 150 and read by tesseract psm 6.
        Rendering the PAGE at high dpi does NOT help - these scans are 115-200 dpi and
        a page render only upscales the same pixels through a worse filter. Read at
        400 dpi page-render, FY2020's balance sheet did not foot (equity 5,548,307 vs
        a total-liabilities read of 33,979,364); by this route it foots exactly.
"""
import os, io, sys, json, subprocess, warnings
warnings.filterwarnings('ignore')
import fitz
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FIL = os.path.join(HERE, 'filings')
OUT = os.path.join(HERE, 'pages')
os.makedirs(OUT, exist_ok=True)

SCALE = 4
THRESH = 150
MIN_DIGITS = 60


def _ocr(img):
    g = img.convert('L')
    g = g.resize((g.width * SCALE, g.height * SCALE), Image.LANCZOS)
    g = g.point(lambda x: 0 if x < THRESH else 255)
    tmp = os.path.join(OUT, '_tmp.png')
    g.save(tmp)
    r = subprocess.run(['tesseract', tmp, 'stdout', '-l', 'eng', '--psm', '6',
                        '-c', 'preserve_interword_spaces=1'], capture_output=True)
    return r.stdout.decode('utf-8', 'ignore')


def ocr_page(doc, i):
    """BOTH passes, always, and both are kept.

    Pass A takes the largest embedded image at its NATIVE resolution; pass B renders
    the whole page at 450 dpi. Neither dominates: FY2020's balance sheet reads cleanly
    off the native image and illegibly off a page render, and FY2025's income statement
    (two overlapping JPEGs per page, one of them a mask) is the exact reverse. Keeping
    both is what lets a figure that does not foot on one pass be resolved on the other
    rather than guessed at.
    """
    pg = doc[i]
    best, area = None, 0
    for im in pg.get_images(full=True):
        info = doc.extract_image(im[0])
        a = info['width'] * info['height']
        if a > area:
            area, best = a, info
    a_txt = ''
    if best is not None and area > 200000:
        a_txt = _ocr(Image.open(io.BytesIO(best['image'])))
    pix = pg.get_pixmap(dpi=450, colorspace=fitz.csGRAY)
    b_txt = _ocr(Image.open(io.BytesIO(pix.tobytes('png'))))
    da = sum(c.isdigit() for c in a_txt)
    db = sum(c.isdigit() for c in b_txt)
    body = ('--- pass A: native image x%d (digits=%d) ---\n%s\n'
            '--- pass B: page render 450dpi (digits=%d) ---\n%s' % (SCALE, da, a_txt, db, b_txt))
    return body, 'ocr-both(nativeA=%d,renderB=%d)' % (da, db)


def run(files, first, last):
    mp = os.path.join(OUT, 'manifest.json')
    man = json.load(open(mp)) if os.path.exists(mp) else {}
    for f in files:
        doc = fitz.open(os.path.join(FIL, f))
        hi = min(last, len(doc))
        rec, chunks = [], []
        for i in range(first - 1, hi):
            t = doc[i].get_text()
            digits = sum(c.isdigit() for c in t)
            route = 'text'
            if digits < MIN_DIGITS:
                t, route = ocr_page(doc, i)
            rec.append({'page': i + 1, 'route': route, 'text_layer_digits': digits})
            chunks.append('\n===== PAGE %d [route=%s] =====\n%s' % (i + 1, route, t))
        open(os.path.join(OUT, f[:-4] + '.txt'), 'w', encoding='utf-8').write('\n'.join(chunks))
        man[f] = {'pages_total': len(doc), 'dumped_range': [first, hi], 'pages': rec,
                  'scale': SCALE, 'threshold': THRESH}
        print('%-24s %d-%d  ocr=%d text=%d' % (
            f, first, hi, sum(1 for r in rec if r['route'] != 'text'),
            sum(1 for r in rec if r['route'] == 'text')))
        doc.close()
    json.dump(man, open(mp, 'w'), indent=1)


if __name__ == '__main__':
    run(sys.argv[3:], int(sys.argv[1]), int(sys.argv[2]))
