"""Render delivered .docx/.xlsx study files to PDF.

THE DELIVERABLE IS A PDF. The Word file is the build artifact; the PDF is what the reader
gets, and no study publishes without one.

Why this script exists. For several editions the house line was "PDF conversion is not
available in this environment — LibreOffice cannot load any spreadsheet or document here".
That was a real symptom with a wrongly-diagnosed cause: LibreOffice was installed, but only
`libreoffice-core` and `libreoffice-common` were — `libreoffice-writer` and
`libreoffice-calc` were absent, so there was no import filter for any document format and
every conversion failed with "source file could not be loaded". Installing the two filter
packages fixes it outright. The lesson is worth keeping: a tool that fails on EVERY input,
including a trivial CSV, is broken or incomplete, not fussy about your file.

Usage:
    python3 engine/make_pdf.py files/X.docx [files/Y.docx ...]
    python3 engine/make_pdf.py --study swdy        # every deliverable for one study

The converter is deliberately strict: a conversion that produces no file, an empty file, or
a PDF whose page count is implausibly low for its source is a FAILURE, not a warning.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SOFFICE = shutil.which('soffice') or shutil.which('libreoffice')

MIN_PAGES = 2          # any real deliverable is longer than one page


def _preflight() -> None:
    if not SOFFICE:
        sys.exit('FAIL: no soffice/libreoffice on PATH')
    prog = '/usr/lib/libreoffice/program'
    missing = [lib for lib in ('libswlo.so', 'libsclo.so')
               if os.path.isdir(prog) and not os.path.exists(os.path.join(prog, lib))]
    if missing:
        sys.exit('FAIL: LibreOffice is installed but its import filters are not — missing '
                 f'{", ".join(missing)}. Install libreoffice-writer and libreoffice-calc; '
                 'without them EVERY conversion fails with "source file could not be loaded".')


def pdf_stats(path: str) -> tuple[int, int]:
    """(pages, embedded images) read straight out of the PDF, no external tool."""
    d = open(path, 'rb').read()
    if not d.startswith(b'%PDF') or not d.rstrip().endswith(b'%%EOF'):
        raise ValueError(f'{path}: not a well-formed PDF')
    return (len(re.findall(rb'/Type\s*/Page[^s]', d)),
            len(re.findall(rb'/Subtype\s*/Image', d)))


def convert(src: str, outdir: str | None = None) -> str:
    src = os.path.abspath(src)
    if not os.path.exists(src):
        sys.exit(f'FAIL: {src} does not exist')
    outdir = os.path.abspath(outdir or os.path.dirname(src))
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, HOME=tmp)
        r = subprocess.run(
            [SOFFICE, '--headless', f'-env:UserInstallation=file://{tmp}/profile',
             '--convert-to', 'pdf', '--outdir', outdir, src],
            capture_output=True, text=True, timeout=600, env=env)
    out = os.path.join(outdir, os.path.splitext(os.path.basename(src))[0] + '.pdf')
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        sys.exit(f'FAIL: {os.path.basename(src)} produced no PDF\n{r.stdout}\n{r.stderr}')
    pages, images = pdf_stats(out)
    if pages < MIN_PAGES:
        sys.exit(f'FAIL: {os.path.basename(out)} has only {pages} page(s) — the conversion '
                 'ran but the content did not come through')
    print(f'  {os.path.basename(src)} -> {os.path.basename(out)}  '
          f'{pages} pages · {images} images · {os.path.getsize(out)/1024:,.0f} KB')
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('sources', nargs='*', help='.docx/.xlsx files to render')
    ap.add_argument('--study', help='render every deliverable of engine/{study}_study')
    ap.add_argument('--outdir', help='where to write (default: alongside the source)')
    a = ap.parse_args()
    _preflight()

    srcs = list(a.sources)
    if a.study:
        d = os.path.join(HERE, f'{a.study}_study')
        srcs += sorted(os.path.join(d, f) for f in os.listdir(d)
                       if f.endswith(('.docx', '.xlsx')) and not f.startswith('~'))
    if not srcs:
        sys.exit('nothing to convert — pass files or --study')

    print(f'rendering {len(srcs)} file(s) to PDF')
    for s in srcs:
        convert(s, a.outdir)
    print('PDF BUILD OK')


if __name__ == '__main__':
    main()
