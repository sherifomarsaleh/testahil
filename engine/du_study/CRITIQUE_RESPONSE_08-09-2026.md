# DU — response to the 8 September 2026 forensic audit

**Source of the critique:** *"Emirates Integrated Telecommunications (DFM: DU) — Valuation
Study Audit"*, an independent AI-authored forensic audit dated 8 September 2026, run against
`DU_Valuation_Study_09-08-2026_public.docx`, `DU_Valuation_Model_09082026_public.xlsx` and
`DU_Bibliography_09-08-2026.docx`.

**Procedure:** `engine/Critique_Response_Prompt.md` v2. Self-audit first; every finding on its
own row; every finding priced before it is judged; premise split from conclusion; rejections
carry receipts; anything over 5% of the central re-derived from primary sources; buckets last.
**Nothing is implemented in this pass.** This document is the stop-and-report of step 8.

**Published central under review:** AED 16.5778 (cash-flow lens). **Published spot:** AED 11.36.
**Latest known close:** AED 11.38, 7 September 2026, `engine/raw_ohlc/AE/DU.csv`.

---

## 0. HONESTY ABOUT THE ORDER OF WORK

The procedure asks for the self-audit before the critique is read in detail. The critique
arrived as the attachment and was read first — that is stated rather than dressed up. What was
genuinely independent is the **work**: the whole chain was rebuilt from the committed inputs in
a script that does not import `compute.py`, the delivered workbook was read cell by cell from
its own XML, the price library and the index files were read directly, and the beta was
re-derived through the sanctioned house routine. Fifteen of the findings below are not in the
critique, and one of them is the largest single number in this document.

---

## 1. SELF-AUDIT — what we found ourselves

Sixteen findings. Column "in critique?" says whether the outside audit also caught it.

