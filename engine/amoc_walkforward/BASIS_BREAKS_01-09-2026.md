# AMOC — basis-break register

**Built before any model was specified and before any error was computed**, per
[R-FCAL-01] §1. Each break states the overlap year, the chain factor where one exists,
and the treatment. A unit driver is scored only inside its own definition window.

Internal. Nothing here reaches a reader.

---

## B-1 · The fiscal year moved from 30 June to 31 December — AFTER the scored window

AMOC reported July–June through FY2025 (year ended 30 June 2025). It then filed a
**six-month transition period, 1 July 2025 to 31 December 2025**, and moves to calendar
years thereafter. The comparative column in that filing is the six months July–December
2024, **not** a year.

**Treatment.** The walk-forward is run entirely on the July–June years FY2021…FY2025,
which are homogeneous. The transition half and the CY2026 interims are held out of the
annual horizon ladder altogether — they are a different period length on a different
clock, and annualising a half-year to reach one more origin would fabricate the very
quantity being scored. They are used only as the current-state anchor for the study
built on top of this record.

**Consequence, stated plainly:** the fiscal-year change costs this run its most recent
origin. That is a real cost and it is not worked around.

## B-2 · The product taxonomy changed twice inside the window

| filing | lines published |
|---|---|
| FY2022 (and its FY2021 comparative) | Oils · Wax · Gas oil · Gas oil (bunker) · Naphtha · LPG · **Export fuel oil** · **Export fuel oil (Authority)** · Blending fuel oil · Heavy fuel oil · **Aromatic extract** · Waste |
| FY2023 | as above, less Aromatic extract and less Export fuel oil (Authority), both nil |
| FY2024, FY2025 | Oils · Wax · **Gas oil** · Naphtha · **Solar Bunker** (nil) · LPG · **Fuel oil (mix)** · Heavy fuel oil · Waste |

Two merges happened: *Gas oil* absorbed *Gas oil (bunker)*, and the three fuel-oil lines
collapsed into *Fuel oil (mix)*.

**Chain factor — verified, not assumed.** FY2023 is published on BOTH cuts. Its own
filing splits gas oil 7,067,718,244 from gas oil (bunker) 429,180,261; the FY2024 filing
restates the same year with Solar Bunker on its own line, and the two sum to
**7,496,898,505** on both bases. `panel.check()` asserts this. Where a chain cannot be
verified against a figure the company published twice, it is not made.

**Treatment.** All five years are mapped onto ONE eight-line taxonomy — oils, wax, gasoil
(incl. bunker), naphtha, lpg, fueloil (all three fuel-oil lines), hfo, other (aromatic
extract + waste). Drivers are specified and scored on that constant definition only.

## B-3 · Export fuel oil stopped — a real change, not a reclassification

Export fuel oil ran **637,120 t (FY2021)** and **418,286 t (FY2022)** and then **nil**
from FY2023, while blending fuel oil went from nil to 356,514 t (FY2022) to 711,867 t
(FY2023). This is inside the fueloil group of B-2, so the GROUP tonnage is continuous and
comparable; the composition inside it is not.

**Treatment.** Scored at group level. No sub-line driver is specified for the fuel-oil
mix, because a driver fitted on a composition that stopped existing would be scored on a
definition the company had abandoned.

## B-4 · The operating-profit subtotal is defined differently before and after FY2023

The FY2022 filing puts **other revenues** and the **claims-and-disputes provision** INSIDE
operating profit. From FY2023 both sit BELOW it. Same year, two subtotals:

| FY2022 operating profit | per FY2022 filing | per FY2023 filing |
|---|---|---|
| | 1,719,827,217 | 2,050,791,203 |

Profit before tax is **1,805,368,977 on both** — the difference is presentation only.

**Treatment.** No driver targets "operating profit". Drivers target the primitive lines
(revenue, cost of sales, G&A, marketing, other expenses, provisions, other revenues), and
every aggregate is rebuilt from those, so the subtotal convention cannot touch a score.
`panel.check()` foots each year under its OWN layout rather than forcing one convention.

