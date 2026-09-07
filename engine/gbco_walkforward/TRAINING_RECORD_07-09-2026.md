# GBCO — FUNDAMENTAL walk-forward [R-FCAL-01]: training record

**7 September 2026. INTERNAL.** The panel, the error cells, the pre-registration and this
record are never shown to a reader.

**WHICH WALK-FORWARD.** The FUNDAMENTAL one. Not the price-engine walk-forward
(`gbco_study/backtest_rows.csv`, band coverage on the Monte Carlo cone) and not the technical
walk-forward (`engine/lab/ta_calibration/`).

---

## 0 · The finding that came before any number

`engine/gbco_study/` held **no filings at all** when this run began, and its own escalation
record — six routes, all failed, dated 5 September — concluded that GB Corp's statements
were unreachable from this container. Re-running that ladder, as [R-IND-01] requires of any
probe whose failure is relied on, found the conclusion **wrong about the world rather than
about the attempt**: the two hostnames it tried and could reach (`gbauto.com`, `gb-corp.com`)
are **domain-parking landers**, and the company's actual investor-relations site,
**`ir.gb-corporation.com`**, answers HTTP 200 and was never tried.

Committed to `engine/gbco_study/src/` in this run: audited consolidated statements FY2020–
FY2025, reviewed statements to 31 March and **30 June 2026**, annual reports 2013–2025,
earnings releases FY2019–FY2025 plus **1Q26 and 2Q26**, and the 1Q26 investor presentation.

**A LADDER THAT GUESSES A NAME SILENTLY FINDS NOTHING AND REPORTS THAT AS A RESULT.**

## 1 · Scope: FULL

Fourteen sourceable fiscal years, **FY2012–FY2025**, every one tier A from a GB Corp
document, every one footed against its own arithmetic before entering the panel. Nine
origins FY2016–FY2024, horizons 1–5, **245 scored cells** across seven drivers.

## 2 · The score

| driver | n | bias (log) | MAE | 95% block bootstrap | vs freeze | vs trend |
|---|---:|---:|---:|---|---|---|
| revenue | 35 | −0.004 | 0.334 | — | **beats at every horizon** | beats at h2–h5 |
| gross_margin | 35 | −0.223 | 0.338 | excludes zero at h4, h5 | **LOSES at h1–h4** | loses at h1–h4 |
| gross_profit | 35 | −0.228 | 0.306 | excludes zero at every h | beats at every horizon | loses at h1–h3, h5 |
| sga | 35 | −0.180 | 0.263 | excludes zero at h1–h4 | beats at every horizon | loses at every horizon |
| operating_profit | 35 | −0.379 | 0.436 | excludes zero at every h | beats at h2–h5 | beats at h4, h5 |
| finance_cost | 35 | +0.401 | 0.890 | **straddles zero at every h** | **LOSES at h1, h2, h4, h5** | beats at h3–h5 |
| net_profit | 15 | −0.692 | 0.761 | excludes zero at h2, h3 | beats at every horizon | loses at h4, h5 |

**The method beats "no change" on revenue, gross profit, SG&A, operating profit and net
profit, and LOSES to it on gross margin and finance cost.** That is said plainly because
[R-FCAL-01] requires it to be: a method that cannot beat "no change" has not earned the
precision it displays, and on two of seven drivers this one has not.

## 3 · Cut-invariance [R-FCAL-01 AMENDED 07-09-2026]

Run through `engine/valuation_calibration/boundary_sensitivity.cuts_for()` rather than
reimplemented, at every boundary leaving five cells each side.

| driver | cuts | sign flips | verdict |
|---|---:|---:|---|
| gross_profit | 6 | **0** | sign holds at every cut |
| operating_profit | 6 | **0** | sign holds at every cut |
| sga | 6 | **0** | sign holds at every cut |
| net_profit | 2 | **0** | sign holds, but only two cuts are admissible |
| gross_margin | 6 | 2 | **the sign depends on where the line was drawn** |
| finance_cost | 6 | 3 | **the sign depends on where the line was drawn** |
| revenue | 6 | **6** | flips at EVERY cut — pooled bias −0.004 is not a bias, it is a mean |

## 4 · The macro/company split

Re-running every origin on the **knowable** IMF WEO vintage at that year-end and on the
**realised** print (`engine/macro_history/EG.json`): mean |macro| 0.089 against mean
|company| 0.315 — **a macro share of 22.1%** over 23 cells, so **78% of the revenue miss is
the company, not the currency**, in a country whose currency lost most of its value inside
the window.

**THE SPLIT'S OWN CHECK READS THE OTHER WAY ROUND HERE AND IS WORTH MORE THAN THE SPLIT.**
The check is that a driver with no inflation term must return a zero macro share by
construction. **This model has no inflation term anywhere** — its revenue rule is the
company's own trailing CAGR — so the split above is attribution AFTER THE FACT rather than a
term the model carries, and that is precisely why the revenue bias flips sign at every cut.

## 5 · One-offs classified

