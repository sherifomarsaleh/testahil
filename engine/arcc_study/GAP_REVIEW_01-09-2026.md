# ARCC — gap review, 1 September 2026

**Written because [R-GAP-01] required it, and it changed the answer.** When this review was
opened the central fair value was **EGP 52.90 against a latest known close of EGP 59.00 —
10.3% below**, which trips the rule. Auditing the answer rather than re-walking the process
found **four further defects**, three of them in the valuation itself. Corrected, the central
is **EGP 54.10, 8.3% below the price**, which no longer breaches.

**That is the rule working, not the rule being escaped.** The threshold is a trigger for an
audit, not a target; the review is kept and published because the defects it found are real
and would otherwise have shipped.

## What the audit found, beyond the eight headings

**1. THE SENSITIVITY BLOCK WAS RUNNING A DIFFERENT MODEL FROM THE HEADLINE.** `reval()`, the
function every sensitivity and every contested judgement in the study is computed through,
discounted the terminal value at the LAST EXPLICIT YEAR'S MID-YEAR factor while the headline
used the END-OF-WINDOW factor. Called with nothing changed it returned **57.27 against a
headline of 55.21** — so every alternative in the study was quoted on a basis **3.7% more
generous** than the number it was being compared against. That is [L-016], one document and
two models, hiding inside the block whose entire job is to test the first one. It is fixed,
and an assertion now requires the function to reproduce the headline when nothing is changed.
**That assertion caught a second instance on its first run**, when the new other-income line
was added to the headline and not to the sensitivity rebuild.

**2. THE CAPEX ANCHOR'S REASONING WAS BACKWARDS.** Maintenance capital was set at USD 4.00
per tonne of capacity on the stated grounds that FY2024 (USD 3.70/t) and FY2025 (USD 3.23/t)
"both carry the alternative-fuel and silo programmes, so the maintenance level is set at the
middle of that band". If both observations INCLUDE growth capital they are an UPPER BOUND on
maintenance — so the maintenance level belongs at or below them, and USD 4.00 sits ABOVE
both. The H1-2026 cash-flow statement settles the direction: it splits six months' spending
into **PP&E purchases of EGP 102.9mn and assets under construction of EGP 505.5mn**, so 83%
of it is the growth programme and the sustaining line is running near USD 0.8/t annualised.
That is a deferral rather than a sustainable rate, so the input is not cut to it; it is reset
to the most recent full year's TOTAL spending per tonne, **USD 3.23**, which remains an upper
bound and is still above the industry sustaining norm of about USD 3/t. Worth **+0.84** on the
central.

**3. THE COST OF DEBT WAS A EURO COUPON INSIDE A POUND DISCOUNT RATE.** 91.1% of the debt
book is euro-denominated at Euribor-linked rates, and the study adopted the CONTRACTED
blended 7.89% while offering the pound-equivalent 13.36% as an alternative — the standing
rule the wrong way round, which is explicit that FX debt is carried at local-equivalent cost
and never as a raw FX coupon in a local-nominal WACC. A 7.89% cost of debt sitting beside a
28.28% cost of equity in the same pound WACC is a currency mismatch, not a cheap borrowing.
The pound-equivalent is now adopted. Worth **−0.06**, and made because it is right rather
than because it moves the answer.

**4. A DISCLOSED REVENUE LINE WAS REGISTERED AND CONSUMED BY NOTHING.** The audited accounts
carry other income of EGP 53.340mn in FY2025 (note 7), of which EGP 32.643mn is export
subsidy — **0.856% of that year's export revenue, a DISCLOSED rate**. The model registered
the line, quoted it, and let no line consume it, which is [L-018] exactly. It is now carried:
the subsidy at its disclosed rate on each year's own export revenue, plus the non-subsidy
remainder escalated. Worth **+0.42**. The separate EGP 467.813mn collected in H1-2026 is 14x
the whole of FY2025's subsidy inside one quarter, reads as accumulated claims, and is left in
the cash balance — but its scale is now **priced as a scenario rather than caveated**: at 2%
of export revenue the cash-flow lens is 58.25, at 5% 59.95 and at 8% 61.65.

## Where the answer came from, computed leg by leg

Each leg is measured on the lens it actually moves: net cash enters all four lenses, so the
bridge moves the weighted central by exactly its per-share change; beta, capex, the cost of
debt and other income enter the cash-flow lens only, so each moves the central by its effect
there times that lens's 50% weight.

