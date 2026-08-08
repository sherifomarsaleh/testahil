# Name-level width_cal shrinkage v2 — full universe, walk-forward: REJECTED

**22-Jul-2026. Local, read-only against production machinery; nothing pushed.
Successor to the 20-Jul 17-name test ("inconclusive, do not promote"). This
run is conclusive: the TOP OPEN ITEM should be closed as REJECTED.**

## Bottom line

- **71 names, 1,154 windows, every multi-name market (EG SA US KR AE IN QA),
  temporal walk-forward own-scale estimation, k cross-fitted leave-target-out.**
  This is the strongest validation design the system has run on any candidate.
- **Global improvement over the existing LONO machinery: zero.** Pooled skill
  +0.0107 → +0.0106; paired block-bootstrap d = CI90 [−0.0002, +0.0001].
- **EG — the largest panel (30 names, 462+ windows) — is monotonically against
  shrinkage.** Every step toward per-name width loses walk-forward skill
  (+0.0159 at k=0.5 vs +0.0196 at no-shrinkage). In a devaluation-driven
  market the names' standardized residuals are homogeneous; per-name width is
  pure estimation noise.
- **SA actively regresses: ALINMA PARITY → robust FAIL (−0.0078 → −0.0160)
  and RAJHI PASS → BOUNDARY.** The method manufactures exactly the artifacts
  it was meant to remove. (Same cost-column pattern as ADNOCGAS in v1.)
- **KR is the one genuine positive** — and it still doesn't clear the bar.
  With k chosen only on the other two names, LGES's robust FAIL resolves to
  PARITY (−0.0268 → +0.0023), SAMSUNG +0.0094 → +0.0359, KR pooled +0.0002 →
  +0.0151. But: paired CI90 [−0.0047, +0.0213] **crosses zero** on 49 windows,
  and both deploy cals are **clip-bound** (LGES 1.245→0.850 = the floor,
  SAMSUNG 1.021→1.300 = the ceiling) — the same cap-bound pathology that
  discredited SA's old cal=1.28. A parameter pinned at its clip is not a fit.
- **The premise of the open item is partly stale.** ELM's robust FAIL is
  UNDER-coverage (cov90 = 0.69), not over-coverage — no width shrinkage fixes
  it. IQCD sits near-nominal coverage (0.89); its FAIL is not a width story
  either. And ALPHADHABI's FAIL dissolves with NO methodology change at all —
  see the pipeline appendix: the pending 18-name AE refit moves its LONO cone
  from 1.056 to 1.035 and its verdict to PARITY. After that refit merges,
  **LGES is the only live FAIL that shrinkage would address**, on the
  weakest panel in the equity universe.

**Verdict: REJECT as a blanket mechanism — do not revive.** It joins
CRPS-selection in the rejected ledger, killed by the same standard (looked
plausible under weak validation, failed under the honest one). Single revisit
condition: if/when the KR panel reaches ~6+ names or ~100+ windows and the
KR-local signal survives a then-adequately-powered walk-forward test,
propose a KR-only exception via the PR path. The real fix for KR — and for
"bands too broad" generally — is panel growth, not a new estimator.

## Method (what v2 changed vs v1)

1. **Universe**: all 71 multi-name-market names (v1: 17). ADIBUAE excluded
   (byte-identical duplicate of ADIB — see appendix). Singleton markets
   (XAU, XPT) excluded by construction: nothing to shrink toward.
2. **Temporal walk-forward own-scale** (the decisive upgrade): the scale used
   at window i is fit ONLY on that name's windows before i (expanding, min 4
   priors; before that the name gets the pure market LONO cal). v1's
   leave-one-window-out barely perturbed a 15-point fit and flattered the
   candidate — exactly the trap the doc itself flagged. Walk-forward is
   deployment-faithful: at each origin only past residuals exist.
3. **k cross-fitted leave-target-out**: the k used to score name x is the
   argmax of pooled walk-forward skill over names EXCLUDING x (per-market
   pool for markets with ≥6 names; also run per-market for the 3-name
   markets as a variant). k never sees the name it scores.
4. Scoring: `rescore_percal` (per-window cal), re-verified bit-for-bit
   against production `fast_rescore` at constant cal. nu held at the market
   LONO value throughout (nu is weakly identified; the open item was about
   width). Same crps/spot normalization, same robust-verdict blocks {2,3,4},
   seeds unchanged.

Known residual leakage, stated: the market LONO scale s_l pools other names'
full histories (including future windows). Production's own refit loop has
the same property, and a fully-jackknifed s_l changes at O(1/total-windows).

## Key tables

Walk-forward pooled skill vs k (selected rows; LONO row = no shrinkage):

| k | EG | SA | US | KR | AE | IN | QA | GLOBAL |
|---|---|---|---|---|---|---|---|---|
| 0.5 | +0.0159 | −0.0023 | −0.0131 | **+0.0151** | −0.0019 | −0.0009 | −0.0359 | +0.0072 |
| 12 | +0.0177 | −0.0006 | −0.0112 | +0.0100 | +0.0013 | +0.0005 | −0.0212 | +0.0093 |
| 50 | +0.0191 | **+0.0007** | −0.0096 | +0.0045 | +0.0024 | +0.0030 | −0.0144 | +0.0105 |
| ∞ (=LONO) | **+0.0196** | +0.0002 | −0.0085 | +0.0002 | **+0.0026** | **+0.0044** | **−0.0110** | **+0.0107** |

Every market except KR (and SA's ~5bp bump, which buys the ALINMA/RAJHI
regressions) maximizes at or near NO shrinkage. QA/US negative levels are the
known low-vol-pegged-market carry story, unrelated to k.

