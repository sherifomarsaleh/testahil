"""WHEN A PUBLISHED FAIR VALUE MOVES, EVERY RECORD OF IT MOVES WITH IT.

WHAT THIS EXISTS TO STOP, and it is a mistake I made twice in one evening.

Correcting a study is not one edit. The answer lives in the study's own committed
numbers, and it is ALSO recorded in the fair-value half of the calibration register and
staged in the publish queue's manifest. Fix the study, rebuild its documents, run its
local gates, push -- and CI goes red on a register nobody touched.

  09-09-2026, PHAR, twice:
    fv_movement       records [31.3738, 47.6035]   study publishes [31.2977, 47.5063]
    publish manifest  the same pair, a second time
    fv_movement       records [31.2977, 47.5063]   study publishes [88.5201, 106.6812]

Both times the study-local gates were green -- recalc, prose, footing, the gap gate --
because none of them reads those two files. Both times the checks that WOULD have caught
it exist and are in CI. The failure was choosing which gates to run by hand and picking
the ones that felt related to what I had changed.

SO THIS IS NOT A NEW CHECK. It runs the two that already exist, together, under one name
that says what they have in common, so a person correcting a study can ask ONE question
-- "does every record still agree with the answer?" -- instead of remembering two files.
The real answer is scripts/run_ci_gates.py, which runs CI's own list; this is the cheap
version for the specific thing that keeps breaking.

[R-ENF-01] reports; it never edits. Where a record disagrees, the fix is to APPEND an
edition to the register (it is append-only) and re-stage the queue, never to retype a
delivered number.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECKS = [
    (['python3', 'engine/fv_movement.py', 'check'],
     'the fair-value calibration register against every study it records'),
    (['python3', 'scripts/build_publish_queue.py', '--check'],
     "the publish queue's manifest against the studies it stages"),
]


def main():
    red = []
    for cmd, what in CHECKS:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        ok = r.returncode == 0
        print('  [%s] %s' % ('ok  ' if ok else 'RED ', what))
        if not ok:
            tail = (r.stdout + r.stderr).strip().splitlines()[-4:]
            red.append((what, tail))
    if red:
        print('\nRED — %d record(s) disagree with the answer the study publishes:' % len(red))
        for what, tail in red:
            print('  %s' % what)
            for line in tail:
                print('     ' + line[:200])
        print('\nAppend an edition to the register and re-stage the queue. Never retype a '
              'delivered number: the register is append-only precisely so a correction '
              'leaves the superseded figure visible beside the new one.')
        return 1
    print('\nOK — every record of a published fair value agrees with the study.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
