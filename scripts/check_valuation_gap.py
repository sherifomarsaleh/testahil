#!/usr/bin/env python3
"""A fair value far BELOW the traded price is a claim that needs auditing.  [R-GAP-01]

WHY THIS EXISTS
    On 1 September 2026 the AMOC rebuild published a central fair value of EGP 5.53
    against a market price of EGP 9.10 — thirty-nine per cent below — and every gate in
    this repository passed it. SIGCM passed. The beta was conforming. The model-report bar
    passed. The workbook recalculated with zero disagreements across 5,775 formula cells.
    The external-reader scrub was clean. None of that was wrong; none of it was looking at
    the answer.

    What the answer was hiding: the reviewed half-year statements had been downloaded from
    the company's own archive and never opened, so the study was still calling that period
    "a press release rather than a filing" and had solved its gross profit from the profit
    line; the coherence test that justified doing so estimated the half's other income by
    doubling one quarter's; three macro paths contradicted each other; the operating cash
    flows were discounted at a rate 374 basis points ABOVE the cost of equity because the
    company holds net cash, and the same cash was then added back at face; terminal growth
    of 5% sat against a terminal discount rate embedding 7% inflation; and the headline
    claimed the market price required a margin "above the best single quarter this company
    has ever filed" when the company had filed a higher one twice. Corrected, the study
    prints 8.64 against 9.10.

    Every one of those is the model being wrong, not the company being cheap. The market
    price was the only thing in the room saying so.

WHAT IT CHECKS, per study directory under engine/*_study/
    1. the study's own committed numbers resolve to a central fair value and the spot it
       was struck against — a study whose answer cannot be read is NOT clean [R-ENF-04]
    2. where the central sits more than GAP_LIMIT below OR GAP_LIMIT_ABOVE above that spot, a dated gap review
       exists in the study directory
    3. that review actually covers the required headings, so it cannot be a rubber stamp

THE RATCHET
    Known breaches and unreadable studies are listed in gap_outstanding.json and allowed
    to fail; the build breaks on a NEW breach, a NEW unreadable study, or a study directory
    with no entry either way. The list may only ever get SHORTER — --prune rewrites it.
    A permanently red check is one everyone learns to ignore.

THE POPULATION IS ANCHORED ELSEWHERE  [R-ENF-04]
    This gate globs engine/*_study, so a mis-resolved ENGINE or a bad pattern would find
    nothing and report "no new violations" — an ABSENT answer wearing the costume of a
    clean one. It therefore holds its own glob against a population counted somewhere
    else: every ticker already named in gap_outstanding.json must resolve to a study
    directory on disk. Defeating that would mean deleting the studies themselves, which is
    a far louder failure than an empty listing. It is EXACT, never a threshold. An empty
    outstanding list is not an escape either — a run that examined zero studies FAILS.

USAGE
    python3 scripts/check_valuation_gap.py          # gate; exit 1 on any hard fail
    python3 scripts/check_valuation_gap.py --prune  # drop the now-passing entries
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'gap_outstanding.json')

# The trigger. As instructed on 1 September 2026: a central fair value more than ten per
# cent BELOW the latest known market price. TWO-SIDED FROM 2 September 2026 [R-GAP-01
# amended, method reassessment WS7]: the same ten per cent ABOVE the price fires the same
# eight-heading review.
#
# Why the extension. The one-sidedness was on the record as a decision, and its stated cost
# was that an over-optimistic study would get no automatic audit and that nothing else
# supplied one. The method reassessment then measured what the one-sided defence had cost:
# because only the downside was audited, every correction the house made ran the same way,
# and the lean survived inside a process that looked rigorous. A gate that can only fire in
# one direction teaches the work to drift in the other.
#
# The trigger stays EVIDENTIAL rather than deferential, in both directions. A large gap
# either way is a high-prior-of-defect region, and the price is the only instrument in the
# room that measures it. The rule does not say the answer must change: a genuine 39%
# discount and a genuine 39% premium are both legitimate conclusions, and this project
# publishes ranges precisely because prices are sometimes wrong. It says the answer is
# AUDITED before it ships.
#
# The threshold is the instruction's own and is not dressed up as a derivation. What is
# defensible is the shape: a review costs an hour and a shipped error costs the study.
GAP_LIMIT = -0.10
GAP_LIMIT_ABOVE = 0.10

# What a review must cover. These are not invented headings: each one names a defect that
# was actually present in the AMOC study the day this rule was adopted, and each was
# individually capable of producing the whole gap.
REQUIRED_SECTIONS = {
    'LATEST FILINGS': 'every disclosed period actually read, the most recent named with its date',
    'BASE YEAR': 'foots to filed periods, and what is annualised or solved rather than filed',
    'MACRO COHERENCE': 'inflation, currency and price paths mutually consistent',
    'DISCOUNT RATE': 'the operating rate is the right one and cash is charged for once',
    'TERMINAL': 'terminal growth coherent with the inflation inside the terminal discount rate',
    'BALANCE SHEET': 'the bridge stands on the latest disclosed balance sheet',
    'CLAIMS AGAINST THE RECORD': 'every "best ever"/"never" statement checked against the filings',
    'MULTIPLE CROSS-CHECK': 'the earnings and enterprise multiples the fair value implies',
}
REVIEW_GLOB = 'GAP_REVIEW_*.md'


def _num(x):
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, dict):
        for k in ('value', 'central', 'base', 'mid'):
            if isinstance(x.get(k), (int, float)):
                return float(x[k])
    return None


def read_answer(sdir):
    """The study's own central fair value and the spot it was struck at.

    Returns (central, spot, route) or (None, None, why). Deliberately tries the shapes the
    studies in this repository actually use rather than one canonical schema — and returns
    the ROUTE it took, because a number found by a fallback is not the same evidence as one
    found where it belongs.
    """
    for fn in ('study_numbers.json', 'numbers.json'):
        p = os.path.join(sdir, fn)
        if not os.path.exists(p):
            continue
        try:
            j = json.load(open(p, encoding='utf-8'))
        except Exception as e:
            return None, None, 'unreadable %s: %s' % (fn, e)
        meta = j.get('meta') or {}
        central = _num(j.get('central')) or _num(j.get('fair')) or _num(meta.get('central'))
        spot = _num(j.get('spot')) or _num(meta.get('spot'))
        if central is not None and spot:
            return central, spot, fn
        return None, None, '%s carries no central/spot pair' % fn
    return None, None, 'no committed numbers file'


def read_review(sdir):
    """The most recent gap review in a study directory, and the headings it covers."""
    hits = sorted(glob.glob(os.path.join(sdir, REVIEW_GLOB)))
    if not hits:
        return None, []
    txt = open(hits[-1], encoding='utf-8').read().upper()
    covered = [k for k in REQUIRED_SECTIONS if k in txt]
    return os.path.basename(hits[-1]), covered


def load_outstanding():
    d = json.load(open(OUTSTANDING, encoding='utf-8'))
    return d, set(d.get('breach_no_review', [])), set(d.get('unreadable', []))


def main(argv):
    prune = '--prune' in argv
    d, known_breach, known_unreadable = load_outstanding()

    sdirs = sorted(glob.glob(os.path.join(ENGINE, '*_study')))
    ok, breaches, unreadable, reviewed, new_fail = [], [], [], [], []

    # [R-ENF-04] the population, counted somewhere other than this gate's own glob
    on_disk = {os.path.basename(s).replace('_study', '').upper() for s in sdirs}
    vanished = sorted((known_breach | known_unreadable) - on_disk)
    if not sdirs:
        new_fail.append('this gate examined ZERO study directories. An empty result is not '
                        'a clean result — re-run the glob before believing the absence.')
    if vanished:
        new_fail.append('%d study directory(ies) named in gap_outstanding.json do not resolve '
                        'on disk (%s). Either the glob did not run or the studies were removed '
                        'without pruning the list; neither is a pass.'
                        % (len(vanished), ', '.join(vanished)))

    for sdir in sdirs:
        tk = os.path.basename(sdir).replace('_study', '').upper()
        central, spot, route = read_answer(sdir)
        if central is None:
            unreadable.append((tk, route))
            if tk not in known_unreadable:
                new_fail.append('%s: its committed numbers do not resolve to a central fair '
                                'value and a spot (%s). A study whose answer cannot be read '
                                'is not a study that passed.' % (tk, route))
            continue
        gap = central / spot - 1.0
        if GAP_LIMIT <= gap <= GAP_LIMIT_ABOVE:
            ok.append((tk, gap))
            continue
        side = 'below' if gap < 0 else 'above'
        review, covered = read_review(sdir)
        missing = [k for k in REQUIRED_SECTIONS if k not in covered]
        if review and not missing:
            reviewed.append((tk, gap, review))
            continue
        breaches.append((tk, gap, review, missing))
        if tk not in known_breach:
            why = ('no gap review in the study directory' if not review
                   else 'the review %s does not cover %s' % (review, ', '.join(missing)))
            new_fail.append('%s: central is %.1f%% %s the spot it was struck at, and %s.'
                            % (tk, abs(100 * gap), side, why))

    print('study directories: %d   readable: %d   reviewed: %d   breaching: %d   unreadable: %d'
          % (len(sdirs), len(ok) + len(reviewed) + len(breaches), len(reviewed),
             len(breaches), len(unreadable)))
    print('trigger: central more than %.0f%% BELOW or %.0f%% ABOVE the spot it was struck at\n'
          % (-100 * GAP_LIMIT, 100 * GAP_LIMIT_ABOVE))

    if reviewed:
        print('OUTSIDE THE BAND, AND REVIEWED (%d):' % len(reviewed))
        for tk, gap, rv in reviewed:
            print('   %-12s %+6.1f%%  %s' % (tk, 100 * gap, rv))
    if breaches:
        print('\nOUTSIDE THE BAND, NOT REVIEWED (%d):' % len(breaches))
        for tk, gap, rv, missing in breaches:
            state = 'no review' if not rv else 'missing: ' + ', '.join(missing)
            print('   %-12s %+6.1f%%  %s' % (tk, 100 * gap, state))
    if unreadable:
        print('\nANSWER NOT READABLE (%d) — tracked, because an unreadable answer is not a '
              'clean one:' % len(unreadable))
        for tk, why in unreadable:
            print('   %-12s %s' % (tk, why))

    now_passing = sorted(({tk for tk, _, _, _ in breaches} ^ known_breach) & known_breach) + \
        sorted(({tk for tk, _ in unreadable} ^ known_unreadable) & known_unreadable)
    if now_passing:
        print('\nNOW PASSING — remove from the list (%d): %s'
              % (len(now_passing), ', '.join(now_passing)))

    if prune:
        d['breach_no_review'] = sorted({tk for tk, _, _, _ in breaches} & known_breach)
        d['unreadable'] = sorted({tk for tk, _ in unreadable} & known_unreadable)
        json.dump(d, open(OUTSTANDING, 'w'), indent=1)
        print('\npruned; %d breach + %d unreadable remain'
              % (len(d['breach_no_review']), len(d['unreadable'])))
        return 0

    if new_fail:
        print('\nFAIL — %d new violation(s):' % len(new_fail))
        for m in new_fail:
            print('   ' + m)
        print('\nA fair value far from the traded price, in EITHER direction, is the case '
              'where the market is telling you something the model may have missed. Write '
              'the review, or fix what it would have found.')
        return 1
    print('\nOK — no new violations.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
