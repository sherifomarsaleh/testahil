"""EGCH study figures.

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
GRIDJ = json.load(open(os.path.join(HERE, 'sensitivity_grid.json')))
SPOT, DR, YEARS = D['spot'], D['drivers'], D['years']

# THE CONE'S ANCHOR IS NOT THE VALUATION'S SPOT, AND THE CONE FIGURES LABELLED IT AS ONE.
# The probability cone was struck on the close of 2026-08-06 at EGP 13.98; the valuation is
# anchored on 2026-09-03 at EGP 14.41. Both are correct and they are DIFFERENT CLOCKS — the
# study says so in section 2, which states its own close and its own date. But the
# distribution figures drew their anchor line at 14.41 and labelled it "anchor", while the
# distribution behind it was centred on 13.98 and the table's "probability the price ends
# above today's" was measured against 13.98 too. A reader saw a median of 14.19 sitting
# BELOW a line labelled anchor, beside a 56.7% chance of finishing above it, which cannot
# both be true. Three things disagreed and only the label was wrong.
_STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json')))
CONE_ANCHOR = _STRIKE['spot']
CONE_ANCHOR_DATE = _STRIKE['anchor_date']


def _spot_date_words():
    """'3 September 2026' from this study's OWN committed spot date. One source, one date."""
    import datetime as _dt
    _s = str((D.get('meta') or {}).get('spot_date') or D.get('spot_date') or '')
    _s = _s.replace('close ', '').strip()
    for _f in ('%Y-%m-%d', '%d %b %Y', '%d %B %Y'):
        try:
            _d = _dt.datetime.strptime(_s, _f).date()
            return '%d %s %d' % (_d.day, _d.strftime('%B'), _d.year)
        except ValueError:
            pass
    raise ValueError('cannot read a spot date out of %r' % _s)


SPOT_DATE_WORDS = _spot_date_words()
CASES = D['cases']
df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'EGCH_Stock_Price_History.csv')),
                  'EGCH', verbose=False, market='EG')


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


# ---- F1: the value range against the market price ---------------------------
order = [('bear', 'Downside\ncapital spent, plant never earns'),
         ('base', 'Committed capital\nANNA completed, half nameplate'),
         ('bull', 'Upside\nurea holds, ANNA at 70%'),
         ('halt', 'Capital discipline\nprogramme stopped')]
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
vals = [CASES[c]['bridge']['per_share'] for c, _ in order]
ys = np.arange(len(order))
cols = [RUST, BRASS, SAGE, GOLD]
for i, (c, lab) in enumerate(order):
    v = CASES[c]['bridge']['per_share']
    ax.barh(i, max(v, 0) - min(v, 0) if v < 0 else v, left=min(v, 0), height=0.5,
            color=cols[i], edgecolor=INK, linewidth=0.6)
    # negative bars run leftward, so their labels go to the RIGHT of the zero line
    # where the panel is empty — never over the category label on the left
    ax.text(v + 0.16 if v >= 0 else 0.16, i, f"EGP {v:,.2f}",
            va='center', ha='left', fontsize=9.5, color=INK, fontweight='bold')
ax.axvline(0, color=GREY, lw=0.9)
ax.axvline(SPOT, color=CANVAS, lw=1.8, ls='--')
ax.text(SPOT - 0.3, 1.5, f"market price\nEGP {SPOT:,.2f}",
        ha='right', va='center', fontsize=9, color=CANVAS, fontweight='bold')
ax.set_yticks(ys); ax.set_yticklabels([l for _, l in order], fontsize=8.8)
ax.set_xlabel('Value per share (Egyptian pounds)')
ax.set_xlim(-4.6, SPOT * 1.12)
ax.set_title('Fair value per share by case, against the traded price', pad=12, fontsize=11.5)
style(ax); ax.grid(axis='y', visible=False)
save(fig, 'fig1_range.png')

