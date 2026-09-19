# Forensic Audit — Sinai Cement Valuation Study

Testahil · Sinai Cement Company S.A.E. (EGX: SCEM) · study issued 7 September 2026, struck on the 2 September 2026 close of EGP 100.50 · audit dated 18 September 2026

---

## Section A — Audit scope

**Audited:** the valuation study, the companion workbook and the source register, against Sinai Cement's own filings. **Primary sources reached:** all six PDFs published on sinaicement.com — the FY2021–FY2025 audited statements and the reviewed interim to 31 March 2026. Every one carries a zero-byte text layer (verified: 0 characters across 36 / 37 / 34 pages), so figures were read by OCR off rendered pixels and footed against the filings' own printed subtotals; the balance sheet, income statement, note 3/2 and note 25 were read directly and are reproduced in Section C.

**Recomputed, not inspected:** the entire model was rebuilt independently in Python from the workbook's formula graph — every driver, the full waterfall, the cost of capital, the terminal and the bridge. The workbook ships with no cached values, so nothing could be read off it.

**Not checked (logged UNVERIFIABLE, not as failures):** Damodaran's January-2026 country file; the EGX daily price series, supplied privately with the engagement; Egyptian sector volumes; replacement cost of USD 130 per annual tonne; the plant's kiln and grinding capacities; the liquidity and walk-forward statistics.

**One asymmetry to note:** the report's own environment was network-blocked and its register says so. Mine was not. Several figures that register marks unobtainable were checkable here, and where the register's numbered entries cite the filings they are accurate — the preamble that denies them is not.

---

## Section B — Fail table

The model reconciles to the last cell: every figure the study prints reproduces from the workbook, and every figure the workbook takes from the filings is correct to the pound. The failures are almost all on the construction and disclosure planes — correct numbers reached by constructions nobody wrote down, and prose carried forward from revisions the model has replaced.

### TOTAL FAIL