| # | Finding | Priced | In critique? |
|---|---|---|---|
| **S1** | **THE BETA IS HAND-ROLLED AND WRONG.** `beta_reg.py` is a study-local regression script. SIGCM clause 6 and CLAUDE.md both say never hand-roll one; `own_stock_beta()` is the only sanctioned route. Run properly — `own_stock_beta('DU','AE','DFM')` — the answer is **beta 0.5569** (n 249, R² 0.141, SE 0.149, Dimson-corrected for thin trading, week rule W-FRI), not the published **0.488**. The local script applies no Dimson correction and uses its own weekly sampling. | **−AED 1.046 / −6.31%** | **NO** |
| **S2** | The regressor is `engine/du_study/ADXGI_daily.csv` — a reformatted copy of the FADGI series sitting inside the study directory, not `engine/raw_indices/AE/FADGI.csv`. This is the exact defect [R-IDX-01] was written for (ADXGENERAL.csv, ADNOCDIST, ADNOCDRILL): the right number with provenance that cannot resolve. | 0 on value; provenance unresolvable | **NO** |
| **S3** | The published DFM cross-check (0.4716) regresses against `engine/du_study/DFMGI_daily.csv` — **1,099 rows** — while the repository holds `raw_indices/AE/DFMGI.csv` at **2,307 rows**. The alternative beta is not reproducible from the registered file. | 0 on the central; a cross-check that cannot be checked | **NO** |
| **S4** | The interim-index disclosure is **never quoted**. `wacc_builder.index_interim_note('AE','DFM')` ends "Quote this note wherever the beta is quoted, and never call such a beta conforming." The study calls FADGI "the base market index for the UAE"; `beta_result.json` says the same; neither document carries the note. | 0 on value; a standing disclosure omitted | **NO** (F25 gets it backwards) |
| **S5** | **THE SENSITIVITY GRIDS RUN THE RETIRED TERMINAL.** `dcf_at()` in `compute.py` still builds `tv = NOPAT(1+g)(1−g/ROIC)/(W−g)` — the reinvestment identity [R-TERM-01] retired — while the headline runs the sanctioned module. Reproduced exactly: the grid centre 17.24187 is the retired terminal, netted of the AED 0.66 and rolled, to five decimals. This is the real cause of the wedge the critique attributes to the dividend. | +AED 0.664 on every discount-rate cell | Symptom yes (F5/F6), cause **NO** |
| **S6** | The delivered workbook's `Assumptions!B66:F66` carries **355 / 350 / 345 / 340 / 335** for lease replacement, feeding `DCF!B13:F13`; the committed model carries `rou_repl = [0,0,0,0,0]` and the document's Table 2 prints zeros. Workbook and document disagree on a printed row. | 0 (memo row, not deducted) | **NO** |
| **S7** | `Assumptions!A93` reads "Days from the 31-Dec-2025 valuation date to the 07-Aug-2026 anchor" over a value of **246**. 31-Dec-2025 to 7-Aug-2026 is 219 days; 246 is 3 September. | see F2 | premise yes (F2) |
| **S8** | `Assumptions!A96` labels the 12.9× multiple "GCC telecom **peer median**" — the fourth place in the delivery that claims a median §1.3 explicitly disclaims. | 0 on value | partly (F19, one place) |
| **S9** | Appendix B1 also prints a superseded **e& at ~20.7×** (the register re-derives 15.7×) and a superseded **stc yield ~5.2%** (the register says "SUPERSEDES 5.2% (stc, aggregator)"). The critique caught only the Mobily row. | 0 on value | partly (F18) |
| **S10** | AED 11.36 entered through `engine/prices/SUPPLIED_03-09-2026.json`, which records it as the 3-Sep close. Our own library says the 3-Sep close was **11.12** and that 11.36 is **31 August**. That price file carries a `corrections` block — used for SWDY on 6-Sep against the library — and DU was never put through the same test. | see F1 | consequence yes (F1), **cause NO** |
| **S11** | The latest session in the library is **7 September, close 11.38**, and `assets/data.js` carries a DU cycle-2 roll-forward struck on it that same day. The study is a session behind its own repository, and the ticker record still shows `px: 11.36, pxDate: "2026-09-03"`. | −0.2pp on the gap | partly (F30) |
| **S12** | §3 publishes a one-month cone "to 2026-09-07". That date has passed; the close was 11.38, below the published 25th percentile of 11.71. The study presents a matured, already-graded forecast as forward-looking. | 0 on fair value | **NO** |
| **S13** | The false lease-replacement claim appears a **third** time, in §A.3: "the lease book is held flat with replacement charged at depreciation." | see F7 | 2 of 3 places (F7) |
| **S14** | The study commits **no** `bridge_record`, no `inflation_inputs` block, no cost-of-capital schedule record, no `forecast_anchor`, no ground-up record and no `diagnostics.json` (so no published reverse read and no sign test). DU sits on six ratchets — anchor, artefact, bridge, coc, macro, output — so these are knowingly outstanding rather than new; they are listed because the critique's own Section E performs our sign test for us and we should not need an outsider to do that. | 0 direct | **NO** |
| **S15** | The valuation uses the **rounded** beta 0.488 (workbook `C73`), not the regression's 0.4879596 that the four-field register publishes. Ke 6.53352% against 6.53335%. | AED 0.005 (0.03%) | **NO** |
| **S16** | `GAP_REVIEW_04-09-2026.md`'s own lever table reads 17.1542 → 16.7705 → **16.8563** while its header audits a central of **16.5778** and `rebuild_ledger.json` — corrected the same day, its own note saying "THIS LEVER READ 16.7705 … AND WAS WRONG" — reads 17.1542 → 16.4935 → 16.5778. The review's workings do not reach the answer it audits. | 0 on value; the review is stale | **NO** |

**A self-audit that finds nothing is a failed self-audit.** This one found the largest number in
the document (S1, −6.31%) and the correct diagnosis of the critique's own headline finding (S5).

---

## 2. THE LEDGER — every finding, in the critique's order, priced before judged

Prices are AED per share against the published central of 16.5778 unless stated.
"P" = premise, "C" = conclusion.

