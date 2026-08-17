# Critique response — ADNOC Distribution, second edition

Four critiques, worked under the standing procedure. **103 findings raised, 103 answered, 0
unaddressed.** Prices are AED per share on the Frame A discounted-cash-flow reading and on
the Frame A weighted centre of **4.3911**, both re-derived independently through the full
chain, not read off the workbook.

Baseline for every price below: DCF Frame A **4.4496**, centre **4.3911**, spot **4.07**
(+7.9%).

---

## PART 1 — SELF-AUDIT, RUN FIRST

**Process disclosure, because it affects how much this list is worth.** The Cowork critique
was loaded into my context in full by the file-read before I could begin, so my list is
**not** independent of that one. I had not opened the other three when I ran the checks
below. Everything here was verified by computation against my own committed numbers, not
taken from any critique.

A self-audit that finds nothing is a failed self-audit. Mine found ten defects, and
**four of them I introduced myself in the two edits I made this session** — which is the
most important thing on this page.

| # | Defect I found | Receipt | Mine, and when |
|---|---|---|---|
| SA-1 | The beta sensitivity ladder does not reproduce the model. `revalue()` in `compute.py` moves the terminal beta by a **fixed additive** `beta_terminal − beta`; the workbook uses `β + 0.389×(1−β)`. They agree only at the base case. At β=1.00 the ladder implies a terminal beta of **1.136** — drifting *away* from the market beta of 1.0 that the note says it drifts toward. | Printed both rules at all five ladder points: terminal β live 0.664/0.725/0.786/0.878/1.000 vs used 0.586/0.686/0.786/0.936/1.136 | **Yes — introduced this turn**, when I made the terminal beta derived and did not update `revalue()` |
| SA-2 | The "2% cost escalator" comparator matches no cost line in my own model. Cash opex escalates at **4.0%**; 2.0% is the **margin-per-litre** escalator. | `V['cash_opex_g']=0.04`, `V['gp_retfuel_per_l_g'][-1]=0.02` | **Yes — introduced this turn**, in the sign-aware crux rewrite |
| SA-3 | The 18.0× reference multiple is **two-thirds the traded price divided by earnings** (18.17× and 19.57×), while the study says it is "what this company's own return, growth and cost of equity justify — NOT a peer median". | Only the third leg (16.32×) is fundamentals-derived | **Yes — introduced last turn**, when I replaced the asserted 16.0× with a triangulation |
| SA-4 | The normalised-earnings lens is labelled "statutory 9%" in the text and computed at the **10.17% effective** rate. | Text: "Taxed at the statutory 9% it is AED 3,204 million"; the model applies `1−C16` = 10.17% | **Yes — introduced last turn**, when I fixed the rate and left the prose |
| SA-5 | The "normalised earnings power" lens asks "if this company never grew again, what would it be worth?" and computes `NOPAT ÷ (WACC − 1.5%)` — a **growing** perpetuity with **zero reinvestment**, while the DCF charges 6.0% of NOPAT for the same 1.5%. | True zero-growth = 3,204.1 ÷ 7.078% → **3.248/share** vs published **4.222** | Pre-existing |
| SA-6 | The published field **3.73–5.25** is `centre_A × 0.85` and `centre_B × 1.15` — an undisclosed ±15% band. The actual method min/max is **3.580–5.338**, so the band **narrows** the field while the caption says it "widen[s]" it. And the dividend reading (3.648) sits **outside** the range it is said to lie within. | `4.3911×0.85 = 3.7325`; `4.5650×1.15 = 5.2498` — exact | Pre-existing |
| SA-7 | Margin per litre printed as "**354.3 fils**". `0.354284 AED = 35.43 fils`. The sentence "comfortably above the 45-fils floor" therefore **inverts**: 35.4 fils is *below* 45. | 1 AED = 100 fils | Pre-existing |
| SA-8 | "The implied beta of **0.77 sits ABOVE** the 90% upper bound of the regression, **0.79**" — 0.77 < 0.79. And the Table 15 caption says a reader believing 0.77 has "a complete and internally consistent case". The two captions assert opposites. | `crux.beta_implied = 0.7669`, `ci90[1] = 0.7928` → BELOW | Pre-existing |
| SA-9 | "the three-month 95th percentile of AED 4.86 sits below every one of the four weighted methods" — 4.86 is **above** three of four (DCF 4.45, normalised 4.22, book 3.58). | Computed against all four | Pre-existing |
| SA-10 | "Dividends paid **have exceeded** free cash flow after capital expenditure in FY2024 and FY2025 — AED 2,599 million against AED 2,715 million" — 2,599 **<** 2,715. The sentence disproves itself. | FY2024: 2,614 < 2,752 | Pre-existing |
| SA-11 | Dividend policy stated as "92% of net profit if that is higher". 92% is my own **realised payout** input, labelled "paid against earnings since listing". | `inputs.payout.source` | Pre-existing |
| SA-12 | The balance-check row is a **hardcoded 0.0** in all three audited columns; the FY2023/FY2024 provisions row is empty, so those columns do not sum. The caption claims "the check row reads zero in **every** audited column". | `brow('chk', ..., [0.0,0.0,0.0], ...)` | Pre-existing |

