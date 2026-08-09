"""ADNOCLS study figures. House palette; SOLID light background on every figure so the
numbers stay readable when the page behind them is dark, and label positions chosen so
nothing overlaps a title, an axis or another label.

Reads study_numbers.json exclusively — no financial numeral is typed into this file."""
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
TEAL, RUST, SLATE = '#3E6F68', '#A2603A', '#5B6E86'
BG = '#FBF9F4'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG})

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M = D['meta']
SPOT = M['spot_aed']
IN = {k: v['value'] for k, v in D['inputs'].items()}


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), facecolor=BG, transparent=False)
    plt.close(fig)
    print('  wrote', name)


# ---- F1 valuation football field --------------------------------------------
L = D['lenses']
keys = ['dcf', 'dcf_asset_beta', 'relative', 'normalized', 'book',
        'central', 'central_asset_beta']
names = ['Cash-flow model\n(own regressed beta)',
         'Cash-flow model\n(asset-risk beta 1.0)',
         'Relative multiples',
         'Normalised\nearnings power',
         'Book value and\nsustainable return',
         'Weighted central\n(own beta)',
         'Weighted central\n(asset beta)']
fig, ax = plt.subplots(figsize=(9.7, 5.3), dpi=110)
xmax = max(L[k]['bull'] for k in keys)
xmin = min(L[k]['bear'] for k in keys)
rng = xmax - xmin
for i, k in enumerate(keys):
    y = len(keys) - 1 - i
    b, ba, bu = L[k]['bear'], L[k]['base'], L[k]['bull']
    central = k.startswith('central')
    col = GOLD if central else SAGE
    ax.barh(y, bu - b, left=b, height=0.50, color=col,
            alpha=0.50 if central else 0.32, edgecolor=col, linewidth=1.1)
    ax.plot([ba, ba], [y - 0.25, y + 0.25], color=BRASS, lw=3.4)
    ax.text(bu + 0.02 * rng, y, f'{b:.2f}–{bu:.2f}  ·  base {ba:.2f}',
            va='center', fontsize=8.6, color=INK)
ax.axvline(SPOT, color=INK, lw=1.7)
ax.text(SPOT + 0.010 * rng, -0.80, f'market price {SPOT:.2f}', color=INK, fontsize=9,
        ha='left', va='center')
ax.set_yticks(range(len(keys)))
ax.set_yticklabels(names[::-1], fontsize=8.4)
ax.set_xlabel('AED per share')
ax.set_xlim(xmin - 0.06 * rng, xmax + 0.34 * rng)
ax.set_ylim(-1.15, len(keys) - 0.40)
ax.set_title('ADNOC Logistics & Services — fair-value field by lens (bear–bull span; '
             'brass tick = base)\nThe two cash-flow rows are the same model on two '
             'costs of equity, shown side by side and never averaged',
             fontsize=10, pad=11)
style(ax)
fig.tight_layout()
save(fig, 'fig1_football.png')

# ---- F2 sensitivity: beta x terminal growth, and the mid-cycle rate anchor ----
S = D['sens']
tab = np.array(S['grid_beta_g'])
fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.2), dpi=110,
                         gridspec_kw={'width_ratios': [1.32, 1.0]})
ax = axes[0]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD])
ax.imshow(tab, cmap=cmap, aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=9.2, color=INK,
                fontweight='bold' if abs(v - SPOT) < 0.35 else 'normal')
ax.set_xticks(range(len(S['gs'])))
ax.set_xticklabels([f'{x*100:.1f}%' for x in S['gs']], fontsize=8.6)
ax.set_yticks(range(len(S['betas'])))
ax.set_yticklabels([f'{b:.3f}' if abs(b - IN['beta']) < 1e-9 else f'{b:.2f}'
                    for b in S['betas']], fontsize=8.6)
ax.set_xlabel('terminal growth rate', fontsize=9)
ax.set_ylabel('beta used in the cost of equity', fontsize=9)
ax.set_title('Fair value (AED/share) — beta × terminal growth\nbold = within '
             f'0.35 of the market price of {SPOT:.2f}', fontsize=9.6, pad=8)
