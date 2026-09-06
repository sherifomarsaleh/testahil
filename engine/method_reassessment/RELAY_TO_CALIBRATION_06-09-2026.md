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

---

# Correction to item 1 above — 06-09-2026, on the principal's challenge

The principal read the relay and objected, correctly: *"that is strange as we have
IS, BS and CF statements forecasted in all tickers."* The objection stands and the
first framing above was too broad. What follows is measured, not argued —
`python3 engine/valuation_calibration/bridge_inputs.py`.

## Two different artefacts were being conflated

- **The delivered study** forecasts a full three-statement model. That is mandatory
  (Appendix A.1/A.2/A.3, and the Balance Sheet and Cash Flow sheets of the 16-sheet
  workbook). Nothing is missing there.
- **The walk-forward run** is a separate artefact. It commits a panel of FILED
  ACTUALS at each past year, which is what the forecasts are scored against. That
  panel is what is patchy.

So "the balance sheet was never forecast" is WRONG and should not be repeated.
PHDC's own panel carries eighteen balance-sheet lines — cash, banks credit, fixed
assets, receivables, payables, equity, the lot.

## What is actually absent, across 55 name-origin cells

| item | present | direction when absent |
|---|---|---|
| debt | 33 (60%) | overstates equity value |
| depreciation | 23 (42%) | what a declared capex substitution would use |
| PPE | 15 (27%) | makes capex derivable by identity |
| working capital | 15 (27%) | sign depends on growth |
| cash | 14 (25%) | understates equity value |
| share count (footed) | 9 (16%) | no comparison with a price is possible at all |
| **capex** | **0 (0%)** | **overstates equity value** |

Cells with a complete bridge AND a capex figure: **0 of 55**.
Cells where capex is DERIVABLE by identity (ΔPPE + D&A) on top of a complete
bridge: **3 of 55** — TMGH 2020, 2021, 2022.
Cells with a bridge but no route to capex at all: **5 of 55** — PHDC 2015-2019.

**No cash-flow statement was committed at any origin, on any of the five names.**

## The sharpened statement of the blocker

The gap is not a missing FORECAST. It is a missing HISTORICAL record. The studies
model the future correctly; what nobody wrote down is the company's own cash-flow
statement, and in most cells its cash and share count, AS THEY STOOD at 2016, 2017,
2018. A past valuation cannot be rebuilt without them, which is exactly
[R-FCAL-01 AMENDED]'s general lesson: what a process commits decides what can ever
be asked of it later, and nobody notices the missing field until the question
arrives.

Practical consequence for the next runs, unchanged in substance: the valuation-input
block is a COPY out of filings already parsed cell by cell, not new research —
cash, interest-bearing debt, PPE, D&A, the working-capital lines, the share count
footed against its par value, and capex disclosed or labelled as derived.
