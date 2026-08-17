# EMPOWER — critique response, 17-Aug-2026

Four external audits of the 9-Aug-2026 study (ADX-beta edition: DCF 2.182/2.027, central
1.901/1.807): CW = "Claude cowork" forensic audit (41 rows), CC = "Claude code" forensic
audit (25 rows), GT = "Gemini think" adversarial memo (7 findings), GR = "Gemini research"
audit (4 findings). **Reconciliation: 77 raised, 77 answered, 0 unaddressed.**
Prices are AED/share against the pre-revision weighted central 1.901 unless stated.
Verdicts: ACCEPT-IMPL (accepted and implemented), ACCEPT-TEXT (text/disclosure fix),
ACCEPT-DEFECT/REJECT-FIX, REJECT (with receipt), RESOLVED (unverifiable → evidence supplied),
DECISION (client's call, priced). Facts marked [F] are verified in critique_facts.json;
computations marked [C] were re-derived independently this session and matched.

## Self-audit (written before reading the critiques)
Thirteen findings: SA1 terminal ROIC 23% perpetuity (−0.19 if 12%); SA2 asymmetric
escalation; SA3 concession-receivable incoherence (+0.02-0.05); SA4 NWC-scales-with-revenue
(−0.02-0.04); SA5 beta CI dominates (±0.45); SA6 capex/RT single-year base (+0.04);
SA7 half-year shock read; SA8 relative-lens war double-count (+0.006); SA9 DDM policy horizon;
SA10 g at top of range (−0.08 at g−50bp); SA11 ERP edition (−0.10); SA12 anchor staleness;
SA13 index-series provenance. The critics caught SA3, SA4, SA5, SA7, SA10, SA12 (harder:
they found the six-month double-count inside it), SA13, and half of SA1 (via g/tariff);
they missed SA2, SA6, SA9, SA11 and the ROIC-level half of SA1 — SA6 and SA11 remain open
as house items. SA8 they inverted with better facts: the multiple I used predated the
peer's own selloff, so that lens was stale-flattered, not war-depressed, at the level used.
They found ~20 real defects my self-audit missed. A self-audit that found nothing would
have failed; this one found 13 and still missed the ceasefire staleness — recorded.

## CW — "Claude cowork" forensic audit (41 rows)

| # | Their finding (their words) | Premise / conclusion | Price | Verdict + receipt |
|---|---|---|---|---|
| CW1 | "The 8 Apr 2026 truce did not hold… Trump publicly declared the ceasefire 'OVER' on 8 July — 32 days before the study date" | Premise TRUE [F]: Fujairah struck 4-May; Hormuz closed from 11-Jul and closed at the anchor; ADNOC tanker hit 8-Aug. Conclusion (bear is the live case) is a weighting judgement | Bear−central gap 0.34-0.40 (18-21%) is the exposure; no mechanical reprice | ACCEPT-IMPL (macro rewrite: base relabelled "de-escalation case", condition stated as NOT holding at the anchor; 17-Aug postscript; catalysts re-pointed). Field kept — re-weighting left to the reader, stated plainly |
| CW2 | "Three of four columns are wrong by ~AED 1.3bn… the report printed the current portion only" | Premise TRUE [C]: builder dict-merge let the current portion (≈21) overwrite the full figure; their "column-shifted" sub-diagnosis wrong (1,305 IS FY2024's non-current) | Nil on value (workbook was right); A.2 does not foot | ACCEPT-IMPL (A.2 sums current+non-current in all columns); sub-diagnosis corrected in this note |
| CW3 | "1.901 < 1.920 and 1.807 < 1.920 — both sit below" the 95th percentile, contradicting the study's own table | Premise TRUE [C]: the relationship was hardcoded prose from the pre-ADX edition (2.250/2.139 > 1.92) and went stale when the centrals fell | Nil on value; kills the §6 divergence claim as written | ACCEPT-IMPL (comparison now computed from the numbers, never asserted) |
| CW4 | "Dxb CoolCo FZCO … 85% 85%" vs the study's "70%-owned" | Premise TRUE (H1-2026 subsidiary note, read directly) | Nil (NCI charged at disclosed profit share) | ACCEPT-TEXT (85%/15% everywhere) |
| CW5 | "Final approval rests with the DSCE… the cited regulator does not hold the power ascribed to it" | Premise TRUE [F]: RD10 — RSB assesses/recommends, Supreme Council of Energy approves | Nil; monitoring misdirected | ACCEPT-TEXT (approval chain fixed; §5 watch-item re-pointed) |
| CW6 | "RD10 v1.3 (17 Sep 2025)… 'indexation or escalation of Capacity Charges will not be approved'; ECR 87/2025… AED 1.55 per RT; RD10 v1.4" | Premise TRUE [F] — a genuine sourcing failure inside the claimed sweep window | Fee ~2.7m/yr ≈ 0.005/share (0.3%); anti-indexation clause: forecloses tariff-escalation upside and hardens the flat-tariff base | ACCEPT-IMPL (instruments added to sweep + register + §1.8/§7; g re-justified volume-only; fee disclosed with its number) |
| CW7 | "Only one tranche was refinanced… one RCF maturing September 2027 and one maturing February 2028" | Premise TRUE (H1-2026 borrowings note read directly: Sep-2027 tranche still outstanding) | Kd roll risk on half the book; ~+25bp on blended Kd ≈ −0.7% on DCF if repriced | ACCEPT-IMPL (claim fixed; Sep-2027 roll added as Kd sensitivity). GR's contrary clearance merely restated the study — arbitrated on the primary note |
| CW8 | "Weights should carry the debt actually financed at Kd. Gross debt → wd 26.84%, WACC 7.2292%, fair value 2.3797" | Premise (construction unpriced) TRUE; conclusion (gross is THE correct frame) contested — GT derives the opposite sign from the same observation | +0.198 DCF / +4.5% central [C, reproduced exactly] | ACCEPT-DEFECT/REJECT-FIX: all three constructions now priced in the deliverables (gross 7.23% → 2.507 on the revised base; carry 7.79% → 2.227). Base stays target-net: company net-debt policy ~2x EBITDA and payout ≈ FCFE make surplus cash transient — receipts in §1.8 |
| CW9 | "Using β 0.652 → fair value 2.6643… resolved on a non-methodological basis" | Premise TRUE (the choice was an explicit client instruction, disclosed as such); the +22.1% spread real [C] | +0.482 DCF / +11% central | DECISION (client's): ADX basis retained per instruction, now PRICED in full — DFM-beta parallel valuation (2.792 on the revised base) in §1.8, sensitivity and workbook, not a parenthetical |
| CW10 | "Interest is capitalised as an operating perpetuity while the capital producing it is written out… ~22% has nothing to do with the airport" | Premise TRUE [C + Note 8 read: 1,005.0 DACC + 289.4 Nakheel] — matches self-audit SA3 | +0.086 DCF / +3.9% [C, reproduced exactly] | ACCEPT-IMPL (clean treatment: interest out of operating EBITDA/FCFF, asset at book 1,294.4 in the bridge, out of terminal IC; renamed "related-party acquisition receivables") |
| CW11 | "UAE nominal GDP runs ~4.5-6.0%. 2.5% is not a GDP-consistent figure… the published grid stops at 1.5%" | Premise TRUE [F: IMF CAGR ≈5.7%]; label wrong (in the conservative direction); flat-tariff volume-only tension real | −0.115 at g=1.5% / −0.25 at g=0 on the DCF (−6%/−12% central) | ACCEPT-IMPL (label dropped; volume-only justification vs RD10; grid extended to 0%). g=2.5% retained as base — DECISION row for the client if they prefer 2.0% (−0.07 on central) |
| CW12 | "Leaves the book lens untouched at 1.630. Under 15% tax… the lens [is] 1.5127. Internally consistent 15% central = 1.7891" | Premise TRUE [C: 1.5127 reproduced] | −0.018 on the 15% central (−1.0%) | ACCEPT-IMPL (book and normalised lenses now re-taxed under the 15% framing) |
| CW13 | "A Pillar-Two top-up… does not generally increase the marginal value of interest deductibility" | Premise TRUE (minimum-ETR mechanics) | −0.021 on the 15% column (−1.0%) | ACCEPT-IMPL (15% framing keeps the 9% shield; both framings discount at 7.61%) |
| CW14 | "The crux grid alone is the outlier… the signature of a straight-line interpolation" | Premise (cells not full re-runs) TRUE [C: true re-runs match their figures to 6dp]; mechanism sub-diagnosis wrong — CC identified it: terminal IC frozen at base | ±0.004 per cell; crux cost 2.85% vs 2.7% published | ACCEPT-IMPL (crux and persist runs now carry their own scenario NWC/PPE into the terminal) |
| CW15 | "The pasted 2.2208 reproduces exactly on connections of 110/110/100/90/80 — not a flat 110k" | Premise TRUE [C: that is literally the coded path] | +0.038 if the description were implemented | ACCEPT-TEXT (description now states the actual path) |
| CW16 | "Tabreed traded AED 2.46 on 6 Aug (−11%)… rolled to the anchor, the relative lens gives 1.4178" | Premise TRUE [F: 2.46 on 6 and 7 Aug; decline −9.6% not −11%] | −0.118 lens / −0.024 central | ACCEPT-IMPL (peers restruck at the anchor: 10.1x / 15.0x) |
| CW17 | "The (1+g) factor converts leading to trailing and should not be present" | Premise TRUE | −0.042 lens / −0.006 central [C: 1.6816 reproduced] | ACCEPT-IMPL (forward justified P/E) |
| CW18 | "Gross debt is held flat; net debt is the plug and falls sharply… the text asserts the opposite of what the model does" | Premise TRUE | Nil on DCF; static-weight WACC tension noted | ACCEPT-TEXT + the target-structure receipt added to §1.8 (the falling path is why target-net, not gross, anchors the weights) |
| CW19 | "It references the static 30-Jun-2026 cash… a hardcoded input mid-chain" | Premise TRUE | Nil on DCF; distorts forecast EPS/cover | ACCEPT-IMPL (finance line linked to the rolling balance) |
| CW20 | "The shock year's margin rises, and it is already inside the audited range" | Premise TRUE [C: FY26 48.6% is the highest forecast year] | Nil | ACCEPT-TEXT (narrative now says the margin rises in the shock year — pass-through — and dips in FY2027) |
| CW21 | "The observed maximum is 49.3%, not 50.5%" | Premise FALSE on the study's stated basis: audited FY2021 derivation (op 933.476 + D&A ≈311.6 on rev 2,463.9) = 50.5% [C]. Their 48.9% is the company's own differently-defined figure | Nil | REJECT with receipt; basis note added so the two definitions can't be confused |
| CW22 | "The study… reports only the revenue lines that support the damage narrative" | Premise TRUE (H1 PBT +16.2%, NP +16.2%, EBITDA +7.5% absent); conclusion inverted — the omitted lines SUPPORT the study's crux | Nil (build conservative vs H1 run-rate) | ACCEPT-TEXT (profit lines added; implied H2 disclosed) |
| CW23 | "Full-year FY2026 FCFF discounted at 0.9293 against a bridge struck on the 30-Jun-2026 balance sheet… the Jan-Jun window is never addressed" | Premise TRUE — the six-month double-count my own "no accretion roll" note walked past | +0.048 DCF (stub fix) [C] | ACCEPT-IMPL (30-Jun stub clock: FY26 half-flow at t=0.5, years at 1.5-4.5, TV at 4.5) |
| CW24 | "The Word study asserts a calibration standard its own companion workbook disclaims" | Premise TRUE (the panel evidence is not in the reader's packet; n=10 has no test power) | Nil | ACCEPT-TEXT (§3 language downgraded to the workbook's own wording; over-width stated as the evidence it is) |
| CW25 | "The two are ~7pp apart and never reconciled" (KAM 56.3% vs deck 49%) | Premise TRUE | Nil on the point estimate; material to the shock's size | ACCEPT-TEXT (reconciliation sentence; pass-through ratio's KAM basis stated) |
| CW26 | "A T-Sukuk maturing 19 February 2033… ~6.5 years… And 30-Jul-2026 → 29-Jan-2031 is 4.50 years, not 4.4" | Premise TRUE [F: sukuk exists, AED 1,650m; last print 4.13% Apr-2026; 4.4 was bid-to-cover] | If re-anchored at a stale 4.13%: +~0.1 — rejected as basis | ACCEPT-TEXT ("longest print" → "most recent print"; tenor 4.50y; the 2033 sukuk named with why its April yield is not the anchor in a repriced market) |
| CW27 | "3.66% is the 31 March fixing… ~29bp higher" | Premise TRUE [F: 3.94-3.96% mid-Aug; first-Aug-week unretrievable, one 3.85% print 12-Aug] | Nil on DCF (Kd is the capitalisation rate) | ACCEPT-TEXT (EIBOR restated ~3.9% Aug; the "no glide" argument softened accordingly) |
| CW28 | "The H1-2026 results release… all dated 6 August 2026" | Premise PARTLY TRUE [F: statements stamped 5-Aug; release/coverage 6-Aug]; the fall ran 4→7 Aug | Nil | ACCEPT-TEXT ("released 5-6 August"; price path stated by day) |
| CW29 | "1,918 + 1,568 = 3,486, 17 short" | Premise TRUE (pipes line) | Nil | ACCEPT-TEXT (pipes row added; labels foot) |
| CW30 | "The 80% figure traces to Empower's 2022 Integrated Report" | Premise TRUE (no later restatement found) | Nil | ACCEPT-TEXT (date-stamped as IPO-era disclosure) |
| CW31 | "Tabreed's reported FY2025 revenue is AED 2,456m… DEWA['s] 5.0% upper bound… not supported" | Premise TRUE | Nil (cross-check inputs) | ACCEPT-TEXT (reported figures; earnings basis stated) |
| CW32 | "A point estimate plus a stated percentage upside plus a directional conclusion is rating-equivalent in substance" | Premise partly true (house rule: ranges/distributions only); a weighted central is house practice in every study | Nil | ACCEPT-TEXT in part: centrals to 2dp, field labelled scenario range, construction range stated beside it; the no-target statement de-absolutised. Central retained (house convention, disclosed weights) |
| CW33 | Damodaran CDS-basis inputs UNVERIFIABLE | Their own coherence test passes (1.5545 scalar both bases) | — | RESOLVED: the July-2026 workbook (ctrypremJuly26.xlsx) was downloaded this session; UAE row 0.393%/4.811%, Abu Dhabi CDS 0.52%/5.008% read directly — file cited by name in the bibliography |
| CW34 | FY2025 KAM consumption + DEWA purchases UNVERIFIABLE (no text layer) | Correct about the scan | — | RESOLVED: the FY2025 filing was OCR-read this session (gate-logged); KAM 1,923.892 and Note 12 1,467.650 are OCR extractions cross-footed to audited totals; stated in the bibliography |
| CW35 | Capitalisation rates 4.92%/5.993% UNVERIFIABLE | Correct about the scan; their deck triangulation (4.5-5.0%) consistent | — | RESOLVED: OCR of FY2025 note 30 (same method, same cross-foots); label fixed per CC15 |
| CW36 | Technical figures UNVERIFIABLE; "internal coherence passes" | Their coherence checks all pass | — | RESOLVED: computed from the supplied exchange series committed in the repo (EMPOWER_Stock_Price_History.csv); series available on request |
| CW37 | Simulation engine and panel UNVERIFIABLE; drift reproduces exactly | Their drift check passes | — | RESOLVED in part: engine and panel live in the public repository; §3 language downgraded (CW24) rather than an appendix added (house rule: no calibration appendix in the deliverable) |
| CW38 | Beta regression UNVERIFIABLE; "an R² of 0.103 against a foreign-exchange index… is a weak regression carrying a 22% swing" | Arithmetic verified by them; weakness real and now priced | ±0.45 on the primary lens across the CI | RESOLVED + ACCEPT-IMPL (both index bases priced; CI carried into the stated uncertainty; series in repo) |
| CW39 | 35-year concession term UNVERIFIABLE | Correct — no reachable filing states the term | — | ACCEPT-TEXT (claim now sourced to the acquisition-period disclosure or dropped to "long-term concession"; flagged in bibliography) |
| CW40 | DFM drawdown basis UNVERIFIABLE (−21.9%) | Their reconstruction consistent (−22.9% intraday) | Nil | ACCEPT-TEXT (basis and dates stated: closing-basis peak 6,774.38 9-Feb → trough 5,288.70 16-Mar) |
| CW41 | "The companion bibliography… was not provided" | True — outside their packet | — | RESOLVED: it exists and ships with the study (9pp PDF); several UNVERIFIABLEs above resolve against it |

## CC — "Claude code" forensic audit (25 rows)

| # | Their finding (their words) | Verdict | Price | Disposition |
|---|---|---|---|---|
| CC1 | "The largest single value driver in the document is disclosed in one parenthetical and never priced" (beta index) | Premise TRUE | +0.482 DCF | Same as CW9: DECISION (client instruction) — now priced in full as a parallel construction |
| CC2 | WACC net-debt weights "disclosed but never sensitised" | Premise TRUE | +0.198 DCF | Same as CW8: constructions table added; base defended with receipts |
| CC3 | "2.5% nominal growth IS 2.5% perpetual real volume growth: 2,101k RT compounds to 3,443k in 20 years… against a total contracted book of 2,018k" | Premise TRUE (arithmetic verified) | −6% to −12% central at g 1.5-0% | Same as CW11: relabelled, volume-justified, grid to 0% |
| CC4 | "H1-2026's AED 200.4mn of net-debt reduction is counted twice" | Premise TRUE | +0.048 DCF (stub fix) | ACCEPT-IMPL (CW23) |
| CC5 | "Only the frozen-IC variant matches all five cells" (crux grid) | Premise TRUE — the correct mechanism (their diagnosis, confirmed in code) | ±0.2% | ACCEPT-IMPL (CW14) |
| CC6 | Book lens untouched at 15% | TRUE | −0.018 on 15% central | ACCEPT-IMPL (CW12) |
| CC7 | "Numerator and denominator sit in different periods" (trailing multiple on forward EBITDA) | TRUE | −0.011 central | ACCEPT-IMPL (trailing-on-trailing) |
| CC8 | "The same input carries two different dates in the same document set" (Tabreed price) | TRUE | −0.024 central (restrike) | ACCEPT-IMPL (CW16 + consistent dating) |
| CC9 | "A premium, not a discount" (Empower 10.96x vs Tabreed 10.7x) | TRUE on the sheet's own cells | Nil | ACCEPT-TEXT (P/E is the defensible discount; sheet note fixed) |
| CC10 | "Total FY2026-30 additions of 445k exceed the backlog by 43%" | Premise TRUE; conclusion (path unjustified) PARTIAL — signings run 163-186 contracts/yr | Bear already prices halved additions (−0.72 DCF) | ACCEPT-TEXT (FY28-30 justified on the signing run-rate, not the standing backlog) |
| CC11 | "A reader is never told that the 'shock' half-year produced record profits" | TRUE | +0.2% if FY26E ran at H1 rate | ACCEPT-TEXT (CW22) |
| CC12 | A.2 receivable row mixes portions | TRUE | Nil | ACCEPT-IMPL (CW2) |
| CC13 | FCFE coverage uses 154.1 actual vs model's 167.6 | TRUE | Nil (outside DCF) | ACCEPT-IMPL (model's own line; coverage 1.01x) |
| CC14 | Equity roll and net-debt roll start from different dates | TRUE | Nil (display) | ACCEPT-IMPL (both from 30-Jun-2026) |
| CC15 | "An IAS 23 capitalisation rate is a weighted historical average… not a marginal rate" | TRUE (label) | +1.0% if struck at the band midpoint — not adopted (top-of-band is the conservative anchor) | ACCEPT-TEXT (relabelled; EIBOR+margin band shown; Sep-2027 roll sensitivity added) |
| CC16 | Workbook "warm-winter shock" vs the company's ~80% hospitality attribution | TRUE | Nil | ACCEPT-IMPL (renamed) |
| CC17 | "The same June-2026 CBUAE report forecasts a rebound to 9.8% in 2027" | TRUE [F] | Nil (supports the base case) | ACCEPT-TEXT (both legs cited) |
| CC18 | "Empower debuted on DFM on 15 November 2022" | TRUE [F: Dubai Media Office] | Nil | ACCEPT-TEXT |
| CC19 | "The report's own 90% beta interval maps to 1.710-2.940, far wider than the published field" | TRUE | The stated-uncertainty defect | ACCEPT-IMPL (construction + beta-interval ranges stated beside the scenario field; centrals to 2dp) |
| CCU1 | Damodaran July row unverifiable; "reported parameters reproduce 4.781%, not 4.811%" | Their reconstruction used a mis-quoted mature ERP | — | RESOLVED: primary July file in hand reads 4.811% exactly (CW33); their 4.17% mature figure belongs to the July HEADLINE set, the workbook's implied mature base is 4.20% |
| CCU2 | Technical indicators unverifiable; coherence passes | — | — | RESOLVED (CW36) |
| CCU3 | Simulation/calibration claims unverifiable; coherence passes | — | — | RESOLVED (CW37) + language downgraded |
| CCU4 | FY2025 note-level splits unverifiable; "strong indirect evidence" | — | — | RESOLVED (CW34/35) |
| CCU5 | Bull 2.221 "matches neither" stated variant | Premise FALSE — it matches 110/110/100/90/80 exactly (CW15 [C]) | — | RESOLVED by CW15's replication; description fixed; their two candidate paths were not the coded one |
| CCU6 | "If any of that other income is rent from the investment properties… it is capitalised in the DCF and the asset is added again" | Possible double count, bounded 0.026 (1.2%) | ≤0.026 | UNRESOLVED→RESEARCH: FY2025 other-income note is OCR-illegible on composition; bounded and disclosed in the bibliography as an open item; conservative reading (strip) would cost ≤0.013 on the central |

## GT — "Gemini think" memo (7 findings)

| # | Their finding | Verdict | Price | Disposition |
|---|---|---|---|---|
| GT1 | Spot "marginally stale against the 1.56 trading tape" | Premise FALSE: the study anchors the 7-Aug close 1.50; their own data lists 1.56 on 10-Aug (post-anchor). GR verified 1.50 at 7-Aug | — | REJECT with receipt (anchor date discipline; their "live tape" postdates the anchor) |
| GT2 | "The cash generated between January and June 2026 is double-counted" | TRUE | +0.048 | ACCEPT-IMPL (CW23/CC4). Their t=0.25 stub implementation overstates the fix; t=0.5 year-end stub adopted |
| GT3 | "You cannot apply a perpetuity growth rate to an amortizing financial receivable" | TRUE in substance (= CW10/SA3) | +0.086 net | ACCEPT-IMPL (clean treatment). Their variant adds the asset AND keeps partial flows — the both-sides fix adopted instead |
| GT4 | "Applying a trailing multiple to forward earnings illegally double-counts the growth rate" | TRUE | −0.006 central | ACCEPT-IMPL (CW17) |
| GT5 | "By netting the cash… but failing to blend the lower cash yield… the author gives the company a free pass on its negative carry" (WACC 7.79%) | Premise TRUE as a construction; conclusion (it is THE correct WACC) contested — CW/CC derive the opposite direction from the same facts | −0.083 DCF at 7.79% [C: 2.099 on old base] | ACCEPT-DEFECT/REJECT-FIX: priced as the third construction (2.227 on revised base); base defended by the transient-cash receipts (payout ≈ FCFE; 2x policy) |
| GT6 | "NCI must be deducted at audited book value (AED 191m)" | Premise FALSE by coherence: valuing the group above book while charging minorities at book applies two standards to the same subsidiaries; GR independently calls the profit-share method "mathematically superior" | +0.004 if adopted | REJECT with receipt (coherence test; the bibliography's judgement row already carries the overturn condition — a disclosed minority transaction) |
| GT7 | "Corrected Fair Value… 2.22 AED" | A stack of their fixes incl. the rejected GT5/GT6 and a mis-set stub (t=0.25) | — | REJECT as a composite; its accepted components (GT2/GT3/GT4) are implemented and priced individually — the revised primary lens is 2.31 |

## GR — "Gemini research" audit (4 findings; the rest are verifications)

| # | Their finding | Verdict | Price | Disposition |
|---|---|---|---|---|
| GR1 | "Terminal value concentration exceeding the 75 percent threshold… classified as an immediate red flag" absent a fade/sensitivity | Premise TRUE as stated risk; the study disclosed the share and sensitises the rate — now also the 0%-growth end | Grid to 0% shows −12% central | ACCEPT-TEXT (grid extended; concentration discussion expanded) |
| GR2 | "A 4.4-year tenor sovereign yield… inherently underprices long-duration interest rate risk" | TRUE and disclosed; tenor corrected to 4.50y; 2033 sukuk named | Direction ambiguous (the 2033's last print is LOWER) | ACCEPT-TEXT (CW26) |
| GR3 | "Extrapolating an aggressive negative working capital ratio into perpetuity… masks severe long-term liquidity constraints" | TRUE as a risk statement (= SA4) | If the release halves: −0.04 central | ACCEPT-TEXT (§7 caveat sharpened; deposit-reversal named as the mechanism; NWC ratio already a tested driver in the workbook) |
| GR4 | "Anchor all risk-adjusted capital allocation assessments strictly to the harsher 15% framing" | A recommendation to the reader, not a defect | — | NOTED to the client; the study continues to publish both framings un-averaged (house rule), reader chooses |

## Contradictions between critiques, arbitrated
1. **WACC construction**: CW/CC (gross weights, value +9%) vs GT (net weights with carry, value −4%). Both observe the same real defect (an unpriced construction); their fixes are mutually exclusive. Arbitrated by coherence + company policy receipts: target-net base retained, ALL THREE constructions priced side by side. 2. **NCI**: GT (book) vs GR (profit-share superior) — profit-share wins on the two-standards coherence test. 3. **Refinancing scope**: CW (one tranche) vs GR (both) — primary borrowings note decides for CW. 4. **Spot**: GT (1.56) vs GR (1.50 verified) — anchor-date discipline decides for GR.

## Revised results (all fixes implemented — FINAL, second run, 17-Aug-2026)
Primary lens 2.12 (9%) / 1.96 (15%) · dual weighted centrals, published side by side with
neither privileged as base: **recovery (de-escalation) 1.84 (9%) / 1.73 (15%)** and
**continuation 1.81 (9%) / 1.70 (15%)** · scenario field 1.45-2.15 · construction range on
the primary lens 2.05 (carry WACC) to 2.49 (DFM beta), with gross-weights at 2.27 ·
crux cost 2.8% (true re-runs) · TV 78.1% of EV. The second run additionally found and
fixed a FY2025 statement-face extraction error (G&A 256.383 / other income 24.430 vs the
first pass's 246.577 / 14.624 — both pairs close the operating-profit identity, hence
unseen by the assertion) and the rental double-count against the investment properties
(CCU6, confirmed against note 29), adopted the two-stage terminal (FY31-40 at 2.5%
volume-only, then 1.5% perpetuity), added the physical EFLH × tariff build showing the
derived 0.634 AED/RTh sits 1.4% below the RD10 v1.3 cap of 0.643 (no tariff headroom),
and de-privileged the recovery case into the dual-central presentation above.
Verification on the rebuilt deliverables: compute asserts 9/9; workbook recalc
all-formula-cells clean; driver test directional with dead-input sweep clean; scrub and
table checks clean; PDFs re-read.
