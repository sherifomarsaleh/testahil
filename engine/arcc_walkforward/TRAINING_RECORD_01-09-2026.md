# ARCC — fundamental walk-forward, training record

**Run 1 September 2026** under [R-FCAL-01], to `PRE_REGISTRATION_01-09-2026.md`, which was
written before a single error was computed and carries no amendments.

**INTERNAL. Never shown to a reader of the study.** The two documents this run must produce
are the rebuilt fundamental analysis and the updated lessons register; this record, the panel,
the error cells and the pre-registration are evidence behind them.

**Which walk-forward this is:** the FUNDAMENTAL one — drivers projected from a past origin and
scored against what the company actually reported. Not the price-engine walk-forward (band
coverage on the Monte Carlo cone) and not the technical walk-forward.

Ticker ARCC · Arabian Cement Company S.A.E. · EGX · class cement and heavy industrial.

---

## 1 · What was run

**Scope: FULL.** Twelve sourceable fiscal years, **FY2014–FY2025**, every one from ARCC's own
audited consolidated financial statements on its own investor-relations archive. Eight origins
(FY2018–FY2025), horizons 1–5, **25 scoreable origin-horizon cells per driver** (20 on the
profit lines, where FY2020's negative profit before tax has no log error and the five cells
that target it are counted as unscoreable rather than dropped quietly).

**Provenance.** 128 primary documents retrieved from the company's own site, every attempt
logged including the failures (`fetch_attempts.json`). Every financial figure is tier A —
the audited statements. Every physical figure is tier A COMPANY_IR — the company's own
earnings releases and presentations, tagged separately because the statements carry no tonne.
No vendor, aggregator or press figure enters the panel.

**Footing.** 97 arithmetic identities are asserted at import and the panel does not load if any
fails. That is not ceremony on this name: every ARCC statement page is a SCAN, and the OCR
misreads a leading 1 as a 2. Five figures came off the page wrong and looking perfectly clean,
and each was caught only because a printed subtotal refused to agree with its parts — then
confirmed independently by the following year's comparative column. **Arithmetic is the
arbiter, not the extractor's confidence.**

---

## 2 · The headline result

**The method beats both naive benchmarks on every aggregate that matters.**

| line | n | bias | MAE | skill vs FREEZE | skill vs TREND |
|---|---|---|---|---|---|
| revenue | 25 | −0.278 | 0.483 | **+0.261** | **+0.177** |
| cost of sales | 25 | −0.245 | 0.379 | **+0.228** | **+0.211** |
| gross profit | 25 | −0.312 | 1.265 | **+0.349** | **+0.530** |
| profit before tax | 20 | −0.457 | 1.381 | **+0.431** | **+0.581** |
| profit after tax | 20 | −0.405 | 1.393 | **+0.434** | **+0.578** |
| total volume | 25 | −0.019 | 0.151 | +0.037 | +0.334 |

**This is the first name in this project where the answer to "can the method beat no change?"
is yes on net profit.** On PHDC it could not, at any horizon, and the protocol says plainly
that a method which cannot beat "no change" has not earned the precision it displays. Here it
beats freezing last year's profit by 43% of mean absolute error and beats a three-year trend
by 58%. **One name does not validate a method** — this is the second full fundamental run in
the repository and everything it produces is PROVISIONAL under [R-LESSON-01] — but it is
evidence in the direction the PHDC record could not supply.

**The method UNDER-forecasts, and that is the opposite of this house's known lean.** Every
aggregate carries a negative bias: revenue −27.8 log points, profit before tax −45.7. The
fundamental walk-forward's own prior finding is that this house leans optimistic; on ARCC,
over this window, the mechanical build was systematically too LOW. The reason is macro and it
is measured in §4 below.

### The horizon profile is the real finding

| horizon | revenue bias | pbt bias | pbt MAE |
|---|---|---|---|
| 1 year | −0.025 | +0.301 | 1.016 |
| 2 years | −0.111 | −0.091 | 0.762 |
| 3 years | −0.353 | −0.043 | 1.510 |
| 4 years | −0.630 | −1.522 | 2.017 |
| 5 years | −0.602 | −1.341 | 1.793 |

**At one year the revenue forecast is essentially unbiased (−2.5 log points). By year four it
is 63 log points low — a factor of about 1.9.** The method is a one-to-two-year instrument on
this name and it degrades sharply beyond that. That is exactly the finding the ranges of §6
are built to carry into the study, and it is why years 3–5 are published as ranges.

---

## 3 · Corrections — twelve candidates, one adopted

