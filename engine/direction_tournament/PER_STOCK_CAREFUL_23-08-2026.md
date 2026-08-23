# Committed drift — careful per-stock dossier (23-Aug-2026)

Exact production signal per market; per stock: rank skill with the house robust bootstrap (blocks {2,3,4}), direction hit rate with a Wilson interval, split-half consistency, and the plain call record (average move after UP calls vs after DOWN calls, per period, above cash). Disposition rule fixed BEFORE computing: suppress a stock's tilt only on robust-contrary + both-halves-negative + n≥40; weaker contrary reads are watch-flags, graded live.

## AE — signal mom_combo — committed tilt

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| ADCB | 1M | 174 | +0.049 | indeterminate | 50% (43%–57%) | +0.9% | +0.5% | yes |
| ADCB | 3M | 58 | +0.073 | indeterminate | 55% (42%–67%) | +3.9% | -0.0% | yes |
| ADIB | 1M | 174 | +0.097 | indeterminate | 57% (50%–64%) | +1.4% | +0.2% | yes |
| ADIB | 3M | 58 | +0.230 | borderline | 60% (48%–72%) | +4.8% | -0.2% | yes |
| ADNOCDIST | 1M | 91 | +0.029 | indeterminate | 56% (46%–66%) | +0.4% | +0.4% | no |
| ADNOCDIST | 3M | 30 | +0.184 | indeterminate | 60% (42%–75%) | +2.3% | -0.5% | yes |
| ADNOCDRILL | 1M | 45 | -0.193 | indeterminate | 53% (39%–67%) | -0.2% | +3.8% | no |
| ADNOCDRILL | 3M | 15 | -0.343 | short history | 40% (20%–64%) | +0.8% | — | yes |
| ADNOCGAS | 1M | 28 | -0.305 | indeterminate | 39% (24%–58%) | -0.5% | +0.3% | yes |
| ADNOCGAS | 3M | 9 | -0.200 | short history | 44% (19%–73%) | — | -0.4% | no |
| ADNOCLS | 1M | 25 | -0.388 | contrary (robust) | 36% (20%–56%) | +0.4% | +4.5% | no |
| ADNOCLS | 3M | 8 | -0.357 | short history | 50% (22%–78%) | +1.0% | — | no |
| AGTHIA | 1M | 174 | +0.130 | borderline | 55% (47%–62%) | +0.9% | -0.6% | yes |
| AGTHIA | 3M | 58 | +0.165 | indeterminate | 60% (48%–72%) | +2.6% | -1.7% | yes |
| AIRARABIA | 1M | 174 | +0.057 | indeterminate | 50% (43%–57%) | +0.7% | +1.6% | no |
| AIRARABIA | 3M | 58 | +0.062 | indeterminate | 53% (41%–66%) | +3.4% | +2.6% | no |
| ALDAR | 1M | 174 | +0.070 | indeterminate | 56% (48%–63%) | +1.4% | +0.5% | yes |
| ALDAR | 3M | 58 | +0.040 | indeterminate | 55% (42%–67%) | +3.4% | +3.0% | yes |
| ALPHADHABI | 1M | 48 | -0.113 | indeterminate | 50% (36%–64%) | -7.7% | -2.1% | yes |
| ALPHADHABI | 3M | 15 | -0.107 | short history | 60% (36%–80%) | — | -7.2% | yes |
| AMR | 1M | 31 | +0.046 | indeterminate | 61% (44%–76%) | — | -1.9% | yes |
| AMR | 3M | 10 | +0.055 | short history | 70% (40%–89%) | — | -6.7% | yes |
| BOROUGE | 1M | 37 | +0.099 | indeterminate | 65% (49%–78%) | +0.3% | -1.3% | yes |
| BOROUGE | 3M | 12 | +0.238 | short history | 67% (39%–86%) | -1.0% | -1.9% | yes |
| BURJEEL | 1M | 33 | +0.027 | indeterminate | 48% (32%–65%) | -1.6% | -3.4% | yes |
| BURJEEL | 3M | 11 | -0.018 | short history | 73% (43%–90%) | — | -10.5% | yes |
| DEWA | 1M | 39 | -0.111 | indeterminate | 59% (43%–73%) | -0.1% | -0.3% | no |
| DEWA | 3M | 13 | -0.159 | short history | 54% (29%–77%) | -1.0% | — | yes |
| DIB | 1M | 174 | +0.046 | indeterminate | 50% (43%–57%) | +0.5% | +1.0% | no |
| DIB | 3M | 58 | +0.093 | indeterminate | 41% (30%–54%) | +2.2% | +2.0% | no |
| DU | 1M | 174 | +0.128 | supports (robust) | 54% (47%–61%) | +1.2% | -0.1% | yes |
| DU | 3M | 58 | +0.165 | indeterminate | 52% (39%–64%) | +2.8% | +1.2% | yes |
| EAND | 1M | 174 | +0.151 | supports (robust) | 59% (51%–66%) | +1.2% | -0.6% | yes |
| EAND | 3M | 58 | +0.279 | supports (robust) | 59% (46%–70%) | +3.5% | -1.0% | yes |
| EMAAR | 1M | 174 | +0.155 | supports (robust) | 59% (51%–66%) | +1.5% | -0.4% | yes |
| EMAAR | 3M | 58 | +0.178 | indeterminate | 62% (49%–73%) | +5.1% | -1.5% | yes |
| EMAARDEV | 1M | 91 | +0.055 | indeterminate | 54% (44%–64%) | +1.7% | -0.8% | yes |
| EMAARDEV | 3M | 29 | +0.029 | indeterminate | 55% (38%–72%) | +6.0% | -0.5% | yes |
| EMPOWER | 1M | 32 | -0.301 | borderline | 47% (31%–64%) | -2.1% | +0.4% | yes |
| EMPOWER | 3M | 10 | -0.794 | short history | 0% (-0%–28%) | -8.0% | — | yes |
| ENBD | 1M | 173 | +0.013 | indeterminate | 56% (48%–63%) | +1.1% | +1.2% | no |
| ENBD | 3M | 57 | -0.068 | indeterminate | 47% (35%–60%) | +3.0% | +5.9% | yes |
| FAB | 1M | 174 | +0.064 | indeterminate | 51% (44%–58%) | +0.8% | +0.0% | no |
| FAB | 3M | 58 | +0.258 | supports (robust) | 60% (48%–72%) | +3.9% | -3.0% | yes |
| FERTIGLB | 1M | 44 | -0.059 | indeterminate | 55% (40%–68%) | -0.8% | -1.9% | yes |
| FERTIGLB | 3M | 14 | -0.191 | short history | 71% (45%–88%) | — | -2.4% | no |
| IHC | 1M | 140 | +0.366 | supports (robust) | 69% (60%–76%) | +7.1% | +0.6% | yes |
| IHC | 3M | 46 | +0.340 | borderline | 65% (51%–77%) | +17.6% | +7.5% | no |
| LULU | 1M | 8 | +0.190 | short history | 62% (31%–86%) | — | -2.8% | yes |
| LULU | 3M | 2 | — | insufficient | — | — | — | — |
| MODON | 1M | 68 | -0.142 | indeterminate | 43% (32%–55%) | +1.8% | +0.6% | no |
| MODON | 3M | 22 | -0.012 | short history | 55% (35%–73%) | +1.8% | +6.9% | yes |
| SALIK | 1M | 33 | -0.162 | indeterminate | 61% (44%–75%) | +1.6% | -0.6% | yes |
| SALIK | 3M | 10 | -0.139 | short history | 60% (31%–83%) | +7.3% | — | yes |
| TWOPOINTZERO | 1M | 43 | -0.167 | indeterminate | 54% (39%–68%) | -2.4% | -2.1% | no |
| TWOPOINTZERO | 3M | 14 | -0.367 | short history | 43% (21%–67%) | -9.3% | -3.5% | yes |

