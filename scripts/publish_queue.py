#!/usr/bin/env python3
"""Part E criterion 6's reading queue — what is present, so the reading is all that is left.

Criterion 6 asks that the publish queue hold FOUR FILES PER NAME on the new standard --
the valuation study in Word AND in PDF, the standalone bibliography, and the 16-sheet
workbook -- EACH OPENED AND READ. The reading is a human act and no script may attest
it, which the plan says in terms and which this script does not try to get around.

WHAT IT DOES IS EVERYTHING ELSE. It resolves each name's LATEST edition of each of the
four, reports what is missing by name, and prints the queue in reading order with paths
-- so the only thing standing between the book and that criterion is somebody's
afternoon, rather than somebody's afternoon plus an hour of finding the files.

THE ARTEFACT HAS SEVERAL NAMES AND THEY ARE READ OFF THE BOOK, NOT GUESSED [L-355].
Twenty-one studies name the bibliography the obvious way, one uses a source-register
name, one a sources name, and one file carries THE COMPANY'S OTHER NAME rather than
its ticker. A matcher built from the obvious convention condemns four compliant
studies, which is the measurement that adopted check_bibliography_sources.

IT IS A REPORT AND NOT A GATE. A study with no documents is not a failing study --
metals deliver none -- and the criterion is the principal's to close.
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATED = re.compile(r'(\d{2})-(\d{2})-(\d{4})')
UNDATED = re.compile(r'(\d{2})(\d{2})(\d{4})')

BIB = re.compile(r'(bibliograph|source[_ ]?register|_sources?_)', re.I)
STUDY = re.compile(r'valuation[_ ]?study', re.I)
BOOK = re.compile(r'(valuation[_ ]?model|workbook)', re.I)


def _stamp(name):
    m = DATED.search(name) or UNDATED.search(name)
    if not m:
        return '0000-00-00'
    return '%s-%s-%s' % (m.group(3), m.group(2), m.group(1))


def latest(d, pat, ext):
    best = None
    for f in glob.glob(os.path.join(d, '*' + ext)):
        b = os.path.basename(f)
        if b.startswith('~$') or not pat.search(b):
            continue
        s = _stamp(b)
        if best is None or s > best[0]:
            best = (s, f)
    return best


def survey():
    rows = []
    for d in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study'))):
        tk = os.path.basename(d).replace('_study', '').upper()
        four = {
            'study (docx)': latest(d, STUDY, '.docx'),
            'study (pdf)': latest(d, STUDY, '.pdf'),
            'bibliography': latest(d, BIB, '.docx'),
            'workbook': latest(d, BOOK, '.xlsx'),
        }
        if not any(four.values()):
            continue                      # delivers no documents; not in this queue
        rows.append((tk, four))
    return rows


def main() -> int:
    only = [a.upper() for a in sys.argv[1:] if not a.startswith('-')]
    rows = survey()
    if only:
        rows = [r for r in rows if r[0] in only]
    if not rows:
        print('no study delivers a document — nothing to queue [R-ENF-04]')
        return 1

    complete = [r for r in rows if all(r[1].values())]
    short = [r for r in rows if not all(r[1].values())]

    print('Part E criterion 6 — the reading queue')
    print('%d name(s) deliver documents; %d hold all four; %d are short\n'
          % (len(rows), len(complete), len(short)))

    for tk, four in short:
        miss = [k for k, v in four.items() if not v]
        print('  SHORT  %-13s missing %s' % (tk, ', '.join(miss)))
    if short:
        print()

    print('READING ORDER — latest edition of each, paths relative to the repository:')
    for tk, four in complete:
        newest = max(v[0] for v in four.values())
        print('\n  %-13s (latest edition %s)' % (tk, newest))
        for k in ('study (docx)', 'study (pdf)', 'bibliography', 'workbook'):
            s, f = four[k]
            print('     %-14s %s' % (k, os.path.relpath(f, ROOT)))

    print('\n%d name(s) are ready to read, %d x 4 = %d files. THE READING IS THE '
          'CRITERION and no script attests it.' % (len(complete), len(complete),
                                                   4 * len(complete)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
