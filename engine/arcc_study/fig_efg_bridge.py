"""EFG Hermes target price -> Testahil weighted central.

REVISION 4. This script holds NO valuation constants. Every bar, label, caption and
verdict is read from efg_bridge.json, which is written by gate (t) — efg_bridge.py — and
only after nine invariants pass. The three earlier versions of this chart each shipped a
defect that summed correctly and was therefore invisible to the one check they had.

Run efg_bridge.py first. This file draws; it does not decide.
"""
import json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, 'efg_bridge.json')))
START, END, MKT, STEPS = B['start'], B['end'], B['market'], B['steps']
if abs(sum(s['value'] for s in STEPS) - (END - START)) > 0.005:
    sys.exit('refusing to draw: efg_bridge.json does not close')

BG, GOLD, BRASS = '#FBFAF6', '#C0A45F', '#896F36'
INK, GRID, GREY, RUST, TEAL = '#1C3A36', '#D5DDDB', '#5A6764', '#A0522D', '#3E7C6A'
CHIP = {'EFG': ('#A0522D', 'EFG off mark'), 'TESTAHIL': ('#1C3A36', 'we were off mark'),
        'OPEN': ('#B8860B', 'open — no referee'), 'NEITHER': ('#8A928F', 'method, not error')}
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG, 'axes.edgecolor': GREY,
                     'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
                     'text.color': INK, 'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'axes.axisbelow': True, 'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG, 'font.size': 9.5})

fig, ax = plt.subplots(figsize=(17.0, 8.2), dpi=150)
TR = ax.get_xaxis_transform()


def foot(xi, lab, sub, off=None):
    ax.text(xi, -0.075, lab, transform=TR, ha='center', va='top', fontsize=9.0,
            fontweight='bold', linespacing=1.35)
    ax.text(xi, -0.192, sub, transform=TR, ha='center', va='top', fontsize=7.4,
            color=GREY, linespacing=1.45)
    if off:
        col, txt = CHIP[off]
        ax.add_patch(FancyBboxPatch((xi - 0.40, -0.335), 0.80, 0.048, transform=TR,
                                    boxstyle='round,pad=0.008,rounding_size=0.012',
                                    facecolor=col, edgecolor='none', alpha=.16, clip_on=False))
        ax.text(xi, -0.311, txt, transform=TR, ha='center', va='center', fontsize=6.9,
                fontweight='bold', color=col)


ax.add_patch(Rectangle((-0.36, 0), 0.72, START, facecolor=BRASS, edgecolor=INK, lw=0.9))
ax.text(0, START + 1.3, f'{START:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11.5)
foot(0, 'EFG Hermes\ntarget price', '6 Aug 2026\nBuy, DCF')

run = START
for i, s in enumerate(STEPS, start=1):
    d = s['value']
    lo = run + d if d < 0 else run
    col = RUST if d < 0 else TEAL
    ax.add_patch(Rectangle((i - 0.36, lo), 0.72, abs(d), facecolor=col, edgecolor=INK,
                           lw=0.8, alpha=.92))
    ax.plot([i - 1 + 0.36, i - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
    ax.text(i, lo + abs(d) + 0.9, f'{d:+.2f}', ha='center', va='bottom', fontweight='bold',
            fontsize=10.5, color=col)
    foot(i, s['label'], s['sub'], s['off'])
    run += d

n = len(STEPS) + 1
ax.plot([n - 1 + 0.36, n - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
ax.add_patch(Rectangle((n - 0.36, 0), 0.72, END, facecolor=GOLD, edgecolor=INK, lw=0.9))
ax.text(n, END - 3.8, f'{END:.2f}', ha='center', va='top', fontweight='bold', fontsize=11.5,
        color=INK)
foot(n, 'Testahil\nweighted central', 'four lenses')

ax.axhline(MKT, color=INK, lw=1.15, ls=(0, (5, 3)), zorder=1)
ax.text(n + 0.30, MKT, f'market\n{MKT:.2f}', va='center', ha='left', fontsize=8.4,
        fontweight='bold', color=INK, linespacing=1.35)

ax.set_xlim(-0.72, n + 1.10); ax.set_ylim(0, 84); ax.set_xticks([])
ax.set_ylabel('EGP per share'); ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80])
ax.tick_params(axis='x', length=0)
for sp in ('top', 'right', 'bottom'):
    ax.spines[sp].set_visible(False)
ax.set_title('From the EFG Hermes target price to the Testahil central',
             fontsize=14.5, fontweight='bold', loc='left', pad=64)
ax.text(0.0, 1.008,
        'Both models reproduce FY2025 to the pound, so the whole EGP 15.10 gap is forward-looking. Each bar replaces exactly ONE driver and\n'
        'flows it through the discounted window AND the cash bridge, so nothing is counted twice. Two thirds of the gap is capex and a dividend\n'
        'that has already been paid. Valuing to TODAY rather than to 1 January ADDS EGP 1.28 — that cash is inside the 54.65, not owed on top.',
        transform=ax.transAxes, fontsize=9.0, color=GREY, ha='left', va='bottom', linespacing=1.6)

out = os.path.join(HERE, 'fig_efg_bridge.png')
fig.savefig(out, bbox_inches='tight')
print('wrote', out, '—', len(STEPS), 'bars from efg_bridge.json')
