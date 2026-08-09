"""EIPICO study figures. SOLID light canvas on every figure so numbers stay readable when
the page behind them is dark; zero transparency; label positions chosen so nothing overlaps
a title, an axis or another label."""
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
INK, GRID, GREY, BG = '#1C3A36', '#D5DDDB', '#5A6764', '#FBF9F4'
TEAL, RUST = '#2E6B63', '#A8552F'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG, 'axes.edgecolor': GREY,
                     'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
                     'text.color': INK, 'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.titlecolor': INK,
                     'savefig.transparent': False, 'savefig.facecolor': BG,
                     'font.size': 9.4})

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, H, FC, W, DCFD, LN = D['meta'], D['history'], D['forecast'], D['wacc'], D['dcf'], D['lenses']
UB, SENS, CAL, CRUX = D['unit_build'], D['sensitivity'], D['calibration'], D['crux']
V = {k: v['value'] for k, v in D['inputs'].items()}
SPOT = M['spot']
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']


def style(ax):
    for s_ in ('top', 'right'):
        ax.spines[s_].set_visible(False)
    for s_ in ('left', 'bottom'):
        ax.spines[s_].set_color(GREY)


def save(fig, name):
    path = os.path.join(HERE, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    from PIL import Image
    import numpy as _np
    im = Image.open(path)
    if im.mode == 'RGBA':
        assert _np.array(im)[:, :, 3].min() == 255, f'{name} has a transparent pixel'
        im.convert('RGB').save(path)
    print('wrote', name, '- solid canvas verified')


# ---- F1: the valuation field -------------------------------------------------
items = LN['items']
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=110)
names = [i['name'].replace('Discounted cash flow — ', 'DCF ').replace(
    'Book value and sustainable return', 'Book value /\nsustainable return').replace(
    'Normalised earnings power', 'Normalised\nearnings power').replace(
    'Relative multiples', 'Relative\nmultiples') for i in items]
vals = [i['value'] for i in items]
y = np.arange(len(items))[::-1]
ax.barh(y, vals, height=0.5, color=SAGE, alpha=0.55, edgecolor=TEAL, linewidth=1.1)
for yy, v in zip(y, vals):
    ax.text(v + 2.0, yy, f'{v:,.0f}', va='center', ha='left', fontsize=9.6, color=INK,
            fontweight='bold')
ax.axvline(LN['fair_base'], color=BRASS, lw=2.6)
ax.axvline(SPOT, color=RUST, lw=2.0, ls='--')
ax.set_yticks(y, names, fontsize=9.0)
ax.set_xlim(0, max(max(vals), SPOT) * 1.22)
ax.set_xlabel('EGP per share')
ax.text(LN['fair_base'], len(items) - 0.28, f"weighted centre {LN['fair_base']:,.0f}",
        color=BRASS, fontsize=9.2, ha='center', fontweight='bold')
ax.text(SPOT - 2.5, len(items) - 0.28, f'market price {SPOT:,.2f}', color=RUST,
        fontsize=9.2, ha='right', fontweight='bold')
ax.set_ylim(-1.25, len(items) - 0.05)
ax.set_title('Five lenses, one field — each is an independent route to a value per share',
             fontsize=10.4, pad=12)
style(ax)
save(fig, 'fig1_field.png')

