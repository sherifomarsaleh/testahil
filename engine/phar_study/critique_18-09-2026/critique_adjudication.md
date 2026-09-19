# PHAR (EIPICO) — adjudication of the forensic audit of 18 September 2026

**Phase 1. Assessed and priced. NOTHING HAS BEEN IMPLEMENTED; awaiting approval.**

**27 findings raised, 27 answered, 0 unaddressed.** A further **16** rows are this desk's own, found before the critique was read in detail; 43 rows in total.

Published answer, two-sided: **Frame A EGP 33.00** (provision charge permanent) and **Frame B EGP 49.68** (provision charge normalising), against a struck spot of EGP 127.30 (3 Sep) and a latest known price of **EGP 128.00** (6 Sep) — **-74.2%** and **-61.2%**. Both branches breach, so the study is HELD under [R-GAP-02] and files no market dissent. **5% of Frame A is EGP 1.65.**

## Bucket counts, on the critique's 27

| Bucket | Count | Rows |
|---|---:|---|
| `accept-and-implement` | **23** | C01, C03, C04, C05, C06, C07, C08, C09, C10, C12, C13, C14, C15, C16, C17, C18, C19, C20, C21, C22, C23, C24, C26 |
| `accept-defect-reject-fix` | **2** | C02, C27 |
| `unproven-go-research` | **0** | — |
| `reject-with-receipts` | **1** | C25 |
| `user-decision` | **1** | C11 |

## How to read the price column

Every price is the effect on the published central of that one correction, everything else held at its delivered value, computed by re-running engine/phar_study/compute.py with a textual patch in a sandbox copy and reading central_two_sided back. The real tree is never written to. compute.py reproduces the delivered study_numbers.json byte for byte, so the baseline is exact. 5% of Frame A is EGP 1.65.

A price of **0.00** means the finding cannot move either central. It does not mean the finding is small: the `damage_note` on every such row says what it does damage instead. No finding is called immaterial anywhere in this register without a number beside the word.

## The ten largest priced findings

| # | Row | Finding | Frame A | Frame B | Bucket |
|---|---|---|---:|---:|---|
| 1 | `C01` | The domestic price escalator does not do what both the workbook and the bibliography say | +178.48% | +122.60% | `accept-and-implement` |
| 2 | `SA-10` | The domestic price basis note calls a 15.9% real cut 'no real price gain' | +178.48% | +122.60% | `accept-and-implement` |
| 3 | `SA-01` | The currency path's FY2026 average sits above the pound's own 52-week high, and the tens | +34.39% | +21.88% | `user-decision` |
| 4 | `C02` | The terminal value is not built on the construction the study declares | -33.57% | -22.99% | `accept-defect-reject-fix` |
| 5 | `SA-14` | The published two-sided axis is narrower than the uncertainty in a single input the stud | +28.18% | +23.93% | `accept-and-implement` |
| 6 | `C11` | The associate stake is carried at a Gulf multiple without the cost-of-equity adjustment  | -20.97% | -13.93% | `user-decision` |
| 7 | `C12` | Two useful lives in one model - the disclosed one used only where it raises the charge | -9.56% | -6.35% | `accept-and-implement` |
| 8 | `C13` | The minority is charged 18 a year in profit and deducted at 4.0 of book in the bridge | -3.41% | -2.27% | `accept-and-implement` |
| 9 | `C03` | Beta is regressed against the analyst's own coverage universe, not the exchange's publis | -2.75% | -2.33% | `accept-and-implement` |
| 10 | `SA-02` | The beta is a composite of the covered library - and this desk can run the conforming re | -2.75% | -2.33% | `accept-and-implement` |


**Not every row above is a proposed change, and the distinction matters more than the ranking.** `C02` is a bucket-2 row: its price is what the critique's PROPOSED FIX would do, and the fix is rejected, so nothing moves. `SA-14` is not a correction at all — it is the conforming beta regression's own 90% confidence interval, priced to show that one input's sampling error is wider than the study's whole published two-sided spread. `SA-01` and `C11` are `user-decision` rows. The rows that actually move the answer if approved are `C01`, `C12`, `C13`, `C03`, `C17` and `C10`, and their stacked effect is the table below.

**The same ten collapsed to distinct findings.** `SA-02` restates `C03` and `SA-10` restates `C01`, so the ten above are eight distinct defects. Collapsed and re-filled from the next largest:

| # | Row(s) | Distinct finding | Frame A | Frame B |
|---|---|---|---:|---:|
| 1 | `C01 + SA-10` | The domestic price escalator does not do what both the workbook and the bibliography say | +178.48% | +122.60% |
| 2 | `SA-01` | The currency path's FY2026 average sits above the pound's own 52-week high, and the tens | +34.39% | +21.88% |
| 3 | `C02` | The terminal value is not built on the construction the study declares | -33.57% | -22.99% |
| 4 | `SA-14` | The published two-sided axis is narrower than the uncertainty in a single input the stud | +28.18% | +23.93% |
| 5 | `C11` | The associate stake is carried at a Gulf multiple without the cost-of-equity adjustment  | -20.97% | -13.93% |
| 6 | `C12` | Two useful lives in one model - the disclosed one used only where it raises the charge | -9.56% | -6.35% |
| 7 | `C13` | The minority is charged 18 a year in profit and deducted at 4.0 of book in the bridge | -3.41% | -2.27% |
| 8 | `C03 + SA-02` | Beta is regressed against the analyst's own coverage universe, not the exchange's publis | -2.75% | -2.33% |
| 9 | `C17` | Two tax rates still run, against a stated remediation that one now runs both | +0.85% | +0.72% |
| 10 | `C10` | The local cost of debt does not reproduce from its own stated construction | -0.24% | -0.20% |

## What the corrections do to the answer, stacked and measured

Every line below is a separate re-run of `compute.py` carrying every correction above it. Prices are not additive and this table is the reason they are not quoted as if they were.

| Stack | Frame A | vs price | Frame B | vs price |
|---|---:|---:|---:|---:|
| As delivered | 33.00 | -74.2% | 49.68 | -61.2% |
| + beta on the conforming EGX30 regression [C03] | 32.09 | -74.9% | 48.52 | -62.1% |
| + the local cost of debt reproduces from its own construction [C10] | 32.01 | -75.0% | 48.42 | -62.2% |
| + the debt tax shield on one rate [C17] | 32.29 | -74.8% | 48.77 | -61.9% |
| + one disclosed useful life throughout [C12] | 29.18 | -77.2% | 45.66 | -64.3% |
| + the minority at its share of value [C13] | 28.05 | -78.1% | 44.53 | -65.2% |
| + the domestic price at zero real on the house ladder [C01]  <- THE UNDISPUTED SET | 86.16 | -32.7% | 104.63 | -18.3% |
|    then + the associate at the cost-of-equity-adjusted 6.33x [C11a] | 79.24 | -38.1% | 97.71 | -23.7% |
|    then + the currency anchored on the realised 2026 level [SA-01] | 97.43 | -23.9% | 115.42 | -9.8% |
|    then + both judgement rows together [C11a + SA-01] | 90.51 | -29.3% | 108.50 | -15.2% |

**THE ANSWER TO THE QUESTION THIS RESPONSE EXISTS TO ANSWER.** The undisputed set — every correction this desk accepts and implements that moves a number — takes Frame A from 33.00 to **86.16** and Frame B from 49.68 to **104.63**, and the gaps from −74.2% / −61.2% to **−32.7% / −18.3%**. **NEITHER BRANCH COMES INSIDE 10%.** Adding the currency row (`SA-01`, a `user-decision` and a change to the house path rather than to this study) takes Frame B to **115.42, −9.8%, INSIDE THE BAND** — which would release this study from the [R-GAP-02] publish block, since a two-sided answer is held only if EVERY branch sits more than 10% below. Adding the associate row as well (`C11`, also a `user-decision`) pushes it back out to −15.2%. **The publish verdict turns on two judgement calls and on nothing else.**

## The self-audit, and what the critique missed

Run first, against the Sweep Register and the standing rules, before the critique was read past its summary table. The question asked was the one the protocol names: *what do the filings and the house records disclose that the model does not consume?*

| Row | Finding | Frame A | Also in the critique? |
|---|---|---:|---|
| `SA-01` | The currency path's FY2026 average sits above the pound's own 52-week high, and the tension the rebuild ledger registered is still unresolved | +34.39% | not raised by the critique |
| `SA-02` | The beta is a composite of the covered library - and this desk can run the conforming regression, which the auditor could not | -2.75% | also raised by the critique as its 03 |
| `SA-03` | beta_ex_subject_price.json is a stale artefact read by two delivered-document builders and written by nothing - and the gate that exists for this cannot see it | 0.00 | not raised by the critique (it found the symptom at 08) |
| `SA-04` | The study's own numeric-traceability check cannot match any of the typed figures that went stale - a check that could not fail on the thing that failed | 0.00 | not raised by either reviewer |
| `SA-05` | The lens record declares a two-sided primary and carries zero branches | 0.00 | not raised by the critique |
| `SA-06` | The published fair-value field's bull is the one lens the study's own record excludes | 0.00 | not raised by the critique (its 20 is the adjacent point) |
| `SA-07` | The study carries no bridge record at all | 0.00 | not raised by the critique, which found two of its clauses empirically |
| `SA-08` | The study carries no cost-of-capital schedule record | 0.00 | not raised by the critique |
| `SA-09` | The committed fx_path_note states a first-year figure the committed path does not carry, and describes the construction the study rejected | 0.00 | not raised by the critique |
| `SA-10` | The domestic price basis note calls a 15.9% real cut 'no real price gain' | +178.48% | also raised by the critique as its 01, and it is its largest finding |
| `SA-11` | LATEST FILINGS is still not cleared, and the one search that would settle it was not among those run | 0.00 | not raised by the critique, which had no primary-source access and said so |
| `SA-12` | The study is struck at a price that is no longer the latest known one | 0.00 | the critique raises the staleness differently, at its 04 |
| `SA-13` | The live site publishes a fair value this house no longer holds, and the sign of the disagreement is the same but its size is not | 0.00 | not raised by the critique, which had no repository access |
| `SA-14` | The published two-sided axis is narrower than the uncertainty in a single input the study publishes as a point | +28.18% | the critique gestures at the input's leverage at its 03 but does not make this comparison |
| `SA-15` | The instrument that would have caught the Appendix A.1 defect was never run on this study | 0.00 | not raised by the critique, which found the defect itself at its 06 |
| `SA-16` | The study never states that the Egyptian Exchange's trading week runs Sunday to Thursday, which is what makes its own check date reproducible | 0.00 | logged as the adjacent defect behind the critique's 25, which is rejected |

