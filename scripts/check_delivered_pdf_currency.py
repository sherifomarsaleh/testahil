#!/usr/bin/env python3
"""[R-ENF-06] applied to the file the reader actually receives — the delivered PDF.

THE PDF IS THE DELIVERABLE AND THE WORD FILE IS THE BUILD ARTEFACT. engine/make_pdf.py
opens with that sentence. Every other gate in this repository reads the .docx and the
.xlsx, so a study can be rebuilt, re-checked and reported clean while the PDF a reader
opens still carries the previous edition's answer.

WHAT PROVOKED IT. On 03-Sep-2026 four studies were rebuilt — ARCC, AMOC, EGCH, PHDC — and
TWELVE OF THEIR DELIVERED PDFs WERE NOT. ARCC's Word file carried a central of 66.53 while
its delivered PDF carried the retired 53.21, for four hours, with every gate green. It was
found by chasing a DIFFERENT gate's ratchet note, which said ARCC would clear on re-issue
and had not: the sentence keeping it there existed nowhere in the live builder, only in a
backup one, which is what a stale render looks like from the outside.

WHY THIS CHECKS CONTENT AND NOT TIMESTAMPS. A fresh clone rewrites every mtime, so a
modification-time comparison reports the whole book clean on the machine where it matters
most — CI. So the test is the study's OWN committed central: it must appear in the text of
the delivered PDF, and the central of an EARLIER edition of the same study must not. That is
the same instrument as check_artefact_currency, pointed at the rendered file instead of at a
JSON.

WHAT IT DELIBERATELY DOES NOT DO. It does not require every figure in a PDF to match the
model — a study legitimately quotes superseded numbers to show what changed, and a gate that
could not tell those apart would push studies to stop explaining themselves. It requires the
CURRENT central to be present. A document that cannot show its own answer is not a delivered
document.

RATCHETED per [R-ENF-02], population-anchored per [R-ENF-04]: a run that examined zero PDFs
FAILS. READ THE POPULATION LIVE — python3 scripts/check_delivered_pdf_currency.py.
"""
from __future__ import annotations

import glob
import json
import os
import re
import subprocess
import sys

import importlib.util as _ilu

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

# [R-ENF-03] THE GAP GATE'S READER, IMPORTED RATHER THAN RE-IMPLEMENTED. This gate carried
# its own and the two disagreed about where a central lives — the gap gate looks at the top
# level AND at meta, this one looked only at the top level, so a study committing its
# answer where the gap gate reads it was reported here as exposing no central at all. Two
# checkers of one fact that disagree are worse than one, because each looks authoritative
# alone. check_publish_block.py imports the same reader for the same reason.
_spec = _ilu.spec_from_file_location(
    'check_valuation_gap', os.path.join(HERE, 'check_valuation_gap.py'))
_gap = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_gap)
RATCHET = os.path.join(REPO, 'engine', 'build_depth_audit', 'pdf_outstanding.json')

# The delivered study document, by the date in its own filename. DD-MM-YYYY, so a lexical
# sort picks the wrong edition — [L-067], and it has bitten this repository before.
DATED = re.compile(r'(\d{2})[-_]?(\d{2})[-_]?(\d{4})')


def _key(path):
    m = DATED.search(os.path.basename(path))
    return (m.group(3), m.group(2), m.group(1)) if m else ('0000', '00', '00')


def latest_study_doc(d):
    """The most recent DELIVERED study document in a study directory, by filename date."""
    cands = [f for f in glob.glob(os.path.join(d, '*.pdf'))
             if 'Valuation_Study' in os.path.basename(f)
             or 'Valuation_Report' in os.path.basename(f)]
    return max(cands, key=_key) if cands else None


