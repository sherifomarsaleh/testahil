# ARCC — valuation gap review, 3 September 2026

**Trigger.** [R-GAP-01], as amended 03-Sep-2026. Central **EGP 53.21** against a spot of
**EGP 77.00** — the close on the Egyptian Exchange on 3 September 2026, supplied by the
principal and committed at `engine/prices/SUPPLIED_03-09-2026.json`. The central sits
**−30.9%** below the price, past the ten per cent trigger, so this review runs before the
files are staged.

**Why this is the first ARCC gap review.** At its 6 August strike the study stood at
EGP 53.46 against EGP 59.00 — **−9.4%**, inside the band, and no review was owed. The price
has since risen to EGP 77.00, **+30.5% in four weeks**, and the gap opened to −30.9%
without a single driver moving. That is precisely the case [R-GAP-01 AMENDED] was written
for on 3 September: ARCC was one of the three studies that were *inside* the band when
struck and breach it against the day's price.

**The conclusion of this review, stated first.** The central does not move — and the reason
is unusually clear on this name. The study is **not** forecasting a cautious business. It
forecasts an EBITDA margin of 39.03% in FY2026, rising to 40.4%, against the best year ARCC
has ever filed of **39.25%**. There is essentially no operating upside left in the
forecast. The disagreement with the market is therefore **not about the business at all**:
solved on this study's own cash flows, the traded price implies a flat cost of capital of
**14.79%** — against an Egyptian sovereign yield of **22.95%**. The market is discounting
this company's cash flows at a rate **816 basis points below the yield on Egyptian
government debt**. That is the whole of the gap, and it is not a defect in this model.

---

## 1. LATEST FILINGS

Every disclosed period is read. The most recent is the **reviewed condensed consolidated
interim financial statements for the six months ended 30 June 2026**, taken from the
company's own investor-relations channel and registered in this study's sweep
(`sweep_register.json`). The audited annual accounts for FY2023, FY2024 and FY2025 are read
from the filings themselves, and the FY2025 audited outturn is the base year.

ARCC reports on a calendar financial year, so the half to 30 June 2026 is the latest
disclosure and the nine months to 30 September 2026 had not been filed on 3 September 2026.
**No unread filing sits behind this gap.**

The Q4-2025 exit price of EGP 3,118 per tonne is disclosed and is used as the anchor for
the FY2026 realised price, rather than the full-year average — the near-term reviewed
actual outranking the stale full-year rate.

## 2. BASE YEAR

The base year is **FY2025, audited**, and it foots to the filed accounts: revenue
EGP 12,447.3mn, EBITDA EGP 4,885.6mn, an EBITDA margin of **39.25%**, EPS EGP 9.49. Nothing
is annualised, scaled or solved out of another line.

The forecast is built bottom-up from the company's own tonnes and prices: FY2026E revenue
EGP 13,349.3mn on volume and a realised price anchored on the disclosed Q4-2025 exit rate,
with each direct cost line on its own driver and margin as the residual.

**The point that matters for this gap, and it runs the other way.** FY2026E EBITDA margin
comes out at **39.03%** — within a fifth of a point of the best year this company has ever
filed — and rises to 40.4% by FY2030. The filed record is FY2023 22.00%, FY2024 23.15%,
FY2025 39.25%. So the base year is the peak of a very short and very steep series, and the
forecast holds that peak and improves on it for five years. **This is not a conservative
forecast.** It is stated here rather than buried, because a review looking for what pushed
the value down has to record where the value was pushed up.

## 3. MACRO COHERENCE

One path, and the growth rates sit on it. The study's `macro_record` carries every growth
line as a **(real, inflation-path)** pair rather than a typed nominal — the FY2026 local
cement price at 8.0% nominal is recorded with a real growth of **−6.90%** against the house
path, and the record says so rather than leaving it to be inferred. The FY2027–FY2030 price
path, the cost escalators and the currency path all resolve to the same house Egyptian
inflation path, `path_as_of` 2 September 2026.

