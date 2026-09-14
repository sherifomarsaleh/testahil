# AMR — the terminal, tested briefly, and what is actually wrong with this study

**Status: STOPPED on the terminal, 5 September 2026 — and the terminal is not this study's
most pressing defect.** Fourth of the five names still carrying the retired construction to
be re-tested today, and the fourth to stop.

## The terminal

It carries the reinvestment identity, whose implied replacement cycle is 1/g — **33.3 years
at a 3.0% terminal** — against a company whose own note gives useful lives of **four to
twenty years**, and mostly four to seven. The charge it levies is 10.0% of terminal profit,
which on those lives is far too light: this is a business of cold rooms, vehicles, equipment
and fit-outs, not a fifty-year plant.

**The measured-age route is closed by [L-328] condition (i).** Note 2:

> *"Depreciation on other assets is calculated using the straight-line method, **at rates
> calculated to reduce the cost of assets to their estimated residual value** over their
> expected useful lives"*

Condition (ii) is NOT evidenced here — no change-in-estimate disclosure was found in the
FY2025 statements, which is worth recording because the previous three names all carried
one. One broken condition is enough: where the depreciable amount is cost less a residual,
accumulated depreciation over the charge overstates the age by an amount the accounts do not
disclose.

**And here, unusually, the residual might genuinely be immaterial** — which is [L-328]'s own
stated limit, and the reason this file says "stopped" rather than "impossible". Vehicles at
four years, cold rooms at five and equipment at four to seven do not usually carry large
scrap values. If any class's accumulated depreciation reached substantially all of its cost
while the assets remained in use, that would bound the residual near zero and the identity
would be usable. **That test was not run**, because of what follows.

## What is actually wrong with this study, and it is larger

`engine/prices/gap_today.py` reports AMR as **unreadable**: its committed numbers expose no
central-and-spot pair the valuation-gap gate can find. The figures are there — the file
carries a spot and a central — but under keys the shared reader does not recognise, so
[R-GAP-01] cannot audit this study at all and [R-GAP-02] cannot decide whether it may
publish. **An unreadable study is not a clean study**, and it is held for exactly that
reason.

It shares that state with two of the other names looked at today, ADNOCDIST and BOROUGE, and
with five more. Making a study readable to the shared reader is a smaller job than a terminal
rebuild and it unblocks a gate that currently says nothing about eight of them — **which is
the better next piece of work on this name, and probably on the group.** Recorded here rather
than acted on now, because it is a decision about sequencing that belongs in the programme
state rather than inside one study's evidence file.

## What would open the terminal

- **The residual values**, or any class whose accumulated depreciation reaches substantially
  all of its cost while still in service, which would bound them near zero.
- Either would make this one of the easier names in the census rather than one of the
  blocked ones, because its disclosed lives are short, specific and mostly unranged
  (buildings break down explicitly into construction 20 years, electrical fit-outs 10 and
  extensions 7).

---

# Second pass, 5 September 2026 — the lives ARE sourced and weightable; the terminal still refuses, for a different reason

The pass above stopped on the MEASURED-AGE route ([L-328] condition (i)) and did not attempt the
weighting. This pass attempts it. **The disclosed lives are sourced, footed on three independent
routes, and weight cleanly into a band. The single maintenance life the terminal needs is still
unavailable, and the blocker is not the one the pass above expected.**

## 1. The accounting-policies note, quoted exactly

Americana Restaurants International PLC, FY2025 consolidated financial statements (audited by
Deloitte & Touche (M.E.) LLP, signed 6 February 2026), **note 2.5 Property and equipment**, page 17
of the PDF:

> "Land is not depreciated. Depreciation on other assets is calculated using the straight-line
> method, at rates calculated to reduce the cost of assets to their estimated residual value over
> their expected useful lives, as follows:"
>
> | | **Years** |
> |---|---|
> | Leasehold improvements and furniture | 5-7 |
> | Buildings | 7-20 |
> | Cold rooms | 5 |
> | Equipment and tools | 4-7 |
> | Vehicles | 4 |
>
> "Buildings comprise of construction-related amounts (20 years); electrical fitouts (10 years) and
> building extensions (7 years)."
>
> "The Group depreciates leasehold improvements and furniture, over the useful life of the assets."

Also disclosed, and both belong to the same owned base: **note 2.6** investment-property buildings
"useful lives ranging from 5 to 20 years"; **note 2.7** intangibles — see §5, which is a defect.

