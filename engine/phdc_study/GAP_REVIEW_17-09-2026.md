# PHDC — GAP REVIEW [R-GAP-01]

- AUDITED CENTRAL: 20.8823 (EGP per share)
- AUDITED SPOT: **EGP 14.40**, the Egyptian Exchange close of 3 September 2026 — the latest
  close this repository holds, from its own supplied-price register, and the price
  [R-GAP-01] measures against. The persistent price history ends earlier, on 23 August
  at 15.200, and that is what the site's ticker page shows and what section 2's trend
  read and section 3's distribution are computed from. A third-party feed shows
  EGP 13.77 on 16 September, below both.
- AUDITED GAP: +45.02%, above the price. The two-sided band of [R-GAP-01] fires at ten per cent
  in either direction, so this review is required.
- PRIOR EDITION: EGP 21.09 (10 September 2026), struck against the same 3 September close.
  This response moved the answer **down** by 0.98%.

**THE DIRECTION IS THE FIRST THING TO SAY.** This edition responds to a forensic audit of a
rebuild struck outside this repository, and every accepted finding that moved the number
moved it AWAY from the traded price or left it alone. The one finding that moved it toward
the price — the minority's share of value, from the FY2025 share alone to the three-year
mean — was adopted on instruction after the audit priced it, and it is worth −1.3%. Nothing
here was chosen for its direction, and a +37% gap is not evidence that it was: the same
model published +46.5% a week ago against this same close, and the corrections narrowed it
to +45.0%.

**WHAT WOULD MAKE THIS REVIEW WORTHLESS** is treating the gap as the finding. It is not. The
finding is below, under heading 8: on ONE driver a reader can check, this study and the
market are 204 basis points apart, and the market's number sits inside the range the
company's own filed cash-flow statements show.

---

## 1 · LATEST FILINGS

**Every disclosed period this study can reach has been read, and the reach was tested today
rather than assumed.** The information set ends at **1Q2026** and the most recent document
consumed is PHD's 1Q2026 earnings release together with the reviewed consolidated statements
at 31 March 2026.

Searched live on 17 September 2026, with the result recorded either way:

| Channel | Result |
|---|---|
| PHD's own result centre | HTTP 200, 86 PDFs. **The newest document of any kind is 1Q2026** — `PHD Consolidated FS Q1 2026` and `PHD - 1Q2026 Earnings Release`. No 2Q or H1-2026 statement or release is posted. |
| PHD IR presentations | HTTP 404 on both candidate paths. The September 2022 investor presentation and the corporate brochure an external audit cites for price and construction cost per square metre, per-project unit mix and a disclosed 5–7 year receivable life **could not be reached**. |
| egx.com.eg | Empty reply from the server, twice. The Exchange's filing record, treasury-share disclosures and board/Article-48 filings are unreachable. |
| Mubasher | HTTP 403. |
| cbe.org.eg auctions | HTTP 200, a 269-byte empty shell. No Egyptian auction curve could be read. |

**THE H1-2026 FILING IS REPORTED AND NOT HELD, AND THAT IS NOW SAID IN THOSE WORDS.** An
external audit states PHD filed reviewed statements to 30 June 2026 with the Exchange on
18 August 2026 and quotes figures from the attachment. This study has not obtained it. It
therefore publishes nothing from it — and the superseded rebuild's defect was the opposite:
it consumed those figures and printed them under a column headed "31 Mar 2026 (reviewed)"
while telling the reader four times that no half-year figures existed. A report of a
disclosure is a lead and never a source; an unread source is not a licence to publish its
numbers under another date.

