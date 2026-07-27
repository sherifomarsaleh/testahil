# SHADOW SELECTION COHORTS — APPEND-ONLY LEDGER

**UNPUBLISHED.** Forward out-of-sample evidence for the selection engine, filed
*before* outcomes are known and never retro-edited. Nothing here appears on
testahil.com — publication requires a factor to pass the pre-registration's §6
adoption rules first. One cohort ≈ one observation (§2): grading reports numbers,
never verdicts.

**Grading spec (fixed for all cohorts):** at each market's anchor + 60 own-calendar
sessions, compute forward log return per name; within-market percentile ranks; pooled
Spearman IC per factor (same estimator as the binding runs) + per-market ICs; append
results below the cohort entry with the grading date and data commit. A cohort grades
only when all three markets have resolved. After grading, file the next cohort at the
then-latest anchors. F5 is retired (UNTESTABLE) and is not scored.

---

## Cohort #1 — filed 27-Jul-2026 (status: PENDING, grades ~late Oct 2026)

Anchors (last session per staged library): **EG 2026-07-22 · AE 2026-07-24 ·
SA 2026-07-26.** Data: EG = repo `cd68546`; AE/SA = 27-Jul long exports (gate docs).
Factor logic identical to the full-power run (RAYA excluded from F4; >20%
degenerate-bars guard; admissibility per §3).

### F6 — 52w-high proximity (PRIMARY; lead candidate, single-only at full power)

EG (30 names, best→worst): ORHD 1.0000 · KABO 1.0000 · EFIH 0.9983 · HELI 0.9952 ·
CLHO 0.9941 · ADIB 0.9940 · TMGH 0.9866 · COMI 0.9755 · CCAP 0.9667 · LCSW 0.9666 ·
PRDC 0.9655 · OCDI 0.9649 · RMDA 0.9414 · GBCO 0.9408 · EMFD 0.9400 · RAYA 0.9361 ·
OIH 0.9304 · ORWE 0.9278 · PHDC 0.9271 · ISPH 0.9200 · ETEL 0.9141 · JUFO 0.9088 ·
FWRY 0.9082 · DSCW 0.9074 · ORAS 0.8921 · EGAL 0.8909 · HRHO 0.8733 · EFID 0.8602 ·
BTFH 0.8583 · ABUK 0.7691

AE (18): IHC 0.9406 · EAND 0.9340 · FAB 0.9014 · ADNOCGAS 0.8978 · ADCB 0.8782 ·
DEWA 0.8530 · ENBD 0.8168 · SALIK 0.7985 · BURJEEL 0.7792 · ADIB 0.7752 ·
LULU 0.7619 · AGTHIA 0.7323 · DIB 0.7206 · EMAARDEV 0.6580 · ALDAR 0.6504 ·
EMAAR 0.6480 · TWOPOINTZERO 0.6319 · ALPHADHABI 0.5868

SA (11): STC 0.9540 · ARAMCO 0.9514 · RIBL 0.9360 · ALINMA 0.9344 · SNB 0.8871 ·
RAJHI 0.8796 · SABIC 0.8320 · ACWA 0.7688 · EXTRA 0.7370 · MAADEN 0.7321 · ELM 0.7007

### Appendix — other live factors (informational; percentile top-5 / bottom-5)

- **F1 momentum (+):** EG top ETEL, RAYA, ORAS, ADIB, EFID / bottom KABO, LCSW, ORWE,
  BTFH, DSCW. AE top ENBD, ADNOCGAS, EAND, DEWA, SALIK / bottom EMAAR, BURJEEL, LULU,
  DIB, ALPHADHABI. SA top ALINMA, MAADEN, SNB, ARAMCO, STC / bottom RIBL, SABIC,
  ACWA, EXTRA, ELM.
- **F2 short-term reversal (−; scored contrarian):** EG high-F2 KABO, PRDC, HELI,
  LCSW, OCDI / low RMDA, PHDC, ISPH, JUFO, ORAS. AE high FAB, BURJEEL, EAND, ADIB,
  ENBD / low SALIK, ALDAR, EMAAR, ALPHADHABI, AGTHIA. SA high RIBL, ARAMCO, SNB,
  SABIC, STC / low MAADEN, ACWA, ELM, ALINMA, EXTRA.
- **F3 long-term reversal (−; scored contrarian):** EG (28 names) high EGAL, TMGH,
  GBCO, LCSW, ADIB / low ABUK, RAYA, HELI, CLHO, FWRY. AE (12) high ADIB, EMAARDEV,
  EMAAR, IHC, ALDAR / low FAB, EAND, AGTHIA, ALPHADHABI. SA (9) high MAADEN, ALINMA,
  RAJHI, RIBL / low ARAMCO, STC, SABIC.
- **F4 low volatility (+):** EG (29; RAYA excluded) top ORWE, HRHO, COMI, TMGH, BTFH /
  bottom EFID, GBCO, PRDC, CCAP, CLHO. AE (17) top IHC, ADNOCGAS, EAND, AGTHIA, DIB /
  bottom EMAAR, BURJEEL, ENBD, TWOPOINTZERO, EMAARDEV. SA top STC, ARAMCO, ALINMA,
  RIBL, EXTRA / bottom SABIC, SNB, MAADEN, ELM, ACWA.

Full per-name values for every factor: `shadow_cohort.py` output against the staged
libraries (reproducible from the repo once the long AE/SA exports are committed).

<!-- Grading results are appended below this line by the monthly cycle. -->
