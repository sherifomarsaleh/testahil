# DU — gap review, 4 September 2026

**AUDITED CENTRAL: 18.8909** — the cash-flow lens, AED per share.
**AUDITED GAP: +66.3%** against the latest known price, AED 11.36 (3 September 2026,
`engine/prices/SUPPLIED_03-09-2026.json`). Against the price this study was struck at,
AED 12.30 (7 August 2026), the gap is +53.6%.

This fires the ABOVE-price half of the audit trigger. Under [R-GAP-02] as amended that
half carries **no publication block** — the block is one-sided below the price, because
the errors in a discounted cash flow are not symmetric and a large discount is the
high-prior-of-defect region. So nothing holds this study, and this review is the only
instrument standing here. It is written on that basis, and the rule's own stated cost —
"an over-optimistic study is no longer HELD" — has a live instance in it.

## What this review found, before the headings

**Every heading either found nothing or pointed at the same single number, and the one
correction the review produced moves the answer FURTHER from the price.**

That last part matters and is recorded rather than smoothed. The terminal-value census
flagged DU as the most extreme under-charger in the book — a capital charge of 9.1% of
terminal profit, an implied replacement cycle of 40 years, a terminal 56.5% above its own
floor. Rebuilt through the sanctioned module on a life derived from du's own audited
notes, the terminal comes out **5.6% higher**, and the fair value with it: 18.89 → 19.80,
+66.3% → +74.3%. A correction that moves the answer away from the price is not a reason to
reconsider the correction.

---

## LATEST FILINGS

Every disclosed period has been read, and the register was re-walked against du's own
investor-relations publications index on the day of this review rather than trusted.

| Document | Date | Read |
|---|---|---|
| Audited consolidated financial statements, year ended 31 Dec 2025 | 9 Feb 2026 | yes — full statements and notes 3.2, 6, 7, 8, 26, 31 |
| Reviewed condensed interim statements, six months to 30 Jun 2026 | 22 Jul 2026 | yes — including the statement of financial position, read by OCR off the rendered page because that page carries no text layer |
| Q2-2026 earnings release | 22 Jul 2026 | yes |
| Audited consolidated financial statements, FY2023 (carrying FY2022) | 13 Feb 2024 | yes — income statement and note 26 |

The most recent filing of any kind is the 22 July 2026 interim set. Nothing has been
published since; Q3-2026 is not due. **The most recent period is fully consumed**: the
FY2026 build chains off the reviewed H1-2026 actuals rather than off FY2025.

One item was added to the study by this review. The FY2022 comparative was read out of the
FY2023 statements so that the section-1.4 superlative has a record to be superlative over
— see CLAIMS AGAINST THE RECORD below.

**Nothing found.**

## BASE YEAR

The base year foots to the audited statements line by line, to the thousand:

| | Audited FY2025 (AED 000) | This study (AED mn) |
|---|---|---|
| Total revenue | 15,905,421 | 15,905.4 |
| Operating profit before D&A | 7,338,388 | 7,338.4 |
| Depreciation and amortisation | 2,167,933 | 2,167.9 |
| Net profit for the year | 2,905,085 | 2,905.1 |

Operating profit reproduces as the difference (7,338.4 − 2,167.9 = 5,170.5) and agrees with
the figure printed on the face. Nothing in the base year is annualised, scaled or solved:
FY2025 is a filed full year, and FY2026 is built forward from the reviewed first half
rather than from an annualisation of it.

The one derived figure in the historical series is FY2023 EBITDA, and it is labelled as
derived because the pre-IFRS-18 statements print no EBITDA subtotal; it is reconstructed
from audited components (revenue less operating expenses excluding D&A, less credit
losses, plus other income) and independently reproduces to 5,799.601. FY2022, added by
this review, is derived on the identical construction so the series is like-for-like.

**Nothing found.**

## MACRO COHERENCE

The dirham is hard-pegged, so the UAE imports United States monetary policy and the house
path returns a flat cost-of-capital schedule by construction of the peg. Terminal
inflation on the house path is 2.0%.

