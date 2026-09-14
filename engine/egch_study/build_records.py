#!/usr/bin/env python3
"""EGCH -- the BUILD ORDER for this study's numbers file, recorded because nothing
in this repository records one and the cost of that was measured today.

THE DEFECT, AND IT PRODUCES NO ERROR OF ANY KIND. study_numbers.json is written by
more than one generator: compute.py REBUILDS it from scratch, and forecast_anchor.py,
bridge_record.py and coc_record.py each ADD one record to whatever is already there.
compute.py therefore silently reverts every record added after it. Running the anchor
generator and then compute.py leaves the working tree BYTE-IDENTICAL TO HEAD, which
reads like nothing was done rather than like something was lost -- an absent answer in
a clean answer's clothes [R-ENF-04], arriving through a build order nobody had written
down. It happened in this pass, to the person writing these generators, within an hour
of adding the first one.

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
#   compute.py             REBUILDS study_numbers.json from the input register
#   lenses.py              adds the lens, macro and bridge records and the two-sided
#                          answer  [R-LENS-03, R-MACRO-01, R-BRIDGE-01]
#   asset_base_record.py   adds `asset_base_record` + `information_set_ends`
#                          [R-ASSET-01]
#   coc_record.py          adds `cost_of_capital_record`   [R-COC-01]
STEPS = ('compute.py', 'lenses.py', 'asset_base_record.py', 'coc_record.py')


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
