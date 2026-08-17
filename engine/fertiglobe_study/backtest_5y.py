"""FERTIGLB — walk-forward backtest reported over four window sets, so the coverage
claim is evidenced explicitly rather than inferred:
  (1) FULL cleaned history (= the entire listed life; FERTIGLB IPO'd 27-Oct-2021,
      so the series is 4.8 years long and a literal five-year lookback does not
      exist. The full set IS the maximum available and is reported as such.)
  (2) the last FIVE YEARS of origins (identical to (1) here, stated not implied)
  (3) the production window set (origins after the market's last structural break)
  (4) a STAGGERED-ORIGIN diagnostic: the same non-overlapping engine re-run from
      five different start offsets and pooled, purely to give the uniformity test
      more than 14 observations. Overlapping across grids, so it is a DIAGNOSTIC
      for PIT shape only and never a verdict — the verdict stays on (3).
Scored against the carry-anchored random-walk benchmark, scale-normalised, with a
chi-square and KS uniformity test on the probability-integral transform.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from scipy import stats
from primitives import load_ohlc
from data_quality import clean_ohlc
from mc_v3 import backtest_v3
from panel_refresh import apply_breaks, robust_verdict
from market_profiles import PROFILES

AE = PROFILES['AE']
with open(os.path.join(HERE, '..', 'fitted_configs.json')) as f:
    reg = json.load(f)['AE']
NU, CAL = float(reg['nu']), float(reg['width_cal'])
assert (NU, CAL) == (float(AE.nu), float(AE.width_cal))

df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'FERTIGLB.csv')),
                   'FERTIGLB', verbose=False, market='AE')
r_all = backtest_v3(df, AE, horizon_months=3, nu=NU, width_cal=CAL,
                    use_signal=AE.signal_active, n_paths=20000, seed=42, min_history=260)
last = pd.Timestamp(df['Date'].iloc[-1])
cut5 = last - pd.DateOffset(years=5)


def score(r, label, verdict_ok=True):
    r = r.copy()
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
               verdict=verd if verdict_ok else 'DIAGNOSTIC ONLY (overlapping grids)',
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
    print(f"  skill vs carry-anchored random walk: {skill:+.4f} (raw basis {out['skill_raw']:+.4f}) "
          f"| {out['verdict']}")
    for b in (2, 3, 4):
        print(f"    block={b}: 90% CI [{detail[b][0]:+.4f}, {detail[b][1]:+.4f}] {detail[b][2]}")
    print(f"  coverage 50/80/90: {out['cov50']:.2f}/{out['cov80']:.2f}/{out['cov90']:.2f} "
          f"| cone width vs benchmark {out['width_vs_benchmark']:.3f}")
    print(f"  PIT mean {out['pit_mean']:.3f} | histogram {out['pit_hist']} | "
          f"chi-square(9)={out['chi2']} p={out['chi2_p']} | KS p={out['ks_p']} "
          f"-> {'roughly uniform' if out['uniform'] else 'NOT uniform'}")
    return out


# staggered-origin diagnostic
stag = []
for off in (0, 12, 24, 36, 48):
    ri = backtest_v3(df, AE, horizon_months=3, nu=NU, width_cal=CAL,
                     use_signal=AE.signal_active, n_paths=20000, seed=42,
                     min_history=260 + off)
    ri = apply_breaks(ri, AE)
    ri['grid'] = off
    stag.append(ri)
stag = pd.concat(stag, ignore_index=True).sort_values('origin')

res = dict(
    full=score(r_all, 'FULL cleaned history (= entire listed life, 4.8 yr)'),
    five_year=score(r_all[r_all['origin'] >= cut5], 'LAST FIVE YEARS of origins'),
    production=score(apply_breaks(r_all, AE), 'production window set (post-break origins)'),
    staggered=score(stag, 'STAGGERED-ORIGIN uniformity diagnostic (5 grids pooled)',
                    verdict_ok=False),
)
res['listing_date'] = str(df['Date'].iloc[0].date())
res['history_span_years'] = round((df['Date'].iloc[-1] - df['Date'].iloc[0]).days / 365.25, 2)
res['five_year_note'] = (
    "FERTIGLB listed on 27-Oct-2021. The cleaned series is 4.77 years long, so a "
    "literal five-year lookback predates the instrument's existence. Sets (1) and (2) "
    "are therefore identical and represent the maximum evidence obtainable.")
res['fit'] = dict(nu=NU, width_cal=CAL, market_verdict=reg['market_verdict'],
                  market_skill=reg['market_skill'], market_ci90=reg['market_ci90'],
                  fit_date=reg['fit_date'], panel_names=len(reg['panel_names']),
                  panel_windows=reg['windows'])
with open(os.path.join(HERE, 'backtest_5y.json'), 'w') as f:
    json.dump(res, f, indent=1)
print("\nwrote backtest_5y.json")
