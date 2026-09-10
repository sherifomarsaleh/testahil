# SWDY — valuation-gap review, 7 September 2026  [R-GAP-01]

**AUDITED CENTRAL: 52.6969**
**AUDITED GAP: -59.5%**

**Trigger.** This edition publishes a central of **EGP 52.6969** against the latest known
price of **EGP 130.00** (3 September 2026, `engine/prices/SUPPLIED_03-09-2026.json`) —
**59.5% below**, six times the ten-point threshold. The study was originally struck at
EGP 105.20 of 5 August 2026, where the same model read −47.3%; **the price moved 23.6% in
four weeks and the model moved −5.0%**, so most of the widening is the market and not the
method. That is exactly the thing a study cannot see from inside itself, and it is why
[R-GAP-01 AMENDED] measures against the latest known price rather than the strike.

**Outcome.** THE ANSWER IS AUDITED AND IT DOES NOT CHANGE FOR THE PRICE. Three defects
were found and every one of them **LOWERED or held the value**; nothing was found that
raises it toward 130. The gap that survives this review is a genuine disagreement with
the market, and its arithmetic is named under DISCOUNT RATE below: at a 26.94%
explicit-window cost of capital and a 15.93% terminal rate, the reverse read says the
price needs a **474 basis point parallel fall** in the cost of capital, which is a
disagreement about Egypt rather than about Elsewedy Electric.

The whole route is in `rebuild_ledger.json` — four levers, three rules, cumulative −5.02%.

---

## LATEST FILINGS — was every disclosed period actually read?

**Yes, and the archive was re-fetched from the company's own investor-relations portal in
this pass rather than taken on trust.** 233 documents retrieved across 2007–2026 from
`ir.elsewedyelectric.com`, logged attempt by attempt in
`engine/swdy_walkforward/fetch_attempts.json`.

Most recent filings, both read:

- **Reviewed condensed interim consolidated financial statements for the six months ended
  30 June 2026**, board-approved 11 August 2026 — revenue, gross profit, net finance,
  associates, tax, attributable profit, the balance sheet at 30 June 2026 and note 38's
  employees' share, all consumed.
- **Q1-2026 reviewed interim consolidated statements** — read for the effective tax rate
  and the disclosed Egyptian-pound borrowing rate, both now REGISTERED as inputs rather
  than quoted in prose.
