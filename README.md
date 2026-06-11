# testahil — Phase 1 (static site)

Zero backend. Zero recurring cost. Deploys anywhere static files are served.

## Deploy (pick one, ~10 minutes)
1. **GitHub Pages**: new repo → upload this folder → Settings → Pages → deploy from branch.
2. **Netlify / Vercel / Cloudflare Pages**: drag-and-drop the folder. Done.
3. Point your domain (testahil.com or .net — check availability) via CNAME.

## Before public launch (one-time)
- [ ] Drop the two PHDC files into `/files/` (names must match `assets/data.js`).
- [ ] **Verify CALC series** in `assets/data.js` (USD/EGP, gold 21k, EGX30, CD rates, CPI — sources: CBE, CAPMAS, EGX). Then set `verified: true` to remove the warning banner.
- [ ] Replace `attack@testahil.com` in `models.html` with your real email.
- [ ] Open every page locally and click everything once.

## Weekly ritual (target: ≤ half a day, all in ONE file: `assets/data.js`)
1. Rerun the Monte Carlo → update `dist`, `touch`, `spot`, `spotDate`, `SITE.updated`.
2. Append the new forecasts as rows in `LEDGER`.
3. On resolve dates: fill `realized`, set `status:"scored"`. Never delete a row.
4. Drop new study/model files in `/files/`, update paths.
5. Commit + push. Site updates itself.

## Structure
```
index.html        home: hero + live PHDC strip + pillars
phdc.html         distributions, touch odds, levels, downloads
calculator.html   real-return calculator (CDs/USD/gold/EGX30, CPI-deflated)
ledger.html       public forecast record (the moat)
models.html       open Excel downloads + attack-my-model
method.html       methodology + full Arabic disclaimer
assets/data.js    ← the only file you edit weekly
assets/app.js     strip renderer, ledger, calculator logic
assets/style.css  design tokens (teal house palette, Alexandria/Plex Arabic)
files/            study + model downloads
```

## Phase 2 (later, when audience exists)
- Beat the Model game (needs accounts → Supabase free tier or similar)
- Telegram bot teaser → site
- English toggle
- More tickers: duplicate `phdc.html`, add a `TICKERS` entry.

<!-- deploy refresh 2026-06-11 22:20 -->