# ---- F2: where the value goes — EV bridge for the committed-capital case -----
b = CASES['base']['bridge']
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
items = [('Present value of\nthe explicit window', b['pv_explicit'], BRASS),
         ('Present value of\nthe terminal value', b['pv_tv'], GOLD),
         ('Enterprise value', b['ev'], CANVAS),
         ('Less net debt', -b['net_debt'], RUST),
         ('Plus listed stakes\nand property', b['fvoci'] + b['inv_prop'], SAGE),
         ('Equity value', b['equity'], CANVAS)]
run = 0
for i, (lab, v, col) in enumerate(items):
    if lab in ('Enterprise value', 'Equity value'):
        ax.bar(i, v, color=col, edgecolor=INK, linewidth=0.6, width=0.62)
        top = v
        run = v
    else:
        ax.bar(i, v, bottom=run, color=col, edgecolor=INK, linewidth=0.6, width=0.62)
        top = run + v
        run = run + v
    ax.text(i, top + (400 if v >= 0 else -900), f"{v:,.0f}", ha='center',
            va='bottom' if v >= 0 else 'top', fontsize=9, color=INK, fontweight='bold')
ax.axhline(0, color=GREY, lw=0.9)
ax.set_xticks(range(len(items)))
ax.set_xticklabels([l for l, _, _ in items], fontsize=8.4)
ax.set_ylabel('EGP million')
ax.set_ylim(-12500, 13500)
ax.set_title('From discounted cash flow to equity value — committed-capital case',
             pad=12, fontsize=11.5)
style(ax); ax.grid(axis='x', visible=False)
save(fig, 'fig2_bridge.png')

# ---- F3: revenue build by channel -------------------------------------------
rows = CASES['base']['rows']
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
x = np.arange(len(YEARS))
legs = [('Export urea', 'rev_exp', GOLD), ('Local free market', 'rev_free', BRASS),
        ('Subsidised', 'rev_sub', SAGE), ('Ammonium nitrate', 'rev_an', CANVAS),
        ('Other', 'rev_other', GREY)]
bot = np.zeros(len(YEARS))
for lab, key, col in legs:
    v = np.array([r[key] for r in rows])
    ax.bar(x, v, bottom=bot, color=col, edgecolor=BG, linewidth=0.8, width=0.62, label=lab)
    bot += v
for i, r in enumerate(rows):
    ax.text(i, bot[i] + 220, f"{r['revenue']:,.0f}", ha='center', fontsize=9,
            color=INK, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(YEARS, fontsize=9)
ax.set_ylabel('Revenue (EGP million)')
ax.set_ylim(0, bot.max() * 1.16)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.26), ncol=5, frameon=False, fontsize=8.6)
ax.set_title('Revenue built channel by channel, tonnes times price', pad=12, fontsize=11.5)
style(ax); ax.grid(axis='x', visible=False)
save(fig, 'fig3_revenue.png')

# ---- F4: cash flow and the capital programme --------------------------------
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
ebitda = np.array([r['ebitda'] for r in rows])
capex = np.array([r['capex'] for r in rows])
fcff = np.array([r['fcff'] for r in rows])
w = 0.28
ax.bar(x - w, ebitda, width=w, color=SAGE, edgecolor=INK, linewidth=0.5, label='EBITDA')
ax.bar(x, -capex, width=w, color=RUST, edgecolor=INK, linewidth=0.5,
       label='Capital expenditure')
ax.bar(x + w, fcff, width=w, color=GOLD, edgecolor=INK, linewidth=0.5,
       label='Free cash flow to the firm')
for i in range(len(YEARS)):
    ax.text(i + w, fcff[i] + (180 if fcff[i] >= 0 else -420), f"{fcff[i]:,.0f}",
            ha='center', va='bottom' if fcff[i] >= 0 else 'top', fontsize=8.4, color=INK)
