# EGCH — response to the forensic verification audit of 13 September 2026

**Subject of the critique:** `EGCH_Valuation_Model_10092026.xlsx` + `EGCH_Bibliography_10-09-2026.docx`
**Subject of this response:** `EGCH_Valuation_Model_05092026.xlsx` + `EGCH_Valuation_Study_05-09-2026.docx`
+ `EGCH_Bibliography_05-09-2026.docx` — the latest edition that exists in this repository.
**Procedure:** `engine/Critique_Response_Prompt.md` v2. Report only. Nothing is implemented.
**Published answer under response:** carried through **EGP 4.0396**, stopped **EGP 8.0388**,
struck at EGP 14.41 on 3 September 2026. Five per cent of the carried-through branch is
**EGP 0.202 a share**; that is the materiality line used throughout and every "immaterial"
below carries a number.

---

## 0. THE AUDITED FILE IS NOT IN THIS REPOSITORY, AND THAT IS ITSELF A FINDING

The critique audits a 10-September-2026 edition. No such edition exists here, on either ref,
anywhere on disk:

```
git branch -a                  -> claude/egch-audit-procedure-nwdrd6, main (identical heads)
git log --all --name-only | grep -i '10092026\|10-09-2026'   -> nothing
find / -iname '*10092026*' -o -iname '*10-09-2026*'          -> nothing
```

The newest EGCH edition committed is **05-09-2026**, and the repository's last commit is
8 September 2026. So an edition was built after this repository's head and never reached it —
which is exactly the failure [R-MERGE-01] names: *a run that ends on a branch has not ended.*

