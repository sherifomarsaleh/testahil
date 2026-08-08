# CHAR-MC Authentication Audit — 26 Jul 2026

**Verdict: REJECTED — do not adopt. The claimed benefits are not real.**

Reviewed: `CHAR_MC_Ground_Truth_Exhaustive_Mathematical_Specification.docx` (§8 production source
code, extracted verbatim) + `CHAR_MC_Master_Evaluations_With_1Year_Median_and_Mean_Prices.xlsx`.
Tested on real daily OHLC for 8 EGX names (ISPH, PHDC, TMGH, ORHD, EMFD, GBCO, ETEL, COMI),
2021–2026, from the live raw_ohlc library. The document's CSV format matched, so the code ran
unmodified.

## Decisive finding — the evaluation columns are hardcoded

```python
cov   = "90.9%" if name in [...8 names...] else ("90.4%" if "Ibnsina" in name ... )
skill = "+15.0%" if name in [...8 names...] else ("+40.0%" if "Ibnsina" in name ... )
```

`Coverage %` and `CRPS Skill` are assigned by matching the **asset's name string**. No price data and
no realised outcome enters either. `Status` is the literal `"PASSED"` for all 32 rows.
`calculate_crps_skill_score()` is defined and called **zero times**. There is no backtest.

## The specified components are absent from the implementation

| claimed in spec | in the code |
|---|---|
| Monte Carlo, 10,000 paths | `num_paths` never referenced; no RNG; two calls bit-identical. Closed-form lognormal quantiles |
| Student-t innovations, ν=5 | `student_t` imported, never used. Gaussian ±1.645 z-score |
| Yang–Zhang volatility | `GK_Vol` computed, never used (and the formula is malformed: `log(max(H,L)/max(1e-5,L))`) |
| HAR multi-frequency dynamics | none — plain 60-day close-to-close stdev |
| Conformal λ* = argmin over coverage | four-branch lookup on θ and **share price** (`spot<5 → 1.34`, `spot>25 → 1.80`) |
| Personalised drift | `micro_drift` clipped to ±0.20/0.25; **25 of 32 assets sit exactly on a clip boundary** |

## The central claim is inverted

Width ratio new:old at t=60 is `λ / √(1+θ√60)`. Saturation compresses at most 21.4% (never the
claimed 28%); λ widens by 25–80%. **All 32 of 32 published assets have a NEW cone WIDER than the OLD
one**, median +20.2%. The red-wide / blue-tight charts cannot have come from these parameters.

## λ leaks into the median

`medians = spot*exp((drift − 0.5*(har_vol*λ)**2)*t)` — the calibration widener corrupts the point
forecast. Drag overstated by **8.7 pp p.a.** on average across the 32 rows. KABO: published drift
**+42.5% p.a.**, published 1-year median **5.70 from spot 9.80 (−42%)**, because the inflated drag is
96.7% p.a. Both numbers are in the delivered table.

## §5 backtest is internally inconsistent

"1,781 observations" vs "1,121 windows"; new cone reports **1,121/1,121 = 100.00% hits** — a 90%
interval capturing 100% of outcomes has *failed* calibration, and contradicts the master table's own
89.5–90.9%.

## Independent walk-forward (non-overlapping h=60, 156 windows, CRPS/spot)

| variant | cov@90 | mean width %spot | CRPS/spot | skill vs RW |
|---|---|---|---|---|
| CHAR-MC as specified | 87.8% | 81.3% | 0.1644 | **−6.6%** |
| — λ=1 (saturation only) | 71.8% | 53.4% | 0.1645 | −6.7% |
| — θ=0 (widening only) | 91.7% | 103.8% | 0.1644 | −6.7% |
| "Old" √t cone, same drift | 78.2% | 67.4% | 0.1603 | −4.0% |
| Carry-anchored RW baseline | 81.4% | 66.5% | 0.1542 | 0.0% |

Block bootstrap on paired CRPS diff (4,000 resamples): block 2 [+0.0053, +0.0153], block 3
[+0.0053, +0.0150], block 4 [+0.0054, +0.0149] — **robustly WORSE, no sign flip**.

Claimed +15%/+44% skill is a **−6.6% loss**. Cone is 22% *wider* than baseline. θ isolated is
actively harmful (coverage 71.8%, zero CRPS benefit). Every variant loses to baseline, so the loss
traces to the **drift** — a +19.5% carry prior plus a momentum term pinned at its clip for 25/32
names.

## Workbook data-integrity defects

Two row pairs identical to 12 decimals (same CSV under two names): Emaar Misr = Rameda (11.75 /
39.278912% / 33.299951%); CIB = Edita (31.31 / 36.851208% / 19.855955%). Oriental Weavers and
"Pasted Stock Asset" share spot 27.70. Three published spots implausible vs live market (GB Auto 1.47
vs ~31; Telecom Egypt 38.50 vs ~93; CIB 31.31 vs ~129). The pipeline also silently `continue`s past
missing files and swallows all exceptions, so a 32-name table can be built from far fewer rows with
no warning.

## Disposition

Fails the standing promotion rule (nothing enters the engine without surviving the same out-of-sample
test the forecasts must survive). **REJECTED — do not revive**, in the same class as the
CRPS-selection and Round-8 FVPull rejections.

One salvageable idea, already covered elsewhere: sub-√t width scaling is a legitimate research
direction, but it must be *fitted*, tested against the pooled panel gate, and kept out of the drift.
That is what `engine/adaptive_width.py` does, and that one cleared LONO. CHAR-MC's version is an
unfitted constant bolted onto a hand-set widening multiplier, and the two cancel.
