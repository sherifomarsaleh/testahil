"""Compute the technical read for ADNOCDRILL and write technicals.json.

The shared technical module reads from the persistent price library at
engine/raw_ohlc/{MARKET}/{TICKER}.csv. ADNOCDRILL is NOT in that library: placing
it there is a publication step, and it is deliberately not taken by this study.
So this script stages the study's own copy of the price file into the library
just long enough to compute the read, and removes it again if it put it there.

Everything the module produces is a closed-form function of the cleaned series —
moving averages and their slope states, Wilder's relative-strength index and
average true range, the convergence-divergence oscillator, cross recency, the
52-week range, and support and resistance from recency-weighted pivot clusters.
Nothing is fitted and nothing is forecast, so re-running it on an unchanged
series is a no-op.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import technicals as T

SRC = os.path.join(HERE, 'ADNOCDRILL_Stock_Price_History.csv')
DST = os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'ADNOCDRILL.csv')
COMPUTED_ON = '2026-08-09'

staged = not os.path.exists(DST)
if staged:
    shutil.copyfile(SRC, DST)
try:
    st = T.compute('AE', 'ADNOCDRILL', computed_on=COMPUTED_ON)
finally:
    if staged:
        os.remove(DST)

json.dump(st, open(os.path.join(HERE, 'technicals.json'), 'w'), indent=1, default=str)
print(T.pretty(st))
print(f"\nstaged into the shared library for the read and removed again: {staged}")
