# ADNOCLS — why the terminal is still on the retired construction, re-tested and still stopped

**Status: STOPPED, on the accounts' own words, 5 September 2026.** This file exists so the
next session does not re-derive a route that is closed, and so the reason is written where
the block is rather than in a commit message.

## What is wrong, and it is the exemplar

The terminal census reads this study **7.5% BELOW its own no-growth perpetuity at book
depreciation** — the only one of sixteen readable terminals that does. It carries the
retired reinvestment identity, whose implied replacement cycle is 1/g: at a 2.0% terminal,
**fifty years against a fleet the company depreciates over twenty-five.**

That matters more here than on an ordinary name. **This study is the MODEL REPORT**, and
CLAUDE.md tells every new study to open it and match its sections, sheets, content and
depth. A construction sitting in the exemplar propagates by imitation into every study
written after it, which is what [R-ENF-01 EXTENDED, 04-Sep-2026] adopted an exemplar-debt
gate for. The debt is on the ratchet, it is named, and it may not grow.

## The first attempt, and why it stopped (04-Sep-2026)

Maintenance was built on the DISCLOSED 25-year vessel life against the replacement-cost
capital base. It came to **LESS than the model's own book depreciation charge**, so terminal
free cash flow exceeded terminal profit and the implied payout reached **117%**.
`terminal_value.build()` refuses that outright, and is right to: a going concern
distributing more than it earns for ever is a liquidation.

The two figures disagree because **they are not measuring the same thing**. Dry-docking
components are written off over two to five years and major dry docking over sixty months;
dry docking IS maintenance, capitalised and amortised fast. A terminal charging only hull
replacement while adding back ALL book depreciation would add back the amortisation of a
cost it never charged. The filings do not split the vessel line by component, so the life
that would do it cannot be derived — and **a life this desk chose is not a disclosed life**.
Stop and inform, SIGCM clause 8.

## The second route, tested today, and closed by the policy note

**The measured-age route sidesteps that argument entirely and would have worked here if the
accounts allowed it.** Charging maintenance as book depreciation escalated over the base's
own MEASURED age never needs the vessel line split by component: book depreciation already
embeds whatever mix of hull and dry-docking the company charges, and escalating it from
historical cost to today's is the whole of the adjustment. It also cannot produce the 117%
payout, because maintenance is then **greater than or equal to** the depreciation being
added back, by construction, for any age above zero. That is what unlocked EGCH.

**It is closed here, and the accounts say so in one sentence.** Note 3, material accounting
policies, property, plant and equipment:

> *"Depreciation is calculated using the straight-line method to allocate the assets' costs
> **to their residual values** over their estimated useful lives"*

and, four paragraphs later:

> *"The Group reassesses the salvage value of the vessels based on the scrap value rate on a
> yearly basis"*

Those are conditions (i) and (ii) of [L-328]. Where the depreciable amount is cost LESS a
residual, the annual charge is not cost over life, so accumulated depreciation over the
charge **overstates** the age rather than measuring it; and where the residual is reassessed
every year the charge is not level, which breaks the identity outright rather than merely
biasing it. Three of the five names this route has been tried on fail on exactly this
clause, and a vessel fleet — where scrap steel is a real and material residual — is the
clearest case of it in the book.

**So no age is measured and none is assumed.** The direction of the error would have been
safe, which is not a reason: an overstated age overstates maintenance and understates the
value, and [L-328] already records a name where that argument was made and the figure was
withdrawn anyway.

## What would open it

One of three, and each is a disclosure rather than a judgement:

1. **A split of the vessel line by component** — hull against dry-docking — in any period,
   from which a hull life and a dry-docking life could each be applied to their own base.
   The annual report's property note, the fleet schedule, or an investor presentation are
   where it would be.
2. **The residual values themselves**, per class or in total. With the residual disclosed,
   the depreciable amount is recoverable and the age identity works again on
   (cost − residual) rather than on cost.
3. **A disclosed average fleet age**, which shipping companies frequently publish in
   investor material and which would supply the measurement directly, sourced.

None was found in the FY2025 audited statements, the FY2024 or FY2025 annual reports, or
the April 2026 investor presentation held in this directory. **That is a statement about
what was searched, not a claim that no such disclosure exists anywhere**, and route 3 in
particular is worth one look at a fleet list or a rating agency's report before this is
called closed for good.

## The general form, which is not about ships

**A blocker re-tested by a different route is worth the ten minutes even when it stays
blocked**, because the two routes fail for different reasons and the second reason is new
information: this terminal is not blocked by the vessel-component problem alone, it is
blocked by a residual-value policy that would defeat the age identity even if the component
split were published tomorrow. Knowing which of the two is binding changes what a session
should go looking for, and that is the whole value of writing it down.

---

## Route 3 run and closed, and the weighting refused (05-09-2026, later pass)

The three things named above under "What would open it" were left with route 3 — a disclosed
average fleet age — flagged as worth one look. **It was looked at, it exists, and it does not
open this.**

ADNOC L&S investor presentation April 2026, appendix slide 22, *Owned Shipping Fleet (as of
31 December 2025)*: owned counts and average age by vessel type, 87 vessels, subtotals footing
53 + 20 + 11 + 3 = 87. **Read off the rendered pixels, because the text layer does not foot** —
it places FSU with the tankers and returns 55 and 18 against a stated 53 and 20; the pixels put
FSU in the gas block and every subtotal then foots. The extraction was not wrong about any
figure, only about which block a row belongs to, which is exactly the failure a footing check
is for.

