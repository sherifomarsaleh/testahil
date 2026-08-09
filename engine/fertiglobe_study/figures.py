"""Fertiglobe plc (ADX: FERTIGLB) study figures.

Every financial number on every chart is read from study_numbers.json, strike_result.json
or the simulated-path arrays. No financial numeral is typed into this file — the only
literals here are layout constants (figure sizes, font sizes, colours, offsets).

House palette, SOLID light canvas on every figure so the numbers stay readable whatever
sits behind the page, and label positions chosen so nothing overlaps a title, an axis or
another label.
"""
import json
import os
import textwrap

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- house palette ----------------------------------------------------------------
CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
TERRA, SLATE = '#A9543C', '#5B7370'
BG = '#FBF9F4'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG,
    'axes.edgecolor': GREY, 'axes.labelcolor': INK,
    'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
    'font.family': 'DejaVu Sans', 'axes.grid': True,
    'grid.color': GRID, 'grid.linewidth': 0.6,
    'axes.titlecolor': INK, 'savefig.transparent': False,
    'savefig.facecolor': BG, 'figure.dpi': 300, 'savefig.dpi': 300,
    'axes.labelsize': 8.5, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
})

DPI = 300
W = 6.5  # inches — a Word page text column
USD = r'US\$'  # escaped: an unescaped $ pair is parsed as mathtext and eats the spaces

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))

SPOT = d['spot']
CENTRAL = d['central']
SPAN = d['span']
CUR = d['meta']['listing_currency']
PS = f'{CUR} per share'
FX = d['meta']['fx']
SHARES = d['meta']['shares_mn']


def style(ax, left=True, bottom=True):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)
    if not left:
        ax.spines['left'].set_visible(False)
    if not bottom:
        ax.spines['bottom'].set_visible(False)


def save(fig, name):
    path = os.path.join(HERE, name)
    fig.savefig(path, dpi=DPI, facecolor=BG, transparent=False)
    plt.close(fig)
    print(f'  wrote {name}')


# =====================================================================================
# F1 — football field of the four lenses plus the two price-path framings
# =====================================================================================
L = d['lenses']
bA, bB = d['bridge_A'], d['bridge_B']
bA_cds, bB_cds = d['bridge_A_cds'], d['bridge_B_cds']
rel = d['rel']

# The relative lens re-computed at the lowest and the highest peer multiple, using the
# study's own bridge. Asserted against the study's published value before it is drawn.
nci_share = d['nci_share']
net_debt_rel = rel['ev'] - rel['eq_total']


def rel_ps(mult):
    ev = rel['ebitda_mid'] * mult
    eq_total = ev - net_debt_rel
    return eq_total * (1.0 - nci_share) / SHARES * FX


assert abs(rel_ps(rel['mult']) - rel['ps_aed']) < 1e-9, 'relative-lens bridge does not reproduce'
peer_mults = [p['ev_ebitda'] for p in rel['peers']]
rel_lo, rel_hi = rel_ps(min(peer_mults)), rel_ps(max(peer_mults))

rows = [
    dict(label='Cash-flow model\nweight {:.0f}%\nboth price paths'.format(L['dcf']['weight'] * 100),
         lo=bA['ps_aed'], hi=bB['ps_aed'], base=L['dcf']['value'], kind='range', col=GOLD),
    dict(label='Relative multiples\nweight {:.0f}%\npeer multiple range'.format(L['relative']['weight'] * 100),
         lo=rel_lo, hi=rel_hi, base=L['relative']['value'], kind='range', col=SAGE),
    dict(label='Normalised\nearnings power\nweight {:.0f}%'.format(L['normalized']['weight'] * 100),
         lo=None, hi=None, base=L['normalized']['value'], kind='point', col=SAGE),
    dict(label='Book value and\nsustainable return\nweight {:.0f}%'.format(L['book']['weight'] * 100),
         lo=None, hi=None, base=L['book']['value'], kind='point', col=SAGE),
    dict(label='Price path A\nmarginal-cost anchor',
         lo=min(bA['ps_aed'], bA_cds['ps_aed']), hi=max(bA['ps_aed'], bA_cds['ps_aed']),
         base=bA['ps_aed'], kind='range', col=SLATE),
    dict(label='Price path B\nstructurally tight\nmarket',
         lo=min(bB['ps_aed'], bB_cds['ps_aed']), hi=max(bB['ps_aed'], bB_cds['ps_aed']),
         base=bB['ps_aed'], kind='range', col=SLATE),
]

