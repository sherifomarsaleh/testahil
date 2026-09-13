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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from build_all_shared import run                                    # noqa: E402

# MOVED TO THE SHARED RUNNER 13-09-2026. This study kept its own copy of the loop, so it
# did not write the BUILD MANIFEST the artefact-freshness gate reads -- and a figure that
# regenerates byte-identically is never re-committed, so three of this study's figures
# read as stale immediately after a full rebuild that produced them. Two runners is the
# defect this repository keeps finding under other names.

STEPS = [
    ("wacc.py", "wacc.json", "the cost-of-capital schedule the model discounts on"),
    ("peers.py", "peers.json", "reads the committed price libraries; goes stale by the "
                               "calendar, so it runs every time"),
    ("valuation.py", "valuation.json", "the four cases"),
    ("lenses.py", "lenses.json", "the cross-checks, the sensitivity grid and the reverse "
                                 "read — all read by build_numbers"),
    ("build_numbers.py", "study_numbers.json", "the one file every builder reads"),
    # APPENDS TO study_numbers.json, SO IT MUST FOLLOW build_numbers AND NOT PRECEDE IT.
    # build_numbers rebuilds that file from scratch; an appended record written before it
    # is silently reverted and the tree is left byte-identical to HEAD, which reads like
    # nothing was done rather than like something was lost. That is the defect this whole
    # file exists for, and it applies to the asset-base record like any other append.
    ("asset_base_record.py", "study_numbers.json (asset_base_record)",
     "[R-ASSET-01] the land bank's vintage against the information set that read it"),
    ("reverse.py", "diagnostics.json", "[R-ENF-05] reverse read, outside the numbers file"),
    ("contested.py", "contested_judgements.json", "[R-ENF-05] sign-test record"),
    ("experts.py", "experts.json", "the panel; its cross-examination quotes the reverse "
                                   "read, so it must follow build_numbers"),
    ("figures.py", "*.png", "every figure, from the committed numbers"),
    ("docx_tmgh.py", "the study", "the delivered document"),
    ("docx_bibliography.py", "the sources", "the standalone bibliography"),
    # THE PDFs ARE THE FILES A READER OPENS. The old private runner rendered them only
    # when someone remembered --pdf, and its glob never covered the workbook at all, so
    # the model PDF was a whole edition behind the spreadsheet it is named for. Declared
    # steps now: they run every time, in order, after what they render.
    ("bake_docs_pdf.py", "the study and sources PDFs",
     "rendered FROM those documents, so it follows them"),
    ("build_xlsx_tmgh.py", "the workbook", "the delivered model"),
    ("bake_model_pdf.py", "the workbook PDF",
     "rendered FROM the workbook, so it follows it"),
    ("recalc.py", "recalc_result.json", "an independent recalculation of that workbook"),
    ("prose_check.py", None, "every figure in prose reconciled against the model"),
    ("footing_check.py", None, "every total reproducible from the rows printed above it"),
    ("gate_check.py", None, "SIGCM and the model-report standard"),
]


if __name__ == '__main__':
    raise SystemExit(run(HERE, STEPS))