**WHAT DID GET CONSUMED FROM THE FILINGS THIS TIME, and it is the substance of this
edition.** The 1Q2026 release's own income statement, in thousands, replacing its headline
bullets in rounded billions: revenue **9,346.133** for 9,300, gross profit **3,309.973** for
3,300, net profit after tax and minority **1,205.253** for 1,200, and the prior-year quarter
read outright at **8,392.553** rather than inferred from a rounded "up 11 per cent". The
FY2026 revenue anchor is built from that quarter over 1Q2025's share of FY2025, so the
rounding compounded through all fifteen forecast years. Also newly consumed: 1Q2026
operating cash flow of **1,766.705**, FY2025 regional new sales, the FY2026 handover
disclosure, and the FY2024 handover disclosure.

## 2 · BASE YEAR

**FY2025 audited remains the base year and it foots to the filed statements.** Revenue
36,169.3, gross profit 14,887.6, finance cost 3,347.5, profit after tax and minority
4,216.7, operating cash flow 1,424.2 — each from the FY2025 consolidated statements. A
working-capital cycle measured on full years is not restarted from a quarter, so the quarter
moves the ANCHORS and not the base.

**WHAT IS SOLVED RATHER THAN FILED, NAMED.** The delivered-unit count. PHD publishes no
delivered-unit count for any period after FY2024, so every count from FY2025 onward is
implied from revenue divided by revenue per delivered unit, and the FY2024 figure the price
per unit is built from is the company's own approximation — "handed over units exceeding
c. 2,000 units during the period". Because the count is implied, cost per unit collapses to
price per unit times one minus the held margin by construction, whichever way it is written.
So **gross margin is a HELD INPUT here and cost per unit is solved from it**, at the latest
disclosed level (1Q2026, 35.42% computed from 3,309,973 over 9,346,133 rather than from the
rounded 3.3/9.3 the superseded edition used). Four surfaces in this study once called the
margin an OUTPUT; all four now say what the code does.

**AND THE COMPANY'S OWN FY2026 HANDOVER FIGURE IS PRINTED BESIDE THE MODEL'S.** The 1Q2026
release states that "a total of 1,200 contractual units were ready to be handed over in
FY2026". The model implies 2,042. They are different measures — units available for handover
is not deliveries booked, and the identical 1,200 appears in the 3Q2025 release for
end-9M2025, so the company is repeating rather than updating it — but a study that anchors on
deliveries owes the reader the company's own number and its reason for not using it. It did
neither before; it does both now.

## 3 · MACRO COHERENCE

**One path, shared with every EG study, and this study carries no inflation number of its
own [R-MACRO-01].** Price and cost escalate on the house Egyptian path: 16% in 2026 falling
to 12 / 9 / 7.5 / 7 and holding 7% to the terminal. The terminal rate is the Central Bank of
Egypt's published Q4-2026 inflation target.

**THE ONE INCOHERENCE HERE HAS BEEN REMOVED.** The workbook published a cell labelled "Price
escalation" holding the Egyptian CPI three-year trailing mean of 25.2%, which the model does
not escalate at in any year, and no formula on any sheet read it. It is now a live reference
to the first year of the path the model runs, with the whole path published year by year on
the DCF sheet, and the trailing mean is labelled as considered and rejected: a trailing mean
of the worst inflation in Egypt's recent record is not a forecast, and the central bank's own
target contradicts it.

**ONE ESCALATOR DRIVES PRICE AND COST ALIKE, so gross margin is flat by construction.** That
is a limitation and it is stated: the filings disclose no cost decomposition at all, so there
is nothing to escalate a cost line on independently. The margin is sensitised in section 1.9
rather than extrapolated.

## 4 · DISCOUNT RATE

**The operating rate is the adopted one and cash is charged for once.**

| | |
|---|---|
| Expansion-window WACC | **24.9647%**, the traded default-swap basis, which section 1.8 marks ADOPTED |
| Alternative published beside it | 25.8307%, the credit-rating basis; no cell reads it and it is labelled as not used |
| Terminal WACC | **14.9743%** |

