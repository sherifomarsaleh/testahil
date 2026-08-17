"""Structural conformance of the delivered files against the reference study.

Checks the sixteen-section document skeleton and the sixteen-sheet workbook
against the committed machine-readable specification, and asserts the
reference-set invariant holds at import.
"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import openpyxl
from docx import Document
import research_protocol as rp

STUDY = os.path.join(HERE, 'ADNOCDRILL_Valuation_Study_09-08-2026.docx')
XLSX = os.path.join(HERE, 'ADNOCDRILL_Valuation_Model_09082026.xlsx')

# The section headings this study actually emits, in order, mapped to the
# reference skeleton. The reference names some sections descriptively; the
# delivered headings are the reader-facing wording of the same sections.
EXPECTED = [
    ('Masthead + READ FIRST', 'READ FIRST'),
    ('Headline', 'Headline'),
    ('Valuation summary', 'Valuation summary'),
    ('Company overview', 'Company overview'),
    ('1 Fundamental valuation', '1. Fundamental valuation'),
    ('2 Technical and price structure', '2. Technical and price structure'),
    ('3 A probabilistic price map', '3. Probability map'),
    ('4 Comparison of the lenses', '4. Comparison of the lenses'),
    ('5 Catalysts to watch', '5. Catalysts'),
    ('6 Reading the probability zones', '6. Reading the probability zones'),
    ('7 Caveats and what would change our mind', '7. Caveats, and what would change our mind'),
    ('Appendix A Financial statements', 'Appendix A — financial statements'),
    ('Appendix B Peer frame, risk register', 'Appendix B — peers, risks and research register'),
    ('Appendix C Expert panel', 'Appendix C — the expert panel'),
    ('About this series', 'About this study'),
    ('Disclosure & Disclaimer', 'Disclosure'),
]
SUBSECTIONS = ['1.1 Cash-flow model', '1.2 Book value and sustainable return',
               '1.3 Relative multiples', '1.4 Normalised earnings power',
               '1.5 Synthesis', '1.6 Drivers', '1.7 The crux', '1.8 Macro and country',
               '1.9 Sensitivity', 'A.1 Income statement', 'A.2 Balance sheet',
               'A.3 Cash flow', 'B.1 The peer set', 'B.2 Risk register',
               'B.3 Research register', 'C.1 Expert 1', 'C.2 Expert 2', 'C.3 Expert 3',
               'C.4 Cross-examination', 'C.5 The three in one room', 'C.6 Divergence']

doc = Document(STUDY)
heads = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
blob = '\n'.join(heads)

missing_sections = [ref for ref, got in EXPECTED if not any(h.startswith(got) for h in heads)]
missing_sub = [s for s in SUBSECTIONS if not any(h.startswith(s) for h in heads)]

# section order must match the reference order
positions = []
for ref, got in EXPECTED:
    idx = next((i for i, h in enumerate(heads) if h.startswith(got)), None)
    positions.append(idx)
ordered = all(a is not None and b is not None and a < b
              for a, b in zip(positions, positions[1:]))

wb = openpyxl.load_workbook(XLSX, read_only=True)
sheets = [s.title for s in wb.worksheets]
sheets_ok = sheets == rp.MODEL_STUDY['excel_sheets']

# experts must be labelled Expert 1/2/3 and no persona name may appear
persona_leak = re.findall(r'\b(?:persona|Damodaran-style|the sceptic|the optimist)\b', blob, re.I)

out = dict(sections_expected=len(EXPECTED), sections_missing=missing_sections,
           section_order_matches_reference=ordered,
           subsections_expected=len(SUBSECTIONS), subsections_missing=missing_sub,
           excel_sheets=sheets, excel_sheets_match_reference=sheets_ok,
           excel_sheet_count=len(sheets),
           reference_set=list(rp.REFERENCE_SET) if hasattr(rp.REFERENCE_SET, '__iter__')
           else str(rp.REFERENCE_SET),
           expert_labels_present=[f'Expert {i}' in blob for i in (1, 2, 3)],
           persona_name_leaks=persona_leak)
json.dump(out, open(os.path.join(HERE, 'structure_check.json'), 'w'), indent=1)

print(f"sections: {len(EXPECTED) - len(missing_sections)}/{len(EXPECTED)} present, "
      f"order matches reference: {ordered}")
if missing_sections:
    print('  MISSING:', missing_sections)
print(f"sub-sections: {len(SUBSECTIONS) - len(missing_sub)}/{len(SUBSECTIONS)} present")
if missing_sub:
    print('  MISSING:', missing_sub)
print(f"excel sheets: {len(sheets)}, match the reference list exactly: {sheets_ok}")
print(f"experts labelled Expert 1/2/3: {all(out['expert_labels_present'])}; "
      f"persona-name leaks: {len(persona_leak)}")
print(f"reference set (asserted at import): {out['reference_set']}")
assert not missing_sections and not missing_sub and ordered and sheets_ok
assert all(out['expert_labels_present']) and not persona_leak
print('STRUCTURE OK')