fig, ax = plt.subplots(figsize=(W, 4.7), dpi=DPI)
vals = [r['base'] for r in rows] + [r['lo'] for r in rows if r['lo'] is not None] \
    + [r['hi'] for r in rows if r['hi'] is not None] + [SPOT, CENTRAL] + list(SPAN)
xmin, xmax = min(vals), max(vals)
rng = xmax - xmin
x0, x1 = xmin - 0.12 * rng, xmax + 0.34 * rng

ax.axvspan(SPAN[0], SPAN[1], color=SAGE, alpha=0.13, zorder=0)
ax.axvspan(CENTRAL * 0.95, CENTRAL * 1.05, color=GOLD, alpha=0.20, zorder=1)
ax.axvline(CENTRAL, color=BRASS, lw=1.5, ls='--', zorder=3)
ax.axvline(SPOT, color=INK, lw=1.7, zorder=3)

n = len(rows)
for i, r in enumerate(rows):
    y = n - 1 - i
    if r['kind'] == 'range':
        ax.barh(y, r['hi'] - r['lo'], left=r['lo'], height=0.44, color=r['col'],
                alpha=0.45, edgecolor=r['col'], linewidth=1.1, zorder=4)
        ax.plot([r['base'], r['base']], [y - 0.22, y + 0.22], color=BRASS, lw=3.0, zorder=5)
        xt = r['hi']
        sub = f"{r['lo']:.2f}–{r['hi']:.2f}"
    else:
        ax.plot([r['base']], [y], marker='D', ms=7.0, color=BRASS,
                markeredgecolor=BRASS, zorder=5)
        xt = r['base']
        sub = None
    ax.text(xt + 0.022 * rng, y + (0.09 if sub else 0.0), f"{r['base']:.2f}", va='center',
            ha='left', fontsize=8.6, color=INK, fontweight='bold')
    if sub:
        ax.text(xt + 0.022 * rng, y - 0.24, sub, va='center', ha='left', fontsize=6.6,
                color=GREY)

ax.text(SPOT - 0.014 * rng, -0.62, f'market price {SPOT:.2f}', color=INK, fontsize=7.4,
        ha='right', va='center')
ax.text(CENTRAL + 0.016 * rng, -0.98, f'central value {CENTRAL:.2f}', color=BRASS,
        fontsize=7.4, ha='left', va='center')

ax.set_yticks(range(n))
ax.set_yticklabels([r['label'] for r in rows][::-1], fontsize=7.2, linespacing=1.30)
ax.set_xlabel(f'Fair value ({PS})')
ax.set_xlim(x0, x1)
ax.set_ylim(-1.35, n - 0.35)
ax.set_title('Fertiglobe — what each valuation method says the shares are worth\n'
             'bar = a range, diamond = a single estimate, brass tick = the method’s own figure',
             fontsize=9.0, pad=8)
ax.grid(axis='y', visible=False)
style(ax)
fig.tight_layout()
save(fig, 'fig1_football.png')

# =====================================================================================
# F2 — tornado sensitivity of the headline value
# =====================================================================================
S = d['sens']
BASE = bA['ps_aed']
gw = np.array(S['grid_wacc_g'])
gi = [j for j in range(gw.shape[1]) if abs(gw[:, j] - BASE).min() < 1e-9]
wi = [i for i in range(gw.shape[0]) if abs(gw[i, :] - BASE).min() < 1e-9]
assert len(gi) == 1 and len(wi) == 1, 'base cell not uniquely located in the two-way grid'
gj, wr = gi[0], wi[0]
assert abs(gw[wr, gj] - BASE) < 1e-9


def pct(x):
    return f'{x * 100:.1f}%'.replace('.0%', '%')


