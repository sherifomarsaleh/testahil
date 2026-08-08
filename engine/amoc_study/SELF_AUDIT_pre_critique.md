# AMOC — SELF-AUDIT, written BEFORE reading the attached critiques
Build audited: compute.py @ 42cab0a, workbook 488 formulas, study 13pp, central EGP 7.1636.

## A. DEFECTS IN THE MODEL

**S1. Employees' profit share and BOD bonuses are registered and never deducted.**
Note 16 discloses EGP 67,467,871 for the audited half — about EGP 135mn a year, a real cash
distribution out of profit before it reaches a shareholder. `emp_h2_25` is in the input register,
is quoted in the documents, and is consumed by NO line of the model. It should reduce free cash
flow or sit as an expense. PRICE: ~EGP 135mn/yr on ~1,150mn of FCFF is roughly −8% of the
explicit window and, carried into the terminal, of the order of −EGP 0.55/share = −7.7% of the
central. NOT immaterial. This is the same class of defect the reachability sweep was built to
catch, and the sweep passes it because the documents quote it.

**S2. The tax-disputes provision is excluded from the bridge on thin reasoning.**
EGP 904.6mn (note 10-1) is recognised. The study's justification — "the earnings discounted here
are struck after the related tax charge" — conflates a forward effective rate on current profits
with a settlement of PAST disputed assessments. A recognised provision is a probable outflow.
PRICE: −EGP 0.70/share = −9.8% of the central. Above the 5% escalation line and I have not
re-derived it.

**S3. Capital expenditure below depreciation is carried for five years AND into the terminal.**
Capex is held at 0.86x depreciation and the terminal ROIC (22.9%) is computed on an invested
capital base that barely grows as a result. The optimism is therefore counted twice: once in
FCFF and once in the terminal return. §1.9 discloses the contradiction but the model does not
resolve it in either direction. PRICE: reverting capex to depreciation costs ~EGP 20mn/yr in the
window (small) but pulls terminal ROIC down toward the cost of capital, which is large. Unpriced.

**S4. The forecast gross margin sits above three of the four filed periods.**
Filed: 6.85% / 5.05% / 6.15% / 10.19%. Forecast opens at 7.17%. The base year is a 9-month blend
at 7.51%, so the forecast is BELOW the base — but ABOVE every filed period except the single
strongest quarter. The study says the base "blends rather than annualising Q1 alone" and stops
there. It does not say the forecast is above the median filed period. PRICE: reverting to the
6.15% audited half margin is roughly −EGP 1.3/share = −18%.

**S5. The 4/3 annualisation assumes no seasonality, and the data contradicts that.**
Q1-2026 margin 10.19% against the preceding half's 6.15% is a large seasonal or one-off swing.
Weighting Q1 at one third of the base year is a choice, not an identity. Unpriced and unstated.

**S6. `raw_pass = 1.0` was never tested against the currency path.**
Realised price growth is set at 9.0% falling to 5.2%; the FX path implies roughly 4-5% a year of
depreciation. So the model assumes real price growth above currency, while holding the raw
material charge at strict parity. Whether that is coherent was never checked.

**S7. Provision reversals are inside the disclosed "other revenue" and are non-recurring.**
Note 14-B: EGP 154.3mn of the 345.7mn other revenue in the half is "provision no longer
required". The model excludes other revenue from EBIT (correct) but the study nowhere warns that
nearly half of the disclosed other-revenue line is a reversal that cannot repeat.

**S8. The entire cost-of-capital stack is inherited and was never re-examined against the filings.**
rf, sovereign spread, ERP, beta, terminal anchors, cost of debt, cash yield — all carried over
from the pre-audit build. The filings give a finance-expense line of EGP 1.89mn and a
credit-interest line of EGP 173.2mn; neither was used to sanity-check the assumed cost of debt
(22.0%) or cash yield. The implied cash yield from the filings is 173.2mn on ~2.7bn average cash
= about 12.8% annualised, which is testable against the assumed path and was not tested.

**S9. The non-DCF lens ranges are inherited multiples that were never revisited.**
3.5x/6.0x on EV/EBITDA and 5.5x/9.5x on P/E come from the pre-audit build. The audited numbers
are materially different and the ranges were not re-derived.

## B. DEFECTS IN THE DELIVERABLES

**S10. The workbook lost seven sheets and the two standing gates.**
The original specification called for a 16-sheet workbook matching the reference study. The
audited rebuild is NINE sheets: Monte Carlo, Sensitivity, Per-Share & Ratios, Peer & Sector,
Income Statement, Balance Sheet and Cash Flow as separate sheets are all gone. Formula share fell
from 84.0% to 72.4%. `recalc.py` and `driver_test.py` were NOT rebuilt for the new structure — I
ran an inline equivalent of recalc once and never re-ran the driver test at all. The standing
gates are therefore not in place on the delivered file. This is a regression I did not flag.

