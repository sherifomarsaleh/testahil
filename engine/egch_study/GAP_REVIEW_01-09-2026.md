# EGCH (KIMA) — valuation gap review [R-GAP-01]

**1 September 2026.** The rebuilt central fair value is **EGP 3.79** (field EGP 0.00 to
15.47) against the latest known market price of **EGP 13.98** (the last close in the
price library, 6 August 2026) — **72.9% below**. Under [R-GAP-01] a central more than 10%
below the price is a claim about the world and is audited like one before it ships. Eight
headings, none invented; each individually capable of producing the whole gap. The
previous edition (8 August 2026) printed EGP 3.64 against the same price and was on the
gate's outstanding list as *unreadable* (its numbers file exposed no central/spot pair);
this edition exposes both.

**Verdict in one line:** the audit found and fixed two defects (terminal inflation
incoherent with terminal growth; a typed superlative), found one open construction
that is priced but not adopted (tax at the statutory rate on a company that pays none),
and otherwise the discount is a *conclusion* — about a capital programme that on the
disclosed cost and nameplate does not earn its cost of capital, and about an Egyptian
cost of capital that the market price does not use. It is published both ways.

---

## LATEST FILINGS

Every disclosed period has been read, not merely downloaded:

| document | period | read | used for |
|---|---|---|---|
| Reviewed interim, nine months to **31 March 2026** (limited review dated 20 May 2026) | 9M FY2025/26 | income statement, balance sheet, cash flow, auditor's letter — read from the rendered pages this session and footed (PBT 520,569k; net 531,310k; revenue 7,314,933k) | base year, bridge, auditor's flags |
| Reviewed interim, six months to 31 December 2025 | H1 FY2025/26 | read (revenue 4,156,379k; net 1,190,045k) | quarterly path |
| Reviewed interim, three months to 30 September 2025 | Q1 FY2025/26 | read (revenue 1,184,805k; net 482,705k; the auditor's gas-loss and project-progress figures) | gas price, project progress |
| Audited statements, year to 30 June 2025 (CAO report 23 Sep 2025) | FY2024/25 | read and footed this session from the filing itself (revenue 8,602,606k; net 986,964k) | last audited year |
| Audited statements FY2021/22–FY2023/24 | | read and footed this session from each filing's own column | history |
| Audited statements, years to June 2009–2021 (ten filings) | | retrieved 1 September 2026 from the company's own portal, read and footed | the calibration of the method, not a forecast driver |

**The most recent document is the nine months to 31 March 2026.** No later document
exists: the company's portal listing could not be re-read on 1 September (a 709-byte
stub on retry) and the FY2025/26 annual, on the company's own pattern, is filed in
September–October. Nothing downloaded was left unopened.

## BASE YEAR

The base year FY2025/26E is **nine reviewed months plus one run-rated quarter** and the
document says so in Appendix A: revenue 7,314,933k reviewed + a fourth quarter at the
third quarter's revenue (3,158,554k) × 0.97 for the summer gas curtailment = 10,378.7m;
gross profit = the reviewed 3,134,979k + the run-rated quarter at the third quarter's
46.3% margin = 4,553.5m (43.9%); selling and administrative scaled 4/3 on the nine months.
Every constituent foots to a filed period. Nothing is solved from the profit line. The
run-rated quarter is 29.5% of base-year revenue; the third quarter's margin (46.3%) is
the highest quarter on the record, so the base gross margin (43.9%) sits above the last
audited year (38.4%) — stated, and the currency line is set to zero because a
translation swing is not forecastable. The base net profit is the nine-month reviewed
figure (531,310k), not annualised, because the nine-month translation loss (1,072m)
exceeded the nine-month profit.

## MACRO COHERENCE

**One path, now.** Domestic inflation follows the central bank's own target ladder (10%,
7%, 6%, 5%, 5% — 7% ± 2 for Q4 2026, 5% ± 2 for Q4 2028); the currency is *derived* from
that path year by year on the relative purchasing-power identity against 2.4% US
inflation (49.79 → 53.49 → 55.89 → 57.85 → 59.32 → 60.83); the export price is a dollar
commodity path (530 → 440 US$/t, mean-reverting from the August 2026 quote) translated
at that currency; gas is an administered dollar price translated at the same currency;
the dollar debt is carried at a local-equivalent cost built on the same wedge.

