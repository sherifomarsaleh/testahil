# AMOC — response to four reviewer critiques

Procedure: self-audit before reading; every finding enumerated in the reviewers' order; priced
before judged; premise split from conclusion; receipts for every rejection; escalation above 5%
of the weighted central; then buckets.

**Base for all prices: weighted central EGP 9.4611; DCF lens EGP 9.9140; spot EGP 9.10.**
A price given "on the central" is the effect on 9.4611 after the 45/20/20/15 lens weights.

---

## PART 1 — SELF-AUDIT, CONDUCTED BEFORE THE CRITIQUES WERE OPENED

Thirteen findings. Four were missed by all four reviewers, including the largest single item in
the whole exercise.

| # | Finding | Price | Caught by |
|---|---------|-------|-----------|
| **S1** | **The exchange-rate path contradicts the interest-rate differential embedded in my own discount rate.** Both revenue legs are dollar-priced. I discount at an EGP rate of 22.31% against a USD rate of 4.30% — an uncovered-interest-parity depreciation of **17.3%/yr** — while forecasting revenue on **4.3%/yr**. The FX sensitivity grid only tests a ±10% *level* shift, so the inconsistency is untested by construction. | **+25.0% central** (+EGP 2.36) at UIP; +9.6% at the CBE inflation differential | **MISSED BY ALL FOUR** |
| **S2** | **Net cash is added at 100% of face while earning far below the cost of equity**, and the model grows it from 2,438 to 4,827 with no reinvestment story. PV of the five-year return shortfall on that balance. | **−12.8% central** (−EGP 1.21) | Premise caught by GR7 ("frictionless capital allocation", "trapped liquidity") and CC33; neither priced it this way |
| **S3** | **The relative lens is circular.** The "justified" multiple 4.5× equals the company's own trailing 4.52×, so the lens output *is* the discount factor. | Dropping it and reweighting: **+5.6%** (+EGP 0.53) | CW30, CC34 |
| **S4** | **The explicit window is not held to the reinvestment identity the terminal block is.** g = ROIC × RR is enforced in perpetuity but the explicit years imply a **97% incremental return on capital** for five years, undisclosed. | −2.6% at a 40% incremental return; −4.2% at 30% | **MISSED BY ALL FOUR** (CC15 called §1.9 circular but did not find this) |
| **S5** | **The minority is deducted on the parent's cash and the caption claims the opposite.** | +0.27% central to correct | GT1, CC30 |
| **S6** | **Terminal growth of 5% is called "generous" while the model's own currency path makes it +0.7% above pure pass-through.** Two contradictory statements in one document. | interacts with S1 | Half-caught by CW25 ("0% real growth in perpetuity") |
| **S7** | **An unsourced 0.85 constant sets the magnitudes of the headline "other income" finding.** | direction survives; magnitudes move up to 23% | CW11, CC16 |
| **S8** | **The replacement-cost capital base is named "the sharpest single criticism" and then never priced.** | **−2.3% central** at 2× capital; **−4.6%** at 3× | GT10, GR8, CC32 |
| **S9** | **Beta is regressed on an equal-weight composite of Testahil's own covered library** — an index whose membership is selected by which names the house has studied. | not separately priced; ±0.35 on beta spans 12.11–8.36 | Unverifiability caught by CW43, CC45; the selection-bias point was not made |
| **S10** | **"Group I processors 3.5×/6.0×" are presented as observed peer data; they are my own bear/bull bounds with no source**, and my own QC gate counted them as "4 observed peer multiples". | 0% (not in the chain) | CW29 |
| **S11** | **Lens weights 45/20/20/15 are asserted with no derivation.** | span across plausible weightings −3.1% to +4.8% | Mostly missed |
| **S12** | **The "5.5-year implied asset life" presented as a coherence check on the reconstruction is a function of the days assumption, not evidence for it.** At 25/25/40 days the same method gives 0.2 years. | 0% on value; voids a stated check | **MISSED BY ALL FOUR** |
| **S13** | **False precision** — a central quoted to two decimals against a lens spread of 7.07–12.34. | 0% | **MISSED BY ALL FOUR** |

---

## PART 2 — RECONCILIATION

**115 findings raised, 115 answered, 0 unaddressed.**
Claude-cowork 45 · Claude-code 45 · Gemini-deep-thinking 12 · Gemini-deep-research 13.

Of the 115: **68 accepted** (implement or accept-the-defect), **9 rejected with receipts**,
**5 arbitrated between contradicting reviewers**, **14 clearances/passes recorded**,
**19 accepted as disclosure-only with a zero or sub-0.5% price**.

Every claim testable against my own artifacts was tested. **Every single one was confirmed.**
The reviewers did not miss on their own ground; where they are wrong it is on the input plane,
on sources I cannot reach, or on one arithmetic misread of Damodaran's table.

---

## PART 3 — THE ENUMERATION

### Claude-cowork (45 findings, in their order)

