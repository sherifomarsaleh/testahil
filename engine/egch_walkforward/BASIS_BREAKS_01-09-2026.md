# EGCH (KIMA) — basis-break register

**Built before any model was specified and before any error was computed**, per
[R-FCAL-01] §1. Each break states the overlap year, the chain factor where one exists,
and the treatment. A unit driver is scored only inside its own definition window.

Internal. Nothing here reaches a reader.

---

## B-1 · The statement layout changed three times inside the window

| filings | layout | what it does with selling cost |
|---|---|---|
| FY2009–FY2013 | old public-sector layout, full EGP: activity revenue → cost of units sold → **marketing costs** → gross profit → investment revenue → other revenue → admin → burdens → credit interest → gains/losses → PBT | INSIDE "cost of activity revenue", so the printed gross profit is AFTER marketing |
| FY2014–FY2016 | old layout, full EGP, but marketing moved BELOW gross profit | printed gross profit is BEFORE marketing |
| FY2018–FY2022 | new single-column layout, EGP thousand: revenue, cost of sales, gross profit, then every other line as a signed item | selling and distribution as its own line from FY2021 (nil FY2017–FY2020, inside cost of sales) |
| FY2023–FY2025 | new layout with an "operating result" subtotal and finance income / finance cost / investment income below it | own line |

**Chain factor — verified on a year published on both cuts.** The FY2014 filing restates
FY2013's gross profit from 50,340,509 (after marketing) to 91,139,732 (before marketing);
the difference is exactly FY2013's marketing cost of 40,799,223. `panel.py` therefore
carries every year on the PRIMITIVE lines (revenue, cost of units sold, marketing) and
DERIVES gross profit as revenue − cost of sales for all years. No driver targets a printed
subtotal.

**Consequence for FY2017–FY2020.** Those filings print no selling line at all (the cost
of distribution sits inside cost of sales). `selling` is scored only where it is
disclosed as its own line; cost of sales is scored on the taxonomy each year printed and
the break is recorded here rather than chained, because no year is published on both
cuts.

## B-2 · THE PLANT WAS REPLACED — the structural break the whole record turns on

KIMA operated a 1960 Aswan complex (electrolytic hydrogen → ammonia → ammonium nitrate,
with a ferro-silicon furnace) until FY2019. The KIMA-2 gas-fed ammonia/urea complex
(1,200 t/d ammonia, 1,575 t/d urea) was commissioned during FY2020–FY2021; the old plant
stopped in FY2019 (revenue 341m against 571m the year before), FY2020 and FY2021 were
loss years with negative gross profit (−180m and −70m), and FY2022 was the first full
year of the new plant (revenue 4,441m against 1,399m).

| | FY2018 | FY2019 | FY2020 | FY2021 | FY2022 |
|---|---:|---:|---:|---:|---:|
| revenue (EGP m) | 571 | 341 | 315 | 1,399 | 4,441 |
| gross profit | 110 | 17 | −180 | −70 | 2,021 |
| net | 100 | 32 | −1,350 | −1,424 | 651 |

**Treatment.** No chain factor exists and none is invented. The old-plant era and the
new-plant era are two different businesses reporting under one name. Every aggregate
line is scored across the break as the protocol requires — the record is meant to show
what a mechanical method does when the company it is projecting ceases to exist — and
the era split (§B-9) draws its boundary here. Unit drivers (tonnes × realisation) are
defined ONLY inside the KIMA-2 window where the auditor's product-cost table discloses
urea tonnes (FY2023–FY2025). Corrections reset at this break.

## B-3 · Two years of losses, and the log score

FY2020 and FY2021 carry negative gross profit, negative profit before tax and negative
net profit. A log error is undefined on a non-positive pair. **Treatment, fixed in
advance:** a cell is scored on log error only where projection and actual are both
positive; cells where either side is non-positive are excluded from the log statistics
and counted separately as SIGN cells (did the projection carry the right sign), with the
count printed beside every figure that omits them.

## B-4 · Comparative-only years

The company's archive lists no annual for 2012, 2015 or 2017 and nothing older than
2009. FY2008, FY2012, FY2015 and FY2017 are carried from the comparative column of the
following year's filing and flagged `column="comparative"` (L-040). Where the filings
show that a comparative was restated (B-5) the as-first-reported figure is unavailable
for those years and this is recorded rather than hidden.

## B-5 · Restatements of comparatives, recorded beside the as-reported year

