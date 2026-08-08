# Handoff — pipeline fix rebuilt + silver dual-fit computed (23-Jul-2026)

> **[SUPERSEDED IN PART — 8-Aug-2026]** The proposed TOP OPEN ITEM in §3 is wrong on its central claim and must not be pasted anywhere: name-level width_cal was NOT closed-and-rejected, and the "robust FAILs are over-coverage" premise it calls stale is exactly the finding that carried the day — `engine/adaptive_width.py` was ADOPTED 23-Jul-2026 as an EG-only, history-gated (MIN_WINDOWS=28 resolved 3-month windows) online per-name width overlay, and it is merged into main. Everything here gated on "PAT arrival" is also retired: since 07-Aug-2026 there is no token gate, and engine changes go on a feature branch with an open PR reviewed by a human before merge, never a direct push. The rest of this document stands as the dated record of what was done at the time.

Everything below is DONE locally and waiting only on Sherif's one message (PAT + two decisions). Nothing has been pushed; production files on `main` are untouched. [RETIRED 8-Aug-2026 — see header]

## 1. Pipeline crash fix — rebuilt, tested, committed on branch `fix/pipeline-crash-thin-names` (commit adbe70e)

The unattended loop has been dead since ~19-Jul (LULU's 2 windows crash the block bootstrap; AE sorts first so every market starved; junk daily branches with stale PR bodies). Yesterday's fix branch died with the old container — rebuilt today from the documented spec, verified by import (not parse), unit-tested (n=2 → PROVISIONAL(insufficient-windows), n=4 → resolves normally), and full-library dry run:

- `verdict_ci`: n < block → NOBLOCK sentinel instead of ValueError.
- `robust_verdict`: any NOBLOCK → `PROVISIONAL(insufficient-windows)` — a thin name can never robust-FAIL, never silently PARITY, never crash; auto-resolves at ≥4 windows.
- `auto_refresh`: per-market try/except → `PENDING_REVIEW/{MKT}_{date}-ERROR.md`, nonzero exit, other markets still run.
- Workflow: PR title/body from the NEWEST report (`ls -t`), not alphabetical.
- The 6 panels the dead loop never built (AE ADIBUAE/BURJEEL/DEWA/LULU/SALIK, EG DSCW) + refreshed EG_PHDC + hashes.

Dry run reproduces the 22-Jul audit exactly: AE flags MATERIAL (ADCB PARITY→BOUNDARY → proper PR on next CI run), EG non-material (DSCW enters PARITY-range, pooled cal 0.972→0.965, market PASS holds), all other markets reproduce. Also riding on local `main`, unpushed: ca97b83 (ISPH gate-check note) + eb8629e (pycache gitignore).

**On PAT arrival:** push `main` + `fix/pipeline-crash-thin-names`, open the PR, token used at push moment only and never stored, remote reset to tokenless URL after. [RETIRED 8-Aug-2026 — see header]

## 2. Silver calibration — BOTH options computed end-to-end (lab, nothing wired)

Silver panel built lab-side (19 windows, 2021-12→2026-02, 1 stale row dropped by the DQ gate):

| option | fit | silver verdict | notes |
|---|---|---|---|
| **A. Pooled 3-metal (recommended)** | **nu=20, cal=0.965** on 148 windows — matches the XPT note's anticipated config exactly | **PASS +0.0124 on a leave-silver-out fit** — a genuine out-of-sample pass | de-circularizes GOLD too (its LOMO verdict now comes from silver+platinum data: PARITY +0.0013); PLATINUM PARITY −0.0114; complex pooled PARITY [−0.015,+0.007] |
| B. Self-fit | nu=8, cal=1.147 on silver's own 19 windows | +0.0225 BOUNDARY, **CIRCULAR** | same self-fit flaw the metals section already carries for gold |
| (today's config) | borrowed gold, nu=Gaussian, cal=1.0 | +0.0181 — published with NO fit of its own | the thing both options fix |

90% cone half-widths (×σ_h): borrowed 1.645 / pooled 1.579 / self 1.847. Option A is the recommendation on the project's own standards: silver validates out-of-sample, gold's circularity flag finally lifts. Adoption (profile wiring for XAG + registry) is one small change prepared on request after the decision — it interacts with how `XAG` gets a profile code, so it goes in its own commit, not smuggled into the crash fix.

## 3. Proposed TOP OPEN ITEM replacement (paste into project instructions) [RETIRED 8-Aug-2026 — see header; do not paste this block anywhere]

> TOP OPEN ITEM — name-level width_cal shrinkage: CLOSED, REJECTED (22-Jul-2026 full-universe walk-forward, 71 names/7 markets: per-name width loses to the market LONO fit essentially everywhere; KR alone favored it with a zero-crossing CI on 49 windows and clip-bound cals — revisit only if KR reaches ~6+ names / ~100+ windows). The "robust FAILs are over-coverage" premise is stale (ELM is UNDER-covered at cov90 0.69; IQCD near-nominal 0.89). NOW OPEN: (1) FV-pull drift shadow validation — claude/v4_lab/shadow_cohort_20260723.json, grade each name at its actual T+60 (~mid-Oct-2026); promotion needs ≥3 non-overlapping cohorts, paired ΔCRPS bootstrap blocked by cohort favoring the shadow, cov90 ∈ [88,92], no name >25% of the delta. (2) h>60 simulation must move to block-mixture (one-mix-per-path ⇒ infinite terminal mean; published multi-year EVs are seed artifacts — lead with medians until adopted). (3) Metals: pooled 3-metal fit computed (nu=20/cal=0.965, silver PASSES leave-one-metal-out) — adopt on decision. (4) Per-origin vol estimation still not break-aware. (5) GBCO + STC WACCs predate v2 — re-issue. [RETIRED 8-Aug-2026 — see header]

## 4. Still needed from Sherif (one message covers all)

1. The PAT string (previous message said "here is a PAT" but contained no token) + scope line. [RETIRED 8-Aug-2026 — see header]
2. Delete `raw_ohlc/AE/ADIBUAE.csv`? (byte-identical dupe of ADIB — recommend YES; his file-placement call, so not done unilaterally).
3. Silver: option A (pooled, recommended) or B (self-fit).
4. Optionally paste §3 into the project instructions. [RETIRED 8-Aug-2026 — see header]

Scripts: `claude/v4_lab/lab_silver_dual_fit.py` (+ lab silver panel `XAG_SILVER_60d_LAB.csv` local only).