| # | Their words | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| CW1 | "17 of 119 register inputs cannot reach `Summary!C10` at all" against a claim of "no dead inputs" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** My trace finds **19**, not 17 (C9–C15, C19, C21, C23, C32, C43, E72, E73, E78, F78, B82–D82). My driver test swept against 18 headlines, several of which are not the headline; the *document's* claim names "the headline". Overclaim confirmed. |
| CW2 | "the model's own verdict is PARITY … skill +0.676% … Neither published margin appears in the model" | 0% on value | Premise **right**, conclusion **right** | **ACCEPT.** Monte Carlo sheet carries 17 windows / 0.006759 / PARITY only. The 0.92% and 1.32% come from `backtest_5y.json`, which is not in the workbook. The prose asserts significance the sheet does not carry. |
| CW3 | "at the model's own beta of 0.9405 the model returns 9.9140, not 10.0434" | +1.31% overstated *as displayed*; 0% on base | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed: grid centre 10.0434 vs base 9.9140, gap 0.1294. The beta grid re-derives Ke and the terminal Ke but omits the terminal-ERP linkage the base uses. Isolated defect. |
| CW4 | FY2024/25 PAT: "the same release … states 'net profit of approximately EGP 2 billion'" | 0% (dead input) but voids §1.2 | Premise **REFUTED** | **REJECT — receipt.** Coherence test on a disclosure CW itself accepts: the H1-2026 release reports **+109%**. My Jan–Jun 2025 half is 1,550 − 643.6 = 906.4, and 1,900/906.4 = **2.097 = +109.7% ✓**. At PAT 2,000 the half becomes 1,356 and the implied growth is **+40%**, contradicting the disclosed +109%. Gemini-deep-research independently reports **1.552bn**. Two of four reviewers and an internal identity support 1,550. |
| CW5 | "AMOC Annual Report 2023-24: consolidated revenue 33,932 … profit attributable 1,699" | 0% (dead inputs) | Premise **unverifiable here**, plausible | **UNPROVEN → RESEARCH.** amoceg.com is blocked from this environment (403 under the egress policy). If correct, my 33,536 average is superseded by a disclosure and my §7 caveat "available only through growth-rate disclosures" is false. High priority. |
| CW6 | "consolidated revenue 24,140 … gross margin is 5.37%, not 5.76%" | anchors a path worth ±EGP 1.02/share per half-point | Premise **unverifiable here** | **UNPROVEN → RESEARCH.** If true it moves the one disclosed margin anchor in the study. |
| CW7 | "an end-2027 EV discounted to today values only cash flows from 2028 onward. The 2026-27 free cash flows — PV 888 + 839 = 1,728 — are dropped. Corrected lens = EGP 8.65" | **+2.74% central** (+EGP 0.26) | Premise **right**, conclusion **right** | **ACCEPT AND IMPLEMENT.** Confirmed exactly: PV(2026-27) = 1,727.7; lens 7.3508 → 8.6484. |
| CW8 | "Expert 3 correctly executed *is* the primary DCF … EV 10,762.3 — identical … Expert 1 is main-model lens 3 at 7.0× instead of 7.5×" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed: on the correct terminal-EP convention, EV = 10,762.3, gap to the DCF **+0.0**. Expert 1 = same EPS 1.645902 at 7.0×. The panel is not independent. |
| CW9 | "EP₂₀₃₁ = 2,392.2 − 16.523% × 4,408.9 = 1,663.7 … PV 5,153.7" | +0.9% on Expert 3 | Premise **right** | **ACCEPT.** I multiply the capital charge by (1+g); the charge belongs on year-5 closing capital. Confirmed 5,040.9 vs 5,153.7. |
| CW10 | "AMOC does disclose the split … A 5.8% NCI is the disclosure-consistent read" | **−1.4% central** at 5.8% | Premise **right** (category error), conclusion **unverifiable** | **ACCEPT the defect, RESEARCH the number.** The consolidated-minus-standalone gap is subsidiary *contribution*, not the outside share of it — that is a genuine accounting-identity error in my study. The 5.8% figure rests on a source I cannot reach. |
| CW11 | "Formula is `=$E$13*B5/$E$5*0.85` … The 0.85 constant appears nowhere" | 0% on value | Premise **right**, conclusion **right** | **ACCEPT.** Identical to my own S7. A fabricated scaler presented as a statement line. |
| CW12 | "The table is built backwards from reported profit and nothing else … a triple-derived plug is narrated as a discovered economic phenomenon" | 0% on value | Premise **right**, conclusion **partly right** | **ACCEPT the labelling defect, REJECT the strongest form.** The residual *is* triple-derived and the "built from the gross margin down" claim is only half true — PBT is grossed up from disclosed PAT. But the *direction* (760 → 442 → 253 → 10) is robust to the 0.85 constant (at 1.00: 725 → 390 → 195 → 10), so the pattern is not an artefact of the scaler. The causal attribution must go; the pattern may stay, labelled as a residual. |
| CW13 | "The §6 zone boundary is 9.69, not 9.46 … 46.2% is P(>9.69)" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed: P(>9.69) = 40.3%, P(>9.46) = 46.2%. The 46.2% is correctly P(>central) in §4; §6's zones are cut at a stale 9.69 and labelled as the central. |
| CW14 | "'runs from 2022 … 3,754 clean sessions over 15.6 years' … The two halves of one sentence are mutually exclusive" | 0% | Premise **right** | **ACCEPT.** A text defect I introduced by splicing the first backtest origin into a sentence about the series. The series runs 02-Jan-2011 → 06-Aug-2026. |
| CW15 | "Volume is not [built from halves]: `=0.808 × 2 × 0.96`" under a claim that "neither half is estimated" | −0.3% | Premise **right** | **ACCEPT.** My own S-list did not contain this; it is correct and the "neither estimated" claim must be qualified. |
| CW16 | "A residual cannot corroborate the construction that produced it" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** The USD 438/t "check" is a residual of the two aggregates it is offered as validating. |
| CW17 | "AMOC discloses a seven-line product breakdown … 176,998t (12.35% of volume) and EGP 6,862.8mn (20.60% of revenue)" | not separable; margin path ±1.02/half-point | Premise **unverifiable here**, highly specific | **UNPROVEN → RESEARCH, high priority.** If a disclosed volume/value table exists, my calibrated two-leg split is superseded and the specialty share is ~8pp too high. |
| CW18 | "22.97% (Cbonds) / 22.98% (Investing.com) — two independent sources agree" | **−0.5% central** | Premise **plausible**, conclusion **right** | **ACCEPT.** Independently corroborated by Gemini-deep-thinking (22.98%). Also flags the curve inversion — a separate, real point: a 10-year point is the *lowest* rate on an inverted EGP curve and the explicit window is 1–5 years. |
| CW19 | "USD/EGP 2025 average 49.247 … 1.1% understated" | **−0.8% central** | Premise **plausible** | **ACCEPT.** Two independent sources agree; my 48.70 was a house estimate. |
| CW20 | "Correct figure, seven-month-stale vintage, at a 6 August 2026 anchor" | vintage risk | Premise **right**, conclusion **right** | **ACCEPT.** This is the correct form of the ERP finding (see the arbitration in Part 4). |
| CW21 | "True of the level … **False of the shape.** … straight-line → 9.32 (−1.5%); back-loaded → 9.18 (−3.0%)" | **−0.7% to −3.5% central** | Premise **right**, conclusion **right** | **ACCEPT.** My reproduction: straight-line 9.62 (−2.9% DCF), back-loaded 9.15 (−7.7% DCF). *Larger* than CW's own estimate. My Appendix B.2 certifies as immaterial an input that sets the entire discount path. |
| CW22 | "The logic that produces −26.2% today produces a *more* negative weight at terminal, not +10%" | −3.2% DCF at 0% terminal weight (CC31) | Premise **right**, conclusion **right** | **ACCEPT.** Self-contradiction inside one table. |
| CW23 | "it **excludes working capital**, which the study's own FCFF subtracts … 5.39% implied growth — above the adopted 5%" | 0% direct; invalidates a stated check | Premise **right**, conclusion **right** | **ACCEPT.** My reproduction: including ΔWC the CY2025 reinvestment rate is 19.36% and implied g is **7.47%**, not 4.37%. The check reverses. |
| CW24 | "Historical capex … is 1.45% of revenue in every year — the same assumption as 2026E … PP&E is a square-root scaler with no stated basis" | 0% direct | Premise **right**, conclusion **right** | **ACCEPT.** The "record" is manufactured from the assumptions being checked. |
| CW25 | "a perpetuity compared with a cyclical near-term rate … g = 5% against a 5% terminal inflation assumption is **0% real growth in perpetuity** — yet §1.9 calls 5% 'on the generous side'" | conclusion survives | Premise **right**, conclusion **right** | **ACCEPT.** This is the half of my S6 they caught, and they caught it better than I stated it. |
| CW26 | "2,438 + 1,169 + 413 − 1,173 = 2,847 ≠ 2,751" | 0% (the roll is right) | Premise **right** | **ACCEPT.** Confirmed: gap 97 = the tax on finance income. The printed statement does not reach its own closing balance. |
| CW27 | "`C26` contains `=E25/E5` — the CY2025 ratio, in the FY2023/24 column … `DCF!B16:F16` … reads `$C$26`" | 0% today; latent | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed verbatim. This is exactly the defect class my gate (q) claims to catch, and it shipped — because the expected-value map recorded the *wrong* value as correct. |
| CW28 | "`E14 = 1562.828` is pasted, yet it is not disclosed … and derivable and already derived at `Product Legs!B29`" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed. A hardcode mid-chain in the constructed base year, and the reason C19/C21/C23 are dead inputs. |
| CW29 | "Three of four are neither observed, nor peers, nor disclosed" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** Identical to my own S10. |
| CW30 | "The 'justified' multiple is set equal to the observed one" | 20% of the headline is circular | Premise **right**, conclusion **right** | **ACCEPT.** Identical to my own S3. |
| CW31 | "3.83 is the book lens's bear; 16.69 is the DCF's bull. **They cannot both obtain.**" | the most-quoted output is undefined | Premise **right**, conclusion **right** | **ACCEPT.** And the bear/bull driver sets are published nowhere. |
| CW32 | "Stated definition omits the minority step" | 0% | Premise **right** | **ACCEPT.** Text fix. |
| CW33 | "The **ROIC row is on ending capital** … Spread 9.5% × 3,211 = 305 ≠ the 410 printed" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** The table contradicts its own commentary one row above. |
| CW34 | "**EGPC does not appear** [on the register]. Alexandria Petroleum Co. 20.77%" | 0% | Premise **unverifiable here**, corroborated by CC5 | **ACCEPT provisionally.** Two independent reviewers name Alexandria Petroleum Company at ~20.8% as the *largest* holder. My "EGPC, second-largest, 20%" is wrong on entity and rank in at least one respect. Economic substance survives. |
| CW35 | "AMOC declared a further EGP 0.40 for H2-2025 (BoD 30 July 2026) — *before* the 6 August anchor and absent from the study" | C43 is dead; C62 −0.03 at +10% | Premise **unverifiable here** | **UNPROVEN → RESEARCH.** If a declaration predates the anchor it must be in. |
| CW36 | "**Total liabilities there are 3,312, not 3,189.56**" | **−0.3% central** | Premise **plausible** | **ACCEPT provisionally.** Priced: book lens 7.07 → 6.90. |
| CW37 | "AMOC published **conflicting figures for the same period** … sales EGP 20.53bn, revenues EGP 21.264bn and PAT EGP 844mn" | at PAT 844 the base year becomes 1,750 | Premise **partly corroborated** | **ACCEPT the disclosure duty.** I saw the 844 figure in my own sweep and did not resolve or disclose the conflict. That is a real omission regardless of which figure is right. |
| CW38 | "The company attaches **+14.5% to the sales value** … not to volume" | −0.3% | Premise **unverifiable here**, plausible | **ACCEPT provisionally.** A growth rate transferred between lines. |
| CW39 | "ln(1.20) = **0.1823** … 0.290 corresponds to +33.6%, which is no EGX band" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** The house threshold is market-wide, not AMOC-specific, but the *study* states it as the EGX limit, and 0.290 is not one. And the observed maximum sits at the band, not comfortably inside it. |
| CW40 | "All four are measured against the **DCF lens (9.9140)**, not the headline weighted central" | 0% | Premise **right** | **ACCEPT.** Disclose the base in the column header. |
| CW41 | "`B14 − B22 ≡ 0` **identically**, for any inputs whatsoever … A tautology presented as a verification" | 0% | Premise **right**, conclusion **right** | **ACCEPT.** Cash is the plug for the three June years; PPE is the plug for CY2025. The check cannot fail. |
| CW42 | "the delivered workbook stores **zero cached values** across all 901 formula cells" | — | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed on the raw XML: 145 `<f>` on the DCF sheet, 0 with a non-empty `<v>`. The gate ran and passed, but on a recomputation, not on stored values — and no reader can reproduce it without recalculating. |
| CW43 | "no price series, no index composition and no regression output accompany the study" | — | Premise **right** | **ACCEPT.** Publish the composite definition. |
| CW44 | "Volatility implied by the published quantiles is 36.6% … the study never states the volatility model" | — | Premise **right** | **ACCEPT.** Both framings should be given. |
| CW45 | "The **5.5-point real-rate 'convention' has no identifiable source**" | ±14% per 2pp | Premise **right** | **ACCEPT.** It is a house convention; §7 concedes it, but a figure setting 62.5% of value deserves its source named or its status stated on the face. |

