# GBCO — GAP REVIEW [R-GAP-01], edition 17-09-2026

**17 September 2026.** Written because the rebuilt answer's UPPER branch sits more than 10%
from the latest known price. The trigger is two-sided since 02-Sep-2026, and this fires on
the upper side — the side that gets no automatic hold under [R-GAP-02] and therefore needs
this review most.

- AUDITED CENTRAL: 31.6368  (EGP per share — MNT-Halan at its reviewed carrying value)
- AUDITED CENTRAL: 44.1187  (EGP per share — MNT-Halan at the June-2026 round price)
- AUDITED SPOT: **EGP 28.98**, the supplied close of **3 September 2026**, the latest price
  this repository holds — fourteen days old at this edition's date, which is disclosed here
  rather than carried silently ([R-GAP-01 AMENDED 07-09-2026]: the price is asked for at the
  start, the work routes around it, and the standing default is the latest committed price
  used with its date stated and its age disclosed).
- AUDITED GAP: +9.2%   (the nearer branch; the far branch is +52.2%)

**A TWO-SIDED ANSWER IS AUDITED ON EVERY BRANCH.** Publishing two numbers instead of one is
not a way to publish two unaudited numbers.

**WHAT THIS REVIEW REPLACES, AND WHY IT IS A NEW ONE RATHER THAN AN AMENDMENT.**
`GAP_REVIEW_07-09-2026.md` audited 41.3484 and 52.3453 at +42.7% and +80.6%. This edition
answers a forensic external audit of that one and the answer moved: the carrying branch is
**−23.5%**, from +42.7% to +9.2%, on ten levers whose order was declared in
`REBUILD_PLAN_17-09-2026.md` **before any figure was recomputed** and whose route is walkable
in `rebuild_ledger.json`. A review written for a different answer is not a review.

---

## 1. LATEST FILINGS — every disclosed period actually read

Unchanged in substance and now recorded where a checker can point at it, which it was not
before: this study committed **no Step 2A sweep register at all** and now commits one
(`sweep_register.json`, 25 findings, 11 driver rows, zero validator errors), and it is that
register that establishes what LATEST means for the bridge.

Read and consumed: the **audited** consolidated statements for FY2023, FY2024 and FY2025;
the **reviewed** consolidated interim statements at 31 March 2026 and **30 June 2026**; and
the 4Q/FY25 (26 February 2026), 1Q26 and **2Q/1H26 (13 August 2026)** earnings releases. The
company's own investor-relations filings page was attempted this session and reached (HTTP
200); every primary document is held under `src/`.

**The most recent period is the half to 30 June 2026 and the bridge stands on it.** Nothing
newer exists: GB Corp's next disclosure is its 3Q26 release. Two things were read this
edition that the previous one had mis-read rather than missed — note 34 (re-read at 500 dpi
off the rendered pixels, the filing carrying no text layer at all) and note 26 (which states
EGP **and USD** borrowing rates, against a study that had asserted the book was entirely
local-currency).

## 2. BASE YEAR — what foots to filed periods, and what is annualised or solved

The Auto leg's base is **GB Auto's FY2025 total revenue of EGP 66,358.3mn**, the company's
own Table 8 figure. The delivered edition's four driver lines summed to 65,230.7 and the
fifth line of **1,127.6** was carried in the base and **zeroed in every forecast year**,
while the gross margin applied to that forecast is struck by the company on the whole of
total revenue. It is now carried, split into its two disclosed components — EGP 682.8mn of
external revenue outside the four published lines and EGP 444.8mn of inter-segment revenue —
and **held flat**, because GB Corp publishes no volume, price or growth rate for either.

**What is annualised, named as such:** the cost-of-debt evidence uses 1H2026's finance cost
doubled (18.20% against FY2025's 20.02%, both on a quarter-weighted average of the
borrowings that actually bear the charge); and the working-capital anchor is measured over
**trailing twelve-month** revenue of 75,707.1 rather than an annualised half.

**What is solved rather than filed:** the currency split of the debt book. Note 26 discloses
the two RATES (21.91% EGP, 8.30% USD) and not the two BALANCES, so the split is DERIVED by
identity from those rates and this segment's own measured effective rate, and is labelled
derived everywhere it is quoted.

**The first forecast year is a stub and that is new.** A bridge struck at 30 June 2026
already reflects the cash the first half produced — GB Auto's net debt fell 15,210.0 →
14,493.6 — so a full calendar-2026 free cash flow beside it counts that half twice. The
first year's profit, depreciation and capital expenditure are scaled to the **49.77%** of
the year still unearned, measured from GB Auto's own disclosed first-half revenue against
the model's own FY2026E. This was found by implementing the audit's finding 2 rather than by
the audit.

