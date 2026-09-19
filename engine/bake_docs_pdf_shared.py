"""Render this study's delivered DOCUMENTS to PDF, from edition.py and nothing typed.

WHY THIS EXISTS. engine/bake_model_pdf_shared.py already renders the WORKBOOK, and nothing
rendered the study or the bibliography: those PDFs were made by hand with soffice whenever
somebody remembered. So a rebuild refreshed the .docx and left the .pdf beside it — and the
PDF is the file a reader actually opens.

scripts/check_artefact_freshness.py found it the moment it was pointed at the book, on the
very studies that had just been rebuilt whole: ADIB's study and bibliography PDFs committed
3,634 minutes before the documents they are rendered from. A build that leaves the reader's
own file stale has not rebuilt the study.

It renders whatever the edition module names and skips nothing silently: an edition that
declares a PDF whose source document is missing is a FAILURE, not a skip [R-ENF-04].
"""
import os
import subprocess
import sys


def bake(here, edn):
    pairs = []
    for doc_attr, pdf_attr in (('STUDY_DOCX', 'STUDY_PDF'),
                               ('BIBLIO_DOCX', 'BIBLIO_PDF'),
                               ('SOURCES_DOCX', 'SOURCES_PDF')):
        doc, pdf = getattr(edn, doc_attr, None), getattr(edn, pdf_attr, None)
        if doc and pdf:
            pairs.append((doc, pdf))
    if not pairs:
        print('edition.py names no document/PDF pair — nothing this script can render, '
              'which is a fact about the edition module rather than a clean result')
        return 1

    fails = []
    for doc, pdf in pairs:
        src = os.path.join(here, doc)
        if not os.path.exists(src):
            print('%-46s MISSING — the edition names it and it is not on disk' % doc)
            fails.append(doc)
            continue
        r = subprocess.run(['soffice', '--headless', '--convert-to', 'pdf',
                            '--outdir', here, src],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
        out = os.path.join(here, pdf)
        if r.returncode != 0 or not os.path.exists(out):
            print('%-46s RENDER FAILED' % doc)
            print(r.stdout.decode('utf-8', 'replace')[-400:])
            fails.append(doc)
            continue
        print('%-46s -> %s (%d KB)' % (doc, pdf, os.path.getsize(out) // 1024))
    if fails:
        print('FAILED to render: %s' % ', '.join(fails))
        return 1
    print('%d delivered document(s) rendered from edition.py' % len(pairs))
    return 0
