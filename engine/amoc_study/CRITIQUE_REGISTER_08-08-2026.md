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
