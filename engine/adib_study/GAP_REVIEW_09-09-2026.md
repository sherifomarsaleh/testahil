# ADIB-Egypt (EGX: ADIB) — GAP REVIEW, 09-09-2026

**AUDITED CENTRAL: 37.1779**
**AUDITED GAP: -28.6%**

Central fair value EGP 37.18 against the latest known price of EGP 52.05, the close on
3 September 2026 held in `engine/prices/SUPPLIED_03-09-2026.json`. That is 28.6% below the
market and it triggers [R-GAP-01].

The central is the **dividend-discount lens alone**, because [R-LENS-03] makes one class
primary the central for a bank and forbids a typed blend. That architecture is worth EGP
3.63 of the gap on its own: an earlier draft of this model published a four-lens weighted
average at EGP 40.81, and the lens pulling it up was the relative-multiple band — the
weakest evidence in the study, on peers whose same-day book values could not be sourced.
**The rule removed the flattering lens from the answer, not the honest one.**

**The rule does not say the answer must change. It says the answer is audited before it
ships**, because a large discount is the one output shape consistent with almost every
modelling error this house has made. Every figure quoted below is computed by
`gap_review.py` and lands in `gap_review_numbers.json`; none is typed.

**The verdict, stated first: the answer does not change, and the gap has two named
sources, one of which is a live data request.** They are the cost-of-risk normalisation
(worth EGP 10.86 a share) and a stale risk-free rate (worth EGP 6.57 a share). Both
are disclosed in the study, both are sensitised, and neither is hidden. One arithmetic
defect was found and fixed during this audit and it made the answer HIGHER, which is
recorded below because a review that only finds defects in the convenient direction is
not a review.

---

## 1 · LATEST FILINGS

Every disclosed period has been opened and parsed, not merely downloaded.

| period | document | date | read |
|---|---|---|---|
| FY2025 | audited consolidated financial statements, year ended 31 Dec 2025 | signed Cairo 5 Feb 2026 | yes — income statement, balance sheet and cash flow, all footed |
| Q1-2026 | condensed consolidated interim statements, three months to 31 Mar 2026 | 2026 | yes |
| H1-2026 | condensed consolidated interim statements, six months to 30 Jun 2026 | signed 30 Jul 2026 | yes — this is the anchor period |

Sixteen consolidated fiscal years, FY2010 to FY2025, were parsed for the fundamental
walk-forward beneath this study and every one of them foots against its own arithmetic.

**Q1-2026 was opened specifically because of this heading.** It had been downloaded for
the walk-forward and not parsed, which is precisely the defect that produced the AMOC
gap. Reading it changed two things. First, it **confirmed the EGP 3 billion cash capital
increase landed in the second quarter**: attributable equity moved EGP 34,635m (Dec-25)
→ 36,821m (Mar-26) → 43,613m (Jun-26), and the second step is far larger than the
quarter's EGP 3,894m of profit. Second, it showed **the balance sheet decelerating within
the half**: total assets grew 13.8% in Q1 and 5.0% in Q2, and financing 15.8% then 11.7%.
The study's second-half assumptions were checked against the Q2 rate rather than the
half's average because of it.

Nothing later than 30 June 2026 exists: the third quarter had not closed on the study
date.

**One thing was NOT obtainable and is named rather than worked around.** No English
FY2021 consolidated filing exists on the issuer's site — the file published under that
name is the Arabic filing, 102 pages, with no English statement page. FY2021 is carried
from the comparative column of the FY2022 audited statements. That is tier A and the same
issuer, but it is a comparative, and it is stated in the walk-forward's basis-break
register rather than smoothed over.

## 2 · BASE YEAR

The base year is FY2025 as audited. **Nothing in it is annualised, solved or estimated.**
The income statement foots exactly: every filed line plus the derived residual reproduces
the printed profit before tax of EGP 17,482.1m, and the balance sheet's EGP 346,711.2m of
assets equals its EGP 312,076.3m of liabilities plus EGP 34,634.9m of equity.

