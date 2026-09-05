# ADNOCDRILL — gap review [R-GAP-01]

**AUDITED CENTRAL: 4.9194**
**AUDITED GAP: -15.2%**

AED 4.9194 a share against the latest known close of **AED 5.80 on 3 September 2026** —
15.2% below. It was struck against AED 5.94 on 7 August, where its own document states
17.2% below.

Written because the answer was invisible: the study carried it at `fair_value.central` and
`fair_value.spot`, and the shared reader looks for `central` and `spot` at the top level, so
[R-GAP-01] could say nothing about this study and it sat on the unreadable list. **The
invisibility and the defect are the same event** — nothing was looking at the number, so
nothing asked why three lenses that value a franchise at historical cost were carrying half
the weight.

**The verdict is that the discount is OURS, and it is architectural.**

---

## The shape of the answer, which is itself part of what is audited

| lens | weight | AED | vs 5.80 | vs 5.94 at strike |
|---|---|---|---|---|
| cash flow — continued expansion | 0.25 | 6.2083 | **+7.0%** | +4.5% |
| cash flow — capacity plateau | 0.25 | 5.3970 | **−6.9%** | −9.1% |
| relative multiple | 0.20 | 3.9495 | −31.9% | −33.5% |
| book and sustainable return | 0.15 | 4.7251 | −18.5% | −20.5% |
| normalised earnings power | 0.15 | 3.4628 | −40.3% | −41.7% |
| **weighted central** | | **4.9194** | **−15.2%** | −17.2% |
| the two cash-flow framings, midpoint | | **5.8026** | **+0.0%** | −2.3% |

**The two cash-flow framings STRADDLE the market and their midpoint lands 0.04% from it.**
That single fact organises everything below.

## 1. LATEST FILINGS

**Clean.** The company's own investor page names its latest announcement as **30 July 2026
(second-quarter results)** and its next as third-quarter results on 28 October. Nothing later
than the half year exists. The half-year statements, management discussion, press release,
presentation and **earnings-call transcript** are all consumed — twenty-one separate
half-year inputs, each sourced to the reviewed interim.

**One superseded anchor, in the model rather than only in the prose.** The study carries
"six island rigs on order for delivery between 2026 and **2028**" from the FY2025 management
discussion, and the fleet plan reaches eighteen island rigs in 2028. The half-year
management discussion supersedes it: one arrived in the second quarter ahead of schedule,
one around the middle of the third, and "the **remaining four** new island rigs are
currently expected to join the fleet **in 2027**." Worth **+0.0054** on the expansion
framing.

## 2. BASE YEAR

**Foots, and everything solved is named.** The annualised half-year revenue is used only as
the denominator of the working-capital ratio and is labelled annualised. The stub and anchor
year fractions are real calendar arithmetic. The infeasible oilfield-services solve is the
study **demonstrating** an unidentified split rather than filling it — the two-population
solve returns an implied rate of **−6,788** and it declined to use it. That is the rule
working as intended.

**The live item is the segment calibration** — persistent multi-year level shifts on unit
rates (onshore 0.9002, offshore 1.0253, services 1.0799) **solved against FY2026 guidance**
("~2 / ~1.5 / ~1.5", one-decimal roundings). That is guidance **consumed**, not scored,
against [R-FCAL-01] — and it runs against the value, because the raw ground-up build totals
5,086mn against a guided 5,000mn. Worth **+0.2001** on the expansion framing.

## 3. MACRO COHERENCE

**One path, slightly below the house ladder.** The AE house path, read live: 2.5 / 2.0 / 2.0
/ 2.0 / 2.0, terminal 2.0%, terminal risk-free 3.98% derived, pegged. The study is
internally coherent — revenue price +1.5%, cost basket about +1.4%, fuel on its own crude
path per the cost-stack rule — and **this is not the [L-048] defect.**

Two breaks. The cost escalator sits at **1.5% against the house 2.0%** on every domestic
line, sourced to the study's own consumer-price read; moving revenue and the domestic cost
lines onto the house ladder is worth **+0.0997** on the expansion framing. And terminal
growth is typed nominal — 2.5% on framing A is **+0.49% real**, 1.5% on framing B is
**−0.49% real**, a perpetual real decline in the plateau case that the document nowhere
writes down as the real number it is.

## 4. DISCOUNT RATE

