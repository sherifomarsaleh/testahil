#!/usr/bin/env python3
"""[R-ENF-01] NO CHECK MODIFIES THE TREE IT CHECKS.

ADOPTED 07-09-2026 ON A COMMITTED LOSS. check_escalations_negative_control.py wrote
its fixture into the REAL engine/escalations.json and copied a backup over it in a
`finally`. A `finally` survives an exception and does not survive a kill, a timeout,
or the machine going away — and on 07-09-2026 one did not run, so THIRTEEN LIVE
ESCALATIONS WERE REPLACED BY A SINGLE FIXTURE CALLED NC-example AND COMMITTED. The
register is the artefact [R-IND-01] adopted so a question is never asked twice; the
control that existed to protect it is what destroyed it.

WHY NOTHING SAW IT is the part worth keeping. Every gate here reads the tree and
reports on what it finds, so a gate reading a file some earlier step had rewritten
reports faithfully on the rewritten file. The damage was not a wrong answer anywhere
— it was the SUBJECT being replaced between the write and the read, which no
instrument inspecting content can distinguish from the content having always been
that. What catches it is not another reader but the question no reader asks: DID
RUNNING THE CHECKS CHANGE ANYTHING?

THE INSTANCE WAS CLOSED AT ITS MECHANISM (the gate now reads
TESTAHIL_ESCALATIONS_REGISTER, so the control points the reader at a temp file and
the real one is never opened for writing, and the control asserts byte-identity on
every case). THIS CLOSES THE CLASS, per [R-ENF-01]: when a defect of this species is
found again, close the class rather than the instance. A sweep of all forty-odd
negative controls found every other one copying FROM the real tree INTO a tempdir,
which is correct — but that is a fact about today, checked by a person reading, and
this rule exists so it stays a fact without anyone reading again.

WHAT IT CHECKS AND WHAT IT DELIBERATELY DOES NOT. It refuses a TRACKED file that is
modified or deleted. It says nothing about UNTRACKED files: a gate that renders a
document, writes a scratch panel or leaves a build artefact has changed nothing that
was committed, and refusing that would be a claim about tidiness rather than about
the record. The damage class is a committed artefact being silently rewritten.

IT IS A POSITION IN THE RUN RATHER THAN A CHECK ON A FILE, so it comes in two
halves: --record writes the tracked-file state BEFORE the checks, and the default
compares against it after. THE QUESTION IS "DID ANYTHING CHANGE WHILE THE CHECKS
RAN", NOT "IS THE TREE DIRTY" — and the difference is not pedantry. A local
pre-commit run always has uncommitted edits, so a gate keyed on dirtiness would be
red every time anybody ran it, which is the permanently-red check [R-ENF-02] forbids
and the surest way to make a real leak invisible. CI checks out clean, so there the
two questions coincide; the operator's own tree is where they do not, and that is
exactly where this has to keep working.

A MISSING BASELINE IS A FAILURE, NEVER A SKIP [R-ENF-04]: comparing against nothing
is the absent answer wearing a clean one's clothes, and it is the state this gate
enters if the recording step is ever dropped from the workflow.

WHAT IT CANNOT DISTINGUISH, STATED RATHER THAN DISCOVERED LATER: a file written by a
CHECK and a file written by the OPERATOR while the checks were running look identical
to it, because both are simply a tracked file that changed between the record and the
comparison. In CI that gap is empty by construction — nobody edits a runner's
checkout mid-job — so there the gate means exactly what it says. Locally it means
DO NOT EDIT THE TREE WHILE THE SUITE IS RUNNING, and a red result there is read as
that first and as a leaking check second. Narrowing it further would need the gate to
know which process wrote a file, which git does not record and no amount of care here
can supply.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BASELINE = os.path.join(
    os.environ.get('TESTAHIL_TREE_BASELINE_DIR') or '/tmp', 'testahil_tree_baseline.txt')


def git(*a):
    r = subprocess.run(('git',) + a, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def tracked_state():
    """The modified/deleted TRACKED files, one per line. Untracked is not the subject."""
    rc, out, err = git('rev-parse', '--is-inside-work-tree')
    if rc != 0:
        raise RuntimeError('not a git work tree: %s' % err.strip()[:160])
    rc, out, err = git('status', '--porcelain', '-uno')
    if rc != 0:
        raise RuntimeError('git status did not run: %s' % err.strip()[:160])
    return sorted(ln for ln in out.splitlines() if ln.strip())


def main(argv):
    baseline = DEFAULT_BASELINE
    if '--baseline' in argv:
        baseline = argv[argv.index('--baseline') + 1]
    record = '--record' in argv

    print('TREE-UNMODIFIED GATE  [R-ENF-01]')
    try:
        state = tracked_state()
    except RuntimeError as exc:
        print('\nFAIL — the question this gate asks cannot be answered: %s. '
              'An unanswerable check is not a clean one [R-ENF-04].' % exc)
        return 1

    if record:
        with open(baseline, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(state) + ('\n' if state else ''))
        print('   baseline recorded: %d tracked file(s) already modified before the '
              'checks ran -> %s' % (len(state), baseline))
        return 0

    if not os.path.exists(baseline):
        print('\nFAIL — no baseline at %s, so there is nothing to compare against. '
              'Comparing against nothing is an absent answer wearing the costume of a '
              'clean one [R-ENF-04]: the --record step is missing from the run.'
              % baseline)
        return 1

    before = sorted(ln for ln in
                    open(baseline, encoding='utf-8').read().splitlines() if ln.strip())
    rc2, head, _ = git('rev-parse', '--short', 'HEAD')
    appeared = [ln for ln in state if ln not in before]
    vanished = [ln for ln in before if ln not in state]

    print('   no check modifies the tree it checks — tracked files only, at %s'
          % (head.strip() or 'an unknown head'))
    print('   %d tracked file(s) modified before the run, %d after'
          % (len(before), len(state)))

    if not appeared and not vanished:
        print('\nOK — every check that ran left the committed tree exactly as it '
              'found it.')
        return 0

    print('\nFAIL — the tracked tree changed WHILE the checks ran:')
    for ln in appeared[:40]:
        print('  appeared  ' + ln)
    for ln in vanished[:40]:
        print('  reverted  ' + ln)
    print('\nA check writes to a SANDBOX, never to the tree. Where a checker needs '
          'different inputs, give it different inputs — never the real ones and a plan '
          'to put them back, because the putting back is the part that does not run on '
          'the one occasion the state mattered.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