| # | Location | Item | Plane | What the report says | What is correct | Why it failed | Impact | Correct method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | §"The terminal value"; DCF!B25, B48 | Terminal maintenance charge struck in the wrong money | Construction | Maintenance = replacement capital ÷ disclosed 20-year life = EGP 1,241mn; workbook calls it "the SAME charge the terminal makes" | The explicit window charges EGP 2,022mn in FY2030 (1,241 × the model's own cost index 1.6289). The terminal charges 1,241 against FY2030-money NOPAT | Replacement capital is struck at spot FX 50.25 and FY2025 costs; NOPAT₅ is FY2030 nominal. The capital charge **falls 38.6%** at the terminal boundary | **+EGP 11.91 (+11.9%)** | Escalate the charge to FY2030 money → EGP 99.71, and terminal ROIC becomes 12.25%, below the 18.98% terminal WACC |
| 2 | Assumptions!B7; DCF row 10 | Forecast taxed at the statutory rate while the register commits the effective one | Construction / Input | "NOPAT (EBIT × (1 − t))", t never printed. Register input 37 sets tax_eff = 32.0% and criticises revision 1 for using 22.5%. §"One thing to fix" uses "the effective 32.0%" | The model uses 22.5% throughout; the value 0.32 appears in no cell of the workbook. Filed effective rate FY2025 = 1,074,326,268 ÷ 3,358,865,272 = **31.99%** | The register's own committed input is absent from the model, and one document applies two tax rates to one company without reconciling them | **−EGP 12.04 (−10.8%)** | Print the forecast tax rate and reconcile it with the historical treatment |
| 3 | Assumptions!C28–G28; §1.6 Table 9 | FY2026 opens 9.6% above the latest reviewed period | Input | FY2026E revenue EGP 10,550mn, +16.1% on FY2025 | Reviewed Q1-2026 sales EGP 2,135,463,626, **+5.9% y/y**. At FY2025's own Q1 seasonality (22.18%) that annualises to EGP 9,627mn | Pass 6 mirror case: a forecast above everything filed must name a mechanism and carry a disclosure. None is given for volume | **−EGP 13.97 (−12.5%)** | Anchor utilisation on the reviewed quarter, or name and evidence the mechanism |
| 4 | §1.6 Table 12; Unit Build A38–A49 | The "test that can fail" is an identity on both legs | Construction | "Nothing above was solved to match the accounts — every cost driver is an independent physical or market norm — so the comparison below is a genuine test rather than a restatement" (+0.10% revenue, +0.26% EBITDA) | The register's own §3 says "realised price is then disclosed revenue divided by that volume, so the build reproduces the reported top line exactly". Input 12 derives fixed cost as revenue − EBITDA − the two disclosed lines | Unit Build B23/B24 divide the **disclosed** cost lines by modelled volume, so volume cancels. EBITDA_built ≡ Revenue_built − Revenue_disclosed + EBITDA_derived, and the EBITDA delta is algebraically the revenue delta ÷ EBITDA: 9 ÷ 3,455 = 0.26% | Nil on value; the model's principal validation carries none | Withdraw the claim, or test against a driver not used to build the stack |
| 5 | §"And this is why growth does not help"; Expert 3; Sensitivity!A28 | Terminal return is **above** the cost of capital; the report says below, three times, with three different pairs | Logic / Disclosure | "Terminal return on capital of 19.9% sits BELOW the terminal cost of capital of 19.0%". The workbook's own note says "(9.4%) is below … (16.3%)" | Recomputed from the model's own cells: terminal ROIC = NOPAT₅ × 1.07 ÷ 24,823.5 = **19.95%**; terminal WACC = **18.98%**. ROIC exceeds WACC | Three statements of one pair of figures, none agreeing, and the sign is wrong in all of them | Nil on arithmetic; fatal to the narrative — the report's central claim about why this company should harvest rather than grow is the opposite of what its model computes | State the model's actual relation, or fix finding 1, which makes the prose true |
| 6 | Figure 4 caption; Table 8 box; Table 12 | Higher growth said to lower value; the grid beside it shows value rising | Logic / Disclosure | "raising terminal growth from 3% to 7% LOWERS fair value, from EGP 96.33 to EGP 111.62"; "Reading left to right, higher growth lowers the value" | The quoted numbers rise. My recomputation reproduces the grid exactly: 96.33 / 99.39 / 102.89 / 106.92 / 111.62 | A direction asserted in words against figures printed in the same table | Nil on value | Correct the direction |
| 7 | §"The terminal value, and the judgement that decides it" | Terminal declared as the reinvestment identity, built as a maintenance charge | Construction | "the terminal return on capital is 19.9% and the reinvestment rate is 25.1% of profit" | At g = 7% and ROIC = 19.95% the identity gives a reinvestment rate of **35.09%**, not 25.1%. The 25.1% is an **output** of the maintenance charge (1,241.2 ÷ terminal NOPAT 4,951.6 = 25.07%) | The declared construction and the built construction are different objects, and the report reasons from the declared one | Applying the declared identity gives EGP 101.36 (**−EGP 10.26, −9.2%**) | Name the construction actually used |
| 8 | §1.8 cost-of-capital table | Terminal cost of equity does not reproduce from the inputs printed beside it | Logic / Disclosure | rf 12.50%, Beta **1.00**, ERP 7.00%, cost of equity **20.82%** | 12.50% + 1.00 × 7.00% = **19.50%**. The model (DCF!C56) relevers the asset beta by Hamada to **1.1889** at the 20% terminal debt weight: 12.50% + 1.1889 × 7.00% = 20.82% | Pass 3's explicit rule: a terminal cost of equity on a different beta must name its construction and state its leverage and tax rate. The workbook does; the page does not, and prints the wrong beta | Nil on value (the model is right); the page is unreproducible | Print the relevered beta with the leverage and tax rate that produce it |
| 9 | Summary table; Tables 8, 16, A2; Relative & Normalized!B41 | Every per-share figure but one uses 260.81mn shares; the book floor uses 222mn | Input / Logic | Book value **EGP 27.12** a share, "a disclosed floor" | Filed equity at 31 Dec 2025 = EGP 6,020,338,736 ÷ 260,812,477 shares in issue = **EGP 23.08**. The 27.12 divides by the FY2025 weighted-average count of 222mn. The workbook carries both (Per-Share & Ratios!D7 = 23.08) | Period-end equity over a period-average count, published beside four lenses on the current count. Table A2's own BVPS row switches denominator for one column and back | Disclosed floor overstated **17.5%** | One share basis — the current count — for every per-share figure |
| 10 | Table A1 | Historical EPS contradicts the company's own disclosed EPS | Input | EPS −0.45 (FY2023), **11.78** (FY2024), **8.76** (FY2025) | Audited income statement, printed page 3: **23.09** (FY2024) and **10.29** (FY2025), on the weighted-average counts the filing itself uses. The workbook computes these correctly (Income Statement B16–D16); the document divided by 260.81 instead | A figure the filing discloses outright is printed differently, and differently from the model beneath it | A disclosed figure misstated by 49% (FY2024) and 15% (FY2025) | Print the filed EPS |
| 11 | Table A2 | The cash row is the valuation-date figure printed against two year-ends | Input | Cash 6,708 at FY2024 **and** 6,708 at FY2025; net cash 6,570 / 6,555 | Audited balance sheets: cash **1,890,505,077** at 31 Dec 2024 and **4,762,348,666** at 31 Dec 2025. The 6,708 is DCF!B34 — the 31 Mar 2026 balance rolled to the valuation date (5,802.0 + 2,720.3 × 0.333 = 6,707.8) — and the two net-cash figures are that one number less two different debt balances | One dated figure printed against two other dates, in a table headed as a balance sheet | FY2025 cash overstated EGP 1,946mn; the balance sheet does not foot to its own equity | Print the filed balances and show the roll separately |
| 12 | §1 opening | Debt and equity taken from an aggregator and contradicting the filing | Input | "EGP 36.8 million of total debt against roughly EGP 5.2 billion of equity" | Lease liabilities **EGP 137,565,888** (111,742,265 + 25,823,623) and equity **EGP 6,020,338,736** at 31 Dec 2025. The register's research trail sources the 36.8 / 5.2bn pair to "EGX filings via aggregated financial summaries" | Prime Directive 1: an aggregator cited for line items that exist in the filing — and neither figure is right | Nil on value | Take both from the balance sheet |
| 13 | Assumptions!B56 and C5; Summary!A2 | The model is struck to 6 August 2026; only the spot price moved to 2 September | Input / Disclosure | "issued 7 September 2026, struck on the closing price of 2 September 2026"; "scaled to the 41.7% of FY2026E still unearned at the valuation date" | 41.7% = 5/12 exactly — seven months elapsed, i.e. **31 July 2026**. At 2 September the unearned fraction is 33.2%. The workbook's cells read "close 06-Aug-2026" beside a value of 100.50, and "06-Aug-2026" on the Summary masthead. Register input 1 records the re-strike from a 6-Aug close of 79.00, +27.2% | The price cell was updated; the valuation date behind the stub, the discount timeline and every dated artefact was not | Stub over-weights year 1 by ~25%; small on the central, but findings 14, 15 and 36 all descend from it | Re-run the model at the valuation date, not just the price cell |
| 14 | §3 Table 15; Monte Carlo!A5–B10 | The probability map is anchored on the superseded EGP 79.00 close | Logic / Disclosure | One-month median **80.17**, three-month median **82.78**, "Above spot **54%**" and "**57%**" — against a published spot of EGP 100.50 | Fitting a lognormal to the published 5th/95th percentiles gives P(>100.50) = **7.3%** (1M) and **24.5%** (3M). The published 54%/57% reproduce against 79.00 (53.8% / 56.6%). The one-month 95th percentile (103.50) barely clears spot while the median sits 20% below it | The sheet is labelled "PASTED — a whole-model re-run. Does NOT redraw", with grade dates of 6 Sep and 8 Nov 2026. It is a memory of the 6-August answer | Every probability statement in §3 and §6 is stated against a price the report no longer publishes | Re-run the simulation from the strike price |
| 15 | §3 box; §7 | The calibration record contradicts the workbook four ways | Disclosure | "**57** resolved three-month forecasts", 90% band held "**93%**", middle band "**70%**", cone "about **1.38 times** as wide as a simple carry-anchored benchmark … published rather than tuned away" | Monte Carlo!B13–B15: **17** resolved forecasts; coverage **0.94 / 0.76**; cone width **4.64×**, with the workbook's own verdict "The map is ILLUSTRATIVE ONLY. It is materially too wide and must not be read with the confidence of a calibrated name" | Four figures, four disagreements, all in the direction that flatters the map | Nil on value; a 4.64× cone is a different object from a 1.38× one, on a third of the claimed sample | Print the workbook's figures |
| 16 | §1.6, after Table 11 | The price narrative describes a model that was replaced | Disclosure / Construction | "Nominal realised prices rise **4.5% to 6.0%** a year across the forecast … that is a **REAL price decline in every single year** — which is what a supply glut does to pricing power" | The blended realised price rises **14.8 / 11.1 / 8.2 / 6.6 / 6.2%**, and the domestic price escalates at exactly the cost-inflation ladder 16 / 12 / 9 / 7.5 / 7% — **zero real growth, not a decline**. Register input 95 explicitly repudiates the earlier real-decline path as sourcing "no mechanism" | The paragraph defending the price forecast is revision-3 text against a revision-4 model | Nil on value | Describe the flat-real-spread construction the model uses |
| 17 | Source register preamble and §§2–6 | The bibliography's preamble denies the evidence its own register cites | Disclosure | "The company's audited consolidated financial statements could not be retrieved … Revenue and profit after tax are carried as reported through press coverage"; §3 says cash is "inferred as the derived FY2024 treasury income divided by the prevailing deposit yield" and prints a return on capital of "**nan%**"; §4 carries an FY2024 balance sheet of 6,385.9 / 1,610.9 / 4,775.1, "the triple closes exactly" | The register's numbered inputs cite the filings page by page and I verified them to the pound. The audited FY2024 triple is **5,695,608,211 / 1,959,808,479 / 3,735,799,732** | Two irreconcilable claims about the same evidence base in one document, plus a failed computation printed to the reader | Nil on value; it makes the register unusable as a control | Retire the superseded sections |
| 18 | §1.8 beta sensitivity table | Mislabelled, so the published central appears under an input that does not produce it | Logic / Disclosure | Columns "0.60 │ 0.80 │ **1.00 (adopted)** │ 1.15 │ 1.30" against 136.83 / 122.63 / **120.38** / 111.62 / 99.10 | The workbook's own headers (Sensitivity!B21–F21) are "0.60 │ 0.80 │ **0.84** │ 1.00 │ 1.30" on the identical value row. 120.38 belongs to the lead-lag beta of 0.84. My recomputation gives **111.62 at β = 1.00** and 104.87 at β = 1.15 | Every label shifted one step, and a β = 1.15 column invented that appears nowhere in the model | The document shows its adopted beta producing EGP 120.38 when its model produces EGP 111.62 | Print the workbook's labels |
| 19 | §1.7, §5, Table B2; Peer & Sector!B14–B21 | The sector capacity the report calls its largest swing factor is decorative | Construction | 12.6Mt of dormant capacity, "about 23% of domestic consumption, arriving inside the forecast window … the single largest swing factor" | The sector block's only formulas are three display ratios. **No line of the Unit Build, DCF or Assumptions reads** Egyptian capacity, consumption, production, exports or the revival figure. Kiln utilisation is a typed House path rising monotonically from 71.0% to 79.1% in spite of it | Pass 12's decorative case: recorded, printed, and read by nothing | The risk is described at length and priced at zero | Drive utilisation or price from the supply balance, or say the table is context only |
| 20 | Throughout; register preamble | The filings are the company's separate statements, not consolidated | Input / Disclosure | "audited consolidated financial statements"; EGP 120mn of non-controlling interests deducted "on the share of profit the subsidiaries actually earn" | The FY2025 filing's contents page reads "**Independent** Balance Sheet", "**Independent** Income Statement", "Notes to the **Independent** Financial Statements". Affiliates are carried at cost (EGP 25,039,500) and **there is no non-controlling-interest line anywhere in it** | A false statement about the basis of the evidence, and a bridge line with no source in the statements relied on | −EGP 0.46 as printed; the revenue base is the parent's | State the basis, and evidence the NCI or drop it |
| 21 | §1.1 discount schedule | The discounting convention is undisclosed and unreproducible from the page | Disclosure | "Each forecast year is … discounted at its own forward rate … The first year is scaled to the 41.7% … that is the only line a reader cannot add up from the two above it" | DF₁ = 1.2896^−0.2085 = 0.9484 — the stub discounted at its own **midpoint** — and years 2–5 are **mid-year** on a stub-shifted timeline (DCF!B18–F18). Nothing on the page says mid-period | The sentence claims full reproducibility for every line but one, and the discount row is not reproducible at all | At 28.96% the convention is worth roughly **13%** of the explicit PV | State the convention |
| 22 | §1.1 after Table 1 | Capex described as a run rate, built as a convergence to replacement-cost maintenance | Disclosure | "Capital expenditure is the company's own run rate from its cash-flow statements — EGP 121mn in FY2023, 526mn in FY2024 and 262mn in FY2025 — escalated with domestic costs" | DCF!B20–F20 interpolate from the EGP 303.2mn run rate to the EGP 1,241.2mn maintenance charge on undisclosed weights of 0 / 0.25 / 0.5 / 0.75 / 1, then escalate. Inflation alone takes 352 to 494 by FY2030; the model charges **2,022** | The described line and the modelled line differ fourfold by the last forecast year | Nil on value (the construction is defensible) | Disclose the convergence |
| 23 | Table 13 note; §7 | Net cash described as a reported balance; it is a modelled roll-forward | Disclosure | "the balance is taken from the reported accounts rather than inferred from the income it earns"; "the cash the valuation adds back is read off the reviewed balance sheet directly" | DCF!B34 = the 31 Mar 2026 reviewed cash of EGP 5,801,981,716 **plus a third of a year's modelled free cash flow** = 6,707.8 | The sentence was written to retire an earlier inference and describes a construction the model does not use | EGP 906mn of the EGP 6,555mn added at face is forecast, not reported — **EGP 3.47 a share** | Say so |

