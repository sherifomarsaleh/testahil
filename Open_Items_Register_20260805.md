# Open Items Register — 05-Aug-2026 (rev. 3)

Every open item across the whole project history (16-Jun → 05-Aug). Continues the 29-Jul rev. 2
register (which lived outside the repo as a session artifact — this revision commits the register
into the repo so it survives sessions). Same discipline as rev. 2: items re-checked against
**live `main`** where the repo can answer, closures moved to Section D rather than left to
resurface, and every claim tagged.

Verification tags: `[LIVE]` = confirmed against `main`/`data.js`/GitHub on 05-Aug-2026.
`[DOC]` = carried from rev. 2, not independently re-verified this pass.
`[MEASURED 05-Aug]` = established by this session's diagnostics (QNB roll-forward PR #63 and the
calibration research after it); the numbers are in that PR's thread and the session record.

**Rev. 3 headline:** the 29-Jul stall is over — 0 matured-ungraded cohorts (was 19), 0 open PRs
(was 10), adaptive-width wired in (was code-without-callers), all four 29-Jul data defects
(11b–11d + the garbage stamp) verified closed. The register's weight has shifted from "the loop
is stalled" to "known engine questions, measured and triaged."

---

## A. HIGH IMPACT

Something published is wrong, unsourced, or not moving.

### A1 — Published output is wrong or unverifiable

| # | Item | Unblocked by |
|---|------|--------------|
| 1 | **~27 live Egyptian DCFs are materially understated** by the retired flat-WACC convention. GBCO must be re-issued outright; STC was never default-spread-normalised (~0.5% on the equity leg). `[DOC]` | Each name's next rebuild; GBCO needs a full v2 re-run |
| 2 | **RMDA's delivered study reported PARITY where production's break-filtered fit says robust PASS.** `[DOC]` | Re-run Step 0 under the engine-reconciliation assert, re-issue the block |
| 3 | **Published silver study still carries the refuted "Hormuz unwind" crash attribution** for 30-Jan-2026. `[DOC]` | Silver's next refresh (append-only, corrects forward) |
| 4 | **HELI's cycle-1 cohort is anchored on a session not in its own library**; **LCSW's published anchor is 29.45 against a 30.10 tape (+2.21%)**; 14 sub-1% anchor-vs-tape warnings. `[DOC]` | A decision: annotate, re-strike, or root-cause the capture path first |
| 5 | **Carry anchors are unsourced in four markets.** SAR rf is a SAMA-repo estimate, EGP needs a fresh 3M T-bill quote, IN carries a flat 6.50% placeholder, QA is a QCB-tracking estimate (`[LIVE]` — the QA profile still carries its own FLAG, and QNB has now published two cycles under it). | Sourcing a real local yield per market |
| 6 | **`q_annual = 0` on every name.** Still a correctness defect — but now bounded: `[MEASURED 05-Aug]` a location shift at the 3-month horizon is ~0.08 of the cone's sigma, so the CRPS/calibration impact of fixing it is small; the published MEDIAN is what moves (down, by roughly the yield). Fix for honesty of the centre, not expecting a skill gain. | Sourcing per-name dividend yields |
| 7 | **Index cones (EGX30/EGX70) have no index profile** — FAIL verdict confounded by the single-stock fit and an unsourced index yield. `[DOC]` | Sourced index yield + index-appropriate Step 0.0 threshold + own fit |
| 8 | **ISPH publishes a single ERP basis**, against the standing dual-basis rule. `[DOC]` | Add the CDS-basis WACC and reissue |
| 9 | **Year-1 declining-WACC off-by-one fixed in ORHD and ISPH only** — never swept across the rest of the EGX declining-WACC library. `[DOC]` | Open each model, confirm FY26E multiplier starts at `*0` |
| 9b | **NEW 05-Aug:** `engine/metal_backtest.py:367` hardcodes the y-axis label `'Price (USD, log)'`, so **every non-USD calibration panel mislabels its currency** (e.g. `calibration_QNB.png` reads USD over QAR values). `[LIVE]` One-line code fix, but fixing it honestly means regenerating all 74 panels in the same commit — the generator and the pages must not disagree. | The next occasion a fleet-wide panel regeneration is warranted anyway; do not run the fleet for the label alone |

