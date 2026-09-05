import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

# mc_v2 WAS RENAMED ON 2 AUGUST 2026 and is legacy reference only; this file had not run
# since. The production primitives are what the model itself reads.
import primitives as m

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
plt.rcParams.update({'figure.facecolor': CREAM, 'axes.facecolor': CREAM,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK,
                     # SOLID LIGHT CANVAS, ZERO TRANSPARENCY — depth-bar standard 5, and it
                     # is verified programmatically rather than trusted. A transparent PNG
                     # renders correctly on a white page and turns unreadable the moment a
                     # reader opens it on anything else.
                     'savefig.transparent': False,
                     'savefig.facecolor': CREAM})

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
spot = d['spot']
# THE PERSISTENT LIBRARY, not a one-off export of this study's own. Reading a
# private copy is how a figure comes to disagree with the cone above it.
df = m.load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'STC.csv'))

def style(ax):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    for s in ['left', 'bottom']: ax.spines[s].set_color(GREY)

# ---- F1 the lenses, one primary and its cross-checks -----------------------
# THE BLEND IS RETIRED [R-LENS-03] AND THIS FIGURE USED TO PUBLISH IT: its last bar was
# labelled "Weighted central" and drew a fifth number averaged out of the four above it. One
# class primary IS the central; every other lens is a CROSS-CHECK shown beside it, and the
# envelope is the RANGE of the present-value reads rather than a spread invented around a
# mean. Reading the four bars and expecting the fifth to be their average is exactly what a
# reader would do, and it would be wrong about what this study claims.
L = d['lenses']
LR = d['lens_record']
_names = {'dcf': 'Discounted cash flow\n(the central)',
          'ddm': 'Dividend discount\n(cross-check)',
          'relative': 'Enterprise multiple on own\nhistory (cross-check)',
          'normalized': 'Normalised earnings\n(cross-check)'}
keys = ['dcf', 'ddm', 'relative', 'normalized']
names = [_names[k] for k in keys]
fig, ax = plt.subplots(figsize=(9.7, 4.1), dpi=110)
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = L[k]['bear'], L[k]['base'], L[k]['bull']
    col = GOLD if k == LR['primary']['kind'] else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col, alpha=0.5 if col is GOLD else 0.32,
            edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(bu + 0.7, y, f'{b:.0f}–{bu:.0f}  ·  {ba:.1f}', va='center', fontsize=8.6,
            color=INK)
# the published envelope is the RANGE OF THE READS, drawn as a band rather than as a bar,
# so nothing on this chart can be mistaken for a fifth lens
_env = LR['envelope']
# DRAWN AS EDGES RATHER THAN AS A WASH, and in a different colour from the primary bar: at
# the first attempt the band and the central lens were both gold and a reader could not tell
# which was which — the wash read as a fifth, wider lens, which is the exact misreading the
# retired blend used to invite.
for _x in (_env['low'], _env['high']):
    ax.axvline(_x, color=BRASS, lw=1.0, ls=(0, (5, 3)), zorder=0)
ax.annotate('', xy=(_env['low'], -0.72), xytext=(_env['high'], -0.72),
            arrowprops=dict(arrowstyle='<->', color=BRASS, lw=1.0))
# LEFT-ALIGNED off the low edge, not centred: centred, the text sat exactly under the spot
# line and the line ran through it. Three passes on this one figure, each one found by
# looking at the rendered image and none of them visible in the code.
ax.text(_env['high'] + 0.8, -0.72,
        f"published range {_env['low']:.1f}–{_env['high']:.1f}", color=BRASS, fontsize=8.2,
        ha='left', va='center')
ax.axvline(spot, color=INK, lw=1.6)
# INSIDE the axes and below the top bar, not above it: at the previous placement the label
# sat on the title and the two were unreadable together. Caught by looking at the rendered
# image, which is a gate rather than a formality — nothing in the code says two pieces of
# text overlap.
ax.text(spot + 0.5, -0.30, f'spot {spot:.2f}', color=INK, fontsize=8.6, ha='left',
        va='center')
ax.set_yticks(range(len(keys)), names[::-1], fontsize=9)
ax.set_xlabel('SAR / share'); ax.set_xlim(26, 76); ax.set_ylim(-1.05, len(keys) - 0.35)
ax.set_title('stc — one primary lens and its cross-checks. The bar is each lens\u2019s own '
             'range, the brass tick its central read,\nand the dashed pair the range this '
             'study publishes. Nothing here is an average of the others.',
             fontsize=9.4, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png')); plt.close(fig)

# ---- F2 sensitivity heatmap: EBITDA margin × capex intensity (real units) ---
S = d['sens']; tab = np.array(S['table_cm'])
fig, ax = plt.subplots(figsize=(7.6, 3.7), dpi=110)
im = ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=10,
                color=INK, fontweight='bold' if abs(v - spot) < 1.2 else 'normal')
