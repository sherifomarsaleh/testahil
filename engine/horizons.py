"""horizons.py — calendar-anchored forecast horizons (1 month / 3 months).

ADOPTED 27-Jul-2026 (user decision), retiring the session-counted convention.
Every horizon Testahil publishes is a CALENDAR horizon: one month and three
months. Cohorts struck before the changeover are graded on the window they
were issued for and their published numbers are never retro-edited — the
Calibration Ledger is append-only — but their horizons are NAMED in calendar
terms like every other row. Session-counted labels appear nowhere.

WHY THIS MODULE EXISTS
----------------------
"One month" and "three months" are calendar objects. The Monte-Carlo engine
steps in TRADING SESSIONS. Something has to map one onto the other, and the
mapping is not a constant: a calendar month is 18-23 sessions on the EGX and
19-24 on the metals calendar, and a calendar quarter ranges 55-67 sessions
across the markets Testahil covers. Hard-coding "1 month = 21 sessions" would
reproduce, with a calendar label, exactly the session-counting the change was
meant to remove — which is the mismatch the metals rows already carried
("1 month" labels sitting on 28-calendar-day, session-derived grade dates).

THE CONVENTION (single definition, used by publish AND by grading)
------------------------------------------------------------------
  target_date  = anchor_date + N calendar months, month-end clamped
                 (31-Jan + 1M -> 28/29-Feb; 31-Aug + 1M -> 30-Sep).
  grade_date   = the first REAL trading session on or after target_date on
                 that exchange's own calendar. If the target is a session, it
                 IS the grade date; a holiday or weekend rolls forward, never
                 back.
  h (sessions) = the number of sessions from anchor to grade_date, used to
                 size the cone.

At publish time the grade date lies in the future, so `h` and the grade date
are PROJECTED from the exchange's own realized calendar — never assumed.
Projection error is recorded, not hidden: `resolve()` returns basis='projected'
with the components it used, and basis='realized' once the library covers the
target.

HOW h IS PROJECTED (and what was tested)
----------------------------------------
Three candidate projections were backtested on every market's own realized
calendar, each scored strictly out-of-sample (a probe anchor only ever sees
anchors before it) — see projection_diagnostics():

  density   open weekdays to target x realized sessions-per-open-weekday
  seasonal  median realized h over prior-year anchors within +/-10 days of
            the same day-of-year (captures Eid / Ramadan / Golden Week /
            year-end holiday clustering, which a flat density cannot)
  blend     the average of the two  <- ADOPTED

Scored in SESSIONS, pooled over 9 markets x 2 horizons, the three are close
and disagree by horizon: density 1.083, seasonal 0.879, blend 0.913. Seasonal
wins 3-month in 8 of 9 markets; blend wins 1-month in 6 of 9.

Sessions are the wrong loss function, though. What a wrong h actually costs is
CONE WIDTH, and width scales as sqrt(h) — so one misplaced session is ~2.4% of
the cone at 1M (h~21) but only ~0.8% at 3M (h~63). Scored on that
decision-relevant loss, BLEND wins outright and is adopted: mean width error
1.33% (seasonal 1.39%, density 1.51%) and worst cell 2.84% (seasonal 3.12%,
density 3.18%). One rule, every market, both horizons — no per-horizon pick,
which would be selecting a rule on the sample used to score it, the exact
failure the standing PROMOTION RULE names (CRPS-selected (nu, width_cal)
looked better in-sample and lost under LONO).

Worst-case residual is ~2.8% of cone width, inside the 5% materiality
threshold and an order below the acknowledged (nu, width_cal) identification
uncertainty. It touches the PUBLISHED cone only — grading never uses it.

At GRADE time the projection is irrelevant. Grading reads the real calendar
and grades on the actual first session on or after target_date. Unlike the
retired session rule, a holiday no longer moves the horizon — it only moves
which session the horizon lands on, by at most a few days. That is the whole
point of the change: the grade date is now determined by the calendar, not by
counting sessions the projection did not know about.

CALENDAR SOURCE
---------------
Each market's trading calendar is the UNION of session dates across every
series in engine/raw_ohlc/{MARKET}/, passed through the Step 0.0
data-quality gate first (data_quality.clean_ohlc) so placeholder / non-trading
rows never enter a calendar. Union, not intersection: a single name being
suspended for a day does not close the exchange. Real closures survive — the
EGX's 2011 shutdown shows up correctly as a ~1-session calendar month.

VERIFY BY IMPORT, NOT BY PARSE (standing rule) — see self_check() at the foot
of this file; `python3 horizons.py` runs it.
"""
from __future__ import annotations

