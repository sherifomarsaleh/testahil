# Forensic Valuation Audit — Air Arabia PJSC study & model dated 09-Aug-2026

Auditor: independent line-by-line verification of `AIRARABIA_Valuation_Study_09082026_public.pdf` (17 pp.) and `AIRARABIA_Valuation_Model_09082026_public.xlsx` (16 sheets). Audit date: 9 August 2026.

---

## Section A — Audit Scope Statement

Audited: the 17-page valuation study PDF and the 16-sheet companion Excel model (every formula extracted and independently recomputed in full; the workbook stores no cached values, so all outputs were rebuilt from the Assumptions sheet alone). Primary sources reached: Air Arabia's audited FY2025 consolidated financial statements (KPMG, 13-Feb-2026) and Q1-2026 reviewed interim from airarabia.com, company press releases and results presentations, UAE MoF T-bond auction results, CBUAE rate announcements, Damodaran's January-2026 country-premium and industry datasets, EIA STEO (July-2026), IATA June-2026 outlook, and market-data aggregators for the 7-Aug-2026 close and peer multiples. Not checkable: the study's own OHLC price library (not supplied), so the beta regression, technical indicators, and Monte Carlo/backtest outputs could be tested for internal coherence only; the companion bibliography document (referenced, not supplied); FY2022–FY2023 filings (only the FY2025 filing's restated 1-Jan-2024 comparatives were verified); and the fragmented note-12 100%-basis JV tables.

## Section B — Fail Table

No TOTAL FAILs were found. Ten PARTIAL FAILs and seven UNVERIFIABLE items follow.

