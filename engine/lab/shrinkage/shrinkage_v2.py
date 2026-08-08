"""shrinkage_v2.py — full-universe, walk-forward test of NAME-LEVEL width_cal
shrinkage (TOP OPEN ITEM). Successor to the 20-Jul 17-name test whose verdict
was "inconclusive, do not promote" (k unidentified, LOWO too weak).

Upgrades over v1:
  1. UNIVERSE: every multi-name market (EG SA US KR AE IN QA), 71 names,
     not 17. ADIBUAE excluded (byte-identical duplicate of ADIB).
  2. TEMPORAL WALK-FORWARD own-scale: s_own for window i is fit ONLY on that
     name's windows with origin strictly before i (expanding, min 4 priors;
     before that w=0 -> pure market LONO cal). This is deployment-faithful:
     at each origin only past residuals exist. v1's window-LOWO barely
     perturbed the fit and over-stated out-of-sample protection.
  3. k CROSS-FITTED LEAVE-TARGET-OUT: the k used to score name x is chosen by
     maximizing pooled walk-forward skill over names EXCLUDING x (per-market
     where the panel is big enough, global otherwise). Doubly out-of-sample:
     scale is walk-forward in time, k never sees the target name.
Known residual leakage, stated: s_l (market LONO scale) pools other names'
FULL histories, incl. windows after i. Production itself refits as data
arrives, so this matches the deploy loop; a fully-jackknifed variant would
change s_l by O(1/total-windows) and is second-order.

Read-only vs repo: writes results JSON to /home/claude/ only.
"""
import sys, os, json
sys.path.insert(0, '/home/claude/repo/engine')
import numpy as np
import pandas as pd
from scipy import stats

from mc_v3 import fit_nu_scale, shrink_cal, simulate_terminal_v3
from mc_v2 import crps_sample
from panel_refresh import (fast_rescore, robust_verdict, verdict_ci,
                           apply_breaks, panel_path, existing_panel_names)
from market_profiles import PROFILES

MARKETS = ['EG', 'SA', 'US', 'KR', 'AE', 'IN', 'QA']
EXCLUDE = {('AE', 'ADIBUAE')}          # byte-identical dupe of AE/ADIB
MIN_PRIOR = 4                          # windows of own history before w > 0
K_GRID = [0.5, 1, 2, 3, 5, 8, 12, 18, 25, 35, 50, 75, 110, 160, 250, 400, 700, 1200, 3000, 1e6]

# ---------------------------------------------------------------- load
panels, universe = {}, []
for mkt in MARKETS:
    for n in existing_panel_names(mkt):
        if (mkt, n) in EXCLUDE:
            continue
        r = apply_breaks(pd.read_csv(panel_path(mkt, n)), PROFILES[mkt])
        r = r.sort_values('origin').reset_index(drop=True)
        if len(r) == 0:
            continue
        panels[(mkt, n)] = r
        universe.append((mkt, n))
print(f"universe: {len(universe)} names, "
      f"{sum(len(panels[k]) for k in universe)} windows")

# ---------------------------------------------------------------- LONO market fits
lono = {}
for mkt, n in universe:
    others = [m for (mk, m) in universe if mk == mkt and m != n]
    u = np.concatenate([panels[(mkt, m)]['u'].values for m in others])
    lono[(mkt, n)] = fit_nu_scale(u)          # (nu_l, s_l)

OWN_S_GRID = np.linspace(0.30, 3.00, 271)

def fit_own_scale(u, nu_fixed, s_grid=OWN_S_GRID):
    u = np.asarray(u, float); u = u[np.isfinite(u)]
    if len(u) == 0:
        return 1.0
    if nu_fixed >= 200:
        ll = stats.norm.logpdf(u[None, :] / s_grid[:, None]).sum(1) - len(u) * np.log(s_grid)
    else:
        kk = np.sqrt(nu_fixed / (nu_fixed - 2))
        ll = stats.t.logpdf(u[None, :] * kk / s_grid[:, None], nu_fixed).sum(1) \
             + len(u) * (np.log(kk) - np.log(s_grid))
    return float(s_grid[np.argmax(ll)])

def rescore_percal(r, nu, cal_arr, n_paths=20000, seed=42):
    """Exact per-window rescore; identical math to fast_rescore but cal varies by row."""
    carry = r['drift'].values - r['alpha'].values
    sigma = r['sigma_h'].values * cal_arr
    drift = carry + r['alpha'].values * cal_arr
    spot = r['spot'].values; realized = r['realized'].values
    idx = r['origin_idx'].values
    out = np.empty(len(r))
    for i in range(len(r)):
        samp = simulate_terminal_v3(spot[i], sigma[i], drift[i], nu=nu,
                                    n_paths=n_paths, seed=int(seed + idx[i]))
        out[i] = crps_sample(samp, realized[i])
    return out

# sanity: rescore_percal == fast_rescore at constant cal, bit-for-bit
_r = panels[universe[0]]
_c1 = fast_rescore(_r, 8.0, 1.05)
_c2 = rescore_percal(_r, 8.0, np.full(len(_r), 1.05))
assert np.array_equal(_c1, _c2), "rescore_percal != fast_rescore at constant cal"
print("rescore_percal verified bit-for-bit against fast_rescore")

# ---------------------------------------------------------------- walk-forward own scales
wf = {}
for key in universe:
    r = panels[key]; nu_l, s_l = lono[key]
    u = r['u'].values; m = len(u)
    s_prior = np.empty(m)
    for i in range(m):
        s_prior[i] = fit_own_scale(u[:i], nu_l) if i >= MIN_PRIOR else np.nan
    wf[key] = s_prior

def wf_cal_arr(key, k):
    nu_l, s_l = lono[key]
    s_prior = wf[key]; m = len(s_prior)
    cal = np.empty(m)
    for i in range(m):
        if i < MIN_PRIOR or not np.isfinite(s_prior[i]):
            cal[i] = shrink_cal(s_l)
        else:
            w = i / (i + k)
            cal[i] = shrink_cal(w * s_prior[i] + (1 - w) * s_l)
    return cal

# ---------------------------------------------------------------- score all names x all k
per_k = {}          # (key, k) -> (crps_n_sum, crps_b_n_sum, crps_n_vec)
base = {}           # key -> dict of baselines
for key in universe:
    mkt, n = key
    r = panels[key]; nu_l, s_l = lono[key]
    cb = r['crps_b'].values; sp = r['spot'].values
    cal_lono = shrink_cal(s_l)
    c_lono = fast_rescore(r, nu_l, cal_lono)
    prof = PROFILES[mkt]
    c_prod = fast_rescore(r, prof.nu if prof.nu else 8.0, prof.width_cal)
    base[key] = dict(cbn=cb / sp, c_lono_n=c_lono / sp, c_prod_n=c_prod / sp,
                     cal_lono=cal_lono, nu_l=nu_l, s_l=s_l, m=len(r))
    for k in K_GRID:
        c = rescore_percal(r, nu_l, wf_cal_arr(key, k))
        per_k[(key, k)] = c / sp
    print(f"  scored {mkt}/{n} ({len(r)}w)", flush=True)

json_out = {'universe': [f"{m}/{n}" for m, n in universe]}
np.save('/home/claude/shrink_v2_cache.npy',
        np.array([1.0]))  # placeholder so reruns know phase 1 done
import pickle
with open('/home/claude/shrink_v2_state.pkl', 'wb') as f:
    pickle.dump(dict(per_k=per_k, base=base, lono=lono, wf=wf,
                     universe=universe, K_GRID=K_GRID), f)
print("state saved -> shrink_v2_state.pkl")