| year | item | treatment |
|---|---|---|
| FY2022 | EGP **8,207.3mn** gain on the MNT-Halan revaluation, inside an EBT of 11,300.4mn | classified as a one-off; net profit is scored with and without it, and its origin's cells are the only ones where the model under-forecasts by more than 10x |
| FY2016–FY2017 | the EGP float; finance cost 1,853.4 and 1,369.9 against operating profit of 866.0 and 618.2 | era boundary A, not an adjustment |
| FY2024–FY2025 | operating profit REDEFINED between release vintages (provisions moved above the line) | presentation only, confirmed by arithmetic: 6,176.6 − 355.7 = 5,820.9 against the later vintage's 5,820.8. Scored on the ORIGINAL vintage at each origin. |
| FY2025 | **the audit opinion is QUALIFIED** — MNT-BV's audited financials were not provided | recorded, never adjusted for |

## 6 · The two named traps, on this name

**(i) INTEREST COMES FROM THE BORROWINGS THAT ACTUALLY BEAR IT — and GBCO is the sharpest
case this book has produced, because the leak runs the OTHER way from the usual one.**

The usual failure is a denominator too broad. Here the **numerator is too narrow**: GB Corp
contains a lender, and **GB Capital's cost of funds is booked inside that segment's cost of
revenue**, not in the group finance-cost line — EGP 3,756.9mn in FY2025 and 2,192.3mn in
FY2024. Three denominators, one numerator, on FY2025:

| construction | rate | against a policy corridor above 24% |
|---|---:|---|
| group finance charge / TOTAL liabilities | **7.05%** | understates by 3.8x |
| group finance charge / group borrowings | **11.27%** | understates by 2.4x |
| whole interest incurred / average borrowings | **26.53%** | **reproduces the CBE lending rate** |

The last is confirmed independently by the company's own segment cash flow: GB Auto's
interest expense for 1H2026 alone is **EGP 2,450.5mn**, which on that leg's own average
borrowings annualises to roughly 22%, right on the disclosed corridor.

The delivered study adopted a Kd of **20.7% — below the 23.00% sovereign**, which a
same-currency corporate cannot borrow at and which `cost_of_capital.py` refuses outright.

**(ii) REVENUE AND COST ON THE SAME RECOGNITION CLOCK.** Both legs recognise symmetrically —
vehicles at delivery with their cost, finance income over the life of the receivable with its
funding cost — so trap (ii) does not fire here. **It is why the legs must be built separately
rather than netted**: the group gross margin blends a 14.3% assembler with a lender whose
"cost of sales" is largely interest.

## 7 · Corrections — none promoted, four watch-flagged

The first clause passes on **gross_profit, operating_profit, sga and net_profit** (sign holds
at every admissible cut). **None is promoted, and the reason is the second clause.**

Every one of the four is an OUTPUT of the same two inputs — revenue, whose bias is −0.004 and
flips at all six cuts, and gross margin, whose bias flips at two. **A correction applied to an
output while its inputs are unstable is a multiplier standing in for a mis-specified margin
rule**, which is [L-002] exactly: a steady error usually means something is wired wrong, and a
fudge factor hides the wiring. All four are recorded as **WATCH FLAGS** — graded live,
revisited at every refit, acted on by nobody.

## 8 · Years 3–5 as ranges [R-FCAL-01 AMENDED 07-09-2026]

Published as **multipliers to apply to a point projection**, with basis, count and
orientation declared:

| driver | h=3 | h=4 | h=5 | basis | orientation | n |
|---|---|---|---|---|---|---|
| revenue | 0.74 – 1.35 | 0.63 – 1.61 | 0.66 – 1.66 | **span** | **actual over forecast** | 7 / 6 / 5 |
| gross_profit | 0.72 – 1.05 | 0.68 – 1.09 | 0.60 – 1.14 | **span** | **actual over forecast** | 7 / 6 / 5 |
| operating_profit | 0.61 – 1.06 | 0.53 – 1.05 | 0.47 – 1.09 | **span** | **actual over forecast** | 7 / 6 / 5 |

**BASIS IS `span`, NOT `percentile`, AND THE DIFFERENCE IS THE WHOLE POINT.** Seven, six and
five observations is the range of seven, six and five numbers. Calling it a p10–p90 would be
the free parameter the promotion rule forbids.

## 9 · Limits, stated

- **No volume-anchored revenue driver.** Unit volumes are disclosed from FY2019 in the
  releases and in the annual-report business reviews before that, but an exogenous Egyptian
  market-size series dated at EVERY origin was not obtained from company documents inside this
  run. The gap is flagged, not filled.
- Balance-sheet items for **FY2018 and FY2019 debt** could not be resolved: those annual
  reports lay the statements out numbers-first in a split two-column form the text layer
  cannot attach to labels, and GB Corp's own statement archive starts at 31 March 2020.
  Recorded as missing with that reason in `valuation_inputs.json`.
- Fifteen cells on net profit and two admissible cuts is thin, and the interval on it is wide.
- **One name. This record is PROVISIONAL and binds nothing.**
