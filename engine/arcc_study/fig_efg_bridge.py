"""EFG Hermes target price -> Testahil weighted central, driver-based.

REVISION 2 OF THIS CHART. The first version substituted line items — it swapped NET CASH
wholesale, which silently carried EFG's capex and margin assumptions into the cash bar on
top of the capex bar that had already counted them. About a pound was double-counted.

This version substitutes DRIVERS, and each driver flows through BOTH the discounted window
and the cash bridge, so nothing is counted twice. It also opens with a step that uses only
EFG's own numbers: their discount factors are 1/(1.2006)^(t-1), which dates their cash
flows to 1 January 2026, but the net cash they add is above the 31-December balance. Put
their balance sheet on the same date as their flows and their own target falls to 67.64.
"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
BG, GOLD, BRASS = '#FBFAF6', '#C0A45F', '#896F36'
INK, GRID, GREY, RUST, TEAL = '#1C3A36', '#D5DDDB', '#5A6764', '#A0522D', '#3E7C6A'
plt.rcParams.update({'figure.facecolor': BG, 'axes.facecolor': BG, 'axes.edgecolor': GREY,
                     'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
                     'text.color': INK, 'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'axes.axisbelow': True, 'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': BG, 'font.size': 9.5})

START, END = 69.76, 54.65
STEPS = [
    ("EFG date\ninconsistency", -2.12, "flows at 1-Jan,\nbalance sheet at Aug"),
    ("Maintenance\ncapex",            -7.63, "5-yr 1.5 → 5.6bn\ntheirs below D&A"),
    ("Operating\nbuild",              +2.44, "our volume up,\nmargin down"),
    ("Terminal\nblock",               -2.38, "reinvestment takes\n56.8% of terminal profit"),
    ("Valuation date\nJan → Aug",     -4.68, "broken out\nbelow"),
    ("Other three\nlenses",           -0.73, "50/20/22/8\nand share count"),
]
INSIDE_5 = [
    ("7 months of FY2026 taken OUT of the discounted window,\nand our glide replaces their flat 20.06%", -3.62),
    ("the same 7 months added back as CASH at face,\nplus treasury income   (+1,729mn)", +4.61),
    ("FY2025 dividend, declared and PAID\nex-date 12 Apr 2026   (−2,002mn)", -5.34),
    ("debt at the reviewed 31-Mar-2026 vintage\nrather than 31-Dec-2025", -0.33),
]

fig = plt.figure(figsize=(14.2, 9.4), dpi=150)
gs = fig.add_gridspec(2, 1, height_ratios=[2.35, 1.0], hspace=0.72)
ax, bx = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
TR = ax.get_xaxis_transform()


def foot(xi, lab, sub):
    ax.text(xi, -0.085, lab, transform=TR, ha='center', va='top', fontsize=9.0,
            fontweight='bold', linespacing=1.35)
    ax.text(xi, -0.215, sub, transform=TR, ha='center', va='top', fontsize=7.5,
            color=GREY, linespacing=1.45)


ax.add_patch(Rectangle((-0.36, 0), 0.72, START, facecolor=BRASS, edgecolor=INK, lw=0.9))
ax.text(0, START + 1.5, f'{START:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11.5)
foot(0, 'EFG Hermes\ntarget price', '6 Aug 2026\nBuy, DCF')
run = START
for i, (lab, d, sub) in enumerate(STEPS, start=1):
    lo = run + d if d < 0 else run
    col = RUST if d < 0 else TEAL
    ax.add_patch(Rectangle((i - 0.36, lo), 0.72, abs(d), facecolor=col, edgecolor=INK, lw=0.8, alpha=.92))
    ax.plot([i - 1 + 0.36, i - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
    ax.text(i, lo + abs(d) + 1.0, f'{d:+.2f}', ha='center', va='bottom', fontweight='bold',
            fontsize=10.5, color=col)
    foot(i, lab, sub)
    run += d
n = len(STEPS) + 1
ax.plot([n - 1 + 0.36, n - 0.36], [run, run], color=GREY, lw=0.9, ls=(0, (3, 3)))
ax.add_patch(Rectangle((n - 0.36, 0), 0.72, END, facecolor=GOLD, edgecolor=INK, lw=0.9))
ax.text(n, END - 4.2, f'{END:.2f}', ha='center', va='top', fontweight='bold', fontsize=11.5, color=INK)
foot(n, 'Testahil\nweighted central', 'four lenses')
ax.axhline(59.00, color=INK, lw=1.15, ls=(0, (5, 3)), zorder=1)
ax.text(n + 0.30, 59.00, 'market price\n59.00', va='center', ha='left', fontsize=8.6,
        fontweight='bold', color=INK, linespacing=1.35)
ax.set_xlim(-0.72, n + 1.28); ax.set_ylim(0, 84); ax.set_xticks([])
ax.set_ylabel('EGP per share'); ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80])
ax.tick_params(axis='x', length=0)
for sp in ('top', 'right', 'bottom'):
    ax.spines[sp].set_visible(False)
ax.set_title('From the EFG Hermes target price to the Testahil central',
             fontsize=14, fontweight='bold', loc='left', pad=48)
ax.text(0.0, 1.015, 'Both reproduce FY2025 to the pound — the whole EGP 15.11 gap is forward-looking. Each bar substitutes\n'
        'one DRIVER and flows it through the discounted window AND the cash bridge, so nothing is counted twice.',
        transform=ax.transAxes, fontsize=9.2, color=GREY, ha='left', va='bottom', linespacing=1.6)

# ---- inset: what is inside the date move -----------------------------------
ys = range(len(INSIDE_5))[::-1]
for y, (lab, v) in zip(ys, INSIDE_5):
    bx.barh(y, v, height=0.46, color=(TEAL if v > 0 else RUST), edgecolor=INK, lw=0.7, alpha=.92)
    bx.text(v + (0.16 if v > 0 else -0.16), y, f'{v:+.2f}', va='center',
            ha='left' if v > 0 else 'right', fontsize=9.2, fontweight='bold',
            color=(TEAL if v > 0 else RUST))
    bx.text(-13.6, y, lab, va='center', ha='left', fontsize=8.4, color=INK, linespacing=1.45)
bx.axvline(0, color=INK, lw=1.0)
bx.set_xlim(-13.7, 5.6); bx.set_ylim(-0.72, len(INSIDE_5) - 0.28)
bx.set_yticks([]); bx.set_xlabel('EGP per share'); bx.set_xticks([-6,-4,-2,0,2,4])
bx.grid(axis='y', visible=False)
for sp in ('top', 'right', 'left'):
    bx.spines[sp].set_visible(False)
bx.set_title('Inside the date move (−4.68) — the two halves of one adjustment, and the dividend',
             fontsize=10.5, fontweight='bold', loc='left', pad=10)
out = os.path.join(HERE, 'fig_efg_bridge.png')
fig.savefig(out, bbox_inches='tight'); print('wrote', out)