import glob
import os
import sys
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_quality import clean_ohlc          # noqa: E402
from mc_v2 import load_ohlc as _raw_load_ohlc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, 'raw_ohlc')

# The two published horizons. Ledger labels are the human strings.
HORIZONS = (1, 3)
LABEL = {1: "1 month", 3: "3 months"}
SHORT = {1: "1M", 3: "3M"}

# Cohorts struck on or after this date use the calendar convention.
CONVENTION_CHANGEOVER = pd.Timestamp("2026-07-27")

# Density is measured over a trailing window so a market that changed its
# trading week (ADX/DFM moved Sun-Thu -> Mon-Fri in Jan-2022) is described by
# the week it actually keeps now, not by a decade-old average.
DENSITY_LOOKBACK_YEARS = 3
WEEKMASK_LOOKBACK_YEARS = 2
# A weekday counts as part of the trading week if it carries at least this
# share of the busiest weekday's sessions. Well separated in practice: real
# trading days sit near 1.0, closed days near 0.0.
WEEKDAY_MIN_SHARE = 0.25
# Seasonal leg of the h projection: how close in day-of-year a prior anchor
# has to be to count, and how many such anchors are needed before the
# seasonal median is trusted at all.
SEASONAL_WINDOW_DAYS = 10
SEASONAL_MIN_ANCHORS = 5


# ------------------------------------------------------------------ calendar
@lru_cache(maxsize=None)
def trading_calendar(market: str) -> pd.DatetimeIndex:
    """Union of clean session dates across the market's raw_ohlc library."""
    dates: set = set()
    for path in sorted(glob.glob(os.path.join(RAW_DIR, market, '*.csv'))):
        ticker = os.path.splitext(os.path.basename(path))[0]
        try:
            df, _ = clean_ohlc(_raw_load_ohlc(path), ticker,
                               verbose=False, market=market)
        except Exception:
            continue
        dates |= set(pd.to_datetime(df['Date']).dt.normalize())
    if not dates:
        raise ValueError(
            f"no usable raw_ohlc series for market {market!r} — a calendar "
            f"horizon cannot be resolved without the exchange's own sessions")
    return pd.DatetimeIndex(sorted(dates))


@lru_cache(maxsize=None)
def weekmask(market: str) -> str:
    """Empirical 7-char Mon..Sun mask, derived from recent realized sessions."""
    cal = trading_calendar(market)
    cutoff = cal[-1] - pd.DateOffset(years=WEEKMASK_LOOKBACK_YEARS)
    recent = cal[cal >= cutoff]
    counts = np.array([(recent.dayofweek == d).sum() for d in range(7)],
                      dtype=float)
    busiest = counts.max()
    return ''.join('1' if c >= WEEKDAY_MIN_SHARE * busiest else '0'
                   for c in counts)


@lru_cache(maxsize=None)
def session_density(market: str) -> float:
    """Realized sessions per open weekday (holiday load), trailing window."""
    cal = trading_calendar(market)
    cutoff = cal[-1] - pd.DateOffset(years=DENSITY_LOOKBACK_YEARS)
    recent = cal[cal >= cutoff]
    open_days = np.busday_count(recent[0].date(), recent[-1].date(),
                                weekmask=weekmask(market))
    if open_days <= 0:
        return 1.0
    return float(len(recent) - 1) / float(open_days)


# ------------------------------------------------------------------ mapping
def target_date(anchor, months: int) -> pd.Timestamp:
    """anchor + N calendar months, month-end clamped by pandas' DateOffset."""
    return (pd.Timestamp(anchor).normalize()
            + pd.DateOffset(months=int(months)))


def next_session(market: str, date) -> Optional[pd.Timestamp]:
    """First real session on or after `date`; None if beyond the library."""
    cal = trading_calendar(market)
    d = pd.Timestamp(date).normalize()
    i = cal.searchsorted(d, side='left')
    return None if i >= len(cal) else cal[i]


def sessions_between(market: str, start, end) -> Optional[int]:
    """Realized session count from `start` to `end`, both real sessions."""
    cal = trading_calendar(market)
    s = cal.searchsorted(pd.Timestamp(start).normalize(), side='left')
    e = cal.searchsorted(pd.Timestamp(end).normalize(), side='left')
    if s >= len(cal) or e >= len(cal):
        return None
    return int(e - s)


