# GBCO — fundamental walk-forward training record

**Run:** 30-Aug-2026, branch `claude/gbco-fundamental-training-5pxqeq`. Nothing here is
published; no rating, target, or buy/sell language. This is the training record required
before the GBCO fundamental update is finalised. The du reference run named in the
training prompt is not present in this repository on any branch (verified against every
remote ref); the record follows the training prompt's own specification with the same
file naming (`gbco_panel.py`, `bottom_up.py`, `GBCO_IS_projected_vs_actual_all_origins.md`).

## 1. Data obtained

- **Span: 15 of 15 targeted fiscal years — FY2011–FY2025 — plus Q1-2026 and H1-2026.**
  The window stops at FY2011 only because 15 years was the target; the company's own
  archive continues to AR2007 and remains available.
- **Provenance: every company figure is tier A** (GB Corp's own IR site: audited
  consolidated FS for FY2020–FY2025 and the 2026 interims; annual reports embedding the
  audited statements for FY2011–FY2022; 4Q earnings releases for segment volumes).
  The hard gate (last 3 FY + current-year quarters from company documents) is satisfied:
  FY2023/24/25 audited FS (KPMG Hazem Hassan) + Q1-2026 and H1-2026 reviewed interim FS,
  all downloaded from ir.gb-corporation.com this session. Tier C appears only in the
  exogenous conditioning series (World Bank CPI and EGP/USD). Tier B: the statutory tax
  schedule. Every figure carries value/source/date/tier in `gbco_panel.json`; DERIVED
  values carry formulas (market series 2023–2025; PC-unit sums 2017–2018).
- Ten image-only PDFs (FY2022–FY2025 FS, ERs 4Q23–4Q25, AR2017/2023/2024, 2026 interims)
  were read visually page-by-page; text-layer documents were extracted by five parallel
  extraction passes with verbatim quote lines per figure. Identity assertions
  (rev−COGS=GP; NP splits; balance-sheet identity) run in `gbco_panel.py` and pass on all
  15 years. Source attempts (all successes; none failed) are logged in SWEEP_LOG.md.

## 2. Pre-registration adherence

`PREREGISTRATION.md` was committed (b8bef351) before the first scoring run. Deviations:
none of substance. Implementation notes: (i) the "residual" revenue line
(others + eliminations + non-modelled auto lines) is forecast under the non-volume-line
rule (own t3 CAGR, else π); (ii) segment starting gross margins are proxied by the group
margin because GB discloses no segment COGS in most years — gap flagged, per the
finest-sourced-level rule; (iii) composition lines are scored only inside their basis
windows (C1 2011-16, C2 2017-22, C3 2023-25 per BASIS_BREAKS.md B3/B4/B5), so no growth
rate or scored cell ever crosses a perimeter or re-cut.

## 3. Results (raw mechanical model; log errors; n = scored origin-cells)

| line | h | n | bias | MAE | 5–95% CI (block bootstrap) | skill vs freeze | skill vs trend | era signs |
|---|---|---|---|---|---|---|---|---|
| revenue | 1 | 10 | −0.04 | 0.23 | (−0.21, +0.08) | 0.00 | −0.08 | E1− E2+ E3− E4− |
| revenue | 3 | 8 | +0.08 | 0.34 | (−0.21, +0.34) | +0.26 | −0.03 | E1+ E2+ E3− |
| revenue | 5 | 6 | +0.42 | 0.49 | (+0.24, +0.50) | +0.25 | −0.32 | E1+ E2+ |
| net profit | 1 | 6* | −0.64 | 0.81 | (−0.86, −0.41) | +0.22 | +0.33 | E2− E3− E4− |
| net profit (ex one-offs) | 1 | 6* | −0.43 | — | — | — | — | — |
| net profit | 3 | 3* | +0.34 | 0.34 | thin | +0.56 | +0.84 | E2+ E3+ |

*NP cells where model and actual are both positive; loss years (FY16/17 actuals) and
model-negative cells are scored on the scaled-error branch in errors_by_line.csv.

