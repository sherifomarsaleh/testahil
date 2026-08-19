"""Riyadh Cables study figures. House palette; SOLID light background on every figure so
the numbers stay readable when the page behind them is dark, and label positions chosen so
nothing overlaps a title, an axis or another label. Every figure is inspected as a rendered
image before delivery."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from primitives import load_ohlc
from data_quality import clean_ohlc

CANVAS, CREAM, GOLD, BRASS, SAGE = '#14322E', '#F5F0E4', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#14322E', '#D5DDDB', '#55625E'
BG = '#FBF9F4'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG})

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
spot = d['spot']
SRC = json.load(open(os.path.join(HERE, 'source_financials.json')))
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'RIYADHCABLE.csv')),
                   'RIYADHCABLE', verbose=False, market='SA')
F = d['fcst']


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


# ---- F1 football field ------------------------------------------------------
L = d['lenses']
names = ['FCFF DCF\n(primary)', 'Relative\n(EV/EBITDA · P/E)', 'Normalised\nearnings power',
         'Book value /\nsustainable return', 'Weighted central']
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
    ax.text(bu + 0.02 * (xmax - xmin), y, f'{b:.0f}–{bu:.0f} · base {ba:.0f}',
            va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.01 * (xmax - xmin), -0.62, f'spot {spot:.2f}', color=INK, fontsize=9,
        ha='left', va='top')
cB = L['central']
ax.axvspan(cB['base'] * 0.95, cB['base'] * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(keys)), names[::-1], fontsize=8.6)
ax.set_xlabel('SAR / share')
ax.set_xlim(xmin - 0.06 * (xmax - xmin), xmax + 0.30 * (xmax - xmin))
ax.set_ylim(-1.0, len(keys) - 0.4)
ax.set_title('Riyadh Cables — valuation football field (bear–bull span per lens; brass tick = base)',
             fontsize=10, pad=10)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png')); plt.close(fig)

# ---- F2 sensitivity heatmap (terminal WACC x terminal g) --------------------
S = d['sens']; tab = np.array(S['grid_wacc_g'])
NMM = np.array(S['grid_wacc_g_nm'], dtype=bool)
tab = np.ma.masked_array(tab, mask=NMM)   # n/m cells carry no colour, only the label
fig, ax = plt.subplots(figsize=(7.9, 3.8), dpi=110)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
NM = S['grid_wacc_g_nm']
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        if NM[i][j]:
            # terminal spread below 2%: the growing perpetuity is not meaningful — no number
            ax.text(j, i, 'n/m', ha='center', va='center', fontsize=9.5, color='#8A948F')
        else:
            ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=9.5, color=INK,
                    fontweight='bold' if abs(v - spot) < 8 else 'normal')
ax.set_xticks(range(len(S['g_grid'])), [f'{x*100:.0f}%' for x in S['g_grid']])
ax.set_yticks(range(len(S['wt_grid'])), [f'{x*100:.1f}%' for x in S['wt_grid']])
ax.set_xlabel('terminal growth g'); ax.set_ylabel('terminal cost of capital')
ax.set_title(f'DCF fair value (SAR/share) — terminal cost of capital × terminal growth; '
             f'bold ≈ spot {spot:.0f}; n/m = terminal spread under 2%', fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png')); plt.close(fig)

# ---- F3 moving-average stack -------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='RIYADHCABLE close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper left')
ax.set_title('Riyadh Cables — price against the moving-average stack, last 260 sessions',
             fontsize=10, pad=8)
ax.set_ylabel('SAR'); style(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_ma.png')); plt.close(fig)

# ---- F4 fan chart --------------------------------------------------------------
fan = np.load(os.path.join(HERE, 'fan.npy')); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = d['lenses']['central']['base']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ymax = fan[4].max(); ymin = fan[0].min(); rng = ymax - ymin
ax.text(1, cb + 0.020 * rng, f'fundamental central ≈ {cb:.0f}', color=BRASS, fontsize=8.6, va='bottom')
ax.text(days[-1] - 1, spot - 0.022 * rng, f'spot {spot:.2f}', color=GREY, fontsize=8.6,
        ha='right', va='top')
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('SAR / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to three months — 50,000 simulated paths', fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_fan.png')); plt.close(fig)

# ---- F5/F6 distributions --------------------------------------------------------
for tag, fn, out in [('one month', 'paths_1M.npy', 'fig5_dist.png'),
                     ('three months', 'paths_3M.npy', 'fig6_dist.png')]:
    x = np.load(os.path.join(HERE, fn))[:, -1]
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    yl = ax.get_ylim()[1]
    ax.text(spot, yl * 0.96, f'spot {spot:.0f} ', color=INK, fontsize=8.4, ha='right', va='top')
    ax.text(np.median(x), yl * 0.84, f' median {np.median(x):.0f}', color=BRASS, fontsize=8.4,
            ha='left', va='top')
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('SAR / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, out)); plt.close(fig)

# ---- F7 the cost stack (materials / conversion / gross profit) + gross margin -----
IS = SRC['income_statement']; CB = SRC['cost_of_revenue_breakdown']
yrs = ['FY25'] + [y.replace('E', '') for y in F['years']]
rev = [IS['revenue']['2025'] / 1e6] + F['rev']
mat = [CB['materials']['2025'] / 1e6] + F['mat_cab']
conv = [(CB['total']['2025'] - CB['materials']['2025']) / 1e6] + F['conv_cab']
gp = [IS['gross_profit']['2025'] / 1e6] + F['gp']
gm = [IS['gross_profit']['2025'] / IS['revenue']['2025']] + F['gm']
fig, ax = plt.subplots(figsize=(9.7, 4.2), dpi=110)
xs = np.arange(len(yrs))
matb = np.array(mat) / 1000; convb = np.array(conv) / 1000; gpb = np.array(gp) / 1000
ax.bar(xs, matb, width=0.58, color=SAGE, alpha=0.85, label='Materials (copper/aluminium)', edgecolor='#FFFFFF', linewidth=0.6)
ax.bar(xs, convb, width=0.58, bottom=matb, color='#7B8D88', alpha=0.85, label='Conversion cost', edgecolor='#FFFFFF', linewidth=0.6)
ax.bar(xs, gpb, width=0.58, bottom=matb + convb, color=GOLD, alpha=0.9, label='Gross profit', edgecolor='#FFFFFF', linewidth=0.6)
for i in range(len(yrs)):
    ax.text(i, (matb + convb + gpb)[i] + 0.12, f'{rev[i]/1000:.1f}', ha='center', fontsize=8.2, color=INK)
ax.set_ylabel('revenue (SAR bn)'); ax.set_ylim(0, max(matb + convb + gpb) * 1.20)
ax.set_xticks(xs, yrs, fontsize=8.8)
ax2 = ax.twinx()
ax2.plot(xs, np.array(gm) * 100, color=BRASS, lw=2.1, marker='o', ms=4.5, label='Gross margin (right)')
for i, m in enumerate(gm):
    ax2.text(i, m * 100 + 0.55, f'{m*100:.1f}%', ha='center', fontsize=8.0, color=BRASS,
             bbox=dict(boxstyle='round,pad=0.16', facecolor=BG, edgecolor='none', alpha=0.92))
ax2.set_ylabel('gross margin (%)', color=BRASS); ax2.tick_params(axis='y', colors=BRASS)
ax2.set_ylim(0, max(gm) * 100 + 6); ax2.grid(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.2, loc='upper left', labelcolor=INK, ncol=2)
ax.set_title('The cost stack — materials are ~95% of cost of revenue; gross margin is the output',
             fontsize=10, pad=9)
style(ax)
for s_ in ['top']:
    ax2.spines[s_].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig7_stack.png')); plt.close(fig)

# ---- F8 the gross-margin story + the contested judgement both ways ----------------
hgm = {y: IS['gross_profit'][y] / IS['revenue'][y] for y in ['2022', '2023', '2024', '2025']}
h1_26 = SRC['interims_2026']['H1_2026_gross_margin']
xh = ['2022', '2023', '2024', '2025', 'H1-26'] + [y.replace('E', '') for y in F['years']]
yh = [hgm['2022'], hgm['2023'], hgm['2024'], hgm['2025'], h1_26] + F['gm']
fig, ax = plt.subplots(figsize=(9.9, 4.2), dpi=110)
xs = np.arange(len(xh))
ax.plot(xs[:5], np.array(yh[:5]) * 100, color=INK, lw=2.2, marker='o', ms=5, label='Actual')
ax.plot(xs[4:], np.array(yh[4:]) * 100, color=BRASS, lw=2.2, marker='o', ms=5, ls='--', label='Forecast (base)')
# both-ways band from FY2026
bull = [0.16] * 5; bear = [0.145] * 5
ax.fill_between(xs[5:], np.array(bear) * 100, np.array(bull) * 100, color=GOLD, alpha=0.16,
                label='Contested band (14.5%–16.0%)')
ax.axhline(hgm['2025'] * 100, color=SAGE, lw=1.1, ls=':')
ax.text(0.1, hgm['2025'] * 100 + 0.2, f"FY2025 peak {hgm['2025']*100:.1f}%", color=SAGE, fontsize=8.2, va='bottom')
ax.text(4, h1_26 * 100 - 1.1, f'H1-2026\nanchor {h1_26*100:.1f}%', color=INK, fontsize=8.0, ha='center', va='top')
ax.set_ylabel('gross margin (%)'); ax.set_ylim(6, 19)
ax.set_xticks(xs, xh, fontsize=8.6)
ax.legend(frameon=False, fontsize=8.3, loc='lower right', labelcolor=INK)
ax.set_title('Gross margin — the metal-tailwind peak, the H1-2026 normalisation, and the forecast',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig8_margin.png')); plt.close(fig)

# ---- FD1 experts ------------------------------------------------------------------
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
    ax.text(hi + 0.02 * xr, y, f'{lo:.0f}–{hi:.0f} · base {ba:.0f}', va='center', fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.012 * xr, -0.58, f'spot {spot:.2f}', fontsize=9, color=INK, ha='left', va='top')
pc = d['panel_centre']
ax.axvspan(pc * 0.95, pc * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=8.6)
ax.set_xlabel('SAR / share')
ax.set_xlim(min(los) - 0.08 * xr, max(his) + 0.30 * xr)
ax.set_ylim(-0.95, len(ex) - 0.4)
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel centre',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png')); plt.close(fig)
print('figures done')
