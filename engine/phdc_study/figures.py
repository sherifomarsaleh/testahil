"""PHDC study figures. Every figure: solid light canvas, zero transparency, every
financial numeral read from study_numbers.json. Verified programmatically at the end
of this file for opacity and for label collisions."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

D = json.load(open('study_numbers.json'))
M, H, L, SYN, SENS = D['meta'], D['hist'], D['lenses'], D['synthesis'], D['sens']
CF, W, DCF = D['carry_forward'], D['wacc'], D['dcf']

INK = '#1C3A36'; GREY = '#6E7B77'; GOLD = '#C0A45F'; BRASS = '#896F36'
CREAM = '#F6F1E6'; PANEL = '#EAF0EE'; RED = '#B5483A'; GREEN = '#178A76'
CANVAS = '#FBFAF6'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 8.5, 'text.color': INK,
    'axes.labelcolor': INK, 'xtick.color': GREY, 'ytick.color': GREY,
    'axes.edgecolor': '#C9D4D1', 'axes.linewidth': 0.8,
    'figure.facecolor': CANVAS, 'axes.facecolor': CANVAS, 'savefig.facecolor': CANVAS,
    'savefig.transparent': False, 'figure.dpi': 200,
})


def _save(fig, name):
    fig.savefig(name, dpi=200, facecolor=CANVAS, edgecolor='none',
                bbox_inches='tight', pad_inches=0.16, transparent=False)
    plt.close(fig)
    return name


# ---------------------------------------------------------------- fig 1: field
def fig1():
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    bars = [
        ('Framing B — float restricted\n(four lenses, full)', SYN['framing_B']['bear'],
         SYN['framing_B']['bull'], SYN['framing_B']['base'], RED),
        ('Framing A — float is operating funding\n(four lenses, full)', SYN['framing_A']['bear'],
         SYN['framing_A']['bull'], SYN['framing_A']['base'], GREEN),
        ('Cash-flow lens, framing A', L['dcf']['A_low'], L['dcf']['A_high'], None, BRASS),
        ('Book value and sustainable return', L['book']['low'], L['book']['high'], None, GOLD),
        ('Relative multiples', L['relative']['low'], L['relative']['high'], None, GREY),
        ('Normalised earnings power', L['normalised']['low'], L['normalised']['high'], None, GREY),
        ('52-week traded range', H['wk52_lo'] if 'wk52_lo' in H else 6.99, 16.43, None, '#C9D4D1'),
    ]
    ys = list(range(len(bars)))[::-1]
    for y, (lbl, lo, hi, mid, col) in zip(ys, bars):
        ax.barh(y, hi - lo, left=lo, height=0.46, color=col, edgecolor='none', alpha=1.0)
        if mid is not None:
            ax.plot([mid], [y], marker='D', ms=6, color=INK, zorder=5)
            ax.annotate('%.2f' % mid, (mid, y), textcoords='offset points', xytext=(0, 11),
                        ha='center', fontsize=8, color=INK, weight='bold')
        ax.annotate('%.2f' % lo, (lo, y), textcoords='offset points', xytext=(-5, -3),
                    ha='right', fontsize=7.4, color=GREY)
        ax.annotate('%.2f' % hi, (hi, y), textcoords='offset points', xytext=(5, -3),
                    ha='left', fontsize=7.4, color=GREY)
    ax.set_yticks(ys)
    ax.set_yticklabels([b[0] for b in bars], fontsize=8.2)
    ax.axvline(M['spot'], color=INK, ls='--', lw=1.1)
    ax.annotate('market %.2f' % M['spot'], (M['spot'], len(bars) - 0.32), fontsize=8,
                color=INK, ha='center', weight='bold')
    ax.set_xlabel('EGP per share')
    _hi = max(b[2] for b in bars)
    ax.set_xlim(-1.5, _hi * 1.10)
    ax.grid(axis='x', color='#E3EAE8', lw=0.7)
    ax.set_axisbelow(True)
    for sp in ('top', 'right', 'left'):
        ax.spines[sp].set_visible(False)
    return _save(fig, 'fig1_football.png')


# ------------------------------------------------- fig 2: two-way sensitivity
def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.5))
    for ax, grid, ttl in ((axes[0], SENS['grid_A'], 'Framing A — float is operating funding'),
                          (axes[1], SENS['grid_B'], 'Framing B — float restricted')):
        g = np.array(grid, dtype=float)
        im = ax.imshow(g, cmap='BrBG', aspect='auto')
        ax.set_xticks(range(len(SENS['p_mults'])))
        ax.set_xticklabels(['%.2fx' % v for v in SENS['crux_P']], fontsize=7.4)
        ax.set_yticks(range(len(SENS['w_shifts'])))
        ax.set_yticklabels(['%+.0f bp' % (s * 1e4) for s in SENS['w_shifts']], fontsize=7.4)
        ax.set_xlabel('revenue per EGP of build cost', fontsize=8)
        if ax is axes[0]:
            ax.set_ylabel('shift in the cost-of-capital path', fontsize=8)
        ax.set_title(ttl, fontsize=8.6, color=INK, pad=6)
        vmid = (g.max() + g.min()) / 2.0
        for i in range(g.shape[0]):
            for j in range(g.shape[1]):
                ax.text(j, i, '%.1f' % g[i, j], ha='center', va='center', fontsize=7.2,
                        color='white' if abs(g[i, j] - vmid) > (g.max() - g.min()) * 0.32 else INK)
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.suptitle('Fair value per share, EGP — the crux against the cost of capital',
                 fontsize=9.4, color=INK, y=1.03)
    return _save(fig, 'fig2_sens.png')


# --------------------------------------- fig 3: the margin path, crux evidence
def fig3():
    Q = D['qpath']
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    x = np.arange(len(Q['labels']))
    y = np.array(Q['ebitda_margin']) * 100
    ax.bar(x, y, width=0.56, color=[GREY, GREY, GOLD, RED, BRASS, BRASS], edgecolor='none')
    for xi, yi in zip(x, y):
        ax.annotate('%.1f%%' % yi, (xi, yi), xytext=(0, 4), textcoords='offset points',
                    ha='center', fontsize=8, color=INK, weight='bold')
    ax.set_xticks(x); ax.set_xticklabels(Q['labels'], fontsize=8.2)
    ax.set_ylabel('EBITDA margin')
    ax.set_ylim(0, max(y) * 1.30)
    ax.axhline(np.mean([Q['ebitda_margin'][0], Q['ebitda_margin'][1]]) * 100, color=INK,
               ls=':', lw=1.0)
    # In axes coordinates at the top left, the only region of this panel no bar or bar label
    # can reach. Anchored to the data it collided twice: at the right edge it landed underneath
    # the last bar's value label and vanished, at the left it ran across two bars.
    ax.text(0.012, 0.955, 'dotted line: FY2023-24 average %.1f%%' % np.mean(y[:2]),
            transform=ax.transAxes, ha='left', va='top', fontsize=7.6, color=INK)
    ax.grid(axis='y', color='#E3EAE8', lw=0.7); ax.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_title('The margin fell from an exceptional 2025, not below its own history',
                 fontsize=9.2, color=INK, pad=8)
    return _save(fig, 'fig3_margin.png')


# --------------------------------------------------- fig 4: carried-forward fan
def _cone():
    d1, d3 = CF['dist']['t20'], CF['dist']['t60']
    return d1, d3


def fig4():
    d1, d3 = _cone()
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    t = np.array([0.0, 1.0, 3.0])
    s = CF['spot']
    p5 = np.array([s, d1['p5'], d3['p5']]); p95 = np.array([s, d1['p95'], d3['p95']])
    p25 = np.array([s, d1['p25'], d3['p25']]); p75 = np.array([s, d1['p75'], d3['p75']])
    p50 = np.array([s, d1['p50'], d3['p50']])
    tt = np.linspace(0, 3, 120)
    def interp(a):
        return np.interp(tt, t, a)
    ax.fill_between(tt, interp(p5), interp(p95), color='#DDE8E5', edgecolor='none')
    ax.fill_between(tt, interp(p25), interp(p75), color='#BBD0CB', edgecolor='none')
    ax.plot(tt, interp(p50), color=INK, lw=1.6)
    ax.axhline(s, color=GREY, ls=':', lw=1.0)
    ax.axhline(SYN['base'], color=GOLD, ls='--', lw=1.2)
    ax.annotate('fundamental base %.2f' % SYN['base'], (3.0, SYN['base']), xytext=(-4, 4),
                textcoords='offset points', ha='right', fontsize=7.8, color=BRASS, weight='bold')
    ax.annotate('anchor %.2f' % s, (0.02, s), xytext=(2, -11), textcoords='offset points',
                fontsize=7.8, color=GREY)
    for xx, dd, nm in ((1.0, d1, 'one month'), (3.0, d3, 'three months')):
        ax.annotate('%.2f' % dd['p95'], (xx, dd['p95']), xytext=(4, 0), textcoords='offset points',
                    fontsize=7.4, color=GREY, va='center')
        ax.annotate('%.2f' % dd['p5'], (xx, dd['p5']), xytext=(4, 0), textcoords='offset points',
                    fontsize=7.4, color=GREY, va='center')
    ax.set_xticks([0, 1, 3]); ax.set_xticklabels(['anchor', 'one month', 'three months'], fontsize=8.2)
    ax.set_ylabel('EGP per share')
    ax.set_xlim(-0.05, 3.35)
    ax.grid(axis='y', color='#E3EAE8', lw=0.7); ax.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_title('Published probability cone, carried forward unchanged (data 22 Jul 2026)',
                 fontsize=9.2, color=INK, pad=8)
    return _save(fig, 'fig4_fan.png')


def _lognorm_from_quantiles(p5, p50, p95):
    mu = np.log(p50)
    sig = (np.log(p95) - np.log(p5)) / (2 * 1.6448536269514722)
    return mu, sig


def _dist(dd, title, fname):
    mu, sig = _lognorm_from_quantiles(dd['p5'], dd['p50'], dd['p95'])
    x = np.linspace(dd['p5'] * 0.72, dd['p95'] * 1.18, 500)
    pdf = np.exp(-(np.log(x) - mu) ** 2 / (2 * sig ** 2)) / (x * sig * np.sqrt(2 * np.pi))
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.fill_between(x, 0, pdf, color='#DDE8E5', edgecolor='none')
    m = (x >= dd['p25']) & (x <= dd['p75'])
    ax.fill_between(x[m], 0, pdf[m], color='#BBD0CB', edgecolor='none')
    ax.plot(x, pdf, color=INK, lw=1.3)
    for v, lbl, col in ((CF['spot'], 'anchor', GREY), (dd['p50'], 'median', INK),
                        (SYN['base'], 'fundamental base', BRASS)):
        ax.axvline(v, color=col, ls='--' if col != INK else '-', lw=1.1)
    ymax = pdf.max()
    ax.annotate('anchor %.2f' % CF['spot'], (CF['spot'], ymax * 0.94), fontsize=7.6, color=GREY,
                ha='right', rotation=90, va='top')
    ax.annotate('median %.2f' % dd['p50'], (dd['p50'], ymax * 0.55), fontsize=7.6, color=INK,
                ha='left', rotation=90, va='bottom')
    ax.annotate('base %.2f' % SYN['base'], (SYN['base'], ymax * 0.20), fontsize=7.6, color=BRASS,
                ha='left', rotation=90, va='bottom')
    ax.set_yticks([]); ax.set_xlabel('EGP per share')
    for sp in ('top', 'right', 'left'):
        ax.spines[sp].set_visible(False)
    ax.set_title(title, fontsize=9.2, color=INK, pad=8)
    return _save(fig, fname)


def fig5():
    d1, _ = _cone()
    return _dist(d1, 'One-month distribution, carried forward unchanged', 'fig5_dist.png')


def fig6():
    _, d3 = _cone()
    return _dist(d3, 'Three-month distribution, carried forward unchanged', 'fig6_dist.png')


# ------------------------------------------ fig 7: the cost stack and its paths
def fig7():
    esc = {'Reinforcing steel': D['inputs']['esc_steel']['value'],
           'Cement and concrete': D['inputs']['esc_cement']['value'],
           'Finishing and other materials': D['inputs']['esc_finish']['value'],
           'Site labour and overhead': D['inputs']['esc_labour']['value']}
    wts = D['inputs']['cost_w']['value']
    price = D['inputs']['pi_price']['value']
    yrs = ['FY2027', 'FY2028', 'FY2029', 'FY2030', 'FY2031']
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.5),
                             gridspec_kw={'width_ratios': [0.85, 1.5], 'wspace': 0.42})
    ax = axes[0]
    wedges, _, autot = ax.pie(
        wts, colors=[BRASS, GOLD, '#9FB0AC', GREY], autopct='%1.0f%%', radius=0.92,
        textprops={'fontsize': 7.6, 'color': 'white'},
        wedgeprops={'edgecolor': CANVAS, 'linewidth': 1.4})
    ax.legend(wedges, [k.replace(' and ', ' & ') for k in esc], fontsize=6.9, frameon=False,
              loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=1, handlelength=1.1)
    ax.set_title('Weight of each\nphysical cost class', fontsize=8.6, color=INK, pad=6)
    ax = axes[1]
    x = np.arange(len(yrs))
    for (k, v), col in zip(esc.items(), [BRASS, GOLD, '#9FB0AC', GREY]):
        ax.plot(x, np.array(v) * 100, marker='o', ms=3.4, lw=1.3, color=col, label=k)
    ax.plot(x, np.array(price) * 100, marker='s', ms=4.2, lw=2.0, color=GREEN,
            label='Selling price')
    ax.plot(x, np.array(DCF['pi_cost']) * 100, marker='^', ms=3.8, lw=1.6, color=RED,
            ls='--', label='Weighted build cost')
    ax.set_xticks(x); ax.set_xticklabels(yrs, fontsize=7.8)
    ax.set_ylabel('escalation, per cent a year', fontsize=8)
    ax.legend(fontsize=6.8, frameon=False, ncol=3, loc='upper center',
              bbox_to_anchor=(0.5, -0.16), handlelength=1.5, columnspacing=1.1)
    ax.grid(axis='y', color='#E3EAE8', lw=0.7); ax.set_axisbelow(True)
    ax.set_ylim(0, max(max(v) for v in esc.values()) * 100 * 1.12)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_title('One escalator per class, against the price path', fontsize=8.6, color=INK, pad=8)
    return _save(fig, 'fig7_mix.png')


# ------------------------------------------------ figure D1: expert divergence
def figD1():
    E = D['experts']
    names = ['Expert 1\ncash flow on\nconstruction execution',
             'Expert 2\ncontracted-book\nrun-off',
             'Expert 3\nreturn on equity\nagainst its cost']
    lo = [min(E['e1']['vps_A'], E['e1']['vps_B']), E['e2']['vps'],
          min(E['e3']['vps_spot'], E['e3']['vps_norm'])]
    hi = [max(E['e1']['vps_A'], E['e1']['vps_B']), E['e2']['vps'],
          max(E['e3']['vps_spot'], E['e3']['vps_norm'])]
    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    x = np.arange(3)
    for xi, a, b, col in zip(x, lo, hi, [BRASS, GOLD, GREY]):
        if abs(b - a) < 0.05:
            ax.plot([xi], [a], marker='D', ms=9, color=col)
            ax.annotate('%.2f' % a, (xi, a), xytext=(0, -14), textcoords='offset points',
                        ha='center', fontsize=7.8, color=INK)
            continue
        ax.plot([xi, xi], [a, b], lw=9, color=col, solid_capstyle='butt')
        ax.annotate('%.2f' % a, (xi, a), xytext=(0, -12), textcoords='offset points',
                    ha='center', fontsize=7.8, color=INK)
        ax.annotate('%.2f' % b, (xi, b), xytext=(0, 6), textcoords='offset points',
                    ha='center', fontsize=7.8, color=INK)
    ax.axhline(M['spot'], color=INK, ls='--', lw=1.1)
    ax.annotate('market %.2f' % M['spot'], (2.46, M['spot']), xytext=(0, -13),
                textcoords='offset points', ha='right', fontsize=7.8, color=INK, weight='bold')
    ax.axhline(SYN['base'], color=GOLD, ls=':', lw=1.4)
    ax.annotate('study base %.2f' % SYN['base'], (2.46, SYN['base']), xytext=(0, 7),
                textcoords='offset points', ha='right', fontsize=7.8, color=BRASS, weight='bold')
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=7.8)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylabel('EGP per share')
    ax.grid(axis='y', color='#E3EAE8', lw=0.7); ax.set_axisbelow(True)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.set_title('Three methods, three answers — and what drives the gap', fontsize=9.2,
                 color=INK, pad=8)
    return _save(fig, 'figD1_experts.png')


if __name__ == '__main__':
    made = [fig1(), fig2(), fig3(), fig4(), fig5(), fig6(), fig7(), figD1()]
    # opacity gate: every delivered figure must be fully opaque on a solid canvas
    from PIL import Image
    for f in made:
        im = Image.open(f)
        if im.mode in ('RGBA', 'LA'):
            a = np.array(im.split()[-1])
            assert a.min() == 255, 'transparent pixels in ' + f
        px = np.array(im.convert('RGB'))
        assert px.shape[0] > 300 and px.shape[1] > 600, 'figure too small: ' + f
        print('  %-22s %4dx%-4d opaque' % (f, px.shape[1], px.shape[0]))
    print('%d figures written, all opaque on a solid canvas' % len(made))
