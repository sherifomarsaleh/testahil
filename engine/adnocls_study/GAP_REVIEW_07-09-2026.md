# ADNOCLS — GAP REVIEW, 07-09-2026  [R-GAP-01]

[R-GAP-01] AUDITED CENTRAL: 5.34 — AED 5.34 a share.
[R-GAP-01] AUDITED GAP: -21.5 per cent against the latest known price of AED 6.80
(close of 2026-09-07, from the price file committed at engine/prices/SUPPLIED_07-09-2026.json).
This study is now STRUCK at that price, so the strike gap and the delivered gap are the
same number and there is no second figure to reconcile.

**WHY THIS REVIEW EXISTS, AND IT IS NOT THE USUAL REASON.** The edition delivered earlier
on 7 September 2026 carried its own review (`GAP_REVIEW_04-09-2026.md`) at -18.2 per cent,
and that review names the thing this one is about, in its own words: *"This review is
written on 4 September 2026 and the half-year to 30 June 2026 would normally have been
filed by mid-August. This study holds no such document."* It did exist. It had been public
for twenty-seven days. **The rule is that every disclosed quarter is swept in BEFORE the
build starts, and it was not** — the previous review registered the gap as an open item
and the edition shipped anyway. Four documents are now read, footed and consumed, the
answer has moved from 5.6054 to 5.3385 by way of 6.6100, and the route is in
`rebuild_ledger.json`.

**THIS IS THE EXEMPLAR.** Every study written afterwards is built by opening this one
beside it, so a defect here is a debt every later study inherits without anybody deciding
to take it on. That is why the audit is written in full and why the miss is recorded as
the finding it is rather than as a footnote.

---

## 1. LATEST FILINGS

**Every disclosed period is now read and consumed.** The most recent is the CONDENSED
CONSOLIDATED INTERIM FINANCIAL INFORMATION FOR THE SIX MONTHS ENDED 30 JUNE 2026, with a
PricewaterhouseCoopers review report signed 10 August 2026. Beside it: the management
discussion and analysis for the first half, the first-half earnings release and the
first-half earnings presentation, all dated 11 August 2026. The valuation date IS that
balance-sheet date, so no roll-forward stands between the bridge and a filing.

Consumed before them and still consumed: the audited statements for FY2022 through FY2025,
the FY2025 annual report and results release, the FY2025 and Q1-2026 management discussion,
the investor presentations of FY2025 and April 2026, the FY2025 and Q1-2026 earnings calls,
and the reviewed 31 March 2026 quarter — which is retained rather than discarded, because
the second quarter is read as the difference between it and the half.

**EVERY FIGURE THE MODEL CONSUMES COMES FROM THE STATEMENTS, NOT THE COMMENTARY, AND THE
DIFFERENCE IS NOT COSMETIC.** The management discussion re-presents the first three
quarters of 2025 Tankers revenue and direct costs "for analytical consistency, with no
impact on Gross Profit, Net Profit or EBITDA". Its prior-year half-year revenue is
therefore USD 2,507 million against the reviewed statements' USD 2,438.936 million — a
difference of 68.104 million appearing identically on both revenue and direct cost, so
every margin and every profit line is the same on both bases. The basis break is registered
in the sweep and the model runs on the statements.

**Arithmetic is the arbiter, and it was applied.** Twelve footing assertions run in
`compute.py` on this half alone: the balance sheet foots; equity foots to its three
components; the income statement foots from revenue to operating profit and from operating
profit to profit for the period; the segment note foots to group revenue, group direct
costs and group earnings; the company's stated earnings measure reproduces from its own
stated definition (profit before tax 1,199,874 plus finance costs 18,636 less finance
income 5,763 plus depreciation and amortisation 262,121 = 1,474,868); and the published net
debt of 257,318 REPRODUCES only when loans and other borrowings are included, which the
stated definition omits — so it is footed rather than taken.

