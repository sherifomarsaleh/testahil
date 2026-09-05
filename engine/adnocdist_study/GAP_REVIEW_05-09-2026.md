# ADNOCDIST — gap review [R-GAP-01]

This study publishes **two weighted centres and no single figure**, so both are audited.

**AUDITED CENTRAL: 4.4113** — Frame A, inventory movements normalised to zero from FY2027
**AUDITED CENTRAL: 4.5821** — Frame B, inventory movements carried at the FY2024–FY2025 average
**AUDITED GAP: +14.0%**

Against the latest known close of **AED 4.02 on 3 September 2026**: Frame A **+9.7%**,
inside the band, and Frame B **+14.0%**, outside it. The study was struck against AED 4.07
on 7 August, where Frame B already sat **+12.6%** — **so this review was owed on 9 August
and did not happen, purely because the answer sat at `lenses.centre_A` and `lenses.centre_B`
where the shared reader does not look.** That is now fixed; the invisibility and the defect
below are the same event.

This is an **above-the-price** gap. [R-GAP-01] is two-sided and audits it exactly as it
audits a discount; [R-GAP-02]'s publication block is one-sided and does not hold it. **This
review is therefore the only instrument pointed at this answer,** which is why it hunts for
optimism with the energy the usual case spends on pessimism.

**The verdict is that the premium is OURS.**

---

## 1. LATEST FILINGS

**Clean, with one asymmetry.** The most recent disclosed period is the **reviewed interim
for the six months ended 30 June 2026, Grant Thornton, signed 4 August 2026**; no third
quarter exists on 5 September. Its income statement is fully consumed — the registered
half-year depreciation and amortisation of 369.702 reconciles exactly to the interim's
282,115 + 71,651 + 15,936, which also proves the right column was read. **Its balance sheet
is not consumed at all** (heading 6).

The exclusion of the proposed Shell Downstream South Africa acquisition (announced 7 July
2026, approximately USD 1,000mn of enterprise value) is right and **is** consistently
applied: it was announced after the 30 June sheet, so no revenue, no cost, no value and no
funding debt appear on either side.

## 2. BASE YEAR

**This is where the largest defect lives.** The FY2025 audited statements foot. The
*forecast* base does not rest on a filed full year: commercial volume, fuel transactions and
litres per station are all **the first half of 2026 doubled**, and the growth escalators are
then applied to that half-year as though it were a full one.

Combined with the commercial margin step, the study's FY2026 structural EBITDA of AED
4,648.2mn requires a **second half 9.9% above the reviewed first half's underlying AED
2,214.5mn (USD 603mn)**. The company's own FY2025 second-half-to-first-half seasonality is
**+2.8%**, and its own quarterly disclosure shows **underlying EBITDA of USD 298mn in the
second quarter against USD 305mn in the first** — the structural business decelerated. The
second quarter's headline 44.5% gross-profit growth is inventory: EBITDA less underlying
EBITDA is USD 3mn in Q1 and **USD 180mn in Q2**.

**Inventory movements are not a line in the audited statements.** They appear only in
management commentary and the results presentations, with no reconciliation to the audited
accounts — which the study's own READ FIRST discloses. They are 15% of Frame A's FY2026
EBITDA and they are the entire difference between the two frames.

The load-bearing line is `compute.py:451`, a **+17.0% step** in the structural commercial
margin per litre in FY2026, justified as "the realised first-half outcome". **The realised
first-half outcome is the anchor the step is applied TO** (`margin_comm_h126`), and that
anchor is already 19.2% above the prior year.

## 3. MACRO COHERENCE

**Substantively clean, formally non-conforming.** The house AE path, read live: pegged,
terminal inflation 2.00%, terminal growth at zero real 2.00%, terminal risk-free 3.98%
derived.

The study carries **no study-local inflation array**. The domestic escalator is "about 2% a
year", the currency is pegged so there is no purchasing-power wedge, and fuel is correctly
on its own crude path rather than a domestic index — one escalator per driver class,
properly done, and this is not the [L-048] defect.

