# GBCO — GAP REVIEW [R-GAP-01]

**7 September 2026.** Written because the rebuilt central sits more than 10% from the latest
known price. The trigger is two-sided since 02-Sep-2026, and this one fires on the UPPER
side, which is the side that gets no automatic hold and therefore needs this review most.

- AUDITED CENTRAL: 44.3295  (EGP per share)
- AUDITED SPOT: **EGP 28.98**, the supplied close of **3 September 2026** — the latest price this repository holds
- AUDITED GAP: +53.0%

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

At EGP 44.3295 the equity value is **EGP 48,121mn**. Against FY2025 net profit of 2,880.0mn
that is **16.7×**; against 1H2026 annualised (2,524.0mn) **19.1×**. The traded price implies
**10.9×** and **12.5×** on the same two. An Egyptian auto assembler at 16.7× would be rich.

**It is not an assembler multiple, and the arithmetic says so.** Strip the associates at the
study's own 10% complexity discount and the operating business is valued at EGP 48,001 −
0.9 × 28,060.7 = **22,866mn**, or **7.9×** FY2025 group net profit and **3.4×** FY2025 group
operating profit — a low multiple, not a high one. The whole of the premium over the traded
price is the private mark on MNT-Halan and how far a reader believes it.

**THE REVERSE READ.** The traded price of EGP 28.98 values the whole company at EGP
31,458.2mn. Holding this study's operating value of 22,866mn, the market is paying **EGP
8,592mn for the associates** — a 69.4% discount to the 27,670.7mn read-through, i.e. the
market is marking GB Corp's MNT-Halan stake at roughly **USD 434mn against the USD 583mn the
June 2026 round implies**. That is not an absurd belief. It is the ordinary discount a public
market applies to an unlisted growth stake it cannot exit, and it is a **believable number** —
which under [R-GAP-02]'s own standard is evidence AGAINST dissenting from the market, not for
it.

---

## Verdict

**The answer is not changed by this review, and the answer is not the interesting part.**
Four rule-driven corrections were applied in a declared order and the value moved 35.75 →
73.71 → 43.96 → 44.33 (`rebuild_ledger.json`); two of the four pull in opposite directions
and the running total is a contest rather than a landslide. The +53.0% premium is **almost
entirely one line** — an unlisted associate marked at a private round price, on which the
company's own auditors have issued a **qualified opinion**, and against which the market is
applying a discount this review finds believable.

**What would overturn it:** an audited MNT-Halan financial statement, or any subsequent round
or transaction repricing the stake. Both would move 58% of this valuation.

**[R-GAP-02] does not hold this study** — that block is one-sided and fires only where the
central sits BELOW the price. Publishing remains a separate, explicitly-requested step and
nothing here asks for one.
