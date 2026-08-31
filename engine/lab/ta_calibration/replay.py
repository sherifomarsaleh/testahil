"""replay.py — walk-forward replay of the SHIPPED technical read, 15 years.

WHAT THIS ANSWERS
-----------------
The Monte Carlo lens is calibrated because every cone is struck, frozen, dated
and graded: `in90` in a panel row is a fact about a claim that was actually
made. The technical lens makes claims too — a resistance is "the next level
price has to deal with", a bull trigger says a close above R1 "would open the
R3 zone" — but it records none of them. It is regenerated every pass and is
idempotent, so there is no frozen claim to grade and nothing has ever been
scored.

With 15 years of library there is no need to wait for a record to accrue.
`technicals.compute()` is a pure function of the cleaned series up to a date,
so it can be re-run at every historical origin on a truncated library and the
claims it WOULD have published are graded against what actually happened.

THE READ IS RE-RUN, NEVER RE-IMPLEMENTED. Every claim below comes out of the
shipped `technicals.compute()` via its `frame=` injection. A replay that
re-derived the levels would be scoring a different read from the one that
ships — the [R-ENF-03] lesson (a checker that models the parser is checking a
different file), in Python rather than JS.

THE NULL IS THE POINT, NOT THE HIT RATE
---------------------------------------
"Price touched R1 in 68% of windows" is a statement about volatility, not about
R1. Every claim here is scored against a DISTANCE-MATCHED NON-STRUCTURAL
PLACEBO: a price on the same side, at as close to the same distance as can be
found while sitting at least CLUSTER_TOL away from every charted cluster and
every published level. That holds the mechanical part (how far price travels in
three months) constant and varies only the thing the technical read claims to
know — that THIS price is special. It is the same shape as the engine's own
w90/w90_b: our number is only meaningful beside the naive one.

LOOK-AHEAD
----------
The library is cleaned ONCE and then sliced, which is the same convention
panel_refresh uses to build the MC panels. Step 0.0's back-adjustment is
multiplicative over the whole pre-event history, and every claim scored here is
a RATIO (a level as a fraction of spot, RSI, ATR%), so the adjustment cancels.
No indicator reads a bar after its origin.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd

ENGINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)

import technicals as T                                    # noqa: E402
from strike_cohorts import load_clean                     # noqa: E402

# Replay grid. 21 sessions ~ one month: the cadence the roll-forward actually
# republishes a technical read on, so the replay strikes claims as often as
# production does. Origins overlap at the 3-month horizon by construction; the
# block bootstrap below is what handles that, not a thinned grid.
STEP = 21
MIN_HISTORY = 520          # 500 pivot lookback + slack, so the read is never degraded
HORIZON_MONTHS = (1, 3)

# SHORT HORIZONS — THE TECHNICAL LENS'S OWN CLOCK.
# The first pass scored the technical read at 1 and 3 calendar months. That is
# the MC lens's horizon, not this one: in this project the technical read is the
# under-one-month view, the cone owns 1-3 months and the fundamental study owns
# the year. Scoring a short-term read against a quarterly outcome measures the
# wrong thing, and it also throttled the evidence — non-overlapping quarterly
# windows yield about 60 tests per name, against the ~560 a 3-4pp effect needs,
# which is why the first pass concluded a level record could never be per name.
# At a one-week horizon fifteen years yields roughly 750 non-overlapping tests
# per name. The limit was the horizon, not the level.
HORIZON_SESSIONS = (5, 10, 21)      # ~1 week, ~2 weeks, ~1 month
SHORT_STEP = 5                      # weekly origins; windows at h=5 barely overlap


# ----------------------------------------------------------------- utilities
def _grade_index(dates: pd.Series, i: int, months: int):
    """First session on/after origin + N calendar months, month-end clamped.

    Same commitment horizons.resolve() makes, evaluated on the name's OWN
    sessions — which is the grid a claim about this name would be graded on.
    """
    tgt = pd.Timestamp(dates.iloc[i]) + pd.DateOffset(months=months)
    j = int(np.searchsorted(dates.values, np.datetime64(tgt), side='left'))
    return j if j < len(dates) else None


# TWO-SIDED, CENTRED BY CONSTRUCTION. The published level is itself banned, so
# a placebo can never sit at exactly its distance and every single-sided search
# is offset — the first cut walked inward first and drew placebos 1.4% to 4.3%
# nearer than the levels they stood in for, which is enough on its own to make
# structure look real (a nearer price is touched more and broken more for
# reasons that have nothing to do with the chart). Alternating the pair order
# by row narrowed that offset but did not close it, because the two sides do
# not survive the ban at equal rates.
#
# So the null is a PAIR: the nearest admissible non-level inside the published
# distance and the nearest one outside it, scored and then averaged. Whatever
# the step, the pair straddles the real distance, so the comparison is centred
# by construction rather than by hoping two searches balance. Rows where only
# one side is admissible are recorded with n_sides=1 and can be excluded.
_PLACEBO_STEPS = (0.07, 0.13, 0.19, 0.25, 0.33)


def _placebo_pair(level: float, spot: float, above: bool, banned: list[float]):
    """(inward, outward) non-level prices straddling the published distance."""
    d = abs(level - spot) / spot
    out = []
    for sign in (-1.0, +1.0):
        hit = None
        for step in _PLACEBO_STEPS:
            mult = 1.0 + sign * step
            if mult <= 0:
                continue
            cand = spot * (1 + d * mult) if above else spot * (1 - d * mult)
            if all(abs(cand - b) / spot > T.CLUSTER_TOL for b in banned):
                hit = (float(cand), float(d * mult))
                break
        out.append(hit)
    return out


def _volume(series):
    """Vendor volume strings ('2.87M', '640.00K') to floats. NaN where absent."""
    v = series.astype(str).str.strip().str.replace(',', '', regex=False)
    mult = v.str[-1].map({'K': 1e3, 'M': 1e6, 'B': 1e9})
    num = pd.to_numeric(v.str.rstrip('KMB'), errors='coerce')
    return (num * mult.fillna(1.0)).where(num.notna())


def _placebo_ladder(near, far, spot, above, banned):
    """A two-rung ladder at the same distances, moved together off structure.

    The bull trigger is a claim about a PAIR of levels — close above the near
    one and the far one opens — so its null has to be a pair too, and the gap
    between the rungs has to survive the move. Scaling both by one factor keeps
    the near/far ratio exactly and shifts the whole ladder off charted
    structure; scaling them independently would change the very thing the claim
    is about.
    """
    dn = abs(near - spot) / spot
    dfar = abs(far - spot) / spot
    # A wide, symmetric grid. The first cut offered six offsets and only 6% of
    # origins found a pair clearing every charted level on both rungs, which
    # would have made this the thinnest claim in the set for a reason that is
    # about the search, not about the market.
    grid = []
    for step in (0.08, 0.14, 0.20, 0.27, 0.34, 0.42, 0.50):
        grid += [1 + step, 1 - step]
    for m in grid:
        pn = spot * (1 + dn * m) if above else spot * (1 - dn * m)
        pf = spot * (1 + dfar * m) if above else spot * (1 - dfar * m)
        if all(abs(pn - b) / spot > T.CLUSTER_TOL for b in banned) and \
           all(abs(pf - b) / spot > T.CLUSTER_TOL for b in banned):
            return float(pn), float(pf), float(m)
    return None, None, None


def _trigger(fc, fh, fl, near, far, above):
    """Did the trigger fire, and did the far rung then open?

    'A daily close back above R1 would clear the nearest resistance and open the
    R3 zone' is the only explicitly CONDITIONAL forecast the read makes, and the
    grading has to respect the order: the far rung must be reached AFTER the
    close that fired the trigger, not merely somewhere in the window.
    """
    fired = (fc >= near) if above else (fc <= near)
    if not fired.any():
        return False, None
    k = int(np.argmax(fired))                     # first firing close
    rest_h, rest_l = fh[k + 1:], fl[k + 1:]
    if not len(rest_h):
        return True, False
    opened = bool((rest_h >= far).any()) if above else bool((rest_l <= far).any())
    return True, opened


def _all_structure(high, low, close, spot):
    """Every charted cluster the read could have drawn on, for placebo exclusion.

    Uses the module's own pivot/cluster helpers at the module's own constants,
    so 'not at structure' means what technicals.py means by it. These build the
    NULL only — no claim is derived from them.
    """
    lb = min(T.PIVOT_LOOKBACK, len(high))
    ph, pl = T._fractal_pivots(high[-lb:], low[-lb:])
    lv = [c['level'] for c in T._cluster(ph, lb) + T._cluster(pl, lb)]
    for w in T.MA_WINDOWS:
        m = T._sma(close, w)
        if m is not None:
            lv.append(m)
    win = min(252, len(high))
    lv += [float(high[-win:].max()), float(low[-win:].min())]
    return lv


# -------------------------------------------------------------------- harvest
def harvest_short(market: str, ticker: str, step: int = SHORT_STEP,
                  horizons=HORIZON_SESSIONS, frame=None):
    """The same claims, graded on the technical lens's own clock.

    Identical to harvest() except the forward window is counted in SESSIONS
    rather than calendar months, and origins are weekly. The read itself is
    still the shipped technicals.compute(), re-run and never re-implemented.
    """
    df, rep = load_clean(market, ticker) if frame is None else frame
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    high = df['High'].to_numpy(dtype=float)
    low = df['Low'].to_numpy(dtype=float)
    vol = _volume(df['Vol.']).to_numpy(dtype=float) if 'Vol.' in df.columns else None
    n = len(df)
    hmax = max(horizons)

    rows = []
    for i in range(MIN_HISTORY, n - hmax - 1, step):
        try:
            st = T.compute(market, ticker,
                           frame=(df.iloc[:i + 1].reset_index(drop=True), rep))
        except ValueError:
            continue
        spot = st['close']
        struct = _all_structure(high[:i + 1], low[:i + 1], close[:i + 1], spot)
        published = [float(x) for x in st['levels']['res'] + st['levels']['sup']]
        # VOLUME IS IN EVERY LIBRARY AND THE READ HAS NEVER LOOKED AT IT.
        # Carried here as a trailing-60 z-score of log volume, walk-forward safe
        # (the window ends at the origin), so the claim families below can be
        # tested against it without the technical read asserting anything yet.
        vz = np.nan
        if vol is not None and i >= 60:
            w = np.log(vol[i - 59:i + 1])
            w = w[np.isfinite(w)]
            if len(w) >= 30 and w.std(ddof=1) > 0:
                vz = float((np.log(vol[i]) - w.mean()) / w.std(ddof=1)) \
                    if np.isfinite(vol[i]) and vol[i] > 0 else np.nan
        base = dict(market=market, ticker=ticker,
                    origin=dates.iloc[i].date().isoformat(), origin_idx=i, spot=spot,
                    rsi=st['rsi'], atr_pct=st['atr_pct'],
                    trend=st['tech']['trend'].split(';')[0],
                    macd_hist=(st['macd'] or {}).get('hist'),
                    cross_ago=(st['ma_cross'] or {}).get('ago'),
                    cross_kind=(st['ma_cross'] or {}).get('kind'),
                    vol_z=vz,
                    # 52-week position and MA slope state: both are published on
                    # every page and neither had ever been scored.
                    off_high=st.get('pct_off_high'), off_low=st.get('pct_off_low'),
                    slope20=(st['ma_slope'] or {}).get(20),
                    slope50=(st['ma_slope'] or {}).get(50),
                    slope200=(st['ma_slope'] or {}).get(200))

        for h in horizons:
            g = i + h
            if g >= n:
                continue
            fh, fl, fc = high[i + 1:g + 1], low[i + 1:g + 1], close[i + 1:g + 1]
            if not len(fc):
                continue
            fwd_ret = float(fc[-1] / spot - 1.0)
            rlz_vol = (float(np.std(np.diff(np.log(close[i:g + 1])), ddof=1) * np.sqrt(252))
                       if g - i > 2 else np.nan)
            for side, above in (('res', True), ('sup', False)):
                # KIND AND TOUCH COUNT COME ALONG. technicals.py ranks a swing
                # cluster ABOVE a moving average, a 52-week extreme and a round
                # number, and weights a level by how many times it was tested.
                # Both are assumptions the module makes about itself and neither
                # had ever been checked; level_detail carries them in the same
                # order as the published ladder.
                detail = st['level_detail'][side]
                for rank, lv in enumerate(st['levels'][side], start=1):
                    lv = float(lv)
                    dk = detail[rank - 1] if rank - 1 < len(detail) else {}
                    pair = _placebo_pair(lv, spot, above, struct + published)
                    got = [p for p in pair if p is not None]
                    if not got:
                        continue
                    hit = (lambda x: (fh >= x).any()) if above else (lambda x: (fl <= x).any())
                    thr = (lambda x: (fc >= x).any()) if above else (lambda x: (fc <= x).any())
                    pt = [(pp, dd) for pp, dd in got if hit(pp)]
                    rows.append(dict(base, h=h, claim='level', side=side, rank=rank,
                                     kind=dk.get('kind'), touches=dk.get('touches'),
                                     level=lv, dist=abs(lv - spot) / spot,
                                     placebo_dist=float(np.mean([dd for _, dd in got])),
                                     n_sides=len(got),
                                     touched=bool(hit(lv)), broke=bool(thr(lv)),
                                     p_touched=bool(len(pt)),
                                     p_broke=(float(np.mean([thr(pp) for pp, _ in pt]))
                                              if pt else np.nan),
                                     p_touch_dist=(float(np.mean([dd for _, dd in pt]))
                                                   if pt else np.nan),
                                     fwd_ret=fwd_ret, rlz_vol=rlz_vol))
            for side, above in (('res', True), ('sup', False)):
                lad = [float(x) for x in st['levels'][side]]
                if len(lad) < 2:
                    continue
                near, far = lad[0], lad[-1]
                pn, pf, mult = _placebo_ladder(near, far, spot, above,
                                               struct + published)
                if pn is None:
                    continue
                fired, opened = _trigger(fc, fh, fl, near, far, above)
                p_fired, p_opened = _trigger(fc, fh, fl, pn, pf, above)
                rows.append(dict(base, h=h, claim='trigger', side=side, rank=None,
                                 level=near, dist=abs(near - spot) / spot,
                                 placebo_dist=abs(pn - spot) / spot, n_sides=int(mult * 100),
                                 touched=fired, broke=opened,
                                 p_touched=p_fired, p_broke=p_opened,
                                 p_touch_dist=abs(far - spot) / spot,
                                 fwd_ret=fwd_ret, rlz_vol=rlz_vol))
            rows.append(dict(base, h=h, claim='state', side=None, rank=None, level=None,
                             dist=None, placebo_dist=None, n_sides=None, touched=None,
                             broke=None, p_touched=None, p_broke=None, p_touch_dist=None,
                             fwd_ret=fwd_ret, rlz_vol=rlz_vol))
    return pd.DataFrame(rows)


def harvest(market: str, ticker: str, step: int = STEP, verbose=False, frame=None):
    """Every claim the shipped read would have published, graded on the tape.

    ``frame`` accepts a pre-loaded (df, rep) already through Step 0.0, so an
    alternative export can be scored without being written into the persistent
    library. Nothing under raw_ohlc/ is read or touched when it is supplied.
    """
    df, rep = load_clean(market, ticker) if frame is None else frame
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    high = df['High'].to_numpy(dtype=float)
    low = df['Low'].to_numpy(dtype=float)
    n = len(df)

    rows = []
    for i in range(MIN_HISTORY, n - 1, step):
        grades = {m: _grade_index(dates, i, m) for m in HORIZON_MONTHS}
        if grades[max(HORIZON_MONTHS)] is None:
            break
        try:
            st = T.compute(market, ticker, frame=(df.iloc[:i + 1].reset_index(drop=True), rep))
        except ValueError:
            continue

        spot = st['close']
        struct = _all_structure(high[:i + 1], low[:i + 1], close[:i + 1], spot)
        published = [float(x) for x in st['levels']['res'] + st['levels']['sup']]

        base = dict(market=market, ticker=ticker, origin=dates.iloc[i].date().isoformat(),
                    origin_idx=i, spot=spot,
                    rsi=st['rsi'], atr_pct=st['atr_pct'],
                    trend=st['tech']['trend'].split(';')[0],
                    macd_hist=(st['macd'] or {}).get('hist'),
                    cross_ago=(st['ma_cross'] or {}).get('ago'),
                    cross_kind=(st['ma_cross'] or {}).get('kind'))

        for months, g in grades.items():
            if g is None:
                continue
            fh = high[i + 1:g + 1]
            fl = low[i + 1:g + 1]
            fc = close[i + 1:g + 1]
            if not len(fc):
                continue
            fwd_ret = float(fc[-1] / spot - 1.0)
            rlz_vol = float(np.std(np.diff(np.log(close[i:g + 1])), ddof=1) * np.sqrt(252)) \
                if g - i > 2 else np.nan

            for side, key in (('res', True), ('sup', False)):
                for rank, lv in enumerate(st['levels'][side], start=1):
                    lv = float(lv)
                    pair = _placebo_pair(lv, spot, key, struct + published)
                    got = [p for p in pair if p is not None]
                    if not got:
                        continue
                    hit = (lambda x: (fh >= x).any()) if key else (lambda x: (fl <= x).any())
                    thr = (lambda x: (fc >= x).any()) if key else (lambda x: (fc <= x).any())
                    # A placebo only enters the average when it was actually
                    # reached; comparing a touched level against an untouched
                    # null would score the distance, not the structure.
                    pt = [(pp, dd) for pp, dd in got if hit(pp)]
                    rows.append(dict(base, months=months, claim='level', side=side,
                                     rank=rank, level=lv, dist=abs(lv - spot) / spot,
                                     placebo_dist=float(np.mean([dd for _, dd in got])),
                                     n_sides=len(got),
                                     touched=bool(hit(lv)), broke=bool(thr(lv)),
                                     p_touched=bool(len(pt)),
                                     p_broke=(float(np.mean([thr(pp) for pp, _ in pt]))
                                              if pt else np.nan),
                                     p_touch_dist=(float(np.mean([dd for _, dd in pt]))
                                                   if pt else np.nan),
                                     fwd_ret=fwd_ret, rlz_vol=rlz_vol))

            rows.append(dict(base, months=months, claim='state', side=None, rank=None,
                             level=None, dist=None, placebo_dist=None, n_sides=None,
                             touched=None, broke=None, p_touched=None, p_broke=None,
                             p_touch_dist=None,
                             fwd_ret=fwd_ret, rlz_vol=rlz_vol))
        if verbose and i % (step * 20) == 0:
            print(f'  {ticker} {dates.iloc[i].date()} ({i}/{n})', flush=True)
    return pd.DataFrame(rows)


if __name__ == '__main__':
    mkt = sys.argv[1] if len(sys.argv) > 1 else 'EG'
    tkr = sys.argv[2] if len(sys.argv) > 2 else 'COMI'
    r = harvest(mkt, tkr, verbose=True)
    print(r.head())
    print(len(r), 'claim rows')
