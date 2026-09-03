# ARCC — valuation gap review, 3 September 2026
### Revision 5. This review REPLACES the revision-4 review of the same date, whose stated conclusion was wrong.

**Trigger.** [R-GAP-01], as amended 03-Sep-2026. Central **EGP 66.53** against a spot of
**EGP 77.00** — the close on the Egyptian Exchange on 3 September 2026, supplied by the
principal and committed at `engine/prices/SUPPLIED_03-09-2026.json`. The central sits
**−13.6%** below the price, past the ten per cent trigger, so this review runs before the
files are staged.

**What this revision replaces, and why the replacement was necessary.** The review written
earlier the same day audited a central of EGP 53.21 at a gap of −30.9% and concluded, in
these words, that *"the disagreement with the market is therefore not about the business at
all"* — that the whole gap sat in a cost of capital the market was applying 816 basis points
below the Egyptian sovereign yield. **That conclusion was wrong, and it was wrong because
the review examined the drivers, the base year, the macro path, the rate and the bridge, and
did not examine the terminal.** The terminal carried 41% of enterprise value and contained a
specification error worth EGP 13.32 a share. The earlier review's own reasoning was sound at
every step it took; it simply did not take the step that mattered. That is recorded here
rather than quietly superseded, because a review that reaches a confident wrong conclusion is
more dangerous than no review, and the reason it did so is instructive: **it looked for the
gap everywhere the arithmetic could be wrong, and the arithmetic was not wrong.**

---

## THE DEFECT THE EARLIER REVIEW MISSED

Revisions 1–4 built the terminal from the reinvestment identity `rr = g / ROIC` on
replacement-cost capital. Substituting the definitions collapses it to

```
TV = [ NOPAT (1+g)  −  g · IC ] / (W − g)
```

so the construction charged **g × IC = 7% × EGP 51,190.9mn = EGP 3,583.4mn every year, for
ever** — 62.2% of terminal profit. Read that charge as a capital-maintenance programme and
ask how long it takes to replace the asset base: `IC / (g·IC) = 1/g` = **14.3 years**.

**The implied asset life was the reciprocal of the inflation rate.** It was not a fact about
the plant. At 15% terminal inflation the same construction would have replaced this kiln
every 6.7 years.

The reinvestment identity is a statement about **real** growth. This model's terminal real
growth is **zero** — `macro_record.growth_at_horizon_end` is the house terminal inflation
exactly. So the charge bought no capacity at all: the model was paying for what inflation
supplies free. A second, independent error sat in the same six lines: the explicit window
builds `FCFF = NOPAT + D&A − capex − ΔWC`, and the terminal never added D&A back although
NOPAT is already net of it. **One model, two definitions of free cash flow, with the terminal
holding the larger share of the value.**

Nothing in that arithmetic was wrong, which is why it survived four revisions, a
cell-by-cell workbook recalculation with zero disagreements, a conforming beta attestation,
all eight depth-bar standards and a clean external-reader scrub. It is a **specification**
error.

**Three implied asset lives sat inside this one model and they disagreed by 2.8×:**

| | implied life | maintenance per annual tonne |
|---|---|---|
| the terminal's `1/g` | 14.3 years | USD 9.10 |
| **DISCLOSED — accounting-policies note** | **20.0 years** | **USD 6.50** |
| the explicit window's own capex (130.0 / 3.23) | 40.2 years | USD 3.23 |

The sourced figure sits **between** the model's own two conventions, which is the whole
argument for sourcing it. ARCC's FY2025 audited accounts disclose machinery and equipment at
20 years, other installations at 20 and buildings at 10–20; the replacement-cost base this
study builds is capacity × replacement cost per tonne, which is a greenfield cement plant,
which is those classes. The filing carries **no text layer** — `pdftotext` returns 47
characters across 47 pages — so it was read by OCR off the rendered pixels at 200dpi and the
route is recorded, cross-checked against the FY2024 filing carrying the identical table
(`useful_lives.json`).

Corrected on the disclosed life, holding every other driver exactly as published:
**EGP 53.21 → 66.53**, and the gap −30.9% → −13.6%.

**The explicit window and the terminal are still allowed to differ, and the reason is
economic rather than a fudge.** The explicit window's maintenance is ARCC's own most recent
full-year spend, and kiln 2 sits in assets under construction: a young plant genuinely spends
less than replacement depreciation for a while. The terminal is perpetuity, where every asset
must be replaced at current cost on its disclosed life. The step at the boundary is real and
is now stated in the study rather than left implicit.

---

## 1. LATEST FILINGS

Every disclosed period is read. The most recent is the **reviewed condensed consolidated
interim financial statements for the six months ended 30 June 2026**, from the company's own
investor-relations channel and registered in this study's sweep. The audited annuals for
FY2023, FY2024 and FY2025 are read from the filings themselves and FY2025 is the base year.
ARCC reports on a calendar year, so the half to 30 June 2026 is the latest disclosure and the
nine months to 30 September had not been filed on 3 September 2026. **No unread filing sits
behind this gap.**

