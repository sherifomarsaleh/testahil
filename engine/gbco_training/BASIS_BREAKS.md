# GBCO panel — basis-break register

Built before modelling, per the training pre-registration. Each break states the era it
separates, the overlap-year reading(s), the chain treatment, and the scoring consequence.
Unit drivers are scored only inside their own definition window. All quotes are from GB
Corp's (formerly GB Auto's) own documents extracted in this session — see SWEEP_LOG.md.

## B1 — FX regime changes (macro, exogenous)
- 3-Nov-2016 float: EGP/USD average 7.69 (2015) → 10.03 (2016) → 17.78 (2017).
- Mar-2022 / Jan+Mar-2023 step devaluations, Mar-2024 unification, flexible after:
  19.16 (2022) → 30.63 (2023) → 45.30 (2024) → 49.23 (2025 avg).
- Treatment: no chaining (all figures nominal EGP); depreciation is an exogenous driver
  input; era boundaries E1 2016–2019, E2 2020–2021, E3 2022–2024, E4 2025– used for
  sign-by-era tests. Macro-vs-company split re-runs origins with realized FX.

## B2 — Leases (EAS 49 / presentation)
- ER segment presentation: "Due to a change in Egyptian Accounting Standards, the related
  leased assets have been recorded on the balance sheet under PP&E, while the liabilities
  have been booked under Payables, starting from 2Q19 onwards" (ER 4Q23, Table 7 footnote).
- FS level: AR2019 restated the FY2018 comparatives (revenue 25,811,964 → 25,621,245
  EGP 000, −0.74%; parent NP 515,710 → 544,833; total assets 21,070,927 → 21,517,951);
  EAS 47/48/49 formally first-applied 1-Jan-2021 after PM Decision 1871/2020 postponed
  them (FY2021 FS: right-of-use asset 440,333, lease liability 327,299, EAS 48 retained
  earnings effect EGP 12.5mn, EAS 47 risk reserves created).
- Overlap year: FY2018 has two readings — original (AR2018) and EAS-49-restated (AR2019).
  Revenue chain factor 25,621,245 / 25,811,964 = 0.99261.
- Treatment: panel records the original reading (point-in-time rule); the restated reading
  sits beside it; growth rates spanning FY2018→FY2019 are computed restated-to-reported
  (same basis) inside bottom_up.py where the origin could see both (origins ≥ 2020).