The pre-registered bar is: the bias holds its sign in **both** eras **and** survives the block
bootstrap at **all three** block lengths {2, 3, 4}. Twelve drivers cleared it. They were then
tested under both clauses of [R-FCAL-01] §5.

| driver | bias | MAE raw → adjusted | clause 1 | clause 2 | disposition |
|---|---|---|---|---|---|
| manufacturing depreciation | −0.059 | 0.090 → 0.081 | pass | **pass** | **ADOPTED** |
| local volume | +0.193 | 0.146 → 0.130 | pass | fail | watch flag |
| provisions | −1.409 | 1.406 → 1.193 | pass | fail | watch flag |
| export volume | −0.667 | 0.767 → 0.869 | fail | fail | watch flag |
| local price | −0.297 | 0.410 → 0.497 | fail | fail | watch flag |
| export price | −0.411 | 0.477 → 0.495 | fail | fail | watch flag |
| services | −0.549 | 0.782 → 0.840 | fail | fail | watch flag |
| raw materials per tonne | −0.214 | 0.275 → 0.324 | fail | fail | watch flag |
| transport per tonne | −0.675 | 0.706 → 0.738 | fail | fail | watch flag |
| overhead per tonne | −0.147 | 0.207 → 0.210 | fail | fail | watch flag |
| transport | −0.693 | 0.866 → 0.943 | fail | fail | watch flag |
| interest income | −1.641 | 2.634 → 2.926 | fail | fail | watch flag |

**Nine of the twelve fail clause one on their own arithmetic**: the expanding-window
half-strength correction makes the out-of-sample error WORSE, not better. A bias that is large,
robust, and consistent across eras, and whose correction still degrades the forecast, is not a
calibration problem. **It is a specification problem, and this run is mostly a catalogue of
them.**

### The three that matter, and why none of them is corrected

**Local volume is driven by the wrong thing, and the score says so out loud.** The
pre-registered rule anchors local tonnage on Egyptian population growth — the exogenous
Country-ring driver [R-FCAL-01] §3 asks for. It scores **WORSE THAN FREEZE (−0.166)**: holding
last year's tonnage flat would have beaten it at every horizon. ARCC's local volume FELL from
3,944kt (FY2019) to 2,618kt (FY2024) while Egypt's population rose 9%, because the company was
reallocating clinker to export, not because domestic demand grew. The correction improves the
in-window MAE (0.146 → 0.130) and it is still refused: **a multiplier on a rule that points
the wrong way leaves a rule that points the wrong way** ([L-002]). This is the clearest
instance in either fundamental run of clause two doing its job.

**Interest income is the largest bias in the run (−1.641) and a pure specification defect.**
Held flat, it cannot track a line that went from EGP 4.9mn (FY2018) to EGP 226.3mn (FY2025) as
ARCC built a net cash position into Egyptian deposit rates of 27%. The fix is to drive it off
the cash balance at the deposit rate — which is how the rest of the book builds it — not to
multiply a flat line by a constant.

**Transport per tonne carries the largest cost bias (−0.675) and it is a MIX effect, not an
escalation error.** Transport went from 19 EGP per tonne sold (FY2018) to 157 (FY2025) as the
sales mix swung to export clinker moving to port. Escalating a per-tonne rate on total tonnage
cannot see that. The fix is to drive transport off EXPORT tonnage.

**The one adoption is the smallest correction in the set, which is what a genuine calibration
adjustment ought to look like.** Manufacturing depreciation held flat under-forecasts by 5.9%;
the sign holds in both eras; it is robust at all three block lengths; the expanding-window
correction improves it out of sample; and it matches the book, because every other study here
builds depreciation off a PP&E roll-forward and therefore grows it with the capital programme.

---

## 4 · Macro versus company

Every origin was re-run on the realised inflation, exchange-rate and coal paths.

| driver | macro share | knowable MAE | perfect-foresight MAE |
|---|---|---|---|
| export price | **+0.805** | 0.474 | 0.092 |
| G&A | +0.407 | 0.467 | 0.277 |
| local price | +0.413 | 0.426 | 0.250 |
| revenue | +0.401 | 0.483 | 0.289 |
| cost of sales | +0.367 | 0.379 | 0.240 |
| raw materials per tonne | +0.149 | 0.273 | 0.233 |
| overheads per tonne | +0.140 | 0.221 | 0.190 |
| profit before tax | +0.083 | 1.381 | 1.265 |
| **gross profit** | **−0.058** | 1.265 | 1.339 |

**Four-fifths of the export-price miss is the exchange rate itself.** Told the true EGP/USD
path, the export-price error collapses from 0.474 to 0.092. That is a statement about Egypt's
currency, not about how this company prices a tonne of clinker, and it is why no correction is
taken there.

