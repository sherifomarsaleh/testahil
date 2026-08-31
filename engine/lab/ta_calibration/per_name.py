"""per_name.py — the per-name calibration record for a named list of stocks.

Same claims, same distance-matched two-sided null, same house bar as the pooled
run. What changes is that nothing is pooled across names, so the counts are
small and are printed beside every figure — a percentage without its count is
the number that misleads ([R-CAL-02]).

`--uploads` scores an alternative export WITHOUT writing it into the persistent
library. Nothing under raw_ohlc/ is read or modified on that path.
"""
import sys, os, json, argparse
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
import replay, score
from data_quality import clean_ohlc

# Below this a name's own figure cannot separate an honest read from a broken
# one; band_record.py derives the same floor for the same reason and the number
# is deliberately carried across rather than re-invented.
READABLE_MIN = 22


def load_upload(path):
    """A TradingView-style export mapped onto the library schema, then Step 0.0."""
    u = pd.read_csv(path)
    df = pd.DataFrame({'Date': pd.to_datetime(u['time']), 'Price': u['close'],
                       'Open': u['open'], 'High': u['high'], 'Low': u['low'],
                       # Step 0.0 reads 'Vol.' to spot pre-listing placeholder rows
                       # (flat bar AND no volume); the export calls it 'Volume'.
                       'Vol.': u['Volume']}).dropna(subset=['Date', 'Price', 'High', 'Low'])
    return df.sort_values('Date').reset_index(drop=True)


def score_name(r, months, side=None):
    d = r[(r.claim == 'level') & (r.months == months) & (r.n_sides == 2)]
    if side:
        d = d[d.side == side]
    both = d[d.touched & d.p_touched].dropna(subset=['p_broke'])
    n = len(both)
    if n == 0:
        return dict(months=months, side=side or 'all', n=0, readable=False)
    diff = (both.p_broke - both.broke.astype(float)).to_numpy()
    out = dict(months=months, side=side or 'all', n=int(n),
               readable=bool(n >= READABLE_MIN),
               broke_real=float(both.broke.mean()), broke_null=float(both.p_broke.mean()),
               delta=float(diff.mean()),
               dist_real=float(both.dist.mean()), dist_null=float(both.p_touch_dist.mean()))
    if n >= READABLE_MIN:
        ci = score.block_boot(diff, np.zeros(n))
        out['ci'] = {str(k): v for k, v in ci.items()}
        out['verdict'] = score.robust(ci)
    return out


def state_rows(r, months):
    from scipy import stats
    s = r[(r.claim == 'state') & (r.months == months)]
    if not len(s):
        return {}
    v = s.dropna(subset=['atr_pct', 'rlz_vol'])
    rho = float(stats.spearmanr(v.atr_pct, v.rlz_vol)[0]) if len(v) > 10 else float('nan')
    above = s[s.trend.str.startswith('Trading above the whole')]
    below = s[s.trend.str.startswith('Trading below the whole')]
    return dict(n=int(len(s)), base_up=float((s.fwd_ret > 0).mean()), tape_spearman=rho,
                stack_above_n=int(len(above)),
                stack_above_up=float((above.fwd_ret > 0).mean()) if len(above) else float('nan'),
                stack_below_n=int(len(below)),
                stack_below_up=float((below.fwd_ret > 0).mean()) if len(below) else float('nan'))


U = '/root/.claude/uploads/972d4834-4b15-5e35-8d2b-653ceed1c887/'
NAMES = [('AE', 'LULU',     U + '6c4fe75f-ADX_LULU_1D.csv'),
         ('AE', 'SALIK',    U + '193a1cb8-DFM_DLY_SALIK_1D.csv'),
         ('AE', 'EMAAR',    U + 'cf94e5a8-DFM_DLY_EMAAR_1D.csv'),
         ('AE', 'EMAARDEV', U + 'a891bd31-DFM_DLY_EMAARDEV_1D.csv'),
         ('AE', 'ENBD',     U + '07977c4b-DFM_DLY_EMIRATESNBD_1D.csv'),
         ('AE', 'FAB',      U + 'ec2ea478-ADX_FAB_1D.csv'),
         ('AE', 'IHC',      U + '068cfb0d-ADX_IHC_1D.csv')]

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--uploads', action='store_true')
    a = ap.parse_args()
    out = {}
    for mkt, tkr, path in NAMES:
        frame = None
        if a.uploads:
            raw = load_upload(path)
            df, rep = clean_ohlc(raw, tkr, verbose=False, market=mkt)
            frame = (df.reset_index(drop=True), {'rows_in': len(raw), 'repairs': list(rep)})
        r = replay.harvest(mkt, tkr, frame=frame)
        if not len(r):
            src = frame[0] if frame else None
            n = len(src) if src is not None else None
            print(f"--- {tkr} | NOT SCOREABLE: {n if n else '<'+str(replay.MIN_HISTORY)} clean "
                  f"sessions against a first origin at {replay.MIN_HISTORY}. "
                  f"The read IS published for this name; the calibration cannot reach it. ---\n",
                  flush=True)
            out[tkr] = dict(scoreable=False, clean_sessions=n, min_history=replay.MIN_HISTORY)
            continue
        rec = {'rows': int(len(r)), 'origins': int(r[r.claim == 'state'].origin.nunique()),
               'first': r.origin.min(), 'last': r.origin.max(), 'levels': [], 'state': {}}
        for months in (1, 3):
            for side in (None, 'res', 'sup'):
                rec['levels'].append(score_name(r, months, side))
            rec['state'][months] = state_rows(r, months)
        out[tkr] = rec
        print(f"--- {tkr} | {rec['origins']} origins {rec['first']} -> {rec['last']} ---", flush=True)
        for c in rec['levels']:
            if not c['n']:
                continue
            tail = (f"[{c['verdict']}]" if c['readable']
                    else f"(n<{READABLE_MIN} — not readable alone)")
            print(f"  {c['months']}M {c['side']:4} n={c['n']:>3}  real {c['broke_real']:.3f} "
                  f"null {c['broke_null']:.3f}  delta {c['delta']:+.4f}  {tail}", flush=True)
        for months, s in rec['state'].items():
            print(f"  {months}M state n={s['n']:>3} base-up {s['base_up']:.3f} | tape rho "
                  f"{s['tape_spearman']:+.3f} | stack-above {s['stack_above_up']:.3f} "
                  f"(n={s['stack_above_n']}) stack-below {s['stack_below_up']:.3f} "
                  f"(n={s['stack_below_n']})", flush=True)
        print(flush=True)
    json.dump(out, open(os.path.join(HERE, 'RESULTS_per_name%s.json'
                                     % ('_uploads' if a.uploads else '')), 'w'),
              indent=1, default=float)
