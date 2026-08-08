"""
lab_round8_fvpull.py -- Equation Lab, Round 8 (23-Jul-2026).
Fair-value-pull drift: the first candidate NOT derived from price statistics.

Discovery driving this round: ALL 30 EGX names already carry published
fair-value bands (site assets/data.js, fair{bear,base,full}, studies dated
09-Jun..20-Jul-2026). Full panel coverage exists TODAY -- the drift can be
per-name, signed, and fundamental. What CANNOT exist is a walk-forward
backtest (the FVs postdate every DEV and FINAL origin; and several lenses
inside each FV are anchored on the market price at study date, so using them
retroactively would be double look-ahead). This round therefore does the only
three honest things available:

  A. NATURAL EXPERIMENT (legitimate, tiny): every study was PUBLISHED, then
     prices moved 3..45 days. Did ln(FV_base/spot at publication) predict the
     subsequent realized move (raw and net of EGX30)? n=30 names, ONE period,
     cross-sectionally correlated -- reported with those caveats, not dressed
     up as more than it is.
  B. PROTOTYPE: what the FV-pull drift (OU-style convergence) would do to
     each name's T+60 center today, at half-life 1/1.5/2yr. Shape untouched.
  C. (in the writeup) SHADOW-COHORT forward validation protocol -- the same
     out-of-sample discipline as the promotion rule, run in forward time.
"""
import numpy as np
import pandas as pd

RAW = '/home/claude/testahil_repo/engine/raw_ohlc/EG/{}.csv'

# fair values from assets/data.js (bear, base, full) + study dates
# (dates from the data.js fair comments where present, else the study
#  filename in files/; EGX ADIB = ADIB_Valuation_Study_03-07-2026)
FV = {
    'PHDC': (7.62, 15.89, 24.92, '2026-06-09'),
    'TMGH': (83.60, 147.12, 189.60, '2026-06-09'),
    'EMFD': (13.71, 19.84, 23.43, '2026-06-17'),
    'OCDI': (16.72, 26.43, 30.77, '2026-06-24'),
    'ORHD': (22.50, 53.79, 70.52, '2026-06-24'),
    'COMI': (90.86, 123.30, 169.70, '2026-06-29'),
    'CCAP': (3.30, 5.89, 8.60, '2026-06-30'),
    'ORAS': (740.00, 928.00, 1272.00, '2026-06-30'),
    'RAYA': (4.77, 5.56, 8.22, '2026-07-01'),
    'JUFO': (22.00, 26.00, 33.00, '2026-07-01'),
    'FWRY': (11.50, 14.70, 20.30, '2026-07-01'),
    'ABUK': (50.00, 60.00, 72.00, '2026-07-01'),
    'HRHO': (23.00, 27.70, 33.60, '2026-07-01'),
    'ORWE': (16.70, 20.90, 29.70, '2026-07-01'),
    'EFIH': (10.20, 14.16, 23.60, '2026-07-03'),
    'OIH': (0.53, 0.78, 1.70, '2026-07-03'),
    'HELI': (5.20, 8.40, 11.82, '2026-07-03'),
    'EGAL': (183.00, 250.00, 358.00, '2026-07-03'),
    'EFID': (16.41, 27.68, 42.78, '2026-07-03'),
    'BTFH': (1.89, 2.88, 4.13, '2026-07-03'),
    'ETEL': (82.00, 118.00, 160.00, '2026-07-03'),
    'ADIB': (31.60, 54.30, 95.30, '2026-07-03'),
    'KABO': (1.42, 2.39, 3.52, '2026-07-06'),
    'LCSW': (26.00, 37.00, 51.00, '2026-07-06'),
    'PRDC': (5.92, 8.23, 11.51, '2026-07-06'),
    'ISPH': (12.85, 17.78, 22.68, '2026-07-07'),
    'GBCO': (23.30, 35.70, 51.00, '2026-07-09'),
    'CLHO': (6.51, 9.21, 11.05, '2026-07-13'),
    'RMDA': (2.11, 2.77, 3.48, '2026-07-13'),
    'DSCW': (0.59, 0.88, 1.20, '2026-07-20'),
}


def load_close(t):
    df = pd.read_csv(RAW.format(t))
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['Price'] = df['Price'].astype(str).str.replace(',', '', regex=False).astype(float)
    return df.sort_values('Date').reset_index(drop=True)[['Date', 'Price']]


# EGX30 index for the market-factor netting
idx = pd.read_csv('/home/claude/labwork/EGX30_index.csv')
idx['Date'] = pd.to_datetime(idx['Date'], format='%m/%d/%Y')
idx['Price'] = idx['Price'].astype(str).str.replace(',', '', regex=False).astype(float)
idx = idx.sort_values('Date').reset_index(drop=True)[['Date', 'Price']]


