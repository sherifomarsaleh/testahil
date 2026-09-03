# PHDC — valuation gap review, 3 September 2026

**Trigger.** [R-GAP-01], two-sided since 02-Sep-2026 and measured against the latest known
price since 03-Sep-2026. Central **EGP 17.85** against a spot of **EGP 14.40** — the close
on the Egyptian Exchange on 3 September 2026, supplied by the principal. The central sits
**+23.9% ABOVE** the price, past the ten per cent trigger.

**Why a second review, one day after the first.** The 02-September review was written at
**+12.8%**, against a strike price of EGP 15.20 from 23 August. Nothing in the business has
changed since. The gap is now +23.9% for two reasons that are both worth stating plainly:

| | |
|---|---:|
| gap the 02-September review audited | **+12.8%** |
| same central, against the 3-September price of 14.40 | **+19.1%** |
| plus the re-strike's own effect on the cost of capital | **+21.2%** |
| plus conforming the equity-risk-premium basis to the house default | **+23.9%** |

**A review of a 12.8% disagreement is not a review of a 23.9% one**, and that is now
enforced rather than left to judgement: reviews state the gap they audited and
`check_valuation_gap.py` compares, because a review can audit exactly the right central and
still have been written against a price four weeks old. The answer standing still is not
the same as the disagreement standing still.

**The conclusion, stated first.** The central does not move on account of the price. It
moved for two mechanical reasons, both disclosed below, and **both of them raised it** — a
direction this review is obliged to be more sceptical about, not less, because [R-GAP-01]
is two-sided precisely so an over-optimistic study gets the same audit as a pessimistic
one. Nothing in the eight headings was found wanting. The disagreement is real and it is
legible: **the price implies a cash-conversion rate of 7.31% and this study forecasts
8.71%, against a range of 3.94% to 17.87% that the company's own filed cash-flow statements
actually show.**

---

## 1. LATEST FILINGS

The most recent disclosure is the **consolidated financial statements for the three months
ended 31 March 2026**, with a limited review report attached, taken from the company's own
result centre and registered line by line — accepted only because its own subtotals foot.

The record explicitly states that **the company had published no later statement at this
edition's date**: the half-year 2026 filing was not out. That claim is re-checked in this
pass and still holds on 3 September.

This heading matters more than usual on PHDC, because the defect the 01-September review
found on a sister study was a bridge standing on a superseded balance sheet while a newer
one sat in the same document set. Here the newest sheet in existence is the one the bridge
uses.

## 2. BASE YEAR

The forecast is built bottom-up from the company's own units and prices — FY2026 revenue of
EGP 40,148mn is **anchored on the reported quarter**, not on a growth rate applied to a
prior total, and the base is the 1Q2026 reviewed actual rather than a stale full-year rate.

The revenue and cost legs escalate on the **same** house inflation path with zero real
growth, so **margin is an OUTPUT** rather than an input. That is the construction
[R-ANCHOR-01] and the cost-stack rule both require, and on this study it is what the
committed macro record says in its own words: *"price and cost escalate together so the
margin is an OUTPUT."*

Delivery growth is a separate driver on its own path, so volume and price are not conflated.

## 3. MACRO COHERENCE

One path, dated. `macro_record.path_as_of` is **2 September 2026** — the current house
Egyptian path — and every growth line resolves to it as a (real, inflation-path) pair
rather than a typed nominal. Price and cost carry **real 0.0** against that path, and the
record says so explicitly rather than leaving a reader to infer it.

This is the heading that produced [L-048] and [R-MACRO-01], and the failure mode is
escalating costs at domestic inflation while holding prices still. **It is not present
here**: the two legs are on one path by construction, and the study cannot separate them
without changing the record.

## 4. DISCOUNT RATE

**THE FIRST OF THE TWO THINGS THAT MOVED THE ANSWER, AND IT IS A CORRECTION.**

PHDC published the **rating** equity-risk-premium basis as its central. [R-COC-01] names
the **swap (CDS) basis** as the house default — the market's own live pricing of the
sovereign's credit, against an agency judgement updated in steps — and AMOC, ARCC and (as
of today) EGCH all follow it. PHDC was the second study on the other convention.

| | rating basis | CDS basis, now central |
|---|---:|---:|
| equity risk premium | 13.94% | **9.41%** |
| cost of equity, explicit | 31.26% | **29.46%** |
| cost of capital, explicit | 26.10% | **25.11%** |

Worth **+2.2%**, EGP 17.46 → 17.85. Both bases remain published; only which one is central
has moved, and the committed record now *names* the one it uses — it previously read
`erp_basis: "rating"` while the model discounted on the rating schedule, which was at least
consistent, but is now correct rather than merely consistent.

**Why this was done here rather than deferred, since it moves the answer AWAY from the
price.** The identical switch on EGCH earlier today moved that study *toward* the market.
Correcting the one that helps and deferring the one that hurts is exactly the lean
[R-ENF-05]'s sign test exists to measure, and a basis chosen by which way it moves the
answer is not a basis at all. The convention is a house convention; it is not decided per
study by its consequences.

**The rest of the construction, re-checked:** country risk enters once (the observed 23.0%
sovereign yield normalised by Egypt's own default spread, the premium added back on the
same basis); weights are market-value; the schedule is a **15-year** glide, not a single
crisis-level rate, and it runs until the growth path has converged on the terminal so the
model never capitalises a rate it has not reached. Years beyond the published policy path
sit at the terminal rate, which is the honest completion rather than an extrapolation.

