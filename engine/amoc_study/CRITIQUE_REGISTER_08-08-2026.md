# AMOC — critique register, four reviewers, one row per finding

**Subject:** `AMOC_Valuation_Study_06-08-2026_public.docx` / `AMOC_Valuation_Model_06082026_public.xlsx`, audited edition, published weighted central **EGP 7.1636** against spot **EGP 9.10**.

**Procedure:** the ten-step critique-response procedure. This file is steps 2 to 7. Step 1 (the self-audit written before any critique was opened) is `SELF_AUDIT_pre_critique.md`. Step 6 (full independent re-derivation of anything above 5% of central) is appended to that file for finding D-1 and appears inline below for the others that cross the line.

**The 5% line:** 5% of EGP 7.1636 is **EGP 0.3582 a share**. Anything at or above that is escalated to a re-derivation and may not be settled by argument alone.

**Pricing method:** every price in this file is a number out of the same engine that produced the published figure, not an estimate. Parameter findings are priced by `price.py`, which re-runs the whole model — all four lenses, all weights — with the named registered input overridden. Bridge findings are priced on the published lens outputs. Where a finding cannot be priced because it names no number, the row says so explicitly and prices the *largest* reading of it, so no finding is dismissed for vagueness.

**Reconciliation:** 89 raised, 89 answered, 0 unaddressed.
- A — Gemini deep thinking: 15 raised, 15 answered
- B — Gemini deep research: raised and answered, see §B
- C — Claude Code: raised and answered, see §C
- D — Claude Cowork: raised and answered, see §D

**Bucket key:**
`ACCEPT` accept and implement · `DEFECT-NO-FIX` accept the defect, reject the proposed fix · `RESEARCH` unproven, needs evidence I do not have · `REJECT` rejected with receipts · `YOURS` your decision, priced, with a recommendation.

---

## §A — Gemini deep thinking ("Head of Quantitative Model Risk Management", Zero-Trust Adversarial Audit)

### A-1. "The report recognizes an EGP 921.4mn provision for past tax disputes (Note 10-1) but deliberately leaves it out of the EV-to-Equity bridge… It must be treated as debt-like and deducted dollar-for-dollar."

**Premise — VERIFIED, and the receipt is worse than the critic's.** `provisions` is a registered input at `compute.py:189` carrying 921,440,353 (tax disputes 904,609,345 + other 16,831,008). It appears exactly three times in the whole model: twice inside a `say()` narration at `compute.py:705-706`, and once in the output dictionary at `compute.py:1305`. It appears **nowhere in the bridge**. I did not have to take the critic's word for it — `python3 price.py '{"provisions": 0.0}'` returns central EGP 7.1636, **identical to the published figure to four decimals**. Setting a 921mn liability to zero moves the valuation by nothing at all. It is a dead input that my own reachability sweep passed, because the sweep accepts "quoted in a deliverable" as reachability and the study does quote it. The sweep was satisfied by a sentence.

**Price — EGP −0.6064 a share on the weighted central, −8.47%, to EGP 6.5572.** Full face on the DCF, relative and normalised lenses (0.7135 a share each, weights 0.45 / 0.20 / 0.20); the book lens is untouched because parent equity is already struck after the provision. The critic's own arithmetic lands on EGP 6.56. **Above the 5% line — escalated to re-derivation, below.**

**Conclusion — ACCEPTED in full, including the magnitude.** The claim that "DCF NOPAT covers it" is one I never actually made in the study; the study simply never carries the number into the bridge at all, which is worse than making a bad argument for it. Forward NOPAT applies the audited 22.12% effective rate to forward EBIT. That is the recurring operating tax charge. It cannot also be the settlement of an assessment raised on years already closed. Two separate cash outflows, one modelled, one not.

**Re-derivation (step 6).** Three questions decide the size, and I worked each rather than accepting 921.4 because a critic named it.
1. *Is it a real claim on the cash?* Yes. Note 10-1 is a provision recognised under the local equivalent of IAS 37, i.e. a present obligation whose settlement is probable and whose amount management has already best-estimated. It sits inside total liabilities of 3,311.6mn. The critic calls it "off-balance-sheet"; it is not, and that word is wrong — but the error runs against the critic, because a recognised provision is a *stronger* case for deduction than a contingent disclosure would be.
2. *Is it already deducted somewhere?* No. Net debt is `debt_b − cash_b` at `compute.py:682` — short and long borrowings 20.977mn less free cash 2,463.522mn. Working capital is `inventory + receivables − payables` at `compute.py:679`; provisions are not in the payables line. Invested capital is PPE plus that same working capital at `compute.py:685`. The provision is in none of the three. No double count.
3. *Full face, or discounted?* Full face. A best-estimate provision is already the expected value of the outflow; haircutting it a second time for probability would double-count the estimation. Timing would argue for discounting, but no settlement schedule is disclosed, and at a 27.8% cost of equity a guessed two-year deferral would cut the charge by roughly 39% — a swing of 0.24 a share resting on a date nobody has published. Full face is the defensible reading, and I record the timing question as an unresolved uncertainty rather than pretending it away.
   A fourth question — is the deduction 921.4 or only the 904.6 tax-disputes component? — is worth EGP 0.0110 on the central (6.5682 vs 6.5572). The other 16.8mn is also a recognised provision. Deduct all of it.

**Bucket: ACCEPT.** This is the largest single defect any reviewer found in the bridge, and it is mine.

---

### A-2. "Lens 2 (Relative Multiples) claims to be a cross-check, but the forward EV is achieved by discounting a 2027 exit multiple using Lens 1's exact explicit WACC factor (0.6022), while adding back Lens 1's exact interim PV of Free Cash Flow. Lens 2 is mathematically subordinated to the intrinsic DCF, destroying its value as an independent market read."

**Premise — VERIFIED.** `df_rel = df[REL_I]` at `compute.py:1061` is literally the DCF's own year-2 discount factor, 0.60218, and `pv_interim = sum(pv[:REL_I+1])` on the next line is literally the sum of the DCF's own discounted free cash flows. The critic read the model correctly and quoted the factor to four decimals.

**Price — the contamination is worth EGP +0.9789 on the relative lens, EGP +0.1958 on the weighted central, +2.73%.** Struck by removing the borrowed machinery entirely: apply the same 4.5× multiple to *trailing* EBITDA of 1,653.2mn, so nothing is discounted and nothing is added back. That gives EGP 7.3841 against the published 6.4052, and a central of 7.3594. Note the direction: the borrowed DCF machinery is currently making the relative lens **lower**, not higher. The contamination is not flattering the answer.

**Conclusion — PREMISE ACCEPTED, CONCLUSION REJECTED with receipts.** "Destroying its value as an independent market read" does not follow, and the coherence test is this: what does a relative lens actually contribute? It contributes a **multiple** — 4.5× EV/EBITDA — and a **metric** to put it on. Both are independent of the DCF; the multiple comes from the peer read, the EBITDA from the operating build that every lens shares. What it borrows is only the *time-shift*: the arithmetic that moves a 2027 enterprise value to today. Any forward multiple needs a discount rate to do that, and the alternatives are not more independent — a "market-implied" rate would have to be reverse-engineered from prices that already embed the same cost of capital, and using a different rate for the same firm in two lenses would be an inconsistency, not an independence.

That said, the critic has found something real underneath the wrong conclusion: **the cleaner construction avoids the time-shift altogether.** Putting the multiple on the trailing metric needs no discount factor and no interim add-back, and it is the construction a market participant actually quotes. I will rebuild the lens that way. So the fix goes in — for the critic's reason restated, not for the critic's reason as written.

**Bucket: DEFECT-NO-FIX on the argument, ACCEPT on the rebuild.** Rebuild lens 2 on trailing EBITDA; drop `df_rel` and `pv_interim`; keep the forward-multiple version as a disclosed alternative so the reader sees both. Net effect on the central, before the other accepted changes, +2.73%.

---

### A-3. "Capital Expenditure (EGP 146mn) is running permanently below Depreciation (EGP 148mn). This forces a negative net reinvestment rate. Applying a +5% perpetual terminal growth rate on a shrinking capital base violently breaks the steady-state identity (Growth = ROIC * Reinvestment Rate). The Terminal Value (58.7% of EV) is structurally bloated."

**Premise — PARTLY VERIFIED, and the part that is wrong is load-bearing.** Year-1 capex is 145.56 against D&A of 147.63, so in 2026E capex is indeed 2.07mn below depreciation. But "permanently" is false on the model's own output: capex compounds at the fixed-cost inflation path to 164.5 / 183.4 / 201.7 / **220.9** by 2030E while D&A is held flat at 147.63, so the asset base **grows** — `fcst.ppe` runs 1,298.3 → 1,315.1 → 1,350.9 → 1,405.0 → **1,478.2**. The critic checked one year and wrote "permanently".

More important, the identity the critic invokes is the one the model actually enforces, and enforces on invested capital, not on PPE alone. `compute.py` solves the terminal reinvestment rate *from* growth and return: `rr = g / roic`, then applies `(1 − rr)` to terminal NOPAT. At `roic_term` 35.36% and g of 5%, `rr_term` is 14.14% — terminal free cash flow is struck at 85.86% of NOPAT, not 100%. The identity is not broken; it is the constraint the terminal block is built on. Invested capital rises from 3,034.5 to 4,197.7 over the window, a 38% increase, which is the opposite of a shrinking base.

**Price — EGP −0.2160 on the weighted central (−3.02%) for g = 3%, or EGP −0.0902 (−1.26%) for g = 4.24%.** The second is the more interesting number: 4.24% is the growth the reinvestment waterfall itself produces (`terminal_recon.g_waterfall`), so it is what the company's own history implies rather than what a critic prefers. Both are **below the 5% line**, so this finding, at its full stated force, cannot move the answer more than a fifth of the way to the critic's own corrected number. The critic asserted "violently" and "structurally bloated" without pricing either.

**Conclusion — REJECTED on the mechanism, with receipts; the residual is a disclosure gap.** The steady-state identity is enforced at `compute.py` in the `_val_at` and `dcf_scenario` terminal blocks and can be read off `study_numbers.json` as `roic_term` 0.3536 and `rr_term` 0.1414. What the study does **not** do well enough is *show* that enforcement to a reader who would otherwise do exactly what this critic did — compare year-1 capex to D&A and conclude the base is shrinking. That is a real defect in the writing.

**Bucket: REJECT on the finding; ACCEPT a presentation fix** — put the `g = rr × ROIC` reconciliation on the face of the DCF sheet and in the terminal-value section, with the five-year PPE and invested-capital paths beside it, so the identity is visible rather than merely true. Also disclose the 4.24% waterfall growth beside the 5% used, priced at −1.26%.

---

### A-4. "The author deducts 4.645% (the NCI share of net income) from the entire consolidated Operating Enterprise Value… However, the author then adds 100% of the consolidated cash to the parent equity, effectively seizing the minority's claim on the subsidiary's cash."

**Premise — VERIFIED.** The bridge is `eq_attr = ev × (1 − nci_share) − nd` with `nd` the consolidated net debt of −2,442.5mn. The minority is charged its share of the operating enterprise and credited none of the cash. That is an internal inconsistency, and it is mine.

**Price — EGP −0.0878 on the DCF lens, EGP −0.0395 on the weighted central, −0.55%.** Struck by applying the minority share to the whole enterprise including net cash: `(ev − nd) × (1 − nci)` gives EGP 6.7640 against the published 6.8518. Below the 5% line, and I am pricing it rather than calling it small.

**Conclusion — ACCEPTED as a defect; the critic's implied fix is the wrong end of the correction, and I have receipts for a third answer.** Charging the minority 4.645% of the *cash* would be right if the cash sat in the subsidiary in proportion to its earnings. Nothing in the filings says it does. The consolidated cash of 2,463.5mn against a subsidiary whose minority earns 30.5mn a half is far more likely to sit at the parent — a refinery's treasury does not distribute itself pro rata to a wax affiliate. The honest correction is not to move the minority onto the cash but to admit that **the 4.645% figure is a profit-share proxy standing in for an ownership-and-location question the filings do not answer.**

**Bucket: YOURS.** Three ways to settle it, priced: (i) leave the bridge as published and disclose the inconsistency — EGP 7.1636, and the least defensible; (ii) charge the minority its share of the whole enterprise including cash — EGP 7.1241, −0.55%, internally consistent and conservative; (iii) keep the earnings-share deduction on operating EV but disclose a range spanning (i) and (ii). **My recommendation is (ii)**: it costs half a percent, it removes an inconsistency a reader can find in one line of arithmetic, and where the filings are silent the conservative reading is the one to publish.

---

### A-5. "The state (EGPC) controls 76.5% of sales and supplies the feedstock. The gross margin is highly volatile (swinging 5% to 10% QoQ). A minor 50bps policy shift by the state wipes out EGP 1.02/share."

**Premise — VERIFIED, and the number is mine.** The margin swing is on the face of my own history: `hist_is` runs 6.85% (6M Dec-24) → 5.05% (3M Mar-25) → 6.14% (6M Dec-25) → 10.19% (3M Mar-26). The EGP 1.02 is read directly off my own published sensitivity: `sens.grid_margin` at a −0.5pp shift gives 5.8305 against 6.8518, a difference of **1.0213**. The critic did not derive it; they quoted my table back at me, correctly.

