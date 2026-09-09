# ARCC — valuation gap review, 9 September 2026

**AUDITED CENTRAL: 69.2217**

**AUDITED GAP: −9.63%** against 76.60, the latest known close (6 September 2026). The
study strikes at 77.00, a stale spot; the gap on the struck figure is −10.10%. On the
latest known close the answer sits INSIDE the ten per cent trigger.

**THIS EDITION SUPERSEDES THE REVIEWS OF 1 AND 3 SEPTEMBER, which audited a central of
66.5300 at −13.15%.** Two corrections landed between them, worth **+2.76** and **−0.07**,
and a third finding closed the study's largest contested judgement at a cost of nothing.

## What moved

### 1. The replacement-cost roll counted one year of inflation twice — worth +2.76

The terminal's capital base is capacity × replacement cost per tonne × spot FX, rolled to
the last explicit year on the model's own cost index:

    ic_repl = 5.0Mt × USD 130/t × 50.30 × cost_infl[5]

`repl_usd_t` and `fx` are **both dated 2026-08-06**. Their product is therefore an
August-2026 EGP figure. `cost_infl` is indexed to **FY2025 = 1.0**. The FY2025-to-FY2026
step of 11.5% was charged twice: once inside the August exchange rate and the replacement
quote taken beside it, and again in the index.

The vintage of a figure is carried by its own source date, and both source dates say the
same thing. This is arithmetic rather than judgement, and it would have been an error
whichever way it moved the answer.

**The endpoint was checked rather than assumed, and it is right.** `terminal_value.build`
takes FCFF = NOPAT + D&A − maintenance − π·WC at the level of the **last explicit year**
and grows the whole of it by (1+g) inside the perpetuity, so every term in that sum must
be FY2030-nominal. `nopat[-1]`, `dna_f[-1]` and the working-capital level all are.
`cost_infl[5]` is the FY2030 index — the unit build runs i=0..5 over FY2025..FY2030 — so
the destination never moved. Only the origin was wrong.

The base is taken at `cost_infl[1]`, the FY2026 index point, and that is the
**conservative** reading rather than the precise one: August is month eight of a calendar
year, so the true August-2026 price level sits above the FY2026 average, the true roll is
shorter still, and the capital base and the maintenance charge that comes out of it are
if anything a little too large.

| | retired | corrected |
|---|---|---|
| roll factor | 1.565711 (FY2025 base) | 1.404225 (FY2026 base) |
| replacement-cost capital, EGP mn | 51,190.921 | 45,911.145 |
| terminal maintenance charge, EGP mn/yr | 2,559.546 | 2,295.557 |
| central, EGP | 66.5300 | 69.29 (before correction 2 below) |

### 2. The working-capital rate's justification was false — worth −0.07

`wc_pct_drev` was typed **0.12** and justified in its own source string as *"the FY2025
outturn on the disclosed movements is close to this"*.

**The FY2025 outturn on the disclosed movements is 18.06%.** Nothing in four revisions had
opened the statement of cash flows to check. This is the same shape SWDY carried on its
backlog and its employees'-cap headroom: a delivered sentence asserting something the
issuer's own filing contradicts.

What actually supports 12% is the **two disclosed years pooled**:

| | ΔWC invested, EGP mn | ΔRevenue, EGP mn | ratio |
|---|---|---|---|
| FY2024 | 115.488 | 2,686.951 | 4.30% |
| FY2025 | 671.276 | 3,717.537 | 18.06% |
| **pooled** | **786.764** | **6,404.489** | **12.28%** |

The two years disagree four-fold, so neither is a basis on its own. Pooling weights each
year by its own revenue growth, which is the weighting a driver expressed *per unit of
revenue growth* already implies.

The six movement lines are now registered one each with their note references and the rate
is **derived** from them rather than typed. *Provisions used* sits on the same block of the
cash-flow statement (−40.721mn in FY2025, −32.599mn in FY2024) and is deliberately
excluded and named: it is the utilisation of a provision, and this model already carries
provisions on their own line in the EBITDA bridge.

**THE DERIVED RATE IS LARGER THAN THE TYPED ONE, so this correction moves the answer AWAY
from the traded price and widens the gap it was found while trying to close.** It is
applied for that reason and not in spite of it. Declining a correction because of where it
lands is the same offence as making one because of where it lands [R-GAP-04].

### 3. The largest contested judgement is closed by measurement — worth nothing

