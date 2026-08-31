# Calibrating the technical lens — method and first measurement

**Run 31-Aug-2026.** The method and record here were adopted 31-Aug-2026 as the
technical lens's standing calibration under [R-LENS-02] — BESIDE the MC calibration, on
the lens's own clock, never an input to any other lens. **Nothing here is published or
wired into any lens.** Numbers below are the state of this run; re-run `run_all.py` +
`analyse.py` rather than quoting them from this file.

## The problem

The MC lens is calibrated because every cone is **struck, frozen, dated and graded**:
`in90` in a panel row is a fact about a claim that was actually made. The fundamental
lens is calibrated the same way — a study's fair value is a dated claim the price
later tests.

The technical read has no such record. `technicals.py` is deterministic and
**idempotent**: re-running it on an unchanged library is a no-op, and every pass
overwrites the last. It states claims — a resistance is "the next level price has to
deal with", a bull trigger says a close above R1 "would open the R3 zone" — and
records none of them. There is nothing to grade, and nothing ever has been.

So the first move is not statistics. It is that **the technical read must make a
dated claim that is written down**. With 15 years of library, that record does not
have to be waited for: `technicals.compute()` is a pure function of the cleaned
series up to a date, so it can be re-run at every historical origin on a truncated
library and the claims it *would* have published graded against what happened.

## Method

**The read is re-run, never re-implemented.** Every claim comes out of the shipped
`technicals.compute()` through a new `frame=` injection (behaviour-identical on the
full library; production still passes `None`). A replay that re-derived the levels
would be scoring a different read from the one that ships — the [R-ENF-03] lesson in
Python rather than JS.

**Grid.** Origins every 21 sessions from 520 sessions of history, per name, both
calendar horizons (1M/3M) resolved on the name's own sessions. 92 of 93 libraries on
disk (LULU is too short); 89,190 claim rows, origins 2011-12-30 → 2026-05-19.

**The null is the whole point.** "Price touched R1 in 44% of windows" is a fact about
volatility, not about R1. Each published level is scored against a **distance-matched
non-structural null**: the nearest admissible price inside its distance and the
nearest outside, both at least `CLUSTER_TOL` from every charted cluster, MA, 52-week
extreme and published level — scored and averaged. The pair straddles the real
distance, so the comparison is centred by construction. Same shape as the engine's
own `w90/w90_b`: our number only means something beside the naive one.

**Bar.** The house bar, unchanged: block bootstrap over origins at blocks {2,3,4},
3000 draws, seed 42, ROBUST only when the sign holds across all three; plus
leave-one-name-out and a calendar split-half. Origins overlap at 3M — that is what
the block bootstrap is for.

### Two nulls were built and discarded before this one

Both are recorded because each looked clean and was not:

1. **Single-sided, inward-first** search drew nulls 1.4–4.3% *nearer* than the levels
   they stood for. A nearer price is touched more and broken more for reasons that
   have nothing to do with the chart, and that alone produced a large positive
   "support holds" result.
2. **Alternating the pair order by row** narrowed the offset but did not close it —
   the two sides do not survive the ban at equal rates.

The two-sided pair fixes it structurally. A residual selection remains (the inner
null is likelier to be touched, so the *touched* null sits 0.003–0.006 nearer): the
measured elasticity of break-through to distance is −0.32, so that gap accounts for
**3–4% of the deltas below**, and every finding survives it.

The **population is counted against the libraries on disk** and asserted. The first
count keyed on the bare ticker string and reported 91 of 93 as clean — `ADIB` is a
different bank in EG and AE and shares a filename. [R-ENF-04], caught by the assert.

## What the 15 years say

### 1. The S/R levels are real, and the effect is modest

Break-through rate at the published level vs the distance-matched null, conditional on
both being reached. Positive delta = the published level held more often.

| horizon | claim | n | names | real | null | delta | verdict | LONO | split-half |
|---|---|---|---|---|---|---|---|---|---|
| 1M | R1 | 283 | 72 | 0.802 | 0.848 | +0.046 | robust + | ✓ | ✓ |
| 1M | all resistances | 2078 | 90 | 0.816 | 0.856 | +0.040 | robust + | ✓ | ✓ |
| 1M | S1 | 211 | 67 | 0.758 | 0.801 | +0.043 | robust + | ✓ | ✓ |
| 1M | all supports | 1056 | 84 | 0.733 | 0.799 | +0.066 | robust + | ✓ | ✓ |
| 3M | R1 | 391 | 76 | 0.895 | 0.919 | +0.024 | robust + | ✓ | ✓ |
| 3M | all resistances | 3990 | 91 | 0.896 | 0.927 | +0.031 | robust + | ✓ | ✓ |
| 3M | S1 | 322 | 77 | 0.866 | 0.874 | +0.008 | **not robust** | ✓ | ✗ |
| 3M | all supports | 2002 | 89 | 0.838 | 0.878 | +0.040 | robust + | ✓ | ✓ |

