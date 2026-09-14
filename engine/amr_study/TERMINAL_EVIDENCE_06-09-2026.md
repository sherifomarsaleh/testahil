# AMR — the disclosed useful life, sourced and verified independently, 6 September 2026

**Status: the lives ARE disclosed, foot, and weight. NO SINGLE MAINTENANCE LIFE IS AVAILABLE,
and the blocker is the base rather than the note.** This pass re-ran the 5 September work from
the filings rather than reading its conclusions, per the independence discipline. It CONFIRMS
that pass on every figure it re-measured, CORRECTS one claim in it, and CLOSES one test that
pass recorded as not run. **Nothing here changes a published number, a document or a central.**

## 1. The accounting-policies note, quoted exactly

Americana Restaurants International PLC, FY2025 consolidated financial statements, **note 2.5
Property and equipment**, page 17:

> "Land is not depreciated. Depreciation on other assets is calculated using the straight-line
> method, at rates calculated to reduce the cost of assets to their estimated residual value
> over their expected useful lives, as follows:"
>
> | | **Years** |
> |---|---|
> | Leasehold improvements and furniture | 5-7 |
> | Buildings | 7-20 |
> | Cold rooms | 5 |
> | Equipment and tools | 4-7 |
> | Vehicles | 4 |
>
> "Buildings comprise of construction-related amounts (20 years); electrical fitouts (10 years)
> and building extensions (7 years)."

Also disclosed: **note 2.6** investment-property buildings "useful lives ranging from 5 to 20
years"; **note 2.7** intangibles, which states its life two ways — see §5.

## 2. The route, and why the pixels had to arbitrate

**The FY2025 PDF's own text layer is an OCR product.** Its Producer string is ABBYY FineReader
14, so "text layer" here is not the filing's native typesetting and the extractor's confidence
is worth nothing. **The Years column has no arithmetic to foot against**, so the footing test
cannot arbitrate it and a second route is not optional.

| route | toolchain | what it gave |
|---|---|---|
| FY2025 text layer, `pdftotext -layout` p17 | ABBYY FineReader 14 | 5-7 / 7-20 / 5 / 4-7 / 4 |
| **FY2025 rendered pixels, `pdftoppm -r 200` p17, read as an image** | none | **5-7 / 7-20 / 5 / 4-7 / 4** |
| FY2024 filing p19, native text layer | Adobe PDF Library 24.5.175 | 5-7 / 7-20 / 5 / 4-7 / 4 |
| FY2023 filing p20, native text layer | Adobe PDF Library 23.8.246 | 5-7 / 7-20 / 5 / 4-7 / 4 |

Three toolchains, four reads, one set of five figures. **The lives are sourced.**

## 3. The page foots — 39 tests, no break

Note 5 was footed cell by cell in all three directions, both years, against the printed totals:
every movement row ACROSS to its printed Total (19 rows), every column DOWN from opening through
eight movement rows to the printed closing balance (14 columns), and the IDENTITY cost less
accumulated equals net book for all six classes plus Total. **No break.** Note 11 (leases) foots
too: both roll-forwards, the category table both years, and the lease-liability split both years.

**Cross-checked against a separate document.** The FY2024 standalone filing's own note 5 closing
column reproduces the FY2025 filing's opening row to the digit — 19,387 / 455,112 / 108,145 /
406,315 / 15,359 / 15,972 = 1,020,290, accumulated 321,134 / 90,549 / 267,912 / 11,934 =
691,529. Two documents, two toolchains, one set of figures.

## 4. The weighting, from note 5's own carrying amounts

The collapse is the **carrying-amount-weighted harmonic mean**, which is arithmetic rather than
a choice: maintenance is the sum of IC(class)/life(class), and `terminal_value.build()` charges
IC(total)/L, so the single life reproducing that charge is IC(total) divided by that sum. An
arithmetic mean would overstate the life and undercharge. Land and capital work in progress are
excluded — neither is depreciated.

US$'000, 31 December 2025, from note 5's own columns:

| class | net book | gross cost | disclosed life |
|---|---|---|---|
| Leasehold improvements and furniture | 138,575 | 494,100 | 5-7 |
| Buildings and cold rooms | 18,348 | 113,262 | **7-20 and 5, one column** |
| Equipment and tools | 144,503 | 456,370 | 4-7 |
| Vehicles | 3,159 | 14,955 | 4 |
| **depreciable base** | **304,585** | **1,078,687** | |

| weight base | weighted life |
|---|---|
| FY2025 net book amount | **4.46 – 7.23 years** |
| FY2025 gross cost | **4.51 – 7.43 years** |
| FY2024 net book amount | 4.46 – 7.22 years |
| FY2024 gross cost | 4.52 – 7.44 years |

Stable across weight base and across years. **It stays a band and is not collapsed further**:
both endpoints are figures the note prints, and picking a point inside 5-7 or 4-7 would be this
desk choosing a life under cover of a citation.

**The one class the note does not split is bounded and small.** Buildings (7-20) and cold rooms
(5) share a single carrying-amount column, 6.02% of net book and 10.50% of gross cost. Moving
ALL of it to cold rooms gives 4.46–6.78; ALL to buildings gives 4.53–7.23 — at most 6.1%, well
inside the spread the other classes' own ranges already produce. That is the difference from the
exemplar's dry-docking case, where the unsplit component drove the answer and could not be
bounded.

## 5. Why no single maintenance life follows: the base is 62% right-of-use

