# AMOC — valuation gap review, 3 September 2026

**Trigger.** [R-GAP-01], as amended 03-Sep-2026. Central **EGP 11.83** against a spot of
**EGP 13.50** — the close on the Egyptian Exchange on 3 September 2026, supplied by the
principal and committed at `engine/prices/SUPPLIED_03-09-2026.json`. The central sits
**−12.3%** below the price, past the ten per cent trigger, so this review runs before the
files are staged.

**This review found a defect and the central MOVED: EGP 9.91 → EGP 11.83, +19.4%.** The
first draft of this review, written an hour earlier, cleared seven of the eight headings
and reported the gap as a legitimate disagreement about margin persistence. It was wrong,
and what found the defect was the principal reading the forecast margin path — which this
review had looked at only through the base year and not through the five forecast years
beside it. The finding is at heading 2 and the correction is not a matter of judgement:
the study was carrying an unsourced real cost drift that contradicted its own registered
principle and ran against the measured direction in its own filings.

**What changed since the review of 1 September.** Nothing in the model. The price moved:
EGP 9.10 on 6 August, EGP 13.50 on 3 September, **+48.4% in four weeks**. The 1-September
review was struck against 9.10 and found six defects behind a −39% discount; correcting
them left the central at 9.91 and the gap at −8.9%. That gap has re-opened entirely on the
price, and re-opening it that way is the case [R-GAP-01 AMENDED] was written for: a study
audited against a month-old quote is audited against its own past.

**The conclusion of this review, stated first.** TWO defects, one of which moved the answer.
(i) The forecast margin declined every year — 9.494% to 8.764% — because the pound
conversion cost legs escalated at full domestic inflation while realised price grew only at
the currency differential, a real cost drift of +2.7 points a year that nothing sourced and
that contradicted the study's own registered principle. Corrected: EGP 9.91 → 11.83.
(ii) The relative-multiple lens was anchored on the traded price; it is withdrawn, and it
carried no weight so it moves nothing. A THIRD question is priced and deliberately NOT
adopted — the base anchor, worth +55% — and heading 2 says why.

After the correction, **the market is paying for a gross margin of 10.36% sustained for
ever, and this study forecasts 9.68%.** Both sit inside the range this company has filed
and below the 12.43% of its latest half, so the remaining disagreement is about
persistence, not arithmetic.

---

## 1. LATEST FILINGS

Every disclosed period is read. The most recent is the **reviewed condensed interim
financial statements for the six months ended 30 June 2026**, and they are read as
statements — revenue EGP 26,223.0mn, gross profit EGP 3,258.9mn, a gross margin of
**12.43%**, operating profit EGP 2,456.2mn, all carried in `study_numbers.json` under
`hist_is["6M Jun-2026"]` and all footed against the filing rather than solved out of the
profit line.

That is the defect the 1-September review found and closed. This edition re-checks it
rather than assuming it: the five filed periods now in the record are 6M Dec-2024,
3M Mar-2025, 6M Dec-2025, 3M Mar-2026 and 6M Jun-2026, each with its own revenue, gross
profit, margin and operating profit.

Nothing newer exists to read. AMOC moved its financial year from 30 June to 31 December,
so 30 June 2026 is a half-year end and the next disclosure is the nine months to
30 September 2026, which had not been filed on 3 September 2026. **No unread filing sits
behind this gap.**

## 2. BASE YEAR

The base year is a trailing twelve months built from filed periods, not an annualisation.
Base-year gross margin **9.653%**, revenue and cost lines footing to the filed halves and
quarters that compose them. Base-year EBITDA EGP 2,951.1mn is gross profit less operating
expenses plus depreciation, each component from the filings.

What is *not* filed and is labelled as such: nothing in the base year is solved out of the
profit line. The 1-September review found the previous edition solving H1 gross profit out
of the profit line while calling the period a press release; that construction is gone and
the gross profit above is the filed figure.

### THE DEFECT THIS HEADING MISSED ON ITS FIRST PASS, AND WHAT IT COST

The base year was clean. **The five forecast years beside it were not**, and a review that
checks the base year without checking the path leaving it has checked half the question.

As it stood, the forecast gross margin *declined every year*: 9.494% / 9.325% / 9.146% /
8.959% / 8.764%, against a base year of 9.653% and a filed first half of 12.428%. The
implied second half of calendar 2026 was **6.56%** — barely half what the company had just
filed for the first half, and below every period in the record except one.

The mechanism is arithmetic, not a view. Per tonne, realised price grows at the currency
differential (11.7% falling to 6.8%) while the pound-denominated conversion legs — salaries
and other conversion cost — escalate at the full Egyptian inflation ladder (14.5% falling
to 9.5%). That is a **real cost drift of +2.7 to +2.8 points a year, compounding for ever**.
It is the whole of the margin decline.

