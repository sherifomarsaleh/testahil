"""data_quality.py — OHLC cleaning gate for the Testahil learning loop (11-Jul-2026).

A continuous-learning system is only as good as what it ingests. This gate runs
BEFORE any series enters a calibration panel.

Two failure modes found on the first full EGX ingest:

1. PRE-LISTING PLACEHOLDERS. e-finance (EFIH) carried flat 0.50 rows with NaN
   volume for the days before its 19-Oct-2021 IPO, then opened at 13.98 — which
   the engine read as a +333% (log) one-day return.

2. UNADJUSTED CORPORATE ACTIONS. EFIH's 3:2 split on 26-May-2025 (19.77 -> open
   13.18, ratio exactly 1.500) and SODIC/OCDI's action on 14-Aug-2025 (61.00 ->
   open 17.50) appear as fake -34% and -73% one-day crashes.

DETECTION IS PRINCIPLED, NOT A MAGIC THRESHOLD: the EGX enforces a daily price
limit (circuit breaker) around +/-20%. Empirically every clean EGX name in our
25-name universe tops out at |log move| <= 0.223. A single-session move beyond
that is not reachable by trading — it can only be a corporate action or a data
error. The 0.35 threshold sits well clear of the limit AND well clear of the
largest plausible ex-dividend drop (a 29.5% single-payment yield), so genuine
ex-div gaps -- which the engine SHOULD see, since it forecasts price and its
carry anchor is rf - q -- are never touched.

Repair is a standard back-adjustment: scale all prior O/H/L/C by the observed
ratio so the artifact day's return becomes zero.
"""
import numpy as np
import pandas as pd

# Exchange daily price limits (circuit breakers). A single-session move beyond the
# limit is NOT reachable by trading — it can only be a corporate action or a data
# error. This is the principled basis for artifact detection, and it is PER-MARKET:
# a global threshold is wrong. KOSPI's limit is +/-30%, so a legitimate Korean
# limit-down day is log(0.70) = -0.357 — which an EGX-calibrated threshold of 0.35
# would have falsely "repaired". (Caught 11-Jul-2026 on the Korea ingest.)
DAILY_LIMIT = {
    'EG': 0.20,   # EGX
    'SA': 0.10,   # Tadawul
    'AE': 0.15,   # ADX / DFM
    'QA': 0.10,   # Qatar Exchange
    'KR': 0.30,   # KOSPI
    'IN': 0.20,   # NSE (banded 5/10/20)
    'US': None,   # no single-stock limit — real -40% earnings crashes happen
    'GB': None,
    'BR': None,
    'XAU': None,  # spot metal, no limit
    'XPT': None,  # spot metal, no limit
}
NO_LIMIT_THRESHOLD = 0.70   # markets without a limit: only a >50% one-day move is suspect
LIMIT_SAFETY = 1.30         # margin above the limit before we call it an artifact


def jump_threshold(market):
    lim = DAILY_LIMIT.get(market)
    if lim is None:
        return NO_LIMIT_THRESHOLD
    return abs(np.log(1 - lim)) * LIMIT_SAFETY


def clean_ohlc(df, ticker="", verbose=True, market=None):
    df = df.copy().reset_index(drop=True)
    log = []

    # --- 1. drop non-trading placeholder rows (no volume AND no intraday range) ---
    novol = df['Vol.'].isna() | (df['Vol.'].astype(str).str.strip().isin(['', 'nan', 'None', '-']))
    flat = (df['High'] == df['Low'])
    placeholder = novol & flat
    if placeholder.any():
        # only strip a LEADING placeholder block (pre-listing); interior halts are real
        first_real = int((~placeholder).idxmax())
        lead = placeholder.iloc[:first_real].sum()
        if lead:
            log.append(f"dropped {lead} leading pre-listing placeholder rows "
                       f"(flat price, no volume) before {df['Date'].iloc[first_real].date()}")
            df = df.iloc[first_real:].reset_index(drop=True)
        interior = placeholder.sum() - lead
        if interior:
            df = df[~(df['Vol.'].isna() & (df['High'] == df['Low']))].reset_index(drop=True)
            log.append(f"dropped {interior} interior stale/no-trade rows")

    # --- 2. detect + back-adjust unadjusted corporate actions ---
    thr = jump_threshold(market)
    for _ in range(6):  # iterate: repairing one can reveal another
        p = df['Price'].values
        lr = np.diff(np.log(p))
        hits = np.where(np.abs(lr) > thr)[0]
        if len(hits) == 0:
            break
        i = int(hits[0])                       # index of the day BEFORE the break
        factor = p[i + 1] / p[i]               # scale prior history onto the new basis
        d = df['Date'].iloc[i + 1].date()
        for c in ['Price', 'Open', 'High', 'Low']:
            df.loc[:i, c] = df.loc[:i, c] * factor
        log.append(f"back-adjusted {i+1} rows before {d} by x{factor:.4f} "
                   f"(raw 1-day log move {lr[i]:+.3f} exceeds the {market or '?'} "
                   f"artifact threshold {thr:.3f} — not reachable by trading)")

    if verbose and log:
        print(f"  [{ticker}] " + f"\n  [{ticker}] ".join(log))
    return df, log


def screen(df):
    """Post-clean sanity metrics."""
    lr = np.diff(np.log(df['Price'].values))
    return dict(rows=len(df), max_abs_log=float(np.abs(lr).max()),
                flat_frac=float((np.abs(lr) < 1e-9).mean()))