## 5. TERMINAL

Terminal risk-free **12.50%**, terminal ERP 7.00%, terminal cost of capital **16.15%**.
Terminal growth is set on the same terminal inflation that sits inside the terminal
risk-free rate, so the two are one number.

This closes the defect the 01-September review found on this study: 12% terminal growth
against a discount rate embedding roughly 14.6% inflation — a perpetual real decline of
about two and a half points a year that nothing supported and nothing stated. It is gone.

The explicit window running fifteen years rather than five is what keeps the terminal from
doing the work: value is recognised across the period in which growth actually converges,
not capitalised at a rate the company never reaches.

## 6. BALANCE SHEET

The bridge stands on the **31 March 2026** sheet — the latest disclosed — and it foots:

| line | EGP mn |
|---|---:|
| present value of the explicit 15 years | 49,462.4 |
| present value beyond year 15 | 22,474.6 |
| less net debt, 31 March 2026 | −23,244.7 |
| plus investments in associates | +3,838.7 |
| plus investment property | +1,020.5 |
| less minority interests **at their share of value** | −2,508.2 |
| **equity value** | **51,043.2** |
| shares (mn) | 2,859.92 |
| **per share** | **EGP 17.8478** |

Two [R-BRIDGE-01] clauses to check specifically, because this study failed both once:

- **The minority is deducted at its share of VALUE, not at book, and not at all.** The
  30-August edition deducted *nothing* while dividing by parent shares. It now deducts
  EGP 2,508.2mn, from EQUITY value rather than enterprise value.
- **The book lens divides equity attributable to the PARENT** by parent shares. The
  30-August edition divided total equity, minority included.

## 7. CLAIMS AGAINST THE RECORD

The range is the claim most worth checking on this study, because it is the one this house
got wrong across the book: `range_basis` states the crux is **cash conversion**, flexed
from **3.94% to 17.87%** — *"the full observed span of that rate in the company's own filed
cash-flow statements ... Not a chosen percentage band: the low and the high are values this
company has actually printed."*

That recomputes against the study's own diagnostics and it is a **business** driver, with
the macro path held still. It is the construction [R-LENS-03]'s range clause requires, and
PHDC is the worked precedent the other studies were brought into line with today.

The forecast conversion rate of **8.71%** sits inside that observed span, nearer the low end
than the high.

## 8. MULTIPLE CROSS-CHECK

| lens | bear | central | bull |
|---|---:|---:|---:|
| **cash flow (the primary, and the answer)** | 4.01 | **17.85** | 46.50 |
| earnings multiple on own history | 7.45 | 11.17 | 17.37 |
| book value — a disclosed floor, never weighted | 5.97 | 6.63 | 8.62 |
| market price | | **14.40** | |

**The lenses disagree and the disagreement is published rather than averaged.** The
earnings multiple reads 11.17 and the cash-flow lens 17.85; the market sits between them at
14.40. That ordering is exactly what [R-LENS-03] predicts for a developer: an earnings
multiple values a company recognising revenue on handover at whatever happened to complete
in a given year, and book carries an undelivered order book at historical cost in a
currency that has lost most of its value since 2022. **Both are floors, not values**, and
neither is weighted into the answer.

The retired 45/15/20/20 blend of these lenses would read materially below the cash-flow
lens — which is the finding that retired it: the blend put PHDC 28% below a market its own
cash-flow lens sat within 2.2% of.

**THE REVERSE READ.** Solved on this study's own model, holding every driver at its
published value:

> At EGP 14.40 the price is paying for a cash-conversion rate of **7.31%**, against this
> study's forecast of **8.71%** and an observed range of **3.94% to 17.87%** in the
> company's own filed cash-flow statements.

That is a **140 basis point** disagreement on one driver, both values inside the range the
company has actually printed, with the market's implied figure nearer the bottom of it.
It is a legible, checkable, small disagreement — and it is a far more useful statement than
"the study is 24% above the price."

**The honest caution, because this gap points upward.** A +23.9% central is not audited less
carefully than a −23.9% one, and the direction of the two corrections that produced it is
recorded: both raised the value. Neither was chosen for that reason — one is the house cost
-of-capital convention and the other is arithmetic on a lower market capitalisation — but
the pattern is what [R-ENF-05]'s sign test measures, and it is written down here rather
than left for someone to notice.

---

## Register

| item | state |
|---|---|
| central | EGP 17.8478 (was 17.1517 at the 02-September edition) |
| spot | EGP 14.40, 3 September 2026 (was 15.20, struck 23 August) |
| gap | **+23.9%** — the 02-September review audited +12.8% |
| what moved the central | the re-strike's effect on market-value weights (+1.8%) and conforming the ERP basis to the house default (+2.2%). No business driver moved. |
| headings clean | 1, 2, 3, 5, 6, 7, 8 |
| heading with a change | 4 — the rating ERP basis conformed to the CDS default per [R-COC-01]; the committed record previously labelled itself "rating" and now names what it uses |
| where the gap lives | one driver: the price implies 7.31% cash conversion, the study forecasts 8.71%, both inside a filed range of 3.94%–17.87% |

---

*AUDITED CENTRAL: 17.8478* — the figure this review audits.

*AUDITED GAP: +23.9%* — the disagreement this review interrogates, stated so a job outside
the study can tell whether the eight headings were asked at the size the study now carries.
This review exists because its predecessor was written at +12.8% and the answer had not
moved.
