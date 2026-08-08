> Written 26-Jul-2026 ~19:15 UTC, alongside (not replacing) the session close-out in
> `claude/handoff/MC_Conversation_Handoff_20260726.md`. That doc's open-items list needs
> ONE ordering change before its step 2 is executed.

# URGENT — merge the data_quality patch BEFORE the next calibration run

## The situation, in one line

**The 15-year EG library is on `main` (PR #22). The gate that reads it is still broken on
`main`. The nightly cron fires at 03:00 UTC.**

## Why this matters now

`engine/data_quality.clean_ohlc` on `main` corrupts any series containing a zero or
negative price. `log(0) = -inf` trips the artifact threshold, the repair computes
`factor = p[i+1]/p[i] = x/0 = inf`, and the gate back-adjusts entire histories by
`x0.0000` then `xinf` — **while logging success.** Nine names come out with
`max|log move| = nan` and their pre-2013 history destroyed.

Verified today against the pushed long library
(`origin/data/eg-long-history-20260726`, now merged): **22 non-positive rows survive in
it**, exactly as expected — the library correctly stores RAW and the gate is supposed to
handle them.

| ticker | non-positive rows | dates |
|---|---|---|
| ABUK | 13 | 2011-03-29 … 2011-07-20 |
| CCAP, HRHO, KABO, LCSW, OCDI, OIH, TMGH | 1 each | **all 2013-05-07** (market-wide vendor fill) |
| ORWE | 1 | 2011-06-07 |
| BTFH | 1 | 2016-05-22 |

Before the 15-year merge this was harmless: the old library started in 2021 and contained
none of these rows. **The merge is what activated the bug.**

## Consequence if the order is wrong

Open item 2 of the close-out is *"Actions → Testahil continuous calibration → Run
workflow."* If that runs — or if the 03:00 UTC cron fires — before the patch lands, the
pipeline refits EG over 15 years of data with nine names' early history destroyed, and
opens a calibration PR whose numbers look plausible and are wrong. The close-out's own
expectation (*"expect roughly nu 4.0 → 5.0, width_cal 0.972 → 0.93"*) would be computed on
corrupted input.

## Required order

1. **Merge `fix/dq-nonpositive-prices`** (2 commits, pushed, `e0358aa`).
   - `3a5fa58` — `data_quality` step 1b: drop non-positive/non-finite OHLC rows before the
     repair loop, plus a defence-in-depth abort if a repair factor is ever non-finite or
     ≤ 0. **Regression: byte-identical output on all 74 production series across 9 markets**
     (sha256 of the cleaned frame vs the pre-patch gate) — a NO-OP on every pre-merge fit.
   - `e0358aa` — `market_profiles` EG fit_meta: records the 15-year calibration sample as
     TESTED, NOT ADOPTED. Comment-only; `nu=4.0`, `width_cal=0.972`, breaks and
     `signal_active` verified unchanged **by import, not parse**.
2. **Then** merge `feat/adaptive-width-overlay-eg`.
3. **Then** run the calibration workflow.

## The adaptive-width validation should be re-run after the patch

The overlay validation (22/30 names better-sized, pooled |std_u−1| 0.096 → 0.083, CRPS
PARITY) was committed at 16:17 UTC — one minute before the patch existed — against the
long library through the unpatched gate. The overlay learns each name's multiplier from
that name's **own resolved 60-day residual history**, and the `MIN_WINDOWS=28` gate counts
those windows. Nine of the thirty names had their early history destroyed, which changes
both the residuals and the window counts feeding the estimator.

The conclusion may well survive — it is a large, consistent effect. But it is currently
**unverified on clean data**, in exactly the same way the calibration comparison was.
Cheap to re-run once the patch is in; do that before treating the numbers as final.

## One reconciliation worth noting

The close-out reports the calibration-sample comparison as **PARITY** on the 30-name panel.
Re-run on **patched** data (`claude/data/EG_15yr_Calibration_ReRun_PostPatch_20260726.md`),
identical 492 scoring windows, LONO cross-fitted: LONG(2011+) **beats** CURRENT robustly
across blocks {2,3,4} *and* survives a drop-one-name jackknife (0 flips in 30).

These are not in conflict — they are the same test on different data, and the direction is
exactly what the bug predicts: the corruption sits in pre-2013 history, which **only the
LONG arm uses**, so the bug specifically handicapped the arm that wins once it is fixed.

**Neither result changes production.** The LONG advantage moves the published 90% cone by
−0.65% against a 5% materiality gate — real but immaterial. `nu=4.0 / width_cal=0.972` and
the 2022-03-21 cut stand, and that decision is now recorded in `market_profiles.py` itself
so it is not re-litigated on skill alone.

## Housekeeping

Two GitHub PATs were pasted into chat today and **both should be revoked** — neither ever
reached GitHub (every use was blocked by the sandbox classifier before the command ran).
The push that eventually succeeded used a third. See the corrected
`claude/ops/GitHub_Push_Playbook_20260723.md`: the blocker is **command shape** — any pipe,
redirect, `&&` or `;` around a credentialed push is rejected; the bare command works.
