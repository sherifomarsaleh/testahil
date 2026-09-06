# TESTAHIL — where the money is, consolidated (01-Sep-2026)

Internal. Consolidates six documents into one ranked list:

- **A** — "Our channels, ranked by what they are actually worth" (internal, 25-Aug-2026, v1 window construction).
- **B** — "The money is not in the cone's centre" memo (24-Aug-2026; 1,794 resolved EG 3-month windows).
- **C** — "Strategic Alpha Generation on the EGX" (narrative; class-conditional lens playbook with TMGH / HELI / COMI / FWRY / EKH worked examples).
- **D** — "Rev. 8 … asymmetric probability engine" (six protocol-rule-keyed mechanisms).
- **E** — "EGX monetisation review — 25-Aug-2026 v2" (re-derived after the 25-Aug refits, 57 origins, 1,718 name-quarters). **Where E re-derived a figure it supersedes A**, by A's own v1/v2 rule.
- **F** — the four-mechanism quick answer (live EG profile read).

Every figure below is quoted **as measured in those sessions on the 23–25 Aug-2026 close**. All of them are
volatile — fits, ledger counts, library ages, fair-value stamps — and none may be re-quoted from this file. Read
the live state first (`engine/market_profiles.py`, `engine/fitted_configs.json`, `python3 scripts/check_technical_read.py`,
`python3 scripts/check_band_vocabulary.py`, `python3 engine/direction_record.py`). Nothing here is a rating or a price target.