ax.axhline(0, color=GREY, lw=0.9)
ax.set_xticks(x); ax.set_xticklabels(YEARS, fontsize=9)
ax.set_ylabel('EGP million')
ax.set_ylim(-5200, 7600)
ax.legend(loc='upper right', frameon=False, fontsize=8.8)
ax.set_title('The explicit window is a construction window', pad=12, fontsize=11.5)
style(ax); ax.grid(axis='x', visible=False)
save(fig, 'fig4_cashflow.png')

# ---- F5: the crux, in observable units --------------------------------------
fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=110)
G = np.array(GRIDJ['grid'])
im = ax.imshow(G, cmap='YlGnBu_r', aspect='auto', origin='lower')
for i in range(G.shape[0]):
    for j in range(G.shape[1]):
        v = G[i, j]
        ax.text(j, i, f"{v:,.2f}", ha='center', va='center', fontsize=9.2,
                color='#0F2B45' if v > G.mean() else CREAM, fontweight='bold')
ax.set_xticks(range(len(GRIDJ['waccs'])))
ax.set_xticklabels([f"{w*100:.1f}%" for w in GRIDJ['waccs']], fontsize=9)
ax.set_yticks(range(len(GRIDJ['prices'])))
ax.set_yticklabels([f"US$ {p:,.0f}/t" for p in GRIDJ['prices']], fontsize=9)
ax.set_xlabel('Terminal cost of capital (nominal Egyptian pounds)')
ax.set_ylabel('Long-run export urea price, free on board Egypt')
ax.set_title('The crux, in observable units: value per share (EGP)', pad=12, fontsize=11.5)
ax.grid(visible=False)
save(fig, 'fig5_crux.png')

# ---- F6: cost stack per tonne of urea ---------------------------------------
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
r0 = rows[0]
per_t = [('Natural gas', r0['gas_cost'] / r0['urea_t'] * 1e6, GOLD),
         ('Other materials', r0['other_mat'] / r0['urea_t'] * 1e6, BRASS),
         ('Depreciation', r0['dep'] / r0['urea_t'] * 1e6, SAGE),
         ('Inland freight to port', r0['freight'] / r0['urea_t'] * 1e6, CANVAS),
         ('Wages and services',
          (r0['wages'] + r0['services']) / r0['urea_t'] * 1e6, GREY),
         ('Administration and other',
          (r0['admin'] + r0['other_sell'] + r0['abnormal']) / r0['urea_t'] * 1e6, RUST)]
labs = [p[0] for p in per_t]; vals = [p[1] for p in per_t]; cols2 = [p[2] for p in per_t]
bars = ax.barh(range(len(per_t)), vals, color=cols2, edgecolor=INK, linewidth=0.6, height=0.6)
for i, v in enumerate(vals):
    ax.text(v + 90, i, f"EGP {v:,.0f}/t", va='center', fontsize=9, color=INK,
            fontweight='bold')
ax.set_yticks(range(len(per_t))); ax.set_yticklabels(labs, fontsize=9)
ax.set_xlabel('Cost per tonne of urea, FY2026/27 (Egyptian pounds)')
ax.set_xlim(0, max(vals) * 1.34)
ax.set_title('Where a tonne of urea costs its money', pad=12, fontsize=11.5)
style(ax); ax.grid(axis='y', visible=False)
save(fig, 'fig6_coststack.png')

# ---- F7: the discount-rate glide --------------------------------------------
fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=110)
wacc = [w * 100 for w in DR['wacc_path']] + [DR['wacc_terminal'] * 100]
xs = list(range(len(wacc)))
ax.plot(xs, wacc, color=CANVAS, lw=2.2, marker='o', markersize=6,
        markerfacecolor=GOLD, markeredgecolor=CANVAS, label='Weighted average cost of capital')
rf = [r * 100 for r in DR['rf_star_path']] + [DR['rf_star_terminal'] * 100]
ax.plot(xs, rf, color=BRASS, lw=1.6, ls='--', marker='s', markersize=4.5,
        label='Normalised risk-free rate')
