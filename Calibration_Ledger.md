# Calibration Ledger

**Purpose.** This is the Monte Carlo counterpart to `Fundamental_Driver_Ledger.md` — the append-only
scoreboard that grades every published price-distribution forecast against what actually happened.
Where the Forecast-Assumptions Log scores individual *assumptions* name-by-name, this ledger scores
the *whole forecast distribution* for a ticker at a given horizon: pass/fail on CRPS skill versus a
zero-drift random-walk benchmark, per the published research standards's grading rule.

**Source of truth.** The live, authoritative copy of this ledger is the `LEDGER` array in
`assets/data.js` (repo: `sherifomarsaleh/testahil`), rendered publicly at `testahil.com/ledger`. This
file is a **read-only mirror** for reference inside this project — human-readable, not
machine-updated. If the two ever disagree, `data.js` wins. Do not hand-edit rows here expecting them
to propagate to the site.

**Discipline this ledger enforces (same as the live site):**
- Append-only. A row is anchored at publication and never deleted, even if the forecast is later shown
  to have failed calibration.
- Every row logs `anchor_vol` + `horizon_days` implicitly via `anchor_date`/`grade_date`, so the
  benchmark can always be rebuilt.
- Grading happens at `grade_date` via `ledger_scorer.py` (CRPS skill vs. zero-drift random-walk,
  interval score, PIT) — never self-certified in the study itself.

---

## HORIZON CONVENTION — CHANGED 27-JUL-2026

Cohorts struck **on or after 27-Jul-2026** are graded at **1 month** and **3 months** —
calendar horizons. `grade_date` is `anchor_date + N calendar months` (month-end clamped),
rolled forward to the first real trading session on that exchange if the target is closed.
`horizon_days` is whatever session count spans that window (≈21 and ≈63, varying by market and
month), projected at publish time by `engine/horizons.py` and re-resolved against the real
calendar at grade time.

Cohorts struck **before** that date keep **session-counted** — a fixed 20 or 60 sessions, with a
`grade_date` projected on a naive Sun–Thu calendar. **They are not re-labelled and not
re-struck.** They grade on the horizon they were issued on and count in the score exactly as
before; append-only governs. `horizon_label` is the field that says which convention a row
belongs to. Full rationale in `engine/Standing_Research_Protocol.md` → Step 0 → *Horizon
convention*.

The change was made because the old convention's error landed in the check DATE: the projected
Sun–Thu `grade_date` had no holiday awareness, so it routinely fell ~2 sessions short of a true
1 month — every graded row so far (PHDC, TMGH, EMFD) carries a `grade_note` recording exactly that
correction. A calendar target cannot drift.

---

## Snapshot as of 2026-07-09

> **Stale — this snapshot predates both the first three grades and the 27-Jul-2026 horizon
> change. Kept as the dated record it is; `assets/data.js` is the source of truth.**

- **112 anchor rows** logged (1 month and 3 months per instrument), across **55 covered instruments**
  (EGX, GCC/international equities, and metals).
- **0 rows graded so far.** Every row is still `pending` — no horizon has matured yet. The first
  scheduled grading event is **PHDC's 3 months cohort on 2 September 2026**, per the Business Plan's
  Phase 0 schedule and the Operating Manual's hard-date flag.
- Schema (per row): `instrument`, `asset_class` (equity | metal | other), `anchor_date`,
  `anchor_price`, `ccy`, `horizon_label`, `grade_date`, `cycle_no`, `p5..p95`, `touch` bands. Grade-time
  fields (`realized_close`, `in_90`, `in_50`, `realized_quantile`, `median_err`, `touch_hit`) stay
  `null` until `grade_date`.

## the calibration back-test status — SNAPSHOT AS OF 2026-07-09, SUPERSEDED

