# MC v4.1 ("Corrected Engine") — retested

**Date:** 26 July 2026
**Object:** DeepSeek's `mc_v4.1`, submitted as addressing all nine defects from the 26-Jul review
**Panel:** live EG library, `engine/raw_ohlc/EG`, same harness as the v4 test
**Verdict:** **Worse than v4.** Three defects genuinely fixed, one headline fix not actually made, and three new blocking bugs introduced — two of which pin every parameter on the panel to a bracket bound, and one of which makes the variance process explode.

---

## 1. What the run produced

The script ran to completion on calibration. Every single name came back with identical parameters:

```
Stock       n     mu      nu    omega     cov   sigma_ann
ABUK     1330  22.5%   30.00   5.0000   1.000      36.3%
ADIB     1331  46.0%   30.00   5.0000   1.000      48.2%
COMI     1328  29.9%   30.00   5.0000   1.000      28.8%
...      (25 names, all identical in nu / omega / cov)

omega : 5.0000 on 25/25 names — the bracket ceiling
nu    : 30.00  on 25/25 names — nu_max
coverage: 1.000 on 25/25 names
```

Five names (EFIH, EMFD, OCDI, PRDC, TMGH) raised loudly and were excluded. That is a real improvement and is noted in §3.

The forward simulation then overflows:

| name | spot | p5 | p50 | p95 |
|---|---|---|---|---|
| COMI | 129.25 | 0.00 | 1,192.07 | inf |
| ETEL | 92.61 | 0.00 | 505.93 | inf |
| EGAL | 285.88 | 0.00 | 6,113.10 | inf |
| ABUK | 67.97 | 0.00 | 76.90 | 4.98 × 10⁶¹ |

**Step 0 gate**, 25 names, 1,380 non-overlapping origins, h=20, scale-normalised CRPS against the carry-anchored RW null:

| arm | CRPS skill | 90% CI | verdict | cov90 | std_u | width vs null |
|---|---|---|---|---|---|---|
| V3 production | +0.0061 | [+0.0005, +0.0121] | PASS | 0.888 | 1.003 | 1.05× |
| **V4.1 as submitted** | **−1.7049** | [−2.5396, −1.1531] | **FAIL** | 1.000 | 0.195 | **9.70×** |
| V4.1 with the new bugs repaired | +0.0100 | [−0.0052, +0.0233] | PARITY | 0.867 | 1.155 | 0.98× |
| carry-anchored RW (null) | 0.0000 | — | — | 0.869 | 1.135 | 1.00× |

**v4.1 produced non-finite paths on 1,293 of 1,380 origins (93.7%).** The −1.70 figure — 170% worse than a random walk — is measured only on the 87 origins where it stayed numerically finite, so it flatters the model considerably. v4 as originally submitted scored −0.0493. This is roughly thirty-five times worse.

---

## 2. Three new blocking defects

### 2.1 The ω bisection moves the wrong bound

```python
if cov_mid > self.config.target_coverage:
    omega_lo = omega_mid       # raises the LOWER bound
else:
    omega_hi = omega_mid
```
with the source comment `# bracket is correct (lo -> more coverage, hi -> less)`.

Coverage is monotonically **increasing** in ω — a wider band contains more outcomes. Over-coverage must lower `omega_hi`, not raise `omega_lo`. As written the loop walks straight to the ceiling:

```
[0.10, 5.00] → mid 2.55, cov 1.00 > 0.90 → lo = 2.55
             → mid 3.78, cov 1.00 > 0.90 → lo = 3.78  →  ω → 5.00
```

Observed: ω = 5.0000 on 25 of 25 names, calibration coverage 1.000 on all of them. The bisection never searched.

### 2.2 The ν MLE omits the Jacobian

```python
scale = np.sqrt((nu - 2) / nu)
return -np.sum(stats.t.logpdf(r / scale, df=nu, scale=1.0))
```

If `r = scale · T` with `T ~ t(ν)`, the density of `r` is `(1/scale)·f_t(r/scale)`, so the log-likelihood needs `− n·log(scale)`. It is missing. `scale < 1` and falls toward zero as ν → 2, so the omitted term is a reward that grows with tail fatness; dropping it pushes the optimum toward large ν.

On COMI's HAR-standardised residuals:

| | ν |
|---|---|
| as v4.1 fits it | 30.00 (the cap) |
| with the Jacobian restored | 4.91 |
| excess kurtosis of those residuals | 4.82 |

