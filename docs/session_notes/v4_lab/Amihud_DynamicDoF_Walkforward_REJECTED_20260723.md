# Candidate: Amihud illiquidity → dynamic tail-shape (nu) — REJECTED, 23-Jul-2026

First of the 3-LLM triage candidates taken to a real walk-forward test (per
`Three_LLM_Signal_Ideas_Triage_20260723.md`). Source idea: quant_signals_report.pdf #2
— "tail fatness isn't constant; when systemic illiquidity is high, gaps are likelier, so
Student-t nu should drop (fatter), and rise (~Gaussian) when liquid."

**VERDICT: REJECTED on the EG panel.** Parity at best (doc mapping), robustly WORSE at the
fair centered mapping. The time-variation itself — isolated against a matched-mean static
control — adds nothing and, centered, actively hurts. Same standard that killed CRPS-selection
and width-shrinkage; a DEV-phase rejection this clean does not earn the one final-window shot
(only *promising* DEV candidates do).

## Test design (script: `claude/v4_lab/lab_amihud_dof.py`)

- EG panel, 30 names, 538 non-overlapping 60d walk-forward windows, production harness
  (`fit_har_v3`/`har_forecast_v3`/`simulate_terminal_v3`), n_paths=20k, per-window seed 42+origin.
- **Only nu changes across variants.** Identical drift (carry, q=0 — cancels in the paired
  delta), identical HAR width forecast, identical width_cal=0.972, identical seeds, scored
  against the identical carry-anchored benchmark. So any difference is purely the tail-shape.
- Amihud = |logret| / (price×volume), 22d trailing smooth, strictly point-in-time expanding
  eCDF percentile p(t) (prior data only). nu(t) = nu_hi − p·(nu_hi−nu_lo): illiquid→fat, liquid→Gaussian.
- **Two a-priori mappings, neither tuned on the data:** `doc` = the source's literal [3,8];
  `centered` = [2.5,5.5], built so the time-average sits near EG's own production nu=4 (the doc
  range mis-centers EG toward Gaussian — EG demonstrably wants fat tails, nu=4).
- **Three engine variants per window:** BASELINE (static nu=4, production), CANDIDATE (dynamic
  nu(t)), CONTROL (static nu = the candidate's own time-average). The candidate-vs-CONTROL
  comparison is the decisive one: same average tail level, differing ONLY in the time-variation,
  so it isolates whether *conditioning nu on Amihud* carries information — free of the nu/width_cal
  confound and of any "just a different average nu" effect.
- **Metric:** LOG-space CRPS (proper score for the multiplicative exp(t) model; the raw-price
  CRPS is corrupted by the infinite-mean terminal artifact documented in
  `MC_TailInstability_BlockMix_20260723.md` — it literally blew up ~1e6 when the dynamic nu dipped
  near 3, which is itself a mark against letting nu roam that low). Block-bootstrap 90% CI on the
  paired delta across block sizes {2,3,4} quarters (protocol robustness requirement).

## Results (log-CRPS skill vs shared carry benchmark; higher better)

Baseline static nu=4: **+0.0164**, cov90 0.892.

| Mapping | dyn nu mean | candidate skill | matched-static control | vs BASELINE {2,3,4}Q | vs CONTROL (pure time-variation) {2,3,4}Q |
|---|---|---|---|---|---|
| doc [3,8] | 6.66 | +0.0112 | +0.0121 | PARITY (never better) | PARITY→WORSE |
| centered [2.5,5.5] | 4.70 | +0.0133 | +0.0153 | **WORSE (robust, all blocks)** | **WORSE (robust, all blocks)** |

Candidate win-rate vs baseline: 40% (doc) / 42% (centered) of 538 windows — i.e. it loses the
majority either way. Coverage stays fine (0.888–0.898, inside the ±2% band), so this isn't a
calibration blow-up; the point forecast distribution just scores worse under the proper rule.

## Why it fails (economic read)

Trailing Amihud illiquidity does not predict WHEN the 60-day-ahead tail event lands for these
names. High trailing illiquidity ≠ imminent gap. EG wants *persistent* fat tails (nu≈4) because
jumps are frequent and not forecastable from trailing liquidity; thinning the tails during
"liquid" stretches (which are most of the sample) removes fat-tail protection that was still
earning its keep. The signal's timing is wrong, and the decisive tell is that even holding the
average nu fixed (candidate vs control), the Amihud-driven variation is parity-to-worse — the
conditioning carries no usable information on this panel.

## Scope / honesty notes

- Tested the PER-STOCK own-Amihud → own-nu(t) form. The doc also floated a market-cap-weighted
  AGGREGATE (one systemic nu(t) for the whole panel); not tested (no mktcap weights in the repo).
  Given the per-stock version shows the *conditioning signal itself* is uninformative here, an
  aggregate is unlikely to rescue it, but it's not literally what was run — noted, not claimed.
- This closes the FIRST of the data-available triage candidates. Still untested and next in
  queue: **bid-ask autocovariance denoising of the vol estimate** (Roll's model — attacks the
  width, not the tail) and **CSAD herding → nu toggle** (a different conditioning variable than
  Amihud, so not pre-judged by this result). Production stays on static per-market (nu, width_cal).
