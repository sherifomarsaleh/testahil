# ARCC — basis-break register
### Written before any modelling. Fundamental walk-forward, 01-Sep-2026.

Every break below was found in ARCC's own filings, by reading them, and each one
carries its overlap year, its size and its treatment. A break discovered after
scoring is a break that has already contaminated the score.

---

## B-1 · The releases report the CEMENT SEGMENT; the statements report the GROUP

**This is the largest and most consequential item in this register, and it would
have been invisible to a model built from either source alone.**

ARCC's earnings releases and IR decks head their revenue line "Total Revenues".
For FY2024 that figure is EGP 8,585mn. The audited consolidated statement of
profit or loss reports net sales of EGP 8,729.8mn. The two differ by EGP 144.8mn.

Note 36 (operating segments) of the FY2025 filing resolves it **exactly**:

| FY2024 | EGP |
|---|---|
| Revenue from external customers — cement production segment | 8,585,462,048 |
| Revenue from external customers — other segments (ready-mix concrete, alternative fuels) | 144,320,773 |
| **Total, = audited net sales** | **8,729,782,821** |

So the release's revenue *is* the cement segment, to the pound. The gap is real
revenue from a real business the release simply does not cover.

| FY | group sales | release/segment | gap | gap % |
|---|---|---|---|---|
| 2014 | 2,520.6 | 2,498.7 | 21.9 | 0.9% |
| 2016 | 2,350.0 | 2,287.3 | 62.7 | 2.7% |
| 2018 | 3,274.7 | 3,160.0 | 114.7 | 3.5% |
| 2020 | 2,481.2 | 2,410.0 | 71.2 | 2.9% |
| 2022 | 4,675.0 | 4,549.0 | 126.0 | 2.7% |
| 2024 | 8,729.8 | 8,585.0 | 144.8 | 1.7% |
| 2025 | 12,447.3 | 12,320.0 | 127.3 | 1.0% |

**Treatment.** The volume and per-tonne series describe the CEMENT SEGMENT and are
used only against segment revenue. The group income statement is scored as the
group. The non-cement remainder is carried as its own driver. **Dividing group
sales by cement volume to obtain a "revenue per tonne" is prohibited in this
run** — it is L-010's error (a value over a volume that does not describe it)
wearing different clothes, and it would silently inflate the price driver by one
to three and a half per cent in a way no diagnostic downstream could separate
from a genuine price move.

---

## B-2 · The releases changed their definition of gross profit between FY2015 and FY2016

The FY2015 release reports "Gross Profit 573,249,200" against revenue of
2,236,127,591 and COGS of 1,466,357,744 — a difference of 769,769,847, not
573,249,200. The residual is exactly D&A (196,520,647). So the FY2015 release's
gross profit is struck **after** depreciation.

Every release from FY2016 reports revenue less cash cost, and the FY2016 release
restates FY2015's figure to 769,770 (thousand) on that new basis.

**Treatment.** "Cash gross profit" = segment revenue − cash cost throughout, which
is what every release from FY2016 means and what the FY2015 release's own
arithmetic yields once D&A is added back. The FY2015 release's printed gross
profit is not used. Verified by footing on FY2014 as well: 2,498.7 − 1,558.9 =
939.8, and 939.8 − 190.7 = 749.1, the release's printed figure.

---

## B-3 · The FY2015 release is standalone; every later release is consolidated

The FY2015 release states in its own footer: *"Based on standalone Financial
Statements."* The consolidated FY2015 filing reports net sales of 2,273.3mn
against the release's 2,236.1mn.

**Treatment.** FY2014 and FY2015 operating figures are flagged `basis:standalone`
in the panel. They sit outside every origin's five-year fitting window except as
history, and no unit driver is scored inside a window that straddles this break.

---

## B-4 · Three restatements, recorded beside the original and never substituted

Point-in-time discipline is absolute: an origin sees what had been published by
its own date, as originally reported.

| year | line | as first reported | as restated | by | size |
|---|---|---|---|---|---|
| 2015 | net sales | 2,273,300,139 | 2,256,645,854 | FY2016 filing | −0.73% |
| 2015 | cost of sales | 1,718,039,515 | 1,702,399,822 | FY2016 filing | −0.91% |
| 2018 | cost of sales | 2,826,502,704 | 2,821,949,633 | FY2019 filing | −0.16% |
| 2018 | G&A | 108,388,819 | 112,941,890 | FY2019 filing | +4.2% |
| 2019 | cost of sales | 2,894,882,469 | 2,899,331,819 | FY2020 filing | +0.15% |
| 2019 | G&A | 103,266,465 | 98,817,115 | FY2020 filing | −4.3% |