**Price — EGP −1.0213 on the DCF lens, EGP −0.4596 on the weighted central, −6.42%, for a 50bp margin shift.** **Above the 5% line.**

**Conclusion — PREMISE ACCEPTED, and the finding is not a defect but a correctly-read risk.** There is nothing to fix in the arithmetic: the sensitivity is published, it is live, and it says what the critic says it says. Where the critic is right and I am not, is *emphasis*. A firm whose entire equity value moves 6.4% on a 50bp margin change, whose margin has ranged 5.05% to 10.19% across four consecutive reported periods — a range of 514bp, i.e. **ten times** the shift being sensitised — and whose margin is set by an administered feedstock relationship with a 20.77% shareholder, does not have a point estimate. It has a distribution, and the study's headline presents a point.

**Escalation (step 6) — what does the disclosed margin range actually do?** Re-priced at the observed extremes rather than at ±50bp: the four-period low of 5.05% sits 2.46pp below the 7.51% base, and the high of 10.19% sits 2.68pp above. At −1pp the DCF lens is 4.8091 and at +1pp it is 8.8945 — a span of 4.09 a share on a ±1pp move, against a published bear-to-bull span of 2.37 to 14.66 that is driven by five simultaneous levers. The observed margin range **alone**, at roughly ±2.5pp, would take the DCF lens from about 1.7 to about 12.0. That is the honest statement of this company's uncertainty and the study underplays it.

**Bucket: ACCEPT a disclosure change, REJECT any change to the numbers.** Move the margin sensitivity out of the appendix and onto the summary page; state the four-period observed range beside the base assumption; and say in the opening paragraph that the margin is administered rather than competed, so its history is a policy record, not a market one.

---

### A-6. "Risk-Free Rate (10Y EGP) | 22.31% | ~22.98% | CBE / Sovereign Yields | +3.00%"

**Premise — UNVERIFIABLE FROM HERE, and I will not pretend otherwise.** Every route to a live Egyptian sovereign curve is blocked from this environment: the agent proxy returns 403 on the CBE, on the EGX and on the data vendors, and the same block is why `BIBLIOGRAPHY` carries seven recorded negative results. I cannot confirm or refute 22.98%. What I can say is that the study's 22.31% is sourced and dated in the input registry, and that the critic gives a tilde and a rounded variance rather than a security, a tenor or a date.

**Price — EGP −0.0379 on the weighted central, −0.53%** (`price.py '{"rf":0.2298}'` → 7.1257). Below the 5% line, priced anyway.

**Conclusion — RESEARCH, not accepted and not rejected.** At half a percent this cannot change any reading of the stock, but "I could not check it" is the honest verdict, not "it doesn't matter".

**Bucket: RESEARCH.** Re-verify the 10-year EGP yield against a named auction result the next time egress permits, and disclose the −0.53% sensitivity in the meantime.

---

### A-7. "Statutory Tax Rate | 22.50% | 22.50% | Egyptian Tax Authority | 0.00%"

**Premise — the reviewer has verified a number the model does not use, and scored it a clearance.** The statutory rate is registered as `tax_stat` and is *not* what drives the forecast. Every forward tax charge runs on `TAX_EFF` = 22.1188%, solved from the audited nine months as tax over profit before tax. The critic's own table records "0.00% variance" on a parameter that is inert.

**Price — EGP +0.0000.** No change either way; the statutory rate does not enter the cash flows.

**Conclusion — REJECTED as a clearance, because it clears the wrong number.** This is not a point against the study, but it is a point about the audit: a variance table that ticks a parameter the model does not use is not evidence the model is right. Recorded so the reviewer's clean bill on this line is not mistaken for verification of the tax treatment that actually matters.

**Bucket: REJECT.** No change. The effective-rate derivation is already on the Assumptions sheet; I will label it explicitly as *superseding* the statutory rate so the next reader does not check the wrong one.

---

### A-8. "Your mandate ordered a Sum-of-the-Parts (SOTP) verification for listed subsidiaries 'Aldar, NMDC, and JLR.' I am rejecting this premise. AMOC is a single-asset integrated Egyptian refinery… AMOC has no listed subsidiaries; a Holdco/SOTP valuation framework is inapplicable."

**Premise — correct, and not about this study.** Aldar, NMDC and JLR appear nowhere in the study, the model, the input registry or the bibliography. The reviewer is rejecting an instruction in their own prompt, not a claim of mine.

**Price — EGP 0.0000.** Nothing to price.

**Conclusion — no action.** Recorded for completeness because the procedure says enumerate every finding, and because it is worth noting on the record that one of the four reviewers was working from a contaminated brief. That does not discredit their other findings — A-1 is correct and is the largest in this file — but it is a reason to check each of their factual claims against the filings rather than accept them, which is what the rows above do.

**Bucket: REJECT** (not applicable to this study).

---

### A-9. "The author successfully decomposed the cash line. Total gross cash + deposits is ~EGP 2.97bn. The author flawlessly backed out the EGP 508.8mn in pledged deposits to arrive at the true free cash figure of EGP 2,463.5mn without double-counting."

**A clearance.** Independently reproduced by the reviewer's own Python: 883,351,250 + 2,127,100,720 + 166,405 − 38,345,960 − 508,750,050 = 2,463,522,365, matching `cash` exactly, and net debt 20,977,437 − 2,463,522,365 = −2,442,544,928 matching `nd_cy25` exactly.

**Price — EGP 0.0000.** **Bucket: no action.** Recorded because a register that lists only the hits misrepresents what the reviewer said.

---

### A-10. "Because AMOC holds ~21% of its market cap in net cash… This report brilliantly applies a negative weight to debt (-26.2%). This forces the explicit operating WACC (31.6%) higher than the Cost of Equity (27.8%), properly isolating and penalizing the cash flows for the risk of the pure, unlevered operating assets."

**A clearance, and the one I most wanted checked.** This is the construction that broke my own build twice — an assertion `wacc_exp > wacc_net_naive` failed and was decomposed rather than patched. The reviewer reproduced `we = 1.2624`, `wd = −0.2624`, `wacc = 0.3158` to four decimals from the stated inputs.

**Price — EGP 0.0000.** **Bucket: no action.**

---

### A-11. "The internal math of the model (discount factors, fractional WACC glides, and terminal PVs) was executed flawlessly by the author with zero plain-text arithmetic breaks."

**A clearance on the arithmetic layer.** Consistent with the workbook's own gate: 488 of 488 formula cells reproduce the model under the strict evaluator, 0 unresolvable, 0 unchecked.

**Price — EGP 0.0000.** **Bucket: no action.** Recorded with one caveat that runs against me, not for me: the reviewer checked the arithmetic of the *published* build. It is the standing gates on the *nine-sheet audited* workbook that I have not yet rebuilt (my own self-audit items S10–S12), so this clearance is narrower than it reads.

---

### A-12. "Book Value Lens: Unaffected, as the provision is already appropriately recorded in total liabilities, making the Book Value of EGP 3.71/share accurate."

**Premise — VERIFIED.** `bvps` 3.7094 is parent equity 4,790.7mn over 1,291.5mn shares, and parent equity is struck after the provision sits in liabilities of 3,311.6mn. The reviewer is right that the book lens needs no adjustment for A-1, and this is also the internal consistency check that confirms A-1: the provision is real enough to reduce book equity, so it is real enough to reduce the bridge.

**Price — EGP 0.0000** (this row asserts no change and none is warranted). **Bucket: no action.**

---

### A-13. "Corrected Weighted Central: (0.45·6.14) + (0.20·5.70) + (0.20·7.99) + (0.15·7.06) = 6.56 EGP."

**Premise — the arithmetic is right on their own inputs.** Reproduced exactly: deducting 0.7135 from the DCF, relative and normalised lenses and leaving book alone gives **6.5572**, which rounds to their 6.56. The weights they used are my published weights.

**Price — EGP −0.6064, −8.47%.** Same as A-1; not double-counted, this row is the aggregation of it.

**Conclusion — ACCEPTED as the correct consequence of A-1 alone.** It is not the final number, because it takes no account of A-2 (+2.73% the other way), A-4 (−0.55%) or anything in the other three files. A corrected central will be struck once, after every accepted change, and not lens-by-lens in the middle of a register.

**Bucket: ACCEPT** (as the consequence of A-1).

---

### A-14. "This represents a severe -27.9% downside against the spot price of EGP 9.10."

**Premise — arithmetically correct** (6.5572 / 9.10 − 1 = −27.9%). **Price — no separate price; a restatement of A-13.**

**Conclusion — ACCEPTED as arithmetic, flagged as presentation.** Worth one line on the record: the published study already reads EGP 7.1636 against a spot of 9.10, i.e. −21.3%. The critic's correction deepens a discount the study already reported. This is not a case of a critique overturning a "fairly valued" conclusion — that was the *superseded* EGP 9.38 edition, which is still what the live website publishes. **Bucket: ACCEPT.**

---

### A-15. "Furthermore, given the structural inflation of Free Cash Flow via capex starvation, EGP 6.56 should be viewed as an absolute ceiling, not a conservative baseline."

**Premise — REJECTED, with receipts, and this is the row where the reviewer's own file contradicts itself.** "Capex starvation" is A-3 restated, and A-3's premise fails on the model's own five-year capex path (145.6 → 220.9) and PPE path (1,298 → 1,478). But the sharper point is internal to the critique: a *ceiling* claim requires that every unpriced adjustment run downward. The reviewer's own A-2 finding, priced, runs **upward** by 2.73%, because the DCF machinery they object to is currently depressing the relative lens. A number cannot be a ceiling when one of the two "critical failures" that produced it pushes the other way.

**Price — the "ceiling" claim, taken at its own word, is worth EGP 0.0000**, because it proposes no adjustment; the adjustments it gestures at are A-3 (−1.26% to −3.02%) and A-2 (+2.73%), which substantially offset.

**Bucket: REJECT.** No change. Recorded because a rejection needs receipts at the same standard as an acceptance, and the receipts here are the model's own capex path and the reviewer's own second finding.

---

**§A running total, before arbitration against the other three files:** A-1 −8.47%, A-2 +2.73%, A-4 −0.55% (recommended), A-3 −1.26% (disclosure of the waterfall growth, if adopted). Everything else in §A is priced at zero or is a clearance.

---

## §B — Gemini deep research ("Quantitative Model Risk Audit", Zero-Trust Protocol, corrected central EGP 6.10)

**Before the rows: this file has an internal contradiction that decides three of them.** Its own audit ledger records `Cash & Equivalents (mn EGP) | 2,463.52 | 2,463.52 | Audited Financials | 0.00%` — a clean verification of the exact figure the model uses. Its bridge then strips a further 508.75mn of pledged deposits out of that same 2,463.52mn. Both cannot be true. §3.2 of the same document also deducts the 921.4mn provision from the equity bridge *and* §3.3 deducts it a second time from book equity to reach a book value of 2.996. The coherence test below resolves each against the filing, not against the other reviewer.

### B-1. "Independent verification of the Egyptian Exchange (EGX) data feed confirms these exact figures without variance… The implied market capitalization mechanically calculates to 11,752.65 million EGP. The empirical grounding of the equity base passes verification."

**A clearance.** Spot 9.10, shares 1,291.5mn, market capitalisation 11,752.65mn all confirmed. **Price EGP 0.0000. Bucket: no action.**

### B-2. "the ownership structure correctly identifies Alexandria Petroleum Company as the 20.77% primary shareholder, rectifying historical reporting errors in prior editions that misattributed this direct stake to the Egyptian General Petroleum Corporation"

**A clearance, and specifically a clearance on a defect the audited rebuild fixed.** The superseded edition named EGPC as a 20% shareholder; the filings name Alexandria Petroleum Company at 20.77%, and `alexpet_stake` now carries it. **Price EGP 0.0000. Bucket: no action.** Recorded because it is one of the twelve overturned assumptions and an outside reader confirming the correction is worth having on the file.

### B-3. "annualizing a highly volatile gross margin business introduces profound seasonal forecasting risk. The audited disclosures indicate that the gross margin swung violently from 5.05% in the March 2025 quarter to 10.19% in the March 2026 quarter. Applying a linear extrapolation to a single exceptional quarter creates a structurally fragile base year assumption."

**Premise — VERIFIED on my own history; the characterisation "a single exceptional quarter" is FALSE.** The margins are mine and are right. But the base year is not extrapolated from the March-2026 quarter. It is nine contiguous months — the audited six to 31-Dec-2025 *plus* the reviewed three to 31-Mar-2026 — scaled by 4/3, and the blended base margin that comes out is **7.506%**, sitting between the 6.14% of the six-month half and the 10.19% of the quarter, closer to the half because the half is twice the weight. Reading 7.506% as an extrapolation of 10.19% is a misreading of the arithmetic at `compute.py`: `BASE_GM = gp9 / rev9`, gross profit over revenue across all nine months, not the last three.

**Price — the fragility is real and is worth EGP −0.4596 on the weighted central per 50bp of margin (−6.42%)**, the same live sensitivity priced at A-5, and at the ±2.5pp of the observed four-period range it dominates every other finding in all four files combined. **Above the 5% line.**

