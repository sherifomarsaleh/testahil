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

AE/ADXGENERAL is the FTSE ADX General Index, added 9-Aug-2026 for the ADNOCDIST
study. Before it, an ADX name's beta was regressed against an equal-weight
composite built from the `raw_ohlc/AE` library — the house stand-in when a
market's index was missing. That stand-in is NOT interchangeable with the real
index, and the direction of its error is systematic rather than random: the
equal-weight composite's weekly volatility is 1.34x the published
capitalisation-weighted index's, and since beta divides covariance by the
market's own variance, the more volatile stand-in returns a LOWER beta. For
ADNOCDIST it gave 0.507 against the published index's 0.649, on an almost
unchanged correlation (0.44 vs 0.42). Any other AE study whose beta predates this
file was therefore biased low and should be re-measured against it.

The index is screened on its own terms and NOT through `data_quality.clean_ohlc`.
That gate asks whether a move exceeds what one session can physically produce
under the exchange's own daily price limit — a test about corporate actions in a
single stock. An index has neither, so the gate has nothing to say about it;
applying it would risk "repairing" a real market move. Screening instead checks
continuity, duplication, non-positive levels, and whether the trading-day pattern
matches the exchange calendar. It does: 3,884 sessions, no duplicate or
out-of-order dates, largest single-session move 8.4% (March 2020), and the
weekday distribution switches cleanly from Sunday-Thursday to Monday-Friday at
the January 2022 workweek change.

Note the series ends 2026-07-22, a few weeks behind spot. That is immaterial for
a 2–5yr weekly beta regression but should be refreshed alongside the price
libraries; flag the as-of date whenever a beta is quoted from it.
