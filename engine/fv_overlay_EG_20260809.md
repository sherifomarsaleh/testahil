# Fair-value / MC overlay — EG (Phase A)

Protocol: `Fundamental_MC_Integration_Protocol.md (PROPOSED 6-Aug-2026)`  
Engine: nu=6.0, width_cal=0.951, overlay_active=True, cash hurdle rf=19.50%  
Names: 36 computed, 0 blocked

`G` is the fair-value gap in the name's own horizon volatility (drift-free). Probabilities are suppressed in NOT-EXPRESSIBLE per protocol §4.

| Ticker | Gap% | G 1M | band 1M | G 3M | band 3M | P(touch base) 1M | P(touch base) 3M | beats cash |
|---|---|---|---|---|---|---|---|---|
| HELI | +2% | +0.15 | IN-REACH | +0.08 | IN-REACH | 80%&dagger; | 90%&dagger; | no |
| OCDI | -4% | -0.31 | IN-REACH | -0.17 | IN-REACH | 59% | 73%&dagger; | no |
| HRHO | +3% | +0.33 | IN-REACH | +0.18 | IN-REACH | 67% | 85%&dagger; | no |
| PHDC | +6% | +0.54 | IN-REACH | +0.29 | IN-REACH | 51% | 76% | yes |
| CCAP | +7% | +0.52 | IN-REACH | +0.29 | IN-REACH | 51% | 75% | yes |
| LCSW | +9% | +0.56 | IN-REACH | +0.33 | IN-REACH | 47% | 71% | yes |
| ARCC | -7% | -0.74 | IN-REACH | -0.38 | IN-REACH | 31% | 56% | no |
| BTFH | -7% | -0.75 | IN-REACH | -0.39 | IN-REACH | 28% | 50% | no |
| ADIB | +10% | +0.93 | IN-REACH | +0.48 | IN-REACH | 29% | 62% | yes |
| JUFO | -10% | -0.97 | IN-REACH | -0.52 | IN-REACH | 20% | 41% | no |
| GBCO | +14% | +0.95 | IN-REACH | +0.53 | IN-REACH | 27% | 57% | yes |
| ETEL | +14% | +1.25 | STRETCH | +0.71 | IN-REACH | 17% | 47% | yes |
| ORWE | -10% | -1.45 | STRETCH | -0.73 | IN-REACH | 8% | 26% | no |
| PRDC | -16% | -1.16 | STRETCH | -0.73 | IN-REACH | 14% | 30% | no |
| EGAL | -17% | -1.97 | STRETCH | -0.95 | IN-REACH | 3% | 20% | no |
| ABUK | -17% | -1.84 | STRETCH | -1.00 | IN-REACH | 4% | 18% | no |
| COMI | -13% | -1.94 | STRETCH | -1.06 | STRETCH | 3% | 14% | no |
| SCEM | -33% | -2.47 | OUT-OF-REACH | -1.36 | STRETCH | 2% | 10% | no |
| ORAS | +29% | +2.92 | OUT-OF-REACH | +1.44 | STRETCH | 1% | 16% | yes |
| FWRY | -24% | -2.99 | OUT-OF-REACH | -1.49 | STRETCH | 1% | 7% | no |
| RAYA | -28% | -2.81 | OUT-OF-REACH | -1.52 | STRETCH | 1% | 7% | no |
| ORHD | +34% | +2.94 | OUT-OF-REACH | +1.54 | STRETCH | 1% | 13% | yes |
| SWDY | -34% | -3.28 | OUT-OF-REACH | -1.93 | STRETCH | 0% | 4% | no |
| ISPH | +52% | +3.81 | OUT-OF-REACH | +2.05 | OUT-OF-REACH | 0% | 5% | yes |
| AMOC | -35% | -3.88 | OUT-OF-REACH | -2.24 | OUT-OF-REACH | 0% | 2% | no |
| TMGH | +46% | +4.17 | NOT-EXPRESSIBLE | +2.29 | OUT-OF-REACH | — | 4% | yes |
| CLHO | -46% | -4.35 | NOT-EXPRESSIBLE | -2.45 | OUT-OF-REACH | — | 2% | no |
| EFIH | -40% | -4.73 | NOT-EXPRESSIBLE | -2.51 | OUT-OF-REACH | — | 1% | no |
| EMFD | +72% | +5.92 | NOT-EXPRESSIBLE | +3.16 | OUT-OF-REACH | — | 1% | yes |
| RMDA | -44% | -6.60 | NOT-EXPRESSIBLE | -3.18 | OUT-OF-REACH | — | 1% | no |
| OIH | -47% | -6.55 | NOT-EXPRESSIBLE | -3.45 | OUT-OF-REACH | — | 0% | no |
| DSCW | -55% | -8.06 | NOT-EXPRESSIBLE | -4.09 | NOT-EXPRESSIBLE | — | — | no |
| KABO | -73% | -10.17 | NOT-EXPRESSIBLE | -5.44 | NOT-EXPRESSIBLE | — | — | no |
| EGCH | -74% | -12.98 | NOT-EXPRESSIBLE | -6.79 | NOT-EXPRESSIBLE | — | — | no |
| ELEC | -84% | -19.41 | NOT-EXPRESSIBLE | -10.10 | NOT-EXPRESSIBLE | — | — | no |
| EFID | -0% | -0.01 | IN-REACH | -0.00 | IN-REACH | 85%&dagger; | 90%&dagger; | no |

- **IN-REACH** — 1M: 12/36, 3M: 17/36
- **STRETCH** — 1M: 6/36, 3M: 7/36
- **OUT-OF-REACH** — 1M: 8/36, 3M: 8/36
- **NOT-EXPRESSIBLE** — 1M: 10/36, 3M: 4/36

&dagger; already converged (|G| <= 0.25): the fair value sits inside the horizon's own noise, so a high P(touch) means spot is already at fair value — the probability is correct but carries no information about the thesis.

**Informative rows** (neither suppressed nor already converged) — 1M: 24/36, 3M: 28/36.

Self-test — reconstructed cone vs published, worst relative deviation: 1M 0.324%, 3M 0.481% (tolerance 2%).
