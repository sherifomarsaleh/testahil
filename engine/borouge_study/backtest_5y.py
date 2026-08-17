"""BOROUGE — walk-forward backtest reported over three window sets, so the
five-year claim is evidenced explicitly rather than inferred:
  (1) FULL cleaned history
  (2) the last FIVE YEARS of origins
  (3) the production window set (origins after the market's last structural break)
Scored against the carry-anchored random-walk benchmark, scale-normalised, with a
chi-square uniformity test on the probability-integral transform.

HONESTY NOTE, and it is the point of this file rather than a footnote: Borouge listed
on 3 June 2022. The cleaned series therefore spans 4.17 years, not five, and the
five-year window set is identical to the full history — the study says so in plain
words rather than presenting a five-year claim it cannot support. The name's own
non-overlapping three-month window count is small for that reason, which is exactly
why the standing gate is the market panel and not the single name.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np                                    # noqa: E402
import pandas as pd                                   # noqa: E402
from scipy import stats                               # noqa: E402
from data_quality import clean_ohlc                   # noqa: E402
from market_profiles import PROFILES                  # noqa: E402
from mc_v3 import backtest_v3                         # noqa: E402
from panel_refresh import apply_breaks, robust_verdict  # noqa: E402
from primitives import load_ohlc                      # noqa: E402

AE = PROFILES['AE']
with open(os.path.join(HERE, '..', 'fitted_configs.json')) as f:
    reg = json.load(f)['AE']
NU, CAL = float(reg['nu']), float(reg['width_cal'])
assert (NU, CAL) == (float(AE.nu), float(AE.width_cal)), \
    "fitted_configs.json and market_profiles.py disagree — read the live state, do not proceed"

# Dividend carry, sourced (see strike_borouge.py). The benchmark is carry-anchored, so
# the yield has to be in it or the comparison flatters the model.
DPS_AED = 0.162

df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'BOROUGE_Stock_Price_History.csv')),
                   'BOROUGE', verbose=False, market='AE')
q_annual = DPS_AED / float(df['Price'].iloc[-1])

r_all = backtest_v3(df, AE, horizon_months=3, nu=NU, width_cal=CAL,
                    use_signal=AE.signal_active, n_paths=20000, seed=42,
                    min_history=260, q_annual=q_annual)
last = pd.Timestamp(df['Date'].iloc[-1])
cut5 = last - pd.DateOffset(years=5)


def score(r, label):
    r = r.copy()
    if not len(r):
        print(f"\n[{label}] no windows")
        return dict(label=label, windows=0)
    r['crps_n'] = r['crps'] / r['spot']
    r['crps_b_n'] = r['crps_b'] / r['spot']
    skill = 1 - r['crps_n'].sum() / r['crps_b_n'].sum()
    verd, detail = robust_verdict(r['crps_n'].values, r['crps_b_n'].values)
    pit = r['pit'].values
    hist = np.histogram(pit, bins=10, range=(0, 1))[0]
    exp = len(pit) / 10.0
    chi2 = float(((hist - exp) ** 2 / exp).sum())
    p = float(1 - stats.chi2.cdf(chi2, 9))
    ks = stats.kstest(pit, 'uniform')
    out = dict(label=label, windows=int(len(r)),
               first_origin=str(r['origin'].iloc[0].date()),
               last_origin=str(r['origin'].iloc[-1].date()),
               span_years=round((r['origin'].iloc[-1] - r['origin'].iloc[0]).days / 365.25, 2),
               skill_norm=float(skill),
               skill_raw=float(1 - r['crps'].sum() / r['crps_b'].sum()),
               verdict=verd,
               ci_blocks={str(b): [round(float(detail[b][0]), 4), round(float(detail[b][1]), 4),
                                   detail[b][2]] for b in (2, 3, 4)},
               cov50=float(r['in50'].mean()), cov80=float(r['in80'].mean()),
               cov90=float(r['in90'].mean()),
               pit_mean=float(pit.mean()), pit_hist=hist.tolist(),
               chi2=round(chi2, 2), chi2_p=round(p, 3),
               ks_stat=round(float(ks.statistic), 3), ks_p=round(float(ks.pvalue), 3),
               uniform=bool(p > 0.05 and ks.pvalue > 0.05),
               width_vs_benchmark=float((r['w90'] / r['w90_b']).mean()))
    print(f"\n[{label}] {out['windows']} windows | {out['first_origin']} .. {out['last_origin']} "
          f"({out['span_years']} yr)")
    print(f"  skill vs carry-anchored random walk: {skill:+.4f} "
          f"(raw basis {out['skill_raw']:+.4f}) | {verd}")
    for b in (2, 3, 4):
        print(f"    block={b}: 90% CI [{detail[b][0]:+.4f}, {detail[b][1]:+.4f}] {detail[b][2]}")
    print(f"  coverage 50/80/90: {out['cov50']:.2f}/{out['cov80']:.2f}/{out['cov90']:.2f} "
          f"| cone width vs benchmark {out['width_vs_benchmark']:.3f}")
    print(f"  PIT mean {out['pit_mean']:.3f} | histogram {out['pit_hist']} | "
          f"chi-square(9)={out['chi2']} p={out['chi2_p']} | KS p={out['ks_p']} "
          f"-> {'roughly uniform' if out['uniform'] else 'NOT uniform'}")
    return out


res = dict(
    full=score(r_all, 'FULL cleaned history'),
    five_year=score(r_all[r_all['origin'] >= cut5], 'LAST FIVE YEARS of origins'),
    production=score(apply_breaks(r_all, AE), 'production window set (post-break origins)'),
)
res['history_span_years'] = round(
    (pd.Timestamp(df['Date'].iloc[-1]) - pd.Timestamp(df['Date'].iloc[0])).days / 365.25, 2)
res['listing_date'] = str(pd.Timestamp(df['Date'].iloc[0]).date())
res['five_year_available'] = bool(res['history_span_years'] >= 5.0)
res['q_annual'] = q_annual
res['fit'] = dict(nu=NU, width_cal=CAL, market_verdict=reg['market_verdict'],
                  market_skill=reg['market_skill'], market_ci90=reg['market_ci90'],
                  fit_date=reg['fit_date'], panel_names=len(reg['panel_names']),
                  panel_windows=reg['windows'])
r_all.to_csv(os.path.join(HERE, 'backtest_rows.csv'), index=False)
with open(os.path.join(HERE, 'backtest_5y.json'), 'w') as f:
    json.dump(res, f, indent=1)
print(f"\nhistory spans {res['history_span_years']} years from {res['listing_date']} — "
      f"a full five years of origins is {'available' if res['five_year_available'] else 'NOT available'}")
print("wrote backtest_5y.json")
