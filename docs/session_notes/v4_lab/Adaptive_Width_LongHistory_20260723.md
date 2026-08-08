# Adaptive per-stock width + the "more history" test — 23-Jul-2026

Tests the fix the non-stationarity finding pointed to: not a STATIC per-stock width (that keeps
failing — the target moves), but an ADAPTIVE one that tracks each stock's own recent residual
errors. width_mult(o) = sqrt(EWMA_{resolved past}(u^2)), clipped [0.7,1.5], EWMA lambda 0.85,
walk-forward safe (a 60d window at origin o' only enters the estimate once it resolves at o'+60).
Baseline = production static width_cal=0.972. Data: user supplied 15yr histories.

## Long-history pilot (ORHD ~11.5yr/41 windows, ISPH ~8.6yr/30 windows), DEV 55% / FINAL 45%

| stock | scheme | FINAL std_u (→1) | cov90 (→0.90) | logCRPS skill |
|---|---|---|---|---|
| ORHD (too wide) | baseline | 0.74 | 1.00 | +0.0169 |
| | static-fit (DEV) | 0.71 | 1.00 | +0.0168 |
| | **adaptive** | **0.88** | **0.89** | +0.0071 |
| ISPH (too narrow) | baseline | 1.32 | 0.71 | −0.0289 |
| | static-fit (DEV) | 1.57 | 0.64 | −0.0517 |
| | **adaptive** | **1.03** | **0.86** | **+0.0013** |

- **Static per-stock width fails even with more data** — ISPH proves why: too WIDE early (DEV std
  0.84) but too NARROW late (FINAL 1.32); fitting the early period pushes the cone the wrong way
  and FINAL gets worse. The moving target, made concrete.
- **Adaptive works, right direction, both stocks.** ISPH is a clean win on all three metrics
  (log-CRPS flips negative→positive). ORHD: calibration fixed (over-covered 1.00→0.89, std toward
  1) at a small log-CRPS cost. Multipliers self-correct: ORHD ~0.86× (shrinks its wide cone),
  ISPH ~1.33× (widens its narrow one).

## Panel confirmation (all 30 EG names, 5yr each — the n=2 caveat check)

- **Calibration dispersion improved: adaptive moved std_u closer to 1.0 for 22 of 30 names**;
  pooled |std_u−1| = 0.091 → **0.018**. First mechanism in the whole program to improve per-name
  width (criterion B) out-of-sample.
- **BUT it over-corrects on 5yr history.** Pooled cov90 0.892 → 0.859 (past target, now outside
  the ±2% band), and log-CRPS is **PARITY** (block-bootstrap straddles 0 at all block sizes,
  slight lean worse; adaptive wins only 49% of warmed windows). The scheme fixes the extreme
  mis-calibrated names (ISPH, TMGH, EFID, CLHO all improve) but adds noise to already-fine names
  (HELI 1.02→1.40, OIH 1.11→1.30) because on ~17 windows the EWMA of only 3–10 resolved windows
  is itself noisy.

## The synthesis (this answers "will more history help?")

**Yes — empirically, more history is exactly what makes the adaptive fix work.** The adaptive
correction's quality depends on how many resolved windows it can average: on 8–11yr (ORHD/ISPH)
it cleanly fixes extreme mis-calibration; on 5yr (panel) it's too noisy and nets to parity while
over-correcting good names. The mechanism that improves criterion B is the one that most needs
more windows. Static per-stock width can NOT be rescued by more data (the target is non-stationary);
adaptive width CAN, and needs the data.

## Status: PROMISING, needs refinement — NOT yet promotable

First non-rejection of the session. Two concrete fixes before it could clear the full gate:
1. **Shrink the correction toward 1.0** (e.g. mult = 1 + s·(sqrt(EWMA)−1), s~0.4–0.6, DEV-tuned)
   so it stops over-correcting already-calibrated names — should recover the cov90 loss and the
   log-CRPS parity while keeping the dispersion gain.
2. **Confirm on more long-history names** (the 6–8 originally proposed), since the clean wins
   showed up only where history was long. The pilot is 2 stocks — directional, not a verdict.

Production unchanged. Scripts: `lab_adaptive_width.py` (long pilot), `lab_adaptive_panel.py` (panel).
