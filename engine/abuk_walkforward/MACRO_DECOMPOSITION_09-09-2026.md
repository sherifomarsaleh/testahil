# ABUK — the macro/company decomposition on the lines that decide the scope

**INTERNAL.** Run after the drafts were harvested, on the coordinator's
instruction, because DRAFT-ABUK-11 and -12 answered the right question on the
two SMALLEST lines. This runs the identical test on revenue, cost of sales,
gross profit and the volume proxy, pooled and by era, and adds an exact
decomposition the model's own construction makes available.

Everything below is computed by `decompose_macro.py` from the run's own
committed projections. Nothing is retyped.

---

## 1 · The split on the four lines

| driver | era | n | bias | MAE as known | MAE with the actual macro path | macro share | company share |
|---|---|---:|---:|---:|---:|---:|---:|
| revenue | pooled | 20 | -0.469 | 0.497 | 0.269 | **46%** | 54% |
| revenue | E1 pre-spike | 3 | +0.006 | 0.070 | 0.067 | 5% | 95% |
| revenue | E2 spike and after | 17 | -0.552 | 0.573 | 0.304 | **47%** | 53% |
| cost of sales | pooled | 20 | -0.310 | 0.338 | 0.425 | **-26%** | 126% |
| cost of sales | E1 | 3 | +0.088 | 0.088 | 0.148 | **-69%** | 169% |
| cost of sales | E2 | 17 | -0.380 | 0.382 | 0.474 | **-24%** | 124% |
| gross profit | pooled | 20 | -0.643 | 0.711 | 0.252 | **65%** | 35% |
| gross profit | E1 | 3 | -0.113 | 0.183 | 0.111 | 39% | 61% |
| gross profit | E2 | 17 | -0.736 | 0.804 | 0.277 | **66%** | 34% |
| volume proxy | pooled | 20 | +0.225 | 0.269 | 0.269 | **0%** | 100% |
| volume proxy | E1 | 3 | +0.008 | 0.067 | 0.067 | 0% | 100% |
| volume proxy | E2 | 17 | +0.263 | 0.304 | 0.304 | 0% | 100% |

**E1 HAS THREE CELLS.** The "essentially unbiased before the spike" reading —
the thing the era-flip drafts rest on — is three observations against seventeen.
It is not a well-measured era and no ruling should treat it as one.

**Cost of sales has a NEGATIVE macro share in BOTH eras.** Substituting the
actual currency, commodity price and inflation makes the cost error WORSE, not
better. The currency is ruled out for that line, in both regimes, and the error
belongs to the ratio specification: a trailing three-year mean of cost over
revenue cannot carry a regime in which the gas price formula and the urea price
both move, because on this issuer the two are contractually linked to each other.

---

## 2 · The revenue error decomposes exactly, with no residual

The model sets `revenue = volume proxy x urea price x EGP per USD`, and the
volume proxy is DERIVED as `revenue / (urea x FX)`. So

```
ln(rev_proj/rev_act) = ln(vol_proj/vol_act) + ln(urea_o/urea_act) + ln(fx_o/fx_act)
```

is an identity. The three legs sum to the revenue error to machine precision —
the largest residual across all twenty cells is 3.3e-16.

| era | n | volume leg | commodity-price leg | currency leg | total | max residual |
|---|---:|---:|---:|---:|---:|---:|
| pooled | 20 | **+0.225** | **-0.226** | **-0.467** | -0.469 | 3.3e-16 |
| E1 | 3 | +0.008 | -0.065 | +0.063 | +0.006 | 2.9e-16 |
| E2 | 17 | **+0.263** | **-0.255** | **-0.561** | -0.552 | 3.3e-16 |

---

## 3 · Which macro variable carries it — one substitution at a time

| substitution | revenue bias | revenue MAE | net profit bias | net profit MAE |
|---|---:|---:|---:|---:|
| as known — both flat | -0.469 | 0.497 | -0.690 | 0.773 |
| **actual currency only** | **-0.001** | 0.335 | -0.335 | 0.574 |
| actual commodity price only | -0.242 | 0.384 | -0.524 | 0.586 |
| both actual | +0.225 | 0.269 | -0.160 | 0.331 |

**Substituting the exchange rate alone takes the revenue bias from -0.469 to
-0.001.** The currency is the whole of it.