Three things are wrong with it and none is a matter of taste:

1. **It contradicts the study's own declared principle.** The `raw_pass = 1.0` input is
   registered with the words *"the gross SPREAD per tonne is held flat in real terms and
   the margin neither widens nor narrows."* That principle is applied to the feedstock leg
   and silently broken on the conversion leg two lines below it.
2. **It is unsourced.** No input registers a real cost drift, nothing disclosed supports
   one, and no sentence told a reader that the forecast margin decline was an escalator
   artefact rather than a finding. This is [L-048], and the digest already carries the ARCC
   precedent verbatim: *"the model's whole forecast margin decline was a mechanical
   artifact of the price path being set below a single blended cost-inflation index in
   every year, by construction."* The lesson was registered, correct, and re-violated here.
3. **The measured direction in the company's own filings is the opposite.** The standing
   rule permits a unit rate to drift only where a named mechanism has a *measured*
   like-for-like direction in the company's own period pair. Cost per unit of revenue
   across the five filed periods runs 93.146% → 94.947% → 93.855% → 89.810% → **87.572%**:
   it FELL 5.58 points while the model asserted it rises 2.7 points a year for ever.

**Corrected.** The study's own principle now applies to every cost leg. Margin path
9.68% / 9.70% / 9.72% / 9.73% / 9.74% — essentially flat, and still *below* the 12.43% the
company filed for the half to 30 June 2026 and below the 10.19% of the quarter before it.
Worth **+19.4%**, EGP 9.9142 → 11.8342. The as-published framing is priced beside it in the
sign test.

**This is not moving the number toward the price.** [R-GAP-01] prohibits that outright. The
correction removes an unsupported *decline*; it does not adopt the observed *improvement*,
which the same rule says to hold flat.

### THE SECOND LEVER, PRICED AND DELIBERATELY NOT PULLED

The standing rule also says a near-term reviewed actual outranks a stale full-year rate,
and the most recent reviewed period is the half to 30 June 2026 at **12.428%** against the
twelve-month base of 9.653% this study forecasts forward. The like-for-like test that rule
prescribes supports the alternative rather than the base: **Q1-2025 5.053% against Q1-2026
10.190% — the same quarter, doubled** — which no seasonal pattern produces, and Q2-2026
higher again at 13.925%. Every period *after* the shift is at the higher level and every
period *before* it at the lower one; the twelve-month base averages across the shift.

Anchoring there and holding it flat gives **EGP 18.35 a share, +35.9% against the price**.

**It is not adopted, and the reason is a rule rather than a preference.** [R-VCAL-01]'s
promotion guard takes levers one at a time and halts the moment the stack would cross zero
by more than the bootstrap half-width — the guard against stacking individually-justified
moves into an overshoot, which is the exact failure that called the method reassessment.
One correction has already moved this study from 26.6% below the price to 12.3% below it.
A second lands 35.9% above. That is a crossing in a single pass, so the lever is priced,
published as the study's most consequential contested judgement, and left for the next
edition to take on its own evidence rather than on this one's momentum.

## 3. MACRO COHERENCE

One economy, one path, all three legs derived from it. The study runs on a registered
Egyptian inflation ladder of 14.5 / 13.0 / 11.5 / 10.0 / 9.5 per cent for 2026–2030, and
**both** the currency path and the product-price path are DERIVED from that same ladder by
purchasing-power parity. There is no second view of the economy inside the model: costs do
not escalate at one inflation while prices are held at another, which is [L-048] and which
was measured on this company's own history at −0.570 log.

The recorded divergence, stated rather than hidden: this ladder **predates the house macro
path** [R-MACRO-01] and differs from it year by year. It is registered as an exemption in
the study's own `macro_record` with the reason — rebuilding the ladder moves every
operating number in the model and belongs in its own pass. The study is internally coherent
on one path; it is not yet on the *house* path. That is a scheduled item, not a defect
behind this gap, and conforming it would move the answer in an unknown direction rather
than a helpful one.

## 4. DISCOUNT RATE

Cash is charged for **exactly once**, and this is checked arithmetically rather than
asserted.

AMOC is net cash: net debt is **EGP −3,001.5mn**. On a net-debt-weighted rate that drives
the debt weight negative (`wd_exp = −0.2080`), the equity weight above one
(`we_exp = 1.2080`) and the operating rate *above* the cost of equity — the defect the
1-September review found, worth 374bp. It is gone. The committed record now carries
`wacc_exp = 0.2745428` and `ke_exp = 0.2745428`: **identical to seven decimal places**.
Operations are discounted at the pure cost of equity, and the cash is added once, in the
bridge, at face.

