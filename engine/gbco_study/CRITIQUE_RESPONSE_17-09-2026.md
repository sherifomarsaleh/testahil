# GBCO — response to the forensic audit of edition 07-09-2026

Under `engine/Critique_Response_Prompt.md`. **Nothing is implemented in this document.** It is
the self-audit, the ledger, the count reconciliation and the buckets, per step 8.

**Published answers under audit:** bear 19.2911 · carrying branch **41.3484** · round branch
**52.3453**, against EGP 28.98 of 3 September 2026. All percentages below are of the carrying
branch unless stated.

---

## PART 0 — SELF-AUDIT, DONE BEFORE THE CRITIQUE WAS READ

Eight findings, listed before opening the audit document. Three were also caught by the audit;
**five were not** — and one of the five is the most serious thing in this response.

| # | finding | price | audit caught it? |
|---|---|---|---|
| S-1 | **No `bridge_record` is committed at all.** [R-BRIDGE-01] requires the bridge's CHOICES to be recorded — which sheet, the minority basis, whether cash is charged once. `check_bridge.py` reports "GBCO carries no bridge record"; the study is on that ratchet. The bridge is where the whole two-sided answer lands and its construction is unrecorded. | nil on the answer; the construction cannot be checked from outside | **NO** |
| S-2 | **Auto net debt of 14,623.7 does not reproduce the company's own published 14,493.6**, while the code comment claims "the COMPANY'S OWN definition". Reconciled: the study omits the current portion of lease obligations (2,345.8 − 1,333.3 = 1,012.5) and omits the due-from-related-parties receivables (9.5 + 1,142.1 = 1,151.6) that Table 7 nets. | **+EGP 0.1199/share, +0.29%** | **YES — finding 24** |
| S-3 | **Capital expenditure consumes management guidance.** [R-FCAL-01] forbids it outright. The ladder implies depreciation coverage falling to 1.76× against a filed record of 3.87 / 2.79 / 3.67. | −22.91/share through the current terminal; **unpriceable through a correct one** | **YES — construction register, "Guidance"** |
| S-4 | **The terminal is the retired Gordon-on-last-FCFF construction**, on the [R-TERM-01] ratchet; `terminal_value.build()` refuses on this name because no usable asset life is sourceable. | any capex correction is multiplied ~15× through it | partly — finding 12 reaches the same place by a different route |
| S-5 | **There is no property-plant-and-equipment roll-forward.** Capex, depreciation and working capital are three independent typed ratios with no balance sheet joining them, so the asset base the model buys never appears, never depreciates and never constrains anything. SIGCM clause 7 unmet for PP&E. | nil directly; it is the defect underneath S-3, S-4 and finding 12 | **NO** |
| S-6 | **Peers are characterised, not studied.** The `Peer & Sector` sheet carries **zero** formulas and **zero** numeric cells. SIGCM clause 5 unmet. | nil on the answer; a required construction is absent | **NO** |
| S-7 | **GBCO commits no Step 2A sweep register at all** — no sweep script, no register. It sits on `sweep_outstanding.json`. | nil on the answer | **NO** |
| S-8 | **Workbook formula density measured: 69.3% (851 formulas, 377 hardcoded).** The hardcoded cells are concentrated in Assumptions (192), the historical statements (126) and the Monte Carlo draws (35) — all legitimately inputs. No *derived* cell was found hardcoded and `recalc.py` reconciles 851 of 851. | nil | partly — the audit's finding 18 found a **worse** version of this that I missed (see below) |

**WHAT THE AUDIT FOUND THAT MY SELF-AUDIT MISSED, AND IT MATTERS MOST:** the working-capital
anchor (finding 2). **I fixed that exact defect on another name in this same session — hours
earlier — and did not think to look for it here.** A self-audit that only re-checks the work it
did will keep missing the work it never did, and this is a worked example of it.

---

## PART 1 — THE LEDGER

One row per finding, in the audit's own order, quoting its words. **Prices marked ✓ were
re-derived independently here**; prices marked (audit) are the audit's own, accepted without
independent recomputation because the finding is not valuation-critical.

