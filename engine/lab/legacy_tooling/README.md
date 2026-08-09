# Legacy engine README (June 2026) — recovered 8-Aug-2026

This was a second, stale `README.md` sitting in the project knowledge base behind the current
one (two docs shared the path; only the newer was reachable by path). It describes the v1
engine — "one Monte Carlo model, ten external factors" — and is long superseded by mc_v3.

KEEP IT ANYWAY, for one reason: it is the only surviving documentation of the API of the five
scripts that are still uncommitted — `viz.py`, `ledger_scorer.py`, `demo_verify.py`,
`_demo_verify.py`, `driver_ledger_scorer.py`. When those are recovered to the repo, this file
belongs next to them. It also names `factor_library.py` and `monte_carlo.py`, the "unverified
parallel engine" removed from GitHub in July.

Nothing in it is current. Horizons are session-counted (retired), the factor magnitudes are
flagged uncalibrated, and the engine it documents is not production.

---

# Testahil analytics engine

One Monte Carlo model, ten external factors, seed 42, 50k paths — the machinery behind every
valuation study and the Calibration Ledger. Build a study from a name + OHLC in three calls.

## Files
- `factor_library.py` — per-asset-class factor sets. `classify(ticker)`, `for_ticker(ticker)`,
  `get_factors(class)`, `split(factors)`, `is_calibrated(factors)`. The **EGX-developer** class is
  calibrated from the published TMGH study (real numbers). Every other class carries the Appendix-A
  factor **structure** with starting magnitudes flagged `calibrated=False` — red-pen these at the
  new-asset sign-off before publishing.
- `monte_carlo.py` — `run(anchor, realized_vol, continuous, events, ...) -> MCResult`. Result has
  `.percentile_table()`, `.touch_probability(level, by_day)`, `.prob_between(lo, hi)`.
  `expected_factor_contribution(continuous, events)`.
- `viz.py` — `study_panel(result, levels, path, ticker)` (fan + bells + touch ladder),
  `fan_chart / bells / touch_ladder / scorecard_chart`. EFG teal palette.
- `ledger_scorer.py` — `Cohort`, `score_cohort(c)`, `aggregate(cohorts)`. Band coverage, PIT,
  touch Brier; the plain-language `read` says which tier to move. Built for the PHDC T+60 grade.
- `demo_verify.py` — reproduces a TMGH-shaped run as a check.

## Build a study
```python
import factor_library as fl, monte_carlo as mc, viz
cls, factors = fl.for_ticker("PHDC")
cont, events = fl.split(factors)
res = mc.run(anchor=<close>, realized_vol=<ann_vol_from_OHLC>, continuous=cont, events=events)
print(res.percentile_table())
viz.study_panel(res, levels=[...], path="phdc.png", ticker="PHDC")
```

## Grade a cohort (e.g. PHDC T+60, 2 Sep)
```python
from ledger_scorer import Cohort, aggregate
cohorts = [Cohort("PHDC","2026-07-04","T+60", anchor, {5:..,25:..,50:..,75:..,95:..},
                  realized_close=.., realized_path_high=.., realized_path_low=..,
                  touch_quotes=[(level, stated_prob), ...])]
print(aggregate(cohorts))
```

## Honest caveats
- This is a clean re-implementation of the **published methodology**, not a copy of your existing
  TMGH/PHDC notebook. It reproduces the published T+60 percentiles within ~2% on the median and the
  net +8% factor contribution exactly. **Reconcile it against your current code before adopting** —
  do not silently swap it into a live cohort mid-flight.
- `realized_vol` (diffusion) must be calibrated from the attached OHLC; it already embeds historical
  factor vol, so the C-tier `vol_3m` fields are informational here (used for stress modes), not added
  on top in the base run.
- Discrete impacts are level shifts from a random session forward; measured on daily returns this
  prints path vol a touch high — band coverage, not daily-vol, is the calibration target.
- Non-developer factor magnitudes are **starting judgments**, not finals. Calibrate before publishing.