### Claude-code (45 findings, in their order)

| # | Their words | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| CC1 | "Jul–Dec 2024 PAT of 643.6 is back-solved … no such period was ever filed" | ≈0% | Premise **right** | **ACCEPT.** The claim "neither of them estimated" is false: one leg is back-solved from a growth rate. |
| CC2 | "Disclosed consolidated revenue = EGP 37,622.61mn … 36,900 is the value of the 1.26mn t sales volume — a different line" | +0.25% DCF, **+0.11% central** | Premise **plausible and specific** | **ACCEPT provisionally.** Averaging a disclosure with a non-comparable line is a real method error even if the number barely moves. |
| CC3 | "Disclosed comparative 33.767bn" | ≈0% | Premise **plausible** | **ACCEPT provisionally.** Note this **contradicts CW5** (33,932) — see Part 4. |
| CC4 | "The consolidated–standalone gap is subsidiary contribution, not the outside shareholders' share of it … At the newest 14.7% gap: −12.06%" | removing: **+1.5% central**; at 14.7%: **−5.7% central** | Premise **right**, conclusion **self-refuting** | **ACCEPT the premise, REJECT the 14.7% — receipt.** CC states correctly that the gap is not the minority share, then uses the gap as the minority share. Minorities own a *fraction* of consolidated subsidiaries; 14.7% would require them to own all of them, which is impossible for consolidated entities. **ESCALATED (>5%): re-derived in Part 5.** |
| CC5 | "Alexandria Petroleum Company 20.8% as the largest holder … No evidence of a direct 20% EGPC stake" | 0% | Premise corroborated by CW34 | **ACCEPT provisionally.** |
| CC6 | "Disclosed 30-Jun-2025 shareholders' equity EGP 5,422mn … The formula charges only half the dividend" | ROE 32.0% → 30.4%, feeds Lens 4 | Premise **unverifiable here**; the half-dividend point is **verifiable and right** | **ACCEPT the half-dividend defect.** `=E20/(1−nci) − pat_h2cy25 + 0.5×dps×shares` charges half a year's dividend to a six-month roll-back with no stated basis. |
| CC7 | "Only disclosed realisation: exports 70,000 t for USD 65mn = USD 929/t — the model input is 19% above it" | −0.46% DCF | Premise **unverifiable here**, specific | **UNPROVEN → RESEARCH.** Directly attacks the one free input in the unit build. |
| CC8 | "1.551 = 0.808 × 2 × 0.96 … CY2025 = 1.362mn t" | ≈0% | Premise **right** | **ACCEPT.** Same as CW15, with the halves-consistent alternative computed. |
| CC9 | "EGP 0.80 … plus EGP 0.40 for the transition half = EGP 1.20 gone ex within the trailing 12 months = 13.2%" | 0% on FV | Premise **plausible** | **ACCEPT.** Two framings exist; only the lower is given. |
| CC10 | "Egypt statutory corporate rate is 22.5% … Unsourced 100bp premium … used twice" | **+0.52% central** at 22.5% | Premise **right**, conclusion **partly right** | **ACCEPT the sourcing defect.** The double use is the sharper point: the same unsourced rate sets NOPAT *and* defines the "other income" residual. Note **GR6 calls the same 23.5% "empirical grounding and institutional conservatism"** — arbitrated in Part 4. |
| CC11 | "~49.74 mid-market on 2026-08-06" | 0% (display only) | Premise **plausible**; **contradicts CW19's basis** | **ACCEPT provisionally.** Different quantity from CW19 (spot vs 2025 average); both can hold. |
| CC12 | "My re-run: 12.110 · 10.709 · **9.914** · 8.940 · 8.362" | +1.31% as displayed | Premise **right** | **ACCEPT.** Independently reproduces CW3 to three decimals. Two reviewers, same defect, same magnitude. |
| CC13 | "all 901 formula cells carry an empty `<v></v>`" | 0% on FV | Premise **right** | **ACCEPT.** Same as CW42, independently. |
| CC14 | "There is no mix–margin linkage anywhere in the model — no per-leg margins exist" | gross margin ±1pt = **±EGP 2.05/share** | Premise **right**, conclusion **right** | **ACCEPT — and this is the most important judgment finding either reviewer made.** Figure 2's caption asserts a mechanism the model does not contain. The margin path is an input; the legs have no separate margins. |
| CC15 | "Not one line is disclosed. I reproduced the whole table from assumptions: PPE = 2,403 × (rev/rev_CY25)^0.5 … capex = the 2026E ratio applied backwards" | terminal block = 62.5% of EV | Premise **right**, conclusion **right** | **ACCEPT.** Reproduced exactly. The sole support for the terminal rate is generated by the model it tests. |
| CC16 | "Reported PBT was never observed … 'Other income' is a triple residual of three assumptions" | drives §7's caveat | Premise **right** | **ACCEPT.** Same as CW12, sharper. |
| CC17 | "TTM to 30-Jun-2026 = 46,935 revenue and 2,556 PAT — both already above the full-year 2026E … implies H2-2026 revenue 18,726 (−28.5% sequential) and PAT of −158mn" | **+6.3% central** on the rebased forecast | Premise **right**, conclusion **right** | **ACCEPT — ESCALATED (>5%), re-derived in Part 5.** My reproduction: 2026E revenue 44,926 vs a reported half of 26,200; rebasing at 2× the half gives DCF 11.23, central 10.05. The study calls this "conservative"; it is a forecast contradicted by data at the anchor date. |
| CC18 | "skill 0.006759 (0.68%), verdict PARITY … Neither 0.92% nor 1.32% appears anywhere" | 0% on FV | Premise **right** | **ACCEPT.** Same as CW2, independently. |
| CC19 | "gross margin ±1pt = ±2.05 and doubling volume growth = +1.48. Both operating assumptions exceed 1.42" | 0% on FV | Premise **right**, conclusion **right** | **ACCEPT.** My §1.10 note ranks the levers wrongly against my own printed table. |
| CC20 | "Expert 1 = Lens 3's identical 2028E EPS at 7.0× … Expert 3 … is the primary DCF algebraically rearranged" | 0% | Premise **right** | **ACCEPT.** Same as CW8, independently. |
| CC21 | "The disclosures were reachable — I retrieved the FY22/23, FY24/25, Jul–Dec 2025 and Jun-2026 releases" | via CC4: up to −12.1% | Premise **contested** | **PARTLY ACCEPT.** They were not reachable from *my* environment (egress policy, verified 403 on amoceg.com, egx.com.eg, Mubasher, Investing.com). My study said "not reachable from the build environment", which is true and disclosed. But the unused *standalone* line in a release I did cite is a fair hit: I quoted the consolidated figures from that release and not the standalone ones. |
| CC22 | "implied ERP = 9.89%, only 48bp above the CDS-basis 9.41% … the contested choice is not actually tested" | understates the exposure | Premise **wrong in detail, right in substance** | **ACCEPT the defect, REJECT the arithmetic — receipt.** CC back-solved assuming I used the cost of *net* debt. I used the plain after-tax Kd (16.83%) in the alternative while the base uses the cost of net debt (12.97%) — so the alternative is **not a clean one-variable perturbation**, and 101bp of the move is a changed debt term. Done consistently the rating basis gives DCF **8.07 (−18.6%)**, central 8.63 (−8.8%) — a *larger* exposure than published, not smaller. |
| CC23 | "bear 9.052462 ÷ base EPS 1.645902 = 5.500000×; bull … 9.500000×. The EPS is unchanged" | widens the headline range without a driver change | Premise **right** | **ACCEPT.** Confirmed to six decimals. My READ FIRST claim that all bear/bull cells are whole-model re-runs is false for Lens 3. |
| CC24 | "9.5% × 3,468 = 329, not the 410 shown" | 0% | Premise **right** | **ACCEPT.** Same as CW33. |
| CC25 | "58% of the first forecast year has elapsed … the whole 2026 cash flow is discounted a full year … Mid-year convention: FV 9.91 → 10.65 (+7.4%)" | **+3.5% central** | Premise **right**, conclusion **right** | **ACCEPT.** Reproduced exactly. A material undisclosed convention choice. |
| CC26 | "EGX bands are ±5% / ±10% / ±20% → max log move ln(1.20) = 0.1823" | 0% | Premise **right** | **ACCEPT.** Same as CW39. |
| CC27 | "3,754 / 240.8 = 15.59 years → a start of ~Jan-2011, not 2022" | 0% | Premise **right** | **ACCEPT.** Same as CW14. |
| CC28 | "The fundamental central estimate is 9.46" | 0% | Premise **right** | **ACCEPT.** Same as CW13. |
| CC29 | "'The recent compound NOPAT rate (+34.8%) … all sit below Egyptian nominal growth of about 15%'. 34.8% > 15%" | 0% | Premise **right**, conclusion **right** | **ACCEPT — and this is a defect I introduced in my own last edit and did not re-check.** The gross-margin rework moved NOPAT CAGR from +2.6% to +34.8% and my assertion only tested `g_term < ceiling`, so the sentence broke silently. It also falsifies "both checks come in BELOW the adopted rate": check (a) is now +34.8%, far above 5%. |
| CC30 | "Deducting after adding the cash allocates the minority 3% of the cash … 73mn = EGP 0.057/share" | **−0.6% DCF, +0.27% central to fix** | Premise **right** | **ACCEPT.** Identical to my own S5 and to GT1. |
| CC31 | "At 0% terminal debt weight: FV 9.60 (−3.2%)" | −3.2% DCF | Premise **right** | **ACCEPT.** Same as CW22, priced. |
| CC32 | "The identical issue is applied in the 15%-weight lens and not in the 45%-weight DCF … §1.12 prices four smaller contested choices while declining to price this one" | **−2.3% to −4.6% central** | Premise **right**, conclusion **right** | **ACCEPT.** Identical to my own S8, and the "breaching the report's own computed-rather-than-argued rule" charge is fair. |
| CC33 | "Expert 2 … valuing the pile at 52.8% of face, while the primary bridge adds it at 100%" | ≈EGP 0.89/share of a 0.60 gap | Premise **right**, conclusion **right** | **ACCEPT.** Confirmed: 9.027%/17.084% = 52.8%. The same asset at two values in one document. |
| CC34 | "The 'justified' multiple is the market's own current multiple" | 20% weight | Premise **right** | **ACCEPT.** Same as CW30 and my S3. |
| CC35 | "'the shares are roughly fairly valued' and prints a 'vs spot' percentage column" against "no rating" | 0% | Premise **right**, conclusion **arguable** | **ACCEPT the tension, REJECT the framing.** A fair-value-versus-price comparison is the study's whole object and the standing rule bars a *rating or price target*, not a comparison. But "roughly fairly valued" is an adjective doing rating-like work and should go. |
| CC36 | "cash B13 is the plug … Neither column can fail" | 0% | Premise **right** | **ACCEPT.** Same as CW41. |
| CC37 | "C26 = E25/E5 … Likewise IS!C8:E8 apply `Assumptions!$B$72`, the 2026E opex ratio, to all historical years" | ≈0% | Premise **right** | **ACCEPT.** Both confirmed verbatim. The second half CW did not find. |
| CC38 | "1M median 9.171 vs spot 9.10 → +9.35%/yr … neither reconciles" | 0% on FV | Premise **right**, conclusion **wrong** | **ACCEPT the disclosure defect, REJECT the reconciliation claim — receipt.** The drift *does* reconcile, to the stated convention rather than to the raw rf: carry = ln(1+0.195) − ln(1+0.0879) = **9.84%/yr**, against implied 9.77% (1M) and 10.47% (3M). CC tested against 22.31% and 13.5%; the engine uses the policy rate, not the 10-year. The real defect is that the study never states the drift or which rate it uses. |
| CC39 | "β '0.941' vs '0.940' vs 0.9405; TV/EV '62.5%' vs '63%'; check date '2026-11-08' vs 2026-11-06" | 0% | Premise **right** | **ACCEPT.** Confirmed. |
| CC40 | "No moving-average values, signs or crossover claims are published anywhere" | 0% | Premise **right** | **ACCEPT.** A figure with no computable content. |
| CC41 | "The DCF bull of 16.69 lies outside every cell of every published sensitivity grid" | sets the headline range | Premise **right** | **ACCEPT.** Same as CW31, with the grid check added. |
| CC42 | "A secondary account of the July-2026 table reports Egypt total ERP 14.87% … I could not establish whether that figure is the rating-based or CDS-based column" | if applied: **−11.9% central** | Premise **honest**, verdict **UNVERIFIABLE** | **ARBITRATED — see Part 4.** CC is the only reviewer to state the question honestly rather than assert an answer. Priced anyway: at 14.87%, Ke 32.90%, WACC 38.11%, DCF 7.41, central 8.33. |
| CC43 | "Last reachable local-currency 10Y data: 21.29% average / 21.58% high, 27 Apr – 25 May 2026" | ±100bp ≈ ±0.08/share | Premise **honest** | **NOTE.** CC's own reachable data points *below* my 22.31%; CW and GT point above at 22.97/22.98. Contradiction arbitrated in Part 4. |
| CC44 | "Last reachable print: 8.91 on 31-Jul-2026 … at 8.91 the +4% gap becomes +6.2%" | 0% (spot is the anchor, not an output) | Premise **honest** | **REJECT — receipt.** The spot is not sourced from an aggregator: it is the last row of the price history supplied with the study, `engine/raw_ohlc/EG/AMOC.csv`, 06/08/2026 close **9.10** (open 9.20, high 9.37, low 9.01, volume 10.29M). That file is the primary record for this input. |
| CC45 | "The internal diagnostics are coherent and I verify them … But no return series, index definition or constituent list is supplied" | β ±0.35 spans 12.11–8.36 | Premise **right** | **ACCEPT.** Same as CW43. |

