# TESTAHIL — Fundamental / Monte-Carlo Integration Protocol (1-month & 3-month)

**Status: PROPOSED — not adopted.** Awaiting Sherif's decision. Nothing in this document changes
a published cone, a `LEDGER` row, or an engine config until it is adopted. Written 6-Aug-2026.

**All three phases are implemented.** Each reads published data only; none writes back to
`assets/data.js`, and `mc_v3.py` / `market_profiles.py` are untouched.

```
python3 engine/fv_overlay.py         --market EG --json out.json --md out.md   # Phase A
python3 engine/direction_score.py                                              # Phase B self-check
python3 engine/value_gap_backtest.py --market EG --json out.json --md out.md   # Phase C
```

Three clauses of this document were amended by implementation, each marked in place: the σ source
(§2), the already-converged rule (§4), and the Phase C engine hook (§8) — which stays deliberately
unwired, because Phase C returns INSUFFICIENT-POWER and promotion must follow measurement.

**Purpose.** Define the one honest way to read a ground-up fair value and a calibrated Monte-Carlo
cone *together* at the two horizons Testahil publishes — 1 month and 3 months — without
contaminating either.

**What this is not.** It is not a way to make the MC engine forecast direction. The engine is
carry-only by deliberate, tested decision (`market_profiles.py:102`, `signal_active=False`), and
this protocol does not change that. It adds a **diagnostic overlay** computed *after* the cone is
struck, which answers a question the cone alone cannot: *given this market's own volatility, is the
fundamental thesis even expressible at a 1–3 month horizon?*

Precedent: `ISPH_Fundamentals_Gate_Check_and_MC_Integration_20260722.md` established the method at
multi-year horizons and the standing rule that a point-in-time DCF **is not injected into engine
drift**. This document carries that rule down to 1M/3M and makes the procedure repeatable.

---

## 1. Design invariants

These are binding. A run that breaks any of them is a HARD FAIL and must not be published.

1. **The cone is never modified.** `p5/p25/p50/p75/p95` are the calibrated, gradeable object.
   The overlay is a separate set of fields. No fundamental input touches `drift`, `sigma_h`,
   `nu`, or `width_cal`.
2. **No drift injection without a measured IC.** A single DCF is a thesis, not a LONO-testable
   signal. The socket for injection already exists (`mc_v3.py:114`,
   `alpha = ic × sigma_h × sign × clip(z)`) and stays empty until Phase C (§8) measures the `ic`
   that belongs in it.
3. **Point-in-time only.** The overlay at `anchor_date` may use only a fair value **published on or
   before `anchor_date`**. Never the current fair value applied to a past anchor. This is what
   keeps Phase C free of look-ahead bias, and it must hold from the first run, not be retrofitted.
4. **Append-only.** Overlay fields are added to a `LEDGER` row at strike and graded at that row's
   own `grade_date`. Never back-filled onto rows struck before adoption.
5. **The overlay is graded, or it is not published.** An unfalsifiable overlay is decoration.
   See §7.
6. **The cash hurdle is always shown.** EGP risk-free is `rf_live = 19.50%`
   (`market_profiles.py:95`). Any read that does not compare against it is incomplete.

---

## 2. Inputs

| Input | Source | Notes |
|---|---|---|
| `S0` anchor price | `TICKERS[t].spot` | must equal the last row of the cleaned OHLC |
| `anchor_date` | `TICKERS[t].spotDate` | the cone's anchor, not today |
| `sigma_h` (1M, 3M) | **inversion from the published p5/p95** | primary — see the amendment below |
| `nu`, `width_cal` | `market_profiles` for the market | EG: `nu=6.0`, `width_cal=0.951` |
| `h1`, `h3` sessions | `horizons.resolve()` | calendar-anchored, blend projection |
| `FV_bear/base/full` | the published study | point-in-time, per invariant 3 |
| `rf` | `profile.rf_live` | the hurdle |

> **AMENDED 6-Aug-2026 during Phase A implementation — σ source reversed.**
> This section originally named the engine panel as primary and quantile inversion as fallback.
> That is backwards for a *live* overlay, on three counts found while building `fv_overlay.py`:
> (1) `engine/panels/EG_*.csv` hold **backtest origins** — the last EG origin is 2026-04-12, while
> the live ELEC anchor is 2026-08-05, so the panel does not contain the live strike at all;
> (2) EG runs `width_overlay_active=True`, so the published quantiles carry the per-name adaptive
> width overlay, and inverting them recovers the **effective** σ that actually shaped the published
> cone; (3) an overlay annotates a specific ledger row, so it must be consistent with *that row*
> rather than with a fresh re-fit of the same name, which could legitimately disagree.
> Inversion is therefore primary. `sigma_src` records the path taken on every row, and a self-test
> reproduces the published quantiles from the reconstruction (worst deviation on the live EG panel:
> **0.32% at 1M, 0.48% at 3M**, tolerance 2%).