**Gross profit's macro share is NEGATIVE, and this is the most interesting number in the
run.** Perfect foresight of the macro path makes the gross-profit forecast WORSE. The reason
is that under the knowable path the revenue leg and the cost leg are BOTH under-forecast, by
similar amounts, and the two errors substantially cancel in the difference. Handing the model
the true inflation and currency paths repairs each leg by a different amount and breaks the
cancellation. **A forecast can be right about the margin for the wrong reason, and a macro
split is what exposes it.** It is also a direct warning against the tempting repair: correcting
the price leg toward its realised path without correcting the cost leg the same way would have
manufactured a margin trend out of the correction — which is [L-009] and [L-110] in a new
costume.

**The wiring check passed.** Every driver with no CPI, FX, population or coal term in its rule
returned a macro share of exactly zero, as the pre-registration requires. A non-zero value
there would have been a wiring error in the split, and the run would have failed rather than
reported it.

---

## 5 · The sensitivity, reported and not selected

`w` is the pre-registered blend weight on the coal path in the raw-materials driver (D7),
stated at 0.5 because ARCC's own presentations record that it sources 70–80% of its coal needs
through **local pet-coke** alongside imported coal and refuse-derived fuel — so neither a pure
coal escalator nor a pure domestic-inflation escalator is right.

| w | raw materials per tonne bias | cost of sales bias | gross profit bias | pbt bias |
|---|---|---|---|---|
| 0.3 | −0.164 | −0.205 | −0.542 | −0.383 |
| **0.5 (pre-registered)** | **−0.214** | **−0.245** | **−0.312** | **−0.457** |
| 0.7 | −0.267 | −0.288 | −0.135 | −0.304 |

**w = 0.7 gives the smallest gross-profit bias and the smallest profit-before-tax bias, and it
is not adopted.** Choosing it after seeing this table is the CRPS-selection mistake in a new
costume, which the promotion rule forbids and which this project has already retired once. The
parameter stays where the disclosure put it.

---

## 6 · What the study carries forward

**Years 3–5 are published as RANGES, from this record's own error distribution** — and the
ranges are wide because the record says they are. At horizon 5 there are three resolved cells
and at horizon 4 there are four, so a percentile would be a fiction and the band is the
observed min-max with its count printed beside it.

| line | h=3 (n=5) | h=4 (n=4) | h=5 (n=3) |
|---|---|---|---|
| revenue | ×0.49 – ×2.99 | ×0.81 – ×4.02 | ×0.91 – ×3.77 |
| gross profit | ×0.13 – ×7.33 | ×0.53 – ×11.75 | ×0.60 – ×16.68 |
| profit before tax | ×0.05 – ×6.48 | ×0.37 – ×37.78 | ×0.51 – ×46.67 |
| total volume | ×0.69 – ×1.52 | ×0.90 – ×1.44 | ×0.90 – ×1.11 |

**Volume is forecastable at five years and profit is not.** The tonnage band at h=5 is ±10%;
the profit band spans two orders of magnitude. That is not a presentational choice, it is what
twenty-five cells on this company measured, and a study that published a single fifth-year
profit number would be claiming a precision this record cannot support.

**Carried into the rebuilt study:** the adopted depreciation correction; the volume, revenue
and margin ranges above; and the four specification defects named in §3, which are fixed in the
rebuild rather than corrected for — local volume driven off the company's own channel plan
rather than population, interest income off the cash balance, transport off export tonnage, and
the fuel escalator disclosed as a blend with its sensitivity.

---

## 7 · Honest limits

- **One company, twenty-five cells, eight origins.** Every lesson this run produces is
  PROVISIONAL under [R-LESSON-01] and the code refuses to write one as adopted.
- **The two eras are not one population.** E1 (origins FY2018–FY2021) and E2 (FY2022–FY2025)
  differ enough that profit after tax changes the SIGN of its bias between them (−0.581 against
  +0.006). That is reported as instability and is never corrected for: the average of two
  opposite regimes was true in neither.
- **The cells are not independent.** Overlapping horizons from eight origins share target
  years; the block bootstrap over origins is what handles it, and it is why the block lengths
  were fixed in advance.
- **The TREND benchmark fell back to FREEZE on 154 line-cells** where a line was zero or
  negative at one end of its window. That is counted and disclosed rather than absorbed,
  because a benchmark that quietly becomes FREEZE on the hard lines flatters the method it is
  meant to test.
- **The window's earliest two years sit on a different revenue basis** (gross, with a disclosed
  discount line running to 19.6% of gross — B-13). They are history for the trailing rates,
  never scored targets, and no price per tonne is computed across that break.