## EG — signal mom_combo — committed tilt

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| ABUK | 1M | 170 | +0.080 | indeterminate | 55% (48%–63%) | +1.3% | -0.9% | yes |
| ABUK | 3M | 56 | +0.158 | indeterminate | 61% (48%–72%) | +3.8% | -1.5% | yes |
| ADIB | 1M | 171 | +0.070 | indeterminate | 54% (47%–62%) | +1.8% | +0.0% | yes |
| ADIB | 3M | 56 | +0.187 | indeterminate | 55% (42%–68%) | +6.1% | +0.9% | yes |
| AMOC | 1M | 172 | +0.191 | supports (robust) | 55% (48%–62%) | +0.4% | -1.9% | yes |
| AMOC | 3M | 56 | +0.255 | supports (robust) | 55% (42%–68%) | +3.5% | -7.2% | yes |
| ARCC | 1M | 133 | +0.114 | indeterminate | 54% (46%–62%) | +1.6% | -1.9% | yes |
| ARCC | 3M | 43 | +0.188 | indeterminate | 58% (43%–72%) | +4.8% | -4.2% | yes |
| BTFH | 1M | 163 | -0.016 | indeterminate | 50% (43%–58%) | +0.9% | -0.1% | yes |
| BTFH | 3M | 54 | -0.164 | indeterminate | 41% (29%–54%) | -3.6% | +9.6% | yes |
| CCAP | 1M | 171 | +0.082 | indeterminate | 52% (44%–59%) | +0.0% | -1.3% | yes |
| CCAP | 3M | 56 | +0.293 | supports (robust) | 54% (41%–66%) | +1.8% | -4.6% | yes |
| CLHO | 1M | 107 | -0.063 | indeterminate | 52% (43%–62%) | +0.2% | +0.9% | no |
| CLHO | 3M | 35 | -0.041 | indeterminate | 40% (26%–56%) | -0.6% | +3.9% | no |
| COMI | 1M | 172 | +0.003 | indeterminate | 54% (47%–61%) | +1.2% | +0.6% | yes |
| COMI | 3M | 56 | -0.009 | indeterminate | 61% (48%–72%) | +3.0% | +4.0% | no |
| DSCW | 1M | 87 | +0.204 | supports (robust) | 64% (54%–74%) | +3.9% | -5.5% | yes |
| DSCW | 3M | 29 | +0.333 | indeterminate | 69% (51%–83%) | +8.6% | -11.1% | yes |
| EFID | 1M | 120 | +0.051 | indeterminate | 48% (40%–57%) | -0.6% | +0.5% | no |
| EFID | 3M | 39 | +0.085 | indeterminate | 51% (36%–66%) | -0.5% | +1.8% | no |
| EFIH | 1M | 43 | -0.132 | indeterminate | 44% (30%–59%) | -0.3% | +1.4% | yes |
| EFIH | 3M | 13 | -0.297 | short history | 31% (13%–58%) | -1.2% | — | no |
| EGAL | 1M | 170 | +0.110 | indeterminate | 52% (45%–60%) | +3.8% | -1.5% | yes |
| EGAL | 3M | 56 | +0.206 | indeterminate | 57% (44%–69%) | +10.1% | -3.1% | yes |
| EGCH | 1M | 172 | +0.011 | indeterminate | 45% (38%–52%) | -1.2% | +0.3% | no |
| EGCH | 3M | 56 | +0.095 | indeterminate | 50% (37%–63%) | +1.9% | -3.1% | yes |
| ELEC | 1M | 172 | +0.040 | indeterminate | 49% (42%–57%) | +1.1% | -0.0% | yes |
| ELEC | 3M | 56 | +0.133 | indeterminate | 61% (48%–72%) | +7.1% | -3.3% | yes |
| EMFD | 1M | 120 | -0.047 | indeterminate | 52% (44%–61%) | +0.5% | -0.2% | yes |
| EMFD | 3M | 40 | +0.041 | indeterminate | 55% (40%–69%) | +2.6% | -2.0% | yes |
| ETEL | 1M | 171 | +0.001 | indeterminate | 47% (40%–55%) | +0.2% | +0.1% | no |
| ETEL | 3M | 56 | +0.029 | indeterminate | 54% (41%–66%) | +1.9% | -0.2% | yes |
| FWRY | 1M | 69 | +0.173 | indeterminate | 61% (49%–72%) | +0.9% | -1.1% | no |
| FWRY | 3M | 22 | +0.155 | short history | 59% (39%–77%) | +3.8% | -4.6% | yes |
| GBCO | 1M | 171 | +0.015 | indeterminate | 52% (44%–59%) | +0.8% | -0.2% | no |
| GBCO | 3M | 56 | +0.033 | indeterminate | 55% (42%–68%) | +2.7% | -1.5% | yes |
| HELI | 1M | 171 | -0.005 | indeterminate | 49% (42%–57%) | +1.2% | -0.2% | no |
| HELI | 3M | 56 | +0.062 | indeterminate | 61% (48%–72%) | +5.9% | -3.1% | yes |
| HRHO | 1M | 171 | -0.041 | indeterminate | 50% (42%–57%) | +0.2% | +0.0% | no |
| HRHO | 3M | 56 | -0.011 | indeterminate | 50% (37%–63%) | +0.3% | +1.7% | no |
| ISPH | 1M | 89 | +0.105 | indeterminate | 52% (42%–62%) | +0.9% | -2.0% | no |
| ISPH | 3M | 29 | +0.103 | indeterminate | 55% (38%–72%) | +1.2% | -5.4% | no |
| JUFO | 1M | 171 | +0.025 | indeterminate | 53% (46%–60%) | +0.6% | +0.3% | no |
| JUFO | 3M | 56 | +0.048 | indeterminate | 52% (39%–64%) | +2.0% | +0.5% | yes |
| KABO | 1M | 170 | -0.018 | indeterminate | 48% (41%–56%) | +0.6% | +0.3% | no |
| KABO | 3M | 56 | -0.040 | indeterminate | 46% (34%–59%) | -0.1% | +4.4% | yes |
| LCSW | 1M | 170 | -0.002 | indeterminate | 47% (40%–55%) | -0.2% | +0.6% | no |
| LCSW | 3M | 56 | +0.022 | indeterminate | 46% (34%–59%) | -2.7% | +5.8% | yes |
| OCDI | 1M | 172 | +0.040 | indeterminate | 52% (45%–60%) | +1.3% | -0.4% | yes |
| OCDI | 3M | 56 | +0.053 | indeterminate | 54% (41%–66%) | +3.7% | -1.0% | yes |
| OIH | 1M | 160 | +0.048 | indeterminate | 50% (42%–58%) | +1.4% | -0.9% | yes |
| OIH | 3M | 52 | +0.058 | indeterminate | 56% (42%–68%) | +4.1% | -2.9% | yes |
| ORAS | 1M | 123 | -0.001 | indeterminate | 50% (42%–59%) | +1.6% | +0.2% | no |
| ORAS | 3M | 40 | -0.031 | indeterminate | 45% (31%–60%) | +4.2% | +2.3% | no |
| ORHD | 1M | 123 | +0.023 | indeterminate | 54% (45%–62%) | +2.5% | -0.5% | yes |
| ORHD | 3M | 41 | +0.045 | indeterminate | 51% (36%–66%) | +7.3% | +0.3% | yes |
| ORWE | 1M | 170 | +0.018 | indeterminate | 50% (43%–57%) | +0.1% | +0.7% | no |
| ORWE | 3M | 56 | +0.057 | indeterminate | 52% (39%–64%) | +2.2% | +0.7% | yes |
| PHAR | 1M | 170 | +0.065 | indeterminate | 55% (48%–63%) | +0.8% | -1.0% | yes |
| PHAR | 3M | 56 | +0.152 | indeterminate | 57% (44%–69%) | +0.8% | -1.4% | no |
| PHDC | 1M | 171 | -0.003 | indeterminate | 50% (43%–58%) | +0.8% | -0.2% | no |
| PHDC | 3M | 56 | +0.112 | indeterminate | 52% (39%–64%) | +5.2% | -5.8% | yes |
| PRDC | 1M | 43 | +0.016 | indeterminate | 44% (30%–59%) | +0.2% | +10.8% | no |
| PRDC | 3M | 13 | +0.346 | short history | 31% (13%–58%) | -0.5% | — | no |
| RAYA | 1M | 167 | -0.007 | indeterminate | 48% (41%–56%) | +1.4% | +1.9% | no |
| RAYA | 3M | 54 | -0.030 | indeterminate | 48% (35%–61%) | +5.2% | +4.3% | no |
| RMDA | 1M | 65 | -0.009 | indeterminate | 45% (33%–57%) | +1.0% | +0.1% | no |
| RMDA | 3M | 21 | -0.113 | short history | 52% (32%–72%) | +2.4% | +5.7% | no |
| SCEM | 1M | 171 | +0.076 | indeterminate | 56% (48%–63%) | +2.3% | -1.8% | yes |
| SCEM | 3M | 56 | +0.090 | indeterminate | 57% (44%–69%) | +4.3% | -3.6% | yes |
| SWDY | 1M | 172 | +0.106 | indeterminate | 51% (44%–58%) | +2.1% | -0.3% | yes |
| SWDY | 3M | 56 | +0.194 | indeterminate | 50% (37%–63%) | +6.2% | -0.0% | yes |
| TMGH | 1M | 171 | +0.037 | indeterminate | 52% (45%–59%) | +1.6% | -0.2% | no |
| TMGH | 3M | 56 | +0.065 | indeterminate | 52% (39%–64%) | +4.9% | -0.5% | yes |