def _projected_next_open(market: str, date) -> pd.Timestamp:
    """Roll `date` forward to the next day inside the market's trading week.

    Trading-week structure only — a projection cannot know future holidays.
    Grading re-resolves against the real calendar, so this is a display target.
    """
    mask = weekmask(market)
    d = pd.Timestamp(date).normalize()
    for _ in range(10):
        if mask[d.dayofweek] == '1':
            return d
        d += pd.Timedelta(days=1)
    return d


@lru_cache(maxsize=None)
def _realized_h(market: str, months: int):
    """Realized (anchor, h) pairs for this span — the seasonal projection's
    only evidence. Returns (DatetimeIndex, h array)."""
    cal = trading_calendar(market)
    hs, ds = [], []
    for i, d in enumerate(cal):
        j = cal.searchsorted(target_date(d, months), side='left')
        if j >= len(cal):
            break
        ds.append(d)
        hs.append(j - i)
    return pd.DatetimeIndex(ds), np.asarray(hs, dtype=int)


def _h_density(market: str, anchor, grade_projected) -> int:
    """Open weekdays to target, discounted by the market's holiday load."""
    open_days = np.busday_count(pd.Timestamp(anchor).date(),
                                pd.Timestamp(grade_projected).date(),
                                weekmask=weekmask(market))
    return max(int(round(open_days * session_density(market))), 1)


def _h_seasonal(market: str, anchor, months: int) -> Optional[int]:
    """Median realized h among prior anchors near the same day-of-year."""
    idx, hs = _realized_h(market, months)
    if len(idx) == 0:
        return None
    anchor = pd.Timestamp(anchor).normalize()
    prior = idx < anchor
    if prior.sum() == 0:
        prior = np.ones(len(idx), dtype=bool)   # no history before: use all
    doy = idx.dayofyear.values
    gap = np.abs(doy - anchor.dayofyear)
    gap = np.minimum(gap, 365 - gap)
    sel = hs[prior & (gap <= SEASONAL_WINDOW_DAYS)]
    return int(np.median(sel)) if len(sel) >= SEASONAL_MIN_ANCHORS else None


def resolve(market: str, anchor, months: int) -> dict:
    """Map (market, anchor, N months) -> grade date + session horizon.

    Returns a dict with:
      target_date  ISO — anchor + N calendar months, month-end clamped
      grade_date   ISO — first session on/after target (real, or projected)
      h            int — sessions from anchor to grade_date
      basis        'realized' when the library already covers the target,
                   'projected' when it does not
      h_density / h_seasonal — the two projection legs, for audit
    """
    anchor = pd.Timestamp(anchor).normalize()
    tgt = target_date(anchor, months)
    cal = trading_calendar(market)

    if tgt <= cal[-1]:
        gd = next_session(market, tgt)
        return dict(target_date=tgt.date().isoformat(),
                    grade_date=gd.date().isoformat(),
                    h=sessions_between(market, anchor, gd),
                    basis='realized', h_density=None, h_seasonal=None)

    gd = _projected_next_open(market, tgt)
    hd = _h_density(market, anchor, gd)
    hs = _h_seasonal(market, anchor, months)
    h = hd if hs is None else int(round((hd + hs) / 2))
    return dict(target_date=tgt.date().isoformat(),
                grade_date=gd.date().isoformat(),
                h=max(h, 1), basis='projected',
                h_density=hd, h_seasonal=hs)


def projection_diagnostics(markets=None, months=(1, 3), warmup=500):
    """Out-of-sample backtest of the three candidate h projections.

    Reproduces the table quoted in this module's docstring. Each probe anchor
    sees ONLY anchors strictly before it, so the seasonal leg is never scored
    on evidence it was fitted to.
    """
    if markets is None:
        markets = sorted(d for d in os.listdir(RAW_DIR)
                         if os.path.isdir(os.path.join(RAW_DIR, d))
                         and glob.glob(os.path.join(RAW_DIR, d, '*.csv')))
    out = []
    for m in markets:
        wm, dens = weekmask(m), session_density(m)
        for mo in months:
            idx, hs = _realized_h(m, mo)
            doy = idx.dayofyear.values
            eD, eS, eB = [], [], []
            for i in range(warmup, len(idx)):
                gd = _projected_next_open(m, target_date(idx[i], mo))
                od = np.busday_count(idx[i].date(), gd.date(), weekmask=wm)
                hd = max(int(round(od * dens)), 1)
                gap = np.abs(doy[:i] - doy[i])
                gap = np.minimum(gap, 365 - gap)
                sel = hs[:i][gap <= SEASONAL_WINDOW_DAYS]
                hsn = (int(np.median(sel))
                       if len(sel) >= SEASONAL_MIN_ANCHORS else hd)
                eD.append(hd - hs[i])
                eS.append(hsn - hs[i])
                eB.append(int(round((hd + hsn) / 2)) - hs[i])
            if not eB:
                continue
            out.append(dict(market=m, months=mo, n=len(eB),
                            mae_density=float(np.abs(eD).mean()),
                            mae_seasonal=float(np.abs(eS).mean()),
                            mae_blend=float(np.abs(eB).mean()),
                            bias_blend=float(np.mean(eB))))
    return pd.DataFrame(out)


