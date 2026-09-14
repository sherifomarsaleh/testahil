# STC — the disclosed useful life, sourced from outside the study

**6 September 2026.** An independent sourcing of the asset life [R-TERM-01] needs, run
against the filings on disk rather than against the study's own record. It CHANGES NO
PUBLISHED NUMBER: the committed terminal is reproduced, not rebuilt. Where it extends
`TERMINAL_EVIDENCE_05-09-2026.md` that is said; that file is dated and is not rewritten.

## 1. What the accounting-policies note actually discloses

Note 10 of the FY2025 audited consolidated statements, under the roll-forward, states:

> Property and equipment are depreciated using the following estimated useful lives:
> **Buildings 25 - 50 years** · **Telecommunication network and equipment 3 - 30 years** ·
> **Other assets 2- 20 years**

Method, note 4.11:

> *"Depreciation is charged using **mainly** the straight-line method over the estimated
> useful lives of property and equipment, other than land."*

**These are RANGES. The note discloses no single life for any class, and none for the
group.** A midpoint is a life this desk chose, which SIGCM clause 1 does not permit.

## 2. The page foots — 25 checks, both directions, no OCR needed

Every filing carries a real text layer. The FY2025 note was footed vertically (each class's
cost and accumulated roll-forward), horizontally (each row across the four classes) and on
the identity net book value = cost less accumulated, for both the FY2025 column and the
FY2024 comparative: **25 of 25 reproduce to the riyal, zero difference on every one.** The
FY2024 filing's own note and the FY2023 filing's own note were footed the same way and also
reproduce exactly. Arithmetic is the arbiter and it agrees at every point, so the text layer
is the route and no pixel re-read was required.

Route recorded: **text layer** (`pdftotext -layout`), FY2025 pp.57-58, FY2024 p.59, FY2023 p.54.

## 3. Weighting the classes into one maintenance life

The note discloses the split — cost, accumulated depreciation, the year's own charge and net
book value, for all three depreciable classes. Land (SAR 1,996,000 thousand, note 10(1)) and
capital work in progress (4,910,376) come out of the depreciable base; 134,634,729 + 1,996,000
+ 4,910,376 reproduces the stated cost of 141,541,105.

