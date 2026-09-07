"""Fill the IMAGE-ONLY PAGES of a filing that otherwise carries a text layer.

A DOCUMENT-LEVEL ROUTE IS NOT A PAGE-LEVEL ROUTE, and this is the finding that forced
the file: SWDY's FY2025 audited statements yield 329,052 characters over 70 pages —
comfortably a text layer by any density test — and PAGES 3, 4 AND 5 CARRY ONE CHARACTER
EACH. Those three pages are the consolidated statement of financial position and the
statement of changes in equity, so the words "Total assets" occur NOWHERE in the
extracted text of a seventy-page audited annual report, and a parser looking for the
balance sheet finds nothing and reports the filing as carrying none.

The route is recorded PER PAGE, so a figure taken off page 4 is known to have come by
OCR while a figure off page 6 is known to have come off the text layer.
"""
import os, subprocess, json, sys

os.environ.setdefault('OMP_THREAD_LIMIT', '1')

HERE = os.path.dirname(os.path.abspath(__file__))
FILINGS = os.path.join(HERE, 'filings')
TEXT = os.path.join(HERE, 'text')
MIN_CHARS = 200


def npages(pdf):
    r = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True)
    for ln in r.stdout.splitlines():
        if ln.startswith('Pages:'):
            return int(ln.split()[1])
    return 0


def page_text(pdf, p):
    r = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), pdf, '-'],
                       capture_output=True, text=True)
    return r.stdout or ''


def ocr_page(pdf, p, dpi=200):
    tmp = os.path.join(TEXT, f'.fill{os.getpid()}')
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(p), '-l', str(p), '-png', pdf, tmp],
                   capture_output=True)
    png = next((c for c in (f'{tmp}-{p}.png', f'{tmp}-{p:02d}.png', f'{tmp}-{p:03d}.png')
                if os.path.exists(c)), None)
    if png is None:
        return ''
    r = subprocess.run(['tesseract', png, 'stdout', '-l', 'eng', '--psm', '6'],
                       capture_output=True, text=True)
    os.remove(png)
    return r.stdout or ''


def fill(name, dpi=200):
    pdf = os.path.join(FILINGS, name)
    n = npages(pdf)
    out, routes = [], {}
    for p in range(1, n + 1):
        t = page_text(pdf, p)
        if len(t.strip()) >= MIN_CHARS:
            routes[p] = 'text_layer'
        else:
            t = ocr_page(pdf, p, dpi)
            routes[p] = 'ocr_%ddpi' % dpi
        out.append(f'\n=== page {p} [{routes[p]}] ===\n' + t)
    dst = os.path.join(TEXT, name[:-4] + '.filled.txt')
    open(dst, 'w', encoding='utf-8').write(''.join(out))
    rp = os.path.join(HERE, 'page_routes.json')
    all_r = json.load(open(rp)) if os.path.exists(rp) else {}
    all_r[name] = dict(pages=n, routes={str(k): v for k, v in routes.items()},
                       ocr_pages=[p for p, r in routes.items() if r.startswith('ocr')])
    json.dump(all_r, open(rp, 'w'), indent=1, sort_keys=True)
    print(f'{name}: {n} pages, {len(all_r[name]["ocr_pages"])} by OCR -> {os.path.basename(dst)}',
          flush=True)
    return dst


if __name__ == '__main__':
    for a in sys.argv[1:]:
        fill(a)