# ---- F2: revenue built from volume and price ---------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.6), dpi=110)
x = np.arange(7)
labels = ['FY24', 'FY25'] + YRS
dom = [UB['dom_rev_fy24'], UB['dom_rev_fy25']] + FC['rev_dom']
exp = [UB['exp_rev_fy24'], UB['exp_rev_fy25']] + FC['rev_exp']
a1.bar(x, dom, 0.62, label='Domestic', color=TEAL, alpha=0.85)
a1.bar(x, exp, 0.62, bottom=dom, label='Export', color=GOLD, alpha=0.9)
a1.set_xticks(x, labels, fontsize=8.6)
a1.set_ylabel('EGP million')
a1.legend(frameon=False, fontsize=8.8, loc='upper left')
a1.set_title('Revenue by book', fontsize=10)
style(a1)
dp = [UB['dom_packs_fy24'], UB['dom_packs_fy25']] + FC['dom_packs']
ep = [UB['exp_packs_fy24'], UB['exp_packs_fy25']] + FC['exp_packs']
pp = [UB['dom_price_fy24'], UB['dom_price_fy25']] + FC['dom_price']
a2.bar(x - 0.2, dp, 0.36, label='Domestic packs (mn)', color=TEAL, alpha=0.75)
a2.bar(x + 0.2, ep, 0.36, label='Export packs (mn)', color=GOLD, alpha=0.85)
a3 = a2.twinx()
a3.plot(x, pp, color=RUST, lw=2.1, marker='o', ms=4.2, label='Domestic EGP/pack')
a3.set_ylabel('EGP per pack', color=RUST)
a3.tick_params(axis='y', colors=RUST)
a3.grid(False)
a2.set_xticks(x, labels, fontsize=8.6)
a2.set_ylabel('million packs')
a2.set_title('Volume and realised price, built separately', fontsize=10)
h1, l1 = a2.get_legend_handles_labels(); h2, l2 = a3.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.2, loc='upper left')
style(a2)
save(fig, 'fig2_volume_price.png')

# ---- F3: the depreciation step ------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.5), dpi=110)
xs = np.arange(8)
lab = ['FY23', 'FY24', 'FY25'] + YRS
dna = [H['FY2023']['dna'], H['FY2024']['dna'], H['FY2025']['dna']] + FC['dna']
cip = [3058.2, V['cip_fy24'], V['cip_fy25']] + FC['cip']
ax.bar(xs, dna, 0.58, color=RUST, alpha=0.85, label='Depreciation and amortisation')
ax.set_ylabel('EGP million — charge', color=RUST)
ax.set_xticks(xs, lab, fontsize=8.8)
axb = ax.twinx()
axb.plot(xs, cip, color=TEAL, lw=2.2, marker='s', ms=4.4,
         label='Construction balance not yet depreciating')
axb.set_ylabel('EGP million — balance', color=TEAL)
axb.tick_params(axis='y', colors=TEAL)
axb.grid(False)
for i, v in enumerate(dna):
    ax.text(i, v + 12, f'{v:,.0f}', ha='center', fontsize=8.2, color=INK)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = axb.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.6, loc='upper center',
          bbox_to_anchor=(0.5, -0.13), ncol=2)
ax.set_ylim(0, max(dna) * 1.18)
ax.set_title('The construction balance stops being free — the depreciation step is the '
             'largest mechanical change in the forecast', fontsize=10, pad=10)
style(ax)
save(fig, 'fig3_depreciation.png')

# ---- F4: the traded multiple, re-rated ----------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=110)
oh = LN['own_pe_history']
xs = list(range(len(oh) + 1))
pes = [o['pe'] for o in oh] + [LN['pe_now']]
labs = [str(o['year']) for o in oh] + ['today']
cols = [SAGE] * len(oh) + [RUST]
bars = ax.bar(xs, pes, 0.56, color=cols, alpha=0.85)
for b, v in zip(bars, pes):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.28, f'{v:.1f}x', ha='center', fontsize=9.4,
            color=INK, fontweight='bold')
ax.axhline(LN['own_pe_mean'], color=BRASS, lw=1.8, ls='--')
ax.text(0.02, LN['own_pe_mean'] + 0.35, f"four-year mean {LN['own_pe_mean']:.1f}x",
        color=BRASS, fontsize=9.0)
ax.axhline(LN['just_fwd_pe'], color=TEAL, lw=1.8, ls=':')
ax.text(len(xs) - 1.4, LN['just_fwd_pe'] + 0.35,
        f"multiple this model justifies {LN['just_fwd_pe']:.1f}x", color=TEAL, fontsize=9.0,
        ha='right')