| # | the audit's claim (its words) | premise | conclusion | price | verdict |
|---|---|---|---|---|---|
| **1** | The US$1,400mn round, presented as one of GB Corp's own two disclosures. *"The cited GB Corp document does not contain the claimed figure."* | **RIGHT** — verified in the study's own record: `mnt_halan_stake_source` cites the 9-June release for the **41.61% stake**; `mnt_halan_round_usd` carries **no source field at all**, and the release is not in `src/`. | **RIGHT** | the framing of the whole upper branch; EGP 25.49/share = 49% of 52.3453 | **ACCEPT** ① |
| **2** | The working-capital anchor. *"The model runs its cash-flow walk from the 31-Dec-2025 stock while the bridge deducts 30-Jun-2026 net debt — two balance-sheet dates in one calculation."* | **RIGHT** — `WC_OPENING = 18917.0` is 4Q25; `auto_nd` is 30-Jun-2026. Disclosed ratio 28.51% → **22.62%** ✓ (audit 22.58%); working capital fell 1,824.2 while auto revenue rose 30.0% ✓ | **RIGHT** | ✓ **−3.3% / −20.1% / −24.8%** (39.98 / 33.03 / 31.11). The audit's 39.98 reproduced **exactly**; its 31.19 to within 0.08 | **ACCEPT** ② |
| **3** | Expert 2's residual income: *"a return struck on the Dec-2025 equity, multiplied onto the Jun-2026 book."* | **RIGHT** — 2,880.0 ÷ 33,454.3 = 8.61%, not the printed 10.00%; 10.00% is 2,880.0 ÷ 28,788.7 | **RIGHT** | nil on 41.35/52.35; **+16.2% / +86.7%** on Expert 2's own EGP 7.89, which is the printed panel floor | **ACCEPT** |
| **4** | *"The book is entirely local-currency on the disclosed facility note."* Note 26 names EGP **and USD** loans at 21.91% and 8.30%. | **RIGHT** | **RIGHT** | small in value; the assertion switched off a whole branch of the cost-of-debt test | **ACCEPT** |
| **5** | GB Auto FY2025 revenue 66,358 against four printed rows summing to **65,231**; a fifth unprinted row of 1,127.6 zeroed for every forecast year. | **RIGHT** — I confirmed the same 1,127.6 gap independently when tracing the pre-elimination revenue | **RIGHT** | (audit) +1.4% carried flat; **+2.0%** grown | **ACCEPT** |
| **6** | Appendix A.2 operating profit 3,977.0 / 6,176.6 does not foot; the audited restatement gives 5,820.840 — *"exactly the footed figure."* | **RIGHT** | **RIGHT** | nil on the answer; overstates FY2023 by 7.3% and FY2024 by 6.1% | **ACCEPT** |
| **7** | Expert 3's Auto ROCE of 21.3% against the company's own disclosed LTM 24.7% (4Q25) / 22.9% (2Q26). *"The sign flips, and the sign is the entire justification."* | **RIGHT** | **RIGHT** | (audit) Expert 3 at 1.00× = **39.50 vs 36.88, +7.1%** on his figure | **ACCEPT** |
| **8** | A **restated** associates comparative (15,732.426) subtracted from an **unrestated** segment equity (18,312.6), halving the Dec-25 base. | **RIGHT** — note 34's restatement is +2,460.218 | **RIGHT** | (audit) lender leg 482 vs 1,656 = **−EGP 1.08/share, −2.6%** | **ACCEPT** |
| **9** | The finance-cost ladder −4,100 → −3,100 *"while borrowings grow 38,041 → 66,241"*; a typed ladder with no derivation. | **RIGHT** | **RIGHT** | nil on the SOTP primary; **−8.9%** on the relative cross-check | **ACCEPT** |
| **10** | FY2026E group attributable profit of 3,298 implies a second half **+61.3%** on the actual first half, with no mechanism named. | **RIGHT** | **RIGHT** | nil on the SOTP primary; it is the denominator of the relative cross-check | **ACCEPT** |
| **11** | *"Three different capital structures in one calculation"* — group borrowings and group market cap in the weights, a group Kd, the segment's net debt in the bridge. | **RIGHT** — GB Auto's own effective rate computes to **19.98%** ✓ (audit 19.96%) against the group's 26.53% | **RIGHT** | (audit) **−13% to +19.7%** depending on which pair is made consistent | **ACCEPT** ③ |
| **12** | The asset-life refusal is honest, *"but the construction pins a life anyway"* — capex 2,800 / D&A 1,592.4 solves to **L ≈ 19.9 years** against a disclosed composite of 8–11. | **RIGHT** | **RIGHT** | direction conservative; a number reached by a construction nobody wrote down | **ACCEPT** — and it is S-4/S-5 arriving by another route |
| **13** | The register *"contains two layers, both Company"* — no country or market layer; the macro inputs, EGP/USD, the carrying value and the associates line carry no source or date. | **RIGHT** — confirmed: **19 register entries, and not one is MNT-Halan, the round, the associates line or EGP/USD** | **RIGHT** | not quantifiable; it is what makes findings 31/32 UNVERIFIABLE rather than PASS | **ACCEPT** |
| **14** | All four country-risk inputs reproduce exactly, **but the file's vintage is 5 Jan 2026 and a 1 July 2026 update exists.** | **RIGHT** | **RIGHT** | direction unknown; magnitude **UNVERIFIABLE** | **ACCEPT THE DEFECT** — see bucket 3 |
| **15** | *"The study is dated 7 September 2026, a Monday. The EGX trades Sunday to Thursday, so 6 September was a session."* | **RIGHT** on the calendar | **RIGHT** | ~2–2.5% of the published +43% / +81% | **ACCEPT THE DEFECT, REJECT THE FIX** ④ |
| **16** | Note 34 reads **15,723,523**, not the study's 15,733,523 — a transposition; the note's own rows foot on the audit's figure. | **RIGHT** | **RIGHT** | nil on the carrying branch (the residual absorbs it); round branch **EGP 0.009/share** | **ACCEPT** |
| **17** | Three §1.9 cells printed "n.m." are *"perfectly computable"*; the suppression rule is stated nowhere. | **RIGHT** | **RIGHT** | nil; narrows the apparent grid top from ~102 to 69.4 | **ACCEPT** |
| **18** | *"Years 2–5 of the cost-of-capital schedule and the terminal rate are hardcoded constants, not formulas."* A reader changing the ERP, beta or rf moves year 1 and nothing else. | **RIGHT** | **RIGHT** | nil on the answer; **84%+ of the Auto leg does not respond to the Assumptions sheet** | **ACCEPT** ⑤ |
| **19** | *"The file carries no cached values at all. Every formula reads empty."* | **RIGHT** | **RIGHT** | nil; defeats the check the workbook exists to enable | **ACCEPT** |
| **20** | The study's §1.9 grid 1 is mark × cost of capital; the workbook's is mark × gross-margin shift. The two do not correspond. | **RIGHT** | **RIGHT** | nil; both grids reproduce to ±0.05 | **ACCEPT** |
| **21** | `Fundamental Valuation!B7/D7` carry typed bounds 28.5273 / 85.4849 that appear nowhere in the study and sit outside its own envelope. | **RIGHT** | **RIGHT** | nil | **ACCEPT** |
| **22** | *"Other associates (Bedaya, Kaf)"* — note 34 lists **three** besides MNT: Misr E-commerce, Bedaia, Kaf. | **RIGHT** | **RIGHT** | nil | **ACCEPT** |
| **23** | The EGP 2,460,218 thousand restatement of the associate carrying value is never disclosed to the reader. | **RIGHT** | **RIGHT** | nil directly; it is the root of finding 8 | **ACCEPT** |
| **24** | Auto net debt 14,623.7 against the company's own published **14,493.6**. | **RIGHT** | **RIGHT** | ✓ **+EGP 0.12/share, +0.29%** — independently derived as **S-2** before reading the audit | **ACCEPT** |
| **25** | GB Capital's 10.10% is the study's own construction; the company publishes **15.1% (FY25) / 13.5% (1H26)** for the same segment, neither cited nor rebutted. | **RIGHT** | **RIGHT** | (audit) at 13.5% the leg is 3,472 vs 1,656 = **+4.0%** | **ACCEPT THE DEFECT, REJECT THE FIX** ⑥ |
| **26** | The EPS row is captioned as the company's own reporting but is attributable profit ÷ shares; the audited basic EPS is 2.609 / 2.635 after employees' profit share. | **RIGHT** | **RIGHT** | (audit) cross-check **19.95 vs 19.29, +3.4%** | **ACCEPT** |
| **27** | *"Every cut lowers GB Capital's funding cost on a fixed-rate lending book"* — the rate-risk note says the book is **variable**-rate (37,921,342) with only ~a quarter fixed. | **RIGHT** | **RIGHT** | nil on any computed number; a narrative claim a reader would act on | **ACCEPT** |
| **28** | The factor stack's discrete events sum to +1.06%; the seven continuous factors carry the residual +0.40% with no printed magnitude. | **RIGHT** | **RIGHT** | nil on the fundamentals; 27% of the simulation's factor drift | **ACCEPT** |
| **29** | *"GB Auto at its cash-flow value of EGP 28.7 bn"* — §1.1 and the bridge both give 26,998; 28.7bn is both legs. | **RIGHT** | **RIGHT** | nil; overstates the Auto leg by **+6.3%** in the headline paragraph | **ACCEPT** |
| **30** | The dash convention says the record does not carry FY2023/FY2024 segment splits; *"the workbook does carry them."* | **RIGHT** | **RIGHT** | nil | **ACCEPT** |
| **31** | The 23.00% risk-free is **UNVERIFIABLE** — public quotes span ~18.65% to 24.95% and no primary auction record was reachable. | **RIGHT** | **RIGHT** | *"A 1pp error in rf* moves the answer ~2.3%"* | **UNPROVEN — RESEARCH REQUIRED** |
| **32** | EGP/USD 47.5: *"Four different dates are in play for one rate on a line worth 49% of the higher answer."* | **RIGHT** | **RIGHT** | round branch only; a 3% move ≈ **EGP 0.76/share** on it | **ACCEPT** |
| **33** | Expert 1's range 27.10–87.19: *"Neither endpoint reproduces from any stated construction."* | **RIGHT** | **RIGHT** | nil — the base feeds the panel spread and reproduces exactly | **ACCEPT** |
| **34** | The risk register prices the beta fork against a unit beta rather than against the regression's **own** standard error of 0.2041, *"worth roughly twice as much."* | **RIGHT** | **RIGHT** | nil on the answer; understates a disclosed exposure by about half | **ACCEPT** |

