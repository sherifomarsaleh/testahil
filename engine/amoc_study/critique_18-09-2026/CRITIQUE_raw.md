# Forensic Verification Audit — AMOC Valuation Study

**Subject:** Alexandria Mineral Oils Company S.A.E. (EGX: AMOC) — *Testahil Independent Valuation Study*, fair value EGP 11.40 against a stated price of EGP 13.50
**Package audited:** `01_valuation_study.docx` (500 paragraphs) · `02_valuation_model.xlsx` (16 sheets, 6,069 formulas) · `03_bibliography.docx` (source register)
**Audit date:** 18 September 2026
**Method:** Independent Python replica of the workbook's full formula chain, rebuilt from the Assumptions input cells only. The replica reproduces the published answer to the last cell (**EGP 11.4012** vs 11.40), which allowed every published claim to be tested against a working engine rather than against prose.

---

## Section A — Audit Scope

Audited: the valuation study, the workbook and the source register in full.

**Reachable primary sources: none.** No filing, exchange disclosure, Damodaran country file or bond quote could be opened from this environment, so every INPUT-plane test is run against the study's own source register and against internal arithmetic; external verdicts are logged UNVERIFIABLE rather than asserted.

What *could* be done exhaustively is rebuild the engine: all ~40 driver cells, the per-line cost build, the five-year waterfall, the discount glide, the terminal block, the enterprise-to-equity bridge, all six sensitivity grids (30 points) and every adversarial give-back row were recomputed independently from the Assumptions sheet alone. Findings are therefore concentrated on the **LOGIC**, **CONSTRUCTION** and **DISCLOSURE** planes, where the evidence sits inside the package itself.

**Not checked:** the daily price series (vendor file not supplied), the beta regression, the Monte Carlo engine (50 pasted cells, zero formulas), and the two exchange budgets the study names as unreachable.

**Materiality threshold:** ±3% of the headline (±EGP 0.34 a share), per the audit standard.

---

## Section B — Fail Table

