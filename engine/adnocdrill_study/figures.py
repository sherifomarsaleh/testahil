"""ADNOC Drilling study figures.

House palette, and a SOLID light canvas on every figure so the numbers stay
readable when the page behind them is dark — no transparency anywhere, verified
programmatically at the end of this file. Label positions are chosen so nothing
overlaps a title, an axis, or another label, and every figure is inspected as a
rendered image before it ships.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
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

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
ST = json.load(open(os.path.join(HERE, 'strike_result.json')))
TA = json.load(open(os.path.join(HERE, 'technicals.json')))
spot = D['market']['spot_aed']
FIGS = []


def style(ax):
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
    for s_ in ('left', 'bottom'):
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    p = os.path.join(HERE, name)
    fig.savefig(p, facecolor=BG, transparent=False)
    plt.close(fig)
    FIGS.append(p)


# ---- F1 valuation football field -------------------------------------------
LR = D['fair_value']['lens_range']
CR = D['fair_value']['central_range']
names = ['Discounted cash flow\ncontinued expansion', 'Discounted cash flow\ncapacity plateau',
         'Relative multiples\n(EV/EBITDA, peer set)', 'Book value and\nsustainable return',
         'Normalised\nearnings power', 'Weighted central']
keys = ['dcf_A', 'dcf_B', 'relative', 'book', 'normalised', 'central']
band = dict(LR); band['central'] = CR
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=120)
xmax = max(band[k]['bull'] for k in keys)
xmin = min(band[k]['bear'] for k in keys)
# Labels sit in a single column to the right of the WIDEST bar and of the
# market-price line, not at each bar's own end — otherwise the vertical price
# line runs straight through whichever label happens to start behind it.
label_x = max(xmax, spot) + 0.04 * (xmax - xmin)
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = band[k]['bear'], band[k]['base'], band[k]['bull']
    col = GOLD if k == 'central' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col,
            alpha=0.52 if k == 'central' else 0.32, edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(label_x, y, f'{b:.2f}–{bu:.2f} · base {ba:.2f}',
            va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.008 * (xmax - xmin), -0.72, f'market price {spot:.2f}', color=INK, fontsize=9,
        ha='left', va='top')
ax.set_yticks(range(len(keys)))
ax.set_yticklabels(names[::-1], fontsize=8.4)
ax.set_xlabel('AED per share')
ax.set_xlim(xmin - 0.06 * (xmax - xmin), xmax + 0.34 * (xmax - xmin))
ax.set_ylim(-1.15, len(keys) - 0.4)
ax.set_title('ADNOC Drilling — fair-value range by lens (bar = bear-to-bull span, '
             'brass tick = base)', fontsize=10, pad=10)
style(ax)
fig.tight_layout()
save(fig, 'fig1_football.png')

# ---- F2 sensitivity heatmap -------------------------------------------------
S = D['sensitivity']
tab = np.array(S['matrix'])
fig, ax = plt.subplots(figsize=(8.1, 3.9), dpi=120)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=9.2, color=INK,
                fontweight='bold' if abs(v - spot) < 0.20 else 'normal')
ax.set_xticks(range(len(S['g_grid'])))
ax.set_xticklabels([f'{x*100:.1f}%' for x in S['g_grid']])
ax.set_yticks(range(len(S['wacc_grid'])))
ax.set_yticklabels([f'{x*100:.2f}%' for x in S['wacc_grid']])
ax.set_xlabel('terminal growth rate')
ax.set_ylabel('weighted average cost of capital')
ax.set_title(f'Value (AED/share), continued-expansion case — bold is within AED 0.20 of '
             f'the market price {spot:.2f}', fontsize=9.4, pad=8)
ax.grid(False)
fig.tight_layout()
save(fig, 'fig2_sens.png')

# ---- F3 price and the moving-average stack ----------------------------------
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ADNOCDRILL_Stock_Price_History.csv')),
                   'ADNOCDRILL', verbose=False, market='AE')
px = df['Price'].to_numpy(float)
dt = df['Date']
w = 400
fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=120)
ax.plot(dt[-w:], px[-w:], color=INK, lw=1.3, label='close')
for n, col, lab in ((20, GOLD, '20-day'), (50, BRASS, '50-day'), (200, SAGE, '200-day')):
    ma = np.convolve(px, np.ones(n) / n, mode='valid')
    ax.plot(dt[-len(ma):][-w:], ma[-w:], color=col, lw=1.5, label=f'{lab} average')
lev = TA['levels']
for v in lev['res']:
    ax.axhline(v, color=BRASS, lw=0.9, ls='--', alpha=0.75)
    ax.text(dt.iloc[-1], v, f'  {v:.2f}', color=BRASS, fontsize=8, va='center')
for v in lev['sup']:
    ax.axhline(v, color=SAGE, lw=0.9, ls=':', alpha=0.9)
    ax.text(dt.iloc[-1], v, f'  {v:.2f}', color=GREY, fontsize=8, va='center')
ax.set_ylabel('AED per share')
ax.set_xlim(dt.iloc[-w], dt.iloc[-1] + (dt.iloc[-1] - dt.iloc[-40]))
# The published resistance ladder runs along the top of the plot, so the legend
# goes to the bottom left where nothing else is drawn — a legend box sitting on
# top of a level line is exactly the overwriting this check exists to prevent.
ax.set_ylim(min(px[-w:].min(), min(lev['sup'])) * 0.955,
            max(px[-w:].max(), max(lev['res'])) * 1.015)
ax.legend(frameon=False, fontsize=8.4, ncol=4, loc='lower left')
ax.set_axisbelow(True)
ax.set_title('ADNOC Drilling — price, moving-average stack and computed support and '
             'resistance (dashed above, dotted below)', fontsize=10, pad=8)
style(ax)
fig.tight_layout()
save(fig, 'fig3_ma.png')

# ---- F4 three-month fan ------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
h = paths3.shape[1]
qs = [5, 25, 50, 75, 95]
band_q = np.percentile(paths3, qs, axis=0)
x = np.arange(h + 1)
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=120)
hist_n = 120
xb = np.arange(-hist_n, 1)
ax.plot(xb, px[-hist_n - 1:], color=INK, lw=1.2)
for lo, hi, a, lab in ((0, 4, 0.16, '5th–95th percentile'), (1, 3, 0.30, '25th–75th percentile')):
    ax.fill_between(x, np.r_[spot, band_q[lo]], np.r_[spot, band_q[hi]], color=GOLD, alpha=a,
                    linewidth=0, label=lab)
ax.plot(x, np.r_[spot, band_q[2]], color=BRASS, lw=1.6, label='median path')
ax.axhline(spot, color=GREY, lw=0.9, ls='--')
for k, lab in ((0, 'p5'), (1, 'p25'), (2, 'p50'), (3, 'p75'), (4, 'p95')):
    ax.text(h + 1.5, band_q[k][-1], f'{lab} {band_q[k][-1]:.2f}', fontsize=8.2, va='center',
            color=INK)
ax.set_xlim(-hist_n, h + 14)
ax.set_xlabel('trading sessions from the 07-Aug-2026 anchor')
ax.set_ylabel('AED per share')
ax.legend(frameon=False, fontsize=8.4, loc='upper left')
ax.set_title(f"Three-month probability cone to {ST['horizons']['3M']['grade_date']} — "
             f"50,000 simulated paths", fontsize=10, pad=8)
style(ax)
fig.tight_layout()
save(fig, 'fig4_fan.png')

# ---- F5 / F6 terminal distributions -----------------------------------------
for tag, fn, title in (('1M', 'fig5_dist.png', 'One-month'), ('3M', 'fig6_dist.png',
                                                              'Three-month')):
    p = np.load(os.path.join(HERE, f'paths_{tag}.npy'))[:, -1]
    hz = ST['horizons'][tag]
    fig, ax = plt.subplots(figsize=(8.4, 3.5), dpi=120)
    ax.hist(p, bins=90, color=SAGE, alpha=0.55, edgecolor='none')
    for q, col, lab in ((hz['pct']['p5'], BRASS, 'p5'), (hz['pct']['p50'], INK, 'median'),
                        (hz['pct']['p95'], BRASS, 'p95')):
        ax.axvline(q, color=col, lw=1.4, ls='--' if col == BRASS else '-')
    ax.axvline(spot, color=GOLD, lw=1.8)
    ymax = ax.get_ylim()[1]
    ax.text(spot, ymax * 0.97, f' market {spot:.2f}', color=BRASS, fontsize=8.6, va='top')
    ax.text(hz['pct']['p5'], ymax * 0.80, f" p5 {hz['pct']['p5']:.2f} ", color=INK, fontsize=8.4,
            ha='right', va='top')
    ax.text(hz['pct']['p95'], ymax * 0.80, f" p95 {hz['pct']['p95']:.2f}", color=INK, fontsize=8.4,
            ha='left', va='top')
    ax.set_xlabel('AED per share at the check date')
    ax.set_ylabel('simulated paths')
    ax.set_title(f"{title} outcome distribution at {hz['grade_date']} — "
                 f"probability of finishing above the current price "
                 f"{hz['p_above']*100:.0f}%", fontsize=10, pad=8)
    style(ax)
    fig.tight_layout()
    save(fig, fn)

# ---- F7 revenue build, history and forecast ---------------------------------
hist_years = [2023, 2024, 2025]
rowsA = D['cases']['A']['rows']
yrs = hist_years + [r['year'] for r in rowsA]
on = [D['history'][str(y)]['seg_onshore'] / 1e6 for y in hist_years] + \
     [r['seg_onshore'] / 1e6 for r in rowsA]
off = [D['history'][str(y)]['seg_offshore'] / 1e6 for y in hist_years] + \
      [r['seg_offshore'] / 1e6 for r in rowsA]
ofs = [D['history'][str(y)]['seg_ofs'] / 1e6 for y in hist_years] + \
      [r['seg_ofs'] / 1e6 for r in rowsA]
fig, ax = plt.subplots(figsize=(9.8, 4.1), dpi=120)
ax.set_axisbelow(True)      # gridlines behind the bars, not drawn through them
xs = np.arange(len(yrs))
ax.bar(xs, on, color=SAGE, label='Onshore', edgecolor='none')
ax.bar(xs, off, bottom=on, color=GOLD, label='Offshore', edgecolor='none')
ax.bar(xs, ofs, bottom=np.array(on) + np.array(off), color=BRASS, label='Oilfield Services',
       edgecolor='none')
tot = np.array(on) + np.array(off) + np.array(ofs)
for i, t in enumerate(tot):
    ax.text(i, t + 0.08, f'{t:.2f}', ha='center', fontsize=8.4, color=INK)
ax.axvline(2.5, color=GREY, lw=1.0, ls='--')
ax.text(2.55, max(tot) * 0.10, ' forecast', fontsize=8.6, color=GREY)
ax.set_xticks(xs)
ax.set_xticklabels([str(y) for y in yrs], fontsize=8.8)
ax.set_ylabel('USD billion')
ax.set_ylim(0, max(tot) * 1.16)
ax.legend(frameon=False, fontsize=8.6, ncol=3, loc='upper left')
ax.set_title('Revenue by segment — three audited years and the five-year unit build',
             fontsize=10, pad=8)
style(ax)
fig.tight_layout()
save(fig, 'fig7_mix.png')

# ---- F8 expert divergence ----------------------------------------------------
EX = json.load(open(os.path.join(HERE, 'experts.json')))
fig, ax = plt.subplots(figsize=(9.4, 3.6), dpi=120)
labels = [e['label'] for e in EX['experts']]
lo = [e['range'][0] for e in EX['experts']]
base_ = [e['base'] for e in EX['experts']]
hi = [e['range'][1] for e in EX['experts']]
ys = np.arange(len(labels))[::-1]
ex_label_x = max(max(hi), spot) + 0.06        # clear of the market-price line
for y, l_, b_, h_ in zip(ys, lo, base_, hi):
    ax.plot([l_, h_], [y, y], color=SAGE, lw=7, solid_capstyle='butt', alpha=0.45)
    ax.plot([b_, b_], [y - 0.18, y + 0.18], color=BRASS, lw=3.2)
    ax.text(ex_label_x, y, f'{l_:.2f}–{h_:.2f} · base {b_:.2f}', va='center', fontsize=8.6,
            color=INK)
ax.axvline(spot, color=INK, lw=1.5)
ax.text(spot + 0.03, -0.78, f'market price {spot:.2f}', fontsize=8.8, color=INK, va='top')
ax.set_yticks(ys)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('AED per share')
ax.set_xlim(min(lo) - 0.25, ex_label_x + 1.30)
ax.set_ylim(-1.15, len(labels) - 0.45)
ax.set_title('Three independent valuations of the same company, by method', fontsize=10, pad=8)
style(ax)
fig.tight_layout()
save(fig, 'figD1_experts.png')

# ---- figure discipline: no transparency anywhere -----------------------------
bad = []
for p in FIGS:
    im = Image.open(p)
    if im.mode in ('RGBA', 'LA'):
        alpha = np.array(im.split()[-1])
        if alpha.min() < 255:
            bad.append((os.path.basename(p), int(alpha.min())))
    im.close()
assert not bad, f'figures with transparent pixels: {bad}'
print(f'{len(FIGS)} figures written, all with a solid opaque canvas:')
for p in FIGS:
    im = Image.open(p)
    print(f'  {os.path.basename(p):22s} {im.size[0]}x{im.size[1]} mode={im.mode}')
    im.close()