**The two editions are the same lineage and differ in identifiable drivers.** They share the
input register keys and values, the filings, the derived currency path
(55.4303 / 59.8149 / 63.2321 / 66.2269 / 69.2020 — identical to the critique's own recomputation),
the share count 1,986,578,999, gross debt 14,639.005, investment property 2,155.061, the equity
weight 0.6616480, the measured asset age 4.4544 years and the implied life 22.0702 years, and
gross fixed assets 17,022.493. They differ in at least six places, each measured:

| | this edition (05-09) | audited edition (10-09) | evidence |
|---|---|---|---|
| export duty | **10%** of export value | **nil** | the critique's FY26/27 revenue of 12,643.0 reproduces from this edition's 11,673.98 **exactly** when the export leg is grossed up by 1/0.9: 11,673.980 − 8,721.601 + 8,721.601/0.9 = **12,643.047**. EBITDA, EBIT, NOPAT and maintenance capex all differ by precisely the same gross-up |
| long-run real rate | 5.5% → terminal rf 12.50% | 3.5% → terminal rf 10.50% | critique C1 |
| terminal cost of capital | **18.333%** | **16.877%** | critique C1 |
| nitrate price in the terminal | US$280/t (`Assumptions`!C142) | US$408.163/t (= 20,000/49) | critique C3 |
| working capital, year one | **releases** 788.18 | **charges** 690.3 | critique C2 |
| beta | 1.0302 (own regression) | 1.0198 | this edition's `beta_result.json` carries `blume_crosscheck` = 1.0201 |
| carried through / stopped | **4.0396 / 8.0388** | 8.0748 / 11.6065 | — |

Every price below is therefore measured **on the 05-09 edition**, by re-running its own
`compute.py` + `lenses.py` on a copy with one driver moved. The control run reproduces
4.039580816491561 / 8.038774888582243 to the last digit before any edit is applied.

**What I need:** the 10-09-2026 workbook and bibliography, or your instruction that the
05-09 edition is the subject. Where a finding's arithmetic is specific to the audited edition
the row says so and is priced on this one instead.

---

## 1. SELF-AUDIT — DONE FIRST, BEFORE THE CRITIQUE WAS WORKED

Twenty findings. Twelve of them the critique did not raise.

| # | finding | price (carried / stopped) | critique? |
|---|---|---|---|
| **S1** | `Summary`!B36 — the **stopped** branch — is a pasted constant (8.038774888582243) while B34, the carried-through branch, is a live formula `=B5`. One half of a two-sided answer is frozen: move any driver on Assumptions and B34 repriaces while B36 does not. | nil to the number; fatal to a workbook whose READ FIRST says "change a blue cell and the valuation recomputes" | **missed** |
| **S2** | `Fundamental Valuation`!B23:B27 — the whole four-lens field table — are pasted constants, and B29/C29 take MIN/MAX over them. The field is frozen against the lenses it claims to summarise. | nil today; the field stops tracking on any change | **missed** |
| **S3** | The field is computed **two different ways under one name**: `Summary`!B11 = MIN(B5,C5,B7,B8) **excludes** the book lens; `Fundamental Valuation`!B29 = MAX(0,MIN(B23:B27)) **includes** it. They agree at 4.0396 / 15.9877 only by accident of where the book lens happens to sit. | nil today | **missed** |
| **S4** | The `Balance Sheet` sheet does not balance in **any** of its four columns: printed total assets vs printed total equity and liabilities are out by 0.273 / 2.606 / 2.562 / **2.535** (EGP m) at 30-Jun-23/24/25 and 31-Mar-26. | nil | partly — #23 flags one column |
| **S5** | Reserves at 31-Mar-2026 are carried at 6,273.191 against 6,273.201 from the study's own extraction (2,857.030 + 2,467.723 + 417.138 + 531.310). | nil | yes — #24 |
| **S6** | The two lines the balance sheet omits are **in the study's own register and extraction** — `bs_loansext_M9FY2526` 0.238 and `bs_otherfin_M9FY2526` 2.307. The workbook drops what the study holds. With S5 they close the sheet exactly: 2.545 omitted less the 0.010 reserve slip = the 2.535 gap. | nil | the omission yes (#23); that the study holds them, no |
| **S7** | `g_terminal_alt` = **3.0%**, sourced as "two points below the terminal inflation of **5%**". Terminal inflation is **7%**. The Sensitivity sheet labels the row "Two percentage points below it". It is four. | the published downside row reads **2.4481**; constructed as labelled it is **3.1245** — the study **overstates its own worst terminal-growth case by EGP 0.676 a share, 16.7% of the central** | **missed** |
| **S8** | `maint_capex_pct_replacement` = gross assets × 3.95% ÷ **11014.0** — a typed, superseded first-forecast-year revenue — inside a line whose own comment reads "THE THREE FIGURES ARE READ, NOT TYPED". Two of the three are read; the denominator is not. `Cash Flow`!D29 computes **5.76%** on live revenue. | the alternative prints 3.1311; on the live denominator it is 3.1939. **EGP 0.063** | the symptom yes (#27); the cause no |
| **S9** | The crux grid's rows are **not a flat price at the labelled level**: `sensitivity.py` runs `[p+90, p+60, p+30, p+10, p]`. The published central runs US$530 **flat**. | at the model's own stated inputs (long-run US$530, terminal 18.333%) the grid's construction returns **EGP 4.9896** against a published 4.0396 — **+0.950, +23.5%** | #4, for a different reason |
| **S10** | Register `anna_nameplate` = 189,862.77 t/y still reads "no filing states the new plant's capacity", while `Assumptions`!C131/C139 use 264,000 t/y from the Tecnimont/Orascom EPC award and say so. A live register entry contradicted by the model beside it. | nil | **missed** |
| **S11** | `compute.py` says the built-vs-assumed project margin "is carried as a contested construction" and prices it at "**EGP 0.58 a share**". It is not one of the eleven alternatives on the delivered Sensitivity sheet, and `contested_judgements.json` names it among the three constructions that carry **no committed value on the other framing**. So the model's own comment says it is carried and the study's own record says it is not. The real gap is **EGP 1.1281**, not 0.58 — a typed figure in a comment that the model does not reproduce. | disclosure; the underlying judgement is worth **+1.1281 (+27.9%)** | **missed** |
| **S12** | `DCF`!B28 releases capital when terminal growth falls below terminal inflation. `compute.py` refuses to (`if _g_real < 0: _inc_cap = 0.0`). The delivered workbook does not implement the model's own one-sided rule. | nil at the published inputs (g = π, charge = 0); a reader flexing C117 down to 5% gets a **+1,016 EGP m** release the model would not give | #3, same cell, different reason |
| **S13** | The repository's own price library records the **3 September close as 14.50** and the **6 September close as 14.23**. The study strikes at **14.41**, from a spreadsheet supplied by the principal. Two committed artefacts, one session, two closes for the same day. | at 14.50: 4.0279 / 8.0250. At the latest known 14.23: 4.0633 / 8.0667. **EGP 0.012–0.024** | **missed** |
| **S14** | The bridge adds listed stakes "**at market**" at the 31-Mar-2026 carrying amount, while the study's own extraction of the reviewed accounts records the auditor's finding that the ABUK stake **has not been re-marked since 30 Sep 2025 and is EGP 112m understated**. | **+0.0564 (+1.40%)** | #17, in a different and weaker form |
| **S15** | The company's own News page — reached by `curl` this session, HTTP 200 — carries three dated study-year items the Sweep Register does not hold: **14 Apr 2026**, a management target of **EGP 1.5bn** plus agreements for **gas liquefaction and solar power plants**; **30 Nov 2025**, Q1 FY2025/26 profit of EGP 482.7m; **16 Jan 2025**, a silicon-manganese furnace contract with East Investment. The register itself records the IR portal as reachable and lists its "News" section. | the solar and liquefaction agreements are in no driver and no sentence of the study. Unpriced until sized — see bucket 3 | **missed** |
| **S16** | The study's own 9M extraction records six auditor findings and the model consumes **none**: unbooked KIMA-2 interest EGP 27.563m, Damietta urea stock overstated 11.6kt / EGP 116m, unbilled electricity EGP 49.679m accrued, ANNA loan FX loss EGP 197.841m expensed rather than capitalised, the ABUK mark (S14), and the USD loan balance question. | the three balance-sheet ones sum to about **EGP 193m**, ≈ **0.097/share** | **missed** |
| **S17** | The 9M extraction and the workbook disagree on the holding-company loan at 31-Mar-2026: 45,905 vs 45,955 thousand. The balance sheet's own footing shows the **workbook** is right; nothing checks the two against each other. | nil | **missed** |
| **S18** | Note 22 foots other-selling to **176,298,477** (786,462,833 − 610,164,356); the register carries **176.305**. EGP 6.5 thousand. Flagged for a higher-DPI re-read rather than asserted. | nil | **missed** |
| **S19** | The **export duty of 10%** — the single largest haircut in this model — is sourced to "2026 replacement of the shortfall levy with an ad-valorem duty tied to the global price", with **no decree number, no issuing body** and a date of 2026-01-01, while the 2021 levy registered three lines above it cites decree 241 of 2021 by number. | **EGP 2.6831 a share on both branches — +66.4% carried, +33.4% stopped.** It is also the whole revenue difference between this edition and the audited one | **missed** — and it is the largest single number in this response |
| **S20** | The Sensitivity row and the register say maintenance's alternative is "6.11% of revenue"; `Cash Flow`!D29 computes 5.76%. | see S8 | yes — #27 |

**Every repository gate is green.** `check_valuation_gap`, `check_publish_block`,
`check_artefact_currency`, `check_forecast_anchor`, `check_terminal_floor`,
`check_macro_coherence`, `check_bridge`, `check_lens_design`, `check_cost_of_capital`,
`check_prose_figures`, `check_table_footing`, `check_waterfall_assertions`,
`check_sign_convention`, `check_source_integrity`, `check_output_records`,
`check_rebuild_ledger`, `check_delivered_vocabulary`, `check_study_provenance`,
`check_workbook_structure` — all report "no new violations", and the delivered workbook
reproduces the model on **639 of 639 formula cells, 0 unresolvable, 0 unchecked**. Not one of
the twenty findings above was visible to any of them.

---

## 2. THE LEDGER — EVERY FINDING, THE CRITIQUE'S OWN ORDER, PRICED BEFORE JUDGED

Prices are per share against the carried-through branch of 4.0396 unless the row says
otherwise. **P** = premise, **C** = conclusion.

### Section B — the fail table

| # | the critique's claim (its words) | P | C | price on this edition | verdict |
|---|---|---|---|---|---|
| 1 | Register `usd_egp_path` "53.49 / 55.89 / 57.85 / 59.32 / 60.83 … Workbook derives 55.43 / 59.82 / 63.23 / 66.23 / 69.20" | ✔ | ✔ | **nil to the valuation** — the register array is consumed by nothing; `Assumptions`!C41–C49 derive FX live off C38 and the CPI path. It *is* consumed by Lens 4 (row 2) and by every reader of the bibliography | **1 ACCEPT** |
| 2 | "`Relative & Normalized`!B24 … 55.89, 'the second year of the currency path'. Second year is 59.815. Hardcoded override mid-chain" | ✔ | partly | reproduces **exactly**: B24 = 55.89, label identical. Lens 4 moves **4.2896 → 6.199, +44.5%**. But the critique's rider — "it is the LOW of the published field" — is **false here**: the field low is the cash-flow lens at 4.0396 (`Summary`!B11), so the floor does not move. **nil to the field, +1.909 to lens 4** | **2 ACCEPT THE DEFECT, REJECT THE FIX-DESCRIPTION** |
| 3 | "`Sensitivity` row 21 … DCF row 28 releases cash when g < terminal inflation on a capital base of maint × 22.07yr = 54,368 — 25% above the model's own replacement gross base of 43,351 — so g self-hedges" | ✔ | partly | the base reproduces to the pound: 2,463.4376 × 22.0702 = **54,368.5**. But `compute.py` **refuses** the release (`if _g_real < 0: _inc_cap = 0.0`), so the model self-hedges nowhere; only the **sheet** does. **nil to every published number**; the defect is that the workbook does not implement the model | **1 ACCEPT (the sheet), 4 REJECT (the model)** |
| 4 | "Model's terminal WACC recomputes to 16.877%, outside the grid … Grid implies a central +1.03/share (12.8%) above the one published" | ✖ | ✔ | premise fails here — terminal WACC is **18.333%**, inside the 17.0–24.0 axis. Conclusion holds for a **different reason** (S9): the rows are not flat prices. At the model's own inputs the grid returns **4.9896 vs 4.0396, +0.950, +23.5%** | **1 ACCEPT, premise corrected** |
| 5 | "1M median 14.26, spot 14.41, P(above spot) 59.13% … Coherent only against the 6 Aug close of 13.98. Price cell updated to the new strike, simulation not re-run" | ✔ | ✔ | reproduces exactly. `Monte Carlo`!B12 = 14.41 labelled "Spot at the anchor date", B13 = 2026-08-06, and `strike_result.json` records spot **13.98** at that anchor. **nil to the valuation** (the sheet feeds nothing); the published cone is a full cycle behind | **1 ACCEPT** |
| 5b | (same row) "3M check date 2026-11-08 is 3 months after 8 Aug, not 6 Aug" | ✖ | ✖ | **REJECT with the rule**: `horizons.resolve()` is anchor + N calendar months, month-end clamped, **rolled forward to the exchange's first real trading session**. 6 Aug + 3 months = Fri 6 Nov 2026; EGX trades Sun–Thu; the first real session is **Sun 8 Nov**. The roll is correct | **4 REJECT** |
| 6 | "§2: 'EGP 14.41 … 6 Aug 2026'. L2: 14.41 at 3 Sep … One document states two mutually exclusive facts about its own strike" | ✔ | ✔ | reproduces: bibliography §2 prints **"Share price · EGP 14.41 · 6 Aug 2026"** while the study masthead and `Assumptions`!D7 both say the 3 September close and name 13.98 as the 6 August one. **nil to the number, fatal to the evidence trail** | **1 ACCEPT** |
| 7 | "urea 7,509; prior yr 9,254; ammonia 9,114 EGP/t … Filing prints **75.09 / 92.54 / 911.4** … Decimal moved on 3 rows of 5 by two different factors" | ✔ | ✖ | **The critique is right and my first reading was wrong.** The auditor's product cost table (FY2024/25 annual, CAO report p.14) foots against its own totals column at the low reading on **every row**: 75.09 × 513,385 = 38.550m ✔; 911.4 × 318,242 = 290.046m ✔; 8,154.48 × 8,171 = 66.630m ✔; 610 × 35,590 = 21.710m ✔. The comma is a **decimal separator**. I found a **fifth** mis-read the critique missed: prior-year ammonia, register 5,439.1 against a printed **543.91** (×10). **But "none is consumed" is false here**: `an_conversion_cost_FY2425` = 4076.31 − 0.43×9114 = **157.29** and `compute.py:540` consumes it. On the filing's figures it is **3,684.41**, 23.4× higher | **1 ACCEPT, conclusion corrected** |
| 7b | (same row) the price of correcting it | — | — | **EGP 0.0000, 0.00%.** The terminal takes `min(built, assumed)`; correcting the conversion cost moves the built project margin from **65.9% to 36.7%** and its EBIT from 1,761.0 to 981.4, still above the assumed 855.0, so `min()` still picks 32%. The cushion collapses from 906m to **126m** | **1 ACCEPT (the input), effect measured at nil** |
| 8 | "Register: 32% 'replaced' 9 Aug by the disclosed conversion cost … Workbook still runs C148 = 0.32 … The declared replacement never happened" | ✖ | partly | **premise false here, with receipts.** `compute.py:536-556` builds the terminal tonne from the disclosed conversion cost, computes `_ebit_built` **and** `_ebit_assumed`, takes the lower with a written reason, and records the built margin. The replacement did happen; the assumption is retained as a floor. **But** the delivered workbook shows only `Assumptions`!C143 = 0.32 with none of that; the gap is not among the eleven published alternatives, and the study's own record names it as contested with no committed value on the other framing (S11). Adopting the built margin is worth **+1.1281 (+27.9%) carried, nil stopped** | **5 YOUR DECISION** |
| 9 | "`peer_ev_ebitda_high` 9.9 … 'the median of … 4.35, 5.92, 8.2, 11.52, 17.61'. Median = 8.2×; mean = 9.52×. Neither is 9.9" | ✔ | ✔ | arithmetic confirmed: median 8.2, mean 9.52. **nil to the cash-flow central**; the relative lens (the field **high**) moves **15.9877 → 13.9279, −2.060, −12.9%**, and the published field ceiling falls with it | **1 ACCEPT** |
| 10 | "Opening NWC 1,662.024 (net of EGP 1,407m documentary credits); forecast on DIO 165.25 (gross of them) … Two definitions of inventory on the two sides of one subtraction" | ✖ | ✖ | **REJECT with the arithmetic.** This edition's opening NWC is **3,069.424** = 3,378.160 + 1,230.232 − 1,538.968, every line the reviewed balance sheet's own gross figure, and DIO is 2,399.625/5,300.310 × 365 on the same gross basis. **Both sides gross. One definition.** The 1,662.024 the critique quotes is 1,407.4 lower and belongs to its own edition | **4 REJECT** |
| 10b | (the underlying question) should documentary credits be in working capital at all? | — | — | not settled by anything I hold; note 11 of the reviewed statements was not read. **Bound: DIO 165.25 → 114 days is worth +0.5851 (+14.5%) carried, +0.5851 (+7.3%) stopped** | **3 UNPROVEN — note 11 needed** |
| 11 | "`READ FIRST`!A15 … 'worth … more than twice the central estimate itself' … 11.6065 − 8.0748 = 3.5318 = 0.44× … Typed, not computed" | ✔ | ✔ | reproduces and is **worse** here: the gap is 3.9992 against a carried-through central of 4.0396 — **0.99×**, not "more than twice". Confined to the workbook: the study document says "a difference of EGP 4.00 a share", which is right | **1 ACCEPT** |
| 12 | "'terminal inflation plus a STATED real growth of zero' … ~76% of revenue is a USD price held flat; its EGP value grows at the wedge (4.49%), not 7%" | ✔ | partly | premise confirmed — year-five EBIT grows **2.24%** here, against a 7% terminal. Growing the terminal at the currency wedge instead is worth **−1.1053 (−27.4%) carried, −1.1551 (−14.4%) stopped**, not the critique's −0.9%. But [R-MACRO-01] fixes terminal growth as terminal inflation plus a **stated** real growth, and a −2.4% real terminal is a claim that must be written down as such, not arrived at by re-deriving from one revenue leg | **5 YOUR DECISION** |
| 13 | "Window: 1.1157% of revenue. Terminal: current-cost depreciation 2,463 … Two definitions of maintenance capital in one model, unreconciled" | ✔ | partly | the 13.7× step reproduces. **The proposed fix is refused by the house's own module**: putting the terminal on the window's 1.12%-of-revenue basis makes `terminal_value.build()` raise — *"implied payout of terminal NOPAT is 132.8%, outside [0,1]: the terminal distributes more than it earns"*. That is a going concern valued as a liquidation. The **reverse** direction is legitimate and priced: window on the terminal's basis → **3.1939, −0.846, −20.9%**; terminal at book D&A with no replacement uplift → **5.0694, +1.030, +25.5%**. [R-TERM-01] permits the two to differ and **requires the step to be stated**; the study states the window's low rate and never states the step | **2 ACCEPT THE DEFECT, REJECT THE FIX** |
| 14 | "Gross debt 14,639.0 in the weights; net debt 10,032.5 in the bridge; cash added at face … Cash sits on the generous side of both" | ✔ | ✔ | confirmed. Net-debt weights are worth **−0.6110 (−15.1%) carried, −0.7252 (−9.0%) stopped**, against the critique's −11.4%. [R-BRIDGE-01] permits either convention and requires the record to say which; this study weights on gross and adds cash back, which is the generous pairing and is not declared | **5 YOUR DECISION** |
| 15 | "'Held FLAT … at the opening level'; register calls US$545 (7 Aug) 'the export-price anchor'. Model runs US$530" | ✔ | ✔ | reproduces exactly: `urea_fob_egypt` = **545.0** at 2026-08-07 in the register; `export_usd_path` = 530 flat. 530 traces to neither. Worth **+0.7734 (+19.2%) carried, +0.7734 (+9.6%) stopped** | **1 ACCEPT** — and see row 16: 545 is a 7-Aug quote against a 3-Sep strike, so the right fix is a current quote, not 545 |
| 16 | "rf 23.00% (6 Aug), FX 49.79 (7 Aug), urea 545 (7 Aug) … Study strikes 3 Sep … Cost of capital mixes a 3-Sep equity value with a 6-Aug risk-free rate" | ✔ | ✔ | reproduces: bibliography §2 dates the yield 6 Aug and the FX spot 7 Aug against a 3-Sep equity value. [R-COC-01] refuses a sovereign quote older than 14 days unless the staleness is disclosed; it is 28 days and it is not disclosed | **1 ACCEPT** |
| 17 | "Stake at 94.00 (3 Sep); peer multiple at 73.77 / mcap 93,320 (5 Aug). One stock, one study, two dates" | ✖ | ✔ | premise fails here — this edition marks **nothing**: `DCF`!B42 = 1,382.886, the 31-Mar-2026 carrying amount, under the label "**at market**". The conclusion is right by a better route (S14): the company's **own reviewed accounts** record the stake as unmarked since 30 Sep 2025 and **EGP 112m understated**. Worth **+0.0564 (+1.40%)** | **1 ACCEPT, premise corrected** |
| 18 | "Summary: 0.00/share, −100% vs spot. Fund Val: 8.158 … One lens, two published numbers; the clamp is disclosed, the duplication is not" | ✔ | ✔ | reproduces exactly: `Summary`!B6 = 0.0000 (= `Fundamental Valuation`!B18) and `Fundamental Valuation`!B25 = 8.1578, both labelled the book lens. Justified P/B before flooring = **−0.0062** (ROE 6.861% < g 7.0%). **nil to the field** | **1 ACCEPT** |
| 19 | "Note 21 foots to 5,300,309,915 only after −87.165m WIP and −65.173m finished-goods movement … Study's stack = 5,564.641, i.e. +264.3m (+5.0%)" | ✔ | ✔ | **read off the filing and footed**: materials 4,398,635,932 + wages 212,857,408 + services 62,556,751 + depreciation 776,471,327 + indirect tax 2,056,278 + property tax 69,990 − WIP 87,164,710 − finished goods 65,173,061 = **5,300,309,915 exactly**. The study's stack is +264.331m, which decomposes precisely: **+114.120** from charging total D&A (890.591) in cost of sales where note 21 carries **776.471**, **−2.126** from omitting the two tax lines, **+152.338** from ignoring the stock movements. The 114.120 is charged **twice** — once in cost of sales and again inside the disclosed selling and administrative totals. Removing that double count is worth **+0.3997 (+9.9%) carried, +0.3997 (+5.0%) stopped**, against the critique's −0.3 to −0.4 | **1 ACCEPT, magnitude and sign corrected** |
| 20 | "Note 22 line is 'product transport freight **and other commissions**' = 610,164,356 … An ad-valorem commission … escalated per tonne on CPI" | ✔ | ✔ | **read off the filing**: the Arabic line is نوالين نقل المنتجات وعمولات أخرى = 610,164,356, and note 22 foots to 786,462,833 exactly. The CAO report (p.13) records the Abu Qir contract at **12% of the export price** — and finds it is a contract for use of marine and land facilities, **not** a marketing contract, which also makes the workbook's own Peer-sheet description wrong. Upper bound, escalating the whole line on the currency path instead of CPI: **+0.1832 (+4.5%)**. Conservative as the critique says, and now with a number | **1 ACCEPT** |
| 21 | "`export_tonnes` is itself revenue ÷ (385 × 49.0) … Two unknowns, one equation — circular" | ✔ | ✔ | reproduces: `Assumptions`!C8 = 49, sourced "the rate that reconciles note 20 export revenue to the disclosed export price and the implied export tonnage". C8 sets the nitrate USD equivalent (20,000/49 = 408.163) that carries the terminal project leg | **3 UNPROVEN — an independent FY2024/25 average rate is needed to break the circle** |
| 22 | "C138 = 2.5391% (derived at 5%); C108 = 4.4922% (derived at 7%). Terminal inflation is 7% … They do not share one number" | ✔ | ✔ | **confirmed at source**: `inputs.py:107` types `(1 + 0.050)/(1 + 0.024) − 1` while `expected_depreciation` uses `_HOUSE.terminal_inflation` = 7%, and the latter's **prose still says 5%**. Correcting the wedge to 7%: **−0.0199 (−0.49%) carried, nil stopped**. The critique's "negligible, and only by coincidence" is right, and now carries a number. I found a third survivor of the same superseded 5% (S7), worth EGP 0.676 | **1 ACCEPT** |
| 23 | "33,634.477 … Filing: 33,637.022. Loans to others (0.238) and other non-current financial assets (2.307) omitted" | ✔ | ✔ | **read off the audited balance sheet** (FY2024/25 statements, p.19): the face of the statement prints قروض لجهات خارجية اخرى and استثمارات ماليه غير متداوله اخرى as their own lines. The study's own register and extraction hold both. It fails in **all four columns** (S4), not one | **1 ACCEPT, scope widened** |
| 24 | "16,206.086 … Filing foots to 16,206.096" | ✔ | ✔ | confirmed against the study's own 9M extraction: 9,932,895 + 2,857,030 + 2,467,723 + 417,138 + 531,310 = **16,206,096**. With row 23 it closes the balance sheet exactly — an internal coherence test the critique's version passes and this edition's fails | **1 ACCEPT** |
| 25 | "Low multipliers 0.1070 / 0.0355 / 0.0811 … Not monotonic in horizon; no computable meaning for a going concern" | ✔ | ✔ | reproduces: `Summary Financials` D19/E19/F19 give revenue lows of EGP 1,445m, **507m** and 1,220m for FY2028/29–FY2030/31, against centrals of 13,513 / 14,277 / 15,043. A company with EGP 10bn of debt earning EGP 507m of revenue is not a going concern. **nil to the valuation, printed to a reader** | **1 ACCEPT — withdraw or re-derive** |
| 26 | "`roc_terminal` 18% … the terminal uses no reinvestment identity and reads no such cell; model's implied terminal ROIC = 15.3%" | ✔ | ✔ | reproduces: `roc_terminal` = 0.18 with that source text, and `reinv_rate`/`fcff_retired`/`tv_retired` are computed and **published nowhere** — the sanctioned [R-TERM-01] construction is what feeds the answer. An orphan against the register's own claim that there are none. **nil** | **1 ACCEPT** |
| 27 | "6.11% … `Cash Flow`!D29 now computes 5.32%" | ✔ | ✔ | reproduces with a different number: D29 computes **5.76%**, and I found the cause (S8) — a typed, superseded revenue denominator of 11014.0 inside a line whose own comment says nothing there is typed. **EGP 0.063** | **1 ACCEPT, cause supplied** |
| 28 | "`Sensitivity` r19 … 5.4073. Full rating-basis rebuild → 5.4540. 0.9% residual" | n/a | — | this edition's row 19 is the terminal-growth alternative, not the rating basis; the rating-basis row is 17 at **2.5099**, and all eleven alternatives are written by `alternatives.py` through `run_case()`, so each is a re-run of the model rather than a re-description. The critique's residual cannot be tested on an edition I do not hold. **Row 19 does carry a separate defect — S7, the mislabelled terminal-growth alternative, worth EGP 0.676** | **3 UNPROVEN on its own terms; 1 ACCEPT for what row 19 does carry here** |
| 29 | "`#,##0.00` — A number-format string printed where a basis description belongs" | ✔ | ✔ | reproduces **exactly**: `Per-Share & Ratios`!C15 = `'#,##0.00'`. Cosmetic, and it reaches a reader | **1 ACCEPT** |
| 30 | "'Behind a bot challenge that refused every automated read' … The company's **own IR portal** serves it: Shares: 1,986,578,999" | partly | ✔ | **the Directive-10 half reproduces**: WebFetch returns **503** on kimaegypt.com in this session and `curl` returns **HTTP 200, 31,058 bytes**. A probe was not re-run another way. The other half I **could not reproduce**: `InvestorsRelations.aspx` renders empty here and mistnews.com redirects to a login. The sharper point is the study's own: its Sweep Register records the IR portal's sections as including "**Share Price**" and "**News**", and the bibliography records the absence against the **EGX** portal instead. **nil — the figure used is right** | **1 ACCEPT the process defect; 3 UNPROVEN on the portal serving it** |

### Section B — the six unverifiables

| # | claim | verdict and evidence |
|---|---|---|
| **U1** | "the anchor price … the portal quotes 14.17 today (13 Sep 2026), so the strike is ten days old" | **3 UNPROVEN — and worse than the critique says.** The repository's own OHLC library records **14.50 on 3 Sep** and **14.23 on 6 Sep**, against a strike of 14.41 from a supplied spreadsheet (S13). [R-GAP-01 AMENDED] requires the latest known price and makes prices a committed artefact. At 14.23 the study prints 4.0633 / 8.0667 and the gaps are −71.4% / −43.3%. **I could not source a 13-Sep close by any sanctioned route; a supplied price file is needed.** |
| **U2** | "cost-of-capital inputs … The country-premium workbook was not reachable" | **REJECT — it is in the repository.** `engine/egch_study/ctryprem_snapshot.xlsx` and `.pdf` are committed. Every line of the critique's own C1 recomputation agrees with `Assumptions`!C91–C116 to the basis point on this edition's figures too; the cost-of-capital block carries **no finding** and passes the three hard tests (country risk once, the currency-of-borrowing pair, the interest-bearing denominator). |
| **U3** | "beta 1.0198 … Not reproducible without the price history" | **REJECT — reproducible here.** `beta_result.json`: beta **1.0302**, R² 0.2504, s.e. 0.1907, n = 253 weekly, 4.89 years to 2026-07-16, regressor `raw_indices/EG/EGX30.csv` as of 2026-07-22, `conforming: true`, Dimson-adjusted, W-THU week rule, and the superseded composite recorded beside it. The critique's 1.0198 is within 0.001 of this record's **Blume cross-check of 1.0201** — its edition appears to run the Blume-adjusted number. |
| **U4** | "note 11's EGP 1,407m of documentary credits" | **moot on this edition** — nothing is netted; both sides of the working-capital subtraction are gross (row 10). The substantive question stands and is **3 UNPROVEN**: note 11 of the reviewed statements was not read by me either. Bound: **+0.5851 (+14.5%)**. |
| **U5** | "Investment property is added at 2,155.061 while `Assumptions`!D63 names 'the ferrosilicon plant's rent' inside the other-revenue line the DCF capitalises" | **3 UNPROVEN — RESEARCH REQUIRED, and the premise is live here.** `Assumptions`!D63 reads exactly that, `DCF`!B43 adds 2,155.061, and the FY2024/25 statements record the ferrosilicon furnace idle since 2019 and leased from May 2025, with investment property appearing only in FY2023/24 on a revaluation gain of 2,034.573m. Upper bound, removing **all** other revenue from the capitalised stream: **−0.4094 (−10.1%) carried, −0.4094 (−5.1%) stopped**. Note 24 puts FY2024/25 rental income at only EGP 3.871m, so the true figure is far smaller — but it is above the materiality line at its bound and the investment-property note settles it. |
| **U6** | "a disclosure for the period ended 30 June 2026 exists … If it carries FY2025/26 outturn, the run-rated FY2025/26E column is superseded" | **3 UNPROVEN — RESEARCH REQUIRED, and it is the most consequential open item.** The bibliography itself records "the quarterly board and shareholder-structure disclosure reports through 30 June 2026" as indexed and not used. If a fourth quarter exists, [R-ANCHOR-01] anchors the forecast on it. I could not reach the portal's document index this session. |

### Section D — the construction register

| # | the critique's verdict | mine |
|---|---|---|
| D1 | Primary lens & the others — **Yes** | **agree.** The retired blend is on `Summary`!B38 at 5.8733, published and consumed by nothing; [R-LENS-03] satisfied |
| D2 | Terminal construction — **No** (#8, #12, #13) | **agree in part.** #8's premise is false here (row 8) and #13's fix is refused by the module (row 13). The substance that survives is real: the step between window and terminal maintenance is **not stated**, and the study's own argument for the window's 1.12% ("the replacement cycle sits far beyond the terminal year") contradicts a terminal charging EGP 2,463m |
| D3 | Cost-of-capital path — **Yes** | **agree.** Verified to the basis point on this edition |
| D4 | Currency split of the debt book — **Yes** | **agree.** 0.3139% local / 99.6861% dollar, verified against the reviewed sheet |
| D5 | Inflation path & escalators — workbook yes, **register no** | **agree**, and one more: the superseded 5% survives in **three** places, not one (rows 22, S7) |
| D6 | Forecast anchor — **Partly** | **agree, with the record.** `forecast_anchor` declares `input_cost_outpacing_price`, carries the cost-stack disclosure and the like-for-like measurement (cost per unit of revenue 54.059% FY2022/23 → 61.613% FY2024/25), and `check_forecast_anchor` passes. The critique's "mirror case" reading of the FY2025/26E → FY2026/27 step is fair and unpriced by either of us |
| D7 | The bridge — **Yes, subject to U5** | **agree, subject to U5 and S14** — the stakes are not at market |
| D8 | Margins as outputs — **Yes** | **agree.** `Segments` sets no margin; every cost is a physical unit times a price times a named escalator |
| D9 | Guidance — scored, never consumed — **Yes** | **agree.** `budget_net_9M` is registered and read by nothing |
| D10 | Clamps — **Partly** | **agree** — row 18 |

### Section E — the verdict summary

| # | claim | verdict |
|---|---|---|
| E1 | "The maintenance-capital definition is not one definition … on the window's own basis the model prints 12.29" | **defect accepted, remedy rejected** — row 13. On this edition the window's basis makes the module refuse |
| E2 | "The 32% project cash margin the register says was retired is still running the model" | **premise false here** — row 8. The disclosed cost **is** consumed; the 32% is a floor with a written reason |
| E3 | "The macro path is not one path … Lens 4, which sets the published field's floor, is hardcoded to it" | **half accepted** — row 2. Lens 4 **is** hardcoded; it does **not** set the floor here |
| E4 | "Fifteen choices move the answer by more than 5% … Nine are resolved toward the higher value and six toward the lower … This report does not resolve every contested judgement the same way" | **accept, and it is the fairest paragraph in the critique.** Measured on this edition's own eleven alternatives, the study takes the **higher** side on 8 and the **lower** on 3 (binomial p = 0.227, no lean at the 5% level). But its [R-ENF-05] sign-test record carries **one** judgement and says so in its own words, naming three more — the ANNA terminal margin, the ANNA nameplate and the premium basis — as contested with **no committed value on the other framing**. `check_output_records` passes because the study declares what it has not measured; that is honest, and it is not the same as having measured it |
| E5 | "put the terminal maintenance charge on the same basis the explicit window uses and the model prints 12.29 unaided … A reverse read that lands on the traded price without leaving the report's own assumptions is evidence against its disagreement with the market" | **reject the route, accept the principle.** The route is the one the module refuses at a 132.8% payout. The principle is [R-GAP-02]'s own and this study is **HELD** under it |
| E6 | "Does the headline range survive? It shifts materially … it belongs in the low-to-mid teens" | **not on this edition.** Every non-judgement correction applied together moves the answer to **4.5004 / 8.5239** — **+11.4% / +6.0%** — against the latest known price of 14.23 that is **−68.4% / −40.1%**. The study stays held. The judgement calls in bucket 5 are worth up to another +2.68 on the duty alone, and they are yours |

---

## 3. COUNT RECONCILIATION

**78 findings raised, 78 answered, 0 unaddressed** — on 81 rows, because three findings
carry two separable claims each and each claim gets its own answer.

56 fail-table rows · 6 unverifiables · 10 construction-register rows · 6 verdict-summary
claims = **78 raised**. Rows 5, 7 and 10 each carry a second, separable claim, answered as
5b, 7b and 10b, so the fail table takes **59 answers** and the ledger runs to **81 rows**.
No two rows were merged. Rows 2/E3, 3/S12, 4/S9, 8/E2,
13/E1 and 27/S8 are the same object seen twice — each is answered where the critique raises it
and cross-referenced, never silently combined.

## 4. BUCKETS

**1 — ACCEPT AND IMPLEMENT (23):** critique rows 1, 4, 5, 6, 7, 7b, 9, 11, 15, 16, 17, 18, 19,
20, 22, 23, 24, 25, 26, 27, 29, 30 (process half), 3 (the sheet half) — plus self-audit S1–S6,
S8, S10, S11, S13, S14, S17, S18, S20. Applied together, and taking the latest known price:
**carried 4.0396 → 4.5004 (+11.4%), stopped 8.0388 → 8.5239 (+6.0%).**

**2 — ACCEPT THE DEFECT, REJECT THE FIX (2):** row 2 (the hardcode is real; it does not set the
field floor — link the cell, do not re-describe the field) and row 13 (the two maintenance
definitions are real; the terminal must **not** go onto the window's basis, because the module
refuses it at a 132.8% payout — **state the step** instead, as [R-TERM-01] requires).

**3 — UNPROVEN, RESEARCH REQUIRED (6):** U1 (a current supplied price file), U4/10b (note 11),
U5 (the investment-property note — bounded at −0.41), U6 (any 30-June-2026 disclosure), row 21
(an independent FY2024/25 average rate), row 30's portal claim. Plus **S15** — the company's own
News page carries a gas-liquefaction and solar agreement and a management target of EGP 1.5bn
that no driver and no sentence of this study consumes.

**4 — REJECT, WITH RECEIPTS (4):**
- **Row 5b** — the 3-month check date. `horizons.resolve()` rolls 6 Nov 2026 (a Friday) forward to the exchange's first real session, Sunday 8 Nov. The rule, not an opinion.
- **Row 10** — the working-capital basis. Opening NWC here is 3,378.160 + 1,230.232 − 1,538.968 = 3,069.424, every figure the reviewed sheet's own gross line, and DIO is struck on the same gross basis. One definition, both sides.
- **U2** — the country-premium workbook is committed at `engine/egch_study/ctryprem_snapshot.xlsx`.
- **U3** — the beta is fully reproducible from `beta_result.json`, attested by `assert_beta_provenance()`, index file `raw_indices/EG/EGX30.csv`.
- *(and the parts of rows 3, 7, 8, 17 whose premises fail, each corrected in place rather than merely dismissed.)*

**5 — YOUR DECISION (5), priced both ways:**

| judgement | as published | the alternative | worth (carried / stopped) | my recommendation |
|---|---|---|---|---|
| **Export duty** (S19) | 10% ad valorem on export revenue | nil, as the audited edition runs it | **+2.6831 / +2.6831** (+66.4% / +33.4%) | **Source it or drop it.** A haircut worth two-thirds of the answer cannot rest on a source field that names no instrument. If the decree exists, cite it; if it does not, the duty goes and the answer moves to 6.72 / 10.72 |
| **Export price** (row 15) | US$530 flat, unsourced | the register's own US$545 at 7 Aug, or a 3-Sep quote | **+0.7734 / +0.7734** | re-quote at the strike date rather than adopt a 7-August number; the anchor should be as current as the price it is compared with |
| **Project cash margin** (row 8, S11) | `min(built 65.9%, assumed 32%)` | the built margin from the disclosed cost table | **+1.1281 / nil** | keep the floor, **commit the other framing** — the model's own comment says the gap is carried, the study's own record says it is not, and correcting the mis-read ammonia cost (row 7) leaves only EGP 126m between the two |
| **WACC weights** (row 14) | gross debt, cash added back at face | net-debt weights | **−0.6110 / −0.7252** | declare the convention in the bridge record either way; [R-BRIDGE-01] permits both and forbids silence |
| **Terminal growth** (row 12) | 7% nominal = terminal inflation, real growth stated at zero | the revenue's own currency wedge, 4.49% | **−1.1053 / −1.1551** | keep 7% and **write the real number down** — a −2.4% real terminal is a claim, and [R-MACRO-01] says it must be stated in real terms, not reverse-engineered from one revenue leg |

---

## 5. WHAT I AM ASKING FOR

1. The **10-09-2026 workbook and bibliography**, or your instruction that the 05-09 edition is the subject.
2. A **current supplied price file** — `engine/prices/SUPPLIED_{DD-MM-YYYY}.json`. The committed one is ten days old and disagrees with this repository's own library about the 3 September close (14.41 vs 14.50).
3. Your ruling on the **five judgement calls** above.
4. Approval to implement buckets 1 and 2, and to run the research in bucket 3.

Nothing has been implemented. Under [R-GAP-02] this study is **HELD** and stays held: on the
latest known price of 14.23 both branches sit 68.4% and 40.1% below it, and
`scripts/check_publish_block.py` reports 0 of 24 studies may publish.

<!-- CRITIQUE RESPONSE — EGCH — 13-09-2026 — report only, nothing implemented -->