**What was incoherent and is fixed:** the 8 August edition typed a currency path at "4.5%
a year" beside a derivation that produced a different number every year, and it
compounded the terminal risk-free rate on the 7% Q4-2026 target while growing the
perpetuity at the 5% Q4-2028 target. The register now carries the derived path itself,
and the terminal inflation equals the terminal growth. This is L-048 and L-055 applied
before the answer was read, not after.

## DISCOUNT RATE

Rating basis: rf* 16.63% (23.00% ten-year less Egypt's own 6.37% default spread) + β
1.030 × ERP 13.94% = **Ke 30.99%**; after-tax cost of debt 11.28% on a book that is 99.7%
dollar (11.7% in dollars grossed up by the depreciation wedge); market-value weights
65.5% / 34.5% on **gross** debt of EGP 14.64bn → WACC 24.18% in year one, gliding to a
terminal 18.23% built from 5% inflation, a 3.5% real rate, the same β and ERP, and a
long-run dollar cost of debt.

**Cash is charged for exactly once.** The weights use gross debt (positive debt weight,
equity weight below one — the L-054 failure cannot occur), and the bridge subtracts *net*
debt (gross 14,639m less cash 4,607m = 10,032m) and adds the listed stakes (1,383m) and
investment property (2,155m) at their 31 March 2026 carrying amounts. The operating cash
flows are discounted at a rate below the cost of equity, as they must be.

**The beta is conforming**: 1.030 against the published EGX30 through
`beta_regression.own_stock_beta()`, attested by `assert_beta_provenance()`; the 8 August
composite beta (1.053) is withdrawn. The change is −2.1% on beta and +EGP 0.15 on the
carried-through cash-flow value (the terminal fix is the larger mover, −0.67 → −0.56).

**What the audit notes without changing:** the terminal cost of equity is 23.0% nominal on
5% inflation — a real 17% in perpetuity — because the house method carries Egypt's Caa1
country premium (9.71% of the 13.94% ERP) for ever. That is the v2 cost-of-capital method
applied as written, and the CDS-basis alternative (+EGP 0.75) is priced in section 1.8.
The market price implies a *flat* nominal discount rate of 7.8% on the committed-capital
case and 9.0% on the capital-discipline case — below the sovereign's own 23% yield. That
is the whole of the disagreement with the price, and the study says so.

## TERMINAL

Terminal growth **5.0%** = the inflation inside the terminal rate (5.0%) → **zero real
growth**, stated. Terminal EBIT 2,296m = the year-five urea business grown once (2,362m)
plus the new nitrate complex at half its nameplate, which after its own depreciation
contributes −66m; NOPAT 1,779m; reinvestment 27.8% (g / an 18% return on capital); FCFF
1,285m; value 9,713m at a 13.23% cap rate; present value 3,625m = 67% of enterprise
value. The previous edition's terminal (7% inflation in the rate, 5% growth) implied a
perpetual real decline of about 2% a year that nothing disclosed; corrected.

The terminal is where the answer lives and the two cases are both published: with the
programme carried through the equity is worth −0.56 a share; stopped, 3.59. The
disagreement is EGP 4.14 a share and is the study's contested judgement, never averaged.

## BALANCE SHEET

The bridge stands on the **31 March 2026 reviewed statement of financial position** — the
latest disclosed: cash 4,606.5m, bank loans 14,386.1m + current portion 207.0m + holding
company 45.9m, listed stakes at fair value 1,382.9m, investment property 2,155.1m,
construction in progress 5,653.5m (the programme's spend to date, 27.8% of the approved
cost), equity 16,206.1m. The auditor's letter on that period flags an unmarked ABUK stake
(+112m unbooked), an 11.6kt Damietta stock overstatement (116m), unissued electricity
invoices (49.7m accrued) and 27.6m of under-booked loan interest; together they are
under EGP 0.10 a share and are listed in section 7 rather than adjusted for.

## CLAIMS AGAINST THE RECORD

Every superlative in the delivered document was searched for and recomputed:

- *"almost three times anything this company has ever spent to keep this plant running"*
  (the maintenance-capex paragraph) — **false as worded**. Three per cent of revenue is
  2.7 times the *pooled* pre-project rate (1.12%) but only 1.65 times the higher of the two
  pre-project years (1.82% in FY2021/22). Replaced by the two computed ratios, driven off
  the register, never typed (L-056).
- *"The company has never spent EGP 3,000m in a year on this project"* — **true** on the
  filed record: 2,396.6m (FY2023/24), 1,545.1m (FY2024/25), 1,949.1m in nine months of
  FY2025/26 (2,598.8m at a full-year rate).
- The base-year note that the third quarter's 46.3% gross margin is used for the fourth —
  the quarter *is* the highest on the disclosed quarterly record (Q1 32.9%, Q2 43.1%, Q3
  46.3%); the document states the run-rate and the 3% haircut rather than calling it a
  record.

## MULTIPLE CROSS-CHECK

At the market price: market capitalisation EGP 27.8bn; enterprise value (net debt added,
non-operating stakes and property deducted) EGP 34.3bn; **EV/EBITDA 11.2× on the last
audited year, 8.4× on the base year, 7.3× on the first forecast year; P/E 28× on the last
audited year, 39× on the nine months annualised; 1.7× book.** Named Egyptian
comparables trade at 4.4× (Ezz Steel) to 8.2× (Abu Qir) to 11.5×–17.6× (EFIC, SKPC) on
the same basis; the relative lens at 6.0–9.9× centres at EGP 15.47, *above* the price,
and it is the one lens that reaches the price — by never charging the capital programme.

At the rebuilt central: enterprise value 5.4bn = **1.2× first-year EBITDA**. The gap
between 1.2× and 8× is arithmetic the reader can follow: the explicit window's free cash
flow (1,963m, 298m, −156m, −219m, 450m) is consumed by EGP 14.7bn of programme spend, and
the terminal value capitalises a business whose EBIT falls from 3,793m to 2,250m as the
export price mean-reverts against a cost base inflating at the central bank's target,
plus a complex that earns nothing after its own depreciation, at an 18.2% rate. Every one
of those is a stated, sensitised driver; none is a defect the audit could find.

**The one open construction the audit surfaces, priced and not adopted.** The model charges
tax at the statutory 22.5% on EBIT from year one — EGP 853m, 762m, 643m, 554m, 506m, a
present value of EGP 1,968m, **EGP 0.99 a share**. The company has booked no current tax
in any year of the new complex (only deferred credits: +234m FY2023/24, +11m FY2024/25,
+30m in the nine months), and its own calibration record (the fundamental walk-forward
run beside this edition) measures the statutory-rate formula as the second-largest source
of profit error on this name. The mechanism — loss carry-forwards from the FY2020–FY2021
losses of EGP 1.70bn before tax and the accelerated first-year deduction on new plant —
is not sourced in this edition's register because the deferred-tax note has not been read
at the line level, and an unsourced tax holiday would be a fabricated driver. The audit
therefore states the size (EGP 0.99 a share on the explicit window, a bound), carries it
in section 7 as what would move the answer up, and leaves the statutory rate in place.
Adopting it would move the central from 3.79 to about 4.78 — still 66% below the price.

---

**Conclusion.** Two defects fixed (terminal inflation, a typed superlative: net +EGP 0.15
on the carried-through lens), one construction priced and left open (+EGP 0.99 bound),
and the remainder is the study's conclusion stated in its own units: at the market price
a buyer is paying 8.4× base-year EBITDA for a plant that must fund a EGP 14.7bn programme
earning, on the disclosed cost and nameplate, less than its own depreciation — and is
discounting the whole thing at 7.8% in a country whose sovereign borrows at 23%. The
central stays at EGP 3.79 in a field of 0.00 to 15.47; `scripts/check_valuation_gap.py`
is cleared by this review's existence and its eight headings, not by a changed answer.
