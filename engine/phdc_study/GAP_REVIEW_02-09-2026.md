# PHDC — valuation gap review, 02-Sep-2026

**[R-GAP-01, amended the same day to fire on BOTH sides of the price.]** The
rebuilt central of **EGP 17.15** sits **+12.8% above** the close of
EGP 15.20 on 23 August 2026. Under the rule as originally given this review would
not exist: it fired only below the price. It fires now because the reassessment
found that a one-sided audit is how a lean survives — every correction the house
made ran the same way, each individually right.

This is the first study in this repository audited for being too optimistic, and
it is the house's own method that made it so. Nothing about Palm Hills changed
today: every driver, every filing and every operating assumption is the one the
morning's edition carried.

## Where the move came from, before the headings

| | EGP/share |
|---|---:|
| 30-Aug-2026, weighted blend of four lenses (retired) | 10.94 |
| 30-Aug-2026, its own cash-flow lens | 14.86 |
| 02-Sep-2026, the cash-flow lens on the new standard — the central | 17.15 |

Two changes, and they do not point the same way.

**The lens architecture** raised the published central without touching a single
valuation number. The blend averaged the cash-flow lens with three lenses that
value a developer on its reported earnings and its historical-cost book, and for
a company whose worth sits in an undelivered order book carried at historical
cost those three measure a floor. Removing the average moved the published
figure to whatever the cash-flow lens says; it did not move the cash-flow lens.

**The cost of capital** moved the cash-flow lens, and it is by far the larger
effect. Rebuilt with a flat rate in place of the schedule, everything else
exactly as it stands, the same model gives **EGP 6.35** rather than
17.15. The whole of that +10.80 a share is the difference between
assuming Egypt's cost of capital never normalises and following the central
bank's own published path.

**Running against both** is the horizon. Extending the explicit window from five
years to fifteen — required, because the old window ended at 44% growth and then
capitalised at 7% — cut the terminal from 74% of enterprise value to
31% and took the cash-flow lens DOWN from 26.51 to 17.15.

## 1. LATEST FILINGS — every disclosed period actually read

The most recent filing is the **reviewed consolidated statements for the three
months ended 31 March 2026**, posted to the company's own result centre on
20 May 2026, registered line by line in `bs_1q2026.json`, read by OCR off the
rendered pages because the file is a scan with no text layer, and accepted only
because every subtotal foots. No half-year 2026 statements had been published at
this edition's date. The 1Q2026 results release is registered separately and
supplies the order book, new sales and the land-plot launch.

## 2. BASE YEAR — foots to the filed periods

FY2025 is the audited full year and its income statement foots: revenue less
cost of revenue less the disclosed cash-discount line equals reported gross
profit in all three registered years. FY2026 is **part-reported and is anchored
on what was reported** — disclosed 1Q2026 revenue of EGP 9,300mn, up 11% on the
prior first quarter — rather than projected over the top of it. The implied
FY2026 deliveries of 2,035 units follow from that anchor divided by revenue
per delivered unit and are labelled implied, not disclosed. Nothing is annualised.

## 3. MACRO COHERENCE — one economy, one inflation

Prices and costs escalate on the **house macro path**, 16.0% in 2026 falling to
7.0%, rather than at the flat 25.2% trailing mean the earlier editions carried.
That flat rate was a fair measurement of the recent past and an indefensible
forecast, because the central bank publishes a path the study was ignoring while
using that same bank's target inside its own terminal rate. Price and cost
escalate **together**, so gross margin is an output and holds at
38.3% — the average of the FY2025 and 1Q2026 disclosures. The
coherence is asserted in code rather than in prose: every growth rate is stored
as a real rate against the path and recomputes to its nominal.

## 4. DISCOUNT RATE — the right rate in each year, cash charged once

The ladder runs 26.25% · 22.68% · 19.83% · 17.69% · 16.26% and then holds at
16.26%. Its shape is the central bank's own easing calendar, not a second
assumption of this study's. The terminal value is brought home on the **same
cumulative factor** as the last explicit year's cash flow.

