#!/usr/bin/env python3
"""SCEM walk-forward — render and OCR the pages of the company's own filings.

THE ROUTE IS OCR OFF THE RENDERED PIXELS AND IT IS RECORDED HERE, per [R-FCAL-01].
Every one of Sinai Cement's six published filings is an image-only scan: pdftotext
returns between 30 and 37 characters for filings of 30 to 36 pages, so no text layer
exists to extract and no extraction confidence is available to trust. ARITHMETIC IS
THE ARBITER — every figure read by this route is footed in panel.py against a
subtotal the filing itself prints, and a misread digit breaks one of those.

OMP_THREAD_LIMIT=1 is not a tuning knob, it is the difference between working and
not: tesseract's OpenMP pool oversubscribes a shared container and the process then
runs for tens of minutes without finishing. Recorded because the first attempt at
this run lost half an hour to it.
"""
import os, subprocess, sys, concurrent.futures

HERE = os.path.dirname(os.path.abspath(__file__))
FILINGS = os.path.join(os.path.dirname(HERE), 'scem_study', 'filings')
OUT = os.path.join(HERE, 'ocr')
os.makedirs(OUT, exist_ok=True)

ENV = dict(os.environ, OMP_THREAD_LIMIT='1')


def page(pdf, tag, pg, lang='eng', dpi=150):
    txt = os.path.join(OUT, '%s_p%02d.txt' % (tag, pg))
    if os.path.exists(txt) and os.path.getsize(txt) > 50:
        return txt
    png = os.path.join(OUT, '%s_p%02d' % (tag, pg))
    subprocess.run(['pdftoppm', '-f', str(pg), '-l', str(pg), '-r', str(dpi), '-gray',
                    '-png', '-singlefile', os.path.join(FILINGS, pdf), png],
                   check=True, env=ENV)
    subprocess.run(['tesseract', png + '.png', png, '-l', lang, '--psm', '6',
                    '-c', 'tessedit_do_invert=0'],
                   check=True, env=ENV, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    os.remove(png + '.png')
    return txt


def run(jobs, workers=3):
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda a: page(*a), jobs))


if __name__ == '__main__':
    pdf, tag, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    lang = sys.argv[5] if len(sys.argv) > 5 else 'eng'
    run([(pdf, tag, p, lang) for p in range(first, last + 1)])
    print('OCR done: %s pages %d-%d' % (tag, first, last))
