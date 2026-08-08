"""Phase 2 — k selection (leave-target-out), verdicts, coverage, deploy table."""
import sys, os, json, pickle
sys.path.insert(0, '/home/claude/repo/engine')
import numpy as np
from scipy import stats
from mc_v3 import shrink_cal
from panel_refresh import robust_verdict, verdict_ci
from market_profiles import PROFILES

S = pickle.load(open('/home/claude/shrink_v2_state.pkl', 'rb'))
per_k, base, lono, wf, universe, K_GRID = (S[k] for k in
    ('per_k', 'base', 'lono', 'wf', 'universe', 'K_GRID'))
MKTS = ['EG', 'SA', 'US', 'KR', 'AE', 'IN', 'QA']
mkt_names = {m: [n for (mk, n) in universe if mk == m] for m in MKTS}
BIG = {m for m in MKTS if len(mkt_names[m]) >= 6}      # per-market k feasible

def pooled_skill(keys, k=None):
    """pooled WF-shrunk skill at fixed k (or LONO baseline if k is None)."""
    cs = sum(per_k[(key, k)].sum() if k is not None else base[key]['c_lono_n'].sum()
             for key in keys)
    cb = sum(base[key]['cbn'].sum() for key in keys)
    return 1 - cs / cb

# ---------------------------------------------------------------- 1. in-sample k curves
print("=== per-market pooled walk-forward skill vs k (in-sample curve) ===")
print(f"{'k':>7} | " + " | ".join(f"{m:>8}" for m in MKTS) + " |   GLOBAL")
for k in K_GRID:
    row = []
    for m in MKTS:
        keys = [(m, n) for n in mkt_names[m]]
        row.append(pooled_skill(keys, k))
    g = pooled_skill(universe, k)
    print(f"{k:>7} | " + " | ".join(f"{v:+.4f} " for v in row) + f" | {g:+.4f}")
print("   LONO | " + " | ".join(f"{pooled_skill([(m,n) for n in mkt_names[m]]):+.4f} "
                                for m in MKTS) + f" | {pooled_skill(universe):+.4f}")

# ---------------------------------------------------------------- 2. LTO k per name
k_lto = {}
for key in universe:
    mkt, n = key
    pool = ([(mkt, x) for x in mkt_names[mkt] if x != n] if mkt in BIG
            else [kk for kk in universe if kk != key])
    k_lto[key] = max(K_GRID, key=lambda k: pooled_skill(pool, k))

# ---------------------------------------------------------------- 3. pooled comparison
print("\n=== pooled skill: production vs LONO-const vs WF-shrunk(LTO-k) ===")
def pooled3(keys):
    cb = np.concatenate([base[key]['cbn'] for key in keys])
    cp = np.concatenate([base[key]['c_prod_n'] for key in keys])
    cl = np.concatenate([base[key]['c_lono_n'] for key in keys])
    cs = np.concatenate([per_k[(key, k_lto[key])] for key in keys])
    return cb, cp, cl, cs
rows_mkt = {}
for m in MKTS + ['GLOBAL']:
    keys = [(m, n) for n in mkt_names[m]] if m != 'GLOBAL' else universe
    cb, cp, cl, cs = pooled3(keys)
    sk = lambda c: 1 - c.sum() / cb.sum()
    # paired block bootstrap on the improvement (LONO -> shrunk), block=6
    rng = np.random.default_rng(42); nw = len(cb); diffs = []
    for _ in range(3000):
        starts = rng.integers(0, max(nw - 6 + 1, 1), size=int(np.ceil(nw / 6)))
        idx = np.concatenate([np.arange(s, s + 6) for s in starts])[:nw]
        diffs.append((1 - cs[idx].sum() / cb[idx].sum()) - (1 - cl[idx].sum() / cb[idx].sum()))
    lo, hi = np.percentile(diffs, [5, 95])
    verd = "IMPROVES" if lo > 0 else ("DEGRADES" if hi < 0 else "inconclusive")
    rows_mkt[m] = dict(prod=sk(cp), lono=sk(cl), shrunk=sk(cs),
                       d_lo=float(lo), d_hi=float(hi), call=verd)
    print(f"{m:>7}: prod {sk(cp):+.4f}  lono {sk(cl):+.4f}  shrunk {sk(cs):+.4f}  "
          f"d(shrunk-lono) CI90 [{lo:+.4f},{hi:+.4f}]  {verd}")

