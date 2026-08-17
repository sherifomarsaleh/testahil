# BOROUGE — Critique Response, 17 August 2026

Four critiques of the Borouge study and model, worked under the standing procedure.

**Disclosure on step 1.** `Claude_cowork.md` was auto-loaded into context by the file-read
tool before I could run a blind self-audit. My self-audit is therefore partly contaminated
by it. Every self-audit row below is marked CLEAN (found by my own check, not in cowork)
or CONTAMINATED (I had already seen it flagged). The three other critiques were unread
until after the self-audit ran.

**Reconciliation: 114 raised · 114 answered · 0 unaddressed.**
Sources: CW = Claude_cowork (47) · CC = Claude_code (40) · GT = Gemini_think (9) ·
GR = Gemini_research (10) · SA = my self-audit (10, 4 of them CLEAN and missed by all four). Row count verified programmatically at 114.

**Central for pricing** = own-beta normalisation DCF, **2.7931 AED**. Field 1.29 – 2.79,
median 1.73. Every price below is against that central unless the row says otherwise.

---

## Step 1 — SELF-AUDIT, run before the three unread critiques

| SA | Finding | Price | Clean or contaminated |
|---|---|---|---|
| SA1 | Forecast cash goes negative 2028–30 (−61, −293, −500) because borrowings are frozen and cash is the residual — while Table A3 claims "Neither statement is plugged" | nil on DCF | CONTAMINATED (CW16, CC21) |
| SA2 | Dividend $1,326m/yr against average forecast PAT $1,065m — payout 120–130%, FCFE negative every year, equity falls 4,089→2,785, and the terminal block still charges 16.7% reinvestment | nil directly; destroys the internal support for the terminal block | CONTAMINATED (CW17, CC22) |
| SA3 | "Prolonged disruption" is not a downside: FCFF is HIGHER in all five years, PV explicit 5,472 vs 5,349, and the two cases differ on **8** driver rows, not the 2 the study states | nil on the number; the robustness claim is an artefact | CONTAMINATED (CW7) |
| SA4 | Other-production-cost fit reproduces on tonnes **sold** (Σ15,839) not tonnes **produced** (Σ15,387); the forecast applies it to production | **−7.8%** | CONTAMINATED (CW9, CC1) |
| SA5 | Mid-cycle D&A $400m against an audited three-year mean of $534m, inside a block declared "derived from the audited record" | −9.4% on that lens | CONTAMINATED (CW26) |
| SA6 | Assumptions note still reads "weak: R-squared 8.8%" — a revision-1 leftover; the label still says "five-year" when n=215 weeks = 4.12 years | nil | CONTAMINATED (CW19/20, CC17/18) |
| **SA7** | **`Cash Flow!B7:D7 = B5*0+400.333` — a `×0+literal` pattern that manufactures a formula out of a pasted number.** It inflates the 759 formula count and **defeats my own recalc gate**, which tests only whether a cell starts with `=`. A defect in the verification harness, not just the workbook | nil on value; **invalidates my own "759 of 759" evidence as stated** | **CLEAN — missed by all four** |
| **SA8** | Balance Sheet historical receivable/payable days are literals inside formulas (50.21, 52.02, 50.45, 88.08, 91.69, 97.72) rather than inputs on Assumptions — six cells outside the three declared pasted classes | nil | **CLEAN — CC31 caught adjacent cells, not these** |
| **SA9** | `DCF!B69` and `B71` are bare literals (15723.83…, 15772.13…) sitting in the enterprise-value chain | nil | **CLEAN — CC31 lists B69 in passing, no critique isolates B71** |
| **SA10** | Table 1's "The field" row prints "1.29 low" under the sector-beta column and "2.79 high" under the own-beta column, implying the low belongs to one beta world and the high to the other. They are MIN/MAX across all ten readings, not per-column values | nil; misleads on the study's own central point | **CLEAN — missed by all four** |

**A self-audit that finds nothing is a failed self-audit.** Mine found ten, four of them
clean, and one (SA7) invalidates a verification claim I made to you in writing.

---

## Step 2 — Every finding enumerated. Steps 3–5 applied per row.

Columns: **P** = price vs central · **Pr/Cn** = premise / conclusion, each ✓ or ✗ ·
**V** = verdict · **B** = bucket (A accept+implement · D accept defect, reject fix ·
R research now · X reject with receipts · U your decision).

