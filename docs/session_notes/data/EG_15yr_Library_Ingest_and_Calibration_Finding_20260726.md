# EG 15-year library — ingest, data-quality gate, and what the extra history actually buys
**26 Jul 2026 · library COMPLETE (32 series, 97,756 cleaned sessions)**

> **CORRECTION (same day).** An earlier version of this doc reported that longer-history
> calibration BEAT the adopted post-2022-03-21 break cut, robustly across bootstrap blocks. That was
> a **26-name** result and it **did not survive** adding COMI, KABO, OIH and PRDC. On the full
> 30-name equity panel the comparison is **PARITY at every block size**. The break filter stands.
> The earlier claim should not be cited.

## Headline

1. **Calibration sample: PARITY. Do not change the break cut.**
2. **The real payoff is `adaptive_width.py`.** Its MIN_WINDOWS=28 history gate went from **0 / 30**
   names clearing it to **26 / 30**. The overlay has been adopted-but-dormant purely for want of
   history. This library ends that.

## Ingest

32 series, all received. Median history **15.6 yrs** (was 5.5), 17 names ≥14 yrs, **97,756** cleaned
sessions (was ~35,000).

## Step 0.0 gate — 827 rows removed, three real problems

Post-gate every series tops out at ≤0.241 |log move|, consistent with the EGX ±20% daily limit.
Pre-gate, six names carried impossible jumps — all pre-listing placeholder rows at the IPO boundary:

| name | placeholder jump | date |
|---|---|---|
| HELI | 0.330 → 12.080 (+360%) | 2012-02-07 |
| EFIH | 0.500 → 13.980 (+333%) | 2021-10-19 |
| RMDA | 0.190 → 3.580 (+294%) | 2019-12-09 |
| CLHO | 0.070 → 1.280 (+291%) | 2016-06-01 |
| BTFH | 4.638 → 16.390 (+126%) | 2016-03-24 |
| DSCW | 0.281 → 0.929 (+120%) | 2017-11-14 |

ABUK additionally carried **13 zero/negative prices** (an `inf` log return) absent from the short file.

**Two standing flags:**

1. **EGX70 gains nothing from this upload.** `High == Low` on **100% of pre-2019 rows** — no intraday
   range, so no Yang-Zhang variance exists. Gate dropped 748 of 2,317 rows; usable history starts
   **2020-01-20 (6.5 yrs)**, shorter than the equities. Any "EGX70 has 15 years" claim is false.
2. **RAYA has flat High==Low on 34.6% of sessions.** A third of its history has zero intraday range.
   This depresses its YZ proxy and narrows its cone. Needs a decision before it enters a fit.
   (Next worst: LCSW 9.4%, EFID 9.0%, ABUK 8.7%, BTFH 8.1%.)

Note PRDC and EFIH are genuinely short (4.8 yrs each — recent listings, no 15-year history exists).

## Calibration-sample test — PARITY

Only the calibration sample varies. Identical scoring windows (post-2022-03-21, non-overlapping
h=60, **492 windows, 30 equities**), LONO cross-fitted, scored against the carry-anchored
trailing-252d RW null. Production chain throughout. Incremental expanding-window HAR **verified
against `fit_har_v3` at five origins: max |Δβ| = 1.5e-12, max |Δs²| = 1.5e-13.**

| arm | ν | width_cal | cov90 | width | CRPS skill |
|---|---|---|---|---|---|
| A LONG (2011+) | 5.90 | 0.911 | 0.9004 | 0.783 | +0.0158 |
| C MID (≥2016 float) | 5.76 | 0.911 | 0.8984 | 0.780 | +0.0155 |
| B CURRENT (≥2022-03-21) | 5.07 | 0.933 | 0.9045 | 0.790 | +0.0157 |

| comparison | mean CRPS diff | block 2 | block 3 | block 4 |
|---|---|---|---|---|
| LONG vs CURRENT | −0.000024 | [−7.4e−5, +2.7e−5] | [−7.5e−5, +2.5e−5] | [−7.4e−5, +2.5e−5] |
| MID vs CURRENT | +0.000020 | [−3.2e−5, +7.1e−5] | [−3.2e−5, +6.8e−5] | [−2.7e−5, +6.8e−5] |

**No significant difference at any block size.** LONG wins on 18/29 names, loses on 11 — two of the
three names that broke the earlier result (KABO, OIH) were among the worst. Under the standing gate,
PARITY → do not adopt. **The 2022-03-21 break cut stays.**

Methodological note for the ledger: the earlier 26-name result was a panel-composition artifact.
Three names (~10% of the panel, ~10% of windows) flipped a "robust across blocks {2,3,4}" verdict to
parity. Block-bootstrap robustness does **not** imply robustness to panel composition — the two
should be checked separately before anything is reported as a finding.

## What the history DOES buy — the adaptive_width gate

`adaptive_width.py` (EG-only, adopted 23-Jul-2026) is history-gated at MIN_WINDOWS=28 resolved 60-day
windows and is **dormant in production** because no EG name had enough history.

| | names clearing MIN_WINDOWS=28 |
|---|---|
| 2021-start library | **0 / 30** (max 22 windows) |
| this library | **26 / 30** |

19 names now carry 52–58 resolved windows against a gate of 28. Only **FWRY (23), RMDA (22),
EFIH (14), PRDC (14)** remain below.

This is the direct remedy for the per-name calibration spread measured on the live engine: 8 names
below the 88% coverage floor, 4 above 92%, because one pooled width multiplier cannot fit names whose
own volatility sits away from the panel average. The overlay was built for exactly that, already
cleared LONO, and has only ever been waiting on data.

## Next

1. **Run the overlay on the long histories** — the decisive remaining test. Blocked: `adaptive_width.py`
   is on an unmerged feature branch and is not reachable at `main` or at six guessed branch names.
   Need the branch name or the file.
2. Decide RAYA's treatment before it enters a production fit.
3. Landing `lib15_clean/` in `engine/raw_ohlc/EG/` needs a fresh PAT. Nothing has been pushed.

Artefacts (session workspace): `lib15_clean/` (32 gate-cleaned CSVs, library format),
`lib15_dq_report.csv`, `longhist_test.py`, `longhist_residuals.csv`, `longhist_{A,B,C}*.csv`.
