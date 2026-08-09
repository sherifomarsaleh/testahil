import json, sys, os
sys.path.insert(0, os.path.abspath('repo/engine'))
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from market_profiles import MarketProfile, FED_SCHEDULE
from mc_v2 import yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_paths_v3
from scipy import stats

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
plt.rcParams.update({'figure.facecolor': 'none', 'axes.facecolor': 'none',
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': True})

d = json.load(open('study_numbers_xpt.json'))
spot = d['meta']['spot']
df = pd.read_csv('XPT_clean_staged.csv', parse_dates=['Date'])
NU, CAL, SEED, NPATHS = 250.0, 0.853, 42, 50000
XPT = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363, "", None, +1, 0.0, False,
                    nu=250.0, width_cal=CAL, breaks=[])

def style(ax):
    for s_ in ['top', 'right']: ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']: ax.spines[s_].set_color(GREY)

# ---- F1 anchors football field ----------------------------------------------
A, Z = d['anchors'], d['zone']
rows = [('Pt/Au ratio lens\n(primary)', A['ratio']), ('Analyst consensus\n(forward anchor)', A['consensus']),
        ('Supply/demand balance\n(structural floor)', A['balance']), ('Cost curve\n(floor & incentive)', A['cost']),
        ('Weighted fair-value zone', dict(bear=Z['lo'], base=Z['centre'], bull=Z['hi']))]
fig, ax = plt.subplots(figsize=(9.7, 4.1), dpi=110)
for i, (nm, L) in enumerate(rows):
    y = len(rows) - 1 - i
    b, ba, bu = L['bear'], L['base'], L['bull']
    col = GOLD if 'zone' in nm else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col, alpha=0.5 if 'zone' in nm else 0.32,
            edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(bu + 25, y, f'{b:,.0f}–{bu:,.0f} · base {ba:,.0f}', va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 8, len(rows) - 0.34, f'spot {spot:,.0f}', color=INK, fontsize=9)
ax.axvspan(Z['lo'], Z['hi'], color=GOLD, alpha=0.10)
ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1], fontsize=8.6)
ax.set_xlabel('US$ / oz'); ax.set_xlim(850, 2850)
ax.set_title('Platinum — valuation football field (bear–bull span per anchor; brass tick = base; ink line = spot)',
             fontsize=10, pad=10)
style(ax); fig.tight_layout(); fig.savefig('fig1_football.png'); plt.close(fig)

# ---- F2 ratio sensitivity heatmap -------------------------------------------
G = d['ratio_grid']; tab = np.array(G['fv'])
fig, ax = plt.subplots(figsize=(7.9, 3.8), dpi=110)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:,.0f}', ha='center', va='center', fontsize=9.6,
                color=INK, fontweight='bold' if abs(v - spot) < 45 else 'normal')
