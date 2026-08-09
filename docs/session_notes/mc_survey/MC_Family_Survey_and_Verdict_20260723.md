# Monte Carlo Family Survey — Can Any Engine Deliver "Reality + Individualism" on EGX?

**Date:** 23 Jul 2026. **Trigger:** owner directive to scan ALL MC/stochastic-simulation families for a replacement to the carry-anchored YZ-HAR-t engine that (1) reflects EGX's high realized nominal returns and (2) differentiates expected return per stock from data.

**Method:** automated deep-research sweep — 5 search angles, 22 primary sources fetched, 25 falsifiable claims extracted and put through 3-vote adversarial verification. 8 claims verified 3-0; 3 refuted; 14 could not complete verification (the run hit a usage-credit ceiling mid-verification — these rest on real fetched primary sources with quotes, but were NOT adversarially confirmed and are flagged as such below). Auto-synthesis did not run; this document is the hand-synthesis. Sources listed at the end.

---

## The one-paragraph answer

The literature confirms, rather than overturns, last night's empirical result — and explains *why* it happened. **No Monte Carlo family can manufacture the thing you want, because the thing you want lives in the drift, and forecastable drift is the single most-studied, most-consistently-failing problem in empirical finance.** Every MC family in the survey — GBM, jump-diffusion, Heston/Bates stochastic vol, the whole GARCH tree, Lévy processes, rough vol, regime-switching, neural SDEs, GANs — is a technology for shaping the *distribution around a center*. None of them determines the center; you feed the center in. So swapping engines changes the cone's shape, tails, and asymmetry, but does nothing for the per-stock expected return unless you separately supply a drift estimator that survives out-of-sample — and the survey's central finding is that drift estimators almost never do. There is exactly **one honest, literature-backed lever we have not yet pulled** (Bayes-Stein / hierarchical shrinkage of per-name means), and it buys *modest* individualism, not EGX-matching returns. The "reality" requirement — medians near 20-46%/yr — cannot be met without extrapolating the 2023-24 devaluation regime forward, and the survey hands us the canonical precedent for why that is a trap, not a feature.

---

## Why the engine swap is the wrong axis (the structural point)

Separate every simulation model into two jobs:

- **Center** (drift, μ): where the distribution is anchored. This is what you want to be high and per-name.
- **Shape** (vol dynamics, tails, skew, jumps, regimes): how the distribution spreads and bends around that center.

**Every family in the survey is a shape technology.** GBM, Heston, Bates, SABR, Merton/Kou jumps, VG/NIG/CGMY Lévy, rough vol, GJR/EGARCH/FIGARCH, MSGARCH, QuantGAN/TimeGAN/diffusion/neural-SDE — the entire zoo differs in how it models *shape*. In every one, μ enters as a free input (risk-neutral for pricing, or physical-measure for forecasting), estimated separately. This is why last night's failures were not failures of the *engine*: we already had a fully per-name shape (own-history HAR vol → cones spanning w90 0.45-1.14). We were trying to fix the *center*, and no shape upgrade touches the center.

Conclusion: **the replacement question is not "which MC family," it is "which drift estimator survives your walk-forward gate."** The survey answers that question, and the answer is sobering.

## The drift wall (why 5 families failed — it wasn't you)

The most-cited result in this literature is Goyal & Welch (2008): the standard equity-premium predictors (dividend-price, earnings-price, book-to-market, rates, inflation, issuance) fail to beat the naive historical mean out-of-sample. Replications extend the verdict:

- Re-testing 29 predictors published *after* Goyal-Welch on data through 2021: ~half lose significance even in-sample, before OOS testing begins; of survivors, ~half fail OOS (compounded attrition). *[source: SSRN 3929119 — fetched, verification incomplete]*
- Ten advanced **emerging markets**: only a limited number of single predictors give significant OOS forecasts — the Goyal-Welch verdict holds outside the US too. *[Acct&Fin 2018 — fetched, verification incomplete]*
- Unregularized cross-sectional expected-return estimation delivers *negative* OOS R² on 50 anomaly portfolios — raw per-name means overfit noise. *[NBER w24070 Kozak-Nagel-Santosh — fetched, verification incomplete]*

