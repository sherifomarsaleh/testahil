# ABUK — basis-break register

**Built BEFORE modelling**, as [R-FCAL-01] §1 requires. Internal.

Each break carries the overlap year, the chain factor and the treatment. Unit
drivers are scored only inside their own definition window.

---

## BB-1 · THE FISCAL YEAR MOVED FROM 30 JUNE TO 31 DECEMBER

| | |
|---|---|
| **what** | Twelve-month years to 30 June through FY-Jun-2025, then an AUDITED SIX-MONTH TRANSITIONAL PERIOD 1-Jul-2025 to 31-Dec-2025, then calendar quarters from January 2026 |
| **overlap year** | none — the transitional period is the join and it is half a year |
| **chain factor** | none is applied. No year-on-year rate spans the change |
| **treatment** | FY-Jun-2025 is the last annual actual and the last scoreable target. The transitional half and the 2026 calendar periods are EXCLUDED from scoring rather than annualised |

**THE TRAP, NAMED BEFORE IT WAS SPRUNG.** The company's own investor-relations
page files the transitional statements under *"Q4 (Year ended December 31,
2025)"* while the statements themselves say *"for the six months from July 1
till December 31, 2025"*. Taking the website's label books EGP 13,131,643,463 as
a full year when it is half of one — a base overstated by about a factor of two,
compounded through every forecast year and the terminal. The period length is
proved three ways across three separately filed documents: FY-Jun-2025 revenue
of 22,915,657,021 less the H1-2026 filing's comparative six months to 30-Jun-2025
of 12,666,528,690 equals 10,249,128,331, which is EXACTLY the comparative printed
in the transitional filing.

Inflation mapping splits with it: `fiscal_june` governs the years to June and
`calendar` the periods from January 2026, and the transitional half belongs to
neither by itself [R-MACRO-01 AMENDED].

---

## BB-2 · THE PRESENTATION CHANGED AT FY-JUN-2023, AND THERE IS NO OVERLAP YEAR

| | |
|---|---|
| **what** | The audited FY-Jun-2024 filing prints its FY-Jun-2023 comparative as *"Restated and Reclassified"* and introduces an operating-profit subtotal, an expected-credit-loss line, an other-expenses line and a net-financing-income block. The FY-Jun-2022 and earlier statements carry none of these |
| **overlap year** | **NONE.** The FY-Jun-2023 statements were never published on either the live shelf or the archived one, so no year exists on both presentations |
| **chain factor** | **not computable, and none is invented** |
| **treatment** | Revenue and net profit are chained across the break; the COST AND OVERHEAD SPLIT is treated as two definition windows, FY2015-FY2022 (old) and FY2023-FY2025 (new), and the cost-ratio driver is scored inside each |

**What makes the chain defensible on the two lines that are chained.** The
transition note in the audited FY-Jun-2024 filing restates the FY-Jun-2022
balance sheet — total assets from 22,372,473,861 to 22,019,544,491, total equity
from 17,806,394,611 to 16,357,091,104 — and prints profit for that year as EGP
9,054,139,328, which is EXACTLY the figure the FY-Jun-2022 statements themselves
print on the old presentation. Net profit is therefore unchanged by the
restatement and is comparable across the break. Revenue carries the same caption
either side. Cost of sales does not.

---

## BB-3 · EQUITY INVESTMENTS MOVED FROM FAIR VALUE THROUGH OCI TO THE EQUITY METHOD

| | |
|---|---|
| **what** | The audited transitional-period statements restate 30-Jun-2025 total assets from 42,219,047,998 to 34,264,303,968 and total equity from 32,135,051,656 to 26,885,346,553 |
| **overlap year** | FY-Jun-2025, printed on both bases |
| **chain factor** | assets -7,954,744,030; equity -5,249,705,103 (EGP 4.16 a share) |
| **treatment** | The investments line falls by EXACTLY -7,954,744,030, equal to the whole change in total assets, which is the proof that the restatement is the accounting change and not a bundle. Any equity-anchored lens uses the RESTATED base. This run's scoring is income-statement based and is unaffected |

**One item is unresolved and is flagged rather than smoothed.** The transitional
filing's restated 1-Jul-2024 equity of EGP 28,698,066,473 cannot be reconciled
with the Q1-2026 filing's restated 1-Jan-2025 equity of EGP 18,865,158,720 across
a half-year in which the company earned EGP 5,025,798,914. The two filings appear
to carry different restatement vintages. This is named as an open item, not
resolved by choosing one.

---

## BB-4 · THE WORKING-CAPITAL CAPTION WIDENS AT FY-JUN-2023

| | |
|---|---|
| **what** | The pre-FY2023 filings print one *"suppliers and other creditors"* line; the restated presentation splits trade and notes payables out, at EGP 92,153,797 in FY2024 against a pre-break line an order of magnitude larger |
| **overlap year** | none |
| **treatment** | Working capital in the valuation-input block is computed inside each window on its own caption, and the two are NOT compared as a series |

---

## BB-5 · THE COMPANY'S OWN WEBSITE WAS REBUILT AND THE ARCHIVE BECAME THE SOURCE

| | |
|---|---|
| **what** | abuqir.net was rebuilt in November 2025. Its investor shelf now begins at the quarter ended 30-Sep-2023; every filing older than that was removed |
| **treatment** | FY-Jun-2015 to FY-Jun-2022 are the company's own audited statements retrieved through the Internet Archive's capture of the old site. Tier A — the DOCUMENT is the issuer's — with the retrieval route recorded on every figure |

This is a provenance break rather than an accounting one, and it is in this
register because it changes what a later reader can verify: the URLs in the
bibliography for those eight years point at web.archive.org, not at the company.

---

## BB-6 · REGULATORY BREAKS INSIDE THE CURRENT YEAR

Not inside the scored window, and recorded because the study built on this run
must carry them as DATED WINDOWS rather than as permanent rates.

- **Prime Minister Decree 928 of 2026, 29-Mar-2026** — natural gas to the
  nitrogen-fertilizer industry priced by formula **with a floor of USD 8.50 per
  mmBtu**, against USD 5.50 from Sep-2025.
- **Ministerial Decision 190 of 2026, 4-May-2026** — USD 90 a tonne export duty
  on nitrogenous fertilizer for three months; **Decision 258 of 2026, 23-Jun-2026**
  replaced it with 10% of free-on-board value.
- **Ministerial Decision 340 of 2026, 25-Jun-2026** — **CANCELS every fertilizer
  export duty with effect from 1 August 2026.** Nine press and analyst sources
  were searched and NOT ONE carries it; the reversal exists only in the issuer's
  own note 48. The forward duty rate is ZERO, not 10%.

Each is a dated window in any forward model, never a permanent rate, and the
reinstatement case is priced rather than assumed away.
