# Market-wide MC cone re-strike — EG · AE · SA (28-Jul-2026) — **PUBLISHED**

Trigger (b), applied at market scale: 58 already-covered tickers, fresh 15-year libraries.
**Live on `main` at `29998a4`** (CI auto-regenerated `feed.xml` at `3f713e6`).

## 1. The finding that shapes everything else

**The calibration was already current. The published cones were not.**

Re-running the full 3-month panel fit on today's libraries reproduces the live profiles *exactly*:

| Market | Live (nu, width_cal) | Refit on current library | Band move | Market verdict |
|---|---|---|---|---|
| EG (30 names, 15.6 yr median) | 6.0 / 0.951 | 6.0 / 0.951 | **0.00%** | PASS |
| AE (18 names) | 10.0 / 0.979 | 10.0 / 0.979 | **0.00%** | PARITY |
| SA (11 names) | 12.0 / 1.07 | 12.0 / 1.07 | **0.00%** | PARITY |

So the 15-year history had already been absorbed into the engine on 27-Jul. What had *not* happened
is the part the reader actually sees: **all 58 published cones were still the old ones** — struck at
spot dates 1–19 Jul, under the superseded fits, on the retired session-counted T+20/T+60 convention.
Not one ticker carried the `hz` calendar marker. That gap is what this run closes.

Per-name verdicts also reproduce unchanged: EXTRA (SA) remains the system's one robust FAIL, LULU
stays PROVISIONAL(insufficient-windows), and EG's ISPH sits at BOUNDARY(PARITY-flagged).

## 2. Step 0.0 — data-quality gate, all 59 series

Clean. 100 rows dropped across the whole set, ~40 corporate-action repairs, and **no vendor
corruption of the kind that has bitten before**. Four names breach a naive density screen and all
four are genuine, not export damage:

- **DSCW** (148.8 rows/yr), **BTFH** (222.2), **LCSW** (218.5), **IHC** (184.6) — the shortfall is
  concentrated in 2011–2013 suspension blocks (IHC has a 159-session absence in 2012; DSCW a
  75-session one in 2013). Scattered illiquidity and real suspensions in small/controlled names,
  all of it *before* each market's adopted break cut, so none of it enters the calibration sample.

Two EG names exceed the EGX ±20% single-session limit and both are explained: **OCDI** at exactly
0.2231 (= ln(1.25), a clean limit-down) and **PHDC** at 0.2407 across a 3-day calendar gap, i.e. a
multi-session move, not one session.

A model-vs-realized volatility screen across all 59 names sits in a 0.77–1.22 band with one
exception: **LCSW at 1.90** (model 58.3% vs 252-day realized 30.7%). Its 63-day realized is 42.2%,
so the HAR is extrapolating a genuine recent vol spike — which is why LCSW is one of the few names
whose cone *widens*. Flagged, not suppressed.

## 3. Grading — nothing could be graded, and that is the correct answer

Eight cohorts show a stored `grade_date` on or before today. **None of them has actually matured.**

| Cohort | Anchor | Stored grade_date | Sessions since anchor | Needs | Short by |
|---|---|---|---|---|---|
| COMI (EG) | 29-Jun | 27-Jul | 16 | 20 | 4 |
| CCAP (EG) | 30-Jun | 28-Jul | 15 | 20 | 5 |
| ORAS (EG) | 30-Jun | 28-Jul | 15 | 20 | 5 |
| EMAAR (AE) | 29-Jun | 27-Jul | 19 | 20 | 1 |
| Kakao, LGES (KR) | 26-Jun | 24-Jul | 0 | 20 | 20 |
| TMPV (IN), TSLA (US) | 30-Jun | 28-Jul | 0 | 20 | 20 |

This is the stored-`grade_date` trap the protocol names explicitly: those dates are projected on a
holiday-blind weekmask, and EGX closures on 2-Jul and 23-Jul push the true T+20 four to five
sessions later than the stored target. Grading against the stored date would have marked four EGX
names on the wrong close. **No cohort was graded and no `realized_close` was written.**

Kakao, LGES, TMPV and TSLA still have *zero* post-anchor data — they are the same four names flagged
as un-postable on 27-Jul. They stay blocked until their OHLC is posted.

