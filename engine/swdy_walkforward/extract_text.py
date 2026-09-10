"""Render every filing to text, and RECORD THE ROUTE EACH ONE CAME BY.

[R-FCAL-01]: arithmetic is the arbiter, not the extractor's confidence. A broken
character map yields figures that look perfectly clean and are wrong, so a page that
does not foot is re-read by OCR off the rendered pixels and the route is recorded on
the same footing as the four-field rule.

Route A — the PDF's own text layer, where it carries one.
Route B — OCR at 300 dpi off the rendered pixels (tesseract, eng), where the text
          layer is absent or too thin to be a text layer at all.

The threshold is not a judgement about quality: a filing yielding under 200 characters
PER PAGE has no text layer (SWDY's FY2009 annual statement yields 36 characters across
36 pages — one newline a page). Anything above it is read from the layer AND then held
to its own arithmetic downstream, which is where a broken font map is actually caught.
"""
import os, subprocess, json, sys, hashlib

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
MIN_CHARS_PER_PAGE = 200


def pages(pdf):
    r = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True)
    for ln in r.stdout.splitlines():
        if ln.startswith('Pages:'):
            return int(ln.split()[1])
    return 0


def text_layer(pdf):
    r = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True)
    return r.stdout or ''


def ocr(pdf, npages, dpi=200):
    out = []
    tmp = os.path.join(TEXT, '.ocrtmp')
    for p in range(1, npages + 1):
        subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(p), '-l', str(p), '-png',
                        pdf, tmp], capture_output=True)
        png = None
        for cand in (f'{tmp}-{p}.png', f'{tmp}-{p:02d}.png', f'{tmp}-{p:03d}.png'):
            if os.path.exists(cand):
                png = cand
                break
        if png is None:
            out.append(f'\n=== page {p} — RENDER FAILED ===\n')
            continue
        r = subprocess.run([# The column gap is preserved, or two adjacent columns of space-separated
        # figures merge into one number that parses cleanly and is wrong by twelve
        # orders of magnitude. See fill_pages.py for the measured case.
        'tesseract', png, 'stdout', '-l', 'eng', '--psm', '6',
                        '-c', 'preserve_interword_spaces=1'],
                           capture_output=True, text=True)
        out.append(f'\n=== page {p} ===\n' + (r.stdout or ''))
        os.remove(png)
    return ''.join(out)


def main(only=None, ocr_pass=True):
    routes = {}
    rp = os.path.join(HERE, 'extract_routes.json')
    if os.path.exists(rp):
        routes = json.load(open(rp))
    names = sorted(os.listdir(FILINGS))
    if only:
        names = [n for n in names if any(o in n for o in only)]
    for n in names:
        if not n.lower().endswith('.pdf'):
            continue
        dst = os.path.join(TEXT, n[:-4] + '.txt')
        pdf = os.path.join(FILINGS, n)
        np_ = pages(pdf)
        if n in routes and os.path.exists(dst):
            continue
        t = text_layer(pdf)
        per_page = len(t) / max(np_, 1)
        if per_page >= MIN_CHARS_PER_PAGE:
            route, body = 'text_layer', t
        else:
            if not ocr_pass:
                continue
            route, body = 'ocr_200dpi', ocr(pdf, np_)
        open(dst, 'w', encoding='utf-8').write(body)
        routes[n] = dict(route=route, pages=np_, chars=len(body),
                         text_layer_chars=len(t),
                         sha256=hashlib.sha256(open(pdf, 'rb').read()).hexdigest()[:16])
        json.dump(routes, open(rp, 'w'), indent=1, sort_keys=True)
        print(f'{route:12s} {np_:3d}p {len(body):8d}ch  {n}', flush=True)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    main(args or None, ocr_pass=('--text-only' not in sys.argv))
