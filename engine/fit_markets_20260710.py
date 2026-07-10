"""Fit nu + width_cal PER MARKET on each market's own pooled panel, then
re-score every covered name under ITS OWN market's fitted config.
Standing rule (10-Jul-2026): a market lacking its own fitted shape/width must
fit it on its own panel before any name-level FAIL is treated as real."""
import sys, glob, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mc_v3 import fit_nu_scale, shrink_cal, backtest_v3
from mc_v2 import load_ohlc
from market_profiles import PROFILES

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panels')

def load_market(code):
    out = {}
    for f in sorted(glob.glob(f"{P}/{code}_*_60d.csv")):
        name = os.path.basename(f).split('_')[1]
        out[name] = pd.read_csv(f)
    return out

def verdict_ci(crps, crps_b, n_boot=3000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(crps); block = max(2, n // 6)
    boot = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        boot.append(1 - crps[idx].sum() / crps_b[idx].sum())
    lo, hi = np.percentile(boot, [5, 95])
    v = "PASS" if lo > 0 else ("FAIL" if hi < 0 else "PARITY")
    return lo, hi, v

def rescore(df_ohlc, profile, nu, cal):
    rows = backtest_v3(df_ohlc, profile, horizon=60, nu=nu, width_cal=cal,
                       use_signal=profile.signal_active, n_paths=20000, seed=42)
    r = pd.DataFrame(rows)
    skill = 1 - r['crps'].sum() / r['crps_b'].sum()
    lo, hi, v = verdict_ci(r['crps'].values, r['crps_b'].values)
    return skill, lo, hi, v, r

CSVS = {  # OHLC available this session for re-scoring
    'EG': {'PHDC': '/mnt/project/Palm_Hills_Develop_Stock_Price_History.csv',
           'TMGH': '/mnt/project/T_M_G_Holding_Stock_Price_History.csv',
           'EMFD': '/mnt/project/Emaar_Misr_for_Development_SAE_Stock_Price_History.csv',
           'OCDI': '/mnt/project/SODIC_Stock_Price_History.csv',
           'ORHD': '/mnt/project/Orascom_Hotels_Stock_Price_History2.csv',
           'GBCO': '/mnt/project/GB_AUTO_Stock_Price_History.csv',
           'KABO': '/mnt/user-data/uploads/El_Nasr_Clothing___Textiles_Stock_Price_History.csv'},
    'SA': {'ALINMA': '/mnt/user-data/uploads/Alinma_Stock_Price_History.csv',
           'MAADEN': '/mnt/user-data/uploads/Ma_aden_Stock_Price_History.csv'},
    'QA': {'QGTS': '/mnt/user-data/uploads/Gas_Transport_Co_Stock_Price_History.csv'},
    'XAU': {'GOLD': '/mnt/project/XAU_USD_Historical_Data.csv'},
}

results = {}
for code in ['EG', 'SA', 'QA', 'XAU']:
    panel = load_market(code)
    if code == 'XAU' and not panel:
        # build the metals panel from gold OHLC under the METALS profile
        prof = PROFILES['XAU']
        df = load_ohlc(CSVS['XAU']['GOLD'])
        rows = backtest_v3(df, prof, horizon=60, nu=1e9, width_cal=1.0,
                           use_signal=False, n_paths=20000, seed=42)
        fr = pd.DataFrame(rows)
        fr.to_csv(f"{P}/XAU_GOLD_60d.csv", index=False)
        panel = {'GOLD': fr}
    prof = PROFILES[code]
    names = list(panel)
    pooled_u = np.concatenate([panel[n]['u'].values for n in names])
    nu_pool, s_pool = fit_nu_scale(pooled_u)
    cal_pool = shrink_cal(s_pool)
    # LONO fits (fit excluding the name, used for that name's own verdict)
    lono = {}
    for n in names:
        if len(names) >= 2:
            u = np.concatenate([panel[m]['u'].values for m in names if m != n])
            nu_l, s_l = fit_nu_scale(u); lono[n] = (nu_l, shrink_cal(s_l))
        else:
            lono[n] = (nu_pool, cal_pool)  # single-name market: self-fit, FLAGGED
    print(f"\n=== {code} ({prof.name}) — {len(names)} names, {len(pooled_u)} windows ===")
    print(f"POOLED production fit: nu={nu_pool:.0f}, mle_scale={s_pool:.3f}, width_cal={cal_pool:.3f}"
          + ("  [SINGLE-NAME SELF-FIT — provisional]" if len(names) < 2 else ""))
    per = []
    for n in names:
        nu_l, cal_l = lono[n]
        sk, lo, hi, v, _ = rescore(load_ohlc(CSVS[code][n]), prof, nu_l, cal_l)
        per.append((n, nu_l, cal_l, sk, lo, hi, v))
        print(f"  {n:7s} nu={nu_l:>4.0f} cal={cal_l:.2f}  skill={sk:+.4f}  CI[{lo:+.3f},{hi:+.3f}]  {v}")
    # market pooled verdict under production fit
    allc, allb = [], []
    for n in names:
        _, _, _, _, r = rescore(load_ohlc(CSVS[code][n]), prof, nu_pool, cal_pool)
        allc.append(r['crps'].values); allb.append(r['crps_b'].values)
    ac, ab = np.concatenate(allc), np.concatenate(allb)
    sk = 1 - ac.sum() / ab.sum(); lo, hi, v = verdict_ci(ac, ab)
    print(f"  MARKET PANEL under pooled fit: skill={sk:+.4f}  CI[{lo:+.3f},{hi:+.3f}]  {v}")
    results[code] = dict(nu=nu_pool, cal=cal_pool, s=s_pool, names=names,
                         windows=len(pooled_u), panel_skill=sk, ci=(lo, hi), verdict=v, per=per)

import json
print("\n" + json.dumps({k: {kk: (vv if not isinstance(vv, (list, tuple)) or kk=='names' else str(vv))
      for kk, vv in v.items() if kk != 'per'} for k, v in results.items()}, indent=1, default=str))