## 4. What was re-struck

58 cones, each anchored at **that name's own last clean close** — EG 22-Jul (LCSW 21-Jul, it did not
trade; OCDI/ORHD 27-Jul), AE 24-Jul, SA 26-Jul — through the production chain with no approximation:

> `clean_ohlc` → YZ variance proxy → `fit_har_v3` → `har_forecast_v3` →
> carry `ln(1+rf_live) − ln(1+q)` → `simulate_paths_v3`, 50,000 paths, seed 42, signal OFF everywhere.

Horizons come from `horizons.resolve()` on each exchange's own realized calendar — h = 20–22 sessions
at 1M and 61–63 at 3M — never a hard-coded 20/60. Every ticker now carries `hz{h1,h3,cal:true}`.

**The adaptive per-stock width overlay is NOT in this.** `engine/adaptive_width.py` is still absent
from `main` — the PR has not merged — so every cone here uses the flat market-level `width_cal`,
exactly as production does today.

### The headline: the bands got narrower

| Market | n | Median 1M width Δ | Median 3M width Δ | Median \|Δspot\| |
|---|---|---|---|---|
| EG | 30 | **−12.8%** | −3.2% | 3.6% |
| AE | 17 | **−11.1%** | −2.1% | 4.5% |
| SA | 11 | **−8.2%** | −6.8% | 1.1% |
| **All** | **58** | **−11.1%** | −3.3% | 2.7% |

**46 of 58 cones narrow.** The largest: IHC −62.6%, COMI −49.2%, ENBD −43.5%, HRHO −39.5%,
ABUK −38.6%, EMAAR −38.5%, RAYA −38.4%.

**CORRECTION (28-Jul-2026, same day): the causal claim first published here was wrong.**
The original text said the narrowing came from the libraries going ~5yr → ~15yr, letting the HAR
train on 3× the data and stop over-forecasting vol. That was asserted, not tested. Tested, it fails.

