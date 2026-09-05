# STC — the rebuild plan, declared before any lever is touched

**5 September 2026.** [R-REBUILD-01] requires the audit point to be declared in
advance and the lever order fixed before the work. The LEDGER itself (`rebuild_ledger.json`)
is created when the first lever lands, because that gate refuses a ledger carrying no
lever — a rebuild that changed nothing is not a rebuild. This file is the plan; the
ledger will be walked against it.

## Where it starts

| | |
|---|---:|
| published central (the four-lens blend) | **SAR 47.1108** |
| the spot it was struck at, 9 July 2026 | 43.58 |
| gap at strike | +8.1% |
| latest known close, 3 September 2026 | 43.86 |
| gap against the latest price | +7.4% |

## The audit point

AFTER LEVER 3, AND THE REASON IS THAT LEVERS 2 AND 3 PULL IN OPPOSITE DIRECTIONS. This is the shape [R-REBUILD-01] exists for: read as a list of corrections a rebuild of seven levers is a landslide, and read as the rules they serve it is a contest. DECLARED BEFORE ANY LEVER IS TOUCHED. Normalising the risk-free by Saudi Arabia's own sovereign default spread ([R-COC-01], lever 2) takes it from a raw 5.50% to 4.99% on the rating basis or 4.52% on the CDS basis, which LOWERS the cost of capital and RAISES the value. Re-deriving the beta through own_stock_beta ([R-BETA-04], lever 3) replaces the 0.48 this study actually uses — from a nine-week DAILY regression the rule states is not a tier — with a conforming 0.71 from 252 weekly points over 4.91 years, which the study's own beta record prices at +1.156pp on the cost of equity on the rating basis and +1.320pp on the CDS basis, and which LOWERS the value. THE SIZE IS KNOWN IN ADVANCE ONLY FOR THE LENS LEVER AND IT IS STATED HERE RATHER THAN DISCOVERED: retiring the four-lens blend under [R-LENS-03] moves the central from 47.1108 to the cash-flow lens's 50.1165, and against the latest known close of SAR 43.86 on 3 September that carries the gap from +7.4% to +14.3% — from inside [R-GAP-01]'s band to outside it, owing the eight-heading review, and NOT held by [R-GAP-02], whose block is one-sided and below. A LOOK TAKEN BEFORE LEVER 3 WOULD AUDIT A STATE THIS STUDY NEVER PUBLISHES — a normalised risk-free on a beta the rule refuses — which is why the audit point is after the pair rather than between them.

## THE AUDIT, TAKEN — 5 September 2026, after lever 3, exactly where it was declared

| | |
|---|---:|
| published central, the four-lens blend | SAR 47.1108 |
| after [R-COC-01] — the sanctioned schedule, on the RETIRED beta held fixed | **51.0714** (+8.41%) |
| after [R-BETA-04] — the conforming own-stock weekly beta | **44.0502** (−13.75%) |
| net across both | **−6.50%** |
| against the latest known close of SAR 43.86, 3 September 2026 | **+0.43%** |

**The two levers disagreed, and the route is why that matters.** Taken in the order fixed
in writing before either was touched, the cost-of-capital correction moved the answer AWAY
from the market — from 8.1% above the price it was struck at to 16.4% above the latest one —
and the beta correction brought it back. Neither was chosen for where it landed and neither
could have been: the first raises every value it touches and the second lowers every value
it touches, and which of them dominates is arithmetic about this company's own capital
structure. Read as one net figure of −6.5% this is a small tidy-up; read as its two levers
it is an 8.4% and a 13.8% pulling against each other, and that is the decomposition
[R-REBUILD-01] exists to keep visible.

**The answer now sits essentially on the price, and that is an observation rather than
corroboration.** Four levers remain and the lens retirement is one of them. A rebuild that
stopped here because the number looked comfortable would be fitting to the price by choosing
when to stop, which is the same offence as moving a driver to meet one.

**The two levers could not in fact be separated in the model, only in measurement, and that
is recorded rather than glossed.** `cost_of_capital.schedule()` REFUSES to build on a tier-1
beta recorded as non-conforming, and the beta this study carried is a 40-session daily
regression the standing rule says is not one of the three tiers at all — so there is no state
of this study in which the schedule rule is satisfied and the beta rule is not. The
intermediate above is produced through the module's own sensitivity path, on a beta declared
as a sensitivity and never as this study's beta, and it writes `beta_sensitivity.json` and
nothing else. The ledger reads that artefact; no figure in it was copied from a terminal.

