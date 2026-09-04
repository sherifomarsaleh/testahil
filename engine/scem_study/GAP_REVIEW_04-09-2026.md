# SCEM — gap review, 4 September 2026

[R-GAP-01] AUDITED CENTRAL: 88.4852 — EGP 88.49 a share.
AUDITED GAP: -12.0% against the latest known price of EGP 100.50 (2 September 2026), from
the price file the principal supplied on 3 September and committed at
`engine/prices/SUPPLIED_03-09-2026.json`.

The rule fires because the central sits more than ten per cent from the price. It does not
say the answer must change. What it says is that a large disagreement is a high-prior-of-
defect region and the price is the only instrument in the room that measures it — so the
answer is audited before it ships. This review is what that audit found, and it found a
great deal, because the study it audits had never opened the company's own filings.

**Where the answer moved, and why none of it is a move toward the price.** The central was
EGP 53.12 when this pass began and −32.8% against the price it was then struck at. It is
now 88.49. Every step is sourced to the audited statements or to a standing rule, and the
test [R-GAP-01] sets is whether the same correction would have been made at a different
price. It would: the cost stack was 6.3% above the company's own disclosed cost, the
depreciation charge more than three times the filed one, the forecast's opening margin
eight points below the latest audited year with a mechanism the filings contradict, and
the terminal built on the reciprocal of an inflation rate. One correction in this review
moves the answer AWAY from the price by 1.2% and it was made anyway.

---

## 1. LATEST FILINGS — every disclosed period actually read

**Clean, and it was not before.** The first edition of this study took its revenue, profit
and balance-sheet figures from Global Cement, cemnet, Daily News Egypt, Arab Finance and an
aggregator's carry of S&P Global Market Intelligence — a plain breach of SIGCM clause 1,
which has forbidden exactly that since July 2026. The audited statements were on the
company's own website the whole time: `sinaicement.com` carries them as direct PDF links
from its homepage, no authentication and no investor-relations portal to navigate.

Read this pass, in full, by OCR off the rendered pixels (the filings carry a 37-byte text
layer across 37 pages, so no extraction is possible):

| document | period | kind | route |
|---|---|---|---|
| SCC-AFS-E-1225.pdf | year ended 31 December 2025 | audited | OCR, arithmetic-verified |
| SCC-AFS-E-1224.pdf | year ended 31 December 2024 | audited | OCR, arithmetic-verified |
| SCC-AFS-E-0326.pdf | three months to 31 March 2026 | reviewed | OCR, arithmetic-verified |

**The most recent disclosed period is the reviewed quarter to 31 March 2026.** Nothing
newer is published: the site's own media listing returns the FY2025 and Q1-2026 statements,
English and Arabic, all dated 9 June 2026 as the newest financial documents, and direct
probes for a 30-June interim under the naming convention the company uses return 404. The
probe was re-run rather than remembered, per [R-IND-01].

`filings_extract.py` commits every figure with its statement, printed page and route, and
asserts every footing the filings themselves perform. **Two of those assertions fired and
both were right to.** Note 24's FY2024 column summed ten short of its printed total —
re-rendered at 220 dpi, wages are 69,084,467 and I had read 69,084,457, a single digit
located in a column of nineteen. And FY2025 profit over the footed closing share count
gives EPS 8.76 against a printed 10.29, which is not a misread but the capital increase
registered on 22 April 2025; note 27 states its own weighted-average working and it
reproduces to the cent.

## 2. BASE YEAR — foots to the filed periods, nothing annualised or solved

**Clean, and it was not before.** The base year is FY2025 exactly as filed: revenue EGP
9,089.15mn, operating profit 3,304.13mn, depreciation and amortisation 122.56mn, EBITDA
3,455.21mn at a 38.01% margin, profit after tax 2,284.54mn.

The first edition **solved** its operating profit rather than reading it: it grossed a
press profit figure at an effective tax rate and subtracted a treasury income estimated on
a cash balance rolled back by a guessed factor of 1.25, reaching an EBITDA of 3,058mn at
33.6%. It also charged depreciation at 4.6% of revenue — EGP 418mn against a company that
filed 122.6mn.

The bottom-up volume-and-price build backcasts FY2025 revenue within **+0.02%** of the
filed figure and FY2025 EBITDA within **+0.06%**. That second number is the one that
matters: the first edition's stack agreed with its own closure to 1.36% **while being EGP
355mn out**, because both sides came from the same press figures. A check whose two sides
share a source cannot fail.