ax.axhline(DR['implied_wacc_base'] * 100, color=RUST, lw=1.6, ls=':')
ax.text(0.06, DR['implied_wacc_base'] * 100 + 0.55,
        f"rate implied by the market price, {DR['implied_wacc_base']*100:.1f}%",
        fontsize=9, color=RUST, fontweight='bold')
for i, v in enumerate(wacc):
    ax.text(i, v + 0.55, f"{v:.1f}%", ha='center', fontsize=8.8, color=INK)
ax.set_xticks(xs); ax.set_xticklabels(YEARS + ['Terminal'], fontsize=8.8)
ax.set_ylabel('Per cent, nominal Egyptian pounds')
ax.set_ylim(7, 28)
ax.legend(loc='upper right', frameon=False, fontsize=8.8)
ax.set_title('The discount rate glides to a terminal rate built from its own components',
             pad=12, fontsize=11.5)
style(ax); ax.grid(axis='x', visible=False)
save(fig, 'fig7_glide.png')

# ---- F8: price history -------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.8, 4.0), dpi=110)
d5 = df[df['Date'] >= df['Date'].max() - np.timedelta64(365 * 5, 'D')]
ax.plot(d5['Date'], d5['Price'], color=CANVAS, lw=1.3)
ax.axhline(SPOT, color=GOLD, lw=1.2, ls='--')
ax.text(d5['Date'].iloc[int(len(d5) * 0.03)], SPOT + 0.5,
        # DERIVED, NOT TYPED [FIXED 03-Sep-2026]: this read "6 August 2026" against the
        # study's own committed spot_date of 2026-09-03 — twenty-eight days stale, on a
        # figure whose price is computed from that very spot.
        f"{SPOT_DATE_WORDS} close, EGP {SPOT:,.2f}", fontsize=9, color=BRASS,
        fontweight='bold')
ax.set_ylabel('Share price (Egyptian pounds)')
ax.set_title('Five years of the traded price', pad=12, fontsize=11.5)
style(ax)
save(fig, 'fig8_price.png')

# ---- D1: expert appendix comparison -----------------------------------------
EX = json.load(open(os.path.join(HERE, 'experts.json')))
fig, ax = plt.subplots(figsize=(9.8, 3.8), dpi=110)
ex = [(f"Expert 1 — {EX['e1']['title']}", EX['e1']['low'], EX['e1']['high']),
      (f"Expert 2 — {EX['e2']['title']}", EX['e2']['low'], EX['e2']['high']),
      (f"Expert 3 — {EX['e3']['title']}", EX['e3']['low'], EX['e3']['high'])]
for i, (lab, lo, hi) in enumerate(ex):
    ax.barh(i, hi - lo, left=lo, height=0.46, color=[GOLD, BRASS, SAGE][i],
            edgecolor=INK, linewidth=0.6)
    ax.text(hi + 0.16, i, f"EGP {lo:,.2f} – {hi:,.2f}", va='center', fontsize=9,
            color=INK, fontweight='bold')
ax.axvline(SPOT, color=CANVAS, lw=1.8, ls='--')
# the label sat above the top bar and struck through the title; it now sits beside the
# rule at mid-height, inside the plot, where nothing else is drawn
ax.text(SPOT - 0.25, 1.0, f"market price\nEGP {SPOT:,.2f}", ha='right', va='center',
        fontsize=9, color=CANVAS, fontweight='bold')
ax.set_yticks(range(3)); ax.set_yticklabels([e[0] for e in ex], fontsize=8.8)
ax.set_xlabel('Value per share (Egyptian pounds)')
ax.set_xlim(-0.4, SPOT * 1.14)
ax.set_title('Three independent methods, three different answers', pad=12, fontsize=11.5)
style(ax); ax.grid(axis='y', visible=False)
save(fig, 'figD1_experts.png')

