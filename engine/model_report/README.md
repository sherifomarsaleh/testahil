# THE MODEL REPORT

`MODEL_REPORT_09-08-2026.docx` is the document every TESTAHIL valuation study is modelled on
[adopted 19-Aug-2026, per instruction]. **Open it beside the study you are writing.**

It is `ADNOCLS_Valuation_Study_09-08-2026` (`engine/adnocls_study/` — the study, its Excel
model, its standalone bibliography, and `QC_GATE_09-08-2026.md`) **minus the section "What
changed in these editions, and why"**: edition history is internal QC evidence and belongs in
the QC gate and the critique adjudication, not in a document an external reader receives.

Match its sections list, its sheet list, its content and its research depth. Adapt the market,
the currency, the lens and the indicator set to the company's class — never the structure or
the depth.

ADNOCLS displaced SWDY under the standing one-in-one-out rule. The reference set is closed at
three: **ADNOCLS** (model report + operating-company lens pattern), **ADCB** (bank),
**ALPHADHABI** (holdco). `REFERENCE_SET` in `engine/research_protocol.py` asserts on exactly
those at import.

## Rebuilding it

```bash
python3 engine/model_report/build_model_report_docx.py          # rebuild from the exemplar
python3 engine/model_report/build_model_report_docx.py --check  # verify the built file
python3 engine/make_pdf.py engine/model_report/MODEL_REPORT_09-08-2026.docx   # render the PDF
```

The builder performs the subtraction rather than describing it, and asserts every edit. Beyond
removing the section it rescues one live caveat out of it into §7 (the sanctioned beta routine
returns 1.103 where the study's tables carry the adopted 1.085 — a live discrepancy, not
history), drops the matching edition paragraph from the READ FIRST box, and repairs the
sentence in "About this series" that pointed at the removed section. The inline "an earlier
edition of this study…" passages in 1.2, 1.7, 1.8 and 7 are deliberately kept: each prices a
live construction against the superseded one at the point the number is used.

The published ADNOCLS study itself is untouched — re-issuing it is a separate, explicitly
requested step.
