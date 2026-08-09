"""dq_patch.py — proposed fix for TWO defects in engine/data_quality.py that only
become reachable once EGX history extends back before ~2021.

DEFECT 1 — NON-POSITIVE PRICE ROWS.
The vendor writes Price = 0.00 on some sessions while Open/High/Low are valid
(a missing-close artifact). clean_ohlc does np.log(0) = -inf, reads it as an
infinite one-day move, and computes factor = p[i+1]/p[i] = inf (or 0.0). It then
multiplies EVERY prior row by 0 or inf. Measured on this upload: 17 such rows
across 5 of 16 names — and on OCDI it rescales 536 rows of history to zero.
These rows survive the existing placeholder filter because they carry real
volume and a real High != Low range.
FIX: drop non-positive / non-finite Price rows BEFORE the jump scan. Dropping,
not imputing — no invented closes enter a calibration panel.

DEFECT 2 — SPIKE-AND-REVERT BAD PRINTS TREATED AS CORPORATE ACTIONS.
A one-session bad print (BTFH 4.638 -> 16.390 -> 5.006; HELI 0.330 -> 12.080 ->
0.340) is not a corporate action. A corporate action is ONE-WAY and permanent.
The current iterative back-adjust handles each leg separately and applies two
rescalings that do NOT cancel:
    BTFH  x3.5339 then x0.3054 -> net 1.0793  (+7.9% on 952 prior rows)
    BTFH  x3.0933 then x0.2971 -> net 0.9190  (-8.1% on 989 prior rows)
    HELI  x36.606 then x0.0281 -> net 1.0286  (+2.9% on 228 prior rows)
so prior history is left permanently mis-scaled AND the bad print itself stays.
FIX: before treating a breach as a corporate action, check whether the NEXT
session reverses it. If breach i and breach i+1 are opposite-signed and their
sum returns within the artifact threshold of the pre-spike level, it is a
single-session bad print -> drop that ONE row, rescale nothing.

Both fixes are conservative: they only ever REMOVE rows the exchange could not
have traded, and they strictly reduce the number of back-adjustments applied.
"""
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '/tmp/mcrev/testahil/engine')
from data_quality import jump_threshold


def clean_ohlc_v2(df, ticker="", verbose=False, market=None):
    df = df.copy().reset_index(drop=True)
    log = []

    # --- 0. leading pre-listing placeholders (unchanged behaviour) -----------
    novol = df['Vol.'].isna() | (df['Vol.'].astype(str).str.strip()
                                 .isin(['', 'nan', 'None', '-']))
    flat = (df['High'] == df['Low'])
    placeholder = novol & flat
    if placeholder.any():
        first_real = int((~placeholder).idxmax())
        lead = int(placeholder.iloc[:first_real].sum())
        if lead:
            log.append(f"dropped {lead} leading pre-listing placeholder rows")
            df = df.iloc[first_real:].reset_index(drop=True)
        interior = int(placeholder.sum() - lead)
        if interior:
            df = df[~(df['Vol.'].isna() & (df['High'] == df['Low']))].reset_index(drop=True)
            log.append(f"dropped {interior} interior stale/no-trade rows")

    # --- FIX 1: non-positive / non-finite closes ----------------------------
    bad = ~np.isfinite(df['Price'].values) | (df['Price'].values <= 0)
    if bad.any():
        d0 = df.loc[bad, 'Date']
        log.append(f"FIX1 dropped {int(bad.sum())} rows with a non-positive/missing close "
                   f"({d0.iloc[0].date()}..{d0.iloc[-1].date()}) — vendor missing-close "
                   f"artifact, would have produced log(0) = -inf")
        df = df[~bad].reset_index(drop=True)

    # --- FIX 2 + corporate actions ------------------------------------------
    thr = jump_threshold(market)
    for _ in range(12):
        p = df['Price'].values
        lr = np.diff(np.log(p))
        hits = np.where(np.abs(lr) > thr)[0]
        if len(hits) == 0:
            break
        i = int(hits[0])
        # spike-and-revert? a breach at i that REVERSES within MAXBLOCK sessions
        # is a bad-print block, not a corporate action (which is one-way and
        # permanent). BTFH 2016-05 is a 3-session block, so adjacent-only is not
        # enough — scan forward.
        MAXBLOCK = 5
        rev = None
        for k in range(1, min(MAXBLOCK, len(lr) - i)):
            cum = lr[i:i + k + 1].sum()
            if abs(lr[i + k]) > thr and np.sign(lr[i + k]) != np.sign(lr[i]) \
                    and abs(cum) <= thr:
                rev = k
                break
        if rev is not None:
            d0 = df['Date'].iloc[i + 1].date(); d1 = df['Date'].iloc[i + rev].date()
            log.append(f"FIX2 dropped {rev} bad-print row(s) {d0}..{d1} "
                       f"({p[i]:.3f} -> {p[i+1]:.3f} ... -> {p[i+rev+1]:.3f}; "
                       f"net log over the block {lr[i:i+rev+1].sum():+.3f}) — reverts "
                       f"within {rev} session(s), so NOT a corporate action; "
                       f"rescaled nothing")
            df = df.drop(index=range(i + 1, i + rev + 1)).reset_index(drop=True)
            continue
        # genuine one-way corporate action -> back-adjust (unchanged behaviour)
        factor = p[i + 1] / p[i]
        if not np.isfinite(factor) or factor <= 0:
            log.append(f"FIX1 guard: refused a non-finite back-adjust factor at "
                       f"{df['Date'].iloc[i+1].date()}")
            break
        d = df['Date'].iloc[i + 1].date()
        for c in ['Price', 'Open', 'High', 'Low']:
            df.loc[:i, c] = df.loc[:i, c] * factor
        log.append(f"back-adjusted {i+1} rows before {d} by x{factor:.4f} "
                   f"(raw 1-day log move {lr[i]:+.3f} exceeds the {market} "
                   f"artifact threshold {thr:.3f})")

    if verbose and log:
        print(f"  [{ticker}] " + f"\n  [{ticker}] ".join(log))
    return df, log
