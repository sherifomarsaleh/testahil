# Adaptive per-stock width — FINAL verdict, full 30-stock EG universe, 23-Jul-2026

Definitive result. User supplied long histories (6–15.6yr) for the ENTIRE 30-name EG coverage
universe. All gated through the robust pre-filter (`prep.py`) + data_quality; every cross-panel
data error caught and logged (2013-05-07 market-wide zero fills across TMGH/OIH/LCSW/KABO; the
2011 revolution EGX-closure zeros in ABUK; isolated spikes in PHDC/DSCW; the real Feb-2024
Ras-El-Hekma limit-down shared by ABUK/ORWE — kept as a genuine fat-tail event). This supersedes
the 11-stock note; method and rationale below.

## The mechanism (final form)
Online per-stock width multiplier m_raw = clip(sqrt(EWMA_{resolved past} u^2), 0.7, 1.5),
walk-forward safe. GENTLED by shrink s and a soft DEAD-ZONE dz:
    mult = 1 + s · sign(m_raw−1) · max(0, |m_raw−1| − dz)
Both fixed A-PRIORI: s=0.5 (fit once on the first 11 stocks' DEV, out-of-sample ever since),
dz=0.10 (leave a stock's cone alone when its recent implied mis-calibration is within ±10% of
correct). One-time DEV fit only; nothing tuned on the growing panel or on FINAL. Per-stock 55/45
time split; one shot on FINAL. Script: `lab_gentled_adaptive.py`. 1,397 windows (DEV 750, FINAL 647).

## Held-out FINAL result (30 stocks)

| scheme | log-CRPS skill | cov90 (→0.90) | pooled \|std_u−1\| (→0) |
|---|---|---|---|
| baseline (production, s=0) | +0.0154 | 0.903 | 0.096 |
| gentled, no dead-zone (s=0.5) | +0.0135 | 0.884 | 0.038 |
| **gentled + dead-zone (s=0.5, dz=0.10)** | **+0.0152** | **0.893** | 0.069 |

**The dead-zone is what makes it adoptable.** Plain gentling fixed calibration but cost a little
on the proper score (+0.0135 vs +0.0154) and slightly disturbed already-fine names. Adding the
dead-zone brings the proper score back to **dead-even with baseline** (+0.0152 vs +0.0154 —
statistically indistinguishable) and centres coverage best of the three (0.893), while still
cutting per-stock width error from 0.096 to 0.069 and moving 24 of 30 stocks closer to a
perfectly-sized cone. Only 3 names end up marginally worse (the residual adaptive-lag on names
whose recent behaviour differs from the test window).

Proper-score gate (dead-zone vs baseline, paired FINAL log-CRPS, block-bootstrap 90% CI across
{2,3,4}Q): mean delta +2.3e-5 (≈0), CI straddles 0 at every block size → **PARITY, dead-even**.

## Bottom line

Across the full universe, adaptive-width-with-dead-zone **improves per-stock cone calibration
(criteria B and D) at zero cost to the overall accuracy score and with better-centred coverage.**
This is the first — and now fully panel-validated — mechanism in the whole v4 program to fix the
per-stock width problem out-of-sample. It is NOT a CRPS *win* (parity), but with the dead-zone it
is no longer a CRPS *cost* either: you get materially better-sized individual cones for free.

Replication as the panel grew (per-stock closer-to-1 / dispersion halving held every step):
11/11, 13/16, 17/21, and 24/30 with the dead-zone — s=0.5 never re-fit.

## Recommendation (unchanged in direction, now much stronger)

Adopt as an explicit, gentled (s=0.5), dead-zoned (dz=0.10), clipped ONLINE per-stock width
overlay on top of the existing engine — NOT a refit of the pooled (nu, width_cal), which stays.
It requires long per-stock history to work (data-hungry; on 5yr it over-corrected), so it should
only activate for names with enough resolved windows and fall back to the pooled width otherwise.
This is a promotion decision on the B/D criteria (which it meets) at CRPS parity — take it to the
sponsor as such. Nothing is pushed to production without the standard token/PAT step and QC gate.

Open follow-ups: (1) the 3 lag-disturbed names suggest a slightly larger dead-zone or a longer
EWMA is worth a quick DEV check; (2) wire the overlay into the production engine behind a
per-name "enough history" switch; (3) the same overlay should be sanity-checked on the GCC/metals
panels before any cross-market rollout.