# ---------------------------------------------------------------- 4. per-name verdicts + coverage
def cov90_wf(key, k):
    r_u = None
    import pandas as pd
    from panel_refresh import panel_path, apply_breaks
    r = apply_breaks(pd.read_csv(panel_path(*key)), PROFILES[key[0]]).sort_values('origin')
    u = r['u'].values
    nu_l, s_l = lono[key]
    s_prior = wf[key]; m = len(u); cal = np.empty(m)
    for i in range(m):
        if i < 4 or not np.isfinite(s_prior[i]):
            cal[i] = shrink_cal(s_l)
        else:
            w = i / (i + k); cal[i] = shrink_cal(w * s_prior[i] + (1 - w) * s_l)
    z = u / cal
    if nu_l >= 200:
        q90 = stats.norm.ppf(0.95)
    else:
        kk = np.sqrt(nu_l / (nu_l - 2)); q90 = stats.t.ppf(0.95, nu_l) / kk
    return float(np.mean(np.abs(z) <= q90))

print("\n=== per-name: verdict LONO-const -> WF-shrunk(LTO-k); changes only ===")
per_name_rows = []
for key in universe:
    mkt, n = key
    cbn = base[key]['cbn']; cl = base[key]['c_lono_n']; cs = per_k[(key, k_lto[key])]
    v_l, _ = robust_verdict(cl, cbn)
    v_s, _ = robust_verdict(cs, cbn)
    sk_l = 1 - cl.sum() / cbn.sum(); sk_s = 1 - cs.sum() / cbn.sum()
    per_name_rows.append(dict(market=mkt, name=n, windows=int(base[key]['m']),
                              k_lto=float(k_lto[key]),
                              skill_lono=round(float(sk_l), 4), skill_shrunk=round(float(sk_s), 4),
                              verdict_lono=v_l, verdict_shrunk=v_s,
                              cov90_shrunk=round(cov90_wf(key, k_lto[key]), 3)))
    if v_l != v_s:
        print(f"  {mkt}/{n:14s} {v_l:>26s} -> {v_s:<26s} skill {sk_l:+.4f} -> {sk_s:+.4f}")
print("focus names:")
for mkt, n in [('KR','LGES'), ('AE','ALPHADHABI'), ('SA','ELM'), ('QA','IQCD')]:
    row = next(r for r in per_name_rows if r['market'] == mkt and r['name'] == n)
    print(f"  {mkt}/{n}: {row['verdict_lono']} -> {row['verdict_shrunk']} "
          f"skill {row['skill_lono']:+.4f} -> {row['skill_shrunk']:+.4f} "
          f"cov90_shrunk={row['cov90_shrunk']} k_lto={row['k_lto']}")

# ---------------------------------------------------------------- 5. k stability bootstrap
print("\n=== k stability: bootstrap names within market, argmax-k distribution ===")
rng = np.random.default_rng(7)
k_stab = {}
for m in ['EG', 'SA', 'AE']:
    keys = [(m, n) for n in mkt_names[m]]
    arg = []
    for _ in range(1000):
        draw = [keys[i] for i in rng.integers(0, len(keys), len(keys))]
        arg.append(max(K_GRID, key=lambda k: pooled_skill(draw, k)))
    vals, cnt = np.unique(arg, return_counts=True)
    top = sorted(zip(vals, cnt), key=lambda x: -x[1])[:4]
    k_stab[m] = dict(median=float(np.median(arg)),
                     iqr=[float(np.percentile(arg, 25)), float(np.percentile(arg, 75))],
                     top=[(float(v), int(c)) for v, c in top])
    print(f"  {m}: median={np.median(arg)}, IQR=[{np.percentile(arg,25)}, "
          f"{np.percentile(arg,75)}], top: " +
          ", ".join(f"k={v} ({100*c/1000:.0f}%)" for v, c in top))

json.dump(dict(markets=rows_mkt, per_name=per_name_rows, k_stability=k_stab,
               k_lto={f"{m}/{n}": float(k) for (m, n), k in k_lto.items()}),
          open('/home/claude/shrink_v2_results.json', 'w'), indent=2, default=str)
print("\nsaved shrink_v2_results.json")