**COUNT RECONCILIATION: 34 findings raised, 34 answered, 0 unaddressed.** No two findings
duplicate. Finding 24 duplicates my own self-audit S-2, reached independently before reading
the audit, and is recorded in both places rather than merged.

**The audit's six "checks that fired on work which turned out to be right"** — the cost of
debt, the 28% tax rate, the share count, the absent geographic split, the excluded 2Q26
presentation and the asset-life refusal's three grounds — are all PASSes for the study and are
recorded here as such. I re-checked none of them, because the audit re-pointed each and
published the arithmetic.

---

## PART 2 — THE FOOTNOTED VERDICTS

**① Finding 1 — the provenance of the upper branch.** Accepted in full, and it is the most
consequential thing in the audit because it is not a number, it is the study's organising
device. Verified from the study's own committed record rather than from the audit's assertion:
`mnt_halan_stake_source` cites GB Corp's 9-June release for the **stake**, and
`mnt_halan_round_usd` carries **no source field at all**. The register holds 19 inputs and not
one of them is this line. **The study's own sourcing rule — no press report is a source for a
figure the company reported about itself — is breached on the largest input of the higher
branch.** The round price is not thereby worthless; it is a recent primary transaction and a
legitimate reference. What cannot stand is calling it a company disclosure.

**② Finding 2 — the working-capital anchor.** Accepted in full; **it is the largest finding in
the audit and the one my own self-audit missed.** Independently re-derived: starting the walk
at the 30-June stock alone gives **39.9807**, reproducing the audit's 39.98 exactly; holding
the latest reviewed ratio flat gives **31.11** against its 31.19. My middle case comes out at
33.03 against its 35.10 — the gap is the interpolation path between the anchor and the 21.5%
endpoint, not a disagreement about the finding.

