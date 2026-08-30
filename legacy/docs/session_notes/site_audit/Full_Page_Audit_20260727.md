# Full ticker-page audit — 27 Jul 2026

Triggered by: user screenshot of `rmda.html` showing no Monte Carlo section, plus
"some other pages are simply incomplete. Check all pages and make sure they all
have all the sections."

Shipped on `main` as `36c789e` (structure/cache) and `b78e6fb` (content integrity).

## Method — render, don't read

The markup lies. `rmda.html` *contained* every `sec-*` anchor and every
`<details>`; grepping for section ids returned a perfect page. The fault only
showed under a real parse. So the audit was done by rendering all 75 ticker pages
headless (`file://`, `wait_until='load'` — NOT `networkidle`, which never fires in
this sandbox) and querying the live DOM:

- **nesting depth** of every `details.rds` (count `DETAILS` ancestors) — a section
  at depth ≥1 is invisible until its parent is opened
- **populated-ness** of every JS-filled container (`#gauge`, `#pct`, `#techread`,
  `#level-list`, `#peers`, `#zoom-chart`, `#mc-fan-static svg`, `.mc-ladder tbody`)
- **dangling nav**: every `.secnav a[href^="#"]` resolved against real element ids
- **`pageerror`** capture per page
- **cross-page duplication**: md5 of each `<table>`'s ordered `<td class="num">`
  values; any hash appearing under two different tickers is a clone
- **internal contradiction**: each page's static weighted-central row vs that
  ticker's `fair.base` in `data.js` (the value the on-page gauge renders)

The last two checks are what found the real damage. Neither is visible by reading
one page at a time — a wrong-but-plausible number looks fine in isolation.

## What was wrong

### 1. rmda.html — Monte Carlo buried (the reported bug)

Missing `</details>`: the Lens-3 `<details>` opened inside the still-open Lens-2
`<details>`. The whole MC block (sec-odds, fan, percentiles, drivers) rendered
only after opening "Technical & price structure", and the "The odds" nav entry
pointed into a hidden subtree. The MC block also sat between the Technical lens
header and the price chart, so Technical was headless too.

Fixed by moving the block to sibling level (Fundamental → Technical → Monte Carlo
→ Peers → About, matching all 74 others). Contents untouched.
**Only page in the site with this fault.**

Same page: footer studies list read `<a href="emfd.html">Rameda</a>` — a
find/replace artifact from the page rmda was cloned off. Restored to "Emaar Misr".

### 2. Stale `app.js` cache-buster — sitewide

All 84 pages loaded `assets/app.js?v=20260720a` while `app.js` had been changed
on 27 Jul. Returning visitors kept the cached 20-Jul copy and saw **no** front-end
change, which is why earlier verified pushes read as "still not fixed".
Bumped to `?v=20260727b`. (`data.js` was already correct at `?v=20260727t`.)

**Standing rule worth keeping: bump the query string in the same commit that
changes the asset.** A push can be correct at the git layer and invisible to the
user; verifying the file on `raw.githubusercontent.com` does not prove the browser
will fetch it.

### 3. Five pages published another company's numbers

Clone-and-forget. On four of them the static table contradicted the fair-value
gauge on the same page — the contradiction is what made them findable.

| page | was showing | correct | source |
|---|---|---|---|
| `ihc.html` | Aramco 5-lens → AED 25.04 | **104.5** (SOTP 120 / DCF 81 / rel 102 / norm 91) | IHC study tbl 8 |
| `ihc.html` | Aramco peer table + prose ("IHC is an integrated oil major… world's largest and lowest-cost crude producer") | holdco comparator set | IHC study tbl 21 |
| `salik.html` | e& 4-lens → AED 22.72 | **4.62** (DCF 4.49 / norm 5.44 / rel 4.89 / DDM 3.55) | SALIK study tbl 2 |
| `clho.html` | Rameda lenses → EGP 2.77 | **9.21** (DCF 7.17·40% / rel 13.21·25% / norm 8.37·20% / EV-per-bed 9.08·15%) | CLHO study tbl 2 |
| `jufo.html` | Abu Qir SOTP → EGP 60 | **26.1** (DCF 24.3·40% / rel 28.7·25% / norm 28.7·25% / seg 20.5·10%) | JUFO study tbl 8 |
| `aapl.html` | Tesla peer map (EV manufacturing, humanoid robotics, NACS charging) | mega-cap comps (AAPL 38× fwd P/E on low-single growth vs 31× cohort median) | AAPL study tbl 25 |

