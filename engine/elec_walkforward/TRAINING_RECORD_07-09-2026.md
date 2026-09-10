# ELEC — fundamental walk-forward [R-FCAL-01]: training record

**Electro Cable Egypt · EGX · 7 September 2026 · INTERNAL — never shown to a reader**

**Scope: SKIP.** *walk-forward not run — insufficient sourceable history (4 years).*
The decision, its three independent grounds and the design that was pre-registered
are in `PRE_REGISTRATION_07-09-2026.md`. **No error was computed, because there is
no origin to compute one at.**

This record exists for what the run found while the filings were open, which is
larger than the scope decision and points the other way from the reading this
study's own audit reached yesterday.

---

## 1 · What was obtained, and the arithmetic that admits it

Four filings, all audited by UHY United, all Arabic scans with **no text layer**
(`pdftotext` returns 3 characters across the 33 pages of the one complete file).
Three of the four are **truncated** at exactly 1 MiB, 5 MiB and 5 MiB with no
`%EOF` and no readable xref; they open at zero pages, and their page images were
recovered by scanning the raw bytes for JPEG streams. Every figure below was read
off the rendered pixels and **re-added against its own statement**.

| filing | basis | pages recovered | status |
|---|---|---:|---|
| FY2020 annual | consolidated | 7 | truncated — cash flow and all notes lost |
| FY2021 annual | standalone | 33 | **complete** |
| FY2022 annual | standalone | 17 | truncated |
| FY2023 annual | standalone | 24 | truncated — notes from 8 onward lost |

**Footing: 15 checks, 0 refusals.** Reproduced by `python3 filed_record.py`.

Three of those checks are cross-statement rather than within one page, and they
are the ones worth naming because a broken font map would not survive them:
FY2023 additions to fixed assets reconcile between the cash-flow statement and
note 3's own roll-forward; the depreciation charge reconciles between the cash-flow
statement, the roll-forward and its allocation across cost of sales, selling and
administrative expenses; and FY2021's closing cash of EGP 107,414,240 is FY2022's opening
cash **read out of a different filing**.

## 2 · The filed record

### Income statement, standalone (EGP)

| | FY2020 | FY2021 | FY2022 | FY2023 |
|---|---:|---:|---:|---:|
| revenue | 1,003,350,740 | 1,421,442,451 | 3,159,826,850 | 4,857,508,463 |
| gross profit | 59,145,112 | 114,195,232 | 357,111,928 | 941,242,764 |
| operating profit | 3,524,172 | 57,604,982 | 249,243,079 | 834,200,418 |
| net profit | 65,409,824 | 72,903,639 | 141,310,292 | 404,120,612 |
| D&A | 10,837,212 | 12,654,394 | 14,396,156 | 15,395,929 |
| **EBITDA** | **14,361,384** | **70,259,376** | **263,639,235** | **849,596,347** |
| **EBITDA margin** | **1.43%** | **4.94%** | **8.34%** | **17.49%** |

### Income statement, consolidated (EGP) — the basis the study models

| | FY2019 | FY2020 |
|---|---:|---:|
| revenue | 2,033,436,125 | 1,740,090,697 |
| gross profit | 387,984,958 | 211,697,261 |
| operating profit | 248,842,725 | 121,562,003 |
| net profit | 166,778,241 | 133,506,537 |
| **operating margin** | **12.24%** | **6.99%** |

D&A is not obtainable on the consolidated basis — the FY2020 consolidated
cash-flow statement sits past the truncation — so **the consolidated line is the
operating margin and is not directly comparable to an EBITDA margin.** On the
standalone accounts D&A runs 0.32% to 1.08% of revenue, so the consolidated EBITDA
margin would sit a little above the operating margin, not several times it.

## 3 · The correction — the audit's central claim does not survive the filings

`AUDIT_06-09-2026.md` states, and the gap review repeats, that
**"this company's own reconstructed filed record"** of terminal EBITDA margin is
**25.33% – 30.68%**, that the study forecasts 12.30%, and therefore that the study "forecasts
less than half of the lowest filed year".

**Those margins are not filed.** They are the study's own committed `hist_is`,
which is vendor data:

| | study `hist_is` | ratio to filed |
|---|---:|---:|
| FY2023 EBITDA margin | 30.68% | — |
| FY2024 EBITDA margin | 25.33% | no filing exists |
| FY2025 EBITDA margin | 26.54% | no filing exists |

Against the company's own audited FY2023 standalone accounts:

| FY2023 | study | filed standalone | study / filed |
|---|---:|---:|---:|
| revenue | 8,673,400,000 | 4,857,508,463 | **1.79x** |
| EBITDA | 2,661,036,381 | 849,596,347 | **3.13x** |
| D&A | 60,713,800 | 15,395,929 | **3.94x** |
| finance cost | 990,000,000 | 308,666,911 | **3.21x** |
| net profit | 1,248,000,000 | 404,120,612 | **3.09x** |

**Consolidation explains the revenue gap and does not explain the profit gap.**
At the one year that exists on both bases the group is **1.73x** the parent on
revenue and **2.04x** on net profit. The study's FY2023 revenue sits at 1.79x the
parent — squarely consistent with a consolidated figure — while its net profit sits
at 3.09x, half again beyond what the measured consolidation wedge delivers.

### What the filed margins actually are, and where the forecast sits in them

