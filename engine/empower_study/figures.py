"""EMPOWER study figures.

House palette on a SOLID LIGHT canvas (#f8f9fb) so every number stays readable when the
page behind the figure is dark. ZERO transparency anywhere: shades are pre-blended into
the canvas colour instead of drawn with alpha, and every figure asserts (figure patch +
every axes patch alpha == 1.0) before it is written. Label positions are chosen so
nothing overlaps a title, an axis, a bar or another label; every axis carries units.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, to_rgb
from primitives import load_ohlc
from data_quality import clean_ohlc

BG = '#f8f9fb'
CANVAS = '#1C3A36'   # dark teal ink / primary line
GOLD, BRASS, SAGE = '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY, RUST = '#1C3A36', '#D9DEE4', '#5A6764', '#A0522D'


def mix(c, f, bg=BG):
    """Blend colour c into the canvas at fraction f — a solid stand-in for alpha."""
    r1, g1, b1 = to_rgb(c); r2, g2, b2 = to_rgb(bg)
    return (r1 * f + r2 * (1 - f), g1 * f + g2 * (1 - f), b1 * f + b2 * (1 - f))


def bbox():
    """Solid canvas-coloured box behind a label so a line under it reads as
    interrupted, never as a strikethrough. Solid — no alpha."""
    return dict(facecolor=BG, edgecolor='none', boxstyle='square,pad=0.15')


SAGE_L = mix(SAGE, 0.42)
GOLD_L = mix(GOLD, 0.45)
GOLD_XL = mix(GOLD, 0.18)
TEAL_L = mix(CANVAS, 0.35)
RUST_L = mix(RUST, 0.30)

plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG, 'font.size': 9.5})

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
SPOT = D['meta']['spot']
TECH = json.load(open(os.path.join(HERE, 'tech_read.json')))
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'EMPOWER_Stock_Price_History.csv')),
                   'EMPOWER', verbose=False, market='AE')


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    # ZERO-transparency gate: figure patch and every axes patch fully opaque.
    assert fig.patch.get_facecolor()[3] == 1.0, f'{name}: figure facecolor not opaque'
    for ax_ in fig.get_axes():
        assert ax_.patch.get_facecolor()[3] == 1.0, f'{name}: axes facecolor not opaque'
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, name), dpi=200, facecolor=BG)
    plt.close(fig)
    print('wrote', name)


# ---- F1 football field -------------------------------------------------------
dcf_ct, dcf_dmtt = D['lenses']['dcf']['ps'], D['lenses']['dcf']['ps_dmtt']
rel_ev, rel_pe = D['rel']['ps_rel'], D['rel']['ps_pe']
norm_ps, book_ps = D['norm']['ps'], D['book']['ps']
ddm_ps = D['ddm']['ps']
bear, bull = D['central']['bear'], D['central']['bull']
dewa = D['dewa_buyin']['price']

rows = [  # (label, lo, hi, right-hand text) — top to bottom
    ('Discounted cash flow\n(FCFF, five-year)', dcf_dmtt, dcf_ct,
     f'{dcf_dmtt:.2f} (15% DMTT) – {dcf_ct:.2f} (9% CT)'),
    ('Relative multiples\n(EV/EBITDA → P/E)', rel_ev, rel_pe,
     f'{rel_ev:.2f} (EV/EBITDA) – {rel_pe:.2f} (P/E)'),
    ('Normalised earnings\npower', norm_ps, norm_ps, f'{norm_ps:.2f}'),
    ('Book value &\nsustainable return', book_ps, book_ps, f'{book_ps:.2f}'),
    ('Dividend discount\n(AED 875m policy)', ddm_ps, ddm_ps, f'{ddm_ps:.2f}'),
]
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=110)
n = len(rows)
ax.axvspan(bear, bull, color=GOLD_XL, zorder=0)
for i, (lab, lo, hi, txt) in enumerate(rows):
    y = n - 1 - i
    if hi > lo:
        ax.barh(y, hi - lo, left=lo, height=0.46, color=SAGE_L,
                edgecolor=SAGE, linewidth=1.2, zorder=3)
        if i == 0:  # DCF: the 15% DMTT framing as a paired darker segment on the same bar
            ax.barh(y - 0.12, hi - lo, left=lo, height=0.17, color=mix(BRASS, 0.75),
                    edgecolor=BRASS, linewidth=0.8, zorder=4)
        ax.plot([lo, lo], [y - 0.24, y + 0.24], color=BRASS, lw=3.2, zorder=5)
        ax.plot([hi, hi], [y - 0.24, y + 0.24], color=BRASS, lw=3.2, zorder=5)
    else:  # single-value lens: a slim bar so it still reads as a bar, plus the tick
        ax.barh(y, 0.05, left=lo - 0.025, height=0.46, color=SAGE_L,
                edgecolor=SAGE, linewidth=1.2, zorder=3)
        ax.plot([lo, lo], [y - 0.24, y + 0.24], color=BRASS, lw=3.6, zorder=5)
    ax.text(3.02, y, txt, va='center', ha='left', fontsize=9, color=INK)
ax.text((bear + bull) / 2, -0.52, f'scenario field: bear {bear:.2f} → bull {bull:.2f}',
        fontsize=9, color=BRASS, ha='center', va='center', bbox=bbox(), zorder=7)
ax.axvline(SPOT, color=RUST, lw=2.4, zorder=6)
ax.text(SPOT - 0.02, n - 0.30, f'spot {SPOT:.2f}  ', color=RUST, fontsize=9.5,
        fontweight='bold', va='bottom', ha='right')
ax.axvline(dewa, color=GREY, lw=1.4, ls='--', zorder=6)
ax.text(dewa + 0.02, n - 0.30, ' DEWA control transaction Feb-2026 — 2.16',
        color=GREY, fontsize=9, va='bottom', ha='left')
ax.set_yticks(range(n))
ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=9)
ax.set_xlim(1.30, 3.95)
ax.set_ylim(-0.80, n - 0.05)
ax.set_xlabel('Value per share (AED)')
ax.set_title('Valuation by lens, against the market price', fontsize=11.5,
             fontweight='bold', loc='left', pad=12)
ax.grid(axis='y', visible=False)
style(ax)
save(fig, 'fig1_football.png')

# ---- F2 sensitivity heat grid ------------------------------------------------
SN = D['sens_wg']
G = np.array(SN['table'])  # rows = WACC (ascending), cols = terminal growth (ascending)
fig, ax = plt.subplots(figsize=(8.6, 4.3), dpi=110)
cmap = plt.get_cmap('RdYlGn')
# Diverging palette centred at the spot price: green above 1.50, red below.
norm = TwoSlopeNorm(vmin=2 * SPOT - G.max(), vcenter=SPOT, vmax=G.max())
ax.imshow(G, cmap=cmap, norm=norm, aspect='auto')
ax.set_xticks(range(len(SN['g_grid'])))
ax.set_xticklabels([f'{g:.1%}' for g in SN['g_grid']], fontsize=9.5)
ax.set_yticks(range(len(SN['wacc_grid'])))
ax.set_yticklabels([f'{w:.2%}' for w in SN['wacc_grid']], fontsize=9.5)
ax.set_xlabel('Terminal growth')
ax.set_ylabel('WACC')
# Text colour from each cell's OWN relative luminance, not a guessed value cutoff.
for i in range(G.shape[0]):
    for j in range(G.shape[1]):
        r, g_, b, _ = cmap(norm(G[i, j]))
        lum = 0.2126 * r + 0.7152 * g_ + 0.0722 * b
        ax.text(j, i, f'{G[i, j]:.2f}', ha='center', va='center', fontsize=9.5,
                color=('#FFFFFF' if lum < 0.55 else '#12211F'), fontweight='bold')
ax.set_title('Fair value per share (AED) by WACC and terminal growth\n'
             f'(diverging scale centred at the {SPOT:.2f} spot — every cell sits above it)',
             fontsize=10.5, fontweight='bold', loc='left', pad=10)
ax.grid(False)
save(fig, 'fig2_sens.png')

# ---- F3 price and moving averages -------------------------------------------
ma = {w: df['Price'].rolling(w).mean() for w in (20, 50, 200)}
cut = df['Date'].max() - np.timedelta64(548, 'D')  # last 18 months
m3 = df['Date'] >= cut
d3 = df[m3]
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=110)
ax.plot(d3['Date'], d3['Price'], color=CANVAS, lw=1.5, label='Close', zorder=4)
for win, col in ((20, RUST_L), (50, GOLD), (200, SAGE)):
    ax.plot(df['Date'][m3], ma[win][m3], color=col, lw=1.6, label=f'{win}-day average',
            zorder=3)
x0, x1 = d3['Date'].iloc[0], d3['Date'].iloc[-1]
xr = x1 + (x1 - x0) * 0.012
for lv in TECH['levels']['res']:
    ax.axhline(lv, color=BRASS, lw=1.0, ls='--', zorder=2)
    ax.text(xr, lv, f'R {lv:.2f}', color=BRASS, fontsize=9, va='center', ha='left',
            bbox=bbox(), zorder=6)
for lv in TECH['levels']['sup']:
    ax.axhline(lv, color=GREY, lw=1.0, ls='--', zorder=2)
    ax.text(xr, lv, f'S {lv:.2f}', color=GREY, fontsize=9, va='center', ha='left',
            bbox=bbox(), zorder=6)
hi52, lo52 = TECH['hi_52w'], TECH['lo_52w']
hi_dt = d3['Date'][d3['Price'].idxmax()]
ax.annotate(f'52w high {hi52:.2f}', (hi_dt, hi52), xytext=(0, 10),
            textcoords='offset points', ha='center', fontsize=9, color=INK,
            fontweight='bold', bbox=bbox(), zorder=6)
lo_idx = d3['Price'].idxmin()
ax.annotate(f'52w low {lo52:.2f}', (d3['Date'][lo_idx], d3['Price'][lo_idx]),
            xytext=(-64, -18), textcoords='offset points', ha='center', fontsize=9,
            color=INK, fontweight='bold', bbox=bbox(), zorder=6)
ax.plot([x1], [SPOT], marker='o', ms=6, color=RUST, zorder=6)
ax.annotate(f'close {SPOT:.2f}', (x1, SPOT), xytext=(-8, -20),
            textcoords='offset points', ha='right', fontsize=9.5, color=RUST,
            fontweight='bold', bbox=bbox(), zorder=6)
ax.set_ylabel('AED per share')
ax.set_ylim(1.22, 2.10)
ax.set_xlim(x0, x1 + (x1 - x0) * 0.085)
ax.set_title('Eighteen months of price, moving averages, and the support/resistance ladder',
             fontsize=11.5, fontweight='bold', loc='left', pad=12)
ax.legend(frameon=False, loc='upper right', fontsize=9, ncol=2)
style(ax)
save(fig, 'fig3_ma.png')

# ---- F4 three-month fan ------------------------------------------------------
paths = np.load(os.path.join(HERE, 'paths_3M.npy'))  # (20000, 1 + 63): col 0 = anchor
h = paths.shape[1] - 1
qs = [5, 25, 50, 75, 95]
Q = np.percentile(paths, qs, axis=0)
x = np.arange(0, h + 1)
hist = df['Price'].values[-61:]           # ~60 sessions of trailing history
xh = np.arange(-len(hist) + 1, 1)
pct3 = D['strike']['horizons']['3M']['pct']
fig, ax = plt.subplots(figsize=(9.8, 4.4), dpi=110)
ax.fill_between(x, Q[0], Q[4], color=SAGE_L, label='5th–95th percentile', zorder=2)
ax.fill_between(x, Q[1], Q[3], color=GOLD_L, label='25th–75th percentile', zorder=3)
ax.plot(x, Q[2], color=CANVAS, lw=2.0, label='Median', zorder=5)
ax.plot(xh, hist, color=GREY, lw=1.4, zorder=4)
ax.axvline(0, color=GREY, lw=0.8, ls=':', zorder=1)
ax.plot([0], [SPOT], marker='o', ms=5, color=RUST, zorder=6)
ax.text(-1, SPOT + 0.03, f'spot {SPOT:.2f}', color=RUST, fontsize=9.5,
        fontweight='bold', ha='right', va='bottom')
for lab, yv in (('p5', pct3['p5']), ('p50', pct3['p50']), ('p95', pct3['p95'])):
    ax.text(h + 1.2, yv, f'{lab} {yv:.2f}', fontsize=9, color=INK, va='center')
ax.set_xlim(xh[0], h + 9)
ax.set_xlabel('Trading sessions (history ← 0 → forecast)')
ax.set_ylabel('AED per share')
ax.set_title('Three-month price cone from the anchor close, with the trailing tape',
             fontsize=11.5, fontweight='bold', loc='left', pad=12)
ax.legend(frameon=False, loc='upper left', fontsize=9)
style(ax)
save(fig, 'fig4_fan.png')

# ---- F5/F6 terminal distributions --------------------------------------------
for tag, fname, word in (('1M', 'fig5_dist.png', 'One-month'),
                         ('3M', 'fig6_dist.png', 'Three-month')):
    p = np.load(os.path.join(HERE, f'paths_{tag}.npy'))[:, -1]
    pct = D['strike']['horizons'][tag]['pct']
    fig, ax = plt.subplots(figsize=(8.6, 3.7), dpi=110)
    ax.hist(p, bins=90, range=(np.percentile(p, 0.5), np.percentile(p, 99.5)),
            color=SAGE_L, edgecolor='none', zorder=2)
    ymax = ax.get_ylim()[1]
    for q, col, lab in ((pct['p5'], GREY, 'p5'), (pct['p25'], GREY, 'p25'),
                        (pct['p50'], CANVAS, 'p50'), (pct['p75'], GREY, 'p75'),
                        (pct['p95'], GREY, 'p95')):
        ax.axvline(q, color=col, lw=1.7 if lab == 'p50' else 1.1,
                   ls='-' if lab == 'p50' else '--', zorder=3)
        ax.text(q, ymax * 0.97, f'{lab} {q:.2f}', fontsize=9, color=INK,
                rotation=90, va='top', ha='center', bbox=bbox(), zorder=5)
    # Spot label sits at mid-height so it cannot collide with the percentile labels
    # above it (the 1M median lands within 0.003 of spot).
    ax.axvline(SPOT, color=RUST, lw=1.5, zorder=4)
    ax.text(SPOT, ymax * 0.42, f'spot {SPOT:.2f}', fontsize=9, color=RUST,
            rotation=90, va='center', ha='center', fontweight='bold', bbox=bbox(),
            zorder=5)
    ax.set_xlabel('AED per share')
    ax.set_ylabel('Simulated paths')
    ax.set_title(f'{word} outcome distribution at the {tag} check date',
                 fontsize=11, fontweight='bold', loc='left', pad=10)
    style(ax)
    save(fig, fname)

# ---- F7 EV -> equity waterfall -----------------------------------------------
B = D['dcf']['base_ct']
pv_exp, pv_tv, ev = B['pv_explicit'], B['pv_tv'], B['ev']
nd = D['wacc']['net_debt']
side = (D['inputs']['invprop_jun26']['value'] + D['inputs']['fvtpl_jun26']['value']
        + D['inputs']['fvoci_jun26']['value'])
recv = D['inputs']['recv_jun26']['value']
nci, eq, ps = B['nci_val'], B['eq_attr'], B['ps']
assert abs(ev - nd + recv + side - nci - eq) < 1.0
steps = [  # (label, base, height, colour, printed value)
    ('PV explicit\nFCFF FY26–30', 0, pv_exp, SAGE_L, pv_exp),
    ('PV terminal\nvalue', pv_exp, pv_tv, GOLD_L, pv_tv),
    ('Enterprise\nvalue', 0, ev, TEAL_L, ev),
    ('Net debt\n(Jun-26)', ev - nd, nd, RUST_L, -nd),
    ('Concession-grantor\nreceivables at book', ev - nd, recv, SAGE_L, recv),
    ('Inv. property\n+ FVTPL/FVOCI', ev - nd + recv, side, SAGE_L, side),
    ('Non-controlling\ninterests', ev - nd + recv + side - nci, nci, RUST_L, -nci),
    ('Equity attributable\nto holders', 0, eq, TEAL_L, eq),
]
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=110)
for i, (lab, b, hgt, col, val) in enumerate(steps):
    ax.bar(i, hgt, bottom=b, color=col, width=0.62,
           edgecolor=GREY, linewidth=0.8, zorder=3)
    top = b + hgt
    if i < len(steps) - 1:  # connector to the next bar
        nb = steps[i + 1][1] + (0 if steps[i + 1][4] >= 0 else steps[i + 1][2])
        ax.plot([i + 0.31, i + 1 - 0.31], [nb, nb], color=GREY, lw=0.9,
                ls=':', zorder=2)
    ax.text(i, top + 550, f'{val:+,.0f}' if i not in (2, 6) else f'{val:,.0f}',
            ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=INK)
ax.text(1, pv_exp + pv_tv * 0.45, f'terminal value\n= {B["tv_share"]:.1%} of EV',
        ha='center', va='center', fontsize=9.5, color=INK)
ax.text(6, eq * 0.45, f'= AED {ps:.3f}\nper share', ha='center', va='center',
        fontsize=10, fontweight='bold', color=INK)
ax.set_xticks(range(len(steps)))
ax.set_xticklabels([s[0] for s in steps], fontsize=9)
ax.set_ylabel('AED million')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:,.0f}'))
ax.set_ylim(0, ev * 1.13)
ax.set_title('From discounted cash flows to value per share — base case, 9% corporate tax',
             fontsize=11.5, fontweight='bold', loc='left', pad=12)
ax.grid(axis='x', visible=False)
style(ax)
save(fig, 'fig7_bridge.png')

# ---- F8 the unit build -------------------------------------------------------
U = D['unit']
rt_hist = D['inputs']['rt_conn']['value']       # {'2021':..,'2022':..,'2024':..,'2025':..}
rt_fcst = U['rt_path']                          # FY25..FY30
contracted = D['inputs']['rt_contracted']['value']
fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.6, 4.4), dpi=110)

years_h = ['FY2021', 'FY2022', 'FY2023', 'FY2024', 'FY2025']
vals_h = [rt_hist['2021'], rt_hist['2022'], None, rt_hist['2024'], rt_hist['2025']]
years_f = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
vals_f = [rt_fcst[k] for k in ('FY26', 'FY27', 'FY28', 'FY29', 'FY30')]
xs = np.arange(len(years_h) + len(years_f))
for i, v in enumerate(vals_h):
    if v is None:
        axL.text(i, 40, 'not\ndisclosed', ha='center', va='bottom', fontsize=9,
                 color=GREY)
        continue
    axL.bar(i, v, color=CANVAS, width=0.66, zorder=3)
    axL.text(i, v + 28, f'{v:,.0f}', ha='center', fontsize=9, color=INK)
for j, v in enumerate(vals_f):
    i = len(years_h) + j
    axL.bar(i, v, color=TEAL_L, width=0.66, zorder=3)
    axL.text(i, v + 28, f'{v:,.0f}', ha='center', fontsize=9, color=INK)
axL.axhline(contracted, color=BRASS, lw=1.5, ls='--', zorder=4)
axL.text(0.1, contracted + 30, f'contracted {contracted:,.0f}k RT (Jun-2026)',
         fontsize=9, color=BRASS, ha='left', va='bottom')
axL.set_xticks(xs)
axL.set_xticklabels(years_h + years_f, fontsize=9, rotation=45, ha='right')
axL.set_ylabel('Connected capacity (thousand RT)')
axL.set_ylim(0, 2350)
axL.set_title('Connected refrigeration tons — history and build-out path',
              fontsize=10.5, fontweight='bold', loc='left', pad=10)
axL.grid(axis='x', visible=False)
style(axL)

# Right panel: consumption revenue per average connected RT (AED thousand per RT).
# Actuals are computable on the model's average-RT basis only for FY2022 and FY2025 —
# the 2023 connected figure is not disclosed, so FY2023/FY2024 are shown as a gap,
# never interpolated.
a22 = D['inputs']['cons_rev']['value']['2022'] / ((rt_hist['2021'] + rt_hist['2022']) / 2)
a25 = U['cons25'] / ((rt_hist['2024'] + rt_hist['2025']) / 2)
fy = ['FY26', 'FY27', 'FY28', 'FY29', 'FY30']
base_prt = [D['fcst']['base']['cons'][y] / U['rt_avg'][y] for y in fy]
pers_cons = [D['fcst']['base']['cons'][y]
             - (D['fcst']['base']['rev'][y] - D['fcst']['persist']['rev'][y]) for y in fy]
pers_prt = [c / U['rt_avg'][y] for c, y in zip(pers_cons, fy)]
xa = {'FY2022': 0, 'FY2025': 3}
xf = np.arange(4, 9)
axR.plot([xa['FY2022'], xa['FY2025']], [a22, a25], color=GREY, lw=1.0, ls=':', zorder=2)
axR.plot([0], [a22], marker='o', ms=7, color=CANVAS, zorder=4)
axR.plot([3], [a25], marker='o', ms=7, color=CANVAS, zorder=4)
axR.text(0, a22 + 0.008, f'{a22:.2f}', ha='center', fontsize=9, color=INK)
axR.text(3, a25 + 0.008, f'{a25:.2f}', ha='center', fontsize=9, color=INK)
axR.text(1.5, (a22 + a25) / 2 - 0.020,
         'FY23–FY24 not shown:\n2023 connected RT\nnot disclosed', ha='center',
         fontsize=9, color=GREY)
axR.plot(np.r_[3, xf], np.r_[a25, base_prt], color=GOLD, lw=2.0, marker='o', ms=5,
         zorder=4, label='base case — usage recovers in FY27')
axR.plot(np.r_[3, xf], np.r_[a25, pers_prt], color=RUST, lw=1.8, ls='--', marker='s',
         ms=4.5, zorder=3, label='persistence — −6% usage endures')
axR.text(8, base_prt[-1] + 0.008, f'{base_prt[-1]:.2f}', ha='center', fontsize=9,
         color=BRASS, fontweight='bold')
axR.text(8, pers_prt[-1] - 0.014, f'{pers_prt[-1]:.2f}', ha='center', fontsize=9,
         color=RUST, fontweight='bold')
axR.set_xticks(range(9))
axR.set_xticklabels(['FY2022', 'FY2023', 'FY2024', 'FY2025', 'FY2026E', 'FY2027E',
                     'FY2028E', 'FY2029E', 'FY2030E'], fontsize=9, rotation=45,
                    ha='right')
axR.set_ylabel('Consumption revenue per avg connected RT\n(AED thousand per RT)')
axR.set_ylim(1.00, 1.28)
axR.set_title('Usage intensity — the crux, both framings',
              fontsize=10.5, fontweight='bold', loc='left', pad=10)
axR.legend(frameon=False, loc='lower right', fontsize=9)
axR.grid(axis='x', visible=False)
style(axR)
save(fig, 'fig8_unit.png')

# ---- FD1 expert panel --------------------------------------------------------
# Ranges derived from study_numbers.json with the same constructions the study
# document states (docx_empower.py): E1 = the crux-grid endpoints each carrying
# half the effect of a 50bp move in the cost of capital; E2 = the committed-
# dividend model at the 2.0% and 3.0% growth nodes; E3 = market price to the
# DEWA control print, central at the peer-P/E read.
_SN, _CRX, _W = D['sens_wg'], D['crux'], D['wacc']
_gi = _SN['g_grid'].index(D['inputs']['g_term']['value'])
_wi = _SN['wacc_grid'].index(_W['rating_ct'])
_bc = _SN['table'][_wi][_gi]
_e1lo = _CRX['rows'][0]['ps'] * (1 + 0.5 * (_SN['table'][_wi + 1][_gi] / _bc - 1))
_e1hi = _CRX['rows'][-1]['ps'] * (1 + 0.5 * (_SN['table'][_wi - 1][_gi] / _bc - 1))
_dps, _ke = D['ddm']['dps'], _W['ke_rating']
_e2 = lambda g: _dps * (1 + g) / (_ke - g)
experts = [('Expert 1\n(Infrastructure DCF)', _e1lo, _e1hi, D['dcf']['base_ct']['ps']),
           ('Expert 2\n(Income/dividend)', _e2(_SN['g_grid'][1]), _e2(_SN['g_grid'][3]),
            D['ddm']['ps']),
           ('Expert 3\n(Relative value & control transaction)', D['meta']['spot'],
            D['dewa_buyin']['price'], D['rel']['ps_pe'])]
fig, axes = plt.subplots(1, 3, figsize=(9.8, 4.2), dpi=110, sharey=True)
for k, (ax, (lab, lo, hi, ce)) in enumerate(zip(axes, experts)):
    ax.bar(0, hi - lo, bottom=lo, width=0.42, color=SAGE_L, edgecolor=SAGE,
           linewidth=1.2, zorder=3)
    ax.plot([-0.24, 0.24], [ce, ce], color=BRASS, lw=3.4, zorder=5)
    ax.text(0.30, ce, f' central {ce:.2f}', va='center', ha='left', fontsize=9.5,
            color=INK, fontweight='bold', bbox=bbox(), zorder=6)
    ax.text(0.30, hi, f' {hi:.2f}', va='center', ha='left', fontsize=9, color=INK,
            bbox=bbox(), zorder=6)
    ax.text(0.30, lo, f' {lo:.2f}', va='center', ha='left', fontsize=9, color=INK,
            bbox=bbox(), zorder=6)
    ax.axhline(SPOT, color=RUST, lw=1.7, zorder=4)
    if k == 0:
        ax.text(-0.62, SPOT, f'spot {SPOT:.2f}', va='bottom', ha='left', fontsize=9.5,
                color=RUST, fontweight='bold')
    ax.set_xlim(-0.70, 1.05)
    ax.set_xticks([])
    ax.set_title(lab, fontsize=9.5, fontweight='bold', pad=10)
    ax.grid(axis='x', visible=False)
    style(ax)
axes[0].set_ylabel('Value per share (AED)')
axes[0].set_ylim(1.35, 3.05)
fig.suptitle('The expert panel — three independent methods, three ranges',
             fontsize=11.5, fontweight='bold', x=0.02, ha='left')
save(fig, 'figD1_experts.png')

# ---- post-render alpha verification -----------------------------------------
print('\nalpha check on rendered files:')
for f_ in ['fig1_football.png', 'fig2_sens.png', 'fig3_ma.png', 'fig4_fan.png',
           'fig5_dist.png', 'fig6_dist.png', 'fig7_bridge.png', 'fig8_unit.png',
           'figD1_experts.png']:
    img = plt.imread(os.path.join(HERE, f_))
    amin = img[:, :, 3].min() if img.shape[2] == 4 else 1.0
    print(f'  {f_}: shape {img.shape}, min alpha {amin:.3f}')
    assert amin == 1.0, f'{f_} carries transparency'
print('figures done — zero transparency confirmed')