def close_asof(df, d):
    sub = df[df['Date'] <= pd.Timestamp(d)]
    return (sub.iloc[-1]['Price'], sub.iloc[-1]['Date']) if len(sub) else (np.nan, None)


# ---------------------------------------------------------------- A: natural experiment
rows = []
for t, (bear, base, full, d0) in FV.items():
    px = load_close(t)
    s0, dt0 = close_asof(px, d0)
    s1, dt1 = px.iloc[-1]['Price'], px.iloc[-1]['Date']
    i0, _ = close_asof(idx, dt0)
    i1, _ = close_asof(idx, dt1)
    sessions = int(((px['Date'] > dt0) & (px['Date'] <= dt1)).sum())
    gap0 = np.log(base / s0)
    realized = np.log(s1 / s0)
    mkt = np.log(i1 / i0)
    rows.append(dict(ticker=t, fv_date=d0, spot0=s0, spot_now=s1, last=str(dt1.date()),
                     sessions=sessions, gap0=gap0, realized=realized, mkt=mkt,
                     excess=realized - mkt, bear=bear, base=base, full=full))

ne = pd.DataFrame(rows).sort_values('gap0')
print("=== A. Natural experiment: published FV gap -> subsequent move (post-publication only) ===")
print(f"{'ticker':7s} {'fv_date':10s} {'sess':>4s} {'gap0%':>7s} {'realized%':>9s} {'mkt%':>6s} {'excess%':>8s}")
for _, r in ne.iterrows():
    print(f"{r['ticker']:7s} {r['fv_date']:10s} {r['sessions']:4d} {r['gap0']*100:+7.1f} "
          f"{r['realized']*100:+9.1f} {r['mkt']*100:+6.1f} {r['excess']*100:+8.1f}")

for ycol in ['realized', 'excess']:
    c = np.corrcoef(ne['gap0'], ne[ycol])[0, 1]
    hit = (np.sign(ne['gap0']) == np.sign(ne[ycol])).mean()
    # per-session normalization (windows differ 3..32 sessions)
    ps = ne[ycol] / ne['sessions'].clip(lower=1)
    cps = np.corrcoef(ne['gap0'], ps)[0, 1]
    slope = np.polyfit(ne['gap0'], ne[ycol], 1)[0]
    print(f"\n[{ycol}] corr(gap0, {ycol})={c:+.3f}  per-session corr={cps:+.3f}  "
          f"sign hit-rate={hit:.1%}  slope={slope:+.3f} (fraction of gap closed over the window)")
print(f"\nCaveats printed with the numbers: n={len(ne)} names but ONE overlapping period "
      f"(3-32 sessions), cross-sectionally correlated, market move {ne['mkt'].mean()*100:+.1f}% avg; "
      "this is a smell test, not a gate.")

# ---------------------------------------------------------------- B: prototype drift table
print("\n=== B. FV-pull drift prototype: T+60 center shift vs carry-only, today ===")
CARRY_60 = np.log1p(0.1950) * 60 / 252          # current CBE 19.50% carry over T+60
print(f"carry-only T+60 log-drift: {CARRY_60*100:+.2f}% (every name identical today)")
print(f"{'ticker':7s} {'spot':>8s} {'base FV':>8s} {'gap%':>7s} | T+60 add-on: {'HL=1y':>7s} {'HL=1.5y':>7s} {'HL=2y':>7s} | {'total@1.5y':>10s}")
hl_fracs = {hl: 1 - np.exp(-np.log(2) * 60 / (hl * 250)) for hl in [1.0, 1.5, 2.0]}
proto = []
for _, r in ne.sort_values('gap0', ascending=False).iterrows():
    gap_now = np.log(r['base'] / r['spot_now'])
    adds = {hl: f * gap_now for hl, f in hl_fracs.items()}
    proto.append(dict(ticker=r['ticker'], spot=r['spot_now'], base=r['base'],
                      gap_now=gap_now, **{f'add_{hl}': a for hl, a in adds.items()}))
    print(f"{r['ticker']:7s} {r['spot_now']:8.2f} {r['base']:8.2f} {gap_now*100:+7.1f} |"
          f"          {adds[1.0]*100:+6.2f}% {adds[1.5]*100:+6.2f}% {adds[2.0]*100:+6.2f}% |"
          f" {(CARRY_60+adds[1.5])*100:+9.2f}%")
pd.DataFrame(proto).to_csv('/tmp/lab_round8_proto.csv', index=False)
ne.to_csv('/tmp/lab_round8_natexp.csv', index=False)

print(f"\nconvergence fractions over 60 sessions: HL=1y {hl_fracs[1.0]:.1%}, "
      f"HL=1.5y {hl_fracs[1.5]:.1%}, HL=2y {hl_fracs[2.0]:.1%} of the log-gap")
