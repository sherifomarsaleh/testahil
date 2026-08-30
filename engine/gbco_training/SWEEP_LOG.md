# GBCO fundamental walk-forward training — Sweep Register (source attempts)
# Every attempt logged: timestamp UTC | target | outcome | note

| 2026-08-30 13:05 UTC | WebSearch: GB Corp IR site | SUCCESS | ir.gb-corporation.com identified (also gb-corporation.com/investor-relations/) |
| 2026-08-30 13:07 UTC | https://ir.gb-corporation.com/en + /en/filings | SUCCESS | Results center 2020–2026; 289 filings, paginated |
| 2026-08-30 13:10 UTC | Scrape /en/filings?page=1..29 (curl) | SUCCESS | 292 unique PDF URLs enumerated |
| 2026-08-30 13:12 UTC | Download 31 company PDFs (ARs 2011–2025, cons. FS 31-Dec-2020..2025, ER 4Q20..4Q25, ER 1Q26, ER 2Q26, cons. FS 30-Jun-2026, standalone FS 31-Mar-2026) | SUCCESS | 159 MB, all valid PDFs; held in session scratchpad, cited by URL in panel |
| 2026-08-30 13:15 UTC | pdftotext conversion | PARTIAL | Image-only (no text layer): FS 31-Dec-2022/2023/2024/2025, FS 30-Jun-2026, ER 4Q23/4Q24/4Q25, AR 2017, AR 2023, AR 2024 — extracted by visual page read instead |
| 2026-08-30 13:40 UTC | Visual reads: FS 31-Dec-2025/-2024/-2023, ER 4Q25/4Q24/4Q23, FS 30-Jun-2026, FS 31-Mar-2026, AR2017 pp.6-15+ | SUCCESS | statements + segment volumes + guidance captured; recorded in extract/*.json |
| 2026-08-30 13:20 UTC | World Bank API: EGY CPI inflation (FP.CPI.TOTL.ZG), EGP/USD avg (PA.NUS.FCRF), 2009-2025 | SUCCESS | exogenous conditioning series, tier C |
| 2026-08-30 14:30 UTC | Extraction complete: 15 FY + 2026 interims + ER KPI files, all tier A | SUCCESS | 21 JSON records archived under extraction/ with verbatim quote lines |
| — | Sources NOT attempted this run | n/a | AMIC's own published tables (market series taken from GB's own documents; 2023–2025 entries DERIVED and flagged); EGX disclosure archive (unneeded — company archive covered the full span) |
