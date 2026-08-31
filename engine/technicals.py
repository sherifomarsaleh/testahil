"""technicals.py — deterministic technical read, computed from the library.

WHY THIS EXISTS
---------------
Until 29-Jul-2026 the roll-forward workflow was forbidden from touching a
ticker's ``levels`` (S/R) or ``tech`` (narrative) — both were hand-authored
from a visual chart read, so a price update left them behind. The cost was
real and visible: on 28-Jul-2026 COMI's published spot was 142.00 while its
narrative still read "the price closed 129.25 below a falling 20-day", a
month-stale statement on a live page.

This module replaces the chart read with a reproducible computation over the
same persistent OHLC library the Monte Carlo engine already runs on, so a
price update refreshes the technical read in the same pass and by the same
evidence. Nothing here is fitted or forecast — every number is a closed-form
function of the cleaned series, and every sentence is a template selected by
those numbers. Re-running it on an unchanged library is a no-op.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not editorialize. The retired hand-written narratives sometimes closed
with a fundamental sentence ("the equity case rests on the spread between a
~30% ROE and a ~24% cost of equity"). A deterministic module cannot source
that, so it does not assert it. Fundamental context lives in the study, the
fair-value gauge, and the driver stack — not in the technical block.

Both the Step 0.0 data-quality gate and the per-market daily-limit thresholds
apply here exactly as they do for calibration: no series is read raw.

VERIFY BY IMPORT, NOT BY PARSE — per the standing rule, this module must be
imported (``python3 -c "import technicals"``) before any commit.
"""
from __future__ import annotations

import os
import sys
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from strike_cohorts import load_clean                       # noqa: E402

# ----------------------------------------------------------------- constants
MA_WINDOWS = (20, 50, 200)
RSI_N = 14
ATR_N = 14
SLOPE_LOOKBACK = 10          # sessions used to call an MA rising / falling
SLOPE_FLAT = 0.0030          # |pct change| below this over SLOPE_LOOKBACK = flat
PIVOT_K = 5                  # fractal half-width: a pivot dominates 2k+1 bars
PIVOT_LOOKBACK = 500         # ~2 trading years of structure
CLUSTER_TOL = 0.015          # pivots within 1.5% of each other are one level
MIN_DIST = 0.008             # a level inside 0.8% of the close is not a level
N_LEVELS = 3                 # resistances / supports published per name
RECENCY_HALFLIFE = 180.0     # sessions; pivot weight halves every this many
MACD_FAST, MACD_SLOW, MACD_SIG = 12, 26, 9
CROSS_FRESH = 25             # a 50/200 cross this recent is still news

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# ---------------------------------------------------------------- indicators
def _sma(x: np.ndarray, n: int):
    if len(x) < n:
        return None
    return float(np.mean(x[-n:]))


def _sma_series(x: np.ndarray, n: int):
    if len(x) < n:
        return None
    c = np.cumsum(np.insert(x, 0, 0.0))
    return (c[n:] - c[:-n]) / n


def _slope_state(x: np.ndarray, n: int):
    """'rising' / 'falling' / 'flat' for the n-period MA over SLOPE_LOOKBACK."""
    s = _sma_series(x, n)
    if s is None or len(s) <= SLOPE_LOOKBACK:
        return None, None
    now, then = float(s[-1]), float(s[-1 - SLOPE_LOOKBACK])
    if then == 0:
        return None, None
    chg = (now - then) / then
    if chg > SLOPE_FLAT:
        return 'rising', chg
    if chg < -SLOPE_FLAT:
        return 'falling', chg
    return 'flat', chg


def _rsi_wilder(close: np.ndarray, n: int = RSI_N):
    """Wilder's RSI — the original smoothing, not a simple moving average."""
    if len(close) < n + 1:
        return None
    d = np.diff(close)
    gain, loss = np.clip(d, 0, None), np.clip(-d, 0, None)
    ag, al = float(np.mean(gain[:n])), float(np.mean(loss[:n]))
    for i in range(n, len(d)):
        ag = (ag * (n - 1) + gain[i]) / n
        al = (al * (n - 1) + loss[i]) / n
    if al == 0:
        return 100.0
    return float(100.0 - 100.0 / (1.0 + ag / al))