### PARTIAL FAIL

| # | Location | Item | Plane | What the report says | What is correct | Impact |
| --- | --- | --- | --- | --- | --- | --- |
| 24 | §1.8 | Terminal risk-free rate stated two ways | Disclosure | "The terminal risk-free rate of **10.5%** is the central bank's … target of 5% plus … about 5.5 points" | The table beside it says **12.50%** — the 7% operative Q4-2026 target plus 5.5. Register input 96 confirms the 7% basis; the table is right and the prose is a stale draft | Nil (reverting to 10.5% would *add* 9.9%) |
| 25 | Assumptions!B54 | Terminal debt weight 20% against an observed 0.52% | Disclosure | Debt weight 0.52% (explicit), 20.00% (terminal) | The forecast balance sheet holds debt flat at EGP 137.6mn for ever. The gearing-up is never justified | +2.5% to value |
| 26 | §1.3 Table 6 caption | Caption contradicts the multiple used | Construction | "struck at the peer's own EBITDA multiple" | It uses **4.2×** against the peer's 5.03×. Register input 82 explains why; the caption does not | Nil (cross-check lens only) |
| 27 | §1.3 | Quotes the peer multiple its own register rejects | Input | Misr Beni Suef "at **6.44 times** trailing earnings" | Table B1 and register input 55 give **3.48×**, and the register rejects 6.44 as irreconcilable with the market cap printed beside it (6.44 × 3,946 = 25,412 against a stated 13,730) | Nil |
| 28 | §1.7 | Net cash as a share of market cap, stated three ways | Disclosure | "Net cash of EGP 6,555 million is **37%** of the market capitalisation" | 6,555 ÷ 26,212 = **25.0%**, as the header and Expert 3 both say. The 37% is the register's revision-1 figure against a different denominator (equity value) | Nil |
| 29 | §1.2 | EV per tonne stated two ways | Disclosure | "the market is paying roughly **USD 81** per annual tonne" | Its own Table 5 says **102.9** and Expert 1 says "USD 103/t". 81 is the 2025 price per tonne of cement, not EV per tonne of capacity | Nil |
| 30 | Assumptions!B87; Table 3, Table 8, §7 | The bear bound is a hardcoded constant and does not reproduce at the stated margin | Logic | Range low **EGP 22.36**, "flexes the operating margin down to **8.7%**" | 22.36 is typed into Assumptions!B87 and reproduces at a **9.71%** margin. At an actual 8.7% the model gives **19.25** | Headline range low overstated ~16% |
| 31 | Table 14 caption | Caption contradicts its own grid | Disclosure | "Each two-point change in the EBITDA margin is worth roughly **EGP 4.50** a share" | Its own grid steps **5.96**; my recomputation gives **6.17** | Nil |
| 32 | §6 zones table | Zone description contradicts the stated price | Disclosure | "Below the replacement-cost read │ under 94.23 │ … **Where the price sits today**" | The price is **100.50**, above 94.23 — it sits in the next zone up | Nil |
| 33 | §1.6 Table 10 note | A promised sensitivity that does not exist | Disclosure | The dollar-linked share of the materials line (48.4%) "is **sensitised in section 1.9**" | §1.9 sensitises the cost of capital, growth, net cash and margin. There is no dollar-share grid anywhere | Nil |
| 34 | §§1.6, 1.8 | Table numbering broken | Disclosure | — | Two tables numbered **10**, two numbered **11**, and no Table 4 | Nil |
| 35 | §1.8 vs §7 | The beta regressor is named two ways | Construction | §1.8 and the register: "an **equal-weight Egyptian composite**" of 32 names. §7: "The own-stock regression against **EGX30**" | A 32-name coverage basket is not the published index of the exchange the stock is listed on (Pass 2). Impact is nil because the regression is rejected and β = 1.00 adopted — but the diagnostic justifying the override is itself non-standard, and one regression is given two regressors | Nil |
| 36 | §2 | A stated high below the stated close | Logic | "a 2026 high of **EGP 87.99**" | The stated close is **100.50**. The price file ends 6 August 2026 — the same stale anchor as findings 13–15 | Nil |
| 37 | Appendix C | Weights quoted in a study whose thesis is that nothing is weighted | Disclosure | Expert 1: "it now carries **8% of the weight** rather than 15%". Table C1 caption: "the **weighted central** of the four principal lenses" | The register still carries live weights summing to 1.00 (0.48 / 0.23 / 0.21 / 0.08). The panel median 78.39 is not close to the retired blend of 90.37 either | Nil |
| 38 | §1.7 | A claim untrue in most years it covers | Disclosure | "It is why **profit after tax exceeds EBITDA**" | True only in FY2028–FY2030 of its own Table A1; false for FY2023, FY2025, FY2026 and FY2027 | Nil |
| 39 | Register input 37 | A citation whose stated figures are not in the source | Input | "Disclosed pre-tax profit of **3,378.7** against profit after tax of **2,298.2** gives 32.0%" | The filing prints **3,358,865,272** and **2,284,539,004**. The derived 32.0% is right; the two figures quoted are not in the document cited | Nil |
| 40 | Register input 87 | A check declared impossible that the filing supports | Construction | "The audited statements disclose no rate on the EGP borrowings", so kd = sovereign + 200bp = 25.0% | True that no *rate* is disclosed — but finance expenses of **EGP 28,517,057** against an average lease book of ~EGP 143.8mn give an effective **19.8%**, which is the computation Pass 3 asks for | ~1bp of WACC |

