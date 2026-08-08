# Name-level width_cal shrinkage — inconclusive, not a pass

**20-Jul-2026. Local, read-only test against production machinery. Nothing in
`repo/engine` was modified; nothing was committed or pushed.**

**Corrected bottom line** (my original chat summary oversold this — see below
for the precise numbers, this section is the honest read of them):

- **LGES** — the exact case the TOP OPEN ITEM was written about — moves from
  a clean FAIL to **BOUNDARY(PARITY-flagged)**: the FAIL/PARITY verdict now
  depends on which bootstrap block size {2,3,4} you pick. By this system's
  own rule that state is explicitly *"never a silent proceed"* — it's an open
  flag, not a fix. The flagship case is **not resolved**.
- **ADNOCGAS moved the wrong way**: PARITY → BOUNDARY. The new scheme made a
  previously-stable-looking name *less* certain, not more. That's a cost the
  method introduced, not a neutral side effect.
- **The credibility hyperparameter k is barely identified by 17 names.**
  Bootstrapping which k looks best is bimodal: 44% of resamples want almost
  no shrinkage, but 18.4% want the *opposite extreme* — the setting that
  produces zero improvement over doing nothing. That split is a real reason
  to doubt there's genuine signal here versus noise at this panel size.
  Worse: the within-name cross-validation (leave-one-window-out on 9–18
  windows) is a weak out-of-sample test by construction — removing 1 of ~15
  points barely perturbs the fit, so the scoring is more optimistic than a
  true held-out test would be. That's uncomfortably close to the shape of
  the trap this protocol already flagged once: CRPS-maximizing selection
  "looked clearly better IN-SAMPLE and LOST under LONO ... REJECTED."
- Genuine bright spots, stated plainly so they're not lost: **ALPHADHABI**
  (FAIL → PARITY, clean, skill -0.0139→-0.0012) and **ADCB** (PARITY → PASS)
  both improved unambiguously, and no PARITY/PASS name outright failed. That
  is a real, partial signal — it just doesn't redeem the original ask, which
  was specifically about LGES.

**Verdict: do not promote as-is.** This needs a much larger panel (beyond 17
names) and a sturdier validation than window-level LOWO before it's a real
candidate. As tested, it does not clear the bar.

## Scope

KR (SAMSUNG/KAKAO/LGES, 3 names) + the 14 names currently in AE's *live fitted
panel* per `fitted_configs.json` (ADCB/ADIB/ADNOCGAS/AGTHIA/ALDAR/ALPHADHABI/
DIB/EAND/EMAAR/EMAARDEV/ENBD/FAB/IHC/TWOPOINTZERO) = 17 names, 306 windows.

**Side-finding, not acted on:** `raw_ohlc/AE/` has 19 files, not 14. Four real
tickers — BURJEEL, DEWA, LULU, SALIK — plus a byte-identical duplicate of
ADIB (`ADIBUAE.csv`, `diff` confirms zero difference) exist in the persistent
library but have **never been through `build_panel_file`** — `panel_hashes.json`
has no entry for any of them. Per the protocol, posting a stock should trigger
a whole-market refit automatically; either that hasn't run for these four, or
it ran and hit the materiality gate and is sitting as an unmerged PR. Worth
someone checking. Not touched here.

## Method

- **nu stays at the market LONO fit** (fit on every *other* name in the same
  market) — nu is weakly identified system-wide; fitting it per name on
  9–18 windows would be pure noise, and the open item only calls for
  width_cal to move.
- **Each name's own scale** is a 1-parameter MLE (nu held at the LONO value)
  on that name's own standardized residuals (`u`, taken directly from the
  real committed panel files, hash-verified current against today's raw
  OHLC).
- **Credibility blend:** `s_shrunk = w·s_own + (1-w)·s_l`,
  `w = n_windows / (n_windows + k)`. Thin-history names shrink hard toward
  the market; well-populated names barely move.
- **k chosen out-of-sample, doubly so** — not tuned to make LGES/ALPHADHABI
  look good:
  1. *LONO across names* — `s_l` excludes the target name entirely, same as
     the existing per-name verdict machinery.
  2. *LOWO across the target name's own windows* — its own-scale estimate for
     window *i* is fit on that name's *other* windows only, so a name's score
     never leans on the residual being graded. **See the bottom line above:
     this is weaker protection than it sounds at n=9–18.**
