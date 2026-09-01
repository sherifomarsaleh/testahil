# AMOC — fundamental walk-forward training record

**1 September 2026 · Alexandria Mineral Oils Company S.A.E · EGX · class: petrochemical
(refining, specialty base oils and paraffin wax) · scope LIGHT · 9 scoreable cells**

**Internal.** The panel, the error cells, the pre-registration and this record are never
shown to a reader. Nothing here reaches the live site.

**Which walk-forward:** the FUNDAMENTAL one — drivers projected from a past origin and
scored against what the company reported. Not the price-engine walk-forward (band coverage
on the Monte Carlo cone) and not the technical walk-forward.

Companion files: `PRE_REGISTRATION_01-09-2026.md` (written first, unamended),
`BASIS_BREAKS_01-09-2026.md`, `panel.py` (the panel, with its footings as assertions),
`scores.json`, `diagnostics.json`, `corrections_log.json`, `forward_ranges.json`,
`amoc_IS_projected_vs_actual_all_origins.md`.

---

## 1 · The headline, stated plainly

**The method does not beat "no change" on this company, at any horizon, and the margin is
not close.**

| | bias | MAE | over-forecast | skill vs freeze |
|---|---:|---:|---:|---:|
| Majority profit | **−64.1%** | 178.4% | **0 of 9 cells** | **−1.128** |
| Profit before tax | −65.7% | 191.9% | 0 of 9 | −1.021 |
| Net sales | −43.5% | 76.8% | 0 of 9 | n/a (rule = benchmark) |
| Gross profit | −39.0% | 65.6% | 1 of 9 | −0.499 |

A skill of −1.128 means the pre-registered model's average miss on majority profit is
**more than twice** the miss you get by writing down last year's profit and stopping.
Under [R-FCAL-01] that is not a figure of speech and this record says so: **a method that
cannot beat "no change" has not earned the precision it displays.**

The bias worsens with horizon — −51.3% at one year, −71.9% at two, −71.7% at three — and it
is one-sided at every one of them.

## 2 · Why, and it is a specification error rather than a calibration one

The dominant defect is in the **macro scenario**, not in the drivers.

The pre-registration defined the knowable path as "the last published annual value at the
origin, held flat forward". For inflation the published value is a **rate**, so holding it
flat compounds the price level. For the exchange rate and for crude the published value is a
**level**, so holding it flat means no change at all. The result is a scenario in which
Egyptian domestic costs compound at 20–30% a year while the currency never moves.

**That is not a coherent state of the world**, and on this company it is fatal. AMOC buys
fuel oil and wax distillate from EGPC and sells refined products drawn from the same barrel
in the same months; raw materials are **90.7% of cost of sales**. Freezing revenue in
nominal EGP while inflating salaries, utilities, overheads and marketing guarantees a
one-sided profit miss — which is exactly the record above.

**The same rules on a coherent path** (crude flat in USD, the currency depreciating at the
inflation rate already assumed for domestic costs — `diagnose.ppp_project`):

| majority profit | bias | MAE | over-forecast | skill vs freeze |
|---|---:|---:|---:|---:|
| pre-registered (currency frozen) | −64.1% | 178.4% | 0 of 9 | −1.128 |
| PPP-consistent (diagnostic) | −25.0% | 58.2% | 4 of 9 | **+0.047** |
| perfect foresight of crude-in-EGP | +66.7% | 72.3% | 8 of 9 | −0.131 |

**The PPP run is a DIAGNOSTIC and it is not evidence.** It was specified after the
pre-registered record existed, and under L-042 the identical change that would have been a
choice beforehand is tuning afterwards. The pre-registered rule stands, its result stands,
and no correction factor is allowed to hide the defect. What the diagnostic establishes is
*where* the error lives, which is what a diagnostic is for.

## 3 · The finding that survives fixing the macro path

**Perfect foresight of crude-in-EGP does not rescue the method**, and the reason is the more
interesting half of this run.

Given the realised crude-in-EGP path, the driver structure is **very accurate**:

- net sales: bias **+6.0%**, MAE 6.4%
- cost of sales: bias **+0.1%**, MAE **1.6%**

and yet, on the same cells:

