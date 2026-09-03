# What a mechanical value needs, and what this house actually committed

**3 September 2026.** A finding, not a declaration. It is the answer
`MECHANICAL_LENS_2_03-09-2026.md` named in advance — *"if this construction also
fails, the finding is that a mechanical valuation is not constructible from what
the walk-forward commits, which is a real and reportable result"* — arrived at by
measurement rather than by a third attempt at a shape.

## The question that kept being asked too late

[R-VCAL-01]'s pre-registration commits **series (a)**: a fair value rebuilt at
every origin from the drivers the statement walk-forwards produce, with no
judgement. Two constructions have now been declared for it.

The **first** capitalised projected net profit into a perpetuity. It was withdrawn
on a rule that was already written down — [R-LENS-03] excludes normalised earnings
from the developer row outright — and the first run was committed unaltered before
the replacement was written, so the withdrawal can be audited against what
triggered it.

The **second** valued the contracted order book over a fixed delivery period with
no terminal value and nothing for land, and said in its own text that it is a
**floor**.

Both were shaped by the same constraint, and neither said so plainly enough:
**a cash-flow lens needs capital expenditure and working capital, and neither was
to hand.** The lens was being chosen by what happened to be in the repository.
Choosing a third shape would have been the third answer to a question nobody had
measured, and *a construction adjusted until it produces a comfortable number is a
fit* — which is the bar the second declaration set on itself.

So the question was made a measurement: `engine/valuation_calibration/bridge_inputs.py`.

## What it measures

For every name and every origin the macro archive declares, which of the items a
valuation needs is present in **that run's own committed artefacts**, and which
file carries it. The items, and why each is on the list:

| item | why it is needed | what its absence does to the answer |
|---|---|---|
| cash | the enterprise-to-equity bridge, [R-BRIDGE-01] (iii) | **understates** equity value |
| debt | the other side of that bridge | **overstates** equity value |
| capex | the reinvestment a flow lens subtracts | **overstates** equity value |
| PPE | makes capex derivable by identity: capex = ΔPPE + D&A | — |
| depreciation | what a *declared* capex substitution would use | — |
| working capital | conversion of profit into cash | sign depends on growth |
| share count | turns an equity value into a price | no comparison is possible at all |

Two conventions the module enforces on itself, because both were got wrong on its
first run and the errors were invisible:

- **The key map is named per run, not matched by pattern.** The five runs share no
  schema and several abbreviate: TMGH writes `da` for depreciation and PHDC writes
  `bs.ar` and `bs.np_short`. A regex broad enough to catch those matches a third of
  the keys in the repository; the narrow one that ran first reported TMGH as
  carrying no depreciation and PHDC as carrying no working capital. The regex is
  kept only as a **guard** that prints every key it matches which the map does not
  claim, so the next run's vocabulary cannot go missing in silence [R-ENF-04].
- **Paid-in capital is not a share count.** TMGH commits `paid_capital` in currency;
  it becomes a count only when divided by a par value. The two are different rows,
  because crediting a cell with a count it does not have is the fabrication this
  archive exists to refuse.

## What it found

Read it live — `python3 engine/valuation_calibration/bridge_inputs.py` — never from
this document. On the day it was written:

- **0 of 55** name-origin cells carry a complete bridge **and** a capital-expenditure
  figure. Not one walk-forward committed a capex actual. TMGH has a `capex`
  parameter slot and it is null at every origin.
- **3 of 55** carry a complete bridge where capex is derivable by identity
  (ΔPPE + D&A): TMGH 2020, 2021, 2022.
- **5 of 55** carry the bridge but no route to capex at all, and are valuable only
  under a *declared substitution* — an assumption, not a figure: PHDC 2015–2019.
  These are exactly the five cells the second declaration ran on, which is why it
  had to be a floor.
- Cash is present on **25%** of cells, debt on **60%**, working capital on **27%**,
  a footed share count on **16%**.

Eight cells, across two names, **both of them developers**.

## Why that settles it, and the reason is not the count

Eight cells could still be worth scoring. What rules it out is **the direction of
what is missing**.

The reassessment tests whether this house leans pessimistic. Every omission above
has a known sign, and they do not point the same way: no cash **understates** value,
no capex **overstates** it, working capital does either depending on growth. An
instrument assembled from whatever each cell happens to carry therefore has a bias
whose direction is set by *which items that cell is missing* — so it varies from
cell to cell, in unknown direction and unknown magnitude.

That is worse than a large bias. A floor is honest because you know which way it
points; a per-cell bias of unknown sign cannot be corrected, disclosed as a
direction, or reasoned around. **An instrument like that cannot measure a
directional hypothesis** — and where its bias happens to run the same way as the
hypothesis, it would confirm it by construction. On AMOC, a net-cash company, the
omission of cash is not a rounding error: it is most of the answer.

## What would make series (a) constructible, named exactly

Nothing here is unobtainable. Every missing item is on a balance sheet or a
cash-flow statement in filings this repository already holds — they were simply
never carried out of the run:

1. **cash and equivalents** at each origin — absent for AMOC, ARCC, EGCH;
2. **interest-bearing debt** at each origin — absent for AMOC; present for ARCC and
   EGCH, present for PHDC and TMGH;
3. **capital expenditure**, or PPE **and** a depreciation charge from which it can be
   derived — absent everywhere as a figure, derivable only on TMGH;
4. **the share count**, footed against its own filing — now held for PHDC 2015–2019
   and TMGH 2020–2025; in progress for ARCC and EGCH.

Three of the four are balance-sheet lines beside statements that were parsed cell
by cell. The cost of not carrying them is not a gap in a table: it is that **no
valuation this house makes can ever be rebuilt at a past origin**, and that loss is
permanent for every year whose filings are no longer to hand.

That is a recommendation about [R-FCAL-01]'s required outputs, and it is put
forward as one: **a fundamental walk-forward should commit a valuation-input block
beside its driver panel** — cash, interest-bearing debt, PPE, depreciation and
amortisation, the working-capital lines, and the share count with its par value —
because those six are what separate a driver record from a record a value can be
rebuilt from.

## What the calibration rests on until then

**Series (b), the as-delivered book** — every fair value this house has published,
against the spot it was struck at. It is short (2025 onward) and the
pre-registration says so. It is also the series that has already changed the
diagnosis: the mean sits about a tenth below the price, the **median sits
essentially on it**, and the names split almost evenly either side, with the whole
of the mean in a tail. The house was not uniformly pessimistic; it was
**inconsistent** — a different finding with a different remedy, and the obvious
remedy would have been the wrong one.

Series (a) is **not abandoned and not weakened**. It is blocked on four named
inputs, and the pre-registration already governs what happens to a cell whose
inputs are not sourced: *the origin is dropped and the window shortened — never
interpolated.* This is that rule applied at the scale of the whole series rather
than one cell.

## What would overturn this finding

- **A run that commits the block.** The moment any name carries cash, debt, capex
  and a share count at a run of origins, series (a) is constructible on it and the
  census will say so on its next run. This finding expires by measurement, not by
  argument.
- **A demonstration that the per-cell bias is bounded.** If someone shows that the
  missing items are small relative to value on a given name — a company with no
  debt, no cash and no reinvestment — then a mechanical value on that name is
  honest and the census is too strict. The test is arithmetic and available.
- **A finding that the mechanical series was never the right instrument.** The
  pre-registration's own falsifier already covers this: if the mechanical series
  turns out not to resemble the as-delivered one once the latter is long enough to
  compare, then it grades a method the house does not use.

---

*This document asserts no fair value and declares no lens. It records a
measurement, the four inputs it names, and the recommendation that follows.*
