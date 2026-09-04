# SCEM — GAP REVIEW, 04-09-2026  [R-GAP-01]

[R-GAP-01] AUDITED CENTRAL: 123.27 — EGP 123.27 a share.
[R-GAP-01] AUDITED GAP: +22.7 per cent against the latest known price of EGP 100.50
(close of 2026-09-02, from the price file committed at
engine/prices/SUPPLIED_03-09-2026.json).

THIS REVIEW IS ON THE OTHER SIDE OF THE PRICE FROM THE LAST ONE, AND THAT IS THE WHOLE
REASON IT HAD TO BE REWRITTEN. The 04-09-2026 review published earlier today audited a
central of 88.49 at −12.0 per cent. Nothing about the company changed since; what changed
is that this study was brought onto five construction standards it had never been held to
— the house macro path [R-MACRO-01], the cost-of-capital schedule [R-COC-01], the bridge
record [R-BRIDGE-01], the lens architecture [R-LENS-03] and the forecast anchor
[R-ANCHOR-01] — and the answer moved from 12 per cent below the market to 23 per cent
above it. A review written for a −12 per cent disagreement audits nothing at +23, which is
exactly what the AUDITED GAP marker exists to catch, and it caught this.

The trigger here is EVIDENTIAL, NOT DEFERENTIAL, and it fires in both directions since
02-Sep-2026. A large gap either way is a high-prior-of-defect region and the price is the
only instrument in the room that measures it. The question below is not whether the market
is right. It is whether WE made a mistake, and this time the mistake would have to be an
OPTIMISTIC one.

WHAT MOVED THE ANSWER, MEASURED RATHER THAN ASSERTED
  88.49  the previous edition, on the retired four-lens blend
  +9.3%  the house inflation ladder: this study carried 14.0/11.0/7.9/6.2/5.5 per cent
         against a house 16.0/12.0/9.0/7.5/7.0, and a terminal growth of 5 per cent
         against a terminal risk-free rate built on 7 — a perpetual real decline of two
         points that nothing disclosed
  +2.9%  the discount factors: the study compounded its forward rates in whole-year steps
         from t=0, so the entire 0.917 years to the FY2027 midpoint was discounted at the
         FY2026 rate and the FY2030 rate never entered any factor at all. On a path that
         FALLS, that over-discounts every year after the first
  −1.1%  the cost of debt: 21.50 per cent sat 81 basis points BELOW the sovereign that
         taxes this company, which [R-COC-01] refuses outright. Now derived as the house
         sovereign plus a stated 200 basis point corporate spread
  −3.7%  the capital charge: see BASE YEAR below — this one runs AGAINST the value and is
         the largest thing this review found
  the blend retired: the published answer is now the cash-flow lens alone at 123.27,
         where the retired 48/21/23/8 blend would read 95.96

Everything above is arithmetic on this study's own committed record. The net effect is
that the answer rose, and the eight headings below are the audit of it.

---

## 1. LATEST FILINGS

Every disclosed period is read and consumed. THE MOST RECENT IS THE REVIEWED CONDENSED
INTERIM FINANCIAL STATEMENTS FOR THE THREE MONTHS ENDED 31 MARCH 2026, downloaded from the
company's own website and read by OCR off the rendered pixels because the file carries a
37-byte text layer across 37 pages. Every statement in it foots against its own arithmetic
and the footings are asserted in filings_extract.py, not eyeballed.

Consumed, with what each supplies:
  * FY2025 audited statements — revenue, the cost lines of notes 24/25/26, note 4's
    fixed-asset schedule, note 3/2's disclosed depreciation rates, note 27's earnings per
    share working, the statement of changes in equity.
  * FY2024 audited statements — the comparative year and the disposal gain stated on the
    face of the income statement.
  * The reviewed quarter to 31 March 2026 — the balance sheet the bridge stands on, and
    the quarter's own profit of EGP 1,114.5mn.

