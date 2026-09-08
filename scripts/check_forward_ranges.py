#!/usr/bin/env python3
"""[R-ENF-01] A RUN'S FAR-YEAR RANGES ARE CHECKED ON THE PAGE A READER RECEIVES,
NOT IN THE RECORD THAT PRODUCED THEM.

[R-FCAL-01] says every fundamental walk-forward produces two documents, and of the
first — the updated fundamental analysis — that it carries the corrections that passed
and publishes YEARS 3-5 AS RANGES from this record's own driver-error distribution,
NEVER AS POINTS. All five completed runs commit that band. NOTHING HAD EVER ASKED
WHETHER IT REACHES THE DOCUMENT, and the two questions are not the same one: the record
is internal by the same rule's own instruction, so a band can be computed, committed,
scored, and never printed, and every instrument in this repository would report the run
complete.

MEASURED: THREE OF THE FIVE PRINT IT AND TWO PRINT POINTS.
  PHDC   Table 4, "Revenue, years three to five (EGP mn) | Low | Point | High"
  EGCH   A.4, rows "Revenue - low of the range" / "- high of the range", with counts
  TMGH   Table 19, "84,517 - 193,380" per far year, with the tests behind each band
  ARCC   FY2028E/29E/30E as single figures, and NOT ONE SENTENCE about the test —
         while its own band reaches h=3,4,5 on n=5,4,3 and was committed on 01-09,
         two days BEFORE that document was rebuilt on 03-09
  AMOC   FY2028E/29E/30E as single figures. It states the principle in Section 7
         ("THE FAR FORECAST YEARS SUPPORT A RANGE AND NEVER A POINT") and prints no
         range; its record reaches only h=3, so years four and five have no band to
         publish and year three has one on two observations

THE THREE SHAPES ARE READ OFF THE BOOK RATHER THAN INVENTED, which is [L-355] applied
to the instrument rather than to the work: a matcher built from PHDC's convention finds
nothing in EGCH or TMGH and reports that as a result. The detector lives in
engine/range_disclosure.py — the module that already owns this subject, and which until
now nothing imported.

THE ARCHITECTURE WAS DECIDED BY MEASUREMENT AND THE MEASUREMENT CHANGED IT. A first
draft asked only that a range appear in a table naming a far year, and fired on SIX
studies that have no walk-forward at all — a period written with a dash ("2026-2027"),
a multiple range in a lens table, a charter-rate spread against a vessel class. Every
one was work that is right. Per [R-COC-01] it was RE-POINTED rather than widened: the
low/high evidence must sit in a row LABELLED with a far year or a column HEADED by one.
After re-pointing, 0 of 18 non-run studies trip any shape and all three true positives
survive.

WHAT IT DELIBERATELY DOES NOT CHECK, stated rather than discovered later: whether the
printed range REPRODUCES the run's committed band. A study applies a multiplier band to
its own point path, so the committed figures never appear on the page, and searching
every numeric pair for a matching ratio is the coincidence the waterfall instrument
already measured at 42.4% of all tables. Reconciling printed to committed needs the
study to DECLARE what it printed, on the prose_figures architecture, which is a re-issue
on four studies rather than something done in passing. This tells a published range from
NO RANGE AT ALL, which is the breach actually found. It therefore fails SAFE: a study
that prints a wrong range passes, and no study doing right work is condemned.

RATCHET [R-ENF-02]: AMOC and ARCC are listed with their reasons; rebuilding a delivered
study is a re-issue and is not done in passing. The build breaks on a NEW run whose
study publishes points, and the list may only ever SHORTEN.

POPULATION-ANCHORED [R-ENF-04] BOTH WAYS, off the run directories on disk as
check_lessons_register anchors: zero runs committing a band FAILS, and so does zero
delivered documents READ across present runs, because a reader that stopped reading is
indistinguishable from a book that prints every range.

ARTEFACT-conditional in the new-study gauntlet [R-ENF-07]: an empty study directory has
no walk-forward run behind it and no delivered document, so demanding that it go red
would be a false claim about what this gate checks.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'forward_ranges_outstanding.json')

from engine import range_disclosure as RD          # noqa: E402

STUDY_DOC = re.compile(r'valuation[_ ]study.*\.docx$', re.I)
DATE = re.compile(r'(\d{2})-(\d{2})-(\d{4})')
BAND = 'forward_ranges.json'


def load_ratchet():
    if not os.path.exists(OUTSTANDING):
        return {}
    return json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', {})


def latest_study(directory):
    """The delivered study at its LATEST edition, by the date PARSED out of the
    filename. Sorting these strings lexicographically reads 08-08 as later than
    03-09 and audits a superseded edition [L-355]."""
    try:
        names = os.listdir(directory)
    except OSError:
        return None
    docs = [n for n in names if STUDY_DOC.search(n) and not n.startswith('~')]
    if not docs:
        return None

    def key(n):
        m = DATE.search(n)
        return (m.group(3), m.group(2), m.group(1)) if m else ('0000', '00', '00')

    return sorted(docs, key=key)[-1]


def tables_of(path):
    import docx
    doc = docx.Document(path)
    out = []
    for tb in doc.tables:
        out.append([[c.text.strip().replace('\n', ' ') for c in r.cells] for r in tb.rows])
    return out


def census():
    rows = []
    for run in sorted(glob.glob(os.path.join(ENGINE, '*_walkforward'))):
        if not os.path.exists(os.path.join(run, BAND)):
            continue
        tk = os.path.basename(run)[:-len('_walkforward')].upper()
        study_dir = os.path.join(ENGINE, '%s_study' % tk.lower())
        if not os.path.isdir(study_dir):
            rows.append(dict(ticker=tk, state='no_study'))
            continue
        doc = latest_study(study_dir)
        if not doc:
            rows.append(dict(ticker=tk, state='no_document'))
            continue
        m = DATE.search(doc)
        year = int(m.group(3)) if m else 0
        try:
            tbs = tables_of(os.path.join(study_dir, doc))
        except Exception as exc:                                  # noqa: BLE001
            rows.append(dict(ticker=tk, state='unreadable', doc=doc, why=str(exc)[:70]))
            continue
        rows.append(dict(ticker=tk, state='read', doc=doc, year=year,
                         tables=len(tbs),
                         shapes=RD.far_year_range_shapes(tbs, year)))
    return rows


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    rows = census()
    read = [r for r in rows if r['state'] == 'read']

    print('FAR-YEAR RANGE GATE  [R-ENF-01]  [R-FCAL-01] years 3-5 as ranges, never points')
    print('   a run that computes a band must PRINT it in the study a reader receives')
    print('   %d runs committing a band · %d delivered documents read · %d printing a range'
          % (len(rows), len(read), sum(1 for r in read if r['shapes'])))

    if not rows:
        print('\nFAIL — the gate examined ZERO walk-forward runs committing a band. An '
              'empty result is not a clean result [R-ENF-04].')
        return 1
    if not read:
        print('\nFAIL — the gate READ ZERO delivered documents across %d runs. A reader '
              'that stopped reading is indistinguishable from a book that prints every '
              'range [R-ENF-04].' % len(rows))
        return 1

    fail = []
    on_disk = {r['ticker'] for r in rows}
    for tk in sorted(rat):
        if tk not in on_disk:
            fail.append('the ratchet lists %s and no walk-forward run of that name '
                        'commits a band — the list is anchored on nothing' % tk)

    print()
    breaching = []
    for r in sorted(rows, key=lambda r: r['ticker']):
        tk = r['ticker']
        if r['state'] == 'read' and r['shapes']:
            print('    %-8s prints a far-year range   shape %s   (%s)'
                  % (tk, '+'.join(r['shapes']), r['doc'][:44]))
            continue
        breaching.append(tk)
        mark = 'ratcheted' if tk in rat else 'NEW'
        if r['state'] == 'read':
            print('    %-8s POINTS ONLY — no far-year range in %d tables  [%s]'
                  % (tk, r['tables'], mark))
            why = ('publishes years three to five as points while its own run commits '
                   'a band')
        else:
            print('    %-8s %s  [%s]' % (tk, r['state'], mark))
            why = ('the delivered study could not be read (%s). An unreadable study is '
                   'not a clean study [R-ENF-04].' % r['state'])
        if tk not in rat:
            fail.append('%s: %s' % (tk, why))

    cleared = [tk for tk in rat if tk in on_disk and tk not in breaching]
    if cleared:
        print('\n  RATCHET ENTRIES NOW CLEAN: %s' % ', '.join(sorted(cleared)))
        if prune:
            keep = {k: v for k, v in rat.items() if k not in cleared}
            json.dump({'rule': 'R-FCAL-01 far-year ranges reach the reader',
                       'outstanding': keep},
                      open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
            print('  --prune: list shortened to %d' % len(keep))
        else:
            print('  run with --prune to shorten the list (it may only ever SHORTEN)')

    if fail:
        print('\nFAIL')
        for f in fail:
            print('  - ' + f)
        return 1
    print('\nOK — every run that computes a far-year band prints one, or is listed with '
          'its reason.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