New in this revision: the FY2025 filing's **accounting-policies note** is now read and
registered. It had been parsed for the statements and not for the policies, and the useful
lives it discloses are what the terminal turned on. **A filing is not "read" until the notes
that bear on the model are read** — which is the same lesson as the reviewed half-year that
[R-GAP-01] was adopted over, one level in.

## 2. BASE YEAR

**FY2025, audited**, and it foots to the filed accounts: revenue EGP 12,447.3mn, EBITDA
EGP 4,885.6mn, an EBITDA margin of 39.25%, EPS EGP 9.49. Nothing is annualised, scaled or
solved out of another line.

FY2026E EBITDA margin comes out at **39.03%** — within a fifth of a point of the best year
this company has ever filed — and rises to 40.4% by FY2030, against a filed record of 22.00%
(FY2023), 23.15% (FY2024), 39.25% (FY2025). **This is not a conservative forecast**, and it
is stated here rather than buried, because a review looking for what pushed the value down
must record where it was pushed up. [R-ANCHOR-01]'s record is printed for this study whether
or not it fires, and it does not fire: the forecast opens 0.56% below the filed peak, well
inside the 5% relative threshold.

Grossing FY2026 up from the half rests on the median of three measurable half-year shares
and lifts the year 9.8% above simply doubling. The share is not stable (44.2% / 45.5% /
52.7%) and that remains the single largest assumption in the study. On the worst of the three
shares FY2026 revenue is 11,540mn against the central 13,349mn.

## 3. MACRO COHERENCE

One path, and every growth rate sits on it. Growth lines are recorded as **(real, inflation
path)** pairs rather than typed nominals, so the FY2026 local cement price at 8.0% nominal
carries an explicit real growth of −6.90% against the house path. The FY2027–FY2030 price
path, the cost escalators and the currency path all resolve to the same house Egyptian
inflation path, `path_as_of` 2 September 2026. The euro debt leg is carried at
local-equivalent cost, so the currency assumption inside the cost of debt is the same one as
everywhere else. Costs are not escalated at domestic inflation while prices are held still —
[L-048] — and the price lines carry negative real growth explicitly.

**This heading is where the terminal defect should have been caught and was not.** The
inflation path was coherent in every place a study normally carries one, and the failure was
that the inflation rate had also become an **asset life**, through an identity nobody had
substituted. [R-MACRO-01] holds every inflation-class input a study registers; `1/g` was not
an input, it was a consequence.

## 4. DISCOUNT RATE

Built through the shared cost-of-capital builder on the house macro path: explicit-window
WACC 27.60% gliding to a terminal 18.34%, market-value weights, country risk counted once,
the euro leg at local-equivalent cost, and the terminal risk-free **derived** from terminal
inflation plus the real-rate convention rather than quoted. The cash is charged for exactly
once — operations at the blended rate, net cash added at face in the bridge, and the bridge
record says which.

The earlier review solved the price back through the model and found it implied a flat cost
of capital of 14.79% against an Egyptian sovereign yield of 22.95%, and concluded that the
market was discounting Egyptian cement 816bp below its own government. **That reverse read
was arithmetically correct and its interpretation was wrong**, because it was solved on a
model whose terminal was mis-specified. Re-solved on the corrected model the price implies a
flat **17.77%** against this study's own schedule equivalent of **19.80%** — a disagreement
of 203 basis points on the price of time, not 816 below the sovereign. **A reverse read is
only as good as the model it is read backwards through**, and that is a general caution about
the instrument, not a criticism of this one use of it. The study's own record names beta as
its most consequential contested judgement, worth 12.0% of value, and beta enters through
exactly this rate — so the residual disagreement sits in the one place the study already
calls contested.

## 5. TERMINAL

The heading the earlier review passed over, and where the whole correction sits. It is set
out in full above. In summary: the terminal is now built by the shared builder
[R-TERM-01], which takes **real** growth and derives the nominal rate from the house
inflation path, so a nominal rate cannot arrive as a growth assumption at all. The charge is
maintenance at the disclosed 20-year life, plus the capital that stated real growth needs
(zero, here, so zero), plus inflation on working capital, less the book depreciation already
inside NOPAT — the same free-cash-flow definition the explicit window uses.

Terminal growth is 7% nominal at **zero real**, coherent with the 7% terminal inflation
inside the terminal discount rate. That is not a perpetual real decline and it is not
disguised: it is written down as the real number it is.