Holding code, fit, anchor date and horizon fixed and changing **only** library depth (pre-ingest
~5.5yr vendor file vs today's ~15.5yr file, both truncated to the same anchor bar), the longer
history mostly *widens* the cone:

| | COMI | PHDC | ENBD | EMAAR | SABIC | ABUK | HRHO | ISPH | IHC |
|---|---|---|---|---|---|---|---|---|---|
| 1M half-width Δ | +14.8% | +14.5% | +13.0% | +5.4% | +4.1% | +1.2% | +0.3% | 0.0% | **−11.3%** |

IHC is the single exception. So history is not the mechanism.

**What actually drove it: the published cones were a patchwork of engine vintages.** Testing whether
each old cone is what today's chain produces *at its own anchor under the fit that was live then*:

| | COMI | ABUK | HRHO | IHC | ENBD | SABIC | EMAAR | EXTRA | PHDC | ISPH | ALINMA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| implied ann. vol | 53.2% | 65.0% | 53.8% | 23.8% | 56.2% | 27.8% | 41.5% | 29.3% | 36.8% | 37.0% | 17.5% |
| chain ann. vol | 25.2% | 38.0% | 32.6% | 12.9% | 35.1% | 18.8% | 33.0% | 24.1% | 38.6% | 40.0% | 18.7% |
| ratio | **2.11×** | **1.71×** | **1.65×** | **1.85×** | **1.60×** | 1.48× | 1.26× | 1.22× | 0.95× | 0.93× | 0.94× |

The split is clean. Names last struck through the current `mc_v3` chain — PHDC, ISPH, ALINMA — sit at
0.93–0.95× and barely moved in the re-strike (PHDC and ISPH in fact *widened*, tracking EG's fit
change of +10.1%). Names carrying cones published earlier alongside their valuation studies (COMI on
29-Jun, ABUK, HRHO, IHC, ENBD) implied **1.6–2.1× the volatility the engine estimates** and are
where the whole median narrowing comes from.

So the honest description of this run is **normalization, not improvement**: it puts all 58 names on
one engine at one moment. The bands are narrower because the legacy ones were too wide for the
engine that is supposed to be producing them — a site-consistency defect, now closed. It does
partially answer the "bands are too broad" complaint, but by fixing stale published output, not by
making the model sharper.

### What happened to the median

Two different things, and they are worth separating.

**In absolute terms the median moved with spot** — that is re-anchoring, not a view. COMI's 1M median
went 128.87 → 142.09, but its spot went 129.25 → 140.00 over the same three weeks.

**As a multiple of spot, the median barely moved — and that is by design.** With the signal OFF
everywhere, the median of the terminal distribution is exactly `spot × exp(carry drift)`; width does
not touch it. Median p50/spot:

| Market | 1M before | 1M after | 3M before | 3M after |
|---|---|---|---|---|
| EG | +1.419% | +1.491% | +4.359% | +4.706% |
| AE | +0.179% | +0.282% | +0.573% | +0.965% |
| SA | +0.103% | +0.301% | +0.000% | +1.072% |

The small lift is purely the horizon convention: the old cones applied the annual carry over a
session proxy (20/252 = 0.0794 yr), the new ones over an exact calendar fraction (1/12 = 0.0833 yr) —
about 5% more time, so about 5% more drift. On EG's 19.50% carry that is +0.07pp at 1M and +0.35pp
at 3M. Nothing about direction changed.

**The real change is that the spread of the median collapsed.**

| Market | 1M p50/spot range before | after |
|---|---|---|
| EG | −0.67% … +4.63% | +1.361% … +1.618% |
| AE | −0.46% … +2.38% | +0.000% … +0.375% |
| SA | −0.29% … +0.68% | +0.285% … +0.310% |

Eleven names previously carried a **negative** median drift — BTFH and HRHO at −0.67%, FAB −0.46%,
ABUK −0.40%, COMI −0.29% — i.e. a published directional view that the carry anchor does not sanction.
Every name is now pinned to its market's carry, and the residual spread inside each market is
Monte-Carlo noise on 50k paths plus 2-decimal rounding, nothing more. This is the retired
secular-drift / trend-drift machinery finally cleared out of published output.

Twelve cones **widen**, and they are worth reading rather than waving through: ISPH +22.9%,
LCSW +20.2%, PHDC +10.3%, ADCB +9.0%. LCSW and ISPH are the two genuine recent-vol-spike names;
widening there is the model working, not failing.

## 5. Left alone, deliberately

`fair{bear,base,full}` (separate clock — needs a real study refresh, not a price roll-forward) ·
the interactive slider's bespoke factor-stack constants (`CONT_FIXED`/`EV_FIXED`/`GEO_MEAN` — fitted
to the fundamental driver stack, not the carry-anchored engine) · technical S/R `levels` and the
`tech` narrative (need a fresh chart read) · `files` · `market_profiles.py`, `fitted_configs.json`
and `panel_hashes.json` (all three byte-identical — this is a data change, not an engine change) ·
the five-year quarterly backtest PNGs (a coarse 20-quarter replay that one new cohort does not move;
**a regen is not warranted here**) · METALS/KR/IN/US/QA tickers, all 13 untouched.

Touch ladders were recomputed at the **same absolute levels already on each page**, never re-picked.

## 6. QC gate

| Item | Evidence |
|---|---|
| Step 0.0 passed | 59/59 series through `clean_ohlc` with per-market limits; 4 density outliers diagnosed as genuine suspensions, 2 limit-breaches explained |
| Step 0 / calibration current | Full-panel 3m refit reproduces live profiles at 0.00% band move in all three markets |
| Materiality gate | No fit changed, so no gate trip; the change is to published cones only |
| Verify by IMPORT, not parse | 11 modules imported cleanly incl. `market_profiles`, `mc_v3`, `horizons`, `panel_refresh`, `research_protocol`, `wacc_builder` |
| Production chain, no approximation | Re-running `strike()` reproduces the written percentiles bit-for-bit on 5 spot-checked names across all 3 markets |
| Cell-by-cell diff vs delivered file | 58 tickers changed; **only** `spot`/`spotDate`/`dist`/`touch`/`hz` differ — zero disallowed field changes; 13 out-of-scope tickers byte-identical |
| Ledger append-only | First 162 rows byte-identical; 116 appended (58 × 2 horizons), none pre-realized |
| Touch levels preserved | 0 of 58 ladders had their level set changed |
| Page integrity | `scripts/check_page_integrity.py` clean — 0 hard findings, incl. cache-buster-drift |
| Cache-buster bumped in the same change | 90 references across 87 files → `v=20260728a` |

