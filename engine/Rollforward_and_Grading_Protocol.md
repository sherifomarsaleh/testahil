# TESTAHIL — Roll-Forward & Grading Protocol (v3, 29-Jul-2026)

Paste this + a ticker + fresh OHLC to trigger the full cycle below, end-to-end, unattended
(all local until a PAT is supplied for push — same discipline as every other write).

Trigger phrase: "Roll forward {TICKER} with this data" / "recalibrate and forecast {TICKER}"

**v3 change (29-Jul-2026): THE FORECAST LIFECYCLE (STEP 0) is adopted.** One current
forecast per name per horizon; the 1-month maturity is the metronome for both horizons'
ledger strikes; a fresh 3-month strike demotes the previous 3-month to an aging calibration
tail that runs untouched to its own grade date. This replaces the prior practice under which
every data update minted new ledger cycles on top of still-open old ones — which produced
135 of 150 (instrument, horizon) pairs carrying two or more simultaneously-open, overlapping
forecasts, and meant no 3-month forecast ever survived to grading (all 11 grades earned to
date are 1-month windows). A one-time cleanup deleted the 143 superseded-and-never-graded
legacy rows (304 → 161: 150 live + 11 graded, permanent). Grading and striking are
CALENDAR-NATIVE throughout, per the 28-Jul horizon standing amendment: the check date is a
calendar date, never a session count. **v2/v2.1 changes** (technical
read computed in-pass; chart part of the read; two-part as-of stamps; overlay gate) stand.

---

## STEP 0 — THE FORECAST LIFECYCLE (adopted 29-Jul-2026)

**The rules:**

1. **At most one CURRENT forecast per name per horizon** — always the latest strike. It
   alone feeds the ticker page, Trade, and Portfolio (all of which read `TICKERS`, never
   `LEDGER` — verified: zero `LEDGER` references in trade.html / portfolio.html).
2. **Every monthly update — the 1-month maturity is the metronome:** grade the matured 1M,
   strike a fresh 1M AND a fresh 3M.
3. **A fresh 3M demotes the previous 3M to an aging calibration tail** — it stays open,
   untouched, and is graded at its own maturity. It is used for nothing else: not the site,
   not Trade, not Portfolio.
4. **Steady state per name is 4 open rows** — current 1M, current 3M, two aging 3Ms. The
   count runs 2 → 3 → 4 from coverage start and holds at 4. From month 3 onward every
   monthly update grades one window of each horizon.
5. **Graded rows are permanent and never edited.**
6. **Routine updates never delete a ledger row.** Deletion is reserved for deliberate
   mid-flight engine corrections (the superseded ungraded row is removed in the same commit
   that strikes its replacement) — plus the one-time 29-Jul-2026 cleanup of the 143 legacy
   rows created under the old overwrite practice.

**The two-object split (why nothing ever goes stale):** the displayed cone
(`TICKERS.{T}.dist`) answers "where could it go from TODAY" and refreshes with every data
update, both horizons — Trade and Portfolio always run on a fresh 1M and a fresh 3M
lookahead. The LEDGER row is one frozen sample of that same engine, held to maturity purely
to prove the machinery honest. A fresh + non-overlapping + maturity-reaching 3-month ledger
commitment more often than every 3 months is arithmetically impossible; the freshness lives
in the cone, the ledger takes the monthly sample and grades every one of them.

**Adopted decisions:**
- **(a) Mid-cycle OHLC updates** (data arriving between monthly events): refresh the
  displayed cone + technical read (STEPs 5/5B) ONLY. No new ledger rows — ledger strikes
  stay on the monthly metronome. (Otherwise 1M tails accumulate and the rhythm breaks.)
  **Tool: `engine/refresh_cone_one.py {MARKET} {SERIES} {SITE_KEY} --today DD-Mon-YYYY
  --write`** (added 03-Aug-2026). Until then this decision had no executable form and the
  only single-name tool was `rollforward_one.py`, which always appends two ledger rows —
  so running the obvious thing mid-cycle struck a cohort the metronome never called for
  and broke the lifecycle invariant. Both tools rewrite the ticker entry through the same
  `rollforward_one.restrike_entry`, so they cannot publish differently-shaped cones; the
  only difference is whether a LEDGER row is struck, and the mid-cycle tool ASSERTS the
  LEDGER came out byte-identical rather than trusting that it did.
