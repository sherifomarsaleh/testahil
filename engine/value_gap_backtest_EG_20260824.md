# Value-gap backtest — EG (Phase C)

Protocol: `Fundamental_MC_Integration_Protocol.md §8 (Phase C)`  
Signal: `G = ln(fair_base / spot) / sigma_h`, point-in-time from the git history of `assets/data.js`.  
Scored against forward log return **net of carry** via `direction_score.py` (Phase B). CRPS is not used.

### 1M horizon

- n = **32**
- IC (Spearman) = **-0.140**  (p=0.446, Pearson -0.177)
- IC 90% CI, block 2 = [-0.409, +0.221] → PARITY
- bootstrap verdict (blocks [2, 3, 4]) = **PARITY**
- hit rate = **56.2%** on 32 (95% CI 39.3%–71.8%, null 50%)
- LONO IC range [-0.219, -0.044], sign stable: True
- **VERDICT: INSUFFICIENT-POWER**
  - n=32 < 100. IC -0.140 is DESCRIPTIVE ONLY and must not be promoted: at n=32 an estimate this large is far more likely sampling noise than signal. Resolving a realistic value-signal IC of 0.10 at 80% power needs n≈783 (n≈3138 at IC 0.05).

Observations needed to resolve an IC at 80% power: 0.05→3138, 0.10→783, 0.15→347, 0.20→194

- distinct origin dates: 15 (2026-06-11 → 2026-07-19)
- sign balance: 18 positive / 14 negative
- observations dropped for lack of a realized outcome: 6

### 3M horizon

- **INSUFFICIENT-POWER** — no observation has a realized outcome yet

## Engine hook

- wired into the engine: **False**
- reason: no IC has cleared the Phase B gate; promotion requires a verdict other than INSUFFICIENT-POWER
- adapter ready at `value_gap_backtest.grinold_alpha (mirrors mc_v3.signal_alpha)`
