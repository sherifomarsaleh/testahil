# TMGH — fundamental walk-forward: BASIS-BREAK REGISTER

**Instrument:** Talaat Moustafa Group Holding (EGX:TMGH) · market EG · exchange EGX
**Written:** 1 September 2026, BEFORE the pre-registration and before any projection was run.
**Standing rule:** [R-FCAL-01]. Internal training record; nothing here is published.

A driver is only comparable inside the window where its definition holds. This register
fixes those windows before any model is built, so that a break is a stated scope limit
rather than a measured "bias". Each entry states the break, the overlap year, the chain
factor where one exists, and the treatment the pre-registration then applies.

---

## B1 — Segment presentation changes twice, and both changes are ours to live with

| era | presentation | source |
|---|---|---|
| FY2011–FY2016 | THREE lines: revenues from units sold · revenues from hotels · other revenues, each with its own cost line | full-year earnings releases, "Key Operational Highlights" |
| FY2017–FY2018 | TWO lines: development · **hospitality and other recurring combined** | FY2018 earnings release, consolidated income statement |
| FY2019–FY2025 | THREE lines: real estate development · hospitality · activities with periodic yield and service activities | FY2019+ releases and the audited statements |

**Overlap:** FY2018 is reported both ways — combined (2,127.9 → 3,432.1 across FY2017/FY2018)
in the FY2018 release, and split (hospitality 1,606.6 + other recurring 1,825.5 = 3,432.1) in
the FY2019 release. The two foot exactly, so the chain factor is **1.000** and no adjustment
is needed; what is NOT recoverable is the FY2017 split, which no document publishes.

**Treatment.** Hospitality and other recurring are scored as ONE driver, `recurring_revenue`,
across the whole span. They are additionally scored separately over FY2019–FY2025, and that
second record is reported as the shorter-window result it is. The combined line is never
read as either half — a first pass did exactly that, matching "other recurring revenue"
inside "Hospitality and other recurring revenue", and put the FY2018 combined figure into
the other-recurring cell.

## B2 — Revenue recognition: point-in-time throughout, with percentage-of-completion added for Saudi Arabia in FY2025

TMG recognises revenue on contracted residential, professional, commercial and administrative
units **at a point in time, when control transfers to the customer** — the handover clock. That
policy is unchanged across the whole panel and is quoted verbatim in the FY2023 and FY2025
statements alike.

From FY2025 a SECOND basis appears alongside it, for one geography only:

> "For contracts related to real estate projects under development in the Kingdom of Saudi
> Arabia, revenue is recognized over time using the percentage of completion method … The
> Group determines the percentage of completion based on the proportion of costs incurred to
> total estimated project costs."
> — FY2025 consolidated financial statements, note 2.3

The 1H2026 release quantifies it: Banan "is recognized under the percentage-of-completion
method, contributed 52.5% of the real estate segment's revenues during 1H26."

**Why this matters more than it looks.** [L-102] says to check the recognition basis before
anything else, and [L-001] records what happens when revenue and cost sit on different clocks.
TMGH is NOT the PHDC case: PHDC moved wholesale to percentage-of-completion in January 2016,
and a model built without noticing produced a net profit three times too high. TMGH's Egyptian
business has never moved, so the trap that caught PHDC does not arise here — but a NEW one
does, in the opposite direction: from FY2025 a growing share of revenue is on a different
clock from the rest, and treating the segment as one homogeneous conversion process will
mis-time it.

**Treatment.** The development driver is a **backlog-conversion rate**, δ, defined on the
handover clock, and it is scored only over origins whose whole horizon sits inside the
point-in-time era — that is, resolved horizons ending FY2024 or earlier. FY2025 and later are
carried in the panel and used for the forward projection, where the Saudi leg is projected
SEPARATELY on its own basis and labelled. No conversion rate is scored across the break.

## B3 — The Egyptian pound, four times

| date | event | EGP/USD before → after |
|---|---|---|
| Nov 2016 | free float | ~8.9 → ~18 |
| Mar 2022 | first step devaluation | 15.7 → ~18.3 |
| Oct 2022 | second step | → ~24.7 |
| Jan 2023 | third step | → ~30.9 |
| Mar 2024 | fourth step, IMF programme | → ~47.6 |

Annual averages, World Bank WDI `PA.NUS.FCRF`, in `macro.json`: 7.69 (2015), 10.03 (2016),
17.78 (2017), 19.16 (2022), 30.63 (2023), 45.30 (2024), 49.23 (2025).

**Treatment.** Three eras, fixed here and never re-cut after seeing a result:

* **E1, pre-float:** FY2011–FY2015
* **E2, post-float:** FY2016–FY2021
* **E3, devaluation:** FY2022–FY2025

Every measured bias is reported by era as well as pooled, and — per [L-029] and [L-030] — a
bias that changes sign between eras is reported as instability and is NOT corrected for.

## B4 — The seven-hotel acquisition, FY2024

TMG acquired a 39% stake with management rights in a portfolio of seven hotels (Sofitel Legend
Old Cataract Aswan, Cairo Marriott and Omar Khayyam Casino among them), consolidated from
2024. Hospitality revenue goes from EGP 3,540.9mn (FY2023) to EGP 11,496.5mn (FY2024) — a
3.2x step that is an acquisition, not growth.