**11 of the 16 are defects no reviewer raised** (`SA-01`, `SA-03`, `SA-04`, `SA-05`, `SA-06`, `SA-07`, `SA-08`, `SA-09`, `SA-11`, `SA-13`, `SA-15`), and **7** of those could not have been reached from outside the repository at all. The sharpest is `SA-04`: the study's own numeric-traceability check reports zero typed financial numerals in its builders while the bibliography builder carries at least seven, every one a full edition stale and every one in the delivered document — because the regex it uses can only match comma-grouped numbers and figures with four integer digits and three decimals. **It is a check that could not fail on the thing that failed.** `SA-03` is the same species one level out: the repository gate built for stale artefacts cannot see any of PHAR's nine, because it looks for a key called `central` and this house writes `centre`.

## The reverse read, which is evidence against our own answer

The critique solves the published model for EGP 127.30 one driver at a time and finds four of five reverse reads absurd and one believable. **That one was re-solved here rather than accepted**, and it holds: a flat domestic price growth of 12.52% a year gives Frame A **125.22**, and 11.50% gives Frame B **127.51**. A reverse read landing on a believable number is evidence against our answer, not for it.

Two corrections to how the critique frames it, both in the direction of making our answer *less* comfortable and one in the other direction:

- **Their 'Believable? Yes — below the 16% and 12% the model's own CPI path applies in FY2026–27' compares a flat rate against the first two years of a declining ladder.** The honest comparison is cumulative: 12.52% flat compounds to 1.8042 over five years against the CPI ladder's 1.6289, so the price the market is paying needs domestic prices to rise **10.8% in REAL terms**, not merely to track inflation. Full pass-through at zero real is worth a lot and is not the whole gap: it takes Frame A to 91.89, which is 72% of the traded price.
- **They never ran the reverse read on the currency**, which is the other half of the same wedge and which this desk found independently. The two are not substitutes and they do not offset: measured jointly they are almost exactly additive (+178.5% and +34.4% alone, +212.9% together), because the price path acts on domestic revenue and the currency acts on imported cost and export revenue.

## The register

### `accept-and-implement` — 37 rows