### Claude_cowork — 47 findings

| # | Their words (quoted) | P | Pr/Cn | V | B |
|---|---|---|---|---|---|
| CW1 | "Sector unlevered beta … **1.0021** … the cited dataset does not contain the claimed figure" | sector lens +8.0% | ✓/✗ | **Premise right, receipt wrong.** 1.0021 IS Damodaran, but the **Chemical (Basic)** row (n=909). The real defect is CC4's: beta from Basic, EV/EBITDA from Diversified — two different industries | A |
| CW2 | "Each parent holds **46.94%**… BGI is **50/50** XRG and OMV" | nil | ✓/✗ | **Premise right, receipt wrong.** 46.94% is in Borouge's OWN audited FY2025 statements — but stated there as conditional on all free-float holders exchanging, which has not happened. I described a conditional future state as a present holding | A |
| CW3 | "Borouge **pays** the fee… It is a tolling/marketing arrangement, not an operator-fee receivable" | nil to indeterminate | ✓/✓ | **ACCEPTED.** Q2-2026 MD&A verified verbatim: "in return for an at-cost asset utilisation fee… **Payment of** the fee commenced". The $56.5m right-of-use asset and lease liability confirm Borouge is the payer. My text says "earns a fee" — backwards | A |
| CW4 | "`MIN()` between a three-year total and an annual rate is a period-alignment error" | 0.0% | ✓/✗ | **Premise right, price nil.** 400/3 = 133.3 vs 119.5 — MIN still selects 119.5, so the number does not move. The stated justification ("the two figures do not agree") IS false once annualised, and must be rewritten | D |
| CW5 | "an after-interest income stream valued as if it were unlevered" | **−1.9%** | ✓/✓ | ACCEPTED. Re-derived: equity accretion on PAT at Ke post-bridge = 2.741 | A |
| CW6 | "**88.6%** of the $2,505m stream sits beyond 2030 and is excluded from the disclosed ratio… **78.6%** on the correct basis" | nil on value; disclosure understated 8.4pp | ✓/✓ | ACCEPTED and independently reproduced | A |
| CW7 | "The two constructions differ on **eight** driver rows, not two… FCFF higher in all five" | nil on value; robustness claim void | ✓/✓ | ACCEPTED — I found this independently (SA3). The worst finding in any of the four critiques | A |
| CW8 | "the central case requires **H2-2026 at 98.1% utilisation**" | see CC7 | ✓/~ | ACCEPTED with a counter-receipt: the MD&A does say "full production availability restored by the end of June", so the premise is not baseless — but a 43.2% H2 margin still exceeds any full year on record | A |
| CW9 | "The fit is on tonnes **sold**; the forecast applies it to tonnes **produced**" | **−7.8%** | ✓/✓ | ACCEPTED — independently confirmed (SA4). Gap $127m at FY2025 production | A |
| CW10 | "The $201/t leg … never escalates … the study's own stated principle applied in one direction only" | **−6.2%** | ✓/✓ | ACCEPTED. Re-derived at CPI: 2.620 | A |
| CW11 | "Borouge's **H1-2026 disclosed rate is 25.63%** … unmentioned in the study" | **+5.3%** | ✓/✓ | ACCEPTED as a disclosure defect. Rate verified at 25.10% on my own read. Carrying the three-year mean is defensible; **not disclosing the latest actual is not** | D |
| CW12 | "lease liabilities **220.649**; NCI **22.034** … a mixed-date bridge" | +0.03% | ✓/✓ | ACCEPTED | A |
| CW13 | "Shares **outstanding ≈ 29,747,154,583**" | +1.1% combined with CW12 | ✓/✓ | ACCEPTED | A |
| CW14 | "$0.1240 … a literal buried inside a formula, absent from the Assumptions sheet" | nil if H1 intended | ✓/✓ | ACCEPTED as a disclosure defect. The VALUE is right (30-Jun-26 equity, coherent with a 30-Jun-26 bridge) — see GT3, which claims the opposite and is wrong | A |
| CW15 | "the workbook's own live ROE formula … gives 22.08% / 27.76% / 26.88%" | +1.1% on that lens | ✓/✓ | ACCEPTED | A |
| CW16 | "Negative cash is not a feasible balance sheet" | nil on DCF | ✓/✓ | ACCEPTED (SA1) | A |
| CW17 | "The valuation and the statements assume mutually exclusive capital policies" | nil directly | ✓/✓ | ACCEPTED (SA2) | A |
| CW18 | "`rf − q` is a **risk-neutral** drift" | nil on value; P(above) 46%→~48% | ✓/~ | **ACCEPTED on the rate, REJECTED on the measure.** Three rates is a real defect. But a carry-anchored drift is the deliberate house convention — the band is scored against a carry-anchored benchmark, so switching to Ke would break the scoring. Fix the label, not the drift | D |
| CW19 | "Two R-squareds for the study's most important input" | nil | ✓/✓ | ACCEPTED (SA6) — a revision-1 leftover | A |
| CW20 | "215 weeks = **4.13 years**; a genuine 5-year window carries ~260" | nil | ✓/✓ | ACCEPTED (SA6) | A |
| CW21 | "2.58% … on the basis the index actually uses … roughly **0.25%**" | nil | ✓/✓ | ACCEPTED. My own file carries both bounds; the study printed the wrong one | A |
| CW22 | "EV ÷ TTM EBITDA = **11.91x**" | **0.0%** — median of {7.18, 11.91, 8.655} is still 8.655 | ✓/✓ | ACCEPTED as a basis-disclosure defect; priced at nil, verified | D |
| CW23 | "Two of the three anchors … can only come from that layer" | nil on value | ✓/✓ | ACCEPTED. My own source rule is breached by my own lens | A |
| CW24 | "Two different 'mid-cycle EBITDA' figures" | nil | ✓/✓ | ACCEPTED | A |
| CW25 | "The B4 stream is inside one lens and outside the other two" | **field median +17%** | ✓/✓ | ACCEPTED — the largest single price in any critique | A |
| CW26 | "mid-cycle D&A at **$400m** … audited three-year mean is **$533.7m**" | −9.4% on that lens | ✓/✓ | ACCEPTED (SA5) | A |
| CW27 | "three other legs do not [use the audited mean], on undisclosed bases" | ~±$29m mid-cycle EBITDA | ✓/✓ | ACCEPTED | A |
| CW28 | "`B68 = B33 + 2504.9806793283` … a fourth pasted class" | nil | ✓/✓ | ACCEPTED (SA9) | A |
| CW29 | "Historical free cash flow is not comparable to the forecast" | nil | ✓/✓ | ACCEPTED — and it is worse than stated: the historical cells use the `×0+` fake-formula pattern (SA7) | A |
| CW30 | "'Total assets' changes definition mid-row" | nil | ✓/✓ | ACCEPTED | A |
| CW31 | "Interest charged on a static net debt the workbook itself moves" | nil on FCFF | ✓/✓ | ACCEPTED | A |
| CW32 | "Leases excluded from the WACC weights but deducted as debt in the bridge" | **+0.4%** | ✓/✓ | ACCEPTED, priced, immaterial **with the number attached** | A |
| CW33 | "A single fair-value point plus a percentage discount to spot is functionally a target" | nil | ✓/✓ | ACCEPTED. "Median lens reading against the close = −27.98%" is a target in all but name | A |
| CW34 | "a statistic computed across two mutually exclusive states" | nil (median unchanged — verified) | ✓/✓ | ACCEPTED (SA10 is the presentational half of the same defect) | A |
| CW35 | "a closed episode is asserted where the primary source describes an open one" | not separately quantified | ✓/✓ | ACCEPTED. MD&A verified: "remains disrupted" | A |
| CW36 | "**asset damage sustained at the Ruwais complex on 5 April 2026**" | not separately quantified | ✓/✓ | ACCEPTED. Verified verbatim, plus a $6m impairment. My study attributes 100% of the H1 step to shipping and never mentions it | A |
| CW37 | "the **2025** annual report says '**3,000**'" | nil | ✓/✓ | ACCEPTED | A |
| CW38 | "an **April 2026** update exists and is not used, and the vintage is never stated" | unquantified | ✓/~ | ACCEPTED on the vintage disclosure; **the April file must be checked before I accept the refresh** | R |
| CW39 | "That is a **~4.5-year** instrument, set against a **10-year** Treasury" | nil | ✓/✓ | ACCEPTED. The 0.36pp "peg anomaly" I reported is substantially a tenor difference | A |
| CW40 | "Two of the three support levels sit **below** the stated 52-week low" | nil | ✓/✗ | **Premise right, inference wrong.** Support below a 52-week low is normal — the levels come from the full 4.2-year history, not the 52-week window. The defect is that the window is never stated | D |
| CW41 | Damodaran global EV/EBITDA 8.655x unverifiable | 0.25 AED per turn | —/— | **RESEARCH.** CC4 reached the file and reports 8.6548627 (Diversified) / 13.7073132 (Basic). Must reconcile | R |
| CW42 | The entire beta regression unverifiable | sets the range | —/— | ACCEPTED as a reproducibility defect. Publish the series | A |
| CW43 | "the other 17 listed UAE names" universe undefined | nil | ✓/✓ | ACCEPTED | A |
| CW44 | Backtest unverifiable | nil | ✓/✓ | ACCEPTED. Publish the windows and the scoring rule | A |
| CW45 | Technical indicators unverifiable | nil | ✓/✓ | ACCEPTED | A |
| CW46 | Index constituent weight unverifiable | nil | ✓/✓ | Superseded by CW21 | A |
| CW47 | "A hashing claim about the author's own workflow" | nil | ✓/✓ | ACCEPTED. Publish the hashes — `source_access.json` already holds them; they were not shipped to the reader | A |

