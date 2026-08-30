> **RESOLVED — same day.** Everything in §6 below except items 4/5/6 is now closed out — see §7 at
> the bottom for the final state. `market_profiles.py` is fully on the calendar 3-month fit as of
> commit `48bc1f5`. This banner is the only edit to text above it; §1–§6 are left exactly as
> written in the moment, per the append-only convention.

# Calendar horizons (1 month / 3 months) — adopted 27-Jul-2026

**Status:** built, gate re-run, merge conflict against `main` resolved, merge commit `b8d67f6`
created locally on `feat/calendar-horizons-1m-3m`. **Still not pushed** (PAT rule — a fresh token
is requested at push time and never stored) and **not written into `market_profiles.py`**. Needs a
review decision before it reaches production.

Trigger: user instruction, 27-Jul-2026 — *"I want the register to be updated on 1 month and 3
months instead of 20 working days and 60 working days. I want the testahil pages to be changed
accordingly, especially the ledger page."*

---

## 1. The rule that changed

Published horizons are now **calendar objects**, replacing the session-counted T+20 / T+60:

    target_date = anchor_date + 1 (or 3) calendar months, month-end clamped
                  (31-Jan + 1M -> 28/29-Feb)
    grade_date  = the first REAL trading session on or after target_date on that
                  exchange's own calendar; weekend/holiday rolls FORWARD, never back
    h           = the sessions spanning that window — NOT a constant
                  (18-24 for a month, 55-67 for a quarter, by market and anchor)

**Why it was worth doing, in one line:** the old convention's error landed in the *check date*.
The projected Sun–Thu `grade_date` had no holiday awareness, so it routinely fell ~2 sessions
short of a true T+20 — **every graded cohort so far (PHDC, TMGH, EMFD) carries a `grade_note`
recording exactly that correction.** A calendar target cannot drift.

**Grandfathering is absolute.** The 151 open T+20/T+60 cohorts keep the horizon they were issued
on, grade on it, and count in the score unchanged. Not one published percentile was touched.
`horizon_label` records which convention a row belongs to; both render side by side.

---

## 2. Engine

New: **`engine/horizons.py`** — the single place a horizon is resolved; never hand-computed.
Per-market trading calendars are the union of session dates across the whole `raw_ohlc/{MKT}/`
library (post Step 0.0). Week-masks are derived empirically from recent sessions, so ADX/DFM's
Jan-2022 Sun–Thu → Mon–Fri switch is handled without a hard-coded table.

At publish time `h` must be projected. Three candidates were backtested strictly out-of-sample on
every market:

| projection | mean session error | mean **cone-width** error | worst cell |
|---|---|---|---|
| density | 1.083 | 1.51% | 3.18% |
| seasonal | 0.879 | 1.39% | 3.12% |
| **blend (adopted)** | 0.913 | **1.33%** | **2.84%** |

Sessions are the wrong loss function — width goes as √h, so a misplaced session costs ~2.4% of the
cone at 1M but only ~0.8% at 3M. On that decision-relevant loss the **blend wins outright**.
Picking per horizon (seasonal wins 3M in 8/9 markets, blend wins 1M in 6/9) would be selecting a
rule on the sample used to score it — the exact failure the PROMOTION RULE names.

**`mc_v3.backtest_v3(horizon_months=)`** runs the gate on calendar windows, with a split that
matters:

- `h_grade` — where the outcome is read (calendar fact, no forecasting).
- `h_size` — a **causally projected** session count, from the series' own trailing density up to
  the origin, used to size the cone.

Conflating them puts hindsight in the gate. A name suspended for two of three months has
`h_grade ≈ 6` while any live forecaster would still have sized a full quarter; scoring that
outcome against a 6-session cone credits the engine with a cone it could never have drawn. The gap
return stays in the sample, scored against the quarter-wide cone that was actually issuable.
**161 of 2,198 windows (7.3%) have |h_grade − h_size| > 5** — the split does real work.

Carry now runs on the exact calendar year-fraction rather than h/252.

**The legacy fixed-h path is bit-for-bit unchanged** — including the floating-point *expression
order* of `carry_log_h`, which broke the regression on first attempt. Verified against the
pre-change engine on EG/AE/QA/SA/KR.

Panels are namespaced by horizon set (`_60d` vs `_3m`), so the retired gate stays re-runnable for
the grandfathered cohorts and the two calibrations never overwrite each other.