## After the audit

| lever | rule | before | after | move |
|---|---|---:|---:|---:|
| 4 | R-MACRO-01 | 44.0502 | **41.7388** | −5.25% |
| 5 | R-TERM-01 | 41.7388 | **40.4206** | −3.16% |
| 5b | R-BRIDGE-01 | 40.4206 | **41.8568** | +3.55% |
| 6 | R-LENS-03 | 41.8568 | **41.1548** | −1.68% |
| 7 | R-GAP-01 | 41.1548 | **41.1548** | +0.00% |

Cumulative **−12.64%** from the delivered 47.1108, and **−6.17%** against the latest known
close of SAR 43.86 — inside the ten per cent band either way, so no eight-heading review is
owed and the publication block does not fire on the gap. **All seven levers are landed.**

**Worth more than the plan expected, and the reason is the lens that was about to be
retired anyway.** The plan judged this "likely to change what a reader can see rather than
the number", which is right about a pegged market's cash-flow lens — the terminal falls from
a typed 2.5% to a derived 2.0% and the discounted-cash-flow read moves 45.24 to 42.23. What
the plan did not anticipate is that the study carried a SECOND terminal growth rate, 3.0%,
inside its dividend lens: two answers to one question about one economy, in one model, on
one company. A discounted-dividend terminal is the most convex thing in this model to its
own growth rate, so that read falls 40.47 to 35.43 — and it carried a quarter of the blend.

**Neither number was defended anywhere.** Both were typed, and a typed nominal rate is
unfalsifiable: nobody reading the page can tell whether 2.5% meant terminal inflation plus
half a point or something else. Both now sit on the house Saudi path as (real, path id) at
the rule's own stated default of zero real growth. Reverse-engineering the real rate that
reproduces the typed 2.5% would have kept the number and invented a reason for it.

**The [R-MACRO-01] RECORD is not yet written and STC stays on that ratchet, deliberately.**
The rule binds every growth rate in the model, and the four segment growth arrays — `g_cbu`,
`g_ebu`, `g_wc`, `g_sub` — are typed nominals with no source, date or layer, whose implied
real growth wanders from 0.68% to 0.00% across five years with nothing saying why. They
cannot be expressed as (real, path) without choosing a real rate, and choosing one to clear
a checker is the offence this protocol names in three separate places. **The honest fix is
the ground-up rebuild on the eleven disclosed segments** the FY2025 filing carries with two
years of revenue AND gross profit each, which [R-SIGCM-02] requires anyway and which the
section below already names. Until then a partial macro record would be worse than none: the
ratchet allows a listed study to carry no record and breaks on one that has appeared and is
wrong.

### Lever 5, and the direction was not predicted

The retired terminal charged g × IC every year for ever, which reads as a capital
maintenance programme with a replacement cycle of 1/g — a fact about the currency and not
about the asset. At a pegged 2% terminal that is **fifty years**, against a base whose own
accounts run twenty-one. The same construction never added book depreciation back although
the operating profit it starts from is already net of it, so one model carried two
definitions of free cash flow with the terminal holding three quarters of the value.

The life is **20.86 years** and the base is **15.23 years old**, both DERIVED from note 10's
own roll-forward by the identity this protocol already sanctions, because the company
discloses ranges rather than one life. All three conditions that break that identity were
checked on the policy note first and all three are clear. The terminal is smaller on this
name; on the last name rebuilt it was about 5% larger, which is why [R-TERM-01 CLAUSE TWO
CORRECTED] forbids predicting the sign before running it.

**A filename, and it was worth more than it looks.** This study called its numbers file
`stc_study_numbers.json` where twenty-one of twenty-four call it `study_numbers.json`. Most
gates glob for it; the terminal census resolved the name literally and reported the study
"no committed numbers file" — an ABSENT answer wearing a clean one's costume, and worse than
a failure because a study reported unreadable is one nobody looks at again. The file is
renamed to the house name and the census now globs like everything else, which also recovers
the two other studies that name theirs differently.

### Lever 5b, and the largest line was not stale but wrong by more than half

The bridge stood on a first-quarter net-debt figure and a 31 March 2026 minority while a
reviewed 30 June 2026 balance sheet was already published — in the same document set this
rebuild had just read to source the debt book. That is the stale-sheet defect [R-BRIDGE-01]
was written for, and it is the smaller half of what was found.

