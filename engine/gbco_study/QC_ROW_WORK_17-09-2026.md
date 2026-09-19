# GBCO — working the QC gate's FAIL rows, 17 September 2026

The 07-09-2026 QC gate returned **NOT DELIVERABLE** on five rows. Step 5 hands the study to an
external auditor, and handing one a study our own gate already blocks spends their pass
re-finding what we know. So the rows were worked first.

**THE SCORE, STATED BEFORE THE DETAIL RATHER THAN AFTER IT:** of the five, **two were already
closed on 8 September** and this document's own first draft claimed them — corrected in §3 and
§4, along with the finding that covers both, which is that **the gate itself is stale and is the
instrument step 5 would have handed over** (§4a). **One is closed by this pass** — the
asset-conversion cycle, built from the disclosed segment tables (§1). **Two remain open**, and
the larger of them is open for a reason worth more than the row: **the gate's own pricing of it
is understated by a factor of four and a half, and the obvious fix is not a fix** (§2).

Nothing here moves the published answer. **bear 19.2911 · 41.3484 · 52.3453 against EGP 28.98
of 3 September stand exactly as delivered.** Why they stand is the substance of §2.
---

## 1 · ROW 21 — the asset-conversion cycle: **BUILT**

SIGCM clause 4 asks that DSO, DIO and DPO be studied from the statements. They now are —
`asset_cycle.py` → `asset_cycle.json`, four periods, from GB Corp's own disclosed segment
tables.

| period | DSO | DIO | DPO | **CCC** | WC / revenue | balances |
|---|---|---|---|---|---|---|
| FY2023 | 27.2 | 131.9 | 126.5 | **32.6** | 19.1% | closing |
| FY2024 | 21.4 | 133.7 | 121.6 | **33.5** | 23.2% | average |
| FY2025 | 25.0 | 149.0 | 112.7 | **61.3** | 28.7% | average |
| 1H2026 | 25.6 | 127.1 | 83.3 | **69.3** | 21.4% | average |

**EVERY DISCLOSED TABLE FOOTS TO ITS OWN STATED TOTAL** before a day is computed — five
quarters, components summing to the published working capital to within EGP 0.1mn. Arithmetic
is the arbiter, not the extractor's confidence.

**THE HARD PART WAS NOT THE ARITHMETIC, IT WAS THE DENOMINATOR.** GB Corp contains a lender.
Consolidated "Accounts and notes receivables" is EGP 13,465.1mn at 31-Dec-2025 against GB
Auto's own disclosed trade receivables of **EGP 5,316.9mn** — the difference is GB Capital's
loan book, a financing asset. A group-level DSO divides a lender's book by an assembler's
revenue and produces a days figure two and a half times too long: large, robust and entirely
spurious, which is [R-FCAL-01]'s interest-rate trap arriving in working-capital costume. The
cycle is built on the **auto segment**, the leg the cash-flow lens actually values, and whose
disclosed total is the `WC_OPENING = 18,917.0` the model already carries.

**TWO BASIS BREAKS REGISTERED RATHER THAN SMOOTHED.** The 4Q23 release publishes payables NET
of finance-lease liabilities and the 4Q24 release publishes the same date gross; the
difference of 275.8 reconciles to the pound against the 275.9 that release's own footnote
names. FY2023 is therefore computed on **closing balances only** — averaging a net-basis
opening with a gross-basis closing is a days figure with no definition. Separately, group
receivables are restated twice (FY2024 7,581.3 → 8,334.2; FY2025 13,465.1 → 14,157.9), noted
beside rather than substituted.

**WHAT THE CYCLE SAYS ABOUT THE COMMITTED LADDER — and it is not what was expected.** The
model projects working capital at 26.5% of auto revenue falling to 21.5%. The **latest
reviewed period runs 22.78% on trailing-twelve-month revenue.** So the committed ladder opens
nearly four points ABOVE the latest actual and lands on it — it charges the company more
working capital than it is currently running. The typed ladder is **conservative**, and the
build confirms it rather than overturning it.

**ONE HALF OF THE STUDY'S STATED MECHANISM IS CONTRADICTED BY THE FILINGS.** The study says
working capital falls "as payables re-extend and the pre-build unwinds". The pre-build
unwinding is measured and real: inventory days fell 149.0 → 127.1 and inventory fell in
absolute terms while revenue grew 30%. **Payables re-extending is the opposite of what
happened** — payable days fell by a third, 112.7 → 83.3, and that is the single largest mover
in the cycle. A mechanism contradicted by the company's own filings is not a mechanism
[R-ANCHOR-01]. The wording is corrected at the next edition; the direction of the error is
against the company, so it does not flatter the answer.