Two form breaks. FY2026 uses 2.0% where the ladder publishes 2.5%. And **terminal growth is
a typed nominal 1.5%**, not stored as (real, inflation-path id) as [R-MACRO-01] requires: it
is a **real decline of −0.490% a year**, and the study nowhere writes that number down.

## 4. DISCOUNT RATE

**Every error in this heading runs conservative — that is, against the study's own answer.**

The beta of 0.6494 comes from 257 weekly points against FTSE ADX General, R² 0.179, standard
error 0.087, usable. The number is right, but the record's `index_file` is
`raw_indices/AE/ADXGENERAL.csv`, which the resolver does not register — and that file is
**byte-identical to FADGI.csv**. This is [R-IDX-01] exactly as the digest describes it, with
this study as the worked case: the right number with provenance that cannot resolve.

The schedule is **flat**, which is correct for a peg and is what [R-COC-01] returns, and the
study never tells a reader why. The cost of debt of 5.08% sits above the 4.48% sovereign.
Cash is charged exactly once — net debt is positive, there is no negative weight and no
double add-back.

Two live breaks, **both over-charging**: country risk is **not counted exactly once** — the
study strips the **4bp market** default spread and adds back the **64bp rating** premium,
which it defends explicitly on the ground that stripping 42bp would put the normalised rate
below the matched-tenor Treasury under a hard peg; and the market-value weights exclude the
AED 1,446mn of leases that the bridge deducts as debt.

## 5. TERMINAL

**The retired construction, and correcting it runs the OTHER way.** The terminal carries the
reinvestment identity: terminal return on capital 25%, growth 1.5%, reinvestment 6%, a
charge of AED 261.8mn a year against terminal profit of 4,363.5, and an implied replacement
cycle of **66.7 years — the reciprocal of the growth rate, a fact about the dirham's peg and
not about a fuel-retail network.** It is 74.9% of enterprise value.

The measured-age route is **closed twice over** and no life was invented here: the accounts
depreciate **to a residual value** that is not disclosed, and FY2025 carries a **quantified
change in estimate** — a lower depreciation charge of AED 90,917 thousand, 15.3% of the
year's entire charge, on assets holding two-thirds of net book value. Both are recorded with
the filings' own words in `TERMINAL_EVIDENCE_05-09-2026.md`.

**Bounded instead.** Under `terminal_value.build()`'s form — free cash flow = profit + book
depreciation − maintenance at current cost − growth capital − inflation on working capital —
the published terminal is equivalent to charging maintenance at **1.3594× book
depreciation**, i.e. replacement cost on a base **15.5 years old at 2% inflation**. The
accounts support **10.47 to 12.07 years** (1.2306× to 1.2716×). **So the published terminal
OVER-charges maintenance, and correcting it RAISES the value by AED 0.029 to 0.048.**

[R-TERM-01 CLAUSE TWO CORRECTED] is vindicated on this name: the ratio said the terminal was
optimistic and the arithmetic says the opposite. The bound's assumptions are stated — a
steady-state base (which the evidence file establishes), 2% terminal inflation, replacement
cost scaling as (1+π) over the age, and real growth at or below zero.

## 6. BALANCE SHEET

**Stale by one reviewed period** — [R-BRIDGE-01](i). The bridge stands on 31 December 2025
while the 30 June 2026 sheet sits in the same directory: net debt 2,985.121 → **3,207.684**,
leases 1,446.327 → **1,472.850**, minority 230.374 → **201.770**. Net effect **−AED
0.0176** a share. Leases are deducted as debt and the bridge foots.

The minority is deducted at **book** while the model capitalises 100% of subsidiary cash
flow — [R-BRIDGE-01](ii). Its profit share is 2.001%, worth about AED 1,196mn of equity
value against 230mn deducted.

Book value per share is AED 0.2584, so the price is 15.6 times book — arithmetically right
and economically meaningless on a 98%-payout carve-out.

## 7. CLAIMS AGAINST THE RECORD

