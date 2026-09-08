# SWDY — fundamental walk-forward training record, 7 September 2026

**INTERNAL. Never shown to a reader.** [R-FCAL-01]. This is the FUNDAMENTAL walk-forward —
drivers projected from a past origin and scored against what Elsewedy Electric went on to
report. It is not the price-engine walk-forward (`swdy_study/backtest_5y.py`) and not the
technical one (`engine/lab/ta_calibration/`).

Pre-registration: `PRE_REGISTRATION_07-09-2026.md`, fixed before a single error was
computed and carrying no amendments. Basis breaks: `BASIS_BREAKS_07-09-2026.md`.

---

## 0 · Scope — FULL, and the largest sample this campaign has run

Seventeen sourceable fiscal years, FY2009–FY2025, every one from the company's own
documents: 233 retrieved from `ir.elsewedyelectric.com`, annual audited consolidated
statements for 17 of 19 years, sixteen consecutive annual earnings releases and investor
sheets carrying cable tonnage from FY2012.

**Twelve origins FY2014–FY2025, horizons 1–5, 750 scoreable driver cells and 105 recorded
unscoreable.** For comparison the runs before it scored 25 cells (ARCC) and 9 (AMOC). It
is still one company, and eleven scoreable origins of one issuer are not eleven
independent observations.

## 1 · The headline, and it is the pooled census arriving on a new name

**REVENUE COMES IN 22.2 LOG POINTS ABOVE FORECAST AND COST OF REVENUE 21.5 POINTS ABOVE
IT.** Both are under-forecast by nearly the same amount, so the margin is roughly right
and **the SCALE is systematically too low**. That is precisely the signature
[R-TERM-01] cites from the pooled census across the earlier runs, reproduced here on a
company in a different industry with thirty times the sample.

**And it compounds.** Revenue MAE runs 0.217 at one year to 0.630 at five; gross profit
0.306 to 0.641. The freeze benchmark degrades faster (0.258 → 1.167), which is why the
skill against it IMPROVES with distance.

## 2 · Skill against both naive benchmarks

| horizon | n | revenue MAE | vs FREEZE | vs TREND | gross profit MAE | vs FREEZE | vs TREND |
|---|---|---|---|---|---|---|---|
| 1 | 11 | 0.217 | +15.7% | +0.0% | 0.306 | +7.7% | +6.0% |
| 2 | 10 | 0.421 | +19.5% | **−3.3%** | 0.540 | +3.0% | +20.4% |
| 3 | 9 | 0.644 | +17.7% | **−13.1%** | 0.689 | +16.4% | +21.6% |
| 4 | 8 | 0.681 | +30.3% | **−6.4%** | 0.738 | +21.0% | +30.2% |
| 5 | 7 | 0.630 | +46.0% | **−5.2%** | 0.641 | +40.1% | +38.9% |

**THE METHOD BEATS "NO CHANGE" ON EVERY LINE AND AT EVERY HORIZON, AND IT LOSES TO A
TRAILING THREE-YEAR CAGR ON THE TOP LINE AT FOUR HORIZONS OF FIVE.** That is written down
plainly because it is the finding: on revenue and cost of revenue, a mechanical trend
extrapolation of the company's own recent growth beats a ground-up build off segment
drivers and an exogenous activity anchor. It does NOT lose on gross profit, where the
build wins by 20 to 39 points from the second year out — so what the ground-up
construction is buying is the MARGIN, not the scale.

The reason is visible in the driver table: the contracting leg grew far faster than
Egyptian real GDP over this window (revenue from EGP 2.7bn in FY2014 to EGP 87.1bn in
FY2025), and an activity anchor cannot see a company taking share of a market that is
itself being built. A trend rule can, because it is fitted to the company's own
acceleration. **That is not an argument for the trend rule** — it has no mechanism and
would have been catastrophic through a downturn — but it is an argument against claiming
the ground-up build is better at forecasting scale, and this record does not claim it.

## 3 · The per-driver record, with block-bootstrap intervals

Moving-block bootstrap over ORIGINS, block lengths {2,3,4}, 2,000 resamples, seed 42, all
pre-registered. "over" is the share of cells over-forecast.

