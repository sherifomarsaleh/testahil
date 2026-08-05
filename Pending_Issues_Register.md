# Pending Issues Register

**Purpose.** The durable list of known-open issues: things surfaced, measured, and deliberately
NOT fixed in the pass that found them. `engine/PENDING_REVIEW/` is the materiality gate's
transient outbox (its files are deleted once reviewed); this file is the opposite — it survives
until an issue is closed, and closing one means editing its entry to CLOSED with a pointer to
the commit/PR that closed it, never deleting the entry.

**Discipline.** One entry per issue. Every entry carries: what it is, the evidence (numbers, not
adjectives), why it was not fixed on discovery, the action that closes it, and the trigger that
says when. An issue with no stated trigger is a wish, not an entry.

Opened 2026-08-05, from the QNB roll-forward session (PR #63) and the calibration research
that followed it.

---

## OPEN

### 1. ORAS — published cone is stale (mid-cycle refresh due)

- **What:** `scripts/check_data_freshness.py` WARN: ORAS's cone is anchored 2026-07-22 while
  its technical read is on 2026-07-29 — the library moved a week past the published cone.
- **Why not fixed on discovery:** surfaced during the QNB pass; the protocol treats a stale-cone
  gap as a roll-forward decision to report, never a silent side-fix inside someone else's pass.
- **Action:** `python3 engine/refresh_cone_one.py EG ORAS ORAS --today DD-Mon-YYYY --write`
  (mid-cycle, STEP 0 decision (a) — no ledger row), then technicals + chart + overlay gate in
  the same pass.
- **Trigger:** next ORAS data arrival, or the next maintenance pass — whichever comes first.

### 2. SAMSUNG — published cone is stale (one session)

- **What:** same WARN: cone anchored 2026-07-27, technical read 2026-07-28.
- **Evidence:** one session of drift — the smallest gap the stamp diagnostic can show.
- **Action:** same as ORAS (`KR SAMSUNG SAMSUNG`).
- **Trigger:** next KR data arrival; not worth a pass on its own at one session.

### 3. `engine/metal_backtest.py:367` — calibration panels mislabel currency as USD

- **What:** the y-axis label is hardcoded `'Price (USD, log)'`, so every non-USD panel (most of
  the 74) mislabels its currency — e.g. `assets/calibration_QNB.png` reads USD over QAR values.
- **Why not fixed on discovery:** the code fix is one line, but fixing it honestly means
  regenerating all 74 panels in the same pass (hours of compute) — fixing the generator without
  the panels leaves 73 pages disagreeing with their own generator.
- **Action:** parameterize the label from the instrument's `ccy`, then a full-fleet
  `metal_backtest.py` regeneration in one commit.
- **Trigger:** the next occasion a fleet-wide panel regeneration is warranted anyway (library
  extension, fit change). Do not run the fleet for the label alone.

### 4. Saudi cone is genuinely too narrow — parked pending more graded history

- **What:** the one statistically real width misfit in the system. Standardized residual
  sd 1.135, 90% cluster-bootstrap CI [1.028, 1.233] (clusters = origin quarters, 58 of them) —
  the only market whose CI excludes 1 on the too-narrow side. EG (0.892, too wide) is the
  documented devaluation-insurance choice; XPT (0.800) is a single 58-window name.
- **Promotion test result (2026-08-05):** LONO-estimated widening (multiplier from the other
  10 SA names, scored on the held-out name) improves scale-normalized CRPS by +0.11% with 7/11
  names improved (64%). Real but below the bar — z≈0.9 against chance. NOT promoted.
- **Action:** re-run the same LONO test, unchanged, when Saudi has materially more graded
  history. If sd's CI still excludes 1 and breadth firms, promote through the standing gate.
- **Trigger:** ≥2 full metronome cycles of additional SA grades (the lifecycle yields 24 graded
  windows/name/year), or new SA names widening the panel past 11.

### 5. Conditional-width (FX-premium) project — passed its feasibility gate, needs a design note

- **What:** Egypt runs one unconditional width across two regimes: deval-window coverage is on
  target (49.5 / 79.4 / 87.9 vs 50 / 80 / 90 on 107 windows) while calm windows over-cover
  (58.0 / 86.4 / 92.7 on 1,295). A width conditioned on FX stress could run tighter in calm
  quarters without selling the devaluation insurance.
- **Feasibility result (2026-08-05, die-cheaply gate — PASSED):** parameter-free ranking test,
  32 quarters 2018Q1–2025Q4, 4 official devaluations, prior-month data only. The parallel-market
  /NDF premium ranked all four deval quarters top-quartile (#7, #5, #2, #1; AUC 0.915, robust to
  ±50% input jitter, median AUC 0.920). Trailing 60d equity vol — what the HAR core sees — scored
  0.768 and was blind exactly at the cycle entry (2022Q1 ranked #17). REER gap (0.536) and
  freeze-pressure (0.433) are DEAD — do not revive them as indicator candidates.
- **Honest limits:** four events; the premium series used was a journalistic reconstruction
  anchored to the committed annual CALC block. A production version needs the real sourced
  series under the four-field INPUTS rule.
- **Action, in order:** (a) design note in `engine/` committing the indicator definition,
  data source, and acceptance criteria BEFORE any engine code; (b) source the monthly premium
  series properly; (c) promotion test = deval-window 90% coverage held-or-improved AND LONO
  CRPS not worse — never headline skill alone, which is the exact circular scoring the
  2024-cut trap in the EGYPT profile comment documents.
- **Trigger:** explicitly scheduled research work — this is the one open item that is a project,
  not a maintenance task. Nothing touches the engine until (a)–(c) clear.

---

## CLOSED THIS SESSION (recorded so they are not re-opened by accident)

Measured and closed 2026-08-05; the full numbers are in the session record and PR #63's thread.

- **"The system is overly cautious" — refuted.** Pooled standardized-residual sd 0.994
  (cluster-bootstrap CI [0.916, 1.083]); PIT-implied coverage 53.5 / 81.8 / 90.1 vs
  50 / 80 / 90 targets on 3,374 windows. Six of nine markets individually calibrated.
- **Break-aware per-origin variance — closed.** The protocol's open gap is real but worth
  −0.76% on Egypt's cone width (arithmetically dominated by the s2 channel, verified). Not the
  cause of Egypt's width; per-name scatter ±10% around a ~zero mean.
- **Risk-premium / market-wise drift — closed structurally.** The realized premium over the
  carry anchor is +6.3%/yr ex-US, but over a 3-month horizon that is 0.08 of the cone's sigma:
  no drift specification can move CRPS at these horizons. LONO confirmed: best variant +0.31%
  with 51% name breadth (a coin flip). Matches the prior sessions' finding; now closed on
  arithmetic, not just on a failed fit.
- **Distribution shape (skew / tail family) — closed.** Pooled skew +0.09 with inconsistent
  signs across markets; excess-kurtosis misfits point in opposite directions (AE fatter than
  its nu, EG thinner). No systematic shape change is supported.