**Associates and joint ventures were carried at SAR 4,641mn against a filed 12,909.648mn.**
That is a figure from before February 2025, when the group contributed the whole of its
towers business to DIIC in exchange for 43.06% of it. **The towers business the entire 2024
restatement was about had left the subsidiaries and arrived in the associates, and the
bridge had followed it into neither** — the same event, missed twice, from opposite sides.

Three more lines moved on the same sheet. The listed equity investment is taken at the fair
value the company itself discloses (8,513.430, Level 1, note 9.1) rather than at a mark
typed here; the investment funds it holds at fair value were omitted altogether; and the
minority now comes out at its SHARE OF EQUITY VALUE — its own disclosed 2.021% of profit,
note 25 — rather than at historical cost, because the model capitalises 100% of subsidiary
cash flow. The share count is footed against par at 4,993.024mn.

**One thing is deliberately absent and the direction is stated.** STC Bank's cash and its
digital-banking financial assets are excluded from net debt, because netting a bank's cash
against group borrowings treats money that backs customer balances as though it were free.
The cost is that the bank's own equity value appears in this bridge nowhere. That
understates the answer, it is left as a gap rather than filled with a number nothing
supports, and the same is true of the market cross-check on BGSM's look-through into a
listed Malaysian operator, whose price this desk does not hold.

### Lever 6, and the multiple was the traded one wearing a different hat

The delivered central was a blend of four lenses at typed weights — 35% cash flow, 25%
dividend discount, 20% relative multiple, 20% normalised earnings — that nobody chose on
evidence and no out-of-sample test ever cleared. **Two of the four are not permitted
cross-checks for a telecom operator at all, and they carried 45% of the answer between
them.** The registry gives this class a cash-flow primary cross-checked on an EV/EBITDA
multiple from its own history and on book value, so the cash-flow read IS the central.

**The multiple is now computed rather than typed, and the old one was circular.** The study
used 8.0 / 9.0 / 10.0 with no source of any kind, and its base of 9.0 sat within a rounding
of the **9.151x** the shares trade at today — which values the company at what it already
trades at. The adopted **8.762x** is the mean of this company's own trailing EV/EBITDA at
the last three year ends (9.131x, 8.316x, 8.839x), each computed from that year-end's own
close in the persistent price library, the shares in issue and that year's own net debt and
EBITDA from the filings. Every one of the three sits BELOW the traded multiple, so the lens
can be *seen* not to be anchored on the price rather than merely asserted not to be.

**The bear and bull are flexed in observable units with the macro path standing still.** The
delivered corners moved the cost of capital by 100 and 70 basis points AND terminal growth
between 2.0% and 3.0% AND the margin AND capex, all at once — and since terminal growth and
the terminal risk-free rate are derived from one house path carrying one terminal inflation,
each corner was an economy nothing describes and the width was chosen rather than observed.
What moves now is capital intensity, between the 15.0% and 17.5% of revenue management
guides to. The published envelope is then the RANGE of the present-value reads on one clock,
40.48 to 48.52, which stretches to what the cross-check says rather than to a spread
invented around the answer; book value of 17.02 is the disclosed floor and is never weighted.

### Lever 7, whose move is zero, and that is the finding

[R-GAP-01] wants the central put against the latest known price before any delivery, and
the valuation has been struck on that price since lever 2, because the cost-of-capital
schedule reads the supplied close register directly. **There was nothing left to re-strike.**

What was missing is that neither the answer nor the price appeared anywhere a reader or a
checker could find them. The study exposed no central at all, so every gate that audits an
ANSWER rather than a step reported it unreadable — and an unreadable study is not a clean
one, it is the cheapest possible route past an audit. Both are now at the top level of the
committed record, and the valuation-gap ratchet carries no breaching study at all.

**Two clocks are named rather than conflated.** The valuation is struck against the latest
known close of SAR 43.86 on 3 September 2026; the Monte Carlo cone is struck against SAR
44.72 on 31 August, the last session in the persistent price library, because a cone has to
start where its own price series ends. Publishing one number for both would either strike
the cone on a session that is not in its series or measure the gap against a price the
market has already left.

## What is left, and it is not small

The seven levers are done and **this is not a delivered study.** It has no bibliography, no
inputs register with four fields, no sweep register, no QC gate, no driver test and no
recalculation harness, and its four segment growth arrays are still typed nominals with no
source, date or layer — which is why [R-MACRO-01]'s record is still unwritten and STC stays
on that one ratchet. The eleven disclosed segments in the FY2025 filing, with two years of
revenue and gross profit each, are the base a ground-up rebuild builds on, and they were not
available to this study before 5 September.

