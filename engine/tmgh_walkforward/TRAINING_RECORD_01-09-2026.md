# TMGH — fundamental walk-forward training record

**Instrument:** Talaat Moustafa Group Holding (EGX:TMGH) · market EG · exchange EGX
**Run date:** 1 September 2026 · **Standing rule:** [R-FCAL-01]
**Scope:** FULL run — 16 sourceable fiscal years, ten scored origins, horizons 1–5.
**Status:** INTERNAL. The training record, the panel, the error tables and the
pre-registration are never shown to a reader. Nothing here reaches the live site.

Companion files, fixed before any error was computed:
`PRE_REGISTRATION_01-09-2026.md` · `BASIS_BREAKS_01-09-2026.md`

---

## 1. What was tested, and what it is not

This is the **FUNDAMENTAL** walk-forward [R-FCAL-01]: the driver model is rebuilt as it
stood at each past year-end, projected forward, and each driver scored against what the
company actually reported. It is not the price-engine walk-forward [R-CAL-02], which tests
the probability cone, and it is not the technical walk-forward [R-TCAL-01], which tests the
shipped chart read. The three test different machinery on different evidence and none
substitutes for another.

## 2. Data — what was obtained, and where it stops

**Every figure comes from a document TMG published itself.** The company's investor-relations
archive was resolved live and 138 of 140 wanted documents downloaded — 25 consolidated
financial statements, 60 earnings releases back to FY2007, 19 investor presentations, market
updates and executive-management reports. Two links on the company's own site are dead (the
1H2009 and 2Q2017 releases); both attempts are logged in `fetch_attempts.json` rather than
quietly dropped.

**SIGCM clause 1 is satisfied.** FY2023, FY2024 and FY2025 come from the audited consolidated
statements, and every 2026 quarter disclosed to date (Q1 2026, H1 2026) likewise.

**Nothing entered the panel on an extractor's confidence.** Each document's reading of each
year was footed against the identities the statement itself asserts — segment gross profits,
their sum, revenue and cost cross-foots, the profit waterfall and the balance-sheet
identities — and footed at BLOCK level, one document-year at a time. Where an identity broke,
the cells it implicated were dropped unless a different identity that foots vouched for them.
Nothing was repaired: repairing means choosing which reading to overwrite, and that choice is
a guess.

**Span obtained: FY2009 and FY2011–FY2025.** FY2007, FY2008 and FY2010 were published and the
releases are held, but survive only as scans whose summary tables do not resolve into columns;
fewer than twelve cells per year survive footing. They are excluded and the reason is stated.
Nothing was estimated to extend the window.

**What is not disclosed, and was left empty rather than filled:**

* FY2017 new sales. The FY2018 release gives 62% growth, from which EGP 13.1bn follows
  arithmetically. That is an inference, not a disclosure.
* Any continuous unit-count series. TMG publishes unit counts occasionally — 2,991 delivered
  in FY2021, 4,091 in FY2022, 2,661 in FY2023, 3,196 in FY2025, 6,102 units sold in FY2022 —
  and never as a series. A price-per-unit driver built on those would divide one year's value
  by another year's count, the arithmetic error [L-010] records. **The unit level is not
  available for this issuer**, and the build stands at SEGMENT level with the gap stated.
* Backlog before FY2018, disclosed only as "approximately EGP 20 BN" and recorded at that
  precision.

## 3. Four extraction defects, found and fixed rather than absorbed

A fabricated or misread cell corrupts the very error it is scored on, so each of these was
fixed in the extraction and the affected results re-run:

1. **Multi-part note references read as figures.** TMG prints "Depreciation and amortization
   (39+765+4) (491,823,556)". A positional note-skipping rule handled "(33)" and "(3)" and
   missed the multi-note forms, reading 39 and 478 as the figures and putting a D&A of EGP
   0.0mn into FY2023 and FY2025. That produced a D&A bias of **+2.406 log — a 70x
   over-forecast — which was robust across every bootstrap block and entirely an artefact.**
   Note references are now stripped by shape before tokenising. The corrected bias is −0.253.
2. **A scale read from the document family rather than the table.** The pre-2018 releases
   EMBED the audited statements, which report in LE, while the same release's own summary
   tables report in EGP mn. Balance sheets a million times too large footed perfectly, because
   every identity is scale-invariant. The unit is now read per table and checked against the
   size of the company.
