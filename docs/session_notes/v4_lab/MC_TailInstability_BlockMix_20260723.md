# MC Engine — Terminal-Mean Instability at Long Horizons, and the Block-Mixture Fix (23-Jul-2026)

**Status: lab finding + validated candidate fix. Production untouched. This is the most consequential engine finding of the v4 lab so far — it affects published deck numbers, not just internals.**

## The finding

The engine's fat tail is built as `price = spot × exp(drift + z·mix·σ)` where `mix = sqrt((ν−2)/χ²_ν)` — one chi-square draw per path, frozen for the whole path (`simulate_paths_v3` / `simulate_terminal_v3`). Two consequences, one structural, one practical:

1. **The theoretical mean of the terminal-price distribution is INFINITE.** A Student-t has no moment-generating function: E[exp(σT)] diverges for any σ>0. Every "mean/EV" ever computed from these paths is a sample mean of an infinite-mean distribution — a number that converges to nothing as paths→∞ and is dominated by whichever near-zero chi-square draws the seed happens to contain. Medians, percentiles, cones, touch probabilities are all UNAFFECTED (they depend on the distribution function, not moments).

2. **The one-mix-per-path construction extrapolates the 60-day tail shape unchanged to any horizon.** ν=4 was FITTED on 60-day residuals. A path that draws mix=10 is simulated at 10× volatility for three straight years — the aggregation-to-Gaussian (CLT) that real multi-period returns undergo is structurally suppressed. This is why the instability explodes with horizon.

## Quantified impact (ISPH, production config ν=4, cal=0.972, 50k paths, seed 42)

| horizon | max path | mean total ret | mean ex-top-0.1% | median | top 0.1% of paths contributes |
|---|---|---|---|---|---|
| T+60 | 13× spot | 6.6% | — | 4.4% | negligible |
| 1yr (H=240) | 205× | 31.9% | 29.7% | 18.7% | 2.3pts |
| 2yr (H=480) | 25,803× | 160.6% | 70.9% | 40.7% | 89.8pts |
| 3yr (H=720) | 98,290× | 520.2% | 125.1% | 66.6% | 395.2pts |

**Deck lineage confirmed exactly:** the introduction deck's published EVs reproduce bit-for-bit from H=500/H=750 seed-42 runs — 2yr 39.2% ann. (mean_tot 93.7%), 3yr 75.5% ann. (mean_tot 440.7%, driven by a 76,687× path). ORHD's 38.6%/72.5% same story.

**The seed lottery, demonstrated (ISPH 3yr, identical model/inputs, only the seed changes):**

| seed | production EV (ann.) | block-mix EV (ann.) | median (both) |
|---|---|---|---|
| 42 | 75.5% | 32.8% | 19.4% |
| 43 | 146.1% | 34.0% | 19.4% |
| 44 | **884.0%** | 33.5% | 19.4% |
| 45 | 76.9% | 36.7% | 19.7% |
| 46 | 50.3% | 34.3% | 19.2% |

The published "3yr EV 75.5%/yr" could have been 884%/yr on a neighboring seed. The medians are rock-stable at ~19.4%/yr. **The deck's 2yr/3yr EV columns (and the 2yr/3yr rows of the stop-loss EV tables) are seed artifacts. The 1yr EVs are only mildly contaminated (~2.3pts of 31.9%). All cones, medians, percentiles, touch ladders, and the T+60 production forecasts are unaffected.**

## Collateral finding — the Step-0 gate itself carries MC-sampling noise

CRPS = E|X−y|−½E|X−X′| needs a finite first moment of X — which lognormal-t does not have. So even h=60 pooled CRPS skill is exposed: four independent-seed reruns of the identical carry-only config on the identical 447 DEV windows (20k paths) gave pooled skills +0.0233 / +0.0293 / +0.0314 / +0.0335 — a ~1.0pt spread on a gate whose adopted panel PASS is +0.0204 and whose bootstrap CI (which resamples windows, not paths) cannot see this noise. One hash-salted rerun landed at −8.1 skill from a single chi²≈1e-4 draw. Same-seed PAIRED deltas between variants remain clean (shared draws cancel), which is why the lab's relative verdicts stand — but absolute gate levels have more uncertainty than the ledger CIs state. Candidate fixes to test: score CRPS in log-price space (t(4) has finite E|X| in logs → finite CRPS; still a proper score, applied to both engine and benchmark), or winsorize samples for scoring only. NOT yet tested — flagged for a dedicated round.

## The fix candidate: block-mixture (redraw mix per 60-session block)

`simulate_paths_blockmix`: identical to production except the chi-square mixture is redrawn independently per 60-session block — the horizon ν was actually fitted on — instead of once per path. Properties:

- **At h≤60 it is bit-for-bit IDENTICAL to production** (one block; verified numerically: T+60 row matches to every digit). The entire Step-0 calibration, all T+60 published forecasts, all ledger cohorts are untouched by construction.
- At long horizons the terminal distribution correctly thins toward Gaussian (sum of independent t-blocks), while each 60-day window retains the calibrated t(4) fatness. 3yr max path 276× vs 98,290×; 3yr EV stable at 33–37% ann. across seeds (vs 50–884%); medians/percentiles essentially unchanged (p5/p95 within a few points, median identical).
- Theoretical mean is still technically infinite (each block is still lognormal-t) but the practical instability collapses by ~200× at 3yr; a documented trimmed/winsorized mean or median-first reporting remains the right presentation layer on top.

## Recommendations (in order)

1. **Presentation now:** anywhere a multi-year "EV/mean" is shown (deck EV tables, decile slide, stop-loss tables), lead with the MEDIAN (stable, honest) and show mean only winsorized with the trim stated — or drop long-horizon means entirely. The 1yr numbers can stand with a footnote.
2. **Engine next:** adopt block-mixture for any simulation beyond the fitted horizon (h>60), after it clears the standard promotion test (it cannot change h=60 backtests by construction, so the test is on long-horizon realism: e.g., 240d/480d walk-forward coverage where history allows).
3. **Gate hygiene:** dedicated round on log-space CRPS scoring for Step 0; re-state ledger CIs if adopted.

Scripts: `claude/v4_lab/lab_blockmix_demo.py` (session `/tmp` work consolidated). Related: Equation_Lab_Round6 (the CAPM level-fix finding, unaffected by this — its paired deltas used shared seeds).
