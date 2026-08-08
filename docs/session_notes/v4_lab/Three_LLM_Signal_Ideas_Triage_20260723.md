# Three independent LLM brainstorms vs. the YZ-HAR replacement prompt — triage, 23-Jul-2026

Sponsor sent the `Prompt_for_YZHAR_Replacement_Ideas.md` prompt to three different LLMs
and asked for a viability check on the results before anything is built. 12 distinct proposals
across 3 documents, triaged here by DATA FEASIBILITY first (hard gate for this repo today),
then by genuine novelty vs. what's already been tried and rejected, then against the sponsor's
four standing criteria (A-D, see `Round8_FVPull_RETIRED_20260723.md`) and the no-fundamental-
dependency rule.

Source docs: `quant_signals_report.pdf` (2 signals), `Provide_me_your_answer...pdf` (4 signals),
`Advanced_Distributional_and_CrossSectional_Signals...pdf` (6 signals, cited).

## Headline finding: convergence

All three, independently, proposed the same two families of idea without prompting each other:

1. **A Shadow-FX / parallel-market GDR premium as a regime signal** — proposed identically
   three times (quant_signals_report #1, the "Provide me" doc #1, and Advanced-Distributional
   candidate II). All three use COMI (EGX) vs. its London GDR CBKD as the mechanism.
2. **A time-varying tail-shape (DoF) parameter**, replacing the current static per-market nu —
   proposed via three DIFFERENT mechanisms (Amihud illiquidity, cross-sectional herding/CSAD,
   and HMM regime-switching) that all land on the same underlying claim: tail fatness isn't
   constant over time.

Independent convergence across three separately-prompted LLMs is worth taking seriously as a
prior — it doesn't substitute for the walk-forward test, but it's a legitimate signal that these
two directions are the more obviously-motivated ones in the set, not cherry-picked LLM noise.

## Confirmed against the actual repo before ranking anything

