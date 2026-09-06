# SWDY — gap review, 6 September 2026

**AUDITED CENTRAL: 55.4822** — the cash-flow lens, EGP per share. Unchanged from the
4 September review; nothing in the model has moved since.

**AUDITED GAP: -59.3%** against the latest known price, EGP 136.20 (6 September 2026,
`engine/raw_ohlc/EG/SWDY.csv`, the close in this name's own library after that day's
roll-forward). Against the corrected 3 September close of EGP 130.00 the gap is -57.3%.
Against the price this study was struck at, EGP 105.20 (5 August 2026), it is -47.3%.

## Why this review exists, and it is not because the answer moved

**The 4 September review audited a price that never traded.** It states AUDITED GAP -38.7%
against a latest known price of EGP 90.50, taken from
`engine/prices/SUPPLIED_03-09-2026.json`. That figure was wrong. SWDY closed at **130.00**
on 3 September. The true gap on the day that review was written was **-57.3%**, not -38.7%
— eighteen and a half percentage points wider, more than three times [R-GAP-01 AMENDED]'s
five-point staleness tolerance.

The supplied file itself is sound and the error was one row in it: every other EG name in
it reconciles to its own library (COMI 0.9999, EMFD 1.0073, ORHD 1.0120 against libraries
reaching 1 September), and three independent published anchors reproduce from the merged
series to the cent — a previous close of 126.20 into 25 August, a 52-week low of 62.03 and
a 52-week high of 133.98 as it stood that day. 90.50/130.00 is 0.696, which no corporate
action in this name's record explains and which the vendor export contradicts: that export
agrees with the held library to the cent on all 35 overlapping sessions after 14 June 2026,
including the 5 August close of 105.20 this study was struck at. The row is corrected in
that file with its route recorded.

**This is the failure mode [R-GAP-01 AMENDED] was written for, arriving from the one
direction nobody guarded.** That amendment worried about a review written against a price
four weeks *old*. Here the price was three days old and simply *wrong*, and the gate could
not see it either way, because the 4 September review states its gap with a Unicode minus
sign (U+2212) that `AUDITED_GAP_RX` does not match — so `_audited_gap` returned `None` and
the staleness clause could not fire on it at all. Four of the twenty reviews that state a
gap are unreadable to the gate for that reason, the exemplar among them. Reported, not
fixed here: widening that regex reaches every study in the book and is its own change.

## What changed, and it is the verdict rather than a number

The model has not moved. What has moved is the size of the disagreement the eight headings
exist to interrogate, and at -59.3% **the 4 September verdict does not survive its own
evidence.**

That review concluded the gap was "one parameter — the currency the cash flows are
discounted in", and it could say so honestly because against 90.50 the published
currency-of-discounting alternative of EGP 69.58 sat -23.1% away: close enough that one
contested construction plausibly spanned the disagreement.

Against 136.20 it does not:

| | value | vs 136.20 |
|---|---:|---:|
| cash-flow lens — the central | 55.48 | **-59.3%** |
| currency-of-discounting alternative | 69.58 | **-48.9%** |
| relative lens (cross-check) | 80.58 | **-40.8%** |
| **bull case** | **104.96** | **-22.9%** |
| bear case | 19.89 | -85.4% |

**The study's own BULL case is 22.9% below the market.** No single published construction
in this study, and no combination of them, reaches the price. A review whose conclusion is
"one contested parameter explains this" is not available at this gap, and saying so is the
whole point of re-running against the right price.

---

## LATEST FILINGS

Re-checked, and the position is unchanged from 4 September: every disclosed period has been
read. The audited FY2025 statements (March 2026) and the reviewed condensed interim
statements for the six months to 30 June 2026 (approved for issuance 11 August 2026, note
2-1) are both consumed, along with Q1-2026. The H1 half was approved six days AFTER this
study was struck on 5 August, so there was no unread filing on the first edition's desk;
the half is now consumed and re-anchored every segment margin and the corporate load.

No filing has been published since. **Found: nothing new.**

## BASE YEAR

Unchanged and re-verified against the committed record. FY2025 is a filed audited full year;
segment revenue sums exactly to the consolidated figure in all three years and segment
profit less the corporate load reproduces audited operating profit in all three.

The naming defect the last review caught stands corrected: the note-16 **segment profit**
row (gross profit less selling and distribution) is registered under a key named `gp`, and
comparing it against a gross-profit margin is [L-289] — a ratio between two quantities
defined differently. **Found: nothing new.**

## MACRO COHERENCE

