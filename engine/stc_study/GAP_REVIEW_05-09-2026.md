# STC — gap review, 5 September 2026

The rebuilt central sits **20.7% below** the latest known price, past [R-GAP-01]'s ten per
cent trigger, so the study is not finished until this review has covered its eight headings.
The trigger is **evidential, not deferential**: errors in a discounted cash flow are not
symmetric — a stale base year, an over-charged discount rate, a missed revenue line, a
real-terms terminal decline, an unread filing all push value DOWN — so a large discount is a
high-prior-of-defect region and the price is the only instrument in the room that measures
it. The rule does not say the answer must change.

| | |
|---|---:|
| central, the cash-flow lens under [R-LENS-03] | **SAR 34.8885** |
| latest known close, 3 September 2026 | 43.86 |
| **gap** | **−20.45%** |
| envelope, the range of the present-value reads | 34.23 – 47.15 |
| where it stood before tonight's driver rebuild | 41.1548, −6.17% |

## 1. LATEST FILINGS

**Every disclosed period has been read, and the most recent is the reviewed interim for the
six months to 30 June 2026.** Five sets are in `src/` with the URL each came from: the
audited statements for FY2023, FY2024 and FY2025, and the reviewed interims for the three
and six months to 31 March and 30 June 2026. The delivered study stood on first-quarter
figures while the half-year set was already published; that is corrected and the bridge now
stands on the 30 June sheet.

**Nothing was found unread.** The one thing not in the register is the investor-relations
channel — presentations and earnings-call material — which is where subscriber counts and
revenue per user would be if this company publishes them, and which SIGCM's Company ring
requires. That gap is named in `DRIVER_REBUILD_05-09-2026.md` and it bears on the *finest
sourced level*, not on whether a period was missed.

## 2. BASE YEAR

