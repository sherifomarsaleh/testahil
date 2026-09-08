import os as _os_pathfix
# EVERY PATH IN THIS BUILDER IS RELATIVE, SO THE RUN'S DIRECTORY DECIDED WHERE ITS
# INPUT WAS READ AND ITS OUTPUT WAS WRITTEN. Run from anywhere but this folder it
# either crashed or, worse, wrote a deliverable into the caller's directory.
_HERE = _os_pathfix.path.dirname(_os_pathfix.path.abspath(__file__))
_os_pathfix.chdir(_HERE)
import sys as _sys_pathfix
_sys_pathfix.path.insert(0, _HERE)
_sys_pathfix.path.insert(0, _os_pathfix.path.join(_HERE, '..'))

import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import primitives as m

CANVAS, CREAM, GOLD, BRASS, SAGE = '#1C3A36', '#F6F1E6', '#C0A45F', '#896F36', '#9FB0AC'
INK, GRID, GREY = '#1C3A36', '#D5DDDB', '#6E7B77'
plt.rcParams.update({'figure.facecolor': CREAM, 'axes.facecolor': CREAM,
                     'axes.edgecolor': GREY, 'axes.labelcolor': INK,
                     'xtick.color': INK, 'ytick.color': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans', 'axes.grid': True,
                     'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.titlecolor': INK, 'savefig.transparent': False,
                     'savefig.facecolor': CREAM, 'savefig.edgecolor': CREAM})

d = json.load(open('study_numbers.json'))
spot = d['spot']
# THE EXCHANGE LIBRARY, NOT THE STUDY-LOCAL COPY. compute.py strikes the cone on
# engine/raw_ohlc/EG/GBCO.csv; a chart drawn from the study-local extract, which stops
# at 7 July 2026, would draw a different series from the one every number came off.
import os as _os
df = m.load_ohlc(_os.path.join(_os.path.dirname(_os.path.dirname(
    _os.path.abspath(__file__))), 'raw_ohlc', 'EG', 'GBCO.csv'))

def style(ax):
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    for s in ['left', 'bottom']: ax.spines[s].set_color(GREY)

# ---- F1 football field ------------------------------------------------------
# REBUILT 07-09-2026. There is no weighted central and no normalised lens to draw. The
# class primary IS the answer and it has two branches, so it is drawn as the SPAN BETWEEN
# THEM with a tick on each; the cross-checks are single marks, because a single value with
# an invented spread around it is exactly what this edition removed.
LR = d['lens_record']
BR = d['central_two_sided']['branches']
V_LO, V_HI = BR[0]['value'], BR[1]['value']
CC = {c['kind']: c for c in LR['cross_checks']}
ENV = LR['envelope']
_reads = [
    ('The sum of the parts\n(class primary — the answer)', (V_LO, V_HI), (V_LO, V_HI)),
    ('Relative multiple\n(cross-check)', (CC['relative_multiple']['value'],), None),
    ('Disclosed book value\n(cross-check — a floor)', (CC['book_value']['value'],), None),
]
_all = [v for _, ticks, _ in _reads for v in ticks] + [spot, ENV['low'], ENV['high']]
_LO, _HI = min(_all), max(_all)
_SPAN = _HI - _LO
_PAD = _SPAN * 0.012
fig, ax = plt.subplots(figsize=(9.7, 3.5), dpi=110)
for i, (nm, ticks, span) in enumerate(_reads):
    y = len(_reads) - 1 - i
    if span:
        ax.barh(y, span[1] - span[0], left=span[0], height=0.46, color=SAGE, alpha=0.32,
                edgecolor=SAGE, linewidth=1.1)
        lbl = f'{span[0]:.2f}  and  {span[1]:.2f}'
    else:
        lbl = f'{ticks[0]:.2f}'
    for t in ticks:
        ax.plot([t, t], [y - 0.23, y + 0.23], color=BRASS, lw=3.4)
    ax.text(max(ticks) + _PAD, y, lbl, va='center', fontsize=8.6, color=INK)