Re-verified live against `engine/macro_path.py EG` rather than carried forward. The house
path's terminal inflation is 7.00% and the study's `pi_term` is 7.00%; `g_term_real` is a
STATED zero and `g_term` derives to 7.00%. Coherent.

**The one residual remains open and still runs away from the price.** The study's terminal
risk-free is 10.5% (`rf_term`) against the house derivation of 12.50% — terminal inflation
of 7.00% plus the 5.50% real-rate convention, read live from the path today. Correcting it
lowers the value and widens the gap.

**Found: coherent; one registered residual, direction away from the price.**

## DISCOUNT RATE

| | |
|---|---:|
| Cost of equity, explicit window | 28.40% |
| Cost of capital, explicit window | 26.63% |
| Cost of capital, terminal | 15.93% |
| Egyptian risk-free | 22.31% |
| Beta (own-stock, weekly, 5y, vs EGX30) | 1.0087, R² 0.291, n 258 |

Every figure re-read from the committed record. The two findings the last review registered
are still open and **both still run against the price**: the adopted cost of debt of 9.50%
sits 12.8 points BELOW the sovereign that taxes this company, which [R-COC-01] refuses
outright on a local-currency book — the study computes the local-equivalent at 13.94% and
publishes EGP 55.16 as an alternative — and the terminal risk-free is 200bp under the house
derivation. Adopting either lowers the value.

The construction running the other way is the crux and is published, not adopted: 52.6% of
forecast revenue is earned in hard currency, and the currency-of-discounting alternative
reads **EGP 69.58**. At 90.50 that was a plausible bridge across the gap. At 136.20 it
closes ten and a half points of a fifty-nine point disagreement and leaves 48.9%.

**Found: the same single construction, and it is no longer sufficient to explain the gap.**

## TERMINAL

The terminal carries **85.0%** of enterprise value. Rebuilt through the sanctioned module
on a life derived by identity from note 17 at 17.26 years, with implied payout of 56.9% of
terminal NOPAT and 8.6% above the NOPAT-perpetuity floor; terminal ROIC 20.10% against a
reinvestment rate of 34.82%. Growth is 7.00% nominal on a stated zero real.

Nothing here has moved and nothing new was found. The heading is capable of producing the
whole gap and does not: at 85% of enterprise value the terminal would have to be wrong by
roughly 70% to reach the price on its own, and its construction is now the sanctioned one
on a disclosed life. **Found: nothing new.**

## BALANCE SHEET

The bridge stands on 31 December 2025 and the reviewed 30 June 2026 sheet is deliberately
not used — net financial debt rose from 20,560 to 28,629 over the half, and that
deterioration is not information the model lacks: its own FY2026 forecast absorbs cash on
exactly that mechanism, a working-capital movement of 17,783 against capex of 16,281, for
free cash flow to the firm of -4,268. Deducting the June net debt from a valuation dated
31 December 2025 charges one outflow twice. The half reaches the study through the forecast.

The minority is deducted at a 9.675% share of value against non-controlling interests of
7.47% of total equity at 30 June, 7.11% at December and 6.81% of the half's profit — the
study's figure is conservative on all three readings and the alternative sequencing is
published at EGP 62.37, which is still -54.2% against 136.20.

**Found: nothing new; one construction declined with its reason, as before.**

## CLAIMS AGAINST THE RECORD

The employees' statutory share of distributable profits is charged, at the three-period mean
of 12.19%: FY2024 2,025.8 on attributable profit of 17,461.4 (11.60%), FY2025 2,073.1 on
17,330.2 (11.96%), H1-2026 1,291.2 on 9,921.7 (13.01%). It is an appropriation disclosed
only in the earnings-per-share note, so it appears in no income-statement line; the
reconciliation that exposes it is the study's own reported EPS of 7.13 against
17,330.245 / 2,140.778 = 8.095. The statutory cap at total annual wages is not modelled
because nothing in the filings discloses its headroom, so the charge is an upper bound and
the direction of the unmodelled cap is recorded rather than guessed.

**One new claim fails, and it is this review's predecessor rather than the study.** The
4 September review states "the market is paying 4.9x forward EBITDA where that arithmetic
says 3.2x". Both halves of that sentence are wrong, for two independent reasons set out
under the next heading, and the corrected reading reverses its direction.

**Found: the study's claims hold; the prior review's headline claim does not.**

## MULTIPLE CROSS-CHECK

**This heading now carries the review, and it reverses the last one's finding.**