**Country risk counted once; cash charged once; flat is right and unstated.** The study says
so in terms at line 625: the risk-free is the US ten-year of 4.69% less the **US** default
spread of 0.23%, and the equity premium carries the Abu Dhabi country premium. The cost of
debt of 5.15% clears the sovereign floor of 4.86% and is the only one of three candidates
that does. Weights are market-value on **gross** debt and the bridge adds cash back — the
sanctioned "value the operations, add the cash" construction, not both.

Three findings. **Flat is correct for a peg and never explained** — the study sets the
terminal rate equal to the cost of capital and does not tell a reader why. **The risk-free
basis**: the house AE path holds a sovereign quote of 4.48% with a rating spread of 0.42%,
giving a normalised 4.06% against the study's 4.46% — worth **+0.4612** on the expansion
framing and **+0.2789** on the blend. *The caveat is not hidden*: the house quote is on an
approximately five-year tenor, so part of that difference is tenor rather than basis; on a
like-tenor comparison the two estimates are 4.17% and 4.06%, eleven basis points apart. And
**Table 17 mislabels its own weight** — the caption reads "market capitalisation over market
capitalisation plus **net** debt" beside 91.1%, which is the **gross** figure (91.14%); the
net one is 92.30%. The number is right and the caption is stale from the edition before the
weights moved.

## 5. TERMINAL

**The retired construction, and it is NOT where the gap is.** The census lists this study
under `unreadable` — its terminal exposes no terminal rate — so it is not clean, it is
invisible. It does not go through the sanctioned module. `compute.py:1265` is the identity:
reinvestment = growth / return on capital, terminal value = profit × (1 − reinvestment) /
(rate − growth). The implied replacement cycle is 1/g — **40.0 years on framing A and 66.7
on framing B** — against a disclosed **4 to 30 years** for drilling rigs (FY2025 note 3) and
a gross-cost-over-charge implied life of **19.29 years**.

Rebuilt through the sanctioned module rather than reading the sign off the ratio, per
[R-TERM-01 CLAUSE TWO CORRECTED]:

| maintenance basis | maintenance (2030) | framing A | vs the published 6.2083 |
|---|---|---|---|
| the company's disclosed "up to USD 0.3bn per annum" | 324,729 | **REFUSED** — implied payout 107.3% | — |
| the disclosed 30-year life (top of the 4–30 band) | 516,236 | 6.8884 | +0.6801 |
| a 20-year life (the reassessed 8–20 band, note 4) | 774,354 | 6.1021 | −0.1061 |
| 19.29 years, gross cost over the FY2025 charge | 803,032 | 6.0148 | −0.1935 |

**On every basis the module accepts, the sanctioned terminal is neutral to slightly lower.**
The bases that would raise it are refused because terminal cash flow exceeds terminal
profit. That is a **disclosure** problem, not a modelling one: the accounts do not split
short-lived drilling equipment (some at four years, with 16.1% of gross cost fully
depreciated and still in use) from rig hulls, and the FY2025 accounts **reassessed useful
lives and residual values**, which breaks the accumulated-over-charge age identity outright.
**A life this desk chose is not a disclosed life**, so this is stop-and-inform rather than a
correction. The 1/g flag was right to fire and the terminal is not the culprit.

## 6. BALANCE SHEET

**Clean, and every line was verified against the filing.** All thirteen bridge items check
against the reviewed 30 June 2026 statements: property and equipment 5,705,373 · joint
venture 461,729 · cash 355,423 · borrowings 1,247,510 + 1,221,269 · leases 28,206 + 16,977 ·
financial liability 62,530 · minority 53,594 · equity 4,287,313. Net debt of 2,158,539
reproduces the management discussion's printed 2,158. The acquired working capital of 41,134
comes out of note 5 and is stripped from the 2026 operating movement so the acquisition is
not charged twice; the perimeter is handled consistently on both sides.

The minority is deducted as the **put liability (62,530)** rather than book (53,594), with
the reasoning written down — deducting both would charge the parent twice. Deducting book as
well would cost **0.0123 AED**. The second-quarter dividend of USD 262.5mn was declared
30 July with a record date of 10 August, so the 7 August anchor traded cum and it is
correctly not deducted.

## 7. CLAIMS AGAINST THE RECORD

**Two fail.**

**"The return on capital employed was 24.4% in 2025."** The company's own FY2025 management
discussion discloses **23%**, defined as trailing operating profit over capital employed.
24.4% is the study's own after-tax computation presented under the company's defined term
without saying so — and **the study's own input register says 23% in the same file.** The
terminal return of 18% is then justified as fading "the 23%", an **after-tax** target
against a **pre-tax** disclosed figure (23% pre-tax at 9% tax is 20.9% after tax).

