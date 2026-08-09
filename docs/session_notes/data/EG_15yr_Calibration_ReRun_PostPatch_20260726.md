# EG 15-year calibration comparison — RE-RUN on patched data, 26 Jul 2026

Supersedes the calibration-sample section of
`EG_15yr_Library_Ingest_and_Calibration_Finding_20260726.md`, whose verdict was
invalidated by the non-positive-price gate bug
(`DQ_NonPositivePrice_Bug_and_EG_Selection_Power_20260726.md`). That doc's ledger text
is NOT retro-edited; this is the superseding pointer.

## Headline — the verdict CHANGED

**Pre-patch (that doc): PARITY at every block size → "the 2022-03-21 break cut stands."**
**Post-patch: LONG (2011+) is BETTER than CURRENT, robustly across blocks {2,3,4}.**

**But the difference is statistically robust and practically immaterial** — adopting
LONG would move the published 90% cone by **−0.65%** against a 5% materiality gate. The
choice therefore cannot be made on cone impact; it has to be made on which calibration
sample is the more honest object.

## Method

Panels rebuilt from the patched 32-series library. Only the CALIBRATION SAMPLE varies;
scoring windows are identical — **492 windows, 30 names, 2022-03-22 … 2026-04-20**
(matching the prior run's 492 exactly). (ν, width_cal) fitted **LONO**: for each
held-out name, MLE on the pooled standardized residuals of every other name inside that
arm's calibration sample, then that name scored out-of-sample under a config it did not
help fit. Scale-normalized gate (crps/spot), carry-anchored trailing-252d RW benchmark,
carry-only drift (every EG signal is OFF), 20k paths, seed 42.

**Incremental expanding-window HAR** was used to make 15-year panels tractable
(`fit_har_v3` is O(n) per origin → O(n²) per name and does not finish on 3,745-row
series). It accumulates the normal equations as the origin advances, and was
**verified against `fit_har_v3` at sampled origins on four names: max |Δβ| < 1e-8,
max |Δs²| < 1e-8.**

## Results

| arm | cal-sample | pooled ν | width_cal | scale-norm CRPS skill | 90% cone mult |
|---|---|---|---|---|---|
| A LONG (2011+) | 1,397 windows | 6.0 | 0.909 | **+0.0157** | 1.4422 |
| C MID (2016+) | 1,114 windows | 6.0 | 0.923 | +0.0155 | 1.4644 |
| B CURRENT (2022-03-21+) | 492 windows | 5.0 | 0.930 | +0.0153 | 1.4516 |
| *live production* | *478 windows* | *4.0* | *0.972* | — | *1.4652* |

Prior (pre-patch) run for comparison: LONG ν 5.90 / cal 0.911 / +0.0158; MID 5.76 /
0.911 / +0.0155; CURRENT 5.07 / 0.933 / +0.0157. The arms reproduce closely; **what
changed is the gap between them.**

### Paired block bootstrap (arm − CURRENT), 90% CI

| arm | mean diff | block 2 | block 3 | block 4 | verdict |
|---|---|---|---|---|---|
| A LONG | +6.18e−05 | [+2.5e−05, +1.13e−04] | [+2.5e−05, +1.13e−04] | [+3.1e−05, +1.11e−04] | **BETTER** |
| C MID | +3.40e−05 | [−7.1e−05, +1.58e−04] | [−6.7e−05, +1.59e−04] | [−6.0e−05, +1.54e−04] | PARITY |

### Panel-composition robustness — the check that killed the last version of this result

Drop-one-name jackknife, all 30 names, LONO configs held fixed:

- **Verdict flips on 0 of 30 single-name removals.** Every one returns BETTER.
- Mean diff range across removals: +5.24e−05 (drop ISPH) to +7.03e−05 (drop OIH).
- **No name contributes >25% of the advantage** — top contributors ISPH 18.1%,
  ORHD 16.4%, EGAL 13.9%, ADIB 9.7%, EMFD 8.8%. Three names contribute negatively
  (OIH −9.7%, LCSW −5.6%, JUFO −4.6%).

Block-bootstrap robustness and panel-composition robustness both hold, checked
separately — the two are not the same test, which is precisely why the earlier
26-name result died.

## Why the verdict moved, and why that is coherent

The bug destroyed pre-2013 history for **nine** names (ABUK, CCAP, HRHO, KABO, LCSW,
OCDI, OIH, ORWE, TMGH) by back-adjusting through `x0.0000` and `xinf`. That corrupted
region is **used only by the LONG arm** — CURRENT starts 2022 and never sees it. So the
bug specifically handicapped LONG, and the pre-patch comparison landed on PARITY
(gap +0.0001). Post-patch the gap is +0.0004, four times larger, and robust. This is the
expected direction, not a surprise.

## Recommendation

**Do not change production on the strength of this.** The gap is real but worth −0.65%
of cone width — an order of magnitude inside the materiality gate — and the standing
rule is that nothing enters the engine without surviving the test the forecasts must
survive AND mattering. A robust-but-immaterial result is an argument for a considered
decision, not an automatic switch.

The considered argument, stated for the record: the reason the 2022-03-21 cut was
adopted was that it keeps three devaluations in the calibration sample while a later cut
produces a devaluation-free sample that "wins" only because it is scored on a calm
period. **The LONG arm keeps all of those devaluations and adds more history**, so it is
not vulnerable to that critique — it is the opposite trade. Against it: 2011–2016 is a
genuinely different EGP regime (managed peg, pre-float), and the earlier finding that
going back to 2016 "hurts" was measured on corrupted data and is now itself unverified.

**Next step before any change:** re-run the ORIGINAL adoption comparison (dev-window
coverage during the Mar-2024 devaluation windows, the column that actually drove the
2022-03-21 choice) on patched data across all three arms. Skill alone did not decide
the break cut and should not decide it now.

Artefacts (session workspace, not pushed): `/home/claude/eg15/build_panels.py`,
`run_arms.py`, `_panel_raw.csv` (1,397 windows × 30 names), `_w_{arm}.csv`, `_arms.json`.
