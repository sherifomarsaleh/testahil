# Calibration Ledger

**Purpose.** This is the Monte Carlo counterpart to `Fundamental_Driver_Ledger.md` — the append-only
scoreboard that grades every published price-distribution forecast against what actually happened.
Where the Fundamental Driver Ledger scores individual *assumptions* name-by-name, this ledger scores
the *whole forecast distribution* for a ticker at a given horizon: pass/fail on CRPS skill versus a
zero-drift random-walk benchmark, per the Standing Research Protocol's grading rule.

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

## Snapshot as of 2026-07-09

- **112 anchor rows** logged (T+20 and T+60 per instrument), across **55 covered instruments**
  (EGX, GCC/international equities, and metals).
- **0 rows graded so far.** Every row is still `pending` — no horizon has matured yet. The first
  scheduled grading event is **PHDC's T+60 cohort on 2 September 2026**, per the Business Plan's
  Phase 0 schedule and the Operating Manual's hard-date flag.
- Schema (per row): `instrument`, `asset_class` (equity | metal | other), `anchor_date`,
  `anchor_price`, `ccy`, `horizon_label`, `grade_date`, `cycle_no`, `p5..p95`, `touch` bands. Grade-time
  fields (`realized_close`, `in_90`, `in_50`, `realized_quantile`, `median_err`, `touch_hit`) stay
  `null` until `grade_date`.

## Step 0 calibration status (pass/fail gate, separate from the ledger's own grading)

This is the *pre-publication* CRPS-skill test (Step 0), not the ledger's post-hoc grading — but it's
tracked alongside the ledger because a Step 0 failure changes how a row's eventual grade should be
read (an indicative-only forecast failing calibration later is expected, not a surprise).

| Ticker | Status | Detail |
|---|---|---|
| **KABO** | FAILED | CRPS skill −0.010 vs. random walk (Appendix B). No price forecast published; §3 is an illustrative volatility map only. |
| **AGTHIA** | FAILED | CRPS skill < 0 vs. random walk. §3 marked indicative only, not skill-validated. |
| **ISPH** | FAILED | CRPS skill < 0 vs. random walk. §3 marked illustrative only, not skill-validated. |
| **MAADEN** | FAILED | Monte Carlo lens showed no skill. §3 is a probability map, not a validated forecast. |
| **QGTS** | TIES (does not beat) | Unusually stable name — engine ties, rather than beats, a random walk. §3 illustrative only. |
| **ALPHADHABI** | PARITY (v3 gate) | CRPS skill +0.006, 90% CI [−0.008, +0.016] spans zero; robust across blocks {2,3,4}. AE fit is 1-name PROVISIONAL (Gaussian, width_cal 1.042) per the QGTS precedent. Published on the parity tier; anchor 03-Jul-26 pre-dates the 7–8 Jul ceasefire collapse (timing-flagged). |
| **LCSW** | PASSED | No failure note attached; confirmed calibration pass per memory and site content. |
| *(all other covered names)* | Presumed passed | No failure/tie note found in `coverage.js`; not individually re-verified line-by-line in this snapshot. |

**Note on this snapshot vs. prior memory:** earlier working memory recorded only KABO, QGTS, and
MAADEN as confirmed failures. Pulling the live `coverage.js` text directly for this file surfaced two
more — **AGTHIA and ISPH** — also carrying explicit Step-0-failure notes. Treat this ledger file as
the more current source on failure status; worth reconciling into standing memory.

---

## How to use this file

Before citing a specific ticker's calibration status or ledger grade in a study or conversation,
prefer re-pulling the live `data.js` LEDGER array or `coverage.js` notes over this snapshot if it's
more than a few publish-cycles old — this file will drift out of date the moment a new grade lands
and isn't regenerated. Its value is as a fast, readable reference of the *shape* of the ledger
(schema, current pass/fail roster, snapshot counts), not as the live grading feed itself.