---

## 4 · The volume proxy is not a bias, it is the mirror of the price leg

| | |
|---|---|
| correlation between the volume leg and the commodity leg, 20 cells | **-0.578** |
| slope of the commodity leg on the volume leg | **-1.28** (-1.00 is exact cancellation) |
| mean of the two legs SUMMED | **-0.0013 log** |

The volume proxy is defined as revenue divided by the urea price and the
exchange rate. When the world urea price rises and ABUK's realised revenue does
not rise proportionally — which is what a regulated Ministry-of-Agriculture
quota, a local free market and dated duty windows guarantee — the derived
"volume" falls *by construction*. So the +0.225 volume "bias" and the -0.226
commodity-price "bias" are two readings of one thing, and they cancel to within
0.13% of a log point across twenty cells.

**This is a wiring defect in the driver definition, not a bias to correct with a
factor.** The volume driver and the price driver are not independent, because
one is defined as the other's denominator. It is the L-002 shape exactly: a
steady error that means something is wired wrong, where a multiplier would hide
the wiring instead of fixing it. That the correction test then failed on the
aggregate at three of five origins is the same fact arriving a second way.

**What would fix it, stated so the next run can do it rather than repeat this.**
Separate realisation from tonnage — either by obtaining tonnage (ABUK does not
disclose it; the negative search is on the record) or by defining a realisation
driver explicitly as `realised revenue per tonne / world urea price` and letting
the volume driver carry only what an exogenous demand anchor supports. The
present specification cannot tell the two apart and its error says so.

---

## 5 · This is not an ABUK finding. Ten EGX runs.

Revenue bias and macro share, read live from every completed run's own
`scores.json`.

| run | cells | revenue bias | macro share |
|---|---:|---:|---:|
| ABUK | 20 | -0.469 | 46% |
| AMOC | 9 | -0.570 | 89% |
| ARCC | 25 | -0.278 | 40% |
| EGCH | 55 | -0.596 | 22% |
| GBCO | 35 | -0.004 | 32% |
| PHAR | 12 | -0.310 | 58% |
| PHDC | 35 | **+0.105** | 22% |
| SCEM | 9 | -0.561 | 33% |
| SWDY | 45 | -0.222 | 13% |
| TMGH | 35 | -0.090 | 35% |

**Nine of ten under-forecast revenue. Two-sided sign test p = 0.0215. The mean
bias is -0.2995 log — about 26% too low — across 280 cells and ten companies in
six different industries.** Every run carries a substantial macro share, from
13% to 89%.

**ONE CAVEAT THAT CUTS IN THE SAME DIRECTION AND MUST BE STATED.** The
`macro_split` field is computed by each run's own code and the substitution set
is NOT the same everywhere: PHDC and PHAR substitute the INFLATION path only,
SWDY substitutes inflation and currency, this run substitutes the commodity
price, the currency and inflation. A run that substitutes only inflation reports
a SMALLER macro share than one that also substitutes the currency, by
construction. So the reported shares understate the book-wide macro
contribution rather than overstating it. The SIGN of the revenue bias is
unaffected by the definition and is comparable across all ten.

---

## 6 · What this bears on

ABUK is campaign entry #11 and the first EGX name beyond the ten that
`criterion3.py` scores. Two things follow and both are stated plainly.

1. **The under-forecast of nominal revenue is a property of the METHOD, not of
   Abu Qir.** Every origin in every run holds the exchange rate at its
   origin-dated value because that is the only thing knowable at the origin.
   That is defensible and it is also, in a currency that has stepped three times
   in six years, a systematic downward lean on every nominal line. It will
   reproduce on every Egyptian name and on any emerging-market name whose
   currency moves in steps rather than drifts.

2. **The era problem is the same one criterion 3 already reports about itself.**
   `criterion3.py` clause C prints *"E1 pre-float cells 0 — TOO THIN TO BE A
   SIDE (needs 5)"* and scores E2 alone on 16 cells. This run finds 3 cells
   against 17 across the same kind of break. So on both instruments the question
   "does it hold in both eras" is being answered on one side of a currency
   regime change. That is not a contradiction of a criterion 3 clause — criterion
   3 scores DELIVERED fair values against price, and this run struck none — but
   it is the same limitation surfacing twice, and it is the limitation the UAE
   leg exists to test.