ax.axvline(spot, color=INK, lw=1.6)
ax.axvspan(ENV['low'], ENV['high'], color=GOLD, alpha=0.13)
ax.set_yticks(range(len(_reads)), [r[0] for r in _reads][::-1], fontsize=9)
ax.set_xlabel('EGP / share')
# THE AXIS IS FITTED TO THE DATA, NOT TYPED — a hardcoded limit clips whatever the rebuild
# moved past it, and a clipped reference line is a claim drawn outside its own picture.
ax.set_xlim(_LO - _SPAN * 0.06, _HI + _SPAN * 0.22)
ax.set_ylim(-0.75, len(_reads) - 0.4)
ax.text(spot + _PAD, -0.62, f'spot {spot:.2f}', color=INK, fontsize=8.6, ha='left', va='center')
ax.set_title('GB Corp — the primary lens on both of its branches (never averaged), and the '
             'cross-checks beside it', fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('fig1_football.png'); plt.close(fig)

# ---- F2 the crux grid --------------------------------------------------------
# THE COMMITTED sens GRID IS NOT DRAWN AND THE REASON IS RECORDED. It re-prices the sum of
# the parts across an Auto-margin shift and a COMPLEXITY DISCOUNT, and this edition applies
# no complexity discount at all; its base cell also carries the lender at its book rather
# than at the residual-income mark the study adopts, so it does not reproduce the published
# answer. What is drawn instead is the crux on its own axes: the associate mark against the
# cost of capital, recomputed from the study's own committed outputs, whose centre cell IS
# the published branch.
MARK_LO = LR['primary']['range_basis']['low']
MARK_HI = LR['primary']['range_basis']['high']
_S = d['sotp']; _DCF = d['dcf']; _SH = d['shares']
_TG = d['macro']['terminal_growth_nominal']


def _ps(mark, shift):
    fcffs = [r['fcff'] for r in _DCF['rows']]
    fac, cum = [], 1.0
    for r in _DCF['forward_wacc']:
        cum /= (1.0 + r + shift)
        fac.append(cum)
    wt = _DCF['wacc_terminal'] + shift
    if wt - _TG <= 0.045:
        return float('nan')
    pv = sum(f * fac[i] for i, f in enumerate(fcffs))
    tv = fcffs[-1] * (1.0 + _TG) / (wt - _TG) * fac[-1]
    return ((pv + tv - _DCF['auto_nd'] - _DCF['auto_nci'] + _S['cap_val'] + mark
             + _S['other_assoc']) / _SH)


_wshift = [-0.02, -0.01, 0.0, 0.01, 0.02]
_marks = sorted({MARK_LO, MARK_HI} | {MARK_HI * f for f in (0.25, 0.50, 0.75, 1.00)})
tab = np.array([[_ps(m, w) for w in _wshift] for m in _marks])
fig, ax = plt.subplots(figsize=(7.6, 3.9), dpi=110)
ax.imshow(tab, cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
    'th', ['#EFF3F1', '#DCE5E2', '#E8DDC4', GOLD]), aspect='auto')
for i in range(tab.shape[0]):
    for j in range(tab.shape[1]):
        _branch = abs(_marks[i] - MARK_LO) < 1 or abs(_marks[i] - MARK_HI) < 1
        ax.text(j, i, f'{tab[i, j]:.0f}', ha='center', va='center', fontsize=10, color=INK,
                fontweight='bold' if (_branch and _wshift[j] == 0.0) else 'normal')
ax.set_xticks(range(len(_wshift)),
              [f'{(_DCF["forward_wacc"][0]+w)*100:.1f}%' for w in _wshift])
ax.set_yticks(range(len(_marks)),
              [f'{m:,.0f}' + ('  \u2021' if (abs(m - MARK_LO) < 1 or abs(m - MARK_HI) < 1) else '')
               for m in _marks])
ax.set_xlabel('first-year cost of capital on the Auto leg (the whole ladder moves with it)')
ax.set_ylabel('MNT-Halan mark (EGP mn)')
ax.set_title('Sum-of-the-parts fair value (EGP/share) — the associate mark \u00d7 the cost of capital\n'
             '\u2021 marks the two published branches; bold cells are the published answers',
             fontsize=9.5, pad=8)
ax.grid(False); fig.tight_layout(); fig.savefig('fig2_sens.png'); plt.close(fig)

# ---- F3 MA stack ------------------------------------------------------------
s = df.set_index('Date')['Price'].iloc[-260:]
fig, ax = plt.subplots(figsize=(10.5, 4.1), dpi=110)
ax.plot(s.index, s.values, color=INK, lw=1.7, label='GBCO close')
for n, c in [(20, GOLD), (50, BRASS), (100, SAGE), (200, '#7B8D88')]:
    ma = df.set_index('Date')['Price'].rolling(n).mean().iloc[-260:]
    ax.plot(ma.index, ma.values, color=c, lw=1.2, label=f'SMA {n}')
