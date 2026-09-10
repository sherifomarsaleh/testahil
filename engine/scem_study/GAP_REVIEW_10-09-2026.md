# SCEM — GAP REVIEW, 10-09-2026  [R-GAP-01]

[R-GAP-01] AUDITED CENTRAL: 122.67 — EGP 122.67 a share.
[R-GAP-01] AUDITED GAP: +22.1 per cent against the price this edition is STRUCK at,
EGP 100.50, the close of 2026-09-02 from the price file committed at
engine/prices/SUPPLIED_03-09-2026.json.

THE NEWEST PRICE THIS REPOSITORY HOLDS IS NEWER STILL AND IS DISCLOSED RATHER THAN
QUIETLY IGNORED: the persistent library at engine/raw_ohlc/EG/SCEM.csv closed at
EGP 98.52 on 2026-09-06, which puts the same central at +24.5 per cent. No heading
below answers differently against one price than against the other — both sit on the
same side and inside the same band — and re-striking on the library close remains a
SEPARATE lever, because the spot enters the market capitalisation and therefore the
equity weight in the cost of capital.

THIS FIRES ON THE HIGH SIDE, AND THE MISTAKE WOULD HAVE TO BE AN OPTIMISTIC ONE.
The question below is not whether the market is right. It is whether WE made an error
in the company's favour.

## WHAT MOVED SINCE THE 07-09-2026 REVIEW: ONE LEVER, AND IT IS A HOUSE LEVER

  111.62   the 07-09-2026 edition, audited at +11.1 per cent
  +9.9%    the TERMINAL RISK-FREE RATE, 12.50% -> 10.50%
  122.67   this edition

Nothing else changed. The forecast, the bottom-up cost stack, the terminal life, the
bridge and the lens weights are as they were on 7 September, and a reader can hold the
two documents side by side and find one number and its consequences between them.

**WHAT THE LEVER WAS.** This study TYPED its terminal risk-free rate into its own input
register — the central bank's 7% inflation target plus a 5.5 percentage-point
"emerging-market real-rate convention" — and the note beside it flagged the alternative
in its own words as a "REVIEWABLE CHOICE: reverting to 10.5% adds ~1.8%". That is a
defect recorded rather than fixed, and it sat in the register through three editions.

The house Egyptian macro path carries the convention at 3.5%. The retired 5.5% was a
description of a RESTRICTIVE POLICY STANCE — the real rate a central bank runs in order
to break an inflation — and a cement plant does not live inside a policy stance in
perpetuity. Charging one for ever taxed this company permanently for a monetary
condition that is by construction temporary. The rate is now read live from
`engine/macro_paths/EG.json` and cannot be set by this study at all.

**THE DIRECTION IS NOT THE REASON.** This correction raises the value and moves it
further above the traded price. It would have been made had it done the opposite, and
the house rule that a fair value is never adjusted toward a quotation cuts both ways —
which is exactly why a gate that fires in only one direction was replaced by one that
fires in both.

---

## 1. LATEST FILINGS

