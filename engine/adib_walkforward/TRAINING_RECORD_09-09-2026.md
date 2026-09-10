# ADIB (EGX) — FUNDAMENTAL walk-forward: training record

**09-Sep-2026 · INTERNAL — never shown to a reader.** [R-FCAL-01].

**WHICH WALK-FORWARD.** The FUNDAMENTAL one: ADIB-Egypt's drivers rebuilt at eleven past
year-ends from what had been published by each of those dates, projected one to five years
forward, and scored against what the bank actually reported. It is **not** the price-engine
walk-forward (band coverage on the Monte Carlo cone, `{ticker}_study/backtest_5y.py`) and
**not** the technical walk-forward (`engine/lab/ta_calibration/`). Three different tests in
this system are called a walk-forward and this record says which one it is every time.

**WHICH COMPANY.** Abu Dhabi Islamic Bank – Egypt S.A.E., EGX: ADIB, Cairo-listed, EGP,
formerly National Bank for Development. NOT ADIB Group PJSC (ADX: ADIB), the Abu Dhabi
parent, which is the separate covered name ADIBUAE.

**CLASS: `bank`.** The first bank in this campaign. What that meant for the machinery is
section 2 below, and it is the most transferable thing in this record.

---

## 1 · Scope, and the span obtained

**FULL.** Sixteen sourceable consolidated fiscal years, FY2010–FY2025, every one from the
issuer's own audited consolidated statements on adib.eg, plus Q1-2026 and H1-2026. **Every
one of the eighteen statements foots against its own arithmetic** — `panel.py` prints the
failures on import and there are none.

**Where the span stops, and why.** FY2010 is the earliest CONSOLIDATED filing the issuer
publishes; FY2009 exists only as a standalone and a standalone is a different basis. The
window is 16 years rather than the 15 targeted and it stops at the archive's own floor
rather than at a choice.

**Origins FY2014 … FY2024, horizons 1–5, 45 origin-horizon cells per driver, 14 drivers.**
FY2014 is the first year with five years of consolidated history behind it.

**Route.** Seven filings publish their statements as rasters with no text layer. Each was
read TWICE and independently — the largest embedded image at native resolution upscaled,
and a page render — with every disagreement settled by the statement's own arithmetic and,
where that was not decisive, by the comparative column of the following year's filing.
FY2020's balance sheet did not foot on a 400 dpi page render (equity 5,548,307 against a
total-liabilities read of 33,979,364) and foots exactly by the native-image route. Two
figures could be settled only by the footing identity and both are labelled DERIVED.

---

## 2 · A BANK IS NOT AN INDUSTRIAL COMPANY, AND THE TWO NAMED TRAPS DO NOT SURVIVE THE MOVE UNCHANGED

This is the campaign's first bank, and the question the run existed to answer is whether
the walk-forward machinery's industrial shape can carry one. **It can, but only after both
named traps are re-derived rather than copied.**

### Trap 1 — "interest comes from the borrowings that actually bear it." THE RULE HOLDS; ITS EXAMPLE INVERTS.

For an industrial company the rule EXCLUDES customer deposits from the denominator, and the
protocol says so in terms. **For a bank, customers' deposits are the largest thing that
bears the charge.** ADIB-Egypt's `Cost of deposits and similar costs` is precisely the
return paid to depositors, to banks and to subordinated lenders. The denominator here is
customers' deposits plus due to banks plus subordinated financing, on average balances, and
nothing else.

The rule's PRINCIPLE — divide the charge by what actually bears it — is what transfers. Its
EXAMPLE is class-specific, and reading it literally on a bank would have excluded 94 per
cent of the correct denominator. Obeyed structurally rather than remembered:
`bottom_up.interest_bearing()` is the only route to that denominator, and total liabilities
appears nowhere in the build. At FY2025 the two are EGP 293.7bn against EGP 312.1bn — using
the wider figure would understate the funding rate by about a sixth of itself.

### Trap 2 — "revenue and cost on the same recognition clock." THE INDUSTRIAL VERSION CANNOT FIRE; ITS BANK-SHAPED ANALOGUE CAN.

