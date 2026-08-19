"""SAVOLA study figures. House palette; SOLID light background on every figure so the
numbers stay readable when the page behind them is dark, and label positions chosen
so nothing overlaps a title, an axis or another label."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from primitives import load_ohlc
from data_quality import clean_ohlc

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
BG = '#FBF9F4'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG})

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
spot = d['meta']['spot']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'SAVOLA.csv')),
                   'SAVOLA', verbose=False, market='SA')

def style(ax):
    for s_ in ['top', 'right']: ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']: ax.spines[s_].set_color(GREY)

# ---- F1 football field ------------------------------------------------------
L = dict(d['lenses'])
L['central'] = dict(base=d['central'],
                    bear=sum(L[k]['bear'] * d['weights'][k] for k in
                             ('dcf', 'relative', 'normalized', 'book')),
                    bull=sum(L[k]['bull'] * d['weights'][k] for k in
                             ('dcf', 'relative', 'normalized', 'book')))
names = ['FCFF DCF\n(primary; Framing A)', 'Relative\n(peer-mix P/E, discounted)',
         'Normalised\nearnings power', 'Book value /\nsustainable return',
         'Weighted central\n(bar = weighted bear-bull span)']
keys = ['dcf', 'relative', 'normalized', 'book', 'central']
fig, ax = plt.subplots(figsize=(9.7, 4.2), dpi=110)
xmax = max(L[k]['bull'] for k in keys); xmin = min(L[k]['bear'] for k in keys)
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = L[k]['bear'], L[k]['base'], L[k]['bull']
    col = GOLD if k == 'central' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col,
            alpha=0.5 if k == 'central' else 0.32, edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(bu + 0.02 * (xmax - xmin), y, f'{b:.1f}–{bu:.1f} · base {ba:.1f}',
            va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.01 * (xmax - xmin), -0.62, f'spot {spot:.2f}', color=INK, fontsize=9,
        ha='left', va='top')
ax.axvspan(d['central'] * 0.97, d['central'] * 1.03, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(keys)), names[::-1], fontsize=8.6)
ax.set_xlabel('SAR / share')
ax.set_xlim(xmin - 0.06 * (xmax - xmin), xmax + 0.30 * (xmax - xmin))
ax.set_ylim(-1.0, len(keys) - 0.4)
ax.set_title('Savola — valuation football field (bear–bull span per lens; brass tick = base)',
             fontsize=10, pad=10)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png')); plt.close(fig)

# ---- F2 sensitivity heatmap (WACC x terminal g) ------------------------------
S = d['sens']; tab = np.array(S['grid'])
fig, ax = plt.subplots(figsize=(7.9, 3.8), dpi=110)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
_near = int((np.abs(tab - spot) < 0.8).sum())
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=9.5, color=INK,
                fontweight='bold' if abs(v - spot) < 0.8 else 'normal')
ax.set_xticks(range(len(S['g_grid'])), [f'{x*100:.1f}%' for x in S['g_grid']])
ax.set_yticks(range(len(S['wacc_grid'])), [f'{x*100:.2f}%' for x in S['wacc_grid']])
ax.set_xlabel('terminal growth g'); ax.set_ylabel('explicit-window cost of capital')
ax.set_title('DCF fair value (SAR/share) — cost of capital × terminal growth; '
             + (f'bold ≈ spot {spot:.2f}' if _near else
                f'no cell within 0.8 of the spot of {spot:.2f}'), fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png')); plt.close(fig)

# ---- F3 moving-average stack -------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='SAVOLA close')
for n, c in [(20, GOLD), (50, BRASS), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper right')
ax.set_title('Savola — price against the moving-average stack, last twelve months',
             fontsize=10, pad=8)
ax.set_ylabel('SAR'); style(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_ma.png')); plt.close(fig)

# ---- F4 fan chart ------------------------------------------------------------
paths = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths, [5, 25, 50, 75, 95], axis=0)
days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = d['central']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ymax = fan[4].max(); ymin = fan[0].min(); rng = ymax - ymin
ax.text(1, cb + 0.020 * rng, f'fundamental central ≈ {cb:.1f}', color=BRASS, fontsize=8.6,
        va='bottom')
ax.text(days[-1] - 1, spot - 0.022 * rng, f'spot {spot:.2f}', color=GREY, fontsize=8.6,
        ha='right', va='top')
_n = len(days) - 1
ax.set_xticks([0, _n / 3.0, 2 * _n / 3.0, _n], ['0', '1', '2', '3'])
ax.set_xlabel('calendar months ahead'); ax.set_ylabel('SAR / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to three months — 50,000 simulated paths', fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_fan.png')); plt.close(fig)

# ---- F5/F6 distributions ------------------------------------------------------
for tag, fn, out in [('one month', 'paths_1M.npy', 'fig5_dist.png'),
                     ('three months', 'paths_3M.npy', 'fig6_dist.png')]:
    x = np.load(os.path.join(HERE, fn))[:, -1]
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    yl = ax.get_ylim()[1]
    _bb = dict(boxstyle='round,pad=0.2', facecolor=BG, edgecolor='none', alpha=0.95)
    ax.text(spot, yl * 0.96, f'spot {spot:.2f} ', color=INK, fontsize=8.4, ha='right',
            va='top', bbox=_bb)
    ax.text(np.median(x), yl * 0.84, f' median {np.median(x):.2f}', color=BRASS,
            fontsize=8.4, ha='left', va='top', bbox=_bb)
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('SAR / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, out)); plt.close(fig)

# ---- F7 the segment mix and the margin path -----------------------------------
F = d['fcst']; SEGF = d['segments_fy25']
yrs = ['FY25'] + [str(y) for y in F['years']]
segdata = dict(
    fp=[SEGF['fp']['rev']] + F['fp_rev'],
    panda=[d['inputs']['ret_segrev_fy25']['value']] + F['panda']['rev'],
    herfy=[d['inputs']['fsv_segrev_fy25']['value']] + F['herfy']['rev'],
    frozen=[d['inputs']['frz_segrev_fy25']['value']] + F['frozen']['rev'])
SEGLAB = dict(fp='Food Processing', panda='Retail (Panda)', herfy='Food Services (Herfy)',
              frozen='Frozen (Al Kabeer)')
SEGCOL = dict(fp=SAGE, panda=GOLD, herfy='#7B8D88', frozen=BRASS)
mar = [d['hist_is']['FY25']['ebitda'] / d['hist_is']['FY25']['rev']] + F['ebitda_margin']
fig, ax = plt.subplots(figsize=(9.7, 4.0), dpi=110)
xs = np.arange(len(yrs))
bottom = np.zeros(len(yrs))
for s_ in ['fp', 'panda', 'herfy', 'frozen']:
    vals = np.array(segdata[s_]) / 1000
    ax.bar(xs, vals, width=0.56, bottom=bottom, color=SEGCOL[s_],
           alpha=0.85 if s_ != 'fp' else 0.75, label=SEGLAB[s_],
           edgecolor='#FFFFFF', linewidth=0.6)
    bottom += vals
for i in range(len(yrs)):
    ax.text(i, bottom[i] + 0.32, f'{bottom[i]:.1f}', ha='center', fontsize=8.4, color=INK)
ax.set_ylabel('segment revenue before eliminations (SAR bn)')
ax.set_ylim(0, bottom.max() * 1.26)
ax.set_xticks(xs, yrs, fontsize=8.8)
ax2 = ax.twinx()
ax2.plot(xs, np.array(mar) * 100, color=INK, lw=2.1, marker='o', ms=4.5,
         label='group EBITDA margin (right)')
for i, m in enumerate(mar):
    ax2.text(i, m * 100 - 0.10, f'{m*100:.1f}%', ha='center', fontsize=8.2, color=INK,
             va='top',
             bbox=dict(boxstyle='round,pad=0.18', facecolor=BG, edgecolor='none', alpha=0.92))
ax2.set_ylabel('EBITDA margin (%)', color=INK)
ax2.tick_params(axis='y', colors=INK)
ax2.set_ylim(min(mar) * 100 - 1.4, max(mar) * 100 + 2.6)
ax2.grid(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.4, loc='upper left', labelcolor=INK,
          ncol=3)
ax.set_title('Segment revenue (before eliminations), and the group margin path — margins '
             'are outputs', fontsize=10, pad=9)
style(ax)
for s_ in ['top']: ax2.spines[s_].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig7_mix.png')); plt.close(fig)

# ---- FD1 experts --------------------------------------------------------------
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
    ax.text(hi + 0.02 * xr, y, f'{lo:.1f}–{hi:.1f} · base {ba:.1f}', va='center',
            fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.012 * xr, -0.58, f'spot {spot:.2f}', fontsize=9, color=INK, ha='left',
        va='top')
pm = d['panel_median']
ax.axvspan(pm * 0.95, pm * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=8.6)
ax.set_xlabel('SAR / share')
ax.set_xlim(min(los) - 0.08 * xr, max(his) + 0.30 * xr)
ax.set_ylim(-0.95, len(ex) - 0.4)
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel '
             'median', fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png')); plt.close(fig)
print('figures done')
