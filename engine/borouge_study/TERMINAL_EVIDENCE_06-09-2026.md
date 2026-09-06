# BOROUGE — the disclosed useful life, sourced from the filings, 6 September 2026

**Status: THE LIVES ARE DISCLOSED, THEY FOOT, AND THEY WEIGHT. NO SINGLE MAINTENANCE LIFE
IS AVAILABLE, and the blocker is the width of the company's own range rather than an
absence.** This pass re-ran the 5 September work from the filings rather than reading its
conclusions. It CONFIRMS that pass on every figure it re-measured, CORRECTS one claim in it,
and moves this name from *not sourced* to *sourced, not yet collapsed* — which is a
different state and the one the register is built to hold. **Nothing here changes a
published number, a document or a central.**

## 1. The accounting-policies note, quoted exactly

Borouge PLC, FY2025 audited consolidated financial statements, **note 3 Material accounting
policy information**, printed page 22 (PDF page 28), under *Change in estimate — useful life
of property, plant and equipment*:

> "The estimated useful lives of the Group's Property, Plant and Equipment is applied
> prospectively, in accordance with IAS 8, from 1 July 2025, as follows:"
>
> | | **Years** |
> |---|---|
> | Buildings | 15 – 40 |
> | Plant and machinery | 8 – 35 |
>
> "The estimated useful lives of the Group's remaining Property, Plant and Equipment where
> there is no change in useful life is as follows:"
>
> | | **Years** |
> |---|---|
> | Motor vehicles | 4 – 10 |
> | Furniture, fixtures and equipment | 3 – 4 |

and, in the depreciation policy above it:

> "Depreciation is charged so as to write off the cost **less estimated residual values** of
> property, plant and equipment, **other than capital work in progress**, over their
> estimated useful lives, using the straight-line method"

No land is carried — the Ruwais site is held under a right and licence granted by the
Supreme Petroleum Council (note 6). Capital work in progress is excluded from every
weighting below because the note says outright that it does not depreciate.

## 2. The route — four reads, and the pixels are the arbiter

The source PDFs are gitignored. **The FY2025 statements and the FY2024 statements were
refetched from the company's own investor-relations site today and both hash-match
`source_access.json` byte for byte** (FY2025 `988c9016…a83f`, 1,057,217 bytes; FY2024
`6c6f3c27…c91a`, 1,183,317 bytes).

| route | toolchain | what it gave |
|---|---|---|
| FY2025 text layer, `pdftotext -layout` p28 | PDF-XChange 10.7.2 | 15-40 / 8-35 / 4-10 / 3-4 |
| FY2025 text layer, `pdftotext` without `-layout` | PDF-XChange 10.7.2 | 15-40 / 8-35 / 4-10 / 3-4 |
| **FY2025 rendered pixels, `pdftoppm -r 200` p28, read as an image** | none | **15-40 / 8-35 / 4-10 / 3-4** |
| FY2024 filing p30, text layer and rendered pixels | PDF-XChange 10.4.3 | 15-40 / **8-30** / 4-10 / 3-4 |
| FY2023 filing, text layer | — | 15-40 / **8-30** / 4-10 / 3-4 |

**A column of lives has no arithmetic to foot against, so the footing test cannot arbitrate
it and the pixel route is not optional.** It is also the inverse of the case that taught the
lesson: there `-layout` silently dropped the Years column, here it is the route that carries
it and the plain extraction floats the figures away from their labels. Neither rendering of
one text layer is a second route.

## 3. The page foots — 78 tests, no break

Note 6 was footed in all three directions, both years, against its printed totals: every
movement row **across** to the Total column, every class column **down** from opening to
printed closing, and the identity **cost less accumulated equals net book** for all five
columns plus Total. Then two checks the note cannot mark itself on: the FY2025 opening row
against **the FY2024 filing's own printed closing row**, class by class, cost and
accumulated; and the year's charge against its allocation note on page 35
(408,732 + 36,611 + 4,040 + 1 = 449,384; and 456,370 + 64,438 + 3,307 + 1 = 524,116).

