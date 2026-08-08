# Equation Lab — Round 8: Fair-Value-Pull Drift + Shadow Cohort #1 (23-Jul-2026)

**Trigger:** Sherif's approval ("OK") of the Round 7 recommendation — stop torturing price data and anchor each stock's drift to its own fair value. **This is the first drift candidate in eight rounds that is not derived from the price series it is trying to forecast.**

**Headline: the data to do this already exists, for the whole panel.** All 30 EGX names carry published fair-value bands (`assets/data.js` `fair{bear,base,full}`), each from a dated study (09-Jun-2026 PHDC/TMGH through 20-Jul-2026 DSCW). Coverage is not the bottleneck I expected — it is complete. What is impossible is a *retroactive* backtest, and this round refuses to fake one. Instead it (A) attempted the only legitimate retrospective check, (B) built the live prototype, and (C) **started the forward out-of-sample clock: Shadow Cohort #1 is generated and on file.**

Lab-only throughout. Scripts: `claude/v4_lab/lab_round8_fvpull.py`, `lab_round8_shadow_cohort.py`; ledger: `claude/v4_lab/shadow_cohort_20260723.json`.

---

## Why no backtest, stated once and plainly

Every published FV postdates every DEV origin *and* every FINAL origin. Worse, several lenses inside each FV (relative multiples, MC-median lenses) reference the market price at study date, so the FV is not even fully exogenous at publication. Reconstructing "historical fair values" from memory of what a study *would* have said is exactly the look-ahead sin Round 7 just caught in the ERP snapshot — 80% of that "win" evaporated when dated properly. Criterion C (beat the dumb yardstick) therefore **cannot be scored today** for this candidate; anyone who claims otherwise is overfitting. The shadow ledger below is the C-test, run in forward time — the same out-of-sample bar as the standing promotion rule, honestly ordered.

## A. The natural experiment — attempted, found not yet runnable

Design: each study was published, then prices moved; did `ln(FV_base/spot_at_publication)` predict the subsequent move, net of EGX30? Finding: **the raw_ohlc library itself ends at (roughly) each name's study date** — 27 of 30 names have *zero* post-publication sessions on file. The three that do: PHDC (gap +5.3% → move −1.9% ex-index, 26 sessions), TMGH (+42.9% → +3.8%, 26), EMFD (+46.7% → −6.0%, 20). n=3, one overlapping month, one shared market factor — unreadable, and reported as such rather than aggregated into a fake statistic. Side-finding worth recording: **PHDC's +75% Feb–May rally happened *before* its 09-Jun study** — the study was published near the top with FV≈spot (+5%), so PHDC is *not* evidence the FV work predicts rallies; it is evidence the FV work marked a finished rally as roughly fairly priced (which its subsequent −1.5% drift is consistent with).

## B. The prototype — per-name, signed, individual centers (first time in the lab)

Construction (Ornstein-Uhlenbeck-style convergence, base half-life 1.5yr = 375 sessions):

```
pull_i  = (1 − exp(−ln2 × 60/375)) × ln(FV_base,i / spot_i)     # 10.5% of the log-gap per 60 sessions
drift_i = carry + clip(pull_i, ±1.0 × σ60,i)                     # capped at the name's own cone width
```

T+60 centers today (carry-only gives every name the identical +4.24%):

| | gap to FV | pull/60d | total center | reading |
|---|---|---|---|---|
| EMFD | +52.8% | +5.54% | **+9.79%** | deepest discount, strongest pull up |
| ISPH | +42.1% | +4.42% | +8.66% | |
| TMGH | +38.7% | +4.07% | +8.31% | |
| ORHD | +31.4% | +3.29% | +7.54% | |
| **PHDC** | **+6.8%** | **+0.72%** | **+4.96%** | mild premium — the rally already converged to FV |
| HRHO | +3.2% | +0.33% | +4.58% | ≈ carry |
| PRDC | −0.6% | −0.06% | +4.18% | ≈ carry |
| **ORWE** | **−6.7%** | **−0.70%** | **+3.54%** | below carry — no premium, mildly rich |
| FWRY | −22.5% | −2.36% | +1.88% | |
| RAYA | −32.6% | −3.42% | +0.82% | |
| CLHO | −57.1% | −6.00% | −1.76% | negative center |
| DSCW | −79.1% | −8.30% | −4.06% | |
| KABO | −107.5% | −11.28% | **−7.04%** | steepest overvaluation, strongest pull down |

