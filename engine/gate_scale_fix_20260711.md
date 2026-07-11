# Pooled-gate scale-weighting defect — found and fixed, 11-Jul-2026

## The defect

The Step-0 pooled gate scored a market panel as:

    skill = 1 - sum(crps) / sum(crps_b)

summed across every name and window in the panel. **CRPS is denominated in the
units of the forecast variable — price.** A name trading at 380 AED produces
CRPS values roughly 100x larger than a name trading at 3.4 AED for the same
*proportional* forecast quality. Summing raw CRPS across names therefore weights
each name by its share price, not by its information content.

Measured on the live panels the day the 11-name Saudi and 14-name UAE panels
were built:

| Panel | Top name | Its share of the pooled weight | Smallest name |
|---|---|---|---|
| UAE (14 names) | IHC @ 382 AED | **57.9%** | ADNOCGAS 0.2% |
| Saudi (11 names) | ELM @ 874 SAR | **58.7%** | ARAMCO 1.0% |
| Egypt (7 names) | TMGH | **42%** | — |

A "14-name UAE panel verdict" was, arithmetically, an IHC verdict. In Saudi, two
names (ELM + ACWA) carried 79% of an 11-name panel.

The same defect operated **within** a single name across time: IHC ran from 42 to
382 AED over the backtest, so its recent windows outweighed its early windows
roughly 9:1 in that name's own verdict.

## The fix

Normalize each window's score by that window's spot before pooling:

    skill = 1 - sum(crps / spot) / sum(crps_b / spot)

This makes the score scale-free and fixes both the cross-name and the
cross-time weighting in one step. It is now the primary gate basis
(`panel_refresh.py::rescore`). The raw price-weighted figure is still computed
and reported as `*_raw_basis` so numbers already published against the old basis
remain reconcilable.

Concentration after the fix: UAE top-name weight 57.9% -> 11.4% (EAND);
Saudi 58.7% -> 18.5% (MAADEN).

## Effect on existing verdicts

Isolating the normalization alone (same nu/width_cal config, raw vs normalized
score): **zero verdict changes**, market-level or name-level, across all three
fitted markets. The published record is not invalidated.

What *does* change:

- **Confidence intervals tighten sharply.** The UAE panel CI went from
  [-0.088, +0.057] to [-0.006, +0.013] — the old width was almost entirely
  IHC scale-noise, not genuine forecast uncertainty.
- **Headline skills de-inflate.** Egypt's pooled PASS restates from +0.0591
  (raw) to **+0.0387** (normalized). The verdict stands, but the published skill
  figure was ~50% overstated by TMGH's price weight.
- **BOUNDARY cases resolve.** Because the corrected gate is a more powerful test,
  two names that were block-dependent BOUNDARY cases under the old gate resolved
  cleanly once combined with their LONO fits:
  - **SA / RAJHI -> PASS** (skill +0.0151; PIT 0.495, width ratio 0.991 — clean)
  - **AE / ALPHADHABI -> FAIL** (skill -0.0122, robust across blocks {2,3,4})

## ALPHADHABI — the one material consequence

Alpha Dhabi Holding is the house holdco reference exemplar and carries a
published study. Under the corrected gate it is a **robust name-level FAIL**.
The diagnosis is specific and legible:

- band width: engine 90% cone is **1.136x** the benchmark's — too wide
- coverage: cov90 = 0.94 against a 0.90 target — over-covered
- centre: **PIT mean 0.333** (target 0.50) — the median sits systematically above
  realized outcomes

Alpha Dhabi fell from 16.90 to 8.22 across the backtest window. The carry anchor
drifts the median *up* (positive rf, carry-only market — the UAE signal is off),
while the stock declined persistently. Carry-only drift against a structurally
declining name produces exactly this upward centre bias. It is a real failure of
the current UAE configuration on this name, not a scoring artifact.

Ledger banner / tier changes are a publish step and are NOT actioned here.

## Related gap found (not fixed)

