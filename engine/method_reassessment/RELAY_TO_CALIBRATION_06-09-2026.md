# Relay to the calibration chat — 06-09-2026

Written here rather than said in a conversation, per [R-IND-01]: an answer living
only in a chat binds nothing, because the container is rebuilt from the repository.

## What closes criterion 3, in order — and the first item is the blocker

**1. The valuation-input block has to exist per origin.** `bridge_inputs.py`
measured it: across the five names run, not one origin carried a complete bridge
AND a capex figure. Without cash, debt, capex, working capital and a footed share
count at each past origin, a cash-flow lens cannot be built. That is why series (a)
today is a contracted-order-book FLOOR rather than a fair value, and why
`SCORES_contemporaneous_03-09-2026.json` says in its own text that a reading below
the price is the expected case. [R-FCAL-01 AMENDED] binds forward only, so each
name gets its block at its NEXT walk-forward run.

**2. Series (a) is then rebuilt as a real fair value** on those inputs, replacing
the floor.

**3. The panel has to be large enough to carry a bootstrap CI.** It holds four
origins on one name today (PHDC 2016-19), and the scores file says so in terms:
"four origins on one name is not a finding."

**4. Then the score runs**, per Part E criterion 3: pooled contemporaneous bias
CI includes zero, LONO-stable in sign, holds in both eras, beats "FV = price" and
trailing P/E x EPS on MAE, residual attributed to a named lever.

## The knot, raised rather than resolved

Step 3 needs many names. Many names is Phase 2a. The plan holds Phase 2a until
Phase 1's record shows the method unbiased — and Phase 1 cannot reach a credible
interval on five names. As written the two wait on each other.

This is a decision for the principal, not something the calibration can settle on
its own. It is recorded here so it is visible rather than discovered later. Note
that [R-GAP-02] clause three holds ISSUING AND PUBLISHING, not internal work, so
running backtests on further names is not itself blocked by that gate — what is
sequenced is the plan's own Part D ordering.
