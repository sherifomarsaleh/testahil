"""
Phase 2: (a) bootstrap the k-selection over names to see how stable/noisy the
"optimal" k really is (guards against picking a plateau artifact), then
(b) full per-name before/after table at a chosen, defensibly-conservative k:
cal, coverage, PIT, robust verdict, skill -- current production vs honest
LONO-only vs shrunk. (c) recombined market-level panel check.
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
ALL_NAMES = [(mkt, n) for mkt, names in MARKETS.items() for n in names]


def load_panel(market, name):
    r = pd.read_csv(os.path.join(PANELS_DIR, f"{market}_{name}_60d.csv"))
    return apply_breaks(r, PROFILES[market]).reset_index(drop=True)


panels = {(mkt, n): load_panel(mkt, n) for mkt, names in MARKETS.items() for n in names}


def lono_fit(mkt, names, exclude):
    others = [n for n in names if n != exclude]
    u = np.concatenate([panels[(mkt, n)]['u'].values for n in others])
    return fit_nu_scale(u)  # (nu_l, s_l)


OWN_S_GRID = np.linspace(0.30, 3.00, 271)


def fit_own_scale(u, nu_fixed, s_grid=OWN_S_GRID):
    u = np.asarray(u, float); u = u[np.isfinite(u)]
    if len(u) == 0:
        return 1.0
    best = (-np.inf, 1.0)
    if nu_fixed >= 200:
        for s in s_grid:
            ll = stats.norm.logpdf(u / s).sum() - len(u) * np.log(s)
            if ll > best[0]:
                best = (ll, s)
    else:
        kk = np.sqrt(nu_fixed / (nu_fixed - 2))
        for s in s_grid:
            ll = stats.t.logpdf(u * kk / s, nu_fixed).sum() + len(u) * (np.log(kk) - np.log(s))
            if ll > best[0]:
                best = (ll, s)
    return float(best[1])


def rescore_percal(r, nu, cal_arr, n_paths=20000, seed=42):
    carry = r['drift'].values - r['alpha'].values
    sigma = r['sigma_h'].values * cal_arr
    drift = carry + r['alpha'].values * cal_arr
    spot = r['spot'].values; realized = r['realized'].values; idx = r['origin_idx'].values
    out = np.empty(len(r))
    for i in range(len(r)):
        samp = simulate_terminal_v3(spot[i], sigma[i], drift[i], nu=nu, n_paths=n_paths, seed=int(seed + idx[i]))
        out[i] = crps_sample(samp, realized[i])
    return out


def cov_pit(u, nu, cal):
    u = np.asarray(u, float) / cal
    if nu >= 200:
        pit = stats.norm.cdf(u); q = lambda p: stats.norm.ppf(p)
    else:
        kk = np.sqrt(nu / (nu - 2)); pit = stats.t.cdf(u * kk, nu); q = lambda p: stats.t.ppf(p, nu) / kk
    inb = lambda p: float(np.mean(np.abs(u) <= q(0.5 + p / 2)))
    return dict(pit_mean=float(pit.mean()), cov50=inb(0.50), cov80=inb(0.80), cov90=inb(0.90))


# ---------------------------------------------------------------- precompute (same as phase 1)
precomp = {}
for mkt, n in ALL_NAMES:
    names = MARKETS[mkt]
    nu_l, s_l = lono_fit(mkt, names, n)
    r = panels[(mkt, n)]
    u_own = r['u'].values
    m = len(u_own)
    s_own_lowo = np.empty(m)
    for i in range(m):
        mask = np.ones(m, dtype=bool); mask[i] = False
        s_own_lowo[i] = fit_own_scale(u_own[mask], nu_l)
    s_own_full = fit_own_scale(u_own, nu_l)
    precomp[(mkt, n)] = dict(nu_l=nu_l, s_l=s_l, m=m, s_own_lowo=s_own_lowo, s_own_full=s_own_full)

K_GRID = [0.5, 1, 2, 3, 5, 8, 12, 18, 25, 35, 50, 75, 110, 160, 250, 400, 700, 1200, 3000, 1e6]

# ---------------------------------------------------------------- cache per-name per-k (c_shrunk_sum, cb_sum)
percomp_by_k = {k: {} for k in K_GRID}
for k in K_GRID:
    for mkt, n in ALL_NAMES:
        p = precomp[(mkt, n)]; r = panels[(mkt, n)]; m = p['m']
        w = (m - 1) / ((m - 1) + k) if m > 1 else 0.0
        cal_arr = np.array([shrink_cal(w * p['s_own_lowo'][i] + (1 - w) * p['s_l']) for i in range(m)])
        c = rescore_percal(r, p['nu_l'], cal_arr)
        cb = r['crps_b'].values; spot = r['spot'].values
        percomp_by_k[k][(mkt, n)] = (float((c / spot).sum()), float((cb / spot).sum()))

print("=== bootstrap: resample names (with replacement), find argmax-k each draw ===")
rng = np.random.default_rng(7)
names_list = ALL_NAMES
n_boot = 2000
argmax_ks = []
for _ in range(n_boot):
    draw = [names_list[i] for i in rng.integers(0, len(names_list), len(names_list))]
    best_k, best_skill = None, -np.inf
    for k in K_GRID:
        cs = sum(percomp_by_k[k][nm][0] for nm in draw)
        cbs = sum(percomp_by_k[k][nm][1] for nm in draw)
        sk = 1 - cs / cbs
        if sk > best_skill:
            best_skill, best_k = sk, k
    argmax_ks.append(best_k)
argmax_ks = np.array(argmax_ks)
vals, counts = np.unique(argmax_ks, return_counts=True)
print("  distribution of argmax-k across 2000 name-resamples:")
for v, c in sorted(zip(vals, counts), key=lambda x: -x[1]):
    print(f"    k={v:>10}: {c:>5} draws ({100*c/n_boot:.1f}%)")
print(f"  median argmax-k = {np.median(argmax_ks)}, 25th/75th pct = "
      f"{np.percentile(argmax_ks,25)}/{np.percentile(argmax_ks,75)}")

CHOSEN_K = 12.0  # conservative pick from the flat, high-density part of the plateau -- see report
print(f"\n>>> using k={CHOSEN_K} for the detailed report (robust middle of the plateau, "
      f"not the raw single-sample argmax -- see bootstrap distribution above)")

# ---------------------------------------------------------------- detailed per-name table
rows_out = []
print(f"\n{'name':14s} {'m':>3} {'prod_cal':>9} {'lono_cal':>9} {'shrunk_cal':>10} "
      f"{'sk_prod':>9} {'sk_lono':>9} {'sk_shrunk':>10} "
      f"{'cov90_lono':>11} {'cov90_shr':>10} {'pit_lono':>9} {'pit_shr':>8} {'verdict_shr':>13}")
for mkt, n in ALL_NAMES:
    p = precomp[(mkt, n)]; r = panels[(mkt, n)]; m = p['m']
    nu_l = p['nu_l']
    prod_nu_disp = "Gaussian" if PROFILES[mkt].nu is None or PROFILES[mkt].nu >= 200 else PROFILES[mkt].nu
    cal_prod = PROFILES[mkt].width_cal
    cal_lono = shrink_cal(p['s_l'])
    w = (m - 1) / ((m - 1) + CHOSEN_K)
    s_shrunk_full = w * p['s_own_full'] + (1 - w) * p['s_l']
    cal_shrunk = shrink_cal(s_shrunk_full)

    c_prod = fast_rescore(r, PROFILES[mkt].nu if PROFILES[mkt].nu else 8.0, cal_prod)
    c_lono = fast_rescore(r, nu_l, cal_lono)
    c_shrunk = fast_rescore(r, nu_l, cal_shrunk)
    cb = r['crps_b'].values; spot = r['spot'].values
    sk_prod = 1 - (c_prod / spot).sum() / (cb / spot).sum()
    sk_lono = 1 - (c_lono / spot).sum() / (cb / spot).sum()
    sk_shrunk = 1 - (c_shrunk / spot).sum() / (cb / spot).sum()

    cp_lono = cov_pit(r['u'].values, nu_l, cal_lono)
    cp_shrunk = cov_pit(r['u'].values, nu_l, cal_shrunk)

    verd_shrunk, detail_shrunk = robust_verdict(c_shrunk / spot, cb / spot)
    verd_lono, detail_lono = robust_verdict(c_lono / spot, cb / spot)

    print(f"{mkt+'/'+n:14s} {m:>3} {cal_prod:>9.3f} {cal_lono:>9.3f} {cal_shrunk:>10.3f} "
          f"{sk_prod:>+9.4f} {sk_lono:>+9.4f} {sk_shrunk:>+10.4f} "
          f"{cp_lono['cov90']:>11.2f} {cp_shrunk['cov90']:>10.2f} "
          f"{cp_lono['pit_mean']:>9.3f} {cp_shrunk['pit_mean']:>8.3f} {verd_shrunk:>13s}")
    rows_out.append(dict(market=mkt, name=n, windows=m, cal_prod=round(cal_prod,3),
                          cal_lono=round(cal_lono,3), cal_shrunk=round(cal_shrunk,3),
                          skill_prod=round(sk_prod,4), skill_lono=round(sk_lono,4), skill_shrunk=round(sk_shrunk,4),
                          cov90_lono=round(cp_lono['cov90'],3), cov90_shrunk=round(cp_shrunk['cov90'],3),
                          cov80_lono=round(cp_lono['cov80'],3), cov80_shrunk=round(cp_shrunk['cov80'],3),
                          pit_lono=round(cp_lono['pit_mean'],3), pit_shrunk=round(cp_shrunk['pit_mean'],3),
                          verdict_lono=verd_lono, verdict_shrunk=verd_shrunk))

print(f"\nverdict changes (LONO-only -> shrunk) at k={CHOSEN_K}:")
for row in rows_out:
    if row['verdict_lono'] != row['verdict_shrunk']:
        print(f"  {row['market']}/{row['name']}: {row['verdict_lono']} -> {row['verdict_shrunk']}")

# ---------------------------------------------------------------- market-level recombination
print(f"\n=== market-level panel check at k={CHOSEN_K}: heterogeneous per-name cal vs uniform production cal ===")
for mkt, names in MARKETS.items():
    allc_prod, allb, allc_shrunk = [], [], []
    for n in names:
        p = precomp[(mkt, n)]; r = panels[(mkt, n)]; m = p['m']
        cal_prod = PROFILES[mkt].width_cal
        w = (m - 1) / ((m - 1) + CHOSEN_K)
        cal_shrunk = shrink_cal(w * p['s_own_full'] + (1 - w) * p['s_l'])
        c_prod = fast_rescore(r, PROFILES[mkt].nu if PROFILES[mkt].nu else 8.0, cal_prod)
        c_shrunk = fast_rescore(r, p['nu_l'], cal_shrunk)
        cb = r['crps_b'].values; spot = r['spot'].values
        allc_prod.append(c_prod / spot); allb.append(cb / spot); allc_shrunk.append(c_shrunk / spot)
    ac_prod, ab, ac_shrunk = np.concatenate(allc_prod), np.concatenate(allb), np.concatenate(allc_shrunk)
    sk_prod = 1 - ac_prod.sum() / ab.sum()
    sk_shrunk = 1 - ac_shrunk.sum() / ab.sum()
    lo_p, hi_p, v_p = verdict_ci(ac_prod, ab, block=6)
    lo_s, hi_s, v_s = verdict_ci(ac_shrunk, ab, block=6)
    print(f"  {mkt}: production skill={sk_prod:+.4f} CI90=[{lo_p:.3f},{hi_p:.3f}] {v_p}  |  "
          f"per-name-shrunk skill={sk_shrunk:+.4f} CI90=[{lo_s:.3f},{hi_s:.3f}] {v_s}")

json.dump(dict(chosen_k=CHOSEN_K, bootstrap_argmax_median=float(np.median(argmax_ks)),
               bootstrap_argmax_iqr=[float(np.percentile(argmax_ks,25)), float(np.percentile(argmax_ks,75))],
               per_name=rows_out),
          open('/tmp/testahil_work/detailed_report.json', 'w'), indent=2)
print("\nsaved detailed_report.json")