| year | as first reported | as restated (next filing) | where |
|---|---|---|---|
| FY2009 | cost of units sold 123,225,776; investment revenue 31,058,026; net 69,951,589 | 124,677,883; 33,824,042; 71,333,350 | FY2010 filing |
| FY2010 | net sales 208,577,140; cost 146,530,058 | 208,533,457; 145,939,458 | FY2011 filing |
| FY2013 | gross profit 50,340,509 (after marketing) | 91,139,732 (before) — layout, not substance | FY2014 filing |
| FY2022 | cost of sales 2,419,611; selling 176,188; gross profit 2,021,090 | 2,322,989; 272,810; 2,117,712 — freight reclassified, PBT unchanged | FY2023 filing |

**Treatment.** As-first-reported at every origin that has one; `panel.RESTATED` carries
the other basis and the FY2022 reclassification is asserted at import so a later tidy-up
onto one basis fails the panel. The 08-08-2026 study's `extract_history.json` had taken
FY2022 from the FY2023 comparative (restated) and additionally mis-read provisions formed
as 21,000 against the printed 210,000; both are corrected here from the FY2022 filing
itself.

## B-6 · FY2014 is a partial year

The company's 2014 annual is a 367 × 519 pixel scan (the embedded image, extracted at
native resolution). The revenue, selling/administrative, burdens, investment-income and
currency-gain blocks each foot on the page and are carried; credit interest, profit
before tax, tax and net profit cannot be read and are NOT reconstructed by arithmetic.
**Treatment:** FY2014 is a target only for the lines it holds and an origin only for the
drivers those lines feed; profit-line cells touching FY2014 are absent, not estimated.

## B-7 · The cost-by-nature notes in the prior extraction do not foot

`engine/egch_study/extract_history.json` and `extract_fy2425.json` carry cost-of-sales
notes by nature for FY2023, FY2024 and FY2025. Summed, they miss the printed cost of
sales by 247,046 / 36,291,957 / 63,000 EGP respectively. Under the footing rule they are
not sources. **Treatment:** no cost-by-nature driver (materials, wages, depreciation) is
specified in this run; cost of sales is one line on one escalator, and the published
study's gas/materials split remains what it already says it is — a construction.

## B-8 · One-offs the company itself attributed

| year | item | amount (EGP k) | treatment |
|---|---|---|---|
| FY2024 | gain on revaluation of investment property | +2,034,573 | own line `reval_gain`; excluded from the `other_bucket` driver; the headline record is shown with and without it |
| FY2021 | miscellaneous losses (old-plant write-downs) | −479,643 | inside `other_bucket`; classified, not removed |
| FY2022 | miscellaneous losses | −309,967 | inside `other_bucket` |
| FY2020 | impairment losses | −26,037 | inside `other_bucket` |
| FY2020 | deferred-tax charge on the transition | −915,157 | tax line; the tax driver is a statutory-rate formula so this lands in the tax error, where it belongs |
| FY2019 | extraordinary losses | −23,803 | inside `other_bucket` |
| FY2016–FY2019 | currency gains on dollar deposits (68m, 176m, −0.2m, 217m) | `fx` line | the fx driver is a formula on the PPP path (§2 of the pre-registration), never zero by assumption |

## B-9 · Currency regime and eras

EGP/USD fiscal-year average (derived, World Bank): FY2016 8.86 · FY2017 13.90 (the
November-2016 float) · FY2018 17.77 · FY2019 17.27 · FY2020 16.26 · FY2021 15.70 ·
FY2022 17.40 · FY2023 24.89 · FY2024 37.96 · FY2025 47.26. Three eras are drawn for the
sign-stability test, and the boundaries are the plant replacement (B-2) and the float:

- **E1 old plant, pre-float:** origins FY2012–FY2016
- **E2 old plant post-float and the transition:** origins FY2017–FY2020
- **E3 KIMA-2 operating, three devaluations:** origins FY2021–FY2024

## B-10 · The administered gas price

KIMA-2 buys gas at an administered dollar price: US$4.50/mmBtu, raised to US$5.75 under
the November-2021 decision and applied from 13 September 2022 (note 28, FY2024/25). The
old plant bought electricity at an administered tariff. Neither is a world price.
**Treatment:** the world gas price is fetched as context and is NOT a driver; cost of
sales escalates on domestic CPI (pre-registered) with a currency-path sensitivity for
the KIMA-2 era reported and never selected.

## B-11 · Tax regime by origin

Statutory corporate rate at the origin: 20% to FY2013; 25% for FY2014–FY2015 (Law
44/2014; the temporary 5% surcharge is excluded); 22.5% from FY2016. The company has in
fact paid almost no current tax in the KIMA-2 era (deferred credits). The driver is the
formula; the record will show the gap.
