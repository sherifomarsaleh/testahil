# Equation Lab — Round 7: Dated Egypt ERP Schedule + Signed Individual Trend (23-Jul-2026)

**Trigger:** two direct corrections from Sherif, both acted on in full, not partially:
1. *"I never asked for the return to be higher for all stocks across the board... treat each one individually"* — beta (Round 6) only scales the **magnitude** of one common positive premium; it never flips **sign**. Round 7 builds and tests a candidate whose sign is genuinely per-name, using a statistic beta cannot provide.
2. *"'...slower but bulletproof.' Go for the slower bullet proof of course."* — build a **dated** Egypt ERP/rf* schedule instead of Round 6's static Jul-2026 snapshot, before any FINAL-window shot is considered.

**Headline result: the dated rebuild changed the verdict on Round 6 itself.** Once the ERP is allowed to vary with the actual macro regime at each historical origin (instead of using today's elevated premium retroactively), roughly 80% of Round 6's apparent gain evaporates — it was substantially a look-ahead artifact. The new signed-trend candidate (continuation) fails cleanly, and a diagnostic explains *why* in a way that connects directly to the production engine's own already-validated signal character. A reversal-flavored variant shows a small bump that does not clear this lab's own bar for "real, not noise." Full numbers below; nothing here is being oversold.

Lab-only throughout: `engine/mc_v3.py`, `market_profiles.py`, `fitted_configs.json` untouched, imported read-only. Scripts: `claude/v4_lab/lab_round7_signedtrend.py`, `lab_round7b_reversal.py`, `lab_round7c_dated_capm.py`.

---

## Part A — dated Egypt ERP/rf* schedule (closes the "slower bulletproof" ask)

Damodaran's raw source files (`ctryprem*.xls/.xlsx`, archived back to 2001) are **binary and unparseable by this session's web tools**; the Wayback Machine is proxy-blocked; his own blog write-ups narrate methodology but never embed the per-country table; several third-party mirrors are paywalled or JS-gated. After an extensive search (report in full below, not glossed over), four independently-sourced, dated anchors were recovered and cross-checked:

| Date | Rating | Default spread | Total ERP | Source |
|---|---|---|---|---|
| 2013-01-01 | B2 | 5.00% | 13.30% | studylib.net mirror of Damodaran's ctryprem table ("last updated Jan 2013") |
| 2022-01-01 | — | — | 9.68% | gurufocus.com "Egypt Total Equity Risk Premium", sourced "Damodaran Online" |
| 2023-01-01 | — | — | 15.43% | gurufocus.com, same series |
| 2026-01-01 | Caa1 | 6.37% | 13.94% | tools.theinvestlog.com "Egypt as of 2026-01-01" — **matches Cost_of_Capital_Reference.md's already-vetted rating-basis figure exactly**, cross-validating both sources |

Held flat between knowns (step function) — identical convention to `EGYPT.carry_schedule`'s own `carry_rate()` lookup, not a new mechanism. **Checked directly rather than assumed:** the actual EG panel history is not 2016–2026 — 21 of 30 raw_ohlc names start exactly 2021-01-03; only CLHO (2016) and DSCW (2012) go deeper. So the real MIN_HISTORY=260 backtest population lives almost entirely in 2021–2026, which this schedule covers well (three of the four anchors sit inside that exact window, including both sides of the 2022→2023 devaluation spike). The sparse 2013→2022 flat segment only touches the earliest origins of the two long-history names — flagged, not hidden, and it does not miss any break inside the actual backtest data (the profile's 2016-11-03 break predates the panel).

## Part A payoff — Round 6 rerun, dated vs static

Same CAPM construction as Round 6 (`Ke_i = rf*_i + beta_i × ERP`, real-EGX30-index beta, walk-forward, `drift = carry + s×(Ke−carry)`), only the rf*/ERP source changes:

| variant | s=0.00 | s=0.25 | s=0.50 | s=0.75 | s=1.00 |
|---|---|---|---|---|---|
| **static snapshot** (Round 6 replica) | +0.0314 | +0.0341 | +0.0365 | +0.0384 | **+0.0399** |
| **dated schedule** (Round 7) | +0.0314 | +0.0319 | +0.0319 | +0.0316 | **+0.0309** |

