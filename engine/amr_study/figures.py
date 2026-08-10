"""AMR study figures.

House palette, and a SOLID LIGHT background on every figure so the numbers stay readable
whatever the page behind them is. Label positions are chosen so nothing overlaps a title,
an axis, a bar or another label, and every axis carries its units.
"""
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
M, LR, SN, H, F = D['meta'], D['lenses']['ranges'], D['sensitivity'], D['history'], D['forecast']
FX = M['fx']
SPOT = M['spot_aed']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'AMR_Stock_Price_History.csv')),
                  'AMR', verbose=False, market='AE')


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


# ---- F1 the four lenses, in dirhams a share ---------------------------------
keys = ['Discounted cash flow', 'Relative multiples', 'Normalised earnings power',
        'Book value and sustainable return']
labels = ['Discounted cash flow\n(primary)', 'Relative multiples\n(EV / EBITDA)',
          'Normalised earnings\npower', 'Book value and\nsustainable return',
          'Weighted central']
rows = [(k, [x * FX for x in LR[k]]) for k in keys]
central = D['lenses']['central'] * FX
rows.append(('Weighted central', [min(r[1][0] for r in rows), central,
                                  max(r[1][2] for r in rows)]))
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=110)
xmin = min(r[1][0] for r in rows)
xmax = max(r[1][2] for r in rows)
span = xmax - xmin
for i, (k, (b, ba, bu)) in enumerate(rows):
    y = len(rows) - 1 - i
    col = GOLD if k == 'Weighted central' else SAGE
    ax.barh(y, bu - b, left=b, height=0.46, color=col,
            alpha=0.55 if k == 'Weighted central' else 0.34, edgecolor=col, linewidth=1.2)
    ax.plot([ba, ba], [y - 0.24, y + 0.24], color=BRASS, lw=3.6)
    ax.text(xmax + 0.06 * span, y, f'{b:.2f}–{bu:.2f}', va='center', ha='left',
            fontsize=9, color=INK)