## IN — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| INFY | 1M | 174 | +0.009 | indeterminate | 48% (41%–56%) | -0.1% | +0.6% | yes |
| INFY | 3M | 58 | +0.186 | supports (robust) | 62% (49%–73%) | +1.7% | -1.1% | yes |
| RELIANCE | 1M | 174 | -0.208 | contrary (robust) | 40% (33%–47%) | +0.0% | +2.2% | no |
| RELIANCE | 3M | 58 | -0.105 | indeterminate | 55% (42%–67%) | +1.8% | +1.9% | no |
| TMPV | 1M | 174 | +0.080 | indeterminate | 57% (50%–64%) | +0.6% | -1.0% | yes |
| TMPV | 3M | 58 | +0.142 | indeterminate | 57% (44%–69%) | +1.8% | -2.2% | yes |

## KR — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| KAKAO | 1M | 174 | +0.082 | indeterminate | 57% (50%–65%) | +0.7% | -0.7% | no |
| KAKAO | 3M | 58 | +0.126 | indeterminate | 53% (41%–66%) | +1.6% | -1.8% | no |
| LGES | 1M | 41 | -0.130 | indeterminate | 54% (39%–68%) | -4.0% | +0.7% | yes |
| LGES | 3M | 13 | -0.495 | short history | 46% (23%–71%) | — | -3.0% | no |
| SAMSUNG | 1M | 166 | +0.043 | indeterminate | 50% (42%–57%) | +1.2% | +0.8% | no |
| SAMSUNG | 3M | 54 | +0.105 | indeterminate | 46% (34%–59%) | +3.9% | +3.6% | no |

