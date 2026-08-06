# SCEM — self-audit, written 2026-08-06T16:19Z

Written BEFORE reading `Claude_code.docx`, `Gemini_deep_thinking.docx` and
`Gemini_deep_reserach.docx`. **Anchoring disclosure:** the harness auto-loaded
`Claude_cowork.md` into context before this audit could be run, so this list is NOT
independent of that document. It IS independent of the other three. Items marked †
are ones I can evidence I knew from building the model (they concern my own code paths
and my own deliberate shortcuts), not from reading a critique.

A self-audit that finds nothing is a failed self-audit. This one finds 45.

## A. Derivation of the historical operating line — my largest exposure

1. † **FY2025 EBIT back-solved through the STATUTORY rate.** `ebit['FY2025'] = pat_fy25/(1-0.225) - treasury`. If the effective rate ≠ 22.5%, EBIT is wrong by the whole wedge. I took this shortcut knowingly because the filings were unreachable, and I did not test it against any disclosed effective rate.
2. † **FY2025 treasury income is degenerate, not derived.** `cash_fy24 = treas_fy24 / yield` then `treas_fy25 = cash_fy24 * yield` — the same yield both ways, so `treas_fy25 ≡ treas_fy24` identically. In the workbook this shows as the literal formula `=C10`. It contradicts my own FY2026+ method (opening cash × yield) and my own balance sheet, on which cash rises 35%.
3. † **FY2024 EBIT inherits the same statutory-rate error** via the profit bridge.
4. † **FY2023 EBIT/EBITDA rest on an input I invented.** `treas_fy23 = 198` is a house estimate I introduced *specifically* to stop FY2023 EBITDA going negative under an earlier scaling. That is fitting an input to a desired output.
5. † **I never searched for quarterly results.** A study dated 6 Aug 2026 whose latest actual is FY2025 (Dec-2025). If Q1-2026 was filed, the forecast base is stale and every forward line inherits it.

## B. The net-cash leg — 37% of the DCF equity value

6. † **The ×1.35 FY2025 cash roll is a bare assumption**, introduced late to break a circular reference between the DCF and the balance sheet. It carries ~EGP 20/share and appears nowhere in the Word study.
7. † **FY2024 cash back-solved using a yield captioned "FY2025"** — period mismatch in my own cell.
8. † **Stock/flow error:** a full-year income flow divided by a yield produces an *average* balance, not a year-end one. I used it as year-end.
9. † **Net cash is not sensitised**, although §7 of my own study says an error there "matters more than an error in almost any operating assumption." I published four sensitivity grids and omitted the one I named as largest.
10. † **The balance sheet closes on a silent plug.** I wrote row 11 = assets − equity, so total liabilities is a residual that absorbs every inconsistency. FY2025 residual falls to ~706 against FY2024's *disclosed* 1,611.

## C. Arithmetic and internal-consistency defects I introduced

11. † **"Net cash worth 37% of its market capitalisation"** — 5,307/20,604 = 25.8%. 37% is against the *DCF equity value*. I used the wrong denominator on the cover and in §1.7, and the right one in §7.
12. † **"Profit after tax exceeds EBITDA"** is false in my own Table A1 for every year except FY2024. It was true in an earlier draft (when I had FY2025 EBITDA at 1,590) and I failed to retract it after the P&L closure changed the number.
13. † **Weighted-central bear/bull are fudge factors.** In `compute.py` the bull is literally `fv_central * 1.14` and the bear carries a `* 0.88`. They are presented in Table 8 as a weighted range. No weight vector produces them, and they exist nowhere in the "formula-driven" model.
14. † **The 172% book ROIC in ¶27 does not reconcile to my own balance sheet.** The DCF's invested-capital roll and the Balance Sheet's PPE + working capital are two different quantities. This sits in the paragraph carrying what I called "the single most consequential judgement."
15. † **Historical EPS on today's share count.** I *derived* the 92.61mn → 260.81mn rights issue in my own first response and then failed to carry weighted-average shares into the model. FY2023/FY2024 EPS are wrong.
16. † **Table 4's capex "history" is one assumption, three years.** 4.8% of revenue each year, with a "Character: burst/stable" column implying observed behaviour — in a study whose §7 says no capex figure could be retrieved.
17. † **Cash Flow sheet headers are offset from the data** (labels in B4:F4, data in E5:I5). Every column is mislabelled.
18. † **The workbook ships with no cached values.** openpyxl writes formulas without evaluating them, so the delivered file reads blank until recalculated — while READ FIRST tells the reader to "change a blue cell and watch the model reprice."
19. † **D&A ratios (9.4/6.2/4.6%) are embedded inside Income Statement formulas**, not on Assumptions. They are drivers my own driver test therefore cannot perturb.
20. † **`Balance Sheet`!B5/B7 are back-solved constants pasted to 12+ decimals**, outside the three pasted classes READ FIRST declares — which says "anything else pasted would be a defect."
21. † **"three and a half times" (Word) vs "3.4x" (model)** — one statistic, two renderings.
22. † **Word Table A2 omits the reported-equity cross-check** (5,200) that the model carries in `Balance Sheet`!D13, so BVPS 27.09 is printed against body text saying "roughly EGP 5.2 billion of equity."
23. † **Terminal reinvestment jumps ~5% → 53% of NOPAT** between the explicit window and the terminal. A real discontinuity I neither quantified nor defended.