**Return on equity of 74.92 / 80.90 / 86.49%, mean 80.77% — recomputes exactly** from
attributable profit over parent equity. It sits on a book that FELL from 3,472 to 2,992 to
3,230, and at a 98.1% implied payout the justified price-to-book and price-to-earnings it
feeds are essentially 1/(cost of equity − growth); the return does almost no work.

**"The harshest reading available" (AED 4.73) is false as it reads.** Two harsher readings
come from the study's own drivers: margins held strictly at the first half of 2026 gives
4.25, and the 15% top-up tax gives 4.51.

**"Grown revenue in each of the three audited years and gross margin in each of them too —
from 16.9% to 19.3%" reverses once the study's own windfall is removed**: ex-inventory,
FY2024 is **16.82% against FY2023's 16.85%** — flat to down, not grown.

**The published volume sensitivity states its base as AED 4.86 when the study's base is
4.78**: the sensitivity rebuilds volume from FY2025 stations times throughput instead of the
half-year anchor the model actually uses, so the reader is shown a base the study does not
hold.

## 8. MULTIPLE CROSS-CHECK

| | EV/EBITDA FY25 | EV/EBITDA FY26E | P/E trailing | P/E forward | yield |
|---|---|---|---|---|---|
| spot 4.02 | 12.83× | 10.15× | 17.95× | 13.25× | 5.12% |
| centre A 4.4113 | 13.97× | 11.05× | 19.69× | 14.54× | 4.66% |
| centre B 4.5821 | 14.47× | 11.45× | 20.46× | 15.10× | 4.49% |
| cash-flow lens A 4.7840 | 15.06× | 11.91× | 21.36× | 15.76× | 4.30% |

Own trailing price-to-earnings ran 19.57 / 20.98 / 18.17. The forward 14.5× *looks* well
inside that, but forward earnings per share (0.303) are 35% above trailing (0.224), **so the
low forward multiple is the FY2026 step, not caution.** On trailing FY2025 EBITDA the two
centres sit at 14.0–14.5× against a market at 12.8×.

**The relative lens is itself the problem.** Its justified forward multiple of 16.32 is
payout × (1+g) / (cost of equity − g) on the *same* growth of 1.5% and the *same* 7.60% as
the cash-flow lens, applied to **FY2026 earnings — the peak year**, higher than FY2027,
FY2028 and FY2029 operating profit and carrying the AED 762mn realised inventory gain. It
was correctly de-circularised on 9 August when the price-derived legs were dropped; it is
still not independent evidence.

---

## What the price implies under this study's own drivers

**The published reverse read is solved against the wrong lens, and correcting it is the
decisive finding.** The study states "the price implies terminal growth of −0.26% against
our +1.50%" — solved through `revalue()`, which returns the **cash-flow lens at 4.7840**,
not the answer the study publishes at 4.4113 / 4.5821. Solved coherently against the
published answer, moving terminal growth through all four lenses as they are actually built,
AED 4.02 implies terminal growth of **+0.746% nominal** (+0.852% at the 4.07 strike).

Against the house AE terminal inflation of 2.00% that is a **real decline of −1.22% a year**
— precisely what a fuel-retail network facing the electric-vehicle drag this study itself
models should be worth. **A reverse read landing on a believable number is evidence against
the dissent**, and the published figure overstates the disagreement because it was solved on
a lens the study does not publish.

## The corrections, priced, in both directions

Each holds every other driver exactly as published; the gap is against AED 4.02.

