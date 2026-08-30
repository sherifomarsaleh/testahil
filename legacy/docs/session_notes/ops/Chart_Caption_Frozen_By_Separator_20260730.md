# The chart caption froze because it required `&middot;` — 30-Jul-2026

**PR #45**, merged to main as `b5097da`. Gate green: 0 failures, 4 known warnings.
Found by Sherif on dscw.html: the chart read *"last 500 sessions to 19 Jul 2026"* while the
technical read beside it read *"price data through 22 Jul 2026"*.

## Root cause

`ta_chart.py` regenerates the `<svg id="ta-chart-svg">` block. The caption lives in the
`<figcaption>` **outside** that block, so it is a second, separate substitution — and that
substitution required the caption's separator to be the HTML entity `&middot;`.

- **66 pages** write it that way → caption updates.
- **8 pages** write a literal `·` (U+00B7) → the pattern never matched, so the caption froze
  at whatever date it was last hand-authored while the chart above it kept regenerating.

| page | caption said | chart actually on | stale by |
|---|---|---|---|
| phdc.html | 17 Jun | 22 Jul | **35 days** |
| efih.html | 1 Jul | 22 Jul | 21 days |
| heli.html | 1 Jul | 22 Jul | 21 days |
| gbco.html | 7 Jul | 22 Jul | 15 days |
| lcsw.html | 6 Jul | 21 Jul | 15 days |
| dscw.html | 19 Jul | 22 Jul | 3 days |

## Why nothing caught it

`check_ta_chart_overlay.js` only tests that level lines land inside the viewBox — **a caption
is not a line**. And `ta_chart` reported these pages as *"chart block not replaced"*, the
identical message it gives a page that is already current, so a silent failure was
indistinguishable from success. `caption_updated` was recorded in the run report and read by
nothing.

This is the same shape as the 29-Jul stamp regression: a tool that cannot reach its target
reporting success.

## Fixes

1. Pattern accepts either separator and **preserves whichever the page already uses**, so the
   66 correct pages are untouched rather than churned.
2. `ta_chart` now distinguishes *"already current (chart and caption both match)"* from
   *"CAPTION PATTERN DID NOT MATCH — caption left stale next to a regenerated chart"*.
3. `check_data_freshness` fails when a page's caption names a different session from the read
   it labels. **Negative-controlled**: reverting dscw.html and phdc.html reproduces exactly
   two FAILs naming both pages and both dates.

## Checked and NOT a defect: the DSCW Monte Carlo stamp

*"price data through 22 Jul 2026 · simulation computed 28 Jul 2026"* is correct. The ledger
row carries `anchor_date 2026-07-22`, `anchor_price 1.96`, `run_date 2026-07-28`, and the
strike was the 28-Jul market-wide EG/AE/SA re-strike. EG's profile gained
`width_overlay_active` on 29-Jul, one day after — but the overlay is history-gated at
`MIN_WINDOWS=28` and `live_width_mult` returns exactly **1.0** for DSCW, COMI, PHDC and TMGH,
so it is a true no-op today and the 28-Jul cone is still what the engine would produce. **The
two dates differing is the stamp working, not a fault.**

## Due-date correction

A library moving is **not** a trigger to re-strike — strikes happen when a cohort matures, on
the monthly rhythm. Against the live ledger as at 30-Jul:

- **Due now:** TMPV 1-month, 30 Jul.
- **Next:** Silver 3 Aug · QNB 5 Aug · XPTUSD 20 Aug · ORAS 23 Aug · AAPL/NVDA/TSLA/Samsung 27 Aug.

So ORAS and QNB do **not** need rolling forward, and the platinum and US price files are not
urgent — they need to be in place before 20 and 27 Aug. Earlier guidance in this project that
listed them as immediate next actions was wrong.

## Still open

- **TMPV** — grade on today's (30 Jul) close.
- **Silver** — page publishes a cone centred **57.38** resolving 28 Aug; the ledger holds a
  different forecast centred **63** graded 3 Aug. The page's version is in no ledger row and
  will never be graded. Either write the ledger rows for the 28-Jul strike or put the page
  back on the 3-Jul one. SAMSUNG has the same shape one day apart.
- ORAS and QNB cones lag their refreshed libraries (warnings, not failures).