def horizon_schedule(market: str, months: int):
    """Callable (origin_date, origin_idx, calendar) -> h, for backtest_v3.

    Used by the walk-forward gate so the horizon it validates is the SAME
    calendar object that gets published, not a fixed 60.
    """
    def _h(date, *_):
        return resolve(market, date, months)['h']
    return _h


def median_h(market: str, months: int) -> int:
    """Median realized session count for this calendar span on this market."""
    cal = trading_calendar(market)
    arr = cal.values
    out = []
    for i, d in enumerate(cal):
        j = cal.searchsorted(target_date(d, months), side='left')
        if j >= len(arr):
            break
        out.append(j - i)
    return int(np.median(out)) if out else 0


# ------------------------------------------------------------------ grading
def cohort_plan(market: str, anchor) -> dict:
    """Everything a new cohort needs from the calendar, for both horizons.

    The single entry point a roll-forward should call — so grade dates and
    session counts are never hand-computed. `h` feeds simulate_paths_v3;
    `grade_date` and `horizon_label` go straight into the ledger row.
    """
    out = dict(market=market,
               anchor_date=pd.Timestamp(anchor).normalize().date().isoformat(),
               convention='calendar (adopted 27-Jul-2026)', horizons={})
    for m in HORIZONS:
        r = resolve(market, anchor, m)
        r['horizon_label'] = LABEL[m]
        r['horizon_days'] = r.pop('h')
        out['horizons'][SHORT[m]] = r
    return out


def grade_target(market: str, anchor, months: int) -> Optional[dict]:
    """Grade-time resolution: the ACTUAL session this horizon lands on.

    Returns None while the horizon has not matured in the library yet, so a
    caller can never accidentally grade against a stale or projected date.
    """
    r = resolve(market, anchor, months)
    if r['basis'] != 'realized':
        return None
    return r


# ------------------------------------------------------------------ check
def self_check(verbose: bool = True) -> bool:
    """Import-time-safe sanity pass over every market with a library."""
    ok = True
    markets = sorted(d for d in os.listdir(RAW_DIR)
                     if os.path.isdir(os.path.join(RAW_DIR, d))
                     and glob.glob(os.path.join(RAW_DIR, d, '*.csv')))
    for m in markets:
        cal = trading_calendar(m)
        wm, dens = weekmask(m), session_density(m)
        h1, h3 = median_h(m, 1), median_h(m, 3)
        # a projected horizon must land near the realized median
        probe = cal[-1]
        p1, p3 = resolve(m, probe, 1), resolve(m, probe, 3)
        bad = (abs(p1['h'] - h1) > 3 or abs(p3['h'] - h3) > 5
               or not (15 <= h1 <= 24) or not (52 <= h3 <= 68))
        ok &= not bad
        if verbose:
            print(f"{m}: n={len(cal)} mask={wm} density={dens:.3f} "
                  f"median h 1M={h1} 3M={h3} | projected from {probe.date()}: "
                  f"1M h={p1['h']} -> {p1['grade_date']}, "
                  f"3M h={p3['h']} -> {p3['grade_date']}"
                  f"{'   <-- CHECK' if bad else ''}")
    return ok


if __name__ == '__main__':
    # python3 horizons.py                    -> self-check every market
    # python3 horizons.py EG 2026-07-27      -> cohort plan for one anchor
    # python3 horizons.py --diagnostics      -> projection backtest table
    argv = sys.argv[1:]
    if argv and argv[0] == '--diagnostics':
        import pandas as _pd
        _pd.set_option('display.width', 200)
        print(projection_diagnostics().to_string(index=False))
        sys.exit(0)
    if len(argv) == 2:
        import json as _json
        print(_json.dumps(cohort_plan(argv[0], argv[1]), indent=2))
        sys.exit(0)
    sys.exit(0 if self_check() else 1)
