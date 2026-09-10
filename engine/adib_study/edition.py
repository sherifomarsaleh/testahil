"""THE EDITION DATE OF THE ADIB-EGYPT STUDY, WRITTEN ONCE.

Adopted 10-09-2026, after this study shipped its edition under three different
dates in one pass. The masthead said 9 September, the bibliography filename said
9 September, the workbook filename said 09092026 -- and the answer inside all
three had been re-struck that morning at EGP 43.39 against the 37.18 those dates
belonged to. Each site had typed the date for itself, so nothing could compare
them.

Worse, the masthead did not type it at all: engine/doc_dates.py falls back to
reading the DATE OUT OF THE DELIVERED FILENAMES when a study has no edition
module, and the newest filename on disk at the moment the builder runs is the
PREVIOUS edition -- the one it is about to supersede. A builder that reads the
name it is in the middle of writing can only ever be one edition behind.

So the date lives here, doc_dates.issue_date() reads this module before it
reaches for any filename, and every artefact name is derived from it.

THE PREVIOUS EDITIONS ARE NAMED, NOT DELETED. A delivered document is a
historical artefact: it is what a reader received on that day, and rebuilding
over its filename destroys the only record of what was said.
"""
import datetime as _dt

EDITION = _dt.date(2026, 9, 10)

SUPERSEDES = (_dt.date(2026, 9, 7), _dt.date(2026, 9, 9))   # delivered editions

_D = EDITION.strftime('%d-%m-%Y')
_C = EDITION.strftime('%d%m%Y')           # the workbook drops the separators

ISO = EDITION.isoformat()
WORDS = '%d %s %d' % (EDITION.day, EDITION.strftime('%B'), EDITION.year)
STUDY_DOCX = 'ADIB_Valuation_Study_%s.docx' % _D
BIBLIO_DOCX = 'ADIB_Bibliography_%s.docx' % _D
MODEL_XLSX = 'ADIB_Valuation_Model_%s.xlsx' % _C