- **Deploy number** (what you'd actually ship) uses *all* of a name's own
  windows, no LOWO — same convention the existing per-name verdict already
  follows.
- `rescore_percal`, a small extension of production's own `fast_rescore` that
  accepts a per-row cal array, was checked bit-for-bit identical to
  `fast_rescore` for a constant cal before use.

## Reproduction check

| Market | Mine | Live registry |
|---|---|---|
| KR | nu=Gaussian, cal=1.154 (n=49) | nu=Gaussian, cal=1.154 |
| AE | nu=10.0, cal=1.049 (n=237) | nu=10.0, cal=1.049 |

Exact match — the local chain reproduces production.

## k stability (this is why the verdict above is "inconclusive," not "passed")

Bootstrapping the 17 names (2000 resamples, argmax-k each draw): the
distribution is wide and **bimodal** — 44.0% of draws pick the most
aggressive setting tested (k=0.5, ≈ trust each name's own data almost
entirely), 18.4% pick the *opposite* extreme (effectively infinite k — "no
shrinkage, zero improvement"). Median argmax = 8, 25th/75th percentiles span
0.5 to 75 — nearly the whole grid. k=12 (used below) is a conservative pick
from the dense middle, not a statistically pinned-down value.

## Results at k=12 (17 names)

| Name | windows | cal: prod → LONO-only → shrunk | skill: prod → LONO-only → shrunk | cov90: LONO → shrunk | verdict (shrunk) |
|---|---|---|---|---|---|
| KR/SAMSUNG | 18 | 1.154 → 1.021 → **1.210** | +0.0323 → +0.0094 → **+0.0407** | 0.72 → 0.78 | PARITY |
| KR/KAKAO | 18 | 1.154 → 1.168 → 1.156 | +0.0029 → +0.0022 → +0.0019 | 0.89 → 0.89 | PARITY |
| KR/LGES | 13 | 1.154 → 1.245 → **1.035** | +0.0323→-0.0268→**+0.0142** | 1.00 → 1.00 | **FAIL → BOUNDARY (unresolved)** |
| AE/ADCB | 18 | 1.049 → 1.063 → 0.969 | +0.0244 → +0.0228 → +0.0318 | 0.94 → 0.83 | **PARITY → PASS** |
| AE/ADIB | 18 | 1.049 → 1.035 → 1.125 | +0.0049 → +0.0051 → +0.0075 | 0.78 → 0.78 | PARITY |
| AE/ADNOCGAS | 9 | 1.049 → 1.063 → 0.931 | +0.0002 → -0.0043 → +0.0340 | 1.00 → 1.00 | **PARITY → BOUNDARY (regression)** |
| AE/AGTHIA | 18 | 1.049 → 1.049 → 1.070 | +0.0073 → +0.0073 → +0.0076 | 0.89 → 0.89 | PARITY |
| AE/ALDAR | 18 | 1.049 → 1.035 → 1.187 | -0.0059 → -0.0102 → +0.0057 | 0.78 → 0.83 | PARITY |
| AE/ALPHADHABI | 16 | 1.049 → 1.063 → **0.977** | -0.0116 → -0.0139 → **-0.0012** | 0.94 → 0.88 | **FAIL → PARITY (clean)** |
| AE/DIB | 18 | 1.049 → 1.035 → 1.092 | -0.0015 → -0.0014 → -0.0010 | 0.89 → 0.89 | PARITY |
| AE/EAND | 18 | 1.049 → 1.063 → 0.985 | +0.0036 → +0.0022 → +0.0090 | 0.89 → 0.89 | PARITY |
| AE/EMAAR | 18 | 1.049 → 1.035 → 1.121 | +0.0064 → +0.0050 → +0.0122 | 0.83 → 0.89 | PARITY |
| AE/EMAARDEV | 18 | 1.049 → 1.056 → 1.056 | +0.0030 → +0.0005 → +0.0005 | 0.94 → 0.94 | PARITY |
| AE/ENBD | 18 | 1.049 → 1.056 → 1.044 | +0.0024 → +0.0015 → +0.0011 | 0.89 → 0.89 | PARITY |
| AE/FAB | 18 | 1.049 → 1.042 → 1.116 | -0.0063 → -0.0065 → -0.0053 | 0.83 → 0.83 | PARITY |
| AE/IHC | 18 | 1.049 → 1.056 → 0.953 | +0.0473 → +0.0474 → +0.0433 | 0.89 → 0.89 | PARITY |
| AE/TWOPOINTZERO | 14 | 1.049 → 1.049 → 1.049 | +0.0007 → +0.0007 → +0.0007 | 0.93 → 0.93 | PARITY |

No PARITY/PASS name outright fails. But one of the two motivating FAILs
(LGES) only reaches an unresolved BOUNDARY, and one previously-clean PARITY
(ADNOCGAS) becomes an unresolved BOUNDARY too — the method has a real cost
column, not just a benefit column.

Notably the mechanism isn't one-directional: **SAMSUNG was under-covered**
(cov90=0.72, its own vol running hotter than the market pool implies) and
shrinkage correctly *widens* its cone (cal 1.021→1.210), moving coverage
toward nominal. That's a genuine property of the mechanism — it doesn't
change the bottom line on LGES.

## Market-panel level

| Market | Production | Per-name-shrunk |
|---|---|---|
| KR | skill +0.0144, CI90 [-0.003, 0.030], PARITY | skill +0.0216, CI90 [0.002, 0.039], PASS |
| AE | skill +0.0049, CI90 [-0.004, 0.015], PARITY | skill +0.0083, CI90 [0.001, 0.017], PASS |

Both aggregate panel verdicts improve. Aggregates can improve even when the
single name that motivated the exercise doesn't resolve — worth remembering
before reading this row as vindication.

## Honest caveats

1. k is not identified with any confidence (above) — 12 is a judgment call
   from a wide, bimodal range, not a fitted constant.
2. Thin-history names (LGES 13, ADNOCGAS 9, ALPHADHABI 16, TWOPOINTZERO 14)
   carry real estimation risk in their own-scale term; LOWO on that few
   points is weak protection, not strong protection.
3. k was selected on 17 names (KR+AE only) — a production-grade attempt
   should use the full ~65-name universe and probably fit k per-market.
4. **This candidate has not survived its own out-of-sample test with
   confidence** — it shows a partial, plausible signal (ALPHADHABI, ADCB)
   but does not resolve LGES and introduces one regression (ADNOCGAS). That
   does not meet the bar the protocol sets before something is even worth
   floating for the PR/review path, let alone merging.

## What was not touched

`repo/engine/*.py`, `market_profiles.py`, `fitted_configs.json`,
`panel_hashes.json` — all read-only. No git add/commit/push. No PAT was
requested or used. Everything above lives in a local clone and two standalone
scripts (`shrinkage_test.py`, `shrinkage_test2.py`), not inside `repo/engine`.