#### C01 · The domestic price escalator does not do what both the workbook and the bibliography say it does

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C14:G14; bibliography input `dom price growth`; study Table 7, Table 20
- **They say** “Both artefacts state the same basis: "Administered prices track inflation, no real gain" ... The path carried is 5.0% / 8.0% / 7.5% / 6.5% / 5.5%. ... Over five years the selling price compounds to 1.3697 while domestic prices compound to 1.6289 - a 15.9% cumulative real price cut.”
- **Claimed severity** TOTAL FAIL, +182%
- **Price** Frame A **+58.8944** (**+178.48%**) · Frame B **+60.9051** (**+122.60%**)
- **How it was priced** compute.py patch dom_price_growth=I([0.05,0.080,0.075,0.065,0.055] -> [0.16,0.12,0.09,0.075,0.07]. Read back central_two_sided: A 91.8919, B 110.5840. Gross-margin path 39.19/37.28/36.86/36.76/36.46 -> 43.17/42.79/42.94/43.20/43.46.
- **What it damages** Also: the model's forecast margin decline, which the study presents as an OUTPUT of an honest unit build, is the artefact of this one mismatch.
- **Premise** right · **Conclusion** right
- **Evidence** Re-run confirms the auditor to within 1.5 points (they report +182%, measured +178.5%). THE RECEIPT IS THE AUDITED RECORD, not the arithmetic: gross margin ran 44.64% (FY2023), 44.87% (FY2024), 44.00% (FY2025) across the period in which the average pound went from roughly 30.7 to 47.74 - a 55% devaluation on a cost stack the study itself measures as 68.4% dollar-priced. In the single year the imported cost base rose 55% in pounds, the margin did not fall; it ROSE 23 basis points. The administered price passed a 55% cost shock through inside the fiscal year. The model then forecasts prices recovering 31% of a far smaller escalation in FY2026 rising to 79% by FY2030, and nothing in the filings supports the Egyptian Drug Authority ceasing to approve adjustments. [R-MACRO-01 EXTENDED 18-09-2026], adopted today, is decisive on the CLAIM: a quantity that grows below inflation is a real-decline forecast and a study may not call it the absence of one.
- **Note** The implementation is NOT simply 'set it to the CPI ladder'. [R-MACRO-01] requires the rate stored as (real, inflation-path id). Zero real is the basis note's own stated assumption and is what is priced here; any other real rate must be stated and evidenced. Note also that zero real does NOT close the gap - it takes Frame A to 91.89, still 27.8% below the price.

#### SA-10 · The domestic price basis note calls a 15.9% real cut 'no real price gain'

- **Source** self-audit 18-09-2026 (run before the critique was read in detail) · **duplicate of** C01
- **Location** compute.py line 475 dom_price_growth source field
- **They say** “The path assumes price growth tracks domestic inflation as it converges on the central bank's target, with no real price gain”
- **Claimed severity** also raised by the critique as its 01, and it is its largest finding
- **Price** Frame A **+58.8944** (**+178.48%**) · Frame B **+60.9051** (**+122.60%**)
- **How it was priced** See C01.
- **What it damages** [R-MACRO-01 EXTENDED 18-09-2026], adopted today, is exactly on this: a quantity that does not keep pace with inflation is a real-decline forecast and a study may not call it the absence of one. WHAT IS REFUSED IS THE CLAIM, NEVER THE CONSTRUCTION - a below-inflation administered price path is a legitimate thing to forecast and describing it as 'no real gain' is a false statement about the model.
- **Premise** right · **Conclusion** right
- **Evidence** Same as C01. Recorded here because the self-audit reached it from the rule side rather than from the arithmetic side, and because the rule adopted today settles what the fix has to be: the rate stored as (real, inflation-path id) with the real component STATED, not a nominal path typed.

#### SA-14 · The published two-sided axis is narrower than the uncertainty in a single input the study publishes as a point

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** lens_record.primary.range against the beta regression's own confidence interval
- **They say** “central_two_sided: Frame A 32.9975, Frame B 49.6789 - 'the study's single most consequential contested judgement'”
- **Claimed severity** the critique gestures at the input's leverage at its 03 but does not make this comparison
- **Price** Frame A **+9.2985** (**+28.18%**) · Frame B **+11.8868** (**+23.93%**)
- **How it was priced** Priced at the conforming regression's own 90% interval: beta 0.4478 gives A 42.2960 / B 61.5657; beta 0.8509 gives A 24.2598 / B 38.5112. Frame A therefore spans 24.26 to 42.30, a width of 18.04, against the provision axis's 33.00 to 49.68, a width of 16.68.
- **What it damages** The study nominates the provision charge as its single most consequential contested judgement and builds its whole two-sided architecture on it. Measured on the conforming regression, ONE input's own sampling error is wider. That does not make the provision framing wrong - it is the right axis for a judgement a reader has to make - but the document does not tell a reader that the coefficient it publishes to three decimals carries a range wider than the answer's whole published spread.
- **Premise** right · **Conclusion** right
- **Evidence** own_stock_beta('PHAR','EG','EGX') returns ci90 [0.4478, 0.8509] with se 0.1225 and r2 0.1667 on n=249 - a wide interval, honestly reported by the estimator, on a regression that clears the usability gate. The handover pack asked auditors to attack whether the provision charge is the right axis; this is the answer that came back from our own side.
- **Note** It is NOT a reason to re-axis the study. It is a reason to publish the beta interval's value consequence beside the beta, which the sensitivity sheet already computes and the document does not foreground.

#### C12 · Two useful lives in one model - the disclosed one used only where it raises the charge

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C38 = 6.2%; DCF!B23; bibliography input `asset life weighted` = 13.8 years
- **They say** “The disclosed life appears in the terminal, where the shorter life raises the maintenance charge; the chosen, longer life runs the five explicit years, where it lowers the depreciation charge. ... Impact: -6.2% ... Frame A EGP 33.00 -> 30.94.”
- **Claimed severity** PARTIAL FAIL (material), -6.2%
- **Price** Frame A **-3.1552** (**-9.56%**) · Frame B **-3.1552** (**-6.35%**)
- **How it was priced** compute.py patch dep_rate=I(0.062 -> 0.0724637681159420), i.e. 1/13.8: A 29.8423 (-9.56%), B 46.5237 (-6.35%). Envelope for context: at 4.5% (22.2 years) A 38.5894; at 8.0% (12.5 years) A 27.6984.
- **What it damages** Only one of the two lives carries a citation. The 6.2% input's own source field says '6.2% is a blended rate consistent with roughly a sixteen-year average life' and is registered at the House layer; the 13.8 years is registered at the Company layer, derived from the FY2024 audited note 3.1 lives weighted by note 4.1 gross cost, with the depreciable base footing to the note's own total.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed in compute.py: dep_rate drives the explicit window (line 1232) and the terminal catch-up (line 1460), while asset_life_weighted drives TV.build()'s maintenance (lines 1511, 1536, 1559). [R-TERM-01] is explicit that A LIFE THIS DESK CHOSE IS NOT A DISCLOSED LIFE (SIGCM clause 1). The terminal is right; the explicit window is the limb with no source. The auditor prices it at -6.2%; measured it is -9.56% on Frame A and -6.35% on Frame B, so their figure happens to match Frame B.
- **Note** The auditor states -6.2% and Frame A 30.94; measured, Frame A is 29.84. Their number is Frame B's.

#### C13 · The minority is charged 18 a year in profit and deducted at 4.0 of book in the bridge

- **Source** forensic audit 18-09-2026
- **Location** Income Statement!E25:I25 = -18.0; Assumptions!C80 = 3.9998; SOTP Bridge!B10
- **They say** “The cash-flow model capitalises 100% of subsidiary cash flow, and the model's own income statement assigns 18.0 a year to minorities in every forecast year. Capitalised on the study's own terminal terms that stream is worth about 194m, or 1.15 a share, against the 0.02 deducted.”
- **Claimed severity** PARTIAL FAIL (material), -3.4%
- **Price** Frame A **-1.1259** (**-3.41%**) · Frame B **-1.1259** (**-2.27%**)
- **How it was priced** compute.py patch nci_bridge=I(3.999807 -> 194.0), the auditor's own capitalisation of the 18.0 forecast charge on the study's terminal terms: A 31.8716 (-3.41%), B 48.5530 (-2.27%).
- **What it damages** The -18.0 is itself a perimeter contradiction: audited minorities ran 0.99 / 1.21 / 16.24, and almost all of the FY2025 figure belonged to the company deconsolidated in Q1-2026 - the same event the bridge relies on to justify deducting 4.0.
- **Premise** right · **Conclusion** right
- **Evidence** [R-BRIDGE-01] clause (ii) is directly on point and predates this audit: 'THE MINORITY AT BOOK OR NOT AT ALL ... the model capitalises 100% of subsidiary cash flow, so the minority's claim is worth its SHARE OF THAT VALUE, not its historical cost ... deducted from EQUITY value, NEVER from enterprise value.' PHAR deducts book. SEE ALSO SA-07: this study carries NO bridge_record at all, so assert_bridge() has never been run on it and check_bridge.py reports 'PHAR carries no bridge record'.

#### C03 · Beta is regressed against the analyst's own coverage universe, not the exchange's published index

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C49 = 0.629; study Table 10, Table 19; bibliography 6.2
- **They say** “an equal-weighted composite of 36 Egyptian listed names built from the full covered price library ... Impact: Direction indeterminate; magnitude large. Each 0.10 of beta is worth roughly EGP 4-5 a share ... The true EGX-regressed coefficient is unverifiable here.”
- **Claimed severity** TOTAL FAIL, magnitude large
- **Price** Frame A **-0.9065** (**-2.75%**) · Frame B **-1.1587** (**-2.33%**)
- **How it was priced** beta_regression.own_stock_beta('PHAR','EG','EGX') run live: beta 0.6493355960727006, r2 0.1667, se 0.1225, n 249, window 4.81y, Dimson weekly W-THU, index_file raw_indices/EG/EGX30.csv, index_asof 2026-07-22, usable True, conforming True. compute.py patch beta=I(0.629 -> 0.6493355960727006): A 32.0910, B 48.5202.
- **What it damages** The composite contains the subject at about 2.8% weight, which the study discloses. Every figure hanging off beta - the cost of equity, the terminal cost of equity, both centres, the book lens, the relative lens and the normalised lens - rests on a non-conforming regressor.
- **Premise** right · **Conclusion** wrong
- **Evidence** THE PREMISE IS A HARD FAIL AND IS ACCEPTED WITHOUT ARGUMENT: SIGCM clause 6 and the WACC block both say a constituent composite is a hard fail and not a tier, and every study in this repository once made this error. THE CONCLUSION IS MEASURED AND IT IS NOT LARGE. The auditor could not run the regression; this desk can, and did. The conforming EGX30 coefficient is 0.6493 against the composite's 0.629 - a difference of 0.0203, worth -0.91 a share on Frame A. The correction moves the answer AWAY from the price, which is the only direction that proves the discipline is not fitting.
- **Note** What IS large, and the auditor stopped one step short of it, is the coefficient's own uncertainty: the conforming 90% interval [0.4478, 0.8509] spans Frame A 42.30 to 24.26 - an 18.04 spread, WIDER than the 16.68 spread between the two published frames. See SA-14.

#### SA-02 · The beta is a composite of the covered library - and this desk can run the conforming regression, which the auditor could not

- **Source** self-audit 18-09-2026 (run before the critique was read in detail) · **duplicate of** C03
- **Location** compute.py line 797; bibliography 6.2
- **They say** “Own-stock first-tier regression: weekly logarithmic returns of the company's own shares against an equal-weighted composite of 36 Egyptian listed names built from the full covered price library”
- **Claimed severity** also raised by the critique as its 03
- **Price** Frame A **-0.9065** (**-2.75%**) · Frame B **-1.1587** (**-2.33%**)
- **How it was priced** See C03. own_stock_beta('PHAR','EG','EGX') = 0.6493355960727006 against the composite's 0.629.
- **What it damages** SIGCM clause 6 hard fail on provenance, small on value.
- **Premise** right · **Conclusion** right
- **Evidence** Same as C03. Recorded here because the self-audit found it independently and could close it, where the critique could only name it.

#### C17 · Two tax rates still run, against a stated remediation that one now runs both

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C102, C112 (use C9 = 22.5%); DCF!B7 (uses C10 = 23.5%); study Table 18
- **They say** “The cash-flow engine was fixed; the debt tax shield was not. Both the first-year and the terminal after-tax cost of debt still multiply by (1 - C9), the statutory 22.5%.”
- **Claimed severity** PARTIAL FAIL, about 5 basis points
- **Price** Frame A **+0.2792** (**+0.85%**) · Frame B **+0.3570** (**+0.72%**)
- **How it was priced** compute.py patch TAX = V['tax_stat'] -> V['tax_eff_fwd']: A 33.2767 (+0.85%), B 50.0359 (+0.72%).
- **What it damages** A declared fix that is half-made, and a claim about the model ('One rate now runs both') that the model contradicts.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed at compute.py line 987: TAX = V['tax_stat'], the statutory 22.5%, used for the debt shield while the cash-flow engine takes tax_eff_fwd at 23.5%. Table 18's remediation row is quoted verbatim in the delivered text. The auditor calls it 'immaterial' at 5 basis points of WACC; measured on the answer it is +0.85% on Frame A, which is above the 0.00 they imply and still small.
- **Note** WHICH WAY THE FIX GOES IS A JUDGEMENT the auditor states as settled. A tax shield is worth the rate at which interest is actually deducted, which is the STATUTORY rate; the effective rate differs because of deferred-tax movements and associate income arriving already taxed, neither of which shields interest. The defect is that Table 18 claims one rate runs both when two do; the honest fix may be to state the shield is deliberately taken at the statutory rate, which is the auditor's own second option.

#### C10 · The local cost of debt does not reproduce from its own stated construction

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C50 = 24.81%; study Table 10; bibliography input `kd egp`
- **They say** “23.00% + 2.50% = 25.50%, not 24.81%. The bibliography resolves the gap: its kd egp row derives 24.81% from the ten-year sovereign yield of 22.31% plus a 250 basis-point corporate credit spread - the previous edition's yield.”
- **Claimed severity** TOTAL FAIL (reproduce test), about +0.5%
- **Price** Frame A **-0.0785** (**-0.24%**) · Frame B **-0.1002** (**-0.20%**)
- **How it was priced** compute.py patch kd_egp=I(0.2481 -> 0.2550): A 32.9190, B 49.5787.
- **What it damages** The 'above the sovereign by construction' floor now stands 181bp above a yield that moved 69bp, so the floor is no longer the construction it is described as.
- **Premise** right · **Conclusion** right
- **Evidence** Arithmetic confirmed: the study's own rf input is 0.23 and the stated construction is sovereign + 250bp, which gives 25.50%; the carried 24.81% is 22.31% + 250bp, the superseded yield. Measured effect is -0.24% on Frame A, the OPPOSITE sign to the auditor's '+0.5%' - a higher cost of debt raises the discount rate and lowers the value. Their direction is wrong; the defect is real and the reproduce test is absolute.
- **Note** The auditor states the impact as '+0.5%'; measured it is -0.24% on Frame A and -0.20% on Frame B.

#### C04 · A 3 September edition delivered under a 9 August masthead, with a false price date in three places

- **Source** forensic audit 18-09-2026
- **Location** Study masthead; Table 10 source column; Table 18 remediation row; Assumptions!C3; READ FIRST!B11
- **They say** “Prepared 9 August 2026 - share price EGP 127.30 at the close of 6 August 2026. ... EGP 127.30 is not the 6 August close and never was.”
- **Claimed severity** TOTAL FAIL, no effect on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** No model input touched; 127.30 is the number the model holds and it is the right one. Priced at 0.00 on both branches by inspection of spot/spot_date in study_numbers.json.
- **What it damages** The masthead read verbatim from the delivered document reads 'Prepared 9 August 2026 - share price EGP 127.30 at the close of 6 August 2026'. study_numbers.json carries spot_date 2026-09-03 and the input register's own spot row records that the 6 August close was 130.05. So the price date is false, the preparation date is the superseded edition's, and Table 18 lists as a CLOSED defect ('The risk-free rate and the share price are struck on ONE date') something that is open - the yield is a 6 August print against a 3 September price, 28 days apart.
- **Premise** right · **Conclusion** right
- **Evidence** Verified verbatim in the delivered docx (line 4 of the extracted text). Confirmed against study_numbers.json spot_date '2026-09-03' and inputs.spot source text naming the 3 September close and recording 130.05 for 6 August.

#### C05 · The technical read and the whole probability map are memories of the superseded edition

- **Source** forensic audit 18-09-2026
- **Location** Study 2, 3, 6, Tables 13-15, 17; Monte Carlo!B3:C4; bibliography 6.1
- **They say** “The anchor is the EGP 130.05 close of 2026-08-06 ... The cleaned price series runs 02 Jan 2011 to 06 Aug 2026 - it does not contain the close the valuation uses.”
- **Claimed severity** TOTAL FAIL, no effect on fair value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** Section 3 is walled off from the valuation by [R-LENS-01]; no valuation input reads it. 0.00 on both branches.
- **What it damages** Every moving average, RSI, ATR, MACD reading, 52-week range, pivot cluster, volatility input, percentile and touch probability in the study is computed on data ending six weeks before the valuation date, and the published one-month band's check date of 2026-09-06 had already passed twelve days before the audit.
- **Premise** right · **Conclusion** right
- **Evidence** Delivered text line 95: 'Table 14 - the percentile map. The anchor is the EGP 130.05 close of 2026-08-06.' Line 87 opens the technical section on the same 130.05. The valuation is struck at 127.30 on 2026-09-03. This is the 29-Jul-2026 standing rule - when the library moves, the technical read moves with it, IN THE SAME PASS - not obeyed across a re-strike.

#### C06 · Appendix A.1 does not foot in any of its five forecast columns

- **Source** forensic audit 18-09-2026
- **Location** Study Table 20 (Appendix A.1); Income Statement!E13:I14 and !E25:I25
- **They say** “Following the table's own rows: FY2026E gives 2,175.5 against the 2,110.9 printed. Every forecast year is short by 64.6 / 89.5 / 93.7 / 92.0 / 89.1.”
- **Claimed severity** TOTAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A printing defect; no input moves. 0.00 on both branches.
- **What it damages** A reader following the instructions the page itself gives arrives 64.6 to 93.7 away from the operating profit the page prints. This is [R-ENF-01 EXTENDED 04-Sep-2026] - a waterfall a reader is asked to follow must reach the answer it prints.
- **Premise** right · **Conclusion** right
- **Evidence** Reproduced independently from study_numbers.json forecast arrays: gross_profit - marketing - rnd - ga - prov_A gives 2175.5 / 2343.4 / 2685.1 / 3048.9 / 3379.4 against published ebit_A of 2110.9 / 2253.9 / 2591.4 / 2956.9 / 3290.3 - short by 64.6 / 89.5 / 93.7 / 92.0 / 89.1, matching the auditor to the decimal. The two missing rows are the board fee (2.0) and the 20.58% selling-and-administrative share of depreciation. SEE ALSO SA-15: PHAR sits on the waterfall-assertion ratchet as NO IMPORT, so the shared instrument that exists for exactly this was never run on this study.

#### C07 · Four of the five terminal cash-flow lines are typed constants, against an explicit and tested claim that they are live

- **Source** forensic audit 18-09-2026
- **Location** DCF!B22, B23, B24, B25, B44; READ FIRST!B3
- **They say** “The four lines are literals: 423.085728, -674.802126, -0.000000, -717.450174 ... The terminal block - 80% of core enterprise value - responds to no driver.”
- **Claimed severity** TOTAL FAIL, nil on the delivered answer
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** Every constant is the correct number for the delivered driver set and the auditor rebuilt all four to six decimals. 0.00 on both branches.
- **What it damages** READ FIRST!B3 claims the terminal block moves with any driver and that the claim 'is tested, not asserted'. It is not: change the depreciation rate and FY2030E depreciation moves while the terminal still adds back 423.09 and still charges 674.80. The workbook cannot be used as the study says it can, in the block carrying 80% of core enterprise value.
- **Premise** right · **Conclusion** right
- **Evidence** The study's own driver_test.py passes 30 asserted directions and reports 138 further inputs live - and the terminal block is not among the assertions, which is why a passing driver test coexists with four frozen cells. The recalculation gate is equally blind by construction: it reconciles the workbook TO ITSELF, so four literals that happen to be correct reproduce perfectly ([R-BRIDGE-01]'s lesson - a model that recalculates is not a model that is right).