### Total fails

| # | The critique's claim (its words) | Price | P | C | Verdict |
|---|---|---|---|---|---|
| **F1** | "The anchor price is dated wrongly in all three documents" — 11.36 "is the 31 August 2026 close … neither the 7 August close the study prints … nor the 3 September close the register certifies it as." | 0 on fair value; the **+45.9% headline gap is struck against a price with no correct date anywhere in the delivery** | ✔ | ✔ | **ACCEPT.** Verified against our own library: 7-Aug 12.30, 27-Aug 11.54, **31-Aug 11.36**, 1-Sep 10.88, 2-Sep 11.04, 3-Sep 11.12, 4-Sep 11.26, 7-Sep 11.38. Cause is S10, not carelessness in the document. Its restruck "+34.1% on the 7-Aug anchor" is arithmetic on a price we do not use and is not adopted. |
| **F2** | "The printed anchor-accretion equation is false on its face" — "(1+Ke)^(219/365) = 1.0436" | −AED 0.081 (−0.49%) if the printed exponent were honoured | ✔ | ✔ | **ACCEPT.** Recomputed: 1.065335^(219/365) = 1.038704 → AED 16.4973. 1.065335^(246/365) = 1.043578 → 16.5778. The printed factor is right and the printed exponent is wrong, in the document AND on `Assumptions!A93` (S7). |
| **F3** | "The price cone is simulated from a spot of AED 12.29, not the AED 11.36 the page prints" | 0 on fair value; **§3, §6 and the level-touch ladder are invalid as published** | ✔ | ✔ | **ACCEPT, with a better receipt than the critique had.** It solved 12.294 from the medians; our own `strike_result.json` says `"spot": 12.30, "anchor_date": "2026-08-07"` outright. Add S12: that cone has since matured. |
| **F4** | "The technical table compares a 31 August close against 7 August moving averages" | 0 on fair value; **all four moving-average gaps and the §2 narrative are wrong** | ✔ | ✔ | **ACCEPT.** Recomputed from the library. As of 7-Aug (close 12.30): MA20 12.180 → +0.99%, MA50 11.916 → +3.22%, MA100 11.220 → +9.62%, MA200 10.600 → +16.04%. As of 31-Aug (close 11.36): MA20 11.777 → **−3.54%**, MA50 11.924 → −4.73%, MA100 11.460 → −0.87%, MA200 10.775 → **+5.43%**. The published levels are 7-Aug; the published gaps are 11.36 against them. The 52-week closing high of 12.76 on 7-Jul-2026 is verified. |
| **F5** | "The sensitivity grids do not return the headline" — the gap is "the AED 0.66 of ex-dividends the headline nets and these grids do not" | +AED 0.664 on every discount-rate cell (+4.0%) | ✔ | ✘ | **ACCEPT THE DEFECT, REJECT THE REASON.** Receipt: `dcf_at()` in `compute.py` line 1762 **does** subtract `V['div_between']` and **does** apply `ROLL`. Rebuilt independently, the retired reinvestment-identity terminal, netted and rolled, returns **17.24187** against the published grid cell **17.24187**. The gap is 0.66407, not 0.66 — and it is the retired terminal [R-TERM-01] left running inside the grid function when the headline terminal was rebuilt on 4 September. Worse than alleged: the grids are built on a construction the protocol retired. |
| **F6** | "Table 10 publishes two different base values for the same base case, and understates the risk-free question sixfold" (−0.14 vs −0.80) | see below | ✔ / ✘ | ✔ | **SPLIT.** *Half accepted:* Table 10 does print 16.58 in one row and 17.24 in another for one base case — real, and it is the beta row that is on the wrong basis. *Reason rejected:* the rf alternatives are **not** un-netted. `dcf_at_rf()` subtracts the dividend and rolls. *Conclusion right by accident:* re-derived like-for-like on the sanctioned terminal — rf 4.69% → **15.81** (−0.77, not −0.14); rf 4.13% → **18.03** (+1.46, not +2.19); the 3.779% debut → **19.78** (+19.3%, not +24%); beta 0.80 → **12.59**, not 13.07. |
| **F7** | "The lease construction is declared in two places and inverted in both" | charged in the window −2.00%; ROU out of the terminal +1.51%; both as declared **−0.50%** | ✔ | ✔ | **ACCEPT, and it is three places not two** (S13). Receipts: `DCF!B13` label "NOT deducted (leases are debt)" against Table 2's caption "lease replacement **is charged**"; `DCF!A74` "Plus **owned** depreciation" against `DCF!C74 = 2582.418423`, which is PP&E 1,926.922 + amortisation 320.497 + right-of-use 335.000 exactly. The study's **own** `terminal_record` says "THE FULL charge — property, intangibles and right-of-use alike". The record is right; the prose and the cell label are stale. |
| **F8** | "Catalyst 1 reprints, verbatim, the error the study says it corrected" | 0 on fair value; the study's most prominent forward claim is one it retracts on page 508 | ✔ | ✔ | **ACCEPT.** Both sentences are in the delivered document: §1.7 "du published its own disclosure … on 24 July 2026"; catalyst 1 "The **other** operator has disclosed … du's mirroring disclosure … is the single most valuable sentence the company can publish." |

