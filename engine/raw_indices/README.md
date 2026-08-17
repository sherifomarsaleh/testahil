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
| AE | `AE/FADGI.csv` (FTSE ADX General) | 2011-01-02 → 2026-07-24 | investing.com daily export |
| EG | `EG/EGX30.csv` | 2011-01-02 → 2026-07-22 | investing.com daily export |
| IN | `IN/NIFTY50.csv` | — | investing.com daily export |
| KR | `KR/KOSPI100.csv` | — | investing.com daily export |
| QA | `QA/QATAR10.csv` | — | investing.com daily export |
| SA | `SA/TASI.csv` (Tadawul All Share) | 2011-01-01 → 2026-07-27 | investing.com daily export |
| US | `US/NASDAQCOMP.csv` | — | investing.com daily export |

## Missing — no conforming beta is possible in these markets

**BR, GB.** (SA/TASI supplied 10-Aug-2026.) Under the amended BETA rule (10-Aug-2026) a constituent
composite is not a substitute, so a study on a name in these markets must STOP AND ASK
for the index rather than build one.

AE/FADGI was added 10-Aug-2026. Until then every AE beta ran against an equal-weight
composite of the covered `raw_ohlc/AE/` names — which mixed ADX and DFM constituents,
so an ADX-listed share was regressed against an ADX/DFM mongrel. On FERTIGLB that
composite gave beta 0.492 (R² 6.2%) against the real index's 0.931 (R² 10.0%): a ~40%
understatement that overstated fair value by 21.6%. The same substitution was in force
in all seven EGX studies. See the BETA section of `Standing_Research_Protocol.md`.

**A market having a file here is not the same as its studies using it.** EGX30 landed
09-Aug-2026 and no EGX study regressed against it; they all kept the composite until the
rule was made explicit. When adding an index, re-derive the betas that predate it.

EG/EGX30 was added 9-Aug-2026. Until then this directory carried an index for
every covered market EXCEPT Egypt — the largest panel, and the one whose beta
rule this README already named explicitly. The series lived only as an upload in
a chat tool, so every EGX beta rested on a file that was in no repository.
Trading-day density is 241–244 sessions/year for 2021–2025 against a real EGX
calendar of ~245, and no row carries a blank price.

AE/FADGI (the FTSE ADX General Index) was added 9-Aug-2026, and the gap it closed was
the same one EGX30 closed for Egypt: until it arrived, the UAE beta had no local index to
regress against, and the BOROUGE study's first revision used an equal-weight basket of the
other names in `raw_ohlc/AE/` as a stand-in. That stand-in is not the market. An
equal-weight basket over-weights small, thinly traded constituents, which drags its own
volatility up and its covariance with any single large name down; on BOROUGE it produced a
beta of 0.271 against the index's 0.415, a 35% understatement. Any AE beta measured before
9-Aug-2026 rests on the basket and should be re-run.

Cleaning gate on FADGI: 3,884 rows in, 3,883 out (one stale no-trade row dropped),
238-252 trading days a year against an ADX calendar of about 250, ZERO sessions closing
unchanged, and a maximum daily move of 8.4% against the ADX ±15% limit. A cap-weighted
index with no flat sessions carries no stale-price artefact, which matters because a stale
regressor biases every beta measured against it downward.

Note the series ends 2026-07-22, a few weeks behind spot. That is immaterial for
a 2–5yr weekly beta regression but should be refreshed alongside the price
libraries; flag the as-of date whenever a beta is quoted from it.