#### C08 · The published price of the ex-subject beta is wrong by an order of magnitude

- **Source** forensic audit 18-09-2026
- **Location** Study Table 19 (caveats); bibliography 6.2
- **They say** “Removing it gives 0.565 rather than 0.629, which would RAISE the two centres by about EGP 32.04 and EGP 23.18 a share. ... Running the delivered model at beta = 0.5652 gives Frame A 36.01 and Frame B 53.53 - uplifts of EGP 3.01 and EGP 3.85.”
- **Claimed severity** TOTAL FAIL, nil on published value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** compute.py patch beta=I(0.629 -> 0.5652): A 36.0065, B 53.5252. Uplifts 3.01 and 3.85 against the 32.04 and 23.18 the caveat table claims. The auditor's figures reproduce exactly. 0.00 on the delivered central.
- **What it damages** The error sits in the caveat table, where it inflates the apparent cost of the conservative choice the study is defending by roughly tenfold.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed by re-run to four decimals. THE CAUSE, WHICH THE AUDIT DID NOT REACH, IS SA-03: the figures are computed in docx_phar.py as (XBJ['beta_ex_subject_centre_A'] - LN['centre_A']) where XBJ is beta_ex_subject_price.json - an artefact dated 31 August carrying 65.04 and 72.86, the SUPERSEDED edition's answers, read by two delivered-document builders and written by no generator anywhere in the repository. Subtracting today's 33.00 and 49.68 from a stale 65.04 and 72.86 is exactly how 32.04 and 23.18 arise.

#### C09 · Bibliography sections 3 and 4 and primary document P10 are the previous edition's, wholesale