### Partial fails

| # | The claim | Price | P | C | Verdict |
|---|---|---|---|---|---|
| **F9** | Dividend mislabelled "the AED 0.66 final dividend" in three artefacts; the final was 0.40 | 0 on value; label wrong in Table 3, `DCF!A64`, `Relative & Normalized!A9` | ✔ | ✔ | **ACCEPT.** The register has it right ("0.40 final + 0.26 interim"); the labels do not. |
| **F10** | Table 3's note still says the 0.26 interim "stays in the share" while `Assumptions!C92 = 0.66` nets it | 0 on value; direct self-contradiction | ✔ | ✔ | **ACCEPT.** The register records the 17-Aug correction from 0.40 to 0.66; the pre-correction sentence was left standing in two documents. |
| **F11** | Catalyst 2 says the licence outcome "is due at press time" when §1.7 reports it renewed for 20 years | 0 on value | ✔ | ✔ | **ACCEPT.** Same shape as F8. |
| **F12** | §A.3 says cash declines "in every year of the forecast with no rebuild" against a printed 2,023 → 1,899 → 1,856 → 1,979 → 2,158 | 0 on value | ✔ | ✔ | **ACCEPT.** Three years of decline, two of rebuild. Prose contradicts the table above it. |
| **F13** | The ARPU mix decomposition mismatches periods; per-leg erosion is −5.3%/yr, not −2.4% | the priced downside case (−2.5%/yr → 13.53) is calibrated on the smaller figure; at −5.3%/yr it is materially lower | ✔ | ✔ | **ACCEPT.** Recomputed from our own register: Q4-2025 65.3 → Q2-2026 63.4 is −2.91% over two quarters = **−5.73%/yr**; FY2025 average 63.3 → Q2-2026 63.4 is +0.16%. The two legs of the study's own sentence sit on different period pairs. |
| **F14** | Table 9's rows do not reproduce its total: 96.4%×6.53% + 3.6%×5.10% = 6.48%, not 6.40% | 0 on value; **a reader cannot reproduce the printed cost of capital** | ✔ | ✔ | **ACCEPT.** Recomputed: 6.4785%. The after-tax step (5.10%×(1−43.57%) = 2.878%) is in the workbook and not in the table. The terminal 6.17% cannot be reproduced at all — the terminal cost of debt 4.90% and terminal Ke 6.35% appear nowhere in Table 9. |
| **F15** | Terminal inflation of 2.00% appears in no register layer | ±AED 1.5–1.7 at ±50bp on the study's own grid | ✔ | ✔ | **ACCEPT.** The Country layer holds 14 inputs, none of them inflation; 2.0% reaches the model through `Assumptions!C81` "UAE house macro path" with no value/date/source row. Compounds with S14 (no `inflation_inputs` block). |
| **F16** | `Assumptions!C71/C72` labelled "rating basis" carry the market-spread values | 0 on value (country risk still enters exactly once) | ✔ | ✔ | **ACCEPT, scoped to the workbook.** The document's Table 9 says "MARKET-observed" and is correct; the workbook labels say "rating basis" over 0.0004 and 0.0429, which are the market figures (the rating pair is 0.0042 / 0.0487). |
| **F17** | The register's judgements table carries stale beta 0.472 / composite 0.394 and terminal growth 2.5% | 0 on value; the artefact a reader checks the study with is wrong | ✔ | ✔ | **ACCEPT.** Adopted values are 0.488, 0.400 and 2.0%, as the register's own House-layer entries state four hundred lines earlier. |
| **F18** | Appendix B1 reprints Mobily at ~15.5× / ~2.9% | 0 on value | ✔ | ✔ | **ACCEPT, and extend** — see S9: e& ~20.7× and stc ~5.2% are superseded in the same table. |
| **F19** | Expert 1's 15.0× is defended as "set at the peer median" while §1.3 says no peer median is claimed | AED 0.66/share per turn on that expert's lens | ✔ | ✔ | **ACCEPT, and it is four places not one** — §C.4, §4 ("at the peer median multiple"), and `Assumptions!A96` (S8). |
| **F20** | §C.5 says "two of its three members set the terminal on a market multiple"; only Expert 1 does | 0 on value | ✔ | ✔ | **ACCEPT.** Expert 2 capitalises at the terminal cost of equity, Expert 3 at the cost of capital; the panel median is Expert 2 at 16.361. |
| **F21** | Three hardcodes in the workbook: `DCF!C74`, and the two constants inside `DCF!C76` | 0 at base; **the workbook reprices away from the engine off-base** | ✔ | ✔ | **ACCEPT.** Read straight off the XML: `C74 = 2582.418423`; `C76 = -C71*10429.868530-C70*-1297.459758`. This breaches the workbook's own READ FIRST promise and SIGCM clause 7 ("never hardcoded values"). |
| **F22** | The bear case's "terminal growth 2.0%" is the base rate, so the bear carries no growth adjustment | on the sanctioned terminal +100bp of terminal growth is worth **+AED 4.57**; the bear takes none of it and the bull takes all of it | ✔ | ✔ | **ACCEPT.** Recomputed: g 1.5% → 15.03, g 2.0% → 16.58, g 3.0% → 21.14. Its "+AED 4.02" is the retired grid's number. |
| **F23** | The dividend cross-check (0.696/4.89% = 14.24) carries no anchor roll and no dividend netting | **−AED 0.040** on that cross-check if put on the study's own clock | ✔ | ✔ | **ACCEPT.** One lens on a different clock from the other four. Small, and it is stated with the number. |
| **F24** | The AED 12.76 "floor" is a justified price-to-book of 5.74×, not book value; book is 2.24 | 0 on value; the word is wrong and it sits above the price and above two lenses | ✔ | ✔ | **ACCEPT.** [R-LENS-03] calls **book value** the disclosed floor. 12.76 is a sustainable-ROE construction. |
| **F25** | "Wrong exchange's index, on a stated reason that is not a market rationale" | ≈ −AED 0.2 on its own account; but see S1 | ✘ | ✘ | **REJECT the finding as framed; ACCEPT the adjacent defect it points at.** Receipt: the ADX regressor for DFM names is a **standing, measured, labelled house exception** (`wacc_builder.INTERIM_INDEX`), adopted 10-Aug-2026 and held open 23-Aug-2026, on evidence that FADGI explains the DFM names better than the ADX names it covers (median R² 0.240 vs 0.127). It is not "a stated reason that is not a market rationale". What the critique should have found, and did not, is **S4**: the note ends "Quote this note wherever the beta is quoted, and never call such a beta conforming", and the study does neither. And **S1**: run through the sanctioned routine on that same regressor the beta is 0.5569, not 0.488. |
| **F26** | Table 11's "base" marker sits over the third value; for beta and fiscal take the base is the second | 0 on value; misdirects on 2 of 8 rows | ✔ | ✔ | **ACCEPT.** Verified in the workbook: beta grid (0.35 / **0.488** / 0.62 / 0.65 / 0.80) and tax grid (0.40 / **0.4357** / 0.47 / 0.50 / 0.531) both have the base second. |
| **F27** | "every 0.10 on beta is worth roughly AED 1.34" is one linear number for a convex relation, quoted at its shallowest point | the true local slopes on the sanctioned construction are **1.93 / 1.48 / 1.28 / 1.10** per 0.10 across 0.35→0.80 | ✔ | ✔ | **ACCEPT.** 1.34 is the average over 0.488→0.80 on the retired grid. |
| **F28** | The AED 1.8bn combined floor is named everywhere and modelled nowhere | **does not bind**: the modelled charge runs 2,484 / 2,565 / 2,691 / 2,809 / 2,931 against a floor of 1,800 | ✔ | ✔ | **ACCEPT the finding, with the number the critique did not compute.** It is named as a key feature and is not in the model and is not listed among what the disclosure holds that the model does not consume. Immaterial in the base case — with the arithmetic beside the word. |
| **F29** | The "+4bp" sovereign spread and the 16bp implied by 4.48% AED vs 4.32% UST are mutually inconsistent | **≈ −3bp on Ke ≈ −AED 0.07 (−0.4%)** | ✔ | ✔ | **ACCEPT.** Two sourced figures on two dates (30-Jul auction vs 7-Aug treasury.gov). Because the same basis is stripped and added back, it barely flows. |
| **F30** | "Delivery vintage" — titled 9 August, register to 3 September, price the 31 August close, today's close 11.62 | see S11 | ✔ | ✘ | **ACCEPT THE DEFECT, REJECT THE FIX.** The defect is real and is worse than stated (S10, S11). The receipt against the fix: **our library's 8-Sep session does not exist; the last session is 7 September at 11.38**, not 11.62. We re-strike on our own library, not on a figure we cannot source. Its "FV 16.59 on a 250-day roll" is therefore not adopted. |
| **F31** | The bridge stands on 31-Dec-2025 although a reviewed 30-Jun-2026 balance sheet exists and is read elsewhere | direction adverse; bounded at **up to −AED 0.41 (−2.5%)** on the term-deposit leg alone (FY2025 deposits 1,784.0mn ÷ 4,532.9mn shares × roll), exact figure not isolable | ✔ | ✔ | **ACCEPT, and raise its severity.** The critique files this as a partial fail with a benign note. It is a plain breach of the standing rule that the bridge stands on the **latest disclosed** sheet [R-BRIDGE-01]. That the number cannot be pinned down is itself the defect: the register holds the H1-2026 income statement and capex and **no** H1-2026 balance-sheet line. |