## B3 — Disclosure re-cut, 2Q17: "GB Auto & Auto Related" vs "GB Capital"
- Adopted in 2Q17 ("in the second quarter of the year we adopted a new disclosure
  structure that separately reports our core automotive under GB Auto & Auto Related and
  high-margin financing businesses under GB Capital" — AR2017 CEO letter).
- Treatment: segment-level financing drivers exist from FY2017; before that, financing
  results sit inside "Others/Financing" segment lines. Financing driver scored from
  origin 2018 onward only.

## B4 — Microfinance / MNT-Halan perimeter (the central perimeter break)
- Through FY2021: Mashro'ey + Tasaheel (microfinance) CONSOLIDATED. Sep-2021: 5% of
  MNT (BV) sold, stake to 57.26%, still consolidated (gain EGP 251mn direct to retained
  earnings, FY2021 FS note 41). Halan Consumer Finance new 57.26% subsidiary FY2021;
  "Halan for Information Technology" a 40.13% associate.
- 4Q22: loss of control — sale of a 7.5% stake in MNT-Halan plus deconsolidation:
  FY2022 IS carries "Gain from sale & Revaluation of investment associate" of
  8,207,309 EGP 000 (FY2023 FS comparative column); FY2022 equity statement carries
  "Loss of control of subsidiary" rows. ER 4Q23 Table 14: GB Capital FY22 "restated …
  without consolidating MNT-Halan to be comparable to 2023".
- FY2023 onward: MNT-BV an associate (~44% per FY24/FY25 audit reports; 42.93% per
  H1-2026 review) picked up through the associates line; auditor qualifications from
  FY2024 on stem from MNT-BV's FS not being provided.
- Overlap-year readings: GB Capital segment revenue FY22 as-consolidated 4,274.3
  (restated ex-MNT, ER 4Q23) vs FY23 4,950.9 EGP mn — same basis; group revenue FY22
  original 29,789,079 EGP 000 (includes part-year microfinance consolidation effects).
- Treatment: financing-segment driver scored within windows (≤2021 incl. microfinance;
  ≥2023 ex.); FY2022 is a flagged transition year; the 8,207.3mn gain is registered as
  a one-off and NP is scored both as-reported and ex-one-offs; the associates line from
  FY2023 is a separate driver (frozen-at-last-actual rule per pre-registration).

## B5 — KPI/LoB re-cut, FY2024 reporting
- From ER 4Q24: PC line of business reported as Egypt+Iraq+Jordan COMBINED (previously
  Egypt PC and Regional separately); "Trading" LoB introduced (Tires Egypt + Ready
  Parts Egypt & Iraq); After-Sales no longer a separate LoB row.
- Overlap-year readings (FY2023, both cuts disclosed): Egypt-only PC 16,469 units /
  9,545.2 EGP mn (ER 4Q23) vs combined PC 26,994 units / 16,544.3 EGP mn (ER 4Q24
  comparative). Chain factor on PC units 26,994/16,469 = 1.639 (adds Iraq+Jordan).
- Treatment: PC volume/ASP drivers scored on the Egypt-only definition through
  origin 2023 outcomes, and on the combined definition from origin 2024 outcomes;
  no cross-definition growth rate is ever computed inside bottom_up.py.

## B6 — Restatements register (measurement, not perimeter)
| year restated | where | what moved (EGP 000) |
|---|---|---|
| FY2018 | AR2019 (EAS 49) | see B2 |
| FY2020 | FY2021 FS note 35 | associate opening balance −2,680; parent equity 4,630,779→4,628,099; CF 2020 comparative: associate payment 42,550 moved CFF→CFI |
| FY2023 | FY2024 FS | IS reclass, NP-neutral: OP 3,708,121→3,637,293 (+other-expenses/ECL presentation), tax −493,234→−422,406; BS: parent equity 19,838,656→19,792,950, intangibles 350,473→535,108, associates 10,625,833→10,395,492 |
| FY2024 | FY2025 FS | parent equity 25,438,502→26,233,452 (+794,950); associates 11,598,273→12,107,366; NCI 1,978,417→2,016,109 |
| FY2025 | H1-2026 FS | "Adjustments on the beginning balance" +2,882,696 to parent equity (28,788,713→31,671,409); associates 13,272,208→15,732,426; fair-value reserve 2,012,393→3,452,187 (MNT-BV fair-value uplift) |
- Treatment: the panel stores originally-reported values (point-in-time); restated values
  are recorded beside them here and in the panel oddities. Restatements never enter a
  driver history at an origin that predates their publication.

## B7 — One-off register (company-attributed, scored both ways per pre-registration)
| FY | item | size |
|---|---|---|
| 2016–2017 | post-float shock: FY16 net loss 865.7 EGP mn parent, FY17 net loss 666.9 EGP mn parent; PC market fell 29.9% in FY17 (AMIC) | era marker |
| 2020 | COVID demand shock (market still +32% on 2019's low base) | era marker |
| 2021 | 5% MNT (BV) stake sale gain, direct to retained earnings | 251 EGP mn |
| 2022 | MNT-Halan deconsolidation + 7.5% stake sale gain in IS | 8,207.3 EGP mn |
| 2023 | Algeria investment fully impaired (4Q23) | 522.0 EGP mn |
| 2023 | impairment of fixed assets (CF add-back; Algeria-linked) | 375.5 EGP mn |
| 2023 | 4Q23 FX loss inside FY23 FX line (devaluation) | 1,019.7 EGP mn (4Q) |
| 2023 | three-wheeler import ban from 1-Jul-2023 (regulatory; permanent) | 3W volumes → ~0 |
| 2025 | goodwill impairment (CF); selective impairment/inventory provisioning 4Q25; Turkey hyperinflation drag via MNT-BV pickup | 47.8 EGP mn + flagged |

## B8 — Auditor qualification window (caveat, not an adjustment)
- FY2024, FY2025 audits and Q1/H1-2026 reviews are QUALIFIED solely on MNT-BV's
  financial statements not being made available to the auditor (profit share recorded:
  FY24 849.9, FY25 965.6, H1-26 409.9 EGP mn). FY2023 and earlier: unqualified
  (FY2023 carries an FX-availability emphasis of matter).
- Consequence: the associates line from FY2024 is management-recorded, not
  auditor-verified; the training treats it as a separate driver and the caveat is
  restated in TRAINING_RECORD.md.