> **STALE — DO NOT CITE. Superseded by the 2026-08-24 snapshot below.** This table carried no date
> and no expiry banner, so it read as current for 46 days while the fits underneath it were refit
> repeatedly. Every verdict in it has since moved. Two examples of how wrong it had become:
> **AGTHIA is listed FAILED here and is PARITY today** (skill −0.0142 on the 28-name AE panel), and
> the ALPHADHABI row describes the AE fit as "1-name PROVISIONAL (Gaussian, cone width 1.042)" when
> AE is a 28-name panel at ν=10.0 / width_cal 0.916 that now PASSES its market gate. Kept, not
> deleted, as the dated record it is — [R-DOC-02]: a status sentence is a claim about the world and
> it rots, so it carries the date it was true.

This is the *pre-publication* CRPS-skill test (the calibration back-test), not the ledger's post-hoc grading — but it's
tracked alongside the ledger because a the calibration back-test failure changes how a row's eventual grade should be
read (an indicative-only forecast failing calibration later is expected, not a surprise).

| Ticker | Status | Detail |
|---|---|---|
| **KABO** | FAILED | CRPS skill −0.010 vs. random walk (Appendix B). No price forecast published; §3 is an illustrative volatility map only. |
| **AGTHIA** | FAILED | CRPS skill < 0 vs. random walk. §3 marked indicative only, not skill-validated. |
| **ISPH** | FAILED | CRPS skill < 0 vs. random walk. §3 marked illustrative only, not skill-validated. |
| **MAADEN** | FAILED | Monte Carlo lens showed no skill. §3 is a probability map, not a validated forecast. |
| **QGTS** | TIES (does not beat) | Unusually stable name — engine ties, rather than beats, a random walk. §3 illustrative only. |
| **ALPHADHABI** | PARITY (v3 gate) | CRPS skill +0.006, 90% CI [−0.008, +0.016] spans zero; robust across blocks {2,3,4}. AE fit is 1-name PROVISIONAL (Gaussian, cone width 1.042) per the QGTS precedent. Published on the parity tier; anchor 03-Jul-26 pre-dates the 7–8 Jul ceasefire collapse (timing-flagged). |
| **LCSW** | PASSED | No failure note attached; confirmed calibration pass per memory and site content. |
| *(all other covered names)* | Presumed passed | No failure/tie note found in `coverage.js`; not individually re-verified line-by-line in this snapshot. |

**Note on this snapshot vs. prior memory:** earlier working memory recorded only KABO, QGTS, and
MAADEN as confirmed failures. Pulling the live `coverage.js` text directly for this file surfaced two
more — **AGTHIA and ISPH** — also carrying explicit the calibration back-test-failure notes. Treat this ledger file as
the more current source on failure status; worth reconciling into standing memory.

---

## Snapshot as of 2026-08-24

Read live from `assets/data.js` (LEDGER) and `engine/market_profiles.py` + `engine/fitted_configs.json`
at the moment of writing — never from memory or from the sections above. Regenerate the same way.

**Ledger size.** **271 rows** across **93 covered instruments** — 246 equity, 13 metal, 12 other.
**41 graded, 230 open** (99 × 1-month, 129 × 3-month, 2 × metals 12-month).

**How the cone has actually scored.** All 41 graded rows are 1-month windows; **no 3-month cohort has
matured yet**, which is exactly what the 29-Jul-2026 forecast-lifecycle adoption predicted — before it,
no 3-month forecast ever survived to grading at all, and the first ones are still running to their dates.

| | result | target | read |
|---|---|---|---|
| inside the 90% band | **38 / 41 = 93%** | 90% | slightly over-covered — the band is honest, marginally wide |
| inside the 50% band | **23 / 41 = 56%** | 50% | same direction, same size |
| mean PIT | **0.572** *(38 of 41 rows)* | 0.500 | outcomes land a little above centre |
| mean median error | **+3.28%** *(41 of 41 rows)* | 0% | the centre has run modestly low against realised prices |

The PIT denominator is 38, not 41: **Samsung (2026-06-26), OIH and RMDA (both 2026-07-22) carry a
`realized_close` but no `realized_quantile`**, so they score coverage but not centring. The denominator
is printed because averaging three missing values into 41 silently reports 0.530 instead of 0.572 —
a difference that reads as "better centred than it is" and is invisible unless the basis is stated.
Worth closing at source in `grade_ledger.compute()`; not repaired here, since a graded row is permanent.

