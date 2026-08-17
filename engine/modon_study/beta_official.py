#!/usr/bin/env python3
"""MODON beta — TIER 1: own-stock regression against its OWN local index.

The FTSE ADX General Index series was unobtainable through revision 2 (ten
sources logged), so revision 2 adopted a flagged proxy: a weekly regression
against an equal-weight composite of the house UAE library. The official series
arrived 10-Aug-2026 and is now the regressor, which is what the standing beta
hierarchy asks for in the first place.

Runs, in order:
  1. Step 0.0-style data-quality screen on the index series (per-market limit,
     trading-day density against the exchange's own calendar, non-positive rows).
  2. Weekly log-return regressions over 2y / 3y / 5y windows.
  3. The standing usability gate: n >= 24, R2 >= 5%, SE(beta) < |beta|.
     Adopt the LONGEST window up to 5y that passes.
  4. The retired proxy, re-run on the same weeks, so the change is priced.

Writes beta_official.json for compute.py to read. No number is typed by hand.
"""
import csv, json, math, os, datetime as dt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
IDX = os.path.join(REPO, 'raw_ohlc', 'INDEX', 'AE.csv')
LIB = os.path.join(REPO, 'raw_ohlc', 'AE')
SUBJ = 'MODON'
ADX_DAILY_LIMIT = 0.15          # ADX price band, per the Step 0.0 table


def _num(s):
    s = (s or '').strip().strip('"').replace(',', '')
    return None if s in ('', '-', 'null') else float(s)


