# Fundamental Driver Ledger

Append-only record of driver decisions by name and class, with the evidence each
decision rests on. Referenced by CLAUDE.md and the standing protocol; this file was
first created 30-Aug-2026, seeded by the GBCO fundamental walk-forward training run
(the first entry below). Back-filling driver decisions from the previously delivered
studies (each study's own compute.py and QC documents) remains an open research task —
entries are added from real compute only, never reconstructed from memory.

---

## GBCO (GB Corp, EGX) — walk-forward training, 30-Aug-2026

**Source of record:** engine/gbco_training/ (panel FY2011–FY2025 + 2026 interims, all
company-primary; PREREGISTRATION.md committed before scoring; 738 scored cells over
origins 2016–2025).

| driver class | decision | evidence |
|---|---|---|
| volumes — PC | share × market anchoring is roughly unbiased (h1 bias +3.6%) but only where the AMIC market series and a same-basis unit history exist; own-trend fallback under-forecasts violently in devaluation years (origin-2024 h1 −61% on a truncated window). In the update: never freeze PC off a short post-re-cut window; state the market anchor explicitly. | errors_by_driver.csv; TRAINING_RECORD.md failure mode 2 |
| volumes — 2/3/4W | trailing-CAGR volumes are unbiased on average but MAE 0.63; the Jul-2023 3W import ban is a regulatory kill no trend rule sees. Regulatory-regime flags belong in the driver set for this class. | BASIS_BREAKS.md B7; errors_by_driver.csv |
| price/ASP | π + 0.5·FX-dep escalator on ASPs performed adequately at h1; at h3–h5 compounding trailing macro over-forecasts after shocks (origin 2020). The wedge vs cost pass-through is the single most NP-consequential stated assumption (NP h1 MAE 0.57–1.46 across stated variants) — sensitivity reported, not re-fitted. | sensitivities.csv |
| SG&A | fixed/variable split (φ=0.5) escalated at CPI under-forecast SG&A at 9 of 10 origins (median −11%). WATCH FLAG SGA_UP_5PCT: +5.7% growth-factor correction passed on GBCO's own record (4 of 6 corrected origins improved; sign-stable across eras) but is NOT carried — book-wide consistency unverifiable on a first run. Re-test when a second EG name runs this program. | corrections_test.json |
| capex | revenue-ratio capex over-forecasts (bias +25%): GB's capex is programme-driven (Sadat, Ain Sokhna). Anchor on the disclosed programme. | errors_by_driver.csv; ER 4Q24/4Q25 guidance items |
| working capital | t3-average DIO/DSO/DPO days landed MAE 0.36–0.50 with mild negative bias — serviceable; inventory days spike with import restrictions (2022–24) faster than a 3-year average adapts. | errors_by_driver.csv |
| financing segment | most forecastable driver at h1 (MAE 0.17) but persistently under-forecast (−16%): portfolio compounding beats trailing CAGR; in C3 (ex-MNT) origins the under-forecast widens (portfolio nearly doubled FY25). Model the portfolio, not the revenue line, when disclosure allows. | errors_by_driver.csv; ER 4Q25 GB Capital tables |
| associates | freezing at last actual misses the MNT-BV pickup entirely (~EGP 1bn/yr from FY2023); the line is auditor-qualified (MNT-BV FS not provided, FY24→H1-26). Model explicitly; carry the qualification as a caveat wherever quoted. | BASIS_BREAKS.md B8 |
| one-offs | FY22 deconsolidation gain (EGP 8,207mn) and FY23 Algeria impairment (EGP 522mn) dominate reported-NP scoring; ex-one-off scoring removes a third of the NP h1 bias. Register one-offs before scoring any NP record for this name. | np_ex_oneoffs.csv; B7 |
| macro conditioning | realized-macro re-runs remove only 8% (rev) / 20% (NP) of h1 MAE and HURT at h3–h5 — long-horizon misses are company-structure errors (perimeter, volumes under import restriction, associates), not macro-path errors. | macro_company_split.csv |
| forecast ranges | update publishes years 3–5 as ranges from this record's error quantiles: rev h3 ×[0.61..1.40], h4 ×[0.38..1.30], h5 ×[0.41..1.12]; GP h4 ×[0.81..1.43]; NP ranges built from rev/GP plus the SG&A bias band (NP quantile sample too thin, n=3, and said so). | TRAINING_RECORD.md §5 |
