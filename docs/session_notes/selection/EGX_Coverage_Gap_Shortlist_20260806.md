# EGX coverage-gap shortlist — highly traded names NOT in Testahil (6-Aug-2026)

Supersedes the June-2026 `Highest traded stocks on EGX.xlsx`, which is now effectively
exhausted: every name on it is already covered except MFPC, AMOC, SKPC, MASR, EKHO (now
Valmore/VLMR) and PHAR.

## Live coverage baseline (read from the repo, not from memory)

`assets/markets.js` → `MARKET_OF`, market == EG — **32 names**:
ABUK ADIB BTFH CCAP CLHO COMI DSCW EFID EFIH EGAL ELEC EMFD ETEL FWRY GBCO HELI HRHO
ISPH JUFO KABO LCSW OCDI OIH ORAS ORHD ORWE PHDC PRDC RAYA RMDA SWDY TMGH.
(ELEC added 5-Aug-2026; study blocked at SIGCM pending official statements.)

NB: GitHub **API** access is blocked from the Cowork sandbox (HTTP 403 on
api.github.com); anonymous `raw.githubusercontent.com` reads work fine. Directory
listings therefore have to come from a generated file such as `assets/markets.js`, not
from the contents API.

## Uncovered EGX30 members — the exchange's own liquidity screen

The EGX30 selection rule is turnover + free-float cap, so membership is the cleanest
available "highly traded" filter. Six index slots are uncovered:

| Code | Company | ~Mkt cap | Note |
|---|---|---|---|
| EAST | Eastern Company (tobacco) | 113bn | Consumer-staples gap; decades of history; strong disclosure |
| EGCH | Egyptian Chemical Industries (Kima) | 30bn | ADDED to EGX30 Feb-2026 |
| ARCC | Arabian Cement | 22bn | Zero cement coverage today |
| MCQE | Misr Cement (Qena) | 19bn | Zero cement coverage today |
| AMOC | Alexandria Mineral Oils | 11bn | Refining/petchem gap |
| VLMR / VLMRA | Valmore Holding (ex-Egypt Kuwait Holding, EKHO) | 41bn | Dual line; reports in USD — FX complication for a local-nominal WACC |

## Large uncovered names outside the EGX30

MFPC (MOPCO, 123bn) · QNBE (QNB Alahli, 119bn) · ALCN (Alexandria Containers, 88bn) ·
HDBK (Housing & Development Bank, 76bn) · SCTS (57bn) · CIEB (Crédit Agricole Egypt,
30bn) · SKPC (20bn) · MASR (Madinet Masr, 15bn) · EGTS · TAQA Arabia · CIRA · MTIE ·
VALU · CNFN.

MFPC, SKPC, CIEB and MASR were all **deleted from the EGX30 at the Feb-2026 semi-annual
review** (additions were EFID, EGCH, HELI, OIH) — large but with slipping relative
turnover. MASR and CIEB moved into the EGX70 EWI.

## Actual July-2026 turnover leaders that are uncovered

Monthly value (Amwal Al Ghad, 2-Aug-2026): COMI 8.11bn · TMGH 7.32bn · **ZMID 5.33bn** ·
**KORA 4.73bn** · PHDC 4.68bn · BTFH 4.45bn.
Week 3 of July (Youm7, 25-Jul-2026): COMI · TMGH · PHDC · **ZMID** · **NIPH** · **GDWA** ·
BTFH · **MCRO** · ADIB · **SCEM**.

These are genuinely high-turnover but are small-cap retail/momentum flow, not
institutional depth — ZMID ~6bn cap, NIPH ~8bn, GDWA ~4bn, MCRO ~0.7bn. Treat turnover
rank alone as a misleading selector for this system.

**KORA (Qura/Kora for Energy Projects & Investment) is disqualified on history**: listed
and first traded **11-Jun-2026**, ~2 months of bars. Fails the history-span rule outright.

## Sector gaps in the existing 32-name panel

Cement (none) · ports & logistics (none) · education (none, CIRA/TALM) · consumer finance
(none, VALU/CNFN) · energy distribution (none, TAQA) · tobacco/staples (none, EAST) ·
banks — only COMI and ADIB against QNBE/HDBK/CIEB/SAUD/EXPA/FAIT available.

## Binding constraint is disclosure, not price data

ELEC proved the bottleneck is obtaining the company's own issued statements (SIGCM Rule
1/8), not OHLC. Prefer candidates with retrievable audited PDFs — EAST, AMOC, MFPC, QNBE,
ALCN, ARCC all have functioning IR disclosure — over high-turnover microcaps whose filings
are hard to source.

## Suggested order

1. **EAST** — biggest uncovered EGX30 name, deep history, clean disclosure, new sector.
2. **QNBE** or **HDBK** — second bank beyond COMI/ADIB; ADCB is already the bank-lens exemplar.
3. **MFPC** — 123bn cap, direct ABUK comparable, strengthens the fertilizer read.
4. **ARCC** or **MCQE** — opens cement.
5. **ALCN** — ports/Suez exposure, nothing like it in the panel.
6. **AMOC**, **EGCH**, **SKPC** — EGX30/petchem fill-ins.

Sources: repo `assets/markets.js`; stockanalysis.com EGX list; investing.com EGX30
components; EGX semi-annual index review press release eff. 1-Feb-2026 (mondovisione);
Amwal Al Ghad 2-Aug-2026; Youm7 25-Jul-2026; TradingView EGX movers.
