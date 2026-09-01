# TESTAHIL — where the money is, consolidated (01-Sep-2026)

Internal. Consolidates three documents into one ranked list:

- **A** — "Our channels, ranked by what they are actually worth" (internal, 25-Aug-2026; 37-name EG book, walk-forward, non-overlapping windows, net of 0.35% a side, seed 42).
- **B** — "The money is not in the cone's centre" memo (24-Aug-2026; 1,794 resolved EG 3-month windows, live profile imported).
- **C** — "Strategic Alpha Generation on the EGX" (narrative, Aug-2026; class-conditional lens playbook with TMGH / HELI / COMI / FWRY / EKH worked examples).

Every figure below is quoted **as measured in those sessions on the 23–25 Aug-2026 close**. All of them are
volatile — fits, ledger counts, library ages, fair-value stamps — and none may be re-quoted from this file.
Read the live state first (`engine/market_profiles.py`, `engine/fitted_configs.json`,
`python3 scripts/check_technical_read.py`, `python3 scripts/check_band_vocabulary.py`). Nothing here is a rating
or a price target.

---

## The combined list, ranked by what each channel is worth

### 1. Be in the market at all, sized off the cone's p5 — the regime/beta return
**Status: PROVEN on our own record. Worth more than every selection edge combined.**

- A: the 37-name covered panel, equal-weight, rebalanced quarterly net of commission, returned **71.9%/yr at 27.0% vol post-March-2022** (Sharpe 1.94 vs 19.5% cash) and 33.0%/yr at 35.7% vol over the full 15 years. Every selection edge below is worth 3–9 points a year; being in the market was worth ~50.
- B, the same thing measured net of the engine's own carry over 1,794 resolved 3-month windows: **+5.54%/qtr excess, t = 6.07, +24.8%/yr post-2022** — but **−2.26%/qtr, t = −2.53, −8.6%/yr over 2017–2021**. Egyptian equities lost to T-bills for five straight years and have beaten them decisively since the devaluation.
- The two documents agree on the mechanism and on the honest caveat: TESTAHIL **measures** this regime (the break date is its own) but **does not forecast it**. Say so to clients.
- What the product actually sells here is not a forecast but a **survivable size**: the cone prices the drawdown in advance (median published 3M p5 across the book −23.5%; worst panel quarter −14.0% post-2022, −23.9% full sample), so the position is sized against a real number rather than an optimistic one. The reason people fail to collect this return is that they are sized to be shaken out of it.

### 2. Execution — entries, scale-outs and stops priced off the touch ladder, not guessed
**Status: PROVEN. Worth discipline, not alpha — and it is the most immediately monetisable output already published.**

- B: over 1,699 non-overlapping 3M windows, **55% touch −10%** from the origin and **65% touch +10%**; median worst drawdown inside a window −11.1%, median run-up +16.0% (post-2022: 48% / 76%, −9.5% / +22.2%). Consequences: staggered limits at −5%/−10% get filled in most windows; scale-outs at +10/+15/+20 hit often; **any stop tighter than ~11% on an EGX name is noise, not risk management**. Size off p5, not off a round-number stop.
- A, the per-name version: because the bands are calibrated, the touch ladder is a probability, not a chart line. PHDC at 15.20: 20.00 at 19% over 3M, 17.50 at 51%, 16.50 at 71% — so a plan to scale at 14.50–16.50 is a two-in-three event this quarter, while a reload plan at 11.50–12.50 sits below the 3M p5 (11.98) and is a one-in-twenty event. **Any target above a name's p95 is a target the price process gives under a 5% chance.**
- C adds the same rule as an execution mandate: where the fundamental lens says cheap but the cone's p5 sits far below spot, **tranche the entry** on the −10%/+10% touch probabilities rather than deploy at once.

### 3. A quarterly momentum tilt into the top tercile (3-month horizon only)
**Status: REAL on 15 years, THIN, FLAT since 2022. Size it as a tilt, never as a conviction trade.**

- A: two constructions clear the cross-sectional bar on the EG panel, both only at 3M — six-month momentum (XS IC +0.049, tercile spread +1.80%/qtr; **top tercile beat equal weight by +8.7%/yr over 56 quarters** net of costs) and the 200-day trend (+6.1%/yr full sample, +9.2%/yr post-2022). Six-month momentum runs **−2.2%/yr post-2022** (17 quarters) — low power, not refutation.
- B, on 70 independent quarters, puts the top-vs-bottom-third portfolio at **+0.5 to +1.8%/qtr with t = 0.37–1.12 — not significant**.
- **The two documents disagree on whether the tercile edge is significant, and the disagreement is recorded rather than averaged**: A reports a point spread with no test statistic, B reports the test. Until a 3-month live record exists (see gap 3 below) the B reading is the one to size on.
- Both agree on two qualifications: (i) the construction the engine tilts on — 12-1 momentum — is a **time-series** signal (IC +0.068 at 3M) but is **cross-sectionally flat** (ranking on it lost 5.3%/yr): it improves each name's own centre by up to ~4% and says nothing about which name to prefer; (ii) with 31–35 of 37 names printing an UP call, the **sign carries almost nothing in this tape — only the rank is information**.

### 4. The gap between the fundamental lens and the price — the largest claimed edge, currently unusable
**Status: BLOCKED. Highest-return fix in the system.**

