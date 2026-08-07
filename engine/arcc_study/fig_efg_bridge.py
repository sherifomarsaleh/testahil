"""Waterfall bridging the EFG Hermes target price to the Testahil weighted central.

Every step is a REAL re-run, not an allocation: each EFG assumption is substituted into
our own waterfall one at a time and the model is re-solved, so the bars sum to the gap
by construction rather than by plugging a residual.
"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
BG, CREAM, GOLD, BRASS = '#FBFAF6', '#F6F1E6', '#C0A45F', '#896F36'
INK, GRID, GREY, RUST, SAGE = '#1C3A36', '#D5DDDB', '#5A6764', '#A0522D', '#9FB0AC'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True, 'axes.axisbelow': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6, 'axes.titlecolor': INK,
                     'savefig.transparent': False, 'savefig.facecolor': BG, 'font.size': 9.5})

START, END = 69.76, 54.65
STEPS = [
    ("Maintenance\ncapex",            -7.63, "USD 4.00/t held\n5-yr 1.5 → 5.6bn"),
    ("Discount\nschedule",            -3.21, "20.1% flat →\n24.5% gliding"),
    ("Terminal\nblock",               -2.38, "replacement-cost\nreinvestment"),
    ("Operating\nbuild",              +2.02, "EBITDA and\nworking capital"),
    ("Net\ncash",                     -3.18, "FY2025 dividend out,\nfresher debt"),
    ("Other three\nlenses",           -0.75, "50/20/22/8\nweighting"),
]

fig, ax = plt.subplots(figsize=(12.2, 6.4), dpi=150)
TR = ax.get_xaxis_transform()          # x in data units, y in axes fraction


def foot(xi, lab, sub):
    ax.text(xi, -0.085, lab, transform=TR, ha='center', va='top',
            fontsize=9.3, fontweight='bold', linespacing=1.35)
    ax.text(xi, -0.205, sub, transform=TR, ha='center', va='top',
            fontsize=7.7, color=GREY, linespacing=1.45)


x = 0
ax.add_patch(Rectangle((x - 0.36, 0), 0.72, START, facecolor=BRASS, edgecolor=INK, lw=0.9))
ax.text(x, START + 1.5, f'{START:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11.5)
foot(x, 'EFG Hermes\ntarget price', '6 Aug 2026\nBuy, DCF')
run = START
for i, (lab, d, sub) in enumerate(STEPS, start=1):
    lo = run + d if d < 0 else run
    col = RUST if d < 0 else '#3E7C6A'
    ax.add_patch(Rectangle((i - 0.36, lo), 0.72, abs(d), facecolor=col, edgecolor=INK, lw=0.8, alpha=.92))
    ax.plot([i - 1 + 0.36, i - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
    ax.text(i, lo + abs(d) + 1.0, f'{d:+.2f}', ha='center', va='bottom',
            fontweight='bold', fontsize=10.5, color=col)
    foot(i, lab, sub)
    run += d
n = len(STEPS) + 1
ax.plot([n - 1 + 0.36, n - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
ax.add_patch(Rectangle((n - 0.36, 0), 0.72, END, facecolor=GOLD, edgecolor=INK, lw=0.9))
ax.text(n, END - 4.2, f'{END:.2f}', ha='center', va='top', fontweight='bold',
        fontsize=11.5, color=INK)
foot(n, 'Testahil\nweighted central', 'four lenses\n50/20/22/8')

# spot line, labelled in clear air above the bars rather than across them
ax.axhline(59.00, color=INK, lw=1.15, ls=(0, (5, 3)), zorder=1)
ax.text(n + 0.28, 59.00, 'market price\n59.00', va='center', ha='left', fontsize=8.8,
        fontweight='bold', color=INK, linespacing=1.35)

ax.set_xlim(-0.72, n + 1.30); ax.set_ylim(0, 84)
ax.set_xticks([]); ax.set_ylabel('EGP per share')
ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80])
ax.tick_params(axis='x', length=0)
for sp in ('top', 'right', 'bottom'):
    ax.spines[sp].set_visible(False)
ax.set_title('From the EFG Hermes target price to the Testahil central',
             fontsize=13, fontweight='bold', loc='left', pad=34)
ax.text(0.0, 1.012, 'Both reproduce FY2025 to the pound \u2014 the whole EGP 15.11 gap is forward-looking.\n'
        'Each bar is a re-run with one EFG assumption substituted, not an allocated residual.',
        transform=ax.transAxes, fontsize=9.2, color=GREY, ha='left', va='bottom', linespacing=1.5)
fig.subplots_adjust(bottom=0.26, top=0.86)
out = os.path.join(HERE, 'fig_efg_bridge.png')
fig.savefig(out, bbox_inches='tight'); print('wrote', out)
