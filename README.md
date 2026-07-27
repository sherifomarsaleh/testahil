# Testahil — concept preview

A working prototype of two product ideas for Testahil, built on top of the Monte Carlo cone work:

1. **Trade Cards** (`/tickers/<SYM>.html`) — entry zone, target, and stop read directly off each ticker's
   MC percentiles, plus a live position-size calculator (portfolio size × max risk % → shares).
2. **Verified Ledger** (`/ledger.html`) — a public win-rate track record with a per-ticker **Trust Meter**
   (rolling % of sessions price closed inside the cone).

`/index.html` is the coverage landing page linking both.

## Status

This branch is a **concept preview**, not the production site. Every page carries a visible "concept
preview" banner and `<meta name="robots" content="noindex, nofollow">`.

> **Do not deploy this branch to GitHub Pages from this repository.** `main` carries a `CNAME` for
> `testahil.com` and is the live production site. A repository serves exactly one Pages site, so any
> Pages deployment from this branch would replace testahil.com. To host this preview, use a separate
> repository (or a separate host) — never this repo's Pages.

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

## Publishing this to GitHub yourself

This folder is already a git repo with one commit (`main` branch). The agent session that built this
could not push it directly — its network access to the GitHub API is restricted to repos explicitly
attached to the session, and no such attachment exists here. To publish it yourself:

```
# 1. Create an empty repo on GitHub (no README/license — this folder already has one), then:
cd testahil-web
git remote add origin https://github.com/<you>/<repo-name>.git
git push -u origin main

# 2. Optional — a live-but-unlisted preview via GitHub Pages:
#    Settings -> Pages -> Deploy from branch -> main -> / (root)
#    (Private-repo Pages needs GitHub Pro/Team/Enterprise; on the free tier, keep the repo private
#    for source control and skip Pages, or make the repo public once the data is real.)
```

Revoke/rotate the token you used while testing this, if you haven't already — it was pasted in plaintext
during the session that built this.