drivers = [
    ('Gas cost pass-through rate', [(pct(p), v) for p, v in zip(S['pt_grid'], S['grid_pt'])]),
    ('Product price path', [(f'{p * 100:+.0f}%', v) for p, v in zip(S['px_grid'], S['grid_px'])]),
    ('Beta', [(f'{p:.2f}', v) for p, v in zip(S['beta_grid'], S['grid_beta'])]),
    ('Terminal cost of capital', [(pct(p), v) for p, v in zip(S['wacc_grid'], gw[:, gj])]),
    ('Tax rate', [(pct(p), v) for p, v in zip(S['tax_grid'], S['grid_tax'])]),
    ('Terminal growth rate', [(pct(p), v) for p, v in zip(S['g_grid'], gw[wr, :])]),
]
tor = []
for name, pairs in drivers:
    lo_p, lo_v = pairs[0]
    hi_p, hi_v = pairs[-1]
    tor.append((name, lo_p, lo_v, hi_p, hi_v, abs(hi_v - lo_v)))
tor.sort(key=lambda t: t[-1], reverse=True)

fig, ax = plt.subplots(figsize=(W, 4.3), dpi=DPI)
allv = [v for t in tor for v in (t[2], t[4])] + [BASE]
lo_all, hi_all = min(allv), max(allv)
rng = hi_all - lo_all
ax.axvline(BASE, color=INK, lw=1.6, zorder=5)
for i, (name, lo_p, lo_v, hi_p, hi_v, _) in enumerate(tor):
    y = len(tor) - 1 - i
    for p_lab, v in ((lo_p, lo_v), (hi_p, hi_v)):
        col = GOLD if v >= BASE else SAGE
        left, width = min(BASE, v), abs(v - BASE)
        ax.barh(y, width, left=left, height=0.52, color=col, alpha=0.62,
                edgecolor=col, linewidth=0.9, zorder=3)
        outward = 0.014 * rng
        if v >= BASE:
            ax.text(v + outward, y, f'{p_lab} → {v:.2f}', va='center', ha='left',
                    fontsize=7.0, color=INK)
        else:
            ax.text(v - outward, y, f'{v:.2f} ← {p_lab}', va='center', ha='right',
                    fontsize=7.0, color=INK)
ax.set_yticks(range(len(tor)))
ax.set_yticklabels([t[0] for t in tor][::-1], fontsize=7.8)
ax.set_xlim(lo_all - 0.26 * rng, hi_all + 0.26 * rng)
ax.set_ylim(-0.95, len(tor) - 0.35)
ax.text(BASE, -0.78, f'headline value {BASE:.2f}', ha='center', va='center',
        fontsize=7.4, color=INK, zorder=9,
        bbox=dict(boxstyle='round,pad=0.22', facecolor=BG, edgecolor=GREY, linewidth=0.6))
ax.set_xlabel(f'Fair value ({PS})')
ax.set_title('Fertiglobe — how the value moves when one driver is changed\n'
             'each bar runs from that driver’s low setting to its high setting,\n'
             'with every other driver held still',
             fontsize=9.0, pad=8)
ax.grid(axis='y', visible=False)
style(ax)
fig.tight_layout()
save(fig, 'fig2_sens.png')

# =====================================================================================
# F3 — cash cost per tonne against realised price per tonne (the pass-through evidence)
# =====================================================================================
U = d['unit']
PERIODS = [('FY2024', 'FY24'), ('FY2025', 'FY25'), ('H1 2026', 'H1_26')]
px = np.array([U[k]['px_realised'] for _, k in PERIODS])
cost = np.array([U[k]['cash_cost_t'] for _, k in PERIODS])
cost_ex = np.array([U[k]['cash_cost_t_ex_accr'] for _, k in PERIODS])
CS = d['cost_stack']
f_all, f_ex = CS['passthrough'], CS['passthrough_ex_accrual']
assert abs(CS['passthru_used'] - f_all['slope']) < 1e-12

fig, ax = plt.subplots(figsize=(W, 4.35), dpi=DPI)
xlo, xhi = px.min(), px.max()
pad = 0.20 * (xhi - xlo)
xs = np.linspace(xlo - pad, xhi + pad, 100)
ax.plot(xs, f_all['slope'] * xs + f_all['intercept'], color=BRASS, lw=2.0, zorder=3,
        label='fitted line — cash cost as reported')
ax.plot(xs, f_ex['slope'] * xs + f_ex['intercept'], color=SLATE, lw=1.5, ls='--', zorder=3,
        label='fitted line — excluding the contract accrual')
ax.scatter(px, cost, s=78, color=GOLD, edgecolor=BRASS, linewidth=1.2, zorder=5,
           label='cash cost as reported')
