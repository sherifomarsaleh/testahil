# TESTAHIL SELECTION ENGINE — PRE-REGISTRATION v1

> **[HEADER NOTE — 8-Aug-2026 · NOT AN AMENDMENT; NOTHING BELOW IS EDITED]** The horizon named in §3 — "60 trading sessions forward, counted as *actual trading rows in the library*, never a calendar projection" — was subsequently RENAMED, not redefined, by the project-wide calendar-only horizon adoption (1 month / 3 months). The pre-registered quantity, the cohort construction, the factor definitions and every critical value in §6 and §7 are unchanged, so no §10 amendment is triggered and this pre-registration stands exactly as signed. Recorded here only so a later reader does not mistake the naming change for specification drift.

**Status: DRAFT for sign-off. 26 July 2026.**

This document fixes the test *before* any factor is computed. Nothing in it may be
changed after the first result is seen except through the amendment rule in §10, which
requires the change and its reason to be recorded and the affected result re-run and
re-reported under both the old and new specification.

It exists because the failure mode here is not carelessness — it is the ordinary,
almost invisible drift of a specification toward whatever happened to work. This
project has produced two such results in the last week, both caught, neither the
result of sloppiness:

- The 26-name long-history calibration "win" that was robust across bootstrap blocks
  {2,3,4} and **did not survive adding four names**. Block-bootstrap robustness does
  not imply panel-composition robustness. They are separate checks.
- Round 7's ERP snapshot, where **~80% of the measured gain evaporated** once the
  inputs were properly dated.

A selection engine is more exposed to this than the MC ever was: many candidate
factors, many defensible parameterisations, one panel, and — per §7 — a critical
threshold that sits directly on top of the effect sizes the literature reports.

---

## 1. What this engine is, and what it is not

**Is:** a cross-sectional ranking model. Given a set of names at a point in time, it
orders them by expected relative forward return.

**Is not:** any part of the Monte Carlo forecast engine.

The separation runs in **both** directions and is architectural, not stylistic:

1. **Selection output never enters MC drift.** This is the standing constraint of
   23-Jul-2026 (`Round8_FVPull_RETIRED`): the MC's honesty must not be hostage to a
   separate, independently-fallible research process. That constraint stands unamended.
2. **MC output never enters the selection score.** The MC is calibrated against a
   carry-anchored random walk and is deliberately viewless in the cross-section. Using
   its median, drift, or "g" as a ranking input would be ranking on a constant plus
   noise. (Measured 26-Jul-2026 on the live 74-name library: T+60 median return spans
   4.367%–4.411% across all 30 EGX names — a 0.044pp spread, which is Monte Carlo
   sampling noise, not signal.)

The two engines share a *harness* — LONO discipline, block bootstrap, panel-composition
robustness, append-only ledgers — and nothing else.

---

## 2. The object being tested

**Null hypothesis (H₀):** the factor carries no cross-sectional information about
forward relative return on this panel.

**Benchmark: the equal-weight panel, not a random walk.** This is the single most
important line in the document. The MC's benchmark is a carry-anchored lognormal RW,
because the MC forecasts a *distribution*. Selection forecasts a *ranking*, and beating
a random walk is not selection skill — a model that correctly predicts every name will
rise beats the RW and selects nothing. The benchmark is the cross-sectional mean of the
cohort, which rank-based metrics impose automatically.

**Primary metric:** mean cross-sectional **Spearman rank IC** between the factor score
at cohort anchor and the realised forward 60-session return, averaged across cohorts.

**Secondary metric:** mean **tercile spread** — equal-weight mean forward return of the
top third minus the bottom third, in cross-sectional standard-deviation units. Reported
always; it is what a portfolio would actually harvest, and it is the sanity check on the
IC. Deciles are *not* used: on a 30-name panel a decile is 3 names.

**Unit of evidence: one cohort.** Thirty names sharing one 60-day macro period is
approximately one observation, not thirty. Every confidence interval, bootstrap and
critical value in this document is computed with the cohort as the unit. Treating
name-windows as independent would overstate the sample by more than an order of
magnitude and is the most common way this kind of study fabricates significance.

---

## 3. Cohort construction

- **Anchors:** non-overlapping, every 60 trading sessions, walking backward from the
  most recent complete session in the library.
- **Horizon:** 60 trading sessions forward, counted as *actual trading rows in the
  library*, never a calendar projection. (Standing grading rule — stored projected dates
  carry no holiday awareness.)
- **Inclusion:** a name enters a cohort only if it has the full trailing history its
  factor requires **and** a resolved forward outcome. No forward-fill, no partial windows.
- **No break filter.** The MC filters pre-2022-03-21 origins because it is estimating a
  volatility regime. Selection is asking a different question and deliberately wants
  multiple regimes in-sample. This is a considered divergence from the MC, recorded here
  so it is not later mistaken for an oversight.
