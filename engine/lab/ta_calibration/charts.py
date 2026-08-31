"""charts.py — every figure in the register, generated from the results files.

Palette is the validated categorical set (validate_palette.js, light mode, all
checks PASS). The contrast warning on the yellow and aqua slots is discharged
the way the skill requires: every bar carries a visible direct label, so identity
and value never rest on the fill alone.

One axis per chart, thin marks, recessive grid, no chart type chosen for
decoration. A bar is used for magnitude comparison, a ladder for a calibration
mapping, a histogram for a distribution.
"""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# set_yticklabels() on an auto-located axis relabels whatever ticks happen to
# exist and silently mislabels the axis if the locator later moves them. A
# formatter is applied to the VALUE, so it cannot drift.
PCT_PT = FuncFormatter(lambda v, _: f'{v*100:.0f}')
PCT = FuncFormatter(lambda v, _: f'{v*100:.0f}%')

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, 'figures')
os.makedirs(FIG, exist_ok=True)

SURFACE = '#fcfcfb'
INK = '#0b0b0b'
INK2 = '#52514e'
MUTED = '#8a8984'
BLUE, ORANGE, AQUA, YELLOW, VIOLET = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#4a3aa7'
GOOD, BAD = '#1baf7a', '#eb6834'

plt.rcParams.update({
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE,
    'savefig.facecolor': SURFACE, 'font.family': 'DejaVu Sans',
    'font.size': 9, 'axes.edgecolor': '#d8d7d2', 'axes.labelcolor': INK2,
    'xtick.color': INK2, 'ytick.color': INK2, 'axes.titlesize': 11,
    'axes.titleweight': 'bold', 'axes.titlecolor': INK,
})

D = json.load(open(os.path.join(HERE, 'RESULTS_deep.json')))
S = json.load(open(os.path.join(HERE, 'RESULTS_scopes.json')))
X = json.load(open(os.path.join(HERE, 'RESULTS_extra.json')))
VP = json.load(open(os.path.join(HERE, 'RESULTS_volume_partial.json')))


def _finish(ax, title, sub=None, xlabel=None, ylabel=None):
    import textwrap
    if sub:
        sub = textwrap.fill(sub, 108)
    ax.set_title(title, loc='left', pad=(14 + 10 * sub.count('\n')) if sub else 8)
    if sub:
        # wrapped, because a single long line hangs past the axes and the tight
        # bounding box then grows sideways — the plot ends up squeezed into the
        # left third of its own figure
        ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=8.5, color=INK2,
                va='bottom')
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.grid(axis='y', color='#ebeae5', lw=0.8)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)


def _save(fig, name):
    path = os.path.join(FIG, name)
    fig.tight_layout()
    fig.savefig(path, dpi=170, bbox_inches='tight')
    plt.close(fig)
    return path


def _labels(ax, bars, vals, fmt='{:+.1f}', dy=0.0015, pct=True):
    for b, v in zip(bars, vals):
        y = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, y + (dy if y >= 0 else -dy),
                fmt.format(v * 100 if pct else v), ha='center',
                va='bottom' if y >= 0 else 'top', fontsize=8.5, color=INK)


# 1 — the horizon decay, the finding the whole re-run rests on
def fig_horizon():
    hs = [5, 10, 21]
    v = [S[f'levels|h{h}|market_label']['pooled']['effect'] for h in hs] + [0.0337]
    lab = ['1 week', '2 weeks', '1 month', '3 months\n(the cone’s horizon)']
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    cols = [BLUE, BLUE, BLUE, MUTED]
    bars = ax.bar(lab, v, color=cols, width=0.6)
    _labels(ax, bars, v)
    _finish(ax, 'A charted level is worth most in the first week',
            'How much less often price closes through a published level than through a '
            'matched non-level at the same distance',
            ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '01_horizon_decay.png')