**THE TERMINAL RATE NAMES EVERY COMPONENT**, which is the defect the audit found in the
rebuild struck outside this repository — there it was a bare 16.1547% with no construction
anywhere in three delivered files. Here: terminal risk-free **10.50%**, mature-market equity
premium **7.00%**, country premium **2.77%** split out of the market premium rather than
carried on the measured beta, pre-tax cost of debt **15.00%**, debt weight **44.90%**. That
is the house construction and it is read from the shared macro path, not from a real-rate
convention typed inside this study.

**CASH IS CHARGED ONCE.** Free cash flow is struck at the firm level and discounted at a WACC
whose weights stand on GROSS debt; net debt is then deducted once in the bridge. The company
is net *debt*, so the net-cash pathology that produced the AMOC failure cannot arise here.

**AND TWO CROSS-CHECKS NOW REASON OFF THE ADOPTED BASIS.** Sections 1.2 and 1.4 previously
capitalised at the credit-rating cost of equity of 30.77% while the model discounts on the
swap basis at 29.20% — so the study argued about whether the company earns a cost of capital
it is not charged. Both now name the adopted figure first and the alternative beside it.

## 5 · TERMINAL

**Terminal growth of 7.00% against 7% inflation inside the terminal discount rate: zero real
growth, which is the conservative middle and is coherent by construction.** The terminal
carries **36.1%** of enterprise value (29,567.0 of 81,876.6). That is high, it is published
as high, and it is why the answer is published as a range.

**THE CONSTRUCTION IS NOW VISIBLE IN THE WORKBOOK, CELL BY CELL.** Every earlier edition of
this workbook carried the discounted terminal as a single hardcoded number holding roughly a
third of the answer, with no terminal flow, growth rate, capitalisation rate or formula
anywhere in sixteen sheets. The DCF sheet now publishes the terminal flow, the growth rate,
the terminal cost of capital, the terminal value and its discounted value as five formulas,
and the bridge reads them. Changing terminal growth on the Assumptions sheet now moves the
answer the way the workbook's own warranty says it does.

**AND THE ALTERNATIVE IS PRICED.** The 12% terminal growth earlier editions carried is worth
EGP 38.45 a share, +84%. It is rejected because 12% nominal in perpetuity exceeds Egypt's own
long-run nominal GDP growth in the same currency, which makes the company the economy.

## 6 · BALANCE SHEET

**The bridge stands on the latest disclosed balance sheet this study has read — 31 March
2026, reviewed — and every figure in it is confirmed against the company's own release.**

| Line | This study | PHD 1Q2026 release, EGP thousand |
|---|---|---|
| Total assets | 177,979.015 | **177,979,015** |
| Total non-current assets | 63,115.069 | **63,115,069** |
| Total current assets | 114,863.946 | **114,863,946** |
| Cash | 9,125.128 | **9,125,128** |
| Equity attributable to the parent | 18,955.743 | **18,955,743** |
| Non-controlling interest | 1,432.670 | **1,432,670** |
| Total non-current liabilities | 49,497.422 | **49,497,421** |

Matched to the thousand. The bridge deducts net debt of **23,244.719** — gross borrowings of
32,369.847 from the study's own eight interest-bearing lines, less cash — and adds associates
of 3,838.697 and investment property of 1,020.475, all at 31 March 2026 and all labelled 31
March 2026.

**THIS IS WHERE THE AUDITED REBUILD FAILED AND WHY THE CORRECTION MATTERS.** That rebuild's
column headed "31 Mar 2026 (reviewed)" held total assets of 194,767.3, cash of 7,804.2 and
minority interest of 1,723.0 — the 30 June figures — and its bridge deducted net debt of
27,471.2. The audit's own "true 31 March" column is the table above. It also priced the
correction at +1.45 a share on net debt of 23,076.3; that figure drops two lease-liability
lines from the study's own eight-line definition, and the correct figure is 23,244.719,
which this study's own foot reproduces exactly and which the release now corroborates.