It does not open the terminal, for three reasons and the first is sufficient:

1. **It is counts and ages, not carrying amounts.** A count weight prices a very large crude
   carrier and an MR the same; this file's own verified newbuild prices put them at about
   USD 136mn and USD 45mn.
2. **One age is not disclosed at all.** LNG — 8 of the 87 owned vessels, the newest and among
   the most valuable — prints as **"XX"**, an unfilled placeholder in the published deck. The
   79 that carry an age count-weight to 9.87 years, and the 8 that do not are precisely the
   ones that would move it.
3. A vessel age is not the charge-weighted age of the depreciable base, which also carries
   buildings, ports, plant, equipment and the capitalised dry-docking components.

### The weighting itself is refused, and the reason is in note 11's shape

Note 11 carries six columns. **97.85% of depreciable net book value — 95.85% of depreciable
gross cost — sits in the single "vessels and marine equipment" column**, which spans six
disclosed lives from 2 to 40 years. No filing, annual report, presentation or management
discussion held here splits it. **The note discloses the lives and does not disclose the
composition they would be weighted by**, so no single life is recorded.

Two corrections to the sourced record came out of this pass, both now in
`engine/valuation_calibration/disclosed_lives.json`:

* The band was recorded as **2–40 years** from the six vessel classes; the note discloses **ten**
  classes and its widest is buildings, ports, wharves and land improvements at **7–50**. The
  census printed 2–40 for two days. A partial transcription of a policy note reads exactly like
  a complete one.
* The dry-docking bound of **2.79%–6.04%** reproduces to the digit and is **a property of the 25
  in the solve, not of the disclosure**: one equation, five unknown class costs. At other hull
  composites the same residual charge gives 6.68–9.79% at 30 years and 11.12–14.09% at 40. The
  company's own FY2022 and FY2023 notes disclose the vessel line as *"Vessels (excluding dry
  docking component) 20 – 40 years"*, which contradicts 25 outright; FY2024 is where it was
  disaggregated into five classes, and **no carrying amount followed the disaggregation**.

**The stop stands, and it is now stopped for a third distinct reason** — not the vessel-component
problem, not the residual-value policy, but that the one column carrying 98% of the base is
disclosed at no finer level than a six-life range. Knowing which of the three is binding is the
whole value of writing it down.

---

## Re-tested against the H1 2026 filings and STILL STOPPED (07-09-2026, the re-strike pass)

Four documents the delivered edition never held were swept in on 7 September 2026 — the
reviewed six-month statements to 30 June 2026, the management discussion, the earnings
release and the first-half earnings presentation. **Each of the three routes above was
re-tried against them. None opens.**

**Route 1 — a split of the vessel line by component.** The interim carries a
property, plant and equipment note (note 4) that is a SINGLE-COLUMN roll-forward: cost at
1 January 8,167,686, additions 463,814, disposals (175,377), transfers, cost at 30 June
8,453,284; accumulated depreciation and impairment 1,283,508 to 1,411,696; net book value
7,041,588. **No class split, no capital work in progress, no useful lives.** An interim
prepared under IAS 34 does not repeat the accounting-policies note, and this one does not.
The one new figure it does give — gross cost of 8,453,284 at 30 June against 8,167,686 at
the year end — is a TOTAL, and a total cannot be apportioned across the six lives the
FY2025 note discloses for the vessel line.

**Route 2 — the residual values.** Searched across all four documents for *residual*,
*scrap*, *salvage*, *useful li* and *dry-dock*: **zero occurrences in any of them.** The
FY2025 policy note's two clauses stand unamended and unrepeated.

**Route 3 — a disclosed average fleet age.** The first-half deck DOES carry the slide, at
30 June 2026 rather than 31 December 2025, and one thing has improved: **the LNG row's age
is now filled at 15 years where the April deck printed an unfilled placeholder.** The
owned shipping fleet is 88 vessels — 52 tankers, 22 gas, 11 dry bulk, 3 container — and the
four class subtotals foot to the printed total. That closes the SECOND of the three reasons
recorded above and leaves the first and third exactly as they were: **it is counts and
ages, not carrying amounts** (a count weight prices a very large crude carrier and an MR
the same), and **a vessel age is not the charge-weighted age of a depreciable base** that
also carries buildings, ports, plant, equipment and the capitalised dry-docking components.
The first reason alone is sufficient, as it was.

### And the refusal is sharper than it was, not softer

`terminal_value.build()` was re-run on this re-strike's own figures — terminal NOPAT
1,081,231, book depreciation and amortisation 746,550, the disclosed 25-year vessel life
against the FY2025 gross base ex capital work in progress of 7,595,070, zero real growth —
and refused:

> `implied payout of terminal NOPAT is 140.1%, outside [0, 1]: the terminal distributes
> more than it earns`

It was **117%** when this was last tested on 4 September. The gap widened for a reason that
is a fact about this rebuild rather than about the terminal: the charter-rate reversion this
study prices carries 2030 profit DOWN while the fleet — and therefore book depreciation —
carries ON growing, so maintenance at a 25-year hull life covers 303,803 against a book
charge of 746,550. **The wedge the module refuses to swallow is the dry-docking amortisation
this disclosure will not let anybody separate, and it is now 2.5 times the hull charge.**

**The ratchet entry stands.** A life this desk chose is not a disclosed life, and choosing
one here would be choosing the single number that decides the largest construction in the
study. What is recorded, so the next session does not re-run three closed routes: the
component split and the residual values are absent from the half-year filings as well, and
the fleet-age slide has improved without becoming usable.
