"""Run a study's build steps in its DECLARED order, and refuse to guess that order.

WHY THIS EXISTS, AND IT IS NOT A CONVENIENCE. Measured on 13-09-2026, 23 of 25 studies had
no single build entry point, so reissuing one was a remembered sequence of six or seven
commands. Seven studies were then audited from outside, and the largest defect class in
every one of them was a step somebody forgot: AMOC shipped four of five figures at EGP
11.40 beside tables at 20.05, ARCC shipped four at 66.53 against a published 77.18, SCEM
shipped nine at 111.62 against 122.67, and both ARCC and TMGH shipped a workbook PDF older
than the workbook it was rendered from.

PHDC's own build_all.py had already written the argument down, in the edition before this
one, and it was never propagated:

    "The lesson is not 'remember harder' but that a step which rebuilds the numbers file
     indirectly is as much a rebuilder as one that does it in its own code, and only a
     declared order can hold that."

THE ORDER IS DECLARED PER STUDY AND IS NOT DISCOVERED HERE. It cannot be: the ordering
constraint is about what each step does to study_numbers.json, and that is invisible from
the filename. Anything writing an INPUT comes before the builder that reads it; anything
APPENDING to the numbers file comes after everything that REBUILDS it, or the append is
silently reverted and the tree is left byte-identical to the state before it ran -- an
absent answer in a clean answer's clothes [R-ENF-04]. AMOC found the worst version of
this: adversarial.py calls runpy.run_path on compute.py to get a clean record to perturb,
so it rebuilds the numbers file as a SIDE EFFECT of a step whose own code never mentions
doing so.

So each study keeps its own build_all.py holding a STEPS list, three fields to a row --
the script, what it writes, and why it sits where it does -- and calls run() here. This
file is the runner they share; it is not the order.

    python3 build_all.py                 every step, in order
    python3 build_all.py compute.py      one step, for iterating
    python3 build_all.py --list          the declared order, run nothing
"""
import os
import subprocess
import sys


REBUILD_ONLY = ("TWO DIFFERENT OPERATIONS WEAR THE SAME NAME, and conflating them moved a\n"
                "published answer. See run().")


def run(here, steps, argv=None):
    """Run `steps` from directory `here`. Returns a process exit code.

    A MISSING SCRIPT IS A FAILURE, NEVER A SKIP. A declared step that is not on disk means
    the order describes a study that no longer exists, and continuing past it would report
    a clean build of something else [R-ENF-04].
    """
    # REBUILDING A STUDY AND RE-STRIKING IT ARE TWO DIFFERENT OPERATIONS, and this file
    # conflated them on its first day [corrected 13-09-2026]. Rebuilding ARCC end to end
    # moved its published central from EGP 77.1781 to 77.1858 and the fair-value register
    # caught it in CI. Nothing was wrong with the arithmetic: step0.py refreshes the local
    # price history from the repository library, beta_reg.py then regresses on a slightly
    # longer series, beta went 0.928 -> 0.927, and the answer followed.
    #
    # THAT IS A NEW EDITION, NOT A REBUILD. An edition is a fixed thing in this book --
    # edition.py exists to say so -- and rebuilding the 10-09-2026 edition must reproduce
    # the number 10-09-2026 published, or the edition is not reproducible and every
    # comparison against it is against a moving target. Re-deriving inputs from today's
    # data is a legitimate and separate act which produces a new answer that must be
    # registered.
    #
    # So the steps that RE-DERIVE AN INPUT are marked, and they run only when asked.
    # Default: rebuild every artefact from the committed inputs, which is what the stale
    # figures and stale PDFs needed. --restrike: re-derive the inputs too, and expect the
    # answer to move.
    argv = sys.argv[1:] if argv is None else argv
    restrike = '--restrike' in argv
    steps = [(s_[0], s_[1], s_[2], (len(s_) > 3 and s_[3])) for s_ in steps]
    if not restrike:
        skipped = [s_[0] for s_ in steps if s_[3]]
        steps = [s_ for s_ in steps if not s_[3]]
        if skipped:
            print('rebuilding from the COMMITTED inputs; %d input-deriving step(s) held '
                  'back: %s' % (len(skipped), ', '.join(skipped)))
            print('   pass --restrike to re-derive them, which makes a NEW EDITION whose '
                  'answer must be registered.\n')
    if '--list' in argv:
        print('%d declared steps, in order:' % len(steps))
        for i, (script, writes, why, rs) in enumerate(steps, 1):
            print('  %2d  %-26s -> %-34s %s%s'
                  % (i, script, writes or '(checks only)', why,
                     '   [re-derives an input]' if rs else ''))
        return 0

    only = [a for a in argv if not a.startswith('-')]
    unknown = [a for a in only if a not in {s_[0] for s_ in steps}]
    if unknown:
        print('not a declared step of this study: %s' % ', '.join(unknown))
        print('run with --list to see the order')
        return 2

    fails, ran = [], 0
    for script, writes, why, _rs in steps:
        if only and script not in only:
            continue
        path = os.path.join(here, script)
        if not os.path.exists(path):
            print('%-26s MISSING — %s' % (script, why))
            fails.append(script)
            continue
        r = subprocess.run([sys.executable, path], cwd=here,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode('utf-8', 'replace').strip().splitlines()
        print('%-26s %s' % (script, out[-1][:110] if out else ''))
        ran += 1
        if r.returncode != 0:
            fails.append(script)
            for line in out[-12:]:
                print('     %s' % line[:150])
            # STOP AT THE FIRST FAILURE. Every later step reads what this one writes, so
            # continuing produces a cascade of failures with one cause and buries it.
            print('\nSTOPPED at %s — later steps read what it writes.' % script)
            break

    print()
    if fails:
        print('FAILED: %s' % ', '.join(fails))
        return 1
    print('all %d step(s) clean' % ran)
    return 0