### UNVERIFIABLE

| # | Item | What was searched | What would resolve it |
| --- | --- | --- | --- |
| 41 | Damodaran Egypt ERP, January 2026 — CDS 9.41% and rating 13.94%, sovereign spreads 3.40% / 6.37% | The internal construction reproduces exactly: 4.23% + 3.40% × (9.71 ÷ 6.37) = 9.4127%, and 4.23% + 6.37% × 1.52433 = 13.94%. The January-2026 vintage file itself was not opened in this audit | Opening the original ctryprem file for that vintage |
| 42 | Egypt 10-year local-currency yield of 23.00% at 6 August 2026 | Not verified. Note a demonstrable internal inconsistency beside it: §1.1 says "a policy rate of 19.00%" while the register's research trail says "CBE main operation rate 19.50%, held since 2 Apr 2026" | CBE's published yield curve and policy-rate history for the stated date |
| 43 | Replacement cost USD 130/t; justified EV/t 95; Egyptian sector volumes (76 / 65 / 54 / 18.5 / 12.6 Mt); kiln 2.57Mt and grinding 3.80Mt; the 29.3% unchanged-close statistic; the walk-forward record | Not reachable or not independently sourceable here. The company discloses no volume, capacity or utilisation — the report says so, and that is correct | The plant register, the sector trade press, and the supplied price file |
| 44 | Whether a 30 June 2026 reviewed interim exists | Checked: the company's website publishes exactly six PDFs, the latest being the reviewed interim to 31 March 2026. No H1-2026 filing is published | — resolved. The bridge standing on 31 March 2026 is correct, and the study's "six PDFs" is accurate |

---

## Section C — Arithmetic reconciliation

The whole model was rebuilt independently from the workbook's formula graph. Lines that matched are shown as well as lines that did not — that is the proof the audit ran.