## QA — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| IQCD | 1M | 173 | +0.108 | indeterminate | 51% (44%–58%) | +0.1% | -0.6% | no |
| IQCD | 3M | 57 | +0.077 | indeterminate | 47% (35%–60%) | -1.0% | -0.1% | no |
| QGTS | 1M | 173 | +0.041 | indeterminate | 49% (42%–56%) | +0.4% | +0.3% | no |
| QGTS | 3M | 57 | +0.065 | indeterminate | 51% (38%–63%) | +1.3% | +0.8% | no |
| QNB | 1M | 173 | +0.016 | indeterminate | 52% (45%–59%) | +0.2% | +0.0% | yes |
| QNB | 3M | 57 | -0.033 | indeterminate | 47% (35%–60%) | -0.2% | +1.4% | no |

## SA — signal mom_12_1 — committed tilt

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| ACWA | 1M | 44 | +0.118 | indeterminate | 61% (47%–74%) | +1.7% | -3.8% | yes |
| ACWA | 3M | 14 | +0.051 | short history | 71% (45%–88%) | +2.7% | — | no |
| ALINMA | 1M | 172 | +0.055 | indeterminate | 53% (46%–60%) | +0.7% | +0.8% | no |
| ALINMA | 3M | 57 | -0.065 | indeterminate | 42% (30%–55%) | +0.9% | +4.8% | yes |
| ARAMCO | 1M | 66 | -0.061 | indeterminate | 47% (35%–59%) | -1.0% | +0.1% | no |
| ARAMCO | 3M | 22 | -0.285 | short history | 36% (20%–57%) | -3.8% | +0.7% | yes |
| ELM | 1M | 39 | +0.141 | indeterminate | 54% (39%–68%) | +1.9% | -2.5% | no |
| ELM | 3M | 12 | +0.378 | short history | 58% (32%–81%) | +6.5% | — | yes |
| EXTRA | 1M | 160 | +0.173 | supports (robust) | 57% (50%–65%) | +1.6% | -2.2% | yes |
| EXTRA | 3M | 52 | +0.140 | indeterminate | 54% (40%–67%) | +3.6% | -3.7% | yes |
| MAADEN | 1M | 172 | -0.019 | indeterminate | 51% (44%–58%) | +0.5% | +1.7% | no |
| MAADEN | 3M | 57 | -0.079 | indeterminate | 44% (32%–57%) | +1.0% | +6.9% | no |
| RAJHI | 1M | 172 | +0.030 | indeterminate | 49% (42%–57%) | +0.4% | +1.0% | no |
| RAJHI | 3M | 57 | +0.004 | indeterminate | 47% (35%–60%) | +1.2% | +3.0% | no |
| RIBL | 1M | 172 | +0.072 | indeterminate | 57% (50%–64%) | +0.8% | -0.2% | no |
| RIBL | 3M | 57 | +0.136 | indeterminate | 51% (38%–63%) | +1.5% | +0.3% | no |
| RIYADHCABLE | 1M | 30 | +0.165 | indeterminate | 57% (39%–73%) | +0.5% | -4.1% | yes |
| RIYADHCABLE | 3M | 10 | +0.309 | short history | 60% (31%–83%) | +1.4% | — | yes |
| SABIC | 1M | 172 | +0.102 | indeterminate | 56% (49%–64%) | +0.2% | -1.0% | yes |
| SABIC | 3M | 57 | +0.090 | indeterminate | 56% (43%–68%) | +0.1% | -2.5% | no |
| SAVOLA | 1M | 172 | +0.113 | indeterminate | 61% (54%–68%) | +1.0% | -1.3% | yes |
| SAVOLA | 3M | 57 | +0.188 | borderline | 58% (45%–70%) | +2.8% | -3.1% | yes |
| SNB | 1M | 125 | +0.082 | indeterminate | 52% (43%–61%) | +0.3% | -0.1% | yes |
| SNB | 3M | 42 | +0.048 | indeterminate | 55% (40%–69%) | +0.8% | -0.2% | no |
| STC | 1M | 172 | -0.095 | indeterminate | 51% (43%–58%) | +0.2% | +0.9% | yes |
| STC | 3M | 57 | -0.211 | indeterminate | 49% (37%–62%) | -0.4% | +4.9% | yes |