**No break anywhere.** So the figures are arbitrated by arithmetic and the lives by pixels.

## 4. What the prior years say, which is the sharpest evidence here

| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Buildings | 15 – 40 | 15 – 40 | 15 – 40 |
| Plant and machinery | 8 – 30 | 8 – 30 | **8 – 35** |
| Motor vehicles | 4 – 10 | 4 – 10 | 4 – 10 |
| Furniture, fixtures and equipment | 3 – 4 | 3 – 4 | 3 – 4 |

Three filings, three documents, three years. **Three of the four classes are identical to
the digit and exactly one figure moved** — the top of the plant-and-machinery range — which
is the reassessment the note describes and quantifies at both ends: a decrease in the charge
of **USD 90,335 thousand** in 2025, and an expected **USD 179,198 thousand in 2026**, applied
prospectively from 1 July 2025. The note also says lives rose "by up to an additional 10
years" while the disclosed class range top rose 5. **That tension is recorded and not
resolved**; the range is what the note discloses as policy.

## 5. The weighting, from note 6's own carrying amounts

The collapse is the **carrying-amount-weighted harmonic mean**, which is arithmetic rather
than a choice: maintenance is the sum of IC(class)/life(class), and the sanctioned builder
charges IC(total)/L, so the single life reproducing that charge is IC(total) divided by that
sum. An arithmetic mean would overstate the life and undercharge.

USD'000, 31 December 2025, from note 6's own columns:

| class | net book | gross cost | disclosed life |
|---|---:|---:|---|
| Buildings | 330,318 | 718,265 | 15 – 40 |
| Plant and machinery | 5,440,390 | 12,945,813 | 8 – 35 |
| Motor vehicles | 392 | 14,093 | 4 – 10 |
| Furniture, fixtures and equipment | 22,962 | 198,248 | 3 – 4 |
| **depreciable base** | **5,794,062** | **13,876,419** | |

| weight base | weighted life |
|---|---|
| FY2025 net book | **8.16 – 34.19 years** |
| FY2025 gross cost | **7.99 – 31.62 years** |
| FY2024 net book | 8.17 – 34.34 years |
| FY2024 gross cost | 8.00 – 31.64 years |
| FY2025 net book, on the *pre*-reassessment lives | 8.16 – 29.65 years |

**Stable across weight base and across years, and the band's width is not a weighting
artefact.** Plant and machinery is 93.9% of depreciable net book value and 93.3% of
depreciable gross cost, and contributes 95.8% of the charge at the short end and 91.7% at
the long end. **The band is that one class's own 8-to-35 range, and nothing else.**

## 6. Why no single life follows, and this time it is priced rather than asserted

Priced through the sanctioned builder on this study's own last explicit year (FY2030: NOPAT
1,208.8, book D&A 379.9, net property plant and equipment 5,716.3, net working capital
555.4, all USD mn), at the study's own published rate and the house pegged terminal of 2.0%
inflation with zero real growth — which is exactly the 2.0% nominal the study already
carries:

| capital base | life | outcome |
|---|---|---|
| study's net property, plant and equipment FY2030 — a **floor** on the charge | 8.16 y | builds: terminal 21,928, **−12.9%**, AED 2.2586/share |
| the same | 34.19 y | **REFUSED** — implied payout 116.7% of terminal profit |
| filed FY2025 depreciable **gross historical cost** — a base that still understates replacement | 8.16 y | **REFUSED** — terminal free cash flow −122.4 |
| the same | 34.19 y | builds: terminal 29,287, **+16.3%**, AED 2.9279/share |

**Two of four constructions refuse outright and the two that build straddle the published
terminal from −12.9% to +16.3%, on a terminal holding 76.7% of enterprise value.** A point
inside the band would therefore not be a rounding convenience; it would be the number that
decides the answer, and it would be this desk's number rather than the company's. **A life
this desk chose is not a disclosed life.** Stop and inform, SIGCM clause 8.

