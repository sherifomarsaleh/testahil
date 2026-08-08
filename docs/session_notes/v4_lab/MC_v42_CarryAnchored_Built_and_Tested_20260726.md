# MC v4.2 — built to spec, run, and scored

**Date:** 26 July 2026
**Spec:** `mc_v42_spec.md` (DeepSeek, presented as from Sherif / Testahil)
**Panel:** full EG library, 30 names, 1,603 non-overlapping walk-forward origins, h=20
**Verdict:** **As specified: FAIL** (−0.0192, CI [−0.0283, −0.0106]). **With its two defects corrected: PARITY vs the null and FAIL vs production.** The spec's own §9 exit condition has now been reached three times over.

---

## 1. The spec's self-check does not pass

§8 says to run it first. Two of the four checks fail, and one fails for a reason that matters.

### Check 1 — FAIL. The Jacobian is applied with the wrong sign.

```python
jacobian = len(r_std) * np.log(scale)
return -np.sum(stats.t.logpdf(r_std / scale, df=nu, scale=1.0)) - jacobian
```

For `r = s·T` with `T ~ t(ν)`, the density of `r` is `(1/s)·f_t(r/s)`, so

```
logL  = Σ log f_t(r/s) − n·log(s)
negLL = −Σ log f_t(r/s) + n·log(s)          ← PLUS
```

The spec subtracts it. Recovery of a known ν on synthetic data, 40 replications, n=3,000:

| true ν | v4.1 (no Jacobian) | spec's signed Jacobian | correct sign |
|---|---|---|---|
| 3 | 29.00 | 29.90 | **3.06** |
| 4 | 29.90 | 29.90 | **3.91** |
| 6 | 29.90 | 29.90 | **5.90** |
| 10 | 29.90 | 29.90 | **10.08** |

The spec's version is indistinguishable from the v4.1 bug it was written to fix — it pins ν at the grid cap on every draw. The check itself fired correctly (`correct_best = 20.0`, assertion `< 8` failed), which is to the author's credit; it just was not run before sending.

### Check 3 — FAIL at ν=3. The tolerance is unsatisfiable.

`Var[t_ν] = 1` exactly, but the **sample** variance needs a finite fourth moment, i.e. ν > 4. At ν=3 the kurtosis is infinite, so the estimator has no finite sampling variance and cannot be held to ±0.005:

| ν | sample var across 12 seeds (500k draws each) | within ±0.005 |
|---|---|---|
| 3 | 0.9616 – 1.0406 | 1/12 |
| 4 | 0.9903 – 1.0190 | 6/12 |
| 6 | 0.9908 – 1.0038 | 11/12 |
| 10 | 0.9957 – 1.0042 | 12/12 |

Not a code defect — an impossible assertion. Tolerance replaced with a band that scales with ν.

Checks 2 and 4 pass.

---

## 2. Disclosed deviations from the spec

Per the spec's instruction to stop and report rather than proceed silently:

| | deviation | why |
|---|---|---|
| X1 | ν Jacobian sign corrected | otherwise ν pins at 30 and nothing runs |
| X2 | Check-3 tolerance widened | otherwise the self-check can never pass |
| X3 | James-Stein computed **both ways** | §2.2 mixes units — see §3 |
| X4 | carry run on the **real CBE schedule** as well as the flat 25% | see §4 |
| X5 | q = 0 retained as instructed, **flagged** | EGX names pay real dividends; a price-series carry of rf − 0 overstates drift by the yield |
| X6 | corporate actions **back-adjusted**, not dropped | v4.1's drop-the-bar gate leaves the jump in the return series |
| X7 | ω refit every 5 origins, not every origin | strictly walk-forward either way; per-origin refitting is what made v4.1's validation need 207 hours |

Everything else is as written. One `forward_paths()` function is called by the calibrator, the simulator and the validator, so §3's "call one function from both places" is satisfied literally.

---

## 3. Change 1 does not happen: the carry anchor is cosmetic as specified