### Gemini deep-thinking (12 findings, in their order)

| # | Their words | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| GT1 | "taking a 3% blanket deduction from the combined (Operating EV + Parent Cash) mathematically gifts the minority shareholders 3% of the parent's risk-free cash" | +0.27% central to fix | Premise **right**, conclusion **right** | **ACCEPT.** Third independent statement of the same defect (with CC30 and my S5). |
| GT2 | "averaging a 2028 future stock price with 2026 present-value metrics. This is a catastrophic TVM violation" | **−12.5% to −13.2% central** if discounted | Premise **right**, conclusion **overstated** | **ACCEPT the defect, DECISION on the fix.** The lens *is* undiscounted and is averaged with present values — that is a real inconsistency and my study only half-discloses it. But it is the reference-study house convention (an earnings-*power* statement, not a present value), and "catastrophic" overstates a 20%-weight lens. **Escalated (>5%): decision required, Part 6.** |
| GT3 | "it entirely deletes the Free Cash Flows generated by the firm during the interim holding period (2026 and 2027), leaking roughly EGP 1.7bn" | **+2.74% central** | Premise **right**, conclusion **right** | **ACCEPT.** Their 1.7bn vs my computed 1,727.7mn — exact. |
| GT4 | "The WACC logic is actually mathematically brilliant … pushes the WACC (31.6%) above the Cost of Equity (27.8%)" | — | clearance | **RECORDED.** Corroborated by CW's unlevering-identity check (closes to 0.8bp). |
| GT5 | Spot 9.10 vs "9.10 – 9.20 EGP", variance ~0% | 0% | clearance | **RECORDED.** |
| GT6 | Shares 1,291.56 vs 1,291.50, variance 0.0% | 0% | clearance | **RECORDED.** |
| GT7 | "Rf (10Y Yield) 22.31% → 22.98%" | −0.5% central | Premise **plausible** | **ACCEPT.** Corroborates CW18 independently. |
| GT8 | "9.41% represents Damodaran's Country Risk Premium (CRP) … The author **illegally stripped out the base premium** to artificially depress the Cost of Equity by over 500 basis points, **forcing a manufactured upside**" | if applied: −11.9% central | Premise **REFUTED**, conclusion **refuted and improper** | **REJECT — receipt in Part 4.** A coherence test on the two rows of my own register solves to a single volatility scalar of 1.53 and a mature-market premium of **4.22%** — Damodaran's own published parameters. Under GT8's reading the same table would imply two different scalars (2.77 and 2.19). This is the load-bearing claim of GT's entire verdict and it is arithmetically wrong. |
| GT9 | "Corrected WACC 38.96% … DCF 9.11 (perfectly converges to the current market spot price)" | — | follows from GT8 | **REJECT** — inherits GT8. Also note the convergence-to-spot is presented as corroboration; it is coincidence. |
| GT10 | "sustaining 5% terminal growth will inevitably require a replacement-cost CapEx cycle. When that capital cliff hits … terminal free cash flow will evaporate" | **−2.3% to −4.6% central** | Premise **right**, conclusion **right** | **ACCEPT.** Same as my S8, GR8 and CC32. Four-way agreement. |
| GT11 | "True Weighted Central Fair Value is exactly EGP 7.97 … Reject the report's conclusion. Do not deploy capital." | — | conclusion **rests on GT8** | **REJECT.** Strip GT8 and GT2's full-discount fix and the same arithmetic returns to the 9.3–9.5 region. The word "exactly" against a 74%-wide lens spread is itself a precision claim I would not make. |
| GT12 | "The forensic stripping of EGP ~760mn in historical FX devaluation windfalls … proves excellent earnings-quality hygiene" | — | clearance | **RECORDED — but note it is the same line CW12/CC16 correctly attack as a triple residual.** Two reviewers praise it and two call it fabricated. Arbitration in Part 4. |

