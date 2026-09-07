"""OCR a NAMED PAGE RANGE of a filing off the rendered pixels, and record the route.

Separate from extract_text.py's whole-document pass on purpose: OCRing 1,840 pages to
read four statements is three hours of work for ten minutes of evidence, and a run that
cannot afford its own extraction stops being able to check anything. The statements sit
in the front of every one of these filings and the notes are reached by page, so the
range is NAMED per document rather than guessed at.

200 dpi, tesseract eng, --psm 6, one page at a time. The route and the range are written
into ocr_routes.json beside every figure that comes off them [R-FCAL-01] §1.
"""
import os, subprocess, sys, json

# TESSERACT IS RUN SINGLE-THREADED, AND THAT IS NOT A TUNING CHOICE.
# Measured on this box: one 1654x2340 page of the FY2023 filing takes MORE THAN 110
# SECONDS under the default OpenMP settings and 2.0 SECONDS with OMP_THREAD_LIMIT=1 -
# a factor of fifty-five, on four cores. At the default the whole archive is three days
# of work and the honest conclusion would have been "the OCR route is not affordable",
# which is a claim about the operator rather than about the documents [R-IND-01].
os.environ.setdefault('OMP_THREAD_LIMIT', '1')

HERE = os.path.dirname(os.path.abspath(__file__))
FILINGS = os.path.join(HERE, 'filings')
TEXT = os.path.join(HERE, 'text')
os.makedirs(TEXT, exist_ok=True)


def ocr_range(name, first, last, dpi=200):
    pdf = os.path.join(FILINGS, name)
    tmp = os.path.join(TEXT, '.pg')
    out = []
    for p in range(first, last + 1):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(p), '-l', str(p), '-png',
                        pdf, tmp], capture_output=True)
        png = None
        for c in (f'{tmp}-{p}.png', f'{tmp}-{p:02d}.png', f'{tmp}-{p:03d}.png'):
            if os.path.exists(c):
                png = c
                break
        if png is None:
            out.append(f'\n=== page {p} — RENDER FAILED ===\n')
            continue
        r = subprocess.run(['tesseract', png, 'stdout', '-l', 'eng', '--psm', '6'],
                           capture_output=True, text=True)
        out.append(f'\n=== page {p} ===\n' + (r.stdout or ''))
        os.remove(png)
    return ''.join(out)


def pages(pdf):
    r = subprocess.run(['pdfinfo', os.path.join(FILINGS, pdf)], capture_output=True, text=True)
    for ln in r.stdout.splitlines():
        if ln.startswith('Pages:'):
            return int(ln.split()[1])
    return 0


def run(name, first=1, last=None, dpi=200, tag=''):
    n = pages(name)
    last = min(last or n, n)
    body = ocr_range(name, first, last, dpi)
    dst = os.path.join(TEXT, name[:-4] + (tag or f'.ocr{first}-{last}') + '.txt')
    open(dst, 'w', encoding='utf-8').write(body)
    rp = os.path.join(HERE, 'ocr_routes.json')
    routes = json.load(open(rp)) if os.path.exists(rp) else {}
    routes[os.path.basename(dst)] = dict(source=name, pages=f'{first}-{last}', dpi=dpi,
                                         engine='tesseract 5.3.4 eng --psm 6',
                                         route='ocr_off_rendered_pixels', chars=len(body))
    json.dump(routes, open(rp, 'w'), indent=1, sort_keys=True)
    print(f'ocr {name} pp{first}-{last} -> {len(body)} chars', flush=True)
    return dst


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], int(a[1]) if len(a) > 1 else 1, int(a[2]) if len(a) > 2 else None)