NOTHING IS OUTSTANDING. There is no half-year statement between 31 March 2026 and the
valuation date; the company's next disclosure is the half to 30 June 2026 and it had not
been filed. THIS IS THE HEADING THAT PRODUCED THE LARGEST FINDING OF THE WHOLE REBUILD,
and it did so a day before this edition: the prior study built its historicals from Global
Cement, cemnet, Daily News Egypt, Arab Finance and an aggregator's carry of S&P Global
Market Intelligence WHILE THESE STATEMENTS SAT ON THE COMPANY'S OWN WEBSITE, six PDFs one
click from the homepage. Filed equity was EGP 6,020.3mn against 5,240.0mn used, cash
4,762.3mn against 3,850.0mn, FY2025 depreciation 122.6mn against 418.1mn, operating profit
3,304.1mn against an EBIT of 2,640.0mn — EVERY ONE UNDERSTATING THE COMPANY. That is where
most of the distance between this answer and the old one comes from, and it is a defect of
the *we did not read the filings* kind rather than the *the company did better than we
thought* kind.

## 2. BASE YEAR

The base year foots to the filed periods. FY2025 revenue of EGP 9,089.1mn, EBITDA of
3,455.2mn (38.01 per cent), depreciation of 122.6mn and operating profit of 3,304.1mn are
the audited figures, not a solve. The bottom-up physical model reproduces that revenue to
+0.10 per cent and that EBITDA to +0.26 per cent from tonnes and prices, which is the test
that the driver structure is right rather than merely calibrated.

NOTHING IS ANNUALISED OR SCALED. FY2026 is stubbed to the five months of the year still
unearned at the valuation date and the seven already earned are rolled into opening cash,
so the period between the 31 March balance sheet and the valuation date is counted exactly
once.

**THE ONE THING THIS HEADING FOUND, AND IT RUNS AGAINST THE VALUE.** The explicit window
charged capital spending of EGP 352mn rising to 494mn — the company's own three-year
average of 303.2mn, escalated. The terminal charges maintenance at CURRENT COST on the
disclosed life, which is EGP 959mn a year in today's money. The two differ by 3.2x,
and the reason is not that the plant is young: note 4 shows accumulated depreciation of
EGP 1,875.0mn against a gross cost of 3,140.9mn — 59.7 per cent written down, MACHINERY
68.4 PER CENT — with EGP 379.4mn of assets fully depreciated AND STILL IN USE. Replacement
cost is 7.9x the book cost this plant was built at, because it was built in
pre-devaluation pounds.

Holding that spend flat for five years while simultaneously running the kilns HARDER, from
71.0 per cent of clinker capacity to 79.1, is two assumptions that cannot both be true. The
charge now GLIDES from the company's own disclosed run rate to the terminal's own
current-cost maintenance by FY2030, so the step at the boundary is zero by construction.
It costs EGP 4.73 a share, and it is the correction this review was written to
find.

## 3. MACRO COHERENCE

Inflation, currency and price are ONE path, and none of them is this study's own any more.
The domestic cost index, the domestic realised price and the pound are all derived from the
house EG macro path [R-MACRO-01]: the ladder is 16.0 / 12.0 / 9.0 / 7.5 / 7.0 per cent for
2026-2030, sourced to the Central Bank of Egypt's baseline and its published glide, and the
currency path is relative purchasing-power parity ON THAT LADDER against long-run United
States inflation, read from the path file rather than computed here.

The previous edition derived the same identity from its OWN ladder, two points a year
below the house one, so the pound slid more slowly than the house says it does. Conforming
raises nominal cash flows and RAISES the answer 9.3 per cent — which is worth stating
plainly because it is the direction that invites suspicion. It is not fitting: the house
ladder is the same one every Egyptian study in this book now carries, it was sourced before
this study was touched, and AMOC's own conformance the day before moved its answer the
opposite way, DOWNWARD, for the same reason (a lower ladder means a stronger pound, and on
a dollar-linked slate the translation gain lost outweighs the pound costs saved).

The export price is US-dollar denominated and declines on the European carbon border
mechanism; it carries a stated exemption from the ladder because Egyptian inflation does
not set it. Egyptian inflation reaches it through the currency path, which is where it
belongs.