**σ back-out (primary).** Under the engine's unit-variance Student-t
(`simulate_terminal_v3`, `mix = sqrt((nu-2)/chi2_nu)`):

```
q(p)   = sqrt((nu-2)/nu) * t_inv(p, nu)          # standardized-t quantile
sigma_h = (ln p95 - ln p5) / (2 * q(0.95))
mu_h    = ln p50                                  # = carry, alpha is 0
```

Record which path was used in `sigma_src`, and always emit the self-test deviation alongside it —
a reconstruction that cannot reproduce the published cone invalidates every measure built on it.

---

## 3. The five overlay measures

### 3.1 Reachability, `G` — the headline

How far fair value sits from spot, measured in that name's own horizon volatility. Drift-free by
construction, so it is a pure statement about distance vs dispersion:

```
G = ln(FV / S0) / sigma_h
```

`G` is the single most useful number in this protocol. It is comparable across names, across
horizons and across markets in a way that a percentage gap is not.

### 3.2 Convergence probability, terminal

Probability the horizon **close** is at or beyond fair value:

```
z    = (ln(FV/S0) - mu_h) / sigma_h
P_term = 1 - F_t*(z)          # F_t* = standardized-t CDF, same nu as the cone
```

### 3.3 Touch probability, path

Probability the price trades through fair value **at any point** before the horizon. Always ≥
`P_term`. The reflection principle does not hold for a drifted t-mixture, so this must be
**simulated**, not approximated — reuse `simulate_paths_v3` with the production seed (42) and path
count (50,000). This is the same machinery that already produces the `touch` ladder on every ticker
page; the only change is that the levels are `FV_bear/base/full` instead of round numbers.

### 3.4 Required CAGR vs the cash hurdle

What annualized return the stock must deliver to reach fair value *by this horizon*, against what
cash pays for the same period:

```
required_cagr = (FV / S0) ** (1 / yearfrac) - 1        # yearfrac = 1/12 or 0.25
verdict       = required_cagr vs rf_live (19.50%)
```

At 1M and 3M this number is almost always absurd, and that is the point — it makes the timescale
mismatch explicit rather than leaving it implied.

### 3.5 Tail asymmetry

Which tail of the cone the fundamental sits behind:

```
asym = (ln(FV/S0) - mu_h) / sigma_h  evaluated against the p5 and p95 z-levels
```

Report as: fair value inside the 90% band / beyond the upper tail / beyond the lower tail. A name
whose fair value sits *below* p5 is one the market is pricing above every modelled outcome — a
different and more urgent statement than "overvalued."

---

## 4. Reachability taxonomy

Bands calibrated on the live 31-name EGX panel (6-Aug-2026), not invented:

| Band | `|G|` | Reading | 1M count | 3M count |
|---|---|---|---|---|
| **IN-REACH** | ≤ 1.0σ | Convergence is an ordinary move. The overlay is decision-relevant. | 11 / 31 | 16 / 31 |
| **STRETCH** | 1.0 – 2.0σ | Possible, needs a catalyst. Report, do not lead with it. | 6 / 31 | 5 / 31 |
| **OUT-OF-REACH** | 2.0 – 4.0σ | Not a 1–3 month proposition. Report as a timescale statement. | 5 / 31 | 7 / 31 |
| **NOT-EXPRESSIBLE** | > 4.0σ | The horizon cannot carry the thesis. Suppress the probability. | 9 / 31 | 3 / 31 |

Panel medians: `|G|` = **1.94σ at 1M**, **1.00σ at 3M**.

**The suppression rule.** In NOT-EXPRESSIBLE, `P_term` rounds to zero and publishing it invites
the reader to treat a modelling artefact as a forecast. Publish the band label and `G`; suppress the
probability. ELEC at 1M is `G = −19.4σ` — a number with no meaningful probability attached.

**The already-converged rule (added 6-Aug-2026, first full EG run).** The mirror failure sits at the
opposite end of the range. EFID has a gap of −0.4% and reported `P(touch) = 85% / 90%` — which reads
as a strong result and is in fact the *absence* of one: the fair value is inside the horizon's own
noise, so the level is already where the price is. Where `|G| ≤ 0.25σ`, set `already_converged` and
flag the probability. It is not suppressed — "spot is at fair value" is a genuine, useful state —
but it is not evidence for a thesis, and an unflagged 90% will be read as though it were.