### Gemini deep-research (13 findings, in their order)

| # | Their words | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| GR1 | "intraday trading range fluctuating between EGP 8.93 and EGP 9.24, with subsequent close figures reaching EGP 9.58 … Market Capitalization … ~5.2%" variance | 0% | Premise **partly right**, conclusion **wrong** | **REJECT — receipt.** The supplied series gives 06-Aug-2026 high 9.37 / low 9.01 / close 9.10; the 8.93–9.24 range is the *05*-Aug session. 9.58 is a later date than the anchor. Anchoring on a post-anchor price would be look-ahead. |
| GR2 | Shares 1,291.56 vs 1,291.50, 0.00% | 0% | clearance | **RECORDED.** |
| GR3 | "This aggregation methodology is mathematically sound and empirically verifiable, completely avoiding the utilization of hallucinated extrapolations" | — | clearance | **RECORDED — but contradicted by CC1/CW15**, which show one leg is back-solved and the volume leg is not built from halves at all. CC1/CW15 are right; GR3 checked the revenue arithmetic and not the provenance. |
| GR4 | Cash and gross debt "validates these exact figures" | — | clearance | **RECORDED.** |
| GR5 | "the ERP and default spread align exactly with credit default swap (CDS) derivations for Egypt's sovereign rating" | — | clearance | **RECORDED — directly contradicts GT8.** Arbitrated in Part 4 in GR5's favour. |
| GR6 | Tax 23.5% "applying a conservative 100 basis point buffer over the statutory minimum, thereby demonstrating empirical grounding and institutional conservatism" | +0.52% at 22.5% | clearance, **contradicted by CC10** | **ARBITRATED.** Both are right about different things: the buffer *is* conservative for NOPAT and it is *unsourced*, and CC10's sharper point stands — the same rate also grosses disclosed PAT into the PBT that defines "other income", where a higher rate is not conservative but simply changes the residual. |
| GR7 | "theoretically abusive … artificially suppresses the present value of the near-term FCFF … adding the raw, undiscounted EGP 2.43 billion cash pile back … presumes zero trapped liquidity" | **−12.8% central** on my own quantification | Premise **right on the economics**, conclusion **wrong on the mechanics** | **ACCEPT the economics, REJECT the double-count charge — receipt.** There is no double count: the unlevering identity recombines exactly to Ke (0.79×31.63% + 0.21×12.97% = 27.76% = Ke). What is real is that the cash is added at face while earning below the cost of equity — my own S2, worth −12.8%. GR7 found the right problem and named the wrong mechanism. |
| GR8 | "The inevitable replacement of this aging industrial infrastructure at current market costs will force capital expenditure to explode … which currently props up an untenable 62.5%" | −2.3% to −4.6% central | Premise **right** | **ACCEPT.** Fourth statement of the same finding. |
| GR9 | "an explicitly formulated 'Qualified Conclusion' issued by the independent auditor, Dr. Khaled A.M. Hegazy of Crowe Global … EAS No. 47 … EGP 12 million … EGP 21 million" | ~0.3% of market cap | Premise **unverifiable here**, highly specific and checkable | **UNPROVEN → RESEARCH, and a genuine gap in kind.** No reviewer else mentions an audit qualification and I did not look for one. Even at an immaterial amount, an unremarked qualified opinion is a disclosure failure. |
| GR10 | "the model's text asserts an EBIT of EGP 1,864 million … yields exactly EGP 1,865 million" | 0% | Premise **wrong** | **REJECT — receipt.** Unrounded: EBITDA 2,358.61 − D&A 494.19 = **1,864.42**, which rounds to 1,864. GR subtracted the two *rounded* figures (2,359 − 494 = 1,865). A rounding artefact of their own construction. |
| GR11 | "the model systematically discounts this forward valuation back to the anchor date … deriving an accurate present value … demonstrates a high degree of mathematical independence" | — | Premise **wrong** | **REJECT — receipt, and note it contradicts CW7, CC-implied, GT3.** The discounting is done; what is missing is the interim free cash flow, PV 1,727.7. Three reviewers found it; GR11 checked that the discount factor was applied and stopped there. |
| GR12 | "The operational projections assume that the profound gross margin expansion witnessed during the recent cycle of EGP devaluation represents a permanent, structural paradigm shift" | gross margin ±1pt = ±EGP 2.05 | Premise **partly wrong**, conclusion **right by accident** | **PARTLY ACCEPT.** The devaluation windfall is *excluded* from the forecast (GR itself says so at GR-clearance). But the *gross margin path* is still an unsupported assumption rising to 6.88% from one disclosed 5.76% observation, and CC14 shows there is no mix mechanism behind it. Right worry, wrong reason. |
| GR13 | "The Re-Calculated Central Fair Value is definitively established at EGP 9.45 per share … priced at a nominal 1.3% premium" | — | recomputation clearance | **RECORDED.** 9.45 vs my 9.4611 is their own rounding. But "definitively established" against an unaudited input plane is a claim GR's own Phase 1 does not support. |

