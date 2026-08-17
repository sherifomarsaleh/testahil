# raw_indices — market indices, deliberately OUTSIDE raw_ohlc

Every `.csv` under `engine/raw_ohlc/{MARKET}/` is treated by the unattended
pipeline as a COVERED NAME: it enters that market's calibration panel, gets a
per-name verdict, and counts toward the panel's pooled fit. Market and ticker
are decided by file placement, never inferred from a filename.

An index is not a covered name. Dropping KOSPI100.csv into `raw_ohlc/KR/`
would silently make Korea a four-name panel in which one "stock" is a
capitalisation-weighted average of the other three — double-counting them and
flattering the fit with a series that is, by construction, less volatile than
its members.

Indices live here instead, and are read explicitly by the code that wants them:

  - BETA (SIGCM #6 / the WACC beta hierarchy): a stock's beta must come from its
    OWN price history regressed against its OWN local index. KOSPI100 is the
    correct regressor for a KR name, exactly as EGX30 is for an EGX name.
  - Market-factor diagnostics and any future index-relative work.

Nothing in this directory is part of any MC panel.

## Present

| Market | File | Span | Source format |
|---|---|---|---|
| AE | `AE/ADXGENERAL.csv` | 2011-01-02 → 2026-07-24 | investing.com daily export |
| EG | `EG/EGX30.csv` | 2011-01-02 → 2026-07-22 | investing.com daily export |
| IN | `IN/NIFTY50.csv` | — | investing.com daily export |
| KR | `KR/KOSPI100.csv` | — | investing.com daily export |
| QA | `QA/QATAR10.csv` | — | investing.com daily export |
| US | `US/NASDAQCOMP.csv` | — | investing.com daily export |

EG/EGX30 was added 9-Aug-2026. Until then this directory carried an index for
every covered market EXCEPT Egypt — the largest panel, and the one whose beta
rule this README already named explicitly. The series lived only as an upload in
a chat tool, so every EGX beta rested on a file that was in no repository.
Trading-day density is 241–244 sessions/year for 2021–2025 against a real EGX
calendar of ~245, and no row carries a blank price.

Note the series ends 2026-07-22, a few weeks behind spot. That is immaterial for
a 2–5yr weekly beta regression but should be refreshed alongside the price
libraries; flag the as-of date whenever a beta is quoted from it.

AE/ADXGENERAL is the FTSE ADX General Index, added 9-Aug-2026 alongside the
ADNOCDRILL study. Until then the UAE had no index here and the one beta the house
had measured for an Abu Dhabi name used an equal-weight composite of the 18-name
price library as a stand-in. That stand-in is not neutral: it under-weights the
large-capitalisation constituents the published index is concentrated in, and on
ADNOCDRILL it read beta 0.664 against 0.795 on the real index — a 0.13 difference
worth about 64 basis points of cost of equity, despite the two series correlating
0.84 week to week. Any beta previously measured against a constructed composite
should be re-run against the published index before it is relied on.

Screened before use: 3,884 rows, no blank prices, no duplicate dates, largest
single-session move 8.4% (well inside the ADX daily limit), and 238-253
sessions/year for 2021-2025 against a real calendar of ~250 after the Jan-2022
workweek switch. Like EGX30 it ends a few weeks behind spot (2026-07-24), which
is immaterial for a 2-5yr weekly regression but must be flagged whenever a beta
is quoted from it.