ax.scatter(px, cost_ex, s=64, facecolor=BG, edgecolor=SLATE, linewidth=1.4, zorder=5,
           label='excluding the contract accrual')

halo = dict(boxstyle='round,pad=0.16', facecolor=BG, edgecolor='none', alpha=0.94)
xmid = 0.5 * (px.min() + px.max())
for (lab, _), xp, yp, yq in zip(PERIODS, px, cost, cost_ex):
    # labels sit on the inward side of the point so nothing runs off the plot
    side, ha = (-1, 'right') if xp > xmid else (1, 'left')
    ax.annotate(lab, (xp, yp), textcoords='offset points', xytext=(0, 12), zorder=8,
                ha='center', fontsize=7.6, color=INK, fontweight='bold', bbox=halo)
    ax.annotate(f'price {xp:,.0f}\ncost {yp:,.0f}', (xp, yp), textcoords='offset points',
                xytext=(9 * side, -7), ha=ha, va='top', fontsize=6.6, color=GREY, zorder=8,
                linespacing=1.35, bbox=halo)
    ax.annotate(f'{yq:,.0f}', (xp, yq), textcoords='offset points', xytext=(13 * side, -11),
                ha=ha, va='top', fontsize=6.6, color=SLATE, zorder=8, bbox=halo)

ylo = min(cost_ex.min(), cost.min())
yhi = max(cost.max(), (f_all['slope'] * xs + f_all['intercept']).max())
ax.set_xlim(xlo - pad, xhi + pad)
ax.set_ylim(ylo - 0.24 * (yhi - ylo), yhi + 0.30 * (yhi - ylo))

eq = (f"cash cost  =  {f_all['slope']:.3f} × price  +  {f_all['intercept']:.1f}"
      f"      R² = {f_all['r2']:.3f}   (n = {f_all['n']})")
eq2 = (f"excluding the accrual:  {f_ex['slope']:.3f} × price  +  {f_ex['intercept']:.1f}"
       f"      R² = {f_ex['r2']:.3f}")
ax.text(0.025, 0.965, eq + '\n' + eq2, transform=ax.transAxes, va='top', ha='left',
        fontsize=7.4, color=INK, linespacing=1.55,
        bbox=dict(boxstyle='round,pad=0.42', facecolor=CREAM, edgecolor=BRASS, linewidth=0.9))
ax.text(0.025, 0.735,
        f"about {f_all['slope'] * 100:.0f} cents of every extra dollar of price\n"
        f"comes back out again as cost",
        transform=ax.transAxes, va='top', ha='left', fontsize=7.2, color=BRASS,
        linespacing=1.5, style='italic')

ax.legend(frameon=False, fontsize=6.9, loc='lower right', labelcolor=INK,
          handletextpad=0.5, borderaxespad=0.6)
ax.set_xlabel(f'Realised selling price, {USD} per tonne of own-produced product')
ax.set_ylabel(f'Own-produced cash cost, {USD} per tonne')
ax.set_title('Fertiglobe — cash cost moves with the selling price\n'
             'each point is one disclosed reporting period', fontsize=9.2, pad=8)
style(ax)
fig.tight_layout()
save(fig, 'fig3_costpass.png')

# =====================================================================================
# F4 — probability range for the share price, one month and three months ahead
# =====================================================================================
QS = [5, 25, 50, 75, 95]
panels = []
for tag, fn, hkey in [('One month ahead', 'paths_1M.npy', '1M'),
                      ('Three months ahead', 'paths_3M.npy', '3M')]:
    arr = np.load(os.path.join(HERE, fn))
    bands = np.percentile(arr, QS, axis=0)
    # The saved array is a sample of the full simulation, so the terminal percentiles
    # agree with the published probability map to within a sampling tolerance.
    for i_q, key in enumerate(['p5', 'p25', 'p50', 'p75', 'p95']):
        pub = strike['horizons'][hkey]['pct'][key]
        assert abs(bands[i_q][-1] - pub) / pub < 0.01, \
            f'{hkey} {key} does not reproduce from the saved paths'
    panels.append((tag, arr, bands, strike['horizons'][hkey]))

