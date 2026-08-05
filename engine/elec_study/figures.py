"""ELEC study figures. House palette; SOLID light background on every figure
(readable on the site's dark pages — transparent PNGs with ink text are not),
and label positions chosen to avoid overlap with titles/axes."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from primitives import load_ohlc
from data_quality import clean_ohlc

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
BG = '#FBF9F4'   # solid near-cream canvas — figures must stay legible on a dark page
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG})

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
spot = d['spot']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ELEC_Stock_Price_History.csv')),
                   'ELEC', verbose=False, market='EG')

def style(ax):
    for s_ in ['top', 'right']: ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']: ax.spines[s_].set_color(GREY)

# ---- F1 football field ------------------------------------------------------
L = d['lenses']
names = ['FCFF DCF\n(primary)', 'Relative\n(P/E · EV/EBITDA)', 'Normalized\nearnings', 'Book / replacement\n(P/B vs ROE)', 'Weighted central']
keys = ['dcf', 'relative', 'normalized', 'book', 'central']
fig, ax = plt.subplots(figsize=(9.7, 4.2), dpi=110)
xmax = max(L[k]['bull'] for k in keys)
xmin = min(L[k]['bear'] for k in keys)
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = L[k]['bear'], L[k]['base'], L[k]['bull']
    col = GOLD if k == 'central' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col,
            alpha=0.5 if k == 'central' else 0.32, edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(bu + 0.02 * (xmax - xmin), y, f'{b:.2f}–{bu:.2f} · base {ba:.2f}',
            va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
# spot label BELOW the bars, not over the title (EAND fig-1 defect fixed)
ax.text(spot + 0.03, -0.62, f'spot {spot:.2f}', color=INK, fontsize=9, ha='left', va='top')
cB = L['central']
ax.axvspan(cB['base'] * 0.95, cB['base'] * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(keys)), names[::-1], fontsize=8.6)
ax.set_xlabel('EGP / share')
ax.set_xlim(xmin - 0.06 * (xmax - xmin), xmax + 0.30 * (xmax - xmin))
ax.set_ylim(-1.0, len(keys) - 0.4)
ax.set_title('Electro Cable Egypt — valuation football field (bear–bull span per lens; brass tick = base)',
             fontsize=10, pad=10)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png')); plt.close(fig)

# ---- F2 DCF sensitivity heatmap (explicit-window WACC x terminal g) ---------
S = d['sens_wg']; tab = np.array(S['table'])
fig, ax = plt.subplots(figsize=(7.6, 3.7), dpi=110)
im = ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=9.5, color=INK,
                fontweight='bold' if abs(v - spot) < 0.10 else 'normal')
ax.set_xticks(range(len(S['g_grid'])), [f'{x*100:.0f}%' for x in S['g_grid']])
ax.set_yticks(range(len(S['wacc_grid'])), [f'{x*100:.1f}%' for x in S['wacc_grid']])
ax.set_xlabel('terminal growth g'); ax.set_ylabel('terminal WACC')
ax.set_title(f'DCF fair value (EGP/sh) — terminal WACC × terminal g; bold ≈ spot {spot:.2f}',
             fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png')); plt.close(fig)

# ---- F3 MA stack ------------------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='ELEC close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper right')
ax.set_title('ELEC — price versus the moving-average stack, last 260 sessions', fontsize=10, pad=8)
ax.set_ylabel('EGP'); style(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_ma.png')); plt.close(fig)

# ---- F4 fan chart ------------------------------------------------------------
fan = np.load(os.path.join(HERE, 'fan.npy')); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = d['lenses']['central']['base']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ymax = fan[4].max()
ax.text(1, cb + 0.012 * ymax, f'fundamental central ≈ {cb:.2f}', color=BRASS, fontsize=8.6)
ax.text(days[-1] - 1, spot - 0.03 * ymax, f'spot {spot:.2f}', color=GREY, fontsize=8.6, ha='right')
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('EGP / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to 3 months — 50,000 paths, walk-forward-validated volatility engine',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_fan.png')); plt.close(fig)

# ---- F5/F6 distributions -----------------------------------------------------
for tag, fn, out in [('1 month', 'paths_1M.npy', 'fig5_dist.png'),
                     ('3 months', 'paths_3M.npy', 'fig6_dist.png')]:
    x = np.load(os.path.join(HERE, fn))[:, -1]
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    yl = ax.get_ylim()[1]
    # spot and median labels on opposite sides, never overlapping
    ax.text(spot, yl * 0.95, f'spot {spot:.2f} ', color=INK, fontsize=8.4, ha='right', va='top')
    ax.text(np.median(x), yl * 0.84, f' median {np.median(x):.2f}', color=BRASS, fontsize=8.4, ha='left', va='top')
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('EGP / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout()
    fig.savefig(os.path.join(HERE, out)); plt.close(fig)

# ---- FD1 experts -------------------------------------------------------------
E = d['experts']
ex = [(f"Expert 1 — {E['e1']['method_short']}", E['e1']['base'], E['e1']['rng']),
      (f"Expert 2 — {E['e2']['method_short']}", E['e2']['base'], E['e2']['rng']),
      (f"Expert 3 — {E['e3']['method_short']}", E['e3']['base'], E['e3']['rng'])]
fig, ax = plt.subplots(figsize=(9.7, 3.5), dpi=110)
his = [hi for _, _, (lo, hi) in ex]; los = [lo for _, _, (lo, hi) in ex]
xr = max(his) - min(los)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + 0.02 * xr, y, f'{lo:.2f}–{hi:.2f} · base {ba:.2f}', va='center', fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.02, -0.58, f'spot {spot:.2f}', fontsize=9, color=INK, ha='left', va='top')
pc = sorted([E['e1']['base'], E['e2']['base'], E['e3']['base']])[1]
ax.axvspan(pc * 0.95, pc * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=8.6)
ax.set_xlabel('EGP / share')
ax.set_xlim(min(los) - 0.08 * xr, max(his) + 0.32 * xr)
ax.set_ylim(-0.95, len(ex) - 0.4)
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel centre',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png')); plt.close(fig)
print('figures done')
