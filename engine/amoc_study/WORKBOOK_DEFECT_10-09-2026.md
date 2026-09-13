# AMOC — the delivered workbook published a superseded answer. Found and repaired.

**Found 10 September 2026, repaired 13 September 2026.** Kept because the failure mode is
general and the repair is one line in each of two generators.

## What the reader was handed

The study published **EGP 20.05** a share. The workbook beside it recalculated to
**EGP 12.85**. 1,867 of 6,069 formula cells disagreed with the model's own registered
values.

EGP 12.85 is not a random number. It is `dcf.ps_ttm_base_superseded` — the study's own
name for **the base the study explicitly superseded**: the twelve-month blend at a 9.653%
gross margin, replaced by the reviewed half to 30-Jun-2026 at 12.428%. The workbook was
still running the old base and reproducing it faithfully to six decimal places.

## Why nothing caught it

The base-period correction is carried in `compute.py` as a gross-margin shift laid on top
of the eight per-line unit builds (`ADOPTED_GM_SHIFT`, 2.744 points). The workbook's
forecast engine reads that shift from ONE cell, `DCF!B7`, and the builder typed `0.0` into
it under a label reading "the base case sets them all neutral". The base case is not
neutral on that row, and had not been since the correction was adopted.

Everything downstream then agreed with itself. Revenue was right. The cost of capital
reproduced exactly (0.27439). The discount factors matched to three decimals. The footing
tests passed, the per-line allocation footed to the pound, the gross-margin reconciliation
passed — because it checks the BASE year, which is the twelve-month blend in both places.
The divergence opened at the first forecast year and ran through EBIT (2,949 against
4,407), NOPAT, free cash flow and the present value. **Every one of those 1,867 cells was
internally consistent with the wrong opening margin**, which is why a checker looking for
incoherence found none.

The second copy of the same defect: the sensitivity grid wrote the INCREMENT into its
margin lever (`-1.0% … +1.0%`) while running `ADOPTED_GM_SHIFT + increment` in the model,
so all five margin blocks were short by the same 2.744 points.

## The repair — in the generators, both of them

- `compute.py` now EXPORTS `dcf.adopted_gm_shift`. The builder reads
  `study_numbers.json` and nothing else by design, so a number it cannot see is a number
  it silently gets wrong.
- `compute.py`'s margin grid writes the lever the model actually ran, not the increment.
  The label stays the increment, because that is what a reader of a sensitivity grid is
  being offered.
- `build_xlsx_v5.py` puts `DCF['adopted_gm_shift']` in `DCF!B7` and relabels row 5.

Nothing was hand-edited in the workbook and no fair value moved: the study published
EGP 20.0503 before the repair and EGP 20.0503 after it. `recalc_v5.py` goes from
1,870 problems to **PASS**, 0 disagreements across all 6,069 formula cells.

## THE GENERAL LESSON, which is about the publish queue

The queue checks a study's fair values against the manifest. It does NOT check that the
workbook beside the study reproduces the study. That is how a file publishing a superseded
answer reached the staging set with every gate green. A workbook is a delivered artefact
and it carries its own copy of the model; the copy has to be checked against the original,
not assumed from the fact that both were built in the same pass.
