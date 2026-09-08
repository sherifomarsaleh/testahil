#!/usr/bin/env python3
"""The delivered workbook must publish the answer the study publishes — checked by RUNNING
each study's own recalculation, not by noting that it has one.

WHY THIS EXISTS
    Depth-bar standard 3 requires that "an independent evaluator recalculates the delivered
    workbook and reports anything unparseable as FAILURE, never a skip", and the QC gate of
    every study in this book carries a row attesting it. Twenty-two of twenty-four studies
    carry the instrument to do it. Measured on 5 September 2026, NO GATE ANYWHERE RAN ANY OF
    THEM — every mention of the word "recalculation" outside a study directory is a sentence
    in a comment. What that cost:

        SWDY   the delivered workbook a reader opens publishes SAR 59.31 where the delivered
               document publishes 55.48, +6.9%, with ZERO formula errors. Two independent
               formula defects pulling opposite ways: DCF!C25 still carries the g x IC
               reinvestment-identity terminal that [R-TERM-01] retired on 03-Sep (the study's
               own compute.py computes that same figure and labels it "published unused,
               feeds nothing"), worth -6.5% alone; and SOTP Bridge!C12 has NO LINE for the
               employees' statutory share of profit that compute.py deducts at 12.19%, worth
               +14.4% alone. The builder's own expected-value map records the RIGHT answer
               for both cells — so the builder knew, and wrote a formula that cannot reach
               it. The study's recalc.py FAILS on this today, in 0.4 seconds, naming all 27
               cells. It was simply never run after the 4-Sep rebuild.

        AMOC   its recalculator refuses outright: it was written for the NINE-sheet workbook
               of 06-08-2026 and the delivered file is the SIXTEEN-sheet edition of 01-09.
               That is L-066/L-067 verbatim — A CHECK THAT OPENS A DELIVERED FILE BY NAME
               MOVES WITH THE RE-ISSUE — registered on this very study a week ago, on two of
               its own gates, and the third one broke the same way.

    Neither is a modelling error and both reach a reader. They survive because a study's own
    check is run by whoever remembers to run it, and the moment a rebuild lands is exactly
    the moment nobody does.

WHAT THIS GATE REQUIRES, AND WHAT IT DELIBERATELY DOES NOT
    It RUNS the instrument. Treating a script's existence as conformance would put a green
    tick on a red result — which is case 2 of the prose-figure gate's negative control and
    the case that matters most, and here it is not hypothetical: SWDY has the script, the
    script is correct, and the script is red.

    It does NOT prescribe what the recalculation must check, or how. The studies use two
    evaluators (an in-repo one and a headless spreadsheet) and reconcile between 85 and 1,318
    cells; imposing one shape would mean rewriting twenty-two working instruments to satisfy
    a checker, which is the "move the number to satisfy the check" move this house forbids
    in its own words. What it requires is that the study's own check PASSES.

    A SCRIPT THAT CANNOT RUN IS RED, NOT SKIPPED [R-ENF-04]. A missing dependency, a timeout
    and a crash all produce an ABSENT answer, and an absent answer wearing the costume of a
    clean one is strictly worse than a failure, because a failure announces itself.

THE POPULATION IS ANCHORED ELSEWHERE, BOTH WAYS  [R-ENF-04]
    Every ticker listed in the ratchet must resolve to a study directory on disk; a run that
    examined zero directories FAILS; and a run that RAN zero checks across present
    directories FAILS, which is the distinction an absent answer hides behind.

THE RATCHET  [R-ENF-02]
    Two groups, and they are NOT interchangeable — the same lesson [R-TERM-01]'s negative
    control learned: an entry able to travel between groups would let a study escape a real
    disagreement by being re-filed as merely unchecked. `no_check` excuses a study with no
    recalculation script; `failing` excuses one whose script exists and is red. A study
    moving from one to the other is a CHANGE and goes red until the move is recorded.
    The lists may only ever SHORTEN. --prune rewrites them.

USAGE
    python3 scripts/check_workbook_values.py
    python3 scripts/check_workbook_values.py --prune
"""
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATCHET = os.path.join(ROOT, 'engine', 'build_depth_audit', 'workbook_values_outstanding.json')
# The two names a study's recalculation goes by, in the order they are looked for.
SCRIPTS = ('recalc.py', 'lo_recalc_gate.py')
TIMEOUT = 600


