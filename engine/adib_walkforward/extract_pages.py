#!/usr/bin/env python3
"""ADIB walk-forward — dump the primary statement pages of every filing.

Route is recorded per page: 'text' where the PDF's own text layer carries the
figures, 'ocr' where it does not. [R-FCAL-01 §1] — a page that does not foot is
re-read from the rendered pixels, and the route each figure came by is recorded.
"""
import os, re, sys, json, subprocess, warnings
warnings.filterwarnings('ignore')
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
FIL = os.path.join(HERE, 'filings')
OUT = os.path.join(HERE, 'pages')
os.makedirs(OUT, exist_ok=True)

DPI = 400

def ocr_page(doc, i):
    pg = doc[i]
    pix = pg.get_pixmap(dpi=DPI)
    png = os.path.join(OUT, '_tmp.png')
    pix.save(png)
    r = subprocess.run(['tesseract', png, 'stdout', '-l', 'eng', '--psm', '6',
                        '-c', 'preserve_interword_spaces=1'],
                       capture_output=True)
    return r.stdout.decode('utf-8', 'ignore')

def main(files, first, last):
    manifest = {}
    for f in files:
        p = os.path.join(FIL, f)
        doc = fitz.open(p)
        n = len(doc)
        hi = min(last, n)
        rec = []
        chunks = []
        for i in range(first - 1, hi):
            t = doc[i].get_text()
            digits = sum(c.isdigit() for c in t)
            route = 'text'
            if digits < 60:
                t = ocr_page(doc, i)
                route = 'ocr'
            rec.append({'page': i + 1, 'route': route, 'digits': digits})
            chunks.append('\n===== PAGE %d [route=%s] =====\n%s' % (i + 1, route, t))
        base = f[:-4]
        open(os.path.join(OUT, base + '.txt'), 'w', encoding='utf-8').write('\n'.join(chunks))
        manifest[f] = {'pages_total': n, 'dumped': rec}
        print('%-24s pages %d-%d  ocr=%d text=%d'
              % (f, first, hi, sum(1 for r in rec if r['route'] == 'ocr'),
                 sum(1 for r in rec if r['route'] == 'text')))
        doc.close()
    mp = os.path.join(OUT, 'manifest.json')
    old = json.load(open(mp)) if os.path.exists(mp) else {}
    old.update(manifest)
    json.dump(old, open(mp, 'w'), indent=1)

if __name__ == '__main__':
    main(sys.argv[3:], int(sys.argv[1]), int(sys.argv[2]))