Terminal growth is now 7.0 per cent — the house terminal inflation at a STATED real growth
of ZERO — against a terminal risk-free rate of 12.5 per cent built on that same 7. The
previous edition held 5 per cent against the same 12.5, a perpetual real decline of about
two points a year that nothing in the study disclosed. assert_macro_coherence() reproduces
every one of these from the path.

## 4. DISCOUNT RATE

Operations are discounted at a rate weighted on GROSS debt, and the cash is added at face
exactly ONCE. This company is heavily net cash; a net-debt weighting would drive the debt
weight negative, lever the equity weight above one, put the operating rate ABOVE the cost
of equity, and then add the same cash back in the bridge. That is the double charge
[R-BRIDGE-01] names and it is not made here.

The schedule is 28.96 per cent in the explicit window gliding to 18.98 per cent
in the terminal, and THE GLIDE'S FRACTIONS ARE THE CENTRAL BANK'S OWN EASING CALENDAR — the
policy path's cumulative progress from 19.0 per cent to 12.0 — rather than a shape anybody
typed. The terminal beta is re-levered by Hamada from an ASSET beta, unlevered at the
observed structure first; the previous edition levered an already-levered beta.

Country risk enters ONCE: the risk-free rate is normalised by Egypt's own CDS-implied
default spread and the premium adds the same basis back. Both premium bases are published
and the CDS basis is named central. TWO THINGS THIS HEADING FOUND, both corrected above:
the cost of debt sat below the sovereign, and the discount factors did not reproduce from
the forward path.

The reverse read is the honest summary of this heading. At EGP 100.50 the price is paying
for a flat 24.47 per cent cost of capital on these same cash flows; this study's schedule
is equivalent to a flat 20.43 per cent. FOUR HUNDRED BASIS POINTS ON THE PRICE OF TIME IS
MOST OF THE DISAGREEMENT, and it is a legible one: the market is saying Egypt's cost of
capital does not normalise as fast as the central bank's own published path assumes. A
reader who believes that lands close to the market.

## 5. TERMINAL

The terminal is built by the sanctioned module on a DISCLOSED asset life [R-TERM-01], not
on the reciprocal of the inflation rate. Note 3/2 states 2-2.5 per cent on buildings and
utilities, 5 per cent on machinery, 20 per cent on vehicles and tools and 10-25 per cent on
furniture; weighted on note 4's own gross-cost mix that is a 25.9-year life, and it
reproduces the filed FY2025 charge to within 1.2 per cent. The FY2024 filing carries the
identical table.

Terminal growth is coherent with the inflation inside the terminal rate (heading 3).
Terminal free cash flow is EGP 4297mn, positive, and the terminal sits ABOVE the
NOPAT-perpetuity floor. The implied replacement cycle is not 1/g and an assertion in the
study refuses it if it ever becomes so.

**THE TERMINAL IS 66.5 PER CENT OF ENTERPRISE VALUE AND THAT IS THE STRUCTURAL WEAK
POINT OF THIS ANSWER.** It is not a defect — a five-year window on a business whose growth
converges to the terminal rate exactly, discounted at a rate falling from 29 to 19 per
cent, will put most of its value late — but it means the answer is more sensitive to the
terminal construction than to anything in the explicit window, and the contested-judgement
record prices exactly that: moving to the 20-year machinery life alone is worth
5.1 per cent.

## 6. BALANCE SHEET

The bridge stands on the LATEST disclosed balance sheet, the reviewed statement at 31 March
2026 — cash of EGP 5,802.0mn and interest-bearing debt of EGP 152.7mn, both filed. The four
months from that date to the valuation date are carried on the model's own free cash flow.
Non-controlling interests are deducted from EQUITY value at the value-share basis, with the
book, profit-share and proportional framings published beside it; at EGP 120mn against an
equity value above EGP 33bn the three cannot differ by anything reaching the second decimal
of a per-share number, and that is stated rather than used as a shortcut.

No dividend is deducted, and the reason is arithmetic rather than assumption: the filed
statements of changes in equity show NO distribution at all, twice over and to the pound.
Equity of EGP 3,735.80mn at 31-Dec-2024 plus FY2025 profit of 2,284.54mn is exactly the
filed 6,020.34mn, and that plus the reviewed quarter's 1,114.48mn is exactly the filed
7,134.82mn. A 60 per cent payout had been assumed against a company whose own statements
reconcile with none.

