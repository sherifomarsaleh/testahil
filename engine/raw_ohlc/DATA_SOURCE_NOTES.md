# Vendor export conventions — read before splicing a library

Step 0.0 (`engine/data_quality.py`) catches jumps, placeholder rows, non-positive
prices and isolated phantom prints. It does **not** check whether a vendor's OHLC
columns mean what the library's columns mean, and that is a per-export property —
"Vendor corruption is PER-EXPORT: never assume a file is clean because another from
the same vendor was."

## The continuous-bar (`open = previous close`) export

Measured 06-Sep-2026 on a TradingView-style `EGX_ELEC_1D.csv` export.

The library convention (Investing.com exports) carries the **true session open**.
A continuous-bar export instead carries, for each session *d*:

    open(d)  = close(d-1)                       -- no information about the true open
    high(d)  = max(trueHigh(d), close(d-1))     -- widened to include the prior close
    low(d)   = min(trueLow(d),  close(d-1))     -- widened to include the prior close
    close(d) = close(d)                         -- sound

Only **close and volume survive**. Verified on 623 overlapping 2024+ sessions where
both conventions were available for the same days: the two identities above reproduce
the export's high and low on 99.7% and 98.2% of rows, and `open == prev close` on 95.0%.

### How to tell, in one line

Compare the rate of `open == previous close` against the library's own rate. Across
all 37 EG libraries over 2024+ the natural rate is **15%–36%** (thin names on a 0.01
tick). A continuous-bar export runs at **100%**.

```python
pc = df['Price'].shift(1)
((df['Open'] - pc).abs() < 1e-9).mean()      # >0.9 means a continuous-bar export
```

### What it costs

Striking a cone on such bars feeds `primitives.yz_variance_proxy`, whose overnight
term is `log(open/prev_close)` — identically **zero** on every affected bar, with the
Rogers–Satchell term distorted by the widened high/low.

Measured by striking the *same* origin (2026-08-05, EG/ELEC) twice, with the trailing
window carried under each convention and nothing else changed:

| | library convention | continuous-bar | move |
|---|---|---|---|
| `sigma_h` 1M | 0.09658 | 0.10076 | **+4.3%** |
| `sigma_h` 3M | 0.18774 | 0.19394 | **+3.3%** |
| 90% band width 1M | 30.27% of spot | 31.58% | +3.9% |
| 90% band width 3M | 60.88% of spot | 62.92% | +2.9% |

Both are **inside** the 5% materiality trigger [R-CAL-01], and the direction is
**widening** — the conservative side. The pooled 2024+ variance proxy moves the other
way (−6.6%), so the sign is not stable across windows: **measure it, never assume it.**

### The rule

There is no reconstruction: the true open is **not recoverable** and must not be
invented (SIGCM clause 8 — leave the gap, never interpolate). So:

1. **The close series may always be spliced.** Grading reads closes only, so a
   matured cohort can be graded from such an export with no loss at all.
2. **Splicing the OHL carries a measured cost.** Price it at the actual origin before
   splicing, state it, and do not splice silently.
3. **Never back-fill history from one of these exports.** The same ELEC file was
   dividend-back-adjusted before 2016 (ratio 0.856 in 2011 rising to 1.000 by 2016)
   while the library is unadjusted — 1,996 of 3,738 overlapping rows disagreed beyond
   the 4th decimal, almost all of them from that adjustment.

### Applied history

- **06-Sep-2026, EG/ELEC.** 21 sessions (06-Aug → 06-Sep-2026) spliced from a
  continuous-bar export, all 21 carrying `open == prev close`. Cost priced at the table
  above and disclosed; every pre-existing row preserved byte-for-byte; the library's own
  05-Aug close (2.190) kept over the export's (2.18). Step 0.0 raised no new repair.
