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
