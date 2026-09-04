# EMPOWER — the evidence for a terminal rebuild, gathered and not yet spent

**Status: the terminal is NOT rebuilt in this edition, and this file exists so the next
pass is a build rather than a research task.** What follows was established on 4 September
2026, checked, and then set down when the rebuild ran into a workbook obstacle described at
the end. Nothing here is a conclusion about value; it is the material a rebuild needs.

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
second reading runs that way.** Accumulated depreciation over the same charge is 10.11
years, against the 14.05 that half of a 28.10-year life implies. Where a base is younger
than uniform, escalating the book charge over half the life OVER-states replacement cost, so
the derived life is the heavier of the two readings and therefore the conservative one.

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

## 6. Why the rebuild stopped, stated plainly

The model change is small and was built and run: routed through the sanctioned module, the
terminal came out about 1.5% higher and the answer about 0.5% higher. **The workbook is
what stopped it.** EMPOWER publishes FOUR parallel live models on one sheet — the crux
columns, the 15% tax framing, the bear case and the upside — each rebuilding the two-stage
terminal in live formulas on a fixed row map built from chained `range()` allocations. The
sanctioned construction needs six more rows per block, and inserting them moves addresses
that a dozen formulas on four other sheets name directly. That is the defect L-300 was
written about, and doing it carelessly would have been worse than not doing it.

**So this edition carries the re-strike and the readable answer, and the terminal stays on
its ratchet with this file as the reason.** The next pass needs no research: it needs the
row map published from the builder, as was done for another study after the same problem,
and then the change above.