A bank's financing income and its cost of deposits already accrue on the same
effective-yield clock, so percentage-of-completion cannot go wrong here. **The analogue
that can, and that this run had to obey, is that income accrues on AVERAGE balances, not
closing ones.** ADIB-Egypt grew customer financing 54 per cent in FY2025 and its balance
sheet 33 per cent. Applying a yield to a CLOSING balance would credit a full year of income
to half a year of assets and inflate projected net profit by a large, robust, entirely
spurious margin — exactly the shape of the PHDC error in a bank's clothing. Every rate in
the build reaches its base through `_avg()` and by no other route.

### What else did not transfer

No units times price. No capex driving volume and depreciation. No working-capital cycle —
a bank has no inventory, no days sales outstanding, no days inventory, no days payable, and
the valuation-input block records that as MISSING WITH A REASON rather than filling in a
number. The protocol's own volume clause DOES transfer, and it names the bank case
explicitly: *system credit times share*.

---

## 3 · The result, per driver

| driver | n | bias | MAE | bias 90% CI | early | late | over | sign-broken | stable? |
|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| admin | 45 | -0.043 | 0.233 | [-0.177, +0.098] | -0.030 | -0.053 | 36% | 0 | yes |
| cost_funds | 45 | -0.467 | 0.519 | [-0.623, -0.308] | -0.537 | -0.411 | 18% | 0 | yes |
| cust_deposits | 45 | -0.291 | 0.315 | [-0.406, -0.170] | -0.309 | -0.276 | 24% | 0 | yes |
| ecl | 40 | -0.186 | 0.734 | [-0.531, +0.193] | +0.089 | -0.351 | 28% | 5 | **NO — not a bias** |
| fin_customers | 45 | -0.311 | 0.326 | [-0.447, -0.170] | -0.473 | -0.182 | 16% | 0 | yes |
| fin_income | 45 | -0.455 | 0.527 | [-0.632, -0.270] | -0.556 | -0.374 | 22% | 0 | yes |
| net_fees | 45 | -0.185 | 0.427 | [-0.407, +0.048] | -0.138 | -0.223 | 33% | 0 | yes |
| net_funds | 45 | -0.446 | 0.564 | [-0.677, -0.212] | -0.593 | -0.328 | 24% | 0 | yes |
| np | 40 | -0.547 | 0.670 | [-0.829, -0.270] | -0.709 | -0.450 | 22% | 5 | yes |
| np_parent | 40 | -0.550 | 0.677 | [-0.842, -0.266] | -0.725 | -0.445 | 22% | 5 | yes |
| other_nii | 45 | +0.051 | 0.505 | [-0.233, +0.324] | -0.027 | +0.113 | 51% | 0 | **NO — not a bias** |
| other_op | 32 | -0.414 | 0.512 | [-0.633, -0.214] | -0.671 | -0.342 | 19% | 13 | yes |
| pbt | 40 | -0.372 | 0.630 | [-0.688, -0.058] | -0.409 | -0.350 | 35% | 5 | yes |
| total_assets | 45 | -0.313 | 0.359 | [-0.444, -0.173] | -0.336 | -0.295 | 27% | 0 | yes |

**Reading it.** The method under-forecasts almost everything: twelve of fourteen drivers
carry a negative bias, and on attributable profit it is −0.550 in logs — a projection about
58 per cent of the outcome. **Two drivers are NOT biased and are reported as unstable
instead**: expected credit losses (+0.089 early, −0.351 late) and other non-interest income
(−0.027 early, +0.113 late). A bias that changes sign between eras is not a bias.

### By horizon, on attributable profit

| horizon | cells | bias | MAE |
|---|---:|---:|---:|
| h1 | 10 | -0.243 | 0.350 |
| h2 | 9 | -0.460 | 0.661 |
| h3 | 8 | -0.610 | 0.798 |
| h4 | 7 | -0.742 | 0.841 |
| h5 | 6 | -0.893 | 0.893 |

The shortfall widens monotonically with distance, which is the signature of a level
assumption compounding rather than of noise.

---

## 4 · SKILL — and this is the first name in the campaign that beats "no change" on net profit