**The base foots to the filed periods and nothing in it is annualised, scaled or solved.**
FY2025 revenue of 77,818.675, gross profit 37,699.689, EBITDA 24,469.435, EBIT 14,438.264
and D&A 10,031.171 each reconcile to note 9 of the audited statements to the riyal, and the
segment table foots to its own stated total in both years. FY2023 was checked on **both**
bases and the bridge between them foots exactly (72,336.611 as originally reported, less
TAWAL and its eliminations, less note 49's reclassification, to 71,777.161).

**One exception was found and it is in the delivered study rather than in this base.** Its
cash line read 30,755 for FY2024 against a note-20 figure of 15,543 and 15,080 for FY2025
against 13,376 — very nearly double in one year — with no source named for the wider figure.
The rebuilt bridge uses the disclosed lines, and the FY2025 closing figure is corroborated
independently by the Q2-2026 cash-flow statement's own opening balance.

## 3. MACRO COHERENCE

**One path, one economy.** Inflation, the terminal risk-free rate and terminal growth all
come from `engine/macro_paths/SA.json` and nothing in this study carries an inflation number
of its own. The three historical prints used to deflate the trailing growth rates are dated
scalars from the same IMF database, series and country row as the forward ladder, so the
history and the forecast are the same economy. The riyal is pegged, so the currency path is
flat by construction of the peg and the cost-of-capital schedule is flat for the same
reason — stated by the module rather than assumed by the study.

**The one thing this heading found is a defect in my own reasoning rather than in a number.**
Terminal growth is the rule's stated default of zero real, and the justification first
written for it read "a mature domestic telecom growing with the economy in perpetuity" —
which describes a POSITIVE real rate, since an economy grows by inflation plus real output
and a company growing at inflation alone grows with prices only. The number was defensible
and the reason was false, which is the more dangerous of the two because it survives review.
Corrected in place: zero real means STC's revenue grows with the price level for ever and
**its share of Saudi output declines in perpetuity**. That is written down as the real
assumption it is. It is not moved, because any positive rate would have to be sourced and
telecommunications revenue has fallen as a share of output across most markets for two
decades — "it holds its share of a growing economy" is a claim about this company that
nothing here evidences.

## 4. DISCOUNT RATE

**The operations are discounted at the right rate and the cash is charged for exactly once.**
The schedule comes from `engine/cost_of_capital.py`: the risk-free is normalised by Saudi
Arabia's OWN default spread, so country risk is counted once rather than twice as it was in
the delivered study, which used a raw local sovereign yield and then added a premium loaded
with the same risk. Weights are **gross** — market capitalisation over market capitalisation
plus gross borrowings — so no cash is netted inside the rate, and the cash added in the
bridge is therefore charged once. Cost of capital 8.133% on the swap basis, 8.103% on the
rating basis.

**The beta is the largest single input and it moved the most.** A 40-session daily
regression over nine weeks gave 0.48; the conforming own-stock weekly regression against
TASI gives 0.7078 over 252 observations and 4.91 years. That correction alone took 13.75% off
the value and it is the reason the answer is where it is. It is not a candidate for
reversal: the daily construction is not one of the three tiers the rule recognises.

## 5. TERMINAL

**Terminal growth is coherent with the inflation inside the terminal discount rate** — both
are the house path's 2.0%, derived rather than quoted, and the market is pegged so the
terminal rate equals the explicit-window rate by construction of the peg rather than by
assumption.

**THIS HEADING FOUND THE ONE STRUCTURAL TENSION IN THE MODEL AND IT IS RECORDED RATHER THAN
RESOLVED.** Maintenance in the terminal is book depreciation escalated to current cost over
the measured age of the base, 15.23 years, a factor of 1.3519 — which comes to **17.43% of
terminal revenue**, essentially the TOP of management's 15.0–17.5% capital-expenditure
guidance band. The explicit window meanwhile takes capital expenditure DOWN to **15.0% of
revenue**, the bottom of that band, by the last explicit year. Free cash flow therefore steps
from 12,114 in the last explicit year to 10,059 in the terminal, a fall of 17% at the
boundary.

[R-TERM-01] permits the two to differ and requires the reason to be **economic rather than a
fudge**: its own example is a young plant genuinely spending less than replacement
depreciation for a while. **This base is not young.** Seventy-three per cent of it is written
off and it stands at 1.46 times half its own implied life, so the step points the wrong way
for the asset it describes — an old base should be spending *more* than replacement
depreciation to catch up, not less. **The suspect half is the explicit window, not the
terminal**: a declining capital intensity on an ageing base flatters the five years before
the terminal, which means this defect makes the answer too HIGH rather than too low and
cannot explain the discount. It is recorded here and it is the first thing the next edition
should price.

## 6. BALANCE SHEET

**The bridge stands on the latest disclosed balance sheet**, the reviewed 30 June 2026 sheet,
and every line is read from it. The largest correction in the whole rebuild sits here and it
runs the other way: associates and joint ventures were carried at **4,641 against a filed
12,910**, a figure from before February 2025, when the group contributed its whole towers
business to DIIC in exchange for 43.06% of it. Adding 8,269 of associate value **raised** the
answer by 3.55%, which is a defect found in the direction that closes the gap rather than
opens it.

Two omissions are stated with their directions, and **both understate the answer**: STC
Bank's own equity value appears in this bridge nowhere, because its cash backs customer
balances and is excluded from net debt rather than netted; and no market cross-check is
taken on BGSM's look-through into a listed Malaysian operator, because that price is not
held. Neither is filled with a number nothing supports.

## 7. CLAIMS AGAINST THE RECORD

**No "best ever", "never", "highest" or "unprecedented" claim is made anywhere in this
study's committed record**, so there is nothing of that kind to recompute. Every figure a
reader would see is computed from the committed numbers file; the multiple, the life, the
age and the share count that were previously typed are now each derived from a filed
disclosure and asserted in code.

The one claim worth stating plainly is the negative one: **this is a rebuilt model, not a
delivered study.** It has no bibliography, no four-field inputs register, no sweep register,
no QC gate, no driver test and no recalculation harness, and nothing here has been published.

## 8. MULTIPLE CROSS-CHECK

**This is the heading that argues hardest against the answer, and it is set out rather than
explained away.**

| | at the fair value | at the traded price | this company's own history |
|---|---:|---:|---:|
| enterprise value / FY2026 EBITDA | **6.26x** | 8.98x | 8.32x – 9.13x |
| price / FY2026 earnings | **14.6x** | 18.4x | — |

**The fair value implies an enterprise multiple below every one of the last three years.**
That is a real disagreement and it does not dissolve on inspection. Three readings of it,
and the honest answer is that the third cannot be ruled out:

1. **It follows arithmetically from the terminal.** Maintenance at current cost on a base
   fifteen years old is 35% above book depreciation for ever, so this company converts
   materially less EBITDA into distributable cash than a young one, and a lower multiple is
   what that means. The historical multiples embed no such charge because the market has
   never had to state one.
2. **It follows from the growth.** Revenue compounds at 2.50% nominal against the delivered
   study's 3.71%, because every segment now grows at **its own measured rate** rather than
   at four typed arrays, and the measured rates are lower — stc, two thirds of revenue,
   grows +0.16% real. The market may be paying for growth this company's own last three
   years do not show.
3. **The trailing window is two years and that is short.** A rate measured over FY2023 to
   FY2025 and extrapolated is a crude driver, chosen because it is mechanical and sourced
   rather than because it is good. If those two years understate the run rate — a plausible
   reading, since Channels fell 7% in FY2025 alone and may be a one-off — the whole forecast
   is too low, and the gap is ours.

**What would settle it was found the same morning, and it sharpens the third reading rather
than removing it.** The investor-relations channel was reachable all along — four guessed
URLs had failed and been written up as evidence it was gone — and its earnings presentations
carry the subscriber base by category at three fiscal year ends. The `stc` segment is now
built as **volume times price**: a subscriber base compounding at **+6.00%** a year against
revenue per subscriber falling **−3.86%** nominal, which multiply back to exactly the +1.91%
the audited statements report.

**That does not close the gap and it was not expected to** — the two halves multiply to the
net either way, and the answer moves 0.26%. What it does is make the question answerable: the
forecast's growth rests on a volume line that Saudi mobile penetration cannot extend for ever
and a price line that may not fall for ever, and those are now two visible assumptions instead
of one invisible net. A later edition can fade them differently with a reason. **The remaining
gap between the segment counts and a true unit build is that these are chart labels from an
unaudited page, and that is what is still to be found in a table.**

## The verdict

**The gap is ours to the extent that the driver rule is crude, and the rule is crude for a
stated reason rather than a hidden one.** No defect was found in the base year, the filings,
the macro coherence, the discount rate or the bridge that would close it; the two defects
this review did find — a false justification for the terminal growth rate and a declining
capital intensity on an ageing base — both make the answer too HIGH, not too low, so
correcting either widens the discount rather than closing it.

**The answer does not move on this review.** What moves is the queue: revenue is built from
an extrapolated two-year rate because the disclosure this study holds stops at the segment,
and the honest next step is to get the disclosure that goes below it rather than to adjust
the rate until the answer is comfortable. **A fair value moved to meet a price is the
reverse-engineered rate this protocol prohibits outright, arriving through the front door.**

The study is HELD in any case: [R-GAP-02] blocks publication past 10% below the price, and
Phase 1 of the method reassessment is not proven, which holds every study in the book.

*AUDITED CENTRAL: 34.8885* — the figure this review audits, stated so a job outside the
study can tell whether the review still describes the answer the study publishes.

*AUDITED GAP: -20.5%* — the disagreement this review interrogates, stated so a job outside
the study can tell whether the eight headings were asked at the size the study now carries.