- **Source** forensic audit 18-09-2026
- **Location** Bibliography Table B1 row P10; Table B3 (judgements); Table B4 (negative results)
- **They say** “Eight material contradictions with the study it accompanies ... associate contribution normalised to 320 (study: 250); terminal growth 5% (study: 7%); terminal debt weight 20% (study: 25.5%) ... the sensitivity table runs 3% to 7% and the value ranges from EGP 78 to EGP 98 (study's grid: EGP 17 to 48).”
- **Claimed severity** TOTAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A delivered-document defect; no input moves. 0.00 on both branches.
- **What it damages** The document whose whole function is to let a reader audit the study contradicts it on the terminal growth rate, the discount rate, the bridge, the cost stack and the published range. Depth-bar standard 1 makes the bibliography a QC item in its own right.
- **Premise** right · **Conclusion** right
- **Evidence** Verified in the delivered bibliography text: 'The associate contribution is normalised to EGP 320 million' (against an input register on the same document reading 250 and stating it was 'REVISED DOWN from 320'); 'Terminal growth is 5%, which is roughly zero in real terms ... the value ranges from EGP 78 to EGP 98'; '8.1x ... 6.7x ... 9.8x ... would give EGP 133 a share'. ALL OF THESE ARE HARDCODED PROSE LITERALS IN docx_biblio.py at lines 183, 206, 211 and 232-234 - frozen at the 09-Aug edition and never moved when the model was rebuilt on 3, 7, 17 and 18 September. See SA-04: the study's own numeric-traceability check cannot match any of them.
- **Note** The auditor's mitigating half is correct and worth keeping: the INPUT register (278 rows, four fields each) is current and correct, names the mid-year July 2026 country-risk vintage and its four values, and states what the January vintage carried. The inputs are properly sourced; the three narrative registers are not.

#### C14 · 1.5 declares four weights and then states they give a number they do not give

- **Source** forensic audit 18-09-2026
- **Location** Study 1.5; Table 1; Fundamental Valuation!B7:B9
- **They say** “0.50x33.00 + 0.20x43.91 + 0.15x48.65 + 0.15x56.78 = 41.10, and the Frame B equivalent is 49.44 - which the same table prints two rows below as the weighted blend this edition replaced.”
- **Claimed severity** PARTIAL FAIL, nil
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** The published centres ARE the unweighted cash-flow readings and are correct; the sentence explaining how they were reached is not. 0.00 on both branches.
- **What it damages** The prose describes the retired construction while the table prints the current one, in the section that tells a reader what the answer IS.
- **Premise** right · **Conclusion** right
- **Evidence** Verified verbatim in the delivered text (line 44): 'the cash-flow weight of 50% is carried in full on ONE frame at a time ... book value against sustainable return at 20%, relative multiples at 15%, and normalised earnings power at 15%. That gives EGP 33.00 a share on Frame A'. study_numbers.json confirms the arithmetic: lenses.blend_A = 41.0961 and blend_B = 49.4368, both committed and both labelled retired_blend in the lens record. [R-LENS-03] retired the typed blend; the study's model obeys and its prose does not.

#### C15 · The relative lens is built on an average of the two frames the study says it never averages

- **Source** forensic audit 18-09-2026
- **Location** Relative & Normalized!B11 = AVERAGE(B9:B10); study Table 6 leg 1; 1.5
- **They say** “The justified-multiple leg's earnings base of EGP 5.46 is the mean of Frame A's 5.2774 and Frame B's 5.6410. The relative lens therefore does turn on the contested judgement.”
- **Claimed severity** PARTIAL FAIL, +/- EGP 0.4 on the lens
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A cross-check lens; neither centre reads it. 0.00 on both branches. On the lens itself the auditor's figures are 48.27 (Frame A alone) and 49.04 (Frame B alone) against a published 48.65.
- **What it damages** A breach of the document's most-repeated rule - the study states five times that the frames are never averaged - and a false independence claim about a lens both centres are published beside.
- **Premise** right · **Conclusion** right
- **Evidence** Reproduced from the source: compute.py line 1696 reads eps_fwd = (eps_26_A + eps_26_B) / 2, and study_numbers.json confirms eps_26_A 5.277397, eps_26_B 5.640997, eps_fwd 5.459197, which is their exact arithmetic mean. The workbook's own note pleads that 'Averaging the two frames' EARNINGS is not averaging the two VALUATIONS' - true of the arithmetic and beside the point, because 1.5 tells a reader this lens does not turn on the judgement at all, and it does.

#### C16 · Three workbook basis notes describe the superseded build of the terminal - on the cells carrying 80% of core value

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!B56, B62; Peer & Sector!D8
- **They say** “B56: 'A sourced 5% medium-term inflation target plus an UNSOURCED 5.5-point real convention' - which gives 10.5%, while C56 holds 12.5%. ... A reader auditing C56 against its own basis reproduces 10.5% and concludes the single most terminal-sensitive number in the model is 200bp wrong. It is not wrong - the note is.”
- **Claimed severity** PARTIAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** Reference case only, to size what the note asserts: patching ke_term to the note's 10.5% risk-free gives A 45.96 and B 66.26, confirming the auditor's 45.96 exactly. The delivered cell is right, so the price of the finding on the central is 0.00.
- **What it damages** The gap between the delivered rate and the rate its own note implies is 39% of the Frame A centre in APPARENT error - a reader doing exactly what a careful reader should do concludes the most terminal-sensitive number in the model is 200bp wrong.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed at build_xlsx_phar.py line 300, which types 'A sourced 5% medium-term inflation target plus an ...'. The current derivation is the one [R-MACRO-01] mandates: terminal inflation 7.0% plus the 5.5-point real-rate convention = 12.5%, DERIVED and never quoted, and study_numbers.json derived.note says exactly that. The auditor's own recomputation column agrees the delivered cell is correctly derived.
- **Already carried** yes — The CELL is already correct and was corrected by rebuild-ledger lever 4 on 04-09-2026, which is recorded as worth -24.66% when it was made. What was not corrected is the three notes describing it.

#### C18 · The crux's '32% of FY2030 revenue' is 32% of a revenue figure the study does not publish

- **Source** forensic audit 18-09-2026
- **Location** Study 1.7; Sensitivity!A34
- **They say** “8,871 / 18,608 (the published FY2030E revenue) = 47.7%. The 32.3% is 8,871 / 27,479 - the enlarged revenue including the increment itself.”
- **Claimed severity** PARTIAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A framing defect in a stated hurdle; no input moves. 0.00 on both branches.
- **What it damages** It makes the hurdle the market is pricing look a third smaller than it is against the business as forecast - and the crux is the study's own nominated central question.
- **Premise** right · **Conclusion** right
- **Evidence** Arithmetic reproduced: forecast.revenue[-1] = 18,608.03, so 8,871/18,608 = 47.67% and 8,871/27,479 = 32.28%. Both framings are legitimate and the dual-framing rule requires BOTH to be stated; only the smaller is. Verified verbatim in the delivered text (line 61).

#### C19 · '2.3 times what the plant cost to build' converts a historical outlay at a 2030 exchange rate

- **Source** forensic audit 18-09-2026
- **Location** Study 1.7
- **They say** “7,011 / 100 = 70.11 - the model's FY2030E exchange rate. ... On the company's own recorded figure the market is paying 3.25x the build cost, not 2.3x.”
- **Claimed severity** PARTIAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A unit error in a headline claim; no input moves. 0.00 on both branches.
- **What it damages** It understates the study's own headline proposition by 40%, in a comparison the study offers specifically as 'a multiple of an observable outlay'.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed against the study's own inputs: fx_path[-1] = 70.1139, and 100 x 70.1139 = 7,011. The observable outlay is cip_fy25 = 4,901.22, which is USD 100m at the study's own disclosed FY2025 average of 49.48 (4,948). 15,914/4,901 = 3.25x. A future rate applied to a past outlay, in the one place the study asks a reader to trust an observable.

#### C20 · The normalised-earnings lens reverses the depreciation step the whole study exists to charge

- **Source** forensic audit 18-09-2026
- **Location** Relative & Normalized!B32:B37; study 1.4
- **They say** “Those three years carried depreciation of 105, 103 and 118. Applying their average margin to FY2027 revenue gives operating profit of 2,888 against the model's own 2,254 after the 425 depreciation charge that is the study's central mechanism.”
- **Claimed severity** PARTIAL FAIL, nil on the two centres
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** This lens enters neither centre - the study's own lens record lists it under lenses_excluded with the reason 'not a permitted lens for any class in the registry'. 0.00 on both branches.
- **What it damages** It produces the highest of the five readings (56.78) by undoing the thesis, and 1.4 describes only the first of the two givebacks.
- **Premise** right · **Conclusion** right
- **Evidence** The premise checks out against the study's own history block: dna was 105.25 / 102.81 / 117.73 in FY2023-25 against a forecast dep of 295.7 rising to 437.5 - so a margin averaged over the pre-commissioning years, applied to post-commissioning revenue, does carry the old depreciation load and not the new one.
- **Note** THE DEEPER DEFECT IS MINE AND IS LARGER (SA-06): this lens, which the study's own record excludes as impermissible for this class and says 'does not enter either centre', nevertheless SETS the published fair-value field's bull at 56.78, because compute.py takes fair_bull = max(vals) across all five readings. The committed lens_record.envelope says 33.00-49.68. Two envelopes in one model, and the one a reader receives is built on the excluded lens.

#### C21 · Two price anchors on one technical page

- **Source** forensic audit 18-09-2026 · **duplicate of** C05 — same root cause (the technical read not re-run at the re-strike), separate row because the two are separately visible to a reader and separately fixable.
- **Location** Study 2 and Table 13
- **They say** “Every ladder distance reproduces off 127.30 ... Every prose figure reproduces off 130.05 ... A reader cannot tell which close the section is about.”
- **Claimed severity** PARTIAL FAIL, nil
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; the technical section is walled off from the valuation.
- **What it damages** The narrative states one close and the table beneath it prints another.
- **Premise** right · **Conclusion** right
- **Evidence** Verified in the delivered text: line 87 'The price closed 130.05 above a rising 20-day (101.58) ... the last close sits 17% below that high and 198% above that low'; line 307 'Last close | 127.30'. This is C05's defect surfacing inside one section rather than a separate cause.

#### C22 · The workbook still calls Frame A's 5.25% 'the three-year average' after the study retracted that label

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!B34
- **They say** “B34: 'Permanent, at the three-year average.' Study 1.9: 'That is NOT the three-year average, and this edition no longer calls it one.'”
- **Claimed severity** PARTIAL FAIL, nil
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** A label; no input moves. 0.00 on both branches. For reference the study publishes the true three-year average reading: at 6.516% Frame A is 24.55.
- **What it damages** A retracted label surviving in the delivered model, on the study's own nominated contested judgement.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed at build_xlsx_phar.py line 255, which types the string 'Permanent, at the three-year average'. The study's own input register for prov_pct_permanent carries the retraction in capitals: 'LABEL CORRECTED: this is NOT the three-year average, which the earlier edition called it.' The correction reached the register and the document and not the workbook.

#### C23 · A table that says it is summed from its own column is not

- **Source** forensic audit 18-09-2026
- **Location** Study Table 3; 1.6
- **They say** “1,943 + 3,591 + 751 + 2,967 + 49 = 9,301. The three domestic rows sum to 6,285.”
- **Claimed severity** PARTIAL FAIL, under 0.02%
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; a rounding artefact of the printed components.
- **What it damages** Under a caption that promises the total is the sum of its column, the printed components sum to 9,301 and the printed total is 9,302.
- **Premise** right · **Conclusion** right
- **Evidence** Reproduced from the study's own channel inputs: 1943.421 + 3591.140 + 751.062 + 2967.480 + 49.366 = 9302.469, which rounds to 9,302 as a total and whose individually-rounded components sum to 9,301. The defect is one of caption rather than arithmetic and is worth 0.011% of the line. The study's own footing_check.py examines 42 tables and reports zero unreconciled totals, so its tolerance absorbs this.

#### C24 · The Q1 finance-cost movement is stated two different ways

- **Source** forensic audit 18-09-2026
- **Location** Study Headline, 1.7 and Table 17; bibliography input `int path`
- **They say** “Study, three times: 'financing expense of EGP 312.9 million ran DOWN 6.1% year on year.' Bibliography: '312.862 of financing expense in three months, DOWN 6.9% year on year.' ... One of the two is wrong.”
- **Claimed severity** PARTIAL FAIL, nil
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** The model is calibrated to the LEVEL (int_path[0] = 1,250) and not to the change. 0.00 on both branches.
- **What it damages** A figure appearing in more than one place is not identical, on the observation that carries the study's decision not to expense the EGP 551m of capitalised interest - which the study itself prices at about EGP 551m a year of pre-tax profit if the step arrives.
- **Premise** right · **Conclusion** right
- **Evidence** Both statements verified verbatim: the delivered study text carries 'DOWN 6.1% year on year' at lines 58 and 333; the delivered bibliography carries 'DOWN 6.9% year on year' twice. WHICH IS RIGHT COULD NOT BE SETTLED HERE AND THE ROUTE WAS RUN: the comparative quarter's finance cost is registered in none of the three documents and in no input, and the Q1-2026 interim PDF held in the study directory has no text layer, so settling it needs an OCR pass off the rendered pixels. The implied comparative is 333.19 on 6.1% and 336.05 on 6.9%. Registering the comparative as a four-field input is the fix, which makes the figure computed rather than typed.

#### C26 · Three promised sensitivities are not delivered, and the largest driver has no grid at all

- **Source** forensic audit 18-09-2026
- **Location** Sensitivity sheet; study 1.9; bibliography inputs `peer pe regional`, `assoc multiple`, `assoc norm`
- **They say** “None of the three grids exists in the delivered workbook or study. ... There is no grid on the domestic price - the driver this audit finds is worth +182% of the centre.”
- **Claimed severity** PARTIAL FAIL, nil on value
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; a risk-display defect. The omitted driver is C01, measured at +178.5% / +122.6%.
- **What it damages** Disclosed ranges that were not produced, and a published risk display that omits the one input dominating it. Worse than the auditor states: the missing associate-multiple grid is the one that would have sized C11, measured here at -20.97% / -7.63% depending on the branch - so two of the three ungridded legs are exactly the two largest findings in this audit after the price path.
- **Premise** right · **Conclusion** right
- **Evidence** Confirmed from study_numbers.json: sensitivity carries grids for wacc, g, beta, prov, fx, volume and dep. There is no domestic-price grid, no peer-multiple grid and no associate grid. The bibliography's own text promises all three.

#### SA-03 · beta_ex_subject_price.json is a stale artefact read by two delivered-document builders and written by nothing - and the gate that exists for this cannot see it

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** engine/phar_study/beta_ex_subject_price.json; docx_phar.py line ~1080; docx_biblio.py
- **They say** “{'beta_ex_subject_centre_A': 65.03646729066745, 'beta_ex_subject_centre_B': 72.86208716615127}”
- **Claimed severity** not raised by the critique (it found the symptom at 08)
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; the artefact feeds a caveat table only.
- **What it damages** THIS IS THE CAUSE OF C08. docx_phar.py prints the uplift as (XBJ['beta_ex_subject_centre_A'] - LN['centre_A']). XBJ is this file, dated 31 August, carrying the SUPERSEDED edition's answers of 65.04 and 72.86. Subtracting today's 33.00 and 49.68 from them produces 32.04 and 23.18 - the two figures the auditor found wrong by roughly tenfold. No generator writes this file: a repository-wide grep finds it read by docx_phar.py and docx_biblio.py and written by nothing.
- **Premise** right · **Conclusion** right
- **Evidence** [R-ENF-06] names this species exactly - 'AN ARTEFACT EVERY BUILDER READS AND NOTHING WRITES IS A NUMBER FROZEN AT THE DATE SOMEBODY LAST TYPED IT' - and requires such a file to declare published_central and published_spot. It declares neither. AND THE GATE MISSES IT FOR A ONE-LETTER REASON: scripts/check_artefact_currency.py detects a valuation-carrying artefact by VALUE_KEYS = ('central','per_share','value_adopted','fair','end','value_per_share','weighted_central'), and this house writes CENTRE. Tested directly, carries_valuation() returns False for EVERY ONE of PHAR's nine candidate artefacts - beta_ex_subject_price.json, audit_pricing.json, audit_pricing_2.json, late_pricing.json, rebuild_ledger.json (which carries the study's own answer under start_value and value), touch_ladder.json, useful_lives.json, far_year_ranges.json and qc_result.json - so the gate reports PHAR clean having recognised nothing. That is [R-ENF-04]: an absent answer in a clean answer's clothes, and [L-355] landing on the instrument.
- **Note** The fix is in two places and only one of them is PHAR's: generate the artefact from compute.py with a published_central declaration, AND widen the shared gate's key list to the spelling this house actually uses. The second is a repository change and is reported rather than made here.