## D. Method and judgement

24. † **The unit-build "check" is tautological.** Price is solved as revenue ÷ volume, so the residual is zero for *any* market-share assumption. I presented "zero in every historical year" as calibration evidence. It is an identity.
25. † **The solved FY2025 realised price (EGP 3,367/t) sits well below the ~3,900/t industry level I cite two sections earlier**, and I waved it through as "ex-works net of freight and rebates" without testing it. If the market price is right, my volume is too high.
26. † **The normalised lens capitalises a peak revenue base.** Normalised EBITDA = FY2025 revenue × 26.5%. FY2025 revenue embeds the post-quota price spike I describe at length. I normalised the margin and not the base — half a normalisation, in the lens whose stated purpose is refusing to capitalise a peak.
27. † **A trailing peak-year peer multiple applied to normalised earnings.** 5.03x is struck in the peer's peak year; applying it to already-normalised EBITDA discounts the cycle twice.
28. † **The DCF margin path (mean 27.7%) runs above my own mid-cycle margin (26.5%)**, unreconciled, and FY2026 *expands* 250bp in a year I describe as having real price declines and rising energy costs.
29. † **Experts 1 and 2 are verbatim the asset and normalised lenses.** Only Expert 3 is a new construction. Appendix C claims "three independent valuations … each built by a different method." My own Table C1 caption half-concedes this without withdrawing the claim.
30. † **"No rating and no price target"** against a single-point central of 62.81, a "−20.5%" headline, per-lens "versus spot" columns and named price zones. Functionally a target.
31. † **Beta 1.00 versus my own bias-corrected 0.837.** Containment in a wide CI is not corroboration. I rounded up, which lowers the value, and did not price the rounding.
32. † **"Not usable" overstates the beta gate.** n and SE(β) both pass; only the R² floor fails, and a low R² is exactly what thin trading produces — which I then correct for two paragraphs later.
33. † **Terminal rf rests on a 5% CBE target while my own §1.6 says "the 7% and then 5% targets."** The operative Q4-2026 target is 7% ±2. Both terminal rf and terminal g hang off the 5%.
34. † **"A standard ~5.5pp emerging-market real-rate convention"** — I called a house view "standard" in the same paragraph where I correctly label the neighbouring terminal inputs as house views.
35. † **ERP citation is under-specified.** "Damodaran, Egypt row" — the Egypt row's headline total ERP is the rating-based figure; 9.41% is the CDS-based variant. A checker following my citation lands on a different number.
36. † **Replacement-cost basis not stated.** USD/tonne benchmarks are commonly quoted on *clinker* capacity; I applied USD 130/t to *cement* capacity (3.8Mt). The two bases differ materially and feed both the asset lens and terminal invested capital.
37. † **Discounting is year-end with no stub**, at a valuation date seven months into FY2026. FY2026 cash flow is discounted a full year and the cash added is a 31-Dec-2025 balance.
38. † **Sector table mixes bases.** 54 consumption + 18.5 exports ≠ 65 production. I captioned it "the sector case in one number."
39. † **Free float stated as 22.4%** — that is the non-Vicat remainder. If any other strategic holder exists, the true float is lower and my own illiquidity argument is understated.
40. † **Monte Carlo median drifts up (+4.8% over 3M)** against a −20.5% fundamental conclusion, unreconciled, while §6 reads zones "against the fundamental work."
41. † **Word says the distribution is "worse than the benchmark"; the model says PARITY.** The point estimate is negative; the bootstrap does not reject parity. I stated the stronger claim in prose.
42. † **The beta sensitivity moves the terminal cost of equity too**, although the terminal rates are declared house views. Arguably inconsistent.
43. † **"The egress policy refused every external host"** in READ FIRST, without saying that server-side search still worked and supplied the macro, peer and sector figures. Incomplete in the deliverable even though I said it correctly in chat.
44. † **No sources cited in the study itself.** They are in the separate bibliography, which is what was asked for — but a reader of the study alone cannot trace a figure.
45. † **Export cap not researched.** I did not check whether Egypt constrains export volumes, on a plant whose export position I argue in §1.7.

## Priced?

No. Nothing above is priced yet. Pricing follows in the main pass, per the procedure —
no finding gets called immaterial without a number.