**③ Finding 11 — whose capital structure.** Accepted. GB Auto's own effective borrowing rate
computes to **19.98%** against the group's 26.53% used in the weights. The audit's sharpest
sentence is the one to keep: the published 22.88% lands within 0.3pp of one internally
consistent pairing — **right by offsetting errors, not by construction, and no reader could
tell.**

**④ Finding 15 — the price anchor. ACCEPT THE DEFECT, REJECT THE FIX.** The premise is right:
7 September is a Monday and 6 September was an EGX session, so a newer close existed at
delivery. The proposed fix — strike on the last session before delivery — cannot be executed
here on the audit's own terms, because it names no primary record for that close and this
container holds no exchange-primary price feed. **The house rule is stricter than the audit's
fix and already binds**: [R-GAP-01 AMENDED 07-09-2026] requires the price to be *asked for at
the start of the study*, and the standing default where none arrives is the latest committed
price used **with its date stated and its age disclosed**. What I will do instead: ask for the
close, and disclose the anchor's age against the delivery date rather than silently carrying it.

**⑤ Finding 18 — the hardcoded rate schedule.** Accepted, and **this is the finding that
answers the question about hardcoding better than my own S-8 did.** I measured formula density
at 69.3% and concluded the hardcoded cells were legitimate inputs. That was the wrong test.
The audit asked what happens when a reader *changes* an assumption — and the answer is that
years 2–5 and the terminal, which carry **84%+ of the Auto leg's value**, do not move. A
workbook can be 69% formulas and still be inert where it matters.