- **(b) Metals 12-month horizon stays on its own annual clock** — one open 12M per metal,
  graded at maturity then re-struck. It does NOT join the monthly strike (that would leave
  11 overlapping year-long tails per metal, clutter without calibration value).

**Yield:** 12 graded 1-month + 12 graded 3-month windows per name per year (the record
before adoption: 11 and 0).

---

## STEP 1 — MERGE, NOT OVERWRITE
Diagnose the upload: full history or partial export? If partial, splice onto the persistent
library (`engine/raw_ohlc/{MKT}/{TICKER}.csv`) — verify overlapping dates match to the 4th
decimal (no silent back-adjustment), keep only genuinely new rows, preserve vendor format.
Never let a partial upload replace the library.

## STEP 2 — CALIBRATION (Step 0.0 gate + refit)
Run the existing pipeline unchanged: `data_quality.clean_ohlc` (per-market price-limit gate),
then `auto_refresh.py` dry-run against the FULL market panel (never just the touched name).
Report the materiality verdict. If material (verdict flip, new-name-arrives-FAILING, cone
moves >5%, breaks change) — stop, do not proceed to Step 3/4 without flagging it explicitly;
this is a PR-gated event, not an auto-apply one.

## STEP 3 — GRADE EVERY NOW-MATURED COHORT
Under the lifecycle this means: the matured current 1M, PLUS any aging 3M tail (and any
metals 12M) whose grade date has arrived. **The forecast is a DATE, not a session count.**
The check date is the calendar grade date resolved at strike by `horizons.resolve()` —
anchor + 1 (or 3) calendar months, month-end clamped, rolled FORWARD to the first real
trading session on or after the target on that exchange's own calendar. Whether the window
contained 18 sessions or 24 is irrelevant to grading; sessions matter only at strike time,
to size the cone. Never re-derive the target by counting rows. For every open LEDGER row
(`realized_close == null`) whose grade date the persisted library now covers:

1. Verify the stored `grade_date` against the library: it must be a real traded session. If
   an unscheduled closure or suspension pushed the first real session past it, the grade
   session is the next actual session in the library.
2. Grade against the close ON that date (realized_close/high/low over the calendar window's
   actual sessions, in_90/in_50 via the frozen p5/p25/p50/p75/p95, realized_quantile via
   linear interpolation on those percentiles, median_err = realized/p50 − 1, touch_hit at
   the same ±5/10/15/20%/±5/10% relative levels used at publish, using running max/min over
   the window).
3. If the graded session differs from the stored `grade_date`, do NOT silently overwrite
   history: set `grade_date` to the actual session graded, add `grade_date_projected` (the
   original stored value) and a one-line `grade_note` stating the gap and likely cause
   (closure/suspension). This is an append/annotate, never a silent retro-edit of the
   frozen percentiles themselves — those stay exactly as published.
4. The ledger page's existing JS needs NO template change for this — once `realized_close`
   is non-null it already renders the real close + "we got it right ✓ / we were off ✗" from
   `in_90`. Grading is a DATA fix, not a code fix.