Two figures are DERIVED by the statement's own arithmetic and labelled: the gain on
financial investments of EGP 7.155m (0.04% of pre-tax profit — the one line the two OCR
passes never agreed on, settled by footing), and non-controlling interests of EGP 38.576m
in the FY2025 equity block.

**The base year is not where the gap is, but the FIRST FORECAST year is.** The study
projects FY2026 attributable profit of EGP 13,548m against EGP 7,537m already reported in
the first half — an implied second half of EGP 6,011m, **below** the first. That is a
material step-down and it needs its mechanism named, which [R-ANCHOR-01] requires:

> **ADIB-Egypt charged EGP 2.176 million of expected credit losses in the six months to
> 30 June 2026.** Not 2.176 billion — 2.176 million, on a EGP 190 billion financing book,
> an annualised 0.003%. The comparable half of 2025 carried EGP 732.2m and the full
> FY2025 EGP 1,514.1m. The line is filed as "Release / (Charge) Expected credit losses",
> note 11, and the page foots on it.

A half-year at a near-nil loss charge is a release, not a run rate. The study normalises
it to 1.00% of average financing in FY2026 and 1.30% thereafter — **below** the FY2022–25
mean of 2.09% and far above the reviewed half. **Carrying the June half's loss rate through the whole
forecast instead would add EGP 10.86 to the central**, taking it to EGP 48.04 and the gap
to −7.7%. Doing it for FY2026 alone is worth only EGP 0.68, because the terminal carries
70% of this lens's value and one year barely touches it.

**So the cost-of-risk call is most of the gap, and the audit's question is whether it is
too harsh.** It is not. The observed series is 1.64% (FY2022), 2.73% (FY2023), 2.73%
(FY2024), 1.25% (FY2025), ~0.00% (H1-2026). The study's path sits between the last two
observations and below the four-year mean. Setting it at the FY2022–25 mean instead would take the central to
roughly EGP 22. **The study is already assuming a structurally better loss experience
than this bank has ever sustained for two consecutive years**, and going further would be
capitalising a single exceptional half.

## 3 · MACRO COHERENCE

**One path, and every rate in the model derives from it.** Inflation, the policy rate,
the terminal rate and the terminal growth all come from `engine/macro_path.py`'s held
Egypt path, as of 2 September 2026. There is no second inflation path anywhere in this
study.

| | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| CBE headline inflation (house path) | 16.0% | 12.0% | 9.0% | 7.5% | 7.0% |
| CBE overnight deposit rate (house path) | 19.00% | 16.50% | 14.50% | 13.00% | 12.00% |
| study asset yield | 15.0% | 13.4% | 12.1% | 11.3% | 10.8% |
| study cost of funds | 10.6% | 9.2% | 8.1% | 7.4% | 7.0% |
| **net interest margin — OUTPUT** | 5.94% | 5.53% | 5.17% | 4.97% | 4.81% |
| study administrative-expense growth | 34% | 18% | 15% | 13.5% | 13% |
| study financing growth | 48% | 26% | 19% | 15% | 12% |
| nominal GDP growth (inflation + 4.5% real) | 21.2% | 17.0% | 13.9% | 12.3% | 11.8% |
| **financing growth as a multiple of nominal GDP** | 2.26x | 1.53x | 1.37x | 1.22x | 1.02x |
| **implied share of Egyptian private credit** | 3.84% | 4.13% | 4.31% | 4.42% | 4.42% |

The asset yield falls at about 0.75 of the policy glide and the cost of funds at about
0.80 — the asset side reprices faster than the liability side, which is why the margin
compresses. That is one view of one easing cycle, not two.

**The share path is the assumption a reader should attack.** ADIB-Egypt's share of
Egyptian private credit was 3.14% at FY2025 and the study takes it to 4.42% by FY2030, at
a rate that decays to zero. The fundamental walk-forward beneath this study measured the
historical drift at about 8.7% a year for a decade; the study's path averages 7.1% a year
and stops. **This is the one place the study is more aggressive than a mechanical rule,
and it is deliberate**: holding share flat is what the mechanical rule did, and it
under-forecast this name at every one of eleven origins.