**WHAT IS STILL OPEN:** the cycle is built and published, and the model still projects working
capital from an intensity ratio rather than FROM the days. Converting the projection is a
model change and belongs with §2's dependency, not ahead of it.

## 2 · ROW 30 — guidance consumed as a driver: **REAL, AND THE OBVIOUS FIX IS NOT A FIX**

**The breach is confirmed.** `compute.py:213` sets first-year capital expenditure to EGP
3,000mn and §1.2 says in terms that it "follows the EGP 3,000mn **guided** for the first
year". [R-FCAL-01] is unambiguous: **guidance is scored and never consumed**, because
management's forward targets lean the same way an optimistic model does.

**THE GATE'S OWN PRICING IS UNDERSTATED 4.5×, AND THE REASON MATTERS.** The gate measured the
fix at "EGP −8.98 or −6.14 a share". Reproduced here exactly — holding capex at the filed
FY2025 intensity takes the present value of explicit free cash flow from **+6,915 to −2,830**,
which is the gate's figure to the million. But the gate stopped at the explicit window, and
offered as a mitigation that "the terminal is 84% of the auto leg, so the explicit window
carries about a sixth of it." **That reasoning runs backwards.** The terminal capitalises the
FINAL explicit year's free cash flow, so a capex level held flat through FY2030E hits the
terminal too — and by more. Flowed through: **−40.34 a share, not −8.98.**

**AND AT THAT POINT THE CORRECTION CONDEMNS ITSELF.** It drives the auto leg to *negative
equity* on a business filing EGP 66bn of revenue and covering its depreciation 3.7 times. A
correction that produces an absurd answer is a wrong correction, and the reason it is wrong is
visible in the arithmetic: capex intensity on revenue has been **falling mechanically** —
8.78% → 6.79% → 5.56% — while revenue nearly tripled in an inflating currency. Holding a
falling ratio flat is not "holding the actual flat"; it is a hypothesis about the asset base
dressed as a measurement. [R-TERM-01 CLAUSE TWO CORRECTED], exactly: **a ratio between two
quantities defined differently is not evidence about either.**

**THE ONE COVERAGE THE FILINGS DO DISCLOSE, AND WHAT IT SHOWS:**

| | capex | D&A | **capex / D&A** | capex / auto revenue |
|---|---|---|---|---|
| FY2023 | 2,056.0 | 531.4 | **3.87×** | 8.78% |
| FY2024 | 3,171.9 | 1,138.5 | **2.79×** | 6.79% |
| FY2025 | 3,664.2 | 999.3 | **3.67×** | 5.56% |
| committed forecast | 3,000 → 2,800 | | **3.47× → 1.76×** | 3.82% → 1.93% |

**So the finding is sharper than the gate's.** The guided first year happens to land on the
company's own disclosed coverage — 3.47× against FY2025's 3.67×. **What is unsourced is the
DECLINE from it**, to 1.76× by FY2030E, below every year the company has filed. That is
[R-ANCHOR-01 CLAUSE TWO] precisely: a rate declining materially from its own opening year
makes the same claim as one opening below the filed record, and must name a mechanism. None is
named.

**AND THE CORRECTION CANNOT BE PRICED HONESTLY YET. THIS IS THE FINDING.** Holding coverage
flat at the filed FY2025 3.6668× is worth **−22.91 a share**; with the cycle-based working
capital beside it, **−30.59**, which would carry the study from +42.7%/+80.6% above the price
to −62.9%/−24.9% below it. **That number is manufactured by a construction this house has
already retired.** GBCO's terminal is `FCFF_FY2030E × (1+g)/(w−g)` — a perpetuity struck on
the last explicit year — so it capitalises that year's growth capital and its working-capital
build forever at roughly fifteen times, charging the company for growth it will never have.
GBCO sits on the [R-TERM-01] ratchet for this (`no nopat_term, no ic`), and
`engine/terminal_value.py` **refuses to build it**, because `useful_lives.json` records that
no usable asset life is sourceable: the policy note discloses rate ranges spanning 3 to 50
years, and the derived identity is contaminated by an undisclosed land component. That refusal
was right and stands.

**SO THE LEVERS HAVE A DEPENDENCY AND THE ORDER IS FIXED HERE, IN ADVANCE, PER [R-REBUILD-01]:
terminal first, then the capex anchor, then working capital from the days.** Correcting capex
first and the terminal second would multiply a real correction through a retired construction
and land somewhere neither lever supports — which is the stacking failure that rule exists to
stop, and it is visible here BEFORE it happened rather than after.