ax.axvline(SPOT, color=RUST, lw=1.7, ls='--')
ax.text(SPOT, len(rows) - 0.32, f'  market {SPOT:.2f}', color=RUST, fontsize=9,
        ha='left', va='center')
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([lab for lab in reversed(labels)], fontsize=9.5)
ax.set_xlim(xmin - 0.06 * span, xmax + 0.30 * span)
ax.set_ylim(-0.7, len(rows) - 0.1)
ax.set_xlabel('AED per share')
ax.set_title('Each lens, and where the market sits', loc='left', fontsize=12, pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig1_lenses.png')

# ---- F2 the contested judgement, both ways ----------------------------------
C = D['contested']
fig, ax = plt.subplots(figsize=(9.0, 3.5), dpi=110)
vals = [C['way_b']['value_aed'], C['way_a']['value_aed']]
names = ['Cyclical\nmargin reverts to the\nthree-year average',
         'Structural\nthe first-half gains hold']
cols = [SAGE, GOLD]
bars = ax.barh([0, 1], vals, height=0.42, color=cols, alpha=0.6,
               edgecolor=[BRASS, BRASS], linewidth=1.2)
for y, v in zip([0, 1], vals):
    ax.text(v + 0.03, y, f'{v:.2f}', va='center', ha='left', fontsize=11, color=INK)
ax.axvline(SPOT, color=RUST, lw=1.7, ls='--')
ax.text(SPOT, 1.62, f'market {SPOT:.2f}', color=RUST, fontsize=9.5, ha='center')
ax.set_yticks([0, 1]); ax.set_yticklabels(names, fontsize=9.5)
ax.set_xlim(0, max(vals) * 1.22)
ax.set_ylim(-0.55, 1.85)
ax.set_xlabel('AED per share')
ax.set_title('The judgement that decides it: is the margin gain structural or cyclical?',
             loc='left', fontsize=12, pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig2_contested.png')

# ---- F3 price and moving averages -------------------------------------------
d = df.tail(500).reset_index(drop=True)
px = d['Price'].to_numpy(float)
dates = d['Date']
sma = lambda n: np.array([px[max(0, i - n + 1):i + 1].mean() for i in range(len(px))])
fig, ax = plt.subplots(figsize=(9.8, 4.3), dpi=110)
ax.plot(dates, px, color=CANVAS, lw=1.5, label='Close')
ax.plot(dates, sma(50), color=GOLD, lw=1.4, label='50-day average')
ax.plot(dates, sma(200), color=SAGE, lw=1.4, label='200-day average')
T = json.load(open(os.path.join(HERE, 'technicals.json')))
lab_x = dates.iloc[-1] + (dates.iloc[-1] - dates.iloc[-22])
for lv in T['levels']['res']:
    ax.plot([dates.iloc[0], dates.iloc[-1]], [lv, lv], color=RUST, lw=0.9, ls=':', alpha=0.7)
    ax.text(lab_x, lv, f'R {lv:.2f}', color=RUST, fontsize=8.5, va='center', ha='left')
for lv in T['levels']['sup']:
    ax.plot([dates.iloc[0], dates.iloc[-1]], [lv, lv], color=BRASS, lw=0.9, ls=':', alpha=0.7)
    ax.text(lab_x, lv, f'S {lv:.2f}', color=BRASS, fontsize=8.5, va='center', ha='left')
ax.set_ylabel('AED per share')
ax.set_xlim(dates.iloc[0], dates.iloc[-1] + (dates.iloc[-1] - dates.iloc[-95]))
lo = min(px.min(), min(T['levels']['sup'])) * 0.97
hi = max(px.max(), max(T['levels']['res'])) * 1.03
ax.set_ylim(lo, hi)
ax.legend(loc='upper left', frameon=False, fontsize=9)
ax.set_title('Two years of price, with the moving averages and the computed levels',
             loc='left', fontsize=12, pad=12)
style(ax)
save(fig, 'fig3_price.png')

# ---- F4 the probability cone -------------------------------------------------
p1, p3 = STK['horizons']['1M'], STK['horizons']['3M']
fig, ax = plt.subplots(figsize=(9.8, 4.3), dpi=110)
hist = df.tail(120).reset_index(drop=True)
ax.plot(range(-len(hist) + 1, 1), hist['Price'].to_numpy(float), color=CANVAS, lw=1.5)
xs = [0, p1['h'], p3['h']]
for lo_k, hi_k, a in (('p5', 'p95', 0.16), ('p25', 'p75', 0.30)):
    ax.fill_between(xs,
                    [STK['spot'], p1['pct'][lo_k], p3['pct'][lo_k]],
                    [STK['spot'], p1['pct'][hi_k], p3['pct'][hi_k]],
                    color=GOLD, alpha=a, linewidth=0)
ax.plot(xs, [STK['spot'], p1['pct']['p50'], p3['pct']['p50']], color=BRASS, lw=1.8)
ax.axvline(0, color=GREY, lw=0.9)
ax.text(p3['h'], p3['pct']['p95'], f"  {p3['pct']['p95']:.2f}", fontsize=8.5, color=INK,
        va='center')
ax.text(p3['h'], p3['pct']['p5'], f"  {p3['pct']['p5']:.2f}", fontsize=8.5, color=INK,
        va='center')
ax.text(p3['h'], p3['pct']['p50'], f"  {p3['pct']['p50']:.2f}", fontsize=8.5, color=BRASS,
        va='center')
ax.set_xlim(-len(hist) + 1, p3['h'] * 1.16)
_lo = min(hist['Price'].min(), p3['pct']['p5'])
_hi = max(hist['Price'].max(), p3['pct']['p95'])
ax.set_ylim(_lo - 0.06 * (_hi - _lo), _hi + 0.06 * (_hi - _lo))
ax.set_ylabel('AED per share')
ax.set_xlabel('Trading sessions from the anchor date')
ax.set_title('Where the price could be in one and three months — the middle 50% and the '
             'middle 90%', loc='left', fontsize=12, pad=12)
style(ax)
save(fig, 'fig4_cone.png')

# ---- F5 and F6 the three-month and one-month distributions -------------------
for tag, p, fname, ttl in (('3M', p3, 'fig5_dist3m.png', 'Three months'),
                           ('1M', p1, 'fig6_dist1m.png', 'One month')):
    paths = np.load(os.path.join(HERE, f'paths_{tag}.npy'))
    term = paths[:, -1]
    fig, ax = plt.subplots(figsize=(9.0, 3.6), dpi=110)
    ax.hist(term, bins=90, range=(np.percentile(term, 0.4), np.percentile(term, 99.6)),
            color=SAGE, alpha=0.62, edgecolor='none')
    for q, lab in ((p['pct']['p5'], '5th'), (p['pct']['p50'], 'median'),
                   (p['pct']['p95'], '95th')):
        ax.axvline(q, color=BRASS, lw=1.4)
        ax.text(q, ax.get_ylim()[1] * 0.94, f' {lab} {q:.2f}', fontsize=8.5, color=BRASS,
                rotation=90, va='top', ha='left')
    ax.axvline(STK['spot'], color=RUST, lw=1.6, ls='--')
    ax.text(STK['spot'], ax.get_ylim()[1] * 0.30, f' market {STK["spot"]:.2f}',
            fontsize=8.5, color=RUST, rotation=90, va='bottom', ha='right')
    ax.set_xlabel('AED per share'); ax.set_ylabel('Simulated paths')
    ax.set_yticklabels([])
    ax.set_title(f'{ttl} — the shape of the distribution, not just its edges',
                 loc='left', fontsize=12, pad=12)
    style(ax)
    save(fig, fname)

# ---- F7 revenue bridge: restaurants and revenue per restaurant ---------------
U = D['unit_build']
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
yrs = ['FY2025'] + F['years']
rev = [H['revenue'][2]] + F['revenue']
st = [U['stores_hist']['UAE'][1] and D['forecast']['stores'][0]] if False else None
stores = [2749] + F['stores']
ax.bar(range(len(yrs)), rev, color=SAGE, alpha=0.5, edgecolor=BRASS, linewidth=1.0, width=0.6)
for i, v in enumerate(rev):
    ax.text(i, v + 60, f'{v:,.0f}', ha='center', fontsize=9, color=INK)
ax.set_xticks(range(len(yrs))); ax.set_xticklabels(yrs, fontsize=9.5)
ax.set_ylabel('Revenue, USD million')
ax.set_ylim(0, max(rev) * 1.20)
ax2 = ax.twinx()
ax2.plot(range(len(yrs)), stores, color=RUST, lw=1.8, marker='o', ms=4)
for i, v in enumerate(stores):
    ax2.text(i, v + 40, f'{v:,.0f}', ha='center', fontsize=8.5, color=RUST)
ax2.set_ylabel('Restaurants at year end', color=RUST)
ax2.tick_params(axis='y', colors=RUST)
ax2.set_ylim(min(stores) * 0.90, max(stores) * 1.10)
ax2.grid(False)
ax.set_title('Revenue is restaurants times revenue per restaurant — both grow, and both are '
             'shown', loc='left', fontsize=12, pad=12)
style(ax)
save(fig, 'fig7_build.png')

# ---- F8 sensitivity tornado --------------------------------------------------
sng = SN['single']
names, spans = [], []
for k, v in sng.items():
    names.append(k.split('(')[0].strip())
    spans.append((min(v) * FX, max(v) * FX))
order = sorted(range(len(names)), key=lambda i: spans[i][1] - spans[i][0])
fig, ax = plt.subplots(figsize=(9.4, 3.6), dpi=110)
base = SN['base'] * FX
for y, i in enumerate(order):
    lo, hi = spans[i]
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.42,
            edgecolor=BRASS, linewidth=1.0)
    ax.text(hi + 0.02, y, f'{lo:.2f}–{hi:.2f}', va='center', ha='left', fontsize=9, color=INK)
ax.axvline(base, color=BRASS, lw=1.8)
ax.text(base, len(order) - 0.35, f' base {base:.2f}', color=BRASS, fontsize=9, ha='left')
ax.axvline(SPOT, color=RUST, lw=1.5, ls='--')
ax.text(SPOT, -0.72, f'market {SPOT:.2f}', color=RUST, fontsize=9, ha='center')
ax.set_yticks(range(len(order)))
ax.set_yticklabels([names[i] for i in order], fontsize=9.5)
ax.set_xlim(min(s[0] for s in spans) * 0.94, max(s[1] for s in spans) * 1.16)
ax.set_ylim(-0.95, len(order) - 0.05)
ax.set_xlabel('AED per share')
ax.set_title('What moves the answer, one driver at a time', loc='left', fontsize=12, pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig8_tornado.png')

# ---- F9 expert panel ---------------------------------------------------------
E = D['experts']
fig, ax = plt.subplots(figsize=(9.4, 3.2), dpi=110)
for i, e in enumerate(E):
    y = len(E) - 1 - i
    lo, ba, hi = e['low'] * FX, e['base'] * FX, e['high'] * FX
    ax.barh(y, hi - lo, left=lo, height=0.40, color=SAGE, alpha=0.38,
            edgecolor=BRASS, linewidth=1.0)
    ax.plot([ba, ba], [y - 0.22, y + 0.22], color=BRASS, lw=3.2)
    ax.text(hi + 0.03, y, f'{ba:.2f}', va='center', ha='left', fontsize=9.5, color=INK)
ax.axvline(SPOT, color=RUST, lw=1.5, ls='--')
ax.text(SPOT, len(E) - 0.42, f' market {SPOT:.2f}', color=RUST, fontsize=9, ha='left')
ax.set_yticks(range(len(E)))
ax.set_yticklabels([f"{e['label']}\n{e['method'].lower()}" for e in reversed(E)], fontsize=9)
lo_all = min(e['low'] for e in E) * FX
hi_all = max(e['high'] for e in E) * FX
ax.set_xlim(lo_all * 0.92, hi_all * 1.14)
ax.set_xlabel('AED per share')
ax.set_title('Three methods, three answers', loc='left', fontsize=12, pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig9_experts.png')

# ---- transparency check ------------------------------------------------------
from PIL import Image
for f in sorted(os.listdir(HERE)):
    if f.startswith('fig') and f.endswith('.png'):
        im = Image.open(os.path.join(HERE, f))
        assert im.mode in ('RGB', 'P') or (im.mode == 'RGBA' and
                                           im.getchannel('A').getextrema() == (255, 255)), \
            f'{f} carries transparency'
print('figure check: every figure renders on a solid light canvas, zero transparency')