| change | effect on the central |
|---|---|
| beta re-derived through the sanctioned route — the composite is withdrawn | **−4.27** |
| the bridge moved onto the disclosed 30-June balance sheet | **−3.44** |
| the reviewed half-year, calibrated into price, cost and services together | **+5.95** |
| the capex anchor, whose reasoning was backwards | **+0.84** |
| the disclosed other-income line, previously consumed by nothing | **+0.42** |
| the pound-equivalent cost of debt | **−0.06** |
| net, from EGP 54.65 | **−0.55** |

**The largest single cause is still the beta**, and it is a correction of this house's own
method rather than a view about the company. That is set out under DISCOUNT RATE below.

## 1 · LATEST FILINGS — every disclosed period actually read

**128 primary documents** were retrieved from the company's own investor-relations archive at
`arabiancementcompany.com`, and every attempt is logged including the failures
(`engine/arcc_walkforward/fetch_attempts.json`). The archive lists 175 PDFs; the 47 not
fetched are Arabic-language duplicates and parent-only (standalone) filings, recorded as seen
and deliberately not used, because the study values the consolidated group and mixing the two
bases inside one panel would be an undeclared break.

**The most recent disclosed period is the condensed consolidated interim financial statements
for the six months ended 30 June 2026**, limited review by Wafik, Ramy & Partners (Deloitte),
**created 13 August 2026**. It is READ AND CONSUMED: the income statement, the balance sheet,
the cash-flow statement, note 3 (sales, split local/export and goods/services), note 29 (the
export subsidy) and note 30 (significant events, including the February 2026 rate cut to 19%).

**A point of fairness to the previous edition:** that filing did not exist when the previous
edition was struck. Its valuation date was 6 August 2026 and the interim accounts were filed a
week later. This is NEW INFORMATION, not a source that was skipped — the failure mode
[R-GAP-01] was adopted from (reviewed statements sitting unopened in the company's own
archive) is not what happened here.

Also read and in the panel: the reviewed Q1-2026 interim accounts (25 May 2026), the audited
FY2025 accounts (Deloitte, signed 25 February 2026), and **every annual filing back to
FY2015**, whose comparative column carries FY2014 — twelve fiscal years, all tier A.

**Nothing disclosed is unread.**

## 2 · BASE YEAR — what is filed, and what is annualised

**FY2025 is filed and the build reproduces it.** The unit build — kiln utilisation, the
clinker factor and two export shares — reproduces audited FY2025 revenue to **+0.000%** and
audited EBITDA to **+0.000%**, and every disclosed tonne to within 0.012%. Nothing in the base
year is solved out of a profit line.

**FY2026 IS ANNUALISED, and it is named as such.** It is built by grossing the reviewed half
up to a full year:

| line | reviewed half | half-year share used | FY2026E |
|---|---|---|---|
| revenue | 6,080.578 | 45.55% (median of three) | 13,349 |
| cost of sales | 3,619.040 | 46.08% (median of three) | 7,854 |
| general and administration | 225.745 | 44.20% | 511 |

**The share is the assumption, and it is measured rather than assumed.** How much of a year
ARCC's first half is has been **44.19% (FY2025), 45.55% (FY2022) and 52.69% (FY2023)** — it is
NOT stable. The median is used. Grossing up on FY2025 alone would have given FY2026 revenue of
13,703mn and rested a 12.7% lift on a single year; an earlier cut of this revision did exactly
that, reached a central of EGP 61.15, and was wrong to. The full range is published: 11,540mn
on the least favourable share, 13,761mn on the most favourable, 12,161mn on simply doubling.

**Price, cost and services were calibrated TOGETHER on the same half.** Calibrating the price
leg alone would have manufactured a margin out of the calibration — which is [L-009] and
[L-110] — and this name's own walk-forward warned about it from a second direction: gross
profit's macro share came back NEGATIVE (−0.058), meaning the revenue and cost errors were
cancelling and repairing one leg alone breaks the cancellation. The resulting FY2026 EBITDA
margin of 39.0% reproduces what the half implies to within half a point, and that is asserted
in code rather than asserted in prose.

## 3 · MACRO COHERENCE — inflation, currency and price are one path

| year | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---|---|---|---|---|
| cost inflation | 11.5% | 10.0% | 9.0% | 8.0% | 7.0% |
| local cement price | 8.0% | 9.0% | 8.0% | 7.0% | 6.5% |
| EGP/USD | 50.6 | 53.1 | 55.8 | 58.6 | 61.5 |
| export price, USD | −3.2% | −2.5% | −1.8% | −1.7% | −1.8% |

