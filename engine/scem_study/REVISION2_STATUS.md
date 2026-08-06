# SCEM revision 2 — IN PROGRESS. Do not deliver the workbook in this state.

## Deliverable status

| Artefact | State |
|---|---|
| `compute.py` (revision 2) | **COMPLETE and passing.** All ASSERTs green. |
| `compute_bu.py` (bottom-up cost stack) | **COMPLETE.** Validation passes. |
| `SCEM_Valuation_Model_06082026_public.xlsx` (this directory) | **MID-MIGRATION — NOT DELIVERABLE.** 739 formula cells, 2 unresolvable, **257 disagreements** against the model. |
| `files/SCEM_Valuation_Model_06082026_public.xlsx` | Untouched revision 1. Internally consistent, but carries the defects the critique found. |
| `files/SCEM_Valuation_Study_...docx` | Untouched revision 1. Narrates 62.81; the model now says 53.12. |
| `files/SCEM_Bibliography_...docx` | Untouched revision 1. |

**Nothing in `files/` has been overwritten.** The revision-1 set remains internally
consistent — study, model and bibliography all agree with each other, even though the
numbers are now known to be wrong. That is deliberate: a self-consistent old set is safer
to hold than a half-migrated new one.

## What revision 2 establishes

EBITDA is an OUTPUT of a physical cost stack, not an asserted margin:

    kiln clinker capacity x utilisation -> clinker
    clinker / OBSERVED clinker factor (2.57/3.80 = 0.676) -> cement
    cement x domestic/export split x price by channel -> revenue
    thermal energy, fuel, power, tariff, raw materials, packaging,
      distribution, fixed cost per tonne of CAPACITY -> cost
    revenue - variable - fixed -> EBITDA

The validation CAN fail, unlike the identity it replaces (revision 1 solved price as
revenue / volume, so its residual was zero for any assumption):

  * bottom-up revenue within **+0.01%** of disclosed
  * cost stack within **+1.36%** of EBITDA derived from disclosed profit at the
    EFFECTIVE 32% tax rate on the REPORTED cash balance

Headline effect: central **62.81 -> 53.12**, DCF lens **54.49 -> 43.81**, gap to spot
**-20.5% -> -32.8%**, TV share **41% -> 49%**. FY2026E margin was an INPUT of 30.5%,
set above the very year the study called a cyclical peak; it is now an OUTPUT of 30.1%
falling to 26.4%.

A defect found in my own correction and fixed: the first stub formula produced a year-1
discount factor of **1.0209** — above 1.0, i.e. future money worth more than today's.
The 7 elapsed months of FY2026 now roll into opening cash rather than being lost.

## Remaining work — mechanical, not conceptual

1. Repoint `Income Statement`, `Balance Sheet`, `Cash Flow` and `Per-Share & Ratios` at
   the revision-2 chain. `Income Statement!B5` currently returns 0.88 where it should
   return 4,280 — a plain row-reference error.
2. Clear 2 divide-by-zero cells (`Per-Share & Ratios!H11:I11`).
3. Drive recalc to "N of N reproduce, 0 unresolvable, 0 unchecked".
4. Re-run the driver test; re-price the terminal-growth and net-cash expectations.
5. Save with cached values (critique P29 / row 29).
6. Rebuild the Word narrative around the bottom-up build and the corrected conclusion,
   and the bibliography around the revision-2 input register.
7. Re-run the full QC gate (a)-(r) and report before/after.

## Two decisions still open

* Asset-lens weight: 8% applied as the default; 15% adds ~3.6%, zero subtracts ~2.6%.
* Terminal risk-free rate: 12.5% applied (CBE's OPERATIVE 7% target + ~5.5pp real);
  reverting to 10.5% adds ~1.8%. Terminal growth held at 5%.

Both are flagged in the `compute.py` input register as REVIEWABLE CHOICE.
