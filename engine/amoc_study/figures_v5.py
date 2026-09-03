"""Figures for AMOC. THIS FILE WRITES FOUR OF THE FIVE FIGURES THE DELIVERED STUDY USES —
fig3_bridge, fig4_adversarial, fig5_spread and fig6_cone — and it is current, not superseded.

THE NAME SAYS v5 AND THE NAME IS MISLEADING, WHICH COST AN HOUR AND IS RECORDED HERE SO IT
DOES NOT AGAIN. It also used to write fig1_football, and so does figures.py; the two
collided on that one filename and this one ran last, so the delivered study carried ITS
football field: the retired 45/20/20/15 blend weights in the row labels, a WEIGHTED RANGE
bar at a central of 11.83 the study had stopped publishing, and a hardcoded x-axis of 2 to
11 against a spot of 13.50, so the price line fell outside the axis and was clipped away
silently while the caption said the price was shown.

The first diagnosis was that this whole file was superseded, and it was WRONG: figures.py
writes nine figures of which the delivered document embeds exactly one, and this file writes
four of the other four. Reading the filename instead of reading what the builder embeds is
how that happened. THE FIX IS THE COLLISION, NOT THE FILE: the fig1 block is gone from here
and figures.py owns it, so the two can both run in any order and neither can overwrite the
other.

Every number is read from study_numbers.json / case_adversarial.json — nothing is retyped.
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
ADV = json.load(open(os.path.join(HERE, 'case_adversarial.json')))
INK, GOLD, GREY, RED = '#1C3A36', '#C0A45F', '#6E7B77', '#8C3B2E'
PANEL = '#EAF0EE'
L = D['lenses']; SPOT = D['spot']; C = D['central']
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': GREY, 'text.color': INK,
                     'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK})

# ---- fig 1 lives in figures.py -------------------------------------------------
# It was written here too, and this file ran last. Two generators, one filename,
# and the older picture won. Removed rather than renamed: a second football field
# under another name would still be a second answer to the same question.

# ---- fig 2: the margin record vs what a buyer at spot must believe -----------
fig, ax = plt.subplots(figsize=(7.4, 3.0))
hist = D['hist_is']
periods = ['6M Dec-2024', '3M Mar-2025', '6M Dec-2025', '3M Mar-2026', '6M Jun-2026']
gm = [hist[p]['gm'] * 100 for p in periods]
fx = [g * 100 for g in D['fcst']['gm']]
x1 = np.arange(len(periods)); x2 = np.arange(len(periods) + 1, len(periods) + 1 + 5)
ax.bar(x1, gm, color=PANEL, edgecolor=INK, lw=0.8, label='Filed record')
ax.bar(len(periods), D['ttm']['gm'] * 100, color=GOLD, edgecolor=INK, lw=0.8,
       label='Base year (TTM to 30-Jun-26)')
ax.bar(x2, fx, color='#CBD9D4', edgecolor=INK, lw=0.8, label='Forecast (output of the build)')
# SOLVED by the model, not typed. The previous edition hardcoded 12.16 here, in the headline
# and in section 1.14, and none of the three moved when the model did.
req = D['gm_required']['level'] * 100
ax.axhline(req, color=RED, lw=1.4, ls='--')
# The annotation sits BELOW its own line and to the right of the legend. Rendered, the
# previous placement put it straight through the legend's first entry and the two were
# unreadable on top of each other; a figure is checked as an image, not as code.
# The required margin now sits INSIDE the bars rather than above them all, so the label goes
# under the axis line's left end where nothing is drawn, not across the forecast columns.
# Placed over the FORECAST columns, which are the shortest bars the line crosses. On the left
# it clipped the two 2026 filed bars, which are the ones a reader most needs to see.
ax.text(len(periods) + 5.4, req + 0.55,
        'required IN PERPETUITY for the market price to be fair: %.2f%%' % req,
        color=RED, fontsize=8.2, ha='right', va='bottom')
ax.set_xticks(list(x1) + [len(periods)] + list(x2))
# The four filed periods are long labels on adjacent ticks and ran into one another.
# Stagger them onto two lines rather than shrinking the type until nobody can read it.
_perlab = [p.replace(' ', '\n') for p in periods]
ax.set_xticklabels(_perlab + ['TTM\nJun-26'] + list(D['fcst']['years']), fontsize=7.4)
ax.set_ylabel('Gross margin, %'); ax.set_ylim(0, max(gm + fx + [req]) + 2.2)
ax.legend(fontsize=7.4, frameon=False, loc='upper left', ncol=3,
          bbox_to_anchor=(0.0, 1.16), borderaxespad=0.0)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_margin.png'), dpi=170)

# ---- fig 3: EV -> equity bridge, per share -----------------------------------
fig, ax = plt.subplots(figsize=(7.4, 3.0))
B = D['bridge']; SH = D['meta']['shares_mn']
steps = [('Enterprise\nvalue', B['ev'] / SH), ('+ net cash', -B['nd'] / SH),
         ('− minority\n(incl. cash)', -B['nci'] / SH), ('− tax-disputes\nprovision', -B['prov'] / SH),
         ('− dividends\npayable', -B['divp'] / SH), ('+ investments\n& pledged', B['inv'] / SH)]
cum = 0; xs = []
for i, (lab, v) in enumerate(steps):
    ax.bar(i, v, bottom=cum, color=(PANEL if v >= 0 else '#E8D5D0'), edgecolor=INK, lw=0.8)
    ax.text(i, cum + v + 0.12 if v >= 0 else cum + 0.12, f'{v:+.2f}', ha='center', fontsize=8)
    cum += v; xs.append(lab)
ax.bar(len(steps), cum, color=GOLD, edgecolor=INK, lw=1.0)
ax.text(len(steps), cum + 0.12, f'{cum:.2f}', ha='center', fontsize=8.5, fontweight='bold')
ax.axhline(SPOT, color=RED, lw=1.2, ls='--')
# the label sat 0.1 above the line on a 0-14 axis, which put it ON the line; it now clears
# it and carries the panel colour behind it
ax.text(5.6, SPOT + 0.34, f'spot {SPOT:.2f}', color=RED, fontsize=8,
        bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'))
ax.set_xticks(range(len(steps) + 1)); ax.set_xticklabels(xs + ['EQUITY\nper share'], fontsize=7.4)
ax.set_ylabel('EGP per share'); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_bridge.png'), dpi=170)

# ---- fig 4: the adversarial stack --------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 3.0))
adv = [('Published central', ADV['base']['central'], GOLD),
       ('no provision', ADV['no_provision']['central'], PANEL),
       ('no dividends payable', ADV['no_divp']['central'], PANEL),
       ("no employees' share", ADV['no_emp']['central'], PANEL),
       ('old terminal rate', ADV['terminal_rf_5pct_target']['central'], PANEL),
       ('effective tax', ADV['effective_tax']['central'], PANEL),
       ('ALL GIVE-BACKS AT ONCE', ADV['ALL_GIVEBACKS']['central'], '#CBD9D4')]
ys = np.arange(len(adv))
for i, (lab, v, col) in enumerate(adv):
    ax.barh(i, v, color=col, edgecolor=INK, lw=0.9)
    # the labels sit past the spot line now that the axis reaches it, so they carry a
    # background and the line goes behind them
    ax.text(v + 0.07, i, f'{v:.2f}  ({v/SPOT-1:+.0%})', va='center', fontsize=8, zorder=4,
            bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none'))
ax.axvline(SPOT, color=RED, lw=1.4, ls='--', zorder=1)
ax.text(SPOT - 0.05, -0.65, f'spot {SPOT:.2f}', color=RED, fontsize=8.5, ha='right')
ax.set_yticks(ys); ax.set_yticklabels([a[0] for a in adv], fontsize=8.3)
ax.invert_yaxis()
# THE LIMIT WAS HARDCODED AT 10.4 AND EVERY BAR HERE IS WORTH MORE THAN THAT. The values
# run 10.86 to 12.74 against a spot of 13.50, so every bar was clipped at the axis edge and
# they ALL RENDERED THE SAME LENGTH — 11.40 indistinguishable from 12.74 — while the spot
# line the caption's whole argument rests on ("not all of them together reaches the price")
# was drawn outside the axis and thrown away. A hardcoded axis limit is a number that stops
# being true the moment the model moves, and it fails SILENTLY: nothing raises, the picture
# renders, and it is wrong in a way only a reader looking at it can see.
ax.set_xlim(0, max(max(v for _, v, _c in adv), SPOT) * 1.10)
ax.set_xlabel('Weighted central, EGP per share')
ax.spines[['top', 'right', 'left']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_adversarial.png'), dpi=170)

# ---- fig 5: spread per tonne by line -----------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 2.8))
UB = D['unitbuild']
ks = [k for k in UB['lines'] if k != 'waste']
sp = [UB['spread'][k] for k in ks]
labs = [UB['labels'][k] for k in ks]
cols = [GOLD if k in ('oils', 'wax') else PANEL for k in ks]
ax.bar(range(len(ks)), sp, color=cols, edgecolor=INK, lw=0.9)
for i, v in enumerate(sp):
    ax.text(i, v + 60, f'{v:,.0f}', ha='center', fontsize=8)
ax.set_xticks(range(len(ks)))
ax.set_xticklabels([l.replace(' ', '\n') for l in labs], fontsize=7.4)
ax.set_ylabel('Gross spread, EGP per tonne')
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig5_spread.png'), dpi=170)

# ---- fig 6: the price cone ---------------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 2.8))
STK = D['strike']
h1, h3 = STK['horizons']['1M'], STK['horizons']['3M']
xs = [0, 1, 3]
for q in ['p5', 'p25', 'p50', 'p75', 'p95']:
    ys = [SPOT, h1['pct'][q], h3['pct'][q]]
    ax.plot(xs, ys, color=INK, lw=0.9 if q != 'p50' else 1.6,
            ls='-' if q == 'p50' else ':')
    ax.text(3.05, ys[-1], f"{q} {ys[-1]:.2f}", fontsize=7.6, va='center')
ax.fill_between(xs, [SPOT, h1['pct']['p5'], h3['pct']['p5']],
                [SPOT, h1['pct']['p95'], h3['pct']['p95']], color=PANEL, alpha=0.6)
ax.axhline(C, color=GOLD, lw=1.4); ax.text(0.05, C - 0.32, f'fair value {C:.2f}', color='#896F36', fontsize=8)
ax.set_xticks(xs); ax.set_xticklabels(['anchor\n06-Aug-26', '1 month', '3 months'], fontsize=8)
ax.set_ylabel('EGP'); ax.set_xlim(-0.1, 3.7)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig6_cone.png'), dpi=170)
print('6 figures written')