## 3. MACRO COHERENCE — inflation, currency and price on one path

The study carries **no inflation number of its own** and now carries no currency of its own
either. Both come from `engine/macro_paths/EG.json`: the CBE's published ladder to a 7%
terminal, the policy-rate glide that gives the cost-of-capital schedule its shape, and
**USD/EGP 50.25 as at 6 August 2026**.

That last is a change and it is finding 32's: the delivered edition typed **47.5** with no
source and no date on a line worth roughly half the upper branch. The house anchor is 5.8%
weaker, so the round branch RISES. **A correction that moves an answer AWAY from the price is
not a reason to reconsider the correction.**

The anchor is 42 days old against [R-COC-01]'s 14-day bound; the staleness is accepted
deliberately and disclosed in the study's own macro record, which is the shape that rule
requires rather than a silent substitution.

## 4. DISCOUNT RATE — the operations discounted at the right rate, the cash charged once

**This is the heading the rebuild changed most.** The delivered edition ran THREE capital
structures in one calculation: the GROUP's borrowings and market capitalisation in the
weights, a GROUP cost of debt whose numerator deliberately included **GB Capital's** cost of
funds, and the AUTO segment's net debt in the bridge. The published 22.88% landed within
0.3pp of one internally consistent pairing — right by offsetting errors, and no reader could
have told.

One entity throughout now. GB Auto's own interest-bearing book (22,733.1 of debt plus
2,345.8 of leasing notes, because the release's own footnote says the finance charge
includes the leasing expense), GB Auto's own segment finance cost over a quarter-weighted
average of it, and the leg's own equity value as the equity weight — taken to a **fixed
point by bisection**, because a segment has no quoted price and borrowing the group's market
capitalisation is what finding 11 named. Explicit-window WACC **19.40%** against 22.88%
before; terminal **14.16%**, essentially unmoved.

**The cash is charged exactly once.** The operations are discounted at a GROSS-debt-weighted
rate and the cash is netted inside the company's own published net-debt figure. The
prohibited pair — cash added at face beside NET weights — is not what this model does, and
the bridge record now says so in the field [R-BRIDGE-01] requires rather than leaving it to
be inferred.

## 5. TERMINAL — growth coherent with the inflation inside the terminal rate

Terminal growth is **derived**, not typed: the house path's 7.0% terminal inflation plus a
stated REAL growth of zero. The terminal risk-free rate is derived the same way. **85.1%** of
the Auto leg's enterprise value is terminal value, which is disclosed in the document in
those words rather than buried.

