# STC Publish — QA Notes (9 Jul 2026)

Context: publishing the completed stc Group (Saudi Telecom, TADAWUL:7010) study to testahil.com surfaced three findings worth keeping on record. None required re-opening the study itself (Step 0, financials, WACC, MC, QC gate were already complete before this publish) — these are all site-infrastructure findings from the mandatory pre-publish Playwright render check.

## 1. Site-wide bug: `fmtN is not defined` breaks the interactive MC widget on 49 pages

The client-side "Tune the biggest forces yourself" widget's distribution-label code calls `fmtN(FLOOR)` / `fmtN(TARGET)` unconditionally (no `typeof` guard) inside the render() function. `fmtN` is only actually defined on 7 pages (efih, gbco, heli, kabo, lcsw, phdc, prdc). On every other page that uses the widget, this throws a ReferenceError the first time render() runs — which silently aborts the rest of render() before it reaches the percentile table, probability-read stats, zone bar, and touch-ladder population. Net effect: those four elements never populate on page load, and slider/horizon-toggle interactions stop updating anything, on **49 live pages**, including `ribl.html` (last week's publish).

**Fixed on `stc.html` only** (this publish): added
```js
var DEC=S0<30?1:0;
var fmtN=function(v,d){d=(d==null)?DEC:d; return v.toFixed(d);};
```
matching the pattern already used on the 7 working pages. Verified via Playwright: zero page errors, percentile table/zone bar/ladder/probability-read all populate, slider and horizon-toggle interactions confirmed live.

**Not fixed elsewhere** — left `ribl.html` and the other 47 affected pages untouched, since a 49-file sweep is a separate, larger change than "publish STC." Affected list (grep `fmtN(` calls minus `var fmtN=` definitions):

aapl, abuk, acwa, adib, adnocgas, agthia, aldar, alrajhi, aramco, btfh, ccap, comi, efid, egal, emaar, emaardev, emfd, enbd, etel, fab, fwry, gold, hrho, ihc, infy, iqcd, isph, jufo, kakao, lges, maaden, nvda, ocdi, oih, oras, orhd, orwe, qgts, qnb, raya, reliance, ribl, sabic, samsung, silver, snb, tmgh, tmpv, tsla

Fix is mechanical and low-risk (same 2-line pattern already proven on 7 pages) — a good candidate for a dedicated batch-fix pass.

## 2. Site-wide bug: feed.xml hardcoded "EGP"/"جنيه" regardless of ticker currency — fixed

`scripts/generate_feed.js` hardcoded the currency unit in every RSS item description instead of reading the ticker's own `ccy` field, so every non-EGP name (RIBL, STC, ARAMCO, SABIC, SNB, MAADEN, ACWA, ENBD, FAB, IHC, TSLA, AAPL, NVDA, Samsung, Kakao, LGES, Reliance) showed the wrong currency in its feed description. Fixed by adding an AR/EN currency-word lookup keyed on `ccy` (AED/EGP/INR/KRW/QAR/SAR/USD) and regenerating `feed.xml`. Pushed as a follow-up commit (`c344277`) immediately after the STC publish commit. This one **was** fixed everywhere since it lives in one shared script, not per-page markup.

## 3. MC engine v3 — deliberately NOT used for this publish

Commit `74f7fcb` (titled "Adopt MC engine v3...") and a follow-up `b5c4ebf` landed in the repo just before this publish, adding `engine/mc_v3.py` + `engine/market_profiles.py` + validation docs (carry-anchored YZ-HAR-t, pooled-panel CRPS gate). Despite the commit title, the validation doc's own flags section is explicit: *"Adoption not yet executed... Publishing remains a separate explicit step."* Neither commit touches `Standing_Research_Protocol.md`, any live ticker page, or any build script — v3 has zero live references anywhere on the site (verified by grep). Its Saudi MarketProfile specifically flags "SAR risk-free not directly sourced... replace before any Saudi publish." Given STC is a Saudi ticker, and v2 is what all 60+ currently-live pages (including STC's own already-completed study) are built on, this publish kept the existing v2-based numbers. This is a call worth revisiting once v3 adoption is formally executed per its own stated checklist.

## Publish summary

- `stc.html` + `ar/stc.html` added, `TICKERS.STC` + 2 `LEDGER` rows in `data.js`, `COVERAGE_EN/AR` + `SHORT` in `coverage.js`, `HAS_BACKTEST += STC` in `ledger.html`, `calibration_STC.png`, 3 study files, `SITE.latest = STC`, site-wide cache-bust `20260709d → e`.
- Commits: `898a8de` (publish) → `b72d0f4`/`7751876` (CI auto-regen sitemap/feed) → `c344277` (feed currency fix).