---

## 3. Gate re-run — 60d vs calendar-3M, ORIGINAL library (12-Jul snapshot, superseded for 5 markets — see §3b)

Run via `engine/refit_calendar_horizon.py`; compared with `engine/compare_horizon_fits.py` against
a freshly-run 60d baseline on the **same** library. **These numbers for AE, EG, KR, SA, XAU no
longer describe the current repo state** — see §3b. IN/QA/US/XPT were never touched by any
concurrent commit and these remain their live numbers.

| mkt | ν | width_cal | 90% band | verdict | skill |
|---|---|---|---|---|---|
| AE | 10 → 10 | 1.028 → 1.007 | −2.04% | PARITY → PARITY | +0.0033 → +0.0066 |
| EG | 5 → 6 | 0.930 → 0.951 | +3.95% | PASS → PASS | +0.0158 → +0.0158 |
| **IN** | Gauss → Gauss | 0.930 → 0.986 | **+6.02%** | PARITY → PARITY | +0.0046 → +0.0042 |
| KR | Gauss → Gauss | 1.154 → 1.161 | +0.61% | PARITY → PARITY | +0.0144 → +0.0058 |
| QA | 12 → 10 | 0.972 → 0.937 | −3.95% | PARITY → PARITY | −0.0091 → −0.0028 |
| SA | 6 → 6 | 1.063 → 1.070 | +0.66% | PARITY → PARITY | +0.0023 → +0.0051 |
| **US** | 12 → Gauss | 1.014 → 1.077 | **+7.38%** | PARITY → PARITY | −0.0056 → +0.0085 |
| **XAU** | 20 → 12 | 1.035 → 0.993 | −4.60% | **PASS → PARITY** | +0.0099 → +0.0077 |
| XPT | Gauss → 8 | 0.853 → 0.860 | −1.29% | PARITY → PARITY | −0.0004 → +0.0078 |

**Material under the standing gate (as of this snapshot): IN (band +6.0%), US (band +7.4%), XAU
(verdict change).** IN/US/QA/XPT are unaffected by anything below and these figures still stand.

---

## 3b. Post-merge re-verification (27-Jul, same day) — AE/EG/KR/SA/XAU redone on the current library

While this branch was in flight, 10 commits (140 files) landed on `main`: a long-history
"Selection engine" ingest re-pulled full price history for all 18 AE names and all 11 SA names
(~2.8x longer for most), a 15-year Samsung ingest for KR (with an already-merged KR refit:
nu Gaussian→12, cal 1.154→1.105), a GOLD refresh, and a roll-forward that graded the OCDI/ORHD/
GOLD/SAMSUNG cohorts and appended 3 sessions to OCDI/ORHD. The GitHub PR (#32) came back showing 3
merge conflicts (`engine/panel_hashes.json`, `engine/panels/EG_OCDI_60d.csv`,
`engine/panels/EG_ORHD_60d.csv`). Resolved by recomputing every conflicting hash from the current
merged raw files, not by picking a side — main's own conflicting values turned out to be stale for
unrelated EG names (RMDA, CLHO), a second instance of the exact bug §4(b) below already fixed once.

Because AE/EG/KR/SA/XAU's underlying libraries had genuinely moved, the §3 numbers for those five
were no longer honest and were redone end to end (`engine/reverify_post_merge.py`, log at
`engine/reverify_log.txt`) for both `60d` and `3m`. Doing this also rebuilt every AE/SA/KR/XAU panel
file whose content hash had drifted from the merged raw CSV — main's ingest had updated raw data
for AE and SA without rebuilding their panels or hash registry, the same staleness pattern as §4(b),
now recurring for two more markets. All of it is committed in the merge (`b8d67f6`);
`market_profiles.py` itself has **zero diff** against `origin/main` — nothing here writes a new
number into production.

**Band-width move, new fit vs. today's live `market_profiles.py` incumbent** (the number the
standing gate actually measures — `width_cal × q95(t(ν))`):