**Conclusion — PREMISE ACCEPTED, mechanism REJECTED, and the accepted part is the most important thing any reviewer says about this company.** The single-quarter claim is wrong and I have the receipt. The fragility claim is right and I priced it before I judged it. **Bucket: ACCEPT the disclosure change already carried at A-5** — margin sensitivity onto the summary page, observed range beside the base, administered-margin language in the opening. No change to the numbers, because the 4/3 scalar on nine contiguous months is what the filings support and the alternative twelve-month base is handled separately at D-1.

### B-4. "The target report utilizes a 9.41% total ERP on a credit-default-swap basis. Independent verification utilizing Aswath Damodaran's July 2026 Country Risk Premium dataset indicates that Egypt's total ERP… has widened to 13.94%… The target report's reliance on a stale 9.41% ERP fundamentally underprices the geopolitical and currency devaluation risks."

**Premise — the number is already in the model, and the reviewer has rediscovered my own published alternative.** `erp_rating` is a registered input carrying **0.1394** — the identical figure — sourced to the Damodaran country-premium file, Egypt row, rating basis. The study already computes and publishes the whole rating-basis branch: `wacc_exp_rating` 32.18%, `wacc_term_rating` 20.35%, `ps_rating_basis` EGP **5.8434**. It is not a number I failed to find; it is a number I found, registered, computed, and put in the study as the alternative to the basis I chose.

**Price — EGP −0.2299 on the weighted central, −3.21%** (`price.py '{"erp_cds":0.1394}'` → 6.9337; the DCF lens falls to 6.4650). Below the 5% line, priced anyway.

**Conclusion — PREMISE PARTLY REJECTED with receipts, CONCLUSION becomes YOURS.** "Stale" is wrong: both columns carry the same January-2026 file date in my registry, and the reviewer's "July 2026" citation resolves to a third-party blog reprint, not to the source file. What is genuinely contestable is the *choice* between the CDS column and the rating column, and that is a judgement about which market signal to trust for a Caa1/B3 sovereign, not an error. The CDS basis is the market's live price of Egyptian default risk; the rating basis is an agency letter mapped to a table. I chose the market price. A reasonable person prefers the rating basis on the grounds that Egyptian CDS is thinly traded.

**Bucket: YOURS.** CDS basis EGP 7.1636 as published, rating basis EGP 6.9337 (−3.21%). **My recommendation: keep the CDS basis as the headline and promote the rating-basis figure from a buried alternative to a line on the summary page**, because two of four reviewers reached for it independently, which is evidence the choice needs to be visible rather than defended.

### B-5. "Egypt 10Y Sovereign Yield | 22.31% | ~22.64% - 22.98% | Investing.com Rates | +1.40%"

**Same as A-6, from a second reviewer, with a range instead of a point.** Unverifiable from this environment — egress to the rate sources is blocked and the block is recorded in the bibliography with seven negative results. **Price — EGP −0.0379, −0.53%** at the top of their range. **Bucket: RESEARCH.** Two independent reviewers landing near 22.6–23.0% raises my prior that 22.31% is low, and I record that rather than resting on "I could not check it".

### B-6. "the model then deducts 4.645% of the entire consolidated operating Enterprise Value, amounting to 312 million EGP, as the NCI deduction. This is mathematically illiterate… The audited balance sheet correctly carries the NCI at 34.08 million EGP. Deducting 312 million EGP represents massive valuation leakage and destroys intrinsic parent value."

**Premise — VERIFIED as to what the model does; the proposed fix is worse than the defect.** The bridge does apply 4.645% to the whole operating enterprise value. The reviewer is right that the minority's claim is on Alexandria Wax Products, not on the base-oil, gas-oil and fuel-oil operations the parent owns outright.

**Price — EGP +0.2152 on the DCF lens, EGP +0.0969 on the weighted central, +1.35%**, for the reviewer's fix (deduct the 34.079mn carrying amount instead of 312.05mn). Note the sign: this is one of only two findings across all four files that raises the valuation, and the reviewer includes it in a package they present as a −14.80% correction.

**Conclusion — PREMISE ACCEPTED, FIX REJECTED with receipts.** Substituting the balance-sheet carrying amount for a valuation of the minority stake is the error the reviewer accuses me of, in mirror image. The 34.079mn is historical cost less accumulated share of retained earnings — an accounting residual on a heavily depreciated asset base. Using it as the *value* of a claim on a business earning 30.5mn of minority profit a half implies the minority stake is worth 0.56 years of its own earnings. The same document argues four rows earlier that book value understates a depreciated plant. It cannot be a bad proxy for the parent and a good one for the subsidiary.

**Arbitration against §A — the two reviewers point in opposite directions and both premises are right.** §A-4 says the 4.645% deduction is too *small* in scope because the minority is charged its share of the enterprise but credited none of the cash; §B-6 says it is too *large* in scope because it reaches the parent's wholly owned operations. The coherence test that settles it: **both complaints are symptoms of one defect — a group-level profit share is being used as a stand-in for a subsidiary-level valuation, because the filings disclose no subsidiary balance sheet or segment result.** Neither reviewer's fix repairs that; §B's makes it worse by anchoring on cost, §A's at least keeps the treatment internally consistent. Priced: §B's fix +1.35%, §A's fix −0.55%, the gap between the two reviewers' preferred bridges is **1.90% of central**, or EGP 0.1364 a share.

**Bucket: DEFECT-NO-FIX.** Keep the earnings-share basis, adopt §A-4's consistency correction (recommended there), and **disclose the range explicitly** — 6.7640 to 7.0670 on the DCF lens depending on the treatment — labelled as what it is: a spread created by a disclosure the company does not make.

### B-7. "Note 9-E of the audited financials explicitly discloses that 508.75 million EGP of this balance consists of deposits pledged against credit facilities… In its bridge, the report indiscriminately adds back the entire 2,463.5 million EGP cash pile… Treating it as free cash artificially inflates the equity value by approximately 0.39 EGP per share."

**Premise — FALSE, and the receipt is the reviewer's own audit ledger.** The pledged deposits are **already excluded**. The registered input at `compute.py:166-169` reads, verbatim: *"time deposits 883,351,250 plus current accounts 2,127,100,720 plus cash on hand 166,405, less expected credit losses 38,345,960, **less PLEDGED deposits 508,750,050** which sit in other financial investments."* The pledged balance is separately registered as `fin_inv` = 508,750,050 and described as *"deposits PLEDGED against credit facilities, so not free cash"*. The reviewer in §A independently reproduced the arithmetic in their own Python — 883,351,250 + 2,127,100,720 + 166,405 − 38,345,960 − 508,750,050 = 2,463,522,365 — and recorded it as a verified clearance, *"without double-counting"*. This reviewer's own table then records that same 2,463.52 as verified at **0.00% variance**, and their §3.2 strips 508.75 out of it a second time.

**Price — EGP −0.3939 on the DCF lens, EGP −0.1773 on the weighted central, −2.47%, of pure double-deduction.** This is 30% of the reviewer's entire claimed correction, and it is an error.

**Conclusion — REJECTED with receipts.** No change. **Bucket: REJECT.**

### B-8. "Note 10-1 of the audited financials discloses a massive provision for tax disputes and claims amounting to 921.44 million EGP. The target report explicitly notes this liability but deliberately excludes it from the EV-to-Equity bridge… artificially inflates the fundamental intrinsic value by 0.71 EGP per share."

**The same finding as A-1, from a second reviewer, at the same price, and I accept it for the same reasons.** Independently confirmed by `price.py '{"provisions": 0.0}'` returning the published central unchanged to four decimals — the input is dead. **Price EGP −0.6064 weighted, −8.47%.** Not double-counted with A-1; it is the same correction found twice.

One correction to the reviewer's account of my reasoning: the study does not argue that "the earnings the model discounts are struck after the tax charge that the provision relates to". It makes no argument at all — the number is quoted in the text and never enters the arithmetic. That is a worse failure than a bad argument, and I would rather record it accurately. **Bucket: ACCEPT.**

### B-9. "cash capital expenditure, annualized at 127 million EGP, is running substantially below the depreciation charge of 148 million EGP… the physical plant is degrading, and the company is effectively liquidating its asset base… Applying a 5% perpetual growth rate to a company that is shrinking its physical capital base breaks the theoretical integrity of the model."

**Premise — VERIFIED for the base year, FALSE for the forecast, and this reviewer is more careful than §A on the first half.** Base-year capex of 127.12mn against D&A of 147.63mn is 0.861×, and that ratio is correctly quoted. But the forecast does not hold it there: capex compounds to 145.6 / 164.5 / 183.4 / 201.7 / **220.9**, D&A is flat at 147.63, and PPE rises 1,298 → **1,478** with invested capital rising 3,034 → **4,198**. The asset base grows through the window. And the terminal block solves reinvestment *from* the identity the reviewer invokes: `rr_term = g / roic_term` = 5% / 35.36% = **14.14%**, applied as `(1 − rr)` to terminal NOPAT.

**Price — EGP −0.2160 (−3.02%) at g = 3%, EGP −0.0902 (−1.26%) at g = 4.24%**, the growth the company's own reinvestment history implies. Below the 5% line at full stated force.

**Conclusion — REJECTED on the mechanism with receipts, ACCEPT the presentation fix** already carried at A-3: put the `g = rr × ROIC` reconciliation and the PPE / invested-capital paths on the face of the DCF sheet, and disclose the 4.24% waterfall growth beside the 5% used. Two independent reviewers made the same misreading from the same page, which is evidence the page is at fault even though the model is not. **Bucket: REJECT the finding, ACCEPT the disclosure.**

### B-10. "In Lens 3… the report takes 2028E operating profit (EBIT), inexplicably adds the annualized credit interest earned on the massive cash pile (316 million EGP), applies the corporate tax rate, and then multiplies the resulting earnings by a 7.5x Price-to-Earnings ratio… By capitalizing non-operating financial income at an equity multiple of 7.5x, the model is valuing the risk-free cash asset as if it were a high-return operating business."

**Premise — VERIFIED exactly.** `norm_np = (norm_ebit + norm_interest) × (1 − TAX) × (1 − NCI_SHARE)` at `compute.py:1090`. Stripping the interest gives operating EPS of **0.9782**, which is the reviewer's 0.978 to three decimals; times 7.5 gives **7.3362**, which is their 7.34. Every number in this row reproduces.

**Price — and here the reviewer's own construction breaks, in the direction that flatters their conclusion.** Capitalising the interest at 7.5× values the net cash at **EGP 1.3646 a share**. The net cash attributable to the parent is worth **EGP 1.8034 a share** at face. So the published construction does not inflate the cash — it **understates** it by 0.44 a share. The reviewer strips the interest out and then *does not add the cash back anywhere*, which deletes 1.80 a share of real, disclosed, unencumbered money from a lens: EGP 7.3362 against a published 8.7009, a weighted **−3.81%**. The reviewer's own text states the correct rule — *"the multiple must be applied strictly to pure operating earnings per share, with net cash added separately outside the multiple"* — and then does only the first half of it.

Done properly, the reviewer's own rule gives 7.5 × 0.9782 + 1.8034 = **EGP 9.1396**, a weighted **+1.22%**, i.e. the correction they demand moves the valuation **up**, not down.

**Conclusion — PREMISE ACCEPTED, CONCLUSION REJECTED with receipts, FIX ACCEPTED in the reviewer's stated form rather than their executed form.** Mixing operating and financial income under one operating multiple is muddled and I will separate them. **Bucket: ACCEPT the separation (+1.22%), REJECT the reviewer's arithmetic (−3.81%).** The 5.03% gap between the two is larger than the 5% escalation line and is entirely the reviewer's omission.

### B-11. "For the initial forecast year of 2026, the FCFF correctly calculates to 955.2 million EGP. Discounting these flows… yields a present value of the explicit window of 2,777 million EGP. Adding the terminal value results in a mathematically sound operating Enterprise Value of 6,719.7 million EGP. The core operating mechanics of the model are verified as accurate."

**A clearance, independently recomputed.** Against `fcst.fcff[0]` 955.0998, `dcf.pv_explicit` 2,776.54 and `dcf.ev` 6,718.63. **Price EGP 0.0000. Bucket: no action.**

### B-12. "the recognized IFRS tax liability of 921.4 million EGP was forcibly deducted… This rigorous bridging sequence results in a corrected Equity Value of 7,697.9 million EGP… yields a Corrected DCF Fair Value of 5.96 EGP per share."

**Premise — the arithmetic reproduces exactly** (6,718.63 − 34.079 + 1,933.79 − 921.44 = 7,696.9 → **5.9597**, their 5.96) **and three of its four components are wrong.** The bridge combines: the tax provision (correct, B-8, accepted), the pledged-cash strip (a double deduction, B-7, rejected with receipts), NCI at carrying amount (rejected with receipts, B-6, and it runs the *other* way), and gross debt (correct). **Price — as built, EGP 5.9597 on the DCF lens; with only the defensible component, EGP 6.1383.** **Bucket: REJECT as constructed; the accepted part is already carried at B-8.**

### B-13. "passing this EV through the newly corrected, liability-adjusted equity bridge drops the fair value from 6.41 EGP to 5.49 EGP, an equivalent 14.27% variance"