ax.grid(False)

ax2 = axes[1]
mults = sorted(S['anchor'].keys(), key=float)
xs = [float(m) for m in mults]
ys = [S['anchor'][m] for m in mults]
ax2.plot(xs, ys, color=BRASS, lw=2.2, marker='o', ms=6, zorder=3)
for x, y in zip(xs, ys):
    ax2.annotate(f'{y:.2f}', (x, y), textcoords='offset points', xytext=(0, 9),
                 ha='center', fontsize=8.8, color=INK)
ax2.axhline(SPOT, color=INK, lw=1.4, ls=':')
ax2.text(xs[0], SPOT, f' market price {SPOT:.2f}', color=INK, fontsize=8.4,
         ha='left', va='bottom')
ax2.set_xticks(xs)
ax2.set_xticklabels([f'{x:.0%}' for x in xs], fontsize=8.6)
ax2.set_xlabel('mid-cycle tanker rate anchor, against the base', fontsize=9)
ax2.set_ylabel('AED per share', fontsize=9)
lo, hi = min(ys + [SPOT]), max(ys)
ax2.set_ylim(lo - 0.10 * (hi - lo), hi + 0.22 * (hi - lo))
ax2.set_title('Fair value against the rate the fleet reverts to\nthe single most '
              'consequential operating input', fontsize=9.6, pad=8)
style(ax2)
fig.tight_layout()
save(fig, 'fig2_sens.png')

# ---- F3 price, moving averages and the level ladder ---------------------------
T = D['technicals']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ADNOCLS_Stock_Price_History.csv')),
                  'ADNOCLS', verbose=False, market='AE')
px = df.set_index('Date')['Price']
win = 300
s = px.iloc[-win:]
fig, ax = plt.subplots(figsize=(10.5, 4.6), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.8, label='ADNOCLS close', zorder=4)
for n, c in [(20, GOLD), (50, BRASS), (200, SLATE)]:
    ma = px.rolling(n).mean().iloc[-win:]
    ax.plot(ma.index, ma.values, color=c, lw=1.3, label=f'{n}-session average', zorder=3)
lo = min(s.min(), min(T['levels']['sup']))
hi = max(s.max(), max(T['levels']['res']))
pad = 0.10 * (hi - lo)
x0, x1 = s.index[0], s.index[-1]
span = (x1 - x0)
bbox = dict(boxstyle='round,pad=0.16', facecolor=BG, edgecolor='none', alpha=0.95)
for lv in T['levels']['res']:
    ax.axhline(lv, color=RUST, lw=1.0, ls='--', alpha=0.85, zorder=2)
    ax.text(x1 + 0.012 * span, lv, f'R {lv:.2f}', color=RUST, fontsize=8.0,
            va='center', ha='left', bbox=bbox, zorder=6)
for lv in T['levels']['sup']:
    ax.axhline(lv, color=TEAL, lw=1.0, ls='--', alpha=0.85, zorder=2)
    ax.text(x1 + 0.012 * span, lv, f'S {lv:.2f}', color=TEAL, fontsize=8.0,
            va='center', ha='left', bbox=bbox, zorder=6)
ax.set_ylim(lo - pad, hi + pad)
ax.set_xlim(x0, x1 + 0.105 * span)
from matplotlib.lines import Line2D
h, l = ax.get_legend_handles_labels()
h += [Line2D([0], [0], color=RUST, lw=1.0, ls='--'),
      Line2D([0], [0], color=TEAL, lw=1.0, ls='--')]
l += ['R — resistance', 'S — support']
ax.legend(h, l, frameon=False, fontsize=8.5, ncol=2, labelcolor=INK, loc='upper left')
ax.set_ylabel('AED per share')
ax.set_title(f'Price against the moving-average stack, with the computed level ladder — '
             f'last {win} sessions to {T["data_date"]}', fontsize=10, pad=9)
style(ax)
fig.tight_layout()
save(fig, 'fig3_ma.png')