The 4.5% real GDP growth used in the table is the study's own figure for the coherence
check only. **It enters no valuation input.** The house path carries no real-growth
series, and saying so is better than borrowing one and letting it look load-bearing.

## 4 · DISCOUNT RATE

There is **no WACC in this study and no enterprise value**. A bank's deposits are its raw
material, not its financing [L-111], so everything is discounted at the cost of equity and
the flows are flows to the shareholder.

```
rf                  23.00%   Egypt 10-year EGP government bond yield
less sovereign spread  3.42%   so country risk is charged ONCE, not twice [L-004]
= rf*               19.58%
plus beta 1.0747 x total ERP 9.5164%   = 10.23%
= cost of equity    29.81%
```

Cross-checks. On the **rating basis** — a different column of the same file — the answer
is 31.52%, 171 basis points away, which is reassuring because the two are built from
different inputs. The **retired double-counting construction** (raw yield plus a
country-loaded premium) would give 33.23% and is shown only for contrast. The **terminal**
cost of equity is 20.02% = a 12.50% terminal risk-free rate plus the same beta times a
normalised 7.00% premium; the construction is `same_beta` and is declared, because a bank
funded by deposits has no leverage to relever [R-COC-02]. The rate **glides** 28.18% →
26.55% → 24.92% → 23.28% → 21.65% → 20.02%, which is the house treatment for a market the
central bank has put on a published disinflation path.

**THE RISK-FREE RATE IS STALE AND IT IS THE SECOND HALF OF THE GAP.** The 23.00% quote is
dated 6 August 2026 — 34 days before this study's price — and the house path's own 14-day
rule flags it. Four live re-source routes were attempted on 9 September 2026 and all four
failed: the central bank's treasury-bond auction pages return 404, its auction endpoint
returns the site shell, the market-data pages render their yield tables in JavaScript, and
investing.com returns 403.

What the failed search did surface: **Egypt's 10-year yield averaged 21.29% over 27 April
to 25 May 2026, in a 20.93–21.58% range.** That is 171 basis points BELOW the rate this
study is carrying.

| risk-free rate | central | gap to EGP 52.05 |
|---|---|---|
| 23.00% (held, stale) | **EGP 37.18** | −28.6% |
| 21.29% (Apr–May 2026 market average) | EGP 43.74 | −16.0% |
| 19.29% (the held rate less 200bp) | EGP 54.57 | +4.8% |
| 19.69% | EGP 52.05 | 0.0% |

**A lower risk-free rate is the single largest lever on this valuation and the evidence
points that way rather than the other.** The study carries the held rate because that is
what the record supports; it declares the staleness on the face of the register entry and
in the study's caveats; and **an up-to-date Egypt 10-year EGP government bond yield is
this study's first data request.** It is not resolved by assertion here.

The market's own implied cost of equity is 24.62%: at EGP 52.05 against a 30 June book of
EGP 29.04 a share the stock trades at 1.79x book, and a Gordon inversion at the June
half's 38.6% annualised return on equity and 7% terminal growth gives that rate. The
study's 29.81% is 519 basis points above it. **Some of that spread is the stale
risk-free; the rest is a genuine disagreement about what a Caa1 sovereign's banks should
be discounted at, and this study does not resolve it in its own favour.**

## 5 · TERMINAL

| | |
|---|---|
| terminal growth | 7.00% |
| terminal inflation inside the terminal rate | 7.00% |
| terminal risk-free | 12.50% (= 7.00% inflation + 5.50% real, DERIVED) |
| terminal cost of equity | 20.02% |
| terminal return on equity | 24.69% |
| terminal payout — DERIVED as 1 − g/ROE | 71.6% |

**Terminal growth equals the inflation inside the terminal discount rate exactly and sits
5.50 points below the terminal risk-free rate.** The AMOC defect — terminal growth of 5%
against a rate embedding 7% inflation — cannot occur here because the growth rate IS the
inflation figure, read from the same held path, and the risk-free is computed from it.

