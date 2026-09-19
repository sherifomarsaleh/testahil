"""THE EDITION DATE OF THE EGCH STUDY, WRITTEN ONCE.

It was derived from a filename literal carried in docx_egch.py and again in
docx_biblio.py -- two places, each parsing a date back out of a string it typed
itself. On 10-09-2026 the study was re-struck and both still named the
5 September file.

Worse than a stale name: the strike moved the answer and only compute.py's half
of study_numbers.json was regenerated, so lenses.json, the workbook and the
delivered document went on carrying EGP 4.0396 while the model said 4.8990 --
21% apart, with recalc.py failing 10 of its 16 headline reconciliations and
saying so out loud. A study's own red gate is not a warning to be carried; it is
the study telling you it cannot be issued.

The date lives here now, doc_dates.py reads it before it reaches for any
delivered filename, and every artefact name is derived from it.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 10)

SUPERSEDES = (_dt.date(2026, 8, 8), _dt.date(2026, 9, 1), _dt.date(2026, 9, 3),
              _dt.date(2026, 9, 5))

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')

ISO = EDITION.isoformat()
WORDS = '%d %s %d' % (EDITION.day, EDITION.strftime('%B'), EDITION.year)
PRIOR_WORDS = '%d %s %d' % (SUPERSEDES[-1].day, SUPERSEDES[-1].strftime('%B'),
                            SUPERSEDES[-1].year)
STUDY_DOCX = 'EGCH_Valuation_Study_%s.docx' % _D
BIBLIO_DOCX = 'EGCH_Bibliography_%s.docx' % _D
MODEL_XLSX = 'EGCH_Valuation_Model_%s.xlsx' % _C
STUDY_PDF = STUDY_DOCX[:-5] + '.pdf'
BIBLIO_PDF = BIBLIO_DOCX[:-5] + '.pdf'
MODEL_PDF = MODEL_XLSX[:-5] + '.pdf'