**FY2024 and FY2023 carry this table verbatim**, same five classes, same five figures, same
buildings breakdown. The one wording change is in the sentence after the table: FY2024 and FY2023
read "over the **lower of** the useful life of the assets **or the property lease term**", FY2025
drops the lease-term cap. The Years table is unchanged either way; recorded because leasehold
improvements are 45.5% of the depreciable net book amount and the cap that was dropped is the one
that would have shortened them.

## 2. The route, and why it needed three

**The FY2025 PDF's own text layer is an OCR product** — its Producer string is ABBYY FineReader 14,
so "text layer" here is not the filing's native typesetting and the extractor's confidence is worth
nothing. Three routes were run and all three agree:

| route | what it gave |
|---|---|
| FY2025 text layer, `pdftotext` without `-layout` | 5-7 / 7-20 / 5 / 4-7 / 4 |
| FY2025 rendered pixels, `pdftoppm -r 200` page 17, read as an image | 5-7 / 7-20 / 5 / 4-7 / 4 |
| FY2024 and FY2023 filings, native Adobe text layers (not OCR) | 5-7 / 7-20 / 5 / 4-7 / 4 |

The third route is the one that does the work: the Years column has **no arithmetic to foot
against**, so a footing test cannot arbitrate it, and two filings produced by a different toolchain
in different years reproducing the same five figures is the only check available. It passes.

## 3. The page foots, in both directions, on every block

Note 5 (property and equipment) and note 11 (leases) were footed cell by cell — every column down,
every row across, both years, against the printed totals. **No break.**

| block | test | result |
|---|---|---|
| PPE cost 31-Dec-2025 | six classes sum to 1,118,072 | foots |
| PPE accumulated depreciation | four classes + CWIP sum to 776,667 | foots |
| PPE net book amount | six classes sum to 341,405 | foots |
| PPE, per class | cost less accumulated equals net book, all six | foots |
| PPE charge for the year | four classes sum to 86,788 | foots |
| PPE roll-forward | all eight movement rows across all seven columns | foots |
| PPE FY2024 comparative | closing cost 1,020,290, net book 328,761, charge 81,466 | foots |
| ROU roll-forward, both years | to 610,822 and 566,054 | foots |
| ROU by category and its charge | to 610,822 and 205,566 | foots |

**Cross-checked against a separate document**: the FY2024 comparative column inside the FY2025
filing reproduces the FY2024 standalone filing's own note 5 to the digit — 455,112 / 108,145 /
406,315 / 15,359 / 15,972 / 1,020,290, leasehold charge 39,817. Two documents, two toolchains, one
set of figures.

## 4. The weighting, from the note's own carrying amounts

The collapse is the **carrying-amount-weighted harmonic mean**, and that is arithmetic rather than a
choice: a maintenance charge is the sum of IC(class)/life(class), so the single life reproducing it
is IC(total) divided by that sum. An arithmetic mean would overstate the life and undercharge.
Land and capital work in progress are excluded — neither is depreciated.

US$'000, 31 December 2025, from note 5's own columns:

| class | net book | gross cost | disclosed life |
|---|---|---|---|
| Leasehold improvements and furniture | 138,575 | 494,100 | 5-7 |
| Buildings and cold rooms | 18,348 | 113,262 | **7-20 / 5, one column** |
| Equipment and tools | 144,503 | 456,370 | 4-7 |
| Vehicles | 3,159 | 14,955 | 4 |
| depreciable base | **304,585** | **1,078,687** | |

| weight base | weighted life |
|---|---|
| FY2025 net book amount | **4.46 – 7.23 years** |
| FY2025 gross cost | **4.51 – 7.43 years** |
| FY2024 net book amount | 4.46 – 7.22 years |
| FY2024 gross cost | 4.52 – 7.44 years |

Stable across weight base and across years. **It stays a band and it is not collapsed further**:
both endpoints are figures the note prints, and picking a point inside 5-7 or 4-7 would be this desk
choosing a life under cover of a citation.

**The one class the note does not split does not block it.** Buildings (7-20) and cold rooms (5)
share a single carrying-amount column. That column is 6.02% of the depreciable net book amount and
10.50% of gross cost; moving all of it to cold rooms or all of it to buildings moves the weighted
life by at most 6.6%, entirely inside the spread the other classes' own ranges already produce. That
is the difference from the exemplar's dry-docking case, where the unsplit component drove the answer
and could not be bounded. Here it is bounded and small.