### Unverifiable — resolved here where we can

| # | What the critique could not confirm | Resolution |
|---|---|---|
| **U1** | The 16.70-year asset life and its 15.96 / 22.97 cross-readings | **Resolvable inside the repo.** The derivation is committed in `terminal_record`: PP&E 28,616,356 ÷ 1,542,393 = 18.55y; intangibles 3,500,287 ÷ 239,907 = 14.59y; right-of-use 3,726,888 ÷ 364,063 = 10.24y; blended 16.70y. It validates against note 7's directly disclosed 10.1-year average lease term, 1.4% apart. Sensitivity across 10.7–22.7 years is AED 1.50 (Table 11). No defect found. |
| **U2** | That **du**, not e&, published the royalty extension on 24-Jul-2026 | **Open, and it matters.** The substance is corroborated; the attribution is the precise fact §1.7 says the prior edition got backwards. Registered for primary re-verification against the DFM announcement list before any re-issue. |
| **U3** | The three beta regressions | **Resolved, and it produced S1.** The index files are in the repository. Re-run through `own_stock_beta()`: **0.5569**, not 0.488. The reason an outside auditor could not check this is itself a defect — `beta_result.json` carries a prose index name and no `index_file` path (S2), the shape [R-BETA-04] names as the weakest. |
| **U4** | MoF auction releases, Damodaran vintages, stc sukuk quotes | Open. Registered for live re-sourcing at re-issue. The internal arithmetic reproduces exactly and is same-basis coherent (our Section G recomputation). |
| **U5** | The cone's backtest statistics | Committed in `backtest_5y.json` / `study_numbers.strike`; the 18-window origins are in the repository. Superseded in practice by S12 — the cone has matured. |
| **U6** | Mobily's SAR 61.30 close and 4.89% trailing yield | Open on the close and the yield; the earnings route is corroborated two ways in our own register (TTM EPS 4.76 → 12.88×; market-cap route → 12.89×). |

