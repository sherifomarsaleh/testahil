"""Re-fetch and re-read the primary filings this study is built from.

The filings themselves are ADNOC Drilling's own copyright and are freely
available from its investor-relations site, so they are NOT committed here. This
script reproduces the reading step end to end: it downloads each document to
src/, extracts the text to txt/, and runs optical character recognition over the
pages that are images rather than text.

    python3 fetch_sources.py

Three pages in each annual report are images: the signed consolidated statement
of financial position and the signed pages of the auditor's report. pdfplumber
returns zero characters for them, which is the trigger this script uses to decide
what needs recognising rather than a hand-maintained list.

Requires poppler-utils (pdftoppm) and tesseract-ocr for the image pages.
"""
import os, subprocess, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
S, T, O = (os.path.join(HERE, d) for d in ('src', 'txt', 'ocr'))
BASE = 'https://adnocdrilling.ae/-/media/drilling/files'

DOCS = [
    # (local name, path under BASE)
    ('FY2023_FS.pdf', '2024/fy-2023-results/enfs-adnoc-drilling-pjsc-dec-23-signed.ashx'),
    ('FY2024_FS.pdf', 'fy-2024/4q24-adnoc-drilling---financial-statements---en.ashx'),
    ('FY2025_FS.pdf', '2026/fy-2025-results/fy25-adnoc-drilling_fs_en.ashx'),
    ('Q1_2026_FS.pdf', '2026/1q-2026-results/adnoc-drilling-1q26-financial-statements_en.ashx'),
    ('Q2_2026_FS.pdf', '2026/1h-2026-results/adnoc-drilling-2q26-financial-statements_en.ashx'),
    ('FY2023_MDA.pdf', '2024/fy-2023-results/4q23-adnoc-drilling-mda_en-final.ashx'),
    ('FY2024_MDA.pdf', 'fy-2024/4q24-adnoc-drilling-mda---en.ashx'),
    ('FY2025_MDA.pdf', '2026/fy-2025-results/4q25-adnoc-drilling-mda_en.ashx'),
    ('Q1_2026_MDA.pdf', '2026/1q-2026-results/adnoc-drilling-1q26-mda_en.ashx'),
    ('Q2_2026_MDA.pdf', '2026/1h-2026-results/adnoc-drilling-2q26-mda_en.ashx'),
    ('FY2025_PRES.pdf', '2026/fy-2025-results/adnoc-drilling_earnings-presentation_fy25.ashx'),
    ('Q2_2026_PRES.pdf', '2026/1h-2026-results/adnoc-drilling-2q26-earnings-presentation.ashx'),
    ('Q2_2026_PR.pdf', '2026/1h-2026-results/adnoc-drilling-2q26-press-release_en.ashx'),
    ('Q2_2026_CALL.pdf',
     '2026/1h-2026-results/adnoc-drilling-2q26-earnings-call--webcast-transcript.ashx'),
    ('CORP_PRES_2026.pdf',
     '2026/corporate-presentation/adnoc-drilling---company-presentation---2026.ashx'),
]


def download():
    os.makedirs(S, exist_ok=True)
    for name, path in DOCS:
        dst = os.path.join(S, name)
        if os.path.exists(dst) and os.path.getsize(dst) > 10_000:
            print(f'  {name}: already present')
            continue
        r = subprocess.run(['curl', '-sSL', '--max-time', '120', f'{BASE}/{path}',
                            '-o', dst, '-w', '%{http_code} %{size_download}'],
                           capture_output=True, text=True)
        print(f'  {name}: {r.stdout}')


def extract():
    import pdfplumber
    os.makedirs(T, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(S, '*.pdf'))):
        out = os.path.join(T, os.path.basename(f)[:-4] + '.txt')
        if os.path.exists(out):
            continue
        with pdfplumber.open(f) as pdf:
            parts = ['\n=== PAGE %d ===\n' % (i + 1) + (p.extract_text() or '')
                     for i, p in enumerate(pdf.pages)]
            open(out, 'w').write(''.join(parts))
            print(f'  {os.path.basename(out)}: {len(pdf.pages)} pages')


def ocr():
    """Recognise the pages that carry no extractable characters."""
    import pdfplumber
    from PIL import Image
    os.makedirs(O, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(S, '*.pdf'))):
        stem = os.path.basename(f)[:-4]
        txt_path = os.path.join(T, stem + '.txt')
        if '#### OCR' in open(txt_path).read():
            continue
        with pdfplumber.open(f) as pdf:
            blank = [i + 1 for i, p in enumerate(pdf.pages) if len(p.chars) == 0]
        if not blank:
            continue
        out = []
        for pno in blank:
            png = os.path.join(O, f'{stem}_p{pno}')
            subprocess.run(['pdftoppm', '-r', '400', '-f', str(pno), '-l', str(pno),
                            '-png', f, png], check=True)
            img = glob.glob(png + '*.png')[0]
            txt = subprocess.run(['tesseract', img, 'stdout', '--psm', '6'],
                                 capture_output=True, text=True).stdout
            if len(txt.strip()) < 40:
                for ang in (90, 180, 270):
                    Image.open(img).rotate(ang, expand=True).save(img + f'.r{ang}.png')
                    t2 = subprocess.run(['tesseract', img + f'.r{ang}.png', 'stdout',
                                         '--psm', '6'], capture_output=True, text=True).stdout
                    if len(t2.strip()) > len(txt.strip()):
                        txt = t2
            out.append(f'\n=== OCR PAGE {pno} ===\n{txt}')
            print(f'  {stem} p{pno}: {len(txt.strip())} characters recognised')
        with open(txt_path, 'a') as fh:
            fh.write('\n\n#### OCR OF IMAGE-ONLY PAGES ####\n' + ''.join(out))


if __name__ == '__main__':
    print('downloading the primary filings from adnocdrilling.ae')
    download()
    print('extracting text')
    extract()
    print('recognising the image-only pages')
    ocr()
    print('done — src/ holds the filings, txt/ holds the readable text')
