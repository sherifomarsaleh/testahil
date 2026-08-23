# Committed drift — per-ticker backtest (23-Aug-2026)

The exact production signal per market (AE/EG: combined 6+12-month momentum; SA: 12-month momentum), each name's own full cleaned history, month-end origins, non-overlapping forwards, excess of carry. Per-name samples are small by nature — the market-pooled tournament (leave-one-name-out checked) is the statistical basis of the adoption; this table is the per-name due-diligence record, contrary names included.

## AE — signal mom_combo — 28 tickers

| ticker | 1M obs | 1M hit | 1M rank skill | 1M verdict | 3M obs | 3M hit | 3M rank skill | 3M verdict |
|---|---|---|---|---|---|---|---|---|
| ADCB | 174 | 50% | +0.049 | supports | 58 | 55% | +0.073 | supports |
| ADIB | 174 | 57% | +0.097 | supports | 58 | 60% | +0.230 | supports |
| ADNOCDIST | 91 | 56% | +0.029 | flat | 30 | 60% | +0.184 | supports |
| ADNOCDRILL | 45 | 53% | -0.193 | contrary | 15 | 40% | -0.343 | short history |
| ADNOCGAS | 28 | 39% | -0.305 | contrary | 9 | 44% | -0.200 | short history |
| ADNOCLS | 25 | 36% | -0.388 | contrary | 8 | 50% | -0.357 | short history |
| AGTHIA | 174 | 55% | +0.130 | supports | 58 | 60% | +0.165 | supports |
| AIRARABIA | 174 | 50% | +0.057 | supports | 58 | 53% | +0.062 | supports |
| ALDAR | 174 | 56% | +0.070 | supports | 58 | 55% | +0.040 | supports |
| ALPHADHABI | 48 | 50% | -0.113 | contrary | 15 | 60% | -0.107 | short history |
| AMR | 31 | 61% | +0.046 | supports | 10 | 70% | +0.055 | short history |
| BOROUGE | 37 | 65% | +0.099 | supports | 12 | 67% | +0.238 | short history |
| BURJEEL | 33 | 48% | +0.027 | flat | 11 | 73% | -0.018 | short history |
| DEWA | 39 | 59% | -0.111 | contrary | 13 | 54% | -0.159 | short history |
| DIB | 174 | 50% | +0.046 | supports | 58 | 41% | +0.093 | supports |
| DU | 174 | 54% | +0.128 | supports | 58 | 52% | +0.165 | supports |
| EAND | 174 | 59% | +0.151 | supports | 58 | 59% | +0.279 | supports |
| EMAAR | 174 | 59% | +0.155 | supports | 58 | 62% | +0.178 | supports |
| EMAARDEV | 91 | 54% | +0.055 | supports | 29 | 55% | +0.029 | flat |
| EMPOWER | 32 | 47% | -0.301 | contrary | 10 | 0% | -0.794 | short history |
| ENBD | 173 | 56% | +0.013 | flat | 57 | 47% | -0.068 | contrary |
| FAB | 174 | 51% | +0.064 | supports | 58 | 60% | +0.258 | supports |
| FERTIGLB | 44 | 55% | -0.059 | contrary | 14 | 71% | -0.191 | short history |
| IHC | 140 | 69% | +0.366 | supports | 46 | 65% | +0.340 | supports |
| LULU | 8 | 62% | +0.190 | short history | 2 | — | — | short history |
| MODON | 68 | 43% | -0.142 | contrary | 22 | 55% | -0.012 | short history |
| SALIK | 33 | 61% | -0.162 | contrary | 10 | 60% | -0.139 | short history |
| TWOPOINTZERO | 43 | 54% | -0.167 | contrary | 14 | 43% | -0.367 | short history |

3M summary: 12 support · 1 flat · 1 contrary · 14 short-history

## EG — signal mom_combo — 37 tickers