---

## 3. COUNT RECONCILIATION

**31 findings raised (F1–F31), 31 answered, 0 unaddressed.**
**6 unverifiables raised (U1–U6), 6 answered, 0 unaddressed.**
**16 further findings raised by our own audit (S1–S16), 15 of which the critique did not make.**
**Total ledger: 53 rows.**

No two findings were merged. F5 and F6 share a root cause (S5) and are answered on separate
rows saying so.

---

## 4. BUCKETS

### Bucket 1 — ACCEPT AND IMPLEMENT (26)

F1, F2, F3, F4, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22,
F23, F24, F26, F27, F29, F31 — plus our own S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S12, S13,
S15, S16.

### Bucket 2 — ACCEPT THE DEFECT, REJECT THE FIX (3)

- **F5.** The grids do not return the headline. The fix is not to net a dividend: it is to point
  `dcf_at()`, `dcf_at_rf()` and `dcf_beta()` at the sanctioned terminal module, then rebuild
  Figure 3, Tables 10 and 11 and every discount-rate figure quoted in §1.7 and §1.8.
- **F6.** Two bases in one table, yes. Not "understated sixfold because of the dividend": the rf
  rows are already netted; the beta row is on the retired terminal. Restated like-for-like the
  rf question is worth **−0.77**, close to the critique's −0.80 by coincidence of construction.
