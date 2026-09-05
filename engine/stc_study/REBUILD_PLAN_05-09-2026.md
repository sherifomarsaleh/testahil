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

## The levers, in order

| # | rule | what |
|---|---|---|
| 1 | mechanical | import mc_v2 -> primitives (a pure rename, the module was renamed 2 August 2026) and the price history taken from the persistent library engine/raw_ohlc/SA/STC.csv, which this study never committed. BOTH TESTED IN A SCRATCH COPY: the import resolves and the file is in the same vendor format. Neither is a valuation decision, though the library re-strikes the study from 9 July to 31 August 2026 at SAR 44.72, which [R-GAP-01] wants anyway. |
| 2 | R-COC-01 | the cost-of-capital schedule through engine/cost_of_capital.py on the house Saudi path, FLAT because the market is pegged and stated as such rather than left as an absence. rf* = 5.50% less Saudi Arabia's own default spread (rating 0.51%, market 0.98%). RAISES the value. |
| 3 | R-BETA-04 | the beta re-derived live through beta_regression.own_stock_beta('STC','SA','TADAWUL') and attested. LOWERS the value. Do not carry either recorded figure forward — the committed 0.7107 and tonight's 0.7078 differ only because the library lengthened. |
| AUDIT | R-REBUILD-01 | STOP AND LOOK. Levers 2 and 3 pull opposite ways and the net is not predicted here. |
| 4 | R-MACRO-01 | terminal growth stored as (real, inflation-path id) rather than the typed nominal 2.5%. Against a Saudi terminal inflation of 2.00% that is +0.5% real; on a pegged market this is likely to change what a reader can see rather than the number ([L-319]). |
| 5 | R-TERM-01 | the terminal through engine/terminal_value.py on the DERIVED life in TERMINAL_EVIDENCE_05-09-2026.md — 20.86 years, base 15.23 years old, 73% of the depreciable base written off, on three filed years that each foot to the riyal. THE BASE IS OLD, at 1.46 times half its own implied life, so maintenance at current cost is a large multiple of the book charge. THE SIGN IS NOT PREDICTED [R-TERM-01 CLAUSE TWO CORRECTED]. |
| 6 | R-LENS-03 | the four-lens blend retired. LENS_REGISTRY['telecom operator'] is a cash-flow primary cross-checked on own-history EV/EBITDA, a relative multiple and book — so the dividend-discount and normalised-earnings reads come OUT of the answer entirely. STC is the ONE of the seven unreadable studies whose class the registry holds. |
| 7 | R-GAP-01 | re-struck on the latest known price, and the eight-heading review written before any file is staged. |

## What this rebuild also needs, and the ledger does not measure

this study has never had a bibliography, an inputs register with four fields, a sweep register, a QC gate, a driver test or a recalculation harness. Its drivers are typed arrays with no source, date or layer. The five audited and reviewed statement sets now in src/ are the material a proper register is built from, and they were not there before 5 September.

## Why the plan is committed first

PLAN COMMITTED BEFORE THE WORK, and this file is rewritten with the levers as they land. What is fixed here and may not move afterwards: the levers, their order, and the audit point. [R-REBUILD-01] exists because six individually-required corrections were once stacked on one name without anybody looking at the running total until the last one was in — and that name passed through +45% on its way to -56%.