| driver | cells | model | freeze | trend | vs freeze | vs trend | (model−freeze) MAE 90% CI |
|---|---:|---:|---:|---:|---:|---:|---|
| fin_customers | 45 | 0.326 | 0.680 | 0.182 | +52% | -79% | [-0.484, -0.234] |
| cust_deposits | 45 | 0.315 | 0.690 | 0.160 | +54% | -96% | [-0.480, -0.275] |
| total_assets | 45 | 0.359 | 0.703 | 0.186 | +49% | -93% | [-0.441, -0.247] |
| fin_income | 45 | 0.527 | 0.839 | 0.423 | +37% | -25% | [-0.376, -0.245] |
| cost_funds | 45 | 0.519 | 0.873 | 0.541 | +41% | +4% | [-0.401, -0.299] |
| net_funds | 45 | 0.564 | 0.799 | 0.499 | +29% | -13% | [-0.319, -0.147] |
| net_fees | 45 | 0.427 | 0.615 | 0.659 | +31% | +35% | [-0.328, -0.052] |
| other_nii | 45 | 0.505 | 0.461 | 1.073 | -9% | +53% | [-0.139, +0.224] |
| admin | 45 | 0.233 | 0.361 | 0.260 | +35% | +10% | [-0.221, -0.020] |
| other_op | 18 | 0.412 | 1.328 | 1.972 | +69% | +79% | [-1.884, -0.235] |
| ecl | 25 | 0.663 | 1.058 | 0.881 | +37% | +25% | [-0.693, -0.118] |
| pbt | 30 | 0.587 | 0.903 | 0.585 | +35% | -0% | [-0.412, -0.212] |
| np | 35 | 0.582 | 0.984 | 0.561 | +41% | -4% | [-0.482, -0.311] |
| np_parent | 35 | 0.583 | 0.977 | 0.588 | +40% | +1% | [-0.480, -0.300] |

**Against FREEZE the method wins, decisively, on thirteen of fourteen drivers.** On
attributable profit the MAE is 0.583 against 0.977 — forty per cent better — and the
block-bootstrap interval on the difference is entirely below zero, [−0.480, −0.300]. On
PHDC the method could not beat "no change" on net profit at any horizon. Here it does, and
that is this run's most important result for the campaign as a whole.

**Against TREND it is a dead heat on profit (+1 per cent) and it LOSES BADLY on volume** —
79 per cent worse on financing, 96 per cent worse on deposits, 93 per cent worse on total
assets. That is the second most important number in this record and section 5 is about why.

**The comparison is on the cells all three methods can score**, not on each method's own
population. Comparing a model MAE over 45 cells with a benchmark MAE over 31 is not a skill
measure; `score.skill()` takes the intersection first and reports its size.

---

## 5 · Why it under-forecasts: the flat-share rule, and it is a SPECIFICATION finding

Rule R2 holds ADIB's share of Egyptian private credit FLAT at each origin, because the
protocol anchors volume on an exogenous market driver and *never on the company's own trend
alone*. **ADIB-Egypt has taken share every year for a decade** — from 1.5 per cent of system
credit at the FY2014 origin to 2.5 per cent at FY2024, a trailing drift of about 8.7 per
cent a year. So the rule was wrong in the same direction at all eleven origins.

The decomposition at the cleanest origin makes it unmistakable. Projecting FY2025 from
FY2024, one year out, EGP million:

| line | projected | actual | ratio |
|---|---:|---:|---:|
| financing to customers | 112,697 | 147,226 | 0.765 |
| total assets | 273,742 | 346,711 | 0.790 |
| net income from funds | 16,250 | 20,152 | 0.806 |
| **net fees** | **2,686** | **2,730** | **0.984** |
| **other non-interest income** | **797** | **721** | **1.106** |
| **administrative expenses** | **3,076** | **3,431** | **0.897** |
| attributable profit | 9,122 | 12,589 | 0.725 |

**The rate drivers are essentially right. The asset base is 21 per cent too small.** The
profit miss traces almost entirely to the volume anchor.

**REPORTED, NEVER SELECTED — the sensitivity R2 was not allowed to become.** Letting the
share drift at its own trailing rate instead of holding it flat moves the financing bias
from −0.311 to −0.064 and the MAE from 0.326 to 0.238. That is a large improvement and **it
is not adopted**, because adopting it means anchoring volume on the company's own trend,
which is the thing the protocol forbids. The number is on the record so the next bank knows
what the conservatism costs.

---

## 6 · Macro versus company