fig, axes = plt.subplots(1, 2, figsize=(W, 3.9), dpi=DPI, sharey=True)
ylo = min(p[2][0].min() for p in panels)
yhi = max(p[2][-1].max() for p in panels)
ypad = 0.10 * (yhi - ylo)
for ax, (tag, arr, bands, hz) in zip(axes, panels):
    t = np.arange(arr.shape[1])
    ax.fill_between(t, bands[0], bands[4], color=GOLD, alpha=0.20,
                    label='5th to 95th percentile', linewidth=0)
    ax.fill_between(t, bands[1], bands[3], color=GOLD, alpha=0.45,
                    label='25th to 75th percentile', linewidth=0)
    ax.plot(t, bands[2], color=INK, lw=1.8, label='median path')
    ax.axhline(SPOT, color=GREY, lw=1.2, ls=':')
    ax.plot([0], [SPOT], marker='o', ms=4.0, color=INK, zorder=6)
    ax.set_xlim(0, t[-1] * 1.36)
    ax.set_ylim(ylo - ypad, yhi + ypad)
    halo4 = dict(boxstyle='round,pad=0.14', facecolor=BG, edgecolor='none', alpha=0.92)
    for lab, v, col, dy in [('95th', hz['pct']['p95'], BRASS, 0.020),
                            ('median', hz['pct']['p50'], INK, 0.055),
                            ('5th', hz['pct']['p5'], BRASS, -0.040)]:
        ax.text(t[-1] * 1.02, v + dy * (yhi - ylo), f'{lab} {v:.2f}', fontsize=6.8,
                color=col, va='center', ha='left', zorder=8, bbox=halo4)
    ax.text(t[-1] * 0.03, SPOT - 0.075 * (yhi - ylo), f'today {SPOT:.2f}', fontsize=6.8,
            color=GREY, ha='left', va='center', zorder=8, bbox=halo4)
    ax.set_title(f'{tag}  ·  to {hz["grade_date"]}', fontsize=8.6, pad=6)
    ax.set_xlabel('Trading days ahead')
    style(ax)
axes[0].set_ylabel(f'Share price ({PS})')
axes[0].legend(frameon=False, fontsize=6.6, loc='upper left', labelcolor=INK,
               borderaxespad=0.3, handlelength=1.6)
fig.suptitle('Fertiglobe — probability range for the share price, from simulated price paths',
             fontsize=9.4, y=0.985)
fig.tight_layout(rect=(0, 0, 1, 1.0))
save(fig, 'fig4_fan.png')

# =====================================================================================
# F5 — distribution of the share price three months ahead
# =====================================================================================
arr3 = np.load(os.path.join(HERE, 'paths_3M.npy'))[:, -1]
pc = strike['horizons']['3M']['pct']
fig, ax = plt.subplots(figsize=(W, 3.8), dpi=DPI)
lo_x, hi_x = np.percentile(arr3, 0.3), np.percentile(arr3, 99.7)
counts, bins, _ = ax.hist(arr3, bins=90, range=(lo_x, hi_x), color=GOLD, alpha=0.92,
                          edgecolor='#FFFFFF', linewidth=0.25, zorder=3)
ymax = counts.max()
ax.fill_between([pc['p25'], pc['p75']], 0, ymax * 1.02, color=BRASS, alpha=0.10, zorder=2)
halo5 = dict(boxstyle='round,pad=0.15', facecolor=BG, edgecolor='none', alpha=0.94)
xw = hi_x - lo_x
marks = [('5th', pc['p5'], 0.60, 'center', 0.0), ('25th', pc['p25'], 0.80, 'center', 0.0),
         ('median', pc['p50'], 1.02, 'right', -0.006 * xw),
         ('75th', pc['p75'], 0.80, 'center', 0.0), ('95th', pc['p95'], 0.60, 'center', 0.0)]
for lab, v, hfrac, ha_, dx in marks:
    ax.plot([v, v], [0, ymax * hfrac], color=BRASS, lw=1.4, ls='--', zorder=5)
    ax.text(v + dx, ymax * hfrac + ymax * 0.035, f'{lab}\n{v:.2f}', ha=ha_, va='bottom',
            fontsize=6.9, color=BRASS, linespacing=1.25, zorder=8, bbox=halo5)
