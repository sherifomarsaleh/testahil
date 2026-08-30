# Roll-forward — OCDI · ORHD · Gold · Samsung (27-Jul-2026) — **PUBLISHED**

Trigger (b): four already-covered tickers with fresh OHLC and matured T+20 cohorts.
Live on `main` at `627e626`. The KR refit is **not** merged — see §8.

## 1. Grading — against ACTUAL sessions, not the stored grade_date

| Instrument | Anchor | 90% band | True T+20 | Projected | Realized | Verdict |
|---|---|---|---|---|---|---|
| OCDI | 24-Jun @ 22.80 | 18.31 – 29.35 | **26-Jul** | 21-Jul | 27.10 | **IN** (q 0.831, outside the 50% band) |
| ORHD | 24-Jun @ 39.30 | 32.54 – 49.64 | **26-Jul** | 21-Jul | 39.90 | **IN** (q 0.476, dead centre) |
| Gold | 25-Jun @ 3,989.85 | 3,431 – 4,598 | 23-Jul | 23-Jul | 4,048.78 | **IN** (q 0.577) |
| Samsung | 26-Jun @ 339,500 | 277,676 – 430,413 | **27-Jul** | 24-Jul | 254,000 | **OUT** (−25.2%, below p5) |

Running record **6 of 7**.

The projected dates were wrong on three of four because the Sun–Thu / Mon–Fri weekmask carries no
holiday awareness: **EGX closed 2-Jul and 23-Jul (Revolution Day); KRX closed 17-Jul (reinstated
Constitution Day)**. Corrected `grade_date` kept, `grade_date_projected` + `grade_note` added — no
percentile, anchor or touch probability retro-edited.

Samsung's `realized_quantile` is recorded **null**, not extrapolated: it closed below the published
p5, so the quantile is left-censored at <0.05. The miss is robust to the date question — at the
projected 24-Jul close (249,500) it was also outside.

OCDI's published `anchor_price` 22.80 is the **23-Jun** close, not 24-Jun (24.23) — its ticker page
already says "close 23 Jun 2026". Pre-existing label inconsistency, left alone (append-only). Graded
20 sessions from the stated `anchor_date`; the verdict is IN either way.

## 2. Step 0.0 — two data findings

**Samsung: 41 phantom pre-split prints (repaired, full history now ingested).**
Rows with `Change % = "4,900.00%"` (= 50×−1, the May-2018 50:1 split), O=H=L=C, volume `0.00K`–`0.09K`
or NaN. **Every one sits on a non-trading day** — 33 Sundays plus 8 confirmed KRX closures (Memorial
Day ×2, Seollal, Labour Day, Buddha's Birthday, the 2017 presidential election, National Foundation
Day, Hangul Day). They survive step 1 of the gate *only* because the volume string is non-NaN. Same
class as the 10-Jul KAKAO 5:1 finding, at 41 rows and 50:1.

Dropped, not rescaled. What remains is one genuine unadjusted segment before **2016-04-14**, which the
gate back-adjusts ×0.0204. Result: **1,515 → 3,709 sessions (2011-08-23 →)**, annual counts 243–250
matching the real KRX calendar, max |log return| 0.135. **The post-break history reproduces the
previous library EXACTLY — max abs diff 0.000000 over 1,365 shared sessions** — so this is purely
additive, not a restatement.

**Gold: the fresh export revises two already-published rows.** 24-Jun close 4,012.59 → 4,000.69 and
25-Jun close 3,989.85 → 4,027.56, and it drops a stray Sunday (21-Jun) the library carries. The
library rows were left **FROZEN** so the published Gold anchor stays reproducible; only genuinely new
dates spliced. Flagged, not silently adopted — say the word if you'd rather adopt the vendor's
revised vintage.

Merge was append-only throughout: **zero pre-existing dates lost** in any of the four files.

## 3. Engine bug found and shipped

`clean_ohlc`'s step-2 back-adjust does `df.loc[:i, c] = df.loc[:i, c] * factor`. Korean prices are
whole KRW, so pandas infers int64 and the assignment raises `LossySetitemError` — **the gate dies
mid-repair**. It has never bitten because EG/AE/QA/SA/US/XAU prices all carry decimals. One-line
float pre-cast, behaviour-preserving for every series that already loaded. On `main` at `5250d6c`.

## 4. Refit + materiality gate

Full panels, not just the touched names.

| Market | Fit | 90% cone | Material? |
|---|---|---|---|
| EG (30 names) | (5.0, 0.93) → **unchanged** | 0.00% | no |
| XAU (2 names) | (20.0, 1.035) → **unchanged** | 0.00% | market verdict PARITY → PASS |
| KR (3 names) | (Gaussian, 1.154) → **(12.0, 1.105)** | **−5.3%** | **YES → PR, unmerged** |