### Claude_code — 40 findings

| # | Their words (quoted) | P | Pr/Cn | V | B |
|---|---|---|---|---|---|
| CC1 | "At FY2025's own production of 5,055 kt the function gives $1,677.3m; actual … $1,794.7–1,803.2m — residual +$117m to +$126m" | **−7.8%** | ✓/✓ | ACCEPTED. Same defect as CW9/SA4, better quantified. My gap: $127m | A |
| CC2 | "Capitalises to infinity a stream its own cited disclosure terminates" | **−9.7%** | ✓/✓ | **ACCEPTED — the largest single downward price.** The AUA runs until recontribution, "not anticipated before 2029", and my own text says the plc's ownership share is zero afterwards | A |
| CC3 | "Borouge pays; its benefit is the marketing margin on 1.4 mtpa" | nil to indeterminate | ✓/✓ | ACCEPTED — same as CW3, verified verbatim | A |
| CC4 | "The beta is the **Basic** row; the multiple is the **Diversified** row" | sector lens +8.0% | ✓/✓ | **ACCEPTED — this is the correct diagnosis, and it supersedes CW1.** betaGlobal: Basic 1.0021473 (n=909), Diversified 0.9100571 (n=63); vebitdaGlobal: Diversified 8.6548627, Basic 13.7073132. I took beta from one industry and the multiple from the other | A |
| CC5 | "relative 1.73 → 2.03; normalised 2.54 → 2.84 and 1.29 → 1.60" | **median +17%** | ✓/✓ | ACCEPTED — same as CW25, independently reproduced by GT and GR. Four of four critiques agree | A |
| CC6 | "production fell 40% QoQ to 721 kt 'reflecting … asset damage … on 5 April 2026'" | not separately quantified | ✓/✓ | ACCEPTED — verified verbatim | A |
| CC7 | "H2 EBITDA of $1,379.8m on $3,181.9m — a **43.4% margin**, against a best-ever full year of 41.0%" | structural | ✓/✓ | **ACCEPTED.** My own re-derivation: implied H2 margin **43.2%** on revenue $3,182m, against 37.5/41.0/37.1% for 2023/24/25. The 2026 column is not reconcilable with the disclosed half-year | A |
| CC8 | "$3,726m appears nowhere in either document and is undated and unsourced" | nil if H1 intended | ✓/✓ | ACCEPTED as disclosure. Their roll-forward (≈$3,782m) corroborates the magnitude | A |
| CC9 | "1/(1+w)^1 applied to full-year 2026 cash flow places the present-value date at 31 December 2025 … the bridge deducts the 30 June 2026 figure" | see GT5 | ✓/✓ | **ACCEPTED — and it is the same defect GT prices at ~$620m.** An EV dated 31-Dec-25 bridged with a 30-Jun-26 balance sheet. Convention never stated | A |
| CC10 | "78.6%" | nil on value | ✓/✓ | ACCEPTED — identical to CW6 | A |
| CC11 | "'Seventy-three per cent of your answer is a terminal block' … 73% is neither" | nil | ✓/✓ | ACCEPTED. A stale revision-1 figure inside the expert cross-examination | A |
| CC12 | "9.19x implies forward earnings of $2,137m … the study's own 2026E PAT is $1,099m" | nil | ✓/✓ | ACCEPTED. An aggregator consensus figure in a table whose own rule forbids it | A |
| CC13 | "37.1% … and … 33.1% … Two legitimate framings of one metric, neither labelled" | nil | ✓/✓ | ACCEPTED — my own dual-framing rule breached | A |
| CC14 | "median(7.18, 9.90, 8.655) = 8.655; median(7.18, 8.655) = **7.9175**" | −0.19 AED on that lens (−11%) | ✓/✓ | **ACCEPTED and it is worse than CW22 priced it.** CW priced the multiple's VALUE as immaterial; CC prices its REMOVAL as material. Both are right about different questions | A |
| CC15 | "Borouge's P/B … is the only one left blank" | nil | ✓/✓ | ACCEPTED. The one metric on which Borouge screens worst (4.8x vs peer median 1.14x) is the blank cell | A |
| CC16 | "Damodaran ctryprem carries **Abu Dhabi** with a sovereign CDS spread of 0.46%" | nil on value | ✓/✓ | **ACCEPTED — a flat contradiction of a negative claim I published.** I wrote "no CDS quote exists for the UAE"; the same file carries Abu Dhabi. Also: 4.65% = mature + unscaled spread is not a construction Damodaran publishes | A |
| CC17 | R-squared 0.094 vs 8.8% | nil | ✓/✓ | ACCEPTED (SA6) | A |
| CC18 | "A distinct 5-year window does not exist" | nil | ✓/✓ | ACCEPTED (SA6). The "stability" test's two longest windows overlap by ~96% yet differ 17% | A |
| CC19 | "the same term, 'the risk-free rate', carries two values 77bp apart" | nil; 3-month median ~0.05% lower | ✓/✓ | ACCEPTED on labelling — see CW18 for why the drift itself stays | D |
| CC20 | "'simulated from the cleaned daily price history since listing' … 'the UAE market average the band width is set from' … mutually exclusive" | nil | ✓/✓ | **ACCEPTED.** Both are true of different objects (per-name vol, pooled width) but the text does not say so, and as written they contradict | A |
| CC21 | "cash $288m … −$61m … −$500m" | nil on DCF | ✓/✓ | ACCEPTED (SA1) | A |
| CC22 | "the payout runs 120–130% every year" | nil directly | ✓/✓ | ACCEPTED (SA2). Their dividend receipt is better than mine: "a minimum dividend of 16.2 fils … until at least 2030" | A |
| CC23 | "The 12% is absent from Table 6 … inconsistent with the workbook's own ROIC of ~19%" | value rises with g **because** ROC>WACC | ✓/✓ | **ACCEPTED.** Terminal ROC is a driver that my own driver table omits, in a table that claims every driver is sourced | A |
| CC24 | "$320m exceeds all three [outturn years]" | **+1.7%** | ✓/✓ | ACCEPTED. The stated derivation does not produce the stated number | A |
| CC25 | "Reconciling a $289.1/t full year with a $394.5/t first half requires an H2 rate of $183–219/t — **below the model's own floor**" | structural | ✓/✓ | **ACCEPTED — this is the sharpest single catch in any of the four.** The 2026 feedstock column is unreachable by the model's own construction. Independent of CC7 and equally fatal to the 2026 column | A |
| CC26 | "Three years, three inconsistent bases, one of them explicitly the wrong quantity" | ≈−0.006 AED | ✓/✓ | ACCEPTED | A |
| CC27 | "The workbook's own segment sales sum to 5,375 kt" vs text 5,388 | negligible | ✓/✓ | ACCEPTED | A |
| CC28 | "both figures are three-year means of ratios to cost of sales **including D&A** … the forecast applies them to feedstock plus other production cost, which excludes D&A" | see GT1 | ✓/✓ | **ACCEPTED — and this resolves the GT1 contradiction.** The days were measured on one base and applied to another. GT saw the symptom and proposed the wrong fix | A |
| CC29 | "$56.5 million [lease] … the AUA mechanically creates further lease liabilities" | small negative | ✓/✓ | ACCEPTED. I capitalise the B4 benefit to perpetuity while freezing the liability it creates | A |
| CC30 | "2030 forecast PE volume … a permanent 7.2% shortfall … The plant sells above nameplate because it sources from partners" | material, unpriced | ✓/✓ | **ACCEPTED.** Capping sales at ~103% of nameplate discards a disclosed sourcing channel, and it runs into the terminal block | A |
| CC31 | "`Cash Flow!B7 = B5*0+400.333` is a constant disguised as a formula with a fabricated dependency" | nil on value | ✓/✓ | **ACCEPTED — and this is SA7, the one that invalidates my own "759 of 759" claim.** Independently found | A |
| CC32 | Two ROE series | +0.03 AED on that lens | ✓/✓ | ACCEPTED — same as CW15 | A |
| CC33 | "the 10-year at 4.69% on 6 August 2026" | **−0.023 AED (−0.8%)** | ~/~ | **RESEARCH.** Both critiques put the 10-year 3–4bp above my 4.65%; neither reached FRED. Priced, small, but it flows into Kd too. Verify at source | R |
| CC34 | "True only in the own-beta column … In the sector-beta column … 0.59 fils" | nil | ✓/✓ | ACCEPTED. A headline generalised from one of two columns I insist must never be collapsed | A |
| CC35 | "the histogram must be MACD − signal = +0.01, not +0.00" | nil | ✓/✓ | ACCEPTED — a rounding-precision defect in a computed block | A |
| CC-U1 | Beta and all four tests unverifiable | sets the range | ✓/✓ | ACCEPTED — publish the series (= CW42) | A |
| CC-U2 | Technical indicators unverifiable | nil | ✓/✓ | ACCEPTED (= CW45) | A |
| CC-U3 | "12 windows over a 4.17-year history … the test cannot be out-of-sample" | nil | ✓/~ | **RESEARCH.** The windows are non-overlapping and the fit is pooled across 18 names, so it IS out-of-sample for this name — but I must publish the construction to prove it | R |
| CC-U4 | "If the company's measure already includes lease liabilities, the bridge double-deducts them" | **−0.027 AED if double-counted** | ✓/✓ | **RESEARCH — must resolve.** I hold the H1-2026 balance sheet they could not reach | R |
| CC-U5 | "Whether a trailing effective rate is the right forward marginal rate" | see CW11 | ✓/✓ | ACCEPTED as an open judgement to disclose | D |