ax.axvline(SPOT, color=INK, lw=1.8, zorder=6)
ax.text(SPOT + 0.006 * xw, ymax * 1.27, f'today\n{SPOT:.2f}', ha='left', va='bottom',
        fontsize=7.0, color=INK, linespacing=1.25, zorder=8, bbox=halo5)
ax.set_xlim(lo_x, hi_x)
ax.set_ylim(0, ymax * 1.60)
ax.set_yticks([])
ax.set_xlabel(f'Share price three months ahead ({PS})')
ax.set_ylabel('Share of simulated outcomes')
ax.set_title(f'Fertiglobe — where the share price could be on '
             f'{strike["horizons"]["3M"]["grade_date"]}\n'
             f'simulated outcomes, with the middle half shaded', fontsize=9.2, pad=8)
ax.grid(axis='x', visible=False)
style(ax, left=False)
fig.tight_layout()
save(fig, 'fig5_dist.png')

# =====================================================================================
# F6 — revenue and EBITDA by segment, history and forecast under framing A
# =====================================================================================
I = d['inputs']
FA = d['frame_A']
hist_years = ['2023', '2024', '2025']
fc_years = [f'{y}E' for y in FA['years']]
years = hist_years + fc_years

rev_own = [None, I['seg_own_rev_fy24']['value'], I['seg_own_rev_fy25']['value']] + FA['rev_own']
rev_3p = [None, I['seg_3p_rev_fy24']['value'], I['seg_3p_rev_fy25']['value']] + FA['rev_3p']
rev_tot = [d['hist_is']['FY23']['rev'], d['hist_is']['FY24']['rev'],
           d['hist_is']['FY25']['rev']] + FA['rev']
assert abs(rev_own[1] + rev_3p[1] - rev_tot[1]) < 1e-6

eb_own = [None, I['seg_own_ebitda_fy24']['value'], I['seg_own_ebitda_fy25']['value']] + FA['ebitda_own']
eb_3p = [None, I['seg_3p_ebitda_fy24']['value'], I['seg_3p_ebitda_fy25']['value']] + FA['ebitda_3p']
eb_corp = [None, I['seg_oth_ebitda_fy24']['value'], I['seg_oth_ebitda_fy25']['value']] \
    + [t - o - p for t, o, p in zip(FA['ebitda'], FA['ebitda_own'], FA['ebitda_3p'])]
eb_tot = [d['hist_is']['FY23']['ebitda'], d['hist_is']['FY24']['ebitda'],
          d['hist_is']['FY25']['ebitda']] + FA['ebitda']

xs = np.arange(len(years))
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(W, 5.5), dpi=DPI)
bw = 0.62

for ax, own, thp, corp, tot, ylab, ttl in [
    (ax1, rev_own, rev_3p, None, rev_tot, f'Revenue ({USD} million)',
     'Revenue by segment — the figure above each bar is the group total'),
    (ax2, eb_own, eb_3p, eb_corp, eb_tot, f'EBITDA ({USD} million)',
     'EBITDA by segment — the figure above each bar is the group total'),
]:
    for i, yr in enumerate(years):
        if own[i] is None:
            ax.bar(i, tot[i], width=bw, color=GREY, alpha=0.35, edgecolor=GREY,
                   linewidth=0.8, hatch='//', zorder=3)
            continue
        ax.bar(i, own[i], width=bw, color=GOLD, alpha=0.90, edgecolor='#FFFFFF',
               linewidth=0.6, zorder=3)
        ax.bar(i, thp[i], width=bw, bottom=own[i], color=SAGE, alpha=0.95,
               edgecolor='#FFFFFF', linewidth=0.6, zorder=3)
        if corp is not None:
            ax.bar(i, corp[i], width=bw, color=TERRA, alpha=0.85, edgecolor='#FFFFFF',
                   linewidth=0.6, zorder=3)
    tops = [max(t, (own[i] or 0) + (thp[i] or 0)) for i, t in enumerate(tot)]
    hi = max(tops)
    lo = min([0] + [c for c in (corp or []) if c is not None])
    for i, t in enumerate(tot):
        ax.text(i, tops[i] + 0.035 * (hi - lo), f'{t:,.0f}', ha='center', va='bottom',
                fontsize=6.9, color=INK)
    ax.axvline(len(hist_years) - 0.5, color=GREY, lw=0.9, ls=':', zorder=2)
    ax.set_xticks(xs)
    ax.set_xticklabels(years, fontsize=7.6)
    ax.set_ylabel(ylab)
    ax.set_ylim(lo - 0.10 * (hi - lo), hi + 0.19 * (hi - lo))
    ax.set_xlim(-0.62, len(years) - 0.38)
    if lo < 0:
        ax.axhline(0, color=GREY, lw=0.8)
    ax.set_title(ttl, fontsize=8.2, pad=5, loc='left')
    ax.grid(axis='x', visible=False)
    style(ax)