| | correction | Δ A | Δ B | centre A / B | gap A / B |
|---|---|---|---|---|---|
| — | **published** | — | — | 4.4113 / 4.5821 | +9.7% / +14.0% |
| 1 | both fuel margins per litre anchored strictly on the first half of 2026, then 2% | **−0.2121** | **−0.2121** | 4.1992 / 4.3700 | +4.5% / +8.7% |
| 1b | the step sized to the company's own +2.8% seasonality | −0.0774 | −0.0774 | 4.3339 / 4.5047 | +7.8% / +12.1% |
| 2 | tax at the 15% top-up rate (a risk, not a defect — the half-year filed 10.09%) | −0.1111 | −0.1179 | 4.3002 / 4.4642 | +7.0% / +11.0% |
| 3 | relative lens on FY2027, not the FY2026 inventory-gain peak | −0.1072 | −0.0821 | 4.3041 / 4.5000 | +7.1% / +11.9% |
| 4 | net capital spending at the own realised FY2023–25 rate (387/yr against 166) | −0.0312 | −0.0312 | 4.3801 / 4.5509 | +9.0% / +13.2% |
| 5 | minority at its 2.001% profit share of value, not book | −0.0311 | −0.0336 | 4.3802 / 4.5485 | +9.0% / +13.1% |
| 6 | working capital flat — no crude-driven payables release | −0.0180 | −0.0180 | 4.3933 / 4.5641 | +9.3% / +13.5% |
| 7 | bridge on the reviewed 30 June 2026 sheet | −0.0071 | −0.0071 | 4.4042 / 4.5750 | +9.6% / +13.8% |

**And the corrections this house's own rules require run the OTHER way, which is stated
here rather than discovered later:**

| | correction | Δ A | Δ B |
|---|---|---|---|
| 8 | leases inside the market-value weights (they are debt in the bridge) | +0.0258 | +0.0258 |
| 9 | the sanctioned terminal, maintenance at 1.2306–1.2716× book depreciation | +0.029 / +0.042 | +0.035 / +0.048 |
| 10 | terminal growth 1.5% → the house AE 2.0% (zero real) | +0.1143 | +0.1213 |
| 11 | country risk on ONE basis, either basis | +0.1321 | +0.1389 |
| 12 | **[R-LENS-03]: the class primary IS the central; the blend retired** | **+0.3727** | **+0.5186** |

**A conforming rebuild moves this study FURTHER from the price before any finding above
applies** — the class primary alone is AED 4.7840 / 5.1007, +19.0% / +26.9% — **and that is
not a reason to reconsider the findings.**

Walked in order, one lever at a time, on the items the evidence supports (1, 3, 5, 7):
4.4113 / 4.5821 → 4.0982 / 4.2690 → 3.9878 / 4.1837 → 3.9609 / 4.1543 → 3.9531 / 4.1465,
i.e. −1.7% / +3.1%. On the milder seasonality-calibrated margin item the same stack lands
near 4.24 / 4.42, **+5.5% / +9.9%, inside the band on both frames.**

**Direction of the contested judgements.** The study commits no `contested_judgements`
record and no sign test — it is on the [R-ENF-05] ratchet — so this count is the reviewer's:
resolved UP on value, the commercial margin step, the filed tax rate, guidance-sourced
capital spending, the peak-year relative lens, the full working-capital release, the
minority at book and the stale bridge = **7**; resolved DOWN, the 4bp/64bp sovereign basis,
terminal growth below the house path, the lowest of three earnings-multiple methods and the
blend itself = **4**; one, the inventory judgement, carried both ways, correctly. **7–4,
p = 0.55, no lean.** Reported as a count regardless of the p-value: this is not a study that
took every fork one way.

## Conclusion

**The premium is ours, and the structural point the study does not make about itself is
that all four weighted lenses are the same perpetuity.** The cash-flow terminal, normalised
earnings power, the justified forward earnings multiple and the justified price-to-book
every one sit on growth of 1.5% and the same 7.60%/7.44%. The blend buys no diversification
at all: 100% of the weight rides on one growth-and-discount-rate pair, on top of a
cash-flow model that is 74.9% terminal. The crux says the whole disagreement is the
terminal; the whole *answer* is the terminal, four times over — **which is what lets an 11%
error in the FY2026 base year propagate undamped into the published number.**

**This study is not deliverable at 4.4113 / 4.5821.** The margin anchor and the relative
lens are rebuilt first — both are evidenced from the company's own quarterly disclosure and
between them worth AED 0.08 to 0.32 — and the answer is then re-struck on the latest price.
Nothing here moves a number toward the price: every item is a driver the filings measure
differently from the model.