def _ema(x: np.ndarray, n: int):
    k = 2.0 / (n + 1.0)
    out = np.empty_like(x, dtype=float)
    out[0] = x[0]
    for i in range(1, len(x)):
        out[i] = x[i] * k + out[i - 1] * (1 - k)
    return out


def _macd(close: np.ndarray):
    """MACD(12,26,9) — the standard EMA construction, not an SMA stand-in."""
    if len(close) < MACD_SLOW + MACD_SIG:
        return None
    line = _ema(close, MACD_FAST) - _ema(close, MACD_SLOW)
    sig = _ema(line, MACD_SIG)
    return {'macd': float(line[-1]), 'signal': float(sig[-1]),
            'hist': float(line[-1] - sig[-1])}


def _ma_cross(close: np.ndarray, fast: int = 50, slow: int = 200):
    """Sessions since the fast MA last crossed the slow one, and which way."""
    f, s = _sma_series(close, fast), _sma_series(close, slow)
    if f is None or s is None:
        return None
    n = min(len(f), len(s))
    d = f[-n:] - s[-n:]
    sgn = np.sign(d)
    idx = np.where(np.diff(sgn) != 0)[0]
    if not len(idx):
        return None
    last = int(idx[-1])
    return {'ago': int(n - 1 - last),
            'kind': 'golden' if sgn[-1] > 0 else 'death'}


def _atr_wilder(high, low, close, n: int = ATR_N):
    """Wilder's ATR on the true range (gap-aware, unlike a plain high-low)."""
    if len(close) < n + 1:
        return None
    pc = close[:-1]
    tr = np.maximum.reduce([high[1:] - low[1:],
                            np.abs(high[1:] - pc),
                            np.abs(low[1:] - pc)])
    a = float(np.mean(tr[:n]))
    for i in range(n, len(tr)):
        a = (a * (n - 1) + tr[i]) / n
    return a


# ------------------------------------------------------------ S/R structure
def _fractal_pivots(high, low, k: int = PIVOT_K):
    """Bars whose high (low) is the extreme of the 2k+1 window centred on them."""
    hi, lo = [], []
    for i in range(k, len(high) - k):
        w = slice(i - k, i + k + 1)
        if high[i] == high[w].max():
            hi.append((i, float(high[i])))
        if low[i] == low[w].min():
            lo.append((i, float(low[i])))
    return hi, lo


def _cluster(pivots, n_bars: int, tol: float = CLUSTER_TOL):
    """Collapse nearby pivots into levels weighted by touches and recency.

    A level that was tested five times matters more than one tested once, and
    a test from last month matters more than one from two years ago — hence
    an exponential recency weight rather than a raw count.
    """
    if not pivots:
        return []
    pv = sorted(pivots, key=lambda p: p[1])
    groups, cur = [], [pv[0]]
    for idx, price in pv[1:]:
        if abs(price - cur[-1][1]) / max(cur[-1][1], 1e-9) <= tol:
            cur.append((idx, price))
        else:
            groups.append(cur)
            cur = [(idx, price)]
    groups.append(cur)

    out = []
    for g in groups:
        w = [2.0 ** (-(n_bars - 1 - i) / RECENCY_HALFLIFE) for i, _ in g]
        tot = sum(w)
        lvl = sum(p * wi for (_, p), wi in zip(g, w)) / tot
        out.append({'level': float(lvl), 'touches': len(g),
                    'weight': float(tot), 'last_idx': max(i for i, _ in g)})
    return out


def _round_numbers(close: float, above: bool):
    """Whole-number levels the tape reacts to, at a step scaled to the price.

    These score below real structure and exist to fill a slot when a name is
    pressed against its own two-year extreme and genuinely has little charted
    structure on that side — the honest alternative to publishing one level.
    """
    step = 10.0 ** np.floor(np.log10(max(close, 1e-9))) / 10.0
    out, k = [], 1
    while k <= 40:
        lvl = (np.floor(close / step) + k) * step if above else \
              (np.ceil(close / step) - k) * step
        if lvl <= 0 or abs(lvl - close) / close > 0.35:
            break
        out.append(float(lvl))
        k += 1
    return out


