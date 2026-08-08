"""
Name-level width_cal shrinkage — proposed candidate, tested LOCALLY and READ-ONLY
against the actual production machinery. Nothing in repo/engine is modified;
nothing is committed or pushed. This is exactly the TOP OPEN ITEM from the
Standing Research Protocol: "a NAME-LEVEL width_cal shrunk toward the market
fit ... PROPOSED, NOT BUILT -- must clear the same LONO gate that killed the
CRPS-selection idea."

Design (kept deliberately close to the existing LONO/robust-verdict machinery
so this is a genuine apples-to-apples test, not a new methodology):

  - nu stays at the MARKET LONO fit (nu_l, fit on every OTHER name in the same
    market) -- nu is weakly identified system-wide; fitting it per name on
    13-40 windows would be noise, and the TOP OPEN ITEM text itself only calls
    for width_cal to move, not nu.
  - Each name's own scale s_own is a 1-parameter MLE (nu held at nu_l) on that
    name's own standardized residuals ('u', already computed by the real
    production panel files at the baseline nu=8/cal=1).
  - Credibility-weighted blend: s_shrunk = w*s_own + (1-w)*s_l,
    w = n_windows / (n_windows + k). Small-history names (LGES ~13-15 windows)
    shrink hard toward the market; well-populated names barely move. k is the
    ONE free hyperparameter.
  - k is chosen by held-out performance, not by making LGES/ALPHADHABI look
    good: pooled, doubly out-of-sample --
      (a) LONO across names (s_l excludes the target name entirely), same as
          the existing per-name verdict machinery, AND
      (b) LOWO across the target name's OWN windows (s_own for window i is
          fit on that name's windows EXCLUDING i), so a name's own score never
          leans on the very residual being graded.
    This avoids the exact trap the protocol already flagged once: "selecting
    (nu, width_cal) by maximising CRPS skill instead of MLE looked clearly
    better IN-SAMPLE and LOST under LONO ... REJECTED."
  - Final "deploy" number per name uses ALL of that name's own windows (no
    LOWO) blended with the LONO market fit -- same convention the existing
    per-name verdict already uses (score honestly out-of-sample; deploy on
    full data).

Scope: KR (SAMSUNG/KAKAO/LGES) + the 14 names that are ACTUALLY in AE's live
fitted panel per fitted_configs.json (ADCB/ADIB/ADNOCGAS/AGTHIA/ALDAR/
ALPHADHABI/DIB/EAND/EMAAR/EMAARDEV/ENBD/FAB/IHC/TWOPOINTZERO) = 17 names.
Four AE raw files (BURJEEL/DEWA/LULU/SALIK) plus a byte-identical ADIB
duplicate (ADIBUAE) exist in raw_ohlc/AE but have NEVER been through the
panel-build pipeline (panel_hashes.json has no entry for them) -- they are
NOT part of what production currently treats as the AE panel, so including
them would be widening scope beyond "the existing procedure", not testing
against it. Flagged separately, not touched.
"""
import sys, os, json
sys.path.insert(0, '/tmp/testahil_work/repo/engine')
import numpy as np
import pandas as pd
from scipy import stats

from mc_v3 import fit_nu_scale, shrink_cal, simulate_terminal_v3
from mc_v2 import crps_sample
from panel_refresh import fast_rescore, robust_verdict, verdict_ci, apply_breaks, MIN_HISTORY
from market_profiles import PROFILES

PANELS_DIR = '/tmp/testahil_work/repo/engine/panels'

KR_NAMES = ["SAMSUNG", "KAKAO", "LGES"]
AE_NAMES = ["ADCB", "ADIB", "ADNOCGAS", "AGTHIA", "ALDAR", "ALPHADHABI", "DIB",
            "EAND", "EMAAR", "EMAARDEV", "ENBD", "FAB", "IHC", "TWOPOINTZERO"]

MARKETS = {"KR": KR_NAMES, "AE": AE_NAMES}


def load_panel(market, name):
    r = pd.read_csv(os.path.join(PANELS_DIR, f"{market}_{name}_60d.csv"))
    r = apply_breaks(r, PROFILES[market])
    return r.reset_index(drop=True)


panels = {}
for mkt, names in MARKETS.items():
    for n in names:
        panels[(mkt, n)] = load_panel(mkt, n)