ax.set_xticks(range(len(G['gold'])), [f"${g:,.0f}" for g in G['gold']])
ax.set_yticks(range(len(G['ratio'])), [f"{r:.3f}×" if r != 0.405 else "0.405× (now)" for r in G['ratio']])
ax.set_xlabel('gold price scenario (US$/oz)'); ax.set_ylabel('Pt/Au ratio scenario')
ax.set_title('Platinum fair value = gold × Pt/Au ratio (US$/oz); bold ≈ spot 1,608', fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig('fig2_grid.png'); plt.close(fig)

# ---- F3 MA stack (last 520 sessions ≈ 2y) ------------------------------------
s = df.set_index('Date')['Price'].iloc[-520:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.6, label='XPT/USD close')
for n, c in [(20, GOLD), (50, BRASS), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-520:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=4, labelcolor=INK, loc='upper left')
ax.set_title('Platinum — price versus the moving-average stack, last ~2 years (the 2025 re-rating, the January 2026 record, the halving)',
             fontsize=10, pad=8)
ax.set_ylabel('US$/oz'); style(ax)
fig.tight_layout(); fig.savefig('fig3_ma.png'); plt.close(fig)

# ---- F4 momentum: RSI + MACD --------------------------------------------------
sc = pd.Series(df['Price'].values, index=df['Date'])
dd = sc.diff(); up = dd.clip(lower=0).rolling(14).mean(); dn = (-dd.clip(upper=0)).rolling(14).mean()
rsi = 100 - 100 / (1 + up / dn)
e12, e26 = sc.ewm(span=12, adjust=False).mean(), sc.ewm(span=26, adjust=False).mean()
macd = e12 - e26; sig = macd.ewm(span=9, adjust=False).mean(); hist = macd - sig
fig, axes = plt.subplots(2, 1, figsize=(10.5, 4.6), dpi=110, sharex=True)
a = axes[0]; a.plot(rsi.index[-520:], rsi.values[-520:], color=BRASS, lw=1.3)
a.axhline(70, color=GREY, ls=':', lw=1); a.axhline(30, color=GREY, ls=':', lw=1)
a.set_ylabel('RSI(14)'); a.set_ylim(0, 100); style(a)
a.set_title('Momentum — RSI(14) and MACD(12,26,9)', fontsize=10, pad=8)
b = axes[1]
b.plot(macd.index[-520:], macd.values[-520:], color=INK, lw=1.2, label='MACD')
b.plot(sig.index[-520:], sig.values[-520:], color=BRASS, lw=1.1, label='signal')
b.bar(hist.index[-520:], hist.values[-520:], color=[GOLD if x >= 0 else SAGE for x in hist.values[-520:]], width=1.4)
b.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='lower left'); b.set_ylabel('MACD'); style(b)
fig.tight_layout(); fig.savefig('fig4_mom.png'); plt.close(fig)

# ---- recompute paths (identical seed/params) for fan + dists ------------------
v = yz_variance_proxy(df); origin = len(df) - 1
def sim(h):
    beta, s2 = fit_har_v3(v, origin, horizon=h)
    dv = har_forecast_v3(v, origin, beta, s2, horizon=h)
    drift = carry_log_h(XPT, df['Date'].iloc[-1], 0.0, h)
    return simulate_paths_v3(spot, dv, h, drift, nu=NU, n_paths=NPATHS, seed=SEED, width_cal=CAL)
p252 = sim(252); p63 = sim(63)
assert abs(np.percentile(p63[:, -1], 50) - d['mc']['t63']['p50']) < 0.01  # exact reproduction guard
fan = np.percentile(p252, [5, 25, 50, 75, 95], axis=0)
days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
ax.axhline(d['zone']['centre'], color=BRASS, lw=1.4, ls='--')
ax.text(3, d['zone']['centre'] + 22, f"fair-value centre ≈ {d['zone']['centre']:,.0f}", color=BRASS, fontsize=8.6)
ax.text(3, spot - 60, f'spot {spot:,.0f}', color=GREY, fontsize=8.6)
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('US$/oz')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward cone to T+252 — 50,000 carry-anchored YZ-HAR paths, Gaussian tail, width_cal 0.853 (provisional metals-family fit)',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('fig5_fan.png'); plt.close(fig)

for tag, arr, fn in [('T+63 (3 months)', p63[:, -1], 'fig6_dist63.png'),
                     ('T+252 (12 months)', p252[:, -1], 'fig7_dist252.png')]:
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(arr, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(arr), color=BRASS, lw=1.6, ls='--')
    ax.text(spot, ax.get_ylim()[1] * 0.94, f' spot {spot:,.0f}', color=INK, fontsize=8.4)
    ax.text(np.median(arr), ax.get_ylim()[1] * 0.84, f' median {np.median(arr):,.0f}', color=BRASS, fontsize=8.4)
    ax.set_xlim(np.percentile(arr, 0.3), np.percentile(arr, 99.7))
    ax.set_xlabel('US$/oz'); ax.set_yticks([])
    ax.set_title(f'Terminal price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout(); fig.savefig(fn); plt.close(fig)

# ---- FB1 calibration 3-panel --------------------------------------------------
bt = pd.read_csv('XPT_panel_60d.csv', parse_dates=['origin'])
s0 = json.load(open('step0_results.json'))
fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9), dpi=110)
a = axes[0]
a.plot(df['Date'], df['Price'], color=INK, lw=0.9, label='realized')
for _, r in bt.iterrows():
    o = r['origin']; e = o + pd.Timedelta(days=88)
    # widths stored at baseline cal=1.0; adopted cone = ±1.645·sigma_h·0.853 around carry
    med = r['spot'] * np.exp(r['drift'])
    lo = r['spot'] * np.exp(r['drift'] - 1.645 * r['sigma_h'] * CAL)
    hi = r['spot'] * np.exp(r['drift'] + 1.645 * r['sigma_h'] * CAL)
    a.fill_between([o, e], [r['spot'], lo], [r['spot'], hi], color=GOLD, alpha=0.20)
    a.plot([e], [r['realized']], marker='o', ms=2.6, color=BRASS)
