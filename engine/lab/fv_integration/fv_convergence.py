"""How far / how long: does the market's OWN calibrated vol+carry (no
fundamental input, no signal) make reaching the DCF fair-value zone a
statistically ordinary event, and on what timescale? Diagnostic only —
NOT a prediction, NOT an engine change. Same production chain as route 1,
just extended to multi-year horizons and priced against fair-value levels
instead of chart S/R."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_paths_v3
from data_quality import clean_ohlc
import market_profiles as mp
prof = mp.PROFILES['EG'] if isinstance(mp.PROFILES, dict) else mp.EGYPT
TODAY = pd.Timestamp('2026-07-22')

spot, q = 11.77, 0.0
FV_BEAR, FV_BASE, FV_BULL = 17.5, 20.9, 25.4     # note's own headline range + recalculated central
FV_GRID_LO, FV_GRID_HI = 15.0, 32.2               # full WACC x g grid corners

df = load_ohlc('/home/claude/testahil_repo/engine/raw_ohlc/EG/ISPH.csv')
df, _ = clean_ohlc(df, 'ISPH', verbose=False, market='EG')
v = yz_variance_proxy(df); o = len(df)-1

HORIZONS = [60, 120, 180, 240, 375, 500, 750, 1000]   # ~3mo,6mo,9mo,1y,1.5y,2y,3y,4y
rows = []
for H in HORIZONS:
    beta, s2 = fit_har_v3(v, o, horizon=min(H, 252))   # HAR forecast itself still uses <=1y variance forecast horizon convention
    dv = har_forecast_v3(v, o, beta, s2, horizon=min(H, 252))
    # scale the daily-var forecast forward flat for horizons beyond 1y (engine has no >1y variance term structure;
    # flat extrapolation of the 1y forecast is the explicit, stated assumption here)
    drift = carry_log_h(prof, TODAY, q, H)
    paths = simulate_paths_v3(spot, dv, H, drift, nu=prof.nu, n_paths=50000, seed=42, width_cal=prof.width_cal)
    term = paths[:,-1]
    row = dict(H=H, yrs=round(H/252,2), median=np.median(term), p25=np.percentile(term,25), p75=np.percentile(term,75))
    for name, lvl in [('bear17.5',FV_BEAR),('base20.9',FV_BASE),('bull25.4',FV_BULL),('gridlo15.0',FV_GRID_LO),('gridhi32.2',FV_GRID_HI)]:
        touch = (paths.max(axis=1) >= lvl)
        row[f'P_touch_{name}'] = touch.mean()*100
    rows.append(row)
res = pd.DataFrame(rows)
pd.set_option('display.width',200)
for c in res.columns:
    if c.startswith('P_touch') or c in ('median','p25','p75'):
        res[c]=res[c].round(1)
print(res.to_string(index=False))

# first horizon where P(touch base 20.9) crosses 50%
print("\nmedian terminal price by horizon vs fair-value markers (11.77 spot / 17.5 bear / 20.9 base / 25.4 bull):")
for _,r in res.iterrows():
    print(f"  {r.yrs:>4}y (h={int(r.H):>4}): median={r['median']:.2f}  P(touch base)={r['P_touch_base20.9']:.0f}%  P(touch bear)={r['P_touch_bear17.5']:.0f}%  P(touch bull)={r['P_touch_bull25.4']:.0f}%")

# implied annualized return to reach each level from spot, for reference
print("\nimplied CAGR to reach level from spot (11.77), various assumed horizons:")
for lvl,name in [(17.5,'bear'),(20.9,'base'),(25.4,'bull')]:
    for yrs in (1,2,3,5):
        cagr = (lvl/spot)**(1/yrs)-1
        print(f"  {name} {lvl}: over {yrs}y -> {cagr*100:.1f}% CAGR")