### A2 — The loop (formerly "stalled" — now moving; what remains)

| # | Item | Unblocked by |
|---|------|--------------|
| 10 | ~~19 matured cohorts ungraded~~ **CLOSED — see D.** | — |
| 11 | **Stale libraries, shrunk from 4 to 1 + two stale CONES** `[LIVE]`: PLATINUM's library still ends 2026-07-20 (its 14-years-off stamp is fixed — see D — but the data is 16 days old). Separately, `check_data_freshness.py` WARNs two cones lag their own libraries: **ORAS** anchored 2026-07-22 vs a library at 2026-07-29 (a full week), **SAMSUNG** 2026-07-27 vs 2026-07-28 (one session). IQCD/QGTS were re-struck 28-Jul with matching stamps; QNB is fully current (05-Aug, PR #63). | PLATINUM: one vendor export. ORAS/SAMSUNG: `refresh_cone_one.py` mid-cycle pass (STEP 0 decision (a)) on next touch — ORAS is the one worth a pass of its own |
| 12 | **Library refresh is entirely manual.** No feed; if nobody posts, everything sits still. `[DOC]` | A standing posting cadence, or a wired feed |
| 13 | ~~adaptive_width merged but not wired~~ **CLOSED — see D.** | — |
| 14 | ~~Ten open PRs, nothing reviewed~~ **CLOSED — see D.** | — |
| 15 | **Two GitHub PATs pasted into chat on 26-Jul should be revoked.** `[DOC]` — cannot be verified from the repo; stays open until confirmed revoked. | Revoking both in GitHub settings |

### A3 — Engine questions, known and measured