Cash is charged exactly once: net debt of EGP 23,244.7mn is deducted in the
bridge and the discount-rate weights stand on **gross** debt. The equity weight
is 0.564, below one, so the net-cash pathology that produced the AMOC defect
cannot arise here. Country risk enters once, through a risk-free rate normalised
by Egypt's own default spread.

## 5. TERMINAL — growth coherent with the inflation inside the rate

Terminal risk-free 12.50% = terminal inflation 7.00% plus the standard
emerging-market real convention. Terminal growth is **7.00% — that same
inflation, and zero real growth**, stated as such. Earlier editions carried 12%
against roughly 14.6% of embedded inflation, a perpetual real decline of two to
three points a year that nothing disclosed supports. This correction runs
AGAINST the value, not for it.

The explicit window ends with revenue growing at 7.00%, which is the terminal
rate exactly: the boundary gap is 0.00pp against a 2pp bound. The terminal
is 31% of enterprise value, a normal share for a fifteen-year window and
a long way from the 74% the five-year window produced.

## 6. BALANCE SHEET — the bridge stands on the latest disclosed sheet

It does. Net debt, associates, investment property and book value all come from
the reviewed 31 March 2026 statements. Minority interests are deducted at their
share of value, EGP 0.84 a share on the base case, with book and the
proportional read published beside the adopted basis.

## 7. CLAIMS AGAINST THE RECORD — recomputed, not asserted

The study makes no "best ever" or "never" claim about this company. What it does
assert is recomputed: the FY2026 delivery figure is implied by the reported
quarter and labelled implied; the forward gross margin is the arithmetic mean of
the two most recent disclosures and reproduces to four decimals; and the delivery
path takes handovers to **2.19 times** the 2026 level over fifteen years, which
is the one forward claim worth challenging. It rests on the company's disclosed
15% run faded to nothing over ten years. **A reader who doubts that Palm Hills
can roughly double its handover rate over fifteen years should read the lower end
of the published range**, which is what the range is for.

## 8. MULTIPLE CROSS-CHECK — what the central implies

| | EGP/share | P/E 2025 | P/E 2026e | EV/EBITDA 2025 | P/B | market cap over order book |
|---|---:|---:|---:|---:|---:|---:|
| the central | 17.15 | 11.6x | 13.8x | 6.8x | 2.59x | 18.7% |
| the traded price | 15.20 | 10.3x | 12.2x | 6.2x | 2.29x | 16.5% |

Nothing here is extravagant. The central asks a reader to pay 11.6 times last
year's reported earnings and 18.7% of an order book the company has already sold.
The price-to-book of 2.59x is the highest-looking figure in the table and the
least meaningful, for the reason this study gives throughout: the book carries an
undelivered backlog at historical cost in a currency that has lost most of its
value since 2022.

## Verdict

**The answer stands.** The gap is produced by two corrections already required by
this project's own written rules and not being applied: each explicit year
discounted at its own rate rather than at a crisis rate held for fifteen years,
and one lens as the central rather than an average of four. The first is worth
about +10.80 a share on its own. Neither is a new view of Palm Hills.

Two things deserve a reader's scepticism and both are stated rather than buried.
The delivery path takes handovers to 2.19 times their current level over fifteen
years. And the schedule rests on the central bank reaching a 7% inflation target
it has not yet reached; the sensitivity shifts the entire ladder rather than
flattening it, and the low end of the published range is what the model produces
if none of that happens.

**The price sits inside the published range.** This study does not claim the
market is wrong.

## Evidence in this directory

- `gap_review_calcs_above.py` → `gap_review_calcs_above.json` — every computed figure above.
- `study_numbers.json` — the committed numbers, including the macro, cost-of-capital, lens and bridge records the outside gates read.
- `GAP_REVIEW_01-09-2026.md` — the earlier review, written when this same study sat 28% BELOW the price.

---

*AUDITED CENTRAL: 17.1517* — the figure this review audits, stated so a job outside the study can tell whether the review still describes the answer the study publishes. A review of a number the study no longer carries is not a review of this study.