- **F30.** Vintage is stale, yes. Not re-struck on AED 11.62 — that session is not in our
  library. Re-strike on **11.38, 7 September 2026**, the latest session we hold.

### Bucket 3 — UNPROVEN, RESEARCH REQUIRED (3)

- **U2** — du's own 24-Jul-2026 royalty disclosure, to be re-verified on the DFM announcement list.
- **U4** — MoF auction releases and the Damodaran UAE row, to be re-sourced live.
- **U6** — Mobily's close and trailing yield at the anchor.

None is parked: each is registered with what would close it.

### Bucket 4 — REJECT, with receipts (1)

- **F25.** The FADGI regressor for a DFM name is a standing, measured, labelled house exception,
  not a wrong-exchange error — `wacc_builder.INTERIM_INDEX`, adopted 10-Aug-2026, held open
  23-Aug-2026, on evidence that FADGI explains the DFM names better (median R² 0.240 vs 0.127)
  than the ADX names it covers. What a careful reader would have had to misread to land there is
  that the study **never quotes the disclosure that says so** — logged as S4, and the beta itself
  is wrong for an entirely different reason, logged as S1.

### Bucket 5 — YOUR DECISION (1)

**The regressor, now that the beta is being re-derived anyway.** Both branches priced on the
sanctioned routine and the sanctioned terminal:

| Branch | Beta | Fair value | Gap to 11.38 |
|---|---|---|---|
| Keep FADGI (the registered interim, per the standing instruction) | 0.5569 | **AED 15.53** | +36.5% |
| Register DFMGI, du's own listing venue (needs your instruction — [R-IDX-01] forbids registering it because the file exists) | to be re-derived on the 2,307-row registered series | ≈ AED 16.8 on the study's 0.4716; the real number needs the run | ≈ +48% |