| # | Item | Unblocked by |
|---|------|--------------|
| 17 | **Per-origin vol estimation is still not break-aware — but now MEASURED, and it is not what it was suspected of.** `[MEASURED 05-Aug]` Re-running the production width chain with post-break-only training at every panel origin: EG **−0.76%** cone width (not the cause of Egypt's width — that is the deliberate devaluation insurance), AE −3.2%, SA **+2.96%** (via the HAR-coefficient channel, not s2 — and in the direction SA's genuine narrowness needs, ~1/6 of the gap). Downgraded from "more material as libraries grow" to a small, per-market redistribution. | Only worth promoting as part of a Saudi width fix (see #22); not on its own |
| 18 | **Gate CRPS is scored in price space** (non-convergent for a lognormal-t) with sampled rather than exact CRPS; published CIs understate uncertainty. `[DOC]` | Move panel scoring to log-space or a bounded score, restate CIs |
| 19 | **Known residual leakage in the refit loop**: market LONO scale pools other names' full histories. Judged small, deferred. `[DOC]` | A fully-jackknifed scale |
| 20 | **Block-mixture fix for h>60 not adopted**; the 12-month gold cohort sits outside the validated horizon. `[DOC]` | A 240d/480d walk-forward coverage test |
| 21 | **The project-instructions block still reads `h=60` / `T+20/T+60`** — calendar-horizon adoption never made it in. `[DOC]` — outside the repo, only the owner can edit it. | Owner edit; replacement text drafted in four docs |
| 22 | **NEW 05-Aug: Saudi's cone is genuinely too narrow — the one statistically real width misfit in the system.** `[MEASURED 05-Aug]` Standardized-residual sd 1.135, 90% cluster-bootstrap CI [1.028, 1.233] (58 origin-quarter clusters) — the only market whose CI excludes 1. LONO-estimated widening improves scale-normalized CRPS +0.11% with 7/11 names better (z≈0.9) — real but **below the promotion bar; NOT promoted.** For contrast: EG 0.892 is the documented insurance choice, XPT 0.800 is one 58-window name, the other six markets are calibrated (pooled sd 0.994, CI [0.916, 1.083]). | Re-run the same LONO test unchanged after ≥2 more metronome cycles of SA grades, or new SA names past 11 |
| 23 | **NEW 05-Aug: conditional-width (FX-premium) project — feasibility gate PASSED, design stage owed.** Egypt runs one width across two regimes: deval windows on target (87.9% on the 90% band, 107 windows), calm windows over-wide (92.7%, 1,295). `[MEASURED 05-Aug]` Parameter-free ranking test, 32 quarters 2018Q1–2025Q4, prior-month data only: the parallel-market/NDF premium ranked **all four devaluations top-quartile** (#7 #5 #2 #1, AUC 0.915, robust to ±50% input jitter), vs 0.768 for trailing equity vol — which was blind exactly at cycle entry (2022Q1 ranked #17). **REER gap (0.536) and freeze-pressure (0.433) are DEAD — do not revive.** Limits: 4 events; premium series was a journalistic reconstruction anchored to the committed CALC block. | In order: (a) design note in `engine/` fixing indicator, source, and acceptance criteria BEFORE any code; (b) properly sourced monthly premium series (four-field INPUTS rule); (c) promotion test = deval-window coverage held-or-improved AND LONO CRPS not worse — never headline skill, per the 2024-cut trap in the EGYPT profile comment |

---

## B. LOW IMPACT / BACKLOG

Carried from rev. 2 `[DOC]` except where tagged; nothing published depends on these today.

**Calibration & panels** — IN wants a 4th NSE name (TMPV 43.7% weight); EGX70's 6.5 usable years
(standing caveat); RAYA's 34.6% flat sessions need an exclude-or-fallback decision; three robust
name-level FAILs (ELM, LGES, IQCD) with no remedy; AE/LULU PROVISIONAL, AE/ADCB BOUNDARY pending
next grade; SA `mom_12_1` and AE `rev_1m` ablations owed; GB/BR are stubs; full-sample PASS→PARITY
degradation unexplained.

**Metals** — gold circular self-fit; silver borrows gold's fit; platinum provisional single-name;
PR #16's pooled 3-metal fit was part of the drained PR queue — whether it merged or closed
unmerged was not re-verified this pass, so the underlying fit-group question stays here; copper
still a placeholder page (`[LIVE]` 6.9 KB); platinum cross-marks re-quote at first grade
(12-Oct-2026).

**Selection engine** — pre-registration v1 unsigned, v2 owed; no factor adoptable on EG alone;
F5 (Amihud) data-quality-unverified; survivorship bias must appear on any published selection
result; FV shadow-cohort monthly grading trigger should be reinstated (first maturity mid-Oct
2026). (Note: the Selection Engine R&D folder was removed from the repo in #62 — the register
items stand, the code home moved.)

**Parked ideas** — Bayes-Stein shrunk drift, MSGARCH regime vol, GJR-FHS substrate, conformal
wrapper, CSAD herding, event-time HAR, HMM DoF. **Rev. 3 updates two of these:** the GDR/shadow-FX
premium idea is no longer parked — it graduated to item #23. And every *drift*-family idea
(Bayes-Stein included) now carries a measured ceiling: `[MEASURED 05-Aug]` at a 3-month horizon
any drift change is ~0.08σ of the cone — LONO-tested best variant +0.31% CRPS at 51% name breadth
(a coin flip). Drift cannot pay at these horizons; parked ideas in that family should be evaluated
against that arithmetic before any build.

**Studies & pages** — RMDA paused mid-pipeline (SIGCM clause-1); ORAS fundamentals never supplied;
XPT study pack unpublished; ISPH lighter-note caveats; IHC weighted-central footing (104.5 vs
104.75); source-tag retrofit deferred; `dist.t20/t60` retired naming across ~80 files; `hz` written
but unread; one-sided touch ladders (EMFD, PHDC, HELI, OCDI, Samsung) need a human re-pick.

**Tooling & ops** — still no `engine/grade_cohorts.py` (`[LIVE]` 404): every grade remains
per-session script work — the QNB pass had to re-validate the grading convention by replaying all
12 prior rows, which is exactly the cost of not having this module; no ADX General Index or EGX30
series in the repo (`[LIVE]` — beta regressions and RMDA still blocked on this); no route to
testahil.com's served bytes; automated study pipeline v1 awaiting sign-off; local clone refspec
pinned to `main`.

---

## C. Driver Ledger — 39 open rows

Unchanged from rev. 2: all genuinely open, none actionable until its scheduled disclosure.
**GBCO rows 1–6 unblock first — 2Q26 results, 11-Aug-2026, six days from this revision.**
STC rows 7–12 (FY26), ALPHADHABI 13–20, EAND 21–36, XPTUSD 37–39 (first T+60 grade 12-Oct-2026).

Both structural fixes remain unadopted: named source for every ownership % and consideration
("press-cited/estimated" in a delivered study = QC fail), and a pre-publish check that each
driver's narrated value equals its wired-in value.

---

## D. Verified CLOSED since rev. 2

Listed so they don't resurface as phantom work. (Rev. 2's Section D closures all still stand.)

| Item | Evidence |
|------|----------|
| **#10 — 19 matured cohorts ungraded** | `[LIVE]` 0 open LEDGER rows with `grade_date <= 2026-08-05`; the 29-Jul lifecycle adoption (one current forecast per name/horizon, 143 legacy rows cleaned) plus the daily passes since cleared the backlog. Lifecycle invariant asserted 05-Aug: 150 open pairs, 0 violations, 0 overdue |
| **#11 (QNB leg) — QNB/IQCD/QGTS stale libraries** | `[LIVE]` QNB current to 05-Aug (PR #63, graded + re-struck); IQCD/QGTS re-struck on the 28-Jul close with `asof.mc.data = 2026-07-28` matching their spots |
| **#11b — fresh spot beside stale cone (IQCD/QGTS)** | `[LIVE]` both now carry `asof.mc.data` equal to their spot date — cone and spot move together |
| **#11c — nine names lost `asof` entirely** | `[LIVE]` all nine (TMPV, TSLA, RELIANCE, NVDA, INFY, AAPL, SAMSUNG, KAKAO, LGES) carry full `asof` blocks again |
| **#11d — PLATINUM's garbage "2012-01-05" stamp** | `[LIVE]` now reads `mc: 2026-07-20/2026-07-20` — sane, though the library itself is still stale (see #11) |
| **#13 — adaptive-width landed but not wired** | `[LIVE]` `strike_cohorts.py` imports `adaptive_width` and calls `live_width_mult()` in the production strike; EGYPT profile carries `width_overlay_active=True` (EG-only, MIN_WINDOWS=28-gated) |
| **#14 — ten open PRs, oldest 23-Jul** | `[LIVE]` GitHub reports **zero** open PRs on 05-Aug |
| **"The system is overly cautious" — refuted as a premise** | `[MEASURED 05-Aug]` pooled standardized-residual sd 0.994 (cluster CI [0.916, 1.083]); PIT coverage 53.5/81.8/90.1 vs 50/80/90 on 3,374 windows; six of nine markets individually calibrated. The one real misfit runs the other way (see #22) |
| **Risk-premium / market-wise drift as a CRPS lever** | `[MEASURED 05-Aug]` closed structurally: +6.3%/yr realized premium ex-US is 0.08σ over 3 months; best LONO variant +0.31% at 51% breadth. Confirms the earlier sessions' "everything nearly the same" finding, now on arithmetic |
| **Distribution shape (skew / tail family) changes** | `[MEASURED 05-Aug]` pooled skew +0.09 with inconsistent signs across markets; kurtosis misfits point in opposite directions (AE fatter than its ν, EG thinner). No systematic change supported |
| **`run_date` missing from single-name strike rows** | Fixed in PR #63 (`apply_rollforward.js_row` + `rollforward_one`); `check_data_freshness.py` now passes 0 failures |
| **Roll-forward notes hardcoding "last week's story"** | Fixed in PR #63: metronome status now read off the ledger (`_prior_1m_matured`, validated against a node-parsed ledger across all 74 instruments) |

---

## The short version

The stall that dominated rev. 2 is cleared: nothing matured sits ungraded, the PR queue is empty,
adaptive-width is live, and all four 29-Jul data defects are verified closed. What rev. 3 adds is
triage by measurement: the calibration is sound in aggregate (0.994), drift-family work is closed
by arithmetic, and exactly three engine-side things deserve attention — **Saudi's too-narrow cone
(#22, parked with a re-test trigger), the conditional-width project (#23, gate passed, design note
owed), and the currency label on 74 panels (#9b, waiting for the next fleet regeneration).**

The most-ground-clearing actions now: **ORAS's week-stale cone (#11)**, **PLATINUM's export
(#11)**, and — first calendar deadline — **GBCO's 2Q26 results on 11-Aug (Section C), which also
reopens #1's flat-WACC re-issue for the name it hits hardest.**