ax.legend(frameon=False, fontsize=8.5, ncol=5, labelcolor=INK, loc='upper left')
ax.set_title('GBCO — price versus the moving-average stack, last 260 sessions', fontsize=10, pad=8)
ax.set_ylabel('EGP'); style(ax)
fig.tight_layout(); fig.savefig('fig3_ma.png'); plt.close(fig)

# ---- F4 fan chart ------------------------------------------------------------
fan = np.load('fan.npy'); days = np.arange(fan.shape[1])
fig, ax = plt.subplots(figsize=(10.5, 4.5), dpi=110)
ax.fill_between(days, fan[0], fan[4], color=GOLD, alpha=0.14, label='5–95%')
ax.fill_between(days, fan[1], fan[3], color=GOLD, alpha=0.32, label='25–75% (the 50% band)')
ax.plot(days, fan[2], color=INK, lw=2, label='median')
ax.axhline(spot, color=GREY, lw=1.2, ls=':')
# BOTH BRANCHES ARE DRAWN AND THE AXIS IS WIDENED TO HOLD THEM. A reference line outside
# the limits is thrown away silently and the label then floats over nothing.
for _v, _lab in ((V_LO, BR[0]['label']), (V_HI, BR[1]['label'])):
    ax.axhline(_v, color=BRASS, lw=1.4, ls='--')
    ax.text(1, _v + 0.4, f'{_lab} — {_v:.2f}', color=BRASS, fontsize=8.4)
ax.text(1, spot - 1.3, f'spot {spot:.2f}', color=GREY, fontsize=8.6)
_ylo = min(fan[0].min(), spot, V_LO, V_HI)
_yhi = max(fan[4].max(), spot, V_LO, V_HI)
ax.set_ylim(_ylo - 0.06 * (_yhi - _ylo), _yhi + 0.10 * (_yhi - _ylo))
ax.set_xlabel('trading sessions ahead'); ax.set_ylabel('EGP / share')
ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc='lower left')
ax.set_title('Forward price cone to 3 months — 50,000 simulated paths, fat-tailed, with the '
             'drift this stock’s own history supports',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('fig4_fan.png'); plt.close(fig)

# ---- F5/F6 distributions -----------------------------------------------------
for tag, fn in [('1 month', 'pT20.npy'), ('3 months', 'pT60.npy')]:
    x = np.load(fn)
    fig, ax = plt.subplots(figsize=(7.6, 3.8), dpi=110)
    ax.hist(x, bins=90, color=GOLD, alpha=0.9, edgecolor='#FFFFFF', linewidth=0.2)
    ax.axvline(spot, color=INK, lw=1.6)
    ax.axvline(np.median(x), color=BRASS, lw=1.6, ls='--')
    ax.text(spot, ax.get_ylim()[1]*0.94, f' spot {spot:.2f}', color=INK, fontsize=8.4)
    ax.text(np.median(x), ax.get_ylim()[1]*0.84, f' median {np.median(x):.1f}', color=BRASS, fontsize=8.4)
    ax.set_xlim(np.percentile(x, 0.3), np.percentile(x, 99.7))
    ax.set_xlabel('EGP / share'); ax.set_yticks([])
    ax.set_title(f'Price distribution at {tag}', fontsize=10, pad=8)
    style(ax); fig.tight_layout()
    fig.savefig(f"fig{'5' if tag=='1 month' else '6'}_dist.png"); plt.close(fig)

# ---- FB1 calibration 3-panel --------------------------------------------------
bt = pd.read_csv('backtest_rows.csv', parse_dates=['origin'])
fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9), dpi=110)
a = axes[0]
a.plot(df['Date'], df['Price'], color=INK, lw=1.0, label='realized')
for _, r in bt.iterrows():
    o = r['origin']; e = o + pd.Timedelta(days=88)
    a.fill_between([o, e], [r['spot'], r['p5']], [r['spot'], r['p95']], color=GOLD, alpha=0.22)
    a.plot([e], [r['realized']], marker='o', ms=3, color=BRASS)
a.set_yscale('log'); a.set_title('Quarterly cone replay (log scale)', fontsize=9.5)
a.set_ylabel('EGP'); style(a)
b = axes[1]
b.bar(np.arange(10) / 10 + 0.05, np.array(d['step0']['pit_hist']) / d['step0']['n_rows'],
      width=0.09, color=GOLD, edgecolor='#FFFFFF')
