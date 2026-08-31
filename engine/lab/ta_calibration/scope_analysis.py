"""scope_analysis.py — every technical claim, at all three scopes, on the short clock.

For each claim family and each horizon this answers the three questions the
Lessons Register's ladder asks:

  ALL     does the claim hold pooled across every ticker?
  CLASS   does it differ BETWEEN classes by more than sampling noise? A set of
          per-class numbers is not a class-level finding — a claim only earns
          the middle rung when the classes genuinely disagree, which is a
          heterogeneity question and is tested as one (Cochran's Q).
  STOCK   how many individual names carry it on their own history?

THE MIDDLE RUNG HAS TO BE EARNED. It is easy to slice any effect by market or
sector, print ten different numbers and call the differences a finding; ten
draws from one distribution also look different. Q asks whether the spread
between classes exceeds what the within-class standard errors already explain.
"""
from __future__ import annotations
import numpy as np, pandas as pd
from scipy import stats
import scopes, score

ALPHA = 0.05
MIN_CLASS_NAMES = 4       # a class with fewer names cannot carry a class finding
MIN_OBS = 100             # per-cell floor before any effect is reported


# ---------------------------------------------------------------- claim families
def trend_gap(s):
    """Forward up-rate above the whole MA stack minus below it."""
    a = s[s.trend.str.startswith('Trading above the whole')]
    b = s[s.trend.str.startswith('Trading below the whole')]
    if len(a) < 30 or len(b) < 30:
        return None
    ka, kb = int((a.fwd_ret > 0).sum()), int((b.fwd_ret > 0).sum())
    p1, p2 = ka / len(a), kb / len(b)
    pool = (ka + kb) / (len(a) + len(b))
    se = np.sqrt(max(pool * (1 - pool) * (1 / len(a) + 1 / len(b)), 1e-12))
    return dict(effect=p1 - p2, se=se, n=len(a) + len(b),
                extra=dict(up_above=p1, up_below=p2, n_above=len(a), n_below=len(b)))


def tape_rho(s):
    """Rank correlation between the ATR reading and realized forward vol."""
    v = s.dropna(subset=['atr_pct', 'rlz_vol'])
    if len(v) < MIN_OBS:
        return None
    rho, _ = stats.spearmanr(v.atr_pct, v.rlz_vol)
    # Fisher-z standard error, the standard interval for a rank correlation
    return dict(effect=float(rho), se=float(1 / np.sqrt(max(len(v) - 3, 1))), n=len(v),
                extra=dict())


def _bucket_lift(s, mask, label):
    sub = s[mask]
    if len(sub) < MIN_OBS:
        return None
    base = float((s.fwd_ret > 0).mean())
    p = float((sub.fwd_ret > 0).mean())
    se = float(np.sqrt(max(p * (1 - p) / len(sub), 1e-12)))
    return dict(effect=p - base, se=se, n=len(sub),
                extra=dict(up_rate=p, base=base, label=label))


def rsi_high(s):  return _bucket_lift(s, s.rsi >= 70, 'RSI>=70')
def rsi_low(s):   return _bucket_lift(s, s.rsi < 30, 'RSI<30')
def macd_pos(s):  return _bucket_lift(s, s.macd_hist > 0, 'MACD histogram positive')


def level_edge(d):
    """Paired real-vs-null break rate, conditional on both being reached."""
    both = d[(d.claim == 'level') & (d.n_sides == 2) & d.touched & d.p_touched]
    both = both.dropna(subset=['p_broke'])
    if len(both) < MIN_OBS:
        return None
    diff = (both.p_broke - both.broke.astype(float)).to_numpy()
    return dict(effect=float(diff.mean()),
                se=float(diff.std(ddof=1) / np.sqrt(len(diff))), n=len(diff),
                extra=dict(broke_real=float(both.broke.mean()),
                           broke_null=float(both.p_broke.mean())))


STATE_FAMILIES = {'trend': trend_gap, 'tape': tape_rho, 'rsi_high': rsi_high,
                  'rsi_low': rsi_low, 'macd': macd_pos}


# ------------------------------------------------------------------ heterogeneity
def cochran_q(effects, ses):
    """Do these class estimates differ by more than their own standard errors?"""
    e, s = np.asarray(effects, float), np.asarray(ses, float)
    ok = np.isfinite(e) & np.isfinite(s) & (s > 0)
    e, s = e[ok], s[ok]
    if len(e) < 2:
        return None
    w = 1 / s ** 2
    mu = float((w * e).sum() / w.sum())
    q = float((w * (e - mu) ** 2).sum())
    df = len(e) - 1
    return dict(q=q, df=df, p=float(1 - stats.chi2.cdf(q, df)), pooled=mu,
                i2=float(max(0.0, (q - df) / q) * 100) if q > 0 else 0.0, k=len(e))


def run(r, family, h, class_col):
    """One family, one horizon, all three scopes."""
    fam = STATE_FAMILIES.get(family)
    sel = r[(r.h == h) & (r.claim == ('state' if fam else 'level'))]
    f = fam if fam else level_edge

    allv = f(sel)
    per_class, per_stock = {}, {}
    for cls, g in sel.groupby(class_col):
        if g.key.nunique() < MIN_CLASS_NAMES:
            continue
        v = f(g)
        if v:
            per_class[cls] = dict(v, names=int(g.key.nunique()))
    for k, g in sel.groupby('key'):
        v = f(g)
        if v:
            z = v['effect'] / v['se'] if v['se'] > 0 else 0.0
            per_stock[k] = dict(v, sig=bool(abs(z) > stats.norm.ppf(1 - ALPHA / 2)),
                                z=float(z))
    het = cochran_q([v['effect'] for v in per_class.values()],
                    [v['se'] for v in per_class.values()]) if len(per_class) > 1 else None
    return dict(family=family, h=h, scope_class=class_col, pooled=allv,
                per_class=per_class, heterogeneity=het,
                n_stocks=len(per_stock),
                n_stocks_sig=sum(1 for v in per_stock.values() if v['sig']),
                per_stock=per_stock)