**What does not corroborate, and it is the note's own arithmetic saying so.** Depreciable gross cost
over the year's own charge implies 12.43 years (FY2024: 12.09) against a disclosed-class weighting
of 4.5-7.4. Vehicles is the sharpest case because it carries **no range at all**: a disclosed life of
exactly 4 years against an implied 11.75. The charge is therefore not cost/life, which is
[L-328] condition (i) confirmed by arithmetic as well as by the note's own residual-value wording,
and the base is 71.8% written down with an apparent age of 8.92 years — longer than the disclosed
life it is supposedly being depreciated over. Assets are outliving their book lives and still sitting
in the cost column. **That is a reason the disclosed life may understate the true replacement cycle;
it is not a licence to lengthen it.** A life this desk chose is not a disclosed life.

## 5. Why the terminal still refuses: the base is 62% right-of-use

The study capitalises leases (its own framing note: "the lease liability is debt, right-of-use
depreciation is in depreciation and amortisation"). At FY2030 its terminal capital base is

    invested capital 904.5 = owned assets 485.7 + right-of-use 789.4 + working capital (370.6)

so **right-of-use is 61.9% of the gross capital base and 68.7% of terminal book depreciation**
(268.5 of 390.6). Note 2.5 does not govern right-of-use assets at all. What the filing discloses
for them is:

- policy: "Rental contracts are typically made for fixed periods of **1 to 25 years**" and
  right-of-use assets are depreciated "over the shorter of the asset's useful life and the lease
  term". A 1-to-25 range is not a life.
- note 11's roll-forward is **net** — additions less depreciation. There is **no gross cost column
  and no accumulated depreciation column**, so the cost-over-charge identity that gives a life for
  property and equipment cannot be formed at all. Net book over charge gives 2.94 years, which is a
  *remaining* life, not a useful life.
- the lease-liability maturity ladder in note 3.1(c) is three coarse undiscounted buckets
  (212,414 / 386,470 / 175,388). A weighted term could be manufactured from it by picking a midpoint
  for "later than five years". That is picking a number.

Run against the sanctioned builder, every construction on the whole base refuses, and the refusal is
the exemplar's own:

| construction | outcome |
|---|---|
| study's own real growth 0.98%, disclosed life | REFUSED — real growth stated with no incremental capital |
| whole invested capital, life 4.51 / 7.43 | REFUSED — implied payout 144.2% / 161.9% |
| owned assets at net book, life 4.51 / 7.43 | REFUSED — implied payout 104.9% / 114.4% |
| life supplied with no source | REFUSED — SIGCM clause 1 |

The payout refusals are the exemplar's sentence in a restaurant's costume: **a terminal charging
only the property-and-equipment life while adding back all book depreciation adds back the
amortisation of a cost it never charged** — here two thirds of it, the depreciation of leased
restaurants whose renewal cost is rent and whose liability the model already carries as debt.

**A second, smaller disclosure defect in the same base.** Note 2.7 states the intangibles life twice
and the two disagree: the prose says "estimated useful life of **5 to 10 years**", the table beneath
it says **Franchises and agencies 10-20 years, Software 5 years**. The intangibles sit inside the
owned base the study depreciates. Recorded, not resolved. *The plain text layer dropped the
"Software 5 years" line silently and carried "10-20 years" alone* — the same silent column drop
already recorded against the note 5 table, found on a second table in the same document, and the
reason the pixel route was run rather than trusted around.

## 6. Direction, stated because it runs the wrong way

The one construction that builds — the owned leg only, on the company's own **gross historical** PPE
cost of 1,078.7 with owned depreciation added back — gives a terminal of 4,456.3 at 4.51 years and
5,700.0 at 7.43, against the study's 6,167.9: **-27.7% to -7.6% on a terminal holding 74.2% of
enterprise value**, roughly -21% to -6% on enterprise value. It is a **ceiling, not an answer**:
historical cost understates replacement cost, and 1,078.7 is a 31-December-2025 base against an
FY2030 flow, so the true charge is heavier and the terminal lower still.

AMR's committed central of AED 2.1455 already sits 3.8% **below** its committed spot of 2.23. This
correction points **down**, further below the price, on every construction that builds. That is the
direction and it is reported as it came out. A correction that moves the answer away from the price
is not a reason to reconsider the correction.

## 7. What would open it

- **A disclosed life for the right-of-use base**, or a decision — which is a construction and
  belongs in a rebuild with a ledger — that lease renewal is occupancy cost rather than capital
  maintenance, in which case the terminal's base is the owned leg and this record's 4.46-7.43 band
  is the life it needs.
- **A replacement-cost owned capital base at the terminal year**, which the study does not commit.
  The [R-FCAL-01] valuation-input block is where it belongs.
- **The intangibles life**, which note 2.7 states two ways.

Nothing in this pass changed a published number, a document or a central.