The construction is therefore the second of the two [R-BRIDGE-01] permits — value the
operations at the operating rate and add the cash — and the record says so. The first
(a blended rate with nothing added) is not also applied.

Cost of equity: risk-free 22.31% normalised by Egypt's own default spread to 18.91%, beta
0.9080 regressed against EGX30 (`raw_indices/EG/EGX30.csv`, conforming), ERP on the CDS
basis. Cost of debt is immaterial by construction — gross debt is **0.0966%** of the
capital structure, and a 500bp error in it moves the weighted rate by 0.38 basis points.
The study says that rather than presenting an immaterial input as a precise one.

## 5. TERMINAL

Terminal growth **7.00%**, and it is **inflation only, with zero real growth**. The
terminal nominal risk-free rate is not typed: it is derived as the terminal real rate
(5.5%) plus the central bank's published inflation target in force for the terminal
horizon — the same 7% that sits inside terminal growth. **One inflation number, appearing
in both places, by construction.**

That closes the defect the 1-September review found (5% growth against a terminal rate
embedding 7% inflation — a perpetual real decline of about two points a year, never stated
as one). Zero real growth remains the conservative end and is stated as such: it assumes
AMOC never again grows a tonne, on a plant serving a population growing 1.6% a year.

Terminal value is **54.4%** of enterprise value — a normal share for a five-year explicit
window, and below the level at which the terminal is doing all the work.

## 6. BALANCE SHEET

The bridge stands on the **30 June 2026** balance sheet, which is the latest disclosed, and
the register establishing what "latest" means is named in the record (`bridge_record.
latest_disclosed_source`, the investor-relations register under `engine/amoc_walkforward`).
The valuation date is that balance-sheet date, so no roll-forward stands between the bridge
and a filing.

The bridge, and it foots:

| line | EGP mn |
|---|---:|
| Enterprise value | 10,874.2 |
| less net debt — the company is NET CASH, so this ADDS | +3,001.5 |
| less provisions | −996.9 |
| less dividend payable | −258.3 |
| plus investments | +594.8 |
| less non-controlling interests | −411.1 |
| **equity value** | **12,804.2** |
| shares (mn) | 1,291.5 |
| **per share** | **EGP 9.9142** |

The minority is deducted from **equity** value and not from enterprise value, and the
dividend deducted is one declared *after* the bridge's balance-sheet date.

## 7. CLAIMS AGAINST THE RECORD

Every superlative in the study is recomputed against the filings rather than typed. The
one claim that carries weight here is the reverse read, and it is computed by solving:

> holding every other driver at the base case, the cash-flow lens reaches EGP 13.50 at a
> gross margin of **11.17%** sustained in every forecast year and in perpetuity, against a
> base year of **9.65%**.

Checked against the filed record: AMOC has filed **13.84%** for the full year to 30 June
2022 and **13.92%** in the quarter to 30 June 2026. The required 11.17% is therefore
**inside** the range this company has actually printed — comfortably inside it, and below
the most recent quarter.

This is the claim the 1-September review found typed rather than computed and **false**:
the previous edition put the required margin at 12.2% and called it "above the best single
quarter this company has ever filed" when the company had filed a higher one twice. The
number is now solved by the model and the comparison is made against the filed maxima held
as committed constants (`GM_FILED_MAX = 0.1384`, `GM_FILED_MAX_Q = 0.1392`). No superlative
in this edition is typed.

**What that means for the gap, said plainly.** The market is not asking for something this
company has never done. It is asking for 11.17% to persist, where the study forecasts the
base year's 9.65% to persist. Neither is absurd. The study's answer is the more cautious of
the two and it is a *choice about persistence*, which is why the honest output of this
review is an unchanged central and a clearly stated disagreement.

## 8. MULTIPLE CROSS-CHECK

The multiples the fair value implies, against the multiples the price implies, on the same
base-year EBITDA of EGP 2,951.1mn and the same attributable earnings of EGP 1,651.2mn:

| | at our central (9.91) | at the traded price (13.50) |
|---|---:|---:|
| enterprise value | EGP 10,874.2mn | EGP 14,433.7mn |
| EV / base-year EBITDA | **3.69x** | **4.89x** |
| price / earnings | **7.75x** | **10.56x** |

**THE ONE REAL DEFECT THIS REVIEW FOUND, AND THE RE-STRIKE IS WHAT EXPOSED IT.**

The study's relative-multiple lens was **anchored on the traded price**. Its "justified
multiple" was computed as `(market cap + net debt) / base-year EBITDA`, re-rated by zero —
the traded multiple exactly. The lens therefore valued the company at what it already
traded at, and its entire distance from the share price was the bridge. The study's own
code comment said so in as many words, while its committed lens record attested the
opposite: *"enterprise value to EBITDA from the company's own history and its regional
peers, never a multiple read off the current price."*

