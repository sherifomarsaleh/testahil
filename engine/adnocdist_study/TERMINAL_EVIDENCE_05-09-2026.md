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