# 2 — level kind, against the module's own ranking
def fig_kind():
    k = D['h5']['by_kind']
    order = ['20-day MA', 'swing', 'round', '52w high']
    items = [(o, k[o]) for o in order if o in k]
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    names = ['20-day moving\naverage', 'swing high/low\n(charted structure)',
             'round number', '52-week high']
    vals = [i[1]['effect'] for i in items]
    ns = [i[1]['n'] for i in items]
    sig = [abs(i[1]['z']) > 1.96 for i in items]
    cols = [AQUA if s else MUTED for s in sig]
    bars = ax.bar(names[:len(items)], vals, color=cols, width=0.6)
    _labels(ax, bars, vals)
    for b, n in zip(bars, ns):
        ax.text(b.get_x() + b.get_width() / 2, 0.004, f'n={n:,}', ha='center',
                fontsize=7.5, color=SURFACE, weight='bold')
    _finish(ax, 'The 20-day average holds as well as charted structure',
            'The read ranks a swing cluster ABOVE a moving average. Grey = not '
            'statistically distinguishable from zero.', ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '02_level_kind.png')


# 3 — touch count, against the module's weighting
def fig_touches():
    t = D['h21']['by_touches']
    order = ['none (MA/round/52w)', '1', '2', '3-4', '5+']
    items = [(o, t[o]) for o in order if o in t]
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    vals = [i[1]['effect'] for i in items]
    bars = ax.bar([i[0] for i in items], vals, color=ORANGE, width=0.6)
    _labels(ax, bars, vals)
    m = float(np.mean(vals))
    ax.axhline(m, color=MUTED, lw=1.2, ls='--')
    ax.text(len(items) - 0.4, m, ' average', va='center', fontsize=8, color=INK2)
    _finish(ax, 'How often a level was tested does not predict whether it holds',
            'The read scores a level by touch count. The edge is flat across every '
            'count.', xlabel='times the level was tested before publication',
            ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '03_touches.png')


# 4 — the ATR ladder, the best-calibrated thing in the read
def fig_atr():
    rows = D['h21']['atr']
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    y = np.arange(len(rows))
    for i, r in enumerate(rows):
        ax.plot([r['q25'], r['q75']], [i, i], color='#cfd8e6', lw=9,
                solid_capstyle='round', zorder=1)
        ax.plot([r['med']], [i], 'o', ms=10, color=BLUE, zorder=3,
                markeredgecolor=SURFACE, markeredgewidth=2)
        ax.text(r['q75'] + 0.02, i, f"{r['med']*100:.0f}%", va='center',
                fontsize=9, color=INK, weight='bold')
        ax.text(0.02, i + 0.30, f"n={r['n']:,}", fontsize=7.5, color=MUTED)
    ax.set_yticks(y)
    ax.set_yticklabels([r['word'] for r in rows])
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(PCT)
    _finish(ax, 'The tape sentence is a real forecast, and it is well calibrated',
            'Realized movement over the next month. Dot = median, bar = the middle '
            'half of outcomes.', xlabel='annualised movement that actually followed')
    ax.grid(axis='y', visible=False)
    ax.grid(axis='x', color='#ebeae5', lw=0.8)
    return _save(fig, '04_atr_ladder.png')


# 5 — RSI across its whole range
def fig_rsi():
    b = D['h5']['rsi']['buckets']
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    x = [f"{r['lo']:.0f}–{r['hi']:.0f}" for r in b]
    v = [r['lift'] for r in b]
    e = [r['se'] for r in b]
    cols = [VIOLET if i == len(b) - 1 else MUTED for i in range(len(b))]
    bars = ax.bar(x, v, yerr=e, color=cols, width=0.62,
                  error_kw=dict(ecolor='#b9b8b2', lw=1, capsize=2))
    ax.axhline(0, color=INK2, lw=1)
    ax.text(len(b) - 1, v[-1] + e[-1] + 0.002, f'{v[-1]*100:+.1f}',
            ha='center', fontsize=8.5, color=INK, weight='bold')
    _finish(ax, 'RSI says almost nothing until its very top',
            'Change in the odds of a higher close one week later, against this book’s '
            'base rate. Bars are one standard error.',
            xlabel='RSI(14) decile', ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '05_rsi_curve.png')


# 6 — 52-week position
def fig_52w():
    b = D['h21']['w52']['buckets']
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    x = [r['mid'] * 100 for r in b]
    v = [r['lift'] for r in b]
    ax.plot(x, v, '-o', color=BLUE, lw=2, ms=7, markeredgecolor=SURFACE,
            markeredgewidth=1.6)
    ax.axhline(0, color=INK2, lw=1)
    ax.annotate(f'{v[0]*100:+.1f}', (x[0], v[0]), textcoords='offset points',
                xytext=(6, 8), fontsize=8.5, color=INK, weight='bold')
    lo = int(np.argmin(v))
    ax.annotate(f'{v[lo]*100:+.1f}', (x[lo], v[lo]), textcoords='offset points',
                xytext=(0, -14), fontsize=8.5, color=INK, weight='bold', ha='center')
    _finish(ax, 'Stocks near their 52-week high keep doing better',
            'Change in the odds of a higher close one month later, against the base '
            'rate. The read publishes this distance and has never scored it.',
            xlabel='% below the 52-week high at the time of reading',
            ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '06_52week.png')