Over-coverage on both bands with a PIT above 0.5 is one coherent story, not two: the cones are a touch
wide and the centre a touch low. It is the same signature the per-name width overlay was built for, and
it is a small sample — 41 windows, one horizon, no 3-month evidence yet. It is not a licence to narrow
anything by hand.

**Live fits** (the pooled (ν, width_cal) pair is the fitted object; ν alone is weakly identified and must
never be quoted as precise):

| market | ν | width_cal | signal | panel verdict | names | windows |
|---|---|---|---|---|---|---|
| AE | 10.0 | 0.916 | mom_combo (active) | **PASS** | 28 | 407 |
| EG | 5.0 | 0.958 | mom_combo (active) | PARITY | 37 | 618 |
| SA | 12.0 | 1.063 | mom_12_1 (active) | PARITY | 13 | 446 |
| IN | 6.0 | 1.021 | — | PARITY | 3 | 172 |
| KR | 8.0 | 1.070 | — | PARITY | 3 | 125 |
| QA | 6.0 | 0.951 | — | PARITY | 3 | 174 |
| US | 12.0 | 1.084 | — | PARITY | 3 | 174 |
| XAU | 12.0 | 0.958 | — | PARITY | 2 | 120 |
| XPT | 8.0 | 0.860 | — | PARITY | 1 | 58 |

BR and GB carry no fit and no registered index — no conforming beta is possible there.

**Names not at PASS or PARITY.** Everything not listed is PASS or PARITY; absent means unremarkable,
which is the common case and deliberately not enumerated.

| market | name | verdict | skill |
|---|---|---|---|
| AE | BOROUGE | **FAIL** | −0.0582 |
| AE | EMPOWER | **FAIL** | −0.0252 |
| EG | CLHO | **FAIL** | −0.0201 |
| SA | EXTRA | **FAIL** | −0.0372 |
| AE | LULU | PROVISIONAL (insufficient windows) | −0.0646 |
| AE | AMR | BOUNDARY (PARITY-flagged) | −0.0123 |
| AE | BURJEEL | BOUNDARY (PARITY-flagged) | +0.0701 |
| AE | DIB | BOUNDARY (PARITY-flagged) | +0.0344 |
| AE | EAND | BOUNDARY (PARITY-flagged) | +0.0408 |
| EG | ARCC | BOUNDARY (PARITY-flagged) | −0.0190 |
| EG | FWRY | BOUNDARY (PARITY-flagged) | +0.0184 |
| EG | OCDI | BOUNDARY (PARITY-flagged) | +0.0329 |
| EG | PRDC | BOUNDARY (PARITY-flagged) | +0.0295 |
| EG | RAYA | BOUNDARY (PARITY-flagged) | −0.0304 |
| IN | INFY | BOUNDARY (PARITY-flagged) | −0.0114 |
| QA | QNB | BOUNDARY (PARITY-flagged) | +0.0190 |
| US | NVDA | BOUNDARY (PARITY-flagged) | −0.0234 |

**Metals remain the weakest calibration in the system** and the table above should not be read as
softening that: gold is a single-name self-fit and therefore circular, and silver is published on gold's
fit with none of its own. Silver, copper and platinum history is what fixes it.

**Nothing gradable today.** 19 open rows reached their calendar grade date of 2026-08-24 and none could
be graded: no library holds that session's close yet. They stay open and grade on the first session that
covers the date — the horizon is a calendar commitment, so they have matured; they are simply unsettled.

---

## How to use this file

Before citing a specific ticker's calibration status or ledger grade in a study or conversation,
prefer re-pulling the live `data.js` LEDGER array or `coverage.js` notes over this snapshot if it's
more than a few publish-cycles old — this file will drift out of date the moment a new grade lands
and isn't regenerated. Its value is as a fast, readable reference of the *shape* of the ledger
(schema, current pass/fail roster, snapshot counts), not as the live grading feed itself.