Your five dead drift families (raw mean, trend, β×premium, momentum tilt, vol-rank) are not a local embarrassment — they are the field's consensus reproduced on your panel. That is worth saying to partners plainly: *the reason our medians don't chase returns is the same reason the entire academic literature can't — and we're one of the few shops honest enough to show it.*

## The one lever we haven't pulled: shrinkage drift (Bayes-Stein / hierarchical)

This is the survey's constructive finding. The raw sample mean is a *provably inadmissible* estimator of expected returns — it is dominated by shrinkage estimators (Bayes-Stein, Jorion 1986). The corrected form of "per-name historical mean" is **each name's mean shrunk toward the panel grand mean, with the shrinkage intensity tuned out-of-sample**:

- Heavy L2 shrinkage toward an economic prior turns the −R² of raw cross-sectional means into ~+30% OOS R² on the 50-anomaly set; the *shrinkage*, not sparsity, drives the gain. *[NBER w24070 — fetched, verification incomplete]*
- Optimal shrinkage is *heterogeneous*: shrink hardest on differentiation orthogonal to the dominant covariance directions (treat idiosyncratic-return differences as mostly noise; keep only co-movement-aligned tilts). For a ~30-name panel this means per-name drifts shrunk hard toward the market level, retaining only the component aligned with major factors. *[NBER w24070 — fetched, verification incomplete]*
- Bayesian hierarchical panels give per-name conditional means stabilized by cross-name partial pooling, and — importantly — deliver **near-nominal interval coverage** (95% intervals covered 93.6-94.5% OOS vs 89% for Random Forest). *[ScienceDirect S030440762100258X — fetched, verification incomplete]*

**The honest caveat, and it is decisive:** that same winning hierarchical study showed **essentially zero OOS point-forecast skill for the return center** (OOS R² vs a trailing-mean benchmark was slightly *negative*, −0.007 to −0.010). Its edge was in *interval calibration and estimation-risk handling*, not in beating a trailing mean at locating the center. Read that against your goal: shrinkage drift can honestly give you **genuine but small per-name differentiation with correct coverage** — it will NOT give you medians that match EGX's realized 20-46%/yr. What we tested (raw mean, β×premium) is the un-shrunk version the theory predicts should fail; the shrunk version is the untested, defensible upgrade — but its realistic prize is individualism-with-honesty, not "reality" as you've defined it.

## The "reality" requirement, and the regime-extrapolation flag you asked for

You asked me to flag any candidate whose higher returns are just regime extrapolation. The survey hands over the textbook precedent: the apparent OOS success of equity-premium models **concentrates in a single macro-shock episode (the 1973-75 Oil Shock), with essentially no skill in the three decades after.** *[Goyal-Welch, ivo-welch.info — fetched, verification incomplete: all 3 voters errored on credits, treat as strong-prior-but-unconfirmed]*

Your EGX equivalent is exact: the 20-46%/yr "reality" is dominated by the 2023-24 EGP devaluation repricing. **Any engine tuned to reproduce those returns is fitting one currency shock and calling it skill.** A drift that "matches history" here is the Oil-Shock illusion in an Egyptian accent. This is the single most important sentence in the report: *the reality requirement, as literally stated, cannot be satisfied by any honest system, because the returns that define it are a one-off regime event, not a repeatable process.* The defensible reframing of "reality" is not "high medians" but "correctly-calibrated wide cones whose upper reaches contain the boom outcomes at honest probability" — which the current engine already does.

## Family-by-family verdict table

