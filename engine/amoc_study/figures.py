"""AMOC study figures. House palette; a SOLID light background on every figure so the
numbers stay readable when the page behind them is dark, and label positions chosen so
nothing overlaps a title, an axis, a series or another label.

Values on this name run from roughly EGP 4 to EGP 17 a share, so every money label carries
two decimals — a whole-pound label would collapse distinct lenses onto the same number.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib
matplotlib.use('Agg')
# A FIGURE MAY NOT DRAW SOMETHING OUTSIDE ITS OWN AXIS AND SAY NOTHING. This wraps
# savefig, so every figure below is checked; it caught a hardcoded x-axis that clipped
# seven bars to the same length and threw away the price line the caption relies on.
import figure_guard                                                   # noqa: F401,E402
import matplotlib.pyplot as plt
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

d = json.load(open(os.path.join(HERE, 'study_numbers.json')))
spot = d['spot']
F, U, BASE, DCF = d['fcst'], d['unit'], d['base'], d['dcf']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'AMOC_Stock_Price_History.csv')),
                  'AMOC', verbose=False, market='EG')


def style(ax):
    for s_ in ['top', 'right']:
        ax.spines[s_].set_visible(False)
    for s_ in ['left', 'bottom']:
        ax.spines[s_].set_color(GREY)


# ---- F1 football field ------------------------------------------------------
# THE FIGURE IS BUILT FROM lens_record, NOT FROM THE RAW LENS SPANS, AND THE REASON IS THAT
# IT DISAGREED WITH THE STUDY'S OWN RECORD ON THREE ROWS OF FIVE. It carried a "Weighted
# central" bar whose span and base were IDENTICAL to the cash-flow row above it — because
# under [R-LENS-03] the primary lens IS the central, so the row duplicated the answer under
# a name the protocol retired. It drew the relative multiple as a live 9.88-15.30 lens
# while the record marks it withdrawn:true and the study's own Table 1 prints it WITHDRAWN
# with dashes for bear and bull. And it drew normalised earnings as a lens, which the
# record's retired note drops for this class outright and carries as a diagnostic.
#
# THE ANSWER IS ONE BAR. Everything else is a cross-check, drawn as a POINT where the
# record says it has no present-value range, and labelled with what it is. A reader can now
# see which number is the study's and which are held beside it, which is the whole of what
# [R-LENS-03] asks a figure to show.
LR = d['lens_record']
L = d['lenses']
PRIM = LR['primary']
rows = [('%s\n(the answer)' % {'dcf': 'Free cash flow\nto the firm'}.get(
             PRIM['kind'], PRIM['kind']),
         PRIM['range']['low'], PRIM['value'], PRIM['range']['high'], True, '')]
_LABEL = {'relative_multiple': 'Relative\n(EV/EBITDA)', 'book_value': 'Book value /\nsustainable return'}
for c in LR['cross_checks']:
    tag = 'withdrawn' if c.get('withdrawn') else 'cross-check'
    if c.get('kind') == 'book_value':
        tag = 'disclosed floor'
    k = {'relative_multiple': 'relative', 'book_value': 'book'}.get(c['kind'])
    lo = hi = None
    if not c.get('withdrawn') and k and k in L:
        lo, hi = L[k]['bear'], L[k]['bull']
    rows.append((_LABEL.get(c['kind'], c['kind']), lo, c['value'], hi, False, tag))
for name, val in LR.get('diagnostics', {}).items():
    rows.append((name.replace('_', ' ').capitalize(), None, val, None, False, 'diagnostic'))

fig, ax = plt.subplots(figsize=(9.7, 4.2), dpi=110)
_all = [x for r in rows for x in (r[1], r[2], r[3]) if x is not None] + [spot]
xmin, xmax = min(_all), max(_all)
pad = 0.04 * (xmax - xmin)
for i, (name, lo, base, hi, primary, tag) in enumerate(rows):
    y = len(rows) - 1 - i
    col = GOLD if primary else SAGE
    if lo is not None and hi is not None:
        ax.barh(y, hi - lo, left=lo, height=0.46, color=col,
                alpha=0.5 if primary else 0.32, edgecolor=col, linewidth=1.1)
        txt = f'{lo:.2f}-{hi:.2f} · base {base:.2f}'
        at = hi
    else:
        # NO RANGE IS DRAWN WHERE THE RECORD SAYS THERE IS NONE. A withdrawn lens and a
        # diagnostic have a value and no present-value span, and drawing a bar for them
        # would state a range the study does not publish.
        ax.plot([base], [y], marker='D', ms=7, color=col, zorder=3)
        txt = f'{base:.2f}'
        at = base
    ax.plot([base, base], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    # A LABEL THAT CROSSES THE SPOT LINE IS A COLLISION, and depth-bar standard 5 says
    # they are fixed in the pass that finds them. The line goes behind and the text
    # carries the panel colour behind it, so both stay legible where they overlap.
    ax.text(at + pad, y, txt + (f'  ({tag})' if tag else ''),
            va='center', fontsize=8.6, color=INK, zorder=4,
            bbox=dict(boxstyle='square,pad=0.12', fc=BG, ec="none"))
ax.axvline(spot, color=INK, lw=1.6, zorder=1)
ax.text(spot + 0.3 * pad, -0.62, f'spot {spot:.2f}', color=INK, fontsize=9,
        ha='left', va='top', zorder=4)
ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1], fontsize=8.6)
ax.set_xlabel('EGP / share')
# THE LIMITS ARE DERIVED FROM WHAT IS DRAWN, SPOT INCLUDED. The superseded generator that
# last wrote this file hardcoded set_xlim(2, 11) against a spot of 13.50, so the price line
# it drew fell outside the axis and was clipped away silently — while the caption told a
# reader the price was shown. That is the same defect the chart-overlay gate exists for,
# arriving in a study figure instead of a ticker page.
ax.set_xlim(xmin - 1.5 * pad, xmax + 9 * pad)
ax.set_ylim(-1.0, len(rows) - 0.4)
ax.set_title('Alexandria Mineral Oils — the answer, and the reads held beside it',
             fontsize=10, pad=10)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png')); plt.close(fig)

# ---- F2 sensitivity heatmap (terminal cost of capital x terminal growth) -----
S = d['sens_wg']; tab = np.array(S['table'])
fig, ax = plt.subplots(figsize=(8.4, 3.9), dpi=110)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        v = tab[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=9.2, color=INK,
                fontweight='bold' if abs(v - spot) < 0.5 else 'normal')
ax.set_xticks(range(len(S['g_grid'])), [f'{x*100:.0f}%' for x in S['g_grid']])
ax.set_yticks(range(len(S['wacc_grid'])), [f'{x*100:.1f}%' for x in S['wacc_grid']])
ax.set_xlabel('terminal growth'); ax.set_ylabel('terminal cost of capital')
ax.set_title(f'Cash-flow fair value (EGP/share) — terminal cost of capital × terminal growth; '
             f'bold ≈ spot {spot:.2f}', fontsize=10, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png')); plt.close(fig)

# ---- F3 moving-average stack ------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='AMOC close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'{n}-session average')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper left')
ax.set_title('Alexandria Mineral Oils — price against the moving-average stack, last 260 sessions',
             fontsize=10, pad=8)
ax.set_ylabel('EGP'); style(ax)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_ma.png')); plt.close(fig)

# ---- F4 fan chart -----------------------------------------------------------
fan = np.load(os.path.join(HERE, 'fan.npy')); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the middle half)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
cb = L['central']['base']
ax.axhline(cb, color=BRASS, lw=1.4, ls='--')
ymax = fan[4].max(); ymin = fan[0].min(); rng = ymax - ymin
ax.text(1, cb + 0.022 * rng, f'fundamental central ≈ {cb:.2f}', color=BRASS, fontsize=8.6,
        va='bottom')
ax.text(days[-1] - 1, spot - 0.026 * rng, f'spot {spot:.2f}', color=GREY, fontsize=8.6,
        ha='right', va='top')
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('EGP / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='upper left')
ax.set_title('Forward price cone to three months — 50,000 simulated paths', fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_fan.png')); plt.close(fig)

# ---- F5/F6 distributions ----------------------------------------------------
for tag, fn, out in [('one month', 'paths_1M.npy', 'fig5_dist.png'),
                     ('three months', 'paths_3M.npy', 'fig6_dist.png')]:
    x = np.load(os.path.join(HERE, fn))[:, -1]
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    yl = ax.get_ylim()[1]
    ax.text(spot, yl * 0.97, f'spot {spot:.2f} ', color=INK, fontsize=8.4, ha='right', va='top')
    ax.text(np.median(x), yl * 0.84, f' median {np.median(x):.2f}', color=BRASS, fontsize=8.4,
            ha='left', va='top')
    # THE TAIL IS CROPPED ON PURPOSE AND THE PRICE LINE MUST STILL BE INSIDE IT. Cropping
    # a simulated distribution at its 0.3rd and 99.7th percentiles is an honest choice —
    # the extreme paths are a handful of draws and drawing them flattens everything else.
    # Losing the spot line off the edge is not: this figure drew the price at 13.50 with
    # the axis ending at 13.35, so the line the reader is meant to compare against was
    # clipped away. The crop is declared, and the limits are widened to hold whatever the
    # figure actually draws.
    _lo, _hi = np.percentile(x, 0.3), np.percentile(x, 99.7)
    _refs = [spot, float(np.median(x))]
    _pad = 0.02 * (_hi - _lo)
    ax.set_xlim(min([_lo] + _refs) - _pad, max([_hi] + _refs) + _pad)
    figure_guard.allow(ax, 'the simulated tail beyond the 0.3rd and 99.7th percentiles is '
                           'cropped deliberately; every reference line is inside the axis')
    ax.set_xlabel('EGP / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, out)); plt.close(fig)

# ---- F7 revenue by product leg, and the margin path -------------------------
yrs = ['Base yr'] + [y.replace('E', '') for y in F['years']]
_b_spec = U['rev25_lines']['oils'] + U['rev25_lines']['wax']
_b_tot = sum(U['rev25_lines'][k] for k in U['lines'])
spec = [_b_spec] + U['spec_rev']
fuel = [_b_tot - _b_spec] + U['fuel_rev']
mar = [d['audited']['base_gm']] + F['gm']
fig, ax = plt.subplots(figsize=(9.9, 4.2), dpi=110)
xs = np.arange(len(yrs))
ax.bar(xs, np.array(fuel) / 1000, width=0.56, color=SAGE, alpha=0.75,
       label='Fuel and by-products', edgecolor='#FFFFFF', linewidth=0.6)
ax.bar(xs, np.array(spec) / 1000, width=0.56, bottom=np.array(fuel) / 1000, color=GOLD,
       alpha=0.88, label='Base and special oils, paraffin wax', edgecolor='#FFFFFF', linewidth=0.6)
tot = (np.array(spec) + np.array(fuel)) / 1000
for i, t in enumerate(tot):
    ax.text(i, t + tot.max() * 0.028, f'{t:.1f}', ha='center', fontsize=8.4, color=INK)
ax.set_ylabel('revenue (EGP bn)')
ax.set_ylim(0, tot.max() * 1.46)
ax.set_xticks(xs, yrs, fontsize=8.8)
ax2 = ax.twinx()
ax2.plot(xs, np.array(mar) * 100, color=BRASS, lw=2.1, marker='o', ms=4.5,
         label='gross margin, as filed then forecast (right axis)')
for i, m in enumerate(mar):
    ax2.text(i, m * 100 + 0.055, f'{m*100:.2f}%', ha='center', va='bottom', fontsize=8.0,
             color=BRASS,
             bbox=dict(boxstyle='round,pad=0.16', facecolor=BG, edgecolor=BRASS,
                       linewidth=0.4, alpha=0.96))
ax2.set_ylabel('gross margin (%)', color=BRASS)
ax2.tick_params(axis='y', colors=BRASS)
# lift the margin axis so the line and its labels ride clear ABOVE the revenue bars
ax2.set_ylim(min(mar) * 100 - 1.95, max(mar) * 100 + 0.22)
ax2.grid(False)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8.4, loc='upper left', labelcolor=INK, ncol=3)
ax.set_title('Revenue by product line, and the gross-margin path', fontsize=10, pad=9)
style(ax)
ax2.spines['top'].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig7_mix.png')); plt.close(fig)

# ---- F8 the free-cash-flow waterfall, 2026E ---------------------------------
i0 = 0
steps = [('EBITDA', F['ebitda'][i0], GOLD),
         ('less depreciation', -F['dna'][i0], SAGE),
         ('less tax on EBIT', -(F['ebit'][i0] - F['nopat'][i0]), SAGE),
         ('add back depreciation', F['dna'][i0], SAGE),
         ('less capital spend', -F['capex'][i0], SAGE),
         ('less working-capital build', -F['dnwc'][i0], SAGE)]
fig, ax = plt.subplots(figsize=(9.9, 4.3), dpi=110)
run = 0.0
for i, (lab, v, col) in enumerate(steps):
    bottom = run if v >= 0 else run + v
    ax.bar(i, abs(v), bottom=bottom, width=0.56, color=GOLD if v >= 0 else '#B98A6B',
           alpha=0.85, edgecolor='#FFFFFF', linewidth=0.6)
    run += v
    ax.text(i, max(run, run - v) + F['ebitda'][i0] * 0.035, f'{v:+,.0f}', ha='center',
            fontsize=8.3, color=INK)
ax.bar(len(steps), run, width=0.56, color=BRASS, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.6)
ax.text(len(steps), run + F['ebitda'][i0] * 0.035, f'{run:,.0f}', ha='center', fontsize=8.6,
        color=INK, fontweight='bold')
ax.set_xticks(range(len(steps) + 1),
              [s[0].replace(' ', '\n', 1) for s in steps] + ['free cash flow\nto the firm'],
              fontsize=8.0)
ax.set_ylabel('EGP mn')
ax.set_ylim(0, F['ebitda'][i0] * 1.22)
ax.set_title('From EBITDA to free cash flow to the firm — 2026E', fontsize=10, pad=9)
ax.grid(axis='x', visible=False)   # vertical rules through a waterfall read as bar edges
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig8_waterfall.png')); plt.close(fig)

# ---- FD1 experts ------------------------------------------------------------
E = d['experts']
ex = [(f"Expert 1 — {E['e1']['method_short']}", E['e1']['base'], E['e1']['rng']),
      (f"Expert 2 — {E['e2']['method_short']}", E['e2']['base'], E['e2']['rng']),
      (f"Expert 3 — {E['e3']['method_short']}", E['e3']['base'], E['e3']['rng'])]
fig, ax = plt.subplots(figsize=(9.9, 3.5), dpi=110)
his = [hi for _, _, (lo, hi) in ex]; los = [lo for _, _, (lo, hi) in ex]
xr = max(his) - min(los)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + 0.02 * xr, y, f'{lo:.2f}–{hi:.2f} · base {ba:.2f}', va='center', fontsize=8.6)
ax.axvline(spot, color=INK, lw=1.6)
ax.text(spot + 0.012 * xr, -0.58, f'spot {spot:.2f}', fontsize=9, color=INK, ha='left', va='top')
pc = d['panel_centre']
ax.axvspan(pc * 0.96, pc * 1.04, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=8.4)
ax.set_xlabel('EGP / share')
ax.set_xlim(min(los) - 0.08 * xr, max(his) + 0.34 * xr)
ax.set_ylim(-0.95, len(ex) - 0.4)
ax.set_title('The three experts’ fair-value ranges — brass tick = base; gold band = panel centre',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png')); plt.close(fig)
print('figures done')
