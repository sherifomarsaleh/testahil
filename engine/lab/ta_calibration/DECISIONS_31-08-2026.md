# Three decisions — total-return series, FAB/IHC libraries, per-name record scope

31-Aug-2026. Decision 1 answered by instruction ("the obvious one is the total return
one ... yes. Considering that a high dividend affects the share price"); decisions 2
and 3 delegated. Nothing here is executed — decision 1 turns out to be a two-part
change that cannot be made for 7 of 93 names, and decision 2 reverses a claim made
earlier in this session.

## Decision 1 — total-return: right, and it is TWO changes, not one

**The reasoning is correct.** A dividend does drop the share price on the ex-date, and
in a price series that drop is a return the company never actually lost. Measured on
the four dividend-payers here, a single ex-date shows up as a **6.2%–9.1% one-day gap**
between the price series and the total-return series.

**But `carry_log_h` already handles it, and the two corrections would stack.**

```
base = np.log1p(rf) - np.log1p(q_annual)        # mc_v3.py:79
```

The cone centre is anchored at the risk-free rate **minus the dividend yield**,
because the engine forecasts a series that drops on ex-dates. `q_annual` is live and
non-zero across the book — 0.0275, 0.0406, 0.0511 and higher appear in the shipped
ledger, and study strike scripts carry values to 0.0879.

Move the library to total-return and leave that subtraction in place and the dividend
is counted twice: once by a series that no longer falls, once by a carry that still
assumes it does. **Every cone centre is then biased low by 0.7%–2.2% over a
three-month horizon** — the same size as, or larger than, the entire committed
momentum tilt the direction tournament spent a session earning. It is structurally
the WACC double-count the protocol already records: country risk entering once via
the CRP, then again via the raw local yield.

So the change is **total-return library AND `q_annual` = 0, in the same commit,
never one without the other.**

**What it buys is small.** Annualised volatility on the total-return series versus the
price series, on the identical common window:

| name | n | vol (price) | vol (TR) | change |
|---|---|---|---|---|
| EMAAR | 3873 | 0.3231 | 0.3211 | −0.59% |
| EMAARDEV | 2188 | 0.3299 | 0.3255 | −1.32% |
| ENBD | 3742 | 0.3100 | 0.3085 | −0.49% |
| FAB | 2255 | 0.2669 | 0.2623 | −1.70% |
| IHC | 2078 | 0.3339 | 0.3339 | 0.00% |

One to two ex-dates a year cannot move an annualised vol estimate much. The fix is
correct and worth about 1% of the width — a tidy-up, not a repair.

### The technical lens must stay on the price series

This is the part that is not a matter of degree. Back-adjustment deflates every
historical price, so a level that was really tested at 12.75 appears in the
total-return series at 11.57. Both series agree on today's close and disagree on
every level behind it:

| name | close | resistances (price) | resistances (total-return) |
|---|---|---|---|
| EMAAR | 11.000 | 12.75, 13.04, 13.81 | 11.57, 11.96, 12.83 |
| ENBD | 31.000 | 31.26, 31.81, 37.40 | 31.26, 31.87, 36.37 |
| FAB | 19.640 | 20.13, 20.74, 22.00 | 19.81, 20.15, 21.00 |
| IHC | 372.000 | 375.51, 385.09, 400.16 | 375.51, 385.09, 400.16 |

EMAAR's nearest resistance moves from **+15.9% away to +5.2% away**. A support level
is a claim about where orders sit, and the tape has memory of 12.75, not of 11.57 —
nothing ever traded at 11.57. **Total-return levels are prices at which nothing ever
happened.** IHC is identical in both columns because it pays no dividend, which is
the control that proves the mechanism.

The same argument does not touch the MC lens, which consumes returns, not levels.
This is a genuinely lens-specific answer: **total-return for the engine, price for
the technical read** — so the repository would carry two series, which is a real
build and not a swap.

### Why it cannot be done for these seven names

Market fits pool every name in a market. Converting 6 AE names while 22 stay on price
means the AE panel is fitted on a mixed basis, which is worse than either choice made
consistently. **This needs all 93 libraries, or it needs to wait.** Nothing is spliced.

## Decision 2 — FAB: no change. I was wrong earlier today.

Earlier in this session I wrote that FAB's library "carries 1,723 sessions of the
wrong company." **That is incorrect and is withdrawn.** In the 2017 NBAD/FGB merger
NBAD was the *surviving* entity, renamed First Abu Dhabi Bank; NBAD shareholders
carried into FAB one-for-one. The pre-2017 series is FAB's legal predecessor, not a
different company, and the tape shows exactly that — the series runs continuously
through the merger window with no gap above 15%, its largest single move 5.13%, and
9.88 → 10.50 across Feb–Jul 2017.

The upload starts 10-May-2017 because that is where the vendor's data starts, not
because the earlier history belongs to someone else. **The library is the better
series and should be left alone.** This also re-reads the earlier per-name result:
FAB's +15.9pp did not "rest on NBAD history" — the upload simply has six fewer years,
and the shorter sample is the weaker one, not the cleaner one.

## Decision 2b — IHC: a trading-density problem, not a truncation

IHC is one company throughout, so nothing should be deleted for identity reasons.
What the yearly profile shows is a density failure:

| year | sessions | flat bars | median price |
|---|---|---|---|
| 2011 | 27 | 88.9% | 1.10 |
| 2012 | 29 | 96.6% | 1.42 |
| 2015 | 61 | 63.9% | 1.10 |
| 2019 | 219 | 20.5% | 1.80 |
| 2020 | 251 | 7.6% | 29.82 |
| 2024 | 252 | 0.0% | 404.00 |

27 sessions in 2011 against an ADX year of roughly 250, with 89% of those bars flat.
The protocol already has the rule this breaches — *screen a market's trading-day
density against that exchange's real calendar before trusting any fit built on it* —
and Step 0.0 does not catch it because it strips only a **leading** placeholder block,
and IHC's sparse years are interleaved with real ones.

**Ruling: this is a Step 0.0 density gate or a documented structural break, not a
hand-truncation.** Deleting rows by judgement is precisely the untestable,
per-name intervention [R-DRIFT-02] prohibits. The general fix — a per-year density
screen that refuses a fit built on years below a stated fraction of the exchange
calendar — closes the class rather than the instance, per [R-ENF-01], and would be
worth running across all 93 libraries to see who else is affected.

## Decision 3 — the per-name record covers tape and trend, never levels

Measured across the whole book:

| clause | per-name record | evidence |
|---|---|---|
| **tape** (ATR) | **yes** | rho>0 significant for 70/78 names at 1M, 61/78 at 3M |
| **trend** (MA stack) | **where earned** | 7/71 names at 1M, 15/71 at 3M; 0 backwards |
| **levels** (S/R) | **never** | needs n≈560; best name in the book has 239 |
| **momentum words** (RSI) | **no** | the wording contradicts the measurement |

Levels are excluded permanently, not pending more data: fifteen years yields a median
of 62 paired observations per name against the ~560 a 3–4pp effect requires, and
denser origins do not help because the windows overlap. Trend and tape fall back to
the market figure where a name has not earned its own, which is `band_record.py`'s
long / short / market-only ladder reached independently.

The RSI wording is a separate matter from the record: "stretched" is followed by an
up-rate 7.6pp **above** base at three months while reading to an investor as
over-extended. That is a wording defect to fix in `technicals.py`, not a number to
publish.

## What is executed here

Nothing. Decision 1 needs 86 more libraries and a paired `q_annual` change; decision
2 rules that both libraries stay as they are; decision 3 is a design that belongs in
whatever change actually builds the record.
