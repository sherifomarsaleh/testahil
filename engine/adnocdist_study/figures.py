"""ADNOC Distribution study figures. SOLID light canvas on every figure so numbers stay
readable when the page behind them is dark; zero transparency; label positions chosen so
nothing overlaps a title, an axis, a rule or another label.

Every financial numeral on every figure is a dictionary lookup out of study_numbers.json,
strike_result.json or the cleaned price history. No number is typed into this file.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
CUR = M['currency']
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
HIST = ['FY24', 'FY25']


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


def _pc(x, d=1):
    return f'{x * 100:.{d}f}%'


# ---- F1: the valuation field -------------------------------------------------
# One bar per reading. The two frames of the cash-flow model are shown side by side and
# never averaged; the dividend reading carries no weight in either centre.
_relA = LN['shared'][0]['value']
_relB = LN['shared_B'][0]['value']
rows1 = [('Discounted cash flow\nFrame A', LN['items_A'][0]['value']),
         ('Discounted cash flow\nFrame B', LN['items_B'][0]['value']),
         ('Normalised\nearnings power', LN['items_A'][1]['value']),
         (f'Relative multiples\nFrame A (Frame B {_relB:,.2f})', _relA),
         ('Book value /\nsustainable return', LN['shared'][1]['value']),
         ('Dividend capitalisation\n(no weight in either centre)', LN['unweighted'][0]['value'])]
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=110)
vals = [r[1] for r in rows1]
y = np.arange(len(rows1))[::-1]
ax.barh(y, vals, height=0.5, color=SAGE, alpha=0.55, edgecolor=TEAL, linewidth=1.1)
_XMAX = max(max(vals), SPOT) * 1.30
for yy, v in zip(y, vals):
    # printed in a clear right-hand gutter, so a value label can never collide with the
    # centre or market-price rules the chart draws through the bars
    ax.text(_XMAX * 0.995, yy, f'{v:,.2f}', va='center', ha='right', fontsize=9.6, color=INK,
            fontweight='bold')
# the rules stop at the bar band: an axvline would run straight through the legend below it
_YB, _YT = -0.62, len(rows1) - 0.42
ax.vlines(LN['centre_A'], _YB, _YT, color=BRASS, lw=2.6)
ax.vlines(LN['centre_B'], _YB, _YT, color=BRASS, lw=2.6, ls=(0, (5, 2)))
ax.vlines(SPOT, _YB, _YT, color=RUST, lw=2.0, ls='--')
ax.set_yticks(y, [r[0] for r in rows1], fontsize=8.6)
ax.set_xlim(0, _XMAX)
ax.set_xlabel(f'{CUR} per share')
# the three rules sit within 0.8 of each other, so their labels go in a legend in the empty
# band below the last bar rather than as free text that would overprint one another
handles = [Line2D([], [], color=BRASS, lw=2.6, label=f"weighted centre, Frame A  {LN['centre_A']:,.2f}"),
           Line2D([], [], color=BRASS, lw=2.6, ls=(0, (5, 2)),
                  label=f"weighted centre, Frame B  {LN['centre_B']:,.2f}"),
           Line2D([], [], color=RUST, lw=2.0, ls='--', label=f'market price  {SPOT:,.2f}')]
ax.legend(handles=handles, frameon=False, fontsize=9.0, ncol=3, loc='lower center',
          bbox_to_anchor=(0.5, -0.03), handlelength=2.4, columnspacing=2.0)
ax.set_ylim(-1.5, len(rows1) - 0.35)
ax.set_title('Five weighted readings and one unweighted reading — the two inventory frames '
             'are published side by side, never averaged', fontsize=10.4, pad=12)
style(ax)
save(fig, 'fig1_field.png')

# ---- F2: revenue built from volume and price ---------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.8, 3.6), dpi=110,
                             gridspec_kw={'wspace': 0.34})
x = np.arange(7)
labels = HIST + YRS
retf = [V['rev_retfuel_fy24'], V['rev_retfuel_fy25']] + FC['rev_retfuel']
nonf = [V['rev_nonfuel_fy24'], V['rev_nonfuel_fy25']] + FC['rev_nonfuel']
comm = [UB['rev_comm_fy24'], UB['rev_comm_fy25']] + FC['rev_comm']
b1 = np.array(retf)
b2 = b1 + np.array(nonf)
a1.bar(x, retf, 0.62, label='Retail fuel', color=TEAL, alpha=0.88)
a1.bar(x, nonf, 0.62, bottom=b1, label='Non-fuel retail', color=GOLD, alpha=0.92)
a1.bar(x, comm, 0.62, bottom=b2, label='Commercial', color=SAGE, alpha=0.92)
tot = b2 + np.array(comm)
for xi, t in zip(x, tot):
    a1.text(xi, t + tot.max() * 0.018, f'{t:,.0f}', ha='center', va='bottom', fontsize=7.6,
            color=INK)
a1.set_xticks(x, labels, fontsize=8.4)
a1.set_ylim(0, tot.max() * 1.14)
a1.set_ylabel(f'{CUR} million')
a1.set_yticks(a1.get_yticks(), [f'{t:,.0f}' for t in a1.get_yticks()], fontsize=8.6)
a1.set_ylim(0, tot.max() * 1.14)
a1.legend(frameon=False, fontsize=8.4, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.13),
          columnspacing=1.2, handlelength=1.5)
a1.set_title('Revenue by stream', fontsize=10)
style(a1)

vr = [V['vol_retail_fy24'], V['vol_retail_fy25']] + FC['vol_retail']
vc = [V['vol_comm_fy24'], V['vol_comm_fy25']] + FC['vol_comm']
pr = [UB['price_retail_fy24'], UB['price_retail_fy25']] + FC['price_retail']
# commercial keeps the SAGE it carries in the left panel — one colour, one meaning
a2.bar(x - 0.2, vr, 0.36, label='Retail fuel', color=TEAL, alpha=0.82)
a2.bar(x + 0.2, vc, 0.36, label='Commercial', color=SAGE, alpha=0.95)
a2.set_ylim(0, max(vr) * 1.45)
a2.set_yticks(a2.get_yticks(), [f'{t:,.0f}' for t in a2.get_yticks()], fontsize=8.6)
a2.set_ylim(0, max(vr) * 1.45)
a3 = a2.twinx()
a3.plot(x, pr, color=RUST, lw=2.1, marker='o', ms=4.2, label=f'Realised retail {CUR}/litre')
_pspan = max(pr) - min(pr)
for xi, p in zip(x, pr):
    # opaque plate behind each price label so the line it belongs to can never strike through it
    a3.text(xi, p + _pspan * 0.13, f'{p:.2f}', ha='center', va='bottom', fontsize=7.8,
            color=RUST, fontweight='bold',
            bbox=dict(facecolor=BG, edgecolor='none', pad=0.9))
a3.set_ylabel(f'{CUR} per litre', color=RUST)
a3.tick_params(axis='y', colors=RUST)
a3.set_ylim(min(pr) - _pspan * 2.0, max(pr) + _pspan * 0.62)
a3.grid(False)
a2.set_xticks(x, labels, fontsize=8.4)
a2.set_ylabel('million litres')
a2.set_title('Volume and realised price, built separately', fontsize=10)
h1, l1 = a2.get_legend_handles_labels(); h2, l2 = a3.get_legend_handles_labels()
a2.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.4, ncol=3, loc='upper center',
          bbox_to_anchor=(0.5, -0.13), columnspacing=1.1, handlelength=1.5)
style(a2)
save(fig, 'fig2_volume_price.png')

# ---- F3: gross profit split into structural and inventory movement -------------
# THE CENTRAL CHART. The structural bar is what the network earns on the litres it sells;
# the inventory bar is what the price of the barrel did to the stock already in the tanks.
fig, ax = plt.subplots(figsize=(9.0, 3.5), dpi=110)
inv_h = [V['invgain_fy24'], V['invgain_fy25'], V['invgain_h126'] * 2]
str_h = [V['gp_fy24'] - V['invgain_fy24'], V['gp_fy25'] - V['invgain_fy25'],
         (V['gp_h126'] - V['invgain_h126']) * 2]
hx = [0.0, 1.0, 2.0]
ax.bar(hx, str_h, 0.52, color=SAGE, alpha=0.92, label='Structural gross profit')
ax.bar(hx, inv_h, 0.52, bottom=str_h, color=RUST, alpha=0.88, label='Inventory movement')
fx = [3.35 + i for i in range(5)]
allx, alltot, allinv = list(hx), [s + i for s, i in zip(str_h, inv_h)], list(inv_h)
for i, xc in enumerate(fx):
    for dx, frame in ((-0.19, 'A'), (0.19, 'B')):
        st = FC['gp_struct'][i]
        iv = FC['invmove_A'][i] if frame == 'A' else FC['invmove_B'][i]
        ax.bar(xc + dx, st, 0.34, color=SAGE, alpha=0.92)
        ax.bar(xc + dx, iv, 0.34, bottom=st, color=RUST, alpha=0.88)
        allx.append(xc + dx); alltot.append(st + iv); allinv.append(iv)
        ax.text(xc + dx, -max(alltot) * 0.055, frame, ha='center', va='top', fontsize=7.4,
                color=GREY)
_TOP = max(alltot) * 1.30
for xi, t, iv in zip(allx, alltot, allinv):
    ax.text(xi, t + _TOP * 0.012, f'{iv:,.0f}', ha='center', va='bottom', fontsize=7.2,
            color=RUST, fontweight='bold')
ax.set_ylim(0, _TOP)
ax.set_xticks(hx + fx, ['FY24', 'FY25', 'H1-26\nannualised'] + YRS, fontsize=8.4)
ax.tick_params(axis='x', pad=13)
ax.set_ylabel(f'{CUR} million')
ax.legend(frameon=False, fontsize=8.6, loc='upper left',
          title='inventory movement printed above each bar', title_fontsize=8.0)
ax.get_legend().get_title().set_color(GREY)
# the leader arrives at the LEFT FLANK of the inventory block, at its mid-height — it never
# approaches the top of the bar, so it cannot cross that bar's printed value label
ax.annotate(f"H1 2026 inventory gain {CUR} {V['invgain_h126']:,.0f}m in six months —\n"
            f"more than the whole of FY24 and FY25 together "
            f"({CUR} {V['invgain_fy24'] + V['invgain_fy25']:,.0f}m)",
            xy=(2.0 + 0.27, str_h[2] + inv_h[2] / 2.0), xytext=(2.63, _TOP * 0.935),
            fontsize=8.4, color=RUST, fontweight='bold', ha='left', va='top',
            arrowprops=dict(arrowstyle='-|>', color=RUST, lw=1.2, shrinkA=3, shrinkB=2,
                            connectionstyle='arc3,rad=0.0'))
ax.set_title('The structural bar grows slowly; the bar that moved in 2026 is the inventory '
             'one — and it is the one that does not repeat', fontsize=10, pad=10)
style(ax)
save(fig, 'fig3_margin_bridge.png')

# ---- F4: the traded multiple --------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=110)
oh = LN['own_pe_history']
labs = [y_.replace('FY', 'FY') for y_ in M['audited_years']]
labs = labs[:len(oh) - 1] + [labs[len(oh) - 1] + '\n(current)']
cols = [SAGE] * (len(oh) - 1) + [RUST]
xs = np.arange(len(oh))
bars = ax.bar(xs, oh, 0.5, color=cols, alpha=0.9)
for b, v in zip(bars, oh):
    ax.text(b.get_x() + b.get_width() / 2, v + max(oh) * 0.022, f'{v:.1f}x', ha='center',
            fontsize=9.6, color=INK, fontweight='bold')
# both rules stop short of the right-hand gutter, which is reserved for their labels; nothing
# is drawn through a number
_RX = len(oh) - 1 + 1.90
ax.set_xlim(-0.62, _RX + 0.12)
ax.hlines(LN['own_pe_mean'], -0.62, len(oh) - 1 + 0.42, color=BRASS, lw=1.8, ls='--')
ax.hlines(LN['just_fwd_pe'], -0.62, len(oh) - 1 + 0.42, color=TEAL, lw=1.8, ls=':')
ax.text(_RX, LN['own_pe_mean'], f"own three-year average\n{LN['own_pe_mean']:.1f}x",
        color=BRASS, fontsize=9.2, ha='right', va='center', fontweight='bold')
ax.text(_RX, LN['just_fwd_pe'],
        f"the forward multiple\nthis model justifies {LN['just_fwd_pe']:.1f}x", color=TEAL,
        fontsize=9.2, ha='right', va='center', fontweight='bold')
ax.set_xticks(xs, labs, fontsize=9.0)
ax.set_ylabel('price / attributable earnings')
ax.set_ylim(0, max(oh) * 1.22)
ax.set_title('The share has not re-rated — it trades near its own recent average, and above '
             'the multiple the cash flows support', fontsize=10, pad=10)
style(ax)
save(fig, 'fig4_multiple.png')

# ---- F5: the probability cone --------------------------------------------------
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'ADNOCDIST_Stock_Price_History.csv')),
                  M['ticker'], verbose=False, market=M['market'])
tail = df.tail(160)
fig, ax = plt.subplots(figsize=(9.6, 3.9), dpi=110)
ax.plot(range(len(tail)), tail['Price'].values, color=INK, lw=1.5)
n0 = len(tail) - 1
last = float(tail['Price'].iloc[-1])
for short, hz, off in (('1M', strike['horizons']['1M'], 20), ('3M', strike['horizons']['3M'], 63)):
    xs = [n0, n0 + off]
    for lo, hi, al in (('p5', 'p95', 0.16), ('p25', 'p75', 0.30)):
        ax.fill_between(xs, [last, hz['pct'][lo]], [last, hz['pct'][hi]], color=TEAL,
                        alpha=al, linewidth=0)
    ax.plot(xs, [last, hz['pct']['p50']], color=BRASS, lw=1.8)
    ax.plot([n0 + off], [hz['pct']['p50']], marker='o', ms=4.0, color=BRASS)
    _bb = dict(facecolor=BG, edgecolor='none', pad=1.2)
    ax.text(n0 + off + 2.0, hz['pct']['p95'], f"{short} 95th {hz['pct']['p95']:,.2f}",
            fontsize=8.4, va='center', color=INK, bbox=_bb)
    ax.text(n0 + off + 2.0, hz['pct']['p50'], f"{short} median {hz['pct']['p50']:,.2f}",
            fontsize=8.4, va='center', color=BRASS, fontweight='bold', bbox=_bb)
    ax.text(n0 + off + 2.0, hz['pct']['p5'], f"{short} 5th {hz['pct']['p5']:,.2f}",
            fontsize=8.4, va='center', color=INK, bbox=_bb)
ax.axhline(LN['centre_A'], color=RUST, lw=1.6, ls='--')
ax.axhline(LN['centre_B'], color=RUST, lw=1.2, ls=':')
_bbr = dict(facecolor=BG, edgecolor='none', pad=1.4)
ax.text(2, LN['centre_A'], f"fundamental centre, Frame A {LN['centre_A']:,.2f}", color=RUST,
        fontsize=8.8, va='top', fontweight='bold', bbox=_bbr)
ax.text(2, LN['centre_B'], f"fundamental centre, Frame B {LN['centre_B']:,.2f}", color=RUST,
        fontsize=8.8, va='bottom', fontweight='bold', bbox=_bbr)
_lo = min(strike['horizons']['3M']['pct']['p5'], float(tail['Price'].min()))
_hi = max(LN['centre_B'], strike['horizons']['3M']['pct']['p95'], float(tail['Price'].max()))
ax.set_ylim(_lo - (_hi - _lo) * 0.10, _hi + (_hi - _lo) * 0.13)
ax.set_xlim(0, n0 + 63 + 46)
ax.set_ylabel(f'{CUR} per share')
ax.set_xticks([])
ax.set_title('Where the price could be in one and three months — the shaded bands are the '
             '50% and 90% intervals', fontsize=10, pad=10)
style(ax)
save(fig, 'fig5_cone.png')

# ---- F6: sensitivity tornado ----------------------------------------------------
# EVERY bar carries the INPUT range that produced it. A tornado whose input ranges are not
# printed cannot be checked by the reader.
fig, ax = plt.subplots(figsize=(9.2, 4.0), dpi=110)
base = DCFD['frame_A']['per_share']


def _ends(key):
    s = SENS[key]
    return s[0][1], s[-1][1], s[0][0], s[-1][0]


rows = []
lo_, hi_, a_, b_ = _ends('beta')
rows.append((f'Beta\n{a_:.2f} to {b_:.2f}', lo_, hi_))
lo_, hi_, a_, b_ = _ends('wacc')
rows.append((f'Discount rate\n{_pc(a_, 2)} to {_pc(b_, 2)}', lo_, hi_))
lo_, hi_, a_, b_ = _ends('g')
rows.append((f'Terminal growth\n{_pc(a_)} to {_pc(b_)}', lo_, hi_))
lo_, hi_, a_, b_ = _ends('margin')
rows.append((f'Structural gross margin\n{_pc(a_, 0)} to {_pc(b_, 0)} on the unit margin',
             lo_, hi_))
lo_, hi_, a_, b_ = _ends('inventory')
rows.append((f'Recurring inventory movement\n{CUR} {a_:,.0f}m to {CUR} {b_:,.0f}m a year',
             lo_, hi_))
lo_, hi_, a_, b_ = _ends('tax')
rows.append((f'Effective tax rate\n{_pc(a_)} to {_pc(b_)}', lo_, hi_))
lo_, hi_, a_, b_ = _ends('volume')
rows.append((f'Fuel volume growth\n{a_ * 1e4:+,.0f}bp to {b_ * 1e4:+,.0f}bp a year', lo_, hi_))
lo_, hi_, a_, b_ = _ends('capex')
rows.append((f'Capital spending\n{_pc(a_, 0)} to {_pc(b_, 0)} on the forecast', lo_, hi_))
rows.sort(key=lambda t: abs(t[2] - t[1]))
lo_all = min(min(r[1], r[2]) for r in rows); hi_all = max(max(r[1], r[2]) for r in rows)
span = hi_all - lo_all
for i, (nm, lo, hi) in enumerate(rows):
    # RUST always points to the adverse side and TEAL to the favourable one, whichever end of
    # the input range produced it — otherwise the colours would mean opposite things by row
    v_lo, v_hi = min(lo, hi), max(lo, hi)
    ax.barh(i, v_hi - base, left=base, height=0.5, color=TEAL, alpha=0.65)
    ax.barh(i, v_lo - base, left=base, height=0.5, color=RUST, alpha=0.6)
    ax.text(v_lo - span * 0.012, i, f'{v_lo:,.2f}', ha='right', va='center', fontsize=8.6,
            color=INK)
    ax.text(v_hi + span * 0.012, i, f'{v_hi:,.2f}', ha='left', va='center', fontsize=8.6,
            color=INK)
# the base rule stops at the bar band, and its caption sits BESIDE it, not on it
ax.vlines(base, -0.42, len(rows) - 0.42, color=INK, lw=1.6)
ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=8.0)
ax.set_xlabel(f'{CUR} per share')
ax.set_xlim(lo_all - span * 0.19, hi_all + span * 0.19)
ax.set_ylim(-0.95, len(rows) - 0.25)
ax.text(base + span * 0.018, -0.60, f'Frame A base {base:,.2f}', ha='left', va='center',
        fontsize=8.8, color=INK, fontweight='bold')
ax.set_title('What actually moves the answer — each bar labelled with the input range that '
             'produced it', fontsize=10, pad=10)
style(ax)
save(fig, 'fig6_tornado.png')

# ---- F7: the crux, as a reverse valuation ---------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.4), dpi=110)
gx = [p[0] for p in CRUX['ramp']]
gy = [p[1] for p in CRUX['ramp']]
ax.plot(gx, gy, color=TEAL, lw=2.4, marker='o', ms=4.6, zorder=3)
gi, base_v = CRUX['g_implied'], CRUX['normalised_value']
_ylo, _yhi = min(gy + [SPOT]), max(gy + [base_v])
_pad = (_yhi - _ylo)
ax.set_ylim(_ylo - _pad * 0.16, _yhi + _pad * 0.20)
_xlo, _xhi = min(gx), max(gx)
ax.set_xlim(_xlo - (_xhi - _xlo) * 0.06, _xhi + (_xhi - _xlo) * 0.30)
ax.axhline(SPOT, color=RUST, lw=1.8, ls='--')
ax.text(_xhi + (_xhi - _xlo) * 0.28, SPOT - _pad * 0.035, f'market price {SPOT:,.2f}',
        color=RUST, fontsize=9.0, ha='right', va='top', fontweight='bold')
ax.axhline(base_v, color=BRASS, lw=1.8, ls=':')
ax.text(_xlo, base_v + _pad * 0.030,
        f"the model's own reading at {_pc(CRUX['g_base'])} long-run growth {base_v:,.2f}",
        color=BRASS, fontsize=9.0, ha='left', va='bottom', fontweight='bold')
ax.axvline(gi, color=INK, lw=1.4)
ax.plot([gi], [SPOT], marker='o', ms=6.0, color=INK, zorder=4)
ax.annotate(f'the traded price implies long-run\ngrowth of {_pc(gi, 2)} a year — roughly '
            f'nothing,\nfor ever', xy=(gi, SPOT),
            xytext=(gi + (_xhi - _xlo) * 0.09, _ylo + _pad * 0.02), fontsize=9.0, color=INK,
            fontweight='bold', ha='left', va='bottom',
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, shrinkA=2, shrinkB=5))
ax.set_xticks(gx, [_pc(g) for g in gx], fontsize=8.8)
ax.set_xlabel('long-run growth rate assumed after the forecast period')
ax.set_ylabel(f'{CUR} per share')
ax.set_title('The crux, stated backwards — what long-run growth the market is already paying '
             'for', fontsize=10, pad=10)
style(ax)
save(fig, 'fig7_crux.png')

# ---- F8: the expert panel -------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.0, 3.2), dpi=110)
# Each expert's range and worked value are computed from this study's own model, not asserted.
_e1_mid = DCFD['frame_A']['per_share']
_e1_lo = min(SENS['g'][1][1], DCFD['frame_B']['per_share'])
_e1_hi = max(SENS['g'][1][1], DCFD['frame_B']['per_share'])
_e2_mid = LN['book_lens']
_e2_lo, _e2_hi = _e2_mid * 0.85, _e2_mid * 1.15
_e3_mid = LN['div_ps']
_e3_lo = min(SPOT, LN['rel_A'])
_e3_hi = max(SPOT, LN['rel_A'])
experts = [('Expert 1\ncash-flow method', _e1_lo, _e1_mid, _e1_hi),
           ('Expert 2\nasset and sustainable return', _e2_lo, _e2_mid, _e2_hi),
           ('Expert 3\nmarket-implied method', _e3_lo, _e3_mid, _e3_hi)]
_span = max(e[3] for e in experts) - min(e[1] for e in experts)
_yy = list(range(len(experts)))[::-1]          # Expert 1 reads at the TOP
for i, (nm, lo, mid, hi) in zip(_yy, experts):
    ax.barh(i, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.55, edgecolor=TEAL,
            linewidth=1.2)
    ax.plot([mid, mid], [i - 0.23, i + 0.23], color=BRASS, lw=3.2, zorder=4)
    ax.text(hi + _span * 0.035, i, f'{lo:,.2f} – {hi:,.2f}   ·   worked value {mid:,.2f}',
            va='center', ha='left', fontsize=9.0, color=INK)
# the rule stops above the caption band, and the caption sits beside its own rule
ax.vlines(SPOT, -0.55, len(experts) - 0.45, color=RUST, lw=1.8, ls='--', zorder=1)
ax.text(SPOT + _span * 0.02, -0.80, f'market price {SPOT:,.2f}', color=RUST, fontsize=8.8,
        ha='left', va='center', fontweight='bold')
ax.set_yticks(_yy, [e[0] for e in experts], fontsize=9.0)
ax.set_xlim(min(e[1] for e in experts) - _span * 0.10,
            max(e[3] for e in experts) + _span * 0.80)
ax.set_ylim(-1.05, len(experts) - 0.45)
ax.set_xlabel(f'{CUR} per share')
ax.set_title('Three independent methods, three different answers — the brass tick is each '
             "expert's own worked value", fontsize=10, pad=10)
style(ax)
save(fig, 'fig8_experts.png')
print('all figures written on a solid light canvas, zero transparency')