**THE MINORITY COMES OUT OF EQUITY VALUE, NOT ENTERPRISE VALUE, AND AT ITS SHARE OF VALUE
RATHER THAN AT BOOK** — the model capitalises all of a subsidiary's cash flow, so the
minority's claim is worth its share of that value. The share is now the **mean of the filed
profit share over FY2023–FY2025, 5.9367%**, adopted on instruction. The FY2025 share alone
(4.6838%, worth +1.3%) and the book share of equity on this sheet (**7.0269%**, worth −1.2%)
are both published. An external audit quoted the book basis as 8.35%; on this sheet it is
7.03%, and that figure of the audit's is wrong.

## 7 · CLAIMS AGAINST THE RECORD

Every "best ever", "never", "not disclosed" and "only" checked against the filings. Six
claims failed and are corrected.

| The claim | Tested against | Verdict |
|---|---|---|
| "No half-year 2026 figures had been released" | PHD's result centre, read live 17-09-2026 | **TRUE OF THE CHANNEL SEARCHED, and now scoped to it.** The result centre carries nothing newer than 1Q2026. A filing is reported to exist with the Exchange; the search is dated and the reach is named. The superseded rebuild consumed that filing while printing this claim, which is the reverse failure. |
| §5 catalyst: "None had been published as at 30 August 2026" | The edition's own date | **FAILED — false and stale.** It carried a superseded edition's date inside a later document and told the reader the half-year results were still to come. Corrected. |
| "the sum of the regional unit series overstates the company total by about a third because the charts overlap" | This study's own extract of the release charts: 21 year-and-vintage pairs | **FAILED.** The three regional series equal the printed company total EXACTLY in 19 of 21 (2017 2,136; 2018 3,102; 2019 2,470; 2020 1,840; 2021 3,350; 2022 4,033). Worst discrepancy anywhere: −3.0% in 2016, +0.8% in 2023. Nothing near a third. **Negative result withdrawn.** |
| "FY2024 and FY2025 unit counts are absent rather than inferred" | PHD 4Q2024 release | **HALF FAILED.** FY2024 handovers are disclosed ("exceeding c. 2,000 units"), and the same release charts FY2024 units sold by region at 4,192 / 2,839 / 453 — the figures this study already uses. Only FY2025 is genuinely absent. |
| "The three regions reconcile to the group total the same release prints" | The 1Q2026 release, every charted year | **FAILS IN FY2025 AND THE FAILURE IS NOW PUBLISHED.** 2024: 44,570 + 11,364 + 95,082 = 151,016 exactly. 1Q2026: 52,059 exactly. **FY2025: 88,337 + 20,751 + 54,904 = 163,992 against a printed 215,384 — 51,392mn, 23.9%, attributed to no charted region.** The study never consumed FY2025, so its own integrity check had never met the year it fails on. |
| "Gross margin is an OUTPUT of price against cost, never an input" | `bottom_up_model.py` | **FAILED on the fourth surface.** Three prose surfaces were corrected on 10-09-2026; the machine-readable driver record `assert_ground_up()` actually reads still said OUTPUT. Corrected. |

**AND ONE CLAIM MADE AGAINST THIS STUDY WAS TESTED AND REJECTED.** An external audit states
PHD publishes an "Outstanding shares" count net of treasury of 2,839,980,164 at 31 March
2026, against the 2,859,914,173 issued count this study divides by. Neither the 1Q2026 nor
the 4Q2024 release carries a share count at all (checked live), and the one third-party
source reachable from here reports 2,859.91mn — which agrees with this study's divisor. The
claim is unresolved rather than accepted, and both figures are registered.

## 8 · MULTIPLE CROSS-CHECK

**The reverse read is the useful statement, and it is much narrower than the gap.**

| | At the central 20.88 | At the price 14.40 |
|---|---|---|
| P/E on FY2025 earnings | 14.2× | 10.3× |
| P/E on the model's FY2026 | 22.4× | 16.3× |
| EV/EBITDA on FY2025 | 7.9× | 6.2× |
| Price to book, 31-Mar-2026 | 3.15× | 2.29× |
| Market value over the order book | 22.7% | 16.5% |

