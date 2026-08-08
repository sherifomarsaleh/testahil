# Roll-Forward — COMI, EMFD, KAKAO, LGES — 28 Jul 2026

**Status: PUSHED to main as `dfd20d3`** (verified byte-identical on `raw.githubusercontent.com`).

Trigger: 4 fresh OHLC uploads for already-covered tickers → roll-forward workflow, not a new study. A 5th upload ("LG Electronics") was surfaced as a mismatch against the site's LGES coverage (066570 vs 373220 — LG Electronics' 2011 start date rules out LGES, which IPO'd Jan-2022); the user confirmed the mix-up, supplied the correct file, and dropped LG Electronics from scope.

## THE HEADLINE: this session raced a concurrent session on the same repo

While this roll-forward was being built, a **separate Claude session** (`session_01V25qLtQrqksqaavJdunC4U`) pushed `29998a4` — a market-wide EG/AE/SA cone re-strike touching 58 cones, including **COMI and EMFD**. It landed ~30 minutes before this session tried to push. Consequences:

- Every EG ticker entry in `data.js` was rebuilt, so this session's assert-guarded replacement anchors no longer existed. The first publish script would have MISSed rather than corrupted — the assert guard did its job.
- **It burned the same cache-buster token, `20260728a`.** Two independent sessions picked the same date-plus-letter. Had this session pushed without checking, readers would have had a stale-cache token collision with no way to distinguish. Bumped to `20260728b`.
- It introduced a richer ledger row schema (`grade_basis`, `horizon_days`, `anchor_vol`, `note`) and an `hz` field on ticker entries. Both adopted here.

**Standing lesson: `git fetch` and inspect divergence BEFORE building publish anchors, not just before pushing.** The anchors are the expensive artifact; rebuilding them cost a full second pass. A `git fetch` at the top of the roll-forward would have caught it for free.

Note `hz` is currently read by **no page on the site** — it is forward-looking metadata as of this commit.

## 1. OHLC merge (merge-never-overwrite)

| Ticker | Market | New rows | Overlap verified |
|---|---|---|---|
| COMI | EG | +3 | exact, byte-for-byte |
| EMFD | EG | +3 | exact, byte-for-byte |
| KAKAO | KR | +21 | exact, byte-for-byte |
| LGES | KR | +21 | exact, byte-for-byte |

Header match confirmed, overlap row matched to the 4th decimal, only upload-only rows prepended, no back-adjustment, UTF-8 BOM preserved. Origin never touched `raw_ohlc/`, so these merged cleanly through the collision.

## 2. Calibration (Step 0.0 + Step 0, full market panel)

Scoped refresh for EG (30 names, 494 windows) and KR (3 names, 85 windows) via the real `auto_refresh.py`/`panel_refresh.py`, not a reimplementation.

- **EG**: proposed nu=6.0 / width_cal=0.951 — **numerically identical** to incumbent. Flagged MATERIAL solely on 14 per-name verdict changes. Market verdict PASS (skill +0.0158, CI[0.009, 0.022]).
- **KR**: proposed nu=10.0 / width_cal=1.063 — **numerically identical** to incumbent. Flagged MATERIAL solely on LGES verdict FAIL→PARITY. Market verdict PARITY (skill +0.0008, CI[-0.003, 0.009]).

