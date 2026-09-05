# BOROUGE — what its published central actually is, and it is not a valuation choice

Written 5 September 2026 while diagnosing why seven studies are invisible to the
valuation-gap gate. **This is a finding, not a rebuild.** The rebuild is the next pass's
first job on this name and its audit point should be declared before it starts, because
three corrections stack here and two of them are large.

## The published central is a counting artefact

`compute.py:721-722` builds the answer this way:

```
vals = list(lenses.values())
FAIR_LOW, FAIR_HIGH = float(min(vals)), float(max(vals))
FAIR_MID = float(np.median(vals))
```

Nine lens readings, and the middle one is published. **The nine are not nine independent
views of the company.** They are a 2×2 grid of two orthogonal framings — a beta choice
(own-stock against bottom-up sector) and a scenario choice (normalisation against
prolonged) — plus a framing-neutral relative multiple. Sorted:

| | value |
|---|---:|
| normalised earnings, sector beta | 1.3012 |
| DCF prolonged, sector beta | 1.3100 |
| book value, sector beta | 1.4388 |
| relative multiples | 1.4599 |
| **DCF normalisation, sector beta — THE PUBLISHED CENTRAL** | **1.4770** |
| normalised earnings, own beta | 2.3458 |
| DCF prolonged, own beta | 2.3481 |
| book value, own beta | 2.3898 |
| DCF normalisation, own beta | 2.5499 |

**The readings do not spread — they cluster in two blocks, one per beta**, 1.30–1.48 and
2.35–2.55, with the relative multiple sitting inside the lower block. So the median does
not average anything: it SELECTS ONE CELL of the grid, and which cell it selects is
decided by how many lenses happen to have been computed under each framing.

**Four sector readings plus the framing-neutral relative multiple make five below the
gap; four own-beta readings sit above it, so the fifth of nine lands at the top of the
lower block.** Compute one more lens under the own-stock beta and the median moves to
**1.9114**. Drop one sector lens and it moves to **1.9028**. Neither of those is a
different view of the company — **it is a different number of rows in a list.**

That is the [R-LENS-03] failure in an unusually clean form. The rule is written against a
typed weighted blend; this is not one, and it is caught for the same reason it gives: *"a
number produced by averaging several methods is not more robust than the best of them — it
is a NEW method with free parameters nobody tested."* Here the free parameter is not even a
weight somebody chose. It is a count.

## And the cell it selects is the SECOND framing's, not the one the study adopts

**CORRECTED BEFORE ACTING ON IT.** An earlier version of this section said the study had
substituted a tier-2 beta where a tier-1 beta passes, and that is wrong. `beta_result.json`
records the opposite in its own words: *"tier-1 own-stock weekly regression against its own
local index (usability gate PASSED) … All three conditions of the usability gate are met,
so the regression estimate is adopted rather than a default."* **The study adopts the
tier-1 beta.** It then builds a bottom-up sector beta as a SECOND FRAMING and publishes both
side by side — which is not a defect at all; it is depth-bar standard 8, the study's single
most consequential contested judgement computed both ways and published side by side.

**The defect is the median, and only the median.** The dual framing is correct and the
`fair_mid` that collapses it is the very thing standard 8 forbids in the same sentence that
requires it: *"never averaged into one number."* The study does the hard half right and then
undoes it in one line of `compute.py`.

That distinction matters for the rebuild. There is nothing to fix in the beta, and there is
no shrinkage to apply: the own-stock regression passes its gate and is adopted, its weakness
is disclosed, and the sector read stands beside it as the labelled alternative. **What has
to change is what the study CALLS its answer.**

The own-stock beta is 0.4153 with R² 9.45%, n 215, SE 0.0881, `usable: true` and a `weak:
true` flag — a 90% interval of [0.27, 0.56] spanning 0.70× the point estimate. That
weakness is exactly why a second framing exists, and it is disclosed rather than hidden.
Whether a Vasicek shrinkage toward the sector prior would be a better central than either
cell is a real question and it is NOT this rebuild's: [R-COC-01] permits it, the study has
not taken it, and taking it would be a new construction rather than the application of a
standing rule.

## What the rebuild has to do, and why it needs a declared audit point

Two corrections, not three, and the beta is not one of them:

1. **The lens architecture** — [R-LENS-03]: one class primary IS the central. BOROUGE is
   registered `petrochemical`, whose row is a DCF primary with EV/EBITDA on own history,
   replacement cost, a relative multiple and book beside it. **Normalised earnings appears
   in no row of the registry at all**, so those two readings come out entirely — the same
   thing EMPOWER's record found, and the rule working rather than a gap in it.
2. **The median retired** — the two framings stay, published side by side as standard 8
   requires; what goes is the single number that averages across them. Whether the answer
   is then two branches or one central with the other framing as a labelled alternative is
   the rebuild's own decision, and it is the only judgement in this pass.

**Which cell the answer lands on decides the size of the move and it is large either way.**
The own-beta normalisation cell reads 2.5499 against the published 1.4770, +72.6%, against
a spot of 2.40 that is itself a month stale — which would take the study from 38% below the
price to roughly 6% above it, crossing [R-GAP-02]'s publication block in the direction that
releases it. **That is exactly why the audit point is declared BEFORE the levers are
applied rather than after**, and why the choice between the two framings has to be made on
the rules rather than on where it lands. [R-REBUILD-01] exists for this shape.

**None of the three is discretionary and none was chosen for where it lands.** Each is a
standing rule applied to a study that predates it.