- **Point-in-time discipline:** every factor uses only data timestamped at or before the
  anchor. Any factor requiring a value that did not exist at the anchor is inadmissible
  — see §5.

**Expected sample (to be confirmed when the 15-year library lands):** ~62 cohorts on EG.
The 5.5-year library on `main` supports ~22. All critical values below are stated for
both so the difference is explicit.

---

## 4. Universe

| Panel | Names | Basis |
|---|---|---|
| EG | ~30 | 15-year library, median 15.6 yrs history |
| AE | ~18 | 5.5-yr library (EAND 10.5 yrs) |
| SA | ~11 | 5.5-yr library |

**Primary test: pooled EG+AE+SA**, ranks computed *within market, within cohort*, then
pooled. Pooling is where the statistical power is (§7).

**Robustness: per-market.** A factor that clears the bar pooled but only works in one
market is **not adopted**. This resolves the tension with the standing per-market fit
rule ("every market is different"): pooling is permitted for *power*, but a factor must
show the same sign in at least 2 of 3 markets to be believed.

Markets with 3-name panels (QA/IN/KR/US) and the metals are **excluded**. A 3-name
cross-section cannot support a ranking test.

---

## 5. Factor list — FROZEN at six

Six, not more, and the reason is arithmetic: under Bonferroni every additional factor
raises the bar for all of them (§6). Adding a seventh factor must remove one.

All six are computable from `Date, Price, Open, High, Low, Vol.` — the columns already
in the library. Verified present, not assumed.

| # | Factor | Definition at anchor *t* | Expected sign |
|---|---|---|---|
| F1 | Momentum 12–1 | `ln(P[t−21] / P[t−252])` | + |
| F2 | Short-term reversal | `ln(P[t] / P[t−21])` | − |
| F3 | **Long-term reversal** | `ln(P[t−252] / P[t−1260])` | − |
| F4 | Low volatility | `−1 ×` trailing 252d Yang-Zhang vol | + |
| F5 | Amihud illiquidity | mean over 252d of `|ret| / (Price × Vol.)` | + |
| F6 | 52-week-high proximity | `P[t] / max(P[t−252 … t])` | + |

**F3 is the factor that only the 15-year library makes possible.** It needs five years
of history per name per anchor and was not testable at all on the short library.

**Expected signs are pre-registered and binding.** A factor that clears the threshold
with the *opposite* sign is recorded as a failure of the stated hypothesis, not
reinterpreted as a discovery. Egypt's `rev_1m` prior has already been refuted once this
way (empirical IC +0.018 against a pre-registered contrarian sign) and India's
`mom_12_1` prior carries an empirical IC of −0.093 against a pre-registered `+`. Both
were correctly recorded as refutations.

**Not in scope, and why:** value, quality, size, and growth are **not computable** — the
library carries no market cap and no fundamentals. Sourcing them is a separate project
requiring point-in-time financials, and back-filling them from today's statements is the
same look-ahead sin that killed the retroactive FV test. Any proposal to add them is an
amendment (§10), not an extension of this test.

---

## 6. Decision rule

Critical values below are **simulated**, not assumed — 30,000 draws under H₀ with the
cohort as the unit, at the stated panel dimensions. They are not analytic
approximations.

### Critical mean rank IC (one-sided, factor must clear this)

| Panel | Single factor (α=0.05) | **Six factors, Bonferroni (α=0.0083)** |
|---|---|---|
| EG only, 22 cohorts (5.5yr) | 0.065 | — *underpowered, not run* |
| EG only, 62 cohorts (15yr) | 0.039 | **0.057** |
| **EG+AE+SA, 62 cohorts (primary)** | 0.027 | **0.040** |

Corresponding tercile-spread thresholds: EG-only 0.093 / 0.137 sd-units; pooled
0.066 / 0.098 sd-units.

### A factor is ADOPTED only if all five hold

1. Pooled mean rank IC clears the **Bonferroni** threshold (0.040) with the
   pre-registered sign.
2. Tercile spread clears its threshold with the same sign — IC and spread must agree.
3. Same sign in **≥2 of 3 markets** individually.
4. Survives **drop-one-name jackknife**: no single name's removal flips the verdict.
   This check is *separate from and additional to* the block bootstrap — the 26-name
   calibration result proved these are not the same test.
5. No single cohort contributes **>25%** of the pooled mean (the scale-normalisation
   lesson, carried over from the MC gate).

Block bootstrap over cohorts at block sizes **{2,3,4}** is reported for every factor.
A verdict that flips with block size is **BOUNDARY**, recorded as such, never a silent
proceed.

---

## 7. What a null result means — read this before interpreting one

Power at the Bonferroni bar, simulated at the same dimensions:

| True IC | EG only (62 cohorts) | **EG+AE+SA (62 cohorts)** |
|---|---|---|
| 0.03 | 11% | **24%** |
| 0.05 | 33% | **67%** |
| 0.08 | 77% | **98%** |
| 0.10 | 94% | **100%** |

