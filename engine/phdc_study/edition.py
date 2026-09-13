"""THE EDITION DATE OF THE PALM HILLS STUDY, WRITTEN ONCE.

The document builder derived it from a filename literal it carried itself --
which is one place rather than the three it replaced, and was a real improvement
-- but it is still a date typed by hand beside an answer that is computed. On
10-09-2026 the study was re-struck and the literal still named the 3 September
file, so the reissued document would have shipped under the superseded
edition's name.

The date lives here now. engine/doc_dates.py reads this module before it reaches
for any delivered filename, so the masthead, the filename and the supersession
sentence cannot disagree.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED. A delivered document is what a
reader received on that day; rebuilding over its filename destroys the only
record of what was said.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 10)

SUPERSEDES = (_dt.date(2026, 6, 11), _dt.date(2026, 8, 30),
              _dt.date(2026, 9, 2), _dt.date(2026, 9, 3))

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
WORDS = '%d %s %d' % (EDITION.day, EDITION.strftime('%B'), EDITION.year)
PRIOR_WORDS = '%d %s %d' % (SUPERSEDES[-1].day, SUPERSEDES[-1].strftime('%B'),
                            SUPERSEDES[-1].year)
STUDY_DOCX = 'PHDC_Valuation_Study_%s.docx' % _D
BIBLIO_DOCX = 'PHDC_Bibliography_%s.docx' % _D
MODEL_XLSX = 'PHDC_Valuation_Model_%s.xlsx' % _C


# THE PDF IS THE FILE A READER ACTUALLY OPENS, so it is named here too rather than
# spelled out again wherever one is baked or checked. Added 13-09-2026: three of the
# six delivered artefacts had no name in this module, so every script that touched a
# PDF typed the edition date itself -- which is the defect this file exists to stop,
# surviving in the half of the set it did not cover.
STUDY_PDF = STUDY_DOCX[:-len('.docx')] + '.pdf'
BIBLIO_PDF = BIBLIO_DOCX[:-len('.docx')] + '.pdf'
MODEL_PDF = MODEL_XLSX[:-len('.xlsx')] + '.pdf'