| mkt | tag | live ν/cal | new ν/cal | move | flag |
|---|---|---|---|---|---|
| XAU | 60d | 20.0 / 1.035 | 20.0 / 1.035 | +0.00% | — |
| XAU | 3m | 20.0 / 1.035 | 12.0 / 1.0 | −0.16% | — |
| EG | 60d | 5.0 / 0.93 | 5.0 / 0.93 | +0.00% | — (OCDI/ORHD's 3 extra sessions moved nothing) |
| EG | 3m | 5.0 / 0.93 | 6.0 / 0.951 | −1.39% | — |
| KR | 60d | 12.0 / 1.105 | 12.0 / 1.105 | +0.00% | reproduces main's already-merged refit exactly |
| KR | 3m | 12.0 / 1.105 | 10.0 / 1.063 | −2.17% | — |
| **AE** | **60d** | 10.0 / 1.028 | 8.0 / 0.895 | **−10.68%** | **MATERIAL — unrelated to this PR, see below** |
| AE | 3m | 10.0 / 1.028 | 10.0 / 0.979 | −4.77% | close to the line, not over it |
| **SA** | **60d** | 6.0 / 1.063 | 8.0 / 1.021 | **−8.08%** | **MATERIAL — unrelated to this PR, see below** |
| **SA** | **3m** | 6.0 / 1.063 | 12.0 / 1.07 | **−7.68%** | **MATERIAL — this PR's own proposal for SA** |

**Two different things are true here and should not be conflated:**

1. **AE-60d and SA-60d are not about calendar horizons at all.** They're what happens if you simply
   refit the *existing* legacy 60d convention against the library `main`'s own concurrent ingest
   already grew. `main` added the raw CSVs but never re-ran the calibration for AE/SA (unlike KR,
   which it did refit). That's a pending recalibration debt on `main`, independent of and pre-dating
   this branch. Flagging it here because I found it as a byproduct of the re-verification; not
   fixing it in this PR — that's its own promotion decision.
2. **SA-3m is this PR's actual proposal for SA, and it breaches the gate.** Adopting calendar
   horizons for SA specifically would move the published cone by −7.68%, over the 5% line. This
   should not be treated as a routine part of the calendar-horizon adoption; SA needs its own
   explicit sign-off.

**SA/EXTRA's FAIL, re-examined on >2x the data:** confirmed, and now robust at both horizons.

| | old (short SA library) | new (current, long SA library) |
|---|---|---|
| 60d | PARITY, skill −0.0140, 190 windows | **FAIL**, skill −0.0308, 410 windows |
| 3m | FAIL, skill −0.0427, 180 windows | **FAIL**, skill −0.0372, 392 windows |

More data sharpened the same conclusion rather than reversing it — at 3m it was already a robust
FAIL pre-ingest and remains one on more than double the windows; at 60d it moves from PARITY to a
robust FAIL now that there's enough history to clear the block-bootstrap bar. SA/ALINMA also moves
PARITY→BOUNDARY(PARITY-flagged) at 60d. SA/ELM stays FAIL at 60d (unchanged, pre-existing) but reads
PARITY at 3m in both the old and new SA libraries — a genuine difference by horizon granularity, not
an artifact of the merge; noted, not resolved, here.

AE per-name churn from the same re-verification (all verdict-category changes, none newly FAIL):
ADIB, DIB, EMAAR move PARITY→PASS at 3m; AGTHIA, EAND, ENBD move PARITY→BOUNDARY(PARITY-flagged) at
3m; ADNOCGAS, EAND move PARITY→BOUNDARY at 60d. KR/LGES moves FAIL→PARITY at 3m (un-fails on more
data). Every one of these is an "existing name's verdict changed" event under the standing
materiality gate — correctly routed through this PR rather than auto-committed.

---

## 4. Two findings the change surfaced (both pre-existing, from the original §3 pass)

**(a) The old fixed-60 windows were not 3-month windows on sparse tapes.** EG_BTFH's worst
60-session window spanned **343 calendar days** — an 11-month outcome scored as a quarterly
forecast. Medians were fine (~90–94 days); the tails were badly wrong. DSCW is the extreme case: 15
gaps over 20 days in 2012–2017, one of **373 days**, and at origin 260 its trailing 252 sessions
span **1,936 calendar days**. The calendar convention exposes this by construction. Worth deciding
whether DSCW's pre-2018 tape should be in a panel at all under the Step 0.0 density rule. Unaffected
by the merge (BTFH/DSCW raw files weren't touched by any concurrent commit).

**(b) `panel_hashes.json` was stale for all 30 EG names**, pre-merge. Recorded hashes didn't match
the committed raw files though the raw files were unmodified, so the content-hash cache silently
never applied to the largest market. Fixed on this branch pre-merge. **It recurred independently on
`main`** for AE and SA (and for RMDA/CLHO inside the merge-conflict block) once their libraries grew
without a matching panel/hash rebuild — see §3b. Fixed again, same way: recompute from the actual
file, never trust either side's stored string.

---

## 5. Site

- **`ledger.html`** — convention explainer (`#hz-note`); horizon-aware sorting by actual length
  (a raw string compare would sort "12 months" before "3 months"); **data-driven countdown**,
  which had been hard-coded to "9 July 2026, PHDC T+20" and had gone stale; and a plain-calendar
  date formatter. That last one is a real bug fix: `new Date("2026-08-17")` parses as UTC midnight,
  so **every grade date rendered a day early for readers west of UTC** — on a page whose whole
  subject is *on what date*. Confirmed post-merge: main's own `COHORT_OHLC` additions and the
  roll-forward-graded rows for OCDI/ORHD/Gold/Samsung coexist correctly with all of the above.
- **`assets/app.js`** — fan axis, touch-ladder headers and hover read-out now driven by an optional
  per-ticker `hz:{h1,h3,l1,l3,cal}`. Absent `hz` = legacy 20/60. Verified byte-identical rendering
  on legacy tickers (PHDC, TMGH), and confirmed the calendar path renders
  `latest | 10d | 1 month | 31d | 41d | 52d | 3 months`.
- **`assets/data.js`** — schema documents both conventions; no row's numbers touched. Confirmed
  post-merge: main's roll-forward-graded LEDGER rows (162 total) are intact.
- **`method.html`** — new `#horizons` section defining the rule and the changeover.

**Deliberately left alone:** `extra.html` and `elm.html` carry "Monte-Carlo — T+60 median" rows
inside published valuation cross-checks. Those numbers *were* struck at T+60; relabelling them
"3 months" would misstate their provenance. They restrike at the next roll-forward. Same reasoning
for `publish_adh.py` / `build_adh_*.py`, which are dated one-off publish records. `ar/` is
redirect stubs only.

---

## 6. Open, needs a decision

1. **Adopt or not.** `market_profiles.py` still carries the 60d fit (verified zero diff against
   `origin/main` after the merge). `auto_refresh.HORIZON_TAG` is set to `'3m'`, so the next
   pipeline run compares a calendar fit against a 60d incumbent, the materiality gate fires, and it
   opens a PR instead of auto-committing — intended, not a fault.
2. **SA/EXTRA's FAIL** — publish the FAIL, or extend the adaptive-width overlay to SA first (it
   would have to clear the same LONO gate on SA's own panel). Now confirmed robust on 2x+ the data
   at both horizons (§3b) — the extra history did not soften this.
3. **SA/AE recalibration debt (new, §3b).** AE-60d and SA-60d/3m all breach the 5% cone-move gate
   against today's live production numbers, for reasons unrelated to this PR (a concurrent
   long-history ingest that was never followed by a refit). This needs its own review, separate
   from the calendar-horizon decision.
4. **Matured, ungraded cohorts** — the §-3 original list (OCDI, ORHD, Gold, Kakao, LGES, Samsung,
   COMI, EMAAR) is now **partly stale**: main's concurrent roll-forward already graded OCDI, ORHD,
   Gold, and at least part of Samsung's cycle. Kakao, LGES, and COMI/EMAAR's status was not
   independently re-checked in this session — needs a fresh look before treating any of them as
   still outstanding.
5. **The project-instructions block** needs its Step 0 line changed from `h=60` to the calendar
   rule. That block is a rules document, so this is a rule change, not a number change.
6. **`adaptive_width.py`** is confirmed **absent from `main` and from this branch** (checked
   directly, not assumed). A dedicated branch `feat/adaptive-width-overlay-eg` exists on the
   remote; its contents weren't fetched/inspected in this session since the overlay is out of scope
   for this PR. Don't assume it's live anywhere until that branch is actually reviewed and merged.

---

## 7. Resolution (same day, later) — items 1–3 closed; how, and what it cost

Picked up in a later conversation the same day. Sequence, in order:

**Push-policy change, twice over (full detail: `Push_Policy_Decision_20260727.md`).** First,
material Claude-prepared engine changes moved from "always PR" to "match the bot's own
materiality gate" (PR only when actually material). Later the same day, further loosened to
"Claude pushes straight to `main` even when material, once the user gives an explicit go-ahead in
chat" — no branch, no PR, for Claude-prepared changes specifically. Both revisions are why
everything below shipped as direct pushes to `main`, none as PRs.

**Item 3 (SA/AE recalibration debt) closed first**, independently, before calendar horizons were
touched again: AE and SA's 60d fits were re-verified against the grown library and pushed straight
to `main` (nu 10→8/cal 1.028→0.895 for AE, −10.68%; nu 6→8/cal 1.063→1.021 for SA, −8.08%), each
with full per-name verdict detail in `market_profiles.py`'s own `fit_meta`. Caught and fixed a
mid-flight problem the hard way: `origin/main` moved (unrelated concurrent `portfolio.html` work)
between branching and pushing — the naive fast-forward would have silently reverted that work.
Fetch-compare-merge-reverify before every push from here on, not just the first time.

**Item 1 (adopt calendar horizons or not) resolved market-by-market, not as one switch.** Re-ran
KR/US/QA/AE/EG/SA/XAU/XPT/IN fresh against the (by-then-further-grown) library rather than trusting
the §3/§3b tables above, which caught two more problems:

- The one available precomputed 3m file (`calendar_horizon_refit_3m.json`) had a **stale KR
  entry** — its baseline predated KR's own 60d refit that had, by then, separately landed on
  `main`. Cross-checked every other market's `_incumbent` field in that file against live
  `market_profiles.py` before trusting any of it; KR was the only one that failed the check.
- A first pass screened only the market-level band-move number and nearly cleared EG and SA as
  "safe" — both have market-level moves under 5%. Checking **per-name** verdicts caught real
  churn hiding under that average: EG had 15 of 30 names change category (5 losing PASS); SA had
  MAADEN lose PASS. Market-level screening alone would have missed both.

User then set a standing rule mid-session — **don't auto-adopt for a worsening market or name**
— which produced a genuine three-way split, not a single yes/no:

- **KR, US, QA** had zero worsening (band flat-or-narrower, no name moves to a worse category) and
  were adopted on that basis alone, no further sign-off asked. QA's one verdict change (IQCD
  FAIL→PARITY) was flagged in `fit_meta` as a precision-loss artifact (fewer/noisier quarterly
  windows widening the CI, not an improved point estimate) rather than presented as clean good
  news, even though it satisfied the rule's letter.