| # | Location | Item | Plane | Severity | What the report says | What is actually correct | Why it failed | Impact on fair value | Correct method |
|---|----------|------|-------|----------|---------------------|--------------------------|---------------|---------------------|----------------|
| 1 | PDF p.1, Headline | Gap vs market prose | Logic | PARTIAL | "The market is paying roughly a fifth more than the base fundamental value" | Spot 5.24 is **+35.7%** above the base central 3.86 (equivalently base is −26% vs spot). "A fifth more" is true only vs the JV-capitalised DCF (5.24/4.39 = +19.4%) — a different object | Prose understates the gap on the stated basis; conclusion-drift (here in the *less* dramatic direction) | None on numbers; headline framing only | State "roughly a third more than the base central" or attach "a fifth" to the JV-capitalised framing explicitly |
| 2 | PDF p.2, Company overview | FY2025 revenue mix | Input/Logic | PARTIAL | "79% … passenger fares plus baggage, another 11% … ancillary/cargo/services, 3% aircraft leases and 1% hotels" (sums to 94%) | From the filing and the model's own lines: fare+baggage **80.3%**, ancillary alone **10.9%**, cargo+services **5.3%**, leases **2.8%**, hotels **0.8%** (sums to 100) | The 11% bucket covers only ancillary; cargo+services (5.3%) are dropped and fares rounded down | None (descriptive) | Recompute the mix from the disclosed revenue lines already in the model |
| 3 | PDF p.9 §3 vs workbook Monte Carlo A17 | Backtest coverage statistics | Logic | PARTIAL | PDF: realised inside 80% band **79%**, inside 90% band **86%** | Workbook note for the same claim: **83%** and **89%**. The two deliverables disagree; without the engine run I cannot say which is right | Same-fact mismatch across the two published documents | None on fair value; weakens the calibration-evidence trail | One figure, one source of truth, stamped in both documents |
| 4 | PDF p.6 §1.9 / Sensitivity sheet | "Each cell is a complete revaluation" | Logic | PARTIAL | Beta row: 4.56 / 4.21 / 3.83 / 3.55 / 3.25 | A complete revaluation gives **4.52 / 4.20 / 3.83 / 3.57 / 3.28**. The published cells reproduce **exactly** (to 4 d.p.) only when the anchor-roll accretion factor is held at the base cost of equity while beta moves everything else. Terminal-growth grid cells likewise differ ≤0.2% under every construction tested (e.g. 8.67%/1.5% cell: published 3.6115, full revaluation 3.6085) | The claimed convention ("complete revaluation") is not the convention used; the anchor roll is itself a function of Ke | ±0.01–0.03 on off-base sensitivity cells only; base column exact | Roll at the perturbed Ke, or state the roll is held fixed |
| 5 | Workbook 'Relative & Normalized'!C16 vs 'Per-Share & Ratios'!C15 / PDF §1.3 | Trailing EV/EBITDA basis | Judgment | PARTIAL | Published trailing EV/EBITDA **10.6×** (EBITDA incl. fees/other income); justified 7.5× applied to FY2027E EBITDA **incl. fees** (2,287) | The workbook itself also computes the same-labelled ratio excl. other income: **11.65×** — unpublished. Peer and Damodaran sector multiples (7.58×) are struck on reported EBITDA, which for the comparators does not include an "other income" line; on the matching basis the relative lens is **3.52**, not 3.85 | Numerator/denominator basis differs between subject and comparators; the study's own dual-framing rule (state both framings) is not applied to this one | Relative lens −0.33; weighted central −0.066 (−1.7%) on the stricter basis — below the ±3% materiality line but the single largest untaken haircut | Publish both bases, or apply the sector multiple to like-for-like EBITDA |
| 6 | DCF sheet rows 39/46, Cash Flow rows 12–16, SOTP bridge | Future leased-fleet cost | Judgment/Logic | PARTIAL | Fleet roll adds AED 300mn/yr of leased aircraft (net of their depreciation); caveat says only that the owned/leased **split** is assumed | The 300/yr raises invested capital (cutting terminal ROIC → TV), yet **no lease liability, lease interest, or lease payment for post-2025 leases appears anywhere**: FCFF subtracts owned capex only, the financing walk holds gross debt flat at 2,781, and the bridge nets only 31-Dec-2025 lease liabilities. Leased capacity is cash-free inside the window while its traffic is fully in revenue. The two internally-consistent treatments bound the DCF at ≈ **3.56** (charge the leased additions as capex-equivalent: −PV 1,174mn ≈ −0.27/sh) and ≈ **3.92** (leases as NPV-0 financing, leased assets excluded from IC: +0.09/sh) vs the published 3.83 | Hybrid treatment sits between two consistent framings, and unlike fuel and the JV network this contested construction is **not** dual-framed | ∓0.09–0.27 on the DCF lens (∓1–3% of the weighted central); published value inside the consistent band, direction of the study's conclusion unchanged either way | Apply the dual-framing rule: price both lease treatments, or subtract new-lease ROU additions as capex-equivalent |
| 7 | Workbook 'Cash Flow'!B14:F14 | Finance-cost formula | Logic | PARTIAL | Label: "Finance costs (booked rate × gross debt)" | Formula is `kd_path × gross debt × 0.8` — an undisclosed ×0.8 constant hardcoded mid-chain, on no assumptions row and in no document (audited effective rate 2.73% vs 5.4%×0.8 = 4.3% modelled) | Unexplained hardcoded adjustment inside a formula chain that the READ FIRST sheet claims is fully driver-driven | ~AED 24mn/yr pre-tax on the IS/EPS path; nil on the DCF (FCFF is pre-financing); immaterial | Put the 0.8 (or an effective-rate driver) on the Assumptions sheet with its rationale |
| 8 | Workbook Cash Flow row 15 / PDF A.3 & catalysts | FY2026E dividend vs the ladder | Judgment | PARTIAL | Catalysts: a fifth consecutive raise "would signal…"; risk register lists "the dividend ladder breaking" as a bear marker | The model's own FY2026E dividend is 100% payout of the dip-year profit = AED 1,226mn = **0.263/sh — a cut from 0.30**, i.e. the ladder breaks inside the base case, unremarked | Narrative treats the ladder as intact/raisable while the base case quietly breaks it | Nil (no dividend-discount lens) | Either floor the DPS at 0.30 (payout >100% is affordable given net cash) or state that the base case assumes a cut |
| 9 | PDF p.6 §1.8 & p.10 | Macro context lines | Input | PARTIAL | UAE GDP "~5% projected for 2026"; inflation "~2%"; "seven airspaces closed" in H1-2026 | CBUAE's maintained 2026 projection is **5.6%** (Apr-2026); 2025 inflation printed **1.3%** (1.8–2.0% is the 2026–27 projection); at least **eight** states closed airspace 28-Feb–1-Mar-2026 (Iran, Israel, Iraq, Jordan, Qatar, Bahrain, Kuwait, UAE, plus partial Syria) | Context figures slightly stale/miscounted vs the primary sources the study's own class of sourcing requires | None (context only; none of the three feeds a calculation) | Cite CBUAE's current projection and the realised CPI with dates; count the closures from the NOTAM record |
| 10 | PDF Appendix A.1 | Statement table does not foot | Logic | PARTIAL | Historical columns print Revenue, "Direct operating costs", EBITDA, D&A, Operating profit | The historical direct-cost line is the audited face figure **including direct depreciation** (FY2025: 6,088,132) while D&A is also deducted separately and the admin/S&M rows are omitted: 7,788 − 6,088 − 622 = 1,078 ≠ 1,270 operating profit shown; every historical column double-counts direct depreciation if footed as printed | The footnote flags the basis switch but the printed rows cannot be reconciled to the printed subtotals | None (all underlying figures verified correct individually) | Print the cash-basis direct costs (already in the model IS) plus admin/S&M rows, or drop the D&A row from the historical columns |
| 11 | PDF §1.8 / Assumptions C34 | Beta 1.086 (5-yr weekly vs DFM) | Input | UNVERIFIABLE | β 1.086, R² 0.40, 258 weeks, SE 0.083, 90% CI 0.95–1.22 | Internal statistics are mutually consistent (t = 1.086/0.083 = 13.1 → implied R² = 0.401 ✓; 1.086 ± 1.645×0.083 = 0.95–1.22 ✓; 5yr ≈ 258 wks ✓). But the price series was not supplied, and public aggregators print 0.29–0.32 (benchmark unstated) — neither confirming nor refuting a DFM-index weekly regression | Searched: Yahoo/stockanalysis/Investing/GuruFocus; no published DFM-benchmark beta exists | Valuation-critical if wrong: β 0.85 alone moves the DCF to ≈4.52 (still below spot) | Resolvable with the weekly return series vs the DFM General Index |
| 12 | PDF §2 | Technical read & 52-wk range | Input | UNVERIFIABLE | SMA20/50/200 = 5.09/5.20/4.82; RSI 54; ATR 0.15; MACD −0.02/−0.06/+0.04; 52-wk 3.63–6.03; S1/S2/S3 = 3.80/3.68/3.60 | No OHLC series supplied. Internal coherence passes (price above all MAs as claimed; MACD histogram = line − signal ✓; −13%/+44% to the extremes ✓ against the stated range). Aggregators show the 52-wk low at 3.68 (close/intraday basis unknown) vs 3.63 stated; the nearest support 3.80 sits 27% below spot with no level in between — odd for a fractal-pivot ladder on a stock that ranged 3.63–6.03 | Searched aggregator quote pages; indicator values cannot be recomputed without the series | None on fundamental value | Resolvable with the price library the study was built on |
| 13 | PDF §3 / Monte Carlo sheet | Simulation bands, probabilities, backtest | Logic | UNVERIFIABLE | 50k paths; 1M/3M bands; 58 backtest windows; +0.7% skill vs RW | Engine outputs cannot be re-simulated without the fitted profile and series. All internal-coherence tests pass: percentiles monotonic; median ≈ spot with dividend-drag drift (P(above spot) 49%); touch ≥ terminal probabilities (24.2/21.2 ≥ 14.4/12.9; 48.6/46.2 ≥ 25.9/25.5); zone probabilities equal the band definitions; check dates 2026-09-07 and 2026-11-09 are correct calendar-month rolls of the 7-Aug anchor; horizon labelling never conflates the 3-month map with the 12-month fair-value objects | See row 3 for the one demonstrated coverage-figure inconsistency | — | Resolvable with the engine's committed fit and library |
| 14 | Summary/Fundamental Valuation pasted cells | Scenario bounds (bear 0.81 / bull 7.53) and Expert 2 bear leg | Logic | UNVERIFIABLE | "high fuel + weaker traffic + tighter money" / "fuel relief + stronger traffic + JV capitalised"; E2 range "tighter rate + full cash / wider rate, no cash" | Parameter combinations are not disclosed precisely enough to reproduce (unlike the high-fuel DCF 2.1666 and E2 bull leg 4.3726, which I reproduced exactly). Not demonstrably wrong; not reproducible | Whole-model re-runs with undisclosed settings | Bounds only; centrals all reproduce | List the perturbed values per scenario in the workbook |
| 15 | PDF §1.7 | "Ventures' 100%-basis profits grew roughly 65% in FY2025" | Input | UNVERIFIABLE | ~65% growth on 100% basis | The group's **share** grew 52% (124.752→189.975, verified in the filing). The 100%-basis venture-by-venture columns in note 12 could not be reassembled from the PDF text layer; with Egypt's stake raised 40%→49% mid-2025 the share should if anything outgrow the 100% basis, so the 65% claim needs the note table to stand | Note-12 table extraction fragmented | None (colour only; the bridge uses the audited 190.0 share and 363.4 carrying value, both verified) | Resolvable by reading note 12's printed columns |
| 16 | PDF p.9 catalysts | "Every quarter the curve view wins is roughly AED 0.04 per share of annualised value" | Logic | UNVERIFIABLE | AED 0.04/quarter | No construction stated; not derivable from the published fuel framings (gap 3.83 − 2.17 = 1.66/share for the full path divergence) | Narrative-only arithmetic | None | State the construction or drop the figure |
| 17 | Bibliography references throughout | Companion bibliography document | — | UNVERIFIABLE | "A companion bibliography document lists every input with source and date"; FY2022–24 machine-read figures cross-checked; FY2024 footing inconsistency "recorded in the bibliography" | Document not supplied to this audit. (The FY2024 footing inconsistency itself I **confirmed in the filing**: the FY2024 revenue disaggregation column sums to 6,765,852 — total revenue including lease rental — against contract revenue of 6,616,409 shown in the same note, exactly as the study's caveat describes.) FY2023-and-earlier filing line items were not independently pulled; the FY2023 equity 7,534,006 does match the FY2025 filing's restated 1-Jan-2024 note | Attachment absent | — | Supply the bibliography and FY2022–23 filings |

## Section C — Arithmetic Reconciliation Appendix

Every value below was recomputed from the Assumptions sheet inputs alone before comparison. "Δ" is mine − report at the report's printed precision.

**Cost of capital**

| Line | Mine | Report | Δ |
|---|---|---|---|
| Net rf = 4.48% − 0.42% | 4.060% | 4.06% | 0 |
| Ke = 4.06% + 1.086 × 4.87% | 9.349% | 9.35% | 0 |
| Market cap = 5.24 × 4,666.7 | 24,453.5 | 24,453.5 | 0 |
| Debt weight = 2,781.4 / 27,235.0 | 10.21% | 10.2% | 0 |
| WACC explicit = 0.8979×9.349% + 0.1021×(5.5%×0.85) | 8.871% | 8.87% | 0 |
| Terminal Ke = 4.0% + 1.086 × 4.75% | 9.159% | 9.16% | 0 |
| WACC terminal = 0.9×9.159% + 0.1×(5.0%×0.85) | 8.668% | 8.67% | 0 |

**DCF waterfall (AED mn; FY26E–FY30E)**

| Line | Mine | Report | Δ |
|---|---|---|---|
| Revenue | 7,868.8 / 8,450.9 / 9,257.2 / 10,094.7 / 10,951.9 | 7,869 / 8,451 / 9,257 / 10,095 / 10,952 | 0 (rounding) |
| EBITDA incl. fees | 1,876.3 / 2,286.6 / 2,419.5 / 2,555.8 / 2,679.8 | 1,876 / 2,287 / 2,420 / 2,556 / 2,680 | 0 |
| EBIT | 1,156.3 / 1,476.6 / 1,519.5 / 1,575.8 / 1,619.8 | 1,156 / 1,477 / 1,520 / 1,576 / 1,620 | 0 |
| NOPAT (×0.85) | 982.9 / 1,255.1 / 1,291.6 / 1,339.5 / 1,376.8 | 983 / 1,255 / 1,292 / 1,339 / 1,377 | 0 |
| ΔWC | +150.8 / −372.6 / −516.0 / −536.0 / −548.6 | 151 / −373 / −516 / −536 / −549 | 0 |
| FCFF | −447.9 / 537.7 / 807.6 / 905.5 / 985.5 | −448 / 538 / 808 / 905 / 985 | 0 |
| Discount factors (glide 8.87%→8.67% on the Kd path) | 0.9185 / 0.8445 / 0.7767 / 0.7148 / 0.6578 | same | 0 |
| PV of FCFF | −411.4 / 454.0 / 627.3 / 647.2 / 648.2 | −411 / 454 / 627 / 647 / 648 | 0 |

**Terminal block and bridge**

| Line | Mine | Report | Δ |
|---|---|---|---|
| PV explicit years | 1,965.3 | 1,965 | 0 |
| Terminal NOPAT ×(1−g/ROIC), ROIC 14.39%, reinvestment 17.37% | rr 17.37% | 17.4% | 0 |
| PV terminal value | 12,436.8 | 12,437 | 0 |
| Enterprise value | 14,402.2 | 14,402 | 0 |
| TV share of EV | 86.35% | 86% | 0 |
| + Net cash (5,198.7 − 2,781.4) | 2,417.3 | 2,417 | 0 |
| + Non-operating (457.5 + 277.1 + 334.7) | 1,069.3 | 1,069 | 0 |
| + JV at carrying value | 363.4 | 363 | 0 |
| − Minorities (×0.00015963) | 2.91 | 2.9 | 0 |
| Equity attributable 31-Dec-2025 | 18,249.2 | 18,249 | 0 |
| Per share × 1.09349^(219/365) − 0.30 | **3.826** | 3.83 | 0 |
| JV capitalised (15 × 189.975 in the bridge) | **4.388** | 4.39 | 0 |
| High-fuel path whole-model re-run | **2.1666** | 2.1666 | 0 (exact) |

**Lenses and weighting**

| Line | Mine | Report | Δ |
|---|---|---|---|
| Relative: 7.5 × 2,286.6 × DF₂ + PV(FCFF₁₋₂) → bridge → anchor | 3.854 (bear 3.199 / bull 4.508) | 3.85 / 3.20 / 4.51 | 0 |
| Normalised: 23.45% margin on FY26E revenue, EPS 0.2960 × 13 | 3.760 (2.823 / 4.697) | 3.76 / 2.82 / 4.70 | 0 |
| Book: P/B (18−2.5)/(9.159−2.5) = 2.328 × 1.802 | 4.126 (3.623 / 4.697) | 4.13 / 3.62 / 4.70 | 0 |
| Weighted central 0.45/0.20/0.20/0.15 | **3.863** | 3.86 | 0 |
| Weighted, JV-capitalised framing | 4.116 | 4.12 | 0 |
| All eight "vs spot" percentages | −27.0 / −26.5 / −28.3 / −21.3 / −26.3 / −16.3 / −21.5 / −58.7 | −27 / −26 / −28 / −21 / −26 / −16 / −21 / −59 | 0 |

**Expert panel**

| Line | Mine | Report | Δ |
|---|---|---|---|
| E1: (1,519.5 − 6.5 + 269.8) × 0.85 × (1−min)/4,666.7 = EPS 0.3248; ×13, rolled | 4.1533 (3.1256 / 5.1810) | 4.1533 / 3.13 / 5.18 | 0 (exact) |
| E2: avg FCFF₂₈₋₃₀ 899.6 − 7.1 + 105.3 = 997.9; ×1.025 / (9.159%−2.5%) + ½ net cash, −min, rolled | 3.4458 | 3.4458 | 0 (exact once the grow-then-capitalise convention is identified; bull leg 4.3726 reproduces at g = 3.5% with full cash; bear leg not reproducible — row 14) |
| E3: IC₀ 4,846.5 + PV excess 2,394.0 + PV terminal excess 5,761.4 (spread vs IC₃₁) = EV 13,001.9 → bridge | 3.5094 (bull 4.0714) | 3.51 / 4.07 | 0 (exact) |
| Panel median | 3.509 (−33.0% vs spot) | 3.51 / −33% | 0 |
| E3 ROIC path | 14.9 / 16.5 / 15.4 / 14.7 / 14.0% | 15 / 17 / 15 / 15 / 14% | 0 |

**Statements, walk and ratios (selected)** — financing walk net debt −854 / −110 / +360 / +802 / +1,224 vs A.2's −854 / 360 / 1,224 ✓; equity roll 8,409 / 8,556 / 8,783 / 9,022 / 9,272 vs A.2 ✓; fleet roll 10,251 / 11,641 / 12,941 / 14,211 / 15,451 ✓; EPS history 0.3315 / 0.3144 / 0.3490 vs 0.33 / 0.31 / 0.35 ✓; trailing P/E 15.02 ✓; EV/EBITDA (fee-incl.) 10.55 ✓ (see row 5); dividend yield 5.73% ✓; trailing ROE on average equity 19.91% ✓; FY24/FY25 effective tax 8.79% / 11.60% both match the filing's own disclosed reconciliation (11.60% = 212,444 tax expense before the −10,390 prior-period credit ÷ 1,830,789) ✓; per-passenger history table (fare 495/479, fuel 172/172, staff 79/82, etc.) all reproduce from the filing's disclosed cost lines ÷ disclosed passengers ✓.

**Input verification against primary sources (all confirmed exactly unless noted):** FY2025 revenue 7,787,581k / PBT 1,830,789k / attributable 1,628,475k / minorities 260k; every revenue and direct-cost line of the disaggregation (fare+baggage 6,251,713 = passenger 6,165,584 + baggage 86,129); D&A 621,798; other income 197,132; finance income/costs 240,774/66,672; JV share 189,975 and carrying value 363,386; net cash 2,417,297 (= 1,072,692 + 4,126,040 − 1,515,068 − 1,266,367); intangibles 1,362,497; FVOCI 457,528; investment property 277,090 with disclosed fair value AED 334mn; net investment in lease 334,666 (subleases to Maroc/Fly Jinnah/Abu Dhabi confirmed); equity 8,408,904; op. cash flow 2,860,401; capex 2,327,603 = 1,387,154 + 940,449 (audited CF lines); dividends paid 1,167,376; shares 4,666,700k; FY2024 restated comparatives; dividend ladder 8.5→15→20→25→30 fils (fourth consecutive raise ✓, AGM 12-Mar-2026 ✓); auditors and report dates ✓; incorporation 19-Jun-2007 ✓; fleet 90 + 2019 order 73/27/20 with first neo 29-Sep-2025 ✓; JV stakes 49/49 (from 40)/45/44.13/49% incl. Air Arabia DMM ✓; Q1-2026 revenue +1%, net −22%, consolidated pax −11% ✓; DMTT 15% from 2025 ✓; UAE T-bond Jul-2026 4.48% (May 4.30%) ✓; Damodaran 5-Jan-2026 UAE ERP 4.87% = 4.23 + 0.64, Aa2 spread 0.42% ✓; sector P/E 12.87× / EV-EBITDA 7.58× ✓; CBUAE 3.65% held 29-Jul-2026 ✓; EIA Brent $82 (2026) → $65 (2027) ✓; IATA $95 Brent / $152 jet ✓; spot 5.24 on 7-Aug-2026, market cap ≈24.45bn ✓; all six peer multiple sets within tolerance, Jazeera 17.7× reproducing under its stated construction ✓.

## Section D — Verdict Summary

**Counts.** Total fails: **0**. Partial fails: **10** (rows 1–10). Unverifiable: **7** (rows 11–17). Passes: Pass 1 (inputs) ≈50 items confirmed against the audited filing and official sources; Pass 2 (market data) 14 confirmed; Pass 3 (calculations) ≈70 recomputed lines matched at printed precision, including three whole-model re-runs reproduced exactly; Pass 4 (technicals) internal-coherence only (4/4 checks pass, series unavailable); Pass 5 (judgments) all material assumptions anchored and sensitised, terminal growth below nominal GDP, no Ke/haircut double-count found, both contested judgements genuinely dual-framed; Pass 6 (consistency) every repeated number identical across headline/tables/model except rows 1–4; Pass 7 (completeness) newest filing and Q1-2026 used, Egypt stake change captured, no missed corporate action found.

**Three most valuation-critical findings.** (1) Row 6 — the leased-fleet hybrid: the only construction where the model is internally inconsistent rather than merely debatable; consistent treatments bound the DCF at ≈3.56–3.92 vs 3.83. (2) Row 11 — beta 1.086 is internally coherent but externally unverifiable, and it is the input with the most leverage toward closing the gap to market (β 0.85 → DCF ≈4.52, still below spot). (3) Row 5 — the fee-inclusive EBITDA basis flatters both the trailing multiple shown and the relative lens by ~0.33/share against comparators struck on reported EBITDA.

**Headline verdict.** The fair-value range **survives**: every published central reproduces from stated, primary-verified inputs; the corrections in this audit move the weighted central within roughly 3.66–3.93 against a published 3.86, and every demonstrated bias except the beta uncertainty points the same way as the study's conclusion, not against it.
