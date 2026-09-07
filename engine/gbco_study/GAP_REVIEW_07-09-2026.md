# GBCO — GAP REVIEW [R-GAP-01]

**7 September 2026.** Written because the rebuilt central sits more than 10% from the latest
known price. The trigger is two-sided since 02-Sep-2026, and this one fires on the UPPER
side, which is the side that gets no automatic hold and therefore needs this review most.

**REWRITTEN 7 September 2026, second pass.** The study this reviewed published a weighted
blend of four lenses and a single central of 44.3295. That construction is retired: the class
primary is the answer, and on this name the answer has **two sides**, because GB Corp's
largest component is carried two ways in its own disclosures. Every heading below stands;
the header, heading 8 and the verdict are rewritten against the answer the study now
publishes. **A REVIEW OF A DIFFERENT ANSWER IS NOT A REVIEW.**

- AUDITED CENTRAL: 41.3484  (EGP per share — MNT-Halan at its reviewed carrying value)
- AUDITED CENTRAL: 52.3453  (EGP per share — MNT-Halan at the June-2026 round price)
- AUDITED SPOT: **EGP 28.98**, the supplied close of **3 September 2026** — the latest price this repository holds
- AUDITED GAP: +42.7%   (the nearer branch; the far branch is +80.6%)

**A TWO-SIDED ANSWER IS AUDITED ON EVERY BRANCH.** Publishing two numbers instead of one is
not a way to publish two unaudited numbers, so both are stated above and both are audited
below.

**The price, and why it is this one — including a correction to this run's own first
answer.** GBCO carries no price in `engine/prices/SUPPLIED_07-09-2026.json`, and this run's
first probe read only that file and concluded there was none. That was wrong: **GBCO is in
`SUPPLIED_03-09-2026.json` at EGP 28.98 as at 3 September 2026**, and `gap_today.py` merges
every supplied file on each price's OWN date precisely so that a name priced on Thursday and
absent from Monday's file is still priced. A probe that read one place is not a probe that
found nothing elsewhere [R-ENF-04]; the error is recorded here rather than quietly fixed.

The study is therefore struck at **EGP 28.98, 3 September 2026 — four days old**. The cone is
a different clock and is anchored where it has to be, on the exchange library's last real
session (EGP 29.51, 23 August 2026), because a probability cone needs a session series and a
hand-supplied close is not one. Both dates are published. The delivered edition was struck
against a study-local price extract stopping at 7 July 2026 (EGP 31.25), which this rebuild
retired outright.

**The rule does not say the answer must change.** It says the answer is audited before it
ships. What follows is that audit, heading by heading.

---

## 1 · LATEST FILINGS

**This is where the largest single finding of the run sits, and it is not about the answer.**

Until today `engine/gbco_study/` held **no filings at all**. Its own README recorded that
the historical financials were "gathered in conversation rather than by code", and the
directory's rebuild-readiness note of 5 September recorded six routes run to obtain them,
all six failing, and an escalation registered with a default date of 19 September. **SIGCM
clause 1 had nothing behind it on this name.**

That record was re-run today, as [R-IND-01] requires of any probe whose failure is relied
on, and it was **wrong about the world rather than about the attempt**:

| route as recorded 05-09 | re-run 07-09 |
|---|---|
| `gbauto.com` — "a Cloudflare challenge; the host exists" | it exists and **it is not GB Corp**: it 301-redirects to a `sedo.com` domain-sales lander. The challenge was the parking service's. |
| `gb-corp.com` — "fails to connect" | HTTP 200 — and also a parking lander (`/lander`) |
| the company's own site — unreachable | **`gb-corporation.com` and `ir.gb-corporation.com` both return HTTP 200 and are GB Corp's own investor-relations site.** Neither hostname had ever been tried. |

The ladder had been climbed carefully and had guessed a naming convention. **A reader that
guesses a name silently finds nothing and reports that as a result.**

Read and committed to `engine/gbco_study/src/` in this run: the audited consolidated
statements for FY2020–FY2025; the reviewed consolidated and standalone statements to
**31 March 2026 and 30 June 2026**; GB Corp's own annual reports for 2013–2025; the 4Q
earnings releases for FY2019–FY2025 and the **1Q26 and 2Q26 releases**; and the 1Q26
investor presentation. The most recent period actually READ is **1H2026, from the 2Q/1H26
earnings release dated 13 August 2026** and the reviewed 30-June-2026 consolidated
statements. Every fiscal year from 2012 to 2025 now foots against its own arithmetic
(`engine/gbco_walkforward/build_panel.py`, fourteen years, all FOOTS).

