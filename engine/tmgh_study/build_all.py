#!/usr/bin/env python3
"""TMGH — build every artefact and document, in dependency order, in one command.

WHY THIS EXISTS. This study is built by eleven scripts that must run in the right order,
and nothing enforced either the set or the order. In a single afternoon that produced four
separate stale artefacts, each in the same shape: a generator was corrected, the file it
writes was not regenerated, and a delivered document went on printing the old answer.
statements.json was two days behind the model; peers.json was five weeks behind this
repository's own price libraries; experts.json quoted a reverse read that had moved; and
the sensitivity note added to experts.py did not reach the page because the script that
writes its file was not re-run after the edit.

None of those was carelessness about a number. Each was the ordinary consequence of a
pipeline whose steps a person has to remember, and the fix for that is not to remember
harder. [R-ENF-06]'s general lesson is that an artefact every builder reads and nothing
writes is a memory; the companion is that an artefact SOMETHING writes, when nothing makes
it run, is a memory too.

THE ORDER IS THE DEPENDENCY ORDER AND IT IS DECLARED, NOT IMPLIED. Anything reading
study_numbers.json comes after build_numbers; anything reading lenses.json comes before it.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (script, what it writes, why it sits here)
STEPS = [
    ("wacc.py", "wacc.json", "the cost-of-capital schedule the model discounts on"),
    ("peers.py", "peers.json", "reads the committed price libraries; goes stale by the "
                               "calendar, so it runs every time"),
    ("valuation.py", "valuation.json", "the four cases"),
    ("lenses.py", "lenses.json", "the cross-checks, the sensitivity grid and the reverse "
                                 "read — all read by build_numbers"),
    ("build_numbers.py", "study_numbers.json", "the one file every builder reads"),
    ("reverse.py", "diagnostics.json", "[R-ENF-05] reverse read, outside the numbers file"),
    ("contested.py", "contested_judgements.json", "[R-ENF-05] sign-test record"),
    ("experts.py", "experts.json", "the panel; its cross-examination quotes the reverse "
                                   "read, so it must follow build_numbers"),
    ("figures.py", "*.png", "every figure, from the committed numbers"),
    ("docx_tmgh.py", "the study", "the delivered document"),
    ("docx_bibliography.py", "the sources", "the standalone bibliography"),
    ("build_xlsx_tmgh.py", "the workbook", "the delivered model"),
    ("recalc.py", "recalc_result.json", "an independent recalculation of that workbook"),
    ("prose_check.py", None, "every figure in prose reconciled against the model"),
    ("footing_check.py", None, "every total reproducible from the rows printed above it"),
    ("gate_check.py", None, "SIGCM and the model-report standard"),
]


def main():
    pdf = "--pdf" in sys.argv
    for script, writes, why in STEPS:
        p = os.path.join(HERE, script)
        if not os.path.exists(p):
            print("MISSING %s — %s" % (script, why))
            return 1
        r = subprocess.run([sys.executable, p], cwd=HERE, capture_output=True, text=True)
        tail = [l for l in (r.stdout or "").strip().splitlines() if l.strip()][-1:]
        print("%-24s %s" % (script, tail[0][:96] if tail else "ok"))
        if r.returncode:
            print((r.stdout or "") + (r.stderr or ""))
            print("\nSTOPPED at %s — %s" % (script, why))
            return 1
    if pdf:
        # THE PDF IS THE DELIVERABLE AND THE WORD FILE IS THE BUILD ARTEFACT. A document
        # rebuilt without its PDF ships the old page to the reader, which is the hole
        # check_edition_date's delivered-PDF clause was written to close.
        import glob
        for d in sorted(glob.glob(os.path.join(HERE, "TMGH_*.docx"))):
            if os.path.basename(d).startswith("~$"):
                continue
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                            "--outdir", HERE, d], capture_output=True, timeout=600)
            print("%-24s %s" % ("pdf", os.path.basename(d)[:-5] + ".pdf"))
    print("\nall %d steps clean%s" % (len(STEPS), "; PDFs rebuilt" if pdf else
                                      " (pass --pdf to rebuild the delivered PDFs)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