# ---- F9: the four-lens field, as a SPAN per lens -----------------------------
# The earlier version of this chart drew one bar per lens at its central value. A point
# per lens hides the thing the reader most needs, which is how wide each lens is before
# any of them is compared with another. Every bar is now the lens's own bear-to-bull
# span with the central marked, on the same axis as the traded price.
ALT = json.load(open(os.path.join(HERE, 'alternatives.json')))
SPANS = ALT['spans']
order9 = ['cashflow_carry', 'cashflow_stopped', 'book', 'relative', 'normalised']
fig, ax = plt.subplots(figsize=(9.8, 4.4), dpi=110)
cols9 = {'cashflow_carry': RUST, 'cashflow_stopped': CANVAS, 'book': GREY,
         'relative': GOLD, 'normalised': SAGE}
for i, k in enumerate(order9[::-1]):
    sp = SPANS[k]
    lo, hi, ba = sp['low'], sp['high'], sp['base']
    c = cols9[k]
    if hi > lo:
        ax.barh(i, hi - lo, left=lo, height=0.46, color=c, alpha=0.42,
                edgecolor=c, linewidth=1.2)
    ax.plot([ba, ba], [i - 0.24, i + 0.24], color=c, lw=3.4)
    # the widest span's label runs past the market-price rule; an opaque backing box
    # keeps the rule from striking through the text instead of moving the label
    ax.text(max(hi, ba) + 0.28, i,
            (f"{lo:,.2f} to {hi:,.2f} · central {ba:,.2f}" if hi > lo
             else f"{ba:,.2f}"),
            va='center', ha='left', fontsize=8.8, color=INK, zorder=6,
            bbox=dict(facecolor=BG, edgecolor='none', pad=1.4))
ax.axvline(0, color=GREY, lw=0.9)
ax.axvline(SPOT, color=CANVAS, lw=1.8, ls='--')
ax.text(SPOT - 0.28, 2.0, f"market price\nEGP {SPOT:,.2f}", ha='right', va='center',
        fontsize=9, color=CANVAS, fontweight='bold')
ax.set_yticks(range(len(order9)))
ax.set_yticklabels([SPANS[k]['label'].replace(" — ", "\n") for k in order9[::-1]],
                   fontsize=8.4)
ax.set_xlabel('Value per share (Egyptian pounds)')
ax.set_xlim(-4.2, max(SPOT * 1.16, max(SPANS[k]['high'] for k in order9) + 7.5))
ax.set_ylim(-0.7, len(order9) - 0.3)
ax.set_title('Four lenses, one field — each lens as its own bear-to-bull span',
             pad=12, fontsize=11.5)
style(ax); ax.grid(axis='y', visible=False)
save(fig, 'fig9_field.png')