**Which they also caught:** all twelve. Cowork caught SA-1(#4), SA-2(#26), SA-3(#3),
SA-4(#9), SA-5(#2), SA-6(#5), SA-7(#8), SA-8(#11), SA-9(#12), SA-10(#13), SA-11(#7),
SA-12(#14). Code caught ten of the twelve (not SA-9, SA-10).

**Which I missed that they caught — the ones that matter:**
- The **risk-free rate over-strip** (Cowork #1, Code #9). This is the single largest finding
  in the whole exercise and I did not find it. Worse: **the disproof is in my own research
  record**. See Part 3.
- The **sensitivity ladders are retail-only** while the text describes them as moving all
  legs (Code #8) — materially weakens my own crux.
- The **Pillar Two safe-harbour note affirmatively resolves** the top-up-tax question
  (Code #21) — my study presents it as open. This one cuts *in my favour* and I still got
  it wrong.
- **Terminal ROIC 25% appears in no sensitivity table** (Cowork #21) — 0.53/share of
  undisclosed range, the third-largest lever in the model.

---

## PART 2 — ENUMERATION

Price convention: **Δps** = change in the Frame A DCF; **Δc** = change in the weighted
centre. "nil" means computed and below 0.005/share, not asserted.

### 2A — Cowork critique (52 findings, its order)

| # | Their words (abridged) | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| 1 | "Stripping 42bp from a bond whose entire observable credit spread is 4bp produces a 'risk-free' rate ~38bp **below** the matched-tenor USD risk-free rate, in a currency hard-pegged to the dollar" | **Δps −0.259 (−5.8%) at rf* 4.44%; −0.556 (−12.5%) at a tenor-matched 4.89%. Δc −0.226 to −0.474** | Premise ✅ Conclusion ✅ | **ACCEPT — escalated, Part 3** |
| 2 | "The cell is `=NOPAT/(WACC − 1.5%)` — it capitalises perpetual 1.5% growth with zero reinvestment… described three times as zero-growth" | Lens −0.974; **Δc −0.243 (−5.5%)** | Premise ✅ Conclusion ✅ | **ACCEPT — escalated, Part 3** |
| 3 | "**Two of the three legs are the traded price divided by earnings.** Only leg (iii) is fundamentals-derived" | Lens 5.094→4.613; **Δc −0.096 (−2.2%)** | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 4 | "the terminal beta was moved by a **fixed +0.136385** rather than by the workbook's `β + 0.389×(1−β)`… range **1.20**, not 1.80" | Δps nil on 4.45; range overstated 50%; implied β 0.766→**0.828** | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 5 | "3.73 = 4.3911 × 0.85 and 5.25 = 4.5650 × 1.15 — an **undisclosed ±15% band**… It **narrows** the method field" | Δps nil; headline range misdescribed | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 6 | "The company's own FY2025 MD&A discloses **ROCE 32.7%**… The report's figure is its own undisclosed recomputation" | Δps nil; "8× cost of capital" → 4.6× | Premise ✅ (pending primary check) Conclusion ✅ | **ACCEPT, verify figure** |
| 7 | "the report's **own Table 29** state 'or a minimum of **75% of net profit**'… 92% is the model's label for the *historically realised* payout" | Via justified P/E: **Δc −0.057 (−1.3%)** | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 8 | "`Assumptions!C54` = **0.354284 AED** = **35.43 fils**… overstated **10×**, and at the correct 35.4 fils the retail margin is **21% BELOW** the 45-fils floor" | Δps nil; a structural claim inverts | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 9 | "'Tax at the **statutory rate of 9%**'… `B12` = `B11*(1-C16)` where C16 = **10.17%**" | If truly 9%: Δps +0.063, **Δc +0.025** | Premise ✅ Conclusion ✅ | **ACCEPT (relabel, not recompute)** |
| 10 | "'**No data vendor, broker note or press report was used as the source of any number about the company itself.**' Contradicted by the report's own research record: CO-01… StockAnalysis.com" | Δps nil; voids a declared contract | Premise ✅ Conclusion ✅ | **ACCEPT — most serious non-numeric finding** |
| 11 | "0.77 is **below** 0.79. The sentence is false about two numbers printed in the same document" | Δps nil; invalidates the §1.7 ranking | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 12 | "4.86 is **above** three of the four" | Δps nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 13 | "2,599 < 2,715… Dividends did **not** exceed FCF in either year cited" | Δps nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 14 | "`B15`,`C15`,`D15` are **hardcoded zeros**… FY2023 liabilities+equity = 18,404.4 against total assets 18,891.6 (short **487.3**)" | Δps nil; false integrity claim | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 15 | "Several classified drivers correspond to **no cell in the workbook**… UAE CPI 1.8% is stated to be 'the escalator on the domestic cash operating cost line only' — `C41` escalates at **4.0%**" | Δps nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 16 | "A figure the report states it could not read from the named source is cited to that source" | Δps nil (no crude cell) | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 17 | "TTM EPS = 3,564 ÷ 12,500 = 0.2851 → **P/E 14.3×**… EV/EBITDA **10.9×**" | Reference leg falls; **Δc ≈ −0.07** | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 18 | "the subject is **8th of 9**, second-highest; median 10.35×" | nil (peers unused) | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 19 | "it is driven substantially by an aviation mix shift… and it is **capitalised into the perpetuity**. Removing it… gives **AED 4.12**" | **Δps −0.329 (−7.4%); Δc −0.132** — larger than the 0.31 inventory judgement | Premise ✅ Conclusion ✅ | **ACCEPT — escalated, Part 3** |
| 20 | "The model's **own balance sheet** forecasts net debt falling from 2,985 to **409 by FY2030** — it de-gears, it does not re-gear" | **Δps −0.101 (−2.3%)** at today's 5.54% | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 21 | "25% is an unanchored input… It appears in **no** sensitivity table despite being the third-largest single lever" | **0.53/share of undisclosed range** (ROIC 15%→50% spans 4.296–4.565) | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 22 | "`C17` = `C14*(1-C15)` with C15 = **9% statutory**… At 10.17% it is **4.56%**" | ~0.03bp on WACC | Premise ✅ Conclusion ✅ | **ACCEPT (label)** |
| 23 | "the same study defines enterprise value as market cap + net debt + **leases + NCI**… On that definition the debt weight is 8.0%" | **Δps +0.005** | Premise ✅ Conclusion ✅ | **ACCEPT (consistency, not value)** |
| 24 | "2,794 ÷ 3,230.4 (**closing** equity) = 86.49%. On average equity it is **89.8%**" | nil | Premise ✅ Conclusion ✅ | **ACCEPT (label)** |
| 25 | "10.17% = FY2025 tax ÷ **profit before tax**… Applying it to **EBIT** taxes a larger base" | ~0.05 conservative | Premise ✅ Conclusion ⚠️ direction favours me | **ACCEPT the defect, keep the conservative number, disclose** |
| 26 | "`C41` escalates cash operating costs at **4.0% a year**… 2% is the **margin-per-litre** escalator" | nil on value; the crux rhetoric rests on it | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 27 | "6.1% is cash opex ÷ **revenue**… 83.5% reproduces on **no** denominator… 83.5 is also, exactly, the Brent spot price" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 28 | "Both readings are stated as 0.65, so no effect of the stated adjustment is shown… the published index contains the subject" | nil | Premise ✅ Conclusion ✅ | **ACCEPT — the claim is false as written** |
| 29 | "The equivalent total ERP is… **6.00%**, which is **+23%** on the 4.87% used. It is +42% only against the **mature-market** 4.23%" | nil | Premise ✅ Conclusion ✅ | **ACCEPT (name the base)** |
| 30 | "2.9m is an **annual** figure divided by a **half-year** base… On an annual base it is **1.44%**" | nil; the most-quoted observable is ~2× out | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 31 | "The drift fraction of **0.389** is itself a bare input, reverse-engineered" | nil | Premise ✅ Conclusion ✅ | **ACCEPT — "derived" overclaims** |
| 32 | "Peer EV/EBITDA and the subject's own price and market capitalisation → **StockAnalysis.com**… UAE fuel price history → **DubaiWheels**" | nil to small | Premise ✅ Conclusion ✅ | **ACCEPT (see #10)** |
| 33 | "The same quantity carries opposite signs in two tables" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 34 | "'**8 listed comparators**' vs Table 38: '**Seven** usable listed peers'" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 35 | "Two weighted point estimates (4.39 / 4.57) are published with explicit 'vs market' upside percentages" | nil | Premise ✅ Conclusion ✅ | **ACCEPT — the disclaimer overreaches** |
| 36 | "'**Five readings**' vs '**Four independent methods**'… and the fifth reading (3.65) lies outside it" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 37 | "Frame B's DCF pulls **Frame A's** working-capital line" | ~0.004 | Premise ✅ Conclusion ✅ | **ACCEPT the disclosure gap; keep the shortcut** (deliberate — an inventory gain is a margin effect, not a change in physical stock; documented in `compute.py`, not in the study) |
| 38 | "The published 5th–95th spread implies **~20.1%** (1M) and **~22.0%** (3M)… the median equals anchor × exp((r−q)t), i.e. the lognormal **mean**" | nil on value | Premise ✅ Conclusion ⚠️ | **ACCEPT the disclosure gap** — the engine is a Student-t HAR process, not lognormal; backing vol out of percentiles under a lognormal reading will not recover the input. The study should say which process |
| 39 | "0.367395 AED = **36.74 fils**… Same 10× error as #8" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 40 | "Expert 1: 'Your justified multiple is **15 times** book' — The study computes **13.9×**" | nil | Premise ✅ Conclusion ✅ | **ACCEPT** |
| 41 | Beta regression "**UNVERIFIABLE** — no price series in either file" | — | Fair | **ACCEPT — publish the series** |
| 42 | All technical readings "**UNVERIFIABLE**" | nil (TA feeds no valuation cell) | Fair | **ACCEPT — publish the cleaned series** |
| 43 | Backtest statistics "**UNVERIFIABLE**" | nil | Fair | **ACCEPT — publish the window table** |
| 44 | "the specific historical close was not retrievable… CO-01 gives AED 50.86bn, a AED 15m difference" | nil | Premise ✅ Conclusion ⚠️ | **ACCEPT unverifiability; the 15m is vendor rounding of the price to 3dp** |
| 45 | "45 fils/litre… the report's **own Table 38** records it as sourced from secondary reporting" | Load-bearing for #8's inverted claim | Premise ✅ Conclusion ✅ | **ACCEPT — research now** |
| 46 | Eight peer multiples "not recomputed from peer filings" | nil (unused) | Fair | **ACCEPT** |
| 47 | "UAE CPI 1.8%… was not located in the original publication" | nil (no cell) | Premise ✅ Conclusion ✅ | **ACCEPT** |
| S1 | "**H1-2025 inventory movements of AED 147m**… gives a half-yearly series (147 / 188 / 762)" | Tests Frame B's 294.5 directly | Premise ✅ Conclusion ✅ | **ACCEPT — research now** |
| S2 | "**The disclosed retail/commercial split of inventory movements**" | Reconciles against the 17% step (#19) | Premise ✅ Conclusion ✅ | **ACCEPT — research now** |
| S3 | "**The company's own Underlying EBITDA reconciliation**… and **disclosed ROCE** (32.7%)" | Replaces a private normalisation | Premise ✅ Conclusion ✅ | **ACCEPT — research now** |
| S4 | "stations +11.3% y/y against retail volume +1.0%, i.e. volume per station down ~9%" | Direct evidence on the crux | Premise ✅ Conclusion ✅ | **ACCEPT — the best single omission in the list** |
| S5 | "**TotalEnergies Marketing Egypt 50% acquisition**… the exclusion is never disclosed" | See Code #23 — **the date is wrong**; completed Feb-2023 and already consolidated | Premise ⚠️ Conclusion ❌ | **REJECT on the facts, ACCEPT the disclosure point** — Egypt sits inside the audited history. Receipt: 245 Egyptian stations are in the FY2025 network count and Egypt revenue is in the audited segment note |

### 2B — Code critique (34 findings, its order)

| # | Their words (abridged) | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| 1 | "`C54` = 0.35428 AED/l = **35.43 fils**… the comparison inverts" | nil | ✅ / ✅ | **ACCEPT** (= CW#8) |
| 2 | "A 'no growth' lens capitalises a growing perpetuity… while the DCF's own terminal block charges 6%" | **Δc −0.243** | ✅ / ✅ | **ACCEPT** (= CW#2) |
| 3 | "Two of three inputs are the traded price being tested" | **Δc −0.096** | ✅ / ✅ | **ACCEPT** (= CW#3) |
| 4 | "0.77 < 0.79… A false inequality" | nil | ✅ / ✅ | **ACCEPT** (= CW#11) |
| 5 | "Cells reproduce only under terminal β = β + 0.1364 (fixed add)… range 1.20 (not 1.80); implied beta = **0.828**" | nil on 4.45 | ✅ / ✅ | **ACCEPT** (= CW#4) |
| 6 | "Readings run 3.580–5.338… an undisclosed ±15% band" | nil | ✅ / ✅ | **ACCEPT** (= CW#5) |
| 7 | "Model C41 cash opex = **4.0%** p.a… The only 2.0% is the margin-per-litre escalator" | nil | ✅ / ✅ | **ACCEPT** (= CW#26) |
| 8 | "My reruns: **all legs −1pp → 4.1168**; both fuel legs −10% margin → **3.7056**… Retail-only reproduces both" | My re-derivation: all legs −1pp → **4.125**; both legs −10% → **3.696**. Published 4.24 and 3.95 | ✅ / ✅ | **ACCEPT — escalated, Part 3. Materially weakens my own crux** |
| 9 | "Rebuilding on the report's own 4.93%: → **4.1191**/share… subtracting 42bp yields a 'risk-free' 4.06% ~38bp below the same-tenor UST" | **Δps −0.331 (−7.4%)** at 4.93−0.42; **−0.556** at 4.93−0.04 | ✅ / ✅ | **ACCEPT — escalated, Part 3** |
| 10 | "USD 700m… or a minimum of **75%** of net profit… The 92% is model C50, the historical payout" | **Δc −0.057** | ✅ / ✅ | **ACCEPT** (= CW#7) |
| 11 | "Brent **$89.81** on 4 Aug 2026… $89.78 on 17 Aug 2026" vs my 83.55 | Scaling prices +7.5% → +0.5% via working capital only | Premise ⚠️ | **UNPROVEN — research now.** Two sources disagree on a figure that enters no cell |
| 12 | "STEO PDF 'could not be parsed'… then used as a driver anyway. Current STEO carries **$69** for 2027" | immaterial | ✅ / ✅ | **ACCEPT** (= CW#16) |
| 13 | "3,566.85 × 9% = **321.0**, not 363" | Δps +0.063 if truly 9% | ✅ / ✅ | **ACCEPT** (= CW#9) |
| 14 | "`C17` = 5.08% × (1 − 9%)… At 10.17% it is 4.5635%" | immaterial | ✅ / ✅ | **ACCEPT** (= CW#22) |
| 15 | "On average equity ((2,991.839+3,230.423)/2) = **89.81%**" | nil | ✅ / ✅ | **ACCEPT** (= CW#24) |
| 16 | "Including leases in the weights: wd 8.01%, WACC 7.01%… ROCE incl. leases = 44.4%; company's own disclosed H1-26 ROCE = **40%**" | **Δps +0.005** | ✅ / ✅ | **ACCEPT.** Note: gives a *third* ROCE figure (40%) against Cowork's 32.7% — see Part 3 arbitration |
| 17 | "`B12` = (MC+ND+leases) ÷ EBITDA = **12.917×**, excluding NCI. Report's 13.0× = 12.97×" | nil | ✅ / ✅ | **ACCEPT** |
| 18 | "Subject 13.0× is **2nd highest of nine**, and above Aldrees at 12.89×" | nil | ✅ / ✅ | **ACCEPT** (= CW#18) |
| 19 | "**950** is nowhere derived or explained… text says 294 in four places, 295 in two" | Frame B 4.7626 vs 4.7500 → the unexplained 188 is worth **+0.013** | ✅ / ✅ | **ACCEPT** |
| 20 | "reported EBITDA USD 786m vs underlying USD 603m → gap USD 183m = **AED 672m**", not 762 | At 672: 4.4436 (**−0.006**) | Premise ⚠️ Conclusion ⚠️ (their own words: "a discrepancy, not a proven mis-transcription") | **UNPROVEN — research now.** Central to my contested judgement |
| 21 | "FY2025 audited Pillar Two note: the Group… 'applied the transitional CbCR safe harbour… resulting in **no top-up tax**'" | My "largest downside construction" of 0.26/share is overstated as live | ✅ / ✅ | **ACCEPT — and it corrects in my favour, which is why I should have caught it** |
| 22 | "Materials ÷ total cost base = **88.9%**; ÷ revenue = **79.9%** — neither is 83.5%" | nil | ✅ / ✅ | **ACCEPT** (= CW#27) |
| 23 | "Completed **February 2023** (~USD 186m, ~240 stations)" | nil — already consolidated | ✅ / ✅ | **ACCEPT — and it refutes Cowork S5** |
| 24 | "Model has three legs; **corporate and aviation are blended**… aviation volume +53.9% while corporate −2.6%" | Indirect; it is where the 17% step sits | ✅ / ✅ | **ACCEPT** |
| 25 | "`C35` = +17% for FY2026 (8.5× the retail escalator), nowhere explained… the aggregate is supportable, the split and the claim are not" | **Δps −0.329** if removed | ✅ / ✅ | **ACCEPT** (= CW#19). Note their cross-check runs *in my favour* on the aggregate |
| 26 | "Table 1 publishes 'WEIGHTED CENTRE — Frame A 4.39 | 8%'… immediately after the 'no single number' sentence" | nil | ✅ / ✅ | **ACCEPT** (= CW#35) |
| 27 | "The same fixed dividend with no growth: 0.2057 ÷ 7.2226% = **2.848**" | Lens 3.648 → 2.848; unweighted, so **Δc nil** | ✅ / ✅ | **ACCEPT — a contractually flat dividend should not be grown** |
| 28 | "B15/C15/D15 are hardcoded constants 0… short 487.266… The Word table carries the 487/450 lines, so the report balances where the model does not" | nil | ✅ / ✅ | **ACCEPT** (= CW#14) |
| U1 | Beta regression unverifiable | — | Fair | **ACCEPT — publish** |
| U2 | Technical indicators unverifiable; "Prose '3% below that high' vs Table 25's 2.6%" | nil | ✅ / ✅ | **ACCEPT both** |
| U3 | Monte Carlo / backtest unverifiable; "Implied vol backed out ≈ 20%/22% vs stated 21.6%/22.7%" | nil | Fair | **ACCEPT** (= CW#38) |
| U4 | "The canonical ctryprem.html still reads 'Last updated: January 5, 2026'" | — | Fair; "the choice is defensible and honestly disclosed" | **ACCEPT the unverifiability** |
| U5 | FY2024/FY2025 inventory movements not an audited line | Frame A/B gap of 0.31 rests on them | Fair | **ACCEPT — research now** |
| U6 | "Scope not established: which products, which geography" for the 45-fils floor | Load-bearing for the inverted claim | Fair | **ACCEPT — research now** (= CW#45) |

### 2C — Gemini "think" critique (8 findings)

| # | Their words (abridged) | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| GT1 | "**Circular Logic Trap**… By feeding the asset's current market pricing into the intrinsic valuation target, the model illegally contaminates the fair value baseline" | **Δc −0.096** | ✅ / ✅ | **ACCEPT** (= CW#3) |
| GT2 | "**The NCI Trap**… the true economic claim (Fair Value) of the NCI is approximately **AED 790m**. Deducting the accounting book value artificially inflates the parent equity value by over AED 560m" | My re-derivation on their own method (57.042 × 1.015 ÷ (7.2226% − 1.5%)) gives **1,012**, not 790. **Δps −0.063 (−1.4%)** | Premise ✅ Conclusion ❌ (number unreproducible) | **ACCEPT the defect, REJECT the figure.** Receipt: their 790 implies a discount rate of ~8.85% or a growth rate they do not state; at the study's own Ke and g the answer is 1,012. Fix differently — and note the deeper issue is that NCI profit is *flatlined* at 57m in my model, which is the actual defect |
| GT3 | "If leases are treated as debt in the bridge, they must be included in the capital weighting… lowering the first-year WACC to **7.01%**" | **Δps +0.005** | ✅ / ✅ | **ACCEPT — and note it moves value UP, against their framing of it as a correction that deflates** |
| GT4 | "**Frame B is rejected.** Capitalizing non-recurring inventory commodity windfalls into a DCF perpetuity fundamentally violates earnings quality… artificially inflates EV by roughly ~**AED 4.8 billion**" | Frame B − Frame A EV = 68,767 − 60,282 = **8,485**, not 4,800. Per share the gap is **0.313** | Premise ✅ Conclusion ❌ | **ACCEPT the premise, REJECT the fix.** Receipt: Frame A **is** the normalising frame and **is** the headline centre (4.39). Frame B is published beside it, labelled through-cycle, and explicitly never averaged in — the dual-framing rule requires publishing both. Deleting it would remove a disclosure, not a distortion. Their EV figure is also 43% out |
| GT5 | "⚠️ **Tax Rate Contradiction**… claims to tax at the 'statutory rate of 9%'. Mathematically, it applied the 10.17% effective rate" | Δps +0.063 if truly 9% | ✅ / ✅ | **ACCEPT** (= CW#9) |
| GT6 | "**Terminal Weight**: 74.8% of EV sits in the terminal block… introduces severe duration risk" | Disclosed as a bridge line and in the summary table, three places | Premise ✅ Conclusion ⚠️ | **ACCEPT the risk, REJECT "undisclosed".** Receipt: gate item (p); Table 1 caption tells a distrusting reader to read §1.7 first |
| GT7 | "**Working Capital Subsidization**… The model is pricing in the assumption that the parent company will provide free working capital financing **in perpetuity**" | ΔNWC path is +476 then 45/53/49/42; the **terminal block contains no working-capital term at all** | Premise ✅ Conclusion ❌ | **ACCEPT the disclosure gap, REJECT "in perpetuity".** Receipt: my own FCFF rows — the release collapses to ~1% of FCFF after FY2026 and is absent from the terminal. The real gap is the *unwind* risk (GR3), which is unsensitised |
| GT8 | "the mathematically corrected and conceptually sanitized Fair Value is **AED 4.30** per share" | Their own components: 0.40×4.41 + 0.25×**4.30** + 0.20×4.61 + 0.15×3.58 = **4.2965** | Premise ⚠️ Conclusion ❌ | **REJECT.** Receipt: their normalised leg of 4.30 is *higher* than my 4.222 because they corrected the tax to 9% while **not** fixing the zero-growth error they did not find — the single largest lens defect. Their "sanitised" number is built on the growing-perpetuity error. Coherence test against the other two Claude critiques, which both price that lens at 3.25: Gemini's correction moves the wrong way |

### 2D — Gemini "research" critique (9 findings)

| # | Their words (abridged) | Price | Premise / Conclusion | Verdict |
|---|---|---|---|---|
| GR1 | "the model deducts the sovereign's own default spread… **This is an institutionally valid approach**" | — | Premise ❌ | **REJECT — and this is the arbitration that matters.** Two critiques say the deduction is wrong; this one blesses it. Coherence test in Part 3. Receipt: my own record C-06 |
| GR2 | "Because both of these alternative lenses are mathematically anchored to the **exact same Cost of Equity**… they are completely contaminated… a single discounted cash flow model dressed in varying mathematical costumes" | One input (rf) moves 3 of 4 lenses: at rf* 4.44% the centre falls 0.226 of which only 0.104 is the DCF leg | Premise ✅ Conclusion ⚠️ overstated | **ACCEPT the dimensionality point, REJECT "no independent verification".** Receipt: the book lens is driven by realised ROE (80.8%) and the relative lens by earnings — different numerators, shared denominator. Shared ≠ identical. But "four independent methods" overclaims and must go |
| GR3 | "If long-term volume growth stalls… the negative working capital cycle will **violently unwind**… The target model fails to adequately sensitize this terminal unwinding effect" | Unsensitised; a one-off unwind of the −1,797 NWC balance is worth ~**0.14/share** undiscounted | ✅ / ✅ | **ACCEPT — the best finding in this critique, and neither Claude critique made it** |
| GR4 | "The Quantitative Model Risk Group **outright rejects Frame B**" | — | Premise ✅ Conclusion ❌ | **ACCEPT premise, REJECT fix** (= GT4) |
| GR5 | "the Monte Carlo lens is **completely disconnected** from intrinsic valuation; it measures market noise" | nil | Premise ✅ Conclusion ✅ — and the study says exactly this | **ACCEPT — no change needed.** Receipt: §3 states the map "is a description of possible outcomes, not a forecast of one, and it is **entirely independent of the fundamental work above**" |
| GR6 | "This explicitly ignores the looming 15% Domestic Minimum Top-up Tax… destroys approximately AED [x] per share" | **Δps −0.261 (−5.9%)** at 15% | Premise ❌ Conclusion ⚠️ | **REJECT the premise.** Receipt: Code #21 — the FY2025 audited Pillar Two note applies the transitional CbCR safe harbour and concludes **no top-up tax**. The study does not "ignore" it; it follows the audited note. Both Gemini critiques miss the note that Code found |
| GR7 | "the USD [x] million acquisition of **Shell Downstream South Africa** is entirely excluded from the base case" | Excluded and **disclosed** as excluded | Premise ✅ Conclusion ❌ | **REJECT.** Receipt: the study states the exclusion explicitly ("THE BASE CASE IN THIS STUDY EXCLUDES IT"), and their own words concede "excluding unclosed M&A is standard zero-trust protocol" |
| GR8 | "the ownership structure… a 23% free float… This ownership dynamic is highly relevant for subsequent liquidity and governance discounts, **which the original model conspicuously omits**" | No number offered; none computed by them | Premise ⚠️ Conclusion ❌ | **REJECT with receipts.** A minority-stake liquidity discount is not standard in a fair-value range for a large-cap with AED 50.9bn capitalisation and 5–23m shares traded daily; and the finding is unpriced, which the procedure forbids. The free-float fact **is** disclosed in §Company overview |
| GR9 | "The market is actively pricing in a **permanent volume decline**" | — | Premise ❌ | **REJECT.** Receipt: the second edition's implied terminal growth is **+0.59%**, not negative. This repeats a claim from the first edition; it is what I corrected in the last turn. It is also inconsistent with GR's own Phase-1 table, which verifies the second-edition beta of 0.6494 |

---

## PART 3 — ESCALATIONS (anything above 5% of the centre)

Four findings clear 5%. Each gets an independent re-derivation from primary sources.

### E1 — The risk-free rate (Cowork #1, Code #9; contested by GR1)

**The arbitration, by coherence test, not by authority.** Two critiques say stripping 42bp
is wrong; Gemini_research says it is "institutionally valid". The deciding receipt is in
**my own research record**, entry **C-06**, which I wrote and did not act on:

> "Yields to maturity were 4.49% for the October 2027 T-Sukuk tranche and 4.48% for the
> January 2031 T-Bond tranche. **These corresponded to spreads of 24bp and 4bp respectively
> above comparable US Treasuries.**"

The normalisation rule exists to remove sovereign credit risk from the observed yield so it
is not counted twice. The amount to remove is the amount **actually in that yield** — 4bp,
not the 42bp generic ratings-based estimate. Stripping 42bp over-strips by 38bp and produces:

| Coherence test | Result |
|---|---|
| Published rf* 4.06% vs matched-tenor UST 4.44% | **−38bp** |
| Published rf* 4.06% vs US 10-year 4.65% (own record G-09) | **−59bp** |

An AED riskless rate **below** the riskless rate of the currency it is hard-pegged to is not
defensible. GR1's defence is that the ERP already embeds the country risk premium — true,
and irrelevant to whether the yield contained the spread being removed. **The premise and
the conclusion are both right, and the defence fails the coherence test.**

Bounded across every defensible construction:

| rf* construction | rf* | DCF A | Centre | vs spot |
|---|---|---|---|---|
| **Published** — 4.48 less ratings 42bp | 4.06% | 4.450 | 4.391 | **+7.9%** |
| (a) 4.5y observed, less the observed 4bp | 4.44% | 4.191 | 4.166 | +2.3% |
| (b) US 10y as the pegged riskless rate | 4.65% | 4.049 | 4.046 | −0.6% |
| (c) US 10y 4.68% | 4.68% | 4.030 | 4.030 | −1.0% |
| (d) constructed 10y AED 4.93 less 42bp | 4.51% | 4.119 | 4.112 | +1.0% |
| (e) constructed 10y AED 4.93 less 4bp | 4.89% | 3.894 | 3.917 | −3.8% |

**Every construction compresses the premium from +7.9% to between +2.3% and −3.8%.** There
is a second, separate defect inside this one that Code #9 states and Cowork does not: the
rate is a **4.5-year** point discounting a perpetuity with 74.8% of value beyond year five.
Term-matching and correct stripping compound.

**My recommendation: (a) as the published rate, with (b) and (e) shown as the tenor
sensitivity.** (a) is the only construction resting entirely on an observed instrument and
an observed spread. It is also the most conservative *against* the critiques' strongest
case, so it should not be read as me picking the friendliest number — (e) is available and
I am putting it in the sensitivity table rather than burying it.

### E2 — The normalised-earnings lens (all four critiques)

`NOPAT ÷ (WACC − g)` with no reinvestment charge, in a lens the study calls zero-growth
three times. **True zero growth = 3,204.1 ÷ 7.078% = 45,265 → 3.248/share** against a
published 4.222. At 25% weight: **centre 4.391 → 4.148 (−5.5%)**.

Premise and conclusion both right, unanimously. Two coherent fixes:
- **Relabel** it a growing perpetuity and charge reinvestment: `NOPAT×(1−g/ROIC) ÷ (WACC−g)`
  → 3,204.1×0.94 ÷ 5.578% = 54,000 → **3.947/share**
- **Recompute** as true zero growth → **3.248/share**

**Recommendation: charge the reinvestment.** The lens is meant to be "earnings power as it
stands", which is a going concern that must fund its own replacement — not a liquidating
annuity. Zero-growth-no-reinvestment (3.248) and growth-for-free (4.222) are both wrong;
3.947 is the coherent reading. And the *label* must change either way.

### E3 — The commercial margin step (Cowork #19, Code #25)

`C35` = +17% for FY2026, 8.5× the retail escalator, in a study that says "Margins are never
assumed" and "no margin assumption appears anywhere in this model". Removing it:
**Δps −0.329 (−7.4%)** — larger than the AED 0.313 inventory judgement the whole two-frame
apparatus exists to handle, and it appears in no sensitivity table.

Both critiques' cross-checks run partly in my favour: Code #25 confirms the *aggregate*
implied FY26 blended fuel margin (0.3819) sits inside the range H1-2026 disclosure implies
(0.383–0.395). So the aggregate is evidenced; **the retail/commercial split and the "never
assumed" claim are not.** Compounding it, Code #24 shows the leg is corporate and aviation
blended, moving in opposite directions (+53.9% vs −2.6%).

**Recommendation: carry it two ways like the inventory judgement, split the aviation and
corporate legs, and delete the "never assumed" claim.**

### E4 — Sensitivity scope (Code #8)

The study says "shifting the volume path down by one percentage point a year in **every**
forecast year takes the value from 4.45 to 4.24" and "a 10% cut to the margin growth path
across **both fuel legs** takes it to 3.95". My independent re-derivation:

| Described as | Published | All legs, re-derived |
|---|---|---|
| Volume path −1pp, every year | 4.24 | **4.125** |
| Margin −10%, both fuel legs | 3.95 | **3.696** |

The published cells are **retail-only**. This matters because §1.7 concludes "Volume alone
cannot explain the gap inside the explicit window — it has to be the terminal." At 4.125 the
full volume path lands **5.5 fils above the traded price**, so volume alone very nearly does
explain it. **This is the finding that most damages my own crux, and neither Gemini critique
found it.**

---

## PART 4 — BUCKETS

**Accept and implement (79):** CW 2–5, 7–18, 20–40, 44 (partial), 47; CD 1–10, 12–20,
22–28, U2, U3; GT1, GT3, GT5; GR2 (disclosure), GR5 (no change), GR3.
Plus E1–E4.

**Accept the defect, reject the proposed fix (6):** CW #25 (keep the conservative tax base,
disclose it), CW #37 (keep the single working-capital path, disclose it), GT2 (NCI —
real defect, wrong number, and the true fix is to stop flatlining NCI profit), GT4/GR4
(Frame B — keep it, sharpen the terminal-effect disclosure), GT6 (terminal weight is
disclosed), GT7 (working capital is not assumed in perpetuity).

**Unproven → research now (8):** CW #6 / CD #16 (ROCE — three different figures on offer:
32.7%, 40%, 44.4%; must be resolved from the MD&A), CW #45 / CD U6 (45-fils floor scope),
CW S1 (H1-2025 inventory 147m), CW S2 (retail/commercial inventory split), CW S3
(underlying EBITDA reconciliation), CW S4 (volume per station −9%), CD #11 (Brent spot),
CD #20 (H1-26 inventory 762 vs 672), CD U5 (inventory movement sourcing).

**Reject with receipts (7):** CW S5 (Egypt date — refuted by CD #23), GR1 (rf defence —
fails the peg coherence test on my own record C-06), GR6 (DMTT — the audited safe-harbour
note resolves it), GR7 (Shell SA — disclosed as excluded, and they concede the principle),
GR8 (liquidity discount — unpriced, and non-standard for a large-cap), GR9 (permanent
volume decline — implied growth is +0.59%), GT8 (AED 4.30 — built on the un-found
zero-growth error).

**Your decision (3):**

| Choice | Branch A | Branch B | My recommendation |
|---|---|---|---|
| Which rf* to publish | (a) 4.44%, observed instrument + observed spread → centre **4.166 (+2.3%)** | (e) 4.89%, tenor-matched → centre **3.917 (−3.8%)** | **(a)**, with (b) and (e) in the sensitivity table. Publishing (a) is the conservative choice *against* my own prior conclusion while resting only on observed data |
| The normalised lens | True zero growth → **3.248** | Growth with reinvestment charged → **3.947** | **Reinvestment charged.** Relabel either way |
| Frame B | Delete it (two critiques demand this) | Keep both frames, sharpen the terminal disclosure | **Keep.** The dual-framing rule requires it; deleting removes a disclosure |

---

## PART 5 — WHERE THIS LANDS

Correcting only what is arithmetic or definitional — not one matter of judgement:

| | Published | + rf* at 4.44% | + normalised lens with reinvestment | + justified-only reference multiple |
|---|---|---|---|---|
| Discounted cash flow | 4.450 | 4.191 | 4.191 | 4.191 |
| Normalised earnings power | 4.222 | 3.940 | ~3.70 | ~3.70 |
| Relative multiples | 5.094 | 5.000 | 5.000 | ~4.33 |
| Book value / sustainable return | 3.580 | 3.357 | 3.357 | 3.357 |
| **Weighted centre** | **4.391 (+7.9%)** | **4.166 (+2.3%)** | **~4.11 (+1.0%)** | **~3.97 (−2.5%)** |

**The direction of my conclusion does not survive.** The study's central claim — that the
price sits below what the cash the business generates is worth — compresses to inside its
own rounding on the first correction and inverts on the third. I am not going to defend it.

Three things are worth saying plainly in the other direction, because calibration cuts both
ways. The DCF machinery reproduces to six decimals in all four critiques. Every FY2025
input traces exactly to the audited accounts — Cowork verified ~34 line items, including
all three inventory-movement figures and every balance-sheet caption. And both margin-per-
litre unit builds derive precisely from disclosed segment gross profit less disclosed
inventory movements. The failures here are in **inputs, labels and claims**, not in the
model's arithmetic.

The most uncomfortable finding is not any single number. It is CW #10: the study asserts
"No data vendor, broker note or press report was used as the source of any number about the
company itself" while its own research record sources the share price and market
capitalisation to an aggregator. That is a declared contract broken by the document's own
appendix, and it is mine.

---

## PART 6 — RECONCILIATION

**103 raised · 103 answered · 0 unaddressed.**
Accept and implement 79 · accept defect / reject fix 6 · unproven → research 8 ·
reject with receipts 7 · your decision 3.

Nothing here is implemented yet. On approval I will implement, re-run every gate, and report
before/after plus any further defect the fixes surface.