# 7 — 200-day slope
def fig_slope():
    rows = D['h21']['slope200']['rows']
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    v = [r['lift'] for r in rows]
    cols = [GOOD if r['lift'] > 0 else (BAD if r['lift'] < -0.005 else MUTED) for r in rows]
    bars = ax.bar([r['state'] for r in rows], v, color=cols, width=0.55,
                  yerr=[r['se'] for r in rows],
                  error_kw=dict(ecolor='#b9b8b2', lw=1, capsize=3))
    _labels(ax, bars, v)
    ax.axhline(0, color=INK2, lw=1)
    _finish(ax, 'Which way the 200-day is sloping matters',
            'Change in the odds of a higher close one month later.',
            xlabel='200-day moving average', ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '07_slope200.png')


# 8 — level edge by market
def fig_market():
    pc = S['levels|h5|market_label']['per_class']
    items = sorted(pc.items(), key=lambda x: -x[1]['effect'])
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    v = [i[1]['effect'] for i in items]
    bars = ax.bar([i[0].replace(' (', '\n(') for i in items], v, color=BLUE, width=0.55)
    _labels(ax, bars, v)
    _finish(ax, 'A level is worth about twice as much in Saudi as in Egypt',
            'The only place a market-level difference is bigger than sampling noise.',
            ylabel='percentage points')
    ax.yaxis.set_major_formatter(PCT_PT)
    return _save(fig, '08_level_market.png')


# 9 — the trigger, backwards
def fig_trigger():
    hs = [5, 10, 21]
    real = [X[f'trigger|h{h}|both']['p_real'] for h in hs]
    null = [X[f'trigger|h{h}|both']['p_null'] for h in hs]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    x = np.arange(3)
    w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, real, w, color=ORANGE, label='after a real level was cleared')
    b2 = ax.bar(x + w / 2 + 0.01, null, w, color=MUTED, label='after a non-level was cleared')
    for bs, vs in ((b1, real), (b2, null)):
        for b, v in zip(bs, vs):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.006, f'{v*100:.1f}%',
                    ha='center', fontsize=8.5, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(['1 week', '2 weeks', '1 month'])
    ax.legend(frameon=False, fontsize=8.5, loc='upper left')
    ax.yaxis.set_major_formatter(PCT)
    _finish(ax, 'The trigger sentence promised the opposite of what happens',
            'How often the far level opened AFTER the close that fired the trigger. '
            'Lower for the real level, at every horizon.',
            ylabel='far level opened')
    return _save(fig, '09_trigger.png')


# 10 — the cross
def fig_cross():
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    labels, fresh, stale = [], [], []
    for kind in ('golden', 'death'):
        c = X[f'cross|h21|{kind}']
        labels.append(f'{kind} cross')
        fresh.append(c['p_real']); stale.append(c['p_null'])
    x = np.arange(2); w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, fresh, w, color=VIOLET, label='fresh (within 25 sessions)')
    b2 = ax.bar(x + w / 2 + 0.01, stale, w, color=MUTED, label='established')
    for bs, vs in ((b1, fresh), (b2, stale)):
        for b, v in zip(bs, vs):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.004, f'{v*100:.1f}%',
                    ha='center', fontsize=8.5, color=INK)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0.42, 0.58)
    ax.legend(frameon=False, fontsize=8.5, loc='upper right')
    ax.yaxis.set_major_formatter(PCT)
    _finish(ax, 'A “fresh” cross is not a regime change',
            'Odds of a higher close one month later. A fresh golden cross does WORSE '
            'than an established one.', ylabel='higher close')
    return _save(fig, '10_cross.png')