## 2 · BASE YEAR

The forecast opens on FY2026 and **1H2026 is filed**, so the base year is testable rather
than asserted. Group revenue for the half is EGP 48,474.4mn against 35,850.0mn a year
earlier, +35.2%; gross profit 7,421.9mn at a 15.31% margin against FY2025's 15.50%;
operating profit 3,661.3mn; net income 1,262.0mn.

The model's FY2026 **auto-leg** revenue of EGP 78,549.6mn is +18.4% on the FY2025 auto-leg
base of 66,358.3mn, against a group half-year already running +35.2%. **The base year is
conservative against the filed half, not stretched by it** — which is the direction that
argues against, not for, the premium being a modelling error.

Nothing in the base year is annualised, scaled or solved. **One figure is typed and not
sourced and it is named here rather than defended**: the tax rate of 28.0% in
`compute.py:125`. GB Corp's own filed effective rate was 28.1% in FY2025 and 23.5% in
FY2024, so the figure is inside its own record — but it carries no four-field entry and the
Egyptian statutory rate is 22.5%. Registered as an open item for the next edition; moving it
would RAISE the value, so leaving it stands against the gap rather than for it.

## 3 · MACRO COHERENCE

One path, and it is the house one. Inflation, the policy-rate glide, the sovereign quote and
the terminal all come from `engine/macro_paths/EG.json` through
`engine/cost_of_capital.py`; the study carries **no inflation number of its own**, and its
`inflation_inputs` block declares that, because the auto leg is built from **units × ASP**
with company-disclosed volume and price growth and no domestic CPI series escalates any line
in the model.

**Terminal growth is stored as a REAL rate on that path** — 0.0% real, recomputed to 7.00%
nominal against the path's 7.0% terminal inflation. The delivered edition typed a nominal
11.5% against a discount rate that never normalised, which nobody could falsify: it might
have meant inflation plus four points or minus three.

**One incoherence is open and it is disclosed rather than resolved.** The MNT-Halan
associate mark translates USD 1.4bn at **EGP 47.5/USD**, a rate typed in the delivered
edition, while the house path's own FX anchor is **50.25 as at 6 August 2026**. Correcting it
is a [R-MACRO-01] lever worth roughly +5.8% on 58% of the equity value — it moves the answer
FURTHER from the price and it was not in the lever order declared before this rebuild began,
so it is registered for the next edition rather than applied after the audit point. Adding a
lever after seeing the answer is the fitting this method forbids, whichever way it points.

## 4 · DISCOUNT RATE

Rebuilt in full, and this is lever L1 of the rebuild ledger.

- **Country risk is counted exactly once.** The delivered edition passed a RAW Egyptian
  10-year yield of 22.55% into the cost of equity AND added a country-risk-loaded equity
  premium on top of it. That is the systemic v1 defect — and it was FOUND on this very study
  ([L-004], "GBCO study; corrected across the book") and this study was never re-issued on
  the fix. rf* is now 23.00% − 3.41% = 19.59% on the market basis.
- **The beta is conforming and tier-1**: 0.8907 against the published EGX30, weekly W-THU,
  Dimson-corrected, n=251, R² 0.243, attested by `assert_beta_provenance`. The delivered
  edition used an assumed 1.0.
- **The cost of debt is computed on the borrowings that actually bear the interest.** GB Corp
  contains a LENDER, and GB Capital's cost of funds — EGP 3,756.9mn in FY2025 — is booked
  inside that segment's **cost of revenue**, not in the group finance-cost line. The group's
  expensed finance charge over group borrowings reads 14.1%, and over TOTAL liabilities 7.1%,
  against an Egyptian policy corridor above 24% throughout. On the whole interest actually
  incurred over average interest-bearing borrowings the rate is **26.53% (FY2025) and 29.06%
  (FY2024)**. The delivered edition adopted 20.7% — **below the 23.00% sovereign**, which a
  same-currency corporate cannot borrow at and which `cost_of_capital.py` refuses outright.
- **The operations are discounted at a schedule, not one crisis rate for ever**: 22.91% →
  19.81% → 17.32% → 15.45% → 14.21%, the glide inherited from the policy-rate path's own
  cumulative progress. The terminal is brought home on the SAME cumulative factor as the last
  explicit year — one date, one price of time.