a.set_title('62 non-overlapping 60-day cones, 2012–2026', fontsize=9.5)
a.set_ylabel('US$/oz'); style(a)
b = axes[1]
u = bt['u'].values / CAL
pit = stats.norm.cdf(u)
cnt, _ = np.histogram(pit, bins=10, range=(0, 1))
b.bar(np.arange(10) / 10 + 0.05, cnt / len(pit), width=0.09, color=GOLD, edgecolor='#FFFFFF')
b.axhline(0.1, color=INK, ls='--', lw=1)
b.set_title(f'PIT histogram under the adopted fit (n={len(pit)})', fontsize=9.5)
b.set_xlabel('PIT'); style(b)
c = axes[2]
dg = s0['diag_self']
cov = [dg['cov50'], dg['cov80'], dg['cov90']]
c.bar([0, 1, 2], [x * 100 for x in cov], width=0.5, color=GOLD, edgecolor='#FFFFFF')
for i, t in enumerate([50, 80, 90]):
    c.plot([i - 0.32, i + 0.32], [t, t], color=INK, ls='--', lw=1.4)
c.set_xticks([0, 1, 2], ['50% band', '80% band', '90% band'])
c.set_ylim(0, 105); c.set_title('Interval coverage vs target', fontsize=9.5)
sc_ = s0['scores']
c.text(0.02, 0.97, (f"self-fit skill {sc_['self_fit']['skill']:+.4f} (PARITY)\n"
                    f"LONO gold+silver {sc_['lono_gold_silver']['skill']:+.4f} (PARITY)\n"
                    f"borrowed live metals {sc_['borrowed_live_metals']['skill']:+.4f} (PARITY)\n"
                    f"PIT mean {dg['pit_mean']:.3f}"),
       transform=c.transAxes, fontsize=8.0, color=INK, va='top')
style(c)
fig.suptitle('Step 0 — platinum calibration: carry-anchored YZ-HAR vs carry-anchored random-walk benchmark, scale-normalized CRPS',
             fontsize=10, color=INK, y=1.02)
fig.tight_layout(); fig.savefig('figB1_calibration.png', bbox_inches='tight'); plt.close(fig)
import shutil; shutil.copy('figB1_calibration.png', 'calibration_Platinum.png')

# ---- FD1 experts ---------------------------------------------------------------
ex = [('Expert 1 — real-rate / opportunity-cost', 1500, (1300, 1700)),
      ('Expert 2 — industrial supply/demand (cost-curve)', 1800, (1350, 2200)),
      ('Expert 3 — investment-flows / Pt-Au ratio', 1670, (1300, 2070))]
fig, ax = plt.subplots(figsize=(9.7, 3.3), dpi=110)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + 20, y, f'{lo:,.0f}–{hi:,.0f} · base {ba:,.0f}', va='center', fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 8, len(ex) - 0.33, f'spot {spot:,.0f}', fontsize=9, color=INK)
ax.axvspan(d['zone']['lo'], d['zone']['hi'], color=GOLD, alpha=0.10)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=8.8)
ax.set_xlabel('US$ / oz'); ax.set_xlim(1100, 2500)
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = weighted zone; ink line = spot',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('figD1_experts.png'); plt.close(fig)
print('figures done')
