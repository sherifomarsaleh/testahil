# SWDY — response to the external forensic audit of 13-09-2026

**STEP 8 REPORT. Nothing has been implemented.** Procedure: `engine/Critique_Response_Prompt.md` v2.

## Count reconciliation

The audit's own summary strip declares **16 total fail + 23 partial + 3 unverifiable = 42**.
The document carries **41 findings with identifiers** (F1-F41): 16 total, 23 partial, **2** unverifiable.
One declared unverifiable is counted in the strip and carried as no numbered finding. **41 raised
and enumerated, 41 answered, 0 unaddressed — plus one declared-but-unnumbered item flagged back
to the auditor.**

## How this response verified the audit rather than reading it

Every price below marked REPRODUCES was re-run independently: the study's own `compute.py`,
copied to a sandbox, one input patched, the central re-read. Seven of nine re-runs match the
critique to four decimal places. **The audit's model reconstruction is accurate** and its
arithmetic is its own, not asserted.

Two prices do not match and are reported as mine rather than theirs (F4, F15); one matched only
on the second construction (F8).

**The harness itself had the defect it was built to price.** Its first run returned "no change"
on every case because the sandbox carried the committed `study_numbers.json` and a failed
`compute.py` left it in place — an absent result read as a clean one [R-ENF-04]. Fixed before any
number below was taken.

## The ledger — one row per finding, in the audit's own order

