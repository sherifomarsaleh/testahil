# Step 0.0 gate bug (non-positive prices) + EG-only selection power — 26 Jul 2026

Two findings from ingesting the EG 15-year library through the live gate. The first is
an engine bug now patched; the second kills the EG-only selection test as specified.

## 1. GATE BUG — `data_quality.clean_ohlc` corrupted 9 of 30 EG names

**22 rows across 10 of 32 series carry a zero or negative OHLC value.** Seven land on
one market-wide date — **2013-05-07** (CCAP, HRHO, KABO, LCSW, OCDI, OIH, TMGH). Also
ABUK (13 rows, Mar–Jul 2011), BTFH (2016-05-22), ORWE (2011-06-07).

**Failure mode.** A zero price makes `log(p) = -inf`, so `lr = -inf` trips the artifact
threshold; the repair then computes `factor = p[i+1]/p[i] = x/0 = inf`. The gate
back-adjusted whole histories by `x0.0000` and then by `xinf`:

```
[TMGH] back-adjusted 535 rows before 2013-05-07 by x0.0000
       back-adjusted 536 rows before 2013-05-08 by xinf
```

ABUK, CCAP, HRHO, KABO, LCSW, OCDI, OIH, ORWE, TMGH all emerged with
`max|log move| = nan` — pre-2013 history destroyed — **while the gate reported success.**
Same failure class as `nu=Gaussian`: survives every check that is not a numerical
inspection of the output.

**Patch** (branch `fix/dq-nonpositive-prices`, commit `3a5fa58`, NOT pushed — needs a PAT):
step 1b drops non-positive/non-finite OHLC rows before the repair loop, logged; plus a
defence-in-depth abort if any repair factor is ever non-finite or ≤ 0.

**Regression: byte-identical output on all 74 production series across 9 markets**
(sha256 of the cleaned OHLC frame vs the pre-patch gate). The patch is a **NO-OP on
every live fit**; no materiality gate triggered. Verified by import, not parse.

**Blast radius.** Nothing in production is affected — the short library starts 2021 and
contains none of these rows. But **the calibration comparison in
`EG_15yr_Library_Ingest_and_Calibration_Finding_20260726.md` is unverified**: its LONG
(2011+) and MID (2016+) arms calibrate over exactly the destroyed region, for nine
names. Its PARITY verdict must be re-run on patched data before it is cited. The
"break filter stands" conclusion may well survive — but it has not yet been shown to.

**Post-patch library: 32 series, 97,756 cleaned sessions, 829 rows removed, zero
non-finite results.** Max |log move| across all series 0.2407 (EGX ±20% limit implies
≤0.223; the residual is the LIMIT_SAFETY margin, not a defect).

## 2. THE EG-ONLY SELECTION TEST IS UNDERPOWERED — v1 pre-registration §6 is wrong

The v1 thresholds assumed a balanced 30 names × 62 cohorts. The real structure isn't
balanced: on the EGX30 master calendar there are **58** non-overlapping 60-session
anchors (2012-03-26 … 2026-04-20), and the **median cohort carries 25 names, not 30**
(range 15–30) because names enter and leave as listings and history requirements bite.

Critical mean rank IC and power, simulated on the **actual** per-cohort name counts:

| configuration | cohorts | crit α=.05 | Bonferroni-6 | power @IC .05 | @.08 |
|---|---|---|---|---|---|
| Tier A (252 trailing), all 30 | 58 | 0.0457 | **0.0666** | **22%** | 60% |
| Tier A, ex-RAYA only (29) | 58 | — | 0.0670 | 22% | 59% |
| Tier A, ex-6 thin names (24) | 58 | 0.0514 | 0.0735 | 18% | 50% |
| Tier B (1260 trailing, F3), all 30 | 41 | 0.0577 | **0.0843** | **13%** | 37% |

*v1 assumed: EG-only 0.0565 / 33% power; pooled EG+AE+SA 0.0395 / 67%.*

Three consequences:

1. **EG alone cannot decide this.** 22% power against a strong factor (IC 0.05) means
   we miss a real factor four times in five. **AE/SA long history is not optional — it
   is the difference between a test and a ritual.** This supersedes the v1 §4
   "pooled-primary" discussion: pooling is not a power optimisation, it is a
   precondition.
2. **Excluding RAYA is nearly free** (crit 0.0666 → 0.0670, power 22.3% → 22.4%), so do
   it — its 53.9% unchanged-close sessions are categorically different from the next
   worst. **Excluding all six thin names is not free** (power 22.3% → 18.0%); the noise
   they add costs less than the cross-sectional width they provide. Exclude RAYA only;
   keep EFID (21.7%), LCSW (21.3%), OIH (18.5%), RMDA (16.6%), KABO (15.4%) with a flag.
3. **F3 (long-term reversal) is the weakest, not the strongest.** It needs 1260 trailing
   sessions, which costs 17 of 58 cohorts and pushes the bar to 0.0843 — 13% power. The
   factor that motivated the 15-year library is the one that library can least support.
   Recommend dropping F3 → five factors, which also lowers the bar for the other four.

## Next

1. Push the gate patch (branch open, needs a PAT) and re-run the 15-year calibration
   comparison on patched data before its PARITY verdict is cited anywhere.
2. Obtain AE + SA 15-year history. Recompute §6 on the real pooled structure.
3. Issue pre-registration v2: five factors, RAYA excluded, thresholds from the actual
   unbalanced panel, and an explicit statement that EG-only is not a decisive test.

Artefacts (session workspace, not pushed): `/home/claude/eg15/` (32 gate-cleaned CSVs
+ `_gate_report.csv`), branch `fix/dq-nonpositive-prices`.