ax1.text(len(hist_years) - 0.42, ax1.get_ylim()[1] * 0.985, 'forecast', fontsize=6.8,
         color=GREY, va='top', ha='left', style='italic')
ax1.text(len(hist_years) - 0.58, ax1.get_ylim()[1] * 0.985, 'reported', fontsize=6.8,
         color=GREY, va='top', ha='right', style='italic')

handles = [
    Rectangle((0, 0), 1, 1, color=GOLD, alpha=0.90),
    Rectangle((0, 0), 1, 1, color=SAGE, alpha=0.95),
    Rectangle((0, 0), 1, 1, color=TERRA, alpha=0.85),
    Rectangle((0, 0), 1, 1, color=GREY, alpha=0.35, hatch='//'),
]
labels = ['Own-produced production and marketing', 'Third-party trading',
          'Corporate and other', 'Group total (segment split not disclosed for 2023)']
fig.legend(handles, labels, frameon=False, fontsize=7.0, ncol=2, loc='lower center',
           labelcolor=INK, bbox_to_anchor=(0.5, -0.005), columnspacing=1.6)
fig.suptitle('Fertiglobe — revenue and EBITDA by segment, reported and forecast\n'
             f'forecast on price path A ({FA["label"].split("—")[-1].strip()})',
             fontsize=9.4, y=0.997, va='top')
fig.tight_layout(rect=(0, 0.075, 1, 1.0))
save(fig, 'fig6_segments.png')

# =====================================================================================
# F7 — the discounted cash-flow bridge from cash flows to equity value
# =====================================================================================
DA = d['dcf_A']
DB, BB = d['dcf_B'], d['bridge_B']
steps = [
    ('Present value\nof free cash\nflow 2026–2030', DA['pv_explicit'], 'up'),
    ('Present value\nof the terminal\nvalue', DA['pv_tv'], 'up'),
    ('Enterprise\nvalue', bA['ev'], 'total'),
    ('Less\nnet debt', -bA['net_debt'], 'down'),
    ('Less non-\ncontrolling\ninterests', -bA['nci_used'], 'down'),
    ('Equity\nattributable\nto owners', bA['eq_attr'], 'total'),
]
assert abs(DA['pv_explicit'] + DA['pv_tv'] - bA['ev']) < 1e-6
assert abs(bA['ev'] - bA['net_debt'] - bA['nci_used'] - bA['eq_attr']) < 1e-6

fig, ax = plt.subplots(figsize=(W, 4.6), dpi=DPI)
run = 0.0
tops = []
for i, (lab, val, kind) in enumerate(steps):
    if kind == 'total':
        bottom, height = 0.0, val
        col, alp = BRASS, 0.80
        run = val
    else:
        bottom = run if val >= 0 else run + val
        height = abs(val)
        col, alp = (GOLD, 0.85) if val >= 0 else (SAGE, 0.85)
        run = run + val
    ax.bar(i, height, bottom=bottom, width=0.60, color=col, alpha=alp,
           edgecolor='#FFFFFF', linewidth=0.7, zorder=3)
    tops.append(bottom + height)
    ax.text(i, bottom + height + 0.028 * bA['ev'], f'{abs(val):,.0f}', ha='center',
            va='bottom', fontsize=7.4, color=INK, fontweight='bold')

for i in range(len(steps) - 1):
    if steps[i][2] != 'total' and steps[i + 1][2] != 'total':
        y = tops[i]
    else:
        y = tops[i]
    ax.plot([i + 0.30, i + 0.70], [y, y], color=GREY, lw=0.8, ls=':', zorder=2)

