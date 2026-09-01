"""Render every audited consolidated FS to pixels and OCR the statement pages.

WHY PIXELS.  Every one of ARCC's audited filings is a pure scan -- 11 fiscal
years, 0 characters of text layer between them.  [R-FCAL-01] §1 requires the
figures to be read off the rendered pixels in exactly this case, and requires
the ROUTE each figure came by to be recorded.  Nothing here is typed from
memory and nothing comes from an aggregator: the route is
company PDF -> 300dpi render -> tesseract -> footing check.
"""
import os, subprocess, json, sys
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(HERE, 'filings')
OUT  = os.path.join(HERE, 'ocr')
os.makedirs(OUT, exist_ok=True)

WANT = ('statement of profit', 'statement of financial position', 'statement of cash flow',
        'income statement', 'balance sheet', 'statement of profit or loss')

def ocr_page(pdf, i, tag):
    png = os.path.join(OUT, '%s_p%02d.png' % (tag, i + 1))
    if not os.path.exists(png):
        pdf[i].render(scale=300 / 72).to_pil().save(png)
    r = subprocess.run(['tesseract', png, 'stdout', '--psm', '6'],
                       capture_output=True, text=True)
    return r.stdout

def main():
    only = sys.argv[1:] or None
    index = {}
    for f in sorted(os.listdir(DOCS)):
        tag = f[:-4]
        if not f.endswith('.pdf'): continue
        if not (tag.startswith('FY') or tag.startswith('Q')): continue
        if only and tag not in only: continue
        pdf = pdfium.PdfDocument(os.path.join(DOCS, f))
        hits = []
        # the statements always sit in the first ~14 pages, after the audit report
        for i in range(min(14, len(pdf))):
            t = ocr_page(pdf, i, tag)
            low = t.lower()
            if any(w in low for w in WANT):
                kind = ('IS' if 'profit and loss' in low or 'profit or loss' in low
                        else 'BS' if 'financial position' in low
                        else 'CF' if 'cash flow' in low else '?')
                hits.append({'page': i + 1, 'kind': kind, 'chars': len(t)})
                open(os.path.join(OUT, '%s_p%02d.txt' % (tag, i + 1)), 'w').write(t)
        index[tag] = hits
        print('%-14s %s' % (tag, ' '.join('%s@p%d' % (h['kind'], h['page']) for h in hits)))
    prev = {}
    p = os.path.join(HERE, 'ocr_index.json')
    if os.path.exists(p): prev = json.load(open(p))
    prev.update(index)
    json.dump(prev, open(p, 'w'), indent=1)

if __name__ == '__main__':
    main()