- The biggest numbers in the whole system sit here (A: EMFD 72% below base fair value, TMGH 50%, ISPH/ORHD 34%; KABO/EGCH 74% above, ELEC 84%). If current, that is a portfolio. It cannot be sized because:
  - **33 of 37 EG fair values carried no as-of date** (only PHAR, EGCH, ARCC, AMOC stamped, all 6-Aug-2026) in a book whose median name had risen 55% in twelve months — the exact defect the 29-Jul technical-read rule closed, still open on the lens that matters most;
  - B: the value-gap backtest (`engine/value_gap_backtest_EG_20260824.md`) is **n = 32, IC −0.14, insufficient power — ~783 observations needed**; only 8 of 37 EG names had committed studies; at 3M only 17 of 37 fair values were even in reach of the cone. **Most of today's "gaps" measure staleness, not cheapness.**
  - With cash at 19.5%, a two-year value trade needs **~44% cumulative just to draw level**.
- C supplies the **class-conditional playbook for where a gap would be trusted once dated**, all consistent with the protocol's lens-by-class rule: developers on Split-NAV (no terminal value on finite land banks; escrow/handover cash release; cap rate only on recurring legs — TMGH's EGP 457.9bn unrecognised backlog modelled into the cash-release engine, HELI as a pure land-monetisation RNAV bought only at a deep structural discount); banks on a rate-path NIM bridge + DDM keyed to deposit duration (COMI's CASA ratio at 62%, NIM 8.88%, CET1 22.5%, ROAE 31.9% against a 25%+ Ke — the crux is CASA stickiness under easing); aggregators on take-rate migration by segment (FWRY: banking + financial services ~72% of revenue, ADP diluted to 19%; the crux is defending a 56.7% EBITDA margin); holdcos on disciplined SOTP with holdco net debt as its own line (EKH — **not in the covered book**; the urea price per ton is the observable crux).
- C's own hurdle-rate screen belongs here too: in a market whose equity hurdle exceeds 25%, only **deep NAV discounts** and **ROIC-far-above-Ke franchises** clear it; ordinary growth-at-a-reasonable-price does not. (Flag: C builds that hurdle on the raw 12-month T-bill yield of ~26%; the protocol's cost-of-capital rule normalises rf by the sovereign's own default spread and adds country risk once via the ERP, so C's number **double-counts sovereign risk** — the screen is directionally right, the figure is not conforming.)
- **Unlock, in order: stamp every fair value with its as-of date and re-strike the ones that predate the rally; finish the EG study book; keep the libraries current.** That starts the clock on the only test that would prove the research adds return. Nothing else on the roadmap is worth as much.

---

## Tested and refuted — stop doing these (A and B agree)

- **Monthly rebalancing.** Every one-month construction is net-negative after the 0.70% round trip (combo long-short −2.7%/yr at 1M vs +1.6% at 3M; 12-1 momentum −9.9%/yr). On EGX the commission is larger than the signal. Quarterly or not at all.
- **Sizing by cone width.** Inverse-vol weighting returned 31.2%/yr at 34.7% vol vs 33.0% at 35.7% equal-weight (Sharpe 0.34 vs 0.38), worst quarter slightly worse. The 37 names span only 2.2× in cone width and co-move too hard for weighting to bite.
- **Trading the p50.** The centre is carry — ln(1+rf) − ln(1+q) at a 19.5% policy rate, ~+1.5%/month, identical for every name; panel skill against it is +0.9% with a CI straddling zero. Reading p50 as a target is reading the risk-free rate as a forecast.

## Claims in document C that do not describe the system as it stands — do not sell them
- "60-session" / "T+20" horizons: horizons are **calendar-only, 1M/3M**; the session-counted names are retired.
- "Step 0 evaluates CRPS skill against a random walk": the skill verdict is **retired outright** [R-CAL-03]; what a reader is shown is the **band record** [R-CAL-02].
- "16 factors combining macro drivers and discrete events": the production engine is carry-anchored YZ-HAR-t with **one price-native momentum socket**; no macro factor enters the drift.
- "Student-t(5)": ν is **weakly identified** and read live, never quoted as fixed.
- What C gets right and is worth repeating: the fundamental gap is **kept out of the drift** so the cone measures market probability, not reversion to the analyst's number [R-LENS-01]; and the expert-panel divergence table isolates the single variable behind a pricing spread.

## Standing caveats that change how the channels above are sized
- **Bands that under-cover** (own resolved history, 90% band): ISPH 77%, BTFH 80%, CCAP 84%, AMOC 86% — size wider than the page says; ISPH also carried the second-largest claimed fundamental upside.
- **Stale libraries**: 11 of 37 were running behind on 25-Aug (AMOC, ARCC, COMI, EGCH, ELEC, EMFD, OCDI, ORHD, PHAR, SCEM, SWDY); two of the four largest gaps (ORHD, EMFD) sat on month-old cones. **This list is already stale by construction — read it live** (`python3 scripts/check_technical_read.py`).
- **The tilt is ungraded**: live from 23-Aug, none of the 50 graded rows carried a signal_z; first grades late September.
- **No 3-month live record**: all 50 graded rows were 1-month; the horizon where the only tradeable cross-sectional edge lives had zero live evidence.
- **Regime, watch not act**: median realised quantile 0.587 across 32 EGX grades, forecasts undershot by +3.3%, both 90%-band breaks to the upside — a bull quarter on a correctly calibrated cone, not yet a calibration failure.

## What would make the system worth more money, in order
1. **Date every fair value and re-strike the pre-rally ones** — converts the largest block of claimed edge from unusable to tradeable.
2. **Finish the EG study book** (8 of 37 had committed studies) — the campaign now running.
3. **Keep the libraries current** — the only thing that unblocks the stale names.
4. **Grade the direction calls** — the per-name direction record has nothing to compute on yet.
5. **Get a 3-month graded record** — settles the A-vs-B disagreement on the momentum tercile.
