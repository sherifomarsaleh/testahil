"""score.py — the scoring axis for the replayed technical read.

Every number here is a DIFFERENCE against a matched null, never a raw rate.
"Price touched R1 in 68% of windows" is a fact about volatility; "price closed
beyond R1 in 41% of windows against 52% at a distance-matched non-level" is a
fact about R1.

The bar is the house bar, unchanged: block bootstrap over origins at blocks
{2,3,4}, 3000 draws, seed 42, and a result counts as ROBUST only when the sign
holds across ALL THREE block sizes (panel_refresh.robust_verdict's rule).
Origins overlap at the 3-month horizon, which is exactly what the block
bootstrap is for. LONO (leave-one-name-out) so no single name can carry a
finding, and a calendar split-half, mirroring the four joint tests the
direction tournament already required of a drift signal.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

BLOCKS = (2, 3, 4)
N_BOOT = 3000
SEED = 42


def block_boot(x: np.ndarray, groups: np.ndarray, blocks=BLOCKS, n_boot=N_BOOT, seed=SEED):
    """CI on the mean of x, resampling contiguous blocks within each name."""
    out = {}
    for b in blocks:
        rng = np.random.default_rng(seed + b)
        draws = np.empty(n_boot)
        idx_by_g = [np.where(groups == g)[0] for g in np.unique(groups)]
        for k in range(n_boot):
            picks = []
            for gi in idx_by_g:
                nb = max(1, len(gi) // b)
                starts = rng.integers(0, max(1, len(gi) - b + 1), nb)
                for s in starts:
                    picks.append(gi[s:s + b])
            v = x[np.concatenate(picks)] if picks else x
            draws[k] = v.mean()
        out[b] = (float(np.percentile(draws, 5)), float(np.percentile(draws, 95)))
    return out


def robust(ci: dict):
    """ROBUST only if the 5-95 interval excludes zero with ONE sign everywhere."""
    signs = set()
    for lo, hi in ci.values():
        if lo > 0:
            signs.add('+')
        elif hi < 0:
            signs.add('-')
        else:
            return 'not robust'
    return f'robust {signs.pop()}' if len(signs) == 1 else 'not robust'


def wilson(k, n, z=1.96):
    if not n:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


# ------------------------------------------------------------- level claims
def score_levels(r: pd.DataFrame, months: int, side: str = None, rank: int = None):
    """Paired real-vs-placebo break test, conditional on BOTH being touched."""
    d = r[(r.claim == 'level') & (r.months == months)]
    if side:
        d = d[d.side == side]
    if rank:
        d = d[d['rank'] == rank]
    both = d[d.touched & d.p_touched]
    if len(both) < 30:
        return None
    # paired difference: +1 when the real level held and the placebo did not
    diff = (both.p_broke.astype(float) - both.broke.astype(float)).to_numpy()
    ci = block_boot(diff, (both.market + '_' + both.ticker).to_numpy())
    return dict(
        months=months, side=side or 'both', rank=rank or 'all',
        n_paired=int(len(both)),
        touch_real=float(d.touched.mean()), touch_placebo=float(d.p_touched.mean()),
        dist_real=float(d.dist.mean()), dist_placebo=float(d.placebo_dist.mean()),
        break_real=float(both.broke.mean()), break_placebo=float(both.p_broke.mean()),
        delta=float(diff.mean()), ci=ci, verdict=robust(ci),
        names=int(len(both.groupby(['market', 'ticker']))))


def lono_levels(r: pd.DataFrame, months: int, side=None, rank=None):
    """Sign stability with each name removed in turn."""
    d = r[(r.claim == 'level') & (r.months == months)]
    if side:
        d = d[d.side == side]
    if rank:
        d = d[d['rank'] == rank]
    both = d[d.touched & d.p_touched]
    deltas = {}
    both = both.assign(key=both.market + '_' + both.ticker)
    for nm in both.key.unique():
        s = both[both.key != nm]
        deltas[nm] = float((s.p_broke.astype(float) - s.broke.astype(float)).mean())
    v = np.array(list(deltas.values()))
    return dict(n_names=len(v), min=float(v.min()), max=float(v.max()),
                all_same_sign=bool((v > 0).all() or (v < 0).all()))


def split_half_levels(r: pd.DataFrame, months: int, side=None, rank=None):
    d = r[(r.claim == 'level') & (r.months == months)]
    if side:
        d = d[d.side == side]
    if rank:
        d = d[d['rank'] == rank]
    both = d[d.touched & d.p_touched].copy()
    both['o'] = pd.to_datetime(both.origin)
    med = both['o'].median()
    out = {}
    for tag, h in (('early', both[both.o <= med]), ('late', both[both.o > med])):
        out[tag] = dict(n=int(len(h)),
                        delta=float((h.p_broke.astype(float) - h.broke.astype(float)).mean()))
    out['both_same_sign'] = bool(np.sign(out['early']['delta']) == np.sign(out['late']['delta'])
                                 and out['early']['delta'] != 0)
    return out


# -------------------------------------------------------------- state claims
def score_trend(r: pd.DataFrame, months: int):
    """Does the trend clause's own direction beat the name's base up-rate?"""
    d = r[(r.claim == 'state') & (r.months == months)].copy()
    base = float((d.fwd_ret > 0).mean())
    out = {'base_up_rate': base, 'n_total': int(len(d)), 'buckets': {}}
    for label, want_up in (('Trading above the whole moving-average stack', True),
                           ('Trading below the whole moving-average stack', False)):
        s = d[d.trend.str.startswith(label)]
        if len(s) < 30:
            continue
        hit = ((s.fwd_ret > 0) == want_up).mean()
        up = float((s.fwd_ret > 0).mean())
        out['buckets'][label] = dict(
            n=int(len(s)), names=int(len(s.groupby(['market', 'ticker']))),
            up_rate=up, hit_rate=float(hit), lift_vs_base=float(up - base),
            wilson_up=[float(x) for x in wilson(int((s.fwd_ret > 0).sum()), len(s))],
            median_fwd_ret=float(s.fwd_ret.median()))
    return out


def score_tape(r: pd.DataFrame, months: int):
    """Is the ATR tape word a real volatility forecast? (rank correlation + buckets)"""
    d = r[(r.claim == 'state') & (r.months == months)].dropna(subset=['atr_pct', 'rlz_vol'])
    if len(d) < 50:
        return None
    rho, p = stats.spearmanr(d.atr_pct, d.rlz_vol)
    buckets = {}
    edges = [(0, .015, 'orderly'), (.015, .030, 'normal'), (.030, .050, 'lively'), (.050, 9, 'volatile')]
    for lo, hi, name in edges:
        s = d[(d.atr_pct >= lo) & (d.atr_pct < hi)]
        if len(s) >= 20:
            buckets[name] = dict(n=int(len(s)), median_fwd_vol=float(s.rlz_vol.median()))
    return dict(n=int(len(d)), spearman=float(rho), p=float(p), buckets=buckets)


def score_rsi(r: pd.DataFrame, months: int):
    """Do the momentum words separate forward outcomes at all?"""
    d = r[(r.claim == 'state') & (r.months == months)].dropna(subset=['rsi'])
    base = float((d.fwd_ret > 0).mean())
    out = {'base_up_rate': base, 'buckets': {}}
    for lo, hi, name in ((70, 101, 'stretched'), (60, 70, 'firm'), (40, 60, 'neutral'),
                         (30, 40, 'soft'), (0, 30, 'washed out')):
        s = d[(d.rsi >= lo) & (d.rsi < hi)]
        if len(s) >= 30:
            out['buckets'][name] = dict(n=int(len(s)), up_rate=float((s.fwd_ret > 0).mean()),
                                        lift_vs_base=float((s.fwd_ret > 0).mean() - base),
                                        median_fwd_ret=float(s.fwd_ret.median()))
    return out