Costs are not escalated at domestic inflation while prices are held still: that is [L-048],
and the study's own price lines carry negative real growth explicitly, so the direction of
the incoherence [L-048] describes is not present here.

The euro-denominated debt leg is carried at **local-equivalent cost**, not at its euro
coupon, so the currency assumption inside the cost of debt is the same one as everywhere
else.

## 4. DISCOUNT RATE

Operations are discounted on a **cost-of-capital schedule**, not a single crisis-level
rate: forward rates of 27.60% / 24.09% / 21.29% / 19.60% / 18.34%, gliding to a terminal
built from the house macro path, with the terminal brought home on the same factor as the
last explicit year. The glide fractions are the policy-rate path's own cumulative progress
rather than a second free parameter.

Country risk enters **once**: the observed sovereign yield of 22.95% is normalised by
Egypt's own default spread of 3.40% to a risk-free of 19.55%, and the country premium is
added back through the ERP on the same (CDS) basis. Equity weights are market-value
(96.2% / 3.8%).

**Cash is charged for once.** ARCC is net cash on the bridge (cash EGP 1,970.5mn against
interest-bearing debt EGP 1,283.3mn), and the operating rate is built on **gross** debt
weights (`wd_gross = 3.78%`), not net. The net-cash position reaches the shareholder in the
bridge and nowhere else — there is no negative debt weight, no equity weight above one, and
no cash added twice. That is the AMOC defect, and it is not present here.

**The cost of debt, and why the 150bp bound does not bind.** ARCC's adopted Kd is 13.36%
against a trailing effective rate that computes near 5% for FY2025 — outside the ordinary
bound. This study is the **worked case for [R-COC-01 AMENDED]**: the book is 91.1%
euro-denominated at Euribor-linked rates, it re-based inside the year, and construction-
period borrowing costs are capitalised into assets under construction and never reach the
expensed charge. The mechanism is named from the closed list, the disclosure is carried
from the filings, and a contractual anchor reproduces the adopted rate facility by facility
(CIB 20.6%, NBE 5.49%, EBRD 6.84%, blended to local-equivalent). The bound is **re-pointed,
not switched off**, and `scripts/check_cost_of_capital.py` reproduces the rate from the
anchor's own lines.

The discounting convention is **declared** — a mid-period schedule with cumulative times
starting at 0.25 years — and the committed factors reproduce from the declaration.

## 5. TERMINAL

Terminal growth **7.00%**, terminal risk-free **12.50%**. The terminal risk-free is derived
as the terminal real rate plus the central bank's published inflation target, so the 7% in
terminal growth and the 7% inside the terminal discount rate are **the same number**.
Terminal growth is therefore inflation with **zero real growth** — not a real decline, and
not real growth nobody sourced.

Terminal value is **41.4% of enterprise value**, which is low for a five-year window and
means the answer rests mostly on the explicit forecast rather than on the perpetuity. The
terminal reconciliation carries the company's own historical reinvestment rates and implied
growth beside it (FY2023 reinvestment rate −23.7%, FY2024 +48.2%), so the terminal
reinvestment is anchored on the filed record rather than assumed.

## 6. BALANCE SHEET

The bridge stands on the **30 June 2026** balance sheet — the latest disclosed — and the
record names the register that establishes what "latest" means (`sweep_register.json`). The
valuation date *is* that balance-sheet date, so no roll-forward stands between the bridge
and a filing.

| line | EGP mn |
|---|---:|
| Enterprise value | 19,259.4 |
| plus cash and bank balances, 30 June 2026 | +1,970.5 |
| less interest-bearing debt, 30 June 2026 | −1,283.3 |
| less non-controlling interests | −0.2 |
| **equity value** | **19,946.4** |
| shares (mn) | 374.8674 |
| **per share** | **EGP 53.2091** |