3. **An interim statement read as a full year.** "TMG Consolidated F S 9-2020" carries no
   month a filename reader can see. The reporting period is now read from the statement's own
   heading, and an interim contributes only its balance-sheet comparative — under IAS 34 that
   is the preceding year end, while its income statement comparative is the prior interim.
4. **A merge that made identities hold on top of wrong readings.** The first panel merged
   cell-by-cell across documents and then repaired until the identities held. They duly did.
   An identity satisfied by a set of wrong numbers is not evidence.

## 4. Point-in-time discipline, and a real restatement

TMG **restated FY2024** in its FY2025 statements. The FY2025 comparative column is labelled
"(Restated)" and the note explains it as a purchase-price allocation completed inside the
twelve-month measurement period after the seven-hotel acquisition:

| line | as first reported | restated | movement |
|---|---:|---:|---:|
| Hospitality cost | (4,726.6) | (6,024.7) | (1,298.0) |
| Gross profit | 15,300.2 | 14,002.2 | (1,298.0) |
| Net profit | 14,467.5 | 12,769.5 | (1,698.0) |
| Attributable net profit | 10,723.1 | 9,025.1 | (1,698.0) |
| EPS (EGP) | 4.68 | 4.38 | (0.30) |

The net-profit movement is exactly the retained-earnings adjustment the note discloses
(−1,698,008,412), which foots. **Every origin sees FY2024 as first reported**; the restatement
is recorded beside it, never substituted. This is enforced by the panel's ranking rule, not by
remembering to do it.

## 5. Results — per driver, pooled over horizons, as-known macro

Bias and MAE are mean and mean-absolute log error. "Robust" means the bootstrap sign holds
across block lengths {2,3,4}. Costs are scored on magnitude — their sign is a presentation
convention, and scoring them signed would have made every cost cell an undefined log and
dropped the whole cost side of the model from the record.

| driver | n | bias | MAE | over-forecast | robust | E2 | E3 |
|---|---:|---:|---:|---:|:--:|---:|---:|
| new sales | 33 | **−0.877** | 1.022 | 24% | YES | −0.27 | −1.32 |
| development revenue | 35 | −0.055 | **0.276** | 31% | no | −0.09 | −0.02 |
| development cost | 35 | −0.105 | 0.289 | 23% | no | −0.08 | −0.12 |
| recurring revenue | 40 | −0.112 | 0.698 | 48% | no | +0.18 | −0.40 |
| recurring cost | 40 | −0.044 | 0.610 | 50% | no | +0.17 | −0.26 |
| total revenue | 35 | −0.090 | 0.365 | 37% | no | −0.04 | −0.13 |
| gross profit | 35 | −0.079 | 0.421 | 37% | no | −0.05 | −0.10 |
| SG&A | 16 | −0.107 | 0.458 | 31% | no | +0.33 | −0.17 |
| D&A | 30 | −0.253 | 0.435 | 20% | YES | −0.36 | −0.20 |
| finance cost | 30 | **−1.224** | 1.224 | 0% | YES | −1.12 | −1.28 |
| net profit | 34 | **+0.264** | 0.677 | 74% | no | +0.58 | +0.02 |
| customer advances | 11 | +0.230 | 0.627 | 73% | no | +0.60 | −0.21 |
| development properties | 25 | −0.528 | 0.528 | 0% | YES | −0.32 | −0.59 |
| backlog | 35 | −0.284 | 0.441 | 29% | YES | −0.12 | −0.42 |
| PP&E | 30 | −0.459 | 0.808 | 50% | no | +0.04 | −0.71 |

Bootstrap intervals on the robust cells, block lengths {2,3,4}:

| driver | L=2 | L=3 | L=4 |
|---|---|---|---|
| new sales | [−1.50, −0.32] | [−1.59, −0.48] | [−1.58, −0.41] |
| finance cost | [−1.48, −0.80] | [−1.50, −0.77] | [−1.43, −0.81] |
| development properties | [−0.63, −0.31] | [−0.62, −0.31] | [−0.60, −0.39] |
| backlog | [−0.58, −0.01] | [−0.61, −0.09] | [−0.61, −0.10] |
| D&A | [−0.43, −0.09] | [−0.42, −0.01] | [−0.33, −0.16] |

### What the two headline numbers mean