## STEP 4 — STRIKE: NEW CYCLE (monthly metronome only)
**This step runs at the monthly event (the current 1M's maturity), never on a mid-cycle
data arrival — see STEP 0 decision (a).** Strike BOTH horizons: a fresh 1M and a fresh 3M,
anchored at the latest close. The fresh 3M demotes the prior 3M to an aging calibration
tail (no field change needed — "current" is defined mechanically as the latest anchor per
(instrument, horizon); everything older and still open is a tail awaiting its grade date).
Never delete the demoted row; deletion is only for deliberate mid-flight engine corrections,
where the superseded ungraded row is removed in the same commit as its replacement.

Anchor the new cycle (`cycle_no` = prior max + 1, `reanchor_from` = prior cycle's
`anchor_date`), run the actual production engine — not an approximation:

```
h1, h3 = projected SESSION counts spanning the 1M / 3M calendar windows
         (engine/horizons.py blend projection — never a hardcoded 20/60)
v = yz_variance_proxy(df)
beta, s2 = fit_har_v3(v, origin=last_row, horizon=h3)
dv       = har_forecast_v3(v, origin, beta, s2, horizon=h3)
drift    = carry_log_h(profile, anchor_date, q_annual, horizon=h3)   # exact calendar year-
                                                                       # fraction; rf_live from the profile;
                                                                       # q_annual must be SOURCED —
                                                                       # if genuinely disputed/unclear
                                                                       # across sources, default 0 and
                                                                       # flag it, never split the
                                                                       # difference or invent a number
paths = simulate_paths_v3(spot, dv, h3, drift, nu=profile.nu,
                           n_paths=50000, seed=42, width_cal=profile.width_cal)
```
`signal_alpha` is already gated on `profile.signal_active` internally — do not hand-add a
discretionary drift on top of this. This is the SAME single call used for both horizons:
`p1M, p3M = paths[:,h1], paths[:,h3]`; percentiles via `np.percentile(...,[5,25,50,75,95])`;
touch via running max/min (`paths[:,:h1+1]` for 1M, full `paths` for 3M) against both the
existing relative ladder (±5/10/15/20% / ±5/10%) for the LEDGER row and the site's existing
absolute price levels for the ticker-page touch table (Step 5).

**For a single name, use `engine/rollforward_one.py {MARKET} {SERIES} {SITE_KEY} --today
DD-Mon-YYYY --write`.** It runs exactly the chain above via `strike_cohorts.strike()`.
(Mid-cycle — NOT the monthly event — use `refresh_cone_one.py` instead; STEP 0 decision (a).)
`apply_rollforward.py` is the RECORD of the 28-Jul-2026 market-wide re-strike — its header
comment and per-row note are hardcoded to that pass, so re-running it for one name stamps
today's cohort with last week's story.

`grade_date` for the new cycle comes from `horizons.resolve()` — anchor + 1/3 calendar
months, month-end clamped, rolled forward to the exchange's first real session. It is the
calendar commitment Step 3 grades, regardless of how many sessions the window turns out to
hold. Round percentiles to 2dp, touch to whole %, matching existing row formatting exactly.

## STEP 5 — TICKER PAGE (the "financial instrument page")
Runs on EVERY data update, mid-cycle included (STEP 0 decision (a)): the displayed cone is
re-struck fresh from the latest close even when no ledger row is minted. Update
`TICKERS.{TICKER}` in `assets/data.js` only:
  - `spot`, `spotDate` → new anchor/price (cascades automatically to the header badge, the
    "Latest X EGP (close date)" line, the fair-value gauge, and the interactive slider's S0 —
    all of these already read `T.spot`/`T.spotDate` live, no HTML edits needed)
  - `dist.t20`, `dist.t60` → new percentiles + resolve dates (drives the static "could go
    either way" probability-read widget directly)
  - `touch` → recompute at the SAME absolute price levels already on the page (don't
    re-pick levels; comparability across cycles matters more than centering them on the
    new spot)
  - `levels`, `tech`, `asof` and the page's chart → **see STEP 5B**.

**Do NOT touch**, and say so explicitly when reporting back:
  - `fair: {bear, base, full}` — the fundamental valuation is a separate clock (two-clocks
    rule); it only moves on a genuine study refresh, never on a price/OHLC roll-forward.
  - The interactive slider's bespoke factor-stack constants (`CONT_FIXED`, `EV_FIXED`,
    `GEO_MEAN`, `LNCH_MEAN`, `BETA`, and similar `moments()` inputs in the ticker HTML) —
    these were fit once, by hand, to approximate the STUDY's fundamental driver stack, not
    the carry-anchored engine. Re-fitting them is a full study-level task (fresh Information
    Sweep, driver review), not a data refresh. The slider will still re-anchor correctly to
    the new spot (it reads `T.spot` live) but its baseline drift/vol shape stays as last
    published until that separate work happens.

## STEP 5B — TECHNICAL READ, CHART + AS-OF STAMPS (adopted 29-Jul-2026; supersedes v1's carve-out)

**v1 said `levels` and `tech` "need an actual fresh chart read, not a mechanical recompute"
and must be left alone. That rule is RETIRED.** It was written to protect a hand-authored
judgement, and in practice it protected staleness instead: by 28-Jul-2026 COMI's live page
carried a 142.00 spot beside a narrative reading "the price closed 129.25 below a falling
20-day", with all three of its published resistances sitting BELOW spot; SAMSUNG's three
published *supports* all sat ABOVE its spot. A block that is never refreshed is not a
preserved judgement — it is an unmarked expiry date.

**The rule now: when the library moves, the technical read moves with it — levels, narrative
AND the chart underneath them, in the same pass.**

```
python3 engine/apply_technicals.py --write            # levels, tech, asof (all names)
python3 engine/apply_technicals.py --only COMI        # one name
python3 engine/ta_chart.py        --write             # the chart underneath them
node scripts/check_ta_chart_overlay.js                # MANDATORY gate — see below
```

`engine/technicals.py` computes the read from the same cleaned series the MC engine runs on,
through the same Step 0.0 gate — SMA 20/50/200 with slope state, Wilder RSI(14), Wilder
ATR(14) on the true range, MACD(12,26,9), 50/200 cross recency, 52-week range, and S/R from
fractal pivots clustered with a recency weight. Moving averages, the 52-week extremes and
round numbers are admitted as level candidates but score strictly below real swing structure.
The prose is templated: every clause is selected by a computed number. Re-running on an
unchanged library is a no-op — the pass is idempotent by construction.

Binding conventions:
  - **R1/S1 always mean NEAREST to the close.** The retired hand-authored levels were
    inconsistent about this (TSLA ascending, COMI descending), so R1 meant different things
    on different pages.
  - **No fundamental assertions in the technical block.** Some retired narratives closed with
    a valuation sentence ("the equity case rests on a ~30% ROE against a ~24% cost of
    equity"). A deterministic module cannot source that, so it does not say it. Fundamental
    context belongs to the study, the fair-value gauge and the driver stack.
  - **`apply_technicals.py` never re-strikes a cone.** It reads the published cone's anchor
    date off the newest LEDGER row for that instrument and its run date off that row's own
    note, and stamps them. Re-striking is STEP 4's decision, never a side effect here.
    (Under STEP 0 decision (a) a mid-cycle pass refreshes `dist` without a ledger row; the
    stamp source for `asof.mc` is then the `dist` resolve dates, reported as such.)

### The chart is part of the read, not scenery

`engine/ta_chart.py` regenerates the static `<svg id="ta-chart-svg">` on every ticker page
from the same library, and rewrites the figcaption's session count and date.

**Refreshing levels onto a frozen chart is WORSE than leaving both stale.** That is not a
hypothetical: on 29-Jul-2026 COMI's chart axis topped out at 148, captioned "last 500 sessions
to 29 Jun 2026", carrying a freshly computed resistance of 160 — `injectLevels` drew that line
at y=−21, outside the 0..320 viewBox. No exception, no console error, the page looked fine,
the level was simply gone.

**The SVG is a CONTRACT.** `injectLevels()` recovers price→y by regressing over the chart's own
muted axis labels, and `renderZoomChart()` re-reads the same element. Change the label markup
and both silently mis-scale. The generator therefore reproduces the existing structure exactly
— viewBox 0 0 760 320, plot box x 46..700 / y 14..294, five gridlines with muted right-aligned
labels at x=40, three polylines in draw order brass (200-day) → teal (50-day) → ink (price, on
top), seven quarter labels at y=312.

**The y-range is fitted to the union of the price window, both moving averages AND the
published S/R ladder** — so an overlay cannot fall outside the plot by construction, rather
than by anyone remembering to look.

**MANDATORY GATE — `node scripts/check_ta_chart_overlay.js`.** Renders every page carrying a
chart and fails (exit 1) if any injected level line escapes the viewBox. Nothing else catches
this. It is negative-controlled against the 29-Jul defect: restoring the pre-fix `comi.html`
makes it report `comi.html … y=-21.2` and exit 1; the fix makes it pass and exit 0. A gate
never seen to fail is not evidence.

**As-of stamps — two dates, never one.** Each entry carries:

```
asof: {
  mc:   { data:"YYYY-MM-DD", computed:"YYYY-MM-DD" },
  tech: { data:"YYYY-MM-DD", computed:"YYYY-MM-DD" }
}
```

`data` = the last session the block was built on. `computed` = the day it was run. A single
"as of" cannot tell a block recomputed today on last week's prices from one recomputed last
week, which is exactly the failure being closed. `assets/app.js` renders both stamps off this
field — hooked into `renderStaticFan`, the one function every ticker page already calls, so no
page template needs editing and a new page inherits the stamps automatically.

**Read the stamps as a diagnostic, and do not reconcile a gap silently.** When `asof.mc.data`
is older than `asof.tech.data`, the published cone is stale relative to its own library — that
is a roll-forward decision (STEP 4), reported, never quietly patched inside a technicals pass.
The 29-Jul-2026 fan-out surfaced exactly one: 2POINTZERO, cone anchored 03 Jul against a
library running to 24 Jul, page spot 2.16 vs a 2.06 library close. Root cause was a bug, not an
oversight — `apply_rollforward.ticker_blocks` matched unquoted object keys only, so
`"2POINTZERO"` (which MUST be quoted; a JS identifier cannot start with a digit) was silently
dropped from the 28-Jul market-wide pass. It reported "58 cones" where EG 30 + AE 18 + SA 11 =
59, and nobody counted.

**A LAYOUT MUST NEVER DECIDE WHETHER A FIELD GETS REFRESHED (earned 03-Aug-2026).** Both
single-name tools rewrote the ticker entry with hand-rolled regexes that keyed off
INDENTATION, and both were silently wrong on a subset of entries:
  - `dist` was matched as `\n    dist: \{.*?\n    \},`, which closes on the first
    4-space-indented `},`. Nine entries (RELIANCE, IQCD, SAMSUNG, KAKAO, LGES, TMPV, QGTS,
    AAPL, TSLA — the IN/US/KR/QA cluster) close `dist` at TWO spaces, so on those the match
    ran past `dist` and stopped at `tech`'s closer: a roll-forward DELETED `touch`, `levels`
    and `tech` outright. The result was valid JavaScript and a page that still rendered.
  - `touch` was matched only in its multi-line form, so on the 19 entries that write it on
    one line the ladder was left exactly as it was while `spot` and `dist` moved — a stale
    probability table under a fresh cone, with nothing on the page to say so.
Both are now brace/bracket-matched (`_span_of_key`, `_touch_ladder`). The fix was verified
the only way that means anything: replayed across all 71 entries, BYTE-IDENTICAL on the 62
the old code got right, and field-preserving on exactly the 9 it did not. Same family as the
unquoted-key regex that dropped 2POINTZERO from the 28-Jul pass — when a pattern stands in
for a parser, the entries that happen to be formatted differently are the ones that rot.

**STANDING VERIFICATION RULES earned here — apply to every data.js write:**
  1. `node --check` on `data.js` and `app.js`, then **LOAD** `data.js` in node and assert on
     the parsed `TICKERS`/`LEDGER` objects. An assert-guarded string replacement verifies the
     old text existed; it cannot see whether the surrounding structure survived. A missing
     comma before an appended LEDGER row is valid-looking text and invalid JavaScript.
  2. **Count against a known total.** Never trust a tool's own "0 skipped" — the same
     unquoted-key regex bug hit three separate tools, each reporting success.
  3. **After any ledger write, assert the lifecycle invariant:** exactly ONE open row per
     (instrument, horizon) that is the latest anchor; every other open row for that pair must
     be an aging 3M tail (or a metals 12M) with a future grade date. Two rows both claiming
     to be current is the exact defect the 29-Jul cleanup removed — fail loudly, never ship it.

## STEP 6 — LEDGER PAGE
Confirm (don't assume) the grade you wrote in Step 3 renders correctly — the existing
`renderRow()` logic already turns a populated `realized_close` into the pass/fail line with
no template change. Separately assess the five-year quarterly calibration backtest PNG
(`assets/calibration_{TICKER}.png`): this is a coarser, ~quarterly-cadence construct spanning
years, not something a single new 1M/3M cohort or a few weeks of tail data usually moves.
State plainly whether a regeneration pass is actually warranted this cycle, rather than
regenerating by default — and if it is warranted, that's its own step (via `ledger_scorer.py`
+ `viz.py`), reported separately, not bundled silently into a data-only roll-forward.

## STEP 7 — PUBLISH
Everything above stays local. Report a clean summary: what was graded (with any
projected-vs-actual date gap called out), the new cohort's numbers, any 3M demoted to a
tail, the refreshed technical read, the regenerated chart, both as-of stamps, exactly which
ticker-page fields changed vs. were deliberately left alone, and the ledger/backtest-PNG
status. Bump the cache-buster in the same change — and check the token is unused first; two
sessions independently picked `20260728a` once. Push only on request, with a fresh PAT
(never stored), tokenless URL restored immediately after.
