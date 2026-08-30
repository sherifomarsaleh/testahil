# Ledger cleanup audit + due-date ordering — 29 Jul 2026

## 1. What the 304 → 161 cleanup actually removed (verified by import, not by parse)

Loaded `assets/data.js` at `e32df4cf~1` and at `e32df4cf` in node, keyed every row
on `(instrument, horizon_label, anchor_date)`, and diffed the two LEDGER arrays.

| check | result |
|---|---|
| LEDGER rows before / after | 304 / 161 |
| distinct keys removed | 139 (the commit message's 143 counts 4 duplicate-key rows that also collapsed) |
| duplicate keys before / after | 4 (OCDI 1M+3M, ORHD 1M+3M, all anchored 2026-07-27) / 0 |
| **already-graded rows lost** | **0** — 11 graded before, 11 graded after. The scored record is intact. |
| superseded open strikes removed (a newer strike of the same name+horizon survives) | 138 — legitimate under the v3 lifecycle |
| removed rows with no surviving newer strike | 0 |
| **open rows removed that were AT or PAST their check date** | **1 — see below** |

## 2. The one real loss: EMAAR 1-month, due to be graded 29-Jul-2026

```
instrument      EMAAR
horizon_label   1 month
anchor_date     2026-06-29     anchor_price 12.14 AED
grade_date      2026-07-29     <-- today; it was one day from maturity
cycle_no        1              p5 9.98 | p25 11.22 | p50 12.18 | p75 13.22 | p95 14.86
realized_close  null           (deleted before it could be graded)
```

It was swept up with the 138 genuinely-superseded strikes because a newer EMAAR 1M
(anchor 2026-07-24, check 2026-08-24) exists — but supersession is not the test that
matters for a row this close to maturity. A cohort one day from grading is a
**gradeable window**, and the whole point of the v3 lifecycle adoption was to stop
losing those (the pre-adoption record was 11 graded 1M and 0 graded 3M precisely
because re-strikes kept killing cohorts before maturity). The cleanup that adopted
the fix destroyed a 12th window on its way in.

Secondary flag: the deleted row carried `asset_class:"other"` while the surviving
24-Jul EMAAR rows carry `asset_class:"equity"` — the same name was tabbed into two
different asset classes.

**Standing rule this implies (proposed):** the supersession test for deletion must
exclude any row whose `grade_date` falls on or before the deletion date. Grade it
first, then supersede it. Never delete an open row inside its final window.

## 3. Ledger ordering — retired key and its replacement

The ledger's own question is "what do I have to deal with next", so the table is now
an **action queue**, not a publication feed:

1. Still-open rows first, **soonest check date at the top** — overdue and due-today
   lead, then tomorrow, then the day after.
2. Already-graded rows fall to the **bottom** (nothing to do to them), most recently
   resolved first.
3. Ties: same check date → instrument A–Z → near horizon before far.

Retired key: `grade_date` ascending across open *and* graded rows together, which put
the oldest finished rows — the ones needing no action at all — at the very top of
page 1. Changed in `ledger.html` `buildPanel()`; applies to the All tab and every
per-stock tab. Verified: 161 rows in, 161 out; open block strictly ascending; graded
block strictly descending; no row leaks between blocks; `2POINTZERO` survives the
load (quoted key); lifecycle invariant holds — 150 open rows across 150 distinct
`(instrument, horizon)` pairs, zero pairs with more than one open anchor.

## 4. Next data-update date, per stock (as of 29-Jul-2026)

| date | in | names |
|---|---|---|
| 2026-08-03 | 5d | Silver |
| 2026-08-05 | 7d | QNB |
| 2026-08-20 | 22d | XPTUSD |
| 2026-08-23 | 25d | 26 EGX names — ABUK, ADIB, BTFH, CCAP, CLHO, DSCW, EFID, EFIH, EGAL, ETEL, FWRY, GBCO, HELI, HRHO, ISPH, JUFO, KABO, LCSW, OIH, ORAS, ORWE, PHDC, PRDC, RAYA, RMDA, TMGH |
| 2026-08-24 | 26d | 18 UAE names — 2POINTZERO, ADCB, ADIBUAE, ADNOCGAS, AGTHIA, ALDAR, ALPHADHABI, BURJEEL, DEWA, DIB, EAND, EMAAR, EMAARDEV, ENBD, FAB, IHC, LULU, SALIK |
| 2026-08-26 | 28d | 11 Tadawul names — ACWA, ALINMA, ALRAJHI, ARAMCO, ELM, EXTRA, MAADEN, RIBL, SABIC, SNB, STC |
| 2026-08-27 | 29d | AAPL, Gold, NVDA, OCDI, ORHD, Samsung, TSLA |
| 2026-08-28 | 30d | INFY, Kakao, LGES, RELIANCE, TMPV |
| 2026-08-30 | 32d | COMI, EMFD, IQCD, QGTS |

Nothing is due today or overdue in the ledger *after* the EMAAR row was deleted —
before the deletion, EMAAR 1M was the one item due 29-Jul.

## 5. Library staleness (separate from the grade clock)

Days between the last session in each library and today:

- **QNB, IQCD, QGTS — 24 days** (library last session 2026-07-05). Worst on the board.
- 26 EGX names — 7–8 days (2026-07-21/22).
- UAE — 5 days; Tadawul — 3 days; US/KR/IN — 1–2 days.

Nine tickers carry **no `asof` block at all** (AAPL, INFY, KAKAO, LGES, NVDA,
RELIANCE, SAMSUNG, TMPV, TSLA) — they fall back to a free-text `spotDate`
("close 27 Jul 2026") rather than an ISO date, so they cannot self-report staleness
through the stamp the way the protocol assumes. Worth closing.

## 6. Status

Local only. Nothing pushed — the live `testahil.com/ledger.html` is unchanged and
still carries the retired ordering. Publishing needs a fresh PAT supplied at the
moment of the push, per the standing git/publish mechanics.