**Control-run finding**: isolated via `git stash` (pristine clone vs. this session's merge) — output byte-for-byte identical either way, for every market including EG and KR. The verdict churn is 100% pre-existing (stale `fitted_configs.json` registry mirror), not caused by today's data. Independently corroborated: origin's concurrent commit reached the same conclusion from a different starting point ("a full 3m panel refit on today's libraries reproduces the live profiles exactly... 0.00% band move").

`market_profiles.py` **not touched**. `PENDING_REVIEW/EG_2026-07-28.md` and `KR_2026-07-28.md` written via the real `write_pending_review()`.

## 3. Grading — matured cohorts

Never trusted the stored `grade_date`; counted actual trading rows from `anchor_date`.

| Ticker | Stored | True | Matured? | Result |
|---|---|---|---|---|
| COMI cycle-1 T+20 (anchor 29-Jun) | 2026-07-27 | — | **No** — 19 of 20 true EGX sessions | left open |
| KAKAO cycle-1 T+20 (anchor 26-Jun) | 2026-07-24 | 2026-07-27 | Yes | realized 37,050 vs p50 33,294 · in_90 ✓ in_50 ✓ · quantile 0.74 · median_err +11.28% · touch +5/+10 hit |
| LGES cycle-1 T+20 (anchor 26-Jun) | 2026-07-24 | 2026-07-27 | Yes | realized 333,000 vs p50 332,400 · in_90 ✓ in_50 ✓ · quantile 0.505 · median_err +0.18% · touch +5..+20/−5 hit |

Both: `grade_date` corrected, `grade_basis:"actual"`, `grade_date_projected` + `grade_note` added, frozen percentiles untouched.

**Origin could not grade these** — it explicitly noted "Kakao/LGES/TMPV/TSLA still have zero post-anchor data," because it lacked this session's OHLC merge. This is the piece of the work that was genuinely uncontested and is why the user's screenshot showed "due — grading 24 Jul 2026" badges.

COMI is the instructive direction of the never-trust-grade_date rule: the real EGX calendar ran **behind** the naive projection, so a date that has already passed still isn't mature. It matures on the next session.

Six rows remain "due" on the live ledger (COMI, CCAP, ORAS, TMPV, EMAAR, TSLA) — all pre-existing, all 1–5 sessions short of a true T+20, same class origin flagged. None were graded.

## 4. Data-integrity flag — COMI anchor price

Published anchor_price (129.25) vs. library close on 2026-06-29 (126.89): **1.83% discrepancy**, pre-existing — not caused by this merge or by data-quality cleaning (`clean_log` empty for that range). Recorded, not silently reconciled in either direction. **Still open.** EMFD showed a trivial 0.09% rounding difference (11.690 vs 11.70) — noted, immaterial.

## 5. New cohorts struck (append-only, 8 rows)

Calendar 1M/3M convention, production chain with no approximation, seed 42, 50k paths, signal OFF, q_annual=0 (flagged).

| Ticker | Anchor 28-Jul | Cycle | h (1M/3M) | 1M p50 / 3M p50 |
|---|---|---|---|---|
| COMI | 141.50 EGP | 3 (from 22-Jul) | 21 / 62 | 143.61 / 148.09 |
| EMFD | 11.59 EGP | 4 (from 22-Jul) | 21 / 62 | 11.76 / 12.13 |
| KAKAO | 35,650 KRW | 2 (from 26-Jun) | 22 / 62 | 35,717 / 35,984 |
| LGES | 314,000 KRW | 2 (from 26-Jun) | 22 / 62 | 314,565 / 317,022 |

**On superseding origin's 22-Jul COMI/EMFD strike**: the user posted 3 further EGX sessions after that strike was built, so these re-strike on genuinely newer data. Origin's 22-Jul cohorts stay open and grade on their own terms — nothing retro-edited. Precedent for re-striking on this cadence is already in the house record: origin itself struck EMFD cycle-3 three days after cycle-2.

Independent cross-check that both sessions used the same 15-year libraries and the same chain: COMI 1M half-width came out 11.5% here at 141.50 vs. origin's 11.1% at 140.00 — same regime, ~4 sessions apart.

## 6. What was explicitly left alone, and why

- `fair{bear,base,full}` — separate clock, needs a real study refresh.
- Technical S/R levels and `tech` narrative — need a fresh chart read.
- Slider factor-stack constants (CONT_FIXED/EV_FIXED/GEO_MEAN/…) — fit to the fundamental driver stack, not the carry-anchored engine.
- `ledger.html`'s `COHORT_OHLC` overlay map — COMI/KAKAO/LGES still have no entry, so their cohort charts render anchor+realized dots only. Pre-existing, out of scope.
- Five-year quarterly backtest PNGs — not regenerated; a single new cohort never moves that coarser construct.
- **EMFD's touch ladder still sits entirely above spot** and wants a human re-pick — same open item origin raised for PHDC/EMFD/HELI.

## 7. Publish bug caught by `node --check`

The first publish script reported every replacement "OK" and still produced invalid JavaScript: an insertion anchored on the *preceding* row's closing `},` consumed that brace without re-emitting it. Assert-guarded string replacement verifies that the old text existed — it cannot verify that the surrounding structure survives. `node --check` caught it; the assertions never would have.

**Standing lesson: for `data.js`, a syntax check is not optional post-verification — it is the only check that covers stitch points.** Better still, the v2 script was verified by *loading* `data.js` in node and asserting on the parsed `TICKERS`/`LEDGER` objects (counts, spots, grades, cycle numbers) rather than on the text — the JS analogue of the standing VERIFY-BY-IMPORT-NOT-BY-PARSE rule.

## 8. Verification performed

- `node --check assets/data.js` → valid.
- Loaded in node: 71 tickers, 286 ledger rows (278 + 8), all four spots/dists/hz confirmed, both grades confirmed, all 8 new cohorts confirmed with correct cycle numbers.
- Cache-buster `20260728a` → `20260728b` across 87 files; zero stale-token references repo-wide.
- `market_profiles.py` diff empty.
- Staged diff scanned for credential-shaped strings before commit — clean.
- Pushed via one-shot authenticated URL; remote verified tokenless afterwards, no credential in `.git/config`.
- **Post-push**: `raw.githubusercontent.com/.../assets/data.js` byte-identical to local; `raw_ohlc/KR/LGES.csv` on main carries the 28-Jul row.
- Not verifiable from here: what `testahil.com` serves a reader (network-blocked — see `claude/ops/Live_Site_Verification_Blindspot_20260728.md`).

## Open items after this session

1. COMI anchor-price discrepancy (129.25 vs 126.89) — unresolved.
2. `PENDING_REVIEW/{EG,KR}_2026-07-28.md` (plus the older `EG_2026-07-26.md`) — all registry-only churn with numerically unchanged calibration; safe to review at leisure.
3. EMFD/PHDC/HELI touch ladders need a human re-pick.
4. COMI cycle-1 T+20 matures next session and should be graded then.
5. Pushing `raw_ohlc/` to main fires the auto-refit GitHub Action; expect it to reach the materiality gate and open a PR rather than auto-commit.
