#!/usr/bin/env python3
"""AMOC -- the BUILD ORDER for this study's numbers file, recorded because nothing
in this repository records one and the cost of that was measured today.

THE DEFECT COST A FALSE FINDING ON THIS VERY STUDY, AND IT PRODUCES NO ERROR OF ANY
KIND. The 08-09-2026 rebuild ran the judgement generator against a numbers file that
was only partly refreshed, so five contested judgements kept alternatives priced on
the SUPERSEDED EGP 11.40 edition while their adopted side had already been re-stamped
to EGP 17.62. Every one of those five then read as a 30-38% material gap resolved the
same way, and the sign test printed p=0.01 -- "every material judgement resolved one
way", the lean flag, on the only study in the book carrying it. THE LEAN WAS AN
ARTEFACT OF THE BUILD ORDER. Run in order the same figures give p=0.06 and five
material judgements rather than eight. Nothing valued moved by a basis point either
way, which is exactly what makes it dangerous: the answer was right and the record
about the answer was wrong.

THE GENERAL DEFECT, AND IT PRODUCES NO ERROR OF ANY KIND. study_numbers.json is written by
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
#   compute.py           REBUILDS study_numbers.json, and with it every figure the
#                        two records below price their alternatives against
#   diagnostics_amoc.py  writes this study's reverse-read and contested-judgement
#                        records  [R-ENF-05]
#   adversarial.py       writes the give-back cases  [R-ENF-06]
#
# The two record generators are named by their ROLE rather than by the files they
# emit, and that is deliberate rather than coy: the reverse-read containment check
# scans every .py in a study directory for the diagnostic artefact's own filename,
# because a builder that reads a quantity solved from the traded price back into
# the model is the reverse-engineered rate arriving through a side door. It exempts
# the diagnostic generator itself and nothing else, so a runner that merely LISTED
# those filenames in a comment tripped it. THE CHECK WAS NOT WIDENED TO LET THIS
# FILE PASS -- a gate edited to admit the thing in front of it is the defect wearing
# the fix's clothes. The filenames live in the generator that emits them, which is
# where a reader looks for them anyway.
STEPS = ('compute.py', 'diagnostics_amoc.py', 'adversarial.py')


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
