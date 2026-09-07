# ADNOCDIST — the terminal, the evidence gathered, and why it stops here too

**Status: STOPPED, on the accounts' own words, 5 September 2026.** Written so the next
session does not re-derive a closed route.

## What is wrong

The terminal carries the retired reinvestment identity. Its implied replacement cycle is
1/g — **66.7 years at a 1.5% terminal** — against a base the company's own note turns over
in about twenty-four. That is a fact about the dirham's peg and not about a fuel-retail
network. The charge it levies is 6.0% of terminal profit, the lightest in the book, and per
[R-TERM-01 CLAUSE TWO] the defect runs the OPTIMISTIC way in a pegged market: correcting it
would be expected to LOWER this value, not raise it.

Expected, not predicted. [R-TERM-01 CLAUSE TWO CORRECTED] is explicit that the sign is
measured per name and never read off the ratio, so nothing here claims to know the
direction before a rebuild runs.

## The fixed-asset note, which is fully extracted and clean

Note 5 gives cost and accumulated depreciation by class with a complete roll-forward, and
the arithmetic foots. Capital work in progress is removed from both years because it does
not depreciate — its accumulated column is empty and its charge line is nil.

| | FY2025 | FY2024 |
|---|---:|---:|
| cost, total (AED'000) | 15,205,099 | 14,191,580 |
| less capital work in progress | (1,153,329) | (985,253) |
| **depreciable gross cost** | **14,051,770** | **13,206,327** |
| the year's own charge | 594,222 | 602,186 |
| accumulated depreciation | 7,172,902 | 6,639,402 |
| implied life, gross over charge | 23.65 y | 21.93 y |
| naive age, accumulated over charge | 12.07 y | 11.03 y |
| half the implied life | 11.82 y | 10.97 y |

**This base looks like a textbook steady state** — the naive age sits within three per cent
of half the implied life in both years, which is exactly what a uniform-vintage base should
do and the opposite of EGCH's young plant or RIYADHCABLE's. On the arithmetic alone the
measured age would be worth almost nothing here, and the half-life assumption the shared
construction already makes would be very nearly right.

## And the accounts close the route anyway, twice over

**[L-328] condition (i), the residual value.** Note 3.10:

> *"Depreciation is calculated using the straight-line method to allocate their cost **to
> their residual values** over their estimated useful lives"*

So the annual charge is (cost less residual) over life, not cost over life. Both the implied
life and the naive age above are therefore **overstatements** rather than measurements, and
by an unknown amount, because the residual is not disclosed.

**[L-328] condition (ii), the reassessment — and here it is not a policy sentence, it is an
event with a number on it.** Under "Changes in Judgements":

> *"The Group has **revised the estimated useful lives** of its assets, currently classified
> as property, plant and equipment with a carrying value of AED 5,347,053 thousand. This
> change in estimate has been applied in current year and prospectively and resulted in a
> **lower depreciation charge by AED 90,917 thousand** during the year ended 31 December
> 2025."*

That is **15.3% of the year's entire charge**, on assets carrying two-thirds of the net
book value, applied prospectively — so the FY2025 charge is not the charge that produced
the accumulated balance sitting above it. On the prior basis the charge would have been
685,139 and the same accumulated column would give an age of **10.47 years against the
12.07 the current charge implies**: a 15% swing in the measured quantity from an accounting
estimate rather than from anything about the assets. The disclosed ranges moved with it —
buildings 15–30 to 15–50, furniture 5–10 to 4–15, pipelines 10–40 to 10–50.

**A ratio whose numerator and denominator were struck on different bases is not a
measurement of anything**, and this is the cleanest example of condition (ii) in the book,
because the company quantified the break itself.

## Why the disclosed-life route does not rescue it

`terminal_value.build()`'s `disclosed_life` basis needs a life AND a replacement-cost
capital base. The note publishes RANGES per class and no weighting — 15–50 for buildings,
5–30 for plant, 5–20 for vehicles, 4–15 for furniture and computers, 10–50 for pipelines —
and taking a midpoint of a range is a choice, not a disclosure. The identity that would
supply a weighted life is the gross-over-charge one above, which the residual-value policy
has just broken. And the replacement-cost base needs an escalation from historical cost,
which needs an age. **Every route runs back through the same missing number.**

So no life is adopted and no age is assumed. Stop and inform, SIGCM clause 8. The name stays
on the ratchet with its reason.

## What would open it

- **The residual values**, in aggregate or by class. With those disclosed, both identities
  work again on (cost − residual) and this name becomes straightforward.
- **A pre- and post-reassessment charge by class**, which the AED 90,917 disclosure gets
  close to but does not give: it names the carrying value affected and the total effect,
  not the split.
- Neither is in the FY2025 audited statements, the FY2025 management discussion, the FY2025
  results presentation or the 2025 integrated report held in this directory. That is a
  statement about what was searched.

## The general form, which is not about fuel retail

**The measured-age route is the exception, not the rule, and it is now measured rather than
asserted.** Of the names it has been tried on, it works where a company writes off cost with
no residual mentioned and fails where the depreciable amount is cost less a residual — and
residual-value depreciation is the ordinary IFRS presentation. The two names it has just
failed on could hardly be less alike: an ocean fleet whose scrap steel is a real residual,
and a fuel-retail network whose residual is a piece of accounting policy. **Read the policy
note first. The arithmetic corroborates, and only sometimes** ([L-328]).

---

## Second pass, same day: independently re-sourced, stop confirmed, and one defect found

Run from the filings rather than from the section above, so the agreement is evidence
rather than a copy. **Every figure in the fixed-asset table above reproduces cell for
cell** — depreciable gross cost 14,051,770 and 13,206,327, the charge 594,222 and 602,186,
accumulated depreciation 7,172,902 and 6,639,402, the implied life 23.65 y and 21.93 y, the
naive age 12.07 y and 11.03 y, and the prior-basis charge of 685,139 giving 10.47 y. **The
stop stands, on the same two conditions.** Four things this pass adds.

### 1. The shared lives register was a year stale, and it is corrected

`engine/valuation_calibration/disclosed_lives.json` read **5–40 years** for this name and
cited the **FY2024** audited statements; the census printed that. It was not wrong about
FY2024 — that filing carries one column and it says 15–30 / 5–30 / 5–20 / 5–10 / 10–40,
confirmed by opening it, which is also this pass's prior-year cross-check and it matches
the comparative column in the FY2025 note exactly. It was **stale**: the FY2025 audited
statements sit in this directory and revise three of the five classes **upward**. On the
current filing the span is **4–50**, not 5–40. The register now carries the FY2025 basis
with the superseded reading recorded beside it.

The filing that moved the lives is the filing that quantifies the move — the AED 90,917
thousand relief is on the same page — so the staleness and its own explanation were one
paragraph apart, and the register cited the older filing.

### 2. The composition IS disclosed; it is the class lives that are bands

The section above says the note "publishes RANGES per class and no weighting". The first
half is right and the second is not, and the sharper statement is worth having: **note 5
discloses cost, accumulated depreciation and net carrying amount for every one of the five
depreciable classes**, so a carrying-amount weighting is arithmetically available. What
defeats it is that each class discloses a **band**, and weighting bands returns a band:

| weighted on | all low ends | all high ends | spread |
|---|---:|---:|---:|
| gross cost (the replacement proxy) | 10.89 y | 39.87 y | 28.98 y |
| net carrying amount (the note's own) | 12.20 y | 43.41 y | 31.21 y |

Buildings alone are **59.9% of gross cost on a 15–50 band**, so the answer is decided
almost entirely by where inside one class's range a figure is picked. **A twenty-nine-year
spread is not a life with an uncertainty around it; it is the absence of one.** And the
identity that would collapse it is the one the residual-value policy and the quantified
reassessment have already broken. The cheap cross-check the shared module says to run
first — implied 23.65 y against the band — *passes*, and proves nothing: a band that wide
contains almost any number. **The note is the test; the arithmetic corroborates only
sometimes.**

### 3. The pages foot, and the lives table was read off the pixels because footing cannot reach it

Note 5 was footed cell by cell, both years: every movement row sums across the six classes
to its printed total in both the cost and the accumulated-depreciation blocks; every class
column rolls from opening through additions, transfers, disposals, impairment and exchange
differences to its printed close; closing cost less closing accumulated depreciation
reproduces the printed net carrying amount for all six columns in both years; FY2025
openings tie to FY2024 closings; and the note total ties to the balance-sheet line on a
different page (8,032,197 and 7,552,178). **Roughly forty tests, zero failures.** Route:
text layer.

The **lives table carries no arithmetic at all**, so footing cannot arbitrate it and the
extractor's confidence would be the only evidence. It was therefore rendered at 200 dpi and
read as an image; the pixels and the text layer agree character for character on all ten
bands, and the table is printed twice in the same filing — note 3.10 and again under note 4
— with the two occurrences agreeing class for class.

### 4. The other route to the same quantity was run, and it is closed too

A terminal does not strictly need a life if the company states its **maintenance capital
spending**. It does not. The FY2025 management discussion breaks capital expenditure down
by *project type* and puts new-station construction and capitalised property maintenance in
the **same category**, saying only that "about 50% of the CAPEX comprised development and
construction of new service stations"; the H1 2026 management discussion says "over 50%
represented growth CAPEX" on AED 339 million — a bound, over half a year, on the other side
of the split. Neither is a maintenance figure.

**Negative searches actually run**, so the next pass does not repeat them: no maintenance or
sustaining capital figure appears in the FY2025 management discussion, the FY2025 or
Q1/Q2 2026 results presentations, or the 2025 integrated report.

### And the life is not the only thing missing

`terminal_correction_price.py` reports this name **missing `working_capital` and
`ic_replacement`** as well, so nothing could be priced here even with a life in hand — and
the replacement-cost base needs an escalation from historical cost, which needs an age,
which is the same missing number arriving a third time.

**Nothing in this pass moves a published number.** No central, no document, no workbook.
