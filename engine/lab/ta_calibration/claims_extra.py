"""claims_extra.py — the three families the first calibration left unscored.

  TRIGGER   "A daily close back above R1 would clear the nearest resistance and
            open the R3 zone." The only explicitly CONDITIONAL forecast in the
            read. Scored in the order it claims: the far rung must be reached
            AFTER the close that fired the trigger, against a null ladder moved
            off structure with the near/far ratio preserved.

  CROSS     "a fresh golden-cross, a momentum-regime change rather than noise
            inside an intact trend." That is an assertion about the forward
            distribution, and it is testable: compare origins carrying a fresh
            cross against origins in the SAME trend state without one, so the
            comparison isolates the cross rather than re-measuring the trend.

  VOLUME    Never tested, and not currently claimed anywhere in the read — so
            this is exploration, not calibration, and nothing here may enter the
            read without clearing the promotion rule on its own out-of-sample
            evidence.
"""
from __future__ import annotations
import numpy as np, pandas as pd
from scipy import stats

MIN_N = 100


def _two_prop(k1, n1, k2, n2):
    if min(n1, n2) < 20:
        return None
    p1, p2 = k1 / n1, k2 / n2
    pool = (k1 + k2) / (n1 + n2)
    se = np.sqrt(max(pool * (1 - pool) * (1 / n1 + 1 / n2), 1e-12))
    z = (p1 - p2) / se
    return dict(p_real=p1, p_null=p2, n_real=n1, n_null=n2, effect=p1 - p2,
                se=se, z=float(z), p=float(2 * (1 - stats.norm.cdf(abs(z)))))


def trigger(r, h, side=None):
    """Given the trigger fired, does the far rung open more often than for the null?"""
    d = r[(r.claim == 'trigger') & (r.h == h)]
    if side:
        d = d[d.side == side]
    real = d[d.touched].dropna(subset=['broke'])
    null = d[d.p_touched].dropna(subset=['p_broke'])
    if not len(real) or not len(null):
        return None
    out = _two_prop(int(real.broke.sum()), len(real),
                    int(null.p_broke.sum()), len(null))
    if out:
        out.update(fire_rate_real=float(d.touched.mean()),
                   fire_rate_null=float(d.p_touched.mean()), n_origins=len(d))
    return out


def cross(r, h, kind='golden', fresh=25):
    """Fresh cross vs the same trend state without one — the cross, not the trend."""
    d = r[(r.claim == 'state') & (r.h == h)].copy()
    d['fresh'] = d.cross_ago.notna() & (d.cross_ago <= fresh) & (d.cross_kind == kind)
    d['stale'] = (d.cross_kind == kind) & (~d['fresh'])
    a, b = d[d.fresh], d[d.stale]
    if len(a) < 30 or len(b) < 30:
        return None
    out = _two_prop(int((a.fwd_ret > 0).sum()), len(a),
                    int((b.fwd_ret > 0).sum()), len(b))
    if out:
        # the clause claims a REGIME change, so movement is tested too, not only direction
        va, vb = a.rlz_vol.dropna(), b.rlz_vol.dropna()
        out['vol_ratio'] = float(va.median() / vb.median()) if len(vb) and vb.median() else np.nan
        out['mw_p'] = float(stats.mannwhitneyu(va, vb, alternative='two-sided')[1]) \
            if len(va) > 20 and len(vb) > 20 else np.nan
    return out


def volume(r, h):
    """Does a volume surge carry direction, or movement, or neither?"""
    d = r[(r.claim == 'state') & (r.h == h)].dropna(subset=['vol_z'])
    if len(d) < MIN_N:
        return None
    hi, lo = d[d.vol_z >= 1.0], d[d.vol_z <= -1.0]
    dir_ = _two_prop(int((hi.fwd_ret > 0).sum()), len(hi),
                     int((lo.fwd_ret > 0).sum()), len(lo)) if min(len(hi), len(lo)) >= 20 else None
    v = d.dropna(subset=['rlz_vol'])
    rho, p = stats.spearmanr(v.vol_z, v.rlz_vol) if len(v) > MIN_N else (np.nan, np.nan)
    rho_r, p_r = stats.spearmanr(d.vol_z, d.fwd_ret.abs()) if len(d) > MIN_N else (np.nan, np.nan)
    return dict(direction=dir_, vol_rho=float(rho), vol_p=float(p),
                absret_rho=float(rho_r), absret_p=float(p_r), n=len(d))