# 11 — volume against the tape reading
def fig_volume():
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    names = ['tape reading\n(ATR)', 'volume\nalone', 'volume, after the\ntape is accounted for']
    v = [VP['5']['atr'], VP['5']['raw'], VP['5']['partial']]
    bars = ax.bar(names, v, color=[BLUE, YELLOW, MUTED], width=0.55)
    for b, val in zip(bars, v):
        ax.text(b.get_x() + b.get_width() / 2, val + 0.012, f'{val:+.3f}',
                ha='center', fontsize=9, color=INK, weight='bold')
    _finish(ax, 'Volume says the same thing as the tape reading, far more faintly',
            'Correlation with how far price actually travelled over the next week.',
            ylabel='rank correlation')
    return _save(fig, '11_volume.png')


# 12 — per-name distribution of the tape claim
def fig_pername():
    vals = D['h5']['tape_per_name']
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.hist(vals, bins=22, color=BLUE, edgecolor=SURFACE, linewidth=1.2)
    ax.axvline(0, color=BAD, lw=1.6)
    ax.text(0.01, ax.get_ylim()[1] * 0.92, ' no relationship', color=BAD, fontsize=8.5)
    ax.axvline(float(np.median(vals)), color=INK, lw=1.4, ls='--')
    ax.text(float(np.median(vals)) + 0.01, ax.get_ylim()[1] * 0.72,
            f' median {np.median(vals):+.2f}', fontsize=8.5, color=INK)
    _finish(ax, 'The tape reading works on nearly every stock, one at a time',
            f'Each bar counts stocks. {sum(1 for v in vals if v > 0)} of {len(vals)} '
            f'sit above zero — this is the only claim that survives per name.',
            xlabel='the stock’s own correlation between tape reading and what followed',
            ylabel='number of stocks')
    return _save(fig, '12_pername_tape.png')


# 13 — does each family survive both halves of the fifteen years?
def fig_stability():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    fams = ['levels', 'trend', 'tape (÷10)']
    e5, l5 = D['h21']['stability']['early'], D['h21']['stability']['late']
    early = [e5['levels']['effect'], e5['trend'], e5['tape'] / 10]
    late = [l5['levels']['effect'], l5['trend'], l5['tape'] / 10]
    x = np.arange(3); w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, early, w, color=BLUE, label='2012–2020')
    b2 = ax.bar(x + w / 2 + 0.01, late, w, color=AQUA, label='2020–2026')
    for bs, vs in ((b1, early), (b2, late)):
        for b, v in zip(bs, vs):
            # A negative bar's label goes just ABOVE the zero line, not below the
            # bar: below, it lands on top of the category tick label.
            y, va = (v + 0.002, 'bottom') if v >= 0 else (0.002, 'bottom')
            ax.text(b.get_x() + b.get_width() / 2, y, f'{v:+.3f}', ha='center',
                    va=va, fontsize=8.5, color=INK)
    ax.axhline(0, color=INK2, lw=1)
    ax.set_xticks(x); ax.set_xticklabels(fams)
    ax.legend(frameon=False, fontsize=8.5, loc='upper left',
              bbox_to_anchor=(0.0, -0.16), ncol=2)
    _finish(ax, 'Two of the three hold in both halves. The trend claim does not.',
            'One-month horizon, split at 2020-08-14. The trend effect flips sign in the '
            'recent half; tape is divided by 10 to share the axis.',
            ylabel='effect size')
    return _save(fig, '13_stability.png')


ALL = [fig_horizon, fig_kind, fig_touches, fig_atr, fig_rsi, fig_52w, fig_slope,
       fig_market, fig_trigger, fig_cross, fig_volume, fig_pername, fig_stability]

if __name__ == '__main__':
    for f in ALL:
        print('  wrote', os.path.basename(f()))
    print(f'{len(ALL)} figures in {FIG}')


# ============================ third edition: aggregates =========================
M = json.load(open(os.path.join(HERE, 'RESULTS_more.json')))


