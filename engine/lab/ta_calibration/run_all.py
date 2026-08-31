import os, sys, time, glob
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replay import harvest

RAW = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'raw_ohlc'))
out, skipped = [], []
t0 = time.time()
for mkt in sorted(os.listdir(RAW)):
    for f in sorted(glob.glob(os.path.join(RAW, mkt, '*.csv'))):
        tkr = os.path.basename(f)[:-4]
        try:
            r = harvest(mkt, tkr)
            if len(r):
                out.append(r)
                print(f'{mkt}/{tkr}: {len(r)} rows', flush=True)
            else:
                skipped.append((mkt, tkr, 'no windows'))
        except Exception as e:
            skipped.append((mkt, tkr, f'{type(e).__name__}: {e}'))
            print(f'{mkt}/{tkr}: SKIP {type(e).__name__}: {e}', flush=True)
r = pd.concat(out, ignore_index=True)
r.to_pickle('claims.pkl')
n_names = len(r.groupby(['market', 'ticker']))
print(f'\n=== {len(r)} claim rows, {n_names} names, '
      f'{r.market.nunique()} markets in {time.time()-t0:.0f}s ===')
print('SKIPPED:', skipped)
# COUNT AGAINST A KNOWN TOTAL — the population is the libraries on disk.
total = sum(len(glob.glob(os.path.join(RAW, m, '*.csv'))) for m in os.listdir(RAW))
# COUNT AGAINST A KNOWN TOTAL, on (market, ticker) — never the bare ticker.
# ADIB is a different bank in EG and AE and shares a filename; nunique() on the
# ticker string alone silently reported 91 of 93 and called it clean, which is
# the exact shape [R-ENF-04] exists to catch.
print(f'libraries on disk: {total} | replayed: {n_names} | skipped: {len(skipped)}')
assert n_names + len(skipped) == total, 'population mismatch'