**Solved back through the model, holding every driver at its published value and varying only
cash conversion, the price of EGP 14.40 pays for a conversion rate of 6.387%.** This study
forecasts **8.714%** — the mean of the three years PHD has published a cash-flow statement
(4.333%, 17.870%, 3.938%). **The disagreement is 204 basis points on one driver a reader can
check, and the market's implied figure sits INSIDE the filed range.** That is the honest
reading of +37.4%: not that the market is wrong by a third, but that it is pricing a
collection rate two points below the three-year mean and above the two weak years.

**A NEWLY CONSUMED OBSERVATION CUTS THE OTHER WAY AND IS PUBLISHED ANYWAY.** 1Q2026 operating
cash flow of 1,766.705 on revenue of 9,346.133 is **18.90%** — above the strongest full year
on record. It is not the anchor: a quarter is not a year for a company whose collections and
construction both swing with which project completes, and 1Q2025's own 12.07% against
FY2025's 3.94% measures that seasonality directly. It is recorded because the reader should
see the newest number and the reason it is not used, rather than discover it later.

**THE CONTESTED DIRECTION COUNT IS THREE UP, THREE DOWN** on the six judgements re-runnable
against this model: the interest add-back's footing +69.6%, terminal growth +84.1%, the
FY2025 minority share +1.3%; against the flat discount rate −65.2%, a five-year window
−74.6%, the minority at book −1.2%. A study resolving every contested choice one way is how a
lean survives an audit of its steps. This one does not.

---

## VERDICT

**The answer is audited and stands at EGP 20.8823 against EGP 14.40, +45.02%.**

The gap is not explained by a defect, and the hunt for one was run before this was written
[R-GAP-04]: the model was rebuilt independently from the workbook's own cells, every typed
constant was put against its derived equivalent — which found five separate typed copies of
the spot price, two typed edition dates and a hardcoded bridge — every source string was put
against what the filings actually disclose, and the contested register was tested for a lean
inside each category and not only across the file. What the hunt found is in this document
and in `CRITIQUE_RESPONSE_17-09-2026.md`, and none of it closes the gap: the corrections
moved the central DOWN by a point, from 21.09 to 20.88.

**THE LARGEST UNRESOLVED CONSTRUCTION IS NAMED RATHER THAN RESOLVED IN THE DIRECTION THAT
FLATTERS IT.** Free cash flow adds back the FY2025 finance charge after tax, flat and nominal,
for fifteen years, while operating cash is set as a share of revenue. Those two do not sit on
the same footing: the charge ran at 9.26% of revenue in FY2025 and this model holds it at a
level that is 8.3% of revenue in 2026 and 1.4% by 2040. Putting the add-back on the revenue
ratio — the internally consistent reading — is worth **+69.6%**. It is not adopted. Because
operating cash is exogenous here, raising the modelled charge raises free cash flow and
nothing offsets it, so a consistency correction worth seventy per cent upward is
indistinguishable from fitting. Which footing is right depends on where PHD presents interest
paid, and that cash-flow statement is a scan this study has not read. The conservative
construction is kept and the alternative is priced in the contested register.

**WHAT WOULD OVERTURN THIS.** The H1-2026 filing, which would move the bridge onto a newer
sheet and settle the conversion rate for a fourth period. The FY2025 audited cash-flow
statement, which would settle the interest add-back's footing and could split the
EGP 16,938.5mn wedge between the balance sheet and the cash-flow statement that this study
measures and does not decompose. A full-year 2026 conversion rate near 6.4%, which would say
the market was right and this study's three-year mean was the wrong anchor. Or a refreshed
price register: this study strikes against the 3 September close of 14.40 and a third-party
feed shows EGP 13.77 on 16 September, 4.4% below it, which would widen this gap rather than
close it. The persistent price history, which the site's ticker page and this study's own
cone are built from, has not been refreshed since 23 August and is the artefact most
overdue here.
