# Testahil — concept preview

A working prototype of two product ideas for Testahil, built on top of the Monte Carlo cone work:

1. **Trade Cards** (`/tickers/<SYM>.html`) — entry zone, target, and stop read directly off each ticker's
   MC percentiles, plus a live position-size calculator (portfolio size × max risk % → shares).
2. **Verified Ledger** (`/ledger.html`) — a public win-rate track record with a per-ticker **Trust Meter**
   (rolling % of sessions price closed inside the cone).

`/index.html` is the coverage landing page linking both.

## Status

This is a **staging/concept repo**, not the production site. `testahil.com` currently runs on GoDaddy
WebsiteBuilder (no git backing), so nothing here is wired to that domain. Every page carries a visible
"concept preview" banner and `<meta name="robots" content="noindex, nofollow">` so it won't get indexed if
it's ever made public.

**All data is illustrative / sample data** — ticker percentiles, calls, and trust scores are invented for
the prototype, not real MC output or a real trading record. Do not treat any figure on this site as a live
signal.

## Wiring this to real data

Everything reads from one file: [`assets/data.js`](assets/data.js).

- `TESTAHIL_TICKERS` — per-ticker current price, daily % change, and the P10/P15/P30/median/P75/P90
  30-day percentiles from your MC engine. `TESTAHIL_TICKER_ORDER` controls coverage-grid and nav order.
- `TESTAHIL_CALLS` — the ledger's source of truth: `{ticker, date, entry, horizon, pct, status, r}` per
  logged call (`status` is `hit` / `open` / `stopped`). Every stat tile, the table, and the equity curve
  in `ledger.html` are computed from this array — nothing is hardcoded.
- `TESTAHIL_TRUST` — `{ticker, accuracy}` per name, where `accuracy` is your rolling "% of sessions price
  closed inside the cone" figure. Drives the Trust Meter bar and its High/Medium/Low Reliability label.

To add a covered ticker: add a key to `TESTAHIL_TICKERS` and to `TESTAHIL_TICKER_ORDER`, then run:

```
node build-tickers.js
```

which regenerates `/tickers/<SYM>.html` for every ticker in the data file.

## Structure

```
index.html            coverage landing page
ledger.html            verified ledger + trust meter
tickers/<SYM>.html      one trade card per covered ticker (generated — see build-tickers.js)
assets/tokens.css       shared design tokens (palette, nav, page shell)
assets/data.js          the single source of truth for all pages
assets/trade-card.{css,js}
assets/ledger.{css,js}
build-tickers.js        regenerates tickers/*.html from data.js
```

No build step is required to view the site — open `index.html` in a browser, or serve the folder with any
static file server (everything is plain HTML/CSS/vanilla JS, no framework, no bundler).