**The backlog-conversion rule works.** Development revenue — the largest line and the one the
valuation turns on — comes back with a bias of −0.055 and an MAE of 0.276 across 35 cells. For
a company that recognises revenue on handover, converting a disclosed order book at its own
trailing rate is a genuinely forecastable process, and this is the strongest positive result in
the record.

**The volume rule does not.** New sales miss low by 0.877 log — the projection is about 42% of
the outcome — robustly, across every block length, in both eras. This is the class lesson
[L-101] in its strongest form: **volume is set by the launch calendar, and no demographic
anchor can see it.** Contracted sales run EGP 33.2bn (FY2022) → 142.8 → 504.0 → 382.2 across
FY2023–FY2025 on the SouthMed and Spine launches. Nothing anchored on population and inflation
can see a launch. The pre-registration said this in advance, in §9(3), so the finding is a
measurement rather than a discovery — but its SIZE is new: PHDC's equivalent miss was −19%,
TMGH's is −58%.

## 6. Skill against the naive benchmarks

MAE, lower is better. `freeze` = every line flat at the last actual; `trend` = trailing
three-year CAGR.

| driver | h | model | freeze | trend | verdict |
|---|--:|--:|--:|--:|---|
| total revenue | 1 | 0.216 | 0.231 | **0.104** | beats freeze only |
| total revenue | 3 | 0.449 | 0.674 | **0.297** | beats freeze only |
| total revenue | 5 | 0.460 | 1.043 | **0.286** | beats freeze only |
| development revenue | 1 | 0.272 | **0.198** | **0.110** | **BEATS NEITHER** |
| development revenue | 5 | 0.357 | 0.965 | **0.330** | beats freeze only |
| gross profit | 1 | 0.231 | 0.247 | **0.144** | beats freeze only |
| gross profit | 5 | 0.486 | 0.948 | **0.437** | beats freeze only |
| net profit | 1 | 0.511 | **0.364** | 0.459 | **BEATS NEITHER** |
| net profit | 3 | **0.712** | 0.870 | 1.527 | beats both |
| net profit | 5 | **0.808** | 1.380 | 2.106 | beats both |
| new sales | 1 | 0.532 | **0.513** | 0.600 | beats trend only |
| new sales | 3 | **1.174** | 1.498 | 1.233 | beats both |

**A method that cannot beat "no change" has not earned the precision it displays.** At one
year out, the bottom-up build is worse than freezing last year's number on both development
revenue and net profit. That is not a figure of speech and the record states it. What the
build earns is the LONG horizons: at three to five years it beats both benchmarks on net
profit, where a trailing CAGR compounds into nonsense (trend MAE 2.106 at h=5). The honest
summary is that this method is a five-year instrument that adds nothing at one year, where the
last reported number is a better forecast.

## 7. Macro versus company

Each projection is run twice — on the information set the origin actually had, and on perfect
foresight of realised inflation. The difference is the macro share.

| driver | as-known | perfect foresight | macro part |
|---|---:|---:|---:|
| new sales | −0.877 | −0.801 | −0.075 |
| development revenue | −0.055 | −0.021 | −0.035 |
| total revenue | −0.090 | −0.048 | −0.042 |
| gross profit | −0.079 | −0.039 | −0.040 |
| net profit | +0.264 | +0.307 | −0.043 |
| customer advances | +0.230 | −0.042 | **+0.272** |
| finance cost | −1.224 | −1.224 | **+0.000** |
| development properties | −0.528 | −0.528 | +0.000 |

**Almost none of the miss is macro.** Even across three currency devaluations, perfect
foresight of Egyptian inflation removes 4 percentage points of a 9-point revenue miss and
8 of an 88-point new-sales miss. The company error dominates everywhere except customer
advances, where the macro part is the larger half.

**The split carries its own check and it passes.** Finance cost's rule has no inflation term
in it, and its macro share comes back as exactly zero by construction. The check is printed by
`score.py` rather than asserted.

## 8. Error decomposition

Each driver set to its actual value one at a time, the aggregate rebuilt, the reduction in
absolute error attributed to that driver.

| aggregate | driver | share of absolute error |
|---|---|---:|
| total revenue | development revenue | 44.6% |
| total revenue | recurring revenue | 42.7% |
| gross profit | recurring revenue | 19.3% |
| gross profit | development revenue | 4.4% |
| gross profit | recurring cost | **−77.6%** |
| gross profit | development cost | **−108.6%** |
| net profit | gross profit | 54.6% |
| net profit | SG&A | −12.3% |
| net profit | finance cost | −10.6% |