ax.set_xticks(range(len(steps)))
ax.set_xticklabels([s[0] for s in steps], fontsize=6.5, linespacing=1.32)
ax.set_ylabel(f'{USD} million')
ax.set_ylim(0, bA['ev'] * 1.30)
ax.set_xlim(-0.62, len(steps) - 0.38)
# The terminal-value share sits in the empty band above the first bar, clear of every
# bar top and of every value label.
ax.text(-0.50, bA['ev'] * 1.16,
        f'terminal value is {DA["tv_share"] * 100:.0f}% of enterprise value',
        fontsize=7.4, color=BRASS, ha='left', va='center', zorder=8,
        bbox=dict(boxstyle='round,pad=0.28', facecolor=CREAM, edgecolor=BRASS,
                  linewidth=0.8))
ax.text(len(steps) - 1, bA['eq_attr'] * 0.50,
        f'{bA["ps_aed"]:.2f}\n{CUR} per share', ha='center', va='center', fontsize=7.4,
        color=INK, linespacing=1.35, zorder=8,
        bbox=dict(boxstyle='round,pad=0.28', facecolor=BG, edgecolor=BRASS, linewidth=0.8))
ax.set_title('Fertiglobe — from discounted cash flows to the value of the shares\n'
             f'price path A ({FA["label"].split("—")[-1].strip()})', fontsize=9.2, pad=8)
ax.grid(axis='x', visible=False)
style(ax)
fig.tight_layout(rect=(0, 0.155, 1, 1))
foot = (f'On price path B the same bridge gives an enterprise value of '
        f'{USD}{DB["ev"]:,.0f} million and equity attributable to owners of '
        f'{USD}{BB["eq_attr"]:,.0f} million, or {BB["ps_aed"]:.2f} {CUR} per share, '
        f'with the terminal value {DB["tv_share"] * 100:.0f}% of enterprise value.')
fig.text(0.035, 0.125, textwrap.fill(foot, 104), fontsize=6.9, color=GREY, va='top',
         ha='left', linespacing=1.55)
save(fig, 'fig7_waterfall.png')

# =====================================================================================
# FD1 — the three expert valuations
# =====================================================================================
E = d['experts']
ex = [(f'Expert {i}', E[k]['method'], E[k]['ps_aed']) for i, k in enumerate(['e1', 'e2', 'e3'], 1)]
vals = [v for _, _, v in ex]
spread = max(vals) - min(vals)

fig, ax = plt.subplots(figsize=(W, 3.5), dpi=DPI)
xhi = max(max(vals), SPOT) * 1.30
for i, (nm, meth, v) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, v, height=0.48, color=SAGE, alpha=0.55, edgecolor=SLATE, linewidth=1.0,
            zorder=3)
    ax.text(v + 0.012 * xhi, y, f'{v:.2f}', va='center', ha='left', fontsize=8.4,
            color=INK, fontweight='bold')
ax.axvspan(min(vals), max(vals), color=GOLD, alpha=0.16, zorder=1)
ax.axvline(SPOT, color=INK, lw=1.7, zorder=5)
ax.text(SPOT + 0.008 * xhi, len(ex) - 0.52, f'market price {SPOT:.2f}', fontsize=7.2,
        color=INK, ha='left', va='center', rotation=0)

ax.annotate('', xy=(min(vals), -0.62), xytext=(max(vals), -0.62),
            arrowprops=dict(arrowstyle='<->', color=BRASS, lw=1.1))
ax.text((min(vals) + max(vals)) / 2, -0.80,
        f'spread between the three: {spread:.2f} {CUR} per share '
        f'({spread / min(vals) * 100:.0f}% of the lowest)',
        ha='center', va='center', fontsize=7.2, color=BRASS)

ylabs = []
for nm, meth, _ in ex:
    ylabs.append(nm + '\n' + '\n'.join(textwrap.wrap(meth, 26)))
ax.set_yticks(range(len(ex)))
ax.set_yticklabels(ylabs[::-1], fontsize=7.0, linespacing=1.30)
ax.set_xlim(0, xhi)
ax.set_ylim(-1.05, len(ex) - 0.38)
ax.set_xlabel(f'Fair value ({PS})')
ax.set_title('Fertiglobe — three independent valuations, three different methods',
             fontsize=9.2, pad=8)
ax.grid(axis='y', visible=False)
style(ax)
fig.tight_layout()
save(fig, 'figD1_experts.png')

print('figures done')