| | EBITDA margin |
|---|---:|
| FY2020 filed, standalone | 1.43% |
| FY2021 filed, standalone | 4.94% |
| FY2022 filed, standalone | 8.34% |
| FY2023 filed, standalone | 17.49% |
| **the study's terminal forecast** | **12.30%** |
| the price's reverse read, class primary | 27.17% |
| the price's reverse read, published blend | 28.34% |

**The forecast terminal margin of 12.30% sits INSIDE the company's own filed range
of 1.43% – 17.49%. It is not below the filed record; it is in the middle of it.**

**And the reverse read runs the other way from the audit's reading of it.** The
price needs 27-28%, which is **1.6 times** the highest EBITDA margin this company
has filed on the basis that can be checked, and roughly double the operating margin
of its last consolidated year. [R-GAP-02] is explicit that a reverse read landing on
a *believable* number is evidence against dissent — here it lands on a number the
filings do not support, which is evidence the other way, and yesterday's audit read
it as support because it was comparing the price against vendor figures rather than
against filings.

**This does not make the study right.** The study's 12.30% was not derived from
these accounts — it was justified in the delivered document against "the pre-windfall
2022 norm (about 12%)" for a year the model holds no income statement for, and the
filed FY2022 standalone EBITDA margin is 8.34%, not 12%. **A number can be inside the
right range for a reason that is not evidence, and that is what happened here.**

## 4 · Trap (i), demonstrated rather than asserted

[R-FCAL-01] warns that dividing the finance charge by a broader liabilities total
understates the borrowing rate by a multiple. ELEC's own accounts price it:

| | on the borrowings that bear it | on total liabilities | understated by |
|---|---:|---:|---:|
| FY2021 | **8.49%** | 4.48% | 4.01 points |
| FY2022 | **8.98%** | 5.88% | 3.09 points |
| FY2023 | **18.25%** | 14.10% | 4.15 points |

The broad-denominator column is not merely low — at 4.48% and 5.88% it sits **below the
Egyptian sovereign**, which [R-COC-01] refuses outright. The bearing-debt column
tracks the policy rate through the tightening, which is the control that says the
denominator is the right one.

## 5 · The useful life

**Route (1) failed.** The FY2023 policy note (page 13) discloses spans — buildings
10–50, machinery 4–25, vehicles 5–20, tools 5–20, computers 5, furniture 5–10 —
with no dominant class and no weighting. A range is not a life.

**Route (2), derived and labelled derived:** depreciable gross cost of
EGP 343,770,105 (total cost less land, which is not depreciated) over an annual charge of
EGP 14,246,581 gives **24.13 years**, with a prior-year control at 24.99.

The note also discloses EGP 93,877,527 of cost **fully depreciated and still in use** —
27.31% of the depreciable base. Those assets carry cost and no charge, so they lengthen
the ratio; removing them gives **17.54 years**. Both ends sit inside the union of the
disclosed spans, so **the band 17.54–24.13 is what is recorded** and no point inside it
is chosen — that choice is the one route (1) failed for.

## 6 · What was NOT done, and why

**The study was not rebuilt and `fair{bear,base,full}` did not move.**

Two levers were priced by the audit and both were left unapplied:

| lever | rule | direction | why it was not applied |
|---|---|---|---|
| retire the typed four-lens blend, take the class primary | [R-LENS-03] | **down**, 0.3357 to −1.8082 a share | it would rebuild the answer on a panel this run has just shown cannot be reconciled to any document the company has issued |
| re-anchor the terminal margin to the filed record | [R-ANCHOR-01] | the audit said **up** | **the premise is withdrawn.** The forecast is inside the filed range, not below it, so there is no anchoring defect of the kind claimed |

**No rebuild ledger is written, because no rebuild happened.**
`engine/rebuild_ledger.py` refuses a ledger with no lever in it — *"a rebuild that
changed nothing is not a rebuild"* — and writing one with a lever nobody applied
would be the opposite of what that module is for. The two priced-and-declined
levers are recorded here instead, which serves the same purpose the ledger serves:
what it forbids is the move being invisible, and a move that was considered and
refused is recorded with its reason.

**The fair-value register records a movement of about -1.3% on the base and it is
NOT a change in the answer.** The frozen baseline was read from `assets/data.js`,
which carries the fair value at two decimal places (0.34); this edition records the
study's OWN committed figures (0.3357186228503667), which are what it has always
published. The register compares the two and the difference is the rounding in
`data.js`. **No lever was applied and no number was recomputed.**

**The gap is not closed and is not claimed to be.** The published central of
EGP 0.3357 against EGP 2.08 as at 2026-09-03 (SUPPLIED_03-09-2026.json) is -83.86%. This run does not move it toward
the price and does not defend it — it establishes that **the base the number is
built on cannot be verified against anything the issuer has published**, which is a
SIGCM clause 1 condition rather than a disagreement with the market.

## 7 · Caveats, stated plainly

- **Four sourceable fiscal years, standalone; two consolidated.** The window stops
  at FY2023 because the issuer's own index ends at 30 September 2025 and serves
  nothing after August 2020.
- **Everything here is the parent entity.** It is not the group, and it must never
  be substituted into the study's consolidated panel. The wedge is measured, and it
  is unstable down the statement (1.73x on revenue, 34.49x on operating profit).
- **Three of four filings are truncated**, so the FY2023 capital note, the FY2020
  consolidated cash-flow statement and the FY2022 notes are unread and recorded as
  unread rather than worked around.
- **No forecast was scored**, so this run contributes no cell to any pooled
  driver-bias census and no evidence for or against any correction.