# ---- F12/F13: the two price distributions ------------------------------------
# The cone in F10 shows the middle of the distribution over time. It cannot show the
# SHAPE of the distribution at the check date, which is what a reader needs in order to
# see that the tail is not symmetric. One figure per horizon, on the same construction.
ST_ = json.load(open(os.path.join(HERE, 'strike_result.json')))
for tag, fn, out in [('one month', 'paths_1M.npy', 'fig12_dist1m.png'),
                     ('three months', 'paths_3M.npy', 'fig13_dist3m.png')]:
    hz = ST_['horizons']['1M' if tag == 'one month' else '3M']
    x = np.load(os.path.join(HERE, fn))[:, -1]
    fig, ax = plt.subplots(figsize=(9.4, 3.6), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.92, edgecolor=BG, linewidth=0.2)
    # the percentiles are READ FROM THE STRIKE RESULT, never recomputed here: a figure
    # that recomputes its own quantiles will disagree with the table beside it in the
    # second decimal, and it did
    med = hz['pct']['p50']
    ax.axvline(CONE_ANCHOR, color=CANVAS, lw=1.7)
    ax.axvline(med, color=RUST, lw=1.7, ls='--')
    yl = ax.get_ylim()[1]
    ax.set_ylim(0, yl * 1.22)                    # headroom so no label sits on a bar
    yl = ax.get_ylim()[1]
    ax.text(CONE_ANCHOR, yl * 0.99, f"anchor {CONE_ANCHOR:,.2f} ", color=CANVAS,
            fontsize=8.6,
            ha='right', va='top', fontweight='bold')
    ax.text(med, yl * 0.90, f" median {med:,.2f}", color=RUST, fontsize=8.6,
            ha='left', va='top', fontweight='bold')
    for q, lab in (('p5', 'P5'), ('p95', 'P95')):
        v = hz['pct'][q]
        ax.axvline(v, color=GREY, lw=0.9, ls=':')
        ax.text(v, yl * 0.70, f" {lab} {v:,.2f}" if q == 'p95' else f"{lab} {v:,.2f} ",
                color=GREY, fontsize=8.0, ha='left' if q == 'p95' else 'right', va='top')
    ax.set_xlim(float(np.percentile(x, 0.3)), float(np.percentile(x, 99.7)))
    ax.set_xlabel('Share price at the check date (Egyptian pounds)')
    ax.set_yticks([])
    ax.set_title(f"The distribution of the price at {tag}, to {hz['grade_date']}",
                 pad=10, fontsize=11.5)
    style(ax); ax.grid(axis='y', visible=False)
    save(fig, out)

# ---- F14: the capital programme, in its own units ----------------------------
PRG = ALT['programme']
fig, (axa, axb) = plt.subplots(1, 2, figsize=(9.8, 3.7), dpi=110,
                               gridspec_kw={'width_ratios': [1.0, 1.0]})
bars = [('Money spent', PRG['spent_pct'] * 100, BRASS),
        ('Physical progress', PRG['progress'] * 100, RUST),
        ('Progress planned', PRG['plan'] * 100, SAGE)]
for i, (lab, v, c) in enumerate(bars):
    axa.bar(i, v, width=0.56, color=c, edgecolor=INK, linewidth=0.6)
    axa.text(i, v + 1.2, f"{v:.1f}%", ha='center', fontsize=9.2, color=INK,
             fontweight='bold')
axa.set_xticks(range(len(bars)))
axa.set_xticklabels([b[0] for b in bars], fontsize=8.6)
axa.set_ylabel('Per cent of the approved cost, or of the plan')
axa.set_ylim(0, 46)
axa.set_title('More than a quarter of the money, an eighth of the plant',
              fontsize=10.4, pad=9)
style(axa); axa.grid(axis='x', visible=False)

rets = [('Return on the approved cost', PRG['return_on_cost'] * 100, RUST),
        ('Terminal cost of capital', DR['wacc_terminal'] * 100, CANVAS)]
for i, (lab, v, c) in enumerate(rets):
    axb.bar(i, v, width=0.5, color=c, edgecolor=INK, linewidth=0.6)
    axb.text(i, v + 0.6, f"{v:.1f}%", ha='center', fontsize=9.2, color=INK,
             fontweight='bold')
axb.set_xticks(range(len(rets)))
axb.set_xticklabels([r[0].replace(' the ', '\nthe ').replace(' cost of', '\ncost of')
                     for r in rets], fontsize=8.6)
axb.set_ylabel('Per cent')
axb.set_ylim(0, max(DR['wacc_terminal'] * 100, PRG['return_on_cost'] * 100) * 1.28)
axb.set_title('What the new plant earns on what it costs', fontsize=10.4, pad=9)
style(axb); axb.grid(axis='x', visible=False)
save(fig, 'fig14_programme.png')

# ---- F10: the price fan ------------------------------------------------------
ST = json.load(open(os.path.join(HERE, 'strike_result.json')))
p3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
hist = df.tail(120)
ax.plot(range(-len(hist), 0), hist['Price'].to_numpy(), color=CANVAS, lw=1.3,
        label='Traded price')
