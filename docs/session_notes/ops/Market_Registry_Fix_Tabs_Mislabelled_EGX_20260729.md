# Market registry fix — 34 international names were rendering under EGX (29 Jul 2026)

## The defect

The ledger tab bar decided a stock's market by reading `asset_class` off the first
LEDGER row it encountered for that name:

```js
LEDGER.forEach(r=>{ if(!(r.instrument in classOf)) classOf[r.instrument]=r.asset_class; });
equity -> "EGX"      other -> "International markets"      metal -> "Metals"
```

That overloaded a genuine asset-class field to also carry a market flag. It worked
only while every non-Egyptian equity sat mislabelled as `other` — Aramco, Emaar and
Apple were all filed as "other" rather than "equity".

Two commits knocked the prop out:

1. **28-Jul market-wide re-strike** wrote the semantically *correct* value on the new
   rows — Aramco IS an equity — so the fresh UAE/Tadawul/US/India/Qatar rows carried
   `asset_class:"equity"`.
2. **29-Jul cleanup (`e32df4cf`, 304→161)** deleted the older `other`-tagged rows that
   had been determining `classOf`.

Result: `classOf` fell through to `equity` for **34 names**, all of which rendered
under the **EGX** heading — all 18 UAE, all 11 Tadawul, AAPL/NVDA/TSLA, INFY/RELIANCE,
QGTS. "International markets" was left with 5 names (QNB, Samsung, Kakao, LGES, TMPV).

Nothing threw. No console error. The page rendered cleanly and was simply wrong —
only a human reading the tab bar could catch it. `TMPV` was additionally carrying two
different `asset_class` values across its surviving rows.

## The fix

**Market is decided by FILE PLACEMENT**, `engine/raw_ohlc/{MARKET}/{TICKER}.csv` —
which the standing protocol already mandates for the unattended pipeline. Extended it
to the site.

- **`engine/build_market_registry.py`** (new) scans the library tree and emits
  **`assets/markets.js`** — `MARKET_OF` (ticker→market), `MARKET_META` (label, group),
  `MARKET_ORDER`. Generated, never hand-edited.
- Eight aliases cover the stem↔site-name mismatches: `AE/TWOPOINTZERO`→`2POINTZERO`,
  `AE/ADIB`→`ADIBUAE` (distinct from `EG/ADIB` = ADIB-Egypt, same stem, two banks),
  `SA/RAJHI`→`ALRAJHI`, `KR/KAKAO`→`Kakao`, `KR/SAMSUNG`→`Samsung`, `XAU/GOLD`→`Gold`,
  `XAU/SILVER`→`Silver`, `XPT/PLATINUM`→`XPTUSD`. A stem needing an alias and lacking
  one fails the coverage assert rather than being silently dropped.
- `ledger.html` groups tabs from the registry. `asset_class` now means asset class and
  nothing else; it can no longer decide what country a stock trades in.
- **Fail loud, not into EGX:** any ticker with no registry entry renders in a visible
  "⚠ Unplaced — no market library" group and logs a console warning, instead of
  defaulting into someone else's market. This is the check that would have caught the
  original defect on the page itself.

## Verification

- `python3 engine/build_market_registry.py --write` — **74 libraries scanned, 74 LEDGER
  instruments, zero missing, zero unmapped**. Counted against a known total, not a
  tool's own "0 skipped".
- Emitted `markets.js` checked by `node --check` **and by IMPORT** (74 tickers, 9 markets).
- `ledger.html` rendered headlessly in Chromium: **no JS exceptions**; EGX = exactly 30
  Egyptian names; zero international names leaking into EGX (checked against an explicit
  16-name probe list); no "Unplaced" group; 74 tabs total.

Groups as rendered: EGX — Egypt (30) · UAE — ADX & DFM (18) · Saudi Arabia — Tadawul (11)
· Qatar — QSE (3) · India — NSE (3) · South Korea — KOSPI (3) · United States (3) ·
Metals (3).

## Standing rules this adds

1. **Never infer a stock's market from `asset_class`, currency, or any field that exists
   for another purpose.** Market comes from the library registry.
2. **A classification fallback must be visible.** Any grouping that can silently default
   a name into a wrong bucket needs an explicit unplaced bucket instead.
3. **A rendered page is part of verification.** `node --check` and an import test both
   passed on the broken code — only rendering the tab bar and reading it caught this.

## Status

Local only. Nothing pushed; the live site still shows the mislabelling. Publishing
needs a fresh PAT at the moment of the push, per the standing git/publish mechanics.
Still open from the same commit: the EMAAR 1-month cohort (anchor 29-Jun @ 12.14 AED,
`grade_date` 2026-07-29) deleted while inside its final window — see
`claude/ops/Ledger_Cleanup_Audit_and_Due_Ordering_20260729.md`.