**The negative shares are the finding, not a bug.** Substituting the ACTUAL cost makes the
gross-profit forecast worse. Cost is projected as a fixed ratio of revenue, so an
under-forecast revenue drags an under-forecast cost with it and the two errors partly cancel.
Gross profit therefore looks more accurate than either of its parts, and part of that accuracy
is offsetting error rather than skill. Any reader of the gross-profit MAE should know that.

## 9. One-offs identified

| year | item | size | source |
|---|---|---|---|
| FY2023 | non-core land transaction inside new sales | EGP 47.9bn of the EGP 142.8bn total | FY2023 release |
| FY2024 | seven-hotel acquisition (39% with management rights) | hospitality revenue 3,540.9 → 11,496.5 | FY2024 statements |
| FY2024 | investment-property revaluation surplus | EGP 4,924.1mn | FY2024 statements |
| FY2024 | gain on the hotels acquisition | EGP 718.8mn | FY2024 statements |
| FY2024 | SouthMed launch (July 2024) | contracted sales 142.8 → 504.0 EGP bn | FY2024 release |
| FY2025 | investment-property revaluation surplus | EGP 3,952.5mn | FY2025 statements |
| FY2025 | first Saudi revenue (Banan), percentage-of-completion | 52.5% of segment revenue by 1H2026 | FY2025 statements, 1H2026 release |

Net profit's +0.264 bias is measured against actuals that INCLUDE the FY2024 and FY2025
revaluation surpluses (EGP 8.9bn between them), which the model does not forecast and should
not. Stripping them would make the over-forecast larger, not smaller.

## 10. Corrections — four adopted, one blocked, ten refused

Expanding window only, half strength, applied only where the bias holds its sign across eras,
reset after a structural break, and — the clause that does the real work — only where the
correction matches how that driver class is built across the market's book.

| driver | bias | robust | eras | MAE raw → adjusted | outcome |
|---|---:|:--:|:--:|---|---|
| new sales | −0.877 | YES | same | 1.587 → 1.440 | **adopted**, half strength |
| development properties | −0.528 | YES | same | 0.308 → 0.145 | **adopted**, half strength |
| backlog | −0.284 | YES | same | 0.546 → 0.509 | **adopted**, half strength |
| D&A | −0.253 | YES | same | 0.629 → 0.584 | **adopted**, half strength |
| finance cost | −1.224 | YES | same | 0.812 → 0.445 | **WATCH FLAG** — see below |
| PP&E, recurring revenue, recurring cost, SG&A, customer advances | | no | FLIP | | refused |
| development revenue, development cost, total revenue, gross profit, net profit | | no | same | | refused — bias not robust |

### The blocked correction, and why the second clause matters

The finance-cost correction passed its own test **convincingly** — MAE 0.812 → 0.445, robust
across every block length, sign holding in both eras, zero origins over-forecast. On its own
test it is the best correction in the record. It is **not adopted**.

TMG's reported finance cost is not interest on its borrowings alone. The FY2025 note splits it
into finance expenses of EGP 3,820.4mn and bank charges of EGP 116.2mn, against opening
interest-bearing debt of EGP 8,928mn — an implied **44%**, against an Egyptian policy rate that
peaked near 27.25%. The excess is the unwinding of the significant financing component the
company recognises on customer contracts (FY2025 statements, note 2.3) plus factoring charges,
neither of which arises on a loan. The statements do not disclose the split, so the ratio this
run measures is an **effective charge per unit of borrowing, not a borrowing rate**.

Every other Egyptian study in this book builds interest from named facilities at their own
rates against the borrowings that actually bear it. Correcting a driver whose numerator and
denominator do not describe the same thing would be a multiplier over a mis-specification.
**This is the same species as the correction blocked on PHDC, reached from the opposite
direction: there the DENOMINATOR was too broad, here the NUMERATOR is.** That the clause has
now caught the same disease twice, in mirror image, is itself the argument for keeping it.

### The adopted new-sales correction, and what it does not license

The correction passed both gates as the rule requires, and it is adopted for the record. Two
things must travel with it:

* **Its magnitude is entirely regime-dependent** — E2 −0.27 against E3 −1.32, a factor of five.
  The sign holds, which is what the pre-registered gate tests, but a correction estimated on
  the pre-launch era would have been a fifth of what the launch era needed.
* **The expanding-window estimator zeroes it at the launch origins.** The two-sigma structural
  break fires at FY2024 and FY2025, so the correction carried into the forward projection is
  **0.000** — the pre-registered reset working exactly as designed, and the reason the forward
  path below is the raw mechanical path.

## 11. The forward projection, and what it is for

Origin FY2025 is struck but unresolved. Years 3–5 are published as RANGES built from this
record's own driver-error distribution [L-011], never as points. The band's own median is
reported as the centre: where the method has a standing bias, its point estimate sits outside
the band it earns, and saying so is the purpose of measuring the bias.

| driver | FY2026 model | band median | band (p10–p90) | n |
|---|---:|---:|---|--:|
| development revenue | 58,890 | 63,809 | 34,636 – 67,930 | 9 |
| recurring revenue | 46,304 | 55,216 | 32,711 – 71,835 | 10 |
| total revenue | 105,194 | 111,477 | 75,360 – 124,055 | 9 |
| gross profit | 36,051 | 36,955 | 25,750 – 46,364 | 9 |
| net profit | 24,837 | 15,253 | 10,711 – 18,520 | 8 |

| driver | FY2030 model | band median | band (p10–p90) | n |
|---|---:|---:|---|--:|
| development revenue | 265,066 | 350,505 | 198,631 – 554,340 | 5 |
| total revenue | 746,263 | 899,167 | 398,140 – 2,222,229 | 5 |
| net profit | 201,879 | 141,528 | 44,134 – 743,411 | 5 |

**These are not the study's forecast, and must not become it.** The mechanical path compounds
a launch-boom intensity anchor at roughly 68% a year and reaches EGP 746bn of revenue by
FY2030, which is a statement about the rule, not about the company. The walk-forward's two
purposes are per-driver bias detection and calibrated ranges on years 3–5; **a better point
estimate is a by-product and never the aim**, and tuning toward one is the CRPS-selection
mistake in a new costume. What the update carries forward is the ERROR DISTRIBUTION, the four
adopted corrections and the blocked one — not this path.

The FY2030 net-profit band spans a factor of seventeen on five observations. That width is the
honest answer, and it is the argument for publishing a range.

## 12. Guidance ledger — scored, never consumed

| guidance for | target | outcome | direction | log error |
|---|---|---:|---|---:|
| FY2021 new sales | EGP 30bn (raised mid-year) | 32,400 | under-promised | −0.077 |
| FY2022 new sales | EGP 24–26bn | 33,200 | under-promised | −0.284 |
| FY2024 | "internal sales targets", no figure published | 504,000 | not gradeable | — |

Mean log error of the two gradeable targets: **−0.180** — management guided BELOW the outcome
in both. Note the direction: TMG's published guidance has been conservative, and the model's
own new-sales driver leans the same way, only much harder. Guidance is scored, never used as
an input [L-012]. On this name, feeding it in would have improved the forecast — and that is
exactly why the rule is a rule: two observations of under-promising is not a property of the
company, and a driver that consumed guidance would inherit whatever lean the next cycle brings.

## 13. Caveats, stated plainly

1. **One name.** Nothing here is evidence about developers in general. Every lesson this run
   produces is filed PROVISIONAL under [R-LESSON-01].
2. **The cells are not independent.** Ten origins × five horizons is 40 cells drawn from
   fifteen years of one company; overlapping horizons share outcome years. The block bootstrap
   is the response and it does not make the sample large. Several intervals straddle zero, and
   the non-overlapping confirmation set is two origins.
3. **The launch calendar dominates the late origins**, and it is what the new-sales bias is
   mostly measuring.
4. **The devaluation era carries most of the nominal growth** — four of fifteen years.
5. **The recognition break is live, not historical.** The Saudi percentage-of-completion leg
   starts in the last panel year and is already 52.5% of segment revenue by 1H2026. The scored
   record describes a company whose development revenue basis is currently changing.
6. **Backlog before FY2018 is approximate**, and δ at the early origins inherits that roundness.
7. **Three fiscal years are missing** from the front of the window and one new-sales cell from
   its middle, for stated reasons.
8. **The gross-profit accuracy is partly offsetting error**, per §8.
