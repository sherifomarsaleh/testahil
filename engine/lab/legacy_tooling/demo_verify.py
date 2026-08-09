"""
Verification run — reproduces a TMGH-shaped developer study from the calibrated factor set,
to prove the engine matches the published methodology before it is adopted.

Published TMGH reference (study dated 15-06-2026), T+60:  median ~104, 5th ~76, 95th ~143.
"""
import factor_library as fl
import monte_carlo as mc
import viz

TICKER = "TMGH"
ANCHOR = 95.68          # published anchor close
REALIZED_VOL = 0.36     # annualized, from the attached OHLC history

cls, factors = fl.for_ticker(TICKER)
cont, events = fl.split(factors)
print(f"class={cls}  calibrated={fl.is_calibrated(factors)}  "
      f"continuous={len(cont)}  events={len(events)}")

net = mc.expected_factor_contribution(cont, events)
print(f"net expected 3M factor contribution = {net:+.1%}  (TMGH doc: ~+8%)")

res = mc.run(ANCHOR, REALIZED_VOL, cont, events, horizon=60, n_paths=50_000, seed=42)
print(f"simulated annualized path vol = {res.ann_path_vol:.1%}  (realized {REALIZED_VOL:.0%})\n")

print("Percentile table:")
for h, row in res.percentile_table().items():
    print(f"  {h}:  " + "  ".join(f"P{q}={v:6.2f}" for q, v in row.items()))

print("\nTouch ladder (by T+60):")
for lvl in (80, 100, 110, 120, 130, 140):
    print(f"  {lvl:>4}: {100*res.touch_probability(lvl, 60):5.1f}%")

print("\nZone probabilities (T+60):")
print(f"  < 90       : {100*res.prob_between(None, 90):5.1f}%")
print(f"  90 – 110   : {100*res.prob_between(90, 110):5.1f}%")
print(f"  110 – 130  : {100*res.prob_between(110, 130):5.1f}%")
print(f"  >= 130     : {100*res.prob_between(130, None):5.1f}%")

viz.study_panel(res, [80, 100, 110, 120, 130, 140], "demo_panel.png", ticker=TICKER)
print("\nsaved demo_panel.png")