- `raw_ohlc/{MARKET}/{TICKER}.csv` columns: Date, Price, Open, High, Low, Vol., Change % —
  **volume already exists** for every covered name. Amihud illiquidity, CSAD, lag-1 return
  autocovariance (Roll's proxy), and event-time/active-day HAR lags are all computable from
  data already in the pipeline, zero new sourcing.
- No GDR/CBKD, no point-in-time foreign-ownership/FOL data, no ex-dividend-date database
  anywhere in the repo. Confirmed by grep, not assumed.

## Tier 1 — computable today, worth scoping a real walk-forward test

- **Amihud illiquidity -> dynamic DoF** (quant_signals_report #2). Same-day signal, no
  detection lag, point-in-time eCDF construction is already correct in the supplied code
  (strict history[:-1] isolation, NaN-safe, clipped to [nu_min, nu_max]). Cleanest of the three
  DoF mechanisms — recommend testing this one FIRST among the tail-dynamism family.
- **Bid-ask autocovariance subtraction from daily variance** ("Provide me" #2, Roll's model).
  Addresses a real, specific mathematical concern: sqrt(T) scaling assumes iid daily returns,
  and bid-ask bounce breaks that assumption in thin names. The supplied code already defends
  against its own identified failure mode (negative-variance trap) with a 10%-of-raw-YZ floor —
  a legitimate anti-fragility patch, not hand-waved.
- **Cross-sectional herding (CSAD) -> DoF toggle** ("Provide me" #3). Same mechanism class as
  Amihud, worth testing alongside it. Real risk specific to THIS panel: EG has genuine sector
  clustering (COMI/ADIB financials; EMFD/ORHD/PHDC/TMGH real estate) — a sector-wide move
  could false-trigger "herding" exactly as the source doc's own failure-mode section warns.
  Check the false-trigger rate against known earnings-season dates before trusting it.
- **Event-time (liquidity-clock) HAR** ("Provide me" #4). Legitimate and data-available, but
  worth a five-minute empirical check before investing effort: testahil's actual covered EG
  names (PHDC/TMGH trade multi-million-share days) look considerably more liquid than the
  "multiple zero-volume days a week" premise the idea is motivated by. Confirm the real
  zero-volume-day frequency in-panel before prioritizing this one over the others.

## Tier 2 — real idea, but needs new data infrastructure before it's even testable

- **Shadow-FX/GDR premium** (all three docs). The most-converged idea in the set and grounded
  in genuine, well-documented EM structure (parallel FX premia under capital controls are real,
  not data-mined) — worth the sourcing investment. But two of the three proposals frame it as a
  DRIFT override (bet the peg breaks and equities reprice up), and one frames it as a VOL
  conditioner (widen the cone when stress rises). The vol-conditioning framing is much safer
  and more defensible than the drift-override framing — take a directional view on a currency
  peg is a materially bigger claim than "uncertainty is elevated," and the drift version's own
  self-identified failure mode (pegs routinely outlive a 60-day window; block-bootstrap will
  reject on a single-block outperformance) is a real, likely outcome, not a tail risk. If this
  gets built, build the vol-conditioning version only, not the drift override.
- **HMM regime-switching DoF** (Advanced-Distributional IV). Same underlying claim as the
  Tier-1 DoF ideas, more sophisticated mechanism, but its own source doc honestly flags the
  fatal-looking problem: HMMs lag real-time regime detection ("Forecasting Irreversibility
  Paradox") — tails fatten AFTER the crisis is already reflected in price, i.e. exactly when the
  market is mean-reverting. Likely the weakest of the three DoF mechanisms in practice despite
  being the most theoretically elaborate. Deprioritize relative to Amihud/CSAD.

## Tier 3 — currently infeasible or geographically mis-scoped for this panel

- **Matched-filter order-flow imbalance drift** (Advanced-Distributional I). Requires Level-1
  quote data or signed trade data (Lee-Ready algorithm). Testahil has daily OHLCV only — no
  tick infrastructure exists or is planned. Not testable without a data source this project
  doesn't have and the source doc doesn't claim is available for EM panels this thin.
- **Foreign Ownership Limit (FOL) scarcity premium** (Advanced-Distributional III). Needs a
  point-in-time foreign-room feed that doesn't exist anywhere in the repo. Also worth flagging:
  EGX does not run the same strict foreign-ownership-ceiling regime GCC markets do — this idea
  fits AE/QA/SA structurally better than EG, which is a scoping question as much as a data one.
  Park unless/until a GCC-specific foreign-room data source is identified.
- **EVT/GPD tails with threshold-weighted CRPS** (Advanced-Distributional V). The source doc's
  own failure-mode section already concedes the likely-fatal problem: ~60 tail events at a 95th
  percentile threshold on 5 years of daily data is sample starvation for a 2-parameter GPD fit;
  one outlier can blow up the shape parameter. Agree with the source's own self-assessment —
  lowest-priority candidate in the set, not viable at testahil's current data scale.
- **Dividend seasonality / ex-date run-up** (Advanced-Distributional VI). Needs a point-in-time
  ex-dividend-date database that doesn't exist (testahil currently sources only a flat annual
  q_annual per stock via manual research, not a date-stamped payout calendar). Also sits in the
  "calendar effect" anomaly class, historically one of the more fragile/data-mined categories,
  and is closer to dividend-policy/fundamentals territory than the other candidates — worth a
  second look at whether it clears the no-fundamental-dependency spirit even if not the letter.

## Against the sponsor's four criteria and the fundamental-dependency screen

None of the 12 touch DCF/fair-value/analyst-target fundamentals — all clear the hard screen set
after Round 8's retirement. None revive the already-rejected per-stock static width_cal shrinkage
— the DoF-dynamism family varies by TIME (still pooled across the market at each point), not by
STOCK, which is a genuinely different axis than what failed under LONO on 71 names. C and D (the
dumb-yardstick and cov90 tolerance) aren't given for free by any of these — every one still needs
the actual walk-forward/block-bootstrap test before it means anything.

## Recommendation

Scope Amihud->DoF first (cleanest mechanism, zero data gap, already-correct point-in-time code).
CSAD and bid-ask denoising next, in parallel. Event-time HAR pending a quick liquidity check on
the actual panel. Shadow-FX (vol-conditioning framing only) is worth the data-sourcing effort
given three-way convergence, but is a bigger lift and a separate track. Everything in Tier 3
stays parked, not rejected — infeasible today, not wrong in principle.
