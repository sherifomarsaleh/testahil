import os as _os_pathfix
# EVERY PATH IN THIS BUILDER IS RELATIVE, SO THE RUN'S DIRECTORY DECIDED WHERE ITS
# INPUT WAS READ AND ITS OUTPUT WAS WRITTEN. Run from anywhere but this folder it
# either crashed or, worse, wrote a deliverable into the caller's directory.
_HERE = _os_pathfix.path.dirname(_os_pathfix.path.abspath(__file__))
_os_pathfix.chdir(_HERE)
import sys as _sys_pathfix
_sys_pathfix.path.insert(0, _HERE)
_sys_pathfix.path.insert(0, _os_pathfix.path.join(_HERE, '..'))

import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import primitives as m

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
plt.rcParams.update({'figure.facecolor': CREAM, 'axes.facecolor': CREAM,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': CREAM, 'savefig.edgecolor': CREAM})

d = json.load(open('study_numbers.json'))
spot = d['spot']
# THE EXCHANGE LIBRARY, NOT THE STUDY-LOCAL COPY. compute.py strikes the cone on
# engine/raw_ohlc/EG/GBCO.csv; a chart drawn from the study-local extract, which stops
# at 7 July 2026, would draw a different series from the one every number came off.
import os as _os
df = m.load_ohlc(_os.path.join(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))), 'raw_ohlc', 'EG', 'GBCO.csv'))

def style(ax):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    for s in ['left', 'bottom']: ax.spines[s].set_color(GREY)

# ---- F1 football field ------------------------------------------------------
L = d['lenses']
names = ['Sum-of-the-parts\n(split legs)', 'Pre-discount NAV\n(DCF-anchored)', 'Relative multiples', 'Normalized earnings', 'Weighted central']
keys = ['sotp', 'prediscount', 'relative', 'normalized', 'central']
_LO = min(L[k]['bear'] for k in keys + ['central'])
_HI = max(L[k]['bull'] for k in keys + ['central'])
_SPAN = _HI - _LO
_PAD = _SPAN * 0.012
fig, ax = plt.subplots(figsize=(9.7, 4.1), dpi=110)
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = L[k]['bear'], L[k]['base'], L[k]['bull']
    col = GOLD if k == 'central' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col, alpha=0.32 if k != 'central' else 0.5,
            edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(bu + _PAD, y, f'{b:.0f}–{bu:.0f}  ·  base {ba:.1f}', va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
cB = L['central']
ax.axvspan(cB['base'] * 0.95, cB['base'] * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(keys)), names[::-1], fontsize=9)
ax.set_xlabel('EGP / share')
# THE AXIS IS FITTED TO THE DATA, NOT TYPED. A hardcoded 8-64 clipped the widest lens's
# label off the canvas the moment the rebuild moved the bull case past it, and the label
# collision is a depth-bar standard 5 failure rather than a cosmetic one.
ax.set_xlim(_LO - _PAD, _HI + _SPAN * 0.34)
# the spot label sits BELOW the bars rather than at the top, where it collided with the title
ax.set_ylim(-0.75, len(keys) - 0.4)
ax.text(spot + _PAD, -0.62, f'spot {spot:.2f}', color=INK, fontsize=8.6, ha='left', va='center')
ax.set_title('GB Corp — valuation football field: bear–bull span per lens',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('fig1_football.png'); plt.close(fig)

# ---- F2 SOTP sensitivity heatmap -------------------------------------------
S = d['sens']; tab = np.array(S['table']); _NEAR = []
fig, ax = plt.subplots(figsize=(7.6, 3.7), dpi=110)
im = ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        near = abs(v - spot) < 1.6
        _NEAR.append(near)
        ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=10,
                color=INK,
                fontweight='bold' if near else 'normal')
