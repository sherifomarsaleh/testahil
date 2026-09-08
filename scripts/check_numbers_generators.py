#!/usr/bin/env python3
"""[R-ENF-01] A STUDY WHOSE NUMBERS FILE HAS TWO GENERATORS DECLARES THEIR ORDER.

Adding one line to SWDY's lens record and rebuilding it produced an EIGHTEEN-LINE
diff, and the sixteen deleted lines were that study's entire [R-ANCHOR-01]
forecast_anchor record — a long, carefully evidenced block recording that no
closed-list mechanism fits that company's filings. study_numbers.json there is
written WHOLE by compute.py and that block is appended AFTERWARDS by a second
script. Nothing in either file, or anywhere else, said so.

IT WAS CAUGHT BY READING A DIFFSTAT. No gate could have caught it, and that is a
property of gates rather than an oversight in them: A GATE READS THE FILE THAT IS
THERE AND CANNOT KNOW WHAT A REBUILD REMOVED.

WHAT THIS CHECKS, and it is deliberately narrow. Not that the numbers file
reproduces — running every study's model would take minutes and would fail for
reasons that have nothing to do with this defect. It checks that where more than
one script WRITES the file, the study SAYS SO, in the first place a rebuilder
looks: the run order is declared in the main generator's own module docstring.
The declaration is what was missing; the arithmetic was never in doubt.

THE INSTRUMENT IS SHARED (engine/numbers_generators.py) rather than copied into
each study, which is the prose-figures finding: a rule that one study implements
is a rule that one study obeys. Three studies had each written the restore-guard
for themselves and it bound nowhere else.

CLASSIFICATION IS DECLARED, DETECTION IS MECHANICAL. A writer whose write is a
RESTORE — its value read from the same file earlier in the same script — is a
guard, not a generator, and is not counted. That distinction was got wrong twice
by the author of this gate before it was got right.

RATCHET [R-ENF-02]: studies already carrying an undeclared second generator are
listed and allowed to fail; the build breaks on a NEW one. The list may only
SHORTEN. POPULATION-ANCHORED [R-ENF-04] both ways: a run that examined zero study
directories FAILS, and so does one that found no writer for some study, because a
detector that cannot find a generator has not proved there is none.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, 'engine')
sys.path.insert(0, ENGINE)
OUTSTANDING = os.path.join(ENGINE, 'build_depth_audit', 'generators_outstanding.json')


def declared_order(study_dir, generators):
    """The run order a study declares, read from its main generator's docstring.

    A docstring rather than a JSON field ON PURPOSE: the failure is somebody
    rebuilding a study by running its compute.py, and the first thing they open is
    that file. A declaration in a numbers file they never look at would be a
    record of the rule rather than an application of it.
    """
    for g in generators:
        p = os.path.join(study_dir, g)
        try:
            head = open(p, encoding='utf-8').read(4000)
        except OSError:
            continue
        if 'RUN ORDER' in head.upper():
            named = [x for x in generators if x in head]
            return g, named
    return None, []


def main(argv):
    import numbers_generators as NG

    prune = '--prune' in argv
    try:
        known = set(json.load(open(OUTSTANDING, encoding='utf-8')).get('outstanding', []))
    except FileNotFoundError:
        known = set()

    census = NG.census()
    if not census:
        print('FAIL — examined zero study directories. An empty result is not a clean '
              'result [R-ENF-04].')
        return 1
    blind = sorted(k for k, v in census.items() if not v)
    if blind:
        print('FAIL — no writer found for %s. A detector that cannot find a generator '
              'has not proved there is none [R-ENF-04].' % ', '.join(blind))
        return 1

    multi, ok, still, hard = {}, [], [], []
    for tk, ws in sorted(census.items()):
        d = os.path.join(ENGINE, '%s_study' % tk.lower())
        guards = set(NG.restorers(d))
        gens = [w for w in ws if w not in guards]
        if len(gens) < 2:
            continue
        multi[tk] = gens
        where, named = declared_order(d, gens)
        missing = [g for g in gens if g not in named]
        if where and not missing:
            (still if tk in known else ok).append((tk, '%s declares: %s' % (where, ', '.join(named))))
        else:
            why = ('no generator declares a RUN ORDER' if not where
                   else '%s declares a run order that does not name %s'
                        % (where, ', '.join(missing)))
            (still if tk in known else hard).append((tk, why))

    print('NUMBERS-FILE GENERATORS  [R-ENF-01]')
    print('   a rebuild running one generator deletes what the others appended, and no')
    print('   gate can see it: a gate reads the file that is there')
    print('   %d study directories · %d written by more than one generator · %d declared'
          % (len(census), len(multi), len(ok) + sum(1 for t, _ in still if t in dict(still))))
    for tk, d in ok:
        print('   %-12s %s' % (tk, d))
    if still:
        print('\nknowingly outstanding, allowed for now (%d):' % len(still))
        for tk, d in still:
            print('   %-12s %s' % (tk, d))
    if hard:
        print('\nFAIL — a second generator nobody declared (%d):' % len(hard))
        for tk, d in hard:
            print('   %-12s %s' % (tk, d))

    now_passing = sorted(known - {t for t, _ in still})
    if now_passing:
        print('\nNOW DECLARED — remove from the list (%d): %s'
              % (len(now_passing), ', '.join(now_passing)))
    if prune:
        json.dump({'rule': 'R-ENF-01 / a numbers file with two generators declares their order',
                   'outstanding': sorted({t for t, _ in still})},
                  open(OUTSTANDING, 'w'), indent=1)
        print('\npruned — now %d entries' % len({t for t, _ in still}))
        return 0
    if hard:
        return 1
    print('\nOK — no new violations.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
