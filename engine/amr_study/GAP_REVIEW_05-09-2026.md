# AMR — gap review [R-GAP-01]

**AUDITED CENTRAL: 2.1455**
**AUDITED GAP: -10.2%**

AED 2.1455 a share (USD 0.5842075319 at the 3.6725 peg) against the latest known close of
**AED 2.39 on 3 September 2026** — 10.2% below. The study was struck against AED 2.23 on
7 August, where it sat 3.8% below and owed no review; **the breach was created by the
price, not by the model** (the shares are up 7.2% and the study has not moved), which is
[R-GAP-01 AMENDED]'s stale-spot case exactly.

Written because the answer was invisible until tonight: the study carried its central at
`lenses.central` and its spot at `meta.spot`, and the shared reader looks for `central`
and `spot` at the top level, so [R-GAP-01] could say nothing about this study at all.

**The verdict is that the gap is OURS, and the single highest-confidence correction closes
36% of it and clears the publication block on its own.** It is architecture and one
unsourced escalator, not a missed filing and not a market disagreement.

---

## 1. LATEST FILINGS

**Clean, and the best-swept heading in the study.** The most recent disclosed period is the
**reviewed condensed consolidated interim statements for the six months ended 30 June 2026,
review report by Deloitte & Touche (M.E.) LLP dated 28 July 2026.** Every line the study
registers reconciles to the filing to the thousand: revenue 1,364,520 · cost of revenues
598,498 · selling and marketing 479,601 · general and administrative 109,239 · operating
profit 184,120 · profit before tax 171,084 · tax 24,101 · attributable 147,221. The
second-quarter stand-alone column (714,784) is read; the half-year release is read (like-
for-like 6.3%, free cash flow USD 160.0mn, 2,746 restaurants, the 120–130 net-new guidance,
the interim dividend of USD 100.8mn); the investor pack is read (delivery 52% of sales,
capital cost per store USD 402k, three-year payback). Nothing later exists — the third
quarter ends 30 September. **This heading contributes nothing to the gap.**

## 2. BASE YEAR

**Foots exactly.** The FY2025 audited statements (page 10) give revenue 2,508,821 · cost of
revenues 1,143,928 · selling and marketing 886,102 · general and administrative 202,562 ·
other income 13,361 · hyperinflation (1,052) · impairment (5,559) · operating profit
282,728, and every one matches the register. Nothing in the base year is annualised or
solved.

