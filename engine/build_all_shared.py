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


def run(here, steps, argv=None):
    """Run `steps` from directory `here`. Returns a process exit code.

    A MISSING SCRIPT IS A FAILURE, NEVER A SKIP. A declared step that is not on disk means
    the order describes a study that no longer exists, and continuing past it would report
    a clean build of something else [R-ENF-04].
    """
    argv = sys.argv[1:] if argv is None else argv
    if '--list' in argv:
        print('%d declared steps, in order:' % len(steps))
        for i, (script, writes, why) in enumerate(steps, 1):
            print('  %2d  %-26s -> %-34s %s'
                  % (i, script, writes or '(checks only)', why))
        return 0

    only = [a for a in argv if not a.startswith('-')]
    unknown = [a for a in only if a not in {s for s, _, _ in steps}]
    if unknown:
        print('not a declared step of this study: %s' % ', '.join(unknown))
        print('run with --list to see the order')
        return 2

    fails, ran = [], 0
    for script, writes, why in steps:
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