**⑥ Finding 25 — GB Capital's return. ACCEPT THE DEFECT, REJECT THE FIX.** The audit concedes
the study's construction is *"defensible and arguably better"* — associate income out of the
numerator, associates out of the base, so MNT-Halan is not counted twice in a sum of the parts
that already carries it as its largest leg. **Adopting the company's 13.5% would double-count
the associate**, which is why the fix is rejected. The defect is real and is one of disclosure:
the company publishes a figure for this exact segment and the page neither cites nor rebuts it.
Remedy: print the company's 15.1% / 13.5% beside the study's 10.10% with the reason, exactly as
the study already does for the two premium bases.

---

## PART 3 — BUCKETS

**BUCKET 1 — ACCEPT AND IMPLEMENT (26):** 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18,
19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34 — *and* self-audit S-1, S-2, S-5, S-6,
S-7.

**BUCKET 2 — ACCEPT THE DEFECT, REJECT THE FIX (3):** 15 (price anchor — the house rule is
stricter and already binds), 25 (GB Capital's return — the company's figure double-counts the
associate; disclose beside rather than adopt), 1 in part (the round price stays published as a
*third-party mark*; what is retired is the "two company disclosures" framing).

**BUCKET 3 — UNPROVEN, RESEARCH REQUIRED (2):** 14 (the July-2026 country-risk vintage — the
audit could not retrieve Egypt's row and neither has this session yet), 31 (the 23.00%
risk-free — needs a primary auction or central-bank curve record).

**BUCKET 4 — REJECT (0).** **I reject nothing.** Every one of the 34 findings has a premise
that holds against a primary document or against the study's own committed record, and I
verified the three largest myself rather than accepting them. A response that accepts
everything is as uncalibrated as one that accepts nothing — so it is worth saying exactly why
this one does: the audit re-pointed its own checks six times when they fired on work that
turned out to be right, and published those as PASSes. **It had already done the rejecting.**

**BUCKET 5 — YOUR DECISION (1).**

> **What the upper branch is, now that it is not a company disclosure.** Finding 1 removes the
> premise for publishing two answers. Three honest responses, priced:
>
> 1. **Keep both branches, relabel.** Carrying value = the company's number; round price = a
>    third-party mark GB Corp has never adopted. Answers unchanged at 41.35 / 52.35 before the
>    other findings. *This is my recommendation* — the disagreement is real and a reader is
>    entitled to see it, and the audit itself says the upper branch "is not thereby worthless".
> 2. **Publish the carrying value alone**, with the round price as a disclosed cross-check.
>    Single answer ≈ 41.35 before the other findings; loses the study's most honest feature.
> 3. **Publish the round branch alone.** Rejected outright — it would rest the whole answer on
>    a press-relayed figure the company has never adopted.

---

## PART 4 — WHAT THIS RESPONSE OWES BEFORE ANY REBUILD

**The combined effect is not the sum of the rows.** Findings 2, 11 and 12 all move the Auto
leg and interact; S-3/S-4/S-5 sit underneath them. Under [R-REBUILD-01] the levers must be
ordered **before** any figure is recomputed, and the running total read at each step.

**And [R-GAP-01] will bite on the way down.** The carrying branch is +42.7% against 28.98
today. Finding 2 alone takes it to between +38% and +7%. A restruck central more than 10% from
the latest known price in either direction owes its eight-heading review before the files are
staged — and the answer may cross the trigger *during* the rebuild rather than at the end of it.

**Nothing is implemented. Awaiting approval.**