The study's escalators sit on it. The three pure-inflation lines — staff, administration
and other operating cost — each escalate at exactly 2.0%. The lines that differ each carry
a named mechanism with a measured like-for-like direction in du's own half-year pair:
mobile interconnect at −1.5% against a measured −4.1%, commission at +3.0% against a
measured +3.0%, network at +3.0%, fixed capacity and devices held flat against measured
improvements that are stopped rather than projected.

Terminal growth is 2.5% nominal against terminal inflation of 2.0% — a stated real growth
of **+0.49%**, positive and small. This is not the real-terms perpetual decline that
[L-055] names; it is its opposite, and it is coherent with the terminal discount rate.

The terminal risk-free rate the study uses, 4.30%, sits 32bp above the house-derived
terminal AED risk-free of 3.98% (2.0% terminal inflation plus the 1.9751% real-rate
convention). The difference is small and runs against the study's own answer.

The study carries no machine-readable macro record, so this coherence is established by
reading rather than by assertion, and DU remains on that ratchet.

**Nothing found.**

## DISCOUNT RATE

This is where the gap is, and it is the only place it is.

The cost of equity is 6.53% — a measured beta of 0.488 on a sourced equity risk premium of
4.29%, added to a risk-free rate normalised by the sovereign's own default spread so
country risk enters exactly once. The company has no drawn borrowings, so the weighted
cost of capital is essentially the cost of equity: 6.41% in the explicit window, 6.17% in
the terminal.

**The reverse read**, solved on the real chain through the study's own pricing harness
rather than on a re-implementation, holding every other driver at its published value:

| | beta |
|---|---|
| Measured, du's own weekly returns over five years, n=256 | **0.488** (SE 0.083, R² 0.12, 90% CI 0.352–0.624) |
| Implied by the struck price of AED 12.30 | 0.966 |
| **Implied by the latest known price of AED 11.36** | **1.079** |

The price is paying for a beta **7.1 standard errors above** the measured one, and well
outside its 90% confidence interval. In level terms 1.079 is an entirely ordinary telecom
beta and is close to this market's own median — measured across 28 UAE names through the
sanctioned regression, the cross-sectional distribution is mean 1.150, median 1.124,
standard deviation 0.499. **A reverse read landing on a believable number is evidence
against the dissent**, and it is recorded as such rather than argued away.

What was checked, and did not explain the gap:

- **Shrinking the noisy beta.** A Vasicek shrinkage toward the market-class prior is
  permitted where a beta is noisy. Applied with the prior *measured* off this market's own
  book rather than assumed, it moves the beta from 0.488 to **0.5056** — 3.6%, worth about
  half a per cent of value. The shrinkage is near-nil precisely because the estimate is
  *precise* relative to how much betas vary here: a standard error of 0.083 against a
  cross-sectional dispersion of 0.499.
- **The regressor.** DU is DFM-listed and stands on FTSE ADX General, the registered but
  labelled-interim regressor. Its own listing venue's index gives a beta of 0.4716 at a
  *tighter* R² of 0.202, and the equal-weight library composite gives 0.400. Both
  alternatives point the same way or lower. Switching would widen the gap, not close it.
- **The measurement window.** Five years, weekly, 256 observations, passing the usability
  gate. Not a short-window stopgap.

**Found: the whole gap, and it is one parameter.** The study already publishes this
judgement both ways — see the crux — and the review does not move the number toward the
price, which is prohibited outright.

## TERMINAL

The terminal carries **83.4%** of enterprise value, so any error here is most of the
answer. Two things were checked.

**Convergence.** The explicit window ends at 3.68% revenue growth against a 2.50% terminal
— a gap of 1.18 percentage points, inside the two-point requirement. The model does not
capitalise a rate it never reached.

**The construction.** The published terminal uses the reinvestment identity `rr = g/ROIC`,
which charges `g × IC` every year for ever and therefore implies a replacement cycle of
`1/g` = **40 years**. That is a fact about the inflation rate and not about the asset.

The asset life was derived by identity from du's own audited notes — gross cost excluding
capital work in progress over the year's own charge — and nothing about it was chosen:

| | gross cost (AED 000) | charge | implied life |
|---|---|---|---|
| Property, plant and equipment (note 6) | 28,616,356 | 1,542,393 | 18.55 y |
| Intangibles (note 8) | 3,500,287 | 239,907 | 14.59 y |
| Right-of-use assets (note 7) | 3,726,888 | 364,063 | 10.24 y |
| **Blended** | **35,843,531** | **2,146,363** | **16.70 y** |

The route validates itself on a disclosed figure: the right-of-use component derives 10.24
years against the **10.1-year average lease term note 7 discloses directly** — 1.4% apart.

So the terminal charges maintenance on a 40-year cycle for an asset base the company's own
accounts turn over in 16.7. Rebuilt through the sanctioned module — maintenance at
replacement cost on the derived life, book depreciation added back, growth capital charged
only for the stated real growth, inflation on working capital charged (a release here,
because working capital is negative):

| | published | rebuilt |
|---|---|---|
| Terminal value | 96,247.7 | **101,639.2** (+5.6%) |
| Enterprise value | 85,008.8 | 88,982.0 |
| Fair value per share | 18.89 | **19.80** (+4.8%) |
| Gap to AED 11.36 | +66.3% | **+74.3%** |

**The correction raises the value.** That is the opposite of what the census ratio
suggested, and it is the second name on which that has happened. The reason is exact and is
[L-289]: the two figures are not like for like. The retired construction charges `g × IC`
*net*, on an implied capital base, with maintenance assumed equal to depreciation and
cancelled out; the sanctioned one charges maintenance *gross* at replacement cost and adds
book depreciation back. Under a 2% peg the wedge between replacement cost and book
depreciation is only about 8%, so the gross-for-gross swap is nearly free while the
retired growth charge disappears entirely. **The ratio is a flag, not an inference, and
nobody may predict which way a rebuild moves a value before running it.**

**Found, and it widens the gap.** A defect was also found in what the retired construction
licensed: the study removed its explicit-window lease-replacement capex on the stated
reasoning that *"terminal reinvestment (g/ROIC) maintains it"* — a charge implying a
40-year renewal cycle against a disclosed 10.1-year lease term. The retirement's own
justification rested on the construction this rule retires. The sanctioned terminal
charges lease renewal inside the blended life, which closes it.

## BALANCE SHEET

The bridge deducts lease liabilities of AED 1,938.8mn and adds cash and term deposits of
AED 2,249.7mn — both at 31 December 2025 — while a **reviewed 30 June 2026 balance sheet
exists** and shows a materially different position:

| AED 000 | 30 Jun 2026 | 31 Dec 2025 |
|---|---|---|
| Term deposits | – | 1,784,019 |
| Cash and bank balances | 307,169 | 465,700 |
| Lease liabilities | 1,735,106 | 1,938,819 |
| Total equity | 9,967,124 | 10,148,291 |

**This is not the stale-sheet defect, and the reason is the valuation date.** The study
values at 31 December 2025, on the 31 December 2025 sheet, then accretes to the 7 August
2026 anchor at the cost of equity (1.038704 over 219 days, which annualises to 6.5335% —
exactly `ke_exp`) and deducts the AED 0.66 of dividends whose ex-dates fall in between.
That is internally coherent: sheet, valuation date and roll agree. Moving the bridge onto
the June sheet *while also* deducting those dividends would charge the same distribution
twice, which is the trap the bridge rule names in mirror image.

The term deposits did not vanish; they were spent on the royalty settlement and the final
dividend, both of which the roll already accounts for. As a sanity check on the roll, book
equity fell AED 181.2mn over the half while AED 1,813.2mn of dividends were paid — equity
before distributions rose about 16% annualised on a 6.53% roll, so the roll is conservative
against the actual outturn.

The study carries no machine-readable bridge record and remains on that ratchet.

**Nothing found.**

## CLAIMS AGAINST THE RECORD

Every absolute claim in the delivered documents was scanned for and recomputed. One was a
defect.

**"the first half of 2026 printed the best margin in the company's history"** — section
1.4. This was **typed, not computed**, and it claimed over a record the study did not
carry: the committed history ran to FY2023, three years, and the sentence claimed the
company's whole history. That is the same shape as the AMOC defect this heading exists for.