def _pick_levels(clusters, close: float, above: bool, ma_levels, extra):
    """Top-N levels on one side of spot, scored by structure then proximity.

    Moving averages, the 52-week extremes and round numbers are admitted as
    candidates because they are levels the tape actually reacts to, but they
    score strictly below a swing cluster and only win a slot when structure
    does not fill one — they are never auto-included.
    """
    cands = []
    for c in clusters:
        side = c['level'] > close
        if side != above:
            continue
        dist = abs(c['level'] - close) / close
        if dist > 0.35 or dist < MIN_DIST:   # too far, or indistinguishable from spot
            continue
        cands.append({'level': c['level'],
                      'score': c['weight'] * (1.0 + c['touches']) / (1.0 + 8 * dist),
                      'kind': 'swing', 'touches': c['touches']})
    for name, lvl in list(ma_levels.items()) + list(extra.items()):
        if lvl is None:
            continue
        if (lvl > close) != above:
            continue
        dist = abs(lvl - close) / close
        if dist > 0.35 or dist < MIN_DIST:
            continue
        cands.append({'level': float(lvl),
                      'score': 1.0 / (1.0 + 8 * dist),
                      'kind': name, 'touches': 0})
    for lvl in _round_numbers(close, above):
        dist = abs(lvl - close) / close
        if dist < MIN_DIST:
            continue
        cands.append({'level': lvl, 'score': 0.35 / (1.0 + 8 * dist),
                      'kind': 'round', 'touches': 0})

    # de-duplicate: two candidates within tol are the same wall, keep the best
    cands.sort(key=lambda c: -c['score'])
    kept = []
    for c in cands:
        if all(abs(c['level'] - k['level']) / close > CLUSTER_TOL for k in kept):
            kept.append(c)
        if len(kept) == N_LEVELS:
            break
    # NEAREST FIRST, both sides — so R1/S1 on the page always means "the next
    # level price has to deal with". The retired hand-authored levels were
    # inconsistent about this (TSLA ascending, COMI descending); this fixes it.
    kept.sort(key=lambda c: c['level'] if above else -c['level'])
    return kept


def _fmt(x: float, ref: float):
    """Match the decimal convention the page already uses for this name."""
    return int(round(x)) if ref >= 1000 else round(x, 2)


# -------------------------------------------------------------- the narrative
def _trend_line(pos, slopes, close, ma):
    """One clause naming where price sits in the MA stack, and the 200-day."""
    above = [n for n in MA_WINDOWS if ma.get(n) is not None and close > ma[n]]
    below = [n for n in MA_WINDOWS if ma.get(n) is not None and close < ma[n]]
    s200 = slopes.get(200)
    tail = f", above a {s200} 200-day" if (200 in above and s200) else (
        f", below a {s200} 200-day" if (200 in below and s200) else "")
    if len(above) == len([n for n in MA_WINDOWS if ma.get(n) is not None]):
        head = "Trading above the whole moving-average stack"
    elif not above:
        head = "Trading below the whole moving-average stack"
    elif 200 in above and 20 in below:
        head = "Consolidating below the near-term moving averages"
    else:
        head = "Mixed against the moving-average stack"
    if tail and tail.lstrip(', ').split()[0] in ('above', 'below'):
        # avoid "above ... , above a rising 200-day" reading twice
        if head.startswith("Trading above") and 200 in above:
            tail = f", on a {s200} 200-day" if s200 else ""
        if head.startswith("Trading below") and 200 in below:
            tail = f", under a {s200} 200-day" if s200 else ""
    return head + tail


def _momentum_words(rsi):
    if rsi is None:
        return "not computable on this history"
    if rsi >= 70:
        return "stretched"
    if rsi >= 60:
        return "firm"
    if rsi > 40:
        return "neutral"
    if rsi > 30:
        return "soft"
    return "washed out"


def _tape_words(atr_pct):
    if atr_pct is None:
        return "an unreadable tape"
    if atr_pct < 0.015:
        return "an orderly tape"
    if atr_pct < 0.030:
        return "a normal tape"
    if atr_pct < 0.050:
        return "a lively tape"
    return "a volatile tape"


