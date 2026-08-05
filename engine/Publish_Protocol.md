# TESTAHIL — Publish Protocol (v1, 05-Aug-2026)

How a completed study becomes a live ticker page + a ledger cohort. Companion to
`Rollforward_and_Grading_Protocol.md` (which governs what happens to that cohort
afterwards) and to the PUBLISHING block in `PROJECT_INSTRUCTIONS_11-07-2026.md`.

Publishing is a SEPARATE, EXPLICITLY-REQUESTED step. Running a study never
publishes it; a study is delivered as files and sits until publication is asked
for by name. (The one carve-out is the matured-cohort auto-publish in the
roll-forward protocol.)

---

## THE STANDING PROMPT

This is the canonical instruction. Keep this file and the prompt in sync — if you
edit one, edit the other in the same commit.

```
Publish [TICKER] to the website and update the ledger — standard workflow, no exploration:
•	Clone the most recently published ticker's page + data.js/coverage.js/ledger.html entries as the
	template. Adapt the numbers; don't rebuild structure from scratch.
•	Reuse every figure already sitting in study_numbers.json / docx_ctx.json (percentiles, touch ladder,
	drivers). Don't re-run the engine or re-derive stats that already exist.
•	Publish the calibration record too, not just the forecast:
	– place engine/raw_ohlc/{MKT}/{TICKER}.csv, then generate assets/calibration_{TICKER}.png
	  (cd engine && python3 metal_backtest.py {TICKER})
	– register the ticker in BOTH ledger.html sets: HAS_BACKTEST and the raw-CSV map
	– append cycle-1 LEDGER rows for 1M and 3M — frozen p5–p95 plus the touch ladder at
	  ±5/10/15/20% and −5/−10%, read off the study's existing path arrays; don't re-simulate
	– record the verdict in the ledger comment header (skill, CI, block-robustness). Set the row's
	  `cal` field ONLY for matches / untested / fail — absent means PASS.
•	Regenerate all four generated surfaces — none of them are hand-edited, and a missed one fails
	silently rather than loudly:
	1. sitemap + homepage footer strip   node scripts/generate_seo.js
	2. feed                              node scripts/generate_feed.js
	3. market registry (exchange group)  python3 scripts/build_market_registry.py --write
	4. page chart + technical read       python3 engine/ta_chart.py --only {TICKER} --write
	                                     python3 engine/apply_technicals.py --only {TICKER} --write
	(4 runs last — it rewrites the ticker's own data.js block, so the entry and page must exist first.)
•	Verify by render, not by grep: load the ticker page and ledger.html headless and confirm the ticker
	appears under its own exchange group. Then scripts/check_data_freshness.py and
	scripts/check_page_integrity.py — both clean before you commit.
•	If any automated check (materiality gate, etc.) flags something, check in one step whether it's
	actually about this ticker. If it's pre-existing and unrelated, proceed and just note it in passing —
	don't investigate further. A red X on the calibration workflow is its designed behaviour (it fails the
	run so a material change can't be mistaken for a clean one), not a break.
•	Size any illustrative/interactive values (slider impacts, etc.) with a quick reasonable estimate.
	Don't build a fresh financial model to calibrate them precisely.
•	Build everything, commit, then ask me for the token once, right before the push. Don't ask twice,
	don't re-litigate after I give it.
•	Report back in a short list of what shipped — no narration of the process.
```

---

## WHAT GETS WRITTEN, AND WHY EACH ONE EXISTS

### 1. The page — `{ticker}.html`
Cloned from the most recently published ticker, never rebuilt. Per-ticker edits are
confined to: title/meta/OG/canonical, the JSON-LD graph, the masthead chip + `<h1>`,
the attack-form hidden fields, the share string, the side-card heading, the edition
line, `data-ticker` / compare links, `const T=TICKERS.{KEY}` + `renderPeers`, the
fair-value levers, and the three prose blocks (plain-terms, MC bear paragraph, MC
driver list). Everything else is template and must stay byte-identical — five pages
once shipped another company's valuation table from a clone-and-forget edit, which is
why `check_page_integrity.py` diffs numeric tables across pages.

### 2. `assets/data.js`
- `TICKERS.{KEY}` entry — spot, fair{bear,base,full}, `dist` (both horizons + resolve
  dates), `hz`, `touch`, `levels`, `tech`, `asof`, `files`.