**WHAT IS UNDERNEATH ALL OF IT, AND IS THE MORE USEFUL HALF:** capital expenditure,
depreciation and working capital are **three independent typed ratios with no balance sheet
connecting them.** Capex runs at 3.82% of revenue and D&A at a flat 1.1%, so the model spends
three and a half times its depreciation every year and the asset base it is buying never
appears anywhere, never depreciates and never constrains anything. That is SIGCM clause 7 —
driver → IS → **BS** → CF → DCF, every statement a live formula model — not being met for
property, plant and equipment. **Fixing any one of the three ratios in isolation is arithmetic,
not modelling**, and that is why row 30's obvious fix produced an absurd answer.

**WHAT IS RECORDED, THEREFORE:** the breach stands, priced at −22.91 through the current
terminal and *unpriceable* through a correct one; the dependency is named; and no fair value
moves on a lever whose magnitude is an artefact of a construction already on the ratchet.
[R-GAP-02] clause three holds this study from publishing on the method in any case, so no
reader receives the breach meanwhile.

## 3 · ROW 44 — the driver ledger: **ALREADY CLOSED ON 8 SEPTEMBER, AND THIS PASS NEARLY CLAIMED IT**

**A CORRECTION TO THIS DOCUMENT'S OWN FIRST DRAFT, recorded rather than quietly fixed**, because
it is the same failure the gate exists to catch. This pass wrote a fresh GBCO section into
`engine/Fundamental_Driver_Ledger.md` listing thirteen non-sourced drivers — and the ledger
**already carried that section**, dated 08-09-2026, naming every one of them. The draft would
have left two records of one fact, which diverge the moment somebody prunes one. It was
replaced with a dated correction beneath the existing entry, appended rather than rewritten.

**WHAT THE CORRECTION ADDS IS REAL, AND TWO ITEMS OF IT ARE FIXES TO THAT ENTRY:** the capex
figure of "EGP 8.98 a share" is understated 4.5× for the reason in §2; and its second stated
mitigation — that a terminal carrying 84% of the leg makes an explicit-window driver matter
*less* — is backwards for a driver held flat to the final explicit year, where it makes it
matter roughly fifteen times *more*. It also adds the disclosed capex/depreciation coverage
table, the superseded working-capital evidence, and the order of levers.

## 4 · ROW 10 — the external-reader scrub: **ALREADY CLOSED ON 8 SEPTEMBER**

Not closed by this pass, and the first draft of this document said it was. `scrub.py` was
committed on 8 September (`ef81e3be4`), scans both delivered documents against fifteen banned
patterns with three ordinary senses declared, and returns **0 hits**. Verified here by running
it, and independently by extracting both `.docx` files and counting — zero occurrences of
`walk-forward`, `hard gate`, `valuation-input block`, a rule identifier or a repository path.

**THE PROBE WAS NEGATIVE-CONTROLLED BEFORE THE ABSENCE WAS BELIEVED** [R-ENF-04]: the
extraction yields 33,150 characters with 29 hits for "GB Corp" and 22 for "source", so the
empty result is the document's property and not the probe's.

## 4a · THE FINDING THAT COVERS BOTH: **THE QC GATE IS STALE, AND IT IS THE INSTRUMENT STEP 5 HANDS OVER**

Two of the five blocking rows were closed the day after the gate was written, and the gate
still reads NOT DELIVERABLE on all five. Every individual statement in it was true when
written; nothing in it is careless. **But it is dated 07-09-2026 and six commits have landed on
this study since**, and it is the artefact an external auditor would have been handed as the
statement of what is wrong.

This is [R-ENF-06] on a document rather than on a JSON — *an artefact every reader consumes and
nothing rewrites is a judgement frozen at the date somebody last typed it* — and the existing
enforcement does not reach it: `check_artefact_currency.py` requires a generated artefact
carrying a valuation figure to declare the central and spot it was built against, and a QC gate
carries a VERDICT rather than a valuation, so it declares nothing and nothing compares it to the
tree. **A gate whose verdict has been overtaken looks exactly like one that has not.**

## 5 · ROW 22 — peers studied for KPIs and multiples: **OPEN, AND NOT CLOSED BY ARGUMENT**

The gate's reading is right: peers are characterised, not studied, and the `Peer & Sector`
sheet carries no numeric cell. The study's own defence — that no clean comparable exists — is
an honest finding and is not what SIGCM clause 5 asks for, which is that peers be studied and
the figures sourced and dated. It is not closed here. **Naming it is not the same as closing
it, and it is not moved to a different heading to make it go away.**

---

## WHAT THIS CHANGES ABOUT STEP 5

The study goes to the external auditor **with this document beside it**, so their pass is spent
on what we have not found rather than on what we have. The gate's verdict stands at NOT
DELIVERABLE: rows 30 and 22 remain open, and row 30 is open for a reason that cannot be closed
on this name without a disclosed asset life the filings do not carry.
