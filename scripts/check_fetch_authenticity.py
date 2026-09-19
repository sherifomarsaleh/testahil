#!/usr/bin/env python3
"""[R-ENF-01] A SAVED FILE IS CHECKED AGAINST WHAT IT ACTUALLY CONTAINS, NOT ITS NAME.

SIGCM clause 1 says historicals come from the company's own sources and that a figure is
never invented, estimated or interpolated. Every instrument built for it so far reads what a
study SAYS its source was. None of them ever opened the file.

WHAT THAT MISSES, FOUND ON 09-09-2026 ACROSS THE TRACKED TREE. A fetch that a firewall
refuses does not fail loudly. It returns 200 with a rejection page in the body, the fetcher
writes that body to the filename it intended, and a filing that was never obtained sits in
the study's own filings directory under a filing's name:

    engine/raya_study_pending/filings/CBE_MPR_Q1_2026.pdf     269 bytes, "Request Rejected"
    engine/ocdi_study_pending/src/pdf/bodsum_6_2_2025.pdf      94 bytes, {"error":404}
    engine/ocdi_study_pending/src/cbe.html                    269 bytes, "Request Rejected"

The third one is why this gate has TWO tests and not one. It is real HTML with a .html
extension, so nothing about its type is a lie — only its content is. A reader that opens it
for the policy rate finds no rate, reports "not disclosed", and the study proceeds on a
negative that was manufactured by a firewall. That is [L-355] with an outside cause.

TEST 1 — THE EXTENSION MUST NOT LIE ABOUT THE TYPE. Magic bytes against extension, over
every tracked file whose extension names a binary format.

TEST 2 — THE BODY MUST NOT BE A KNOWN BLOCK PAGE. A closed list of signatures that only
ever appear in a WAF rejection, a bot challenge or an API error envelope, tested on every
tracked file under a study's own source directories whatever its extension. The list is
closed on purpose: a heuristic here would fire on real filings that quote the words.

EXCEPTIONS ARE NAMED WITH THEIR REASON, NEVER PATTERNED. Two publishers ship a file whose
extension is wrong at source, and one delivered artefact was already found, flagged and
deliberately left intact. Each is listed by exact path with the reason it is allowed, so a
NEW file of the same shape still fails.

THE POPULATION IS ANCHORED [R-ENF-04]: examining zero files FAILS, and a file that cannot be
read is a failure rather than a skip — unreadability is the cheapest route past any gate.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- test 1: type
MAGIC = {
    '.pdf':  (b'%PDF',),
    '.xlsx': (b'PK\x03\x04',),
    '.docx': (b'PK\x03\x04',),
    '.pptx': (b'PK\x03\x04',),
    '.zip':  (b'PK\x03\x04', b'PK\x05\x06'),
    '.xls':  (b'\xd0\xcf\x11\xe0',),
    '.doc':  (b'\xd0\xcf\x11\xe0',),
    '.png':  (b'\x89PNG\r\n\x1a\n',),
    '.jpg':  (b'\xff\xd8\xff',),
    '.jpeg': (b'\xff\xd8\xff',),
    '.gif':  (b'GIF87a', b'GIF89a'),
}

# Exact paths only. Each carries the reason it is allowed. A pattern here would let the
# next fetch failure through on the strength of where it landed.
TYPE_EXCEPTIONS = {
    'engine/scem_walkforward/weo/WEOApr2025all.xls':
        "the IMF's own World Economic Outlook release: UTF-16LE tab-delimited text shipped "
        "under a .xls name by the publisher. Read as text by scem_walkforward/macro.py.",
    'engine/scem_walkforward/weo/WEOOct2024all.xls':
        "the IMF's own World Economic Outlook release, same shape as the April 2025 file.",
    'files/PHDC_Valuation_Study_09-06-2026_public.docx':
        "Markdown delivered under a .docx name in June 2026. Found and flagged on "
        "28-07-2026 (Horizon_Naming_Calendar_Only_20260728.md) and deliberately left "
        "intact: rewriting a delivered document is a different act from fixing a build. "
        "It is not linked from the site — archive.html and editions.json name the PDF.",
    'legacy/files/PHDC_Valuation_Study_09-06-2026_public.docx':
        "the archived copy of the same delivered artefact, byte-identical.",
}

# ------------------------------------------------------- test 2: block pages
# Every entry was read off an actual captured body in this repo or is the vendor's own
# fixed marker. Nothing here is a guess about what a block page might say.
BLOCK_SIGNATURES = (
    (b'<title>Request Rejected</title>',        'F5/BIG-IP ASM rejection page'),
    (b'The requested URL was rejected',         'F5/BIG-IP ASM rejection page'),
    (b'window["bobcmn"]',                       'Imperva/Incapsula bot challenge'),
    (b'Incapsula incident ID',                  'Imperva/Incapsula block page'),
    (b'cf-browser-verification',                'Cloudflare browser challenge'),
    (b'Attention Required! | Cloudflare',       'Cloudflare block page'),
    (b'Checking your browser before accessing', 'Cloudflare interstitial'),
    (b'<title>403 Forbidden</title>',           'server 403 page saved as a document'),
    (b'<title>404 Not Found</title>',           'server 404 page saved as a document'),
    (b'"status":404',                           'API 404 envelope saved as a document'),
    (b'"status": 404',                          'API 404 envelope saved as a document'),
    (b'Access Denied</title>',                  'CDN access-denied page'),
    (b'AccessDenied</Code>',                    'S3 AccessDenied XML saved as a document'),
)

# Where a study keeps what it fetched. A block page anywhere under one of these is a
# source that was never obtained, whatever its extension says.
SOURCE_DIRS = ('/filings/', '/src/', '/sources/', '/ocr/', '/raw/', '/weo/', '/pages/')

BLOCK_EXCEPTIONS = {}

# A body only counts if it is small enough to BE a block page. A real filing that quotes
# one of these strings runs to hundreds of kilobytes; every captured block page in this
# repo is under 8 KB. Stated as a number so it can be argued with.
BLOCK_MAX_BYTES = 65536


def tracked(root):
    p = subprocess.run(['git', 'ls-files', '-z'], cwd=root,
                       capture_output=True, check=True)
    return [f for f in p.stdout.decode('utf-8', 'surrogateescape').split('\0') if f]


def survey(root, files):
    """(type failures, block failures, files examined by each test)."""
    type_bad, block_bad, n_type, n_block = [], [], 0, 0
    for rel in files:
        path = os.path.join(root, rel)
        ext = os.path.splitext(rel)[1].lower()
        in_source = any(d in '/' + rel for d in SOURCE_DIRS)
        if ext not in MAGIC and not in_source:
            continue
        try:
            with open(path, 'rb') as fh:
                head = fh.read(BLOCK_MAX_BYTES)
            size = os.path.getsize(path)
        except OSError as exc:
            type_bad.append((rel, 'UNREADABLE — %s' % exc))
            continue

        if ext in MAGIC:
            n_type += 1
            if not any(head.startswith(m) for m in MAGIC[ext]):
                if rel not in TYPE_EXCEPTIONS:
                    type_bad.append((rel, '%d bytes, starts %r — not a %s'
                                     % (size, head[:12], ext.lstrip('.').upper())))

        if in_source and size <= BLOCK_MAX_BYTES:
            n_block += 1
            for sig, what in BLOCK_SIGNATURES:
                if sig in head and rel not in BLOCK_EXCEPTIONS:
                    block_bad.append((rel, '%d bytes, %s (%r)' % (size, what, sig)))
                    break
    return type_bad, block_bad, n_type, n_block


def main():
    root = ROOT
    files = tracked(root)
    type_bad, block_bad, n_type, n_block = survey(root, files)

    print('FETCH AUTHENTICITY — what is in the file, not what it is called')
    print('  tracked files:                       %d' % len(files))
    print('  test 1  extension vs magic bytes:    %d examined, %d named exception(s)'
          % (n_type, len(TYPE_EXCEPTIONS)))
    print('  test 2  block-page signatures:       %d examined, %d signature(s)'
          % (n_block, len(BLOCK_SIGNATURES)))

    # [R-ENF-04] — an empty run is not a clean run.
    if n_type == 0 or n_block == 0:
        print('\nFAIL — a test examined nothing. An empty result is not a clean result.')
        return 1

    if type_bad:
        print('\nTEST 1 FAILED — the extension lies about the content:')
        for rel, why in type_bad:
            print('  %-70s %s' % (rel, why))
    if block_bad:
        print('\nTEST 2 FAILED — a block page is stored as a source:')
        for rel, why in block_bad:
            print('  %-70s %s' % (rel, why))

    if type_bad or block_bad:
        print('\nA source that was never obtained must not sit in a study under a source\'s'
              ' name.\nDelete it and record the failed access in the sweep register, or'
              ' name it above\nwith the reason it is allowed. Do not widen the'
              ' signatures [R-COC-01].')
        return 1

    print('\nPASS — every tracked file is the type it claims and no stored source is a'
          ' block page.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
