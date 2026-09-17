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
        out = os.path.join(here, pdf)
        # THE SUCCESS TEST WAS SATISFIABLE WITHOUT THE WORK BEING DONE [fixed 17-09-2026].
        #
        # soffice EXITS 0 AND LEAVES THE OLD FILE IN PLACE when it has no filter for the
        # input — a machine with libreoffice-core but not libreoffice-writer converts
        # nothing, says nothing, and returns success. The old test was `returncode != 0 or
        # not os.path.exists(out)`, and the stale PDF from the previous edition satisfies
        # os.path.exists, so this script printed "2 delivered document(s) rendered" over
        # two files it had not touched. That is precisely the defect the docstring above
        # says this file exists to stop, reappearing one level up: the reader's own file
        # stayed at the pre-fix render while the build reported clean. It was found on
        # PHDC on 17-09-2026 by reading the PDF's mtime, not by any gate.
        #
        # THE TEST IS NOW THAT THE OUTPUT IS NEWER THAN ITS SOURCE. A render that did not
        # happen cannot pass it, whatever soffice's exit code says, and the failure names
        # the missing filter as the likely cause so the next person does not have to
        # rediscover it.
        before = os.path.getmtime(out) if os.path.exists(out) else -1.0
        r = subprocess.run(['soffice', '--headless', '--convert-to', 'pdf',
                            '--outdir', here, src],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
        if r.returncode != 0 or not os.path.exists(out):
            print('%-46s RENDER FAILED' % doc)
            print(r.stdout.decode('utf-8', 'replace')[-400:])
            fails.append(doc)
            continue
        after = os.path.getmtime(out)
        if after <= before or after < os.path.getmtime(src):
            print('%-46s NOT WRITTEN — soffice exited 0 and left the existing PDF in '
                  'place. It is older than the document it is rendered from, so this '
                  'build did NOT refresh the file a reader opens. The usual cause is a '
                  'missing document filter (libreoffice-writer for .docx, '
                  'libreoffice-calc for .xlsx) on a machine that has libreoffice-core.'
                  % doc)
            print(r.stdout.decode('utf-8', 'replace')[-400:])
            fails.append(doc)
            continue
        print('%-46s -> %s (%d KB)' % (doc, pdf, os.path.getsize(out) // 1024))
    if fails:
        print('FAILED to render: %s' % ', '.join(fails))
        return 1
    print('%d delivered document(s) rendered from edition.py' % len(pairs))
    return 0
