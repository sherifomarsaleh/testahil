# STC — what stands between the rebuilt model and a delivered study

**5 September 2026.** The rebuild is finished and every gate it can reach is green: twelve
levers over ten rules, a 176-row four-field input register, the macro and forecast-anchor
records, the bridge on the latest disclosed sheet, the terminal on a disclosed asset life,
the Step 2A sweep through the shared register. What does not exist is the *delivered study* —
no Word document, no workbook, no bibliography, no QC gate.

This file is the scoped list, written because the alternative is discovering it one traceback
at a time. It was produced by trying to build the document and reading what broke.

## The finding that matters: the model stops at EBITDA

The old document builder resolves **thirteen** forecast fields. The rebuilt model publishes
**seven**, and only one of the thirteen survives.

- the document asks for: `att`, `cbu`, `dna`, `eb`, `ebit`, `ebu`, `npc`, `oth`, `pbt`, `rev`, `sub`, `wc`, `zk`
- the model publishes: `ebitda`, `ebitda_margin`, `elim`, `gp`, `gross`, `rev`, `sga`

The missing twelve are not a renaming. The delivered study was built on **business units**
(`cbu`, `ebu`, `att`, `oth` — consumer, enterprise and the rest) and the rebuild replaced
those with the **eleven disclosed operating segments** of note 9, which is the whole point of
[R-SIGCM-02]'s finest-sourced-level rule and is not going back. The others — `ebit`, `pbt`,
`zk`, `npc`, `dna`, `wc`, `eb`, `sub` — are an income statement the rebuilt model never
projects, because **the valuation does not need one**: free cash flow to the firm runs off
NOPAT, and NOPAT comes from EBIT and a tax rate without ever passing through a finance charge.

**That is the [R-FCAL-01] amendment's own lesson arriving from another direction.** What a
process commits decides what can be asked of it later, and nobody notices the missing field
until the question arrives. The rebuild was correct, careful and well evidenced, and it
answered the question it was built for — what is this company worth — while leaving no trace
of the figures beside it. Appendix A is the question arriving.

### What the model already carries, so the gap is smaller than it looks

The discounted cash flow rows carry `capex`, `df`, `dna`, `dwc`, `ebit`, `ebitda`, `fcff`, `nopat`, `pv`, `rev`, `year` — so EBIT,
depreciation, NOPAT, capital expenditure and the working-capital movement are all projected
already. The historicals carry `assets`, `capex`, `cash`, `debt`, `dna`, `dps`, `ebit`, `ebitda`, `eq_att`, `fcf`, `gp`, `nci`, `np_att`, `np_cont_att`, `ocf`, `rev` for three filed years.

## The ordered list

1. **The forecast income statement, down to net profit.** Needs a net finance charge, profit
   before zakat, the zakat charge and the minority's share. The debt book is committed
   facility by facility with its own rate and the adopted cost of debt is the January 2026
   sukuk. What is NOT yet decided is the debt PATH, and holding gross debt flat is a stated
   assumption rather than a free one — it has to be written down as such.
2. ~~**The forecast balance sheet and cash flow.**~~ **HALF DONE, AND THE OTHER HALF IS
   BLOCKED BY THE FILING ITSELF.** The asset-conversion cycle is studied and committed
   (`working_capital.py`) and the working capital is now projected from it rather than
   plugged — which found that net working capital more than doubled in FY2025 while the plug
   said the outflow shrank. THE FORECAST BALANCE SHEET IS NOT BUILT: the reviewed interim's
   own balance sheet **does not foot in its current column** — four subtotals and both
   totals — while every prior-year column foots exactly, on the PDF's text layer and on OCR
   off the rendered pixels alike (`balance_sheet.py`). A statement is accepted only if it
   foots against its own arithmetic. The lines the bridge uses are corroborated by the
   interim's own cash-flow statement instead, to the riyal. Unblocked by the FY2026 audited
   statements or a corrected interim; **Appendix A.2 and A.3 wait on that**, and the study
   says so rather than projecting from figures that do not add up.
3. **A live formula model, not a table of values** (SIGCM clause 7): driver to income
   statement to balance sheet to cash flow to discounted cash flow, blue for input and black
   for formula, recomputing when a driver moves. Sixteen sheets in a fixed order, and the
   shape is read off the delivered file rather than attested.
4. **The three document parts, re-pointed.** The skeleton is broadly right — the old study
   already carries sections 1 to 7, appendices A to C, About and Disclosure — so this is
   re-binding rather than re-writing. Two content corrections ride with it: section 4 is
   titled "Comparison of the lenses, and a verdict", and section 3 leans on a calibration
   appendix that depth-bar standard 4 forbids outright, the evidence belonging in section 3
   as plain-language sentences with the statistics inline.
5. **The reconciliation script**, so every figure a reader sees is matched against the
   committed numbers. STC is the study the prose-figure gate reports as having none.
6. **The standalone bibliography**: the primary-documents table, the full input register
   grouped by research layer, the judgements table each with what would overturn it, and the
   negative-results table. The input register now exists and is generated, so this is a
   rendering job rather than a research one.
7. **The QC gate**, filled from outside the study, every row naming the artefact, command or
   number that carries it.

## What is deliberately not on this list

Publishing. STC is held on both [R-GAP-02] conditions — its central sits -15.27% below the
latest known price, and Phase 1 of the method reassessment is not proven — and neither is
what this list is about.

## The figures are done and are the one part already finished

Nine, all rebuilt on the current numbers, all opaque and verified by reading the alpha
channel rather than trusting the setting, and the first of them no longer publishes the
retired weighted blend.