b.axhline(0.1, color=INK, ls='--', lw=1)
b.set_title('Where outcomes landed inside the cone (n=%d, non-overlapping windows)'
            % d['step0']['nonoverlap']['n'], fontsize=9.5)
b.set_xlabel('position inside the cone, 0 = bottom, 1 = top'); style(b)
c = axes[2]
so = d['step0']['nonoverlap']
cov = [so['cov50'], so['cov80'], so['cov90']]
c.bar([0, 1, 2], [x * 100 for x in cov], width=0.5, color=GOLD, edgecolor='#FFFFFF')
for i, t in enumerate([50, 80, 90]):
    c.plot([i - 0.32, i + 0.32], [t, t], color=INK, ls='--', lw=1.4)
c.set_xticks([0, 1, 2], ['50% band', '80% band', '90% band'])
c.set_ylim(0, 105); c.set_title('Interval coverage vs target', fontsize=9.5)
c.text(0.02, 0.94,
       'score against a naive benchmark %+.1f%% (n=%d)\nmonthly origins %+.1f%% (n=%d)'
       % (so['crps_skill'] * 100, so['n'],
          d['step0']['monthly']['crps_skill'] * 100, d['step0']['monthly']['n']),
       transform=c.transAxes, fontsize=8.2, color=INK, va='top')
style(c)
fig.suptitle('GBCO — testing the price cone on this stock’s own history: the quarterly replay, '
             'where outcomes landed, and how often the bands held',
             fontsize=10, color=INK, y=1.02)
fig.tight_layout(); fig.savefig('figB1_calibration.png', bbox_inches='tight'); plt.close(fig)
# site-style copy for the ledger
import shutil; shutil.copy('figB1_calibration.png', 'calibration_GBCO.png')

# ---- FD1 experts -------------------------------------------------------------
# EVERY RANGE IS READ FROM THE RECORD. The three spans were TYPED here and two of the
# three disagreed with the study's own numbers — Expert 1's brass tick sat outside its own
# bar and outside the axis entirely, because his base came from the model and his range did
# not. All three now come from experts.{e1,e2,e3}.rng, which compute.py derives from each
# expert's own stated levers.
E = d['experts']
ex = [('Expert 1 — split-legs net asset value', E['e1']['base'], tuple(E['e1']['rng'])),
      ('Expert 2 — residual income on the group', E['e2']['base'], tuple(E['e2']['rng'])),
      ('Expert 3 — return on capital vs its cost', E['e3']['base'], tuple(E['e3']['rng']))]
_ELO = min(min(r) for _, _, r in ex + [(0, 0, (spot,))])
_EHI = max(max(r) for _, _, r in ex)
_ESPAN = _EHI - _ELO
_EPAD = _ESPAN * 0.012
_EBASES = sorted(b for _, b, _ in ex)
fig, ax = plt.subplots(figsize=(9.7, 3.3), dpi=110)
for i, (nm, ba, (lo, hi)) in enumerate(ex):
    y = len(ex) - 1 - i
    ax.barh(y, hi - lo, left=lo, height=0.42, color=SAGE, alpha=0.32, edgecolor=SAGE)
    ax.plot([ba, ba], [y - 0.21, y + 0.21], color=BRASS, lw=3.4)
    ax.text(hi + _EPAD, y, f'{lo:.0f}–{hi:.0f} · base {ba:.1f}', va='center', fontsize=8.6,
            color=INK)
ax.axvline(spot, color=INK, lw=1.6)
# the gold band is the PANEL CENTRE — the middle expert's base, not a typed pair of levels
ax.axvspan(_EBASES[1] * 0.95, _EBASES[1] * 1.05, color=GOLD, alpha=0.13)
ax.set_yticks(range(len(ex)), [e[0] for e in ex][::-1], fontsize=9)
ax.set_xlabel('EGP / share')
ax.set_xlim(_ELO - _EPAD, _EHI + _ESPAN * 0.22)
ax.set_ylim(-0.75, len(ex) - 0.4)
ax.text(spot + _EPAD, -0.62, f'spot {spot:.2f}', fontsize=8.6, color=INK, va='center')
ax.set_title('The three experts’ fair-value ranges — brass = base; gold band = panel centre',
             fontsize=10, pad=8)
style(ax); fig.tight_layout(); fig.savefig('figD1_experts.png'); plt.close(fig)
print('figures done')
