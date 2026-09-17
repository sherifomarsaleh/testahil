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

17-09-2026, AND THE REASON IT IS A NEW EDITION RATHER THAN A CORRECTION OF THE
LAST ONE. A forensic audit of a rebuild that had been struck outside this
repository was worked finding by finding; the response is
CRITIQUE_RESPONSE_17-09-2026.md. What changed here is not cosmetic: the 1Q2026
anchors moved from the release's rounded headline billions to its own income
statement in thousands, the minority's share of value moved from a single year
to the three-year mean on instruction, the price moved to the one the committed
library actually holds, five separate typed copies of that price were wired to
one registry row, the workbook's bridge and terminal were wired to the sheet
that computes them instead of carrying constants, and four prose surfaces that
described the model wrongly were corrected. A reader who received the 10
September file received different numbers under different labels, so it keeps
its own name and this one gets a new one.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 17)

SUPERSEDES = (_dt.date(2026, 6, 11), _dt.date(2026, 8, 30),
              _dt.date(2026, 9, 2), _dt.date(2026, 9, 3),
              _dt.date(2026, 9, 10))

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


# THE SUPERSEDED EDITION'S OWN DELIVERED FILES, named here for the same reason the
# current ones are. A supersession sentence that states what moved has to read the
# edition it superseded, and typing those figures is how the document came to say the
# rate "fell from 25.83% to 24.96%" -- 25.83% being this edition's own rating-basis
# alternative, never any edition's published rate.
_P = SUPERSEDES[-1]
PRIOR_STUDY_DOCX = 'PHDC_Valuation_Study_%s.docx' % _P.strftime('%d-%m-%Y')
PRIOR_MODEL_XLSX = 'PHDC_Valuation_Model_%s.xlsx' % _P.strftime('%d%m%Y')