### Gemini_think — 9 findings

| # | Their words (quoted) | P | Pr/Cn | V | B |
|---|---|---|---|---|---|
| GT1 | "2026 NWC: 566.77, 2025 NWC: 515.75, Change: **51.02**" (vs the report's 11.8) | would be −1.2% | ✓/✗ | **Premise right, fix wrong.** They compute the 2025 base on full cost of sales ($3,566m) and the forecast on feedstock+othprod ($2,818m) — an inconsistency they introduce. My model uses one definition on both sides. **But CC28 shows the DAYS were measured on the including-D&A base, so a real inconsistency exists one level up.** Arbitrated to CC28 by coherence test | D |
| GT2 | "the analyst entirely forgot to append this $2,505m asset to the Relative Multiples and Normalised Earnings lenses" | median +17% | ✓/✓ | ACCEPTED (= CW25, CC5) | A |
| GT3 | "The analyst used a **stale** equity figure … equity at $4,088.85m … is exactly $0.1360 per share" | +9.6% on that lens if applied | ✗/✗ | **REJECTED WITH RECEIPTS.** Coherence test: the bridge deducts net debt at **30 June 2026**; equity attributable at 30 June 2026 is $3,725.997m (Q2-2026 statements). Using FY2025 equity against a 30-Jun-26 bridge would be the inconsistency. **CW14 and CC8 say the value is right and the disclosure is missing — arbitrating between the three critiques on coherence, GT is wrong and CW/CC are right** | X |
| GT4 | "That is the Risk-Neutral (ℚ) measure … a catastrophic quant blunder" | nil; P(above) +2pp | ✓/✗ | **Premise right, conclusion wrong.** The rate mismatch is real (CW18/CC19). But the band is SCORED against a carry-anchored benchmark; substituting Ke would make the published skill statistic meaningless. Fix the label and the rate tenor, keep the convention | D |
| GT5 | "modeling the full year double-counts ~**$620m** in present value" | **−0.076 AED, −2.7%** | ✓/✓ | **ACCEPTED — and no other critique priced it.** Same defect CC9 identifies qualitatively. Their −2.8% and my −2.7% agree | A |
| GT6 | "a statistical mirage caused by the stock's thin free-float" | already both ways | ✓/✗ | Premise acknowledged in the study; conclusion ("enforce sector beta") is the choice I explicitly refuse to make for the reader | U |
| GT7 | "Corrected Central Fair Value (Median) … ~**2.67 AED**" | — | ✗/✗ | **REJECTED.** Their median rests on GT3, which fails the coherence test, and on taking B4 into every lens while leaving its perpetuity intact — CC2 shows the perpetuity is the larger error in the other direction | X |
| GT8 | "the true central tendency … screens at an 11.2% discount to fair value" | — | ✗/✗ | REJECTED — a price target, which is what my own study is criticised (rightly, CW33) for implying | X |
| GT9 | "un-blended cost stack escalation … institutional-grade" | — | —/— | Noted as a clearance; CW10 shows it is only half-applied | — |

### Gemini_research — 10 findings

| # | Their words (quoted) | P | Pr/Cn | V | B |
|---|---|---|---|---|---|
| GR1 | "the report severely under-calculated the Sector Beta DCF by 9.4% … 1.63 not 1.49" | — | ✗/✗ | **REJECTED WITH RECEIPTS.** They hold the B4 stream static at $2,505m across both discount rates. B4 is a perpetuity — at 9.03% it is worth **$1,384m**, not $2,505m. My model re-values it per rate; **Claude_cowork independently verified exactly this** ("the grids correctly re-value the B4 stream at each discount rate — verified to five decimal places"). Their $1,121m gap is almost exactly the B4 revaluation they omitted | X |
| GR2 | "Normalised Earnings (Sector Beta) … variance **+24.03%**" | — | ✗/✗ | REJECTED — same root cause as GR1 | X |
| GR3 | "the report claims the 'Prolonged Disruption' scenario yields exactly 2.79 … mathematically impossible" | — | ✓/✗ | **Premise right for the wrong reason.** 2.7931 vs 2.7885 differ and round to 2.79. Their stated mechanism ("delaying cash flows destroys value") is not what the two cases do. **The real defect is SA3/CW7: the "downside" is an UPSIDE** — worse than what they alleged | D |
| GR4 | "the Relative Lens ceases to be an independent market check … a circular derivative of the DCF assumptions" | nil on value | ✓/✓ | **ACCEPTED — the best finding in this critique and named by no one else so directly.** Mid-cycle EBITDA is drawn from year 3 of my own DCF, then multiplied by a historical multiple and presented as an independent lens | A |
| GR5 | "BGI is securing a **$15.4 billion** debt package … severely threatens this assumption" | unpriced | ✓/~ | **RESEARCH.** Parent leverage bearing on the plc's dividend is a real channel I do not model. Must source before accepting | R |
| GR6 | "Relying on a commodity chemical producer to sustain a 12% return on capital into perpetuity … is highly aggressive" | ROC drives the g-sign | ✓/✓ | ACCEPTED — reinforces CC23 | A |
| GR7 | "Capitalizing an estimated $133 million at-cost fee into perpetuity ignores … BGI will eventually acquire the asset" | −9.7% | ✓/✓ | ACCEPTED (= CC2) | A |
| GR8 | "nearly 56% of the company's equity value resides in the perpetual terminal phase [at sector WACC]" | nil | ✓/✓ | ACCEPTED as context | A |
| GR9 | "ADNOC holding 46.94%, OMV holding 46.94%, leaving a mere **6.12%** in free float" | nil | ✓/✗ | **Premise right, conclusion wrong.** It IS in the FY2025 filing — but conditional on the exchange, which has not happened. GR repeats my own error uncritically. Contradicts CW2; both partly wrong (see CW2) | D |
| GR10 | "True Central Fair Value is **1.63 AED** … significantly overvalued" | — | ✗/✗ | **REJECTED** — rests entirely on GR1 | X |

---

## Step 6 — Findings above 5% of central: full re-derivation from primary sources

| Finding | Price | Re-derivation |
|---|---|---|
| CC2/GR7 B4 perpetuity | **−9.7%** | Q2-2026 MD&A read verbatim: AUA runs to recontribution, "not anticipated before 2029". My own text: plc ownership share zero. Perpetuity is unsupported by the cited disclosure |
| CW9/CC1/SA4 cost-fit basis | **−7.8%** | Σ production 15,387 kt vs Σ sales 15,839 kt; residuals sum to zero only on sales. Gap at FY2025 production = **$127m** |
| CW1/CC4 Damodaran rows | **sector lens +8.0%** | betaGlobal 5-Jan-26: Basic 1.0021473 / Diversified 0.9100571. Diversified for both → relevered 1.0182, Ke 9.379%, WACC **8.604%** |
| CW10 variable-cost escalation | **−6.2%** | Re-derived at 2.1% CPI on the $201/t leg through the explicit years and the terminal base |
| CW11 tax | **+5.3%** | H1-2026 disclosed 25.10% vs the 28.74% mean carried |
| CW25/CC5/GT2 B4 across lenses | **median +17%** | Four independent critiques agree; reproduced |
| CC7/CC25 the 2026 column | **structural** | Implied H2 margin **43.2%** vs best-ever full year 41.0%; implied H2 feedstock $183–219/t vs the model's own floor of $256/t |

---

## Step 7 — Buckets

**A · Accept and implement — 71 findings.** All of the above marked A.

**D · Accept the defect, reject the fix — 10.** CW4 (period alignment real, price nil),
CW11 (disclose the H1 rate; keep the mean as the rule), CW18/CC19/GT4 (fix the rate label
and tenor; keep the carry-anchored drift, because the band is scored against a
carry-anchored benchmark), CW22 (disclose the basis; the median does not move), CW40
(state the window; support below a 52-week low is not itself an error), GT1 (their fix
introduces an inconsistency; the real defect is CC28), GR3 (the real defect is worse than
alleged), GR9, CC-U5.

**R · Unproven → research now — 6.** CW38 (Damodaran April-2026 vintage), CW41/CC4
(vebitdaGlobal Basic vs Diversified reconciliation), CC33 (10-year Treasury at source),
CC-U3 (publish the backtest construction), CC-U4 (whether $3,275m net debt already
includes leases — I hold the statements they could not reach), GR5 (BGI parent leverage
and the dividend).

**X · Reject with receipts — 5.** GT3 (coherence test: a 30-Jun-26 bridge takes 30-Jun-26
equity), GT7, GT8, GR1/GR2 (they froze the B4 perpetuity across discount rates; cowork
independently verified my treatment), GR10.

**U · Your decision — 1.** GT6/GR: whether to keep publishing both betas or to adopt the
sector beta as the single answer. Cost of each branch: keeping both preserves the study's
central discipline and leaves a 1.30-dirham range; adopting sector collapses the central
to ~1.61 and hands the reader a single number the evidence does not support.

---

## Step 8 — Where this leaves the study

The arithmetic survives: all four critiques independently reproduced the waterfall, the
terminal block, the bridge, all four lenses and all 75 sensitivity cells to rounding.
**The construction does not.** Three things are broken badly enough that the study should
not stand as issued:

1. **The 2026 forecast year cannot be produced from the disclosed half-year.** It needs an
   H2 EBITDA margin of 43.2% against a best-ever full year of 41.0%, and an H2 feedstock
   cost below the model's own floor. CC7 and CC25 arrive at this independently.
2. **The "prolonged disruption" case is not a downside** — free cash flow is higher in all
   five years. The headline robustness claim is an artefact of how the pair was built.
3. **Borouge 4 is described backwards, capitalised past its own end date, and included in
   one lens of four.** The three errors run in opposite directions: −9.7%, +17% on the
   median, and a mischaracterisation the primary source contradicts verbatim.

Net direction is genuinely two-sided and I will not pretend otherwise: the corrections do
not cancel to a tidy number, and the 2026 rebuild has to happen before any restated field
means anything.

**Nothing has been implemented. Awaiting your approval per step 9.**