**Route A — weighting the DISCLOSED RANGES by the note's own amounts gives a range, not a
life.** On the maintenance-equivalent basis (the single life reproducing the sum of each
class's cost over its own life) the three ranges weight to **3.21 - 30.28 years** on gross
cost, or 3.37 - 30.81 on net book value. That is a 9.4x span, and it prices to a 33-point
spread on the terminal. Collapsing it to a point requires choosing a position inside each
class's range. **That route is refused.**

**Route B — the identity, off the note's own columns.** Depreciable gross cost over that
class's own charge is the weighted life by identity, not by assumption:

| class | depreciable cost | the year's charge | implied life | disclosed range | inside |
|---|---:|---:|---:|:---:|:---:|
| Lands and buildings (ex land) | 15,700,925 | 475,018 | 33.05 y | 25 - 50 | yes |
| Telecommunication network and equipment | 108,848,482 | 5,481,822 | 19.86 y | 3 - 30 | yes |
| Other assets | 10,085,322 | 496,503 | 20.31 y | 2 - 20 | **no** |
| **TOTAL** | **134,634,729** | **6,453,343** | **20.86 y** | 3.21 - 30.28 | yes |

**The single maintenance life is the COST-WEIGHTED HARMONIC mean, 20.86 years, and the
distinction is not pedantry.** Maintenance is the sum of each class's cost over its own life,
so the one life reproducing it is total cost over total charge. The cost-weighted ARITHMETIC
mean of the same three lives is 21.43 years and under-charges maintenance by SAR 170,654
thousand a year — 2.6% on the life, in the direction that flatters the value.

**Weights are gross cost, not carrying amount, and that is deliberate**: an asset 90% written
down still costs full price to replace, so net book value is the wrong base for a replacement
charge. Both weightings are shown above; the range they produce differs by under 2%.

## 4. What the per-class split shows that the pooled figure hides

**Other assets' implied life of 20.31 years sits ABOVE the top of its own disclosed range of
2 - 20.** This is the one internal disagreement in the note, and it is informative rather
than fatal. Its most likely mechanism is assets fully written off, still carried in cost and
no longer charged, which is consistent with 69.2% of that class already depreciated — and it
is exactly the bias `terminal_value.py` records against the age identity ("slightly
OVERSTATED where assets sit fully depreciated and still in use, which errs toward charging
more"). **Bounded: capping that class at its own disclosed 20 years moves the pooled life
from 20.86 to 20.84, -0.12%.** Immaterial, and it says the identity reads marginally LONG.

## 5. [L-328]'s three conditions, checked on the policy note first

**(i) Residual value — CLEAR.** Note 4.11 depreciates "over the estimated useful lives",
with nothing deducted. The FY2025 document contains exactly three occurrences of "residual
value": the IAS 16 annual-review sentence at note 4.11, lease **residual value guarantees**,
and an investment-property **valuation technique**. No residual enters the depreciable amount
and none is quantified. This is the condition that failed on three of the five names tried
before it.

**(ii) A life reassessed mid-life — CLEAR, and now with affirmative evidence rather than an
absence.** Note 5.2.2 carries only boilerplate. What settles it is a footnote the FY2024
filing puts on its own life table: the ranges DID change between FY2023 (buildings **10** -
50, other assets **3** - 20) and FY2024 (25 - 50, **2** - 20), and the filing states why —

> *"(*) Range has been updated to reflect the impact of deconsolidating discontinued
> operations (Note 14.1)."*

**That is a change in the population, not a reassessment of any surviving asset's life**,
which is precisely the distinction the condition turns on. Recorded here because a range that
moves looks like a reassessment until the filing says otherwise.

**(iii) A base assembled by business combination — CLEAR.** FY2025 acquisitions add SAR 9,898
thousand of cost against 141,541,105, **0.007%**, and 4,304 of accumulated against a charge of
6,453,343, **0.07%**. Nothing resembling the acquired-history problem that makes the ratio
meaningless elsewhere.

**A fourth qualification, unquantified and recorded rather than resolved.** Note 4.11 says
"**mainly** the straight-line method". Both identities are exact only under straight line.
The FY2025 document names no other method for property and equipment anywhere — every other
depreciation-method sentence in it concerns leases, right-of-use assets or intangibles — so
the exposure is small and undisclosed. Its direction is unknown, which is why it is written
down rather than adjusted for.

## 6. Cross-check against the prior years' identical tables

| | depreciable cost | charge | implied life | measured age | depreciated share |
|---|---:|---:|---:|---:|---:|
| FY2025, FY2025 filing | 134,634,729 | 6,453,343 | **20.86 y** | 15.23 y | 73.0% |
| FY2024, FY2024 filing (as reported) | 130,697,817 | 6,600,613 | 19.80 y | 14.37 y | 72.6% |
| FY2024, FY2025 filing (comparative) | 130,697,817 | 6,690,097 | 19.54 y | 14.18 y | 72.6% |
| FY2023, FY2023 filing (as reported) | 135,611,856 | 6,834,977 | 19.84 y | 13.60 y | 68.5% |
| FY2023, FY2024 filing (comparative) | 136,217,457 | 6,834,977 | 19.93 y | 13.60 y | 68.2% |

Three filed years hold the life inside **19.5 - 20.9 years**, a 6.8% spread, and the measured
age moves the way a year passing should: 13.60 → 14.18 → 15.23.

**The FY2024 charge is filed twice at two values** and this is recorded because point-in-time
discipline needs it: 6,600,613 as originally reported against 6,690,097 in the FY2025
comparative. The 89,484 difference is offset exactly in the transfers line (+67,242 against
-22,242) and both routes reach the identical closing accumulated of 94,847,791, so it is a
reclassification between two lines of one note rather than a restated charge. It moves that
year's implied life by 1.3%, 19.80 against 19.54, and both sit inside the band. The earlier
record quotes 19.54 without noting the pair exists.

## 7. What this prices, and it changes nothing

Reproduced through `terminal_value.build()`, the committed record rebuilds exactly. **The
life is not what drives this terminal**: the basis is book depreciation escalated to current
cost over the **MEASURED age of 15.23 years**, an identity off the same note, so the 20.86
life stands as the record and the corroborating cross-check rather than as the charge.

| basis for the escalation | maintenance | terminal free cash flow | terminal value | vs committed |
|---|---:|---:|---:|---:|
| measured age 15.23 y — **committed** | 15,461 | 11,112 | 184,812 | — |
| half the FY2025 identity life, 10.43 y | 14,061 | 12,512 | 208,101 | +12.6% |
| half the FY2024 life, 9.77 y | 13,877 | 12,695 | 211,153 | +14.3% |
| half the FY2023 life, 9.92 y | 13,919 | 12,653 | 210,456 | +13.9% |
| disclosed ranges, fast end, 3.21 y | 11,806 | 14,767 | 245,606 | +32.9% |
| disclosed ranges, slow end, 30.28 y | 15,435 | 11,138 | 185,249 | +0.2% |

**The disclosed ranges span 33 points of terminal value, which is the whole argument for the
identity** — and the committed construction sits at the conservative end of everything above.

**No direction is predicted for a rebuild and none is implied here.** [R-TERM-01 CLAUSE TWO
CORRECTED] is explicit that the sign is measured per name and never read off a ratio, on the
evidence of a name that read 0.26x and came out roughly 5% higher.

## 8. The honest limitation on the cross-check itself

`terminal_value.py` prescribes comparing the identity's implied life against the life the
disclosed class rates weight to, and on one name that comparison fired at +48% and stopped a
wrong number shipping. **Here it cannot fire.** The disclosed band is 3.21 - 30.28 years and
would contain almost any answer; 20.86 sitting inside it is close to no evidence at all. What
does the work on this name is the policy note read directly — which is the order
`terminal_value.py` insists on, the note being the test and the arithmetic a corroborator
that works only sometimes.

The note's line is "Depreciation **and impairment**" with no separate impairment figure, so
both identities carry whatever impairment sits inside the charge. Its direction is known:
impairment inflates the denominator, which shortens the life and the age, which under-states
the escalation to current cost and over-states the value. The charge series is smooth
(6,834,977 → 6,690,097 → 6,453,343, changes of -2.1% and -3.5%), so no material impairment
spike is visible, and the depreciated share of 73.0% — which carries no charge in it at all —
is what independently establishes that the base is old.