| driver | n | bias | MAE | 95% CI | over | vs FREEZE | vs TREND |
|---|---|---|---|---|---|---|---|
| D1 cable volume, tonnes | 20 | +0.250 | 0.256 | [+0.068, +0.360] | 95% | −38.1% | +18.2% |
| D2 cable price per tonne | 20 | −0.026 | 0.433 | [−0.378, +0.712] | 40% | +1.2% | +9.3% |
| D3 cable cost per tonne | 20 | −0.024 | 0.410 | [−0.357, +0.681] | 40% | +2.4% | +10.9% |
| D4 cables revenue | 45 | −0.207 | 0.651 | [−0.984, +0.365] | 40% | +4.5% | −14.7% |
| D5 contracting revenue | 45 | −0.326 | 0.390 | [−0.530, −0.031] | 24% | +49.7% | +30.2% |
| D6 other revenue | 45 | −0.316 | 0.584 | [−0.791, +0.168] | 33% | +25.8% | +29.0% |
| D7 cables cost | 45 | −0.181 | 0.645 | [−0.985, +0.382] | 40% | +5.0% | −54.2% |
| D8 contracting cost | 45 | −0.358 | 0.402 | [−0.546, −0.085] | 22% | +50.1% | +21.2% |
| D9 other cost | 45 | −0.316 | 0.599 | [−0.794, +0.170] | 36% | +25.0% | +32.8% |
| D10 selling, general and administrative | 30 | −0.190 | 0.284 | [−0.385, +0.068] | 33% | +46.2% | +29.7% |
| D11 depreciation and amortisation | 30 | −0.931 | 0.931 | [−1.043, −0.725] | 0% | −88.9% | −204.0% |
| D12 capital expenditure | 45 | −0.679 | 0.826 | [−0.954, −0.234] | 20% | +23.9% | +17.1% |
| D13 other operating income | 45 | −0.862 | 0.993 | [−1.185, −0.531] | 18% | n/a | +6.8% |
| D14 other operating expense | 45 | −0.425 | 0.677 | [−1.015, +0.023] | 38% | n/a | +45.3% |
| D15 finance costs | 45 | −0.880 | 0.919 | [−1.548, −0.416] | 9% | n/a | −2.9% |
| D16 finance income | 45 | −0.869 | 1.139 | [−1.458, −0.175] | 31% | n/a | +31.4% |
| **A revenue** | 45 | −0.222 | 0.494 | [−0.709, +0.201] | 27% | +28.4% | −6.5% |
| **A cost of revenue** | 45 | −0.215 | 0.489 | [−0.726, +0.201] | 31% | +29.8% | −10.9% |
| **A gross profit** | 45 | −0.262 | 0.563 | [−0.633, +0.224] | 31% | +19.7% | +25.6% |

D13, D14, D15, D16 are level-persistence rules and are IDENTICAL TO FREEZE by
construction, as declared in advance; their skill against it is zero by definition and is
reported "n/a — rule equals benchmark" rather than as a measurement.

**D1 is the one driver that runs the other way**, over-forecasting cable tonnage by 28% in
19 cells of 20, and it LOSES to freeze by 38%. Egyptian real GDP growth over-predicts this
company's cable volume: the volume is set by copper price rationing and by which projects
are being wired, not by activity in aggregate. **THE CI DOES NOT COVER ZERO AND THE SIGN
SURVIVES EVERY ADMISSIBLE CUT** — it is the only driver in the table that is both robust
and stable — and it is still not corrected, for the reason in §5.

## 4 · Macro versus company, and the split's own check

Every origin re-run on (a) the macro path known at the origin and (b) perfect foresight of
inflation, currency and activity.

| driver | as known | perfect inflation | perfect all | macro share (all) |
|---|---|---|---|---|
| D1 cable volume | +0.250 | +0.250 | +0.283 | −13.3% |
| D4 cables revenue | −0.207 | −0.180 | −0.172 | 16.9% |
| D5 contracting revenue | −0.326 | −0.265 | −0.256 | 21.6% |
| D7 cables cost | −0.181 | −0.107 | −0.098 | 45.9% |
| D11 depreciation | −0.931 | −0.941 | −0.941 | −1.1% |
| D15 finance costs | −0.880 | −0.880 | −0.880 | 0.0% |
| A revenue | −0.222 | −0.194 | −0.185 | 16.7% |
| A cost of revenue | −0.215 | −0.163 | −0.154 | 28.3% |

