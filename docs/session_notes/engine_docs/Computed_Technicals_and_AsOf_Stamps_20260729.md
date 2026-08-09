# Computed Technical Read + As-Of Stamps — 29 Jul 2026

**Status: built, verified, committed LOCALLY on `feature/computed-technicals-and-asof-stamps`
(`c2f3e52` pilot, `fcee684` fan-out). NOT pushed — needs a fresh PAT and a PR.**

Adopted at Sherif's instruction, 29-Jul-2026. Retires the standing roll-forward carve-out that
said the technical block "needs a fresh chart read" and must be left alone.

## 1. Why the old rule had to go

The carve-out was written to protect a hand-authored judgement. In practice it protected
staleness, and the evidence was on live pages:

| name | what the live page said | reality |
|---|---|---|
| COMI | narrative: "the price closed **129.25** below a falling 20-day"; all 3 resistances 129.50–135.15 | spot 142.00 — every published resistance sat *below* spot |
| SAMSUNG | supports 334,675 / 320,000 / 286,320 | spot 254,000 — all three "supports" sat *above* spot |

A block that is never refreshed is not a preserved judgement. It is an unmarked expiry date.

## 2. What was built

**`engine/technicals.py`** — deterministic technical read, computed from the same persistent
OHLC library the MC engine runs on, through the same Step 0.0 data-quality gate. Nothing is
fitted or forecast; every number is a closed-form function of the cleaned series.

- SMA 20/50/200 with a slope state (rising / falling / flat over 10 sessions, ±0.30% band)
- Wilder RSI(14) and Wilder ATR(14) on the true range — gap-aware, not a plain high-low
- MACD(12,26,9) on proper EMAs, reported as **line sign AND histogram sign separately** (a
  MACD below zero with a positive histogram is falling momentum that has begun to turn, not
  "positive MACD")
- 50/200 cross recency — a cross inside 25 sessions is called fresh and leads the trend line
- 52-week range and distance from each extreme
- S/R from fractal pivots (half-width 5) over ~500 sessions, clustered at 1.5% and weighted
  by touch count × exponential recency (180-session half-life). Moving averages, the 52-week
  extremes and round numbers are admitted as candidates but score strictly below real swing
  structure — they only win a slot when structure does not fill one. Levels inside 0.8% of
  the close are rejected as indistinguishable from spot.
- Prose is templated: every clause is selected by a computed number.

**`engine/apply_technicals.py`** — surgical writer, same spirit as `apply_rollforward.py`.
Rewrites ONLY `levels`, `tech` and the new `asof`. `spot`, `spotDate`, `dist`, `hz`, `touch`,
`fair{}`, the slider constants and `files` are left byte-identical. **It never re-strikes a
cone** — it reads the published cone's anchor date off the newest LEDGER row and its run date
off that row's own note, and stamps them.

**`assets/app.js`** — renders both stamps from `asof`. Hooked into `renderStaticFan`, the one
function all 74 ticker pages already call, and deferred to `DOMContentLoaded` because each
page's technical read is written by its own inline script. No page template was edited; a new
page inherits the stamps automatically.

## 3. Two dates, never one

```
asof: { mc:   { data:"2026-07-28", computed:"2026-07-28" },
        tech: { data:"2026-07-28", computed:"2026-07-29" } }
```

`data` = last session the block was built on. `computed` = the day it was run. A single
"as of" cannot distinguish a block recomputed today on last week's prices from one recomputed
last week — which is exactly the failure being closed.

Renders as: `price data through 28 Jul 2026 · read computed 29 Jul 2026`.

## 4. Deliberate behaviour changes

1. **R1/S1 now always mean NEAREST to the close.** The retired hand-authored levels were
   inconsistent (TSLA ascending, COMI descending), so R1 meant different things on different
   pages.
2. **The fundamental sentence is gone from the technical block.** Some retired narratives
   closed with a valuation claim ("the equity case rests on a ~30% ROE against a ~24% cost of
   equity"). A deterministic module cannot source that, so it does not assert it. If that
   context is wanted back, the clean way is an optional human `tech_note` field that survives
   refreshes and carries its own date — considered and not taken on 29-Jul.

## 5. What the stamps immediately exposed

This is the point of them.

- **2POINTZERO — a genuinely stale cone.** Published anchor 03 Jul, page spot 2.16, on a
  library that runs to 24 Jul with a 2.06 close: a 4.6% gap. Its two stamps now disagree in
  public (MC "through 3 Jul", read "through 24 Jul") instead of the gap sitting invisible.
  **NOT reconciled** — re-striking a published cone is a roll-forward decision, never a side
  effect of a technicals pass. **OPEN.**
- **Library freshness across the site**, now visible on every page: TMPV and TSLA end 30 Jun;
  QSE (IQCD, QNB, QGTS) 05 Jul; US (AAPL, NVDA, RELIANCE, INFY) 06 Jul; SILVER 03 Jul;
  PLATINUM 20 Jul. Only COMI, EMFD, KAKAO and LGES reach 28 Jul.
- Every other name's page spot agrees with its library close to within 0.5%.

## 6. Bugs found and fixed during the build

- **`top_level_blocks` matched unquoted object keys only.** `"2POINTZERO"` *must* be quoted —
  a JS identifier cannot start with a digit — so it was silently skipped on the first pass,
  which reported "73 rewritten, 0 skipped" and no error. The count against the site's own key
  list is what caught it. Now matches optionally-quoted keys.
- **The brace matcher read apostrophes in prose comments as string opens** ("EG's own
  calendar") and swallowed the rest of the file. Now comment-aware as well as string-aware.
- Degenerate one-level bull/bear sentences ("above 144.63 … open the 144.63 zone") and the
  awkward double clause ("…, on a rising 200-day, on a fresh golden-cross") both fixed.

## 7. Verification performed

- `technicals.py` and `apply_technicals.py` both **imported**, not merely parsed — the
  standing VERIFY-BY-IMPORT rule.
- `node --check` clean on `assets/data.js` and `assets/app.js`.
- `data.js` **loaded** in node and asserted on the parsed objects: 74 entries, every one
  carrying `asof.mc` and `asof.tech`, exactly 3 resistances and 3 supports each, every
  resistance above and every support below its own library close, ordering nearest-first on
  both sides.
- **Idempotency**: re-running the writer reproduced byte-identical `levels`/`tech`/`asof` for
  every name already written.
- 8 pages rendered headless across all markets (comi, 2pointzero, tsla, gold, samsung,
  aramco, emaar, tmpv) — 2 stamps each, zero console errors.
- Cache-buster bumped to `20260729a` across 87 files for **both** `data.js` and `app.js`
  (app.js changed, so the data.js token alone would not have been enough). Confirmed the
  token was unused before choosing it.

## 8. Open after this session

1. **Push and PR** — nothing has left the machine. Engine changes go on a feature branch with
   an open PR per standing rule; needs a fresh PAT at the moment of the write.
2. **2POINTZERO's stale cone** (item 5 above) — wants a STEP 4 roll-forward, not a patch.
3. **Stale libraries** — TMPV/TSLA (30 Jun), QSE (05 Jul), US (06 Jul), SILVER (03 Jul). Now
   self-reporting on every page, so this is visible rather than latent.
4. The project instruction block still carries the retired "never touch technicals" clause in
   its ROLL-FORWARD section. Replacement text was drafted and handed over 29-Jul; the block
   itself is maintained outside this repo.