- **AE, EG, SA, XAU, XPT, IN** each had a real, specific worsening (see the table in the closing
  chat message of that conversation, or `market_profiles.py`'s own per-market `fit_meta` — every
  one is documented inline, not summarized away) and were held back pending explicit sign-off.
- User then gave that sign-off explicitly ("switch all to one month and 3 months") after one round
  of confusion about which horizon was even in question (worth knowing: they briefly asked to
  keep the long horizon at 60 days instead of 3 months, which would have been a real scope cut —
  confirmed via a clarifying question before doing anything, and the answer was to proceed with
  both as originally specified, not to cut scope). All six shipped with every worsening spelled
  out in the commit message and in `fit_meta`, not smoothed over.

**Final state, verified live via anonymous `raw.githubusercontent.com` reads, commit `48bc1f5`:**
all 11 market profiles (EG, SA, US, KR, AE, IN, QA, XAU, XPT, plus placeholder GB/BR) are on the
calendar 3-month fit. `HORIZON_TAG='3m'` in `auto_refresh.py` now matches what's actually in
`market_profiles.py`, so the next scheduled pipeline run should find nothing material left to flag
for these nine markets — that's an expectation to check when it fires, not a guarantee.

**Items 2 (SA/EXTRA's FAIL) closed as a side-effect, not a separate step:** EXTRA is a robust FAIL
under both the 60d push and the 3m push (skill −0.0308 and −0.0372 respectively) — confirmed twice
over on the grown library, in both window conventions. It is live. No separate publish action was
taken or needed beyond the two calibration pushes above.

**Items 4, 5, 6 remain exactly as stated above — untouched by this resolution.** In particular,
item 5 (persistent project-instructions text still says `h=60` and still says "always PR for
engine changes") is now stale in *three* ways, not one — see `Push_Policy_Decision_20260727.md`
for the exact replacement language for both push-policy revisions; the h=60→calendar wording still
needs drafting whenever the user next has access to edit that claude.ai project setting.