**Treatment.** The hospitality driver is scored only inside its own definition window. Origins
projecting hospitality across FY2024 have that leg flagged as spanning a structural break, and
the break resets any correction on that driver per §5 of the standing prompt.

## B5 — FY2024 restated in the FY2025 statements (EAS 29 measurement period)

The FY2025 statements label their FY2024 comparative column "(Restated)". The note explains it
as a purchase-price allocation completed within the twelve-month measurement period for the
hotel acquisition:

| line | before | adjustment | after |
|---|---|---|---|
| Intangible assets | 4,100,364,530 | (4,056,516,092) | 43,848,438 |
| Goodwill | 10,289,353,903 | 2,454,102,773 | 12,743,456,676 |
| Retained earnings | 47,493,595,935 | (1,698,008,412) | 45,795,587,523 |

It flows through the income statement: hospitality cost 4,726.6 → 6,024.7 (+1,298.0), gross
profit 15,300.2 → 14,002.2, net profit 14,467.5 → 12,769.5, EPS 4.68 → 4.38. The net profit
movement is exactly the retained-earnings adjustment, −1,698.0, which foots.

**Treatment.** Point-in-time discipline: every origin sees FY2024 **as first reported**, and the
panel carries the restatement beside it rather than substituting it. This is enforced in code —
`panel.py` ranks the document that first reports a year above any later document quoting it —
not by remembering to do it.

## B6 — Cheques for undelivered units come onto the balance sheet, FY2022–FY2023

From 2022–2023 the statements gross up two new lines — "Notes receivable for undelivered units"
and "Liabilities against cheques received from customers on undelivered units" / "Obligations
against notes receivable for undelivered units" — while separately disclosing post-dated cheques
held OFF balance sheet (EGP 72.9bn at end-2023, EGP 171.4bn at end-2025).

**Treatment.** Receivables and contract liabilities are NOT comparable across FY2022. Working
capital is therefore driven off **customer advances** and **development properties**, both of
which run the span, and the gross-up lines are excluded from every ratio. The off-balance-sheet
cheque balance is recorded as a disclosure, never netted into a driver.

## B7 — New sales, FY2023: total versus core

The FY2023 release states BOTH "Total new sales in FY2023 soared to an unprecedented EGP142.8bn"
and that "EGP94.9bn came from core new sales". The difference is a large non-core land
transaction.

**Treatment.** The driver is the TOTAL, consistently across every year, because that is what the
other years report and a series that switches definition mid-way measures the switch. The core
figure is recorded beside it and the FY2023 conversion rate is reported both ways under the
dual-framing rule [L-026].

## B8 — Saudi Arabia and the mega-launches, FY2024–FY2026

SouthMed launched July 2024; contracted sales reach EGP 504bn in FY2024 against EGP 142.8bn in
FY2023 and EGP 33.2bn in FY2022. Banan (KSA) begins contributing revenue in FY2025; The Spine
launches April 2026.

**Treatment.** This is the class lesson [L-101] in its strongest form: **volume is set by the
launch calendar, and no demographic anchor can see it.** The population-anchored volume driver
is kept because it is the mechanical rule the pre-registration commits to, and its miss at
these origins is REPORTED rather than corrected — the correct reading of a 15x sales year is
that the method cannot see launches, not that the method needs a multiplier.

## B9 — What the panel could not source, and why the window stops where it does

* **FY2007, FY2008, FY2010** are excluded from the annual panel. TMG published them and the
  releases are held, but they survive only as scans whose summary tables do not resolve into
  columns; fewer than twelve cells per year survive footing. Nothing was estimated to keep them.
* **FY2017 new sales** is not stated in any document held. The FY2018 release gives 62% growth,
  from which EGP 13.1bn follows arithmetically. That is an inference, not a disclosure, and the
  cell is left empty.
* **Unit counts** are published occasionally (2,991 delivered in FY2021; 4,091 in FY2022; 2,661
  in FY2023; 3,196 in FY2025; 6,102 units sold in FY2022) and never as a continuous series.
  A price-per-unit driver built on them would divide one year's value by another year's count,
  which is exactly the arithmetic error [L-010] records. **The unit level is therefore not
  available for this issuer**, and the build stands at SEGMENT level with that gap stated —
  [R-SIGCM-02]'s "segment", not "unit".
* **Backlog before FY2018** is disclosed only as an approximation ("approximately EGP 20 BN").
  Recorded at the stated precision, not at false precision.

## B10 — Definition windows, as they bind the scoring

| driver | scored over | why it stops there |
|---|---|---|
| new sales value | FY2011–FY2025, FY2017 absent | B9 |
| backlog | FY2012–FY2025, FY2011 absent | B9 |
| conversion rate δ | FY2012–FY2024 | B2 — no rate is scored across the percentage-of-completion break |
| development revenue, cost | FY2011–FY2025 | continuous |
| recurring revenue (combined) | FY2011–FY2025 | continuous by construction, per B1 |
| hospitality alone / other recurring alone | FY2019–FY2025 | B1, and B4 breaks hospitality at FY2024 |
| SG&A, D&A, finance cost, tax | FY2011–FY2025 where present | continuous |
| working capital (advances, development properties) | FY2017–FY2025 | balance sheet resolves from FY2017 |
