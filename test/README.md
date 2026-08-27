# testahil.com/test/ — the proposed structure, working

A complete, functional build of the new information architecture. Ten nav items become five;
the four simulation tools merge into one workspace; every instrument gets one canonical page.

## Deploy
Copy the `test/` folder to the repo root and push — it becomes `testahil.com/test/`.
Nothing outside `test/` is touched. All pages carry `noindex`.

It references the LIVE site's own files relatively:
- `../assets/style.css` — base tokens/typography (dark mode included)
- `../assets/data.js` — every number on these pages (spot, cones, touch ladders, bands, ledger, calc series)
- `../files/…` — study PDF/XLSX downloads
- `../{ticker}.html` — "full narrative study" links back to current pages

So the test site tracks live data automatically: publish a study, and /test/ updates itself.

## Pages
- `index.html` — search-first home; latest study card (reads SITE.latest); live tally strip
- `coverage.html` — stocks + metals merged, filter chips per market, sortable, search
- `study.html?t=PHDC` — canonical per-name page: at-a-glance (the old -3lenses summary),
  three lenses, odds buckets, touch ladder, own band record, downloads, editions note
- `tools.html` — one workspace, four tabs (#screener #compare #odds #portfolio);
  odds math (invCDF/probAbove/buckets) ported from trade.html; portfolio uses the same
  ρ_same=0.55 / ρ_cross=0.25 factor model on seeded draws
- `savings.html` — the calculator, renamed, real/nominal per vehicle from CALC series
- `record.html` — tally first (from BANDS/BAND_MARKETS), live ledger pending + graded, rules collapsed
- `method.html` — lenses, self-testing, open models, disclaimer as anchored sections

## If this structure goes live at root
1. Rename pages up one level (coverage/tools/savings/record/method), keep this shell.
2. 301s: stocks.html + metals.html → coverage.html · picker.html + compare.html +
   trade.html + portfolio.html → tools.html (#tab anchors) · calculator.html → savings.html ·
   ledger.html → record.html · archive.html → method.html#open · news.html → index.html ·
   every `{ticker}-3lenses.html` → `{ticker}.html`
3. Per-ticker pages: add the at-a-glance strip at top (as study.html shows), retire the -3lenses twins.
4. Remove the TEST PREVIEW badge (`.t-testflag` in assets/test.css).

## Not in this build (deliberately)
- The 93 hand-written narrative studies stay on their current pages (linked from each study.html);
  merging the at-a-glance strip into them is a build-pipeline change, listed above.
- Arabic (`ar/`) mirror.

## SEO at go-live (prepared, not active — /test/ is noindex)
When this structure becomes the main site:
1. Remove <meta name="robots" content="noindex"> from all shells + flat pages.
2. Per-study <head>: canonical URL, meta description from the name's verdict line,
   OG/Twitter cards (og-image.png), and FAQPage JSON-LD — regenerate from the
   per-ticker Q&A in test/assets/prose/{KEY}.json (FAQ panel).
3. Point the "Generate SEO surfaces" workflow at the new URLs (sitemap entries for
   /{T}/study|3lens|calibration|archive/), 301 map per this README.
4. One canonical per name: the study page; 3lens/calibration/archive reference it.