| driver | MAE as pre-registered | MAE on perfect macro | macro share | company share |
|---|---:|---:|---:|---:|
| fin_customers | 0.326 | 0.185 | 43% | 57% |
| cust_deposits | 0.315 | 0.173 | 45% | 55% |
| total_assets | 0.359 | 0.177 | 51% | 49% |
| fin_income | 0.527 | 0.378 | 28% | 72% |
| cost_funds | 0.519 | 0.397 | 23% | 77% |
| net_funds | 0.564 | 0.391 | 31% | 69% |
| net_fees | 0.427 | 0.271 | 36% | 64% |
| other_nii | 0.505 | 0.413 | 18% | 82% |
| admin | 0.233 | 0.109 | 53% | 47% |
| other_op | 0.512 | 0.414 | 19% | 81% |
| ecl | 0.734 | 0.700 | 5% | 95% |
| pbt | 0.630 | 0.397 | 37% | 63% |
| np | 0.670 | 0.517 | 23% | 77% |
| np_parent | 0.677 | 0.523 | 23% | 77% |

**The split's own check, in its bank form.** The protocol's check is that a unit volume
driver carries no inflation term and must return a zero macro share by construction. A bank
has no unit driver — every line it reports is nominal EGP — so the equivalent is ADIB's
SHARE of system credit: numerator and denominator are nominal EGP of the same year, so
inflation cancels identically. Measured rather than asserted: share-driver macro-invariance check: max |difference| = 0.000e+00 **PASS, exactly.**

**Only 23 per cent of the net-profit miss is macro.** Give the model perfect foresight on
Egyptian inflation and on the size of the credit system — through a 2016 float and three
devaluations — and it still misses attributable profit by an MAE of 0.523 against 0.677.
The devaluations are not the story; the share assumption is.

---

## 7 · The era sub-sample, reported and not selected

Basis break B2 puts FY2010–FY2013 in a loss-making, recapitalising era, so the FY2014 and
FY2015 origins carry loss years inside their trailing windows. Every result above was
recomputed on the nine origins from FY2016, whose whole five-year window sits in the profit
era. **It does not change the story**: the attributable-profit bias moves from −0.550 to
−0.438 and the MAE from 0.677 to 0.583, and the skill against freeze is +40 per cent either
way. Neither sample is the headline; both are printed. Choosing between them after seeing
the scores is the selection mistake the pre-registration exists to stop.

**The FY2014 origin is the record's worst and it is kept.** Its cost-of-risk driver reads
6.25 per cent because the FY2012 legacy-book clean-up sits inside its trailing window, and
it projects a LOSS at every horizon — five sign-broken net-profit cells, the only ones in
the record. That is what a mechanical rule does when a trailing mean spans a restructuring,
and deleting the origin would be deleting the finding.

---

## 8 · Corrections — ZERO PROMOTED

Expanding window only, half strength, applied only where the bias holds its sign across
eras, reset at break B2, aggregates rebuilt from adjusted drivers and tested adjusted
against raw BY ORIGIN.