- **Audited consolidated financial statements for the year ended 31 December 2025** — read
  in full, including note 17 (property, plant and equipment), note 29 (share capital),
  note 40 (shareholders' structure) and note 44-2 (depreciation policy).

**One extraction defect was found and it is worth naming**, because the figure looked
perfectly clean: the FY2025 statement of financial position is on an IMAGE-ONLY PAGE of an
otherwise text-layer filing, and its OCR renders cash and equivalents as `Al 949 208 624`.
Read naively that is EGP 949,208,624 against a real EGP 41,949,208,624 — out by a factor
of 44, in a column of otherwise perfect figures. It is caught because the balance sheet is
footed three ways and against the cash-flow statement's own closing balance, which sits on
a text-layer page. **Arithmetic is the arbiter, not the extractor.**

## BASE YEAR — does it foot to filed periods?

**Yes, and nothing in it is annualised, scaled or solved.** The base is audited FY2025 as
filed: revenue 281,049,081,719, gross profit 40,762,108,187, operating profit
25,354,225,619, profit before tax 24,777,689,839, attributable profit 17,330,244,990. Every
subtotal foots against its own printed parts, and the segment split reproduces total revenue
to the pound. The forecast is anchored on the **reviewed H1-2026** margin, not on the
full-year average: `forecast_anchor.py` records the latest reviewed period at 13.9966% and
the first forecast year at 12.0800%, and the path RISES from there — the study is not
walking a rate back toward a longer average, and the record is printed whether or not it
fires.

## MACRO COHERENCE — are inflation, currency and price one path?

**Yes.** There is one Egyptian inflation figure in this study and it is the house terminal
of 7.0%; terminal growth is DERIVED from it and a stated real growth of zero, never typed
beside it. The currency path is the study's own registered `fx_path`, and the terminal
risk-free rate, terminal cost of debt and terminal growth all sit on the same 7%. The
hard-currency leg is translated on that same path and is not held still while pound costs
escalate — which is [L-048], the defect this heading exists to catch.

**The one place it could have gone wrong is the cross-check and it is disclosed rather than
hidden:** the currency-of-discounting alternative deflates the hard-currency leg to dollars
at each year's own rate, discounts at a USD cost of capital and translates back, giving EGP
70.85. That is a DIFFERENT clock deliberately, published as an alternative reading, and it
is not averaged into the answer.

## DISCOUNT RATE — the right rate, and cash charged for exactly once

**This is where the gap actually lives, and the arithmetic is stated rather than asserted.**
The explicit window discounts at **26.94%** and the terminal at **15.93%**, on a glide whose
shape is inherited from the cost-of-debt path rather than being a second free parameter.
Cost of equity 28.40% explicit, 17.56% terminal. Country risk enters once: the risk-free
rate is normalised by Egypt's own default spread and the premium is added back on the same
basis.

**Cash is charged for exactly once.** SWDY is a NET DEBT company — interest-bearing
borrowings EGP 62,509.2mn against cash of EGP 41,949.2mn at 31 December 2025, net debt
EGP 20,560.0mn — so the weights are ordinary, the equity weight is below one, and the
operating rate sits BELOW the cost of equity as it must. Net debt is deducted once in the
bridge and nowhere else, and the reviewed 30-June-2026 net debt of EGP 28,629mn is
explicitly NOT deducted, because the deterioration over that half is the same working-capital
absorption the model's own FY2026 forecast already carries — deducting it in the bridge as
well would charge one cash outflow twice.

**THE MARKET-VALUE EQUITY WEIGHT MOVED WITH THE PRICE AND THAT IS NOT CIRCULARITY, IT IS THE
RULE:** re-striking at 130.00 raised market capitalisation, cut the debt weight and took the
explicit-window rate from 26.63% to 26.94%. [R-COC-01] requires market-value weights and
this is what they do.

**THE REVERSE READ, SOLVED RATHER THAN ASSERTED** (`path_to_130.json`): holding every other
driver at its published value, EGP 130.00 today needs a **parallel fall in the cost of
capital of 474 basis points** — the only single driver that reaches it inside a defensible
range. An EBITDA-margin uplift would need **+6.07 percentage points**, which is outside any
defensible range; the currency path, terminal growth, working capital and extra foreign
revenue growth are each UNREACHABLE across their whole plausible span. Two combinations of
individually-defensible legs reach EGP 85–88, not 130.

**A REVERSE READ LANDING ON A BELIEVABLE NUMBER IS EVIDENCE AGAINST THE STUDY, and this one
is half-believable.** A 474bp fall in Egypt's cost of capital is not absurd — the central
bank is easing and this model's own terminal rate is 1,100bp below its explicit-window rate.
What the price is disagreeing about is the SPEED of that easing, not this company's
operations. That is recorded as the crux rather than resolved.

## TERMINAL — coherent with the inflation inside the terminal rate

**A DEFECT WAS FOUND HERE AND IT LOWERED THE VALUE.** The terminal is built by
`engine/terminal_value.py`, the only sanctioned route, on a **DISCLOSED useful life of
17.2627 years** derived by identity from the company's own note 17 and recorded with its
route in `useful_lives.json`. Route one fails on this name — the policy note discloses five
RANGES and no scalar, machinery spanning 5 to 15 years — and the identity is corroborated
twice: a second fiscal year of the same note gives 17.9761, and the composite implied by
charging every class at the LONG END of its own disclosed range gives 17.3041, agreement to
0.24%.

**The defect was the BASIS of the flows handed to that module, not the module.**
`TerminalInputs` says in its first sentence that it takes the LAST EXPLICIT YEAR'S figures
and grows the free cash flow one year itself, and warns in terms that a NOPAT already grown
by (1+g) overstates the terminal by exactly (1+g). This study passed NOPAT, book
depreciation AND the working-capital base all multiplied by 1.07 before handing them to a
function that multiplies by 1.07 again — a year-seven flow discounted at the year-five
factor. The module's own note records that six of eight callers read the field this way on
4 September 2026; **this was one of them and had not been corrected**. Terminal value
319,477 → 298,577; the central 56.26 → 52.70.

Terminal growth of 7.0% equals the inflation inside the terminal discount rate exactly, so
real terminal growth is ZERO and is stated as zero — no perpetual real decline, and no real
growth charged for without capital behind it. The terminal carries **84.1%** of enterprise
value, which is high and is disclosed: at a 15.93% terminal rate and 7% growth the
capitalisation factor is 11.2x, and a five-year window on a company compounding at these
rates leaves most of the value beyond it.

## BALANCE SHEET — does the bridge stand on the latest disclosed sheet?

**It stands on the audited 31-December-2025 sheet, and the reason is stated rather than
assumed.** The bridge is dated to the valuation date and the reviewed 30-June-2026 sheet is
read and published beside it (net debt 28,629, associates 7,120) rather than substituted,
because the model's own FY2026 forecast already carries the working-capital absorption that
produced the change. The bridge FOOTS: enterprise value 138,203.0 less net debt 20,560.0
plus associates at carrying value 6,757.7 = 124,400.7; less minority interests at their
9.68% share of group profit = 12,032.7; less the employees' statutory share at 12.19% =
13,703.5; equals equity attributable to ordinary shareholders **98,664.5**, which divides by
2,140,777,876 shares to EGP 46.0882 at 31 December 2025 and rolls to EGP 52.6969 at the
3-September-2026 anchor.

**A SECOND DEFECT WAS FOUND HERE, IN THE DELIVERED WORKBOOK RATHER THAN IN THE MODEL.** The
workbook published EGP 59.3132 where the document published 55.4822 — +6.9%, with ZERO
formula errors — because two builder defects pulled opposite ways: `DCF!C25` still carried
the retired g x IC reinvestment identity, and `SOTP Bridge!C12` carried no line at all for
the employees' statutory share. A reader following the printed bridge from enterprise value
to equity arrived EGP 13.7bn above where the study did. Both are fixed; `recalc.py` now
reports 594 formulas, 0 unresolvable, 594 cell-level agreements and 41 headline
reconciliations passed.

**The share count is footed against its own par value and is NOT today's count carried
back.** Note 29 is a chronology: EGP 2,234,180,000 over 223,418,000 shares at par EGP 10 in
January 2017; 218,418,000 shares after the May 2017 treasury write-off; a par split to EGP 1
in May 2018; 2,170,777,876 shares after the October 2022 retirement; 2,140,777,876 after
April 2024. Issued capital over par reproduces the count the same note states at every step.

## CLAIMS AGAINST THE RECORD — every superlative recomputed

Every percentage and multiple in both delivered documents is now reconciled against a model
output or a NAMED ratio of committed inputs: `prose_check.py` reports **543 figures checked,
0 unmatched**. It reported 22 unmatched before this pass, and the repair was to REGISTER the
disclosed figures the bibliography was quoting in prose — fifteen of them, each with four
fields: the family shareholdings from note 40, the disclosed effective tax rates for Q1-2026
and the 2025 halves, the disclosed Egyptian-pound borrowing rates at FY2024 and Q1-2026, the
export share from note 5, the minority's share of H1-2026 profit and of total equity, and
the H1-2025 employees' share. **If a figure is real and the model cannot produce it, the
model is what is missing.**

**A widening was tried first and REVERTED, and it is recorded because it nearly shipped:**
adding every pairwise ratio among the committed inputs took the unmatched count to zero and
the rendering set to 3,613,198 values, which matched **400 of 400 random two-decimal
percentages between 0.5 and 99.5**. That is a green tick on a red result. The set now stands
at 64,269 and misses 284 of 400 random percentages, so the zero it reports means something.

No "best ever" or "never" claim survives in either document that has not been recomputed;
the FY2025 gross margin, the EBITDA path and the segment shares are all model outputs.

## MULTIPLE CROSS-CHECK — what the fair value implies

| multiple | at the fair value 52.6969 | at the market price 130.00 |
|---|---|---|
| P/E on FY2025 attributable profit | **6.51x** | 16.06x |
| P/E on FY2026E attributable profit | **4.97x** | 12.26x |
| EV/EBITDA on FY2025 | **4.70x** | 10.54x |
| EV/EBITDA on FY2026E | **3.51x** | 7.87x |

**The implied multiples are low and they are not absurd for this market at this cost of
capital** — an Egyptian industrial discounted at 26.94% in the explicit window mechanically
prints a mid-single-digit earnings multiple. But two readings sit against the central and
both are published beside it rather than buried:

1. **THE BOOK LENS IS ABOVE THE CENTRAL.** The justified price-to-book floor reads EGP
   55.90 against a cash-flow lens of 52.70. A company's disclosed book floor exceeding the
   discounted value of its own cash flows is a flag, not a proof, and it is what the
   cross-checks are for.
2. **THE RELATIVE LENS READS 71.64 AND THE NORMALISED LENS 97.90.** Under [R-LENS-03] the
   class primary IS the central and these are cross-checks; the disagreement between them is
   published rather than averaged. The retired 45/20/20/15 blend would have printed EGP
   66.01 and shown a reader about half the disagreement this study actually holds.

**A THIRD DEFECT WAS FOUND UNDER THIS HEADING.** The employees' statutory share was charged
in the bridge, the currency alternative, the sensitivity helper and the scenarios — and NOT
in the three cross-check lenses a reader is shown beside the central, so the same company was
worth 12.19% more per share depending on which lens was reading it. [L-294] is about a claim
ahead of ordinary shareholders and it does not become one only when a discounted cash flow is
the instrument. Relative 80.58 → 71.64, normalised 109.52 → 97.90. **The central does not
move**, which is the whole point of the class-primary architecture.

---

## What this review did NOT find

Nothing that raises the value toward 130. No unread filing, no stale base year, no
contradictory macro path, no double-charged cash, no real-terms terminal decline, no typed
claim that is false. The three defects found all ran the other way, and the largest of them —
the terminal basis — **moved the answer FURTHER from the price**, which is the only
direction that demonstrates the discipline is not fitting to a quote.

**The gap is a disagreement about Egypt's cost of capital, and it is stated as one.** The
study holds a 26.94% explicit-window rate; the price needs 22.20%. Which of those is right
is not settled by this review, and the range this study publishes — EGP 19.64 to 101.31 on
its own clock — is wide precisely because that question is open.
