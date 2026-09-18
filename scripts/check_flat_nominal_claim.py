#!/usr/bin/env python3
"""[R-ENF-01] A QUANTITY HELD FLAT IN NOMINAL TERMS IS A REAL-DECLINE FORECAST, AND A
STUDY MAY NOT CALL IT THE ABSENCE OF ONE.

[R-MACRO-01] requires growth rates to be stored as (real, inflation-path id) and to
recompute to their nominal, because A TYPED NOMINAL RATE IS UNFALSIFIABLE. A quantity
held flat is a typed nominal rate of zero whose real component is minus whatever
inflation applies, stated nowhere.

WHAT IS REFUSED IS THE CLAIM, NOT THE CONSTRUCTION. Holding a traded commodity price
flat in dollars is legitimate, common and often sensible. Describing it as "no forecast
of a traded commodity price is defensible" is a FALSE STATEMENT ABOUT THE MODEL: the
model forecasts a price falling every year for ever, and the reader is told the
opposite.

MEASURED ACROSS EVERY STUDY BUILDER AND COMMITTED RECORD -- 898 files, 361 mentions of a
quantity held flat -- TWO STUDIES DENY IT AND TWO NAME IT, and the two that name it are
what makes this checkable:

    NAMED     "flat in nominal terms, which is a REAL DECLINE across the window"
    NAMED     "holding earnings flat in NOMINAL terms while discounting at a NOMINAL rate"
    DENIED    "held FLAT in dollars -- no forecast of it is defensible"
    DENIED    "Holding a traded commodity price flat RATHER THAN FORECASTING IT is
               settled house convention AND IS NOT CONTESTED"

THE SECOND DENIAL HAS A CONSEQUENCE BEYOND THE READER, and it is the sharper one: by
calling the choice "not contested" it keeps a material judgement OUT OF [R-ENF-05]'s
sign test -- the instrument built to count which way a study's judgements go. A denial
that removes its own subject from the measurement is not a wording problem.

THE COST IS MEASURED ELSEWHERE AND IS NOT SMALL: closing the escalator wedge this
convention creates is worth +17.8% on one of the two and +68.7% on the other, because
in both the costs escalate at FULL domestic inflation while the revenue does not -- and
the manufactured margin decline is then reported as a finding.

10 passages in 361 mentions, 2.8%, ZERO false positives on inspection. Ratcheted at two
with their measurement [R-ENF-08]; population-anchored [R-ENF-04] BOTH ways.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import flat_nominal_claim as FN                                    # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit',
                       'flat_nominal_outstanding.json')
SELF = {'engine/flat_nominal_claim.py'}


def survey():
    """(hits, files read, 'held flat' mentions seen)."""
    hits, read, flats = {}, 0, 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study', '*.py'))
                    + glob.glob(os.path.join(ROOT, 'engine', '*_study', '*.json'))):
        rel = os.path.relpath(f, ROOT).replace('\\', '/')
        if rel in SELF:
            continue
        tk = os.path.basename(os.path.dirname(f)).replace('_study', '').upper()
        try:
            t = open(f, encoding='utf-8').read()
        except (OSError, UnicodeDecodeError):
            continue
        read += 1
        flats += len(FN.FLAT.findall(t))
        for ex, why in FN.passages(t):
            hits.setdefault(tk, []).append((os.path.basename(f), ex, why))
    return hits, read, flats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true')
    a = ap.parse_args()

    hits, read, flats = survey()
    if read == 0:
        print('FAIL — read zero study files. An absent answer is not a clean one.')
        return 1
    if flats == 0:
        print('FAIL — %d file(s) read and NOT ONE quantity held flat anywhere. A matcher '
              'that stopped matching reads exactly like a book that never holds anything '
              'flat [R-ENF-04].' % read)
        return 1

    r = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allow = set(r.get('denying', []))
    on_disk = {os.path.basename(d).replace('_study', '').upper()
               for d in glob.glob(os.path.join(ROOT, 'engine', '*_study'))}
    ghosts = sorted(allow - on_disk)
    if ghosts:
        print('FAIL — the ratchet names studies not on disk: %s' % ', '.join(ghosts))
        return 1

    print('%d file(s) read, %d quantit%s held flat; %d stud%s call it the absence of a '
          'forecast' % (read, flats, 'y' if flats == 1 else 'ies', len(hits),
                        'y' if len(hits) == 1 else 'ies'))
    for tk in sorted(hits):
        print('%s%-12s %d passage(s)' % ('   ' if tk in allow else '>> ', tk,
                                         len(hits[tk])))
        for f, ex, _why in hits[tk][:2]:
            print('       %-26s %s' % (f, ex[:86]))

    new = sorted(set(hits) - allow)
    if a.prune:
        if set(hits) - allow:
            print('\nREFUSED to prune — %s would GROW the list.' % ', '.join(new))
            return 1
        json.dump({**r, 'denying': sorted(hits)}, open(RATCHET, 'w'),
                  indent=1, ensure_ascii=False)
        open(RATCHET, 'a').write('\n')
        print('\npruned — %d remain' % len(hits))
        return 0

    if new:
        print('\nFAIL — %d stud%s newly describing a flat nominal path as the absence of '
              'a forecast: %s' % (len(new), 'y' if len(new) == 1 else 'ies',
                                  ', '.join(new)))
        return 1
    print('\nOK — %d on the ratchet, which may only SHORTEN.' % len(allow))
    return 0


if __name__ == '__main__':
    sys.exit(main())
