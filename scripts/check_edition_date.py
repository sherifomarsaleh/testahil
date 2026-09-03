#!/usr/bin/env python3
"""[R-ENF-01] A DELIVERED DOCUMENT STATES ITS OWN EDITION DATE, AND STATES THE RIGHT ONE.

WHY THIS EXISTS, AND IT WAS FOUND BY READING RATHER THAN BY ANY GATE. ARCC shipped a
masthead a day stale and it was caught by a person reading the rendered pages. That was
recorded as a defect in one study. Reading PHDC's pages the same way found the identical
thing — a 3 September edition whose masthead reads "edition of 2 September 2026" — which
made it a CLASS rather than an incident, and closing the class rather than the instance is
what [R-ENF-01] requires.

Measured across every delivered valuation study: SEVEN OF THIRTY-ONE do not carry their own
edition date in their masthead, in three distinct shapes.

  STATED AND WRONG        PHDC (3 Sep edition reading 2 September), TMGH (2 Sep reading
                          1 September). Both a day stale, both otherwise clean, and ARCC
                          made three.
  STATED NOWHERE AT ALL   ADNOCLS and SAVOLA. The date in the filename appears in NO
                          paragraph of either document. A reader receives a valuation of a
                          listed company with nothing on it saying when it was struck —
                          and ADNOCLS IS THE MODEL REPORT, the document every other study
                          is written against.
  BURIED IN THE BODY      DU (paragraph 74, inside a sentence about a licence expiry),
                          GBCO (167, in an expert-log note) and RIYADHCABLE (119, in the
                          disclaimer). Present, but not where a reader looks for it, and
                          incidental rather than declared.

WHAT IS CHECKED AND WHAT IS NOT. The masthead must CARRY the filename's date in some
ordinary rendering of it. It is NOT required to be the only date there, and that matters:
AMOC's masthead reads "Valuation study as of 6 August 2026, issued 3 September 2026", which
is the better form — a study can be anchored on one date and issued on another, and saying
both is more honest than saying one. What may not happen is a document whose issue date
disagrees with the file it ships as, or is absent.

Ratcheted [R-ENF-02] — the seven are listed and allowed, the list may only ever SHORTEN.
Population-anchored [R-ENF-04]: a run that examined zero documents FAILS.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'edition_outstanding.json')
DATE = re.compile(r'(\d{2})-(\d{2})-(\d{4})')
# the masthead is the block before the document gets going. Ten paragraphs is generous:
# every study that states its date correctly does so within the first four.
MASTHEAD_PARAS = 10


def renderings(d):
    """Every ordinary way a human writes one date. Shape, not one house format.

    A study may render its date as it likes — the point of this check is that the date is
    THERE and RIGHT, not that every study writes it the same way. Requiring one format
    would fail documents that are perfectly correct, which is the check firing on work that
    is right [R-COC-01].
    """
    out = set()
    for f in ('%d %B %Y', '%d %b %Y', '%B %d, %Y', '%b %d, %Y', '%Y-%m-%d', '%d-%m-%Y',
              '%d/%m/%Y', '%d.%m.%Y'):
        s = d.strftime(f)
        out.add(s)
        out.add(re.sub(r'\b0(\d)', r'\1', s))      # 06 August -> 6 August
    return out


def documents():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study', '*.docx'))):
        b = os.path.basename(f)
        if b.startswith('~$') or 'Valuation_Study' not in b:
            continue
        m = DATE.search(b)
        if m:
            out.append((f, datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))))
    return out


def audit():
    from docx import Document
    examined, bad = 0, {}
    for f, dt in documents():
        rel = os.path.relpath(f, ROOT)
        try:
            doc = Document(f)
        except Exception as e:                                    # noqa: BLE001
            bad[rel] = 'will not open: %s' % e
            examined += 1
            continue
        examined += 1
        forms = renderings(dt)
        head = ' | '.join(p.text for p in doc.paragraphs[:MASTHEAD_PARAS])
        if any(x in head for x in forms):
            continue
        whole = ' | '.join(p.text for p in doc.paragraphs)
        where = next((i for i, p in enumerate(doc.paragraphs)
                      if any(x in p.text for x in forms)), None)
        if where is None:
            # is some OTHER date stated in the masthead? that is the stale-masthead shape,
            # and it is worse than an absent date because it reads as a fact.
            other = re.search(r'(\d{1,2} \w+ 20\d\d)', head)
            bad[rel] = ('the masthead states %r and the file is dated %s'
                        % (other.group(1), dt) if other
                        else 'the edition date %s appears NOWHERE in the document' % dt)
        else:
            bad[rel] = ('the edition date %s appears only at paragraph %d, not in the '
                        'masthead' % (dt, where))
    return examined, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()
    rat = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allowed = set(rat.get('outstanding', {}))

    examined, bad = audit()
    if not examined:
        print('FAIL — examined zero delivered studies; an empty result is not a clean '
              'result [R-ENF-04]')
        return 1
    stranded = sorted(p for p in allowed
                      if not os.path.exists(os.path.join(ROOT, p)))
    if stranded:
        print('FAIL — the ratchet names documents that no longer exist: %s [R-ENF-04]'
              % stranded)
        return 1

    print('delivered valuation studies examined: %d;  not carrying their own edition '
          'date: %d' % (examined, len(bad)))
    for p in sorted(bad):
        print('  [%s] %-52s %s' % ('ratcheted' if p in allowed else 'NEW',
                                   os.path.basename(p), bad[p]))
    fixed = sorted(allowed - set(bad))
    if fixed:
        print('\nNOW CARRYING IT — remove from the list (%d): %s'
              % (len(fixed), ', '.join(os.path.basename(x) for x in fixed)))

    if a.prune:
        grown = sorted(set(bad) - allowed)
        if grown:
            print('\nREFUSING TO PRUNE — the list would GROW by %s. A ratchet may only '
                  'ever SHORTEN [R-ENF-02].' % grown)
            return 1
        rat['outstanding'] = {k: bad[k] for k in sorted(set(bad) & allowed)}
        json.dump(rat, open(RATCHET, 'w'), indent=1)
        print('\npruned: %d -> %d' % (len(allowed), len(rat['outstanding'])))
        return 0

    new = sorted(set(bad) - allowed)
    if new:
        print('\nFAIL — a delivered document must state its own edition date in its '
              'masthead, and state the right one:\n  %s' % '\n  '.join(new))
        return 1
    print('\nOK — no new violations. %d document(s) on the ratchet, which may only SHORTEN.'
          % len(allowed))
    return 0


if __name__ == '__main__':
    sys.exit(main())