# ---- F4 forward cone ----------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
qs = [5, 25, 50, 75, 95]
fan = np.percentile(paths3, qs, axis=0)
days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.6), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5th–95th percentile')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32,
                label='25th–75th percentile')
ax.plot(days, fan[2], color=INK, lw=2, label='median path')
ax.axhline(SPOT, color=GREY, lw=1.2, ls=':')
cb = D['central']
cba = D['central_asset_beta']
ax.axhline(cb, color=BRASS, lw=1.5, ls='--')
ax.axhline(cba, color=TEAL, lw=1.5, ls='--')
ymax, ymin = fan[4].max(), fan[0].min()
r = ymax - ymin
ax.text(days[-1] - 0.5, cb + 0.018 * r, f'weighted central, own beta  {cb:.2f}',
        color=BRASS, fontsize=8.6, va='bottom', ha='right')
ax.text(days[-1] - 0.5, cba + 0.018 * r, f'weighted central, asset beta  {cba:.2f}',
        color=TEAL, fontsize=8.6, va='bottom', ha='right')
ax.text(0.8, SPOT - 0.030 * r, f'market price {SPOT:.2f}', color=GREY,
        fontsize=8.6, ha='left', va='top')
ax.set_xlabel('trading sessions ahead')
ax.set_ylabel('AED per share')
ax.set_xlim(0, days[-1])
ax.set_ylim(ymin - 0.06 * r, ymax + 0.12 * r)
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='lower left')
ax.set_title('Forward price cone to three months — 50,000 simulated paths from the '
             'anchor close', fontsize=10, pad=9)
style(ax)
fig.tight_layout()
save(fig, 'fig4_fan.png')