def _num(x, ref):
    return f'{x:,.0f}'.replace(',', '') if ref >= 1000 else f'{x:.2f}'


def build_narrative(st: dict) -> dict:
    """Templated prose. Every clause is selected by a computed number above."""
    close, ma, sl = st['close'], st['ma'], st['ma_slope']
    ref = close
    parts = []
    named = [(n, ma[n], sl.get(n)) for n in MA_WINDOWS if ma.get(n) is not None]
    if named:
        def phrase(items):
            segs = [f"a {s or 'flat'} {n}-day ({_num(v, ref)})" for n, v, s in items]
            if len(segs) == 1:
                return segs[0]
            return ", ".join(segs[:-1]) + " and " + segs[-1]
        up = [t for t in named if close > t[1]]
        dn = [t for t in named if close <= t[1]]
        if up and dn:
            # the informative shape: which side of the stack it is on, and where it isn't
            lead, second = (dn, up) if len(dn) >= len(up) else (up, dn)
            lw = "below" if lead is dn else "above"
            sw = "above" if lead is dn else "below"
            body = (f"{lw} {phrase(lead)}, but {sw} {phrase(second)}")
        elif up:
            body = f"above {phrase(up)}"
        else:
            body = f"below {phrase(dn)}"
        parts.append(f"The price closed {_num(close, ref)} {body}.")
    mom = _momentum_words(st['rsi'])
    tape = _tape_words(st['atr_pct'])
    bits = f"Momentum is {mom}"
    if st['rsi'] is not None:
        bits += f": RSI(14) is ~{st['rsi']:.0f}"
    if st['atr'] is not None:
        bits += (f" and the daily ATR near {_num(st['atr'], ref)} "
                 f"(~{st['atr_pct'] * 100:.1f}%) points to {tape}")
    parts.append(bits + ".")
    md = st.get('macd')
    if md:
        # the LINE's sign and the HISTOGRAM's sign are different facts — a MACD
        # below zero with a positive histogram is falling momentum that has
        # started to turn, not "positive MACD". Say both.
        if md['macd'] >= 0:
            side = ("positive and rising" if md['hist'] > 0
                    else "above zero but rolling over")
        else:
            side = ("below zero but turning up" if md['hist'] > 0
                    else "negative and still falling")
        sgn = lambda v: ('+' if v > 0 else '\u2212') + _num(abs(v), ref)  # noqa: E731
        parts.append(
            f"MACD (12\u00b726\u00b79) is {side} "
            f"({sgn(md['macd'])} / {sgn(md['signal'])} / {sgn(md['hist'])}).")
    xo = st.get('ma_cross')
    if xo and xo['ago'] <= CROSS_FRESH:
        parts.append(
            f"The 50-day crossed {'above' if xo['kind'] == 'golden' else 'beneath'} "
            f"the 200-day {xo['ago']} session{'s' if xo['ago'] != 1 else ''} ago — "
            f"a fresh {xo['kind']}-cross, a momentum-regime change rather than "
            f"noise inside an intact trend.")
    if st['hi_52w'] and st['lo_52w']:
        parts.append(
            f"Over the last year it has ranged {_num(st['lo_52w'], ref)}–"
            f"{_num(st['hi_52w'], ref)}; the last close sits "
            f"{st['pct_off_high'] * 100:.0f}% below that high and "
            f"{st['pct_off_low'] * 100:.0f}% above that low.")

    res = st['levels']['res']
    sup = st['levels']['sup']
    r_near, r_far = (res[0], res[-1]) if res else (None, None)
    s_near, s_far = (sup[0], sup[-1]) if sup else (None, None)
    if not res:
        bull = ("There is no charted resistance above the last close — the tape "
                "is at the top of its own two-year structure.")
    elif len(res) == 1 or r_far == r_near:
        bull = (f"A daily close back above {_num(r_near, ref)} would clear the "
                f"only charted resistance in range.")
    else:
        bull = (f"A daily close back above {_num(r_near, ref)} would clear the "
                f"nearest resistance and open the {_num(r_far, ref)} zone.")
    if not sup:
        bear = ("There is no charted support below the last close — the tape is "
                "at the bottom of its own two-year structure.")
    elif len(sup) == 1 or s_far == s_near:
        bear = (f"A close below {_num(s_near, ref)} would break the only charted "
                f"support in range.")
    else:
        bear = (f"A close below {_num(s_near, ref)} would break the nearest "
                f"support and open the {_num(s_far, ref)} zone.")
    return {'trend': _trend_line(None, sl, close, ma),
            'summary': " ".join(parts), 'bull': bull, 'bear': bear}


