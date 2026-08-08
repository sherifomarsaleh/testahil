"""
lab_round8_shadow_cohort.py -- Round 8, part C: generate SHADOW COHORT #1.

For each of the 30 EGX names, produce TWO T+60 forecasts from the same anchor
(the name's latest library close), same shape, same seed, via the ACTUAL
production chain (fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_terminal_v3, live profile nu/width_cal, seed 42, 50k paths):

  1. production drift: carry (what the engine publishes today)
  2. shadow drift:     carry + min(|pull|, cap) * sign(pull),
                       pull = (1 - exp(-ln2 * 60/375)) * ln(FV_base/spot)
                       (half-life 1.5yr; cap = 1.0 x the name's own T+60 sigma)

Output: labwork/shadow_cohort_20260723.json -- append-only lab ledger row per
name with both distributions (p5/p25/p50/p75/p95, 2dp convention). Graded when
each name's T+60 session arrives (count ACTUAL trading rows per the grading
rule, not calendar). LAB ARTIFACT: not pushed, not on ticker pages, flagged
shadow=true throughout. This starts the forward out-of-sample clock for the
FV-pull candidate under the standing promotion rule.
"""
import sys, os, json
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_terminal_v3
from data_quality import clean_ohlc
from market_profiles import EGYPT

from lab_round8_fvpull import FV   # fair values + study dates (single source in lab)

PROFILE = EGYPT
HORIZON = 60
N_PATHS = 50000
SEED = 42
HL_SESSIONS = 375          # 1.5yr half-life, base case
CONV_FRAC = 1 - np.exp(-np.log(2) * HORIZON / HL_SESSIONS)
CAP_SIGMA_MULT = 1.0       # |pull| capped at 1.0 x own T+60 sigma

d = '/home/claude/testahil_repo/engine/raw_ohlc/EG'
rows = []
for t, (bear, base, full, fv_date) in sorted(FV.items()):
    df = load_ohlc(os.path.join(d, f'{t}.csv'))
    df, _ = clean_ohlc(df, t, verbose=False, market='EG')
    df = df.sort_values('Date').reset_index(drop=True)
    v = yz_variance_proxy(df)
    o = len(df) - 1
    anchor_date = df['Date'].iloc[o]
    spot = float(df['Price'].iloc[o])

    beta, s2 = fit_har_v3(v, o, horizon=HORIZON)
    dv = har_forecast_v3(v, o, beta, s2, horizon=HORIZON)
    sigma_h = float(np.sqrt(dv * HORIZON) * PROFILE.width_cal)
    carry_b = carry_log_h(PROFILE, anchor_date, 0.0, HORIZON)

    gap = np.log(base / spot)
    pull_raw = CONV_FRAC * gap
    cap = CAP_SIGMA_MULT * sigma_h
    pull = float(np.clip(pull_raw, -cap, cap))
    capped = abs(pull_raw) > cap

    fv_age_sessions = int((df['Date'] > pd.Timestamp(fv_date)).sum())

    out = dict(ticker=t, anchor_date=str(anchor_date.date()), spot=round(spot, 4),
               fv_bear=bear, fv_base=base, fv_full=full, fv_date=fv_date,
               fv_age_sessions=fv_age_sessions,
               gap_log=round(float(gap), 4), sigma_h=round(sigma_h, 4),
               carry_drift=round(float(carry_b), 5),
               pull_raw=round(float(pull_raw), 5), pull_capped=bool(capped),
               shadow_drift=round(float(carry_b + pull), 5),
               half_life_sessions=HL_SESSIONS, cap_sigma_mult=CAP_SIGMA_MULT,
               nu=PROFILE.nu, width_cal=PROFILE.width_cal, seed=SEED,
               n_paths=N_PATHS, horizon=HORIZON, shadow=True,
               grade_after_sessions=HORIZON, realized_close=None)

    for label, drift in [('prod', carry_b), ('shadow', carry_b + pull)]:
        samp = simulate_terminal_v3(spot, sigma_h, drift, nu=PROFILE.nu,
                                    n_paths=N_PATHS, seed=SEED)
        q = np.percentile(samp, [5, 25, 50, 75, 95])
        out[f'{label}_p5'], out[f'{label}_p25'], out[f'{label}_p50'], \
            out[f'{label}_p75'], out[f'{label}_p95'] = [round(float(x), 2) for x in q]
    rows.append(out)
    print(f"{t:6s} anchor={out['anchor_date']} spot={spot:>8.2f} sigma60={sigma_h*100:5.1f}% "
          f"gap={gap*100:+6.1f}% pull={pull*100:+6.2f}%{' [CAPPED]' if capped else '':9s} "
          f"med prod {out['prod_p50']:>8.2f} -> shadow {out['shadow_p50']:>8.2f}")

meta = dict(cohort='shadow_fvpull_001', created='2026-07-23',
            construction='carry + clip((1-exp(-ln2*60/375))*ln(FV_base/spot), +-1.0*sigma_h)',
            engine='mc_v3 production chain, EGYPT live profile', purpose=(
                'Forward out-of-sample test of FV-pull drift vs production carry drift. '
                'Same anchor/shape/seed per name; graded at actual T+60 sessions; '
                'paired deltas. LAB shadow ledger - not published.'))
with open('/home/claude/labwork/shadow_cohort_20260723.json', 'w') as f:
    json.dump(dict(meta=meta, rows=rows), f, indent=1)

n_cap = sum(r['pull_capped'] for r in rows)
print(f"\n{len(rows)} names written to shadow_cohort_20260723.json; {n_cap} pulls hit the 1-sigma cap")
print(f"convergence fraction (HL=1.5yr): {CONV_FRAC:.1%} of log-gap per 60 sessions")