**S11. The study fell from 25 pages to 13 and lost whole sections.**
Gone: the three-expert appendix, Appendix B on the cost of capital in detail, the peer and sector
work, the contested-choices table, the scenario-definition table, the terminal-growth crossover
test. I reported the page count as a fact and did not report the loss of scope as a loss.

**S12. The QC gate (a)-(r) has not been re-run against the audited build at all.**
QC_GATE_06-08-2026.md still describes the superseded per-tonne construction and quotes EGP 9.3818
as the central. It is stale and internally contradicts the shipped study.

**S13. Two of the four filings supplied were barely used.**
`2023.pdf` was never read beyond confirming it exists. `2024.pdf` was read for one balance sheet
page only. Those documents very likely carry product tables and cost stacks for earlier periods,
which would let the cost composition's STABILITY be tested rather than assumed from one half.
That is the single largest piece of available evidence left on the table.

**S14. Three generated figures are now orphaned.**
figures.py still emits fig5_dist, fig6_dist and figD1_experts; the 13-page study references
none of them.

**S15. The live site still publishes the superseded EGP 9.38.**
Flagged repeatedly but not fixed, and it is the only artefact a member of the public can see.

---
# RECONCILIATION AGAINST THE FOUR ATTACHED CRITIQUES
Written AFTER reading them. The list above is unedited from before.

## Findings they also caught
- S1 (employees' profit share never deducted) = Cowork #4. Same defect, same direction.
- S2 (tax-disputes provision excluded) = Gemini deep research §2.3.
- S5 (4/3 annualisation assumes no seasonality) = Gemini deep research §1.2.
- S8 (cost-of-capital stack inherited, never re-checked) = Cowork #6, #7, #19, #24 — and they
  went further, checking each against a primary source and finding actual errors.
- S9 (lens ranges inherited, never re-derived) = Cowork #29 (bear/bull unreproducible).

## Findings they missed
- S11 (the study fell from 25pp to 13pp and lost whole sections)
- S12 (QC_GATE_06-08-2026.md is stale and still quotes the superseded 9.3818)
- S13 (2023.pdf and 2024.pdf were barely used)
- S14 (three orphan figures)
- S15 (the live site still publishes the superseded 9.38)

## Findings I MISSED, verified where checkable
- **Cowork #1 — the 1 Jan–30 Jun 2026 disclosure.** Released to the EGX 29–30 July 2026, a week
  BEFORE the study's own anchor date. Confirmed from this repo's history: `rev_h1cy26_rep`
  (26,200mn) and `pat_h1cy26_rep` (1,900mn) were live inputs at commit 2e54245 and were DELETED
  in the audited rebuild — after which §1.2 argues no clean twelve-month period exists. Twelve
  months to 30-Jun-2026 = revenue 46,959mn, GM 9.65%. Priced by the critic at +96% to +113% on
  the DCF lens. ABOVE THE 5% ESCALATION LINE BY A FACTOR OF ~20.
- **Cowork #2 — period mismatch inside the gross-profit line. CONFIRMED BY COMPUTATION:**
  revenue engine base = 6M product table x2 = 41,471.5; cost engine base = 9M x 4/3 = 38,535.1;
  implied base margin 7.081%, which is neither the filed 6M 6.145% nor the stated 7.506%. The
  study's claim that the 4/3 scaling "is the only step between the filings and the base year" is
  false.
- **Cowork #3 — lens 3 undiscounted.** The SAME defect the first critique round raised and that
  was fixed in the pre-audit build. It regressed in the rebuild.
- **Cowork #8 — probability zones sum to 103.4%. CONFIRMED** on the delivered PDF, and one band
  prints descending ("EGP 7.50 – 7.16").
- **Cowork #13 — the study's headline caveat is backwards.** capex/depreciation runs
  0.99 / 1.11 / 1.24 / 1.37 / 1.50; capex already EXCEEDS depreciation from 2027. Setting capex =
  depreciation would RAISE the value. §1.9 and §7 assert the opposite. My own S3 repeated the
  same error.
- **Cowork #11 — t=0 is 31-Dec-2025**, not the 6-Aug-2026 price the answer is compared against.
- Cowork #9, #15, #22, #23, #25, #30 — sensitivity rows that do not reproduce, dividends payable
  inside net working capital, a "weighted" range that is an unweighted min/max, and an
  Appendix A.2 that does not foot. Not yet independently verified.

## One critic premise that is wrong
Cowork Section A states the workbook "was shipped with no cached values". It carries 488 cached
values against 488 formulas — verified in the sheet XML. This made their recomputation harder
than necessary; it does not affect any of their findings.

## Status of the procedure
Step 1 complete. Steps 2-7 NOT done: ~100+ findings across four documents, each requiring a
price, a premise/conclusion split and receipts. Not started rather than partially done.