### C1 · Cost of capital

| Line | Report | Recomputed | Delta |
| --- | --- | --- | --- |
| Risk-free rate (EGP 10-year) | 23.00% | 23.00% | — |
| Less sovereign default spread (CDS basis) | −3.40% | −3.40% | — |
| Normalised risk-free rate | 19.60% | 19.6000% | ✓ |
| Beta | 1.00 | 1.00 | ✓ |
| Equity risk premium | 9.41% | 9.4127% (= 4.23% + 3.40% × 9.71/6.37) | ✓ |
| **Cost of equity, explicit** | **29.01%** | **29.0100%** | ✓ |
| Debt weight D/(D+E) | 0.52% | 0.5221% (137.566 ÷ 26,349) | ✓ |
| Cost of debt after tax | 19.38% | 19.375% (25.0% × 0.775) | ✓ |
| **WACC, explicit window** | **28.96%** | **28.9597%** | ✓ |
| Terminal risk-free rate | 12.50% | 12.50% (7% terminal inflation + 5.5pp real) | ✓ table, ✘ prose (10.5%) |
| Terminal beta **as printed** | 1.00 | — | — |
| Terminal beta **as used** (Hamada relever, t = 22.5%, D/(D+E) = 20%) | *not printed* | **1.18891** | **undisclosed** |
| **Terminal cost of equity** | **20.82%** | 12.50% + 1.00 × 7.00% = **19.50%** from printed inputs; **20.8224%** from the relevered beta | **✘ does not reproduce from the page** |
| Terminal cost of debt after tax | 11.62% | 11.625% (15.0% × 0.775) | ✓ |
| **WACC, terminal** | **18.98%** | **18.9829%** | ✓ |
| Sovereign risk counted | once | once — spread netted from rf on the same CDS basis the ERP adds back | ✓ **PASS** |

### C2 · Free-cash-flow waterfall and discount factors

Every line reproduces. The discount row reproduces only once the undisclosed mid-period convention is inferred.

| EGP mn | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| --- | --- | --- | --- | --- | --- |
| Revenue — report | 10,550 | 12,015 | 13,316 | 14,560 | 15,848 |
| Revenue — recomputed | 10,549.8 | 12,015.1 | 13,316.3 | 14,560.1 | 15,848.1 |
| EBITDA — report | 4,076 | 4,677 | 5,225 | 5,754 | 6,313 |
| EBITDA — recomputed | 4,075.5 | 4,677.3 | 5,225.0 | 5,754.4 | 6,312.7 |
| D&A — report / recomputed | 135 / 134.9 | 162 / 161.9 | 204 / 204.1 | 263 / 263.3 | 341 / 341.4 |
| NOPAT — report / recomputed | 3,054 / 3,054.0 | 3,499 / 3,499.4 | 3,891 / 3,891.2 | 4,256 / 4,255.6 | 4,628 / 4,627.7 |
| Capex — report / recomputed | (352) / 351.7 | (699) / 698.6 | (1,094) / 1,093.5 | (1,533) / 1,532.5 | (2,022) / 2,021.8 |
| Δ working capital — report / recomputed | (117) / 116.9 | (117) / 117.2 | (104) / 104.1 | (100) / 99.5 | (103) / 103.0 |
| **FCFF — report** | **1,134** | **2,846** | **2,898** | **2,887** | **2,844** |
| **FCFF — recomputed** | **1,134.4** | **2,845.5** | **2,897.7** | **2,886.9** | **2,844.4** |
| Forward cost of capital | 28.96 / 28.9597% | 25.40 / 25.3966% | 22.55 / 22.5461% | 20.41 / 20.4082% | 18.98 / 18.9829% |
| **Discount factor — report** | **0.9484** | **0.8032** | **0.6479** | **0.5334** | **0.4456** |
| **Discount factor — recomputed** | **0.9484** | **0.8032** | **0.6479** | **0.5334** | **0.4456** |
| PV of FCFF — report / recomputed | 1,076 / 1,075.8 | 2,285 / 2,285.4 | 1,877 / 1,877.4 | 1,540 / 1,539.8 | 1,267 / 1,267.5 |

**The convention the discount row actually uses, nowhere stated on the page:** DF₁ = (1.2896)^−(0.417/2) = 0.9484 — the stub discounted at its own midpoint. DF₂ = (1.2896)^−0.417 × (1.2540)^−0.5, and so on: **mid-year on a stub-shifted timeline**. A reader given only "discounted at that year's own forward rate" and "scaled to the 41.7% still unearned" cannot arrive at 0.9484 — the naive year-end factor is 0.7755. At 28.96% the convention is worth roughly 13% of the explicit-window present value.

### C3 · Terminal value, and the implied asset life

| Line | Report | Recomputed | Note |
| --- | --- | --- | --- |
| Replacement-cost invested capital | EGP 24,824mn | 24,823.5 (3.8Mt × USD 130 × 50.25) | ✓ |
| **Disclosed useful life** | 20 years | **20 years — verified**: note 3/2, printed page 8, "Machinery 5%", a scalar among five classes, two of which are ranges | ✓ **PASS** |
| Maintenance charge (capital ÷ life) | *not printed* | EGP 1,241.2mn | |
| **Implied asset life at t = 0** (capital ÷ charge) | *not printed* | **20.0 years** | ✓ matches the disclosed life |
| Terminal working-capital charge | *not printed* | 50.9 (rev₂₅ × 8% × g) | |
| Terminal FCF (NOPAT₅ + D&A₅ − maintenance − ΔWC) | *not printed* | 3,677.1 | Same waterfall definition as the explicit window — ✓ **PASS** on Pass 4's one-definition test |
| Terminal value | *not printed* | 32,834.0 | |
| **PV of terminal value** | **14,631** | **14,631.3** | ✓ |
| **Terminal value as % of EV** | **64.5%** | **64.52%** | ✓, and below the 70–75% disclosure threshold |
| Terminal FCF positive | — | yes | ✓ **PASS** |
| Implied terminal payout (FCF ÷ NOPAT) | — | 0.794 | ✓ within [0,1] |
| **Terminal ROIC** | **19.9%, "BELOW the terminal cost of capital of 19.0%"** | **19.95%, ABOVE the 18.98% terminal WACC** | **✘** |
| **Terminal reinvestment rate** | **"25.1% of profit"**, presented as following from the return | 25.07% — but that is maintenance ÷ terminal NOPAT, an **output**. The identity g ÷ ROIC gives **35.09%** | **✘ declared construction ≠ built construction** |