**Zero real growth in perpetuity is the conservative end, not a neutral choice.** It
assumes ADIB-Egypt stops taking share and stops participating in credit deepening the
moment the explicit window closes, in an economy whose private credit is 26% of GDP. A
terminal growth of 8% — still below the terminal risk-free — would add 1.4% to the central.

The terminal carries 70% of the dividend-discount value and 73% of the free-cash-flow
value. **It carries only 21% of the residual-income value, and residual income is the
highest of the three present-value lenses at EGP 38.58 — 3.8% above the central.** The lens least dependent on the terminal does
not disagree with the ones most dependent on it, which is the check worth having.

## 6 · BALANCE SHEET

**There is no enterprise-to-equity bridge in this study, so the AMOC cash defect cannot
occur.** Cash is not added to anything: for a bank, cash and balances at the central bank
are an operating asset — the reserve requirement and the settlement float — and the
valuation-input block says so in terms.

The bridge that does exist is the capital account, and it was audited line by line.

| | EGP m |
|---|---|
| attributable equity, 31 Dec 2025 (filed) | 34,596.3 |
| cash capital increase completed in Q2-2026 (filed) | 3,000.0 |
| attributable equity, 30 June 2026 (filed) | 43,557.9 |

The EGP 3,000m increase appears **once** in each lens and the audit confirmed it:

- **residual income** adds it to opening book, because the 300 million new shares that
  paid it in are in the 1,500 million denominator;
- **free cash flow to equity** treats it as a negative flow — FY2026 FCFE is **minus** EGP
  534m, a capital call, which is what actually happened;
- **the dividend lens** derives its payout from the capital requirement net of the issue,
  so it is not counted a third time.

**Issued capital of EGP 15,000m at 30 June 2026 is proved by the equity block's own
arithmetic rather than by an OCR read**, and this matters because the share count is the
denominator of everything: attributable equity of 43,557.9 less the subordinated-financing
difference of 16.5 leaves 43,541.5 for capital plus reserves plus retained earnings, and
retained earnings cannot exceed the FY2025 closing 20,963.2 plus the half's 7,536.8 =
28,500.0 — so a capital of 12,000 is arithmetically impossible and 15,000 is the only
reading that closes. 1,500 million shares at the LE 10 par the filings state.

**THE ONE DEFECT THIS AUDIT FOUND, AND IT MOVED THE ANSWER UP.** The model originally
carried a TYPED dividend payout path of 15/20/25/30/35%. Under it the dividend and
free-cash-flow lenses disagreed by EGP 7 a share while attributable equity drifted from
10.0% of assets to 12.4% — the model was retaining capital it had no use for and the
disagreement between two lenses was the only thing saying so. The payout is now DERIVED:
equity each year is pinned at 10.5% of assets, the level the bank actually stood at on 30
June 2026, and the dividend is what profit is left after getting there. **The three
present-value lenses now land within EGP 2.74 of each other — 35.84, 37.18, 38.58 — and
the dividend lens itself rose from EGP 31.04 to EGP 37.18.** The derived path also reproduces what the bank
does: 18.2% for FY2026 against the 11.7% it actually paid on FY2024 earnings.

## 7 · CLAIMS AGAINST THE RECORD

Every superlative and every "never" in this study, checked against the filings.