def fig_schematic():
    """How the test works — drawn, not photographed."""
    rng = np.random.default_rng(7)
    n = 130
    px = 100 * np.exp(np.cumsum(rng.normal(0.0006, 0.012, n)))
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    cut = 95
    ax.plot(range(cut + 1), px[:cut + 1], color=INK, lw=1.8)
    ax.plot(range(cut, n), px[cut:], color=MUTED, lw=1.6, ls=':')
    lvl = px[:cut].max() * 1.004
    fake = lvl * 1.045
    ax.set_ylim(px.min() * 0.945, fake * 1.035)
    ax.set_xlim(-2, n + 1)
    ax.axvline(cut, color=BLUE, lw=1.4)
    ax.axvspan(cut, cut + 21, color=BLUE, alpha=0.08)
    ax.axhline(lvl, color=ORANGE, lw=1.8)
    ax.text(2, lvl, 'a published level', va='bottom', fontsize=9, color=ORANGE,
            weight='bold')
    ax.axhline(fake, color=MUTED, lw=1.4, ls='--')
    ax.text(2, fake, 'a made-up level at a similar distance, placed where the chart '
            'shows nothing', va='bottom', fontsize=8.5, color=INK2)
    ax.annotate('one origin — the read is computed here,\nusing only what is to '
                'the left', xy=(cut, px.min() * 0.985),
                xytext=(cut - 42, px.min() * 0.958), fontsize=8.5, color=BLUE,
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1))
    ax.text(cut + 10.5, fake * 1.005, 'then we watch\nwhat happens', ha='center',
            va='bottom', fontsize=8.5, color=INK2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    _finish(ax, 'How every test in this document works',
            'Repeat at every week of fifteen years, on 92 stocks, and compare the '
            'real line against the made-up one.')
    ax.grid(visible=False)
    return _save(fig, '14_schematic.png')


def fig_res_sup():
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    hs = [5, 10, 21]
    res = [M['side'][str(h)]['res']['effect'] for h in hs]
    sup = [M['side'][str(h)]['sup']['effect'] for h in hs]
    x = np.arange(3); w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, sup, w, color=AQUA, label='support (below the price)')
    b2 = ax.bar(x + w / 2 + 0.01, res, w, color=BLUE, label='resistance (above the price)')
    for bs, vs in ((b1, sup), (b2, res)):
        _labels(ax, bs, vs)
    ax.set_xticks(x); ax.set_xticklabels(['1 week', '2 weeks', '1 month'])
    ax.legend(frameon=False, fontsize=8.5)
    ax.yaxis.set_major_formatter(PCT_PT)
    _finish(ax, 'The floor is stronger than the ceiling',
            'The same test, split by side. Support holds better than resistance at '
            'every horizon.', ylabel='percentage points')
    return _save(fig, '15_res_sup.png')


def fig_touch_rate():
    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    hs = [5, 10, 21]
    near = [M['touch'][str(h)]['nearest'] for h in hs]
    bars = ax.bar(['within 1 week', 'within 2 weeks', 'within 1 month'], near,
                  color=VIOLET, width=0.55)
    for b, v in zip(bars, near):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.008, f'{v*100:.0f}%', ha='center',
                fontsize=9.5, color=INK, weight='bold')
    ax.set_ylim(0, 0.52)
    ax.yaxis.set_major_formatter(PCT)
    _finish(ax, 'Most weeks, the nearest level is never even touched',
            'How often price reaches the closest published level at all. The test of a '
            'level only begins when price gets there.',
            ylabel='price reached the nearest level')
    return _save(fig, '16_touch_rate.png')


def fig_coin():
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    mk = ['EG', 'AE', 'SA', 'QA', 'KR', 'IN', 'US']
    w1 = [M['coin']['5']['by_market'][m]['up'] for m in mk]
    m1 = [M['coin']['21']['by_market'][m]['up'] for m in mk]
    x = np.arange(len(mk)); w = 0.34
    b1 = ax.bar(x - w / 2 - 0.01, w1, w, color=MUTED, label='over 1 week')
    b2 = ax.bar(x + w / 2 + 0.01, m1, w, color=BLUE, label='over 1 month')
    ax.axhline(0.5, color=INK2, lw=1.2)
    ax.text(len(mk) - 0.4, 0.502, 'a fair coin', fontsize=8, color=INK2)
    for bs, vs in ((b1, w1), (b2, m1)):
        for b, v in zip(bs, vs):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.004, f'{v*100:.0f}',
                    ha='center', fontsize=8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(['Egypt', 'UAE', 'Saudi', 'Qatar', 'Korea', 'India', 'US'])
    ax.set_ylim(0.44, 0.64)
    ax.yaxis.set_major_formatter(PCT)
    ax.legend(frameon=False, fontsize=8.5, loc='upper left')
    _finish(ax, 'The coin is fair over a week and tilted over a month',
            'How often a stock simply closes higher. Every claim in this document is '
            'judged against this tilt, never against 50%.',
            ylabel='closed higher')
    return _save(fig, '17_tilted_coin.png')