Unchanged from the 07-09-2026 review and re-verified against the directory: the company
publishes six documents and all six are on disk and read. `SCC-AFS-E-1225.pdf` (audited,
year ended 31 December 2025) is the base year; `SCC-AFS-E-0326.pdf` (REVIEWED, three
months to 31 March 2026, auditor's report dated 11 May 2026) is the latest disclosed
period and the balance sheet the bridge stands on; `SCC-AFS-E-1224.pdf`,
`SCC-AFS-E-1223.pdf`, `SCC-AFS-E-1222.pdf` and the FY2021 comparatives carry the history.

**NOTHING HAS BEEN DISCLOSED SINCE.** The half to 30 June 2026 is not out at the review
date. No period this study could have read is unread, and no figure below rests on an
estimate of a period the company has already published.

## 2. BASE YEAR

Unchanged. FY2025 as filed: revenue and cost of sales foot to the audited statement of
profit or loss, and the gross margin of **38.01 per cent** is the FILED figure rather
than a solved one. The three filed margins run 6.62% (FY2023), 24.66% (FY2024) and
38.01% (FY2025) — the recovery is the company's own record, not this desk's ramp.

**WHAT IS ANNUALISED RATHER THAN FILED, STATED:** the FY2026 stub uses the reviewed
first quarter's profit of EGP 1,114.5mn against a full prior year of EGP 2,284.5mn. The
quarter is reviewed and filed; the annualisation is ours and is named here.

## 3. MACRO COHERENCE

**THIS HEADING IS THE ONE THIS EDITION CHANGES, AND IT CHANGES IT TOWARD COHERENCE.**
Until today the study carried a terminal risk-free rate built on a real-rate convention
of its own, 200 basis points away from the house path every other Egyptian study in this
book discounts on. Three studies in one market on two conventions is the incoherence
[R-MACRO-01] exists to close.

The inflation ladder, the currency path and the terminal growth rate all read
`engine/macro_paths/EG.json`. Terminal growth is 7.00 per cent nominal — the house
terminal inflation at a STATED real growth of zero — and the terminal risk-free is
10.50 per cent, the same 7.00 per cent inflation plus the house real convention of 3.50
per cent. **One economy, one inflation, in both the growth and the discount rate.** The
previous edition had 7 per cent inflation inside its growth and 7 per cent plus a
different real rate inside its discount rate, which is coherent only by accident.

## 4. DISCOUNT RATE

Explicit weighted cost of capital **28.96 per cent**; terminal **17.38 per cent**. The
explicit rate is built on a cost of equity of 29.01 per cent at a beta of 1.00, and the
debt weight is 0.52 per cent — this company is effectively unlevered, so the weighted
rate IS the cost of equity to within half a point, and there is no leverage assumption
carrying the answer.

**THE CASH IS CHARGED FOR ONCE.** Net cash of EGP 6,555.1mn — EGP 25.13 a share, **20.5
per cent of the answer** — is added at face in the bridge and is NOT inside the
discounted flows. The weights are struck on market-value equity against gross debt, not
net, so the operating rate is not lowered by holding a deposit and the deposit then
counted again at par.

**THE COST OF EQUITY REPRODUCES FROM ITS OWN INPUTS** under a construction the record
names, which it did not before this edition: the country premium is charged once and
flat rather than multiplied by beta. On this name that is worth nothing at all — the
beta is exactly 1.00 — and it is recorded because a construction that happens to be
neutral here is not neutral on the next company.

## 5. TERMINAL

Terminal value is **68.2 per cent** of enterprise value, which is high and is disclosed
rather than buried. Two things hold it up and both are measured rather than assumed.

**THE LIFE IS THE DISCLOSED SCALAR OF THE DOMINANT ASSET CLASS, 20 years**, not an
average of five classes' lives. Terminal maintenance is EGP 1,241.2mn — replacement
capital over that life — which is 26.8 per cent of the last explicit year's profit.

**GROWTH AND THE DISCOUNT RATE CARRY THE SAME INFLATION.** Terminal growth of 7.00 per
cent nominal at zero real sits inside a terminal rate of 17.38 per cent built on the
same 7.00 per cent. The previous edition held 5 per cent growth against a 12.5 per cent
risk-free built on that same 7 per cent inflation — a perpetual REAL DECLINE of about
two points a year that nothing in the study disclosed and nothing supports. Real decline
in perpetuity stays permitted and must be written down as the real number it is; this
study assumes none.

**THE TERMINAL SITS ABOVE ITS OWN FLOOR:** terminal free cash flow of EGP 3,677.1mn
against a NOPAT-perpetuity floor of EGP 26,622.3mn, and the ordering terminal rate <
explicit rate holds (17.38% < 28.96%).

## 6. BALANCE SHEET

The bridge stands on the **reviewed balance sheet of 31 March 2026** — cash EGP
5,802.0mn, lease liabilities EGP 152.7mn — and not on 31 December 2025. Net cash of EGP
6,555.1mn is that sheet's own arithmetic, and at 25.0 per cent of market capitalisation
it is the largest single line in the disagreement with the price after the terminal.

## 7. CLAIMS AGAINST THE RECORD

Every superlative in the document was re-checked against the filings for this edition
and none of them moved, because none of them touches the rate that did.

**UTILISATION IS THE ONE TO WATCH ON THE HIGH SIDE.** The filed record runs 53.2%,
62.7%, 71.0%; the forecast runs 71.7%, 73.5%, 75.3%, 77.2%, 79.1%. The forecast opens
essentially AT the last filed year and climbs about 1.8 points a year. That is an
optimistic path if the industry's quota lift reverses, and it is the assumption most
capable of making this study the one that is wrong. It is disclosed here rather than
defended.

**THE MARGIN IS NOT EXTRAPOLATED.** The forecast margins (38.6% rising to 39.8%) sit
just above the FILED 38.01 per cent of FY2025 and well inside what this company has
printed — the study does not assume a margin it has never earned.

## 8. MULTIPLE CROSS-CHECK

| | at the fair value | at the traded price |
|---|---:|---:|
| Enterprise value / FY2025 EBITDA | **7.40x** | 5.72x |
| Enterprise value / FY2026E EBITDA | **6.27x** | 4.85x |
| Price / FY2025 earnings | **14.00x** | 11.47x |
| Price / FY2026E earnings | **8.52x** | 6.98x |

**WHAT A BUYER AT THE FAIR VALUE IS PAYING.** 7.40x trailing EBITDA for a cement
producer with a fifth of its market capitalisation in net cash, on a margin the company
filed last year rather than one this desk forecast. Ex the cash, the enterprise is on
about 6.0x. That is not a demanding multiple for the asset, and the cross-check does not
contradict the cash-flow lens.

**THE HONEST WEAKNESS OF THIS HEADING** is that the multiples are struck against a
justified enterprise-value multiple of 4.2x carried elsewhere in the study, which is
BELOW both figures above. The relative lens reads EGP 62.11 against the cash-flow lens's
122.67, and that spread is published as an ENVELOPE rather than averaged. A reader who
believes the multiple lens over the cash-flow lens reaches a number below the market
price, and this study does not hide that.

---

## VERDICT

**No error found in the company's favour, and the lever that moved this edition moved
AWAY from the price rather than toward it.** The gap widened from +11.1 per cent to
+22.1 per cent because a rate this study should never have owned came off a house file,
and the correction would have been taken in either direction.

**WHAT WOULD MAKE THIS STUDY THE OPTIMISTIC ONE:** the utilisation path in heading 7. It
opens at the last filed year and climbs, and the Egyptian Competition Authority's
permanent lift of the output quotas in July 2025 is what licenses that climb. If the
quotas return, the path is wrong from year one and the terminal — 68.2 per cent of the
answer — is wrong with it.