It foots, and the equity divides to the stated per-share figure. The minority is trivial
(EGP 0.216mn) and is deducted from equity value, not from enterprise value. No dividend is
deducted, because none was declared after the bridge's balance-sheet date.

## 7. CLAIMS AGAINST THE RECORD

The study's superlatives are computed from the committed history rather than typed. Checked
in this pass:

- *"the best year this company has ever filed"* — FY2025 EBITDA margin 39.25%, against
  FY2024 23.15% and FY2023 22.00%. **True on the three audited years the study holds**, and
  the claim is scoped to those three years rather than to all time.
- The normalised-lens mid-cycle margin of 31.20% is stated as **the midpoint of the audited
  FY2024 outturn of 23.15% and the audited FY2025 peak of 39.25%**. That recomputes exactly:
  (23.15 + 39.25) / 2 = 31.20. **True.**
- The FY2026 price growth of 8.0% is stated as **0.8 points above a no-further-increase
  path**, because the disclosed Q4-2025 exit rate of EGP 3,118/t is 7.2% above the full-year
  average. That recomputes. **True.**

**The claim this review adds, because nothing in the study said it.** The forecast opens at
an EBITDA margin of 39.03% against a filed peak of 39.25% and rises to 40.4%. No sentence
in the study told a reader that the forecast sits at the top of the company's own filed
range. It does now — it is in the range basis (below), and it is the single most important
thing a reader should know about the shape of this forecast.

## 8. MULTIPLE CROSS-CHECK

The multiples the fair value implies, against the multiples the price implies:

| | at our central (53.21) | at the traded price (77.00) |
|---|---:|---:|
| enterprise value | EGP 19,259.4mn | EGP 28,177.6mn |
| EV / FY2026E EBITDA | **3.70x** | **5.41x** |
| EV / FY2025 EBITDA (audited) | **3.94x** | **5.77x** |
| price / FY2026E earnings | **5.19x** | **7.51x** |
| enterprise value per annual tonne | USD 76.6 | **USD 112.0** |

Two cross-checks that are **not** anchored on the price, and they disagree with each other,
which is worth publishing rather than averaging:

- **Replacement cost.** At USD 95 per annual tonne of capacity the lens reads **EGP 65.57**
  — above the central and below the price. The market at USD 112.0/t is paying below a
  replacement cost of USD 130/t, so on an asset basis the price is *not* obviously
  stretched. This is the strongest argument in the study against its own central, and it is
  published as a cross-check rather than blended away.
- **Relative multiple.** EGP 45.65, on a **house** multiple of 4.50x normalised EBITDA. The
  source line has been corrected in this edition: 4.50x is disclosed as weakly anchored
  against an Egyptian peer set of two names (Sinai Cement, Misr Beni Suef), neither of which
  publishes an EBITDA series this study could measure a multiple from. It was previously
  described as coming "from the company's own history and its regional peers", which claimed
  a provenance the number does not have.

  It is **not** read off the price, and that is now arithmetic rather than assertion: the
  record commits the adopted 4.50x beside the three numbers that reproduce the traded
  multiple of **7.72x** on the same normalised EBITDA. The two are far apart. (The
  companion re-strike found AMOC's equivalent lens *was* the traded multiple exactly; the
  gate that let that through now divides rather than reads prose, and ARCC passes it.)

**THE REVERSE READ, WHICH IS WHERE THIS GAP ACTUALLY LIVES.**

Solved on this study's own committed free cash flows, its own terminal, its own bridge and
its own declared discounting convention, holding every driver at its published value and
moving only the discount rate:

> At EGP 77.00 the price is paying for a flat **14.79%** cost of capital, against this
> study's schedule — equivalent to a flat **20.06%** — and an explicit-window rate of
> **27.60%** gliding to a terminal **18.34%**. The disagreement is **526 basis points on
> the price of time and risk, not on the business.**