**Section 3 publishes the retired skill verdict** — "the map scored 1.65% **WORSE** than a
simple no-information benchmark" and "a scoring rule that rewards sharpness penalises it
accordingly". [R-CAL-03] retires that outright from every public surface, and a delivered
study is one. This document is now on the band-vocabulary ratchet with the fix named.

Stale but arithmetically correct at the strike: "12.9 times its own last-twelve-month
EBITDA" (now 12.44×), "AED 0.81 apart — 13.7% of the current price" (now 14.0%), the
masthead's "trades at AED 5.94", and the joint venture "carried at USD 437 million" against
a latest disclosed 461,729. Verified and correct: 4% against 22% revenue growth; 115 rigs in
2022 to 171 by mid-2026; the declined 2027 guidance; the price sitting above four of five
lenses.

## 8. MULTIPLE CROSS-CHECK

| | EV/LTM EBITDA | EV/FY26E EBITDA | P/E FY26E | yield on the **committed** floor |
|---|---|---|---|---|
| central 4.9194 | 10.67× | 10.60× | 15.58× | **4.90%** |
| framing A 6.2083 | 13.25× | 13.17× | 19.66× | 3.88% |
| framing B 5.3970 | 11.63× | 11.55× | 17.09× | 4.47% |
| market 5.80 | 12.44× | 12.35× | 18.37× | 4.16% |

The market's 12.44× sits above every driller (ADES 10.23×, Valaris 10.03×, Arabian 8.75×,
Noble 8.55×) and level with Schlumberger 12.76× and Baker Hughes 12.13× — on a company
running **44–50% EBITDA margins and 29–34% net margins**, where four of the six drillers in
the peer table print **negative** last-twelve-month net income.

**The sharpest cross-check is one the study never runs.** The board has committed USD 1.05bn
in 2026 growing at a minimum 5% a year until at least 2030; that reproduces both of the
company's own disclosures exactly (a minimum cumulative USD 5,801,913k = **AED 1.3323 a
share**, against the presentation's "USD 5.8bn" and "about AED 1.3 a share"). **The central
of 4.9194 implies a 4.90% starting yield on a contractually floored, 5%-growing stream** —
a Gordon-required return of 9.90% against this study's own cost of equity of **8.33%**. The
floor is covered 1.11× to 1.66× by the model's own free cash flow in every forecast year.

---

## What the price implies under this study's own drivers

Solved through the study's own model, holding every other driver at its published value:

| | framing A | framing B |
|---|---|---|
| cost of capital reaching 5.80 | 8.375% (+37bp) | 7.582% (−43bp) |
| terminal nominal growth reaching 5.80 | 1.797% (−0.20% real) | 2.301% (+0.30% real) |
| terminal return on capital reaching 5.80 | 12.06% | unreachable — B is below 5.80 at any return |
| **beta reaching 5.80** | **0.878** | **0.698** |
| FY2030 EBITDA margin reaching 5.80 | 43.8% | 50.6% |

**Not one is an impossible belief.** A beta of 0.878 sits inside this study's own 90%
interval of 0.577–1.014 and *below* its own two-year (0.890) and three-year (1.025)
regressions. A terminal growth of 1.80% is −0.20% real. A 43.8% FY2030 margin is inside the
filed range of 44.1–49.9%. **A reverse read landing on a believable number is evidence
against the dissent**, and there is none to file here.

## The corrections, priced, in both directions

