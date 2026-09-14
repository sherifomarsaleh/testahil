#!/usr/bin/env python3
"""[R-ENF-01] DEPTH-BAR STANDARD 1 IS CHECKED OVER EVERY STUDY, NOT ONLY THE CALIBRATED
ONES, AND THE ARTEFACT HAS THREE NAMES.

Standard 1 requires a STANDALONE BIBLIOGRAPHY DOCUMENT beside every delivered study —
the primary-documents table, the full input register, the judgements table, the
negative-results table. The bar says of its own list that each item is "a QC item,
missing one = FAIL, not a noted limitation".

WHAT CHECKED IT: `check_calibration_deliverables` asserts exactly this, and its
population is the WALK-FORWARD RUN DIRECTORIES — five names. The other nineteen studies
were covered by `bibliography_document`, A BOOLEAN EACH STUDY SETS ON ITSELF. So the
standard was enforced on a fifth of the book and attested on the rest, and the gap is
where the breach turned out to be.

ONE STUDY SHIPS A VALUATION DOCUMENT AND A WORKBOOK AND NO BIBLIOGRAPHY-CLASS DOCUMENT
AT ALL. It is a study that predates the bar and is already listed on four other
ratchets, so this finds nothing anybody has to fix tonight — what it finds is that
nothing was looking.

THE ARTEFACT HAS THREE NAMES AND THAT IS THE PART THAT MATTERS. Twenty-one studies ship
`..._Bibliography_...`, one ships `..._Source_Register_...` and one ships
`..._Sources_...`; and one study's file carries THE COMPANY'S OTHER NAME rather than its
ticker. A check written against the obvious convention would have condemned three
studies that are perfectly compliant, and a check written against the ticker prefix a
fourth. THE AUTHOR'S FIRST TWO PROBES DID EXACTLY THAT — the first grepped for
'bibliograph' and reported two breaches where there is one, the second would have missed
the company-named file — which is the same failure this repository has now recorded
several times in one day: A READER THAT GUESSES A NAMING CONVENTION SILENTLY FINDS
NOTHING. The three variants are therefore NAMED IN CODE, from what the book actually
ships, rather than inferred.

WHAT IT DELIBERATELY DOES NOT DO: it does not read the document's CONTENTS. Whether a
bibliography carries its four tables is depth-bar content, checked inside the study and
by the QC gate; this asks only whether the standalone artefact a reader is supposed to
receive EXISTS. A gate that tried to judge depth from outside would be making a claim it
cannot support, which is worse than the narrow claim it can.

A STUDY THAT SHIPS NO DELIVERED DOCUMENT IS NOT IN SCOPE, and saying so is not a
loophole: a metals directory delivers no valuation study at all, and a study directory
with nothing in it has nothing to be missing a bibliography FROM. That makes this
ARTEFACT-conditional in the new-study gauntlet [R-ENF-07] — demanding it refuse an empty
directory would be a false claim about what it checks.

RATCHET [R-ENF-02]: the one breaching study is listed with its reason and may only ever
leave the list. POPULATION-ANCHORED [R-ENF-04] BOTH WAYS — a run examining zero study
directories FAILS, and so does one that found zero DELIVERED STUDY DOCUMENTS across
present directories, because a matcher that stopped matching reads exactly like a clean
book.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'bibliography_outstanding.json')

# The delivered study document a reader receives.
STUDY_DOC = re.compile(r'valuation[_ ]study.*\.docx$', re.I)

# THE BIBLIOGRAPHY-CLASS ARTEFACT, all three names the book actually uses. Named from
# the shipped files rather than from the obvious convention — see the docstring.
BIBLIO = re.compile(r'(bibliograph|source[_ ]register|_sources_)', re.I)


def load_ratchet():
    if not os.path.exists(OUTSTANDING):
        return []
    return json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', [])


def census():
    rows = []
    for d in sorted(glob.glob(os.path.join(ENGINE, '*_study'))):
        tk = os.path.basename(d)[:-len('_study')].upper()
        try:
            names = os.listdir(d)
        except OSError as exc:
            rows.append(dict(ticker=tk, state='unreadable', why=str(exc)[:80]))
            continue
        studies = [n for n in names if STUDY_DOC.search(n)]
        biblio = [n for n in names
                  if n.lower().endswith('.docx') and BIBLIO.search(n)
                  and not STUDY_DOC.search(n)]
        rows.append(dict(ticker=tk, state='read', studies=sorted(studies),
                         biblio=sorted(biblio)))
    return rows


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    rows = census()
    delivering = [r for r in rows if r['state'] == 'read' and r['studies']]
    dark = [r for r in rows if r['state'] != 'read']

    print('BIBLIOGRAPHY GATE  [R-ENF-01]  depth-bar standard 1')
    print('   every delivered study ships a STANDALONE bibliography-class document;')
    print('   three names are accepted (%s) because that is what the book ships'
          % 'Bibliography / Source_Register / Sources')
    print('   %d study directories · %d delivering a study document · %d shipping one'
          % (len(rows), len(delivering), sum(1 for r in delivering if r['biblio'])))

    fail = []
    if not rows:
        print('\nFAIL — the gate examined ZERO study directories. An empty result is '
              'not a clean result.')
        return 1
    if not delivering:
        print('\nFAIL — the gate found ZERO delivered study documents across %d study '
              'directories. A matcher that stopped matching reads exactly like a clean '
              'book [R-ENF-04].' % len(rows))
        return 1

    on_disk = {r['ticker'] for r in rows}
    for tk in sorted(rat):
        if tk not in on_disk:
            fail.append('the ratchet lists %s and no such study directory exists — the '
                        'list is anchored on nothing' % tk)
    for r in dark:
        fail.append('%s: directory unreadable (%s). An unreadable study is not a clean '
                    'study [R-ENF-04].' % (r['ticker'], r['why']))

    missing = [r for r in delivering if not r['biblio']]
    cleared = [tk for tk in rat
               if tk in on_disk and tk not in {r['ticker'] for r in missing}]

    print('\n  DELIVERING A STUDY WITH NO BIBLIOGRAPHY: %d' % len(missing))
    for r in sorted(missing, key=lambda r: r['ticker']):
        tk = r['ticker']
        mark = 'ratcheted' if tk in rat else 'NEW'
        print('    %-12s ships %s and no bibliography-class document  [%s]'
              % (tk, r['studies'][0], mark))
        if tk not in rat:
            fail.append('%s delivers a valuation study with no standalone '
                        'bibliography document. Depth-bar standard 1 calls a missing '
                        'item a FAIL, not a noted limitation.' % tk)

    if cleared:
        print('\n  RATCHET ENTRIES NOW CLEAN: %s' % ', '.join(sorted(cleared)))
        if prune:
            keep = [t for t in rat if t not in cleared]
            json.dump({'rule': 'R-ENF-01/depth-bar standard 1', 'outstanding': keep},
                      open(OUTSTANDING, 'w', encoding='utf-8'), indent=1)
            print('  --prune: list shortened to %d' % len(keep))
        else:
            print('  run with --prune to shorten the list (it may only ever SHORTEN)')

    if fail:
        print('\nFAIL')
        for f in fail:
            print('  - ' + f)
        return 1
    print('\nOK — every delivered study ships the standalone bibliography the bar '
          'requires.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
