# Which technical claims can carry a per-name record — measured, whole book

Run 31-Aug-2026 after LULU and SALIK were added to the test set. This answers a
question the five-name cut got wrong, and supersedes two statements made from it.

## Two corrections to the first per-name pass

**1. The per-name level record does not fail on sample size.** The first pass read
24–64 paired observations per name and concluded the counts were too small. The
counts are in fact adequate by `band_record.py`'s own floor — across the book,
**68 of 93 names (73%) have ≥40 paired 3M observations** and the median is 62. What
fails is the *effect size*. That floor was derived to catch a cone running 15pp
narrow; the level effect is 3–4pp.

**2. No name's trend clause is significantly backwards.** ENBD was flagged as
pointing the wrong way. Tested properly across all 71 names with both states
populated, **zero are significantly reversed at the 5% level** at either horizon —
ENBD included. The most negative gap in the book is RELIANCE at −0.220, p=0.081.
Withdraw the watch flag.

## What each clause actually needs, and what it has

**Levels.** The paired real-vs-null difference has SD 0.285 at 3M against a mean of
+0.034, so resolving it per name needs:

| horizon | effect | SD | n for 80% power | n for 90% |
|---|---|---|---|---|
| 1M | +0.048 | 0.347 | 405 | 542 |
| 3M | +0.034 | 0.285 | 559 | 749 |

The median name has **62**. The best-endowed name in the entire book has **239**.
Fifteen years is not short of this by a little — it is short by roughly an order of
magnitude, and sampling origins more densely does not fix it because the windows
overlap. **The level claim is a book-level and market-level fact permanently.** It
should never be published per name, at any future library length.

**Tape.** Spearman(ATR%, realized forward vol) per name, names with ≥30 origins:

| horizon | testable | rho > 0 significant at 5% | median rho |
|---|---|---|---|
| 1M | 78 | **70 (90%)** | +0.394 |
| 3M | 78 | **61 (78%)** | +0.353 |

This clause carries a per-name record today, for most of the book.

**Trend.** The above-stack vs below-stack gap in forward up-rate, two-proportion test:

| horizon | testable | significant at 5% | significantly backwards | median abs. gap |
|---|---|---|---|---|
| 1M | 71 | 7 (10%) | **0** | 0.085 |
| 3M | 71 | 15 (21%) | **0** | 0.104 |

Strongest at 3M: IHC +0.524, SWDY +0.346, LCSW +0.319, EGAL +0.307, KABO +0.302,
AGTHIA +0.293. Per name this is readable for the fifth of the book where the name's
own gap is large; everywhere else the market-level figure is the honest one.

## The design this implies

| clause | per-name record? |
|---|---|
| tape (ATR) | **yes, now**, ~80–90% of the book |
| trend (MA stack) | **only where earned** — 7–15 names; market-level otherwise |
| levels (S/R) | **no, permanently** — book/market level only |
| momentum words (RSI) | not a record; the wording contradicts the measurement |

That is the same shape as `band_record.py`'s long / short / market-only strength
ladder, arrived at independently: say it per name where the name's own history can
support it, fall back to the market where it cannot, and never print a figure that
cannot separate an honest read from a broken one.

## LULU and SALIK

| name | clean sessions | origins | verdict |
|---|---|---|---|
| **LULU** | 446 (upload) / <520 (library) | **0** | **not scoreable at all** |
| **SALIK** | 981 / 980 | 19 | every cell n=3–11, nothing readable |

LULU is the one name in the book the calibration cannot reach: the first origin sits
at 520 sessions and LULU has 446. **The technical read is published for LULU
regardless**, because `technicals.compute()` requires only 60 sessions. That gap —
a read we publish and cannot score — is worth naming rather than leaving implicit,
and it closes on its own around Q3-2027 as the library lengthens.

SALIK is scoreable but says nothing: 19 origins, its below-stack state populated by
a single observation. Both are correctly reported as unreadable rather than given a
number, per [R-ENF-04] — an empty result is not a clean result.

## Both uploads are total-return series

Same finding as the first five, now with a clearer mechanism. LULU's divergence from
the library steps in a piecewise-constant staircase — −11.09% → −8.96% → −6.31% →
−3.25% → −3.05% → **0.00%** on 21-Aug-2026 — one step per ex-date. SALIK's median
divergence is 5.07%, converging to 0.000% over the last 90 days.

The first pass reported LULU's last-90-day divergence as 3.05% and read it as
something other than dividend adjustment. That was an artefact of the 90-day window
straddling LULU's final ex-date. **All six dividend-paying uploads are total-return;
only IHC, which pays none, matches the library.** None spliced.