**One scaled figure, and it is named here because the study's own log names it rather than
its document.** The first forecast year is a 50/50 average of two constructions — a unit
build (2,760.4) and an H1-scaled run rate (2,813.0, being half-year revenue divided by the
prior year's first-half share of 48.508%) — adopted at 2,786.7. That is a scale and it is
recorded as one.

## 3. MACRO COHERENCE

**The largest defect in the study: two inflation paths in one model, running in opposite
directions.** This is a dollar-reporting operator in twelve countries. The house paths, read
live: AE terminal inflation 2.0% on a ladder of 2.5/2.0/2.0/2.0/2.0; US 2.2% on
3.2/2.1/2.2/2.2/2.2.

The study carries an inflation-class input of its own, which is what [R-MACRO-01 AMENDED]
closes:

| side | path | layer | the study's own note |
|---|---|---|---|
| cost — `wage_growth` | **6.0% flat, five years** | House estimate | *"deliberately above Gulf CPI"* |
| revenue — `lfl_path` | 5.5 → 4.5 → 4.0 → 3.7 → 3.5% | House estimate | *"converges toward the roughly 2% long-run inflation the IMF projects"* |

**The cost escalator exceeds the revenue escalator in every year and the wedge widens from
0.5 to 2.5 points.** That is [L-048] verbatim: costs escalated at one rate, prices converged
to another, and the manufactured margin decline then reported as a finding.

Three things make it a defect rather than a judgement. The 6% is a **two-year CAGR of two
opposite years** — wage per full-time equivalent ran USD 10,959 (FY2023) → 11,042 (FY2024,
**+0.76%**) → 12,393 (FY2025, **+12.22%**) — and this protocol's own rule is that the
average of two opposite regimes was true in neither. The stated reason is a **mix effect,
not inflation** ("because the mix shifts toward delivery-capable and above-restaurant
staff"), a level change that does not compound for ever, and the study **already models
that mix separately** through staff per store falling 12.05 → 11.25. And the interim
discloses no staff cost, so there is no near-term reviewed anchor to outrank the stale
full-year rate.

**The terminal risk-free rate is QUOTED, not DERIVED.** The study takes today's ten-year
Treasury par yield of 4.65% less the US default spread of 0.22%, rounds to 4.45% and holds
it flat. [R-MACRO-01] requires terminal risk-free = terminal inflation + the real-rate
convention, derived and never quoted: 4.18% on the US path, 3.98% on the AE path.

**Terminal growth is clean**: 3.0% = 2.0% AE inflation + a **stated** 1.0% real, matching the
house path to the basis point. It is not a real-terms decline.

The Egypt currency drag of 2.5% is a house estimate that **the study's own document
contradicts in the same paragraph** — *"the two most recent disclosed readings ran the other
way (Egypt dollar revenue +29% in FY2025, +23% in H1 2026)"*. That is the [R-ANCHOR-01]
shape: a mechanism the company's own filings measure in the opposite direction.

## 4. DISCOUNT RATE

**Clean. Cash is charged exactly once.** The model discounts at a rate weighted on the
**gross** lease liability (637.466) against market capitalisation, giving a debt weight of
11.111% and an equity weight of 88.889% — market-value equity weights, a positive debt
weight, no negative-weight or levered-above-one pathology. The bridge then deducts **net**
debt (gross lease less cash and deposits). Value the firm at a blended rate on the gross
structure, deduct the debt, add the cash once: [R-BRIDGE-01](iii) is satisfied.

Country risk enters once — the risk-free is normalised by the **US** default spread
(4.65 − 0.22 = 4.43%) and the country premium sits inside a revenue-weighted twelve-country
equity risk premium of 6.2010%, which reproduces exactly. The cost of debt of 6.72% sits
above the Abu Dhabi sovereign of about 4.90%, as required. The beta of 0.9299 is regressed
against **FTSE ADX General, the registered ADX regressor**, and attests as conforming — not
the DFM interim. Its R² is 8.4% and its standard error 0.412, so the 90% interval runs
0.252 to 1.608; that weakness matters for the reverse read below and is stated rather than
buried.

## 5. TERMINAL

**On the [R-TERM-01] ratchet, and not a source of this gap.** The measured-age route is
closed by [L-328] condition (i) — the charge is struck to a residual value the accounts do
not disclose — and is documented in `TERMINAL_EVIDENCE_05-09-2026.md`; no life was invented
here.

The charge was priced instead, from the model's own numbers. Terminal profit after tax is
459.77; book depreciation 402.36; the implied gross capital charge is **459.45, being
1.142× book depreciation**; working capital releases 11.12; terminal free cash flow is
413.80, a net reinvestment of **10.0% of profit**. Against the last explicit year, which
charges 455.47 against depreciation of 390.64 — **1.166×**, a net reinvestment of 9.06% —
while adding 120 net stores, 3.7% more units.

**So the terminal charges 98% of the investment intensity of a year expanding the estate by
3.7%, to buy 1% real growth.** [R-TERM-01 CLAUSE TWO]'s under-charging inference requires a
charge BELOW book depreciation; this one is 14% above it, and the census puts this terminal
**+34.2% above its own floor** against ARCC's +6.4%. Aligning the terminal reinvestment rate
to the explicit window's own 9.06% is worth **+0.009 AED**. The construction is wrong and
the number it produces is worth almost nothing.

**What IS a live breach in this heading is the window, not the terminal.** The final explicit
year grows at **7.05%** against a 3.0% terminal — a 4.05-point gap against [R-MACRO-01]'s
two-point requirement — with **74.2% of enterprise value in the terminal.** The window ends
four points above the rate it capitalises. The direction is upward and it needs a rebuild;
no price is faked for it here.

## 6. BALANCE SHEET

**A real [R-BRIDGE-01](i) breach, and it WIDENS the gap.** The company's own note 19
net-debt reconciliation gives **(220,056)** at 31 December 2025 and **(258,449)** at 30 June
2026. The bridge uses the December sheet while the reviewed June sheet is registered in the
study's own input file.

The study's defence is coherent and explicit: it values equity at 31 December 2025 and rolls
219 days forward to the 7 August anchor at the cost of equity, net of the USD 201.6mn
dividend paid in the window. That is a legitimate alternative construction. **The rule says
the LATEST disclosed sheet**, and substituting it costs **−0.0125 AED**.

The minority is deducted at book (0.984) rather than at a value share — immaterial here, and
the minority's profit share is negative. The USD 100.8mn interim dividend declared 28 July,
before the 7 August anchor, is excluded from the roll; including it would cost a further
**−0.044 AED**. **Both bridge items run against the study.**

## 7. CLAIMS AGAINST THE RECORD

**One attribution names the smaller of two drivers.** The document says *"the margin peaks
near 25.4% and eases as the delivery channel grows."* Tested by holding each driver flat:

| | FY2026 → FY2030 EBITDA margin |
|---|---|
| as published | 25.40 → 24.90 (−0.49pp) |
| delivery share held flat at 52% | 25.40 → 25.54 (+0.14pp) → delivery is worth **−0.63pp** |
| wage growth at 3.5%, delivery still rising | 25.82 → 26.96 (+1.14pp) → the wage wedge is worth **−1.63pp** |

The delivery channel is real. **The wage escalator moves the margin trajectory 2.6 times as
much, and the delivered document does not name it anywhere in the margin explanation.**

**One is a self-contradiction the study states out loud.** Of the book lens it writes: *"It
is the lowest of the four lenses and carries the lowest weight. It is reported because
leaving out the lens that disagrees would be dishonest, **not because it is informative**."*
It then weights that lens at **10%** of the published central. [R-LENS-03]: book value is a
disclosed FLOOR, published as such and **never weighted**.

Company-sourced claims ("largest restaurant operator across MENA and Kazakhstan"; "the
region's first concurrent dual listing") are the company's own and stand. The beta history
claim recomputes correctly. The cone record is disclosed honestly.

## 8. MULTIPLE CROSS-CHECK

| | enterprise value (USDmn) | EV/EBITDA FY25 | EV/EBITDA FY26E | P/E FY25 | P/E FY26E | yield |
|---|---|---|---|---|---|---|
| published central 2.1455 | 5,127 | **8.61×** | 7.24× | 22.4× | 16.7× | 4.11% |
| cash-flow lens alone 2.2333 | 5,327 | 8.94× | 7.53× | 23.3× | 17.4× | 3.95% |
| **market 2.39** | 5,686 | **9.55×** | 8.03× | 24.9× | 18.6× | 3.69% |
| global quick-service peer median | | **16.87×** | | 18.76× trailing | | |

**At AED 2.39 the market pays 9.55 times trailing enterprise value to EBITDA — 43% below the
global peer median — for a business compounding revenue at 7.7%, running 25% EBITDA margins
and 41–49% returns on invested capital, and paying a 3.7% yield.** This is not an exuberant
price, and "the market is over-optimistic" is not available as an explanation of a discount
when both parties already sit 40% below the peer set.

The study's own relative lens adopts **8.5×** — *below the market's own 9.55×* — on the
stated ground that "Americana is the operator, not the brand owner." **Its own peer table
contradicts that reason**: the franchisee-operators run HIGHER than the franchisors (Devyani
33.3×, Sapphire 27.6×, Jubilant 23.1× against Yum 17.6×, Domino's 16.2×, Restaurant Brands
14.3×). A cross-check anchored below the market it is meant to check, carrying 20% of the
answer.

---

## What the price implies under this study's own drivers

Solved one driver at a time, everything else at its published value:

| driver | the price implies | the study publishes | credible? |
|---|---|---|---|
| wage escalator | **4.80%** | 6.00% | **yes** — and more conservative than the house AE path of 2.0% |
| beta | **0.8544** | 0.9299 | **yes** — 0.18 standard errors away, deep inside our own 90% interval |
| terminal growth | 3.648% (2.0% inflation + 1.65% real) | 3.0% (2.0% + 1.0%) | plausible; ours is better defended |
| terminal return on capital | 138.8% | 30% | **no** — the company's own is 49% |

Three of the four land on believable numbers and two on numbers this model cannot
distinguish from its own published values. Per [R-GAP-02], **a reverse read landing on a
believable number is evidence against dissent**, and there is no dissent to file here.

## The corrections, priced, in both directions

Gap to close: 0.2445 AED. Every move holds every other driver exactly as published.

| | correction | rule | central after | Δ AED | share of the gap |
|---|---|---|---|---|---|
| 1 | like-for-like anchored on the filed half-year actual of 6.3% rather than guidance | [R-FCAL-01] guidance is scored, never consumed | 2.3123 | **+0.1668** | 68% |
| 2 | wage escalator 6.0% → 4.0% (US terminal 2.2% + 1.8% real) | [R-MACRO-01] | 2.3112 | **+0.1657** | 68% |
| 3 | **retire the four-lens blend; the class primary IS the central** | **[R-LENS-03]** | **2.2333** | **+0.0878** | **36%** |
| 4 | terminal risk-free derived, not quoted (3.98% AE / 4.18% US) | [R-MACRO-01] | 2.2256 / 2.1903 | +0.0801 / +0.0448 | 33% / 18% |
| 5 | terminal return on capital 30% → the model-implied 49.35% | judgement | 2.1847 | +0.0392 | 16% |
| 6 | Egypt currency drag 2.5% → 0 (own filings: +29%, +23% in dollars) | [R-ANCHOR-01] | 2.1740 | +0.0285 | 12% |
| 7 | terminal reinvestment 10.0% → the window's own 9.06% | [R-TERM-01] | 2.1548 | +0.0093 | 4% |
| — | explicit window extended to within two points of terminal | [R-MACRO-01] | rebuild | upward | unpriced |

**And the ones that run the other way, reported because a one-sided hunt is the failure this
review exists to prevent:**

| | correction | central after | Δ AED |
|---|---|---|---|
| 8 | staff per store held flat at the FY2025 12.12 (the productivity gain is unsourced) | 2.0274 | **−0.1181** |
| 9 | FY2026 net new stores 125 → 0 (the half-year actual was **−3**: 2,749 → 2,746) | 2.0625 | **−0.0830** |
| 10 | bridge onto the 30 June 2026 sheet | 2.1330 | −0.0125 |
| 11 | market-value weights re-struck at 2.39 | 2.1397 | −0.0058 |

**Direction of the contested judgements.** On [R-ENF-05]'s five-per-cent bar there are four:
margin structural-over-cyclical (up), staff productivity (up), the wage escalator (down),
like-for-like (down) — **2 up, 2 down, p = 1.00, no lean.** Below the bar it leans down 5 to
2. This study is not uniformly pessimistic in its judgements, and the two largest UPWARD
resolutions are the two resting on unsourced or guidance inputs. AMR carries no committed
reverse read and no sign test; it is on the [R-ENF-05] ratchet and this review is not a
substitute for one.

## Conclusion

**The gap is ours.** The published central is a weighted blend at typed weights
(50/20/20/10), the construction [R-LENS-03] retired outright, and 10% of it sits on a book
lens the study's own document calls "not informative" and 53% below the primary. Applying
the standing rule and nothing else gives **AED 2.2333, a gap of −6.6%, inside the block** —
no new research, no judgement, no driver touched.

Beneath that the study carries its own inflation path and it runs against its own price
path, worth 1.63 points of margin trajectory and 0.08 to 0.17 AED; and the terminal
risk-free is quoted where the rule requires it derived.

**Nothing here is a reason to move a number toward the price**, and the corrections that run
the other way — the June bridge, the re-struck weights, the unsourced productivity path, a
half-year that added minus three stores — belong in the same edition as the ones above. A
rebuild that took only the upward ones would be fitting.