**Nothing is outstanding.** The one open item the previous review named is closed by this
pass. The next disclosure is the third quarter, not yet released at the date of this review.

## 2. BASE YEAR

**The base is no longer a base year. It is a reported half plus a built half, unit by
unit.** FY2026 revenue of USD 6,981.778 million is the reviewed USD 3,666.674 million the
company filed plus USD 3,315.104 million this model builds; FY2026 earnings of USD 2,716.145
million is the filed USD 1,474.868 million plus USD 1,241.277 million built. **No period the
company has already reported is replaced by a forecast of it.**

Nothing is annualised into the answer. FY2026 is discounted over the 0.50 of the year still
unearned at the 30 June valuation date, and the half's own free cash flow of USD 598.095
million — on the company's own stated definition, footed as 1,474,868 less 302,614 of
working capital less 26,942 of income tax expense less 547,217 of capital expenditure — is
removed from FY2026 free cash flow rather than discounted a second time, because it is
already inside the balance-sheet net debt.

**Three quantities are SOLVED rather than sourced, and all three are labelled as solved
wherever they appear.** The tanker cost stack is two of them — a fixed base of USD 529.987
million a year and a variable component of 1.0486 per unit of the owned fleet's
charter-equivalent revenue — solved from the audited 2025 year and the reviewed 2026 half
TOGETHER, with the reviewed 2025 half HELD OUT and reproduced to within 10.7 per cent,
understating it. The third is the gas carrier day rate, solved on 2025 and NOT re-solved on
the half, because the same solve on the half gives USD 108,536 against USD 61,573 for a
reason that is a MIX rather than a rate: the denominator counts CONTRACTED vessels while
the numerator is the whole unit's revenue.

## 3. MACRO COHERENCE

Inflation, currency and price are ONE path and none of them is this study's own. The
running-cost escalator is the house AE ladder year by year — 2.5 per cent in 2026 and 2.0
thereafter — and the terminal risk-free rate of 3.975 per cent is DERIVED from it rather
than typed. `assert_macro_coherence()` runs over the committed `inflation_inputs` block,
which declares every inflation-class input this model registers with the mapping that
derives it from the house ladder.

There is no currency path, and that is a construction rather than an omission: the dirham
is hard-pegged at 3.6725, so the house path returns a FLAT currency path by construction of
the peg. Charter rates carry a STATED exemption from the ladder — they are US-dollar day
rates set in a global freight market, and under a peg there is not even a currency path for
domestic inflation to arrive through.

**The rate path is not a macro assumption at all in 2026, and that is new.** Two of its four
quarters are REPORTED and the third is DISCLOSED to 11 August on the share of vessel days
already contracted. Only the fourth quarter and the years after it are this study's own,
and they revert on a weight of 0.50 that is unchanged from the previous edition — the
parameter did not move, only the quarter it reverts from.

## 4. DISCOUNT RATE

The operations are discounted at a rate weighted on the GROSS capital structure — ordinary
equity 83.14 per cent at 9.433 per cent, drawn debt 4.86 per cent at 6.349 per cent before
tax, and the perpetual capital securities 12.01 per cent at their own disclosed coupon —
giving 8.711 per cent in the explicit window and 8.676 per cent in the terminal. **The cash
is charged for exactly once**: the weights are GROSS, nothing is added back at face, and
`bridge_record.cash.treatment` is `none` with `weights_basis` `gross`.

**The de-levering is why moving the bridge onto the June sheet LOWERED the answer**, and it
is worth naming because the direction is the opposite of the obvious reading. Drawn debt
falls from USD 1,115.212 million at 31 March to USD 800.000 million at 30 June, so the
equity weight rises and the blended rate rises with it — by more than the USD 162.549
million of net-debt reduction is worth on a company this lightly levered. The correction
moved the answer AWAY from the price and was kept.