Recomputed on ONE construction applied identically to every row — enterprise value =
value per share x 2,140.778mn shares in issue + net debt 20,560 + minority 12,904 -
associates 6,758, against FY2027E EBITDA of 43,447 and FY2025 reported EPS of 7.13:

| | P/E (FY25) | EV/EBITDA (FY27E) |
|---|---:|---:|
| cash-flow lens — the central, 55.48 | 7.8x | **3.3x** |
| currency alternative, 69.58 | 9.8x | 4.0x |
| relative lens, 80.58 | 11.3x | 4.6x |
| bull case, 104.96 | 14.7x | 5.8x |
| struck spot, 105.20 (5 Aug) | 14.8x | 5.8x |
| **3-Sep close, 130.00 (corrected)** | **18.2x** | **7.0x** |
| **6-Sep close, 136.20 (latest)** | **19.1x** | **7.3x** |

**The direction of the finding inverts.** This study adopts a justified multiple of **6.5x**
on mid-cycle FY2027E EBITDA. Against the wrong price of 90.50 the market appeared to pay
4.9x — BELOW the study's own justified multiple, which reads as a market that is cheap on
this study's own yardstick and made "the cash-flow lens is the outlier" a comfortable
conclusion. Against the true price the market pays **7.3x, ABOVE the 6.5x this study calls
justified**. Applied undiscounted to FY2027E EBITDA, 6.5x implies EGP 119.44/share, and the
latest close is **+14.0%** against that.

So the market is no longer inside this study's own relative yardstick. It has passed
through it.

**Two construction defects in the prior review's own table were found by recomputing it,
and both are recorded because each individually changes a published figure:**

- **It divided by 1,906.6mn, which is not a share count.** That number is `eq_attr / ps`,
  and because `ps` is the December value rolled 217 days to the anchor at a factor of
  1.16026, it equals shares / roll. The share count is **2,140.778mn**. This is [L-289] in
  the same table that cites [L-289] — a ratio between two quantities defined differently.
- **It used two different bridges in one comparison.** Its fair-value column carries
  December net debt of 20,560 and its price column the June figure of 28,629. On the
  consistent December bridge its price column reads 4.7x, not the 4.9x published. A table a
  reader is asked to compare across must hold one construction in both columns.

Neither defect is large on its own. Together with the wrong price they are why the last
review's sharpest sentence pointed the wrong way.

**Found: the market pays above this study's own justified multiple, not below it.**

---

## Verdict

**The answer does not change and the study remains HELD under [R-GAP-02].** The central is
still EGP 55.48, no correction found here moves it, and every open residual — the cost of
debt below its own sovereign, the terminal risk-free 200bp under the house derivation —
runs AWAY from the price rather than toward it. A fair value moved to meet a quote is the
reverse-engineered rate this method prohibits outright, and nothing in this review is an
argument for moving it.

**What is different from 4 September is the honesty of the explanation.** That review could
say the disagreement reduced to one contested parameter. This one cannot. At -59.3% the
currency alternative leaves 48.9%, the relative cross-check leaves 40.8%, and the study's
own bull case leaves 22.9%. There is no published construction in this study that reaches
the market, and the market now pays more than the multiple this study itself calls
justified.

That leaves exactly two readings, and this review does not pretend to settle them:

1. **The market is wrong**, in which case [R-GAP-02] requires a MARKET_DISSENT naming a
   mechanism from the filings and a reverse read landing on a NON-credible number. On the
   arithmetic above that case is now HARDER than it was on 4 September, not easier: a
   reverse read at 136.20 lands on 7.3x FY2027E EBITDA, which is not an absurd multiple for
   a diversified industrial with half its revenue in hard currency. **A reverse read landing
   on a believable number is evidence against the dissent**, and this one does.
2. **The model is missing something structural** that a stale base year, a discount rate or
   a terminal does not capture — most plausibly the same hard-currency question the crux
   already names, but at a magnitude the published alternative does not reach.

**What would change the verdict:** a defensible basis for discounting the hard-currency leg
at a hard-currency rate as the CENTRAL rather than the alternative, AND a second correction
of similar size. One of them is not enough any more, and that is the measurable difference
between this review and its predecessor. Both are method questions that apply to every
exporter in this book and belong in the method reassessment rather than in one name's
review.

**Registered, not closed:** `engine/swdy_study/path_to_130.json` carries a base of 70.99
against a published central of 55.48 and declares no vintage, so it is an [R-ENF-06]
artefact a rebuild has left behind. It is not read by this review and none of its figures
appear above.