| driver | first clause: adjusted vs raw, by origin | sign across eras | verdict |
|---|---|---|---|
| fin_customers | PASS (6 of 9 origins, 0.246 -> 0.209) | stable | **WATCH FLAG** — passes its own by-origin test (6 of 9 origins improve, MAE 0.246 -> 0.209) and FAILS the second clause. The bias is the flat-share rule in R2, which is how EVERY name in this book anchors volume. A +36% volume uplift on ADIB alone would be a per-name growth premium nothing else carries — and worse, a multiplier over a rule that is provably wrong on this name is arithmetic hiding a specification, which is exactly what L-002 forbids. |
| cust_deposits | PASS (6 of 9 origins, 0.302 -> 0.257) | stable | **WATCH FLAG** — the same driver propagated through R3. Same verdict, same reason. |
| total_assets | PASS (6 of 9 origins, 0.338 -> 0.290) | stable | **WATCH FLAG** — the same driver propagated through R4. Same verdict, same reason. |
| fin_income | PASS (6 of 9 origins, 0.484 -> 0.427) | stable | **REFUSED — AGGREGATE** — an OUTPUT of the volume driver times the yield driver. The yield driver is close to unbiased; the whole bias is the volume base. Correcting the income line as well would apply the volume correction twice. |
| cost_funds | PASS (7 of 9 origins, 0.516 -> 0.443) | stable | **REFUSED — AGGREGATE** — as fin_income: an output of the same volume base times the funding rate. |
| net_funds | PASS (6 of 9 origins, 0.463 -> 0.427) | stable | **REFUSED — AGGREGATE** — the difference of the two above. |
| net_fees | FAIL (4 of 9 origins, 0.383 -> 0.431) | stable | **DECLINED** — fails its own by-origin test: only 4 of 9 origins improve and mean MAE RISES from 0.383 to 0.431. |
| other_nii | not testable — no origin carried a correction | SIGN FLIPS | **NOT A BIAS** — the sign flips between eras (-0.027 early, +0.113 late). Reported as instability and not corrected for. |
| admin | FAIL (3 of 9 origins, 0.233 -> 0.256) | stable | **DECLINED** — fails its own by-origin test: 3 of 9 origins improve and mean MAE rises from 0.233 to 0.256. The bias is -0.043 and its confidence interval spans zero. |
| other_op | PASS (5 of 7 origins, 0.329 -> 0.263) | stable | **WATCH FLAG** — passes (5 of 7 origins, MAE 0.329 -> 0.263) but the line flips sign between income and expense — 13 of its 45 cells are sign-broken — and a correction estimated across a sign flip is not a correction. |
| ecl | not testable — no origin carried a correction | SIGN FLIPS | **NOT A BIAS** — the sign flips between eras (+0.089 early, -0.351 late). This is the cost-of-risk driver and it is the one a bank study most wants a correction on; the rule refuses it and the rule is right. |
| pbt | PASS (6 of 9 origins, 0.570 -> 0.532) | stable | **REFUSED — AGGREGATE** — an output of every driver above it. |
| np | PASS (6 of 9 origins, 0.595 -> 0.511) | stable | **REFUSED — AGGREGATE** — as pbt. |
| np_parent | PASS (6 of 9 origins, 0.596 -> 0.512) | stable | **REFUSED — AGGREGATE** — as pbt. |

**Four watch flags, six refused as aggregates, two declined on their own test, and two are
not biases at all. Nothing is promoted, and no correction from this record enters the live
drivers.**

**The second clause did the work again.** The volume correction passes its own test
convincingly — six of nine origins improve and the MAE falls — and it is refused because
the bias it corrects is the flat-share rule, which is how every name in this book anchors
volume. Bolting a 36 per cent uplift onto ADIB alone would be a per-name growth premium
nothing else carries, and it would be a multiplier laid over a specification this record
has already shown to be wrong on this name. **A steady error usually means something is
wired wrong; the fix is the wiring, and the wiring here is a deliberate house conservatism
rather than a defect.** [L-002, L-003.]

**What went into the live study instead.** Two things and only two: the years three to five
ranges, built from this record's own attributable-profit error dispersion; and the knowledge
that a flat-share rule under-forecasts this name, which is why the study's share path is
explicit, disclosed and audited in the gap review rather than held flat. No multiplier.

**Guidance ledger: empty, and that is itself a finding.** ADIB-Egypt publishes no numeric
forward guidance in any of the eighteen filings parsed. There is nothing to score and
nothing was consumed.

---

## 9 · Caveats

- **One year is a comparative, not an original.** No English FY2021 consolidated filing
  exists on the issuer's site; the file published under that name is the Arabic filing.
  FY2021 comes from the FY2022 comparative column. Tier A, same issuer, but if FY2022's
  auditors restated FY2021 this panel carries the restatement. It is the one row where
  point-in-time discipline could not be fully honoured, and it is an ORIGIN, so the risk is
  that its trailing window is marginally cleaner than a FY2021 reader would have had.
- **The confirmation sample is three origins.** FY2014, FY2019 and FY2024 share no target
  year. Three is small, and no correction was promoted on it.
- **Eleven origins on one company.** Every finding here is provisional. The class finding
  in section 2 is the one most likely to travel and it has been tested on exactly one bank.
- **`other_op` carries 13 sign-broken cells of 45**, because the line is income in FY2015
  and FY2016 and an expense elsewhere. Its bias is reported and its correction is
  watch-flagged rather than declined, but it is the weakest driver in the record.

---

## 10 · The Fundamental Driver Ledger entry

Appended separately. The short form: a bank's drivers are a balance sheet that grows, a
spread earned on it, a loss rate charged against it, a fee annuity, an overhead base and a
tax rate; the spread is an OUTPUT of two rate inputs and is never typed; every rate is
applied to average balances; and the funding charge is divided by the deposits, bank
borrowings and subordinated financing that bear it, and by nothing wider.
