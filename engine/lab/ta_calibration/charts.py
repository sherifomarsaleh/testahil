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
    ax.set_title(title, loc='left', pad=14 if sub else 8)
    if sub:
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