**The money mismatch, which is the largest single finding.** The explicit window escalates the maintenance charge to nominal money — FY2030 capex is 1,241.2 × 1.6289 = **2,021.8**. The terminal then charges **1,241.2**, the unescalated figure, against FY2030-money NOPAT. The capital charge falls 38.6% at the boundary.

| | Charge frozen in FY2026 money (as published) | Charge in FY2030 money (consistent) |
| --- | --- | --- |
| Terminal ROIC | 19.95% | **12.25%** |
| Terminal WACC | 18.98% | 18.98% |
| Terminal value % of EV | 64.5% | 58.9% |
| **Fair value per share** | **EGP 111.62** | **EGP 99.71** |

On consistent money the terminal return **is** below the cost of capital — which is exactly what the report's prose claims and its model contradicts. The prose is describing the corrected model; the number is not.

### C4 · Enterprise-to-equity bridge

| Line | Report (EGP mn) | Per share | Recomputed | Delta |
| --- | --- | --- | --- | --- |
| PV of explicit five years | 8,046 | 30.85 | 8,045.8 | ✓ |
| PV of terminal value | 14,631 | 56.10 | 14,631.3 | ✓ |
| **Enterprise value** | **22,677** | **86.95** | **22,677.1** | ✓ |
| Plus net cash | 6,555 | 25.13 | 6,555.1 | ✓ arithmetic, ✘ description (finding 23) |
| Less non-controlling interests | (120) | (0.46) | −120 | ✓ arithmetic, ✘ source (finding 20) |
| **Equity value** | **29,112** | **111.62** | **29,112.2 ÷ 260.812477 = 111.62** | ✓ |

The bridge **foots** in both columns, net cash is added rather than subtracted on a net-cash company, the minority is deducted from equity rather than enterprise value, and no dividend is deducted — correctly, since none is declared. Those are all **PASS**. What fails is what stands behind two of the lines, not the addition.

**Cash charged once — PASS.** The debt weight is built on gross debt (0.52%), not net, so the net-cash pathology Pass 7 warns about — negative debt weight, equity weight above one, an operating rate above the cost of equity — does not arise. Free cash flow excludes treasury income and the cash is added at face: charged exactly once.

### C5 · The published sensitivity grids, re-run

| Grid | Result |
| --- | --- |
| Terminal growth 3–7% at 28.96% | 96.33 / 99.39 / 102.89 / 106.92 / 111.62 — **reproduces exactly**, and rises with growth, against a caption saying it falls |
| Net cash 5,055 → 8,055 | 105.87 / 108.75 / 111.62 / 114.50 / 117.37 — **reproduces exactly** |
| Beta | 136.83 / 122.63 / **111.62 at β = 1.00** / 104.87 at β = 1.15 / 99.10 — the *values* match the workbook; the document's *labels* do not (finding 18) |
| EBITDA margin shift ±4% | Published 99.70 / 105.66 / 111.62 / 117.58 / 123.55 (uniform 5.96 steps); recomputed 99.28 / 105.45 / 111.62 / 117.79 / 123.96 (uniform 6.17). Centre matches; wings differ ~0.4% and the caption says 4.50 |
| Bear bound 22.36 | A hardcoded constant. Reproduces at a 9.71% margin, not the stated 8.7%; at an actual 8.7% the model gives 19.25 |

### C6 · Primary-source verification of the input plane

Read by OCR off the rendered pixels of the company's own filings, which carry no text layer. **Every figure below matched to the pound or to the last digit printed.**