**The one-paragraph answer (E's, which the other five support):** what TESTAHIL verifiably knows is the SIZE of EGX
moves, not their direction. The cone is calibrated (EG 1,794 resolved 3-month windows, 92.8% inside the 90% band; the
32 graded EGX 1-month rows 53% / 94%), the direction lean is real but small (hit 52.6% ±2.6% on 1,393 historical calls),
and the fundamental lens — the only one that claims large differences between names — has no graded record at all.

---

## The combined list, ranked by how well each channel is evidenced today

### 1. Be in the market at all, sized so the published p5 is survivable
**PROVEN. Worth more than every selection edge combined. (A, B, E, F all rank it first.)**

- E (v2, supersedes A): equal-weight covered panel, quarterly, gross — **full sample +25.7%/yr at 29.9% vol** (cash 12.3%, Sharpe 0.53, worst quarter −30.2%, max drawdown −53.3% into Q1-2020); **post-2022 +60.8%/yr at 26.2% vol** (cash 21.9%, Sharpe 1.26, worst quarter −16.1%, 76% of quarters beat cash). A's v1 figures (71.9% / 33.0%) were a different window construction.
- B, net of the engine's own carry: **+5.54%/qtr excess, t = 6.07, post-2022** but **−2.26%/qtr, t = −2.53 over 2017–2021**. Egyptian equities lost to T-bills for five straight years and have beaten them decisively since the devaluation. TESTAHIL **measures** this regime (the break date is its own) and **does not forecast it** — say so to clients.
- What the product sells here is a **survivable size**, not a forecast: a single name closes a quarter below −15% in 15.1% of windows and below −25% in 4.9% (E); the median published 3M p5 across the 37 names is ~−23%. The cone prices the drawdown before it happens so the position is sized to hold through it. People fail to collect this return because they are sized to be shaken out of it.

### 2. Execution — entries, scale-outs and stops priced off the touch ladder
**PROVEN. Worth discipline, not alpha, and the most immediately monetisable output already published. (A, B, D#3, E, F#1.)**

- Touch facts inside a quarter (E, B agree): a name touches **−10% intraday 54%** of the time (−15%: 38%), **+10% 65%**, +15% 52%, +20% 41%, both −10% and +10% 23%. Median worst drawdown inside a window −11.1%, median run-up +16.0% (B). So staggered limits at −5%/−10% fill in most windows and scale-outs at +10/+15/+20 hit often.
- **Scaled exits matter as much as entries** (E): of quarters that touched +15%, 21% still closed below +5% and 14% closed negative; of quarters that touched −10%, only 29% closed above the origin.
- **Stops are noise at EGX widths** — anything tighter than ~11% (B), and even a −25% three-month stop is noise-level for the typical name (E). **Use size, not stops.**
- Per-name arithmetic (A): PHDC at 15.20, 16.50 at 71% / 17.50 at 51% / 20.00 at 19% over 3M, so a scale plan at 14.50–16.50 is a two-in-three event and a reload plan at 11.50–12.50 sits below the 3M p5 (11.98), a one-in-twenty event. **Any target above a name's p95 is one the price process gives under a 5% chance.** D's version — bid at the level the ladder says is likely to be touched rather than at spot, sell euphoria into the upper band — is the same rule; note the ladder is at ±5/10/15/20% relative levels on the calendar 1M/3M cones, not "T+20/T+60".

### 3. The momentum lean — a filter and tie-breaker, never a strategy
**REAL, SMALL, MEASURED. Worth a few percent a quarter on strong-signal names. (A#2, D#2, E-C, F#2; E-B refutes the portfolio version.)**

- The engine's own lean (E): sign of `mom_combo` z vs the 3-month return net of cash, outside the 0.25 dead zone — **hit 52.6% ±2.6% (n = 1,393, base rate 51%)**; post-2022 54.2% ±4.3% with UP called 81% of the time against a 59% base rate. By strength: |z| 0.25–1 hit 51.3%, +1.1%/qtr; **|z| 1–2.5 hit 54.6%, +3.7%/qtr**; |z| > 2.5 hit 47.4% (n = 38). Consistent with the fitted IC of 0.06–0.07.
- Use (F, D): a **filter** — don't buy against a strong negative call — and a timing tie-breaker between names you already want; weight names whose own direction record grades well via `direction_record.py` once it has rows to score.
- **The cross-sectional tercile is refuted in v2** (E supersedes A's +8.7%/yr): top tercile net of costs — `mom_6_1` +5.1%/yr full (t = 2.5) but −8.2%/yr post-2022; production `mom_combo` +1.2% / −5.0%; `mom_12_1` −5.3% full; trend200 −1.3% full, +14.6% post-2022 (t = 1.2). **No construction is positive in both samples.** B's own read (t = 0.37–1.12 on 70 quarters) agrees.
- In this tape the sign carries almost nothing: 31–35 of 37 names print UP. Only the rank is information, and the rank does not pick names (above).

### 4. The fundamental gap — the largest claimed edge, blocked until it is dated and graded
**UNPROVEN. Highest-value build in the system. E would rank it #2 the day it has a record. (A#3, B#4, C, D#4/#5, E, F#3/#4.)**

- Today's gaps to base fair value (E): **12 names >30% ABOVE fair value** (ELEC −84%, EGCH −74%, KABO −74%, OIH −59%, RMDA −56%, DSCW −55%, PHAR −53%, CLHO −48%, EFIH −43%, AMOC −35%, SWDY −34%, SCEM −33%) and **6 >10% BELOW** (EMFD +72%, TMGH +50%, ISPH +34%, ORHD +34%, GBCO +21%, ORAS +19%). If current, that is a portfolio.
- **Measured 06-Sep-2026, correcting how the source documents put this: the fair values are not undated — 36 of the 37 EG names carry a published, dated valuation study on the site** (`files/{TK}_Valuation_Study_{DD-MM-YYYY}_public.pdf`; only CCAP has none). The dates run 11-Jun-2026 (PHDC) to 09-Aug-2026 (PHAR), and **26 of the 36 were struck in June or the first half of July** — before and during the rally. So the defect is AGE AND STANDARD, not absence: the number has a report and the report has a date on its face. What is missing is (i) the date in machine-readable form — only 4 names carry `fairAsof` in `assets/data.js`, so nothing computes with it and no gate can see it, and (ii) a rebuild to `STANDARD_VERSION` — the 23-Aug audit found the bulk of the book not ground-up, composite-beta era. Every one of the largest claimed gaps sits on a pre-rally study: EMFD 17-Jun, ORHD 25-Jun, KABO 6-Jul, OIH 3-Jul, ISPH 7-Jul, CLHO 13-Jul, RMDA 13-Jul.
- Why it still cannot be sized: **33 of 37 fair values carry no as-of stamp** (only PHAR, EGCH, ARCC, AMOC, all 6-Aug) in a book whose median name rose 55% in twelve months; the value-gap backtest is **n = 32, IC −0.14, insufficient power (~783 observations needed)**; only 17 of 37 fair values were in reach of the 3M cone (B); the early scorecard is Spearman +0.09 with the 11 cheapest names +10.7% and the 12 most expensive +10.1% — **the most expensive names were among the best performers** (KABO +30%, OIH +33%, RMDA +28% since their studies). Most of today's "gaps" measure staleness, not cheapness; and F's point decides which are even candidates: **only fair values rebuilt to `STANDARD_VERSION` are actionable** — the 23-Aug audit found the bulk of the book not ground-up, composite-beta era, so PHAR/EGCH/ELEC-type "spot far above fair" mostly signals a stale study, not a short.
- Hurdle (B): with cash at 19.5%, a two-year value trade needs **~44% cumulative just to draw level**. C's screen follows: in a >25% hurdle market only **deep NAV discounts** and **ROIC-far-above-Ke franchises** clear; ordinary growth-at-a-reasonable-price does not. (C builds its hurdle on the raw 12-month T-bill yield of ~26%; the protocol normalises rf by the sovereign's own default spread and adds country risk once via the ERP, so C's number double-counts — the screen is directionally right, the figure is not conforming.)
- **What the lens pays for once dated — the class playbook (C) and the two protocol mechanisms D names correctly:**
  - Developers on Split-NAV (no terminal value on finite land banks; escrow/handover cash release; cap rate only on recurring legs — TMGH's EGP 457.9bn unrecognised backlog into the cash-release engine; HELI as land-monetisation RNAV bought only at a deep structural discount).
  - Banks on a rate-path NIM bridge + DDM keyed to deposit duration (COMI: CASA 62%, NIM 8.88%, CET1 22.5%, ROAE 31.9% against a 25%+ Ke; the crux is CASA stickiness under easing).
  - Aggregators on take-rate migration by segment (FWRY: banking + financial services ~72% of revenue, ADP diluted to 19%; the crux is defending a 56.7% EBITDA margin).
  - Holdcos on disciplined SOTP with holdco net debt as its own line (EKH — **not in the covered book**; urea $/ton is the observable crux).
  - **Tracking physical drivers between earnings (D#4)**: because margins are outputs of unit cost stacks with one escalator per driver class, a reader can move the sensitivity grid on live urea/gas/FX quotes weeks before the release. Legitimate, but only on names rebuilt to standard, and **untested as a source of return** — it is an input to the gap, not evidence the gap pays.
  - **The sliding-schedule WACC (D#5)** is a real protocol device for markets in monetary transition (EG): a norm-built terminal rate rather than a flat crisis rate, with the sovereign double-count removed. Buying capex-heavy names cheap under it is buying the PV of the disinflation path — but that path is an assumption the walk-forward has not yet graded, so it belongs under this heading, not above it.
- **The build (E, A):** a fair-value ledger with the cone ledger's discipline — every fair value stamped `fairAsof`, frozen at strike, graded on gap-closure at 6 and 12 months, the record printed beside the fair value the way the band record sits beside the cone. Until then the fundamental lens is a hypothesis and the site should say so in plain words. Nothing else on the roadmap is worth as much.

### 5. Three-lens convergence — a gate on WHEN to act, not a source of return
**PARTLY REFUTED as a picker; retained as a discipline. (D#1, F#3 propose it; E-B tests it.)**

- The lenses are independent by construction [R-LENS-01], so agreement is information, not an echo. D and F's rule — deploy heavily only when fundamental floor, technical read and MC lean align; a big value gap with the other two against it is a "wait" — is a real defence against false starts and value traps.
- But **it does not pick names** (E): momentum-UP & trend-UP earned +0.9%/qtr over the same-origin panel mean (t = 0.9, median −2.9%); strong-z & trend-UP +0.3%/qtr (t = 0.2). The only lens that separates names is the fundamental one, and it is ungraded (channel 4). On 25-Aug five names had all three lenses long (EMFD, TMGH, ORHD, GBCO, ORAS — EMFD and ORHD on month-old libraries) and one all three against (ELEC).

### 6. Size by each name's own calibration record
**PROVEN AS RISK MANAGEMENT, refuted as a return source. (A, D#6, E.)**

- What a reader is shown is the **band record** [R-CAL-02] — count, coverage, and a flag only when earned; the per-name CALIB block D describes as "under the fan chart" is an internal diagnostic and renders nowhere (settled 25-Aug under R-CAL-03).
- Use it as D says: **size down where the name's own bands under-cover** — ISPH 77% (flagged narrow), BTFH 84%, CCAP 84%, AMOC 86% on own history; ETEL and PHAR flagged wide. ISPH also carried the second-largest claimed fundamental upside.
- Do **not** turn it into a weighting scheme: inverse-width sizing across the panel is refuted (below).

### 7. Watch-only: breadth as a timing observation
**NOT TESTED OUT-OF-SAMPLE, NOT PROMOTABLE. (E-D.)** Share of names in momentum-UP & trend-UP at origin correlates +0.23 (Spearman, 57 quarters) with the panel's next quarter; breadth <25% averaged +1.3% (worst −30%), >75% averaged +12.1% (6 quarters). Breadth on 25-Aug was 84%. Record it, do not act on it.

---

## Tested and refuted — do not revive without new evidence clearing the promotion rule
- **Monthly rebalancing** on any price signal: net-negative after the 0.70% round trip (combo long-short −2.7%/yr at 1M vs +1.6% at 3M; 12-1 −9.9%/yr). Quarterly or not at all.
- **Inverse-vol / cone-width sizing** across the panel: 31.2%/yr at 34.7% vol vs 33.0% at 35.7% equal-weight; the 37 names span only 2.2× in width and co-move too hard.
- **Trading the p50**: the centre is carry — ln(1+rf) − ln(1+q) at 19.5%, ~+1.5%/month, identical for every name; skill against it +0.9% with a CI straddling zero.
- **Cross-sectional momentum tercile as a selection rule**: sign-unstable across samples (E v2).
- **Lens agreement (momentum × trend) as a stock picker**: zero excess vs the panel (E v2).

## Claims in C and D that do not describe the system as it stands — do not sell them
- "T+20 / T+60", "60-session horizon": horizons are **calendar-only 1M/3M**; session-counted names are retired.
- "Step 0 evaluates CRPS skill / PIT against a random walk": the skill verdict is **retired outright** [R-CAL-03]; what a reader sees is the **band record** [R-CAL-02].
- "16 factors combining macro drivers and discrete events": the engine is carry-anchored YZ-HAR-t with **one price-native momentum socket**; no macro factor enters the drift.
- "Student-t(5)" as a fixed fact: ν is **weakly identified**, read live, never quoted as precise.
- "Per-stock scoreboard under the fan chart": the CALIB block is internal; the band record is what renders.
- "Mathematically validated momentum lean", "perfectly adapts to each stock's volatility": the lean hits 52.6%; the width overlay is history-gated, clipped to (0.7, 1.5), active name by name and read only by recomputing [R-WIDTH-01].
- What C and D get right and are worth repeating: the fundamental gap is **kept out of the drift** [R-LENS-01]; margins are **outputs** of unit cost stacks [R-SIGCM-02]; the EG WACC is a **sliding schedule**, not a flat crisis rate; the expert-panel divergence table isolates the single variable behind a pricing spread.

## Standing caveats that change how the channels above are sized
- **Stale libraries**: 11 of 37 on 25-Aug (ELEC/SWDY 5-Aug; ARCC/AMOC/EGCH/PHAR/SCEM 6-Aug; COMI/EMFD 28-Jul; OCDI/ORHD 27-Jul); ORHD and EMFD — two of the six positive-gap names — sat on month-old cones. **This list is stale by construction — read it live.**
- **The tilt is ungraded**: 68 ledger rows carry `signal_z`, none graded; `direction_record.py` has nothing to score until late September.
- **No 3-month live record**: all 50 graded rows are 1-month; the horizon where every claimed edge lives has zero live evidence.
- **Regime, watch not act**: median realised quantile 0.587 across 32 EGX grades, forecasts undershot by +3.3%, both 90%-band breaks to the upside — a bull quarter on a correctly calibrated cone, not yet a calibration failure.
- **PHDC (held)** as the worked example of the whole list: gap +5% to base (15.89 vs 15.20; bear 7.62 / full 24.92), momentum UP (z +1.94), trend UP, band record 57 windows at 91% — every lens says hold, none says add on fundamentals.

## What would make the system worth more money, in order
1. **A graded fair-value ledger**: stamp every fair value `fairAsof`, freeze at strike, grade gap-closure at 6 and 12 months, print the record beside the number. Converts the largest block of claimed edge from hypothesis to evidence.
2. **Finish the EG study book to `STANDARD_VERSION`** (8 of 37 had committed studies) — the campaign now running; it is the monetisation path, not a side project.
3. **Keep the libraries current** — the only thing that unblocks the stale names and their cones.
4. **Grade the direction calls** as the 23-Aug strikes mature — turns the lean from backtest into a live per-name record.
5. **Get a 3-month graded record** — the horizon every edge is claimed at.