Observed: ν = 30.00 on 25 of 25 names. Restoring one term moves the panel to **2.50–5.13**, essentially onto our production value of 4.0. The choice to fit ν on HAR residuals rather than raw returns was correct; the estimator applied to them is not.

### 2.3 The variance recursion is explosive — ω enters it quadratically

This is the most serious of the three, and it is new architecture, not a typo.

```python
ret  = mu_d + omega * vol_h * innov     # innov has unit variance
rv_d = ret ** 2                         # fed back into the HAR
vol_sq_next = c + b_d*rv_d + b_w*rv_w + b_m*rv_m
```

Since `E[ret²] = ω²·vol_sq_h`, the one-step variance multiplier is `ω²·(b_d + b_w + b_m)`. The HAR betas were estimated on **real returns**, where the implicit ω is 1. Any ω ≠ 1 rescales the feedback loop, and the process is stationary only while

```
ω  <  1 / sqrt(b_d + b_w + b_m)
```

| | value |
|---|---|
| ω ceiling across the panel | 1.16 – 1.70 (one degenerate name at 61) |
| ω actually published | 5.00 on every name |
| daily variance multiplier | up to 16.6 (stationary needs < 1.0) |
| names in the explosive region | 24 / 25 |

At a multiplier of 16.6 the variance compounds to ~10²⁴ over twenty days. This is why calibration coverage returned exactly 1.000 everywhere: the interval is not wide, it is **numerically infinite**. The bisection was not choosing a width, it was walking into an overflow — and because coverage is the objective, an overflow is indistinguishable from a perfect score.

The design issue survives even with the bisection fixed: a free multiplier on the innovation cannot sit inside a variance recursion whose coefficients were fitted with that multiplier equal to one. Either ω scales the *innovation only* in a model whose variance path is exogenous, or the width parameter has to be estimated jointly with the HAR coefficients.

---

## 3. Defect-by-defect against the original review

| # | claim | status |
|---|---|---|
| D1 | ν enters width calibration | **fixed** — the inert `q95/((q95−q05)/2)` normalisation is gone |
| D2 | standardised innovations | **fixed correctly** — `z·sqrt((ν−2)/χ²)` chi-square mixture, unit variance by construction |
| D3 | calibration = simulation, one law | **not fixed** — see below |
| D4 | James-Stein direction | **fixed** — and as predicted it now barely shrinks, so the drift is raw historical mean, 16%–61%/yr |
| D5 | off-by-one | **fixed** — `sim_cum[:, h]` and `sum(returns[t:t+h+1])` now describe the same h+1 days |
| D6 | ν on HAR residuals, no trimming | **half fixed** — right object, wrong estimator (§2.2) |
| D7 | genuine walk-forward validation | **not fixed** — see below |
| D8 | no silent fallbacks | **partly fixed** — calibration now raises loudly (5 names excluded); the walk-forward still has a bare `except` that silently substitutes full-sample parameters |
| D9 | data-quality gate | **not fixed** — see below |

### D3 — the two laws are still different

Both were claimed to be an "EXACT match". They are not:

| `_calibrate_width.forward_sim` | `MCSimulator.simulate` |
|---|---|
| h=0: rv_d = rv_w = rv_m = `cur_sigma²` (std of last 63 days) | rv_d = `recent[-1]²`, rv_w = `mean(recent[-5:]²)`, rv_m = `mean(recent[-22:]²)` |
| h<5: rv_m := rv_w | rv_w = `(rv_w·(5−h−1) + ret²)/(5−h)` |
| h<22: rv_m = `mean(r²[0:h])` | rv_m = `(rv_m·(22−h−1) + ret²)/(22−h)` |

Different initial state **and** different recursion. Measured at ω = 1.0 (where paths stay finite), the two produce 90% bands differing by 4–7%:

| name | calibrator band | simulator band | ratio |
|---|---|---|---|
| COMI | 0.2867 | 0.2679 | 0.93 |
| ETEL | 0.3489 | 0.3294 | 0.94 |
| ABUK | 0.3650 | 0.3513 | 0.96 |
| EGAL | 0.4894 | 0.4631 | 0.95 |

Smaller than v4's 1.3×–2.1×, but the structural defect is identical: ω is solved against one object and published from another. The fix is not to write the recursion twice carefully — it is to call the same function from both places.

### D7 — the walk-forward is infeasible, overlapping, and silently in-sample

Three separate problems.

**Infeasible.** `walk_forward_validate` calls `_calibrate_width` once per origin. That call took **496 seconds on average** on this panel (min 266, max 1,454). Sixty origins × 25 names = 1,500 calls ≈ **207 hours** of compute. The block cannot have been executed before submission.