**The sign condition was re-derived, because it had been derived for the retired charge.**
Under `g × IC` the hurdle was `N/IC` against `W/(1+W)`; with the charge gone the wedge goes
with it and the test is the ordinary marginal one, `N/IC` against `W`. The answer does not
change and that is worth saying: **10.52% against 18.34%.** Building cement capacity at
USD 130 per annual tonne does not clear this company's cost of capital, so real growth
destroys value and the model takes none. **That is a finding about Egyptian cement economics,
not a conservatism** — and it is why charging ARCC for growth was wrong twice over: it is not
growing in real terms, and on these numbers it should not.

The terminal is now **53.5%** of enterprise value, up from 41.4%, because the numerator rose
while the explicit window did not. That is a higher share than this desk likes and it is
disclosed rather than managed: a five-year window on a business whose growth is at terminal
by year five will always carry most of its value in the terminal, and shortening the window
would not change the economics, only where they are booked.

## 6. BALANCE SHEET

The bridge stands on the **disclosed 30 June 2026 balance sheet**, not a roll-forward: cash
EGP 1,970.5mn less interest-bearing debt EGP 1,283.3mn = net cash EGP 687.2mn, less
minorities of EGP 0.216mn. The roll-forward revision 3 had to use gave EGP 1,940.1mn —
EGP 3.34 a share too generous, because a roll-forward cannot see a working-capital build or
six months of capital spending. **The disclosed sheet COSTS this valuation 3.34 a share**,
and it is the half of the rebuild that moves the answer down.

## 7. CLAIMS AGAINST THE RECORD

Every "best ever" and "never" is recomputed against the filings rather than typed:

- FY2026E EBITDA margin 39.03% against a filed best of 39.25% — **below it**, by 0.22
  points, computed not asserted.
- Profit compounded 127% a year over FY2023–FY2025. At that rate against 18% nominal
  economic growth this company equals the whole Egyptian economy in 11.1 years, which is why
  terminal growth is held at inflation.
- Book return on capital 43.9% / 44.3% / 60.6% (FY2023–FY2025) — the figures that made the
  retired terminal's 11.26% look wrong, and the reason it was interrogated. Note that the
  correction does **not** adopt those returns: it removes a charge that was never justified,
  and leaves the marginal return on **new** capacity at 10.52%, which is the number that
  governs growth.
- Every figure in the delivered prose is reconciled against the model by this study's own
  prose instrument; the external-reader scrub is clean on 158,437 characters.

## 8. MULTIPLE CROSS-CHECK

| | at the fair value | at the price 77.00 | reference |
|---|---|---|---|
| EV / FY2026E EBITDA | **4.66×** | 5.41× | |
| Price / FY2026E NOPAT | **6.66×** | 7.71× | |
| EV per annual tonne | **USD 96.4** | USD 112.0 | replacement cost USD 130 |

The fair value puts the enterprise at 4.66× forward EBITDA and USD 96 per annual tonne
against a replacement cost of USD 130 — a 26% discount to the cost of building the plant, in
a market carrying substantial idle capacity. The price puts it at USD 112, a 14% discount.
**Neither is absurd, and that is the honest reading of a −13.6% gap**: the market is paying
closer to replacement cost than this model does, on a view of Egyptian cement demand that is
a legitimate disagreement rather than a defect. The multiples are ordinary for the asset and
the geography, which is the change from the earlier review, where 3.1× forward EBITDA and
USD 78 per tonne were not.

---

## THE VERDICT

**The central moves from EGP 53.21 to EGP 66.53 and the gap from −30.9% to −13.6%.** The
correction is justified by the identity and by ARCC's own disclosed useful lives, and it
would be the same size and in the same direction if this company traded at EGP 40 — the
price is what prompted the question, not what set the answer. [R-GAP-01] is explicit that a
fair value adjusted to meet a quote is the reverse-engineered rate this method prohibits
outright, arriving through the front door instead of the side one.

**The residual −13.6% is not claimed to be a market error.** It is one legitimate
disagreement, priced: the market pays USD 112 per annual tonne and this model pays USD 96,
against a replacement cost of USD 130. Under [R-GAP-02] the study remains **HELD** past the
ten per cent publication limit and no market dissent is filed, because on this evidence none
is warranted — a reverse read landing on a believable number is evidence *against* a dissent,
and a 203-basis-point disagreement about the price of time is believable.

*AUDITED CENTRAL: 66.5300* — the figure this review audits, stated so a job outside the study
can tell whether the review still audits the answer the study publishes.

*AUDITED GAP: -13.6%* — the disagreement this review interrogates, stated so a job outside
the study can tell whether the eight headings were asked at the size the study now carries.

**What would overturn this review.** A disclosed asset-class breakdown of property, plant and
equipment by cost showing the replacement-cost base is dominated by a class with a materially
different life; a later filing revising the disclosed lives, which management reviews at every
reporting date; or evidence that ARCC is contractually obliged to spend at the retired rate —
a concession condition, a licence commitment or a take-or-pay — in which case the
no-growth-capital argument fails for this name. None of the three is disclosed.