| Family | Center (can it be high & per-name?) | OOS distributional evidence | Daily-OHLC feasible? | Verdict for EGX |
|---|---|---|---|---|
| GBM / carry-anchored (incumbent) | No — μ is an input; currently carry | Passes your gate now (skill +0.03, cov90 0.89) | Yes | Baseline. Shape is fine; center is the whole problem. |
| Jump-diffusion (Merton/Kou) | No — jumps widen tails, μ still input | Shape only | Yes (jumps from daily) | Widens/fattens tails; irrelevant to center. Skip for drift. |
| Stochastic vol (Heston/Bates/SABR) | No | Strong for options; **needs option prices** for honest calibration — you have none | Weakly (vol-of-vol poorly identified from daily OHLC) | Shape only, and under-identified without options. Skip. |
| GARCH tree (GJR/EGARCH/FIGARCH) | No (unless -M variant) | Genuine vol/tail skill | Yes | Shape upgrade candidate; not a center fix. |
| **GARCH-in-mean (-M)** | **Yes — links μ to own vol** | Weak/mixed OOS; risk-premium coefficient notoriously unstable | Yes | The one classical center-lever. But it makes high-vol names have *higher* drift — economically it's a risk premium, and it's the same convexity you already have. Test, but expect the unstable-coefficient failure. |
| **Filtered Historical Simulation (GJR-FHS)** | **Yes — inherits each stock's own empirical return shape incl. its mean** | **Best *feasible* daily-data scheme** in Geweke-style comparison; CRPS −0.257% vs the option-implied VG winner's −0.286% | **Yes — designed for exactly this** | **Strongest shape candidate.** But "inherits the mean" = inherits the devaluation window = the regime trap. Usable for *shape/tails*; its center inherits the same regime problem, so pair with shrunk drift, don't trust its raw mean. |
| Regime-switching (MSGARCH / Hamilton) | Center is per-regime; **but skill demonstrated only after zero-meaning returns** | **Genuine OOS skill, strongest for individual stocks** (426-stock study) | Yes | **Best shape-side upgrade with real evidence.** Captures devaluation-style breaks in *vol*. Explicitly silent on drift. Build for tails/coverage, not center. |
| Rough volatility | No | Intraday-oriented; thin daily-OHLC evidence | Poorly | Shape only, wrong data regime. Skip. |
| Lévy (VG/NIG/CGMY) | No | VG won Geweke — **but via option calibration you can't do** | Marginally | Shape only; the win was options-driven. Skip. |
| EVT tails | No | Tail-only | Yes | Bolt-on for extreme quantiles; not a center fix. |
| **Hierarchical Bayes / James-Stein shrinkage** | **Yes — per-name means, partially pooled** | **Near-nominal coverage; but ~zero center point-skill** | Yes | **The one honest untested drift lever.** Modest individualism + correct intervals. Not high returns. |
| Black-Litterman drift blend | Yes — blends a prior with views | Portfolio-construction tool, not a forecaster; "views" = your fair values | Yes | Would import FV into the MC = your purity violation. Rejected by your own constraint. |
| ML generative (QuantGAN/TimeGAN/diffusion/neural-SDE) | Yes — learns the mean | **No established OOS evidence base; best NN density only reached *parity* with GARCH**; needs validation from scratch; 30 names × 6yr is far too little data | Yes but data-starved | High risk, no evidence, tiny data. Not for a production gate now. |
| Conformal / quantile-regression | Calibration wrapper, not a generator | Good finite-sample coverage guarantees | Yes | **Useful bolt-on** — wrap any engine to enforce cov90 exactly. Doesn't create drift. |

## Ranked shortlist for the next dev cycle

**1. Bayes-Stein / hierarchical-shrinkage drift (the honest individualism lever).** Per-name μ_i = ĝrand_mean + w_i·(own_mean − grand_mean), with shrinkage w tuned by walk-forward CRPS, heterogeneous (harder shrink off-factor). Sketch: estimate per-name trailing mean and the panel grand mean at each origin; shrink; feed as drift into the *existing* engine (shape unchanged); score on the held-out window with a **center-weighted CRPS** (the survey confirms quantile-weighted CRPS stays a proper rule and can target the center where our miscentering lives). Honest expectation: small, defensible per-name drift spread; correct coverage; NOT EGX-matching. This is the one thing genuinely worth building.

