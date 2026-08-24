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

    # --- 1c. drop ISOLATED one-row price spikes (vendor phantom split prints) ---
    # A corporate action moves the price to a NEW LEVEL and it STAYS there. A vendor
    # phantom print spikes for exactly one row and reverts on the next. That single
    # distinction separates them, and it needs no exchange calendar to apply.
    #
    # Why this exists (28-Jul-2026, KR 15-year Kakao/Samsung ingest): investing.com's
    # Korean exports carry rows whose "Change %" is literally the split ratio
    # ("4,900.00%" = 50x-1; "400.00%" = 5x-1), with O=H=L=C and volume "0.00K".."0.09K".
    # They survive step 1 ONLY because that volume string is non-NaN, so `novol` is
    # False. Step 2 then back-adjusts the whole history INTO the spike, and on the next
    # iteration back-adjusts it OUT again — an oscillation that cannot converge. It
    # burns all 6 iterations and leaves the series on an arbitrary scale, silently:
    # the fresh Samsung export disagreed with the correctly-cleaned library on 1,195 of
    # 3,709 shared sessions, max abs diff 1,574,782 KRW.
    #
    # This was patched BY HAND twice before it was understood as a class — the 10-Jul
    # KAKAO 5:1 finding and the 27-Jul SAMSUNG 50:1 finding, both fixed by editing the
    # raw CSV. Hand-editing does not scale and is not reproducible: the 15-year Kakao
    # file carries 230 such rows against Samsung's 41.
    #
    # GENERALISED 28-Jul-2026 on the QA 15-year ingest: the same artifact appears in
    # Qatar WITHOUT the flat-bar signature. Every QE name carries a single 2013-11-19
    # row printed on the pre-10:1-split scale — IQCD 16.89 -> 168.00 -> 16.85, with a
    # full intraday range (H 169.50 / L 167.90) and inflated volume — so the original
    # flat-bar test missed all three. A +894% session on an exchange with a +/-10%
    # daily limit is 22x the limit: it is not trading, whatever the bar looks like.
    #
    # DROPPED, not rescaled — consistent with the 27-Jul decision. Rescaling a print
    # from a session the market never held would synthesise a trade that never happened.
    p = df['Price'].values.astype(float)
    if len(p) >= 3:
        lr = np.diff(np.log(p))
        # row i+1 is a spike if the move INTO it and OUT of it both exceed the
        # artifact threshold and have OPPOSITE signs (it goes up then straight back
        # down, or vice versa). A real split has one move and no reversal.
        thr0 = jump_threshold(market)
        into, outof = lr[:-1], lr[1:]
        spike = (np.abs(into) > thr0) & (np.abs(outof) > thr0) & (np.sign(into) != np.sign(outof))
        # The round trip must very nearly cancel: a one-row excursion returns to
        # where it started. This is what separates a scale artifact from two
        # unrelated large moves that happen to be adjacent.
        round_trip = np.abs(into + outof) < thr0
        # In a market WITH a statutory daily price limit, an excursion this large
        # cannot be trading in either direction, whatever the row looks like — so
        # the intraday-range test is not required. Where there is NO limit
        # (US equities, spot metals) a violent crash-and-rebound is at least
        # conceivable, so there we still demand the tell-tale non-trade signature
        # of a completely flat bar.
        has_limit = DAILY_LIMIT.get(market) is not None
        flat_row = (df['High'].values == df['Low'].values)[1:-1]
        drop = np.zeros(len(df), dtype=bool)
        drop[1:-1] = spike & round_trip & (True if has_limit else flat_row)

        # SECOND SIGNATURE — THE UNREACHABLE FLAT BAR (24-Aug-2026, JUFO ingest).
        # The test above asks whether a move beats jump_threshold(), which carries a
        # 1.30 safety margin AND applies the DOWN-limit magnitude |ln(1-lim)| to moves
        # in BOTH directions. On EGX that means an UP move goes unquestioned until
        # +25.0%, while the exchange's own up-limit is +20% — a blind spot exactly one
        # bonus-issue ratio wide. Juhayna's 2026-04-12 row sat in it: a single bar the
        # vendor's 5:4 adjustment pass skipped, +25.00% into it and -19.67% straight
        # back out. Neither leg cleared 0.290, so step 1c passed it, step 2 passed it,
        # and it carried JUFO's 250-day realized vol from 31.9% to 44.7% — a 40%
        # overstatement of the volatility that sizes the published cone.
        #
        # The distinguishing fact is not the SIZE of the move, it is that the bar is
        # UNREACHABLE: it has no intraday range at all (H == L) and the move INTO it
        # exceeds the exchange's daily limit IN THE DIRECTION TRAVELLED. No sequence of
        # trades reaches that price, and the next session goes straight back. A real
        # corporate action moves to a new level and STAYS; a real limit session has a
        # RANGE. Same class as the 10-Jul KAKAO, 27-Jul SAMSUNG and 28-Jul IQCD
        # findings — closed as a class, per the standing enforcement rule, rather than
        # by editing one more raw CSV by hand.
        #
        # Deliberately additive and deliberately narrow: it can only ever drop MORE
        # rows, and only zero-range ones that are both unreachable and immediately
        # reversed. Negative-controlled 24-Aug-2026 across every covered series in
        # every market: it drops exactly one row anywhere in the repo — this one.
        lim = DAILY_LIMIT.get(market)
        if lim is not None:
            up_lim, dn_lim = np.log(1.0 + lim), abs(np.log(1.0 - lim))
            unreachable = np.where(into > 0, into > up_lim, -into > dn_lim)
            reverses = np.sign(into) != np.sign(outof)
            drop[1:-1] |= unreachable & reverses & round_trip & flat_row

        if drop.any():
            dts = df['Date'][drop]
            log.append(f"dropped {int(drop.sum())} isolated one-row price spikes "
                       f"({dts.iloc[0].date()}"
                       f"{'..' + str(dts.iloc[-1].date()) if drop.sum() > 1 else ''}) "
                       f"— excursions beyond what {market or '?'} trading can reach "
                       f"that reverse on the very next session: vendor "
                       f"phantom prints, not corporate actions (dropped, not rescaled)")
            df = df[~drop].reset_index(drop=True)

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