**Inherits every error of B-12.** The defensible component alone (provision only) gives 6.4052 − 0.7135 = **5.6917**. **Price — the difference between the reviewer's 5.49 and the defensible 5.69 is EGP 0.20 on this lens, EGP 0.04 weighted (0.56%), entirely attributable to the pledged-cash double-deduction.** **Bucket: REJECT as constructed.**

### B-14. "the 316 million EGP in non-operating credit interest was stripped from the earnings base to isolate pure operating EPS, which correctly calculates to 0.978 EGP. Applying the 7.5x target multiple to this clean baseline yields a true operating value of 7.34 EGP, a severe 15.67% downward variance"

**The executed half of B-10.** Reproduced exactly and rejected for the reason given there: it deletes EGP 1.80 a share of disclosed net cash without replacing it. **Price — EGP −1.3647 on lens 3, −3.81% weighted, of which the whole amount is the omitted cash.** **Bucket: REJECT.**

### B-15. "Applying this multiple to an adjusted parent book value that correctly deducts the 921 million EGP tax dispute liability drops the adjusted book value per share to 2.996 EGP. The corrected fair value subsequently collapses from 7.06 EGP to 5.70 EGP, representing a 19.23% variance"

**Premise — FALSE, and this is the second double-deduction in the same document.** Parent equity of 4,790.696mn is struck **after** the provision, which sits inside total liabilities of 3,311.643mn. The balance sheet foots: assets 8,136.418 = liabilities 3,311.643 + parent equity 4,790.696 + NCI 34.079. Subtracting the provision a second time gives exactly the reviewer's number — (4,790.696 − 921.440) / 1,291.5 = **2.9959**, their 2.996 — which is the arithmetic signature of the double-count.

**The other reviewer got this right and said so explicitly:** §A-12 records *"Book Value Lens: Unaffected, as the provision is already appropriately recorded in total liabilities, making the Book Value of EGP 3.71/share accurate."* **Arbitration by coherence test: the balance sheet foots on §A's reading and does not foot on §B's.** §A wins.

**Price — EGP −1.3581 on the book lens, EGP −0.2037 weighted, −2.84%, of pure error.** **Bucket: REJECT with receipts.**

### B-16. "the Corrected Central Fair Value is 6.10 EGP per share… the asset is not trading at a 21% discount as the target report implies, but rather at a severe 33% premium to its mathematically corrected intrinsic value."

**The aggregation of B-12 to B-15.** Of the −14.80% it claims, **−8.47% is real** (the provision, accepted) and the remainder decomposes into: pledged cash double-deducted (−2.47%, error), book equity double-deducted (−2.84%, error), lens-3 cash deleted (−3.81%, error), NCI at carrying amount (+1.35%, rejected, and it offsets). **Price — the defensible correction from this document is EGP −0.6064, −8.47%, to a central of 6.5572, not 6.10.** **Bucket: ACCEPT the 8.47%, REJECT the remaining 6.33%.**

### B-17. "The extraction of granular, note-level data—such as the 90.7% raw materials cost stack, the specific 8-product slate revenue decomposition, and the exact 4.645% NCI ratio—is highly accurate and strictly tied to the audited base year… the explicit translation of Revenue to Gross Profit, down to EBITDA, and ultimately to unlevered Free Cash Flow to the Firm is mathematically pristine… sliding the discount rate from a highly distressed explicit window (31.6%) to a normalized terminal rate (16.5%) using the cost-of-debt path as a cumulative glide factor is mechanically sophisticated and robust."

**A clearance on the operating build and the discount-rate architecture.** Matches `audited.cost_share['raw']` 0.90692, the eight lines of note 14-A, and `nci_share` 0.046446. **Price EGP 0.0000. Bucket: no action.** Recorded with the same caveat as A-11: this clears the *published* build, not the standing gates on the nine-sheet audited workbook, which I have not yet rebuilt.

### B-18. "Cash & Equivalents (mn EGP) | 2,463.52 | 2,463.52 | Audited Financials | 0.00%"

**A clearance that refutes the same document's B-7.** Recorded as its own row because it is the receipt that decides B-7, and because a register that folded it into B-7 would hide the contradiction rather than arbitrate it. **Price EGP 0.0000. Bucket: no action.**

---

**§B running total:** one finding accepted (B-8, the same as A-1, −8.47%, not additive), two fixes accepted in reworked form (B-10 separation +1.22%, B-6 consistency via A-4 −0.55%), one promotion to the summary page (B-4, rating basis −3.21% shown as an alternative), one research item (B-5), three rejections with receipts carrying −9.12% of arithmetic error between them (B-7, B-14, B-15), and six clearances.

---

## §C — Claude Code ("Fail Table", 43 numbered findings F1–F43, plus a reconciliation appendix)

**This is the most rigorous of the four.** It re-implemented the formula graph independently before comparing, reproduced 41 of 44 lines to the last decimal, and every one of its DCF-lens prices that I re-ran reproduced **exactly** — 5.26, 6.13, 6.48, 5.76, 6.71, 6.88, 4.94, 7.78, 7.0805%, 6.239%, 7.598%. It also has one systematic error that runs consistently in the direction of understating its own case: **it propagates its corrections into the DCF lens but not into the normalised-earnings lens**, so its weighted centrals are too close to the published figure on every finding, in both directions. Where I quote a weighted number below it is my own full re-run of all four lenses, and I flag each place it differs from theirs.

### C-F1. "Revenue engine base = 6M tonnes ×2 × 6M realisation = 41,471.5mn. Cost engine base = 9M COS ×4/3 = 38,535.1mn. Implied opening GM = 1−38,535.1/41,471.5 = 7.0805% — neither the filed 6M 6.14% nor the base-year 7.506%… Two different annualisations applied to the two sides of the same margin ratio."

**Premise — VERIFIED to four decimal places, and it is the largest defect found by anyone.** `build()` at `compute.py:637` sets `base_t = tot_t * 2 / 1e6` and `v = PT[k] * 2.0 / 1e6 * vidx[k]` — the volume base is the note 14-A **six-month** tonnage doubled, priced at the six-month realisation. Three lines earlier, `_cos0 = cogs9 / M * A` sets the cost level from the **nine months** scaled by four thirds. The two sides of the gross margin are annualised from different periods. Summing the eight lines gives an engine base revenue of **41,471.5mn** against `BASE_REV` of 41,662.0mn, and 1 − 38,535.1/41,471.5 = **7.0805%**, the reviewer's figure exactly. Meanwhile the study's own text states the 4/3 scaling "is the only step between the filings and the base year", which is true of the cost side and false of the revenue side.

**Price — the two internally consistent bases span EGP 5.5853 to EGP 7.9347, −22.0% to +10.8%, a range of EGP 2.35 a share or 32.8% of the published central.** Far **above** the 5% line — escalated. The reviewer's DCF prices reproduce exactly (7.7827 against their 7.78; 4.9413 against their 4.94; 2026E margins 7.5980% and 6.2387% against their 7.598% and 6.239%) but their weighted centrals of 7.58 and 6.30 both understate: a full four-lens re-run gives **7.9347** and **5.5853**.

**Re-derivation (step 6) — which basis is correct, decided on the filings and not on preference.**
1. *What does note 14-A actually disclose?* Eight product lines with tonnes and values, **for the six-month transition period only**. There is no nine-month product table anywhere in the four filings. So the six-month table is the only source for the **mix** and the only source for **realisation per tonne**.
2. *What is the base year everywhere else?* Nine months. Operating expense, depreciation, capex, the effective tax rate, working-capital intensity and profit after tax are all struck on `rev9`/`gp9`/`cogs9` × 4/3. The revenue engine is the sole exception.
3. *The model already knows the right answer and states it in a comment.* `compute.py:630-632`: *"The disclosed note 15-A composition is a SHARE structure; the LEVEL is set by the nine-month base so the first forecast year joins the audited base year continuously instead of stepping down to the transition half's own margin."* That is precisely the correct treatment — take the **mix** from the six-month note, take the **level** from the nine-month base — and it was applied to the cost side and **not** to the revenue side. This is not a judgement call I got wrong; it is the same principle applied once instead of twice.
4. *So Option A.* Scale the eight-line product table to the nine-month revenue level, preserving the disclosed mix and realisation structure, and leave the cost level where it is. The base gross margin then becomes 7.5055% — the actual nine-month audited-and-reviewed ratio — instead of an artefact 7.0805% that corresponds to no filed period. Option B (both sides on the six-month half) is wrong because it discards the Q1-2026 quarter entirely, and the Q1-2026 quarter is the reason the nine-month base exists.
5. *Consequence.* Central **EGP 7.9347**, +10.8%. This is one of only three findings across all four files that raises the valuation, and it is the largest single move in either direction.

**Conclusion — ACCEPTED in full, on Option A, at a magnitude larger than the reviewer computed.** **Bucket: ACCEPT.**

### C-F2. "AMOC's board approved a capital-expenditure budget of ~EGP 580.19mn for FY2025/26, disclosed to the EGX (Dec-2025 board meeting, after Audit & Governance Committee review)… a board-approved, exchange-disclosed capex budget — 4.6× the annualised cash run rate, 3.9× depreciation — bearing directly on the assumption the study itself calls decisive, was not swept and is nowhere mentioned."

**Premise — UNVERIFIABLE from this environment, and that is a problem I own rather than a defence.** The EGX disclosure feed, Mubasher and the company's IR site are all egress-blocked at the proxy (403 on CONNECT); the bibliography records seven such negative results. I cannot open the disclosure. But the reviewer reached it, and a board-approved capital budget disclosed to the exchange before the study date is exactly the class of document my own protocol requires me to sweep. **The sweep did not happen, and "the proxy blocked me" does not excuse not saying so on the face of the study.**