# ---- F5 / F6 outcome distributions --------------------------------------------
STK = D['strike']
for tag, fn, out, hz in [('one month', 'paths_1M.npy', 'fig5_dist.png', '1M'),
                         ('three months', 'paths_3M.npy', 'fig6_dist.png', '3M')]:
    x = np.load(os.path.join(HERE, fn))[:, -1]
    p = STK['horizons'][hz]['pct']
    fig, ax = plt.subplots(figsize=(7.8, 3.9), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.92, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(SPOT, color=INK, lw=1.7)
    ax.axvline(p['p50'], color=BRASS, lw=1.7, ls='--')
    for k, lbl in [('p5', '5th'), ('p95', '95th')]:
        ax.axvline(p[k], color=GREY, lw=1.0, ls=':')
    yl = ax.get_ylim()[1]
    ax.set_ylim(0, yl * 1.16)
    yl = ax.get_ylim()[1]
    ax.text(SPOT, yl * 0.985, f'market price {SPOT:.2f} ', color=INK, fontsize=8.4,
            ha='right', va='top')
    ax.text(p['p50'], yl * 0.86, f' median {p["p50"]:.2f}', color=BRASS, fontsize=8.4,
            ha='left', va='top')
    ax.text(p['p5'], yl * 0.50, f'5th {p["p5"]:.2f} ', color=GREY, fontsize=8.0,
            ha='right', va='center')
    ax.text(p['p95'], yl * 0.50, f' 95th {p["p95"]:.2f}', color=GREY, fontsize=8.0,
            ha='left', va='center')
    ax.set_xlim(np.percentile(x, 0.25), np.percentile(x, 99.75))
    ax.set_xlabel('AED per share')
    ax.set_yticks([])
    ax.set_title(f'Simulated price distribution at {tag}', fontsize=10, pad=8)
    style(ax)
    fig.tight_layout()
    save(fig, out)

# ---- F7 earnings mix by business unit -----------------------------------------
GH, FG = D['grp_hist'], D['fcst_group']
GROUPS = D['groups']
yrs = [y.replace('FY', '') for y in D['hist_is']['year']] + \
      [y.replace('FY', '') for y in D['fcst']['years']]
series = {g: [v / 1000.0 for v in GH[g]['ebitda']] + [v / 1000.0 for v in FG[g]['ebitda']]
          for g in GROUPS}
tot = np.array([sum(series[g][i] for g in GROUPS) for i in range(len(yrs))])
rev_tot = np.array([sum(GH[g]['revenue'][i] for g in GROUPS) for i in range(3)] +
                   [sum(FG[g]['rev'][i] for g in GROUPS) for i in range(5)]) / 1000.0
margin = tot / rev_tot
cols = {'Integrated Logistics': SAGE, 'Shipping': GOLD, 'Services': SLATE}
fig, (axb, axm) = plt.subplots(2, 1, figsize=(9.9, 5.6), dpi=110, sharex=True,
                               gridspec_kw={'height_ratios': [2.5, 1.0], 'hspace': 0.10})
xs = np.arange(len(yrs))
bottom = np.zeros(len(yrs))
for g in GROUPS:
    v = np.array(series[g])
    axb.bar(xs, v, width=0.60, bottom=bottom, color=cols[g], alpha=0.88, label=g,
            edgecolor='#FFFFFF', linewidth=0.7)
    bottom = bottom + v
for i, t in enumerate(tot):
    axb.text(i, t + 0.028 * tot.max(), f'{t:,.0f}', ha='center', fontsize=8.4, color=INK)
axb.axvline(2.5, color=GREY, lw=1.1, ls='--')
axb.set_ylim(0, tot.max() * 1.32)
axb.set_ylabel('earnings before interest, tax,\ndepreciation and amortisation (USD mn)',
               fontsize=9)
axb.legend(frameon=False, fontsize=8.5, loc='upper left', labelcolor=INK, ncol=3)
axb.set_title('Earnings by business unit, reported and forecast, with the group margin',
              fontsize=10, pad=10)
style(axb)

axm.plot(xs, margin * 100, color=BRASS, lw=2.1, marker='o', ms=5)
for i, m in enumerate(margin):
    axm.annotate(f'{m*100:.0f}%', (i, m * 100), textcoords='offset points',
                 xytext=(0, 9), ha='center', fontsize=8.2, color=BRASS)
axm.axvline(2.5, color=GREY, lw=1.1, ls='--')
lo_m, hi_m = min(margin) * 100, max(margin) * 100
axm.set_ylim(lo_m - 3.0, hi_m + 6.5)
axm.text(2.40, hi_m + 4.6, 'reported  ', ha='right', fontsize=8.6, color=GREY)
axm.text(2.60, hi_m + 4.6, '  forecast', ha='left', fontsize=8.6, color=GREY)
axm.set_ylabel('group margin\non revenue (%)', color=BRASS, fontsize=9)
axm.tick_params(axis='y', colors=BRASS)
axm.set_xticks(xs)
axm.set_xticklabels(yrs, fontsize=8.8)
style(axm)
fig.tight_layout()
save(fig, 'fig7_mix.png')

# ---- F8 tanker time-charter equivalent by class by quarter ---------------------
QLAB = ['2024 Q1', '2024 Q2', '2024 Q3', '2024 Q4',
        '2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1', '2026 Q2']
QKEY = ['24q1', '24q2', '24q3', '24q4', '25q1', '25q2', '25q3', '25q4',
        'q1_26', 'q2_26']
CLS = [('vlcc', 'Very large crude carriers', RUST),
       ('lr2', 'Long range 2', BRASS),
       ('lr1', 'Long range 1', TEAL),
       ('mr', 'Medium range', SLATE)]
fig, ax = plt.subplots(figsize=(10.4, 4.9), dpi=110)
xs = np.arange(len(QLAB))
ax.axvspan(7.5, 9.5, color=GOLD, alpha=0.13, zorder=0)
for key, lbl, col in CLS:
    ys, xx = [], []
    for i, q in enumerate(QKEY):
        k = f'tce_{key}_{q}'
        if k in IN:
            xx.append(i)
            ys.append(IN[k])
    ax.plot(xx, ys, color=col, lw=2.0, marker='o', ms=5, label=lbl, zorder=3)
    ax.annotate(f'{ys[-1]:,.0f}', (xx[-1], ys[-1]), textcoords='offset points',
                xytext=(7, 0), ha='left', va='center', fontsize=8.4, color=col)
mid = D['fleet']['tce_mid']
for key, lbl, col in CLS:
    ax.plot([-0.35, len(QLAB) - 0.55], [mid[key]] * 2, color=col, lw=1.0, ls=':',
            alpha=0.75, zorder=1)
ax.text(0.15, 175000, 'dotted lines: the mid-cycle rate each class reverts to in the '
        'forecast', fontsize=8.2, color=GREY, va='center', ha='left')
mcc = D['sens']['market_cross_check']
ax.plot([-0.35, len(QLAB) - 0.55], [mcc['vlcc_1y_tc']] * 2, color=INK, lw=1.3, ls='-.',
        alpha=0.9, zorder=2)
ax.text(0.15, mcc['vlcc_1y_tc'] * 1.10,
        f'one-year time charter fixed by a listed owner, early 2026: '
        f'{mcc["vlcc_1y_tc"]:,.0f} a day', fontsize=8.2, color=INK, va='bottom',
        ha='left')
ax.set_yscale('log')
ticks = [20000, 30000, 50000, 80000, 130000, 200000, 300000]
ax.set_yticks(ticks)
ax.set_yticklabels([f'{t/1000:,.0f}k' for t in ticks], fontsize=8.6)
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_ylim(13500, 400000)
ax.set_xticks(xs)
ax.set_xticklabels(QLAB, fontsize=8.4)
ax.set_xlim(-0.45, len(QLAB) - 0.20)
ax.text(8.5, 392000, 'first quarter reported;\nsecond quarter as indicated',
        ha='center', va='top', fontsize=8.4, color=BRASS)
ax.set_ylabel('time-charter equivalent (USD per vessel per day, log scale)', fontsize=9)
ax.legend(frameon=False, fontsize=8.5, ncol=4, labelcolor=INK, loc='lower left')
ax.set_title('The crux, made visible — tanker earnings per vessel per day by class, '
             'by quarter', fontsize=10, pad=9)
style(ax)
fig.tight_layout()
save(fig, 'fig8_tce.png')

# ---- FD1 the three expert ranges ----------------------------------------------
E = D['experts']
ex = [(f"Expert 1 — {E['e1']['method_short']}", E['e1']['base'], E['e1']['rng']),
      (f"Expert 2 — {E['e2']['method_short']}", E['e2']['base'], E['e2']['rng']),
      (f"Expert 3 — {E['e3']['method_short']}", E['e3']['base'], E['e3']['rng'])]
fig, ax = plt.subplots(figsize=(9.7, 3.7), dpi=110)
his = [hi for _, _, (lo, hi) in ex]
los = [lo for _, _, (lo, hi) in ex]
xr = max(his) - min(los)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.44, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.22, y + 0.22], color=BRASS, lw=3.4)
    ax.text(hi + 0.02 * xr, y, f'{lo:.2f}–{hi:.2f}  ·  base {ba:.2f}', va='center',
            fontsize=8.6, color=INK)
ax.axvline(SPOT, color=INK, lw=1.7)
pc_ = D['panel_centre']
ax.axvspan(pc_ * 0.96, pc_ * 1.04, color=GOLD, alpha=0.15)
ax.text(SPOT + 0.012 * xr, -0.72, f'market price {SPOT:.2f}', fontsize=9, color=INK,
        ha='left', va='center')
ax.text(pc_, len(ex) - 0.44, f'panel centre {pc_:.2f}', fontsize=8.6, color=BRASS,
        ha='center', va='bottom')
ax.set_yticks(range(len(ex)))
ax.set_yticklabels([e[0] for e in ex][::-1], fontsize=8.6)
ax.set_xlabel('AED per share')
ax.set_xlim(min(los) - 0.08 * xr, max(his) + 0.32 * xr)
ax.set_ylim(-1.05, len(ex) - 0.20)
ax.set_title('The three expert ranges — brass tick is each base case; gold band is the '
             'panel centre', fontsize=10, pad=10)
style(ax)
fig.tight_layout()
save(fig, 'figD1_experts.png')

print('figures done')