Country risk enters once. The cost of debt sits above the local sovereign yield, as a
corporate borrowing in its sovereign's own currency must. `assert_ke_reproduction()`
reproduces both the explicit and the terminal cost of equity from `rf* + beta x ERP` under
a NAMED construction.

## 5. TERMINAL

**The terminal is on the RETIRED reinvestment identity and it is listed on that rule's
ratchet.** It was re-tested against the new filings in this pass and the sanctioned build
still REFUSES — at an implied payout of 140.1 per cent of terminal profit, against 117 per
cent when it was last tested on 4 September. The full re-test is in
`TERMINAL_EVIDENCE_05-09-2026.md`; in short, all three routes that would open it were
re-tried against the half-year documents and none does. The interim's property, plant and
equipment note is a single-column roll-forward with no class split and no lives; the words
*residual*, *scrap*, *salvage*, *useful li* and *dry-dock* appear in none of the four new
documents; and the fleet-age slide has improved — the LNG row's age is now filled at 15
years where the April deck printed a placeholder — without becoming usable, because it is
counts and ages rather than carrying amounts.

Terminal growth is 2.0 per cent against a terminal discount rate embedding a 2.0 per cent
terminal inflation, so REAL growth is zero and is stated as zero. There is no perpetual
real decline here and no perpetual real growth either.

**WHICH WAY THE RETIRED CONSTRUCTION BITES IS NOT ASSUMED.** [R-TERM-01 CLAUSE TWO
CORRECTED] is explicit that the under-charging ratio is a FLAG and not an inference: the
charge of g x IC is 221.752 million against book depreciation of 746.550 million, a ratio
of 0.30, which flags this terminal as worth rebuilding and says NOTHING about which way a
rebuild would move it. It is not rebuilt because the life cannot be sourced, and no
direction is claimed for it in either the study or this review.

The terminal carries 62.4 per cent of enterprise value. That is high and it is disclosed.

## 6. BALANCE SHEET

**The bridge stands on the LATEST disclosed balance sheet, which is 30 June 2026.** It did
not before this pass — it stood on 31 March — and that is one of the nine levers.

Every line is re-read at that date: net debt 257.318 million (footed, see heading 1),
deferred consideration 304.297 million, the perpetual securities 1,978.619 million,
non-controlling interests 289.197 million, joint ventures at 522.768 million, cash 542.682
million, intangibles 16.192 million, goodwill 51.368 million, ordinary equity 5,883.066
million, and working capital of 718.017 million DERIVED on the same construction as every
historical year.

The minority is deducted from EQUITY value and never from enterprise value, in two parts:
the 20 per cent of the acquired tanker business that is CONTRACTED for purchase is deducted
at its contracted price, because its present value is already in the bridge as deferred
consideration; the remainder is lifted from book to its share of value. **The bridge FOOTS**
— asserted in the document builder, in the workbook and in `bridge_record` — and divides to
the stated per share.

**One line is new and it is a [R-BRIDGE-01] clause working.** The board approved an interim
cash dividend of USD 85.3 million for the second quarter on a record date of 20 August 2026
— DECLARED AFTER the sheet this bridge stands on and with its record date already past at
the price this study is delivered against — so it is deducted. Worth about two fils a share.

## 7. CLAIMS AGAINST THE RECORD

Every superlative and every "never" in the delivered documents is recomputed against the
filings by `prose_check.py`, which reconciles 814 figures across the study, the bibliography
and the workbook's string cells against the model's own outputs and reports **zero
unmatched**. Two figures are declared as legitimately quoted against something other than a
model output, each with its reason, and both are sourced external facts.

**Three claims the previous edition made are now false and are corrected rather than
dropped:**

* *"the two disclosed quarters of 2026"* — there were two when it was written and there are
  four now, two reported and one disclosed to 11 August.