## The levers, in order

| # | rule | what |
|---|---|---|
| 1 ✅ | mechanical | import mc_v2 -> primitives (a pure rename, the module was renamed 2 August 2026) and the price history taken from the persistent library engine/raw_ohlc/SA/STC.csv, which this study never committed. BOTH TESTED IN A SCRATCH COPY: the import resolves and the file is in the same vendor format. Neither is a valuation decision, though the library re-strikes the study from 9 July to 31 August 2026 at SAR 44.72, which [R-GAP-01] wants anyway. |
| 2 ✅ | R-COC-01 | the cost-of-capital schedule through engine/cost_of_capital.py on the house Saudi path, FLAT because the market is pegged and stated as such rather than left as an absence. rf* = 5.50% less Saudi Arabia's own default spread (rating 0.51%, market 0.98%). RAISES the value. |
| 3 ✅ | R-BETA-04 | the beta re-derived live through beta_regression.own_stock_beta('STC','SA','TADAWUL') and attested. LOWERS the value. Do not carry either recorded figure forward — the committed 0.7107 and tonight's 0.7078 differ only because the library lengthened. |
| AUDIT ✅ | R-REBUILD-01 | STOP AND LOOK. Levers 2 and 3 pull opposite ways and the net is not predicted here. |
| 4 ✅ | R-MACRO-01 | terminal growth stored as (real, inflation-path id) rather than the typed nominal 2.5%. Against a Saudi terminal inflation of 2.00% that is +0.5% real; on a pegged market this is likely to change what a reader can see rather than the number ([L-319]). |
| 5 ✅ | R-TERM-01 | the terminal through engine/terminal_value.py on the DERIVED life in TERMINAL_EVIDENCE_05-09-2026.md — 20.86 years, base 15.23 years old, 73% of the depreciable base written off, on three filed years that each foot to the riyal. THE BASE IS OLD, at 1.46 times half its own implied life, so maintenance at current cost is a large multiple of the book charge. THE SIGN IS NOT PREDICTED [R-TERM-01 CLAUSE TWO CORRECTED]. |
| 5b ✅ | R-BRIDGE-01 | **ADDED 5 September 2026, and the timing is recorded because it is the whole question.** The bridge stands on figures the company has since superseded: the study deducts net debt of SAR 7,063mn on a Q1-2026 basis and a minority of SAR 2,335mn at 31 March 2026, while a REVIEWED 30 June 2026 balance sheet was published carrying borrowings of SAR 23,536.554mn, cash of SAR 18,940.773mn and a minority of SAR 2,726.349mn. It also divides by 4,989.8mn shares, which is the 31 December 2025 count; note 17 of that same interim foots issued capital of SAR 50,000,000 thousand at SAR 10 par to 5,000,000 thousand shares and states 4,993.024mn outstanding. THIS WAS FOUND WHILE SOURCING THE DEBT BOOK FOR LEVER 2 AND BEFORE THE MODEL PRODUCED ANY REBUILT ANSWER — the plan is amended at a point where nobody could yet know which way it moves the value, which is the only condition under which adding a lever is not reshaping the route to suit where it lands. |
| 6 ✅ | R-LENS-03 | the four-lens blend retired. LENS_REGISTRY['telecom operator'] is a cash-flow primary cross-checked on own-history EV/EBITDA, a relative multiple and book — so the dividend-discount and normalised-earnings reads come OUT of the answer entirely. STC is the ONE of the seven unreadable studies whose class the registry holds. |
| 7 ✅ | R-GAP-01 | re-struck on the latest known price, and the eight-heading review written before any file is staged. |

## What this rebuild also needs, and the ledger does not measure

this study has never had a bibliography, an inputs register with four fields, a sweep register, a QC gate, a driver test or a recalculation harness. Its drivers are typed arrays with no source, date or layer. The five audited and reviewed statement sets now in src/ are the material a proper register is built from, and they were not there before 5 September.

## Why the plan is committed first

PLAN COMMITTED BEFORE THE WORK, and this file is rewritten with the levers as they land. What is fixed here and may not move afterwards: the levers, their order, and the audit point. [R-REBUILD-01] exists because six individually-required corrections were once stacked on one name without anybody looking at the running total until the last one was in — and that name passed through +45% on its way to -56%.