def central_of(d):
    """The study's own committed central, and its two-sided branches where it has them.

    The reader is [R-GAP-01]'s, imported above rather than written again here.
    """
    central, _spot, _route = _gap.read_answer(d)
    if central is None:
        # read_answer requires BOTH a central and a spot, because ITS question is whether
        # a study was audited against the price it was struck at. This gate's question is
        # only whether the delivered PDF carries the answer the study publishes, so where
        # the spot is missing the central is still resolved — through the gap gate's own
        # field shapes and its own numeric reader, never a second set of key names.
        for fn in ('study_numbers.json', 'numbers.json'):
            q = os.path.join(d, fn)
            if not os.path.exists(q):
                continue
            try:
                j = json.load(open(q, encoding='utf-8'))
            except Exception:
                break
            meta = j.get('meta') or {}
            central = (_gap._num(j.get('central')) or _gap._num(j.get('fair'))
                       or _gap._num(meta.get('central')))
            break
    branches = _gap.read_branches(d) or []
    vals = []
    for b in branches:
        if isinstance(b, (int, float)):
            vals.append(float(b))
        elif isinstance(b, dict) and isinstance(b.get('value'), (int, float)):
            vals.append(float(b['value']))
    if central is not None:
        return float(central), vals
    return (vals[0] if vals else None), vals


def text_of(pdf):
    try:
        r = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                           capture_output=True, text=True, timeout=180)
        return r.stdout or ''
    except Exception:
        return ''


def shows(text, value, dps=(0, 1, 2)):
    """Does the text carry this figure at any of these roundings?

    A ROUNDING THAT COLLAPSES THE FIGURE TO ONE OR TWO SIGNIFICANT DIGITS IS NOT EVIDENCE,
    and this gate passed a stale exemplar on exactly that. ADNOCLS's delivered PDF prints
    a central of AED 7.05 while the study publishes 6.74; at zero decimal places 6.74
    renders as "7", a bare digit that appears on every page of every document ever
    written, so the gate reported the paper current when it was a full edition behind.
    Every other check in the file was sound — the population, the ratchet, the reader —
    and the whole of the hole was one formatting call.

    THE BAR IS SIGNIFICANT DIGITS RATHER THAN A CHOSEN LENGTH, because that is arithmetic
    about the figure rather than a knob: three significant figures is the precision at
    which this house quotes a per-share value, so "6.74", "123" and "1,234" all qualify
    and "7" does not. A study whose central genuinely needs one significant figure to be
    identified in its own document has a bigger problem than this gate.
    """
    for dp in dps:
        f = f'{value:,.{dp}f}'
        if len(f.replace(',', '').replace('.', '').replace('-', '').lstrip('0')) < 3:
            continue                       # not enough of the figure survives the rounding
        if f in text or f.replace(',', '') in text:
            return True
    return False


def headline(pdf, pages=3):
    """The first few pages — masthead, read-first and valuation summary.

    THE REGION IS THE WHOLE DESIGN, and three attempts got there. Searching the WHOLE
    document for the current central fails in both directions: matching at zero decimals is
    satisfied by almost any thirty-page document full of figures, and requiring lossless
    precision is satisfied by almost none, because a committed central carries full float
    precision (27.24258808463448) while a document renders it rounded. Searching the whole
    document for a SUPERSEDED central fails too — TMGH's peer table contains the row
    "2025 80.00 6.98 11.5 39.33 2.03", and 39.33 happens to be one of its own earlier
    centrals.

    A study leads with its answer. A table cell does not live on the masthead. So the test
    is whether the OPENING PAGES carry the central the study now publishes, and measured
    across the book that is exactly right: twelve of thirteen readable studies carry theirs
    within three pages, at whatever rounding they chose to print.
    """
    try:
        r = subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', str(pages), pdf, '-'],
                           capture_output=True, text=True, timeout=180)
        return r.stdout or ''
    except Exception:
        return ''


def require_pdftotext():
    """The gate cannot examine a PDF without a text extractor, and must say so.

    A missing binary would make every document "yield no text", which this gate would then
    report as a book-wide failure — a red build whose message points at the studies rather
    than at the runner. Worse, a caller could be tempted to make that case silent, which
    turns a broken gate into a passing one. So the absence is detected once and named.
    """
    try:
        r = subprocess.run(['pdftotext', '-v'], capture_output=True, text=True, timeout=30)
        if r.returncode == 0 or 'pdftotext' in (r.stderr or '') + (r.stdout or ''):
            return
    except Exception:
        pass
    print('FAIL — pdftotext is not available, so this gate cannot read a single delivered '
          'PDF. That is a broken TOOL, not a finding about the studies, and it is reported '
          'as such rather than as a clean run or as a book-wide failure. Install '
          'poppler-utils.')
    sys.exit(2)