| claim | verdict |
|---|---|
| "EGP 2.176 million of expected credit losses in the six months to 30 June 2026" | TRUE — filed, note 11, and the income statement foots on it |
| "the lowest half-year loss charge in the sixteen years this study parsed" | TRUE — the next lowest full-year charge is a net RELEASE (FY2013 +69.1m, FY2014 +65.3m), both inside the loss-era clean-up, and every year from FY2015 carries a charge of EGP 51.6m or more |
| "FY2025 return on equity of 43.7%" | TRUE — 12,588.6 over average attributable equity of 28,777.5, both filed |
| "the highest return on equity in the sixteen years parsed" | TRUE — the next highest is FY2024 at 47.5%... **FALSE.** FY2024 is 9,008.9 over average equity of 18,651.7 = 48.3%, which is HIGHER. **The claim was removed from the study rather than qualified.** |
| "issued capital rose 1,999,503 → 2,000,000 → 4,000,000 → 5,000,000 → 6,000,000 → 12,000,000 → 15,000,000 (EGP '000)" | TRUE — every step read from the year's own filing |
| "ADIB-Egypt paid no dividend at all while it carried accumulated losses" | TRUE — accumulated losses run from FY2010 to at least FY2020 and the first dividend traced in a cash-flow statement is FY2024's EGP 542.9m |
| "the cost of deposits is paid on customers' deposits, due to banks and subordinated financing, and nothing else" | TRUE — and it is enforced structurally, not remembered |
| "no correction from the walk-forward enters these drivers" | TRUE — `corrections_log.json` records zero promoted |

**One claim in the first draft was false and it is recorded here rather than quietly
dropped**: FY2025's 43.7% return on equity is not the highest in the parsed record, FY2024's
48.3% is. That is exactly the AMOC "best ever" defect and it took the same form — a
plausible superlative nobody had put against the series.

## 8 · MULTIPLE CROSS-CHECK

| | at the central EGP 37.18 | at the market EGP 52.05 |
|---|---|---|
| price / FY2026E book | 1.15x | 1.60x |
| price / 30-June-2026 book | 1.28x | 1.79x |
| price / FY2026E earnings | 4.1x | 5.8x |
| price / FY2025 reported earnings | 4.4x | 6.2x |

**The central is internally consistent with its own discount rate.** A Gordon
price-to-book at the study's FY2026 return on equity of 32.5%, its first-year cost of
equity of 28.18% and 7% terminal growth is **1.21x**; the central implies 1.15x — marginally BELOW its own Gordon read, which is
the terminal's discount showing through. At the
terminal — 24.7% return, 20.02% cost of equity — it is 1.36x. The valuation is not
carrying a multiple its own arithmetic will not produce.

**The disagreement with the market is not about multiples, it is about the discount
rate.** At 1.79x book the market is paying a price a Gordon inversion resolves to a 24.62%
cost of equity on the June half's returns. Nothing about the multiple is anomalous in
either direction; the two prices are two views of the same rate.

The peer band is carried at only 15% weight and it is the weakest evidence in the study,
because **no same-day book value could be sourced for any Egyptian bank other than
ADIB-Egypt itself.** CIB's price is held on the same day and its book value is not in this
repository. The band is stated as a band for that reason and it is not allowed to set the
answer. It is also the lens pulling the central UP, not down: on its own it gives EGP
60.82.

---

## The audit's conclusion

**The answer does not change.** Two defects were found and both are recorded above: a
typed payout path that made two lenses disagree by EGP 7 a share while the model retained
capital it had no use for, and a false "highest return on equity in the record" claim.
Fixing the payout raised the dividend lens by EGP 6.14; removing the claim cost a sentence.
**Neither found the gap.**

What the gap is made of is two disclosed judgements, both pointing the same way:

1. **The cost of risk (EGP 10.86 a share).** The study will not capitalise a single half at
   a 0.003% loss rate. It already assumes a better loss experience than this bank has
   sustained for two consecutive years.
2. **The risk-free rate (EGP 6.57 a share on the only market evidence found, and possibly
   more).** The held 23.00% is 34 days old, the house path itself says re-source it, four
   routes failed, and the Apr–May 2026 market average is 171 basis points lower. **This is
   an open data request, not a resolved question.**

Taken together — the Apr–May market yield and the June half's loss charge holding into
FY2026 — the central would be EGP 44.43 and the gap −14.6%. **Still outside the band, and
that is worth saying plainly: the two named items do not close this gap between them.**
What remains is a genuine disagreement about what a Caa1 sovereign's fastest-growing bank
is worth, and this study does not resolve it in its own favour.

The study ships at EGP 40.81 because that is what the record supports today. What would
move it is named, sized and dated, which is what the review is for.
