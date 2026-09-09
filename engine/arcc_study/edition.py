"""THE EDITION DATE OF THE ARCC STUDY, WRITTEN ONCE.

The third of these modules, and by now the pattern rather than the exception. ARCC
was the better-behaved case: compute.py already held an EDITION_DATE constant and
its meta block read from it. But the FILENAMES were still typed — in the two
document builders, the workbook builder, the driver test and a scrub assertion
inside compute.py itself — so the constant governed what the document SAID about
its edition while five other strings governed what it was CALLED.

That is the same defect TMGH shipped with, split across two halves that happened
to agree. They agree until an edition changes, which is exactly when it matters.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED. Adding a section to a delivered
document is a new edition and not an edit: the 03-09 file is what a reader received
on the third, and rebuilding over its name would destroy the only record of it.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 9)

SUPERSEDES = (_dt.date(2026, 8, 6), _dt.date(2026, 8, 8),
              _dt.date(2026, 9, 2), _dt.date(2026, 9, 3))

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
STUDY_DOCX = 'ARCC_Valuation_Study_%s_public.docx' % _D
MODEL_XLSX = 'ARCC_Valuation_Model_%s_public.xlsx' % _C
BIBLIO_DOCX = 'ARCC_Bibliography_%s.docx' % _D

#: what the delivered-document scrub must have covered — derived, never listed twice
DELIVERED = (STUDY_DOCX, BIBLIO_DOCX)


def prior(pattern):
    """The same artefact under a superseded edition, oldest first."""
    return [pattern.replace(_D, d.strftime('%d-%m-%Y')).replace(_C, d.strftime('%d%m%Y'))
            for d in SUPERSEDES]