**Recommendation: keep FADGI.** The house rule is explicit that a later session must not register
DFMGI on the reasoning that the file exists, and the honest reading is that this correction moves
the answer **toward** the price, which is the direction that shows the discipline is not fitting.

---

## 5. THE ESCALATED FINDING (over 5% of the central)

Only one finding in the whole exercise clears the 5% bar, and it is ours.

**S1 — the beta.** The study publishes 0.488 from `beta_reg.py`, a study-local regression that
CLAUDE.md and SIGCM clause 6 both forbid outright: *"NEVER hand-roll a study-local beta script —
every study in this repo once did and every one regressed on a composite."* Re-derived from the
primary sources through the only sanctioned route, `beta_regression.own_stock_beta('DU','AE','DFM')`,
against the registered `raw_indices/AE/FADGI.csv` as of 24-Jul-2026:

```
beta 0.5568988   r2 0.14116   se 0.14902   n 249   ci90 [0.3118, 0.8020]
dimson true   frequency weekly   week_rule W-FRI   window 4.81y
index_file raw_indices/AE/FADGI.csv   index_asof 2026-07-24   conforming false
```

The local script omits the Dimson lead-lag correction the house routine applies to thinly traded
names, samples its own weekly grid, reads a copy of the index from inside the study directory, and
produces 249 → 256 observations. The gap is 0.069 of beta on a name where the study itself says
each 0.10 of beta is worth AED 1.3 to 1.9.

Priced on the sanctioned terminal, holding every other driver at its published value:

| | Beta | Ke | WACC exp / term | Fair value | vs 11.38 |
|---|---|---|---|---|---|
| As published | 0.4880 | 6.5335% | 6.4009% / 6.1741% | **16.578** | +45.7% |
| Sanctioned routine | 0.5569 | 6.8291% | 6.6857% / 6.4549% | **15.532** | +36.5% |

**−AED 1.046 per share, −6.31% of the central.** It moves the answer toward the price.

---

## 6. THE HEADLINE, IF EVERYTHING ACCEPTED IS IMPLEMENTED

Indicative, not a re-issue — the levers interact and the rebuild ledger will walk them in order.

| Step | Fair value |
|---|---|
| Published | 16.578 |
| + sanctioned beta (S1) | 15.532 |
| + lease treatments built as declared (F7) | ≈ 15.45 |
| + the bridge on the 30-Jun-2026 sheet (F31) | not isolable until that sheet is registered |

Against the latest known close of AED 11.38 the gap moves from **+45.7% to roughly +36%**. It
stays well outside the 10% band, so the eight-heading gap review must be rewritten before
anything is staged. The publication block does not fire — it is one-sided and this central sits
**above** the price — so no authorisation is owed and none is being asked for.

---

## 7. WHAT THIS CRITIQUE GOT RIGHT, AND WHERE IT WAS WRONG

It is a serious piece of work. It reproduced the whole chain independently, it footed every
printed table, it caught eight real total failures and twenty-three real partials, and its
central observation — *"a correct number reached by a construction nobody wrote down"* — is the
right description of this study's weakness. 30 of its 31 findings are accepted in substance.

It was wrong twice, and both times for the same reason: **it inferred a cause from a coincidence
of size.** The AED 0.664 wedge in the grids looks like the AED 0.66 dividend and is not; it is
the retired terminal. And the beta question it raised is real while the reason it gave is not —
the regressor is a documented house exception, and the actual defect is that we hand-rolled the
regression and lost 0.069 of beta doing it.

It also could not see what it could not reach. The largest finding here — worth six times the net move it reports on the central — required
running our own code against our own committed index file.

---

*Prepared under `engine/Critique_Response_Prompt.md` v2. Nothing implemented. Awaiting approval
to proceed to step 9.*