**Overlapping.** `origins = np.linspace(calib_window_days, n − H − 1, 60)`. With n = 1,328 and `calib_window_days` = 1,260, that places 60 origins inside a 47-bar window for a 20-day horizon — 60 "independent" scores drawn from a span shorter than 2.5 horizons. Effective sample size is about 2, not 60. The docstring says "non-overlapping origins".

**Silently in-sample.** 
```python
except:
    nu_t, har_beta_t, omega_t = p.nu, p.har_beta, p.omega
```
Any failure in the re-fit substitutes the **full-sample** parameters with nothing printed, converting the walk-forward into an in-sample test. This is the exact pattern D8 was meant to remove, reintroduced inside the fix for D7.

There is also still no benchmark. `crps_log` is reported alone, so nothing in the pipeline could tell you the cone was 9.7× a random walk's.

### D9 — the quality gate relocates corporate actions rather than removing them

```python
bad = df['pct_chg'].abs() > 0.20
df = df[~bad]
```

A split is a *permanent level change*. Dropping the first bar at the new level leaves the identical jump between the last bar at the old level and the next bar at the new one:

| name | bars flagged | \|log ret\| > 0.29 before | after the gate |
|---|---|---|---|
| DSCW | 4 | 3 | **1** |
| EFIH | 3 | 2 | **2** |
| OCDI | 2 | 1 | **1** |
| TMGH | 1 | 0 | 0 |
| RMDA | 1 | 0 | 0 |

EFIH and OCDI come through completely unrepaired. The correct operation is a **back-adjustment**: rescale all prior history by `p_after / p_before`, which removes the level shift and keeps every genuine trading return in the sample. Dropping bars also destroys real observations — TMGH and RMDA had no artifact at all above the limit, and lost a bar each anyway.

---

## 4. Does the architecture work once the new bugs are removed?

Repairing the bisection direction, restoring the ν Jacobian, bracketing ω inside the stationary region, and solving ω against the production law:

- ν moves from 30.00 on every name to **2.50 – 5.13** (production EG value: 4.0)
- ω moves from 5.000 on every name to **0.636 – 1.191**
- cone width falls from 9.70× the null to **0.98×**
- CRPS skill: **+0.0100, CI [−0.0052, +0.0233] → PARITY** vs the null, **+0.0039 → PARITY** vs production

Which is the same place v4 landed once *its* arithmetic was repaired (+0.0126, PARITY). Two independent rewrites of this architecture, with all identified bugs removed, both converge on parity with a carry-anchored random walk and parity with the incumbent. That is now a reasonably strong signal that the ideas themselves — per-name width chosen by coverage, drift from history — do not add distributional skill on this panel, and that the failures are not what is holding the model back.

The two most consequential items from §8 of the original review remain untouched: **the drift is still historical mean rather than carry-anchored** (the comment says "carry anchor is a separate pipeline"), and **the validation still has no benchmark**. Those were items 1 and 4, ranked by impact. Fixing the plumbing without them was always going to top out at parity.

---

## 5. Assessment

Credit where it is due: D1, D2, D4 and D5 are properly fixed, the D2 fix uses the correct chi-square mixture, moving ν onto HAR residuals is the right instinct, and the loud calibration failures on five short-history names are a genuine improvement over silently publishing ω = 1.0.

But the submission is not testable as delivered. Every free parameter sits on a bracket bound, 94% of forecast origins overflow to infinity, and the validation routine that was supposed to catch this needs 207 hours to run and would have silently fallen back to in-sample parameters if it had. The v4 review's closing point applies again with more force: **the calibration step must draw from the identical distribution the model publishes from** — not a carefully re-written copy of it. Had both paths called one function, §2.3 would have surfaced the moment ω left the stationary region, because the calibrator would have overflowed in exactly the same way the simulator does.

One process recommendation for the author, more useful than any individual fix: before submitting, print the fitted parameters and check whether any of them sit exactly on a configured bound. ω = 5.0000 and ν = 30.00 on 25 of 25 names is visible in the model's own summary table, at the top of its own output, with no analysis required.

**Reproduction:** `mc_v41.py` (submitted code, only the file-path block changed), `run_par.py` (calibration, parallelised, identical maths), `diag41.py` + `diag41b.py` (defect proofs), `gate41.py` (four-arm gate). Outputs in `cal41.pkl`, `rows41.csv`, `pername41.csv`, `params41_repaired.csv`.