`useful_lives.json` named the evidence that would overturn its 20-year terminal life:
*"a disclosed asset-class breakdown of PP&E by cost showing the base is dominated by a
class with a different life"*. **Note 12 of the same filing is that breakdown**, in the
same document the lives themselves were read from, and it had never been opened.

Gross cost less freehold land — which is not depreciated — over the year's own
depreciation expense:

| class | gross cost, EGP | FY2025 charge, EGP | implied life | share of depreciable cost |
|---|---|---|---|---|
| Machinery and equipment | 3,798,051,544 | 178,346,107 | 21.30y | 71.1% |
| Buildings | 914,331,841 | 30,150,833 | 30.32y | 17.1% |
| Other installations | 327,449,670 | 17,546,898 | 18.66y | 6.1% |
| Vehicles | 239,960,170 | 28,721,710 | 8.35y | 4.5% |
| Computers and software | 37,134,556 | 3,232,285 | 11.49y | 0.7% |
| Furniture and fixtures | 22,238,758 | 1,091,849 | 20.37y | 0.4% |
| **depreciable base** | **5,339,166,539** | **259,089,682** | **20.61y** | |

The adopted life is 20.0. The measurement **confirms** it, and it is recorded here
whichever way it had come out.

**No weighting of these classes reaches the 50 years the contested register carries as the
alternative** — that figure is a ready-mix subsidiary's buildings, and the blend cannot
get there. The alternative was worth **+16.06 a share**, the largest contested judgement in
the study, and it is now shut by the company's own charge rather than by argument.

Two independent readings of one fact agree: note 12's total charge of EGP 259,089,682
reproduces the depreciation of property, plant and equipment on the consolidated statement
of cash flows exactly [R-ENF-03]. The study now **asserts** the adopted life against the
implied one rather than trusting the policy note alone.

## The route to the filings, recorded

The ARCC financial statements carry **no usable text layer** — `pdftotext` returns 47
characters for 47 pages. Every figure above was read from the rendered page. The route is
recorded in `useful_lives.json` as [R-FCAL-01] requires, and the arbiter is arithmetic: the
balance sheet read this way reproduces this study's own assertion 33 to the pound
(assets 8,783,721,849 less liabilities 4,140,989,609 = equity 4,642,732,240), and note 12
foots to the cash-flow statement.

## What was searched and did not move the answer

**The beta, and a departure from this repository's own definition of tier 2 [OPEN].**
`wacc_builder.py` defines tier 2 as *"median **unlevered** beta of peers listed in the SAME
country, re-levered via relever_beta()"*. This study took the median **levered** peer beta
(0.9275) and used it directly. Its own cost-of-capital record says so plainly, and gives
the reason — peer leverage is not sourced — and states the direction: *"ARCC holds net cash
against levered peers, so the step could only lower the beta and raise the value."*

Two things are now on the record about that:

1. **The stated direction is not established.** This book's own delivered study of EGAL
   carries debt of 600 against cash and short-term investments of 9,600 — EGAL is net cash
   by a wide margin, not levered. LCSW is clearly levered (facilities and current loans
   1,627.7 against cash 320). The peer set is mixed, so the claim that unlevering *could
   only* lower the beta does not follow from what this desk holds.
2. **The leverage is still not sourceable to SIGCM clause 1** from what this repository
   holds. ORAS has no study directory; the EGAL workbook states that its historical debt
   line is *derived to reconcile* rather than disclosed; the LCSW workbook holds cash and
   debt *roughly flat as blue inputs*. Three of four peers therefore have no
   disclosure-grade leverage here, and a median taken over one sourced peer and three
   derived ones would be worse than not taking it.

The contested register already prices the whole distance: the own-stock regression at
0.698 is worth **+8.01 a share** against the adopted 0.9275, and a properly relevered
figure would land between them. **This is recorded as open debt rather than actioned**, and
what would settle it is named: the four peers' own audited balance sheets, at one date.

Nothing in this section moves the central. It is here because [R-GAP-04] requires the
search to be recorded whether or not it pays.

## Standing

The gap on the latest known close is **−9.63%**, inside the ten per cent trigger. The
study's strike price of 77.00 is stale against a 76.60 close of 6 September and is
disclosed rather than closed. No fair value was moved toward a price at any point in this
review: of the two corrections that changed the answer, one closed the gap and one widened
it, and both were made on their own evidence.
