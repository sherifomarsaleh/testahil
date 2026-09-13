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

## THE GENERAL LESSON — AND A CORRECTION TO THIS DOCUMENT'S FIRST DRAFT

**The first draft of this file said the publish queue "does NOT check that the workbook
reproduces the study", and that this was "how a file publishing a superseded answer
reached the staging set with every gate green". BOTH HALVES WERE WRONG, and the error was
mine.**

`scripts/check_workbook_values.py` exists and does exactly that, by running each study's
own recalculation rather than noting that it has one. **It caught this.** And the ratchet
entry it wrote on 8 September 2026 names the root cause more precisely than my own first
diagnosis did, a week before I looked:

> DCF!C33 builds gross profit as revenue less cost plus a flat margin shift, and
> reproduces a gross margin of 9.68% in year one where the model applies 12.43%.
> Everything upstream agrees — revenue, cost of sales, the base-year margin, the segment
> foot, the whole income statement — and everything downstream of row 33 inherits the gap.

So nothing here was green and nothing was undetected. The file staged because the failure
was a RATCHETED entry — an acknowledged, measured debt — and a ratcheted failure does not
block staging. That is the mechanism working as designed, not a hole in it.

**What that changes about the lesson.** It is not "the queue needs a check". It is
narrower and more useful: a workbook carrying a *measured, named, quantified* 35%
disagreement with its own study sat on the ratchet for five days while the study went on
being staged for publication. The ratchet is right that a known debt should not stop
everything else moving. But a delivered artefact that publishes a different answer from
the document beside it is not the same class of debt as a missing recalculator or a
thin coverage row — a reader who opens both gets two numbers and no way to tell which
is the study's. Whether that class should be able to sit on the ratchet at all is a real
question and it is left open here rather than decided in a study directory.

The entry is now retired, because the defect is fixed rather than re-argued. A ratchet may
only ever shorten, and this shortens it.