cov90 stays in the [0.88, 0.92] band throughout both rows (0.890→0.895). The static row is monotonic and clean, exactly reproducing Round 6. **The dated row is flat-to-slightly-negative** — the entire s=0→1 range moves inside a ±0.001 band around baseline, well short of a real effect. Decomposition on the dated schedule (mirrors Round 6's own check): real per-name beta +0.0309 vs flat beta=1.0 +0.0327 — real beta is, if anything, *worse* than no differentiation at all, the same conclusion Round 6 reached, now a third time.

**Mechanism:** the static snapshot applied *today's* elevated ERP (13.94%, a level set by the 2023 devaluation shock and its partial 2024-26 unwind) uniformly to every window back to 2021 — including 2022 windows where the contemporaneous premium was actually much lower (9.68%). Since EGX nominal prices were also broadly rising over 2021-26, retroactively assigning 2026's high premium to 2022 windows manufactured an apparent edge that a real-time forecaster in 2022 could never have had. This is precisely the failure mode Round 6's own caveat flagged as a risk ("a mildly favorable snapshot could be inflating the win") and precisely why Sherif's "slower but bulletproof" instinct was right — the rebuild caught a real look-ahead contamination, not a hypothetical one. **Round 6's "the market anchor was too low" finding is downgraded from "real" to "not distinguishable from noise once properly dated."**

## Part B — signed individual trend drift (the new candidate)

Distinct in construction from all prior drift families (Rounds 3-6): not an expanding window (Round 5), not shrunk toward a noisy cross-sectional grand mean (Round 5), not cross-sectionally demeaned/zero-net (Round 4b), not a trailing-realized-ERP substitute (Round 4a), not a co-movement/beta statistic (Round 6). It is the actual chart trend a person would read — a bounded lookback (126d/6mo or 252d/12mo trailing log return) — combined with a **James-Stein-style statistical usability gate**, the same *philosophy* already trusted in this codebase for beta (`wacc_builder.py`'s n≥24/R²≥5%/SE<|β| → "not distinguishable from noise" fallback), applied here to trend instead:

```
t_i          = trailing daily mean return / its own standard error   (walk-forward safe)
w_i          = t_i^2 / (t_i^2 + k)              # -> 0 for noisy/flat names, -> 1 for strong trends
tilt_i       = w_i * trailing_daily_mean_i * horizon
drift_i(s)   = carry_b + s * tilt_i
```

A flat/choppy name gets `w≈0` (drift stays at carry) automatically — no hand-tuned rule needed to produce that behavior, it falls out of the statistics. A strongly, persistently trending name gets `w→1`.

### B1 — trend-continuation sweep (DEV, 447 windows)

| window | k | s=0.00 | s=0.50 | s=1.00 |
|---|---|---|---|---|
| 126d | 1 | +0.0314 | −0.0564 | **−0.2627** (cov90 0.848, OUT-OF-RANGE) |
| 126d | 9 | +0.0314 | +0.0050 | −0.0411 |
| 252d | 1 | +0.0314 | −0.0234 | −0.1637 |
| 252d | 9 | +0.0314 | +0.0175 | −0.0111 |

Every one of 18 tested (window, k, s) combinations **loses to carry-only**, monotonically in s, at every gate strength tested. The weakest gate (k=1, i.e. barely any usability filter) is catastrophic; even the strictest gate tested (k=9) only shrinks the damage, never reverses it. Full grid (18 points) logged regardless of outcome, per protocol.

### Why it fails — diagnosed, not just observed

Computed directly on the DEV panel: `corr(trailing 252d trend, forward 60d return)` = **+0.008 pooled** (essentially zero), and **19 of 30 names show a *negative* per-name correlation** between their own trailing trend and their own next-60-day return — i.e. a majority of the panel mildly *reverses* rather than continues. Sign-continuation hit rate is 54.6-58.4%, barely above a coin flip even restricted to the "confident" (`|t|>1.5`) subset. This is not a surprise in isolation — it is **the same qualitative finding already baked into `EGYPT.signal_type="rev_1m"` / `signal_sign=-1`**, whose own notes read *"Literature: no EGX momentum; overreaction/short-term reversal supported."* Round 7's diagnostic extends that already-validated character from the 1-month signal horizon out to 6-12 month trailing windows and finds the same sign. **Trend-following, as a uniform rule, fights the panel's own documented microstructure — that is why it loses, mechanically, not just statistically.**

### B2 — reversal-flip, exploratory (fades the trend instead of following it)

Given the diagnostic above, the mirror-image candidate (`drift = carry − s×tilt`) was tested as due diligence. Best point: window=126d, k=9, s=0.50 → **+0.0375** (vs baseline +0.0314), cov90=0.886 (in range). But the full grid shows a **peak-then-decline shape** as s rises past 0.5 (+0.0314→+0.0371→+0.0375→+0.0321→+0.0206) — the same signature this lab's own standing rule already rejected once (the illiquidity tilt in Round 6, and the CRPS-selection-by-maximization precedent the project ledger forbids reviving). It only survives in a narrow corner of the (window, k) grid; at the weak gate (k=1) it is just as damaging as continuation was, mirrored. **Not adopted** — it doesn't clear this lab's own bar for "real," and just as importantly, it is the *opposite* of what was asked (fading a trend, not following it), so even a clean result here would need to be flagged as a different thing than "individuality" before use.

### Named-stock sanity check (Task 31) — ORWE and PHDC, real numbers

| | latest origin | 126d t-stat | 252d t-stat | raw 6mo px chg | raw 12mo px chg |
|---|---|---|---|---|---|
| **ORWE** | 2026-01-13 | −0.40 | −0.45 | −3.9% | −5.3% |
| **PHDC** | 2026-04-14 | +0.68 | +0.49 | **+74.6%** | **+68.1%** |

The *sign* matches Sherif's chart read exactly — ORWE weakly negative, PHDC positive — and the shrinkage mechanism would give ORWE a near-zero tilt and PHDC a modest positive one, automatically, with no hand-tuning. The instructive part is the **magnitude**: PHDC's own trend t-stat is only ~0.5-0.7 despite a +75% six-month move, because t-stat measures the mean move against PHDC's *own* daily volatility, and this name is volatile enough that even a dramatic-looking rally isn't statistically loud by classical standards (you'd want |t|≈2 for real confidence). The human eye is an excellent pattern-matcher for a visual trend; the statistics — correctly — say even the strongest example in Sherif's own two screenshots is weaker evidence than it looks. That gap between "looks obvious on a chart" and "distinguishable from noise across a 30-name panel" is the entire reason a *uniform* trend-following rule loses money on this panel: for every PHDC there is an HRHO, EFIH, LCSW, JUFO, or CCAP (all showing *strongly negative* trend-forward correlation, −0.29 to −0.58) where the identical rule actively hurts.

### Combined spot-check (dated-CAPM level fix + reversal tilt)

One combined point (dated-CAPM s=0.5 + reversal-tilt s=0.5): crps_skill +0.0408 vs carry-only +0.0314 on the identical harness — larger than either piece alone. **Flagged, not claimed as a finding:** this is a single, unswept spot-check, and the tail-instability doc's own collateral finding already documented that this exact gate carries roughly ±0.01 (±1.0pt) of seed-to-seed pooled-CRPS noise even at h=60 — almost exactly the size of this "improvement." One lucky point is not evidence; it would need a swept grid and a seed-robustness check before it means anything. Logged for the record, not recommended.

## Scoring against the four standing criteria

- **A — cones/drift mimic real life:** partially. Sign is directionally right for the two named examples (and the mechanism produces this automatically, not by hand-tuning), but the magnitude a human reads off a chart is not statistically distinguishable from noise for most of the panel, most of the time — "realistic-looking" and "statistically supportable" are in real tension here, not aligned.
- **B — individuality maintained (cone shape, drift, return):** shape — already true today (HAR vol is per-name, cones already vary 0.45-1.14× in width per Round 0). Drift/return — no construction tested (this round or prior) survives the walk-forward gate as a *uniform rule*; the sign is individually correct for named examples but the panel-wide rule that would generalize it is not supportable.
- **C — passes the dumb yardstick (beats carry on the walk-forward CRPS gate):** trend-continuation, no. Dated-CAPM, no longer (was marginal-positive on the static snapshot, now flat-to-negative once bulletproofed). Reversal-flip, marginally and only in a noise-shaped, unswept corner — not trusted.
- **D — cov90 within 88-92%, ±2pt:** every variant reported here stayed inside [0.88, 0.92] except the catastrophic weak-gate trend-continuation cases (already rejected on crps_skill alone) — so D was never the binding constraint this round; C was.

## Drift ledger, updated

Now nine tested families: secular/unshrunk trend (retired), β×trailing-ERP (FAILED), zero-net momentum (FAILED), vol-rank (FAILED), LHAR vol-asymmetry (FAILED, vol-side), Bayes-Stein grand-mean shrinkage (FAILED), CAPM/beta static-ERP (**downgraded**: was reported REAL in Round 6, now shown to be ~80% look-ahead artifact once dated — real residual effect not distinguishable from noise), illiquidity tilt (inconclusive, not adopted), signed trend-continuation (FAILED, mechanistically diagnosed), signed trend-reversal (noise-shaped, not adopted, also not what was asked).

## Recommendation on the FINAL-window shot

**Do not spend it yet.** Nothing tested — across seven rounds and ten distinct constructions now — has produced a candidate that is simultaneously (a) a real, swept, non-peak-shaped, robust effect on DEV and (b) something that would survive being described honestly to a skeptic. Spending the one held-out shot on any of today's candidates would be spending it on noise. The most promising unexplored direction is not another price-derived statistic — this lab has now tried price levels, returns, momentum, reversal, and co-movement, all from the same underlying ~5.5yr return series — but a genuinely different data source already native to this project: **pulling drift toward each stock's own DCF/SOTP fair value** (the studies already exist for ISPH, ORHD, EAND, ADCB, ALPHADHABI) rather than toward a panel-wide statistical average. That is real, new work (extending fair-value coverage across more of the 30-name panel), not another grid search, and it is the first candidate in this lab that would tie the MC engine's drift to something the project already treats as ground truth elsewhere.