NET CASH IS EGP 25.13 A SHARE, 20.4 PER CENT OF THE ANSWER. A reader who thinks this
study is optimistic should note that a fifth of it is a filed bank balance.

## 7. CLAIMS AGAINST THE RECORD

Every "best ever" and "never" is recomputed against the filings rather than typed. What
this heading finds is not a false claim but an UNMADE one, and it is the most important
sentence in this review:

**THE FORECAST OPENS ABOVE EVERY YEAR THE COMPANY HAS EVER FILED AND RISES FROM THERE.**
Sinai Cement filed EBITDA margins of 6.62 per cent (FY2023), 24.66 (FY2024) and 38.01
(FY2025). The forecast opens at 38.63 per cent — above the best of them — and reaches
39.83 by FY2030. [R-ANCHOR-01] does not fire on a forecast above the latest period, and
the record is printed anyway so the shape is visible rather than merely not-red.

The mechanism is operating leverage and it is an OUTPUT rather than an assumption: kiln
utilisation runs from 71.7 per cent of clinker capacity to 79.1 against a fixed cash cost
that escalates only with the house ladder. THE RAMP IS AN EXTRAPOLATION OF THE COMPANY'S
OWN THREE-YEAR TREND — filed utilisation ran 53.2 / 62.7 / 71.0 per cent across FY2023-25
— AND IT IS AN EXTRAPOLATION AND NOT A DISCLOSURE, with roughly 12.6Mt of dormant Egyptian
capacity queuing to restart against it. It is the single largest judgement in the study,
worth 11.4 per cent of value, and it is the first thing a reader should contest.
Holding utilisation flat at the filed FY2025 rate takes the answer to EGP 109.19, which
is +8.6 per cent from the price.

## 8. MULTIPLE CROSS-CHECK

At the fair value the shares imply 7.44x FY2025 EBITDA and 6.31x this study's FY2026
forecast; at the traded price, 5.72x and 4.85x. On earnings, 14.1x FY2025 and
8.6x FY2026 against 11.5x and 7.0x at the price.

NONE OF THOSE IS ABSURD, IN EITHER DIRECTION. An integrated cement plant trading at 5.7x
trailing EBITDA and valued at 7.4x is a disagreement inside the ordinary range for the
asset class, not a claim that requires the market to be broken. That is worth saying
explicitly, because a multiple cross-check whose only function is to confirm the answer is
not a cross-check: here it neither refutes the study nor rescues it, and the disagreement
has to be settled on the drivers rather than on the multiple.

The other lenses are published beside the cash-flow lens rather than averaged into it
[R-LENS-03]: replacement cost 94.23, the relative multiple 62.11 at a house 4.2x on
normalised EBITDA, and the disclosed book floor of 27.12. The relative lens is the one that
disagrees most and it is the weakest of them — the Egyptian listed peer set is two names
and neither publishes an EBITDA series this study could measure a multiple from, which is
recorded rather than papered over.

---

## VERDICT

The answer is NOT changed to meet the price, and one correction this review produced moves
it further away from the market rather than toward it while another moves it closer; both
were taken on their own evidence.

The gap is +22.7 per cent and it is now READABLE rather than merely large. Four hundred
basis points of it is a disagreement about Egypt's cost of capital, measured by the reverse
read. Most of the rest is one physical judgement — the utilisation ramp — which is stated,
priced at 11.4 per cent, and left as the reader's to contest.

WHAT WOULD CHANGE OUR MIND, IN ADVANCE: a half-year to 30 June 2026 showing utilisation
flat or falling against the 71.0 per cent of FY2025, or an EBITDA margin below the FY2025
outturn. Either would refute the ramp directly, and the study prices what happens if they
do.

THE STUDY IS HELD, NOT PUBLISHED [R-GAP-02]: at +22.7 per cent it is past the 10 per cent
publication limit and no market-dissent document is filed. Holding is the correct outcome
of an audit that found one real correction and left a large disagreement standing on a
stated judgement.
