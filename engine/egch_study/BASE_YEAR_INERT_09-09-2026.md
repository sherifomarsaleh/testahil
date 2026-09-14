# EGCH — the base year is inert, and the study presents it as carrying the model

**09-09-2026 · internal · nothing published · no number changed**

## Measured, not argued

`q4_runrate_haircut` is the haircut applied to the third quarter's revenue to run-rate the
unreported fourth quarter into the base year `fy2526`. Moved across its whole range and
the study re-run end to end each time:

| Q4 run-rate haircut | per share |
|---|---:|
| 1.00 — no haircut at all | 4.0395808164915605 |
| **0.97 — adopted** | **4.0395808164915605** |
| 0.85 | 4.0395808164915605 |
| 0.50 — halve the quarter | 4.0395808164915605 |

**Identical to sixteen decimal places.** Halving the final quarter of the base year does
not move the answer by one part in a quadrillion.

## Why: it reaches the page and nothing else

`fy2526` is built at `compute.py:428-443` and committed at `:887`. Grepping every module
that reads it:

    build_xlsx.py:43   HIS = D['hist']; F25S = D['fy2526']
    docx_egch.py:29    H, F25 = DD['hist'], DD['fy2526']

Both are **document builders**. It never enters `build()`, `terminal()` or `bridge()`. The
forecast is constructed from drivers — volumes, prices, the gas cost, the capital
programme — and it does not open from the base year at all.

## What is wrong is the presentation, not the construction

A trailing-year estimate is worth showing a reader. What is not defensible is presenting it
as load-bearing. The delivered document and heading 2 of `GAP_REVIEW_05-09-2026.md` both
discuss the run-rate and its haircut in the register a driver belongs in — *"the fourth
quarter run-rated on the third quarter's revenue with a disclosed haircut for the summer
gas curtailment"* — with nothing saying that the haircut is worth zero.

## The general form, which is not about EGCH

**A study can present a construction as load-bearing when it only reaches the page, and
every existing check will pass.** `prose_check.py` already tracks "register inputs consumed
by a builder: 272 of 304" — and consumption by a DOCUMENT builder counts as consumption.
It cannot distinguish *feeds the valuation* from *gets printed*, so a figure that drives
nothing but appears in a table is indistinguishable from one that drives everything.

That distinction is worth having across the book and is the thing to build next: split the
consumption count into **inputs the model reads** and **inputs only a document reads**, and
require the second class to be presented as disclosure rather than as a driver. It is not
built here because it is a book-wide instrument and this is one name's finding; building it
on one example is how a check ends up fitting one study.

## What is owed on EGCH specifically

Either wire the base year into the model — if there is a correct place for it, and there
may not be, since the forecast is driver-built by design — or say plainly in the document
that `fy2526` is a DISCLOSURE of the trailing year and not an input to the valuation.
The second is almost certainly right and it costs the answer nothing.

**Neither is done in this pass.** The finding is measured and recorded; changing how a
delivered document describes its own base year is a re-issue, and the study is already
carrying two larger open items — the export duty re-tiered tonight and the CWIP write-off
asymmetry between its branches.