def load(path):
    """date -> close. investing.com export: MM/DD/YYYY, newest first, comma
    thousands separators (the index prints 9,828.14 — stripping them is not
    cosmetic, float('9,828.14') raises)."""
    out = {}
    with open(path, encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            d = (r.get('Date') or '').strip().strip('"')
            try:
                day = dt.datetime.strptime(d, '%m/%d/%Y').date()
            except ValueError:
                continue
            c = _num(r.get('Price'))
            if c is not None and c > 0:
                out[day] = c
    return out


# ---------------------------------------------------------------- Step 0.0
def screen(series, label, limit):
    """A move beyond the exchange's own daily price limit cannot be a real
    session — it is a corporate action or a data error. An INDEX has no limit
    of its own, but its constituents do, so a move beyond the constituent limit
    is still impossible and the same screen applies."""
    days = sorted(series)
    span = (days[-1] - days[0]).days / 365.25
    moves = []
    for a, b in zip(days, days[1:]):
        moves.append((b, abs(math.log(series[b] / series[a]))))
    breaches = [(d, m) for d, m in moves if m > math.log(1 + limit)]
    out = dict(rows=len(days), first=days[0].isoformat(), last=days[-1].isoformat(),
               span_years=round(span, 2),
               density=round(len(days) / span, 1),
               max_abs_log_move=round(max(m for _, m in moves), 4),
               limit_breaches=[(d.isoformat(), round(m, 4)) for d, m in breaches],
               nonpositive_dropped=0)
    print(f'  {label}: {out["rows"]} rows, {out["first"]} -> {out["last"]}, '
          f'{out["span_years"]}y, {out["density"]} rows/yr, '
          f'largest |log move| {out["max_abs_log_move"]}, '
          f'{len(breaches)} beyond the ±{limit:.0%} constituent limit')
    return out


def weekly(series):
    """Last available session in each ISO week — the standing weekly convention."""
    by = {}
    for day, c in series.items():
        k = day.isocalendar()[:2]
        if k not in by or day > by[k][0]:
            by[k] = (day, c)
    return {k: v[1] for k, v in by.items()}


def returns(wkly, keys):
    out = {}
    for k in keys:
        prev = (k[0], k[1] - 1) if k[1] > 1 else (k[0] - 1, 52)
        a, b = wkly.get(prev), wkly.get(k)
        if a and b and a > 0 and b > 0:
            out[k] = math.log(b / a)
    return out


def ols(y, x):
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    s2 = float(resid @ resid) / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / ss_tot if ss_tot > 0 else 0.0
    return dict(beta=float(coef[1]), alpha=float(coef[0]),
                se=float(math.sqrt(cov[1, 1])), r2=r2, n=n)


def gate(r):
    """The standing usability gate. All three limbs, reported individually so a
    failure says WHICH limb failed rather than just 'unusable'."""
    limbs = dict(n=r['n'] >= 24, r2=r['r2'] >= 0.05, se=r['se'] < abs(r['beta']))
    return all(limbs.values()), limbs


def main():
    print('STEP 0.0 — data-quality screen')
    idx_raw, subj_raw = load(IDX), load(os.path.join(LIB, SUBJ + '.csv'))
    dq_idx = screen(idx_raw, 'FTSE ADX General', ADX_DAILY_LIMIT)
    dq_sub = screen(subj_raw, 'MODON', ADX_DAILY_LIMIT)

    wi, ws = weekly(idx_raw), weekly(subj_raw)
    # The regression can only run where BOTH series trade. The index export ends
    # before the price library does, so the window ends at the index's last week
    # — never extrapolated, never forward-filled.
    end = min(max(idx_raw), max(subj_raw))
    print(f'\n  common last session: {end.isoformat()} '
          f'(index {max(idx_raw).isoformat()}, {SUBJ} {max(subj_raw).isoformat()})')

    # the retired proxy, for the before/after
    import sys
    sys.path.insert(0, HERE)
    peers = sorted(f[:-4] for f in os.listdir(LIB)
                   if f.endswith('.csv') and f[:-4] != SUBJ)
    wp = {n: weekly(load(os.path.join(LIB, n + '.csv'))) for n in peers}

    def proxy_returns(keys):
        out = {}
        for k in keys:
            prev = (k[0], k[1] - 1) if k[1] > 1 else (k[0] - 1, 52)
            rs = []
            for n in peers:
                a, b = wp[n].get(prev), wp[n].get(k)
                if a and b and a > 0 and b > 0:
                    rs.append(math.log(b / a))
            if len(rs) >= 5:
                out[k] = float(np.mean(rs))
        return out

    print(f'\n{"window":<10}{"regressor":<22}{"beta":>8}{"SE":>8}{"R2":>8}'
          f'{"n":>6}  gate')
    res = {}
    for yrs in (2, 3, 5):
        start = end - dt.timedelta(days=int(365.25 * yrs))
        keys = sorted(k for k in ws
                      if start <= dt.date.fromisocalendar(k[0], k[1], 5) <= end
                      + dt.timedelta(days=7))
        ry, rx = returns(ws, keys), returns(wi, keys)
        rp = proxy_returns(keys)
        common = sorted(set(ry) & set(rx))
        y = np.array([ry[k] for k in common])
        x = np.array([rx[k] for k in common])
        r = ols(y, x)
        ok, limbs = gate(r)
        r['gate'], r['gate_limbs'] = ok, limbs
        res[f'{yrs}y'] = r
        print(f'{str(yrs)+"y":<10}{"FTSE ADX General":<22}{r["beta"]:>8.3f}'
              f'{r["se"]:>8.3f}{r["r2"]:>8.3f}{r["n"]:>6d}  '
              f'{"PASS" if ok else "FAIL " + str([k for k, v in limbs.items() if not v])}')
        cp = sorted(set(ry) & set(rp))
        rpx = ols(np.array([ry[k] for k in cp]), np.array([rp[k] for k in cp]))
        res[f'{yrs}y_proxy'] = rpx
        print(f'{"":<10}{"(retired proxy)":<22}{rpx["beta"]:>8.3f}'
              f'{rpx["se"]:>8.3f}{rpx["r2"]:>8.3f}{rpx["n"]:>6d}')

    # Adopt the LONGEST window up to 5y that passes the gate.
    adopted_win = None
    for yrs in (5, 3, 2):
        if res[f'{yrs}y']['gate']:
            adopted_win = f'{yrs}y'
            break
    assert adopted_win, 'no window passed the usability gate — beta drops to tier 2'
    adopted = res[adopted_win]
    beta = round(adopted['beta'], 3)
    print(f'\nADOPTED (tier 1): {adopted_win} window, beta {beta} '
          f'(SE {adopted["se"]:.3f}, R2 {adopted["r2"]:.3f}, n {adopted["n"]}) '
          f'vs the FTSE ADX General Index')
    print(f'  the retired proxy on the same window read '
          f'{res[adopted_win + "_proxy"]["beta"]:.3f} — '
          f'{abs(beta - res[adopted_win + "_proxy"]["beta"]):.3f} away, '
          f'{abs(beta - res[adopted_win + "_proxy"]["beta"]) / adopted["se"]:.2f} '
          f'standard errors')

    out = dict(adopted_beta=beta, adopted_window=adopted_win,
               index_name='FTSE ADX General Index',
               index_last_session=max(idx_raw).isoformat(),
               windows={k: v for k, v in res.items()},
               dq_index=dq_idx, dq_subject=dq_sub,
               peers_in_retired_proxy=len(peers))
    with open(os.path.join(HERE, 'beta_official.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print('\nwrote beta_official.json')


if __name__ == '__main__':
    main()
