# Value-gap backtest — EG (Phase C)

Protocol: `Fundamental_MC_Integration_Protocol.md §8 (Phase C)`  
Signal: `G = ln(fair_base / spot) / sigma_h`, point-in-time from the git history of `assets/data.js`.  
Scored against forward log return **net of carry** via `direction_score.py` (Phase B). CRPS is not used.

### 1M horizon

- n = **41**
- IC (Spearman) = **-0.157**  (p=0.326, Pearson +0.006)
- IC 90% CI, block 2 = [-0.430, +0.178] → PARITY
- bootstrap verdict (blocks [2, 3, 4]) = **PARITY**
- hit rate = **53.7%** on 41 (95% CI 38.7%–67.9%, null 50%)
- LONO IC range [-0.238, -0.071], sign stable: True
- **VERDICT: INSUFFICIENT-POWER**
  - n=41 < 100. IC -0.157 is DESCRIPTIVE ONLY and must not be promoted: at n=41 an estimate this large is far more likely sampling noise than signal. Resolving a realistic value-signal IC of 0.10 at 80% power needs n≈783 (n≈3138 at IC 0.05).

Observations needed to resolve an IC at 80% power: 0.05→3138, 0.10→783, 0.15→347, 0.20→194

- distinct origin dates: 22 (2026-06-11 → 2026-08-06)
- sign balance: 21 positive / 20 negative
- observations dropped for lack of a realized outcome: 0

### 3M horizon

- **INSUFFICIENT-POWER** — no observation has a realized outcome yet

## Engine hook

- wired into the engine: **False**
- reason: no IC has cleared the Phase B gate; promotion requires a verdict other than INSUFFICIENT-POWER
- adapter ready at `value_gap_backtest.grinold_alpha (mirrors mc_v3.signal_alpha)`
