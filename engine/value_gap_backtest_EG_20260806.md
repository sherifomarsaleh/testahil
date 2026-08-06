# Value-gap backtest — EG (Phase C)

Protocol: `Fundamental_MC_Integration_Protocol.md §8 (Phase C)`  
Signal: `G = ln(fair_base / spot) / sigma_h`, point-in-time from the git history of `assets/data.js`.  
Scored against forward log return **net of carry** via `direction_score.py` (Phase B). CRPS is not used.

### 1M horizon

- n = **5**
- IC (Spearman) = **-0.600**  (p=0.285, Pearson -0.592)
- IC 90% CI, block 2 = [-1.000, +1.000] → PARITY
- bootstrap verdict (blocks [2, 3, 4]) = **BOUNDARY(PARITY-flagged)**
- hit rate = **80.0%** on 5 (95% CI 37.6%–96.4%, null 50%)
- LONO IC range [-0.800, -0.200], sign stable: True
- **VERDICT: INSUFFICIENT-POWER**
  - n=5 < 100. IC -0.600 is DESCRIPTIVE ONLY and must not be promoted: at n=5 an estimate this large is far more likely sampling noise than signal. Resolving a realistic value-signal IC of 0.10 at 80% power needs n≈783 (n≈3138 at IC 0.05).

Observations needed to resolve an IC at 80% power: 0.05→3138, 0.10→783, 0.15→347, 0.20→194

- distinct origin dates: 5 (2026-06-11 → 2026-06-25)
- sign balance: 5 positive / 0 negative  **— ONE-SIDED: the short side is untested, so the IC is a magnitude ordering within a single sign**
- observations dropped for lack of a realized outcome: 0

### 3M horizon

- **INSUFFICIENT-POWER** — no observation has a realized outcome yet

## Engine hook

- wired into the engine: **False**
- reason: no IC has cleared the Phase B gate; promotion requires a verdict other than INSUFFICIENT-POWER
- adapter ready at `value_gap_backtest.grinold_alpha (mirrors mc_v3.signal_alpha)`
