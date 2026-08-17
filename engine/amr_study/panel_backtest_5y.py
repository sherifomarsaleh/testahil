"""AMR — the five-year evidence, at the level the cone is actually calibrated on.

Americana listed on 12 December 2022, so its own price history supports only ten
non-overlapping three-month windows. The width and shape of the published cone are not
fitted on Americana alone; they are fitted on the pooled UAE panel, and that panel does
carry five years. This script scores the panel over the last five years of origins on the
same basis as the single-name test — carry-anchored random-walk benchmark, scale-normalised
by spot, probability-integral transform tested for uniformity — so the five-year claim has
a real object behind it and the single-name shortfall is stated rather than papered over.
"""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from scipy import stats
from panel_refresh import robust_verdict, apply_breaks
from market_profiles import PROFILES

AE = PROFILES['AE']
files = sorted(glob.glob(os.path.join(HERE, '..', 'panels', 'AE_*_3m.csv')))
rows, per_name = [], {}
for f in files:
    name = os.path.basename(f)[3:-7]
    d = pd.read_csv(f, parse_dates=['origin'])
    d = apply_breaks(d, AE)
    if not len(d):
        continue
    d['name'] = name
    rows.append(d)
    per_name[name] = len(d)
panel = pd.concat(rows, ignore_index=True)
last = panel['origin'].max()
cut5 = last - pd.DateOffset(years=5)


def score(d, label):
    d = d.copy()
    d['crps_n'] = d['crps'] / d['spot']
    d['crps_b_n'] = d['crps_b'] / d['spot']
    skill = 1 - d['crps_n'].sum() / d['crps_b_n'].sum()
    verd, detail = robust_verdict(d['crps_n'].values, d['crps_b_n'].values)
    pit = d['pit'].values
    hist = np.histogram(pit, bins=10, range=(0, 1))[0]
    exp = len(pit) / 10.0
    chi2 = float(((hist - exp) ** 2 / exp).sum())
    p = float(1 - stats.chi2.cdf(chi2, 9))
    ks = stats.kstest(pit, 'uniform')
    out = dict(label=label, names=int(d['name'].nunique()), windows=int(len(d)),
               first_origin=str(d['origin'].min().date()), last_origin=str(d['origin'].max().date()),
               span_years=round((d['origin'].max() - d['origin'].min()).days / 365.25, 2),
               skill_norm=float(skill), verdict=verd,
               ci_blocks={str(b): [round(float(detail[b][0]), 4), round(float(detail[b][1]), 4),
                                   detail[b][2]] for b in (2, 3, 4)},
               cov50=float(d['in50'].mean()), cov80=float(d['in80'].mean()),
               cov90=float(d['in90'].mean()), pit_mean=float(pit.mean()),
               pit_hist=hist.tolist(), chi2=round(chi2, 2), chi2_p=round(p, 3),
               ks_stat=round(float(ks.statistic), 3), ks_p=round(float(ks.pvalue), 3),
               pit_roughly_uniform=bool(p > 0.05 and ks.pvalue > 0.05),
               width_vs_benchmark=float((d['w90'] / d['w90_b']).mean()))
    print(f"\n[{label}] {out['names']} names, {out['windows']} windows | "
          f"{out['first_origin']} .. {out['last_origin']} ({out['span_years']} yr)")
    print(f"  skill vs the carry-anchored random walk: {skill:+.4f} | {verd}")
    for b in (2, 3, 4):
        print(f"    block={b}: 90% CI [{detail[b][0]:+.4f}, {detail[b][1]:+.4f}] {detail[b][2]}")
    print(f"  coverage 50/80/90: {out['cov50']:.2f}/{out['cov80']:.2f}/{out['cov90']:.2f} | "
          f"cone width vs benchmark {out['width_vs_benchmark']:.3f}")
    print(f"  probability-integral transform: mean {out['pit_mean']:.3f}, "
          f"chi-square p={out['chi2_p']}, Kolmogorov-Smirnov p={out['ks_p']} -> "
          f"{'roughly uniform' if out['pit_roughly_uniform'] else 'NOT uniform'}")
    return out


res = dict(five_year=score(panel[panel['origin'] >= cut5], 'UAE panel, last five years of origins'),
           full=score(panel, 'UAE panel, all post-break origins'),
           per_name_windows=per_name,
           note=('Americana itself contributes no window before December 2023 because it listed '
                 'on 12 December 2022 and a full year of history is required before the first '
                 'origin. The five-year evidence is therefore panel-level, and the single-name '
                 'result is reported separately and in full.'))
with open(os.path.join(HERE, 'panel_backtest_5y.json'), 'w') as f:
    json.dump(res, f, indent=1)
print('\nwrote panel_backtest_5y.json')