print("=== panel sizes (post break-filter) ===")
for mkt, names in MARKETS.items():
    for n in names:
        print(f"  {mkt}/{n}: {len(panels[(mkt, n)])} windows")

# ---------------------------------------------------------------- reproduction check
print("\n=== reproduction check: pooled fit vs live registry ===")
for mkt, names in MARKETS.items():
    u_all = np.concatenate([panels[(mkt, n)]['u'].values for n in names])
    nu_p, s_p = fit_nu_scale(u_all)
    cal_p = shrink_cal(s_p)
    nu_disp = round(float(nu_p), 3) if nu_p < 200 else "Gaussian"
    live = PROFILES[mkt]
    live_nu_disp = "Gaussian" if live.nu is None or live.nu >= 200 else live.nu
    print(f"  {mkt}: mine nu={nu_disp} cal={cal_p:.3f} (n={len(u_all)})  |  "
          f"live nu={live_nu_disp} cal={live.width_cal:.3f}")


# ---------------------------------------------------------------- LONO (across names)
def lono_fit(mkt, names, exclude):
    others = [n for n in names if n != exclude]
    u = np.concatenate([panels[(mkt, n)]['u'].values for n in others])
    nu_l, s_l = fit_nu_scale(u)
    return nu_l, s_l


# ---------------------------------------------------------------- own-name scale MLE
OWN_S_GRID = np.linspace(0.30, 3.00, 271)


def fit_own_scale(u, nu_fixed, s_grid=OWN_S_GRID):
    u = np.asarray(u, float)
    u = u[np.isfinite(u)]
    if len(u) == 0:
        return 1.0
    best = (-np.inf, 1.0)
    if nu_fixed >= 200:
        for s in s_grid:
            ll = stats.norm.logpdf(u / s).sum() - len(u) * np.log(s)
            if ll > best[0]:
                best = (ll, s)
    else:
        k = np.sqrt(nu_fixed / (nu_fixed - 2))
        for s in s_grid:
            ll = stats.t.logpdf(u * k / s, nu_fixed).sum() + len(u) * (np.log(k) - np.log(s))
            if ll > best[0]:
                best = (ll, s)
    return float(best[1])


# ---------------------------------------------------------------- per-row rescoring
# Same math as panel_refresh.fast_rescore, generalized to accept a PER-ROW cal
# array (fast_rescore only takes one scalar cal for the whole name). Verified
# against fast_rescore for the scalar case below before use.
def rescore_percal(r, nu, cal_arr, n_paths=20000, seed=42):
    carry = r['drift'].values - r['alpha'].values
    sigma = r['sigma_h'].values * cal_arr
    drift = carry + r['alpha'].values * cal_arr
    spot = r['spot'].values
    realized = r['realized'].values
    idx = r['origin_idx'].values
    out = np.empty(len(r))
    for i in range(len(r)):
        samp = simulate_terminal_v3(spot[i], sigma[i], drift[i], nu=nu,
                                     n_paths=n_paths, seed=int(seed + idx[i]))
        out[i] = crps_sample(samp, realized[i])
    return out


# sanity: rescore_percal with a constant cal array must equal fast_rescore exactly
_test_r = panels[("KR", "SAMSUNG")]
_c1 = fast_rescore(_test_r, 8.0, 1.03)
_c2 = rescore_percal(_test_r, 8.0, np.full(len(_test_r), 1.03))
assert np.allclose(_c1, _c2), "rescore_percal does not match fast_rescore for constant cal!"
print("\n[sanity] rescore_percal verified bit-for-bit identical to fast_rescore for constant cal.")


def cov_pit(u, nu, cal):
    u = np.asarray(u, float) / cal
    if nu >= 200:
        pit = stats.norm.cdf(u)
        q = lambda p: stats.norm.ppf(p)
    else:
        kk = np.sqrt(nu / (nu - 2))
        pit = stats.t.cdf(u * kk, nu)
        q = lambda p: stats.t.ppf(p, nu) / kk
    inb = lambda p: float(np.mean(np.abs(u) <= q(0.5 + p / 2)))
    return dict(pit_mean=float(pit.mean()), cov50=inb(0.50), cov80=inb(0.80), cov90=inb(0.90))