| Input | Model / register | Filing | Source |
| --- | --- | --- | --- |
| Revenue FY2025 | 9,089.149688 | **9,089,149,688** | Income statement, printed p.3 |
| Revenue FY2024 | 6,428.011851 | **6,428,011,851** | same, comparative |
| Profit after tax FY2025 | 2,284.539004 | **2,284,539,004** | same |
| Profit after tax FY2024 | 3,072.361811 | **3,072,361,811** | same |
| Gain on sale of investments FY2024 | 1,517.386642 | **1,517,386,642** | same |
| Interest income FY2025 / FY2024 | 171.609009 / 29.990318 | **171,609,009 / 29,990,318** | same |
| Operating profit + finance charge FY2025 | 3,332.646248 | 3,304,129,191 + 28,517,057 = **3,332,646,248** | same |
| Cash at 31 Dec 2025 | 4,762.348666 | **4,762,348,666** | Balance sheet, printed p.2 |
| Total equity at 31 Dec 2025 | 6,020.338736 | **6,020,338,736** | same |
| Total equity at 31 Dec 2024 | 3,735.799731 | **3,735,799,732** | same, comparative (1 pound, the filing's own rounding, disclosed) |
| Total assets / liabilities at 31 Dec 2024 | 5,695.60821 / 1,959.808479 | **5,695,608,211 / 1,959,808,479** | same |
| Lease liabilities at 31 Dec 2025 | 137.565888 | 111,742,265 + 25,823,623 = **137,565,888** | same |
| Paid under capital increase, FY2024 | 1,277.4661 | **1,277,466,100** | same |
| **Share count** | 260,812,477 | Issued capital **EGP 2,608,124,770** ÷ EGP 10 par = **260,812,477** | same. **The count foots** — Pass 1's explicit test |
| Transport and export cost lines | 579.219496 + 185.690219 + 5.614378 | **579,219,496 + 185,690,219** | Note 25, printed p.24 |
| **Disclosed machinery life** | 20 years (5% scalar) | **"Machinery 5%"**, five classes, two of them ranges | Note 3/2, printed p.8 |
| Profit Q1-2026 | 1,114.4800 | **1,114,478,954** | Interim income statement, printed p.3 |
| **No dividend** | payout = 0 | 3,735,799,732 + 2,284,539,004 = **6,020,338,736 exactly**; + 1,114,478,954 = **7,134,817,690 exactly** | **Verified twice against primary sources — PASS** |
| Filings carry no text layer | "zero bytes across its 36 pages" | **0 characters extracted across 36 / 37 / 34 pages** | Verified. The OCR-route disclosure is honest — **PASS** |

**Two figures the filing discloses and the study contradicts:** earnings per share (filed 23.09 and 10.29; study prints 11.78 and 8.76) and the cash balance (filed 1,890,505,077 and 4,762,348,666; study prints 6,708 for both). Both are findings 10 and 11.

---

## Section D — Construction register

What the report declares, what it does, and whether they agree. This is where the serious findings live.

| Element | What the report DECLARES | What it actually DOES | Agree? |
| --- | --- | --- | --- |
| **Primary lens and the others** | "The cash-flow lens is the answer… The other reads are cross-checks published beside it and are not averaged into it"; the four-lens blend is "retired" | The central **is** DCF!B39 alone; the blend appears once as a clearly-labelled memo. No weighting reaches the answer | **Yes** — and this is the report at its best. The one blemish is Appendix C, which still says the asset lens "carries 8% of the weight rather than 15%" and calls Table C1's median close to "the weighted central", while the register keeps live weights summing to 1.00 |
| **Terminal construction** | The reinvestment identity: "the terminal return on capital is 19.9% and the reinvestment rate is 25.1% of profit". Growth destroys value because return sits below cost of capital | A **maintenance charge**: replacement capital ÷ the disclosed 20-year machinery life. The 25.1% is the *output* of that charge, not an input from the return. The identity at ROIC 19.95% would give 35.09% and EGP 101.36. And the model's ROIC (19.95%) is **above** its WACC (18.98%), so growth *adds* value — as its own grid shows | **No** — the declared method, the built method and the stated direction are three different things |
| **Terminal capital charge, money basis** | "the SAME charge the terminal makes" (workbook, beside the maintenance input); "the SAME waterfall the terminal uses, so the two windows cannot mean different things by the same words" | The explicit window charges EGP 2,022mn in FY2030; the terminal charges EGP 1,241mn — the same charge **unescalated**, in FY2026 money, against FY2030-money cash flows. The capital charge falls 38.6% at the boundary | **No** — worth **+11.9%** of value, the largest single finding |
| **Free cash flow definition** | One definition across both windows: NOPAT + depreciation − capital spent − working capital | Genuinely one definition; the terminal substitutes maintenance for capex and is otherwise identical. Depreciation is added back in both | **Yes** — **PASS** on Pass 4's one-definition test |
| **Cost-of-capital path** | "Each forecast year is… discounted at its own forward rate, sliding from the explicit-window cost of capital to the terminal one… One date, one price of time"; the slide's shape "inherited from the assumed borrowing-cost path" | Exactly that. Rates glide 28.96% → 18.98% on the CBE easing calendar, and the terminal is discounted on year five's own cumulative factor | **Yes** — **PASS**, and it is the right answer to Pass 3's "held flat across the perpetuity" trap. But the **mid-period discounting convention beneath it is never disclosed**, and the terminal cost of equity does not reproduce from the beta printed beside it |
| **Sovereign risk** | "The sovereign default spread is therefore netted out of the risk-free rate before the premium is added", on the same CDS basis | Exactly that: 23.00% − 3.40%, with an ERP built from the same 3.40% spread. The rating-basis alternative (6.37% / 13.94%) is published and never mixed in | **Yes** — **PASS**. Counted once, on one basis |
| **Currency split of the debt book** | "THE COMPANY HAS NO BANK BORROWINGS AT EITHER DATE — the whole of its interest-bearing debt is leases under EAS 49" | Verified against the audited balance sheet: the only interest-bearing liability is lease liabilities of EGP 137,565,888, local-currency. The cost of debt is built as local sovereign + 200bp, which is the correct rule for a local book | **Yes** — **PASS**. Pass 3's paired foreign-tranche error cannot arise here, and the report established the book rather than assuming it. Its one gap: it calls the effective-rate check impossible when the filing discloses a finance charge of EGP 28,517,057 against the lease book, giving 19.8% |
| **Inflation path and its escalators** | "Inflation, currency and product price must be ONE path"; the domestic realised price "escalates on the HOUSE inflation ladder at zero real growth, the same index the domestic cost lines carry, so the margin is an OUTPUT" | Exactly that. Domestic price rises 16 / 12 / 9 / 7.5 / 7%, identical to the cost index; the dollar-linked 48.4% of materials rides the FX path; the FX path follows relative PPP at 2.5% US inflation for years 2–5 | **Yes** on the model — **PASS**, and this is the single hardest test in the protocol. **No** on the page: §1.6 still tells the reader prices rise "4.5% to 6.0%" and that this is "a REAL price decline in every single year", which the register itself repudiates |
| **Margins as outputs** | "Revenue and EBITDA are not assumed here… the margin is what falls out at the bottom"; "a test that can fail" | Margin **is** arithmetically an output of the cost stack. But the stack is not independent: realised price was back-solved from disclosed revenue ÷ modelled volume, and fixed cost is the plug (revenue − EBITDA − the two disclosed lines). Volume cancels out of both, so the validation is an identity | **No** on the validation. The margin claim is true; the claim that the build could fail is not |
| **Forecast anchor** | "FY2026 opens at 38.6% against a filed FY2025 of 38.0% and a reviewed first quarter of 2026 that came in ahead of it" | The **margin** claim checks out: Q1-2026 operating margin 39.49% against FY2025's 36.35%. The **revenue** anchor does not: Q1-2026 sales grew 5.9% y/y and annualise on FY2025 seasonality to EGP 9,627mn, against a forecast of 10,550 | **Partly** — the anchor is tested on margin and not on volume, and volume is where it breaks |
| **Capital expenditure** | "the company's own run rate… escalated with domestic costs" | Interpolated from the run rate to replacement-cost maintenance on undisclosed weights, then escalated. FY2030 charge is 4× the escalated run rate | **No** — defensible construction, undisclosed |
| **The bridge** | Stands on the latest disclosed balance sheet; net cash added; minority deducted from equity; "read off the reviewed balance sheet directly" | Stands on the 31 March 2026 reviewed sheet — correctly, and I confirmed no later filing exists. Net cash added, minority from equity, no dividend deducted, and it foots. But the cash figure is the reviewed balance **plus a third of a year's modelled free cash flow**, and the EGP 120mn minority has no line in statements that are the company's separate, not consolidated, accounts | **Partly** — the arithmetic and the structure pass; two of the inputs are described as something they are not |
| **Evidence base** | "built entirely on the company's own audited financial statements, which are published as six PDFs on its own website"; "audited **consolidated** financial statements" | Six PDFs is right, and the numbered register entries are accurate to the pound. But the filings are the company's **Independent** (separate) statements, not consolidated — and the register's own preamble says the statements "could not be retrieved" and that revenue and profit came from press coverage | **No** — the document makes three different claims about its own evidence, one of which ("could not be retrieved") is demonstrably false against the register beneath it |
| **Valuation date** | "issued 7 September 2026, struck on the closing price of 2 September 2026" | Only the price cell moved. The stub (7 months elapsed), the rate quote, the FX quote, the price history, the technical read, the Monte Carlo and both workbook mastheads are all 6 August 2026 | **No** — and findings 14, 15 and 36 are all consequences |

---

## Section E — Verdict

### Counts by pass

| Pass | Total fail | Partial | Unverifiable | Notable passes |
| --- | --- | --- | --- | --- |
| 1 · Input verification | 5 | 1 | — | Revenue, profit, equity, cash, leases, capital increase and the disposal gain all verified **to the pound**. The share count **foots** from issued capital ÷ par. The no-dividend claim verified twice |
| 2 · Market data | 1 | 2 | 1 | Price × shares reconciles to market cap |
| 3 · Cost of capital | 1 | 3 | 1 | Sovereign risk counted **once**, on one basis. Explicit cost of equity and WACC reproduce exactly. The rate is **not** held flat into the perpetuity — the trap most Egyptian models fall into |
| 4 · Terminal value | 4 | — | — | One FCF definition across both windows. Terminal FCF positive, payout inside [0,1], TV/EV 64.5% and below the disclosure threshold |
| 5 · Macro coherence | 1 | — | — | **One inflation path.** Price and cost escalate on the identical ladder at zero real spread growth; FX follows relative PPP. The protocol's hardest test, passed on the model |
| 6 · Forecast anchoring | 3 | — | — | The margin anchor is tested honestly against the reviewed quarter |
| 7 · Lens architecture and bridge | 2 | 3 | — | Nothing is weighted into the central. Bridge **foots**; cash charged exactly once; book value published as a floor, never weighted |
| 8 · Calculation verification | 1 | 1 | — | **The model reconciles to the last cell.** Every printed figure reproduces from the workbook |
| 9 · The page a reader receives | 2 | 6 | — | Tables foot; the bridge reaches the answer it prints |
| 10 · Probabilistic content | 2 | 1 | — | Percentiles are monotonic |
| 11 · The answer itself | — | — | — | See the reverse read below |
| 12 · Completeness | 1 | — | 2 | No later filing exists — the bridge stands on the genuinely latest reviewed sheet |
| **Total** | **23** | **17** | **4** | |

### The three most valuation-critical findings

1. **The terminal maintenance charge is struck in FY2026 money and applied to FY2030 cash flows** (finding 1). The capital charge falls 38.6% at the terminal boundary. Correcting it alone moves the answer from **EGP 111.62 to EGP 99.71** — and flips the terminal return from 19.95% to 12.25%, below the cost of capital, which is what the report's prose says all along and its model contradicts.
2. **The first forecast year opens 9.6% above the latest reviewed period** (finding 3). Q1-2026 sales grew 5.9% year on year; the model forecasts 16.1% for the year. Anchoring the volume path on the reviewed quarter gives **EGP 97.65**.
3. **The forecast is taxed at the statutory 22.5% while the filed effective rate is 32.0%** (finding 2) — a rate the source register itself commits to as an input and which appears in no cell of the model. Applying it gives **EGP 99.58**.

Each is independent of the others. Applied together they give **EGP 74.56 a share**, against a published central of EGP 111.62 and a market price of EGP 100.50.

### The reverse read

Holding every other published driver still, the traded price of EGP 100.50 implies terminal growth of **4.33%** (against 7.00% adopted), *or* an FY2026 EBITDA margin of **35.03%** (against 38.63% adopted and 38.08% filed), *or* a beta of **1.262** (against 1.00 adopted, with a lead-lag estimate of 0.837). None of those is an exotic belief. A reverse read that lands on perfectly ordinary numbers is evidence **against** the report's disagreement with the market — and correcting the single money mismatch in finding 1 lands almost exactly on the traded price.

### The direction of the contested judgements

Nine judgements are each worth more than about 1% of value. **Seven of the nine favour the published figure.**

| Judgement | Adopted | Alternative | Effect of the alternative |
| --- | --- | --- | --- |
| Terminal maintenance money basis | FY2026 money | FY2030 money | −10.7% |
| Forecast tax rate | statutory 22.5% | filed effective 32.0% | −10.8% |
| FY2026 volume | House utilisation path | reviewed Q1-2026 anchor | −12.5% |
| Terminal growth | 7.0% | 5.0% | −7.8% |
| Non-controlling interests | EGP 120mn | reviewer's EGP 2,008mn | −6.5% |
| Terminal debt weight | 20% | observed 0.52% | −2.5% |
| Equity risk premium basis | CDS 9.41% | rating 13.94% | −1.3% |
| Beta | 1.00 | lead-lag 0.837 | **+7.9%** |
| Terminal risk-free rate | 12.5% (7% target) | 10.5% (5% target) | **+9.9%** |

Two genuinely go the other way, and the report discloses both with their prices attached — that is real discipline and it should be said. But seven of nine leaning one way, in a report that concludes the market is 11% too cheap, is the pattern the protocol exists to surface. It is a flag, not a failure; a company can deserve a consistent read.

### Does the headline range survive?

**It collapses.** The arithmetic is immaculate — the model reconciles to the last cell and the inputs trace to the audited filings to the pound — but three independent corrections, each demonstrable from the report's own sources, each move the answer below the market price it claims to beat, and the +11.1% upside that is the study's entire conclusion does not survive any one of them.

### What this audit found in good order

A gate is not worth less for finding a book in good order, and much of this one is. The inputs are genuinely traceable: I read the filings the register cites, off pixels because they carry no text layer exactly as it says, and every figure matched. Sovereign risk is counted once. Price and cost ride one inflation path at zero real spread — the single most common way a well-built model produces a wrong answer, and this one avoids it. The cost of capital normalises rather than freezing a crisis rate into perpetuity. Nothing is weighted into the central. The bridge foots, cash is charged once, and book value is published as a floor and never averaged in. The no-dividend finding is verified twice against the primary record.

What fails is almost never the arithmetic. It is the gap between the page and the model — a terminal described as one construction and built as another, a validation asserted to be falsifiable that is an identity, a discount row nobody can reproduce, a probability map and a price narrative left over from a superseded draft, and a valuation date that moved in one cell and nowhere else.
