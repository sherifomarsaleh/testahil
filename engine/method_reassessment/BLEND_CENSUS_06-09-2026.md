# The retired blend, measured on the three names that still carry one

**Dated 6 September 2026.** Done by hand against each study's own committed numbers, because
the agents that would have done it were out of credits. Nothing here needed a model run;
every figure reproduces from `study_numbers.json`.

---

## What was found

Three studies still publish a central that reproduces as a **weighted combination of their
own lens reads**, and in all three **book value carries weight** — which [R-LENS-03] forbids
separately from, and in addition to, the blend itself.

| study | weights | book | published central | class primary alone | vs latest price |
|---|---|---|---|---|---|
| ADNOCDIST | 40/25/20/15 | 15% | 4.4113 | 4.7840 (DCF) | blend +9.7% · primary +19.0% |
| ADNOCDRILL | 25/25/20/15/15 | 15% | 4.9194 | 6.2083 (DCF A) | blend **−15.2%** · framings' midpoint **+0.046%** |
| AMR | 50/20/20/10 | 10% | 2.1455 AED | 2.2333 (DCF) | blend −10.2% · primary −6.6% |

Every reproduction is exact: ADNOCDRILL's residual is **zero**, ADNOCDIST's **8.9e-16**, and
AMR's runs through the dirham peg (0.584208 USD × 3.6725 = 2.145502 AED, the published
figure to the last digit — its lens block is in dollars and its central in dirhams, which is
why a naive read makes them look unrelated).

**THE DIRECTION IS THE SAME IN ALL THREE. The blend sits BELOW the class primary in every
case.** That is not a coincidence of three companies; it is what the architecture does. Three
of the four or five lenses in each value the business on reported accounting earnings and
historical-cost book, which are a floor rather than a value, and averaging a floor into an
answer drags the answer toward the floor at whatever weight somebody typed.

---

## The sharpest single case

ADNOCDRILL's two cash-flow framings are 6.20828 and 5.39701. Their midpoint is **5.80264**
against a latest known price of **5.80** — a gap of **0.046%**. The published blend is
4.91943, **15.2% below**.

**The entire discount is the blend.** The study's own cash-flow work lands on the traded price
to within five hundredths of one per cent, and the price sits inside its own 5.40–6.21
envelope, near the middle. There was never a market disagreement here to explain.

This is the PHDC precedent that produced [R-LENS-03], sharper: there the cash-flow lens landed
within 2.2% of the market and the blend 28% below.

---

## What this does NOT establish, and the probe's own limits are the main one

**Sixteen studies commit no weight vector my resolver could find, and that is not the same as
conforming.** Several carry a `retired_blend` key showing they were conformed deliberately
(ARCC, AMOC, DU, MODON, RIYADHCABLE, SWDY); of the ones whose central and lens block pair up
at all, only **ARCC and SCEM** could be positively confirmed as *central IS the DCF*. For the
rest the pairing does not resolve from the committed record, and **an unreadable study is not
a clean one** [R-ENF-04]. The right reading of the table above is "three found", never "three
of twenty-four".

The probe was re-pointed twice before it was believed. Its first draft called twenty of
twenty-four studies unreadable, which was a fact about the resolver rather than the book —
the lens blocks live in at least six different shapes, and AMR was nearly missed entirely
because its lenses are in dollars and its answer in dirhams.

**Nothing is corrected here.** Retiring a blend moves the answer, which makes it a re-issue
with a rebuild ledger [R-REBUILD-01], not a line in a census. And the correction runs
*upward* on all three, so it belongs to [R-VCAL-01]'s promotion guard — which is symmetric,
and which a house that has just found three corrections all pointing the same way should be
reading carefully rather than skipping.
