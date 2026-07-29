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

    # --- 1b. drop non-positive OHLC rows ---------------------------------------
    # A zero or negative price is not a tradeable quote; it is a vendor fill. It MUST
    # be removed before step 2, because step 2 takes log(price) and divides by it.
    #
    # Why this exists (26-Jul-2026, EG 15-year library ingest): 22 rows across 10 of
    # 32 series carried a zero OHLC value, 7 of them on a single market-wide date
    # (2013-05-07: CCAP, HRHO, KABO, LCSW, OCDI, OIH, TMGH). Without this guard,
    # log(0) = -inf trips the artifact threshold, and the repair below computes
    # factor = p[i+1]/p[i] = x/0 -> inf. The gate then back-adjusted entire histories
    # by x0.0000 and then by xinf, destroying pre-2013 data for NINE names while
    # REPORTING SUCCESS. Same failure class as the nu=Gaussian incident: it survives
    # every check that is not a numerical inspection of the output.
    #
    # Interior rows only -- a leading block is already handled by step 1. Dropping
    # (not interpolating) is deliberate: a session with no valid price contributes no
    # information, and synthesising one invents a trade that never happened.
    px = ['Price', 'Open', 'High', 'Low']
    # Cast to float BEFORE any repair. The step-2 back-adjust multiplies a price
    # column by a fractional factor; on an integer-dtype column (Korean prices are
    # whole KRW, so pandas infers int64) that raises LossySetitemError and the gate
    # DIES mid-repair. Never bit before because EG/AE/QA/SA/US/XAU prices all carry
    # decimals and parse as float. Found 27-Jul-2026 on the Samsung 15-year ingest.
    df[px] = df[px].astype(float)
    bad = (df[px] <= 0).any(axis=1) | ~np.isfinite(df[px]).all(axis=1)
    if bad.any():
        dates = df['Date'][bad]
        log.append(f"dropped {int(bad.sum())} rows carrying a non-positive or "
                   f"non-finite OHLC value ({dates.iloc[0].date()}"
                   f"{'..' + str(dates.iloc[-1].date()) if bad.sum() > 1 else ''}) "
                   f"— vendor fills, not tradeable prices")
        df = df[~bad].reset_index(drop=True)

    # --- 1c. drop single-session artifacts that CANCEL the next session --------
    # A session beyond the market's own daily limit cannot be genuine trading —
    # that much is already step 2's premise below. The question step 2 gets
    # wrong is WHICH such jumps are a real, PERMANENT corporate action (back-
    # adjust everything before it) versus a TEMPORARY data error (drop it, adjust
    # nothing). A genuine split does not reverse itself the next session; a data
    # error does. That cancellation -- jump_out =~ -jump_in -- is the actual
    # diagnostic, not whether the row happens to be flat.
    #
    # Found 29-Jul-2026, two different shapes of the same underlying bug:
    #   - Kakao/Samsung/NVDA: FLAT rows (O=H=L=Price), tiny non-empty volume,
    #     recurring roughly weekly across years of history (230/31/1 rows).
    #     novol & flat (step 1) misses these because volume is non-empty.
    #   - Qatar (QGTS/IQCD/QNB): NOT flat -- real intraday range, real volume
    #     (tens of millions), ~10x/~9x/~13x the true level for exactly one
    #     session, on the SAME calendar date (19-Nov-2013) across three
    #     unrelated names -- a one-day vendor feed error, not three
    #     independent corporate actions.
    # Either way, step 2's repair loop (below) treats the first few it meets as
    # genuine splits and back-adjusts all prior history by a bogus factor; with
    # Kakao's ~230 repeats it exhausts its 6-iteration cap and leaves most of
    # them to silently corrupt every HAR fit trained across that history.
    thr_pre = jump_threshold(market)
    p = df['Price'].values
    n = len(df)
    phantom = np.zeros(n, dtype=bool)
    if n > 2:
        with np.errstate(divide='ignore', invalid='ignore'):
            jump_in = np.log(p[1:-1] / p[:-2])     # signed, into row i, i=1..n-2
            jump_out = np.log(p[2:] / p[1:-1])     # signed, out of row i
        # a genuine multi-day rally has jump_in and jump_out the SAME sign (keeps
        # moving); a data error cancels (jump_out =~ -jump_in) -- normal next-day
        # drift is allowed for (0.15 log-unit slack), it just can't be a second
        # jump in the same direction.
        cand = (np.abs(jump_in) > thr_pre) & (np.abs(jump_in + jump_out) < 0.15)
        phantom[1:-1] = cand
    if phantom.any():
        dates = df['Date'][phantom]
        log.append(f"dropped {int(phantom.sum())} single-session rows that cancel "
                   f"the very next session ({dates.iloc[0].date()}.."
                   f"{dates.iloc[-1].date()}) — each exceeds the {market or '?'} "
                   f"artifact threshold then reverses almost exactly the next close "
                   f"(jump_out =~ -jump_in); a genuine corporate action does not "
                   f"cancel like this, so these are dropped rather than back-adjusted")
        df = df[~phantom].reset_index(drop=True)

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
        # Defence in depth: step 1b should make this unreachable, but a factor that is
        # not finite and strictly positive can only corrupt the series, never repair it.
        if not np.isfinite(factor) or factor <= 0:
            log.append(f"ABORTED repair at {df['Date'].iloc[i + 1].date()}: "
                       f"non-finite/non-positive factor from p={p[i]:.6g}->{p[i+1]:.6g}")
            break
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