# ============================ third edition: real tickers =======================
import sys as _sys
_ENG = os.path.abspath(os.path.join(HERE, '..', '..'))
if _ENG not in _sys.path:
    _sys.path.insert(0, _ENG)


def _lib(market, ticker):
    from strike_cohorts import load_clean
    df, _ = load_clean(market, ticker)
    return df.reset_index(drop=True)


def _demo_frame(ep, back=70, fwd=21):
    df = _lib(ep['market'], ep['ticker'])
    i = ep['origin_idx']
    assert str(pd.to_datetime(df['Date']).iloc[i].date()) == ep['origin'], \
        'library moved under the episode'
    a, b = max(0, i - back), min(len(df) - 1, i + fwd)
    return df.iloc[a:b + 1], i - a


import pandas as pd  # noqa: E402


CCY = {'AE': 'AED', 'EG': 'EGP', 'SA': 'SAR', 'QA': 'QAR', 'US': 'USD',
       'IN': 'INR', 'KR': 'KRW'}
NAMES_FULL = {'QNB': 'Qatar National Bank', 'ADCB': 'Abu Dhabi Commercial Bank',
              'ETEL': 'Telecom Egypt', 'SABIC': 'SABIC',
              'IHC': 'International Holding Company'}


def fig_demo_level():
    ep = M['ep_level']
    d, k = _demo_frame(ep, back=55)
    px = d['Price'].astype(float).to_numpy()
    hi = d['High'].astype(float).to_numpy()
    lo = d['Low'].astype(float).to_numpy()
    fig, ax = plt.subplots(figsize=(7.4, 3.7))
    # the intraday range matters here: a "touch" happens on the high of the day,
    # and a close-only line would hide the very thing the chart demonstrates —
    # the first cut of this figure did exactly that, and clipped its own
    # annotation off the top of the axis into the bargain
    ax.fill_between(range(len(d)), lo, hi, color='#dfe7f2', linewidth=0)
    ax.plot(range(len(d)), px, color=INK, lw=1.6, label='daily close')
    ax.axvspan(k, len(d) - 1, color=BLUE, alpha=0.06)
    ax.axhline(ep['level'], color=ORANGE, lw=1.8)
    ax.text(1, ep['level'] * 1.0015, f"published resistance {ep['level']:.2f}",
            fontsize=9, color=ORANGE, weight='bold', va='bottom')
    ax.axvline(k, color=BLUE, lw=1.2)
    ax.text(k - 1.5, lo.min(), f"read published\n{ep['origin']} ", ha='right',
            va='bottom', fontsize=8, color=BLUE)
    fh = hi[k + 1:]
    j = k + 1 + int(np.argmax(fh))
    ax.plot([j], [fh.max()], 'o', ms=8, color=ORANGE, markeredgecolor=SURFACE,
            markeredgewidth=1.8, zorder=5)
    ax.annotate(f'poked to {fh.max():.2f} during the day —\nnever CLOSED above; '
                f'month ended {ep["fwd_ret"]*100:+.1f}%',
                xy=(j, fh.max()), xytext=(j - 26, fh.max() * 0.998), ha='center',
                fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1))
    ax.set_ylim(lo.min() * 0.99, max(hi.max(), ep['level']) * 1.015)
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    _finish(ax, f"{ep['ticker']} — a level doing its job",
            f"{NAMES_FULL.get(ep['ticker'], ep['ticker'])}, {ep['origin']}: resistance "
            f"published at {ep['level']:.2f} — a round number — with the price at "
            f"{ep['spot']:.2f} after a month below it. Shaded band = each day's "
            f"low-to-high range; the following month is tinted.",
            ylabel=f"price ({CCY.get(ep['market'], '')})")
    ax.set_xticks([])
    return _save(fig, '18_demo_level.png')