- **Cash is charged for exactly once.** The auto leg is valued at the operating rate and its
  own net debt is deducted in the bridge; nothing is added back at face.
- Ke reproduces from rf* + β × ERP under the NAMED construction `same_beta` [R-COC-02].

**The staleness is accepted and disclosed, not hidden**: the house path's sovereign quote and
FX anchor are both dated 6 August 2026 and this study is struck on 23 August 2026 — 17 days,
beyond the 14-day bound. Refreshing a house macro path is a house-level act, not a step of one
name's rebuild.

## 5 · TERMINAL

**The sanctioned terminal could not be built and that is recorded rather than worked around.**
[R-TERM-01] requires a DISCLOSED useful life. Both admissible routes were run
(`engine/gbco_study/useful_lives.json`):

- **Route 1, the policy note** — GB Corp discloses **rate RANGES** per class (buildings 2–4%,
  machinery 10–20%, vehicles 20–25%, fixtures 6–33%, IT 25%) and no scalar, no dominant class
  and no weighting. That is a 3-to-50-year span. **Finding a range is not finding a life.**
- **Route 2, the identity** — depreciable gross cost over the annual charge gives **17.1
  years** including the land-and-buildings column and **10.9 years** excluding it, because
  land is not depreciated and the note does not disclose it separately. Worse, the derived
  per-class rates contradict the disclosed bands: machinery derives to 8.48% against a
  disclosed floor of 10%, and the land-and-buildings column to 1.17% against a buildings floor
  of 2%. **A derived life that contradicts the policy it implements is not a life.**

So the Gordon terminal stands, with growth corrected to the house path, and GBCO **stays on
the [R-TERM-01] ratchet with `useful_lives.json` named as the reason**. A life this desk chose
is not a disclosed life.

Terminal growth of 7.00% sits against a terminal discount rate of 14.21% whose own inflation
component is the same 7.00% — so the terminal is a **zero real growth** perpetuity, stated as
such, and not the perpetual real decline the delivered edition's arithmetic implied. The
terminal carries 84% of enterprise value, which is high and is stated: it is the arithmetic
consequence of a five-year window whose free cash flow is still building (FCFF 151 → 5,384)
because working capital absorbs the first two years' growth.

## 6 · BALANCE SHEET

The bridge stands on the **reviewed 30 June 2026 balance sheet**, the latest disclosed, read
from GB Corp's own 2Q26 release Table 12 and its reviewed consolidated statements. The
delivered edition stood on 31 December 2025 while both were published on the company's own
site. Auto-leg net debt is EGP 14,623.7mn on the **company's own net-debt definition** (short
and long-term debt plus lease obligations and due-to-related-parties, less cash) and the
auto leg's own non-controlling interest is EGP 590.7mn. The move is worth +0.9%.

The minority is deducted from EQUITY value, not from enterprise value, and at the segment's
own disclosed figure.

## 7 · CLAIMS AGAINST THE RECORD

Two, and the second is new to this run and material.

- **"GB Corp's ownership stake in MNT-Halan will be adjusted to 41.61%"** — recomputed
  against the company's own press release of 9 June 2026, which states it in those words.
  It holds.
- **THE FY2025 AUDIT OPINION IS QUALIFIED, AND THE QUALIFICATION IS ABOUT THE ASSET THAT
  CARRIES MOST OF THIS VALUATION.** The auditors state, in the FY2025 consolidated
  statements: *"We were not provided with the consolidated audited financial statements ...
  for one of the associate companies (MNT – BV) ... the group's share of the profits
  resulting from this investment"* rests on management-prepared statements. The MNT-Halan
  mark is **EGP 27,670.7mn**, 58% of this study's equity value and **86% of GB Corp's whole
  traded market capitalisation**, and it is carried at a private round price with no audited
  underlying. The delivered study called the read-through "a genuine, now-evidenced anomaly";
  it did not know the audit opinion was qualified on it, because it held no filings. Nothing
  in the valuation is changed by this — a qualification is a disclosure, not a remeasurement
  — but it is the single most important thing a reader of this name is entitled to know.

## 8 · MULTIPLE CROSS-CHECK

| | equity value (EGP mn) | on FY2025 net profit of 2,880.0mn |
|---|---:|---:|
| carrying-value branch, EGP 41.3484 | 44,884 | **15.6×** |
| round-price branch, EGP 52.3453 | 56,821 | **19.7×** |
| the traded price, EGP 28.98 | 31,458 | **10.9×** |

