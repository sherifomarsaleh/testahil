#!/usr/bin/env python3
"""TMGH -- the BUILD ORDER for this study's numbers file, recorded because nothing
in this repository records one and the cost of that was measured today.

THE DEFECT COST A NEAR-MISS ON THIS STUDY. These three scripts pass their work through
FILES, not through imports: valuation.py reads wacc.json, and build_numbers.py reads
valuation.json. So running build_numbers.py after wacc.py -- which looks like a rebuild
and prints like one -- refreshes the committed cost-of-capital RECORD while leaving the
valuation cases untouched, and the study then publishes an answer its own record says
was discounted at a rate the answer never saw. That happened on 08-09-2026 while adding
a provenance field: the beta and the cost of capital moved, the central did not, and the
only reason it did not ship is that the two were compared afterwards. THE FIX IS THE
ORDER, and the order is only visible from outside the scripts.

THE FIX IS THE ORDER, MADE EXPLICIT AND EXECUTABLE. Each record generator reads
study_numbers.json and runs nothing, so the only thing that can go wrong is sequence,
and sequence is what this file is. Run this rather than the pieces:

    python3 build_records.py

THE GENERAL FORM, WHICH IS NOT ABOUT THIS STUDY: WHERE SEVERAL GENERATORS WRITE ONE
ARTEFACT, THE ORDER IS PART OF THE ARTEFACT. A generator that rebuilds a file from
scratch and a generator that appends to it are not interchangeable steps, and nothing
in the file itself can say which ran last.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ORDER MATTERS AND IS THE WHOLE POINT OF THIS FILE.
#   wacc.py           re-runs the beta regression and writes wacc.json, which holds
#                     the cost-of-capital SCHEDULE the valuation discounts on
#   valuation.py      reads wacc.json and writes valuation.json — the cases
#   build_numbers.py  reads BOTH and writes study_numbers.json
STEPS = ('wacc.py', 'valuation.py', 'build_numbers.py')


def main():
    for i, step in enumerate(STEPS, 1):
        print('=== %d/%d  %s' % (i, len(STEPS), step))
        r = subprocess.run([sys.executable, os.path.join(HERE, step)],
                           cwd=HERE, capture_output=True, text=True)
        tail = [l for l in (r.stdout or '').splitlines() if l.strip()][-6:]
        for l in tail:
            print('    ' + l)
        if r.returncode != 0:
            sys.stderr.write(r.stderr or '')
            print('FAILED at %s -- the numbers file is now in whatever state that step left '
                  'it, so re-run this file from the top rather than resuming in the middle.'
                  % step)
            return r.returncode
    print('every step ran in order; study_numbers.json carries every record')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