* *the tanker revenue gross-up of 1.60* — inferred from the first quarter alone. The half
  measures 2.609, the 2025 year 2.734 and the first half of 2025 2.794. **The quarter was
  the outlier**, at 1.51 against the second quarter's 3.16, and one quarter is not an anchor
  for this line.
* *"the tanker unit's earnings are its owned fleet's charter-equivalent revenue less a
  running cost"* — falsified by the company's own half. At the published rates those 52
  ships earned 805.808 million in the six months and the unit reported EARNINGS of 994.166
  million, more than the fleet can earn before any cost at all.

**One claim is checked and stands**: the sign test on contested judgements. Seven material
judgements, four resolved upward and three downward. This study does not resolve every fork
the same way.

**Guidance is SCORED and consumed nowhere.** Against the RAISED guidance of 11 August 2026,
this build runs 11.3 per cent above on 2026 revenue and 8.7 per cent above on 2026
earnings. That is a disagreement in the study's favour on the year and it is published
rather than reconciled away — no driver takes guidance as an input, and a company that has
raised guidance twice in one year while its own disclosed third-quarter rates run far above
mid-cycle is not obviously the pessimistic side of that gap.

## 8. MULTIPLE CROSS-CHECK

At the fair value of AED 5.34 this study implies an enterprise value of USD 12.44 billion
against 2026 earnings before interest, tax, depreciation and amortisation of USD 2.716
billion — **4.6 times**. At the market price of AED 6.80 the same measure is **5.5 times**.
The three comparators in section 1.3 trade at 12.26, 8.96 and 8.10 times.

On earnings, the fair value implies **6.1 times** 2026 earnings attributable to ordinary
shareholders after the perpetual coupon; the market price implies **7.8 times**.

**THE MULTIPLES ARE THE STRONGEST ARGUMENT AGAINST THIS STUDY'S OWN ANSWER AND THEY ARE
PRINTED HERE AS SUCH.** Both the fair value and the price sit well below every comparator
on both measures, and the relative and normalised lenses — which apply peer multiples to
this company's own earnings — land at AED 12.21 and AED 11.07, roughly twice the cash-flow
lens. The disagreement is entirely about ONE thing, and the study says so: the cash-flow
lens prices charter rates reverting from an extraordinary half to the average of 2024 and
2025 by 2030, and a multiple applied to 2026 earnings prices them holding. The alternative
rate path — rates settling 30 per cent above mid-cycle — is computed in full and gives AED
7.46, above the market price.

---

## VERDICT

**The answer does not change, and the reason it does not is that nothing in the eight
headings turned up a defect.** What the review found instead is that the gap is dominated
by a single, named, published judgement — where charter rates settle after 2026 — and that
this study's own machinery already prices the other side of it at AED 7.46.

**Six things were checked and every one came back clean or corrected in this pass:** the
latest filings are read (they were not, and that is the finding this review exists for), the
base year foots to filed periods, the macro path is the house path, cash is charged once,
terminal growth is coherent with terminal inflation, and the bridge stands on the latest
sheet. The one construction the review cannot clear is the terminal, and it cannot be
cleared because the disclosure does not permit it — which is recorded, ratcheted and
re-tested rather than worked around.

**What would change the answer, stated so it can be checked later:** a fourth-quarter 2026
rate holding near the third quarter's disclosed level rather than reverting; the company
fixing a material part of the crude fleet on multi-year charters at anything near current
spot; or a disclosure that splits the vessel line by component and lets the terminal be
rebuilt on a sourced life.

**HELD.** [R-GAP-02] blocks publication while a central sits more than 10 per cent below
the latest known price. This study is 21.5 per cent below and files no market dissent, so
it does not publish. Nothing in this pass was moved toward the price: the price enters no
driver, every parameter is solved from the audited 2025 year or the reviewed 2026 half, and
the two levers that moved the answer most in each direction — the tanker cost stack at
+16.8 per cent and the gas margin at -14.8 per cent — were both measured off the same
reviewed half.