steps = np.arange(p3.shape[1])
for lo, hi, col, lab in [(5, 95, '#E6EDEB', '90% of simulated paths'),
                         (25, 75, '#C4D3CF', '50% of simulated paths')]:
    ax.fill_between(steps, np.percentile(p3, lo, axis=0), np.percentile(p3, hi, axis=0),
                    color=col, linewidth=0, label=lab)
ax.plot(steps, np.percentile(p3, 50, axis=0), color=BRASS, lw=1.6, label='Median path')
ax.axhline(CONE_ANCHOR, color=GOLD, lw=1.1, ls='--')
ax.text(-len(hist) + 3, CONE_ANCHOR + 0.55, f"anchor EGP {CONE_ANCHOR:,.2f}", fontsize=8.8,
        color=BRASS, fontweight='bold')
for p, v in ST['horizons']['3M']['pct'].items():
    ax.text(p3.shape[1] + 1.5, v, f"{p.upper()}  {v:,.2f}", fontsize=8.4, color=INK,
            va='center')
ax.set_xlim(-len(hist), p3.shape[1] + 16)
ax.set_ylabel('Share price (Egyptian pounds)')
ax.set_xlabel('Trading sessions — past to the left of zero, simulated to the right')
ax.legend(loc='upper left', frameon=False, fontsize=8.6)
ax.set_title(f"Where the price may go by {ST['horizons']['3M']['grade_date']} — "
             f"fifty thousand simulated paths", pad=12, fontsize=11.5)
style(ax)
save(fig, 'fig10_fan.png')

# ---- F11: the technical read -------------------------------------------------
TC = json.load(open(os.path.join(HERE, 'technicals.json')))
fig, ax = plt.subplots(figsize=(9.8, 4.2), dpi=110)
d2 = df.tail(320).reset_index(drop=True)
px = d2['Price'].to_numpy()
ax.plot(d2['Date'], px, color=CANVAS, lw=1.3, label='Close')
for wdw, col, ls in [(20, GOLD, '-'), (50, BRASS, '--'), (200, SAGE, '-.')]:
    ma = df['Price'].rolling(wdw).mean().tail(320).to_numpy()
    ax.plot(d2['Date'], ma, color=col, lw=1.2, ls=ls, label=f'{wdw}-session average')
# level labels sit at the RIGHT edge, clear of the legend in the upper left; the
# earlier placement put the top resistance label straight through the legend text
for lv in TC['levels']['res']:
    ax.axhline(lv, color=RUST, lw=0.9, ls=':')
    ax.text(d2['Date'].iloc[-1], lv, f" resistance {lv:,.2f}", fontsize=8,
            color=RUST, va='bottom', ha='left')
for lv in TC['levels']['sup']:
    ax.axhline(lv, color=SAGE, lw=0.9, ls=':')
    ax.text(d2['Date'].iloc[-1], lv, f" support {lv:,.2f}", fontsize=8,
            color='#4C6B62', va='bottom', ha='left')
import matplotlib.dates as _md
_span = (d2['Date'].iloc[-1] - d2['Date'].iloc[0])
ax.set_xlim(d2['Date'].iloc[0], d2['Date'].iloc[-1] + _span * 0.13)
ax.set_ylabel('Share price (Egyptian pounds)')
ax.set_ylim(min(TC['levels']['sup']) * 0.93, max(TC['levels']['res']) * 1.05)
# the legend goes BELOW the plot: the level ladder spans the full width, so any
# in-axes position collides with a line or a label
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=4,
          frameon=False, fontsize=8.4)
ax.set_title('Price structure — moving averages and the computed level ladder',
             pad=12, fontsize=11.5)
style(ax)
save(fig, 'fig11_technical.png')
print('all figures written')
