# PHDC — basis-break register

Built before modelling, per the walk-forward prompt's §1. Every break below is
evidenced from a primary document — the company's own filing or its own results
release — and quoted. A driver is scored only inside its own definition window;
where a break is crossed, either the chain factor below is applied or the driver
is not scored across it, and which of the two is stated.

Sources are the PHD investor-relations result centre
(https://ir.palmhillsdevelopments.com/en-us/financial/resultcenter), which
publishes 1Q2015–1Q2026, and the World Bank WDI series for the macro regime.

---

## B1 · Revenue recognition changed to percentage-of-completion, 1 January 2016
**Type:** accounting-standard change · **Overlap year:** FY2015 · **Chain factor:** 1.0228

The company's own words, 1Q2016 results release:

> "Since the beginning of January 2016, PHD adopted recent amendments to the
> Egyptian Accounting Standards, as stipulated by Ministerial Decree #110 of
> 2015, by applying the Percentage of Completion ("PoC") method as an
> accounting policy with regards to revenue recognition relating to standalone
> units (villas, town-houses and twin-houses)."

and, in the same release:

> "Revenue from apartments and multi-tenants buildings are recognized only upon
> delivery, which remains in line with the previous revenue recognition method."

So the break is **partial**: standalone units moved to PoC, apartments and
multi-tenant buildings did not. The 1Q–3Q2016 releases print two columns
side by side, labelled *BR — before restatement figures (using the old revenue
recognition method)* and *R — restated figures*, which is what makes the break
measurable rather than assumed.

**Measured effect on FY2015 revenue**, both figures from a primary table:

| basis | FY2015 revenue, EGP mn | source |
|---|---|---|
| as originally filed | 3,560.6 | FY2015 consolidated statements, own column |
| as restated under PoC | 3,641.7 | FY2016 consolidated statements, comparative column |

Chain factor 3,641.7 / 3,560.6 = **1.0228**.

**Treatment.** The revenue-recognition rate driver (D4) is *not* scored across
this break: FY2011–FY2015 sits in the pre-PoC definition window and FY2016
onward in the post-PoC one. Revenue *levels* are chained by 1.0228 where a
single series is needed. Each origin uses the basis in force at that origin,
which is the point-in-time rule, so an origin at FY2015 forecasts on the
pre-PoC basis and is scored against pre-PoC actuals.

## B2 · Sales KPI redefined, FY2016
**Type:** KPI redefinition · **Overlap year:** FY2015 · **Chain factor:** none applied

Through FY2015 the releases report three sales measures — *Gross Sales
(reservations)*, *Net Sales* (gross less that period's cancellations) and
*Contracted Sales*. From FY2016 they report a single measure, **New Sales**,
defined in the releases' own footnote as *"Gross New Sales"*.

**Treatment.** The gross series is used throughout, which is continuous across
the redefinition by the company's own definition. The net series is retained in
the panel for FY2011–FY2015 only and is never mixed into the gross series. This
matters: on the net basis FY2011 and FY2012 are **negative** (−1,273 and −560
EGP mn) because post-revolution cancellations exceeded new reservations, so a
series that silently switched basis would show a sign change that never happened.

## B3 · FY2016 new sales and units restated upward
**Type:** restatement · **Overlap year:** FY2016 · **Chain factor:** 1.0333 (value), 1.0305 (units)

| measure | as first reported (FY2016 release) | as later reported (FY2017–FY2019 releases) |
|---|---|---|
| new sales, EGP mn | 8,194 | 8,467 |
| units sold | 1,838 | 1,894 |

**Treatment.** Point-in-time: an origin at FY2016 sees 8,194 / 1,838. The later
figures are held in the panel as `new_sales_restated` / `units_sold_restated`
and used only when scoring an origin that post-dates the restatement.

## B4 · Village Mall disposal, FY2013
**Type:** one-off, company-attributed · **Overlap year:** FY2013 · **Chain factor:** n/a

The FY2015 release's five-year chart carries the company's own footnote:

> "2013 revenue and profit exclude the sale of the Village Mall for
> consideration of EGP240 million and EGP52 million respectively."

**Treatment.** FY2013 is scored on the ex-disposal basis the company itself
publishes. The record is shown both ways in the diagnostics, per the
dual-framing rule, and the disposal is classified as a one-off.

## B5 · Egyptian pound — four devaluation steps
**Type:** currency regime · **Chain factor:** none (nominal EGP is the reporting basis)

Annual average EGP/USD and headline CPI, World Bank WDI:

| year | EGP/USD | YoY | CPI % |
|---|---|---|---|
| 2015 | 7.69 | +8.7% | 10.4 |
| 2016 | 10.03 | **+30.3%** | 13.8 |
| 2017 | 17.78 | **+77.4%** | 29.5 |
| 2021 | 15.64 | −0.7% | 5.2 |
| 2022 | 19.16 | **+22.5%** | 13.9 |
| 2023 | 30.63 | **+59.8%** | 33.9 |
| 2024 | 45.30 | **+47.9%** | 28.3 |
| 2025 | 49.23 | +8.7% | 14.1 |

Three eras follow, and they are the eras the pre-registration fixed **before**
any error was computed: **E1 pre-float FY2011–FY2016**, **E2 post-float
FY2017–FY2021**, **E3 devaluation cycle FY2022–FY2025**.

**Treatment.** Every driver is nominal EGP, so no chaining is applied. The
devaluations are instead handled by the pre-registered macro/company error
split: each origin is run twice, once on the inflation path knowable at that
origin and once on the realised path, and the gap between them is the macro
share of the miss. This is the single largest thing that could make the record
look like company-level skill when it is currency, so it is measured rather
than argued about.

## B6 · Perimeter change — education and hospitality, FY2024
**Type:** M&A / segment re-cut · **Overlap year:** FY2024 · **Chain factor:** not established

From the FY2024 release: completion of the acquisition of **32.6% of Taaleem
Management Services**, an additional **10% of Macor Hotels** (to 69.5%) and a
**20% direct stake in Novotel October**. The company describes itself from
FY2024 as operating "three verticals namely Real Estate, Education and
hospitality".

**Treatment.** The company does not publish a restated pre-acquisition series
for the enlarged perimeter, so **no chain factor can be established**. Unit-level
drivers (units sold, units delivered, price per unit) remain real-estate-only
and are unaffected; the revenue and margin aggregates from FY2024 are flagged as
crossing a perimeter change, and any FY2024–FY2025 aggregate error is reported
with that flag attached rather than being read as a forecasting miss.

## B7 · COVID-19, FY2020
**Type:** one-off, company-attributed · **Overlap year:** FY2020 · **Chain factor:** n/a

FY2020 handovers fell to **633 units** from 964 in FY2019, and construction
spend to EGP 1.5bn. The FY2022 release refers to results "exceeding pre-COVID 19
performance levels". **Treatment:** FY2020 is retained in the sample and is
classified as a one-off in the era analysis; the record is reported with and
without it.

## B8 · FY2022 statement filed in Arabic only
**Type:** disclosure availability, not accounting · **Overlap year:** FY2022

The FY2022 consolidated statements published to the result centre are the Arabic
originals; no English translation is posted, so the FY2022 column cannot be read
from that filing directly.

**Treatment.** FY2022 is taken from the **comparative column of the FY2023
filing** — the same company, the same audited statements, one year later — and
every FY2022 record says so. It is cross-checked against the FY2022 release
(revenue 13,600 both ways). Nothing is estimated.

## B9 · FY2023 revenue differs between the filing and the following release
**Type:** restatement / discrepancy · **Overlap year:** FY2023 · **Chain factor:** 0.99957

| basis | FY2023 revenue, EGP mn |
|---|---|
| FY2023 consolidated statements, own column | 17,462.1 |
| FY2024 results release, comparative column | 17,454.6 |

A 7.5mn difference, 0.04%. **Treatment:** the filing is used, per SIGCM clause 1;
the difference is recorded and is immaterial at the driver level, but it is
recorded rather than rounded away because the direction of such differences is
itself information.

---

## Definition windows, as applied

| driver | window scored | breaks crossed |
|---|---|---|
| units sold (D1) | FY2011–FY2024 | B3 handled point-in-time |
| ASP per unit (D2) | FY2011–FY2024 | B2 handled by using gross throughout |
| new sales (D3) | FY2011–FY2024 | B2, B3 |
| recognition rate δ (D4) | FY2016–FY2025 | **not scored across B1** |
| units delivered (D5) | FY2014–FY2024 | B7 flagged |
| cost per unit (D6) | FY2016–FY2025 | not scored across B1 |
| SG&A (D7) | FY2014–FY2025 | B6 flagged from FY2024 |
| D&A (D8) | FY2014–FY2025 | — |
| interest (D9) | FY2014–FY2025 | — |
| tax (D10) | FY2014–FY2025 | rate regime read at each origin |
| construction spend (D11) | FY2015–FY2024 | — |
| working capital (D12) | FY2014–FY2025 | B1 affects receivables/WIP definitions |

## What is NOT in this register, and why

No Egyptian adoption of IFRS 9/15/16 equivalents is listed. These filings are
prepared under **Egyptian Accounting Standards**, and the only standards change
this archive documents in the company's own words is B1 (Ministerial Decree
#110 of 2015). A break is listed here only where a primary document evidences
it; nothing is added from general knowledge of what standards changed when.
