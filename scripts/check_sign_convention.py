#!/usr/bin/env python3
"""[R-ENF-01] ONE SIGN CONVENTION PER TABLE, SO A DEDUCTION CAN ONLY BE READ ONE WAY.

A table printing "(2,650)", "(360)", "(792)" and then "440" under four rows that all begin
"Less" has told a reader two different things with the same word. THIS IS NOT A STYLE
QUESTION. In every one of the nine tables that do it, the row breaking the convention is a
working-capital line THE MODEL ADDS while its label says "Less":

    Less cash operating expenses      (2,650)
    Less impairment and credit losses   (360)
    Less depreciation and amortisation  (792)
    Less capital expenditure          (1,012)
    Less increase in working capital      440      <- added, not deducted
    Free cash flow to the firm          4,368

A reader following the labels reaches 3,488 against a printed 4,368 — 880 out, twenty per
cent of that year's cash flow — and nothing on the page says so. In three of the nine THE
SAME ROW SWITCHES CONVENTION BETWEEN ADJACENT YEARS, printing 855 in one and -4,550 in the
next under one label, which no reader can possibly get right.

THE SEMANTIC DEFECT BENEATH IT IS THE REAL ONE, and the arithmetic is what makes it
visible: a row labelled "Less INCREASE in working capital" over a figure that is a RELEASE
states the opposite of what happened. The honest fix is a signed label ("Change in working
capital, a release shown positive") or one convention through the table — NEVER a footnote,
because a reader adding a column does not stop to read one.

WHY THIS ONE READS THE PAGE WHILE THE WATERFALL CHECK READS THE BUILDER. The waterfall
check could not be a page-side gate because a statement mixes labelled and unlabelled steps
and the page cannot say which is which (engine/table_residual.py carries that measurement:
42.4% and then 30.7%). NO SUCH AMBIGUITY EXISTS HERE. Whether a figure is printed in
parentheses, as a signed negative, or as a bare magnitude is a property OF THE PAGE and of
nothing else, and the check needs no anchor, no model and no pool of committed numbers.
Measured book-wide it flags 9 of the 100 tables that carry a deduction row, and every one
of the nine is the same real defect.

Ratcheted [R-ENF-02] at the studies already doing it, which may only ever SHORTEN.
Population-anchored [R-ENF-04] both ways: a run examining zero documents FAILS, and so does
one finding zero tables with a deduction row across present documents.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import table_residual as TR                                            # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'signconv_outstanding.json')
DATE = re.compile(r'(\d{2})-(\d{2})-(\d{4})')


def latest(paths):
    """The LATEST edition of each document by DATE, never by string sort [L-067]."""
    keep = {}
    for p in paths:
        b = os.path.basename(p)
        if b.startswith('~$'):
            continue
        m = DATE.search(b)
        key, stamp = DATE.sub('', b), (m.group(3) + m.group(2) + m.group(1)) if m else ''
        if key not in keep or stamp > keep[key][0]:
            keep[key] = (stamp, p)
    return sorted(v[1] for v in keep.values())


def survey():
    """(findings, documents read, tables carrying a deduction row)."""
    from docx import Document
    out, docs, tables = [], 0, 0
    for d in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study'))):
        tk = os.path.basename(d).replace('_study', '').upper()
        for p in latest(glob.glob(os.path.join(d, '*.docx'))):
            docs += 1
            try:
                doc = Document(p)
            except Exception as exc:                     # a document that will not open
                out.append((tk, os.path.basename(p), -1, 'UNREADABLE', str(exc)[:70]))
                continue
            for n, t in enumerate(doc.tables):
                rows = TR.grid(t)
                if not any(TR.op_of((r[0] if r else '') or '') == '-' for r in rows[1:]):
                    continue
                tables += 1
                cols = TR.sign_conventions(rows)
                across = TR.sign_conventions_across(rows)
                for j, seen in sorted(cols.items()):
                    out.append((tk, os.path.basename(p), n, 'column %d' % j,
                                ' vs '.join('%s %s' % (k, [v[1] for v in vs][:3])
                                            for k, vs in sorted(seen.items()))))
                for i, (label, kinds) in sorted(across.items()):
                    out.append((tk, os.path.basename(p), n, 'row %d' % i,
                                '%r switches between years: %s'
                                % (label[:44], ' vs '.join(
                                    '%s %s' % (k, [v[1] for v in vs][:2])
                                    for k, vs in sorted(kinds.items())))))
    return out, docs, tables


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the ratchet; it may only ever SHORTEN')
    a = ap.parse_args()

    found, docs, tables = survey()
    allowed = (set(json.load(open(RATCHET))['outstanding'])
               if os.path.exists(RATCHET) else set())

    if docs == 0:
        print('FAIL — examined zero documents; an absent answer is not a clean one')
        return 1
    if tables == 0:
        print('FAIL — read %d document(s) and found zero tables carrying a deduction row. '
              'Either the book has stopped deducting anything or the reader is broken; '
              'both are findings and neither is clean.' % docs)
        return 1
    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    missing = sorted(allowed - on_disk)
    if missing:
        print('FAIL — the ratchet names studies that do not exist on disk: %s'
              % ', '.join(missing))
        return 1

    print('%d document(s) read, %d table(s) carrying a deduction row, %d finding(s)'
          % (docs, tables, len(found)))
    for tk, doc, n, where, note in found:
        print('%s%-12s %-38s t%-3s %-10s %s'
              % ('   ' if tk in allowed else '>> ', tk, doc[:38],
                 n if n >= 0 else '?', where, note[:78]))

    new = sorted({f[0] for f in found} - allowed)

    if a.prune:
        keep = sorted({f[0] for f in found})
        if allowed and set(keep) - allowed:
            print('REFUSED — --prune may only ever SHORTEN the ratchet; %s would be added'
                  % ', '.join(sorted(set(keep) - allowed)))
            return 1
        json.dump({'rule': 'R-ENF-01 / one sign convention per table',
                   'note': 'Studies whose delivered tables print deductions in more than '
                           'one sign convention. May only ever SHORTEN. Each closes at '
                           'its study\'s next re-issue.',
                   'outstanding': keep}, open(RATCHET, 'w'), indent=1)
        print('ratchet rewritten with %d entr%s'
              % (len(keep), 'y' if len(keep) == 1 else 'ies'))
        return 0

    if new:
        print('\nFAIL — %d study/studies print deductions in more than one sign convention '
              'in the same table: %s' % (len(new), ', '.join(new)))
        print('A reader cannot tell whether to take the magnitude off or add the sign, and '
              'in every case measured the row that broke the convention was one the model '
              'ADDED under a label saying "Less".')
        return 1
    print('\nOK — no new violations. %d stud%s on the ratchet, which may only SHORTEN.'
          % (len(allowed), 'y' if len(allowed) == 1 else 'ies'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
