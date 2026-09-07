# The transmission test, and one defect it found

Read live: `python3 engine/valuation_calibration/clock_test.py`

[L-048] says a model escalating costs at domestic inflation while holding the
price or the currency still counts one event once and ignores it once, and then
reports the manufactured margin decline as a finding. It was registered, it was
correct, and it has been re-violated since. [R-MACRO-01] made the macro PATH
arithmetic; it did not make the TRANSMISSION arithmetic, and the transmission is
where the defect lives.

This measures the transmission instead of reading five modules. For each run,
what each side of the income statement actually escalates by over three years,
against the inflation the same model believes in over the same three years:

| name | own inflation | revenue x | cost x | volume x | revenue clock | cost clock | gap | price clock | unit cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| AMOC | 1.24 | 1.00 | 1.02 | 1.00 | **0.81** | **0.83** | +0.02 | 0.81 | 0.83 |
| EGCH | 1.39 | 1.31 | 1.39 | — | 0.94 | 1.00 | +0.06 | — | — |
| ARCC | 1.32 | 1.36 | 1.21 | 1.04 | 1.03 | 0.92 | -0.11 | 0.99 | 0.88 |
| TMGH | 1.54 | 2.95 | 2.92 | — | 1.78 | 1.76 | n/a | — | — |
| PHDC | 1.46 | 2.10 | 1.47 | 1.40 | 1.44 | 1.00 | n/a | — | — |

A clock of 1.00 escalates exactly at the model's own inflation.

## What the finding is

**AMOC is frozen in nominal terms.** Both clocks near 0.82 with a gap of +0.02.
It is NOT [L-048]: the two sides differ by two points, while the whole model
differs from its own economy by twenty-four. Crude is both this company's product
and, as feedstock, most of its cost of sales, so freezing crude in pounds freezes
almost the entire income statement. A company standing still in nominal terms
inside an economy inflating at 7.4% a year is declining in real terms by
construction — [R-MACRO-01]'s terminal-growth-below-inflation defect arriving in
the explicit window. Putting crude on a path takes the bias from -0.774 to
-0.258; the adopted fix (the house PPP identity) reaches -0.443.

**No run in this book has an [L-048] gap.** Of the three where the gap is
readable, the widest is ARCC at -0.11.

## Where the gap is readable, and where it is not

The gap tests [L-048] only where both sides scale on the SAME volume path, so
that volume cancels. On a single-product operating company it does. **On a
developer it does not**: revenue is a percentage release of a backlog while cost
follows deliveries, two different quantities. So the gap is reported `n/a` for
PHDC and TMGH rather than as a number.

**This was learned by getting it wrong.** PHDC's raw difference came out at
-0.44, four times the next widest, and this document's first version read it as
[L-048] in mirror image — a manufactured margin expansion, on the one name of
five that over-forecasts its own history and whose published central sits 24%
above the market. Three facts lining up is exactly when a reading feels settled.
Reading PHDC's projector settles it the other way: `asp` and `cogs` are escalated
by the SAME `infl` term in the same loop, so there is no price-versus-cost
escalation asymmetry there at all. What the raw gap measures is that revenue is
`delta x (backlog + new_sales)` while cost is `unit cost x deliveries` — the
recognition mechanism of a developer with a growing backlog, which is a forecast
rather than a defect.

**The number was real and the reading of it was wrong**, which is [R-TERM-01
CLAUSE TWO CORRECTED] in another costume: a ratio between two quantities defined
differently is not evidence about either. It computes, it sorts the book, it
looks like a measurement.

## Three drafts of this instrument, and what each got wrong

**Elasticity.** The first bumped inflation by a point and read the local slope. A
derivative cannot see a level held still: it reported AMOC as "one clock" when
both of AMOC's sides were frozen. Re-pointed at the escalation actually applied
over the horizon, per [R-COC-01] — never widened.

**Ratio of averages.** The second reported a clock as mean(revenue) over
mean(inflation). Those are averages over origins whose inflation differs by half
again, so it weights the high-inflation origins into the denominator and the
high-growth ones into the numerator. Each origin's own clock is formed first and
the clocks are averaged.

**A cost recorded as a negative is a sign convention, not a missing value.** An
earlier filter required the base-year figure to be positive and dropped every
cost line TMGH commits, then reported that run untestable — an absent answer
wearing the costume of a result [R-ENF-04].

All five runs are listed, including the ones that need an adapter, and a run that
cannot be measured prints its reason rather than being left off the list.

## What is still open on PHDC

PHDC remains the one name of five that over-forecasts its own history (+0.144
pooled, +0.292 outside the devaluation years) and the one whose central sits well
above the market. This instrument does not explain that, and it should not be
made to: the backlog-release mechanism is where to look, and whether `delta` —
the share of backlog released each year — is forecast at a rate the company's own
delivery record supports is a separate question this test cannot answer.