The James-Stein factor in §2.2:

```python
avg_var    = np.mean([np.var(excess_rets_i) / len(excess_rets_i) for ...])   # DAILY
dispersion = np.sum(np.array(all_alphas) ** 2)                               # ANNUALISED
c = (k - 3) * avg_var / dispersion
```

`avg_var` is the variance of a **daily** mean; `dispersion` is a sum of squared **annualised** alphas. The two differ by 252² = 63,504, so `c` comes out ~10⁻⁵ and `keep` clips to its 0.95 ceiling on essentially every date.

Measured on the panel, across 431 origin dates:

| | keep factor |
|---|---|
| spec formula as written | **0.950 – 1.000** |
| units made consistent | 0.000 – 1.000 (median 0) |

So under the spec, μ = carry + 0.95·(historical mean − carry) ≈ historical mean:

| | min | median | max | origins with \|μ − carry\| > 10pp |
|---|---|---|---|---|
| carry anchor itself | +8.2% | +19.5% | +27.3% | — |
| μ, spec (flat 25% + spec JS) | −69.8% | +24.3% | +98.2% | **59.7%** |
| μ, corrected units | −69.8% | +21.0% | +98.2% | 8.0% |

**correlation(μ_spec, raw historical drift) = 0.9998.**

The entire purpose of v4.2 was to stop using historical mean drift. As specified, it uses historical mean drift with two extra steps. The spec's own success criterion 5 — "most stocks |α| < 5%" — is met on 21% of origins under its own formula and 90% once the units agree. That criterion was the right self-test and it catches this.

---

## 4. The risk-free rate is asserted, and wrong

§7 says `rf = 0.25` and calls it the CBE overnight deposit rate, with no source.

The CBE overnight deposit rate is **19.00%**, held at the 9 July 2026 meeting — the third consecutive hold, after 825bp of cuts from April 2025 to February 2026. Our production anchor is the 19.50% main operation rate (corridor 19.00/20.00).

Worse for a five-year backtest: the rate was **8.25%** through 2021, rose in steps to **27.25%** in March 2024, and has fallen since. A flat 25% is wrong by roughly 17 percentage points at the start of the sample. Running both:

| null | log-CRPS skill vs the scheduled-carry null |
|---|---|
| carry-anchored RW on the real CBE schedule | 0.0000 (reference) |
| carry-anchored RW at the spec's flat 25% | +0.0023, CI [−0.0046, +0.0086] — PARITY |

The anchor level is close to gate-neutral because both engine and benchmark carry it, which is by design. It is not neutral for the model's own centring, and a number this consequential should be sourced, not asserted.

---

## 5. A real finding: price-scale CRPS is not a valid estimator for this model

The first scoring run returned a pooled skill of **−29.45**. That number is an artifact and should not be quoted.

A single origin — OCDI, 18 May 2025 — accounted for **96.7% of the entire panel's CRPS total**:

| | value |
|---|---|
| ν at that origin | 2.62 |
| 90% band / spot | 0.275 (the null's was 0.399 — **narrower**) |
| largest simulated terminal price / spot | 2.35 × 10¹¹ |
| CRPS on price / spot | 3,677.8 |
| CRPS on log-price | 0.0921 |

The quantiles are sane. What diverges is the mean. If the terminal log-return has Student-t tails, the terminal **price** has no finite expectation — `E[exp(X)] = ∞` for any polynomial-tailed `X` — so sample CRPS on the price scale is not a consistent estimator and grows with path count. At ν ≈ 2.6, plus a squared-return feedback into the variance that lets a path compound into a high-vol regime, a handful of paths reach 10¹¹ × spot and one origin swamps 1,602 others.

This is worth flagging in our own direction too: our production engine simulates log-t returns and scores CRPS on prices, so it is exposed to the same thing in principle. It escapes in practice because ν = 4 is fixed, σ_h is small, and there is no variance feedback that can compound a path into a fat-tailed regime. We should still consider moving the standing gate to log-space or to a bounded score.

Credit where due: the spec's §4.1 asks for "CRPS(terminal log-price)", which is the correct choice and is finite. Everything below uses it.

---

## 6. Results

Walk-forward (all parameters fitted on data strictly before each origin), non-overlapping origins every 20 bars from index 300, 30 names, 1,603 origins, log-price CRPS, block bootstrap over half-year calendar blocks resampled jointly across names.

| arm | skill | 90% CI | verdict | cov90 | Winkler skill | width vs null |
|---|---|---|---|---|---|---|
| V3 production | **+0.0075** | [+0.0008, +0.0152] | **PASS** | 0.892 | +0.0243 | 1.05× |
| V4.2 corrected (real carry, units-fixed JS) | −0.0060 | [−0.0119, +0.0001] | PARITY | 0.867 | −0.0410 | 1.03× |
| **V4.2 as specified** (flat 25%, spec JS) | **−0.0192** | [−0.0283, −0.0106] | **FAIL** | 0.859 | −0.0511 | 1.03× |
| V4.2 with α forced to 0 | −0.0042 | [−0.0097, +0.0017] | PARITY | 0.868 | −0.0364 | 1.03× |
| carry-anchored RW (the null) | 0.0000 | — | — | 0.871 | 0.0000 | 1.00× |

Head-to-head against production:

| arm | skill vs V3 | 90% CI | verdict |
|---|---|---|---|
| V4.2 corrected | −0.0136 | [−0.0207, −0.0069] | **FAIL** |
| V4.2 as specified | −0.0270 | [−0.0358, −0.0181] | **FAIL** |

Names losing to the null: **V4.2 corrected 17/30, V4.2 as specified 26/30, production 8/30.**

Note the Winkler column. The interval score depends only on the 5th and 95th percentiles, so it is immune to the tail-mean problem in §5 — and every v4.2 arm is negative on it too. The result is not an estimator artifact.

### Fitted parameters, walk-forward

| | range | median |
|---|---|---|
| ν | 2.50 – 12.40 | 3.77 |
| ω | 0.514 – 1.646 | 1.038 |
| carry | 8.25% – 27.25% | 19.5% |

Nothing pinned: 0.0% of origins at the ν cap, 0.0% at the ω stationarity ceiling. The v4.1 pathologies are gone.

### The spec's own success criteria (§9)

| # | criterion | result |
|---|---|---|
| 1 | skill CI excludes zero | **NOT MET** (as specified: excludes zero on the wrong side) |
| 2 | coverage in [0.85, 0.93] for ≥80% of names | **NOT MET** — 57% |
| 3 | ω in [0.5, 1.5] | MET — 100% |
| 4 | ν in [2.5, 8.0] | MET — 100% |
| 5 | most stocks \|α\| < 5% | **NOT MET** under the spec formula (21%); MET once units agree (90%) |

### Deliverable 4 is not a valid identity check

§6.4 asks to verify that "with α=0 forced, CRPS skill ≈ 0 (model collapses to null)". It does not, and cannot: zeroing α equalises only the **drift**. The HAR width, the Student-t shape and ω all remain, so the model stays a fat-tailed stochastic-volatility process and the null stays a Gaussian trailing-vol random walk. Measured: skill −0.0042 with a band ratio of 1.03× and cov90 0.868 vs the null's 0.871. Useful as a drift ablation — and the ablation says α contributes essentially nothing, since the full model scores −0.0060 against −0.0042 with α removed.

---

## 7. Conclusion — the spec's own exit condition

§9 closes: *"If skill is still PARITY after implementing carry-anchored drift, the conclusion is that distributional modeling (HAR, Student-t, per-stock width) does not add measurable value on this panel beyond a well-anchored random walk. That finding is useful — report it clearly."*

That condition is now met, and it has been met three times with three different architectures:

| | skill vs the carry-anchored null |
|---|---|
| v4, repaired | +0.0126 → PARITY |
| v4.1, repaired | +0.0100 → PARITY |
| v4.2, corrected | −0.0060 → PARITY |
| production v3 | +0.0075 → PASS, and beats all three |

So: reported clearly. **On this panel, per-name distributional machinery does not beat a carry-anchored lognormal random walk with trailing volatility.** The null is a strong baseline — production clears it by +0.0075 with a confidence interval that only just excludes zero, which is roughly what real distributional skill looks like in an emerging market with three years of currency regime change in the sample.

That is not a negative result about v4.2 specifically. It is the answer to the question the whole three-round exercise was asking, and it is worth more than another iteration would have been.

Two things would change the conclusion rather than re-litigate it. Move to h=60, where our standing gate sits and where volatility structure has more room to matter than it does over four weeks. And source per-name dividend yields, since q = 0 on a price series is a systematic drift error in the same direction for every name, and it is the one input in this whole exercise that is cheap to fix and has never been tested.

---

**Deliverables:** `mc_v42.py`, `mc_v42_console.txt` (full run output), `mc_v42_results.csv` (per stock: skill, coverage, ω, ν, α), `selfcheck_spec.py` (the spec's §8 check, instrumented to report rather than abort). Per-origin scores in `rows42b.csv`.

---

## 8. Addendum — the h=60 test (26 Jul 2026)

§7 named h=60 as one of two things that could change the conclusion rather than re-litigate it. It was run: same panel, same walk-forward design, non-overlapping 60-day origins, 531 origins across 30 names, ω and ν re-solved at the longer horizon.

**The horizon was not hiding the signal. It makes v4.2 worse.**

| arm | h=20 | h=60 |
|---|---|---|
| V3 production | +0.0075, PASS | +0.0052, PARITY |
| **V4.2 corrected** | −0.0060, PARITY | **−0.0203, FAIL** [−0.0378, −0.0035] |
| V4.2 as specified | −0.0192, FAIL | −0.0593, FAIL [−0.0884, −0.0304] |
| V4.2, α forced to 0 | −0.0042, PARITY | −0.0132, PARITY |

Head-to-head at h=60, V4.2 corrected vs production: **−0.0257, CI [−0.0380, −0.0140], FAIL.** Names losing to the null: 21/30 for v4.2, 14/30 for production. Winkler skill −0.0564, so the interval score agrees.

Coverage tells the same story from the other side: v4.2's cov90 falls from 0.867 at h=20 to **0.829** at h=60 against a 0.90 target. The per-name ω is solved to hit 90% in calibration and does not hold it forward — the width parameter does not generalise across the horizon it was fitted on.

**Caveat, stated plainly:** production only reaches PARITY here, not PASS, because 531 non-overlapping origins is a third of the h=20 sample and the CI widens accordingly (+0.0052, CI [−0.0041, +0.0153]). This harness is not the standing production gate, which uses the full library and a different minimum-history rule. The comparison between arms is sound — all arms see identical origins — but the absolute verdict on production at h=60 should be read off the standing gate, not off this run.

### The CRPS divergence gets much worse with horizon

The §5 finding scales badly:

| | worst single origin as a share of the panel CRPS total | largest simulated path / spot |
|---|---|---|
| v4.2, h=20 | 96.7% | 2.35 × 10¹¹ |
| v4.2, h=60 | **99.8%** | **2.76 × 10¹⁶** |
| production v3, h=20 | 1.3% | — |
| production v3, h=60 | 3.8% | — |

Sixty days of compounding a fat-tailed variance-feedback process puts a single origin at 99.8% of the entire panel score. Production degrades too — 1.3% to 3.8% — which is small but is the same mechanism, and is the argument for moving our standing gate to log-space or a bounded score before the next refit.

### What this closes

Both of §7's open questions are now answered in one direction: the longer horizon does not help. That leaves sourced per-name dividend yields as the only untested input, and it is a drift correction, not a distributional one — so it can move centring and PIT, but it cannot plausibly turn a −0.02 into a pass. **The v4 line is closed.**