Net profit after tax is unchanged in all three: these are reclassifications
between cost of sales and administrative expenses, and between revenue and
contra-revenue. **They matter to a gross-margin driver and not at all to a net
profit driver, and the run reports both, so the distinction is not cosmetic.**

---

## B-5 · Currency regime — three eras, and they are not a nuisance parameter

The Egyptian pound is the dominant fact in this history. ARCC imports its fuel
and exports roughly a third to a half of its volume, so the exchange rate sits on
both sides of the income statement.

| era | years | EGP/USD | what happened |
|---|---|---|---|
| E1 pre-float | 2014–2016 | 7.08 → 10.03 | managed peg, then the November 2016 float |
| E2 post-float | 2017–2021 | 17.78 → 15.64 | stable, mildly appreciating |
| E3 devaluation | 2022–2025 | 19.16 → 49.23 | four successive devaluations |

**Treatment.** Every measured bias is split by era and reported by era. **A bias
that changes sign between eras is reported as instability and is never corrected
for** [L-029, L-030] — the average of two opposite regimes was true in neither.

---

## B-6 · The export pivot changes what the price driver means

ACC's export volume runs 401kt in FY2017 (10% of volume) and 2,436kt in FY2024
(48%). Exports are priced in USD and clinker exports are a different product from
bagged domestic cement.

**Treatment.** The price driver is split at every origin into a domestic leg
escalating on Egyptian CPI and an export leg escalating on the EGP/USD path,
weighted by the export share of volume **as it stood at that origin**. Nothing is
weighted by a share the origin could not have known.

---

## B-7 · The export line splits clinker from cement only from FY2022

Before FY2022 the releases report a single "ACC Exports Volume". From FY2022 they
split clinker export, cement export and clinker local.

**Treatment.** The unit driver is scored on total export volume, which is defined
consistently across the whole window. The clinker/cement split is carried as
disclosure from FY2022 and **is not scored**, because a driver may only be scored
inside its own definition window.

---

## B-8 · Leases capitalised onto the balance sheet

Right-of-use assets and lease liabilities appear from the FY2019/FY2020 filings
under the Egyptian Accounting Standards revision equivalent to IFRS 16. Lease
interest is a separate line inside finance costs from that point.

**Treatment.** Finance costs are scored as reported in each year. The interest
rate driver is built on interest-bearing borrowings **only** [L-002] — note 25's
credit facilities plus bank loans — and lease interest is left inside the
reported total rather than being matched to a lease liability the earlier years
do not carry.

---

## B-9 · Fuel is not separately disclosed in the profit and loss

Note 5 gives cost of sales as raw materials, manufacturing depreciation,
amortisation of licences, amortisation of right-of-use assets, transportation
and overheads. **Fuel is inside "raw materials" and is not broken out**, even
though the inventory note (note 16) carries a separate Fuel line
(EGP 200.4mn at 31-Dec-2025).

**Treatment — and this is a GAP NOTE, not a silent approximation** [R-SIGCM-02]:
the cost driver is built at `derived` level, not `unit`. Raw materials are
escalated as a single imported, USD-linked class because coal and petcoke
dominate them and both are globally traded [L-110]; transportation and overheads
escalate on domestic CPI. The study states that the fuel share of raw materials
is not disclosed and that the escalator therefore rests on a composition
assumption, rather than implying a precision the filings do not support.

---

## B-10 · Unit labels in the releases are wrong in four separate years

Not an accounting break — a transcription trap, recorded here because it would
corrupt every driver built from these documents.

| document | row | printed unit | actual unit |
|---|---|---|---|
| ER_FY2016 | Revenues 2,287,315 | "K EGP" | thousands — correct |
| ER_FY2017 | D&A 234,707 | "MM EGP" | thousands |
| ER_FY2020 | Revenues 2,410 | "K EGP" | millions |
| ER_FY2021 | Revenues 2,343 | "K EGP" | millions |

**Treatment.** Magnitude is the arbiter, not the printed label. Every figure is
normalised to EGP million and cross-checked against the audited series.

---

## B-11 · Rows without the "ACC" prefix are the national market

The releases interleave Egypt's national cement market with ACC's own
performance in one table. "Domestic Sales 12,417 K Tons" is the country;
"ACC Domestic Sales Volume 938" is the company.

**Treatment.** Only `ACC`-prefixed rows enter the company panel. The national
rows are kept deliberately, as the **exogenous volume anchor** the protocol
requires — volume is projected as national market × ACC share, never as the
company's own trend extrapolated.