**The asset-life refusal stands and the charge it leaves behind is now printed.** No usable
life could be sourced (`useful_lives.json`: the policy note gives rate RANGES implying 3 to
50 years and note 17 combines undepreciated LAND with buildings, so the derived identity
returns 10.9–17.1 years and contradicts the policy note's own bands). `terminal_value.build()`
refuses this name and the study stays on the [R-TERM-01] ratchet with that file as the
reason. What the delivered edition did not say is what its terminal charges anyway: **1.75×
its own book depreciation** on capital expenditure, EGP 2,800mn against 1,604mn. A company
replacing its base over a 10.9–17.1-year composite would spend about book depreciation
grossed for cost inflation, so this terminal charges **above** replacement rather than below
it — the one direction [R-TERM-01 CLAUSE TWO]'s inference runs without a sourced life, and
the conservative one.

**What is still outstanding here, stated rather than discovered later:** capital expenditure
consumes management's described investment plans, which [R-FCAL-01] forbids as an input. It
is not corrected in this edition, because correcting it inside a terminal construction that
is itself retired would multiply the correction roughly fifteen-fold through a construction
nobody defends. It is registered in `REBUILD_PLAN_17-09-2026.md` with that reason and in the
sweep register's own driver-gate row.

## 6. BALANCE SHEET — the bridge on the latest disclosed sheet

The bridge stands on the **reviewed 30 June 2026** statements and the 2Q26 release's Table
12 segmented balance sheet, established by the sweep register rather than asserted.

Two corrections here, both the audit's. **Net debt reproduces the company's own published
figure**: the delivered edition claimed "the COMPANY'S OWN definition" in a comment and came
out at 14,623.7 against a published 14,493.6, because it took only the NON-CURRENT portion
of the notes payable to leasing (1,333.3 of 2,345.8) and omitted the due-FROM-related-parties
balance of 1,142.1 that Table 7 nets. **And the minority comes out at its share of value
rather than at book**: the model capitalises 100% of the segment's cash flow, so the
minority's claim is on the value those flows produce — 4.347% of the leg's equity value, EGP
801.1mn against 590.7 at book, with the book, profit-share and proportional framings all
published beside the adopted one as [R-BRIDGE-01] requires.

The bridge foots, and it is asserted to: EV 32,923.9 less net debt 14,493.6 less the
minority's 801.1 is 17,629.2, plus the lender's 482.0 and the associates at 16,230.5 gives
34,342.2 over 1,085.5 shares — the published carrying branch.

## 7. CLAIMS AGAINST THE RECORD — every "best ever" or "never" recomputed

Three claims in the delivered edition were checked against the filings and two were wrong.

**The lending book is not fixed-rate.** The document said "every cut lowers GB Capital's
funding cost on a fixed-rate lending book"; the interest-rate-risk note shows the book is
overwhelmingly **variable**-rate with only about a quarter fixed, so a cut passes through to
the asset side too. Corrected.

**"Other associates (Bedaya, Kaf)" names two of three.** Note 34 lists Misr E-commerce B.V.,
Bedaia and Kaf for Life Insurance. Corrected.

**The operating-profit line did not foot.** Appendix A.2 printed 3,977.0 for FY2023 and
6,176.6 for FY2024 and the rows above them sum to 3,708.0 and 5,820.9 — the difference is
each year's PROVISIONS to the pound, because GB Corp's own presentation of "Operating
Profit" EXCLUDED provisions in FY2023 and includes them from FY2024. The study's own
committed EBIT proves which basis is which. The line is computed from the rows on one basis
now and the as-reported figures are carried beside it: a restatement is noted, never
substituted.

**What was checked and holds:** the beta is a conforming tier-1 own-stock regression against
the published EGX30 (0.8907, 251 weekly observations), attested by
`assert_beta_provenance()`; country risk enters exactly once; and the three-observation
median behind the relative multiple is published with its count, because a median of three
is a thin statistic and a reader is entitled to know how thin.

## 8. MULTIPLE CROSS-CHECK — what the fair value implies, and what the price implies

On the **carrying branch at EGP 31.64**, the answer is 9.2% above a traded 28.98 — an
ordinary disagreement, and the branch this study can most easily defend. It is a
sum-of-the-parts in which the operating businesses alone (Auto 17.6bn, the lender 0.5bn)
come to **58%** of the traded market capitalisation, with the associates carrying the rest.

On the **round branch at EGP 44.12**, +52.2%, the disagreement is real and is about ONE
LINE. The two branches differ in nothing but the basis on which GB Corp's MNT-Halan interest
is carried: EGP 15,723.5mn in its own reviewed accounts, against EGP 29,272.6mn implied by
41.61% of the June-2026 round. **THE AUDIT'S FIRST FINDING IS ACCEPTED AND IT CHANGES WHAT
THE UPPER BRANCH IS.** The delivered edition presented both as "the company's own
disclosures"; the study's own committed record cites GB Corp's 9 June release for the
**stake** and carries **no source field at all** for the round figure. It is a third-party
mark GB Corp has never adopted as its own carrying value, it is published as that, and both
branches are relabelled accordingly.

**What the price implies, solved from this study's own drivers:** the traded price pays
**US$614mn** for MNT-Halan as a whole, against the US$1,400mn the round was struck at and the
US$752mn the company's own carrying value implies. The price is below both bases the company
discloses — and the reverse read lives in `diagnostics.json`, outside the numbers file any
builder reads, so a quantity solved from a price cannot re-enter the valuation.

The relative cross-check at **EGP 18.08** is the most conservative read here and is 37.6%
BELOW the price: it pays for one year's earnings on the company's own historical rating and
gives nothing at all for the associate stake. It is a cross-check and carries no weight.

---

## VERDICT

**The carrying branch is no longer a large-gap answer and the round branch still is.** Ten
levers took the carrying branch from +42.7% to +9.2%, and the single largest of them —
finding 2's working-capital anchor at −26.9% — is the one the previous review's eight
headings did not catch, because it is a defect in the RELATIONSHIP between two dates rather
than in any figure. That is recorded here as this review's own limitation rather than as a
success: **the eight headings were written and passed on 7 September against a model
carrying that defect.**

The upper branch's +52.2% is not a claim that the market is wrong about GB Corp. It is a
claim that the market is not paying the June-2026 round's price for a stake GB Corp itself
carries at 54% of that price, and the study publishes both rather than choosing. The review
finds nothing in the model that would close that gap; what would close it is a decision about
the associate's basis, and that decision is the reader's.

**Nothing in this review moves an answer toward the price.** One correction in this edition
moved the round branch AWAY from it, and it is kept.