ALL_NAMES = [(mkt, n) for mkt, names in MARKETS.items() for n in names]

# ---------------------------------------------------------------- precompute per-name LONO + own-scale (LOWO)
precomp = {}
for mkt, n in ALL_NAMES:
    names = MARKETS[mkt]
    nu_l, s_l = lono_fit(mkt, names, n)
    r = panels[(mkt, n)]
    u_own = r['u'].values
    m = len(u_own)
    # leave-one-WINDOW-out own-scale, one fit per window (own-history only, never the held-out residual)
    s_own_lowo = np.empty(m)
    for i in range(m):
        mask = np.ones(m, dtype=bool)
        mask[i] = False
        s_own_lowo[i] = fit_own_scale(u_own[mask], nu_l)
    # full-data own-scale (for the "deploy" number, not for scoring)
    s_own_full = fit_own_scale(u_own, nu_l)
    precomp[(mkt, n)] = dict(nu_l=nu_l, s_l=s_l, m=m, s_own_lowo=s_own_lowo, s_own_full=s_own_full)

print("\n=== per-name LONO market fit + own-scale (own vs market) ===")
for mkt, n in ALL_NAMES:
    p = precomp[(mkt, n)]
    nu_disp = round(float(p['nu_l']), 2) if p['nu_l'] < 200 else "Gaussian"
    print(f"  {mkt}/{n:12s} windows={p['m']:3d}  nu_l={nu_disp:>8}  s_l(market)={p['s_l']:.3f}  "
          f"s_own(full)={p['s_own_full']:.3f}  ratio={p['s_own_full']/p['s_l']:.2f}x")

# ---------------------------------------------------------------- grid search over k
K_GRID = [0.5, 1, 2, 3, 5, 8, 12, 18, 25, 35, 50, 75, 110, 160, 250, 400, 700, 1200, 3000, 1e6]

grid_results = []
for k in K_GRID:
    tot_c_shrunk, tot_c_lonoOnly, tot_cb = 0.0, 0.0, 0.0
    for mkt, n in ALL_NAMES:
        p = precomp[(mkt, n)]
        r = panels[(mkt, n)]
        m = p['m']
        w_lowo = m_arr = (m - 1) / ((m - 1) + k) if m > 1 else 0.0
        cal_arr_shrunk = np.array([shrink_cal(w_lowo * p['s_own_lowo'][i] + (1 - w_lowo) * p['s_l'])
                                    for i in range(m)])
        c_shrunk = rescore_percal(r, p['nu_l'], cal_arr_shrunk)
        cal_lonoOnly = shrink_cal(p['s_l'])
        c_lonoOnly = fast_rescore(r, p['nu_l'], cal_lonoOnly)
        cb = r['crps_b'].values
        spot = r['spot'].values
        tot_c_shrunk += (c_shrunk / spot).sum()
        tot_c_lonoOnly += (c_lonoOnly / spot).sum()
        tot_cb += (cb / spot).sum()
    skill_shrunk = 1 - tot_c_shrunk / tot_cb
    skill_lonoOnly = 1 - tot_c_lonoOnly / tot_cb
    grid_results.append(dict(k=k, skill_shrunk=skill_shrunk, skill_lonoOnly=skill_lonoOnly,
                              delta=skill_shrunk - skill_lonoOnly))

print("\n=== k grid search: pooled out-of-sample skill (17 names, LOWO+LONO, scale-normalized) ===")
print(f"  {'k':>8} {'skill_shrunk':>13} {'skill_LONO-only':>16} {'delta':>9}")
for g in grid_results:
    print(f"  {g['k']:>8} {g['skill_shrunk']:>13.5f} {g['skill_lonoOnly']:>16.5f} {g['delta']:>9.5f}")

best = max(grid_results, key=lambda g: g['skill_shrunk'])
print(f"\n>>> best k = {best['k']}  (skill_shrunk={best['skill_shrunk']:+.5f} vs "
      f"LONO-only={best['skill_lonoOnly']:+.5f}, delta={best['delta']:+.5f})")

json.dump(dict(panel_sizes={f"{m}/{n}": len(panels[(m, n)]) for m, n in ALL_NAMES},
               grid_results=grid_results, best_k=best['k']),
          open('/tmp/testahil_work/grid_search.json', 'w'), indent=2)
