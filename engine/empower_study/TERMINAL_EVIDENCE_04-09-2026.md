# EMPOWER — the evidence for a terminal rebuild, gathered and not yet spent

**Status: THE TERMINAL IS REBUILT. This file is the evidence it rests on**, gathered on
4 September 2026 and spent the same day. It is kept because the route by which each figure
was obtained is part of the record — arithmetic is the arbiter here, not the extractor's
confidence, and a reader is entitled to see the four ways the extraction was made to foot.

*An earlier version of this file recorded the rebuild as blocked. That assessment was
wrong and is corrected rather than deleted: see the last section.*

## 1. The audited statements are now to hand, and they had to be read off the pixels

The FY2025 consolidated financial statements, signed 9 February 2026, were fetched from the
company's own investor-relations page. **The file carries no usable text layer** — 85 bytes
across 85 pages — so every figure below was read by OCR off the rendered image, and the
property note, which is printed landscape, had to be rotated before it could be read at all.

**Arithmetic is the arbiter, and the extraction foots four ways:**

| check | extracted | printed |
|---|---|---|
| cost columns sum | 10,929,327 | 10,929,327 |
| accumulated-depreciation columns sum | 3,734,337 | 3,734,337 |
| cost less accumulated | 7,194,990 | balance sheet 7,194,990 |
| the year's charge, split by destination | 341,696 + 10,503 | 352,199 |

The last of those is the strongest: the note states the charge separately in cost of sales
and in general and administrative expenses, and the two reconstitute the total the movement
table prints.

## 2. The disclosed useful lives, and the weighted life they do not give

Note 2.3 gives ranges and no weighting:

| class | years |
|---|---|
| Plant, equipment and machinery | 2 to 30 |
| Buildings | 25 |
| Furniture and fixtures | 3 to 5 |
| Leasehold improvements | 3 to 4 |
| Computer equipment | 3 |
| Vehicles | 3 to 5 |

Land is not depreciated. Intangibles are disclosed at **30 years** outright (note 7), and
the right-of-use note records equipment leases from DEWA on 15-year terms and a head-office
and labour-accommodation lease on one year.

**So no single figure can be read off the policy note, and the identity supplies one:**

| | gross cost (AED 000) | charge | implied life |
|---|---|---|---|
| Property, plant and equipment (note 5) | 10,001,105 | 352,199 | 28.40 y |
| Right-of-use assets (note 6) | 22,649 | 5,361 | 4.22 y |
| Intangibles (note 7) | 364,710 | 12,157 | 30.00 y (disclosed) |
| **Blended** | **10,388,464** | **369,717** | **28.10 y** |

Cross-checked at **27.88 years** on FY2024's own columns. Land is excluded because it is
never depreciated, and capital work in progress because its accumulated column is
impairment rather than depreciation — the charge line against it is nil in both years.

**The right-of-use figure of 4.22 years does not match the 15-year equipment lease the note
names, and the note explains that rather than contradicting it:** the book is 19,997 of
buildings against 2,652 of equipment, and the buildings are a one-year office and
accommodation lease that depreciates fully each year.

**The base is YOUNGER than uniform, which is the first name in this programme where the
second reading runs that way.**

| | accumulated | the year's charge | age |
|---|---:|---:|---:|
| Property, plant and equipment | 3,734,337 | 352,199 | 10.60 y |
| Right-of-use *(gross 22,649 less net 1,878)* | 20,771 | 5,361 | 3.87 y |
| Intangibles *(gross 364,710 less net 315,668)* | 49,042 | 12,157 | 4.03 y |
| **Charge-weighted** | **3,804,150** | **369,717** | **10.29 y** |

against the **14.05** that half of a 28.10-year life implies. Neither the right-of-use nor
the intangible note prints an accumulated column, so both are recovered by the identity
gross less net — an identity, labelled as derived.

*This figure was first written here as **10.11 years**, which took the property note's
accumulated column over the BLENDED charge — a numerator covering one leg and a denominator
covering three. It understated the age by 1.8%. Corrected rather than quietly replaced.*

Where a base is younger than uniform, escalating the book charge over half the life
OVER-states replacement cost: at this market's 2% terminal the escalators are 1.2260 on the
measured age against 1.3208 on half the life, so the construction charges **7.2% more** than
the base's own age supports. The shared construction now takes a measured age where one is
supplied and sourced, so this is a correction this study can take at its next pass rather
than a caveat it has to carry.

## 3. What the retired construction implies here

The published terminal is two-stage — ten years at 2.5% then a perpetuity at 1.5% — and
**both stages charge reinvestment as growth over the return on capital**, which is
arithmetically the same as rebuilding the entire capital base every 1/g years: **fifty years
in stage one and sixty-seven in stage two**, against a base the company's own notes turn
over in 28.1.

## 4. The growth rates, and why storing them properly changes nothing here

This is worth recording because it is the opposite of the last two names. EMPOWER's tariff
is **regulated and not indexed**, so nominal revenue growth IS volume growth, and the typed
nominal rates carry a meaning they do not carry elsewhere:

- stage one, 2.5% nominal on 2.0% house inflation = **+0.49% real**;
- stage two, 1.5% nominal = **−0.49% real**, a real decline that the study's own words
  ("about zero real tariff growth") describe without naming.

Storing them as real rates reproduces both nominal figures to the basis point. **The
storage rule would move no number on this name** — it would only make visible that stage two
assumes the business shrinks in real terms for ever, which a reader currently has to
compute.

## 5. One derivation that must NOT be carried over from the other names

The capital a unit of real growth consumes has been taken elsewhere as the marginal
invested capital per unit of revenue across the explicit window. **On EMPOWER that figure
is NEGATIVE, about −388**, because over these five years the plant is written down faster
than capex replaces it and the working capital is negative and growing more so. A negative
capital requirement would **credit this company for growing**, which is not something a
chilled-water network can do: another unit of demand needs another plant. The defensible
figure is the intensity the business already runs at — one per cent of real growth costs one
per cent of the invested capital it operates on, which is terminal invested capital.

## 6. The obstacle, and why the first assessment of it was wrong

The model change is small and was built and run in under an hour. **The first attempt then
stopped**, on the following reasoning: this study publishes FOUR parallel live models on one
sheet — the crux columns, the second tax framing, the bear case and the upside — each
rebuilding the two-stage terminal in live formulas on a fixed row map built from chained
`range()` allocations; the sanctioned construction appeared to need six more rows per block;
and inserting them moves addresses that a dozen formulas on four other sheets name directly.

**That reasoning contained one wrong step and it is worth naming.** The waterfall needs to
appear *once*, on the sheet where a reader follows the arithmetic. The four parallel blocks
need only the two stages' free cash flows — two figures each — and each of them already had
two rows spare, because the retired construction's terminal-return and NOPAT-in-FY2040 rows
had just become meaningless. **Repurposing two dead rows costs nothing and moves no
address.** The rebuild that had been called blocked took one further pass.

The general form is worth keeping: **an obstacle assessed from the shape of the change is
not the same as an obstacle measured.** The row map was real, the coupling was real, and
the conclusion drawn from them was wrong because it assumed the new construction had to be
displayed everywhere it was used. What a parallel re-run owes a reader is its result, not a
second copy of the derivation.