ax.set_xticks(range(5), [f'{x*100:+.1f}pp' for x in S['capex_steps']])
ax.set_yticks(range(5), [f'{x*100:+.1f}pp' for x in S['margin_steps']])
ax.set_xlabel('capex intensity shift (pp of revenue; base 16.5% FY26E)')
ax.set_ylabel('EBITDA margin shift (base 31.8% FY26E)')
ax.set_title('DCF fair value (SAR/sh) — EBITDA margin × capex intensity; bold ≈ spot 43.58', fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png')); plt.close(fig)

# ---- F3 MA stack ------------------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='stc close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper left')
ax.set_title('stc — price versus the moving-average stack, last 260 sessions', fontsize=10, pad=8)
ax.set_ylabel('SAR'); style(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_ma.png')); plt.close(fig)

# ---- F4 fan chart ------------------------------------------------------------
fan = np.load('fan.npy'); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = d['lenses']['central']['base']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ax.text(1, cb + 0.25, f'fundamental central ≈ {cb:.0f}', color=BRASS, fontsize=8.6)
ax.text(1, spot - 0.8, f'spot {spot:.2f}', color=GREY, fontsize=8.6)
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('SAR / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to T+60 — 50,000 YZ-HAR paths, Student-t(5), zero drift (Step 0-passed)',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_fan.png')); plt.close(fig)

# ---- F5/F6 distributions -----------------------------------------------------
for tag, fn in [('T+20', 'pT20.npy'), ('T+60', 'pT60.npy')]:
    x = np.load(fn)
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    ax.text(spot, ax.get_ylim()[1]*0.94, f' spot {spot:.2f}', color=INK, fontsize=8.4)
    ax.text(np.median(x), ax.get_ylim()[1]*0.84, f' median {np.median(x):.1f}', color=BRASS, fontsize=8.4)
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('SAR / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout()
    fig.savefig(os.path.join(HERE, f"fig{'5' if tag=='T+20' else '6'}_dist.png")); plt.close(fig)

# ---- FB1 calibration 3-panel --------------------------------------------------
bt = pd.read_csv('backtest_rows.csv', parse_dates=['origin'])
fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9), dpi=110)
a = axes[0]
a.plot(df['Date'], df['Price'], color=INK, lw=1.0, label='realized')
for _, r in bt.iterrows():
    o = r['origin']; e = o + pd.Timedelta(days=88)
    a.fill_between([o, e], [r['spot'], r['p5']], [r['spot'], r['p95']], color=GOLD, alpha=0.22)
    a.plot([e], [r['realized']], marker='o', ms=3, color=BRASS)
a.set_title('Quarterly cone replay', fontsize=9.5)
a.set_ylabel('SAR'); style(a)
b = axes[1]
b.bar(np.arange(10) / 10 + 0.05, np.array(d['step0']['pit_hist']) / d['step0']['n_rows'],
      width=0.09, color=GOLD, edgecolor='#FFFFFF')
b.axhline(0.1, color=INK, ls='--', lw=1)
b.set_title(f"PIT histogram (n={d['step0']['n_rows']}, non-overlapping)", fontsize=9.5)
b.set_xlabel('PIT'); style(b)
c = axes[2]
so = d['step0']['nonoverlap']
cov = [so['cov50'], so['cov80'], so['cov90']]
c.bar([0, 1, 2], [x * 100 for x in cov], width=0.5, color=GOLD, edgecolor='#FFFFFF')
for i, t in enumerate([50, 80, 90]):
    c.plot([i - 0.32, i + 0.32], [t, t], color=INK, ls='--', lw=1.4)
c.set_xticks([0, 1, 2], ['50% band', '80% band', '90% band'])
c.set_ylim(0, 105); c.set_title('Interval coverage vs target', fontsize=9.5)
c.text(0.02, 0.94, f"CRPS skill +{so['crps_skill']*100:.1f}% (n={d['step0']['n_rows']})\ninterval skill +{so['interval_skill']*100:.1f}%\nmonthly origins +{d['step0']['monthly']['crps_skill']*100:.1f}% (n={d['step0']['monthly']['n']})",
       transform=c.transAxes, fontsize=8.2, color=INK, va='top')
style(c)
fig.suptitle('Step 0 — stc calibration backtest: YZ-HAR · t(5) · zero drift vs zero-drift random-walk benchmark',
             fontsize=10, color=INK, y=1.02)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figB1_calibration.png'), bbox_inches='tight'); plt.close(fig)
import shutil; shutil.copy(os.path.join(HERE, 'figB1_calibration.png'),
            os.path.join(HERE, 'calibration_STC.png'))

# ---- FD1 experts -------------------------------------------------------------
E = d['experts']
ex = [('Expert 1 — cash returns / economic profit', E['e1']['base'], tuple(E['e1']['rng'])),
      ('Expert 2 — normalized earnings power', E['e2']['base'], tuple(E['e2']['rng'])),
      ('Expert 3 — macro-policy scenario tree', E['e3']['base'], (d['lenses']['ddm']['bear'], d['lenses']['ddm']['bull']))]
fig, ax = plt.subplots(figsize=(9.7, 3.3), dpi=110)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + 0.6, y, f'{lo:.0f}–{hi:.0f} · base {ba:.1f}', va='center', fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot, len(ex) - 0.35, f' spot {spot:.2f}', fontsize=9, color=INK)
ax.axvspan(41.5, 46.5, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=9)
ax.set_xlabel('SAR / share'); ax.set_xlim(28, 62)
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel centre; ink line = spot',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png')); plt.close(fig)
print('figures done')