#### SA-04 · The study's own numeric-traceability check cannot match any of the typed figures that went stale - a check that could not fail on the thing that failed

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** engine/phar_study/qc_checks.py lines 150-165
- **They say** “MONEY = re.compile(r'(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?(?![\w])' r'|(?<![\w.])\d{4,}\.\d{3,}(?![\w])')”
- **Claimed severity** not raised by either reviewer
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; a gate defect.
- **What it damages** The study reports 'numeric traceability: 0 typed financial numeral(s) in builders' and passes, while docx_biblio.py carries at least seven typed financial figures that are a full edition stale and reach the delivered bibliography: 320, 5%, 78, 98, 8.1x, 6.7x, 9.8x and 133. The regex matches only comma-grouped numbers and figures with four or more integer digits AND three or more decimals. Not one of the seven can match either alternative.
- **Premise** right · **Conclusion** right
- **Evidence** Verified by reading the check and by locating the literals at docx_biblio.py lines 183, 206, 211 and 232-234. This is the SWDY-class finding the critique-response procedure says to expect from a real self-audit - a check that could never fail. Depth-bar standard 3 forbids a financial numeral in a builder; the instrument enforcing it here is blind to any figure under 1,000 without three decimals, which is most prices, most multiples and every percentage.

#### SA-05 · The lens record declares a two-sided primary and carries zero branches

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** study_numbers.json lens_record.primary
- **They say** “'primary': {'kind': 'dcf', 'two_sided': true, 'value': null, 'range': {...}}”
- **Claimed severity** not raised by the critique
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; a record-shape defect.
- **What it damages** research_protocol.assert_lens_design() refuses it in its own words: 'the primary declares two_sided and carries 0 branch(es). A two-sided answer IS its branches: without them the record states that there is no single central and never says what the two answers are, which switches the identity clause off rather than satisfying it.' The two answers do exist, in central_two_sided.branches - a different field that the lens gate does not read.
- **Premise** right · **Conclusion** right
- **Evidence** Reproduced directly: assert_lens_design(study_numbers['lens_record']) raises. scripts/check_lens_design.py reports PHAR as LENS FAIL and carries it on the ratchet, so the debt is recorded rather than hidden - but it is live and it is one line to close.

#### SA-06 · The published fair-value field's bull is the one lens the study's own record excludes

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** compute.py line 1815 fair_bear, fair_bull = min(vals), max(vals); lens_record.lenses_excluded
- **They say** “lenses_excluded: [{'kind': 'normalized_earnings', 'value': 56.78, 'why': 'not a permitted lens for any class in the registry. It is computed and published as an observation; it does not enter either centre.'}]”
- **Claimed severity** not raised by the critique (its 20 is the adjacent point)
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both centres. It sets the published bull at 56.78 against a committed envelope high of 49.68 - a 14.3% difference in what a reader is told the top of the range is.
- **What it damages** TWO ENVELOPES IN ONE MODEL. lens_record.envelope reads {low 32.9975, high 49.6789}, which is what [R-LENS-03] requires - the range of the present-value reads of the primary lens on one clock. The published field is fair_bear 32.9975 / fair_bull 56.7824, taken as the min and max across all five readings including the excluded one. The record says the lens does not enter either centre, which is true, and then it sets the top of the range a reader receives.
- **Premise** right · **Conclusion** right
- **Evidence** [R-LENS-03]: 'the bear/full envelope is the RANGE of the PRESENT-VALUE reads on one clock - never averaged into the answer, never a spread invented around it', and normalised earnings is not in LENS_REGISTRY for this class ('pharmaceutical manufacturer, generic and branded' -> ('dcf', ('ev_ebitda_own_history','relative_multiple','book_value'))). The study knows this and writes it down; the field builder does not read it.

#### SA-07 · The study carries no bridge record at all

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** study_numbers.json (absent key)
- **They say** “scripts/check_bridge.py: 'PHAR carries no bridge record'”
- **Claimed severity** not raised by the critique, which found two of its clauses empirically
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 by itself. Its two live consequences are priced at C11 and C13.
- **What it damages** [R-BRIDGE-01] exists because four bridge defects shipped inside arithmetic that recalculated perfectly, and it is enforced on a RECORD of choices - which sheet, which minority basis, cash charged how often - precisely because the number those choices produce cannot be checked by recomputing it. PHAR commits no such record, so assert_bridge() has never been run on it, and the two defects the outside auditor did find (the minority at book, the associate multiple) are two of the exact clauses that record exists to hold.
- **Premise** right · **Conclusion** right
- **Evidence** check_bridge.py run live reports PHAR as carrying no bridge record; PHAR sits on bridge_outstanding.json. The bridge itself foots - the auditor's C.4 reconciles every line to the pound - which is the point [R-BRIDGE-01] makes in its own general lesson: a model that recalculates is not a model that is right.

#### SA-08 · The study carries no cost-of-capital schedule record

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** study_numbers.json (absent key)
- **They say** “scripts/check_cost_of_capital.py: 'PHAR carries no cost-of-capital schedule record'”
- **Claimed severity** not raised by the critique
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 by itself. Its live consequence is priced at C10.
- **What it damages** [R-COC-01]'s hard refusals - country risk counted exactly once, market-value weights, a monotone ladder, the three-assert Kd gate with an independently computed effective rate over at least two periods - are enforced against a committed schedule record. PHAR commits none, so none of them has been tested from outside, and C10 is one of the things the Kd limb of that gate is built to catch.
- **Premise** right · **Conclusion** right
- **Evidence** check_cost_of_capital.py run live. The construction itself is sound and the auditor's C.1 reconciles all fourteen lines of it to zero difference except the one this row and C10 are about - which is the argument for the record rather than against it, since a sound construction with no record cannot be told from an unsound one without redoing the audit by hand.

#### SA-09 · The committed fx_path_note states a first-year figure the committed path does not carry, and describes the construction the study rejected

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** study_numbers.json fx_path_note.registered_tension
- **They say** “so the FY2026 average comes out at 56.87 while the same house path reads 50.25 on 6 August 2026”
- **Claimed severity** not raised by the critique
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches; a typed figure in a committed record.
- **What it damages** The committed fx_path first year is 55.1141, not 56.87. 56.8683 is macro_path.fx_path(5, base=50.25) - the spot-anchored construction the study BUILT AND THEN WITHDREW (rebuild-ledger lever 5). So the note describes, in the study's own committed record, the path it rejected, on the very field the largest lever in its rebuild rests on. This was found by this study's own gap review on 7 September, registered for correction in those words, and is still in the delivered edition eleven days later.
- **Premise** right · **Conclusion** right
- **Evidence** Reproduced live: macro_path.load('EG').fx_path(5) = [55.1141, 60.2223, 64.0413, 67.1652, 70.1139] on the default base of fx.average_2025 = 48.70, and fx_path(5, base=50.25) = [56.8683, ...]. The committed path is the first; the note quotes the second. 'A NUMBER STATED IN PROSE MUST BE COMPUTED, NOT TYPED' has been standing since 07-Aug-2026 and extends to the four-field register's own justification text.

#### SA-12 · The study is struck at a price that is no longer the latest known one

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** study_numbers.json spot 127.3 / spot_date 2026-09-03
- **They say** “scripts/check_valuation_gap.py: 'PHAR: struck at 127.30, latest known 128.00 (2026-09-06)'”
- **Claimed severity** the critique raises the staleness differently, at its 04
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on the valuation. On the GAP it is 0.55%: -74.07% against the strike becomes -74.22% against 128.00.
- **What it damages** [R-GAP-01 AMENDED] requires the central to be put against the LATEST KNOWN price before any delivery and the study's own spot to be that price with its date beside it. Small here, and the rule is the rule.
- **Premise** right · **Conclusion** right
- **Evidence** Read live from engine/prices via the gap gate. The auditor's separate point - that the share rose 24.75% in August and closed the month at 129.74 - is the reason this matters more on this name than on most.

