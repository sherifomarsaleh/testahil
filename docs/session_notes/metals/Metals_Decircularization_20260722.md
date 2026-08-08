# Metals de-circularization — silver activated, pooled 3-metal fit analyzed

**22-Jul-2026. Follows the shrinkage-v2 session's finding that
`raw_ohlc/XAG/SILVER.csv` (1,431 rows, 2020-07 → 2026-07) was posted but
silently skipped every run — `XAG` is not a profile code. The data that fixes
the system's weakest calibration was already in the library.**

## What was done

Branch `metals/pooled-3metal-fit` (local, commit 675cf37, on top of the
ADIBUAE-removal commit): `SILVER.csv` moved `raw_ohlc/XAG/` → `raw_ohlc/XAU/`
(the existing "Metals (Gold/Silver, USD)" profile), plus its panel file
(19 windows, origins 2021-12-31 → 2026-02-27, built through the standard
Step-0.0 gate + backtest_v3 baseline chain) and its `panel_hashes` entry.
**No profile numbers were touched** — deliberately; see the reversal below.

## The pooled 3-metal analysis (run first, then NOT adopted as-is)

Pooling u across GOLD 67w + SILVER 19w + PLATINUM 62w = 148 windows
reproduces exactly the config the 20-Jul XPT note anticipated:
**nu=20, cal=0.965** (mle_scale 0.950). De-circularized leave-one-metal-out
verdicts (robust blocks {2,3,4}):

| metal | w | LOMO fit | skill | verdict | cov90 (LOMO) |
|---|---|---|---|---|---|
| GOLD | 67 | nu=15 / 0.930 | +0.0013 | PARITY | 0.90 — dead-on nominal |
| SILVER | 19 | Gaussian / 0.930 | +0.0124 | **PASS** — first own verdict ever | 0.89 |
| PLATINUM | 62 | nu=20 / 1.035 | −0.0114 | PARITY | 0.97 |

3-metal panel under the pooled fit: PARITY +0.0020 CI[−0.007, +0.009].
Cone moves vs live: gold/silver −4.0% (inside the 5% tolerance), platinum
+12.5% (material — its 0.853 was CLIP-BOUND at the 0.85 floor, a pinned
parameter, the same cap-bound pathology that discredited SA's old 1.28).

**Why the pooled numbers were reverted after being written into the
profiles:** hard-coding cross-code pooled numbers into per-code profiles
fights the pipeline's own per-code refit loop. Verified by dry run — with
(20, 0.965) installed, the next run immediately flags XAU +7.3% and XPT
−11.1% cone drift and would open correction PRs forever. Cross-code pooling
is an ARCHITECTURE (a fit-group concept), not a pair of numbers, and the
standing per-market fit rule ("every market fits its own pooled panel")
argues against it anyway. Adopting it would need Sherif to approve a
methodology change; recorded here as an option, not proposed.

## What the pipeline will now do (the adopted path)

With silver inside XAU, the next calibration run (post-fix-merge) refits the
XAU market on its own 2-name panel and — because the market verdict changes
— goes to a materiality PR, never an auto-commit:

- **XAU fit: nu=20, cal=1.035** on 86 pooled windows (cone vs live
  Gaussian/1.0: +3.0%, inside tolerance; the verdict flip is what gates it).
- **Market verdict: PASS +0.0099 CI[0.001, 0.015]** (was PARITY).
- LONO per-name: **GOLD PARITY +0.0011 — its first NON-CIRCULAR verdict**
  (scored under a fit that never saw it); **SILVER PASS +0.0181 — its first
  verdict of any kind** (no longer borrowing gold's fit unexamined).
- XPT unchanged: single-name provisional self-fit, still flagged circular.
  That flag is now honest and specific — platinum is the LAST metal without
  a de-circularized verdict. Copper (or any 4th metal) history deepens the
  pool; a fit-group mechanism would de-circularize platinum without it.

## Caveats, stated plainly

Silver's PASS rides on 19 windows — real but thin; treat it as a first
verdict, not a settled one. Gold's LONO comparator inside XAU is a
silver-only fit (19w), noisier than the 3-metal LOMO above (81w) — both
agree on PARITY, which is why the result is trustworthy. Metals remain the
thinnest panel in the system; that sentence leaves the standing protocol
only when a third metal has its own fit.

## State of local commits (pushes from this session are being blocked)

On GitHub already: `fix/pipeline-crash-thin-names` @ e4a5a65 (the loop
revival — merge this first: https://github.com/sherifomarsaleh/testahil/pull/new/fix/pipeline-crash-thin-names).
Local only: main @ 0829f70 (ADIBUAE dupe removal), branch
`metals/pooled-3metal-fit` @ 675cf37 (this change). Both are one push away
when access allows; alternatively the ADIBUAE deletion and the silver move
are each reproducible in the GitHub web UI (move = delete XAG file +
re-upload under XAU/), after which the pipeline rebuilds panels itself.