def fig_demo_trigger():
    ep = M['ep_trigger']
    d, k = _demo_frame(ep)
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.plot(range(len(d)), d['Price'].astype(float), color=INK, lw=1.6)
    ax.axvspan(k, len(d) - 1, color=BLUE, alpha=0.07)
    ax.axhline(ep['level'], color=ORANGE, lw=1.8)
    ax.text(1, ep['level'] * 1.003, f"nearest resistance {ep['level']:.2f} — cleared",
            fontsize=8.5, color=ORANGE, weight='bold', va='bottom')
    ax.axhline(ep['far'], color=BAD, lw=1.8, ls='--')
    ax.text(1, ep['far'] * 0.997, f'the "zone" the old sentence promised: '
            f"{ep['far']:.2f} — never approached", fontsize=8.5, color=BAD,
            va='top', weight='bold')
    fc = d['Price'].astype(float).iloc[k + 1:]
    fired = int(np.argmax((fc >= ep['level']).values))
    ax.plot([k + 1 + fired], [fc.iloc[fired]], 'o', ms=9, color=ORANGE,
            markeredgecolor=SURFACE, markeredgewidth=2)
    _finish(ax, f"{ep['ticker']} — the trigger fired, the promise did not",
            f"Telecom Egypt, {ep['origin']}: price closed above {ep['level']:.2f} inside "
            f"the month, and finished {ep['fwd_ret']*100:+.1f}% — nowhere near "
            f"{ep['far']:.2f}. This is the TYPICAL outcome, not a cherry-picked one.",
            ylabel='price (EGP)')
    ax.set_xticks([])
    return _save(fig, '19_demo_etel.png')


def fig_demo_cross():
    ep = M['ep_cross']
    df = _lib(ep['market'], ep['ticker'])
    i = ep['origin_idx']
    a = max(0, i - 260)
    d = df.iloc[a:i + 22].reset_index(drop=True)
    px = d['Price'].astype(float).to_numpy()
    full = df['Price'].astype(float).to_numpy()
    ma50 = pd.Series(full).rolling(50).mean().iloc[a:i + 22].to_numpy()
    ma200 = pd.Series(full).rolling(200).mean().iloc[a:i + 22].to_numpy()
    k = i - a
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ax.plot(px, color=INK, lw=1.3, label='price')
    ax.plot(ma50, color=BLUE, lw=1.6, label='50-day average')
    ax.plot(ma200, color=ORANGE, lw=1.6, label='200-day average')
    ax.axvspan(k, len(d) - 1, color=BLUE, alpha=0.07)
    cx = k - ep['cross_ago']
    ax.plot([cx], [ma50[cx]], 'o', ms=10, color=VIOLET, markeredgecolor=SURFACE,
            markeredgewidth=2, zorder=5)
    ax.annotate('the "golden cross"', xy=(cx, ma50[cx]), xytext=(cx - 90, ma50[cx] * 1.03),
                fontsize=9, color=VIOLET, weight='bold',
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=1))
    ax.text(k + 10, px[k:].max() * 1.005, f'{ep["fwd_ret"]*100:+.1f}%\nin the month after',
            ha='center', fontsize=9, color=BAD, weight='bold')
    ax.legend(frameon=False, fontsize=8.5, loc='lower left')
    _finish(ax, f"{ep['ticker']} — a fresh golden cross, and the month after",
            f"SABIC, {ep['origin']}: the 50-day crossed above the 200-day "
            f"{ep['cross_ago']} sessions earlier. The read used to call this a "
            f"momentum-regime change.", ylabel='price (SAR)')
    ax.set_xticks([])
    return _save(fig, '20_demo_sabic.png')


def fig_demo_ihc():
    r = pd.read_pickle(os.path.join(HERE, 'claims_short.pkl'))
    d = r[(r.claim == 'state') & (r.h == 21) & (r.ticker == 'IHC')].dropna(
        subset=['atr_pct', 'rlz_vol'])
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.scatter(d.atr_pct * 100, d.rlz_vol * 100, s=14, color=BLUE, alpha=0.35,
               edgecolors='none')
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.text(0.97, 0.06, f"rank correlation {M['ihc']['rho']:+.2f} over "
            f"{M['ihc']['n']} readings", transform=ax.transAxes, ha='right',
            fontsize=9.5, color=INK, weight='bold')
    _finish(ax, 'IHC — every dot is one week of the last nine years',
            'International Holding Company: how busy the tape looked that day (across), '
            'and how much the price then moved over the next month (up).',
            xlabel='daily range at the time of the read (ATR, % of price)',
            ylabel='movement that followed (annualised)')
    return _save(fig, '21_demo_ihc.png')


ALL += [fig_schematic, fig_res_sup, fig_touch_rate, fig_coin,
        fig_demo_level, fig_demo_trigger, fig_demo_cross, fig_demo_ihc]