**Driver record at h1** (errors_by_driver.csv): financing revenue is the most
forecastable driver (MAE 0.17, bias −16% — portfolio compounding consistently beats a
trailing CAGR); SG&A is tight (MAE 0.15, bias −6%, under-forecast at 9 of 10 origins —
the persistent bias the corrections stage caught); volumes are unbiased but wild
(m3w MAE 0.63 — the 3W import ban and COVID; cv MAE 0.50); capex over-forecast
(bias +25% — GB's capex is programme-driven, not revenue-ratio-driven); working-capital
days land within 0.36–0.50 MAE with mild negative bias.

**Macro vs company split** (macro_company_split.csv): swapping in realized CPI/FX/market
paths removes only ~8% of revenue h1 MAE and ~20% of NP h1 MAE — and at h3/h5 it makes
revenue WORSE (realized 2022–24 devaluations blow up the escalators). The long-horizon
misses are company-structure errors (volume collapses under import restrictions, the
MNT perimeter, frozen associates), not macro-path errors. Perfect macro foresight would
not have rescued the five-year forecasts.

**Named failure modes** (all visible in GBCO_IS_projected_vs_actual_all_origins.md):
1. *Escalator carryover at post-shock origins* — origin 2020 baked 2017–19 trailing
   π/d into 2020–24 paths: revenue ×2–4 over by h4–h5.
2. *Window-truncated freeze at re-cut origins* — origin 2024 (C3 era, 1-point PC
   history) froze PC revenue into a +91% nominal year: h1 revenue −61% log error.
3. *Frozen associates* — the rule "associates frozen at last actual" misses the
   ~EGP 0.9–1.0bn MNT-BV pickup entirely from pre-2023 origins.
4. *Finance-cost spiral* — when revenue over-forecasts, modelled WC needs inflate debt
   and interest compounds the NP miss (origin 2020 h4–h5 NP negative vs +3.1bn actual).
5. *One-offs* — FY22's 8.21bn deconsolidation gain and FY23's Algeria impairment are
   never forecastable; ex-one-off scoring (np_ex_oneoffs.csv) removes a third of the
   NP h1 bias (−0.64 → −0.43).

**Stated-parameter sensitivities** (sensitivities.csv; reported, never selected): revenue
is insensitive to all three stated parameters (MAE 0.228–0.230). NP is highly sensitive
to the GP-wedge pass-throughs: PASS_COST 0.5/0.75/1.0 → NP h1 MAE 0.57/0.81/1.46;
PASS_PRICE 0.25/0.5/0.75 → 1.07/0.81/0.57. The wedge (cost pass-through minus price
pass-through) is the single most consequential stated assumption in the method. Per the
promotion rule, the better-scoring variants are NOT adopted from this in-sample reading;
the finding is recorded for the book-wide program.

## 4. Corrections — proposed, tested, disposition

The expanding-window learner proposed 20 driver-origin corrections (corrections_test.json);
7 origins carried at least one. Outcomes on corrected origins: SG&A ×1.06–1.08 improved
4 of 6 origins; m3w ×0.88–0.94 mixed and correctly reset by the 3W-ban structural break;
fin_rev ±2% made a tight driver slightly worse; pc_u ×1.07 helped 2023, inert at
2024–25 (mode-dependent). Non-overlapping confirmation (revenue): h1 0.229→0.230 (flat),
h3 0.152→0.139 (better), h5 flat.

**Carry-in decision: NO correction enters the update's point drivers.** The
pre-registered rule requires a correction to pass here AND be consistent with the same
driver class across the market's book. This is the first run of this program in the
repo, so book-wide consistency is unverifiable — every correction is recorded as a
watch flag. Closest to qualifying: **SG&A under-forecast (+5.7% growth-factor
correction; sign-stable E1–E4, 9 resolved origins; majority improvement)** — blocked
solely on the book-consistency leg; it should be re-tested the moment a second EG name
runs this program. Watch flags (recorded, graded live at the next roll of this record):
SGA_UP_5PCT, M3W_TRAILING_OVER, CAPEX_RATIO_OVER, PCU_SHARE_UNDER, FIN_REV_UNDER_C3.

## 5. What carries into the current GBCO update

1. **Drivers**: raw pre-registered rules (no point corrections). The five failure modes
   above are the checklist the update's judgement layer must address explicitly —
   in particular: do not freeze PC revenue off a truncated C3 window (mode-2 failure);
   model the associates line explicitly (MNT-BV is ~EGP 1bn/yr and qualified — see B8);
   anchor capex on the disclosed programme (Sadat/Ain Sokhna), not a revenue ratio.
2. **Years 3–5 as ranges, not points** (per the training prompt §6), built from this
   record's empirical error quantiles (p10/p90 of resolved log errors):
   - revenue h3: point × [0.61 .. 1.40]; h4: × [0.38 .. 1.30]; h5: × [0.41 .. 1.12]
   - gross profit h4: × [0.81 .. 1.43] (h3 gp sample carries one −1.08 outlier cell:
     × [0.86 .. 2.94] as computed; state both, do not trim without a rule)
   - NP h3+: the positive-pair sample is too thin (n=3) for stable quantiles — build the
     NP range from the revenue/GP ranges plus the SG&A bias band (−11% median) and the
     finance-line spread, and say so in the update.
3. **Guidance ledger** (guidance_ledger.md): management market-direction calls missed
   both contractions; GB Capital operational guidance delivered or beat; Sadat landed
   about one-to-two quarters late. Use management volume guidance as a cross-check,
   never an anchor, at cycle turns.
4. **Driver Ledger**: entry appended (engine/Fundamental_Driver_Ledger.md).

## 6. Caveats, stated plainly

- **Single-name record.** Ten origins, six scoreable at h5; every aggregate here is one
  company's history. Corrections were watch-flagged largely for exactly this reason.
- **NP small-n.** Reported-NP h1 has only 6 positive-pair cells (loss years 2016–17 and
  model-negative cells sit in the scaled-error branch); NP h3+ quantiles are thin.
- **Derived market entries.** Egypt PC market 2023–2025 are DERIVED from company growth
  quotes (formulas in the panel); AMIC's own tables were not fetched independently.
- **Minor internal inconsistencies in company documents**, recorded in extraction
  oddities: AR2017's M3W volume sub-items don't sum to its printed total (79,169 vs
  84,427); AR2015 vs AR2017 chart M3W volumes differ ~0.6%; AR2016 prints a Q1-2017
  review report in place of the FY2016 audit page; ER 4Q25 prints FY24 CV volume 2,096
  vs 2,101 in ER 4Q24. None is material to the training conclusions.
- **Restatements are handled point-in-time** (originally-reported values scored;
  B2/B6 register the restated readings). FY2018 growth into FY2019 carries a 0.74%
  lease-restatement wobble by construction.
- **The associates line from FY2024 onward is management-recorded and auditor-qualified**
  (MNT-BV FS not provided — B8). H1-2026 figures are reviewed, not audited, and FY2025
  was restated (+2.88bn equity) in the H1-2026 interims after being reported.
- **Provisional inputs:** none — no estimated or interpolated figure entered the panel;
  gaps were left as gaps and the affected drivers scored at the coarser sourced level.