ax.set_xticks(xs, labs, fontsize=9.0)
ax.set_ylabel('price / attributable earnings')
ax.set_ylim(0, max(pes) * 1.25)
ax.set_title('The single most important fact about this share price: the multiple has more '
             'than doubled', fontsize=10, pad=10)
style(ax)
save(fig, 'fig4_multiple.png')

# ---- F5: the probability cone --------------------------------------------------
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'PHAR_Stock_Price_History.csv')), 'PHAR',
                  verbose=False, market='EG')
tail = df.tail(160)
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=110)
ax.plot(range(len(tail)), tail['Price'].values, color=INK, lw=1.5)
n0 = len(tail) - 1
for short, hz, off in (('1M', strike['horizons']['1M'], 22), ('3M', strike['horizons']['3M'], 64)):
    xs = [n0, n0 + off]
    for lo, hi, al in (('p5', 'p95', 0.16), ('p25', 'p75', 0.30)):
        ax.fill_between(xs, [tail['Price'].iloc[-1], hz['pct'][lo]],
                        [tail['Price'].iloc[-1], hz['pct'][hi]], color=TEAL, alpha=al,
                        linewidth=0)
    ax.plot(xs, [tail['Price'].iloc[-1], hz['pct']['p50']], color=BRASS, lw=1.8)
    ax.text(n0 + off + 1.5, hz['pct']['p95'], f"{short} 95th {hz['pct']['p95']:,.0f}",
            fontsize=8.4, va='center', color=INK)
    ax.plot([n0 + off], [hz['pct']['p50']], marker='o', ms=4.0, color=BRASS)
    ax.text(n0 + off + 1.5, hz['pct']['p50'], f"{short} median {hz['pct']['p50']:,.0f}",
            fontsize=8.4, va='bottom', color=BRASS)
    ax.text(n0 + off + 1.5, hz['pct']['p5'], f"{short} 5th {hz['pct']['p5']:,.0f}",
            fontsize=8.4, va='center', color=INK)
ax.axhline(LN['fair_base'], color=RUST, lw=1.6, ls='--')
ax.text(2, LN['fair_base'] + 5.5, f"weighted central fair value {LN['fair_base']:,.0f}",
        color=RUST, fontsize=8.8, va='bottom')
ax.set_xlim(0, n0 + 92)
ax.set_ylabel('EGP per share')
ax.set_xticks([])
ax.set_title('Where the price could be in one and three months — the shaded bands are the '
             '50% and 90% intervals', fontsize=10, pad=10)
style(ax)
save(fig, 'fig5_cone.png')

# ---- F6: sensitivity tornado ----------------------------------------------------
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=110)
base = DCFD['frame_A']['per_share']
rows = [('Terminal risk-free rate', SENS['wacc'][0][1], SENS['wacc'][-1][1]),
        ('Beta', SENS['beta'][-1][1], SENS['beta'][0][1]),
        ('Terminal growth', SENS['g'][0][1], SENS['g'][-1][1]),
        ('Provision charge', SENS['prov'][-1][1], SENS['prov'][0][1]),
        ('Exchange-rate path', SENS['fx'][-1][1], SENS['fx'][0][1]),
        ('Domestic volume growth', SENS['volume'][0][1], SENS['volume'][-1][1]),
        ('Depreciation rate', SENS['dep'][-1][1], SENS['dep'][0][1])]
rows.sort(key=lambda t: abs(t[2] - t[1]))
yy = np.arange(len(rows))
for i, (nm, lo, hi) in enumerate(rows):
    ax.barh(i, hi - base, left=base, height=0.5, color=TEAL, alpha=0.6)
    ax.barh(i, lo - base, left=base, height=0.5, color=RUST, alpha=0.55)
    ax.text(min(lo, hi) - 1.5, i, f'{min(lo, hi):,.0f}', ha='right', va='center', fontsize=8.6)
    ax.text(max(lo, hi) + 1.5, i, f'{max(lo, hi):,.0f}', ha='left', va='center', fontsize=8.6)