Set that against the observed Egyptian sovereign yield of **22.95%**. The traded price
implies a discount rate **816bp below the rate at which the Egyptian government borrows**,
for an equity claim on a cyclical cement producer. Either the market expects Egyptian rates
to normalise much faster and further than the central bank's own published path, or it is
paying for operating performance beyond a forecast that already sits at the company's
best-ever filed margin.

The study's own record names **beta as its most consequential contested judgement, worth
9.9% of value**, and beta enters through exactly this rate — so the honest statement is
that the gap is concentrated in one input the study already flags and already publishes
both ways.

**This is why the number does not move.** Adjusting the central toward EGP 77.00 would mean
adopting a cost of capital solved backwards from the price, which is the reverse-engineered
rate [R-COC-01] prohibits outright. The diagnostic stays in `diagnostics.json`, no builder
reads it back, and `assert_reverse_dcf()` refuses any study whose builders do.

---

## Also examined, and changed, in this pass

**The central moved very slightly, and the direction is worth recording: EGP 53.4593 →
EGP 53.2091, −0.47%.** Nothing in the business changed. The higher market capitalisation
raised the market-value equity weight, which raised every forward cost of capital
(`forward_wacc[0]` 27.403% → 27.600%), which lowered the value. **A rising price
mechanically lowers this study's fair value**, because market-value weights are mandatory.
It is a small effect here and it is disclosed rather than left for a reader to trip over.

**The bear and the bull were rebuilt on filed evidence** — the item
`engine/build_depth_audit/lens_outstanding.json` promised at this study's next re-issue, and
this is that re-issue. The old corners moved the EBITDA margin by two points *and* the
discount rate by 150bp in opposite directions at each end. The discount rate is not this
company's to move: under [R-MACRO-01] it is derived from the house path, so the published
width was a choice of dial settings — while its own note called it "never a spread invented
around the answer", a cautious label attached to the construction it disclaims.

The range now moves one business driver across the span the audited accounts have printed:
the EBITDA margin, FY2023 **22.00%** to FY2025 **39.25%**, macro path held completely still.

Range: **EGP 11.29 – 53.76**, against a published 47.56 – 59.04.

**The asymmetry is the finding.** The forecast opens at 39.03%, so the bull corner
(EGP 53.76) is barely above the central and essentially the entire range is downside — and
if margin reverts to what this company earned two years ago, the value is EGP 11. The old
symmetric two-point band concealed that completely. Note also what it says about the price:
**EGP 77.00 sits above even the filed-peak-margin read.** The market is not paying for
ARCC's best year; it is paying for more than its best year, at a discount rate below the
sovereign's.

## What would change the answer

A cost of capital that normalises faster than the central bank's published path — the
market's own view, evidently — would raise the central materially, and beta is the input it
would come through. The nine months to 30 September 2026 holding the 39%-plus margin would
confirm the forecast rather than raise it, because the forecast already assumes it. A
reversion toward the FY2024 margin would take the value toward the bear corner quickly, and
the range now shows how quickly.

## Register

| item | state |
|---|---|
| central | EGP 53.2091 — **unchanged by this review** (−0.47% from the strike, from market-value weights alone) |
| spot | EGP 77.00, 3 September 2026, `engine/prices/SUPPLIED_03-09-2026.json` |
| gap | −30.9% (was −9.4% at the 6 August strike; the price moved, the model did not) |
| headings clean | 1, 2, 3, 4, 5, 6, 7, 8 |
| where the gap lives | the discount rate: the price implies a flat 14.79% against a sovereign yield of 22.95% |
| delivered numbers moved | central −0.47% (market-value weights); bear/bull rebuilt on filed evidence; relative-lens source line corrected |
| gates | `check_lens_design` now PASSES on ARCC — it comes off that ratchet |

---

*AUDITED CENTRAL: 53.2091* — the figure this review audits, stated so a job outside the study
can tell whether the review still describes the answer the study publishes. A review of a
number the study no longer carries is not a review of this study.
