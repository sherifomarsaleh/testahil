# What the score does not score

Read live: `python3 engine/valuation_calibration/scoring_blindspot.py`

Every driver bias this house publishes is a **log error**, and a log error needs
both the projection and the actual to be positive. On a revenue line that is
harmless. On a profit line it is not: a cell where the model projected a loss, or
where the company made one, is dropped — silently, from a mean everyone then
reads as that driver's bias.

## The measurement

For each driver: how many cells exist, how many the log score takes, and the bias
on ALL cells against the bias on the taken subset — **both in relative error**, so
the comparison is about the SAMPLE and not about the scale.

| name | driver | cells | taken | bias ALL | bias TAKEN | factor |
|---|---|---:|---:|---:|---:|---:|
| EGCH | revenue | 55 | 55 | -0.200 | -0.200 | 1.0x |
| EGCH | cost of sales | 55 | 55 | -0.269 | -0.269 | 1.0x |
| EGCH | gross profit | 55 | 34 | +0.332 | +0.436 | 0.8x |
| EGCH | selling | 35 | 21 | -0.491 | -0.152 | **3.2x** |
| EGCH | other bucket | 48 | 23 | +0.341 | +0.813 | 0.4x |
| EGCH | **fx** | 50 | **0** | **-5.743** | **not scored** | — |
| EGCH | **pbt** | 48 | 23 | **-1.589** | -0.298 | **5.3x** |
| EGCH | tax | 44 | 21 | +0.077 | -0.328 | 0.2x |
| EGCH | **net** | 48 | 23 | **-1.496** | -0.382 | **3.9x** |
| ARCC | pbt | 25 | 20 | +1.226 | +1.399 | 0.9x |
| ARCC | attributable | 25 | 20 | +1.395 | +1.712 | 0.8x |
| AMOC | every driver | 9 | 9 | — | — | 1.0x |

**Thirteen of twenty-eight drivers lose cells to the log score, and where it
happens the two samples disagree by up to 5.3 times.**

## The omission is not one-signed, and that is the finding

Of the thirteen drivers that lose cells, **five show a larger bias on the full
sample and eight show a smaller one**. A first draft of the instrument asserted
the flattering direction — that dropping loss cells removes the worst misses and
so understates the error — and the measurement refused it.

**That is the worse of the two outcomes.** A known lean can be corrected for. A
published figure that differs from its own full sample by up to five times in an
unknown direction cannot, and nothing on the page says which way it went.

What IS consistent is *where* it happens. Revenue and cost are always positive
and lose nothing. The distortion falls entirely on the **bottom-line drivers a
valuation actually depends on** — profit before tax, net profit, tax, and the
signed residual lines.

## One driver is scored by nothing at all

**EGCH's foreign-exchange line has 50 cells and the log score takes none of
them.** It is declared in that run's driver list, it drops out of the scores file
because every cell is unscoreable, and it appears in no table this house
publishes. Its bias on all fifty cells is **-5.743** — by far the worst driver in
the run — and the sign is right in 15 of 50 cells, which is worse than a coin
flip.

The construction behind it is separable: the model computes a translation loss on
the origin's dollar-denominated bank borrowings and nothing else. A fertiliser
exporter selling in dollars also holds dollar receivables, which produce
translation GAINS — so the model projects a loss where the company reported a
gain. In levels this line is **-409,482 of EGCH's -947,868 profit-before-tax gap,
43% of it.**

## Why this matters beyond one run

The reassessment has spent days working from pooled driver biases. On the profit
lines of at least one name, **those pooled biases were computed on under half the
cells**, and the half was chosen by whether a loss appeared. That is not an
argument that the earlier conclusions are wrong — the break effect, the spread
result and the escalation ranking all rest on revenue and cost lines, which lose
nothing. It is an argument that **the bottom-line figures were never as solid as
the top-line ones, and nothing distinguished them.**

## What is not proposed

Relative error is used here to hold the two SAMPLES against each other in one
metric. It is **not proposed as a replacement score**: it is unbounded below and
asymmetric, and swapping the house score on the strength of this file would be
exactly the selection the promotion rule forbids. What is established is narrower
— that a published bias on a signed driver is measured on a sample nobody
declared, and that the sample and the full set disagree materially.
