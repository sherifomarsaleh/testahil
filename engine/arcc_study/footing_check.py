#!/usr/bin/env python3
"""ARCC — every total a reader sees, reproduced from the rows printed above it.

The mechanism is engine/table_footing.py, shared with every other study; what is declared
here is only what is genuinely this study's own — the rows whose label reads like a total
and which are NOT a roll-up of the table they sit in.

WHAT THIS CAUGHT ON ITS FIRST RUN, all three in documents that had already passed the
recalculation gate, the prose-figure check, the scrub and the table-column audit:

  * Table 3 deducted provisions and credit losses in the model and did not print the line,
    so a reader adding the printed cost rows came out 82mn above the printed EBITDA.
  * Table 5 printed four CONTRACTUAL rates and labelled their blend "adopted 13.36%"; the
    printed four weight to 7.89%, and the adopted figure reproduces from the local-equivalent
    column the table did not carry.
  * Table 2 went from cement sold of 3.553Mt to total despatches of 4.854Mt with the export
    cement tonnage printed nowhere and the clinker tonnage eight rows up — and clinker is
    27% of this company's volume.

None of the three was a modelling error. In all three the model was right and the page could
not be reconciled by the reader it was written for, which is a class of defect every gate in
this repository was blind to: recalculation reconciles the model to ITSELF, and a per-figure
check cannot see a relationship BETWEEN figures.

A FALSE POSITIVE IS FIXED BY DECLARING THE EXCEPTION WITH ITS REASON, NEVER BY DELETING THE
TOTAL. A total a reader cannot reproduce is indistinguishable from one that is wrong, so the
reason is the whole point of the declaration.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
import table_footing as TF                                              # noqa: E402

STUDY = 'ARCC_Valuation_Study_03-09-2026_public.docx'
BIBLIO = 'ARCC_Bibliography_03-09-2026.docx'
DOCS = [STUDY, BIBLIO]

DECLARED = [
    (STUDY, 5, 'Total cash cost (EGP per tonne of cement)',
     'A PER-TONNE figure sitting under three EGP-million totals, and deliberately so: '
     'materials and fuel are driven by CLINKER produced because the kiln burns the fuel, '
     'while transportation and overheads are driven by cement DESPATCHED, so no single '
     'per-tonne rate describes all three and the table states each row in its own unit. '
     'The cash cost per tonne is the three totals divided by despatches, which is an '
     'operation on a quantity the column does not carry.'),
    (STUDY, 5, 'Blended realised price (EGP per tonne of cement)',
     'A blend ACROSS PRODUCTS — local cement, export cement and export clinker at their '
     'three derived prices — not a roll-up of the rows above it. The label carries the '
     'word "blended" in its ordinary sense.'),
    (STUDY, 8, 'Blended cost of capital',
     'The cost of equity and the after-tax cost of debt weighted by the equity and debt '
     'weights, which the table prints as a ROW rather than a column: this table is '
     'transposed, its rows being line items and its columns the explicit-window and '
     'terminal anchors. The weighted average is reproducible from the table by a reader '
     'and not by a column-wise instrument.'),
]

if __name__ == '__main__':
    examined, problems = TF.check([d for d in DOCS if os.path.exists(d)], DECLARED)
    assert examined, 'no tables examined — an empty result is not a clean result'
    for d in DECLARED:
        assert str(d[-1]).strip(), f'declared exception with no reason: {d[:3]}'
    sys.exit(TF.report(examined, problems, 'ARCC'))