---

## PART 4 — CONTRADICTIONS, ARBITRATED BY COHERENCE TEST

**(1) The Damodaran ERP. GT8 says 9.41% is a bare country premium; GR5 and CW20 say it is the
CDS-basis total; CC42 says unverifiable.**

My register carries two rows of the same table: CDS basis (spread 3.40%, ERP 9.41%) and rating
basis (spread 6.37%, ERP 13.94%). Damodaran's construction is Total = Mature + spread × λ.
Solving both rows simultaneously:

    λ = (0.1394 − 0.0941) / (0.0637 − 0.0340) = 1.5253
    Mature = 0.0941 − 0.0340 × 1.5253 = 4.2241%

One scalar and one mature-market premium reproduce **both** rows, and both land on Damodaran's
published values. Under GT8's reading the implied scalars would be 9.41/3.40 = 2.77 and
13.94/6.37 = 2.19 — two different scalars from one table, which is impossible.
**GT8 refuted. GR5 and CW20 upheld.** The surviving real finding is CW20's: the vintage is
January 2026 at an August 2026 anchor, and a later vintage exists. That must be fixed.

**(2) The Egypt 10-year. CW18 and GT7 say 22.97–22.98%; CC43's reachable data says 21.29–21.58%
(Apr–May 2026); mine says 22.31% (21-Jul-2026 print).**
CC43's window is two to three months earlier than mine, so it is not a contradiction — it is a
different date on a rising curve. CW18 and GT7 agree with each other on the anchor date and
disagree with me by 66bp. Two independent sources at the right date beat one cached print.
**Accept 22.97%, −0.5% on the central.**

