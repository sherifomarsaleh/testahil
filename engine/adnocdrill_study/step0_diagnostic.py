"""ADNOCDRILL — diagnosis of the 3-month Step 0 FAIL.

The verdict is a ROBUST FAIL under blocks {2,3,4}, so it is not a boundary
artifact. This script establishes WHICH failure it is. Two candidate mechanisms:

  (A) MIS-CENTRING — the cone points the wrong way (drift wrong). Signature:
      PIT mass piled at one end, coverage BELOW nominal.
  (B) OVER-WIDTH — the cone is correctly centred but too wide, so it pays a
      CRPS sharpness penalty against a tighter benchmark. Signature: coverage
      ABOVE nominal at every level, PIT centred, w90 ratio > 1.

Mechanism (B) is the known signature of a market-level width_cal applied to a
name whose own realised vol sits below the panel average. The remedy for (B)
exists in this repo (engine/adaptive_width.py) but is EG-only and
history-gated; it is NOT applied here and this script does not refit anything.
The width sweep below is a DIAGNOSTIC — it reports what the score would have
been at other widths in order to identify the mechanism, and its results are
not eligible to enter the engine (the promotion rule requires an out-of-sample
test on a panel, which a single name cannot supply).
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc as raw_load
from data_quality import clean_ohlc
from mc_v3 import backtest_v3
from panel_refresh import apply_breaks, robust_verdict
from market_profiles import PROFILES

AE = PROFILES['AE']
with open(os.path.join(HERE, '..', 'fitted_configs.json')) as f:
    reg = json.load(f)['AE']
NU, CAL = float(reg['nu']), float(reg['width_cal'])

df_raw = raw_load(os.path.join(HERE, 'ADNOCDRILL_Stock_Price_History.csv'))
df, _ = clean_ohlc(df_raw, 'ADNOCDRILL', verbose=False, market='AE')

rows = []
for mult in (0.70, 0.80, 0.90, 1.00, 1.10):
    r = backtest_v3(df, AE, horizon_months=3, nu=NU, width_cal=CAL * mult,
                    use_signal=AE.signal_active, n_paths=20000, seed=42,
                    min_history=260)
    r = apply_breaks(r, AE)
    sk = 1 - (r['crps'] / r['spot']).sum() / (r['crps_b'] / r['spot']).sum()
    rows.append(dict(mult=mult, width_cal=round(CAL * mult, 4), skill=float(sk),
                     cov50=float(r['in50'].mean()), cov80=float(r['in80'].mean()),
                     cov90=float(r['in90'].mean()), pit_mean=float(r['pit'].mean()),
                     w90_ratio=float((r['w90'] / r['w90_b']).mean())))
    print(f"  width x{mult:.2f} (cal {CAL*mult:.3f}): skill {sk:+.4f} "
          f"cov50 {r['in50'].mean():.2f} cov80 {r['in80'].mean():.2f} "
          f"cov90 {r['in90'].mean():.2f} PIT {r['pit'].mean():.3f} "
          f"w90/bench {(r['w90']/r['w90_b']).mean():.3f}")

# --- realised vol of ADNOCDRILL vs the AE panel, post-break -----------------
d = df[df['Date'] >= pd.Timestamp('2022-01-01')].copy()
lr = np.diff(np.log(d['Close'].values if 'Close' in d.columns else d['Price'].values))
own_vol = float(np.std(lr, ddof=1) * np.sqrt(252))
panel = {}
for nm in reg['panel_names']:
    p = os.path.join(HERE, '..', 'raw_ohlc', 'AE', nm + '.csv')
    if not os.path.exists(p):
        continue
    x, _ = clean_ohlc(raw_load(p), nm, verbose=False, market='AE')
    x = x[x['Date'] >= pd.Timestamp('2022-01-01')]
    px = x['Close'].values if 'Close' in x.columns else x['Price'].values
    if len(px) > 30:
        panel[nm] = float(np.std(np.diff(np.log(px)), ddof=1) * np.sqrt(252))
pv = np.array(sorted(panel.values()))
pct = float((pv < own_vol).mean())

out = dict(width_sweep=rows, own_annualised_vol=own_vol,
           panel_vols={k: round(v, 4) for k, v in sorted(panel.items(), key=lambda kv: kv[1])},
           panel_median_vol=float(np.median(pv)), panel_mean_vol=float(np.mean(pv)),
           own_vol_percentile_in_panel=pct)
with open(os.path.join(HERE, 'step0_diagnostic.json'), 'w') as f:
    json.dump(out, f, indent=1)
print(f"\nADNOCDRILL annualised vol (post-2022) {own_vol:.4f} | AE panel median "
      f"{np.median(pv):.4f} mean {np.mean(pv):.4f} | percentile {pct:.2f}")