An Egyptian auto assembler at 15.6× would be rich, and at 19.7× very rich. **Neither is an
assembler multiple, and the arithmetic says why.** Take the operating businesses alone — the
auto leg at its cash-flow value of EGP 26,997.5mn and the lender at the residual-income value
of 1,655.7mn its own disclosed return supports — and they come to **EGP 28,653.2mn, or 9.95×
FY2025 group net profit**. That is a low multiple, not a high one. Every point of premium
over the traded price is the associate.

**THE REVERSE READ, AND IT IS HARSHER THAN THE FIRST PASS FOUND.** The traded price values
the whole company at EGP 31,457.8mn. This study's operating businesses are worth 28,653.2mn
of that — **91.1% of the entire market capitalisation, before a single pound of associate
value.** What is left for the associates is **EGP 2,804.6mn, or 2.58 per share**:

- against the June-2026 round read-through of 28,167.6mn, a discount of **90.0%**
- against the **reviewed carrying value** of 16,230.5mn, a discount of **82.7%**

The first pass of this review computed a 69.4% discount and called it *"the ordinary discount
a public market applies to an unlisted growth stake it cannot exit"* and *"a believable
number"*. **That conclusion does not survive the rebuild and it is withdrawn here rather than
quietly dropped.** Two changes moved it: the conglomerate discount that was suppressing the
whole sum came off, and the lender leg fell from a typed 9,500 to 1,655.7 — so the operating
side is now worth more of the market capitalisation and less is left over for the associate.
A discount of 90% to a private round is arguable. **A discount of 83% to a figure a reviewing
accountant has signed a balance sheet on is a different claim**, and it is the one the market
is making.

**SO THE GAP IS ONE LINE, AND THE STUDY SAYS WHICH.** Either the market is marking a stake
carried at EGP 14.95 per share at roughly EGP 2.58, or one of the two operating legs above is
worth materially less than this study says. **Both are live and this review does not resolve
them**, which is the honest state of it; what it does is stop the question being invisible.
The place to look if the second is true is the auto leg's terminal, which carries 84% of that
leg's enterprise value.

---

## Verdict

**The answer changed, and what changed it was not the price.** Four rule-driven corrections
were applied to this study in a declared order in the first pass (35.75 → 73.71 → 43.96 →
44.33, `rebuild_ledger.json`). This second pass applies a further set, and each one is a rule
that already bound rather than a lever anybody chose:

| what moved | the rule it serves |
|---|---|
| the four-lens weighted blend, retired | [R-LENS-03] — one class primary IS the central |
| the typed 10% conglomerate discount, removed | the promotion rule — a free parameter with no out-of-sample evidence |
| the lender at book × 1.0, replaced by residual income on its own operating equity | [R-LENS-03] — book is a floor and is never weighted |
| the associate marked one way, now marked two ways | depth-bar standard 8 — the contested judgement is published both ways, never averaged |
| the normalised-earnings lens, removed | the class row does not carry it — associate marks make these earnings unnormalisable |
| the relative multiple's three typed multiples, replaced by the company's own trailing median | [R-LENS-03] — a multiple comes from peers or own history |

**A CORRECTION TO THIS RUN'S OWN COMMIT MESSAGE.** The commit that made these changes says
the study "did not mention" the qualification on the associate. That is wrong and is recorded
here rather than left standing: the FY2025 qualification was already a registered input in
the study's own numbers file, dated 26 February 2026, and heading 7 of this review discusses
it at length. What was genuinely absent is the **30 June 2026** review qualification with its
own wording and its EGP 409.9mn figure, and the **42.93% from 44.01%** ownership pair the
reviewed statements state for the same transaction the press release states as 41.61% from
42.58%. Both are now in the record. The overstatement was mine and it is corrected where a
reader of this study will see it.

**What would overturn the whole thing:** an audited MNT-Halan financial statement, or any
subsequent round or transaction repricing the interest. On the round-price branch that line
is 50% of the answer; on the carrying-value branch, 36%.

**[R-GAP-02] does not hold this study** — that block is one-sided and fires only where a
branch sits BELOW the price, and every branch here sits above it. [R-GAP-02] clause three
holds it, as it holds every study in the book, until Phase 1 acceptance closes. Publishing
remains a separate, explicitly-requested step and nothing here asks for one.