**Local price grows BELOW cost inflation in every year** — a real price decline, which is the
intended reading and not an accident: the market carries about 76Mt of nameplate capacity
against roughly 54Mt of consumption, and the production quota that supported price was
abolished in May 2025. **The currency path runs 2.7% to 4.9% a year of depreciation** against
7–11.5% domestic inflation, i.e. slightly less than strict purchasing-power parity would give;
that is a real-appreciation assumption on a post-stabilisation currency and it is disclosed
rather than buried. **Export prices fall in dollars** on global clinker oversupply, so in
pounds they grow about 2% a year — slower than local prices, which is why the mix shift the
half-year shows is margin-positive.

**There is no third path.** The one inflation number drives the cost stack, the local price
path and G&A; the one currency path drives the export price and the euro debt; there is no
place in the model where two different inflations meet, which is the AMOC defect this heading
exists to catch.

## 4 · DISCOUNT RATE — the right rate, and cash charged for exactly once

**Cash is charged for ONCE.** The debt weight is **GROSS** — debt of 1,135.1mn over debt plus
market capitalisation, **4.88%, positive**. There is no negative debt weight, no equity weight
above one, and no operating rate pushed above the cost of equity. The cash balance is then
added once, at face, in the bridge. This is the AMOC defect and it is not present.

| | |
|---|---|
| local 10-year government yield | 22.95% |
| less Egypt's own CDS-implied default spread | −3.40% |
| **normalised risk-free rate** | **19.55%** |
| beta (tier 2, peer median) | 0.9275 |
| **cost of equity** | **28.28%** |
| cost of debt, blended (91.1% euro) | 7.89%, 6.12% after tax |
| **operating discount rate** | **27.20%** |
| terminal rate | 16.46% |

**Country risk is counted once**: the risk-free rate is normalised by the sovereign's own
default spread before a country-loaded equity risk premium is added back ([L-004]).

**THE BETA IS THE LARGEST SINGLE CAUSE OF THIS GAP AND IT IS A CORRECTION, NOT A VIEW.**
Earlier editions carried 0.6281, described as a passing own-stock regression. That regression
was **against an equal-weight composite of the other Egyptian names this house covers**, not
against the EGX30. SIGCM clause 6 calls a constituent composite a HARD FAIL and not a tier,
for a reason visible here: a basket of covered names explains a covered name better precisely
because it partly consists of companies like it, so the better R-squared was the artefact
rather than the evidence.

Re-derived through `beta_regression.own_stock_beta()` against the EGX30 — the only conforming
regressor for an EGX listing — ARCC returns **beta 0.698 on an R-squared of 0.047**, below the
5% usability floor. Tier 1 is therefore unavailable, and the protocol's answer is not to keep
the number: it is tier 2, a same-country peer beta. The peer set was named before it was
measured — Lecico 0.815, Egypt Aluminium 0.919, Orascom Construction 0.936, Egyptian Chemical
Industries 1.030 — and the median, **0.9275**, is adopted. Sinai Cement, the closest business
match, fails the same gate more badly (R-squared 0.025) and is reported rather than used.

**What could not be done, and which way it cuts.** Peer leverage is not sourced, so the
unlever-and-re-lever step was not performed and the peers' equity betas are used as published.
ARCC holds net cash and its peers carry debt, so completing that step **could only LOWER the
beta and RAISE the value**. The adopted figure is the conservative end of tier 2, the gap is
flagged, and the whole peer spread is published as a sensitivity. **The discount rate is
therefore more likely too high than too low, which cuts against the gap rather than for it.**

## 5 · TERMINAL — growth coherent with the inflation inside the terminal rate

Terminal growth is **5.0%** against a terminal risk-free rate of **10.50%**, which is built as
the central bank's longest-dated published inflation target (**5.0%**, Q4-2028) plus a
standard emerging-market real rate of about 5.5 points. **Terminal growth is therefore 0.0% in
real terms** — neither the perpetual real DECLINE that was the AMOC defect, nor perpetual real
growth nothing disclosed supports.

Terminal value is **48.8% of enterprise value**, below half and lower than the previous
edition's 51.8%.

The growth lever is tested on the analytic condition rather than the textbook shortcut: the
sign turns on **N/IC against W/(1+W)**, which is **9.58% against 14.13%** — growth DESTROYS
value here, and the model destroys it, a spread of **−17.2%** from 3% to 7% terminal growth.
That is material and it is published rather than smoothed, because the terminal denominator is
replacement cost rather than a 2010-vintage book.

## 6 · BALANCE SHEET — the bridge stands on the latest disclosed one

**It does, and this is the heading that moved the answer.**

| | EGP mn |
|---|---|
| cash and bank balances, reviewed 30 June 2026 | 1,970.501 |
| less interest-bearing debt (borrowings 761.098 + current portion 269.115 + credit facilities 253.075) | −1,283.288 |
| **net cash** | **687.213** |
| less non-controlling interests, reviewed 30 June 2026 | −0.216 |