## 7. Needs your decision / still open

1. **Three touch ladders now sit entirely on one side of spot** and want a human re-pick, not a
   recompute: **PHDC** (spot 15.01, all levels 15.55–20.00 above), **EMFD** (11.75, all above),
   **HELI** (8.27 after a +28.6% move, all levels below). The probabilities are correct at those
   levels; the level *sets* are stale.
2. **`q_annual = 0` everywhere, flagged.** House convention, consistent with every existing cohort —
   but it is a real bias: the drift is a gross-of-dividend price carry and overstates the centre by
   roughly the yield. On GCC banks yielding 5–6% that is not negligible over a 3-month horizon.
   Worth sourcing properly rather than carrying forward by inertia.
3. **OCDI and ORHD were re-struck at an unchanged anchor** (27-Jul), so they enter as cycle 3 with
   `reanchor_from` equal to their own `anchor_date`. Nothing was re-anchored — only the convention
   and fit changed. Annotated explicitly in the ledger note rather than left to look like an error.
4. **Four cohorts remain ungradeable for want of data** — Kakao, LGES (KR), TMPV (IN), TSLA (US).
   Post the OHLC and they grade and roll the same way.
5. The engine's per-origin vol estimation is **still not break-aware** — the HAR trains across the
   AE Jan-2022 workweek switch and EG's devaluation steps even though the *calibration sample* is
   correctly break-filtered. Unchanged by this run, but the longer libraries make it more material
   than it was, since there is now far more pre-break history to train on.

## 8. Per-name detail