## 3. MACRO COHERENCE — inflation, currency and price on one path

**One defect found and corrected; one incoherence measured and left, with its reason.**

*The currency was hand-set.* The path slid the pound 5.4% in FY2026 while the same model
escalated domestic costs 14.0% — one event counted once and ignored once, which is [L-048].
It is now derived on relative purchasing-power parity against 2.5% foreign inflation from
this study's own cost path, as [R-MACRO-01] requires. **Correcting it LOWERS the answer by
1.2%**, because a faster slide costs more on the dollar-linked materials line than it earns
translating export revenue. That is the AMOC precedent exactly, and it is the evidence that
conforming to the rule is not fitting to the price.

*The realised price was falling in real terms with nothing behind it.* The old path grew
domestic price 4.5–6.0% a year against costs rising 14.0%, 11.0%, 7.9%, 6.2% and 5.5%. The
input register described it in its own words as "a REAL decline against CBE inflation" and
sourced no mechanism. **It was worth 23% of the answer.** See heading 5 for why it was
refused rather than argued about.

*The terminal inflation is the study's own 5%, not the house path's 7%.* Within this
study's ladder it is coherent — the cost path decelerates to 5.5% by FY2030 and 5% is the
step beyond it — and raising the terminal alone without the ladder would create the
incoherence [R-MACRO-01] forbids in the other direction. Conforming the whole ladder is
worth **+3.9%** and is this study's standing entry on the macro ratchet; it is a separate
pass, and it is recorded here rather than done by halves.

## 4. DISCOUNT RATE — the operations at the right rate, the cash charged exactly once

**Clean.** The explicit window discounts at 28.26% gliding to a terminal 19.01%. The debt
weight is **0.52%** — gross lease liabilities against market capitalisation, not net debt —
so the equity weight is 99.5% and never levers above one. This is the case [R-BRIDGE-01]
calls defect (iii): a net-cash company discounted at a net-debt-weighted rate drives the
debt weight negative and the operating rate above the cost of equity, and then adds the
same cash back at face. **This study does not do it.** The cash is added at face, once, in
the bridge, and the operations carry no credit for it.

## 5. TERMINAL — growth coherent with the inflation inside the terminal rate

**The largest correction in this pass, and it is arithmetic rather than judgement.**

The first edition built its terminal on the reinvestment identity `rr = g/ROIC`, which
substitutes to a charge of `g × invested capital` every year for ever. Read as a capital
maintenance programme the implied replacement cycle is `1/g` — **20.0 years at a 5%
terminal rate, which is a fact about the currency and not about the plant.** The terminal
it produced sat **34% below the value of not investing at all**, the worst case in this
house's book.

It is now built by `engine/terminal_value.py` on the **disclosed** life. Note 3/2 of the
audited accounts gives the rates — buildings and utilities 2–2.5%, machinery 5%, motor
vehicles and tools 20%, furniture 10–25% — and weighted on note 4's own gross-cost mix that
is a **25.9-year** life. It reproduces the filed FY2025 depreciation charge to within 1.2%,
which is what makes it a sourced rule rather than a house guess, and the FY2024 filing
carries the identical table. Maintenance at current cost is EGP 950mn a year, 24.7% of
terminal profit, and the terminal free cash flow of 3,848mn sits above its floor.

**A second, independent error rode with it.** The explicit window ran on NOPAT less a
reinvestment charge derived from the growth in NOPAT while the terminal ran on something
else — one model, two definitions of free cash flow, with the terminal holding 57% of
enterprise value. The driver test measured what that cost: raising capital spending by EGP
100mn a year moved the value by **0.12%**. Both windows now run the same waterfall.

**And the forecast's own margin path was refused on the company's measurement.** The old
forecast opened at a 30.1% EBITDA margin against a filed FY2025 of 38.0% — 20.8% below in
relative terms, four times [R-ANCHOR-01]'s trigger — and the mechanism it would have needed
is `input_cost_outpacing_price`. That rule demands the mechanism be **measured
like-for-like in the company's own period pair**, and here it runs the other way: cost per
unit of revenue is 67.91% in Q1-2025, 61.99% in the audited FY2025 and **58.93% in the
reviewed Q1-2026**. Falling, where the forecast needed it to rise. A mechanism contradicted
by the filings is the assumption wearing one. The forecast now holds the real spread per
tonne flat and opens at 38.2%, one fifth of a point above the year the company filed.

