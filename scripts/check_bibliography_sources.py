#!/usr/bin/env python3
"""[R-ENF-01] SIGCM CLAUSE 1 IS CHECKED ON THE PAGE A READER RECEIVES, NOT ONLY IN
THE REGISTER THE STUDY COMMITS.

check_source_integrity.py reads each study's committed INPUT REGISTER, where the
sources name filings, and it passes the book. The claim a reader actually receives is
in the DELIVERED BIBLIOGRAPHY'S own sources table, and that population was reached by
nothing. Measured 18-09-2026 across 46 delivered documents and 12,654 table rows:

    AMOC  "Company financial summary pages | stockanalysis.com; Investing.com;
           TradingView | Aug 2026 | Shares outstanding, market capitalisation, TOTAL
           ASSETS, TOTAL LIABILITIES, CASH AND EQUIVALENTS, TOTAL DEBT ..."

    ELEC  twelve rows, among them the company's own FY2024 and FY2025 revenue, net
          profit, EPS and total assets sourced to Mubasher, Arab Finance, Zawya,
          Decypha and a Reuters flash, and its FY2024 EBIT, total liabilities and
          interest coverage to a Simply Wall St health page.

Both studies passed the register-side gate on the same day. This is [R-ENF-01]'s own
species one level along: the rule was enforced on the artefact somebody had built a
reader for, and the delivered document is the artefact that reaches a reader.

IT RUNS THE SHARED INSTRUMENT [R-ENF-03]: engine/source_integrity.py owns the vendor
list, the relay phrases and what clears a row, and this gate supplies the population.
Nothing here re-implements that arithmetic.

THE FALSE-POSITIVE RATE WAS MEASURED AND THE INSTRUMENT RE-POINTED TWICE, never
widened [R-COC-01]. A first draft flagged 34 rows and the largest class was PEER
MULTIPLES -- nine in one study, five in another, every one the construction SIGCM
clause 5 requires, since clause 1 governs THE SUBJECT'S OWN historicals. A second
matched a FORWARD REVENUE TARGET inside a budget announcement. With peers, non-Company
sweep rings and forward claims out of scope the rate is 15 rows in 12,654 -- 0.119% --
and what remains is, with one exception carried on the ratchet, real.

Ratcheted [R-ENF-02], population-anchored [R-ENF-04] BOTH ways: zero study directories
fails, and zero DOCUMENT ROWS read across present directories fails too, because a
reader that stopped finding tables reads exactly like a clean book.
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import source_integrity as SI                                        # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit',
                       'bibliography_sources_outstanding.json')
DATED = re.compile(r'(\d{2})-(\d{2})-(\d{4})')


def rows_of(docx):
    """Every table row of a .docx as a list of its cells, in printed order."""
    with zipfile.ZipFile(docx) as z:
        x = z.read('word/document.xml').decode('utf-8', 'ignore')
    out = []
    for r in re.findall(r'<w:tr[ >].*?</w:tr>', x, re.S):
        cells = []
        for c in re.findall(r'<w:tc[ >].*?</w:tc>', r, re.S):
            t = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', c, re.S))
            cells.append(html.unescape(re.sub(r'<[^>]+>', '', t)).strip())
        out.append(cells)
    return out


def latest_editions(d):
    """One file per document FAMILY — the latest edition only.

    A superseded edition is history and is not delivered; holding a study to a file it
    replaced is the defect check_workbook_structure already names.
    """
    best = {}
    for f in glob.glob(os.path.join(d, '*.docx')):
        b = os.path.basename(f)
        if b.startswith('~$'):
            continue
        m = DATED.search(b)
        key = DATED.sub('', b)
        stamp = ('%s-%s-%s' % (m.group(3), m.group(2), m.group(1))) if m else '0000'
        if key not in best or stamp > best[key][0]:
            best[key] = (stamp, f)
    return [f for _s, f in best.values()]


def survey():
    """(hits, documents read, rows read)."""
    hits, docs, rows = {}, 0, 0
    for d in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study'))):
        tk = os.path.basename(d).replace('_study', '').upper()
        for f in latest_editions(d):
            try:
                rs = rows_of(f)
            except (zipfile.BadZipFile, KeyError, OSError):
                continue                      # not a readable Word document
            docs += 1
            rows += len(rs)
            for row, why in SI.audit_document(rs):
                hits.setdefault(tk, []).append((os.path.basename(f), row, why))
    return hits, docs, rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the ratchet; it may only ever SHORTEN')
    a = ap.parse_args()

    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    if not on_disk:
        print('FAIL — zero study directories. An absent answer is not a clean one.')
        return 1

    hits, docs, rows = survey()
    if rows == 0:
        print('FAIL — read zero document rows across %d stud(ies). A reader that '
              'stopped finding tables reads exactly like a clean book [R-ENF-04].'
              % len(on_disk))
        return 1

    r = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allow = set(r.get('breaching', []))
    ghosts = sorted(allow - on_disk)
    if ghosts:
        print('FAIL — the ratchet names studies that do not exist on disk: %s'
              % ', '.join(ghosts))
        return 1

    print('%d delivered document(s) read, %d table row(s); %d stud%s with a row '
          'sourcing its own reported history outside the filings'
          % (docs, rows, len(hits), 'y' if len(hits) == 1 else 'ies'))
    for tk in sorted(hits):
        print('%s%-12s %d row(s)' % ('   ' if tk in allow else '>> ', tk, len(hits[tk])))
        for f, row, why in hits[tk][:3]:
            print('       %-28s %s' % (why[:28], row[:96]))

    new = sorted(set(hits) - allow)
    if a.prune:
        if set(hits) - allow:
            print('\nREFUSED to prune — %s would GROW the list. A ratchet may only '
                  'ever SHORTEN.' % ', '.join(new))
            return 1
        json.dump({**r, 'breaching': sorted(set(hits))}, open(RATCHET, 'w'),
                  indent=1, ensure_ascii=False)
        open(RATCHET, 'a').write('\n')
        print('\npruned — %d remain' % len(hits))
        return 0

    if new:
        print('\nFAIL — %d stud%s newly sourcing its own reported history to a vendor '
              'or an outlet in a DELIVERED document: %s'
              % (len(new), 'y' if len(new) == 1 else 'ies', ', '.join(new)))
        return 1
    print('\nOK — %d on the ratchet, which may only SHORTEN.' % len(allow))
    return 0


if __name__ == '__main__':
    sys.exit(main())