| # | Sev | Finding | Price (EGP/share, % of 87.94) | Verification |
|---|---|---|---|---|
| F1 | total | The corporate cost load: the prose describes the retired path | **53.9962** (-33.9463, -38.6%) | CONFIRMED from the numbers file: opex_pct = 3.07% flat in all five years, BELOW FY2025's 3.16%. The prose says it "glides UP ... toward the FY2023-24 average, the single most conservative choice in the build". It does not. — REPRODUCES the critique exactly (it said 54.00 / -33.95 / -38.6%) |
| F2 | total | Table 14's capital-expenditure row is the retired path; the model holds capex flat | **87.1387** (-0.8038, -0.9%) | CONFIRMED: model capex/revenue = 3.5742% in every year; the registered capex_pct taper [4.4, 4.0, 3.6, 3.3, 3.1] that the driver table prints drives nothing. — REPRODUCES exactly (critique: 87.14 / -0.80). Surfaced by compute.py's own scenario assert |
| F3 | partial | “Holding capex at the FY2025 peak would cost roughly EGP 1.8” | **79.6549** (-8.2877, -9.4%) | REPRODUCES exactly (critique: 79.65 / -8.29). The study prints "roughly EGP 1.8" — understated 4.6x |
| F4 | total | The published Cables FY2026 driver is read by no formula in the model | **81.2480** (-6.6945, -7.6%) | CONFIRMED AND WORSE THAN STATED: FY2026 Cables grows at 30.5683% (the H1-2026/H1-2025 ratio). compute.py carries an assertion that REFUSES the published 10.71% outright. The two rows are mine, added 13-09-2026. — MATERIAL, price differs: critique says 83.52 / -4.42. Mine applies volume x pass-through, theirs +10.7% flat. Both clear the 5% escalation bar |
| F5 | total | The forecast is calibrated on the reviewed half, which the study never mentions and lists as a future catalyst | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F6 | total | Segment margins are inputs, not outputs | Impact: none on the central directly, but the margin row is the largest single sensitivity in the study (±15% = 74.00 a share, wider than any cost-of- | price as the audit states it; not independently re-run in this pass |
| F7 | total | Table 18's cost-of-capital rows do not produce Table 18's cost of capital | Impact: the model run at the literally printed cost of capital gives EGP 56.97 — −30.97 / share, −35.2%. Correct method: print the two legs as separat | price as the audit states it; not independently re-run in this pass |
| F8 | partial | The study's own stated country-premium arithmetic does not reproduce either | **96.2291** (+8.2865, +9.4%) | CONFIRMED: crp_eff = 3.984% committed, lambda = 0.5928, crp_home = 5.168%. 5.168 x 0.5928 = 3.064, not 3.984. The 2.26% non-Egypt leg is in no delivered page. — REPRODUCES exactly once applied to BOTH windows (critique: 96.23 / +8.29). Explicit window alone gives only +1.05 |
| F9 | total | The terminal risk-free rate is published on a 5% inflation the terminal growth rate contradicts | Impact: applying the printed 5.5pp real convention to the study's own 7% inflation gives a terminal risk-free of 12.5% → EGP 66.62 (−21.33, −24.3%). M | price as the audit states it; not independently re-run in this pass |
| F10 | total | The published headline range is generated on retired terminal-growth parameters, and its bear case is internally contradictory | Impact: the range a reader is given is not a range around the published answer under the published assumptions. Correct method: re-run both scenarios  | price as the audit states it; not independently re-run in this pass |
| F11 | total | The published copper sensitivity is a mathematical no-op in the published model | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F12 | total | The bridge does not stand on the latest disclosed balance sheet | Impact: bridging on the 30-Jun-2026 sheet with a 65-day roll gives EGP 77.32 (−10.62, −12.1%) — an upper bound, since that construction should also dr | CONFIRMED FROM THE STUDY'S OWN REGISTER: h1_26_debt 84,005.21 less h1_26_cash 55,376.24 = 28,629.0 net debt, exactly the critique's figure, against the 20,560.0 the bridge subtracts. — price as the audit states it; not independently re-run in this pass |
| F13 | total | The H1-2026 effective tax rate of 30.85% was read, registered, flagged as material — and not priced | **73.4550** (-14.4875, -16.5%) | CONFIRMED: the register's own h1 26 tax entry says "a material step this re-issue must price rather than average away". It is priced nowhere in the study. — REPRODUCES exactly (critique: 73.45 / -14.49 / -16.5%) |
| F14 | partial | The register carries the same tax rate under two different periods | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F15 | partial | Copper is not “held near the current market level”; it escalates 2.5% a year | **85.2050** (-2.7375, -3.1%) | Critique says 85.87 / -2.07. Mine flattens from FY2027 on the house US-inflation term; same sign, same order |
| F16 | partial | 19.67% working capital is an H1-2026 figure described as “the FY2025 disclosed level” | **87.1967** (-0.7458, -0.8%) | CONFIRMED: nwc_pct = 0.1967 committed; FY2025 disclosed = 55,852.5/281,049.1 = 19.873%, and Table 17 prints 19.9%. — REPRODUCES exactly (critique: 87.20 / -0.75) |
| F17 | partial | A capital reduction the register denies exists is filed with the exchange | Impact on value: negligible — on the correct count the central is 88.00 rather than 87.94, and market capitalisation at the anchor is 278,116 rather t | price as the audit states it; not independently re-run in this pass |
| F18 | partial | SWDY is not an EGX30 constituent, and the beta's stated justification depends on its being one | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F19 | total | Table 6, “The valuation, on one page”, does not foot | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F20 | total | The normalised-earnings row label omits a third deduction worth 14.62 a share | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F21 | total | The relative lens's interim cash-flow row has the wrong sign, and three statements about it are backwards | Impact: as printed the lens is 76.96 against the published 79.68 — the row misstates its own lens by 2.72 a share and inverts a fact the document esta | price as the audit states it; not independently re-run in this pass |
| F22 | partial | The working-capital sensitivity row does not pass through the published central, against an explicit assertion that every grid does | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F23 | partial | Three of Table 20's six contested-choice valuations understate themselves by 2.5× to 8× | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F24 | partial | Nine prose claims contradicted by the tables printed beside them | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F25 | partial | The risk-free rate is not read on the anchor date, and the study says it is | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F26 | partial | The bibliography's judgements table publishes three retired values as adopted | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F27 | partial | The study and its register give two incompatible accounts of what the multiple rests on — and the study's account is the one that fails | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F28 | total | The price map's stated drift does not reproduce from its own published medians | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F29 | partial | The zone map omits 40% of the distribution it maps | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F30 | partial | The technical section is stale at the issue date the document carries, and mixes closing and intraday bases | Impact on the valuation gap: immaterial — at 127.10 the central sits −30.8% rather than −32%. | price as the audit states it; not independently re-run in this pass |
| F31 | partial | Two register entries about the same reviewed half: a mis-sequenced backlog series and a misattributed transformer contract | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F32 | partial | Expert 1's earnings per share reproduces on no published combination; Expert 2's printed formula does not reach its own answer; Expert 3 drops a charge the central bridge makes | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F33 | partial | The terminal capitalises a return above every year in its own forecast, at the end of a window still compounding at twice the terminal rate | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F34 | unver | The beta triple is not self-consistent on the construction the study prints | Impact: small either way. Beta multiplies only the 4.24% mature leg, so the full tested 0.6–1.3 range moves the answer 4.87 a share. | price as the audit states it; not independently re-run in this pass |
| F35 | partial | Minor foot-checks and citation slips | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F36 | total | The study's “single largest open question in the cost of capital” switches two things at once, and the data source alone moves the answer the other way | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F37 | partial | The risk-free rate on the anchor date is 22.97%, not the 22.31% adopted | Impact: at 22.97% the central is EGP 87.20 (−0.74); at 23.00%, 87.17. Immaterial on its own — but the study's own framing, that it chose the generous  | price as the audit states it; not independently re-run in this pass |
| F38 | partial | The US risk-free rate is 4.68–4.77%, not 4.30%, so the currency-of-discounting alternative is struck too cheap | Impact: the published alternative of EGP 77.86 is struck 35bp too cheap and is therefore modestly too high. The study's conclusion from it — that the  | price as the audit states it; not independently re-run in this pass |
| F39 | unver | The registered USD/EGP annual averages sit 3% below the market averages, and are cited to a note this audit could not read | Valuation impact: nil. Only year-on-year exchange-rate ratios enter the model, and FY2026 Cables revenue is hardcoded, so rebasing the entire path on  | price as the audit states it; not independently re-run in this pass |
| F40 | partial | The employees' statutory charge is described against the wrong statutory base | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
| F41 | partial | The company profile understates the operating footprint by a factor of four | _no valuation effect claimed_ | price as the audit states it; not independently re-run in this pass |
