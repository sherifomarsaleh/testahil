# F5 (AMIHUD) VOLUME FORENSIC PASS — 27-Jul-2026

**Status: forensic determination complete; treatment SIGNED by the sponsor
27-Jul-2026 — F5 retired as UNTESTABLE ON THIS DATA (recorded in the
pre-registration's §11 addendum).** This is the per-name pass that §8 of the pre-registration made a
precondition for trusting F5 in either direction. Bottom line: **F5 is untestable on
this library — not because of the flagged jump-days alone, but because the factor's
construction (vendor-adjusted Price × unadjusted Volume) violates point-in-time
discipline at every corporate action.** The flags were the smoke; the adjustment
asymmetry is the fire.

## Method

For every name (EG queue first, then AE; SA already near-pristine): every >50× /
<1/50× jump-day vs the trailing 20d median volume was classified by whether the
20d-median level AFTER the day differs from BEFORE by >10× and persists (**SHIFT** —
a level break), reverts to within 3× (**SPIKE** — a real one-day burst), or neither
(**AMBIG**); each jump-day was also checked for a vendor-suffix anomaly (a K-day
inside an M-neighbourhood etc.) and a coincident >25% price move (corporate-action
signature). Classifier thresholds recorded here so the pass is reproducible.

## EG results (30 names)

| Class | Names | Detail |
|---|---|---|
| CLEAN (0 flags) | CCAP, COMI, EFIH, EMFD, OIH, PHDC, TMGH | — |
| SPIKES-ONLY (real lumpiness) | ISPH, KABO, FWRY, ETEL, HELI, OCDI, HRHO, PRDC | 1–9 one-day bursts each, all revert — ordinary EGX block-trade lumpiness, not a data defect |
| LEVEL BREAKS / defects | **EFID** (176 flags: 21 SHIFT, 60 suffix anomalies, dead-days at 140–740 shares), **JUFO** (129: mostly real spikes + 2 SHIFTs incl. the Nov-2022 devaluation regime), **GBCO** (91: two-week collapse to ~1k shares May-2014), **BTFH** (45: week at 1% volume Nov-2015), **CLHO** (45: ×34 sustained step Aug-2017, ×12 step Jan-2018), **ABUK** (65: 2011 zero-price placeholder rows at 20–160 shares — already repaired by the Step 0.0 gate, no leak into returns), LCSW, ORWE, RAYA, ORAS (40-share days Jan-2019), DSCW (×48 step Jan-2019), EGAL, ORHD, RMDA (×17 step Jun-2020), ADIB | micro-volume collapse episodes are impossible as trading; sustained step-ups mostly coincide with real events (IPO stabilisation, offerings, the Nov-2022 float) |

## AE results (18 names, long export)

Much cleaner: BURJEEL, DIB, EMAAR, LULU, SALIK, TWOPOINTZERO clean; ADCB, FAB, ADIB,
ALDAR, ALPHADHABI, EMAARDEV, ADNOCGAS, DEWA, EAND spikes-only; **AGTHIA** (64 flags,
2 SHIFTs), **IHC** (35 flags, 7 SHIFTs — consistent with its restructuring history)
and ENBD (38, all revert) carry the pre-2021 flags. SA: ≤2 jump-days per name,
0 SHIFTs — near-pristine (per the SA gate).

## The disqualifying finding — demonstrated, not asserted

**CLHO, January 2018** (known corporate action): in the vendor file the *adjusted*
price glides through the event — max daily move 8.3%, no jump anywhere in the window —
while volume steps permanently from ~0.2M to 7–14M shares/day:

```
2018-01-16  4.58  193.02K      2018-01-21  4.83  10.13M
2018-01-17  4.84    7.06K      2018-01-22  4.95  14.23M
2018-01-18  5.25    4.56M      2018-01-23  5.08   7.49M
```

That is the signature of **retroactively adjusted prices with unadjusted volume**.
Consequences, mechanical and general:

1. `Price × Vol.` carries a **permanent level break at every corporate action** —
   every Amihud window before the event is mis-scaled relative to after.
2. The mis-scaling applies to all history *before* the event, and the vendor applies
   it retroactively — so **the F5 value at anchor t changes when a corporate action
   happens years later.** A 2015 Amihud reading depends on a 2024 stock dividend.
   That is a §3 point-in-time violation *by construction* — the same class of sin as
   the retroactive-FV look-ahead — and no per-name exclusion fixes it: ordinary
   2:1–4:1 EGX stock dividends never trip a 50× screen and were never flagged.
3. Cross-sectionally, names are mis-scaled by *different* future factors, so the
   ranking itself — the only thing F5 feeds — is contaminated.

The jump-day defects (EFID's suffix drops, the micro-volume collapse episodes) are
real and would justify excluding specific names; they are listed above for the
record. But the adjustment asymmetry disqualifies the factor definition itself on
this library, exclusions or not.

## Treatment (SIGNED by sponsor, 27-Jul-2026)

1. **F5 is recorded as `UNTESTABLE ON THIS DATA` — retired from the runnable set,
   not refuted.** Its interim (−0.0086) and full-power (+0.0104, 3/3 signs) readings
   are void, not weak — the sign consistency is as meaningless as the magnitude.
2. **The Bonferroni divisor stays at 6.** The bar was registered at six factors;
   retiring one as untestable must not loosen the bar for the survivors.
3. Future re-runs compute F5 for continuity but its verdict column reads
   `UNTESTABLE`, with no IC quoted in headlines.
4. **Revival path (a §10 amendment + new data, if ever wanted):** source daily
   **value traded** (EGP/AED/SAR turnover — EGX, ADX and Tadawul all publish it) and
   re-register the factor as `mean |ret| / turnover`, which is both the fix and the
   textbook Amihud construction. The volume column in the current library is fine
   for what the other five factors use it for: nothing.

## Reproduction

`f5_forensics.py` (EG) / `f5_forensics_ae.py` (AE) in the session workspace; inputs =
repo EG at `cd68546` + staged AE long export; outputs `f5_forensics{,_ae}.pkl` with
the full per-jump-day classification. ABUK's 11 corporate-action-flagged days were
traced to 2011 zero-price placeholder rows already repaired by `clean_ohlc`
(post-gate returns show NaN, not −inf) — no leakage into F1–F4/F6.