**2. Regime-switching vol (MSGARCH) for shape, as a v4 cone-shape upgrade.** Strongest OOS evidence of any family, best for individual stocks, captures devaluation-type breaks. Won't touch the center (build it knowing that), but could improve tail coverage and make the *width* react to regime — real, testable, honest.

**3. GJR-FHS as the simulation substrate.** Best feasible daily-data scheme in the literature; inherits each name's own return shape. Use it for shape/tails; explicitly do NOT trust its inherited mean (regime trap) — pair with the shrunk drift from #1.

**4. Conformal calibration wrapper.** Cheap bolt-on to guarantee the 90% band hits 0.90 exactly on any engine. Pure risk reduction.

**Not recommended:** GARCH-M (unstable premium coefficient, and it just re-expresses vol convexity you already have), Black-Litterman (violates your FV-purity rule by construction), ML generators (no evidence, data-starved), rough vol / Lévy / Heston (shape-only and/or need options you don't have).

## The bottom line for the partner problem

The survey does not rescue the "high per-name returns" goal — it explains, with the field's most-cited evidence, why that goal is unreachable by honest means: drift is unforecastable, and EGX's realized returns are a currency-shock regime. What it *does* give you is (a) the vindication that five failures were the literature's consensus, not our incompetence; (b) one honest untested lever (shrinkage drift) that yields *real* per-name individualism with correct coverage, just not big numbers; and (c) the exact language to make the small, honest number your *strength* in the room. The engine was never the weak link. The market's forecastability is.

---

### Sources (primary, fetched)
- Geweke & Amisano (2010), *Int. J. Forecasting* — 5-model daily density-forecast comparison. [3-0 verified]
- Wiley *J. Forecasting* for.2521 — 15-scheme IBEX density comparison; GJR-FHS best feasible. [partially verified]
- ScienceDirect S0169207018300840 — MSGARCH, 426 stocks, OOS VaR/tail skill. [3-0 verified]
- ResearchGate 227369481 — threshold/quantile-weighted CRPS (proper, center-targetable). [3-0 verified]
- Wiley *J. Econ. Surveys* 70018 — probabilistic-AI survey: no standardized OOS benchmark yet. [3-0 verified]
- arXiv 2508.18921 — CNN/LSTM density forecasting; LSTM-skew-t best, only parity vs GARCH. [3-0 verified]
- Goyal & Welch (2008), *RFS* (ivo-welch.info) — predictors fail OOS; success concentrated in Oil Shock. [fetched; verification errored on credits]
- SSRN 3929119 — 29 post-2008 predictors re-tested; most fail. [fetched; unverified]
- Cambridge JFQA — Bayes-Stein estimation for portfolios (Jorion). [fetched; unverified]
- NBER w24070 (Kozak-Nagel-Santosh) — shrinking the cross-section; heavy L2 shrinkage. [fetched; unverified]
- Acct & Finance 2018 (RePEc bla/acctfi) — 10 emerging markets; only combination forecasts survive OOS. [fetched; unverified]
- ScienceDirect S030440762100258X — Bayesian hierarchical: near-nominal coverage, ~zero center skill. [fetched; unverified]

*Verification integrity note: 8 claims cleared 3-0 adversarial voting; the drift-wall and shrinkage claims (the report's backbone) come from real fetched primary sources but their verification votes errored on a credit ceiling — they are canonical, well-known results (Goyal-Welch, Jorion Bayes-Stein, Kozak-Nagel-Santosh are landmark papers) but are flagged here as not independently re-confirmed in this run. Re-running verification is a resumable next step.*