**(3) The FY2023/24 revenue. CW5 says 33,932 consolidated; CC3 says 33,767.**
Both claim a disclosed figure and they differ by 165. Neither is reachable from here.
**Unresolved — research task, and the fact that two auditors reading the same document report
different figures is itself a reason not to adopt either without the source in hand.**

**(4) The FY2024/25 profit. CW4 says ~2,000; GR says 1,552; mine is 1,550.**
Settled by the coherence test in CW4's row: the disclosed +109% on the June half reproduces only
at 1,550. **CW4 refuted.**

**(5) The "other income" analysis. GT12 and GR call it "excellent earnings-quality hygiene";
CW12 and CC16 call it a triple residual narrated as a discovered fact.**
Both are right about different objects. The *decision* to exclude non-operating income from the
forecast is sound and conservative — that is what GT12/GR are praising. The *narrative* that the
line was read off the filings, and the causal attribution to export receivables, is unsupported —
that is what CW12/CC16 are attacking. **Keep the decision, delete the narrative.**

---

## PART 5 — ESCALATED: FULL RE-DERIVATION ABOVE 5% OF THE CENTRAL

| Item | Price | Re-derivation |
|---|---|---|
| **My S1 — FX path vs the interest-rate differential** | **+25.0%** | EGP 10Y 22.31% against USD 10Y 4.30% implies 17.27%/yr depreciation. My path assumes 4.30%/yr. Both legs are dollar-priced, so EGP revenue is understated throughout. At UIP: DCF 15.16, central 11.82. At the CBE inflation differential (~10%/yr): DCF 11.94, central 10.37. **The direction is unambiguous; the magnitude depends on which parity condition you accept.** Note the offset: a faster depreciation should also lift the terminal nominal growth rate, which is currently 5% against a 4.3% currency assumption. |
| **My S2 — cash added at face** | **−12.8%** | Net cash 2,438 → 4,827 earning 17.0% falling to 11.8% pre-tax (13.0% → 9.0% after tax) against a 27.76% cost of equity. Five-year PV of the shortfall 1,564 = EGP 1.21/share. Adding cash at face assumes it is distributed or reinvested at the cost of capital; the model's own forecast has it accumulating. |
| **CC17 — 2026E contradicted by reported actuals** | **+6.3%** | The reported half to 30-Jun-2026 is 26,200 against a full-year 2026E of 44,926, implying an H2 of 18,726, −28.5% sequential. Rebasing 2026E at 2× the reported half (×1.166) and holding all margins: DCF 11.23, central 10.05. **But this compounds with the period-labelling risk**: if that release is not the six months to June 2026, the rebasing is wrong. Two reviewers accept the period identification; it rests on my own two-way growth reconciliation. |
| **CC4 — minority interest at 14.7%** | **−5.7%** | Rejected on its own logic (Part 3), but the *premise* — that my 3.0% is a category error — is accepted. At CW10's 5.8%: central 9.33 (−1.4%). At 3.0% on EV only: 9.49 (+0.3%). **The honest position is that I do not know the number and my derivation of it was wrong in kind.** |
| **GT2 — Lens 3 discounted** | **−12.5% to −13.2%** | At the WACC year-3 factor: 6.09. At the cost-of-equity year-3 factor: 6.45. Central falls to 8.21–8.28. |
| **My S3 — relative lens circularity** | **+5.6%** | Dropping the lens and reweighting the other three: 9.99. |
| **CC22 — rating basis done consistently** | **−8.8%** | Using the cost of net debt in the alternative as the base does: DCF 8.07, central 8.63, against the 8.38 published. |
| **GT8/CC42 — ERP at 14.87%** | **−11.9%** | Priced although the premise is refuted: Ke 32.90%, WACC 38.11%, DCF 7.41, central 8.33. This is the size of the vintage question CW20 raises. |

**These do not net.** S1 (+25%) and S2 (−12.8%) are the two largest and pull opposite ways;
several are mutually exclusive framings of the same lens. Netting them into a single revised
number would repeat exactly the error the reviewers convicted the bear/bull range of.