# ------------------------------------------------------------------- compute
def compute(market: str, series: str, computed_on: str | None = None,
            frame=None) -> dict:
    """The whole technical read for one name, from the cleaned library.

    ``frame`` is an optional pre-loaded ``(df, rep)`` pair, already through the
    Step 0.0 gate. It exists so a walk-forward replay can re-run THIS function
    on a truncated library rather than re-implementing the read against it — a
    checker that models the thing it checks is checking a different thing
    (the [R-ENF-03] lesson, in Python rather than JS). Production always passes
    None and loads the full library exactly as before.
    """
    df, rep = load_clean(market, series) if frame is None else frame
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    high = df['High'].to_numpy(dtype=float)
    low = df['Low'].to_numpy(dtype=float)
    n = len(close)
    if n < 60:
        raise ValueError(f'{market}/{series}: only {n} clean sessions — '
                         'too short for a technical read')

    last = float(close[-1])
    ma = {w: _sma(close, w) for w in MA_WINDOWS}
    slopes = {w: _slope_state(close, w)[0] for w in MA_WINDOWS}
    rsi = _rsi_wilder(close)
    atr = _atr_wilder(high, low, close)
    macd = _macd(close)
    cross = _ma_cross(close)
    win = min(252, n)
    hi52, lo52 = float(high[-win:].max()), float(low[-win:].min())

    lb = min(PIVOT_LOOKBACK, n)
    ph, pl = _fractal_pivots(high[-lb:], low[-lb:])
    cl_hi, cl_lo = _cluster(ph, lb), _cluster(pl, lb)
    ma_lv = {f'{w}-day MA': ma[w] for w in MA_WINDOWS}
    res = _pick_levels(cl_hi + cl_lo, last, True, ma_lv, {'52w high': hi52})
    sup = _pick_levels(cl_lo + cl_hi, last, False, ma_lv, {'52w low': lo52})

    st = {
        'market': market, 'series': series,
        'close': last,
        'data_date': dates.iloc[-1].date().isoformat(),
        'computed_on': computed_on or date.today().isoformat(),
        'sessions': int(n), 'rows_in': rep['rows_in'], 'repairs': rep['repairs'],
        'ma': ma, 'ma_slope': slopes, 'rsi': rsi, 'atr': atr,
        'macd': macd, 'ma_cross': cross,
        'atr_pct': (atr / last) if atr else None,
        'hi_52w': hi52, 'lo_52w': lo52,
        'pct_off_high': (hi52 - last) / hi52,
        'pct_off_low': (last - lo52) / lo52,
        'levels': {'res': [_fmt(c['level'], last) for c in res],
                   'sup': [_fmt(c['level'], last) for c in sup]},
        'level_detail': {'res': res, 'sup': sup},
    }
    st['tech'] = build_narrative(st)
    if cross and cross['ago'] <= CROSS_FRESH:
        st['tech']['trend'] += f"; fresh {cross['kind']}-cross"
    return st


def pretty(st: dict) -> str:
    t = st['tech']
    L = st['levels']
    return (f"{st['market']}/{st['series']}  close {st['close']} on {st['data_date']}"
            f"  ({st['sessions']} clean sessions)\n"
            f"  res {L['res']}   sup {L['sup']}\n"
            f"  trend  : {t['trend']}\n"
            f"  summary: {t['summary']}\n"
            f"  bull   : {t['bull']}\n"
            f"  bear   : {t['bear']}")


if __name__ == '__main__':
    mkt = sys.argv[1] if len(sys.argv) > 1 else 'EG'
    tkr = sys.argv[2] if len(sys.argv) > 2 else 'COMI'
    print(pretty(compute(mkt, tkr)))