A row is **informative** only when it is neither suppressed nor already converged. On the live EG
panel that is **20/31 at 1M and 24/31 at 3M** — the honest denominator for anything built on top.

**The structural finding this taxonomy encodes:** the largest fundamental gaps sit on the *least*
reachable names. EMFD (+72%) is `G = +5.9σ` at 1M; HELI (+2%) is `G = +0.15σ`. Ranking by upside
and ranking by reachability are close to inverses. Any procedure that does not surface this will
recommend exactly the wrong names for a 1–3 month horizon.

---

## 5. Procedure

**Step 0 — Preconditions.** Cone struck under the current roll-forward cycle
(`Rollforward_and_Grading_Protocol.md` Step 0). Fair value published on or before `anchor_date`.
Both confirmed before anything is computed. If the fair value post-dates the anchor, **STOP** —
that is a look-ahead violation, not a rounding issue.

**Step 1 — Load.** Pull `S0`, `sigma_h` (both horizons), `nu`, `h1`/`h3` from the panel and
`horizons.resolve()`. Record whether `sigma_h` came from the panel or from quantile inversion.

**Step 2 — Compute `G`** at both horizons for all three fair-value levels (bear / base / full).
Assign the band from §4 on the **base** level.

**Step 3 — Gate on the band.** NOT-EXPRESSIBLE → skip Steps 4–5, emit the band and `G` only.
Everything else → continue.

**Step 4 — Probabilities.** `P_term` closed-form; `P_touch` by simulation (seed 42, 50k paths,
production config). Both horizons, all three levels.

**Step 5 — Hurdle.** `required_cagr` at each level and horizon, against `rf_live`. State plainly
whether the fundamental case beats cash *at this horizon* — at 1M/3M it usually will not, and the
honest output is that the thesis lives at a longer horizon.

**Step 6 — Asymmetry.** Locate all three fair-value levels against the p5/p95 band. Flag any name
whose **full** (bull) case sits below spot, or whose **bear** case sits above spot — those are the
two configurations where the fundamental and the market disagree unconditionally.

**Step 7 — Emit and stamp.** Write the overlay block (§6). Stamp `overlay_basis` with the σ source,
the fair-value publication date, and the engine config used. Mark
`overlay_status: "PROVISIONAL — value-gap IC unmeasured"` until Phase C reports.

---

## 6. Output schema

Added to the `LEDGER` row at strike; every field nullable so pre-adoption rows stay valid.

```jsonc
"fv_overlay": {
  "fv_asof":        "2026-07-15",     // publication date of the fair value used
  "fv_bear":  0.18, "fv_base": 0.34, "fv_full": 0.95,
  "sigma_src":      "panel",          // "panel" | "quantile_inversion"
  "G":        { "bear": -2.9, "base": -19.4, "full": -8.1 },
  "band":           "NOT-EXPRESSIBLE",
  "informative":     false,           // neither suppressed nor already converged
  "already_converged": false,         // |G| <= 0.25 sigma
  "selftest_max_dev": 0.0032,         // reconstructed vs published quantiles
  "p_term":   { "bear": null, "base": null, "full": null },   // suppressed in this band
  "p_touch":  { "bear": null, "base": null, "full": null },
  "required_cagr":  { "base": -0.9999 },
  "hurdle_rf":      0.1950,
  "beats_cash":     false,
  "asymmetry":      "base below p5",
  "overlay_status": "PROVISIONAL — value-gap IC unmeasured",
  // graded at grade_date:
  "realized_vs_fv": null,             // ln(realized_close / fv_base)
  "converged":      null              // did it reach fv_base by grade_date
}
```

---

## 7. Grading — how the overlay is falsified

Graded at the row's own `grade_date`, alongside the cone, per the append-only rule.

**Per row:** did the price reach `fv_base` (terminal and touch)? Record `converged` and
`realized_vs_fv`.

**Across rows, the two tests that matter:**

1. **Overlay calibration.** Bucket all graded rows by predicted `P_touch` (0–10%, 10–25%, …). In
   each bucket the realized hit-rate should match the predicted range. This tests the overlay the
   same way PIT tests the cone. It needs ~40+ graded rows before it says anything.
2. **Direction skill — the missing axis.** CRPS is direction-blind: it is dominated by the width
   term, so a genuinely informative signal barely moves it. This is why `rev_1m` was ablated on
   `P(signal helps)=0.31` — the referee could not see the goal. Score `sign(G)` against
   `sign(realized − S0)`: hit-rate, IC (Spearman of `G` vs forward return), and pinball loss at the
   median. Same LONO + block-bootstrap discipline as `fit_markets_20260710.py:21`.