Every replacement figure was read out of that company's own study `.docx` in
`files/` via `python-docx` — not reconstructed, not carried across from `data.js`.
CLHO's and JUFO's published weights reproduce their central exactly (9.2065→9.21,
26.12→26.1), an incidental check that the right table was picked up.

**No weight is displayed that isn't in the source document.** IHC and SALIK show
bear–bull spans instead, because their studies give bear/base/bull with no weight
vector. SALIK's weights back-solve cleanly to 35/25/20/20 (→4.6195) and IHC's note
implies 45/15/20/20 (→104.75 vs a published 104.5) — both were **left out**. A
back-solved weight is an inferred number wearing a sourced number's clothes, and
the IHC one doesn't even foot.

Not touched: `data.js`, any `fair{}` value, distributions, the ledger, the study
documents. The studies were always right; only these five page-level summary
tables were wrong. No published forecast was retro-edited.

## Checked and cleared (not bugs)

- `copper.html`, `mfpc.html` — deliberate "Coming soon" stubs, correct as-is
- `deadfilelinks 2/6` on 70 pages — the "Open the source register" buttons;
  confirmed `href="#"` **and** `offsetParent === null` (hidden) where no biblio
  file exists
- `peers-EMPTY` on 47 pages — `#peers` is the EGX-only cross-coverage widget;
  non-EGX pages carry a static comparator table in the same card
- gold/silver/platinum showing 4 accordions not 5 — metals have no peer set
- 44 pages carry a static arena/comparator table; only `aapl`/`ihc` were clones

## Post-fix state (as of this first pass — see update below, this undercounted by one)

- 75/75 pages: 5 accordions at depth 0, MC fan renders, zero JS errors
- 0 pages where the static weighted-central differs from `data.js fair.base` by
  >2% (was 4)
- 0 numeric tables shared between different tickers (was 5)
- 0 dangling nav links, 0 pages missing a section

## Update — later the same day: a 6th clone, and the gate is now permanent

The "Open" item below (make the checks a standing gate, not a one-off sweep) is
done: `scripts/check_page_integrity.py` + `.github/workflows/page-integrity.yml`,
shipped in `44a4554`. Runs on every push/PR touching `**.html` or `data.js`.
**Confirmed actually executing on GitHub Actions** (not just passing locally) —
checked the live run history directly, three runs so far, all Success, SHAs
`03f71fb` / `3358e8b` / `310cbef` matching the commits that triggered them.

Building it caught what this first pass missed: `rmda.html` — the very page this
whole audit started from, already edited once that day for the accordion bug —
was *itself* still carrying Oriental Weavers' lens VALUES under its own row
labels ("FCFE DCF 17.3", "Mid-cycle EBITDA 21.2", "Normalized 21.1"), with only
"Relative multiples" and the weighted total legitimately correct. The whole-table
hash above didn't catch it because only 2 of 5 rows matched orwe.html — a
row-level check (added same commit, kept advisory-only: it also flags 3
legitimate shared-fact rows — gold/silver, emaar/emaardev, emfd/ocdi/orhd — so it
needs a human glance, not a bot verdict) is what surfaced it. Fixed in `03f71fb`,
sourced from RMDA's own study table 8. So "0 numeric tables shared (was 5)" above
should read **was 6**.

Verified against the live site itself, not just the repo: fetched
`testahil.com/rmda.html` directly post-deploy and confirmed the rendered table
now shows FCFF DCF 1.73 / Relative 4.40 / Normalized 3.65 / DDM 1.00 / weighted
2.77 — the correct RMDA-sourced numbers. Note while doing this: a fresh push does
not appear on the live custom domain instantly — two fetches taken within the
propagation window still showed the pre-fix table even though the repo and the
Actions deploy log both already showed the new commit as live. A third fetch a
short while later showed the fix. Treat "pushed" and "confirmed live" as two
separate claims going forward; don't make the second on the strength of the
first.

Real lesson: a whole-page audit can still miss a partial clone on the exact page
it started from, and "deployed successfully" per CI can still lag what a visitor
actually receives for a few minutes. The permanent gate + the practice of
re-fetching the live page (not just the repo) after a push is what closes both
gaps going forward.