- `SITE.latest` = the new key, `SITE.updated` = the publish date. `SITE.updated` only
  ever moves FORWARD (`bump_site_updated` clamps it — a single-name refresh once rolled
  the whole site's date back a week).
- LEDGER: a dated comment header carrying the calibration verdict, then the cycle-1
  rows (below).

### 3. `assets/coverage.js`
EN row, AR row, and the `SHORT` label. Three separate places; the coverage grids and
the footer strip read different ones.

### 4. `ledger.html`
Two registrations, both silent-failure-prone:
- `HAS_BACKTEST` — absent and the panel omits the whole calibration block with no error.
- the raw-CSV map (`{KEY}: "{MKT}/{TICKER}.csv"`) — feeds the graded-cohort chart's
  realized-price overlay.
`check_data_freshness.py` gates `HAS_BACKTEST` in BOTH directions (listed-without-image
= broken `<img>`; image-without-key = invisible backtest); two names sat mis-registered
for weeks before that check existed.

### 5. The calibration artifacts
- `assets/calibration_{KEY}.png` — `cd engine && python3 metal_backtest.py {KEY}`.
  Quarterly replay with 90%/50% cone boxes and realized dots, PIT histogram, band
  coverage vs target, honesty footer. Windows = every non-overlapping 3-month window
  from the market's last structural break to today, walked BACK from the last session.
- The LEDGER comment header records the verdict, the scale-normalized CRPS skill, the
  bootstrap CI and whether it is robust across block sizes {2,3,4}.

### 6. `assets/markets.js` — the market registry
`python3 scripts/build_market_registry.py --write`. Market is decided by FILE PLACEMENT
(`engine/raw_ohlc/{MARKET}/{TICKER}.csv`); this generated file is the bridge the ledger
reads. **The ELEC publish (05-Aug-2026) placed the CSV and regenerated the sitemap, the
feed, the footer strip and the chart — but not this — so `MARKET_OF['ELEC']` was
undefined and the ledger rendered ELEC OUTSIDE the "EGX — Egypt" group. Nothing threw.**
That is the same failure class the registry was introduced to close (29-Jul-2026: 34
international names under the EGX heading). Now gated by `check_data_freshness.py`
check 9 — which compares on the LEDGER INSTRUMENT name, not the `TICKERS` key, because
`ledger.html` feeds `marketOf()` the instrument ("Gold", "Samsung", "XPTUSD").

---

## THE LEDGER ROWS

Two rows at first coverage: 1-month and 3-months, `cycle_no: 1`, no `reanchor_from`.
Both anchored on the study's own strike — reuse the arrays the study already produced;
re-simulating at publish time would publish a cone the study never claimed.

- `p5/p25/p50/p75/p95` — the frozen percentiles, from `strike_result.json` /
  `study_numbers.json`.
- `touch` — running-max/min hit rates at ±5/10/15/20% and −5/−10% off the anchor,
  computed from the saved `paths_1M.npy` / `paths_3M.npy`. NOT the ticker page's
  absolute-level ladder; different object, different levels.
- `grade_date` — from `horizons.resolve()` at strike (calendar month(s) forward, rolled
  to the first real session on that exchange's calendar). Never a session count.
- `realized_*`, `in_90`, `in_50`, `realized_quantile`, `median_err`, `touch_hit` — all
  `null` until the cohort matures. Grading is a later, separate event.
- `anchor_vol` — the horizon's own annualized anchor vol, not one value for both.
- **`cal`** — OMIT for a PASS. Set `"matches"`, `"untested"` or `"fail"` only when that
  is the verdict; `ledger.html` derives its banner from this field, so a wrong value
  either stamps a healthy name "⚠ INDICATIVE ONLY · CALIBRATION FAILED" or suppresses a
  warning that should be showing.

A new name does NOT appear in the "Were we right?" headline score. It joins that
denominator when its first cohort grades — open rows are shown with their check date
and nothing more.

---

## VERIFY BY RENDER, NOT BY GREP

Every defect this protocol exists to prevent passed a grep. The markup was well-formed
in all of them: a missing `</details>` that buried a whole section, five pages showing
another company's table, a ticker outside its exchange group, a backtest block silently
omitted. Load the pages headless (`file://`, `waitUntil:'load'` — NOT `'networkidle'`,
which never fires here), open the accordions, and read the DOM.

Then both static gates must be clean before the commit:
```
python3 scripts/check_page_integrity.py     # accordion nesting, sections, cross-page tables, stale fair value
python3 scripts/check_data_freshness.py     # ledger<->published pairing, as-of stamps, HAS_BACKTEST, market registry
```

---

## THE CALIBRATION WORKFLOW WILL GO RED — THAT IS CORRECT

Placing the CSV triggers `testahil-calibration.yml`, which refits the whole market.
If the materiality gate finds anything that needs a human (a verdict flip, a new name
arriving already FAILING, the market verdict changing, a panel name with no raw data,
the published 90% cone moving >5%) it writes a `PENDING_REVIEW/*.md` report, opens a
review PR, leaves `market_profiles.py` untouched, and then **deliberately fails the
run** — the step is named "Fail the run so a material change is never mistaken for a
clean one".

A NEW NAME IS NOT MATERIAL BY ITSELF. Read the report before assuming the failure is
about the ticker being published: the 05-Aug ELEC run tripped on ORAS drifting
PASS → BOUNDARY as the panel went 30 → 31 names, while ELEC itself scored the panel's
best skill.

Each completed run opens its OWN review branch, so N pushes to a publish branch produce
N duplicate review PRs (`concurrency: cancel-in-progress` stops overlapping runs, not
the accumulation of branches). Merge the one cut from post-merge `main`; close the rest
as superseded.

---

## ORDER OF OPERATIONS

1. Place `engine/raw_ohlc/{MKT}/{TICKER}.csv`; copy the deliverables into `files/`.
2. Write the `TICKERS` entry, `SITE.latest`/`updated`, and the LEDGER header + rows.
3. Clone the page; adapt the per-ticker slots.
4. `build_market_registry.py --write`; `metal_backtest.py {KEY}`; register both
   `ledger.html` sets; add the `coverage.js` rows.
5. `ta_chart.py` then `apply_technicals.py` (both `--only {TICKER} --write`) — these
   rewrite the ticker's own block, so they run after step 2/3.
6. `generate_seo.js`, `generate_feed.js`.
7. Render-verify; run both gates; commit; ask for the token once; push.
