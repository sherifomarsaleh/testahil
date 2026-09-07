# The projected depreciation carried the wrong sign, and this run's own scorer hid it

**6 September 2026.** A specification defect in this run's forward model, found from
outside it, corrected here, with the run's own scores re-computed and the direction of
the change stated rather than presented as an improvement.

---

## What was wrong

`bottom_up.py` fits the depreciation rate as a ratio off the panel:

```
d_rate = ttm(A, None, o, 3, fn=_ratio("da", "ppe"))
```

**This panel stores `da` NEGATIVE** — the company's own presentation convention, and the
right one; `panel_annual.json` carries `da = −491.8236` for FY2023. So `d_rate` comes out
**negative**, and the projection then ran:

```
da = d_rate * state["ppe"]      # negative x positive  ->  NEGATIVE
f["da"] = -da                   # ->  POSITIVE
...
state["ppe"] = state["ppe"] + cx - da     # ->  ppe + capex + |charge|
...
f["pbt"] = f["gross_profit"] + f.get("sga", 0.0) + f.get("da", 0.0) + f.get("finance_cost", 0.0)
```

Two consequences, both silent:

1. **`pbt` ADDED depreciation to profit instead of deducting it.** At origin 2023,
   horizon 5, the projection carried `da = +726.72` against a filed FY2023 actual of
   `−491.82`.
2. **The property, plant and equipment roll-forward GREW the asset base by the charge**
   as well as by capex, so `ppe` compounded upward and each subsequent year's charge —
   `d_rate x ppe` — grew with it.

## Why nothing inside this run could see it

`score.py` lists `da` in `MAGNITUDE`:

> *Cost and expense lines are stored with the company's own sign, which is negative.
> That sign is a presentation convention, not information: a cost forecast is right or
> wrong by its MAGNITUDE.*

That reasoning is correct and the clause is right to exist. Its effect here was that
**the one driver where the sign was visible was the one driver scored on `|x|`**, so the
depreciation cells looked fine. `net_profit` and `ppe` are not in that set and are scored
on the signed value — and both were wrong.

**Measured before the correction, across the 40 cells carrying both `da` and
`net_profit`: net_profit was overstated by a mean 12.8%, and by 26.7% at its worst
(origin 2024, horizon 1).**

## How it was found

By building [R-VCAL-01]'s cash-flow lens on this run. That instrument needed the
projection's operating profit and its depreciation as separate signed lines, which no
consumer inside this run had ever asked for, and the sign fell out immediately.

## The correction

```
da = abs(d_rate) * state["ppe"]     # the MAGNITUDE, then this panel's own sign
f["da"] = -da
```

Nothing else changes. `capex0` was already right and stays untouched — it is computed as
`ppe_y − ppe_{y−1} − da_y` with `da` negative, which is the identity
`capex = ΔPPE + D&A` and was correct all along.

## What it did to this run's own scored record — worse on two of three

| driver | bias before | bias after | MAE before | MAE after |
|---|---|---|---|---|
| `da` | −0.2531 | **−0.3692** | 0.4352 | **0.5151** |
| `net_profit` | +0.2638 | **+0.1876** | 0.6772 | **0.6577** |
| `ppe` | −0.4586 | **−0.6427** | 0.8082 | **0.8615** |

`da` moved even though it is scored on magnitude, because the magnitude itself changed:
the roll-forward no longer inflates the asset base the charge is struck on, so the
projected charge is smaller and more under-forecast.

**TWO OF THE THREE GOT WORSE AND THE CORRECTION STANDS.** A correction is validated by
being right, not by improving a score, and this house has already written that down in
another costume: *a correction that moves the answer away from the price is not a reason
to reconsider the correction.* The sign was wrong; it is now right.

## Regenerated in the same pass

`bottom_up.json` → `forward_ranges.json`, `diagnostics.json`, `error_cells.json`,
`scores.json`, `tmgh_IS_projected_vs_actual_all_origins.md`. `score.py` reads
`bottom_up.json` for the origin span, so a model change does not reach the scores until
that artefact is rebuilt — the L-066/L-067 shape, and the reason the run order is now
declared in `bottom_up.py`'s own docstring where a rebuilder will see it.

## What this changes elsewhere

The pooled driver-bias census (`engine/valuation_calibration/driver_bias_census.py`)
reads every run's scored record, and [R-TERM-01]'s diagnosis rests on it. Three of
TMGH's drivers have moved, so the census must be **read live** rather than quoted from
any earlier run of it.