| ticker | 1M obs | 1M hit | 1M rank skill | 1M verdict | 3M obs | 3M hit | 3M rank skill | 3M verdict |
|---|---|---|---|---|---|---|---|---|
| ABUK | 170 | 55% | +0.080 | supports | 56 | 61% | +0.158 | supports |
| ADIB | 171 | 54% | +0.070 | supports | 56 | 55% | +0.187 | supports |
| AMOC | 172 | 55% | +0.191 | supports | 56 | 55% | +0.255 | supports |
| ARCC | 133 | 54% | +0.114 | supports | 43 | 58% | +0.188 | supports |
| BTFH | 163 | 50% | -0.016 | flat | 54 | 41% | -0.164 | contrary |
| CCAP | 171 | 52% | +0.082 | supports | 56 | 54% | +0.293 | supports |
| CLHO | 107 | 52% | -0.063 | contrary | 35 | 40% | -0.041 | contrary |
| COMI | 172 | 54% | +0.003 | flat | 56 | 61% | -0.009 | flat |
| DSCW | 87 | 64% | +0.204 | supports | 29 | 69% | +0.333 | supports |
| EFID | 120 | 48% | +0.051 | supports | 39 | 51% | +0.085 | supports |
| EFIH | 43 | 44% | -0.132 | contrary | 13 | 31% | -0.297 | short history |
| EGAL | 170 | 52% | +0.110 | supports | 56 | 57% | +0.206 | supports |
| EGCH | 172 | 45% | +0.011 | flat | 56 | 50% | +0.095 | supports |
| ELEC | 172 | 49% | +0.040 | supports | 56 | 61% | +0.133 | supports |
| EMFD | 120 | 52% | -0.047 | contrary | 40 | 55% | +0.041 | supports |
| ETEL | 171 | 47% | +0.001 | flat | 56 | 54% | +0.029 | flat |
| FWRY | 69 | 61% | +0.173 | supports | 22 | 59% | +0.155 | short history |
| GBCO | 171 | 52% | +0.015 | flat | 56 | 55% | +0.033 | supports |
| HELI | 171 | 49% | -0.005 | flat | 56 | 61% | +0.062 | supports |
| HRHO | 171 | 50% | -0.041 | contrary | 56 | 50% | -0.011 | flat |
| ISPH | 89 | 52% | +0.105 | supports | 29 | 55% | +0.103 | supports |
| JUFO | 171 | 53% | +0.025 | flat | 56 | 52% | +0.048 | supports |
| KABO | 170 | 48% | -0.018 | flat | 56 | 46% | -0.040 | contrary |
| LCSW | 170 | 47% | -0.002 | flat | 56 | 46% | +0.022 | flat |
| OCDI | 172 | 52% | +0.040 | supports | 56 | 54% | +0.053 | supports |
| OIH | 160 | 50% | +0.048 | supports | 52 | 56% | +0.058 | supports |
| ORAS | 123 | 50% | -0.001 | flat | 40 | 45% | -0.031 | contrary |
| ORHD | 123 | 54% | +0.023 | flat | 41 | 51% | +0.045 | supports |
| ORWE | 170 | 50% | +0.018 | flat | 56 | 52% | +0.057 | supports |
| PHAR | 170 | 55% | +0.065 | supports | 56 | 57% | +0.152 | supports |
| PHDC | 171 | 50% | -0.003 | flat | 56 | 52% | +0.112 | supports |
| PRDC | 43 | 44% | +0.016 | flat | 13 | 31% | +0.346 | short history |
| RAYA | 171 | 48% | -0.014 | flat | 56 | 48% | -0.040 | contrary |
| RMDA | 65 | 45% | -0.009 | flat | 21 | 52% | -0.113 | short history |
| SCEM | 171 | 56% | +0.076 | supports | 56 | 57% | +0.090 | supports |
| SWDY | 172 | 51% | +0.106 | supports | 56 | 50% | +0.194 | supports |
| TMGH | 171 | 52% | +0.037 | supports | 56 | 52% | +0.065 | supports |

3M summary: 24 support · 4 flat · 5 contrary · 4 short-history

## SA — signal mom_12_1 — 13 tickers

| ticker | 1M obs | 1M hit | 1M rank skill | 1M verdict | 3M obs | 3M hit | 3M rank skill | 3M verdict |
|---|---|---|---|---|---|---|---|---|
| ACWA | 44 | 61% | +0.118 | supports | 14 | 71% | +0.051 | short history |
| ALINMA | 172 | 53% | +0.055 | supports | 57 | 42% | -0.065 | contrary |
| ARAMCO | 66 | 47% | -0.061 | contrary | 22 | 36% | -0.285 | short history |
| ELM | 39 | 54% | +0.141 | supports | 12 | 58% | +0.378 | short history |
| EXTRA | 160 | 57% | +0.173 | supports | 52 | 54% | +0.140 | supports |
| MAADEN | 172 | 51% | -0.019 | flat | 57 | 44% | -0.079 | contrary |
| RAJHI | 172 | 49% | +0.030 | flat | 57 | 47% | +0.004 | flat |
| RIBL | 172 | 57% | +0.072 | supports | 57 | 51% | +0.136 | supports |
| RIYADHCABLE | 30 | 57% | +0.165 | supports | 10 | 60% | +0.309 | short history |
| SABIC | 172 | 56% | +0.102 | supports | 57 | 56% | +0.090 | supports |
| SAVOLA | 172 | 61% | +0.113 | supports | 57 | 58% | +0.188 | supports |
| SNB | 126 | 52% | +0.081 | supports | 42 | 55% | +0.048 | supports |
| STC | 172 | 51% | -0.095 | contrary | 57 | 49% | -0.211 | contrary |

3M summary: 5 support · 1 flat · 3 contrary · 4 short-history
