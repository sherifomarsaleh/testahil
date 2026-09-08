# BASIS-BREAK REGISTER — SCEM fundamental walk-forward

Built **before** modelling, per [R-FCAL-01]. Every break carries its overlap year, its
chain factor and its treatment. A unit driver is scored only inside its own definition
window.

---

### B1 · The cost-note line set changes between the FY2023 and FY2024 filings
**Overlap year:** none — the change is clean at the boundary.
**What moved:** "Operation and Development fees" is disclosed in FY2021, FY2022 and
FY2023 (EGP 78.4mn / 78.6mn / 78.9mn) and disappears; "Clay resource fees" (98.8mn /
115.8mn) and "Subcontractor" (104.6mn / 151.9mn) appear in FY2024 and FY2025 and are in
neither earlier year.
**Chain factor:** none is computable. Nothing in either filing maps the old line onto
the new ones and no overlap year exists to solve it from.
**Treatment:** all three lines are **EXCLUDED FROM THE DRIVER SET** and scored nowhere.
The six lines this run does score carry identical wording in all five years. The totals
are unaffected: the cost note foots to the face of the profit and loss account in every
year, which is asserted in `panel.py`.

---

### B2 · Other financial investments reclassified, FY2023 filing
**Overlap year:** FY2022, disclosed both ways.
**What moved:** EGP 65,010 of other financial investments sits in CURRENT assets in the
FY2022 filing and in NON-CURRENT assets in the FY2023 filing's comparative column.
**Chain factor:** 1.0000. The identical balance, both times.
**Treatment:** noted and nothing else. It moves no total, no driver and no working
capital line — the working-capital driver is built from inventories, debtors, due from
affiliates, sundry debtors and other debit accounts less suppliers and other credit
accounts, and this balance is in none of them. Recorded because a reclassification
nobody wrote down is how a chain factor gets invented later.

---

### B3 · Lease liabilities appear from FY2024 (EAS 49)
**Overlap year:** none disclosed.
**What moved:** FY2021–FY2023 carry bank facilities, long-term bank loans and loans from
affiliated companies and **no lease liability line**; FY2024 and FY2025 carry lease
liabilities (long and short) and no bank facilities at all.
**Chain factor:** not applicable — this is a change in what the company owes, not in how
it is described.
**Treatment:** the interest-bearing debt driver is defined as the **sum of every
interest-bearing line present in that year** — bank facilities + long-term loans +
affiliate loans + lease liabilities — so the definition is stable across the break even
though its components are not. This is the definition trap (i) exists to protect: it
excludes suppliers, other credit accounts, provisions and the deferred-tax liability,
which pay nothing.

---

### B4 · The capital increase of FY2024–FY2025
**Overlap year:** FY2024, where EGP 1,277,466,100 sits as "amounts paid under capital
increase" inside equity and EGP 147,466,100 of cash is blocked under it.
**What moved:** issued capital goes from EGP 1,330,658,670 (133,065,867 shares) to EGP
2,608,124,770 (260,812,477 shares), registered 22 April 2025. FY2021 carries a
different count again: EGP 680,584,430, i.e. 68,058,443 shares.
**Chain factor:** the counts are 68.06mn → 133.07mn → 260.81mn and **no count is ever
carried across a boundary**. Each year's count is that year's own issued capital over
the EGP 10 par the same document states, and every one of them reproduces that year's
printed earnings per share to within a cent — which is the check that makes a
carried-back count impossible here rather than merely discouraged.
**Treatment:** per-share figures are computed on each year's own count. FY2025's printed
EPS is struck on a weighted-average 222.0mn because the increase converted during the
year, and the closing count is used only for value per share.

---

### B5 · The disposal of the Sinai White Portland Cement stake, FY2024
**Overlap year:** FY2024 itself.
**What moved:** a gain on sale of investments of **EGP 1,517,386,642** — 48.2% of that
year's profit before tax — from the sale of the 25.40% holding in Sinai White Portland
Cement to Aalborg Portland Holding, completed 13 August 2024. Long-term financial
investments fall from EGP 125,561,420 to EGP 25,039,500 across the same boundary.
**Chain factor:** none. It is a one-off, not a change of basis.
**Treatment:** classified as a **one-off** and excluded from every driver rule and from
the profit the drivers rebuild. The record shows net profit both ways — as reported and
with the disposal removed — because a driver model that cannot foresee a stake sale
should not be scored as though it should have.

---

### B6 · Egypt's currency regime, and the IMF's fiscal year
**Overlap:** continuous.
**What moved:** the pound floated in March 2022, October 2022 and March 2024. Egyptian
consumer inflation on a calendar basis ran 16.5% (2022), 28.9% (2023) and 26.5% (2024)
against the 6.7–7.1% the October 2021 edition projected for those same years.
**Chain factor:** not applicable; this is the exogenous path, not a company basis.
**Treatment:** two eras, E1 before the float (origins FY2021–FY2022) and E2 through the
devaluation sequence (FY2023 onward). Separately, the IMF publishes Egypt on a **fiscal
year ending 30 June** while Sinai reports on a calendar year, so every macro figure is
mapped `fiscal_june → calendar` as half of each of the two fiscal years that span it.
Using the fiscal figure as though it were the calendar one would put the whole of the
2024 devaluation in the wrong year.

---

### B7 · The presentation of finance expense
**Overlap:** continuous, all five years.
**What it is:** this issuer prints finance expense **inside** total operating expenses,
so the line it labels "operating" is already after interest. It is not an EBIT.
**Treatment:** EBIT is rebuilt as `operating + finance` and EBITDA as
`operating + finance + D&A`, in `panel.py`, in every year. Recorded because taking the
printed "operating" line as EBIT would understate it by the whole finance charge — EGP
275.6mn in FY2023, which is larger than that year's entire EBITDA.
