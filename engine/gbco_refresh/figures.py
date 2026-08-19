"""GBCO refresh — study figures. Reads study_numbers.json only. Solid light canvas,
zero transparency, ink text; every figure inspected as a rendered image after build."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))

INK = '#1C3A36'; GREY = '#6E7B77'; GOLD = '#C0A45F'; BRASS = '#896F36'
CREAM = '#F6F1E6'; PANEL = '#EAF0EE'; RED = '#8C3B2E'; BLUE = '#2E5A8C'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.color': INK,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'figure.dpi': 160})

def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor('white'); ax.set_facecolor('white')
    return fig, ax

spot = D['spot']

# ---- fig 1: football field — both framings carried side by side ----------------------
L = D['lenses']; BW = D['both_ways']
rowsA = [
    ("Sum of the parts — round mark", BW['A']['sotp_bear'], BW['A']['sotp'], BW['A']['sotp_bull'], GOLD),
    ("Sum of the parts — balance-sheet mark", BW['B']['sotp_bear'], BW['B']['sotp'], BW['B']['sotp_bull'], BRASS),
    ("Book value & sustainable return", L['book']['bear'], L['book']['base'], L['book']['bull'], BLUE),
    ("Relative multiples", L['relative']['bear'], L['relative']['base'], L['relative']['bull'], GREY),
    ("Normalised earnings power", L['normalized']['bear'], L['normalized']['base'], L['normalized']['bull'], RED),
    ("Weighted central — round mark", L['central']['bear'], L['central']['A'], L['central']['bull'], INK),
    ("Weighted central — balance-sheet mark", L['central']['bear'], L['central']['B'], L['central']['bull'], '#3E5C58'),
]
fig, ax = canvas(9.4, 4.6)
for i, (name, lo, mid, hi, col) in enumerate(rowsA[::-1]):
    y = i
    ax.barh(y, hi-lo, left=lo, height=0.52, color=PANEL, edgecolor=col, linewidth=1.4)
    ax.plot([mid, mid], [y-0.26, y+0.26], color=col, linewidth=3.2)
    ax.text(hi+0.8, y, f"{mid:.1f}", va='center', ha='left', fontsize=9, color=col, fontweight='bold')
    ax.text(lo-0.8, y, f"{lo:.0f}–{hi:.0f}", va='center', ha='right', fontsize=7.6, color=GREY)
ax.axvline(spot, color=RED, linewidth=1.2, linestyle='--')
ax.text(spot+0.6, 0.02, f"last close {spot:.2f} (22 Jul)", fontsize=8, color=RED,
        ha='left', va='bottom')
ax.set_yticks(range(len(rowsA))); ax.set_yticklabels([r[0] for r in rowsA[::-1]], fontsize=8.6)
ax.set_xlabel("EGP per share", fontsize=9); ax.set_xlim(0, 62)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title("Where the value sits — every lens, with the contested stake shown both ways",
             fontsize=11, fontweight='bold', loc='left', pad=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig1_football.png'), facecolor='white'); plt.close(fig)

# ---- fig 2: sensitivity heatmap — stake mark x holding discount ----------------------
S = D['sens']; T = np.array(S['table'])
fig, ax = canvas(7.6, 4.4)
im = ax.imshow(T, cmap='YlGn', aspect='auto')
vmid = T.min() + 0.72*(T.max()-T.min())
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        ax.text(j, i, f"{T[i, j]:.1f}", ha='center', va='center', fontsize=9.5,
                color=('white' if T[i, j] > vmid else INK),
                fontweight='bold' if (S['grid_mult'][i] == 1.0 and S['grid_disc'][j] == 0.10) else 'normal')
ax.set_xticks(range(len(S['grid_disc'])))
ax.set_xticklabels([f"{d*100:.0f}%" for d in S['grid_disc']], fontsize=9)
ax.set_yticks(range(len(S['grid_mult'])))
ax.set_yticklabels([f"{m*100:.0f}% of round" for m in S['grid_mult']], fontsize=9)
ax.set_xlabel("holding-company discount", fontsize=9.5)
ax.set_ylabel("MNT-Halan stake marked at…", fontsize=9.5)
mB = S['mult_B']
yB = float(np.interp(mB, S['grid_mult'], range(len(S['grid_mult']))))
ax.axhline(yB, color=RED, linewidth=1.6, linestyle='--')
ax.text(len(S['grid_disc'])-0.55, yB+0.30,
        f"the company's own book mark sits here ({mB*100:.0f}% of the round)",
        fontsize=8, color=RED, ha='right', va='top',
        bbox=dict(facecolor='white', edgecolor='none', pad=1.5))
ax.set_title("Sum-of-the-parts per share across the two live judgements (EGP)",
             fontsize=11, fontweight='bold', loc='left', pad=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig2_sens.png'), facecolor='white'); plt.close(fig)

# ---- fig 3: revenue by line of business, FY23 -> FY30E -------------------------------
H = D['hist']; lob = D['lob']
years = ['FY23', 'FY24', 'FY25'] + list(lob.keys())
keys = [('pc_r', 'Passenger cars', GOLD), ('cv_r', 'Commercial vehicles & equipment', BLUE),
        ('lm_r', 'Two-, three- & four-wheelers', RED), ('tr_r', 'Tires & parts trading', GREY),
        ('oth_r', 'Other automotive', BRASS)]
fig, ax = canvas(9.4, 4.3)
bottom = np.zeros(len(years))
for k, label, col in keys:
    vals = np.array([H[y][k] for y in ['FY23', 'FY24', 'FY25']] + [lob[y][k] for y in lob]) / 1000.0
    ax.bar(years, vals, bottom=bottom, color=col, edgecolor='white', linewidth=0.6, label=label)
    bottom += vals
for i, y in enumerate(years):
    ax.text(i, bottom[i]+1.2, f"{bottom[i]:.0f}", ha='center', fontsize=8.6, color=INK, fontweight='bold')
ax.axvline(2.5, color=GREY, linewidth=0.9, linestyle=':')
ax.text(2.56, ax.get_ylim()[1]*0.97, "history | forecast", fontsize=8, color=GREY, va='top')
ax.set_ylabel("automotive revenue, EGP bn", fontsize=9.5)
ax.legend(fontsize=8, loc='upper left', frameon=False)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title("The automotive build: every line grown on its own volumes and prices",
             fontsize=11, fontweight='bold', loc='left', pad=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig3_drivers.png'), facecolor='white'); plt.close(fig)

# ---- fig 4: scorecard — what H1 said about the last forecast -------------------------
V = [v for v in D['variance'] if v.get('h1_share_fy25')]
fig, ax = canvas(9.4, 3.9)
names = [v['line'] for v in V]
dev = [v['deviation']*100 for v in V]
cols = [RED if abs(d) > 5 else '#4E7A46' for d in dev]
ax.barh(range(len(V))[::-1], dev, color=cols, height=0.55, edgecolor='white')
for i, d in enumerate(dev):
    ax.text(d + (1.2 if d >= 0 else -1.2), len(V)-1-i, f"{d:+.0f}%", va='center',
            ha='left' if d >= 0 else 'right', fontsize=9, color=INK, fontweight='bold')
ax.axvline(0, color=INK, linewidth=1)
for x in (-5, 5):
    ax.axvline(x, color=GREY, linewidth=0.8, linestyle=':')
ax.set_yticks(range(len(V))[::-1]); ax.set_yticklabels(names, fontsize=9)
ax.set_xlabel("first-half pace vs the July study's full-year forecast (seasonally adjusted), %",
              fontsize=9)
ax.set_xlim(-40, 47)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title("Scoring the July forecast against the first half that actually printed",
             fontsize=11, fontweight='bold', loc='left', pad=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'fig4_variance.png'), facecolor='white'); plt.close(fig)

# ---- fig D1: the three experts -------------------------------------------------------
E = D['experts']
fig, ax = canvas(8.6, 3.0)
rows = [("Expert 1 — sum-of-the-parts practitioner", E['e1']['rng'][0], E['e1']['base'], E['e1']['rng'][1], GOLD),
        ("Expert 2 — normalised-earnings conservative", E['e2']['rng'][0], E['e2']['base'], E['e2']['rng'][1], BLUE),
        ("Expert 3 — returns-on-capital sceptic", E['e3']['base']*0.82, E['e3']['base'], E['e3']['base']*1.15, RED)]
for i, (name, lo, mid, hi, col) in enumerate(rows[::-1]):
    ax.barh(i, hi-lo, left=lo, height=0.45, color=PANEL, edgecolor=col, linewidth=1.4)
    ax.plot([mid, mid], [i-0.22, i+0.22], color=col, linewidth=3)
    ax.text(hi+0.7, i, f"{mid:.1f}", va='center', fontsize=9.5, color=col, fontweight='bold')
ax.axvline(spot, color=RED, linewidth=1.1, linestyle='--')
ax.text(spot+0.5, -0.42, f"last close {spot:.2f}", fontsize=8, color=RED, ha='left', va='bottom')
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=8.8)
ax.set_xlabel("EGP per share", fontsize=9); ax.set_xlim(0, 62)
ax.spines[['top', 'right']].set_visible(False)
ax.set_title("Three independent readings of the same company", fontsize=11,
             fontweight='bold', loc='left', pad=10)
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'figD1_experts.png'), facecolor='white'); plt.close(fig)

# transparency check — every figure fully opaque on a light canvas
from PIL import Image
for f in ['fig1_football.png', 'fig2_sens.png', 'fig3_drivers.png', 'fig4_variance.png',
          'figD1_experts.png']:
    im = Image.open(os.path.join(HERE, f))
    assert im.mode in ('RGB', 'RGBA')
    if im.mode == 'RGBA':
        alpha = np.array(im)[:, :, 3]
        assert alpha.min() == 255, f"{f} carries transparency"
    corner = np.array(im.convert('RGB'))[2, 2]
    assert corner.mean() > 235, f"{f} canvas not light"
    print(f, im.size, "opaque-light OK")
print("figures built")