def load_ratchet():
    if not os.path.exists(RATCHET):
        return {'no_check': {}, 'failing': {}}
    d = json.load(open(RATCHET))
    return {'no_check': d.get('no_check', {}), 'failing': d.get('failing', {})}


def studies():
    return sorted(glob.glob(os.path.join(ROOT, 'engine', '*_study')))


def script_for(d):
    for name in SCRIPTS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return name
    return None


def run_one(d, name):
    """(ok, tail). A crash, a timeout and a nonzero exit are all NOT ok."""
    try:
        r = subprocess.run([sys.executable, name], cwd=d, timeout=TIMEOUT,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired:
        return False, 'TIMED OUT after %ds — an absent answer is not a clean one' % TIMEOUT
    except Exception as e:                                          # noqa: BLE001
        return False, 'could not run: %s' % e
    out = r.stdout.decode('utf-8', 'replace').strip().splitlines()
    return r.returncode == 0, (out[-1][:160] if out else '(no output)')


def main(argv):
    prune = '--prune' in argv
    rat = load_ratchet()
    dirs = studies()
    if not dirs:
        print('FAIL — examined ZERO study directories. The resolver is broken, not the book.')
        return 1

    # every listed ticker must resolve on disk [R-ENF-04]
    on_disk = {os.path.basename(d)[:-len('_study')].upper() for d in dirs}
    for grp in ('no_check', 'failing'):
        for tk in rat[grp]:
            if tk.upper() not in on_disk:
                print('FAIL — %s is listed under %r and has no study directory on disk.'
                      % (tk, grp))
                return 1

    ran = 0
    clean, red, missing = [], [], []
    for d in dirs:
        tk = os.path.basename(d)[:-len('_study')].upper()
        name = script_for(d)
        if name is None:
            missing.append(tk)
            continue
        ok, tail = run_one(d, name)
        ran += 1
        (clean if ok else red).append((tk, name, tail))

    if ran == 0:
        print('FAIL — %d study directories are present and ZERO recalculations RAN. An '
              'empty result is not a clean result.' % len(dirs))
        return 1

    print('WORKBOOK VALUES — each study\'s own recalculation, run rather than counted')
    print('examined %d study directories; ran %d recalculations' % (len(dirs), ran))
    print()
    if clean:
        print('CLEAN (%d): %s' % (len(clean), ', '.join(t for t, _, _ in clean)))

    problems = []
    for tk, name, tail in red:
        if tk in rat['failing']:
            continue
        problems.append(('failing', tk, '%s exits nonzero: %s' % (name, tail)))
    for tk in missing:
        if tk in rat['no_check']:
            continue
        problems.append(('no_check', tk, 'no recalculation script in the study directory'))

    # A study on the WRONG list is a change, not nothing.
    for tk, name, tail in red:
        if tk in rat['no_check']:
            problems.append(('moved', tk, 'listed as having NO check, and it has one that '
                                          'is RED — the two allowances are not '
                                          'interchangeable: %s' % tail))
    for tk in missing:
        if tk in rat['failing']:
            problems.append(('moved', tk, 'listed as FAILING, and its script has gone — an '
                                          'allowance for a red check does not excuse an '
                                          'absent one'))

    if red:
        print()
        print('RED (%d):' % len(red))
        for tk, name, tail in red:
            mark = '  [on the ratchet] ' if tk in rat['failing'] else '  ** NEW ** '
            print('%s%-12s %s — %s' % (mark, tk, name, tail))
    if missing:
        print()
        print('NO CHECK (%d): %s' % (len(missing), ', '.join(missing)))

    if prune:
        new = {'no_check': {t: rat['no_check'][t] for t in missing if t in rat['no_check']},
               'failing': {t: rat['failing'][t] for t in
                           [x[0] for x in red] if t in rat['failing']}}
        cut = ((len(rat['no_check']) - len(new['no_check']))
               + (len(rat['failing']) - len(new['failing'])))
        new['note'] = json.load(open(RATCHET)).get('note', '')
        json.dump(new, open(RATCHET, 'w'), indent=1, sort_keys=True)
        print('\npruned %d entr%s; the list may only ever get shorter.'
              % (cut, 'y' if cut == 1 else 'ies'))
        return 0

    if problems:
        print()
        for kind, tk, why in problems:
            print('  ! %-8s %-12s %s' % (kind, tk, why))
        print('\nFAIL — a delivered workbook must publish the answer the study publishes.')
        return 1
    print('\nOK — no new disagreement between a delivered workbook and its study.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
