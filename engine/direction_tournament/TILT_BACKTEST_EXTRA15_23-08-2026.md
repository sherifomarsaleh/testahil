# Committed tilt — full production backtest, 93 tickers (23-Aug-2026)

The engine's own walk-forward backtest (backtest_v3), per ticker, both calendar clocks, signal ON (adopted config) vs OFF (carry-only), seed-paired. 'CRPS gain' and 'center gain' are per-origin improvements from the tilt, in units of price (positive = the tilt helped). Coverage under ON shows the tilt does not break the bands. The six non-committed markets run carry-only in production (tilt backtest identical to OFF by construction) — signal-level per-stock records for them are in PER_STOCK_CAREFUL_23-08-2026.

## AE — 0 tickers

| stock | clock | obs | tilted share | CRPS gain | center gain | call hit (tilted) | cov90 ON | cov90 OFF |
|---|---|---|---|---|---|---|---|---|

## EG — 0 tickers

| stock | clock | obs | tilted share | CRPS gain | center gain | call hit (tilted) | cov90 ON | cov90 OFF |
|---|---|---|---|---|---|---|---|---|

## SA — 0 tickers

| stock | clock | obs | tilted share | CRPS gain | center gain | call hit (tilted) | cov90 ON | cov90 OFF |
|---|---|---|---|---|---|---|---|---|

## Pooled summary (committed markets)

| market | clock | stocks | CRPS gain (mean) | center gain (mean) | stocks helped | call hit (pooled) | cov90 ON (mean) |
|---|---|---|---|---|---|---|---|

Caveat (stated in the file header too): direction is out-of-sample validated; tilt magnitudes are in-sample calibrated — live monthly grading is their forward test.