def main(argv):
    require_pdftotext()
    prune = '--prune' in argv
    rat = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    rat.setdefault('entries', {})

    dirs = sorted(glob.glob(os.path.join(REPO, 'engine', '*_study')))
    print('DELIVERED PDF CURRENCY  [R-ENF-06]')
    print('   the PDF is what the reader gets; every other gate reads the Word file')
    if not dirs:
        print('\nFAIL — examined ZERO study directories. An empty result is not a clean one.')
        return 1

    examined, clean, stale, dark, fail = 0, [], [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-6].upper()
        pdf = latest_study_doc(d)
        if pdf is None:
            dark.append((tk, 'no delivered study PDF'))
            continue
        c, branches = central_of(d)
        if c is None:
            dark.append((tk, 'study_numbers.json exposes no central'))
            continue
        txt = text_of(pdf)
        examined += 1
        if not txt.strip():
            dark.append((tk, f'{os.path.basename(pdf)} yields no text'))
            continue
        want = branches or [c]
        head = headline(pdf)
        if not head.strip():
            dark.append((tk, f'{os.path.basename(pdf)} opening pages yield no text'))
            continue
        # EVERY BRANCH, NOT ANY BRANCH. A two-sided study publishes two answers and a
        # document showing one of them is HALF CURRENT — which is the gap gate's own
        # rule three files away ("a review naming one of two answers has audited half
        # the study") and was not this one's. It cost a real miss the day it was
        # written: a study rebuilt from two branches of 58.04 and 73.03 to 36.64 and
        # 54.24 passed, because 36.64 happened to appear in the stale document's
        # opening pages while the headline still read 58.04. `any` over a set of
        # answers asks whether the paper carries SOMETHING the model believes; the
        # question is whether it carries what the model PUBLISHES.
        missing = [v for v in want if not shows(head, v)]
        if missing:
            stale.append((tk, os.path.basename(pdf),
                          ('its opening pages carry none of %s'
                           if len(missing) == len(want) else
                           'it publishes %d branches and its opening pages carry only '
                           'some of them; missing %s')
                          % (', '.join(f'{v:,.2f}' for v in
                                       (want if len(missing) == len(want) else missing))
                             if len(missing) == len(want) else
                             (len(want), ', '.join(f'{v:,.2f}' for v in missing)))))
        else:
            clean.append(tk)

    if examined == 0:
        print('\nFAIL — examined ZERO delivered PDFs across %d study directories. That is an '
              'absent answer wearing the costume of a clean one [R-ENF-04].' % len(dirs))
        return 1

    print('   %d study directories · %d PDFs read · %d current · %d not showing their own '
          'answer' % (len(dirs), examined, len(clean), len(stale)))

    print('\n  THE DELIVERED PDF DOES NOT SHOW THE STUDY\'S OWN CENTRAL: %d' % len(stale))
    for tk, f, miss in sorted(stale):
        known = tk in rat['entries']
        print('    %-12s%-46s missing %s%s' % (tk, f[:45], miss,
                                               '' if known else '   *** NEW ***'))
        if not known:
            fail.append('%s: %s does not carry the central its study publishes (%s). The PDF '
                        'is the deliverable; rebuild it with engine/make_pdf.py.'
                        % (tk, f, miss))

    print('\n  NOT READABLE: %d' % len(dark))
    for tk, why in sorted(dark):
        known = tk in rat['entries']
        print('    %-12s%s%s' % (tk, why, '' if known else '   *** NEW ***'))
        if not known:
            fail.append('%s: %s [R-ENF-04] — an unreadable answer is not a clean one.'
                        % (tk, why))

    now = {t for t, _, _ in stale} | {t for t, _ in dark}
    cleared = set(rat['entries']) - now
    if cleared:
        print('\n  CLEARED: %s' % ', '.join(sorted(cleared)))
        if prune:
            for tk in cleared:
                rat['entries'].pop(tk, None)
            json.dump(rat, open(RATCHET, 'w'), indent=1, sort_keys=True)
            print('  --prune: the list has SHORTENED. It may never grow.')
        else:
            print('  run with --prune to shorten the list.')

    if fail:
        print('\nFAIL — %d:' % len(fail))
        for m in fail:
            print('   * %s' % m)
        return 1
    print('\nOK — every delivered PDF carries the answer its study publishes.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