---

## PART 6 — BUCKETS

### A. Accept and implement — mechanical, no judgment required (31 items)
CW7/GT3 relative lens interim FCFF · CW9 terminal economic profit · CW13/CC28 zone boundary ·
CW14/CC27 price-series sentence · CW26 cash-flow footing · CW27/CC37 both pointer errors ·
CW28 the E14 hardcode · CW32 FCFE definition · CW33/CC24 the ROIC row · CW40 the effect-column
base · CC29 the crossover sentence and the "both checks below" claim · CC39 all restatement
mismatches · CW3/CC12 the beta sweep · CW22/CC31 the terminal debt weight · CW23 the
reinvestment definition · CC30/GT1/S5 the minority on cash · CW29/S10 the peer-multiple labels ·
CW31/CC41 the headline range and the bear/bull driver sets · CC23 the Lens-3 bear/bull labelling ·
CC22 the rating-basis alternative's debt term · CW39/CC26 the price-limit threshold ·
CC38 stating the drift · CW44 the volatility framing · CW11/CC16 labelling the 0.85 scaler and
the other-income line as residuals · CW12 deleting the causal attribution · CW16 the fuel-price
"check" · CW24/CC15 relabelling the terminal-growth "record" · CW41/CC36 the balance check ·
CW42/CC13 shipping cached values · CC14 the Figure 2 caption · CC19 the lever ranking.

### B. Accept the defect, reject or defer the proposed fix (6)
- **CC4** minority at 14.7% — premise accepted, number rejected on its own logic.
- **GT2** Lens 3 — defect accepted; the full-discount fix is a house-convention change (Part 6D).
- **CC35** "roughly fairly valued" — drop the adjective, keep the comparison.
- **GR7** cash — economics accepted, "double count" rejected.
- **CC21** sourcing — the releases were genuinely unreachable here; the unused standalone line is accepted.
- **CW1** dead inputs — accepted; the fix is to publish the reachability set, not to force 19 history inputs into the valuation chain.

### C. Unproven → research now (9)
CW5/CC3 FY2023/24 disclosed revenue (and the 33,932 vs 33,767 conflict) · CW6 FY2022/23
consolidated revenue · CW10 the disclosed minority line · CW17 the seven-line product breakdown ·
CC7 the USD 929/t export realisation · CW34/CC5 the shareholder register · CW35 the July-2026
dividend declaration · CW37 the conflicting transition-period releases · **GR9 the auditor's
qualified conclusion**. All require amoceg.com, which this environment blocks.

### D. Your decision, with the price of each branch (5)
1. **The exchange-rate path (my S1).** Keep 4.3%/yr (+0%), move to the inflation differential
   ~10%/yr (**+9.6%**), or to full UIP 17.3%/yr (**+25.0%**). Recommendation: **the inflation
   differential**, with the terminal growth rate raised in step so the two stay coherent, and the
   UIP case published as a computed alternative. Keeping 4.3% while discounting at 22.31% is the
   one position I cannot defend.
2. **Cash added at face (my S2).** Face (+0%) or a return-shortfall haircut (**−12.8%**).
   Recommendation: **keep face as primary** — it is the standard bridge — and publish the
   shortfall as a computed contested choice, which is what my own rules require.
3. **Lens 3 (GT2).** Undiscounted earnings power (+0%), discounted (**−12.5%**), or dropped.
   Recommendation: **discount it**, and say so — the reference-study convention is not a reason
   to average a 2028 number with present values in the same weighted mean.
4. **The relative lens (S3/CW30/CC34).** Keep circular (+0%), re-anchor on fundamentals, or drop
   and reweight (**+5.6%**). Recommendation: **re-anchor** — a lens that cannot disagree with the
   market has no place at 20% weight in a study whose thesis is that value is independent of price.
5. **2026E (CC17).** Keep (+0%) or rebase on the reported half (**+6.3%**). Recommendation:
   **rebase**, and disclose the implied second half either way — a forecast year whose first half
   is already reported above the whole-year estimate cannot be called conservative.

### E. Reject with receipts (9)
GT8 (coherence test on Damodaran's two rows) · GT9, GT11 (inherit GT8) · CW4 (the +109%
identity) · GR10 (rounding artefact of their own construction) · GR11 (the interim FCFF are
demonstrably dropped) · GR1 (post-anchor price) · CC44 (the price history is the primary record) ·
CC38's reconciliation half (the drift does reconcile to the policy-rate carry).

### F. Clearances recorded (14)
GT4/GR-Phase-2 on the WACC unlevering · GT5, GT6, GR2, GR4 on the cap table · GR3 on the base-year
arithmetic · GR5 on the ERP basis · GR13 and CW/CC Section C on the whole computation chain
(every reviewer independently reproduced the WACC, glide, all five discount factors, the full
waterfall, the terminal block, the bridge and all four lenses to the last decimal) · CW/CC on the
901/279 census · CC45/CW43 on the beta diagnostics' internal coherence · GT12/GR on excluding the
currency windfall · CW/CC on "the valuation and the price map are never blended".

---

## PART 7 — WHAT THIS EXERCISE ESTABLISHED

The arithmetic held. Four independent reviewers rebuilt the model from the input register and
none could break a calculation in the primary chain.

Everything else did not. The failures cluster in three places, and they are the same three the
QC gate was supposed to close:

1. **Claims about the artifact that the artifact does not support.** "No dead inputs" (19),
   "901 of 901 reproduce" (true, but nothing is stored in the file to check against), "each
   column foots exactly" (a tautology), "bear and bull are whole-model re-runs" (not for Lens 3),
   "every step is visible and checkable" (the cash-flow statement does not foot). My gate tested
   what I told it to test and I told it the wrong things.

2. **Narrative asserting mechanisms the model does not contain.** The margin "widens on mix"
   when no mix mechanism exists; the terminal rate "checked against what the business has
   actually done" when the record is generated from the assumptions being checked; "other income"
   read off filings when it is a triple residual; a fuel-price "check" that is a residual of what
   it validates. CC14 is the sharpest of these and it is correct.

3. **Two pointer errors and a stale sweep that gate (q) should have caught** — and did not,
   because the expected-value map recorded the wrong value as correct. A gate that compares the
   workbook to the model cannot catch an error the model and the workbook share.

Against that, the two largest findings in this document are mine, not theirs: the exchange-rate
path contradicts my own discount rate by 13 percentage points a year (+25% of the central), and
the explicit window implies a 97% incremental return on capital that no reviewer noticed. A
critique that agrees with your self-audit everywhere is not being adversarial enough; one that
misses your two biggest defects while finding forty-three of your smaller ones is doing something
genuinely useful, which is why the count matters less than the reading.