(Full 30-name table in `/tmp/lab_round8_proto.csv` and the shadow JSON.) This is, for the first time, exactly the shape of Sherif's ask: **ORWE sits below the uniform carry (no premium), PHDC sits modestly above it, genuinely overvalued names get negative centers, and the spread — −7.0% to +9.8% per 60 sessions — comes from fundamental information, not from re-slicing the price series.** Zero of 30 pulls hit the 1σ cap (KABO's −11.3% is inside its own 24.4% σ60), so the cone shape and width — the already-calibrated part — are untouched and criterion D is not mechanically threatened; whether it survives *empirically* is what grading measures.

## C. Shadow Cohort #1 — generated, the clock is running

`shadow_cohort_20260723.json`: for each of the 30 names, from its latest library close (anchors 23-Jun..19-Jul, per-name staleness recorded), **two full T+60 distributions from the actual production chain** (fit_har_v3 → har_forecast_v3 → carry_log_h → simulate_terminal_v3, live ν=4.0/width_cal=0.972, seed 42, 50k paths, p5–p95 to 2dp): one at the production carry drift, one at the shadow FV-pull drift. Same anchor, same shape, same seed — paired by construction, so grading deltas are clean of MC noise (the shared-seed discipline this session validated).

**Grading & promotion protocol (the C-test, forward):**
1. When each name's actual T+60 session arrives (count trading rows from anchor, per the standing grading rule — not calendar), fill `realized_close` and score both rows: CRPS (log-space), hit/miss per band, PIT.
2. One cohort = 30 names sharing one macro period = effectively **one observation** of the market factor. No promotion verdict from a single cohort, however good it looks.
3. Accumulate ≥3 non-overlapping cohorts (roll a new shadow cohort at each subsequent panel refresh, ~quarterly cadence → verdict circa Q2-2027; faster if refreshes are monthly). Paired ΔCRPS bootstrap CI **blocked by cohort** must favor FV-pull, AND shadow cov90 ∈ [88%, 92%] (criterion D as a hard gate), AND no single name contributes >25% of the pooled delta (the scale-normalization lesson).
4. Only then a production PR. Until then: shadow rows never touch ticker pages, the live site, or the engine.

## Scoring against the four criteria

**A (mimic real life):** yes in design — the center now points where the fundamental work says the business is worth, up when cheap, down when rich, flat when fair; this is how a human analyst actually centers expectations. **B (individuality — cone, drift, return):** fully met in construction, for the first time: per-name width (already), per-name signed drift (new), per-name outcome spread (follows). **C (dumb yardstick):** unknowable today, by honest necessity; the shadow ledger is the test and it has started. **D (cov90 88–92 ±2):** structurally protected (shape untouched, pull capped ≪ σ for 29/30 names) and explicitly a hard gate in the promotion rule, graded not assumed.

## Caveats, on the record

The deep-discount tail (KABO −66%, DSCW −55%, OIH, RMDA, CLHO) is exactly where the studies *themselves* say the market is pricing a regime the DCF can't see (CLHO: takeout/per-bed re-rating; RMDA: rate-normalization bet). If those names dominate early grading, the right read may be "shrink the pull where the study flags a non-DCF regime," not "the idea failed" — flagged now so it isn't invented later as an excuse. FV staleness (studies age; a stale FV pulls toward an old number — propose: fall back to carry when FV age >120 sessions, ages recorded per name). Half-life 1.5yr is a judgment anchor (from the ISPH integration's own 2–3yr convergence finding), not a fitted parameter — deliberately NOT fitted, to keep zero tuned knobs ahead of the out-of-sample window; 1yr/2yr sensitivities logged in the prototype table.

## Standing conclusion

Rounds 0–7 established that ~5.5 years of EGX prices cannot supply a per-name drift — every price-derived statistic failed the same gate. Round 8 changes the *input*, not the statistic: the drift now comes from the project's own fundamental layer, which is the one source of per-name, signed, forward-looking information this platform actually produces. It cannot be validated retroactively, so it is being validated the only honest way — publicly-reproducible shadow forecasts, graded on future data, under the same promotion rule as everything else in the engine. First grading window closes ~mid-October 2026.