**The EG verdict churn is NOT from this update.** A control run on a pristine pre-splice clone
reproduced all 12 name-level changes identically — it is pre-existing drift between the stale
`fitted_configs.json` mirror and the current library (already logged in the 26-Jul Master Evaluations
note). `fitted_configs.json` was deliberately not written.

KR's refit narrows the published cone 5.3% and moves **LGES FAIL → PARITY**; all three names now
PARITY, market panel stays PARITY (+0.0004). It sits on branch `refit/kr-15yr-samsung`, **not
merged** — the reviewer caveat is that the panel is now unbalanced (Samsung 15 years, KAKAO/LGES ~5),
so backfilling those two before adopting is defensible. This is also the first real answer to the
"bands are too broad" complaint on KR: the width came from missing history, not from the model.

## 5. Cycle-2 cohorts (live)

Struck on the **live** profiles via the production chain — `clean_ohlc` → YZ proxy → `fit_har_v3` →
`har_forecast_v3` → carry `ln(1+rf_live) − ln(1+q)` → `simulate_paths_v3`, 50,000 paths, seed 42,
signal OFF everywhere. `q_annual = 0`, flagged (house convention; drift is a gross-of-dividend price
carry). Chain verified by reproducing the 19-Jul PHDC/EMFD/TMGH roll-forwards.

All anchored 27-Jul-2026, grading 24-Aug (T+20) / 19-Oct (T+60).

| | Anchor | T+20 p5–p50–p95 | T+60 p5–p50–p95 |
|---|---|---|---|
| OCDI | 27.48 | 23.06 – 27.87 – 33.67 | 20.45 – 28.69 – 40.33 |
| ORHD | 40.16 | 35.15 – 40.73 – 47.19 | 31.54 – 41.92 – 55.82 |
| Gold | 4,090.87 | 3,725 – 4,102 – 4,516 | 3,493 – 4,127 – 4,880 |
| Samsung | 254,000 | 177,014 – 254,565 – 365,889 | 144,517 – 256,106 – 454,889 |

Samsung on the **incumbent** (Gaussian, 1.154) by design, per the materiality gate.

## 6. Left alone, on purpose

`fair{bear,base,full}` · slider factor-stack constants · technical S/R levels and narrative ·
`market_profiles.py` (import-verified on `main`: EG 5.0/0.93, KR 250.0/1.154, XAU 20.0/1.035) ·
`fitted_configs.json` · `panel_hashes.json` beyond the touched names · **METALS.GOLD.dist.t252**
(the 12-month cohort is still open on the 25-Jun clock; a T+250 cone is outside the h=60 the fit is
validated at) · the five-year backtest PNGs (one cohort does not move a 20-quarter replay).

## 7. Needs a decision / still open

- **Four due cohorts had no data**: KAKAO T+20, LGES T+20 (both due 24-Jul), COMI T+20, EMAAR T+20
  (both due today). Post the OHLC and they roll the same way.
- **Touch ladders on two ticker pages now straddle spot.** OCDI's levels were picked for a 22.80 spot
  and 27/25/24 are now *below* 27.48; Samsung's 286,000 is now *above* 254,000. Probabilities were
  recomputed at the same absolute levels with direction taken from the new spot, per protocol — but
  the level sets themselves want a human re-pick.
- Gold vintage question above.
- Metals remains the weakest calibration in the system — a 2-name panel. The Gold PASS should not be
  read like an EGX or GCC name.

## 8. Publish record

Fast-forwarded to `main` (linear, no merge commits). PAT injected as an authenticated URL for each
push and the remote reset to the tokenless URL immediately after; nothing stored.

| commit | what |
|---|---|
| `5250d6c` | `data_quality` int64 back-adjust fix |
| `359ce6e` | roll-forward — library + `data.js` |
| `1cf5f68` | CI auto-regenerated `feed.xml` from the new `data.js` |
| `627e626` | **cache-buster bump** — see below |
| `7d9ea18` | CI auto-regenerated sitemap + homepage strip |

**`refit/kr-15yr-samsung` remains an unmerged branch** — deliberately. Merging it is the only
outstanding publish decision.

### The cache-buster trap (worth remembering)

Every page pins the data file as `assets/data.js?v=<token>`. Changing `data.js` without bumping that
token means browsers and the Pages CDN keep serving the **cached old file** — the deploy succeeds and
the ledger still looks unchanged. The site had also drifted: 83 pages on `v=20260713f`, 5 on
`v=20260720p`. All 88 references across 85 files are now unified on `v=20260727r`.

**Standing rule for any future `data.js` change: bump the token in the same commit.**
