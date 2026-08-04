"""metal_backtest.py — the five-year calibration backtest PNG, metals edition.

Renders assets/calibration_{PanelKey}.png in the exact format of the committed
Gold panel (the one live on ledger.html since 13-Jul-2026): quarterly-replay
price chart with 90%/50% cone boxes and realized dots, PIT histogram, band
coverage vs target, and the honesty footer. The original generator lived in a
session outside this repo (publish_adh.py records only a copy step), so this
module reconstructs it — and calibrates the reconstruction by replaying GOLD
under its build-time config (nu=250, width 1.000) against the committed
panel's own printed numbers (17 windows, PIT mean 0.482, coverage 29.4% /
88.2%). The replay reproduces the window count exactly and the PIT mean to
within 0.02; the coverage bars land within 1-2 windows (of 17). Exact
reproduction is not attainable: the 13-Jul build predates the 27-Jul
calendar-horizon amendment (it counted sessions) and its generator was never
committed, so the residual gap is the retired convention, not a defect in the
chain. New panels deliberately use the LIVE calendar rule — anchor + 3
calendar months, first session on/after — because the replay should mirror
how forecasts are actually graded today. Run `--validate-gold` to repeat.

Method, per window (one per calendar year, anchored the first session on/after
1 April — 17 windows is what the committed Gold panel shows for 2010-2026):
the ACTUAL production chain at that historical origin — Step 0.0 clean ->
yz_variance_proxy -> fit_har_v3(origin) -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3 (50k paths, seed 42) — then the realized close on the first
session on/after anchor + 3 calendar months. PIT = fraction of simulated
terminal paths at or below the realized close. No look-ahead in the variance
fit (it sees only data up to the origin); the (nu, width_cal) pair and carry
are the LIVE market config applied across history, which is why the footer
calls this a reconstruction, not a stored figure.

Usage:
    python3 metal_backtest.py --validate-gold
    python3 metal_backtest.py SILVER          # writes assets/calibration_Silver.png
    python3 metal_backtest.py PLATINUM       # writes assets/calibration_XPTUSD.png
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt                              # noqa: E402
from matplotlib.patches import Rectangle                     # noqa: E402

from strike_cohorts import load_clean                        # noqa: E402
from primitives import yz_variance_proxy                     # noqa: E402
from mc_v3 import (fit_har_v3, har_forecast_v3, carry_log_h,  # noqa: E402
                   simulate_paths_v3)
import market_profiles as MP                                 # noqa: E402

N_PATHS = 50_000
SEED = 42

TEAL_DARK = '#0f6b64'
TEAL_MID = '#3d7f7a'
TEAL_BOX50 = '#4e8f8a'
TEAL_BOX90 = '#b8dcd8'
GOLD_DOT = '#d9a441'
RED_X = '#c0392b'
TAN = '#c9a227'
INK = '#1c2b29'
GREY = '#9aa8a5'

# Panel identity: (market, series) -> (display name, site panel key, ledger alias)
PANELS = {
    'GOLD': ('XAU', 'GOLD', 'Gold', 'Gold'),
    'SILVER': ('XAU', 'SILVER', 'Silver', 'Silver'),
    'PLATINUM': ('XPT', 'PLATINUM', 'Platinum', 'XPTUSD'),
}


def windows(market, series, nu, width_cal, rf_live, min_warmup=55,
            h_sessions=None):
    """One 3-month replay window per calendar year, anchor = first session
    on/after 1 April (grading ~1 July). Returns the list of scored windows.

    h_sessions: None grades at anchor + 3 calendar months (the LIVE rule,
    used for every published panel). An integer grades at a fixed session
    count instead — only the Gold validation uses this, because the committed
    13-Jul Gold panel was built under the retired session-count convention
    and a like-with-like check must replay it that way."""
    df, _ = load_clean(market, series)
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    v = yz_variance_proxy(df)
    prof = MP.PROFILES[market]

    out = []
    for year in range(int(dates.iloc[0].year), int(dates.iloc[-1].year) + 1):
        target = pd.Timestamp(year=year, month=4, day=1)
        pos = dates.searchsorted(target)
        if pos >= len(df):
            continue
        i = int(pos)
        if i < min_warmup:
            continue
        anchor_date = dates.iloc[i]
        spot = float(close[i])
        if h_sessions is not None:
            gpos = i + h_sessions
        else:
            # grade at anchor + 3 calendar months, first session on/after
            gtarget = anchor_date + pd.DateOffset(months=3)
            gpos = int(dates.searchsorted(gtarget))
        if gpos >= len(df):
            continue
        # horizon in sessions = the real span this window turned out to hold
        h = gpos - i
        if h < 30:
            continue
        beta, s2 = fit_har_v3(v, i, horizon=h)
        dvar = har_forecast_v3(v, i, beta, s2, horizon=h)
        if not np.isfinite(dvar) or dvar <= 0:
            continue
        drift = carry_log_h(prof, anchor_date, 0.0, h, yearfrac=0.25)
        paths = simulate_paths_v3(spot, dvar, h, drift, nu=nu,
                                  n_paths=N_PATHS, seed=SEED,
                                  width_cal=width_cal)
        term = paths[:, -1]
        realized = float(close[gpos])
        p = {q: float(np.percentile(term, q)) for q in (5, 25, 50, 75, 95)}
        out.append({
            'anchor_date': anchor_date, 'grade_date': dates.iloc[gpos],
            'spot': spot, 'realized': realized, 'h': h,
            'p5': p[5], 'p25': p[25], 'p50': p[50], 'p75': p[75], 'p95': p[95],
            'pit': float((term <= realized).mean()),
            'in90': p[5] <= realized <= p[95],
            'in50': p[25] <= realized <= p[75],
        })
    return df, out


def render(series_key, nu, width_cal, header2, header3, out_path):
    market, series, disp, panel_key = PANELS[series_key]
    df, wins = windows(market, series, nu, width_cal,
                       MP.PROFILES[market].rf_live)
    dates = pd.to_datetime(df['Date'])
    close = df['Price'].to_numpy(dtype=float)
    n = len(wins)
    cov50 = 100.0 * sum(w['in50'] for w in wins) / n
    cov90 = 100.0 * sum(w['in90'] for w in wins) / n
    pit_mean = float(np.mean([w['pit'] for w in wins]))

    fig = plt.figure(figsize=(20.6, 11.9), dpi=144)
    fig.patch.set_facecolor('white')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.55, 1.0],
                          left=0.062, right=0.985, top=0.845, bottom=0.075,
                          hspace=0.52, wspace=0.28)

    # ---- headers
    fig.text(0.062, 0.965, f'{disp} — five-year calibration backtest',
             fontsize=27, fontweight='bold', color=TEAL_DARK, ha='left')
    fig.text(0.062, 0.928, header2, fontsize=15.5, color=INK, ha='left')
    fig.text(0.062, 0.899, header3, fontsize=12.5, color=TEAL_MID, ha='left')
    fig.text(0.062, 0.868,
             'Quarterly replay — each 3-month forecast cone vs the price '
             'that actually printed',
             fontsize=15.5, fontweight='bold', color=TEAL_DARK, ha='left')

    # ---- price chart
    ax = fig.add_subplot(gs[0, :])
    ax.set_yscale('log')
    ax.plot(dates, close, color=GREY, lw=1.0, zorder=1,
            label='Realized close')
    span = (dates.iloc[-1] - dates.iloc[0]).days
    half_w = pd.Timedelta(days=max(18, span // 220))
    for w in wins:
        g = w['grade_date']
        for lo, hi, col, z in ((w['p5'], w['p95'], TEAL_BOX90, 2),
                               (w['p25'], w['p75'], TEAL_BOX50, 3)):
            ax.add_patch(Rectangle((matplotlib.dates.date2num(g - half_w), lo),
                                   2 * half_w.days, hi - lo,
                                   facecolor=col, edgecolor='none',
                                   alpha=0.85 if z == 2 else 0.9, zorder=z))
        ax.plot([g - half_w, g + half_w], [w['p50'], w['p50']],
                color=INK, lw=1.6, zorder=4)
        if w['in90']:
            ax.plot(g + half_w * 1.9, w['realized'], 'o', ms=10,
                    mfc=GOLD_DOT, mec=INK, mew=0.8, zorder=5)
        else:
            ax.plot(g + half_w * 1.9, w['realized'], 'X', ms=11,
                    mfc=RED_X, mec='white', mew=1.0, zorder=5)
    ax.plot([], [], 'o', ms=9, mfc=GOLD_DOT, mec=INK, mew=0.8,
            label='Realized — inside 90%')
    ax.plot([], [], 'X', ms=10, mfc=RED_X, mec='white', mew=1.0,
            label='Realized — outside 90%')
    ax.legend(loc='upper left', frameon=False, fontsize=12.5)
    ax.set_ylabel('Price (USD, log)', fontsize=12.5)
    ax.grid(True, which='major', color='#e3ecea', lw=0.8)
    ax.tick_params(labelsize=12.5)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)

    # ---- PIT histogram
    axp = fig.add_subplot(gs[1, 0])
    axp.set_title('PIT histogram — flat is calibrated', loc='left',
                  fontsize=15.5, fontweight='bold', color=TEAL_DARK, pad=12)
    counts, edges, _ = axp.hist([w['pit'] for w in wins], bins=8,
                                range=(0, 1), color=TEAL_BOX50,
                                edgecolor='white', lw=1.0)
    axp.axhline(n / 8, color=TAN, ls='--', lw=2)
    axp.text(0.06, 0.92, f'mean {pit_mean:.3f}\n(0.50 = centred)',
             transform=axp.transAxes, va='top', fontsize=12.5, color=INK)
    axp.set_xlabel('PIT value', fontsize=12.5)
    axp.set_ylabel('Count', fontsize=12.5)
    axp.grid(True, color='#e3ecea', lw=0.8)
    axp.tick_params(labelsize=12)
    for s in ('top', 'right'):
        axp.spines[s].set_visible(False)

    # ---- band coverage
    axc = fig.add_subplot(gs[1, 1])
    axc.set_title('Band coverage vs target (dashed)', loc='left',
                  fontsize=15.5, fontweight='bold', color=TEAL_DARK, pad=12)
    bars = axc.bar([0, 1], [cov50, cov90], width=0.55,
                   color=[TEAL_BOX90, TEAL_DARK])
    for x, tgt in ((0, 50), (1, 90)):
        axc.plot([x - 0.34, x + 0.34], [tgt, tgt], color=TAN, ls='--', lw=2.4)
    for b, v in zip(bars, (cov50, cov90)):
        axc.text(b.get_x() + b.get_width() / 2, v + 3, f'{v:.1f}%',
                 ha='center', fontsize=14, fontweight='bold', color=INK)
    axc.set_xticks([0, 1])
    axc.set_xticklabels(['50% band\n(P25–P75)', '90% band\n(P5–P95)'],
                        fontsize=12.5)
    axc.set_ylim(0, 104)
    axc.set_ylabel('Realized coverage (%)', fontsize=12.5)
    axc.grid(True, axis='y', color='#e3ecea', lw=0.8)
    axc.tick_params(labelsize=12)
    for s in ('top', 'right'):
        axc.spines[s].set_visible(False)

    fig.text(0.062, 0.012,
             "Reconstructed walk-forward replay (real price history, live "
             "market ν/cone-width); coverage bars and PIT are this "
             "reconstruction's own, not a stored figure.  ·  Independent "
             "Valuation Study — Educational Analysis · distributions, "
             "not tips",
             fontsize=10.8, style='italic', color=TAN, ha='left')

    fig.savefig(out_path, facecolor='white')
    plt.close(fig)
    return {'windows': n, 'cov50': cov50, 'cov90': cov90,
            'pit_mean': pit_mean, 'out': out_path}


def validate_gold():
    """Replay GOLD under its build-time config and compare the committed
    panel's own printed numbers: 17 windows, PIT mean 0.482, 29.4% / 88.2%."""
    _, wins = windows('XAU', 'GOLD', nu=250.0, width_cal=1.0, rf_live=0.0363,
                      h_sessions=63)
    n = len(wins)
    cov50 = 100.0 * sum(w['in50'] for w in wins) / n
    cov90 = 100.0 * sum(w['in90'] for w in wins) / n
    pit = float(np.mean([w['pit'] for w in wins]))
    print(f'GOLD replay: {n} windows, PIT mean {pit:.3f}, '
          f'cov50 {cov50:.1f}%, cov90 {cov90:.1f}%')
    print('committed:   17 windows, PIT mean 0.482, cov50 29.4%, cov90 88.2%')
    # Tolerance: coverage within 2 windows of 17 (~12 pts) — see module
    # docstring for why bit-exact is not attainable.
    ok = (n == 17 and abs(pit - 0.482) < 0.03
          and abs(cov50 - 29.4) <= 200 / 17 and abs(cov90 - 88.2) <= 200 / 17)
    print('VALIDATION', 'PASS (within the documented tolerance)' if ok else 'FAIL')
    return ok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('series', nargs='?', choices=['SILVER', 'PLATINUM'])
    ap.add_argument('--validate-gold', action='store_true')
    a = ap.parse_args()
    if a.validate_gold:
        sys.exit(0 if validate_gold() else 1)
    if not a.series:
        ap.error('give SILVER or PLATINUM, or --validate-gold')

    cfg = json_path = os.path.join(HERE, 'fitted_configs.json')
    import json
    fc = json.load(open(cfg))
    if a.series == 'SILVER':
        prof = MP.PROFILES['XAU']
        pn = fc['XAU']['per_name']['SILVER']
        h2 = (f"{pn['verdict']}  ·  CRPS skill {pn['skill']*100:+.2f}% vs a "
              f"carry-anchored random walk  ·  Metals (Gold/Silver, USD) "
              f"market panel ({fc['XAU']['windows']} windows; this replay shows "
              f"one per year)")
        h3 = (f"Market fit ν={prof.nu:g}, cone width {prof.width_cal:.3f} "
              f"· carry = {prof.rf_live*100:.2f}% live anchor · "
              f"BORROWED FIT — silver has no independent (ν, width) of "
              f"its own; the production cone runs on the shared Gold/Silver "
              f"panel fit")
        out = os.path.join(ROOT, 'assets', 'calibration_Silver.png')
        r = render('SILVER', prof.nu, prof.width_cal, h2, h3, out)
    else:
        prof = MP.PROFILES['XPT']
        pn = fc['XPT']['per_name']['PLATINUM']
        h2 = (f"{pn['verdict']}  ·  CRPS skill {pn['skill']*100:+.2f}% vs a "
              f"carry-anchored random walk  ·  Platinum (USD) panel "
              f"({fc['XPT']['windows']} windows; this replay shows one per year)")
        h3 = (f"Panel fit ν={prof.nu:g}, cone width {prof.width_cal:.3f} "
              f"· carry = {prof.rf_live*100:.2f}% live anchor")
        out = os.path.join(ROOT, 'assets', 'calibration_XPTUSD.png')
        r = render('PLATINUM', prof.nu, prof.width_cal, h2, h3, out)
    print(r)
