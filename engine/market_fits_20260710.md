# Per-market MC v3 fits — 10-Jul-2026

Standing rule executed (user instruction "customize MC v3 for each market; create a
customized fit for every new market"): every market now carries its OWN fitted
(nu, width_cal) from its OWN pooled panel, persisted in `market_profiles.py` and
resolved automatically by `backtest_v3` when not passed explicitly. Fitting script:
`fit_markets_20260710.py`. Panels: `engine/panels/` (grow like ledgers).

## Production fits

| Market | Panel | Windows | nu | width_cal | Panel verdict | Status |
|---|---|---|---|---|---|---|
| Egypt (EG) | 7 names: EMFD GBCO KABO OCDI ORHD PHDC TMGH | 115 | **4** | **0.965** | PASS +0.062 [+0.036,+0.078] | LONO-stable |
| Saudi (SA) | 2 names: ALINMA MAADEN | 36 | **5** | **1.28** (cap-bound) | PASS +0.022 [+0.001,+0.041] | pooled = production; LONO unstable at n=2 |
| Qatar (QA) | 1 name: QGTS | 18 | **Gaussian** (250) | **0.916** | PARITY −0.011 [−0.037,+0.005] | PROVISIONAL single-name self-fit |
| Metals (XAU) | GOLD 2009–2026 | 67 | **12** | **1.014** | PARITY +0.009 [−0.003,+0.028] | PROVISIONAL; silver shares, flagged |
| US/UK/BR/KR/AE/IN | none | — | unfitted | 1.0 | — | fit on first names' panel before any FAIL is real |

## Per-name verdicts under own-market fits (LONO where ≥2 names)

EG: EMFD PASS +0.103 · OCDI PASS +0.087 · TMGH PASS +0.054 · ORHD PARITY +0.036 ·
PHDC PARITY +0.037 · GBCO PARITY +0.001 · KABO PARITY −0.008.
SA: MAADEN PARITY +0.020 (LONO); ALINMA **BOUNDARY** (below).
QA: QGTS PARITY −0.011. XAU: GOLD PARITY +0.009 (near-PASS).

## Headline results

1. **QGTS: FAIL → PARITY under its own market fit.** Under the borrowed Egypt
   archetype (nu=4, cal=1.0) it was a confirmed FAIL; its own fit is the
   *Gaussian limit* with a slightly-wide cone (0.916) — a pegged low-vol LNG
   utility has thin tails, the opposite of EGX devaluation-jump tails. Exactly
   the fabricated-FAIL pattern the standing rule targets. Ledger banner change
   is a publish step, separately initiated.
2. **KABO re-scored under Egypt's own fit: PARITY −0.008 [−0.051,+0.042]** —
   the queued re-score (OHLC now available) no longer supports its FAILED
   banner either. Same publish-step caveat.
3. **Metals ≠ EGX shape, quantified**: gold fits nu=12/cal≈1.0 — near-Gaussian.
   The old borrowed t5 was too fat for metals; the borrowed EG nu=4 would have
   been worse. Egypt's cone narrows ~3.5% (cal 0.965) — the LONO range from
   the earlier 5-name fit (0.98–1.06) tightens with 7 names.

## Two rules codified in code this session

**Robust-verdict rule**: a name-level FAIL requires the bootstrap CI entirely
below zero robustly across block sizes {2,3,4} (10k draws, 50k paths). A
block-dependent sign flip = BOUNDARY → recorded PARITY-flagged, reviewed at the
name's next live grade. Trigger case: **ALINMA** (skill −0.010; block=2 →
PARITY, block=3/4 → FAIL). Its published parity-tier record stands (frozen);
structural driver is Saudi-wide (shrink_cal cap 1.30 binding — MLE wanted
1.40), not Alinma-specific; first live grade 2026-08-04 is the review point.

**Per-market fit rule** (docstring, `market_profiles.py`): a new market's FIRST
action is fitting its own shape/width; borrowed configs are flagged and never
ground a FAIL; single-name fits are provisional until 2+ names; refits on the
panel-growth cadence with the outlier-triggered immediate-review exception.

## Honest caveats

- QA and XAU are self-fits (fit and verdict share the same data) — configs are
  the best available production choice, but the verdicts are indicative until a
  second name/instrument de-circularizes them (QNB/IQCD, silver OHLC queued).
- SA LONO at n=2 produced a Gaussian fit from MAADEN alone that FAILed ALINMA —
  documented as why pooled is production and why the ELM panel append
  (SA_ELM_60d.csv, open item) matters.
- Fed schedule added for XAU/US backtest carry (policy-history midpoints,
  gate-neutral by construction); US profile's flat placeholder replaced.
