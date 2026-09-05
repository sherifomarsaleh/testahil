# STC — everything this rebuild needs, measured, and the blocker that was already closed

**5 September 2026.** STC is the ONE of the seven studies invisible to the valuation-gap
gate whose class — telecom operator — is in `research_protocol.LENS_REGISTRY`, so its lens
architecture can be corrected without waiting on the taxonomy escalation. This file records
what was measured tonight so the rebuild does not re-derive it.

## 1. The recorded blocker is closed, and it was closed three days ago

`beta_result.json` carries:

> `wacc_reissue_blocked_on`: *"Saudi Arabia's own sovereign default spread, rating basis and
> CDS basis, read fresh from Damodaran's original ctryprem.html. Not reconstructed from
> memory: stop and inform."*

`engine/macro_paths/SA.json` carries both — **rating 0.51%, market 0.98%** — sourced and
dated, since [R-MACRO-01] on 2 September. GBCO's `beta_result.json` carries the identical
field for Egypt and is closed the same way. Those two are the whole population: a sweep of
every JSON in every study directory for a field naming a blocker returns exactly two, and
both were answered by a rule adopted three days before anyone looked. Registered as [L-339].

## 2. The file runs after two changes, neither of which is a valuation decision

Both were tested in a scratch copy rather than asserted.

- `import mc_v2 as m` → `import primitives as m`. A pure rename (the module was renamed on
  2 August 2026) and the import then resolves.
- `STC_Stock_Price_History.csv` is not in this directory and never was — the study's own
  price history was never committed. `engine/raw_ohlc/SA/STC.csv` is the persistent library
  and carries the same vendor format; it runs to **31 August 2026 at SAR 44.72** against the
  study's strike of 9 July 2026. Pointing at the library re-strikes the study, which the
  rebuild wants anyway under [R-GAP-01]'s latest-price rule.

## 3. Then it stops at the same line GBCO does, and that one IS a valuation decision

`stc_compute.py:181` passes `rf=0.055` to a `WaccInputs` that has taken `rf_observed` since
the v2 method. Renaming the argument is not the fix and would be worse than leaving it
broken: `sov_default_spread_rating` and `sov_default_spread_cds` default to zero, so the
call would run, reproduce today's figures exactly, and go on committing the v1 double-count —
the raw local yield PLUS a country-risk-loaded equity premium.

| | as committed | v2, rating basis | v2, CDS basis |
|---|---:|---:|---:|
| risk-free used | 5.50% | 4.99% | 4.52% |
| the arithmetic | raw derived SAR 10-year | 5.50 − 0.51 | 5.50 − 0.98 |

## 4. The beta is already re-derived, attested, and is NOT what the study uses

`beta_result.json` records a conforming tier-1 regression — **0.7107**, R² 0.302, SE 0.103,
n=254 weekly over 4.94 years against `raw_indices/SA/TASI.csv` — beside
`superseded_beta 0.48` from *"a daily short-window stopgap, which the rule states is not a
tier"* (n=40 paired sessions over nine weeks). **The delivered study runs on 0.48.** The
record prices the correction itself: **+1.156pp on the cost of equity on the rating basis,
+1.320pp on the CDS basis.**

Re-run tonight through `beta_regression.own_stock_beta('STC','SA','TADAWUL')` the number is
**0.7078** (R² 0.302, SE 0.103, n=252, 4.91 years, last observation 13 August 2026) — the
same regression on a library three weeks longer. Use the live call at rebuild time; do not
carry either figure forward from here.

**This correction runs the OTHER WAY from the risk-free one**: a higher beta raises the cost
of equity and lowers the value, while normalising the risk-free lowers it and raises the
value. Neither is chosen for its direction and the net is not predicted here.

## 5. The terminal, which is derivable and was derived tonight

`engine/stc_study/TERMINAL_EVIDENCE_05-09-2026.md` has the full working. In short: all three
of [L-328]'s conditions are clear — the charge is cost over life with no residual deducted,
there is no quantified change in estimate, and the acquired base is 0.007% of cost — so the
identity works, and it is the first name in five where it does.

**Implied life 20.86 years, measured age 15.23 years, 73.0% of the depreciable base written
off**, on three filed years that each foot to the riyal. The base is OLD, at 1.46 times half
its own implied life, so maintenance at current cost is a large multiple of the book charge.
`terminal_value.build()` takes those; nothing here chooses a life.

## 6. Growth and the schedule

Terminal growth is a **typed nominal 2.5%** against an SA terminal inflation of 2.00%, i.e.
a real +0.5%. [R-MACRO-01] requires it stored as (real, inflation-path id) and recomputed;
on a pegged market that is likely to change what a reader can see rather than the number
([L-319]). SA is **pegged**, so [R-COC-01] returns a FLAT schedule and says so — there is no
glide to build here, and that must be stated rather than left as an absence.

## 7. The lens, which is the reason this name can move at all

Committed: a four-lens weighted blend — dcf 0.35, ddm 0.25, relative 0.20, normalised 0.20 —
giving 50.1165 / 45.8784 / 47.2140 / 43.2883 and a central of **47.1108**.

`LENS_REGISTRY['telecom operator']` is `('dcf', ('ev_ebitda_own_history',
'relative_multiple', 'book_value'))`. So the cash-flow lens IS the central; the relative
multiple stays as a cross-check; **the dividend-discount and normalised-earnings reads come
out of the answer entirely** — a discounted dividend model is the bank row's primary and
normalised earnings appears in no row of the registry at all.

The consequence is worth stating in advance so it is not discovered afterwards: on the
committed figures the central moves from 47.1108 to 50.1165, and against the latest known
close of **SAR 43.86 (3 September 2026)** the gap moves from **+7.4%** to **+14.3%** — from
inside [R-GAP-01]'s band to outside it. That owes the eight-heading review before delivery.
It does NOT trigger [R-GAP-02], whose block is one-sided and below.

## 8. What is still missing, and it is not small

No bibliography document, no inputs register with four fields, no sweep register, no QC gate,
no driver test, no recalculation harness — the delivered study was recovered from project
files on 8 August 2026 and its build scripts were never written to produce any of them. Its
drivers are typed arrays with no source, date or layer. The five sets of audited statements
in `src/` are the material a proper register is built from, and they were not there before
tonight.

## 9. The order, declared here so it is not chosen afterwards

1. the two mechanical unblocks in section 2, which move no number by decision;
2. the cost-of-capital schedule through `engine/cost_of_capital.py` on the house SA path,
   flat because the market is pegged ([R-COC-01]);
3. the beta re-derived live through `own_stock_beta` ([R-BETA-04]) — which pulls the other
   way from (2);
4. growth stored as a real rate on that path ([R-MACRO-01]);
5. the terminal through `engine/terminal_value.py` on the derived life ([R-TERM-01]);
6. the lens architecture ([R-LENS-03]) — available, unlike every other blocked name;
7. the re-strike on the latest known price and the eight-heading review ([R-GAP-01]).

A rebuild ledger [R-REBUILD-01] carries all seven with the audit point declared before the
first is applied. **Two of them pull in opposite directions** and that is exactly the case
the ledger exists for: read as seven corrections it is a landslide, read as the rules they
serve it is a contest.