**THE SPLIT PASSES ITS OWN CHECK.** D1 carries no inflation term and moves by EXACTLY zero
under perfect-foresight inflation. Its non-zero "macro share (all)" is the ACTIVITY leg,
which it does carry — the check is on the inflation term and it returns zero to machine
precision.

**Perfect foresight of the currency and of inflation removes at most 28% of the error.**
On a company whose currency lost eighty-five per cent of its value inside the window, that
is the important negative result: the misses are the COMPANY — the pace at which it took
contracting share and levered its balance sheet — and looking for a macro fix would waste
the effort.

## 5 · Corrections — NOT ONE PASSES BOTH CLAUSES

Eleven of nineteen drivers are declined before any test: five because the sign FLIPS at
some admissible cut ([R-FCAL-01 AMENDED 07-09-2026] — the era boundary alone is not the
test), and six because the bootstrap interval covers zero.

Eight reach clause one, and four pass it **after that clause was re-pointed**. A first
draft asked only whether a majority of origins improved; both contracting legs passed it
while the MEAN error ROSE (0.256 → 0.282 and 0.268 → 0.272), because the origins that get
worse get worse by more. **A correction that raises the average error has not passed
anything, and a test that calls it a pass is the wrong test** [R-COC-01].

| driver | clause 1 | clause 2 |
|---|---|---|
| D1 cable volume | PASS (3 of 3 origins, MAE 0.077 → 0.037) | **WATCH FLAG** |
| D5 contracting revenue | FAIL (5 of 8 origins, mean MAE rises) | declined |
| D8 contracting cost | FAIL (5 of 8, mean MAE rises) | declined |
| D11 depreciation | PASS (5 of 5, MAE 0.820 → 0.373) | **DECLINED — SPECIFICATION DEFECT** |
| D12 capex | FAIL (4 of 8) | declined |
| D13 other operating income | PASS (6 of 8, 0.840 → 0.687) | **WATCH FLAG** |
| D15 finance costs | PASS (7 of 8, 1.041 → 0.966) | **DECLINED — SPECIFICATION DEFECT** |
| D16 finance income | FAIL (4 of 8) | declined |

**THE SECOND CLAUSE DID ITS JOB TWICE AND BOTH REFUSALS ARE THE POINT.**

**D11 offers the largest improvement any candidate makes and is REFUSED.** The rule rolls
PP&E forward at historical cost plus capex less cost over the disclosed life; the reported
charge is struck on a base that ALSO carries the translation of foreign subsidiaries. Note
17 adds **EGP 9,941,876,468** to the cost of machinery in FY2024 as an "effect of movement
in exchange rates" alone, against additions of EGP 2,061,542,102. A roll-forward that
models the additions and not the translation must under-forecast on a currency that
halved, and it will do so in a NEW way next year rather than the way a multiplier was
fitted to. Every PP&E roll-forward in this book omits the translation term, so it fails
the second clause on its own terms as well. **A specification error is not a calibration
one and no correction factor may hide it.**

**D15 passes on seven origins of eight and is REFUSED, and it is [L-002] in a new
costume.** The rule holds the finance charge flat, which is a flat DEBT BOOK. SWDY's
interest-bearing borrowings went from EGP 6.6bn at FY2014 to EGP 62.5bn at FY2025, nine
and a half times, while the rate on the borrowings that actually bear it went from 5.79%
to 9.37%. The 88 log points of "bias" are the growth of the debt book. **Across this
market's book the house builds finance cost as rate × interest-bearing borrowings** — it
is the first trap [R-FCAL-01] names — so a multiplier on a flat charge is inconsistent
with every other name here. A correction factor is honest when the model is right and
reality is awkward.

**D1 is a WATCH FLAG on sample rather than on principle.** The expanding window leaves
THREE origins with three or more resolved cells, because the unit disclosure closes at
FY2020. Three origins of one issuer is not a population.