| Mkt | Ticker | Anchor | Spot old → new | 1M cone (p5–p95) | 1M half-width | 3M half-width | h 1M/3M |
|---|---|---|---|---|---|---|---|
| AE | ADCB | 24 Jul 2026 | 15.10 → 14.42 | 12.55 – 16.63 | 13.0% → 14.1% (+9.0%) | 22.6% → 25.4% (+12.4%) | 20/63 |
| AE | ADIBUAE | 24 Jul 2026 | 21.76 → 21.24 | 18.50 – 24.47 | 13.9% → 14.1% (+1.3%) | 24.4% → 25.4% (+4.4%) | 20/63 |
| AE | ADNOCGAS | 24 Jul 2026 | 3.44 → 3.34 | 3.08 – 3.64 | 11.8% → 8.4% (-28.8%) | 20.1% → 16.2% (-19.4%) | 20/63 |
| AE | AGTHIA | 24 Jul 2026 | 3.51 → 3.20 | 2.86 – 3.59 | 12.0% → 11.4% (-4.7%) | 20.8% → 22.2% (+6.7%) | 20/63 |
| AE | ALDAR | 24 Jul 2026 | 8.30 → 7.61 | 6.64 – 8.75 | 17.4% → 13.9% (-20.4%) | 29.7% → 26.3% (-11.5%) | 20/63 |
| AE | ALPHADHABI | 24 Jul 2026 | 8.22 → 7.30 | 6.35 – 8.42 | 16.0% → 14.2% (-11.4%) | 28.2% → 26.6% (-5.6%) | 20/63 |
| AE | BURJEEL | 24 Jul 2026 | 1.11 → 1.20 | 1.03 – 1.41 | 16.7% → 15.8% (-5.0%) | 29.3% → 29.2% (-0.4%) | 20/63 |
| AE | DEWA | 24 Jul 2026 | 2.79 → 2.67 | 2.41 – 2.97 | 10.8% → 10.5% (-2.6%) | 19.0% → 18.9% (-0.2%) | 20/63 |
| AE | DIB | 24 Jul 2026 | 7.72 → 7.35 | 6.65 – 8.16 | 10.2% → 10.3% (+0.4%) | 17.6% → 19.5% (+10.4%) | 20/63 |
| AE | EAND | 24 Jul 2026 | 19.66 → 20.08 | 18.20 – 22.25 | 10.1% → 10.1% (-0.1%) | 17.5% → 18.1% (+3.0%) | 20/63 |
| AE | EMAAR | 24 Jul 2026 | 12.14 → 11.08 | 9.82 – 12.56 | 20.1% → 12.4% (-38.5%) | 35.7% → 24.0% (-32.8%) | 20/63 |
| AE | EMAARDEV | 24 Jul 2026 | 14.26 → 13.16 | 11.46 – 15.16 | 16.7% → 14.1% (-15.8%) | 30.6% → 27.5% (-10.1%) | 20/63 |
| AE | ENBD | 24 Jul 2026 | 30.64 → 30.22 | 25.93 – 35.34 | 27.6% → 15.6% (-43.5%) | 37.4% → 28.7% (-23.2%) | 20/63 |
| AE | FAB | 24 Jul 2026 | 17.40 → 18.66 | 16.48 – 21.20 | 13.7% → 12.6% (-7.9%) | 23.2% → 22.9% (-1.3%) | 20/63 |
| AE | IHC | 24 Jul 2026 | 382.30 → 380.00 | 365.12 – 397.56 | 11.4% → 4.3% (-62.6%) | 18.3% → 9.6% (-47.5%) | 20/63 |
| AE | LULU | 24 Jul 2026 | 0.94 → 0.96 | 0.84 – 1.10 | 16.0% → 13.5% (-15.1%) | 27.1% → 26.6% (-2.1%) | 20/63 |
| AE | SALIK | 24 Jul 2026 | 5.70 → 5.47 | 4.83 – 6.22 | 14.3% → 12.7% (-11.1%) | 25.6% → 24.6% (-4.0%) | 20/63 |
| EG | ABUK | 22 Jul 2026 | 67.97 → 72.30 | 62.48 – 86.21 | 26.7% → 16.4% (-38.6%) | 46.6% → 31.5% (-32.4%) | 20/61 |
| EG | ADIB | 22 Jul 2026 | 46.64 → 49.30 | 42.43 – 59.02 | 22.7% → 16.8% (-26.0%) | 41.9% → 33.8% (-19.4%) | 20/61 |
| EG | BTFH | 22 Jul 2026 | 2.97 → 3.09 | 2.70 – 3.64 | 20.0% → 15.2% (-24.1%) | 33.7% → 30.1% (-10.6%) | 20/61 |
| EG | CCAP | 22 Jul 2026 | 4.77 → 5.51 | 4.56 – 6.87 | 24.7% → 21.0% (-15.1%) | 43.7% → 39.4% (-9.8%) | 20/61 |
| EG | CLHO | 22 Jul 2026 | 16.31 → 16.90 | 13.75 – 21.41 | 25.8% → 22.7% (-12.2%) | 35.9% → 42.2% (+17.4%) | 20/61 |
| EG | COMI | 22 Jul 2026 | 129.25 → 140.00 | 127.41 – 158.50 | 21.8% → 11.1% (-49.2%) | 37.7% → 21.5% (-43.0%) | 20/61 |
| EG | DSCW | 22 Jul 2026 | 1.94 → 1.96 | 1.70 – 2.33 | 17.8% → 16.1% (-9.6%) | 31.7% → 32.9% (+3.8%) | 20/61 |
| EG | EFID | 22 Jul 2026 | 27.34 → 27.70 | 23.72 – 33.33 | 20.5% → 17.3% (-15.4%) | 35.8% → 35.2% (-1.7%) | 20/61 |
| EG | EFIH | 22 Jul 2026 | 20.74 → 23.39 | 20.06 – 28.10 | 22.6% → 17.2% (-23.8%) | 39.7% → 33.7% (-15.3%) | 20/61 |
| EG | EGAL | 22 Jul 2026 | 285.88 → 301.12 | 263.16 – 355.02 | 20.6% → 15.3% (-25.8%) | 38.5% → 33.0% (-14.3%) | 20/61 |
| EG | EMFD | 22 Jul 2026 | 11.70 → 11.75 | 10.36 – 13.74 | 15.4% → 14.4% (-6.5%) | 27.3% → 28.8% (+5.5%) | 20/61 |
| EG | ETEL | 22 Jul 2026 | 92.61 → 103.28 | 88.52 – 124.16 | 19.3% → 17.3% (-10.7%) | 36.6% → 31.7% (-13.4%) | 20/61 |
| EG | FWRY | 22 Jul 2026 | 18.40 → 19.30 | 16.96 – 22.64 | 19.3% → 14.7% (-23.8%) | 34.2% → 30.8% (-10.0%) | 20/61 |
| EG | GBCO | 22 Jul 2026 | 31.25 → 31.31 | 25.55 – 39.54 | 23.1% → 22.3% (-3.3%) | 43.4% → 42.3% (-2.6%) | 20/61 |
| EG | HELI | 22 Jul 2026 | 6.43 → 8.27 | 7.12 – 9.89 | 19.6% → 16.7% (-14.5%) | 34.4% → 32.5% (-5.8%) | 20/61 |
| EG | HRHO | 22 Jul 2026 | 26.83 → 26.95 | 24.01 – 31.16 | 21.9% → 13.3% (-39.5%) | 37.0% → 25.1% (-32.2%) | 20/61 |
| EG | ISPH | 22 Jul 2026 | 11.67 → 11.73 | 10.01 – 14.16 | 14.4% → 17.7% (+22.9%) | 25.2% → 34.2% (+35.6%) | 20/61 |
| EG | JUFO | 22 Jul 2026 | 29.99 → 28.90 | 24.68 – 34.87 | 16.9% → 17.6% (+4.6%) | 30.8% → 34.2% (+11.0%) | 20/61 |
| EG | KABO | 22 Jul 2026 | 7.00 → 8.80 | 7.29 – 10.95 | 23.9% → 20.8% (-12.8%) | 42.1% → 40.7% (-3.2%) | 20/61 |
| EG | LCSW | 21 Jul 2026 | 29.45 → 33.83 | 26.69 – 44.21 | 21.5% → 25.9% (+20.2%) | 38.5% → 46.4% (+20.6%) | 21/61 |
| EG | OCDI | 27 Jul 2026 | 27.48 → 27.48 | 22.80 – 34.14 | 19.3% → 20.6% (+6.9%) | 36.2% → 38.3% (+5.8%) | 21/62 |
| EG | OIH | 22 Jul 2026 | 1.41 → 1.47 | 1.28 – 1.74 | 22.0% → 15.6% (-28.8%) | 40.4% → 31.0% (-23.4%) | 20/61 |
| EG | ORAS | 22 Jul 2026 | 720.00 → 713.50 | 626.04 – 837.88 | 22.1% → 14.8% (-32.8%) | 38.3% → 29.8% (-22.3%) | 20/61 |
| EG | ORHD | 27 Jul 2026 | 40.16 → 40.16 | 34.82 – 47.74 | 15.0% → 16.1% (+7.3%) | 30.2% → 32.0% (+5.9%) | 21/62 |
| EG | ORWE | 22 Jul 2026 | 22.34 → 23.12 | 21.01 – 26.21 | 12.9% → 11.2% (-12.8%) | 22.5% → 23.2% (+2.9%) | 20/61 |
| EG | PHDC | 22 Jul 2026 | 14.84 → 15.01 | 12.89 – 18.01 | 15.5% → 17.1% (+10.3%) | 27.4% → 32.9% (+19.9%) | 20/61 |
| EG | PRDC | 22 Jul 2026 | 8.28 → 9.80 | 7.84 – 12.62 | 24.5% → 24.4% (-0.3%) | 44.1% → 40.5% (-8.3%) | 20/61 |
| EG | RAYA | 22 Jul 2026 | 7.70 → 7.76 | 6.53 – 9.51 | 31.2% → 19.2% (-38.4%) | 54.9% → 37.1% (-32.4%) | 20/61 |
| EG | RMDA | 22 Jul 2026 | 5.00 → 4.98 | 4.39 – 5.82 | 16.3% → 14.4% (-11.9%) | 28.9% → 31.0% (+7.4%) | 20/61 |
| EG | TMGH | 22 Jul 2026 | 99.88 → 100.50 | 88.26 – 117.92 | 13.8% → 14.8% (+6.7%) | 24.5% → 28.0% (+14.2%) | 20/61 |
| SA | ACWA | 26 Jul 2026 | 193.90 → 191.20 | 161.06 – 228.76 | 19.8% → 17.7% (-10.5%) | 33.9% → 31.6% (-6.8%) | 22/62 |
| SA | ALINMA | 26 Jul 2026 | 24.00 → 23.80 | 21.87 – 26.09 | 8.3% → 8.9% (+6.7%) | 14.5% → 17.1% (+18.0%) | 22/62 |
| SA | ALRAJHI | 26 Jul 2026 | 66.00 → 64.50 | 58.58 – 71.54 | 10.9% → 10.0% (-8.2%) | 18.5% → 18.4% (-0.8%) | 22/62 |
| SA | ARAMCO | 26 Jul 2026 | 26.24 → 26.60 | 24.68 – 28.87 | 9.1% → 7.9% (-13.3%) | 15.9% → 13.5% (-15.2%) | 22/62 |
| SA | ELM | 26 Jul 2026 | 658.50 → 666.00 | 557.58 – 801.78 | 19.7% → 18.3% (-7.1%) | 35.2% → 30.4% (-13.7%) | 22/62 |
| SA | EXTRA | 26 Jul 2026 | 68.10 → 68.50 | 61.75 – 76.54 | 14.0% → 10.8% (-22.6%) | 24.2% → 21.1% (-12.8%) | 22/62 |
| SA | MAADEN | 26 Jul 2026 | 58.80 → 58.20 | 50.75 – 67.25 | 15.6% → 14.2% (-9.4%) | 27.5% → 25.4% (-7.5%) | 22/62 |
| SA | RIBL | 26 Jul 2026 | 20.23 → 20.92 | 19.08 – 23.11 | 10.3% → 9.6% (-6.3%) | 17.9% → 17.2% (-3.8%) | 22/62 |
| SA | SABIC | 26 Jul 2026 | 51.80 → 52.25 | 47.72 – 57.62 | 13.2% → 9.5% (-28.0%) | 22.2% → 17.5% (-21.0%) | 22/62 |
| SA | SNB | 26 Jul 2026 | 38.96 → 39.92 | 35.32 – 45.45 | 13.7% → 12.7% (-7.5%) | 22.9% → 22.8% (-0.4%) | 22/62 |
| SA | STC | 26 Jul 2026 | 43.58 → 43.10 | 40.36 – 46.35 | 6.9% → 6.9% (+0.6%) | 12.1% → 13.3% (+10.3%) | 22/62 |