Trade and notes payable, creditors and other credit balances and current tax liabilities are
**excluded by construction** — they bear no interest, and dividing a finance charge by them is
the trap [R-FCAL-01] §3 names first.

**The previous edition had no balance sheet for its valuation date and had to roll one
forward**: FY2025 cash, plus stub free cash flow, plus stub treasury income, less the declared
dividend, netted against the Q1-2026 debt. That gave net cash of 1,974mn — **EGP 1,173mn, or
EGP 3.44 per share, too generous**. It could not have been otherwise: a roll-forward cannot
see a 698.6mn inventory build, an 832.8mn rise in debtors, or 608.4mn of capital spending in
six months. The valuation date moves to 30 June 2026 so that the bridge and the explicit
window meet at the same instant. The roll-forward is retained in the workbook as a labelled
memo, so a reader can see the size of what it missed.

## 7 · CLAIMS AGAINST THE RECORD — every superlative recomputed

Every "best", "never", "highest" and "first" in the delivered document was scanned for and
recomputed against the filings.

**"the best year the industry has had in more than a decade" — TRUE, and now measured on
twelve years rather than three.** ARCC's own audited gross margin across the whole sourced
window: 29.2% (FY2014), 24.4%, 29.6%, 14.3%, 13.7%, 6.7%, **1.0% (FY2020)**, 6.8%, 18.9%,
21.2%, 23.9%, **40.6% (FY2025)**. FY2025 is the highest of the twelve and the next best is
29.6% in FY2016. The claim stands and is now checkable.

**"audited profit up 210% in a single year on a 42.6% revenue step" — recomputed and correct.**
3,599.586 / 1,160.129 − 1 = 210.3%; 12,447.320 / 8,729.783 − 1 = 42.6%.

**ONE CLAIM WAS STALE AND HAS BEEN REPLACED.** The previous edition's caveats said "the
forecast is well below the first-quarter run rate… the first quarter of 2026 ran a 42.9% gross
margin". The half-year accounts now show the SECOND quarter ran **38.1%** and the half **40.5%**
— so the first quarter was the better one, not the run rate. The caveat is removed and
replaced by the three that are actually live: the half-to-year gross-up, the price-versus-
volume split that no interim tonnage can resolve, and the export subsidy.

## 8 · MULTIPLE CROSS-CHECK — what the fair value implies

| | at the central EGP 54.10 | at the market EGP 59.00 |
|---|---|---|
| equity value, EGP mn | 19,831 | 22,117 |
| enterprise value, EGP mn | 19,144 | 21,430 |
| EV / FY2026E EBITDA | **3.67x** | 4.11x |
| price / FY2026E earnings | **5.21x** | 5.81x |
| EV per annual tonne of capacity | **USD 76.1** | USD 85.2 |
| replacement cost per annual tonne | USD 130 | USD 130 |

**Nothing here is implausible and nothing here is generous.** An Egyptian industrial at 3.7x
forward EBITDA and 5.2x forward earnings is at the low end of a market that trades roughly
4–6x and 5–8x, which is what a 10% discount to the traded price should look like. The asset
lens is the one that disagrees — at USD 95 per annual tonne it gives EGP 65.57, above the
price — and its disagreement is the most informative fact in the study rather than an
inconvenience: the market is paying 65% of replacement cost for a plant, which is what a
market with 12.6Mt of dormant capacity under restart study ought to do.

---

## Conclusion

**The answer does not change, and one defect was found.** The defect is the beta: earlier
editions carried a figure measured against a composite of covered names, which SIGCM calls a
hard fail, and correcting it costs EGP 5.35 of the central on its own — nearly the whole EGP 6.10 gap
between the fair value and the price. That is a correction of this house's own method, not a
discovery about the company.

Two of the eight headings moved a number: BALANCE SHEET (−3.44 per share, the roll-forward
superseded by the disclosed balance sheet) and CLAIMS AGAINST THE RECORD (one stale caveat
removed). One heading moved a number the other way and is the reason the gap is not larger:
BASE YEAR, where the reviewed half is worth +5.95 per share once price, cost and services are
calibrated together.

**The remaining discount is a conclusion, not a residual.** At EGP 54.10 the market is paying
4.11x forward EBITDA for a plant at 65% of replacement cost in a market carrying 40% surplus
capacity, and this study's cost of equity of 28.28% rests on a beta borrowed from peers
because the share's own history cannot carry one. Both of those are stated in the delivered
document in the reader's own words.
