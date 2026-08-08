import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import crps_sample
from mc_v3 import simulate_terminal_v3
from panel_refresh import robust_verdict, verdict_ci

r = pd.read_pickle('/tmp/ta/records.pkl')
SIGS = ['brk20', 'macd', 'rsi', 'rev_1m']
NPATHS, SEED, BCAP = 20000, 42, 0.10

# --- verify exp-rescale shortcut vs direct sim (bit-for-bit) ---
row = r.iloc[100]
a = 0.0123
s1 = simulate_terminal_v3(row.spot, row.sigma_h, row.carry + a, nu=4.0, n_paths=NPATHS, seed=SEED + int(row.oidx))
s0 = simulate_terminal_v3(row.spot, row.sigma_h, row.carry, nu=4.0, n_paths=NPATHS, seed=SEED + int(row.oidx))
assert np.allclose(s1, s0 * np.exp(a), rtol=0, atol=1e-9 * row.spot)
print("exp-rescale shortcut verified bit-for-bit")

# --- LONO slopes: for name j, OLS slope of u on clip(z) pooled over others ---
slopes = {}
for h in (5, 10):
    rh = r[r.h == h]
    for j in rh.name.unique():
        tr = rh[rh.name != j]
        for k in SIGS:
            zc = np.clip(tr[k].values, -2, 2)
            u = tr.u.values
            ok = np.isfinite(zc) & np.isfinite(u)
            zc, u = zc[ok], u[ok]
            b = np.polyfit(zc, u, 1)[0]
            slopes[(h, j, k)] = float(np.clip(b, -BCAP, BCAP))
raw_pooled = {}
for h in (5, 10):
    rh = r[r.h == h]
    for k in SIGS:
        zc = np.clip(rh[k].values, -2, 2); u = rh.u.values
        raw_pooled[(h, k)] = float(np.polyfit(zc, u, 1)[0])
print("pooled slopes (uncapped):", {f"h{h}:{k}": round(v, 4) for (h, k), v in raw_pooled.items()})

# --- pass 2: paired CRPS ---
out = {k: np.zeros(len(r)) for k in SIGS}
crps_off = np.zeros(len(r)); crps_bench = np.zeros(len(r))
alphas = {k: np.zeros(len(r)) for k in SIGS}
for i, row in enumerate(r.itertuples()):
    samp = simulate_terminal_v3(row.spot, row.sigma_h, row.carry, nu=4.0,
                                n_paths=NPATHS, seed=SEED + int(row.oidx))
    crps_off[i] = crps_sample(samp, row.y)
    rngb = np.random.default_rng(SEED + int(row.oidx) + 1)
    bench = row.spot * np.exp(row.carry + row.sig_b * rngb.standard_normal(NPATHS))
    crps_bench[i] = crps_sample(bench, row.y)
    for k in SIGS:
        z = getattr(row, k)
        if abs(z) < 0.5:
            a = 0.0
        else:
            b = slopes[(row.h, row.name, k)]
            a = float(np.clip(b * row.sigma_h * np.clip(z, -2, 2), -0.5 * row.sigma_h, 0.5 * row.sigma_h))
        alphas[k][i] = a
        out[k][i] = crps_off[i] if a == 0.0 else crps_sample(samp * np.exp(a), row.y)

r['crps_off'] = crps_off; r['crps_bench'] = crps_bench
for k in SIGS:
    r[f'crps_{k}'] = out[k]; r[f'alpha_{k}'] = alphas[k]
r.to_pickle('/tmp/ta/scored.pkl')

# --- verdicts ---
res = []
for h in (5, 10):
    rh = r[r.h == h]
    base = 1 - (rh.crps_off / rh.spot).sum() / (rh.crps_bench / rh.spot).sum()
    for k in SIGS:
        on = (rh[f'crps_{k}'] / rh.spot).values; off = (rh.crps_off / rh.spot).values
        d = 1 - on.sum() / off.sum()
        verd, detail = robust_verdict(on, off)
        fired = float((rh[f'alpha_{k}'] != 0).mean())
        res.append(dict(h=h, signal=k, dskill=round(d, 5), fired=round(fired, 3),
                        verdict=verd, ci2=[round(x, 4) for x in detail[2][:2]],
                        ci3=[round(x, 4) for x in detail[3][:2]],
                        ci4=[round(x, 4) for x in detail[4][:2]],
                        base_skill_off=round(float(base), 4)))
res = pd.DataFrame(res)
print(res.to_string(index=False))
res.to_json('/tmp/ta/verdicts.json', orient='records')

# --- conditional terciles: mean u by z-tercile (route-3 evidence) ---
print("\nmean standardized fwd return u by z-tercile (pooled, post-break):")
for h in (5, 10):
    rh = r[r.h == h]
    for k in SIGS:
        q = pd.qcut(rh[k], 3, labels=['lo', 'mid', 'hi'], duplicates='drop')
        m = rh.groupby(q, observed=True).u.agg(['mean', 'size'])
        print(f"h={h} {k:7s}", {i: (round(row['mean'], 3), int(row['size'])) for i, row in m.iterrows()})