## US — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| AAPL | 1M | 174 | -0.136 | contrary (robust) | 52% (44%–59%) | +1.6% | +1.8% | yes |
| AAPL | 3M | 58 | -0.242 | contrary (robust) | 60% (48%–72%) | +5.2% | +4.0% | yes |
| NVDA | 1M | 174 | +0.055 | indeterminate | 55% (48%–62%) | +3.7% | +3.0% | yes |
| NVDA | 3M | 58 | +0.183 | indeterminate | 57% (44%–69%) | +11.3% | +9.9% | yes |
| TSLA | 1M | 174 | +0.003 | indeterminate | 48% (41%–56%) | +3.0% | +2.5% | yes |
| TSLA | 3M | 58 | -0.001 | indeterminate | 48% (36%–61%) | +7.1% | +12.1% | yes |

## XAU — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| GOLD | 1M | 187 | +0.090 | indeterminate | 49% (42%–56%) | +0.5% | +0.3% | no |
| GOLD | 3M | 62 | +0.111 | indeterminate | 48% (36%–61%) | +1.4% | +1.4% | no |
| SILVER | 1M | 174 | -0.017 | indeterminate | 50% (43%–57%) | +0.3% | +0.1% | yes |
| SILVER | 3M | 58 | -0.115 | indeterminate | 41% (30%–54%) | -1.1% | +2.1% | yes |