Pooled, at honest LTO-k: production +0.0122 / LONO +0.0107 / shrunk +0.0106.
(Production's edge over LONO is in-sample flattery — its cal was fit with
each name in the pool; LONO is the honest baseline, as established 10-Jul.)

Verdict changes at honest LTO-k, entire universe: SA/ALINMA PARITY→FAIL,
SA/RAJHI PASS→BOUNDARY. No name anywhere improves its verdict. Under the
per-market-k variant KR resolves LGES (FAIL→PARITY, blocks {2,3,4} all
PARITY: [−0.034,+0.044]/[−0.025,+0.048]/[−0.020,+0.051]) at the cost of
KAKAO +0.0022→−0.0039 (stays PARITY) and the clip-bound cals above.

k-stability bootstrap (1,000 name-resamples): EG picks k=∞ in 93% of draws —
unambiguous. AE median ∞ (60% of draws). SA wide/bimodal (IQR 25–160 with
18% at ∞) — no identified k even on 11 names. Consistent with v1's finding;
now with the added information that where k IS identified, it's identified
as "don't".

## Why this is trustworthy

- Same production code path (fast_rescore verified bit-for-bit; panels
  hash-current; local chain reproduced every live market fit exactly before
  the experiment — 9/9 including AE on its live 14-name panel).
- Doubly out-of-sample where it counts: scale walk-forward in time, k
  cross-fitted across names.
- The one favorable result (KR) is reported with its CI, its clip-bound
  deploy values, and its sample size — the reasons it doesn't promote.

---

# Appendix — pipeline audit (found en route, fixed on a local branch)

**The unattended loop has been dead since ~19-Jul-2026.** Root cause: LULU
(AE, listed Nov-2024) produces 2 post-burn-in windows; `robust_verdict`'s
block bootstrap at block≥3 calls `rng.integers(0, n−block+1)` with high≤0 →
ValueError. AE sorts first, so the exception killed every daily run for ALL
markets: nothing has been refit since, EG/DSCW was never panel-built, silver
was never touched, and the workflow's failure path shipped a junk branch per
day (`calibration-review-2026072*`) containing half-written panels with a PR
body drawn from the stale 13-Jul EG breaks report (alphabetical `ls`).

**Fix — committed locally on branch `fix/pipeline-crash-thin-names`, not
pushed (no token stored, per protocol):**

1. `verdict_ci`: n < block → `(nan, nan, "NOBLOCK")` instead of raising.
2. `robust_verdict`: any NOBLOCK → **`PROVISIONAL(insufficient-windows)`** —
   the robust-FAIL bar is unmeetable on a thin name, so it can never FAIL,
   never silently PARITY, never crash; re-resolves at ≥4 windows.
3. `auto_refresh`: per-market try/except — a crashed market writes
   `PENDING_REVIEW/{MKT}_{date}-ERROR.md`, exits nonzero, and the OTHER
   markets still run. One market can never again kill the loop.
4. Workflow: PR title/body from the NEWEST report (`ls -t`), not alphabetical.
5. The 6 rebuilt panels (5 AE + EG/DSCW) + panel_hashes entries.

Verified by import (not parse) and by a full dry run.

**What the unblocked pipeline reports (preview of what CI will do once the
fix merges):**

- **AE — MATERIAL, will open a proper PR**: with BURJEEL/DEWA/LULU/SALIK in
  the pool, ADCB flips PARITY→BOUNDARY (flip is genuine — reproduced with and
  without the dupe). Pooled fit 19-name: nu=10, cal=1.042; **18-name (dupe
  deleted): nu=10, cal=1.028**. And on the 18-name panel **ALPHADHABI's
  robust FAIL resolves to PARITY** (LONO cal 1.056→1.035, skill −0.0094) —
  one of the two motivating FAILs of the shrinkage item, fixed by simply
  processing the posted data.
- **EG — NOT material, will auto-commit**: DSCW enters cleanly
  (PARITY-range), pooled cal 0.972→0.965, nu=4 unchanged, market PASS holds.
- All other markets: reproduce exactly, no changes.

**Recommendations needing Sherif:**

1. **Delete `raw_ohlc/AE/ADIBUAE.csv`** (byte-identical to ADIB.csv —
   `diff` verified). It double-weights ADIB in every AE fit and LONO pool.
   File placement is the human decision, so I did not remove it.
2. **Silver is posted but invisible**: `raw_ohlc/XAG/SILVER.csv` (1,431
   rows, ~5.7y) is skipped every run because `XAG` is not a profile code.
   The data that de-circularizes metals — the system's weakest calibration —
   is already in the library. Decision needed: pooled 3-metal fit (the
   XPT note's anticipated nu≈20/cal≈0.965 config) vs an XAG self-fit. I
   recommend the pooled fit; say the word and I'll run it end-to-end.
3. Merge the fix branch (I'll push it whenever you hand me a fresh PAT —
   until it merges, the loop keeps crashing daily at 03:00 UTC).
4. Update the TOP OPEN ITEM in the project instructions: name-level
   width_cal shrinkage → REJECTED (this doc), revisit only as a KR-only
   candidate if the KR panel grows to ~6+ names / ~100+ windows. The open
   item's claim that all robust FAILs are over-coverage is stale (ELM is
   under-covered at 0.69; IQCD near-nominal at 0.89).

## Reproduction

Scripts alongside this doc in the project: `shrinkage_v2.py` (scoring pass,
~80s), `shrinkage_v2_phase2.py` (k-selection/verdicts/bootstrap),
`shrink_v2_results.json` (full per-name table, LTO-k map, k-stability).
Universe = current library incl. the 4 genuine new AE names + DSCW, excl.
ADIBUAE. Engine at commit 1804481 + the fix branch. Seeds all production
defaults (42); no Date.now-style nondeterminism anywhere.