ax.set_xticks(range(5), [f'{x*100:.0f}%' for x in S['grid_disc']])
ax.set_yticks(range(5), [f'{x*100:+.0f}pp' for x in S['grid_margin']])
ax.set_xlabel('complexity / conglomerate discount')
ax.set_ylabel('Auto GPM shift vs base')
# THE TITLE STATES WHAT THE PICTURE ACTUALLY SHOWS. It used to promise bold cells at a
# typed spot of 31.25; the rebuild moved both the grid and the price and NO cell is within
# a pound and a half of the price any more, so the promise described a figure that does not
# exist — the defect a heatmap caption was caught making on another study.
ax.set_title('SOTP fair value (EGP/sh) — Auto margin \u00d7 complexity discount'
             + (f'; bold \u2248 spot {spot:.2f}' if any(_NEAR)
                else f'; no cell reaches the EGP {spot:.2f} price'),
             fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig('fig2_sens.png'); plt.close(fig)

# ---- F3 MA stack ------------------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='GBCO close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper left')
ax.set_title('GBCO — price versus the moving-average stack, last 260 sessions', fontsize=10, pad=8)
ax.set_ylabel('EGP'); style(ax)
fig.tight_layout(); fig.savefig('fig3_ma.png'); plt.close(fig)

# ---- F4 fan chart ------------------------------------------------------------
fan = np.load('fan.npy'); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = d['lenses']['central']['base']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ax.text(1, cb + 0.4, f'fundamental central ≈ {cb:.0f}', color=BRASS, fontsize=8.6)
ax.text(1, spot - 1.3, f'spot {spot:.2f}', color=GREY, fontsize=8.6)
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('EGP / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to 3 months — 50,000 YZ-HAR paths, Student-t(5), secular drift (Step 0-passed)',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('fig4_fan.png'); plt.close(fig)

# ---- F5/F6 distributions -----------------------------------------------------
for tag, fn in [('1 month', 'pT20.npy'), ('3 months', 'pT60.npy')]:
    x = np.load(fn)
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    ax.text(spot, ax.get_ylim()[1]*0.94, f' spot {spot:.2f}', color=INK, fontsize=8.4)
    ax.text(np.median(x), ax.get_ylim()[1]*0.84, f' median {np.median(x):.1f}', color=BRASS, fontsize=8.4)
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('EGP / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout()
    fig.savefig(f"fig{'5' if tag=='1 month' else '6'}_dist.png"); plt.close(fig)

# ---- FB1 calibration 3-panel --------------------------------------------------
bt = pd.read_csv('backtest_rows.csv', parse_dates=['origin'])
fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9), dpi=110)
a = axes[0]
a.plot(df['Date'], df['Price'], color=INK, lw=1.0, label='realized')
for _, r in bt.iterrows():
    o = r['origin']; e = o + pd.Timedelta(days=88)
    a.fill_between([o, e], [r['spot'], r['p5']], [r['spot'], r['p95']], color=GOLD, alpha=0.22)
    a.plot([e], [r['realized']], marker='o', ms=3, color=BRASS)
a.set_yscale('log'); a.set_title('Quarterly cone replay (log scale)', fontsize=9.5)
a.set_ylabel('EGP'); style(a)
b = axes[1]
b.bar(np.arange(10) / 10 + 0.05, np.array(d['step0']['pit_hist']) / d['step0']['n_rows'],
      width=0.09, color=GOLD, edgecolor='#FFFFFF')
b.axhline(0.1, color=INK, ls='--', lw=1)
b.set_title('PIT histogram (n=17, non-overlapping)', fontsize=9.5)
b.set_xlabel('PIT'); style(b)
c = axes[2]
so = d['step0']['nonoverlap']
cov = [so['cov50'], so['cov80'], so['cov90']]
c.bar([0, 1, 2], [x * 100 for x in cov], width=0.5, color=GOLD, edgecolor='#FFFFFF')
for i, t in enumerate([50, 80, 90]):
    c.plot([i - 0.32, i + 0.32], [t, t], color=INK, ls='--', lw=1.4)
c.set_xticks([0, 1, 2], ['50% band', '80% band', '90% band'])
c.set_ylim(0, 105); c.set_title('Interval coverage vs target', fontsize=9.5)
c.text(0.02, 0.94, f"CRPS skill +{so['crps_skill']*100:.1f}% (n=17)\nmonthly origins +{d['step0']['monthly']['crps_skill']*100:.1f}% (n=49)",
       transform=c.transAxes, fontsize=8.2, color=INK, va='top')
style(c)
fig.suptitle('Step 0 — GBCO calibration backtest: YZ-HAR · t(5) · secular drift vs zero-drift random-walk benchmark',
             fontsize=10, color=INK, y=1.02)
fig.tight_layout(); fig.savefig('figB1_calibration.png', bbox_inches='tight'); plt.close(fig)
# site-style copy for the ledger
import shutil; shutil.copy('figB1_calibration.png', 'calibration_GBCO.png')

# ---- FD1 experts -------------------------------------------------------------
# EVERY RANGE IS READ FROM THE RECORD. The three spans were TYPED here and two of the
# three disagreed with the study's own numbers — Expert 1's brass tick sat outside its own
# bar and outside the axis entirely, because his base came from the model and his range did
# not. All three now come from experts.{e1,e2,e3}.rng, which compute.py derives from each
# expert's own stated levers.
E = d['experts']
ex = [('Expert 1 — split-legs NAV', E['e1']['base'], tuple(E['e1']['rng'])),
      ('Expert 2 — normalized earnings power', E['e2']['base'], tuple(E['e2']['rng'])),
      ('Expert 3 — cash returns / ROCE vs WACC', E['e3']['base'], tuple(E['e3']['rng']))]
_ELO = min(min(r) for _, _, r in ex + [(0, 0, (spot,))])
_EHI = max(max(r) for _, _, r in ex)
_ESPAN = _EHI - _ELO
_EPAD = _ESPAN * 0.012
_EBASES = sorted(b for _, b, _ in ex)
fig, ax = plt.subplots(figsize=(9.7, 3.3), dpi=110)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + _EPAD, y, f'{lo:.0f}–{hi:.0f} · base {ba:.1f}', va='center', fontsize=8.6,
            color=INK)
ax.axvline(spot, color=INK, lw=1.6)
# the gold band is the PANEL CENTRE — the middle expert's base, not a typed pair of levels
ax.axvspan(_EBASES[1] * 0.95, _EBASES[1] * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=9)
ax.set_xlabel('EGP / share')
ax.set_xlim(_ELO - _EPAD, _EHI + _ESPAN * 0.22)
ax.set_ylim(-0.75, len(ex) - 0.4)
ax.text(spot + _EPAD, -0.62, f'spot {spot:.2f}', fontsize=8.6, color=INK, va='center')
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel centre',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('figD1_experts.png'); plt.close(fig)
print('figures done')