The payout refusal at the long end is the exemplar's own sentence in a polyolefins costume:
a terminal charging maintenance over 34 years while adding back a book charge struck on a
much shorter effective life adds back the amortisation of a cost it never charged. The
study's own explicit window carries net property, plant and equipment of 5,716.3 against a
book charge of 379.9 — a 15.05-year *remaining*-life figure, which the band brackets and
neither endpoint is near.

## 7. The measured-age route stays closed, and this is the clearest case for it in the book

Both [L-328] conditions sit in the same note, and the second is quantified at both ends:
depreciation writes off "cost **less estimated residual values**", and a life reassessed
**from 1 July 2025** makes the FY2025 charge half a year on the old lives and half on the
new. So accumulated depreciation over that charge is nine years of one basis divided by half
a year of another.

| the age the identity returns | denominator | years |
|---|---|---:|
| on the pre-change basis | the 2025 charge plus the 90,335 the change removed | **14.98** |
| on the charge actually reported | the blended 2025 charge of 449,384 | **17.99** |
| on the go-forward basis | approximately 360,521 | **22.42** |

**The same accumulated balance supports three ages spanning fifty per cent and nothing about
the assets moved.** The third row is approximate and is labelled so — it holds additions and
disposals still, as the disclosure itself does. Confirms the 5 September reading exactly.

## 8. One correction to the 5 September pass

That pass wrote that the disclosed-life route does not rescue this name because "a midpoint
of a range is a choice, not a disclosure, **and the identity that would weight them is the
one just broken**." The first half stands. **The second half conflates two different
identities and is wrong.** The broken one is *accumulated over the charge*, which measures
an age. The one that weights classes into a life is *IC(total) over the sum of
IC(class)/life(class)*, which needs only note 6's carrying amounts and note 3's disclosed
lives — no age, no residual, nothing the reassessment touched. **It was available all along
and is run in §5 above.**

The consequence was not cosmetic: because the weighting was believed unavailable, **the band
was never recorded, and the census went on reporting this name's life as "not sourced" when
its note discloses lives on four classes across three filings.** An absent answer wearing
the costume of a settled one. The conclusion is unchanged — no life is adopted — but the
sourcing state is not the same thing as the collapsing decision, and reporting the first as
the second hides research that has already been done.

## 9. Direction, stated because it does not resolve

This study's terminal carries the retired reinvestment identity: a replacement cycle of
**50.0 years against 1/g of 50.0**, charging 16.7% of terminal profit. **Fifty years is a
fact about the dirham's peg. The longest life this company discloses for any class is 40
years, for buildings, which are 5.7% of the depreciable base; the weighted band tops out at
34.19.** So the terminal assumes a life the accounts do not support anywhere, in the
direction that overstates value.

**That does not settle the sign of a rebuild and nothing here claims it does.** The priced
range spans both directions, and the central sits at AED 2.5543 against a spot of AED 2.3500
struck 3 September — a +8.7% gap, inside the audit trigger. Whether correcting the terminal
would move that toward the price or away from it is not knowable before the base is sourced,
and a correction that moved it away would not be a reason to reconsider the correction.

## 10. What would open it

- **A narrower disclosure for plant and machinery**, which is 93.9% of the base and whose
  own 8-to-35 range is the entire width of the band.
- **The residual values**, in aggregate or by class, which would reopen the identity route.
- **The FY2026 charge as reported** — the first full year on the new lives, which lands the
  go-forward denominator on the same basis as the accumulated column. One more reporting
  cycle makes the age route straightforwardly measurable, and that is a date rather than a
  hope.
- **A replacement-cost capital base at the terminal year**, which this study does not commit
  and which §6 had to bracket with a net-book floor and a historical-cost ceiling.

*Sourced band recorded in the disclosed-lives register; no life adopted, no terminal record
committed, no published figure moved.*