The 12.6Mt of dormant Egyptian capacity queuing to restart is a real risk to price. It
belongs in the bear case and the sensitivity grid, which carry it, and not in the base path
as an unsourced assumption.

## 6. BALANCE SHEET — the bridge stands on the latest disclosed sheet

**Corrected.** The bridge stood on the audited 31 December 2025 sheet rolled forward on an
estimate. It stands on the **reviewed 31 March 2026 statement of financial position**:
cash on hand and at banks EGP 5,801.98mn, lease liabilities of 137.62mn long-term and
15.09mn current, and **no bank borrowings at either date** — the whole of the company's
interest-bearing debt is leases under EAS 49. The four months from that sheet to the
valuation date are carried on this model's own free cash flow, so the period between the
two dates is counted once and only once.

Net cash at the valuation date is **EGP 6,533.0mn, 24.9% of market capitalisation**.

## 7. CLAIMS AGAINST THE RECORD — every absolute claim recomputed

Five claims were scanned and recomputed. Two were wrong.

**"Net cash worth 37% of its market capitalisation"** was typed and stale; it recomputes to
24.9% at the current price and is now rendered from the model.

**"The company has no dividend on record, yet the balance sheet arithmetic implies a
substantial FY2025 distribution. A declared payout would resolve the largest single
uncertainty in the equity bridge."** The second half is false, and the filed statements
settle it twice over, to the pound:

| | EGP mn |
|---|---|
| Total equity, 31 December 2024 | 3,735.80 |
| plus FY2025 profit after tax | 2,284.54 |
| = | **6,020.34** — the filed 31 December 2025 equity, exactly |
| plus the reviewed quarter's profit | 1,114.48 |
| = | **7,134.82** — the filed 31 March 2026 equity, exactly |

**Nothing has been distributed.** The study was reading a distribution out of arithmetic it
had not taken from the statements, and calling the result its largest uncertainty. The
model's 60% payout assumption is corrected to the filed nil. It changes no valuation number
— free cash flow to the firm is struck before financing — and it changes the projected
balance sheet a reader is shown.

The other three claims stand: the industry's best year since 2008, the policy rate and
ten-year yield, and the 29.3% unchanged-close share, which is computed from the price
library.

## 8. MULTIPLE CROSS-CHECK — what the fair value implies

| on FY2026E | at the fair value 88.49 | at the market 100.50 |
|---|---|---|
| enterprise value (EGP mn) | 16,545 | 19,679 |
| EV / EBITDA | **4.17x** | 4.96x |
| price / earnings | **6.29x** | 7.14x |

| on FY2025 as filed | at the fair value | at the market |
|---|---|---|
| EV / EBITDA | **4.79x** | 5.70x |
| price / earnings | **10.10x** | 11.47x |

The only named Egyptian comparator, Misr Beni Suef, is quoted at **5.03x** EV/EBITDA. This
study's own justified multiple for the relative lens is **4.2x**, below the peer, and the
cash-flow lens implies 4.17x on FY2026 earnings — so the answer is a discount to the one
disclosed peer on the one multiple both can be measured on.

**That is the reading this heading is for, and it is not comfortable.** Three of the four
lenses (relative 62.02, normalised 70.39, asset 93.52) sit below the cash-flow lens at
107.89, and the weighted central of 88.49 is dragged down by two lenses whose own inputs
are weaker than the cash-flow model's: the relative lens applies a multiple this study
chose below the peer's quoted one, and the normalised lens capitalises a mid-cycle margin
struck between FY2024 and FY2025 — a pair that now looks conservative against a reviewed
quarter running at 54.6% gross margin. Under [R-LENS-03] the class primary would BE the
central and the others cross-checks beside it; this study still publishes a typed four-lens
blend, which is its standing entry on the lens ratchet and the largest remaining structural
item against it.

---

## What this review did not do

It did not move any number toward the price, and the −1.2% currency correction is the
evidence. It did not conform the macro ladder to the house path (+3.9%), because doing half
of that would create an incoherence rather than remove one. It did not retire the four-lens
blend for the same reason: [R-LENS-03] is an architecture change and this study carries it
on the ratchet.

The gap of −12.0% therefore stands as the honest output of a study that now reads the
company's own statements. It is past [R-GAP-02]'s publication limit and the study is
**HELD**. Publishing it would need a market-dissent filing, and on this evidence the
dissent would be hard to write: the two open items above both move the answer toward the
price, which is a reason to finish them rather than to argue with the market.