Published equity factor ICs typically run **0.02–0.05**.

Two consequences, both binding:

**A null result at IC ≈ 0.03 is not evidence of absence.** Even on the pooled panel we
would miss such a factor three times in four. Any factor that fails must be recorded as
`NOT DETECTED at this power`, never as `no signal`. This is a specific correction to how
Round 4's results should now be read: momentum, β×ERP and vol-rank drift were killed on
22 cohorts where power against a true IC of 0.05 was **31%**. Those were not refutations.
They were underpowered tests, and this document supersedes their interpretation.

**Conversely, an IC that clears 0.040 is larger than most published factor premia.**
If one clears comfortably, the first hypothesis is a bug or a look-ahead leak, not a
discovery. §8 lists the leaks to check first.

---

## 8. Data prerequisites and known problems

**Blocking:**
- The 15-year library (`lib15_clean/`, 32 series, 97,756 cleaned sessions) has **not
  been pushed** and is not reachable from `main`. It is the input to everything here.
- Every series must pass the Step 0.0 gate (`data_quality.clean_ohlc`) with the
  per-market threshold before entering a cohort. No exceptions.

**Known data problems that affect specific factors:**
- **RAYA carries flat `High==Low` on 34.6% of sessions.** A third of its history has no
  intraday range, which depresses its Yang-Zhang variance proxy. This directly
  contaminates **F4** and must be resolved — exclude the name, or fall back to
  close-to-close vol for it — *before* F4 is run, with the choice recorded here.
  (Next worst: LCSW 9.4%, EFID 9.0%, ABUK 8.7%, BTFH 8.1%.)
- **EGX70 has 6.5 usable years, not 15** — 100% of pre-2019 rows are rangeless. Not part
  of this universe, noted so the claim is not repeated.
- **PRDC and EFIH are genuinely short** (4.8 yrs each, recent listings). They will drop
  out of F3 cohorts entirely. Expected, not a defect.
- **Volume units are unverified.** F5 divides by `Price × Vol.`; if `Vol.` changes units
  or scale anywhere in a series the factor breaks silently. Screen before running.

**Survivorship bias — unfixable, and stated plainly.** The library contains only
currently-covered names. Names that delisted, collapsed or were acquired are absent.
This biases every factor here in an unknown direction and cannot be corrected with the
data on hand. It must appear in any published result. It is a reason to treat a positive
finding with more suspicion than a negative one.

---

## 9. What happens after

- **Any factor adopted** goes into a standalone Selection Ledger — append-only, same
  discipline as the Calibration and Driver ledgers. No published ranking is ever
  retro-edited.
- **Nothing** touches `market_profiles.py`, the MC engine, ticker pages, or the live
  site. Different repo, different project, no shared write path.
- **Live tracking from day one:** every ranking published is scored forward, cohort by
  cohort, exactly as the MC's forecasts are. The backtest is the entry ticket, not the
  evidence.

**Separately, and starting now: restart the FV shadow-cohort clock.** Shadow Cohort #1
(30 EGX names, anchors 23-Jun–19-Jul-2026, paired production/FV-pull T+60 distributions,
shared seed) is already on file. Its monthly grading trigger was cancelled when Round 8
was retired. That cancellation should be reversed — grading costs minutes a month, first
maturity is mid-October 2026, and it is the only path to measuring whether the
fundamental work predicts returns. Retiring FV-pull as an **MC drift** candidate does not
argue against measuring it as a **selection** signal; the retirement's own reasoning
(keep the engines independent) is the argument *for* scoring it separately.

---

## 10. Amendment rule

Any change after the first result is seen requires: the change, the date, the reason,
and a re-run reporting the affected result under **both** the old and the new
specification. Amendments are appended, never overwritten. An amendment that can only be
justified by the result it produces is not an amendment — it is the failure mode this
document exists to prevent.

---

## 11. Sign-off

Signed before any factor is computed:

| | |
|---|---|
| Universe and cohort construction (§3, §4) | ☐ |
| Factor list frozen at six, signs pre-registered (§5) | ☐ |
| Decision rule and thresholds (§6) | ☐ |
| Interpretation of a null accepted (§7) | ☐ |
| RAYA treatment for F4 decided and recorded (§8) | ☐ |
| Pooled-primary / per-market-robustness resolution accepted (§4) | ☐ |

Sponsor: ______________________  Date: ______________

---

### Appendix — critical values, reproduction

Simulated 26-Jul-2026. Draws under H₀: factor score and forward return independent
standard normals, ranked within cohort, Spearman IC per cohort, mean across cohorts;
30,000 replications for thresholds, 8,000–9,000 for power. Cohort is the unit throughout.
Reproduce before relying on the numbers — they are the whole decision rule.