15 of 16 cells robust and same-signed under LONO and split-half. The honest summary
is **"a published level holds about 3–4 percentage points more often than a
non-level at the same distance"** — real, reproducible, and far smaller than the
language of a technical read implies. The one non-result (3M S1) is reported, not
dropped.

### 2. The tape word is a genuine volatility forecast — the strongest thing in the read

Spearman(ATR% at origin, realized forward vol) = **+0.63 (1M) / +0.66 (3M)**, n=10,659.
The four published buckets separate monotonically:

| word | n | median realized fwd vol (1M) |
|---|---|---|
| an orderly tape | 1147 | 0.146 |
| a normal tape | 4896 | 0.236 |
| a lively tape | 3557 | 0.342 |
| a volatile tape | 1059 | 0.461 |

This is the best-calibrated statement the technical lens makes, and it is currently
published as an adjective with no record attached.

### 3. The trend clause carries direction, at the size the tournament already found

Against a base up-rate of 0.526 (1M) / 0.560 (3M):

| clause | horizon | n | up-rate | lift | verdict |
|---|---|---|---|---|---|
| above the whole MA stack | 1M | 3696 | 0.545 | +0.019 | robust + |
| below the whole MA stack | 1M | 2601 | 0.506 | −0.019 | robust − |
| above the whole MA stack | 3M | 3696 | 0.593 | +0.034 | robust + |
| below the whole MA stack | 3M | 2601 | 0.511 | −0.049 | robust − |

Consistent with `direction_tournament/RESULTS_23-08-2026.md`, where `trend200` scored
PASS in AE and EG at both horizons. That evidence was excluded from MC promotion by
[R-LENS-01] clause 2 — correctly, because wiring it into the engine would make two
lenses agree by construction. **The technical lens is its sanctioned home.**

### 4. The momentum words point the wrong way

| word | horizon | n | up-rate | lift vs base | verdict |
|---|---|---|---|---|---|
| "stretched" (RSI ≥ 70) | 1M | 913 | 0.587 | +0.061 | robust + |
| "stretched" (RSI ≥ 70) | 3M | 913 | 0.635 | **+0.076** | robust + |
| "washed out" (RSI < 30) | 3M | 545 | 0.541 | **−0.018** | robust − |
| "soft" (RSI 30–40) | 3M | 1506 | 0.530 | −0.030 | robust − |

"Stretched" reads to an investor as *over-extended, due a pullback*. Over 15 years it
is followed by an up-rate **7.6pp above base** at three months. "Washed out" reads as
*due a bounce*; it is followed by a below-base up-rate. Both words carry real
information and **both connote the opposite of what they predict.**

Note this is not in tension with the tournament's `rsi14` PARITY: that measured a
monotone rank correlation across the whole RSI range, which is ~0. The information is
in the tails, which is exactly where the read puts its words.

**This is the [R-CAL-02] species, found again.** A cautious-sounding label is still a
claim about the world and is audited like one: "failed calibration test" survived
because it *sounded* like conservative disclosure. "Stretched" survives for the same
reason — it sounds like a warning, so nobody checked which way it pointed.

## What this does not establish

- **No parameter here has been fitted, and none should be.** `technicals.py` carries
  ~12 free constants chosen by convention (`PIVOT_K`, `CLUSTER_TOL`,
  `RECENCY_HALFLIFE`, `MIN_DIST`, `SLOPE_FLAT`, `CROSS_FRESH`, the RSI and ATR cut
  points). The module docstring says the promotion rule does not apply because
  nothing is fitted — that is half right: they are not fitted, but they *are* free
  parameters. The moment any is tuned on these 15 years the promotion rule binds in
  full. **Calibrate first; tune only through the gate, if ever.**
- **Look-ahead.** The library is cleaned once and then sliced, the same convention
  `panel_refresh` uses for the MC panels. Step 0.0's back-adjustment is multiplicative
  over the whole pre-event history and every claim scored here is a ratio, so it
  cancels. No indicator reads a bar after its origin.
- **The bull/bear trigger is not yet scored.** "A close above R1 would open the R3
  zone" is the only explicitly conditional forecast the module makes and the most
  directly gradeable claim in it. It needs a conditional-continuation null.
- **Not scored:** the fresh golden/death cross clause, which asserts "a momentum-regime
  change rather than noise inside an intact trend" — a strong empirical claim that
  [R-NEG-01] gives reason to doubt.
- **Nothing is per-market yet.** Every cell above is pooled. A per-market and
  per-name split is the natural next cut, and it is what a published record would
  need.

## Files

- `replay.py` — walk-forward replay of the shipped read; the two-sided null.
- `score.py` — block bootstrap {2,3,4}, LONO, split-half, Wilson.
- `run_all.py` — the book-wide harvest; asserts the population against disk.
- `analyse.py` / `state_ci.py` — the scored tables; write `RESULTS*.json`.

`claims.pkl` (12MB) is regenerated by `run_all.py` and deliberately not committed.