#### SA-13 · The live site publishes a fair value this house no longer holds, and the sign of the disagreement is the same but its size is not

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** assets/data.js TICKERS.PHAR.fair
- **They say** “fair: {bear: 58.04, base: 61.21, full: 73.03}, spot: 128, spotDate: 'close 06 Sep 2026'”
- **Claimed severity** not raised by the critique, which had no repository access
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on the study. The reader-facing gap is -52.2% on the published base against the -74.1% the study holds.
- **What it damages** A reader on the site is told the fair value is EGP 61.21 while this house holds 33.00 and 49.68 - the 09-Aug edition's numbers, frozen because [R-GAP-02] holds the study from publishing while every branch sits more than 10% below the price. So the block is keeping the AUDITED number away from the reader and leaving the UNAUDITED one on the page, which is [R-GAP-03]'s own finding arriving on this name.
- **Premise** right · **Conclusion** right
- **Evidence** Read through a real JavaScript parse of assets/data.js [R-ENF-03]. This is a recorded, ratcheted debt rather than a new defect, and it is named here because it is the number a reader actually receives and because any decision taken on this response changes it.

#### SA-15 · The instrument that would have caught the Appendix A.1 defect was never run on this study

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** scripts/check_waterfall_assertions.py ratchet
- **They say** “PHAR  NO IMPORT (ratchet)  EIPICO_Valuation_Study_09-08-2026.docx  4 waterfall table(s); first says 'Less depreciation and amortisation'”
- **Claimed severity** not raised by the critique, which found the defect itself at its 06
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches.
- **What it damages** The study delivers four instructing tables and calls engine/table_residual.waterfall() on none of them. The gate records this as a ratcheted debt, correctly, and the debt then cost exactly what the rule predicted: an outside auditor found by hand the defect the instrument exists to find at build time.
- **Premise** right · **Conclusion** right
- **Evidence** check_waterfall_assertions.py run live. The study's own footing_check.py examines 42 tables and reports zero unreconciled totals - which is right and beside the point, because Table 20 is a WATERFALL whose rows are named in words and whose label declares no total, so the label test never fires. That is the distinction [R-ENF-01 EXTENDED 04-Sep-2026] was adopted on.

#### SA-16 · The study never states that the Egyptian Exchange's trading week runs Sunday to Thursday, which is what makes its own check date reproducible

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** Study Table 14
- **They say** “Check date | 2026-09-06 | 2026-11-08”
- **Claimed severity** logged as the adjacent defect behind the critique's 25, which is rejected
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both branches.
- **What it damages** The study says the check date is 'a calendar date, resolved to the exchange's first real trading session' and stops there. A reader assuming a Monday-to-Friday week cannot reproduce 8 November from 6 August and concludes the rule does not produce the date - which is exactly what the outside auditor concluded, in good faith, and it is the only finding in twenty-seven where they were simply wrong about the world rather than about the document.
- **Premise** right · **Conclusion** right
- **Evidence** The rejection at C25 is on a live run of engine/horizons.resolve, which returns grade_date 2026-11-08 because the calendar target 2026-11-06 is a Friday. One clause naming the exchange's week would have made the finding impossible. Per the procedure's step 4: for every rejection, ask what a careful reader had to misread to land there, and whether that thing is unclear. It was unclear.

### `accept-defect-reject-fix` — 2 rows

#### C02 · The terminal value is not built on the construction the study declares

- **Source** forensic audit 18-09-2026
- **Location** DCF!B18:B29; study 1.1; Table 18; workbook lens note
- **They say** “The sheet does not use the reinvestment identity ... The terminal cash flow is built instead from four typed constants ... producing a reinvestment rate of 40.9%, not 55.0%. ... Correct method: Either implement the identity the study declares - terminal FCF = NOPAT x (1 - g/ROIC).”
- **Claimed severity** TOTAL FAIL, -27% to -34%
- **Price** Frame A **-11.0775** (**-33.57%**) · Frame B **-11.4197** (**-22.99%**)
- **How it was priced** The study already COMMITS the retired construction's terminal: dcf.frame_A.tv_retired = 14,272.89 against the live tv 18,664.92. Bridging it at the study's own year-five factor 0.42561: EV core 8,076.6, EV total 11,067.5, equity 3,699.2, per share 21.92. Frame B: tv_retired 19,354.18 -> pv 8,237.40, EV core 10,833.94, per share 38.2592 (-22.99%). The auditor reports 21.77 on the same construction; the 0.15 difference is discount-factor rounding.
- **What it damages** The delivered study states a terminal reinvestment of 55.0% while its terminal reinvests 40.90% (1 - 1,400.507/2,369.674). The 55.0% is g/ROIC - the RETIRED identity's answer - computed and printed beside a terminal that does not apply it. The workbook's own lens note calls the construction 'a terminal value on the growth-over-return reinvestment identity'.
- **Premise** right · **Conclusion** wrong
- **Evidence** [R-TERM-01] RETIRED the g/ROIC reinvestment identity outright: it charges g x IC every year for ever, so the implied replacement cycle is 1/g - a fact about the growth rate and not about the asset. compute.py line 1487 labels it in its own words: 'THE RETIRED FORM, kept in one line so the change is legible and priced.' The live terminal is engine/terminal_value.py build(), the only sanctioned route, on the DISCLOSED 13.8-year weighted life from the FY2024 audited note 3.1 weighted by note 4.1 gross cost. The auditor's own reconciliation table C.3 concedes both halves: 'Life implied by the terminal maintenance line 13.80 yrs - matches disclosure', and 'The second is the better construction; it is simply not the one on the page.' Implementing their fix would reinstate a defect this house retired on measured evidence.
- **Note** WHAT WILL BE DONE INSTEAD: the prose is corrected to describe the maintenance-capex terminal that is actually run, and the printed terminal reinvestment is changed from the identity's 55.0% to the model's own 40.90%. The model does not move.

#### C27 · The 2022 leg of the multiple history uses a year-end count under a rule that says weighted average, with no corporate-action check

- **Source** forensic audit 18-09-2026
- **Location** Relative & Normalized!C17; Assumptions!C4; study 1.3
- **They say** “the count rose from 99.17m to 148.76m during 2023 - if that increase was a bonus or stock-dividend issue, the 2022 close of EGP 28.08 requires adjustment and the 4.74x leg is overstated by up to a third; if it was a cash rights issue at market, no adjustment is due.”
- **Claimed severity** UNVERIFIABLE, up to -0.4x on the four-year mean
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** 0.00 on both centres. On the relative cross-check lens, applying the theoretical ex-rights adjustment takes the 2022 leg from 4.744x to 3.726x, the four-year mean from 6.5722x to 6.3177x, and the lens from 48.6499 to 47.9251 (-0.72).
- **What it damages** Two separate defects, and the auditor found the smaller one. FIRST, the stated rule is contradicted by the study's own register: 1.3 says each year divides profit by 'that year's own weighted-average share count' while the input register's own note says 'the share count in issue at each year end' - and THREE of the four legs use year-end counts, not one. Only FY2025 uses a weighted average.
- **Premise** wrong · **Conclusion** right by accident
- **Evidence** RESOLVED FROM THE PRIMARY SOURCE THE AUDITOR COULD NOT REACH. The FY2023 audited consolidated statements held in this study directory carry the capital note in its own words: 'In accordance with the decision of the company's general assembly held on 1/4/2023, it was approved to increase the capital from 991,705,000 to 1,487,557,500 With an increase of 495,852,500 pounds, FINANCED FROM THE CASH PAYMENT FROM SHAREHOLDERS by 50% From the issued and paid-up capital before the increase.' It was CASH, not a bonus issue - and the same note distinguishes the two mechanisms in its own words one paragraph earlier, describing the 2018 increase as 'the distribution of a FREE SHARE for every four original shares to be financed from the investment projects financing reserve'. So the auditor's bonus hypothesis is false and their 'up to a third' overstatement does not arise. BUT AN ADJUSTMENT IS STILL OWED AND FOR A DIFFERENT REASON: no share premium appears anywhere in the FY2023 filing, so the rights issue was at the EGP 10 par value while the 2022 close was 28.08 - a rights issue at par carries a bonus ELEMENT. The theoretical ex-rights price is (2 x 28.08 + 10)/3 = 22.053, a factor of 0.7854.
- **Note** WHAT WILL BE DONE INSTEAD OF THE PROPOSED FIX: not a bonus restatement, but (a) the theoretical ex-rights adjustment of 0.7854 applied to pre-2023 closes, worth -0.72 on the relative cross-check lens and nil on both centres, and (b) the larger half the auditor did not see - 1.3's weighted-average claim corrected to what three of the four legs actually do, or the legs rebuilt on weighted averages.

### `reject-with-receipts` — 1 rows

#### C25 · The three-month check date is 94 days after the anchor

- **Source** forensic audit 18-09-2026
- **Location** Study Table 14; Monte Carlo!C4
- **They say** “Three calendar months is 2026-11-06 (a Friday); the date used is +94 days. The stated resolution rule does not produce it. ... Impact: Negligible - roughly 1% on the band width.”
- **Claimed severity** PARTIAL FAIL, negligible
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** Nothing is wrong, so there is nothing to price. 0.00 on both branches and 0.00 on the band.
- **What it damages** None. The premise is false.
- **Premise** wrong · **Conclusion** wrong
- **Evidence** RECEIPT, RUN LIVE: engine/horizons.resolve('EG','2026-08-06',3) returns target_date '2026-11-06' and grade_date '2026-11-08'. The published date is exactly what the stated rule produces. The reason is that 6 November 2026 is a FRIDAY and the Egyptian Exchange trades Sunday to Thursday, so the calendar target rolls forward to the exchange's first real trading session, Sunday 8 November - which is the rule the study states in those words. The same module returns 2026-09-06 for the one-month horizon, also a Sunday, which the auditor accepts as correct at +31 days without noticing it is the same roll-forward. The cone was sized on h=62 projected sessions, which is the honest count.
- **Note** WHAT A CAREFUL READER HAD TO MISREAD TO LAND HERE, AND IT IS A REAL GAP OF OURS: the study says the check date is 'a calendar date, resolved to the exchange's first real trading session' and nowhere says that the Egyptian Exchange's week runs Sunday to Thursday. A reader assuming a Monday-to-Friday week reads 8 November as unexplained. Logged as SA-16.

### `user-decision` — 3 rows