Moving the price is what made it visible: **the price rose 48.4% and the lens rose 51.3%**
(EGP 8.32 → EGP 12.59). A lens built on five years of own history cannot do that. A lens
built on today's price cannot do anything else.

Three things follow, all done in this edition:

1. **The lens is withdrawn as a valuation** and published as a diagnostic of what the
   market is paying. It carried no weight in the central — the central is the cash-flow
   lens alone under [R-LENS-03] — so **no delivered number moves**. What moves is the
   envelope of cross-checks and the honesty of the record.

2. **It is not rebuilt, and the reason is a measurement rather than a preference.** An
   own-history EV/EBITDA needs this company's net debt and share count at each past year
   end. AMOC's committed record carries PPE at 2021–2023 and *neither of those at any
   origin* — `engine/valuation_calibration/bridge_inputs.py` prints the census. That is
   precisely the gap [R-FCAL-01 AMENDED] was adopted to close, AMOC is on its outstanding
   list, and inventing a peer multiple nobody sourced would be the same offence in the
   other direction. Under SIGCM clause 8 the lens stops rather than guesses. It returns
   when AMOC's next walk-forward run commits the valuation-input block.

3. **The gate that passed it three times is now arithmetic.** `assert_lens_design()` read
   the `multiple_source` *prose*, found the reassuring words and passed. It now requires
   the adopted multiple and the three numbers that reproduce the traded one, and refuses
   when they agree to within half a per cent. AMOC's construction, exactly as it shipped,
   is case 10a in `scripts/check_lens_design_negative_control.py`; a genuine own-history
   multiple standing clear of the traded one is added as a clean case that must stay green.

**Read the two columns as a disagreement.** At 3.69x EV/EBITDA and 7.75x earnings this
study is not calling AMOC expensive on any absolute measure — it is saying the market's
4.89x and 10.56x pay for a margin that persists above the base year. That is the same
disagreement as heading 7, expressed in multiples.

---

## Also examined, and changed, in this pass

**The bear and the bull were rebuilt on filed evidence** — the item
`engine/build_depth_audit/lens_outstanding.json` promised at this study's next re-issue.
The old corners moved five things at once, three of them macro: the currency path, the cost
of capital at both anchors, and terminal growth. Under [R-MACRO-01] all three carry the
same Egyptian inflation, so the old bull corner needed inflation high and low at the same
time and the old bear corner needed the mirror image. The published width was this desk's
choice of dial settings.

The range now moves only what the audited filings have printed — gross margin from 5.05%
(the quarter to 31 March 2025, the worst in the record) to 13.84% (the full year to 30 June
2022, the best full year; the best *quarter* of 13.92% is deliberately not used, because a
forecast margin is sustained for five years and a quarter is not a year), and tonnage −4.5%
to +3.0% a year, the bear leg carrying the base year back to the five-year mean. The macro
path is held completely still.

Range: **EGP 1.08 – 22.77**, against a published 4.93 – 16.73. It is wider and it is
asymmetric, and both of those are properties of this company's filed record rather than of
this desk's preferences. The spot of 13.50 sits inside it.

## What would change the answer

A ninth-month filing showing the 12.43% half-year margin holding into the second half would
move the base year up and the central with it, and that is the single most likely source of
a materially higher fair value. Conforming the study to the house macro path [R-MACRO-01]
would move every operating number in an unknown direction. Neither is available today.

## Register

| item | state |
|---|---|
| central | EGP 11.8342 — **moved +19.4% by this review**, from EGP 9.9142 |
| spot | EGP 13.50, 3 September 2026, `engine/prices/SUPPLIED_03-09-2026.json` |
| gap | −12.3% (was −26.6% before the correction at heading 2) |
| headings clean | 1, 3, 4, 5, 6, 7 |
| headings with findings | 2 — an unsourced real cost drift produced the whole forecast margin decline (corrected, +19.4%); 8 — the relative lens was anchored on the price (withdrawn, moves nothing) |
| delivered numbers moved | the central, +19.4%; bear/bull rebuilt on filed evidence; the relative lens withdrawn |
| gates newly red on this study | `check_lens_design` — honestly, on the circularity; AMOC is on that ratchet |
| scheduled | the own-history multiple returns with the [R-FCAL-01 AMENDED] valuation-input block at AMOC's next walk-forward run |

---

*AUDITED CENTRAL: 11.8342* — the figure this review audits, stated so a job outside the study
can tell whether the review still describes the answer the study publishes. A review of a
number the study no longer carries is not a review of this study.
