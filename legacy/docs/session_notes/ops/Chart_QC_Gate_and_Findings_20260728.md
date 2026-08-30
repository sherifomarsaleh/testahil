# Chart QC gate + what it found — 28-Jul-2026

Triggered by one reported defect: COMI's cone apex sat above the start of its price line. Investigating it surfaced a second failure that was completely silent and much larger. Shipped as `755e91c`; the plotting work it builds on is `4c7a37d`.

## The silent failure — all 11 Saudi charts were drawing nothing

`drawActualLine`'s CSV parser extracted only quoted (`"..."`) fields. Every EG/AE/KR/US/IN/QA/XAU/XPT export is quoted; **all 11 Tadawul exports are not.** On an unquoted file the parser returned zero rows, and the function then bailed on `if(!series.length) return` — so every Saudi cohort chart fell back to endpoints-only, with no error logged anywhere and nothing visibly wrong on the page.

`splitRow` now handles both shapes: quoted-group extraction when the row is quoted (that is what protects a thousands comma sitting *inside* a field — Gold `"4,090.87"`, LGES `"314,000"`), plain split otherwise. Verified safe before adopting: every row of all 11 unquoted files splits to exactly 7 fields, i.e. those exports carry no embedded commas, which is precisely why the vendor omitted the quotes. RAJHI now parses **3,881 rows where it parsed 0**; Gold and LGES still parse correctly.

**Standing lesson: a parser that returns an empty series and a caller that returns early on empty is a silent failure by construction.** Three separate ways the full-path rule was being violated — a missing map entry, an unparseable file, a mismatched anchor — and none of them announced itself. That is what the gate is for.

## The gate — `qc_charts.js`

Run before any publish that touches `assets/data.js`, `ledger.html`, or `engine/raw_ohlc/`. Exits non-zero on FAIL.

```
node qc_charts.js
```

| # | Check | Result |
|---|---|---|
| 1 | every ledger instrument has a `COHORT_OHLC` entry | PASS 74/74 |
| 2 | every mapped file exists and parses to a non-empty series | PASS 74/74 |
| 3 | mapped market directory agrees with the ledger `ccy` | PASS 74/74 |
| 4 | each cohort anchor is a real trading session in its own library | **1 FAIL** |
| 5 | published `anchor_price` agrees with that date's close | **2 FAIL**, 14 warn |
| 6 | every graded cohort has a full path, not just endpoints | PASS |

Check 3 is the ADIB/EGX vs ADIBUAE/ADX guard — same filename, different exchange, prices off by 2×. Checks 1/2/3/6 passing is the machine-checkable statement that the standing full-path-plotting rule actually holds, rather than an assertion that it does.

## What it flags — data defects, deliberately NOT auto-corrected

These are published forecasts. The ledger is append-only and the percentiles were struck off the published anchors, so silently re-writing an anchor would trade a *visible* defect for a *hidden* inconsistency — a row whose cone no longer follows from its own stated anchor. Left for an explicit decision:

| Instrument | Issue |
|---|---|
| **HELI** | anchored 2026-07-03 — a **Friday**, EGX closed. Not a trading session at all. |
| **LCSW** | 2026-07-06: published 29.45 vs tape 30.10 (**+2.21%**) |
| **COMI** | 2026-06-29: published 129.25 vs tape 126.89 (**−1.83%**) — the reported one |

Plus 14 sub-1% warnings (DSCW, RIBL, ISPH, SABIC, KABO, PHDC, TMGH ×2, ARAMCO, MAADEN, ACWA, PRDC, ALINMA, ELM), mostly rounding-scale. Note most of the Saudi entries only became visible *after* the parser fix — before it, those files parsed to zero rows and check 5 had nothing to compare.

**The chart was never wrong about COMI.** It was correctly reporting that the published anchor 129.25 does not appear anywhere in COMI's 15-year library — not as a close, open, high or low, on any day. The rendering is faithful; the data underneath it is not.

## Options for the three FAILs

1. **Accept and annotate** — keep the published anchors (append-only intact) and add a chart footnote wherever published and tape differ by >1%, so a reader sees an explained discrepancy rather than an apparent rendering bug.
2. **Re-strike the affected cohorts** — recompute percentiles from the true anchor and supersede in place, as was done for the 28-Jul intraday-bar correction. Honest, but it discards three live forecasts.
3. **Investigate provenance first** — all three are EGX/Tadawul names anchored in a narrow window; a common capture path (a different vendor snapshot at publish time) is the likeliest root cause, and finding it would prevent recurrence rather than patch instances.

Recommendation: **3, then 1.** Root-cause first, because a fix that does not explain how 129.25 was captured will not stop the next one; annotate in the meantime so the page stops looking broken.

## Maintenance obligation

When a new name is covered, add it to `COHORT_OHLC_PATH` in `ledger.html` **in the same change** that adds its ledger rows, then run `node qc_charts.js`. A name that reaches the ledger without a path entry silently degrades to an endpoint-only chart — now a gate failure, not a default.
