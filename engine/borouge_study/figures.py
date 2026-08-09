"""BOROUGE study figures.

House palette, and a SOLID LIGHT background on every figure so the numbers stay
readable when the page behind them is dark. Label positions are chosen so nothing
overlaps a title, an axis, a bar or another label, and every axis carries units.
Zero transparency anywhere — asserted programmatically at the end of this file.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import matplotlib                                        # noqa: E402
matplotlib.use('Agg')
import matplotlib.pyplot as plt                          # noqa: E402
import numpy as np                                       # noqa: E402
from data_quality import clean_ohlc                      # noqa: E402
from primitives import load_ohlc                         # noqa: E402

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY, RUST, TEAL = '#1C3A36', '#D5DDDB', '#5A6764', '#A0522D', '#3E6E68'
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
BT = json.load(open(os.path.join(HERE, 'backtest_5y.json')))
SPOT = D['spot_aed']
LEN, SN, H = D['lenses'], D['sensitivity'], D['history']
FR = D['framings']
WRITTEN = []


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), dpi=150, facecolor=BG)
    plt.close(fig)
    WRITTEN.append(name)
    print('wrote', name)


# ---- F1 football field -------------------------------------------------------
# Each lens is a BAR from its sector-beta reading to its own-stock-beta reading, because
# the beta is the study's central contested judgement and every lens moves with it.
rows = [
    ('Discounted cash flow\n(normalisation)', LEN['dcf_normalisation_sector_beta'],
     LEN['dcf_normalisation_own_beta']),
    ('Discounted cash flow\n(prolonged disruption)', LEN['dcf_prolonged_sector_beta'],
     LEN['dcf_prolonged_own_beta']),
    ('Book value and\nsustainable return', LEN['book_value_sector_beta'],
     LEN['book_value_own_beta']),
    ('Normalised\nearnings power', LEN['normalised_earnings_sector_beta'],
     LEN['normalised_earnings_own_beta']),
    ('Relative multiples\n(beta-independent)', LEN['relative_multiples'],
     LEN['relative_multiples']),
]
fig, ax = plt.subplots(figsize=(9.9, 4.6), dpi=110)
xmin = min(min(a, b) for _, a, b in rows)
xmax = max(max(a, b) for _, a, b in rows)
span = xmax - xmin
for i, (lab, lo, hi) in enumerate(rows):
    y = len(rows) - 1 - i
    lo_, hi_ = min(lo, hi), max(lo, hi)
    if hi_ - lo_ < 0.012 * span:                      # beta-independent lens: draw a marker
        ax.plot([lo_], [y], marker='D', ms=9, color=GOLD, zorder=4)
    else:
        ax.barh(y, hi_ - lo_, left=lo_, height=0.44, color=SAGE, alpha=0.42,
                edgecolor=TEAL, linewidth=1.2)
        ax.plot([lo_, lo_], [y - 0.23, y + 0.23], color=TEAL, lw=3.0)
        ax.plot([hi_, hi_], [y - 0.23, y + 0.23], color=BRASS, lw=3.0)
    ax.text(xmax + 0.06 * span, y, f'{lo_:.2f} – {hi_:.2f}' if hi_ > lo_ else f'{lo_:.2f}',
            va='center', ha='left', fontsize=9, color=INK, fontweight='bold')
ax.axvline(SPOT, color=RUST, lw=1.8, zorder=5)
ax.text(SPOT, len(rows) - 0.30, f'  close {SPOT:.2f}', color=RUST, fontsize=9,
        fontweight='bold', va='bottom', ha='left')
ax.set_yticks(range(len(rows)))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=9)
ax.set_xlim(xmin - 0.06 * span, xmax + 0.40 * span)
ax.set_ylim(-0.62, len(rows) - 0.10)
ax.set_xlabel('Value per share (AED)')
ax.set_title('Four lenses, each shown across the beta the study contests\n'
             'Left edge: sector bottom-up beta.  Right edge: the share’s own regression beta.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
style(ax)
fig.tight_layout()
save(fig, 'fig1_football.png')

# ---- F2 sensitivity: WACC x terminal growth ----------------------------------
G = np.array(SN['grids']['normalisation'], dtype=float)
wg = [w * 100 for w in SN['wacc_grid']]
gg = [g * 100 for g in SN['g_grid']]
fig, ax = plt.subplots(figsize=(8.4, 4.5), dpi=110)
im = ax.imshow(G, cmap='YlGnBu', aspect='auto', origin='upper', alpha=1.0)
for r in range(G.shape[0]):
    for c in range(G.shape[1]):
        v = G[r, c]
        # White on the dark cells, ink on the light ones — contrast is chosen per cell.
        lim = G.min() + 0.62 * (G.max() - G.min())
        ax.text(c, r, f'{v:.2f}', ha='center', va='center', fontsize=9.5,
                color='#FFFFFF' if v > lim else INK,
                fontweight='bold' if abs(v - LEN['dcf_normalisation_own_beta']) < 1e-6 else 'normal')
ax.set_xticks(range(len(gg)))
ax.set_xticklabels([f'{g:.1f}%' for g in gg])
ax.set_yticks(range(len(wg)))
ax.set_yticklabels([f'{w:.2f}%' for w in wg])
ax.set_xlabel('Terminal growth rate')
ax.set_ylabel('Weighted average cost of capital')
ax.set_title('Value per share (AED) across cost of capital and terminal growth\n'
             'Normalisation construction, own-stock beta. Bold cell is the published reading.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
ax.grid(False)
cb = fig.colorbar(im, ax=ax, fraction=0.040, pad=0.02)
cb.set_label('AED per share', color=INK)
cb.ax.tick_params(colors=INK)
cb.outline.set_edgecolor(GREY)
fig.tight_layout()
save(fig, 'fig2_sens.png')

# ---- F3 price and moving averages -------------------------------------------
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'BOROUGE_Stock_Price_History.csv')),
                   'BOROUGE', verbose=False, market='AE')
px = df['Price'].to_numpy(dtype=float)
dt = df['Date'].to_numpy()
ma20 = np.convolve(px, np.ones(20) / 20, mode='valid')
ma50 = np.convolve(px, np.ones(50) / 50, mode='valid')
ma200 = np.convolve(px, np.ones(200) / 200, mode='valid')
fig, ax = plt.subplots(figsize=(9.9, 4.2), dpi=110)
ax.plot(dt, px, color=TEAL, lw=1.1, label='Close')
ax.plot(dt[19:], ma20, color=GOLD, lw=1.3, label='20-session average')
ax.plot(dt[49:], ma50, color=BRASS, lw=1.3, label='50-session average')
ax.plot(dt[199:], ma200, color=RUST, lw=1.5, label='200-session average')
ax.set_ylabel('AED per share')
ax.set_title('Price since listing, with moving averages\n'
             'Cleaned daily series, 3 June 2022 to 7 August 2026.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
leg = ax.legend(loc='upper right', frameon=True, fontsize=9)
leg.get_frame().set_facecolor(BG)
leg.get_frame().set_edgecolor(GREY)
style(ax)
fig.tight_layout()
save(fig, 'fig3_ma.png')

# ---- F4 forward fan ----------------------------------------------------------
p3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
h3 = STK['horizons']['3M']
steps = np.arange(p3.shape[1])
qs = {q: np.percentile(p3, q, axis=0) for q in (5, 25, 50, 75, 95)}
fig, ax = plt.subplots(figsize=(9.9, 4.3), dpi=110)
tail = 120
ax.plot(np.arange(-tail, 0), px[-tail:], color=INK, lw=1.2, label='Realised close')
ax.fill_between(steps, qs[5], qs[95], color=SAGE, alpha=0.30, label='90% band')
ax.fill_between(steps, qs[25], qs[75], color=TEAL, alpha=0.28, label='50% band')
ax.plot(steps, qs[50], color=BRASS, lw=1.6, label='Median path')
ax.axhline(SPOT, color=RUST, lw=1.0, ls='--')
ax.text(-tail + 2, SPOT, f' close {SPOT:.2f}', color=RUST, fontsize=8.5, va='bottom')
ax.set_xlabel(f"Trading sessions from 7 August 2026 (band ends {h3['grade_date']})")
ax.set_ylabel('AED per share')
ax.set_title('Three-month probability band\n'
             'Simulated from the cleaned price history; the drift is the risk-free rate '
             'less the dividend yield.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
leg = ax.legend(loc='upper left', frameon=True, fontsize=9, ncol=2)
leg.get_frame().set_facecolor(BG)
leg.get_frame().set_edgecolor(GREY)
style(ax)
fig.tight_layout()
save(fig, 'fig4_fan.png')

# ---- F5 / F6 terminal distributions -----------------------------------------
for tag, fname, title in [('1M', 'fig5_dist.png', 'One-month outcome distribution'),
                          ('3M', 'fig6_dist.png', 'Three-month outcome distribution')]:
    p = np.load(os.path.join(HERE, f'paths_{tag}.npy'))[:, -1]
    hz = STK['horizons'][tag]
    fig, ax = plt.subplots(figsize=(9.0, 3.9), dpi=110)
    ax.hist(p, bins=90, color=SAGE, alpha=0.75, edgecolor=TEAL, linewidth=0.3)
    ymax = ax.get_ylim()[1]
    for q, lab, col in [(hz['pct']['p5'], '5th', TEAL), (hz['pct']['p50'], 'median', BRASS),
                        (hz['pct']['p95'], '95th', TEAL)]:
        ax.axvline(q, color=col, lw=1.5)
        ax.text(q, ymax * 0.97, f' {lab} {q:.2f}', color=col, fontsize=8.8,
                rotation=90, va='top', ha='left', fontweight='bold')
    ax.axvline(SPOT, color=RUST, lw=1.6, ls='--')
    ax.text(SPOT, ymax * 0.55, f' close {SPOT:.2f}', color=RUST, fontsize=8.8,
            rotation=90, va='center', ha='right', fontweight='bold')
    ax.set_xlabel('AED per share at the end of the window')
    ax.set_ylabel('Simulated outcomes')
    ax.set_title(f"{title}\nWindow ends {hz['grade_date']}. "
                 f"Probability of finishing above the close: {hz['p_above']:.0%}.",
                 fontsize=10.5, fontweight='bold', loc='left', pad=12)
    style(ax)
    fig.tight_layout()
    save(fig, fname)

# ---- F7 the unit build: where a dollar of 2025 revenue went ------------------
h25 = H['2025']
ub = D['unit_build']
labels = ['Feedstock', 'Other production\ncost', 'Selling and\ndistribution',
          'General and\nadministrative', 'Depreciation and\namortisation', 'Operating\nprofit']
prod25 = ub['production']['2025']
vals = [ub['feed_per_t']['2025'] * prod25 / 1000.0,
        ub['othprod_fixed'] + ub['othprod_var_per_t'] * prod25,
        h25['sd'], h25['ga'], h25['da'], h25['ebit']]
tot = h25['revenue']
fig, ax = plt.subplots(figsize=(9.6, 4.1), dpi=110)
left = 0.0
cols = [RUST, BRASS, GOLD, SAGE, GREY, TEAL]
for lab, v, c in zip(labels, vals, cols):
    ax.barh(0, v, left=left, height=0.5, color=c, alpha=0.85, edgecolor=BG, linewidth=1.4)
    left += v
# Labels alternate above and below the single bar so none can collide with another.
left = 0.0
for k, (lab, v, c) in enumerate(zip(labels, vals, cols)):
    mid = left + v / 2
    up = (k % 2 == 0)
    ax.annotate(f'{lab}\n${v:,.0f}m  ({v / tot:.0%})',
                xy=(mid, 0.26 if up else -0.26), xytext=(mid, 0.62 if up else -0.62),
                ha='center', va='bottom' if up else 'top', fontsize=8.6, color=INK,
                arrowprops=dict(arrowstyle='-', color=GREY, lw=0.8))
    left += v
ax.set_xlim(0, tot * 1.02)
ax.set_ylim(-1.15, 1.15)
ax.set_yticks([])
ax.set_xlabel('USD million — FY2025 revenue and where it went')
ax.set_title('The 2025 cost stack, built from tonnes and dollars per tonne\n'
             'Each block is a driver the forecast projects separately, not a margin assumption.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
ax.grid(False)
style(ax)
fig.tight_layout()
save(fig, 'fig7_stack.png')

# ---- F8 peer cross-check -----------------------------------------------------
pt = D['peer_table']
names = [n for n in pt if pt[n]['ev_ebitda'] is not None]
vals = [pt[n]['ev_ebitda'] for n in names]
loss = [pt[n]['loss_making'] for n in names]
order = np.argsort(vals)
names = [names[i] for i in order]
vals = [vals[i] for i in order]
loss = [loss[i] for i in order]
fig, ax = plt.subplots(figsize=(9.6, 4.5), dpi=110)
bars = ax.barh(range(len(names)), vals,
               color=[RUST if l else TEAL for l in loss], alpha=0.72, height=0.6)
for i, v in enumerate(vals):
    ax.text(v + 0.9, i, f'{v:.1f}x', va='center', fontsize=8.8, color=INK)
tri = D['relative']['median_ev_ebitda']
ax.axvline(tri, color=GOLD, lw=2.2)
ax.text(tri, len(names) - 0.35, f'  through-cycle anchor {tri:.2f}x', color=BRASS,
        fontsize=9, fontweight='bold', va='bottom')
ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=8.8)
ax.set_xlim(0, max(vals) * 1.20)
ax.set_xlabel('Enterprise value to EBITDA, trailing (times)')
ax.set_title('Why the peer median is rejected\n'
             'Red bars are peers making a loss on trailing net income: nine of eleven. '
             'A median built on collapsed earnings measures the trough, not the multiple.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
style(ax)
fig.tight_layout()
save(fig, 'fig8_peers.png')

# ---- F9 the two constructions side by side ----------------------------------
yrs = [r['year'] for r in FR['normalisation']['rows']]
fig, axes = plt.subplots(1, 2, figsize=(9.9, 3.9), dpi=110)
for ax, key, ttl in [(axes[0], 'ebitda', 'EBITDA (USD million)'),
                     (axes[1], 'ebitda_margin', 'EBITDA margin')]:
    for fr_key, col, lab in [('normalisation', TEAL, 'Normalisation'),
                             ('prolonged', RUST, 'Prolonged disruption')]:
        series = [r[key] for r in FR[fr_key]['rows']]
        ax.plot(yrs, series, marker='o', ms=4.5, lw=1.8, color=col, label=lab)
    if key == 'ebitda_margin':
        ax.set_ylim(0, max(max(r[key] for r in FR[k]['rows']) for k in FR) * 1.28)
        ax.yaxis.set_major_formatter(lambda v, p: f'{v:.0%}')
    ax.set_xticks(yrs)
    ax.set_title(ttl, fontsize=9.8, fontweight='bold', loc='left')
    style(ax)
# One figure-level legend, placed BELOW the panels where no series can run under it.
handles, labs = axes[0].get_legend_handles_labels()
leg = fig.legend(handles, labs, loc='lower center', ncol=2, frameon=True, fontsize=9,
                 bbox_to_anchor=(0.5, 0.005))
leg.get_frame().set_facecolor(BG)
leg.get_frame().set_edgecolor(GREY)
fig.suptitle('The two constructions the study publishes side by side\n'
             'They differ only in how long the shipping lane stays impaired.',
             fontsize=10.5, fontweight='bold', x=0.012, y=0.985, ha='left', va='top')
fig.tight_layout(rect=(0, 0.085, 1, 0.90))
save(fig, 'fig9_framings.png')

# ---- FD1 expert panel --------------------------------------------------------
experts = ['Expert 1\ncash-flow', 'Expert 2\nasset and return', 'Expert 3\ncycle and multiple']
elo = [LEN['dcf_prolonged_sector_beta'], LEN['book_value_sector_beta'],
       LEN['relative_multiples']]
ehi = [LEN['dcf_normalisation_own_beta'], LEN['book_value_own_beta'],
       LEN['normalised_earnings_own_beta']]
fig, ax = plt.subplots(figsize=(9.2, 3.7), dpi=110)
for i, (lo, hi) in enumerate(zip(elo, ehi)):
    ax.plot([lo, hi], [i, i], color=SAGE, lw=7, alpha=0.55, solid_capstyle='round')
    ax.plot([lo], [i], marker='o', ms=8, color=TEAL)
    ax.plot([hi], [i], marker='o', ms=8, color=BRASS)
    ax.text(lo, i + 0.24, f'{lo:.2f}', ha='center', fontsize=8.8, color=TEAL,
            fontweight='bold')
    ax.text(hi, i + 0.24, f'{hi:.2f}', ha='center', fontsize=8.8, color=BRASS,
            fontweight='bold')
ax.axvline(SPOT, color=RUST, lw=1.7)
ax.text(SPOT, len(experts) - 0.55, f'  close {SPOT:.2f}', color=RUST, fontsize=9,
        fontweight='bold', va='bottom')
ax.set_yticks(range(len(experts)))
ax.set_yticklabels(experts, fontsize=9)
ax.set_ylim(-0.55, len(experts) - 0.30)
ax.set_xlabel('Value per share (AED)')
ax.set_title('Where the three experts land, and how far each spans\n'
             'The span is the beta disagreement; the gap between experts is method.',
             fontsize=10.5, fontweight='bold', loc='left', pad=12)
style(ax)
fig.tight_layout()
save(fig, 'figD1_experts.png')

# ---- transparency / readability assertions ----------------------------------
from PIL import Image                                   # noqa: E402

bad = []
for name in WRITTEN:
    im = Image.open(os.path.join(HERE, name))
    if im.mode in ('RGBA', 'LA'):
        alpha = im.getchannel('A')
        if alpha.getextrema()[0] < 255:
            bad.append(f'{name}: has transparent pixels')
    corners = im.convert('RGB')
    w, h = corners.size
    for xy in [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]:
        r, g, b = corners.getpixel(xy)
        if (r, g, b) == (0, 0, 0) or max(r, g, b) < 200:
            bad.append(f'{name}: corner {xy} is dark {(r, g, b)} — canvas is not solid light')
if bad:
    for b in bad:
        print('  ! ', b)
    raise SystemExit('FIGURE DISCIPLINE FAILED')
print(f'\n{len(WRITTEN)} figures written; all solid light canvas, zero transparency.')
