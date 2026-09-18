#!/usr/bin/env python3
"""[R-ENF-01] A DEFERRAL MAY NOT GIVE A STANDING RULE AS ITS REASON WHEN THAT RULE
DOES NOT SAY SO [R-REBUILD-01 CLAUSE TWO].

The clause was adopted 18-09-2026 on AMOC's own forecast-anchor record, which gave
[R-VCAL-01]'s one-lever-at-a-time guard as the reason a correction worth +55% was not
applied. That guard governs LEVERS PROMOTED FROM THE VALUATION CALIBRATION --
candidates seeking evidence -- and never corrections to defects; [R-REBUILD-01] says
in its own words that a study wrong in six ways moves a long way when all six are
fixed, and that WHAT IS FORBIDDEN IS THE MOVE BEING INVISIBLE.

MEASURED THE SAME DAY: the misreading had reached SIX passages across two study
builders and one ratchet, and EVERY ONE OF THEM DEFERRED A CORRECTION THAT RAISES THE
VALUE. That asymmetry is the finding rather than a detail beside it -- an
interpretation that always runs one way is not an interpretation.

NONE IS RATCHETED, because none had to be: every one already carried its MEASUREMENT
(+55%, 105 basis points), so correcting them was rewriting the REASON and keeping the
number. No value moved anywhere.

TWO STRENGTHS, ON PURPOSE, and the split is where the clause actually binds:

    a committed RECORD -- a ratchet entry, a study's own numbers -- is a hard refusal.
    a builder COMMENT is prose in code: it teaches the next reader the wrong reason
    and it is not a record, so it is MEASURED, PRINTED, and never a bar.

That is the prose_figures architecture and it is taken for its reason: a comment that
merely EXPLAINS the guard is ordinary and correct, and a gate that could not tell the
two apart would push builders to stop explaining things.

WHAT IT DELIBERATELY DOES NOT DECIDE: whether the deferral was WISE. Sequencing real
work is a real judgement and the clause says so. What a record may not do is dress
that judgement as a prohibition.

Ratcheted [R-ENF-02] at zero. Population-anchored [R-ENF-04] BOTH ways: zero files
read fails, and so does zero GUARD REFERENCES found across them -- because a matcher
that stopped matching reads exactly like a book with no false reasons in it.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'engine'))
import deferral_reason as DR                                        # noqa: E402

RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit',
                       'deferral_reason_outstanding.json')

# THE MODULE AND ITS CONTROL HOLD THE PATTERNS, SO THEY MATCH THEMSELVES. This is the
# same self-match that made a first measurement of lesson enforcement report 312 of
# 312 earlier the same day; excluded BY NAME rather than by a substring, because a
# substring exclusion is how a probe silently drops a directory [R-DOC-02].
SELF = {'engine/deferral_reason.py',
        'scripts/check_deferral_reason.py',
        'scripts/check_deferral_reason_negative_control.py'}


def _files():
    recs = sorted(set(glob.glob(os.path.join(ROOT, 'engine', '**', '*.json'),
                                recursive=True)))
    code = sorted(set(glob.glob(os.path.join(ROOT, 'engine', '**', '*.py'),
                                recursive=True)
                      + glob.glob(os.path.join(ROOT, 'scripts', '*.py'))))
    keep = lambda fs: [f for f in fs                                 # noqa: E731
                       if os.path.relpath(f, ROOT).replace('\\', '/') not in SELF]
    return keep(recs), keep(code)


def survey():
    """(record hits, comment hits, files read, guard references seen)."""
    recs, code = _files()
    hits_r, hits_c, read, refs = {}, {}, 0, 0
    for group, into in ((recs, hits_r), (code, hits_c)):
        for f in group:
            try:
                t = open(f, encoding='utf-8').read()
            except (OSError, UnicodeDecodeError):
                continue
            read += 1
            refs += len(DR.GUARD.findall(t))
            found = DR.passages(t)
            if found:
                into[os.path.relpath(f, ROOT)] = found
    return hits_r, hits_c, read, refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--prune', action='store_true',
                    help='rewrite the ratchet; it may only ever SHORTEN')
    a = ap.parse_args()

    hits_r, hits_c, read, refs = survey()
    if read == 0:
        print('FAIL — read zero files. An absent answer is not a clean one.')
        return 1
    if refs == 0:
        print('FAIL — %d file(s) read and NOT ONE reference to the promotion guard '
              'anywhere. A matcher that stopped matching reads exactly like a book '
              'with no false reasons in it [R-ENF-04].' % read)
        return 1

    r = json.load(open(RATCHET)) if os.path.exists(RATCHET) else {}
    allow = set(r.get('records', []))

    print('%d file(s) read, %d reference(s) to the guard; %d record(s) and %d '
          'builder comment(s) give it as the reason for a deferral'
          % (read, refs, len(hits_r), len(hits_c)))
    for f in sorted(hits_r):
        print('%s%s' % ('   ' if f in allow else '>> ', f))
        for ex, why in hits_r[f][:2]:
            print('       %s' % why)
    if hits_c:
        print('\n  ADVISORY — builder comments, measured and never a bar:')
        for f in sorted(hits_c):
            print('     %-46s %d' % (f, len(hits_c[f])))

    new = sorted(set(hits_r) - allow)
    if a.prune:
        if set(hits_r) - allow:
            print('\nREFUSED to prune — %s would GROW the list.' % ', '.join(new))
            return 1
        json.dump({**r, 'records': sorted(hits_r)}, open(RATCHET, 'w'),
                  indent=1, ensure_ascii=False)
        open(RATCHET, 'a').write('\n')
        print('\npruned — %d remain' % len(hits_r))
        return 0

    if new:
        print('\nFAIL — %d committed record(s) give a standing rule as the reason for '
              'a deferral the rule does not govern: %s' % (len(new), ', '.join(new)))
        return 1
    print('\nOK — no committed record gives the promotion guard as a reason. '
          '%d on the ratchet, which may only SHORTEN.' % len(allow))
    return 0


if __name__ == '__main__':
    sys.exit(main())