Recomputed on one construction, footed to audited and reviewed filings, with FY2022 read
out of the FY2023 statements and registered so the claim has evidence behind it:

| period | revenue (AED 000) | EBITDA | margin |
|---|---|---|---|
| FY2022 | 12,754,492 | 5,142,857 | 40.32% |
| FY2023 | 13,636,340 | 5,799,601 | 42.53% |
| FY2024 | 14,635,917 | 6,469,839 | 44.21% |
| FY2025 | 15,905,421 | 7,338,388 | 46.14% |
| H1-2025 | 7,750,295 | 3,650,187 | 47.10% |
| **H1-2026** | **8,197,573** | **4,031,922** | **49.18%** |

The claim is **true on this record**, and the four full years rise monotonically. The
sentence now computes the figure, names the window it claims over, and prints the series
behind it; the model asserts the maximum is the period the sentence names, so the claim
cannot go stale silently.

Two other claims were checked and stand: "zero drawn borrowings in every year shown"
(confirmed against all four audited balance sheets; the AED 2.0bn revolving facility signed
6 April 2026 is disclosed as undrawn and is named as the liquidity backstop), and the
sensitivity assertion that every cell of the terminal grid sits above the spot — computed
from the grid, not typed.

**Found and fixed.**

## MULTIPLE CROSS-CHECK

This is the strongest evidence against the premium in the review, and it is stated as such.

| | at the fair value of 18.89 | at the price of 11.36 | peer / own benchmark |
|---|---|---|---|
| P/E, FY2025 earnings | 29.5x | 17.7x | — |
| P/E, trailing twelve months | **27.7x** | 16.7x | **12.9x** justified, derived from Mobily's own filings |
| EV/EBITDA, trailing twelve months | **11.1x** | 6.6x | **7.56x**, du's own trailing |
| Dividend yield, FY2026E | **3.69%** | 6.13% | **4.89%** peer benchmark |

At its fair value du would trade at more than **twice** the earnings multiple the study
itself derived from the closest structural analogue's audited filings, and would yield
less than three-quarters of the peer benchmark, on a business with five-sixths of its value
in a terminal.

The two readings reconcile exactly, and the reconciliation is the finding: a 27x earnings
multiple *is* a 6.17% discount rate on a slowly growing annuity — `1/(0.0617 − 0.025)` =
27.2x. **The multiple and the discount rate are the same disagreement stated twice.**

**Found: the same single parameter, from the other side.**

---

## Verdict

The answer does not change, and the reasons are stated rather than asserted.

Six of the eight headings found nothing: the filings are all read and the most recent
period is consumed, the base year foots to the thousand, the macro path is coherent and
the terminal implies real *growth* rather than real decline, the bridge stands on a sheet
that matches its own valuation date, and the two claims that could have been wrong were
recomputed. One heading found a typed superlative, which is now computed, bounded and
true. One heading — the terminal — found a real construction defect whose correction
**widens** the gap by eight points.

The remaining two findings are the same finding: the entire disagreement is the discount
rate, and the multiple cross-check is that rate restated as a multiple. The parameter is
measured rather than chosen — five years of du's own weekly returns, 256 observations,
precisely estimated, with both alternative regressors pointing lower and a shrinkage toward
this market's own measured prior worth half a per cent.

**What a reader should weigh, and it is not resolved here.** The price is paying for a beta
of 1.08, which is this market's median and an ordinary telecom number; du's own returns say
0.49 with a standard error of 0.08. One of those is a fact about a company's measured
co-movement and the other is a fact about what a market charges. The study's own crux
already prices the closest available proxy for that disagreement both ways — hold today's
enterprise multiple into perpetuity instead of the one the measured rate implies and the
same cash flows are worth **AED 14.81** rather than 18.89, a judgement worth AED 4.08 a
share that is published side by side and never averaged. Even at 14.81 the premium to the
latest price is +30.4%.

**The number is not moved toward the price.** A fair value adjusted to meet a quote is the
reverse-engineered rate this method prohibits outright, arriving through the front door
instead of the side one. What this review changes is what a reader is told: the
disagreement is one parameter, that parameter is measured, and the multiple it implies is
far above anything this study's own peer work supports.