## B-5 · FY2022's other-revenue / investment-revenue split was restated

| FY2022 | other revenues | investment revenues | total |
|---|---|---|---|
| per FY2022 filing | 133,456,159 | 85,541,760 | 218,997,919 |
| per FY2023 filing | 215,617,919 | 3,380,000 | 218,997,919 |

Same total, different split.

**Treatment.** As-first-reported is used at an origin standing in FY2022. The restatement
is recorded beside it and never substituted (L-037).

## B-6 · **FY2024 profit was restated down by EGP 259,596,921 — and the FY2025 filing contradicts itself about it**

| FY2024 | as first reported (FY2024 filing, 18-Aug-2024) | as restated (FY2025 filing, 18-Aug-2025) |
|---|---|---|
| Other revenue | 950,868,836 | 691,271,915 |
| Net profit before tax | 2,390,484,058 | 2,130,887,137 |
| **Majority's share** | **1,699,154,495** | **1,439,557,574** |

The whole of it sits in **miscellaneous other revenues** (368,246,666 → 108,649,745). It
is **15.3% of majority profit**.

**The primary document disagrees with itself.** The FY2025 filing's *statement of changes
in equity* still carries **1,699,154,493** as FY2024's profit at 1 July 2024 — the
as-first-reported figure — while its *income-statement comparative* shows 1,439,557,574.
Registered as found; not reconciled away, because nothing in either filing explains it.

**Treatment.** The panel carries FY2024 twice. An origin standing at FY2024 sees
1,699,154,495, which is what a reader of the accounts had. The restatement is carried in
`RESTATED` and asserted, so a later tidy-up onto one basis fails the panel.

## B-7 · There was no per-product costing system before 1 July 2023

The FY2023 auditor's **emphasis of matter** records that the company "seeks to develop the
current costing system so that the cost of each type of product produced by the company is
accurately reached", and that it "implemented a system of costs from the beginning of
July 2023".

This is load-bearing for what may be claimed. Note 14-A discloses revenue and tonnage per
product for every year; note 15-A discloses cost **by nature** (salaries, raw materials,
supporting materials, depreciation, other) for the company as a whole and **never by
product**. Any per-product cost or per-product margin is therefore a CONSTRUCTION, and
before FY2024 it is one the company itself states it could not perform.

**Treatment.** No per-product cost driver is specified at any origin. Cost is driven at
the level the filings disclose it — by nature, against total throughput. The published
study's per-line "feedstock plus conversion cost per tonne, allocated on processing-
intensity weights" is a modelling choice with no disclosure beneath it, and this record
says so rather than inheriting it.

## B-8 · FY2023 carries a qualified audit opinion

Qualified on two matters: an EGP 21mn technical study inside projects under construction,
unresolved at 30 June 2023; and EGP 12mn of ASPC investments carried as available-for-sale
and not evaluated by management. Both are balance-sheet items and neither touches revenue,
cost of sales or the product table.

**Treatment.** FY2023 stays in the panel. The qualification is recorded and is quoted in
the caveats of anything built on it. It does not impair the lines this run scores.

## B-9 · Currency regime — three devaluations inside five years

EGP/USD, fiscal-year average (derived, World Bank annual): FY2021 15.70 · FY2022 17.40 ·
FY2023 24.89 · FY2024 37.96 · FY2025 47.26. The March-2022, October-2022/January-2023 and
March-2024 devaluations fall inside FY2022, FY2023 and FY2024 respectively.

**Treatment.** Era boundaries for the sign-stability test are drawn at the fiscal years
containing a devaluation, and the macro/company split re-runs every origin on the
knowable path and on perfect foresight. With five origins an era split cannot be
load-bearing, and the pre-registration says so in advance rather than discovering it
afterwards.

## B-10 · A nil is printed as a dash, and one was nearly read as data

FY2024's gain-on-disposal is a dash. Read as a repeat of FY2023's 208,000 it produced an
other-revenue column that missed its own printed total by exactly 208,000. This is L-036,
and the column footing is what refused it.

**Treatment.** Every column in `panel.py` foots to a total the company printed, as an
assertion that runs at import.