| # | Location | Item | Plane | Sev | What the report says | What is correct (recomputed) | Why it failed | Impact on fair value | Correct method |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Assumptions B122–126 vs B167–171; DCF C31/C35 | Two inflation paths inside one income statement | Construction / Disclosure | **TOTAL** | §1.4: "realisation grows on one path"; no escalator is published anywhere | Realisation growth = (1 + Egyptian inflation) / **1.025** − 1, to six decimals, in all five years. Operating expense and capex take the **full** inflation index. Revenue CAGR 6.20% vs opex CAGR 8.86% | An undisclosed 2.5%-a-year real wedge between the two sides of the income statement. Opex/revenue drifts 3.795% → 4.189%; at parity it is a constant 3.703%. The model manufactures a 39bp operating-margin decline out of the escalator mismatch alone. Invisible on the gross line because cost of sales rides the *same* index as revenue | **+17.8% → EGP 13.44** | Publish the escalator. One inflation path per driver class; if realisations are held flat in USD under PPP, say so, and put Egyptian salaries (49.8% of the conversion stack) on the Egyptian index, not the product index |
| 2 | READ FIRST box, Headline box, §1.14 | "a REDUCTION of −0.93%" | Logic | **TOTAL** | "10.58% … against a base year of 9.65% — that is a REDUCTION of −0.93%, not an increase"; "requires a margin BELOW what this company has just reported" | 10.58 − 9.65 = **+0.93pp — an increase**. My model inversion: +0.926pp shift → margins 10.61–10.66% → value exactly 13.5000 | Sign reversed on the study's own subtraction, then built into the headline conclusion ("the burden of proof sits with the seller"). Appears in three places on the delivered page | Reverses the headline's direction of proof | State it as an increase over the adopted base year, or invert against 12.43% and show that arithmetic |
| 3 | Table 7, Table 18, Headline box | Employees' profit-share give-back | Logic | **TOTAL** | 11.69 (+2.5%); "ALL OF THE ABOVE AT ONCE" 12.74 (−5.7% vs price) | Re-run of the workbook engine with the profit-share rate set to zero: **12.0632** (+0.66). All six concessions simultaneously: **12.4855** (−7.5% vs price) | The published row understates the concession by EGP 0.37 (3.3% of the central); the all-at-once row *over*states by EGP 0.25 and reconciles to no combination I can construct. Neither figure exists in the workbook — Table 18 is pasted from an external script | ±3.3%; the "12.74" headline is wrong | Re-run the stack inside the workbook, as the sensitivity grids already are |
| 4 | Table 3, Table 7, Table A.2, §1.3 | Balance-sheet date | Disclosure | **TOTAL** | "the balance sheet at **31 December 2025**, as filed"; "EGP 997mn **at 31-Dec-2025**"; "EGP 258mn **at 31-Dec-2025**"; Table A.2 column headed "Filed 31-Dec-2025" | The register dates every one of these at **30 June 2026**, and states the 31-Dec-2025 values itself: parent equity 4,790.7 (not 6,070.3), cash 2,463.5 (not 3,018.4), dividends payable 517.25 (not 258.3) | The model is **right** — it correctly stands on the latest reviewed balance sheet. The delivered page mis-dates it by six months. A reader opening the audited transition-period statements to check Table 3 finds none of these numbers | 0% on value; destroys the audit trail | Re-date the page to 30-Jun-2026, and fix the one genuinely stale row (B91, fixed assets at cost, still 31-Dec-2025 beside a 30-Jun-2026 net book) |
| 5 | Bibliography "What changed"; Assumptions E35; Income Statement!A2 | The evidence claim | Disclosure | **TOTAL** | Study §1.2 / §7: "BOTH HALVES ARE FILED … the reviewed statements settle it". Register: the H1-2026 disclosure "**is a press release, not a filing** … its gross-profit line is **REJECTED** … and **SOLVED** from its own profit line". The workbook repeats this in two places | Cannot both be true. The Assumptions cells (nine-significant-figure line items, note references, "limited review report attached") indicate the reviewed statements *are* held and the register is stale | Prime Directive 2: a package that misstates which document it holds has made a false claim about its own evidence. Compounded by a register paragraph whose coherence test now returns "**+0.0%** above the profit printed in the same release, **so it is rejected**" — the test confirms and the text still rejects. Three different values (12.6% / 0.0% / "right to 0.03%") for one test in one package | 0% direct | Rewrite the register to the current edition; delete the retired solve machinery (Income Statement rows 6–11) |
| 6 | Table 20 vs Table 22 | The band record | Disclosure | **TOTAL** | T20: **57** resolved forecasts, **49 of 57 (86.0%)** inside the 90% band, band width **1.225x — "wider, not narrower"**. T22: **17** windows, **94.1%**, width **0.969x — "marginally NARROWER"** | Workbook Monte Carlo B18–B23: **17** windows, coverage 52.94 / 88.24 / 94.12%. Table 22 reproduces exactly. Table 20 reproduces nothing; "49 of 57" is uncomputable from the package (17 scored + 40 dropped = 57) | Two mutually exclusive track records for one object on facing pages, including a **reversed direction** on band width. Table 20's caption doubles down on the wrong one | Not valuation; destroys the calibration claim | Publish the 17 scored windows only, with the 40 drops stated |
| 7 | Table 21, Table 24 | Probabilities labelled against the wrong price | Disclosure | **TOTAL** | "Above EGP **13.50 (the traded price)** — 3.3%"; touch ladder "13.50 … 0.0% / 5.0%" | The cone is anchored at **EGP 9.10** (MC!B6; verified — the 1-month median 9.170973 = 9.10·e^(carry/12) exactly). The traded price *is* 13.50 | The study publishes a 3.3% probability that the price exceeds a level it currently sits at, and a 0.0% one-month touch probability for a level already touched. §3's "two clocks" note explains the anchor, but the tables are still labelled with the live price | Not valuation; the zone table is unusable as printed | Re-anchor the cone on the pricing date, or label every zone against 9.10 |
| 8 | Masthead, Table 23 | Price date | Input / Disclosure | **TOTAL** | "Valuation study as of **6 August 2026**"; Table 23: "last close EGP 13.50 — **6 August 2026**" | Register B7: price 13.50, date **2026-09-03**, "closing price … 3 September 2026". The 6-Aug close was **9.10** | Two different closes published for one date. Every fundamental input is dated 30-Jun-2026 or earlier; the price is four weeks younger and **+48%**. The study's entire posture ("sits well below the market price") is generated by that gap, not by the analysis — against the 6-Aug close, EGP 11.40 is **+25% above** the price | Reverses the sign of the headline gap | One valuation date, one price, stated once |
| 9 | §1.13 and Appendix B.3 | Rating-basis alternative | Logic | **TOTAL** | "On the RATING-BASIS premium the explicit rate is 30.61% and the cash-flow lens is EGP 9.22" | An explicit Ke of 30.61% implies ERP 12.886%; that ERP gives **EGP 10.99**. To reach 9.22 by ERP alone needs 30.0% (Ke 46.15%); holding 30.61%, you need a terminal ERP near 10.7%, which the study does not publish | The stated rate and the stated value cannot come from the same re-run. Quoted twice as a key adversarial result; 9.22 is 16% below the reproducible figure | Understates a published alternative by ~19% | Re-run and publish both anchors under the rating basis |
| 10 | Table C.2 | Expert 2 waterfall does not foot | Disclosure | **TOTAL** | 6,035 + 6,028, "less the disclosed claims carried in the bridge **(1,255)**", EQUITY VALUE **12,063**, EGP **9.34** | 6,035 + 6,028 = 12,063 exactly — **the (1,255) row is printed and not taken**. Taking it: 10,808 → EGP **8.37** | Pass 9 read literally: the printed operations do not reach the printed answer. C.4 then asserts "Both are deducted: EGP 1,255mn, or EGP 0.97 a share" — the page claims a deduction its own table did not make | Expert 2 overstated by EGP 0.97 (10.4%) | Foot the table or delete the row |
| 11 | Table C.3, C.5, C.7 | Expert 3 capital basis and reconciliation | Construction | **TOTAL** | "Arithmetically it **must reconcile to the primary lens** on the same inputs"; C.4 concedes that objection as true; panel median **12.32**, −8.8% vs price | Expert 3 runs on **net-book** invested capital (IC 4,677; EP = NOPAT − WACC × opening net-book IC reproduces 882 / 1,179 / 1,316 / 1,418 / 1,493 **exactly**, PV 3,337.8 = "3,338"). The primary lens's terminal runs on **gross** capital. EV 13,536 vs 12,853 — it does **not** reconcile, gap 683 (5.3%). And 13,536 walked through the study's own bridge gives EGP **11.91**, not 12.32 | §1.9 declares "One view is now applied across the model"; three views are in fact printed (terminal 30.3% gross, Table A.3 memo 42.3% net, Expert 3 wholly net). The panel median — the study's second headline — rests on the unreconciled lens and on a per-share that does not walk | Panel median overstated ~3.4%; the identity claim is false | Put every lens on one capital basis, or stop claiming the identity |
| 12 | C.4 / C.5 / C.7 | Panel median after its own concession | Construction | **TOTAL** | C.4 CONCEDES Expert 1 is undiscounted and worth **8.10, not 14.50**; C.7 then prints E1 at 14.50 and the panel median at **12.32 (−8.8%)** | Median of (8.10, 9.34, 12.32) = **9.34**, i.e. **−30.8%** vs price | The headline panel number is the median of a set containing a figure the study has already withdrawn two pages earlier | Panel read moves −8.8% → −30.8% | Publish the median of the discounted set |
| 13 | §5, §7 vs Bibliography sources table | The capital budget | Disclosure / Completeness | **TOTAL** | §7: "A board-approved FY2025/26 capital-expenditure budget … **could not be opened**"; worth "roughly −12% at face" | Register lists it as obtained: "**EGP 580.19mn** … Zawya/Reuters; Egypt Oil & Gas … **the anchor for the capital-expenditure driver**". The model's capex is not anchored on it at all (maintenance = base-year depreciation 156.6, escalated → 182 in 2026E) | Three-way contradiction: the study says unreachable, the register says obtained and used, the model uses neither. The study quantifies the impact of a document it says it does not have | −12% if the budget is right | Resolve, and state which |
| 14 | Bibliography, "Negative results" | Self-contradicting table | Disclosure | **TOTAL** | Row 1: audited statements "**NOT REACHED** … refused connection". Row 3: "THE AUDITED FINANCIAL STATEMENTS THEMSELVES … **REACHED**" | Both rows sit in the same table. Also "A disclosed NCI balance … **NOT FOUND**" (three are in the register); "depreciation, capex, PP&E … **NOT FOUND as disclosed lines** … depreciation is set as a share of revenue and PP&E is the residual" (all three are read off note 6 and both cash-flow statements) | The negative-results register — the one artefact whose job is to record what is missing — describes a different study | 0% direct | Rebuild for this edition |
| 15 | Table 2, Segments B5/C5, register | Period label on the product table | Disclosure | PARTIAL | "Tonnes, **6M**" / "Value, EGP 6M"; "note 14-A of the **audited transition-period** statements"; register: "1,502,325 tonnes for EGP 46,959mn **for the transition half**" | Assumptions B67–B82 state these are the **twelve** months to 30-Jun-2026 — audited half **plus reviewed** half. EGP 46,959mn is the 12-month revenue (= B10 + B12) | The figures are right; three separate labels are wrong, and half the table comes from a *reviewed* statement while attributed to an *audited* one. "Realisation per tonne is disclosed arithmetic" is a 12-month blend, not a note reading | 0% | Re-label; state the audited/reviewed split |
| 16 | Workbook: FV!C13, DCF C48:G48, DCF B13/B17, Summary B6–D9 | Dead cells behind live claims | Construction | PARTIAL | Summary!A2 "**Nothing on this sheet is typed**"; register "every input was **perturbed in place** … to confirm it moves the headline in the asserted direction"; "96.0% live" | Book-lens cost of equity is the constant `0.2285092330`; the five glide fractions are constants; the tax rate in both cost-of-debt cells is the constant `0.22118761296853667`; the bear/bull columns are pasted (Summary!A23 says so, contradicting A2 on the same sheet) | Perturbing beta does not move the book lens; perturbing the cost-of-debt path does not move the glide and therefore does not move the headline at all — the asserted perturbation test cannot have passed on those inputs | 0% base case; the liveness claim is overstated | Point the cells at their drivers |
| 17 | Table 18, row 5 | "Effective instead of statutory tax" | Logic | PARTIAL | **11.40** (−15.5%) — zero movement | Re-run at 22.11876%: **11.4601** (+0.06) | A give-back row that moves the valuation by exactly nothing is the signature of an unread input — the precise defect §1.3 says the new reachability gate now catches | +0.5% | Re-run |
| 18 | Table 10; Table 3 note; B.3 | "Weighted" cost of capital | Disclosure | PARTIAL | Equity weight 99.90% / debt 0.10%, "WEIGHTED COST OF CAPITAL 27.45% … at that debt weight it IS the cost of equity to three decimals"; "the net-cash position pushing the operating rate **ABOVE** the cost of equity" | DCF!B14 = `=B10` — no weighting occurs; B11–B13 are computed and explicitly "not used". A true weighted value would be 27.4398% (1.4bp below, not "three decimals"). The operating rate **equals** the cost of equity; "above" is true only of the **retired** construction | The page presents a weighting the model does not perform, and states as a present property of the adopted construction something true only of the rejected one | ~0.01% | Say "cost of equity, unlevered"; drop the weights |
| 19 | §5 vs Table 6 / §1.2 | Filed margin spread | Disclosure | PARTIAL | §5: "the filed record spans **514 basis points**"; Table 6 and §1.2: "a spread of **737 basis points**" | 12.43 − 5.05 = 738bp | Same quantity, two numbers, same document | 0% | One figure |
| 20 | §1.8, IS!B42/B43 | Maintenance capex "built" | Disclosure | PARTIAL | "maintenance at gross asset cost over the **implied 17.5-year life**" | B42 = cost ÷ depreciation = 17.4996; B43 = cost ÷ B42 ≡ **depreciation**. Algebraically, maintenance capex = base-year depreciation, escalated. Two tautologies presented as a derivation. No **disclosed** useful life is cited anywhere | Pass 4 requires a disclosed life with citation; a life defined as cost ÷ depreciation cannot be tested. Implied terminal replacement cycle is 1/g = **14.3 years** against the model's own 17.5 | ~0% base case | Cite the accounting-policies note; reconcile 14.3 vs 17.5 |
| 21 | §1.9, DCF!A53 | "REPLACEMENT cost" | Construction | PARTIAL | Terminal return "struck on invested capital at **REPLACEMENT cost** — working capital plus the asset base at **GROSS cost**", giving 30.3% | Historical **gross book** cost (2,741mn, on a register 67.4% written down) in an economy that has run 20–30% inflation. Replacement cost is far higher; the derived intensity is EGP 2,100 per annual tonne, roughly a tenth of a refinery's real build cost | Understating invested capital overstates terminal ROIC, understates required reinvestment (g ÷ ROIC) and **overstates** terminal value — the one material judgement running the other way. On net book: 44.3% ROIC → EGP 11.91 | +4.5% if net book | Call it gross historical cost, or index it |
| 22 | Table 15 volume row; terminal-growth row | Grid labels and base point | Disclosure | PARTIAL | "Volume growth path, **as a multiple** of the assumed path"; "every row reproduces the base case **at its own base point**" (column headed "base") | The workbook feeds DCF!$B$6 "volume growth **added** a year": −6 / −3 / 0 / +3 / +6 **percentage points**. And the terminal-growth row's base case (7% → 11.40) sits in the **high** column, not the "base" column | Both are the exact defects §1.11 says the new gate eliminated ("a volume row whose label described a different scenario from the one it ran"; "a beta row whose centre did not return the base case") | 0% | Fix the labels |
| 23 | Table 13 vs register | Minority rate | Input | PARTIAL | "**2.963%** of the WHOLE enterprise" | Register: "Minority interest inferred at 3.0% against a **disclosed 4.645%**", listed among assumptions "overturned by the filings"; and elsewhere "NOT FOUND. **Held at 4.6%**". The 2.963% is correctly computed (12-month NCI ÷ PAT-ex-interest); 4.645% is the audited half over group PAT. Unreconciled | Also struck **ex** interest income but applied to a **cash-inclusive** enterprise value; the consistent ratio is 2.687% | −1.8% at 4.645%; 0.3% for the ex-interest mismatch | Reconcile the two publicly |
| 24 | Bibliography sources table | Aggregators cited for filed line items | Input | PARTIAL | "Company financial summary pages \| **stockanalysis.com; Investing.com; TradingView** \| Shares outstanding, market capitalisation, **total assets, total liabilities, cash and equivalents, total debt**, dividend per share" | All exist in the statements the study says it holds; Table A.2 prints total assets 11,405 and total liabilities 5,262 | Prime Directive 1 — citing an aggregator for a line item that exists in a filing is a finding even when the number is right. The register also defines the entire "Company" layer as figures "**as reported by the trade and financial press**" | 0% | Re-source to the filing |
| 25 | Table 18, row 4 | One-sided macro give-back | Logic | PARTIAL | "Terminal rate on the 2028 target \| 10.86 \| the softer **5% target** replaces the 7% target in force" | The row moves terminal **growth** to 5% and leaves the terminal risk-free rate at 12.50% — which is *built as* 7% target + 5.5% real. Moving both (Table 16, 16.14% / 5%) gives **12.14** | Inflation taken out of the growth rate and left in the discount rate. The wedge runs *against* the study here, but it is the same Pass-5 defect as #1 | −1.1pp on that row | Move the target once, everywhere |
| 26 | §1.8, DCF C50 | Discounting convention | Disclosure | PARTIAL | Convention never named | Workbook is **year-end**: 1/(1+r), cumulative. Mid-year gives EGP **12.32** | Pass 8 requires the convention be confirmable from the page; a choice worth **+8.0%** is unstated | +8.0% if mid-year | Name it and justify it |
| 27 | §1.10, A110 | Terminal growth in real terms | Disclosure | PARTIAL | "the adopted 7% is **generous**" against a five-period record implying 0.70% | The terminal risk-free rate is built as **7% inflation** + 5.5% real, so 7% nominal growth is **0.00% real** in perpetuity. The register says so ("INFLATION ONLY, and no real growth at all"); §1.10 does not | Pass 4 requires the real number be written down. "Generous" is the wrong word for zero real growth | 0% | State the real rate on the page |
| 28 | Table 17; DCF C37 | Decorative rows and inputs | Disclosure | PARTIAL | Table titled "**what the bear and bull columns actually move**" lists "Exchange-rate path 1.00x / 1.00x / 1.00x" and "Cost of capital 0.0% / 0.0% / 0.0%". §1.8: growth capex "at the plant's own EGP 2,100 per annual tonne" | Two of four rows move nothing. Volume is flat in every base-case year, so the growth-capex term `MAX(Δvolume,0) × 2100.379938` is **identically zero** in all five years | Pass 12 "DECORATIVE": printed, dated, fresh — and read by nothing in the base case. Also 2100.379938 is hardcoded in the formula, not registered | 0% | Mark them as inert |
| 29 | Table 6, Table A.1 cols 1–2 | Two filed periods with no source | Input | PARTIAL | 6M Dec-2024 (18,246 / 1,251 / 6.85%) and 3M Mar-2025 (10,068 / 509 / **5.05%**) presented as "the filed margin record" | Neither period has a single cell in the 181-row register. The 5.05% figure is the low end of the "737 basis point" spread that anchors §1.2, §5 and the margin thesis | A headline statistic resting on two columns the model cannot reproduce | 0% direct | Register them or withdraw the range |
| 30 | About-this-study box | Workbook statistics | Disclosure | PARTIAL | "6,069 formulas against **251 pasted filing values** (96.0% live)"; "**180 registered inputs**"; "0 disagreements" | 6,069 formulas ✓. But **181** valued rows on Assumptions, and 251 matches nothing in the file. 5,406 of the 6,069 formulas (89%) are the Sensitivity grid; the core model carries 663 | The liveness statistic is not reproducible from the delivered file | 0% | Recount |
| 31 | Table 1, Headline | "All four lenses land below the price" | Construction | PARTIAL | Four lenses below the price, presented as corroboration | Lens 2 is, algebraically, market cap × (1 − minority) − claims: at a zero re-rating it **must** land below the price. Reproduced exactly (12.589) | The study correctly withdraws the lens as circular in §1.12, then counts it in the four-of-four claim | 0% | Count three |
| 32 | Monte Carlo B7 | Risk-free rate | Input | PARTIAL | Cone drift uses rf **19.50%**; the valuation uses rf **22.31%** | Both are facts about one sovereign on one date | Lens independence does not license two risk-free rates | 0% on FV | One rate |
| 33 | §1.6, §7 | rf 22.31%, ERP 9.41%, spread 3.40%, beta 0.908 | Input | **UNVERIFIABLE** | rf "carried from a house reference this environment could not open"; ERP/spread from Damodaran Jan-2026; beta n=253, R² 25.9%, EGX30 | Not reachable here. Internally the ERP is **coherent**: 4.31% mature + 1.5 × 3.40% spread = 9.41% | Searched: no primary access in this environment (no filings, no Damodaran file, no bond data) | ~−0.5% at rf 23.0% (the study's own estimate) | Cite the bond quote; publish the regression |
| 34 | §2, §3 | Price history; 3,754 sessions; 0.1813 max log move | Input | **UNVERIFIABLE** | Series 2011-01-02 to 2026-08-06, one row dropped | Cannot open the vendor file. Internal checks pass: 0.1813 < ln(1.20) = 0.18232; the ±20% band is correctly tested asymmetrically; the 48% move from 9.10 to 13.50 in four weeks is not checkable | — | — | Publish the screened series |

---

## Section C — Arithmetic Reconciliation Appendix

Independent rebuild from the Assumptions cells only. **Every line below matched unless a delta is shown.**

### C.1 Base year and solved rates

| Item | Report | Recomputed | Δ |
|---|---|---|---|
| Base-year revenue / gross profit / margin | 46,959 / 4,533 / 9.65% | 46,959.0 / 4,533.1 / 9.6534% | 0 |
| Nine-month alternative base | 41,662 at 7.51% | 41,661.7 at 7.505% | 0 |
| Solved realisation index | 1.000 | 1.000000 | 0 |
| Per-line cost rebuild vs disclosed cost of sales | "foots exactly" | residual **0.000000000** | 0 |
| Feedstock share of cost of sales (note 15-A) | 91.2% | 91.157% | 0 |
| Profit-share rate / minority rate | 5.24% / 2.963% | 5.2359% / 2.9628% | 0 |
| Implied asset life | 17.5 y | 17.4996 y | 0 |
| Share count foots (issued capital ÷ par) | 1,291.5mn | 1,291,500,000 ÷ EGP 1 ✓ | 0 |

### C.2 Cost of capital

Country risk is counted **exactly once** — the risk-free rate is netted of the 3.40% sovereign spread, then a CDS-basis ERP is added whose country premium equals 1.5 × that same spread. **This passes.**

| | Report | Recomputed | Δ |
|---|---|---|---|
| Ke explicit (22.31 − 3.40 + 0.908 × 9.41) | 27.45% | 27.4543% | 0 |
| Ke terminal (12.50 + 0.908 × 7.00) | 18.86% | 18.8560% | 0 |
| WACC terminal (90 / 10) | 18.14% | 18.1386% | 0 |
| "Weighted" explicit WACC | 27.45% | **27.4398%** if actually weighted; model uses Ke | +1.4bp |
| Glide fractions | .000 / .517 / .731 / .893 / 1.000 | .0000 / .5166 / .7315 / .8926 / 1.0000 — **exactly** the cost-of-debt path's cumulative progress, as declared | 0 |
| Forward rates | 27.45 / 22.64 / 20.64 / 19.14 / 18.14 | 27.4543 / 22.6414 / 20.6401 / 19.1392 / 18.1386 | 0 |
| Cumulative discount factor (year-end) | .78460 / .63975 / .53029 / .44510 / .37676 | .78460 / .63975 / .53029 / .44510 / .37676 | 0 |
| Cost of debt after tax 13.21% | "on NET debt" | (0.2431 × 16.85 − 0.17 × 3,018.4) / (−3,001.5) × (1 − 0.22119) = 13.208% — dominated by the 17% **cash** yield, not a borrowing rate | 0 |

### C.3 Free-cash-flow waterfall (EGP mn) — report / recomputed

Deltas are ≤1 rounding throughout.

| | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---|---|---|---|---|
| Revenue | 53,144 / 53,143.6 | 58,069 / 58,069.1 | 61,752 / 61,751.5 | 64,764 / 64,763.7 | 67,607 / 67,607.0 |
| Cost of sales | 47,997 / 47,997.2 | 52,434 / 52,434.3 | 55,752 / 55,751.6 | 58,465 / 58,465.1 | 61,026 / 61,026.4 |
| Gross profit | 5,146 / 5,146.4 | 5,635 / 5,634.8 | 6,000 / 5,999.9 | 6,299 / 6,298.6 | 6,581 / 6,580.6 |
| Gross margin | 9.68 / 9.6839% | 9.70 / 9.7036% | 9.72 / 9.7163% | 9.73 / 9.7255% | 9.73 / 9.7335% |
| Operating expense | 2,017 / 2,016.9 | 2,259 / 2,258.9 | 2,462 / 2,462.2 | 2,647 / 2,646.9 | 2,832 / 2,832.1 |
| EBITDA | 3,130 / 3,129.5 | 3,376 / 3,375.9 | 3,538 / 3,537.7 | 3,652 / 3,651.8 | 3,748 / 3,748.4 |
| Depreciation | 180 / 180.3 | 191 / 190.7 | 202 / 202.3 | 215 / 215.0 | 229 / 228.6 |
| EBIT | 2,949 / 2,949.2 | 3,185 / 3,185.2 | 3,335 / 3,335.4 | 3,437 / 3,436.8 | 3,520 / 3,519.8 |
| NOPAT after profit share | 2,166 / 2,166.0 | 2,339 / 2,339.3 | 2,450 / 2,449.6 | 2,524 / 2,524.0 | 2,585 / 2,585.0 |
| Capital expenditure | 182 / 181.7 | 203 / 203.5 | 222 / 221.8 | 238 / 238.4 | 255 / 255.1 |
| Change in working capital | 446 / 446.1 | 355 / 355.3 | 266 / 265.6 | 217 / 217.3 | 205 / 205.1 |
| **Free cash flow to the firm** | 1,718 / 1,718.5 | 1,971 / 1,971.2 | 2,165 / 2,164.5 | 2,283 / 2,283.3 | 2,353 / 2,353.4 |
| **Present value** | 1,348 / 1,348.3 | 1,261 / 1,261.1 | 1,148 / 1,147.8 | 1,016 / 1,016.3 | 887 / 886.7 |

One free-cash-flow definition holds across both blocks: 2030 net reinvestment is 8.94% of NOPAT ("9.0%"), and the terminal uses NOPAT × (1 − 23.1%). **Pass.**

### C.4 Terminal block, with the implied asset life

| | Report | Recomputed |
|---|---|---|
| Terminal NOPAT (2,585 × 1.07) | — | 2,765.9 |
| Invested capital, gross basis | — | 9,134.8 (NWC 4,879 + gross register 4,256) |
| Terminal ROIC | 30.3% | 30.2794% |
| Reinvestment = g ÷ ROIC | 23.1% | 23.1181% |
| Terminal free cash flow | — | 2,126.5 — **positive** ✓ |
| Implied payout (1 − reinvestment) | — | 76.9% — inside (0,1) ✓ |
| Terminal value | — | 19,091.5 |
| PV of terminal block | 7,193 | 7,193.0 |
| Terminal share of enterprise value | 56.0% | 55.963% — disclosed and discussed ✓ |
| **Implied replacement cycle = 1/g** | not reported | **14.3 years** |
| Model's own depreciation life | 17.5 y | 17.4996 y |
| **Disclosed useful life (policies note)** | **never cited** | **UNVERIFIABLE** |
| Terminal real growth | not reported | **0.00%** (7% nominal on 7% embedded inflation) |
| Terminal real WACC | not reported | 10.41% |

The 14.3-year implied cycle against the model's own 17.5-year life is a ~22% specification gap; against a refinery's normal disclosed life it is likely a 2–3× gap, but that cannot be settled without the note. In a 7%-inflation terminal the identity starves the asset, so the direction is conservative.

### C.5 Enterprise-to-equity bridge — foots to the last unit

| Step | Report | Recomputed | Δ |
|---|---|---|---|
| PV of the explicit window | 5,660 | 5,660.2 | 0 |
| PV of the terminal block | 7,193 | 7,193.0 | 0 |
| **Enterprise value** | 12,853 | 12,853.2 | 0 |
| plus net cash | 3,002 | 3,001.5 | 0 |
| Enterprise value including cash | 15,855 | 15,854.7 | 0 |
| less minority interest (2.963% of the whole) | (470) | (469.7) | 0 |
| less tax-disputes provision | (997) | (996.9) | 0 |
| less dividends payable | (258) | (258.3) | 0 |
| plus non-operating investments (525 + 70) | 595 | 594.8 | 0 |
| **Equity attributable** | 14,725 | 14,724.6 | 0 |
| **Per share** | **11.40** | **11.4012** | **0** |

The bridge construction passes on every Pass-7 test: cash charged **once** (operations at the unlevered rate, cash added at face — the previous net-debt double-count is correctly retired); minority deducted from **equity** value at share-of-value (470) rather than book (73); the dividend deducted because declared before the balance-sheet date; pledged deposits returned rather than vanishing from both sides; the lines sum to the stated equity value and that value divides to the stated per-share figure.

### C.6 Cross-checks that also reproduced exactly

- Lens 3 normalised EPS **1.8405** ("1.841") and value **9.0639** ("9.06")
- Lens 2 at **12.589** ("12.59"); trailing EV/EBITDA **4.891** ("4.89")
- Lens 4 justified P/B **1.3248** × book **4.7002** = **6.2271** ("1.32 / 4.70 / 6.23") — and its cost of equity **22.850923%** is, to seven figures, the PV-weighted average of the five-year Ke glide, exactly as declared
- Expert 2's five discount factors and its entire PV column
- Expert 3's five economic-profit figures and their PV of 3,337.8
- Table 14's counts (three of five positive; 0.6% and 0.70% averages)
- Table 24's zones summing to 100.0%; the touch ladder monotone in both directions
- The Monte-Carlo 1-month median 9.170973 = 9.10 · e^(carry/12)
- **All six sensitivity grids and Table 16's 25 cells are live formula blocks and reproduce to 2dp**

**The one cross-check that does not tie:** Expert 1, my 14.68 against the printed 14.50 (−1.2%); cause not isolated.

---

## Section D — Construction Register

| | What the report DECLARES | What it actually DOES | Agree? |
|---|---|---|---|
| **Primary lens** | One class primary; DCF is the answer; three cross-checks carry no weight | Exactly that. The retired 45/20/20/15 blend is computed and unused (FV!B17) | **Yes** |
| **Relative lens** | Withdrawn; circular; "a statement about the BRIDGE" | Algebraically market cap × (1 − MI) − claims. Correctly withdrawn — then counted in "all four lenses land below the price" | Mostly |
| **Terminal construction** | "Growth = return × reinvestment is ENFORCED"; invested capital "at REPLACEMENT cost"; "One view is now applied across the model" | Identity enforced correctly. Capital is **historical gross book**, not replacement. Three capital views coexist: terminal on gross (30.3%), Table A.3 memo on net (42.3%), Expert 3 wholly on net | **No** |
| **Cost-of-capital path** | Glides; sovereign spread stripped once; weighted; "net cash pushes the operating rate ABOVE the cost of equity" | Glide correct and correctly derived. Country risk counted once — clean. But no weighting occurs (B14 = B10), the glide is hardcoded, and the operating rate **equals** the cost of equity; "above" is true only of the retired construction | Partly |
| **Discounting convention** | Not stated | Year-end, cumulative on forward rates. Worth **+8.0%** if mid-year | **No** |
| **Currency split of the debt book** | Never addressed | Never split. Immaterial at 0.0966% of capital, and the study says so honestly. The adopted 24.31% has no contractual anchor; trailing loan interest implies ~13.6% | Not stated |
| **Inflation path and every escalator** | "One path"; "one escalator per driver class"; "only genuinely domestic lines take a domestic index" | **Two paths.** Realisation and cost of sales on (1+i)/**1.025**; operating expense and capex on the full Egyptian index. Egyptian salaries — 49.8% of the conversion stack — ride the **product** index. Depreciation inside cost of sales is the only line held flat. No exchange-rate path, no USD inflation rate and no wedge is published anywhere | **No — the largest gap in the package** |
| **Forecast anchor** | Twelve contiguous months to 30-Jun-2026, both sides, no scalar | Exactly that, and it foots. But the first forecast year opens at 9.68% against a latest filed 12.43%; the study's own evidence argues the weak half is not seasonal ("5.05% against 10.19%, which no seasonal pattern produces"); and the named mechanism is a process rule — "corrections are made one at a time" — not evidence | Partly |
| **Bridge** | "the balance sheet at 31 December 2025, as filed" | Stands on **30 June 2026** (correct, and the latest available) — except fixed assets at cost, still 31-Dec-2025 beside a 30-Jun-2026 net book | **No** |
| **The evidence base** | Reviewed H1-2026 statements in hand; the released gross profit confirmed | Register and two workbook cells still say it is a press release whose gross profit was rejected and solved | **No** |

---

## Section E — Verdict Summary

### Counts by pass

| Pass | Result |
|---|---|
| 1 — Input verification | 3 partial, 2 unverifiable |
| 2 — Market data | 1 total, 1 partial, 1 unverifiable |
| 3 — Cost of capital | 1 total, 2 partial — **country risk correctly counted once** |
| 4 — Terminal value | 2 partial — identity, FCF definition, payout and TV disclosure all pass |
| 5 — Macro coherence | **1 total, 1 partial** — the escalator wedge |
| 6 — Forecast anchoring | 1 partial |
| 7 — Lens architecture and bridge | 3 total, 1 partial — **the bridge itself is clean** |
| 8 — Calculation verification | **entire waterfall, glide, terminal and bridge reproduce to the last cell**; 2 total on pasted give-back rows; 1 partial on dead cells |
| 9 — The page a reader receives | 5 total, 5 partial |
| 10 — Probabilistic content | 2 total, 1 partial |
| 11 — The answer itself | see below |
| 12 — Completeness sweep | 2 total, 2 partial |
| **Totals** | **14 TOTAL · 18 PARTIAL · 2 UNVERIFIABLE** — against roughly thirty distinct arithmetic reconciliations that passed clean |

### The three most valuation-critical findings

1. **The undisclosed 2.5%-a-year escalator wedge (#1).** Revenue and cost of sales escalate at Egyptian inflation ÷ 1.025; operating expense and capex escalate at full inflation. Closing it moves the central from **EGP 11.40 to EGP 13.44 — within 0.5% of the traded price.** The study's entire disagreement with the market is smaller than one escalator nobody wrote down.

2. **The price is four weeks younger than everything else in the study (#8).** The masthead, Table 23 and the §3 cone all say 6 August 2026, where the close was **9.10**; the register dates the 13.50 to 3 September. Against its own stated valuation date the study's fair value is **+25% above** the price, not 15.5% below.

3. **The adversarial stack does not reproduce (#3, #9, #11, #12).** The profit-share give-back is 12.06 not 11.69; "all of the above at once" is 12.49 (−7.5%) not 12.74 (−5.7%); the rating-basis pair (30.61%, 9.22) cannot come from one re-run and gives 10.99; and the panel median, after the study's own conceded correction to Expert 1, is 9.34 not 12.32. Every published defence of the gap is mis-stated — in both directions.

### Direction of the contested judgements

Seven judgements are worth more than ~5% of value.

**Five resolve toward a lower value:**

| Judgement | Worth |
|---|---|
| The base anchor (the study's own figure: 17.62 on the latest half) | +55% |
| The escalator wedge | +17.8% |
| Year-end rather than mid-year discounting | +8.0% |
| The terminal capital basis (gross rather than net book) | +4.5% |
| Taking all three disclosed charges | +EGP 1.63/share |

**Two resolve higher:** 7% terminal growth against a filed record implying 0.70%; and the CDS-basis premium over the rating basis.

**Five–two — and the two that go the other way are together worth about EGP 1.35 while the five are worth several times that.** This is a flag, not a failure, but it is the pattern the audit exists to surface, and the study never counts it. To its credit, §7's own back-test independently reports a one-sided miss in the same direction ("under-forecast every single time, by 64% on average"), and §1.14's inversion says the price needs only 10.58% margin. Both point at the same conclusion the study declines to draw.

### Does the headline range survive the corrections?

**It collapses.**

Not because the model is broken — it is the most cleanly reproducing model one could hope to audit. The waterfall, glide, terminal identity, bridge, per-line cost footing and all thirty sensitivity points recompute exactly, and the cost-of-capital construction, the single cash charge and the minority treatment are done properly and are improvements the study is right to claim.

It collapses because the two largest corrections are independent of the model's quality: closing the undisclosed escalator wedge takes the central to **13.44**, and pricing the study on the date it says it was struck makes **11.40 a premium to the market, not a discount**.

The reverse read is decisive: the price requires a 10.61% gross margin — inside a filed range the study itself puts at 5.05–12.43%, and below the 12.43% just reported — which is a thoroughly believable number, and Prime Directive 11 holds that this is evidence *against* the report's disagreement with the market.

**The stated −15.5% does not survive. The lens machinery does.**

---

*Audit performed 18 September 2026. Every row above carries either a primary-source reference or shown arithmetic from an independent rebuild of the delivered workbook.*