ax.axvline(base, color=INK, lw=1.6)
ax.set_yticks(yy, [r[0] for r in rows], fontsize=9.0)
ax.set_xlabel('EGP per share')
lo_all = min(min(r[1], r[2]) for r in rows); hi_all = max(max(r[1], r[2]) for r in rows)
ax.set_xlim(lo_all - (hi_all - lo_all) * 0.16, hi_all + (hi_all - lo_all) * 0.16)
ax.set_title(f'What actually moves the answer (base {base:,.0f} per share)', fontsize=10,
             pad=10)
style(ax)
save(fig, 'fig6_tornado.png')

# ---- F7: the crux, as a reverse valuation ---------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=110)
levels = [0, 1000, 2000, 3000, 4000, CRUX['required_fy30_revenue'], 6000]
import bisect
xs = sorted(set(levels))
ys = []
for L in xs:
    frac = L / CRUX['required_fy30_revenue'] if CRUX['required_fy30_revenue'] else 0
    ys.append(base + frac * (SPOT - base))
ax.plot(xs, ys, color=TEAL, lw=2.4, marker='o', ms=4.6)
ax.axhline(SPOT, color=RUST, lw=1.8, ls='--')
ax.text(80, SPOT + 1.6, f'market price {SPOT:,.2f}', color=RUST, fontsize=9.0)
ax.axhline(base, color=BRASS, lw=1.8, ls=':')
ax.text(80, base + 2.4, f'the model without a revenue line for the new plant {base:,.0f}',
        color=BRASS, fontsize=9.0, va='bottom')
ax.axvline(CRUX['required_fy30_revenue'], color=INK, lw=1.4)
ax.text(CRUX['required_fy30_revenue'] - 150, (base + SPOT) / 2,
        f"EGP {CRUX['required_fy30_revenue']:,.0f}m required\n"
        f"(USD {CRUX['required_rev_usd_mn']:,.0f}m a year)", fontsize=9.0, ha='right',
        va='center', color=INK, fontweight='bold')
ax.set_xlabel('additional FY2030E revenue from the biologicals facility (EGP million)')
ax.set_ylim(base - 6, max(ys) + 4)
ax.set_ylabel('EGP per share')
ax.set_title('The crux, stated as a reverse valuation — how much the new plant must sell',
             fontsize=10, pad=10)
style(ax)
save(fig, 'fig7_crux.png')

# ---- F8: the expert panel -------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.2), dpi=110)
experts = [('Expert 1\ncash-flow', 74.0, 86.1, 101.0),
           ('Expert 2\nasset and return', 62.0, 73.5, 88.0),
           ('Expert 3\nmarket-implied', 96.0, 118.0, 141.0)]
for i, (nm, lo, mid, hi) in enumerate(experts):
    ax.barh(i, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.5, edgecolor=TEAL)
    ax.plot([mid, mid], [i - 0.21, i + 0.21], color=BRASS, lw=3.0)
    ax.text(hi + 2, i, f'{lo:,.0f}–{hi:,.0f} · centre {mid:,.0f}', va='center', fontsize=8.8)
ax.axvline(SPOT, color=RUST, lw=1.8, ls='--')
ax.text(SPOT, -0.78, f'market price {SPOT:,.2f}', color=RUST, fontsize=8.8, ha='center')
ax.set_yticks(range(3), [e[0] for e in experts], fontsize=9.0)
ax.set_xlim(40, 190)
ax.set_ylim(-1.0, 2.6)
ax.set_xlabel('EGP per share')
ax.set_title('Three independent methods, three different answers', fontsize=10, pad=10)
style(ax)
save(fig, 'fig8_experts.png')
print('all figures written on a solid light canvas, zero transparency')