**Price — EGP −0.8265 on the weighted central, −11.54%, to EGP 6.3371** (`CAPEX_ANN = 580.19` inflating; DCF lens **5.2604**, matching the reviewer's 5.26 exactly). Their weighted 6.45 (−10.0%) again understates. **Above the 5% line.**

**Conclusion — DEFECT ACCEPTED, the number RESEARCH.** The defect — a decisive assumption held at the cash run rate without sweeping the exchange disclosures — is accepted unreservedly. The 580.19mn itself I cannot confirm, and a −11.54% adjustment may not be published on a figure I have not read. **Bucket: RESEARCH, with an ACCEPTED disclosure change**: state on the face of the study that forward capex is held at the cash run rate, that a board capital budget may exist and was not reachable, and publish the 580.19mn case as a priced scenario labelled unverified.

### C-F3. "Board-approved revised FY2026 budget: sales 44,888mn, gross profit 3,428mn, operating profit 2,081mn, NPAT ~2,099mn (revised up from 1,024mn)… the study's EBIT is 28.3% below the company's own operating-profit budget."

**Premise — UNVERIFIABLE from here, same egress block, same accepted process defect as C-F2.** **Price — EGP +1.1947 weighted, +16.68%, to EGP 8.3583** (operating expense scaled to the guidance-implied 1,347mn; DCF lens 8.3169 against the reviewer's 9.18, the one place their DCF price and mine diverge materially — they scaled the whole EBIT path, I scaled the line the divergence actually sits in). **Above the 5% line, and it runs upward.** **Bucket: RESEARCH**, same disclosure change as C-F2. Recorded prominently because it is evidence against the reading that this critique is uniformly bearish: its second and third headline findings point in opposite directions by 28 percentage points.

### C-F4. "EGP 67,467,871 in the half = 134.9mn/yr. Cell C23 is referenced by zero formulas… The item is identified, priced, flagged as previously missed — and then still not modelled."

**Premise — VERIFIED.** `V['emp_h2_25']` appears **zero times** in the model body after the input registry. Its own source note reads *"A real distribution out of profit that the previous edition of this study did not model at all"* — and this edition does not model it either. **Price — EGP −0.5876 weighted, −8.20%, to EGP 6.5760** (DCF lens **6.1312**, matching the reviewer's 6.13 exactly; their weighted 6.84 understates by 3.7pp). **Above the 5% line.** **Conclusion — ACCEPTED.** Employees' profit share and board bonuses are a contractual distribution out of profit before the shareholder sees it; it must be charged in the waterfall and in normalised EPS. **Bucket: ACCEPT.**

### C-F5. "10.3% + 0.0% + 37.1% + 40.1% + 15.9% | Sum = 103.4%. Zone 'EGP 7.50 – 7.16' is inverted (7.16 < 7.50) and reports 0.0%; the 7.16–7.50 band is double-counted."

**Premise — VERIFIED by addition; the zones do not partition.** **Price — EGP 0.0000 on fair value; every zone probability in the table is misstated.** **Conclusion — ACCEPTED.** Bins must tile. **Bucket: ACCEPT** the reviewer's partition: <7.16 = 6.9%, 7.16–7.50 = 3.4%, 7.50–9.10 = 33.7%, 9.10–11.00 = 40.1%, >11.00 = 15.9%.

### C-F6. "The published row is non-monotonic (rises from 6.85 to 7.32 as NWC intensity increases), its endpoints are wrong by up to +0.97 (+12.8%), and its centre does not correspond to the model's actual 4.162%."

**Premise — SPLIT, and the split matters.** The non-monotonicity is **real** and the cause is simpler than diagnosed: the published grid is `[0.0, 0.01, 0.0416243, 0.03, 0.05]` — **the x-axis is not sorted**. The base ratio was inserted in the middle position rather than in value order, so the row reads out of sequence. The **values are all correct**: re-running the engine gives 0% → 8.5225, 5% → 6.5156, base 4.1624% → 6.8518, every one matching the published cell.

The "endpoints are wrong by up to +0.97" claim is **REJECTED with receipts**. The reviewer's own recomputed row (7.55 / 7.34 / 7.13 / 6.92 / 6.71) spans 0.84 across 0–5% where a full re-run spans 2.01, while their centre at 4.162% matches mine exactly at 6.85. A re-implementation that agrees at the centre and disagrees at both ends has not propagated the change in invested capital into the terminal block. Mine does; `dcf_scenario(nwc_p=·)` returns 8.5225 / 8.0208 / 7.5191 / 7.0174 / 6.5156 on their own grid — strictly monotone, and the endpoints are the published ones.

**Price — EGP 0.0000 on the headline; the defect is a sorting error in a published table.** **Bucket: ACCEPT the sort fix, REJECT the endpoint claim with receipts.**

### C-F7. "Carry alone… = +0.02348 → median 9.316 (reported 9.33)… Carry less half-variance = +0.0026 → median 9.12. The stated number is the carry with no half-variance deduction; if the stated formula were applied the 3M median would be 9.12, not 9.33."

**Premise — VERIFIED.** The prose describes a half-variance deduction the number does not contain. **Price — EGP 0.0000 on the fundamental; −2.2% on the cone median if the prose were taken literally, flowing into every probability in the cone tables.** **Conclusion — ACCEPTED.** The engine's carry is `ln(1+rf) − ln(1+q)` and the prose should say so. **Bucket: ACCEPT** the wording fix.

### C-F8. "The study's own Table 13 shows reinvestment −6.9%, +12.7%, −10.5%, +4.9% — positive in two of four periods. Implied growth −1.9/+2.8/−2.6/+3.2%, average +0.375% — positive."

**Premise — VERIFIED against `terminal_recon`:** reinvestment −0.0687 / +0.1267 / −0.1051 / +0.0487, implied growth −0.0193 / +0.0282 / −0.0262 / +0.0321, mean **+0.37%**. The study says reinvestment is "NEGATIVE in every audited period" and calls +0.4% "shrinking its capital base". Both are contradicted by the table printed beside them. **Price — EGP 0.0000 arithmetically; it misstates the direction of the study's self-declared sharpest weakness.** **Conclusion — ACCEPTED.** **Bucket: ACCEPT.** Note this also partly refutes §A-3 and §B-9: the reinvestment record is not uniformly negative, and two other reviewers built a "shrinking asset base" argument on my own incorrect sentence rather than on my own correct table.

### C-F9. "Model capex/depreciation by year: 0.99 / 1.11 / 1.24 / 1.37 / 1.50… the caveat's premise that the model 'carries the 0.86× forward' is false… The stated concession understates the real correction by ~250×."

**Premise — VERIFIED exactly** (0.986 / 1.114 / 1.242 / 1.366 / 1.496). The study's stated concession — "free cash flow in the explicit window is overstated by roughly EGP 2mn a year", printed twice — holds only for 2026 and reverses sign from 2027. **Price — EGP 0.0000 as a standalone; the real correction is C-F2's −11.54% if the board budget is confirmed.** **Conclusion — ACCEPTED.** **Bucket: ACCEPT.** This is also the receipt that settles §A-3 and §B-9 against those reviewers: the capex path rises to 1.50× depreciation and the asset base grows.

### C-F10. "engine/Cost_of_Capital_Reference.md is absent from the repository… The only Egypt 10Y figure cached anywhere in the repo is 22.55%."

**Premise — VERIFIED.** The cited file does not exist; `ls` returns no such file. A citation to a non-existent document is a citation failure of the first order, whatever the number turns out to be. **Price — EGP −0.0284 weighted (−0.40%) at 22.55%; total on the citation plane.** **Conclusion — ACCEPTED without qualification.** **Bucket: ACCEPT.** This is the row that decides §A-6 and §B-5 as well: three reviewers questioned the risk-free rate, and the reason none of us can settle it is that the source I cited is not there to check.

### C-F11. "2.47mn (6M) + 30.0mn + 20.3mn (Q1) = 52.8mn over 9M = 70.4mn/yr. All three cells referenced by zero formulas… Disclosed, recurring-in-practice charges recorded and then excluded from the forecast with no stated reason."

**Premise — VERIFIED for the forecast.** The three inputs are each referenced once, in the historical reconstruction of the filed periods, and **not once** in the forward build. **Price — EGP −0.3065 weighted, −4.28%** (DCF lens **6.4759**, matching their 6.48 exactly). With C-F4 together: **EGP −0.8941, −12.48%, to EGP 6.2695** (DCF 5.7554 against their 5.76, exact). **Conclusion — ACCEPTED**; formed provisions and expected credit losses have appeared in every filed period and belong in the run rate. **Bucket: ACCEPT.**

### C-F12. "An equal-weight basket of the analyst's own coverage list is not the local market index and is not investable or published; it is an artifact of which names happen to be covered."

**Premise — correct as stated; the conclusion is a methodology dispute I cannot settle from here.** **Price — UNVERIFIABLE without an EGX30 regression; the grid span is EGP 8.24 → 6.01 on the DCF lens across beta 0.60–1.30, and beta 1.15 alone is EGP −0.4003 weighted (−5.59%), above the 5% line.** **Bucket: RESEARCH.** Run the EGX30 regression and publish both. Recorded as above the line because the *parameter* is, even though the *finding* is unresolved.

### C-F13. "EV = 9.10×1,291.5mn + (−2,442.5mn) = 9,310mn. Base-year EBITDA = 1,653mn. 9,310/1,653 = 5.63×. The stated trailing multiple is wrong; 4.5× is a 20% de-rating, not a hold, so the lens's entire stated justification is false."

**Premise — VERIFIED, and the model itself already computes the right number.** `rel.ev_ebitda_trailing` = **5.6315**. The study text says "around 4.6x". The model's own output contradicts the study's own sentence. **Price — EGP +0.1770 weighted, +2.47%, to EGP 7.3406** at 5.6315× (matching their "weighted 7.34 (+2.5%)" exactly — the one weighted figure of theirs that reproduces, because this lens is the only one it touches). **Conclusion — ACCEPTED.** The 4.5× may still be the right multiple, but it must be justified as a de-rating, not described as a hold. **Bucket: ACCEPT** the correction of the stated trailing multiple; the choice of 4.5× versus 5.63× then becomes **YOURS**, priced at +2.47%, and my recommendation is to keep 4.5× and state plainly that it is a 20% de-rating for the administered-margin and state-counterparty risk.

### C-F14. "The published centre (6.93) is above the base case (6.85) at a beta (0.95) above the base beta — directionally impossible."

**Premise — VERIFIED.** `grid_beta[2]` = 6.9312 at beta 0.9405, against a base DCF of 6.8518. A sensitivity row whose centre does not reproduce the base case is broken. **Price — EGP 0.0000 on the headline; the row is unusable.** **Bucket: ACCEPT** — rebuild the row from full re-runs, and add a gate asserting that every sensitivity row reproduces the base at its base point. That gate did not exist and would have caught this, C-F6 and C-F15 at once.

### C-F15. "At zero volume growth: 2.572. The other four points reproduce exactly. 2.76 corresponds to ≈0.05× the path, not zero."

**Premise — REJECTED with receipts.** `dcf_scenario(vol_mult=0.0)` returns **2.7647**, the published value, to four decimals. `vol_mult` scales the *growth rates*, so 0.0 holds volume flat at the base level; it does not zero volume. The published number is correct for the scenario the model runs. **The real defect is the label**: "zero to double" reads as a volume range when it is a growth-path multiplier, and that ambiguity is what produced this finding. **Price — EGP 0.0000.** **Bucket: REJECT the number, ACCEPT the relabelling.**

### C-F16. "Itemised assets = 8,059.2mn (gap 77.3mn); itemised liabilities = 2,994.8mn (gap 316.8mn)… Presented as a footing table that does not foot."

**Premise — ACCEPTED**; the reviewer also confirms the totals themselves close to zero. **Price — EGP 0.0000; ~0.3 a share of balances left unexamined.** **Bucket: ACCEPT** — add an "other" residual line. This also matches my own pre-critique self-audit item on Appendix A.2.

### C-F17. "Base-year P&L runs to 31-Mar-2026; net debt, NWC, invested capital and book value all taken at 31-Dec-2025… struck four months apart with no disclosure; net cash alone is 1.89/share (28% of fair value)."

**Premise — VERIFIED.** Every balance-sheet input carries `2025-12-31`; the P&L runs to 31-Mar-2026. **Price — the reviewer estimates ~−0.03 a share on the visible items and leaves working capital unquantified; I accept that as the best available number and record the working-capital leg as unpriced.** **Conclusion — ACCEPTED as a disclosure defect.** **Bucket: ACCEPT** — disclose the mismatch explicitly, and where the reviewed 31-Mar-2026 balance sheet supports it, restate the bridge at the base-year date.

### C-F18. "4.6446% is a computed ratio from one half-year… Q1-2026 gives 3.563%; the 9-month blend consistent with the base year is 4.113%… A single-period ratio labelled 'disclosed'."

**Premise — VERIFIED.** The study calls the rate "the DISCLOSED 4.645%"; it is computed from one half-year, 30,488,250 / 656,428,711. **Price — EGP +0.0272 weighted, +0.38%** at 4.113% (DCF **6.8795**, their 6.88, exact). **Conclusion — ACCEPTED on the word "disclosed" and on the period basis.** **Bucket: ACCEPT** — blend over the nine-month base year and stop calling a computed ratio disclosed. This finding also sharpens the §A-4 / §B-6 arbitration: all three reviewers found the NCI treatment, and this is the one that identifies the actual mechanical error.

### C-F19. "the explicit window's own 2030 net reinvestment = 18.25%… Terminal FCFF 1,274mn vs 2030 explicit FCFF 1,156mn = +10.3% step-up. The terminal block assumes less reinvestment than the final explicit year."

**Premise — VERIFIED exactly** (18.253% against a terminal 14.141%). **Price — EGP −0.0627 weighted, −0.88%** (DCF lens **6.7124**, their 6.71, exact). **Conclusion — ACCEPTED as an undisclosed discontinuity.** **Bucket: ACCEPT the disclosure**; the step is a legitimate consequence of the steady-state identity, but a reader is entitled to see that terminal free cash flow steps up 10.3% over the last explicit year.

### C-F20. "TV = 11,039.7mn ✓; but 58.7% is PV(TV)/EV = 3,942.1/6,718.6. 11,039.7/6,718.6 = 164.3%. Two different objects joined in one clause."

**Premise — VERIFIED.** **Price — EGP 0.0000.** **Bucket: ACCEPT** the rewording.

### C-F21. "Table 3: capex 'about EGP 604mn a year'; depreciation 'about EGP 458mn a year' | Model source notes: 'about 649mn in the first forecast year' and 'about 440mn a year'."

**Premise — ACCEPTED**; the reviewer establishes that the report is the internally consistent one (1.45% × 41,662 = 604.1; 1.1% × 41,662 = 458.3). **Price — EGP 0.0000.** **Bucket: ACCEPT** — reconcile the model's source notes to the report.

### C-F22. "Statements!B10/C10 are blank for those periods; no opex, capex, depreciation or invested-capital input exists for 2024/2025 anywhere on Assumptions… Published figures with no support in the delivered model."

**Premise — ACCEPTED**, and the reviewer is scrupulous enough to record that the two later columns of the same table do reproduce and that the P33 growth rates reconcile to within 1.6mn on an 18,246mn base. **Price — EGP 0.0000 directly; it removes the audit trail from the volume ranking at C-F25, which is the widest sensitivity in the model.** **Bucket: ACCEPT** — carry every published historical line as a sourced input.

### C-F23. "Source note: multiple applied 'on mid-cycle 2028E EBITDA' | Formula reads Forecast!C39 = 2027E."

**Premise — VERIFIED** (`REL_I = 1`, 2027E). **Price — EGP 0.0000** (report text and formula agree; only the source note is wrong). **Bucket: ACCEPT** the note correction.

### C-F24. "Attributable annualised EPS = 1.2785 → P/E 7.12× (6.83× on group profit; 10.2× after the note-16 employees' share). Overstated, and the framing is single when three legitimate bases exist."

**Premise — VERIFIED**; `rel.pe_trailing` = **7.1175** against a stated "about 7.5x". **Price — EGP 0.0000 as published**; the 10.2× basis is a consequence of C-F4 and is priced there. **Bucket: ACCEPT** — state the basis alongside the figure.

### C-F25. "Measured value growth ranking: HFO +60.7% > fuel oil +29.1% > wax +21.3%… Assumed volume ranking: wax 7.0% > base oils 4.5% > fuel oil 3.0%… a value-growth record is used to rank volume growth, which mixes price into a volume driver."

**Premise — VERIFIED against `unit.growth_v` and `line_vol_growth`; the rankings do not match and the study says they do.** **Price — no direct price; volume is the model's widest single sensitivity, EGP 2.76 to 11.76 on the DCF lens across the published grid.** **Conclusion — ACCEPTED.** Ranking volume growth off a value-growth record is a category error, and note 14-A discloses tonnes as well as values, so the decomposition is available and was not done. **Bucket: ACCEPT** — decompose the record into volume and price and re-rank on volume.

### C-F26. "One 'Egyptian inflation factor' applied to salaries and to 'natural gas, electricity, water, spare parts, maintenance, EPROM contract'… the entire FX path is defined and unused, while feedstock and gas are world-priced/administered."

**Premise — SPLIT.** The single-escalator criticism is **accepted**: one domestic-CPI factor across physically distinct cost drivers, with energy escalated on domestic inflation, is not defensible. The "FX path referenced by zero formulas" claim is **rejected for the model** — `V['fx_path']` is referenced twice in `compute.py`, in the currency-of-discounting alternative — though the reviewer is describing the *workbook*, where it may well be inert, and I have not yet rebuilt the standing gates on the nine-sheet file to check. **Price — the reviewer's own bound, confined to the 8.7% of cost of sales that is not pass-through, so second-order; no separate number.** **Bucket: ACCEPT** one escalator per driver class; **RESEARCH** the workbook-level orphan claim pending the gate rebuild.

### C-F27. "Referenced by zero formulas. It is also incoherent with the study's own terminal build: terminal rf 10.5% = '5% inflation target + ~5.5% real', so 15% nominal growth would imply ~10% real growth in perpetuity."

**Premise — the incoherence is VERIFIED and is the better half of the finding.** **Price — EGP 0.0000** (unused; the adopted g of 5% is well inside any of these ceilings). **Bucket: ACCEPT** — delete the 15% or restate it consistently with the terminal inflation assumption.

### C-F28. "Rating-basis inputs sit in the model unused. Recomputed rating-basis: Ke = 29.05%, WACC = 33.21% → DCF 6.73. No USD/real cross-check is run."

**Premise — PARTLY REJECTED with receipts.** The rating basis is **not unused**: `wacc_exp_rating` = 32.177%, `wacc_term_rating` = 20.352% and `ps_rating_basis` = **EGP 5.8434** are all computed and emitted, and the currency-of-discounting cross-check the reviewer says is absent is computed too, at `ccy_alt_ps` = **EGP 7.2093**, discounting the export leg in dollars at 10.72%. Both are in the model and neither is prominent enough in the study for a careful reader to find, which is the real defect. Their recomputed 33.21% differs from my 32.18% because they glide the terminal differently. **Price — EGP −0.2299 weighted (−3.21%) on the rating basis, as at §B-4.** **Bucket: DEFECT-NO-FIX** — the computations exist; promote both to the summary page.

### C-F29. "A July-2026 Damodaran country-premium update exists and pre-dates the study… the implied mature ERP is consistent with the newer file, leaving the stated 05-Jan-2026 date in doubt."

**Premise — the internal check is elegant and I accept it**: both my pairs imply the same ~4.20% mature-market premium and the same ~1.53 relative-volatility multiplier, which is a genuine coherence test of my own two columns against each other. The vintage claim is **UNVERIFIABLE** — `pages.stern.nyu.edu` is egress-blocked for both of us. **Price — small, direction unknown until the Egypt row is read.** **Bucket: RESEARCH.**

### C-F30. "AMOC pays an annual DPS of EGP 0.80 (0.80/9.10 = 8.791% ✓). But neither audited document states the DPS… and the study's own filed cash dividends paid (736.6mn + 603.0mn = 1,339.5mn over 9M = EGP 1.38/share annualised, 15.2%) sit unreconciled beside it — while §7 claims 'the dividend… is read off a filing'."

**Premise — VERIFIED, and this is the sharpest citation finding in the file.** The value is right, the sourcing claim is false, and the study's own cash-flow data disagrees with it by 6.4 percentage points of yield. **Price — the value as used is correct; at the filed 15.2% the 3M cone median falls to 9.19, −1.5%.** **Bucket: ACCEPT** — state the DPS, its declaration date, and reconcile declared against paid.

### C-F31. "488 formula cells, 0 with cached values — the file has never been recalculated and saved by a spreadsheet engine."

**Premise — REJECTED with receipts.** Reading the delivered workbook directly out of its own zip container: **488 formula cells, 488 with cached values** (`</f><v>` pairs), across 9 sheets. The cached values were injected by post-save XML rewrite and verified on the saved file. Either the reviewer received a stripped copy or their reader did not follow the `</f><v>` encoding. **Price — EGP 0.0000** (the reviewer records no value impact either). **Bucket: REJECT.**

### C-F32. "Iterating the weights to the model's own fair value (6.85 × 1,291.5mn) gives net-debt weight −38.1%, WACC 33.3%, DCF 6.71… The discount rate is weighted on a price the study concludes is 21% too high."

**Premise — VERIFIED, and the circularity is real and undisclosed.** **Price — EGP −0.0768 weighted, −1.07%, to EGP 7.0868** (DCF **6.7225**, their 6.71). **Conclusion — ACCEPTED as a disclosure defect, the fix is YOURS.** Iterating to convergence is defensible; so is using observable market weights and saying so. With a negative debt weight the iteration is self-reinforcing, which argues for disclosing the spot-based choice rather than iterating into it. **Bucket: YOURS**, priced at −1.07%; **my recommendation is to keep the spot-based weights and disclose the circularity in one sentence**, because a rate weighted on a price you are arguing against is at least an observable input, whereas the iterated version is an output of the thing being computed.

### C-F33. "Cell referenced by zero formulas. The bridge has no line for investments or associates… A dividend-paying equity stake outside the operating EV is excluded from the bridge and never named."

**Premise — VERIFIED**; `fvoci` is referenced zero times and the bridge carries no investments line. **Price — the reviewer's estimate is ~+0.17 a share (+2.4%) at 8×; the disclosed carrying amount of 69.6mn is +0.054 a share.** **Conclusion — ACCEPTED**; a non-operating asset that pays a dividend of 13.52mn belongs in the bridge. **Bucket: ACCEPT** at the disclosed carrying amount, with the 8× earnings-based figure shown as an alternative.

### C-F34. "House template requires a 16-section Word document, 16-sheet Excel, a three-expert appendix and a six-clause disclaimer. Delivered: 7 sections + 1 appendix, 9 sheets, no expert appendix… three-clause closing box."

**Premise — VERIFIED, and it is the same finding as my own pre-critique self-audit.** The audited rebuild lost roughly twelve pages and whole sections against the template the previous edition met. **Price — EGP 0.0000.** **Bucket: ACCEPT** — restore the template.

### C-F35. "No moving-average value, slope, cross state, RSI, MACD, ATR or support/resistance level is quantified anywhere in the study; §2's only content is data-cleanliness prose."

**Premise — VERIFIED.** A four-indicator chart asserted with no computable figure in the text. **Price — EGP 0.0000.** **Bucket: ACCEPT** — state the computed levels or drop the claim.

### C-F36. "The live site record for AMOC carries fair: { bear: 3.83, base: 9.38, full: 18.12 }… while linking AMOC_Valuation_Study_06-08-2026_public.docx and stamping asof.mc.computed 2026-08-06."

**Premise — VERIFIED and outstanding.** The published site still carries the superseded EGP 9.38 and a "roughly fairly valued" reading against a study that concludes EGP 7.16 and a −21.3% discount. A reader of the site sees +3% against spot. **Price — EGP 0.0000 inside the documents; the entire published conclusion outside them.** **Bucket: ACCEPT — highest operational priority.** This is the one finding in all four files where the defect is live in front of the public right now, and it must be fixed in the same pass as the numbers.

### C-F37. "it is derived on a pre-tax base that includes ~316mn of credit interest and other income (items excluded from EBIT) and is flattered by a 19.4mn deferred credit; it is then applied to EBIT and into perpetuity."

**Premise — VERIFIED.** The rate is right for its own base (366,807,706 / 1,658,355,952 = 22.1188%) and is then applied to a narrower base. I also record, against myself, that the registered `tax_eff` input is **dead** — `price.py '{"tax_eff": 0.225}'` returns the published central unchanged, because `TAX = TAX_EFF` is derived. **Price — EGP −0.0287 weighted (−0.40%) at the statutory 22.5%.** **Bucket: ACCEPT** — use the statutory rate on EBIT for the unlevered waterfall and keep the effective rate for the historical reconciliation only.

### C-F38 to C-F43 (six UNVERIFIABLE rows). **Recorded individually, none dismissed.**
- **C-F38** note-level statement items: the reviewer could not read the filings (egress-blocked) and corroborated eight headline figures against press reporting instead — H2-2025 revenue 20.74bn, NPAT 656.4mn, Q1-2026 revenue 10.51bn, NPAT 635.12mn, comparative 10.07bn, APC ~20.8%, wax subsidiary 86.45%, DPS 0.80, share capital 1,291,500,000, all matching. **I read the four filings visually, page by page, and `filings/AUDITED_EXTRACT.md` is the note-by-note record.** **Price EGP 0.0000. Bucket: no action**, with the extract offered as the resolution.
- **C-F39** Damodaran Egypt row: unreachable for both of us; internally coherent on the two-pair test. **Bucket: RESEARCH.**
- **C-F40** Egypt 10Y at 21-Jul-2026: unreachable; repo cache disagrees at 22.55%. **Priced at −0.40%. Bucket: RESEARCH**, and see C-F10 for the citation failure underneath it.
- **C-F41** bear and bull columns: **ACCEPTED as a real defect.** The five driver sets are stated in `SCEN` in the model but not in the delivered study, and the weighted "range" is `MIN`/`MAX` of the DCF lens's own extremes rather than a weighted envelope — the reviewer is right that a 6.2× headline span is untestable as published, and §A's independent complaint about the range rests on the same gap. **Price EGP 0.0000 on the central; it sets the entire published range. Bucket: ACCEPT** — publish the driver sets and express the range as a weighted envelope.
- **C-F42** anchor volatilities: match the repo ledger exactly but are engine outputs not re-derivable from the delivered files. **Bucket: no action**, with the fit output offered.
- **C-F43** the "about 12%" net effect of the superseded edition's errors: not reproducible because the superseded build is not supplied. **Bucket: RESEARCH** — supply the superseded workbook or drop the claim.

---

**§C running total.** Accepted and material: C-F1 **+10.8%**, C-F4 **−8.20%**, C-F11 **−4.28%**, C-F13 **+2.47%**, C-F18 +0.38%, C-F19 −0.88%, C-F32 −1.07% (recommended as disclosure only), C-F37 −0.40%. Research, priced but not adopted: C-F2 **−11.54%**, C-F3 **+16.68%**, C-F12 −5.59% at beta 1.15. Rejected with receipts: C-F6's endpoint claim, C-F15, C-F31, and half of C-F26 and C-F28. Accepted with no price: C-F5, C-F7, C-F8, C-F9, C-F10, C-F14, C-F16, C-F17, C-F20 to C-F25, C-F27, C-F30, C-F33 to C-F36, C-F41.

---

## §D — Claude Cowork ("Forensic Valuation Audit", 33 numbered findings, 104 passes)

**Unlike §C, this reviewer propagates every correction through all four lenses**, and every weighted figure of theirs that I re-ran reproduces to two decimals — 6.28, 6.77, 6.64, 6.65, 6.48, 4.04–11.51, 5.404%. Where I disagree below it is on method, not on their arithmetic. Their reconciliation appendix is the most complete of the four: ~62 lines recomputed from the Assumptions sheet alone, all reproducing, plus three independent structural passes the others did not run (the cash-adjusted WACC identity, the Damodaran double-count check, and the D&A add-back double-count check).

### D-1. "AMOC disclosed 1 Jan–30 Jun 2026 results to the EGX on 29–30 July 2026, one week before the report's own anchor date: revenue EGP 26,223mn, gross profit EGP 3,258mn, NPAT EGP 1,903mn… Adding it to the audited transition half gives a clean contiguous twelve months to 30-Jun-2026… which dissolves the stated reason for annualising nine months."

**Fully re-derived under step 6 before any other finding was read; the derivation is appended to `SELF_AUDIT_pre_critique.md` and is summarised here.**

**Premise — ACCEPTED, and worse than the reviewer knew.** `rev_h1cy26_rep` (26,200) and `pat_h1cy26_rep` (1,900) were **live registered inputs** at commit `2e54245`. The audited rebuild **deleted them**, on a rule that treated "is it inside one of the four PDFs?" as the test for whether a figure could be used — after which §1.2 argues that no clean twelve-month period exists. The rule deleted a disclosure the previous edition had already sourced and corroborated. That is a process defect, recorded as such.

**Three coherence tests, run before judging:**
1. *Profit.* H1-2026 group profit 1,903 → 1,815 majority at the disclosed 4.645% NCI, against 1,837 implied by "+109%" on the Jan–Jun 2025 majority profit of 878.8 read off the **audited** equity statement. **Match within 1.2% — CONFIRMS the press profit.**
2. *Revenue.* 26,223 at +35.2% implies Jan–Jun 2025 revenue of 19,396; plus audited Jul–Dec 2024 of 18,246 gives a twelve-month figure of 37,642 against 37,507 triangulated independently. **Match within 0.4% — CONFIRMS the press revenue.**
3. *Gross profit.* Run the press GP of 3,258 through Q1-2026's own expense run rates: EBIT 2,402 → PBT 2,751 → PAT **2,142** against a claimed 1,903, i.e. **+12.6% too high**. A GP of **2,943** gives PAT 1,897, within 0.3%. **REFUTES the press gross profit**; the coherent H1-2026 GP is ~2,943, putting Q2-2026 at ~12.0%, not the 13.92% the reviewer's summary implies.

**Price — PUBLISHED base EBIT 1,506 · reviewer's basis 2,888 (+91.8%, central ~13.74) · coherence-tested basis 2,573 (+70.9%, central ~12.24).** Far above the 5% line and the second-largest move in the exercise after C-F1, in the same upward direction.

**Conclusion — PREMISE ACCEPTED, CONCLUSION ACCEPTED IN DIRECTION, REJECTED IN MAGNITUDE, with receipts.** **Bucket: ACCEPT**, implemented on the coherence-tested base: rebase on the twelve months to 30-Jun-2026 using revenue 46,959 as reported and gross profit **solved from the release's own profit**, flag the H1-2026 half as REPORTED and not audited, and sensitise between the nine-month annualisation and the twelve-month TTM.

### D-2. "Volumes are `'Product and Cost'!B6 * 2 * (1+g)` — the six-month table doubled (implied revenue base 41,471.5mn). Cost of sales is `(D35−D37) * 4/3`… The engine's implied base-year margin is 7.081%."

**The same finding as C-F1, found independently, with the same numbers and the correct weighted propagation.** Their "2026E EBIT 1,491 → 1,706 (+14.4%); DCF 7.78; weighted 7.93 (+10.8%)" matches my re-run of **7.9347 (+10.8%)** — the reviewer got the weighted effect right where §C did not. **Price EGP +0.7711, +10.8%.** **Bucket: ACCEPT**, per the C-F1 re-derivation (Option A: mix from note 14-A, level from the nine months).

### D-3. "8.70 is a 2028 value. Lens 2 in the same report explicitly discounts its forward EV back at the model's own 0.6022 factor; lens 3 discounts nothing. At the model's own year-3 factor 0.4939, lens 3 = EGP 4.30."

**Premise — ACCEPTED, and it is a regression: an earlier edition of this study fixed exactly this defect and the audited rebuild reintroduced it.** The internal inconsistency is real and undeniable — one lens discounts its forward-dated output and the sibling lens does not.

**Price — EGP −0.8806 weighted, −12.29%, to EGP 6.2830** at the reviewer's own factor, reproducing their 4.30 and 6.28 exactly. **Above the 5% line.**

**Conclusion — PREMISE ACCEPTED, the reviewer's FACTOR REJECTED with receipts, and the correct factor priced.** 0.49394 is the **WACC** discount factor — the rate for an unlevered enterprise cash flow. Lens 3 produces an **equity** value from attributable earnings, so the right rate is the cost of equity, not the weighted cost of capital, and using the WACC factor over-discounts a levered claim at an unlevered rate. At Ke of 27.76% over two years the lens is **EGP 5.3305** and the central **6.4896 (−9.41%)**; over the 2.4 years from the 6-Aug-2026 price date to mid-2028 it is **EGP 4.8330** and the central **6.3900 (−10.80%)**.

There is also a live question the reviewer does not raise and I must: a lens called *normalised earnings power* should arguably not be dated at all — the point of normalisation is a through-cycle level, which needs no discounting. If that is the intent, the defect is the label "2028E", not the missing discount. But the model takes every component from `NORM_I = 2`, i.e. specifically 2028, so as built it is a dated number and must be discounted.

**Bucket: ACCEPT** at the cost of equity over the 2.4 years to the mid-point of 2028: **−10.80%**, not the reviewer's −12.29%. The 1.5pp difference between their fix and mine is itself a receipt for why the rate had to be re-derived rather than adopted.

### D-4. "No formula in the workbook reads C23… Annualised ≈ EGP 134.9mn = 7.8% of base-year group profit = EGP 0.104/share/year. The study names the omission as a defect of the prior edition and then repeats it."

**The same finding as C-F4, independently found. Premise VERIFIED** — `V['emp_h2_25']` is referenced zero times in the model body. **Price — EGP −0.5876 weighted, −8.20%** on my full re-run (DCF 6.1312); the reviewer's −5.5% understates here, the one place their propagation is short. **Above the 5% line. Bucket: ACCEPT.**

### D-5. "EV = 9,310.1; base-year EBITDA = 1,653.6. EV/EBITDA = 5.63×. The cited anchor is off by 22%, and it is sourced to 'the constructed 2025 base' — the discarded prior edition. 4.5× is a 20% de-rating, not a hold."

**The same finding as C-F13, and the additional point about the source note tracing to the discarded edition is new and correct.** `rel.ev_ebitda_trailing` = **5.6315**. **Price EGP +0.1770 weighted, +2.47%. Bucket: ACCEPT** the correction of the stated trailing multiple; the 4.5× versus 5.63× choice remains **YOURS**, recommendation as at C-F13 (keep 4.5×, call it a de-rating).

### D-6. "Actual EGP 10-year yield: 22.700% on 21-Jul-2026 and ~22.98–23.00% on 5–6 Aug-2026… The claimed re-verification does not match the market on either stated date; 22.31% is below the entire observed window."

**Premise — UNVERIFIABLE from this environment (403 at the proxy on every rate source), but this is now the third independent reviewer landing above 22.6%, and the second citing 22.98–23.00% for the anchor date.** Combined with C-F10 — the cited house reference file **does not exist in the repository** — I treat the balance of evidence as against 22.31%. **Price — EGP −0.0379 weighted, −0.53%** at 22.98%; their DCF 6.79 against my 6.788. **Bucket: RESEARCH on the number, ACCEPT on the citation** — the "re-verified 06-Aug-2026" claim must be withdrawn or given a source, because the file it points at is not there.

### D-7. "The CBE's 5% (±2) target is dated Q4 2028; the medium-term anchor in force is 7% (±2), for Q4 2026, and the July-2026 MPC pushed even that to H2-2027… IMF projects Egypt CPI at 7.0% through FY2030/31."

**Premise — the strongest single input finding in any of the four files.** The terminal risk-free rate is the most terminal-value-sensitive parameter in the model, terminal value carries 58.7% of enterprise value, and it is built off the *furthest and softest* of two published central-bank targets while being described as "the" medium-term target. The IMF corroboration at 7.0% through FY2030/31 is independent of the CBE and points the same way.

**Price — EGP −0.3922 weighted, −5.48%, to EGP 6.7714** (`rf_term = 12.5%`; DCF lens **6.3234**, their 6.32, exact). **Above the 5% line.**

**Conclusion — ACCEPTED.** I cannot reach the CBE statement or the IMF report from here, but the finding does not depend on egress: it is an internal-consistency failure. A terminal rate built on an inflation target dated Q4-2028 is inconsistent with a terminal *horizon* that begins in 2031, and it is inconsistent with the model's own C130 long-run nominal growth of 15% (see D-21). **Bucket: ACCEPT** — use the target in force for the terminal horizon, publish both, and treat the 5.48% as a disclosed sensitivity rather than a silent choice.

### D-8. "The five zones sum to 103.4%… Table 17 states P(above 7.16) = 93.1% ⇒ P(below 7.16) = 6.9%; Table 18 rows 1–2 imply 10.3% ⇒ 89.7% — a 3.4pp contradiction."

**The same finding as C-F5, with the additional cross-check against Table 17 that identifies the 3.4pp as exactly the double-counted band. Premise VERIFIED by addition. Price EGP 0.0000; invalidates the published probability map. Bucket: ACCEPT.**

### D-9. "Recomputed on the report's own model: 8.52 · 8.02 · 7.52 · 7.02 · 6.52 — exactly linear at −0.40/pp. Endpoints match; three interior cells do not… The base-case answer has been spliced into the middle slot and the remaining points jumbled."

**Premise — VERIFIED, and this reviewer's diagnosis is exactly right where §C's was wrong.** Re-running the engine on their grid gives **8.5225 · 8.0208 · 7.5191 · 7.0174 · 6.5156** — their row to two decimals, strictly monotone, and their reading of the cause ("the base-case answer spliced into the middle slot") is precisely what the unsorted grid `[0.0, 0.01, 0.0416243, 0.03, 0.05]` does. **§C-F6 claimed the endpoints were wrong by up to 0.97; they are not, and this reviewer says so explicitly ("Endpoints match"). Arbitration by coherence test: §D reproduces my endpoints, §C does not. §D wins.** **Price EGP 0.0000 on the headline. Bucket: ACCEPT** — sort the grid, recompute each point, and assert monotonicity as a gate.

### D-10. "The stated formula gives +0.0060. +0.0235 is that expression per annum — or the carry over three months with no half-variance deduction (0.02415)… overstates the drift in every percentile, probability and zone in §3 and §6 by roughly 4×."

**Premise — ACCEPTED as a prose-versus-number contradiction, the "4×" REJECTED with receipts.** §C-F7 diagnoses the same defect and gets closer: the published +0.0235 **is** the carry over three months with no half-variance term, and it reproduces both published medians exactly (3M 9.316 against 9.33; 1M 9.1692 against 9.17, exact). The engine's carry is `ln(1+rf) − ln(1+q)` and that is what it computed; the **prose** wrongly adds "less the half-variance term". So the number is right for the engine's definition and the sentence is wrong — not a 4× overstatement of the drift, but a description of a formula that was never applied. **Price — EGP 0.0000 on fair value; −2.2% on the 3M cone median if the prose were made true.** **Bucket: ACCEPT the wording fix, REJECT the "4×" characterisation.**

### D-11. "The 2026 flow is discounted a full year (DF 0.7600), ΔWC-2026 is measured from the 31-Dec-2025 balance, and net debt is the 31-Dec-2025 figure. t = 0 is therefore 31 December 2025, 218 days before the price it is compared with."

**Premise — VERIFIED and undisclosed.** This is the same defect §C-F17 found from the balance-sheet side; this reviewer finds it from the discounting side and gets the whole of it. **Price — the reviewer's own number: rolling the enterprise forward 0.597 years at 31.58% gives EGP 7.74 a share (+12.9%), against ~EGP 1.037 a share of dividends actually paid in the interim — "the two legs roughly offset here by luck, and neither is disclosed."** I accept that framing entirely; it is the most intellectually honest sentence in any of the four documents. **Above the 5% line on the gross leg.** **Bucket: ACCEPT** — state the valuation date on the face of the study, and either roll the value to the price date net of interim distributions or discount partial periods.

### D-12. "Three mutually exclusive statements about the same identity in one document."

**The same finding as C-F8, with the sharper observation that the study says three different things — "negative in every audited period", "about 0.4%", and "a NEGATIVE steady-state rate" — about one identity. Premise VERIFIED** (`terminal_recon.rr` positive in two of four; mean implied growth +0.37%). **Price EGP 0.0000. Bucket: ACCEPT.**

### D-13. "Setting capex = depreciation changes FCFF by −2, +17, +36, +54, +73. Correct only in 2026; wrong in sign in four of five years. The stated correction would raise the valuation, not lower it."

**The same finding as C-F9 with the year-by-year cash effect added. Premise VERIFIED** (capex/depreciation 0.986 / 1.114 / 1.242 / 1.366 / 1.496). **Price EGP 0.0000 directly; it inverts the direction of the study's own headline caveat.** **Bucket: ACCEPT.** Recorded again as the receipt that settles §A-3 and §B-9 against those reviewers.

### D-14. "4.6446% is the minority share of group profit for the audited half only; on the nine-month base it is 4.1126%. And the ratio was struck on a profit figure that includes EGP 173mn of parent credit interest — excluding it gives 5.846%."

**Premise — VERIFIED, and the credit-interest point is new across all four files and is the sharpest version of the NCI finding.** The study's stated justification for applying the ratio to enterprise value is that "deducting a percentage of a total that already includes the cash would hand the minority a slice of the parent's balance" — and then the ratio itself is struck on a profit number that includes the parent's cash interest. The justification is not applied to the ratio it justifies. **Price — 4.1126% → DCF 6.8795, weighted +0.38%; 5.846% → DCF 6.79, weighted ≈ −0.4%; the two together span 0.78% of central.** **Bucket: ACCEPT** — strike the ratio on the nine-month base and on operating profit only. **This row also completes the four-way NCI arbitration**: §A-4 (cash inconsistency), §B-6 (scope), §C-F18 (period), §D-14 (profit base) are four true premises about one defect, and only §B proposed a fix that makes it worse.

### D-15. "Creditors of 2,044.4mn include dividends payable of EGP 517.25mn — a financing claim, not operating working capital. Excluding it: NWC 2,251.4mn = 5.404% of revenue."

**Premise — VERIFIED exactly** (1,734.2 + 517.25 = 2,251.4 = **5.4040%** of base revenue, their 5.404%). A declared shareholder distribution is netted into the operating capital ratio that drives ΔWC in all five forecast years and the terminal invested-capital base. **Price — EGP −0.1060 weighted, −1.48%, for the NWC correction alone (DCF **6.6437**, their 6.64); EGP −0.3237 weighted, −4.52%, if the 517.25mn is also carried in the equity bridge (DCF 6.3147 against their 6.24).** **Conclusion — ACCEPTED on both legs.** Dividends payable is a declared claim on the balance sheet exactly as the tax provision at A-1 is, and consistency requires it be treated the same way. **Bucket: ACCEPT.**

### D-16. "Invested capital of 4,198mn rests on net fixed assets of 893mn against gross cost of 2,740.8mn — 67% written down. The workbook uses precisely this argument to haircut ROE from ~33% to 28% for the book lens, and does not apply it here."

**Premise — VERIFIED, and it is the best-argued judgement finding in any of the four files.** The `roe_sust` source note says, in my own words, that the reported return "is flattered by a heavily written-down asset base that will have to be renewed" — and that identical fact is not applied to the terminal ROIC of 35.4%, which sets the reinvestment rate that funds 58.7% of enterprise value. One disclosed fact, used to lower one lens and omitted from the other where it raises the answer. **Price — terminal ROIC 25% → DCF **6.6532**, weighted −1.25%; 20% → DCF **6.4837**, weighted −2.31%** (their 6.65 and 6.48, exact). **Bucket: ACCEPT** — apply one view of the asset base across all lenses, and disclose the terminal ROIC beside the gross-cost/net-book ratio that qualifies it.

### D-17. "17.1% is the terminal cost of equity. The near-term cost of equity in the same model is 27.76%, and the DCF applies 31.58% in year one. A perpetuity starting today is priced entirely at the post-normalisation rate."

**Premise — ACCEPTED.** The justified price-to-book of 1.9034 is (28% − 5%) / (17.0835% − 5%), a Gordon multiple built on the terminal rate and applied to **today's** book value. **Price — the reviewer gives a direction and a rough landing ("the lens falls toward 4–5") rather than a number, so I price the bound myself: at the explicit-window Ke of 27.76% the justified multiple is (28% − 5%)/(27.76% − 5%) = 1.0106, giving a book lens of EGP 3.749 against 7.0606 — EGP −0.4967 weighted, −6.93%.** **Above the 5% line**, and it is above it only because I priced it; the reviewer left it unpriced. **Conclusion — ACCEPTED as a defect; the fix is YOURS.** The pure terminal rate is too generous and the pure explicit rate is too harsh for a perpetuity that mostly lies beyond the glide. A rate path consistent with lens 1 — the same glide, applied to the equity claim — is the coherent answer and lands between them. **Bucket: YOURS**, bounded at 0.00% and −6.93%; **my recommendation is the glided path**, which I will implement and price rather than pick an endpoint.

### D-18. "No source is given anywhere in the study or workbook. The filings show cash dividends paid of EGP 1,339.5mn over nine months = 15.2% annualised. Declared DPS in the 12 months to 6-Aug-2026 = 0.80 + 0.40 = 1.20 → 13.2%; the latest single declaration alone = 4.4%."

**The same finding as C-F30, with a fourth framing added and both declarations cited.** The value is right on one framing and unsourced on all of them, in a study that claims every input carries a value, a source and a date. **Price — EGP 0.0000 on fair value; the 3M cone median moves −1.5% at the filed 15.2%, and the four framings span 4.4% to 15.2%, which is the whole of the cone's drift term.** **Bucket: ACCEPT** — state the DPS, the declaration dates, and the framing.

### D-19. "19.50% is the CBE main operation / discount rate, not a risk-free bond yield… The same term denotes two different rates 280bp apart in one document."

**Premise — VERIFIED as an internal inconsistency, which needs no egress to establish.** §1.6 calls 22.31% "the risk-free rate" and §3 calls 19.5% "the local risk-free rate". Both cannot be. **Price — EGP 0.0000 on fair value; it affects the cone drift.** **Bucket: ACCEPT** — name the instrument and tenor at each use.

### D-20. "Reference scan of all nine sheets: 'Yield on cash path' and 'USD/EGP average rate path' are orphans, as are the rating-basis default spread and ERP, the statutory tax rate, 'Expert 1 justified price/earnings 7.0' and 'Egyptian long-run nominal growth 15%'… A stated control that does not exist is a methodology-contract failure."

**Premise — ACCEPTED, and my own independent sweep found it is worse.** Scanning `compute.py` for inputs that never reach the model body: **`emp_h2_25`, `e1_pe`, `capex_pct`, `opex_pct`, `dna_pct`, `leases`, `fvoci`, `dtax_liab`, `egpc_sales`, `div_declared`, `dps`, `tax_due`, `world_nominal_growth`, `egypt_gdp_nominal`, `provisions`, and `tax_eff`** — sixteen registered inputs that drive nothing, of which the reviewer names six. My own reachability gate reported **zero** dead inputs, because it accepts "quoted in a deliverable" as reachability. **The gate is the defect**, and it passed while a 921mn liability (A-1), a 135mn profit distribution (D-4) and the model's own effective-tax input all sat inert. **Price — the individually priced ones total −8.47% (provisions) and −8.20% (employees' share); the rest are zero.** **Bucket: ACCEPT** — rewrite the reachability gate so that "quoted" no longer counts as "reached" for any input on the balance sheet or in the profit statement, and re-run it over the nine-sheet workbook.

### D-21. "IMF nominal EGP GDP growth falls 13.5% → 12.0% by FY2030/31. Internally, C124 builds the terminal risk-free rate off 5% inflation; 15% nominal growth with 5% inflation implies ~10% real growth."

**The same internal incoherence as C-F27, with the external IMF path added. Premise ACCEPTED.** **Price — EGP 0.0000; the ceiling binds nothing because it is never tested.** **Bucket: ACCEPT** — set the ceiling from the same inflation assumption used to build the terminal rate, and make it a live assertion rather than a sentence.

### D-22. "`=MIN(B5:B8)` and `=MAX(D5:D8)` — the min and max across all four lenses, both of which come from the DCF lens alone. The genuinely weighted range is 4.04 – 11.51."

**Premise — VERIFIED exactly.** Weighting the bear and bull columns as the base column is weighted gives **4.0384 – 11.5135**, their 4.04 – 11.51. The published 2.37 – 14.66 is the DCF lens's own extremes wearing the label "weighted central". **Price — EGP 0.0000 on the point estimate; the published spread is overstated by ~2.5×.** **Bucket: ACCEPT** — weight the bear and bull columns, and publish the five driver sets (which also answers C-F41 and §A's complaint about the range).

### D-23. "Recomputed with beta flowing to both the explicit and terminal cost of equity: 8.13 · 7.41 · 6.82 · 6.34 · 5.94. Explicit-window-only: 7.17 · 7.00 · 6.84 · 6.69 · 6.54. Neither reproduces the published row."

**Premise — ACCEPTED, and the reviewer is more careful than §C-F14: they tested two wirings and report that neither reproduces.** The decisive receipt is simpler and mine: `grid_beta[2]` = **6.9312** at the base beta of 0.9405, against a base DCF of **6.8518**. A row whose centre does not return the base case is broken regardless of which wiring was intended. **Price — EGP 0.0000 on the headline.** **Bucket: ACCEPT** — rebuild from full re-runs, publish which parameters are held fixed, and add the base-point-reproduction gate described at C-F14.

### D-24. "Damodaran January-2026 country-premium file, Egypt row: 3.41%. Transcription off by 1bp. Separately, a January-2026 spread is netted against a July-2026 bond yield — a six-month period mismatch inside one rate."

**Premise — the 1bp is UNVERIFIABLE (source egress-blocked); the vintage mismatch is VERIFIED and is the real finding.** **Price — EGP +0.0006, +0.01%,** at 3.41% — and I record that number rather than calling a 1bp transcription immaterial without one. **Bucket: ACCEPT** the vintage discipline (match the spread's vintage to the yield's); **RESEARCH** the 1bp.

### D-25. "Listed asset lines sum to 8,059.2 (unexplained 77.3mn); listed liability lines sum to 2,994.8 (unexplained 316.8mn). Presented as a balance sheet, but the components do not reconcile to the totals."

**The same finding as C-F16, with the additional identification that the 77.3mn gap contains the Alexandria Specialized Petroleum Products stake — which ties it to C-F33. Premise ACCEPTED.** **Price — ≈ +0.06 a share if the investment were carried at book, ≈ +0.17 at 8× its dividend.** **Bucket: ACCEPT** — add a residual line, and carry the investment in the bridge.

### D-26. "ln(1.20) = 0.18232 is correct for +20%; the −20% bound in logs is 0.22314, not 0.1823… A symmetric log bound is asserted for an arithmetically asymmetric limit; the halt trigger is not mentioned."

**Premise — VERIFIED, and the reviewer correctly notes it produced no false pass** (the observed maximum absolute log move is **0.18135**, inside the tighter of the two bounds, so the conservative test held). **Price — EGP 0.0000.** **Bucket: ACCEPT** — test up-moves against ln(1.20) and down-moves against |ln(0.80)|, and mention the ±10% halt.

### D-27. "AMOC raised its FY2026 profit target to EGP 2.1bn on 29 June 2026, from EGP 1.02bn set in December 2025. A disclosed company forecast, 36% above the model's own first forecast year, is neither used nor rebutted."

**The same finding as C-F3, dated and sourced independently by a second reviewer, and the 2.1bn / 1.02bn pair matches §C's "NPAT ~2,099mn (revised up from 1,024mn)" exactly. Two independent reviewers reaching the same two figures from the same disclosure raises this from unverified to strongly corroborated**, even though the disclosure itself is egress-blocked for me. **Price — EGP +1.1947 weighted, +16.68%** at guidance-implied operating expense; **above the 5% line, and upward.** **Bucket: RESEARCH on the number, ACCEPT on the process** — the study must cite disclosed guidance and say where and why it departs from it.

### D-28. "The regression statistics are internally coherent (t = β/SE = 10.81; from R² and n, t = 10.75; the 90% CI reproduces to [0.797, 1.084])… But the index is a house construct, not a published series… the beta cannot be reproduced by any reader."

**The same finding as C-F12, with an additional coherence test of my own diagnostics that I did not run and that passes.** **Price — the beta grid spans EGP 8.13 to 5.94 on their recomputation; beta 1.15 alone is −5.59% weighted, above the 5% line.** **Bucket: RESEARCH** — regress against EGX30 and publish both, or publish the composite's constituents and weights.

### D-29. "Which five drivers, and at what levels, is stated nowhere in the study or the workbook. Cannot be reproduced or falsified; sits inside the study's headline range."

**Premise — ACCEPTED**; the `SCEN` dictionary exists in the model and is not in the delivered documents. **Price — EGP 0.0000 on the point estimate; it defines the published range.** **Bucket: ACCEPT**, together with D-22.

### D-30. "The 2024-25 columns require invested capital of ≈4,124mn and ≈3,467mn — figures that appear nowhere in the study or the workbook… in a table presented under 'Every column is as filed'."

**Premise — VERIFIED** (`hist_bs.ic` carries 4,115.5 and 3,465.3 for those periods, and neither is a disclosed input in the delivered documents). The reviewer also confirms the two later columns reproduce exactly. **Price — EGP 0.0000 directly; it removes the audit trail from the table carrying the study's self-declared sharpest weakness.** **Bucket: ACCEPT** — publish the invested-capital denominator for every period shown.

### D-31. "Back-solving the seven rates reproduces total Dec-2024 product revenue of 18,244.7mn against filed net sales of 18,246.1mn — a 0.007% difference, so the set is arithmetically sound."

**A clearance, arrived at by independent back-solution, and it also clears the input C-F22 flags as unsupported.** **Price EGP 0.0000. Bucket: no action**, with the comparative product table to be published so a reader need not back-solve.

### D-32. "A secondary registry lists the Central Auditing Organization as joint auditor alongside Crowe, which the study does not mention."

**Premise — UNVERIFIABLE from here and important.** I read the four filings visually; `filings/AUDITED_EXTRACT.md` records the Crowe opinion, signed at Giza on 18 February 2026. For a company with a 20.77% state-linked shareholder, a joint CAO audit is plausible and would be material to how the opinion is read. **Price — EGP 0.0000.** **Bucket: RESEARCH** — re-read the signature block of the transition-period filing and name every signing auditor.

### D-33. "The same EGX disclosure carries standalone net profit of EGP 843.86mn — higher than consolidated, implying ≈218mn of consolidation effects on attributable profit that the study never explains."

**Premise — UNVERIFIABLE from here; the reviewer confirms the study uses the correct (consolidated) basis.** A standalone profit **above** consolidated is unusual and, if real, points at loss-making or equity-accounted consolidation effects that would bear directly on the NCI question running through A-4, B-6, C-F18 and D-14. **Price — EGP 0.0000 (the correct basis is used).** **Bucket: RESEARCH** — reconcile standalone to consolidated where both are disclosed.

---

**§D running total.** Above the 5% line and accepted: D-1 (**+70.9%** on the coherence-tested base), D-2 (+10.8%), D-3 (−10.80% at the corrected rate), D-4 (−8.20%), D-7 (−5.48%), D-11 (+12.9% gross, offset by interim dividends), D-17 (bounded at −6.93%). Accepted below the line: D-5, D-8 to D-10, D-12 to D-16, D-18 to D-26, D-29, D-30. Research: D-6, D-24 (1bp), D-27, D-28, D-32, D-33. Clearances: D-31, and the ~62-line reconciliation appendix in their §C.