## 9. Publish record

| commit | what |
|---|---|
| `29998a4` | the re-strike — `assets/data.js` (58 cones + 116 ledger rows), 87 HTML cache-buster bumps to `v=20260728a`, and the two new build scripts |
| `3f713e6` | CI auto-regenerated `feed.xml` from the new `data.js` |

Rebased onto `99881c6` (a trade/portfolio picker commit that landed mid-session) before pushing —
clean, no conflict: that commit changed picker JS, this one changed only the cache-buster line in
the same two files. Verified after rebase that both survived.

PAT injected as an authenticated URL for the push only and never written to `.git/config`
(pushed straight to the URL rather than via `git remote set-url`, so the token never touched the
repo at all); remote confirmed tokenless afterwards, and `grep -r github_pat .git/` is empty.

`engine/strike_*.json` and `engine/rollforward_ledger.json` were deliberately **not** committed —
~220 KB of intermediates fully regenerable from `strike_cohorts.py`, which is deterministic at
seed 42 and was verified bit-for-bit against the delivered file on five names.

Verified live on `main` via `raw.githubusercontent.com`: `SITE.updated = 2026-07-28`, 278 ledger
rows (162 + 116), 58 entries carrying `hz`, and PHDC/IHC/ALRAJHI percentiles matching the
delivered file exactly. The `testahil.com` and `github.io` domains are outside this sandbox's
network allowlist, so **the final CDN-served check was not run from here** — worth loading a
ticker page once to confirm the cache-buster took.

---

*Published 28-Jul-2026.*
