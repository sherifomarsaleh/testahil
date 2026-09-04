"""SCEM study figures.

House palette, and a SOLID LIGHT background on every figure so the numbers stay readable
when the page behind them is dark. Label positions are chosen so nothing overlaps a
title, an axis, a bar or another label, and every axis carries units.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from primitives import load_ohlc
from data_quality import clean_ohlc

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY, RUST = '#1C3A36', '#D5DDDB', '#5A6764', '#A0522D'
BG = '#FBF9F4'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG, 'font.size': 9.5})

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
STK = json.load(open(os.path.join(HERE, 'strike_result.json')))
SPOT = D['meta']['spot']
LR, SN, H, F = D['lens_ranges'], D['sensitivity'], D['history'], D['forecast']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'SCEM_Stock_Price_History.csv')),
                  'SCEM', verbose=False, market='EG')


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), dpi=150, facecolor=BG)
    plt.close(fig)
    print('wrote', name)


# ---- F1 football field -------------------------------------------------------
keys = ['DCF (cash flow)', 'Relative multiples', 'Asset / replacement cost',
        'Book value (disclosed floor)']
labels = ['Discounted cash flow\n(THE CENTRAL)', 'Relative multiples\n(EV/EBITDA)',
          'Asset lens\n(EV per tonne)', 'Book value\n(disclosed floor)']
fig, ax = plt.subplots(figsize=(9.8, 4.4), dpi=110)
xmin = min(LR[k]['bear'] for k in keys)
xmax = max(LR[k]['bull'] for k in keys)
span = xmax - xmin
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = LR[k]['bear'], LR[k]['base'], LR[k]['bull']
    col = GOLD if k == 'DCF (cash flow)' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col,
            alpha=0.55 if k == 'DCF (cash flow)' else 0.34, edgecolor=col, linewidth=1.2)
    ax.plot([ba, ba], [y - 0.24, y + 0.24], color=BRASS, lw=3.6)
    # All labels sit in a single column clear of the plot, so none can cross the spot
    # rule or another bar.
    ax.text(xmax + 0.055 * span, y, f'{b:.0f}–{bu:.0f}', va='center', ha='left',
            fontsize=9, color=INK)
    ax.text(xmax + 0.175 * span, y, f'base {ba:.1f}', va='center', ha='left',
            fontsize=9, color=INK, fontweight='bold')
ax.axvline(SPOT, color=RUST, lw=1.8, zorder=5)
ax.text(SPOT, len(keys) - 0.28, f'  spot {SPOT:.2f}', color=RUST, fontsize=9,
        fontweight='bold', va='bottom', ha='left')
ax.set_yticks(range(len(keys)))
ax.set_yticklabels(labels[::-1], fontsize=9)
ax.set_xlim(xmin - 0.05 * span, xmax + 0.34 * span)
ax.set_ylim(-0.6, len(keys) - 0.15)
ax.set_xlabel('Value per share (EGP)')
ax.set_title('Valuation by lens, against the market price', fontsize=11.5,
             fontweight='bold', loc='left', pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig1_football.png')

# ---- F2 sensitivity heat grid ------------------------------------------------
fig, ax = plt.subplots(figsize=(8.6, 4.3), dpi=110)
G = np.array(SN['wacc_g'])
cmap = plt.get_cmap('YlGnBu')
norm = plt.Normalize(G.min(), G.max())
im = ax.imshow(G, cmap=cmap, norm=norm, aspect='auto')
ax.set_xticks(range(5)); ax.set_xticklabels([f'{g:.0%}' for g in SN['g_grid']])
ax.set_yticks(range(5)); ax.set_yticklabels([f'{w:.1%}' for w in SN['wacc_grid']])
ax.set_xlabel('Terminal growth rate')
ax.set_ylabel('Explicit-window cost of capital')
# Text colour is chosen from each cell's OWN relative luminance, not from a value
# threshold: a mid-tone teal defeats both black and white if the cutoff is guessed.
for i in range(5):
    for j in range(5):
        r, g_, b, _ = cmap(norm(G[i, j]))
        lum = 0.2126 * r + 0.7152 * g_ + 0.0722 * b
        ax.text(j, i, f'{G[i, j]:.1f}', ha='center', va='center', fontsize=9.5,
                color=('#FFFFFF' if lum < 0.55 else '#12211F'), fontweight='bold')
ax.set_title('Fair value per share (EGP) — note that HIGHER growth gives a LOWER value',
             fontsize=11, fontweight='bold', loc='left', pad=12)
ax.grid(False)
save(fig, 'fig2_sens.png')

# ---- F3 price and moving averages -------------------------------------------
d3 = df[df['Date'] >= df['Date'].max() - np.timedelta64(365 * 3, 'D')]
fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=110)
ax.plot(d3['Date'], d3['Price'], color=CANVAS, lw=1.5, label='Close')
for win, col, lab in ((50, GOLD, '50-day'), (200, SAGE, '200-day')):
    ma = df['Price'].rolling(win).mean()
    ax.plot(df['Date'][df['Date'] >= d3['Date'].min()],
            ma[df['Date'] >= d3['Date'].min()], color=col, lw=1.6, label=f'{lab} average')
ax.axhline(SPOT, color=RUST, lw=1.0, ls='--')
ax.text(d3['Date'].iloc[0], SPOT, f' spot {SPOT:.2f}', color=RUST, fontsize=9,
        va='bottom', ha='left')
ax.set_ylabel('EGP per share')
ax.set_title('Three years of price, with the 50- and 200-day averages', fontsize=11.5,
             fontweight='bold', loc='left', pad=12)
ax.legend(frameon=False, loc='upper left', fontsize=9)
style(ax)
save(fig, 'fig3_ma.png')

# ---- F4 fan ------------------------------------------------------------------
paths = np.load(os.path.join(HERE, 'paths_3M.npy'))
h = paths.shape[1]
qs = [5, 25, 50, 75, 95]
Q = np.percentile(paths, qs, axis=0)
x = np.arange(h)
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
ax.fill_between(x, Q[0], Q[4], color=SAGE, alpha=0.25, label='5th–95th percentile')
ax.fill_between(x, Q[1], Q[3], color=GOLD, alpha=0.35, label='25th–75th percentile')
ax.plot(x, Q[2], color=CANVAS, lw=2.0, label='Median')
ax.axhline(SPOT, color=RUST, lw=1.2, ls='--')
ax.text(0, SPOT, f' spot {SPOT:.2f}', color=RUST, fontsize=9, va='bottom')
for q, yv in zip(qs, Q[:, -1]):
    ax.text(h * 1.01, yv, f'{yv:.0f}', fontsize=8.8, color=INK, va='center')
ax.set_xlim(0, h * 1.09)
ax.set_xlabel('Trading sessions ahead')
ax.set_ylabel('EGP per share')
ax.set_title('Three-month price cone — ILLUSTRATIVE ONLY, this cone is materially too wide',
             fontsize=11, fontweight='bold', loc='left', pad=12)
ax.legend(frameon=False, loc='upper left', fontsize=9)
style(ax)
save(fig, 'fig4_fan.png')

# ---- F5/F6 terminal distributions --------------------------------------------
for tag, fname in (('1M', 'fig5_dist.png'), ('3M', 'fig6_dist.png')):
    p = np.load(os.path.join(HERE, f'paths_{tag}.npy'))[:, -1]
    hz = STK['horizons'][tag]
    fig, ax = plt.subplots(figsize=(8.6, 3.5), dpi=110)
    ax.hist(p, bins=90, range=(np.percentile(p, 0.5), np.percentile(p, 99.5)),
            color=SAGE, alpha=0.65, edgecolor='none')
    for q, col, lab in ((hz['pct']['p5'], GREY, '5th'), (hz['pct']['p50'], CANVAS, 'median'),
                        (hz['pct']['p95'], GREY, '95th')):
        ax.axvline(q, color=col, lw=1.6 if lab == 'median' else 1.1,
                   ls='-' if lab == 'median' else '--')
        ax.text(q, ax.get_ylim()[1] * 0.94, f' {lab} {q:.0f}', fontsize=8.8, color=INK,
                rotation=90, va='top', ha='left')
    ax.axvline(SPOT, color=RUST, lw=1.4)
    ax.text(SPOT, ax.get_ylim()[1] * 0.55, f' spot {SPOT:.0f}', fontsize=8.8, color=RUST,
            rotation=90, va='center', ha='right', fontweight='bold')
    ax.set_xlabel('EGP per share')
    ax.set_ylabel('Simulated paths')
    ax.set_title(f'{"One-month" if tag == "1M" else "Three-month"} outcome distribution '
                 f'— illustrative only', fontsize=11, fontweight='bold', loc='left', pad=10)
    style(ax)
    save(fig, fname)

# ---- F7 the FY2024 profit bridge (why FY2024 is not a base year) -------------
fig, ax = plt.subplots(figsize=(9.4, 3.9), dpi=110)
und = D['disposal']['underlying_fy24_pat']
gain = D['disposal']['gain']
bars = [('FY2023\nnet loss', H['pat'][0], RUST),
        ('FY2024\nunderlying', und, SAGE),
        ('FY2024\ndisposal gain', gain, GOLD),
        ('FY2024\nas reported', H['pat'][1], GREY),
        ('FY2025\nnet profit', H['pat'][2], CANVAS)]
xs = np.arange(len(bars))
for i, (lab, v, col) in enumerate(bars):
    ax.bar(i, v, color=col, alpha=0.85, width=0.62)
    ax.text(i, v + (170 if v >= 0 else -260), f'{v:,.0f}', ha='center',
            va='bottom' if v >= 0 else 'top', fontsize=9.5, fontweight='bold', color=INK)
ax.axhline(0, color=GREY, lw=1.0)
ax.set_xticks(xs)
ax.set_xticklabels([b[0] for b in bars], fontsize=9)
ax.set_ylabel('EGP million')
ax.set_ylim(min(H['pat']) - 700, max(H['pat']) + 900)
ax.set_title('Why FY2024 is not a base year: profit after tax, and what was in it',
             fontsize=11.5, fontweight='bold', loc='left', pad=12)
ax.grid(axis='x', visible=False)
style(ax)
save(fig, 'fig7_bridge.png')

# ---- F8 sector supply and demand --------------------------------------------
PS = D['peers']['sector']
fig, ax = plt.subplots(figsize=(9.0, 3.7), dpi=110)
cats = ['Nameplate\ncapacity', 'Production\n2025', 'Domestic\nconsumption 2025',
        'Dormant capacity\nunder revival']
vals = [PS['capacity_mt'], PS['production_mt'], PS['consumption_mt'], PS['revival_mt']]
cols = [GREY, SAGE, CANVAS, RUST]
for i, (v, c) in enumerate(zip(vals, cols)):
    ax.bar(i, v, color=c, alpha=0.85, width=0.6)
    ax.text(i, v + 1.1, f'{v:.1f} Mt', ha='center', fontsize=9.5, fontweight='bold', color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels(cats, fontsize=9)
ax.set_ylabel('Million tonnes per year')
ax.set_ylim(0, max(vals) * 1.20)
ax.set_title('The Egyptian cement balance — the surplus is the whole sector case',
             fontsize=11.5, fontweight='bold', loc='left', pad=12)
ax.grid(axis='x', visible=False)
style(ax)
save(fig, 'fig8_sector.png')

# ---- FD1 expert panel --------------------------------------------------------
EXP = D['experts']
fig, ax = plt.subplots(figsize=(9.4, 3.6), dpi=110)
names = [e['label'] for e in EXP]
lo = [e['low'] for e in EXP]; hi = [e['high'] for e in EXP]; ce = [e['central'] for e in EXP]
for i in range(len(EXP)):
    y = len(EXP) - 1 - i
    ax.barh(y, hi[i] - lo[i], left=lo[i], height=0.42, color=SAGE, alpha=0.35,
            edgecolor=SAGE, linewidth=1.2)
    ax.plot([ce[i], ce[i]], [y - 0.22, y + 0.22], color=BRASS, lw=3.4)
    ax.text(max(hi) + 3.0, y, f'{lo[i]:.0f}–{hi[i]:.0f}', va='center', ha='left',
            fontsize=9, color=INK)
    ax.text(max(hi) + 15.0, y, f'central {ce[i]:.1f}', va='center', ha='left',
            fontsize=9, color=INK, fontweight='bold')
ax.axvline(SPOT, color=RUST, lw=1.7)
ax.text(SPOT, len(EXP) - 0.30, f'  spot {SPOT:.2f}', color=RUST, fontsize=9,
        fontweight='bold', va='bottom', ha='left')
ax.set_yticks(range(len(EXP)))
ax.set_yticklabels(names[::-1], fontsize=9.5)
ax.set_xlim(min(lo) - 6, max(hi) + 34)
ax.set_xlabel('Value per share (EGP)')
ax.set_title('The expert panel — three independent methods', fontsize=11.5,
             fontweight='bold', loc='left', pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'figD1_experts.png')
print('figures done')