At the terminal year the study's own committed capital base is

    invested capital 904.5 = owned assets 485.7 + right-of-use 789.4 + working capital (370.6)

so **right-of-use is 61.9% of the gross capital base and 68.7% of terminal book depreciation**
(268.5 of 390.6). **Note 2.5 does not govern right-of-use assets at all**, and the filing gives
no substitute:

- the policy is "the shorter of the asset's useful life and the lease term", against rental
  contracts "typically made for fixed periods of **1 to 25 years**". A 1-to-25 range is not a life.
- **note 11's roll-forward is NET** — additions less depreciation. There is no gross cost column
  and no accumulated depreciation column, so the cost-over-charge identity that gives a life for
  property and equipment **cannot be formed at all**. Net book over charge gives 2.97 years,
  which is a *remaining* life, not a useful life.

And the owned leg is not purely note 2.5 either: at FY2025 it is PPE 341.4 + intangibles 63.3 +
investment property 3.7, so **note 2.5 governs 83.6% of the owned leg and about 32% of the
terminal gross capital base.**

## 6. What the sanctioned builder does with it

| construction | outcome |
|---|---|
| study's own real growth 0.98%, disclosed life | REFUSED — real growth stated with no incremental capital |
| whole invested capital 904.5, life 4.46 / 4.51 / 7.23 / 7.43 | REFUSED — implied payout 143.7% / 144.2% / 161.1% / 161.9% |
| owned assets at net book 485.7, life 4.51 / 7.43 | REFUSED — implied payout 104.9% / 114.4% |
| life 12.43 (the identity's), no disclosure behind it | REFUSED — SIGCM clause 1 |
| **owned leg at gross historical cost 1,078.7, life 4.51 / 7.43** | **builds: 4,456.6 / 5,700.3** |

The payout refusals are the exemplar's sentence in a restaurant's costume: **a terminal charging
only the property-and-equipment life while adding back all book depreciation adds back the
amortisation of a cost it never charged** — here two thirds of it, the depreciation of leased
restaurants whose renewal cost is rent and whose liability the model already carries as debt.

## 7. The measured-age route stays closed, and the test flagged unrun is now run

Note 2.5 depreciates "to their estimated residual value", which is [L-328] condition (i): the
depreciable amount is cost less a residual, so accumulated over the charge overstates the age.
Condition (ii) is **not** evidenced — no change-in-estimate disclosure appears in the FY2025
statements, unlike four of the other names tried.

[L-328]'s overturning condition is a residual small enough to be immaterial, evidenced by a class
whose accumulated depreciation reaches substantially all of its cost while still in use. **That
test was recorded as not run on 5 September. It is run here and it FAILS:**

| class | % written down | cost/charge implies | disclosed |
|---|---|---|---|
| Leasehold improvements and furniture | 72.0% | 12.20 y | 5-7 |
| Buildings and cold rooms | 83.8% | 23.41 y | 5-20 |
| Equipment and tools | 68.3% | 11.36 y | 4-7 |
| **Vehicles** | 78.9% | **11.75 y** | **4** |

The highest is 83.8% — none reaches substantially all of its cost — and **the filing quantifies
no residual anywhere**, only the boilerplate that residuals are reviewed annually. The route stays
closed. The sharpest corroborator is the one class carrying **no range at all**: vehicles at a
disclosed life of exactly 4 years against an implied 11.75, a factor of 2.9. The charge is not
cost/life. **That is a reason the disclosed life may understate the true replacement cycle; it is
not a licence to lengthen it.** A life this desk chose is not a disclosed life.

## 8. One correction to the 5 September pass

That pass recorded that the plain text layer "dropped the *Software 5 years* line silently and
carried 10-20 years alone". **Measured here, it does not.** `pdftotext` without `-layout` on page
18 carries **both** figures — but detaches them from their row labels entirely and floats the
bare pair "10-20 years / 5 years" into the middle of the *next* section, 2.8 Financial assets.
The defect is real and arguably worse (a value under the wrong heading rather than a value
missing), but it is a different defect, and the reason for the pixel route is restated rather
than weakened. The underlying disclosure problem stands: **note 2.7 states the intangibles life
twice and the two disagree** — prose "estimated useful life of 5 to 10 years" against a table
reading "Franchises and agencies 10-20 years, Software 5 years". Recorded, not resolved.

## 9. Direction, stated because it runs the wrong way

The one construction that builds — owned leg, gross historical cost, owned depreciation added
back — gives 4,456.6 at 4.51 years and 5,700.3 at 7.43 against the study's 6,167.9: **-27.7% to
-7.6% on a terminal holding 74.2% of enterprise value.** It is a **ceiling, not an answer**:
historical cost understates replacement cost, and 1,078.7 is a 31-December-2025 base against an
FY2030 flow, so the true charge is heavier and the terminal lower still.

AMR's committed central of AED 2.1455 already sits 3.8% **below** its committed spot of 2.23.
This correction points **down**, further below the price, on every construction that builds.
That is the direction and it is reported as it came out. **A correction that moves the answer
away from the price is not a reason to reconsider the correction.**

## 10. What would open it

- **A disclosed life for the right-of-use base**, or a decision — which is a construction and
  belongs in a rebuild with a ledger — that lease renewal is occupancy cost rather than capital
  maintenance, in which case the terminal's base is the owned leg and §4's band is the life it needs.
- **A replacement-cost owned capital base at the terminal year**, which the study does not commit.
- **The intangibles life**, which note 2.7 states two ways.