## XPT — signal mom_combo — NOT committed — evidence record only

| stock | clock | obs | rank skill | robust verdict | hit rate (95% CI) | after UP calls | after DOWN calls | split-half OK |
|---|---|---|---|---|---|---|---|---|
| PLATINUM | 1M | 173 | -0.084 | indeterminate | 44% (37%–52%) | -0.4% | +0.1% | no |
| PLATINUM | 3M | 57 | -0.018 | indeterminate | 54% (42%–67%) | +0.6% | -0.4% | no |

## Dispositions

- **No stock met the suppression bar.** No tilt is switched off; the market-level signal stands for every name.

Watch-flags (contrary or borderline, below the bar — recorded and graded live, not acted on):
  - ADIB (AE, 3M): rank skill +0.230, borderline
  - ADNOCDRILL (AE, 1M): rank skill -0.193, indeterminate
  - ADNOCGAS (AE, 1M): rank skill -0.305, indeterminate
  - ADNOCLS (AE, 1M): rank skill -0.388, contrary (robust)
  - AGTHIA (AE, 1M): rank skill +0.130, borderline
  - ALPHADHABI (AE, 1M): rank skill -0.113, indeterminate
  - DEWA (AE, 1M): rank skill -0.111, indeterminate
  - EMPOWER (AE, 1M): rank skill -0.301, borderline
  - ENBD (AE, 3M): rank skill -0.068, indeterminate
  - FERTIGLB (AE, 1M): rank skill -0.059, indeterminate
  - IHC (AE, 3M): rank skill +0.340, borderline
  - MODON (AE, 1M): rank skill -0.142, indeterminate
  - SALIK (AE, 1M): rank skill -0.162, indeterminate
  - TWOPOINTZERO (AE, 1M): rank skill -0.167, indeterminate
  - BTFH (EG, 3M): rank skill -0.164, indeterminate
  - CLHO (EG, 1M): rank skill -0.063, indeterminate
  - EFIH (EG, 1M): rank skill -0.132, indeterminate
  - RELIANCE (IN, 1M): rank skill -0.208, contrary (robust)
  - RELIANCE (IN, 3M): rank skill -0.105, indeterminate
  - LGES (KR, 1M): rank skill -0.130, indeterminate
  - ALINMA (SA, 3M): rank skill -0.065, indeterminate
  - ARAMCO (SA, 1M): rank skill -0.061, indeterminate
  - MAADEN (SA, 3M): rank skill -0.079, indeterminate
  - SAVOLA (SA, 3M): rank skill +0.188, borderline
  - STC (SA, 1M): rank skill -0.095, indeterminate
  - STC (SA, 3M): rank skill -0.211, indeterminate
  - AAPL (US, 1M): rank skill -0.136, contrary (robust)
  - AAPL (US, 3M): rank skill -0.242, contrary (robust)
  - SILVER (XAU, 3M): rank skill -0.115, indeterminate
  - PLATINUM (XPT, 1M): rank skill -0.084, indeterminate

Multiplicity note: ~186 stock-horizon tests at 90% CIs imply a handful of false single-test excursions by chance; the joint suppression rule keeps the expected false-suppression count well under one.