#### SA-01 · The currency path's FY2026 average sits above the pound's own 52-week high, and the tension the rebuild ledger registered is still unresolved

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** engine/macro_paths/EG.json fx; study_numbers.json fx_path and fx_path_note; rebuild_ledger.json lever 5
- **They say** “registered_tension: 'The derivation compounds a full year of purchasing-power depreciation onto a quote taken EIGHT MONTHS INTO that year ... The study CONFORMS rather than inventing an anchor, and this is registered as a property of the house path's first year.'”
- **Claimed severity** not raised by the critique
- **Price** Frame A **+11.3493** (**+34.39%**) · Frame B **+10.8674** (**+21.88%**)
- **How it was priced** compute.py patch _HOUSE_FX = [50.5, 55.1805, 58.6798, 61.5422, 64.2441] - the FY2026 average held near the observed level and relative purchasing-power parity run forward from there on the same house ladder: A 44.3468 (+34.39%), B 60.5463 (+21.88%). Two bounding runs for the shape: the note's own base=50.25 construction gives A 28.6827 (-13.08%); a flat 50.25 throughout gives A 68.3287 (+107.07%), which is a bound and not a forecast.
- **What it damages** This is the largest single item in the study after the price path, it is registered in the study's own rebuild ledger as worth -25.4% when it was applied, and no instrument has re-priced it since.
- **Premise** right · **Conclusion** right
- **Evidence** THE RECEIPT IS INSIDE THE HOUSE PATH'S OWN SOURCE FIELD. engine/macro_paths/EG.json records fx.spot 50.25 at 6 August 2026 and, in the same sentence, 'its 52-week range is 46.64-54.86'. The committed FY2026 average of 55.1141 is ABOVE THE TOP OF THAT ENTIRE RANGE. Arithmetically: with the pound at 49.52 at end-2025 and 50.25 in August, the first eight months of 2026 average roughly 49.9, so a calendar-2026 average of 55.11 requires the pound to average about 65.5 from September to December - a 30% devaluation in four months. THE DIRECTION IS NOT NEUTRAL FOR THIS NAME AND IS MEASURED: dollar-linked COST runs 40.0-42.2% of revenue across the window while dollar-linked REVENUE runs 32.8-34.1%, so the company is net short dollars by 7-8 points of revenue on an EBIT margin near 19% - which is why a currency correction moves the answer by a third. The study itself is NOT at fault: [R-MACRO-01] forbids a study carrying a currency number of its own, the path is derived by relative purchasing-power parity, and rebuild-ledger lever 5 records that a first draft anchored on the observed spot and was withdrawn for exactly that reason. THE DEFECT IS IN THE PATH, NOT IN THE STUDY.
- **Note** RECOMMENDATION: escalate to the pass that owns engine/macro_paths/EG.json rather than patching PHAR, because the path is shared by every Egyptian study and the correction runs in OPPOSITE directions across them - a stronger pound raises PHAR (net short dollars) and lowers AMOC (dollar-linked revenue), which is the strongest available evidence that it is a repair rather than a lean. [R-REBUILD-01 CLAUSE TWO] CHECK, WHICH THE BRIEF ASKED FOR: lever 5's stated reason is '[R-MACRO-01] does not admit a leading-year anchor for a currency', which is a TRUE reason and cites the rule that actually governs - it is NOT the promotion-guard misreading that clause was adopted to close, and scripts/check_deferral_reason.py confirms zero records anywhere in this study give the guard as a reason. The ledger carries the measurement (-25.4%), which is what the clause requires of a deferral.

#### C11 · The associate stake is carried at a Gulf multiple without the cost-of-equity adjustment the study applies one page earlier

- **Source** forensic audit 18-09-2026
- **Location** Assumptions!C64 = 11.0; SOTP Bridge!B5; study Table 5
- **They say** “The study adjusts the peer P/E from 21.35x to 6.47x precisely because those companies face a ~10% cost of equity rather than this one's 16.9% ... The associate multiple is the same kind of number and receives no such adjustment. ... Impact: -21% of the Frame A centre.”
- **Claimed severity** PARTIAL FAIL (material), -21%
- **Price** Frame A **-6.9198** (**-20.97%**) · Frame B **-6.9198** (**-13.93%**)
- **How it was priced** TWO BRANCHES, BOTH RE-RUN. (a) assoc_multiple=I(11.0 -> 6.3290), the study's own cost-of-equity-consistent multiple: A 26.0777 (-20.97%), B 42.7591 (-13.93%). (b) assoc_multiple=I(11.0 -> 9.3), the one observable listed comparable in the portfolio: A 30.4790 (-7.63%), B 47.1604 (-5.07%).
- **What it damages** Two constructions for one problem inside one document. The study also never discloses on its own page that one associate is listed, nor its observable multiple; a listed associate carried above its own market price owes that disclosure.
- **Premise** right · **Conclusion** partly right
- **Evidence** The inconsistency is real and is the study's own: its input register states the 9.3x observable in its own words ('the one associate in the group that is itself listed trades on roughly 9.3 times trailing earnings, so 11 times is above the only observable comparable in the portfolio'), so the study knew the number and carried above it. BUT THE AUDITOR'S FIX IS NOT AUTOMATIC. The larger holding is a 30% interest in a SAUDI manufacturer whose cash flows are in riyal against a pegged dollar, not in pounds - applying an Egyptian cost of equity to a Saudi earnings stream is the mirror of the error being corrected. The auditor's own 'correct method' concedes this: 'or carry the Saudi holding at a Gulf multiple and the Egyptian holdings at an Egyptian one, and say which is which.' That split needs a disclosure the company does not publish - no standalone associate accounts are issued through this company, a negative search this study has run three times.
- **Note** RECOMMENDATION: adopt the observable 9.3x (branch b, -7.63% / -5.07%) rather than the constructed 6.33x. It is an OBSERVED price for an asset in the same portfolio, which is evidence, where 6.33x is a construction applying a pound cost of equity to a riyal earnings stream. Whichever is taken, the split between the Saudi and Egyptian holdings must be stated.

#### SA-11 · LATEST FILINGS is still not cleared, and the one search that would settle it was not among those run

- **Source** self-audit 18-09-2026 (run before the critique was read in detail)
- **Location** GAP_REVIEW_07-09-2026.md heading 1; external_news_17-09-2026/ADJUDICATION; sweep_register.json study_quarters_disclosed
- **They say** “The most recent period the model consumes is still Q1-2026, reviewed. ... It remains true that if an H1-2026 was lodged with the exchange, the bridge stands on a superseded balance sheet. NOT cleared, and it cannot be cleared from here.”
- **Claimed severity** not raised by the critique, which had no primary-source access and said so
- **Price** Frame A **+0.0000** (**+0.00%**) · Frame B **+0.0000** (**+0.00%**)
- **How it was priced** Unpriceable without the document. Direction is stated rather than guessed: a newer balance sheet moves the bridge's net debt and a newer income statement moves the anchor, and on a company whose Q1-2026 gross margin ran 3.3 points below its comparative quarter, the sign is not predictable from here.
- **What it damages** The bridge stands on the 31 December 2025 audited balance sheet for net debt and a 31 March 2026 figure for the minority - a mixed perimeter the study discloses and prices at about EGP 3.04 a share. If a 30 June 2026 reviewed interim exists, both are superseded, and that is the exact defect [R-BRIDGE-01] clause (i) was adopted on after PHDC and AMOC shipped it.
- **Premise** right · **Conclusion** right
- **Evidence** ROUTES RE-RUN LIVE TODAY RATHER THAN CARRIED [R-IND-01]. eipico.com.eg returns HTTP 200; its Investor Relations section was fetched and parsed today and carries EXACTLY ONE document class - Annual Reports, seven PDFs FY2019-FY2025 - with no interim, quarterly or results document of any year. egx.com.eg does not resolve from here. So far this reproduces the gap review. WHAT IT MISSED, AND IT IS IN THIS STUDY'S OWN SWEEP REGISTER: the reviewed Q1-2026 interim that the whole anchor and bridge stand on DID NOT COME FROM THE WEBSITE EITHER. The register's fourth primary-access row reads 'company-supplied issued financial statements', dated 2026-08-11: 'The reviewed FY2026 first-quarter interim ... supplied directly after the first issue of this study. This CLOSES the study-year quarter that could not be reached online.' The same register records the exchange portal returning a bot-defence challenge and the regulator sub-domain refused at the proxy. THEREFORE INTERIMS EXIST FOR THIS COMPANY, THEY ARE NOT PUBLISHED ON ITS OWN SITE, AND THE ONLY ROUTE THAT HAS EVER OBTAINED ONE IS ASKING THE PRINCIPAL - used successfully once, and not used for the half-year. The gap review's conclusion that the absence is 'a property of EIPICO's own disclosure rather than a document this desk failed to open' is true of the WEBSITE and does not follow, because the document the study does hold did not come from the website. The reasoning is pointed at the wrong channel. Separately, the 17 September external-news pass ran two independent engines over price determinations, registrations, contracts, management changes, litigation, covenants, plant outages and company-issued updates to eleven named drivers - and HAS A HALF-YEAR STATEMENT BEEN LODGED is on none of those lists. A negative search is only evidence about what it searched for.
- **Note** RECOMMENDATION, AND IT IS ONE LINE: ask the principal for the reviewed 30-June-2026 interim, or for confirmation that none was issued - the same route that supplied the Q1-2026 interim on 11 August. This is the shape [R-IND-01] sanctions: the ladder is climbed and exhausted (IR page fetched live today, exchange bot-defended, regulator refused at the proxy), the figure is one only the principal can supply, and the work routes around it rather than stopping on it. DEFAULT IF NO ANSWER ARRIVES: the study continues on Q1-2026 and its gap review states that the half-year was ASKED FOR and not obtained - a different and more honest sentence than the one it carries now. THIS ROW IS NOT PARKED: what could be tested from here was tested today and it changed the finding.

---

*Phase 1 under `engine/Critique_Response_Prompt.md` v2. Assessed, priced and reported; nothing implemented, no fair value moved, no delivered file touched. Every price in this register was produced by re-running this study's own `compute.py` in a sandbox copy and reading the central back.*