| # | correction | rule | framing A | blend |
|---|---|---|---|---|
| **1** | **the typed five-lens blend retired; the class primary alone** | **[R-LENS-03]** | — | **+0.8832** (midpoint) to **+1.2889** (framing A) |
| 2 | the normalised lens capitalises flat NOMINAL profit at a nominal rate — a 2%/yr perpetual real decline | [R-LENS-03] Fisher clause | — | +0.1932 to +0.2087 |
| 3 | risk-free on the AE sovereign rating basis, not the US ten-year | WACC / [R-MACRO-01] | +0.4612 | +0.2789 (tenor caveat above) |
| 4 | book lens' sustainable return 30.6% against a realised 36.7% | dual framing | — | +0.1547 |
| 5 | segment calibration solved off ROUNDED guidance | [R-FCAL-01] | +0.2001 | +0.0841 |
| 6 | onshore peer multiple blends US land drillers (median 6.15×, including one at 2.16×) against a MENA national-oil-company median of 9.49× | [R-LENS-03] | — | +0.0833 |
| 7 | escalators 1.5% → the house AE 2.0% | [R-MACRO-01] | +0.0997 | +0.0557 |
| 8 | working capital on the mid-year sheet (9.008%) against audited history (5.913%) | — | +0.0400 | +0.0193 |
| 9 | relative lens on trailing rather than guided EBITDA | — | — | +0.0184 |
| **10** | **depreciation anchored on FY2025 (9.520%) rather than the reviewed half-year annualised (8.917%)** | **[R-ANCHOR-01]** | +0.0543 | +0.0183 |
| 11 | FY2026 capital spending 700 against the guided low end of 600 | — | +0.0386 | +0.0181 |
| 12 | island fleet on the superseded FY2025 schedule | MODON precedent | +0.0054 | ~0 |

**#10 is the sharpest small finding because the study refutes itself on it.** Its own
normalised lens uses the half-year annualised charge of 521,060 and says in terms that this
is "the depreciation this fleet carries… what the fleet being priced actually carries" — and
then the primary lens charges 556,281 in 2026 off a stale FY2025 rate. One model, two
depreciation anchors, and the study argues for the one it does not use. The company's own
halves agree: depreciation FELL 5.3% into the second half of 2025 after the useful-life
reassessment, and the model implies it rising 13.5% into the second half of 2026.

**And the ones that run the other way:**

| | correction | framing A | blend |
|---|---|---|---|
| 13 | book minority deducted alongside the put | — | −0.0123 |
| 14 | **the terminal rebuilt through the sanctioned module** on the lives it accepts | **−0.1061 to −0.1935** | — |
| 15 | terminal rate at the cost of equity on the 2030 net-cash sheet | −0.2849 | −0.1221 |
| 16 | **beta 0.795 (five-year) against the study's own three-year 1.025 / two-year 0.890** | **−1.0172 / −0.4622** | −0.6250 / −0.2823 |

**Stacked, sourced corrections only** (risk-free on the AE path, depreciation on the reviewed
half, capital spending at the guided low end, the current island schedule): framing A 6.7735,
framing B 5.8261, midpoint 6.2998, blend **5.2361, −9.7%**. Adding the house escalator ladder
and removing the guidance calibration: 7.1620 / 6.1568, midpoint 6.6594, blend 5.4158,
**−6.6%**.

**Direction of the contested judgements.** The study commits no contested-judgements record
and no diagnostics file — it is on the [R-ENF-05] ratchet — so this count is the reviewer's:
**15 material contested judgements, 13 resolved DOWN and 2 UP** (the beta window and the
terminal-rate reversal), binomial two-sided **p = 0.0074**. Restricting to those worth more
than 5% of the answer they govern: **6, five down and one up**, p = 0.219 by the test and
**5:1 by the count**, which is the number worth seeing whatever the p-value says.

## Conclusion

**The −15.2% is not a disagreement with the market. It is the price of a construction
[R-LENS-03] retired outright.**

Two cash-flow readings of one contested question straddle the price and their midpoint lands
0.04% away from it. The blend then pulls the answer 15% below by weighting in three lenses
that, on this company, are not measuring the business: the **normalised** lens capitalises
flat nominal earnings at a nominal rate — the perpetual real decline that rule names by that
description; the **relative** lens prices a 44%-margin, 23%-return, single-counterparty
franchise partly off US spot land drillers, four of whose six members are loss-making; and
the **book** lens is a historical-cost floor carrying weight, which that rule forbids in
terms.

Three-quarters of the gap is the blend and the last quarter is the discount rate's basis and
the guidance-calibrated segments. Everything that would push the answer FURTHER below the
price — the sanctioned terminal, the beta window, the terminal rate on the net-cash sheet —
is real, is priced above, and is not a defect the market is telling us about; it is the
ordinary width of an honest cash-flow lens on a company whose terminal carries 76% of
enterprise value.

**Two consequences worth stating plainly.** Under [R-GAP-02] the blend is HELD at −15.2%
while a two-sided answer on the class primary would not be held at all — neither branch
breaches — so this study's publication status turns entirely on an architecture the
protocol has retired. And this study is on **sixteen ratchets**; the review does not
substitute for any of them.