**Test 2 is a prerequisite for Phase C.** Running the value-gap backtest under a CRPS-only gate
would reproduce the `rev_1m` false negative exactly.

---

## 8. Phase roadmap

| Phase | What | Depends on | Status |
|---|---|---|---|
| **A** | The overlay above. Ships on validated machinery; changes no cone. Output labelled PROVISIONAL. | — | **implemented** — `engine/fv_overlay.py` |
| **B** | Direction-scoring axis added to the gate (§7 test 2). | — | **implemented** — `engine/direction_score.py` |
| **C** | Backtest `value_gap` as an alpha signal, measure IC on the EG panel under LONO. | **B** | **implemented, returns INSUFFICIENT-POWER** — `engine/value_gap_backtest.py` |

### Phase C — first read, 6-Aug-2026

Run: `value_gap_backtest_EG_20260806.{json,md}`. **Verdict: INSUFFICIENT-POWER at both horizons.**
Not a negative result about the fair values — a statement that the evidence does not yet exist.

| | 1M | 3M |
|---|---|---|
| observations with a realized outcome | **5** | **0** |
| IC (Spearman) | −0.600 (descriptive only) | n/a |
| sign balance | 5 positive / 0 negative — **one-sided** | n/a |
| dropped for no realized outcome | 29 | 34 |

Three separate things each independently block a verdict, and all three are data-availability
facts rather than modelling choices:

1. **n = 5.** Resolving a realistic value-signal IC of 0.10 at 80% power needs n ≈ 783; even
   IC 0.20 needs n ≈ 194. The observed −0.600 is what a 5-point rank correlation does, not a finding.
2. **The signal is one-sided.** All five names were undervalued at their origin, so the short
   side is untested and the IC degenerates to a magnitude ordering within a single sign.
3. **There is almost no signal history.** 30 of 31 EGX names carry exactly ONE fair value across
   the entire git history of `assets/data.js`; only GBCO has revisions, and those are same-week
   edits. A value-gap panel needs *vintages*, and the archive is effectively one cross-section.

**What would unblock it.** Not time alone — re-studies. Each name needs repeated, dated fair-value
strikes, which is what turns 31 points into a panel. The roll-forward cycle already mints a fresh
cone monthly; Phase C becomes answerable when fair values are re-struck on a comparable cadence and
the ledger's graded population grows. Until then the harness runs on every invocation and reports
its own inadequacy, which is the intended behaviour.

**The engine hook stays unwired.** `signal_active=False` is unchanged, `mc_v3.py` is untouched, and
`profile.ic` keeps its retained prior. The adapter (`value_gap_backtest.grinold_alpha`) mirrors
`signal_alpha` exactly and is ready to lift the day an IC clears the gate — promotion is a
measurement result, never a decision made in advance of one.

**How C closes the loop.** Phase A defines the signal — `G` *is* the standardized value gap that
`signal_z` would return. Phase C measures its IC. That IC is then the `profile.ic` in the existing
`signal_alpha` (`mc_v3.py:114`), and it is *also* the shrinkage weight that upgrades Phase A's
probabilities from "P(reach the full fair value)" to "P(reach the IC-weighted fair value)". A and C
are the same object seen from two sides: A uses the fair values, C tests them.

**Power warning.** 13 graded rows exist today (12/13 inside the 90% band, PIT mean 0.520 — the cone
is well calibrated; direction 8/13, which is noise). Phase C cannot return a trustworthy IC this
year. Build it, let the ledger fill, and read the first result as direction-of-travel, not verdict.

---

## 9. What this establishes, and what it does not

**Does.** Gives a calibrated, comparable answer to "can this thesis play out in 1–3 months," in the
name's own volatility units. Makes the timescale mismatch explicit and measurable rather than
implicit. Defines the signal that Phase C needs, with point-in-time discipline from day one.
Preserves the calibration record intact.

**Does not.** Validate any DCF's assumptions. Turn the MC into a return forecaster. Produce a price
target — the output is a probability and a band label, never a point. Justify a position on its own:
until Phase C reports an IC, `G` is a *distance measure*, not evidence that the fair value predicts
anything.

**The honest summary at these horizons:** for most EGX names the fundamental gap is 2–10σ away at
1M and 1–5σ at 3M. The overlay's main output is therefore usually a *negative* one — "not at this
horizon" — and that is a useful, decision-relevant answer, not a failure of the method.

---

*Companion to `Standing_Research_Protocol.md` (study construction),
`Rollforward_and_Grading_Protocol.md` (the forecast lifecycle) and `Publish_Protocol.md` (surfaces).
Precedent: `ISPH_Fundamentals_Gate_Check_and_MC_Integration_20260722.md`. No engine code, config or
published forecast is modified by this document.*