- gross profit: bias **+68.0%**
- majority profit: bias **+66.7%**, skill vs freeze **−0.131**

**AMOC's gross margin is a ~6.6% residual between two numbers each above EGP 35 billion.**
An error of 6% on revenue against 0.1% on cost does not stay 6% — almost the whole of it
lands in the residual. The arithmetic: at a 6.6% margin, `ΔGP/GP ≈ 0.06/0.066 ≈ 90%`, and
the measured +68% is that mechanism with the cost error working slightly the other way.

The β sensitivity is the same fact seen from another angle. Moving the crude pass-through
exponent across its pre-registered range on the foresight path:

| β | net sales bias | cost of sales bias | gross profit bias | majority bias |
|---:|---:|---:|---:|---:|
| 0.8 | −6.5% | −10.7% | +38.7% | +30.8% |
| 1.0 | +6.0% | +0.1% | +68.0% | +66.7% |
| 1.2 | +20.2% | +12.5% | +100.8% | +107.0% |

**A 27-point swing in the revenue assumption becomes a 76-point swing in profit.** On a
thin-margin pass-through business the two sides must be right *relative to each other*, and
being individually excellent is not the same thing and is not sufficient.

Note also that β is **vacuous under the pre-registered path**: with the crude ratio held at
1.0 it multiplies nothing, and all three values are identical. Reporting three identical
numbers as a sensitivity would have been theatre; it is reported where it bites and the
reason is stated.

## 4 · Per driver

Log bias and MAE translated to percentages; macro share is `1 − MAE(foresight)/MAE(knowable)`.

| driver | n | bias | MAE | over | macro share | skill vs freeze | skill vs trend |
|---|---:|---:|---:|---:|---:|---:|---:|
| throughput, tonnes | 9 | +7.6% | 8.5% | 89% | 0% | n/a rule = benchmark | +0.214 |
| net sales | 9 | −43.5% | 76.8% | 0% | 89% | n/a rule = benchmark | +0.114 |
| raw materials | 9 | −46.6% | 87.3% | 0% | 98% | +0.000 | −0.019 |
| salaries | 9 | −11.0% | 18.6% | 33% | 60% | +0.454 | −0.904 |
| other cost of sales | 9 | −17.1% | 20.8% | 11% | 74% | +0.507 | +0.360 |
| cost of sales | 9 | −43.9% | 78.3% | 0% | 97% | +0.033 | −0.131 |
| gross profit | 9 | −39.0% | 65.6% | 11% | **−3%** | −0.499 | +0.782 |
| general and administrative | 9 | −22.9% | 30.2% | 11% | 53% | +0.421 | +0.244 |
| marketing and selling | 9 | −52.6% | 113.0% | 11% | 21% | +0.198 | +0.006 |
| other revenues | 9 | −87.2% | 682.0% | 0% | 8% | −0.401 | −1.163 |
| — of which credit interest | 9 | −66.3% | 202.8% | 11% | 17% | +0.136 | −0.309 |
| profit before tax | 9 | −65.7% | 191.9% | 0% | 53% | −1.021 | +0.448 |
| majority profit | 9 | −64.1% | 178.4% | 0% | 47% | −1.128 | +0.296 |

Four things in that table are worth naming.

**Throughput is the only line that is over-forecast** (+7.6%, 8 of 9 cells). AMOC's sales
tonnage fell in four of the five years — 1,548kt (FY2022) → 1,449 → 1,433 → 1,262 (FY2025) —
and a flat-volume rule cannot see a declining plant. It is a small error and it points the
opposite way to everything else.

**The revenue error is almost entirely realisation, not volume or mix.** Decomposed over the
nine cells: realisation +88.3%, volume −7.0%, mix +1.0%. The eight-line product build adds
essentially nothing over a single-line build on this name, because every line moves with the
same barrel.

**Gross profit's macro share is −3%.** Perfect foresight of the macro path improves revenue
and cost enormously and leaves gross profit slightly *worse*. The residual is a
company-side quantity and the macro conditioning has nothing to say about it — which is §3's
finding arriving through a second route.

**The macro split's own check passed.** The seven drivers carrying no CPI and no crude term
returned a macro share of exactly zero, as they must by construction. A non-zero value there
would have been a wiring error rather than a finding, and the run asserts on it.