`MarketProfile.breaks` is declared on every profile and documented in the
Standing Research Protocol ("volatility pools use post-break windows only where a
MarketProfile lists a structural break") but is **never read** by `mc_v2.py` or
`mc_v3.py`. grep returns no reference. Regime-break vol pooling is documented but
not implemented. Left in place rather than silently changed, because fixing it
would move Egypt's fit (2016 float, 2022-23 devaluations) as well as UAE's.

---

# Addendum — selection procedure tested and NOT changed (11-Jul-2026)

## nu is weakly identified — do not quote it as precise

Profiling the log-likelihood across the nu grid on the refreshed panels:

- **UAE (237 windows, 14 names):** *every* nu from 5 through the Gaussian limit sits
  inside the 95% likelihood interval. nu=4 (the incumbent) is only dlogL=2.23 from
  the MLE at nu=10.
- **Saudi (190 windows, 11 names):** nu=4 through nu=15 are all within the interval.
  The incumbent nu=5 vs the new MLE nu=6 differ by dlogL=0.23 — indistinguishable.
  (The Gaussian limit IS decisively rejected at dlogL=-6.42, so Saudi genuinely has
  fat tails — they are simply not pinned between 4 and 15.)

nu also trades off against width_cal: a fatter tail wants a wider scale to fit the
same residuals. **The (nu, width_cal) PAIR is what is fitted. Neither coordinate is
individually precise and neither should be quoted as though it were.**

## A CRPS-skill grid search was tried, and it LOST out-of-sample

Since nu is weakly identified by likelihood but strongly determines the published
p5/p95, an obvious idea is to select (nu, width_cal) by maximizing pooled CRPS skill
instead of likelihood. In-sample this looked like a clear win (UAE +0.0038 vs the
incumbent's -0.0017).

It was then tested honestly, leave-one-name-out: for each held-out name, run BOTH
selection procedures on the other names only, then score the held-out name.

| Selection procedure | UAE OOS skill | Saudi OOS skill |
|---|---|---|
| **MLE on residuals (house method)** | **+0.0032** | **+0.0008** |
| CRPS-skill grid search | +0.0021 | -0.0011 |
| Incumbent config in production | -0.0017 | -0.0000 |

**The CRPS grid search overfits.** It wins in-sample and loses out-of-sample, in both
markets. The house's existing MLE-on-standardized-residuals procedure is retained
unchanged. This is recorded as a tested-and-rejected idea; do not revive it without
new evidence.

What the exercise *did* establish is that the incumbent **configs** were stale, not
that the **procedure** was wrong. Same procedure + bigger panel = better fit:

| Market | Old config | New config | Panel |
|---|---|---|---|
| Saudi | nu=5, cal=1.28 (2 names) | **nu=6, cal=1.063** (11 names) | cone ~17% narrower |
| UAE | nu=4, cal=1.070 (9-10 names) | **nu=10, cal=1.056** (14 names) | thinner tail |
| Qatar | nu=12, cal=0.972 (3 names) | unchanged — reproduced exactly | — |
| US | nu=12, cal=1.014 (3 names) | unchanged — reproduced exactly | — |

Qatar and the US reproducing the incumbent fits *exactly* is a useful validation that
the refreshed pipeline is the same engine, not a fork.

## Break filtering now applied to the CALIBRATION SAMPLE (partial fix)

`panel_refresh.apply_breaks` now drops windows whose origin precedes a market's last
declared structural break, so pre-regime data no longer contaminates the shape/width
fit. This bit for real on UAE: EAND's OHLC starts in 2016 and 21 of its 39 windows
predate the Jan-2022 workweek switch. Unfiltered, they pulled the UAE fit to
nu=6/cal=1.084; filtered, it is nu=10/cal=1.056.

**This is only a partial fix.** The Standing Research Protocol's actual claim is that
*volatility pools* use post-break windows only, which would require the per-origin vol
estimation INSIDE mc_v3 (the YZ proxy / HAR window) to be break-aware. It still is not
— `breaks` remains unread by mc_v2.py and mc_v3.py. Fixing that would move every
published distribution, Egypt's included, and is left as an open decision.
