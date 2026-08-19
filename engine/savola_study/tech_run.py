#!/usr/bin/env python3
"""SAVOLA study — regenerate tech_read.json from the persistent library via the
production technicals module (engine/technicals.py: SMA 20/50/200 with the
10-session slope-state convention, Wilder RSI(14)/ATR(14), MACD(12,26,9),
recency-weighted fractal-pivot S/R). Committed so the study's technical read is
reproducible — the first edition produced this file ad hoc (critique finding)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import technicals

st = technicals.compute('SA', 'SAVOLA', computed_on='2026-08-19')
out = dict(state=st, narrative=st['tech'])
with open(os.path.join(HERE, 'tech_read.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)
print(f"close {st['close']} data {st['data_date']} computed {st['computed_on']}")
print(f"MA20 {st['ma'][20]:.2f} ({st['ma_slope'][20]}) | MA50 {st['ma'][50]:.2f} "
      f"({st['ma_slope'][50]}) | MA200 {st['ma'][200]:.2f} ({st['ma_slope'][200]})")
print(f"RSI {st['rsi']:.2f} | ATR {st['atr']:.3f} | MACD {st['macd']['macd']:.3f}/"
      f"{st['macd']['signal']:.3f}/{st['macd']['hist']:+.3f}")
print(f"res {st['levels']['res']} sup {st['levels']['sup']}")
print("tech_read.json written")
