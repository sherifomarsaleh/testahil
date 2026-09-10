#!/usr/bin/env python3
"""PHDC -- build every artefact in dependency order, in one command.

WHY THIS EXISTS, AND IT IS NOT A CONVENIENCE. This study is built by several scripts that
must run in a particular order, and nothing recorded that order. The cost was measured on
09-09-2026: asset_base_record.py APPENDS the [R-ASSET-01] record to study_numbers.json and
build_numbers.py REBUILDS that file from scratch, so running the record and then anything
that rebuilds silently reverts it. The tree is left byte-identical to the state before the
record was written -- an absent answer in a clean answer's clothes [R-ENF-04] -- and the
gate goes on reporting "no asset_base_record committed" while a correct one has been
written twice.

THE SAME DEFECT HAS NOW BEEN FOUND ON THREE STUDIES IN ONE DAY, and on AMOC it survived a
build order that HAD been written down: adversarial.py calls runpy.run_path on compute.py
to get a clean record to perturb, so it rebuilds the numbers file as a SIDE EFFECT of a
step whose own code never mentions it. The lesson is not "remember harder" but that a step
which rebuilds the numbers file indirectly is as much a rebuilder as one that does it in
its own code, and only a declared order can hold that.

THE ORDER IS THE DEPENDENCY ORDER AND IT IS DECLARED, NOT IMPLIED. Anything writing an
input to build_numbers comes before it; anything APPENDING to study_numbers.json comes
after everything that rebuilds it, which is why the asset-base record is last.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (script, what it writes, why it sits here)
STEPS = [
    ("wacc.py", "wacc_result.json", "the cost-of-capital schedule the model discounts on"),
    ("peers.py", "peers.json", "reads the committed price libraries, so it goes stale by "
                               "the calendar and runs every time"),
    ("compute.py", "valuation.json", "the lenses and the cases"),
    ("bottom_up_model.py", "bottom_up_model.json", "the unit build build_numbers reads"),
    ("build_numbers.py", "study_numbers.json", "the one file every builder reads -- and it "
                                               "REBUILDS the file, so every append follows it"),
    ("diagnostics_phdc.py", "diagnostics.json", "the reverse read; it READS study_numbers "
                                                "and must follow build_numbers"),
    ("build_figures.py", "*.png", "every figure, from the committed numbers"),
    ("docx_phdc.py", "the study", "the delivered document"),
    ("docx_bibliography.py", "the sources", "the standalone bibliography"),
    ("build_xlsx_phdc.py", "the workbook", "the delivered model"),
    ("recalc.py", None, "an independent recalculation of that workbook"),
    ("prose_check.py", None, "every figure in prose reconciled against the model"),
    ("footing_check.py", None, "every total reproducible from the rows above it"),
    ("gate_check.py", None, "SIGCM and the model-report standard"),
    # LAST, AND THE REASON IS THE WHOLE POINT OF THIS FILE. It appends to
    # study_numbers.json; anything above that rebuilds the file would revert it.
    ("asset_base_record.py", "study_numbers.json (asset_base_record)",
     "[R-ASSET-01] the land bank's vintage against the information set that read it"),
]


def main():
    argv = sys.argv[1:]
    only = [a for a in argv if not a.startswith('-')]
    fails = []
    for i, (script, writes, why) in enumerate(STEPS, 1):
        if only and script not in only:
            continue
        path = os.path.join(HERE, script)
        if not os.path.exists(path):
            print('%-24s MISSING -- %s' % (script, why))
            fails.append(script)
            continue
        r = subprocess.run([sys.executable, path], cwd=HERE,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = r.stdout.decode('utf-8', 'replace').strip().splitlines()
        tail = out[-1][:110] if out else ''
        print('%-24s %s' % (script, tail))
        if r.returncode != 0:
            fails.append(script)
            for line in out[-12:]:
                print('    %s' % line[:150])
    print()
    if fails:
        print('FAILED: %s' % ', '.join(fails))
        return 1
    print('all %d steps clean' % len(STEPS))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
