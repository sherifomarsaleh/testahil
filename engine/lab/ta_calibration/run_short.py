"""Book-wide short-horizon harvest — the technical lens on its own clock."""
import os, sys, time, glob
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replay import harvest_short

RAW = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'raw_ohlc'))
out, skipped = [], []
t0 = time.time()
for mkt in sorted(os.listdir(RAW)):
    for f in sorted(glob.glob(os.path.join(RAW, mkt, '*.csv'))):
        tkr = os.path.basename(f)[:-4]
        try:
            r = harvest_short(mkt, tkr)
            if len(r):
                out.append(r)
                print(f'{mkt}/{tkr}: {len(r)} rows, '
                      f'{r[r.claim=="state"].origin.nunique()} origins', flush=True)
            else:
                skipped.append((mkt, tkr, 'no origins'))
        except Exception as e:
            skipped.append((mkt, tkr, f'{type(e).__name__}: {e}'))
r = pd.concat(out, ignore_index=True)
r.to_pickle('claims_short.pkl')
n_names = len(r.groupby(['market', 'ticker']))
total = sum(len(glob.glob(os.path.join(RAW, m, '*.csv'))) for m in os.listdir(RAW))
st = r[r.claim == 'state']
print(f'\n=== {len(r):,} rows | {n_names} names | {time.time()-t0:.0f}s ===')
print(f'ticker-origins (state rows, one horizon): {len(st[st.h==5]):,}')
print(f'origins per name: median {st[st.h==5].groupby(["market","ticker"]).size().median():.0f}')
print(f'libraries {total} | replayed {n_names} | skipped {len(skipped)}: {skipped}')
assert n_names + len(skipped) == total, 'population mismatch'
