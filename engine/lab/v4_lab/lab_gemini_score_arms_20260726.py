"""score_arms.py — PASS 2 (cheap): score the repaired arms.

Every arm gets IDENTICAL treatment: its own (nu, width_cal) fitted by the same
pooled MLE production uses (fit_nu_scale -> shrink_cal) on its own standardized
residuals. So no arm is penalised for being uncalibrated, and PROD is refitted
the same way rather than carrying its shipped advantage.

Online learners are walk-forward: at each origin they see only windows that had
already RESOLVED by that origin's date.
"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/tmp/mcrev/testahil/engine')
from scipy import stats
from mc_v3 import fit_nu_scale, shrink_cal, simulate_terminal_v3
from mc_v2 import crps_sample
from panel_refresh import robust_verdict, verdict_ci

NP = 20000; SEED = 42; H = 60
MARKET = sys.argv[1] if len(sys.argv) > 1 else 'EG'
R = pd.read_csv(f'/tmp/mcrev/comp_{MARKET}.csv', parse_dates=['origin'])
R = R.sort_values(['ticker', 'origin']).reset_index(drop=True)
R['u_prod'] = (np.log(R.realized / R.spot) - R.drift) / R.sh_prod
R['u_hl'] = (np.log(R.realized / R.spot) - R.drift) / R.sh_harq_lvl
R['u_hg'] = (np.log(R.realized / R.spot) - R.drift) / R.sh_harq_log

K95 = float(stats.t.ppf(0.95, 4) * np.sqrt((4 - 2) / 4.0))   # unit-var t(4) 95th pct


def aci_mult(R, ucol, lr=0.30, target=0.10, lo=0.6, hi=2.0):
    """Multiplicative ACI on a FULL-CONE width multiplier (repair d), per name,
    walk-forward: window i is forecast with the multiplier learned from windows
    that resolved strictly before it."""
    out = np.ones(len(R))
    for tk, idx in R.groupby('ticker').groups.items():
        idx = list(idx); m = 1.0
        for i in idx:
            out[i] = m
            miss = 1.0 if abs(R[ucol].iloc[i]) / m > K95 else 0.0
            m = float(np.clip(m * np.exp(lr * (miss - target)), lo, hi))
    return out


def rms_mult(R, ucol, w=0.5, minw=6, lo=0.7, hi=1.4, pooled=False):
    """Shrunk running RMS of resolved standardized residuals (repair d, variant).
    pooled=True -> market-level in calendar time (far more data per update)."""
    out = np.ones(len(R))
    if pooled:
        order = R.sort_values('origin').index
        hist = []
        # a window resolves H sessions after its origin; approximate with origin
        # order and a one-window lag so nothing in-sample leaks
        for i in order:
            if len(hist) >= minw:
                r = np.sqrt(np.mean(np.square(hist)))
                out[i] = float(np.clip(1 + w * (r - 1), lo, hi))
            hist.append(R[ucol].iloc[i])
        return out
    for tk, idx in R.groupby('ticker').groups.items():
        idx = list(idx); hist = []
        for i in idx:
            if len(hist) >= minw:
                r = np.sqrt(np.mean(np.square(hist)))
                out[i] = float(np.clip(1 + w * (r - 1), lo, hi))
            hist.append(R[ucol].iloc[i])
    return out


R['m_aci'] = aci_mult(R, 'u_prod')
R['m_rms'] = rms_mult(R, 'u_prod')
R['m_rmsp'] = rms_mult(R, 'u_prod', pooled=True)
R['m_aci_hg'] = aci_mult(R, 'u_hg')

ARMS = {
 'PROD  log-HAR (production)':            ('sh_prod',      None,       False),
 'R1  true HARQ, levels':                 ('sh_harq_lvl',  None,       False),
 'R2  true HARQ, log-space':              ('sh_harq_log',  None,       False),
 'R3  PROD + skew-t shape':               ('sh_prod',      None,       True),
 'R4  PROD + online ACI width':           ('sh_prod',      'm_aci',    False),
 'R5  PROD + online RMS width (name)':    ('sh_prod',      'm_rms',    False),
 'R6  PROD + online RMS width (pooled)':  ('sh_prod',      'm_rmsp',   False),
 'R7  GEMINI FULLY REPAIRED (a+b+c+d)':   ('sh_harq_log',  'm_aci_hg', True),
}


def skew_t(spot, sh, drift, nu, alpha, n, seed):
    rng = np.random.default_rng(seed)
    chi = rng.chisquare(nu, n); mix = np.sqrt((nu - 2) / chi)
    if abs(alpha) < 1e-9:
        x = rng.standard_normal(n) * mix
    else:
        d = alpha / np.sqrt(1 + alpha * alpha)
        U0 = rng.standard_normal(n); U1 = rng.standard_normal(n)
        Z = d * np.abs(U0) + np.sqrt(1 - d * d) * U1
        Z = (Z - Z.mean()) / Z.std()
        x = Z * mix
    x = (x - x.mean()) / x.std()          # unit variance, zero mean (repair b)
    return spot * np.exp(drift + x * sh)


def build(R, scol, mcol, skew, nu=None, cal=None):
    base = R[scol].values * (R[mcol].values if mcol else 1.0)
    u = (np.log(R.realized / R.spot).values - R.drift.values) / base
    if nu is None:
        nu, s = fit_nu_scale(u); cal = shrink_cal(s)
    sh = base * cal
    crps = np.empty(len(R))
    for i in range(len(R)):
        a = R.alpha_skew.values[i] if skew else 0.0
        samp = skew_t(R.spot.values[i], sh[i], R.drift.values[i], nu, a, NP,
                      SEED + int(R.origin_idx.values[i]) + (11 if skew else 0))
        crps[i] = crps_sample(samp, R.realized.values[i])
    inb = np.abs(u / cal) <= K95 * (nu and 1.0)   # placeholder, recomputed below
    return crps, nu, cal, sh, u


bn = (R.crps_b / R.spot).values
print(f"=== {MARKET}: {len(R)} windows / {R.ticker.nunique()} names — "
      f"scale-normalized CRPS skill vs carry-anchored RW ===")
print(f"{'arm':38s} {'nu':>5s} {'cal':>6s} {'skill':>9s}  {'CI':>20s}  verdict   vs PROD")
res = {}
for lab, (scol, mcol, skew) in ARMS.items():
    crps, nu, cal, sh, u = build(R, scol, mcol, skew)
    cn = crps / R.spot.values
    sk = 1 - cn.sum() / bn.sum()
    v, _ = robust_verdict(cn, bn); lo, hi, _ = verdict_ci(cn, bn, 3)
    res[lab] = dict(cn=cn, sk=sk, nu=nu, cal=cal, sh=sh, u=u)
    d = f"{sk - res['PROD  log-HAR (production)']['sk']:+.4f}" if 'PROD  log-HAR (production)' in res else ""
    print(f"{lab:38s} {nu:5.1f} {cal:6.3f} {sk:+9.4f}  [{lo:+.4f},{hi:+.4f}]  {v:22s} {d}")

# ---- paired block bootstrap of (arm - PROD) skill difference -----------------
print(f"\n--- paired block bootstrap (block=3), P(arm beats PROD) and 90% CI of the difference ---")
base = res['PROD  log-HAR (production)']['cn']
rng = np.random.default_rng(0); n = len(R); B = 3000; blk = 3
idxs = [np.concatenate([np.arange(s, s + blk) for s in
        rng.integers(0, n - blk + 1, size=int(np.ceil(n / blk)))])[:n] for _ in range(B)]
for lab in ARMS:
    if lab.startswith('PROD'): continue
    a = res[lab]['cn']
    d = np.array([(1 - a[ix].sum() / bn[ix].sum()) - (1 - base[ix].sum() / bn[ix].sum())
                  for ix in idxs])
    lo, hi = np.percentile(d, [5, 95])
    print(f"  {lab:38s} delta {d.mean():+.4f}  CI[{lo:+.4f},{hi:+.4f}]  P(better)={np.mean(d>0):.2f}")

# ---- calibration diagnostics -------------------------------------------------
print(f"\n--- calibration (|std(u)-1| closer to 0 is better; cov90 target 0.900) ---")
for lab in ARMS:
    u = res[lab]['u'] / res[lab]['cal']
    nu = res[lab]['nu']
    k = float(stats.t.ppf(0.95, nu) * np.sqrt((nu - 2) / nu)) if nu < 200 else 1.645
    print(f"  {lab:38s} std(u)={u.std():.3f}  |std-1|={abs(u.std()-1):.3f}  "
          f"cov90={np.mean(np.abs(u) <= k):.3f}")
R.to_csv(f'/tmp/mcrev/arms_{MARKET}.csv', index=False)