## 5 · Corrections — none, and the ruling was made in advance

The pre-registration ruled, before any number existed, that **no correction would be
estimated from this record**: nine cells cannot support an expanding-window estimate and a
separate confirmation sample. Every bias is a **watch flag** — recorded, graded at the next
update, acted on by nobody.

That ruling is vindicated by what clause 1 does here: **sixteen of twenty-one drivers
"pass" it**. That is not sixteen warranted corrections, it is a degenerate test. With one
origin in the pre-devaluation era, the sign-stability check has nothing to compare, and with
every driver dragged the same way by one specification defect the bootstrap agrees with
itself for a reason that has nothing to do with the driver. **A test that almost everything
passes is not evidence, and a pass rate of 76% is the signal that the test is not
discriminating** — the same lesson this project learned when it retired a gate that had
never rejected anything.

Clause 2 would have blocked the large ones independently: the book builds feedstock as cost
per unit escalated on the commodity's own price path in every study that has a physical
input, and no study in the book carries a multiplier on an aggregate. And the governing
rule overrides both clauses here anyway — **a correction factor is honest when the model is
right and reality is awkward; when the model is wrong, a correction hides it.** This
record's dominant error is a specification defect, so a multiplier fitted on top of it would
be fitting the defect.

## 6 · The borrowing-rate driver is refused, not widened

AMOC's interest-bearing borrowings were **EGP 20,977,437** at 31 December 2025 against total
equity of **EGP 4,824,774,948**; the company holds net cash of about EGP 2.44bn. A borrowing
rate formed on a denominator that small is noise, and the tempting repair — divide the
finance charge by a broader liabilities total until the answer looks sensible — is precisely
how a spurious bias is manufactured.

**The rate was declared undefined in the pre-registration, before any number was computed,
and the charge was held flat.** This is an independent second observation of L-041, on a
different company in a different industry from the one that produced it.

## 7 · What this licenses the study to say about years 3–5

Multiplicative bands, from this record's own error distribution. **Counts are printed beside
every figure and no percentile is computed**: the horizons hold 4, 3 and 2 observations, and
a p10/p90 on two numbers is a pair of numbers wearing the costume of a distribution.

| horizon | net sales | gross profit | majority profit |
|---|---|---|---|
| 1 year (n=4) | ×0.52 – ×1.08 | ×0.47 – ×1.36 | ×0.24 – ×1.17 |
| 2 years (n=3) | ×0.28 – ×1.00 | ×0.33 – ×1.42 | ×0.08 – ×1.18 |
| 3 years (n=2) | ×0.15 – ×1.00 | ×0.27 – ×1.36 | ×0.08 – ×1.23 |

These are the wider of the pre-registered band and the PPP diagnostic band, per line per
horizon. The diagnostic may widen a published range and may never narrow one.

**A fifteen-fold band on year-3 profit is not a useful forecast and the study must not
pretend otherwise.** What it is, is an honest measurement of how little this method knows
about a thin-margin refiner's profit three years out when it cannot forecast a currency.
The study carries it into the fair-value range rather than burying it, and says in §7 that
the far years support a range and never a point.

## 8 · Caveats, stated rather than implied

- **Nine cells.** Everything above rests on five origins and three horizons. No finding here
  is validated; all of it is provisional under [R-LESSON-01].
- **The window stops at FY2021 because AMOC publishes nothing older.** The exchange, the
  regulator's disclosure portal and the Wayback Machine are all refused at this session's
  egress proxy; the only vendor reachable carries the same five years, restated.
- **The era split is degenerate.** One origin sits in the pre-devaluation era. The
  sign-stability results in §5 should be read as untested, not as passed.
- **FY2023 carries a qualified audit opinion** (B-8). It touches balance-sheet items, not
  the lines scored here, but it is on the record.
- **FY2024 is used as first reported**, and the restatement that followed is 15.3% of
  majority profit (B-6). Had the run used the restated figure, every FY2024-target error
  would move by that amount — which is the whole reason point-in-time discipline is a rule.
- **No per-product cost driver exists in this run**, because the company itself had no
  per-product costing system before July 2023 (B-7). Any per-line margin in the published
  study is a construction, and the study now says so.
