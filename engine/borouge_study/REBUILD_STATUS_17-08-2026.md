# BOROUGE — rebuild in progress, 17 August 2026

## The three questions, answered honestly

**1. Did I take the critique seriously enough? NO.**
Audited programmatically: **66 of 106 findings were judged without a number in the price
column**, against my own rule that forbids exactly that. The two I called the sharpest
catches in the whole set I marked "structural"; one I labelled "material, unpriced" and
accepted anyway. Priced properly, two of them cross the 5% escalation threshold I had
promised would trigger full re-derivation:

| Finding | What I wrote | What it actually prices at |
|---|---|---|
| CC30 sales capped at nameplate | "material, unpriced" | **+6.2%** |
| CC7 the 2026 column | "structural" | −0.6% as a one-year miss; **−12.3%** as a level shift |
| CC25 feedstock floor | "structural" | −0.4% |
| CC29 B4 lease liabilities | "small negative" | −0.2% to −0.7% |
| GR1/GR2/GR10 | "—" (rejected, no price) | their error is worth **+0.137 AED** on their own answer |

**2. Was the model built bottom up? IN FORM, YES. IN SUBSTANCE, NOT WELL ENOUGH.**
It is volume × price and cost per tonne throughout. But the unit build had three basis
errors, and one of them I introduced while trying to fix another:
- the cost split was fitted on tonnes SOLD and applied to tonnes PRODUCED;
- my first fix — refit on production — returned a variable rate of **minus $856/tonne** on
  a $6,114m fixed leg, because production spans only 161kt across three audited years and
  a three-point regression cannot identify a slope from that. **A three-point regression
  was never capable of identifying this split at all.** Presenting it as "least squares
  across three audited years" was the deeper defect;
- the forecast conflates production and sales, discarding the disclosed partner-sourcing
  channel that makes sales exceed production.

**3. Is the Excel calculated with as little hard-coding as possible? NO.**
`Cash Flow!B7:D7 = B5*0+400.333` is a pasted number wearing a formula's clothes. It
inflates the 759 formula count and defeats my own recalc gate, which tests only whether a
cell begins with `=`. There are also six day-count literals inside Balance Sheet formulas,
two bare enterprise values in the DCF chain, a book-value-per-share literal and three
hard-coded returns on equity — none of them inside the three pasted classes READ FIRST
declares.

## What has been rebuilt so far

| Fix | Finding | Status |
|---|---|---|
| Cost split re-anchored to reproduce the AUDITED FY2025 cost at FY2025's own production; the variable rate now declared a judgement, not a fit | CW9 · CC1 · SA4 | **done** |
| Feedstock floored at the contracted ethane rate — the 2026 column previously implied an H2 rate of $204/t against a $256/t floor | CC25 | **done** |
| Borouge 4 perpetuity removed; the agreement ends at recontribution, "not anticipated before 2029" | CC2 · GR7 | **done** |
| Sourcing uplift measured from the audited record | CC30 | measured, **not yet applied** |

**Model before → after:** DCF (own beta, normalisation) **2.79 → 2.28 AED, −18.3%**.
Field **1.29 – 2.79, median 1.73** → **1.16 – 2.39, median 1.59**.

## What remains, and it is not small

1. Rebuild the 2026 column as H1 actual + an H2 built from restored availability, then
   re-derive 2027–30 from that base — the only way to settle whether CC7 is worth −0.6%
   or −12.3%.
2. Apply the sourcing uplift to sales (CC30, +6.2%).
3. Put Borouge 4 into all four lenses consistently (CW25 · CC5 · GT2, +17% on the median).
4. Rebuild the "prolonged" case as a genuine downside (SA3 · CW7).
5. Fix the Damodaran row inconsistency — beta from Chemical (Basic), multiple from
   Chemical (Diversified) (CC4).
6. Strip every hard-code from the workbook and re-verify with a gate that detects
   `*0+literal`, which the current one does not.
7. Rebuild the Word study, the bibliography, the figures and all three PDFs.

**The delivered .docx/.xlsx/.pdf files in this directory are now INCONSISTENT with the
model.** They carry the pre-rebuild numbers. Nothing should be circulated from this
directory until items 1–7 are complete.