**D13 is a WATCH FLAG because a correction there changes the RULE rather than calibrating
it.** The line was DECLARED equal to FREEZE in advance, and other operating income — a
residual of disposals, grants and reversals — is not a driver class this book builds
consistently anywhere, so the second clause has nothing to be consistent WITH.

**Adopted: NONE.** No correction enters the live drivers from this run.

## 6 · The two traps, and whether they bit

**Trap (i) — interest from the borrowings that actually bear it — is closed by
construction and this name makes it unusually easy to fall into.** At 31 December 2025
total liabilities are EGP 239.1bn of which loans and borrowings are EGP 62.5bn: trade and
other payables (68.9), contract liabilities (81.3), amounts due to related parties and
provisions are together more than TWO AND A HALF TIMES the borrowings and not one of them
pays interest. Dividing the finance charge by the liabilities total would have given a
borrowing rate near 2.4% against a real 9.4% and manufactured a bias that looks exactly
like evidence. The rate is formed on loans and borrowings alone at every origin, and the
twelve rates run 3.70% to 13.14%.

**Trap (ii) — one recognition clock — is live on this name in a way it was not on a cement
maker, and it is closed by construction.** SWDY's contracting leg recognises revenue OVER
TIME as work completes; the FY2025 balance sheet carries EGP 29.9bn of contract assets
against EGP 81.3bn of contract liabilities. The scored drivers are MATCHED PAIRS — D4/D7,
D5/D8, D6/D9 — each leg's cost on the same clock as that leg's revenue, and the legs never
mixed. **There is no group-level cost driver in the table, and that is deliberate:** one
would break the matching by construction. [L-295] is the class finding that says why, and
it was produced by this company.

## 7 · Sensitivity, reported and never selected

`w`, the declared blend between the metal-and-currency path and domestic inflation on the
cable price and cost, at 0.5 / 0.7 / 0.9:

| w | revenue bias | revenue MAE | gross profit bias | gross profit MAE |
|---|---|---|---|---|
| 0.5 | −0.232 | 0.470 | −0.278 | 0.558 |
| **0.7 (pre-registered)** | −0.222 | 0.494 | −0.262 | 0.563 |
| 0.9 | −0.213 | 0.522 | −0.246 | 0.570 |

**No verdict in this record turns on `w`.** The bias moves by two log points across the
whole stated range and every sign is unchanged; `w = 0.5` gives the lowest MAE and is NOT
adopted, because a parameter selected on its score is the CRPS-selection mistake in a new
costume.

## 8 · Years three to five, as ranges

`forward_ranges.json`, declared with BASIS, COUNT and **ORIENTATION** — actual over
forecast, so a band of 1.4 to 1.8 says the outturn landed between 1.4 and 1.8 times the
point. Percentile at nine observations or more, otherwise the SPAN, which is a smaller
claim and is labelled as one.

| driver | h=3 | h=4 | h=5 |
|---|---|---|---|
| revenue | 0.542 – 2.596 (percentile, 9) | 0.359 – 3.391 (span, 8) | 0.351 – 3.645 (span, 7) |
| gross profit | 0.463 – 2.864 (percentile, 9) | span, 8 | span, 7 |
| contracting revenue | 0.874 – 2.502 (percentile, 9) | 0.840 – 3.101 (span, 8) | 0.898 – 4.030 (span, 7) |

**They are wide and the width is the finding.** Twelve years containing a currency that
went from seven to forty-eight and a revenue line that grew sixteen and a half times will
not produce a narrow five-year band, and a narrow one would be a claim this record cannot
support.

## 9 · Caveats, plainly

- **One company.** Every number here is Elsewedy Electric's own history. Nothing in it is
  evidence about another name until a second name shows the same thing.
- **The cells are not independent.** Forty-five cells per driver come from eleven
  overlapping origins; the block bootstrap is over origins for that reason and the
  intervals are still optimistic.
- **The unit drivers stop five years before the window does**, so D1–D3 rest on 20 cells
  against 45 for the rest, and their definition window is a fact about the disclosure.
- **The method loses to a trailing CAGR on the top line.** Stated in §2 and not softened.
- **Nothing here has been out-of-sample tested.** Every finding is PROVISIONAL under
  [R-LESSON-01] and the code refuses to write one as adopted.
